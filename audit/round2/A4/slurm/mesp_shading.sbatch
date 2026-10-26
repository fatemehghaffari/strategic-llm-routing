#!/bin/bash
#SBATCH --job-name=mesp_shading
#SBATCH --partition=cpu-preempt
#SBATCH --requeue
#SBATCH --account=<slurm-account>
#SBATCH --array=0-39
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --time=04:00:00
#SBATCH --output=<workspace>/mesp_shading/logs/%x-%A_%a.out
# MESP (context-local) against the routers' slow and fast effort-reduction schedules, the ten real-order
# subsets, both horizons, real and independent arrivals. task = subset (10) x horizon (2) x order (2).
set -euo pipefail
echo "host $(hostname)  date $(date -u +%FT%TZ)  task ${SLURM_ARRAY_TASK_ID}"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=<scratch>/venv/bin/python
S=<repo>/audit/round2/A4/scripts
W=<workspace>/mesp_shading
T=${SLURM_ARRAY_TASK_ID}; SUB=$(sed -n "$((T % 10 + 1))p" "$W/tasks.txt"); H=$(( (T / 10) % 2 )); O=$(( T / 20 ))
N=$([ "$H" -eq 0 ] && echo 300000 || echo 3000000); NS=$([ "$H" -eq 0 ] && echo 20 || echo 10); ORDER=$([ "$O" -eq 0 ] && echo real || echo iid)
LABEL=${SUB%%=*}; echo "subset $LABEL n=$N seeds=$NS order=$ORDER"
cd "$S" && "$PY" run_v3.py --subset "$SUB" --taskset merged5 --n "$N" --nseeds "$NS" --orders "$ORDER" --rules plmesp --profiles exploit_slow,exploit_fast --out "$W/out/${LABEL}_n${N}_${ORDER}.csv"
echo "done $(date -u +%FT%TZ)"
