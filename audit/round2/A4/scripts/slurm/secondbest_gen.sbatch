#!/bin/bash
#SBATCH --job-name=a4_sbgen
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=08:00:00
#SBATCH --array=0-21
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# Sensitivity to the one ambiguity in their pseudocode: whether line 21's
# "if validated" gates blind trust phase II as well as phase I. This run takes
# the reading GENEROUS to them, in which phase II still runs after the monitor
# fires, so the two readings can be compared rather than asserted.
SP=<scratch>
cd $SP/llm
$SP/venv/bin/python baseline_secondbest.py --n 300000 --nseeds 20 --gate-blind2 0 \
  --alphas a0.00,a0.25,a0.50,a0.75,het \
  --shard ${SLURM_ARRAY_TASK_ID} --nshards 22 \
  --out $SP/llm/raw/secondbestgen_${SLURM_ARRAY_TASK_ID}.csv
