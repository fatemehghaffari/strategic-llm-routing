#!/bin/bash
#SBATCH --job-name=a4_horizall
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=08:00:00
#SBATCH --array=0-19
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python horizon_sweep.py --set Q3 --triples all \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 20 \
  --ns 3000000 --nseeds 5 --alpha a0.50 \
  --out $SP/llm/raw/horizall_Q3_${SLURM_ARRAY_TASK_ID}.csv
