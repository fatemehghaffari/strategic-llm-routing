# Final contextual-performance experiments

This directory contains the reproducible contextual learning comparison used
for internal paper evaluation. It is not included in the manuscript.

Run from the repository root:

```bash
python3 scratch/experiments/final/contextual_performance/run.py --reps 100 --workers 3
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/mpl-contextual-final \
  python3 scratch/experiments/final/contextual_performance/plot.py
```

`trials.csv` contains every method-run. `summary.csv` contains nonparametric
bootstrap 95% confidence intervals. `paired_comparisons.csv` contains paired
bootstrap differences in oracle regret relative to LinUCB. Each plotted cell
has 100 independent trials; methods within a trial share context paths and
arm-by-round reward uniforms. Seeds are deterministic.

The methods are exact finite-context UCB, cell-local Static Grid-UCB, Static
Grid-ETC with exploration-only feedback, context-blind UCB, and disjoint
full-profile LinUCB. The continuous environments are exactly linear, smooth
nonlinear, and discontinuous checkerboard families. Full-profile dimensions
are `D=2` and `D=6`; the finite family uses `D=2`. The grid sensitivity study
uses width multipliers 0.75, 1, and 1.5 at horizon 8,000.

Every arm's intrinsic mean and capacity depend only on that arm's local
context, as required by the manuscript model. In the exactly linear family,
`M_i(x_i)` is arm-specific and affine in `x_i`. Full-profile LinUCB is given
all `D` coordinates, so its cross-arm coefficients are irrelevant zeros.

The plotted oracle regret is based on conditional expected rewards, while each
algorithm learns from Bernoulli outcomes. This removes irrelevant evaluation
noise without changing algorithm behavior. Honest shortfall is relative to
the best intrinsic mean. Effort is delivered mean minus intrinsic mean.

LinUCB is a stronger-assumption statistical comparator, not a strategic
mechanism. Its advantage in the exactly linear family should not be read as a
like-for-like theorem comparison.

Figures are PDF and SVG, have no embedded titles, and use the common palette:
Grid-UCB orange, Grid-ETC green, LinUCB purple, global UCB gray, and
finite-context UCB sky blue. Markers supplement color coding.
