# ADVERSARY_OPEN -- DONE

Status: DONE (29 Sep 2026). All four items attacked. One P2 found, with a P1 witness under the
audit's own formalisation (item 1). Items 2, 3 and 4: P3 only. No existing file was edited.
Scripts and outputs are in `adv_open/` (standard library only, deterministic seeds).

Scope: the four statements that CHECK.md Section 11 lists as uncovered by any audit:
Proposition `prop:ctx-continuum-exact`(i) (sections/app_contextual_private.tex 1191-1391), the appendix
preamble (lines 1-57), the hypotheses paragraph (750-822), the main-text (A2) note (sections/sec2_model.tex
line 71), `lem:cost-convert` (sections/appendix_private.tex 14-27) with every Lambda in (i), and FINAL.md
Lemma 9.

## Verdict table

| item | verdict | severity |
|:-|:-|:-|
| 1. (i) over `B^ctx` "under exogeneity and (A3) alone" | **fails under the distributional reading of exogeneity** (FINAL.md's (X)): witness W1, gain `0.887 n` against a bound of `0.388 n` at `n = 4*10^6`. It holds under a *structural* reading (the path is a fixed function of primitives shared by all profiles), and the proof on file supports that reading. The manuscript's wording does not say which reading it means | **P2** (hypothesis undefined; P1 under (X)+(A3)) |
| 2. the two remainder constants | confirmed: both steps treat a random count, or a random index set, as fixed. With the counts corrected the remainder is `4J_n n^-4 + 6J_n n^-3/K`, and that is at most the displayed `4n^-3 + 4K^-1 n^-2` whenever `J_n <= 2n/3`, which holds at every horizon where the bound is below `n` | P3 (the text changes, the display stands) |
| 3. convex costs, `lem:cost-convert`, the Lambda factors | the lemma is correct line by line and tight; every Lambda in (i) is placed correctly; no break with a convex phi attaining (N) with equality | P3 at most (one measurability remark) |
| 4. FINAL.md Lemma 9 | sound under (X)+(A4f-P). W1 shows its use of (f1) given the path is load bearing even for `B^ctx`. One P3 on what "the law in the model" means for `B^ctx+` | P3 |

## 1. Part (i) over `B^ctx` under exogeneity and (A3) alone

### 1.1 Witness W1 (reward XOR priority routing)

`K = 2`, `d = 1`, linear cost (`Lambda = 1`), constant primitives (Lipschitz constant 0, so
(ctx-horizon) holds for every `n`). Agent 1 is strategic with `mu_1 = M_1 = 1`. Agent 2 is honest with
`mu_2 = M_2 = 1`. The cubes are `Cmid` (containing `1/2`), `C0 = [0,h)` and `C1 = [1-h,1)`, and `L = L_n`.

Path:
* round 1: `x_1 = 1/2`. This is the first visit to `Cmid`, hence agent 1's Stage-1 pull. `Cmid` is never
  visited again and never awards.
* rounds `2 .. 2L+1`: `x = h/2`. This is the whole of Stage 1 at `C0`, and `Pi_C0` is drawn at round 2.
* rounds `2L+2 .. 4L+1`: `x = 1-h/2`. This is the whole of Stage 1 at `C1`, and `Pi_C1` is drawn.
* rounds `4L+2 .. n`: every round goes to `C_Z`, where `Z := 1 - (Y_1 XOR b0)` and
  `b0 := 1{Pi_C0 ranks agent 1 first}`.

Deviation (deterministic, in `B^ctx`): deliver `0` at round 1, then play `S*_1`.

Checks that each hypothesis holds:
* **(A3) holds verbatim.** Each context is a function of `Y_1` and `Pi_C0`, and both are realised before
  that context. `Pi_C0` is uniform given `G^0_2`, which contains `Y_1`. `Pi_C1` is uniform given its
  past. Every seed is uniform given `G^-_u`. This is exactly the latitude the hypotheses paragraph grants
  (line 794: "`x_u` may be an arbitrary measurable function of the entire past, including past rewards and
  past randomisations").
* **Exogeneity in the sense of FINAL.md (X) holds**, for every profile, including randomised ones and
  deviations by agent 2. `b0` is a fair bit independent of `(Y_1, theta)`, so `Z` is a fair bit
  independent of `Y_1`, of `theta` and of the deterministic prefix. The joint law of `(A, theta)` is
  therefore the same under every profile, and no agent can move the law of the path.
* **(A2)'s second half fails, as it should.** Given the whole path and `Y_1`, the value of `Z` pins
  `b0`, so (f1) fails in the path-augmented filtration. Theorem `thm:ctx-private-continuum`(i), which
  is stated under (A2), is therefore not touched.

Mechanics. Both agents bid exactly `1` at `C0` and at `C1`, so `Pi` decides the winner at each.
* In the baseline (`Y_1 = 1`), `Z = b0`. Agent 1 wins the bulk exactly when `b0 = 0` and `b1 = 1`,
  which has probability `1/4`.
* Under the deviation (`Y_1 = 0`), `Z = 1 - b0`. Agent 1 wins the bulk if `b0 = 1`, or if `b0 = 0`
  and `b1 = 1`, which has probability `3/4`.
* A winning agent 1 delivers `tau = (1 - sigma_n)_+`, is never switched on the good event, and earns
  `2 - tau >= 1` per pull. The same shape appears in CHECK.md Section 8.
* Expected gain: `1 + (n - 4L - 1)(2 - tau)/2 >= n/2 - o(n)`, which is `Theta(n)`.

Numbers (`adv_open/witness_xor_priority.py`, full CG-MESP simulator with monitor and EXP3, coupled on
shared seeds, priorities and EXP3 coins; `--stratify` averages exactly over the four equally likely
priority pairs):

| n | sigma_n | empirical P(Z=1) base / dev | gain (sim = analytic) | bound of Prop (i) |
|:-|:-|:-|:-|:-|
| 2*10^5 | 1.392 | 0.500 / 0.500 | 0.991 n | 0.722 n |
| 4*10^6 (monitor live, tau = 0.223) | 0.777 | 0.500 / 0.500 | 0.887 n | 0.388 n |
| 10^8 (analytic) | 0.399 | | 0.699 n | 0.200 n |
| 10^12 (analytic) | 0.054 | | 0.527 n | 0.029 n |

**Control, per the method rule.** Delete the `Y_1` clause, so that `Z := 1 - b0`, and rerun. The gain
falls to `1.0` exactly (round 1 only; `adv_open/witness_xor_priority.py 200000 40 --stratify --control`).
The numbers move, so W1 is a witness. Deleting the `b0` clause instead gives `Z = 1 - Y_1`, which is
the witness of Remark `rem:ctx-continuum-exogeneity`. That version violates (X), because the path law
then moves.

Why the proof on file misses W1: its coupling uses "the same arrival path, seed array, priorities". In
W1, sharing seeds and priorities forces the two paths apart, because `Z` flips. Sharing the path
instead forces `Pi_C0` apart, and then the win inclusion (ctx-win-inclusion) fails. No coupling
satisfies both. W1 is the path analogue of CHECK.md Section 8: there the tie-break law reacted to an
agent's reward, and here the path reacts to reward XOR tie-break, which leaves the path law fixed.

### 1.2 What the manuscript's hypothesis means, and the repair

"No agent's behaviour can change the realised sequence of contexts" is a counterfactual statement, and
it has no content until the coupling is fixed. The manuscript never fixes it, and it never defines
"EXP3 coins". Under the distributional formalisation (FINAL.md (X)), W1 is exogenous and the clause of
(i) is **false**. Under the natural causal coupling, in which the primitives are shared, W1 is not
exogenous. The statement is therefore ill-posed as written, which is P2, and false under the only
formalisation on file, which is P1 relative to "(X) + (A3)".

This also fills the gap CHECK.md Section 7 left ("the one hypothesis without a witness is (A4f-P) over
(A4f) together with (X) for part (A) restricted to `B^ctx`"). W1 is that witness: (X) + (A4f) do not
suffice for `B^ctx`.

**Repaired hypothesis (XS), structural exogeneity.** On one space there are:
* environment randomness `omega`;
* agents' randomisation `theta`;
* independent of `(omega, theta)` jointly and of each other: i.i.d. uniform seeds `(U_t)`, i.i.d.
  uniform Stage-3 coins `(xi_t)` (with `I_t` the `xi_t`-quantile of `p_t`), and i.i.d. uniform cube
  priorities `(Pi_C)`.

The path is required to satisfy `x_u = f_u(omega, U_{<u}, xi_{<u}, (Pi_C)_{C met before u})` for fixed,
profile-independent maps `f_u`. It may depend on past seeds and past coins. It may not depend on
rewards, targets or realised selections.

**Proof check under (XS).** (A3) holds automatically for every profile. Both executions are built on
this space with shared primitives, and the path is the same in both by construction. The first visit
of each cube is therefore the same, the priorities are the same, and the Stage-1 rounds and the other
agents' Stage-1 rewards are the same. So (ctx-win-inclusion) and the common price hold pathwise.
* A `B^ctx` deviator who learns past seeds, other agents' rewards, the EXP3 state or priorities from the
  contexts gains nothing. Its target is still `G^-_u`-measurable, and every lemma (`lem:ctx-bidconc`,
  `lem:ctx-monitor-cont`, `lem:ctx-fallback-cont`, `lem:ctx-dev-fallback`) is uniform over
  `G^-_u`-adapted targets.
* `E*_C` lies in the deviating field `G^fb_C`, because `G_u` contains the seeds `U_t`.
* I tried the channels the brief lists (seed-encoding contexts, EXP3 state, monitor proximity, prices,
  priorities, `theta` correlated with `omega`). None of them breaks a step.

Conclusion: the proof on file supports "(XS) and (A3)", with the item-2 text fix, and needs no new
argument. FINAL.md Lemma 9 does **not** cover (XS), since it takes `A` independent of the seeds; a
Lemma 9' identical to Lemma 9 with `A := f(omega, U, xi, Pi)` is needed.

**Minimal repaired Proposition (i):** "under (A2), for every `S' in B^ctx+`; and, under (XS), for every
`S' in B^ctx`". The (XS) clause may also simply be dropped: the main theorem uses (A2) only.

### 1.3 Manuscript sentences that must change

1. `sections/sec2_model.tex` l.71: "The second half matters only for such deviators: ... against
   deviators who condition only on contexts already seen, exogeneity and (A3) suffice." Under the
   distributional reading this is false, because W1 needs the second half against a `B^ctx` deviator
   through the priority clause. Replace with the (XS) statement, or delete.
2. `app_contextual_private.tex` l.55-57 (preamble): "does not use it over `B^ctx`: there its proof uses
   exogeneity and (A3) only".
3. l.794-795: "`x_u` may be an arbitrary measurable function of the entire past, including past rewards
   and past randomisations". This is true for (A3), but next to "exogeneity" it invites W1. Add that
   part (i) additionally needs (XS).
4. l.808-809 ("Over `B^ctx` it is neither needed nor used") and l.819-822 ("uses all of (A3) and in
   addition the exogeneity half of (A2)").
5. l.1196: Proposition (i), "under exogeneity and (A3) alone, for every `S' in B^ctx`".
6. l.1312-1320 ("Exogeneity is used for the coupling and for nothing else"), and the end of the proof,
   l.1388. The coupling must be named: shared primitives, with the path a function of them.
7. Remark `rem:ctx-continuum-exogeneity`, l.1511ff: "The accurate statement of what is needed is that
   the arrival path is the same random sequence in the two coupled executions". It must add "in the
   coupling that also shares seeds, priorities and Stage-3 coins", because W1 is a path that is the
   same in *some* coupling.

## 2. The two remainder constants

Both CHECK.md claims are confirmed.

(a) l.1350 and l.1365-1366: "`2 n_C Pr((H*_C)^c)`", summed "with `sum_C n_C <= n`" to get `2n^-3/K`.
Here `n_C` is random and may be correlated with `H*_C`. Under (XS) the path may dump the rest of the
horizon into a cube once that cube's baseline monitor has left its band. The correct bound is
`sum_C 2E[n_C 1{H*_C^c}] <= 2n Pr(U_C H*_C^c) <= 2 J_n n^-3 / K`. The manuscript's figure is too small by
the factor `J_n`. This charge is also **missing** from the displayed remainder.

(b) l.1369-1370: "`2n sum_C Pr(bad_C) <= 2n * n * (...)`". This is valid only as a sum over the
deterministic set of `J_n` grid cubes with `J_n <= n`. Read as a sum over visited cubes, it is a sum over
a random index set.

Correct total: `4 J_n n^-4 + 6 J_n n^-3 / K`. This is at most the displayed `4n^-3 + 4K^-1 n^-2` if
`J_n <= 2n/3`. `adv_open/remainder_constants.py` scans every `n >= 4` for `d = 1..10`. Horizons with
`J_n <= n < 3J_n/2` exist only at `n <= 88573` (`d = 10`), and at smaller `n` for smaller `d`. All of
them lie far below the horizons at which the bound of (i) drops below `n` (`10^5.2` or more; see
`rem:ctx-horizons`). **The displayed statement stands.** Change the text at l.1350, l.1365-1366 and
l.1369-1370 to the corrected charges plus one line saying `J_n <= 2n/3` absorbs them. P3.

## 3. Convex costs

* **`lem:cost-convert`** (`sections/appendix_private.tex` l.14-27).
  * Part (a) is part (b) with the empirical measure.
  * Part (b): `m_bar in [0,1]`, and Jensen's inequality is applied to `pi/Q_bar`.
  * If `m_bar >= theta`, monotonicity finishes it. Otherwise `0 <= theta - m_bar <= Delta/Q_bar`, and the
    Lipschitz bound finishes it.
  * Correct. It is also tight: a point mass at `theta - Delta/Q_bar` on the steep piece of the kink
    `phi(m) = Lambda (m - 1 + 1/Lambda)_+` attains it with equality, so Lambda cannot be dropped.
  * A randomized test over 2*10^5 instances (kinks with `Lambda` up to 50, `m^p`, random convex
    piecewise-linear functions, all with `phi(1) - phi(0) = 1`) gives a minimum slack of `-9e-16`
    (`adv_open/cost_convert_check.py`).
* **Every Lambda in (i):**
  * Stage 2: `lem:ctx-monitor-cont`(c), `Lambda(1+2b_n(q))`. A deviator that under-delivers inside the
    band saves exactly `Lambda b_n(q)` (checked numerically). Correct.
  * Oscillation: `phi(mu^sup) - phi(mu^inf) <= Lambda rho_n/3`. Correct, and convexity cannot replace it.
  * Fallback: `lem:ctx-dev-fallback`, part (b) with `Delta = R_bar + (rho/3)H_bar`. Then `nu >= tau`
    gives `phi(nu) >= phi(tau)`, and the coefficient `1 + phi(mu^sup) - phi(nu) >= 0` holds by (N).
    Correct.
  * Honest cases: the per-pull utility is at most `1`, and the minimum of the two bounds equals `w_C`
    (both branches re-derived). Correct.
  * Terms with no Lambda:
    * Stage 1: `phi(M) - phi(m') <= phi(1) - phi(0) <= 1`. Correct.
    * The bad-event charges: per-pull utility lies in `[0,2]`, by (N) and monotonicity. Correct.
    * The facts `U'^fb >= 0` and `0 <= w_C <= 2`: by (N). Correct.
  * The accounting `q rho/3 + (2/3) rho H <= rho n_C` is correct.
* A phi attaining (N) with equality breaks nothing. The only P3: in `lem:ctx-dev-fallback`, `pi` is a
  conditional-expectation measure. Say that it is taken from a regular conditional law, which exists on
  a standard Borel space, so that `lem:cost-convert`(b) applies for each `omega`.

## 4. FINAL.md Lemma 9 (canonical coupling)

Sound under (X)+(A4f-P).
* (a): conditional on `(A, theta, past)`, each draw has its specified kernel by (A4f-P). The law of
  `(A, theta)` is profile independent by (X). The construction's fresh coordinates reproduce these
  kernels, so the joint laws agree.
* (b) and (c): re-derived; correct.

Attacks:
* **W1 shows the (f1)-given-path use is load bearing even for `B^ctx`.** W1 satisfies (X) and (A4f) and
  violates only (f1) given the path. Lemma 9's "freshness given the path of all three kinds of draw" is
  therefore not an artefact of `B^ctx+`. Recommendation: FINAL.md Section 3.4 and CHECK.md Section 7
  should cite W1.
* **P3.** (X)+(A4f-P) do *not* exclude reward-reactive paths. For example, `x_{u+1} := Y_u XOR zeta_u`
  with `zeta_u` a fair environment bit satisfies both. For a `B^ctx+` target that reads `x_{u+1}`, the
  causal model is then circular, as FINAL.md Remark 3.2e observes. So Lemma 9(a) *defines* the model's
  law ("draw `A` first") rather than reproducing it. FINAL.md Remark 3.2e's implicit claim that
  (A4f-P) removes reward-reactive arrivals is too strong. State that under (X)+(A4f-P) the model is the
  path-first model. For `B^ctx` the two coincide, so nothing else changes.
* Other channels tried: the cube-indexed `Pi_C` against first visits; `xi_t` at rounds that are Stage 3
  in only one execution; `theta` correlated with `A`; `E*_C` in the deviating field. None breaks the
  lemma.

## Files

* `adv_open/witness_xor_priority.py`: W1 simulator, analytic gain and Prop (i) bound (`--table`,
  `--stratify`, `--control`). Output at `n = 4*10^6`: `adv_open/w1_n4e6.txt`.
* `adv_open/remainder_constants.py`, output `adv_open/remainder_constants.txt`: the item-2 scan.
* `adv_open/cost_convert_check.py`, output `adv_open/cost_convert_check.txt`: the item-3 tests.
