#!/bin/bash
#SBATCH --job-name=a4_ladcomp
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=10:00:00
#SBATCH --array=0-2
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# Re-run of the COMPLIANT arm of the monitor ladder with a longer wall clock.
# A compliant winner is (correctly) almost never convicted, so those replicates
# run the full horizon and the cells are far slower than the deviating ones.
SP=<scratch>
cd $SP/llm
ALPHAS=(a0.25 a0.50 a0.75)
$SP/venv/bin/python monitor_ladder.py --n 300000 --reps 300 \
  --alphas ${ALPHAS[$SLURM_ARRAY_TASK_ID]} --behaviour compliant \
  --out $SP/llm/raw/monitor_ladder_comp${SLURM_ARRAY_TASK_ID}.csv
