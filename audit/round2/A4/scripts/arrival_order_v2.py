"""Arrival order, v2: one honest provider fixed in advance, every other provider
playing the equilibrium of the mechanism being run.

Differences from arrival_order.py (v1), all decided before any v2 run:
  * Honest set = {Mixtral-8x7B} (open weights, self-hostable), the same under
    every mechanism. Honest means exactly what Section 2 says: it never
    delivers below its intrinsic level mu_i(x). It is NOT a full-capability
    provider.
  * Intrinsic level mu_i(x) = min(M_i(x), M_Mistral-7B(x)): the quality of the
    cheapest model in the data, as a zero-effort substitute. v1 used mu = 0.
  * A strategic provider may deliver anything in [0, M_i(x)] (Section 2), so its
    cheapest action is 0; the honest provider's is mu.
  * Cao et al. (WWW 2026) on pooled traffic, with the pooled-mean exploitation
    target of arrival_order.PooledPrimary. Three profiles:
      cao_eq0      their Theorem 5.2 strategy: truthful exploration, meet the
                   announced value in exploitation, minimum cost in unmonitored
                   rounds (strategic 0, honest mu). The model's equilibrium.
      cao_eqmu     as cao_eq0 but strategic providers stop at mu in unmonitored
                   rounds: lenient to Cao.
  (A full-effort profile for Cao is deliberately NOT run: nothing in their
   mechanism rewards effort in unmonitored rounds, so it is not realistic.)
  * Ours: S* (plmesp_star), and the low-revenue member of the equilibrium family
    of thm:equilibrium-set (plmesp_low): at each benchmark every agent that is
    not pointwise top elicits its minimum (strategic 0, honest mu), everything
    else as S*. MESP (scalar) under S* for reference.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrival_order import DATA, ORDERS, PooledPrimary, reorder  # noqa: E402
from baseline_secondbest import Q7, TheirEquilibrium, scalarize  # noqa: E402
from mechanisms import (Instance, MechanismRun, ProfileStrategy,  # noqa: E402
                        honest_benchmark_per_round, oracle_per_round,
                        run_second_best, second_capability_per_round)
from run_sim import draw_queries  # noqa: E402
from trace import Trace  # noqa: E402

HONEST = "Mixtral-8x7B"
CHEAP = "Mistral-7B"
PROFILES = {"plmesp": ["plmesp_star", "plmesp_low"],
            "mesp_scalar": ["mesp_star"],
            "second_best": ["cao_eq0", "cao_eqmu"]}


def build_instance(models):
    cap = pd.read_csv(os.path.join(DATA, "capabilities_finite_5shot.csv"))
    cap = cap[cap.context.isin(Q7)]
    tab = cap.pivot(index="context", columns="model", values="M").loc[Q7]
    masses = pd.read_csv(os.path.join(DATA, "context_masses_5shot.csv")).set_index("context")
    p = masses.loc[Q7, "n_queries"].values.astype(float)
    p /= p.sum()
    M = tab[models].values.astype(float)
    mu = np.minimum(M, tab[[CHEAP]].values.astype(float))
    honest = np.array([m == HONEST for m in models])
    return Instance(M=M, mu=mu, key=np.arange(len(Q7)), honest=honest, names=list(models)), p


class CaoEq(TheirEquilibrium):
    """Their equilibrium; `floor` sets what a strategic provider delivers in the
    unmonitored rounds ("zero" or "mu"). The honest provider always stops at mu."""

    def __init__(self, inst, top_masks, second, floor):
        super().__init__(inst, ["proposed"] * inst.K, top_masks, second=second)
        self.floor = floor

    def target(self, i, phase, q, price, state=None):
        if phase == "fallback":
            mu = self.inst.mu[q, i]
            return mu if (self.inst.honest[i] or self.floor == "mu") else 0.0
        return super().target(i, phase, q, price, state)


class LowEq(ProfileStrategy):
    """S* except that, at each benchmark, an agent that is not pointwise top
    elicits its minimum feasible mean (strategic 0, honest mu)."""

    def target(self, i, phase, q, price, state=None):
        if phase == "elicit" and not self.top_masks[q, i]:
            return self.inst.mu[q, i] if self.inst.honest[i] else 0.0
        return super().target(i, phase, q, price, state)


def one_run(mech, prof, inst, flat, p, qs, n, s, trace_path=None, meta=None):
    used = flat if mech in ("second_best", "mesp_scalar") else inst
    tm = (used.M >= used.M.max(axis=1, keepdims=True) - 1e-12)
    second = np.sort(used.M, axis=1)[:, -2]
    allc = [True] * used.K
    if prof in ("plmesp_star", "mesp_star"):
        st = ProfileStrategy(used, ["proposed"] * used.K, tm, second=second)
    elif prof == "plmesp_low":
        st = LowEq(used, ["proposed"] * used.K, tm, second=second)
    elif prof in ("cao_eq0", "cao_eqmu"):
        st = PooledPrimary(CaoEq(used, tm, second, "zero" if prof == "cao_eq0" else "mu"), used, p, allc)
    else:
        raise ValueError(prof)
    tr = Trace(qs) if trace_path else None
    if mech == "second_best":
        r = run_second_best(used, n, s, st, qs, gate_blind2=True, trace=tr)
        if tr is not None:
            tr.save(trace_path, {**meta, "result": r})
        return dict(revenue=r["revenue_per_round"], fired=float(r["monitor_fired"]),
                    undelegated=r.get("undelegated_fraction", 0.0),
                    util=np.asarray(r["utility_per_round"], dtype=float))
    run = MechanismRun(used, n, s)
    r = run.run(st, qs, trace=tr)
    if tr is not None:
        tr.save(trace_path, {**meta, "result": r, "L": run.L, "s_n": run.s,
                             "locals": {k: {"W": l.W, "tau": l.tau, "phase": l.phase,
                                            "elicited": (l.sum / np.maximum(l.cnt, 1)).tolist(),
                                            "conv_r": l.conv_r, "r": l.r}
                                        for k, l in run.locals.items()}})
    return dict(revenue=r["revenue_per_round"], fired=float(r["convictions"] > 0), undelegated=0.0,
                util=np.asarray((r["T"] - r["C"]) / n, dtype=float))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", required=True)
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=20)
    ap.add_argument("--orders", default=",".join(ORDERS))
    ap.add_argument("--mechs", default="second_best,mesp_scalar,plmesp")
    ap.add_argument("--out", required=True)
    ap.add_argument("--trace-dir", default=None, help="write one .npz per run here")
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
        for mech in a.mechs.split(","):
            for prof in PROFILES[mech]:
                res = []
                for s in range(a.nseeds):
                    tp, meta = None, None
                    if a.trace_dir:
                        d = os.path.join(a.trace_dir, label, str(a.n), order)
                        os.makedirs(d, exist_ok=True)
                        tp = os.path.join(d, f"{mech}_{prof}_seed{s:02d}.npz")
                        meta = dict(subset=label, models=models, contexts=Q7, masses=p, M=inst.M,
                                    mu=inst.mu, honest=inst.honest, n=a.n, seed=s, order=order,
                                    mech=mech, profile=prof, cost="linear phi(m)=m",
                                    honest_provider=HONEST, cheap_substitute=CHEAP)
                    res.append(one_run(mech, prof, inst, flat, p,
                                       reorder(draw_queries(inst, p, a.n, s), order, s, Q),
                                       a.n, s, tp, meta))
                u = np.mean([r["util"] for r in res], axis=0)
                rows.append({**base, "order": order, "mech": mech, "profile": prof,
                             "revenue_per_round": float(np.mean([r["revenue"] for r in res])),
                             "revenue_sd": float(np.std([r["revenue"] for r in res])),
                             "fire_rate": float(np.mean([r["fired"] for r in res])),
                             "undelegated_fraction": float(np.mean([r["undelegated"] for r in res])),
                             **{f"util_{j}": u[j] for j in range(K)}})
                pd.DataFrame(rows).to_csv(a.out, index=False)
            print(f"done {label} n={a.n} {order} {mech}", flush=True)


if __name__ == "__main__":
    main()
