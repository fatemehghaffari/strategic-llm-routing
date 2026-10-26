#!/bin/bash
#SBATCH --job-name=a4_ladder
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=04:00:00
#SBATCH --array=0-8
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
SP=<scratch>
cd $SP/llm
ALPHAS=(a0.25 a0.50 a0.75)
BEHS=(compliant baitswitch baitswitch_mild)
AI=$((SLURM_ARRAY_TASK_ID / 3)); BI=$((SLURM_ARRAY_TASK_ID % 3))
$SP/venv/bin/python monitor_ladder.py --n 300000 --reps 300 \
  --alphas ${ALPHAS[$AI]} --behaviour ${BEHS[$BI]} \
  --out $SP/llm/raw/monitor_ladder_${SLURM_ARRAY_TASK_ID}.csv
