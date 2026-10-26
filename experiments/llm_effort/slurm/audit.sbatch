#!/bin/bash
#SBATCH --job-name=llm_audit
#SBATCH --partition=gpu-preempt
#SBATCH --requeue
#SBATCH --gres=gpu:1
#SBATCH --constraint=l40s|a100|h100
#SBATCH --account=<slurm-account>
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=01:00:00
#SBATCH --output=<workspace>/llm_effort/logs/%x-%j.out
# Stage 7 audit: rerun the first 25 evaluation questions per benchmark under every budget, seed 0, from the saved configs
set -euo pipefail
W=<workspace>/llm_effort; OUT=$W/results/audit/seed0; mkdir -p "$OUT"
echo "host $(hostname)  date $(date -u +%FT%TZ)"; nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
module load cuda/13.1 2>/dev/null || module load cuda/12.8 2>/dev/null || true
export FLASHINFER_DISABLE_VERSION_CHECK=1 HF_HOME=$W/hf HF_HUB_OFFLINE=1 VLLM_LOGGING_LEVEL=WARNING PATH=$W/venv/bin:$PATH
cd <repo>/experiments/llm_effort
python src/run_experiment.py --config configs/model.json --tasks configs/tasks.csv --split evaluation --mode fixed --seeds 0 --limit 25 --out "$OUT"
echo "done $(date -u +%FT%TZ)"
