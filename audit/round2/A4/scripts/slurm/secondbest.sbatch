#!/bin/bash
#SBATCH --job-name=a4_sb
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=08:00:00
#SBATCH --array=0-21
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# BASELINE 3: the Second-Best Utility Guarantee Mechanism (WWW 2026),
# reimplemented from the paper, in the scalar and the contextual settings.
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python baseline_secondbest.py --n 300000 --nseeds 20 \
  --alphas a0.00,a0.25,a0.50,a0.75,het \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 22 \
  --out $SP/llm/raw/secondbest_${SLURM_ARRAY_TASK_ID}.csv
