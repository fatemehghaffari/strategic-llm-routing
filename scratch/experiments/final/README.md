# Final experimental suite

The retained artifacts were generated with Python 3.13.15, NumPy 2.3.1, and
Matplotlib 3.11.1. All commands are run from the repository root.

```bash
python3 scratch/experiments/final/scalar_incentives/run.py --reps 120 --tied-reps 240 --horizons 2000 8000 20000 --seed 20260828 --workers 3
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/mespf-final python3 scratch/experiments/final/scalar_incentives/plot.py
python3 scratch/experiments/final/scalar_performance/run.py --reps 120
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/scalar-performance-final python3 scratch/experiments/final/scalar_performance/plot.py
python3 scratch/experiments/final/contextual_performance/run.py --reps 100 --workers 3
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/contextual-performance-final python3 scratch/experiments/final/contextual_performance/plot.py
python3 scratch/experiments/final/contextual_incentives/run.py --reps 240 --workers 3
python3 scratch/experiments/final/contextual_incentives/validate.py
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/contextual-incentives-final python3 scratch/experiments/final/contextual_incentives/plot.py
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/final-composites python3 scratch/experiments/final/make_composites.py
```

Every subdirectory contains trial-level raw CSV data, summaries, vector PDF
and SVG figures, and its implementation. The two recommended main-paper
composites are `main_incentives` and `main_performance`. Figures contain no
titles; TeX captions and labels are in `audit/experiments/final/CAPTIONS.tex`.
The method palette is global and colorblind-safe, with markers and line styles
as redundant encodings.
