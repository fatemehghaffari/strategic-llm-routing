"""v3 driver for the WWW 2027 Tier-1 grids (A5, Agent B).

Generalises arrival_order_v2.py and baselines_v2.py without editing them:
  * every (rule, profile) pair that v2 already runs is delegated to the v2
    `one_run` functions unchanged, so v2 numbers reproduce exactly;
  * new profiles: `learning` for every rule (learners.Learner), and the
    audit-and-ban router `router_audit` (mechanisms.run_router_audit) with the
    SELF reference only, delta in {0.02, 0.05};
  * --taskset q7 (RouterBench's 7 families, as v2) or merged5 (Agent A's five
    merged task types, experiments/data/A5/capabilities_merged5_5shot.csv);
  * --orders adds `real`: a window of Agent A's timestamp-ordered stream of task
    types; the seed picks the start offset; the horizon never exceeds the
    stream (never tiled).
Setup as v2: honest provider Mixtral-8x7B at its floor mu in every rule,
mu_i(x) = min(M_i(x), M_Mistral-7B(x)), strategic floor 0, no full-effort
profile for any rule that does not reward effort, full per-round traces.
"""
import argparse
import glob
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arrival_order_v2 as AO2  # noqa: E402
import baselines_v2 as BL2  # noqa: E402
from arrival_order import ORDERS as SYN_ORDERS, reorder  # noqa: E402
from baseline_secondbest import scalarize  # noqa: E402
from learners import Learner  # noqa: E402
from mechanisms import (Instance, MechanismRun, honest_benchmark_per_round,  # noqa: E402
                        oracle_per_round, run_router, run_router_audit,
                        run_second_best, run_single_observation_exclusion,
                        second_capability_per_round)
from run_sim import draw_queries  # noqa: E402
from trace import Trace  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
A4DATA = os.path.normpath(os.path.join(HERE, "../../../../experiments/data/A4"))
A5DATA = os.path.normpath(os.path.join(HERE, "../../../../experiments/data/A5"))
HONEST, CHEAP = AO2.HONEST, AO2.CHEAP
AUDIT_DELTAS = {"router_audit_d002": 0.02, "router_audit_d005": 0.05}
# 5% false-ban variants (29 Sep 2026, author's decision): mechanisms.run_router_audit(false_ban=0.05)
AUDIT_FB = {"router_audit_d002_fb05": 0.05, "router_audit_d005_fb05": 0.05}
AUDIT_DELTAS.update({"router_audit_d002_fb05": 0.02, "router_audit_d005_fb05": 0.05})
ROUTERS_V2 = {"router_greedy": "greedy", "router_eps": "epsgreedy", "router_ucb": "ucb"}
# router_static (29 Sep 2026): offline benchmark router, never learns (mechanisms.run_router_static)
ROUTERS = {**ROUTERS_V2, "router_static": "static"}
PROFILES = {
    # exploit_slow / exploit_fast (24 Oct 2026): the routers' effort-reduction schedules (BL2.ExploitDecay)
    # played against the mechanisms, so Figure 5 can show MESP under the same provider behaviour
    "plmesp": ["plmesp_star", "plmesp_low", "learning", "exploit_slow", "exploit_fast"],
    "mesp_scalar": ["mesp_star", "learning", "exploit_slow", "exploit_fast"],
    "second_best": ["cao_eq0", "cao_eqmu", "learning"],
    **{r: ["exploit_slow", "exploit_fast", "average", "learning"] for r in ROUTERS},
    "esmaeili": ["proposed", "learning"],
    **{r: ["exploit_slow", "exploit_fast", "average", "evade", "learning"] for r in AUDIT_DELTAS},
}
V2_MECH = {("plmesp", "plmesp_star"), ("plmesp", "plmesp_low"), ("mesp_scalar", "mesp_star"),
           ("second_best", "cao_eq0"), ("second_best", "cao_eqmu")}
V2_BASE = {(r, p) for r in ROUTERS_V2 for p in ("exploit_slow", "exploit_fast", "average")} | {
    ("esmaeili", "proposed")}


# --------------------------------------------------------------------------- #
# instances
# --------------------------------------------------------------------------- #
def build_instance(models, taskset):
    if taskset == "q7":
        inst, p = AO2.build_instance(models)
        return inst, p, list(AO2.Q7)
    cap = pd.read_csv(os.path.join(A5DATA, "capabilities_merged5_5shot.csv"))
    col = "type" if "type" in cap else "context"
    types = list(dict.fromkeys(cap[col]))
    tab = cap.pivot(index=col, columns="model", values="M").loc[types]
    ms = pd.read_csv(os.path.join(A5DATA, "type_masses_merged5_5shot.csv")).set_index("type")
    nq = ms.loc[types, "n_queries"].values.astype(float)
    p = nq / nq.sum()          # RouterBench masses; a `real` order brings its own mix
    M = tab[models].values.astype(float)
    mu = np.minimum(M, tab[[CHEAP]].values.astype(float))
    honest = np.array([m == HONEST for m in models])
    return (Instance(M=M, mu=mu, key=np.arange(len(types)), honest=honest, names=list(models)),
            p, types)


REAL_DIR = "<workspace>/real_sequences"
REAL_FILE = {"merged5": "wildchat48m_all.npz"}   # Agent A: all-language WildChat-4.8M stream


def real_stream(taskset, types):
    """Agent A's stream: `type` = uint8 task-type index per user turn in timestamp order,
    `types` = the type names in index order (must equal the taskset's order)."""
    if taskset not in REAL_FILE:
        raise ValueError(f"no real stream for taskset {taskset}")
    f = os.path.join(REAL_DIR, REAL_FILE[taskset])
    z = np.load(f, allow_pickle=False)
    seq = z["type"].astype(np.int64)
    names = [str(x) for x in z["types"]]
    assert names == list(types), (names, types)
    return seq, os.path.basename(f)


def queries_for(inst, p, n, s, order, taskset, types):
    Q = inst.M.shape[0]
    if order != "real":
        return reorder(draw_queries(inst, p, n, s), order, s, Q), {}
    seq, src = real_stream(taskset, types)
    if n > len(seq):
        raise ValueError(f"horizon {n} exceeds the real stream ({len(seq)}); never tiled")
    start = int(np.random.default_rng(31337 + s).integers(0, len(seq) - n + 1))
    return seq[start:start + n].copy(), {"real_source": src, "real_start": start,
                                         "real_stream_len": int(len(seq))}


# --------------------------------------------------------------------------- #
# new profiles
# --------------------------------------------------------------------------- #
class AuditProfile:
    """Provider behaviour against the audit router (honest provider at mu).

    exploit_* and average are the baselines_v2 profiles. evade: at each task
    type deliver capability for the first `warm` selections (which sets the
    reference), then the most shading the test cannot see, M - delta - rad,
    backed off by three standard errors of the reference so that reference
    noise does not trip it: m = max(0, M - delta - rad + 3 * 0.5 / sqrt(warm)).
    """

    def __init__(self, inst, n, prof, delta, false_ban=None):
        self.inst, self.prof, self.delta = inst, prof, delta
        self.warm = int(np.ceil(4 * np.log(n)))
        K, Q = inst.K, inst.M.shape[0]
        self.rad = float(np.sqrt(np.log(2.0 * n * K * Q) / (2.0 * self.warm)))
        if false_ban is not None:           # evade knows the router's radius exactly
            Qr = inst.Q
            self.rad = float(np.sqrt(np.log(4.0 * Qr / false_ban) / (2.0 * self.warm)))
        self.cnt = np.zeros((Q, K), dtype=np.int64)
        if prof.startswith("exploit"):
            self.base = BL2.ExploitDecay(inst, n, prof.split("_")[1])
        elif prof == "average":
            self.base = BL2.Average(inst)
        else:
            self.base = None

    def target(self, i, phase, q, price, state=None):
        if self.base is not None:
            return self.base.target(i, phase, q, price, state)
        M, mu = self.inst.M[q, i], self.inst.mu[q, i]
        k = int(self.inst.key[q])
        c = self.cnt[k, i]
        self.cnt[k, i] += 1
        if self.inst.honest[i]:
            return mu
        if c < self.warm:
            return M
        return max(0.0, M - self.delta - self.rad + 3 * 0.5 / np.sqrt(self.warm))

    def meta(self):
        return {"warm": self.warm, "ref_radius": self.rad, "delta": self.delta,
                "evade_rule": "M - delta - rad + 3*0.5/sqrt(warm), floor 0"}


def one_run_new(rule, prof, inst, flat, p, qs, n, s, trace_path, meta):
    tr = Trace(qs) if trace_path else None
    extra = {}
    if rule in AUDIT_DELTAS:
        used = inst
        fb = AUDIT_FB.get(rule)
        st = (Learner(used, n, s) if prof == "learning"
              else AuditProfile(used, n, prof, AUDIT_DELTAS[rule], false_ban=fb))
        r = run_router_audit(used, n, s, st, qs, delta=AUDIT_DELTAS[rule], trace=tr, false_ban=fb)
        fired = float(r["banned"].any())
        extra["audit"] = {"banned": r["banned"], "ban_round": r["ban_round"],
                          "honest_bans": r["honest_bans"], "idle_rounds": r["idle_rounds"],
                          "warm": r["warm"], "ref_radius": r["ref_radius"]}
    elif rule == "router_static":
        used = inst
        st = (Learner(used, n, s) if prof == "learning" else BL2.Average(used) if prof == "average"
              else BL2.ExploitDecay(used, n, prof.split("_")[1]))
        r = run_router(used, n, s, st, qs, rule="static", trace=tr)
        fired = 0.0
        extra["static_choice"] = r["static_choice"]
        if isinstance(st, BL2.ExploitDecay):
            extra.update(warmup_selections=st.warm, decay_selections=st.D)
    elif rule in ("plmesp", "mesp_scalar") and prof in ("exploit_slow", "exploit_fast"):
        used = flat if rule == "mesp_scalar" else inst
        st = BL2.ExploitDecay(used, n, prof.split("_")[1])     # same schedule the routers face; honest providers deliver mu
        run = MechanismRun(used, n, s)
        r = run.run(st, qs, trace=tr)
        r["utility_per_round"] = (r["T"] - r["C"]) / n
        fired = float(r["convictions"] > 0)
        extra["L"], extra["s_n"] = run.L, run.s
        extra.update(warmup_selections=st.warm, decay_selections=st.D, convictions=int(r["convictions"]),
                     compliant_convictions=int(r.get("compliant_convictions", 0)), first_switch_round=int(r.get("first_switch_round", -1)))
    elif prof == "learning":
        used = flat if rule in ("second_best", "mesp_scalar", "esmaeili") else inst
        st = Learner(used, n, s)
        if rule == "plmesp" or rule == "mesp_scalar":
            run = MechanismRun(used, n, s)
            r = run.run(st, qs, trace=tr)
            r["utility_per_round"] = (r["T"] - r["C"]) / n
            fired = float(r["convictions"] > 0)
            extra["L"], extra["s_n"] = run.L, run.s
        elif rule == "second_best":
            r = run_second_best(used, n, s, st, qs, gate_blind2=True, trace=tr)
            fired = float(r["monitor_fired"])
        elif rule == "esmaeili":
            r = run_single_observation_exclusion(used, n, s, st, qs, trace=tr)
            fired = float(r["exclusions"] > 0)
        elif rule in ROUTERS:
            r = run_router(used, n, s, st, qs, rule=ROUTERS[rule], trace=tr)
            fired = 0.0
        else:
            raise ValueError(rule)
    else:
        raise ValueError((rule, prof))
    if hasattr(st, "meta"):
        extra["strategy"] = st.meta()
    if tr is not None:
        tr.save(trace_path, {**meta, **extra, "result": r})
    served = float(np.mean(tr.agent != 255)) if tr is not None else np.nan
    learned = None
    conv = np.nan
    if isinstance(st, Learner):
        learned = {i: lg[-1]["arms"] for i, lg in st.log.items() if lg}
        conv = float(st.convergence()[0])
    return dict(revenue=r["revenue_per_round"], fired=fired, served=served,
                util=np.asarray(r["utility_per_round"], dtype=float), learned=learned,
                converged=conv)


def one_run(rule, prof, inst, flat, p, qs, n, s, trace_path, meta):
    if (rule, prof) in V2_MECH:
        r = AO2.one_run(rule, prof, inst, flat, p, qs, n, s, trace_path, meta)
        r.setdefault("served", np.nan)
        if trace_path and np.isnan(r["served"]):
            from trace import load
            r["served"] = float(np.mean(load(trace_path)["agent"] != 255))
        return r
    if (rule, prof) in V2_BASE:
        return BL2.one_run(rule, prof, inst, flat, qs, n, s, trace_path, meta)
    return one_run_new(rule, prof, inst, flat, p, qs, n, s, trace_path, meta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", required=True, help="label=ModelA|ModelB|...")
    ap.add_argument("--taskset", default="q7", choices=["q7", "merged5"])
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=20)
    ap.add_argument("--seed0", type=int, default=0)
    ap.add_argument("--orders", default=",".join(SYN_ORDERS))
    ap.add_argument("--rules", default=",".join(PROFILES))
    ap.add_argument("--profiles", default=None, help="restrict to these profiles")
    ap.add_argument("--out", required=True)
    ap.add_argument("--trace-dir", default=None)
    a = ap.parse_args()
    label, models = a.subset.split("=")
    models = models.split("|")
    inst, p, types = build_instance(models, a.taskset)
    flat = scalarize(inst)
    K = inst.K
    qs0 = draw_queries(inst, p, a.n, 0)
    base = dict(subset=label, models="|".join(models), K=K, n=a.n, nseeds=a.nseeds,
                taskset=a.taskset, oracle=oracle_per_round(inst, qs0),
                second_cap=second_capability_per_round(inst, qs0),
                honest_bench=honest_benchmark_per_round(inst, qs0))
    keep = set(a.profiles.split(",")) if a.profiles else None
    rows = []
    for order in a.orders.split(","):
        for rule in a.rules.split(","):
            for prof in PROFILES[rule]:
                if keep is not None and prof not in keep:
                    continue
                res = []
                for s in range(a.seed0, a.seed0 + a.nseeds):
                    qs, qmeta = queries_for(inst, p, a.n, s, order, a.taskset, types)
                    tp, meta = None, None
                    if a.trace_dir:
                        d = os.path.join(a.trace_dir, a.taskset, label, str(a.n), order)
                        os.makedirs(d, exist_ok=True)
                        tp = os.path.join(d, f"{rule}_{prof}_seed{s:02d}.npz")
                        meta = dict(subset=label, models=models, contexts=types, masses=p, M=inst.M,
                                    mu=inst.mu, honest=inst.honest, n=a.n, seed=s, order=order,
                                    mech=rule, profile=prof, cost="linear phi(m)=m", taskset=a.taskset,
                                    honest_provider=HONEST, cheap_substitute=CHEAP, driver="run_v3",
                                    **qmeta)
                    res.append(one_run(rule, prof, inst, flat, p, qs, a.n, s, tp, meta))
                u = np.mean([r["util"] for r in res], axis=0)
                row = {**base, "order": order, "mech": rule, "profile": prof,
                       "revenue_per_round": float(np.mean([r["revenue"] for r in res])),
                       "revenue_sd": float(np.std([r["revenue"] for r in res])),
                       "fire_rate": float(np.mean([r["fired"] for r in res])),
                       "undelegated_fraction": 1.0 - float(np.nanmean([r.get("served", np.nan) for r in res]))
                       if any(np.isfinite(r.get("served", np.nan)) for r in res) else np.nan,
                       "converged_share": float(np.nanmean([r.get("converged", np.nan) for r in res]))
                       if any(np.isfinite(r.get("converged", np.nan)) for r in res) else np.nan,
                       **{f"util_{j}": u[j] for j in range(K)}}
                rows.append(row)
                pd.DataFrame(rows).to_csv(a.out, index=False)
            print(f"done {label} {a.taskset} n={a.n} {order} {rule}", flush=True)


if __name__ == "__main__":
    main()
