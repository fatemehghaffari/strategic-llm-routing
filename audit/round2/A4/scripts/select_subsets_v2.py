"""Fixed rule for the v2 arrival-order subsets, applied before any v2 run.
Honest provider fixed in advance: Mixtral-8x7B (open weights, self-hostable). Every subset contains it.
Among Q7 subsets containing Mixtral-8x7B, for K = 3, 4, 5 take the subsets at the 10th, 50th and 90th
percentiles of gap = E_x M_(2)(x) - tau, tau the second-largest pooled mean (Cao's announced value),
plus the K = 6 median: 10 subsets."""
import itertools, os, numpy as np, pandas as pd
D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../experiments/data/A4"))
cap = pd.read_csv(f"{D}/capabilities_finite_5shot.csv"); m = pd.read_csv(f"{D}/context_masses_5shot.csv").set_index("context")
F = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]
t = cap[cap.context.isin(F)].pivot(index="model", columns="context", values="M")[F]
w = m.loc[F, "n_queries"].values.astype(float); w /= w.sum()
others = [x for x in t.index if x != "Mixtral-8x7B"]
rows = []
for k in range(3, 7):
    for S in itertools.combinations(others, k - 1):
        S = ("Mixtral-8x7B",) + S
        M = t.loc[list(S)].values.T; avg = w @ M
        rows.append(dict(K=k, models="|".join(S), gap=w @ np.sort(M, 1)[:, -2] - np.sort(avg)[-2]))
d = pd.DataFrame(rows); out = []
for k, qs in [(3, [.1, .5, .9]), (4, [.1, .5, .9]), (5, [.1, .5, .9]), (6, [.5])]:
    g = d[d.K == k].sort_values(["gap", "models"]).reset_index(drop=True)
    for q in qs:
        r = g.iloc[int(round(q * (len(g) - 1)))]; out.append((f"k{k}_q{int(q*100)}", r.models, r.gap))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "arrival_order_subsets_v2.txt"), "w") as f:
    for lab, ms, _ in out: f.write(f"{lab}={ms}\n")
for o in out: print(o[0], round(o[2], 4), o[1])
