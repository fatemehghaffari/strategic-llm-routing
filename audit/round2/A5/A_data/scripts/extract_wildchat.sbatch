#!/bin/bash
#SBATCH --job-name=a5_wcx
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --array=0-85%40
#SBATCH --output=<workspace>/logs/%x_%A_%a.out
set -euo pipefail
PY=<scratch>/venv/bin/python
i=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
$PY <repo>/audit/round2/A5/A_data/scripts/extract_wildchat.py <workspace>/raw_data/wildchat48m/data/train-$i-of-00086.parquet <workspace>/raw_data/wildchat_user_turns/shard_$i.parquet
