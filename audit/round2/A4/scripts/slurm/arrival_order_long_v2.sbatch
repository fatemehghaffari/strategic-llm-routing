#!/bin/bash
# Long horizon (3e7): 10 subsets x 2 orders x 3 mechanisms = 60 tasks, proposed and Cao equilibrium, 5 seeds.
# Subsets: fixed quantile rule on ctx_benefit_subsets.csv (Q7) plus the three A4 contextual triples.
#SBATCH --job-name=a4_v2_long
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --array=0-59
#SBATCH --output=<scratch>/ctxbenefit/logs/%x_%A_%a.out
set -euo pipefail
PY=<scratch>/venv/bin/python
OUT=<scratch>/ctxbenefit/raw
cd <repo>/audit/round2/A4/scripts
i=${SLURM_ARRAY_TASK_ID}
MECHS=(second_best mesp_scalar plmesp); ORDERS=(iid bursty)
m=${MECHS[$((i % 3))]}; o=${ORDERS[$(((i / 3) % 2))]}; n=30000000; s=$((i / 6))
SUB=$(sed -n "$((s + 1))p" arrival_order_subsets_v2.txt)
$PY arrival_order_v2.py --subset "$SUB" --n $n --nseeds 5 --orders $o --mechs $m \
  --out $OUT/v2_long_${SUB%%=*}_${o}_${n}_${m}.csv --trace-dir <workspace>/v2
