"""BASELINE 1: the single-observation exclusion rule, run under OUR model.

Esmaeili et al. (AAAI 2025, DOI 10.1609/aaai.v39i13.33510, arXiv:2403.15115)
give a private-capacity mechanism that elicits a bid with ONE pull per agent,
announces the second-highest bid as the price, and excludes an agent whose
delivery falls below it. In THEIR setting the selected agent observes and edits
its realised reward before the platform sees it, so one pull certifies the bid
and the rule is correct.

THIS SCRIPT RUNS THEIR RULE UNDER THIS PAPER'S NOISY-DELIVERY MODEL, where the
agent fixes a target before a fresh Bernoulli draw. IT IS NOT A REPRODUCTION OF
THEIR RESULTS IN THEIR OWN SETTING, and nothing here is evidence that their
mechanism is wrong; it is solving a different problem. The comparison is the
measured form of Theorem `thm:separation`.

Axes, the same as everything else in this package: revenue per round, the rate
at which a FULLY COMPLIANT winner is excluded, and the best deviation found.
"""
import argparse
import itertools
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import (MechanismRun, ProfileStrategy,  # noqa: E402
                        honest_benchmark_per_round, oracle_per_round,
                        run_single_observation_exclusion,
                        second_capability_per_round)
from rb_common import MODELS, SHORT  # noqa: E402
from run_sim import draw_queries  # noqa: E402

Q3 = ["MMLU", "HellaSwag", "GSM8K"]
Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]
DEVIATIONS = ["proposed", "theta0.00", "theta0.50", "theta0.90", "selective",
              "undercut0.02"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=30)
    ap.add_argument("--set", default="Q7")
    ap.add_argument("--alphas", default="a0.00,a0.25,a0.50,a0.75,het")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    fams = Q3 if a.set == "Q3" else Q7
    from select_triples import flip_rate_table, pick
    tris = pick(flip_rate_table(fams))
    tris["dominant"] = "|".join(["GPT-4", "Yi-34B", "Mistral-7B"])
    rows = []
    jobs = [(lab, al) for lab in tris for al in a.alphas.split(",")]
    jobs = [j for k, j in enumerate(jobs) if k % a.nshards == a.shard]
    for lab, al in jobs:
        mstr = tris[lab]
        models = mstr.split("|")
        if True:
            inst, p, gm, av = I.finite_instance(models, fams, al)
            tm = I.top_masks(inst)
            second = np.sort(inst.M, axis=1)[:, -2]
            base = {"context_set": a.set, "triple": lab, "models": mstr, "alpha": al,
                    "n": a.n, "nseeds": a.nseeds}
            for L in (1, 2, 5, 20, 100):
                for empty in ("stop", "roundrobin"):
                    for dev in DEVIATIONS:
                        for devi in ([None] if dev == "proposed" else range(inst.K)):
                            opts = ["proposed"] * inst.K
                            if devi is not None:
                                opts[devi] = dev
                            res = []
                            for s in range(a.nseeds):
                                qs = draw_queries(inst, p, a.n, s)
                                st = ProfileStrategy(inst, opts, tm, second=second)
                                res.append(run_single_observation_exclusion(
                                    inst, a.n, s, st, qs, L_elicit=L, empty=empty))
                            u = np.mean([r["utility_per_round"] for r in res], axis=0)
                            qs0 = draw_queries(inst, p, a.n, 0)
                            rows.append({
                                **base, "rule": "single_observation_exclusion",
                                "L_elicit": L, "empty_policy": empty,
                                "deviation": dev, "deviator_index": devi,
                                "deviator": models[devi] if devi is not None else "",
                                "revenue_per_round": float(np.mean(
                                    [r["revenue_per_round"] for r in res])),
                                "compliant_exclusions": float(np.mean(
                                    [r["compliant_exclusions"] for r in res])),
                                "exclusions": float(np.mean(
                                    [r["exclusions"] for r in res])),
                                "idle_fraction": float(np.mean(
                                    [r["idle_rounds"] for r in res])) / a.n,
                                "announced_price_mean": float(np.mean(
                                    [r["announced_price"] for r in res])),
                                "price_is_one_share": float(np.mean(
                                    [r["announced_price"] >= 1.0 - 1e-9 for r in res])),
                                "price_is_zero_share": float(np.mean(
                                    [r["announced_price"] <= 1e-9 for r in res])),
                                "oracle": oracle_per_round(inst, qs0),
                                "second_cap": second_capability_per_round(inst, qs0),
                                "honest_bench": honest_benchmark_per_round(inst, qs0),
                                **{f"util_{j}": u[j] for j in range(inst.K)}})
            # the monitored second price on the SAME instance, for the comparison
            for dev in DEVIATIONS:
                for devi in ([None] if dev == "proposed" else range(inst.K)):
                    opts = ["proposed"] * inst.K
                    if devi is not None:
                        opts[devi] = dev
                    res = []
                    for s in range(a.nseeds):
                        qs = draw_queries(inst, p, a.n, s)
                        st = ProfileStrategy(inst, opts, tm, second=second)
                        res.append(MechanismRun(inst, a.n, s).run(st, qs))
                    u = np.mean([r["utility_per_round"] for r in res], axis=0)
                    qs0 = draw_queries(inst, p, a.n, 0)
                    rows.append({
                        **base, "rule": "plmesp", "L_elicit": -1,
                        "empty_policy": "", "deviation": dev, "deviator_index": devi,
                        "deviator": models[devi] if devi is not None else "",
                        "revenue_per_round": float(np.mean(
                            [r["revenue_per_round"] for r in res])),
                        "compliant_exclusions": float(np.mean(
                            [r["compliant_convictions"] for r in res])),
                        "exclusions": float(np.mean([r["convictions"] for r in res])),
                        "idle_fraction": 0.0, "announced_price_mean": np.nan,
                        "price_is_one_share": np.nan, "price_is_zero_share": np.nan,
                        "oracle": oracle_per_round(inst, qs0),
                        "second_cap": second_capability_per_round(inst, qs0),
                        "honest_bench": honest_benchmark_per_round(inst, qs0),
                        **{f"util_{j}": u[j] for j in range(inst.K)}})
            print(f"done {lab} {al}", flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
