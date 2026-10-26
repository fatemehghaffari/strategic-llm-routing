"""Does the scalar mechanism's loss TRACK the measured rank-flip rate?

Runs the contextual and the scalar mechanism at the proposed profile on every
one of the 165 three-model subsets, and regresses the simulated revenue gap on
the measured flip rate.  The analytic prediction from analytic_gap.py is
carried alongside so the simulation can be checked against it.
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from run_sim import evaluate  # noqa: E402
from rb_common import OUT, MODELS, SHORT  # noqa: E402

Q3 = ["MMLU", "HellaSwag", "GSM8K"]
Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=5)
    ap.add_argument("--alpha", default="a0.50")
    ap.add_argument("--set", default="Q3")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    fams = Q3 if a.set == "Q3" else Q7
    names = sorted(SHORT[m] for m in MODELS)
    tris = [t for j, t in enumerate(itertools.combinations(names, 3))
            if j % a.nshards == a.shard]
    rows = []
    for tri in tris:
        inst, p, gm, av = I.finite_instance(list(tri), fams, a.alpha)
        tm = I.top_masks(inst)
        rec = {"models": "|".join(tri), "context_set": a.set, "alpha": a.alpha,
               "n": a.n, "nseeds": a.nseeds}
        for mech in ("plmesp", "mesp_scalar"):
            revs = [evaluate(mech, inst, p, a.n, s, ["proposed"] * 3, tm)
                    for s in range(a.nseeds)]
            rec[f"rev_{mech}"] = float(np.mean([r["revenue_per_round"] for r in revs]))
            rec[f"revsd_{mech}"] = float(np.std([r["revenue_per_round"] for r in revs]))
            rec[f"conv_{mech}"] = float(np.mean([r["convictions"] for r in revs]))
        rec["oracle"] = revs[-1]["oracle"]
        rec["second_cap"] = revs[-1]["second_cap"]
        rec["sim_gap"] = rec["rev_plmesp"] - rec["rev_mesp_scalar"]
        rows.append(rec)
        print(rec, flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
