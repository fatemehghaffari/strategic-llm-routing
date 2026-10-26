"""Step 2, second half: HOW OFTEN DOES THE RANKING BETWEEN MODELS FLIP?

The paper's premise is that a provider's capability depends on the task, so a
single scalar per provider is the wrong object.  The sharpest measurable form
of that premise is: given two providers, does which of them is better depend on
the context?  We measure it three ways and we distinguish an apparent flip from
one the sample size supports.

Definitions, all over the finite context set (the seven RouterBench families):

  raw pairwise flip rate
      over all (unordered model pair {i,j}, unordered context pair {z,z'})
      with M_i(z) != M_j(z) and M_i(z') != M_j(z'), the fraction on which
      sign(M_i(z) - M_j(z)) != sign(M_i(z') - M_j(z')).

  significant pairwise flip rate
      the same, restricted to comparisons where BOTH within-context gaps are
      significant.  Because the two models answer the SAME queries inside a
      context, the correct test is paired: a two-sided t test on the per-query
      difference of published scores.  We report alpha = 0.05 and also a
      Bonferroni correction over all model-pair x context tests.

  top-model instability
      the number of distinct pointwise-best models across contexts, and the
      fraction of context pairs whose best model differs.

Outputs: flips_pairwise_<shot>.csv, flips_summary_<shot>.csv,
         flips_triples_<shot>.csv (every 3-model subset), kendall_<shot>.csv
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import FAMILIES, MODELS, OUT, SHORT, load_shot  # noqa: E402
from build_capabilities import clean  # noqa: E402


def pairwise_table(df, contexts):
    """Per (model pair, context): mean gap, paired-t p value, sign."""
    rows = []
    for z in contexts:
        sub = df[df["family"] == z]
        for a, b in itertools.combinations(MODELS, 2):
            d = sub[a].values - sub[b].values
            mean = float(d.mean())
            if np.allclose(d, d[0]):
                p = 1.0 if mean == 0 else 0.0
            else:
                p = float(stats.ttest_1samp(d, 0.0).pvalue)
            rows.append({"context": z, "model_a": SHORT[a], "model_b": SHORT[b],
                         "gap": mean, "p_paired_t": p, "n_queries": len(d)})
    return pd.DataFrame(rows)


def flip_rates(pw, alpha, n_tests):
    """Raw and significant flip rates from the (pair, context) gap table."""
    out = {}
    g = pw.groupby(["model_a", "model_b"])
    raw_f = raw_n = sig_f = sig_n = bon_f = bon_n = 0
    per_pair = []
    for (a, b), sub in g:
        sub = sub.set_index("context")
        for z, zz in itertools.combinations(sub.index, 2):
            g1, g2 = sub.loc[z, "gap"], sub.loc[zz, "gap"]
            if g1 == 0 or g2 == 0:
                continue
            flip = (g1 > 0) != (g2 > 0)
            raw_n += 1
            raw_f += flip
            if sub.loc[z, "p_paired_t"] < alpha and sub.loc[zz, "p_paired_t"] < alpha:
                sig_n += 1
                sig_f += flip
            if (sub.loc[z, "p_paired_t"] < alpha / n_tests
                    and sub.loc[zz, "p_paired_t"] < alpha / n_tests):
                bon_n += 1
                bon_f += flip
        pn = pf = 0
        for z, zz in itertools.combinations(sub.index, 2):
            g1, g2 = sub.loc[z, "gap"], sub.loc[zz, "gap"]
            if g1 == 0 or g2 == 0:
                continue
            pn += 1
            pf += (g1 > 0) != (g2 > 0)
        per_pair.append({"model_a": a, "model_b": b, "n_context_pairs": pn,
                         "n_flips": int(pf), "flip_rate": pf / pn if pn else np.nan})
    out["raw_flip_rate"] = raw_f / raw_n if raw_n else np.nan
    out["raw_comparisons"] = raw_n
    out["raw_flips"] = int(raw_f)
    out["sig_flip_rate"] = sig_f / sig_n if sig_n else np.nan
    out["sig_comparisons"] = sig_n
    out["sig_flips"] = int(sig_f)
    out["bonf_flip_rate"] = bon_f / bon_n if bon_n else np.nan
    out["bonf_comparisons"] = bon_n
    out["bonf_flips"] = int(bon_f)
    return out, pd.DataFrame(per_pair)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--alpha", type=float, default=0.05)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    for shot in ("0shot", "5shot"):
        df, _ = clean(load_shot(shot), shot)
        pw = pairwise_table(df, FAMILIES)
        pw.to_csv(os.path.join(a.out, f"flips_pairwise_{shot}.csv"), index=False)

        n_tests = len(pw)
        summ, per_pair = flip_rates(pw, a.alpha, n_tests)
        per_pair.to_csv(os.path.join(a.out, f"flips_perpair_{shot}.csv"), index=False)

        cap = df.groupby("family")[MODELS].mean().T.loc[MODELS, FAMILIES]
        cap.index = [SHORT[m] for m in cap.index]
        best = cap.idxmax(axis=0)
        summ["n_distinct_best_models"] = int(best.nunique())
        pairs = list(itertools.combinations(FAMILIES, 2))
        summ["ctx_pairs_with_different_best"] = int(sum(best[z] != best[zz] for z, zz in pairs))
        summ["ctx_pairs_total"] = len(pairs)
        summ["frac_ctx_pairs_different_best"] = summ["ctx_pairs_with_different_best"] / len(pairs)
        taus = [stats.kendalltau(cap[z], cap[zz]).statistic for z, zz in pairs]
        summ["mean_kendall_tau_between_contexts"] = float(np.mean(taus))
        summ["min_kendall_tau_between_contexts"] = float(np.min(taus))
        summ["shot"] = shot
        summ["n_models"] = len(MODELS)
        summ["n_contexts"] = len(FAMILIES)
        pd.DataFrame([summ]).to_csv(os.path.join(a.out, f"flips_summary_{shot}.csv"), index=False)

        kt = pd.DataFrame([{"context_a": z, "context_b": zz,
                            "kendall_tau": stats.kendalltau(cap[z], cap[zz]).statistic}
                           for z, zz in pairs])
        kt.to_csv(os.path.join(a.out, f"kendall_{shot}.csv"), index=False)

        # every 3-model subset, for the regression of the mechanism gap on the
        # flip rate in step 4
        pp = per_pair.set_index(["model_a", "model_b"])
        names = [SHORT[m] for m in MODELS]
        rows = []
        for tri in itertools.combinations(names, 3):
            nf = nn = 0
            for x, y in itertools.combinations(tri, 2):
                key = (x, y) if (x, y) in pp.index else (y, x)
                nf += pp.loc[key, "n_flips"]
                nn += pp.loc[key, "n_context_pairs"]
            sub = cap.loc[list(tri)]
            rows.append({"models": "|".join(tri), "flip_rate": nf / nn if nn else np.nan,
                         "n_flips": int(nf), "n_context_pairs": int(nn),
                         "n_distinct_best": int(sub.idxmax(axis=0).nunique())})
        pd.DataFrame(rows).to_csv(os.path.join(a.out, f"flips_triples_{shot}.csv"), index=False)
        print(shot, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in summ.items()})


if __name__ == "__main__":
    main()
