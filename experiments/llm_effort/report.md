# Private, per-request inference effort in LLM serving

All seven stages of the assignment were executed on 21 October 2026. Every number below is computed by `src/analyze.py` from the request-level records in `results/requests/`; the raw completions are in `results/raw_outputs/`; every job, its node and its outcome is in `COMPUTE_LOG.md`.

## 1. Experimental setup

**Model and serving.** Qwen/Qwen3-4B, Hugging Face revision `1cfa9a7208912126459214e8b04321603b3df60c`, bf16, thinking mode enabled through the chat template. Served offline by vLLM 0.32.0 (torch 2.13.0+cu130, Python 3.12.3, eager mode, one engine per job, `max_model_len` 12,288). One GPU per job on the the university cluster, Slurm partition `gpu-preempt`: fixed-budget seeds 0 and 1 and the pilot on an NVIDIA L40S (46 GB, driver 580.178), fixed-budget seed 2, the three policy seeds and the audit on A100-SXM4-80GB nodes (drivers 580.178 and 595.91). The environment is pinned in `requirements.txt` and `requirements-full.txt`.

**Backend control.** vLLM's per-request `thinking_token_budget`. It counts the tokens generated after the `<think>` token and forces `</think>` once the next token would exceed the budget; the model then writes the visible answer. Stage 2 (job 65930037, A100) and the pilot (job 65935075, L40S) verified that this bounds the reasoning segment for this checkpoint. In the main run every one of the 2,700 completions opened and closed a reasoning segment; at the low budget every completion generated exactly 128 reasoning tokens; at the medium budget 494 on average (the segment ended naturally below 512 on 29% of GSM8K requests and 1% of MATH-500 requests); at the high budget 1,284 on average (the cap of 2,048 was reached on 11% of GSM8K and 51% of MATH-500 requests). The offline engine exposes no parsed reasoning field, so reasoning and answer tokens are counted from the token ids around the think tokens (`src/tokens.py`).

**Customer-visible configuration, held fixed for every request.** Model id `Qwen3-4B`, `service_tier = standard`, the same system prompt (`Solve the problem. End with the final answer in the form: Final answer: <answer>.`), temperature 0.6, top-p 0.95, top-k 20, output cap 7,936 tokens, the same weights. Nothing in a request names a reasoning budget.

**Effort levels.** Low 128, medium 512, high 2,048 reasoning tokens. The pilot (Stage 3, 10 questions per benchmark) kept these values: realized reasoning computation differs by a factor of about four between neighbouring levels and no final answer was made impossible. One adjustment followed the pilot: the customer-visible output cap was raised from 4,096 to 7,936 tokens, because the only wrong pilot answers were cap truncations, and a response cut off by the total-output limit is not evidence about reasoning effort. Truncation is still recorded and reported.

**Benchmarks and split.** GSM8K test split and MATH-500. A seeded permutation (seed 20261021) draws, per benchmark, 50 calibration questions (used for the verification run and the pilot) and 150 disjoint evaluation questions (used for every number below). Subgroups were fixed before generation: GSM8K by the length of the reference solution (median split; 82 short and 68 long evaluation questions), MATH-500 by its own difficulty level (level 1-2: 40, level 3: 37, level 4-5: 73).

**Design.** Experiments A and B: every evaluation question under every budget, seeds 0, 1, 2 (2,700 generations), with the (question, budget) pairs shuffled per seed so that budgets are counterbalanced over the run. Experiment C: one shuffled request stream per seed, replayed through five gateway policies (fixed low, fixed medium, fixed high, task-adaptive, random with the adaptive policy's budget proportions; 4,500 generations). The task-adaptive rule is prespecified and uses only the benchmark label available before generation: competition mathematics gets the high budget, arithmetic the low one. No policy sees labels, answers or outcomes. The gateway logs the chronological sequence of its budget decisions (`results/requests/*gateway_log*`).

**Measurements.** Per request: ids, benchmark, subgroup, split, assigned level and budget, seed, reasoning tokens, answer tokens, total output tokens, the batch's wall time and the request's share of it by output tokens, finish reason, budget-exhausted, truncated and malformed flags, the extracted answer and its correctness; the raw completion is saved. GPU power was sampled at 1 Hz for the whole job, with 20 s of idle before the model loaded (34 to 36 W on the L40S, 66 W on the A100); energy per batch is the integral of power above idle, attributed to requests by output-token share.

**Grading.** Only the text after `</think>` is graded. The answer is the content of a `\boxed{}` after the last `Final answer` marker if present, else the paragraph after the marker with tags and math delimiters stripped, else the last boxed expression, else the last number. GSM8K golds are integers and are compared numerically after units and punctuation are dropped. MATH-500 answers are compared after a conservative LaTeX normalisation (`\dfrac` to `\frac`, `\left`/`\right`, `\text{}`, spaces, degrees, percent, fractions to one spelling); no symbolic equivalence is attempted, so an algebraically equal but differently written answer is graded wrong, equally at every budget. Malformed, missing and truncated answers count as wrong and their rates are reported. The grader has a 26-case self-test built from the pilot's failure patterns, and `src/regrade.py` re-grades any results directory from the saved completions.

**Statistics.** Accuracy intervals are question-level bootstrap percentile intervals (2,000 resamples of questions with replacement; a question's three generations stay together). Differences between budgets or policies are paired within questions. Latency is the batch wall time attributed by output-token share: a relative computation proxy on one engine, not a price, and not comparable across batch sizes (see Section 3). Token counts are not FLOPs.

## 2. Results: accuracy against computation (Experiments A and B)

**Per benchmark and budget** (150 questions each, 3 seeds, `table_A_levels.csv`):

| benchmark | budget | accuracy (95% CI) | reasoning tokens | answer tokens | total tokens | latency s | energy J | at cap | truncated | malformed |
|---|---|---|---|---|---|---|---|---|---|---|
| GSM8K | low 128 | 93.3% (89.8, 96.4) | 128 | 448 | 578 | 0.36 | 96 | 100% | 0.2% | 0 |
| GSM8K | medium 512 | 94.9% (91.6, 97.8) | 476 | 253 | 731 | 0.41 | 104 | 71% | 0 | 0 |
| GSM8K | high 2048 | 95.6% (92.2, 98.4) | 922 | 213 | 1,137 | 0.56 | 147 | 11% | 0 | 0 |
| MATH-500 | low 128 | 81.3% (75.6, 86.4) | 128 | 2,172 | 2,302 | 1.44 | 382 | 100% | 9.6% | 0.4% |
| MATH-500 | medium 512 | 86.4% (81.6, 91.1) | 512 | 1,434 | 1,948 | 1.07 | 274 | 99% | 4.7% | 0 |
| MATH-500 | high 2048 | 86.4% (81.3, 91.1) | 1,647 | 1,019 | 2,668 | 1.31 | 345 | 51% | 5.1% | 0.2% |

Accuracy across seeds varies by 0.4 to 3.4 points (standard deviation of the per-seed accuracy), which is the sampling noise of 150 questions at temperature 0.6.

**Paired differences between budgets** (`table_B_contrasts.csv`):

| scope | contrast | accuracy difference (95% CI) | extra reasoning tokens | extra total tokens |
|---|---|---|---|---|
| GSM8K | medium vs low | +1.6 (−0.4, +3.8) | +348 | +153 |
| GSM8K | high vs medium | +0.7 (−0.9, +2.2) | +446 | +406 |
| GSM8K | high vs low | +2.2 (+0.4, +4.7) | +794 | +559 |
| MATH-500 | medium vs low | +5.1 (+1.8, +8.4) | +384 | −354 |
| MATH-500 | high vs medium | 0.0 (−2.7, +2.4) | +1,135 | +720 |
| MATH-500 | high vs low | +5.1 (+2.4, +8.2) | +1,519 | +366 |
| GSM8K short | high vs low | +2.0 (−0.4, +5.3) | +660 | +470 |
| GSM8K long | high vs low | +2.5 (−1.0, +6.4) | +955 | +666 |
| MATH level 1-2 | high vs low | +1.7 (0.0, +4.2) | +1,140 | +840 |
| MATH level 3 | high vs low | −2.7 (−7.2, 0.0) | +1,537 | +442 |
| MATH level 4-5 | medium vs low | +11.0 (+5.0, +16.9) | +384 | −687 |
| MATH level 4-5 | high vs medium | 0.0 (−4.6, +4.6) | +1,333 | +754 |
| MATH level 4-5 | high vs low | +11.0 (+5.9, +16.0) | +1,717 | +67 |

Three findings.

1. **The same checkpoint serves the same questions at distinct quality and computation points** (RQ1, RQ2). Between the low and high budgets, mean reasoning tokens rise by a factor of 7 on GSM8K and 13 on MATH-500, and accuracy rises by 2.2 points on GSM8K and 5.1 points on MATH-500, both with intervals excluding zero. Nothing visible to the client changed.

2. **The benefit is task dependent** (RQ3). On MATH-500 level 4-5 the medium budget adds 11.0 points over the low budget (interval 5.0 to 16.9) and the high budget adds nothing further; on MATH-500 level 1-2, level 3 and both GSM8K subgroups, the differences are within 3 points and their intervals include zero or touch it. The whole MATH-500 gain is carried by its hardest third. Figure 2 shows this; the pattern is the hypothesis of Experiment B, and it is confirmed for this model on these benchmarks, with the qualification that the medium budget already captures it.

3. **Cutting the reasoning budget does not cut the visible answer.** When the budget forces `</think>` early, the model continues to reason in the answer segment: at the low budget the answer segment averages 448 tokens on GSM8K and 2,172 on MATH-500, against 213 and 1,019 at the high budget. On GSM8K total output still falls with the budget (578, 731, 1,137 tokens). On MATH-500 it does not: the low budget produces more total tokens (2,302) than the medium budget (1,948) and nearly as many as the high budget (2,668), and 9.6% of its answers hit the 7,936-token cap. The backend control therefore moves computation between the hidden and the visible segment as well as changing its total; a provider that wants to save computation on hard questions gains little from the low budget, while the medium budget saves 27% of total tokens on MATH-500 at the same accuracy as the high budget. Latency and energy follow total tokens, not reasoning tokens, for the same reason (MATH-500: 1.44 s and 382 J at low, 1.07 s and 274 J at medium, 1.31 s and 345 J at high).

**Example tasks** (`table_E_examples.csv`, chosen by a rule, not by hand: the largest and the smallest change in per-question correctness between the low and high budgets). GSM8K-0108 is wrong at the low budget in all three seeds (answer 300, gold 200) and right in all three at medium and high. GSM8K-0190 is right in one seed at low and medium (answer 30 twice, 180 once) and in all three at high, where the reasoning segment ends naturally at 1,552 tokens. MATH500-0274 (level 4-5, gold 20000/π) is right in one seed at the low budget and in all three at medium and high. The reverse case exists: MATH500-0257 (gold `52_8`) is right in all seeds at low and medium and in one seed at high, where two completions drop the base subscript. These are illustrations beside the aggregate statistics, and the last one shows the grader's strictness as much as the model.

## 3. Results: adaptive serving (Experiment C)

Five policies on the same 300-question stream per seed, three seeds (`table_C_policies.csv`, `table_D_policy_contrasts.csv`):

| policy | accuracy (95% CI) | GSM8K | MATH-500 | reasoning tokens | total tokens | budget shares low / med / high |
|---|---|---|---|---|---|---|
| fixed low | 89.2% (86.0, 92.1) | 93.8% | 84.7% | 128 | 1,494 | 1 / 0 / 0 |
| fixed medium | 90.0% (86.7, 93.1) | 94.9% | 85.1% | 492 | 1,367 | 0 / 1 / 0 |
| fixed high | 91.7% (88.9, 94.3) | 96.0% | 87.3% | 1,277 | 1,941 | 0 / 0 / 1 |
| task-adaptive | 91.7% (88.7, 94.4) | 94.0% | 89.3% | 880 | 1,576 | 0.5 / 0 / 0.5 |
| random, matched | 90.1% (87.0, 93.0) | 95.6% | 84.7% | 711 | 1,665 | 0.5 / 0 / 0.5 |

| contrast | accuracy difference (95% CI) | reasoning tokens |
|---|---|---|
| task-adaptive vs random matched | +1.6 (−0.1, +3.2) | +169 |
| task-adaptive vs fixed low | +2.4 (+0.8, +4.3) | +752 |
| task-adaptive vs fixed high | 0.0 (−1.3, +1.3) | −397 |
| fixed high vs fixed low | +2.4 (+0.9, +4.1) | +1,149 |
| random matched vs fixed low | +0.9 (−0.9, +2.7) | +583 |

Findings (RQ4).

1. **A backend can choose a different budget for successive requests under one service configuration.** Figure 3 shows the gateway's decisions in arrival order for the task-adaptive policy: the assigned budget alternates between 128 and 2,048 from one request to the next with the benchmark label, and the lower panel shows the reasoning tokens actually generated following it. The sequence is in the gateway logs.

2. **Where computation is allocated matters, with a caveat on precision.** The task-adaptive policy matches the fixed-high policy's accuracy (91.7% in both; paired difference 0.0, interval −1.3 to +1.3) with 31% fewer reasoning tokens and 19% fewer total tokens per request. The random policy with the same budget proportions reaches 90.1%; the paired difference of 1.6 points in favour of the adaptive policy has an interval of −0.1 to +3.2, so it is not resolved at the 95% level with 300 questions, though its sign and size are what the fixed-budget results predict (the gain sits on MATH-500, 89.3% against 84.7%, where the adaptive policy spends the high budget). Figure 4 places the five policies on the accuracy-against-computation plane; the adaptive policy lies above the fixed-budget line, the random policy on it.

3. **The policy comparison must be read in token units, not latency.** The engine serves a policy's requests in one batch per budget level, so the fixed policies ran batches of 300 and the mixed policies batches of 150; per-request attributed latency and energy are therefore higher for the mixed policies (1.0 s against 0.6 s) for a reason that has nothing to do with reasoning. Token counts are unaffected by batching and are the computation measure for Experiment C.

## 4. Figures

- `figures/fig1_accuracy_vs_computation` (Figure 1): accuracy against mean reasoning tokens, one line per subgroup through the three budgets, with 95% intervals. Message: one model, several quality and computation points; the hard MATH-500 subgroup climbs, the rest are flat.
- `figures/fig2_marginal_value` (Figure 2): paired accuracy gains (medium vs low, high vs medium, high vs low) per subgroup with 95% intervals. Message: the benefit of extra reasoning computation is concentrated on MATH-500 level 4-5 and is captured by the medium budget.
- `figures/fig3_adaptive_sequence` (Figure 3): the gateway's budget for the first 120 requests of the task-adaptive stream (seed 0), coloured by benchmark, with the reasoning tokens generated below. Message: effort varies from one request to the next while the requested configuration is constant.
- `figures/fig4_policies` (Figure 4; `_total_output_tokens` and `_est_wall_s` variants): overall accuracy against mean computation per request for the five policies. Message: the allocation policy moves the achievable quality-cost point; the adaptive policy matches fixed-high accuracy at lower computation, and the random policy does not.
- Figure 5 is the example table above (`table_E_examples.csv`).

## 5. Reproducibility audit (Stage 7)

The first 25 evaluation questions per benchmark were rerun under every budget with seed 0 from the saved configurations (job 65937961, A100-SXM4-80GB; the matching main-run requests were served on an L40S). On the 150 matched requests: accuracy 93.3% in the rerun against 90.0% in the main run (a difference of 5 answers, inside the noise of 150 draws at temperature 0.6); mean reasoning tokens 624 against 627; correctness agreed on 91.3% of requests; reasoning-token counts agreed on 76% (all low-budget requests by construction, and the capped high-budget ones); the completion text was byte-identical on 10%. Seeded sampling in vLLM is reproducible only for the same batch composition and kernels, and the audit changed both the GPU type and the batch. The claim that reproduces is the aggregate one: the same accuracy and token statistics per budget within sampling noise, not the same samples. `results/aggregate/audit.json` holds the comparison.

## 6. Limitations

- One 4B model, two mathematics benchmarks, 150 questions each. The size and even the sign of a budget effect on other tasks or models is not established here; on MATH-500 level 3 the point estimate is negative.
- Sampling noise is 2 to 3 points on 150 questions. Two policies that assign the same budget to the same questions (fixed high and task-adaptive on MATH-500) differ by 2.0 points for that reason alone. The adaptive-versus-random contrast is not resolved at the 95% level.
- Budget forcing moves reasoning into the visible answer. The low budget is a real operating point for quality, but on MATH-500 it is not a cheaper one in total tokens, latency or energy. Any claim that a provider "saves computation" by cutting the budget holds for the medium budget on hard questions and for all budgets on GSM8K, not in general.
- Latency is attributed batch time on one engine and is confounded by batch size across policies, and by GPU type across seeds (two L40S seeds and one A100 seed in Experiment A; A100s throughout Experiment C). Energy is 1 Hz sampling with idle subtraction on shared nodes and carries the same confounds. Neither is a monetary cost.
- Grading is strict string or numeric matching after normalisation; algebraically equal answers in different forms count as wrong, equally at every budget.
- The reruns reproduce aggregates, not samples (Section 5).
- Nothing here is evidence about any commercial provider's practice. The gateway is a research abstraction of discretion a provider has when the customer specifies a service tier rather than an exact reasoning-token limit; a provider that guarantees an exact limit would not have it.

## 7. Implications for the theoretical paper

The paper models provider i's private serving action at round t as a delivered quality m_{i,t} in [0, M_i(x_t)] with an effort cost. This experiment gives that action a concrete reading. For a fixed model identity, the backend reasoning budget is a private choice made per request before generation; three settings of it produced three (quality, computation) points on the same questions, for example on MATH-500 level 4-5 accuracies of 66.7%, 77.6% and 77.6% at 128, 512 and 1,845 mean reasoning tokens, and the task-adaptive gateway shows the choice can depend on the request's observable context x_t and change from one request to the next. The capability M_i(x_t) corresponds to the accuracy at the budget beyond which more reasoning adds nothing, which this model reaches at the medium budget on these benchmarks; the cost of effort corresponds to the reasoning tokens, latency and energy the budget consumes.

Three things the experiment does not establish and the paper should not claim from it: that the set of operating points is a continuum rather than three settings; that the cost is convex in delivered quality (on MATH-500 the low budget is both worse and no cheaper in total tokens); and that any provider exercises this discretion against its customers. The experiment establishes feasibility and a measurable trade-off, which is what the model's private action requires.

## 8. Proposed manuscript text

The private action is not hypothetical. We served Qwen3-4B through vLLM with a fixed customer-visible configuration (model id, service tier, prompt, sampling parameters, output cap) and let a gateway set the backend reasoning-token budget per request, a control the serving system exposes but the client never sees. On 150 held-out GSM8K and 150 MATH-500 questions with three seeds, raising the budget from 128 to 2,048 tokens raised accuracy by 2.2 points on GSM8K (95% interval 0.4 to 4.7) and 5.1 points on MATH-500 (2.4 to 8.2), the MATH-500 gain coming entirely from its hardest third (11.0 points on level 4-5, already captured at 512 tokens), while mean reasoning tokens rose 7- and 13-fold. A gateway that assigned the high budget to competition mathematics and the low budget to arithmetic matched the all-high policy's accuracy with 31% fewer reasoning tokens per request, and a random assignment with the same budget mix did not. The same checkpoint thus offers several quality-against-computation operating points, and the operator chooses among them per request; this is the m_{i,t} of Section 2.
