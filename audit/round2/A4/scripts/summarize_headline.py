"""Print the headline comparison in the shape section 4 of REPORT.md needs."""
import argparse, os
import numpy as np, pandas as pd
pd.set_option("display.width", 260)

ap = argparse.ArgumentParser(); ap.add_argument("--csv", required=True); a = ap.parse_args()
D = a.csv
hs = pd.read_csv(os.path.join(D, "headline_summary.csv"))
hw = pd.read_csv(os.path.join(D, "headline_worlds.csv"))
ex = pd.read_csv(os.path.join(D, "exploitability.csv"))
M = ["plmesp", "mesp_scalar", "router_greedy", "router_eps", "router_ucb"]

print("=== A. two worlds, revenue per round, mean over the 3 triples ===")
for fs in sorted(hs.family_set.unique()):
    for al in sorted(hs.alpha.unique()):
        s = hs[(hs.family_set == fs) & (hs.alpha == al)]
        if not len(s): continue
        t = s.groupby("mech")[["nonstrategic", "strategic", "degradation",
                               "oracle", "second_cap", "honest_bench"]].mean()
        t = t.reindex([m for m in M if m in t.index])
        print(f"\n-- {fs} alpha={al}"); print(t.round(4).to_string())

print("\n=== B. strategic-world equilibrium profiles found ===")
w = hw[hw.world == "strategic"]
print(w.groupby(["family_set", "alpha", "mech"])["profile"].apply(
    lambda s: s.value_counts().index[0]).to_string())
print("\nfixed point reached:", w.groupby("mech").is_fixed_point.mean().round(3).to_dict())

print("\n=== C. exploitability: best deviation found at the proposed profile ===")
t = ex.pivot_table(index=["family_set", "mech"], columns="alpha",
                   values="best_gain_per_round")
print(t.round(4).to_string())
print("\nwhich deviation wins, counts:")
print(ex.groupby(["mech", "deviation"]).size().unstack(fill_value=0).to_string())

print("\n=== D. compliant convictions at the proposed profile (count per run) ===")
cc = hw[hw.world == "proposed"].groupby(["family_set", "mech"])["compliant_convictions"].mean()
print(cc.round(3).to_string())
print("\n=== E. locals past elicitation ===")
print(hw[hw.world == "proposed"].groupby("family_set")[
    ["locals_past_elicitation", "locals_total"]].mean().round(2).to_string())
print("\n=== F. revenue at the proposed profile ===")
pr = hw[hw.world == "proposed"].groupby(["family_set", "alpha", "mech"])["revenue_per_round"].mean()
print(pr.round(4).unstack().to_string())
