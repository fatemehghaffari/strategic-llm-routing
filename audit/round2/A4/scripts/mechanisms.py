"""Mechanisms and the strategic layer for the RouterBench calibrated simulation.

CALIBRATED SIMULATION.  The capability functions M_i(x) are MEASURED from
RouterBench's published per-query outcome scores.  The strategic behaviour is
SIMULATED: no provider in RouterBench chose a target, and nothing here is
evidence about how any real provider behaves.

Implemented:
  MESP        Section 3, the scalar mechanism: one number elicited per agent.
  PLMESP      Section 4.3, one independent MESP inside each finite context.
  CGMESP      Section 4.4, one independent MESP inside each grid cell, with the
              oscillation allowance rho_n added to the price shading.
  Router      a quality-estimating router of the kind used in the LLM routing
              literature: estimate per-context quality from observed outcomes
              and route to the best, with greedy / epsilon-greedy / UCB
              exploration.  It has no price, no monitor and no fallback.
              THIS IS A POLICY CLASS, NOT A REIMPLEMENTATION OF ANY PUBLISHED
              SYSTEM, and no result here is a benchmark of any named method.
  oracle / honest benchmark: computed in closed form from M and mu.

Monitor rungs (ablation axis):
  "anytime"   the paper's cumulative boundary Z_r < r*tau - b_n(r)
  "twosample" a batched two-sample test against the elicited reference sample,
              in the spirit of model-equality testing (Gao, Liang, Guestrin,
              ICLR 2025).  It is NOT a reimplementation of their MMD test; it
              is a two-sample test used in the same role.
  "none"      no monitoring at all
"""
import math
from dataclasses import dataclass, field

import numpy as np


def _norm_cdf(z):
    return 0.5 * math.erfc(-z / math.sqrt(2.0))

PHASES = ("elicit", "primary", "fallback", "route")



class UniformStream:
    """Buffered uniform(0,1) stream.

    Identical in distribution and in CONSUMPTION ORDER to calling
    rng.random() once per draw; buffering only avoids the per-call overhead,
    which matters because the engine is a per-round Python loop.
    """

    __slots__ = ("_rng", "_buf", "_i", "_size")

    def __init__(self, seed, size=1 << 16):
        self._rng = np.random.default_rng(seed)
        self._size = size
        self._buf = self._rng.random(size)
        self._i = 0

    def __call__(self):
        i = self._i
        if i >= self._size:
            self._buf = self._rng.random(self._size)
            i = 0
        self._i = i + 1
        return self._buf[i]

    def many(self, k):
        out = np.empty(k)
        for j in range(k):
            out[j] = self()
        return out


# --------------------------------------------------------------------------- #
# instance
# --------------------------------------------------------------------------- #
@dataclass
class Instance:
    """M and mu are (n_queries, K); key is the mechanism's context label."""
    M: np.ndarray
    mu: np.ndarray
    key: np.ndarray
    honest: np.ndarray
    names: list = field(default_factory=list)

    def __post_init__(self):
        assert self.M.shape == self.mu.shape
        assert self.M.shape[0] == self.key.shape[0]
        assert (self.mu <= self.M + 1e-12).all(), "mu must not exceed M"
        assert (self.M <= 1 + 1e-12).all() and (self.M >= -1e-12).all()
        assert self.honest.shape == (self.K,)
        assert self.honest.any(), "the honest set must be nonempty"

    @property
    def K(self):
        return self.M.shape[1]

    @property
    def Q(self):
        return int(self.key.max()) + 1


def design_constants(n, K):
    """L_n, s_n and the boundary b_n(.) exactly as Section 3 defines them."""
    # n**4 overflows int64 for n >= 2^16, so every logarithm is taken in
    # float and expanded as log(a) + 4*log(n).
    L = int(min(n // (2 * K), np.ceil(n ** (2 / 3) * np.log(np.e * n) ** (1 / 3))))
    L = max(L, 1)
    s = float(np.sqrt((np.log(2.0 * K) + 4.0 * np.log(float(n))) / (2 * L)))
    c = float((np.log(2.0) + 4.0 * np.log(float(n))) / 2)

    def b(r):
        return np.sqrt(r * c)

    return L, s, b


# --------------------------------------------------------------------------- #
# strategies
# --------------------------------------------------------------------------- #
class Strategy:
    """Maps (agent, phase, query, price) to a target mean in [0, M_i(x)].

    theta is the shading level in the declared stationary class:
        m_i(x) = mu_i(x) + theta_i * (M_i(x) - mu_i(x)),
    so theta = 1 is "deliver the measured capability" and theta = 0 is
    "deliver the intrinsic level".  Honest agents are pinned at m >= mu_i(x)
    by the engine, which is the paper's pointwise honesty requirement.
    """

    def __init__(self, inst, theta, follow_price=True, mode="stationary"):
        self.inst = inst
        self.theta = np.asarray(theta, dtype=float)
        self.follow_price = follow_price
        self.mode = mode

    def target(self, i, phase, q, price, state=None):
        M = self.inst.M[q, i]
        mu = self.inst.mu[q, i]
        base = mu + self.theta[i] * (M - mu)
        if phase == "primary" and self.follow_price and price is not None:
            # the proposed profile: meet the announced price if you can
            if self.theta[i] >= 1.0:
                return min(max(mu, min(price, M)), M) if self.inst.honest[i] else min(price, M)
            return base
        return base


class SelectiveStrategy(Strategy):
    """Deviation: deliver capability where this agent is pointwise top, floor elsewhere.

    This is the deviation a mechanism eliciting ONE number per provider cannot
    see, because only the average over contexts enters its bid.
    """

    def __init__(self, inst, theta, deviator, top_mask, floor_theta=0.0):
        super().__init__(inst, theta)
        self.deviator = deviator
        self.top_mask = top_mask          # (n_queries,) bool: deviator is top here
        self.floor_theta = floor_theta

    def target(self, i, phase, q, price, state=None):
        if i != self.deviator:
            return super().target(i, phase, q, price, state)
        M = self.inst.M[q, i]
        mu = self.inst.mu[q, i]
        if self.top_mask[q]:
            m = M
        else:
            m = mu + self.floor_theta * (M - mu)
        if phase == "primary" and price is not None:
            m = min(m, M)
        return m


class BoundaryTrackStrategy(Strategy):
    """Deviation: elicit honestly, then track the monitoring boundary from below."""

    def __init__(self, inst, theta, deviator, margin=1.0):
        super().__init__(inst, theta)
        self.deviator = deviator
        self.margin = margin

    def target(self, i, phase, q, price, state=None):
        if i != self.deviator or phase != "primary" or state is None:
            return super().target(i, phase, q, price, state)
        M, mu = self.inst.M[q, i], self.inst.mu[q, i]
        r, Z, tau, bfun = state["r"], state["Z"], state["tau"], state["b"]
        # smallest target whose expectation keeps the walk above the boundary
        need = (r + 1) * tau - bfun(r + 1) + self.margin - Z
        return float(np.clip(need, mu if self.inst.honest[i] else 0.0, M))


# --------------------------------------------------------------------------- #
# local MESP state (one per context / cell / or one globally for the scalar)
# --------------------------------------------------------------------------- #
class _Local:
    def __init__(self, K, L, s, b, price_shade, rng_priority):
        self.K, self.L, self.s, self.b = K, L, s, b
        self.price_shade = price_shade      # extra shading: 0 for MESP/PL-MESP
        self.phase = "elicit"
        self.turn = 0                       # which agent is being elicited
        self.cnt = np.zeros(K, dtype=np.int64)
        self.sum = np.zeros(K)
        self.priority = rng_priority
        self.W = -1
        self.tau = 0.0
        self.r = 0
        self.Z = 0.0
        self.convicted = False
        self.conv_r = -1
        self.exp3_w = np.ones(K)
        self.exp3_gamma = None
        self.ref = []                       # winner's elicitation sample, for the two-sample rung
        self.batch = []                     # current monitoring batch
        self.n_switch_tests = 0


class MechanismRun:
    """Engine shared by MESP (Q=1), PL-MESP and CG-MESP."""

    def __init__(self, inst, n, seed, price_shade=0.0, monitor="anytime",
                 batch=200, twosample_alpha=1e-4, fallback="exp3", L_override=None,
                 boundary_mult=1.0, buffer=0.05, burnin=None):
        self.inst, self.n, self.monitor = inst, n, monitor
        self.boundary_mult = boundary_mult
        self.buffer = float(buffer)
        # default burn-in of order n^{3/4}, the order the literature uses
        self.burnin = int(burnin) if burnin is not None else int(np.ceil(n ** 0.75))
        self.batch, self.ts_alpha, self.fallback = batch, twosample_alpha, fallback
        self.rng = UniformStream(seed)
        self.L, self.s, self.b = design_constants(n, inst.K)
        if L_override is not None:
            # the continuum mechanism re-solves the elicitation length for the
            # many-region problem; see instances.cg_elicitation_length
            self.L = int(L_override)
            self.s = float(np.sqrt((np.log(2.0 * inst.K) + 4.0 * np.log(float(n)))
                                   / (2 * self.L)))
        self.price_shade = price_shade
        self.locals = {}

    def _get(self, k):
        if k not in self.locals:
            self.locals[k] = _Local(self.inst.K, self.L, self.s, self.b,
                                    self.price_shade, self.rng.many(self.inst.K))
        return self.locals[k]

    # -- monitoring rungs --------------------------------------------------- #
    def _convict(self, lo, y):
        if self.monitor == "none":
            return False
        if self.monitor == "anytime":
            return lo.Z < lo.r * lo.tau - self.boundary_mult * lo.b(lo.r)
        if self.monitor == "fixedbuffer":
            # Braverman-style: after a burn-in, compare the winner's RUNNING
            # AVERAGE against the announced price using a FIXED buffer that does
            # not grow with the number of pulls.  Our boundary grows like
            # sqrt(r); this rung is the alternative that exists in the
            # literature.
            if lo.r < self.burnin:
                return False
            return (lo.Z / lo.r) < lo.tau - self.buffer
        if self.monitor == "anytime_noslack":
            # the boundary removed entirely: the rung Section 5 reports as
            # convicting a fully compliant winner almost always
            return lo.Z < lo.r * lo.tau
        if self.monitor in ("twosample", "twosample_elicit"):
            lo.batch.append(y)
            if len(lo.batch) < self.batch:
                return False
            x = np.asarray(lo.batch, dtype=float)
            lo.batch = []
            lo.n_switch_tests += 1
            if self.monitor == "twosample":
                # Reference = the standard the winner was AWARDED, i.e. a fresh
                # sample of the same size at the announced price.  This is the
                # batched analogue of the anytime boundary: both ask whether the
                # served stream meets the price.
                ref = (self.rng.many(self.batch) < lo.tau).astype(float)
            else:
                # Reference = the winner's own elicitation sample.  Recorded
                # because it is the naive choice and it is WRONG here: the
                # mechanism instructs the winner to drop from its bid to the
                # price, so this rung convicts a fully compliant winner.
                ref = np.asarray(lo.ref, dtype=float)
            if len(ref) < 2:
                return False
            se = np.sqrt(x.var(ddof=1) / len(x) + ref.var(ddof=1) / len(ref) + 1e-12)
            z = (x.mean() - ref.mean()) / se
            return bool(_norm_cdf(z) < self.ts_alpha)
        raise ValueError(self.monitor)

    # -- main loop ---------------------------------------------------------- #
    def run(self, strategy, queries, stop_on_switch=False, trace=None, reward_fn=None):
        """stop_on_switch ends the run at the first conviction.

        Used ONLY by the monitor ablation ladder, whose two axes are the false
        conviction rate and the detection delay; neither depends on what
        happens after the switch, and simulating the EXP3 fallback to the
        horizon costs about fifty times more than the phase being measured.
        Default False, so nothing else is affected."""
        inst, K = self.inst, self.inst.K
        n = len(queries)
        T = np.zeros(K, dtype=np.int64)
        C = np.zeros(K)
        rev_target = 0.0
        rev_real = 0
        phase_rounds = {p: 0 for p in PHASES}
        convictions = 0
        compliant_convictions = 0
        first_switch_round = -1
        post_switch_rev = 0.0
        post_switch_rounds = 0
        price_above_cap = 0
        primary_by_agent = np.zeros(K, dtype=np.int64)

        for t in range(n):
            q = int(queries[t])
            lo = self._get(int(inst.key[q]))

            if lo.phase == "elicit":
                i = lo.turn
                phase = "elicit"
            elif lo.phase == "primary":
                i = lo.W
                phase = "primary"
            else:
                i, phase = self._exp3_pick(lo), "fallback"

            state = None
            if phase == "primary":
                state = {"r": lo.r, "Z": lo.Z, "tau": lo.tau, "b": lo.b}
            m = strategy.target(i, phase, q, lo.tau if phase == "primary" else None, state)
            M_i, mu_i = inst.M[q, i], inst.mu[q, i]
            assert m <= M_i + 1e-9, "a strategy tried to deliver above its capability"
            m = float(np.clip(m, 0.0, M_i))
            if inst.honest[i]:
                m = max(m, mu_i)

            u_ = self.rng()
            y = int(u_ < m) if reward_fn is None else reward_fn(m, q, u_)
            if trace is not None:
                trace.log(t, q, i, phase, lo.tau if phase == "primary" else np.nan, m, y, mu_i)
            T[i] += 1
            C[i] += m - mu_i
            rev_target += m
            rev_real += y
            phase_rounds[phase] += 1
            # revenue realised AFTER the first time any monitor fires: this is
            # what the fallback is worth, and it is what a mechanism that stops
            # serving instead would forgo
            if first_switch_round >= 0:
                post_switch_rev += m
                post_switch_rounds += 1

            if phase == "elicit":
                lo.cnt[i] += 1
                lo.sum[i] += y
                if lo.cnt[i] >= lo.L:
                    lo.turn += 1
                    if lo.turn >= K:
                        self._close_elicitation(lo)
            elif phase == "primary":
                primary_by_agent[i] += 1
                lo.r += 1
                lo.Z += y
                if self._convict(lo, y):
                    lo.convicted = True
                    lo.conv_r = lo.r
                    convictions += 1
                    if first_switch_round < 0:
                        first_switch_round = t
                    if m >= min(lo.tau, M_i) - 1e-12:
                        compliant_convictions += 1
                    lo.phase = "fallback"
                    H = max(1, n - t - 1)
                    lo.exp3_gamma = float(min(1.0, np.sqrt(K * np.log(K) / ((np.e - 1) * H))))
                    if stop_on_switch:
                        n = t + 1
                        break
            else:
                self._exp3_update(lo, i, y)

            if phase == "primary" and lo.tau > M_i + 1e-12:
                price_above_cap += 1

        return {
            "rounds": n, "T": T, "C": C,
            "revenue_target": rev_target, "revenue_realized": rev_real,
            "revenue_per_round": rev_target / n,
            "utility_per_round": (T - C) / n,
            "phase_rounds": phase_rounds,
            "convictions": convictions,
            "compliant_convictions": compliant_convictions,
            "primary_rounds_price_above_capability": price_above_cap,
            "n_locals": len(self.locals),
            "n_locals_past_elicitation": sum(1 for l in self.locals.values()
                                             if l.phase != "elicit"),
            "primary_by_agent": primary_by_agent,
            "first_switch_round": first_switch_round,
            "post_switch_rounds": post_switch_rounds,
            "post_switch_revenue_per_round": (post_switch_rev / post_switch_rounds
                                              if post_switch_rounds else np.nan),
            "conviction_rounds": {k: l.conv_r for k, l in self.locals.items()
                                  if l.conv_r > 0},
            "primary_rounds_by_local": {k: l.r for k, l in self.locals.items()},
            "prices": {k: l.tau for k, l in self.locals.items() if l.phase != "elicit"},
            "winners": {k: l.W for k, l in self.locals.items() if l.phase != "elicit"},
        }

    def _close_elicitation(self, lo):
        beta = lo.sum / np.maximum(lo.cnt, 1)
        order = np.lexsort((lo.priority, -beta))
        lo.W = int(order[0])
        second = float(np.sort(beta)[-2])
        lo.tau = max(0.0, second - lo.s - lo.price_shade)
        lo.phase = "primary"
        # reference sample for the two-sample rung: the winner's elicitation
        # outcomes, summarised by their count and sum (a Bernoulli sample).
        k = int(lo.cnt[lo.W])
        ones = int(round(lo.sum[lo.W]))
        lo.ref = [1.0] * ones + [0.0] * (k - ones)

    def _exp3_pick(self, lo):
        K = self.inst.K
        g = lo.exp3_gamma if lo.exp3_gamma is not None else 0.1
        w = lo.exp3_w / lo.exp3_w.sum()
        p = (1 - g) * w + g / K
        u = self.rng()
        return int(np.searchsorted(np.cumsum(p), u, side="right").clip(0, K - 1))

    def _exp3_update(self, lo, i, y):
        K = self.inst.K
        g = lo.exp3_gamma if lo.exp3_gamma is not None else 0.1
        w = lo.exp3_w / lo.exp3_w.sum()
        p = (1 - g) * w[i] + g / K
        lo.exp3_w[i] *= np.exp(g * (y / max(p, 1e-12)) / K)
        if lo.exp3_w.max() > 1e250:
            lo.exp3_w /= lo.exp3_w.max()


# --------------------------------------------------------------------------- #
# a standalone transcription of Algorithm 1, used to TEST the engine at Q = 1
# --------------------------------------------------------------------------- #
def run_mesp_reference(inst, n, seed, strategy, queries):
    """Direct transcription of Algorithm 1 with no partition machinery."""
    K = inst.K
    rng = UniformStream(seed)
    L, s, b = design_constants(n, K)
    priority = rng.many(K)
    cnt = np.zeros(K, dtype=np.int64)
    ssum = np.zeros(K)
    T = np.zeros(K, dtype=np.int64)
    C = np.zeros(K)
    rev = 0.0
    phase, turn, W, tau, r, Z = "elicit", 0, -1, 0.0, 0, 0.0
    exp3_w, gamma = np.ones(K), None
    for t in range(n):
        q = int(queries[t])
        if phase == "elicit":
            i, ph = turn, "elicit"
        elif phase == "primary":
            i, ph = W, "primary"
        else:
            g = gamma if gamma is not None else 0.1
            w = exp3_w / exp3_w.sum()
            p = (1 - g) * w + g / K
            i = int(np.searchsorted(np.cumsum(p), rng(), side="right").clip(0, K - 1))
            ph = "fallback"
        st = {"r": r, "Z": Z, "tau": tau, "b": b} if ph == "primary" else None
        m = strategy.target(i, ph, q, tau if ph == "primary" else None, st)
        m = float(np.clip(m, 0.0, inst.M[q, i]))
        if inst.honest[i]:
            m = max(m, inst.mu[q, i])
        y = int(rng() < m)
        T[i] += 1
        C[i] += m - inst.mu[q, i]
        rev += m
        if ph == "elicit":
            cnt[i] += 1
            ssum[i] += y
            if cnt[i] >= L:
                turn += 1
                if turn >= K:
                    beta = ssum / np.maximum(cnt, 1)
                    W = int(np.lexsort((priority, -beta))[0])
                    tau = max(0.0, float(np.sort(beta)[-2]) - s)
                    phase = "primary"
        elif ph == "primary":
            r += 1
            Z += y
            if Z < r * tau - b(r):
                phase = "fallback"
                H = max(1, n - t - 1)
                gamma = float(min(1.0, np.sqrt(K * np.log(K) / ((np.e - 1) * H))))
        else:
            g = gamma if gamma is not None else 0.1
            w = exp3_w / exp3_w.sum()
            p = (1 - g) * w[i] + g / K
            exp3_w[i] *= np.exp(g * (y / max(p, 1e-12)) / K)
            if exp3_w.max() > 1e250:
                exp3_w /= exp3_w.max()
    return {"T": T, "C": C, "revenue_target": rev, "revenue_per_round": rev / n}


# --------------------------------------------------------------------------- #
# quality-estimating router (policy class; NOT a published system)
# --------------------------------------------------------------------------- #
def run_router(inst, n, seed, strategy, queries, rule="ucb", eps=0.05,
               context_aware=True, trace=None, reward_fn=None):
    if rule == "static":
        return run_router_static(inst, n, seed, strategy, queries,
                                 context_aware=context_aware, trace=trace, reward_fn=reward_fn)
    K = inst.K
    rng = np.random.default_rng(seed)
    U = UniformStream(seed + 7919)
    nk = inst.Q if context_aware else 1
    cnt = np.zeros((nk, K), dtype=np.int64)
    ssum = np.zeros((nk, K))
    T = np.zeros(K, dtype=np.int64)
    C = np.zeros(K)
    rev = 0.0
    for t in range(n):
        q = int(queries[t])
        k = int(inst.key[q]) if context_aware else 0
        c, sm = cnt[k], ssum[k]
        if (c == 0).any():
            i = int(np.flatnonzero(c == 0)[0])
        else:
            mean = sm / c
            if rule == "greedy":
                score = mean
            elif rule == "epsgreedy":
                if U() < eps:
                    i = int(rng.integers(K))
                    score = None
                else:
                    score = mean
            elif rule == "ucb":
                tt = c.sum()
                score = mean + np.sqrt(2 * np.log(max(tt, 2)) / c)
            else:
                raise ValueError(rule)
            if score is not None:
                i = int(np.argmax(score + 1e-12 * rng.random(K)))
        m = strategy.target(i, "route", q, None, None)
        m = float(np.clip(m, 0.0, inst.M[q, i]))
        if inst.honest[i]:
            m = max(m, inst.mu[q, i])
        u_ = U()
        y = int(u_ < m) if reward_fn is None else reward_fn(m, q, u_)
        if trace is not None:
            trace.log(t, q, i, "route", np.nan, m, y, inst.mu[q, i])
        cnt[k, i] += 1
        ssum[k, i] += y
        T[i] += 1
        C[i] += m - inst.mu[q, i]
        rev += m
    return {"T": T, "C": C, "revenue_target": rev, "revenue_per_round": rev / n,
            "utility_per_round": (T - C) / n, "rounds": n}


# --------------------------------------------------------------------------- #
# static benchmark router (baseline added 29 Sep 2026, A5): route by the
# published offline capability table, never learn from outcomes
# --------------------------------------------------------------------------- #
def static_benchmark_choice(inst, seed, context_aware=True):
    """Provider chosen for each context label by the offline benchmark table.

    The table is inst.M (the published benchmark capability per task type), NOT
    the delivered effort and NOT observed rewards. When a context label covers
    several query rows, the router sees their unweighted mean capability; with
    context_aware=False it sees one overall score per provider. Ties (within
    1e-12) are broken by a seed-fixed random priority over providers.
    """
    K = inst.K
    if context_aware:
        nk = inst.Q
        key = inst.key
    else:
        nk = 1
        key = np.zeros(inst.M.shape[0], dtype=np.int64)
    bench = np.zeros((nk, K))
    for k in range(nk):
        bench[k] = inst.M[key == k].mean(axis=0)
    prio = np.random.default_rng([seed, 4242]).permutation(K)   # lower = preferred
    choice = np.zeros(nk, dtype=np.int64)
    for k in range(nk):
        top = np.flatnonzero(bench[k] >= bench[k].max() - 1e-12)
        choice[k] = int(top[np.argmin(prio[top])])
    return choice, bench


def run_router_static(inst, n, seed, strategy, queries, context_aware=True,
                      trace=None, reward_fn=None):
    """Static benchmark router (RouteLLM / Not Diamond style offline router, or
    a gateway that trusts the model name): every query of a task type goes to
    the provider with the best offline benchmark capability for that type. It
    never updates from observed outcomes and pays nothing, so a provider that
    shades keeps its traffic. Outcomes use the same uniform stream
    (seed + 7919) as run_router, so profiles see common random numbers."""
    K = inst.K
    U = UniformStream(seed + 7919)
    choice, bench = static_benchmark_choice(inst, seed, context_aware)
    T = np.zeros(K, dtype=np.int64)
    C = np.zeros(K)
    rev = 0.0
    realized = 0
    for t in range(n):
        q = int(queries[t])
        k = int(inst.key[q]) if context_aware else 0
        i = int(choice[k])
        m = strategy.target(i, "route", q, None, None)
        m = float(np.clip(m, 0.0, inst.M[q, i]))
        if inst.honest[i]:
            m = max(m, inst.mu[q, i])
        u_ = U()
        y = int(u_ < m) if reward_fn is None else reward_fn(m, q, u_)
        if trace is not None:
            trace.log(t, q, i, "route", np.nan, m, y, inst.mu[q, i])
        T[i] += 1
        C[i] += m - inst.mu[q, i]
        rev += m
        realized += y
    return {"T": T, "C": C, "revenue_target": rev, "revenue_realized": realized,
            "revenue_per_round": rev / n, "utility_per_round": (T - C) / n, "rounds": n,
            "static_choice": choice, "static_bench": bench}


# --------------------------------------------------------------------------- #
# audit-and-ban router (baseline added 28 Sep 2026, A5): a UCB router with one
# estimate per task type, plus a sequential test per (provider, task type)
# --------------------------------------------------------------------------- #
def run_router_audit(inst, n, seed, strategy, queries, delta=0.05, warm=None, trace=None,
                     false_ban=None):
    """UCB router per task type plus an audit that bans a provider for good.

    Reference (SELF, the only variant run): the provider's realised success
    rate over its first `warm` = ceil(4 log n) selections at that task type.
    After that, every further selection at the type adds Y - (ref - delta) to a
    running sum S; the provider is banned from every type once
        S < -sqrt(r * c) - r * rad,   c = (log 2 + 2 log n) / 2,
        rad = sqrt(log(2 n K Q) / (2 warm)),
    where r is the number of post-reference selections. The first term is the
    anytime Hoeffding boundary with a union bound over r <= n (false alarm at
    most 1/(2n) per test for a compliant provider delivering >= its reference
    mean minus delta); the second is the reference's own estimation radius,
    union-bounded over every (provider, type), without which a compliant
    provider whose warm-up happened to run lucky would be banned. A banned
    provider is never selected again; if every provider is banned the round is
    not delegated (trace agent 255, earns nothing).

    `false_ban` = alpha (variant added 29 Sep 2026, author's decision): a
    platform-realistic level instead of ~1/n. The probability that a compliant
    provider is ever banned is at most alpha, split evenly over its Q tests and,
    within each test, between the boundary and the reference:
        c = log(2 Q n / alpha) / 2        (n e^{-2c} = alpha / (2Q)),
        rad = sqrt(log(4 Q / alpha) / (2 warm))   (2 e^{-2 warm rad^2} = alpha / (2Q)).
    None keeps the 1/n calibration above, unchanged.
    """
    K, Q = inst.K, inst.Q
    rng = np.random.default_rng(seed)
    U = UniformStream(seed + 7919)
    warm = int(np.ceil(4 * np.log(n))) if warm is None else int(warm)
    if false_ban is None:
        c = (np.log(2.0) + 2.0 * np.log(float(n))) / 2.0
        rad = float(np.sqrt(np.log(2.0 * n * K * Q) / (2.0 * warm)))
    else:
        a = float(false_ban)
        c = np.log(2.0 * Q * n / a) / 2.0
        rad = float(np.sqrt(np.log(4.0 * Q / a) / (2.0 * warm)))
    cnt = np.zeros((Q, K), dtype=np.int64)
    ssum = np.zeros((Q, K))
    ref_n = np.zeros((Q, K), dtype=np.int64)
    ref_s = np.zeros((Q, K))
    S = np.zeros((Q, K))
    r_post = np.zeros((Q, K), dtype=np.int64)
    banned = np.zeros(K, dtype=bool)
    ban_round = np.full(K, -1, dtype=np.int64)
    compliant_bans = 0
    T = np.zeros(K, dtype=np.int64)
    C = np.zeros(K)
    rev = 0.0
    realized = 0
    idle = 0
    for t in range(n):
        q = int(queries[t])
        k = int(inst.key[q])
        alive = ~banned
        if not alive.any():
            idle += 1
            continue
        c_k, s_k = cnt[k], ssum[k]
        untried = np.flatnonzero((c_k == 0) & alive)
        if untried.size:
            i = int(untried[0])
        else:
            mean = s_k / np.maximum(c_k, 1)
            tt = c_k[alive].sum()
            score = mean + np.sqrt(2 * np.log(max(tt, 2)) / np.maximum(c_k, 1))
            score = np.where(alive, score + 1e-12 * rng.random(K), -np.inf)
            i = int(np.argmax(score))
        m = strategy.target(i, "route", q, None, None)
        m = float(np.clip(m, 0.0, inst.M[q, i]))
        if inst.honest[i]:
            m = max(m, inst.mu[q, i])
        y = int(U() < m)
        if trace is not None:
            trace.log(t, q, i, "route", np.nan, m, y, inst.mu[q, i])
        cnt[k, i] += 1
        ssum[k, i] += y
        T[i] += 1
        C[i] += m - inst.mu[q, i]
        rev += m
        realized += y
        if ref_n[k, i] < warm:
            ref_n[k, i] += 1
            ref_s[k, i] += y
        else:
            ref = ref_s[k, i] / warm
            r_post[k, i] += 1
            S[k, i] += y - (ref - delta)
            r = r_post[k, i]
            if S[k, i] < -np.sqrt(r * c) - r * rad:
                banned[i] = True
                ban_round[i] = t
                if inst.honest[i]:
                    compliant_bans += 1
    return {"T": T, "C": C, "revenue_target": rev, "revenue_realized": realized,
            "revenue_per_round": rev / n, "utility_per_round": (T - C) / n, "rounds": n,
            "banned": banned, "ban_round": ban_round, "honest_bans": compliant_bans,
            "idle_rounds": idle, "delta": delta, "warm": warm, "ref_radius": rad,
            "boundary_c": c, "false_ban": false_ban}


# --------------------------------------------------------------------------- #
# closed-form benchmarks
# --------------------------------------------------------------------------- #
def oracle_per_round(inst, queries):
    return float(inst.M[queries].max(axis=1).mean())


def second_capability_per_round(inst, queries):
    return float(np.sort(inst.M[queries], axis=1)[:, -2].mean())


def honest_benchmark_per_round(inst, queries):
    h = np.flatnonzero(inst.honest)
    return float(inst.mu[np.ix_(queries, h)].max(axis=1).mean())


# --------------------------------------------------------------------------- #
# per-agent strategy options, so a profile can mix them
# --------------------------------------------------------------------------- #
OPTIONS = ["theta0.00", "theta0.25", "theta0.50", "theta0.75", "theta1.00",
           "proposed", "selective", "boundary"]


# The RICH option class.  The coarse set above cannot express the deviation a
# quality-estimating router is vulnerable to, so a best response computed over
# it attacks each rule only where that rule happens to be weak.  This set adds
# a fine theta grid near 1 and the undercut family
#     m_i(x) = max(mu_i(x), min(M_i(x), M_(2)(x) + eps)),
# which keeps a pointwise-top provider top by eps while banking the rest.
RICH_OPTIONS = (["theta0.00", "theta0.25", "theta0.50", "theta0.75", "theta0.90",
                 "theta0.95", "theta0.975", "theta0.99", "theta1.00",
                 "proposed", "selective", "boundary"]
                + [f"undercut{e}" for e in ("0.0", "0.005", "0.02", "0.05")])


class ProfileStrategy:
    """One option per agent.

    theta<x>  stationary map m_i(x) = mu_i(x) + x*(M_i(x) - mu_i(x)); theta1.00
              is "always deliver the measured capability", which is also the
              NON-STRATEGIC provider of the headline comparison.
    proposed  the paper's S*: capability in elicitation and fallback,
              min(price, capability) as primary winner.
    selective deliver capability where this agent is pointwise top, intrinsic
              level elsewhere.  Invisible to a mechanism that elicits one
              number per provider.
    boundary  elicit at capability, then track the monitoring boundary from
              below as primary winner.
    shadeall<d>  bid the capability, then deliver d below the proposed profile's
              delivery in every later served round (price - d while priced,
              capability - d otherwise); the common deviation of the J traces.
    shadeprice<d>  as shadeall but only while a price is announced; capability
              in every unpriced round.
    """

    def __init__(self, inst, options, top_masks, margin=1.0, second=None):
        self.inst = inst
        self.options = list(options)
        self.top_masks = top_masks
        self.margin = margin
        # pointwise second-largest capability, needed by the undercut options
        self.second = (second if second is not None
                       else np.sort(inst.M, axis=1)[:, -2])

    def target(self, i, phase, q, price, state=None):
        inst = self.inst
        M, mu = inst.M[q, i], inst.mu[q, i]
        opt = self.options[i]
        if opt.startswith("theta"):
            return mu + float(opt[5:]) * (M - mu)
        if opt == "proposed":
            if phase == "primary" and price is not None:
                m = min(price, M)
                return max(mu, m) if inst.honest[i] else m
            return M
        if opt == "selective":
            return M if self.top_masks[q, i] else mu
        if opt.startswith("primaryfixed"):
            # bid the capability, as the proposed profile does, and deliver
            # exactly this mean in the PRIMARY phase only.  This separates the
            # bid from the delivery, which the plain "fixed" family conflates.
            if phase != "primary":
                return M
            lo = mu if inst.honest[i] else 0.0
            return float(np.clip(float(opt[12:]), lo, M))
        if opt.startswith("fixed"):
            # deliver exactly this mean in every phase, clipped to feasibility;
            # used by the utility-against-effort sweep
            lo = mu if inst.honest[i] else 0.0
            return float(np.clip(float(opt[5:]), lo, M))
        if opt.startswith("shadeprice"):
            # deliver the ANNOUNCED price minus delta while priced (whatever mechanism announced it),
            # capability otherwise; the J traces use this against every mechanism alike
            if phase not in ("primary", "exploit") or price is None:
                return M
            lo = mu if inst.honest[i] else 0.0
            return float(np.clip(price - float(opt[10:]), lo, M))
        if opt.startswith("shadeall"):
            # ONE declared deviation against every mechanism alike (the J traces): bid the
            # capability, then in every served round after the bid deliver delta below what
            # the proposed profile would deliver there, i.e. below the announced price while
            # priced and below the capability otherwise (blind trust, fallback, routing).
            if phase in ("elicit", "explore"):
                return M
            lo = mu if inst.honest[i] else 0.0
            base = min(price, M) if price is not None else M
            return float(np.clip(base - float(opt[8:]), lo, M))
        if opt.startswith("undercut"):
            eps = float(opt[8:])
            lo = mu if inst.honest[i] else 0.0
            return float(np.clip(self.second[q] + eps, lo, M))
        if opt == "boundary":
            if phase != "primary" or state is None:
                return M
            r, Z, tau, bfun = state["r"], state["Z"], state["tau"], state["b"]
            need = (r + 1) * tau - bfun(r + 1) + self.margin - Z
            return float(np.clip(need, mu if inst.honest[i] else 0.0, M))
        raise ValueError(opt)


# --------------------------------------------------------------------------- #
# the SINGLE-OBSERVATION EXCLUSION RULE, run under OUR observation model
# --------------------------------------------------------------------------- #
def run_single_observation_exclusion(inst, n, seed, strategy, queries,
                                     L_elicit=1, empty="stop", trace=None):
    """The single-observation exclusion rule of Esmaeili et al. (AAAI 2025),
    run under THIS PAPER'S noisy-delivery model.

    The rule as our related work describes it: elicit a bid with ONE pull per
    agent, announce the second-highest bid as the price, and exclude an agent
    whose realised delivery falls below that price.  In its own setting the
    selected agent observes and edits its realised reward before the platform
    sees it, so one pull certifies the bid and the rule is correct.  Here the
    agent fixes a target before a fresh Bernoulli draw, so one pull certifies
    nothing.

    THIS IS NOT A REPRODUCTION OF THEIR RESULTS IN THEIR OWN SETTING, where
    the rule is correct.  It is their rule transplanted into our observation
    model, which is exactly what Theorem `thm:separation` is about.

    `L_elicit` generalises the single pull so the transition can be seen;
    `L_elicit = 1` is the rule as stated.  `empty` decides what happens when
    every agent has been excluded: "stop" collects nothing further, which is
    the model Theorem `thm:separation` bounds, and "roundrobin" is a charitable
    repair that keeps allocating.
    """
    K = inst.K
    rng = UniformStream(seed)
    priority = rng.many(K)
    cnt = np.zeros(K, dtype=np.int64)
    ssum = np.zeros(K)
    T = np.zeros(K, dtype=np.int64)
    C = np.zeros(K)
    rev = 0.0
    realized = 0
    active = np.ones(K, dtype=bool)
    phase, turn, W, tau = "elicit", 0, -1, 0.0
    order = None
    excluded_rounds = []
    compliant_exclusions = 0
    idle_rounds = 0
    rr = 0
    for t in range(n):
        q = int(queries[t])
        if phase == "elicit":
            i, ph = turn, "elicit"
        elif phase == "primary":
            i, ph = W, "primary"
        else:                                   # every agent excluded
            if empty == "stop":
                idle_rounds += 1
                continue
            i, ph = rr % K, "fallback"
            rr += 1
        m = strategy.target(i, ph, q, tau if ph == "primary" else None, None)
        m = float(np.clip(m, 0.0, inst.M[q, i]))
        if inst.honest[i]:
            m = max(m, inst.mu[q, i])
        y = int(rng() < m)
        if trace is not None:
            trace.log(t, q, i, ph, tau if ph == "primary" else np.nan, m, y, inst.mu[q, i])
        T[i] += 1
        C[i] += m - inst.mu[q, i]
        rev += m
        realized += y
        if ph == "elicit":
            cnt[i] += 1
            ssum[i] += y
            if cnt[i] >= L_elicit:
                turn += 1
                if turn >= K:
                    beta = ssum / np.maximum(cnt, 1)
                    order = list(np.lexsort((priority, -beta)))
                    W = int(order[0])
                    tau = float(np.sort(beta)[-2])   # NO statistical shading
                    phase = "primary"
        elif ph == "primary":
            # exclusion decided from THIS ONE observation
            if y < tau:
                active[W] = False
                excluded_rounds.append(t)
                if m >= min(tau, inst.M[q, W]) - 1e-12:
                    compliant_exclusions += 1
                nxt = [j for j in order if active[j]]
                if nxt:
                    W = int(nxt[0])
                else:
                    phase = "empty"
    return {"rounds": n, "T": T, "C": C,
            "revenue_target": rev, "revenue_realized": realized,
            "revenue_per_round": rev / n,
            "utility_per_round": (T - C) / n,
            "exclusions": len(excluded_rounds),
            "compliant_exclusions": compliant_exclusions,
            "first_exclusion_round": excluded_rounds[0] if excluded_rounds else -1,
            "all_excluded_from_round": (excluded_rounds[-1]
                                        if len(excluded_rounds) >= K else -1),
            "idle_rounds": idle_rounds,
            "announced_price": tau,
            "L_elicit": L_elicit}


# --------------------------------------------------------------------------- #
# the SECOND-BEST UTILITY GUARANTEE MECHANISM, reimplemented from the paper
# --------------------------------------------------------------------------- #
# Their accounting phases mapped onto the strategy-facing phase names, so that
# one and the same provider strategy can be run under both mechanisms:
#   exploration  <-> our elicitation (bid)
#   exploitation <-> our primary phase (priced, monitored)
#   blind trust  <-> our fallback (unpriced)
SB_PHASE = {"explore": "elicit", "exploit": "primary",
            "blind1": "fallback", "blind2": "fallback"}


def run_second_best(inst, n, seed, strategy, queries, eps=1.0 / 3.0,
                    price=None, leftover="to_winner", gate_blind2=True, trace=None,
                    reward_fn=None):
    """Mechanism 1 of Cao, Wang, Liu, Li, Tao and He, "Pay for The Second-Best
    Service: A Game-Theoretic Approach Against Dishonest LLM Providers",
    WWW 2026, pages 249-260, DOI 10.1145/3774904.3792446, arXiv:2511.00847v5.

    REIMPLEMENTED FROM THE PAPER. There is no released code and no artifact.
    This is THEIR mechanism run under THIS paper's observation model, not a
    reproduction of their results in their own setting, where it is correct.

    Their observation model is strictly more general than ours, so ours is a
    special case and the mechanism carries over with no change to its
    instrument set, its monitor, its phase budgets or its proposed provider
    strategy. Three modifications, all stated in REPORT.md:

      (M1) token length L = 1, which disables the billing channel. Per-round
           payment is then the constant p, their user utility is our platform
           revenue minus p, and their benchmark is n (M_(2) - p).
      (M2) reward range R = 1, with the reward being our Bernoulli draw. The
           constant b in their line 16 is the reward range, which the Hoeffding
           step of their Appendix A fixes as b = R = 1.
      (M3) a common price p := min_i (M_i - mu_i), with their truthful cost
           corresponding to delivering capability, so cost c maps to a
           delivered mean m = mu_i + (c / p)(M_i - mu_i).

    Their line 16 is a FIXED-SLACK test after a burn-in B = T^{2 eps}, and on
    firing it sets validated false and BREAKS: the remaining queries are never
    delegated to anyone. That is not our fallback and is not replaced by one.
    The no-reallocation behaviour is the point of the comparison.
    """
    K = inst.K
    rng = UniformStream(seed)
    T = n
    B = max(1, int(np.ceil(T ** (2 * eps))))
    Mslack = (T ** (-eps)) * np.log(K * T)
    R = 1.0
    b = R
    L = 1.0
    if price is None:
        # (M3) over providers that can shade at all: a provider whose capability
        # equals its intrinsic level (e.g. the cheap substitute itself in the
        # v2 setup) has no cost scale and would make p = 0. Unchanged for every
        # instance in which all gaps are positive, i.e. every A4 run.
        gap = inst.M.mean(axis=0) - inst.mu.mean(axis=0)
        price = float(np.min(gap[gap > 1e-12])) if (gap > 1e-12).any() else 1.0
    p = float(price)

    T_i = np.zeros(K, dtype=np.int64)
    C = np.zeros(K)
    rev = 0.0
    realized = 0
    t = 0
    phase_rounds = {"explore": 0, "exploit": 0, "blind1": 0, "blind2": 0,
                    "undelegated": 0}
    rev_by_phase = {k: 0.0 for k in phase_rounds}

    def serve(i, phase):
        """One delegation to provider i, charged to `phase`."""
        nonlocal t, rev, realized
        q = int(queries[t])
        sphase = SB_PHASE[phase]
        m = strategy.target(i, sphase, q,
                            serve.price_signal if sphase == "primary" else None,
                            None)
        m = float(np.clip(m, 0.0, inst.M[q, i]))
        if inst.honest[i]:
            m = max(m, inst.mu[q, i])
        u_ = rng()
        y = int(u_ < m) if reward_fn is None else reward_fn(m, q, u_)
        if trace is not None:
            trace.log(t, q, i, phase, serve.price_signal if sphase == "primary" else np.nan,
                      m, y, inst.mu[q, i])
        T_i[i] += 1
        C[i] += m - inst.mu[q, i]
        rev += m
        realized += y
        phase_rounds[phase] += 1
        rev_by_phase[phase] += m
        t += 1
        return y
    serve.price_signal = None

    # ---- exploration phase (their lines 3 to 7) --------------------------- #
    vbar = np.zeros(K)
    for i in range(K):
        s = 0.0
        for _ in range(B):
            if t >= T:
                break
            s += serve(i, "explore")
        vbar[i] = s / max(1, min(B, T_i[i]))
    if t >= T:
        return _sb_result(n, T_i, C, rev, realized, phase_rounds, rev_by_phase,
                          p, B, Mslack, eps, -1, np.nan, True, -1, 0.0)

    ubar = vbar - p * L                       # user utility per query, L = 1
    delta = 2.0 * vbar / (p * L) - 2.0 * 1.0 / L
    order = np.lexsort((rng.many(K), -ubar))  # ties broken randomly
    istar = int(order[0])
    ubar_prime = float(np.sort(ubar)[-2])

    # ---- exploitation phase (their lines 12 to 18) ------------------------ #
    T_R = int(np.floor(T - (5 * K + 2 * R / (p * L)
                            + float(sum(delta[i] for i in range(K) if i != istar)))
                       * B - K))
    T_R = max(0, min(T_R, T - t))
    serve.price_signal = ubar_prime + p * L   # the delivered mean that meets ubar'
    slack = (b + p * L) * Mslack / 3.0
    validated = True
    fired_at = -1
    su = 0.0
    for j in range(1, T_R + 1):
        if t >= T:
            break
        y = serve(istar, "exploit")
        su += (y - p * L)                     # their per-query user utility
        if j > B and (su / j) < ubar_prime - slack:
            validated = False
            fired_at = j
            break
    serve.price_signal = None

    # ---- blind trust phase I (their lines 20 to 24) ----------------------- #
    # AMBIGUITY IN THEIR PSEUDOCODE: line 21 is "if validated", and whether it
    # gates blind trust phase II as well as phase I is not typographically
    # resolved. `gate_blind2=True` gates both, which is the reading on which
    # the break at line 18 means "the remaining queries are never delegated".
    # `gate_blind2=False` is the alternative, generous to them, in which phase
    # II still runs after the monitor fires. Both are measured.
    if validated:
        for _ in range(B):
            if t >= T:
                break
            serve(istar, "blind1")
        for i in range(K):
            if i == istar:
                continue
            for _ in range(B):
                if t >= T:
                    break
                serve(i, "blind1")
    if validated or not gate_blind2:
        # ---- blind trust phase II (their lines 25 to 30) ------------------ #
        for i in range(K):
            dprime = delta[i] + 3.0
            if dprime < 0:
                continue
            cnt = int(np.floor(B * dprime))
            if rng() < (B * dprime - cnt):
                cnt += 1
            for _ in range(cnt):
                if t >= T:
                    break
                serve(i, "blind2")

    # Their line 18 BREAKS, so after the monitor fires nothing is delegated for
    # the rest of the horizon. Those rounds earn the user nothing.
    post_fire_rounds = T - t if not validated else 0
    # If the monitor did NOT fire, their T_R formula reserves more budget than
    # the two blind-trust phases consume, and the paper does not say what to do
    # with the remainder. The AMBIGUITY IS RESOLVED IN THEIR FAVOUR: the
    # leftover is delegated to the winner under blind trust, which earns the
    # user something rather than nothing.
    leftover_rounds = 0
    if validated and leftover == "to_winner":
        while t < T:
            serve(istar, "blind2")
            leftover_rounds += 1
    phase_rounds["undelegated"] = T - t
    return _sb_result(n, T_i, C, rev, realized, phase_rounds, rev_by_phase, p,
                      B, Mslack, eps, istar, ubar_prime, validated, fired_at,
                      float(post_fire_rounds), leftover_rounds)


def _sb_result(n, T_i, C, rev, realized, phase_rounds, rev_by_phase, p, B,
               Mslack, eps, istar, ubar_prime, validated, fired_at,
               post_fire_rounds, leftover_rounds=0):
    return {
        "rounds": n, "T": T_i, "C": C,
        "revenue_target": rev, "revenue_realized": realized,
        "revenue_per_round": rev / n,
        "utility_per_round": (T_i - C) / n,
        "phase_rounds": phase_rounds,
        "revenue_by_phase": rev_by_phase,
        "undelegated_rounds": phase_rounds["undelegated"],
        "undelegated_fraction": phase_rounds["undelegated"] / n,
        "monitor_fired": (not validated),
        "fired_at_exploitation_round": fired_at,
        "post_fire_rounds": post_fire_rounds,
        "post_fire_revenue_per_round": 0.0 if post_fire_rounds > 0 else np.nan,
        "leftover_rounds_given_to_winner": leftover_rounds,
        "price": p, "B": B, "M_slack": Mslack, "eps": eps,
        "winner": istar, "announced_second_best_utility": ubar_prime,
        # their user utility is our revenue minus the constant price
        "their_user_utility_per_round": rev / n - p * (1 - phase_rounds["undelegated"] / n),
    }
