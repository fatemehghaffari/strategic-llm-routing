"""Shared tape-based simulator for MESP and its ablation variants (round 2, E5).

Coupling (Scout A4, Section 3.2): outcomes are 1{U < m} on pre-drawn uniform tapes, one per
(agent, bidding pull), one per primary pull, one per (fallback round, agent). All behaviors of a
replicate share the tapes, so a lower target can only lower an agent's own bid, other agents'
bids are unchanged, and the deviating win event is contained in the baseline win event.

Mechanism (Private_information_setting.tex): Stage 1 pulls every agent L_n times; empirical bids
beta_i; largest bidder W by (-beta, uniform priority); tau = (beta_(2) - s_n)_+; Stage 2 pulls W and
switches after primary pull r iff Z_r < r tau - b_n(r); Stage 3 restarts explicit-exploration EXP3
with fresh weights for the H remaining rounds. Variants change exactly one component each.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .design import design as make_design, exp3_constants, ucb_bonus
from .instances import Instance


@dataclass(frozen=True)
class Variant:
    """A mechanism variant. `ucb_index` selects the fallback UCB's index for the UCB-fallback rungs only."""
    name: str = "mesp"
    L: int | None = None                 # bidding length override (R1); None = L_n
    price_mode: str = "conservative"     # conservative | raw | conf1n           (R2)
    monitor: str = "anytime"             # anytime | none | noslack | windowed   (R3)
    window: int = 200
    fallback: str = "exp3"               # exp3 | exp3_warm | ucb | ucb_warm | roundrobin | runnerup | exclude (R4 to R6)


VARIANTS = {
    "mesp": Variant(),
    "esp_nomon": Variant("esp_nomon", monitor="none"),
    "esp_mon_nofb": Variant("esp_mon_nofb", fallback="roundrobin"),
    "esp_excl": Variant("esp_excl", fallback="exclude"),
    "esp_ucbfb": Variant("esp_ucbfb", fallback="ucb"),
    "esp_ucbfb_warm": Variant("esp_ucbfb_warm", fallback="ucb_warm"),
    "esp_exp3_warm": Variant("esp_exp3_warm", fallback="exp3_warm"),
    "esp_runnerup": Variant("esp_runnerup", fallback="runnerup"),
    "mesp_rawprice": Variant("mesp_rawprice", price_mode="raw"),
    "mesp_conf1n": Variant("mesp_conf1n", price_mode="conf1n"),
    "mesp_noslack": Variant("mesp_noslack", monitor="noslack"),
    "mesp_windowed": Variant("mesp_windowed", monitor="windowed"),
}


@dataclass
class AgentCtx:
    i: int
    mu: float
    M: float
    honest: bool
    K: int
    n: int
    d: object
    rng: np.random.Generator

    def clip(self, m: float) -> float:
        lo = self.mu if self.honest else 0.0
        return float(min(self.M, max(lo, m)))


class Policy:
    """Behavior of one agent. Targets are clipped to the feasible set by the simulator."""
    constant_bid = True       # bid_target does not depend on (r, z)
    primary_array = True      # primary target depends on (r, tau) only, never on Z_r
    name = "s_star"

    def bid_target(self, ctx: AgentCtx, r: int, z: int) -> float:
        return ctx.M

    def primary_target(self, ctx: AgentCtx, r: int, Z: int, tau: float) -> float:
        return min(tau, ctx.M)

    def primary_targets(self, ctx: AgentCtx, tau: float, r0: int, N: int) -> np.ndarray:
        """Targets for primary pulls r0+1 .. r0+N (used when primary_array is True)."""
        return np.array([self.primary_target(ctx, r0 + r + 1, 0, tau) for r in range(N)])

    def fallback_target(self, ctx: AgentCtx, t: int, own_pulls: int, own_succ: int, H: int) -> float:
        return ctx.M


class SStar(Policy):
    pass


class AllMax(Policy):
    name = "all_max"

    def primary_target(self, ctx, r, Z, tau):
        return ctx.M


class Underbid(Policy):
    def __init__(self, delta: float):
        self.delta = delta; self.name = f"underbid_{int(round(delta * 100)):02d}"

    def bid_target(self, ctx, r, z):
        return ctx.M - self.delta


class PrimaryShade(Policy):
    def __init__(self, delta: float):
        self.delta = delta; self.name = f"primary_shade_{int(round(delta * 100)):02d}"

    def primary_target(self, ctx, r, Z, tau):
        return tau - self.delta


class BaitSwitch(Policy):
    name = "bait_switch"

    def primary_target(self, ctx, r, Z, tau):
        return 0.0


class TriggerFallbackShade(BaitSwitch):
    name = "trigger_fallback_shade"

    def fallback_target(self, ctx, t, own_pulls, own_succ, H):
        return 0.0


class OwnCapacityPrimary(Policy):
    """Winner delivers its own capacity in the primary phase (the intended non-top deviation)."""
    name = "primary_own_capacity"

    def primary_target(self, ctx, r, Z, tau):
        return ctx.M


class BoundaryRide(Policy):
    """Fixed-schedule boundary riding: deliver tau - c / sqrt(r) on primary pull r.

    The cumulative shortfall is about 2 c sqrt(r) against the boundary b_n(r) = sqrt(r log(2 n^4) / 2), which is
    about 4.5 sqrt(r) at n = 20,000, so with c = 1 the schedule stays about 2.5 sqrt(r) (five noise standard
    deviations) inside the boundary and saves about 2 c sqrt(N_n) effort. The exact DP tracks the realized noise
    instead of a fixed schedule and extracts about b_n(N_n).
    """
    primary_array = True

    def __init__(self, c: float = 1.0):
        self.c = c; self.name = f"boundary_ride_c{c:g}"

    def primary_target(self, ctx, r, Z, tau):
        return tau - self.c / math.sqrt(r)


class ZeroFallback(Policy):
    name = "zero_fallback"

    def fallback_target(self, ctx, t, own_pulls, own_succ, H):
        return 0.0


class ThresholdPolicy(Policy):
    """Bang-bang policy from the exact DP: deliver M iff the stored rule says so.

    bid_rule[r] = (a, b): on bidding pull r (0-based) with z successes so far, deliver M iff a <= z < b.
    primary_rules[key(tau)][r - 1] = (a, b): before primary pull r (1-based) with reward sum Z, deliver M iff a <= Z < b.
    The "deliver M" set is an interval: the deviator shades both when far above the boundary (or when the win is
    secured) and when a switch (or a loss) has become unavoidable.
    """
    constant_bid = False
    primary_array = False
    name = "dp_threshold"

    def __init__(self, bid_rule: np.ndarray, primary_rules: dict, tau_key, fallback_target: float | None = None):
        self.bid_rule = bid_rule; self.primary_rules = primary_rules; self.tau_key = tau_key; self.fb = fallback_target

    def bid_target(self, ctx, r, z):
        a, b = self.bid_rule[r]
        return ctx.M if a <= z < b else 0.0

    def primary_target(self, ctx, r, Z, tau):
        key = self.tau_key(tau)
        if key not in self.primary_rules:  # price with negligible mass under the DP truncation: nearest stored rule
            key = min(self.primary_rules, key=lambda k: abs(k - key))
        a, b = self.primary_rules[key][r - 1]
        return ctx.M if a <= Z < b else 0.0

    def fallback_target(self, ctx, t, own_pulls, own_succ, H):
        return ctx.M if self.fb is None else self.fb


def behavior(name: str) -> Policy:
    table = {"profile": SStar(), "s_star": SStar(), "all_max": AllMax(), "underbid_05": Underbid(.05),
             "underbid_15": Underbid(.15), "primary_shade_05": PrimaryShade(.05), "primary_shade_15": PrimaryShade(.15),
             "bait_switch": BaitSwitch(), "trigger_fallback_shade": TriggerFallbackShade(),
             "primary_own_capacity": OwnCapacityPrimary(), "boundary_ride": BoundaryRide(1.0), "zero_fallback": ZeroFallback()}
    return table[name]


def profile(inst: Instance, focal_behavior: Policy | None = None, others: Policy | None = None) -> list[Policy]:
    """Unilateral profile: focal agent uses focal_behavior, everyone else S_star (or `others`)."""
    base = others or SStar()
    pols = [base] * inst.K
    if focal_behavior is not None:
        pols = list(pols); pols[inst.focal] = focal_behavior
    return pols


def _price(beta2: float, d, mode: str) -> float:
    if mode == "conservative":
        return max(0.0, beta2 - d.s)
    if mode == "raw":
        return float(beta2)
    if mode == "conf1n":
        return max(0.0, beta2 - math.sqrt(math.log(2 * d.K * d.n) / (2 * d.L)))
    raise ValueError(mode)


def _monitored_segment(ctx: AgentCtx, pol: Policy, tau: float, U: np.ndarray, d, variant: Variant, r0: int = 0):
    """Pull agent ctx.i for up to len(U) rounds with the monitor. Returns (q, Z, switched, effort, min_target, first_r)."""
    N = len(U)
    if N == 0:
        return 0, 0, False, 0.0, math.inf
    if variant.monitor == "none" or pol.primary_array:
        m = np.asarray([ctx.clip(x) for x in pol.primary_targets(ctx, tau, r0, N)]) if pol.primary_array else None
        if m is None:  # Z-dependent policy without monitor: loop
            return _loop_segment(ctx, pol, tau, U, d, variant, r0)
        stream = U < m
        cs = np.cumsum(stream); rr = np.arange(1, N + 1)
        if variant.monitor == "none":
            crossing = np.array([], dtype=int)
        elif variant.monitor == "anytime":
            crossing = np.flatnonzero(cs < rr * tau - d.b(rr))
        elif variant.monitor == "noslack":
            crossing = np.flatnonzero(cs < rr * tau)
        elif variant.monitor == "windowed":
            w = variant.window
            win = np.full(N, False)
            if N >= w:
                cw = cs[w - 1:] - np.concatenate(([0], cs[:-w]))
                win[w - 1:] = cw < w * tau - math.sqrt(w * d.log2n4 / 2)
            crossing = np.flatnonzero(win)
        else:
            raise ValueError(variant.monitor)
        q = int(crossing[0] + 1) if crossing.size else N
        switched = bool(crossing.size)
        Z = int(cs[q - 1])
        effort = float(np.sum(m[:q] - ctx.mu))
        return q, Z, switched, effort, float(m[:q].min())
    return _loop_segment(ctx, pol, tau, U, d, variant, r0)


def _loop_segment(ctx, pol, tau, U, d, variant, r0):
    N = len(U); Z = 0; effort = 0.0; mn = math.inf
    w = variant.window; hist = []
    for r in range(1, N + 1):
        m = ctx.clip(pol.primary_target(ctx, r0 + r, Z, tau))
        y = int(U[r - 1] < m); Z += y; effort += m - ctx.mu; mn = min(mn, m); hist.append(y)
        if variant.monitor == "anytime" and Z < r * tau - math.sqrt(r * d.log2n4 / 2):
            return r, Z, True, effort, mn
        if variant.monitor == "noslack" and Z < r * tau:
            return r, Z, True, effort, mn
        if variant.monitor == "windowed" and r >= w and sum(hist[-w:]) < w * tau - math.sqrt(w * d.log2n4 / 2):
            return r, Z, True, effort, mn
    return N, Z, False, effort, mn


def episode(inst: Instance, n: int, variant: Variant, policies: list[Policy], gens: dict) -> dict:
    """One coupled episode. gens: dict with Generators 'bid', 'primary', 'fallback', 'mechanism', 'deviation'."""
    K = inst.K
    d = make_design(n, K, L=variant.L)
    L, N = d.L, d.N
    ctxs = [AgentCtx(i, inst.mu[i], inst.M[i], inst.is_honest(i), K, n, d, gens["deviation"]) for i in range(K)]
    pulls = np.zeros(K, int); effort = np.zeros(K); own_pulls = np.zeros(K, int); own_succ = np.zeros(K, int)
    reward = 0
    # Stage 1
    U_bid = gens["bid"].random((K, L))
    succ = np.zeros(K, int)
    for i, pol in enumerate(policies):
        c = ctxs[i]
        if pol.constant_bid:
            m = c.clip(pol.bid_target(c, 0, 0)); y = U_bid[i] < m; succ[i] = int(y.sum()); effort[i] += L * (m - c.mu)
        else:
            z = 0
            for r in range(L):
                m = c.clip(pol.bid_target(c, r, z)); y = int(U_bid[i, r] < m); z += y; effort[i] += m - c.mu
            succ[i] = z
    stage1_effort = effort.copy()
    pulls += L; own_pulls += L; own_succ += succ; reward += int(succ.sum())
    beta = succ / L
    priority = gens["mechanism"].permutation(K); rank = np.empty(K, int); rank[priority] = np.arange(K)
    order = sorted(range(K), key=lambda i: (-beta[i], rank[i]))
    W = order[0]; tau = _price(beta[order[1]], d, variant.price_mode)
    # Stage 2 (possibly several monitored segments under exclusion)
    U_pri = gens["primary"].random(N)
    U_fb = None
    q, Z, switched, eff, mn = _monitored_segment(ctxs[W], policies[W], tau, U_pri, d, variant)
    pulls[W] += q; own_pulls[W] += q; own_succ[W] += Z; effort[W] += eff; reward += Z
    false_switch = int(switched and mn >= tau - 1e-12)
    primary_rounds = q; fallback_rounds = N - q if switched else 0
    detection = q if switched else -1
    exclusions = 0; fb_reward = 0; fb_pulls = np.zeros(K, int); effort_before_fb = effort.copy(); pulls_before_fb = pulls.copy()
    if switched and fallback_rounds > 0:
        H = fallback_rounds
        U_fb = gens["fallback"].random((H, K))
        t0 = 0
        if variant.fallback == "exclude":
            excluded = {W}; remaining = [i for i in order if i not in excluded]
            while t0 < H and remaining:
                exclusions += 1
                Wn = remaining[0]
                if len(remaining) >= 2:
                    tau_n = _price(beta[remaining[1]], d, variant.price_mode); var_n = variant
                else:
                    tau_n = 0.0; var_n = Variant(monitor="none")
                Useg = U_fb[t0:, Wn]
                qn, Zn, swn, effn, _ = _monitored_segment(ctxs[Wn], policies[Wn], tau_n, Useg, d, var_n, r0=0)
                pulls[Wn] += qn; own_pulls[Wn] += qn; own_succ[Wn] += Zn; effort[Wn] += effn; reward += Zn; fb_reward += Zn
                fb_pulls[Wn] += qn; t0 += qn
                if swn:
                    excluded.add(Wn); remaining = [i for i in order if i not in excluded]
                else:
                    break
            if t0 < H:  # everyone excluded: cyclic allocation without monitor (keeps the horizon identity)
                for t in range(t0, H):
                    a = t % K; c = ctxs[a]; m = c.clip(policies[a].fallback_target(c, t, own_pulls[a], own_succ[a], H))
                    y = int(U_fb[t, a] < m); pulls[a] += 1; own_pulls[a] += 1; own_succ[a] += y; effort[a] += m - c.mu
                    reward += y; fb_reward += y; fb_pulls[a] += 1
        elif variant.fallback == "runnerup":
            a = order[1]; c = ctxs[a]
            m_arr = np.array([c.clip(policies[a].fallback_target(c, t, own_pulls[a], own_succ[a], H)) for t in range(H)])
            y = U_fb[:, a] < m_arr; pulls[a] += H; own_pulls[a] += H; own_succ[a] += int(y.sum()); effort[a] += float(np.sum(m_arr - c.mu))
            reward += int(y.sum()); fb_reward += int(y.sum()); fb_pulls[a] += H
        elif variant.fallback == "roundrobin":
            for t in range(H):
                a = t % K; c = ctxs[a]; m = c.clip(policies[a].fallback_target(c, t, own_pulls[a], own_succ[a], H))
                y = int(U_fb[t, a] < m); pulls[a] += 1; own_pulls[a] += 1; own_succ[a] += y; effort[a] += m - c.mu
                reward += y; fb_reward += y; fb_pulls[a] += 1
        elif variant.fallback in ("exp3", "exp3_warm"):
            gamma, eta = exp3_constants(K, H)
            logw = np.zeros(K) if variant.fallback == "exp3" else eta * L * beta  # warm start from Stage-1 bids
            coins = gens["mechanism"].random(H)
            for t in range(H):
                z = logw - logw.max(); qv = np.exp(z); qv /= qv.sum(); p = (1 - gamma) * qv + gamma / K
                a = int(np.searchsorted(np.cumsum(p), coins[t], side="right")); a = min(a, K - 1)
                c = ctxs[a]; m = c.clip(policies[a].fallback_target(c, t, own_pulls[a], own_succ[a], H))
                y = int(U_fb[t, a] < m); pulls[a] += 1; own_pulls[a] += 1; own_succ[a] += y; effort[a] += m - c.mu
                reward += y; fb_reward += y; fb_pulls[a] += 1; logw[a] += eta * y / p[a]
        elif variant.fallback in ("ucb", "ucb_warm"):
            cnt = np.zeros(K, int); sm = np.zeros(K)
            if variant.fallback == "ucb_warm":
                cnt += L; sm += succ
            init = list(gens["mechanism"].permutation(K)); ties = gens["mechanism"].random(H)
            for t in range(H):
                if variant.fallback == "ucb" and t < K:
                    a = int(init[t])
                else:
                    idx = sm / np.maximum(cnt, 1) + ucb_bonus(cnt, t + 1, H)
                    best = np.flatnonzero(idx >= idx.max() - 1e-12); a = int(best[int(ties[t] * len(best)) % len(best)])
                c = ctxs[a]; m = c.clip(policies[a].fallback_target(c, t, own_pulls[a], own_succ[a], H))
                y = int(U_fb[t, a] < m); pulls[a] += 1; own_pulls[a] += 1; own_succ[a] += y; effort[a] += m - c.mu
                reward += y; fb_reward += y; fb_pulls[a] += 1; cnt[a] += 1; sm[a] += y
        else:
            raise ValueError(variant.fallback)
    assert pulls.sum() == n, (pulls.sum(), n)
    utility = pulls - effort
    out = {"n": n, "K": K, "variant": variant.name, "L": L, "N": N, "s": d.s, "tau": tau, "winner": W,
           "beta_second": float(beta[order[1]]), "platform_reward": reward, "stage1_rounds": K * L,
           "primary_rounds": primary_rounds, "fallback_rounds": fallback_rounds, "switched": int(switched),
           "false_switch": false_switch, "detection_delay": detection, "exclusions": exclusions,
           "fallback_reward": fb_reward, "focal": inst.focal, "focal_won": int(W == inst.focal),
           "focal_utility": float(utility[inst.focal]), "total_effort": float(effort.sum()),
           "focal_utility_prefb": float(pulls_before_fb[inst.focal] - effort_before_fb[inst.focal]),
           "focal_stage1_utility": float(L - stage1_effort[inst.focal]),
           "gap_private": inst.M2 * n - reward, "gap_honest": inst.mu_H_star * n - reward, "gap_capacity": inst.M_top * n - reward}
    for i in range(K):
        out[f"utility_{i}"] = float(utility[i]); out[f"pulls_{i}"] = int(pulls[i]); out[f"effort_{i}"] = float(effort[i]); out[f"beta_{i}"] = float(beta[i])
    return out
