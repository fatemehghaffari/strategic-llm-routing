"""RouterBench capabilities on the five merged task types (fixed by the plan, 28 Sep 2026):
knowledge_qa = MMLU+ARC, math = GSM8K, code = MBPP, commonsense = HellaSwag+Winogrande, open_chat = MT-Bench.
M = mean published score over the pooled queries of the type (identical to the query-count weighted
average of the family means); se = pooled sd / sqrt(n). Uses A4's loaders and cleaning unchanged."""
import os, sys
import numpy as np, pandas as pd
A4 = "<scratch>/llm"
sys.path.insert(0, A4)
from rb_common import MODELS, SHORT, load_shot  # noqa: E402
from build_capabilities import clean  # noqa: E402
TYPES = ["knowledge_qa", "math", "code", "commonsense", "open_chat"]
MERGE = {"MMLU": "knowledge_qa", "ARC": "knowledge_qa", "GSM8K": "math", "MBPP": "code",
         "HellaSwag": "commonsense", "Winogrande": "commonsense", "MT-Bench": "open_chat"}
OUT = sys.argv[1]
for shot in ("5shot", "0shot"):
    df, rep = clean(load_shot(shot), shot)
    df["type"] = df["family"].map(MERGE)
    assert df["type"].notna().all(), df.loc[df["type"].isna(), "family"].unique()
    rows = []
    for t in TYPES:
        g = df[df.type == t]
        for m in MODELS:
            v = g[m].values
            rows.append(dict(model=SHORT[m], type=t, M=v.mean(), n_queries=len(v), se=v.std(ddof=1) / np.sqrt(len(v))))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, f"capabilities_merged5_{shot}.csv"), index=False)
    ms = df.groupby("type").size().reindex(TYPES)
    pd.DataFrame({"type": TYPES, "n_queries": ms.values, "mass": (ms / ms.sum()).values}).to_csv(
        os.path.join(OUT, f"type_masses_merged5_{shot}.csv"), index=False)
    print(shot, rep, ms.to_dict())
