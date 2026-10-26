# Continuous contextual incentive experiment

Run `python3 run.py --workers 3`, `python3 validate.py`, and then `MPLBACKEND=Agg python3 plot.py`. The default is 240 paired common-random-number trials for each of five deviations at each horizon. `trials.csv` retains every trial and `summary.csv` gives paired bootstrap 95% confidence intervals.

The full profile is uniform on `[0,1]^3`, with `K=3`, `d=1`, and therefore `D=Kd=3`. Each intrinsic mean and capacity depends only on that arm's local context and is continuous. The closed null set is `B={x:x_1=1/2}`; its complement has two connected components. On both components the constant top set is exactly arms `{1,2}`, tied at capacity `0.72`; arm 3 has capacity `0.53+0.08x_3<0.72`. Each deviation is a feasible deterministic map fixed before play; the random-fixed treatment draws its measurable map independently before play and then holds it fixed.

Static Grid-ETC uses theorem-rate `h=n^{-1/(D+3)}` and `q=ceil(n^{2/(D+3)})`, independent random exploration permutations, cell priorities independent of rewards, and no exploitation updates. Figures deliberately contain no titles because captions belong in LaTeX. Grid-ETC is encoded by green (`#009E73`); deviation types have consistent colors and markers.
