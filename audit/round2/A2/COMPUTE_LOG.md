# Compute log, package A2 (contextual mechanisms), 24 September 2026

All Slurm work ran on the cluster's `cpu` partition under the project account. No GPU was used. The login node was
used only for smoke tests of a few seconds, for the analytic threshold tables of `ctx_local/continuous.py`
(which contain no simulation and run in under two seconds), for aggregation and for figures. One timing
calibration of the exact solver at `n = 8000` ran detached on the login node for 128 seconds before the grid
was sized; it is recorded here rather than omitted.

Scripts are under `scratch/experiments/round2/ctx_local/` and `scratch/experiments/round2/figures/`; Slurm
wrappers, raw outputs, logs and CSVs are under
`<scratchpad>/round2/A2/{slurm,results,logs,csv,figures}`.

## Submissions

| job id | name | script | what | walltime requested |
|:--|:--|:--|:--|:--|
| 64818660 | x_rut_small | slurm/exact.sh | exact grid, replicated_unique_top, n = 2000/8000/20000, Q = 1..6 | 24:00:00 |
| 64818661 | x_rtt_small | slurm/exact.sh | exact grid, replicated_tied_top, same cells | 24:00:00 |
| 64818662 | x_rk2_small | slurm/exact.sh | exact grid, replicated_K2_unique, Q = 1..8 | 24:00:00 |
| 64818663 | x_rng_small | slurm/exact.sh | exact grid, replicated_near_gap, Q = 1..6 | 24:00:00 |
| 64818664 | x_rut_50k | slurm/exact.sh | exact grid, replicated_unique_top, n = 50000, Q = 1..7 | 24:00:00 |
| 64818665 | x_rtt_50k | slurm/exact.sh | exact grid, replicated_tied_top, n = 50000, Q = 1..7 | 24:00:00 |
| 64818666 | x_rk2_50k | slurm/exact.sh | exact grid, replicated_K2_unique, n = 50000, Q = 1..10 | 24:00:00 |
| 64818667 | x_rot | slurm/exact.sh | exact grid, rotating_top, n = 2000..50000, Q = 1..6 | 24:00:00 |
| 64818668 | x_het | slurm/exact.sh | exact grid, heterogeneous, n = 2000..50000, Q = 1..6 | 24:00:00 |
| 64818669 | x_unb | slurm/exact.sh | exact grid, unbalanced_unique_top, n = 2000..50000, Q = 1..6 | 24:00:00 |
| 64818673 | x_rut_200k_hi | slurm/exact.sh | exact grid, replicated_unique_top, n = 200000, Q = 5..10 | 20:00:00 |
| 64818674 | x_rut_200k_q4 | slurm/exact.sh | exact grid, replicated_unique_top, n = 200000, Q = 4 | 36:00:00 |
| 64818675 | x_rut_200k_q3 | slurm/exact.sh | exact grid, replicated_unique_top, n = 200000, Q = 3 | 36:00:00 |
| 64818676 | x_rtt_200k_hi | slurm/exact.sh | exact grid, replicated_tied_top, n = 200000, Q = 5..10 | 20:00:00 |
| 64818677 | x_rk2_200k | slurm/exact.sh | exact grid, replicated_K2_unique, n = 200000, Q = 8..14 | 20:00:00 |
| 64818678 | x_rot_200k | slurm/exact.sh | exact grid, rotating_top, n = 200000, Q = 5..10 | 20:00:00 |
| 64818679 | x_rut_1M | slurm/exact.sh | exact grid, replicated_unique_top, n = 1000000, Q = 12..16 | 36:00:00 |
| 64818680 | x_rtt_1M | slurm/exact.sh | exact grid, replicated_tied_top, n = 1000000, Q = 12..16 | 36:00:00 |
| 64818723 | l_rut_sm | slurm/ladder.sh | contextual ladder, replicated_unique_top, n = 20000/50000, Q = 1/2/3/6, 200 reps | 16:00:00 |
| 64818724 | l_rtt_sm | slurm/ladder.sh | contextual ladder, replicated_tied_top, same cells | 16:00:00 |
| 64818725 | l_rot_sm | slurm/ladder.sh | contextual ladder, rotating_top, same cells | 16:00:00 |
| 64818726 | l_het_sm | slurm/ladder.sh | contextual ladder, heterogeneous, same cells | 16:00:00 |
| 64818727 | l_rut_200k | slurm/ladder.sh | contextual ladder, replicated_unique_top, n = 200000, Q = 1/3/6, 100 reps | 20:00:00 |
| 64818728 | l_rot_200k | slurm/ladder.sh | contextual ladder, rotating_top, n = 200000, Q = 1/3/6, 100 reps | 20:00:00 |
| 64818742 | v_8000 | slurm/validate.sh | validation V1 to V5 at n = 8000, 200 replicates | 06:00:00 |
| 64818743 | v_20000 | slurm/validate.sh | validation V1 to V5 at n = 20000, 200 replicates | 06:00:00 |
| 64818779 | cg_struct | slurm/cg.sh | CG-MESP structural regime, oscillation sweep, tuned regime | 08:00:00 |

## Submissions added later the same day

| job id | name | script | what | walltime requested |
|:--|:--|:--|:--|:--|
| 64818834 | x_rot_1M | slurm/exact.sh | exact grid, rotating_top, n = 1000000, Q = 12..14, the first cells at which the non-top branch condition 4 s_n <= 0.15 holds | 36:00:00 |
| 64818850 | x_reg | slurm/exact.sh | exact grid, regime_switch, n = 2000..50000, Q = 2/4/6 | 24:00:00 |
| 64818851 | x_reg_200k | slurm/exact.sh | exact grid, regime_switch, n = 200000, Q = 2/4/6/8 | 24:00:00 |
| 64818852 | l_reg | slurm/ladder.sh | contextual ladder, regime_switch, n = 20000/50000, Q = 2/4/6, 200 reps | 20:00:00 |
| 64818853 | l_reg_200k | slurm/ladder.sh | contextual ladder, regime_switch, n = 200000, Q = 2/4, 100 reps | 20:00:00 |
| 64818854 | l_hon | slurm/ladder.sh | contextual ladder, replicated_honest_top, n = 20000/50000, Q = 1/2/3, 200 reps | 16:00:00 |
| 64818893, 64818894 | s_unique, s_tied_t | slurm/search.sh | first deviation search, narrow delta grid; superseded and cancelled | 12:00:00 |
| 64818986, 64818987, 64818988 | sw_* | slurm/search.sh | second deviation search, wide delta grid; superseded and cancelled after the comparison correction of the report's Section 13 | 12:00:00 |
| 64818914, 64818915 | v2_8000, v2_20000 | slurm/validate.sh | validation with the corrected comparisons, 400 replicates | 06:00:00 |
| 64819582 to 64819585 | sv_* | slurm/search.sh | deviation search with the value comparison and the wide delta grid, four families | 12:00:00 |

The cancellation of the first two search arrays failed silently: `scancel` was called with repeated `-n NAME`
options, which Slurm does not accumulate, so only the last name was cancelled. Jobs 64818893 and 64818894 ran
to completion and wrote `search_*.csv` files in the superseded form; those files are quarantined under
`results/search_superseded/` and the aggregator reads only `results/search/`. Jobs 64818986 and 64818987 were
then cancelled by job id.

Two search arrays were superseded and re-run rather than patched: the first because its `delta` grid topped out
at 0.5 while the certified optimum shades to the feasible floor, and the second because its acceptance
comparison subtracted a simulated baseline from an exact bound. Both are recorded in Section 13 of
`EXPERIMENT_REPORT.md` with their numbers.

## Note on the repository state

No `git` state-changing command was run by this package. A commit made elsewhere on the branch at 14:21 UTC on
24 September swept this package's files in; that commit was not made here.

## Login-node work

| what | tool | duration |
|:--|:--|:--|
| timing calibration of the exact solver at n = 8000, Q = 1 and 2 | ctx_local/plmesp_exact.py | 128 s, detached |
| analytic threshold and degeneracy tables | ctx_local/continuous.py | under 2 s |
| aggregation into CSVs | ctx_local/aggregate.py | seconds |
| figures | figures/make_figures_a2.py | seconds |
| smoke tests of the simulator and of the ladder | ctx_local/ctxmech.py | seconds each |

## Seeds

The exact computations use no randomness at all: they are backward inductions over exact binomial laws on a
deterministic arrival path, so no seed enters them.

The simulations use `scratch/experiments/round2/common/seeds.py` unchanged:
`SeedSequence([20260828, SUITES[suite], PHASES[phase], instance_index, n, rep])`, with
`suite = "contextual_incentives"` (id 4). The ablation ladder uses `phase = "final"` (id 1); the validation
runs use `phase = "pilot"` (id 0); `instance_index` is `1000 * (family rank + 1) + Q` for the ladder and
`7777 + Q` or `8888 + Q` for the two validation blocks. No seed used by the scalar package (suites 1, 2, 6, 7)
is reused, and the pilot and final phases are disjoint by construction.

## Accounting

To be completed when the last job exits; the running total is recorded in `EXPERIMENT_REPORT.md` Section 9.
