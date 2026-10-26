"""Agent C extras on the v2 setup (Mixtral-8x7B honest at mu, mu = Mistral-7B
capability, arrival_order_subsets_v2.txt), with full per-round traces.

  --item cao_per_type   Item 7. OUR CONSTRUCTION, not the mechanism of Cao et al.:
                        one independent copy of their Mechanism 1 per task type,
                        each copy given its realised query count as its horizon
                        (generous: the copy knows it), the pooled-mean target of
                        arrival_order.PooledPrimary inside each copy, both of
                        their equilibria (cao_eqmu, cao_eq0).
  --item graded         Item 9. Rewards in [0,1] with mean m instead of Bernoulli:
                        variant "emp" draws Beta(m k, (1-m) k) with k = 1/r - 1,
                        r the measured score-variance ratio of the task type
                        (GSM8K, MT-Bench graded; others stay Bernoulli), variant
                        "k10" draws Beta with k = 10 on every type (stress).
  --item noisy          Item 5. The mechanism and the router see a NOISY task
                        label while quality follows the true type. Uniform
                        mislabelling at rate eps (to a different type, uniformly),
                        or a measured confusion matrix (--confusion csv).

Provider observation model (author rule, 28 Sep 2026): a provider sees only its
own history, messages the mechanism sends it, whether it was chosen, and t.
Strategies used here: S* (price is a message), Cao's equilibrium with the
pooled target (its own capability and the traffic mix, their model's
assumption), router exploit/average (own selection count). No strategy here
reads anything about other providers.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrival_order import ORDERS, PooledPrimary, reorder  # noqa: E402
from arrival_order_v2 import CHEAP, HONEST, Q7, CaoEq, build_instance  # noqa: E402
from baseline_secondbest import scalarize  # noqa: E402
from baselines_v2 import Average, ExploitDecay  # noqa: E402
from mechanisms import (Instance, MechanismRun, ProfileStrategy, run_router,  # noqa: E402
                        run_second_best, second_capability_per_round,
                        honest_benchmark_per_round, oracle_per_round)
from run_sim import draw_queries  # noqa: E402
from trace import Trace  # noqa: E402

DATA5 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "../../../../experiments/data/A5"))


class TraceF(Trace):
    """Trace with a float reward column (graded rewards)."""

    def __init__(self, queries):
        super().__init__(queries)
        self.reward = np.zeros(len(queries), dtype=np.float32)


def _tm(inst):
    return inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12


def strategy_for(prof, used, p):
    tm = _tm(used)
    second = np.sort(used.M, axis=1)[:, -2]
    if prof in ("plmesp_star", "mesp_star"):
        return ProfileStrategy(used, ["proposed"] * used.K, tm, second=second)
    if prof in ("cao_eqmu", "cao_eq0"):
        return PooledPrimary(CaoEq(used, tm, second, "mu" if prof == "cao_eqmu" else "zero"),
                             used, p, [True] * used.K)
    if prof == "average":
        return Average(used)
    if prof.startswith("exploit"):
        return ExploitDecay(used, len_hint[0], prof.split("_")[1])
    raise ValueError(prof)


len_hint = [None]


def run_arm(arm, inst, flat, p, qs, n, s, trace=None, reward_fn=None):
    """arm = mech:profile. Returns summary dict."""
    mech, prof = arm.split(":")
    len_hint[0] = n
    if mech == "plmesp":
        used = inst
    elif mech in ("mesp_scalar", "second_best"):
        used = flat
    else:
        used = inst
    st = strategy_for(prof, used, p)
    if mech == "second_best":
        r = run_second_best(used, n, s, st, qs, gate_blind2=True, trace=trace, reward_fn=reward_fn)
        return dict(revenue=r["revenue_per_round"], fired=float(r["monitor_fired"]),
                    unserved=float(r.get("undelegated_fraction", 0.0)),
                    util=np.asarray(r["utility_per_round"], float), raw=r)
    if mech in ("plmesp", "mesp_scalar"):
        run = MechanismRun(used, n, s)
        r = run.run(st, qs, trace=trace, reward_fn=reward_fn)
        return dict(revenue=r["revenue_per_round"], fired=float(r["convictions"] > 0), unserved=0.0,
                    compliant_convictions=r["compliant_convictions"],
                    util=np.asarray((r["T"] - r["C"]) / n, float), raw=r)
    if mech in ("router_ucb", "router_eps", "router_greedy"):
        rule = {"router_ucb": "ucb", "router_eps": "epsgreedy", "router_greedy": "greedy"}[mech]
        r = run_router(used, n, s, st, qs, rule=rule, trace=trace, reward_fn=reward_fn)
        return dict(revenue=r["revenue_per_round"], fired=0.0, unserved=0.0,
                    util=np.asarray(r["utility_per_round"], float), raw=r)
    if mech == "router_audit":
        from mechanisms import run_router_audit
        r = run_router_audit(used, n, s, st, qs, trace=trace)
        fired = float(r.get("bans", 0) > 0) if isinstance(r.get("bans", 0), (int, float)) else float(len(r.get("bans", [])) > 0)
        return dict(revenue=r["revenue_per_round"], fired=fired,
                    unserved=float(r.get("undelegated_fraction", 0.0)),
                    util=np.asarray(r["utility_per_round"], float), raw=r)
    raise ValueError(mech)


# ------------------------------------------------------------------ item 7 --
def cao_per_type(inst, p, qs, n, s, prof, trace=None):
    """One independent Cao copy per task type; merged back into global rounds."""
    Q, K = inst.M.shape
    rev = 0.0
    util = np.zeros(K)
    fired, unserved = 0, 0
    parts = {}
    for z in range(Q):
        pos = np.flatnonzero(qs == z)
        nz = len(pos)
        if nz == 0:
            continue
        sub = Instance(M=inst.M[[z]], mu=inst.mu[[z]], key=np.zeros(1, dtype=int),
                       honest=inst.honest, names=inst.names)
        st = strategy_for(prof, sub, np.ones(1))
        tr = Trace(np.zeros(nz, dtype=np.int64)) if trace is not None else None
        r = run_second_best(sub, nz, 1000 * s + z, st, np.zeros(nz, dtype=np.int64),
                            gate_blind2=True, trace=tr)
        rev += r["revenue_per_round"] * nz
        util += np.asarray(r["utility_per_round"], float) * nz
        fired += int(r["monitor_fired"])
        unserved += float(r.get("undelegated_fraction", 0.0)) * nz
        parts[z] = {k: r[k] for k in ("winner", "announced_second_best_utility", "price",
                                      "monitor_fired", "fired_at_exploitation_round") if k in r}
        if trace is not None:
            for f in ("agent", "phase", "price", "target", "reward", "effort", "agent_utility"):
                getattr(trace, f)[pos] = getattr(tr, f)
    return dict(revenue=rev / n, fired=fired / Q, unserved=unserved / n, util=util / n,
                raw={"copies": parts})


# ------------------------------------------------------------------ item 9 --
def make_graded(inst_rows_type, kappa_by_type, seed):
    gen = np.random.default_rng(424242 + seed)
    kap = np.asarray(kappa_by_type, float)

    def fn(m, q, u):
        k = kap[inst_rows_type[q]]
        if k <= 0:
            return int(u < m)
        if m <= 1e-9:
            return 0.0
        if m >= 1 - 1e-9:
            return 1.0
        return float(gen.beta(m * k, (1.0 - m) * k))
    return fn


def kappas(variant):
    if variant == "k10":
        return [10.0] * len(Q7)
    sv = pd.read_csv(os.path.join(DATA5, "score_variance_5shot.csv"))
    r = sv.groupby("context").ratio.mean().reindex(Q7).values
    return [0.0 if ri > 0.99 else 1.0 / ri - 1.0 for ri in r]


# ------------------------------------------------------------------ item 5 --
def noisy_instance(inst, p, C):
    """Rows r = true*Q + observed; quality from the true type, key = observed."""
    Q, K = inst.M.shape
    rows = [(a, b) for a in range(Q) for b in range(Q)]
    M = np.array([inst.M[a] for a, b in rows])
    mu = np.array([inst.mu[a] for a, b in rows])
    key = np.array([b for a, b in rows])
    pr = np.array([p[a] * C[a, b] for a, b in rows])
    return Instance(M=M, mu=mu, key=key, honest=inst.honest, names=inst.names), pr


def confusion(eps, Q, path=None):
    if path:
        c = pd.read_csv(path, index_col=0).reindex(index=Q7, columns=Q7).fillna(0.0).values
        c = c / np.maximum(c.sum(axis=1, keepdims=True), 1e-12)
        return c
    c = np.full((Q, Q), eps / (Q - 1))
    np.fill_diagonal(c, 1.0 - eps)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item", required=True, choices=["cao_per_type", "graded", "noisy"])
    ap.add_argument("--subset", required=True)
    ap.add_argument("--n", type=int, default=3000000)
    ap.add_argument("--nseeds", type=int, default=20)
    ap.add_argument("--orders", default="iid")
    ap.add_argument("--arms", default="")
    ap.add_argument("--variant", default="emp", help="graded: emp|k10; noisy: eps value or 'measured'")
    ap.add_argument("--confusion", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--trace-dir", default=None)
    a = ap.parse_args()
    label, models = a.subset.split("=")
    models = models.split("|")
    inst, p = build_instance(models)
    flat = scalarize(inst)
    Q, K = inst.M.shape
    qs0 = draw_queries(inst, p, a.n, 0)
    base = dict(item=a.item, variant=a.variant, subset=label, models="|".join(models), K=K, n=a.n,
                nseeds=a.nseeds, oracle=oracle_per_round(inst, qs0),
                second_cap=second_capability_per_round(inst, qs0),
                honest_bench=honest_benchmark_per_round(inst, qs0))
    arms = a.arms.split(",") if a.arms else {
        "cao_per_type": ["cao_per_type:cao_eqmu", "cao_per_type:cao_eq0"],
        "graded": ["plmesp:plmesp_star", "mesp_scalar:mesp_star", "second_best:cao_eqmu",
                   "router_ucb:exploit_slow", "router_ucb:average"],
        "noisy": ["plmesp:plmesp_star", "mesp_scalar:mesp_star", "second_best:cao_eqmu",
                  "router_ucb:exploit_slow", "router_ucb:average"]}[a.item]
    if a.item == "noisy":
        C = confusion(float(a.variant) if a.variant != "measured" else 0.0, Q,
                      a.confusion if a.variant == "measured" else None)
        ninst, npr = noisy_instance(inst, p, C)
        nflat = scalarize(ninst)
    rows = []
    for order in a.orders.split(","):
        for arm in arms:
            res = []
            for s in range(a.nseeds):
                qs = reorder(draw_queries(inst, p, a.n, s), order, s, Q)
                tp = None
                if a.trace_dir:
                    d = os.path.join(a.trace_dir, a.item, a.variant, label, str(a.n), order)
                    os.makedirs(d, exist_ok=True)
                    tp = os.path.join(d, f"{arm.replace(':', '_')}_seed{s:02d}.npz")
                meta = dict(item=a.item, variant=a.variant, subset=label, models=models, contexts=Q7,
                            masses=p, M=inst.M, mu=inst.mu, honest=inst.honest, n=a.n, seed=s,
                            order=order, arm=arm, cost="linear phi(m)=m", honest_provider=HONEST,
                            cheap_substitute=CHEAP)
                if a.item == "cao_per_type":
                    tr = Trace(qs) if tp else None
                    r = cao_per_type(inst, p, qs, a.n, s, arm.split(":")[1], trace=tr)
                elif a.item == "graded":
                    kap = kappas(a.variant)
                    meta["kappa_by_type"] = kap
                    tr = TraceF(qs) if tp else None
                    r = run_arm(arm, inst, flat, p, qs, a.n, s, trace=tr,
                                reward_fn=make_graded(np.arange(Q), kap, s))
                else:
                    gen = np.random.default_rng(99991 + s)
                    u = gen.random(len(qs))
                    cum = np.cumsum(C, axis=1)
                    obs = (u[:, None] > cum[qs]).sum(axis=1)
                    obs = np.minimum(obs, Q - 1)
                    rq = qs * Q + obs
                    meta["confusion"] = C
                    meta["mislabel_rate_realised"] = float(np.mean(obs != qs))
                    tr = Trace(rq.astype(np.int64)) if tp else None
                    if tr is not None:
                        tr.query = rq.astype(np.uint8)
                    r = run_arm(arm, ninst, nflat, npr, rq, a.n, s, trace=tr)
                if tr is not None:
                    tr.save(tp, {**meta, "result": r.get("raw")})
                res.append(r)
            u = np.mean([r["util"] for r in res], axis=0)
            row = {**base, "order": order, "arm": arm,
                   "revenue_per_round": float(np.mean([r["revenue"] for r in res])),
                   "revenue_sd": float(np.std([r["revenue"] for r in res])),
                   "fire_rate": float(np.mean([r["fired"] for r in res])),
                   "unserved_fraction": float(np.mean([r["unserved"] for r in res])),
                   **{f"util_{j}": u[j] for j in range(K)}}
            if all("compliant_convictions" in r for r in res):
                row["compliant_conviction_rate"] = float(np.mean([r["compliant_convictions"] > 0 for r in res]))
            rows.append(row)
            pd.DataFrame(rows).to_csv(a.out, index=False)
            print(f"done {a.item} {a.variant} {label} n={a.n} {order} {arm}", flush=True)


if __name__ == "__main__":
    main()
