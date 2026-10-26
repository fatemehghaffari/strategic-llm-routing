"""Aggregate Agent C raw CSVs into experiments/data/A5 and print the headline tables."""
import glob
import os
import sys

import numpy as np
import pandas as pd

RAW = "<workspace>/v3/C/raw"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "../../../../experiments/data/A5"))
V2 = os.path.normpath(os.path.join(HERE, "../../../../experiments/data/A4/v2_all_summary.csv"))
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 300)


def cat(prefix):
    fs = sorted(glob.glob(os.path.join(RAW, f"{prefix}_*.csv")))
    return pd.concat([pd.read_csv(f) for f in fs], ignore_index=True) if fs else pd.DataFrame()


def main():
    what = sys.argv[1:] or ["c7", "c9", "c5"]
    v2 = pd.read_csv(V2)
    v2["arm"] = v2.mech + ":" + v2.profile
    if "c7" in what:
        d = cat("c7")
        if len(d):
            d.to_csv(os.path.join(OUT, "c7_cao_per_type.csv"), index=False)
            print(f"== item 7: Cao one copy per type (OUR construction), {d.subset.nunique()} subsets, "
                  f"{len(d)} rows")
            t = d.pivot_table(index=["n", "arm"], columns="order", values="revenue_per_round")
            print(t.round(3).to_string())
            ref = v2[v2.arm.isin(["plmesp:plmesp_star", "second_best:cao_eqmu", "second_best:cao_eq0"])]
            print(ref.pivot_table(index=["n", "arm"], columns="order", values="revenue_per_round")
                  .loc[[300000, 3000000]].round(3).to_string())
            m = d.merge(v2[v2.arm == "plmesp:plmesp_star"][["subset", "n", "order", "revenue_per_round"]],
                        on=["subset", "n", "order"], suffixes=("", "_pl"))
            m["pl_minus"] = m.revenue_per_round_pl - m.revenue_per_round
            print("PL-MESP S* minus per-type Cao: subsets ahead / mean margin")
            print(m.groupby(["n", "arm", "order"]).pl_minus.agg(
                ahead=lambda s: int((s > 0).sum()), mean="mean", min="min").round(3).to_string())
            print("per-type Cao unserved:",
                  d.groupby(["n", "arm", "order"]).unserved_fraction.mean().round(3).to_dict())
    if "c9" in what:
        d = cat("c9")
        if len(d):
            d.to_csv(os.path.join(OUT, "c9_graded.csv"), index=False)
            print(f"\n== item 9: graded rewards, {len(d)} rows")
            ref = v2[(v2.n == 3000000) & v2.order.isin(["iid", "bursty"])].copy()
            ref["variant"] = "bernoulli(v2)"
            cols = ["variant", "order", "arm"]
            both = pd.concat([d[cols + ["revenue_per_round", "fire_rate"]],
                              ref[ref.arm.isin(d.arm.unique())][cols + ["revenue_per_round", "fire_rate"]]])
            print(both.pivot_table(index=["arm", "order"], columns="variant",
                                   values=["revenue_per_round", "fire_rate"]).round(3).to_string())
    if "c5" in what:
        d = cat("c5")
        if len(d):
            d.to_csv(os.path.join(OUT, "c5_noisy_labels.csv"), index=False)
            print(f"\n== item 5: noisy labels, {len(d)} rows")
            d["eps"] = d.variant.astype(str)
            print(d.pivot_table(index="arm", columns="eps", values="revenue_per_round").round(3).to_string())
            print(d.pivot_table(index="arm", columns="eps", values="fire_rate").round(3).to_string())
            if "compliant_conviction_rate" in d:
                print(d.pivot_table(index="arm", columns="eps", values="compliant_conviction_rate")
                      .round(3).to_string())


if __name__ == "__main__":
    main()
