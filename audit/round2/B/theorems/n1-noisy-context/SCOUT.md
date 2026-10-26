# N1 scout: PL-MESP under context-label noise

STATUS: DONE (2026-09-29). Simulation: Slurm 65033003, 30 tasks, cpu-preempt --requeue, all COMPLETED.

Scope: feasibility study with a go/no-go, not a proof. No canonical file, .tex source or existing
script was modified. Sources read: c2-local-mesp PROVER1 Sections 0-5 (model, mechanism, Theorem 1,
Lemmas 3-5), PROVER2 Section 4 (hypotheses, theorem, Corollary 4.3), f1-continuous-private
PROVER2 Sections 0-2 and 20, A5/C_extras/REPORT.md item 5, A4/scripts/extras_c.py (item-5 driver),
mechanisms.py (MechanismRun, ProfileStrategy), arrival_order.py (reorder, PooledPrimary).
Scripts and outputs of this scout: `n1-noisy-context/scripts/`, `n1-noisy-context/out/`.

Notation. True task type (profile) `X_t` in a finite set `A` (the Q7 types). Label `B_t` in a
finite set `Lab` (classifier output; in item 5 `Lab = A`). Confusion `C(a, b) = P(B = b | X = a)`,
type masses `p(a)`, label masses `P_B(b)`, posterior `pi_b(a) = P(X = a | B = b)`, posterior error
`e_b = 1 - pi_b(b)`, overall error `eps = P(B != X) = sum_b P_B(b) e_b`. Posterior-mixture
primitives `Mbar_j(b) = sum_a pi_b(a) M_j(a)`, `mubar_j(b)` likewise, and the barred versions of
`T, M_(2), V_i, delta_i, b(.)` of c2 computed from them.

## 0. Diagnosis of the item-5 failure (confirmed from the code)

What the item-5 run does (`extras_c.noisy_instance`, `run_arm` with `used = ninst`): rows are
pairs (true, label), quality follows the true type, and `MechanismRun` keys every local instance on
the LABEL. So the mechanism is PL-MESP on the label partition, and nothing in it is per true type:

1. Stage 1 at label `b`: bidder `j` delivers `M_j(X_t)` on queries whose true type varies, so its
   bid estimates the posterior mixture, `beta_j(b) ~ Mbar_j(b)`.
2. The price is `tau_b = beta_(2)(b) - s ~ Mbar_(2)(b) - s`: a label-level (mixture) price.
3. The winner plays `ProfileStrategy "proposed"`, i.e. the paper's S* applied POINTWISE at the true
   type: `min(tau_b, M_W(X_t))`. Its conditional mean per primary round is
   `tau_b - sh_b`, `sh_b := sum_a pi_b(a) (tau_b - M_W(a))_+ > 0` whenever the winner is below the
   price on any type with posterior mass at `b`.
4. The anytime monitor sees a drift of `-sh_b` per round and fires once `r sh_b > b(r)`, i.e. after
   about `ell / (2 sh_b^2)` primary rounds (`ell = log(2n^4) ~ 60` at `n = 3e6`). With
   `sh_b ~ 0.01` that is about `3e5` rounds, so convictions appear only at large `eps` and large `n`,
   exactly the item-5 pattern (0 / 18 / 58 %). `scripts/analytic.py` gives `sh_b` in closed form:
   `max_b sh_b` is 0.006 to 0.039 at `eps = 0.05` and 0.011 to 0.075 at `eps = 0.2` across the 10
   subsets (price taken as `Mbar_(2)` without the `-s`).
5. `compliant_convictions` in `MechanismRun.run` counts `m >= min(tau, M_i(true))`, the same
   pointwise notion, so the headline metric inherits the mismatch.

So the brief's reading is right in effect but the precise cause is sharper: **the monitor's
reference is the label-level price, which the winner CAN meet on average (its mixture capability
exceeds the price on the good event), but the pointwise S* rule does not try to.** It is a mismatch
between a label-level price and a type-level compliance rule, not a defect of the monitor. PROVER2
Corollary 4.3 of c2 already names this as the place where cells with non-constant primitives break
("the monitor may charge an agent a price above its local capacity at some contexts inside the
cell"). Note that the paper already uses the label-level (pooled) notion of compliance for its Cao
baseline: `arrival_order.PooledPrimary` scales delivery so that the POOLED mean meets the price.

Consequence: the natural fix is not a new monitor but the right compliance notion plus the right
hypothesis on the noise. That is candidate D below, which I rank first.

## 1. Candidate D (added; ranked first): PL-MESP keyed on the label, label-level S*

### 1.1 Mechanism
PL-MESP of c2 unchanged, keyed on the label `B_t` (one local instance per label). The platform
needs no knowledge of `C`, `p`, `pi` or `eps`. Messages as (M6) with "profile" read as "label".
Optional message (only for variant D-known): the posterior `pi_b` of the current label.

Model change: the selected agent observes the true type `X_t` (it reads the prompt) and the label
(through the local phase/price message); the platform observes only `B_t`. Target
`m_{i,t} in [0, M_i(X_t)]`, reward `1{U <= m_{i,t}}`, linear cost `m - mu_i(X_t)`; honest agents
`m >= mu_i(X_t)` pointwise.

Proposed profile `S*_N`. Stage 1 and fallback: deliver `M_j(X_t)`. Primary winner at label `b`:
water-fill, `m(a) = clip(c_b, lo_j(a), M_j(a))`, `lo_j = mu_j` if honest else 0, with `c_b` chosen so
that `sum_a pi_b(a) m(a) = max{ mubar_j(b) 1{honest}, min{ tau_b, Mbar_j(b) } }`. (Any allocation
with that label mean gives the same utility under linear cost; water-filling is chosen because it
dominates the pointwise S* at every type, so it is also "compliant" in the item-5 metric.)

Variant D-learn (needs no knowledge by anyone): `pi_b` replaced by the empirical law `pihat_b` of
the true types of the agent's OWN `L` Stage-1 pulls at `b`, and the level raised by
`gamma = sqrt((|A| log 2 + 4 log n) / (2L))` (TV concentration: `P(TV(pihat_b, pi_b) > gamma) <=
2^{|A|} e^{-2 L gamma^2} = n^{-4}`). This uses only the agent's own history, within the author's
observation rule of 28 Sep.

### 1.2 Hypothesis on the noise, in conditional form
Enumerate ALL primitives in one fixed order: the priorities, the agents' private coin arrays, then
round by round the true type `X_t`, the round-`t` mechanism coin, the round-`t` seed (or the seed
array `U_{b,j,k}` in c2-PROVER1 indexing).

**(N)** The label sequence `B = (B_1..B_n)` is exogenous, and conditionally on `sigma(B)` and on
every primitive enumerated before it, each primitive has its specified law: `X_t` has law
`pi_{B_t}`, each seed is Uniform[0,1], each mechanism coin and priority has its specified law. The
agents' private coins may have any law given `B` (an agent may know all future labels) but are
drawn before, hence are "before", every `X_t` and seed.

Because the enumeration is fixed, (N) is equivalent to: given `B`, all primitives are mutually
independent with the stated marginals. That product form is what the c2 phantom-continuation
argument (PROVER1 Lemma 5, which puts FUTURE primitives of other profiles into `H_r`) actually
uses, so it is the form to state. It is one quantifier over a complete enumeration, not a list of
independence clauses, so it cannot silently omit a family (the f1 PROVER2 Section 20 lesson).

Sufficient condition: the pairs `(X_t, B_t)` are i.i.d. from `p(a) C(a, b)` and independent of all
seeds and coins. (Then, given `B`, the `X_t` are independent with `X_t ~ pi_{B_t}`.)
(N) FAILS when the true-type order is bursty or drifting even with an i.i.d. classifier, and when
the classifier's error depends on time or on anything the providers do. This is a real loss
relative to c2, whose theorem holds for arbitrary exogenous arrival orders; Section 5 shows the
loss is unavoidable.

Deviation class `B^N_{i,n}`: `m_{i,t}` measurable in `n`, the whole label sequence `B`, the current
`X_t`, its own history (including the true types of its own past selections), its messages and
its private coins. NOT future true types (that would break (N) relative to the agent's field).
This contains the c2 class `B^ctx` (with profile = label) and is contained in `B^ctx+` except for
the future-`X` clause.

### 1.3 Theorem to claim (Theorem N)
Assume (N), c2's (H1), (H2), (H6) with profiles read as labels, `Q_B := |Lab|`, linear cost. Then:

- (A) Additive behavioural equilibrium: for every `i` and every `S' in B^N_{i,n}`,
  `u_i(S', S*_N,-i) - u_i(S*_N)` is bounded by c2 Theorem 1(i) (PROVER1 numbering) with
  `Q -> Q_B` and `delta_i(z) -> deltabar_i(b)` (gaps of the MIXTURE capabilities). For D-learn add
  `n gamma + O(n^{-2})`, which is of the same order as c2's `2 n s` term (`sqrt(|A|)` factor).
- (B) Revenue: `P(n; S*_N) >= E sum_t Mbar_(2)(B_t) - (c2 error terms with Q_B)`, and
  `E Mbar_(2)(B) >= E M_(2)(X) - eps (omega + omega_2) >= E M_(2)(X) - 2 eps`, where `omega` bounds
  the range of each `M_j(.)` over types and `omega_2` the range of `M_(2)(.)`. Proof of the
  `eps` part: `|Mbar_j(b) - M_j(b)| <= e_b omega`, the second order statistic is 1-Lipschitz in the
  sup norm, `sum_b P_B(b) e_b = eps`, and `TV(P_B, p) <= P(B != X) = eps`. Tight up to the factor
  2: types `a, c`, three agents `M(a) = (1, 1, 0)`, `M(c) = (0, 1, 1)`, symmetric noise `e`: every
  true-type second capacity is 1, every label second capacity is `1 - e`. Mixing can also RAISE
  the benchmark (it does on 3 of the 10 item-5 subsets). Measured on the item-5 subsets
  (`analytic.py`): loss `E M_(2)(X) - E Mbar_(2)(B)` at most 0.015 at `eps = 0.2` (k4_q90), i.e.
  about `0.075 eps`, and negative on k3_q10 and k4_q10.
- (C) Honest benchmark: `P(n; S) >= E sum_t bbar(B_t) - (c2 errors)` for every feasible profile;
  with ONE honest agent `E bbar(B) = E mu_h(X)` exactly (tower property), so there is no `eps` loss
  at all; with several honest agents the loss is at most `2 eps` by the same Lipschitz argument.
- Honest (compliant) conviction: under `S*_N` the winner's predictable mean is `>= tau_b` at every
  primary round, so by the analogue of c2 Lemma 5 (5.3) each label's monitor fires with probability
  at most `(2n^3)^{-1}`. For D-learn the same holds on the TV event, total `<= Q_B (n^{-3} + n^{-4})`.
- (D) Rates unchanged: `O(n^{2/3} (log n)^{1/3})` for fixed `K, Q_B`, sub-linear iff
  `Q_B = o(n^{1/3} (log n)^{-1/3})` (the label set, not the type set, is what counts).

### 1.4 Proof sketch and the hard step
Reduction lemma R: run every c2 lemma on the space carrying `(B, X, U, coins)`, CONDITIONING ON
`B` ONLY (c2 conditions on the whole arrival path; here `B` plays the arrival path and `X` is
treated as part of the per-round randomness). Every c2 step uses one of three properties, each of
which survives:

1. Predictable conditional means. With the field `H` excluding the future true types AND seeds
   at the label under study (PROVER1 Lemma 5's deterministic excluded index set extended by
   `{X_{t_{b,r'}} : r' >= r}`, which is `B`-measurable), `E[Y_r | H_{r-1}] = sum_a pi_b(a) m_r(a)
   =: mbar_r`, with `m_r(.)` an `H_{r-1}`-measurable response function, `mbar_r <= Mbar_W(b)`, and
   increments in an interval of length 1. Lemma 4b (Azuma), Lemma 5 (monitor), bidding
   concentration and the utility identities (`E[1 + mu_i(X_t) - m_t | H] = 1 + mubar_i - mbar_t`)
   go through with barred quantities.
2. Pathwise seed monotonicity across the coupled executions. Both executions share `(B, X, U)`;
   Stage-1 schedules are `B`-measurable (L4d), so `1{U <= m'(X_t)} <= 1{U <= M_i(X_t)}` gives
   (L4a) pathwise, and non-deviators' Stage-1 rewards are identical pathwise (L3a, L4b, L4c).
3. Locality (Lemma 3 / Lemma L): `S*_N` at label `b` is a function of
   `(b, phase, tau_b, j, X_t)` (D-learn: plus `j`'s own Stage-1 types at `b`); still local.

Carry over unchanged (up to barring): PROVER1 Lemmas 3, 4, 4b, 5, 6, 7, 8 and Proposition 2;
PROVER2 Lemmas L, M, F, B; the EXP3 fallback lemmas verbatim (adversarial rewards). What must be
rewritten: PROVER1 Section 4.2 (conditioning on arrivals), because `X` is no longer conditioned on
and so capacities at a visit are random; and every place where a pointwise capacity at a visit is
used as a pathwise bound (e.g. "on the good event the S* winner delivers exactly `tau`" becomes a
statement about `mbar`).

**Hard step.** The part (A) coupling with `X` random. The deviator may condition on the true types
of its past selections, which are correlated with its past rewards and are invisible to the
mechanism; the adversary's F4 (the joint field `D_z`) and F5 (phantom continuation) findings on
c2 must be re-checked with `X` added to the primitives, and the "indicator times conditional
expectation" bookkeeping (f1 PROVER2 Section 20 item 3) recurs at every place the good event at a
label multiplies a barred mean. I see no obstruction, but this is where an adversary will look.

### 1.5 Assessment
Strongest candidate by a wide margin: no mechanism change, no knowledge of the noise, zero false
convictions, revenue benchmark within `2 eps` (measured `<= 0.075 eps`), rates unchanged, and the
proofs are a reduction to c2 which already has two proofs and an adversarial pass. Its cost is
honest and must be stated: (N) replaces c2's arbitrary-order hypothesis, and the equilibrium
profile is label-level, not type-level. Both costs are shown necessary in Section 5.

## 2. Candidate A: noise-aware monitoring tolerance

### 2.1 Mechanism
PL-MESP on labels with the monitor boundary widened: switch at the first `r` with
`Z_r < r (tau_b - kappa_b) - b(r)`; announced price still `tau_b`. Safe choice for the
POINTWISE S*: `kappa_b >= sh_b = sum_a pi_b(a) (tau_b - M_W(a))_+`; a mechanism-computable choice
is `kappa_b = e_b tau_b` (needs `C` and `p`, or an upper bound on the posterior error `e_b`).

### 2.2 Theorem that could be claimed
Under (N) and known `e_b` (or an upper bound): (a) the pointwise S* winner is convicted with
probability `<= (2n^3)^{-1}` per label; (b) the equilibrium is the label-level profile at the
effective price `tau_b - kappa_b` (a strategic winner shades to the widened boundary), with c2's
error terms; (c) revenue at that equilibrium `>= E sum_t (Mbar_(2)(B_t) - kappa_{B_t}) - errors`,
i.e. an extra cost `E[e_B tau_B] <= eps` on top of D's.

### 2.3 Assessment
Dominated by D: it needs the confusion matrix, still needs (N) (the tolerance is an average over
the posterior; under arbitrary orders no `eps`-scale tolerance works, Section 5), and pays up to
`eps` more revenue. Worse, the posterior error `e_b` of RARE labels is large even at small `eps`
(uniform noise at `eps = 0.2` makes the MT-Bench label about 95% mislabelled, since MT-Bench has
0.2% of the mass), so `kappa_b` switches the monitor almost off exactly where labels are
unreliable. Its only merit is protecting non-adaptive pointwise-compliant providers that cannot
compute a label average. Carry-over: identical to D (it is D with the price shaded by `kappa_b`).
Useful as a remark, not as the theorem.

## 3. Candidate B: monitoring against soft posteriors

- B-exact (as in the brief): reference `sum_a q_t(a) tau_a` with per-type prices. Per-type prices
  must be elicited from label-level data by deconvolution through a KNOWN, invertible, calibrated
  confusion matrix (error amplified by `||Pi^{-1}||`), and routing is still label measurable, so
  one agent serves label `b` and its obligation at `b` is a label average anyway. It reduces to D
  with a worse price estimate. Not worth proving.
- B-bins: label := (argmax class, confidence bin). This is D with a finer label set: benchmark
  `E Mbar_(2)` rises towards `E M_(2)(X)` as bins sharpen, cost `Q_B L`. Free corollary of D; worth
  one sentence (the platform should key on the richest finite signal it can afford, subject to
  `Q_B = o(n^{1/3})`).
- B-continuous: context := posterior vector `q_t` in the simplex, run CG-MESP (f1) on it. If the
  classifier is calibrated, `E[M_j(X) | q] = sum_a q(a) M_j(a)` is 1-Lipschitz in L1, so f1's
  Lipschitz hypothesis holds in dimension `d = |A| - 1 = 6`, where f1's grid rate is poor, and f1
  needs i.i.d. arrivals in any case. Not competitive for a 2027 paper.

## 4. Candidate C: coarser merged partition / decoupled routing and monitoring

- C-merge: key PL-MESP on a partition of labels into groups with little cross-group confusion. This
  is D with `Lab` replaced by groups: smaller `Q_B` and smaller cross-group posterior error, lower
  benchmark. Under (N), D already has zero false convictions, so merging buys nothing for
  convictions; it helps only under mild non-stationarity (Section 5.3: the drift allowance `delta`
  is smaller for groups closed under confusion).
- C-decouple: route on fine labels, price/monitor on coarse groups. Breaks locality unless the same
  agent wins every label in the group (pooled obligations are otherwise not attributable), and then
  it is PL-MESP on the coarse partition. No gain over C-merge.
Assessment: subsumed by D as the "choice of label set" trade-off; one sentence in the paper.

## 5. Impossibility: order robustness is lost under label noise, necessarily

### 5.1 Statement (Proposition I, to be proved)
Model: exogenous true-type path chosen arbitrarily (c2's arrival hypothesis), classifier noise
i.i.d. given the true type, `B_t ~ C(X_t, .)`, the mechanism observes only labels, rewards and its
own coins (any label-measurable mechanism, not only PL-MESP). For every `eps in (0, 1/2]` there
are an instance (`K = 3`, three types, two labels, per-type error at most `eps`) and two exogenous
paths `P1`, `P2` such that the joint law of (labels, allocations, rewards) is IDENTICAL under

- `P1` with the winner `W` cooperative: it delivers `min{1/2, M_W(X_t)}`, i.e. the price level
  wherever it can and its full capability where it cannot; and
- `P2` with `W` shading: it delivers 1/2 in the first half and 0 on second-half label-`a` queries,
  although it could deliver 1 there.

Corollary. Let `alpha` be the expected fraction of the (about `eps n / 2`) second-half label-`a`
rounds that the mechanism withholds from the cooperative `W` on `P1`. Then on `P2` the shading
strategy beats "deliver 1/2 throughout" by at least `(1/2 - alpha) eps n / 2 - O(sqrt n)` in
utility (`mu_W = 0`). So either the mechanism punishes a cooperative winner (withholds a constant
fraction of its rounds; for PL-MESP: convicts it) or it leaves a shading gain of order `eps n`
(`>= eps n / 8 - O(sqrt n)` when `alpha <= 1/4`).

### 5.2 Construction (sketch)
Types `a, c, d`, labels `a, c`. `C(a, a) = 1`; `C(c, a) = eps`, `C(c, c) = 1 - eps`; `C(d, c) = 1`.
`W`: `M_W(a) = 1`, `M_W(c) = 0`, `mu_W = 0`; agents 2, 3: `M_j(a) = M_j(c) = 1/2`; `M_j(d) := M_j(c)`
for all `j`. `P1`: first half all `a`, second half all `c`. `P2`: first half all `a`, second half
i.i.d. `a` with probability `eps` and `d` otherwise. The label sequences have the same law
(second half: label `a` w.p. `eps`, else `c`); the label-`c` rounds see identical primitives; at
label `a` the first-half rounds are identical and every second-half reward of `W` is 0 in both
(in `P1` because its capability there is 0). Since the mechanism's allocation at each round is a
function of past labels, rewards and its coins, induction over rounds gives equality of the joint
laws up to the first round at which `W` is not allocated a label-`a` round; the corollary only
needs the law of the set of rounds allocated to `W`, and the per-round utility accounting (shading
earns 1 per allocated second-half label-`a` round, "deliver 1/2" earns at most 1/2 on at most
`eps n / 2 + O(sqrt n)` rounds) must be done with care for what happens after a withdrawal
(non-winners behave differently on `c` versus `a` queries; set their strategies type-blind to
remove this).

### 5.3 What it means, and the positive counterpart
- For `eps = 0` the construction collapses (label `a` never sees type `c`), consistent with c2's
  order-free theorem. The failure is created by noise interacting with arrival order, not by the
  classifier alone, and it holds for every label-measurable mechanism, not only PL-MESP.
- Therefore (N) (or some stationarity of the posterior) is NECESSARY for "no false convictions of
  cooperative winners + sub-linear shading gain", and D is optimal in the sense that it needs
  nothing more than (N).
- Positive counterpart to check (N(delta)): if the conditional law of `X_t` given `B` and the past
  is within TV `delta` of `pi_{B_t}` (not necessarily equal), D with the price shaded by an extra
  `2 delta` keeps (A)-(C) with an extra `2 delta n`. Matches the proposition's order `eps n` when
  `delta ~ eps` (a burst can move the posterior by up to `e_b`).
- A second, easier two-point remark (Remark I'): with stationary noise, pointwise (type-level)
  compliance is unidentifiable from labels: an agent that cannot serve type `c` and delivers 0 on
  it and an agent that can and shades to 0 there produce the same observation law, so no
  label-measurable mechanism can enforce type-level delivery below resolution `e_b tau_b` without
  convicting type-level-compliant agents. This justifies the label-level S* but is too simple to
  be a headline.
Publishability: Proposition I is a clean, short, mechanism-independent statement with an explicit
`eps n` rate; it is a good companion to Theorem N, not a stand-alone paper.

## 6. Simulation (candidates D and A on the item-5 setup)

Driver `scripts/noisy_label.py` (copied from `A4/scripts/extras_c.py` item 5; imports
`mechanisms.py`, `extras_c.noisy_instance/confusion`, `arrival_order.reorder` unchanged). Same
instance, masses, label-noise draw (seed `99991 + s`), mechanism seeds and `n = 3e6` as item 5;
uniform noise; 10 v2 subsets x seeds 0-5 = 60 runs per cell. Tasks `scripts/tasks.txt`, batch
script `scripts/n1.sbatch`, per-run rows `out/n1_all_runs.csv`, summary `out/n1_summary.csv`,
printer `scripts/aggregate.py`. Compute: about 10.3 CPU-hours (more than the few I budgeted; the
cluster nodes ran about 2.5x slower than the login-node timing). Revenue = per-round mean.
"conv." = fraction of runs with any conviction; every conviction below is of a winner that is
compliant under its own rule (fired = compliant_convictions > 0 in every cell).

| order | eps | arm | conv. | revenue | benchmark E Mbar_(2)(B) |
|:--|:--|:--|--:|--:|--:|
| iid | 0.1 | pointwise S* (item-5 baseline) | 0.20 | 0.6558 | 0.6852 |
| iid | 0.1 | **D: label-level S*, known pi_b** | **0.00** | 0.6564 | 0.6852 |
| iid | 0.1 | D-learn: own Stage-1 pihat_b, margin gamma | 0.00 | 0.6710 | 0.6852 |
| iid | 0.1 | A: widened monitor, pointwise S* | 0.00 | 0.6553 | 0.6852 |
| iid | 0.1 | A: strategic best response (shade to tau - kappa) | 0.00 | 0.6408 | 0.6852 |
| iid | 0.2 | pointwise S* (item-5 baseline) | 0.58 | 0.6556 | 0.6820 |
| iid | 0.2 | **D: label-level S*, known pi_b** | **0.00** | 0.6533 | 0.6820 |
| iid | 0.2 | D-learn | 0.00 | 0.6671 | 0.6820 |
| iid | 0.2 | A: widened monitor, pointwise S* | 0.00 | 0.6510 | 0.6820 |
| iid | 0.2 | A: strategic best response | 0.00 | 0.6211 | 0.6820 |
| bursty | 0.2 | pointwise S* | 0.60 | 0.6570 | 0.6820 |
| bursty | 0.2 | D: label-level S* | 0.22 | 0.6551 | 0.6820 |

Reference: noise-free PL-MESP S* 0.659 (item 5, 20 seeds), true-type benchmark E M_(2)(X) 0.6887.

Readings.
1. The baseline reproduces item 5 (20% and 58% here on 6 seeds, against 18% and 58% on 20).
2. **D removes every false conviction at eps = 0.1 and 0.2 under i.i.d. arrivals (0/120 runs), with
   no change to the mechanism.** Its revenue, 0.656 and 0.653, is within 0.003 and 0.006 of the
   noise-free 0.659, which matches the benchmark drop (0.0035, 0.0067). It is 0.002 BELOW the
   pointwise arm at eps = 0.2, because in the pointwise arm the conviction sends traffic to the
   EXP3 fallback, where S* delivers capability, which is above the second price; that revenue is
   bought with false convictions and is not a guarantee.
3. D-learn (no knowledge of the noise by anyone) also has 0 convictions and higher revenue
   (0.671, 0.667) because the margin `gamma ~ 0.025` is delivered on top of the price; the provider
   pays that, which is the extra `n gamma` term in the equilibrium bound.
4. A removes the convictions of pointwise agents but its equilibrium costs 0.016 (eps 0.1) and
   0.032 (eps 0.2) of revenue relative to D, the predicted `E[e_B tau_B]`; the monitor is nearly off
   on rare labels.
5. Bursty true-type order breaks (N) and D then convicts in 22% of runs (pointwise 60%), with 4 of
   10 subsets at 33-50%. This is the empirical face of Proposition I: under label noise order
   robustness is lost, for D too. Noise-free PL-MESP is order invariant (item 5, item 7), so this
   is a genuine new limitation to state, not an artefact.
6. Not run: the measured confusion matrix (`experiments/data/A5/classifier_confusion.csv` exists
   now, but it is on the merged-5 type space, has an empty commonsense row and about 230 hand-checked
   prompts, so it cannot be mapped to Q7 without a modelling choice), the `real` order, and
   `eps = 0.05` (item 5 already shows 0 convictions there).

## 7. Ranking, recommendation, feasibility

Ranking.
1. **D (PL-MESP keyed on the label, label-level S*) + Theorem N**, with D-learn as the implementable
   profile. No mechanism change, no knowledge of the noise, zero false convictions under (N),
   benchmark `E Mbar_(2)(B) >= E M_(2)(X) - 2 eps` (tight up to 2; measured loss `<= 0.075 eps`),
   rates unchanged, honest benchmark unchanged with one honest agent.
2. **Proposition I (impossibility)**: without posterior stationarity, every label-measurable
   mechanism either punishes a cooperative winner or leaves an `eps n / 8` shading gain. Short,
   mechanism-independent, and it explains the bursty numbers. Companion result, not stand-alone.
3. A (noise-aware tolerance): correct but dominated (needs C, still needs (N), costs up to `eps`
   more); one remark.
4. C (merged partition) and B-bins: corollaries of D as a choice of label set; one sentence each.
5. B-exact, B-continuous, C-decouple: no gain over D or poor rates; do not pursue.

Recommendation: **GO** for Theorem N (reduction of c2 Theorem 1 to posterior-mixture primitives
under (N)) plus Proposition I, with A as a remark and the bursty result stated as a limitation.
Against the paper's current text the change is: the item-5 finding becomes "label noise does not
break PL-MESP; it changes compliance to a label average and replaces arbitrary order by posterior
stationarity, which is necessary".

Feasibility by ~15 Oct (two independent proofs + adversarial pass). Theorem N is a reduction with
no new probabilistic idea; Proposition I is a two-point construction. My estimate: two provers
3 to 4 days each in parallel (start 4 Oct, done about 8 Oct), adversary 2 to 3 days (about 11 Oct),
repairs by 13 to 15 Oct. Probability of finishing on time about 70%; the main schedule risk is
that the reduction touches c2's Section 4.2 conditioning convention, which every lemma inherits,
so the provers must rewrite the probability-space section and re-audit each lemma rather than
substitute symbols, and the adversary must re-examine c2's own findings F3 to F5 in the new space.

Weakest step: the part (A) coupling with the true types random rather than conditioned on (the
deviator sees past true types that the mechanism does not, and they enter the phantom-continuation
field of Lemma 5), together with stating (N) in the product/conditional form over a complete
enumeration of primitives, the error pattern this project has repeated three times. Second: the
utility accounting after a withdrawal in Proposition I.
