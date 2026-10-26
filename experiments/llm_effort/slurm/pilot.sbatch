#!/bin/bash
#SBATCH --job-name=llm_pilot
#SBATCH --partition=gpu-preempt
#SBATCH --requeue
#SBATCH --gres=gpu:1
#SBATCH --constraint=l40s|a100|h100
#SBATCH --account=<slurm-account>
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=01:00:00
#SBATCH --output=<workspace>/llm_effort/logs/%x-%j.out
set -euo pipefail
echo "host $(hostname)  date $(date -u +%FT%TZ)"; nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
module load cuda/13.1 2>/dev/null || module load cuda/12.8 2>/dev/null || true
export FLASHINFER_DISABLE_VERSION_CHECK=1 HF_HOME=<workspace>/llm_effort/hf HF_HUB_OFFLINE=1 VLLM_LOGGING_LEVEL=WARNING PATH=<workspace>/llm_effort/venv/bin:$PATH
cd <repo>/experiments/llm_effort
<workspace>/llm_effort/venv/bin/python src/run_experiment.py --config configs/model.json --tasks configs/tasks.csv --split calibration --mode fixed --seeds 0 --limit 10 --out <workspace>/llm_effort/results/pilot2
echo "done $(date -u +%FT%TZ)"
