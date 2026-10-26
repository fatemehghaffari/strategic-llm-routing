#!/bin/bash
#SBATCH --job-name=a4_gapref
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=08:00:00
#SBATCH --array=0-5
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# Resolve the crossover, which the coarse sweep places between 0.005 and
# 0.0075, against the predicted bid-difference scale of 0.0068.
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python two_top_sweep.py --n 300000 --br-seeds 4 --eval-seeds 10 \
  --curve-grid 21 --curve-seeds 6 --alpha a0.50 \
  --models "GPT-4|Claude-V2|Mistral-7B" \
  --deltas 0.0055,0.006,0.0065,0.0068,0.007,0.0072 \
  --mechs plmesp \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 6 \
  --out $SP/llm/raw/gapsweep_ref${SLURM_ARRAY_TASK_ID}.csv
