# Compute log, LB1 scout, 13 October 2026

No Slurm job was submitted. Everything ran on the login node, single core, NumPy only, venv
<scratch> (NumPy 2.5.3, Python 3.12.3).

| run | command | wall time | output |
| -- | -- | -- | -- |
| smoke test | `sim_lb1.py 10000 20 test_1e4.json` | 2 s | out/test_1e4.json |
| main grid | `sim_lb1.py 10000,17783,31623,56234,100000 100 grid_main.json` | about 160 s total (per cell 2 s to 42 s) | out/grid_main.json, out/grid_main.log |
| summary | `analyse_lb1.py grid_main.json` plus the pure-elicitation addendum | under 1 s | out/summary.txt |

Scratch copies live in `<scratchpad>/round2/lb1/`. Seeds: `np.random.default_rng(20261013 + n)` for the
uniform arrays, `default_rng(1)` for EXP3 coins and `default_rng(2)` for tie coins, re-created per run so
that every deviation of a replicate is coupled to its baseline.
