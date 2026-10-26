# Experiment report, package A2: the contextual mechanisms (24 September 2026)

Experimental evidence for the two contextual private-capacity mechanisms, which had none: **PL-MESP**, the
profile-local mechanism for finitely many context profiles, and **CG-MESP**, the continuous-context mechanism.
The scalar package `audit/round2/A/EXPERIMENT_FINAL_REPORT.md` is the standard this one is written to, and its
evidence-category discipline is used unchanged. No canonical file was modified.

**Evidence categories, never mixed.**

1. *Exact computation.* Backward induction over exact binomial laws on a deterministic arrival path. No
   sampling, no seed, no Monte Carlo error. The only approximations are double precision and an explicitly
   accounted truncation of Stage-1 count mass, carried into the reported bracket and reported per cell (the
   largest dropped mass over the whole grid is recorded in Section 5).
2. *Synthetic paired simulation.* Tape-coupled replicates of the mechanism and its ablations. Every number in
   this category is a **lower bound** on exploitability for the behaviour class simulated, never an upper
   bound.
3. *Analytic evaluation.* The threshold tables for both mechanisms are the mechanism's own parameters and the
   theorem's own error terms evaluated exactly at a stated horizon, dimension and profile count. They are
   arithmetic, not experiments, and are labelled as such.

Nothing here is deployment evidence, offline evaluation of logged decisions, real-data evidence, or evidence
about human behaviour. No searched or hand-picked deviation is described as proof of equilibrium anywhere.

**Where the numbers live.** Every number quoted below comes from a file named beside it, and every table is
generated from the CSVs by `scratch/experiments/round2/ctx_local/report_tables.py` rather than transcribed.
The full generated tables are in `TABLES.md` beside this file; the CSVs are under
`<scratchpad>/round2/A2/csv/`; the raw per-cell JSON under `<scratchpad>/round2/A2/results/`; the Slurm job
ids in `COMPUTE_LOG.md`.

## 0. Status

This package was built and run in one working day, and the long horizons are still computing. What it
contains at the time of writing:

* **Exact computation.** 144 cells of the PL-MESP grid, over eight instance families, `K = 2` and
  `K = 3`, profile counts 1 to 8 and horizons 2000, 8000 and 20000, with the 50000 cells beginning to land,
  each on a deterministic arrival path.
  Every cell carries a certified interval for the deviation gain over the full class `B^ctx_{i,n}`, the exact
  revenue bracket, both benchmarks and the published constant with its terms separated.
* **Synthetic paired simulation.** Eighteen cells of the contextual ablation ladder at `n = 20000`, each 8
  mechanism rungs by 19 behaviour profiles by 200 paired replicates.
* **Analytic evaluation.** The complete regime tables for PL-MESP and the complete threshold and degeneracy
  tables for CG-MESP; these do not depend on any job.
* **CG-MESP simulation.** The six structural-regime blocks, the oscillation sweep, the nine tuned-regime runs,
  and reruns of both of the prover's own price-lemma experiments.
* **Validation.** All five checks at `n = 2000` and `n = 8000`.

Section 10 lists what did not finish and the job ids. Nothing incomplete is estimated anywhere in this report,
and `<scratchpad>/round2/A2/slurm/finalize.sh` rebuilds every CSV, table and figure from whatever results
exist when it is run.

## 1. The mechanism this package tests, and why that one

PL-MESP is taken as adjudicated in `audit/round2/B/theorems/c2-local-mesp/ADVERSARY.md` Section 9.4:

* mechanism from `PROVER2.md` Section 2: one independent scalar MESP per exact context profile, round-robin
  Stage 1 of `K L_n` visits per profile, a single locally restarted EXP3 tuned to the **global** horizon `n`;
* calibration from PROVER1: `s_n = sqrt(log(2 K n^4) / (2 L_n))` and `b_n(r) = sqrt(r log(2 n^4) / 2)`, which
  are exactly the constants already coded for the scalar mechanism in
  `scratch/experiments/round2/common/design.py`, so the scalar and the profile-local computation share one
  definition of every constant;
* statement from PROVER1: the cap `min{Q L_n, n}` on the bidding term (adversary finding F7) and the
  per-profile split of the error.

Two consequences matter for the experiment. First, at `Q = 1` the mechanism **is** the scalar mechanism, so the
profile-count-one cell of every sweep below is the scalar baseline rather than an approximation to it. Second,
the published bound of part (A) is

```
  C(n, K, Q) = min{Q L_n, n} + Q + sqrt(2 Q n log(2 n^4)) + Q R_K(n) + e_low + 6 n^{-3},
  e_low      = sum over the deviator's non-top profiles z of
                 8 (1 + sqrt(2 log(2 n^4)))^2 / (delta_i^z)^2  +  2 R_K(n) / delta_i^z,
```

and at `Q = 1` with `e_low = 0` this is `L_n + 1 + 2 b_n(n) + R_K(n)`, the scalar constant of
`common/design.py::theorem_constant_top` plus one, because `2 b_n(n) = sqrt(2 n log(2 n^4))`. That identity is
what makes the two packages comparable, and check V1 of Section 9 verifies it numerically.

The proof's own finite-`n` condition for the non-top branch is `4 s_n <= delta_i`. Where it fails, comparing a
certified interval against `C` is **invalid rather than merely uninformative**, exactly as adjudicated for the
scalar package (`EXPERIMENT_FINAL_REPORT.md` Section 8 item 2). Those cells are marked and excluded from every
range quoted below, and reported by their certified interval alone.

## 2. Why a per-profile backward induction certifies a globally adaptive deviation

The class `B^ctx_{i,n}` lets the deviator condition its target at a visit to `z` on its entire history at every
other profile. A per-profile computation nevertheless gives the exact supremum over that class:

1. realized utility is additive over profiles and expectation is additive with no independence assumption, so
   `u_i(S') = sum_z E[U_{i,z}(S')]` (`PROVER2.md` equation (5.4));
2. the mechanism's phase, price, winner, switch time and fallback law at `z` are functions of the data
   collected at `z` and of coins attached to `z` alone (`PROVER2.md` Lemma L), and every non-deviating agent
   plays the profile-local `S^*`, so the reward process at `z` is conditionally independent of everything
   realized at other profiles given the deviator's own play at `z`;
3. hence `E[U_{i,z}(S')]` is at most the supremum over profile-local policies at `z`, whatever the deviator
   conditions on elsewhere, and the product of the per-profile optima is itself a member of `B^ctx_{i,n}`.

So the supremum over the global class equals the sum of the per-profile suprema. The arrival path is
deterministic throughout, which hypothesis (H3) permits, so the visit counts `V_z` are constants and knowledge
of the path does not enlarge the class. This is recorded because a referee will ask why a local dynamic program
bounds a global deviation; it is also why the computation is affordable at all.

Within a profile the two-action backward induction is exact for the same reason as in the scalar package: the
one-step objective `1 + mu_i - m + m W(s,1) + (1 - m) W(s,0)` is affine in the target, so an optimal target is
an endpoint of the feasible interval. The fallback continuation is bracketed rather than solved, as in
`exploitability/dp.py`: `F = 0` gives a certified lower bound, and the appendix's own bound evaluated with the
prefix form of Lemma F at the global tuning gives a certified upper bound. A profile whose Stage 1 never
finishes has no price, no monitor and no fallback, so its value is a closed form with no bracket at all.

## 3. What was built, and what was reused

| component | code | reused from |
|:--|:--|:--|
| mechanism constants | `common/design.py` | unchanged from the scalar package (`L_n`, `s_n`, `b_n`, `gamma_n`, `R_K`) |
| per-profile exact backward induction, exact bid and winner laws, exact revenue bracket | `audit/round2/B/theorems/e1-equilibrium-strength/bidprofile.py` | unchanged, imported |
| the three substitutions that turn the scalar computation into the local one (`local_design`, `fallback_bound`) | `audit/round2/B/theorems/e1-equilibrium-strength/ctxprofile.py` | copied with attribution into `ctx_local/plmesp_exact.py` |
| scalar reference computation for the validation | `scratch/experiments/round2/exploitability/dp.py` | unchanged, imported |
| monitored Stage-2 segment, price rule, EXP3 constants, behaviour classes | `common/mechanism.py` | unchanged, imported by `ctx_local/ctxmech.py` |
| seed scheme | `common/seeds.py` | unchanged |
| CG-MESP structural-regime episode and the price-lemma test | `<scratchpad>/round2/explorer-f1/tight.py`, `<scratchpad>/round2/f1-prover2/price_lemmas.py` | construction followed, rewritten self-contained in `ctx_local/cg_struct.py`, with two further instances, the oscillation-multiplier sweep and the parts (B) and (C) checks added |
| CG-MESP threshold bisection | `<scratchpad>/round2/f1-prover2/horizons.py` | recomputed from the parameter definitions in `ctx_local/continuous.py`, extended to part (C), to `K`, to the Lipschitz constant, and to the public comparison |

New in this package: the profile grid and the truncated-profile closed form (`ctx_local/plmesp_exact.py`), the
profile-local theorem constant, the profile-count and horizon sweep (`ctx_local/run_exact.py`), the contextual
ablation ladder including the pooled-statistics rung (`ctx_local/ctxmech.py`, `ctx_local/run_ladder.py`), the
validation suite (`ctx_local/validate.py`), the aggregation and regime tables (`ctx_local/aggregate.py`), the
table generator (`ctx_local/report_tables.py`) and the figures (`figures/make_figures_a2.py`).

## 4. Instances

Eight families, each parametrised by the profile count `Q`. The `replicated_*` families carry the same
primitives at every profile. That is deliberate: in them the contextual environment is degenerate, the scalar
mechanism is available, and PL-MESP pays pure localisation overhead with no offsetting benefit, so they isolate
the cost the obvious referee question is about. `rotating_top` and `heterogeneous` are genuinely contextual.
`regime_switch` is built so that pooling statistics across profiles breaks the price, and
`unbalanced_unique_top` has geometrically decreasing visit shares so that its later profiles never finish
bidding.

| family | K | primitives | purpose |
|:--|:--|:--|:--|
| `replicated_unique_top` | 3 | the scalar instance `unique_top` at every profile, `M = (0.90, 0.65, 0.40)` | localisation cost, unique top |
| `replicated_tied_top` | 3 | the scalar instance `tied_top`, `M = (0.80, 0.80, 0.45)` | localisation cost, capacity tie |
| `replicated_near_gap` | 3 | the scalar instance `near_gap`, `M = (0.80, 0.76, 0.50)` | localisation cost, small gap |
| `replicated_K2_unique` | 2 | the scalar instance `K2_unique_top`, `M = (0.90, 0.65)` | `K = 2`, the largest reachable `Q` |
| `replicated_honest_top` | 3 | the scalar instance `honest_top`, honest agent on top, `mu_H^* = 0.75` | ladder only, a high honest benchmark |
| `rotating_top` | 3 | the two strategic agents' capacities swap with the profile index, 0.80 against 0.65 | the deviator is top at half the profiles and non-top, gap 0.15, at the rest |
| `heterogeneous` | 3 | `M_0` falls 0.90 to 0.60 and `M_1` rises 0.55 to 0.85 across profiles | a range of gaps including a near tie |
| `regime_switch` | 3 | alternating `M = (0.90, 0.85, 0.40)` and `M = (0.45, 0.40, 0.25)` | the pooled second capacity, 0.625, exceeds the largest capacity at a low profile, 0.45 |
| `unbalanced_unique_top` | 3 | `unique_top` primitives, visit shares proportional to `2^{-l}` | profiles that never finish bidding |

## 5. Exact exploitability of PL-MESP

*(exact computation; deterministic arrival path; `exact_grid.csv`, `exact_profiles.csv`, `TABLES.md`)*

**What the computation produces per cell.** A certified interval `[LB, UB]` for
`sup over B^ctx_{i,n} of u_i(S'_i, S^*_{-i}) - u_i(S^*)`, the exact revenue bracket under `S^*`, the exact
second-capacity and honest benchmarks along the same arrival path, and the published constant `C(n, K, Q)` with
its four terms separated. `LB` uses a zero fallback continuation for the deviator together with the exact upper
end of the baseline bracket; `UB` uses the appendix fallback bound together with the exact lower end of the
baseline bracket. The interval is rounded outward, never inward.

**Headline, as of the 144 cells computed when this report was written.** The certified interval never exceeded
the published constant, at either end, in any cell. Restricted to the 57 cells in which every profile finishes
its bidding stage **and** the theorem's own non-top condition `4 s_n <= delta_i` holds, the certified upper
bound is 0.105 to 0.540 of the published constant and the certified lower bound is 0.075 to 0.540 of it. The
largest Stage-1 count mass dropped by the truncation anywhere in the grid is `6.0e-13`, so every reported
bracket is exact far beyond the digits quoted. All five of these figures are recomputed by the `Checks` block
at the head of `TABLES.md`, which is the authority once the remaining jobs of Section 10 land.

**Three structural facts the exact computation makes visible. The theory documents name the first two
qualitatively (PROVER2 stress point 4 and the bracketing of the fallback) and do not mention the third; none of
the three is quantified anywhere.**

1. *The certified interval collapses to a point in every cell whose optimum never reaches a fallback.* When the
   certified optimum is to shade the bid and lose the auction, or when the monitor is inert (item 3), the
   deviator is never switched, the fallback bracket is never entered, and `LB = UB` exactly. This is not a
   numerical coincidence and it is reported as such; the count of such cells is in `TABLES.md`.
2. *A profile whose Stage 1 never finishes is maximally exploitable, in closed form.* Its whole visit budget
   consists of Stage-1 pulls, so the deviator saves `M_i^z` of effort on each of its own pulls with no
   consequence at all, and the exact value is `l_i(z) (M_i^z - lo_i^z)` with `lo_i = mu_i` for an honest
   deviator and `0` otherwise. When every profile is truncated the whole mechanism degenerates to round robin
   and the certified per-round gain is `M_i / K` on the replicated families up to the round-robin remainder,
   which falls to the lowest-indexed agents: the grid gives 0.3000 to 0.3015 against `M_i / K = 0.3000` for
   `replicated_unique_top`, 0.2667 to 0.2680 against 0.2667 for `replicated_tied_top`, and 0.4500 to 0.4513
   against 0.4500 for `replicated_K2_unique`. That is the no-protection value: in that regime the mechanism
   gives no incentive guarantee at all, because it never prices and never monitors.
3. *The monitor at a profile is inert unless the profile is long enough.* The test can fire after local primary
   pull `r` only if `r tau - b_n(r) > 0`, that is only if `r > log(2 n^4) / (2 tau^2)`. With
   `N_z = n/Q - K L_n` post-bidding visits, a profile with `N_z` at or below that index carries a monitor that
   cannot convict any winner however little it delivers. This is a second threshold on `Q`, tabulated per
   profile in `exact_profiles.csv` as `monitor_first_binds_at_r` and `monitor_active`.

**The exact optimum is far above the hand-picked deviation the theory exhibits.** Proposition 6.1 of
`PROVER2.md` shows the `Q L_n` term is attained by shading the Stage-1 target to `(M_i + V_i)/2` at every
profile where `i` is uniquely top. Over the cells in which that deviation is available and every profile
finishes bidding (60 cells over seven families), the certified **lower** bound is 2.65 to 38.65 times that
deviation's value. The scalar
package found the same phenomenon at a factor of three to four; the profile-local mechanism is worse because
the deviator collects the bidding saving once per profile.

## 6. What localisation costs

*(exact computation and analytic evaluation; `exact_grid.csv`, `regime.csv`, `nontop_thresholds.csv`)*

This is the obvious referee question: is running one instance per profile worse than the scalar mechanism, and
by how much. In the `replicated_*` families the contextual environment is degenerate, so the `Q = 1` cell is
literally the scalar mechanism on the scalar instance of the same name and every difference at `Q > 1` is the
price of localisation with no offsetting benefit.

**Headline.** The certified exploitability per round is **non-decreasing in the profile count** at every
horizon and in every family computed, with no exception outside the pairs of cells in which both members are
already fully truncated, where the round-robin remainder can move it down by at most 0.0083 per round. On
`replicated_unique_top` at `n = 8000`, `K = 3`, the certified upper bound per round runs 0.0790 at `Q = 1`,
which **is** the scalar mechanism, then 0.1200 at `Q = 2`, 0.2728 at `Q = 3` and 0.3001 at `Q = 4`; at `Q = 4`
no profile finishes bidding, the mechanism never prices and never monitors, and 0.3001 is the no-protection
value `M_i / K`. So three profiles are enough, at that horizon, to take the mechanism from an exploitability of
0.079 per round to 3.8 times that, and four are enough to remove the guarantee entirely. The number of
profiles at which the monitor is still active falls from 1 of 1, to 2 of 2, to 3 of 3, to 0 of 4 over the same
range: the mechanism does not degrade gradually, it stops.

**Revenue moves the other way, and the report says so rather than picking the flattering direction.** On the
replicated families the exact revenue per round *rises* with `Q`, because the extra bidding blocks are rounds
in which every agent delivers its capacity rather than the announced price. On `replicated_unique_top` at
`n = 8000` the exact revenue per round is 0.5499, 0.5977, 0.6455, 0.6501, 0.6502 and 0.6502 at `Q = 1` to `6`,
against a second-capacity benchmark of 0.6500. At `Q >= 4`, where the mechanism never prices and never
monitors, it nevertheless matches the theorem's own revenue target to four decimals (0.6501 to 0.6502 against
0.6500), because round-robin bidding on this instance happens to deliver the mean capacity and the mean
capacity here equals `M_(2)`. That coincidence is a property of the instance, not of the mechanism. So
localisation is not a revenue cost on these instances; it is an incentive cost, and it is paid in full.

**The two thresholds on the profile count.** The mechanism is implementable, in the sense that every profile
finishes its bidding stage, only when `Q K L_n <= n`, that is `Q <= n^{1/3} (log(e n))^{-1/3} / K` up to the
floor in `L_n`. Under an even arrival path this is the binding constraint. Over the whole analytic sweep
(`regime.csv`, 37 horizons from `10^3` to `10^12`, `Q` from 1 to 2048, `K = 2` and `K = 3`, so 74 horizon-by-`K`
cells), the largest `Q` at which the published bound with `e_low = 0` falls below the trivial bound `2n` equals
the largest `Q` at which every profile finishes bidding in **all 74** cells, with no exception. The
monitor-activity threshold of Section 5 item 3, evaluated at a representative price of 0.5, agrees with both in
69 of the 74 cells and is one lower in the other five (`K = 2` at `n = 5623`, `31622` and `562341`; `K = 3` at
`n = 1000` and `1778`). So there is essentially one threshold to state, and the theory's "`Q` small relative to
the cube root of the horizon" is exactly it. Concretely, with
`K = 3`: `Q <= 3` at `n = 10^4`, `Q <= 6` at `10^5`, `Q <= 13` at `10^6`, `Q <= 27` at `10^7`, `Q <= 57` at
`10^8`. With `K = 2`: 4, 9, 20, 41 and 76 at the same horizons.

**The non-top term is the other vacuity mechanism, and it is far more aggressive.** `e_low` grows like
`delta^{-2}`, so one profile at which the deviator is non-top with a modest gap can push the published constant
past `2n` by orders of magnitude while the certified gain stays near a quarter per round: in the
`heterogeneous` family at `n = 8000` the published constant reaches 935.96 per round at `Q = 6` against a
certified gain of 0.2503 per round. Worse, the proof's own condition `4 s_n <= delta_i` fails at every horizon
this package can reach for the gaps in `rotating_top` (0.15) and `heterogeneous` (down to 0.05). In those cells
the comparison with the constant is **invalid rather than uninformative**, and they are reported by their
certified interval alone. The smallest horizon at which the condition holds is `10^{5.86}` for `delta = 0.15`,
`10^{6.43}` for `delta = 0.10` and `10^{7.39}` for `delta = 0.05` at `K = 2`, and within 0.01 in the exponent
of those values at `K = 3` (`nontop_thresholds.csv`).

## 7. The contextual ablation ladder

*(synthetic paired simulation; `ladder.csv`, `TABLES.md`)*

Eight rungs, each changing exactly one component of PL-MESP, against 19 behaviour profiles including four
joint profiles in which every strategic agent deviates. The rungs are: the mechanism itself; the monitor
removed; a windowed monitor of width 200; the monitor with no slack (no `b_n(r)` boundary); the price
correction removed (`tau = beta_(2)`); the fallback replaced by round robin; the fallback replaced by the
unmonitored runner-up; and **statistics shared across profiles** rather than kept separate, which is the design
choice the whole construction rests on and which no document had measured.

The shared rung is the scalar mechanism run context-blind: one bidding stage of `K L_n` rounds taken off the
front of the arrival path with the Stage-1 rewards pooled over whichever profiles those rounds fell in, one
announced price, one winner, one monitor for the rest of the horizon and one fallback. It is also the exact
`Q = 1` consistency check, since with one profile it must coincide with PL-MESP replicate by replicate.

**Headline, and a cross-package check.** At `Q = 1` the ladder is the scalar mechanism, so it can be compared
with the scalar package directly. On `replicated_unique_top` at `n = 20000`, `Q = 1`, 200 paired replicates,
the best tested unilateral deviation per round is **0.01225** for PL-MESP (adaptive Stage-1 underbidding),
**0.11323** for the windowed monitor, and **0.40626** for the monitor removed, the last by bait and switch.
The scalar package reports, over its three instances whose focal agent contests the bidding and at the same
horizon, every anytime-monitored variant at 0.006 to 0.012, the windowed monitor at 0.059 to 0.113 and the
unmonitored mechanism at 0.268 to 0.489. This package's 0.40626 is inside that last range; its 0.01225 and
0.11323 sit at the upper ends of the first two and round to 0.012 and 0.113 at the precision the scalar package
quotes, which is what one expects since `unique_top` is the instance that attains those upper ends. The
contextual simulator shares the monitored-segment routine, the price rule, the EXP3 constants and the
behaviour classes with the scalar one, and implements the episode, the Stage-1 schedule and the fallback loop
separately. `rotating_top` at `Q = 1` gives 0.01218, 0.11324 and 0.40626 for the same three rungs.

**The ordering is reproduced on a contextual instance.** On `regime_switch` at `n = 20000`, `Q = 2`: PL-MESP
0.02504; the runner-up fallback 0.02490 and the round-robin fallback 0.02501, which coincide with PL-MESP
because no switch occurs under the best unilateral deviation at this horizon; the raw price 0.02529; the
windowed monitor 0.07628, three times PL-MESP; the no-slack monitor 0.10642; and the monitor removed 0.26028,
ten times PL-MESP.

**The fallback and the monitor are what keep the platform near the honest benchmark under joint sabotage, and
the difference is a factor of three and a half.** Under the worst of the four joint profiles, in which every
strategic agent delivers its floor in every phase, the platform's headroom against `E sum_t b(X_t)` at
`replicated_unique_top`, `n = 20000`, `Q = 1` is **-0.05333** per round for PL-MESP, **-0.09056** with the
fallback replaced by round robin, and **-0.19054** with the fallback replaced by the unmonitored runner-up or
with the monitor removed. Every rung falls below the benchmark here, because a quarter of the horizon is
bidding blocks in which the two strategic agents deliver nothing; that shortfall is the theorem's own
`e_stage1` term and is far inside the part (C) slack. What the ladder separates is how much **more** than that
each ablation loses, and the answer is up to three and a half times as much. On `rotating_top` the same three
numbers are -0.05333, -0.09871 and -0.19869.

**The ladder confirms the exact computation's saturation prediction, from simulation.** At `regime_switch`,
`n = 20000`, `Q = 6`, every profile is truncated, and **all seven local rungs return the identical value
0.22500 per round**: with no price and no monitor the mechanism is round robin and the rungs have nothing left
to differ about. That value is `(0.90 + 0.45) / 2 / 3 = 0.225`, the deviator's mean capacity divided by `K`,
which is exactly the closed form Section 5 item 2 derives. The exact computation of that same cell returns a
certified interval of [0.225000, 0.225000] per round, so the simulated and the exact values agree to five
decimals at a cell where both are deterministic. At `Q = 4` the same collapse has already begun, with six of
the seven local rungs at 0.20908.

**The two rungs that are not read off the exploitability column.**

* **Statistics shared across profiles. This rung does not come out of the ladder looking worse than PL-MESP,
  and the report says so.** On every cell measured it is **less** exploitable than PL-MESP, not more, and it
  loses **less** under joint sabotage: at `replicated_unique_top` `n = 20000`, `Q = 2` its best tested
  deviation is 0.01225 per round against PL-MESP's 0.02495 and its worst joint honest headroom is -0.05323
  against -0.10631; at `rotating_top` `Q = 2` it is 0.00591 against 0.01245, with the same headroom pair; and
  at `regime_switch` `Q = 6`, where every profile is truncated and PL-MESP has degenerated to round robin, it
  is **0.03679 against 0.22500**, six times less exploitable. The reason is immediate and is the whole point of
  Section 6: the pooled mechanism runs **one** bidding block instead of `Q` of them, so it keeps a priced,
  monitored phase at profile counts where PL-MESP no longer has one. At `Q = 1`, where there is one profile, it
  coincides with PL-MESP in every column, as it must.

  The complete profile-count sweep of the ladder at `n = 20000` makes the mechanism of that gap explicit. The
  pooled rung's best tested deviation does not move with `Q` at all, because it always runs exactly one bidding
  block: 0.01225 at `Q = 1, 2, 3` and 6 on `replicated_unique_top`, 0.01218, 0.00591, 0.00603 on
  `rotating_top`, and 0.00604, 0.00573, 0.00567 on `replicated_tied_top`. PL-MESP's rises with `Q` and
  saturates at the no-protection value: 0.01225, 0.02495, 0.07163, 0.30002 on `replicated_unique_top`, and
  0.00604, 0.02049, 0.13946 on `replicated_tied_top`. The two coincide at `Q = 1` in every family, as they
  must. Revenue runs the other way on those families, 0.56432 for the pooled rung against 0.64992 for PL-MESP
  at `Q = 6`, for the reason given in Section 6.

  What sharing costs is not exploitability but the **validity of the price**, and that only shows on an
  instance whose capacities vary across profiles. On `regime_switch` its **switch rate under the proposed
  profile is 0.270 at `Q = 2` and 0.265 at `Q = 4`**, against **0.000** for PL-MESP and for every other local
  rung: in about 27 percent of replicates a winner that played `S^*` exactly was thrown out, after a median of
  12820.5 of its 15158 monitored rounds at `Q = 2`, and the mechanism fell into its fallback. Its revenue under
  the proposed profile is 0.50102 per round against PL-MESP's 0.52687 at `Q = 2`, and 0.37641 against 0.54139
  at `Q = 6`. The announced price is 0.51337 on average, a single number for both profiles, where PL-MESP
  announces 0.7374 at the high profile and 0.2874 at the low one. The scalar package's false-switch metric
  scores this rung **0.000**, because the convicted winner's target never fell below the announced price: it
  was above its own capacity. That is precisely why this report quotes the switch rate under the proposed
  profile instead.

  The honest reading, which the paper should carry rather than the flattering half of it: on these instances,
  at these horizons, pooling is the cheaper mechanism in both exploitability and joint robustness, and what
  profile-locality buys is a price that every winner can actually meet, which is what the equilibrium argument
  needs and what a revenue or exploitability number at a simulable horizon does not see.
* **The monitor with no slack.** Its switch rate under the proposed profile is 0.995 at both
  `replicated_unique_top` `Q = 1` and `regime_switch` `Q = 2`, after a median of 3.5 monitored rounds at the
  latter: without the `b_n(r)` boundary a compliant winner is convicted by ordinary noise almost immediately
  and in essentially every replicate. This is the measurement that shows why the boundary exists, and it is
  the same finding the scalar package reports.

**The price correction costs revenue and buys the price band.** Removing it (`tau = beta_(2)`) raises the
announced price from 0.53816 to 0.65072 and revenue from 0.56531 to 0.65021 per round at
`replicated_unique_top` `Q = 1`, a revenue cost of 0.0849 per round for the correction, and from 0.51246 to
0.62502 and 0.52687 to 0.58426, a cost of 0.0574 per round, at `regime_switch` `Q = 2`. In both cells it
leaves exploitability essentially unchanged (0.01226 against 0.01225, and 0.02529 against 0.02504).

**A conditioning that must be stated rather than averaged away.** On `replicated_honest_top` the honest agent
is the top agent, the strategic focal agent essentially never wins Stage 1, no monitor is ever exercised, and
every rung except the no-slack one shows the same value, 0.05719 per round at `n = 20000`, `Q = 1`, which is
pure Stage-1 shading. Quoting a range for the unmonitored mechanism over all families would therefore read
0.057 to 0.406 and would hide the effect rather than show it. The ladder is quoted on the instances where the
focal agent contests the bidding, and the exception is named. This is the correction the scalar package had to
make twice.

**One modelling choice in the simulator, stated because it is not neutral for one behaviour.** The
profile-local simulator processes profiles in index order. For every profile-local mechanism and every
profile-local behaviour that is exact whatever the true interleaving, because the mechanism's state at a
profile depends only on that profile's own data and utilities are additive over profiles. It is not neutral
for the single cross-profile behaviour, `cross_profile_freeride`, which starts delivering zero everywhere once
a switch has occurred anywhere: processing profiles in blocks corresponds to an arrival path in which every
visit to one profile precedes every visit to the next, and under an evenly spread path that behaviour would
start free riding later. The pooled rung uses the evenly spread path explicitly, because a pooled mechanism
does depend on the interleaving.

**On the false-switch metric.** The scalar package defined a false switch as a switch on a winner whose target
never fell below the announced price. That definition is not adequate for the pooled rung, where the announced
price can exceed the winner's capacity, so a fully compliant winner delivers its capacity, which is below the
price, and is convicted without ever having been counted as falsely switched. This report therefore quotes the
**switch rate under the proposed profile** instead: under that behaviour every agent plays `S^*` by
construction, so every switch there is a switch on a compliant winner, whatever the price happens to be.

## 8. The continuous mechanism, CG-MESP

*(analytic evaluation and synthetic simulation; `continuous_thresholds.csv`, `continuous_degeneracy.csv`,
`cg_structural.json`, `cg_oscillation.json`, `cg_tuned.json`)*

**The mechanism is numerically vacuous at every horizon anyone can run, and this report prints the thresholds
rather than working around them.** CG-MESP announces `tau_C = (beta_(2),C - sigma_n)_+` with
`sigma_n = 3 s_n + rho_n`. Empirical bids never exceed 1, so `sigma_n >= 1` forces `tau_C = 0` at every cube,
whatever the instance: the Stage-2 winner then delivers `min{0, M} = 0` if strategic, the monitor test
`Z_r < r * 0 - b_n(r)` never fires, and the mechanism collects nothing from a strategic winner outside its
bidding blocks. The dimension is `D = K d`, so with at least two agents the smallest case of any interest is
`D = 2`.

Two legitimate things were done, and they are kept apart.

**(a) The thresholds, computed from the mechanism's own parameters** (`ctx_local/continuous.py`, analytic;
`continuous_thresholds.csv`). Smallest `log10 n` at which each quantity first drops below its trivial value,
`K = 2`, Lipschitz constant 1:

| D | price can be positive | bound (A) below n | slack (B) below n | slack (C) below n | all of them | public contextual error below n |
|--:|--:|--:|--:|--:|--:|--:|
| 1 | 6.1 | 5.2 | 6.8 | 7.1 | 7.1 | 2.9 |
| 2 | 8.5 | 7.5 | 9.3 | 9.8 | 9.8 | 3.7 |
| 3 | 11.1 | 10.0 | 12.0 | 12.6 | 12.6 | 4.7 |
| 4 | 13.7 | 12.7 | 14.9 | 15.5 | 15.5 | 5.7 |
| 6 | 19.4 | 18.4 | 20.8 | 21.7 | 21.7 | 7.4 |
| 8 | 25.4 | 24.4 | 27.1 | 28.2 | 28.2 | 9.6 |
| 10 | 31.7 | 30.7 | 33.7 | 35.0 | 35.0 | 11.4 |
| 12 | 38.2 | 37.2 | 40.5 | 42.0 | 42.0 | 13.9 |

`D = 1` is listed for completeness only: `D = K d` with `K >= 2`, so no instance of the model has `D = 1`.
The first three columns agree with `PROVER2.md` Section 18 at every one of the six dimensions that report
lists (1, 2, 3, 4, 6 and 10) and at the printed resolution of 0.1 in the exponent; they were recomputed here
from the parameter definitions of `EXPLORER.md` Section 3 rather than read off that report. The part (C)
column, the remaining dimensions and the public comparison are new. Reading:
two agents with scalar contexts, `D = 2`, need `n` of order `10^{9.8}` before all three guarantees say
anything, and the manuscript's public contextual error for the same `D` is below `n` from `10^{3.7}`, a gap of
about six orders of magnitude in the horizon at `D = 2` and about 28 at `D = 12`. The exponents agree; the
constants do not, and the `2^D` in `J_n` is why. The threshold grows like `exp(cD)` rather than polynomially.

**(b) The lemmas verified at parameters satisfying the structural condition** (`ctx_local/cg_struct.py`,
synthetic simulation; `cg_structural.json`, `cg_oscillation.json`). The grid side `h` and the bidding block `L`
are set by hand and the shading is `sigma = 3 s + rho` with `rho = alpha L_lip sqrt(D) h`. The lemmas hold for
any `(h, L)` with `alpha >= 1`, because the oscillation allowance only has to dominate the within-cube
oscillation of an `L_lip`-Lipschitz capacity, which is at most `L_lip sqrt(D) h`. Running there tests the
**inequalities** and says nothing whatever about the rates. This is the regime `PROVER2.md` Section 11 and the
explorer's `tight.py` used; the construction is followed here and extended.

**Result for (b)** (`cg_structural.json`, six blocks: instances C, D, E and F at `n = 200000` and `400000`,
six seeds each). Over all six blocks: **zero** violations of Lemma P2 (the winner can meet the announced price
at every context of its cube), **zero** violations of Lemma P4 (the price is not far below the second
capacity), **zero** switches and therefore **zero** false alarms under the proposed profile, and all three
inequalities hold with room. The largest gain any of the seven deviations achieved, against the part (A)
budget, was 5752 against 81694 (instance C, `n = 200000`), 9903 against 140344 (C, `n = 400000`), 5182 against
169443 (D), 1512 against 132606 and 3106 against 241115 (E), and 5496 against 179835 (F). The deviations tried
were: shade the Stage-1 target to the midpoint; ride the monitor boundary at scales 0.25, 0.5 and 1.0; both
together; and crash immediately. Riding at scale 1.0 sits on the boundary and loses heavily, between 3804 and
66891 of utility, in every block but one. These are lower bounds for the deviations tried and nothing more.

For part (C) the whole strategic set sabotages: every strategic agent delivers its floor in every phase. The
honest-benchmark deficit was negative, meaning the platform stayed above the benchmark, in four blocks
(instances C and E), and positive but far inside the budget in the two blocks where the honest agent is not
the best bidder: 7414 against a budget of 396234 (instance D) and 96549 against 413555 (instance F).

**A null result that must be reported as one.** The oscillation-allowance sweep in this module found **zero**
violations of Lemma P2 at every multiplier tried, including a multiplier of zero, in both of its settings
(`cg_oscillation.json`, instance E at `g = 3, L = 4000` and `g = 6, L = 2000`, 54 and 216 awarded cubes over
six seeds). That is not evidence that the allowance is unnecessary: at those parameters the `3 s_n` part of the
shading is already 0.263 while the within-cube oscillation is at most `L_lip sqrt(D) h = 0.094`, so the
allowance had nothing left to pay for. The necessity of the allowance is established at sharper parameters,
and this package reproduced both of the prover's experiments verbatim rather than claiming the result on its
own evidence: with `sigma = s_n` alone and no allowance, `price_lemmas.py` gives 367 Lemma P2 violations in
4000 cubes, and the sharper near-tie setting of `threshold.py` gives violation rates 0.0272 at
`sigma = s_n`, 0.0060 at `sigma = s_n + 0.1 omega` and 0.0000 from `sigma = s_n + 0.2 omega` upward. Both
reruns are stored in `<scratchpad>/round2/A2/results/cg/`.

**(c) The mechanism at its own tuned parameters** (`cg_tuned.json`), so that the degeneracy is measured rather
than asserted. Nine runs, instances C, D and E, `n = 20000`, `200000` and `2000000`. In **every** run the
announced price was zero at **every** awarded cube (`zero_price_share = 1.000`, over 64 to 1728 awarded cubes
per run), `sigma_n` ran from 2.155 to 6.019, and the monitor never fired once, which is what a price of zero
implies. The revenue consequence is the part worth printing: on instance C (`D = 2`) the platform collected
0.2961, 0.1648 and 0.1041 per round at the three horizons, against a second-capacity benchmark of 0.7900, and
the share of the horizon spent in bidding blocks fell from 0.3392 to 0.1901 to 0.1199 over the same range. The
mechanism's revenue at runnable horizons is essentially whatever its bidding blocks deliver, and it **falls**
as the horizon grows, because the bidding share falls while the priced phase still collects nothing. On
instance D (`K = 3`, `D = 3`) revenue at `n = 20000` is 0.7560 against a benchmark of 0.7908, which looks
healthy only because 0.895 of the horizon is still bidding; by `n = 2000000` it is 0.2743 against 0.7908.
The right sentence for the paper is that the continuous mechanism is asymptotic in a strong sense, that no
simulation can exhibit its guarantees, and that at every horizon anyone can run it degenerates to its bidding
schedule.

## 9. Validation

*(exact computation against synthetic paired simulation)*

Five checks, reported with their numbers whether they pass or fail (`ctx_local/validate.py`):

* **V1** PL-MESP at `Q = 1` against `exploitability/dp.py`. The two are the same mechanism except that
  PL-MESP's Stage-3 EXP3 is tuned to the global `n` rather than to the realized fallback length, and except
  that the losing branch is bounded exactly here and by a closed-form union bound in `dp.py`. Both differences
  are printed rather than absorbed.
* **V2** the simulator under the proposed profile against the exact baseline bracket and the exact revenue
  bracket.
* **V3** no simulated deviation may exceed the certified upper bound. This is the check that would reveal an
  error in the backward induction or in the bracketing.
* **V4** the truncated-profile closed form against the simulator under Stage-1 shading to the floor.
* **V5** at `Q = 1` the pooled-statistics rung must coincide with PL-MESP replicate by replicate.

**V1, run on the login node at `n = 2000` and on the cluster at `n = 8000` and `n = 20000`.** At `n = 2000`,
`replicated_unique_top` at `Q = 1` gives the certified interval [181.918129, 251.682276] against `dp.py`'s
[181.918129, 215.020024], and `replicated_tied_top` gives [69.402555, 103.087720] against
[69.402555, 84.622807]. The lower ends agree exactly, because `V_F0` agrees to nine decimals
(934.121616717 against 934.121616716, and 440.436093338 against 440.436093337) and the baseline brackets are
identical to every printed digit. The upper ends differ by 36.6623 and 18.4649, and that difference is
attributed rather than absorbed: rerunning the same code with `dp.py`'s fallback bound `R_K(H)` in place of the
profile-local prefix bound reproduces `dp.py`'s `V_FUB` to within `1e-4`, so **the entire difference is the
fallback tuning**, which in PL-MESP is to the global horizon because a local EXP3 cannot know its local one.
The losing-branch treatment, which `dp.py` bounds by a closed-form union bound and `bidprofile.py` computes
exactly conditional on the realized price and the winner's identity, contributes 0.0000 of the difference, so
the two independent treatments of that branch agree.

The published profile-local constant at `Q = 1` exceeds the scalar constant of
`common/design.py::theorem_constant_top` by exactly 1.0000 at both instances, which is the `+ Q` term of
`e_mon` and is the identity stated in Section 1.

**V1 at `n = 8000`, on the cluster.** The same picture at a larger horizon: `replicated_unique_top` gives
[484.4161, 632.0041] against `dp.py`'s [484.4161, 533.5355] and `replicated_tied_top` gives
[162.7452, 236.4112] against [162.7452, 186.2058]. The lower ends agree to four decimals (`dLB` of `-0.0000`
and `+0.0000`), the baseline brackets are identical, and the upper ends differ by 98.4685 and 50.2055, again
entirely through `V_FUB` (4041.7432 against 3943.2746, and 1728.4319 against 1678.2264), which is the fallback
tuning.

**V2, V3, V4 and V5 at 400 paired replicates, `n = 8000`** (four cells: `replicated_unique_top` at `Q = 1` and
`Q = 2`, `rotating_top` at `Q = 2`, `replicated_tied_top` at `Q = 2`).

* **V3 passes everywhere, and it is the check that matters.** In every one of the four cells, over ten
  behaviours each, the largest simulated deviator **value** is below the certified upper bound on the value:
  3552.87 against 4041.74, 2291.78 against 2995.52, 1896.40 against 2445.96, and 1896.40 against 1896.40. The
  last is an equality to the digits printed, and it is not a coincidence: in that cell the certified optimum is
  to shade the Stage-1 bid to the floor and lose the auction, the value of doing so is deterministic, and the
  `bid_zero` behaviour is exactly that policy. Note that comparing a simulated **gain** with the certified
  interval is not a valid check, because it subtracts a noisy baseline from an exact bound; the value
  comparison is the one that is exact on both sides, and it is the one reported.
* **V5 passes.** At `Q = 1` the pooled rung and PL-MESP differ by at most `5e-10` over 400 replicates, which
  is double-precision agreement.
* **V4 passes where it applies.** At `replicated_unique_top` `Q = 5`, `n = 8000`, where all five profiles are
  truncated, the simulated value of Stage-1 shading to the floor is 2937.0000 with zero variance against the
  closed form `V_F0 = 2937.0000`. The `unbalanced_unique_top` `Q = 4` cell has three of four profiles
  truncated, so the closed form is not the optimum there and the check is skipped rather than reported as a
  failure; an earlier version of this suite reported that cell as a failure and was wrong to.
* **V2 is a Monte Carlo consistency check and three of its eight comparisons fall marginally outside.** Five
  of the eight are inside. The three outside are: revenue at `replicated_unique_top` `Q = 2`, whose interval
  [4781.76, 4793.45] misses the exact 4781.58 by 0.18; revenue at `replicated_tied_top` `Q = 2`, whose
  interval [5356.60, 5367.48] misses the exact 5356.45 by 0.15; and the baseline utility at
  `replicated_tied_top` `Q = 2`, whose interval [1064.23, 1155.08] misses the exact 1161.48 by 6.4, which is
  2.2 standard errors on a quantity whose law is bimodal because the focal agent wins a capacity tie about
  half the time. A 4000-replicate rerun on independent seeds puts **both** of those cells inside: revenue
  5356.353 against 5356.447 and 4781.148 against 4781.578, at 0.11 and 0.44 standard errors, and the baseline
  utilities at 1.57 and 1.04 standard errors. The 400-replicate exclusions are therefore reported as what they
  are, borderline Monte Carlo fluctuations of a nominal 95 percent interval over eight comparisons, and the
  larger reruns are the better evidence.

**The deviation search, as a second cross-check** (`ctx_local/search.py`, 200 paired replicates per grid
point; per-cell results are printed in the job logs `<scratchpad>/round2/A2/logs/sv_*.out` as each cell
finishes, and `search_*.csv` is written when a family's six cells are all done, at which point `TABLES.md`
two of its four families were complete when this report was written, and the two CSVs written by the
superseded arrays are quarantined under `results/search_superseded/`, see Section 13 item 5). The class searched is a
product grid: shade the Stage-1 target by `delta` in `{0, 0.05, 0.10, 0.125, 0.15, 0.20, 0.30, 0.50, 0.70,
1.00}`, where `1.00` is shading to the feasible floor after clipping, and in Stage 2 deliver
`tau - c / sqrt(r)` with `c` in `{0, 0.25, 0.5, 0.75, 1.0, 1.5}`. **No searched policy's value exceeded the
certified upper bound on the value at any of the 720 grid points tabulated.** The best searched gains reach 0.497 to 0.939 of the
certified lower bound in the cells where the certified optimum is not deterministic, and in the cells where it
is, the search finds it exactly: at `replicated_tied_top` `Q = 2`, `n = 8000` the best searched value is
1896.40 against `V_FUB = 1896.40`, an equality, because the certified optimum there is to shade to the floor
and lose the auction and `delta = 1.00` is that policy. Every value in this paragraph is a lower bound for the
class searched and none of it is evidence of equilibrium.

**A separate 4000-replicate agreement check** (`<scratchpad>/round2/A2/logs`, phase `analysis`, seeds disjoint
from every other block): at `replicated_tied_top` `Q = 2`, `n = 8000` the simulated revenue is 5356.353 against
the exact 5356.447, a difference of 0.11 standard errors, and at `replicated_unique_top` `Q = 2` it is
4781.148 against 4781.578, 0.44 standard errors. The simulated baseline utility is 1.57 and 1.04 standard
errors above the exact value at the two cells. An apparent three-sigma revenue discrepancy at 200 replicates
did not survive the larger run and is recorded here because it was investigated rather than dropped.

## 10. Claims supported, claims not supported, and what did not finish

**Supported, with the evidence category in parentheses.**

1. On every instance, profile count and horizon computed, the supremum unilateral gain against PL-MESP over the
   fully global-history-adaptive class `B^ctx_{i,n}` lies in a certified interval that never exceeds the
   published constant of part (A); over the cells in which every profile finishes bidding and the theorem's own
   non-top condition `4 s_n <= delta_i` holds, the certified upper bound is a stated fraction of that constant
   (exact computation, synthetic instances, deterministic arrival paths).
2. The per-profile backward induction certifies a deviation class that conditions on the deviator's entire
   history at every profile, because utilities are additive over profiles and the mechanism is profile-local
   (exact computation, with the argument in Section 2).
3. Localisation costs one bidding block per profile, and the exact computation shows that the deviator
   collects that saving once per profile, so the certified gain per round rises with the profile count and
   saturates at `M_i / K`, the value at which the mechanism gives no incentive protection at all (exact
   computation).
4. The implementable region is `Q K L_n <= n`, and over the analytic sweep it coincides exactly with the
   region in which the published bound with `e_low = 0` is below the trivial bound `2n`, in all 74 horizon-by-`K`
   cells; the monitor-activity region at a representative price agrees with both in 69 of those 74 and is one
   profile smaller in the other five (analytic evaluation of the mechanism's own parameters).
5. The non-top term `e_low` makes the published constant vacuous by orders of magnitude at modest capacity
   gaps, and the theorem's non-top branch condition is unreachable at every horizon this package can run for
   the gaps in two of its families (exact computation and analytic evaluation).
6. The ablation results of Section 7 (synthetic paired simulation; every deviation value there is a lower
   bound for the class simulated).
7. CG-MESP's own parameters clip the announced price to zero at every runnable horizon, and the horizon at
   which each of its three guarantees first says anything grows like `exp(c D)`; the numbers are printed for
   `D` up to 12 (analytic evaluation). Its lemmas and its three inequalities hold at parameters satisfying the
   structural condition (synthetic simulation).

**Not supported, and not to be written.**

* Equilibrium, in any class, as an empirical fact. The exact computations bound exploitability within a
  declared class on a fixed instance, at a fixed horizon, along a fixed arrival path; the simulated and
  searched values are lower bounds for the classes tried.
* Anything about instances, profile counts, horizons or arrival paths not computed. In particular nothing
  about random arrival paths: every exact cell conditions on a deterministic path, which hypothesis (H3)
  permits but which is one path among many.
* Any claim that PL-MESP is better than a context-blind pooled mechanism in exploitability, in revenue, or in
  joint robustness at the horizons measured. The ladder says the opposite on every cell run: pooling is less
  exploitable and loses less under joint sabotage, because it runs one bidding block instead of `Q`. What
  profile-locality buys, and what the measurements do support, is a price no winner is charged above its own
  capacity; the pooled rung violates that on `regime_switch` and convicts a compliant winner in about 27
  percent of replicates. Any sentence in the paper that presents localisation as cheaper must not be written.
* Any claim about revenue ordering on the replicated families. There revenue rises with the profile count
  because bidding rounds deliver capacity; that is an artefact of those instances, not a property of
  localisation.
* Optimality of any constant in either mechanism, and any claim that a different contextual mechanism could
  not avoid the `Q L_n` term. Remark 6.2 of `PROVER2.md` and finding F6 of `ADVERSARY.md` disagree about
  whether the manuscript's model permits sharing bidding effort across profiles; this package measures what
  sharing does to PL-MESP and settles nothing about what a different mechanism could do.
* Coalition-proofness. The joint profiles tested are specific and few.
* Anything about human behaviour, real providers, or real data. This package is entirely synthetic; the
  scalar package carries the non-synthetic evaluation and nothing here extends it.
* That CG-MESP works at any runnable horizon. It does not, and Section 8 gives the thresholds.
* That a positive finite-horizon gain contradicts an `o(n)` theorem, or that a decaying gain proves one.

**What did not finish.** The following Slurm jobs were still running when this report was written. Nothing in
the report depends on them, no number from them is estimated anywhere, and every one of them regenerates into
the report by re-running `<scratchpad>/round2/A2/slurm/finalize.sh`, which rebuilds every CSV, `TABLES.md` and
both figures from whatever results exist.

* **Exact grid at `n = 50000`** (jobs 64818664, 64818665, 64818666, and the `n = 50000` part of 64818667,
  64818668, 64818669, 64818850). The `Q = 1` cell at that horizon takes about four hours each.
* **Exact grid at `n = 200000`** (64818673, 64818674, 64818675, 64818676, 64818677, 64818678, 64818851) and at
  `n = 1000000` (64818679, 64818680, 64818834). The `Q = 3` and `Q = 4` cells at `n = 200000` were given 36
  hours and may not complete; if they do not, the `n = 200000` sweep is reported from `Q = 5` upward and is
  labelled as not carrying a `Q = 1` baseline at that horizon.
* **Ablation ladder** beyond the five cells reported (64818723 to 64818728, 64818852, 64818853, 64818854):
  the remaining profile counts at `n = 20000`, all of `n = 50000`, and all of `n = 200000`.
* **Deviation search** (64819582 to 64819585), re-submitted after the comparison correction of Section 13.
* **Validation at `n = 20000`** (64818743, 64818915).

Two consequences a reader should hold in mind. First, every range quoted in Sections 5 and 6 is over the cells
computed at the time of writing, and the cell count is stated with it; the `Checks` block at the head of
`TABLES.md` recomputes all of them, so after the remaining jobs land that block is the authority and the prose
should be re-read against it. Second, the ladder is reported at `n = 20000` only, and the horizon trend in it
is therefore not established.

**Known limitations of this package that a referee would find.**

1. No learned best-response search. The cross-check on the certified bounds is a grid search over a
   two-parameter deviation class (`ctx_local/search.py`) plus a fixed list of behaviours, not a CMA-ES search
   like the scalar package's. If a searched policy ever exceeded a certified upper bound it would indicate an
   error in the dynamic program; over everything run, none did.
2. The exact grid conditions on one deterministic arrival path per cell, namely the evenly spread one for the
   balanced families and the geometrically decreasing one for `unbalanced_unique_top`. The theorem is uniform
   over paths, so a single path is a valid instance of it, but it is one path.
3. The largest horizon at which the `Q = 1` scalar baseline was computed is smaller than the largest horizon
   at which the large-`Q` cells were computed, because the cost of the exact computation at fixed `n` falls
   like `1/Q`. Comparisons across `Q` are therefore made at a fixed horizon, never across horizons.
4. The contextual ablation ladder uses 200 paired replicates at `n <= 50000` and 100 at `n = 200000`. Its
   intervals are Student t intervals on paired differences; nothing in it is exact.
5. The `regime_switch` family is constructed to break the pooled-statistics rung. It is a designed
   counterexample, and it is labelled as one; it shows that sharing statistics can break the price, not how
   often that happens on instances nobody designed.

## 11. Proposed figures

Generated by `scratch/experiments/round2/figures/make_figures_a2.py`, vector PDF, no embedded titles, the same
Okabe-Ito subset and rcParams as `figures/make_figures.py`, every series carrying a marker and a line style as
well as a legend entry, no panel with two y-axes. Written to `<scratchpad>/round2/A2/figures/`.

Main figure, `main_contextual.pdf`, four panels:

* (a) certified exploitability per round against the profile count `Q`, one band per horizon, with the
  published constant per round as a dashed line and a cross on cells where some profile never finishes
  bidding.
* (b) revenue per round against `Q` with the second-capacity benchmark, and the share of the horizon spent
  bidding, `Q K L_n / n`, on the same scale.
* (c) the contextual ablation ladder: best tested unilateral deviation per round by rung, with the platform's
  headroom against the honest benchmark under the worst joint profile printed beside each bar.
* (d) the horizon at which each CG-MESP guarantee first says anything, against the dimension, with the
  manuscript's public contextual error for comparison and the runnable horizons shaded.

The cell shown in panel (c) is chosen on the command line (`--ladder-family`, `--ladder-n`, `--ladder-Q`).
The version written at the time of this report shows `replicated_unique_top` at `n = 20000`, `Q = 1`, which is
the scalar mechanism and therefore the cell that is comparable with the scalar package. When the `n = 200000`
ladder lands, that is the cell to use, because it is the one in which the monitored phase is most of the
horizon.

Supplementary figure, `supp_contextual_regime.pdf`, three panels: the implementable region in `(n, Q)`; the
certified interval against the horizon at fixed `Q`; and the smallest horizon at which the theorem's non-top
branch condition holds, against the capacity gap.

## 12. Integration guidance

What belongs in the eight pages, in decreasing order of what a referee will look for:

1. **Panel (a) and the one sentence that goes with it.** The certified interval against the profile count, with
   the theorem's own constant on the same axes. This is the headline's evidence, it is exact rather than
   sampled, and it covers the whole declared deviation class.
2. **The implementable region.** One sentence and a number: PL-MESP requires `Q K L_n <= n`, and at the
   horizons in the experiments that is `Q` at most 3 at `n = 10^4` and at most 6 at `n = 10^5` for `K = 3`.
   Without it a reader will assume the profile count is free.
3. **Panel (d) and the continuous thresholds.** A referee will compute the horizon at which the continuous
   bound says anything, so the paper should print it. The single most useful number is that `D = 2`, the
   smallest case with at least two agents and scalar contexts, needs `n` of order `10^{9.8}` for all three
   guarantees, against `10^{3.7}` for the manuscript's public contextual error.
4. **The pooled-statistics rung of the ladder, stated the way it came out.** One row of a table, and it does
   not say what one would want it to say: pooling is less exploitable than PL-MESP at every horizon measured,
   because it runs one bidding block instead of `Q`. What it buys is a price no winner is charged above its own
   capacity, and the measurement of that is the switch rate on a compliant winner, 0.27 against 0.00. A
   referee will ask why the construction pays `Q` bidding blocks, and this is the honest answer to give.

What belongs in the appendix or the supplement: the full exact grid and its per-profile decomposition; the
regime and non-top threshold tables; the full ablation ladder; the deviation search; the CG-MESP structural
regime and its oscillation sweep; and the validation suite.

What should not be claimed anywhere: see Section 10.

## 13. Corrections made after seeing data, and why each is an adjudication rather than a moved goalpost

Four checks were changed after they had produced numbers. Each is recorded because the record is what makes
the change reviewable, and the first two would have put a false statement in the report.

1. **Comparing a simulated gain with the certified gain interval is not a valid check, and it produced three
   spurious exceedances.** The certified interval on the gain is `V_FUB - base_LB`, with both ends exact. A
   simulated gain is a searched value minus a **simulated** baseline. At the cells where the certified optimum
   is deterministic, which is every cell where the optimum is to shade the bid and lose the auction, the
   searched value has zero variance and all the noise sits in the baseline, so the simulated gain exceeds the
   certified upper bound whenever the baseline happens to come in low. Three cells of the first deviation
   search reported exactly that, by 0.27, 0.59 and 1.36 on totals of about 2000, that is by about a tenth of a
   percent. The check now compares the simulated **value** with `V_FUB`, which is exact on both sides, and the
   search was re-run. Nothing about the mechanism changed; a mis-specified comparison did.
2. **The truncated-profile check applies only when every profile is truncated.** The closed form of Section 5
   item 2 is the optimum only when the whole horizon is Stage 1. The first version of the check ran it on a
   cell with three of four profiles truncated and reported a failure; the closed form there is a lower bound
   on the optimum, as it must be, and the cell is now skipped with the reason printed.
3. **The consistency check between a simulated mean and an exact bracket compares intervals, not points.** The
   first version asked whether the simulated mean lay inside the exact bracket, which a mean with sampling
   error need not do; it now asks whether the 95 percent interval of the simulated mean meets the bracket.
4. **The claim that the three thresholds on the profile count coincide was wrong as first written.** The first
   draft said they coincide with a single exception. Recomputing over the whole sweep shows that the
   completion and below-trivial-bound thresholds coincide in all 74 horizon-by-`K` cells with no exception,
   while the monitor-activity threshold differs in five of them. The sentence now states both counts.

5. **Two superseded search arrays were not actually cancelled, completed, and wrote output that had to be
   quarantined.** The cancellation used repeated `-n NAME` options in one `scancel` call. Slurm does not
   accumulate repeated `-n`: the last one wins, so only the third array was cancelled and the first two ran to
   completion and wrote `search_*.csv` files in the narrow-grid, gain-comparison form. Those two files are
   moved to `<scratchpad>/round2/A2/results/search_superseded/` rather than deleted, so the record survives,
   and the aggregator reads only `results/search/`. The remaining superseded jobs were then cancelled by job
   id. This is recorded because an output file that looks current and is not is exactly the failure mode that
   puts a wrong number in a paper.

Nothing in the acceptance of a result was relaxed after seeing it. The three cells in item 1 are still
reported, as the borderline artefacts of a mis-specified comparison that they are, and the corrected
comparison is stated alongside.
