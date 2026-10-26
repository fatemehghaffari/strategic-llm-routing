#!/bin/bash
#SBATCH --job-name=a4_ladshade
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=06:00:00
#SBATCH --array=0-3
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# The other half of the fixed-buffer trade-off: a deviator that shades by a
# CONSTANT amount just inside a published buffer.  A fixed buffer c cannot
# convict a persistent shading smaller than c; a boundary that grows like
# sqrt(r) eventually can.
SP=<scratch>
cd $SP/llm
SH=(shade0.01 shade0.05 shade0.10 shade0.19)
$SP/venv/bin/python monitor_ladder.py --n 300000 --reps 200 \
  --alphas a0.25 --behaviour ${SH[$SLURM_ARRAY_TASK_ID]} \
  --out $SP/llm/raw/monitor_ladder_shade${SLURM_ARRAY_TASK_ID}.csv
