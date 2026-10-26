import glob, os, pandas as pd, numpy as np
B = "<scratch>/B/raw"
fs = [f for f in glob.glob(B + "/i1_*merged5_*.csv")]
d = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
sel = [("router_static", p) for p in ("exploit_slow", "exploit_fast", "average")] + \
      [(r, p) for r in ("router_ucb", "router_greedy", "router_eps") for p in ("exploit_slow", "exploit_fast", "average")] + \
      [("plmesp", "plmesp_star")]
d = d[[ (m, p) in sel for m, p in zip(d.mech, d.profile)]].copy()
d["ratio"] = d.revenue_per_round / d.oracle
cnt = d.groupby(["order", "n", "mech", "profile"]).size()
print(cnt.unstack(["order", "n"]))
for order in ("iid", "real"):
    print(f"\n### order = {order}: mean over 10 subsets, revenue per round (revenue / oracle), 20 seeds per subset")
    print("| mech | profile | n = 3e5 | n = 3e6 |\n|---|---|---|---|")
    for m, p in sel:
        cells = []
        for n in (300000, 3000000):
            g = d[(d.order == order) & (d.n == n) & (d.mech == m) & (d.profile == p)]
            cells.append(f"{g.revenue_per_round.mean():.4f} ({g.ratio.mean():.3f}) [{len(g)}]" if len(g) else "n/a")
        print(f"| {m} | {p} | " + " | ".join(cells) + " |")
    o = d[(d.order == order)].drop_duplicates(["subset", "n"])
    print("oracle mean:", o.groupby("n").oracle.mean().round(4).to_dict(), "honest_bench:", o.groupby("n").honest_bench.mean().round(4).to_dict())
# per-subset, 3e6 iid
for order in ("iid", "real"):
  for n in (300000, 3000000):
    g = d[(d.order == order) & (d.n == n)]
    t = g.pivot_table(index="subset", columns=["mech", "profile"], values="revenue_per_round")
    t.columns = [f"{a.replace('router_','')}/{b}" for a, b in t.columns]
    print(f"\nper subset {order} n={n}"); print(t.round(3).to_string())
# learning i2
L = pd.concat([pd.read_csv(f) for f in glob.glob(B + "/i2_*router_static*.csv")], ignore_index=True)
L["ratio"] = L.revenue_per_round / L.oracle
print("\nrouter_static learning 3e6:"); print(L.groupby(["taskset", "order"])[["revenue_per_round", "ratio", "converged_share"]].mean().round(4)); print(L.groupby(["taskset","order"]).size())
