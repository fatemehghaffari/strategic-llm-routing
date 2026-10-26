"""Arrival order: the same prompts, presented in realistic orders.

Question. Cao et al. (WWW 2026) model each prompt as an i.i.d. draw from a
dataset D and summarise every provider by one number, its mean over D. Real
traffic is mixed and arrives in any order: bursts of one task type, whole
days dominated by one workload, slow drift. This script keeps the MULTISET of
prompts fixed and changes only their ORDER, so every difference in outcome is
caused by order alone.

Orders (each a permutation of the same i.i.d. draw, fresh per seed):
  iid      the draw as it comes; their modelling assumption.
  bursty   runs of B consecutive prompts of one benchmark, runs in random
           order (B = n/100 by default: a burst is 1% of the horizon).
  drift    the benchmark mix drifts smoothly over the horizon: each prompt is
           placed by its benchmark's random rank plus Gaussian noise.
  grouped  each benchmark in one contiguous block, blocks in random order.

Mechanisms: second_best (Cao et al., Mechanism 1, on pooled traffic, exactly
as their model treats mixed prompts), mesp_scalar (ours, one number per
provider), plmesp (ours, one capability per benchmark).

Provider behaviour: proposed; their_equilibrium (Cao only); theta0.90 (the
deviator shades 10% of its excess over its intrinsic level, each agent in
turn); baitswitch (elicit at capability, floor when priced).
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from baseline_secondbest import (Q7, make_strategy, price_above_capability_mass,  # noqa: E402
                                 scalarize)
from mechanisms import (MechanismRun, honest_benchmark_per_round,  # noqa: E402
                        oracle_per_round, run_second_best,
                        second_capability_per_round)
from run_sim import draw_queries  # noqa: E402

DATA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "../../../../experiments/data/A4"))
ORDERS = ["iid", "bursty", "drift", "grouped"]
DEVIATIONS = ["proposed", "their_equilibrium", "theta0.90", "baitswitch"]


def reorder(qs, order, seed, Q, burst=None, drift_sd=0.35):
    """A permutation of qs. The multiset is unchanged, so masses are exact."""
    if order == "iid":
        return qs
    rng = np.random.default_rng(7919 + seed)
    n = len(qs)
    if order in ("bursty", "grouped"):
        B = n if order == "grouped" else (burst or max(1, n // 100))
        chunks = []
        for z in range(Q):
            idx = qs[qs == z]
            chunks += [idx[k:k + B] for k in range(0, len(idx), B)]
        perm = rng.permutation(len(chunks))
        return np.concatenate([chunks[j] for j in perm]) if chunks else qs
    if order == "drift":
        rank = rng.permutation(Q) / max(1, Q - 1)
        key = rank[qs] + rng.normal(0.0, drift_sd, size=n)
        return qs[np.argsort(key, kind="stable")]
    raise ValueError(order)


class PooledPrimary:
    """Cao et al. on pooled traffic: the announced value is a POOLED mean, so a
    compliant winner meets it on average over D rather than per benchmark.
    Wraps a strategy and, in the priced phase, replaces the per-benchmark
    min(price, M_i(x)) of every agent playing "proposed" (or their equilibrium)
    by M_i(x) * min(1, price / E_D[M_i]), whose pooled mean is exactly the price
    whenever the agent can meet it. Other options (theta, baitswitch) unchanged."""

    def __init__(self, base, inst, p, compliant):
        self.base, self.inst, self.compliant = base, inst, compliant
        self.avg = p @ inst.M

    def target(self, i, phase, q, price, state=None):
        if phase == "primary" and price is not None and self.compliant[i]:
            M, mu = self.inst.M[q, i], self.inst.mu[q, i]
            m = M * min(1.0, price / max(self.avg[i], 1e-12))
            return max(mu, m) if self.inst.honest[i] else m
        return self.base.target(i, phase, q, price, state)


def one_run(mech, inst, flat, tm, second, dev, devi, qs, n, s, p, pooled=True):
    used = flat if mech in ("second_best", "mesp_scalar") else inst
    st = make_strategy(used, tm, second, dev, devi)
    if mech == "second_best" and pooled:
        K = inst.K
        compliant = [dev in ("proposed", "their_equilibrium") or j != devi for j in range(K)]
        st = PooledPrimary(st, used, p, compliant)
    if mech == "second_best":
        r = run_second_best(used, n, s, st, qs, gate_blind2=True)
        out = dict(revenue=r["revenue_per_round"], fired=float(r["monitor_fired"]),
                   undelegated=r.get("undelegated_fraction", 0.0),
                   delay=r["fired_at_exploitation_round"] if r["monitor_fired"] else np.nan,
                   price_above_cap=price_above_capability_mass(
                       used, p, r["announced_second_best_utility"] + r["price"], r["winner"]),
                   util=np.asarray(r["utility_per_round"], dtype=float))
    else:
        run = MechanismRun(used, n, s)
        r = run.run(st, qs)
        dl = list(r["conviction_rounds"].values())
        out = dict(revenue=r["revenue_per_round"], fired=float(r["convictions"] > 0),
                   undelegated=0.0, delay=float(np.mean(dl)) if dl else np.nan,
                   price_above_cap=float(r["primary_rounds_price_above_capability"]) / n,
                   util=np.asarray((r["T"] - r["C"]) / n, dtype=float))
    return out


def run_cell(label, models, n, seeds, orders, devs, mechs, rows, out_path):
    inst, p, _, _ = I.finite_instance(models, Q7, "a0.00", out=DATA)
    flat = scalarize(inst)
    tm = I.top_masks(inst)
    second = np.sort(inst.M, axis=1)[:, -2]
    Q, K = inst.M.shape
    qs0 = draw_queries(inst, p, n, 0)
    base = dict(subset=label, models="|".join(models), K=K, n=n, nseeds=len(seeds),
                oracle=oracle_per_round(inst, qs0),
                second_cap=second_capability_per_round(inst, qs0),
                honest_bench=honest_benchmark_per_round(inst, qs0))
    for order in orders:
        for mech in mechs:
            for dev in devs:
                if dev == "their_equilibrium" and mech != "second_best":
                    continue
                for devi in ([None] if dev in ("proposed", "their_equilibrium") else range(K)):
                    res = []
                    for s in seeds:
                        qs = reorder(draw_queries(inst, p, n, s), order, s, Q)
                        res.append(one_run(mech, inst, flat, tm, second, dev, devi, qs, n, s, p))
                    u = np.mean([r["util"] for r in res], axis=0)
                    rows.append({**base, "order": order, "mech": mech, "deviation": dev,
                                 "deviator_index": devi,
                                 "deviator": models[devi] if devi is not None else "",
                                 "revenue_per_round": float(np.mean([r["revenue"] for r in res])),
                                 "revenue_sd": float(np.std([r["revenue"] for r in res])),
                                 "fire_rate": float(np.mean([r["fired"] for r in res])),
                                 "undelegated_fraction": float(np.mean([r["undelegated"] for r in res])),
                                 "detection_delay": float(np.nanmean([r["delay"] for r in res]))
                                 if any(np.isfinite(r["delay"]) for r in res) else np.nan,
                                 "price_above_cap": float(np.nanmean([r["price_above_cap"] for r in res])),
                                 **{f"util_{j}": u[j] for j in range(K)}})
            pd.DataFrame(rows).to_csv(out_path, index=False)
            print(f"done {label} n={n} {order} {mech} ({len(rows)} rows)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", required=True, help="label=ModelA|ModelB|...")
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=20)
    ap.add_argument("--orders", default=",".join(ORDERS))
    ap.add_argument("--devs", default=",".join(DEVIATIONS))
    ap.add_argument("--mechs", default="second_best,mesp_scalar,plmesp")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    label, models = a.subset.split("=")
    rows = []
    run_cell(label, models.split("|"), a.n, list(range(a.nseeds)), a.orders.split(","),
             a.devs.split(","), a.mechs.split(","), rows, a.out)


if __name__ == "__main__":
    main()
