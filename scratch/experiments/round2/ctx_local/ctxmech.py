"""Tape-coupled simulator for PL-MESP and its ablations (contextual ablation ladder).

Reused from scratch/experiments/round2/common/mechanism.py without modification: the `Variant` record, the
`Policy` classes and `behavior()`, `AgentCtx`, `_price`, `_monitored_segment` (the vectorised monitored Stage-2
segment with the four monitor rules) and `exp3_constants`. Reused from common/design.py: L_n, s_n, b_n, R_K.
Reused from common/seeds.py: the seed scheme.

What is new here is only the profile structure:

  * `simulate_local`  runs one independent scalar MESP per exact context profile, with the GLOBAL constants
    L_n, s_n, b_n(.) and gamma_n and the LOCAL lengths (K L_n Stage-1 visits, then N_z = V_z - K L_n monitored
    visits, then a locally restarted EXP3 tuned to n). This is PL-MESP (PROVER2 Section 2 with PROVER1's
    calibration, the adversary's Section 9.4 recommendation). A profile with V_z < K L_n never leaves Stage 1.
  * `simulate_shared` runs ONE bidding stage whose Stage-1 rewards are pooled across profiles, announces ONE
    price, picks ONE winner and runs ONE monitor and ONE fallback for the whole horizon. This is the ablation
    that removes profile-locality itself, i.e. the scalar mechanism run context-blind on a contextual instance.

Arrival order. `simulate_local` processes profiles in index order. For every profile-local mechanism and every
profile-local behaviour this is exact whatever the true interleaving, because the mechanism's state at a
profile is a function of that profile's own data (PROVER2 Lemma L) and utilities are additive over profiles.
It is NOT neutral for the one cross-profile behaviour, `cross_profile_freeride`, which reacts to a switch
elsewhere: processing profiles in blocks is the arrival path in which every visit to z_0 precedes every visit
to z_1, and under an evenly spread path that behaviour would start free riding later. `simulate_shared` uses
the evenly spread path explicitly, since a pooled mechanism does depend on the interleaving.

Coupling. All variants and all behaviours of a replicate share pre-drawn uniform tapes, indexed by
(profile, agent, local Stage-1 pull), (profile, local primary pull) and (profile, local fallback round, agent).
The tape index of a draw never depends on the variant or on the behaviour, so comparisons are paired.

Evidence category: SYNTHETIC PAIRED SIMULATION. Reported deviation values are lower bounds on exploitability
for the behaviour class simulated, never upper bounds and never evidence of equilibrium.
"""
from __future__ import annotations

import math
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

R2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R2))

from common.design import design as make_design, Design, exp3_constants  # noqa: E402
from common.mechanism import (Variant, AgentCtx, Policy, SStar, _price, _monitored_segment)  # noqa: E402
from ctx_local.plmesp_exact import CtxInstance, stage1_pull_counts  # noqa: E402


# The contextual ladder. Each rung changes exactly one component of PL-MESP.
CTX_VARIANTS = {
    "pl_mesp": Variant("pl_mesp"),
    "pl_nomonitor": Variant("pl_nomonitor", monitor="none"),
    "pl_windowed": Variant("pl_windowed", monitor="windowed", window=200),
    "pl_noslack": Variant("pl_noslack", monitor="noslack"),
    "pl_rawprice": Variant("pl_rawprice", price_mode="raw"),
    "pl_nofallback": Variant("pl_nofallback", fallback="roundrobin"),
    "pl_runnerup": Variant("pl_runnerup", fallback="runnerup"),
    "pl_shared": Variant("pl_shared"),          # handled by simulate_shared, not by the Variant fields
}
SHARED_RUNGS = {"pl_shared"}


class BidZero(Policy):
    """Stage-1 shading to the floor (0, or mu for an honest agent); S^* everywhere else. This is the
    deviation Proposition 6.1 of PROVER2.md makes explicit, taken to its feasible extreme."""
    name = "bid_zero"

    def bid_target(self, ctx, r, z):
        return ctx.mu if ctx.honest else 0.0


class SabotageAll(Policy):
    """Deliver the feasible floor in every phase at every profile: the strongest feasible sabotage."""
    name = "sabotage_all"

    def bid_target(self, ctx, r, z):
        return ctx.mu if ctx.honest else 0.0

    def primary_target(self, ctx, r, Z, tau):
        return ctx.mu if ctx.honest else 0.0

    def fallback_target(self, ctx, t, own_pulls, own_succ, H):
        return ctx.mu if ctx.honest else 0.0


class CtxPolicy:
    """A behaviour that may depend on the profile and on what happened at other profiles.

    `local(z)` returns the scalar Policy used at profile index z. `reset(ctx, n)` is called once per episode and
    `note_switch(z)` after every local switch, so a cross-profile behaviour can react to events elsewhere.
    """
    name = "s_star"
    cross_profile = False

    def __init__(self, pol: Policy | None = None):
        self._pol = pol or SStar()

    def reset(self, ctx, n):
        pass

    def note_switch(self, z):
        pass

    def local(self, z) -> Policy:
        return self._pol


class PerProfile(CtxPolicy):
    def __init__(self, pol: Policy, name: str):
        super().__init__(pol)
        self.name = name


class CrossProfileFreeRide(CtxPolicy):
    """The adversary's cross-profile deviation (c2 ADVERSARY Section 5.2): crash at the FIRST profile, then
    deliver zero everywhere once any local switch has been triggered anywhere."""
    name = "cross_profile_freeride"
    cross_profile = True

    def __init__(self):
        from common.mechanism import BaitSwitch, ZeroFallback
        super().__init__(SStar())
        self._crash = BaitSwitch()
        self._free = ZeroFallback()
        self._tripped = False

    def reset(self, ctx, n):
        self._tripped = False

    def note_switch(self, z):
        self._tripped = True

    def local(self, z):
        if z == 0:
            return self._crash
        return self._free if self._tripped else SStar()


LOCAL_EXTRA = {"bid_zero": BidZero, "sabotage_all": SabotageAll}


def ctx_behavior(name: str) -> CtxPolicy:
    from common import mechanism as M
    if name == "cross_profile_freeride":
        return CrossProfileFreeRide()
    if name in LOCAL_EXTRA:
        return PerProfile(LOCAL_EXTRA[name](), name)
    return PerProfile(M.behavior(name), name)


CTX_BEHAVIORS = ["profile", "all_max", "underbid_05", "underbid_15", "primary_shade_05", "primary_shade_15",
                 "bait_switch", "trigger_fallback_shade", "primary_own_capacity", "boundary_ride",
                 "zero_fallback", "cross_profile_freeride",
                 "bid_zero", "sabotage_all",
                 "joint:primary_shade_15", "joint:bait_switch", "joint:zero_fallback",
                 "joint:trigger_fallback_shade", "joint:sabotage_all"]


# == tapes

def make_tapes(ctx: CtxInstance, n: int, gens: dict):
    """Pre-draw every uniform a replicate can need, indexed so the index never depends on the variant."""
    K = ctx.K
    g = make_design(n, K)
    V = ctx.visits(n)
    return {"V": V, "L": g.L,
            "bid": [gens["bid"].random((K, g.L)) for _ in V],
            "pri": [gens["primary"].random(max(v, 1)) for v in V],
            "fb": [gens["fallback"].random((max(v, 1), K)) for v in V],
            "prio": [gens["mechanism"].permutation(K) for _ in V],
            "coin": [gens["mechanism"].random(max(v, 1)) for v in V]}


# == the two simulators

def _fallback_segment(loc, ctxs, policies, variant, d, K, H, U_fb, coins, beta, order, acc, n):
    """Run the local Stage-3 phase for H visits. Returns the reward collected. `acc` accumulates per agent."""
    if H <= 0:
        return 0
    rew = 0
    if variant.fallback == "roundrobin":
        for t in range(H):
            a = t % K
            c = ctxs[a]
            m = c.clip(policies[a].fallback_target(c, t, acc["own_pulls"][a], acc["own_succ"][a], H))
            y = int(U_fb[t, a] < m)
            acc["pulls"][a] += 1; acc["own_pulls"][a] += 1; acc["own_succ"][a] += y
            acc["effort"][a] += m - c.mu; rew += y
    elif variant.fallback == "runnerup":
        a = order[1]
        c = ctxs[a]
        m_arr = np.array([c.clip(policies[a].fallback_target(c, t, acc["own_pulls"][a], acc["own_succ"][a], H))
                          for t in range(H)])
        y = int(np.sum(U_fb[:H, a] < m_arr))
        acc["pulls"][a] += H; acc["own_pulls"][a] += H; acc["own_succ"][a] += y
        acc["effort"][a] += float(np.sum(m_arr - c.mu)); rew += y
    elif variant.fallback == "exp3":
        # single local EXP3, fresh weights, tuned to the GLOBAL horizon n (PROVER2 Section 2, Lemma F)
        gamma, eta = exp3_constants(K, n)
        logw = np.zeros(K)
        for t in range(H):
            z = logw - logw.max(); qv = np.exp(z); qv /= qv.sum()
            p = (1 - gamma) * qv + gamma / K
            a = min(int(np.searchsorted(np.cumsum(p), coins[t], side="right")), K - 1)
            c = ctxs[a]
            m = c.clip(policies[a].fallback_target(c, t, acc["own_pulls"][a], acc["own_succ"][a], H))
            y = int(U_fb[t, a] < m)
            acc["pulls"][a] += 1; acc["own_pulls"][a] += 1; acc["own_succ"][a] += y
            acc["effort"][a] += m - c.mu; rew += y
            logw[a] += eta * y / p[a]
    else:
        raise ValueError(variant.fallback)
    return rew


def _assign(pols, cpol, zi, focal, joint, honest):
    """Give the deviating behaviour to the focal agent, or to every strategic agent when `joint`."""
    if joint:
        for i in range(len(pols)):
            if i not in honest:
                pols[i] = cpol.local(zi)
    else:
        pols[focal] = cpol.local(zi)
    return pols


def simulate_local(ctx: CtxInstance, n: int, variant: Variant, cpol: CtxPolicy, focal: int, tapes: dict,
                   joint: bool = False) -> dict:
    """PL-MESP (or a local ablation of it) on a deterministic arrival path with visit counts tapes['V']."""
    K = ctx.K
    g = make_design(n, K)
    L = g.L
    V = tapes["V"]
    acc = {"pulls": np.zeros(K), "own_pulls": np.zeros(K, int), "own_succ": np.zeros(K, int),
           "effort": np.zeros(K)}
    cpol.reset(ctx, n)
    reward = 0
    switches = 0
    false_switches = 0
    monitored_profiles = 0
    delays = []
    prices = []
    stage1_rounds = 0
    per_profile = []
    for zi, (p, V_z) in enumerate(zip(ctx.profiles, V)):
        loc = ctx.local(p)
        pols = [SStar()] * K
        pols = _assign(pols, cpol, zi, focal, joint, ctx.honest)
        ctxs = [AgentCtx(i, loc.mu[i], loc.M[i], loc.is_honest(i), K, n, g, None) for i in range(K)]
        l = stage1_pull_counts(V_z, K, L)
        stage1_rounds += int(l.sum())
        succ = np.zeros(K, int)
        for i in range(K):
            c = ctxs[i]
            pol = pols[i]
            if l[i] == 0:
                continue
            if pol.constant_bid:
                m = c.clip(pol.bid_target(c, 0, zi))
                y = tapes["bid"][zi][i, :l[i]] < m
                succ[i] = int(y.sum())
                acc["effort"][i] += l[i] * (m - c.mu)
            else:
                s = 0
                for r in range(l[i]):
                    m = c.clip(pol.bid_target(c, r, zi))
                    yy = int(tapes["bid"][zi][i, r] < m); s += yy
                    acc["effort"][i] += m - c.mu
                succ[i] = s
            acc["pulls"][i] += l[i]; acc["own_pulls"][i] += l[i]; acc["own_succ"][i] += succ[i]
        reward += int(succ.sum())
        if V_z < K * L:                                   # Stage 1 never completes at this profile
            per_profile.append({"z": p["z"], "V_z": V_z, "truncated": True, "tau": None, "switched": 0})
            continue
        beta = succ / L
        rank = np.empty(K, int); rank[tapes["prio"][zi]] = np.arange(K)
        order = sorted(range(K), key=lambda i: (-beta[i], rank[i]))
        W = order[0]
        tau = _price(beta[order[1]], g, variant.price_mode)
        prices.append(tau)
        N_z = V_z - K * L
        d = Design(n=n, K=K, L=L, N=N_z, s=g.s, log2n4=g.log2n4)
        monitored_profiles += 1
        q, Z, switched, eff, mn = _monitored_segment(ctxs[W], pols[W], tau, tapes["pri"][zi][:N_z], d, variant)
        acc["pulls"][W] += q; acc["own_pulls"][W] += q; acc["own_succ"][W] += Z; acc["effort"][W] += eff
        reward += Z
        switches += int(switched)
        if switched:
            delays.append(q)
            if mn >= tau - 1e-12:
                false_switches += 1
            cpol.note_switch(zi)
            pols = _assign(pols, cpol, zi, focal, joint, ctx.honest)
            H = N_z - q
            reward += _fallback_segment(loc, ctxs, pols, variant, d, K, H, tapes["fb"][zi],
                                        tapes["coin"][zi], beta, order, acc, n)
        per_profile.append({"z": p["z"], "V_z": V_z, "truncated": False, "tau": float(tau), "winner": int(W),
                            "switched": int(switched), "primary_pulls": int(q),
                            "false_switch": int(switched and mn >= tau - 1e-12)})
    assert abs(acc["pulls"].sum() - n) < 1e-9, (acc["pulls"].sum(), n)
    return _finish(ctx, n, variant.name, ("joint:" if joint else "") + cpol.name, focal, acc, reward,
                   switches, false_switches, monitored_profiles, delays, prices, stage1_rounds, per_profile)


def simulate_shared(ctx: CtxInstance, n: int, variant: Variant, cpol: CtxPolicy, focal: int, tapes: dict,
                    joint: bool = False) -> dict:
    """The ablation that removes profile-locality: statistics pooled across profiles.

    One bidding stage of K L_n rounds taken off the front of the arrival path, bids pooled over whichever
    profiles those rounds fell in, one price, one winner, one monitor over all n - K L_n remaining rounds and
    one fallback. The agents' capacities still depend on the profile, so a pooled bid estimates a visit-weighted
    average capacity rather than any one capacity.
    """
    K = ctx.K
    g = make_design(n, K)
    L = g.L
    V = tapes["V"]
    path = arrival_path_cached(tuple(V))
    acc = {"pulls": np.zeros(K), "own_pulls": np.zeros(K, int), "own_succ": np.zeros(K, int),
           "effort": np.zeros(K)}
    cpol.reset(ctx, n)
    locs = [ctx.local(p) for p in ctx.profiles]
    ctxs_by_z = [[AgentCtx(i, lo.mu[i], lo.M[i], lo.is_honest(i), K, n, g, None) for i in range(K)] for lo in locs]
    # Stage 1: rounds 1 .. K L_n, agent ((t-1) mod K) + 1, tape indexed by (profile, agent, local pull)
    used = np.zeros((len(V), K), int)
    succ = np.zeros(K, int)
    KL = min(K * L, n)
    for t in range(KL):
        i = t % K
        zi = path[t]
        c = ctxs_by_z[zi][i]
        pol = cpol.local(zi) if (i == focal or (joint and i not in ctx.honest)) else SStar()
        m = c.clip(pol.bid_target(c, used[zi, i], zi))
        u = tapes["bid"][zi][i, used[zi, i] % L]
        y = int(u < m)
        used[zi, i] += 1
        succ[i] += y
        acc["pulls"][i] += 1; acc["own_pulls"][i] += 1; acc["own_succ"][i] += y; acc["effort"][i] += m - c.mu
    reward = int(succ.sum())
    cnt = np.array([max(1, KL // K + (1 if i < KL % K else 0)) for i in range(K)])
    beta = succ / cnt
    rank = np.empty(K, int); rank[tapes["prio"][0]] = np.arange(K)
    order = sorted(range(K), key=lambda i: (-beta[i], rank[i]))
    W = order[0]
    tau = _price(beta[order[1]], g, variant.price_mode)
    N = n - KL
    Z = 0
    q = 0
    switched = False
    mn = math.inf
    pri_used = np.zeros(len(V), int)
    for r in range(1, N + 1):
        zi = path[KL + r - 1]
        c = ctxs_by_z[zi][W]
        pol = cpol.local(zi) if (W == focal or (joint and W not in ctx.honest)) else SStar()
        m = c.clip(pol.primary_target(c, r, Z, tau))
        u = tapes["pri"][zi][pri_used[zi] % max(V[zi], 1)]
        pri_used[zi] += 1
        y = int(u < m)
        Z += y
        q = r
        acc["pulls"][W] += 1; acc["own_pulls"][W] += 1; acc["own_succ"][W] += y; acc["effort"][W] += m - c.mu
        mn = min(mn, m)
        reward += y
        if variant.monitor == "anytime" and Z < r * tau - math.sqrt(r * g.log2n4 / 2):
            switched = True
        elif variant.monitor == "noslack" and Z < r * tau:
            switched = True
        if switched:
            break
    false_switch = int(switched and mn >= tau - 1e-12)
    delays = [q] if switched else []
    if switched and N - q > 0:
        H = N - q
        gamma, eta = exp3_constants(K, n)
        logw = np.zeros(K)
        fb_used = np.zeros(len(V), int)
        for t in range(H):
            zi = path[KL + q + t]
            zv = logw - logw.max(); qv = np.exp(zv); qv /= qv.sum()
            p = (1 - gamma) * qv + gamma / K
            coin = tapes["coin"][zi][fb_used[zi] % max(V[zi], 1)]
            a = min(int(np.searchsorted(np.cumsum(p), coin, side="right")), K - 1)
            c = ctxs_by_z[zi][a]
            pol = cpol.local(zi) if (a == focal or (joint and a not in ctx.honest)) else SStar()
            m = c.clip(pol.fallback_target(c, t, acc["own_pulls"][a], acc["own_succ"][a], H))
            u = tapes["fb"][zi][fb_used[zi] % max(V[zi], 1), a]
            fb_used[zi] += 1
            y = int(u < m)
            acc["pulls"][a] += 1; acc["own_pulls"][a] += 1; acc["own_succ"][a] += y
            acc["effort"][a] += m - c.mu
            reward += y
            logw[a] += eta * y / p[a]
    assert abs(acc["pulls"].sum() - n) < 1e-9, (acc["pulls"].sum(), n)
    return _finish(ctx, n, variant.name, ("joint:" if joint else "") + cpol.name, focal, acc, reward,
                   int(switched), false_switch, 1, delays, [tau], KL, [])


_PATH_CACHE = {}


def arrival_path_cached(V: tuple) -> np.ndarray:
    if V not in _PATH_CACHE:
        _PATH_CACHE[V] = arrival_path(list(V))
    return _PATH_CACHE[V]


def arrival_path(V) -> np.ndarray:
    """A deterministic arrival path realising the visit counts V, spreading each profile as evenly as possible
    (largest-remainder round robin). Hypothesis (H3) permits a deterministic path."""
    n = int(sum(V))
    out = np.zeros(n, dtype=int)
    rem = np.array(V, dtype=float)
    credit = np.zeros(len(V))
    share = np.array(V, dtype=float) / max(n, 1)
    for t in range(n):
        credit += share
        avail = rem > 0
        c = np.where(avail, credit, -np.inf)
        zi = int(np.argmax(c))
        out[t] = zi
        credit[zi] -= 1.0
        rem[zi] -= 1
    return out


def _finish(ctx, n, variant_name, behavior_name, focal, acc, reward, switches, false_switches,
            monitored_profiles, delays, prices, stage1_rounds, per_profile):
    K = ctx.K
    utility = acc["pulls"] - acc["effort"]
    V = ctx.visits(n)
    bench_M2 = sum(v * ctx.local(p).M2 for v, p in zip(V, ctx.profiles)) / n
    bench_hon = sum(v * ctx.local(p).mu_H_star for v, p in zip(V, ctx.profiles)) / n
    bench_top = sum(v * ctx.local(p).M_top for v, p in zip(V, ctx.profiles)) / n
    out = {"instance": ctx.id, "Q": ctx.Q, "K": K, "n": n, "variant": variant_name, "behavior": behavior_name,
           "focal": focal, "platform_reward": reward, "platform_reward_per_round": reward / n,
           "focal_utility": float(utility[focal]), "focal_utility_per_round": float(utility[focal]) / n,
           "switches": switches, "false_switches": false_switches, "monitored_profiles": monitored_profiles,
           "mean_detection_delay": float(np.mean(delays)) if delays else -1.0,
           "median_detection_delay": float(np.median(delays)) if delays else -1.0,
           "mean_price": float(np.mean(prices)) if prices else -1.0,
           "stage1_rounds": stage1_rounds, "total_effort": float(acc["effort"].sum()),
           "benchmark_M2_per_round": bench_M2, "benchmark_honest_per_round": bench_hon,
           "benchmark_top_per_round": bench_top,
           "gap_honest_per_round": bench_hon - reward / n, "gap_M2_per_round": bench_M2 - reward / n}
    for i in range(K):
        out[f"utility_{i}"] = float(utility[i])
        out[f"pulls_{i}"] = float(acc["pulls"][i])
    return out


def run_episode(ctx: CtxInstance, n: int, rung: str, behavior_name: str, focal: int, gens: dict) -> dict:
    """`behavior_name` may be prefixed with 'joint:' to give the behaviour to every strategic agent."""
    joint = behavior_name.startswith("joint:")
    tapes = make_tapes(ctx, n, gens)
    variant = CTX_VARIANTS[rung]
    cpol = ctx_behavior(behavior_name[6:] if joint else behavior_name)
    if rung in SHARED_RUNGS:
        return simulate_shared(ctx, n, variant, cpol, focal, tapes, joint=joint)
    return simulate_local(ctx, n, variant, cpol, focal, tapes, joint=joint)
