"""Coarse capabilities from open-llm-leaderboard/contents (ungated) for the pre-registered 20 models.
M = the benchmark's raw score column (fraction correct, in [0,1]). The per-question details are gated, so
n is the benchmark's item count as documented by the leaderboard (approximate, flagged) and se is the
binomial approximation sqrt(M(1-M)/n); both are marked approximate in the CSV."""
import glob, os, sys
import numpy as np, pandas as pd
W, OUT = sys.argv[1], sys.argv[2]
d = pd.read_parquet(glob.glob(os.path.join(W, "raw_data/openllm/contents/**/*.parquet"), recursive=True)[0])
FAM = {
    "qwen2.5-instruct": ["Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct",
                         "Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-14B-Instruct", "Qwen/Qwen2.5-32B-Instruct",
                         "Qwen/Qwen2.5-72B-Instruct"],
    "llama-3.x-instruct": ["meta-llama/Llama-3.2-1B-Instruct", "meta-llama/Llama-3.2-3B-Instruct",
                           "meta-llama/Llama-3.1-8B-Instruct", "meta-llama/Llama-3.1-70B-Instruct",
                           "meta-llama/Llama-3.3-70B-Instruct"],
    "gemma-2-it": ["google/gemma-2-2b-it", "google/gemma-2-9b-it", "google/gemma-2-27b-it"],
    "mistral-instruct": ["mistralai/Mistral-7B-Instruct-v0.3", "mistralai/Ministral-8B-Instruct-2410",
                         "mistralai/Mistral-Nemo-Instruct-2407", "mistralai/Mistral-Small-Instruct-2409",
                         "mistralai/Mistral-Large-Instruct-2411"],
}
BENCH = {"IFEval": ("IFEval Raw", 541), "BBH": ("BBH Raw", 5761), "MATH_Lvl5": ("MATH Lvl 5 Raw", 1324),
         "GPQA": ("GPQA Raw", 1192), "MuSR": ("MUSR Raw", 756), "MMLU_Pro": ("MMLU-PRO Raw", 12032)}
rows, fams = [], []
for fam, ms in FAM.items():
    sub = []
    for m in ms:
        g = d[(d.fullname == m) & (d["Official Providers"] == True)]
        assert len(g), m
        g = g[g.Precision == "bfloat16"] if (g.Precision == "bfloat16").any() else g[g.Precision == "float16"]
        r = g.iloc[0]
        sub.append((float(r["#Params (B)"]), m, r))
    sub.sort()
    for rank, (params, m, r) in enumerate(sub):
        fams.append(dict(family=fam, rank_by_size=rank, model=m, params_b=params, precision=r.Precision,
                         model_sha=r["Model sha"], hub_license=r["Hub License"], is_cheapest=(rank == 0)))
        for b, (col, n) in BENCH.items():
            M = float(r[col])
            rows.append(dict(model=m, family=fam, type=b, M=M, n_items_approx=n,
                             se_binomial_approx=np.sqrt(M * (1 - M) / n)))
c = pd.DataFrame(rows)
assert c.M.between(0, 1).all(), c[~c.M.between(0, 1)]
c.to_csv(os.path.join(OUT, "leaderboard_capabilities_coarse.csv"), index=False)
pd.DataFrame(fams).to_csv(os.path.join(OUT, "leaderboard_families.csv"), index=False)
print(c.pivot(index="model", columns="type", values="M").round(3).to_string())
