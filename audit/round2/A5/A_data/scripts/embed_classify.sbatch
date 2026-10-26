#!/bin/bash
#SBATCH --job-name=a5_emb
#SBATCH --partition=gpu-preempt
#SBATCH --account=<slurm-account>
#SBATCH --gpus=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --requeue
#SBATCH --output=<workspace>/logs/%x_%j.out
set -euo pipefail
export HF_HOME=<workspace>/hf_home HF_HUB_OFFLINE=1
nvidia-smi --query-gpu=name,memory.total --format=csv
<workspace>/venv_embed/bin/python <repo>/audit/round2/A5/A_data/scripts/embed_classify.py <workspace>
