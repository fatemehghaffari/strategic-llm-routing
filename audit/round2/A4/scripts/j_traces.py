"""J: per-round traces of ONE declared deviation against the reference profile, with common
random numbers, for the dynamic figures (J1 cumulative gain, J2 gain per round elapsed, J3 the
monitor's deficit against its tolerance, J5 the same at a horizon where Cao et al.'s priced
phase exists).

Single context (the scalar mechanism on the scalarised headline triple), so the fixed-shade
deviation is well defined. Deviator = the pointwise-top provider (GPT-4; Mixtral is honest).

  python j_traces.py --n 20000 --seeds 0-9 --out <dir>
  python j_traces.py --n 300000 --seeds 3 --mechs second_best,mesp_scalar --out <dir>

Profiles, per mechanism and seed (same seed = same uniform stream):
  mesp_scalar  proposed (reference) | boundary | shadeprice<d> | shadeall<d>
  second_best  proposed (reference) | shadeprice<d> | shadeall<d>      (Cao et al., WWW 2026)
  router_ucb, router_eps  capability (reference) | undercut0.02 | undercut0.05 | shadeall<d>
shadeall<d> is the common deviation: bid the capability, then deliver d below what the
reference profile delivers in every later served round (the announced price while priced,
the capability otherwise).  Writes one trace .npz per run plus summary_<seeds>.csv and
instance.json; nothing in experiments/ is touched.
"""
import argparse, os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_v3 import build_instance                       # noqa: E402
from baseline_secondbest import scalarize               # noqa: E402
from mechanisms import MechanismRun, ProfileStrategy, design_constants, run_router, run_second_best  # noqa: E402
import baselines_v2 as BL2                              # noqa: E402
from trace import Trace                                 # noqa: E402

MODELS = ["Mixtral-8x7B", "GPT-4", "Yi-34B"]   # honest Mixtral present; the top provider GPT-4 is strategic, so deviations are feasible
ROUTER_RULE = {"router_ucb": BL2.RULES["router_ucb"], "router_eps": BL2.RULES["router_eps"]}
ALL_MECHS = ("mesp_scalar", "second_best", "router_ucb", "router_eps")

def parse_seeds(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--seeds", default="0-9")
    ap.add_argument("--shades", default="0.05,0.10")
    ap.add_argument("--mechs", default=",".join(ALL_MECHS))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    seeds, mechs = parse_seeds(a.seeds), a.mechs.split(",")
    shades = [float(x) for x in a.shades.split(",")]
    inst, p = build_instance(MODELS, "q7")[:2]
    flat = scalarize(inst)
    K = flat.K
    tm = (flat.M >= flat.M.max(axis=1, keepdims=True) - 1e-12)
    second = np.sort(flat.M, axis=1)[:, -2]
    dev = int(np.argmax(flat.M[0]))                      # pointwise-top provider in the scalar instance
    L, s, b = design_constants(a.n, K)
    rows = []
    for seed in seeds:
        qs = np.zeros(a.n, dtype=np.int64)                # single context
        # ---- the mechanism ----
        if "mesp_scalar" in mechs:
            profs = ([("proposed", "proposed"), ("boundary", "boundary")]
                     + [(f"shade{sh:.2f}", f"shadeprice{sh:.4f}") for sh in shades]
                     + [(f"shadeall{sh:.2f}", f"shadeall{sh:.4f}") for sh in shades])
            for name, opt in profs:
                opts = ["proposed"] * K; opts[dev] = opt
                st = ProfileStrategy(flat, opts, tm, second=second)
                tr = Trace(qs)
                run = MechanismRun(flat, a.n, seed)
                r = run.run(st, qs, trace=tr)
                loc = run.locals[0]
                meta = dict(mech="mesp_scalar", profile=name, deviator=dev, seed=seed, n=a.n, L=run.L,
                            s_n=run.s, tau=float(loc.tau), W=int(loc.W), conv_r=int(loc.conv_r),
                            M=flat.M[0].tolist(), mu=flat.mu[0].tolist(), models=MODELS)
                tr.save(os.path.join(a.out, f"mesp_scalar_{name}_seed{seed:02d}.npz"), meta)
                rows.append(dict(mech="mesp_scalar", profile=name, seed=seed, n=a.n, deviator=dev, W=int(loc.W),
                                 tau=float(loc.tau), conv_r=int(loc.conv_r), convictions=int(r["convictions"]),
                                 fired_at=-1, priced_rounds=int(r["phase_rounds"]["primary"]),
                                 unpriced_rounds=int(r["phase_rounds"]["fallback"]), undelegated=0,
                                 revenue=float(r["revenue_per_round"]), dev_util=float(((r["T"]-r["C"])/a.n)[dev])))
        # ---- Cao et al.'s mechanism under the same deviations (its own announced value as the price) ----
        if "second_best" in mechs:
            profs = ([("proposed", "proposed")] + [(f"shade{sh:.2f}", f"shadeprice{sh:.4f}") for sh in shades]
                     + [(f"shadeall{sh:.2f}", f"shadeall{sh:.4f}") for sh in shades])
            for name, opt in profs:
                opts = ["proposed"] * K; opts[dev] = opt
                st = ProfileStrategy(flat, opts, tm, second=second)
                tr = Trace(qs)
                r = run_second_best(flat, a.n, seed, st, qs, gate_blind2=True, trace=tr)
                pr = r["phase_rounds"]
                tr.save(os.path.join(a.out, f"second_best_{name}_seed{seed:02d}.npz"),
                        dict(mech="second_best", profile=name, deviator=dev, seed=seed, n=a.n, models=MODELS,
                             fired=bool(r["monitor_fired"]), fired_at=int(r["fired_at_exploitation_round"]),
                             winner=int(r["winner"]), phase_rounds={k: int(v) for k, v in pr.items()},
                             price_signal=float(r["announced_second_best_utility"] + r["price"]) if r["winner"] >= 0 else None,
                             M_slack=float(r["M_slack"]), B=int(r["B"])))
                rows.append(dict(mech="second_best", profile=name, seed=seed, n=a.n, deviator=dev, W=int(r["winner"]),
                                 tau=np.nan, conv_r=-1, convictions=int(bool(r["monitor_fired"])),
                                 fired_at=int(r["fired_at_exploitation_round"]), priced_rounds=int(pr["exploit"]),
                                 unpriced_rounds=int(pr["explore"] + pr["blind1"] + pr["blind2"]), undelegated=int(pr["undelegated"]),
                                 revenue=float(r["revenue_per_round"]),
                                 dev_util=float(np.asarray(r["utility_per_round"], dtype=float)[dev])))
        # ---- the routers (same uniform stream seed+7919 inside run_router) ----
        for rule in [m for m in ROUTER_RULE if m in mechs]:
            profs = ["capability", "undercut0.02", "undercut0.05"] + [f"shadeall{sh:.4f}" for sh in shades]
            for prof in profs:
                opts = ["theta1.00"] * K
                if prof != "capability": opts[dev] = prof
                name = prof if not prof.startswith("shadeall") else f"shadeall{float(prof[8:]):.2f}"
                st = ProfileStrategy(flat, opts, tm, second=second)
                tr = Trace(qs)
                r = run_router(flat, a.n, seed, st, qs, rule=ROUTER_RULE[rule], trace=tr)
                tr.save(os.path.join(a.out, f"{rule}_{name}_seed{seed:02d}.npz"),
                        dict(mech=rule, profile=name, deviator=dev, seed=seed, n=a.n, models=MODELS))
                rows.append(dict(mech=rule, profile=name, seed=seed, n=a.n, deviator=dev, W=-1, tau=np.nan, conv_r=-1,
                                 convictions=0, fired_at=-1, priced_rounds=0, unpriced_rounds=a.n, undelegated=0,
                                 revenue=float(r["revenue_per_round"]),
                                 dev_util=float(np.asarray(r["utility_per_round"], dtype=float)[dev])))
        print(f"seed {seed} done", flush=True)
    tag = a.seeds.replace(",", "_")
    pd.DataFrame(rows).to_csv(os.path.join(a.out, f"summary_seeds{tag}.csv"), index=False)
    json.dump(dict(models=MODELS, M=flat.M[0].tolist(), mu=flat.mu[0].tolist(), honest=flat.honest.tolist(),
                   deviator=dev, n=a.n, L=L, s_n=s, c_boundary=float((np.log(2.0)+4*np.log(a.n))/2)),
              open(os.path.join(a.out, "instance.json"), "w"), indent=1)
    print(pd.DataFrame(rows).groupby(["mech","profile"])[["revenue","dev_util","convictions","priced_rounds"]].mean().round(4).to_string())

if __name__ == "__main__":
    main()
