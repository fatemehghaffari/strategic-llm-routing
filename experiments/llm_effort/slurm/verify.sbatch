#!/bin/bash
#SBATCH --job-name=llm_verify
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint=l40s|a100|h100
#SBATCH --account=<slurm-account>
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=00:40:00
#SBATCH --output=<workspace>/llm_effort/logs/%x-%j.out
set -euo pipefail
echo "host $(hostname)  date $(date -u +%FT%TZ)"; nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv
module load cuda/13.1 2>/dev/null || module load cuda/12.8 2>/dev/null || true; export CUDA_HOME=${CUDA_HOME:-$(dirname $(dirname $(which nvcc 2>/dev/null || echo /usr/local/cuda/bin/nvcc)))}; echo "nvcc: $(which nvcc 2>/dev/null || echo none) CUDA_HOME=$CUDA_HOME"
export FLASHINFER_DISABLE_VERSION_CHECK=1 HF_HOME=<workspace>/llm_effort/hf HF_HUB_OFFLINE=1 VLLM_LOGGING_LEVEL=WARNING
<workspace>/llm_effort/venv/bin/python --version
<workspace>/llm_effort/venv/bin/python -c "import torch; print('torch', torch.__version__, 'cuda available', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')"
<workspace>/llm_effort/venv/bin/python <repo>/experiments/llm_effort/src/verify_budget.py <repo>/experiments/llm_effort/configs/model.json
echo "done $(date -u +%FT%TZ)"
