#!/bin/bash
#SBATCH --job-name=a4_utilwin
#SBATCH --partition=cpu
#SBATCH --account=<slurm-account>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=12:00:00
#SBATCH --array=0-7
#SBATCH --output=%x_%A_%a.out
set -euo pipefail
# Utility against effort at a seed count high enough for the win event to
# average out, WITH the win probability recorded as a second series.  The step
# in the utility curve is the win event; this makes that visible instead of
# leaving it to look like noise.
SP=<scratch>
cd $SP/llm
CTX=(MMLU MMLU MMLU MMLU GSM8K GSM8K GSM8K GSM8K)
DUP=(0    0    1    1    0     0     1     1)
ROL=(top  runner_up top runner_up top runner_up top runner_up)
I=${SLURM_ARRAY_TASK_ID}
$SP/venv/bin/python utility_curves.py --n 200000 --nseeds 24 --grid 61 --alpha a0.50 \
  --contexts ${CTX[$I]} --dups ${DUP[$I]} --roles ${ROL[$I]} \
  --rules mesp,router_ucb --crosscheck 0 \
  --out $SP/llm/raw/utilwin_${I}.csv
