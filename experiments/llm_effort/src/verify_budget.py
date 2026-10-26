"""Stage 2: does thinking_token_budget actually bound the reasoning segment for this checkpoint?

Offline vLLM engine, fixed customer-visible configuration, two prompts x three budgets. Prints the
reasoning-token count, the answer-token count, the finish reason, and whether the budget was hit.
"""
import json, os, sys, time
cfg = json.load(open(sys.argv[1]))
os.environ["HF_HOME"] = cfg["hf_home"]; os.environ["HF_HUB_OFFLINE"] = "1"
from vllm import LLM, SamplingParams
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from tokens import split_reasoning, think_ids
llm = LLM(model=cfg["model_id"], revision=cfg["revision"], dtype=cfg["serving"]["dtype"],
          max_model_len=cfg["serving"]["max_model_len"], gpu_memory_utilization=cfg["serving"]["gpu_memory_utilization"],
          reasoning_parser=cfg["serving"]["reasoning_parser"], seed=0, enforce_eager=cfg["serving"].get("enforce_eager", True))
tok = llm.get_tokenizer()
cv = cfg["customer_visible"]
prompts = ["Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
           "Let $f(x)=3x^4-7x^3+2x^2-bx+1$. For what value of $b$ is $f(1)=1$?"]
msgs = [[{"role": "system", "content": cv["system_prompt"]}, {"role": "user", "content": p}] for p in prompts]
print("checkpoint:", cfg["model_id"], cfg["revision"]); print("torch/cuda ok; running", flush=True)
for budget in cfg["backend_budgets"].values():
    sp = SamplingParams(temperature=cv["temperature"], top_p=cv["top_p"], top_k=cv["top_k"], max_tokens=cv["max_tokens_total"],
                        thinking_token_budget=budget, seed=0)
    t0 = time.time(); outs = llm.chat(msgs, sp, chat_template_kwargs={"enable_thinking": True}, use_tqdm=False); dt = time.time() - t0
    for i, o in enumerate(outs):
        c = o.outputs[0]; text = c.text; sp_ = split_reasoning(c.token_ids, tok, think_ids(tok))
        print(json.dumps(dict(budget=budget, prompt=i, finish=c.finish_reason, total_out_tokens=len(c.token_ids), **sp_,
                              budget_hit=sp_["reasoning_tokens"] >= budget,
                              answer_tail=text.strip()[-80:].replace("\n", " "), wall_s=round(dt, 1))))
    sys.stdout.flush()
