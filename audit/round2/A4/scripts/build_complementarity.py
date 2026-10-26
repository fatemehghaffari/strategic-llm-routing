"""The pairwise COMPLEMENTARITY matrix, in the form the routing literature uses.

FrugalGPT (arXiv:2305.05176, Fig. 4) draws a pairwise matrix whose cell (i, j)
is the percentage of queries on which model i is wrong and model j is right.
That is a per-query statistic, so it is computed here once from the published
outcomes and committed as an AGGREGATE table (11 x 11 numbers, plus one such
table per benchmark family); no per-query row is ever committed.

A query counts as answered correctly when its published score is at least 0.5.
Scores are binary on MMLU, HellaSwag, Winogrande, ARC and MBPP; on GSM8K and
MT-Bench they are graded, and the threshold is stated here rather than hidden.
"""
import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_capabilities import clean  # noqa: E402
from rb_common import FAMILIES, MODELS, OUT, SHORT, load_shot  # noqa: E402

THRESH = 0.5


def main():
    df, _ = clean(load_shot("5shot"), "5shot")
    right = (df[MODELS].values >= THRESH)
    names = [SHORT[m] for m in MODELS]
    rows = []
    for scope in ["ALL"] + FAMILIES:
        sel = np.ones(len(df), dtype=bool) if scope == "ALL" else (df["family"] == scope).values
        R = right[sel]
        for a, b in itertools.permutations(range(len(names)), 2):
            rows.append({"scope": scope, "row_model": names[a], "col_model": names[b],
                         "row_wrong_col_right": float((~R[:, a] & R[:, b]).mean()),
                         "n_queries": int(sel.sum()),
                         "row_accuracy": float(R[:, a].mean()),
                         "col_accuracy": float(R[:, b].mean())})
        for a in range(len(names)):
            rows.append({"scope": scope, "row_model": names[a], "col_model": names[a],
                         "row_wrong_col_right": 0.0, "n_queries": int(sel.sum()),
                         "row_accuracy": float(R[:, a].mean()),
                         "col_accuracy": float(R[:, a].mean())})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(OUT, "complementarity.csv"), index=False)
    m = out[out.scope == "ALL"].pivot(index="row_model", columns="col_model",
                                      values="row_wrong_col_right")
    pd.set_option("display.width", 250)
    print("share of queries where the ROW model is wrong and the COLUMN model is right:")
    print((100 * m).round(1).to_string())
    print()
    print("max off-diagonal:", round(float(m.values.max()), 4))
    print("min over pairs of max(i->j, j->i):",
          round(float(min(max(m.iloc[i, j], m.iloc[j, i])
                          for i in range(len(m)) for j in range(i + 1, len(m)))), 4))


if __name__ == "__main__":
    main()
