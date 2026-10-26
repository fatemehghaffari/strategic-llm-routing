#!/bin/bash
#SBATCH --job-name=a4_gapsweep
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=08:00:00
#SBATCH --array=0-12
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# Is the two-top condition a cliff at gap zero, or a graded transition at the
# shading scale?  One delta per array task.
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python two_top_sweep.py --n 300000 --br-seeds 4 --eval-seeds 10 \
  --curve-grid 21 --curve-seeds 6 --alpha a0.50 \
  --models "GPT-4|Claude-V2|Mistral-7B" \
  --deltas 0,0.001,0.002,0.005,0.0075,0.01,0.015,0.02,0.03,0.05,0.1,0.2,0.4 \
  --mechs plmesp,mesp_scalar \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 13 \
  --out $SP/llm/raw/gapsweep_${SLURM_ARRAY_TASK_ID}.csv
