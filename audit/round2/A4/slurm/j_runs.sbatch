#!/bin/bash
#SBATCH --job-name=j_traces
#SBATCH --partition=cpu-preempt
#SBATCH --requeue
#SBATCH --account=<slurm-account>
#SBATCH --array=0-11
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --time=03:00:00
#SBATCH --output=<workspace>/J/logs/%x-%A_%a.out
# task 0: n = 20,000, seeds 0-9, every mechanism      -> J/n20k_r2
# tasks 1-10: n = 300,000, one seed each, every mechanism -> J/n300k
# task 11: Cao et al.'s phase split against n (J4 data)   -> J/cao_phases.csv
set -euo pipefail
echo "host $(hostname)  date $(date -u +%FT%TZ)  task ${SLURM_ARRAY_TASK_ID}"; module list 2>&1 | head -3 || true
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=<scratch>/venv/bin/python
S=<repo>/audit/round2/A4/scripts
J=<workspace>/J
"$PY" --version
T=${SLURM_ARRAY_TASK_ID}
if [ "$T" -eq 0 ]; then
  "$PY" "$S/j_traces.py" --n 20000 --seeds 0-9 --out "$J/n20k_r2"
elif [ "$T" -le 10 ]; then
  "$PY" "$S/j_traces.py" --n 300000 --seeds $((T-1)) --out "$J/n300k"
else
  "$PY" "$S/j_cao_phases.py" --out "$J/cao_phases.csv"
fi
echo "done $(date -u +%FT%TZ)"
