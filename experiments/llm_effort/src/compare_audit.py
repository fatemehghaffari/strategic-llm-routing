"""Stage 7: compare an audit rerun with the main run on the same requests.

    python compare_audit.py --main <main_fixed dir> --audit <audit dir> --out results/aggregate/audit.json

Matches on (task_id, level, seed). Reports agreement of correctness, the share of byte-identical
completions, and the aggregate accuracy and reasoning-token means of both runs. Sampling is seeded, but
a vLLM batch is served as one unit, so a different batch composition can change bf16 numerics and hence
individual samples; aggregate agreement is the reproducibility claim, token-exact agreement is reported
as what it is.
"""
import argparse, glob, json, os
import pandas as pd

def load(d):
    r = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(d, "seed*", "requests.csv")))], ignore_index=True)
    raws = {}
    for f in sorted(glob.glob(os.path.join(d, "seed*", "raw_outputs.jsonl"))):
        for x in map(json.loads, open(f)): raws[(x["policy"], x["task_id"], x["level"], x["seed"])] = x["text"]
    r["text"] = [raws.get((p, t, l, s)) for p, t, l, s in zip(r.policy, r.task_id, r.level, r.seed)]
    return r

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--main", required=True); ap.add_argument("--audit", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); M, A = load(a.main), load(a.audit)
    k = ["task_id", "level", "seed"]; j = A.merge(M, on=k, suffixes=("_audit", "_main"))
    res = dict(n_audit_requests=int(len(A)), n_matched=int(len(j)),
               correctness_agreement=float((j.correct_audit == j.correct_main).mean()),
               identical_text=float((j.text_audit == j.text_main).mean()),
               identical_reasoning_tokens=float((j.reasoning_tokens_audit == j.reasoning_tokens_main).mean()),
               accuracy_audit=float(j.correct_audit.mean()), accuracy_main_same_requests=float(j.correct_main.mean()),
               reasoning_tokens_audit=float(j.reasoning_tokens_audit.mean()), reasoning_tokens_main_same_requests=float(j.reasoning_tokens_main.mean()),
               by_level={lvl: dict(acc_audit=float(g.correct_audit.mean()), acc_main=float(g.correct_main.mean()), rt_audit=float(g.reasoning_tokens_audit.mean()), rt_main=float(g.reasoning_tokens_main.mean()),
                                   identical_text=float((g.text_audit == g.text_main).mean())) for lvl, g in j.groupby("level")})
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True); json.dump(res, open(a.out, "w"), indent=1); print(json.dumps(res, indent=1))

if __name__ == "__main__": main()
