#!/bin/bash
#SBATCH -p cpu
#SBATCH -A <slurm-account>
#SBATCH -c 4
#SBATCH --mem=8G
#SBATCH -t 05:00:00
#SBATCH -o <scratch>/round2/e1/logs/%x-%j.out
# Usage: sbatch -J <tag> run_e1.sh <instance> <bids> <tag> <n1> [n2 ...]
set -euo pipefail
REPO=<repo>
VENV=<scratch>/venv/bin/python
OUT=<scratch>/round2/e1
INST=$1; BIDS=$2; TAG=$3; shift 3
export PYTHONDONTWRITEBYTECODE=1
for n in "$@"; do
  echo "=== $INST $BIDS $TAG n=$n ==="
  $VENV "$REPO/audit/round2/B/theorems/e1-equilibrium-strength/bidprofile.py" \
        --instance "$INST" --bids "$BIDS" --tag "$TAG" --n "$n" --out "$OUT"
done
