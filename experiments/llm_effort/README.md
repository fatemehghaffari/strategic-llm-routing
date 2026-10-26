# Private, per-request inference effort in LLM serving

A reproducible demonstration that an inference provider can vary the reasoning computation spent on
individual requests while the customer-visible model identifier and request configuration stay fixed.
It accompanies the paper *Routing among Strategic LLM Providers: A Contextual Mechanism without
Monetary Transfers* and answers one reviewer question: once the customer has fixed the model and the
service tier, what quality-affecting decisions are left to the provider?

What it shows: the same checkpoint, tokenizer, prompt, sampling parameters and hardware serve the same
questions at three backend reasoning budgets, and accuracy and generated tokens move with the budget.
What it does not show: that any commercial provider does this in production. The gateway below is a
research abstraction of provider-side discretion, and a provider that contractually guarantees an exact
reasoning-token limit would not have this discretion.

## Setup

Model: `Qwen/Qwen3-4B`, revision `1cfa9a7208912126459214e8b04321603b3df60c` (thinking mode on).
Serving: vLLM 0.32.0, torch 2.13.0+cu130, Python 3.12.3, one NVIDIA L40S or A100 per job (the GPU of
every run is in `COMPUTE_LOG.md`). The backend control is vLLM's per-request
`SamplingParams(thinking_token_budget=...)`, which forces the `</think>` token once the reasoning
segment reaches the budget; Stage 2 verified on an A100 that it does so for this checkpoint.

```bash
python -m venv $W/venv && source $W/venv/bin/activate
pip install -r requirements.txt            # requirements-full.txt pins the entire environment
# model weights (8 GB), once, on a node with network access:
HF_HOME=$W/hf python -c "from huggingface_hub import snapshot_download as s; s('Qwen/Qwen3-4B', revision='1cfa9a7208912126459214e8b04321603b3df60c')"
```

`$W` is the scratch workspace that holds the environment, the weights, the raw outputs and the logs
(`<workspace>/llm_effort` here). Jobs run under Slurm on
the `gpu-preempt` partition; the scripts in `slurm/` set every path and environment variable.

## Data

`src/prepare_data.py` draws a seeded (20261021), disjoint calibration set (50 questions per benchmark)
and evaluation set (150 per benchmark) from the GSM8K test split and MATH-500. Subgroups are fixed
before any generation: GSM8K by the reference solution's length (median split), MATH-500 by its own
difficulty level (1-2, 3, 4-5). The resulting `configs/tasks.csv` is committed.

## Design

Customer-visible and held fixed for every request (`configs/model.json`, `customer_visible`): the
model id, `service_tier = standard`, the system prompt that asks for `Final answer: <answer>`,
temperature 0.6, top-p 0.95, top-k 20, and a 7,936-token output cap. Backend-controlled
(`backend_budgets`): the reasoning-token budget, low 128, medium 512, high 2,048.

`src/gateway.py` is the provider's gateway: it maps request metadata available before generation
(benchmark label, prompt) to a budget under one of five policies, fixed low / medium / high,
task-adaptive (competition mathematics gets the high budget, arithmetic the low one), and random
allocation with the adaptive policy's budget proportions. It never sees labels or outcomes.

`src/run_experiment.py` serves the requests through one vLLM engine and records, per request: ids,
benchmark, subgroup, split, assigned level and budget, seed, reasoning tokens and answer tokens (counted
from the token ids around the think tokens, `src/tokens.py`), total output tokens, the batch wall time
and its share attributed to the request, finish reason, budget-exhausted, truncation and malformed
flags, the extracted answer and its correctness. Every raw completion is saved to `raw_outputs.jsonl`,
so `src/regrade.py` can re-grade a results directory offline. `src/grade.py` reads only the answer
segment, prefers a boxed answer, accepts multi-line and tagged final answers, and reduces numeric golds
to the first number; it has a self-test (`python src/grade.py`).

## Commands

```bash
python src/prepare_data.py --data $W/data --out configs            # done; tasks.csv is committed
sbatch slurm/verify_preempt.sbatch                                   # Stage 2: does the budget bind?
sbatch slurm/pilot.sbatch                                            # Stage 3: 10 questions per benchmark, 3 budgets
sbatch slurm/main_fixed.sbatch                                       # Stage 4: 150 + 150 questions x 3 budgets x seeds 0-2
sbatch slurm/main_policies.sbatch                                    # Stage 5: 5 policies on the same request stream, seeds 0-2
python src/analyze.py --fixed $W/results/main_fixed --policies $W/results/main_policies --out results/aggregate --figs figures
sbatch slurm/audit.sbatch                                            # Stage 7: rerun 25 + 25 questions from the saved configs
python src/compare_audit.py --main $W/results/main_fixed --audit $W/results/audit --out results/aggregate/audit.json
```

Conditions are counterbalanced: in the fixed-budget run every question appears once per budget per
seed and the (question, budget) pairs are shuffled per seed; the policy run replays one shuffled
request stream per seed through every policy.

## Analysis

`src/analyze.py` writes `results/aggregate/table_A_levels.csv` (accuracy, tokens, latency, energy,
truncation and malformed rates per benchmark, subgroup and budget), `table_B_contrasts.csv` (paired
differences between budgets with 95% bootstrap intervals), `table_C_policies.csv`,
`table_D_policy_contrasts.csv`, `table_E_examples.csv`, and `figures/fig1..fig4` (PDF and PNG).
Intervals are question-level bootstrap percentiles with 2,000 resamples; a question's generations
across seeds stay together in a resample, and differences are paired within questions. Latency is the
batch wall time attributed by output-token share and is a relative computation proxy, not a price.
Energy is GPU power sampled at 1 Hz, integrated over each batch above the idle power measured before
the model loaded, and attributed by output-token share.

## Layout

```
configs/   model.json (checkpoint, serving, customer-visible settings, budgets), tasks.csv, split_meta.json
src/       prepare_data.py, gateway.py, run_experiment.py, tokens.py, grade.py, regrade.py, analyze.py, compare_audit.py, verify_budget.py
slurm/     verify*.sbatch, pilot.sbatch, main_fixed.sbatch, main_policies.sbatch, audit.sbatch
results/   request-level records (requests.csv per seed) and results/aggregate tables
figures/   fig1 accuracy vs computation, fig2 marginal value, fig3 adaptive sequence, fig4 policies
report.md  the experimental report;  COMPUTE_LOG.md  every job, its hardware and what it produced
```
