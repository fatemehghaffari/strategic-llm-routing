"""Baselines under the v2 setup of arrival_order_v2.py: same subsets, same
honest provider (Mixtral-8x7B), same intrinsic level (Mistral-7B capability),
same arrival orders and horizons, and a full per-round trace of every run.

Routers (greedy, epsilon-greedy, UCB, one estimate per benchmark as in A4)
price nothing and punish nothing, so providers facing them are modelled, as
the author specified on 27 Sep 2026, by:
  exploit_slow / exploit_fast
      honest provider: its honest minimum mu_i(x), always.
      strategic provider: full capability M_i(x) for its first
      ceil(4 log n) selections, then a linear decline to 0 (the model's floor
      for a strategic provider) over D further selections of its own, with
      D = n / K (slow) or n / (10 K) (fast). Providers count their own
      selections: they do not see the global round (Section 2).
  average
      honest provider at mu_i(x); strategic provider at the midpoint
      mu_i(x) + (M_i(x) - mu_i(x)) / 2, always.
No full-capability profile is run: it is not realistic against a rule that
does not reward effort.

The single-observation exclusion rule of Esmaeili et al. (AAAI 2025) prices
and excludes, so it is run under the proposed profile, as our mechanisms are.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrival_order import ORDERS, reorder  # noqa: E402
from arrival_order_v2 import CHEAP, HONEST, Q7, build_instance  # noqa: E402
from baseline_secondbest import scalarize  # noqa: E402
from mechanisms import (ProfileStrategy, honest_benchmark_per_round,  # noqa: E402
                        oracle_per_round, run_router,
                        run_single_observation_exclusion,
                        second_capability_per_round)
from run_sim import draw_queries  # noqa: E402
from trace import Trace  # noqa: E402

RULES = {"router_greedy": "greedy", "router_eps": "epsgreedy", "router_ucb": "ucb"}
PROFILES = {**{r: ["exploit_slow", "exploit_fast", "average"] for r in RULES},
            "esmaeili": ["proposed"]}


class ExploitDecay:
    def __init__(self, inst, n, speed):
        self.inst = inst
        self.warm = int(np.ceil(4 * np.log(n)))
        self.D = max(1.0, n / inst.K / (1.0 if speed == "slow" else 10.0))
        self.k = np.zeros(inst.K, dtype=np.int64)

    def target(self, i, phase, q, price, state=None):
        M, mu = self.inst.M[q, i], self.inst.mu[q, i]
        k = self.k[i]
        self.k[i] += 1
        if self.inst.honest[i]:
            return mu
        if k < self.warm:
            return M
        return M * max(0.0, 1.0 - (k - self.warm) / self.D)


class Average:
    def __init__(self, inst):
        self.inst = inst

    def target(self, i, phase, q, price, state=None):
        M, mu = self.inst.M[q, i], self.inst.mu[q, i]
        return mu if self.inst.honest[i] else mu + 0.5 * (M - mu)


def one_run(rule, prof, inst, flat, qs, n, s, trace_path, meta):
    tr = Trace(qs) if trace_path else None
    if rule == "esmaeili":
        used = flat
        tm = (used.M >= used.M.max(axis=1, keepdims=True) - 1e-12)
        st = ProfileStrategy(used, ["proposed"] * used.K, tm, second=np.sort(used.M, axis=1)[:, -2])
        r = run_single_observation_exclusion(used, n, s, st, qs, trace=tr)
        fired = float(r["exclusions"] > 0)
    else:
        used = inst
        st = (Average(used) if prof == "average"
              else ExploitDecay(used, n, prof.split("_")[1]))
        r = run_router(used, n, s, st, qs, rule=RULES[rule], trace=tr)
        fired = 0.0
    if tr is not None:
        extra = {}
        if isinstance(st, ExploitDecay):
            extra = {"warmup_selections": st.warm, "decay_selections": st.D}
        tr.save(trace_path, {**meta, **extra, "result": r})
    served = float(np.mean(tr.agent != 255)) if tr is not None else np.nan
    return dict(revenue=r["revenue_per_round"], fired=fired, served=served,
                util=np.asarray(r["utility_per_round"], dtype=float))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", required=True)
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=20)
    ap.add_argument("--orders", default=",".join(ORDERS))
    ap.add_argument("--rules", default=",".join(PROFILES))
    ap.add_argument("--out", required=True)
    ap.add_argument("--trace-dir", default=None)
    a = ap.parse_args()
    label, models = a.subset.split("=")
    models = models.split("|")
    inst, p = build_instance(models)
    flat = scalarize(inst)
    Q, K = inst.M.shape
    qs0 = draw_queries(inst, p, a.n, 0)
    base = dict(subset=label, models="|".join(models), K=K, n=a.n, nseeds=a.nseeds,
                oracle=oracle_per_round(inst, qs0), second_cap=second_capability_per_round(inst, qs0),
                honest_bench=honest_benchmark_per_round(inst, qs0))
    rows = []
    for order in a.orders.split(","):
        for rule in a.rules.split(","):
            for prof in PROFILES[rule]:
                res = []
                for s in range(a.nseeds):
                    tp, meta = None, None
                    if a.trace_dir:
                        d = os.path.join(a.trace_dir, label, str(a.n), order)
                        os.makedirs(d, exist_ok=True)
                        tp = os.path.join(d, f"{rule}_{prof}_seed{s:02d}.npz")
                        meta = dict(subset=label, models=models, contexts=Q7, masses=p, M=inst.M,
                                    mu=inst.mu, honest=inst.honest, n=a.n, seed=s, order=order,
                                    mech=rule, profile=prof, cost="linear phi(m)=m",
                                    honest_provider=HONEST, cheap_substitute=CHEAP)
                    res.append(one_run(rule, prof, inst, flat,
                                       reorder(draw_queries(inst, p, a.n, s), order, s, Q),
                                       a.n, s, tp, meta))
                u = np.mean([r["util"] for r in res], axis=0)
                rows.append({**base, "order": order, "mech": rule, "profile": prof,
                             "revenue_per_round": float(np.mean([r["revenue"] for r in res])),
                             "revenue_sd": float(np.std([r["revenue"] for r in res])),
                             "fire_rate": float(np.mean([r["fired"] for r in res])),
                             "undelegated_fraction": 1.0 - float(np.nanmean([r["served"] for r in res])),
                             **{f"util_{j}": u[j] for j in range(K)}})
                pd.DataFrame(rows).to_csv(a.out, index=False)
            print(f"done {label} n={a.n} {order} {rule}", flush=True)


if __name__ == "__main__":
    main()
