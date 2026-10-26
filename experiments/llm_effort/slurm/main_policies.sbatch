#!/bin/bash
#SBATCH --job-name=llm_main_policies
#SBATCH --partition=gpu-preempt
#SBATCH --requeue
#SBATCH --array=0-2
#SBATCH --gres=gpu:1
#SBATCH --constraint=l40s|a100|h100
#SBATCH --account=<slurm-account>
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=02:30:00
#SBATCH --output=<workspace>/llm_effort/logs/%x-%A_%a.out
# policies run on the evaluation split (150 GSM8K + 150 MATH-500 questions); one seed per array task
set -euo pipefail
W=<workspace>/llm_effort
SEED=${SLURM_ARRAY_TASK_ID}; OUT=$W/results/main_policies/seed$SEED; mkdir -p "$OUT"
echo "host $(hostname)  date $(date -u +%FT%TZ)  seed $SEED"; nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
# GPU power sampler (1 Hz) for the whole job; the first 20 s are idle, before the model loads
nvidia-smi --query-gpu=timestamp,power.draw,utilization.gpu,memory.used --format=csv,noheader,nounits -l 1 > "$OUT/gpu_power.csv" &
PW=$!; sleep 20
module load cuda/13.1 2>/dev/null || module load cuda/12.8 2>/dev/null || true
export FLASHINFER_DISABLE_VERSION_CHECK=1 HF_HOME=$W/hf HF_HUB_OFFLINE=1 VLLM_LOGGING_LEVEL=WARNING PATH=$W/venv/bin:$PATH
cd <repo>/experiments/llm_effort
which python && python --version; python -c "import vllm, torch; print('vllm', vllm.__version__, 'torch', torch.__version__)"
python src/run_experiment.py --config configs/model.json --tasks configs/tasks.csv --split evaluation --seeds $SEED --mode policies --policies fixed_low,fixed_medium,fixed_high,task_adaptive,random_matched --out "$OUT"
kill $PW 2>/dev/null || true
echo "done $(date -u +%FT%TZ)"
