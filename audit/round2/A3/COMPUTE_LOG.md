# A3 compute log

Scratch root: `<scratchpad>/round2/A3/` (logs in `logs/`, per-task JSON in `results/`).
Code (written by A3, not canonical): `scratch/experiments/round2/ctx_fast/`.
Partition `cpu`, account `<slurm-account>`, 1 core per task, no GPUs.

| date (2026) | job id | script | array | cores/task | time limit | purpose |
|--|--|--|--|--|--|--|
| 24 Sep | 64822145 | `verify.sh` | - | 1 | 06:00:00 | bit-equality of the C kernel against `ctx_local/cg_struct.py` on recorded numpy draws |
| 24 Sep | 64822146 | `array.sh tasks_d2.txt` | 1-240 (%120) | 1 | 02:30:00 | D = 2 horizon sweep, instances C and E, 16 horizons from 10^6 to 10^10.5, 8 behaviour profiles, 4 seeds (1024 runs, 27 core-h) |
| 24 Sep | 64822147 | `array.sh tasks_d3.txt` | 1-160 (%120) | 1 | 14:00:00 | D = 3 horizon sweep, instances D and F, 10^7 to 10^12.3 (363 runs, 264 core-h) |
| 24 Sep | 64822407 | `verify.sh` | - | 1 | 08:00:00 | superseded by 64822513 (re-run with the sharp Lemma-P2 cases added) |
| 24 Sep | 64822513 | `verify.sh` | - | 1 | 12:00:00 | verification, final: 106 cases including K = 4 and two 2*10^7-round structural cases sharp enough that Lemma P2 violations are nonzero |
| 24 Sep | 64822514 | `array.sh tasks_d4.txt` | 1-21 | 1 | 24:00:00 | D = 4 probe, instance G, 10^9 to 10^12, three profiles |
| 24 Sep | 64822515 | `array.sh tasks_stretch.txt` | 1-3 | 1 | 60:00:00 | D = 3 at 10^12.64, the horizon at which all three guarantees first become non-vacuous at D = 3 |
| 24 Sep | 64822147, 64822514, 64822515 | - | - | - | - | cancelled and resubmitted: the v1 kernel is memory bound at the D = 3 and D = 4 grid sizes (123 to 157 ns per round) and those tasks would have exceeded their time limit |
| 24 Sep | 64823290 | `array_v2.sh tasks_d3.txt` | 1-260 (%130) | 1 | 36:00:00 | D = 3 sweep with the v2 kernel, instances D and F, 10^7 to 10^12.3 (371 runs, 542 core-h) |
| 24 Sep | 64823291 | `array_v2.sh tasks_d4.txt` | 1-21 | 1 | 36:00:00 | D = 4 probe, instance G, 10^9 to 10^12 |
| 24 Sep | 64823292 | `array_v2.sh tasks_stretch.txt` | 1-2 | 1 | 96:00:00 | D = 3 at 10^12.64, all three guarantees non-vacuous; about 54 h per run |
| 24 Sep | 64823294 | `verify_v2.sh` | - | 1 | 12:00:00 | the 106-case verification suite re-run against the v2 kernel |
| 24 Sep | 64826975 | `array_v2.sh tasks_backfill.txt` | 1-6 | 1 | 06:00:00 | backfill of six D = 2 tasks at 10^10.5 whose original array elements were running at about 200 ns per round on old gypsum nodes and risked the 2:30 time limit; the v2 kernel is bit-identical to v1, so a duplicate result is the same result |

Notes.

* `array.sh` and `array_v2.sh` are identical except that the second exports
  `CGMESP_LIB=libcgmesp_v2.so`. Both read a task-bundle file, one line per array element, and run
  `sweep_run.py` once per task in the bundle, skipping any task whose output JSON already exists.
* Job 64823293 was submitted and cancelled within a minute: it would have re-run the verification
  suite against the v1 kernel rather than v2, which 64822513 had already done.
* The three cancelled jobs (64822147, 64822514, 64822515) had produced a handful of completed runs
  before they were cancelled, at instance G and the smaller D = 3 horizons. Those result files were
  kept and the resubmitted arrays skipped them. The v1 and v2 kernels are bit-identical on every
  case tested, so mixing the two builds inside one sweep changes no number; only the wall-clock and
  nanoseconds-per-round columns of threshold_sweep.csv are affected by which build produced a row.
* Total across the sweep at the time this log was written: about 4.4 x 10^12 simulated rounds and
  about 60 core-hours already returned, with the D = 3 and D = 4 arrays still running.

## Re-pointed after the model change (one common context per round, 24 September)

| date (2026) | job id | script | array | cores/task | time limit | purpose |
|--|--|--|--|--|--|--|
| 24 Sep | 64827888 | `array_d.sh tasks_d1.txt` | 1-64 | 1 | 04:00:00 | d = 1 sweep across the common-context thresholds, instances C, E (K = 2) and D, F (K = 3), 22 horizons from 10^5 to 10^9, 8 profiles, 8 seeds (5632 runs, 2.8 core-h) |
| 24 Sep | 64827889 | `verify_d1.sh` | - | 1 | 08:00:00 | bit-equality of the common-context kernel against the unmodified reference driven on a diagonal context path, 160 cases |
| 24 Sep | 64827948 | `array_d.sh tasks_d2K3.txt` | 1-160 (%120) | 1 | 08:00:00 | d = 2 with K = 3, to test that the threshold depends on the dimension and not on the number of agents |
| 24 Sep | 64828160 | `verify_d1.sh` | - | 1 | 08:00:00 | first common-context verification: 160 of 160 cases bit-identical but VACUOUS on the interesting branches, because at 2 x 10^6 rounds the d = 1 price is still zero; superseded |
| 24 Sep | 64829324 | `verify_d1.sh` | - | 1 | 16:00:00 | common-context verification with a horizon of 5 x 10^6 added, above the d = 1 price threshold, so the suite covers positive prices, monitor firings and Stage-3 rounds; returned 240 of 240 bit-identical over 5.76 x 10^8 rounds, 2422 positive-price cubes, 304 monitor firings, 2.45 x 10^7 Stage-3 rounds |
