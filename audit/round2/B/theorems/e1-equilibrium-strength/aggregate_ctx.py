"""Tables for the profile-local computations (REPORT.md Part II)."""
from __future__ import annotations
import json, sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
rows = [json.loads(f.read_text()) for f in sorted(OUT.glob("ctx_*.json"))]

print("| instance | tag | n | profile | V_z | N_z | bids | revenue/visit | agent | exploit at z | base u at z |")
print("| - | - | - | - | - | - | - | - | - | - | - |")
for r in sorted(rows, key=lambda r: (r["instance"], r["tag"], r["n"])):
    for p in r["profiles"]:
        for i, a in sorted(p["agents"].items(), key=lambda kv: int(kv[0])):
            print(f"| {r['instance']} | {r['tag']} | {r['n']} | {p['z']} | {p['V_z']} | {p['N_z']} | "
                  f"{p['bids']} | {p['revenue']['revenue_LB'] / max(p['V_z'],1):.4f} | {i} | "
                  f"[{a['exploit_LB']:.1f}, {a['exploit_UB']:.1f}] | [{a['base_LB']:.1f}, {a['base_UB']:.1f}] |")
print()
print("| instance | tag | n | revenue/round | agent | total exploit | total exploit/round | base utility |")
print("| - | - | - | - | - | - | - | - |")
for r in sorted(rows, key=lambda r: (r["instance"], r["tag"], r["n"])):
    t = r["totals"]
    for i, a in sorted(t["agents"].items(), key=lambda kv: int(kv[0])):
        print(f"| {r['instance']} | {r['tag']} | {r['n']} | {t['revenue_LB_per_round']:.4f} | {i} | "
              f"[{a['exploit_LB']:.1f}, {a['exploit_UB']:.1f}] | "
              f"[{a['exploit_LB_per_round']:.5f}, {a['exploit_UB_per_round']:.5f}] | "
              f"[{a['base_LB']:.1f}, {a['base_UB']:.1f}] |")
print()
print("Coalition gains (base utility, totals), deviated minus star at equal (instance, n):")
by = {(r["instance"], r["tag"], r["n"]): r for r in rows}
for (inst, tag, n), r in sorted(by.items()):
    if tag == "star":
        continue
    s = by.get((inst, "star", n))
    if s is None:
        continue
    for i in sorted(r["totals"]["agents"], key=int):
        a, b = s["totals"]["agents"][i], r["totals"]["agents"][i]
        print(f"  {inst} {tag} n={n} agent {i}: {a['base_LB']:.1f} -> {b['base_LB']:.1f} "
              f"(gain {b['base_LB'] - a['base_UB']:+.1f}); revenue/round "
              f"{s['totals']['revenue_LB_per_round']:.4f} -> {r['totals']['revenue_LB_per_round']:.4f}")
