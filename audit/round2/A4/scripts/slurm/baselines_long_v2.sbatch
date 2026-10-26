#!/bin/bash
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=<scratch>/ctxbenefit/logs/%x_%A_%a.out
#SBATCH --job-name=a4_blv2L
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --array=0-79
set -euo pipefail
PY=<scratch>/venv/bin/python
OUT=<scratch>/ctxbenefit/raw
cd <repo>/audit/round2/A4/scripts
i=${SLURM_ARRAY_TASK_ID}
RULES=(router_greedy router_eps router_ucb esmaeili)
# Baselines v2, long horizon 3e7: 10 subsets x 2 orders x 4 rules = 80 tasks, 5 seeds, full traces.
ORDERS=(iid bursty)
m=${RULES[$((i % 4))]}; o=${ORDERS[$(((i / 4) % 2))]}; n=30000000; s=$((i / 8))
SUB=$(sed -n "$((s + 1))p" arrival_order_subsets_v2.txt)
$PY baselines_v2.py --subset "$SUB" --n $n --nseeds 5 --orders $o --rules $m \
  --out $OUT/v2bl_long_${SUB%%=*}_${o}_${n}_${m}.csv --trace-dir <workspace>/v2
