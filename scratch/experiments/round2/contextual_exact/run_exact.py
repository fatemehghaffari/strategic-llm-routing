"""Cross-check (i) against contextual_incentives/summary.csv and the exact exploitability table (both grids)."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contextual_exact import exact_etc as E  # noqa: E402

REPO = Path(__file__).resolve().parents[4]
SUMMARY = REPO / "scratch/experiments/final/contextual_incentives/summary.csv"
DEVS = ["constant", "cell-aligned", "grid-misaligned", "near-boundary", "random-fixed"]


def retained_random_maps(n, reps=240):
    """Reproduce the random maps of the retained suite (seed and draw order of contextual_incentives/run.py one())."""
    maps = []
    for rep in range(reps):
        seed = 86000000 + n * 1000 + 4 * 100000 + rep
        rng = np.random.default_rng(seed); rng.random((n, 3)); rng.random((n, 3))
        maps.append(rng.choice([0., .06, .12, .18], size=8, replace=True))
    return maps


def crosscheck(out):
    rows = list(csv.DictReader(SUMMARY.open())); res = []
    for n in [2000, 8000, 32000]:
        m = E.CellModel(E.env_current(), n, 0, grid="equal"); base = m.baseline()  # reproduces the retained suite
        for dev in DEVS:
            r = next(x for x in rows if int(x["n"]) == n and x["deviation"] == dev)
            if dev == "random-fixed":
                vals = [m.utility_of_map(E.hand_picked_cell_avg(m, dev, rm)) for rm in retained_random_maps(n)]
                exact = float(np.mean(vals)) - base
            else:
                exact = m.utility_of_map(E.hand_picked_cell_avg(m, dev)) - base
            mean = float(r["utility_gain_mean"]); lo = float(r["utility_gain_lo"]); hi = float(r["utility_gain_hi"])
            se = (hi - lo) / (2 * 1.96); z = (exact - mean) / se
            res.append({"n": n, "deviation": dev, "exact_gain": exact, "sim_mean": mean, "sim_lo": lo, "sim_hi": hi, "inside": bool(lo <= exact <= hi), "z": z})
            print(f"n={n:6d} {dev:16s} exact {exact:9.2f}  sim {mean:9.2f} [{lo:.2f}, {hi:.2f}]  inside={lo <= exact <= hi}  z={z:+.2f}")
    (out / "crosscheck_summary.json").write_text(json.dumps(res, indent=1))
    return res


def table(out, horizons):
    rows = []
    for env_name in ["current", "separator"]:
        env = E.ENVS[env_name]()
        focals = [0] if env_name == "current" else [0, 2]
        for grid in ["equal", "equalized", "dyadic"]:
            for i in focals:
                for n in horizons:
                    t0 = time.time(); mg = 2001 if n <= 128000 else 801
                    m = E.CellModel(env, n, i, grid=grid, m_grid=mg)
                    base = m.baseline(); full, arg, err = m.sup_full(refine=2); own, _ = m.sup_own(); stress = m.stress_explore_then_shade()
                    row = {"env": env_name, "focal": i, "grid": grid, "n": n, "h": m.h, "q": m.q, "cells": len(m.cells),
                           "Kq_J_over_n": env.K * m.q * len(m.cells) / n, "thin_cells": sum(1 for c in m.cells if m.exploit[c] < 1.0),
                           "exploration_share": m.exploration_share(), "baseline": base, "sup_full": full, "sup_own": own,
                           "exploit_full": full - base, "exploit_full_per_round": (full - base) / n,
                           "exploit_own": own - base, "exploit_own_per_round": (own - base) / n, "grid_error_bound": err,
                           "stress_explore_then_shade_gain": stress - base, "stress_per_round": (stress - base) / n,
                           "argmax_cell_avg_min": min(arg.values()), "argmax_cell_avg_max": max(arg.values()), "seconds": time.time() - t0}
                    rows.append(row)
                    print(f"{env_name:9s} focal {i} {grid:6s} n={n:8d} cells={len(m.cells):5d} explore={row['exploration_share']:.3f} "
                          f"exploit full {row['exploit_full_per_round']:+.5f}/rd own {row['exploit_own_per_round']:+.5f}/rd  stress(out) {row['stress_per_round']:+.4f}/rd  {row['seconds']:.1f}s")
    with (out / "exact_exploitability.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--horizons", type=int, nargs="+", default=[2000, 8000, 32000, 128000, 512000, 2000000])
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    print("== cross-check (i) against the retained summary.csv"); crosscheck(out)
    print("== exact exploitability table"); table(out, a.horizons)
