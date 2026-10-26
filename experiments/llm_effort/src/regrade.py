"""Re-grade a results directory offline from its raw_outputs.jsonl with the current grade.py.

    python regrade.py <results dir>

Rewrites correct / pred / extraction / malformed in requests.csv and requests.parquet (a copy of the
previous files is kept as *.pregrade.*) and prints the accuracy table.
"""
import json, os, sys, shutil
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade import correct  # noqa: E402

def main(d):
    raw = {(x["policy"], x["task_id"], x["level"], x["seed"]): x["text"] for x in map(json.loads, open(os.path.join(d, "raw_outputs.jsonl")))}
    req = pd.read_csv(os.path.join(d, "requests.csv"))
    for ext in ("csv", "parquet"):
        f = os.path.join(d, f"requests.{ext}")
        if os.path.exists(f) and not os.path.exists(os.path.join(d, f"requests.pregrade.{ext}")): shutil.copy(f, os.path.join(d, f"requests.pregrade.{ext}"))
    oks, hows, preds = [], [], []
    for _, r in req.iterrows():
        ok, how, pred = correct(raw[(r.policy, r.task_id, r.level, int(r.seed))], r.gold)
        oks.append(bool(ok)); hows.append(how); preds.append(pred)
    req["correct"], req["extraction"], req["pred"] = oks, hows, preds; req["malformed"] = req.pred.isna()
    req.to_csv(os.path.join(d, "requests.csv"), index=False); req.to_parquet(os.path.join(d, "requests.parquet"))
    print(req.groupby(["policy", "benchmark", "level"])[["correct", "reasoning_tokens", "answer_tokens", "budget_exhausted", "truncated", "malformed"]].mean().round(3).to_string())
    print(req.extraction.value_counts().to_string())

if __name__ == "__main__": main(sys.argv[1])
