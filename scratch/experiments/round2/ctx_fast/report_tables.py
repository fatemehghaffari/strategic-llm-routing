"""Emit the markdown tables of audit/round2/A3/THRESHOLD_REPORT.md straight from the summary CSV,
so that no number in the report is transcribed by hand."""
from __future__ import annotations

import argparse
import csv
import json
import math
import os

DEVS = ["underbid", "rider25", "rider50", "rider100", "both", "crash"]


def f(r, k, d=4, default="-"):
    v = r.get(k, "")
    if v in ("", None):
        return default
    try:
        x = float(v)
    except ValueError:
        return str(v)
    return default if math.isnan(x) else f"{x:.{d}f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--verification", nargs="*", default=[])
    a = ap.parse_args()
    rows = list(csv.DictReader(open(os.path.join(a.csv, "threshold_summary.csv"))))
    rows.sort(key=lambda r: (int(r["d"]), r["inst"], float(r["logn"])))
    dims = sorted({int(r["d"]) for r in rows})

    print("**Coverage.** Horizons for which the proposed profile has returned, "
          "by context dimension and instance:\n")
    for dim in dims:
        for inst in ("C", "E", "D", "F", "G"):
            rs = [r for r in rows if r["inst"] == inst and int(r["d"]) == dim]
            if rs:
                print(f"* d = {dim}, instance {inst} (K = {rs[0]['K']}): " +
                      ", ".join(f"{float(r['logn']):.2f}" for r in rs))
    print()

    for dim, inst in [(d, i) for d in dims for i in ("C", "E", "D", "F", "G")]:
        rs = [r for r in rows if r["inst"] == inst and int(r["d"]) == dim]
        if not rs:
            continue
        print(f"\n### d = {dim}, instance {inst} (K = {rs[0]['K']})\n")
        print("| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor "
              "firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | "
              "(B) deficit/n | (C) deficit/n |")
        print("|" + "--:|" * 16)
        for r in rs:
            n = float(r["n"])
            bg = r.get("best_searched_gain", "")
            bgn = (f"{max(float(bg), 0.0) / n:.5f}"
                   if bg not in ("", "nan") and not math.isnan(float(bg)) else "-")
            bd = f"{float(r['revenue_deficit_B']) / n:.4f}" if r.get("revenue_deficit_B") else "-"
            cd = (f"{float(r['honest_deficit_C']) / n:.4f}"
                  if r.get("honest_deficit_C", "") not in ("", None) else "-")
            print(f"| {float(r['logn']):.2f} | {r['g']} | {int(r['J']):,} | {int(r['L']):,} | "
                  f"{f(r, 'sigma_n', 3)} | {f(r, 'positive_price_share', 3)} | {f(r, 'mean_tau')} | "
                  f"{r['switches_proposed']} | {f(r, 'rev_per_round')} | {f(r, 'bench_M2_per_round')} | "
                  f"{f(r, 'boundA_over_n', 3)} | {f(r, 'slackB_over_n', 3)} | {f(r, 'slackC_over_n', 3)} | "
                  f"{bgn} | {bd} | {cd} |".replace(",", " "))

    print("\n### Realised gain of each deviation, per round (paired with the proposed profile, same seed)\n")
    print("| d | instance | log10 n | " + " | ".join(DEVS) + " | part (A) budget / n |")
    print("|" + "--:|" * (len(DEVS) + 4))
    for r in rows:
        n = float(r["n"])
        cells = []
        any_c = False
        for c in DEVS:
            v = r.get(f"gain_{c}", "")
            if v in ("", None):
                cells.append("-")
            else:
                any_c = True
                cells.append(f"{float(v) / n:.5f}")
        if any_c:
            print(f"| {r['d']} | {r['inst']} | {float(r['logn']):.2f} | " + " | ".join(cells) +
                  f" | {float(r['boundA']) / n:.3f} |")

    print("\n### The monitor: conviction of a crashing winner, and false alarms\n")
    print("| d | instance | log10 n | share of regions with tau > 0 | firings under the proposed profile | "
          "regions convicted, crash deviation | regions convicted, ride the boundary at scale 1 | "
          "false alarms, all profiles |")
    print("|" + "--:|" * 8)
    for r in rows:
        fa = sum(int(r.get(f"false_switches_{c}", 0) or 0)
                 for c in ("crash", "rider100", "rider50", "underbid", "both", "sabotage_joint"))
        fa += int(r["false_switches_proposed"])
        print(f"| {r['d']} | {r['inst']} | {float(r['logn']):.2f} | {f(r, 'positive_price_share', 3)} | "
              f"{r['switches_proposed']} | {f(r, 'conviction_share_crash', 3)} | "
              f"{f(r, 'conviction_share_rider100', 3)} | {fa} |")

    print("\n### Numerical hygiene: compensated minus naive floating-point sum of the benchmark\n")
    print("| d | instance | log10 n | n | Neumaier minus naive, benchmark sum | as a share of the sum |")
    print("|" + "--:|" * 6)
    for r in rows:
        n = float(r["n"])
        dr = float(r.get("bench_M2_fp_drift", 0.0) or 0.0)
        tot = float(r["bench_M2_per_round"]) * n
        print(f"| {r['d']} | {r['inst']} | {float(r['logn']):.2f} | {int(n):,} | {dr:.3e} | "
              f"{abs(dr) / max(tot, 1):.2e} |"
              .replace(",", " "))

    for p in a.verification:
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        print(f"\n### Verification file `{os.path.basename(p)}`: {d['n_cases'] - d['n_fail']} of "
              f"{d['n_cases']} cases bit-identical, {d['n_fail']} failures")
        tot = sum(r["tag"]["n"] for r in d["rows"])
        sw = sum(r["ref_switches"] for r in d["rows"])
        v2 = sum(r["ref_viol_P2"] for r in d["rows"])
        v4 = sum(r.get("ref_viol_P4", 0) for r in d["rows"])
        aw = sum(r["ref_awarded"] for r in d["rows"])
        s3 = sum(r.get("fast_stage3", 0) for r in d["rows"])
        print(f"\n- rounds simulated by both implementations: {tot:,}".replace(",", " "))
        print(f"- awarded cubes: {aw:,}; monitor firings: {sw}; Stage-3 (fallback) rounds: {s3:,}"
              .replace(",", " "))
        print(f"- Lemma P2 violations counted: {v2}; Lemma P4 violations counted: {v4}")


if __name__ == "__main__":
    main()
