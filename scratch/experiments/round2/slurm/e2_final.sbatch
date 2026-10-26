#!/bin/bash
#SBATCH -J e2-ladder-final
#SBATCH -p cpu
#SBATCH -A ${SLURM_ACCOUNT:?set SLURM_ACCOUNT}
#SBATCH -c 16
#SBATCH --mem=16G
#SBATCH -t 06:00:00
#SBATCH -o ${R2_WORK}/round2/A/logs/%x-%j.out
set -euo pipefail
# Portable paths. Set these before submitting:
#   R2_CODE_ROOT  the checkout holding scratch/experiments/round2
#   R2_WORK       a writable scratch directory for runs, logs and the venv
: "${R2_CODE_ROOT:?set R2_CODE_ROOT}" "${R2_WORK:?set R2_WORK}"
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
S=${R2_WORK}/round2/A
S=${R2_WORK}/round2/A
V=${R2_WORK}/venv/bin/python
cd ${R2_CODE_ROOT}/scratch/experiments/round2
$V ablations/run_ladder.py --instances unique_top tied_top near_gap honest_top --n 2000 8000 20000 50000 \
  --reps 200 --phase final --workers 16 --out $S/runs/final/ablations
