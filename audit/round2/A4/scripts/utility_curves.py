"""UTILITY AGAINST EFFORT, PER ARM ROLE. The mechanism seen from the agent's side.

For a fixed instance and a fixed single context, with every other provider held
at the proposed profile, one provider's DELIVERED MEAN is swept across its whole
feasible range and ITS OWN utility per round is recorded, once per rule.

Three roles, each with a prediction that can fail:

  top        Under the monitored second price the curve should rise to the
             announced price and then turn DOWN, because effort past the price
             buys no further selections and costs real compute. The kink should
             sit at the price. FALSIFIER: a peak strictly below the agent's own
             capability when the price is at or below that capability would
             contradict the incentive claim. Under a quality-estimating router
             the peak should sit just above the runner-up's capability.

  runner-up  Under the monitored second price this agent sets the price but does
             not win the primary phase, so its entire stake in its own elicited
             value is sublinear elicitation effort and the curve should be
             nearly FLAT. That flatness IS the mechanism of the revenue collapse
             that Theorem `thm:equilibrium-set` predicts. FALSIFIER: if it is
             not flat under a unique top capability, the equilibrium
             characterisation is wrong.

  third      Wins nothing under any rule, so the curve should be flat or
             declining. This is the sanity check on the axes.

The runner-up is also run on a CONSTRUCTED two-top instance, in which a real
model's capability function is duplicated as a second provider so that two
agents attain the top capability exactly. That instance is CONSTRUCTED, NOT
MEASURED, and every output row says so.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import (Instance, MechanismRun, ProfileStrategy,  # noqa: E402
                        run_router)
from rb_common import MODELS, SHORT  # noqa: E402

RULES = ["mesp", "router_greedy", "router_eps", "router_ucb"]


def single_context_instance(models, context, alpha_tag, duplicate_top=False):
    inst, p, gm, av = I.finite_instance(models, [context], alpha_tag)
    M = inst.M.copy()
    mu = inst.mu.copy()
    names = list(models)
    if duplicate_top:
        j = int(M[0].argmax())
        M = np.concatenate([M, M[:, [j]]], axis=1)
        mu = np.concatenate([mu, mu[:, [j]]], axis=1)
        names = names + [names[j] + " (duplicate)"]
    honest = np.zeros(M.shape[1], dtype=bool)
    honest[int(M[0].argmin())] = True
    return Instance(M=M, mu=mu, key=np.zeros(1, dtype=np.int64), honest=honest,
                    names=names), names


def run_rule(rule, inst, n, seed, strat, qs):
    if rule == "mesp":
        run = MechanismRun(inst, n, seed)
        r = run.run(strat, qs)
        # did this agent win the elicitation?  With one context there is one
        # local instance, so this is a single 0/1 event per seed, and its mean
        # over seeds is the win probability the curve is averaging over.
        r["winner"] = next((lo.W for lo in run.locals.values()
                            if lo.phase != "elicit"), -1)
    else:
        rl = {"router_greedy": "greedy", "router_eps": "epsgreedy",
              "router_ucb": "ucb"}[rule]
        r = run_router(inst, n, seed, strat, qs, rule=rl)
    r["utility_per_round"] = (r["T"] - r["C"]) / n
    r["selection_share"] = r["T"] / n
    r.setdefault("winner", -1)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200000)
    ap.add_argument("--nseeds", type=int, default=8)
    ap.add_argument("--grid", type=int, default=41)
    ap.add_argument("--alpha", default="a0.50")
    ap.add_argument("--contexts", default="MMLU,GSM8K")
    ap.add_argument("--sweep", default="all,primary",
                    help="all = deliver the swept mean in EVERY phase; "
                         "primary = bid the capability and sweep only the "
                         "primary delivery, which is where the mechanism's "
                         "incentive property lives.  Routers have no primary "
                         "phase, so only 'all' is defined for them.")
    ap.add_argument("--roles", default="top,runner_up,third")
    ap.add_argument("--rules", default=",".join(RULES))
    ap.add_argument("--dups", default="0,1",
                    help="0 = the measured instance, 1 = the CONSTRUCTED two-top one")
    ap.add_argument("--crosscheck", type=int, default=1)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    # MMLU: the global order holds (GPT-4 top).  GSM8K: the ranking flips
    # (Claude-V2 is top there and near the bottom on HellaSwag).
    models = ["GPT-4", "Claude-V2", "Mistral-7B"]
    want_dups = tuple(bool(int(x)) for x in a.dups.split(","))
    want_roles = a.roles.split(",")
    want_rules = [r for r in RULES if r in a.rules.split(",")]
    jobs = []
    for ctx in a.contexts.split(","):
        for dup in want_dups:
            jobs.append((ctx, dup))
    jobs = [j for k, j in enumerate(jobs) if k % a.nshards == a.shard]
    rows = []
    for ctx, dup in jobs:
        inst, names = single_context_instance(models, ctx, a.alpha, duplicate_top=dup)
        K = inst.K
        M0, mu0 = inst.M[0], inst.mu[0]
        order = list(np.argsort(-M0))
        roles = {k: v for k, v in
                 (("top", order[0]), ("runner_up", order[1]), ("third", order[2]))
                 if k in want_roles}
        srt = np.sort(M0)
        second_cap = float(srt[-2])
        qs = np.zeros(a.n, dtype=int)
        second = np.sort(inst.M, axis=1)[:, -2]
        tm = I.top_masks(inst)
        # the announced price the mechanism actually reaches at the proposed profile
        taus = []
        for s in range(a.nseeds):
            run = MechanismRun(inst, a.n, s)
            run.run(ProfileStrategy(inst, ["proposed"] * K, tm, second=second), qs)
            taus += [lo.tau for lo in run.locals.values() if lo.phase != "elicit"]
        tau_mean = float(np.mean(taus)) if taus else np.nan
        for role, i in roles.items():
            grid = np.linspace(float(mu0[i]), float(M0[i]), a.grid)
            for sweep in a.sweep.split(","):
              for rule in want_rules:
                if sweep == "primary" and rule != "mesp":
                    continue          # routers have no primary phase
                for m in grid:
                    opts = ["proposed"] * K
                    opts[i] = (f"fixed{m:.6f}" if sweep == "all"
                               else f"primaryfixed{m:.6f}")
                    us, rv, wins, sels = [], [], [], []
                    for s in range(a.nseeds):
                        st = ProfileStrategy(inst, opts, tm, second=second)
                        r = run_rule(rule, inst, a.n, s, st, qs)
                        us.append(r["utility_per_round"][i])
                        rv.append(r["revenue_per_round"])
                        wins.append(1.0 if r["winner"] == i else 0.0)
                        sels.append(r["selection_share"][i])
                    rows.append({
                        "context": ctx, "sweep": sweep,
                        "instance": "two_top_CONSTRUCTED" if dup
                        else "measured_unique_top",
                        "alpha": a.alpha, "n": a.n, "nseeds": a.nseeds,
                        "rule": rule, "role": role, "agent": names[i],
                        "delivered_mean": float(m),
                        "own_capability": float(M0[i]),
                        "own_intrinsic": float(mu0[i]),
                        "runner_up_capability": second_cap,
                        "announced_price_mean": tau_mean,
                        "agent_utility_per_round": float(np.mean(us)),
                        "agent_utility_sd": float(np.std(us)),
                        "win_probability": float(np.mean(wins)),
                        "selection_share": float(np.mean(sels)),
                        "platform_revenue_per_round": float(np.mean(rv))})
                # write after every completed block, so a task that runs out
                # of wall clock still leaves everything it finished on disk
                pd.DataFrame(rows).to_csv(a.out, index=False)
                print(f"done {ctx} dup={dup} {role} {sweep} {rule} "
                      f"({len(rows)} rows written)", flush=True)
            # CONSISTENCY CHECK requested by the paper's author: the height of
            # the top agent's peak above its utility at full capability must
            # equal the per-round undercut gain computed by the separate
            # deviation code path.  Two independent implementations, one
            # number.
            for rule in (want_rules if a.crosscheck else []):
                for tag, opt in (("undercut0.02", "undercut0.02"),
                                 ("full_capability", "theta1.00")):
                    opts = ["proposed"] * K
                    opts[i] = opt
                    us = []
                    for s in range(a.nseeds):
                        st = ProfileStrategy(inst, opts, tm, second=second)
                        r = run_rule(rule, inst, a.n, s, st, qs)
                        us.append(r["utility_per_round"][i])
                    rows.append({
                        "context": ctx, "sweep": "crosscheck",
                        "instance": "two_top_CONSTRUCTED" if dup
                        else "measured_unique_top",
                        "alpha": a.alpha, "n": a.n, "nseeds": a.nseeds,
                        "rule": rule, "role": role, "agent": names[i],
                        "delivered_mean": np.nan, "crosscheck_option": tag,
                        "own_capability": float(M0[i]),
                        "own_intrinsic": float(mu0[i]),
                        "runner_up_capability": second_cap,
                        "announced_price_mean": tau_mean,
                        "agent_utility_per_round": float(np.mean(us)),
                        "agent_utility_sd": float(np.std(us)),
                        "platform_revenue_per_round": np.nan})
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
