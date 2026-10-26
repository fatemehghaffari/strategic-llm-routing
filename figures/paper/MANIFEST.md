# Paper figures: manifest

Produced by `audit/round2/A5/scripts/make_paper_figures.py` from committed data; style in `figstyle.py`.

Style: one colour and marker per method everywhere. MESP (ours) #D55E00 circle; CG-MESP #D55E00 diamond; single-price MESP #E69F00 square dashed; Cao et al. #CC79A7 triangle; UCB router #0072B2 down-triangle; ε-greedy router #56B4E9 plus; greedy router #9ecae1 right-triangle; static router #7f7f7f x; one-pull exclusion #009E73 star; fixed-buffer monitor #8c564b hexagon; two-sample monitor #17becf pentagon. References: oracle black dash-dot, second capability black dotted, honest benchmark grey dashed. Type: axis labels 8 pt, ticks 7.5, legend 7, panel letters 8 bold, annotations 7. No titles inside figures. Vector PDF (fonttype 42) + 300 dpi PNG under png/, tight layout, 0.02 in border. Every plotted number is in values_paper.csv (recorded once, from the composite).

Per-panel files: every multi-panel figure also exists as `fig_<name>_<letter>.pdf` (no panel letter inside; LaTeX adds it) at the widths listed below, which fill 7.0 in with 0.15 in gaps; `fig_<name>_legend.pdf` is a one-row legend strip for panels that share their series.

Palette validator: not run

The A4 frontier figure (a4_fig3) is not produced: its inputs undercut_summary.csv / undercut_comparison.csv are not in experiments/data/A4, so the known defect (routers above the oracle line) cannot be re-checked from committed data.

## fig_premise.pdf
- panels: 1
- data: A4/capabilities_finite_5shot.csv (RouterBench, 5-shot): capability of 11 models on 7 benchmark families
- series: highlighted: ['GPT-4', 'Claude-V2'] (the two models that are pointwise best on some family); 9 other models in light grey
- headline: GPT-4 is pointwise best on six of the seven families and Claude-V2 on the seventh; capabilities range 0.314 to 0.954
- file: `fig_premise.pdf`, width 3.33 in, height 2.1 in, legend: own legend below

## fig_two_worlds.pdf
- panels: a, b (horizontal bars, rules on the y axis)
- data: A4/headline_summary.csv, family_set Q3 only: 15 cells = 3 triples (highflip, lowflip, midflip: Claude-Instant-V1|Claude-V1|GPT-4, Claude-Instant-V1|Claude-V1|Claude-V2, Claude-V2|Llama-70B|Mixtral-8x7B) x 5 intrinsic-level settings (alpha 0.00, 0.25, 0.50, 0.75, het), n = 300,000, 10 seeds per cell; bar = mean over the 15 cells, whisker to the worst cell; A4/fine_shading_best.csv, the largest gain_per_round over cells and deviation kinds per rule (undercut for the routers, a shade for the two mechanisms)
- series: ours, pooled, ucb, eps, greedy
- headline: (a) compliant / best-responding: ours 0.694 / 0.396, pooled 0.695 / 0.353, UCB 0.721 / 0.710; honest benchmark 0.248; (b) best single deviation found: eps 0.0648 (undercut), UCB 0.0578 (undercut), greedy 0.0445, pooled 0.0026, ours 0.0105 (a shade; the committed fine_shading.csv puts the undercut against ours at 0.0001 in the worst cell)
- file: `fig_two_worlds_a.pdf`, width 3.9 in, height 2.0 in, legend: own legend
- file: `fig_two_worlds_b.pdf`, width 2.95 in, height 2.0 in, legend: none

## fig_scaling.pdf
- panels: 1
- data: A5/c3_provider_scaling.csv, n = 3e6, mean over subsets
- series: ours, ucb (compliant providers), cao; second capability and honest benchmark
- headline: ours 0.385 at K=3 to 0.445 at K=20; Cao 0.359 to 0.246; UCB 0.323 to 0.405
- file: `fig_scaling.pdf`, width 3.33 in, height 1.9 in, legend: own legend below

## fig_arrivals.pdf
- panels: a, b
- data: A5/c3_leaderboard_replicate.csv (n = 3e6, 10 subsets); audit/round2/A5/B_sim/v3_agg_2026-09-29.csv merged5, both horizons
- series: ours, ucb, cao; Cao unserved share annotated; one legend strip
- headline: (a) ours 0.426 to 0.426 across orders, UCB 0.371, Cao 0.369 iid to 0.149 grouped with unserved 20%/50%/58%; (b) real order: ours 0.630, UCB 0.616, Cao 0.537
- file: `fig_arrivals_a.pdf`, width 1.75 in, height 1.7 in, legend: shared strip
- file: `fig_arrivals_b.pdf`, width 1.3 in, height 1.7 in, legend: shared strip
- file: `fig_arrivals_legend.pdf`, width auto (one row) in, height 0.35 in, legend: strip

## fig_defences.pdf
- panels: 1
- data: A5/c11_router_static.csv and A5/c10_real_order.csv, order = real, mean over 10 subsets and both horizons; ours has no shading points because a shading winner is convicted and the mechanism switches, so only compliant and learning are drawn
- series: static, ucb, ours; second capability, honest benchmark
- headline: static 0.615 compliant to 0.211 / 0.090 / 0.198 (slow / fast / learning); UCB 0.616 to 0.509 / 0.506 / 0.524; ours 0.630 compliant, 0.456 learning; honest benchmark 0.509
- file: `fig_defences.pdf`, width 3.33 in, height 1.9 in, legend: own legend below

## fig_legitimacy.pdf
- panels: 1
- data: A5/c3_leaderboard_replicate.csv, all 880 cells (10 subsets x 4 orders x 2 horizons), mean per arm; routers facing compliant providers; the exploited-router arms are in fig_two_worlds and fig_defences
- series: ours, pooled, UCB, eps, greedy, Cao (price at intrinsic mean), Cao (zero price); false-conviction rate of a compliant provider printed beside the two mechanisms
- headline: pooled 0.426 with 48% false convictions; ours 0.418 with 0%; UCB 0.368; Cao 0.247 and 0.169, both leaving 21% of rounds unserved
- file: `fig_legitimacy.pdf`, width 3.33 in, height 1.7 in, legend: none

## fig_monitors.pdf
- panels: 1
- data: A4/monitor_frontier.csv, alpha a0.25, 300 replicates, n = 300,000; x false-switch rate on a complying winner, y median delay to detect a 0.05 shade (median_delay_mild); settings with detect_rate_mild < 0.5 drawn hollow in the 'not detected' band (fixed buffer 0.2 with burn-in 1,000, 10,000 or none)
- series: ours (anytime boundary at multipliers 0.25 to 2), fixed-buffer monitors, two-sample monitors
- headline: ours at multiplier 1: 0% false switches, 798 pulls to detect the 0.05 shade (199 for a bait-and-switch); two-sample at 0% false switches: 1000 pulls; fixed buffer 0.2 never detects the 0.05 shade unless its burn-in is 100 (then 68% of runs)

## fig_dynamics.pdf
- panels: a, b, c
- data: J traces <workspace>/J/n20k_r2 (10 seeds) and <workspace>/J/n300k (10 seeds); deviation shadeall: bid the capability, then deliver 0.05 (or 0.10) below the reference delivery in every later served round; common random numbers; IQR bands in (a)
- series: ours, cao, eps, ucb in (a); ours and cao at shade 0.05 solid / 0.10 dashed in (b, c), one legend strip for (b, c)
- headline: (a) gain at n: ours -3525, Cao 438, eps 163, UCB -717; (b) at 300K ours -41183 / -119488, Cao 9186 / -134610; (c) platform revenue/round ours 0.724 vs Cao 0.043 at shade 0.10
- file: `fig_dynamics_a.pdf`, width 2.233 in, height 1.9 in, legend: shared strip
- file: `fig_dynamics_b.pdf`, width 2.233 in, height 1.9 in, legend: shared strip
- file: `fig_dynamics_c.pdf`, width 2.233 in, height 1.9 in, legend: shared strip
- file: `fig_dynamics_legend.pdf`, width auto (one row) in, height 0.35 in, legend: strip

## fig_llm.pdf
- panels: a, b
- data: experiments/llm_effort/results/aggregate/table_A_levels.csv (subgroup rows) and table_C_policies.csv; Qwen3-4B, vLLM thinking_token_budget 128/512/2048; 150+150 held-out questions, 3 seeds
- series: (a) five subgroups; (b) fixed budgets line, task-adaptive, random matched
- headline: (a) MATH level 4-5 66.7% to 77.6%; GSM8K short 94.3% to 96.3%; (b) task-adaptive 91.7% at 880 tokens = fixed high 91.7% at 1277; random 90.1% at 711
- file: `fig_llm_a.pdf`, width 1.5 in, height 2.0 in, legend: shared strip
- file: `fig_llm_b.pdf`, width 1.5 in, height 2.0 in, legend: shared strip
- file: `fig_llm_legend_a.pdf`, width auto (two rows) in, height 0.35 in, legend: strip for (a)
- file: `fig_llm_legend_b.pdf`, width auto (one row) in, height 0.35 in, legend: strip for (b)

## fig_certified.pdf
- panels: a, b
- data: A2/exact_grid.csv family replicated_unique_top: (a) Q = 1 over n, exploit_LB/UB_per_round and prop61_gain/n; (b) K = 3, n = 8,000 over Q
- series: ours (exact backward induction); one legend strip
- headline: (a) UB 0.1258 at n = 2,000 to 0.0566 at 20,000, attained 0.0102; (b) UB 0.0790 at Q = 1, 0.1200, 0.2728, 0.3001 at Q = 2, 3, 4
- file: `fig_certified_a.pdf`, width 1.6 in, height 1.55 in, legend: shared strip
- file: `fig_certified_b.pdf`, width 1.6 in, height 1.55 in, legend: shared strip
- file: `fig_certified_legend.pdf`, width auto (one row) in, height 0.35 in, legend: strip

## fig_ladder.pdf
- panels: a, b (stacked)
- data: A2/ladder.csv, family replicated_unique_top, Q = 1, n = 20,000; (a) max over single-agent behaviours of gain_per_round_mean; (b) honest_benchmark_per_round minus the min over joint behaviours of platform reward; false-switch rate at the proposed profile
- series: rungs: full, windowed (monitor), no monitor, no slack, round-robin (fallback), runner-up (unmonitored), raw price; per-panel files 1.6 x 1.6 in for a side-by-side single-column layout; the 99.5% false-conviction note moved to the caption
- headline: best deviation 0.012 full vs 0.113 windowed vs 0.406 no monitor; shortfall 0.053 full vs 0.091 round-robin fallback vs 0.191 unmonitored runner-up / no monitor; no slack convicts a compliant winner in 99.5% of runs
- file: `fig_ladder_a.pdf`, width 1.6 in, height 1.6 in, legend: none
- file: `fig_ladder_b.pdf`, width 1.6 in, height 1.6 in, legend: none

## fig_monitor_path.pdf
- panels: 1
- data: <workspace>/J/n20k_r2/mesp_scalar_shadeall0.05_seed00.npz, primary pulls of the winner; tau = 0.6065, c = 20.154
- series: ours deficit vs tolerance
- headline: deficit crosses the tolerance at pull 7,552; tau 0.6065
- file: `fig_monitor_path.pdf`, width 3.33 in, height 1.8 in, legend: own legend inside

## fig_continuum.pdf
- panels: a, b, c
- data: A3/threshold_summary.csv: d = 1 inst C (K = 2), d = 2 inst E (K = 2), d = 3 inst D (K = 3); predicted turn-on bands {1:(6.53,6.58),2:(9.10,9.16),3:(11.78,11.85)} from audit/round2/A3/THRESHOLD_REPORT.md; (c) d = 1, instance C (K = 2); on instance E, whose capacities cross, the crash-conviction share plateaus at 50% from log10 n = 7.0, with zero false switches on both
- series: CG-MESP at d = 1, 2, 3 (line style), second-capability benchmark; one legend strip for (a, b), (c) carries its own
- headline: first positive price / all priced at log10 n: d=1 6.5 / 6.7, d=2 9.0 / 9.5, d=3 11.7 / 11.9; crash conviction 0 up to 6.4, 19% at 6.6, 100% from 6.7; false switches under the proposed profile: 0
- file: `fig_continuum_a.pdf`, width 2.233 in, height 1.9 in, legend: shared strip
- file: `fig_continuum_b.pdf`, width 2.233 in, height 1.9 in, legend: shared strip
- file: `fig_continuum_c.pdf`, width 2.233 in, height 1.9 in, legend: own legend
- file: `fig_continuum_legend.pdf`, width auto (one row) in, height 0.35 in, legend: strip

## fig_near_tie.pdf
- panels: 1
- data: A4/capability_gap_summary.csv, mech plmesp, delta > 0
- series: ours at the proposed profile; the lowest-revenue member of the equilibrium family
- headline: equilibrium revenue 0.724 up to gap 0.0060, 0.441 from 0.0065; proposed profile 0.754 to 0.527
- file: `fig_near_tie.pdf`, width 3.33 in, height 1.9 in, legend: own legend inside

## fig_app_complementarity.pdf
- panels: 1
- data: A4/complementarity.csv scope ALL (RouterBench 5-shot, 34,764 queries)
- series: 11 x 11 matrix ordered by overall accuracy
- headline: max cell 41.0%
- file: `fig_app_complementarity.pdf`, width 3.33 in, height 2.7 in, legend: colour bar

## fig_app_dynamics_extra.pdf
- panels: a, b
- data: J traces <workspace>/J/n20k_r2; <workspace>/J/cao_phases.csv (3 seeds)
- series: (a) ours, cao, eps, ucb; (b) Cao phases
- headline: Cao priced share 0 at 20K and 50K, 7% at 100K, 35% at 300K, 57% at 1M
- file: `fig_app_dynamics_extra_a.pdf`, width 3.2 in, height 1.9 in, legend: own legend
- file: `fig_app_dynamics_extra_b.pdf`, width 3.65 in, height 1.9 in, legend: own legend

## fig_app_graded_noisy.pdf
- panels: a, b, c
- data: A5/c9_graded.csv (variants emp, k10; n = 3e6, 10 subsets, 20 seeds); A5/c5_noisy_labels.csv (label-noise levels 0, 0.05, 0.10, 0.20)
- series: ours, pooled, ucb compliant, ucb shading (dashed), cao; one legend strip (two rows) that also names the two graded-score variants drawn as the dark and light bar of each pair in (a): empirical-variance scaled score (variant emp) and ten-level discretisation (variant k10)
- headline: (a) graded: ours 0.659 with 0% false convictions, pooled 0.687 with 76%; (b, c) ours false convictions 0% / 0% / 18% / 58% at noise 0 / 5 / 10 / 20%
- file: `fig_app_graded_noisy_a.pdf`, width 2.9 in, height 1.9 in, legend: shared strip
- file: `fig_app_graded_noisy_b.pdf`, width 2.1 in, height 1.9 in, legend: shared strip
- file: `fig_app_graded_noisy_c.pdf`, width 1.7 in, height 1.9 in, legend: shared strip
- file: `fig_app_graded_noisy_legend.pdf`, width auto (one row) in, height 0.35 in, legend: strip

## fig_app_type_scaling.pdf
- panels: a, b
- data: A5/c3_type_scaling.csv, Q in {7,13,23,33,48,63} on RouterBench fine partitions, 3 subsets, mean over both horizons (3e5, 3e6)
- series: ours, pooled, ucb compliant, ucb shading, cao; second capability; one legend strip
- headline: ours 0.685 at Q = 7 to 0.694 at Q = 63 with 0% false convictions; pooled convicts compliant providers in 33% (Q = 7) to 65% (Q = 63) of cells
- file: `fig_app_type_scaling_a.pdf`, width 3.9 in, height 1.9 in, legend: shared strip
- file: `fig_app_type_scaling_b.pdf`, width 2.95 in, height 1.9 in, legend: shared strip
- file: `fig_app_type_scaling_legend.pdf`, width auto (one row) in, height 0.35 in, legend: strip

## fig_app_substitution.pdf
- panels: 1
- data: A5/c3_substitution.csv, one 4-provider subset, n = 3e6, 10 seeds; a provider substitutes a cheaper model instead of shading effort
- series: ours, pooled, ucb, cao; oracle, second capability, honest benchmark; the percentages beside the Cao et al. markers are the shares of rounds it leaves unserved (29%, 14%, 53%)
- headline: learning substitution: ours 0.348 vs UCB 0.397 (UCB ahead); ours compliant 0.557; Cao 0.164 with 53% unserved
- file: `fig_app_substitution.pdf`, width 3.33 in, height 1.9 in, legend: own legend below

## fig_app_cao_per_type.pdf
- panels: 1
- data: A5/c7_cao_per_type.csv (n = 3e6) beside A5/c5_noisy_labels.csv variant 0.00, same 10 subsets, n = 3e6
- series: Cao per type (two price variants), Cao pooled, UCB compliant, ours; second capability, honest benchmark
- headline: Cao per type 0.368 / 0.557, Cao pooled 0.586, UCB 0.627, ours 0.659; second capability 0.635
- file: `fig_app_cao_per_type.pdf`, width 3.33 in, height 1.7 in, legend: own legend below

## fig_app_llm_extra.pdf
- panels: a, b
- data: experiments/llm_effort/results/aggregate/table_B_contrasts.csv; results/requests/main_policies_seed0.csv + gateway log (arrival order)
- series: (a) three contrasts per subgroup; (b) GSM8K and MATH-500 requests
- headline: MATH level 4-5: medium vs low +0.110, high vs medium -0.000; GSM8K short high vs low +0.020
- file: `fig_app_llm_extra_a.pdf`, width 3.7 in, height 2.3 in, legend: own legend inside
- file: `fig_app_llm_extra_b.pdf`, width 3.15 in, height 2.3 in, legend: own legend inside (two stacked rows)

## fig_alternatives.pdf
- panels: a, b
- data: (a) A5/c3_provider_scaling.csv, n = 3e6; (b) A5/c11_router_static.csv and A5/c10_real_order.csv, order = real, mean over 10 subsets and both horizons, plus A5/c13_mesp_shading.csv for MESP under the two reduction schedules when present
- series: ours, ucb, cao (a); static, ucb, ours (b); second capability and honest benchmark
- headline: (a) ours 0.385 at K=3 to 0.445 at K=20, Cao 0.359 to 0.246, UCB 0.323 to 0.405; (b) static 0.615 / 0.211 / 0.090 / 0.198, UCB 0.616 / 0.509 / 0.506 / 0.524, ours 0.630 compliant and 0.456 learning plus MESP under slow and fast reduction from c13
- file: `fig_alternatives_a.pdf`, width 1.6 in, height 1.8 in, legend: shared strip
- file: `fig_alternatives_b.pdf`, width 1.6 in, height 1.8 in, legend: shared strip
- file: `fig_alternatives_legend.pdf`, width auto (one row) in, height 0.35 in, legend: strip
