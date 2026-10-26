# Routing among Strategic LLM Providers: A Contextual Mechanism without Monetary Transfers

## Paper: [paper.pdf](paper.pdf)

The full version of the paper, main text and appendices with all proofs, is [`paper.pdf`](paper.pdf). This repository
holds the code, the results and the figures behind it.

## Repository layout

| Path | Contents |
|---|---|
| [`paper.pdf`](paper.pdf) | The full version of the paper: main text and all appendices with complete proofs. |
| `figures/paper/` | Every figure as a vector PDF and a 300-dpi PNG. `values_paper.csv` lists every plotted number and `MANIFEST.md` names each figure's data source. |
| `experiments/data/` | The result tables the figures and the text are drawn from, one folder per experiment package (`A2` to `A5`), the deviation traces in `J/`, and earlier-round runs in `A/`. |
| `experiments/llm_effort/` | The LLM serving experiment: code, configuration, Slurm scripts, results and its own README. |
| `audit/round2/A2` to `A5` | Simulation code, Slurm scripts and the full report for each experiment package. |
| `audit/round2/B/` | Numerical checks of the theorems' constants and horizons. |
| `scratch/experiments/` | Exact backward induction, the contextual simulations, and the C kernel for the continuum sweep. |

The folder names come from the working project. They are kept so that the scripts' relative paths still work.

## Reproduce the figures

Every figure is drawn from the tables in `experiments/data/` and `experiments/llm_effort/results/`, so no
simulation has to be rerun. On a fresh copy of this repository all 22 figures regenerate with:

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python audit/round2/A5/scripts/make_paper_figures.py --out figures/paper
```

To redraw one figure, add `--only` with the figure's file name without `.pdf`, for example
`--only fig_certified`. The style shared by all figures is in `audit/round2/A5/scripts/figstyle.py`.

## Reproduce the experiments

All simulations run on CPU; only the LLM experiment needs a GPU. They were run with Slurm on a university
cluster. Each Slurm script sets the Python interpreter and its work directories in a few variables near the
top, such as `PY`, `W` or `OUT`; point them at your own paths before submitting. Raw per-replicate output is
not included because of its size. The aggregated tables in `experiments/data/` are what the paper reports.
The report named for each package gives the exact commands, seeds, job sizes and run times.

| Results in the paper | Data | Code and how to run |
|---|---|---|
| Certified bounds on deviation gains, component ablations | `experiments/data/A2/` | `scratch/experiments/round2/ctx_local/`: `run_exact.py` for the exact computation, `run_ladder.py` for the ablations, then `aggregate.py` and `report_tables.py`. Report: `audit/round2/A2/EXPERIMENT_REPORT.md`. |
| Continuum mechanism: activation thresholds and the horizon sweep | `experiments/data/A3/` | C kernel in `scratch/experiments/round2/ctx_fast/`. Compile with `gcc -O2 -ffp-contract=off -fno-fast-math -fPIC -shared -o libcgmesp_v3.so cgmesp_v3.c -lm`, run `sweep_run.py`, aggregate with `aggregate.py`. `assemble.sh` runs every step. Commands and seeds: section 8 of `audit/round2/A3/THRESHOLD_REPORT.md`. |
| RouterBench capabilities, deviation gains, monitors, near ties | `experiments/data/A4/` | `audit/round2/A4/scripts/run_sim.py` through the Slurm scripts in `audit/round2/A4/scripts/slurm/`. Commands: section 10 of `audit/round2/A4/REPORT.md`. |
| Baselines, arrival orders, leaderboard replication, WildChat replay, Cao et al., label noise, graded feedback, task types, substitution | `experiments/data/A5/` | `audit/round2/A4/scripts/run_v3.py` through `audit/round2/A4/scripts/slurm/run_v3.sbatch`, aggregated by `audit/round2/A4/scripts/aggregate_c.py`. Data preparation: `audit/round2/A5/A_data/scripts/`. Reports: `audit/round2/A5/`. |
| MESP under slow and fast effort reduction | `experiments/data/A5/c13_mesp_shading.csv` | `audit/round2/A4/slurm/mesp_shading.sbatch`, which calls `run_v3.py`. |
| Deviation dynamics and the monitor path | `experiments/data/J/` | `audit/round2/A4/scripts/j_traces.py` and `j_cao_phases.py` through `audit/round2/A4/slurm/j_runs.sbatch`. |
| Private reasoning effort in LLM serving | `experiments/llm_effort/results/` | One GPU, vLLM and Qwen3-4B. See [`experiments/llm_effort/README.md`](experiments/llm_effort/README.md). |
| Numerical checks of the theorems' constants and horizons | `audit/round2/B/` | Scripts in `audit/round2/B/theorems/*/`. |

## Data sources

The experiments use RouterBench, the Open LLM Leaderboard (v2), WildChat-4.8M, GSM8K and MATH-500. Only
aggregate statistics derived from WildChat are included here. Sources, versions and licences are recorded in
`audit/round2/A4/DATA_PROVENANCE.md`, `audit/round2/A5/DATA_PROVENANCE.md` and `audit/round2/A5/licenses/`.

## Environment

Python 3.12 with numpy 2.5.4, pandas 3.0.6, matplotlib 3.11.2 and scipy 1.18.1, pinned in
`requirements.txt`. The LLM experiment pins its own environment in `experiments/llm_effort/requirements.txt`.
