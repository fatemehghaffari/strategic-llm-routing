"""Combine the v3 task CSVs into experiments/data/A5/v3_summary.csv.
Seed-sharded cells (3e7) are merged with weights = number of seeds per shard.
revenue_sd over shards is recomputed from per-shard means only when every shard holds one seed."""
import glob, os, sys
import numpy as np, pandas as pd
RAW = sys.argv[1] if len(sys.argv) > 1 else \
    "<scratch>/B/raw"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "../../../../experiments/data/A5/v3_summary.csv"))
fs = sorted(glob.glob(os.path.join(RAW, "*.csv")))
d = pd.concat([pd.read_csv(f).assign(item=os.path.basename(f).split("_")[0]) for f in fs], ignore_index=True)
key = ["item", "taskset", "subset", "models", "K", "n", "order", "mech", "profile"]
num = [c for c in d.columns if c not in key and c != "nseeds" and pd.api.types.is_numeric_dtype(d[c])]
def comb(g):
    w = g["nseeds"].values.astype(float)
    row = {c: np.average(g[c].values, weights=w) if np.isfinite(g[c].values).all() else
           (np.nanmean(g[c].values) if np.isfinite(g[c].values).any() else np.nan) for c in num}
    row["nseeds"] = int(w.sum())
    if len(g) > 1 and (w == 1).all():
        row["revenue_sd"] = float(np.std(g["revenue_per_round"].values))
    return pd.Series(row)
s = d.groupby(key, dropna=False).apply(comb, include_groups=False).reset_index()
s.to_csv(OUT, index=False)
print(len(fs), "files ->", len(s), "cells ->", OUT)
