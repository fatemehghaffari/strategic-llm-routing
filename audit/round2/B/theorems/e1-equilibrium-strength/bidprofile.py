"""Exact evaluation of a phase-stationary MESP bid profile S^c and of the exact best response to it (E1).

Extends scratch/experiments/round2/exploitability/dp.py from the proposed profile S^star (every agent bids its
capacity in Stage 1) to an arbitrary feasible Stage-1 bid vector c = (c_1, ..., c_K), c_i in [0, M_i] and
c_h >= mu_h for honest h. Everything after Stage 1 is unchanged from S^star: the primary winner delivers
min{tau, M_i} (max{mu_i, min{tau, M_i}} if honest) and every agent delivers its capacity in the EXP3 fallback.

For a chosen agent i the script returns
  base_LB, base_UB   an exact bracket for u_i(n; S^c)
  V_F0, V_FUB        an exact bracket for sup over the behavioral class of u_i(n; S'_i, S^c_{-i})
  exploit_LB/UB      the resulting bracket for the deviation gain
and, separately, a bracket for the platform revenue P(n; S^c).

Exactness. (a) The deviator's one-step objective 1 + mu_i - m + m W(s,1) + (1-m) W(s,0) is affine in the target
m, so an optimal target is an endpoint of [lo_i, M_i] with lo_i = mu_i for an honest agent and 0 otherwise, and
two-action backward induction over (pull index, reward count) is exact for Stages 1 and 2 (dp.py, same argument).
(b) The fallback continuation is bracketed, not solved: F = 0 is a valid lower bound and
F_UB(H) = min{2H, (1 + mu_i - V_i) H + R_K(H)} for a top deviator, min{2H, 2 R_K(H)/delta_i} for a non-top one,
which are equations private-fallback-top and private-fallback-low of appendix_private.tex and remain valid
because the non-deviating agents deliver capacity in the fallback under S^c exactly as under S^star.
(c) The deviator's information: it knows the instance, n, K, its own history and the announced price tau; it does
not see the other bids during Stage 1. The other agents' bids are independent binomials, so the law of
(max other count, number tied there) factorizes and is computed exactly.
(d) A losing deviator gets post-bid utility only if the monitor falsely switches; that probability is computed
exactly, conditional on the realized price and on the exact identity of the non-deviating winner (winner_law),
and the resulting utility is bounded by 2 per round. No asymptotic bound is used anywhere.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import binom

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "scratch" / "experiments" / "round2"))
from common.design import design as make_design, R_K  # noqa: E402
from common import instances as I  # noqa: E402


# ===== Stage-1 bid laws

def tie_poly(L, bids, members):
    """poly[t, c] = P(max over `members` of the count <= c, with exactly t of them equal to c), t = 0..|members|.
    For an empty member set this is the deterministic array poly[0] = 1."""
    c = np.arange(L + 1)
    poly = np.zeros((len(members) + 1, L + 1))
    poly[0] = 1.0
    for j in members:
        a = binom.cdf(c - 1, L, bids[j])                           # P(count_j < c)
        b = binom.pmf(c, L, bids[j])                               # P(count_j = c)
        new = np.zeros_like(poly)
        new[0] = poly[0] * a
        new[1:] = poly[1:] * a + poly[:-1] * b
        poly = new
    return poly


def others_law(L, bids, others):
    """P(max other count = c, exactly t others tied at c) as an array [c, t-1], t = 1..len(others)."""
    return tie_poly(L, bids, others)[1:].T                         # [c, t-1]


def winner_law(L, bids, others):
    """P(max other count = c and j wins the uniform tie among the maximizers), as an array [c, j] over `others`.
    Its row sums equal P(max other count = c)."""
    out = np.zeros((L + 1, len(others)))
    for jj, j in enumerate(others):
        rest = [l for l in others if l != j]
        poly = tie_poly(L, bids, rest)                             # [t, c] over the remaining others
        share = sum(poly[t] / (t + 1.0) for t in range(poly.shape[0]))
        out[:, jj] = binom.pmf(np.arange(L + 1), L, bids[j]) * share
    return out


# ===== Stage-2 backward induction

def stage2_dp(d, tau, mu, M, lo, F_list):
    """Deviator's exact Stage-2 value V(r=0, Z=0) for each fallback continuation array F (indexed by H)."""
    N = d.N
    Fm = np.stack([np.asarray(F, dtype=float) for F in F_list])    # [nF, N+1]
    r = np.arange(N + 1)
    bound = r * tau - d.b(r)                                       # alive after pull r iff Z_r >= bound[r]
    Z = np.arange(N + 2)
    V = np.zeros((len(F_list), N + 2))
    for rr in range(N - 1, -1, -1):
        alive_next = Z >= bound[rr + 1]
        W = np.where(alive_next[None, :], V, Fm[:, N - rr - 1][:, None])
        Wz, Wz1 = W[:, :rr + 1], W[:, 1:rr + 2]
        qhi = 1 + mu - M + M * Wz1 + (1 - M) * Wz
        qlo = 1 + mu - lo + lo * Wz1 + (1 - lo) * Wz
        Vn = np.zeros_like(V)
        Vn[:, :rr + 1] = np.maximum(qhi, qlo)
        V = Vn
    return V[:, 0]


def stage2_constant(d, tau, mb):
    """Winner delivering the constant target mb: exact E[q] (primary pulls) and P(switch)."""
    N = d.N
    r = np.arange(N + 1)
    bound = r * tau - d.b(r)
    Z = np.arange(N + 2)
    p = np.zeros(N + 2)
    p[0] = 1.0
    Eq = 0.0
    Psw = 0.0
    for rr in range(N):
        Eq += p.sum()
        pn = (1 - mb) * p
        pn[1:] += mb * p[:-1]
        dead = Z < bound[rr + 1]
        Psw += pn[dead].sum()
        pn[dead] = 0.0
        p = pn
    return Eq, Psw


def stage1_dp(d, mu, M, lo, T):
    """Deviator's exact Stage-1 value with terminal payoff T indexed by its own Stage-1 reward count."""
    L = d.L
    V = np.zeros(L + 2)
    V[:L + 1] = T
    for rr in range(L - 1, -1, -1):
        Wz, Wz1 = V[:rr + 1], V[1:rr + 2]
        qhi = 1 + mu - M + M * Wz1 + (1 - M) * Wz
        qlo = 1 + mu - lo + lo * Wz1 + (1 - lo) * Wz
        Vn = np.zeros_like(V)
        Vn[:rr + 1] = np.maximum(qhi, qlo)
        V = Vn
    return V[0]


# ===== profile evaluation

def winner_target(inst, j, tau):
    mb = min(tau, inst.M[j])
    return max(inst.mu[j], mb) if inst.is_honest(j) else mb


def solve(inst, n, bids, i, mass_tol=1e-13, log=print, d=None, fb=None):
    """Exact bracket for agent i's utility under S^bids and for its best response to S^bids_{-i}.

    `d` overrides the design (the profile-local mechanism keeps the global L, s and b_n but uses the local
    primary length N = V_z - K L_n); `fb`, if given, is the fallback regret bound as an array indexed by the
    local fallback length H, replacing R_K(H) (the profile-local EXP3 is tuned once to the global horizon)."""
    t0 = time.time()
    K = inst.K
    mu, M = inst.mu[i], inst.M[i]
    honest = inst.is_honest(i)
    lo = mu if honest else 0.0
    d = d if d is not None else make_design(n, K)
    L, N = d.L, d.N
    V_i = inst.V(i)
    others = [j for j in range(K) if j != i]
    P_ct = others_law(L, bids, others)
    P_c = P_ct.sum(1)
    W_cj = winner_law(L, bids, others)                              # [c, j] exact identity of the winner
    assert np.allclose(W_cj.sum(1), P_c, atol=1e-12), "winner law does not sum to the max law"
    taus = np.maximum(0.0, np.arange(L + 1) / L - d.s)
    need = np.flatnonzero(P_c > mass_tol)
    dropped = float(P_c[P_c <= mass_tol].sum())
    H = np.arange(N + 1)
    Rfb = np.asarray(fb, dtype=float) if fb is not None else np.array([R_K(K, h) for h in H])
    assert Rfb.shape == (N + 1,)
    if V_i <= M + 1e-15:
        F_ub = np.minimum(2.0 * H, (1 + mu - V_i) * H + Rfb)
    else:
        F_ub = np.minimum(2.0 * H, 2.0 * Rfb / (V_i - M))
    F_ub[0] = 0.0
    F_0 = np.zeros(N + 1)

    V2_f0 = np.zeros(L + 1)      # deviator's Stage-2 value, zero fallback continuation (lower bound)
    V2_fub = np.zeros(L + 1)     # deviator's Stage-2 value, appendix fallback upper bound
    B2_lb = np.zeros(L + 1)      # agent i's baseline Stage-2 utility as winner, lower bound
    B2_ub = np.zeros(L + 1)
    loser_ub = np.zeros(L + 1)   # upper bound on a loser's post-bid utility at this price
    cache = {}
    for c in need:
        tau = float(taus[c])
        key = round(tau, 12)
        if key not in cache:
            vals = stage2_dp(d, tau, mu, M, lo, [F_0, F_ub])
            mb = winner_target(inst, i, tau)
            Eq, Psw = stage2_constant(d, tau, mb)
            psw_each = np.array([stage2_constant(d, tau, winner_target(inst, j, tau))[1] for j in others])
            cache[key] = (vals[0], vals[1], (1 + mu - mb) * Eq,
                          (1 + mu - mb) * Eq + 2 * N * Psw, psw_each)
        V2_f0[c], V2_fub[c], B2_lb[c], B2_ub[c], psw_each = cache[key]
        # exact conditional switch probability of the actual non-deviating winner at this price
        loser_ub[c] = 2 * N * float(W_cj[c] @ psw_each) / max(P_c[c], 1e-300)
    log(f"  {len(cache)} distinct prices, {time.time() - t0:.1f}s")

    z = np.arange(L + 1)
    tie_w = (P_ct / (np.arange(1, K)[None, :] + 1)).sum(1)          # P(max other = z, tie resolved for i)
    cum = np.concatenate(([0.0], np.cumsum(P_c)))                   # cum[z] = P(max other < z)
    Pwin = cum[:L + 1] + tie_w

    def terminal(V2, loser_term):
        cs = np.concatenate(([0.0], np.cumsum(P_c * V2)))
        lo_c = np.concatenate(([0.0], np.cumsum(P_c * loser_term)))
        # losing mass at own count z: others' max c >= z, minus the share of the tie won
        tot_loser = (loser_term * P_c).sum()
        return cs[:L + 1] + tie_w * V2 + (tot_loser - lo_c[:L + 1] - tie_w * loser_term)

    T_f0 = terminal(V2_f0, np.zeros(L + 1))
    T_fub = terminal(V2_fub, loser_ub) + 2.0 * n * dropped
    V_F0 = stage1_dp(d, mu, M, lo, T_f0)
    V_FUB = stage1_dp(d, mu, M, lo, T_fub)

    pz = binom.pmf(z, L, bids[i])
    win_at = np.zeros((L + 1, L + 1))                               # [own z, other max c] winning mass
    for zz in range(L + 1):
        win_at[zz, :zz] = P_c[:zz]
        win_at[zz, zz] = tie_w[zz]
    lose_at = np.tile(P_c, (L + 1, 1)) - win_at
    base_s1 = L * (1 + mu - bids[i])
    base_LB = base_s1 + float(pz @ (win_at @ B2_lb))
    base_UB = base_s1 + float(pz @ (win_at @ B2_ub)) + float(pz @ (lose_at @ loser_ub)) + 2.0 * n * dropped

    out = {"instance": inst.id, "alias": inst.alias, "n": n, "K": K, "agent": i, "bids": list(bids),
           "honest_agent": honest, "L": L, "N": N, "s_n": d.s, "M_i": M, "mu_i": mu, "V_i": V_i,
           "P_win": float(pz @ Pwin), "dropped_mass": dropped,
           "base_LB": base_LB, "base_UB": base_UB, "V_F0": float(V_F0), "V_FUB": float(V_FUB),
           "exploit_LB": float(V_F0 - base_UB), "exploit_UB": float(V_FUB - base_LB),
           "L_n": L, "theorem_constant_top": float(L + 2 * float(d.b(n)) + R_K(K, n)),
           "seconds": time.time() - t0}
    out["exploit_LB_per_round"] = out["exploit_LB"] / n
    out["exploit_UB_per_round"] = out["exploit_UB"] / n
    return out


def revenue(inst, n, bids, mass_tol=1e-13, d=None):
    """Exact bracket for P(n; S^bids). Stage-1 revenue is exact; Stage-2 uses E[q] times the winner's target and
    brackets the fallback contribution by [0, N] times the switch probability."""
    K = inst.K
    d = d if d is not None else make_design(n, K)
    L, N = d.L, d.N
    taus = np.maximum(0.0, np.arange(L + 1) / L - d.s)
    lo = L * float(np.sum(bids))
    hi = lo
    cache = {}
    for w in range(K):
        others = [j for j in range(K) if j != w]
        P_ct = others_law(L, bids, others)
        P_c = P_ct.sum(1)
        tie_w = (P_ct / (np.arange(1, K)[None, :] + 1)).sum(1)
        pz = binom.pmf(np.arange(L + 1), L, bids[w])
        cum = np.concatenate(([0.0], np.cumsum(P_c)))
        # P(w wins and second order statistic count = c)
        mass = np.zeros(L + 1)
        for c in range(L + 1):
            if P_c[c] <= mass_tol and tie_w[c] <= mass_tol:
                continue
            mass[c] = P_c[c] * pz[c + 1:].sum() + tie_w[c] * pz[c]
        for c in np.flatnonzero(mass > mass_tol):
            tau = float(taus[c])
            mb = winner_target(inst, w, tau)
            key = (round(tau, 12), round(mb, 12))
            if key not in cache:
                cache[key] = stage2_constant(d, tau, mb)
            Eq, Psw = cache[key]
            lo += mass[c] * mb * Eq
            hi += mass[c] * (mb * Eq + N * Psw)
        del cum
    return {"revenue_LB": float(lo), "revenue_UB": float(hi), "revenue_LB_per_round": float(lo) / n,
            "revenue_UB_per_round": float(hi) / n}


# ===== driver

def parse_bids(spec, inst):
    """'M' = capacity vector; otherwise a comma-separated list, where 'M' and 'mu' name the agent's own values."""
    if spec == "M":
        return list(inst.M)
    out = []
    for k, tok in enumerate(spec.split(",")):
        tok = tok.strip()
        out.append(inst.M[k] if tok == "M" else inst.mu[k] if tok == "mu" else float(tok))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--bids", required=True, help="'M' or a comma-separated Stage-1 bid vector")
    ap.add_argument("--agents", type=int, nargs="*", default=None)
    ap.add_argument("--tag", default="")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    inst = I.get(a.instance)
    bids = parse_bids(a.bids, inst)
    for k in range(inst.K):
        assert 0.0 <= bids[k] <= inst.M[k] + 1e-12, f"infeasible bid for agent {k}"
        if inst.is_honest(k):
            assert bids[k] >= inst.mu[k] - 1e-12, f"honest agent {k} may not bid below mu"
    agents = a.agents if a.agents else list(range(inst.K))
    for n in a.n:
        rec = {"instance": inst.id, "alias": inst.alias, "n": n, "bids": bids, "tag": a.tag,
               "mu": list(inst.mu), "M": list(inst.M), "honest": list(inst.honest),
               "mu_H_star": inst.mu_H_star, "M_2": inst.M2, "M_top": inst.M_top}
        rec["revenue"] = revenue(inst, n, bids)
        rec["agents"] = {}
        for i in agents:
            r = solve(inst, n, bids, i)
            rec["agents"][str(i)] = r
            print(f"{inst.alias} n={n} bids={bids} agent {i}: exploit in "
                  f"[{r['exploit_LB']:.2f}, {r['exploit_UB']:.2f}] "
                  f"([{r['exploit_LB_per_round']:.5f}, {r['exploit_UB_per_round']:.5f}] per round), "
                  f"L_n={r['L_n']}, thm const {r['theorem_constant_top']:.1f}, {r['seconds']:.1f}s")
        print(f"  revenue per round in [{rec['revenue']['revenue_LB_per_round']:.5f}, "
              f"{rec['revenue']['revenue_UB_per_round']:.5f}]  (M_(2)={inst.M2}, mu_H*={inst.mu_H_star})")
        stem = out / f"bp_{inst.alias}_{a.tag or 'run'}_{n}.json"
        stem.write_text(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
