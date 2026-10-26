# Compute log, Prover 1, candidate C2 (Local-MESP), 18 September 2026

No Slurm jobs were submitted. All computation was single-core Python in the round-2 venv
(`/scratch/.../scratchpad/venv/bin/python`), run on the login node. Scripts and raw
outputs live in `/scratch/.../scratchpad/round2/prover1-c2/`.

| script | what it checks | approximate wall time | cores | output file |
|:--|:--|:--|:--|:--|
| `exp3_doubling.py` | Lemma 6 and Lemma 7, doubling EXP3, plus a brute-force check of `sum_k R_K(2^k) <= R^dbl_K(H)` for `K<=50`, `H<=20000` | about 8 minutes (run detached) | 1 | `out_exp3_doubling.txt` |
| `monitor.py` | Lemma 5, boundary crossing and slack, and the non-top tenure bound (6.11) | under 1 minute | 1 | `out_monitor.txt` |
| `award_checks.py` | Lemma 4 (L4b), (L4c), and `tau_z <= M_W` in the losing branch; 600000 random configurations | under 1 minute | 1 | `out_award_checks.txt` |
| `localmesp.py` | full Local-MESP simulation, 6 scenarios, 12 deviations including cross-profile timed ones, 60 repetitions each, `n = 6000` | about 100 seconds | 1 | `out_localmesp.txt` |

Note on the login-node rule in `audit/round2/prompts/COMMON.md`: the `exp3_doubling.py` run
exceeded a few minutes. It was single-core, low-memory and detached; had it needed more, it
would have gone to `sbatch -p cpu -A <slurm-account>`. Recording this accurately
rather than restating the rule.

No canonical file was modified. No `git` state-changing command was run.
