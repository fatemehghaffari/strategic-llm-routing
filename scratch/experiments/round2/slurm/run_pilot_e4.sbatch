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
SP=${R2_WORK}
WT=${R2_CODE_ROOT}
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=8
export PYTHONPATH="$WT/scratch/experiments/round2"
echo "host=$(hostname) date=$(date -u)"
"$SP/venv/bin/python" -m provider_bank.run_pilot \
  --bank "$SP/round2/A/runs/pilot/provider_bank/bank" \
  --out "$SP/round2/A/runs/pilot/provider_bank/pilot" \
  --datasets fashion_mnist covertype \
  --reps 20 --horizons 2000 8000 20000 200000
echo "done $(date -u)"
