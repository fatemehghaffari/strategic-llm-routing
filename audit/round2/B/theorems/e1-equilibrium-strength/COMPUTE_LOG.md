# Compute log, track E1 (equilibrium strength of MESP)

All runs use the session venv
`/scratch/login/.../scratchpad/venv/bin/python` (NumPy 2.5.3, SciPy 1.18.1).
Outputs go to `<scratchpad>/round2/e1/` (JSON per configuration) with Slurm logs in `<scratchpad>/round2/e1/logs/`.

## Login-node checks (seconds each, allowed as quick checks)

| when | command | wall | result |
| - | - | - | - |
| 18 Sep | `bidprofile.py --instance K2_unique_top --n 200 --bids 0.70,0.35` | 2.9 s | code validation only; at n = 200, s_n = 0.475 so tau = 0 and the horizon is degenerate |
| 18 Sep | `bidprofile.py --instance K2_tied_top --n 2000 --bids 0.50,0.50` | 16.9 s | exploitability 0.330 and 0.323 per round (linear), revenue 0.370 per round |
| 18 Sep | `bidprofile.py --instance K2_tied_top --n 2000 --bids M` | 12.5 s | exploitability 0.038 and 0.036 per round, revenue 0.643 per round |

## Slurm submissions (partition `cpu`, account `<slurm-account>`, 4 cores, 8 GB, 5 h)

Script: `run_e1.sh <instance> <bid vector> <tag> <n ...>`; one job per profile, horizons in increasing order so
that partial results survive a timeout.

| job id | name | instance | Stage-1 bids | horizons |
| - | - | - | - | - |
| 64566140 | e1_k2uni_star | K2_unique_top | capacity (S\*) | 2000, 5000, 10000, 20000 |
| 64566141 | e1_k2uni_bad | K2_unique_top | 0.70, 0.35 | 2000, 5000, 10000, 20000 |
| 64566142 | e1_k2tie_star | K2_tied_top | capacity (S\*) | 2000, 5000, 10000, 20000 |
| 64566143 | e1_k2tie_joint | K2_tied_top | 0.50, 0.50 | 2000, 5000, 10000, 20000 |
| 64566144 | e1_k2tie_asym | K2_tied_top | 0.80, 0.50 | 2000, 5000, 10000 |
| 64566145 | e1_k3uni_star | unique_top | capacity (S\*) | 2000, 5000, 10000 |
| 64566146 | e1_k3uni_bad | unique_top | 0.70, 0.00, 0.35 | 2000, 5000, 10000 |
| 64566147 | e1_k3uni_coal | unique_top | 0.90, 0.00, 0.40 | 2000, 5000, 10000 |
| 64566148 | e1_k3tie_star | tied_top | capacity (S\*) | 2000, 5000, 10000 |
| 64566149 | e1_k3tie_coal | tied_top | 0.50, 0.50, 0.45 | 2000, 5000, 10000 |

Runtimes and outcomes are recorded in the results section of `REPORT.md`.

## Further login-node work, 18 September

| when | command | wall | result |
| - | - | - | - |
| 18 Sep | `bidprofile.py --instance unique_top --n 2000` for bids `M`, `0.70,0.0,0.35`, `0.90,0.0,0.40` | 44 s | K = 3 unique-top panel; first run used a loose loser-branch bound (worst possible winner) and was rerun after `winner_law` was added |
| 18 Sep | `bidprofile.py --instance tied_top --n 2000` for bids `M`, `0.50,0.50,0.45` | 30 s | K = 3 tied-top panel |
| 18 Sep | `bidprofile.py --instance K2_tied_top --n 5000 --bids 0.50,0.50` | 96 s | joint underbid at the second horizon; per-round gain unchanged, hence linear |
| 18 Sep | `bidprofile.py --instance K2_unique_top --n 5000 --bids 0.70,0.50` | 94 s | interior revenue point of the equilibrium continuum |
| 18 Sep | `validate_bp.py` on five configurations, 2000 to 4000 replicates | 90 s total | every simulated mean inside the exact bracket (REPORT.md Section 8.1a) |

## Outcome

All ten Slurm jobs ran on partition `cpu` under account `<slurm-account>`. Elapsed times from `sacct`:
`e1_k2uni_bad` 35:05, `e1_k2tie_asym` 13:55, `e1_k3uni_star` 12:14, `e1_k3uni_coal` 08:20, `e1_k3tie_star`
08:42, `e1_k3tie_coal` 10:09, all COMPLETED; `e1_k2uni_star`, `e1_k2tie_star`, `e1_k2tie_joint` and
`e1_k3uni_bad` were still running on their largest horizon when this report was finalized, and every number
quoted in REPORT.md comes from a completed configuration. The per-configuration JSON files are copied to
`results/` in this directory; the naming is `bp_<instance alias>_<tag>_<n>.json`.

Cost note: the exact primary-phase backward induction is `O(N_n^2)` per distinct price, so a single agent at
`n = 20000` with `K = 2` takes about 12 minutes and the whole `K = 2` ladder about 35 minutes per profile.

## Part II: the profile-local contextual mechanism (18 September)

Driver `ctxprofile.py`, instances in `ctxinstances.json`, Slurm wrapper `run_ctx.sh`, tables from
`aggregate_ctx.py`. One exact computation per profile per agent; cost is `O(N_z^2)` per distinct local price.

| job id | name | instance | bid array | horizons |
| - | - | - | - | - |
| 64567828 | c_mix_star | ctx_mixed | capacity | 8000, 20000 |
| 64567829 | c_mix_badz1 | ctx_mixed | `0.70,0.35` at z1, capacity at z2 | 20000 |
| 64567830 | c_mix_badboth | ctx_mixed | `0.70,0.35` at z1, `0.50,0.50` at z2 | 8000, 20000 |
| 64567831 | c_div_star | ctx_division | capacity | 8000, 20000 |
| 64567832 | c_div_div | ctx_division | `0.80,0.35` at z1, `0.0,0.80` at z2 | 8000, 20000 |
| 64567833 | c_rare_joint | ctx_rare (shares 0.75 / 0.25) | `0.50,0.50` at both | 8000 |
| 64567834 | c_rare_star | ctx_rare | capacity | 8000 |

Login-node checks: the first `ctx_mixed` capacity run at `n = 8000` (151 s under Slurm, 85 s on the login node)
and the `badz1` run at `n = 8000` (89 s) were done interactively; the Slurm run reproduced the login-node
numbers to the last printed digit. A first version of `ctxprofile.py` mis-parsed a bid row given as `M`; fixed
before any recorded run.
