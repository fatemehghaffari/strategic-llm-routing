# Compute log (separation worker, 18 September 2026)

No Slurm job was submitted. All numerical work ran on the login node in under 5 seconds total,
with the project venv
`<scratch>/venv/bin/python`.

| Script | What it checks | Wall time | Seeds |
|:-|:-|:-|:-|
| `check.py` | Part 1: Lemma 2 and Theorem 1' on a PURE-SP style rule; Theorem 2 on `k`-window rules | 1.8 s | 20260918 fixed in file |
| `check2.py` | Part 2: Theorem 3 inequality for Grid-EXP3 with an adversarial periodic context sequence and a bait-and-switch behavioral agent, `n` in {2000, 8000, 32000}, 6 seeds each | 3.6 s | 1000 to 1005 |

Two PDFs were downloaded for the primary-source checks of Section 1.8 and converted with
`gs -q -dBATCH -dNOPAUSE -sDEVICE=txtwrite`; the text copies live in
`<scratchpad>/round2/separation/` and were not copied into the repository.
