# Experimental claim matrix (Agent A, 17 September 2026)

Purpose: map every theorem and mechanism claim of the canonical manuscript to the experiment that currently supports it, state what that experiment establishes and what it does not, and name the most informative missing experiment with its data, code, and compute needs. This document is read-only analysis; no canonical file was changed.

What I read completely: `scratch/experiments/final/` (README, four `run.py`, four `plot.py`, `validate.py`, `make_composites.py`, headers and summaries of every CSV), `scratch/tests/` (five files), `audit/round2/BASELINE.md`, `sections/experiments.tex`, `sections/appendix_experiments.tex`, `sections/setting.tex`, `sections/Stochastic_SAMF_Conditions.tex`, `sections/Public_information_setting.tex`, `sections/Private_information_setting.tex`, `sections/contextual.tex`, `sections/contextual_samf_algorithm.tex`, all five appendices, `sections/Intro.tex`, `references.bib`, and the prior-round experiment reports under `audit/experiments/` (treated as claims, not evidence).

What I computed (login node, seconds, pandas on the committed CSVs; commands recorded in Section 7): design constants L_n, N_n, s_n, b_n(N_n) at the tested and proposed horizons; the pairing integrity of the scalar-incentive suite; the analytic Stage-1 effort saving versus the measured underbid gains; the exploration share of Static Grid-ETC in the contextual-incentive suite; the duplicate-row check.

Evidence categories used throughout (COMMON.md rule 4): every current experiment is a fully synthetic simulation with Bernoulli outcomes and scripted agent behavior. No current experiment is real deployment evidence, offline evaluation on logged data, or real-data-calibrated simulation.

## 1. Inventory of the current suites

### 1.1 Scalar incentives (`scalar_incentives/run.py`)

- Mechanism: MESP exactly as in Section 5 (L_n, N_n, s_n, tau = (beta_(2) minus s_n)_+, strict boundary Z_r < r tau minus b_n(r), fresh explicit-exploration EXP3 with gamma = min(1/2, sqrt(K log K / H)), eta = gamma / K). Stage 2 is vectorized: the whole primary Bernoulli stream is drawn at once and the first boundary crossing is located; this is distributionally exact because every tested primary target is constant within the phase (line 104 to 113). Any history-dependent primary behavior would need the roundwise loop.
- Instances (mu; M; honest; focal): unique_top (.10,.20,.35; .90,.65,.40; arm 2 honest; focal 0), tied_top (.10,.20,.35; .80,.80,.45; arm 2; focal 0), near_gap (.10,.20,.45; .80,.76,.50; arm 2; focal 0), honest_top (.75,.20,.15; .75,.70,.45; arm 0 honest; focal 1), low_gap_nontop (.10,.20,.45; .80,.795,.50; arm 2; focal 1).
- Behaviors: profile; underbid by .05 and .15 in Stage 1; primary shade by .05 and .15 below tau; bait_switch (bid M, deliver 0 in primary); trigger_fallback_shade (bid M, deliver 0 in primary and 0 in fallback); nontop_win_underperform (identical targets to bait_switch, lines 66 to 67).
- Horizons 2,000, 8,000, 20,000; 120 replicates (240 for tied_top and low_gap_nontop); metrics focal utility, platform reward, fallback indicator, fallback rounds, tau, winner, phase lengths; paired differences with percentile bootstrap (4,000 resamples).
- Design constants at the tested horizons (K = 3): n = 2,000: L = 326, KL/n = .49, N = 1,022, s_n = .222; n = 8,000: L = 862, KL/n = .32, N = 5,414, s_n = .148; n = 20,000: L = 1,634, KL/n = .25, N = 15,098, s_n = .113. Half of the horizon at n = 2,000 is bidding, and the conservative correction lowers the price by .11 to .22 below the runner-up bid. These constants, not agent behavior, explain most of the finite-horizon revenue shortfall in the performance suite (Section 1.2).

### 1.2 Scalar performance (`scalar_performance/run.py`)

- Same mechanism with a roundwise Stage 2 loop; all agents follow the proposed profile S_star. Instances differ from the incentive suite despite sharing names (unique_top mu_3 = .40 instead of .35, tied_top .45 instead of .35, near_gap .50 instead of .45); honest_top identical.
- Comparators: capacity UCB (every selected agent delivers M_i; index sqrt(2 log t / T_i) with fixed index-order initialization, not the manuscript's random initialization), intrinsic UCB (every agent delivers mu_i), uniform allocation with capacity delivery, oracle second price (knows capacities; pulls a top agent at target M_(2), or max(mu, M_(2)) if honest). None of the comparators is a mechanism; each fixes a behavior by fiat.
- Metrics: reward per round, capacity and second-price shortfalls, effort, runtime, phase lengths, fallback, pull shares; 120 paired replicates; bootstrap and paired-contrast CSVs.
- Under S_star, fallback never occurred in 1,440 MESP runs; mean tau equals the runner-up capacity minus s_n to three decimals (unique_top n = 20,000: .539 versus .65 minus .113 = .537).

### 1.3 Contextual performance (`contextual_performance/run.py`)

- Rules: cell-local Grid-UCB with h = (log(en)/n)^(1/(D+2)) times a multiplier; Grid-ETC with h = n^(-1/(D+3)), q = ceil(n^(2/(D+3))), fresh permutations per block, priority tie-break, post-exploration feedback ignored; context-blind UCB; disjoint LinUCB on the full profile with alpha = 1; exact finite-context UCB (finite family only).
- Environments: arm-local mu and M; families linear (affine in own context), smooth (sinusoidal), checkerboard (discontinuous), finite (three levels per coordinate). K = 2 whenever D is even, so every continuous family uses K = 2 with d = 1 or 3; the finite family uses K = 2, d = 1. Horizons 2,000 and 8,000; 100 replicates; every agent delivers capacity (all-maximum play). Regret is measured against the delivered-capacity oracle using conditional means.
- Nothing strategic happens in this suite; it is a pure learning comparison under S_max.

### 1.4 Contextual incentives (`contextual_incentives/run.py`)

- K = 3, d = 1, D = 3, X uniform on [0,1]^3; capacities (.72, .72, .53 + .08 x_3); mu_i = .16 + .04 x_i. The top set is {0, 1} on the whole cube, so the closed null separator described in the appendix (B = {x_1 = 1/2}) separates nothing: both "components" have the same top set and the same capacities. Static Grid-ETC at theorem rates; five fixed shading maps of arm 0 (constant .10; cell-aligned .14; misaligned .14 on x_1 < .37; near-boundary .16; random piecewise-constant map drawn before play); 240 paired replicates at n = 2,000, 8,000, 32,000; utility gain, reward change, arm-0 pulls.
- Measured exploration share of the baseline path (my computation from `trials.csv`): 91.4 percent of rounds at n = 2,000 (64 cells, q = 13), 76.4 percent at 8,000 (125 cells, q = 20), 63.5 percent at 32,000 (216 cells, q = 32). The suite therefore measures mostly the exploration phase; commitment effects only begin to dominate at the largest horizon, which is why all five maps look profitable at 2,000 and costly at 32,000.

## 2. Claim matrix

Each entry has six fields: (a) claim as stated; (b) current experiment; (c) what it establishes; (d) what it does not establish; (e) most informative missing experiment; (f) data, code, compute.

### C1. Theorem `thm:sharp-robustness` (sharp adaptivity implies P(n;S) >= mu_H^star n minus O(K sqrt(n log n)))

(a) Deterministic implication; for any sharply adaptive rule on its class.
(b) None. The performance suite reports `honest_shortfall` (contextual) and no scalar suite reports the gap to mu_H^star n for UCB under non-maximum profiles.
(c) Nothing about this claim.
(d) The robustness guarantee for UCB under arbitrary fixed profiles S in S_HI (mixtures of shading agents) has never been simulated.
(e) A small UCB robustness sweep: K in {2,3,5}, honest agent at mu_H^star, strategic agents at fixed targets drawn from a grid including 0; report (mu_H^star n minus P(n;S)) / sqrt(n log n) versus n on a log grid; it should stay bounded. Low priority (the theorem is standard), but it is the only way to show the sqrt(n log n) constant is moderate.
(f) Existing UCB loop from `scalar_performance/run.py` generalized to arbitrary fixed profiles; about 1 to 3 core-hours for n up to 50,000 with 200 replicates; no data.

### C2. Theorem `thm:scalar-ucb` (symmetric UCB is stochastic SAMF on S_HI: sharp adaptivity O(sqrt(n log n)), monotonicity o(n), exact expected FATA)

(a) Three properties for deterministic horizon-independent fixed means.
(b) None directly. Capacity UCB in the performance suite runs one profile (all-maximum) and records pull shares, which is not an SAMF test. Its initialization is fixed index order (line 91 of `scalar_performance/run.py`), not the uniform random order the theorem requires for FATA.
(c) Nothing about sharp adaptivity, monotonicity, or FATA.
(d) Monotonicity (raising one agent's fixed mean does not raise another's share by a linear amount) and FATA (equal-law top agents have equal expected counts) are cheap to test and untested.
(e) A monotonicity and FATA panel: for a fixed instance, sweep agent i's fixed mean over a grid and plot each other agent's expected share; check FATA with two tied top agents and symmetric versus index-order initialization (the index-order version violates exact FATA at finite n, which would make a good ablation of "symmetric initialization"). Supplementary material rather than main text.
(f) Same UCB code with random initialization; about 2 core-hours; no data.

### C3. Theorem `thm:public-ucb` (public restricted equilibrium: with K_top >= 2, all-maximum play is an S_HI equilibrium under symmetric UCB; revenue M_top n minus O(log n)) and the appendix remark that the two-top condition cannot be dropped

(a) Equilibrium within fixed-mean deviations; necessity of two-top illustrated by a unique-top agent with slack.
(b) None. No suite runs UCB under a unilateral fixed-mean deviation.
(c) Nothing.
(d) Both the equilibrium claim and the necessity remark are untested, although both are cheap and the deviation class S_HI is one-dimensional per agent (a fixed target m in [0, M_i]), so the exact best response within the class is a one-dimensional search.
(e) S_HI exploitability of UCB: for tied-top and unique-top instances, sweep the focal agent's fixed target over a grid of 41 values in [0, M_i], estimate the paired utility gain against all-maximum play with common reward tapes, and report the maximum over the grid as the (grid-resolved) in-class exploitability; plot gain per round versus n. Expected outcome: tied-top gain per round decreases toward zero, unique-top gain is linear (about (M_top minus M_(2) minus margin) per round). This is the only experiment that shows the two-top condition doing work. Cheap and directly mechanism-relevant.
(f) UCB loop (about 20 microseconds per round in Python, so 0.4 s per episode at n = 20,000); 41 targets times 200 replicates times 3 horizons times 2 instances = 49,200 episodes, about 3 to 5 core-hours; vectorization across replicates would cut this to minutes.

### C4. Theorem `thm:private-mesp`, equilibrium part (behavioral additive equilibrium: sup over B_{i,n} of the unilateral gain is O(n^(2/3) (log n)^(1/3)); explicit bound L_n + 2 n s_n + 2 b_n(n) + R_K(n) + O(1) for a top agent, plus O(log n / delta_i^2 + R_K(n) / delta_i) for a non-top agent)

(a) Uniform over every feasible nonanticipating unilateral behavior, on each fixed instance.
(b) Scalar incentives: seven hand-picked behaviors (six distinct) in five instances at three horizons; Figure 1(a) of the paper shows unique_top only.
(c) Establishes that those specific behaviors produce the reported paired gains: underbidding gains .0094 to .0044 per round (unique_top, .05), primary shading by .05 gains at n = 2,000 and 8,000 and loses at 20,000, bait-and-switch and fallback shading lose heavily, and non-top deviations lose in low_gap_nontop. My check: the measured underbid gains equal the analytic Stage-1 effort saving L_n times the underbid (unique_top: analytic .0082, .0054, .0041 per round versus measured .0094, .0049, .0044 for .05; .0244, .0162, .0123 versus .0235, .0156, .0127 for .15). So the experiment demonstrates that the L_n term in the theorem's bound is attained by the simplest deviation, which makes the theorem's rate n^(2/3) (log n)^(1/3) unimprovable for MESP as specified. This is a positive and currently unstated fact.
(d) It does not estimate exploitability: the tested deviations are not the best in class. Two better in-class deviations are visible by inspection. First, underbid down to just above the runner-up (slack M_top minus M_(2) minus a safety margin, .25 minus margin in unique_top instead of .15), which scales the L_n gain by the slack. Second, boundary hugging in Stage 2: the monitor tolerates a cumulative deficit of b_n(r) = sqrt(r log(2 n^4) / 2) (b_n(N) = 126, 315, 552 utility units at the three horizons), so a deviator that keeps its target sum a bounded number of standard deviations above the boundary saves effort of order sqrt(n log n) with small detection risk; the tested constant shades do not do this (a constant shade epsilon is detected after about log(2 n^4) / (2 epsilon^2) rounds, which is 6,200, 7,300, 8,100 rounds for epsilon = .05, matching the observed switch to detection between n = 8,000 and 20,000). Combining both, the true in-class exploitability at n = 20,000 in unique_top is plausibly several times the .0044 per round shown in Figure 1(a). The experiment also cannot say anything about history-dependent behavior because Stage 2 is vectorized for constant targets. Finally, the paper's sentence "the normalized gain from underbidding decreases with the horizon" is true but its mechanism (n^(-1/3) scaling of L_n / n) is not stated, and in honest_top the .15 underbid gain does not decrease over the tested horizons (.0061, .0126, .0123 per round; the focal agent is the price-setting loser, so its saving is pure Stage-1 effort).
(e) Exact best response over B_{i,n}. The deviator's information state is small: in Stage 1 it is (pull index, own successes); after Stage 1 it observes tau and whether it won; in Stage 2 it is (r, Z_r) because it is the only agent pulled; in fallback it observes only its own selections and rewards. Its per-pull utility 1 + mu_i minus m and the Bernoulli transition are both affine in m, so at every state the optimal target is an endpoint: m in {0, M_i} (or {mu_i, M_i} for an honest deviator). Backward induction over (r, Z_r) with two actions is therefore exact, needs no target discretization, and costs O(N_n^2) per price value; Stage 1 is a second backward induction over (pull, successes) with terminal value given by the exact distribution of the other agents' bids (independent binomials at capacity). The only part that is not exactly solvable is the fallback continuation, where the deviator does not see EXP3's weights; it is bracketed below by simulated fixed fallback strategies and above by the appendix bound (1 + mu_i minus V_i) H + R_K(H) for a top deviator, which is loose only when H is below roughly (R_K(H) / (2 s_n H))^2 ... about 600 rounds at n = 20,000, so the certified bracket should be narrow for top deviators and vacuous for non-top deviators with tiny gaps (as the theorem's non-uniformity predicts). Output: exact (bracketed) exploitability per round versus n on a log grid from 200 to 50,000, per instance, against the theorem's explicit bound, plus the optimal policy as a threshold map in (r, Z_r minus r tau). For larger n and as an independent check, black-box search over parametric policies gives lower bounds. Scout A2 develops this plan in detail.
(f) New code (DP in NumPy, vectorized over Z); about 5 to 30 minutes per instance and horizon up to n = 20,000 on one core and about 15 core-hours per instance at 50,000 if parallelized over price values; total well under 150 core-hours including pilots. No data.

### C5. Theorem `thm:private-mesp`, revenue part (P(n;S_star) >= M_(2) n minus O_K(n^(2/3) (log n)^(1/3)))

(a) Revenue under the proposed profile.
(b) Scalar performance: MESP reward per round under S_star versus the oracle second price (M_(2) or max(mu, M_(2))) and three non-mechanism comparators.
(c) Establishes the finite-horizon shortfall under S_star: at n = 20,000, .567 versus .650 (unique_top), .682 versus .800 (tied_top), .657 versus .760 (near_gap), .721 versus .750 (honest_top), and that the shortfall shrinks with n. The shortfall decomposes almost exactly into bidding cost (KL_n / n times the difference between the average capacity and M_(2)) and the price correction s_n; no fallback ever occurred.
(d) It does not show the rate: three horizons spanning one decade cannot separate n^(-1/3) from n^(-1/2). It does not isolate the two components (L_n length versus s_n correction), and it offers no mechanism baseline (every comparator fixes a behavior by assumption). The paper's caption "MESP pays a short-horizon cost for bidding and conservative pricing" is a plausible reading of the numbers, not a measured decomposition.
(e) A decomposition and ablation panel: revenue gap to M_(2) n per round versus n on a log grid (200 to 50,000 or more; the mechanism is cheap), with the analytic decomposition KL_n (M_(2) minus mean capacity) + N_n s_n overlaid, and mechanism variants (L multiplier in {1/4, 1, 4}; tau without s_n) so the trade-off between bidding cost, price error, and exploitability is visible. Because the DP of C4 gives exploitability for each variant, a scatter of revenue gap against exploitability per variant is the single most informative mechanism-design figure available.
(f) Existing code with parameters exposed; under 10 core-hours.

### C6. Theorem `thm:private-mesp`, robustness part (for every feasible behavioral profile S, P(n;S) >= mu_H^star n minus O_K(n^(2/3) (log n)^(1/3)))

(a) Joint behavioral profiles, not unilateral deviations; the honest agent is the comparator.
(b) None. The incentive suite is unilateral; the performance suite is S_star only. The trigger_fallback_shade behavior is unilateral and the focal agent is not honest.
(c) Nothing about joint adversarial play.
(d) The claim that the fresh EXP3 fallback is what makes robustness hold under arbitrary joint behavior (appendix, final paragraph) is exactly the claim that distinguishes MESP from exclusion-based variants, and it is untested.
(e) Joint adversarial profiles for each mechanism variant: (i) every strategic agent bait-and-switches; (ii) sequential shading (after the first exclusion or switch the next strategic agent shades); (iii) strategic agents deliver 0 in fallback; (iv) fallback-phase adaptive behavior (deliver M_i for the first rounds of fallback, then 0). Metric: (mu_H^star n minus P(n;S)) / n versus n for MESP, permanent-exclusion variants, unmonitored second price, and UCB fallback. Expected: MESP and monitored variants stay near or above the honest benchmark; unmonitored second price and exclusion followed by unmonitored play fall below it linearly under (ii).
(f) Existing code with a behavior interface; under 10 core-hours.

### C7. Lemma `lem:private-monitor` (false switch probability at most (2 n^3)^(-1) when every primary target is at least tau; cumulative charge A_q >= q tau minus 1 minus 2 b_n(q))

(a) Anytime bound.
(b) The suites record `fallback` under S_star (0 of 1,440 performance runs and 0 of 2,520 profile incentive runs).
(c) Establishes only that no false switch occurred in about 4,000 paths, consistent with any probability below about 10^(-3).
(d) Cannot verify (2 n^3)^(-1) by simulation. The appendix sentence "They do not establish ... a zero false-switch probability" is accurate. Note that the strategic winner under S_star delivers exactly tau, so the monitored martingale has zero drift; the honest winner in honest_top delivers .75 above tau about .59, so it has large slack.
(e) Two cheap complements: (i) a boundary-crossing study with zero drift (the winner delivers exactly tau) for the boundary b_n(r) and for the ablated boundary without the log(2 n^4) factor (for example sqrt(r log n / 2) or a windowed test), reporting the empirical crossing probability with Wilson intervals over 10^5 vectorized paths; (ii) a detection-delay study: under constant shade epsilon, the empirical switch time against the analytic log(2 n^4) / (2 epsilon^2), which I verified against the existing data qualitatively (see C4). Both belong in the supplementary material and cost minutes when vectorized over paths.
(f) New vectorized code; about 1 core-hour.

### C8. Lemma `lem:selected-reactive-exp3` and the fresh-restart rationale (fallback revenue at least v H minus R_K(H) against arbitrary nonanticipating behavior of the other agents; restart retains an honest comparator)

(a) Conditional regret bound with explicit R_K(H) = 3 sqrt(K H log K) + 2 K log K.
(b) Fallback happens only under deviations in the incentive suite (bait-and-switch and shading in unique_top, near_gap, and about half of tied_top paths). Fallback length and the focal's utility are recorded; fallback revenue relative to V_i H is not reported.
(c) Establishes that fallback is long when triggered (about 14,000 to 15,000 rounds at n = 20,000 in unique_top) and that the deviator's utility falls.
(d) Does not report fallback regret against the comparator, so R_K(H) (which is 676 at H = 15,098 with K = 3, about 4.5 percent of H) is never compared with the observed loss. Does not compare fallback rules (fresh EXP3 versus UCB versus permanent exclusion versus warm-started EXP3), which is the ablation reviewers will ask for.
(e) Fallback-rule ablation under the joint adversarial profiles of C6 and under unilateral fallback-phase deviations: metric fallback revenue per round minus V_i (or minus mu_H^star), with R_K(H) / H overlaid; also the deviator's fallback utility for fresh versus warm-started EXP3 (warm start inherits Stage-2 statistics and is the "not fresh" ablation).
(f) Existing EXP3 loop (about 10 microseconds per round); under 10 core-hours.

### C9. Theorem `thm:finite-context` (finite-context UCB: contextual sharp adaptivity O(sqrt(|R| n log n)), monotonicity, exact FATA, robustness O(K sqrt(Q n log n)), and the public S_F equilibrium)

(a) Learning and incentive properties on a finite profile set.
(b) Contextual performance, finite family (K = 2, d = 1, nine profiles), all-maximum play only, regret per round .0308 and .0207 at n = 2,000 and 8,000 for exact finite-context UCB (which coincides with Grid-UCB at this width, as the identical numbers show).
(c) Establishes the learning behavior under S_max in one nine-profile instance.
(d) No incentive test of any kind; the public S_F equilibrium (two top agents at every profile) is untested; the instance has a unique top agent at every profile (capacities .40 + .22 parity + .04 i), so the equilibrium theorem's hypothesis does not even hold there.
(e) S_F exploitability of finite-context UCB by the same one-dimensional-per-profile search as C3 (a fixed map is a vector of Q targets; because instances are independent across profiles, the best response decomposes profile by profile); one tied-top finite instance and one unique-top finite instance. Supplementary material.
(f) Existing CellUCB code; about 5 core-hours.

### C10. Theorem `thm:grid-ucb-robust` (Static Grid-UCB: P(n) >= E sum b(X_t) minus O(n^((D+1)/(D+2)) (log n)^(1/(D+2))) uniformly over S_HDS)

(a) Robustness only, against the honest benchmark b(X).
(b) Contextual performance: Grid-UCB oracle regret against the delivered-capacity oracle (not against b(X)) under S_max; `honest_shortfall` (against the best intrinsic mean) is recorded but negative everywhere because all agents deliver capacity, so it is uninformative.
(c) Establishes learning performance under S_max in the linear, smooth, checkerboard, and finite families at D = 2 and 6 with K = 2, and the grid-width sensitivity at one horizon.
(d) Does not test robustness under non-maximum S_HDS profiles (where b(X) is the relevant benchmark) and cannot estimate the rate exponent from two horizons. The K = 2 restriction means every continuous cell has a two-agent bandit, which flatters all methods relative to K = 3.
(e) Low priority: a robustness sweep under mixed fixed maps (one honest agent at mu, strategic agents shading) reporting (E sum b(X_t) minus P(n)) / n^((D+1)/(D+2)) versus n. If page budget forces a choice, drop this in favor of C11 and C12.
(f) Existing code; about 20 core-hours at K = 3 and n up to 32,000 because the cell-local loops are in Python (about 60 microseconds per round).

### C11. Theorem `thm:grid-etc` (Static Grid-ETC: contextual sharp adaptivity O(n^((D+2)/(D+3)) + n nu((partial R)^(sqrt D h_n))), robustness O(n^((D+2)/(D+3))), exact pathwise monotonicity, expected FATA)

(a) Rates plus two structural properties.
(b) Contextual performance (Grid-ETC regret under S_max, ignoring post-exploration feedback per the tests) and, indirectly, the contextual incentive suite.
(c) Establishes regret under S_max at two horizons and that the implementation ignores exploitation feedback (tests `test_gridetc_exploration_blocks` and `test_celletc_exploration_count_and_ignored_feedback`).
(d) Monotonicity is claimed exact and pathwise under the common-uniform coupling, which is directly checkable by simulation (raise one agent's map to M_i, hold all uniforms and permutations fixed, assert T_j never increases, for all j not equal i, on every path) and has not been checked. FATA is not measured. The ETC ablation "ignoring exploitation rewards" is untested (a variant that keeps updating after commitment would be more efficient but loses the phase-independence that the proof uses).
(e) A pathwise monotonicity assertion test (thousands of coupled paths, zero violations expected; a single violation would be a bug in either code or theorem) plus an ablation comparing Grid-ETC with a "keep updating" variant under S_max and under the phase-dependent stress deviation of C12; the latter is where ignoring exploitation rewards matters (a rule that keeps updating can react to post-commitment shading; ETC by design cannot).
(f) Existing GridETC class; about 5 core-hours.

### C12. Theorem `thm:contextual-public` (continuous public restricted equilibrium under Static Grid-ETC for S_HDS, including independent ex ante mixtures, with revenue E sum M_star(X_t) minus o(n))

(a) Equilibrium within fixed measurable maps under a structural top-set assumption.
(b) Contextual incentives: five fixed maps at three horizons; Figure 1(b) of the paper.
(c) Establishes that these five maps are costly at n = 32,000 (gains per round between minus .0089 and minus .0234) and profitable at 2,000 and 8,000 (up to .024 per round), in an instance where the top set is {0,1} on the entire cube.
(d) It does not estimate in-class exploitability, and it is dominated by forced exploration (63 to 91 percent of rounds), so the sign change at 32,000 mostly reflects the exploration share falling, not commitment dynamics at scale. The instance does not exercise the theorem's separator structure, contrary to the appendix sentence (BASELINE finding 3). It does not test independent ex ante mixtures beyond one random map. The paper's claim "all five ... are costly at n = 32,000" is correct for the data.
(e) Exact in-class best response. Conditional on a fixed map, Grid-ETC sees only each cell's conditional average target m_bar_{i,C} (Lemma `lem:cell-law`), exploration choices do not depend on rewards, and the deviator's expected utility per pull in a cell is 1 + mu_bar_{i,C} minus m_bar_{i,C}. Hence the deviator's problem decomposes into independent one-dimensional problems per cell: choose m_bar in [0, M_bar_{i,C}] to maximize (q_n + p_C(m_bar) E[(V_C minus K q_n)_+]) (1 + mu_bar_{i,C} minus m_bar), where p_C(m_bar) is the exact commitment probability (a polynomial in m_bar computable from K binomials with q_n trials and the priority rule) and V_C is Binomial(n, nu(C)). This is exact up to the one-dimensional maximization, which can be certified on a fine grid with a derivative bound, and it costs seconds for any n (216 cells at n = 32,000; even n = 10^6 has only about 1,000 cells at D = 3). So the exact S_HDS exploitability curve of Grid-ETC can be plotted from n = 10^3 to 10^6 or beyond, in a corrected instance with a real separator (two top-stable components with different top pairs, for example capacities that swap the second top agent across x_1 = 1/2 while staying continuous, which requires the third agent to tie at the boundary; Scout A2 is asked to specify one within the theorem's hypotheses). Separately and clearly labeled out of scope: the phase-dependent deviation (deliver M_i during exploration, shade after commitment), which the appendix itself says breaks the proof; it gains linearly under Grid-ETC and is the honest way to show what the S_HDS restriction excludes, and comparing Grid-UCB under the same stress behavior is informative because Grid-UCB keeps updating.
(f) New short code (exact per-cell computation) plus the existing GridETC for the stress test; under 5 core-hours.

### C13. Prose claims in `sections/experiments.tex` and `sections/appendix_experiments.tex`

- experiments.tex line 4, "Every scalar instance contains an honest agent": true for both scalar suites (checked).
- experiments.tex line 4, replication counts: match the CSVs (120/240, 100, 240).
- experiments.tex line 13, "the normalized gain from underbidding decreases with the horizon": true in unique_top; mechanism is L_n / n scaling (Section C4). "bait-and-switch is costly and triggers a long fallback": true. "primary shading eventually becomes costly": true for .05 at 20,000 (detection delay crosses N_n). "all five fixed ex ante map deviations are costly at n = 32,000": true.
- experiments.tex line 23, "LinUCB benefits from correct linear structure, whereas the grid rules perform better in the checkerboard stress test and deteriorate as D = Kd grows": true at D = 2 (checkerboard: Grid-ETC .0433, Grid-UCB .0460, LinUCB .0487 at 8,000); at D = 6 checkerboard LinUCB (.0755) beats both grids (.0834), so the sentence should be read as D = 2 only, which the caption states.
- appendix line 5, "18,360 scalar-incentive method runs": true, but 720 of them are exact duplicates (nontop_win_underperform equals bait_switch row for row; verified 720 of 720 identical in utility and reward).
- appendix line 7, "less than 30 minutes of wall-clock time": unverified on the original host; the baseline Slurm reproduction took 22.5 minutes on 4 cores. "timed learner calls total 131 seconds for scalar performance and 483 seconds for contextual performance": the contextual number was measured under three-way parallelism (BASELINE finding 5).
- appendix line 10, "assertions verify that the three phases sum to n on every path": only `scalar_incentives/run.py` asserts it (line 119); the performance suite does not (BASELINE finding 2). The same function also asserts nonnegative cumulative effort (line 120), which is a false invariant of the model (negative effort is allowed) that happens not to fire at the retained horizons.
- appendix line 10, the quoted numbers .0044, .0094, minus .114, minus .280, minus .409, 36.3 percent, minus .091: all reproduce (BASELINE) and I re-derived .0044 and .0094 above.
- appendix line 28, quoted contextual regrets: reproduce.
- appendix line 39, "a closed null separator with finitely many complementary components, and exactly two tied top agents on each component": the instance has the same top set on both sides of the separator, so the separator is vacuous (BASELINE finding 3); the sentence is technically true and materially misleading.
- appendix line 39, "the fifth is independently drawn and then held fixed": true.
- The Section 1 caption "Paired utility gain per round" and the appendix "paired-seed": partially inaccurate for underbid deviations (Finding F1 below).

## 3. Findings on the current suites (severity per COMMON.md)

F1 (P2, statistics and wording). `scalar_incentives/run.py` lines 98 to 99: bids are drawn with `rng.binomial(ell, bid_m)` on the whole vector. When the focal agent underbids, its binomial parameter changes, the generator consumes a different number of underlying draws, and every later draw (the other agents' bids, the primary stream, fallback coins) desynchronizes. Measured consequence: for underbid_05 in unique_top the price tau equals the profile run's tau in only 74, 91, and 92 percent of "paired" rows at the three horizons (77, 81, 88 percent for underbid_15); in near_gap 31 to 36 percent. For honest_top and low_gap_nontop the focal agent sets the price, so a changed tau is expected and not a defect. The estimates remain unbiased (each marginal law is correct) but the "paired common-random-number" description in the code docstring and the paper is only true for the primary and fallback phases, and the variance of the underbid contrasts is larger than a true pairing would give. Repair: pre-draw one uniform tape per (agent, pull index) and set Y = 1{U <= m}, which is the coupling used in the proof of the theorem; this also makes the bidding coupling argument directly visible in the data.

F2 (P2, evidence). The tested deviations are far from the best in class (Section C4); Figure 1(a) understates exploitability. The plotted underbid gain is the theorem's L_n term realized; stating this turns a weak-looking plot into a tightness statement. The best in-class deviation must be computed, not guessed (Scout A2).

F3 (P2, evidence). `nontop_win_underperform` duplicates `bait_switch` (BASELINE finding 1; confirmed row by row). The intended behavior, a non-top agent that wins by luck and then delivers its own capacity M_i rather than 0, is the interesting one: in low_gap_nontop tau is about .80 minus s_n = .69 < M_1 = .795, so such a winner is never detected and its utility equals the profile's. The theorem's non-top case only bites once 2 s_n < delta_i / 2 = .0025, which needs L_n beyond 10^7; the instance is therefore pre-asymptotic at every feasible horizon, which is worth saying rather than hiding behind a mislabeled deviation.

F4 (P2, evidence). The contextual incentive suite is exploration-dominated (Section 1.4); its sign pattern is an artifact of the exploration share falling from 91 to 63 percent, and the instance does not exercise the separator (BASELINE finding 3). Repair: the exact per-cell computation of C12 in a corrected instance, with the exploration share reported.

F5 (P3, consistency). Instance names unique_top, tied_top, near_gap denote different intrinsic means in the two scalar suites (BASELINE finding 7); mu_3 of the honest agent differs (.35 versus .40, .45, .50). Any merged figure must use one instance table.

F6 (P3, fidelity). Capacity UCB and context-blind UCB use fixed index-order initialization; the manuscript's UCB uses a uniform random order and independent uniform tie-breaking (Section 3). This does not affect the performance comparison materially but matters for any FATA test (C2) and should be an explicit ablation ("symmetric initialization").

F7 (P3, wording). Runtime and "less than 30 minutes" (BASELINE findings 5 and 6). Any runtime claim in the revision must come from a single-process measurement on a named node with pinned versions.

F8 (P3, code). `scalar_incentives/run.py` line 120 asserts nonnegative cumulative effort; false invariant (BASELINE). Remove or change to a bookkeeping identity.

F9 (P3, scope). All continuous contextual performance cells use K = 2 (BASELINE finding 4) while the incentive suite uses K = 3; the paper's text speaks of D = Kd without saying K = 2. Use K = 3 throughout the revision or state K.

F10 (P3, evidence category). No experiment is non-synthetic. The introduction motivates the model with crowdsourced classification, and the experiments section does not say that every environment is synthetic Bernoulli; a reviewer will notice. The revision must label evidence categories explicitly (COMMON.md rule 4).

## 4. Analytic facts that shape the new package (derived here, to be re-verified in the pilot)

A1. Bang-bang best responses in MESP. For a unilateral deviator, expected per-pull utility 1 + mu_i minus m and the Bernoulli transition law are affine in the target m, so in every phase and at every information state an optimal target is an endpoint of the feasible interval. Consequences: (i) exact backward induction over the deviator's information state needs only two actions, so no target-grid approximation error arises; (ii) private randomization cannot help; (iii) the best response in Stage 2 is a threshold policy in the slack Z_r minus r tau. Pilot check: compare the DP value with the best of a family of randomized-grid policies on the same instance (the DP must dominate) and with the hand-picked deviations (the DP must dominate each measured gain within its interval).

A2. The L_n term of the bound is attained: a unique top agent with slack M_top minus M_(2) > 2 s_n gains L_n (slack minus margin) minus o(L_n) by underbidding, as the current data confirm to within noise. The theorem's rate is therefore tight for MESP; a revision could say so (a matching lower bound is a one-paragraph argument for Agent B, not for me).

A3. The b_n term is nearly attainable by boundary hugging, so the in-class exploitability at n = 20,000 should be of order (L_n slack + c b_n(N_n)) / n, roughly .01 to .03 per round in unique_top, versus .0044 shown now. The exact DP will settle the constant.

A4. Detection delay of a constant shade epsilon under the cumulative monitor is about log(2 n^4) / (2 epsilon^2) primary rounds (6,200 to 8,100 for epsilon = .05, 690 to 900 for .15 at the tested horizons), consistent with every switch pattern in `trials.csv` (shade .05 undetected at N = 1,022, 14 percent detected at N = 5,414, always detected at N = 15,098).

A5. False switches under S_star cannot be observed by simulation (bound (2 n^3)^(-1)); only the boundary-crossing study with zero drift (C7) can show the margin the boundary leaves.

A6. Grid-ETC exploitability within S_HDS decomposes cell by cell into one-dimensional problems and is exactly computable for any n; the current suite's 63 to 91 percent exploration share means the tested horizons are far from the regime the theorem describes, and the exact computation can reach that regime at no cost.

A7. For fixed-map classes (S_HI, S_F, S_HDS) the best response is low-dimensional (one target per agent per profile or cell); for the behavioral class B_{i,n} it is a finite-horizon MDP with a small state. In neither case does a searched best response prove equilibrium; it is exact exploitability when the DP is exact and a lower bound otherwise (COMMON.md rule 5).

## 5. Gap summary

| Claim | Current evidence | Evidence category | Missing experiment (priority) |
|--|--|--|--|
| C1 sharp robustness | none | n/a | UCB robustness sweep (low) |
| C2 UCB SAMF | none (capacity UCB under S_max only) | synthetic | monotonicity and FATA panel, symmetric-initialization ablation (medium, supplementary) |
| C3 public UCB equilibrium and two-top necessity | none | n/a | exact S_HI exploitability of UCB, tied versus unique top (high, cheap) |
| C4 MESP behavioral equilibrium | 6 hand-picked deviations, 5 instances | synthetic | exact DP exploitability over B_{i,n} with certified fallback bracket; learned lower bounds at large n (highest) |
| C5 MESP revenue | S_star reward versus fixed-behavior comparators | synthetic | revenue decomposition and mechanism ablations; revenue versus exploitability scatter (high) |
| C6 MESP robustness | none | n/a | joint adversarial profiles across mechanism variants (high) |
| C7 monitor false switch and charge | 0 of about 4,000 switches | synthetic | zero-drift boundary study; detection-delay check (medium, supplementary) |
| C8 EXP3 fallback lemma and fresh restart | fallback length only | synthetic | fallback-rule ablation with R_K(H) overlay (high, part of ablation suite) |
| C9 finite-context UCB | finite family regret, K = 2 | synthetic | S_F exploitability in tied and unique top finite instances (medium, supplementary) |
| C10 Grid-UCB robustness | S_max regret at D = 2, 6, K = 2 | synthetic | robustness under mixed maps (low) |
| C11 Grid-ETC SAMF | S_max regret; feedback-ignoring tests | synthetic | pathwise monotonicity assertion; keep-updating ablation (medium) |
| C12 continuous public equilibrium | 5 fixed maps, vacuous separator, exploration-dominated | synthetic | exact per-cell S_HDS exploitability to n = 10^6 in a corrected instance; labeled phase-dependent stress test (highest for the contextual part) |
| Non-synthetic dependence | none | n/a | real labeled tasks with algorithmic providers and a compute-effort knob (real outcomes, scripted strategies), or crowd-calibrated simulator (high; Scout A1) |

## 6. What the current package can and cannot say (for the revision text)

Can say: MESP behaves as specified under S_star with no observed false switch; the tested deviations behave as the proof mechanisms predict (underbidding saves exactly the Stage-1 effort L_n times the underbid, constant shading is detected after about log(2 n^4) / (2 epsilon^2) rounds, bait-and-switch triggers a long fallback); the finite-horizon revenue shortfall is dominated by KL_n / n and s_n; grid rules beat context-blind UCB and lose to LinUCB under correct linear structure at D = 2; five fixed contextual maps are costly at n = 32,000.

Cannot say: anything about in-class exploitability (no best response was computed), about joint behavioral robustness, about the two-top condition, about false-switch rates, about fallback regret relative to R_K(H), about the separator structure of Theorem `thm:contextual-public`, or about any non-synthetic setting.

## 7. Commands used for the checks in this document

All run from `scratch/experiments/final/` with the session venv's Python and pandas, read-only:

- design constants: the `design(n, k)` formula of the suites evaluated at n in {200, 500, 1000, 2000, 8000, 20000, 50000, 100000}, K = 3; b_n(N) = sqrt(N log(2 n^4) / 2); detection delay log(2 n^4) / (2 epsilon^2); R_3(N) = 3 sqrt(3 N log 3) + 6 log 3.
- pairing check: join `scalar_incentives/trials.csv` deviation rows to profile rows on (instance, n, seed); fraction with `np.isclose(tau, tau_profile)`.
- analytic underbid saving: L_n times underbid divided by n against `paired_summary.csv` focal_utility mean divided by n.
- duplicate check: join bait_switch and nontop_win_underperform rows on (instance, n, seed); 720 rows, all equal in focal_utility and platform_reward.
- exploration share: `contextual_incentives/trials.csv`, mean of exploration_rounds divided by n, per n.
