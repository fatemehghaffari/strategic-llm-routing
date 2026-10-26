"""IS THE TWO-TOP CONDITION A CLIFF AT ZERO, OR A GRADED TRANSITION AT THE SHADING SCALE?

Theorem `thm:equilibrium-set` states its condition as EXACT equality of the top
two capabilities, but the mechanism shades its announced price anyway, by s_n
for the finite-context mechanism and by 3 s_n + rho_n for the continuum one.
So the binding quantity should not be whether the gap is zero but whether the
gap is small RELATIVE TO THAT SHADING: if the runner-up can still win the
elicitation, it keeps a stake in its own elicited value and the price holds up;
if it cannot win under any bid it becomes indifferent, shades, and the price
collapses.

CONSTRUCTION, and it is CONSTRUCTED rather than measured. Take a real triple
from the measured capability table, keep the top provider and the third
provider exactly as measured, and replace the runner-up's capability function
by `M_top(z) - delta` at every context, so the top-to-second gap is exactly
`delta` everywhere. `delta = 0` is then the instance in which one real model's
capability function is DUPLICATED as a second provider, which is not artificial:
two vendors serving the same open-weight model, or one model behind two
regions, are tied by construction.

For each delta we report the equilibrium revenue reached by best-response
iteration over the rich option class, the mean announced price, and the
runner-up's utility-against-effort curve with its total variation, since the
flatness of that curve IS the indifference that causes the collapse.
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import (RICH_OPTIONS, Instance, MechanismRun,  # noqa: E402
                        ProfileStrategy, design_constants,
                        honest_benchmark_per_round, oracle_per_round,
                        second_capability_per_round)
import run_sim  # noqa: E402

Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


def build(models, fams, alpha_tag, delta):
    """Real top and third; runner-up pinned at M_top - delta everywhere."""
    inst, p, gm, av = I.finite_instance(models, fams, alpha_tag)
    M = inst.M.copy()
    order = np.argsort(-(M * p[:, None]).sum(axis=0))
    top, run, third = (int(order[0]), int(order[1]), int(order[2]))
    M[:, run] = np.clip(M[:, top] - delta, 0.01, 1.0)
    alpha = inst.mu / np.maximum(inst.M, 1e-12)      # keep the same alpha vector
    mu = alpha * M
    honest = np.zeros(M.shape[1], dtype=bool)
    honest[int(np.argmin((M * p[:, None]).sum(axis=0)))] = True
    return (Instance(M=M, mu=mu, key=inst.key, honest=honest, names=list(models)),
            p, top, run, third)


def evaluate(mech, inst, p, n, seeds, options, tm, second):
    revs, utils, taus = [], [], []
    for s in seeds:
        qs = run_sim.draw_queries(inst, p, n, s)
        st = ProfileStrategy(inst, options, tm, second=second)
        if mech == "plmesp":
            run = MechanismRun(inst, n, s)
            r = run.run(st, qs)
            taus += [lo.tau for lo in run.locals.values() if lo.phase != "elicit"]
        else:
            r = run_sim.evaluate_with(mech, inst, p, n, s, st)
        r["utility_per_round"] = (r["T"] - r["C"]) / n
        revs.append(r["revenue_per_round"])
        utils.append(r["utility_per_round"])
    return (float(np.mean(revs)), np.mean(utils, axis=0),
            float(np.mean(taus)) if taus else np.nan)


def best_response(mech, inst, p, n, seeds, tm, second, sweeps=3):
    cur = ["theta1.00"] * inst.K
    for _ in range(sweeps):
        changed = False
        for i in range(inst.K):
            bu, bo = -np.inf, cur[i]
            for o in RICH_OPTIONS:
                t = list(cur)
                t[i] = o
                _, u, _ = evaluate(mech, inst, p, n, seeds, t, tm, second)
                if u[i] > bu + 1e-9:
                    bu, bo = u[i], o
            if bo != cur[i]:
                changed = True
            cur[i] = bo
        if not changed:
            return cur, True
    return cur, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--br-seeds", type=int, default=4)
    ap.add_argument("--eval-seeds", type=int, default=10)
    ap.add_argument("--curve-grid", type=int, default=21)
    ap.add_argument("--curve-seeds", type=int, default=6)
    ap.add_argument("--alpha", default="a0.50")
    ap.add_argument("--models", default="GPT-4|Claude-V2|Mistral-7B")
    ap.add_argument("--deltas",
                    default="0,0.001,0.002,0.005,0.0075,0.01,0.015,0.02,0.03,0.05,0.1,0.2,0.4")
    ap.add_argument("--mechs", default="plmesp,mesp_scalar")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    models = a.models.split("|")
    deltas = [float(x) for x in a.deltas.split(",")]
    deltas = [d for k, d in enumerate(deltas) if k % a.nshards == a.shard]
    L, s_n, _ = design_constants(a.n, len(models))
    rows = []
    for delta in deltas:
        inst, p, top, run, third = build(models, Q7, a.alpha, delta)
        tm = I.top_masks(inst)
        second = np.sort(inst.M, axis=1)[:, -2]
        qs0 = run_sim.draw_queries(inst, p, a.n, 0)
        base = {"delta": delta, "n": a.n, "alpha": a.alpha,
                "models": a.models, "instance": "CONSTRUCTED",
                "construction": ("runner-up capability pinned at M_top - delta; "
                                 "delta = 0 duplicates the top model's capability "
                                 "function as a second provider"),
                "L_n": L, "s_n": s_n, "shading_finite_s_n": s_n,
                "sd_of_bid_difference": float(0.5 * np.sqrt(2.0 / L)),
                "oracle": oracle_per_round(inst, qs0),
                "second_cap": second_capability_per_round(inst, qs0),
                "honest_bench": honest_benchmark_per_round(inst, qs0),
                "top_agent": models[top], "runner_up_agent": models[run]}
        for mech in a.mechs.split(","):
            prof, fixed = best_response(mech, inst, p, a.n, list(range(a.br_seeds)),
                                        tm, second)
            rev, u, tau = evaluate(mech, inst, p, a.n, list(range(a.eval_seeds)),
                                   prof, tm, second)
            rev_pr, u_pr, tau_pr = evaluate(mech, inst, p, a.n,
                                            list(range(a.eval_seeds)),
                                            ["proposed"] * inst.K, tm, second)
            # the runner-up's utility against effort, primary sweep
            lo_, hi_ = float(inst.mu[:, run].min()), float(inst.M[:, run].max())
            grid = np.linspace(lo_, hi_, a.curve_grid)
            cu = []
            for m in grid:
                o = ["proposed"] * inst.K
                o[run] = f"primaryfixed{m:.6f}"
                _, uu, _ = evaluate(mech, inst, p, a.n,
                                    list(range(a.curve_seeds)), o, tm, second)
                cu.append(float(uu[run]))
            cu = np.asarray(cu)
            rows.append({**base, "mech": mech,
                         "equilibrium_profile": "|".join(prof),
                         "is_fixed_point": fixed,
                         "equilibrium_revenue": rev,
                         "revenue_at_proposed": rev_pr,
                         "announced_price_mean": tau_pr,
                         "runner_up_curve_total_variation": float(
                             np.abs(np.diff(cu)).sum()),
                         "runner_up_curve_range": float(cu.max() - cu.min()),
                         "runner_up_curve": json.dumps([round(float(x), 6) for x in cu]),
                         "runner_up_curve_grid": json.dumps(
                             [round(float(x), 6) for x in grid]),
                         **{f"util_{j}": u[j] for j in range(inst.K)}})
            print(f"delta={delta} {mech} rev {rev:.4f} (proposed {rev_pr:.4f}) "
                  f"tau {tau_pr:.4f} TV {rows[-1]['runner_up_curve_total_variation']:.4f} "
                  f"prof {'|'.join(prof)}", flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
