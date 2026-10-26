# A3. CG-MESP run at and around the horizon at which its own thresholds say it starts to work

*(synthetic simulation at the mechanism's own tuned parameters, plus exact computation of its
parameter formulas; 24 September 2026, revised the same day for the common-context model)*

**Files.** Code (written by this package; nothing canonical is touched):
`scratch/experiments/round2/ctx_fast/` holds `cgmesp.c`, `cgmesp_v2.c` and `cgmesp_v3.c` (the
kernel, three builds), `cgfast.py` (the ctypes driver and the instance table), `verify.py` and
`verify_d1.py` (bit-equality against the slow reference), `sweep_run.py` (one episode),
`make_tasks.py`, `aggregate.py`, `report_tables.py`, `reach_table.py`, `make_figures_a3.py` and
`assemble.sh`. **Aggregated data, committed:** `experiments/data/A3/threshold_summary.csv` (one row
per instance, dimension and horizon) and `experiments/data/A3/threshold_sweep.csv` (one row per
run), with the generated figures in `experiments/data/A3/figures_generated/`. The figure script
reads those CSVs and never the raw output, so a restyle costs seconds and no compute. Vector figures
also in `audit/round2/A3/figures/`; verification records in `audit/round2/A3/verification*.json`;
Slurm record in `audit/round2/A3/COMPUTE_LOG.md`. Raw per-run JSON stays in
`<scratchpad>/round2/A3/results/`.

> **Erratum (25 Oct 2026).** The part (C) slack in `scratch/experiments/round2/ctx_fast/cgfast.py` uses
> `e_rob = n(4 s_n + (5/3) rho_n)`, while Proposition `prop:ctx-continuum-exact`(iii) gives
> `e_price = n(4 s_n + (4/3) rho_n)`. With the proposition's constant the part (C) threshold at `d = 1`
> (instance C, K = 2) is predicted at `10^6.93` and evaluated between `10^6.90` (slack/n = 1.016) and `10^7.00`
> (0.967), not `10^7.14`; the paper's threshold table uses the corrected values. Every `10^7.14` for part (C)
> below refers to the looser 5/3 accounting. Parts (A) and (B) and the activation rows are unaffected.

## 0. The headline, first

**The mechanism starts working, and it starts working where the thresholds say it does.** In the
revised model, where all `K` agents face one common context per round and the mechanism grids
`[0,1)^d`, the `d = 1` thresholds are `10^5.25` for part (A), `10^6.06` for a price that can be
positive on any instance, `10^6.76` for part (B) and `10^7.14` for part (C). The sweep runs from
`10^5` to `10^9` and crosses all four. What it finds:

* **The price turns on at `10^6.50` to `10^6.70`**, which is exactly where the instance's own
  crossing `sigma_n < beta_(2)` is predicted: `10^6.53` to `10^6.58` on instance C. The measured
  share of regions with a positive price is 0.000 at `10^6.40`, **0.029** at `10^6.50`, **0.872** at
  `10^6.60` and **1.000** from `10^6.70`.
* **Revenue stops falling and starts rising at the same horizon.** On instance C the platform
  collects 0.0990 per round at `10^5`, falling to a minimum of **0.0421 at `10^6.50`**, then rising
  to 0.0855, 0.1737, 0.2970, 0.4003 and **0.5494 at `10^9`**, against a second-capacity benchmark of
  0.7900. The minimum sits at the horizon where the price turns on, not anywhere else.
* **The monitor turns on with the price.** A winner that delivers nothing is convicted at **no**
  region up to `10^6.40`, at 0.194 of regions at `10^6.60`, and at **every** region from `10^6.70`.
  Under the proposed profile the monitor fired **zero** times, at every instance, dimension, horizon
  and seed, and **no compliant winner was ever convicted anywhere in the sweep**.
* **All three guarantees are vacuous below their thresholds and satisfied with margin above them.**
  On instance C the part (A) budget per round crosses 1 between `10^5.25` (1.15 at `10^5.00`, 1.00
  at `10^5.25`, 0.87 at `10^5.50`), part (B) between `10^6.70` and `10^6.80` (1.03 and 0.98) and
  part (C) at `10^7.14` (1.00), against predictions of `10^5.25`, `10^6.76` and `10^7.14`. At every
  horizon the realised deviation gain, the realised revenue deficit and the realised
  honest-benchmark deficit are inside the corresponding bound.
* **The same prediction is confirmed at three dimensions, spanning 5.3 decades of horizon.** The
  price turns on at `10^6.50` at `d = 1` (predicted `10^6.53`), at `10^9.10` at `d = 2` (predicted
  `10^9.10`) and at `10^11.80` at `d = 3` (predicted `10^11.78`): on instance D at `d = 3` the share
  of regions with a positive price is 0.000 at `10^11.70`, **0.378 at `10^11.80`** and 1.000 at
  `10^11.90`.
* **The threshold is set by `d` and not by `K`, as claimed.** Instances C and E have `K = 2` and
  instances D and F have `K = 3`. At `d = 1` all four turn the price on between `10^6.50` and
  `10^6.90`; at `d = 2`, C (`K = 2`) and D (`K = 3`) both turn it on at `10^9.10`, with shares of
  0.320 and 0.340 there and `sigma_n` differing by 0.001. The `K = 2` and `K = 3` curves at a fixed
  `d` lie on top of each other; consecutive dimensions are 2.6 to 2.7 decades apart, which is what
  the parameter formulas predict.

Nothing was tuned. The mechanism was run at its own `h_n = 1/ceil(n^{1/(d+3)})`,
`L_n = ceil(n^{2/(d+3)})` and `rho_n = sqrt(d) h_n log(e n)`, on the four instances the
smaller-horizon work used, with the six unilateral deviations and the joint sabotage profile it
used.

Three things qualify that, and all three belong in the paper.

1. **Non-vacuous is not tight.** At `10^9`, the largest `d = 1` horizon run, the platform collects
   0.5494 per round against a benchmark of 0.7900. The mechanism prices at
   `tau = beta_(2) - sigma_n` and a compliant winner delivers exactly `tau`, so the shortfall is
   very nearly `sigma_n`, which is still 0.244 at `10^9` and decays only like
   `n^{-1/(d+3)} log n`. Part (B) holds, and it holds because its slack per round is exactly
   `(4/3) sigma_n` plus the elicitation term `K J_n L_n / n`. The guarantee is real and it is loose
   in exactly the way the analysis says.
2. **There is a fourth threshold, above all three analytic ones, and the paper should quote it.**
   Below the threshold a price of zero makes compliance worthless, so the platform collects *more*
   when every strategic agent sabotages than when everyone complies: on instance C at `d = 1` and
   `10^6`, 0.3058 per round under total sabotage against 0.0555 under compliance. The proposed
   profile first overtakes total sabotage between `10^7.50` (0.2970 against 0.3026) and `10^7.75`
   (0.3522 against 0.3022), which is 0.4 decades above the `10^7.14` at which the last of the three
   guarantees becomes non-vacuous.
3. **The dimension still bites, just 2.6 decades later per unit.** `d = 1` costs a few seconds of
   one core. `d = 2` costs about two minutes and was run to `10^10.5`. `d = 3` costs about two days
   and was launched. `d = 4` needs a grid of `7.6 x 10^8` cells, which is 109 GB of cell state
   before any horizon is run, and about 13 core-years. Section 7 gives the table. Since the revised
   model has `d` the context dimension rather than `K d`, `d = 4` now means a genuinely
   four-dimensional context rather than two agents with two-dimensional ones, which is a much
   weaker requirement on the model and a much better position for the paper.

## 1. The model change, and what it did to this package

The model this package was first pointed at gave each agent its own context coordinate, so the
mechanism gridded a profile space of dimension `K d` and every constant carried `K d`. The revised
model gives all `K` agents one common context per round, and the mechanism grids `[0,1)^d`.

**Nothing in the kernel had to change except one index.** In the kernel, agent `j` reads coordinate
`j mod dctx` of the round's context, and the grid has `g^dctx` cells. Setting `dctx = K` is the old
model exactly; setting `dctx = 1` is the common-context model. The two readings coincide bit for bit
at `dctx = K`, which is checked, so the `d = 2` sweep run before the change is still valid: it is
the revised mechanism on a two-dimensional common context in which agent `j` happens to depend on
coordinate `j`. That is a legitimate Lipschitz instance and nothing about it needs re-running. The
same is true of the `d = 3` runs in flight.

**What did have to change is where the sweep was pointed.** The interesting range moved from
`10^8.5` to `10^10.5` down to `10^5` to `10^7.5`, and the `d = 1` sweep, 5632 runs, cost 2.8 core
hours in total. It is now the centrepiece and the `d = 2` and `d = 3` sweeps are the dimension
study.

**What was run.**

* `d = 1`, instances C and E (`K = 2`) and D and F (`K = 3`): 22 horizons from `10^5.00` to
  `10^9.00`, eight behaviour profiles, eight seeds. 5632 runs, complete.
* `d = 2`, instances C and E (`K = 2`): 16 horizons from `10^6` to `10^10.5`, eight profiles, four
  seeds. 1024 runs, complete.
* `d = 2`, instances D and F (`K = 3`): 15 horizons from `10^7` to `10^10.5`, eight profiles, four
  seeds, launched as job 64827948 to test that the threshold moves with `d` and not with `K`.
* `d = 3`, instances D and F (`K = 3`): `10^7` to `10^12.3`, job 64823290. Complete through
  `10^12.00`, which is past the instance-D price turn-on at `10^11.80`; the `10^12.3` points and
  the `10^12.64` stretch runs (job 64823292) were still running.
* `d = 4`, instance G (`K = 4`, defined in this package and nowhere else): `10^9` to `10^12`, a
  probe below the threshold.

**The authority on what returned is the coverage line and the per-instance tables at the end of
Section 4, which are generated from the result files.** Every sentence of prose here is about rows
that are in those tables.

## 2. The fast implementation, and its verification against the slow one

The reference is `run()` in `scratch/experiments/round2/ctx_local/cg_struct.py`, which is read only
for this package and was not modified. At about 40 microseconds per round it reaches `2 x 10^6`
rounds. That is comfortably past the `d = 1` thresholds and four orders of magnitude short of
the `d = 2` ones, so the slow implementation could in principle have found the `d = 1` transition on
its own; nobody had pointed it there.

`scratch/experiments/round2/ctx_fast/cgmesp.c` is a line-for-line C port of it, driven from Python
through `ctypes` (`cgfast.py`). It is compiled with `-O2 -ffp-contract=off -fno-fast-math` and no
`-march=native`: contraction is off because `M_j(x) = a + b x` is a fused-multiply-add candidate and
an FMA would make the C arithmetic differ from numpy's in the last bit, and `-march=native` is off
so that the binary is the same on every node. Every derived parameter (`g`, `L_n`, `ell_n`, `s_n`,
`rho_n`, `sigma_n`) is computed in Python by the reference's own expressions and passed in, so no
parameter can drift between the two implementations.

**How the comparison is made.** The reference is not edited and not copied. `np.random.default_rng`
is intercepted by a recorder that forwards every call to the real Generator and stores what came
out: the `(n, K)` context matrix, the `(n,)` seed vector, every priority permutation in creation
order, and, for every Stage-3 fallback draw, the single uniform that `Generator.choice(K, p = p)`
consumes. The C kernel is then run in replay mode on exactly those draws.

Three things were checked before the comparison could mean anything.

* The recorder's re-implementation of `Generator.choice(K, p = p)` (cumulative sum, normalise by the
  last entry, `searchsorted` to the right, clip to `K - 1`, one `random()` draw) returns the same
  index as numpy's on 18000 random `(K, p)` pairs with `K` from 2 to 5, and leaves the stream in the
  same place. Running the reference with and without the recorder gives identical output on every
  field.
* Every integer-valued quantity is compared for exact equality, and the floating sums are compared
  against an uncompensated accumulator in the C kernel that adds in the same order as the reference,
  so "identical" means identical and not "identical to a tolerance".
* The comparison is not allowed to be a comparison of zeros. Cases were added until the suite
  contains awarded cubes, positive prices, monitor firings, Stage-3 fallback rounds, and nonzero
  Lemma P2 violation counts (the last needs `3 s_n` driven below the within-cube oscillation, which
  takes `L = 200000` and `2 x 10^7` rounds of the reference).

A second build, `cgmesp_v2.c`, was needed because the first is memory bound once the grid stops
fitting in cache: at `d = 3` and `10^12` the grid has about `10^6` cells and v1 runs at 123 to 157
nanoseconds per round, which would have overrun the time limits. v2 changes only memory layout and
scheduling: the fields a Stage-2 round touches are packed into one 64-byte line and the Stage-1 bid
counters and Stage-3 weights moved to a second array; both arrays are 2 MB aligned and marked
`MADV_HUGEPAGE`; and each arrival is drawn eight rounds early, from its own independent stream,
purely so that its cell can be prefetched. The arithmetic and the draw order are unchanged, and
v1 and v2 are checked bit for bit against each other as well as each against the reference. The
alignment and huge-page hint are most of the gain: at `8 x 10^5` cells they take the kernel from
123.5 to 34.7 nanoseconds per round, and at `6.25 x 10^6` cells from 156.7 to 59.3.

A third build, `cgmesp_v3.c`, adds the one thing the revised model needs: `dctx`, the dimension of
the context space the mechanism grids, which the model separates from `K`. The grid is over
`[0,1)^dctx` and agent `j` reads coordinate `j mod dctx` of the round's context. `dctx = K` is the
old reading and `dctx = 1` the common-context one. `dctx` is the **last** field of the configuration
struct, so the two older builds, which know nothing about it, see an unchanged layout and keep
running correctly in jobs that were already in the queue.

**Result.** Every case of every suite is bit-identical, on every integer count, on the naive
floating sums, and on the announced prices, for all three builds. Section 5 has the detail, including
one suite that passed and was thrown away for being vacuous.

## 3. The traps at this scale, and what was done about each

* **Floating-point drift in the monitoring sums.** Rewards are 0 or 1, so every reward sum is an
  integer counter: `uint64` for platform revenue and per-phase revenue, `int64` for each cube's
  Stage-1 bid sums and for the cumulative monitor statistic `Z_r`. No rounding error can enter the
  monitor test or the revenue at any horizon. The two benchmark sums and the `K` utility sums are
  not 0/1, and they are accumulated twice: naively, so the reference can be reproduced bit for bit,
  and by Neumaier compensated summation, which is what the sweep reports. The two are reported
  together and the gap is tabulated in Section 4: it grows from `10^-9` absolute at `10^6` rounds to
  0.25 at `3 x 10^10` and 8.9 at `10^11`, which is `10^-10` of the sum, so the naive accumulator
  would still have been fine for the quantities reported here and would not have been fine for a
  quantity that is a small difference of two such sums. Had the reward sums been left in floating
  point they would sit at the same relative error, and the monitor test `Z_r < r tau - b_n(r)`
  compares two numbers whose difference is `O(sqrt(r))`, so this is the place where it would have
  mattered. It cannot, because `Z_r` is an `int64`.
* **Random number quality and period.** Three independent xoshiro256++ streams (period `2^256 - 1`,
  seeded through SplitMix64 and warmed), one for arrivals, one for the Bernoulli seeds, one for the
  mechanism's own draws. The longest run uses about `1.3 x 10^11` draws, which is `10^-66` of the
  period, and the whole sweep about `10^13`. Three streams rather than one so that the arrival path and the seed sequence are identical
  across deviation runs at a fixed seed: that is the pairing the reference gets for free by drawing
  `Xs` and `U` in advance, and the deviation gains reported below are paired differences at equal
  seed.
* **Memory growth from lazily created regions.** The grid is deterministic and its size is known
  from `n` and `D`, so cells are a flat preallocated array indexed arithmetically, not a dictionary
  that grows. Nothing is allocated inside the round loop and the resident set is constant for the
  whole run.
* **Timing that does not extrapolate.** Throughput is not a single constant. It depends on the grid
  size, because the access is a random walk over the cell array: 20.5 nanoseconds per round while
  the grid fits in cache and 59.3 nanoseconds per round at `6.25 x 10^6` cells, measured on one
  machine with everything else held fixed. It also depends on which node the task landed on: over
  the sweep runs with `n >= 10^9` the median is 35.1 nanoseconds per round on the `cpu` nodes, 40.6
  on `umd-cscdr-cpu`, 44.8 on `uri-cpu` and 54.2 on the older `gypsum` nodes, with a full range of
  18.7 to 201.3. The reach table in Section 7 therefore uses throughput measured as a function of
  the number of cells on one machine, and is a lower bound on the cost on a mixed pool; had it used
  the small-grid rate it would have understated the `d = 4` time by about a factor of three, and it
  is the memory, not the time, that makes `D >= 4` impossible anyway.

## 4. The sweep

Every row below is the mechanism at its own tuned parameters. Columns, in order: the horizon; the
grid side `g_n` and the number of cells `J_n = g_n^D`; the bidding block `L_n`; the shading
`sigma_n = 3 s_n + rho_n`; the share of awarded regions at which the announced price
`tau_C = (beta_(2),C - sigma_n)_+` is strictly positive, under the proposed profile; the mean
announced price over awarded regions; the number of times the monitor fired under the proposed
profile, summed over every seed; the platform's realised revenue per round and the second-capacity
benchmark `M_(2)` per round; the three error terms divided by `n`, which are below 1 exactly when
the corresponding guarantee says something; the best realised gain per round over the six unilateral
deviations tried; and the realised part (B) and part (C) deficits per round.

**How to read the deviation columns.** Gains are paired: the deviator's total utility in the
deviation run minus its total utility in the proposed run at the same seed, with the same context
path and the same Bernoulli seeds. They are **lower bounds on exploitability for the six deviations
tried** and are not evidence of equilibrium. The deviations are the ones the smaller-horizon work
used: shade the Stage-1 target to the midpoint between own capacity and the best alternative
(`underbid`); ride the monitor boundary at scales 0.25, 0.5 and 1.0 (`rider25`, `rider50`,
`rider100`); both together (`both`); and deliver nothing from the moment of winning (`crash`). Part
(C) is the separate profile in which **every** strategic agent delivers its floor in every phase.

**The `d = 2` sweep is the same prediction, checked at a different dimension.** The `d = 2`
crossings are `10^9.10` to `10^9.16` on instance C and `10^8.78` to `10^9.44` on instance E, against
a `sigma_n < 1` threshold of `10^8.49`. The sweep measures the first positive price at `10^9.10`
(0.320 of regions) on C, with 0.999 at `10^9.20` and 1.000 at `10^9.30`; and at `10^9.00` (0.141) on
E, with nothing at `10^8.75` and 1.000 at `10^9.50`. Prediction and observation agree at every one
of those four points too, 2.6 decades higher than at `d = 1`.

**What the sweep shows, in words.** Numbers are `d = 1` unless a dimension is named.

1. **The price turns on where the instance's own crossing is, and the two published thresholds mean
   different things.** The parameter threshold `10^6.06` is where `sigma_n < 1`; 1 enters only
   because an empirical bid can never exceed 1, so `sigma_n >= 1` forces a price of zero on **every**
   instance. It is a necessary condition, not a crossing. The crossing is `sigma_n < beta_(2),C`,
   and `beta_(2),C` concentrates on the second capacity over the cube. The table below puts the
   prediction next to the measurement, and they agree at every point to the resolution of the sweep
   grid.

| instance | K | second capacity | predicted: first region prices | predicted: all regions price | observed: first positive | observed: all positive |
|--|--:|--:|--:|--:|--:|--:|
| C | 2 | `[0.780, 0.800]` | `10^6.53` | `10^6.58` | `10^6.50` (0.029) | `10^6.70` (1.000), 0.872 at `10^6.60` |
| D | 3 | `[0.787, 0.800]` | `10^6.53` | `10^6.57` | `10^6.50` (0.026) | `10^6.70` (1.000), 0.981 at `10^6.60` |
| E | 2 | `[0.700, 0.800]` | `10^6.53` | `10^6.83` | `10^6.50` (0.003) | `10^6.90` (1.000), 0.939 at `10^6.80` |
| F | 3 | `[0.700, 0.720]` | `10^6.76` | `10^6.83` | `10^6.70` (0.008) | `10^6.90` (1.000), 0.689 at `10^6.80` |

   The 0.45-decade gap between `10^6.06` and `10^6.50` is not a discrepancy. It is the difference
   between a bound that must hold on every instance and the crossing of a particular one, and the
   paper should quote both and say which is which.

2. **The threshold is a function of `d` alone and `K` does not move it.** Instances C and E have
   `K = 2`, instances D and F have `K = 3`, and all four cross within 0.2 of a decade of each other
   at `d = 1`. The parameter `sigma_n` differs between `K = 2` and `K = 3` only through
   `ell_n = log(2K) + 5 log n`: at `10^6.5` it is 0.810 for `K = 2` and 0.812 for `K = 3`, a
   difference of 0.002. The cleanest form of the test puts instance C (`K = 2`) beside instance D
   (`K = 3`), whose second capacities agree to within 0.007, at both dimensions:

| d | instance | K | share with a positive price at successive horizons |
|--:|--:|--:|:--|
| 1 | C | 2 | 0.000 at `10^6.40`, **0.029** at `10^6.50`, 0.872 at `10^6.60`, 1.000 at `10^6.70` |
| 1 | D | 3 | 0.000 at `10^6.40`, **0.026** at `10^6.50`, 0.981 at `10^6.60`, 1.000 at `10^6.70` |
| 2 | C | 2 | 0.000 at `10^9.00`, **0.320** at `10^9.10`, 0.999 at `10^9.20`, 1.000 at `10^9.30` |
| 2 | D | 3 | 0.000 at `10^9.00`, **0.340** at `10^9.10`, 1.000 at `10^9.20`, 1.000 at `10^9.30` |

   The `d = 2` pair is the sharpest form of the test, because both sweeps have a point inside the
   transition: 0.320 of regions at `K = 2` against 0.340 at `K = 3`, at the same horizon, with
   `sigma_n` differing by 0.001. Doubling the dimension moves the turn-on by 2.6 decades; adding an
   agent moves it by less than the 0.1-decade resolution of the sweep grid. This is the claim the
   revised model makes and the sweep confirms it directly.

   The `d = 3` sweep adds a third rung to the same ladder. On instance D the predicted crossing is
   `10^11.78` to `10^11.85`, and the measured share is 0.000 at `10^11.70`, **0.378** at `10^11.80`
   and 1.000 at `10^11.90`. On instance F, whose second capacity is `[0.700, 0.720]`, the predicted
   crossing is `10^12.10` to `10^12.20`, and the share is still 0.000 at `10^12.00`, which is where
   it should be. Across three dimensions the prediction is right at every point checked, over 5.3
   decades of horizon.

3. **Revenue falls, bottoms out exactly at the turn-on, and then rises, at every dimension.** At
   `d = 3` on instance D the platform collects 0.1837, 0.1248, 0.0826, 0.0564, 0.0467, 0.0384,
   0.0310 and **0.0291** per round at `10^7.00` through `10^11.70`, and then 0.0292, 0.0508 and
   0.0686 at `10^11.80`, `10^11.90` and `10^12.00`: the minimum sits one tenth of a decade below
   the turn-on, exactly as at `d = 1` and `d = 2`. At `d = 1` on instance C the platform
   collects 0.0990, 0.0866, 0.0742, 0.0648, 0.0555, 0.0496, 0.0438 and **0.0421** per round at
   `10^5.00` through `10^6.50`, and then 0.0511, 0.0855, 0.1167, 0.1459, 0.1737, 0.2370, 0.2970,
   0.4003, 0.4837 and **0.5494** at `10^6.60` through `10^9.00`, against a benchmark of 0.7900. The
   minimum is at `10^6.50`, the horizon at which the price first becomes positive. The same shape
   appears on instance D (minimum 0.0610 at `10^6.50`, rising to 0.5524 at `10^9`) and on instance E
   (minimum 0.1569 at `10^6.50`, rising to 0.5091). On instance F the honest agent is the top agent
   and delivers more than the benchmark at every horizon, so revenue is flat and high throughout;
   that is a property of instance F and not evidence about the mechanism.

4. **Where the revenue comes from changes completely at the threshold.** Below it, all of the
   platform's revenue comes from the Stage-1 elicitation blocks and none from the priced phase,
   because a compliant strategic winner delivers `min{0, M_W} = 0`. Above it the priced phase
   supplies almost all of it. At `d = 2` on instance C the split is 0.0283 from elicitation and
   0.0000 from pricing at `10^9`, against 0.0138 and 0.3160 at `10^10.5`, with elicitation 1.6 per
   cent of the horizon.

5. **The monitor is inert below the threshold and works above it.** A price of zero cannot be
   undercut, so below the threshold the monitor cannot fire against any behaviour, and it does not:
   on instance C the crash deviation, which delivers nothing from the moment of winning, is
   convicted at **no** region at every horizon up to `10^6.40`, at 0.194 of regions at `10^6.60` and
   at **every** region from `10^6.70`. Riding the monitor boundary at scale 1 is convicted at 0.003
   of regions at `10^6.70`, rising to 0.989 at `10^9.00`. On instance E the same curves saturate at
   one half, and that is arithmetic, not weakness: the deviating agent is agent 0, whose capacity
   `0.70 + 0.20 x` beats agent 1's `0.90 - 0.20 x` on exactly half the context space, so it is the
   winner at half the regions and cannot be convicted at the other half; the measured saturation is
   0.499 to 0.504. **Instance F carries no information about deviations at all**, and this is an
   inherited defect of the deviation harness rather than a result: in F the honest agent is agent 0
   and every deviation in this package is played by agent 0, so on F the "deviator" is the honest
   agent and every deviation reduces to honesty. F's deviation and conviction columns should be
   read as blank, not as zero. The same choice was made by the smaller-horizon package and it was
   wrong there too.
   Across every instance, dimension, horizon, profile and seed there was **not one false alarm**,
   and the proposed profile never triggered a single switch. Be honest about which half of that is
   informative. The false-alarm half is what Lemma P6 predicts: the boundary is
   `b_n(r) = sqrt(r ell_n / 2)`, a single false alarm has probability `e^{-ell_n} = 1/(2 K n^5)`,
   and the union bound over `J_n n` pairs leaves about `n^{-3}`. Observing zero is a consistency
   check, not evidence. The informative half is the **power**: until the price is positive the
   monitor cannot convict anybody, so the enforcement device the whole equilibrium argument rests on
   was inert at every horizon that had ever been run, and this is the first evidence that it does
   anything at all.

6. **The searched deviations stay far inside the part (A) budget, and the dangerous one is dangerous
   only in a narrow window.** On instance C the best realised gain per round is 0.0044 at `10^5`,
   decays to 0.0020 at `10^6.40`, **peaks at 0.0171 at `10^6.70`**, and decays again to 0.0020 at
   `10^9`. The budget at `10^6.70` is 0.46 per round, so the worst realised gain is under 4 per cent
   of the budget. The deviation that attains the peak is riding the monitor boundary at scale 1, and
   it attains it exactly where the price has just turned on and is still small relative to the
   boundary increment; a little higher it is already losing, because the monitor convicts it at a
   rising share of regions. Crashing gains exactly zero below the threshold, since a price of zero
   means a compliant strategic winner was delivering zero anyway, and loses heavily above it.
   Shading the Stage-1 bid is the only deviation that pays at every horizon, and it pays a few
   thousandths per round while the budget is between 0.14 and 1.15.

7. **All three guarantees are vacuous below their thresholds and satisfied with margin above.** The
   measured crossings of the trivial bound `n`, on instance C at `d = 1`, are: part (A) between
   `10^5.25` (1.00) and `10^5.50` (0.87), predicted `10^5.25`; part (B) between `10^6.70` (1.03) and
   `10^6.80` (0.98), predicted `10^6.76`; part (C) at `10^7.14` (1.00), predicted `10^7.14`. On
   instance D, with `K = 3`, part (A) crosses between `10^5.25` (1.12) and `10^5.50` (0.97),
   predicted `10^5.45`. Above their thresholds all three hold at every horizon and every instance:
   the realised deviation gain against the part (A) budget, the realised `M_(2)` revenue deficit
   against the part (B) slack, and the realised honest-benchmark deficit against the part (C) slack.
   Below their thresholds the inequalities are still satisfied, but they say nothing, because a
   bound above `n` is weaker than the trivial bound.

8. **Part (B) is loose by construction and the paper should say so.** The realised revenue deficit
   is very nearly `sigma_n` per round, because a compliant winner delivers the announced price and
   the announced price is the second bid minus `sigma_n`. The slack per round is
   `K J_n L_n / n + 4 s_n + (4/3) rho_n`, and `4 s_n + (4/3) rho_n` is exactly `(4/3) sigma_n`. The
   inequality therefore holds with a margin of about a third of the shading plus the elicitation
   term. Part (B) is not a statement that this mechanism nearly extracts `M_(2)` at any runnable
   horizon; it is a statement that its shortfall is the shading, which is true and which the sweep
   confirms numerically.

9. **The two price lemmas hold at the mechanism's own parameters, and the test is no longer
   vacuous.** Over the proposed-profile runs of the whole sweep there are millions of awarded cubes
   and hundreds of thousands with a strictly positive price, and there is **not one** violation of
   Lemma P2 (the winner can meet the announced price at every context of its cube) or of Lemma P4
   (the price is not far below the second capacity). Below the threshold this check says nothing,
   because a price of zero satisfies Lemma P2 for any capacity; the positive-price cubes are the
   part that carries information.

10. **Below its threshold the mechanism is worse for the platform than total sabotage.** With
    `tau_C = 0` a compliant strategic winner delivers nothing, whereas under total sabotage every
    strategic agent bids 0, the honest agent's bid `mu` wins every region, and the honest agent then
    delivers `mu` every round. On instance C at `d = 1` the platform collects 0.3058 per round under
    total sabotage and 0.0555 under compliance at `10^6`. Compliance first overtakes sabotage
    between `10^7.50` (0.2970 against 0.3026) and `10^7.75` (0.3522 against 0.3022). That is the
    honest operational threshold, and it is 0.4 decades above the last of the three analytic ones.

<!--A3TABLES-->

**Coverage.** Horizons for which the proposed profile has returned, by context dimension and instance:

* d = 1, instance C (K = 2): 5.00, 5.25, 5.50, 5.75, 6.00, 6.10, 6.20, 6.30, 6.40, 6.50, 6.60, 6.70, 6.80, 6.90, 7.00, 7.14, 7.25, 7.50, 7.75, 8.00, 8.50, 9.00
* d = 1, instance E (K = 2): 5.00, 5.25, 5.50, 5.75, 6.00, 6.10, 6.20, 6.30, 6.40, 6.50, 6.60, 6.70, 6.80, 6.90, 7.00, 7.14, 7.25, 7.50, 7.75, 8.00, 8.50, 9.00
* d = 1, instance D (K = 3): 5.00, 5.25, 5.50, 5.75, 6.00, 6.10, 6.20, 6.30, 6.40, 6.50, 6.60, 6.70, 6.80, 6.90, 7.00, 7.14, 7.25, 7.50, 7.75, 8.00, 8.50, 9.00
* d = 1, instance F (K = 3): 5.00, 5.25, 5.50, 5.75, 6.00, 6.10, 6.20, 6.30, 6.40, 6.50, 6.60, 6.70, 6.80, 6.90, 7.00, 7.14, 7.25, 7.50, 7.75, 8.00, 8.50, 9.00
* d = 2, instance C (K = 2): 6.00, 7.00, 7.50, 8.00, 8.25, 8.50, 8.75, 9.00, 9.10, 9.20, 9.30, 9.50, 9.80, 10.00, 10.25, 10.50
* d = 2, instance E (K = 2): 6.00, 7.00, 7.50, 8.00, 8.25, 8.50, 8.75, 9.00, 9.10, 9.20, 9.30, 9.50, 9.80, 10.00, 10.25, 10.50
* d = 2, instance D (K = 3): 7.00, 7.50, 8.00, 8.25, 8.50, 8.75, 9.00, 9.10, 9.20, 9.30, 9.50, 9.80, 10.00, 10.25, 10.50
* d = 2, instance F (K = 3): 7.00, 7.50, 8.00, 8.25, 8.50, 8.75, 9.00, 9.10, 9.20, 9.30, 9.50, 9.80, 10.00, 10.25, 10.50
* d = 3, instance D (K = 3): 7.00, 8.00, 9.00, 10.00, 10.50, 11.00, 11.50, 11.70, 11.80, 11.90, 12.00
* d = 3, instance F (K = 3): 7.00, 8.00, 9.00, 10.00, 10.50, 11.00, 11.50, 11.70, 11.80, 11.90, 12.00
* d = 4, instance G (K = 4): 9.00, 10.00, 11.00, 12.00


### d = 1, instance C (K = 2)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 5.00 | 18 | 18 | 317 | 1.610 | 0.000 | 0.0000 | 0 | 0.0990 | 0.7900 | 1.153 | 2.261 | 2.893 | 0.00442 | 0.6910 | -0.0102 |
| 5.25 | 21 | 21 | 422 | 1.435 | 0.000 | 0.0000 | 0 | 0.0866 | 0.7900 | 0.999 | 2.013 | 2.547 | 0.00386 | 0.7034 | -0.0090 |
| 5.50 | 24 | 24 | 563 | 1.289 | 0.000 | 0.0000 | 0 | 0.0742 | 0.7900 | 0.875 | 1.803 | 2.256 | 0.00331 | 0.7158 | -0.0075 |
| 5.75 | 28 | 28 | 750 | 1.145 | 0.000 | 0.0000 | 0 | 0.0648 | 0.7900 | 0.760 | 1.602 | 1.985 | 0.00289 | 0.7252 | -0.0069 |
| 6.00 | 32 | 32 | 1 000 | 1.026 | 0.000 | 0.0000 | 0 | 0.0555 | 0.7900 | 0.668 | 1.432 | 1.759 | 0.00248 | 0.7345 | -0.0058 |
| 6.10 | 34 | 34 | 1 123 | 0.978 | 0.000 | 0.0000 | 0 | 0.0526 | 0.7900 | 0.632 | 1.365 | 1.671 | 0.00235 | 0.7374 | -0.0056 |
| 6.20 | 36 | 36 | 1 259 | 0.934 | 0.000 | 0.0000 | 0 | 0.0496 | 0.7900 | 0.599 | 1.303 | 1.591 | 0.00222 | 0.7404 | -0.0053 |
| 6.30 | 38 | 38 | 1 413 | 0.893 | 0.000 | 0.0000 | 0 | 0.0467 | 0.7900 | 0.569 | 1.245 | 1.515 | 0.00209 | 0.7433 | -0.0050 |
| 6.40 | 40 | 40 | 1 585 | 0.855 | 0.000 | 0.0000 | 0 | 0.0438 | 0.7900 | 0.542 | 1.191 | 1.445 | 0.00196 | 0.7462 | -0.0048 |
| 6.50 | 43 | 43 | 1 779 | 0.810 | 0.029 | 0.0001 | 0 | 0.0421 | 0.7900 | 0.509 | 1.129 | 1.367 | 0.00214 | 0.7479 | -0.0046 |
| 6.60 | 45 | 45 | 1 996 | 0.778 | 0.872 | 0.0126 | 0 | 0.0511 | 0.7900 | 0.487 | 1.082 | 1.306 | 0.01006 | 0.7389 | -0.0043 |
| 6.70 | 48 | 48 | 2 239 | 0.739 | 1.000 | 0.0504 | 0 | 0.0855 | 0.7900 | 0.460 | 1.029 | 1.239 | 0.01711 | 0.7045 | -0.0041 |
| 6.80 | 51 | 51 | 2 512 | 0.704 | 1.000 | 0.0849 | 0 | 0.1167 | 0.7900 | 0.435 | 0.980 | 1.177 | 0.01013 | 0.6733 | -0.0038 |
| 6.90 | 54 | 54 | 2 819 | 0.672 | 1.000 | 0.1172 | 0 | 0.1459 | 0.7900 | 0.413 | 0.934 | 1.120 | 0.00947 | 0.6441 | -0.0037 |
| 7.00 | 57 | 57 | 3 163 | 0.642 | 1.000 | 0.1478 | 0 | 0.1737 | 0.7900 | 0.393 | 0.892 | 1.067 | 0.00880 | 0.6163 | -0.0034 |
| 7.14 | 61 | 61 | 3 716 | 0.604 | 1.000 | 0.1859 | 0 | 0.2083 | 0.7900 | 0.368 | 0.838 | 1.000 | 0.00789 | 0.5817 | -0.0031 |
| 7.25 | 65 | 65 | 4 217 | 0.573 | 1.000 | 0.2169 | 0 | 0.2370 | 0.7900 | 0.348 | 0.795 | 0.946 | 0.00728 | 0.5530 | -0.0030 |
| 7.50 | 75 | 75 | 5 624 | 0.509 | 1.000 | 0.2814 | 0 | 0.2970 | 0.7900 | 0.306 | 0.705 | 0.835 | 0.00604 | 0.4930 | -0.0026 |
| 7.75 | 87 | 87 | 7 499 | 0.450 | 1.000 | 0.3399 | 0 | 0.3522 | 0.7900 | 0.268 | 0.623 | 0.735 | 0.00502 | 0.4378 | -0.0022 |
| 8.00 | 100 | 100 | 10 000 | 0.399 | 1.000 | 0.3907 | 0 | 0.4003 | 0.7900 | 0.236 | 0.552 | 0.649 | 0.00415 | 0.3897 | -0.0019 |
| 8.50 | 134 | 134 | 17 783 | 0.312 | 1.000 | 0.4778 | 0 | 0.4837 | 0.7900 | 0.182 | 0.431 | 0.503 | 0.00286 | 0.3063 | -0.0014 |
| 9.00 | 178 | 178 | 31 623 | 0.244 | 1.000 | 0.5458 | 0 | 0.5494 | 0.7900 | 0.142 | 0.337 | 0.391 | 0.00196 | 0.2406 | -0.0011 |

### d = 1, instance E (K = 2)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 5.00 | 18 | 18 | 317 | 1.610 | 0.000 | 0.0000 | 0 | 0.2069 | 0.7499 | 1.153 | 2.261 | 2.893 | 0.00143 | 0.5431 | -0.0164 |
| 5.25 | 21 | 21 | 422 | 1.435 | 0.000 | 0.0000 | 0 | 0.1979 | 0.7499 | 0.999 | 2.013 | 2.547 | 0.00125 | 0.5521 | -0.0145 |
| 5.50 | 24 | 24 | 563 | 1.289 | 0.000 | 0.0000 | 0 | 0.1815 | 0.7500 | 0.875 | 1.803 | 2.256 | 0.00107 | 0.5685 | -0.0124 |
| 5.75 | 28 | 28 | 750 | 1.145 | 0.000 | 0.0000 | 0 | 0.1743 | 0.7500 | 0.760 | 1.602 | 1.985 | 0.00093 | 0.5757 | -0.0110 |
| 6.00 | 32 | 32 | 1 000 | 1.026 | 0.000 | 0.0000 | 0 | 0.1662 | 0.7500 | 0.668 | 1.432 | 1.759 | 0.00080 | 0.5838 | -0.0094 |
| 6.10 | 34 | 34 | 1 123 | 0.978 | 0.000 | 0.0000 | 0 | 0.1650 | 0.7500 | 0.632 | 1.365 | 1.671 | 0.00076 | 0.5850 | -0.0090 |
| 6.20 | 36 | 36 | 1 259 | 0.934 | 0.000 | 0.0000 | 0 | 0.1619 | 0.7500 | 0.599 | 1.303 | 1.591 | 0.00072 | 0.5881 | -0.0085 |
| 6.30 | 38 | 38 | 1 413 | 0.893 | 0.000 | 0.0000 | 0 | 0.1659 | 0.7500 | 0.569 | 1.245 | 1.515 | 0.00067 | 0.5840 | -0.0081 |
| 6.40 | 40 | 40 | 1 585 | 0.855 | 0.000 | 0.0000 | 0 | 0.1612 | 0.7500 | 0.542 | 1.191 | 1.445 | 0.00063 | 0.5888 | -0.0075 |
| 6.50 | 43 | 43 | 1 779 | 0.810 | 0.003 | 0.0000 | 0 | 0.1569 | 0.7500 | 0.509 | 1.129 | 1.367 | 0.00060 | 0.5931 | -0.0072 |
| 6.60 | 45 | 45 | 1 996 | 0.778 | 0.236 | 0.0032 | 0 | 0.1575 | 0.7500 | 0.487 | 1.082 | 1.306 | 0.00177 | 0.5925 | -0.0068 |
| 6.70 | 48 | 48 | 2 239 | 0.739 | 0.612 | 0.0182 | 0 | 0.1640 | 0.7500 | 0.460 | 1.029 | 1.239 | 0.00440 | 0.5860 | -0.0064 |
| 6.80 | 51 | 51 | 2 512 | 0.704 | 0.939 | 0.0458 | 0 | 0.1740 | 0.7500 | 0.435 | 0.980 | 1.177 | 0.00767 | 0.5759 | -0.0061 |
| 6.90 | 54 | 54 | 2 819 | 0.672 | 1.000 | 0.0771 | 0 | 0.1885 | 0.7500 | 0.413 | 0.934 | 1.120 | 0.00440 | 0.5615 | -0.0058 |
| 7.00 | 57 | 57 | 3 163 | 0.642 | 1.000 | 0.1073 | 0 | 0.2009 | 0.7500 | 0.393 | 0.892 | 1.067 | 0.00432 | 0.5491 | -0.0054 |
| 7.14 | 61 | 61 | 3 716 | 0.604 | 1.000 | 0.1456 | 0 | 0.2170 | 0.7500 | 0.368 | 0.838 | 1.000 | 0.00387 | 0.5330 | -0.0050 |
| 7.25 | 65 | 65 | 4 217 | 0.573 | 1.000 | 0.1765 | 0 | 0.2312 | 0.7500 | 0.348 | 0.795 | 0.946 | 0.00356 | 0.5188 | -0.0047 |
| 7.50 | 75 | 75 | 5 624 | 0.509 | 1.000 | 0.2411 | 0 | 0.2646 | 0.7500 | 0.306 | 0.705 | 0.835 | 0.00287 | 0.4854 | -0.0040 |
| 7.75 | 87 | 87 | 7 499 | 0.450 | 1.000 | 0.3001 | 0 | 0.3118 | 0.7500 | 0.268 | 0.623 | 0.735 | 0.00242 | 0.4382 | -0.0035 |
| 8.00 | 100 | 100 | 10 000 | 0.399 | 1.000 | 0.3507 | 0 | 0.3597 | 0.7500 | 0.236 | 0.552 | 0.649 | 0.00194 | 0.3903 | -0.0030 |
| 8.50 | 134 | 134 | 17 783 | 0.312 | 1.000 | 0.4377 | 0 | 0.4432 | 0.7500 | 0.182 | 0.431 | 0.503 | 0.00132 | 0.3068 | -0.0023 |
| 9.00 | 178 | 178 | 31 623 | 0.244 | 1.000 | 0.5057 | 0 | 0.5091 | 0.7500 | 0.142 | 0.337 | 0.391 | 0.00091 | 0.2409 | -0.0017 |

### d = 1, instance D (K = 3)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 5.00 | 18 | 18 | 317 | 1.613 | 0.000 | 0.0000 | 0 | 0.1439 | 0.7917 | 1.298 | 2.322 | 3.100 | 0.00437 | 0.6478 | 0.0067 |
| 5.25 | 21 | 21 | 422 | 1.438 | 0.000 | 0.0000 | 0 | 0.1257 | 0.7917 | 1.116 | 2.067 | 2.717 | 0.00382 | 0.6660 | 0.0060 |
| 5.50 | 24 | 24 | 563 | 1.291 | 0.000 | 0.0000 | 0 | 0.1077 | 0.7917 | 0.967 | 1.849 | 2.394 | 0.00328 | 0.6839 | 0.0052 |
| 5.75 | 28 | 28 | 750 | 1.147 | 0.000 | 0.0000 | 0 | 0.0942 | 0.7917 | 0.834 | 1.642 | 2.099 | 0.00286 | 0.6975 | 0.0044 |
| 6.00 | 32 | 32 | 1 000 | 1.028 | 0.000 | 0.0000 | 0 | 0.0806 | 0.7917 | 0.727 | 1.466 | 1.852 | 0.00245 | 0.7111 | 0.0038 |
| 6.10 | 34 | 34 | 1 123 | 0.980 | 0.000 | 0.0000 | 0 | 0.0764 | 0.7917 | 0.686 | 1.397 | 1.758 | 0.00233 | 0.7153 | 0.0035 |
| 6.20 | 36 | 36 | 1 259 | 0.936 | 0.000 | 0.0000 | 0 | 0.0721 | 0.7917 | 0.648 | 1.333 | 1.670 | 0.00219 | 0.7196 | 0.0032 |
| 6.30 | 38 | 38 | 1 413 | 0.895 | 0.000 | 0.0000 | 0 | 0.0678 | 0.7917 | 0.614 | 1.274 | 1.589 | 0.00206 | 0.7239 | 0.0031 |
| 6.40 | 40 | 40 | 1 585 | 0.856 | 0.000 | 0.0000 | 0 | 0.0636 | 0.7917 | 0.583 | 1.217 | 1.513 | 0.00194 | 0.7281 | 0.0028 |
| 6.50 | 43 | 43 | 1 779 | 0.812 | 0.026 | 0.0001 | 0 | 0.0610 | 0.7917 | 0.547 | 1.155 | 1.430 | 0.00217 | 0.7306 | 0.0027 |
| 6.60 | 45 | 45 | 1 996 | 0.779 | 0.981 | 0.0155 | 0 | 0.0712 | 0.7917 | 0.521 | 1.106 | 1.365 | 0.01219 | 0.7204 | 0.0024 |
| 6.70 | 48 | 48 | 2 239 | 0.741 | 1.000 | 0.0534 | 0 | 0.1039 | 0.7917 | 0.491 | 1.052 | 1.294 | 0.01701 | 0.6877 | 0.0023 |
| 6.80 | 51 | 51 | 2 512 | 0.705 | 1.000 | 0.0882 | 0 | 0.1340 | 0.7917 | 0.464 | 1.001 | 1.228 | 0.01005 | 0.6576 | 0.0022 |
| 6.90 | 54 | 54 | 2 819 | 0.673 | 1.000 | 0.1201 | 0 | 0.1615 | 0.7917 | 0.440 | 0.955 | 1.167 | 0.00939 | 0.6302 | 0.0021 |
| 7.00 | 57 | 57 | 3 163 | 0.643 | 1.000 | 0.1507 | 0 | 0.1880 | 0.7917 | 0.417 | 0.911 | 1.110 | 0.00874 | 0.6037 | 0.0020 |
| 7.14 | 61 | 61 | 3 716 | 0.605 | 1.000 | 0.1880 | 0 | 0.2202 | 0.7917 | 0.390 | 0.856 | 1.038 | 0.00784 | 0.5715 | 0.0018 |
| 7.25 | 65 | 65 | 4 217 | 0.574 | 1.000 | 0.2188 | 0 | 0.2476 | 0.7917 | 0.367 | 0.811 | 0.982 | 0.00723 | 0.5441 | 0.0017 |
| 7.50 | 75 | 75 | 5 624 | 0.509 | 1.000 | 0.2833 | 0 | 0.3056 | 0.7917 | 0.321 | 0.719 | 0.864 | 0.00601 | 0.4861 | 0.0014 |
| 7.75 | 87 | 87 | 7 499 | 0.450 | 1.000 | 0.3420 | 0 | 0.3593 | 0.7917 | 0.280 | 0.635 | 0.760 | 0.00500 | 0.4323 | 0.0013 |
| 8.00 | 100 | 100 | 10 000 | 0.400 | 1.000 | 0.3924 | 0 | 0.4059 | 0.7917 | 0.246 | 0.563 | 0.670 | 0.00413 | 0.3858 | 0.0011 |
| 8.50 | 134 | 134 | 17 783 | 0.312 | 1.000 | 0.4795 | 0 | 0.4877 | 0.7917 | 0.189 | 0.439 | 0.518 | 0.00285 | 0.3040 | 0.0008 |
| 9.00 | 178 | 178 | 31 623 | 0.245 | 1.000 | 0.5474 | 0 | 0.5524 | 0.7917 | 0.146 | 0.343 | 0.402 | 0.00195 | 0.2393 | 0.0006 |

### d = 1, instance F (K = 3)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 5.00 | 18 | 18 | 317 | 1.613 | 0.000 | 0.0000 | 0 | 0.7725 | 0.7100 | 1.298 | 2.322 | 3.100 | 0.00471 | -0.0625 | 0.0825 |
| 5.25 | 21 | 21 | 422 | 1.438 | 0.000 | 0.0000 | 0 | 0.7723 | 0.7100 | 1.116 | 2.067 | 2.717 | 0.00411 | -0.0623 | 0.0725 |
| 5.50 | 24 | 24 | 563 | 1.291 | 0.000 | 0.0000 | 0 | 0.7724 | 0.7100 | 0.967 | 1.849 | 2.394 | 0.00353 | -0.0624 | 0.0624 |
| 5.75 | 28 | 28 | 750 | 1.147 | 0.000 | 0.0000 | 0 | 0.7730 | 0.7100 | 0.834 | 1.642 | 2.099 | 0.00308 | -0.0630 | 0.0543 |
| 6.00 | 32 | 32 | 1 000 | 1.028 | 0.000 | 0.0000 | 0 | 0.7732 | 0.7100 | 0.727 | 1.466 | 1.852 | 0.00264 | -0.0632 | 0.0466 |
| 6.10 | 34 | 34 | 1 123 | 0.980 | 0.000 | 0.0000 | 0 | 0.7734 | 0.7100 | 0.686 | 1.397 | 1.758 | 0.00250 | -0.0634 | 0.0441 |
| 6.20 | 36 | 36 | 1 259 | 0.936 | 0.000 | 0.0000 | 0 | 0.7735 | 0.7100 | 0.648 | 1.333 | 1.670 | 0.00236 | -0.0635 | 0.0416 |
| 6.30 | 38 | 38 | 1 413 | 0.895 | 0.000 | 0.0000 | 0 | 0.7735 | 0.7100 | 0.614 | 1.274 | 1.589 | 0.00222 | -0.0635 | 0.0391 |
| 6.40 | 40 | 40 | 1 585 | 0.856 | 0.000 | 0.0000 | 0 | 0.7736 | 0.7100 | 0.583 | 1.217 | 1.513 | 0.00208 | -0.0636 | 0.0367 |
| 6.50 | 43 | 43 | 1 779 | 0.812 | 0.000 | 0.0000 | 0 | 0.7737 | 0.7100 | 0.547 | 1.155 | 1.430 | 0.00200 | -0.0637 | 0.0352 |
| 6.60 | 45 | 45 | 1 996 | 0.779 | 0.000 | 0.0000 | 0 | 0.7738 | 0.7100 | 0.521 | 1.106 | 1.365 | 0.00186 | -0.0638 | 0.0328 |
| 6.70 | 48 | 48 | 2 239 | 0.741 | 0.008 | 0.0000 | 0 | 0.7739 | 0.7100 | 0.491 | 1.052 | 1.294 | 0.00177 | -0.0639 | 0.0312 |
| 6.80 | 51 | 51 | 2 512 | 0.705 | 0.689 | 0.0067 | 0 | 0.7739 | 0.7100 | 0.464 | 1.001 | 1.228 | 0.00168 | -0.0639 | 0.0295 |
| 6.90 | 54 | 54 | 2 819 | 0.673 | 1.000 | 0.0372 | 0 | 0.7740 | 0.7100 | 0.440 | 0.955 | 1.167 | 0.00158 | -0.0640 | 0.0278 |
| 7.00 | 57 | 57 | 3 163 | 0.643 | 1.000 | 0.0672 | 0 | 0.7741 | 0.7100 | 0.417 | 0.911 | 1.110 | 0.00149 | -0.0641 | 0.0262 |
| 7.14 | 61 | 61 | 3 716 | 0.605 | 1.000 | 0.1049 | 0 | 0.7742 | 0.7100 | 0.390 | 0.856 | 1.038 | 0.00135 | -0.0642 | 0.0238 |
| 7.25 | 65 | 65 | 4 217 | 0.574 | 1.000 | 0.1355 | 0 | 0.7743 | 0.7100 | 0.367 | 0.811 | 0.982 | 0.00127 | -0.0643 | 0.0223 |
| 7.50 | 75 | 75 | 5 624 | 0.509 | 1.000 | 0.2006 | 0 | 0.7744 | 0.7100 | 0.321 | 0.719 | 0.864 | 0.00110 | -0.0644 | 0.0193 |
| 7.75 | 87 | 87 | 7 499 | 0.450 | 1.000 | 0.2597 | 0 | 0.7744 | 0.7100 | 0.280 | 0.635 | 0.760 | 0.00096 | -0.0644 | 0.0168 |
| 8.00 | 100 | 100 | 10 000 | 0.400 | 1.000 | 0.3102 | 0 | 0.7745 | 0.7100 | 0.246 | 0.563 | 0.670 | 0.00083 | -0.0645 | 0.0145 |
| 8.50 | 134 | 134 | 17 783 | 0.312 | 1.000 | 0.3975 | 0 | 0.7746 | 0.7100 | 0.189 | 0.439 | 0.518 | 0.00062 | -0.0646 | 0.0109 |
| 9.00 | 178 | 178 | 31 623 | 0.245 | 1.000 | 0.4656 | 0 | 0.7747 | 0.7100 | 0.146 | 0.343 | 0.402 | 0.00046 | -0.0647 | 0.0082 |

### d = 2, instance C (K = 2)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 6.00 | 16 | 256 | 252 | 2.431 | 0.000 | 0.0000 | 0 | 0.1120 | 0.7900 | 1.872 | 3.371 | 4.305 | 0.00000 | 0.6780 | -0.0119 |
| 7.00 | 26 | 676 | 631 | 1.696 | 0.000 | 0.0000 | 0 | 0.0740 | 0.7900 | 1.234 | 2.346 | 2.917 | 0.00331 | 0.7160 | -0.0081 |
| 7.50 | 32 | 1 024 | 1 001 | 1.435 | 0.000 | 0.0000 | 0 | 0.0562 | 0.7900 | 1.022 | 1.979 | 2.430 | 0.00251 | 0.7338 | -0.0062 |
| 8.00 | 40 | 1 600 | 1 585 | 1.202 | 0.000 | 0.0000 | 0 | 0.0440 | 0.7900 | 0.841 | 1.653 | 2.011 | 0.00197 | 0.7460 | -0.0048 |
| 8.25 | 45 | 2 025 | 1 996 | 1.095 | 0.000 | 0.0000 | 0 | 0.0394 | 0.7900 | 0.761 | 1.505 | 1.824 | 0.00176 | 0.7506 | -0.0043 |
| 8.50 | 51 | 2 601 | 2 512 | 0.992 | 0.000 | 0.0000 | 0 | 0.0359 | 0.7900 | 0.685 | 1.364 | 1.648 | 0.00160 | 0.7542 | -0.0039 |
| 8.75 | 57 | 3 249 | 3 163 | 0.906 | 0.000 | 0.0000 | 0 | 0.0317 | 0.7900 | 0.622 | 1.244 | 1.498 | 0.00142 | 0.7583 | -0.0035 |
| 9.00 | 64 | 4 096 | 3 982 | 0.824 | 0.000 | 0.0000 | 0 | 0.0283 | 0.7900 | 0.563 | 1.132 | 1.359 | 0.00126 | 0.7617 | -0.0031 |
| 9.10 | 67 | 4 489 | 4 366 | 0.794 | 0.320 | 0.0017 | 0 | 0.0287 | 0.7900 | 0.541 | 1.090 | 1.307 | 0.00238 | 0.7613 | -0.0030 |
| 9.20 | 70 | 4 900 | 4 787 | 0.766 | 0.999 | 0.0242 | 0 | 0.0492 | 0.7900 | 0.521 | 1.051 | 1.258 | 0.01068 | 0.7408 | -0.0028 |
| 9.30 | 73 | 5 329 | 5 249 | 0.739 | 1.000 | 0.0508 | 0 | 0.0737 | 0.7900 | 0.502 | 1.014 | 1.213 | 0.00684 | 0.7163 | -0.0027 |
| 9.50 | 80 | 6 400 | 6 310 | 0.685 | 1.000 | 0.1046 | 0 | 0.1241 | 0.7900 | 0.465 | 0.939 | 1.122 | 0.00615 | 0.6659 | -0.0024 |
| 9.80 | 92 | 8 464 | 8 318 | 0.611 | 1.000 | 0.1792 | 0 | 0.1945 | 0.7900 | 0.412 | 0.837 | 0.996 | 0.00517 | 0.5955 | -0.0021 |
| 10.00 | 101 | 10 201 | 10 001 | 0.565 | 1.000 | 0.2246 | 0 | 0.2377 | 0.7900 | 0.381 | 0.774 | 0.920 | 0.00459 | 0.5523 | -0.0019 |
| 10.25 | 113 | 12 769 | 12 590 | 0.514 | 1.000 | 0.2755 | 0 | 0.2862 | 0.7900 | 0.346 | 0.704 | 0.835 | 0.00393 | 0.5038 | -0.0017 |
| 10.50 | 126 | 15 876 | 15 849 | 0.469 | 1.000 | 0.3211 | 0 | 0.3298 | 0.7900 | 0.315 | 0.641 | 0.759 | 0.00336 | 0.4602 | -0.0015 |

### d = 2, instance E (K = 2)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 6.00 | 16 | 256 | 252 | 2.431 | 0.000 | 0.0000 | 0 | 0.2104 | 0.7667 | 1.872 | 3.371 | 4.305 | 0.00000 | 0.5562 | -0.0190 |
| 7.00 | 26 | 676 | 631 | 1.696 | 0.000 | 0.0000 | 0 | 0.1837 | 0.7667 | 1.234 | 2.346 | 2.917 | 0.00000 | 0.5829 | -0.0128 |
| 7.50 | 32 | 1 024 | 1 001 | 1.435 | 0.000 | 0.0000 | 0 | 0.1696 | 0.7667 | 1.022 | 1.979 | 2.430 | 0.00000 | 0.5970 | -0.0097 |
| 8.00 | 40 | 1 600 | 1 585 | 1.202 | 0.000 | 0.0000 | 0 | 0.1586 | 0.7667 | 0.841 | 1.653 | 2.011 | 0.00000 | 0.6081 | -0.0076 |
| 8.25 | 45 | 2 025 | 1 996 | 1.095 | 0.000 | 0.0000 | 0 | 0.1566 | 0.7667 | 0.761 | 1.505 | 1.824 | 0.00000 | 0.6101 | -0.0068 |
| 8.50 | 51 | 2 601 | 2 512 | 0.992 | 0.000 | 0.0000 | 0 | 0.1535 | 0.7667 | 0.685 | 1.364 | 1.648 | 0.00000 | 0.6132 | -0.0062 |
| 8.75 | 57 | 3 249 | 3 163 | 0.906 | 0.000 | 0.0000 | 0 | 0.1495 | 0.7667 | 0.622 | 1.244 | 1.498 | 0.00000 | 0.6171 | -0.0055 |
| 9.00 | 64 | 4 096 | 3 982 | 0.824 | 0.141 | 0.0036 | 0 | 0.1487 | 0.7667 | 0.563 | 1.132 | 1.359 | 0.00075 | 0.6180 | -0.0049 |
| 9.10 | 67 | 4 489 | 4 366 | 0.794 | 0.280 | 0.0099 | 0 | 0.1507 | 0.7667 | 0.541 | 1.090 | 1.307 | 0.00083 | 0.6160 | -0.0047 |
| 9.20 | 70 | 4 900 | 4 787 | 0.766 | 0.450 | 0.0202 | 0 | 0.1547 | 0.7667 | 0.521 | 1.051 | 1.258 | 0.00129 | 0.6119 | -0.0044 |
| 9.30 | 73 | 5 329 | 5 249 | 0.739 | 0.646 | 0.0347 | 0 | 0.1608 | 0.7667 | 0.502 | 1.014 | 1.213 | 0.00177 | 0.6059 | -0.0042 |
| 9.50 | 80 | 6 400 | 6 310 | 0.685 | 1.000 | 0.0811 | 0 | 0.1818 | 0.7667 | 0.465 | 0.939 | 1.122 | 0.00256 | 0.5849 | -0.0038 |
| 9.80 | 92 | 8 464 | 8 318 | 0.611 | 1.000 | 0.1558 | 0 | 0.2164 | 0.7667 | 0.412 | 0.837 | 0.996 | 0.00215 | 0.5503 | -0.0033 |
| 10.00 | 101 | 10 201 | 10 001 | 0.565 | 1.000 | 0.2012 | 0 | 0.2398 | 0.7667 | 0.381 | 0.774 | 0.920 | 0.00191 | 0.5269 | -0.0031 |
| 10.25 | 113 | 12 769 | 12 590 | 0.514 | 1.000 | 0.2521 | 0 | 0.2712 | 0.7667 | 0.346 | 0.704 | 0.835 | 0.00162 | 0.4955 | -0.0027 |
| 10.50 | 126 | 15 876 | 15 849 | 0.469 | 1.000 | 0.2977 | 0 | 0.3066 | 0.7667 | 0.315 | 0.641 | 0.759 | 0.00137 | 0.4601 | -0.0024 |

### d = 2, instance D (K = 3)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 7.00 | 26 | 676 | 631 | 1.698 | 0.000 | 0.0000 | 0 | 0.1075 | 0.7908 | 1.322 | 2.391 | 3.050 | 0.00329 | 0.6834 | 0.0047 |
| 7.50 | 32 | 1 024 | 1 001 | 1.437 | 0.000 | 0.0000 | 0 | 0.0817 | 0.7908 | 1.082 | 2.013 | 2.524 | 0.00250 | 0.7092 | 0.0035 |
| 8.00 | 40 | 1 600 | 1 585 | 1.203 | 0.000 | 0.0000 | 0 | 0.0639 | 0.7908 | 0.883 | 1.680 | 2.080 | 0.00195 | 0.7269 | 0.0028 |
| 8.25 | 45 | 2 025 | 1 996 | 1.096 | 0.000 | 0.0000 | 0 | 0.0573 | 0.7908 | 0.796 | 1.529 | 1.883 | 0.00175 | 0.7336 | 0.0025 |
| 8.50 | 51 | 2 601 | 2 512 | 0.993 | 0.000 | 0.0000 | 0 | 0.0521 | 0.7908 | 0.714 | 1.386 | 1.699 | 0.00159 | 0.7388 | 0.0023 |
| 8.75 | 57 | 3 249 | 3 163 | 0.907 | 0.000 | 0.0000 | 0 | 0.0461 | 0.7908 | 0.646 | 1.264 | 1.542 | 0.00141 | 0.7448 | 0.0020 |
| 9.00 | 64 | 4 096 | 3 982 | 0.825 | 0.000 | 0.0000 | 0 | 0.0411 | 0.7908 | 0.584 | 1.149 | 1.397 | 0.00126 | 0.7497 | 0.0018 |
| 9.10 | 67 | 4 489 | 4 366 | 0.795 | 0.340 | 0.0017 | 0 | 0.0408 | 0.7908 | 0.561 | 1.106 | 1.343 | 0.00238 | 0.7500 | 0.0017 |
| 9.20 | 70 | 4 900 | 4 787 | 0.766 | 1.000 | 0.0258 | 0 | 0.0620 | 0.7908 | 0.539 | 1.066 | 1.292 | 0.01087 | 0.7289 | 0.0016 |
| 9.30 | 73 | 5 329 | 5 249 | 0.740 | 1.000 | 0.0524 | 0 | 0.0855 | 0.7908 | 0.519 | 1.028 | 1.244 | 0.00681 | 0.7053 | 0.0015 |
| 9.50 | 80 | 6 400 | 6 310 | 0.686 | 1.000 | 0.1060 | 0 | 0.1341 | 0.7908 | 0.479 | 0.953 | 1.150 | 0.00612 | 0.6567 | 0.0014 |
| 9.80 | 92 | 8 464 | 8 318 | 0.611 | 1.000 | 0.1804 | 0 | 0.2025 | 0.7908 | 0.424 | 0.848 | 1.020 | 0.00514 | 0.5884 | 0.0012 |
| 10.00 | 101 | 10 201 | 10 001 | 0.566 | 1.000 | 0.2258 | 0 | 0.2446 | 0.7908 | 0.391 | 0.785 | 0.941 | 0.00457 | 0.5462 | 0.0011 |
| 10.25 | 113 | 12 769 | 12 590 | 0.515 | 1.000 | 0.2766 | 0 | 0.2919 | 0.7908 | 0.354 | 0.714 | 0.853 | 0.00392 | 0.4990 | 0.0010 |
| 10.50 | 126 | 15 876 | 15 849 | 0.469 | 1.000 | 0.3221 | 0 | 0.3344 | 0.7908 | 0.322 | 0.649 | 0.775 | 0.00335 | 0.4564 | 0.0009 |

### d = 2, instance F (K = 3)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 7.00 | 26 | 676 | 631 | 1.698 | 0.000 | 0.0000 | 0 | 0.7729 | 0.7100 | 1.322 | 2.391 | 3.050 | 0.00352 | -0.0629 | 0.0618 |
| 7.50 | 32 | 1 024 | 1 001 | 1.437 | 0.000 | 0.0000 | 0 | 0.7734 | 0.7100 | 1.082 | 2.013 | 2.524 | 0.00267 | -0.0634 | 0.0469 |
| 8.00 | 40 | 1 600 | 1 585 | 1.203 | 0.000 | 0.0000 | 0 | 0.7737 | 0.7100 | 0.883 | 1.680 | 2.080 | 0.00209 | -0.0637 | 0.0368 |
| 8.25 | 45 | 2 025 | 1 996 | 1.096 | 0.000 | 0.0000 | 0 | 0.7739 | 0.7100 | 0.796 | 1.529 | 1.883 | 0.00188 | -0.0639 | 0.0330 |
| 8.50 | 51 | 2 601 | 2 512 | 0.993 | 0.000 | 0.0000 | 0 | 0.7740 | 0.7100 | 0.714 | 1.386 | 1.699 | 0.00170 | -0.0640 | 0.0300 |
| 8.75 | 57 | 3 249 | 3 163 | 0.907 | 0.000 | 0.0000 | 0 | 0.7741 | 0.7100 | 0.646 | 1.264 | 1.542 | 0.00151 | -0.0641 | 0.0265 |
| 9.00 | 64 | 4 096 | 3 982 | 0.825 | 0.000 | 0.0000 | 0 | 0.7742 | 0.7100 | 0.584 | 1.149 | 1.397 | 0.00135 | -0.0642 | 0.0237 |
| 9.10 | 67 | 4 489 | 4 366 | 0.795 | 0.000 | 0.0000 | 0 | 0.7742 | 0.7100 | 0.561 | 1.106 | 1.343 | 0.00128 | -0.0642 | 0.0226 |
| 9.20 | 70 | 4 900 | 4 787 | 0.766 | 0.000 | 0.0000 | 0 | 0.7743 | 0.7100 | 0.539 | 1.066 | 1.292 | 0.00122 | -0.0643 | 0.0215 |
| 9.30 | 73 | 5 329 | 5 249 | 0.740 | 0.000 | 0.0000 | 0 | 0.7743 | 0.7100 | 0.519 | 1.028 | 1.244 | 0.00116 | -0.0643 | 0.0203 |
| 9.50 | 80 | 6 400 | 6 310 | 0.686 | 1.000 | 0.0242 | 0 | 0.7744 | 0.7100 | 0.479 | 0.953 | 1.150 | 0.00105 | -0.0644 | 0.0185 |
| 9.80 | 92 | 8 464 | 8 318 | 0.611 | 1.000 | 0.0988 | 0 | 0.7744 | 0.7100 | 0.424 | 0.848 | 1.020 | 0.00092 | -0.0644 | 0.0162 |
| 10.00 | 101 | 10 201 | 10 001 | 0.566 | 1.000 | 0.1443 | 0 | 0.7745 | 0.7100 | 0.391 | 0.785 | 0.941 | 0.00084 | -0.0645 | 0.0148 |
| 10.25 | 113 | 12 769 | 12 590 | 0.515 | 1.000 | 0.1953 | 0 | 0.7745 | 0.7100 | 0.354 | 0.714 | 0.853 | 0.00075 | -0.0645 | 0.0131 |
| 10.50 | 126 | 15 876 | 15 849 | 0.469 | 1.000 | 0.2408 | 0 | 0.7746 | 0.7100 | 0.322 | 0.649 | 0.775 | 0.00066 | -0.0646 | 0.0115 |

### d = 3, instance D (K = 3)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 7.00 | 15 | 3 375 | 216 | 3.287 | 0.000 | 0.0000 | 0 | 0.1837 | 0.7908 | 2.858 | 4.601 | 6.069 | 0.00000 | 0.6072 | 0.0080 |
| 8.00 | 22 | 10 648 | 465 | 2.482 | 0.000 | 0.0000 | 0 | 0.1248 | 0.7908 | 2.031 | 3.458 | 4.420 | 0.00268 | 0.6660 | 0.0055 |
| 9.00 | 32 | 32 768 | 1 000 | 1.865 | 0.000 | 0.0000 | 0 | 0.0826 | 0.7908 | 1.460 | 2.584 | 3.228 | 0.00253 | 0.7083 | 0.0036 |
| 10.00 | 47 | 103 823 | 2 155 | 1.380 | 0.000 | 0.0000 | 0 | 0.0564 | 0.7908 | 1.050 | 1.906 | 2.344 | 0.00172 | 0.7345 | 0.0025 |
| 10.50 | 57 | 185 193 | 3 163 | 1.183 | 0.000 | 0.0000 | 0 | 0.0467 | 0.7908 | 0.891 | 1.633 | 1.995 | 0.00143 | 0.7442 | 0.0020 |
| 11.00 | 69 | 328 509 | 4 642 | 1.014 | 0.000 | 0.0000 | 0 | 0.0384 | 0.7908 | 0.757 | 1.397 | 1.699 | 0.00118 | 0.7524 | 0.0017 |
| 11.50 | 83 | 571 787 | 6 813 | 0.871 | 0.000 | 0.0000 | 0 | 0.0310 | 0.7908 | 0.646 | 1.199 | 1.450 | 0.00095 | 0.7598 | 0.0014 |
| 11.70 | 90 | 729 000 | 7 944 | 0.816 | 0.000 | 0.0000 | 0 | 0.0291 | 0.7908 | 0.604 | 1.122 | 1.356 | 0.00000 | 0.7617 | 0.0013 |
| 11.80 | 93 | 804 357 | 8 577 | 0.793 | 0.378 | 0.0017 | 0 | 0.0292 | 0.7908 | 0.587 | 1.091 | 1.316 | 0.00000 | 0.7617 | 0.0012 |
| 11.90 | 97 | 912 673 | 9 262 | 0.767 | 1.000 | 0.0248 | 0 | 0.0508 | 0.7908 | 0.566 | 1.054 | 1.272 | - | 0.7400 | 0.0012 |
| 12.00 | 100 | 1 000 000 | 10 000 | 0.747 | 1.000 | 0.0447 | 0 | 0.0686 | 0.7908 | 0.551 | 1.026 | 1.236 | - | 0.7223 | 0.0011 |

### d = 3, instance F (K = 3)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 7.00 | 15 | 3 375 | 216 | 3.287 | 0.000 | 0.0000 | 0 | 0.7714 | 0.7100 | 2.858 | 4.601 | 6.069 | 0.00000 | -0.0614 | 0.1057 |
| 8.00 | 22 | 10 648 | 465 | 2.482 | 0.000 | 0.0000 | 0 | 0.7725 | 0.7100 | 2.031 | 3.458 | 4.420 | 0.00176 | -0.0625 | 0.0718 |
| 9.00 | 32 | 32 768 | 1 000 | 1.865 | 0.000 | 0.0000 | 0 | 0.7733 | 0.7100 | 1.460 | 2.584 | 3.228 | 0.00270 | -0.0633 | 0.0475 |
| 10.00 | 47 | 103 823 | 2 155 | 1.380 | 0.000 | 0.0000 | 0 | 0.7739 | 0.7100 | 1.050 | 1.906 | 2.344 | 0.00185 | -0.0639 | 0.0324 |
| 10.50 | 57 | 185 193 | 3 163 | 1.183 | 0.000 | 0.0000 | 0 | 0.7741 | 0.7100 | 0.891 | 1.633 | 1.995 | 0.00153 | -0.0641 | 0.0269 |
| 11.00 | 69 | 328 509 | 4 642 | 1.014 | 0.000 | 0.0000 | 0 | 0.7742 | 0.7100 | 0.757 | 1.397 | 1.699 | 0.00126 | -0.0642 | 0.0221 |
| 11.50 | 83 | 571 787 | 6 813 | 0.871 | 0.000 | 0.0000 | 0 | 0.7744 | 0.7100 | 0.646 | 1.199 | 1.450 | 0.00102 | -0.0644 | 0.0179 |
| 11.70 | 90 | 729 000 | 7 944 | 0.816 | 0.000 | 0.0000 | 0 | 0.7744 | 0.7100 | 0.604 | 1.122 | 1.356 | 0.00000 | -0.0644 | 0.0168 |
| 11.80 | 93 | 804 357 | 8 577 | 0.793 | 0.000 | 0.0000 | 0 | 0.7745 | 0.7100 | 0.587 | 1.091 | 1.316 | 0.00000 | -0.0645 | 0.0159 |
| 11.90 | 97 | 912 673 | 9 262 | 0.767 | 0.000 | 0.0000 | 0 | 0.7745 | 0.7100 | 0.566 | 1.054 | 1.272 | - | -0.0645 | 0.0154 |
| 12.00 | 100 | 1 000 000 | 10 000 | 0.747 | 0.000 | 0.0000 | 0 | 0.7745 | 0.7100 | 0.551 | 1.026 | 1.236 | - | -0.0645 | 0.0145 |

### d = 4, instance G (K = 4)

| log10 n | g | J | L_n | sigma_n | share of regions with tau > 0 | mean tau | monitor firings (proposed) | revenue/n | M_(2)/n | (A)/n | (B)/n | (C)/n | best gain/n | (B) deficit/n | (C) deficit/n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 9.00 | 20 | 160 000 | 373 | 3.302 | 0.000 | 0.0000 | 0 | 0.1955 | 0.7908 | 2.934 | 4.641 | 6.067 | 0.00000 | 0.5954 | 0.0245 |
| 10.00 | 27 | 531 441 | 720 | 2.636 | 0.000 | 0.0000 | 0 | 0.1253 | 0.7908 | 2.217 | 3.667 | 4.659 | 0.00000 | 0.6655 | 0.0157 |
| 11.00 | 38 | 2 085 136 | 1 390 | 2.031 | 0.000 | 0.0000 | 0 | 0.0949 | 0.7908 | 1.664 | 2.824 | 3.535 | 0.00000 | 0.6959 | 0.0119 |
| 12.00 | 52 | 7 311 616 | 2 683 | 1.586 | 0.000 | 0.0000 | 0 | 0.0642 | 0.7908 | 1.268 | 2.193 | 2.708 | 0.00000 | 0.7266 | 0.0080 |

### Realised gain of each deviation, per round (paired with the proposed profile, same seed)

| d | instance | log10 n | underbid | rider25 | rider50 | rider100 | both | crash | part (A) budget / n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | C | 5.00 | 0.00442 | 0.00000 | 0.00000 | 0.00000 | 0.00442 | 0.00000 | 1.153 |
| 1 | C | 5.25 | 0.00386 | 0.00000 | 0.00000 | 0.00000 | 0.00386 | 0.00000 | 0.999 |
| 1 | C | 5.50 | 0.00331 | 0.00000 | 0.00000 | 0.00000 | 0.00331 | 0.00000 | 0.875 |
| 1 | C | 5.75 | 0.00289 | 0.00000 | 0.00000 | 0.00000 | 0.00289 | 0.00000 | 0.760 |
| 1 | C | 6.00 | 0.00248 | 0.00000 | 0.00000 | 0.00000 | 0.00248 | 0.00000 | 0.668 |
| 1 | C | 6.10 | 0.00235 | 0.00000 | 0.00000 | 0.00000 | 0.00235 | 0.00000 | 0.632 |
| 1 | C | 6.20 | 0.00222 | 0.00000 | 0.00000 | 0.00000 | 0.00222 | 0.00000 | 0.599 |
| 1 | C | 6.30 | 0.00209 | 0.00000 | 0.00000 | 0.00000 | 0.00209 | 0.00000 | 0.569 |
| 1 | C | 6.40 | 0.00196 | 0.00000 | 0.00000 | 0.00000 | 0.00196 | 0.00000 | 0.542 |
| 1 | C | 6.50 | 0.00187 | 0.00009 | 0.00011 | 0.00011 | 0.00198 | 0.00011 | 0.509 |
| 1 | C | 6.60 | 0.00175 | 0.00373 | 0.00637 | 0.00953 | 0.00812 | -0.05041 | 0.487 |
| 1 | C | 6.70 | 0.00166 | 0.00462 | 0.00900 | 0.01669 | 0.01066 | -0.70561 | 0.460 |
| 1 | C | 6.80 | 0.00157 | 0.00433 | 0.00855 | -0.03263 | 0.01012 | -0.79019 | 0.435 |
| 1 | C | 6.90 | 0.00149 | 0.00403 | 0.00798 | -0.17692 | 0.00946 | -0.78691 | 0.413 |
| 1 | C | 7.00 | 0.00140 | 0.00373 | 0.00740 | -0.30404 | 0.00880 | -0.76731 | 0.393 |
| 1 | C | 7.14 | 0.00127 | 0.00333 | 0.00662 | -0.41772 | 0.00789 | -0.73623 | 0.368 |
| 1 | C | 7.25 | 0.00119 | 0.00305 | 0.00609 | -0.47846 | 0.00728 | -0.70907 | 0.348 |
| 1 | C | 7.50 | 0.00103 | 0.00251 | 0.00501 | -0.50611 | 0.00604 | -0.65010 | 0.306 |
| 1 | C | 7.75 | 0.00090 | 0.00207 | 0.00412 | -0.50077 | 0.00502 | -0.59541 | 0.268 |
| 1 | C | 8.00 | 0.00077 | 0.00169 | 0.00338 | -0.49112 | 0.00415 | -0.54615 | 0.236 |
| 1 | C | 8.50 | 0.00058 | 0.00114 | 0.00227 | -0.43572 | 0.00286 | -0.46271 | 0.182 |
| 1 | C | 9.00 | 0.00044 | 0.00076 | 0.00152 | -0.38515 | 0.00196 | -0.39631 | 0.142 |
| 1 | D | 5.00 | 0.00437 | 0.00000 | 0.00000 | 0.00000 | 0.00437 | 0.00000 | 1.298 |
| 1 | D | 5.25 | 0.00382 | 0.00000 | 0.00000 | 0.00000 | 0.00382 | 0.00000 | 1.116 |
| 1 | D | 5.50 | 0.00328 | 0.00000 | 0.00000 | 0.00000 | 0.00328 | 0.00000 | 0.967 |
| 1 | D | 5.75 | 0.00286 | 0.00000 | 0.00000 | 0.00000 | 0.00286 | 0.00000 | 0.834 |
| 1 | D | 6.00 | 0.00245 | 0.00000 | 0.00000 | 0.00000 | 0.00245 | 0.00000 | 0.727 |
| 1 | D | 6.10 | 0.00233 | 0.00000 | 0.00000 | 0.00000 | 0.00233 | 0.00000 | 0.686 |
| 1 | D | 6.20 | 0.00219 | 0.00000 | 0.00000 | 0.00000 | 0.00219 | 0.00000 | 0.648 |
| 1 | D | 6.30 | 0.00206 | 0.00000 | 0.00000 | 0.00000 | 0.00206 | 0.00000 | 0.614 |
| 1 | D | 6.40 | 0.00194 | 0.00000 | 0.00000 | 0.00000 | 0.00194 | 0.00000 | 0.583 |
| 1 | D | 6.50 | 0.00185 | 0.00007 | 0.00008 | 0.00008 | 0.00193 | 0.00008 | 0.547 |
| 1 | D | 6.60 | 0.00173 | 0.00432 | 0.00754 | 0.01158 | 0.00927 | -0.04338 | 0.521 |
| 1 | D | 6.70 | 0.00164 | 0.00459 | 0.00895 | 0.01550 | 0.01059 | -0.71634 | 0.491 |
| 1 | D | 6.80 | 0.00156 | 0.00430 | 0.00849 | -0.04103 | 0.01004 | -0.77892 | 0.464 |
| 1 | D | 6.90 | 0.00147 | 0.00400 | 0.00792 | -0.17777 | 0.00939 | -0.77405 | 0.440 |
| 1 | D | 7.00 | 0.00138 | 0.00370 | 0.00735 | -0.31348 | 0.00874 | -0.75574 | 0.417 |
| 1 | D | 7.14 | 0.00126 | 0.00331 | 0.00658 | -0.40806 | 0.00784 | -0.72581 | 0.390 |
| 1 | D | 7.25 | 0.00118 | 0.00304 | 0.00605 | -0.46648 | 0.00723 | -0.69886 | 0.367 |
| 1 | D | 7.50 | 0.00102 | 0.00250 | 0.00499 | -0.49796 | 0.00601 | -0.64253 | 0.321 |
| 1 | D | 7.75 | 0.00089 | 0.00206 | 0.00411 | -0.50018 | 0.00500 | -0.58918 | 0.280 |
| 1 | D | 8.00 | 0.00077 | 0.00169 | 0.00337 | -0.48762 | 0.00413 | -0.54077 | 0.246 |
| 1 | D | 8.50 | 0.00058 | 0.00113 | 0.00227 | -0.43393 | 0.00285 | -0.45903 | 0.189 |
| 1 | D | 9.00 | 0.00043 | 0.00076 | 0.00152 | -0.37991 | 0.00195 | -0.39330 | 0.146 |
| 1 | E | 5.00 | -0.04581 | 0.00000 | 0.00000 | 0.00000 | -0.04581 | 0.00000 | 1.153 |
| 1 | E | 5.25 | -0.01639 | 0.00000 | 0.00000 | 0.00000 | -0.01639 | 0.00000 | 0.999 |
| 1 | E | 5.50 | -0.01471 | 0.00000 | 0.00000 | 0.00000 | -0.01471 | 0.00000 | 0.875 |
| 1 | E | 5.75 | -0.01732 | 0.00000 | 0.00000 | 0.00000 | -0.01732 | 0.00000 | 0.760 |
| 1 | E | 6.00 | -0.01536 | 0.00000 | 0.00000 | 0.00000 | -0.01536 | 0.00000 | 0.668 |
| 1 | E | 6.10 | -0.01443 | 0.00000 | 0.00000 | 0.00000 | -0.01443 | 0.00000 | 0.632 |
| 1 | E | 6.20 | -0.01722 | 0.00000 | 0.00000 | 0.00000 | -0.01722 | 0.00000 | 0.599 |
| 1 | E | 6.30 | -0.01992 | 0.00000 | 0.00000 | 0.00000 | -0.01992 | 0.00000 | 0.569 |
| 1 | E | 6.40 | -0.01570 | 0.00000 | 0.00000 | 0.00000 | -0.01570 | 0.00000 | 0.542 |
| 1 | E | 6.50 | -0.02372 | 0.00000 | 0.00000 | 0.00000 | -0.02372 | 0.00000 | 0.509 |
| 1 | E | 6.60 | -0.00516 | 0.00047 | 0.00080 | 0.00115 | -0.00441 | -0.00545 | 0.487 |
| 1 | E | 6.70 | -0.00985 | 0.00124 | 0.00227 | 0.00395 | -0.00767 | -0.09781 | 0.460 |
| 1 | E | 6.80 | -0.01137 | 0.00194 | 0.00370 | 0.00121 | -0.00777 | -0.23863 | 0.435 |
| 1 | E | 6.90 | -0.00605 | 0.00197 | 0.00387 | -0.02320 | -0.00223 | -0.34456 | 0.413 |
| 1 | E | 7.00 | -0.00753 | 0.00186 | 0.00368 | -0.06379 | -0.00392 | -0.36410 | 0.393 |
| 1 | E | 7.14 | -0.00679 | 0.00169 | 0.00337 | -0.15444 | -0.00348 | -0.35947 | 0.368 |
| 1 | E | 7.25 | -0.00777 | 0.00155 | 0.00308 | -0.19490 | -0.00474 | -0.34385 | 0.348 |
| 1 | E | 7.50 | -0.00229 | 0.00126 | 0.00251 | -0.23159 | 0.00021 | -0.30948 | 0.306 |
| 1 | E | 7.75 | -0.00602 | 0.00104 | 0.00208 | -0.23679 | -0.00398 | -0.28269 | 0.268 |
| 1 | E | 8.00 | -0.00146 | 0.00084 | 0.00168 | -0.21941 | 0.00020 | -0.25118 | 0.236 |
| 1 | E | 8.50 | -0.00319 | 0.00057 | 0.00114 | -0.20001 | -0.00206 | -0.21206 | 0.182 |
| 1 | E | 9.00 | -0.00137 | 0.00038 | 0.00076 | -0.16872 | -0.00062 | -0.17524 | 0.142 |
| 1 | F | 5.00 | 0.00471 | 0.00000 | 0.00000 | 0.00000 | 0.00471 | 0.00000 | 1.298 |
| 1 | F | 5.25 | 0.00411 | 0.00000 | 0.00000 | 0.00000 | 0.00411 | 0.00000 | 1.116 |
| 1 | F | 5.50 | 0.00353 | 0.00000 | 0.00000 | 0.00000 | 0.00353 | 0.00000 | 0.967 |
| 1 | F | 5.75 | 0.00308 | 0.00000 | 0.00000 | 0.00000 | 0.00308 | 0.00000 | 0.834 |
| 1 | F | 6.00 | 0.00264 | 0.00000 | 0.00000 | 0.00000 | 0.00264 | 0.00000 | 0.727 |
| 1 | F | 6.10 | 0.00250 | 0.00000 | 0.00000 | 0.00000 | 0.00250 | 0.00000 | 0.686 |
| 1 | F | 6.20 | 0.00236 | 0.00000 | 0.00000 | 0.00000 | 0.00236 | 0.00000 | 0.648 |
| 1 | F | 6.30 | 0.00222 | 0.00000 | 0.00000 | 0.00000 | 0.00222 | 0.00000 | 0.614 |
| 1 | F | 6.40 | 0.00208 | 0.00000 | 0.00000 | 0.00000 | 0.00208 | 0.00000 | 0.583 |
| 1 | F | 6.50 | 0.00200 | 0.00000 | 0.00000 | 0.00000 | 0.00200 | 0.00000 | 0.547 |
| 1 | F | 6.60 | 0.00186 | 0.00000 | 0.00000 | 0.00000 | 0.00186 | 0.00000 | 0.521 |
| 1 | F | 6.70 | 0.00177 | 0.00000 | 0.00000 | 0.00000 | 0.00177 | 0.00000 | 0.491 |
| 1 | F | 6.80 | 0.00168 | 0.00000 | 0.00000 | 0.00000 | 0.00168 | 0.00000 | 0.464 |
| 1 | F | 6.90 | 0.00158 | 0.00000 | 0.00000 | 0.00000 | 0.00158 | 0.00000 | 0.440 |
| 1 | F | 7.00 | 0.00149 | 0.00000 | 0.00000 | 0.00000 | 0.00149 | 0.00000 | 0.417 |
| 1 | F | 7.14 | 0.00135 | 0.00000 | 0.00000 | 0.00000 | 0.00135 | 0.00000 | 0.390 |
| 1 | F | 7.25 | 0.00127 | 0.00000 | 0.00000 | 0.00000 | 0.00127 | 0.00000 | 0.367 |
| 1 | F | 7.50 | 0.00110 | 0.00000 | 0.00000 | 0.00000 | 0.00110 | 0.00000 | 0.321 |
| 1 | F | 7.75 | 0.00096 | 0.00000 | 0.00000 | 0.00000 | 0.00096 | 0.00000 | 0.280 |
| 1 | F | 8.00 | 0.00083 | 0.00000 | 0.00000 | 0.00000 | 0.00083 | 0.00000 | 0.246 |
| 1 | F | 8.50 | 0.00062 | 0.00000 | 0.00000 | 0.00000 | 0.00062 | 0.00000 | 0.189 |
| 1 | F | 9.00 | 0.00046 | 0.00000 | 0.00000 | 0.00000 | 0.00046 | 0.00000 | 0.146 |
| 2 | C | 6.00 | -0.00908 | 0.00000 | 0.00000 | 0.00000 | -0.00908 | 0.00000 | 1.872 |
| 2 | C | 7.00 | 0.00294 | 0.00000 | 0.00000 | 0.00000 | 0.00294 | 0.00000 | 1.234 |
| 2 | C | 7.50 | 0.00251 | 0.00000 | 0.00000 | 0.00000 | 0.00251 | 0.00000 | 1.022 |
| 2 | C | 8.00 | 0.00197 | 0.00000 | 0.00000 | 0.00000 | 0.00197 | 0.00000 | 0.841 |
| 2 | C | 8.25 | 0.00176 | 0.00000 | 0.00000 | 0.00000 | 0.00176 | 0.00000 | 0.761 |
| 2 | C | 8.50 | 0.00160 | 0.00000 | 0.00000 | 0.00000 | 0.00160 | 0.00000 | 0.685 |
| 2 | C | 8.75 | 0.00142 | 0.00000 | 0.00000 | 0.00000 | 0.00142 | 0.00000 | 0.622 |
| 2 | C | 9.00 | 0.00126 | 0.00000 | 0.00000 | 0.00000 | 0.00126 | 0.00000 | 0.563 |
| 2 | C | 9.10 | 0.00121 | 0.00076 | 0.00117 | 0.00153 | 0.00237 | -0.00106 | 0.541 |
| 2 | C | 9.20 | 0.00115 | 0.00304 | 0.00583 | 0.01065 | 0.00697 | -0.53987 | 0.521 |
| 2 | C | 9.30 | 0.00109 | 0.00292 | 0.00575 | 0.00308 | 0.00684 | -0.81760 | 0.502 |
| 2 | C | 9.50 | 0.00099 | 0.00260 | 0.00516 | -0.23918 | 0.00615 | -0.81374 | 0.465 |
| 2 | C | 9.80 | 0.00086 | 0.00216 | 0.00430 | -0.48828 | 0.00517 | -0.75075 | 0.412 |
| 2 | C | 10.00 | 0.00079 | 0.00190 | 0.00380 | -0.54070 | 0.00459 | -0.70786 | 0.381 |
| 2 | C | 10.25 | 0.00070 | 0.00162 | 0.00323 | -0.55442 | 0.00393 | -0.66007 | 0.346 |
| 2 | C | 10.50 | 0.00062 | 0.00137 | 0.00274 | -0.54512 | 0.00336 | -0.61601 | 0.315 |
| 2 | D | 7.00 | 0.00329 | 0.00000 | 0.00000 | 0.00000 | 0.00329 | 0.00000 | 1.322 |
| 2 | D | 7.50 | 0.00250 | 0.00000 | 0.00000 | 0.00000 | 0.00250 | 0.00000 | 1.082 |
| 2 | D | 8.00 | 0.00195 | 0.00000 | 0.00000 | 0.00000 | 0.00195 | 0.00000 | 0.883 |
| 2 | D | 8.25 | 0.00175 | 0.00000 | 0.00000 | 0.00000 | 0.00175 | 0.00000 | 0.796 |
| 2 | D | 8.50 | 0.00159 | 0.00000 | 0.00000 | 0.00000 | 0.00159 | 0.00000 | 0.714 |
| 2 | D | 8.75 | 0.00141 | 0.00000 | 0.00000 | 0.00000 | 0.00141 | 0.00000 | 0.646 |
| 2 | D | 9.00 | 0.00126 | 0.00000 | 0.00000 | 0.00000 | 0.00126 | 0.00000 | 0.584 |
| 2 | D | 9.10 | 0.00120 | 0.00077 | 0.00116 | 0.00148 | 0.00236 | -0.00059 | 0.561 |
| 2 | D | 9.20 | 0.00114 | 0.00304 | 0.00587 | 0.01086 | 0.00701 | -0.59348 | 0.539 |
| 2 | D | 9.30 | 0.00108 | 0.00291 | 0.00572 | 0.00304 | 0.00680 | -0.81203 | 0.519 |
| 2 | D | 9.50 | 0.00098 | 0.00258 | 0.00513 | -0.24013 | 0.00612 | -0.80458 | 0.479 |
| 2 | D | 9.80 | 0.00086 | 0.00215 | 0.00428 | -0.48559 | 0.00514 | -0.74348 | 0.424 |
| 2 | D | 10.00 | 0.00079 | 0.00190 | 0.00379 | -0.53544 | 0.00457 | -0.70126 | 0.391 |
| 2 | D | 10.25 | 0.00070 | 0.00161 | 0.00322 | -0.54888 | 0.00392 | -0.65479 | 0.354 |
| 2 | D | 10.50 | 0.00061 | 0.00137 | 0.00274 | -0.54200 | 0.00335 | -0.61137 | 0.322 |
| 2 | E | 6.00 | -0.04678 | 0.00000 | 0.00000 | 0.00000 | -0.04678 | 0.00000 | 1.872 |
| 2 | E | 7.00 | -0.03236 | 0.00000 | 0.00000 | 0.00000 | -0.03236 | 0.00000 | 1.234 |
| 2 | E | 7.50 | -0.03489 | 0.00000 | 0.00000 | 0.00000 | -0.03489 | 0.00000 | 1.022 |
| 2 | E | 8.00 | -0.02456 | 0.00000 | 0.00000 | 0.00000 | -0.02456 | 0.00000 | 0.841 |
| 2 | E | 8.25 | -0.02374 | 0.00000 | 0.00000 | 0.00000 | -0.02374 | 0.00000 | 0.761 |
| 2 | E | 8.50 | -0.02247 | 0.00000 | 0.00000 | 0.00000 | -0.02247 | 0.00000 | 0.685 |
| 2 | E | 8.75 | -0.02001 | 0.00000 | 0.00000 | 0.00000 | -0.02001 | 0.00000 | 0.622 |
| 2 | E | 9.00 | -0.01769 | 0.00023 | 0.00042 | 0.00072 | -0.01730 | -0.02842 | 0.563 |
| 2 | E | 9.10 | -0.01543 | 0.00044 | 0.00082 | 0.00011 | -0.01465 | -0.06988 | 0.541 |
| 2 | E | 9.20 | -0.01515 | 0.00067 | 0.00129 | -0.00511 | -0.01392 | -0.12868 | 0.521 |
| 2 | E | 9.30 | -0.01565 | 0.00091 | 0.00175 | -0.01589 | -0.01397 | -0.19369 | 0.502 |
| 2 | E | 9.50 | -0.01224 | 0.00129 | 0.00254 | -0.06738 | -0.00977 | -0.35445 | 0.465 |
| 2 | E | 9.80 | -0.01035 | 0.00108 | 0.00215 | -0.19095 | -0.00826 | -0.34660 | 0.412 |
| 2 | E | 10.00 | -0.00834 | 0.00095 | 0.00190 | -0.23026 | -0.00648 | -0.32344 | 0.381 |
| 2 | E | 10.25 | -0.00733 | 0.00081 | 0.00162 | -0.24303 | -0.00575 | -0.29934 | 0.346 |
| 2 | E | 10.50 | -0.00616 | 0.00069 | 0.00137 | -0.23896 | -0.00481 | -0.27428 | 0.315 |
| 2 | F | 7.00 | 0.00254 | 0.00000 | 0.00000 | 0.00000 | 0.00254 | 0.00000 | 1.322 |
| 2 | F | 7.50 | 0.00267 | 0.00000 | 0.00000 | 0.00000 | 0.00267 | 0.00000 | 1.082 |
| 2 | F | 8.00 | 0.00209 | 0.00000 | 0.00000 | 0.00000 | 0.00209 | 0.00000 | 0.883 |
| 2 | F | 8.25 | 0.00188 | 0.00000 | 0.00000 | 0.00000 | 0.00188 | 0.00000 | 0.796 |
| 2 | F | 8.50 | 0.00170 | 0.00000 | 0.00000 | 0.00000 | 0.00170 | 0.00000 | 0.714 |
| 2 | F | 8.75 | 0.00151 | 0.00000 | 0.00000 | 0.00000 | 0.00151 | 0.00000 | 0.646 |
| 2 | F | 9.00 | 0.00135 | 0.00000 | 0.00000 | 0.00000 | 0.00135 | 0.00000 | 0.584 |
| 2 | F | 9.10 | 0.00128 | 0.00000 | 0.00000 | 0.00000 | 0.00128 | 0.00000 | 0.561 |
| 2 | F | 9.20 | 0.00122 | 0.00000 | 0.00000 | 0.00000 | 0.00122 | 0.00000 | 0.539 |
| 2 | F | 9.30 | 0.00116 | 0.00000 | 0.00000 | 0.00000 | 0.00116 | 0.00000 | 0.519 |
| 2 | F | 9.50 | 0.00105 | 0.00000 | 0.00000 | 0.00000 | 0.00105 | 0.00000 | 0.479 |
| 2 | F | 9.80 | 0.00092 | 0.00000 | 0.00000 | 0.00000 | 0.00092 | 0.00000 | 0.424 |
| 2 | F | 10.00 | 0.00084 | 0.00000 | 0.00000 | 0.00000 | 0.00084 | 0.00000 | 0.391 |
| 2 | F | 10.25 | 0.00075 | 0.00000 | 0.00000 | 0.00000 | 0.00075 | 0.00000 | 0.354 |
| 2 | F | 10.50 | 0.00066 | 0.00000 | 0.00000 | 0.00000 | 0.00066 | 0.00000 | 0.322 |
| 3 | D | 7.00 | -0.01615 | 0.00000 | 0.00000 | 0.00000 | -0.01615 | 0.00000 | 2.858 |
| 3 | D | 8.00 | 0.00209 | 0.00000 | 0.00000 | 0.00000 | 0.00209 | 0.00000 | 2.031 |
| 3 | D | 9.00 | 0.00253 | 0.00000 | 0.00000 | 0.00000 | 0.00253 | 0.00000 | 1.460 |
| 3 | D | 10.00 | 0.00172 | 0.00000 | 0.00000 | 0.00000 | 0.00172 | 0.00000 | 1.050 |
| 3 | D | 10.50 | 0.00143 | 0.00000 | 0.00000 | 0.00000 | 0.00143 | 0.00000 | 0.891 |
| 3 | D | 11.00 | 0.00118 | 0.00000 | 0.00000 | 0.00000 | 0.00118 | 0.00000 | 0.757 |
| 3 | D | 11.50 | 0.00095 | 0.00000 | 0.00000 | 0.00000 | 0.00095 | 0.00000 | 0.646 |
| 3 | D | 11.70 | - | - | - | - | - | 0.00000 | 0.604 |
| 3 | D | 11.80 | - | - | - | - | - | -0.00733 | 0.587 |
| 3 | F | 7.00 | -0.01981 | 0.00000 | 0.00000 | 0.00000 | -0.01981 | 0.00000 | 2.858 |
| 3 | F | 8.00 | 0.00155 | 0.00000 | 0.00000 | 0.00000 | 0.00155 | 0.00000 | 2.031 |
| 3 | F | 9.00 | 0.00268 | 0.00000 | 0.00000 | 0.00000 | 0.00268 | 0.00000 | 1.460 |
| 3 | F | 10.00 | 0.00185 | 0.00000 | 0.00000 | 0.00000 | 0.00185 | 0.00000 | 1.050 |
| 3 | F | 10.50 | 0.00153 | 0.00000 | 0.00000 | 0.00000 | 0.00153 | 0.00000 | 0.891 |
| 3 | F | 11.00 | 0.00126 | 0.00000 | 0.00000 | 0.00000 | 0.00126 | 0.00000 | 0.757 |
| 3 | F | 11.50 | 0.00102 | 0.00000 | 0.00000 | 0.00000 | 0.00102 | 0.00000 | 0.646 |
| 3 | F | 11.70 | - | - | - | - | - | 0.00000 | 0.604 |
| 3 | F | 11.80 | - | - | - | - | - | 0.00000 | 0.587 |
| 4 | G | 9.00 | - | - | - | - | - | 0.00000 | 2.934 |
| 4 | G | 10.00 | - | - | - | - | - | 0.00000 | 2.217 |
| 4 | G | 11.00 | - | - | - | - | - | 0.00000 | 1.664 |
| 4 | G | 12.00 | - | - | - | - | - | 0.00000 | 1.268 |

### The monitor: conviction of a crashing winner, and false alarms

| d | instance | log10 n | share of regions with tau > 0 | firings under the proposed profile | regions convicted, crash deviation | regions convicted, ride the boundary at scale 1 | false alarms, all profiles |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | C | 5.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 5.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 5.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 5.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 6.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 6.10 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 6.20 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 6.30 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 6.40 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 6.50 | 0.029 | 0 | 0.000 | 0.000 | 0 |
| 1 | C | 6.60 | 0.872 | 0 | 0.194 | 0.000 | 0 |
| 1 | C | 6.70 | 1.000 | 0 | 1.000 | 0.003 | 0 |
| 1 | C | 6.80 | 1.000 | 0 | 1.000 | 0.162 | 0 |
| 1 | C | 6.90 | 1.000 | 0 | 1.000 | 0.419 | 0 |
| 1 | C | 7.00 | 1.000 | 0 | 1.000 | 0.623 | 0 |
| 1 | C | 7.14 | 1.000 | 0 | 1.000 | 0.758 | 0 |
| 1 | C | 7.25 | 1.000 | 0 | 1.000 | 0.817 | 0 |
| 1 | C | 7.50 | 1.000 | 0 | 1.000 | 0.883 | 0 |
| 1 | C | 7.75 | 1.000 | 0 | 1.000 | 0.905 | 0 |
| 1 | C | 8.00 | 1.000 | 0 | 1.000 | 0.961 | 0 |
| 1 | C | 8.50 | 1.000 | 0 | 1.000 | 0.968 | 0 |
| 1 | C | 9.00 | 1.000 | 0 | 1.000 | 0.989 | 0 |
| 1 | D | 5.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 5.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 5.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 5.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 6.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 6.10 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 6.20 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 6.30 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 6.40 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 6.50 | 0.026 | 0 | 0.000 | 0.000 | 0 |
| 1 | D | 6.60 | 0.981 | 0 | 0.233 | 0.000 | 0 |
| 1 | D | 6.70 | 1.000 | 0 | 1.000 | 0.010 | 0 |
| 1 | D | 6.80 | 1.000 | 0 | 1.000 | 0.184 | 0 |
| 1 | D | 6.90 | 1.000 | 0 | 1.000 | 0.426 | 0 |
| 1 | D | 7.00 | 1.000 | 0 | 1.000 | 0.640 | 0 |
| 1 | D | 7.14 | 1.000 | 0 | 1.000 | 0.742 | 0 |
| 1 | D | 7.25 | 1.000 | 0 | 1.000 | 0.813 | 0 |
| 1 | D | 7.50 | 1.000 | 0 | 1.000 | 0.872 | 0 |
| 1 | D | 7.75 | 1.000 | 0 | 1.000 | 0.915 | 0 |
| 1 | D | 8.00 | 1.000 | 0 | 1.000 | 0.955 | 0 |
| 1 | D | 8.50 | 1.000 | 0 | 1.000 | 0.974 | 0 |
| 1 | D | 9.00 | 1.000 | 0 | 1.000 | 0.984 | 0 |
| 1 | E | 5.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 5.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 5.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 5.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 6.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 6.10 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 6.20 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 6.30 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 6.40 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 6.50 | 0.003 | 0 | 0.000 | 0.000 | 0 |
| 1 | E | 6.60 | 0.236 | 0 | 0.022 | 0.000 | 0 |
| 1 | E | 6.70 | 0.612 | 0 | 0.193 | 0.000 | 0 |
| 1 | E | 6.80 | 0.939 | 0 | 0.382 | 0.022 | 0 |
| 1 | E | 6.90 | 1.000 | 0 | 0.491 | 0.086 | 0 |
| 1 | E | 7.00 | 1.000 | 0 | 0.500 | 0.169 | 0 |
| 1 | E | 7.14 | 1.000 | 0 | 0.510 | 0.322 | 0 |
| 1 | E | 7.25 | 1.000 | 0 | 0.508 | 0.383 | 0 |
| 1 | E | 7.50 | 1.000 | 0 | 0.502 | 0.428 | 0 |
| 1 | E | 7.75 | 1.000 | 0 | 0.504 | 0.463 | 0 |
| 1 | E | 8.00 | 1.000 | 0 | 0.496 | 0.468 | 0 |
| 1 | E | 8.50 | 1.000 | 0 | 0.503 | 0.492 | 0 |
| 1 | E | 9.00 | 1.000 | 0 | 0.499 | 0.492 | 0 |
| 1 | F | 5.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 5.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 5.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 5.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.10 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.20 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.30 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.40 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.60 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.70 | 0.008 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.80 | 0.689 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 6.90 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 7.00 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 7.14 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 7.25 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 7.50 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 7.75 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 8.00 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 8.50 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 1 | F | 9.00 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 6.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 7.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 7.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 8.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 8.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 8.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 8.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 9.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | C | 9.10 | 0.320 | 0 | 0.013 | 0.000 | 0 |
| 2 | C | 9.20 | 0.999 | 0 | 0.908 | 0.000 | 0 |
| 2 | C | 9.30 | 1.000 | 0 | 1.000 | 0.036 | 0 |
| 2 | C | 9.50 | 1.000 | 0 | 1.000 | 0.510 | 0 |
| 2 | C | 9.80 | 1.000 | 0 | 1.000 | 0.804 | 0 |
| 2 | C | 10.00 | 1.000 | 0 | 1.000 | 0.875 | 0 |
| 2 | C | 10.25 | 1.000 | 0 | 1.000 | 0.917 | 0 |
| 2 | C | 10.50 | 1.000 | 0 | 1.000 | 0.941 | 0 |
| 2 | D | 7.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | D | 7.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | D | 8.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | D | 8.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | D | 8.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | D | 8.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | D | 9.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | D | 9.10 | 0.340 | 0 | 0.010 | 0.000 | 0 |
| 2 | D | 9.20 | 1.000 | 0 | 0.979 | 0.000 | 0 |
| 2 | D | 9.30 | 1.000 | 0 | 1.000 | 0.036 | 0 |
| 2 | D | 9.50 | 1.000 | 0 | 1.000 | 0.515 | 0 |
| 2 | D | 9.80 | 1.000 | 0 | 1.000 | 0.805 | 0 |
| 2 | D | 10.00 | 1.000 | 0 | 1.000 | 0.875 | 0 |
| 2 | D | 10.25 | 1.000 | 0 | 1.000 | 0.916 | 0 |
| 2 | D | 10.50 | 1.000 | 0 | 1.000 | 0.942 | 0 |
| 2 | E | 6.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | E | 7.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | E | 7.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | E | 8.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | E | 8.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | E | 8.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | E | 8.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | E | 9.00 | 0.141 | 0 | 0.047 | 0.000 | 0 |
| 2 | E | 9.10 | 0.280 | 0 | 0.106 | 0.005 | 0 |
| 2 | E | 9.20 | 0.450 | 0 | 0.186 | 0.020 | 0 |
| 2 | E | 9.30 | 0.646 | 0 | 0.276 | 0.045 | 0 |
| 2 | E | 9.50 | 1.000 | 0 | 0.495 | 0.153 | 0 |
| 2 | E | 9.80 | 1.000 | 0 | 0.500 | 0.364 | 0 |
| 2 | E | 10.00 | 1.000 | 0 | 0.500 | 0.421 | 0 |
| 2 | E | 10.25 | 1.000 | 0 | 0.500 | 0.450 | 0 |
| 2 | E | 10.50 | 1.000 | 0 | 0.499 | 0.466 | 0 |
| 2 | F | 7.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 7.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 8.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 8.25 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 8.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 8.75 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 9.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 9.10 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 9.20 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 9.30 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 9.50 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 9.80 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 10.00 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 10.25 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 2 | F | 10.50 | 1.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 7.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 8.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 9.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 10.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 10.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 11.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 11.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | D | 11.70 | 0.000 | 0 | 0.000 | - | 0 |
| 3 | D | 11.80 | 0.378 | 0 | 0.033 | - | 0 |
| 3 | D | 11.90 | 1.000 | 0 | - | - | 0 |
| 3 | D | 12.00 | 1.000 | 0 | - | - | 0 |
| 3 | F | 7.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | F | 8.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | F | 9.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | F | 10.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | F | 10.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | F | 11.00 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | F | 11.50 | 0.000 | 0 | 0.000 | 0.000 | 0 |
| 3 | F | 11.70 | 0.000 | 0 | 0.000 | - | 0 |
| 3 | F | 11.80 | 0.000 | 0 | 0.000 | - | 0 |
| 3 | F | 11.90 | 0.000 | 0 | - | - | 0 |
| 3 | F | 12.00 | 0.000 | 0 | - | - | 0 |
| 4 | G | 9.00 | 0.000 | 0 | 0.000 | - | 0 |
| 4 | G | 10.00 | 0.000 | 0 | 0.000 | - | 0 |
| 4 | G | 11.00 | 0.000 | 0 | 0.000 | - | 0 |
| 4 | G | 12.00 | 0.000 | 0 | 0.000 | - | 0 |

### Numerical hygiene: compensated minus naive floating-point sum of the benchmark

| d | instance | log10 n | n | Neumaier minus naive, benchmark sum | as a share of the sum |
|--:|--:|--:|--:|--:|--:|
| 1 | C | 5.00 | 100 000 | 5.821e-10 | 7.37e-15 |
| 1 | C | 5.25 | 177 828 | -1.746e-10 | 1.24e-15 |
| 1 | C | 5.50 | 316 228 | -7.567e-10 | 3.03e-15 |
| 1 | C | 5.75 | 562 341 | -1.036e-08 | 2.33e-14 |
| 1 | C | 6.00 | 1 000 000 | -3.120e-08 | 3.95e-14 |
| 1 | C | 6.10 | 1 258 925 | -3.038e-08 | 3.06e-14 |
| 1 | C | 6.20 | 1 584 893 | -6.752e-09 | 5.39e-15 |
| 1 | C | 6.30 | 1 995 262 | -1.746e-08 | 1.11e-14 |
| 1 | C | 6.40 | 2 511 886 | -8.312e-08 | 4.19e-14 |
| 1 | C | 6.50 | 3 162 278 | -1.397e-09 | 5.59e-16 |
| 1 | C | 6.60 | 3 981 072 | 3.539e-08 | 1.13e-14 |
| 1 | C | 6.70 | 5 011 872 | 7.637e-08 | 1.93e-14 |
| 1 | C | 6.80 | 6 309 573 | 1.844e-07 | 3.70e-14 |
| 1 | C | 6.90 | 7 943 282 | 1.742e-07 | 2.78e-14 |
| 1 | C | 7.00 | 10 000 000 | -4.657e-09 | 5.89e-16 |
| 1 | C | 7.14 | 13 803 843 | 1.082e-06 | 9.92e-14 |
| 1 | C | 7.25 | 17 782 794 | 1.447e-06 | 1.03e-13 |
| 1 | C | 7.50 | 31 622 777 | -8.047e-07 | 3.22e-14 |
| 1 | C | 7.75 | 56 234 133 | 1.280e-05 | 2.88e-13 |
| 1 | C | 8.00 | 100 000 000 | 1.875e-05 | 2.37e-13 |
| 1 | C | 8.50 | 316 227 766 | -4.193e-05 | 1.68e-13 |
| 1 | C | 9.00 | 1 000 000 000 | 5.788e-04 | 7.33e-13 |
| 1 | D | 5.00 | 100 000 | 9.604e-10 | 1.21e-14 |
| 1 | D | 5.25 | 177 828 | 4.948e-10 | 3.51e-15 |
| 1 | D | 5.50 | 316 228 | -6.316e-09 | 2.52e-14 |
| 1 | D | 5.75 | 562 341 | -1.135e-08 | 2.55e-14 |
| 1 | D | 6.00 | 1 000 000 | -5.658e-08 | 7.15e-14 |
| 1 | D | 6.10 | 1 258 925 | -5.157e-08 | 5.17e-14 |
| 1 | D | 6.20 | 1 584 893 | -2.654e-08 | 2.12e-14 |
| 1 | D | 6.30 | 1 995 262 | -9.779e-09 | 6.19e-15 |
| 1 | D | 6.40 | 2 511 886 | 4.936e-08 | 2.48e-14 |
| 1 | D | 6.50 | 3 162 278 | 1.322e-07 | 5.28e-14 |
| 1 | D | 6.60 | 3 981 072 | 1.779e-07 | 5.64e-14 |
| 1 | D | 6.70 | 5 011 872 | 9.639e-08 | 2.43e-14 |
| 1 | D | 6.80 | 6 309 573 | 7.171e-08 | 1.44e-14 |
| 1 | D | 6.90 | 7 943 282 | -9.313e-10 | 1.48e-16 |
| 1 | D | 7.00 | 10 000 000 | -1.490e-08 | 1.88e-15 |
| 1 | D | 7.14 | 13 803 843 | 1.449e-06 | 1.33e-13 |
| 1 | D | 7.25 | 17 782 794 | 1.844e-06 | 1.31e-13 |
| 1 | D | 7.50 | 31 622 777 | 2.436e-06 | 9.73e-14 |
| 1 | D | 7.75 | 56 234 133 | 1.138e-05 | 2.56e-13 |
| 1 | D | 8.00 | 100 000 000 | 1.428e-05 | 1.80e-13 |
| 1 | D | 8.50 | 316 227 766 | -2.384e-05 | 9.52e-14 |
| 1 | D | 9.00 | 1 000 000 000 | 1.412e-03 | 1.78e-12 |
| 1 | E | 5.00 | 100 000 | -1.106e-09 | 1.47e-14 |
| 1 | E | 5.25 | 177 828 | -1.746e-10 | 1.31e-15 |
| 1 | E | 5.50 | 316 228 | -2.503e-09 | 1.06e-14 |
| 1 | E | 5.75 | 562 341 | 6.170e-09 | 1.46e-14 |
| 1 | E | 6.00 | 1 000 000 | 3.120e-08 | 4.16e-14 |
| 1 | E | 6.10 | 1 258 925 | 3.050e-08 | 3.23e-14 |
| 1 | E | 6.20 | 1 584 893 | 1.304e-08 | 1.10e-14 |
| 1 | E | 6.30 | 1 995 262 | 1.024e-08 | 6.85e-15 |
| 1 | E | 6.40 | 2 511 886 | -1.150e-07 | 6.11e-14 |
| 1 | E | 6.50 | 3 162 278 | 3.912e-08 | 1.65e-14 |
| 1 | E | 6.60 | 3 981 072 | 2.421e-08 | 8.11e-15 |
| 1 | E | 6.70 | 5 011 872 | -1.104e-07 | 2.94e-14 |
| 1 | E | 6.80 | 6 309 573 | -3.735e-07 | 7.89e-14 |
| 1 | E | 6.90 | 7 943 282 | -1.397e-07 | 2.34e-14 |
| 1 | E | 7.00 | 10 000 000 | -4.750e-08 | 6.33e-15 |
| 1 | E | 7.14 | 13 803 843 | 2.794e-07 | 2.70e-14 |
| 1 | E | 7.25 | 17 782 794 | 6.929e-07 | 5.20e-14 |
| 1 | E | 7.50 | 31 622 777 | -3.215e-06 | 1.36e-13 |
| 1 | E | 7.75 | 56 234 133 | -1.089e-05 | 2.58e-13 |
| 1 | E | 8.00 | 100 000 000 | -1.194e-05 | 1.59e-13 |
| 1 | E | 8.50 | 316 227 766 | -6.840e-05 | 2.88e-13 |
| 1 | E | 9.00 | 1 000 000 000 | -4.388e-04 | 5.85e-13 |
| 1 | F | 5.00 | 100 000 | -9.604e-10 | 1.35e-14 |
| 1 | F | 5.25 | 177 828 | -1.281e-09 | 1.01e-14 |
| 1 | F | 5.50 | 316 228 | -4.657e-10 | 2.07e-15 |
| 1 | F | 5.75 | 562 341 | 9.837e-09 | 2.46e-14 |
| 1 | F | 6.00 | 1 000 000 | 1.839e-08 | 2.59e-14 |
| 1 | F | 6.10 | 1 258 925 | 1.758e-08 | 1.97e-14 |
| 1 | F | 6.20 | 1 584 893 | 3.120e-08 | 2.77e-14 |
| 1 | F | 6.30 | 1 995 262 | 4.191e-08 | 2.96e-14 |
| 1 | F | 6.40 | 2 511 886 | 1.076e-07 | 6.03e-14 |
| 1 | F | 6.50 | 3 162 278 | 6.473e-08 | 2.88e-14 |
| 1 | F | 6.60 | 3 981 072 | 2.794e-08 | 9.88e-15 |
| 1 | F | 6.70 | 5 011 872 | -1.304e-08 | 3.66e-15 |
| 1 | F | 6.80 | 6 309 573 | 3.092e-07 | 6.90e-14 |
| 1 | F | 6.90 | 7 943 282 | 3.194e-07 | 5.66e-14 |
| 1 | F | 7.00 | 10 000 000 | 4.983e-07 | 7.02e-14 |
| 1 | F | 7.14 | 13 803 843 | 2.198e-07 | 2.24e-14 |
| 1 | F | 7.25 | 17 782 794 | -1.453e-07 | 1.15e-14 |
| 1 | F | 7.50 | 31 622 777 | 3.688e-06 | 1.64e-13 |
| 1 | F | 7.75 | 56 234 133 | -8.956e-06 | 2.24e-13 |
| 1 | F | 8.00 | 100 000 000 | -3.278e-06 | 4.62e-14 |
| 1 | F | 8.50 | 316 227 766 | 3.853e-05 | 1.72e-13 |
| 1 | F | 9.00 | 1 000 000 000 | -1.372e-04 | 1.93e-13 |
| 2 | C | 6.00 | 1 000 000 | -9.430e-09 | 1.19e-14 |
| 2 | C | 7.00 | 10 000 000 | 3.157e-07 | 4.00e-14 |
| 2 | C | 7.50 | 31 622 777 | -6.124e-06 | 2.45e-13 |
| 2 | C | 8.00 | 100 000 000 | -7.600e-06 | 9.62e-14 |
| 2 | C | 8.25 | 177 827 941 | -1.651e-05 | 1.18e-13 |
| 2 | C | 8.50 | 316 227 766 | -1.581e-04 | 6.33e-13 |
| 2 | C | 8.75 | 562 341 325 | -1.167e-04 | 2.63e-13 |
| 2 | C | 9.00 | 1 000 000 000 | -2.985e-04 | 3.78e-13 |
| 2 | C | 9.10 | 1 258 925 412 | -1.204e-04 | 1.21e-13 |
| 2 | C | 9.20 | 1 584 893 192 | 9.413e-04 | 7.52e-13 |
| 2 | C | 9.30 | 1 995 262 315 | 1.720e-03 | 1.09e-12 |
| 2 | C | 9.50 | 3 162 277 660 | -1.515e-03 | 6.06e-13 |
| 2 | C | 9.80 | 6 309 573 445 | -2.431e-02 | 4.88e-12 |
| 2 | C | 10.00 | 10 000 000 000 | -3.603e-02 | 4.56e-12 |
| 2 | C | 10.25 | 17 782 794 100 | 4.462e-02 | 3.18e-12 |
| 2 | C | 10.50 | 31 622 776 602 | -2.517e-01 | 1.01e-11 |
| 2 | D | 7.00 | 10 000 000 | -9.313e-08 | 1.18e-14 |
| 2 | D | 7.50 | 31 622 777 | -1.029e-05 | 4.12e-13 |
| 2 | D | 8.00 | 100 000 000 | -1.946e-05 | 2.46e-13 |
| 2 | D | 8.25 | 177 827 941 | -4.581e-05 | 3.26e-13 |
| 2 | D | 8.50 | 316 227 766 | -1.326e-04 | 5.30e-13 |
| 2 | D | 8.75 | 562 341 325 | -3.994e-04 | 8.98e-13 |
| 2 | D | 9.00 | 1 000 000 000 | -8.205e-04 | 1.04e-12 |
| 2 | D | 9.10 | 1 258 925 412 | -6.393e-04 | 6.42e-13 |
| 2 | D | 9.20 | 1 584 893 192 | -6.006e-04 | 4.79e-13 |
| 2 | D | 9.30 | 1 995 262 315 | -5.064e-04 | 3.21e-13 |
| 2 | D | 9.50 | 3 162 277 660 | 1.994e-03 | 7.97e-13 |
| 2 | D | 9.80 | 6 309 573 445 | -1.404e-02 | 2.81e-12 |
| 2 | D | 10.00 | 10 000 000 000 | -1.696e-02 | 2.14e-12 |
| 2 | D | 10.25 | 17 782 794 100 | 2.130e-01 | 1.51e-11 |
| 2 | D | 10.50 | 31 622 776 602 | -7.808e-02 | 3.12e-12 |
| 2 | E | 6.00 | 1 000 000 | 1.164e-09 | 1.52e-15 |
| 2 | E | 7.00 | 10 000 000 | -4.265e-07 | 5.56e-14 |
| 2 | E | 7.50 | 31 622 777 | -5.186e-06 | 2.14e-13 |
| 2 | E | 8.00 | 100 000 000 | -3.502e-06 | 4.57e-14 |
| 2 | E | 8.25 | 177 827 941 | -3.830e-05 | 2.81e-13 |
| 2 | E | 8.50 | 316 227 766 | -8.318e-05 | 3.43e-13 |
| 2 | E | 8.75 | 562 341 325 | -8.476e-05 | 1.97e-13 |
| 2 | E | 9.00 | 1 000 000 000 | 4.721e-05 | 6.16e-14 |
| 2 | E | 9.10 | 1 258 925 412 | 4.110e-04 | 4.26e-13 |
| 2 | E | 9.20 | 1 584 893 192 | 1.734e-03 | 1.43e-12 |
| 2 | E | 9.30 | 1 995 262 315 | 2.068e-03 | 1.35e-12 |
| 2 | E | 9.50 | 3 162 277 660 | 5.528e-03 | 2.28e-12 |
| 2 | E | 9.80 | 6 309 573 445 | -1.429e-03 | 2.95e-13 |
| 2 | E | 10.00 | 10 000 000 000 | -2.390e-02 | 3.12e-12 |
| 2 | E | 10.25 | 17 782 794 100 | 2.434e-02 | 1.79e-12 |
| 2 | E | 10.50 | 31 622 776 602 | -1.108e-01 | 4.57e-12 |
| 2 | F | 7.00 | 10 000 000 | -3.632e-07 | 5.12e-14 |
| 2 | F | 7.50 | 31 622 777 | 4.288e-06 | 1.91e-13 |
| 2 | F | 8.00 | 100 000 000 | -2.240e-05 | 3.15e-13 |
| 2 | F | 8.25 | 177 827 941 | -1.988e-05 | 1.57e-13 |
| 2 | F | 8.50 | 316 227 766 | 1.670e-04 | 7.44e-13 |
| 2 | F | 8.75 | 562 341 325 | 5.162e-05 | 1.29e-13 |
| 2 | F | 9.00 | 1 000 000 000 | 1.473e-04 | 2.08e-13 |
| 2 | F | 9.10 | 1 258 925 412 | -3.076e-05 | 3.44e-14 |
| 2 | F | 9.20 | 1 584 893 192 | -4.411e-04 | 3.92e-13 |
| 2 | F | 9.30 | 1 995 262 315 | -1.220e-03 | 8.61e-13 |
| 2 | F | 9.50 | 3 162 277 660 | 9.689e-04 | 4.32e-13 |
| 2 | F | 9.80 | 6 309 573 445 | 1.489e-02 | 3.32e-12 |
| 2 | F | 10.00 | 10 000 000 000 | 2.661e-02 | 3.75e-12 |
| 2 | F | 10.25 | 17 782 794 100 | -1.411e-02 | 1.12e-12 |
| 2 | F | 10.50 | 31 622 776 602 | 2.513e-01 | 1.12e-11 |
| 3 | D | 7.00 | 10 000 000 | -8.848e-07 | 1.12e-13 |
| 3 | D | 8.00 | 100 000 000 | 1.051e-05 | 1.33e-13 |
| 3 | D | 9.00 | 1 000 000 000 | 6.533e-04 | 8.26e-13 |
| 3 | D | 10.00 | 10 000 000 000 | -1.061e-02 | 1.34e-12 |
| 3 | D | 10.50 | 31 622 776 602 | -8.828e-02 | 3.53e-12 |
| 3 | D | 11.00 | 100 000 000 000 | 4.511e+00 | 5.70e-11 |
| 3 | D | 11.50 | 316 227 766 017 | 2.760e+02 | 1.10e-09 |
| 3 | D | 11.70 | 501 187 233 627 | 3.743e+02 | 9.44e-10 |
| 3 | D | 11.80 | 630 957 344 480 | 3.998e+02 | 8.01e-10 |
| 3 | D | 11.90 | 794 328 234 724 | 3.949e+03 | 6.29e-09 |
| 3 | D | 12.00 | 1 000 000 000 000 | 1.129e+04 | 1.43e-08 |
| 3 | F | 7.00 | 10 000 000 | 1.055e-06 | 1.49e-13 |
| 3 | F | 8.00 | 100 000 000 | -2.143e-05 | 3.02e-13 |
| 3 | F | 9.00 | 1 000 000 000 | 3.114e-04 | 4.39e-13 |
| 3 | F | 10.00 | 10 000 000 000 | 2.208e-02 | 3.11e-12 |
| 3 | F | 10.50 | 31 622 776 602 | 2.133e-01 | 9.50e-12 |
| 3 | F | 11.00 | 100 000 000 000 | -8.868e+00 | 1.25e-10 |
| 3 | F | 11.50 | 316 227 766 017 | -4.793e+02 | 2.13e-09 |
| 3 | F | 11.70 | 501 187 233 627 | 1.279e+03 | 3.59e-09 |
| 3 | F | 11.80 | 630 957 344 480 | 3.591e+03 | 8.02e-09 |
| 3 | F | 11.90 | 794 328 234 724 | 5.365e+03 | 9.51e-09 |
| 3 | F | 12.00 | 1 000 000 000 000 | -2.472e+03 | 3.48e-09 |
| 4 | G | 9.00 | 1 000 000 000 | 1.043e-03 | 1.32e-12 |
| 4 | G | 10.00 | 10 000 000 000 | -3.934e-02 | 4.97e-12 |
| 4 | G | 11.00 | 100 000 000 000 | 5.545e+00 | 7.01e-11 |
| 4 | G | 12.00 | 1 000 000 000 000 | 1.133e+04 | 1.43e-08 |

### Verification file `verification.json`: 106 of 106 cases bit-identical, 0 failures

- rounds simulated by both implementations: 90 300 000
- awarded cubes: 7 591; monitor firings: 54; Stage-3 (fallback) rounds: 311 520
- Lemma P2 violations counted: 4; Lemma P4 violations counted: 8

### Verification file `verification_d1.json`: 240 of 240 cases bit-identical, 0 failures

- rounds simulated by both implementations: 576 000 000
- awarded cubes: 8 640; monitor firings: 304; Stage-3 (fallback) rounds: 24 538 947
- Lemma P2 violations counted: 0; Lemma P4 violations counted: 0

<!--/A3TABLES-->

## 5. Verification of the fast implementation against the slow one

The slow reference is `run()` in `scratch/experiments/round2/ctx_local/cg_struct.py`, read only for
this package and not modified. Two independent suites compare the C kernel against it, and the two
C builds against each other.

**Suite 1, the per-agent-context reading (`dctx = K`).** 106 of 106 cases bit-identical, for
`libcgmesp.so` (job 64822513) and again for `libcgmesp_v2.so` (job 64823294): 90 300 000 rounds
simulated twice, 7591 awarded cubes, 62 cases with a positive announced price, 54 monitor firings,
311 520 Stage-3 fallback rounds, 4 counted Lemma P2 violations and 8 counted Lemma P4 violations, on
all five instances and at `K = 2, 3` and `4`.

**Suite 2, the common-context reading (`dctx = 1`).** There is no slow reference for the revised
model, so one was constructed out of the existing one rather than written fresh, which would have
verified a new implementation against another new implementation. The embedding is exact: drive the
unmodified reference on a **diagonal** context path, `X_t = (x_t, ..., x_t)`. Then
`M_j(X_t[j]) = M_j(x_t)` for every `j`, which is the common-context evaluation, and the reference's
cell key is the diagonal cell, in bijection with the one-dimensional cell. Every branch of the
mechanism is then the common-context mechanism, executed by code that was not touched. The grid side
and the elicitation block are passed as the common-context values `ceil(n^{1/(d+3)})` and
`ceil(n^{2/(d+3)})` with `d = 1`, and the oscillation multiplier is set so that the reference's
structural `rho` equals the mechanism's own `rho_n = sqrt(d) h_n log(e n)` bit for bit. No other
parameter is touched.

**A first version of suite 2 passed and was thrown away, because it was vacuous.** 160 of 160 cases
were bit-identical over 176 000 000 rounds, with **zero** positive-price cubes, **zero** monitor
firings and **zero** Stage-3 rounds: every horizon in it was below the `d = 1` price threshold, so
the two implementations agreed about a mechanism that was doing nothing. The suite was re-run with a
horizon of `5 x 10^6` added, where `sigma_n = 0.739` against a second capacity of about 0.79, so the
price is positive, the monitor can fire and the fallback runs.

**Result of suite 2 (job 64829324): 240 of 240 cases bit-identical**, over 576 000 000 rounds
simulated twice, with **2422 positive-price cubes, 304 monitor firings and 24 538 947 Stage-3
fallback rounds**, on all five instances and at `K = 2, 3` and `4`, under the proposed profile, all
six deviations and the joint sabotage profile. Lemma P2 violations counted: zero, which at these
parameters is the correct answer rather than an absent test, since the sharp parameters at which
that counter is nonzero live in suite 1. The common-context kernel is therefore checked against the
unmodified reference on exactly the branches the `d = 1` sweep exercises, and not only on the
degenerate ones.

**How the comparison is made, in both suites.** `np.random.default_rng` is intercepted by a recorder
that forwards every call to the real Generator and stores what came out: the context matrix, the
seed vector, every priority permutation in creation order, and, for every Stage-3 fallback draw, the
single uniform that `Generator.choice(K, p = p)` consumes. The C kernel is then replayed on exactly
those draws. Three things were checked first: the recorder's re-implementation of `choice` returns
the same index as numpy's on 18000 random `(K, p)` pairs and leaves the stream in the same place;
running the reference with and without the recorder gives identical output on every field; and every
integer count is compared for exact equality while the floating sums are compared against an
uncompensated accumulator in the C kernel that adds in the same order as the reference, so
"identical" means identical and not "identical to a tolerance".

**Build against build.** `libcgmesp.so`, `libcgmesp_v2.so` and `libcgmesp_v3.so` agree bit for bit
in production mode, where the draws come from the kernel's own streams and not from numpy, on 17
runs covering all five instances, both regimes, every deviation, 13 monitor firings and 4 020 252
Stage-3 rounds, and v3 at `dctx = K` reproduces v1 and v2 exactly, which is what makes the `d = 2`
and `d = 3` sweeps run before the model change still valid.

**One real bug was found this way**, and it is the kind a plausibility check would not have caught.
The first attempt at the software pipeline used a ring buffer of exactly the lookahead depth, so the
slot holding the current round's arrival was the slot the lookahead overwrote. Every aggregate still
looked reasonable: revenues within a fraction of a per cent, prices in the right range, the same
qualitative behaviour. The bitwise comparison rejected it immediately. A second, smaller one was
found the same way: an embedding that computed `rho` by a different but algebraically equal
expression, differing in the last bit, which the suite reported as a failure rather than absorbing.

## 6. What this changes for the paper

**Three sentences written elsewhere on this project are now wrong and should be replaced rather than
softened.** All three were correct about the horizons their authors could run and wrong as claims
about what is runnable.

* `audit/round2/B/theorems/f1-continuous-private/PROVER2.md` line 1413: "The theorem is asymptotic
  in a strong sense and no simulation can exhibit it." At `d = 1` a simulation exhibits it in a few
  seconds of one core, and at `d = 2` in about twenty minutes. The repair is to bound the claim by
  the dimension: it is true from `d = 4`, for the reason in Section 7.
* `audit/round2/A2/EXPERIMENT_REPORT.md` line 390: "The mechanism is numerically vacuous at every
  horizon anyone can run." False as stated. That package stopped at `2 x 10^6` rounds.
* `audit/round2/A2/EXPERIMENT_REPORT.md` line 472: "The right sentence for the paper is that the
  continuous mechanism is asymptotic in a strong sense, that no simulation can exhibit its
  guarantees, and that at every horizon anyone can run it degenerates to its elicitation schedule."
  The last clause is the one to drop: above the threshold the priced phase supplies almost all of
  the revenue.

**What to put in their place.** Four thresholds, in the order a reader meets them, with `d = 1`
numbers and the fact that `K` does not move them:

1. `10^5.25`, part (A) stops being weaker than the trivial bound.
2. `10^6.06`, a price **can** be positive on any instance, and `10^6.5` to `10^6.9`, where it
   actually is on these four instances. Quote both and say which is which.
3. `10^6.76` and `10^7.14`, parts (B) and (C) stop being weaker than the trivial bound.
4. `10^7.5` to `10^7.75`, the platform starts preferring compliance to total sabotage. This is the
   number an operator would care about and it is above all three of the others.

**And keep the reach table.** A referee will compute the horizon, and the right form of the sentence
is now: one-dimensional contexts are seconds, two dimensions are minutes, three are about two days,
and four is 109 GB of grid state before any horizon is run. Under the revised model `d` is the
dimension of the context itself rather than `K` times it, which moves the whole comparison down by a
factor of `K` in the exponent and is a much better position for the paper than the one it was in.

## 7. Dimension: where it becomes unreachable

Thresholds are computed from the mechanism's own parameter definitions with `K = 2` and Lipschitz
constant 1, by bisection on `log10 n`, in the same way `ctx_local/continuous.py` computes them; the
last three columns are this package's. Time is single core, using throughput measured as a function
of the number of grid cells (20.5 nanoseconds per round while the grid fits in cache, 59.3 at
`6.25 x 10^6` cells), not extrapolated from the small-grid rate. Memory is the two cell arrays, 144
bytes per cell, before anything else. The table is produced by
`scratch/experiments/round2/ctx_fast/reach_table.py`.

| d | log10 n, price can be positive | log10 n, all three non-vacuous | grid cells at that horizon | cell arrays | single-core time | reached here |
|--:|--:|--:|--:|--:|--:|:--|
| 1 | 6.1 | 7.1 | 61 | 0 MB | 0 s | yes, and exceeded by 1.9 decades |
| 2 | 8.5 | 9.8 | 8.46e+03 | 1 MB | 128 s | yes, and exceeded |
| 3 | 11.1 | 12.6 | 2.05e+06 | 295 MB | 2.0 days | price turn-on reached at 10^11.8 |
| 4 | 13.7 | 15.5 | 7.59e+08 | 109.3 GB | 13 core-years | no |
| 5 | 16.5 | 18.6 | 4.08e+11 | 58.8 TB | 2.5e+04 core-years | no |
| 6 | 19.4 | 21.7 | 2.95e+14 | 42 PB | 4.8e+07 core-years | no |

The `d = 4` line is the one that matters. The horizon at which the `d = 4` price can first be
positive, `10^13.75`, needs about 52 days of one core and 11 GB, which is awkward but not impossible
with checkpointing; the horizon at which all three `d = 4` guarantees are non-vacuous is not
reachable on this machine at all, and the obstruction is the grid, not the horizon. From `d = 5` the
grid alone is tens of terabytes.

**The `d = 4` probe that was run** is instance G (`K = 4`), and under the revised model it is a
`d = 4` instance in which agent `j` depends on coordinate `j`. It is far below the threshold and
behaves exactly as the earlier work described the whole mechanism as behaving: `sigma_n` falling
from 3.302 at `10^9` to 2.031 at `10^11`, never below 1; the announced price zero at every awarded
region; the monitor never firing against anything, including a winner that crashes; revenue falling
from 0.1955 to 0.0949 per round; and the platform collecting three times as much, 0.2881 per round,
when every strategic agent sabotages instead. It is reported as confirmation that the degenerate
regime is the degenerate regime, and for no other purpose.

**On instance F, part (B) is satisfied for a reason that has nothing to do with the mechanism.** The
honest agent is the top agent there, its intrinsic mean is `0.80 - 0.05 x` and the second capacity
is about 0.71, so an honest winner delivers more than the benchmark whatever the price is. The
part (B) deficit is negative at every horizon. That is a property of instance F and should not be
quoted as if it were evidence about CG-MESP.

## 8. Exact commands and seeds

All paths are relative to the repository root; `<venv>` is the package venv and `<scratch>` is
`<scratchpad>/round2/A3/`. Nothing was run on the login node except compilation, the verification
smoke test and the aggregation.

```
cd scratch/experiments/round2/ctx_fast
gcc -O2 -ffp-contract=off -fno-fast-math -fPIC -shared -o libcgmesp.so    cgmesp.c    -lm
gcc -O2 -ffp-contract=off -fno-fast-math -fPIC -shared -o libcgmesp_v2.so cgmesp_v2.c -lm

# verification against the unmodified reference (Slurm job 64822513 for v1, and for v2)
<venv>/bin/python verify.py --out <scratch>/verification.json

gcc -O2 -ffp-contract=off -fno-fast-math -fPIC -shared -o libcgmesp_v3.so cgmesp_v3.c -lm

# verification of the common-context reading against the same reference on a diagonal path
CGMESP_LIB=libcgmesp_v3.so <venv>/bin/python verify_d1.py --out <scratch>/verification_d1.json

# one sweep point (one Slurm array task runs a bundle of these); --d is the dimension of the
# common context space, and omitting it means the earlier reading d = K
CGMESP_LIB=libcgmesp_v3.so <venv>/bin/python sweep_run.py --inst C --logn 6.70 \
    --config proposed --seed 0 --d 1 --outdir <scratch>/results --save-tau

# aggregation, tables and figures
<venv>/bin/python aggregate.py       --results <scratch>/results --out <scratch>/csv
<venv>/bin/python report_tables.py   --csv experiments/data/A3 \
    --verification <scratch>/verification.json <scratch>/verification_d1.json
<venv>/bin/python make_figures_a3.py --csv experiments/data/A3 --out <out> --dim 1
<venv>/bin/python reach_table.py                                  # the Section 7 table

# all of the above in one step, including copying the aggregated CSVs into the repository
bash scratch/experiments/round2/ctx_fast/assemble.sh
```

`--config` is one of `proposed`, `underbid`, `rider25`, `rider50`, `rider100`, `both`, `crash`,
`sabotage_joint`. `--logn` is `log10 n` and the horizon is `round(10 ** logn)`. `--inst` is `C`, `D`,
`E` or `F` from `ctx_local/cg_struct.py`, or `G`, which is defined in `ctx_fast/cgfast.py` and is
instance D with a fourth agent added.

**Seeds.** `--seed s` is the integer `s`. In verification mode it is the seed of
`numpy.random.default_rng(s)` in the reference, whose draws are replayed into the kernel. In
production mode the kernel derives three xoshiro256++ states from `s` and a stream index, one for
arrivals, one for the Bernoulli seeds, one for the mechanism's own draws, so that arrivals and seeds
are identical across behaviour profiles at equal `s`. Seeds used: `0, 1, 2, 3` for the
`d = 2` sweep; `0` to `7` for the whole `d = 1` sweep; `0, 1, 2` for the `d = 3` grid up to
`10^11.5`; `0, 1` for `10^11.7` and `10^11.8` and for the `d = 4` probe up to `10^11`; `0` for every
horizon above that.

**Slurm.** Partition `cpu`, account `<slurm-account>`, one core and 8 to 32 GB per task,
no GPUs anywhere. Job ids, scripts, array ranges and purposes are in
`audit/round2/A3/COMPUTE_LOG.md`.

## 9. What this is not

* Not an equilibrium result. Six unilateral deviations and one joint profile were simulated. The
  numbers are lower bounds on exploitability for exactly those behaviours. Nothing here certifies a
  best response, and nothing here is evidence about the deviation class `B^ctx_{i,n}` as a whole.
* Not real data. Fully synthetic simulation on four instances defined by affine capacity and
  intrinsic maps, plus one more defined here for the `d = 4` probe. The arrival path is independent
  uniform on the cube, which is the arrival law the reference uses; the upgraded hypothesis (A4f) of
  `PROVER2.md` Section 17 permits far more than that, and nothing here tests a reactive path.
* Not a test of the lemmas at their sharp parameters. The structural regime, where `h` and `L` are
  set by hand so that the inequalities can be probed, is the earlier package's territory and is used
  here only inside the verification suite, where it is the setting in which Lemma P2 and Lemma P4
  violations can be made nonzero so that the two counters are themselves verified.
* Not free of implementation risk. What is established is that the C kernel and the reference
  Python agree bit for bit on every case of both suites, and that the three C builds agree bit for
  bit with each other. If the reference itself misstates the mechanism, this package inherits
  that, and it inherits it exactly.
