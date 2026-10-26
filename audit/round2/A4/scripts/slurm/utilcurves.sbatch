#!/bin/bash
#SBATCH --job-name=a4_util
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=12:00:00
#SBATCH --array=0-3
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python utility_curves.py --n 200000 --nseeds 8 --grid 61 \
  --alpha a0.50 --contexts MMLU,GSM8K \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 4 \
  --out $SP/llm/raw/utilcurves_${SLURM_ARRAY_TASK_ID}.csv
