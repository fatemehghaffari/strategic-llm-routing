"""The scalar-vs-contextual revenue gap in closed form, for all 165 triples.

At the proposed profile and ignoring the sublinear overheads, the two
mechanisms deliver

  contextual (PL-MESP):  E_x[ M_(2)(x) ]           the POINTWISE second capability
  scalar    (MESP):      E_x[ min(tau, M_W(x)) ]   one price, one winner

with W the model of largest context-averaged capability and tau the second
largest context-average.  The difference is the quantity the paper's premise
predicts, and this script computes it exactly from the measured capabilities,
with no simulation, so that the simulation can be checked against it.

It also regresses that gap on the measured rank-flip rate, which is the claim
the brief asks to TEST rather than confirm.
"""
import itertools
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import OUT  # noqa: E402
from select_triples import flip_rate_table  # noqa: E402

SETS = {"Q3": ["MMLU", "HellaSwag", "GSM8K"],
        "Q7": ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]}


def gaps(families, shot="5shot", out=OUT, uniform_mass=False):
    cap = pd.read_csv(os.path.join(out, f"capabilities_finite_{shot}.csv"))
    cap = cap[cap["context"].isin(families)]
    tab = cap.pivot(index="model", columns="context", values="M")[list(families)]
    mass = pd.read_csv(os.path.join(out, f"context_masses_{shot}.csv")).set_index("context")
    w = mass.loc[families, "n_queries"].values.astype(float)
    if uniform_mass:
        w = np.ones(len(families))
    p = w / w.sum()
    models = sorted(tab.index)
    rows = []
    for tri in itertools.combinations(models, 3):
        A = tab.loc[list(tri)].values                    # (3, Q)
        avg = A @ p
        W = int(np.argmax(avg))
        tau = float(np.sort(avg)[-2])
        ptwise2 = float(np.sort(A, axis=0)[-2] @ p)
        ptwise1 = float(A.max(axis=0) @ p)
        scalar = float(np.minimum(tau, A[W]) @ p)
        # mass on which the ONE announced scalar price exceeds the winner's
        # capability, i.e. on which the mechanism asks for something the winner
        # cannot deliver even at full effort
        infeasible = float(p[(tau > A[W] + 1e-12)].sum())
        # the same for the contextual mechanism, where the price is the local
        # second capability and is feasible at the winner by construction
        rows.append({"models": "|".join(tri), "winner": tri[W], "tau_scalar": tau,
                     "oracle": ptwise1, "contextual_rev": ptwise2,
                     "scalar_rev": scalar, "gap": ptwise2 - scalar,
                     "gap_rel": (ptwise2 - scalar) / max(ptwise2, 1e-12),
                     "scalar_mass_price_above_capability": infeasible,
                     "contextual_mass_price_above_capability": 0.0})
    return pd.DataFrame(rows)


def main():
    all_rows = []
    for name, fams in SETS.items():
        for um in (False, True):
            g = gaps(fams, uniform_mass=um)
            f = flip_rate_table(fams)[["models", "flip_rate", "n_distinct_best"]]
            m = g.merge(f, on="models")
            m["context_set"] = name
            m["uniform_mass"] = um
            all_rows.append(m)
    df = pd.concat(all_rows, ignore_index=True)
    df.to_csv(os.path.join(OUT, "analytic_gap_triples.csv"), index=False)

    summ = []
    for (name, um), sub in df.groupby(["context_set", "uniform_mass"]):
        sp = stats.spearmanr(sub.flip_rate, sub.gap)
        pe = stats.pearsonr(sub.flip_rate, sub.gap)
        sl = stats.linregress(sub.flip_rate, sub.gap)
        summ.append({"context_set": name, "uniform_mass": um, "n_triples": len(sub),
                     "spearman_rho": sp.statistic, "spearman_p": sp.pvalue,
                     "pearson_r": pe.statistic, "pearson_p": pe.pvalue,
                     "ols_slope": sl.slope, "ols_intercept": sl.intercept,
                     "ols_r2": sl.rvalue ** 2,
                     "gap_at_flip0_mean": float(sub[sub.flip_rate == 0].gap.mean()),
                     "gap_max": float(sub.gap.max()),
                     "gap_mean": float(sub.gap.mean()),
                     "frac_triples_gap_above_0.01": float((sub.gap > 0.01).mean()),
                     "mean_scalar_mass_price_above_capability":
                         float(sub.scalar_mass_price_above_capability.mean()),
                     "frac_triples_scalar_price_infeasible_somewhere":
                         float((sub.scalar_mass_price_above_capability > 0).mean()),
                     "spearman_flip_vs_infeasible_mass":
                         stats.spearmanr(sub.flip_rate,
                                         sub.scalar_mass_price_above_capability).statistic})
    s = pd.DataFrame(summ)
    s.to_csv(os.path.join(OUT, "analytic_gap_summary.csv"), index=False)
    print(s.round(4).to_string(index=False))
    print()
    for (name, um), sub in df.groupby(["context_set", "uniform_mass"]):
        print(name, "uniform" if um else "realmass",
              "| gap by flip-rate quartile:")
        sub = sub.copy()
        sub["q"] = pd.qcut(sub.flip_rate, 4, duplicates="drop")
        print(sub.groupby("q", observed=True).gap.agg(["mean", "max", "count"]).round(4).to_string())


if __name__ == "__main__":
    main()
