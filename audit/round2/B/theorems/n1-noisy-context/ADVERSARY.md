# ADVERSARY: Theorem N / Proposition I (noisy-label PL-MESP)

DONE

Status: DONE 2026-10-01. All five priorities written. Scripts and outputs in `adv/`
(python: the project venv `.../0be94e74-.../scratchpad/venv/bin/python`; every run single core,
under 3 minutes). No canonical file edited; nothing committed.

Inputs read: SCOUT.md, PROVER1.md (all), PROVER2.md (all), `sections/app_contextual_private.tex`
l.60-700, `sections/sec4_contextual.tex` (thm:ctx-private-finite), `sections/appendix_private.tex`
l.100-215 (scalar private proof), c2 ADVERSARY/PROVER grep for the non-top branch, f1
ADVERSARY_OPEN.md Sec. 1 (witness W1).

Summary of verdicts

| priority | verdict | severity |
|:-|:-|:-|
| 1 PROVER2's "dbar > 2s labels cost only Stage 1" | PROVER2 is RIGHT. The paper's remark is a true description of a loose bound, not a false claim; the paper's own scalar proof already uses PROVER2's device. Recommended paper correction (uniform bound, drop the n-threshold and Gamma_i). | P3 for the paper (true but needlessly weak, and inconsistent with the scalar theorem) |
| 2 coupling with common true types | No break. Both (N) forms exclude every W1-type construction I tried; type-aware deviations attain exactly b_n(N), not more. | none |
| 3 (N) completeness | Both complete. Two P3 wording items (PROVER2). | P3 |
| 4 reconciliation | All disputed constants in both files are TRUE; PROVER2's are sharper or equal everywhere except (Conv), where PROVER1's is sharper. Scout's Prop. I corollary FALSE (both counterexamples reproduced, method-rule control passes). | scout corollary: P1 |
| 5 standard checks | Clean in both. | none |

---------------------------------------------------------------------------------------------

## 1. Priority 1: non-top labels with dbar_i(b) > 2 s_n

### 1.1 The remark and the step

* Paper remark: `app_contextual_private.tex` l.175-177 ("part (i) is uniform over deviations for
  each fixed instance but not over instance sequences whose positive capacity gaps vanish with
  n"), l.546-550 (instance threshold `4 s_n <= min delta_i`), and the main-text theorem
  `sec4_contextual.tex` l.52-64 (hypothesis "every n at which s_n has fallen below the capability
  gaps", term `Gamma_i = O(Q log n/delta_i^2 + Q sqrt(Kn log K)/delta_i)`). Same text in
  `AAMAS_sec4_contextual.tex` l.52-74 and `AAMAS_app_contextual_private.tex` l.177, 546.
  c2 (PROVER1 l.242, PROVER2 l.276) repeats it descriptively.
* PROVER2's step: Lemma 2(b),(e) + Part 1 Case 1. The good event `G_b` also contains the UPPER tail of
  the deviator's CAPACITY bid `beta^max_i` (cost `(2Kn^4)^{-1}`). Pathwise `beta'_i <= beta^max_i`
  (Stage-1 feasibility, same `(X_t, U_t)` in both executions). So on `G_b`, if `i` wins:
  `Mbar_i + s >= beta^max_i >= beta'_i >= max_{j!=i} beta_j >= Vbar_i - s`, i.e. `dbar_i <= 2s`,
  and `tau = (max_{j!=i} beta_j - s)_+ <= min{Vbar_i, Mbar_i}`. Hence (a) dbar > 2s: `i` never wins
  on `G_b`, contributes `l_i(b)` plus `O(N_b n^{-4})`; (b) 0 < dbar <= 2s: the top-branch argument
  applies verbatim because it only needs `tau <= Mbar_i` (baseline meets the price) and `tau <= Vbar_i`
  (fallback comparator `j*`).

### 1.2 Line-by-line check

Re-derived: Lemma 2(e),(f); Case 1 primary (`g = psi'_-(tau)` is `F^b`-measurable, `E[M_N|F^b]=0`,
`psi(mbar) >= psi(y*) + g(mbar - y*)` on `[lobar, Mbar]`); Case 1 fallback (`E sum 1{I=i} mbar >=
Vbar_i E Q_i - R_K >= w E Q_i - R_K`, then convexity at `w = min{Vbar_i, Mbar_i}`, then
`psi(y**) >= psi(y*)`); honest `y* = lobar` sub-case. All correct. The extra Hoeffding tail is
inside PROVER2's `P(G_b^c) <= n^{-4}`.

Decisive cross-check in the paper itself: the SCALAR private proof
(`appendix_private.tex` l.105-125, 166) defines `G_i := G_{-i} cap {beta_i^max <= M_i + s_n}` and states
"No capacity gap and no other instance quantity enters it"; `Private_information_setting.tex` and
`app_noisy_public.tex` l.80 say "This covers a non-top winner as well ... No capacity gap enters the
bound." The contextual proof simply did not import that event (its `G(z)` controls only `j != i`), so
its non-top branch had to bound the tenure of a winner whose price may exceed its capability.

### 1.3 Attempted counterexample (simulation)

`adv/p1_nontop.py 100000 200` -> `adv/out_p1_nontop.txt`. PROVER2's one-label simulator (imported
read-only), K = 3, `n = 1e5`, `s = 0.0692`, agent 1 non-top with `dbar` in
`{0.005, 2s-0.005, 2s+0.005, 4s-0.005}`, noise-free and noisy (`pi = (0.8,0.1,0.1)`). Deviation menu:
greedy rider (full Stage-1, ride the monitor, fallback low) with `h = 0, 15`, all-low post-bid,
shade 0.02, zero Stage-1 then ride. Common random numbers.

| case | dbar vs 2s | win rate | best mean gain | PROVER2 bound | paper bound |
|:-|:-|-:|-:|-:|-:|
| noise-free | 0.005 (<=) | 0.16 | 2116 (Stage-1 saving; rider 226 = 0.16 b_n(N)) | 8141 | 174990 (=l_i+2N) |
| noise-free | 0.133 (<=) | 0.000 | 3835 (Stage-1 only) | 8141 | 174990 |
| noise-free | 0.143 (>) | 0.000 | 3785 (Stage-1 only) | 5002 (=l_i) | 174990 |
| noise-free | 0.272 (>) | 0.000 | 3143 (Stage-1 only) | 5002 | 174990 |
| noisy | 0.005 | 0.245 | 345 (rider) | 8141 | 174990 |
| noisy | 0.133 / 0.143 | 0.000 | 3385 / 3335 (Stage-1 only) | 8141 / 5002 | 174990 |

No deviation exceeds PROVER2's bound; above `2s` every post-bid gain is exactly 0 in 200/200 runs
(the deviator never wins), and the only gain is the Stage-1 saving `<= l_i`. On the winning event at
small gap the rider earns `win-rate x b_n(N)` (226 = 0.16 x 1409), i.e. PROVER2's constant 1 in front
of `b_n` is attained there too. The paper's `2 N_z` charge for `delta < 4 s_n` is loose by a factor
of order `n^{1/3}` at this horizon.

### 1.4 Verdict and the correction to the paper

PROVER2 is right. The paper's remark is not a false mathematical claim (it describes the bound as
displayed), so this is not an error in a stated result; but the displayed bound, the hypothesis of
`thm:ctx-private-finite` ("every n at which s_n has fallen below the capability gaps"), and `Gamma_i`
are unnecessary, and they contradict the paper's own scalar theorem's "no capacity gap enters".
Severity P3 (statement true, needlessly weak, internally inconsistent). Recommended correction
(both `sections/` and `AAMAS_` twins):

* `prop:ctx-finite-exact`(i): replace the non-top sum by
  `Lambda sum_{z : 0 < delta_i(z) <= 2 s_n} E[1 + 2 b_n(N_z) + R_K(n)]` (equivalently: the top sum runs
  over `{z : delta_i(z) <= 2 s_n}`), with `G(z)` enlarged by `{beta_i^max(z) <= M_i^z + s_n}`
  (`P(G(z)^c) <= (2K-1)/(2Kn^4) <= n^{-4}`, unchanged total). The second display becomes uniform:
  `min{QL_n,n} + Lambda[Q + sqrt(2 ell_n Q n) + Q R_K(n)] + 8n^{-2}`, with no condition on `n`.
* Delete the remark at l.175-177 ("not uniform over instance sequences ..."), the instance-threshold
  sentences at l.546-550, and `Gamma_i` plus the `n`-hypothesis in `thm:ctx-private-finite`.
* Proof change: the non-top branch splits into (a) `delta_i(z) > 2s_n`: on `G(z)` agent `i` never wins
  (two lines, as in `appendix_private.tex` l.120); (b) `0 < delta_i(z) <= 2s_n`: the top-branch text
  verbatim, with "`tau <= V_i^z <= M_i^z`" replaced by "`tau <= min{V_i^z, M_i^z}` on `G(z)`".
  Both proofs of c2 carry over unchanged otherwise.
* Optional further sharpenings PROVER2 found, all checked and true: monitor slack `1 + b_n` instead of
  `1 + 2 b_n` in (i) (in expectation via `E[M_N | F^b] = 0`; `adv/out_p2_typeaware.txt` shows the
  best rider attains 0.994 `b_n(N)`, so `2 b_n` is loose by 2); and `Q R_K(n)` can be dropped from
  (ii) (charge the whole post-bid block on the switch event, probability `<= N_z/(2n^4)`).

---------------------------------------------------------------------------------------------

## 2. Priority 2: the coupling with common true types (PROVER1 Lemma C; PROVER2 Part 1)

### 2.1 What would have to fail

Both provers put `X_t` among the primitives, so the deviating and baseline executions share
`(B, coins, Pi, zeta/xi, X, U)` and every execution is a measurable function of them. This is
legitimate iff the conditional law of every draw given everything realised before it (in the
execution) is the specified, profile-independent kernel. PROVER1's Lemma C proves the law identity by
the chain rule; I re-derived it, correct. PROVER2 builds the space directly from the enumeration.

### 2.2 W1-type constructions tried (all excluded by (N) as each prover states it)

1. Label path reacts to reward XOR priority bit (literal W1 analogue: `B_t = 1 - (Y_1 XOR b0)` for
   late `t`). Both put `B` in every conditioning field. Given `sigma(B)`, either `Pi` (PROVER2: `Pi`
   uniform given `B, xi`) or `U_1` (both: `U_t` uniform given `sigma(B)` and the past) is no longer
   fresh, since `B` reveals `Y_1 XOR b0`. (N) fails, so excluded. In W1 the failure was that the
   hypothesis conditioned the path only on the PAST; here every draw is conditioned on the WHOLE label
   path, which is what kills it.
2. True type reacts to reward XOR a later priority / later seed / later fallback coin
   (`X_t = f(Y_{t-1} XOR bit(Pi_{b'}))`, `b'` met later; or `bit(U_{t+5})`). (N1) for `X_t` can hold
   (the bit is fresh at time `t`), but the later draw is then not fresh given a field that contains
   `X_t` and `Y_{t-1}`: PROVER1 (N2)/(N3)/(N4) condition on `O^X`, `O^P`, `O^-`; PROVER2 conditions every
   later draw on "every draw listed before it", which includes `X_t` and `U_{t-1}`. Excluded.
3. True type correlated with future labels, with agents' coins, or with past types given `B`: (N1)
   conditions on `sigma(B)`, the coin arrays and all past types. Excluded. (This is the bursty
   witness; it is a genuine restriction, recorded by both and by Prop. I.)
4. Deviator exploiting what it alone sees. The deviator's past true types and rewards are in
   `G_t` / `P_{t-1}`; every lemma is stated for responses `F_t(a)` measurable there; future `X` is
   fresh. Best attack: make rewards DETERMINISTIC given the type (instance `M_0 = (1,0,1)`) and ride the
   monitor exactly. `adv/p2_typeaware.py` -> `adv/out_p2_typeaware.txt`: best gain `1400.7 +- 19.7 =
   0.994 b_n(N)`, against PROVER2's slack `1 + b_n(N) = 1410` (total bound 8141). The type-aware rider
   coincides with PROVER2's seed rider (gains identical to the decimal), so type knowledge adds
   nothing over the pathwise bound `Z_rho >= rho tau - 1 - b_n(rho)`. Control (method rule, type
   clause deleted, blind level when unsafe): convicted in 100/100 and loses 14826, so the type clause
   is what lets the rider stay safe, but it cannot cross the bound.
5. D-learn correlation: the winner's `pihat_j` and its bid come from the same Stage-1 types, so
   winning selects optimistic `pihat`. Lemma 7 (P2) / Lemma 6(ii) (P1) are PATHWISE on the TV event,
   whose probability is unconditional given `B`; the indicator is `F^b`-measurable. No gap.

Verdict: no break. PROVER1's Lemma C and PROVER2's direct construction are both correct; (N) as each
states it excludes every path-reaction or type-reaction channel I could build.

---------------------------------------------------------------------------------------------

## 3. Priority 3: completeness of (N)

Families: labels `B` (both: drawn first, in every field); agents' coins (P1 `theta`, P2 `xi`: before
round 1, arbitrary law given `B`); priorities (P1 at first meeting, conditioned on `O^X_t`; P2 all at
start, conditioned on `B, xi`); fallback coins (P1 `I_t ~ p_t` given `O^P_t`, canonical
`I_t = G(p_t, xi_t)`; P2 `zeta_t` before `X_t`); true types; seeds. Deterministic: Stage-1/2
selections, water-fill level (both fix the tie by a stated rule), D-learn "largest level", messages.
Nothing omitted in either. Each clause conditions on everything realised before the draw, so no
family can be silently omitted (the f1 Sec. 20 lesson). Both forms are equivalent to the product form
given `B`.

P3 items (PROVER2): (i) the profile-independence of the law of `(B, xi)` (PROVER1's (X)) is called
"automatic"; it should be stated, because a deviator's own coin law changes with its strategy and the
coupling needs one fixed array (any behavioural strategy can be read off a fixed uniform array, so
nothing breaks). (ii) The map `zeta_t -> I_t` (quantile of `p_t`) is not written out; PROVER1's
Lemma C does it. (iii) PROVER2's class `D_{i,n}` is narrower than PROVER1's `B^N#`, but PROVER2's
proof is written against `G_t`, which contains all past draws, so its bound holds verbatim for `B^N#`.

---------------------------------------------------------------------------------------------

## 4. Priority 4: reconciliation

| item | PROVER1 | PROVER2 | verdict |
|:-|:-|:-|:-|
| non-top terms in (A) | paper form (1/dbar^2, 2N_b) | none above 2s; top-form at 0<dbar<=2s | both true; P2 strictly sharper (Sec. 1) |
| monitor slack | 1 + 2 b_n | 1 + b_n | both true; 1 is attained (0.994 b_n) |
| costs | linear | convex, Lambda-Lipschitz via psi | P2's Lemma 1 (water-fill optimal for every convex phi and pi; psi convex, monotone, Lambda-Lipschitz) re-derived, correct |
| revenue loss | eps n max_a M_(2)(a) | omega' eps n <= that; Bayes-error form for any label->type map | both true; P2 <= P1 always; constant attained by the scout's example. `adv/p4_bench.py`: 1e5 random instances, max violation 2e-16 for P2's form, 0 for P1's, the Bayes form and the honest form |
| revenue error terms | ... + Q_B R_K(n) + n^{-3} | ... + n^{-3} + n^{-2}/2, no R_K | both true; P2 sharper |
| (Conv) | (2Kn^4)^{-1} + N_b(2n^4)^{-1} per (j,b), WHATEVER the others do; total (2n^3)^{-1} + #labels (2n^4)^{-1} | (2n^3)^{-1} + (2n^4)^{-1} per label, all on S*_N | both true; P1 sharper and more robust |
| D-learn | 2 kappa_n n, kappa_n with 4 log n (failure K n^{-4}) | 2 Lambda gam_n n, gam_n with log(K n^4) (failure n^{-4}) | both true; same order; scout's `n gamma` is not proved (estimation error acts on both sides) |
| Prop. I | identity G + P = D, CL-MESP: P >= eps n/4 - O(n^{2/3} log^{1/3} n), conviction w.p. -> 1 | gain >= (p - alpha_w) eps(1-theta) n vs a cooperative comparator | both true (below) |

Prop. I counterexamples to the scout's corollary, `adv/p4_propI.py 20000 200 0.2` ->
`adv/out_p4_propI.txt`:
* PROVER1's mechanism (label c goes to W only while W's second-half label-a reward rate >= 1/4):
  alpha = 0, scout's bound `eps n/4 = 1000`, measured `G = -6992` (analytic -7000). Identity:
  `G + P = 999.2 = D`. Coupling `(P1, coop) == (P2, shade~)` pathwise: True. CONTROL (cross-label
  clause deleted): `G = 999`, the scout's bound then holds, so the cross-label clause is the witness.
* PROVER2's mechanism (gamma to W iff its last alpha reward was 1): gain vs scout's "1/2 throughout"
  = -1000 < 999 = scout's bound; gain vs PROVER2's cooperative comparator = 1001 >= (p - alpha_w)E_2
  = 999. Coupling pathwise: True.
Scout's corollary: FALSE for general label-measurable mechanisms (P1). Both corrected statements
are true.

Difference in what they mean. PROVER1's `P2` path satisfies (N) (`pi_a = delta_a`, `pi_c = delta_d`),
so (c) ties Prop. I to Theorem N: on an (N)-instance shading gain is `o(n)`, so the compliant winner
must lose `~eps n/4` allocations on the reordered path. PROVER2's `P2` path (a then c) violates (N), so
its statement is about two non-(N) paths and does not connect to Theorem N. PROVER2's reading caveat is
correct and applies to BOTH: in the two-block construction the withheld allocations are rounds where
W has capability 0, so withholding them is efficient. The substantive harm needs a further block
of type-a rounds: under CL-MESP the conviction is permanent and W then serves type a only in the
fallback, where `S*` delivers capability 1 at utility 0 per pull. This is provable in three lines
from PROVER1's (d) (P2's E4 measures it: 8283 vs 19774).

---------------------------------------------------------------------------------------------

## 5. Priority 5: standard checks

* Indicator x conditional expectation: every occurrence in both files has the indicator measurable
  w.r.t. the conditioning field (P1 list after (8.5); P2 Part 7 audit). Re-checked independently,
  including PROVER1 Lemma 5 (`1_Gamma`, `Gamma in P_{t_{q0}}`) and PROVER2 Case 1 (`g`, `tau` in `F^b`).
* Union bounds: over `r <= N_b` and agents/subsets only, all deterministic given `B`; labels are never
  unioned with a per-label failure probability (both charge `N_b x P(bad_b)` and use `sum N_b <= n`).
* Costs: Stage-1 term `phi(M) - phi(m') <= 1` by normalisation in both; P2's convex extension correct.
* Minor: PROVER2's [F] is applied conditionally on `F_sigma` with a random switch round; fine, or
  decompose on the switch index as PROVER1 does.

---------------------------------------------------------------------------------------------

## 6. Recommended final statements

**Theorem N.** Hypotheses: (X) the law of `(B, theta)` is profile-independent; (N) in PROVER1's
named-field sequential form (equivalently PROVER2's enumeration form); fixed posterior kernel `pi`;
nonempty honest set; `K >= 2`, `n >= 2K`; costs convex, nondecreasing, `Lambda`-Lipschitz with
`phi(1) - phi(0) <= 1`. Deviation class `B^N#` (any function of everything realised before the
target, no future types). Then, with `W_i := {b : N_b >= 1, dbar_i(b) <= 2 s_n}`:
* (A) `gain <= E sum_b l_i(b) + Lambda E sum_{b in W_i}(1 + b_n(N_b) + R_K(n)) + n^{-2} + 2n^{-3}
  <= min{Q_B L_n, n} + Lambda[Q_B + sqrt(ell_n Q_B n/2) + Q_B R_K(n)] + n^{-2} + 2n^{-3}` (PROVER2).
* (B) `P(n; S*_N) >= E sum_t Mbar_(2)(B_t) - [min{Q_B K L_n, n} + 2 s_n n + n^{-3} + n^{-2}/2]`; if labels
  name types, `E sum_t M_(2)(X_t) - E sum_t Mbar_(2)(B_t) <= omega' epsbar n <= epsbar n max_a M_(2)(a)`,
  attained.
* (C) PROVER2's form; benchmark loss `<= epsbar n max_a b(a)`, zero with one honest agent.
* (Conv) PROVER1's form.
* (D) rates, `Q_B` for `Q`.
* Corollary (D-learn): extra `2 Lambda gam_n E sum_{b in W_i} N_b <= 2 Lambda gam_n n`,
  `gam_n = sqrt((|A| log 2 + log(K n^4))/(2 L_n))`, extra failure `O(n^{-3})`.

**Proposition I.** PROVER1's instance and paths (class map; `P2` satisfies (N)). (i) For every
label-measurable mechanism, `(P1, sigma)` and `(P2, sigma~)` have identical laws of all observables, and
`G + P = D` exactly. (ii) For CL-MESP with `S*`: `P >= eps n/4 - O(n^{2/3}(log n)^{1/3})`, and the
pointwise-compliant W is switched out at label a on `P1` with probability `>= 1 - P(Bin(n/2, eps) < k_n)
- 2n^{-3}`. (iii) Remark: with a further type-a block of length `theta n`, W's utility on that block is
`0` on `P1` after the switch versus `>= (1/2 - 2 s_n) theta n - O(1)` on `P2`. State explicitly that the
scout's mechanism-independent corollary is false (cross-label punishment), and that Prop. I shows
loss of protection of POINTWISE compliance, not an efficiency loss in the two-block form.

**Paper correction (from priority 1).** Make `prop:ctx-finite-exact`(i) and `thm:ctx-private-finite`
uniform as in Sec. 1.4 (enlarge `G(z)` by the upper tail of `beta_i^max`, split the non-top branch at
`2 s_n`, delete `Gamma_i`, the `n`-threshold and the non-uniformity remark), in both the
`sections/` and `AAMAS_` copies. Not a falsity; a strengthening that removes an inconsistency with
the scalar theorem.
