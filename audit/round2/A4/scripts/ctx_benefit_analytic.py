"""Step 1: where can a contextual second-price rule beat a scalar one, on measured capabilities?
Per subset S of the 11 RouterBench models and context set (Q3/Q7, 5-shot, empirical masses):
  ctx   = E_x M_(2)(x)                      contextual second price (PL-MESP asymptote)
  scl   = E_x min(tau, M_W(x))              scalar second price, W = argmax avg, tau = 2nd avg (MESP/Cao exploit asymptote)
  winM  = E_x M_W(x)                        scalar winner delivering full capability (Cao blind-trust, generous)
  gain_infeas = E_x[(tau - M_W(x))^+]       what the scalar price loses where it exceeds the winner's capability
  plmesp_pred(n) = exact elicitation accounting at global-horizon L_n, s_n
"""
import itertools, sys, numpy as np, pandas as pd
D = sys.argv[1]; OUT = sys.argv[2]
cap = pd.read_csv(f"{D}/capabilities_finite_5shot.csv")
mass = pd.read_csv(f"{D}/context_masses_5shot.csv").set_index("context")
SETS = {"Q3": ["MMLU", "HellaSwag", "GSM8K"],
        "Q7": ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]}
def consts(n, K):
    L = max(1, int(min(n // (2 * K), np.ceil(n ** (2/3) * np.log(np.e * n) ** (1/3)))))
    s = np.sqrt((np.log(2.0 * K) + 4.0 * np.log(float(n))) / (2 * L))
    return L, s
def plmesp_pred(M, w, n):  # M: Q x K, w: masses
    Q, K = M.shape; L, s = consts(n, K); tot = 0.0
    for z in range(Q):
        V = w[z] * n; e = min(V, K * L); srt = np.sort(M[z])
        tau = max(0.0, srt[-2] - s)
        tot += e * M[z].mean() + (V - e) * min(tau, srt[-1])
    return tot / n
rows = []
models = sorted(cap.model.unique())
for cs, fams in SETS.items():
    tab = cap[cap.context.isin(fams)].pivot(index="model", columns="context", values="M")[fams]
    w = mass.loc[fams, "n_queries"].values.astype(float); w /= w.sum()
    for k in range(2, len(models) + 1):
        for S in itertools.combinations(models, k):
            M = tab.loc[list(S)].values.T              # Q x K
            avg = w @ M; order = np.argsort(-avg); W = order[0]; tau = avg[order[1]]
            srt = np.sort(M, axis=1)
            ctx = w @ srt[:, -2]; top = w @ srt[:, -1]
            scl = w @ np.minimum(tau, M[:, W]); winM = avg[W]
            best = M.argmax(axis=1)
            # pairwise flip rate: fraction of (pair, context-pair) comparisons whose order reverses
            fl = []; 
            for a, b in itertools.combinations(range(k), 2):
                d = np.sign(M[:, a] - M[:, b])
                for x, y in itertools.combinations(range(len(fams)), 2):
                    fl.append(d[x] * d[y] < 0)
            r = dict(context_set=cs, K=k, models="|".join(S), has_gpt4="GPT-4" in S,
                     oracle=top, ctx=ctx, scl=scl, winM=winM,
                     gap_price=ctx - scl, gap_win=ctx - winM,
                     infeas_loss=w @ np.maximum(tau - M[:, W], 0),
                     infeas_mass=w @ (tau > M[:, W]),
                     switch_value=top - winM,              # value of picking the best model per context
                     n_distinct_best=len(set(best)), flip_rate=np.mean(fl))
            for n in (3*10**5, 3*10**6, 3*10**7, 3*10**8):
                r[f"pl_{n:.0e}"] = plmesp_pred(M, w, n)
            rows.append(r)
df = pd.DataFrame(rows); df.to_csv(f"{OUT}/ctx_benefit_subsets.csv", index=False)
print(len(df), "rows")
