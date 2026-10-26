"""Step 2(b): measured capability functions over CONTINUOUS contexts.

context x  := a d-dimensional embedding of the query text, rank-transformed so
              that each coordinate is uniform on [0,1], which is the context
              space [0,1]^d the paper's continuous results assume.
M_i(x)     := model i's mean published score over the k nearest OTHER queries
              to x in that space (a leave-one-out local average).

Embedding: TF-IDF over word 1-2 grams, then truncated SVD (latent semantic
analysis).  This is a local CPU embedding with no external service and no
paid API.  It is deliberately the cheapest defensible choice: nothing in the
experiment depends on the embedding being good, only on it being FIXED before
any capability or any mechanism is computed.

Choice of d.  The mechanism partitions [0,1]^D into b_n^D cells.  In LLM
routing one query arrives and every provider sees the SAME query, so the
profile (x_1,...,x_K) lies on the diagonal of [0,1]^{Kd} and the number of
cells carrying positive mass is b_n^d, not b_n^{Kd}; the paper's own remark
about lazily initialised cells is what makes this legitimate.  With
h_n = n^{-1/(D+3)} and n = 10^6 this gives 16^2 = 256 populated cells at d=2
and 10^3 = 1000 at d=3.  We take d = 2 as primary because it is the largest d
at which every populated cell still receives enough visits at our horizon for
the local elicitation block to complete, and we report d = 1 and d = 3.

Outputs: contexts_d{d}.npy, capsurface_d{d}_k{k}.npy, capsurface_meta.csv,
         capabilities_continuous_summary.csv
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import MODELS, OUT, SHORT, load_shot  # noqa: E402
from build_capabilities import clean  # noqa: E402


def build(out, dims, ks, seed=20260924):
    prompts = load_shot("0shot")[["sample_id", "prompt"]]
    scores, _ = clean(load_shot("5shot"), "5shot")
    df = scores.drop(columns=["prompt"]).merge(prompts, on="sample_id", how="inner")
    df = df.sort_values("sample_id").reset_index(drop=True)
    print(f"queries embedded: {len(df)}")

    vec = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=5,
                          max_features=200000, sublinear_tf=True,
                          strip_accents="unicode")
    X = vec.fit_transform(df["prompt"].values)
    print(f"tfidf matrix: {X.shape}, nnz={X.nnz}")

    Y = df[MODELS].values.astype(float)
    meta = []
    for d in dims:
        svd = TruncatedSVD(n_components=d, random_state=seed)
        Z = svd.fit_transform(X)
        # rank transform each coordinate to uniform [0,1]
        U = np.column_stack([(rankdata(Z[:, j]) - 0.5) / len(Z) for j in range(d)])
        np.save(os.path.join(out, f"contexts_d{d}.npy"), U)
        nn = NearestNeighbors(n_neighbors=max(ks) + 1).fit(U)
        _, idx = nn.kneighbors(U)
        for k in ks:
            nbr = idx[:, 1:k + 1]              # drop self: leave-one-out
            M = Y[nbr].mean(axis=1)            # (n_queries, n_models)
            np.save(os.path.join(out, f"capsurface_d{d}_k{k}.npy"), M)
            meta.append({"d": d, "k": k, "n_queries": len(df),
                         "explained_variance_ratio": float(svd.explained_variance_ratio_.sum()),
                         "mean_M": float(M.mean()),
                         "mean_pointwise_max_M": float(M.max(axis=1).mean()),
                         "mean_pointwise_second_M": float(np.sort(M, axis=1)[:, -2].mean()),
                         "mean_global_max_M": float(M.mean(axis=0).max()),
                         "mean_global_second_M": float(np.sort(M.mean(axis=0))[-2])})
            print(meta[-1])
    pd.DataFrame(meta).to_csv(os.path.join(out, "capsurface_meta.csv"), index=False)
    df[["sample_id", "family"]].to_csv(os.path.join(out, "query_index.csv"), index=False)
    pd.DataFrame({"model": [SHORT[m] for m in MODELS]}).to_csv(
        os.path.join(out, "model_order.csv"), index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dims", default="1,2,3")
    ap.add_argument("--ks", default="50,200,800")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    build(a.out, [int(x) for x in a.dims.split(",")], [int(x) for x in a.ks.split(",")])


if __name__ == "__main__":
    main()
