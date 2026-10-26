"""Does the contextual mechanism's revenue advantage appear at a REACHABLE horizon?

The analytic gap of analytic_gap.py ignores the sublinear overheads.  The
profile-local mechanism pays an elicitation block inside EVERY context, so its
overhead is Q times the scalar mechanism's, and at a small horizon that
overhead can be larger than the gap it buys.  This sweeps the horizon so the
crossover can be located rather than assumed.
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import design_constants  # noqa: E402
from run_sim import evaluate  # noqa: E402
from rb_common import MODELS, SHORT  # noqa: E402

Q3 = ["MMLU", "HellaSwag", "GSM8K"]
Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", default="300000,1000000,3000000,10000000")
    ap.add_argument("--nseeds", type=int, default=5)
    ap.add_argument("--alpha", default="a0.50")
    ap.add_argument("--set", default="Q3")
    ap.add_argument("--triples", default="selected")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    fams = Q3 if a.set == "Q3" else Q7
    if a.triples == "selected":
        from select_triples import flip_rate_table, pick
        tris = [tuple(v.split("|")) for v in pick(flip_rate_table(fams)).values()]
    else:
        names = sorted(SHORT[m] for m in MODELS)
        tris = list(itertools.combinations(names, 3))
    tris = [t for j, t in enumerate(tris) if j % a.nshards == a.shard]
    rows = []
    for tri in tris:
        inst, p, gm, av = I.finite_instance(list(tri), fams, a.alpha)
        tm = I.top_masks(inst)
        for n in [int(x) for x in a.ns.split(",")]:
            L, s, _ = design_constants(n, inst.K)
            rec = {"models": "|".join(tri), "context_set": a.set, "alpha": a.alpha,
                   "n": n, "nseeds": a.nseeds, "L_n": L, "s_n": s,
                   "elicit_frac_contextual": inst.K * inst.Q * L / n,
                   "elicit_frac_scalar": inst.K * L / n}
            for mech in ("plmesp", "mesp_scalar"):
                res = [evaluate(mech, inst, p, n, sd, ["proposed"] * 3, tm)
                       for sd in range(a.nseeds)]
                rec[f"rev_{mech}"] = float(np.mean([r["revenue_per_round"] for r in res]))
                rec[f"revsd_{mech}"] = float(np.std([r["revenue_per_round"] for r in res]))
                rec[f"compconv_{mech}"] = float(np.mean(
                    [r["compliant_convictions"] for r in res]))
                rec[f"conv_{mech}"] = float(np.mean([r["convictions"] for r in res]))
                rec[f"priceabovecap_{mech}"] = float(np.mean(
                    [r["primary_rounds_price_above_capability"] for r in res])) / n
            rec["oracle"] = res[-1]["oracle"]
            rec["second_cap"] = res[-1]["second_cap"]
            rec["honest_bench"] = res[-1]["honest_bench"]
            rec["sim_gap"] = rec["rev_plmesp"] - rec["rev_mesp_scalar"]
            rows.append(rec)
            print(rec, flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
