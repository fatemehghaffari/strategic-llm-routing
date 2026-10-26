#!/bin/bash
#SBATCH --job-name=a4_horizon
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=08:00:00
#SBATCH --array=0-1
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
SP=<scratch>
cd $SP/llm
SET=Q3; if [ ${SLURM_ARRAY_TASK_ID} -eq 1 ]; then SET=Q7; fi
$SP/venv/bin/python horizon_sweep.py --set $SET --triples selected \
  --ns 300000,1000000,3000000,10000000,30000000 --nseeds 5 --alpha a0.50 \
  --out $SP/llm/raw/horizon_${SET}.csv
