"""Exact certified exploitability, revenue and benchmarks for PL-MESP (the profile-local mechanism).

Mechanism. PL-MESP as adjudicated in audit/round2/B/theorems/c2-local-mesp/ADVERSARY.md Section 9.4:
PROVER2 Section 2 mechanism (one independent scalar MESP per exact context profile, round-robin Stage 1,
a single locally restarted EXP3 tuned to the GLOBAL horizon n) with PROVER1's calibration
(s_n = sqrt(log(2 K n^4) / (2 L_n)), b_n(r) = sqrt(r log(2 n^4) / 2)), which is exactly the calibration
already coded in scratch/experiments/round2/common/design.py for the scalar mechanism.

Code reused rather than rewritten:
  common/design.py                                   L_n, s_n, b_n, gamma_n, R_K   (unchanged)
  audit/.../e1-equilibrium-strength/bidprofile.py    the exact per-profile two-action backward induction,
                                                     the exact bid/winner laws, the exact revenue bracket
  audit/.../e1-equilibrium-strength/ctxprofile.py    local_design() and fallback_bound(), the substitutions
                                                     that turn the scalar computation into the local one
This module adds: the profile-count/horizon/instance grid, truncated profiles (V_z < K L_n, which
ctxprofile.py refuses), the profile-local theorem constant, the honest and second-capacity benchmarks, and
the exactness argument for aggregating per-profile values (docstring of `solve_instance`).

Evidence category: EXACT COMPUTATION. Nothing here is sampled. The only approximations are double-precision
arithmetic and an explicitly accounted truncation of Stage-1 count mass below `mass_tol`, which is carried
into the bracket as `2 n * dropped` (bidprofile.py) and reported per cell.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R2 = HERE.parent                      # scratch/experiments/round2
REPO = R2.parents[2]
E1 = REPO / "audit" / "round2" / "B" / "theorems" / "e1-equilibrium-strength"
sys.path.insert(0, str(R2))
sys.path.insert(0, str(E1))

from common.design import design as make_design, Design, R_K  # noqa: E402
from common import instances as I  # noqa: E402
import bidprofile as BP  # noqa: E402


# == mechanism constants

def local_design(n: int, K: int, V_z: int) -> Design:
    """Global tuning constants, local primary length N_z = V_z - K L_n (ctxprofile.local_design, extended to
    return None-free objects for truncated profiles; callers must check V_z >= K L_n first)."""
    g = make_design(n, K)
    return Design(n=n, K=K, L=g.L, N=V_z - K * g.L, s=g.s, log2n4=g.log2n4)


def fallback_bound(n: int, K: int, N: int) -> np.ndarray:
    """Prefix regret bound of the single local EXP3 tuned to the global horizon, indexed by H = 0..N.

    PROVER2 Lemma F (prefix form), adversary Section 9.1: with gamma_n = min{1/2, sqrt(K log K / n)} the
    exponential-potential inequality holds for every prefix and gives 2 gamma_n H + K log K / gamma_n, which is
    at most R_K(n) = 3 sqrt(K n log K) + 2 K log K for H <= n. Copied from ctxprofile.fallback_bound.
    """
    H = np.arange(N + 1, dtype=float)
    gamma = min(0.5, math.sqrt(K * math.log(K) / n)) if K > 1 else 0.0
    loss = 2.0 * gamma * H + (K * math.log(K) / gamma if gamma > 0 else 0.0)
    return np.minimum(loss, R_K(K, n))


def theorem_constant(n: int, K: int, Q: int, nontop_deltas=(), cap_at_2n: bool = True) -> dict:
    """The profile-local equilibrium bound of the published statement, term by term.

    PROVER2 Section 4.2/4.3(A) error terms with PROVER1's calibration and PROVER1's cap min{Q L_n, n}
    (adversary Section 9.4, finding F7):

        e_bid  = min{Q L_n, n}                                bidding effort saved, one block per profile
        e_mon  = Q + sqrt(2 Q n log(2 n^4))                   Q times (1 + 2 b_n(V_z)) after Cauchy-Schwarz
        e_fb   = Q R_K(n)                                     one fallback per profile
        e_low  = sum over the deviator's non-top profiles of  8 (1 + sqrt(2 log(2 n^4)))^2 / delta^2
                                                              + 2 R_K(n) / delta
        + 6 n^{-3}

    `nontop_branch_active` is the proof's own finite-n condition 4 s_n <= min delta; when it fails the
    comparison of a certified interval against this constant is invalid, exactly as recorded for the scalar
    non-top branch in audit/round2/A/EXPERIMENT_FINAL_REPORT.md Section 8 item 2.
    """
    d = make_design(n, K)
    ell = d.log2n4
    e_bid = min(Q * d.L, n) if cap_at_2n else Q * d.L
    e_mon = Q + math.sqrt(2.0 * Q * n * ell)
    e_fb = Q * R_K(K, n)
    e_low = 0.0
    for delta in nontop_deltas:
        e_low += 8.0 * (1.0 + math.sqrt(2.0 * ell)) ** 2 / delta ** 2 + 2.0 * R_K(K, n) / delta
    total = e_bid + e_mon + e_fb + e_low + 6.0 * n ** -3
    active = (4.0 * d.s <= min(nontop_deltas)) if nontop_deltas else True
    return {"e_bid": e_bid, "e_mon": e_mon, "e_fb": e_fb, "e_low": e_low,
            "constant": total, "constant_per_round": total / n,
            "constant_is_vacuous": total >= 2.0 * n, "nontop_branch_active": bool(active),
            "L_n": d.L, "s_n": d.s, "b_n_of_n": float(d.b(n)), "R_K_n": R_K(K, n),
            "KL_n": K * d.L, "n_over_KL": n / (K * d.L)}


# == instance families

class CtxInstance:
    """Q exact profiles, each with its own primitives, plus a deterministic visit allocation."""

    def __init__(self, ident, K, honest, focal, profiles):
        self.id = ident
        self.K = int(K)
        self.honest = tuple(honest)
        self.focal = int(focal)
        self.profiles = profiles           # list of dicts with 'z', 'mu', 'M', 'share'
        assert abs(sum(p["share"] for p in profiles) - 1.0) < 1e-12
        assert focal not in self.honest
        for p in profiles:
            assert len(p["mu"]) == len(p["M"]) == self.K
            for i in range(self.K):
                assert 0.0 <= p["mu"][i] <= p["M"][i] <= 1.0

    @property
    def Q(self):
        return len(self.profiles)

    def local(self, p):
        return I.Instance(id=f"{self.id}/{p['z']}", alias=p["z"], mu=tuple(p["mu"]), M=tuple(p["M"]),
                          honest=self.honest, focal=self.focal, index=0)

    def visits(self, n):
        """Deterministic arrival path: V_z = round(share * n), remainder on the last profile.

        Hypothesis (H3) of PROVER2 allows a deterministic arrival path, so conditioning on one is not a
        restriction of the theorem; every bound below is a statement about that path.
        """
        V = [int(round(p["share"] * n)) for p in self.profiles]
        V[-1] = n - sum(V[:-1])
        assert min(V) >= 0 and sum(V) == n
        return V


def _prof(z, mu, M, share):
    return {"z": z, "mu": list(mu), "M": list(M), "share": share}


def family(name: str, Q: int) -> CtxInstance:
    """The instance families of this package. `Q` is the number of exact context profiles.

    replicated_unique_top  every profile carries the scalar instance `unique_top`   (K = 3, gap 0.25)
    replicated_tied_top    every profile carries the scalar instance `tied_top`     (K = 3, tie)
    replicated_K2_unique   every profile carries `K2_unique_top`                    (K = 2, gap 0.25)
    replicated_honest_top  every profile carries `honest_top`, in which the honest agent is the top agent and
                           mu_H^* = 0.75, so joint shading by the two strategic agents can drive the platform
                           below the honest benchmark
    rotating_top           capacities of the two strategic agents swap with the profile index, so the focal
                           agent is top at ceil(Q/2) profiles and non-top (gap 0.15) at the rest
    regime_switch          alternating high-capacity and low-capacity profiles, built so that the pooled second
                           capacity exceeds the largest capacity at a low profile
    heterogeneous          capacities move linearly across profiles: the focal agent goes from top with a
                           large gap to non-top with a large gap, passing through a near tie
    unbalanced_unique_top  `replicated_unique_top` primitives with geometrically decreasing visit shares, so
                           the later profiles are truncated before Stage 1 completes

    The three `replicated_*` families are degenerate contextual environments: the primitives do not depend on
    the profile, so the scalar mechanism is available and PL-MESP pays pure localisation overhead. They are the
    families in which the Q = 1 cell is literally the scalar mechanism on the scalar instance of the same name.
    """
    if name.startswith("replicated_"):
        base = {"replicated_unique_top": "unique_top", "replicated_tied_top": "tied_top",
                "replicated_K2_unique": "K2_unique_top", "replicated_near_gap": "near_gap",
                "replicated_honest_top": "honest_top"}[name]
        b = I.get(base)
        return CtxInstance(f"{name}_Q{Q}", b.K, b.honest, b.focal,
                           [_prof(f"z{l}", b.mu, b.M, 1.0 / Q) for l in range(Q)])
    if name == "unbalanced_unique_top":
        b = I.get("unique_top")
        w = np.array([2.0 ** -l for l in range(Q)])
        w = w / w.sum()
        return CtxInstance(f"{name}_Q{Q}", b.K, b.honest, b.focal,
                           [_prof(f"z{l}", b.mu, b.M, float(w[l])) for l in range(Q)])
    if name == "regime_switch":
        # Half the profiles have high capacities and half low ones, chosen so that the SECOND capacity of the
        # pooled (visit-weighted average) bids, 0.625, exceeds the LARGEST capacity at a low profile, 0.45.
        # A mechanism that shares Stage-1 statistics across profiles therefore announces, at every low profile,
        # a price no agent there can meet, and its monitor convicts a fully compliant winner. This is the exact
        # failure Corollary 4.3 of PROVER2.md describes for a cell over which the capacities vary.
        mu = (0.10, 0.20, 0.15)
        profs = []
        for l in range(Q):
            M = (0.90, 0.85, 0.40) if l % 2 == 0 else (0.45, 0.40, 0.25)
            profs.append(_prof(("zhigh%d" % l) if l % 2 == 0 else ("zlow%d" % l), mu, M, 1.0 / Q))
        return CtxInstance(f"{name}_Q{Q}", 3, (2,), 0, profs)
    if name == "rotating_top":
        mu = (0.10, 0.20, 0.35)
        profs = []
        for l in range(Q):
            M = (0.80, 0.65, 0.40) if l % 2 == 0 else (0.65, 0.80, 0.40)
            profs.append(_prof(f"z{l}", mu, M, 1.0 / Q))
        return CtxInstance(f"{name}_Q{Q}", 3, (2,), 0, profs)
    if name == "heterogeneous":
        mu = (0.10, 0.20, 0.35)
        profs = []
        for l in range(Q):
            u = l / max(Q - 1, 1)
            M0 = 0.90 - 0.30 * u
            M1 = 0.55 + 0.30 * u
            profs.append(_prof(f"z{l}", mu, (round(M0, 6), round(M1, 6), 0.40), 1.0 / Q))
        return CtxInstance(f"{name}_Q{Q}", 3, (2,), 0, profs)
    raise KeyError(name)


FAMILIES = ["replicated_unique_top", "replicated_tied_top", "replicated_K2_unique", "replicated_near_gap",
            "replicated_honest_top",
            "unbalanced_unique_top", "rotating_top", "heterogeneous", "regime_switch"]


# == per-profile exact values

def stage1_pull_counts(V_z: int, K: int, L: int) -> np.ndarray:
    """Number of Stage-1 pulls each agent receives at a profile with V_z visits.

    Stage 1 at z occupies the first min(V_z, K L) visits and pulls agent ((v - 1) mod K) + 1 at visit v
    (PROVER2 Section 2). Agent index i (0-based) is the mechanism's agent i + 1.
    """
    v = min(V_z, K * L)
    full, rem = divmod(v, K)
    out = np.full(K, full, dtype=int)
    out[:rem] += 1
    return out


def truncated_profile(inst_local, n: int, K: int, V_z: int, L: int, focal: int) -> dict:
    """Exact values at a profile whose Stage 1 never completes (V_z < K L_n): no price, no monitor, no fallback.

    Every visit is a Stage-1 pull. A Stage-1 pull of agent j is worth 1 + mu_j - m to j for whatever target m it
    chooses, and contributes m to the platform in expectation, so both the deviator's optimum and the baseline
    are available in closed form with no bracket at all.
    """
    l = stage1_pull_counts(V_z, K, L)
    mu, M = inst_local.mu[focal], inst_local.M[focal]
    lo = mu if inst_local.is_honest(focal) else 0.0
    base = l[focal] * (1.0 + mu - M)
    best = l[focal] * (1.0 + mu - lo)
    revenue = float(sum(l[j] * inst_local.M[j] for j in range(K)))
    return {"V_z": V_z, "N_z": 0, "truncated": True, "stage1_pulls_focal": int(l[focal]),
            "base_LB": base, "base_UB": base, "V_F0": best, "V_FUB": best,
            "exploit_LB": best - base, "exploit_UB": best - base,
            "revenue_LB": revenue, "revenue_UB": revenue, "dropped_mass": 0.0}


def solve_instance(ctx: CtxInstance, n: int, log=print) -> dict:
    """Exact certified interval for the focal agent's deviation gain against PL-MESP, plus revenue.

    Why a per-profile computation is exact for the fully global-history-adaptive class B^ctx_{i,n}.
    (1) Realized utility is additive over profiles and expectation is additive with no independence assumption,
        so u_i(S') = sum_z E[U_{i,z}(S')]  (PROVER2 equation (5.4)).
    (2) The mechanism's phase, price, winner, switch time and fallback law at z are functions of the data
        collected at z and of coins attached to z only (PROVER2 Lemma L), and every non-deviating agent plays
        the profile-local S^*, so the reward process at z is conditionally independent of everything realized at
        other profiles given the deviator's own play at z.
    (3) Hence for each z, E[U_{i,z}(S')] <= sup over profile-local policies at z, whatever the deviator
        conditions on elsewhere; and the product of the per-profile optima is itself a member of B^ctx_{i,n}.
    Therefore sup over the global class equals the sum of the per-profile suprema, and a per-profile exact
    backward induction certifies the global optimum. The arrival path is deterministic here, so the visit
    counts V_z are constants and the class is not enlarged by knowledge of the path.
    """
    t0 = time.time()
    K, focal = ctx.K, ctx.focal
    g = make_design(n, K)
    V = ctx.visits(n)
    recs = []
    tot = {k: 0.0 for k in ("base_LB", "base_UB", "V_F0", "V_FUB", "revenue_LB", "revenue_UB")}
    nontop_deltas = []
    n_trunc = 0
    bench_M2 = 0.0
    bench_honest = 0.0
    for p, V_z in zip(ctx.profiles, V):
        loc = ctx.local(p)
        bench_M2 += V_z * loc.M2
        bench_honest += V_z * loc.mu_H_star
        dlt = loc.V(focal) - loc.M[focal]
        if dlt > 1e-15:
            nontop_deltas.append(dlt)
        if V_z < K * g.L:
            r = truncated_profile(loc, n, K, V_z, g.L, focal)
            n_trunc += 1
        else:
            d = local_design(n, K, V_z)
            fb = fallback_bound(n, K, d.N)
            a = BP.solve(loc, n, list(loc.M), focal, d=d, fb=fb, log=lambda *x: None)
            rev = BP.revenue(loc, n, list(loc.M), d=d)
            r = {"V_z": V_z, "N_z": d.N, "truncated": False, "stage1_pulls_focal": d.L,
                 "base_LB": a["base_LB"], "base_UB": a["base_UB"], "V_F0": a["V_F0"], "V_FUB": a["V_FUB"],
                 "exploit_LB": a["exploit_LB"], "exploit_UB": a["exploit_UB"],
                 "revenue_LB": rev["revenue_LB"], "revenue_UB": rev["revenue_UB"],
                 "dropped_mass": a["dropped_mass"], "P_win": a["P_win"]}
        r["z"] = p["z"]
        r["M"] = list(p["M"])
        r["mu"] = list(p["mu"])
        r["focal_is_top"] = bool(loc.V(focal) <= loc.M[focal] + 1e-15)
        r["delta"] = float(max(0.0, dlt))
        for k in tot:
            tot[k] += r[k]
        recs.append(r)
    tc = theorem_constant(n, K, ctx.Q, tuple(nontop_deltas))
    exploit_LB = tot["V_F0"] - tot["base_UB"]
    exploit_UB = tot["V_FUB"] - tot["base_LB"]
    out = {"instance": ctx.id, "K": K, "Q": ctx.Q, "n": n, "focal": focal, "honest": list(ctx.honest),
           "V": V, "n_truncated_profiles": n_trunc, "profiles": recs,
           "exploit_LB": exploit_LB, "exploit_UB": exploit_UB,
           "exploit_LB_per_round": exploit_LB / n, "exploit_UB_per_round": exploit_UB / n,
           "base_LB": tot["base_LB"], "base_UB": tot["base_UB"], "V_F0": tot["V_F0"], "V_FUB": tot["V_FUB"],
           "revenue_LB": tot["revenue_LB"], "revenue_UB": tot["revenue_UB"],
           "revenue_LB_per_round": tot["revenue_LB"] / n, "revenue_UB_per_round": tot["revenue_UB"] / n,
           "benchmark_M2": bench_M2, "benchmark_M2_per_round": bench_M2 / n,
           "benchmark_honest": bench_honest, "benchmark_honest_per_round": bench_honest / n,
           "revenue_deficit_LB": bench_M2 - tot["revenue_UB"], "revenue_deficit_UB": bench_M2 - tot["revenue_LB"],
           "theorem": tc, "nontop_deltas": sorted(set(round(d, 9) for d in nontop_deltas)),
           "dropped_mass_max": max((r["dropped_mass"] for r in recs), default=0.0),
           "seconds": time.time() - t0}
    out["ratio_UB_to_constant"] = exploit_UB / tc["constant"]
    out["ratio_LB_to_constant"] = exploit_LB / tc["constant"]
    return out
