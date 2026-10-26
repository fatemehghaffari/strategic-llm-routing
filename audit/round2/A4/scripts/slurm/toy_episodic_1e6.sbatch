#!/bin/bash
#SBATCH --job-name=toy_epi
#SBATCH --partition=cpu-preempt
#SBATCH --requeue
#SBATCH --account=<slurm-account>
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=24:00:00
#SBATCH --output=<workspace>/v3/main/toy_episodic_1e6/logs/%x_%A_%a.out
set -euo pipefail
PY=<scratch>/venv/bin/python
cd <repo>/audit/round2/A4/scripts
$PY toy_episodic.py $(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$1")
