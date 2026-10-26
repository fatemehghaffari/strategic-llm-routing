"""Grid search over a parametric deviation class against PL-MESP, as a cross-check on the certified bounds.

The class searched: shade the Stage-1 target by `delta` at every profile, and in Stage 2 deliver
`tau - c / sqrt(r)` on local primary pull `r`, the fixed-schedule boundary rider of `common/mechanism.py`.
Both channels may be used together. The grid is a product of `delta` and `c` values.

Every value reported here is a LOWER bound on exploitability for the class searched. It is not an upper bound,
it is not a best response, and it is not evidence of equilibrium. Its only role is the cross-check that no
searched policy exceeds the certified upper bound, which is the check that would reveal an error in the
backward induction or in the bracketing.
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from pathlib import Path

import numpy as np

R2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R2))

from common import seeds as S  # noqa: E402
from common.mechanism import Policy  # noqa: E402
from common.stats import t_interval  # noqa: E402
from ctx_local.plmesp_exact import family, solve_instance  # noqa: E402
from ctx_local import ctxmech as CM  # noqa: E402


class UnderbidRide(Policy):
    """Shade the Stage-1 target by `delta`; ride the monitor boundary at scale `c` in Stage 2."""
    primary_array = True

    def __init__(self, delta: float, c: float):
        self.delta = delta
        self.c = c
        self.name = f"ubr_d{delta:g}_c{c:g}"

    def bid_target(self, ctx, r, z):
        return ctx.M - self.delta

    def primary_target(self, ctx, r, Z, tau):
        return tau - self.c / math.sqrt(max(r, 1))


def run_cell(fam, Q, n, reps, deltas, cs, phase="pilot"):
    ctx = family(fam, Q)
    ex = solve_instance(ctx, n)
    base = []
    grid = {}
    for rep in range(reps):
        _, _, g = S.trial_streams("contextual_incentives", phase, 5555 + Q, n, rep)
        base.append(CM.run_episode(ctx, n, "pl_mesp", "profile", ctx.focal, g)["focal_utility"])
    for delta in deltas:
        for c in cs:
            pol = CM.PerProfile(UnderbidRide(delta, c), f"ubr_d{delta:g}_c{c:g}")
            vals = []
            for rep in range(reps):
                _, _, g = S.trial_streams("contextual_incentives", phase, 5555 + Q, n, rep)
                tapes = CM.make_tapes(ctx, n, g)
                vals.append(CM.simulate_local(ctx, n, CM.CTX_VARIANTS["pl_mesp"], pol, ctx.focal,
                                              tapes)["focal_utility"])
            gain = np.array(vals) - np.array(base)
            m, lo, hi, _ = t_interval(gain)
            vm, vlo, vhi, _ = t_interval(vals)
            grid[(delta, c)] = (m, lo, hi, vm, vlo, vhi)
    best = max(grid.items(), key=lambda kv: kv[1][0])
    return ex, grid, best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True)
    ap.add_argument("--Q", type=int, nargs="+", required=True)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    # delta is subtracted from the agent's capacity and the result is clipped to its feasible set, so
    # delta = 1.0 is Stage-1 shading to the floor, which is the certified optimum in the cells where the
    # optimum is to lose the auction.
    deltas = [0.0, 0.05, 0.10, 0.125, 0.15, 0.20, 0.30, 0.50, 0.70, 1.00]
    cs = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5]
    rows = []
    for n in a.n:
        for Q in a.Q:
            t0 = time.time()
            ex, grid, best = run_cell(a.family, Q, n, a.reps, deltas, cs)
            (d, c), (m, lo, hi, vm, vlo, vhi) = best
            # The check that is exact on both sides compares the searched VALUE with the certified upper
            # bound on the value, V_FUB. Comparing a simulated GAIN with the certified gain interval is not
            # valid: it subtracts a noisy baseline from an exact bound.
            exceeds = int(vm > ex["V_FUB"] + 1e-9)
            print(f"{a.family} Q={Q} n={n}: best searched gain {m:.2f} [{lo:.2f}, {hi:.2f}] at "
                  f"delta={d:g}, c={c:g}; certified gain interval "
                  f"[{ex['exploit_LB']:.2f}, {ex['exploit_UB']:.2f}]; "
                  f"fraction of the certified lower bound "
                  f"{m / ex['exploit_LB'] if ex['exploit_LB'] > 0 else float('nan'):.3f}; "
                  f"searched VALUE {vm:.2f} against V_FUB {ex['V_FUB']:.2f}; "
                  f"value exceeds the certified upper bound: {bool(exceeds)}; {time.time() - t0:.0f}s",
                  flush=True)
            for (dd, cc), (mm, llo, hhi, vv, vvlo, vvhi) in sorted(grid.items()):
                rows.append({"family": a.family, "Q": Q, "n": n, "reps": a.reps, "delta": dd, "c": cc,
                             "searched_gain_mean": mm, "searched_gain_lo": llo, "searched_gain_hi": hhi,
                             "searched_value_mean": vv, "searched_value_lo": vvlo, "searched_value_hi": vvhi,
                             "certified_LB": ex["exploit_LB"], "certified_UB": ex["exploit_UB"],
                             "V_FUB": ex["V_FUB"],
                             "value_exceeds_V_FUB": int(vv > ex["V_FUB"] + 1e-9)})
    p = out / f"search_{a.family}{('_' + a.tag) if a.tag else ''}.csv"
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {p}")


if __name__ == "__main__":
    main()
