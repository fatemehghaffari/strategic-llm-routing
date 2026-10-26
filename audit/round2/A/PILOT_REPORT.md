# Pilot report (Agent A, round 2)

Acceptance tests of `EXPERIMENT_DECISION.md` Section 8, with measured values, recorded before any final run. Code: worktree `wt-A`, branch `scout/A`, commit 0a5609a and later. All numbers below are pilot numbers on pilot or eval seeds (phase ids 0 and 3); no final-phase seed has been used.

## E1. Exact exploitability of MESP over B_{i,n} (information structure I0 plus the announced tau)

Method: two-action backward induction over the deviator's information state (affine one-step objective, so bang-bang is exact); Stage 1 over (own pull, own successes) with the terminal value integrated over the exact law of the others' bids under S_star; Stage 2 over (r, Z_r) per price value; fallback continuation bracketed by 0 and the appendix bound; baseline utility by the same recursions with the S_star policy fixed. Implementation `scratch/experiments/round2/exploitability/dp.py`; validation `validate_dp.py`; simulator `common/mechanism.py` (uniform tapes per (agent, pull), the proof's coupling).

### Exact values (utility units; per round in parentheses)

| instance | n | L_n | N_n | s_n | exploit LB | exploit UB (I0) | exploit UB (I1) | Stage-2 gain vs b_n(N_n) | adaptive Stage-1 gain | L_n times slack | revised constant / n | previous constant / n | distinct prices | seconds |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| unique_top | 500 | 83 | 251 | 0.401 | 62.3 (0.1246) | 76.3 (0.1526) | 87.5 (0.1751) | 53.7 vs 56.6 | 8.7 | 20.8 | 0.742 | 1.544 | 48 | 0.4 |
| unique_top | 1000 | 166 | 502 | 0.298 | 108.0 (0.1080) | 134.3 (0.1343) | 151.1 (0.1511) | 84.2 vs 84.3 | 23.9 | 41.5 | 0.583 | 1.178 | 84 | 1.3 |
| unique_top | 2000 | 326 | 1022 | 0.222 | 181.9 (0.0910) | 215.0 (0.1075) | 239.7 (0.1198) | 125.9 vs 126.1 | 56.0 | 81.5 | 0.464 | 0.909 | 120 | 4.3 |
| tied_top | 500 | 83 | 251 | 0.401 | 28.8 (0.0575) | 39.2 (0.0784) | 53.7 (0.1073) | 28.0 vs 56.6 | 0.8 | 0.0 | 0.742 | 1.544 | 46 | 0.3 |
| tied_top | 1000 | 166 | 502 | 0.298 | 44.4 (0.0444) | 56.9 (0.0569) | 86.8 (0.0868) | 42.2 vs 84.3 | 2.3 | 0.0 | 0.583 | 1.178 | 70 | 1.1 |
| tied_top | 2000 | 326 | 1022 | 0.222 | 69.4 (0.0347) | 84.6 (0.0423) | 144.7 (0.0724) | 63.0 vs 126.1 | 6.4 | 0.0 | 0.464 | 0.909 | 99 | 3.6 |

Reading. The Stage-2 optimum extracts the monitoring slack b_n(N_n) to within one utility unit in unique_top (the price is far below capacity, so boundary tracking is always available) and about half of it in tied_top (the deviator wins Stage 1 with probability one half only). The adaptive Stage-1 gain is the bid-to-count underbidding (deliver M_i until the count secures the win, then stop), worth 56 utility at n = 2,000 in unique_top against 16.3 for the fixed underbid of .05 that the current figure shows. Per-round exploitability decreases in n at every step. The revised top-agent constant L_n + 2 b_n(n) + R_K(n) is 5 to 6 times the certified upper bound at these horizons; the previous constant (with 2 n s_n) is about twice that again. At n at most 1,000 the price is degenerate (s_n at least .30), so these horizons show Stage-1 effects mostly; the final grid extends to 50,000.

### Acceptance tests (Section 8, E1)

| instance | n | (i) baseline in DP bracket | (i) P(win) sim vs DP | (i) E[tau given win] sim vs DP | (ii) DP policy reproduces V_I0_F0: sim t-interval vs DP | (ii) full simulated gain within [LB, UB_I0] | (iii) every hand-picked gain at or below UB_I0 | (iv) affinity: states checked, worst grid excess | all pass |
|--|--|--|--|--|--|--|--|--|--|
| unique_top | 500 | True (sim 230.0 [229.3, 230.6], DP [230.1, 230.1]) | 1.000 vs 1.000 | 0.250 vs 0.249 | [292.3, 293.9] vs 292.4: True | [62.6, 63.8] vs [62.3, 76.3]: True | True | 1005, 5.7e-14 | True |
| unique_top | 1000 | True (sim 408.1 [407.1, 409.0], DP [408.5, 408.5]) | 1.000 vs 1.000 | 0.353 vs 0.352 | [513.9, 517.6] vs 516.6: True | [106.2, 109.1] vs [108.0, 134.3]: True | True | 945, 5.7e-14 | True |
| unique_top | 2000 | True (sim 753.2 [751.8, 754.6], DP [752.2, 752.2]) | 1.000 vs 1.000 | 0.427 vs 0.428 | [933.1, 938.2] vs 934.1: True | [180.5, 184.4] vs [181.9, 215.0]: True | True | 980, 1.1e-13 | True |
| tied_top | 500 | True (sim 114.4 [109.8, 119.0], DP [115.9, 115.9]) | 0.491 vs 0.500 | 0.374 vs 0.375 | [136.4, 148.3] vs 144.7: True | [26.3, 29.6] vs [28.8, 39.2]: True | True | 1005, 2.8e-14 | True |
| tied_top | 1000 | True (sim 202.9 [195.1, 210.8], DP [204.2, 204.2]) | 0.495 vs 0.500 | 0.484 vs 0.485 | [238.5, 257.6] vs 248.7: True | [42.4, 47.9] vs [44.4, 56.9]: True | True | 945, 5.7e-14 | True |
| tied_top | 2000 | True (sim 372.4 [358.6, 386.3], DP [371.0, 371.0]) | 0.503 vs 0.500 | 0.565 vs 0.565 | [425.2, 457.3] vs 440.4: True | [63.6, 74.1] vs [69.4, 84.6]: True | True | 980, 1.1e-13 | True |

Validation used 1,500 paired seeds per cell (phase eval). Hand-picked gains at n = 2,000 in unique_top (mean [t-interval]): underbid_05 16.3 [16.3, 16.3]; underbid_15 48.1 [46.9, 49.2]; primary_shade_05 51.1 [51.1, 51.1]; primary_shade_15 -81.3 [-86.4, -76.1]; bait_switch -448.8 [-449.8, -447.7]; trigger_fallback_shade -533.7 [-534.6, -532.7]; boundary_ride 61.4 [61.4, 61.4]. The fixed boundary-riding schedule (tau minus 1/sqrt(r)) gains 61.4, the exact optimum 181.9 to 215.0.

Items (v) to (viii) are scheduled: (v) randomized-grid policies versus the two-action DP will be covered by the CMA-ES search (must not exceed UB_I0); (vi) one CMA-ES restart at n = 2,000 pending; (vii) decrease over a decade and comparison with the constant pending the final horizon grid to 50,000 (already true over 500 to 2,000); (viii) extended-precision rerun pending.

Diagnostics recorded. (a) The optimal policy is a two-threshold rule in Z at almost every state (deliver M_i iff a_r <= Z_r < b_r: shade both when far above the boundary and when a switch has become unavoidable; in Stage 1 stop exerting effort both when the win is secured and when it is hopeless); rows where a strict preference for the low target sits inside the interval are counted in the JSON (`noninterval_stage2_rows`) and were rare after excluding exact ties. (b) In unique_top at n = 500, bait-and-switch shows a positive paired gain (about 11 utility) because the price is (.65 minus .40)_+ = .25 there: the degenerate small-horizon price, as Scout A4 warned; it is negative from n = 1,000 on.

### Instance-table reconciliation

`common/instances.json` keeps the scalar_incentives parameters under the legacy aliases (unique_top, tied_top, near_gap, honest_top, low_gap_nontop), so none of the quoted incentive numbers in `appendix_experiments.tex` changes for that reason. The scalar_performance suite used different intrinsic means for the honest agent (.40, .45, .50 versus .35, .35, .45): under S_star that agent delivers its capacity in every phase, so platform reward, tau, and phase lengths are unchanged in law and only the honest agent's effort (hence `effort_per_round` and `total_effort`) changes; the regenerated performance figure will state the unified table. The quoted minus .091 for `nontop_win_underperform` is the duplicated bait_switch value and is dropped (Scout A4 defect 2).

## Compute

See `COMPUTE_LOG.md`; E1 pilots ran on the login node in about six minutes total.

## E3a. Exact in-class (S_HDS) exploitability of Static Grid-ETC

Method: per-cell decomposition (Scout A2, Section 5.2), implemented in `scratch/experiments/round2/contextual_exact/exact_etc.py` with `run_exact.py` (cross-check and table) and `monotonicity.py`. Under fixed maps each cell's rewards are i.i.d. with the cell-average target, exploration ignores rewards, and commitment is a function of the exploration counts, so the deviator's utility is a sum over cells of U_C(m) = (1 + mu_bar_{i,C} minus m) times [E min(V_C, K q_n)/K + p_i(m) E (V_C minus K q_n)_+], with V_C binomial and p_i the exact commitment probability against the others' binomial counts under uniform priority. The supremum over full-profile maps is the sum of per-cell maxima; over own-context maps it separates by the deviator's own interval. Cell averages use adaptive quadrature with the environment's breakpoints; the reported grid error bound is n (1 + q_n) times the refined grid step.

Environments: `current` (the retained instance: capacities .72, .72, .53 + .08 x_3, top set {0,1} everywhere) and `separator` (Scout A2, Section 5.4: M_0 = M_1 = .75, M_2(x) = .75 minus .25 (0.6 minus x)_+, so the top set is {0,1} below x_2 = 0.6 and {0,1,2} above, both components with at least two top agents, capacities continuous). Focal deviators: agent 0 (top everywhere) and, in `separator`, agent 2 (non-top below the separator, top above).

### Acceptance tests (Section 8, E3)

(i) Exact formula against the retained `contextual_incentives/summary.csv`: 14 of the 15 committed cells contain the exact value; the exception is `near-boundary` at n = 32,000 (exact minus 262.07 against the committed interval [minus 300.12, minus 269.10], z = plus 2.88). An independent fresh sample of 480 paired replicates with the retained code gives mean minus 263.77 [minus 275.08, minus 252.46], so the exact value is within 0.30 standard errors of an independent estimate and the committed 240-replicate interval was the outlier, not the formula. `constant` at the same horizon re-checks at z = plus 1.05. Cross-check (i) passes.

(iv) Pathwise monotonicity of Grid-ETC: 2,000 coupled paths at n = 2,000 and 300 at n = 8,000, raising agent 0 from a constant .10 shade to capacity with identical contexts, reward uniforms, exploration permutations, and cell priorities. Violations: 0 of 2,300. Other agents' pull counts changed by mean minus 18.2 (maximum 0, minimum minus 98) at n = 2,000 and mean minus 238.2 (maximum 0) at n = 8,000, while the raised agent gained the complementary amount. The theorem's pathwise claim survives this test.

Pending from the E3 list: the batched cell-wise evaluator reproducing `path()` pathwise (cross-check (ii)) and the CMA-ES search over 32-bin own-context maps (cross-check (iii)); (i) and (iv) are the two that gate the exact table, and both pass.

### Exact exploitability, three grid rules

Exploitability per round, deviator against all-maximum play, `equal` = the retained rule h = n^(-1/(D+3)) with a clipped last cell, `equalized` = exact tiling with b_n = round(1/h_n) cells per axis, `dyadic` = h = 2^(-ceil(log2(n)/(D+3))). "KqJ/n" is the nominal exploration budget over the horizon; "thin" counts cells whose expected exploitation visits are below one.

| env | focal | grid | n | cells | KqJ/n | thin | explore share | exploit full | exploit own | stress (outside S_HDS) |
|--|--|--|--|--|--|--|--|--|--|--|
| current | 0 | equal | 8,000 | 125 | 0.94 | 61 | 0.764 | +0.13294 | +0.13294 | +0.0794 |
| current | 0 | equal | 32,000 | 216 | 0.65 | 16 | 0.635 | +0.07161 | +0.07161 | +0.1268 |
| current | 0 | equal | 128,000 | 512 | 0.61 | 169 | 0.451 | +0.00991 | +0.00335 | +0.1941 |
| current | 0 | equal | 512,000 | 729 | 0.34 | 0 | 0.342 | +0.00000 | +0.00000 | +0.2355 |
| current | 0 | equal | 2,000,000 | 1,728 | 0.33 | 397 | 0.310 | +0.01412 | +0.00480 | +0.2479 |
| current | 0 | equalized | 8,000 | 64 | 0.48 | 0 | 0.480 | +0.00401 | +0.00371 | +0.1745 |
| current | 0 | equalized | 32,000 | 216 | 0.65 | 0 | 0.648 | +0.07767 | +0.07767 | +0.1218 |
| current | 0 | equalized | 128,000 | 343 | 0.41 | 0 | 0.410 | +0.00000 | 0.00000 | +0.2087 |
| current | 0 | equalized | 512,000 | 729 | 0.34 | 0 | 0.342 | +0.00000 | +0.00000 | +0.2355 |
| current | 0 | equalized | 2,000,000 | 1,331 | 0.25 | 0 | 0.252 | +0.00000 | +0.00000 | +0.2690 |
| current | 0 | dyadic | 8,000 | 512 | 3.84 | 512 | 1.000 | +0.24000 | +0.24000 | +0.0000 |
| current | 0 | dyadic | 32,000 | 512 | 1.54 | 512 | 1.000 | +0.24000 | +0.24000 | +0.0000 |
| current | 0 | dyadic | 128,000 | 512 | 0.61 | 0 | 0.612 | +0.05922 | +0.05922 | +0.1372 |
| current | 0 | dyadic | 512,000 | 4,096 | 1.92 | 4,096 | 1.000 | +0.24000 | +0.24000 | +0.0000 |
| current | 0 | dyadic | 2,000,000 | 4,096 | 0.77 | 0 | 0.774 | +0.13393 | +0.13393 | +0.0812 |
| separator | 0 | equalized | 8,000 | 64 | 0.48 | 0 | 0.480 | +0.03457 | +0.03457 | +0.1490 |
| separator | 0 | equalized | 32,000 | 216 | 0.65 | 0 | 0.648 | +0.10293 | +0.10293 | +0.1030 |
| separator | 0 | equalized | 128,000 | 343 | 0.41 | 0 | 0.410 | +0.00830 | +0.00200 | +0.1762 |
| separator | 0 | equalized | 512,000 | 729 | 0.34 | 0 | 0.342 | +0.00000 | 0.00000 | +0.2000 |
| separator | 0 | equalized | 2,000,000 | 1,331 | 0.25 | 0 | 0.252 | +0.00000 | +0.00000 | +0.2307 |
| separator | 2 | equalized | 8,000 | 64 | 0.48 | 0 | 0.480 | +0.05150 | +0.05150 | +0.0889 |
| separator | 2 | equalized | 32,000 | 216 | 0.65 | 0 | 0.648 | +0.11397 | +0.11397 | +0.0564 |
| separator | 2 | equalized | 128,000 | 343 | 0.41 | 0 | 0.410 | +0.03729 | +0.03729 | +0.0882 |
| separator | 2 | equalized | 512,000 | 729 | 0.34 | 0 | 0.342 | +0.02786 | +0.02782 | +0.0923 |
| separator | 2 | equalized | 2,000,000 | 1,331 | 0.25 | 0 | 0.252 | +0.01994 | +0.01976 | +0.0990 |

The full table (both environments, three grids, five horizons, both focal agents, with argmax cell averages) is in the scratchpad at `runs/pilot/contextual_exact/exact_exploitability.csv`.

### Two structural findings that the grid choice decides

1. The clipped last cell of the retained rule is freely shadeable. With b_n = ceil(1/h_n) intervals the last interval is a remainder (0.0200 against h = 0.0891 at n = 2,000,000), so cells touching it carry tiny mass, never reach the K q_n visits needed to commit, and let an in-class deviator shade to zero at no allocation cost. At n = 2,000,000 exactly 100 percent of the in-class gain comes from the 397 of 1,728 cells with expected exploitation visits below one, and the per-round gain rises from 0.00000 at n = 512,000 (where the remainder happens to be nearly a full cell) to 0.01412 at 2,000,000. This also explains why full-profile maps beat own-context maps only at those horizons (0.01412 against 0.00480): a full-profile map can isolate the thin cells, an own-context map cannot. The effect is o(n) and consistent with the theorem, but it is the dominant finite-horizon term and it is an artifact of the rounding, not of the rate.

2. The dyadic rule as specified over-refines. With k_n = ceil(log2(n)/(D+3)) the exploration budget K q_n J_n exceeds the horizon at n = 8,000 (ratio 3.84), 32,000 (1.54) and 512,000 (1.92): no cell ever finishes exploring, the rule never commits, and in-class exploitability is pinned at M_bar/K = 0.24 per round with no decay over two decades of horizon. The same degeneracy affects the retained `equal` rule at n = 2,000 (ratio 1.25), which is the regime the current paper's contextual incentive figure lives in.

3. Exact tiling fixes both. Setting b_n = round(1/h_n) and h = 1/b_n (option `equalized`, added to `common/design.py`) leaves no thin cells at any tested horizon and gives in-class exploitability that falls to exactly zero for the top deviator in both environments by n = 128,000 to 512,000, and to 0.0199 per round at n = 2,000,000 for the mixed deviator (agent 2 of the separator instance, non-top below the separator and top above), which is the slowest-decaying in-class case found. The residual non-monotonicity (0.004 at 8,000, 0.078 at 32,000, 0.000 at 128,000) is the integer jump of b_n, which makes the exploration share oscillate (0.48, 0.65, 0.41, 0.34, 0.25); it is intrinsic to any integer cell count and must be shown rather than smoothed.

Recommendation to the main agent and the theory lead: report `equalized` as the rule in the paper, or state the clipped-cell term explicitly. This is an experimental finding about constants, not about the rate; nothing here contradicts Theorem thm:grid-etc or thm:contextual-public, and none of it is evidence about equilibrium.

### Out-of-scope stress test

Count-based explore-then-shade (deliver capacity during the cell's own exploration pulls, then shade; feasible under the blind model without any information relaxation) gains 0.09 to 0.27 per round and grows with n, because the exploitation share grows. It must be reported in a separate hatched panel labelled "outside S_HDS; the theorem makes no claim and its proof is known to fail for phase-dependent play". The contrast with the in-class values (which fall to zero) is the honest way to show what the fixed-map restriction buys.

## E1 final grid (exact DP, 96 cells)

Slurm array 64554035, 96 tasks, 19.03 core-hours, all COMPLETED. 63 of the 96 results were kept; 33 were lost to an implementation defect found afterwards and re-run as job 64555834 (below). The table `runs/final/exploitability/exploitability_grid.csv` holds every cell.

### Structure of the exact optimum, across instances

The Stage-2 optimum divided by b_n(N_n) identifies what the deviator extracts, and across the 96 distinct cells it tracks the probability of winning Stage 1: the two agree to within 0.001 in 73 cells, 0.005 in 84 and 0.01 in 88, with all eight exceptions at n = 200 or n = 500 where the conservative price is degenerate. So the optimal in-class Stage-2 deviation extracts the monitoring slack on the histories where it is the winner, wherever the mechanism is in its intended regime. The ratio is close to 1 in the always-winning instances (unique_top, near_gap at large n, K2_unique_top, K5_unique_top, unique_top_muHigh) and close to one half in the tied instances (tied_top, K2_tied_top, gap_K3_0.00), but it is not exactly either: over the 33 always-winning cells it runs from 0.527 to 1.002 and over the 19 tied cells from 0.260 to 0.501, the spread coming from the small horizons. The precise statement is the one above, and it replaces the exact constants asserted in an earlier draft. The adaptive Stage-1 gain grows like L_n and reaches 676 utility at n = 50,000 in unique_top against 245 for the best fixed underbid.

Per-round certified lower bounds decay with a log-log slope between minus 0.25 and minus 0.51 over the top four horizons (unique_top minus 0.335, tied_top minus 0.406, near_gap minus 0.359, honest_top minus 0.252, low_gap_nontop minus 0.502, K2 instances minus 0.34 to minus 0.41, K5 minus 0.335). The theoretical composition predicts this: the Stage-1 term scales as L_n/n (slope minus 1/3 up to logs) and the Stage-2 term as b_n(N_n)/n (slope minus 1/2), so a mixture between the two is what should appear, and does.

At n = 50,000, unique_top: LB 0.03245, UB (I0) 0.03413, UB (I1) 0.03605 per round, against the revised top-agent constant 0.1283 per round. The certified interval is therefore about 3.8 times inside the revised constant and 7.7 times inside the previous one.

### Acceptance test (vii): one FAIL, reported rather than worked around

Eleven of the twelve instances pass: the per-round lower bound decreases in n over the n^(2/3) branch of L_n (n at least 2,000) and the certified upper bound stays below the revised constant. Below n = 2,000 the other branch of L_n = min(floor(n/2K), ceil(n^(2/3) (log en)^(1/3))) binds, bidding occupies half the horizon, and the per-round bound can rise with n (honest_top 0.0213 at n = 200 against 0.0867 at n = 2,000); this is a regime change in the mechanism's own constants, and I report monotonicity separately on each branch rather than excluding horizons after seeing them.

`low_gap_nontop` FAILS the comparison: UB (I1) reaches 0.403 per round at n = 20,000 against the revised constant 0.184. Diagnosis, and why this is not a theorem violation:

1. The focal agent there is the strategic runner-up with capacity 0.795 against V_i = 0.80, so delta_i = 0.005 and the agent is non-top. The certified upper bound uses the appendix's non-top fallback bound min{2H, 2 R_K(H)/delta_i}; with delta_i = 0.005 the second term is about 270,000 at H = 15,000, so the bound degenerates to 2H and the upper bound carries no information. Scout A2 predicted exactly this before the run.
2. The comparison itself is wrong for that instance: I compared against the top-agent constant, whereas Theorem thm:private-mesp gives non-top agents the additional O(log n / delta_i^2 + R_K(n)/delta_i) terms, and its stated condition for the non-top branch (which needs 4 s_n at most delta_i, that is 0.452 at most 0.005 at n = 20,000) fails at every horizon that fits in this project. No feasible experiment can exercise that branch of the proof.
3. The substantive quantity is unaffected: the certified lower bound for that instance is 0.0106 per round at n = 20,000 and 0.0067 at 50,000, decreasing with slope minus 0.502, and it is the smallest of all twelve instances.

Proposed resolution, for the main agent to approve rather than for me to apply silently: keep the instance, report only its lower bound, print the non-top constant where the focal agent is non-top, and state in the caption that for vanishing gaps the theorem's own finite-n condition is not met at any horizon we can run. I have not changed the acceptance criterion in the code; `aggregate.py` still prints FAIL for this cell.

### Implementation defect found and fixed

`dp.py` built its output path with `Path.with_suffix(".json")`, which truncates at the last dot. Eleven gap-grid aliases contain dots (`gap_K3_0.05` and similar), so all 33 gap-grid outputs collided onto two filenames and 31 were overwritten. The computations themselves ran correctly and their values are in the Slurm logs (for example `gap_K3_0.01` at n = 20,000: LB 419.8, UB (I0) 467.5, UB (I1) 543.8, Stage-2 gain 419.6 against b_n(N) 551.6), but rather than parse logs I fixed the path construction and re-ran the 33 cells as job 64555834. Lesson recorded: no output path is built from a name that is not known to be extension-free.

## E2 ladder pilot (12 variants, 12 behavior profiles, 3 instances, 2 horizons, 40 paired replicates)

Job 64554052, 3 minutes 32 seconds wall, 0.46 core-hours. All four acceptance tests pass.

(i) Exploitability under the focal bait-and-switch at n = 20,000 (paired gain per round; positive means the deviation pays): ESP-NoMon plus 0.4049 (unique_top) and plus 0.2059 (tied_top), that is of order tau as predicted, while every monitored variant is strongly negative (MESP minus 0.2799 and minus 0.0796; permanent exclusion minus 0.4216; UCB fallback minus 0.2743; round-robin fallback minus 0.3715). The best tested deviation over the six unilateral profiles gives the cleanest ladder result at n = 20,000 in unique_top: no monitor 0.4049, windowed monitor 0.1132, no-slack monitor 0.0123, anytime monitor 0.0123, where 0.0123 is exactly the Stage-1 term 0.15 L_n/n of the best hand-picked underbid. The monitor is what removes a linear exploit, and the anytime boundary is what makes the windowed variant's residual 0.11 disappear.

(ii) False-switch rate under the proposed profile: 0.000 for every variant at both horizons and all three instances, except the no-slack monitor, which fires on a compliant winner in 40 to 100 percent of replicates (0.975 and 1.000 in unique_top and tied_top at n = 2,000 and 20,000). The prediction that the raw price would produce false switches of order 0.25 in tied_top was wrong in its wording: with tau = beta_(2) the winner often cannot reach the price at all, so the monitor fires on a winner that is delivering its capacity. That is a true switch under the metric's definition (a false switch requires every primary target to be at least tau), and the right statement is that the uncorrected price makes the mechanism demand more than the winner can supply. I will report the switch rate alongside the false-switch rate for that variant.

(iii) Detection delay at n = 20,000 against log(2 n^4)/(2 (tau minus m)^2): bait-and-switch ratios 1.014 (unique_top) and 1.015 (tied_top); primary shading by 0.15 ratios 0.996 and 0.873. The windowed monitor detects at 2.9 to 4.6 times the anytime delay, as its detectability floor predicts. Within 25 percent for every anytime-monitor cell.

(iv) Honest benchmark under joint adversarial profiles at n = 20,000. Under sequential joint shading, the platform falls below mu_H^star per round for ESP-NoMon (by 0.190 in unique_top), the unmonitored runner-up (0.190) and the round-robin fallback (0.090), while MESP stays above it (minus 0.096, that is 0.096 per round of headroom), as do the UCB fallbacks and permanent exclusion. This is the separation the fallback is designed to produce, and it is the first measured evidence for the robustness half of Theorem thm:private-mesp, which no previous experiment tested.

One caveat that must be in the caption: in `honest_top` every variant, including MESP, sits 0.0287 per round below mu_H^star under joint adversarial play. That is not a violation. The honest agent is itself the top agent there (mu = M = 0.75), so the K L_n = 4,902 bidding rounds at n = 20,000 necessarily spend about a quarter of the horizon on agents delivering 0.70 and 0.45, which costs about 0.029 per round. The theorem allows a shortfall of order K L_n + n s_n, about 0.358 per round at this horizon, so the measured 0.0287 is inside its slack by a factor of twelve.

Revenue under the proposed profile at n = 20,000 (gap to M_(2) n per round): MESP 0.0856 in unique_top and 0.1174 in tied_top; the uncorrected price cuts this to 0.0009 and 0.0331, and the 1/n confidence exponent to 0.0455 and 0.0778. So the conservative correction costs 5 to 9 percent of the benchmark in revenue at this horizon and buys the false-switch rate of item (ii). That is the revenue-against-exploitability trade-off panel (b) needs, measured.

## E4 provider bank: verdict GO, with a criterion I had mis-stated and two scope limitations

The worker returned NO-GO on the acceptance as I wrote it and did not work around it, which was correct. I adjudicate as follows, having re-derived the arithmetic myself.

My criterion (d), "the mean price is within s_n of the measured second capacity", is equivalent to E[beta_(2)] at least M_(2), because MESP sets tau = (beta_(2) minus s_n)_+. With four near-tied bidders the second order statistic of the empirical bids sits below the second largest true capacity about half the time, so my criterion was a one-sided test of a quantity whose true value is essentially zero. It fails at n = 20,000 by 0.0049 (Fashion-MNIST) and 0.0002 (Covertype) in |mean tau minus M_(2)| against s_n = 0.1130, and passes at n = 2,000 and 8,000. The theory-aligned criterion is the one the proof actually states, equation private-price: on the good event (M_(2) minus 2 s_n)_+ at most tau at most M_(2). I verified every cell against that band: Fashion-MNIST mean tau 0.6035, 0.7080, 0.7359 inside [0.3440, 0.8538], [0.5568, 0.8538], [0.6279, 0.8538]; Covertype 0.6391, 0.7454, 0.7761 inside [0.3794, 0.8892], [0.5922, 0.8892], [0.6633, 0.8892]. The sharper empirical statement is that mean tau tracks M_(2) minus s_n to within 0.018 to 0.044 standard errors of the bidding radius at every horizon on both datasets. Verdict: GO on both datasets. I am recording the criterion change here, before the final run, because it was made after seeing the data: the original was a mis-statement of the mechanism's guarantee, not a threshold that the data missed.

Items (a) to (c) pass as stated: heterogeneity spread 0.0638 and 0.0750 (above 0.05); monotonicity violations 1 of 32 pooled per dataset, both explained (a two-voter tie-rule step, derived in closed form and matching the measurement to within a third of a standard error, and late-stage boosting overfit, so that provider's capacity is attained at knob 128); 0 switches in 160 replicates under the proposed profile.

Two scope limitations that must appear in the paper, not be hidden:

1. There is no clear-top-gap dataset. Both banks are near ties (top gaps 0.0332 and 0.0225 against 2 s_n = 0.2259 at n = 20,000); untampered providers of comparable quality differ by a few accuracy points, while the bidding radius is 0.11. Solving 2 s_n(n) below the gap needs n of order 10^7. The worker was right not to cripple a provider to manufacture a gap, since the design's whole point is heterogeneity through training data rather than tampering. The provider bank therefore exercises the near-tie regime only; the synthetic suites cover both regimes.
2. At the three gate horizons the announced price sits below the winner's intrinsic mean, so the mechanism asks this instance for no positive effort and the scripted knob-1 bait-and-switch is not a downward deviation at all. The worker added a supplementary n = 200,000 cell where it is: the monitor detects the drop in 17 of 20 and 20 of 20 replicates, and the median delay matches log(2 n^4)/(2 eps^2) at the real play-half shortfall within 5 percent (98,534 observed against 103,448 predicted), whereas the calibrated shortfall would have predicted 1,135,029. That is the strongest evidence in the pilot that the outcomes are real rather than Bernoulli by construction, and it is the cell the paper should show.

Memory note for the final run: the n = 200,000 cell peaked at 15.5 GB of a 16 GB request because the adapter pre-draws a tree-ordering row per fallback round per agent; the final run requests 32 GB or draws that tape in blocks.

## UCB index decision (main agent, 17 September 2026)

`ucb_bonus` now defaults to the known-horizon index sqrt(4 log n / T_a), with the anytime index retained for the comparison panel; the UCB fallback of the ablation variants uses the shared function, so the `esp_ucbfb` and `esp_ucbfb_warm` rows of the E2 pilot above were produced with the anytime index and will be regenerated with the horizon index in the final run. Nothing in the E1 exploitability program, MESP, or Grid-ETC is affected, and none of the numbers reported above other than those two rows changes. The contextual performance suite, E3c public-UCB exploitability, and the FATA and symmetric-initialization checks have not been run yet, so they will be run with the horizon index from the start, plus an anytime arm for the comparison panel that the paper's monotonicity remark needs.

## E1 (vii) after the approved resolution, and the gap grid

`aggregate.py` now derives the applicable constant from the instance table: the top-agent constant
L_n + 2 b_n(n) + R_K(n) for a top focal agent, and the explicit non-top constant otherwise (the primary-phase
bound 2 times 4 (1 + sqrt(2 log(2 n^4)))^2 / delta_i^2 plus the fallback bound 2 R_K(n) / delta_i plus L_n and
2 b_n(n) + R_K(n), up to the appendix's unquantified O(1)). It also reports whether the proof's non-top branch
condition 2 s_n <= delta_i / 2 holds. E1 (vii) now reads PASS for all 20 instances on its own terms.

The three instances with a non-top focal agent carry the annotation automatically: honest_top (delta_i = 0.050),
low_gap_nontop (0.005) and unique_top_focRunner (0.250) have an applicable constant above 2 per round, which is
the largest per-round utility physically attainable, and the branch condition is inactive at every horizon we
can run (8 of 8, 8 of 8, 3 of 3). For those three only the certified lower bound is reportable, exactly as
approved. The theory lead's independent figure, that delta_i = 0.005 needs n between 10^10 and 10^11, agrees
with the branch condition computed here.

Gap grid at n = 20,000 (certified lower bound per round, capacity gap M_top minus M_(2), all top focal agents):

| gap | K = 3 LB/round | K = 3 UB (I1)/round | K = 2 LB/round | K = 2 UB (I1)/round |
|--|--|--|--|--|
| 0.00 | +0.01407 | +0.02675 | n/a | n/a |
| 0.01 | +0.02099 | +0.02719 | +0.02209 | +0.02683 |
| 0.02 | +0.02540 | +0.03047 | +0.02674 | +0.03013 |
| 0.05 | +0.02870 | +0.03482 | +0.03014 | +0.03444 |
| 0.10 | +0.03256 | +0.03891 | +0.03399 | +0.03853 |
| 0.20 | +0.04045 | +0.04708 | +0.04188 | +0.04670 |

Reading, as a measured statement: in-class exploitability grows monotonically with the capacity gap, from
0.0141 per round at a tie to 0.0405 at a gap of 0.20 (K = 3), because a wider gap gives the top agent more room
to underbid while still winning. The theorem's top-agent constant does not depend on the gap, so the ratio
between the certified bound and the constant varies by a factor of about three across this grid. The tied
column (gap 0.00) is the smallest, which is the two-top condition doing its work in the private mechanism too.

Measured statement about the Stage-2 optimum, corrected. The optimal in-class Stage-2 deviation extracts the
entire monitoring slack on the histories where it wins the bidding: the Stage-2 gain equals b_n(N_n) times the
probability of winning Stage 1, to within 0.001 in 73 of 96 distinct cells, 0.005 in 84 and 0.01 in 88, with all eight
exceptions at n = 200 or n = 500 where the conservative price is degenerate (s_n of 0.40 to 0.59 and a mean price
given a win of 0.07 to 0.29). I had earlier written that the ratio to b_n(N_n) is exactly 1.000 whenever the
deviator always wins and exactly 0.500 in tied instances. That is false: over the always-winning cells the
ratio runs from 0.527 to 1.002, and over the tied cells from 0.260 to 0.501. The regularity above is both true
and stronger, since it covers every cell rather than two special cases, and it is the form the write-up should
use: the b_n term of the theorem is attained on the winning histories wherever the price is non-degenerate.

## E3c. Public UCB: in-class exploitability, FATA, and the index comparison

Job 64556295 (0.10 core-hours). Implementation `scratch/experiments/round2/public_ucb/run.py`: symmetric UCB with
uniform random initialization order and independent uniform tie-breaking, agents delivering fixed targets, and the
proof's coupling (agent a's r-th pull reads U[rep, a, r], so raising an agent's target raises only its own rewards).
200 replicates per cell, 41 fixed targets per sweep.

### The two-top condition, measured

| instance | n | index | best fixed target | gain per round | 95 percent interval | focal pull share |
|--|--|--|--|--|--|--|
| unique_top | 2,000 | horizon | 0.7425 | +0.07255 | [+0.07048, +0.07463] | 0.683 |
| unique_top | 8,000 | horizon | 0.7425 | +0.10209 | [+0.10091, +0.10327] | 0.812 |
| unique_top | 20,000 | horizon | 0.7200 | +0.12706 | [+0.12593, +0.12819] | 0.845 |
| unique_top | 2,000 | anytime | 0.7425 | +0.08888 | [+0.08630, +0.09146] | 0.760 |
| unique_top | 8,000 | anytime | 0.7200 | +0.12295 | [+0.12119, +0.12470] | 0.832 |
| unique_top | 20,000 | anytime | 0.7200 | +0.14535 | [+0.14427, +0.14644] | 0.900 |
| tied_top | 2,000 | horizon | 0.8000 | +0.00000 | [+0.00000, +0.00000] | 0.479 |
| tied_top | 8,000 | horizon | 0.8000 | +0.00000 | [+0.00000, +0.00000] | 0.488 |
| tied_top | 20,000 | horizon | 0.8000 | +0.00000 | [+0.00000, +0.00000] | 0.496 |
| tied_top | 2,000 to 20,000 | anytime | 0.8000 | +0.00000 | [+0.00000, +0.00000] | 0.491 to 0.498 |

With a unique top agent the best fixed target is 0.72 to 0.74, strictly between the runner-up capacity 0.65 and the
deviator's own capacity 0.90, and the per-round gain grows with the horizon (0.073, 0.102, 0.127), so the deviation
is linear in n: the agent shades, stays uniquely best, keeps 85 percent of the pulls and banks the effort. With two
tied top agents the best fixed target is the capacity itself and the gain is exactly zero at every horizon under
both indices. This is the first experiment for Theorem thm:public-ucb and for the appendix remark that the two-top
assumption cannot be dropped; the remark is not merely a proof convenience, it is the difference between a linear
exploit and none. The known-horizon index is also the less exploitable of the two, by 0.018 to 0.022 per round.

### Pathwise monotonicity, by index and tie rule (200,000 coupled paths per configuration block)

The monotonicity argument uses a tie rule fixed before play. Measuring both rules separates the index from the
coupling, and the separation matters:

| instance | n | index | ties = priority (the proof's rule) | ties = per-round coin |
|--|--|--|--|--|
| unique_top | 8 | horizon | 0 of 20,000 | 12 of 20,000 |
| unique_top | 8 | anytime | 10 of 20,000 | 21 of 20,000 |
| unique_top | 12 | anytime | 0 of 20,000 | 1 of 20,000 |
| unique_top | 50 | anytime | 1 of 20,000 | 4 of 20,000 |
| tied_top | 8 | horizon | 0 of 20,000 | 11 of 20,000 |
| tied_top | 8 | anytime | 45 of 20,000 | 50 of 20,000 |
| tied_top | 12 | anytime | 0 of 20,000 | 10 of 20,000 |
| tied_top | 50 | anytime | 2 of 20,000 | 1 of 20,000 |
| tied_top | 200 | anytime | 8 of 20,000 | 8 of 20,000 |
| both | 6, 12, 50, 200 | horizon | 0 of 20,000 at every size | 0 except n = 8 |

Under the proof's coupling the known-horizon index produced zero violations and the anytime index produced
violations at n = 8, 50 and 200 in both instances. The counts of record are the main agent's independent sweep of
both tie rules at 20,000 replicates per cell over six horizons and two instances, retained as
`public_ucb_monotonicity_bothties.csv`: fixed priority, known-horizon 0 of 240,000 and anytime 59; per-round coin,
known-horizon 36 and anytime 103. My own table in this section came from an interactive run that was never
retained, and the artifact I did retain recorded only the per-round default, so it did not support the sentence
that cited it. See the corrections section for the process fix. This corroborates the main agent's
counterexample in the scalar setting. It also yields a methodological caveat that belongs in the write-up: with a
fresh uniform tie coin each round the coupling is not monotone by construction, and then even the known-horizon
index shows rare violations (12 and 11 of 20,000 at n = 8), because the same coin selects a different agent when
the number of maximizers changes. Any monotonicity claim must name the tie rule.

### FATA

With two tied top agents delivering capacity, the mean difference in pull shares is within noise of zero at every
horizon and under both indices (for example at n = 20,000, horizon index, symmetric initialization: +0.00254 with
interval [-0.00984, +0.01492]), consistent with exact expected FATA. Symmetric and index-order initialization are
empirically indistinguishable at n at least 2,000, where initialization is three rounds of thousands and the shared
reward tape dominates: the two differ only in the fifth decimal. They separate at the small horizons where
initialization is a large share of the run: at n = 6 with the anytime index, index-order initialization gives
-0.00700 with interval [-0.01395, -0.00005], which excludes zero, while symmetric initialization gives -0.00571
with interval [-0.01269, +0.00127], which contains it. So the symmetric initialization earns its place in the
theorem statement, and the honest summary is that it matters for the exact claim and is immaterial for the plots.

## E3a with exact tiling (job 64556296)

| environment | focal | n | K q_n J_n / n | thin cells | exploration share | in class, full-profile maps | in class, own-context maps | outside the class |
|--|--|--|--|--|--|--|--|--|
| current | 0 | 2,000 | 1.25 | 64 | 0.992 | +0.23663 | +0.23663 | +0.0024 |
| current | 0 | 8,000 | 0.48 | 0 | 0.480 | +0.00401 | +0.00371 | +0.1745 |
| current | 0 | 32,000 | 0.65 | 0 | 0.648 | +0.07767 | +0.07767 | +0.1218 |
| current | 0 | 128,000 | 0.41 | 0 | 0.410 | +0.00000 | 0.00000 | +0.2087 |
| current | 0 | 2,000,000 | 0.25 | 0 | 0.252 | +0.00000 | +0.00000 | +0.2690 |
| separator | 0 | 8,000 | 0.48 | 0 | 0.480 | +0.03457 | +0.03457 | +0.1490 |
| separator | 0 | 128,000 | 0.41 | 0 | 0.410 | +0.00830 | +0.00200 | +0.1762 |
| separator | 0 | 2,000,000 | 0.25 | 0 | 0.252 | +0.00000 | +0.00000 | +0.2307 |
| separator | 2 | 8,000 | 0.48 | 0 | 0.480 | +0.05150 | +0.05150 | +0.0889 |
| separator | 2 | 32,000 | 0.65 | 0 | 0.648 | +0.11397 | +0.11397 | +0.0564 |
| separator | 2 | 128,000 | 0.41 | 0 | 0.410 | +0.03729 | +0.03729 | +0.0882 |
| separator | 2 | 512,000 | 0.34 | 0 | 0.342 | +0.02786 | +0.02782 | +0.0923 |
| separator | 2 | 2,000,000 | 0.25 | 0 | 0.252 | +0.01994 | +0.01976 | +0.0990 |

Exact tiling leaves no thin cells at any horizon, and in-class exploitability reaches exactly zero for a top
deviator in both environments by n = 128,000 to 512,000. The slowest-decaying in-class case is the mixed deviator
of the separator instance, agent 2, which is non-top below the separator and top above: 0.0199 per round at
n = 2,000,000. The residual bumps (0.004 at 8,000 against 0.078 at 32,000) are the integer jump in the number of
cells per axis, which makes the exploration share oscillate (0.48, 0.65, 0.41, 0.34, 0.25); that is intrinsic to
any integer cell count and is shown rather than smoothed.

One caveat for the current manuscript figure: at n = 2,000 with K = 3 and d = 1 the exploration budget
K q_n J_n is 1.25 times the horizon even under exact tiling, so Grid-ETC never commits in any cell and the in-class
gain is the whole exploration effort saving, 0.2366 per round. The paper's existing contextual incentive figure
lives at that horizon and at 8,000 and 32,000, so its smallest horizon is entirely pre-commitment. The revision
should either start the horizon axis at 8,000 or state this explicitly.

Out-of-scope count-based explore-then-shade grows to 0.23 to 0.27 per round as the exploitation share grows, while
the in-class values fall to zero. That contrast is the cleanest way to show what the fixed-map restriction buys.

## E2 final (job 64556141: 2,304 cells, 55 minutes wall, 14.4 core-hours)

12 mechanism variants, 12 behavior profiles, 4 instances, horizons 2,000 to 50,000, 200 paired replicates, the
known-horizon UCB index in the UCB-fallback variants. Every pilot conclusion holds at the larger scale.

### The ladder, at n = 20,000 (best tested deviation gain per round, over the six unilateral profiles)

| variant | honest_top | near_gap | tied_top | unique_top |
|--|--|--|--|--|
| no monitor | 0.0123 | 0.4887 | 0.2680 | 0.4061 |
| windowed monitor | 0.0123 | 0.1127 | 0.0589 | 0.1132 |
| MESP and every other monitored variant | 0.0123 | 0.0122 | 0.0063 | 0.0123 |
| no-slack monitor | 0.0000 | 0.0066 | 0.0099 | 0.0123 |

Removing the monitor is worth 0.268 to 0.489 per round in the three instances whose focal agent contests the
bidding, a linear exploit. Replacing the anytime boundary by a fixed window leaves 0.059 to 0.113 in those same
three instances, because a window has a detectability floor and slow shading passes under it. With the
anytime boundary every remaining variant sits at 0.006 to 0.012, which is exactly the Stage-1 term 0.15 L_n / n of
the best underbid: once the monitor is in place, the only deviation left is the one the theorem already charges for.
The fourth instance, honest_top, is excluded from those two ranges because its focal agent is the strategic
runner-up, which essentially never wins Stage 1 at this horizon, so no monitor is exercised and every variant,
including the unmonitored one, shows only the Stage-1 term 0.0123. The table above lists it, and any range quoted
in the paper must say which instances it covers.

### Revenue and its price, at n = 20,000 (gap to M_(2) n per round under the proposed profile)

| variant | honest_top | near_gap | tied_top | unique_top |
|--|--|--|--|--|
| MESP | -0.0213 | 0.1026 | 0.1179 | 0.0844 |
| price without the correction | -0.0213 | 0.0177 | 0.0333 | -0.0006 |
| correction at confidence 1/n | -0.0213 | 0.0628 | 0.0779 | 0.0446 |

The conservative correction costs 0.05 to 0.085 per round of revenue and buys the false-switch rate below. The
1/n confidence exponent recovers about half of that cost, which is the natural middle option if the revision wants
one.

### False switches and the honest benchmark

The false-switch rate is 0.0000 for every variant except the no-slack monitor at every horizon and instance. Its
rate depends on what the winner delivers, so it must be reported per profile and per cell rather than pooled.
Under the proposed profile, where a compliant winner delivers exactly the price and the monitored walk has zero
drift, the no-slack variant fires on that compliant winner in 0.39 to 1.00 of replicates across the sixteen cells
(1.00, 0.99, 0.99, 0.56 at n = 20,000); under all-maximum play, where the winner delivers above the price and the
walk has drift, in 0.13 to 0.63 (0.21, 0.63, 0.43, 0.56 at n = 20,000). An earlier draft of this report gave a
single figure of 87.5 percent for this variant. That number is the pooled mean of the per-cell rates over all
sixteen (instance, horizon) cells under the proposed profile, 0.8747; it is arithmetically correct but it is a
mean over heterogeneous cells presented as though it were a rate, and it was not labelled with its profile. The
per-profile ranges above replace it. Under
sequential joint shading at n = 20,000 the platform falls below mu_H^star for the round-robin fallback (by 0.070 to
0.156 per round), the unmonitored runner-up and the no-monitor variant (0.18 to 0.28), while MESP keeps 0.080 to
0.142 per round of headroom, as do the UCB fallbacks and permanent exclusion. In honest_top every variant sits
0.0287 per round below the benchmark, which is the bidding cost of that instance (the honest agent is itself the
top agent, so the K L_n bidding rounds necessarily spend a quarter of the horizon on weaker agents) and is inside
the theorem's allowance of about 0.358 per round by a factor of twelve.

### MESP's own decay

Best tested deviation per round against MESP: unique_top 0.0307, 0.0286, 0.0123, 0.0093 at n = 2,000, 8,000,
20,000, 50,000; tied_top 0.0184, 0.0164, 0.0063, 0.0043. These are hand-picked deviations, so they are lower
bounds; the certified interval for the same instances is in the E1 table and is three to four times larger.

## E1 search: a defect in my own parametrisation, found and fixed

The first CMA-ES run (job 64556162, cancelled after four tasks) returned negative gains for the bang-bang class,
far below the certified lower bound. The cause was mine: the Stage-2 threshold was parametrised on a unit scale
while the quantity it must match, the slack the monitor tolerates, is b_n(N_n), which is 126 utility units at
n = 2,000 and 552 at 20,000. The optimiser could not reach the right region. Rescaling each phase to its natural
units (Stage 1 to L_n M_i and sqrt(L_n), Stage 2 to b_n(N_n)) raises a hand-set policy from minus 16 to plus 148 at
n = 2,000 in unique_top, against the certified interval [181.9, 215.0]. The rescaled array is job 64557037.

A second structural point came out of the same exercise and is worth stating: I added a lower threshold to the
Stage-2 rule on the theory that the deviator should stop paying effort once a switch is unavoidable. It is inert,
and necessarily so: the monitor ends the primary phase the moment the cumulative slack goes negative, so no live
state exists in which a switch is already unavoidable. The interval structure I reported from the exact dynamic
program is therefore a Stage-1 phenomenon (stop bidding when the win is secured or hopeless), not a Stage-2 one.
The Stage-2 optimum is a single time-varying upper threshold on the slack. I have corrected that reading here
rather than leaving the earlier, looser sentence to stand.

## E4 final: the provider bank (jobs 64556231 and 64556232, 1.98 core-hours)

Evidence category: real labeled tasks and real provider answers; the effort choice is scripted. 20,800 trials:
4 mechanisms times 4 behaviors times {2,000, 8,000, 20,000} at 200 replicates on each of Fashion-MNIST (MIT) and
UCI Covertype (CC BY 4.0), plus a supplementary cell at n = 200,000. Licenses in `DATA_LICENSES.md`; data and the
per-dataset summaries in the scratchpad under `runs/final/provider_bank/`; the worker's own report is
`runs/final/FINAL_E4.md`.

Headline results. The announced price lies inside the proof's band [(M_(2) minus 2 s_n)_+, M_(2)] in 4,800 of 4,800
gate replicates, and the mean price tracks M_(2) minus s_n to within 0.002 to 0.023 s_n, which sharpens the pilot's
0.018 to 0.044 by an order of magnitude at 200 replicates. Zero switches and zero false switches in 4,800
proposed-profile replicates at the gate horizons. Full sabotage is detected in 3,318 of 3,318 focal wins across the
three monitored mechanisms, with median delay within 1.1 to 1.7 percent of log(2 n^4)/(2 eps^2) computed at the real
play-half shortfall. The unmonitored mechanism detects none of its 1,106.

The ablation separates the mechanisms on real outcomes exactly as the synthetic ladder does. At n = 20,000 full
sabotage costs the deviator 7,467 utility (Fashion-MNIST) and 7,683 (Covertype) under the monitored mechanism but
earns it 9,940 and 10,312 without the monitor, where platform reward per round collapses to 0.2765 and 0.2937,
below mu_H^star (0.7240 and 0.7599), while the monitored mechanism holds 0.8563 and 0.8833 above it. This is the
honest-benchmark separation of E2 (iv) reproduced on real provider answers. Permanent exclusion punishes the
deviator hardest (minus 14,107) and earns the platform least (0.759), because it cycles down to weaker providers
instead of restoring everyone. A measurement only a provider bank can give: under detected sabotage the platform's
real compute bill triples, from 73.9 to 226.8 trees per round, because the fallback puts every provider back at
capacity. That is a cost the model's effort convention does not express, and it belongs beside it in the paper.

The supplementary exhibit at n = 200,000 is the sharpest evidence that the outcomes are real rather than Bernoulli
by construction. The knob-1 bait is detected in 86 of 100 and 100 of 100 replicates, and the median detection delay
matches the first-order formula at the real play-half shortfall to ratios 0.962 and 0.996, while the same formula
evaluated at the calibrated shortfall gives 0.124 and 0.916. The Fashion-MNIST factor-of-eight miss is traced to its
5,000-task measurement half overstating that provider's knob-1 accuracy by 0.0108, two thirds of the shortfall the
monitor actually sees; Covertype's 50,000-task half transfers almost exactly. Realized outcome frequencies match the
play-half prediction to 1.2e-4 over 16.8 million real answers.

### My adjudication of the two items the worker raised

1. Three false switches in 100 replicates against a fully compliant winner, at n = 200,000 on Fashion-MNIST only
(Clopper-Pearson [0.006, 0.085]; zero of 100 on Covertype; none at any gate horizon). This is the real mechanism on
real provider answers, so the measured false-switch rate of the mechanism is not zero at every horizon, and that
sentence has to appear wherever the zero at the gate horizons appears. I accept the worker's diagnosis and its
framing. The winner's calibrated delivered mean equals tau to five decimals while its real
play-half mean is 0.0092 lower, giving a first-order crossing time of 295,818 against 167,664 primary rounds, and
the three crossings occurred at 151,480, 160,581 and 162,445. Lemma lem:private-monitor bounds false alarms for an
agent that truly delivers at least tau; an agent that intends to deliver tau but really delivers 0.0092 less is not
that agent, so nothing here contradicts the theorem. It is, however, a real and reportable limitation of any
calibrated bank: on real providers, compliance is only as accurate as the calibration, and a monitor tuned to a
finite measurement sample will eventually fire on a well-intentioned agent. It goes in the paper beside the
detection result, with the honest wording that the mechanism's guarantee is about delivered means and that
delivered means are themselves estimated. The remedy is a larger measurement half, not a change to the mechanism,
and I am not spending the remaining budget on it.
2. One cell where the t and BCa intervals disagree in sign (Covertype underbid at n = 200,000: t [-10,167, +750],
BCa [-14,310, -1,495]). No new decision is needed: the statistics protocol adopted from Scout A4 already says that
the t interval is primary, the BCa interval is the robustness column, and where the two disagree both are printed
and no sign is claimed. The skew is understood (the loss lands only in the 3 of 100 replicates where the underbid
loses the auction), so the cell is reported as inconclusive in sign with both intervals shown.

I also record the worker's own process note, because it is the right practice: it drafted tables from a partial
results file while the jobs ran, then regenerated every table from the jobs' own summaries and diffed cell by cell,
finding and correcting two rows. Everything published comes from complete 200-trial cells.

Two scope limitations stand, unchanged and in the paper: both provider banks are near ties (top gaps 0.033 and
0.023 against 2 s_n = 0.226; a clear gap would need n of order 10^7), and at the gate horizons the announced price
sits below the winner's intrinsic mean, so the effort-positive regime appears only in the supplementary cell.

## E1 search: results from the rescaled class (job 64557037)

Six of the eight cells are in; the two bang-bang cells at n = 20,000 (array tasks 4 and 6) were still running at the
time of writing and are reported as outstanding rather than estimated. One result from the superseded 8-parameter
class survived in the output directory and was quarantined to `runs/final/search/superseded/`, identified by its
parameter count rather than by file time, so no mis-scaled value can enter a table.

| instance | n | class | held-out gain | per round | certified LB | certified UB (I0) | held-out / LB | at or below UB |
|--|--|--|--|--|--|--|--|--|
| unique_top | 2,000 | bang-bang (9) | 175.7 | +0.08783 | 181.9 | 215.0 | 0.966 | yes |
| unique_top | 2,000 | continuous (3) | 141.8 | +0.07088 | 181.9 | 215.0 | 0.779 | yes |
| unique_top | 20,000 | continuous (3) | 642.6 | +0.03213 | 893.1 | 957.2 | 0.719 | yes |
| tied_top | 2,000 | bang-bang (9) | 64.2 | +0.03212 | 69.4 | 84.6 | 0.926 | yes |
| tied_top | 2,000 | continuous (3) | 17.6 | +0.00882 | 69.4 | 84.6 | 0.254 | yes |
| tied_top | 20,000 | continuous (3) | 208.1 | +0.01040 | 281.5 | 312.1 | 0.739 | yes |

Acceptance (v), that interior-target policies do not beat the two-action dynamic program: confirmed in all four
continuous cells, where the searched value reaches 0.25 to 0.78 of the certified lower bound and never approaches,
let alone exceeds, the upper bound. This is the empirical form of the affinity argument.

Acceptance (vi), that a CMA-ES restart at n = 2,000 on the unique-top instance lands between 0.9 times the certified
lower bound (164) and the certified upper bound (215): the searched value is 175.7, so the test passes. The
tied-top cell at the same horizon reaches 0.926 of its lower bound without being part of the stated test.

No searched policy in any completed cell exceeded the certified upper bound, which is the check that would have
indicated an error in the dynamic program or in the bound. The remaining gap between the searched and certified
values is expected: the searched class is a fixed-shape threshold rule, while the exact optimum has a
time-varying threshold, so the search is a lower bound on the exploitability of a subclass, which is what it is
labelled as everywhere.

## Corrections after the main agent's independent re-derivation (18 September 2026)

Four defects in my reporting were found by the main agent re-deriving the numbers from my raw outputs rather than
accepting them. All four are corrected above, in place, with the superseded version recorded beside each.

1. The Stage-2 identity was overstated as two exact constants. The regularity that survives all cells is that the
Stage-2 gain equals b_n(N_n) times the probability of winning Stage 1.
2. The ladder ranges for the no-monitor and windowed variants silently excluded the one instance whose focal agent
does not contest the bidding. They now name the instances they cover.
3. The exploitability grid was reported as 98 cells. It is 98 result files covering 96 distinct cells: two files
written before I fixed the output-filename collision kept truncated names (`dp_gap_K2_0.json` and
`dp_gap_K3_0.json`) and were re-read by the aggregator alongside the correctly named re-runs of the same two cells,
`gap_K2_0.20` and `gap_K3_0.00` at n = 20,000. The main agent's column-by-column comparison, which I reproduced,
shows the duplicated rows agree in every field except wall time, so the computation is deterministic and no value
is affected; the count and its three tallies were wrong, and the correct ones are 73, 84 and 88 of 96. The two
stale files are now in `runs/final/exploitability/superseded/`, so the artifact directory matches the task list and
the aggregator returns 96 cells. This is the second defect traceable to that filename collision, which argues for
the rule I adopted after the first: never build an output path from a name not known to be extension-free, and
assert that the number of result files equals the number of tasks.
4. The no-slack monitor's false-switch rate was given as a single figure of 87.5 percent. That is the pooled mean
of the per-cell rates over all sixteen cells under the proposed profile (0.8747), which is a mean over
heterogeneous cells presented as a rate and was not labelled with its profile. Per-profile, per-cell ranges replace
it.

A note on item 4 for the paper, since the choice of profile changes the number by a factor of two. The profile I
used is the one the manuscript proposes: `sections/Private_information_setting.tex` states that in the proposed
profile a strategic primary winner delivers min{tau, M_i} and an honest winner max{mu_i, min{tau, M_i}}, so a
compliant winner with capacity above the price delivers exactly the price. That is why the no-slack variant fires
so often under it: the monitored walk has zero drift, and a test with no slack convicts a compliant winner by
ordinary noise alone. Under all-maximum play the winner delivers strictly above the price, the walk has positive
drift, and the rate falls to 0.13 to 0.63. Both are worth reporting and the supplement now carries both, but the
zero-drift case is the one that demonstrates why the boundary b_n(r) is in the mechanism at all, so I would not
describe the proposed profile as the wrong comparison for this ablation.

## Further corrections after the main agent's second pass (18 September 2026)

Five more defects, all found by checking my numbers against the retained summaries rather than against my report.
Items 1 to 4 are corrected in place above and in the final report.

5. A certified lower bound was rounded inward. I quoted the interval at n = 50,000 in unique_top as
[0.0325, 0.0361] when the lower bound is 0.032448, so the quoted interval did not contain the interval it
certifies. A certified interval is rounded outward. Now [0.0324, 0.0361].
6. The best fixed target against symmetric UCB was quoted as 0.72. It is 0.7425 at n = 2,000 and 8,000 and 0.72 at
20,000; the gains were right. Now quoted as a range.
7. The monotonicity sentence cited an artifact that contradicted it. `monotonicity()` takes `ties="perround"` by
default and the call site never passed the argument, so the retained `public_ucb_monotonicity.csv` is the per-round
coin, in which the known-horizon index does violate (15 and 19 of 20,000 at n = 8, 2 at n = 50). My fixed-priority
numbers came from an interactive session that produced no artifact. The substance survives the main agent's
independent sweep of both rules at 240,000 paths, but the evidence did not exist in the repository. Fixed three
ways: `ties` and `init` are now recorded in every row, the sweep runs both rules by default through a `--mono-ties`
option, and two tests pin the behavior, one asserting the row records its tie rule and one asserting zero
violations under the proof's coupling at the size where the anytime index fails. The rule I take from this is that
a number quoted in a report must come from a retained artifact, and an interactive run is not one.
8. The price-in-band claim was stated as a count of 4,800 replicates. The four mechanism variants share one bidding
stage, so that count depends on whether they are counted separately; there are 1,200 distinct prices. The rate is
1.000 in every cell and the reports now state the rate. The 4,800 figure is correct for the proposed-profile
false-switch claim and is kept there.
9. The largest-horizon false switches were missing from the final report. Section 2.4 and supported claim 5 gave the
zero rate at the gate horizons without the 3 of 100 at n = 200,000, so a reader of that document alone would not
have learned that the mechanism's measured false-switch rate is nonzero at the largest horizon tested. Both now
carry it, with the measured drift of 0.0092 and its crossing time.

On the characterization of that last item I record one disagreement, since the main agent asked for evidence rather
than assent. My section 2.4 did not say that a calibrated Bernoulli simulator produced the three false switches; it
did not mention them at all, which was the defect. Its sentence about the delay read "the detection delay matches
the formula at the real shortfall but not at the calibrated shortfall, which is the sharpest demonstration that the
outcomes are real and not Bernoulli by construction", describing the outcomes rather than asserting a simulator.
That phrasing was nonetheless loose enough to be read as the main agent read it, and the two ratio columns are now
named for what they are: one formula evaluated at the realized play-half rate and at the rate fitted on the
measurement half, on the partial-shading rows. The correction stands; only the description of what my text said is
adjusted.
