#!/bin/bash
#SBATCH -p cpu
#SBATCH -A ${SLURM_ACCOUNT:?set SLURM_ACCOUNT}
#SBATCH -c 8
#SBATCH --mem=16G
#SBATCH -t 02:00:00
#SBATCH -o ${R2_WORK}/round2/A/logs/%x-%j.out
set -euo pipefail
# Portable paths. Set these before submitting:
#   R2_CODE_ROOT  the checkout holding scratch/experiments/round2
#   R2_WORK       a writable scratch directory for runs, logs and the venv
: "${R2_CODE_ROOT:?set R2_CODE_ROOT}" "${R2_WORK:?set R2_WORK}"
DATASET="$1"
SP=${R2_WORK}
WT=${R2_CODE_ROOT}
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=8
export PYTHONPATH="$WT/scratch/experiments/round2"
echo "host=$(hostname) date=$(date -u) dataset=$DATASET"
"$SP/venv/bin/python" -m provider_bank.build \
  --dataset "$DATASET" \
  --data-root "$SP/round2/A/data" \
  --out "$SP/round2/A/runs/pilot/provider_bank/bank" \
  --jobs 8 --subsets 8
echo "done $(date -u)"
