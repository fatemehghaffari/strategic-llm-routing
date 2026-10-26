# Compute log, package A4

Cluster: a university HPC cluster. Partition `cpu`, account `<slurm-account>`.
Venv: `<scratchpad>/venv` (numpy 2.5.3, scipy 1.18.1, pandas 3.0.5, matplotlib 3.11.2,
scikit-learn 1.9.1, pytest 9.1.1). Scripts: `audit/round2/A4/scripts/`.
All Slurm scripts: `audit/round2/A4/scripts/slurm/`.

## Login-node work (smoke tests and data preparation only)

| what | command | wall clock |
|---|---|---|
| licence and metadata checks | `curl` against github.com, api.github.com, huggingface.co, arxiv.org | about 3 min total |
| dataset download | `curl` of the two pinned `.pkl` files | 7 s (2.3 s + 3.9 s) |
| `build_capabilities.py` | `python scripts/build_capabilities.py` | 41 s |
| `flips.py` | `python scripts/flips.py` | 96 s |
| `build_embeddings.py` | `python scripts/build_embeddings.py` | 48 s |
| `continuous_flips.py` | `python scripts/continuous_flips.py` | 119 s |
| `select_triples.py`, `analytic_gap.py` | as named | 4 s, 6 s |
| `pytest tests/` (44 tests) | `python -m pytest tests/ -q` | 3.5 s |
| engine smoke test, 1 config at n = 20,000, 2 seeds | `run_sim.py --configs /tmp/smoke.jsonl` | 134 s |
| monitor-ladder smoke, n = 20,000, 5 reps, 1 alpha | `monitor_ladder.py --n 20000 --reps 5` | about 5 min |

Nothing heavier than these ran on the login node.

## Slurm submissions

| job id | script | array | what | seeds | n | cpus | wall (per task) |
|---|---|---|---|---|---|---|---|
| 64825768 | `slurm/headline.sbatch` | `0-74` | headline grid: 75 configs, 5 mechanisms each, two worlds, best-response iteration, 21 single deviations | 10 per profile for the headline profiles and deviations, 10 for each best-response evaluation; simulation seeds 0..9, arrival seed `1000003 + seed` | 300,000 | 1 | see table below |
| 64825969 | `slurm/ladder.sbatch` | none | monitor ablation ladder: 4 anytime rungs, no-slack rung, 9 two-sample rungs, the naive two-sample-against-own-bid rung, no-monitor rung; 3 primary behaviours; 3 alphas | 200 replicates per cell, seeds 0..199 | 300,000 | 1 | see table below |
| 64826003 | `slurm/flipreg.sbatch` | `0-19` | contextual vs scalar revenue on all 165 three-model subsets, Q=3 and Q=7 context sets | 5, seeds 0..4 | 300,000 | 1 | see table below |

Seeds are fully determined by the scripts: simulation seed `s` sets the reward stream
(`UniformStream(s)`) and the arrival stream (`default_rng(1000003 + s)`); the embedding uses
`random_state = 20260924`. Nothing is drawn from an unseeded source.

## Additional submissions made after the first pass

| job id | script | array | what | why |
|---|---|---|---|---|
| 64825969 | `slurm/ladder.sbatch` (first version) | none | monitor ladder, single task | CANCELLED: simulating the EXP3 fallback to the horizon after every conviction made it about fifty times slower than the phase being measured, and it would not have finished inside the wall clock. |
| 64826970 | `slurm/ladder.sbatch` (second version) | `0-8` | monitor ladder, one task per (alpha, primary behaviour) | CANCELLED for the same reason after the fix below was written. |
| 64828480 | `slurm/ladder.sbatch` (final) | `0-8` | monitor ladder, 300 replicates per cell | Each replicate now ends at the first conviction (`stop_on_switch`), which is all the two ladder axes depend on. The flag defaults to False and changes nothing else. |
| 64826678 | `slurm/horizon.sbatch` | `0-1` | horizon sweep, the three selected triples, n from 300,000 to 30,000,000 | added after the first results showed the contextual advantage was being swamped by finite-horizon elicitation overhead |
| 64826679 | `slurm/horizon_all.sbatch` | `0-19` | all 165 triples at n = 3,000,000 | same reason |
| 64830515 | `slurm/fineshade.sbatch` | `0-19` | fine theta grid near 1 and the undercut deviation | added after the coarse option set showed zero degradation for the routers, to test whether that was an artefact of the grid |

## Second round of submissions, after the coordinator's additions

| job id | script | array | what |
|---|---|---|---|
| 64835708 | `slurm/ladder_fixedbuffer.sbatch` | `0-2` | BASELINE 2: the monitor ladder rerun including the fixed-buffer rung, 6 buffers x 4 burn-ins, 200 replicates, one task per primary behaviour |
| 64835709 | `slurm/baselines.sbatch` | none | BASELINE 1: the single-observation exclusion rule under our observation model, elicitation length in {1,2,5,20,100}, both empty-set policies, 6 deviations, 4 triples, 5 alphas, 30 seeds |
| 64835920 | `slurm/richbr.sbatch` | `0-19` | the fair strategic comparison over the rich option class. **CANCELLED BY ME IN ERROR**: I meant to cancel the utility-curve job and typed this job id. Resubmitted as 64837051; no results from it were used. |
| 64836619 | `slurm/utilcurves.sbatch` | `0-3` | utility against effort, three arm roles, two sweep modes, 61-point grid, measured and constructed two-top instances, 8 seeds |
| 64837051 | `slurm/richbr.sbatch` | `0-19` | the resubmission of the rich-option-class best response |
| 64833916 | `slurm/ladder_compliant.sbatch` | `0-2` | the compliant arm of the ladder rerun with a longer wall clock, 300 replicates |
| 64837192 | `slurm/baselines.sbatch` | `0-19` | the sharded resubmission of BASELINE 1; the unsharded 64835709 would not have finished inside its wall clock and was cancelled before it produced output |
| 64879587, resubmitted as 64880100 | `slurm/secondbest.sbatch` | `0-21` | first attempt, **CANCELLED**: the array was requeued by the scheduler about forty minutes in and restarted from zero, and that version of the script wrote its CSV only at the end, so a second requeue would have lost everything again. Resubmitted with incremental writing. BASELINE 3: the Second-Best Utility Guarantee Mechanism (WWW 2026) reimplemented from the paper, in the scalar and contextual settings, against our scalar and contextual mechanisms, 20 seeds |
| 64879828, resubmitted as 64880101 | `slurm/secondbest_gen.sbatch` | `0-21` | first attempt, cancelled with the above for the same reason. The same sweep under the generous reading of their line 21, in which blind trust phase II still runs after the monitor fires |
| 64872842 | `slurm/twotopsweep.sbatch` | `0-12` | the capability-gap sweep: is the two-top condition a cliff at gap zero or a transition at a scale? One delta per task |
| 64873504 | `slurm/gaprefine.sbatch` | `0-5` | six further deltas between 0.0055 and 0.0072, to place the crossover to within 0.0005 |
| 64873115 | `slurm/utilwin.sbatch` | `0-7` | the utility curves rerun WITH the win probability recorded as a second series. **CANCELLED at 4.5 hours**: each task wrote its CSV only at the end and was going to exceed its wall clock with nothing on disk. Resubmitted as 64879905 after adding a write after every completed block, which is the rule for this round and which I had not applied to this script. |
| 64879905 | `slurm/utilwin.sbatch` | `0-7` | the resubmission, 24 seeds, writing incrementally |
| 64859491 | `slurm/utilfast.sbatch` | `0-5` | a focused companion to 64836619 at the SAME design constants, restricted to the cells the report quotes, so those numbers do not wait for the full grid |
| 64839998 | `slurm/ladder_shade.sbatch` | `0-3` | the other half of the fixed-buffer trade-off: a deviator that shades by a constant 0.01, 0.05, 0.10 or 0.19 below the announced price, which is the deviation a fixed buffer cannot convict by construction |

A note on the error above, recorded because the rule of this round is that nothing is quietly
repaired: job 64835920 was cancelled by me by mistake, its output was never written, and nothing
in this package depends on it. The resubmission 64837051 runs the identical script and
configuration.

## A job-control error of mine, recorded

When I resubmitted the two second-best arrays with incremental writing, I cancelled the originals
with `scancel --name=a4_sb --name=a4_sbgen`. **That did not take effect**, and for a period both
the original arrays (64879587, 64879828) and their replacements (64880100, 64880101) were running
and writing to the same `secondbest_*.csv` and `secondbestgen_*.csv` paths. I noticed because
`squeue` showed 44 tasks named `a4_sb` where there should have been 22, cancelled the originals
explicitly by job id, and verified that exactly 22 plus 22 plus 8 tasks remained and that every
one of the 44 output files still parses.

Why no result is ambiguous: both arrays ran the identical script with identical arguments, shard
indices, seeds and horizon, so any file written by either is the same measurement. The risk was a
torn file from two concurrent writers, not a wrong number, and every file was checked and parses.
If anything downstream looks odd, the clean rerun is `sbatch slurm/secondbest.sbatch` on its own.

## Measured runtimes and core-hours

Regenerate this table with:

    bash audit/round2/A4/scripts/compute_tally.sh 64825768,64825969,64826003,64826678,64826679,64826970,64828480,64830515

It is the wall clock Slurm actually recorded, one core per task, so the sum of task elapsed times
is the core-hour figure.
| job | tasks | longest task | sum of task elapsed (core-hours) | states |
|---|---|---|---|---|
| a4_base | 20 | 2.93 h | 47.59 | {'COMPLETED': 20} |
| a4_fine | 20 | 3.07 h | 36.38 | {'COMPLETED': 20} |
| a4_flipreg | 20 | 0.17 h | 2.66 | {'COMPLETED': 20} |
| a4_gapref | 6 | 0.50 h | 2.93 | {'COMPLETED': 6} |
| a4_gapsweep | 13 | 1.90 h | 18.77 | {'COMPLETED': 13} |
| a4_headline | 75 | 6.01 h | 302.12 | {'COMPLETED': 70, 'TIMEOUT': 5} |
| a4_horizall | 20 | 1.31 h | 16.45 | {'COMPLETED': 20} |
| a4_horizon | 2 | 5.83 h | 10.65 | {'COMPLETED': 2} |
| a4_ladcomp | 3 | 3.31 h | 9.60 | {'COMPLETED': 3} |
| a4_ladder | 18 | 4.01 h | 23.83 | {'CANCELLED': 9, 'COMPLETED': 8, 'TIMEOUT': 1} |
| a4_ladfix | 3 | 5.39 h | 7.56 | {'COMPLETED': 3} |
| a4_ladshade | 4 | 6.00 h | 13.43 | {'TIMEOUT': 1, 'COMPLETED': 3} |
| a4_richbr | 20 | 9.63 h | 141.26 | {'COMPLETED': 20} |
| a4_sb | 22 | 0.14 h | 3.00 | {'RUNNING': 22} |
| a4_sbgen | 22 | 0.13 h | 2.93 | {'RUNNING': 22} |
| a4_util | 4 | 11.17 h | 36.32 | {'COMPLETED': 4} |
| a4_utilfast | 6 | 3.10 h | 13.41 | {'COMPLETED': 6} |
| a4_utilwin | 8 | 0.22 h | 1.79 | {'RUNNING': 8} |
| **total** | | | **690.67** | |

Login-node wall clock beyond the smoke tests listed above: the data download (7 s), the capability
and embedding builds (about 5 minutes in total), and the aggregation, table and figure
regenerations, each of which takes 5 to 10 seconds and was run perhaps thirty times.

## Real arrival order (WildChat stream), submitted 2026-10-20T17:07:03Z
- job: 65893127, array 0-389%390, partition cpu, qos normal, 1 cpu, 12G, 8h per task
- script: audit/round2/A4/scripts/slurm/run_v3_real.sbatch; task list: tasks_v3_real.txt (390 lines, unchanged from A5 pre-registration)
- stream: <workspace>/real_sequences/wildchat48m_all.npz, 5,167,182 rounds, 5 types, start offset per seed from rng(31337+seed), never tiled
- raw CSVs: <scratch>/real/raw; logs: <scratch>/real/logs; traces: <workspace>/v3/real
- smoke test: plmesp/learning line, n=20000, 1 seed, login node, 3.8s wall, order=real, revenue 0.479, fire_rate 0
- completed 2026-10-20T19:54:34Z: 390/390 COMPLETED, 0 failed, 168.5 CPU-hours, longest cell 01:57:27 wall
- aggregate: experiments/data/A5/c10_real_order.csv (550 cells, via aggregate_v3.py on the raw dir above)
- 2026-10-24T17:12:42Z mesp_shading array 66019415 (40 tasks, cpu-preempt, all COMPLETED): MESP (context-local) against BL2.ExploitDecay slow/fast on the ten real-order subsets, n = 3e5 (20 seeds) and 3e6 (10 seeds), real and iid order; aggregate experiments/data/A5/c13_mesp_shading.csv (c10 column layout). Real order, mean over subsets and horizons: slow 0.492 (fire 99.8%), fast 0.391 (fire 2.5%); UCB router 0.509 / 0.506 on the same cells.
