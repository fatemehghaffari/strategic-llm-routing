#!/bin/bash
#SBATCH -J e1-search
#SBATCH -p cpu
#SBATCH -A ${SLURM_ACCOUNT:?set SLURM_ACCOUNT}
#SBATCH -c 1
#SBATCH --mem=4G
#SBATCH -t 04:00:00
#SBATCH -o ${R2_WORK}/round2/A/logs/%x-%A_%a.out
set -euo pipefail
# Portable paths. Set these before submitting:
#   R2_CODE_ROOT  the checkout holding scratch/experiments/round2
#   R2_WORK       a writable scratch directory for runs, logs and the venv
: "${R2_CODE_ROOT:?set R2_CODE_ROOT}" "${R2_WORK:?set R2_WORK}"
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
S=${R2_WORK}/round2/A
V=${R2_WORK}/venv/bin/python
LINE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" $S/slurm/e1_search_tasks.txt)
INST=$(echo $LINE | cut -d' ' -f1); N=$(echo $LINE | cut -d' ' -f2); CLS=$(echo $LINE | cut -d' ' -f3); G=$(echo $LINE | cut -d' ' -f4)
cd ${R2_CODE_ROOT}/scratch/experiments/round2
$V exploitability/search.py --instance $INST --n $N --class $CLS --restarts 4 --gens $G --pop 16 --batch 64 \
   --eval-reps 2000 --out $S/runs/final/search
