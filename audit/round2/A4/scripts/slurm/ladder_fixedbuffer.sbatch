#!/bin/bash
#SBATCH --job-name=a4_ladfix
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=12:00:00
#SBATCH --array=0-2
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# The ladder rerun that includes BASELINE 2, the fixed-buffer monitor.
SP=<scratch>
cd $SP/llm
BEHS=(compliant baitswitch baitswitch_mild)
$SP/venv/bin/python monitor_ladder.py --n 300000 --reps 200 \
  --alphas a0.25 --behaviour ${BEHS[$SLURM_ARRAY_TASK_ID]} \
  --out $SP/llm/raw/monitor_ladder_fb${SLURM_ARRAY_TASK_ID}.csv
