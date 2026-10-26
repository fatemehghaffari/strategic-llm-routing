# Experiment data, committed so figures can be regenerated without recomputing

The analysis and plotting code lives in `scratch/experiments/round2/` and is
tracked. The AGGREGATED data every figure and every quoted number is built
from lives here, in `experiments/data/`, and is tracked. Raw per-replicate
output (about 209 MB for package A2 alone) is NOT tracked; it lives in the
session scratch directory and can be regenerated from the Slurm scripts.

The split is chosen so that an AESTHETIC change to a figure costs seconds and
needs no compute: the figure scripts read the aggregated CSVs, never the raw
results.

## Regenerating a figure after a style change

    source scratch/tools/texenv.sh
    $VENV/bin/python scratch/experiments/round2/figures/make_figures_a2.py \
        --csv experiments/data/A2 --out figures/experiments

Nothing else is needed. Edit the figure script, rerun, done.

## What is here

| path | package | contents |
|---|---|---|
| `experiments/data/A2/` | contextual mechanisms | aggregated CSVs for the exact grid, the ablation ladder, the deviation search and the continuous runs |
| `experiments/data/A2/figures_generated/` | | the figure PDFs as last generated, for reference |
| `experiments/data/A3/` | continuous threshold sweep | `threshold_sweep.csv`, `threshold_summary.csv` |
| `experiments/data/A/` | round-2 package A | aggregated run CSVs under `runs/` |
| `scratch/experiments/final/` | round-1 package | already tracked from the previous round |

## Regenerating the aggregated data from raw results

Only needed if the raw results change. Requires the scratch results tree:

    LADDER_N=200000 LADDER_Q=3 bash <scratch>/round2/A2/slurm/finalize.sh

which rebuilds the CSVs, `audit/round2/A2/TABLES.md` and the figures.

## Regenerating raw results from scratch (hours, Slurm)

See `audit/round2/A2/COMPUTE_LOG.md` for every job id, script, seed, partition
and runtime, and `scratch/experiments/round2/slurm/` for the submission
scripts. Partition `cpu`, account `<slurm-account>`.

## Rule for anyone adding an experiment

Commit the aggregated CSVs and the script that turns them into a figure.
Do not commit per-replicate output. Every number quoted in the paper must be
recomputable from what is in `experiments/data/` by a single named command,
and the Checks block at the head of each package's `TABLES.md` does exactly
that.
