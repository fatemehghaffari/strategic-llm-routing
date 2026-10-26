"""Rank-flip statistics on the CONTINUOUS context space, for comparison with
the finite ones, plus a diagnostic on how much the embedding actually carries.
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import OUT  # noqa: E402


def cells_for(U, n, d):
    b = int(np.ceil(n ** (1.0 / (d + 3))))
    cc = np.minimum((U * b).astype(int), b - 1)
    key = np.zeros(len(U), dtype=np.int64)
    for j in range(d):
        key = key * b + cc[:, j]
    _, key = np.unique(key, return_inverse=True)
    return key, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    names = pd.read_csv(os.path.join(a.out, "model_order.csv"))["model"].tolist()
    fam = pd.read_csv(os.path.join(a.out, "query_index.csv"))["family"].values
    rows, diag = [], []
    for d in (1, 2, 3):
        U = np.load(os.path.join(a.out, f"contexts_d{d}.npy"))
        key, b = cells_for(U, a.n, d)
        for k in (50, 200, 800):
            S = np.load(os.path.join(a.out, f"capsurface_d{d}_k{k}.npy"))
            df = pd.DataFrame(S, columns=names)
            df["cell"] = key
            cellmean = df.groupby("cell")[names].mean()
            cellsize = df.groupby("cell").size()
            cells = cellmean.index.tolist()
            raw_f = raw_n = 0
            for x, y in itertools.combinations(names, 2):
                g = (cellmean[x] - cellmean[y]).values
                for u, v in itertools.combinations(range(len(cells)), 2):
                    if g[u] == 0 or g[v] == 0:
                        continue
                    raw_n += 1
                    raw_f += (g[u] > 0) != (g[v] > 0)
            best_cell = cellmean.idxmax(axis=1)
            best_query = np.asarray(names)[S.argmax(axis=1)]
            gbest = names[int(np.argmax(S.mean(axis=0)))]
            rows.append({
                "d": d, "k": k, "n_cells": len(cells), "b": b, "n": a.n,
                "raw_flip_rate": raw_f / raw_n if raw_n else np.nan,
                "n_cell_pairs_compared": raw_n,
                "n_distinct_best_cell": int(best_cell.nunique()),
                "frac_cells_best_differs_from_global": float((best_cell != gbest).mean()),
                "frac_queries_best_differs_from_global": float((best_query != gbest).mean()),
                "mean_pointwise_max": float(S.max(axis=1).mean()),
                "mean_pointwise_second": float(np.sort(S, axis=1)[:, -2].mean()),
                "global_max_mean": float(S.mean(axis=0).max()),
                "global_second_mean": float(np.sort(S.mean(axis=0))[-2]),
                "median_cell_size": float(cellsize.median()),
                "min_cell_size": int(cellsize.min())})
            print(rows[-1], flush=True)
        # diagnostic: how much family information does the d-dim embedding carry?
        ct = pd.crosstab(key, fam)
        purity = float((ct.max(axis=1).sum()) / ct.values.sum())
        p = ct.values / ct.values.sum()
        px, py = p.sum(1, keepdims=True), p.sum(0, keepdims=True)
        nz = p > 0
        mi = float((p[nz] * np.log(p[nz] / (px @ py)[nz])).sum())
        hy = float(-(py[py > 0] * np.log(py[py > 0])).sum())
        diag.append({"d": d, "n_cells": len(np.unique(key)), "cell_family_purity": purity,
                     "normalised_mutual_info_cell_family": mi / hy if hy else np.nan})
        print(diag[-1], flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "flips_continuous.csv"), index=False)
    pd.DataFrame(diag).to_csv(os.path.join(a.out, "embedding_diagnostic.csv"), index=False)


if __name__ == "__main__":
    main()
