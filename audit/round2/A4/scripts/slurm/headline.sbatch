#!/bin/bash
#SBATCH --job-name=a4_headline
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --time=06:00:00
#SBATCH --array=0-74
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python run_sim.py \
  --configs $SP/llm/out/configs.jsonl \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 75 \
  --out $SP/llm/raw/headline_${SLURM_ARRAY_TASK_ID}.csv
