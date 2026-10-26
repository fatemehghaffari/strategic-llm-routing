# Compute log, track G1 (experts-over-policies fallback)

18 September 2026. Scratch directory: `<scratchpad>/round2/g1-experts-fallback/`, where
`<scratchpad>` is the session scratch root named in the role brief. Python: the project venv at
`<scratchpad>/venv/bin/python` (NumPy 2.5.3). A copy of every script is in this output directory.

**No Slurm job was submitted.** Every run below finished on the login node in seconds to under a
minute, which is inside the `COMMON.md` allowance ("anything longer than a few minutes goes through
Slurm"). There is therefore no job id, no partition and no account to record.

| Script | What it does | Where it runs | Wall time | Output |
|:-|:-|:-|:-|:-|
| `exponents.py` | exact rational exponent table of REPORT Section 4.4; checks `(d+1)/(d+2) < (d+2)/(d+3)` for `d = 0..11` | login node | under 1 s | stdout, reproduced in REPORT Section 4.4 and 8.1 |
| `exp4check.py` | first pass at selected-reactive EXP4 over an enumerated net, `K=2, J=3, V=3, N=729, T=4096`, 6 seeds | login node | about 30 s | stdout |
| `exp4check2.py` | part (C) comparator test and part (A) conservation test, `K=3, J=3, V=2, N=512, T=2048`, 5 and 3 seeds per configuration | login node | about 60 s | stdout, REPORT Sections 8.2 and 8.3 |
| `scaling.py` | horizon scaling of the deterrence gap, `T = 1024 .. 16384`, 4 seeds each | login node | about 90 s | stdout, REPORT Section 8.4 |
| inline `python -c` | net-size arithmetic of REPORT Section 6.1 (`log_2 N` at `d=1,2` and `n=10^6,10^9`) | login node | under 1 s | stdout, REPORT Section 6.1 |

Seeds are fixed inside each script (`numpy.random.default_rng` with the integer seeds shown in the
scripts). Nothing was written outside the scratch directory and this output directory.
