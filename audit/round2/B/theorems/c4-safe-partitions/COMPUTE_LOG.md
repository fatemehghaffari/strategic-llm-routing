# Compute log, C4 safe partitions

Scratch directory (referred to in `REPORT.md` as `<scratchpad>`):
`.../scratchpad/round2/c4-safe-partitions/`.
Python: the shared venv named in `audit/round2/prompts/COMMON.md` (NumPy 2.5.3).

## Code

| file | what it is |
|:-|:-|
| `partitions.py` | first, readable simulator: `Instance` (piecewise-constant delivered means on a segment), `LeafETC` (the manuscript's cell rule), `run_tree` with rules `coat`, `ra_nofloor`, `ra_floor`, `grid` |
| `fastsim.py` | the same model, rewritten for speed (pre-drawn context and reward streams, prefix sums for exact cell means); used for every run with `n >= 2e5` |
| `w1.py` | Theorem 3, the monotonicity witness (instance W1) |
| `w2.py`, `w2b.py` | Theorem 5, the deviation and robustness witness (instance W2); `w2b.py` is the horizon sweep with the manuscript's grid parameters |
| `w2c.py` | adversarial check on Theorem 5: perturbing the exact tie |
| `w3.py`, `w3b.py`, `w3c.py` | Theorem 4, the honest-play robustness witness (instance W3); `w3c.py` is the final form |
| `rate.py`, `job_rate.sh` | COAT rate study, `D = 4`, curve support, horizons `5e5` to `3.2e7` |
| `check_adv.py` | added 18 September 2026 after `ADVERSARY.md`: reproduces its X1, that deleting the freeze branch (`theta_0 = 10^9`) leaves instance W2's numbers unchanged to four decimals |
| `w1b.py` | added after `ADVERSARY.md`: the corrected Theorem 3 table, on the diagonal support, with each grid row using a single `q = 2000` and COAT at its Section 5.1 schedules |
| `w3d.py` | added after `ADVERSARY.md`: COAT with and without the one added freeze sentence, COAT's own schedules |
| `w3e.py`, `job_w3e.sh` | added after `ADVERSARY.md`: the same comparison at the theorem's own schedules, horizons `2e5` to `5.12e7` |
| `rate2.py` | COAT versus Static Grid-ETC when the ambient dimension is `D = 8` and `d_nu = 1` |
| `abse.html`, `zoom.html`, `ucbogram.html` | full texts downloaded for the citation checks (Section 7 of `REPORT.md`) |

Every run fixes seeds explicitly through `numpy.random.default_rng`; the seed formulas are in the
scripts (`1000 r + 7`, `555 r + 3`, `97 r + 11`, `17 r + 3`, `13`, `29 r + 7`, `31 r + 5`).

## Runs

Login-node runs, each under two minutes of wall time and single threaded:
`w1.py 200000 6`; `w2.py 200000 3`; `w2b.py`; `w2c.py`; `w3.py 100000,400000,1600000,6400000`;
`w3b.py`; `w3c.py 200000,800000,3200000`; `rate.py 25000,50000,100000,200000 2`;
`rate2.py 250000,1000000,4000000`.

Slurm:

| job id | script | partition | account | resources | wall time |
|:-|:-|:-|:-|:-|:-|
| 64568006 | `job_rate.sh` running `rate.py 500000,1000000,2000000,4000000,8000000,16000000,32000000 3` | `cpu` | `<slurm-account>` | `-c 2`, 8G, 3h limit | about 25 minutes |
| 64574905 | `job_w3e.sh` running `w3e.py 200000,800000,3200000,12800000,51200000` | `cpu` | `<slurm-account>` | `-c 2`, 8G, 3h limit | see `logs/c4freeze-64574905.out` |

Log: `logs/c4rate-64568006.out`.

## Web checks (18 September 2026)

| URL | what was taken from it |
|:-|:-|
| `https://arxiv.org/abs/1110.6084` | title, authors, version dates of Perchet and Rigollet |
| `https://projecteuclid.org/journals/annals-of-statistics/volume-41/issue-2/The-multi-armed-bandit-problem-with-covariates/10.1214/13-AOS1101.full` | journal, volume, issue, pages, year, DOI |
| `https://ar5iv.labs.arxiv.org/html/1110.6084` | verbatim Policy 3 (ABSE), Policy 1 (SE), the soundness paragraph, Theorem 5.1 |
| `https://arxiv.org/abs/0907.3986` | title, author, version dates, COLT 2011 and JMLR 2014 |
| `https://www.jmlr.org/papers/v15/slivkins14a.html` | JMLR volume 15, pages 2533 to 2568, 2014 |
| `https://ar5iv.labs.arxiv.org/html/0907.3986` | verbatim selection rule, activation rule, `conf_t`, index, Algorithm 4.2 |
| `https://arxiv.org/abs/1003.1630` | title, authors, date of Rigollet and Zeevi |
| `https://ar5iv.labs.arxiv.org/html/1003.1630` | the regular partition, `M = floor((n/log n)^{1/(2 beta + d)})`, the doubling remark, the `M^d` exploration remark |

For each of the three papers the full text was downloaded with `curl` and the quoted passages were
extracted from the raw HTML with a script, not from a model summary.
