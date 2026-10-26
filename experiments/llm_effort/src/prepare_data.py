"""Build the calibration and held-out evaluation sets (seeded, disjoint), one row per question.

    python prepare_data.py --data <dir with gsm8k_test.parquet, math500_test.parquet> --out <dir>

GSM8K answer: the integer after '####'. MATH-500: the dataset's own `answer` field (boxed answer
already extracted by its authors). Difficulty subgroups: GSM8K by solution length (short/long, median
split); MATH-500 by its `level` field (1-2 easy, 3 medium, 4-5 hard) and `subject`.
"""
import argparse, os, re, json
import numpy as np, pandas as pd

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--n_eval", type=int, default=150); ap.add_argument("--n_calib", type=int, default=50); ap.add_argument("--seed", type=int, default=20261021)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); rng = np.random.default_rng(a.seed)
    g = pd.read_parquet(os.path.join(a.data, "gsm8k_test.parquet"))
    g["gold"] = g.answer.str.extract(r"####\s*(.+)$", flags=re.M)[0].str.replace(",", "").str.strip()
    g["steps"] = g.answer.str.count("\n") + 1
    g["subgroup"] = np.where(g.steps <= g.steps.median(), "gsm8k_short", "gsm8k_long")
    g = g.rename(columns={"question": "prompt"})[["prompt", "gold", "subgroup"]]; g["benchmark"] = "gsm8k"; g["category"] = "arithmetic"
    m = pd.read_parquet(os.path.join(a.data, "math500_test.parquet"))
    m["subgroup"] = pd.cut(m.level, [0, 2, 3, 5], labels=["math_easy", "math_medium", "math_hard"]).astype(str)
    m = m.rename(columns={"problem": "prompt", "answer": "gold"})[["prompt", "gold", "subgroup", "subject", "level", "unique_id"]]; m["benchmark"] = "math500"; m["category"] = "competition_math"
    out = []
    for name, df in (("gsm8k", g), ("math500", m)):
        idx = rng.permutation(len(df)); calib = df.iloc[idx[:a.n_calib]].copy(); ev = df.iloc[idx[a.n_calib:a.n_calib + a.n_eval]].copy()
        calib["split"] = "calibration"; ev["split"] = "evaluation"; out += [calib, ev]
    d = pd.concat(out, ignore_index=True); d.insert(0, "task_id", [f"{b}-{i:04d}" for i, b in enumerate(d.benchmark)])
    d.to_parquet(os.path.join(a.out, "tasks.parquet")); d.to_csv(os.path.join(a.out, "tasks.csv"), index=False)
    print(d.groupby(["benchmark", "split"]).size().to_string()); print(d.groupby("subgroup").size().to_string())
    json.dump(dict(seed=a.seed, n_eval=a.n_eval, n_calib=a.n_calib), open(os.path.join(a.out, "split_meta.json"), "w"))

if __name__ == "__main__": main()
