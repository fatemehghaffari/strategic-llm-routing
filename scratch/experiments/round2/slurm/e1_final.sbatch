#!/bin/bash
#SBATCH -J e1-dp-final
#SBATCH -p cpu
#SBATCH -A ${SLURM_ACCOUNT:?set SLURM_ACCOUNT}
#SBATCH -c 2
#SBATCH --mem=12G
#SBATCH -t 03:00:00
#SBATCH -o ${R2_WORK}/round2/A/logs/%x-%A_%a.out
set -euo pipefail
# Portable paths. Set these before submitting:
#   R2_CODE_ROOT  the checkout holding scratch/experiments/round2
#   R2_WORK       a writable scratch directory for runs, logs and the venv
: "${R2_CODE_ROOT:?set R2_CODE_ROOT}" "${R2_WORK:?set R2_WORK}"
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2
S=${R2_WORK}/round2/A
V=${R2_WORK}/venv/bin/python
CODE=${R2_CODE_ROOT}/scratch/experiments/round2
LINE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" $S/slurm/e1_tasks.txt)
INST=$(echo $LINE | cut -d' ' -f1); N=$(echo $LINE | cut -d' ' -f2); POL=$(echo $LINE | cut -d' ' -f3)
cd $CODE
if [ "$POL" = "1" ]; then
  $V exploitability/dp.py --instance $INST --n $N --out $S/runs/final/exploitability --policy
else
  $V exploitability/dp.py --instance $INST --n $N --out $S/runs/final/exploitability
fi
