# Compute log, H1 impossibility track, 18 September 2026

No Slurm job was submitted. All computation was local, on the login node, and took under one minute
in total. Scripts live in
`<scratchpad>/round2/h1-impossibility/` and were run with the venv python named in `COMMON.md`.

| script | what it checks | result |
| -- | -- | -- |
| `check.py` | the supremum `sup_c (f(c)-V)(1-c)/(c-V)` for the full extraction benchmark `f(c)=c`, and the contradiction of Corollary C2 | supremum equals `1-V`, attained as `c` decreases to `V`; contradiction confirmed at `V=0.2, M=0.9` |
| `check2.py` | the bump mass formula `||b||_1 = L omega_d R^{d+1}/(d+1)` used in T6, by Monte Carlo in `d = 1, 2, 3` | agreement to four digits |
| `check3.py` | whether the linear relaxation behind T4 is satisfiable at `alpha = (1-V)/(1+M-2V)` and infeasible just above it | feasible at that value and infeasible at `1.02` times it, on four instance pairs |

Also downloaded, for prior art only: `braverman19b.txt` (text extraction of the PMLR PDF by
`gs -dBATCH -dNOPAUSE -sDEVICE=txtwrite`) and `esmaeili.pdf` / `esmaeili.txt` (arXiv 2312.07929).
