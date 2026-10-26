# Final scalar performance experiment

Run `python3 run.py --reps 120`, then `python3 plot.py`. Each instance-horizon
cell uses the same deterministic seed for every method, giving 120 paired
replications. `trials.csv` contains every trial and seed; `summary.csv` contains
means and percentile 95% bootstrap intervals (4,000 resamples), and
`paired_comparisons.csv` contains paired MESP-F-minus-baseline contrasts with
paired bootstrap intervals.

The four instances all contain at least one honest arm. MESP-F exactly follows
the manuscript's bidding length, conservative empirical second price,
cumulative monitor, and fresh explicit-exploration EXP3 fallback. Capacity UCB
is an optimistic nonstrategic benchmark; intrinsic UCB is the no-effort
baseline; the oracle knows capacities and continuously obtains the second-price
target. Figures are untitled vector PDF/SVG files and use a consistent
colorblind-safe method palette.
