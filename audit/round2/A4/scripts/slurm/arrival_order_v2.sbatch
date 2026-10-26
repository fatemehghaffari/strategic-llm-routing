#!/bin/bash
# Arrival-order experiment: 10 subsets x 4 orders x 2 horizons x 3 mechanisms = 240 tasks.
# Subsets: fixed quantile rule on ctx_benefit_subsets.csv (Q7) plus the three A4 contextual triples.
#SBATCH --job-name=a4_v2
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --array=0-239%80
#SBATCH --output=<scratch>/ctxbenefit/logs/%x_%A_%a.out
set -euo pipefail
PY=<scratch>/venv/bin/python
OUT=<scratch>/ctxbenefit/raw
cd <repo>/audit/round2/A4/scripts
i=${SLURM_ARRAY_TASK_ID}
MECHS=(second_best mesp_scalar plmesp); ORDERS=(iid bursty drift grouped); NS=(300000 3000000)
m=${MECHS[$((i % 3))]}; o=${ORDERS[$(((i / 3) % 4))]}; n=${NS[$(((i / 12) % 2))]}; s=$((i / 24))
SUB=$(sed -n "$((s + 1))p" arrival_order_subsets_v2.txt)
$PY arrival_order_v2.py --subset "$SUB" --n $n --nseeds 20 --orders $o --mechs $m \
  --out $OUT/v2_order_${SUB%%=*}_${o}_${n}_${m}.csv --trace-dir <workspace>/v2
