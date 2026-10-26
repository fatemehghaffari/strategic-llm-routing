"""Collect the exact bid-profile computations into the two tables used in REPORT.md Section 8."""
from __future__ import annotations
import json, sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
rows = []
for f in sorted(OUT.glob("bp_*.json")):
    r = json.loads(f.read_text())
    if r["n"] < 1000:
        continue
    rows.append(r)

print("| instance | bids (tag) | n | L_n | revenue/round | agent | base u/round | exploit (total) | exploit/round | thm const |")
print("| - | - | - | - | - | - | - | - | - | - |")
for r in sorted(rows, key=lambda r: (r["alias"], r["tag"], r["n"])):
    rev = r["revenue"]
    for i, a in sorted(r["agents"].items(), key=lambda kv: int(kv[0])):
        n = r["n"]
        print(f"| {r['alias']} | {a['bids']} ({r['tag']}) | {n} | {a['L_n']} | "
              f"{rev['revenue_LB_per_round']:.4f} | {i}{'H' if a['honest_agent'] else ''} | "
              f"[{a['base_LB']/n:.4f}, {a['base_UB']/n:.4f}] | "
              f"[{a['exploit_LB']:.1f}, {a['exploit_UB']:.1f}] | "
              f"[{a['exploit_LB_per_round']:.5f}, {a['exploit_UB_per_round']:.5f}] | "
              f"{a['theorem_constant_top']:.0f} |")

print()
print("Coalition comparison (base utility, totals): tag pairs at equal (instance, n).")
by = {}
for r in rows:
    by[(r["alias"], r["tag"], r["n"])] = r
print("| instance | n | agent | u at star [LB,UB] | u at deviated [LB,UB] | gain (LB) | L_n |")
print("| - | - | - | - | - | - | - |")
for (alias, tag, n), r in sorted(by.items()):
    if tag == "star":
        continue
    s = by.get((alias, "star", n))
    if s is None:
        continue
    for i in sorted(r["agents"], key=int):
        a, b = s["agents"][i], r["agents"][i]
        print(f"| {alias} ({tag}) | {n} | {i} | [{a['base_LB']:.1f}, {a['base_UB']:.1f}] | "
              f"[{b['base_LB']:.1f}, {b['base_UB']:.1f}] | {b['base_LB'] - a['base_UB']:.1f} | {a['L_n']} |")
