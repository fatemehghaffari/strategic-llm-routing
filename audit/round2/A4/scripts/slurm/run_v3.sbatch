#!/bin/bash
# v3 grids (A5, Agent B). Usage: sbatch --array=0-(N-1)%80 slurm/run_v3.sbatch <tasklist>
#SBATCH --job-name=a5_v3
#SBATCH --partition=cpu-preempt
#SBATCH --requeue
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --time=06:00:00
#SBATCH --output=<scratch>/B/logs/%x_%A_%a.out
set -euo pipefail
PY=<scratch>/venv/bin/python
OUT=<scratch>/B/raw
TR=<workspace>/v3/B
cd <repo>/audit/round2/A4/scripts
LINE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$1")
read -r ITEM LAB TS RULES PROFS ORDER N SEED0 NSEEDS <<< "${LINE%%|*}"
SUB="${LINE#*|}"
TAG=$(echo "${ITEM}_${LAB}_${TS}_${RULES}_${PROFS}_${ORDER}_${N}_s${SEED0}" | tr ',' '+' | cut -c1-200)
$PY run_v3.py --subset "$SUB" --taskset $TS --n $N --seed0 $SEED0 --nseeds $NSEEDS --orders $ORDER \
  --rules $RULES --profiles $PROFS --out $OUT/$TAG.csv --trace-dir $TR
