#!/bin/bash
#SBATCH --job-name=a4_flipreg
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=04:00:00
#SBATCH --array=0-19
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
SP=<scratch>
cd $SP/llm
SET=Q3; SH=${SLURM_ARRAY_TASK_ID}
if [ ${SLURM_ARRAY_TASK_ID} -ge 10 ]; then SET=Q7; SH=$((SLURM_ARRAY_TASK_ID-10)); fi
$SP/venv/bin/python flip_regression.py --set $SET --shard $SH --nshards 10 \
  --n 300000 --nseeds 5 --alpha a0.50 \
  --out $SP/llm/raw/flipreg_${SET}_${SH}.csv
