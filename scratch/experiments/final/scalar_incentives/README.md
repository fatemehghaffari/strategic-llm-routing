# Final scalar-incentive experiment

Run from the repository root:

```bash
python3 scratch/experiments/final/scalar_incentives/run.py
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/mespf-mpl \
  python3 scratch/experiments/final/scalar_incentives/plot.py
```

Defaults use 120 paired CRN repetitions per cell and 240 for tied-top and
low-gap non-top cells, horizons 2,000, 8,000, and 20,000, and fixed master
seed 20260828. `trials.csv` contains every run; `paired_summary.csv` contains
paired differences and percentile bootstrap 95% confidence intervals.

PDF and SVG figures have no embedded title. All MESP-F curves use the global
dark-blue method color `#0072B2`; unilateral deviations are distinguished by
line style and marker. Utility comparisons are exported both as absolute
paired gain and as gain normalized by the horizon. Every instance includes at
least one honest arm.
