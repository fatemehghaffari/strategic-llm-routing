"""Experiment A/B (fixed budgets) and C (gateway policies) on one vLLM engine.

    python run_experiment.py --config configs/model.json --tasks configs/tasks.csv --split evaluation \
        --mode fixed --seeds 0,1,2 --out <dir>            # every question under every budget
    python run_experiment.py ... --mode policies --policies fixed_low,fixed_high,task_adaptive,random_matched

Every request is recorded with: ids, benchmark, category, subgroup, split, checkpoint/serving config,
assigned level and budget, reasoning tokens, answer tokens, total output tokens, generation wall time
(per batch, attributed per request by its token share), correctness, extraction method, budget-exhausted
flag, finish reason, truncation/malformed flags. Condition order is randomised per seed.
"""
import argparse, json, os, sys, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade import correct  # noqa: E402
from gateway import Gateway         # noqa: E402
from tokens import split_reasoning, think_ids  # noqa: E402

def build_engine(cfg):
    os.environ["HF_HOME"] = cfg["hf_home"]; os.environ["HF_HUB_OFFLINE"] = "1"
    from vllm import LLM
    s = cfg["serving"]
    return LLM(model=cfg["model_id"], revision=cfg["revision"], dtype=s["dtype"], max_model_len=s["max_model_len"],
               gpu_memory_utilization=s["gpu_memory_utilization"], reasoning_parser=s["reasoning_parser"],
               enforce_eager=s.get("enforce_eager", False), seed=0)

def generate(llm, cfg, rows, budgets, seed, raw, policy):
    """rows: list of dict(task_id, prompt, level). Returns per-request records; appends raw texts to `raw`."""
    from vllm import SamplingParams
    cv = cfg["customer_visible"]; tok = llm.get_tokenizer(); think = think_ids(tok); out = []
    for lvl in sorted(set(r["level"] for r in rows)):
        sub = [r for r in rows if r["level"] == lvl]
        msgs = [[{"role": "system", "content": cv["system_prompt"]}, {"role": "user", "content": r["prompt"]}] for r in sub]
        sp = SamplingParams(temperature=cv["temperature"], top_p=cv["top_p"], top_k=cv["top_k"], max_tokens=cv["max_tokens_total"],
                            thinking_token_budget=budgets[lvl], seed=seed)
        t0 = time.time(); res = llm.chat(msgs, sp, chat_template_kwargs={"enable_thinking": True}, use_tqdm=False); t1 = time.time(); dt = t1 - t0
        tot = sum(len(o.outputs[0].token_ids) for o in res) or 1
        for r, o in zip(sub, res):
            c = o.outputs[0]; sp_ = split_reasoning(c.token_ids, tok, think)
            rt = sp_["reasoning_tokens"]; n_out = len(c.token_ids)
            ok, how, pred = correct(c.text, r["gold"])
            raw.append(dict(policy=policy, task_id=r["task_id"], level=lvl, seed=seed, text=c.text, token_ids_len=n_out))
            out.append(dict(**{k: r[k] for k in ("task_id", "benchmark", "category", "subgroup", "split", "gold")}, arrival=r.get("arrival", -1), level=lvl, budget=budgets[lvl],
                            seed=seed, reasoning_tokens=rt, answer_tokens=sp_["answer_tokens"], total_output_tokens=n_out,
                            batch_wall_s=round(dt, 2), est_wall_s=round(dt * n_out / tot, 3), batch_t0=round(t0, 3), batch_t1=round(t1, 3), batch_size=len(sub), finish_reason=c.finish_reason,
                            budget_exhausted=bool(rt >= budgets[lvl]), truncated=c.finish_reason == "length",
                            malformed=pred is None, correct=bool(ok), extraction=how, pred=pred,
                            think_opened=sp_["think_opened"], think_closed=sp_["think_closed"]))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); ap.add_argument("--tasks", required=True)
    ap.add_argument("--split", default="evaluation"); ap.add_argument("--mode", choices=["fixed", "policies"], default="fixed")
    ap.add_argument("--seeds", default="0,1,2"); ap.add_argument("--policies", default="fixed_low,fixed_high,task_adaptive,random_matched")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--out", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    cfg = json.load(open(a.config)); budgets = cfg["backend_budgets"]
    tasks = pd.read_csv(a.tasks); tasks = tasks[tasks.split == a.split]
    tasks = tasks.rename(columns={"level": "difficulty"})   # MATH's own difficulty level; `level` is the effort level below
    if a.limit: tasks = tasks.groupby("benchmark", group_keys=False).head(a.limit)
    llm = build_engine(cfg); recs = []; raw = []
    for seed in [int(s) for s in a.seeds.split(",")]:
        rng = np.random.default_rng(1000 + seed)
        if a.mode == "fixed":
            rows = [dict(**t, level=lvl) for t in tasks.to_dict("records") for lvl in budgets]
            rng.shuffle(rows)                                     # counterbalanced condition order
            recs += [dict(policy="fixed_all", **r) for r in generate(llm, cfg, rows, budgets, seed, raw, "fixed_all")]
        else:
            stream = tasks.sample(frac=1.0, random_state=seed).to_dict("records")   # one fixed request stream per seed
            for pol in a.policies.split(","):
                props = None
                if pol == "random_matched":
                    g = Gateway(budgets, "task_adaptive", seed); lv = [g.choose(t["task_id"], t["category"], t["prompt"])[0] for t in stream]
                    props = {l: lv.count(l) for l in budgets}
                gw = Gateway(budgets, pol, seed, match_proportions=props)
                rows = [dict(**t, level=gw.choose(t["task_id"], t["category"], t["prompt"])[0], arrival=i) for i, t in enumerate(stream)]
                recs += [dict(policy=pol, **r) for r in generate(llm, cfg, rows, budgets, seed, raw, pol)]
                pd.DataFrame(gw.log).assign(policy=pol, seed=seed).to_csv(os.path.join(a.out, f"gateway_log_{pol}_seed{seed}.csv"), index=False)
        pd.DataFrame(recs).to_parquet(os.path.join(a.out, "requests.parquet")); pd.DataFrame(recs).to_csv(os.path.join(a.out, "requests.csv"), index=False)
        with open(os.path.join(a.out, "raw_outputs.jsonl"), "w") as fh:                 # every raw completion, so grading is re-runnable offline
            for x in raw: fh.write(json.dumps(x) + "\n")
        print(f"seed {seed} done; {len(recs)} records", flush=True)
    d = pd.DataFrame(recs); print(d.groupby(["policy", "benchmark", "level"])[["correct", "reasoning_tokens", "budget_exhausted", "truncated", "malformed"]].mean().round(3).to_string())

if __name__ == "__main__": main()
