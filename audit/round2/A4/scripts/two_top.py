"""THE TWO-TOP CONDITION, MEASURED ON REAL LLM CAPABILITIES.

The condition "at least two providers attain the largest capability" is the
hinge of the paper. It makes the public contextual equilibrium work, it rules
out the low-revenue equilibria of Theorem `thm:equilibrium-set`, and it governs
pairwise collusion. It is an EXACT-TIE condition, so on measured data it can
only hold approximately, and the useful question is quantitative: for a given
tolerance `delta`, on how much ARRIVAL MASS are the top two capabilities within
`delta` of one another?

We compute, for every subset of the eleven models of every size from 2 to 11:
  * the mass-weighted mean gap between the best and second-best capability;
  * the arrival mass on which that gap is at most `delta`, for a grid of delta;
  * the same restricted to the mass where the identity of the best provider is
    itself not unique.

No simulation. Pure arithmetic on the measured capability table.
"""
import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import OUT  # noqa: E402

SETS = {"Q3": ["MMLU", "HellaSwag", "GSM8K"],
        "Q7": ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]}
DELTAS = (0.0, 0.002, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20)
MAXSUB = 20000     # cap on subsets enumerated per size, for the large sizes


def main():
    cap = pd.read_csv(os.path.join(OUT, "capabilities_finite_5shot.csv"))
    mass = pd.read_csv(os.path.join(OUT, "context_masses_5shot.csv")).set_index("context")
    rows = []
    for name, fams in SETS.items():
        t = cap[cap.context.isin(fams)].pivot(index="model", columns="context",
                                              values="M")[fams]
        p = mass.loc[fams, "n_queries"].values.astype(float)
        p = p / p.sum()
        models = sorted(t.index)
        for K in range(2, len(models) + 1):
            subs = list(itertools.combinations(models, K))
            if len(subs) > MAXSUB:
                subs = subs[:MAXSUB]
            for sub in subs:
                A = t.loc[list(sub)].values
                srt = np.sort(A, axis=0)
                gap = srt[-1] - srt[-2]
                rec = {"context_set": name, "K": K, "models": "|".join(sub),
                       "mean_top_gap": float(gap @ p),
                       "max_top_gap": float(gap.max()),
                       "min_top_gap": float(gap.min())}
                for dl in DELTAS:
                    rec[f"mass_within_{dl}"] = float(p[gap <= dl + 1e-12].sum())
                rows.append(rec)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "two_top_condition.csv"), index=False)

    agg = {"n_subsets": ("models", "size"),
           "mean_top_gap": ("mean_top_gap", "mean"),
           "best_subset_min_mean_top_gap": ("mean_top_gap", "min")}
    for d in DELTAS:
        agg[f"mean_mass_within_{d}"] = (f"mass_within_{d}", "mean")
        agg[f"best_subset_mass_within_{d}"] = (f"mass_within_{d}", "max")
        agg[f"frac_subsets_mass_within_{d}_above_0.9"] = (
            f"mass_within_{d}", lambda s: float((s >= 0.9).mean()))
    summ = df.groupby(["context_set", "K"]).agg(**agg).reset_index()
    summ.to_csv(os.path.join(OUT, "two_top_summary.csv"), index=False)

    # the most two-top-like subsets that actually exist
    best = []
    for (name, K), s in df.groupby(["context_set", "K"]):
        r = s.loc[s.mean_top_gap.idxmin()]
        best.append({"context_set": name, "K": K, "models": r.models,
                     "mean_top_gap": r.mean_top_gap,
                     "mass_within_0.01": r["mass_within_0.01"],
                     "mass_within_0.05": r["mass_within_0.05"],
                     "mass_within_0.10": r["mass_within_0.1"]})
    pd.DataFrame(best).to_csv(os.path.join(OUT, "two_top_best_subsets.csv"), index=False)

    pd.set_option("display.width", 300)
    cols = ["context_set", "K", "n_subsets", "mean_top_gap"] + \
           [f"mean_mass_within_{d}" for d in (0.0, 0.01, 0.05, 0.1, 0.2)]
    print(summ[cols].round(4).to_string(index=False))
    print()
    print(pd.DataFrame(best).round(4).to_string(index=False))


if __name__ == "__main__":
    main()
