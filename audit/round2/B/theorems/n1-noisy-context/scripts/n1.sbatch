#!/bin/bash
#SBATCH --job-name=n1_noisy
#SBATCH --partition=cpu-preempt
#SBATCH --requeue
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=02:00:00
#SBATCH --output=<repo>/audit/round2/B/theorems/n1-noisy-context/out/logs/%x_%A_%a.out
set -euo pipefail
PY=<scratch>/venv/bin/python
D=<repo>/audit/round2/B/theorems/n1-noisy-context
LINE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" $D/scripts/tasks.txt | sed "s#OUT/#$D/out/#")
eval $PY $D/scripts/noisy_label.py $LINE
