"""Audit every committed table for a measured rule that beats the oracle or
falls below the honest benchmark.

A rule that allocates can never deliver more than the pointwise-best
capability, so measured revenue above the oracle ON THE SAME ROW is always a
bug or a mismatched aggregation. Revenue below the honest benchmark is
possible and expected at a finite horizon under strategic play, so it is
reported rather than flagged as an error.

    python audit_reference_lines.py --csv experiments/data/A4
"""
import argparse
import os

import pandas as pd

# (file, revenue columns, oracle column, honest column)
TARGETS = [
    ("headline_summary.csv", ["nonstrategic", "strategic"], "oracle", "honest_bench"),
    ("headline_worlds.csv", ["revenue_per_round"], "oracle", "honest_bench"),
    ("exploitability.csv", ["revenue_at_best_deviation"], "oracle", "honest_bench"),
    ("strategic_profiles.csv", ["revenue_per_round", "revenue_at_proposed"],
     "oracle", "honest_bench"),
    ("fine_shading.csv", ["revenue_per_round", "baseline_revenue_per_round"],
     "oracle", "honest_bench"),
    ("fine_shading_best.csv", ["revenue_per_round", "baseline_revenue_per_round"],
     "oracle", "honest_bench"),
    ("undercut_comparison.csv", ["revenue_per_round", "baseline_revenue_per_round"],
     "oracle", "honest_bench"),
    ("flip_regression.csv", ["rev_plmesp", "rev_mesp_scalar"], "oracle", None),
    ("horizon_sweep.csv", ["rev_plmesp", "rev_mesp_scalar"], "oracle", "honest_bench"),
    ("horizon_all_triples.csv", ["rev_plmesp", "rev_mesp_scalar"], "oracle",
     "honest_bench"),
    ("baseline_single_observation.csv", ["revenue_per_round"], "oracle",
     "honest_bench"),
    ("utility_curves.csv", ["platform_revenue_per_round"], None, None),
]
TOL = 1e-9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    a = ap.parse_args()
    rows = []
    for fn, revs, orc, hon in TARGETS:
        p = os.path.join(a.csv, fn)
        if not os.path.exists(p):
            rows.append({"file": fn, "status": "absent"})
            continue
        d = pd.read_csv(p)
        rec = {"file": fn, "rows": len(d), "status": "ok"}
        for c in revs:
            if c not in d.columns:
                continue
            if orc and orc in d.columns:
                bad = int((d[c] > d[orc] + TOL).sum())
                rec[f"{c}_above_oracle"] = bad
                if bad:
                    rec["status"] = "ABOVE ORACLE"
                    rec[f"{c}_worst_excess"] = float((d[c] - d[orc]).max())
            if hon and hon in d.columns:
                rec[f"{c}_below_honest"] = int((d[c] < d[hon] - TOL).sum())
        rows.append(rec)
    out = pd.DataFrame(rows).fillna("")
    pd.set_option("display.width", 260)
    print(out.to_string(index=False))
    bad = out[out.status == "ABOVE ORACLE"]
    print()
    print("FILES WITH A RULE ABOVE THE ORACLE:",
          list(bad.file) if len(bad) else "none")
    return 1 if len(bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
