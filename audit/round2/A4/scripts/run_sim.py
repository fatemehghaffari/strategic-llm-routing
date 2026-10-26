"""Step 4: the headline comparison, as a CALIBRATED SIMULATION.

Capabilities are MEASURED from RouterBench.  Strategic behaviour is SIMULATED.
Nothing here is evidence that any real provider behaves strategically.

Two worlds, run for every mechanism:
  NON-STRATEGIC  every provider always delivers its measured capability.
  STRATEGIC      every provider picks the option in the declared stationary
                 class that maximises its own utility, found by best-response
                 iteration from the non-strategic profile.

Mechanisms: PL-MESP / CG-MESP, MESP (scalar), and a quality-estimating router
(greedy / epsilon-greedy / UCB) of the kind used in the routing literature.
The router is a POLICY CLASS; it is not a reimplementation of, and no result
here is a benchmark of, any published routing system.
"""
import argparse
import copy
import itertools
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import (OPTIONS, Instance, MechanismRun, ProfileStrategy,  # noqa: E402
                        honest_benchmark_per_round, oracle_per_round,
                        run_router, second_capability_per_round)
from rb_common import MODELS, OUT, SHORT  # noqa: E402

NAMES = [SHORT[m] for m in MODELS]
MECHS = ["plmesp", "mesp_scalar", "router_greedy", "router_eps", "router_ucb"]


def draw_queries(inst, p, n, seed):
    rng = np.random.default_rng(1000003 + seed)
    if p is None:
        return rng.integers(0, inst.M.shape[0], size=n)
    return rng.choice(len(p), size=n, p=p)


def scalarize(inst):
    """The same instance presented to a mechanism that sees no context."""
    return Instance(M=inst.M, mu=inst.mu, key=np.zeros_like(inst.key),
                    honest=inst.honest, names=inst.names)


def evaluate(mech, inst, p, n, seed, options, tm, monitor="anytime",
             price_shade=0.0, L_override=None):
    qs = draw_queries(inst, p, n, seed)
    strat = ProfileStrategy(inst, options, tm)
    if mech == "plmesp":
        r = MechanismRun(inst, n, seed, price_shade=price_shade, monitor=monitor,
                         L_override=L_override).run(strat, qs)
    elif mech == "mesp_scalar":
        si = scalarize(inst)
        r = MechanismRun(si, n, seed, monitor=monitor).run(ProfileStrategy(si, options, tm), qs)
    elif mech.startswith("router"):
        rule = {"router_greedy": "greedy", "router_eps": "epsgreedy",
                "router_ucb": "ucb"}[mech]
        r = run_router(inst, n, seed, strat, qs, rule=rule)
        r.setdefault("phase_rounds", {})
        r.setdefault("convictions", 0)
        r.setdefault("compliant_convictions", 0)
        r.setdefault("primary_rounds_price_above_capability", 0)
        r.setdefault("n_locals", inst.Q)
        r.setdefault("n_locals_past_elicitation", inst.Q)
        r.setdefault("revenue_realized", -1)
    else:
        raise ValueError(mech)
    r["utility_per_round"] = (r["T"] - r["C"]) / n
    r["oracle"] = oracle_per_round(inst, qs)
    r["second_cap"] = second_capability_per_round(inst, qs)
    r["honest_bench"] = honest_benchmark_per_round(inst, qs)
    return r


def evaluate_with(mech, inst, p, n, seed, strat, monitor="anytime",
                  price_shade=0.0, L_override=None):
    """Same as evaluate() but takes an already-built strategy object."""
    qs = draw_queries(inst, p, n, seed)
    if mech == "plmesp":
        r = MechanismRun(inst, n, seed, price_shade=price_shade, monitor=monitor,
                         L_override=L_override).run(strat, qs)
    elif mech == "mesp_scalar":
        si = scalarize(inst)
        strat2 = copy.copy(strat)
        strat2.inst = si
        r = MechanismRun(si, n, seed, monitor=monitor).run(strat2, qs)
    elif mech.startswith("router"):
        rule = {"router_greedy": "greedy", "router_eps": "epsgreedy",
                "router_ucb": "ucb"}[mech]
        r = run_router(inst, n, seed, strat, qs, rule=rule)
        r.setdefault("convictions", 0)
        r.setdefault("compliant_convictions", 0)
        r.setdefault("revenue_realized", -1)
    else:
        raise ValueError(mech)
    r["utility_per_round"] = (r["T"] - r["C"]) / n
    r["oracle"] = oracle_per_round(inst, qs)
    r["second_cap"] = second_capability_per_round(inst, qs)
    r["honest_bench"] = honest_benchmark_per_round(inst, qs)
    return r


def mean_over_seeds(mech, inst, p, n, seeds, options, tm, **kw):
    revs, utils = [], []
    extra = None
    for s in seeds:
        r = evaluate(mech, inst, p, n, s, options, tm, **kw)
        revs.append(r["revenue_per_round"])
        utils.append(r["utility_per_round"])
        extra = r
    return float(np.mean(revs)), np.mean(utils, axis=0), revs, extra


def best_response(mech, inst, p, n, seeds, tm, start, sweeps=3, **kw):
    """Best-response iteration in the declared option set, from `start`."""
    cur = list(start)
    trace = []
    for sweep in range(sweeps):
        changed = False
        for i in range(inst.K):
            best_u, best_o = -np.inf, cur[i]
            for o in OPTIONS:
                trial = list(cur)
                trial[i] = o
                _, u, _, _ = mean_over_seeds(mech, inst, p, n, seeds, trial, tm, **kw)
                if u[i] > best_u + 1e-9:
                    best_u, best_o = u[i], o
            if best_o != cur[i]:
                changed = True
            cur[i] = best_o
        trace.append(list(cur))
        if not changed:
            return cur, True, sweep + 1, trace
    return cur, False, sweeps, trace


def run_config(cfg, out_rows):
    t0 = time.time()
    models = cfg["models"]
    if cfg["kind"] == "finite":
        inst, p, gm, a = I.finite_instance(models, cfg["families"], cfg["alpha"],
                                           shot=cfg["shot"],
                                           uniform_mass=cfg.get("uniform_mass", False))
        kw, L_over, rho = {}, None, 0.0
    else:
        inst, gm, a, rho, meta = I.continuous_instance(
            models, cfg["alpha"], cfg["n"], d=cfg["d"], k=cfg["k"],
            rho_mode=cfg["rho_mode"])
        p = None
        L_over = I.cg_elicitation_length(cfg["n"], cfg["d"], inst.K)
        kw = {}
    tm = I.top_masks(inst)
    n, seeds = cfg["n"], list(range(cfg["nseeds"]))

    base = dict(cfg)
    base.pop("families", None)
    base["models"] = "|".join(models)
    base["honest_agent"] = models[int(np.flatnonzero(inst.honest)[0])]
    base["alpha_vector"] = "|".join(f"{x:.2f}" for x in a)
    base["n_contexts_instance"] = inst.Q
    base["rho_used"] = rho

    for mech in MECHS:
        mkw = dict(kw)
        if mech == "plmesp" and cfg["kind"] == "continuous":
            mkw = {"price_shade": rho, "L_override": L_over}
        # --- world 1: non-strategic ------------------------------------- #
        opts_ns = ["theta1.00"] * inst.K
        rev, util, revs, ex = mean_over_seeds(mech, inst, p, n, seeds, opts_ns, tm, **mkw)
        out_rows.append({**base, "mech": mech, "world": "nonstrategic",
                         "profile": "|".join(opts_ns), "is_fixed_point": True,
                         "revenue_per_round": rev, "revenue_sd": float(np.std(revs)),
                         "oracle": ex["oracle"], "second_cap": ex["second_cap"],
                         "honest_bench": ex["honest_bench"],
                         "convictions": ex["convictions"],
                         "compliant_convictions": ex["compliant_convictions"],
                         "locals_past_elicitation": ex["n_locals_past_elicitation"],
                         "locals_total": ex["n_locals"],
                         **{f"util_{j}": util[j] for j in range(inst.K)}})
        # --- world 1b: the paper's proposed profile ----------------------- #
        opts_pr = ["proposed"] * inst.K
        rev, util, revs, ex = mean_over_seeds(mech, inst, p, n, seeds, opts_pr, tm, **mkw)
        out_rows.append({**base, "mech": mech, "world": "proposed",
                         "profile": "|".join(opts_pr), "is_fixed_point": False,
                         "revenue_per_round": rev, "revenue_sd": float(np.std(revs)),
                         "oracle": ex["oracle"], "second_cap": ex["second_cap"],
                         "honest_bench": ex["honest_bench"],
                         "convictions": ex["convictions"],
                         "compliant_convictions": ex["compliant_convictions"],
                         "locals_past_elicitation": ex["n_locals_past_elicitation"],
                         "locals_total": ex["n_locals"],
                         **{f"util_{j}": util[j] for j in range(inst.K)}})
        # --- world 2: strategic, best response from non-strategic --------- #
        final, fixed, nsw, trace = best_response(mech, inst, p, n, seeds, tm,
                                                 opts_ns, **mkw)
        rev, util, revs, ex = mean_over_seeds(mech, inst, p, n, seeds, final, tm, **mkw)
        out_rows.append({**base, "mech": mech, "world": "strategic",
                         "profile": "|".join(final), "is_fixed_point": fixed,
                         "br_sweeps": nsw, "br_trace": json.dumps(trace),
                         "revenue_per_round": rev, "revenue_sd": float(np.std(revs)),
                         "oracle": ex["oracle"], "second_cap": ex["second_cap"],
                         "honest_bench": ex["honest_bench"],
                         "convictions": ex["convictions"],
                         "compliant_convictions": ex["compliant_convictions"],
                         "locals_past_elicitation": ex["n_locals_past_elicitation"],
                         "locals_total": ex["n_locals"],
                         **{f"util_{j}": util[j] for j in range(inst.K)}})
        # --- exploitability at the proposed profile ----------------------- #
        _, base_u, _, _ = mean_over_seeds(mech, inst, p, n, seeds, opts_pr, tm, **mkw)
        for i in range(inst.K):
            for o in OPTIONS:
                if o == "proposed":
                    continue
                trial = list(opts_pr)
                trial[i] = o
                rv, u, _, exd = mean_over_seeds(mech, inst, p, n, seeds, trial, tm, **mkw)
                out_rows.append({**base, "mech": mech, "world": "deviation",
                                 "profile": "|".join(trial), "deviator": models[i],
                                 "deviator_index": i, "deviation": o,
                                 "revenue_per_round": rv,
                                 "gain_per_round": float(u[i] - base_u[i]),
                                 "oracle": exd["oracle"], "second_cap": exd["second_cap"],
                                 "honest_bench": exd["honest_bench"],
                                 "convictions": exd["convictions"],
                                 "compliant_convictions": exd["compliant_convictions"],
                                 "locals_past_elicitation": exd["n_locals_past_elicitation"],
                                 "locals_total": exd["n_locals"],
                                 **{f"util_{j}": u[j] for j in range(inst.K)}})
    return time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", required=True)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfgs = [json.loads(l) for l in open(a.configs) if l.strip()]
    mine = [c for j, c in enumerate(cfgs) if j % a.nshards == a.shard]
    rows = []
    for j, c in enumerate(mine):
        dt = run_config(c, rows)
        print(f"[shard {a.shard}] {j+1}/{len(mine)} {c['config_id']} {dt:.1f}s", flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
