"""J4 data: how Cao et al.'s mechanism splits the horizon on the J instance as n grows, under the
honest reference profile.  Exploration and blind trust are unpriced and unmonitored; only the
exploitation phase announces a price and runs their fixed-slack monitor (their line 16).

  python j_cao_phases.py --out <csv>  [--ns 20000,50000,100000,300000,1000000] [--seeds 0-2]
"""
import argparse, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_v3 import build_instance                       # noqa: E402
from baseline_secondbest import scalarize               # noqa: E402
from mechanisms import ProfileStrategy, run_second_best  # noqa: E402
from j_traces import MODELS, parse_seeds                # noqa: E402

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", default="20000,50000,100000,300000,1000000")
    ap.add_argument("--seeds", default="0-2")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    inst, p = build_instance(MODELS, "q7")[:2]; flat = scalarize(inst)
    tm = (flat.M >= flat.M.max(axis=1, keepdims=True) - 1e-12)
    st = ProfileStrategy(flat, ["proposed"] * flat.K, tm)
    rows = []
    for n in [int(x) for x in a.ns.split(",")]:
        for seed in parse_seeds(a.seeds):
            r = run_second_best(flat, n, seed, st, np.zeros(n, dtype=np.int64), gate_blind2=True)
            pr = r["phase_rounds"]
            rows.append(dict(n=n, seed=seed, B=int(r["B"]), price=float(r["price"]), winner=int(r["winner"]),
                             explore=int(pr["explore"]), exploit=int(pr["exploit"]), blind=int(pr["blind1"] + pr["blind2"]),
                             undelegated=int(pr["undelegated"]), fired=bool(r["monitor_fired"]),
                             monitor_slack=float((1.0 + r["price"]) * r["M_slack"] / 3.0)))
            print(rows[-1], flush=True)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)

if __name__ == "__main__":
    main()
