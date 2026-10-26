#!/bin/bash
#SBATCH -J e2-ladder-pilot
#SBATCH -p cpu
#SBATCH -A ${SLURM_ACCOUNT:?set SLURM_ACCOUNT}
#SBATCH -c 8
#SBATCH --mem=8G
#SBATCH -t 02:00:00
#SBATCH -o ${R2_WORK}/round2/A/logs/%x-%j.out
set -euo pipefail
# Portable paths. Set these before submitting:
#   R2_CODE_ROOT  the checkout holding scratch/experiments/round2
#   R2_WORK       a writable scratch directory for runs, logs and the venv
: "${R2_CODE_ROOT:?set R2_CODE_ROOT}" "${R2_WORK:?set R2_WORK}"
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
S=${R2_WORK}/round2/A
V=${R2_WORK}/venv/bin/python
cd ${R2_CODE_ROOT}/scratch/experiments/round2
$V ablations/run_ladder.py --instances unique_top tied_top honest_top --n 2000 20000 --reps 40 --phase pilot --workers 8 --out $S/runs/pilot/ablations
