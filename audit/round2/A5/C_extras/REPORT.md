# Agent C (extras): items 7, 9, 5, 4+6, 8

STATUS: DONE 2026-09-29T15:05Z

## Pre-registered grids

Common setup (v2): the 10 subsets of `audit/round2/A4/scripts/arrival_order_subsets_v2.txt`, Mixtral-8x7B
the only honest provider and it stays at its floor mu, mu_i(x) = min(M_i(x), M_Mistral-7B(x)), linear cost,
Q7 task types with RouterBench 5-shot masses. Provider observation model per the author's rule of 28 Sep:
own history, own messages, whether chosen, and t only. `LowEq` (reads pointwise-top masks) is NOT used.
Code `audit/round2/A4/scripts/extras_c.py`, tasks `slurm/extras_c_tasks_c1.txt`, script `slurm/extras_c.sbatch`.
Traces `<workspace>/v3/C/<item>/<variant>/<subset>/<n>/<order>/`.

**C1a, item 7 (registered 28 Sep, before any full run).** OUR CONSTRUCTION, not the mechanism of Cao et al.:
one independent copy of their Mechanism 1 per task type, each copy told its realised query count as its
horizon, pooled-mean target within the copy, arms `cao_eqmu` (strategic providers stop at mu in unmonitored
rounds) and `cao_eq0` (stop at 0). Orders iid/bursty/drift/grouped, n in {3e5, 3e6}, 20 seeds. 80 tasks.
Comparison rows are the v2 results already in `experiments/data/A4/v2_all_summary.csv`.

**C1b, item 9 (registered 28 Sep).** Rewards in [0,1] with mean m. Variant `emp`: Beta(m k, (1-m) k) with
k = 1/r - 1, r the measured score-variance ratio per type (`experiments/data/A5/score_variance_5shot.csv`:
GSM8K r = 0.180, MT-Bench r = 0.580; the other five types are 0/1 and stay Bernoulli). Variant `k10`: Beta
with k = 10 on every type. Arms plmesp_star, mesp_star, cao_eqmu, router_ucb exploit_slow, router_ucb
average. Orders iid, bursty; n = 3e6; 20 seeds. 40 tasks. Question: do conviction rates and revenue move?

**C2-uniform, item 5 (registered 28 Sep).** Mechanism and router see a label that is wrong with probability
eps, uniformly to another type; quality follows the true type; mislabelling independent of everything else.
eps in {0, 0.05, 0.1, 0.2}; arms as C1b; order iid; n = 3e6; 20 seeds. 40 tasks. The measured confusion
matrix from Agent A, the `real` order and `router_audit` are added in a second registration once available.
Headline metric: PL-MESP compliant-conviction rate and revenue against eps.

**C3, items 4+6 (registered 28 Sep, before any C3 run).** Code `extras_c3.py`, tasks `slurm/extras_c_tasks_c3.txt`
(140 tasks). Subset lists: `c3_leaderboard_subsets.txt`.
- *Deviation from the brief, forced by data access:* the Open LLM Leaderboard per-question tables are gated
  (Agent A did not accept terms on the author's behalf), so there is no ~50-subcategory leaderboard table.
  The **type-scaling** test uses RouterBench's own 63 fine types instead (57 MMLU subjects, ARC, GSM8K,
  HellaSwag, MBPP, Winogrande, MT-Bench merged), table `experiments/data/A5/routerbench_fine63_5shot.csv`.
  Nested partitions `fine_partitions.csv`: the 6 non-MMLU types are fixed, and the MMLU subjects are
  assigned round-robin in a seeded permutation (seed 20260928) to Q-6 groups, Q in {7, 13, 23, 33, 48, 63}.
- (a) **Replication** on the leaderboard coarse table (6 benchmarks, 20 models, masses proportional to
  benchmark item counts): honest provider Llama-3.1-8B-Instruct (the 10th of 20 by pooled capability,
  the median-low rule), intrinsic level = the lowest pooled model, Qwen2.5-0.5B-Instruct, capped at each
  provider's capability. Subsets: the select_subsets_v2 rule (K = 3, 4, 5 at quantiles .1/.5/.9 of the
  pooled-vs-contextual gap, plus the K = 6 median). 11 arms (PL-MESP S*, MESP S*, both Cao equilibria, UCB,
  eps-greedy and greedy routers under exploit and average); 4 orders; n in {3e5, 3e6}; 20 seeds.
  *Note registered before running:* the pooled-vs-contextual gap on this table is small (-0.005 to +0.011),
  because six broad benchmarks rank these models nearly identically. This table is a weak test of the
  contextual advantage by construction and is reported as such.
- (b) **Provider scaling**: same table, K in {3, 5, 8, 12, 16, 20}, providers added in a seeded permutation
  (seed 20260928) after the honest one; n = 3e6, iid, 10 seeds, 5 arms (PL-MESP, MESP, Cao eq-mu, UCB
  exploit_slow, UCB average). **Type scaling**: v2 subsets k4_q90, k5_q50, k6_q50 (Mixtral honest, mu =
  Mistral-7B), Q in {7, ..., 63}, n in {3e5, 3e6}, iid, 10 seeds, same 5 arms. The theory's cut-off is
  Q ~ n^{1/3} (log n)^{-1/3}: about 29 at n = 3e5 and about 59 at n = 3e6.
- (c) **Substitution as shading**: the four family flagships (Qwen2.5-72B, Llama-3.3-70B, gemma-2-27b,
  Mistral-Large-2411); honest = gemma-2-27b (pre-registered: the flagship of the only family without a
  70B-class model); each provider's intrinsic level and floor = its own family's smallest variant; a
  strategic provider can deliver only one of its family's variants. Profiles `learning_subst` (Agent B's
  Learner, quantised down to the nearest own variant) and `switch_cheapest` (capability for ceil(4 log n)
  own selections, then the cheapest variant), plus two continuous references (PL-MESP S*, Cao eq-mu).
  Orders iid, bursty; n = 3e6; 10 seeds. Smoke result (1 seed, 3e5) recorded before the full run:
  learning_subst revenue 0.341 PL-MESP, 0.339 Cao, 0.369 UCB; second capability 0.583, honest 0.298.

## Milestones
- 28 Sep: default-off `reward_fn` hook added to `mechanisms.py` (MechanismRun.run, run_router, run_second_best):
  the uniform draw is still consumed, so every existing run is bit-identical when the hook is absent.
- 28 Sep: `extras_c.py` (items 7, 9, 5) smoke-tested; traces reproduce summary revenue exactly.
- 28 Sep: C1 + C2-uniform launched, Slurm 65004124, 160 tasks.
- 28 Sep: `extras_c3.py` (items 4+6: replicate, scale, subst) written; replicate mode smoke-tested on
  Agent A's merged-5 RouterBench table as a stand-in. Waiting for Agent A's leaderboard tables.

## Results (all runs complete: 300 tasks, 31,080 traces, 352 CPU-hours)

Aggregates in `experiments/data/A5/`: c7_cao_per_type.csv, c9_graded.csv, c5_noisy_labels.csv,
c3_leaderboard_replicate.csv, c3_provider_scaling.csv, c3_type_scaling.csv, c3_substitution.csv.
Printer: `audit/round2/A4/scripts/aggregate_c.py`. Revenue is per round, mean over subsets and seeds.

**Item 7, Cao one copy per type (OUR construction).** Order-invariant, as expected: copies never see bursts
of another type, and none of its monitors fired. PL-MESP S* is still ahead on every subset: +0.12 (3e5) and
+0.09 (3e6) over the mu-equilibrium, and +0.25 to +0.33 over the 0-equilibrium, in every order.
Per-type Cao revenue: 0.523 / 0.318 at 3e5 and about 0.56 / 0.37 at 3e6. So splitting Cao per type removes its
order fragility, but it still loses to PL-MESP because shirking in unmonitored rounds is its equilibrium.

**Item 9, graded rewards.** No effect. Revenue and conviction rates are identical to the Bernoulli runs to
three decimals, for both the empirical-variance and k = 10 variants (e.g. PL-MESP 0.659, conviction 0.00;
MESP 0.693, conviction 0.80; Cao eq-mu bursty 0.262, fires 0.56). The monitor needs only bounded rewards.

**Item 5, noisy task labels. GOES AGAINST US.** Revenue barely moves (PL-MESP 0.659 / 0.657 / 0.656 /
0.656 at eps 0 / 0.05 / 0.1 / 0.2), but **PL-MESP convicts an honest winner in 0% of runs at eps <= 0.05,
18% at eps = 0.1 and 58% at eps = 0.2.** Mislabelled prompts come from types where the winner is weaker,
so its delivered mean at the labelled type falls below the price. Revenue survives only because the fallback
earns well under S*. MESP convicts at 80% regardless; Cao and the routers are unaffected (they either
pool the labels or do not monitor). The measured confusion matrix and the `real` order were not run: Agent
A's `classifier_confusion.csv` and real stream did not exist when this package closed. Practical reading:
PL-MESP needs a task classifier with at most about 5% error, or a monitoring tolerance that absorbs the
label noise. This must be stated as a limitation.

**Items 4+6(a), replication on the Open LLM Leaderboard coarse table (6 benchmarks, 20 open models).**
The contextual advantage is weak here, as pre-registered (pooled-vs-contextual gap -0.005 to +0.011).
- PL-MESP S*: 0.409 (3e5), 0.426 (3e6), identical in every order, no false convictions.
- Ahead of every exploited router, greedy router and both Cao equilibria on 10/10 subsets in every order.
- Ahead of UCB and eps-greedy at average effort on 8/10 (0.426 vs 0.37 on average).
- Cao under realistic order stops serving 18 to 22% (3e5) and 50 to 58% (3e6) of the horizon under
  bursty/grouped arrivals; in iid order its mu-equilibrium earns 0.369 at 3e6.
- **Against us:** MESP (scalar) again beats PL-MESP at 3e6 (0.458 iid, 0.474 bursty) through false
  convictions (65 to 78% of runs), the same effect as on RouterBench.
- Second capability 0.455, honest benchmark 0.217.

**Item 4(b), provider scaling (leaderboard, K = 3 to 20, 3e6, iid).** PL-MESP rises 0.385 to 0.445,
no false convictions. Cao eq-mu falls 0.359 to 0.246 as K grows (its phase budgets grow with K). UCB
average 0.32 to 0.41, UCB exploited flat at about 0.23. MESP again highest from K = 8 on (0.51 to 0.54),
with false convictions in every run.

**Item 4(b), type scaling (RouterBench fine types, Q = 7 to 63; the theory's cut-off is about 29 at 3e5 and
about 59 at 3e6).** PL-MESP does NOT break: revenue 0.674 to 0.687 (3e5) and 0.697 to 0.700 (3e6), zero
false convictions at every Q. **This is NOT evidence that the cut-off is loose.** With Q large, many
low-mass types never finish elicitation, and under S* elicitation delivers capability, which earns more
than the second price. The revenue therefore flatters PL-MESP past the cut-off; what the cut-off
predicts, the loss of the incentive guarantee there, is not measured by revenue under S*. Report it with
that caveat or drop it. MESP starts falsely convicting at 3e5 once Q >= 48 (7 to 40%), and at 90% at Q = 63
at 3e6.

**Item 6(c), substitution as shading (4 flagships, each can only serve its family's variants, 3e6).
GOES AGAINST US under learning providers.**
- With learning providers, PL-MESP earns 0.348 against 0.392 to 0.402 for UCB. Honest benchmark 0.297,
  second capability 0.583.
- With scripted cheapest-switch providers: PL-MESP 0.327, UCB 0.343.
- Cao with learners 0.213 (iid) / 0.115 (bursty), stopping service on 39% / 67% of the horizon.
- PL-MESP under S* (continuous delivery allowed) earns 0.557.
- So when shading is discrete and learners choose it, PL-MESP loses its advantage over a quality-estimating
  router on this subset: the learners shade the elicitation bids down, the low-revenue equilibrium the
  paper already names. One subset only (pre-registered), 10 seeds.

**Item 8 (LinUCB): not run.** Cut as planned; it needs a per-prompt simulator.

- 28 Sep: tasks 6-159 of 65004124 moved by the main agent to `cpu-preempt` with requeue (the `cpu` fairshare
  start was 2 Oct). `slurm/extras_c.sbatch` now uses `--partition=cpu-preempt --requeue`. Every task is
  idempotent: it rewrites its CSV after each arm and overwrites its trace files, so a preempted task that
  restarts from scratch leaves no stale or partial state.

## Deviations and cautions
- Item 5 ran uniform noise only (no measured confusion matrix, no real order): upstream files never appeared.
- Type scaling used RouterBench fine types rather than leaderboard subcategories (gated data).
- Type scaling at large Q is confounded by unfinished elicitation, as explained under Results.
- Provider scaling ran 10 seeds at one horizon; substitution ran one pre-registered subset.
- The low-revenue profile of PL-MESP (`plmesp_low`, class `LowEq`) is not run anywhere in this package:
  it reads pointwise-top masks, i.e. information about other providers, which the author's observation
  rule of 28 Sep forbids.
