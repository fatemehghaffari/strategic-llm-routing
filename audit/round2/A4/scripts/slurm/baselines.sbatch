#!/bin/bash
#SBATCH --job-name=a4_base
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=06:00:00
#SBATCH --array=0-19
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python baselines.py --n 300000 --nseeds 30 --set Q7 \
  --alphas a0.00,a0.25,a0.50,a0.75,het \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 20 \
  --out $SP/llm/raw/baselines_${SLURM_ARRAY_TASK_ID}.csv
