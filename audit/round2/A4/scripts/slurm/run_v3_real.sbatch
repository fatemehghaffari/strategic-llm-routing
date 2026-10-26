#!/bin/bash
# Real WildChat arrival order, the one order A5 could not run because the stream did not yet exist.
# Usage: sbatch --array=0-389%390 slurm/run_v3_real.sbatch tasks_v3_real.txt
#SBATCH --job-name=a5_real
#SBATCH --partition=cpu
#SBATCH --qos=normal
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --time=08:00:00
#SBATCH --output=<scratch>/real/logs/%x_%A_%a.out
set -euo pipefail
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
echo "host $(hostname)  date $(date -u +%FT%TZ)  task $SLURM_ARRAY_TASK_ID"
PY=<scratch>/venv/bin/python
OUT=<scratch>/real/raw
TR=<workspace>/v3/real
cd <repo>/audit/round2/A4/scripts
$PY --version
LINE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$1")
read -r ITEM LAB TS RULES PROFS ORDER N SEED0 NSEEDS <<< "${LINE%%|*}"
SUB="${LINE#*|}"
TAG=$(echo "${ITEM}_${LAB}_${TS}_${RULES}_${PROFS}_${ORDER}_${N}_s${SEED0}" | tr ',' '+' | cut -c1-200)
$PY run_v3.py --subset "$SUB" --taskset $TS --n $N --seed0 $SEED0 --nseeds $NSEEDS --orders $ORDER \
  --rules $RULES --profiles $PROFS --out $OUT/$TAG.csv --trace-dir $TR
echo "done $(date -u +%FT%TZ)"
