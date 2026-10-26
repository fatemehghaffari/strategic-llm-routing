#!/bin/bash
# Re-aggregate, regenerate the figures and the tables, splice the tables into the report at the
# <!--A3TABLES--> marker, and copy the CSVs and the vector figures into audit/round2/A3/.
set -eu
S=<scratch>/round2/A3
R=<repo>
CODE=$R/scratch/experiments/round2/ctx_fast
V=<scratch>/venv/bin/python
export PYTHONDONTWRITEBYTECODE=1
$V "$CODE/aggregate.py"       --results "$S/results" --out "$S/csv"
# the aggregated CSVs go into the repository first; every figure and every quoted number is built
# from THOSE, never from the raw per-run JSON, so a restyle costs seconds and no compute
mkdir -p "$R/experiments/data/A3"
cp "$S/csv/threshold_summary.csv" "$S/csv/threshold_sweep.csv" "$R/experiments/data/A3/"
$V "$CODE/make_figures_a3.py" --csv "$R/experiments/data/A3" --out "$S/figures" --dim 1
$V "$CODE/report_tables.py"   --csv "$R/experiments/data/A3" \
    --verification "$S/verification.json" "$S/verification_d1.json" > "$S/tables.md"
$V - "$R/audit/round2/A3/THRESHOLD_REPORT.md" "$S/tables.md" <<'PY'
import sys
rep, tab = sys.argv[1], sys.argv[2]
t = open(rep).read()
body = open(tab).read().strip()
M = "<!--A3TABLES-->"
E = "<!--/A3TABLES-->"
block = M + "\n\n" + body + "\n\n" + E
if M in t and E in t:
    i, j = t.index(M), t.index(E) + len(E)
    t = t[:i] + block + t[j:]
elif M in t:
    t = t.replace(M, block, 1)
else:
    raise SystemExit("marker not found")
open(rep, "w").write(t)
print("report tables spliced")
PY
mkdir -p "$R/audit/round2/A3/csv" "$R/audit/round2/A3/figures"
cp "$S/csv/threshold_summary.csv" "$S/csv/threshold_sweep.csv" "$R/audit/round2/A3/csv/"
[ -f "$S/verification_d1.json" ] && cp "$S/verification_d1.json" "$R/audit/round2/A3/verification_d1.json"
cp "$S/figures/continuous_threshold.pdf" "$S/figures/continuous_threshold_supp.pdf" \
   "$S/figures/continuous_threshold_dim.pdf" "$R/audit/round2/A3/figures/"
mkdir -p "$R/experiments/data/A3/figures_generated"
cp "$S/figures/"*.pdf "$R/experiments/data/A3/figures_generated/"
cp "$S/verification.json" "$R/audit/round2/A3/verification.json"
[ -f "$S/verification_v2.json" ] && cp "$S/verification_v2.json" "$R/audit/round2/A3/verification_v2.json"
echo "copied CSVs, figures and verification records into audit/round2/A3/"
