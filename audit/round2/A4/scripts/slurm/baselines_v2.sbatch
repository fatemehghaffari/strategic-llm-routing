#!/bin/bash
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=<scratch>/ctxbenefit/logs/%x_%A_%a.out
#SBATCH --job-name=a4_blv2
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --array=0-319%100
set -euo pipefail
PY=<scratch>/venv/bin/python
OUT=<scratch>/ctxbenefit/raw
cd <repo>/audit/round2/A4/scripts
i=${SLURM_ARRAY_TASK_ID}
RULES=(router_greedy router_eps router_ucb esmaeili)
# Baselines v2: 10 subsets x 4 orders x 2 horizons x 4 rules = 320 tasks, 20 seeds, full traces.
ORDERS=(iid bursty drift grouped); NS=(300000 3000000)
m=${RULES[$((i % 4))]}; o=${ORDERS[$(((i / 4) % 4))]}; n=${NS[$(((i / 16) % 2))]}; s=$((i / 32))
SUB=$(sed -n "$((s + 1))p" arrival_order_subsets_v2.txt)
$PY baselines_v2.py --subset "$SUB" --n $n --nseeds 20 --orders $o --rules $m \
  --out $OUT/v2bl_order_${SUB%%=*}_${o}_${n}_${m}.csv --trace-dir <workspace>/v2
