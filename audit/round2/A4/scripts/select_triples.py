"""Deterministic selection of the model triples used in the headline runs.

The rule, fixed before any mechanism was run: on a given context set, compute
the pairwise rank-flip rate of every one of the C(11,3) = 165 three-model
subsets, then take the maximum, the median-ranked and the minimum, breaking
ties by the lexicographically smallest model string.  Triples are STRATIFIED
by flip rate, not hand-picked to make a result look better; the whole point of
step 4 is to see whether the mechanism gap tracks this number.
"""
import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import OUT  # noqa: E402


def flip_rate_table(families, shot="5shot", out=OUT):
    cap = pd.read_csv(os.path.join(out, f"capabilities_finite_{shot}.csv"))
    cap = cap[cap["context"].isin(families)]
    tab = cap.pivot(index="model", columns="context", values="M")[list(families)]
    models = sorted(tab.index)
    rows = []
    for tri in itertools.combinations(models, 3):
        nf = nn = 0
        for x, y in itertools.combinations(tri, 2):
            g = tab.loc[x] - tab.loc[y]
            for z, zz in itertools.combinations(families, 2):
                if g[z] == 0 or g[zz] == 0:
                    continue
                nn += 1
                nf += (g[z] > 0) != (g[zz] > 0)
        sub = tab.loc[list(tri)]
        rows.append({"models": "|".join(tri), "flip_rate": nf / nn if nn else np.nan,
                     "n_flips": int(nf), "n_context_pairs": int(nn),
                     "n_distinct_best": int(sub.idxmax(axis=0).nunique()),
                     "mean_pointwise_max": float(sub.max(axis=0).mean()),
                     "mean_pointwise_second": float(np.sort(sub.values, axis=0)[-2].mean()),
                     "global_best_mean": float(sub.mean(axis=1).max()),
                     "global_second_mean": float(np.sort(sub.mean(axis=1).values)[-2])})
    return pd.DataFrame(rows).sort_values(["flip_rate", "models"]).reset_index(drop=True)


def pick(df):
    lo = df.iloc[0]
    hi = df.iloc[-1]
    md = df.iloc[len(df) // 2]
    return {"lowflip": lo["models"], "midflip": md["models"], "highflip": hi["models"]}


if __name__ == "__main__":
    for name, fams in [("Q3", ["MMLU", "HellaSwag", "GSM8K"]),
                       ("Q7", ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC",
                               "MBPP", "MT-Bench"])]:
        df = flip_rate_table(fams)
        df.to_csv(os.path.join(OUT, f"triples_{name}.csv"), index=False)
        sel = pick(df)
        print(name, "flip-rate range", round(df.flip_rate.min(), 4), "-",
              round(df.flip_rate.max(), 4), "median", round(df.flip_rate.median(), 4))
        for k, v in sel.items():
            r = df[df.models == v].iloc[0]
            print("  ", k, v, "flip", round(r.flip_rate, 4),
                  "ptwise2nd", round(r.mean_pointwise_second, 4),
                  "global2nd", round(r.global_second_mean, 4),
                  "gap", round(r.mean_pointwise_second - r.global_second_mean, 4))
