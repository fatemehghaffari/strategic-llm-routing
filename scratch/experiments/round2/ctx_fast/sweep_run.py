"""One CG-MESP episode at one (instance, horizon, behaviour profile, seed); writes one JSON row.

The mechanism runs at its OWN tuned parameters (h_n = 1/ceil(n^{1/(D+3)}), L_n = ceil(n^{2/(D+3)}),
rho_n = sqrt(D) h_n log(en)).  Nothing is tuned by hand anywhere in this sweep.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cgfast  # noqa: E402

CONFIGS = {
    "proposed":       dict(dev=None, kind=None, alpha_ride=0.0, joint=False),
    "underbid":       dict(dev=0, kind="underbid", alpha_ride=0.0, joint=False),
    "rider25":        dict(dev=0, kind="rider", alpha_ride=0.25, joint=False),
    "rider50":        dict(dev=0, kind="rider", alpha_ride=0.5, joint=False),
    "rider100":       dict(dev=0, kind="rider", alpha_ride=1.0, joint=False),
    "both":           dict(dev=0, kind="both", alpha_ride=0.5, joint=False),
    "crash":          dict(dev=0, kind="crash", alpha_ride=0.0, joint=False),
    "sabotage_joint": dict(dev=0, kind="sabotage", alpha_ride=0.0, joint=True),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inst", required=True)
    ap.add_argument("--logn", type=float, required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--d", type=int, default=0, help="dimension of the common context space; "
                                                     "0 means the earlier reading d = K")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--save-tau", action="store_true")
    a = ap.parse_args()
    n = int(round(10 ** a.logn))
    os.makedirs(a.outdir, exist_ok=True)
    dtag = "" if a.d == 0 else f"_d{a.d}"
    tag = f"{a.inst}{dtag}_lg{a.logn:.2f}_{a.config}_s{a.seed}"
    dst = os.path.join(a.outdir, tag + ".json")
    if os.path.exists(dst):
        print("already done:", dst)
        return
    t0 = time.time()
    r = cgfast.run(a.inst, n, tuned=True, seed=a.seed, d=(a.d or None), **CONFIGS[a.config])
    wall = time.time() - t0
    taus = r.pop("_taus")
    tix = r.pop("_tauidx")
    vis = r.pop("_visits")
    r["config"] = a.config
    r["logn"] = a.logn
    r["wall_s"] = wall
    r["ns_per_round"] = wall / n * 1e9
    r["host"] = os.uname().nodename
    r["slurm_job"] = os.environ.get("SLURM_JOB_ID", "")
    r["kernel"] = os.environ.get("CGMESP_LIB", "libcgmesp.so")
    # floating-point drift diagnostics at this horizon
    r["bench_M2_neumaier_minus_naive"] = r["bench_M2"] - r["bench_M2_naive"]
    r["bench_honest_neumaier_minus_naive"] = r["bench_honest"] - r["bench_honest_naive"]
    r["util_neumaier_minus_naive"] = [u - v for u, v in zip(r["util"], r["util_naive"])]
    if a.save_tau and taus.size:
        np.savez_compressed(os.path.join(a.outdir, tag + "_tau.npz"),
                            tau=taus, cellidx=tix, visits=vis)
        q = np.quantile(taus, [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
        r["tau_quantiles"] = [float(x) for x in q]
    with open(dst + ".tmp", "w") as f:
        json.dump(r, f)
    os.replace(dst + ".tmp", dst)
    print(json.dumps({k: r[k] for k in ("inst", "logn", "config", "seed", "n", "g", "J", "L", "sigma",
                                        "awarded", "tau_pos", "positive_price_share", "mean_tau",
                                        "switches", "rev", "bench_M2", "bench_honest", "wall_s",
                                        "ns_per_round")}))


if __name__ == "__main__":
    main()
