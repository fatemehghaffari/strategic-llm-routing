"""Agent C, items 4+6 on a second capability source (Open LLM Leaderboard tables
from Agent A), with full per-round traces.

Input: a long capability table with columns model, context (or type), M, and
optionally n_queries, family, variant_rank (0 = the family's flagship). Masses
are proportional to n_queries when present, else uniform.

  --mode replicate   v2 Figs 1-2 on the coarse types: arms as v2 minus the
                     low-revenue profile (it reads other providers' top masks),
                     orders iid/bursty/drift/grouped, n in {3e5, 3e6}.
  --mode scale       fixed n; a pre-registered nested sequence of Q task types
                     (fine table) and of K providers; arms plmesp_star,
                     mesp_star, cao_eqmu, router_ucb exploit_slow; order iid.
  --mode subst       substitution-as-shading: a strategic provider can only
                     deliver one of its family's variants (discrete); intrinsic
                     level = cheapest variant's capability; provider behaviour
                     = Agent B's Learner, quantised to the variant at or below
                     the level it chooses (profile `learning_subst`), or the
                     scripted switch to the cheapest variant after
                     ceil(4 log n) own selections (`switch_cheapest`).

Setup rules as v2: one honest provider, at its floor mu, the same under every
rule; strategic floor 0 except in subst mode, where it is the cheapest
variant (a provider cannot serve less than its worst model); provider
observation model per the author's rule of 28 Sep 2026.
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrival_order import reorder  # noqa: E402
from baseline_secondbest import scalarize  # noqa: E402
from extras_c import run_arm  # noqa: E402
from mechanisms import (Instance, honest_benchmark_per_round, oracle_per_round,  # noqa: E402
                        second_capability_per_round)
from run_sim import draw_queries  # noqa: E402
from trace import Trace  # noqa: E402


def load_table(path):
    t = pd.read_csv(path)
    if "context" not in t and "type" in t:
        t = t.rename(columns={"type": "context"})
    return t


def instance_from(t, models, honest, cheap=None, types=None, mu_mode="cheap"):
    types = types or list(dict.fromkeys(t["context"]))
    tab = t.pivot_table(index="context", columns="model", values="M").loc[types]
    if "n_queries" in t:
        nq = t.groupby("context")["n_queries"].first().loc[types].values.astype(float)
    else:
        nq = np.ones(len(types))
    p = nq / nq.sum()
    M = tab[models].values.astype(float)
    if mu_mode == "cheap":
        mu = np.minimum(M, tab[[cheap]].values.astype(float))
    else:                                 # per-family cheapest variant, given as a dict model -> cheapest
        mu = np.column_stack([np.minimum(M[:, j], tab[mu_mode[m]].values) for j, m in enumerate(models)])
    h = np.array([m == honest for m in models])
    return Instance(M=M, mu=mu, key=np.arange(len(types)), honest=h, names=list(models)), p, types


def select_subsets(t, honest, ks=((3, (.1, .5, .9)), (4, (.1, .5, .9)), (5, (.1, .5, .9)))):
    """Same rule as select_subsets_v2.py, on this table."""
    types = list(dict.fromkeys(t["context"]))
    tab = t.pivot_table(index="model", columns="context", values="M")[types]
    nq = (t.groupby("context")["n_queries"].first().loc[types].values.astype(float)
          if "n_queries" in t else np.ones(len(types)))
    w = nq / nq.sum()
    others = [m for m in tab.index if m != honest]
    out = []
    for k, qs in ks:
        rows = []
        for S in itertools.combinations(others, k - 1):
            S = (honest,) + S
            M = tab.loc[list(S)].values.T
            rows.append((w @ np.sort(M, 1)[:, -2] - np.sort(w @ M)[-2], "|".join(S)))
        rows.sort()
        for q in qs:
            g, ms = rows[int(round(q * (len(rows) - 1)))]
            out.append((f"k{k}_q{int(q * 100)}", ms, g))
    return out


class SubstLearner:
    """Agent B's Learner, with delivery quantised to the provider's own family
    variants: the largest variant capability at or below the chosen level (the
    cheapest variant if none is). Observation model unchanged: the wrapper uses
    only the provider's own variant capabilities at the served prompt."""

    def __init__(self, inst, n, seed, variants):
        from learners import Learner
        self.L = Learner(inst, n, seed)
        self.inst, self.var = inst, variants     # variants[i]: (Q, V_i) capabilities, own family

    def target(self, i, phase, q, price, state=None):
        m = self.L.target(i, phase, q, price, state)
        if self.inst.honest[i]:
            return m
        v = self.var[i][q]
        ok = v[v <= m + 1e-12]
        return float(ok.max()) if ok.size else float(v.min())

    def meta(self):
        return {"wrapped": "learners.Learner", "quantised_to": "own family variants"}


class SwitchCheapest:
    def __init__(self, inst, n, variants):
        self.inst, self.var = inst, variants
        self.warm = int(np.ceil(4 * np.log(n)))
        self.k = np.zeros(inst.K, dtype=np.int64)

    def target(self, i, phase, q, price, state=None):
        M, mu = self.inst.M[q, i], self.inst.mu[q, i]
        self.k[i] += 1
        if self.inst.honest[i]:
            return mu
        return M if self.k[i] <= self.warm else float(self.var[i][q].min())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["replicate", "scale", "subst"])
    ap.add_argument("--table", required=True)
    ap.add_argument("--subset", required=True, help="label=ModelA|ModelB|...")
    ap.add_argument("--honest", required=True)
    ap.add_argument("--cheap", default=None)
    ap.add_argument("--types", default=None, help="comma list of task types (scale mode)")
    ap.add_argument("--n", type=int, default=3000000)
    ap.add_argument("--nseeds", type=int, default=20)
    ap.add_argument("--orders", default="iid")
    ap.add_argument("--arms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--trace-dir", default=None)
    a = ap.parse_args()
    t = load_table(a.table)
    label, models = a.subset.split("=")
    models = models.split("|")
    types = a.types.split(",") if a.types else None
    variants = None
    if a.mode == "subst":
        fam = t.groupby("model")["family"].first()
        cheapest = {}
        for m in models:
            fm = fam[fam == fam[m]].index.tolist()
            pooled = t[t.model.isin(fm)].groupby("model").M.mean()
            cheapest[m] = pooled.idxmin()
        inst, p, types = instance_from(t, models, a.honest, types=types, mu_mode=cheapest)
        tab = t.pivot_table(index="context", columns="model", values="M").loc[types]
        variants = {j: tab[fam[fam == fam[m]].index.tolist()].values for j, m in enumerate(models)}
    else:
        inst, p, types = instance_from(t, models, a.honest, cheap=a.cheap, types=types)
    flat = scalarize(inst)
    Q, K = inst.M.shape
    qs0 = draw_queries(inst, p, a.n, 0)
    base = dict(mode=a.mode, subset=label, models="|".join(models), K=K, Q=Q, n=a.n,
                nseeds=a.nseeds, oracle=oracle_per_round(inst, qs0),
                second_cap=second_capability_per_round(inst, qs0),
                honest_bench=honest_benchmark_per_round(inst, qs0), table=os.path.basename(a.table))
    rows = []
    for order in a.orders.split(","):
        for arm in a.arms.split(","):
            res = []
            for s in range(a.nseeds):
                qs = reorder(draw_queries(inst, p, a.n, s), order, s, Q)
                tr, tp = None, None
                if a.trace_dir:
                    d = os.path.join(a.trace_dir, a.mode, label, f"Q{Q}", str(a.n), order)
                    os.makedirs(d, exist_ok=True)
                    tp = os.path.join(d, f"{arm.replace(':', '_')}_seed{s:02d}.npz")
                    tr = Trace(qs)
                meta = dict(mode=a.mode, subset=label, models=models, contexts=types, masses=p,
                            M=inst.M, mu=inst.mu, honest=inst.honest, n=a.n, seed=s, order=order,
                            arm=arm, table=a.table, cost="linear phi(m)=m")
                mech, prof = arm.split(":")
                if prof in ("learning_subst", "switch_cheapest"):
                    import mechanisms as MM
                    st = (SubstLearner(inst, a.n, s, variants) if prof == "learning_subst"
                          else SwitchCheapest(inst, a.n, variants))
                    used = flat if mech in ("second_best", "mesp_scalar") else inst
                    if mech in ("plmesp", "mesp_scalar"):
                        r = MM.MechanismRun(used, a.n, s).run(st, qs, trace=tr)
                        out = dict(revenue=r["revenue_per_round"], fired=float(r["convictions"] > 0),
                                   unserved=0.0, util=(r["T"] - r["C"]) / a.n, raw=r,
                                   compliant_convictions=r["compliant_convictions"])
                    elif mech == "second_best":
                        r = MM.run_second_best(used, a.n, s, st, qs, gate_blind2=True, trace=tr)
                        out = dict(revenue=r["revenue_per_round"], fired=float(r["monitor_fired"]),
                                   unserved=float(r.get("undelegated_fraction", 0.0)),
                                   util=np.asarray(r["utility_per_round"], float), raw=r)
                    else:
                        r = MM.run_router(used, a.n, s, st, qs, rule="ucb", trace=tr)
                        out = dict(revenue=r["revenue_per_round"], fired=0.0, unserved=0.0,
                                   util=np.asarray(r["utility_per_round"], float), raw=r)
                    if hasattr(st, "meta"):
                        meta["strategy"] = st.meta()
                else:
                    out = run_arm(arm, inst, flat, p, qs, a.n, s, trace=tr)
                if tr is not None:
                    tr.save(tp, {**meta, "result": out.get("raw")})
                res.append(out)
            u = np.mean([np.asarray(r["util"], float) for r in res], axis=0)
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
            print(f"done {a.mode} {label} Q={Q} n={a.n} {order} {arm}", flush=True)


if __name__ == "__main__":
    main()
