"""Validation of the exact PL-MESP computation against the simulator and against the scalar package.

Five checks, all reported with their numbers whether they pass or fail:

  V1  Q = 1 against exploitability/dp.py. PL-MESP on a one-profile instance IS the scalar mechanism except
      that its Stage-3 EXP3 is tuned to the global n rather than to the realised fallback length H, and
      except that the losing branch is bounded exactly here and by a closed-form union bound in dp.py. So
      exploit_LB must agree to within the losing-branch term and exploit_UB must differ only through the
      fallback bound. Both differences are printed.
  V2  The simulator under the proposed profile against the exact baseline bracket [base_LB, base_UB] and the
      exact revenue bracket. The simulated mean must lie inside the bracket up to Monte Carlo error.
  V3  No simulated deviation may exceed the certified upper bound V_FUB. This is the check that would reveal
      an error in the backward induction or in the bracketing.
  V4  Truncated profiles: the closed form against the simulator under Stage-1 shading to the floor.
  V5  At Q = 1 the pooled-statistics rung pl_shared must coincide with pl_mesp, since there is one profile.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

R2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R2))
from common import instances as I, seeds as S  # noqa: E402
from common.design import design as make_design  # noqa: E402
from common.stats import t_interval  # noqa: E402
from ctx_local.plmesp_exact import family, solve_instance  # noqa: E402
from ctx_local import ctxmech as CM  # noqa: E402
sys.path.insert(0, str(R2 / "exploitability"))
import dp as DP  # noqa: E402


def v1(n, K=3):
    print(f"\nV1  Q = 1 against exploitability/dp.py, n = {n}")
    for fam, alias in (("replicated_unique_top", "unique_top"), ("replicated_tied_top", "tied_top")):
        ctx = family(fam, 1)
        a = solve_instance(ctx, n)
        b, _ = DP.solve(I.get(alias), n, log=lambda *x: None)
        print(f"  {alias:12s} PL-MESP Q=1 [{a['exploit_LB']:.4f}, {a['exploit_UB']:.4f}]   "
              f"dp.py [{b['exploit_LB']:.4f}, {b['exploit_UB_I0']:.4f}]   "
              f"dLB {a['exploit_LB'] - b['exploit_LB']:+.4f}  dUB {a['exploit_UB'] - b['exploit_UB_I0']:+.4f}")
        print(f"               base PL [{a['base_LB']:.4f}, {a['base_UB']:.4f}]  base dp [{b['base_LB']:.4f}, "
              f"{b['base_UB']:.4f}];  V_F0 {a['V_F0']:.4f} vs {b['V_I0_F0']:.4f} (must agree to 1e-6); "
              f"V_FUB {a['V_FUB']:.4f} vs {b['V_I0_FUB']:.4f} (fallback tuned to n vs to H)")


def v2_v3_v5(fam, Q, n, reps=200, phase="pilot"):
    print(f"\nV2/V3/V5  simulator against the exact brackets: {fam} Q={Q} n={n}, {reps} replicates")
    ctx = family(fam, Q)
    ex = solve_instance(ctx, n)
    behaviours = ["profile", "bid_zero", "underbid_15", "bait_switch", "boundary_ride", "primary_shade_15",
                  "trigger_fallback_shade", "primary_own_capacity", "cross_profile_freeride", "sabotage_all"]
    res = {b: [] for b in behaviours}
    rev = []
    shared = []
    for rep in range(reps):
        for b in behaviours:
            _, _, g = S.trial_streams("contextual_incentives", phase, 7777 + Q, n, rep)
            r = CM.run_episode(ctx, n, "pl_mesp", b, ctx.focal, g)
            res[b].append((r["focal_utility"], r["platform_reward"]))
            if b == "profile":
                rev.append(r["platform_reward"])
        if Q == 1:
            _, _, g = S.trial_streams("contextual_incentives", phase, 7777 + Q, n, rep)
            shared.append(CM.run_episode(ctx, n, "pl_shared", "profile", ctx.focal, g)["focal_utility"])
    def overlaps(lo, hi, a, b):
        """The 95 percent interval of the simulated mean meets the exact bracket."""
        return not (hi < a - 1e-9 or lo > b + 1e-9)

    m, lo, hi, _ = t_interval([u for u, _ in res["profile"]])
    print(f"  V2 baseline utility: simulated {m:.2f} [{lo:.2f}, {hi:.2f}] against exact bracket "
          f"[{ex['base_LB']:.2f}, {ex['base_UB']:.2f}]  -> "
          f"{'CONSISTENT' if overlaps(lo, hi, ex['base_LB'], ex['base_UB']) else 'INCONSISTENT'}")
    rm, rlo, rhi, _ = t_interval(rev)
    print(f"  V2 revenue:          simulated {rm:.2f} [{rlo:.2f}, {rhi:.2f}] against exact bracket "
          f"[{ex['revenue_LB']:.2f}, {ex['revenue_UB']:.2f}]  -> "
          f"{'CONSISTENT' if overlaps(rlo, rhi, ex['revenue_LB'], ex['revenue_UB']) else 'INCONSISTENT'}")
    print(f"  V3 certified upper bound on the deviator's value V_FUB = {ex['V_FUB']:.2f}; "
          f"certified interval on the gain [{ex['exploit_LB']:.2f}, {ex['exploit_UB']:.2f}]")
    worst = None
    for b in behaviours:
        u = np.array([x for x, _ in res[b]])
        mm, llo, hhi, _ = t_interval(u)
        flag = "EXCEEDS UB" if mm > ex["V_FUB"] + 1e-9 else "ok"
        gain = mm - m
        print(f"    {b:26s} value {mm:10.2f} [{llo:9.2f}, {hhi:9.2f}]  gain {gain:9.2f} "
              f"({gain / n:+.6f}/round)  {flag}")
        if worst is None or gain > worst[1]:
            worst = (b, gain)
    best_value = max(float(np.mean([x for x, _ in res[b]])) for b in behaviours)
    print(f"  V3 the comparison that is exact on both sides: the largest simulated deviator VALUE is "
          f"{best_value:.2f} against the certified upper bound on the value V_FUB = {ex['V_FUB']:.2f}  -> "
          f"{'NO POLICY EXCEEDS THE CERTIFIED UPPER BOUND' if best_value <= ex['V_FUB'] + 1e-9 else 'EXCEEDS'}")
    print(f"  V3 best simulated deviation by gain against the SIMULATED baseline: {worst[0]} at "
          f"{worst[1]:.2f}. That gain mixes an exact upper bound with a noisy baseline, so it is not the "
          f"right quantity to compare with the certified interval; the value comparison above is. A searched "
          f"or hand-picked deviation is a LOWER bound only.")
    if Q == 1:
        d = np.array(shared) - np.array([u for u, _ in res["profile"]])
        print(f"  V5 pl_shared minus pl_mesp at Q = 1: max |difference| = {np.abs(d).max():.10f} "
              f"({'identical' if np.abs(d).max() < 1e-9 else 'NOT IDENTICAL'})")


def v4(fam, Q, n, reps=100, phase="pilot"):
    ctx = family(fam, Q)
    ex = solve_instance(ctx, n)
    if ex["n_truncated_profiles"] != ctx.Q:
        print(f"\nV4  {fam} Q={Q} n={n}: {ex['n_truncated_profiles']} of {ctx.Q} profiles truncated; the "
              f"closed form equals the optimum only when EVERY profile is truncated, so this cell is not a "
              f"valid comparison and is skipped")
        return
    print(f"\nV4  truncated profiles ({ex['n_truncated_profiles']} of {Q}) at {fam} Q={Q} n={n}")
    u = []
    for rep in range(reps):
        _, _, g = S.trial_streams("contextual_incentives", phase, 8888 + Q, n, rep)
        u.append(CM.run_episode(ctx, n, "pl_mesp", "bid_zero", ctx.focal, g)["focal_utility"])
    m, lo, hi, _ = t_interval(u)
    print(f"  simulated value of Stage-1 shading to the floor {m:.4f} [{lo:.4f}, {hi:.4f}] against the exact "
          f"closed form V_F0 = {ex['V_F0']:.4f}  -> "
          f"{'INSIDE' if lo - 1e-9 <= ex['V_F0'] <= hi + 1e-9 else 'OUTSIDE'} "
          f"(the closed form is deterministic when every profile is truncated)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8000)
    ap.add_argument("--reps", type=int, default=200)
    a = ap.parse_args()
    v1(a.n)
    for fam, Q, n in (("replicated_unique_top", 1, a.n), ("replicated_unique_top", 2, a.n),
                      ("rotating_top", 2, a.n), ("replicated_tied_top", 2, a.n)):
        v2_v3_v5(fam, Q, n, reps=a.reps)
    v4("replicated_unique_top", 5, a.n)
    v4("unbalanced_unique_top", 4, a.n)


if __name__ == "__main__":
    main()
