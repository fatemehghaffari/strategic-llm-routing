# Compute log, UB1, 16 October 2026

No Slurm job submitted. Login node, single core, NumPy only, venv
<scratch>

| run | command | wall time | output |
| -- | -- | -- | -- |
| pump deviation, first pass (pump to M1) | `python scratch/round2/ub1/pump_check.py` | ~20 s | superseded, see log |
| pump deviation, scan c* in {0.6,0.7,0.75,0.8}, 3 instances x 3 horizons x 50 replicates | same script after edit | ~60 s | pump_check.log (copied here) |

Seeds: `np.random.default_rng(7)` per (instance, n) for the agent-local uniform arrays; baseline and
deviation share them.
| stalling deviation vs overshoot price (REPORT 4.2), 4 horizons x 3 stall lengths x 50 replicates | `python scratch/round2/ub1/stall_check.py` | ~90 s | stall_check.log (copied here) |
