"""Aggregate the per-task JSON of the CG-MESP horizon sweep into two CSVs.

  threshold_sweep.csv    one row per (instance, horizon, behaviour profile, seed), everything measured
  threshold_summary.csv  one row per (instance, horizon): what the mechanism does there, and whether
                         each of the three guarantees is non-vacuous and satisfied

Deviation gains are PAIRED: gain(config, seed) = u0(config, seed) - u0(proposed, seed), which is the
same pairing the reference gets from pre-drawing the context path and the seeds.  They are lower
bounds on exploitability for the seven deviations tried and nothing more.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
from collections import defaultdict

DEVS = ["underbid", "rider25", "rider50", "rider100", "both", "crash"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rows = []
    for p in sorted(glob.glob(os.path.join(a.results, "*.json"))):
        with open(p) as f:
            rows.append(json.load(f))
    if not rows:
        raise SystemExit("no results")
    flat_fields = ["inst", "logn", "n", "config", "seed", "K", "D", "d", "g", "J", "L", "h", "s", "rho",
                   "sigma", "ell", "awarded", "tau_pos", "positive_price_share", "zero_price_share",
                   "mean_tau", "max_tau", "switches", "false_switches", "viol_P2", "viol_P4",
                   "stage1", "stage2", "stage3", "rev", "rev_stage1", "rev_stage2", "rev_stage3",
                   "bench_M2", "bench_honest", "boundA", "slackB", "slackC",
                   "e_bid", "e_stage1", "e_osc", "e_mon", "e_fb", "e_price", "e_rob",
                   "bench_M2_neumaier_minus_naive", "bench_honest_neumaier_minus_naive",
                   "wall_s", "ns_per_round", "slurm_job", "kernel"]
    with open(os.path.join(a.out, "threshold_sweep.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(flat_fields + ["u0", "u0_naive"])
        for r in rows:
            w.writerow([r.get(k, "") for k in flat_fields] + [r["util"][0], r["util_naive"][0]])

    by = defaultdict(dict)   # (inst, logn) -> (config, seed) -> row
    for r in rows:
        by[(r["inst"], int(r.get("d", r["K"])), round(r["logn"], 2))][(r["config"], r["seed"])] = r

    out = []
    for (inst, dctx, lg), d in sorted(by.items()):
        props = [v for (c, s), v in d.items() if c == "proposed"]
        if not props:
            continue
        p0 = props[0]
        n = p0["n"]
        rec = dict(inst=inst, d=dctx, logn=lg, n=n, K=p0["K"], D=p0["D"], g=p0["g"], J=p0["J"],
                   L=p0["L"],
                   s_n=p0["s"], rho_n=p0["rho"], sigma_n=p0["sigma"],
                   n_seeds_proposed=len(props),
                   awarded=p0["awarded"],
                   awarded_share_of_cells=p0["awarded"] / p0["J"],
                   positive_price_share=sum(v["positive_price_share"] for v in props) / len(props),
                   mean_tau=sum(v["mean_tau"] for v in props) / len(props),
                   max_tau=max(v["max_tau"] for v in props),
                   switches_proposed=sum(v["switches"] for v in props),
                   false_switches_proposed=sum(v["false_switches"] for v in props),
                   viol_P2_proposed=sum(v["viol_P2"] for v in props),
                   viol_P4_proposed=sum(v["viol_P4"] for v in props),
                   stage1_share=sum(v["stage1"] for v in props) / len(props) / n,
                   stage2_share=sum(v["stage2"] for v in props) / len(props) / n,
                   stage3_share=sum(v["stage3"] for v in props) / len(props) / n,
                   rev_per_round=sum(v["rev"] for v in props) / len(props) / n,
                   bench_M2_per_round=sum(v["bench_M2"] for v in props) / len(props) / n,
                   bench_honest_per_round=sum(v["bench_honest"] for v in props) / len(props) / n,
                   boundA=p0["boundA"], slackB=p0["slackB"], slackC=p0["slackC"],
                   boundA_over_n=p0["boundA"] / n, slackB_over_n=p0["slackB"] / n,
                   slackC_over_n=p0["slackC"] / n,
                   wall_s_proposed=p0["wall_s"], ns_per_round=p0["ns_per_round"],
                   bench_M2_fp_drift=p0["bench_M2_neumaier_minus_naive"])
        rec["revenue_deficit_B"] = (sum(v["bench_M2"] - v["rev"] for v in props) / len(props))
        rec["B_nonvacuous"] = int(p0["slackB"] < n)
        rec["B_holds"] = int(rec["revenue_deficit_B"] <= p0["slackB"])
        rec["A_nonvacuous"] = int(p0["boundA"] < n)
        rec["C_nonvacuous"] = int(p0["slackC"] < n)
        # paired deviation gains
        best, per = -math.inf, {}
        for c in DEVS:
            gs = [d[(c, s)]["util"][0] - d[("proposed", s)]["util"][0]
                  for (cc, s) in d if cc == c and ("proposed", s) in d]
            if gs:
                per[c] = sum(gs) / len(gs)
                rec[f"gain_{c}"] = per[c]
                rec[f"gain_{c}_max"] = max(gs)
                rec[f"gain_{c}_nseeds"] = len(gs)
                best = max(best, max(gs))
        rec["best_searched_gain"] = best if per else float("nan")
        rec["best_searched_gain_over_boundA"] = (best / p0["boundA"]) if per else float("nan")
        rec["A_holds"] = int(best <= p0["boundA"]) if per else ""
        # monitor behaviour by profile: does the boundary convict a crashing winner, and does it
        # ever convict a compliant one?
        for c in ("crash", "rider100", "rider50", "underbid", "both", "sabotage_joint"):
            vs = [v for (cc, s), v in d.items() if cc == c]
            if vs:
                rec[f"switches_{c}"] = sum(v["switches"] for v in vs)
                rec[f"false_switches_{c}"] = sum(v["false_switches"] for v in vs)
                rec[f"conviction_share_{c}"] = (sum(v["switches"] for v in vs)
                                                / max(sum(v["awarded"] for v in vs), 1))
        # part (C): every strategic agent delivers its floor in every phase
        sab = [v for (c, s), v in d.items() if c == "sabotage_joint"]
        if sab:
            rec["sabotage_rev_per_round"] = sum(v["rev"] for v in sab) / len(sab) / n
            rec["sabotage_bench_honest_per_round"] = sum(v["bench_honest"] for v in sab) / len(sab) / n
            rec["honest_deficit_C"] = sum(v["bench_honest"] - v["rev"] for v in sab) / len(sab)
            rec["C_holds"] = int(rec["honest_deficit_C"] <= p0["slackC"])
            rec["sabotage_switches"] = sum(v["switches"] for v in sab)
        out.append(rec)

    keys = []
    for r in out:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(os.path.join(a.out, "threshold_summary.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in sorted(out, key=lambda r: (r["d"], r["inst"], r["logn"])):
            w.writerow(r)
    print(f"{len(rows)} runs -> {len(out)} (instance, horizon) rows in {a.out}")


if __name__ == "__main__":
    main()
