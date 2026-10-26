# Compute log (F1 sceptic, 18 September 2026)

No Slurm job submitted. Both scripts ran on the login node in under 20 seconds with the project venv
`<scratch>/venv/bin/python`.

| Script | What it checks | Wall time | Seeds |
|:-|:-|:-|:-|
| `check_exponents.py` | Section 1.2: the fitted exponent of the balanced cell-localised cost, with `L` retuned and with `L` pinned at the scalar `n^{2/3}` | 12 s | deterministic, no randomness |
| `check_s1.py` | Theorem S1: survival probability and realised saving of the boundary-tracking deviation against the `MESP` boundary, plus the compliant false-alarm rate | 6 s | 31337, fixed in file |

No PDF was downloaded for this task; the two primary sources were already converted during the
separation task and the text copies are in `<scratchpad>/round2/separation/`.
