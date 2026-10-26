"""THE FAIR STRATEGIC COMPARISON: best response over the SAME RICH option class
for every rule.

The coarse option class used in the first headline grid cannot express the
deviation a quality-estimating router is vulnerable to, so a best response
computed over it attacks each rule only where that rule happens to be weak, and
the router's clean sheet there is a property of the option set rather than of
the router. This script reruns the best-response dynamics for EVERY rule over
`mechanisms.RICH_OPTIONS`, which adds a fine theta grid near 1 and the undercut
family, and verifies whether the profile reached is a fixed point.

Non-strategic revenue is reported beside it, so both halves of the claim are in
one table.
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import RICH_OPTIONS, ProfileStrategy  # noqa: E402
import run_sim  # noqa: E402

Q3 = ["MMLU", "HellaSwag", "GSM8K"]
Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


def evaluate(mech, inst, p, n, seeds, options, tm, second):
    revs, utils, conv = [], [], []
    for s in seeds:
        st = ProfileStrategy(inst, options, tm, second=second)
        r = run_sim.evaluate_with(mech, inst, p, n, s, st)
        revs.append(r["revenue_per_round"])
        utils.append(r["utility_per_round"])
        conv.append(r.get("compliant_convictions", 0))
    return float(np.mean(revs)), np.mean(utils, axis=0), float(np.mean(conv))


def best_response(mech, inst, p, n, seeds, tm, second, start, sweeps=3):
    cur = list(start)
    trace = []
    for sw in range(sweeps):
        changed = False
        for i in range(inst.K):
            bu, bo = -np.inf, cur[i]
            for o in RICH_OPTIONS:
                trial = list(cur)
                trial[i] = o
                _, u, _ = evaluate(mech, inst, p, n, seeds, trial, tm, second)
                if u[i] > bu + 1e-9:
                    bu, bo = u[i], o
            if bo != cur[i]:
                changed = True
            cur[i] = bo
        trace.append(list(cur))
        if not changed:
            return cur, True, sw + 1, trace
    return cur, False, sweeps, trace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=6)
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
    jobs = [(lab, al) for lab in tris for al in a.alphas.split(",")]
    jobs = [j for k, j in enumerate(jobs) if k % a.nshards == a.shard]
    seeds = list(range(a.nseeds))
    rows = []
    for lab, al in jobs:
        models = tris[lab].split("|")
        inst, p, gm, av = I.finite_instance(models, fams, al)
        tm = I.top_masks(inst)
        second = np.sort(inst.M, axis=1)[:, -2]
        qs0 = run_sim.draw_queries(inst, p, a.n, 0)
        from mechanisms import (honest_benchmark_per_round, oracle_per_round,
                                second_capability_per_round)
        base = {"context_set": a.set, "triple": lab, "models": "|".join(models),
                "alpha": al, "n": a.n, "nseeds": a.nseeds,
                "honest_agent": models[int(np.flatnonzero(inst.honest)[0])],
                "oracle": oracle_per_round(inst, qs0),
                "second_cap": second_capability_per_round(inst, qs0),
                "honest_bench": honest_benchmark_per_round(inst, qs0)}
        for mech in run_sim.MECHS:
            ns_opts = ["theta1.00"] * inst.K
            ns_rev, ns_u, _ = evaluate(mech, inst, p, a.n, seeds, ns_opts, tm, second)
            fin, fixed, sw, trace = best_response(mech, inst, p, a.n, seeds, tm,
                                                  second, ns_opts)
            st_rev, st_u, st_cc = evaluate(mech, inst, p, a.n, seeds, fin, tm, second)
            rows.append({**base, "mech": mech,
                         "nonstrategic_revenue": ns_rev,
                         "strategic_revenue": st_rev,
                         "degradation": ns_rev - st_rev,
                         "profile": "|".join(fin), "is_fixed_point": fixed,
                         "br_sweeps": sw, "br_trace": json.dumps(trace),
                         "compliant_convictions": st_cc,
                         **{f"util_{j}": st_u[j] for j in range(inst.K)},
                         **{f"ns_util_{j}": ns_u[j] for j in range(inst.K)}})
            print(f"done {lab} {al} {mech} -> {'|'.join(fin)} "
                  f"rev {ns_rev:.4f} -> {st_rev:.4f}", flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
