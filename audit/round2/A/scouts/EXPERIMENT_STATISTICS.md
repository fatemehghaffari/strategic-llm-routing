# SCOUT A4: statistics and reproducibility design for the round-2 experiments

Written 17 September 2026 for Agent A (experiments lead). Read-only scout; nothing under `scratch/experiments/final/` or `sections/` was modified. Paths below use `<repo>` for the repository root and `<scratchpad>` for the session scratch directory named in COMMON.md; the scout's own working files are under `<scratchpad>/round2/A/scouts/A4/` (`power.py`, `power_output.txt`, `tape.py`, `tape_output.txt`, `delay.py`, `delay_output.txt`, `design_table.py`, `design_table.txt`).

What I read in full: `audit/round2/BASELINE.md`; `scratch/experiments/final/README.md`; the four suites (`README.md`, `run.py`, `plot.py`), `contextual_incentives/validate.py`, `make_composites.py`; headers and first rows of every `trials.csv`, `summary.csv`, `paired_summary.csv`, `paired_comparisons.csv`; the five test files in `scratch/tests/`; `sections/experiments.tex`, `sections/appendix_experiments.tex`, `sections/Private_information_setting.tex`, `sections/contextual_samf_algorithm.tex`; and the monitor lemma and the deviation-class passages of `sections/appendix_private.tex` (lines 10 to 30 in full, the rest by grep). What I computed: standard deviations and power from the committed trials CSVs with pandas; a 240-replicate simulation comparing the current stream coupling with a uniform-tape coupling; the empirical monitor crossing times against the closed-form prediction; the design constants on the proposed horizon grid; Slurm accounting for the baseline reproduction job. I also created and then removed a `__pycache__` directory that my import of `scalar_incentives/run.py` wrote under the canonical suite (untracked; the tree is clean again); any future import of those modules must run with `PYTHONDONTWRITEBYTECODE=1`.

## 1. Summary

1. The current suites are statistically sound in their point estimates but weak in three places: the pairing is only partly real (stream coupling, not tape coupling; the lead verified that for `underbid_05` in `unique_top` the deviation run's price `tau` equals the profile run's `tau` in only 74, 91, and 92 percent of "paired" rows at n = 2,000, 8,000, 20,000), every interval is a percentile bootstrap whose resampling indices come from a NumPy `Generator` method with no cross-version stream guarantee (the committed `scalar_performance/paired_comparisons.csv` is already irreproducible under the venv for that reason), and binary metrics get degenerate bootstrap intervals (`fallback` rows with mean 0 and interval [0, 0]).
2. Power, computed from the committed trials: paired utility differences per round have two regimes. In cells where the deviation does not change the Stage-1 winner (for example `unique_top`), the standard deviation is 0.003 to 0.05 per round and 120 to 240 replicates detect 0.002 to 0.01 per round with 80 percent power at every horizon; a tape coupling makes the Stage-1 effort-saving component exactly deterministic there (simulated SD 0.000 versus 0.006 to 0.009 now). In cells where the deviation flips the winner with probability near one half (`tied_top`, `low_gap_nontop`, `near_gap` with `underbid_05`), the SD is 0.10 to 0.19 per round, 0.002 per round would need 20,000 to 70,000 pairs, and the right design is a stratified report (flip probability with a Wilson interval, conditional gains) rather than more replicates. Reward-per-round contrasts between mechanisms have paired SD 0.007 to 0.013 at n at least 8,000 (0.018 to 0.035 at n = 2,000), so 120 pairs detect about 0.003 per round at n at least 8,000 and about 0.008 at n = 2,000; 0.002 per round at n at least 8,000 needs 110 to 370 pairs, which the budget allows.
3. The theorem's false-switch bound is `(2 n^3)^{-1}` (one-sided, Lemma "Anytime primary monitor", `appendix_private.tex` lines 12 to 25; arithmetic verified). No experiment can certify it; 0 switches in R profile runs gives only the Clopper-Pearson upper bound `1 - 0.025^{1/R}`, about `3/R` (0.025 at R = 120). The detection delay under constant underperformance `m < tau` is `r* = log(2 n^4) / (2 (tau - m)^2)`; the algebra in the brief is correct and the committed data match it to within 4 percent whenever `r*` is well inside `N_n` (observed/predicted ratios 0.96 to 1.02; ratios of 0.63 appear only where censoring at `N_n` truncates the crossing).
4. Proposed grids: horizons {200, 500, 1000, 2000, 5000, 8000, 20000, 50000}; a parameterized instance family over K in {2, 3, 5}, capacity gap in {0, 0.01, 0.02, 0.05, 0.10, 0.20}, two honesty patterns, two intrinsic-mean levels, with instances named by their parameters; the gap grid at K = 3 and K = 2 over all eight horizons. Total cost of everything this document covers (regeneration of the four suites with tape coupling, gap grid, ablation and baseline suite, monitor-only Monte Carlo, serial runtime benchmark) is about 25 core-hours by measured per-round costs; with a factor-five margin for reruns it stays under 150 core-hours, far below half of the 2,000 core-hour budget. The exploitability search and the non-synthetic study are budgeted separately (Section 5.5).
5. Seeds: extend the existing `SeedSequence([master, instance_index, n, rep])` to `SeedSequence([master, suite_id, phase_id, instance_index, n, rep])` with `phase_id` in {0 pilot, 1 final, 2 train, 3 held-out eval} and per-trial `spawn(4)` children for the Stage-1 tape, the primary tape, the fallback tape, and the mechanism's own randomness. Pilot and final seeds are then disjoint by construction, which the current code does not provide (`--quick` reuses the final seeds).
6. Multiple comparisons: each figure gets one pre-registered primary contrast family (the numbers quoted in the text), reported with Holm-adjusted p-values or Bonferroni simultaneous intervals inside that family; everything else is exploratory with unadjusted 95 percent intervals and is labeled as such. With 372 intervals in `paired_summary.csv` alone, unadjusted reporting of "significant" cells would be indefensible, but the paper's claims are directional statements about a handful of quoted numbers, which is the right family to protect.
7. Twenty-three defects are listed in Section 10 with severities; the ones the lead should act on first are the false nonnegative-effort assertion (P1 for the new exploitability suite, where it would crash or silently truncate the deviation class), the duplicated `nontop_win_underperform` rows that the appendix describes as a distinct tested deviation (P1 as a statement about what was tested), the version-fragile bootstrap (P2), and the unsupported wall-clock and host claims (P2).

## 2. Metric definitions

Notation follows `sections/setting.tex` and `sections/Private_information_setting.tex`: K agents, horizon n, intrinsic means `mu_i`, capacities `M_i`, honest set H, `M_top = max_i M_i`, `M_(2)` the second order statistic with multiplicity, `mu_H^star = max_{h in H} mu_h`, `T_i` the number of pulls of agent i, `C_i = sum over its pulls of (m_t - mu_i)` its cumulative effort, `Y_t` the Bernoulli outcome. All per-round quantities divide by n. Each metric names the current CSV column that carries it, or "new" if none does.

| Metric | Operational definition | Current column | Theory anchor |
|--|--|--|--|
| Platform reward `P` | `sum_t Y_t` (realized Bernoulli outcomes, integer) | `platform_reward` (scalar_incentives), `reward` (scalar_performance) | Theorem private-mesp revenue bounds |
| Expected reward `P_bar` | `sum_t m_t` (conditional means; used only where the algorithm still learns from `Y_t`) | `expected_reward` (contextual_performance) | none; a variance-reduced estimator of `E P`; must be labeled as such wherever shown |
| Private-revenue gap | `M_(2) n - P` and per round `M_(2) - P/n` | `second_price_shortfall(_per_round)` | `P(n; S^star) >= M_(2) n - O(n^{2/3} (log n)^{1/3})` |
| Honest-benchmark gap | `mu_H^star n - P` | new (`honest_shortfall` exists only in contextual_performance and is defined against `max_i mu_i`, not against the honest set; see defect 13) | `P(n; S) >= mu_H^star n - O(...)` for every behavioral profile |
| Capacity-oracle gap | scalar: `M_top n - P`; contextual: `sum_t M_star(X_t) - P_bar` | `capacity_shortfall(_per_round)`, `oracle_regret` | Theorem contextual-public and grid-ucb-robust |
| Arm utility `U_i` | `T_i - C_i = sum over pulls of i of (1 + mu_i - m_t)` | `focal_utility` (focal only); `baseline_utility`, `deviation_utility` | `u_i(n; S)` in the equilibrium definition |
| Paired deviation gain | `U_i(S'_i, S^star_{-i}) - U_i(S^star)` on the same coupled path, and per round | `paired_summary.csv` metric `focal_utility`; `utility_gain`, `gain_per_round` | left side of the theorem's sup |
| Exploitability, exact | `max over the DP-feasible class of E[U_i(S'_i) - U_i(S^star)]` computed by dynamic programming (no sampling error; state the class and horizon) | new: `exploit_dp`, `exploit_dp_per_round`, flag `exact = 1` | the sup itself restricted to the DP class |
| Exploitability, searched | the paired gain of the best deviation found on training seeds, re-estimated on held-out evaluation seeds with an interval; a lower bound on the class exploitability, never a certificate | new: `exploit_search`, `exploit_search_lo`, `exploit_search_hi`, `search_class`, `train_phase`, `eval_phase` | lower bound on the sup over the tested class (COMMON rule 5) |
| Switch indicator | 1 if the monitor fired in the primary phase | `fallback` | Stage 3 trigger |
| False switch | 1 if the monitor fired AND every primary target satisfied `m_r >= tau` (under `S^star` a strategic winner delivers `min(tau, M_W) = tau` when `M_W >= tau`; an honest winner `max(mu_W, min(tau, M_W)) >= tau` when `M_W >= tau`; so the event is `switched and M_W >= tau` under the profile, and `switched and min_r m_r >= tau` in general) | new: `false_switch` | Lemma anytime-primary-monitor: `Pr(false switch) <= (2 n^3)^{-1}`; two-sided deviation `Pr(exists r <= n: abs(Z_r - A_r) > b_n(r)) <= n^{-3}`; each fixed-r tail is `exp(-2 b_n(r)^2 / r) = (2 n^4)^{-1}`, union over r <= n gives `(2 n^3)^{-1}` per side |
| Detection delay `d` | number of primary pulls `q` at which the switch occurred, defined only on switch paths; report with the censoring value `N_n` and the fraction not detected by `N_n` | `primary_rounds` when `fallback = 1` | predicted crossing time under constant `m < tau`: `Z_r ~ r m`, switch when `r (tau - m) > sqrt(r c)`, `c = log(2 n^4)/2`, so `r* = c / (tau - m)^2 = log(2 n^4) / (2 (tau - m)^2)`; verified on data, Section 2.1 |
| Fallback length `H` | `N_n - q` on switch paths, else 0 | `fallback_rounds` | Stage 3 length |
| Allocation shares | `T_i / n` for every i | `pull_share_i` (scalar_performance only) | FATA and monotonicity diagnostics |
| Focal-win indicator | 1 if the focal agent is the Stage-1 winner | `focal_won`, `winner` | coupling argument in the proof (maximum bidding wins whenever the deviation wins) |
| Price | `tau = (beta_(2) - s_n)_+` | `tau` | `(M_(2) - 2 s_n)_+ <= tau <= M_(2)` on the good event |
| Runtime | wall time of one trial in seconds, `time.perf_counter_ns`, single process, `--workers 1`, `OMP_NUM_THREADS=1`, pinned node feature, recorded node model; valid only when `runtime_valid = 1` | `runtime_seconds`, `runtime_s` (currently measured under parallel workers or on an unrecorded host) | none |

### 2.1 Checks behind the definitions

False-switch bound. From `appendix_private.tex` lines 12 to 25 (quoted): "Pr{exists r <= n : |Z_r - A_r| > b_n(r)} <= n^{-3}" and "If every primary target is at least tau, the probability of any false switch is at most (2 n^3)^{-1}." With `b_n(r) = sqrt(r log(2 n^4) / 2)`, `exp(-2 b_n(r)^2 / r) = exp(-log(2 n^4)) = (2 n^4)^{-1}`; n values of r give `(2 n^3)^{-1}` for one tail and `n^{-3}` for both. The union is over r <= n although the primary phase has at most `N_n < n` pulls, so the bound is conservative by the factor `n / N_n`. Numerically the bound is 6.3e-11 at n = 2,000 and 4.0e-15 at n = 50,000, seven to twelve orders of magnitude below what any replicate count can resolve. The experiment therefore reports "0 false switches in R runs, Clopper-Pearson 95 percent upper bound `1 - 0.025^{1/R}`" (0.0303 at R = 120, 0.0153 at R = 240, 0.0030 at R = 1,000) and a monitor-only Monte Carlo (Section 5.4) that resolves 1e-5. In the committed data the switch count under the profile is 0 in all 1,740 profile rows of scalar_incentives and all 1,440 `mespf` rows of scalar_performance.

Detection delay. `delay.py` computed, for every switch path with the focal agent as winner, the ratio of the observed `primary_rounds` to `c / (tau - m)^2` with the row's own `tau`. Results (`delay_output.txt`): bait-and-switch (`m = 0`) ratios 1.005 to 1.012 at every instance and horizon (predicted 44 to 84 rounds, observed means within one round); `primary_shade_15` ratios 0.92 to 1.01 (predicted 691 to 896 rounds); `primary_shade_05` at n = 20,000 ratios 0.99 to 1.02 (predicted 8,061 rounds against `N_n = 15,098`); at n = 8,000 the prediction 7,328 exceeds `N_n = 5,414`, only 14 to 19 of about 120 paths switched, and the conditional ratio drops to 0.63 to 0.68, which is censoring, not a formula error. The slight downward bias at ratios 0.92 to 0.98 is the expected overshoot-free first-passage effect of a random walk against a concave boundary; the formula is a first-order approximation, and the report should present it as such and print empirical medians with the censoring fraction.

Winner flips and the pairing claim. `tape.py` reran 240 fresh seeds per cell with (a) the committed `trial()` and (b) an otherwise identical trial whose Stage-1 successes are `sum_r 1{U[i, r] < m_i}` on a `(K, L_n)` uniform tape drawn before the targets are applied. Winner flips between profile and `underbid_05` occur in 103 to 160 of 240 pairs in `tied_top`, `near_gap`, and `low_gap_nontop` under both couplings, so those flips are genuine (the deviation really changes who wins), and the tape does not remove that variance (SD 0.135 versus 0.136 in `tied_top` at n = 2,000). In `unique_top`, where the winner never flips, the tape makes the paired difference exactly `0.05 L_n / n` with SD 0.000 versus 0.006 to 0.009 under the current stream coupling. The lead's independent count (price equality in 74, 91, 92 percent of pairs) measures the same desynchronization from the other side.

## 3. Paired design and interval method

### 3.1 What is and is not coupled today

Scalar suites. One `default_rng(seed)` per trial. Draw order in `scalar_incentives.trial`: priority permutation, then `rng.binomial(ell, bid_m)` over the whole vector, then a fixed-length primary tape `rng.random(primary_budget)`, then EXP3 draws. The permutation is coupled across behaviors. The binomial draws are coupled only while every parameter is identical: a changed focal target changes the number of underlying draws the rejection sampler consumes, so every later draw (the other agents' bids, the primary tape, the fallback coins) is desynchronized for `underbid_*`, while `primary_shade_*`, `bait_switch`, and `trigger_fallback_shade` keep Stage 1 and the primary tape identical and desynchronize only the fallback. `scalar_performance.mespf` uses a per-round Python loop with `rng.random()` for the primary phase and `rng.choice` inside EXP3, so its paths differ from `scalar_incentives.trial` even for the same seed and instance; and baselines consume the stream in unrelated ways, so pairing across methods in scalar_performance shares only the seed (within-replicate correlations of reward per round between `mespf` and the baselines are between -0.19 and 0.64, mostly 0.0 to 0.3; `power_output.txt`).

Contextual suites. Contexts and a `(n, K)` reward-uniform tape are pre-drawn, so all methods (and in contextual_incentives the baseline and the deviation) are coupled by (round, arm), which is the proof's coupling. Grid-ETC's exploration permutations come from a separate per-replicate seed (`777000 + rep`) in contextual_incentives and from the shared generator in contextual_performance (harmless there because no other method draws).

### 3.2 Recommended coupling (tape by pull index)

Per trial, split the trial seed into four child streams with `SeedSequence.spawn(4)`:

1. Stage-1 tape `U_bid[i, r]`, shape `(K, L_n)`: agent i's r-th bidding outcome is `1{U_bid[i, r] < m_{i,r}}`.
2. Primary tape `U_pri[r]`, shape `(N_n,)`: the winner's r-th primary outcome is `1{U_pri[r] < m_r}`.
3. Fallback tape `U_fb[t, i]`, shape `(N_n, K)`: the outcome of agent i if pulled in fallback round t (memory 50,000 x 5 doubles at the largest horizon and K, about 2 MB; fine).
4. Mechanism stream: tie-break priority, EXP3 arm draws by `searchsorted(cumsum(p), U)` on its own uniforms, nothing else.

A randomized deviation gets a fifth child. This is exactly the monotone coupling used in the proof ("Coupling Stage-1 reward uniforms shows that maximum delivery pathwise maximizes an agent's bid and winning event", `Private_information_setting.tex` line 57): under it a lower target can only lower the agent's own bid, other agents' bids are unchanged, and the winner flip is one-directional (deviation loses on a superset of the histories where the profile loses). Consequences for variance: the Stage-1 effort-saving component of an underbid becomes deterministic, `primary_shade` differences are unchanged (already tape-coupled), and the fallback comparison becomes a by-(round, arm) coupling instead of an independent replay. Nothing in the estimand changes; only the variance and the truth of the sentence "paired" do. The estimator of the mean gain remains unbiased under either coupling (Glasserman and Yao 1992 give the monotonicity conditions under which common random numbers reduce variance; the tape by pull index satisfies them for Bernoulli outcomes monotone in the target).

Implement the mechanism once (one module imported by every suite) so that the profile row of the incentives suite and the MESP row of the performance suite are the same function and the same path for the same seed.

### 3.3 Estimator and intervals

Primary estimator: the mean of per-replicate paired differences `D_j = metric(deviation or method B, seed_j) - metric(profile or method A, seed_j)`, divided by n for per-round quantities. Report `mean(D)`, its standard error `sd(D)/sqrt(R)`, and a 95 percent interval.

Interval method. For R between 100 and 240 and a mean estimand, the Student t-interval `mean +- t_{0.975, R-1} sd/sqrt(R)` is first-order correct, deterministic (no bootstrap seed, no NumPy-version dependence), and, in the no-flip cells where `D` is close to normal, indistinguishable from any bootstrap. In the flip cells `D` is a two-point mixture; the mean's sampling distribution is still close to normal at R at least 120 (the mixture proportion is near one half, so skewness is small), and the t-interval remains adequate. The percentile bootstrap is only first-order correct and can be worse than the t-interval for skewed statistics (Hall 1988; DiCiccio and Efron 1996); with B = 4,000 its Monte Carlo error on an endpoint is a few percent of the half-width, which is acceptable, so the existing intervals are not wrong, only fragile and no better than the t-interval. BCa (Efron 1987) is second-order correct for smooth functionals and is the appropriate bootstrap if one is reported.

Recommendation: report the t-interval as the primary interval for every mean of paired differences and every mean of per-round rewards; report a BCa interval from `scipy.stats.bootstrap(data=(dev, base), statistic=mean difference, paired=True, method="BCa", n_resamples=9999, rng=<child SeedSequence>)` as a robustness column in the summary CSVs; state in the appendix that the two agree to the printed precision (or print both where they do not). For proportions (false switch, focal win, switch, allocation accuracy as a fraction of rounds is not a proportion of independent trials and stays under the t-interval) use the Clopper-Pearson interval (exact, conservative) and print the rule-of-three upper bound when the count is zero; Brown, Cai, and DasGupta (2001) document why the Wald interval and, equivalently, the bootstrap of a proportion fail at counts near zero, which is precisely the degenerate `[0, 0]` intervals in the committed `paired_summary.csv`. For paired differences of proportions (switch probability under deviation minus under profile) use the t-interval on the paired indicator differences, or McNemar-type exact intervals if counts are tiny.

Bootstrap seeding. Never share one generator across cells in loop order (defect 9). Derive one child per (cell, metric): `SeedSequence([master, suite_id, 9, cell_index, metric_index])`, where 9 is the reserved analysis phase id; store `cell_index` and `metric_index` in the summary row so any cell's interval can be recomputed alone.

### 3.4 Stratified reporting in flip cells

In cells where the deviation changes the Stage-1 winner with non-negligible probability, report three numbers with intervals: `p_flip` (Clopper-Pearson), `E[D | no flip]`, and `E[D | flip]` (t-intervals on the strata). The overall mean is `(1 - p_flip) E[D | no flip] + p_flip E[D | flip]` and can be checked against the direct estimate. Under the tape coupling `E[D | no flip]` for an underbid equals `delta L_n / n` minus the primary-phase difference, which the reader can verify from `L_n`. This is where the current data are least informative: `low_gap_nontop` and `tied_top` cells have SE 0.007 to 0.012 per round on effects of -0.10 to -0.16 per round; the decomposition explains the size instead of hiding it in a wide band.

## 4. Replication and power

### 4.1 Method

From the committed `trials.csv` files (identical to the regenerated ones except the two NumPy-sensitive rows recorded in BASELINE.md), `power.py` computed the paired differences per replicate, their standard deviation `sd` (ddof 1), and the number of pairs needed for a two-sided 5 percent paired t-test with 80 percent power against per-round effects 0.002, 0.005, 0.010: `R = (t_{0.975, R-1} + t_{0.80, R-1})^2 sd^2 / delta^2`, iterated to a fixed point (normal approximation `7.85 sd^2 / delta^2` plus the small-sample correction). Commands run on the login node (seconds):

```
<venv>/bin/python <scratchpad>/round2/A/scouts/A4/power.py   > power_output.txt
<venv>/bin/python <scratchpad>/round2/A/scouts/A4/tape.py    > tape_output.txt     (about 3 minutes, 240 pairs x 16 cells x 2 couplings)
<venv>/bin/python <scratchpad>/round2/A/scouts/A4/delay.py   > delay_output.txt
<venv>/bin/python <scratchpad>/round2/A/scouts/A4/design_table.py > design_table.txt
```

### 4.2 Paired utility gain per round (scalar_incentives, deviation minus profile)

Selected cells (full table of all 90 cells in `power_output.txt`):

| instance | n | behavior | R | mean/round | sd/round | R for 0.002 | R for 0.005 | R for 0.010 |
|--|--|--|--|--|--|--|--|--|
| unique_top | 2000 | underbid_05 | 120 | +0.00943 | 0.01205 | 287 | 48 | 14 |
| unique_top | 8000 | underbid_05 | 120 | +0.00490 | 0.00529 | 57 | 11 | 3 |
| unique_top | 20000 | underbid_05 | 120 | +0.00435 | 0.00283 | 18 | 4 | 3 |
| unique_top | 20000 | underbid_15 | 120 | +0.01270 | 0.00382 | 31 | 7 | 3 |
| unique_top | 8000 | primary_shade_05 | 120 | +0.02672 | 0.02352 | 1088 | 176 | 46 |
| unique_top | 20000 | primary_shade_05 | 120 | -0.11404 | 0.03822 | 2868 | 461 | 117 |
| unique_top | 20000 | bait_switch | 120 | -0.27983 | 0.00951 | 180 | 31 | 9 |
| unique_top | 20000 | trigger_fallback_shade | 120 | -0.40911 | 0.00931 | 172 | 30 | 9 |
| near_gap | 20000 | underbid_15 | 120 | -0.32857 | 0.00768 | 118 | 21 | 7 |
| near_gap | 20000 | underbid_05 | 120 | -0.26124 | 0.14062 | 38804 | 6211 | 1555 |
| tied_top | 20000 | underbid_05 | 240 | -0.15636 | 0.15818 | 49097 | 7858 | 1966 |
| tied_top | 20000 | primary_shade_05 | 240 | -0.04056 | 0.04762 | 4452 | 714 | 180 |
| low_gap_nontop | 20000 | bait_switch | 240 | -0.09089 | 0.12309 | 29733 | 4759 | 1192 |
| honest_top | 20000 | any | 120 | 0 or +0.0041/+0.0122 | 0.00000 | uninformative: focal never wins | | |

Per-horizon summary over the 90 cells: median sd 0.065 (n = 2,000), 0.039 (8,000), 0.025 (20,000); maximum 0.16 to 0.19 at every horizon (the flip cells). Implied pairs for 0.002 / 0.005 / 0.010 per round at the median sd: 8,299 / 1,330 / 334 (n = 2,000), 3,017 / 485 / 123 (8,000), 1,230 / 199 / 52 (20,000). Reading: the quoted headline numbers (0.0094 and 0.0044 per round for `unique_top` underbidding) have SE 0.0011 and 0.00026 and are secure; the small-horizon near-zero cells (`primary_shade_05` at n = 8,000, `honest_top` at n = 2,000) are not powered for 0.002 and should be quoted with intervals, not as signs. With the tape coupling, the no-flip SDs shrink further (Section 2.1) and the flip cells should be reported stratified (Section 3.4) rather than powered.

Recommended replicate counts for the regenerated incentives suite: 240 pairs in every cell (the flip cells gain nothing from more; the no-flip cells are then powered for 0.002 per round at n at least 8,000 and for about 0.004 at n = 2,000), plus a single 1,000-pair cell per instance at n = 8,000 for the profile alone to tighten the false-switch upper bound to 0.003. Cost is negligible (Section 5.5).

### 4.3 Reward per round between mechanisms (scalar_performance, MESP-F minus baseline, paired by seed)

| instance | n | contrast | paired sd | R for 0.002 | R for 0.005 | R for 0.010 |
|--|--|--|--|--|--|--|
| unique_top | 2000 | minus ucb_capacity | 0.0225 | 996 | 161 | 42 |
| unique_top | 8000 | minus ucb_capacity | 0.0127 | 318 | 53 | 15 |
| unique_top | 20000 | minus ucb_capacity | 0.0090 | 160 | 28 | 9 |
| unique_top | 20000 | minus oracle_second_price | 0.0098 | 190 | 32 | 10 |
| tied_top | 20000 | minus uniform_capacity | 0.0082 | 135 | 24 | 8 |
| near_gap | 2000 | minus uniform_capacity | 0.0227 | 1014 | 164 | 43 |
| honest_top | 2000 | minus ucb_capacity | 0.0339 | 2252 | 362 | 92 |
| honest_top | 8000 | minus ucb_capacity | 0.0049 | 49 | 10 | 3 |
| honest_top | 20000 | minus ucb_capacity | 0.0099 | 193 | 33 | 10 |

Across the 48 contrasts: paired sd 0.007 to 0.013 at n at least 8,000 (except `honest_top` at 8,000, 0.004 to 0.008) and 0.018 to 0.035 at n = 2,000. The unpaired SD of MESP-F's own reward per round is 0.009 to 0.020 (a Binomial(n, p) alone would give 0.0035 at n = 20,000; the excess is the random price and phase lengths). The minimum detectable difference with the current 120 pairs is about `2.8 sd / sqrt(120) = 0.256 sd`: 0.002 to 0.003 per round at n at least 8,000 and 0.005 to 0.009 at n = 2,000. The measured within-pair correlations (mostly 0.0 to 0.3) show that seed sharing alone buys little here; only a (round, arm) tape gives real coupling between different allocation rules, and even then two rules that pull different arms see different tape entries, so expect modest gains. Recommended: 200 pairs per cell for the mechanism and ablation suite (powered for 0.002 per round at n at least 8,000 in every instance and for 0.005 at n = 2,000); the compute cost is trivial.

### 4.4 Contextual suites

contextual_incentives (`gain_per_round`, 240 pairs): sd 0.0026 to 0.0078 across the 15 cells; pairs for 0.002 per round: 16 to 122; the current 240 give a minimum detectable effect of 0.0005 to 0.0014 per round. The five quoted end-point gains at n = 32,000 (-0.0089 to -0.0234) have SE 0.00025 to 0.0005. Adequate; keep 240.

contextual_performance (oracle regret per round, method minus LinUCB, 100 pairs): sd 0.0020 to 0.0132; pairs for 0.002: 11 to 347 (the 347 is `smooth, D = 2, n = 2,000`); the current 100 pairs detect 0.0006 to 0.0037 per round. Adequate for the quoted numbers at n = 8,000 (sd at most 0.0058 there). Recommend 100 pairs at the new horizons 20,000 and 200 pairs at n = 2,000 in the smooth family if that cell is quoted.

## 5. Grids

### 5.1 Horizon grid

`{200, 500, 1000, 2000, 5000, 8000, 20000, 50000}`: roughly log-spaced (ratios 2 to 2.5), containing the three retained horizons so that old and new numbers can be compared, the small horizons where exact dynamic programming over the primary state `(r, Z_r)` is feasible (`N_n^2 / 2` states: 5,000 at n = 200, 126,000 at n = 1,000, 522,000 at n = 2,000, still feasible; 5 x 10^6 at n = 5,000, borderline), and 50,000 as the largest horizon so that the `n^{2/3}` rates get a factor 25 in n. The theorem-defined constants on this grid (from `design_table.txt`, K = 3):

| n | L_n | N_n | s_n | b_n(N_n)/N_n | tau when beta_(2) = 0.65 | tau when beta_(2) = 0.80 | r* for tau minus m = 0.05 | r* for 0.10 | r* for 0.20 |
|--|--|--|--|--|--|--|--|--|--|
| 200 | 33 | 101 | 0.590 | 0.329 | 0.060 | 0.210 | 4377 (> N_n) | 1094 (> N_n) | 274 (> N_n) |
| 500 | 83 | 251 | 0.401 | 0.226 | 0.249 | 0.399 | 5110 (>) | 1278 (>) | 319 (>) |
| 1000 | 166 | 502 | 0.298 | 0.168 | 0.352 | 0.502 | 5665 (>) | 1416 (>) | 354 |
| 2000 | 326 | 1022 | 0.222 | 0.123 | 0.428 | 0.578 | 6219 (>) | 1555 (>) | 389 |
| 5000 | 620 | 3140 | 0.170 | 0.074 | 0.480 | 0.630 | 6952 (>) | 1738 | 435 |
| 8000 | 862 | 5414 | 0.148 | 0.058 | 0.502 | 0.652 | 7328 (>) | 1832 | 458 |
| 20000 | 1634 | 15098 | 0.113 | 0.037 | 0.537 | 0.687 | 8061 | 2015 | 504 |
| 50000 | 3092 | 40724 | 0.085 | 0.023 | 0.565 | 0.715 | 8794 | 2199 | 550 |

Two design facts follow and must be stated wherever the small horizons are shown. First, the price is degenerate at small n: with `s_n = 0.59` at n = 200 the price is `(beta_(2) - 0.59)_+`, which is 0 for every instance whose second capacity is below about 0.6 and at most 0.21 for capacity 0.8; at K = 5 and n = 200 the price is 0 even for capacity 0.8. Exact DP at n at most 1,000 therefore measures exploitability of a mechanism that charges little or nothing, and a positive DP gain there is dominated by Stage-1 effort savings (`L_n / n` is 0.17 at n = 200). This is not a defect of the DP, but the paper must not present small-horizon exploitability as informative about the priced regime. Second, primary shading by 0.05 is undetectable by the monitor for n at most 8,000 (`r* > N_n`) and detectable at 20,000 and 50,000; shading by 0.10 becomes detectable at n = 5,000; the sign change of the `primary_shade_05` gain between 8,000 and 20,000 in the committed data is exactly this threshold, and the horizon grid brackets it.

### 5.2 Instance grid (scalar)

Replace the adjective names by a parameterized family with names derived from parameters (this also fixes defect 6). Base: K = 3, capacities `(M_top, M_top - gap, 0.45)`, honest set = {agent 3} (the low-capacity agent), intrinsic means low `(0.10, 0.20, 0.35)` or high `(0.60, 0.60, 0.40)` (high means leave little effort room and make effort savings small relative to allocation), focal = agent 1 (a top agent) or agent 2 (the runner-up). Factors:

| factor | levels | purpose |
|--|--|--|
| K | 2, 3, 5 | the theorem's O_K constants; K = 2 is the smallest legal case; K = 5 stresses `s_n` and Stage-1 length |
| gap `M_top - M_(2)` | 0, 0.01, 0.02, 0.05, 0.10, 0.20 | the gap grid (Section 5.3); gap 0 is the tied-top case |
| honesty pattern | honest non-top only; honest top (`M_top` agent honest with `mu = M_top`, the current `honest_top`) | robustness benchmark `mu_H^star` versus incentive benchmark |
| intrinsic means | low; high | effort room |
| focal | top agent; runner-up | who deviates |

A full factorial is 3 x 6 x 2 x 2 x 2 = 144 instances; at 8 horizons x 8 behaviors x 240 pairs that is 2.2 million trials, about 60 core-hours by the measured costs (Section 5.5), which is affordable but produces more cells than any figure can show. Recommended: (i) the base instance (K = 3, gap 0.25 as today, low means, honest non-top, focal top) at all horizons and behaviors; (ii) one-factor-at-a-time variations from the base (K in {2, 5}; honest top; high means; focal runner-up) at all horizons, 6 instances; (iii) the gap grid below at K = 3 and K = 2, 12 instances; total 19 named instances, about 290,000 trials at 240 pairs per cell, about 8 core-hours. Every instance keeps at least one honest agent, as the theorem requires. The contextual instances stay as they are, except that the contextual-incentives environment should also be run with a K = 2 version and the contextual-performance suite with K = 3 (defect 4 in BASELINE.md: all performance trials use K = 2 while the incentives suite uses K = 3).

### 5.3 Gap grid (private mechanism)

Gaps `{0, 0.01, 0.02, 0.05, 0.10, 0.20}` between the top two capacities, at `M_top = 0.80`, low means, K = 3 and K = 2, all eight horizons, behaviors `profile`, `underbid_05`, `underbid_15`, `primary_shade_05`, `bait_switch`, and the exploitability search's best deviation. The theorem's constant is not uniform as the gap vanishes (statement: "not over sequences whose positive capacity gaps vanish"), and the relevant scale is `s_n`: the gap grid crosses `s_n` (0.085 to 0.59 on the horizon grid) so the reader sees the transition from "runner-up cannot win" (gap much larger than `s_n`) to "coin flip" (gap much smaller than `s_n`). Report for each (gap, n): `p_flip` with Clopper-Pearson interval, `E[gain | no flip]`, `E[gain | flip]`, the overall paired gain, and the private-revenue gap of the profile. Six gaps x 2 K x 8 horizons x 6 behaviors x 240 pairs = 138,240 trials, about 4 core-hours.

### 5.4 Monitor-only Monte Carlo (false switch)

Independent of the mechanism: simulate `Z_r = sum_{q <= r} 1{U_q < tau}` for `r <= N_n` against `r tau - b_n(r)` for tau in {0.3, 0.5, 0.7} and n in the horizon grid, vectorized in chunks of 10,000 paths, 10^5 paths per (tau, n) (5 x 10^9 uniforms at n = 50,000, about a minute per chunk set with NumPy; about 1 core-hour in total). It yields the false-switch frequency to a resolution of 1e-5 with a Clopper-Pearson upper bound of 3e-5 when zero events occur. This is a diagnostic that the union bound is loose by orders of magnitude, not a test of the theorem, and the appendix must say so.

### 5.5 Budget

Measured costs (Slurm job 64527612, node uri-cpu092, Cascade Lake, 4 cores, 8 GB: wall 22 min 31 s, TotalCPU 56 min 33 s, MaxRSS 140 MB for the complete existing suite; the committed timed learner calls: MESP-F 0.019 s per trial at n = 20,000 with a Python primary loop, UCB 0.082 s at n = 20,000, contextual methods 0.06 to 0.18 s per method-run at n = 8,000, that is 8 to 22 microseconds per round in pure Python).

| component | trials or runs | cost per unit | core-hours |
|--|--|--|--|
| Scalar incentives, 19 instances x 8 horizons x 8 behaviors x 240 pairs (tape coupling, vectorized Stage 1 and primary, Python EXP3 only on switch paths) | 292,000 | 0.02 to 0.4 s (fallback length) | about 8 |
| Gap grid (Section 5.3) | 138,000 | same | about 4 |
| Mechanism ablations and non-mechanism baselines (about 8 variants x 3 agent-behavior models x 7 instances x 8 horizons x 200 pairs; Python-loop learners up to 50,000 rounds) | 269,000 | 0.05 to 0.5 s | about 15 |
| Contextual performance at horizons {500, 2000, 8000, 20000}, 100 pairs, plus K = 3 | 28,000 method-runs | 0.05 to 0.5 s | about 2 |
| Contextual incentives at {2000, 8000, 32000} plus K = 2 variant, 240 pairs | 7,200 pairs | 0.1 to 0.7 s | about 1 |
| Monitor-only Monte Carlo | 24 (tau, n) cells x 10^5 paths | vectorized | about 1 |
| Serial runtime benchmark, pinned node, 5 repeats per cell | 400 runs | up to 1 s | about 0.5 |
| Subtotal covered by this document | | | about 32 |
| With a factor-five margin (slow nodes, reruns after protocol fixes, pilot phase) | | | at most 160 |
| Exploitability search (DP exact at n at most 2,000: minutes; learned or black-box search at n in {5000, 8000, 20000}: for example 10^5 rollouts x 8,000 rounds x 10 microseconds = 2.2 core-hours per configuration, 40 configurations) | | | about 100 CPU plus GPU hours on gpu-preempt |
| Non-synthetic evaluation (unknown until the data source is fixed) | | | reserve 200 |
| Total for Agent A | | | about 460 of 2,000 |

This document's components use under 10 percent of the budget even with the margin; the constraint is calendar, not compute. Schedule: pilots (phase 0 seeds, 20 pairs per cell, all suites) submitted 18 to 19 September; protocol freeze (this document's final revision plus a `PROTOCOL.md` with the fixed grids, replicate counts, primary contrasts, and baseline hyperparameters) on 21 September; final runs (phase 1 seeds) 22 to 25 September; buffer for failed jobs 26 to 28 September; no submission after 28 September. Short-QOS limits are 4 hours wall and 2 nodes per user, so split every suite into array tasks of at most 2 hours.

## 6. Hyperparameter and seed protocol

### 6.1 What may and may not be tuned

Theorem-defined and frozen: `L_n`, `N_n`, `s_n`, `b_n(r)`, the EXP3 constants `gamma = min(1/2, sqrt(K log K / H))` and `eta = gamma / K` (both suites already implement these exactly; `scratch/tests/test_design_formulas.py` checks them), and for the contextual rules `h_n = (log(en)/n)^{1/(D+2)}` (Grid-UCB), `h_n = n^{-1/(D+3)}` and `q_n = ceil(n^{2/(D+3)})` (Grid-ETC) with multiplier 1. The grid-multiplier study (0.75, 1, 1.5) is a sensitivity analysis and must be labeled as such; no headline plot may use a multiplier other than 1. The ablation suite changes the mechanism's structure (removing or replacing a component), not its constants; where an ablation needs a constant that the theorem does not define (for example a fixed-window monitor's window), the choice is stated once, taken from the theory where possible, and never tuned on final seeds.

Tunable on pilot seeds only: the UCB exploration constant (current `sqrt(2 log t / T_i)`), LinUCB `alpha` (current 1.0), any regularization in non-mechanism learning baselines, and the search or training hyperparameters of the learned best response. Procedure: grid of at most 3 to 5 values per parameter, selection by mean primary metric over the phase-0 pilot seeds at the middle horizon (8,000), one choice per baseline per environment family, recorded in `PROTOCOL.md` with the pilot table, applied unchanged to all final cells. The appendix must also show the untuned default in one sensitivity figure so the reader can see the tuning did not manufacture the comparison.

Learned or searched best responses: the policy class and the search budget are fixed before training; training uses phase 2 seeds; model selection (if any) uses a validation split of phase 2 (a distinct spawn child), never phase 3; a single evaluation on phase 3 seeds produces the reported gain and its interval. The reported number is the held-out gain of the selected deviation, which is an unbiased estimate of that deviation's gain and hence a lower bound on the class exploitability up to its own sampling error; the maximum over training seeds is not reported as an estimate because it is biased upward by selection. State this in the appendix in one sentence.

### 6.2 Seed derivation

Extend the existing `np.random.SeedSequence([args.seed, ii, n, rep])` (scalar_incentives line 165, scalar_performance line 111) to a single rule used by every suite:

```
trial_ss = np.random.SeedSequence([master, suite_id, phase_id, instance_index, n, rep])
env_bid, env_pri, env_fb, mech, dev = trial_ss.spawn(5)      # child SeedSequences
seed_uint32 = int(trial_ss.generate_state(1)[0])            # stored in the CSV for humans
```

with `master = 20260828` retained, `suite_id` in {1 scalar_incentives, 2 scalar_performance, 3 contextual_performance, 4 contextual_incentives, 5 gap_grid, 6 ablations, 7 exploitability, 8 nonsynthetic}, `phase_id` in {0 pilot, 1 final, 2 train, 3 held-out eval, 9 analysis (bootstrap)}, `instance_index` the position in a frozen instance table, `n` the horizon, `rep` the replicate. Distinct phases give disjoint seed material by construction; NumPy documents `SeedSequence.spawn` as producing children that are independent with very high probability (parallel-generation page, checked). Each child is passed to `np.random.default_rng(child)`; never reseed from a derived integer inside a trial. The CSV stores `seed_key` as the literal list (a string such as `20260828-1-1-3-8000-17`) and the derived `seed_uint32`; the manifest stores `master`. For contextual suites the same rule replaces `910000 + trial` and `86000000 + n*1000 + dev_i*100000 + rep`; the Grid-ETC per-cell seeds `SeedSequence([self.seed, *key])` stay but take `mech` as `self.seed`. The bootstrap child is `SeedSequence([master, suite_id, 9, cell_index, metric_index])`.

Pilot versus final: pilots are phase 0 with 20 pairs per cell; their outputs live under `<scratchpad>/round2/A/runs/pilot/` and never enter the repository or the paper. Final runs are phase 1 and are executed once; if a bug forces a rerun, the rerun uses phase 1 again (identical seeds; the point is that the seeds were never used for selection) and the COMPUTE_LOG records why. The `--quick` flags (which currently reuse final seeds for the first 4 replicates) become `--phase pilot --reps 20`.

## 7. Multiple comparisons

Counts: `paired_summary.csv` has 372 intervals (5 instances x 3 horizons x up to 7 deviations x 4 metrics); `scalar_performance/paired_comparisons.csv` 48 rows x 3 metrics; `contextual_performance/paired_comparisons.csv` 36; `contextual_incentives/summary.csv` 15 x 5 metrics. The new grids multiply this by ten or more. Unadjusted "significance" statements over that many cells are not defensible, but the paper does not need them: its claims are directional statements about a few quoted numbers plus qualitative shapes.

Recommendation, per figure or paragraph:

1. Pre-register in `PROTOCOL.md` one primary contrast family per figure, consisting of exactly the numbers the text quotes. Examples: incentive figure (a): the sign of the paired gain at the largest horizon for each shown deviation (5 contrasts); incentive figure (b): the sign of the five contextual gains at n = 32,000 (5 contrasts); performance figure: MESP-F minus each baseline at the largest horizon in the two shown instances (8 contrasts); gap grid: the profile's private-revenue gap per round at n = 50,000 against `2 s_n` for each gap (6 contrasts).
2. Inside a family, report Holm step-down adjusted p-values (Holm 1979) or, equivalently for the reader, Bonferroni simultaneous intervals at level `1 - 0.05 / m`; with m at most 8 the widening is a factor 1.4 to 1.5 on the half-width, which none of the quoted numbers would fail (their SEs are 20 to 100 times smaller than their magnitudes; Section 4). Holm is preferable to Bonferroni for p-values because it is uniformly more powerful under the same family-wise error control and needs no independence; simultaneous intervals are preferable in figures because they can be drawn. No FDR procedure: the families are small and the claims are confirmatory.
3. Every other cell is exploratory: unadjusted 95 percent intervals, shown as bands, never described as significant or not; the appendix says in one sentence that bands are pointwise and that only the pre-registered contrasts carry adjusted inference.
4. Where the sign of a gain is the claim (deviation is costly at the largest horizon), the relevant test is one-sided against zero and the adjusted interval must exclude zero on the claimed side; where the claim is a rate (gain per round decreases with n), fit the log-log slope on the horizon grid with the delta method on the paired means and report the slope with its interval instead of per-horizon signs.

## 8. Raw-data schema, manifest, storage

### 8.1 Long-format trials schema

One `trials.csv` per suite, one row per (trial, arm-of-interest or method-run), with a common core followed by suite-specific columns; absent columns are written as empty strings, never as zeros. Core columns extend the current ones so that every existing test in `scratch/tests/` still finds its column names:

| column | type | meaning |
|--|--|--|
| suite | str | one of the eight suite names |
| phase | str | pilot, final, train, eval |
| instance | str | parameter-derived name, for example `K3_gap0.05_honNT_muLow_focTop` or the contextual family name |
| instance_index | int | position in the frozen instance table |
| K, D, d | int | dimensions (D = d = empty in scalar suites) |
| n | int | horizon (replaces `horizon`) |
| rep | int | replicate |
| seed_key, seed | str, int | `master-suite-phase-instance-n-rep` and the derived uint32 |
| mechanism | str | `mespf`, ablation variant id, or baseline name (replaces `method`) |
| behavior | str | `profile`, deviation id, or the agent-behavior model under which a mechanism is evaluated |
| focal | int | deviating agent (empty when none) |
| platform_reward | float | `sum Y_t` (realized); contextual suites add `expected_reward` |
| gap_private, gap_honest, gap_capacity | float | `M_(2) n - P`, `mu_H^star n - P`, `M_top n - P` or `sum M_star(X_t) - P_bar` |
| utility_0 .. utility_{K-1}, pulls_0 .., effort_0 .. | float | per-agent `T_i - C_i`, `T_i`, `C_i` (K at most 5; the current `focal_utility` becomes `utility_{focal}` and is kept as an alias column for the tests) |
| tau, winner, focal_won | float, int, int | Stage-1 outcome |
| stage1_rounds, primary_rounds, fallback_rounds | int | phase lengths; they sum to n (assert on every path) |
| switched, false_switch | int | monitor fired; fired while all primary targets were at least tau |
| detection_delay | int | `primary_rounds` if switched else empty |
| runtime_s, runtime_valid | float, int | wall time; 1 only in the serial pinned benchmark job |
| Contextual extras | | `family, grid_multiplier, oracle_regret, honest_shortfall, allocation_accuracy, state_count, parameter_count, h, q, exploration_rounds, visited_cells` |
| Exploitability extras | | `search_class, exact, exploit_dp, exploit_search, train_phase, eval_phase, deviation_id` |

Summaries: `summary.csv` (one row per cell x mechanism x behavior: `reps, mean, sd, se, t_lo, t_hi, bca_lo, bca_hi, cell_index`) and `paired.csv` (one row per cell x contrast x metric: the same plus `p_flip, p_flip_lo, p_flip_hi, mean_noflip, mean_flip` where applicable, and `family_id, holm_p` for pre-registered contrasts). Proportions carry `cp_lo, cp_hi` instead of `t_lo, t_hi`.

### 8.2 Manifest

Each run directory contains `manifest.json` written by `run.py` before the first trial and completed after the last:

```
{"suite": "scalar_incentives", "phase": "final", "master": 20260828,
 "git_commit": "<12-hex from git rev-parse HEAD of the code that ran>", "git_dirty": false,
 "command": "python run.py --phase final --reps 240 --workers 8 --horizons ...",
 "python": "3.12.3", "numpy": "2.5.3", "scipy": "1.18.1", "pandas": "3.0.5", "matplotlib": "3.11.2",
 "bit_generator": "PCG64", "slurm_job_id": "...", "slurm_array_task": "...", "partition": "cpu",
 "node": "cpu053", "cpu_model": "AMD EPYC 7763", "constraint": "amd7763", "cores": 8, "mem_gb": 8,
 "started_utc": "...", "finished_utc": "...", "wall_s": ..., "cpu_s": ...,
 "trials_written": 292800, "trials_sha256": "...", "instances_sha256": "..."}
```

`git_commit` must be a commit that contains the code that ran; if the tree was dirty the manifest says so and the run is a pilot by definition. The instance table (`instances.json`) is hashed so that a renamed or edited instance invalidates old rows.

### 8.3 Locations, naming, and what enters the repository

Runs write under `<scratchpad>/round2/A/runs/<phase>/<suite>/<YYYYMMDDThhmmZ>_<jobid>/` (`trials.csv`, `summary.csv`, `paired.csv`, `manifest.json`, `slurm.out`). Nothing is written into `scratch/experiments/final/` by a job; after the lead accepts a final run, the four files are copied (not moved) to `scratch/experiments/final/<suite>/` by an explicit copy step recorded in COMPUTE_LOG.md, and the figures are regenerated from the repository copy. The repository keeps, per suite: `run.py`, `plot.py`, `README.md`, `instances.json`, `trials.csv.gz`, `summary.csv`, `paired.csv`, `manifest.json`, and the vector figures the paper uses.

Storage estimate: the committed CSVs total 5.7 MB (2.3 MB for 18,360 scalar-incentive rows, about 125 bytes per row; `scalar_incentives/trials.csv` compresses to 327 KB with gzip, a factor 7). The proposed final grids give about 290,000 + 138,000 + 269,000 scalar rows and 35,000 contextual rows, about 730,000 rows at 200 to 300 bytes with the wider schema, that is 150 to 220 MB uncompressed and 20 to 35 MB gzipped, which does not fit the 25 MB supplementary zip together with code and figures. Therefore: (i) commit gzipped trials for the suites the paper quotes (existing four, gap grid, ablations at the horizons shown), expected 10 to 15 MB; (ii) for the remaining cells commit `summary.csv` and `paired.csv` only (a few hundred KB) plus the seed rule, which regenerates any row deterministically; (iii) store all raw trials in the scratchpad and in a tarball outside the repository with its sha256 in the manifest. Check the zip size before every commit of data (`du -sh` under 20 MB including `figures/experiments`, currently 518 KB).

## 9. Reproduction commands and compute log format

### 9.1 Command layout

One `run.py` per suite with a shared `common/` package (mechanism, tapes, seeds, intervals, CSV writer, manifest). Flags, identical across suites:

```
run.py --phase {pilot,final,train,eval} --master 20260828 --reps R
       --horizons 200 500 1000 2000 5000 8000 20000 50000
       --instances instances.json [--instance-index I ...]
       --workers W --out <dir> [--array-task T --array-size S] [--benchmark]
```

`--phase` selects `phase_id` and defaults `--reps` (pilot 20). `--array-task T --array-size S` makes the process run the T-th of S deterministic slices of the (instance, horizon, rep) job list, so a Slurm array reproduces the same rows as a single process; slices are by `(instance_index, n, rep)` hash order fixed in code, and a `merge.py` concatenates the slices, checks that every expected key appears exactly once, and writes `summary.csv`, `paired.csv`, and the completed manifest. `--benchmark` forces `--workers 1`, `OMP_NUM_THREADS=1`, five repeats per cell, and sets `runtime_valid = 1`; all other runs write `runtime_valid = 0`. Every command is prefixed `PYTHONDONTWRITEBYTECODE=1 MPLBACKEND=Agg MPLCONFIGDIR=<scratchpad>/mpl`.

Slurm array script (one per suite and phase, kept under `<scratchpad>/round2/A/slurm/` and copied into the compute log):

```
#!/bin/bash
#SBATCH -J si-final
#SBATCH -p cpu
#SBATCH -A <account from COMMON.md>
#SBATCH -c 8
#SBATCH --mem=8G
#SBATCH -t 02:00:00
#SBATCH --array=0-15
#SBATCH -o <scratchpad>/round2/A/logs/%x-%A_%a.out
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MPLBACKEND=Agg MPLCONFIGDIR=<scratchpad>/mpl
OUT=<scratchpad>/round2/A/runs/final/scalar_incentives/${SLURM_ARRAY_JOB_ID}
<venv>/bin/python <code>/scalar_incentives/run.py --phase final --master 20260828 --reps 240 \
   --horizons 200 500 1000 2000 5000 8000 20000 50000 --instances <code>/scalar_incentives/instances.json \
   --workers 8 --array-task ${SLURM_ARRAY_TASK_ID} --array-size 16 --out ${OUT}
```

followed by a dependent merge job (`--dependency=afterok:<array job id>`, `-c 1`, 30 minutes) that runs `merge.py --in ${OUT} --out ${OUT}` and `validate.py`. Benchmark job: `-c 2`, `--exclusive` if the partition allows it, otherwise `-C amd7763` (or another single node feature from `sinfo -p cpu`; the partition mixes Cascade Lake, Skylake, Ice Lake, Zen2, Zen3, and Zen4 nodes, so an unpinned runtime is not comparable between jobs), `--benchmark`, and the manifest's `cpu_model` from `lscpu`. Never time anything on the login node (it reports a QEMU virtual CPU). Plot and composite scripts run on the login node from the repository copy of the data (seconds), with the same environment prefix. The existing README commands remain valid for the retained suite until the new suite replaces it; the new README lists the exact final `sbatch` lines with their job ids.

### 9.2 COMPUTE_LOG.md format

One table per output directory, appended at submission and completed at job end, plus a footer with totals. Columns:

| date (UTC) | job id | array size | script (path) | suite / phase | partition | node(s) | cores x tasks | wall (h:mm) | TotalCPU (core-h) | max RSS | state | seed master / phase id | output dir | note |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

`TotalCPU` and `MaxRSS` come from `sacct -j <id> --format=JobID,Elapsed,TotalCPU,MaxRSS,NodeList,State -P` after completion (for the baseline job: 00:22:31 wall, 56:33 TotalCPU, 139,676 KB, uri-cpu092, COMPLETED). Core-hours are `TotalCPU` in hours (0.94 for the baseline job), not `cores x wall` (1.50), and the footer reports both plus the cumulative total against the 2,000 core-hour budget. Failed or cancelled jobs are logged too, with the reason. A copy step (scratch to repository) is a row with partition `none`.

## 10. Defects found in the current suites

Severity per the COMMON.md scale. Line numbers refer to the committed files.

1. P1 (for the new suites; P2 as committed). `scalar_incentives/run.py` line 120, `assert np.all(effort >= -1e-9)`. The model allows negative cumulative effort (any target below `mu_i` for long enough; bait-and-switch delivers 0). It never fires at the retained horizons because the switch comes after about 44 to 84 primary pulls while Stage-1 effort is `L_n (M_i - mu_i)`; but an exploitability search or a deviation that delivers below `mu_i` without triggering (a strategic winner with `tau - 0.15 < mu_W`, or any long tenure at a low target in an ablation without a monitor) crashes the worker or, if the class is restricted to avoid it, silently truncates the deviation class. Repair: delete the assertion; assert instead `pulls.sum() == n` and `effort >= -pulls * mu` elementwise (the true lower bound).
2. P1 (statement about what was tested). `scalar_incentives/run.py` lines 66 to 67 give `bait_switch` and `nontop_win_underperform` identical targets in every phase; with shared seeds all 720 `nontop_win_underperform` rows equal the `bait_switch` rows (verified: identical values in all columns). `appendix_experiments.tex` line 10 lists "bait-and-switch" and "non-top winning followed by underperformance" as two of seven tested deviations, and the quoted "loses 0.091 utility per round" is the `bait_switch` mean (-0.09089) in `low_gap_nontop`. Further, the theoretically distinct case (a non-top winner that cannot deliver `tau` because `M_i < tau`) has probability at most `n^{-4}` under the mechanism (it requires the bad bidding event), and in `low_gap_nontop` the focal runner-up has `M = 0.795 > tau`, so no such case is exercised. Repair: drop the duplicate behavior and the sentence, or define the non-top deviation as something distinct (for example the runner-up delivers its own capacity in the primary phase, which is at least `tau` and hence not an underperformance) and describe it accurately.
3. P2. Percentile-bootstrap indices come from `Generator.integers` (scalar_performance lines 100 to 102 and 118; contextual_performance `bootstrap()` line 184 and `plot.py` line 88; contextual_incentives `summarize()` line 98) and from `rng.integers` inside a Python loop (scalar_incentives lines 146 to 149). NumPy's compatibility policy guarantees stream reproducibility only for the same build in the same environment and explicitly allows `Generator` method streams to change between versions; BASELINE.md already shows the committed `scalar_performance/paired_comparisons.csv` endpoints (138 cells) are not reproducible with NumPy 2.5.3 from the committed trials. Repair: t-intervals as primary; BCa via `scipy.stats.bootstrap` with a per-cell child seed as secondary; pin versions in the manifest; regenerate.
4. P2. The same policy explains the two trial rows that differ between NumPy 2.3.1 and 2.5.3 (BASELINE.md): both scalar suites draw Stage-1 bids with `rng.binomial` and one uses `rng.choice`, `Generator` methods with no cross-version guarantee. Repair: implement every random primitive from uniform doubles (`Y = 1{U < m}`, permutations by `argsort` of uniforms, categorical draws by `searchsorted` on the cumulative probabilities, which scalar_incentives's EXP3 already does), which also delivers the tape coupling; still pin versions.
5. P2. Pairing is stream-based, not tape-based (Section 3.1; lead's count: `tau` identical in 74, 91, 92 percent of `underbid_05` pairs in `unique_top`). Estimates are unbiased; the words "paired common-random-number" in the README and "paired" in `experiments.tex` line 4 and `appendix_experiments.tex` line 5 overstate the coupling for underbids and for every fallback comparison, although the appendix's sentence "Once adaptive scalar paths diverge, matching seeds do not imply identical counterfactual noise" partially discloses it. Repair: the per-(agent, pull index) tape of Section 3.2, which is the proof's coupling; then the sentence becomes true without qualification.
6. P2. Degenerate intervals for binary and zero-variance metrics: `paired_summary.csv` reports `fallback` differences with mean 0 and interval [0, 0] (for example `unique_top, 2000, underbid_05`) and `honest_top` at n = 20,000 has SD exactly 0 in every deviation because the focal agent never wins Stage 1 (`focal_won` = 0 of 120). Repair: Clopper-Pearson intervals for proportions with the rule-of-three upper bound; choose or label instances so that the focal agent's win probability is bounded away from 0 and 1 where the cell is meant to be informative.
7. P2. Unsupported provenance claims in `appendix_experiments.tex` line 7: "Apple arm64 host", "less than 30 minutes of wall-clock time", "at most three worker processes"; no artifact on this machine supports them, and the Slurm reproduction took 22 min 31 s wall and 56.5 CPU-minutes on a Cascade Lake node. Repair: replace with the manifest's numbers from the final regeneration (node model, cores, wall, TotalCPU).
8. P2. Runtime columns were measured under three-way process parallelism (contextual_performance, `ProcessPoolExecutor(3)`; BASELINE.md item 5) and, for scalar_performance, in a serial process on an unrecorded host; the appendix quotes their sums (131 s and 483 s, which I reproduce from the committed CSVs) and the `runtime_memory` figure plots them. Repair: the serial pinned benchmark job with `runtime_valid = 1`; exclude other runtimes from figures.
9. P2. One bootstrap generator is shared across all cells in loop order (`brng` in both scalar suites; `rng` in the contextual summaries), so any change to the set of metrics, cells, or iteration order changes every downstream interval, and no cell's interval can be recomputed in isolation. Repair: per-(cell, metric) child seeds (Section 3.3).
10. P2. Seed schemes differ across suites: `generate_state(1)` (uint32) in scalar_incentives, `generate_state(1, dtype=np.uint64)` in scalar_performance, `910000 + trial` in contextual_performance, `86000000 + n*1000 + dev_i*100000 + rep` and `777000 + rep` in contextual_incentives; the contextual suites have no `--seed` flag. All are valid seeds, but pilot seeds are not separated from final seeds anywhere (`--quick` reuses the first replicates' seeds), and the seed material is not derived from one master. Repair: Section 6.2.
11. P2. `contextual_incentives/run.py` line 111, `reps = 4 if a.quick else max(240, a.reps)`: the flag cannot lower the replicate count, which blocks pilots and the phase separation. Repair: `--phase` with phase-specific defaults.
12. P2. Instance names collide with different parameters across the two scalar suites (`unique_top` intrinsic means (.10, .20, .35) versus (.10, .20, .40); `tied_top` third mean .35 versus .45; `near_gap` .45 versus .50; BASELINE.md item 7), so "unique_top" in the incentive figure and in the performance figure are different instances. Repair: parameter-derived names from one `instances.json` shared by all suites.
13. P2. `honest_shortfall` in contextual_performance is `max_i mu_i(x) - reward` (line 153: `honest = mu.max(axis=1)`), the best intrinsic mean over all agents, not over the honest set; the theorem's benchmark is `mu_H^star`. Nothing in the paper quotes it, but the column name is wrong. Repair: rename to `intrinsic_shortfall` or compute over a declared honest set.
14. P2. Two implementations of MESP exist (`scalar_incentives.trial`, vectorized primary tape; `scalar_performance.mespf`, per-round loop with `rng.choice` in EXP3). They agree in distribution (the tests check the formulas in both) but not pathwise, so "MESP-F" in the performance suite and "profile" in the incentive suite are different sample paths even for equal seeds and instances. Repair: one module.
15. P2. Quoted point estimates without uncertainty: `appendix_experiments.tex` line 10 (0.0044, 0.0094, -0.114, -0.280, -0.409, 36.3 percent, -0.091), line 28 (the eight regret numbers), line 39 (-0.0089 to -0.0234). All are secure by Section 4 (SEs 20 to 100 times smaller), but the reader cannot see that. Repair: print the interval or the SE after each quoted number and pre-register them as the primary contrasts (Section 7).
16. P2. No false-switch metric exists; `fallback` counts every switch. Under the profile they coincide when `M_W >= tau`, which held in every committed row, but under deviations and ablations they differ. Repair: the `false_switch` column (Section 2) and the monitor-only Monte Carlo (Section 5.4).
17. P3. Bootstrap resample counts differ (4,000; 2,000; 5,000) and the contextual_performance paired contrasts are computed inside `plot.py` (seed 7721) rather than `run.py`, so a plotting script writes a data file and the README's statement that `paired_comparisons.csv` comes from the run is only true for the scalar suite.
18. P3. `contextual_performance` grid-sensitivity cells (multipliers 0.75 and 1.5) use fresh trial ids, hence different contexts and tapes from the multiplier-1 cells; the `grid_sensitivity` figure compares unpaired cells and shows no intervals. Repair: same seeds across multipliers; bands.
19. P3. `expected_reward` and `oracle_regret` in contextual_performance are conditional-mean quantities (`reward += cap[t, a]`), a legitimate variance reduction, but `appendix_experiments.tex` line 28 calls them "regret per round" without saying so; only the suite README does. Repair: one clause in the appendix.
20. P3. `appendix_experiments.tex` line 10 says assertions verify the phase identity on every path; only the incentive suite asserts it (BASELINE.md item 2). With one shared mechanism module the assertion covers both.
21. P3. `scratch/tests/test_regression_csv.py` recomputes only n = 2,000 rows; both NumPy-sensitive rows are at n = 8,000 and 20,000, so the regression test cannot detect that class of drift. Repair: include one row per (instance, behavior) at the largest horizon in a slow marker.
22. P3. `write_csv` takes the field names from the first row; rows with extra keys would be silently truncated by `csv.DictWriter` only if `extrasaction` were set, otherwise it raises; harmless today but fragile with the wider schema. Repair: an explicit column list (contextual_performance already does this).
23. P3. `low_gap_nontop` is described as testing a "non-top" deviator, but its runner-up capacity 0.795 exceeds the realized price (about 0.68 at n = 20,000), so it can deliver `tau` and its bait-and-switch loss is the ordinary monitored loss, not a non-top effect; with the gap grid this instance becomes the gap-0.005 point and needs no separate name.

## 11. References checked (primary sources, URLs retrieved 17 September 2026 from the login node)

1. NumPy, "Compatibility policy" for `numpy.random`: https://numpy.org/doc/stable/reference/random/compatibility.html (HTTP 200; text checked: "If you create a Generator with the same BitGenerator, with the same seed, perform the same sequence of method calls with the same arguments, on the same build of numpy, in the same environment, on the same machine, you should get the same stream of numbers"; "Breaking stream-compatibility in order to introduce new features or improve performance in Generator or default_rng will be allowed with caution"; "BitGenerator classes have stronger guarantees of version-to-version stream compatibility"). Used in Sections 3 and 10.
2. NumPy, NEP 19 "Random number generator policy": https://numpy.org/neps/nep-0019-rng-policy.html (HTTP 200; the policy background for item 1).
3. NumPy, "Parallel random number generation" (SeedSequence spawning; children "independent" with very high probability): https://numpy.org/doc/stable/reference/random/parallel.html and https://numpy.org/doc/stable/reference/random/bit_generators/generated/numpy.random.SeedSequence.html (both HTTP 200). Used in Section 6.2.
4. Efron, B. (1987). Better bootstrap confidence intervals. Journal of the American Statistical Association 82(397), 171 to 185. DOI 10.1080/01621459.1987.10478410. Publisher page returned a challenge page to curl; bibliographic record verified through the Crossref registry, https://api.crossref.org/works/10.1080/01621459.1987.10478410 (title, journal, volume, issue, pages, year, author match). BCa; Section 3.3.
5. DiCiccio, T. J. and Efron, B. (1996). Bootstrap confidence intervals. Statistical Science 11(3), 189 to 228. https://projecteuclid.org/journals/statistical-science/volume-11/issue-3/Bootstrap-confidence-intervals/10.1214/ss/1032280214.full (HTTP 200; Crossref record 10.1214/ss/1032280214 confirms authors, journal, volume, issue, year). Section 3.3.
6. Hall, P. (1988). Theoretical comparison of bootstrap confidence intervals. The Annals of Statistics 16(3), 927 to 953. https://projecteuclid.org/journals/annals-of-statistics/volume-16/issue-3/Theoretical-Comparison-of-Bootstrap-Confidence-Intervals/10.1214/aos/1176350933.full (HTTP 200; Crossref record confirms). Section 3.3.
7. Efron, B. and Tibshirani, R. J. (1993). An Introduction to the Bootstrap. Chapman and Hall (Springer US record). DOI 10.1007/978-1-4899-4541-9; verified through https://api.crossref.org/works/10.1007/978-1-4899-4541-9 (title, publisher, year, authors). General bootstrap reference; not load-bearing.
8. Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics 6(2), 65 to 70. JSTOR stable URL https://www.jstor.org/stable/4615733 returned a client-challenge page to curl; bibliographic record verified through OpenAlex (https://api.openalex.org/works?filter=publication_year:1979,title.search:sequentially%20rejective: title, journal, volume 6, pages 65 to 70, author Sture Holm, DOI 10.2307/4615733). Section 7.
9. Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables. Journal of the American Statistical Association 58(301), 13 to 30. DOI 10.1080/01621459.1963.10500830; publisher page challenge-blocked; Crossref record https://api.crossref.org/works/10.1080/01621459.1963.10500830 confirms. Basis of the `(2 n^4)^{-1}` tail in the monitor lemma; Section 2.1.
10. Clopper, C. J. and Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. Biometrika 26(4), 404 to 413. DOI 10.1093/biomet/26.4.404; publisher page challenge-blocked; Crossref record https://api.crossref.org/works/10.1093/biomet/26.4.404 confirms. Exact proportion intervals; Sections 2.1 and 3.3.
11. Brown, L. D., Cai, T. T., and DasGupta, A. (2001). Interval estimation for a binomial proportion. Statistical Science 16(2), 101 to 133. https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.full (HTTP 200; Crossref record confirms). Section 3.3.
12. Glasserman, P. and Yao, D. D. (1992). Some guidelines and guarantees for common random numbers. Management Science 38(6), 884 to 908. DOI 10.1287/mnsc.38.6.884; publisher page challenge-blocked; Crossref record https://api.crossref.org/works/10.1287/mnsc.38.6.884 confirms. Monotone coupling and variance reduction; Section 3.2.
13. SciPy, `scipy.stats.bootstrap` (BCa default, `paired=True`, `rng` argument): https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html (HTTP 200; signature and method options checked). Section 3.3.
14. Slurm, "Job Array Support": https://slurm.schedmd.com/job_array.html (HTTP 200). Section 9.1.
15. Auer, Cesa-Bianchi, Freund, and Schapire (2002), EXP3, is cited by the paper (`auer2002nonstochastic` in `references.bib`) and was not re-verified here; nothing in this document depends on it beyond the constants the tests already check.

Not verified and therefore not cited: nothing else. The sample-size formula in Section 4 is the standard paired t-test power calculation and needs no citation; the crossing-time formula in Section 2 is derived in this document and checked against the data.

## Closing note

What this document does not do: it does not design the exploitability search, the ablation set, or the non-synthetic study (other scouts do), and it does not certify that the committed numbers are error-free; it states which checks were run (Sections 2.1, 4, 10) and where the outputs are. Every number above that is not attributed to a file was computed by the scripts named at the top from the committed `trials.csv` files; the two NumPy-sensitive rows change no digit printed here.
