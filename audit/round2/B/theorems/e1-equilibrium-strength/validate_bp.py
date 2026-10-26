"""Monte Carlo cross-check of bidprofile.py against the round-2 episode simulator.

Runs the shared MESP simulator (scratch/experiments/round2/common/mechanism.py, variant "mesp") with every
agent playing S^star except for a constant Stage-1 target c_i, and compares the simulated mean utility of each
agent and the simulated mean platform reward with the exact brackets computed by bidprofile.py. Seeds come from
common/seeds.py with the "exploitability" suite and the "analysis" phase, so they do not collide with the
suite's own runs.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
import numpy as np

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "scratch" / "experiments" / "round2"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import instances as I, mechanism as M, seeds as S  # noqa: E402
import bidprofile as BP  # noqa: E402


class ConstantBid(M.Policy):
    """S^star with the Stage-1 target replaced by a constant (clipped to feasibility by the simulator)."""
    def __init__(self, c):
        self.c = float(c); self.name = f"bid_{c:.3f}"

    def bid_target(self, ctx, r, z):
        return self.c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--bids", required=True)
    ap.add_argument("--reps", type=int, default=20000)
    a = ap.parse_args()
    inst = I.get(a.instance)
    bids = BP.parse_bids(a.bids, inst)
    pols = [ConstantBid(bids[i]) for i in range(inst.K)]
    var = M.VARIANTS["mesp"]
    U = np.zeros((a.reps, inst.K)); R = np.zeros(a.reps); wins = np.zeros(inst.K)
    for rep in range(a.reps):
        gens = S.trial_streams("exploitability", "analysis", inst.index, a.n, rep)[2]
        out = M.episode(inst, a.n, var, pols, gens)
        for i in range(inst.K):
            U[rep, i] = out[f"utility_{i}"]
        R[rep] = out["platform_reward"]; wins[out["winner"]] += 1
    print(f"{inst.alias} n={a.n} bids={bids} reps={a.reps}  win shares {wins / a.reps}")
    ex = {i: BP.solve(inst, a.n, bids, i, log=lambda *x: None) for i in range(inst.K)}
    rev = BP.revenue(inst, a.n, bids)
    ok = True
    for i in range(inst.K):
        m, se = U[:, i].mean(), U[:, i].std(ddof=1) / math.sqrt(a.reps)
        lo, hi = ex[i]["base_LB"], ex[i]["base_UB"]
        tol = 3 * se + 1e-6 * max(1.0, abs(m))          # se = 0 when the agent's utility is deterministic
        inside = lo - tol <= m <= hi + tol
        z = 0.0 if inside else (m - hi) / max(se, 1e-12) if m > hi else (m - lo) / max(se, 1e-12)
        ok &= inside
        print(f"  agent {i}: simulated {m:9.2f} +- {1.96 * se:6.2f}   exact [{lo:9.2f}, {hi:9.2f}]   "
              f"{'OK' if inside else f'MISMATCH z={z:.2f}'}")
    m, se = R.mean(), R.std(ddof=1) / math.sqrt(a.reps)
    lo, hi = rev["revenue_LB"], rev["revenue_UB"]
    tol = 3 * se + 1e-6 * max(1.0, abs(m))
    inside = lo - tol <= m <= hi + tol
    z = 0.0 if inside else (m - hi) / max(se, 1e-12) if m > hi else (m - lo) / max(se, 1e-12)
    ok &= inside
    print(f"  revenue: simulated {m:9.2f} +- {1.96 * se:6.2f}   exact [{lo:9.2f}, {hi:9.2f}]   "
          f"{'OK' if inside else f'MISMATCH z={z:.2f}'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
