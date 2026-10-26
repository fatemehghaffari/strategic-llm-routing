# Experiment final report (Agent A, experiments lead, 18 September 2026)

Package P1 as approved. This report states what was built, what was measured, what each measurement supports, and
what it does not. Detailed acceptance values and the record of every decision taken after seeing data are in
`PILOT_REPORT.md`; every Slurm submission is in `COMPUTE_LOG.md`; the code is on branch `scout/A` of the worktree
`wt-A` under `scratch/experiments/round2/`, and no canonical file was modified.

Evidence categories, used throughout and never mixed: exact computation (no sampling error, stated class and
instance), synthetic paired simulation, and real labeled tasks with real provider answers and a scripted effort
choice. No experiment in this package is deployment evidence, offline evaluation of logged decisions, or evidence
about human behavior. Searched best responses are lower bounds on exploitability for the class searched; exact
computations are exploitability within a declared class; nothing here is proof of equilibrium.

## 1. What was built

| component | code | what it computes |
|--|--|--|
| Shared mechanism | `common/design.py`, `common/mechanism.py`, `common/instances.py`, `common/seeds.py`, `common/stats.py` | one definition of L_n, N_n, s_n, b_n, the EXP3 and grid constants, the UCB index options and the theorem constants; a tape-coupled MESP simulator with 12 mechanism variants and the behavior classes; one instance table; the seed scheme; t, BCa and Clopper-Pearson intervals |
| Exact exploitability | `exploitability/dp.py`, `validate_dp.py`, `aggregate.py` | exact best response of a unilateral deviator against MESP over B_{i,n} under the information structure I0 plus the announced price, with the fallback bracketed; validation against the simulator; grid aggregation and the acceptance check |
| Searched best response | `exploitability/search.py` | CMA-ES over a phase-scaled threshold class and over an interior-target class, as an independent check |
| Baselines and ablations | `ablations/run_ladder.py` | 12 mechanism variants under 12 behavior profiles, including joint adversarial profiles |
| Exact contextual | `contextual_exact/exact_etc.py`, `run_exact.py`, `monotonicity.py` | exact in-class (S_HDS) exploitability of Static Grid-ETC by cell decomposition, three grid rules, the out-of-scope stress tests, and the pathwise monotonicity check |
| Public UCB | `public_ucb/run.py` | grid-resolved S_HI exploitability, FATA, and the index and tie-rule comparison |
| Provider bank | `provider_bank/` | real labeled tasks answered by frozen scikit-learn providers with an inference-compute knob, driven through the shared mechanism |
| Figures | `figures/make_figures.py` | the four-panel main figure, vector PDF |

Tests: `scratch/tests/`, 200 passed and 8 skipped (the 8 are 2 inherited skips and 6 provider-bank tests that need
an environment variable pointing at the bank artifacts). Every new module's tests were written before the module.

## 2. Core results

### 2.1 Exact exploitability of MESP (exact computation, synthetic instances)

The deviator's one-step objective is affine in its target, so an optimal target is an endpoint and a two-action
backward induction over its information state is exact for Stages 1 and 2, with no target grid and no
discretization error. The fallback is bracketed between a continuation of zero and the appendix's own EXP3 bound.
98 runs covering 96 distinct cells: five named instances to n = 50,000, K = 2 instances to 20,000, an eleven-point capacity-gap grid, and
three structural variants.

- Per-round certified bounds decay over the n^(2/3) branch of L_n in every instance, with log-log slopes between
minus 0.25 and minus 0.51, which is the predicted mixture of the Stage-1 term (slope minus 1/3 up to logs) and the
Stage-2 term (minus 1/2). At n = 50,000 in the unique-top instance the certified interval is [0.0324, 0.0361] per
round against the revised top-agent constant 0.1283 (the lower bound is 0.032448, and a certified interval is
rounded outward, never inward).
- At every horizon where the conservative price is non-degenerate, the optimal in-class Stage-2 deviation
extracts the entire monitoring slack on the histories where it wins the bidding: the Stage-2 gain equals b_n(N_n)
times the probability of winning Stage 1, to within 0.001 in 73 of the 96 distinct cells, 0.005 in 84 and 0.01 in 88. All
eight exceptions are at n = 200 or n = 500, the horizons at which s_n is 0.40 to 0.59 and the announced price
collapses (mean price given a win of 0.07 to 0.29), so the slack is no longer what binds. The b_n term of the
theorem is therefore attained on the winning histories wherever the mechanism is in its intended regime. An
earlier version of this report asserted the stronger and false statement that the ratio to b_n(N_n) is exactly
1.000 whenever the deviator always wins and exactly 0.500 in tied instances; across the 33 always-winning cells
the ratio actually runs from 0.527 to 1.002 and across the tied cells from 0.260 to 0.501, and the regularity
that does hold is the one stated here, which covers all 96 cells rather than two special cases.
- Adaptive Stage-1 underbidding, which stops delivering once the win is secured or hopeless, is worth 676 utility
at n = 50,000 against 245 for the best fixed underbid, so the hand-picked deviations in the current manuscript
understate finite-horizon exploitability by a factor of three to four.
- Exploitability grows monotonically with the capacity gap (0.0141 per round at a tie to 0.0405 at a gap of 0.20 at
n = 20,000, K = 3) while the theorem's top-agent constant does not depend on the gap.
- For a non-top focal agent the certified upper bound is uninformative and the proof's non-top branch condition
2 s_n at most delta_i / 2 fails at every horizon we can run; those instances are reported by their lower bound only.

### 2.2 Mechanism baselines and ablations (synthetic paired simulation)

2,304 cells: 12 variants, 12 behavior profiles, four instances, horizons to 50,000, 200 paired replicates.

- Best tested deviation per round at n = 20,000, in the three instances whose focal agent contests the bidding
(unique_top, tied_top, near_gap): no monitor 0.268 to 0.489, windowed monitor 0.059 to 0.113, every
anytime-monitored variant 0.006 to 0.012, the last being exactly the Stage-1 term of the best underbid. In the
fourth instance, honest_top, the focal agent is the strategic runner-up and essentially never wins Stage 1 at this
horizon, so no monitor is ever exercised and every variant including the unmonitored one shows only that same
Stage-1 term, 0.0123. Quoting a range over all four instances would therefore read 0.012 to 0.489 for the
unmonitored mechanism and hide the effect rather than show it; the conditioning is stated instead.
- False switches under the proposed profile: 0.0000 for every variant except the no-slack monitor. Its rate
depends on what the winner delivers, so it is reported per profile rather than pooled. Under the mechanism's own
proposed profile, where a compliant winner delivers exactly the announced price and the monitored walk has zero
drift, the no-slack variant fires on that compliant winner in 0.39 to 1.00 of replicates across the sixteen cells
(1.00, 0.99, 0.99 and 0.56 at n = 20,000). Under all-maximum play, where the winner delivers strictly above the
price and the walk has positive drift, it fires in 0.13 to 0.63 (0.21, 0.63, 0.43 and 0.56 at n = 20,000). The
zero-drift case is the one that shows why the boundary b_n(r) exists: without slack a compliant winner is
eventually convicted by ordinary noise.
- Detection delay under bait-and-switch and under shading matches log(2 n^4) / (2 (tau minus m)^2) at ratios 0.996
to 1.015.
- Under sequential joint shading the platform falls below mu_H^star for the round-robin fallback, the unmonitored
runner-up and the no-monitor variant, while MESP keeps 0.080 to 0.142 per round of headroom. This is the first
measured evidence for the robustness half of Theorem thm:private-mesp, which is a statement about arbitrary
behavioral profiles and which no previous experiment tested.
- The conservative price correction costs 0.05 to 0.085 per round of revenue and buys the false-switch rate above;
the 1/n confidence exponent recovers about half of that cost.

### 2.3 Fixed-map classes: contextual Grid-ETC and public UCB (exact computation and simulation)

- Exact in-class (S_HDS) exploitability of Static Grid-ETC, computed cell by cell, reaches exactly zero for a top
deviator in both environments by n = 128,000 to 512,000 under exact tiling, and 0.0199 per round at n = 2,000,000
for the mixed deviator that is non-top below the separator and top above. The out-of-scope count-based
explore-then-shade deviation grows to 0.23 to 0.27 per round over the same range.
- Two grid-geometry findings: the retained rule's clipped last cell creates thin cells that never finish exploring
and supply 100 percent of the in-class gain at n = 2,000,000; the dyadic rule over-refines so that K q_n J_n exceeds
the horizon at three of five horizons and the rule never commits at all. Exact tiling removes both.
- Grid-ETC's pathwise monotonicity: zero violations in 2,300 coupled paths.
- Public UCB: with a unique top agent the best fixed target is strictly interior (0.72 to 0.74 against a capacity of
0.90, specifically 0.7425 at n = 2,000 and 8,000 and 0.72 at 20,000) and gains 0.073, 0.102, 0.127 per round at
those horizons, a linear deviation; with two tied top agents
the best fixed target is the capacity itself and the gain is exactly zero at every horizon. The two-top condition
is the difference between a linear exploit and none.
- Index and tie rule: under the proof's fixed-priority coupling the known-horizon index gave zero monotonicity
violations in 240,000 coupled paths while the anytime index gave 59, at n = 8, 50 and 200. Under a fresh per-round
tie coin the known-horizon index gave 36 and the anytime index 103, so the per-round coin is not a monotone
coupling and no pathwise claim is made for it. A monotonicity claim must therefore name the index and the tie rule
together. These counts are from `public_ucb_monotonicity_bothties.csv`, which sweeps both rules; my own earlier
table recorded only the per-round default and so did not support the sentence that cited it (Section 6, item 7).
- FATA: the mean pull-share difference between two tied top agents is within noise of zero at every horizon and
under both indices. Symmetric and index-order initialization are indistinguishable at n at least 2,000 and separate
at n = 6, where index-order initialization gives an interval excluding zero.

### 2.4 The non-synthetic evaluation (real labeled tasks, real provider answers, scripted effort)

20,800 trials on two provider banks. The announced price lies inside the proof's band at a rate of 1.000 in every
cell, over 1,200 distinct prices (the four mechanism variants share one bidding stage, so a replicate count depends
on whether they are counted separately), and tracks M_(2) minus s_n to within 0.002 to 0.023 s_n. Zero switches and zero false switches in 4,800
proposed-profile replicates at the three gate horizons, but not at the largest horizon tested: at n = 200,000 on
Fashion-MNIST the monitored mechanism switched on a fully compliant winner in 3 of 100 trials (Clopper-Pearson
[0.006, 0.085]; 0 of 100 on Covertype). That is the real mechanism on real provider answers, so the measured
false-switch rate of the mechanism is not zero at every horizon, and the paper says so. The cause is measured: the
winner's fitted target equals the price to five decimals while its realized mean on the play half is 0.0092 lower,
a drift whose first-order crossing time, 295,818, is the same order as the 167,664 primary rounds. Lemma
lem:private-monitor bounds false alarms for an agent that truly delivers at least the price, and this agent does not,
so the measurement is a limitation of the evaluation's fitted targets and a real nonzero rate at once; it is not a
counterexample to the lemma and it is not an artifact of simulation. Full sabotage is detected in 3,318 of 3,318 focal wins with median
delay within 1.1 to 1.7 percent of the first-order formula computed at the real shortfall. The ablation separates
the mechanisms on real outcomes exactly as the synthetic ladder does: sabotage costs the deviator about 7,500
utility under the monitored mechanism and earns it about 10,000 without the monitor, where platform reward falls
below mu_H^star while the monitored mechanism stays above it. Under detected sabotage the platform's real compute
bill triples, a cost the model's effort convention does not express. At n = 200,000, on the partial-shading rows, the median
detection delay matches the first-order formula evaluated at the realized play-half rate (ratios 0.962 and 0.996)
and not the same formula evaluated at the rate the calibration fitted on the disjoint measurement half (0.124 and
0.916). Both columns are the same formula at two different rates; no simulator is involved. Every outcome in this
evaluation is a real provider answer to a real labeled task, and nothing anywhere in it is drawn from a Bernoulli
law. The gap between the two columns is the measurement half failing to transfer on one dataset, which is what
makes the realized-rate column the meaningful one.

### 2.5 The searched cross-check (lower bounds for the class searched)

CMA-ES over a phase-scaled threshold class and over an interior-target class, trained on training seeds, selected
on a validation block, and evaluated once on 2,000 held-out paired seeds. Six of eight cells completed; the two
bang-bang cells at n = 20,000 were still running and are reported as outstanding rather than estimated.

- No searched policy in any completed cell exceeded the certified upper bound. This is the check that would have
revealed an error in the dynamic program or in the bound, and it passes everywhere it was run.
- Interior-target policies reach 0.25 to 0.78 of the certified lower bound and never approach the upper bound,
which is the empirical form of the affinity argument that makes the two-action recursion exact.
- The threshold class reaches 0.966 of the certified lower bound at n = 2,000 in the unique-top instance and 0.926
in the tied-top instance. The residual gap is expected: the searched rule has a fixed shape while the exact optimum
has a time-varying threshold.

## 3. Claims the package supports, and claims it does not

Supported, with the evidence category in parentheses:

1. On each tested instance and horizon to 50,000, the supremum unilateral gain against MESP over the behavioral
class lies in a certified interval whose per-round value decays with the horizon and lies three to eight times
inside the theorem's explicit finite-n constant; the gain decomposes into adaptive Stage-1 underbidding of order
L_n and Stage-2 boundary tracking worth b_n(N_n) times the probability of winning the bidding (exact computation,
Stages 1 and 2 exact and the fallback bracketed; synthetic instances).
2. Where the focal agent contests the bidding, removing the monitor makes the mechanism linearly exploitable and a
windowed monitor leaves roughly an order of magnitude more exploitability than the anytime boundary; the conservative price buys a false-switch rate of zero at a revenue
cost of 0.05 to 0.085 per round; removing the fallback or leaving the runner-up unmonitored loses the honest
benchmark under sequential joint shading while MESP retains it (synthetic paired simulation).
3. Within the fixed-map class, Static Grid-ETC's exact exploitability vanishes with the horizon under a grid that
tiles the cube exactly, and phase- or count-dependent play outside that class gains linearly, as the theorem's
scope statement anticipates (exact computation and synthetic simulation).
4. Within the fixed-mean class, symmetric UCB is exploitable at a linear rate by a unique top agent and not at all
by a tied top agent; the known-horizon index is pathwise monotone under the proof's tie rule in every path tested
and the anytime index is not (grid-resolved exploitability and simulation).
5. On real labeled tasks answered by real providers with a compute knob, the mechanism's price stays inside the
band the proof states, the monitor detects scripted sabotage in every instance of it, the detection delay obeys the
first-order formula evaluated at the realized rate, and the honest-benchmark separation between the monitored and
unmonitored mechanisms reproduces (real outcomes, scripted effort). The false-switch rate is zero at the three gate
horizons and 0.03 of 100 trials on one dataset at n = 200,000, where the winner's realized mean drifts 0.0092 below
the price it was fitted to deliver; the package does not support a claim that the rate is zero at every horizon.

Not supported, and not to be written:

- Equilibrium, in any class, as an empirical fact. The exact computations bound exploitability within a declared
class on a fixed instance at a fixed horizon; the searched values are lower bounds for the class searched.
- Anything about instances, classes or horizons not computed, including uniformity as capacity gaps vanish. The
non-top branch of the private theorem cannot be exercised at any horizon we can run.
- Coalition-proofness. The joint profiles tested are specific and few.
- Any claim about human behavior, or about effort from crowd data. The provider bank's effort choice is scripted.
- Optimality of any constant in the mechanism, and any runtime claim beyond the pinned single-process measurements.
- That a positive finite-horizon gain contradicts an o(n) theorem, or that a decaying gain proves one.

## 4. Figures and tables proposed

Main paper, one four-panel figure (`figures/main_experiments.pdf`, vector, 7.1 inches wide, no embedded titles;
the palette is the Okabe-Ito subset already used by the retained suite and was checked with a colorblind-safety
validator, with every series carrying a marker and a line style as well as a legend entry):

- (a) certified exploitability band against the horizon for a unique-top and a tied-top instance, with the
theorem's constant and the searched lower bounds.
- (b) the mechanism ladder at n = 20,000: best tested deviation per variant, with the revenue gap printed beside
each row and the marker showing whether the honest benchmark survived joint shading. A scatter of the two measures
was tried and rejected because every monitored variant coincides in it.
- (c) exact in-class exploitability of Static Grid-ETC against the horizon, with the out-of-scope stress test drawn
separately and labelled as outside the class.
- (d) the provider bank: platform reward per round under the proposed profile and under sabotage, monitored and
unmonitored, against the second measured capacity and the best honest intrinsic mean.

Supplement: the ablation ladder table at n = 20,000; the instance table and design constants; the exact
exploitability grid with its decomposition and slopes; the capacity-gap grid; the contextual table for the three
grid rules with the exploration share; the index and tie-rule monotonicity table; the FATA table; the provider-bank
curves, the price-band table and the large-horizon exhibit; and the regenerated hand-picked deviation figure with
the analytic Stage-1 line overlaid.

## 5. Reproduction

Every result regenerates from the worktree with the pinned virtual environment. The exact commands are the Slurm
scripts in the scratchpad under `round2/A/slurm/` and the `run.py` calls they contain, each logged with its job id
in `COMPUTE_LOG.md`. Seeds derive from `SeedSequence([20260828, suite_id, phase_id, instance_index, n, rep])` with
pilot, final, train and evaluation phases disjoint by construction, so no pilot seed appears in any final table and
no training seed in any reported evaluation. Raw outputs stay in the scratchpad; only the summaries and the vector
figures the paper uses are intended for the repository, which keeps the supplementary archive inside its size
limit.

## 6. Risks and open items

1. Two searched cells at n = 20,000 did not finish inside this window. Their role was to confirm that no searched
policy exceeds the certified upper bound, which is already confirmed in every completed cell; the certified bounds
are the headline and the search is a cross-check, so the package does not depend on them. If they complete, they
extend the table; if they do not, the search is reported as covering the six completed cells only.
2. The certified numbers are only as good as the agreement between the dynamic program and the mechanism as
implemented and as stated. Five independent checks tie them together and all pass; the residual risk is a shared
misreading of the mechanism by both implementations, which the tests against the manuscript formulas reduce but do
not eliminate.
3. The provider bank exercises the near-tie regime only, and its effort-positive regime appears only at the
supplementary horizon. Both limitations are stated in the paper rather than worked around.
4. Calibrated compliance is not exact compliance: on real providers a monitor tuned to a finite measurement sample
eventually fires on a well-intentioned agent, which is what the three false switches at n = 200,000 show. This is a
limitation of the evaluation, not a counterexample to the lemma.
5. Two grid-geometry pathologies were found and one is in the retained implementation. The revision adopts exact
tiling; if that change does not reach the manuscript, the clipped-cell term must be stated.
6. No new experiment may run after 28 September 2026.

## 7. Compute accounting

All work ran on the cluster's `cpu` partition under the project account, with the login node used only for builds,
quick checks and figures. No GPU was used at any point, against a budget of 24 preemptible GPU-hours.

| component | jobs | core-hours |
|--|--|--|
| Exact dynamic program, full grid and the gap re-run | 64554035, 64555834 | about 23 |
| Ablation ladder, pilot and final | 64554052, 64556141 | 14.9 |
| Public UCB, including the failed and superseded runs | 64556140, 64556183, 64556295 | 0.2 |
| Contextual exact tables and checks | 64556296 and login-node work | about 1 |
| Provider bank, pilot and final | five jobs by worker E4 | 2.5 |
| Searched best response, including the cancelled mis-scaled array | 64556162, 64557037 | about 8 so far |
| Total | | about 50 of 2,000 core-hours |

The binding constraint throughout was calendar time and human review, not compute. Three runs were discarded and
re-run rather than patched: a public-UCB job that indexed a second top agent in a unique-top instance, a search
array whose policy class was parametrised on the wrong scale, and 33 dynamic-program cells whose output filenames
collided because instance aliases contain dots. Each is recorded with its diagnosis in `COMPUTE_LOG.md` and in
`PILOT_REPORT.md`.

## 8. Decisions taken after seeing data, and why each is an adjudication rather than a moved goalpost

Three acceptance criteria were changed or reinterpreted after results existed. Each is recorded here because the
record is what makes the change reviewable.

1. The provider-bank price gate. My criterion, that the mean price lie within s_n of the second measured capacity,
is algebraically equivalent to requiring the second order statistic of the empirical bids to exceed the second true
capacity, which four near-tied bidders fail about half the time. It was a mis-statement of the mechanism's
guarantee, not a threshold the data missed. The gate is now the band the proof states, and every cell passes it
with room.
2. The exploitability comparison for a non-top focal agent. I had compared the certified upper bound against the
top-agent constant for every instance. For a non-top agent the theorem gives different terms and its own finite-n
condition fails at every horizon we can run, so the comparison was invalid rather than failed. The aggregator now
derives the applicable constant from the instance table and marks those instances as lower-bound-only.
3. The monotonicity statement about the exact optimum. I first reported that the optimal rule is an interval in the
reward sum in both stages. Testing the lower threshold showed it is inert in Stage 2 and necessarily so, because
the monitor ends the phase the moment the cumulative slack goes negative. The interval structure is a Stage-1
phenomenon; the earlier, looser sentence was corrected rather than left to stand.

Two criteria were not changed when results were uncomfortable: the E1 acceptance test was reported as failing until
the main agent approved a resolution, and the provider-bank worker's NO-GO was carried to the main agent rather
than absorbed.
