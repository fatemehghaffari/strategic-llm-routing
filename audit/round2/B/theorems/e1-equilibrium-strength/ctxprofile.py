"""Exact evaluation of a profile-local bid array for PL-MESP, the contextual mechanism of
audit/round2/B/theorems/c2-local-mesp/ (PROVER2 Section 2 mechanism, PROVER1 calibration, which is the
adversary's Section 9.4 recommendation).

PL-MESP runs one independent scalar MESP per exact context profile, with all tuning constants taken from the
GLOBAL horizon n and the local phases driven by the local visit count V_z. Utilities and revenue decompose
additively over profiles (PROVER2 equation (5.4)), and the mechanism's state at z is a function of data
collected at z only (PROVER2 Lemma L), so the exact per-profile computation of bidprofile.py applies verbatim
once three substitutions are made:

  L      = L_n(n, K)                      global bidding length, per agent, per profile
  s      = s_n(n, K)                      global bid radius, sqrt(log(2 K n^4)/(2 L_n))
  b_n(r) = sqrt(r log(2 n^4)/2)           global monitor boundary
  N      = V_z - K L_n                    LOCAL primary length at z
  fallback regret bound at local length H:  min{ 2H, 2 gamma_n H + K log K / gamma_n, R_K(n) }
                                          with gamma_n = min{1/2, sqrt(K log K / n)}, the single local EXP3
                                          tuned once to n (PROVER2 Lemma F, prefix form; adversary Section 9.1)

Everything else, including the exactness of the two-action backward induction and the bracketing of the
fallback continuation, is as documented in bidprofile.py. The arrival path is conditioned on throughout, as in
PROVER2 Convention F-A, so the visit counts V_z are deterministic inputs here.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO / "scratch" / "experiments" / "round2"))
sys.path.insert(0, str(HERE))
from common.design import design as make_design, Design, R_K  # noqa: E402
import bidprofile as BP  # noqa: E402


class CtxInstance:
    """A finite set of exact profiles with per-profile primitives and visit shares."""

    def __init__(self, raw):
        self.id = raw["id"]
        self.K = int(raw["K"])
        self.honest = tuple(raw["honest"])
        self.profiles = raw["profiles"]
        assert abs(sum(p["share"] for p in self.profiles) - 1.0) < 1e-12, "shares must sum to one"
        for p in self.profiles:
            assert len(p["mu"]) == len(p["M"]) == self.K
            for i in range(self.K):
                assert 0.0 <= p["mu"][i] <= p["M"][i] <= 1.0

    def local(self, p):
        """A scalar-instance view of one profile, for reuse of bidprofile.py."""
        return BP.I.Instance(id=f"{self.id}/{p['z']}", alias=p["z"], mu=tuple(p["mu"]), M=tuple(p["M"]),
                             honest=self.honest, focal=0, index=0)


def load(name, path=None):
    raw = json.loads((path or HERE / "ctxinstances.json").read_text())["instances"]
    for r in raw:
        if r["id"] == name:
            return CtxInstance(r)
    raise KeyError(name)


def local_design(n, K, V_z):
    """Global constants, local primary length."""
    g = make_design(n, K)
    N = V_z - K * g.L
    if N < 0:
        raise ValueError(f"profile with V_z = {V_z} never finishes Stage 1 (K L_n = {K * g.L})")
    return Design(n=n, K=K, L=g.L, N=N, s=g.s, log2n4=g.log2n4)


def fallback_bound(n, K, N):
    """Prefix bound for the single local EXP3 tuned to the global horizon, as an array indexed by H = 0..N."""
    H = np.arange(N + 1, dtype=float)
    gamma = min(0.5, math.sqrt(K * math.log(K) / n)) if K > 1 else 0.0
    loss = 2.0 * gamma * H + (K * math.log(K) / gamma if gamma > 0 else 0.0)
    return np.minimum(loss, R_K(K, n))


def solve_profile(ctx, n, V_z, p, bids_z, i):
    """Exact bracket for agent i's utility at profile p and for its best response there, everything else fixed."""
    inst = ctx.local(p)
    d = local_design(n, ctx.K, V_z)
    return BP.solve(inst, n, bids_z, i, d=d, fb=fallback_bound(n, ctx.K, d.N))


def run(ctx, n, bid_array, agents=None, log=print):
    """bid_array[j][i] = agent i's constant Stage-1 target at the j-th profile."""
    K = ctx.K
    agents = agents if agents is not None else list(range(K))
    shares = [p["share"] for p in ctx.profiles]
    V = [int(round(s * n)) for s in shares]
    V[-1] = n - sum(V[:-1])
    out = {"instance": ctx.id, "n": n, "K": K, "honest": list(ctx.honest), "V": V, "bids": bid_array,
           "profiles": [], "totals": {}}
    tot_rev_lo = tot_rev_hi = 0.0
    tot = {i: {"base_LB": 0.0, "base_UB": 0.0, "V_F0": 0.0, "V_FUB": 0.0} for i in agents}
    for j, p in enumerate(ctx.profiles):
        inst = ctx.local(p)
        d = local_design(n, K, V[j])
        fb = fallback_bound(n, K, d.N)
        rec = {"z": p["z"], "V_z": V[j], "N_z": d.N, "L_n": d.L, "s_n": d.s, "bids": bid_array[j],
               "M": list(p["M"]), "mu": list(p["mu"]), "agents": {}}
        r = BP.revenue(inst, n, bid_array[j], d=d)
        rec["revenue"] = r
        tot_rev_lo += r["revenue_LB"]; tot_rev_hi += r["revenue_UB"]
        for i in agents:
            a = BP.solve(inst, n, bid_array[j], i, d=d, fb=fb, log=lambda *x: None)
            rec["agents"][str(i)] = a
            for k in tot[i]:
                tot[i][k] += a[k]
        log(f"  {p['z']}: V_z={V[j]} N_z={d.N} revenue/visit in "
            f"[{r['revenue_LB'] / max(V[j], 1):.4f}, {r['revenue_UB'] / max(V[j], 1):.4f}]")
        out["profiles"].append(rec)
    out["totals"] = {"revenue_LB": tot_rev_lo, "revenue_UB": tot_rev_hi,
                     "revenue_LB_per_round": tot_rev_lo / n, "revenue_UB_per_round": tot_rev_hi / n,
                     "agents": {str(i): {**tot[i],
                                         "exploit_LB": tot[i]["V_F0"] - tot[i]["base_UB"],
                                         "exploit_UB": tot[i]["V_FUB"] - tot[i]["base_LB"],
                                         "exploit_LB_per_round": (tot[i]["V_F0"] - tot[i]["base_UB"]) / n,
                                         "exploit_UB_per_round": (tot[i]["V_FUB"] - tot[i]["base_LB"]) / n}
                                for i in agents}}
    return out


def parse_array(spec, ctx):
    """'M' for capacity everywhere, else profiles separated by ';' and bids by ',' ('M' and 'mu' allowed)."""
    if spec == "M":
        return [list(p["M"]) for p in ctx.profiles]
    rows = spec.split(";")
    assert len(rows) == len(ctx.profiles), "one bid vector per profile"
    out = []
    for p, row in zip(ctx.profiles, rows):
        if row.strip() == "M":
            out.append(list(p["M"]))
            continue
        if row.strip() == "mu":
            out.append(list(p["mu"]))
            continue
        vec = []
        for k, tok in enumerate(row.split(",")):
            tok = tok.strip()
            vec.append(p["M"][k] if tok == "M" else p["mu"][k] if tok == "mu" else float(tok))
        out.append(vec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--bids", required=True)
    ap.add_argument("--tag", default="run")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ctx = load(a.instance)
    outdir = Path(a.out); outdir.mkdir(parents=True, exist_ok=True)
    for n in a.n:
        bid_array = parse_array(a.bids, ctx)
        for j, p in enumerate(ctx.profiles):
            for i in range(ctx.K):
                assert 0.0 <= bid_array[j][i] <= p["M"][i] + 1e-12, "infeasible bid"
                if i in ctx.honest:
                    assert bid_array[j][i] >= p["mu"][i] - 1e-12, "honest agent may not bid below mu"
        t0 = time.time()
        rec = run(ctx, n, bid_array)
        rec["seconds"] = time.time() - t0
        rec["tag"] = a.tag
        t = rec["totals"]
        print(f"{ctx.id} n={n} tag={a.tag}: revenue/round in "
              f"[{t['revenue_LB_per_round']:.4f}, {t['revenue_UB_per_round']:.4f}]")
        for i, v in t["agents"].items():
            print(f"    agent {i}: total exploit in [{v['exploit_LB']:.1f}, {v['exploit_UB']:.1f}] "
                  f"([{v['exploit_LB_per_round']:.5f}, {v['exploit_UB_per_round']:.5f}] per round)")
        print(f"    {rec['seconds']:.1f}s")
        (outdir / f"ctx_{ctx.id}_{a.tag}_{n}.json").write_text(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
