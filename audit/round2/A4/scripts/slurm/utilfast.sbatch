#!/bin/bash
#SBATCH --job-name=a4_utilfast
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=06:00:00
#SBATCH --array=0-5
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# A focused companion to a4_util: the same design constants, restricted to the
# cells section 4.5 of the report quotes, so those numbers do not have to wait
# for the full grid.
SP=<scratch>
cd $SP/llm
case ${SLURM_ARRAY_TASK_ID} in
  0) ARGS="--contexts MMLU --dups 0 --roles top,runner_up,third --rules mesp --crosscheck 0";;
  1) ARGS="--contexts GSM8K --dups 0 --roles top,runner_up,third --rules mesp --crosscheck 0";;
  2) ARGS="--contexts MMLU --dups 0 --roles top --rules mesp,router_ucb,router_eps,router_greedy --crosscheck 1";;
  3) ARGS="--contexts GSM8K --dups 0 --roles top --rules mesp,router_ucb,router_eps,router_greedy --crosscheck 1";;
  4) ARGS="--contexts MMLU --dups 1 --roles top,runner_up --rules mesp --crosscheck 0";;
  5) ARGS="--contexts GSM8K --dups 1 --roles top,runner_up --rules mesp --crosscheck 0";;
esac
$SP/venv/bin/python utility_curves.py --n 200000 --nseeds 8 --grid 61 --alpha a0.50 \
  $ARGS --out $SP/llm/raw/utilfast_${SLURM_ARRAY_TASK_ID}.csv
