"""Does a quality-estimating router really survive strategic providers, or was
the coarse deviation grid hiding the deviation that matters?

The headline grid lets a provider choose theta in {0, .25, .5, .75, 1}, and its
smallest shading step may be far too large to stay pointwise best.  The exact
best response against a rule that routes to the estimated best provider is not
a constant fraction: it is to deliver just enough to remain best,

    m_i(x) = max( mu_i(x), min(M_i(x), M_(2)(x) + eps) ),

which keeps the provider pointwise top by eps and banks M_i(x) - M_(2)(x) - eps
of effort on every selection.  This is exactly the deviation the paper's
two-top condition is introduced to rule out, so it is the right test.

This script sweeps eps and a fine theta grid near 1, one deviator at a time,
against every mechanism.  Everyone else plays the proposed profile.
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import ProfileStrategy  # noqa: E402
from rb_common import MODELS, SHORT  # noqa: E402
import run_sim  # noqa: E402

Q3 = ["MMLU", "HellaSwag", "GSM8K"]
Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


class FineStrategy(ProfileStrategy):
    """One deviator; everyone else plays the proposed profile."""

    def __init__(self, inst, dev, kind, param, second):
        super().__init__(inst, ["proposed"] * inst.K, None)
        self.dev, self.kind, self.param, self.second = dev, kind, param, second

    def target(self, i, phase, q, price, state=None):
        inst = self.inst
        M, mu = inst.M[q, i], inst.mu[q, i]
        if i != self.dev:
            if phase == "primary" and price is not None:
                m = min(price, M)
                return max(mu, m) if inst.honest[i] else m
            return M
        if self.kind == "theta":
            return mu + self.param * (M - mu)
        if self.kind == "undercut":
            # deliver just enough to stay pointwise best
            return float(np.clip(self.second[q] + self.param, mu if inst.honest[i] else 0.0, M))
        raise ValueError(self.kind)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=10)
    ap.add_argument("--set", default="Q7")
    ap.add_argument("--alphas", default="a0.00,a0.25,a0.50,a0.75,het")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    fams = Q3 if a.set == "Q3" else Q7
    from select_triples import flip_rate_table, pick
    tris = pick(flip_rate_table(fams))
    # a triple containing the globally dominant model, so that a UNIQUELY top
    # provider exists on most contexts, which is the case the two-top condition
    # is about
    names = sorted(SHORT[m] for m in MODELS)
    tris["dominant"] = "|".join(["GPT-4", "Yi-34B", "Mistral-7B"])
    jobs = [(lab, al) for lab in tris for al in a.alphas.split(",")]
    jobs = [j for k, j in enumerate(jobs) if k % a.nshards == a.shard]
    rows = []
    for lab, al in jobs:
        models = tris[lab].split("|")
        inst, p, gm, av = I.finite_instance(models, fams, al)
        second = np.sort(inst.M, axis=1)[:, -2]
        top_mass = float(p[(inst.M.argmax(axis=1) == int(inst.M.mean(axis=0).argmax()))].sum())
        base = {"context_set": a.set, "triple": lab, "models": "|".join(models),
                "alpha": al, "n": a.n, "nseeds": a.nseeds,
                "mass_where_global_best_is_pointwise_best": top_mass}
        for mech in run_sim.MECHS:
            # baseline: everyone plays the proposed profile
            b = [run_sim.evaluate(mech, inst, p, a.n, s, ["proposed"] * inst.K, None)
                 for s in range(a.nseeds)]
            bu = np.mean([r["utility_per_round"] for r in b], axis=0)
            brev = float(np.mean([r["revenue_per_round"] for r in b]))
            for dev in range(inst.K):
                for kind, param in ([("theta", t) for t in (0.90, 0.95, 0.975, 0.99)]
                                    + [("undercut", e) for e in (0.0, 0.005, 0.02, 0.05)]):
                    st = FineStrategy(inst, dev, kind, param, second)
                    res = [run_sim.evaluate_with(mech, inst, p, a.n, s, st)
                           for s in range(a.nseeds)]
                    u = np.mean([r["utility_per_round"] for r in res], axis=0)
                    rows.append({**base, "mech": mech, "deviator": models[dev],
                                 "deviation_kind": kind, "deviation_param": param,
                                 "gain_per_round": float(u[dev] - bu[dev]),
                                 "revenue_per_round": float(np.mean(
                                     [r["revenue_per_round"] for r in res])),
                                 "baseline_revenue_per_round": brev,
                                 "revenue_loss_per_round": brev - float(np.mean(
                                     [r["revenue_per_round"] for r in res])),
                                 "oracle": res[-1]["oracle"],
                                 "second_cap": res[-1]["second_cap"],
                                 "honest_bench": res[-1]["honest_bench"],
                                 "compliant_convictions": float(np.mean(
                                     [r["compliant_convictions"] for r in res]))})
            print(f"done {lab} {al} {mech}", flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
