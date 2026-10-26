#!/bin/bash
#SBATCH --job-name=a5_C
#SBATCH --partition=cpu-preempt
#SBATCH --requeue
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --output=<workspace>/v3/C/logs/%x_%A_%a.out
# usage: sbatch --array=0-N%60 slurm/extras_c.sbatch <tasks-file>
set -euo pipefail
PY=<scratch>/venv/bin/python
RAW=<workspace>/v3/C/raw
cd <repo>/audit/round2/A4/scripts
LINE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$1" | sed "s#RAW/#$RAW/#")
SCRIPT=${2:-extras_c.py}
eval $PY $SCRIPT $LINE --trace-dir <workspace>/v3/C
