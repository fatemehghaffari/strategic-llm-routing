"""Step 2(a): measured capability functions over FINITE contexts.

context z  := the benchmark family a query comes from (RouterBench's own
              `eval_name`, grouped into the seven families its Table 1 reports)
M_i(z)     := model i's mean published performance score on the rows of z

Nothing here is simulated.  Every number is an average of published
per-query outcome scores.

Outputs (all written to out/ and later copied to experiments/data/A4/):
  capabilities_finite_<shot>.csv   M_i(z) per model per family, with row counts
  context_masses_<shot>.csv        empirical mass of each family
  validation_vs_paper_table1.csv   our M_i(z) minus RouterBench's Table 1
  rowcounts.csv                    provenance row counts
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import FAMILIES, MODELS, OUT, SHORT, load_shot  # noqa: E402


def clean(df, shot):
    """Drop unusable rows and report exactly how many were dropped."""
    rep = {"shot": shot, "rows_published": len(df)}
    df = df.drop_duplicates(subset="sample_id", keep="first")
    rep["rows_after_dedup"] = len(df)
    ok = df[MODELS].notna().all(axis=1)
    df = df[ok]
    rep["rows_after_dropna"] = len(df)
    rep["rows_unassigned_family"] = int((df["family"] == "UNASSIGNED").sum())
    df = df[df["family"] != "UNASSIGNED"].copy()
    rep["rows_used"] = len(df)
    rep["outcomes_used"] = len(df) * len(MODELS)
    return df, rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    reps = []
    caps = {}
    for shot in ("0shot", "5shot"):
        raw = load_shot(shot)
        df, rep = clean(raw, shot)
        reps.append(rep)

        cap = df.groupby("family")[MODELS].mean().T.loc[MODELS, FAMILIES]
        cnt = df.groupby("family").size().reindex(FAMILIES)
        cap.index = [SHORT[m] for m in cap.index]
        caps[shot] = cap

        long = cap.stack().rename("M").reset_index()
        long.columns = ["model", "context", "M"]
        long["n_queries"] = long["context"].map(cnt)
        # binomial-style standard error on the family mean (scores lie in [0,1])
        sd = df.groupby("family")[MODELS].std(ddof=1).T
        sd.index = [SHORT[m] for m in sd.index]
        long["se"] = [sd.loc[r.model, r.context] / np.sqrt(cnt[r.context])
                      for r in long.itertuples()]
        long.to_csv(os.path.join(a.out, f"capabilities_finite_{shot}.csv"), index=False)

        mass = (cnt / cnt.sum()).rename("mass").reset_index()
        mass.columns = ["context", "mass"]
        mass["n_queries"] = mass["context"].map(cnt)
        mass.to_csv(os.path.join(a.out, f"context_masses_{shot}.csv"), index=False)

    pd.DataFrame(reps).to_csv(os.path.join(a.out, "rowcounts.csv"), index=False)

    # Provenance check against RouterBench's published Table 1.  The paper uses
    # 5-shot inference for MMLU/HellaSwag/GSM8K/ARC/Winogrande and 0-shot for
    # MBPP/MT-Bench, so we compare against that mixture.
    here = os.path.dirname(os.path.abspath(__file__))
    pub = pd.read_csv(os.path.join(here, "paper_table1.csv")).set_index("model")
    fiveshot_fams = ["MMLU", "HellaSwag", "GSM8K", "ARC", "Winogrande"]
    mix = pd.DataFrame({c: (caps["5shot"][c] if c in fiveshot_fams else caps["0shot"][c])
                        for c in pub.columns})
    v = (mix - pub.loc[mix.index]).stack().rename("ours_minus_published").reset_index()
    v.columns = ["model", "context", "ours_minus_published"]
    v["ours"] = [mix.loc[r.model, r.context] for r in v.itertuples()]
    v["published"] = [pub.loc[r.model, r.context] for r in v.itertuples()]
    v.to_csv(os.path.join(a.out, "validation_vs_paper_table1.csv"), index=False)
    print("rowcounts:\n", pd.DataFrame(reps).to_string(index=False))
    print("\nmax |ours - published| by context:")
    print(v.groupby("context")["ours_minus_published"].apply(lambda s: s.abs().max()).round(4).to_string())


if __name__ == "__main__":
    main()
