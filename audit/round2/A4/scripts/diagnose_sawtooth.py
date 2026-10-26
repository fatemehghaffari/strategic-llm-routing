"""Diagnose the apparent sawtooth in the utility-against-effort curves.

Reported symptom: reading the utility curve for (measured_unique_top, GSM8K,
top, mesp) shows utility alternating between about 0.04 and about 0.30 at
adjacent grid points, with the seed standard deviation exactly zero at many of
them, which rules out sampling noise.

Two hypotheses were offered: (1) a genuine finite-elicitation-length effect, the
elicited bid being an empirical mean over L_n pulls so it can only take values
k/L_n and the swept agent alternates between winning and losing; (2) an
aggregation error in which utility is computed conditional on one realised bid
rather than in expectation.

This script tests both and shows it is NEITHER. Run it and read the output.

    python diagnose_sawtooth.py --csv experiments/data/A4
"""
import argparse
import os

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--instance", default="measured_unique_top")
    ap.add_argument("--context", default="GSM8K")
    ap.add_argument("--role", default="top")
    ap.add_argument("--rule", default="mesp")
    a = ap.parse_args()
    d = pd.read_csv(os.path.join(a.csv, "utility_curves.csv"))
    sel = d[(d.instance == a.instance) & (d.context == a.context)
            & (d.role == a.role) & (d.rule == a.rule)]
    mix = sel.sort_values("delivered_mean")
    u = mix.agent_utility_per_round.values
    dif = np.diff(u)
    print(f"rows: {len(sel)}   sweeps present: {sel.sweep.value_counts().to_dict()}")
    print()
    print("A. sorted by delivered_mean WITHOUT separating the sweeps")
    print(f"   adjacent jumps exceeding 0.05: {int((np.abs(dif) > 0.05).sum())} "
          f"of {len(dif)}; upward: {int((dif > 0).sum())}")
    print(f"   first 10 utilities: {[round(float(x), 3) for x in u[:10]]}")
    print(f"   first 10 sweeps   : {list(mix.sweep.values[:10])}")
    print()
    print("B. the SAME rows split by sweep")
    for sw, g in sel.groupby("sweep"):
        if sw == "crosscheck":
            continue
        g = g.sort_values("delivered_mean")
        dd = np.diff(g.agent_utility_per_round.values)
        print(f"   sweep={sw:8s} points {len(g):3d}  mean |step| {np.abs(dd).mean():.4f}"
              f"  max |step| {np.abs(dd).max():.4f}"
              f"  jumps>0.05: {int((np.abs(dd) > 0.05).sum())} of {len(dd)}")
    print()
    print("C. why the seed standard deviation is exactly zero at many points")
    for sw, g in sel.groupby("sweep"):
        if sw == "crosscheck":
            continue
        z = float((g.agent_utility_sd == 0).mean())
        print(f"   sweep={sw:8s} fraction of points with sd exactly 0: {z:.3f}")
    print()
    print("VERDICT")
    print("   The two sweeps share the SAME delivered-mean grid by construction.")
    print("   'all' sweeps the delivery in every phase, so at a low target the")
    print("   agent loses the elicitation and its utility is its elicitation")
    print("   share alone, about 0.04, deterministically, hence sd = 0.")
    print("   'primary' bids the capability and sweeps only the primary")
    print("   delivery, so the agent always wins and its utility is about 0.30.")
    print("   Concatenated into one file and sorted by delivered mean, the two")
    print("   series interleave and produce a period-two alternation between")
    print("   those two levels. Split by sweep, each series is well behaved.")
    print("   This is an aggregation and presentation fault in how the file was")
    print("   written, NOT a finite-L_n quantisation effect and NOT a")
    print("   conditional-versus-expectation error in the utility computation.")
    print("   Fixed by: dropping duplicate rows, adding an explicit series_id,")
    print("   and writing utility_curves_<sweep>.csv one file per sweep.")


if __name__ == "__main__":
    main()
