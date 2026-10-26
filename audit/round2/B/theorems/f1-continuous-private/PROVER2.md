# F1, CG-MESP on a continuum with private capacities: independent second proof

Worker: second prover on track F1, 18 September 2026. Output scope: this file and the scratchpad.
No canonical file was modified. No em dash and no triple hyphen appears in this file.

I did not walk through `EXPLORER.md` Section 7 confirming steps. I took the mechanism of
`EXPLORER.md` Section 3, the hypotheses of Section 4 and the statement of Section 6, put the
proof aside, and derived the three parts. I read Sections 5 and 7 of `EXPLORER.md` only after my
own derivation was written down, in order to report where the two routes coincide and where they
diverge. Sections 1 to 8 below are my derivation. Section 9 onwards is the comparison, the
defects I found, and my verdict.

**REVISION 2, 18 September 2026, after `ADVERSARY.md`.** Read this note before anything else.
Four things changed and two of the four are my own errors.

1. **The hypotheses as written are pairwise independences and do not give the mutual independence
   every martingale step here uses.** Part (A) is false under the literal hypothesis list; the
   adversary's G1 instance gains about `0.4998 n`. Section 2 of this document said "mutually
   independent by (A3) and (A4)", which is a non sequitur, and is now corrected in place with the
   one word repair and the counterexample stated where a reader cannot miss it. This is the second
   time the defect has been written in this project.
2. **The step I named as least secure is not insecure.** The monitor's predictability requirement
   is a bookkeeping artefact; written at the pre-seed field with the indicator stopped, the same
   bound follows using no property of the arrival path. Section 17.1. The consequence is a genuine
   strengthening: **parts (B) and (C) hold under arrivals merely nonanticipating with respect to the
   seeds, with no exogeneity at all**, and only part (A) needs exogeneity, which it genuinely does
   because it is false without it. Section 17 writes both upgrades out, including the third load on
   exogeneity (the fallback horizon) that nobody had named and that Lemma P7c removes.
3. **A measurability error in my own proof** (the adversary's G5): Section 6 claimed the baseline
   monitor event is measurable at the deviating execution's fallback start, and it is not. Corrected
   in place, three lines, `O(n^{-2})` extra charge, no change to any statement.
4. **Framing withdrawn**: the exponent comparison, the "no top-set condition" claim, the "no
   instance constant" separation, and the scalar by-product, which is already in the manuscript and
   which I quoted from a stale version. Section 19. Section 18 computes the horizons at which the
   bound is not vacuous.

**REVISION 3, after `ADVERSARY.md` Sections 14 to 16.** The adversary closed G2 to G8 and closed G1
for parts (A) and (B), and it broke the hypothesis Revision 2 introduced.

1. **(A4c) omits the mechanism's own randomisation, and my upgraded part (C) was false** (finding
   H1). Lemma P7c uses the freshness of the fallback selection coin, which (A4c) does not supply;
   the witness makes the arrival path a function of that coin, the honest comparator is then never
   selected at a cube, and part (C) upgraded fails by about `0.45 n` against a sublinear budget.
   The failure is mine.
2. **The hypothesis is rewritten in conditional form** as (A4f), Section 17.0: every draw at a
   round, the priority permutation, the selection and the seed, has its specified law conditionally
   on everything realised before it. That is one quantifier, not a list, and it is the form the
   manuscript's scalar theorem already uses. **Three defects on this project have come from
   assembling that sentence as a list; a list can omit a family and the conditional form cannot.**
   Section 17.0 also states, lemma by lemma, which clause each result uses.
3. **Parts (B) and (C) are now stated separately**, because their hypotheses differ and neither
   dominates: part (B) needs the seed clause alone, part (C) needs the mechanism clause too.
4. **The benchmarks are endogenous** under the weakened hypothesis, so the guarantees are statements
   about the realised path and not about a property of the environment (end of 17.5).
5. **Part (A)'s requirement is restated precisely**: not "exogeneity is irreducible" but "a
   deviation cannot move the arrival path", which exogeneity delivers and which is necessary
   (17.4).
6. Two arithmetic corrections: Section 20's instance fails by `n/4`, not `n/2`; and Lemma P7c's
   final sentence was asserted, unproved and unused, and is deleted. Lemma P1c is now stated only
   at cubes that complete bidding, and the martingale step inside a case in part (C) is written
   down.

Section 19 withdraws **my** framing and upholds all five of the adversary's framing findings; the
opposite reading was briefly in circulation and is corrected at the head of that section.

**Summary of my conclusion, as revised.** I believe parts (A), (B) and (C) are true, under the
repaired hypothesis (A4f) of Section 17.0, at the claimed exponent, with no instance constant in the
bounds: part (B) under the seed clause alone, part (C) under the seed and mechanism clauses, and
part (A) under those plus the requirement that a deviation cannot move the arrival path. Neither
(B) nor (C) places any condition on the arrival process itself. I no longer claim that the agreement of the two proofs is strong independent
evidence: the two documents share an upstream error (item 2) and each made the same shaped
conditioning mistake in the one place the other was careful (item 3 and defect D2).

- The explorer's Lemma 5 needs the deviator's **counterfactual** capacity bid `beta^cap_{i,C}` in
  the good event. I do not. I use a one sided Azuma bound on the deviator's **actual** bid, whose
  predictable target average is at most its capacity average by feasibility. That bound is
  uniform over the deviation class and needs no counterfactual object at all.
- I therefore answer the question the explorer could not: the manuscript's sentence at
  `sections/appendix_private.tex` line 99 ("No concentration around the deviator's capacity is
  invoked") is **caution, not an obstruction**. Both the counterfactual route and my actual bid
  route are sound. The by product of `EXPLORER.md` Section 7.4 (deletion of the non-top branch and
  of the `delta_i` constants from `thm:private-mesp`) survives my independent check, and I give a
  proof of it that does not use the counterfactual either.
- I found four defects, none fatal, all local: a union bound that is off by a factor `n` in
  Lemma 6(a); an incorrect measurability assertion about the global good event `G` in Section 7.1
  and again in 7.3, with a one line repair; a constant in `e_rob` that is loose rather than wrong;
  and a missing fallback regret term in part (B). Details and severities in Section 11.
- The step I originally considered least secure was the `F_{s-1}`-measurability of the Stage-2
  indicator. **That ranking was wrong** and Section 17.1 removes the step entirely. The revised
  ranking is in Section 20: the hypothesis list first, the part (A) coupling second, the conditional
  expectation bookkeeping third, the threshold `n >= exp(3L)` fourth. Sections 12 and 14 below are
  the original text and are superseded on this point by Sections 17 and 20.

## 1. What I take as given, and what I prove

Given: the mechanism CG-MESP exactly as specified in `EXPLORER.md` Section 3 (parameters `g_n`,
`h_n`, `J_n`, `L_n`, `ell_n`, `s_n`, `rho_n`, `sigma_n`, `b_n`, `R_K`, `R^dbl_K`; the cube grid;
the per cube state; the round rule; the three stages; the messages; the proposed profile `S^*`),
the hypotheses (A1) to (A6) of Section 4, and the statement of Theorem 1 in Section 6. Nothing
else from `EXPLORER.md` is assumed: in particular I re-derive every lemma I use.

Notation. `[K] = {1,...,K}`; `(x)_+ = max(x,0)`; `log` natural. For a cube `C`, `V_C` is its visit
count over the horizon, `n_C := (V_C - K L_n)_+` its post-bidding visits, `J'_n` the number of
cubes visited at least once. For agent `j`, `x_{j,t}` is its coordinate at round `t`,
`M_j^inf(C) := inf_{X in C} M_j(x_j)`, `M_j^sup(C) := sup_{X in C} M_j(x_j)`, and likewise for
`mu_j`. Per pull utility of `i` is `1 + mu_i(x_{i,t}) - m_{i,t} in [0,2]`.

**Fact 0 (oscillation), my derivation.** Two profiles in the same cube differ by at most `h_n` in
each of the `D` coordinates, so any single agent's `d` coordinates differ by at most
`sqrt(d) h_n <= sqrt(D) h_n` in Euclidean norm. By (A1) every `mu_j` and every `M_j` is
`L`-Lipschitz in its own argument, so
`M_j^sup(C) - M_j^inf(C) <= L sqrt(D) h_n` and the same for `mu_j`. By (A2), `log(en) >= 3 L`, so

    L sqrt(D) h_n  <=  (1/3) sqrt(D) h_n log(en)  =  rho_n / 3 .

I will write `omega := L sqrt(D) h_n <= rho_n/3` for the within cube oscillation. Note that this
is the only role of `L` and of (A2): `L` never enters a bound, only the hypothesis. Note also
that `omega` bounds the oscillation of `mu_j`, of `M_j`, of `M_*`, of `M_(2)` and of `b`, each
being a pointwise maximum or order statistic of `L`-Lipschitz functions of single coordinates
(order statistics are 1-Lipschitz in the supremum norm).

## 2. Probability space, filtration, and the two structural facts

**(A3+A4) AS WRITTEN ARE NOT ENOUGH, AND THIS SENTENCE IS THE PLACE IT MATTERS.** One
probability space carries the arrival path `A = (X_1,...,X_n)`, the seed array `(U_t)_{t <= n}`,
the cube priorities `(Pi_C)`, the EXP3 coins and every agent's private coins. Every argument below
needs these four families to be **mutually** independent. (A3) and (A4) of `EXPLORER.md` Section 4
are lists of **pairwise** independences and do not imply it, and my first version of this paragraph
said "mutually independent by (A3) and (A4)", which is a non sequitur. The adversary
(`ADVERSARY.md` finding G1) exhibits a `K = 2` instance with constant capacities (so (A1) and (A2)
are vacuous) and i.i.d. uniform arrivals in which every displayed clause of (A3) and (A4) holds,
the seeds are `U_t = frac(x_{1,t} + c_t)` with `c_t` the deviator's own coin, the deviator
therefore knows `U_t` exactly before choosing its target, and it reproduces the baseline reward law
at half the effort, gaining `tau_C (2 - tau_C)/2` per post-bidding round, which tends to `0.4998 n`
against a bound `O(n^{4/5} log n)`. I checked that instance by hand: `frac(x + c)` is uniform and
independent of `x`, and uniform and independent of `c`, while being a deterministic function of the
pair, and the Stage-2 rule "deliver `U_t` if `U_t <= tau_C`, else `0`" reproduces Bernoulli(`tau_C`)
rewards at effort `tau_C^2/2`. The counterexample is correct and it is a counterexample to the
hypothesis list, not to the mathematics.

**The repair, which is one word, and which this document now adopts throughout.** Replace (A3) and
(A4) by the single hypothesis

> **(A4m)** `(U_t)_{t <= n}` is an i.i.d. uniform `[0,1]` array, and the four families `A`,
> `(U_t)`, the mechanism coins (the priorities `(Pi_C)` and the EXP3 coins), and the agents'
> private coin arrays are **mutually** independent.

Every use below is a use of (A4m). No bound, statement or rate changes. The manuscript's own scalar
phrasing, "targets are chosen before fresh conditionally independent Bernoulli seeds"
(`sections/Private_information_setting.tex`), is the correct strong form and the contextual
hypotheses should be written to match it rather than weaker than it. Section 17 below shows that
for parts (B) and (C) even (A4m) can be weakened, but in the direction of conditional freshness,
never in the direction of pairwise independence.

Both executions compared in any coupling (the deviating one and the baseline one) are built on this
same space from the same objects.

**Convention A.** Put `sigma(A) subseteq F_0` and `F_t := F_0 v sigma(U_1..U_t, coins through
round t)`. This is legitimate exactly because (A4m) makes `A` independent of the seeds and coins
**jointly**: conditioning on `A` does not change the joint law of the seeds and coins. All statements below are proved
conditionally on `A` and are uniform in `A`, so integrating over the law of `A` at the end is
immediate and no property of that law is used. I flag now that this convention is the single
hypothesis that carries the removal of i.i.d. arrivals, and I return to it in Section 12.

**Fact 1 (the Stage-1 schedule is `F_0`-measurable).** By the round rule, the phase of cube `C` at
a visit is determined by `V_C`, which counts visits to `C` along `A`; Stage 1 at `C` is exactly its
first `K L_n` visits and the agent pulled at the `v`-th visit is `((v-1) mod K) + 1`. Neither
reads a reward, a bid, a coin or a message. Hence: the set of Stage-1 rounds of each cube, the
identity of the agent pulled at each of them, and the map `(j,C,r) -> t_{j,C,r}` giving the round
of agent `j`'s `r`-th Stage-1 pull at `C`, are all `F_0`-measurable and therefore deterministic
once `A` is fixed, in **every** execution, whatever any agent does. In particular they are the same
in the deviating and in the baseline execution.

I verified against `EXPLORER.md` Section 3 that the mechanism as written has this property; it is
the design point 2 of that section. It is indispensable and I use it three times: for the bid
coupling, for the definition of the bidding concentration event, and for the predictability of the
Stage-2 indicator.

**Fact 2 (cube locality).** The bids, price, winner, switch time and fallback state at `C` are
functions of the rewards collected at visits to `C`, of `Pi_C`, of the fallback coins used at `C`,
and of `A`. Proof by induction on `t`: every per cube state variable is updated only at visits to
`C` and only from data produced at those visits, and the grid and all parameters are fixed before
play. Consequence: a switch at one cube changes nothing at another, and the utility of any agent
decomposes as a sum over cubes of contributions each of which is measurable in that cube's own
data and `A`. Note that this is a decomposition of a random variable, not an independence claim: a
deviator may correlate its behaviour across cubes freely, and every bound below is uniform over
everything it may condition on.

**Where the two executions are pinned together.** For `j != i` the Stage-1 target at round
`t_{j,C,r}` is `M_j(x_{j,t})`, an `F_0`-measurable number, and the seed `U_t` is shared, so the
Stage-1 reward `Y_{j,t} = 1{U_t <= M_j(x_{j,t})}` is **identical** in the two executions, for every
`j != i`, every cube and every `r`. Therefore `beta_{j,C}`, `j != i`, are identical pathwise across
the two executions. This uses Fact 1 and nothing else.

## 3. Bidding: the concentration I actually use

This is the place where my route and the explorer's differ, so I state mine in full.

For a cube `C` that completes bidding and an agent `j`, write `m_{j,C,r}` for `j`'s realised target
at round `t_{j,C,r}` (whatever strategy `j` is following), `Y_{j,C,r}` for the realised reward,

    beta_{j,C} := L_n^{-1} sum_{r <= L_n} Y_{j,C,r}          (the bid the mechanism sees),
    Abar_{j,C} := L_n^{-1} sum_{r <= L_n} m_{j,C,r}          (the average realised target),
    Mbar_{j,C} := L_n^{-1} sum_{r <= L_n} M_j(x_{j,t_{j,C,r}})   (F_0-measurable).

By feasibility `m_{j,C,r} <= M_j(x_{j,t_{j,C,r}})` pointwise, hence

    Abar_{j,C}  <=  Mbar_{j,C}      pathwise, for every agent and every behaviour.          (3.1)

By Fact 0, `Mbar_{j,C} in [M_j^inf(C), M_j^sup(C)]`, so for every `X in C`

    M_j(x_j) - omega  <=  Mbar_{j,C}  <=  M_j(x_j) + omega .                                (3.2)

**Lemma P1 (predictable bid concentration, uniform over all behaviour).** Define

    E_C := { |beta_{j,C} - Abar_{j,C}| <= s_n  for every j in [K] } ,
    E   := intersection over cubes C that complete bidding of E_C .

Then `Pr(E_C^c) <= K/(K n^5) = n^{-5}` and `Pr(E^c) <= n^{-4}`, whatever strategies all `K` agents
use, including strategies that condition on the entire arrival path.

*Proof.* Fix `j` and `C`. By Fact 1 the rounds `t_{j,C,1} < ... < t_{j,C,L_n}` are `F_0`-measurable.
Put `D_r := Y_{j,C,r} - m_{j,C,r}`. The target `m_{j,C,r}` is chosen after selection and before the
seed, so it is measurable with respect to `F_{t-1} v sigma(I_t = j, j's private coins)` with
`t = t_{j,C,r}`, and by (A4) the seed `U_t` is independent of that field and uniform, so
`E[D_r | F_{t-1} v sigma(I_t, coins)] = 0` and `D_r` lies in an interval of length `1` conditionally
(namely `[-m, 1-m]`). Hence `(sum_{q <= r} D_q)_{r <= L_n}` is a martingale with conditionally
bounded increments of range `1`, and Azuma-Hoeffding gives

    Pr( |sum_{r <= L_n} D_r| > L_n s_n )  <=  2 exp( -2 (L_n s_n)^2 / L_n )
                                          =  2 exp( -2 L_n s_n^2 )  =  2 e^{-ell_n}  =  (K n^5)^{-1},

using `s_n^2 = ell_n/(2 L_n)` and `ell_n = log(2 K n^5)`. Union over `j in [K]` gives
`Pr(E_C^c) <= n^{-5}`. At most `n` cubes are visited, and a cube that does not complete bidding
imposes no constraint, so `Pr(E^c) <= n^{-4}`. Nothing in the argument used the agent's strategy
beyond predictability of the target, so the bound is uniform over `B^ctx+` and over joint
deviations by all `K` agents. `QED`

Two remarks, because they are the whole point.

1. `E` is **not** a statement that any agent's bid concentrates around its capacity. It is the
   statement that a bid concentrates around the average of the targets that were actually
   delivered. For an agent following `S^*` the two coincide, because then `Abar = Mbar`. For a
   deviator they do not, and `E` does not claim they do. What `E` plus (3.1) gives is the **one
   sided** conclusion `beta_{j,C} <= Mbar_{j,C} + s_n`, which is the only direction any of the
   three parts needs about a deviator.
2. `E` is behaviour dependent as a set, but its probability bound is uniform over behaviour, and
   `E_C` is measurable with respect to the rewards at `C`'s Stage-1 rounds, hence with respect to
   the field at the start of `C`'s Stage 2 and a fortiori at the start of `C`'s fallback. I use
   the per cube events `E_C`, never the global `E`, whenever a conditional expectation is taken.
   Section 11 records that this is where I diverge from `EXPLORER.md` Section 7.1.

## 4. The three price lemmas

Throughout this section fix a cube `C` that completes bidding, let `beta_(1),C >= beta_(2),C` be
the two largest bids with multiplicity, `W = W_C` a largest bidder, and
`tau_C = (beta_(2),C - sigma_n)_+` with `sigma_n = 3 s_n + rho_n`.

**Lemma P2 (the realised winner can meet the price at every context of its cube).** On `E_C`, for
every `X in C`,

    tau_C  <=  ( M_W(x_W)  -  2 s_n  -  (2/3) rho_n )_+   <=  M_W(x_W) .

This holds whoever `W` is, whether or not `W` is deviating, and whatever any agent bid.

*Proof.* `W` is a largest bidder, so `beta_(2),C <= beta_{W,C}`. On `E_C`,
`beta_{W,C} <= Abar_{W,C} + s_n`, and by (3.1) `Abar_{W,C} <= Mbar_{W,C}`, and by (3.2)
`Mbar_{W,C} <= M_W(x_W) + omega <= M_W(x_W) + rho_n/3` for every `X in C`. Chaining,

    beta_(2),C  <=  M_W(x_W) + rho_n/3 + s_n ,

so `beta_(2),C - sigma_n <= M_W(x_W) - 2 s_n - (2/3) rho_n`, and taking positive parts preserves
the inequality since `tau_C = (beta_(2),C - sigma_n)_+`. `QED`

*Comment.* This is the lemma that removes the three obstacles named in
`c2-local-mesp/PROVER2.md` Section 9 item 1, and it does so for a reason worth stating plainly: the
mechanism never needs the bid to **be** a capacity. It needs the shaded second bid to be **below**
the capacity of whoever won, at every context of the cube. The first is false on a continuum; the
second is a one sided statement that survives both the cube averaging (paid for by `rho_n/3`, twice
over) and arbitrary deviation (paid for by `s_n`, via Lemma P1).

*Consequence P2a.* On `E_C`, at every Stage-2 pull at `C` the winner's `S^*` target
`min{tau_C, M_W(x_W)}` equals `tau_C`, and the honest variant `max{mu_W(x_W), min{tau_C, M_W}}` is
at least `tau_C`. So `S^*` delivers a constant during Stage 2 at a cube, and the cube's monitor is
a test against a constant.

*Consequence P2b (there is no non-top branch).* On `E_C`, if the deviator `i` is the winner then
`tau_C <= M_i(x_i)` at every context of `C`, so `S^*_i` is feasible against the announced price
everywhere in the cube. No capacity gap and no threshold on `n` of the form `4 s_n <= delta_i`
appears. I emphasise that my proof of this used the deviator's **actual** bid.

**Lemma P3 (a non-deviating comparator dominates the price).** Fix `i` and suppose all `j != i`
play `S^*`. On `E_C`, put `nu_i(C) := max_{j != i} M_j^inf(C)`. Then `tau_C <= nu_i(C)`.

*Proof.* Let `j*` attain `max_{j != i} beta_{j,C}`. If `i` is a largest bidder then
`beta_(2),C = max_{j != i} beta_{j,C} = beta_{j*,C}`; if `i` is not, then `W != i` and
`beta_(2),C <= beta_{W,C} <= beta_{j*,C}`. Either way `beta_(2),C <= beta_{j*,C}` with `j* != i`.
Since `j*` plays `S^*`, `Abar_{j*,C} = Mbar_{j*,C}`, so on `E_C`,
`beta_{j*,C} <= Mbar_{j*,C} + s_n <= M_{j*}^inf(C) + omega + s_n`. Hence

    tau_C  <=  M_{j*}^inf(C) + omega + s_n - 3 s_n - rho_n  <=  M_{j*}^inf(C) - 2 s_n - (2/3) rho_n
           <=  nu_i(C) .  `QED`

Note that Lemma P3 concerns an agent other than `i`, so it needs no statement about the deviator's
bid at all, one sided or otherwise.

**Lemma P4 (the price is close to the second capacity at `S^*`).** Suppose every agent plays `S^*`.
On `E_C`, for every `X in C`,

    tau_C  >=  M_(2)(X)  -  4 s_n  -  (4/3) rho_n .

*Proof.* Under `S^*`, `Abar_{j,C} = Mbar_{j,C}` for every `j`, so on `E_C`,
`beta_{j,C} >= Mbar_{j,C} - s_n >= M_j(x_j) - omega - s_n` for every `j` and every `X in C`, by
(3.2). The second order statistic is nondecreasing in each argument, so
`beta_(2),C >= M_(2)(X) - omega - s_n`. Subtract `sigma_n` and use `omega <= rho_n/3`; the claim is
trivially true when the right side is negative. `QED`

**Lemma P5 (honest bid floor).** Fix a cube `C`, let `v_C := max_{h in K_H} mu_h^inf(C)` and let
`h_C in K_H` attain it (fixed tie break). Then (i) `b(X) <= v_C + omega` for every `X in C`;
(ii) under any behaviour respecting pointwise honesty, `m_{h_C,t} >= v_C` at every round with
`X_t in C` at which `h_C` is selected; (iii) on the event
`E^H_C := { beta_{h_C,C} >= Abar_{h_C,C} - s_n }`, which has probability at least
`1 - (2 K n^5)^{-1}` by the one sided form of Lemma P1, `beta_{h_C,C} >= v_C - s_n`.

*Proof.* (i) Let `h` attain `b(X) = mu_h(x_h)`; then `mu_h(x_h) <= mu_h^inf(C) + omega <= v_C +
omega` by Fact 0. (ii) Honesty gives `m_{h_C,t} >= mu_{h_C}(x_{h_C,t}) >= mu_{h_C}^inf(C) = v_C`.
(iii) By (ii), `Abar_{h_C,C} >= v_C`. `QED`

## 5. Monitor and fallback

**Lemma P6 (anytime cube monitor).** Fix a cube `C`. Let `psi_s := 1{round s is a Stage-2 pull at
C}`, let `Y^C_r` and `m^C_r` be the reward and target at the `r`-th Stage-2 pull at `C`,
`Z_r := sum_{q <= r} Y^C_q`, `A_r := sum_{q <= r} m^C_q`, both extended with zero increments beyond
the number of Stage-2 pulls actually taken, and `Z_0 = A_0 = 0`. Put
`H_C := { |Z_r - A_r| <= b_n(r) for every r <= n }` and `H := intersection over C of H_C`. Then,
for any behaviour of every agent:

(a) `Pr(H_C^c) <= 2 n e^{-ell_n} = n/(K n^5)`, and `Pr(H^c) <= n^{-3}/K` by a union over the at
    most `n` visited cubes;
(b) on `H_C`, if the Stage-2 phase at `C` lasted `q` pulls counting its failing pull when there is
    one, then `A_q >= q tau_C - 1 - 2 b_n(q)`;
(c) on `H_C`, the Stage-2 winner's realised utility over that phase is
    `U^pri <= sum_{r <= q} (1 + mu_W(x_{W,r}) - tau_C) + 1 + 2 b_n(q)`;
(d) on `H_C`, if every Stage-2 target at `C` is at least `tau_C` then no switch occurs at `C`;
(e) `E[Z_r - A_r] = 0` for `r` equal to the total number of Stage-2 pulls at `C`.

*Proof.* Predictability. Whether round `s` is a Stage-2 pull at `C` is determined by `X_s` and
`V_C` at `s`, which are `F_0`-measurable under Convention A, and by whether `C` has already awarded
and has not yet switched, which is a function of rewards at rounds strictly before `s`. Hence
`psi_s` is `F_{s-1}`-measurable. Martingale. Put `N_t := sum_{s <= t} psi_s (Y_s - m_{I_s,s})`. As
in Lemma P1 the target is measurable with respect to `F_{s-1} v sigma(I_s, coins)` and the seed is
independent of that field, so `E[N_s - N_{s-1} | F_{s-1}] = 0` with conditional range at most `1`.
(a) For fixed `r`, the round of the `r`-th Stage-2 pull at `C` is a bounded stopping time, and the
stopped exponential supermartingale with the Hoeffding conditional bound
`E[e^{lambda(Y - m)} | .] <= e^{lambda^2/8}` gives
`Pr(|Z_r - A_r| > b_n(r)) <= 2 exp(-2 b_n(r)^2 / r) = 2 e^{-ell_n}`. Union over `r <= n`; beyond
the realised count the increments vanish and `b_n` is nondecreasing, so those `r` add nothing new.
(b) If no switch occurred through `q` then `Z_q >= q tau_C - b_n(q)` and on `H_C`
`A_q >= Z_q - b_n(q)`. If the switch occurred at `q`, apply this at `q-1` and use `A_q >= A_{q-1}`,
`tau_C <= 1`, `b_n(q-1) <= b_n(q)`. (c) `U^pri = sum_{r<=q}(1 + mu_W(x_{W,r})) - A_q` with (b).
(d) The hypothesis gives `A_r >= r tau_C`, so on `H_C`, `Z_r >= A_r - b_n(r) >= r tau_C - b_n(r)`
for every `r`, the negation of the switch test. (e) Optional stopping for `N` at the bounded time
`n`. `QED`

**Correction to the stated probability.** `EXPLORER.md` Lemma 6(a) claims `Pr(H^c) <= n^{-4}` by
counting "at most `n` pairs `(C,r)`, because the Stage-2 pulls sum to `n`". That count is not
available: the number of Stage-2 pulls at `C` is random, and a union bound over a random index set
does not follow from `sum_C q_C <= n`. The honest count is at most `n` cubes times `n` values of
`r`, so `Pr(H^c) <= 2 n^2 e^{-ell_n} = n^{-3}/K`. This is a real error but it is benign: it costs
`2 n Pr(H^c) = O(n^{-2}/K)` instead of `O(n^{-3})` in each of the three parts, which is below every
other term by a factor `n^{(D+2)/(D+3)+2}`. The minimal repair that restores the stated constant is
`ell_n := log(2 K n^6)`, which changes only constants inside logarithms. I use the corrected
probability throughout and absorb it into an `O(n^{-2})` term.

**The predictability step above is a bookkeeping artefact and Section 17 removes it.** The proof I
just gave asks `psi_s` to be `F_{s-1}`-measurable, which is true only because Convention A puts the
arrival path in `F_0`, and in the first version of this document I named that as the least secure
step of the whole theorem. That ranking was wrong. Writing the Chernoff step at the pre-seed field
with the indicator stopped gives the same bound using no property of the arrival path at all.
Section 17.1 writes it out; the statement, the constant and parts (b) to (e) are unchanged.

**Lemma P7 (cube fallback, unknown local horizon).** Fix a cube `C` at which a switch occurred and
let `H_C^fb` be the number of fallback visits to `C` (an `F_0`-measurable integer given the switch
round, since the remaining visits to `C` are determined by `A`; the mechanism never uses it).
Suppose some agent `j*` has conditional reward mean at least `v` whenever it is selected at a visit
to `C`. Then, conditionally on the fallback start field at `C`,

    E[ sum over fallback pulls at C of Y_t ]  >=  v H_C^fb  -  R^dbl_K(H_C^fb) .

*Proof.* Within one epoch of planned length `2^k` the algorithm is explicit exploration EXP3 tuned
to `2^k`. Write `r_{j,s} := E[Y_s | G_{s-1}, I_s = j]` where `G_{s-1}` is the whole past before the
selection at the `s`-th fallback visit to `C`; `r_{j*,s} >= v` by hypothesis and all other
`r_{j,s}` are whatever the other agents deliver, which the argument never needs. Since
`p_{j} >= gamma_k/K = eta_k`, the estimates satisfy `0 <= eta_k hat Y_j <= 1`, and the standard
exponential potential inequality with `e^x <= 1 + x + x^2` on `[0,1]` gives, for every prefix of
the epoch of realised length `T_k <= 2^k`,

    E[ sum_{s <= T_k} Y_s ]  >=  v T_k  -  2 gamma_k T_k  -  K log K / gamma_k
                             >=  v T_k  -  ( 3 sqrt( K 2^k log K ) + 2 K log K ) ,

by the two cases `gamma_k = sqrt(K log K / 2^k)` and `gamma_k = 1/2`, the latter only when
`2^k < 4 K log K`, where `3 sqrt(K 2^k log K) >= 1.5 * 2^k >= T_k`. Truncation of the last epoch is
covered because the potential inequality holds for every prefix. Summing over epochs
`k = 0,...,k_max` with `2^{k_max} <= H_C^fb`,

    sum_k 3 sqrt( K 2^k log K )  =  3 sqrt(K log K) ( 2^{(k_max+1)/2} - 1 ) / ( sqrt 2 - 1 )
                                 <=  3 ( 2 + sqrt 2 ) sqrt( K H_C^fb log K )
                                 <=  11 sqrt( K (H_C^fb + 1) log K ) ,

and the number of epochs is at most `log_2( 2 (H_C^fb + 1) )`, each contributing `2 K log K`. This
is `R^dbl_K(H_C^fb)`. The filtration may carry the entire arrival path and every agent's cross
cube history: the argument needs only that `p` is `G_{s-1}`-measurable and that the selection coin
and the seed are fresh, which hold by construction and (A4). `QED`

I re-derived the constant `3(2 + sqrt 2) = 10.24...` independently and it is below `11`, so the
stated `R^dbl_K` is valid.

**Lemma P8 (the deviator's fallback utility at a cube).** Agent `i` deviates, all `j != i` play
`S^*`, a switch occurred at `C`, `H := H_C^fb`. Let `Qbar_i` and `Abar_i` be the conditional
expectations, given the fallback start field at `C`, of `i`'s fallback pull count at `C` and of the
sum of its fallback targets there. Then

    E[ U_i^fb(C) | fallback start ]  <=  ( 1 + mu_i^sup(C) - nu_i(C) ) H  +  R^dbl_K(H)
                                          +  (rho_n / 3) H ,

and for honest `i` also `E[U_i^fb(C)] <= H`.

*Proof.* Let `j` attain `nu_i(C) = max_{j' != i} M_{j'}^inf(C)`. Under `S^*`, `j` delivers
`M_j(x_{j,t}) >= nu_i(C)` at every fallback pull, so Lemma P7 applies with `v = nu_i(C)`. Every
other non-deviator `j'` delivers at most `M_{j'}^sup(C) <= M_{j'}^inf(C) + omega <= nu_i(C) +
rho_n/3`. Splitting the total fallback reward at `C` into `i`'s share and the rest,

    nu_i(C) H - R^dbl_K(H)  <=  Abar_i + ( nu_i(C) + rho_n/3 )( H - Qbar_i ) ,

so `Abar_i >= nu_i(C) Qbar_i - R^dbl_K(H) - (rho_n/3) H`. Then
`E[U_i^fb(C)] <= (1 + mu_i^sup(C)) Qbar_i - Abar_i <= (1 + mu_i^sup(C) - nu_i(C)) Qbar_i +
R^dbl_K(H) + (rho_n/3) H`, and `nu_i(C) <= 1 <= 1 + mu_i^sup(C)` lets `Qbar_i` be replaced by `H`.
For honest `i`, each fallback pull contributes `1 + mu_i(x_i) - m <= 1`. `QED`

## 6. Part (A): additive behavioural equilibrium

Fix `i` and `S'_{i,n} in B^ctx+_{i,n}`, and couple the deviating execution (primes) with the
baseline execution (stars) by the same `A`, seed array, priorities, EXP3 coins and private coins.
By Fact 2 the utility of `i` decomposes over cubes, `u_i = sum_C E[U_{i,C}]`, in both executions,
so it suffices to bound `E[U'_{i,C} - U^*_{i,C}]` cube by cube. Write `E_C, H_C` for the events of
Lemmas P1 and P6 in the deviating execution and `E^*_C, H^*_C` for the same in the baseline, and
`bad_C` for the union of their complements, so `Pr(bad_C) <= 2 n^{-5} + 2/(K n^4)`.

**Bid domination at `C`.** By Fact 1 the two executions have the same Stage-1 rounds at `C` and
pull the same agent at each, and for `j != i` the Stage-1 rewards are identical (Section 2). At
`i`'s Stage-1 round `t`, feasibility gives `m'_{i,t} <= M_i(x_{i,t})`, so with the shared seed
`1{U_t <= m'_{i,t}} <= 1{U_t <= M_i(x_{i,t})}` and hence `beta'_{i,C} <= beta^*_{i,C}` pathwise.
Since the other bids agree and the tie break `Pi_C` is shared, every inequality defining "`i` is a
largest bidder" is preserved, so

    { i wins at C under the deviation }  subseteq  { i wins at C in the baseline } ,          (6.1)

and on that event `beta_(2),C = max_{j != i} beta_{j,C}` in both executions, so `tau_C` is the same
number in both and does not depend on anything `i` does. Note that this is the only use I make of
the baseline bid `beta^*_{i,C}`, and it is a pathwise domination, not a concentration statement.

**Stage 1 at `C`, pathwise.** The two executions are pulled at the same rounds, and the per pull
utilities differ by `M_i(x_{i,t}) - m'_{i,t} in [0,1]`, so the Stage-1 difference at `C` is at most
the number `l_i(C) <= L_n` of Stage-1 pulls `i` receives there. Summing,
`sum_C l_i(C) <= min{J'_n L_n, n} = e_bid`. This holds on every event. Cubes with `V_C < K L_n`
contribute only this term, since they never award.

**Post Stage-1 at `C`, on `E_C cap H_C cap E^*_C cap H^*_C`.**

*Case 1: `i` does not win at `C` under the deviation.* The winner `W != i` plays `S^*`, so by
Consequence P2a its Stage-2 target is at least `tau_C` at every context of `C`, and by Lemma P6(d)
no switch occurs at `C`. Hence there is no fallback at `C` and `i` receives no post Stage-1 pull
there: `U'^post_{i,C} = 0`. The baseline's post Stage-1 utility at `C` is nonnegative because per
pull utilities are nonnegative. The contribution to the gain is at most `0`.

*Case 2: `i` wins at `C` under the deviation.* By (6.1) it wins in the baseline too, at the same
price `tau_C`. Write `n_C = q + H` with `q` the Stage-2 tenure under the deviation and `H` the
fallback length, and set

    w_C := 1 + mu_i^inf(C) - tau_C                    if i is strategic,
    w_C := min{ 1 , 1 + mu_i^inf(C) - tau_C }         if i is honest,

which is nonnegative because Lemma P2 gives `tau_C <= M_i(x_i) <= 1 <= 1 + mu_i^inf(C)`.

Upper bound on the deviation. Lemma P6(c) and `mu_i^sup(C) <= mu_i^inf(C) + rho_n/3` give
`U'^pri <= q (1 + mu_i^sup(C) - tau_C) + 1 + 2 b_n(q) <= q w_C + q rho_n/3 + 1 + 2 b_n(q)` in the
strategic case. In the honest case we also have `U'^pri <= q` because every honest target is at
least `mu_i(x_i)`; taking the smaller of the two bounds gives the same display, since if
`w_C = 1` then `q w_C + q rho_n/3 + 1 + 2 b_n(q) >= q`, and if `w_C = 1 + mu_i^inf(C) - tau_C <= 1`
then `q w_C + q rho_n/3 >= q(1 + mu_i^sup(C) - tau_C)`. Lemma P8 with Lemma P3 (`nu_i(C) >= tau_C`,
which needs only `E_C`) gives `E[U'^fb | fallback start] <= H w_C + (2 rho_n/3) H + R^dbl_K(H)`,
again taking the smaller of the two bounds of Lemma P8 in the honest case. Adding,

    E[ U'^post_{i,C} ]  <=  n_C w_C + n_C rho_n + 1 + 2 b_n(n_C) + R^dbl_K(n_C) .

Lower bound on the baseline. On `E^*_C`, `S^*_i` delivers exactly `tau_C` (strategic) or
`max{mu_i(x_i), tau_C}` (honest) at every Stage-2 pull at `C`, both at least `tau_C`, so by Lemma
P6(d) applied in the baseline execution the baseline never switches at `C` and receives all `n_C`
post Stage-1 pulls, with per pull utility `1 + mu_i(x_i) - tau_C >= w_C` in the strategic case and
`min{1, 1 + mu_i(x_i) - tau_C} >= w_C` in the honest case. So `U^{*,post}_{i,C} >= n_C w_C`.

Difference: `E[U'^post_{i,C} - U^{*,post}_{i,C}] <= n_C rho_n + 1 + 2 b_n(n_C) + R^dbl_K(n_C)`.

**Legitimacy of the conditioning, which is where I diverge from `EXPLORER.md`.** Only two
conditional expectations were taken: Lemma P7 and Lemma P8 at cube `C`, both conditional on the
field at `C`'s fallback start. The events multiplying them must be measurable with respect to that
field. `E_C` is: it is a function of the rewards at `C`'s Stage-1 rounds, all of which precede
`C`'s Stage 2. `H_C` is: the Stage-2 martingale at `C` is frozen once the switch occurs, so the
event `{|Z_r - A_r| <= b_n(r) for all r <= n}` at cube `C` is determined at the switch round.
`E^*_C` likewise, for the baseline execution, which lives on the same space: it is a function of the
baseline's Stage-1 rewards at `C`, which occur at the same rounds in both executions and precede
`C`'s Stage 2 in both. The global events `E` and `H` are **not** measurable with respect to `C`'s
fallback start field, because they involve Stage-1 and Stage-2 data at cubes whose bidding has not
finished when `C` switches. That is why I use the per cube versions everywhere. `U'^fb >= 0`, so if
one prefers the global events the repair is
`E[U'^fb 1_{E cap H}] <= E[U'^fb 1_{E_C cap H_C}] = E[1_{E_C cap H_C} E[U'^fb | .]]`.

**Correction to the first version of this paragraph (`ADVERSARY.md` finding G5, and it is mine).**
The first version also claimed `H^*_C` is measurable with respect to the deviating execution's
fallback start field at `C`. **It is not.** In Case 2 the baseline does not switch at `C`, which is
what the case needs, so the baseline's Stage-2 phase at `C` runs through all `n_C` post Stage-1
visits, the last of them in general at a round strictly after the deviating execution switched at
`C`; so `H^*_C` depends on seeds drawn after `C`'s fallback start. I made, in the one paragraph
where I claimed to be more careful than the explorer, the same shaped error the explorer made with
`G`. The repair is three lines and it is the repair D2 needs. Write
`good := E_C cap H_C cap E^*_C cap H^*_C` and `F := E_C cap H_C cap E^*_C`, which **is** in the
fallback start field. On `good`, pathwise,

    U'^post_{i,C} - U^{*,post}_{i,C}  <=  U'^fb - H w_C + q rho_n/3 + 1 + 2 b_n(q) .

Since `U'^fb >= 0` and `0 <= w_C <= 2`,

    E[ (U'^fb - H w_C) 1_good ]  <=  E[ (U'^fb - H w_C) 1_F ]  +  E[ H w_C 1_{F \ good} ]
                                 <=  E[ 1_F ( (2 rho_n/3) H + R^dbl_K(H) ) ]  +  2 n_C Pr( (H^*_C)^c ) ,

and `Pr((H^*_C)^c) <= 2 n e^{-ell_n}` per cube with `sum_C n_C <= n`, so the extra charge over all
cubes is at most `2 n * 2 n e^{-ell_n} = 2 n^{-3}/K`, absorbed into the `O(n^{-2})` term that the
corrected D1 already produces. Neither the statement nor the rate changes. I record it as my own
defect, at the same severity I gave the explorer's D2, and I record the adversary's observation
that each of the two proofs avoided the other's instance of this error shape and committed its
own: agreement of the two routes is therefore weaker evidence than it looks, and I no longer claim
otherwise.

**Off the good events.** `sum_C E[ (U'_{i,C} - U^*_{i,C}) 1_{bad_C} ] <= 2 n sum_C Pr(bad_C)
<= 2 n * n * (2 n^{-5} + 2/(K n^4)) = 4 n^{-3} + 4/(K n^2)`.

**Summation.** `sum_C n_C <= n`, so `sum_C n_C rho_n <= n rho_n = e_osc`. By Cauchy and Schwarz,
`sum_C [1 + 2 b_n(n_C)] <= J'_n + 2 sqrt( J'_n * (ell_n/2) * sum_C n_C ) <= J'_n +
2 sqrt(J'_n n ell_n / 2) = e_mon`, and
`sum_C 11 sqrt(K (n_C+1) log K) <= 11 sqrt( K log K J'_n sum_C (n_C+1) ) <= 11 sqrt(2 K J'_n n log K)`
using `J'_n <= n`, with the logarithmic part summing to at most `2 K log K J'_n log_2(2(n+1))`, so
`sum_C R^dbl_K(n_C) <= e_fb`. Therefore

    u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)
        <=  e_bid + e_osc + e_mon + e_fb + 4 n^{-3} + 4/(K n^2) ,

uniformly in `A`, hence after integration. This is part (A) with the last term `O(n^{-2})` in place
of the report's `6 n^{-3}`; see Section 11, defect D1. `QED`

## 7. Part (B): second capacity revenue

All agents play `S^*`, so `Abar_{j,C} = Mbar_{j,C}` for every `j` and `C`. By (A4) and the tower
property, `P(n;S^*) = E[ sum_{t <= n} m_{I_t,t} ]`: the reward at a round is Bernoulli with mean
equal to the target chosen just before it, so no optional stopping and no stopping time argument is
needed anywhere in this part. I note that the manuscript's scalar revenue proof
(`sections/appendix_private.tex`, revenue part) does invoke a stopping time argument; the
identity above is strictly simpler and I use it.

Discard the Stage-1 rounds, at most `min{K J'_n L_n, n} = e_stage1` of them, at which the target is
nonnegative and `M_(2) <= 1`. Work on `E_C cap H_C` cube by cube. By Consequence P2a the Stage-2
target at an awarded cube is at least `tau_C` at every context, so by Lemma P6(d) no switch ever
occurs and every post Stage-1 round is a Stage-2 round. By Lemma P4, for every post Stage-1 round
`t` with `X_t in C`,

    m_{I_t,t}  >=  tau_C  >=  M_(2)(X_t) - 4 s_n - (4/3) rho_n .

Summing over the post Stage-1 rounds of `C` and over cubes, and charging `bad_C := E_C^c cup H_C^c`
at `n_C <= n` rounds each with `M_(2) <= 1`,

    P(n;S^*)  >=  E[ sum_{t <= n} M_(2)(X_t) ]  -  e_stage1  -  n (4 s_n + (4/3) rho_n)
                  -  n sum_C Pr(bad_C)
              >=  E[ sum_t M_(2)(X_t) ]  -  ( e_stage1 + e_price + O(n^{-2}) ) .

This is part (B). No fallback regret term is needed, because on the good events `S^*` never
triggers a switch. `QED`

## 8. Part (C): honest benchmark robustness under arbitrary joint behaviour

Now every agent may play any strategy in `B^ctx+`, subject to feasibility and, for `h in K_H`, to
pointwise honesty. `E_C` of Lemma P1 is still available (its probability bound is uniform over all
behaviour), but I only need its one sided honest form. Fix a cube `C` that awards, take `v_C` and
`h_C` from Lemma P5, and work on `E^H_C cap H_C` where
`E^H_C := { beta_{h_C,C} >= Abar_{h_C,C} - s_n }`, so `Pr((E^H_C)^c) <= (2 K n^5)^{-1}` and
`beta_{h_C,C} >= v_C - s_n` there by Lemma P5(iii).

Again `P(n;S) = E[ sum_t m_{I_t,t} ]`, and I discard the at most `e_stage1` Stage-1 rounds.

*Case (i): `W_C = h_C`.* Every Stage-2 target at `C` is at least `mu_{h_C}(x_{h_C,t}) >= v_C` by
honesty (Lemma P5(ii)), so the Stage-2 target sum is at least `v_C q`. If a switch occurs, Lemma P7
with the comparator `h_C` and `v = v_C` (legitimate by Lemma P5(ii), which is pathwise and holds
whatever the other agents do) gives fallback reward at least `v_C H - R^dbl_K(H)` conditionally on
the fallback start field, and `E^H_C cap H_C` is measurable with respect to that field exactly as
in Section 6. Adding, the post Stage-1 contribution of `C` is at least `v_C n_C - R^dbl_K(n_C)`.

*Case (ii): `W_C != h_C`.* Then `beta_(2),C >= beta_{h_C,C} >= v_C - s_n`, so
`tau_C >= v_C - s_n - sigma_n = v_C - 4 s_n - rho_n`. On `H_C`, Lemma P6(b) gives
`A_q >= q tau_C - 1 - 2 b_n(q)`, and if a switch occurs Lemma P7 with comparator `h_C` again gives
at least `v_C H - R^dbl_K(H) >= (v_C - 4 s_n - rho_n) H - R^dbl_K(H)`. Adding, the post Stage-1
contribution of `C` is at least `n_C (v_C - 4 s_n - rho_n) - 1 - 2 b_n(n_C) - R^dbl_K(n_C)`.

Case (ii) is the weaker of the two. By Lemma P5(i), `v_C >= b(X_t) - omega >= b(X_t) - rho_n/3` for
every `X_t in C`, so the post Stage-1 contribution of `C` is at least

    sum_{post Stage-1 t with X_t in C} b(X_t)  -  n_C ( 4 s_n + (4/3) rho_n )
        -  1 - 2 b_n(n_C) - R^dbl_K(n_C) .

Summing over cubes with the two Cauchy and Schwarz steps of Section 6, charging the at most
`e_stage1` Stage-1 rounds at `b <= 1` each, and charging the complements at
`n sum_C Pr((E^H_C)^c cup H_C^c) = O(n^{-2})`,

    P(n;S)  >=  E[ sum_{t <= n} b(X_t) ]  -  ( e_stage1 + n(4 s_n + (4/3) rho_n) + e_mon + e_fb
                 + O(n^{-2}) ) ,

uniformly over the joint behavioural profile. This is part (C), with `n(4 s_n + (4/3) rho_n)` in
place of the report's `e_rob = n(4 s_n + (5/3) rho_n)`; my constant is smaller, so the report's
statement is implied. `QED`

*Why my constant is smaller.* `EXPLORER.md` Lemma 9 takes `v_C` as an infimum over the cube and
loses `2 rho_n/3` in passing from `b(X)` to `v_C`; I lose only `rho_n/3` because Lemma P5(i)
compares `b(X) = mu_h(x_h)` for the maximising `h` at the same `X` directly with `mu_h^inf(C)`, and
then uses `v_C >= mu_h^inf(C)`. Both are correct; the difference is bookkeeping, not substance.

## 9. Part (D): the exponent, checked independently

With `g_n = ceil(n^{1/(D+3)})`, `h_n = 1/g_n`, `L_n = ceil(n^{2/(D+3)})` and `ell_n = log(2 K n^5)`:

- `J_n = g_n^D <= (n^{1/(D+3)} + 1)^D <= 2^D n^{D/(D+3)}` for `n >= 1`, and `J'_n <= min{J_n, n}`.
- `e_bid <= J'_n L_n <= 2^D n^{D/(D+3)} (n^{2/(D+3)} + 1) <= 2^{D+1} n^{(D+2)/(D+3)}`.
- `e_stage1 <= K e_bid <= K 2^{D+1} n^{(D+2)/(D+3)}`.
- `e_osc = n rho_n = sqrt(D) n h_n log(en) <= sqrt(D) n^{(D+2)/(D+3)} log(en)`, using `h_n <=
  n^{-1/(D+3)}`.
- `n s_n = n sqrt(ell_n / (2 L_n)) <= sqrt(ell_n/2) n^{(D+2)/(D+3)}`, so
  `e_price <= (4 sqrt(ell_n/2) + (4/3) sqrt D log(en)) n^{(D+2)/(D+3)}`.
- `e_mon <= J'_n + 2 sqrt(J'_n n ell_n/2) <= 2^D n^{D/(D+3)} + 2^{D/2+1} sqrt(ell_n/2)
  n^{(2D+3)/(2D+6)}`.
- `e_fb <= 11 sqrt(2 K log K) 2^{D/2} n^{(2D+3)/(2D+6)} + 2^{D+1} K log K n^{D/(D+3)} log_2(2(n+1))`.

The three exponents that occur are `(D+2)/(D+3) = (2D+4)/(2D+6)`, `(2D+3)/(2D+6)` and `D/(D+3)`,
and the first strictly dominates the other two. So every error term is
`O( n^{(D+2)/(D+3)} log(e K n) )` with constants depending only on `K` and `D`, and on nothing else.
I confirm the claimed exponent, and I confirm that it matches `thm:grid-etc`'s
`n^{(D+2)/(D+3)}` exactly. It does **not** match the manuscript's headline public contextual rate,
which is `thm:grid-ucb-robust` at `n^{(D+1)/(D+2)}` and is strictly smaller; see Section 19.1. The balance that produces it is three way and is worth recording:
elicitation `J_n L_n = n^{(D+2)/(D+3)}`, price slack `n s_n = n^{(D+2)/(D+3)}`, oscillation
`n h_n log n = n^{(D+2)/(D+3)} log n`, which is exactly the Grid-ETC balance `h_n = n^{-1/(D+3)}`,
`q_n = n^{2/(D+3)}` with `L_n` in the role of `q_n`. That coincidence is a good sign rather than a
coincidence: both mechanisms spend `q` or `L` observations per cell on a `J`-cell grid and pay a
Lipschitz discretisation error.

**Instance constants.** None of the seven displayed bounds contains `L`, `mu`, `M`, a capacity gap,
a mass, or any property of the law of `A`. The only instance dependent hypothesis is
`log(en) >= 3 L` in (A2). I confirm the uniformity claim of Section 6 of the report, with the
qualification in Section 10 below.

## 10. The four questions I was asked to settle for myself

### 10.1 The counterfactual bid in the good event

**Verdict: the distinction is correct, and it is also unnecessary, which is a stronger answer.**

The two objects are genuinely different. The deviator's **actual** bid `beta'_{i,C}` cannot
concentrate around its capacity average: the deviator chooses what it delivers, and by delivering
zero it can force `beta'_{i,C} = 0` while `Mbar_{i,C} = 1`. The **counterfactual** bid
`beta^cap_{i,C}` is, under Fact 1, a measurable function of `A` and of the seeds at the
`F_0`-measurable rounds `t_{i,C,r}` alone, so it is defined on the same draw in both executions,
its law does not depend on the deviation, and `{|beta^cap_{i,C} - Mbar_{i,C}| <= s_n}` is a
behaviour independent event of probability at least `1 - (K n^5)^{-1}`. Putting it in the good
event is legitimate. It is an analyst's object, not an agent's observable, and the deviation class
`B^ctx+` being large enough to see the whole arrival path does not touch it: the class governs what
the agent may condition on, not which random variables the analysis may name. The two properties
the framing identifies as necessary are exactly the right two, and the mechanism has both: the
Stage-1 schedule reads only `A` (Fact 1, design point 2 of Section 3 of the report), and the seeds
are indexed by round, which under Fact 1 coincides with indexing by (agent, cube, local pull), so
the counterfactual is well defined on the same draw. I checked this against the mechanism text and
it holds.

I nevertheless do not use it, because the conclusion Lemma P2 needs about a deviator is one sided,
and a one sided bound on the **actual** bid is available with no counterfactual at all:

    beta'_{i,C}  <=  Abar'_{i,C} + s_n        (Azuma, Lemma P1, uniform over the deviation class)
                 <=  Mbar_{i,C} + s_n         (feasibility, (3.1)) .

"The deviator's bid cannot concentrate" is true two sidedly and false one sidedly. Only the one
sided half is ever needed: no argument in parts (A), (B) or (C) requires a **lower** bound on a
deviator's own bid. That is the whole content of my divergence from the report. The advantages of
my route are that it names no object that does not occur in the deviating execution, that it needs
no second execution for Lemma P2 (the coupling is then used only for bid domination, which is a
pathwise inequality), and that the same lemma serves part (C), where every agent may deviate and
there is no baseline execution to be counterfactual with respect to.

**On `sections/appendix_private.tex` line 99.** My reading, reached independently, is that the
sentence "No concentration around the deviator's capacity is invoked" is a statement of what the
proof happens to use, not a warning. It is literally accurate about the manuscript's good event
`G_{-i}`, which excludes `i`. It is not a reason: adding the deviation independent event
`{|beta_i^max - M_i| <= s_n}` is sound, and so is my version, which adds instead the deviation
uniform event `{beta'_i <= (average of i's realised Stage-1 targets) + s_n}`. So the by product of
`EXPLORER.md` Section 7.4 survives. I re-derived it directly in the scalar model:

> In `thm:private-mesp`, add to the good event `G_{-i}` the event
> `{beta'_i <= L_n^{-1} sum_r m'_{i,r} + s_n}`, which has probability at least `1 - (2 K n^4)^{-1}`
> by Azuma for the predictable targets `m'_{i,r}`, uniformly over `B_{i,n}`. Since
> `L_n^{-1} sum_r m'_{i,r} <= M_i` by feasibility, on that event `beta'_i <= M_i + s_n`. If `i`
> wins, `beta_(2) = max_{j != i} beta_j <= beta'_i`, so `tau_i = (beta_(2) - s_n)_+ <= M_i`. Hence a
> winning deviator can always meet the price, `S^*_i` delivers `min{tau_i, M_i} = tau_i`, the
> baseline does not switch, and the comparison of the top branch applies verbatim. The non-top
> branch of `sections/appendix_private.tex` (the paragraph beginning "If `i` is non-top") is then
> never entered, and the deviation bound becomes `L_n + 1 + 2 b_n(n) + R_K(n) + O(n^{-3})` with no
> `delta_i` and no threshold `4 s_n <= delta_i`.

Two cautions before the manuscript acts on this. First, the non-top branch would still be needed if
one wanted a bound for an agent that **loses** and then receives fallback pulls at a price above its
capacity; I checked that branch and it is already covered by the losing-history paragraph, whose
bound `2n(n^{-4} + (2n^3)^{-1})` does not use `delta_i`. Second, `eq:private-fallback-low` and the
quantity `delta_i` are cited elsewhere in the audit tree (PROVER1's `D_i(z)`, PROVER2's `e_low`);
deleting them from the scalar appendix requires those to be revisited, which is outside my scope.

### 10.2 Is dropping i.i.d. genuine, or hidden elsewhere?

**Genuine.** I traced every step of my own derivation for a use of the law of `A` and found none.
Conditionally on `A`, the following are deterministic: the grid, `J'_n`, each `V_C`, each `n_C`,
every Stage-1 round and its assigned agent, every `Mbar_{j,C}`, every `M_j^inf(C)`, `v_C`, `h_C`.
The only probabilistic inputs are the seeds and the coins, which are independent of `A` by (A3) and
(A4). Every bound in Sections 3 to 9 is therefore uniform in `A`, and integrating over any law of
`A` (i.i.d. or not, with a density or not, deterministic or adversarially chosen in advance) is a
single application of the tower property. The benchmarks are stated pathwise as
`E sum_t M_(2)(X_t)` and `E sum_t b(X_t)`, so they too need no law.

Compare where i.i.d. is used in the manuscript (contract Section 11): `lem:cell-law`, which says
that within a cell the profiles are i.i.d. `nu(.|C)` and that a cell-blind agent's rewards are
i.i.d. Bernoulli at the cell mean. That lemma is needed because Grid-UCB1 and Grid-ETC **estimate a
conditional cell mean and then act on it as if it were a per cell constant**. CG-MESP never does
this. Its bid is compared only with the average capacity **at the very pulls that produced it**
(`Mbar_{j,C}`, a within sample quantity), and the passage from that average to the value at an
arbitrary context of the cube is made by the Lipschitz property, not by a sampling argument. That
is the structural reason i.i.d. is not needed, and I regard it as the most interesting thing in the
construction.

Two checks that the removal is not hidden. (i) A path that starves cubes: an adversary could give
every cube `K L_n - 1` visits so that no cube ever awards and the mechanism only elicits. The total
number of rounds it can waste this way is at most `J_n (K L_n - 1) <= K 2^{D+1} n^{(D+2)/(D+3)}`,
which is exactly `e_stage1` and is `o(n)`. The fixed grid caps the damage; the guarantee does not
become vacuous. (ii) A path that concentrates everything in one cube gives `J'_n = 1` and the three
bounds degrade gracefully to the scalar MESP rates `L_n + O(sqrt(n log n))`. Both checks pass.

What is **not** dropped is exogeneity. (A3) requires `A` to be independent of the seeds and coins,
that is, arrivals that do not react to rewards. This is strictly weaker than i.i.d. and strictly
stronger than nothing, and it is indispensable twice: Fact 1 (without it the two coupled executions
need not have the same Stage-1 rounds, and bid domination fails) and the predictability of `psi_s`
in Lemma P6. So the honest statement is "i.i.d. is replaced by exogeneity", not "no assumption on
arrivals".

### 10.3 Is the oscillation allowance correctly sized?

**Sufficient, necessary in order, and not tight.**

*Sufficient.* Every use of the allowance in my derivation is an application of Fact 0 with a single
factor `omega = L sqrt(D) h_n <= rho_n/3`: Lemma P2 (once), Lemma P3 (once), Lemma P4 (once),
Lemma P5(i) (once), Lemma P8 (once, for `M^sup - M^inf`), and Section 6's `mu_i^sup <= mu_i^inf +
rho_n/3` (once). None of these is ever compounded, so `rho_n/3 >= omega` is the only requirement
and (A2) delivers it.

*Necessary in order.* The shading must dominate the within cube oscillation. If
`sigma_n < omega - s_n` then on the good event one can have `tau_C > M_W(x_W)` at some contexts of
the awarded cube: the winner's bid reflects the average of its capacity over the Stage-1 contexts,
and a Lipschitz capacity may be up to `omega` lower elsewhere in the cube. At such a context `S^*`
is infeasible, the compliant winner must under deliver, the monitor may eject an agent that is
behaving exactly as the mechanism asked, and both the equilibrium comparison (the baseline no
longer survives at the cube) and the revenue identity fail. So an allowance of order `L h_n` is
not an artefact. Since `L` is unknown to the platform (A6), the allowance must be `h_n` times a
factor that diverges, and `log(en)` is the cheapest such factor that keeps the rate at
`n^{(D+2)/(D+3)}` up to a single logarithm.

*Not tight.* I could not find any use of the extra `2 s_n + (2/3) rho_n` in
`sigma_n = 3 s_n + rho_n`. All three parts go through with `sigma_n := s_n + rho_n/3`, which would
reduce `e_price` and the part (C) slack from `n(4 s_n + (4/3) rho_n)` to `n(2 s_n + (2/3) rho_n)`.
I did not change the mechanism, because a larger shading is safe and the rate is unchanged; I
record it because a referee may ask why the constant is `3`.

*A practical caveat that is not a correctness issue.* `sigma_n > 1` for every horizon anyone can
simulate (`EXPLORER.md` Section 10.1 records this, and it is easy to check: `s_n` alone exceeds
`0.3` for `n = 10^6`, `K = 2`, `D = 2`). Then `tau_C = 0` identically, `S^*` is "deliver nothing",
revenue is zero and the revenue bound holds vacuously because `e_price >= n`. The theorem is not
wrong; it is asymptotic in a strong sense, and the manuscript must say so if it uses this result.

### 10.4 Uniformity over instances

**Confirmed, with one qualification that should be stated.** No bound in parts (A), (B), (C)
contains an instance quantity; the constants depend only on `K` and `D`. The only instance
dependence is the hypothesis `n >= exp(3 L)` in (A2), and this is a hypothesis of a different kind
from the scalar theorem's `4 s_n <= delta_i`: the scalar bound **contains** `delta_i` (through
`log n / delta_i^2` and `R_K(n)/delta_i`), whereas here `L` appears nowhere in the bound. So the
claimed improvement is real.

The qualification is that `exp(3 L)` is a severe threshold, exponential in the Lipschitz constant,
whereas the natural scale at which a grid argument becomes meaningful is polynomial: one needs
`L sqrt(D) h_n <= 1`, that is `n >= (L sqrt D)^{D+3}`. The gap is an artefact of using `log(en)` as
the `L`-free surrogate. `EXPLORER.md` Section 7.5 item 5 records the trade (use
`rho_n = sqrt(D) h_n (log en)^{1+a}` to weaken the threshold to `(log en)^{1+a} >= 3L` at a
`(log n)^a` cost), and I add the cheaper alternative: `rho_n := sqrt(D) h_n n^{a/(D+3)}` for small
`a > 0` gives the polynomial threshold `n^{a/(D+3)} >= 3 L` at the cost of raising the exponent from
`(D+2)/(D+3)` to `(D+2+a)/(D+3)`. If the paper claims uniformity over instances, it should say
which of the three it means, because "uniform over all `L`-Lipschitz instances for
`n >= exp(3L)`" is a weaker sentence than it looks.

## 11. Numerical falsification attempt against the two price lemmas

The two price lemmas concern bidding only, and by Fact 2 cubes are independent given the arrival
path, so they can be tested directly without simulating rounds. Scripts:
`<scratchpad>/round2/f1-prover2/price_lemmas.py` and `.../threshold.py`; run on the login node with
the project venv, a few seconds each, no Slurm job submitted, so there is nothing to add to a
compute log. Constants are recalibrated (the honest `s_n`, `rho_n` are numerically vacuous at every
simulable horizon, `EXPLORER.md` Section 10.1); the experiment tests the inequalities, not the
rates.

Setting 1: `K = 3`, `d = 1`, `D = 3`, `L = 2`, cube side `h = 0.05`, `L_n = 4000`, 4000 cubes,
oscillating `L`-Lipschitz capacities, `omega = L sqrt(D) h = 0.173`, `s_n = 0.046`.

Violations, out of 4000 cubes, of Lemma P2 (`tau_C <= min_{X in C} M_W(x_W)`) and of Lemma P4:

* `sigma = s_n + omega`: P2 violations 0, P4 violations 0.
* `sigma = 3 s_n + 3 omega` (as specified): P2 violations 0, P4 violations 0.
* `sigma = s_n` only, no oscillation allowance: **P2 violations 367**, P4 violations 0.

With a deviating agent that shades its Stage-1 delivery to `min{M, 0}` or `min{M, 0.3}` at every
cube, Lemma P2 held at all 4000 cubes under the specified shading. This is the case my Lemma P1
covers and the explorer's Lemma 5 covers through the counterfactual; both predict no violations,
and none occurred.

Setting 2 (sharper necessity test): `K = 2`, exactly tied base capacity levels so that the second
bid is as close to the winner's as the instance allows, monotone `L`-Lipschitz capacities so the
within cube oscillation is fully realised, `L_n = 8000`, `omega = 0.141`, `s_n = 0.033`, 6000
cubes. Violation rate of Lemma P2: `0.027` at `sigma = s_n`, `0.006` at `sigma = s_n + 0.1 omega`,
`0` from `sigma = s_n + 0.2 omega` upward.

Conclusion of the experiment: the oscillation allowance is not decorative. Removing it breaks
Lemma P2 at a percent level rate on ordinary instances, and Lemma P2 is what every distinctive
claim of Theorem 1 rests on. The observed threshold is below my sufficient condition
`sigma >= s_n + omega`, as it should be: the worst case needs `sigma` of order `omega/2` (monotone
capacity, bids nearly tied) and the typical case needs less. This is evidence for sufficiency and
for necessity in order, and it is not evidence about the rates.

## 12. Defects found in `EXPLORER.md`

**D1 (P2). `EXPLORER.md` Lemma 6(a): the monitoring union bound is not valid as argued, and the
stated probability is wrong by a factor `n`.** The proof counts "at most `n` pairs `(C,r)` because
`sum_C (Stage-2 pulls at C) <= n`", but the number of Stage-2 pulls at a cube is a random variable
and a union bound cannot be taken over a random index set on that basis. The correct count is at
most `n` visited cubes times `n` values of `r`, giving `Pr(H^c) <= 2 n^2 e^{-ell_n} = n^{-3}/K`,
not `n^{-4}`. Consequence: the additive constants `6 n^{-3}` in part (A) and `3 n^{-3}` in parts
(B) and (C) become `O(n^{-2})`, which is still smaller than every other term by a factor
`n^{2 + (D+2)/(D+3)}`. Minimal repair: set `ell_n := log(2 K n^6)`, which restores every stated
constant and changes only the numbers inside logarithms. Affected: Theorem 1 (A), (B), (C) as
displayed in Section 6 of that report. The same repair absorbs the extra factor `J_n` that appears
in Lemma P6c of Section 17.1, where the union runs over the deterministic grid of cubes rather than
over the visited ones.

**D2 (P2). `EXPLORER.md` Section 7.1, paragraph "Where each event is used": the claim that `G` is
`F_fb`-measurable at every cube is false.** `G` is an intersection over all cubes of events about
Stage-1 data at those cubes, and the Stage 1 of a cube `C''` may still be running when cube `C`
switches to fallback, because cubes are visited in an interleaved order determined by `A`. So `1_G`
is not measurable with respect to `C`'s fallback start field and the identity
`E[U'^fb_{i,C} 1_G] = E[1_G E[U'^fb_{i,C} | F_fb]]` is not justified as written. The same defect
recurs in Section 7.3, where `G_H` and `H` are used globally inside conditional statements from
Lemma 7. Repair, one line: replace `G` by its cube `C` component `G_C` and `H` by `H_C` in every
conditional step. `G_C` is measurable in the rewards at `C`'s Stage-1 rounds and `H_C` is
determined at `C`'s switch round, so both are in `C`'s fallback start field, and since
`U'^fb_{i,C} >= 0` one has `E[U'^fb 1_G] <= E[U'^fb 1_{G_C}] = E[1_{G_C} E[U'^fb | F_fb]]` for the
upper bound and the analogous inequality for the lower bounds in parts (B) and (C). The complement
is then charged per cube, `sum_C n Pr(bad_C) = O(n^{-2})`, which is the same `O(n^{-2})` as in D1.
The theorem is unaffected. I used the per cube form throughout Sections 6 to 8 above, so my proof
does not inherit this defect.

**D3 (P3). `e_rob` is loose.** My Section 8 gives `n(4 s_n + (4/3) rho_n)` where the report states
`n(4 s_n + (5/3) rho_n)`. The report's statement is implied by mine, so this is a constant that can
be improved, not an error.

**D4 (P3). The shading constant `3 s_n` is unused.** All of Lemmas P2, P3, P4 and P5 go through
with `sigma_n = s_n + rho_n/3`. Keeping `3 s_n + rho_n` is safe and costs only a constant factor in
`e_price` and in the part (C) slack, but a referee will ask, and the report's explanation ("the
`3 s_n` pays for two bid radii and for the counterfactual bid of a deviator") does not match its
own proofs, each of which spends exactly one `s_n`.

**D5 (P3). Part (B) as stated in the report omits the reason no fallback term appears.** It is
correct that none is needed, because on the good events `S^*` never triggers a switch (Consequence
C1 plus Lemma 6(d)), but the report's part (B) never says so and a reader will look for a
`sum_C R^dbl_K` term. One sentence.

I found no defect in Lemmas 2, 3, 4, 5, 7, 7b, 8 or 9 of `EXPLORER.md`, and none in Sections 7.2
or 7.4. In particular I checked Lemma 4(c) (the tie break argument for winner inclusion), Lemma
5's three inequalities, consequence (C3), Lemma 7b's replacement of `Qbar_i` by `H_C`, the Cauchy
and Schwarz steps, and the arithmetic of part (D); all are correct.

**D6 (P3, hypothesis wording). (A3) should say that the law of the arrival path does not depend on
the strategy profile.** "Exogenous" is intended to mean this, and the proof needs it: the
equilibrium statement compares `u_i(n; S'_i, S^*_{-i})` with `u_i(n; S^*)`, and both are integrals
over `A`. My bounds are uniform in `A`, so an arrival path chosen adversarially in advance is
covered, but only if it is the **same** path in the two executions. A path whose law reacted to the
declared profile would make the two expectations integrate different laws and the comparison would
not follow from a per path bound. One clause in (A3).

## 13. Where the two proofs coincide and where they diverge

**Coincide** (same idea, independently reached, and I believe both): the cube locality
decomposition; the pathwise bid domination and winner inclusion (my Section 2 and 6(6.1) versus
Lemma 4); the shape of the good event as a per pull Hoeffding or Azuma statement at the
`F_0`-measurable Stage-1 rounds; the price lemma's conclusion `tau_C <= M_W(x_W)` at every context
of the cube and its two consequences; the comparator lemma `tau_C <= nu_i(C)` (my P3 versus C3);
the monitor and its four consequences; the doubling epoch fallback with the constant
`3(2 + sqrt 2) <= 11`; the deviator's fallback bound with `Qbar_i` replaced by `H_C`; the three
part accounting and the two Cauchy and Schwarz steps; part (B) via `P = E sum_t m_{I_t,t}` rather
than optional stopping; part (C)'s two cases and the honest comparator; and every exponent in part
(D). Where the two routes coincide they coincide in substance and not only in conclusion, and in
those places I regard the result as having two proofs.

**Diverge, and which I believe.**

1. *The good event.* The report puts the deviator's counterfactual capacity bid `beta^cap_{i,C}` in
   `G`; I put a one sided Azuma bound on the deviator's realised bid in `E_C`. **Both are correct**
   (Section 10.1). I prefer mine because it names no object outside the deviating execution and it
   is the same lemma that part (C) needs when all `K` agents deviate; the report needs a separate
   event `G_H` there. If a referee rejects the counterfactual, Theorem 1 is unharmed: my Lemma P1
   replaces it verbatim, with the same constant.
2. *Global versus per cube conditioning.* The report conditions on global `G` and `H` inside
   statements that are conditional on a cube's fallback start field; I use `E_C` and `H_C`. **Mine
   is correct and the report's is not, as written** (defect D2); the repair is one line and does not
   change the statement.
3. *The monitoring union bound.* Defect D1. **Mine is correct**; the report's constant needs
   `ell_n = log(2 K n^6)`.
4. *Constants in `e_rob` and in `sigma_n`.* Defects D3 and D4. Mine are smaller; neither matters to
   the rate.

## 14. The step I consider least secure, and what survives if it fails

**Least secure: the `F_0`-measurability of the arrival path (Convention A), on which two different
things depend at once.** It is what makes `psi_s` predictable in Lemma P6, so that the monitor is a
martingale test, and it is what makes the Stage-1 rounds identical across the two coupled
executions in Fact 1, so that bid domination is pathwise and the bidding concentration event is
about a deterministic index set. If arrivals could react to rewards, both fail simultaneously:
`psi_s` acquires a dependence on `X_s` that is not in `F_{s-1}`, and the deviator can move its own
Stage-1 rounds by moving the arrival process, which destroys the coupling that gives (6.1). This is
the same step `c2-local-mesp/PROVER2.md` names as its least secure one, and the adversary's finite
case construction (reported there as ADVERSARY Section 7.1) shows the finite theorem is false
without it, not merely unproved. (A3) licenses it, and (A3) is a real restriction that the paper
must state prominently, because the headline "no i.i.d. arrivals" will be read by referees as "no
assumption on arrivals".

**I do not consider the counterfactual bid the least secure step**, which is my main disagreement
with the explorer's self assessment. It is sound, and in any case it is removable. Its removal is
the single most useful thing in this report: it means the conclusion that Theorem 1 loses its
uniformity over instances if the counterfactual falls (the explorer's own contingency) does not
arise.

**Second least secure: Lemma P8 composed with the per cube accounting of Section 6**, the step that
replaces `Qbar_i` by `H_C` using `1 + mu_i^sup(C) - nu_i(C) >= 0` inside a conditional expectation
multiplied by the indicator of `E_C cap H_C`. I checked the measurability (Section 6, "Legitimacy
of the conditioning") and I believe it, and it is the place where the two coupled executions, a
conditional expectation and an event interact. It is the same step the explorer lists third. A
third reader should look there.

**Third: the hypothesis `n >= exp(3L)`** (Section 10.4). It is a hypothesis, not a gap, but it is
the place where "uniform over instances" is doing less work than it sounds.

**What survives if Convention A fails.** Everything except (A3) free arrivals. With i.i.d. arrivals
independent of the seeds, `psi_s` predictability and Fact 1 both hold by the same argument (i.i.d.
arrivals are exogenous), so Theorem 1 holds verbatim with i.i.d. arrivals. So the fallback position
is: the same three parts, the same exponent, the same absence of instance constants, under the
manuscript's existing i.i.d. assumption. Only the "no i.i.d." headline is at risk, and only if a
referee disputes exogeneity itself.

## 15. What I did not do

1. I did not verify Sections 2, 8, 9 or 10 of `EXPLORER.md`, and nothing above depends on them. In
   particular I take no position on Proposition 4, on PA-MESP, on the `d` versus `D` comparison, or
   on the correction to the sceptic's Section 2.2.
2. I did not prove a lower bound, and I did not verify the tightness claim of `EXPLORER.md`
   Section 7.5 item 2 in detail. I note that the obvious tightness construction (shade every
   Stage-1 delivery to the midpoint between the top two capacities) needs the top gap to exceed the
   shading plus the oscillation, so the **lower** bound carries an instance constant even though the
   upper bound does not. The statement "the rate is attained" therefore needs an instance quantifier
   that the theorem itself does not.
3. I did not run the mechanism end to end. My numerical work (Section 11) tests the two bidding
   lemmas only, at recalibrated constants.
4. I did not check the consequences of deleting the non-top branch from the scalar appendix for the
   other audit files that cite `delta_i`.
5. I did not check anything about anytime horizons, non-Lipschitz capacities, or arrivals that
   react to rewards.

## 16. Bottom line (original; superseded by Section 20)

I proved parts (A), (B) and (C) of Theorem 1 from the mechanism specification, by a route that
diverges from the existing proof at its own declared weakest step, and I obtained the same three
statements at the same exponent `O(n^{(D+2)/(D+3)} log(e K n))`, with no instance constant in any
bound, without i.i.d. arrivals and with no top set, boundary, mass or component condition. I
believe the theorem is correct. I do not claim it is correct: the two places a third reader should
attack are Convention A (Section 14) and the composition of Lemma P8 with the per cube conditioning
(Section 6). Two defects in the existing write up (D1, D2) are real and must be fixed before the
proof is used, and neither changes the statement.

*Superseded.* Three of the sentences above are withdrawn in Revision 2: "no top set, boundary, mass
or component condition" (Section 19.2), the implied exponent comparison (Section 19.1), and the
ranking of Convention A as the place to attack (Section 20). The corrected bottom line is at the end
of Section 20.

# Revision 2, after `ADVERSARY.md` (18 September 2026)

Sections 1 to 16 above are my original derivation, with three corrections made in place and marked
as such: the mutual independence hypothesis in Section 2, the `H^*_C` measurability defect in
Section 6 (the adversary's G5, which is my error and not the explorer's), and the pointer at
Lemma P6. Sections 17 to 20 are new. Section 17 carries out the two upgrades the adversary
identified and did not write. Section 18 computes the horizons. Section 19 withdraws framing. I no
longer claim the agreement of the two proofs is strong independent evidence; Section 6's correction
and the adversary's G2 show the two routes share an upstream error and make the same-shaped
mistake in complementary places.

## 17. The two upgrades: what each part actually needs from the arrival process

### 17.0 The half step, and the weakened hypothesis

Everything in this section rests on one observation: every conditional mean zero step in this proof
is a statement about a seed given everything determined before that seed, and the arrival of the
round is determined before the seed. So the natural conditioning field is not `F_{s-1}` but a field
half a step later. Define, at round `u`,

    G_u^{0}  := sigma( G_{u-1}, X_u )                       (post arrival)
    G_u^{1}  := sigma( G_u^{0}, Pi_{C(X_u)} if drawn at u )  (post priority draw)
    G_u^{2}  := sigma( G_u^{1}, I_u )                        (post selection)
    G_u^{-}  := sigma( G_u^{2}, the selected agent's coin at u, m_{I_u,u} )   (pre seed)
    G_u      := sigma( G_u^{-}, U_u ) .

Throughout the lemma proofs below I write `G_u^{--} := G_u^{0}` for the post arrival field, which is
the symbol the first version used and which is the conditioning field of every indicator.

**REVISION 3. The hypothesis is now written in conditional form, over every draw and not only the
seed.** The first version of this section wrote

> (A4c) For every round `u`, conditionally on `G_u^{-}` the seed `U_u` is uniform on `[0,1]`, and
> `Y_u = 1{U_u <= m_{I_u,u}}`,

and then asserted in 17.6 that parts (B) and (C) need "nothing further". That is false, and the
adversary's H1 is a counterexample to it: (A4c) constrains the **seed** and says nothing about the
**mechanism's own randomisation**, while Lemma P7c's proof uses the freshness of the fallback
selection coin. The witness makes the arrival path a function of that very coin: `K = 2`, constant
primitives so (A1) and (A2) are vacuous, seeds i.i.d. and independent of everything so (A4c) holds
exactly, and a path that routes into a cube precisely when that cube's fallback would select the
strategic agent from the round's coin. The honest agent is then never selected at that cube, its
EXP3 weight never updates, `p` stays uniform, every pull there delivers `0`, and the lemma's
promised `0.9 E[H_C] - E[R^dbl_K(H_C)] = 0.45 n - O(sqrt n)` is actually `0`. Theorem 1C upgraded
fails by about `0.45 n` against a budget `O(n^{4/5} log n)`. I checked the instance: the path is
well defined because the cube's fallback weight vector is a function of that cube's own past and is
available before the round, and once `X_u` is a function of the coin, that coin is
`G_u^{0}`-measurable, `E[1{I_u = j} | G_u^{0}]` is `0` or `1`, and the importance weighted estimator
is not conditionally unbiased. The finding is correct and the failure is mine.

**This is the third time in this project that a probabilistic hypothesis written as a list of
clauses has omitted a family that a proof then used**: the finite documents' hypothesis list, the
continuous documents' (A3) and (A4), and now (A4c), which was itself written to repair the second.
A list can omit a family; the conditional form cannot, because it quantifies over everything
realised before the draw rather than enumerating what the draw is independent of. So the hypothesis
below is written once, in that form, over every draw made at a round, and the list form is not used
anywhere in this document.

> **(A4f) Fresh draws.** At every round `u` the following are drawn in the order shown, and **each
> one has its specified law conditionally on the sigma-field generated by everything realised before
> it**, that field containing `G_{u-1}`, the arrival `X_u`, and whichever of the draws below have
> already been made at round `u`:
>
> (f1) the priority permutation `Pi_{C(X_u)}`, if the cube `C(X_u)` is met for the first time at
>      round `u`: uniform on the permutations of `[K]`;
> (f2) the mechanism's selection: in Stage 1 and Stage 2 the deterministic function of the cube's
>      state that the mechanism specifies, and in Stage 3 a draw `I_u` with the law `p_u` computed
>      from the cube's own EXP3 state;
> (f3) the seed: `U_u` uniform on `[0,1]`, with `Y_u = 1{U_u <= m_{I_u,u}}`.
>
> The selected agent's private randomisation and its target are drawn between (f2) and (f3) and are
> unconstrained: whatever the agent's strategy specifies, they are part of "everything realised
> before" the seed, and (f3) is stated conditionally on them.

Four remarks, and they are the point of the whole section.

1. **(A4f) is the manuscript's own scalar phrasing, extended to every draw.** The scalar theorem
   assumes "targets are chosen before fresh conditionally independent Bernoulli seeds"
   (`sections/Private_information_setting.tex`). (A4f) says the same thing about the seed and says
   it also about the mechanism's two draws. Every defect of this kind on this project has come from
   reassembling that sentence as a list instead of copying its form.
2. **(A4f) repairs G1.** In that instance `U_t = frac(x_{1,t} + c_t)` is, conditionally on
   everything realised before the seed (which contains `x_{1,t}` and the deviator's coin `c_t`), a
   point mass, so (f3) fails, as it must.
3. **(A4f) repairs H1, and repairs it against variants I looked for.** The witness has `X_u` a
   function of the round's fallback coin, so conditionally on the field containing `X_u` that coin
   is degenerate and (f2) fails. A path that instead depended on a **future** coin is excluded too,
   at the later round: at round `u+1` the draw must be fresh given everything realised before it,
   which contains `X_u`, and `X_u` is a function of that draw. This is what the conditional form
   buys over a list: I do not have to enumerate the channels.
4. **(A4f) still says nothing about the arrival path.** `X_u` may be an arbitrary measurable
   function of the entire past, including past rewards and past coins, plus fresh randomness,
   provided only that it is realised before the round's own draws. It need not be i.i.d., exogenous,
   independent of the seeds, or independent across rounds. I keep the name **nonanticipating** for
   such a path, but I no longer say "with respect to the seeds": the correct phrase is
   **nonanticipating with respect to the round's own draws**.

**Which clause each lemma uses.** This is the table the first version should have carried.

* Fact 0, Lemma P2, Lemma P3, Lemma P4, Lemma P5(i) and P5(ii): **nothing probabilistic**. All are
  pathwise consequences of `E_C`, of Lipschitz continuity or of honesty, and all hold for whoever
  wins, so no property of the tie break is used.
* Lemma P1c (bidding concentration) and Lemma P5(iii): **(f3) only**. The Stage-1 selection is the
  deterministic branch of (f2) and contributes no randomness.
* Lemma P6c (monitor): **(f3) only**. The Stage-2 selection is again the deterministic branch.
* Lemma P7c (fallback): **(f2) Stage-3 branch and (f3)**. This is the lemma H1 attacks, and (f2) is
  exactly the clause it needs.
* Part (B): **(f3) only**, as verified below and independently by the adversary.
* Part (C): **(f2) Stage-3 branch and (f3)**.
* Part (A): all of (A4f), **and in addition** that a deviation cannot move the arrival path
  (Section 17.4).
* **(f1) is used nowhere in parts (B) and (C).** The priority permutation enters only through tie
  breaks, and every lemma that mentions a winner is stated for whoever wins. It is in (A4f) because
  a hypothesis should cover every draw the mechanism makes, not because a proof below needs it; part
  (A) uses the permutation only through the coupling, which is an identity of two executions on one
  space rather than a statement about its law.

**One restriction that comes with it, and it is forced.** Under (A4f) alone the deviation class
must be the contract's `B^ctx_{i,n}`, in which an agent conditions on its own history, the current
profile and the past path, but not on the future path. The larger class `B^ctx+_{i,n}`, in which
an agent conditions on the entire arrival path, is not well posed when arrivals react to rewards:
`X_{u+1}` would be a function of `Y_u`, `Y_u` a function of `m_{i,u}`, and `m_{i,u}` a function of
`X_{u+1}`. This is the adversary's G4 and it is correct. So the two relaxations the headline
advertises are not independent, and the upgrades below are stated for `B^ctx`, with `B^ctx+`
available only under exogeneity.

### 17.1 The monitor, with no property of the arrival path (Lemma P6 restated)

**Lemma P6c.** Assume (A4f); this lemma uses clause (f3) only. Fix a cube `C` of the grid and `r <= n`. With `Z_r`, `A_r`,
`b_n(r)` as in Lemma P6 and the same extension by zero increments,
`Pr( |Z_r - A_r| > b_n(r) ) <= 2 e^{-ell_n}`, and consequently
`Pr( H^c ) <= 2 J_n n e^{-ell_n} <= n^{-3}/K`. Parts (b), (c), (d) of Lemma P6 are unchanged, being
pathwise consequences of the event, and part (e) holds with the same proof.

*Proof.* Let `psi_s := 1{round s is a Stage-2 pull at C}`, let `T_r` be the round of the `r`-th such
pull (`T_r := n` if there are fewer than `r`), and put `phi_s := psi_s 1{s <= T_r}`. Then `phi_s` is
`G_s^{--}`-measurable, hence `G_s^{-}`-measurable: whether round `s` is a Stage-2 pull at `C` is
determined by `X_s`, which `G_s^{--}` contains, by the visit count of `C`, which is determined by
`X_1,...,X_s`, and by whether `C` has awarded and not yet switched, which is a function of rewards
at rounds strictly before `s`; and `{s <= T_r}` says that fewer than `r` Stage-2 pulls at `C` have
occurred before `s`, again a function of the past. **No claim is made that `phi_s` is
`G_{s-1}`-measurable, and none is needed.** Put
`M_t := sum_{s <= t} phi_s (Y_s - m_{I_s,s})`, `c_t := sum_{s <= t} phi_s`, and for `lambda` real

    N_t := exp( lambda M_t - (lambda^2/8) c_t ) ,   N_0 := 1 .

`N_{t-1}`, `phi_t` and `m_{I_t,t}` are all `G_t^{-}`-measurable, and by clause (f3) the conditional law of
`Y_t` given `G_t^{-}` is Bernoulli(`m_{I_t,t}`), so `Y_t - m_{I_t,t}` has conditional mean zero and
conditional range `1`; Hoeffding's lemma gives
`E[ exp( lambda phi_t (Y_t - m_{I_t,t}) ) | G_t^{-} ] <= exp( lambda^2 phi_t / 8 )` (the case
`phi_t = 0` is trivial). Hence `E[N_t | G_t^{-}] <= N_{t-1}` and `E[N_n] <= 1`. Under the zero
extension `M_n = Z_r - A_r` and `c_n <= r`, so
`E[ exp(lambda (Z_r - A_r)) ] <= exp(lambda^2 r/8) E[N_n] <= exp(lambda^2 r/8)`, and Markov with
`lambda = 4 b_n(r)/r` gives `Pr( Z_r - A_r > b_n(r) ) <= exp(-2 b_n(r)^2/r) = e^{-ell_n}`; the lower
tail is symmetric. The union bound now runs over the **deterministic** set of `J_n` grid cubes and
`r <= n`, which is why no measurability of the set of visited cubes is needed either. `QED`

This is the adversary's G2, which is in turn the finite-context adversary's F3 transferred to the
cube monitor; I re-derived it rather than importing it, and it is correct. Both provers, including
me, ranked this step as the least secure in the theorem and attributed it to exogeneity. That was
wrong, and it was wrong in the same way in both documents, which is evidence that the two proofs
share an upstream source and are not as independent as their agreement suggests.

### 17.2 The bidding concentration, with no property of the arrival path (Lemma P1 restated)

**Lemma P1c.** Assume (A4f); this lemma uses clause (f3) only. For every cube `C` of the grid that
completes bidding, and every agent `j` (the bid `beta_{j,C}` is defined only on that event, and the
statement is vacuous off it),
`Pr( |beta_{j,C} - Abar_{j,C}| > s_n ) <= 2 e^{-ell_n}`, whatever strategies all `K` agents use,
so `Pr(E_C^c) <= 2 K e^{-ell_n}` and `Pr(E^c) <= 2 K J_n e^{-ell_n} <= n^{-4}`. The one sided form
used in Lemma P5(iii) has the same bound with the factor `2` removed.

*Proof.* Identical to Lemma P6c with `phi_s := 1{round s is agent j's Stage-1 pull at C and its
local index is at most L_n}`, which is `G_s^{--}`-measurable because the Stage-1 schedule at `C`
reads only the visit count of `C` and the cube's phase. Always `c_n <= L_n`, and on the event that
`C` completes bidding `c_n = L_n` exactly and `M_n = L_n (beta_{j,C} - Abar_{j,C})`; `lambda = 4 s_n`
gives `2 exp(-2 L_n s_n^2) = 2 e^{-ell_n}`. Off that event no bid is formed, `C` never awards,
never prices and never monitors, and every visit to `C` is charged to `e_stage1`. `QED`

So the only thing the original proof of Lemma P1 got from exogeneity was that the index set of the
Stage-1 rounds is deterministic. That is convenient but not necessary: a set of rounds that is
predictable at the half step serves equally well. **What exogeneity is still needed for is not that
the index set is deterministic but that it is the same in two coupled executions**, which is a
different statement and is the subject of 17.4.

### 17.3 The fallback with a local horizon that is not known in advance (Lemma P7 restated)

This removes the third load the adversary identifies as G3, which neither the explorer nor I named:
`EXPLORER.md` Lemma 7 and my Lemma P7 both treat the cube's fallback length `H_C^fb` as known at
the cube's fallback start, which is true only because the arrival path is in `F_0`.

**Lemma P7c.** Assume (A4f), of which this lemma uses clauses (f2) and (f3). Fix a cube `C`, let `H` be the (random) number of fallback visits
to `C` over the horizon, and suppose an agent `j*` has conditional reward mean at least `v` whenever
it is selected at a visit to `C`, that is `E[Y_u | G_u^{--}, I_u = j*] >= v` at every such round.
Then

    E[ sum over fallback pulls at C of Y_u ]  >=  v E[H]  -  E[ R^dbl_K(H) ] .

The algorithm is unchanged; only the analysis is. The first version added "and the same holds
conditionally on any field with respect to which the fallback start is determined". That sentence
was asserted, not proved, and it is used nowhere: part (C) upgraded deliberately does not condition,
which is the whole improvement, and part (A) keeps (A4m) and the original Lemma P7. I delete it
rather than prove it, because an unused conditional claim inside a lemma is where the next reader
will build.

*Proof.* Index rounds, not local times. Let `phi_u := 1{round u is a fallback visit to C}` and
`k(u)` the index of the doubling epoch that the local fallback clock is in at round `u`; both are
`G_u^{--}`-measurable, because the local clock counts previous fallback visits to `C` and `X_u`
tells whether round `u` is a visit to `C`. The weights, hence `q_u` and `p_u`, are functions of the
cube's own past fallback data, so they are `G_u^{--}`-measurable. **Here, and only here, the
mechanism's own randomisation is used, and it is used through clause (f2) of (A4f)**: the Stage-3
selection has law `p_u` conditionally on `G_u^{1}`, and since `p_u` is already
`G_u^{--} = G_u^{0}`-measurable and `G_u^{0} subseteq G_u^{1}`, the tower property gives
`E[ 1{I_u = j} | G_u^{--} ] = p_{j,u}`. The first version of this document asserted that step from
an ordering of the filtration, which does not give it; that is the adversary's H1 and it is the
reason (A4f) exists. Writing
`r_{j,u} := E[Y_u | G_u^{--}, I_u = j]`, we get `E[ hat Y_{j,u} | G_u^{--} ] = r_{j,u}` and
`E[ sum_i q_{i,u} hat Y_{i,u}^2 | G_u^{--} ] <= K/(1 - gamma_{k(u)})`, exactly as in Lemma P7.

Fix an epoch index `k`. The exponential potential inequality of Lemma P7 is pathwise and holds for
every prefix of the rounds of epoch `k`, so, with `T_k := sum_u phi_u 1{k(u) = k}` the realised
length of epoch `k` (`T_k <= 2^k`, and `T_k = 0` if the epoch never starts),

    sum_{u: phi_u = 1, k(u) = k} ( hat Y_{j*,u} - sum_i q_{i,u} hat Y_{i,u}
        - eta_k sum_i q_{i,u} hat Y_{i,u}^2 )  <=  (log K / eta_k) 1{T_k >= 1}   pathwise.

Every indicator appearing here is `G_u^{--}`-measurable, so taking expectations term by term is an
application of the tower property and not of optional stopping, and there is no need for `T_k` to be
known in advance. This gives
`E[ sum_{u in epoch k} (v - Y_u) ] <= E[ 2 gamma_k T_k + (K log K / gamma_k) 1{T_k >= 1} ]`, and
`2 gamma_k T_k <= 2 gamma_k 2^k` with `gamma_k = min{1/2, sqrt(K log K/2^k)}` makes the bracket at
most `3 sqrt(K 2^k log K) 1{T_k >= 1}` when `2^k >= 4 K log K` and at most
`(3 sqrt(K 2^k log K) + 2 K log K) 1{T_k >= 1}` otherwise. Summing over `k` inside the expectation,
and using that `T_k >= 1` only for `k` with `2^k <= H`, the sum telescopes exactly as in Lemma P7 to
`R^dbl_K(H)` pathwise, with the same constant `3(2 + sqrt 2) <= 11`. `QED`

The single change from Lemma P7 is that `H` now appears inside the expectation. Everywhere the
accounting uses `sum_C R^dbl_K(n_C)`, the Cauchy and Schwarz steps of Section 6 apply inside the
expectation and give the same deterministic bound `e_fb` with `J'_n` replaced by its deterministic
upper bound `min{J_n, n}`, which part (D) already uses.

### 17.4 What part (A) needs, and why it is not upgradable

Part (A) uses (A4f) everywhere the other two parts do, and in addition it uses, at exactly one
place, that the two coupled executions have the **same** Stage-1 rounds at every cube and pull the
same agent at each: this is Fact 1, and it is what makes (6.1) and the identity of the price across
the two executions true pathwise. If the arrival path may react to a realised reward, the two
executions separate at the first round at which the deviator's target differs from its capacity and
the seed falls between them; thereafter they visit different cubes at different rounds, the deviator
receives different numbers of Stage-1 pulls at a cube in the two executions, and there is nothing
to compare. This is not a measurability statement and no refinement of a filtration repairs it.

**The accurate statement of what is needed, which is weaker than exogeneity.** The first version
said "this is not a measurability statement and no refinement of a filtration repairs it", which is
right, and then called exogeneity irreducible, which is imprecise. What the proof needs is that
**the arrival path is the same random sequence in the two coupled executions**, that is, that a
deviation cannot move the path. Exogeneity delivers that and is formally stronger. I looked for a
genuinely weaker sufficient condition and the natural candidate fails: "arrivals exogenous until
every cube has completed Stage 1, reactive afterwards" preserves Fact 1 and (6.1) but destroys the
accounting, because `n_C` then differs between the two executions and the comparison of `U'^post`
with `n_C w_C` is between two different numbers of pulls, a difference of order `n`. So the sentence
for the paper is "part (A) requires that a deviation cannot move the arrival path, which exogeneity
delivers and which is necessary, since part (A) is false otherwise", not "exogeneity is
irreducible".

Part (A) is moreover **false** without exogeneity, by the adversary's Section 4.4, which I checked:
`K = 2`, `M_1 = 1`, `mu_1 = 0`, `M_2 = mu_2 = x`, a path that sits at the origin cube if the first
reward is `0` and at the top corner cube if it is `1`, and the deviation "deliver `0` at the first
Stage-1 pull, then follow `S^*`" moves the entire remaining horizon to a cube where the honest
agent's capacity is `0`, hence `tau = 0`, hence per pull utility `1`. The gain is `Theta(n)` at
every horizon with `sigma_n < 1`. So the hypothesis is not merely unremoved, it is necessary.

### 17.5 The upgraded statements

Let `e_stage1`, `e_price`, `e_mon`, `e_fb`, `e_bid`, `e_osc` be as in `EXPLORER.md` Section 6 with
`J'_n` replaced throughout by the deterministic `min{J_n, n}`.

The two upgraded parts have **different hypotheses and neither dominates the other**, so they are
stated separately and should be stated separately in the paper. Part (B) needs only the seed clause
(f3); part (C) needs the mechanism clause (f2) as well, and the adversary's H1 shows that the extra
clause is not a formality. Part (B) is about the proposed profile and part (C) is about arbitrary
joint behaviour, so neither implies the other.

**Theorem 1B upgraded (second capacity revenue under nonanticipating arrivals).** Assume (A1),
(A2), (A6) and **clause (f3) of (A4f) alone**; the arrival path may be any process realised before
the round's own draws, in particular it may react to past rewards, to past coins, and to the
mechanism's own randomisation. Let every agent play `S^*`, with strategies in `B^ctx_{j,n}`. Then

    P(n; S^*_n)  >=  E[ sum_{t <= n} M_(2)(X_t) ]  -  ( e_stage1 + e_price + O(n^{-2}) ) .

*Proof.* Every ingredient is available. `P = E[sum_t m_{I_t,t}]` is the tower property under (f3).
Fact 0 is deterministic. Lemma P1c gives `E_C` with no arrival hypothesis, and Lemmas P2 and P4 are
pathwise consequences of `E_C` and Fact 0. Lemma P6c gives `H_C`, and Lemma P6(d) is pathwise, so
on `E_C cap H_C` **no cube ever switches**: therefore every post Stage-1 round is a Stage-2 round,
every Stage-2 target is at least `tau_C >= M_(2)(X_t) - 4 s_n - (4/3) rho_n` pathwise, and
**Lemma P7 is never invoked**, so the third load of 17.3 does not arise here at all. The Stage-1
rounds number at most `min{K J_n L_n, n}` pathwise. The complement is charged at
`n sum_C Pr(E_C^c cup H_C^c)` over the deterministic set of `J_n` cubes, crudely at `n_C` rounds per
cube. Nothing conditions on a future event, nothing couples two executions, and **no conditional
expectation is taken anywhere in this proof**, which is why the mechanism's own randomisation never
enters: Lemmas P2 and P4 hold for whoever wins, so the tie break needs no probabilistic property,
and Lemma P7 is never invoked. `QED`

I checked this claim the way the adversary did, by going through every step looking for a use of a
mechanism draw rather than by assuming the parallel with part (C), and there is none. Part (B) is
therefore the cleanest of the three statements.

**Theorem 1C upgraded (honest benchmark under nonanticipating arrivals and arbitrary joint
behaviour).** Assume (A1), (A2), (A6) and **clauses (f2) and (f3) of (A4f)**; clause (f2) is
necessary here and its omission is exactly the adversary's H1. For every feasible behavioural
profile in which each agent plays some strategy in `B^ctx_{j,n}` and every honest agent respects
pointwise honesty,

    P(n; S)  >=  E[ sum_{t <= n} b(X_t) ]  -  ( e_stage1 + n(4 s_n + (4/3) rho_n) + e_mon + e_fb
                  + O(n^{-2}) ) .

*Proof.* As in Section 8, with three changes. First, `E^H_C` comes from the one sided form of
Lemma P1c and `H_C` from Lemma P6c, neither of which uses the arrival path. Second, Lemma P5 is
deterministic: `v_C` and `h_C` are defined from the instance and the grid, and P5(ii) is pathwise
honesty. Third, and this is the step that needed the third load, the fallback contribution is now
bounded by Lemma P7c, which permits the local horizon `H` to be random and unknown at the fallback
start. Note that the fallback bound in part (C) needs **no good event at all**: the comparator
`h_C` has conditional mean at least `v_C` whenever selected, pathwise, by honesty alone. So the
only place an indicator multiplies a conditional expectation is absent here, and the conditioning
defect of D2 and of G5 cannot arise in part (C) once Lemma P7c is used. The Cauchy and Schwarz
steps are applied inside the expectation with the deterministic `min{J_n, n}` in place of `J'_n`.

One step that the first version left unstated, and which the adversary is right to ask for. The two
cases write `E[sum over Stage-2 pulls at C of Y_u] = E[sum of targets]` **within the case**, that
is `E[(Z_r - A_r) 1{case}] = 0`, whereas Lemma P6(e) gives only `E[Z_r - A_r] = 0`. The step is
correct: `{W_C = h_C}` and `E^H_C` are both determined by the Stage-1 bids at `C`, hence at `C`'s
award round, which precedes every Stage-2 pull at `C`, so the stopped martingale argument of
Lemma P6c applies with that indicator inserted into `phi_s`. `H_C` is **not** award-time
measurable, and the proof does not multiply a conditional expectation by it: it uses `A_q >= 0` and
charges `E[q tau_C 1_{H_C^c}] <= n Pr(H_C^c)`. `QED`

**The benchmarks are endogenous under this hypothesis, and the sentence must change.** Both
upgraded parts compare revenue with `E sum_t M_(2)(X_t)` and `E sum_t b(X_t)`. Under (A4f) the
arrival path may react to past rewards, so the contexts at which `M_(2)` and `b` are evaluated are
partly determined by what the mechanism did. The inequalities are true exactly as stated and remain
meaningful as one sided guarantees, but "the mechanism attains the second capacity" is no longer the
sentence being proved. The honest reading, and the one the paper should use, is: **on the realised
arrival path, whatever it was, the mechanism collects within the stated error of the second capacity
(respectively of the best honest intrinsic mean) evaluated along that same path.** Under exogeneity,
where the path is not influenced by the mechanism, the two readings coincide, which is why part (A)
is unaffected by this remark.

**Part (A), unchanged.** Under (A1), (A2), (A4m), (A5) with the class `B^ctx+_{i,n}`, and (A6),
part (A) holds as in Section 6. Exogeneity is indispensable and the statement is false without it.

### 17.6 The hypothesis each part uses, stated once

* **Common to all three:** (A1) Lipschitz primitives, (A2) `log(en) >= 3L`, (A6).
* **Part (B):** clause (f3) of (A4f), the seed clause, and nothing else. No condition on the
  arrival process, no use of the mechanism's own randomisation. Deviation class `B^ctx`.
* **Part (C):** clauses (f2) and (f3). No condition on the arrival process. Deviation class
  `B^ctx`. Clause (f2) is not a formality: without it the adversary's H1 instance makes part (C)
  false by about `0.45 n`.
* **Part (A):** all of (A4f), **and in addition** that a deviation cannot move the arrival path,
  which exogeneity delivers (and which (A4m) of Section 2 states in the form actually used, since
  it also licenses Convention A and the larger class `B^ctx+`). Necessary, since part (A) is false
  without it.

The first version of this list said "Parts (B) and (C): nothing further", which is the sentence H1
refutes. I record that the error was in the summary line rather than in any proof: Lemma P7c did
use the mechanism's randomisation, and the hypothesis simply failed to grant it.

This is a sharper statement than either `EXPLORER.md` or the first version of this document made,
and I believe it is the right one for the paper: **the mechanism's revenue and honest benchmark
guarantees place no condition on the arrival process at all, requiring only that the round's own
draws are fresh given everything realised before them; only the incentive guarantee needs the
arrival process to be unmovable by a deviation.** The guarantees are then statements about the
realised path, in the sense recorded at the end of 17.5.

## 18. The horizons at which the bound says anything, computed independently

The mechanism prices at zero whenever `sigma_n >= 1`, and the three error terms exceed the trivial
bound `n` until `n` is large. I recomputed both thresholds from the parameters of `EXPLORER.md`
Section 3 with `K = 2` and `J'_n = min{J_n, n}`, in
`<scratchpad>/round2/f1-prover2/horizons.py`, by bisection on `log_10 n`. Smallest `n` at which each
quantity first drops below its trivial value:

* `D = 1`: `sigma_n < 1` at `10^{6.1}`; bound (A) `< n` at `10^{5.2}`; bound (B) slack `< n` at `10^{6.8}`.
* `D = 2`: `10^{8.5}`, `10^{7.5}`, `10^{9.3}`.
* `D = 3`: `10^{11.1}`, `10^{10.0}`, `10^{12.0}`.
* `D = 4`: `10^{13.7}`, `10^{12.7}`, `10^{14.9}`.
* `D = 6`: `10^{19.4}`, `10^{18.4}`, `10^{20.8}`.
* `D = 10`: `10^{31.7}`, `10^{30.7}`, `10^{33.7}`.

This reproduces the adversary's Section 8.6 table to within `0.1` in the exponent, which is the
resolution of the bisection; I computed it from the parameter definitions rather than from that
report. Reading: since `D = K d`, the smallest case of any interest, two agents with scalar
contexts, already needs `n` of order `10^{8.5}` before the mechanism announces a positive price,
and three agents with two dimensional contexts needs `10^{19.4}`. The threshold grows like
`exp(c D)` rather than polynomially, because `J_n` carries a factor `2^D` and `rho_n` a factor
`sqrt D`.

Three things follow and the paper should say all three.

1. **The theorem is asymptotic in a strong sense** and no simulation can exhibit it. Section 11's
   experiment tests the lemmas at recalibrated constants and says nothing about the rates; the same
   is true of `EXPLORER.md` Section 10.
2. **The comparison with the public result is about exponents, not constants.** The manuscript's
   public contextual error `E_n = L sqrt d n h_n + 4 sqrt(J_n n log n) + 3 min{J_n, n}`
   (`sections/contextual_samf_algorithm.tex`) has no `2^D` multiplying a bidding block of length
   `L_n`, so at any given `n` it is very much smaller. Same exponent, different constants.
3. **A referee will compute this**, so it should be stated rather than discovered.

## 19. Framing I withdraw or correct

I checked each of the following against the canonical files on the branch, not against
`ADVERSARY.md`.

**A correction of the record before the list.** This section withdraws **my** framing, not the
adversary's. All five of its framing findings are upheld here and each was checked again against the
canonical files; nothing in G8 is refuted. I state this because the opposite reading was in
circulation, and if it reached the paper the four sentences this section retires would be restated.

**19.1 The exponent comparison.** My original summary said the result matches `thm:grid-etc`, which
is accurate, but the surrounding framing of this track says "at the exponent of the existing public
contextual result", and that is wrong. `sections/contextual_samf_algorithm.tex` now carries a
**headline** public rule, `thm:grid-ucb-robust`, at
`E_n = O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})`, which delivers contextual sharp adaptivity, exact
pathwise contextual monotonicity with no boundary condition, expected contextual FATA, robustness,
and, under Lipschitz capacities, revenue `E sum_t M_star(X_t) - E_n^K`; `thm:grid-etc` at
`n^{(D+2)/(D+3)}` is presented there as the explore-then-commit **variant**. Since
`(D+1)(D+3) < (D+2)^2` for every `D >= 0`, the headline exponent is strictly smaller. The only
correct sentence is "at the exponent of `thm:grid-etc`, the explore-then-commit variant", and I
will not restate anything stronger.

**19.2 The top-set condition is absorbed, not removed.** I read the theorem text: the public
deviation bound holds "if in addition two agents attain the largest capacity at `nu`-almost every
profile". That hypothesis is **identical** to `M_(2) = M_star` `nu`-almost everywhere. Theorem 1's
revenue benchmark is `E sum_t M_(2)(X_t)`, the public one's is `E sum_t M_star(X_t)`. So on the
instances where the public hypothesis holds the two benchmarks coincide, and on the instances where
it fails Theorem 1 does not remove the condition, it pays for it by weakening the benchmark by
exactly the top gap. My original summary line "with no top-set, boundary, mass or component
condition" is therefore literally true and materially misleading, and I withdraw it. The accurate
sentence is: **the top-set condition is replaced by the second-capacity benchmark.** What is
genuinely removed, and remains a real gain, is the boundary regularity, the positive-mass
condition, the finitely-many-top-stable-components condition, and, for parts (B) and (C), the
arrival assumption altogether.

**19.3 "No instance constant" no longer separates this result from the manuscript.** I checked
`sections/appendix_private.tex` on the branch: it now defines the good event to include the upper
tail of `beta_i^max`, states "On `G_i cap {i wins}` the announced second order statistic is
`beta_(2) = max_{j != i} beta_j <= beta'_i <= beta_i^max <= M_i + s_n`", and
`sections/Private_information_setting.tex` line 66 now says "This covers a non-top winner as well
... No capacity gap enters the bound". So the scalar theorem already has the property. It separates
Theorem 1 from the two finite contextual candidates, which still carry `delta_i`, and from nothing
in the manuscript. The accurate sentence is "no instance constant in the bound, at the price of the
instance dependent horizon threshold `n >= exp(3L)`", and Section 10.4 and the adversary's G6 both
show that threshold is load bearing rather than cosmetic.

**19.4 The scalar by-product is banked and my quotation of it is stale, so I withdraw Section 10.1's
final block.** The manuscript was changed after my first version was written. The sentence I quoted,
"No concentration around the deviator's capacity is invoked", is no longer in
`sections/appendix_private.tex`; the file now does exactly the opposite and uses the counterfactual
bid `beta_i^max` in the good event, and the non-top branch and the `delta_i` constants are gone.
**Nothing in Section 10.1 should be applied to the manuscript again.** Two remarks survive and are
the only parts of that section I still stand behind. First, the route the manuscript adopted is the
counterfactual one, and I verified it is sound: `beta_i^max` is a function of the Stage-1 seeds
alone because Stage 1 pulls each agent `L_n` times on a fixed schedule, exactly as the appendix now
says. Second, my one sided bound on the **realised** bid is an equivalent alternative that would
reach the same conclusion without naming a counterfactual; it is not needed now that the
counterfactual version is in the paper, and I am not proposing a second change.

**19.5 What part (A) does and does not rule out.** Under `S^*`, on the good events no cube ever
switches, so an agent that wins no cube is pulled only during Stage 1 and its entire baseline
utility is at most `2 min{J_n, n} L_n = O(n^{(D+2)/(D+3)})`, which is the same order as the
permitted gain. Such an agent has a real deviation of that order, namely deliver `0` at every
Stage-1 pull, which costs it nothing because it loses anyway. So part (A) is informative only for
an agent whose baseline payoff is `Theta(n)`, that is for a winner. This is a feature of additive
equilibrium statements in this model, the scalar theorem has it too through `prop:tightness`, and
it is not a defect; but the word equilibrium should not be asked to carry more than that.

## 20. Revised least secure step, and revised bottom line

**My ranking of the least secure step was wrong, and wrong in the same way as the explorer's.** I
named the `F_{s-1}`-measurability of the Stage-2 indicator and attributed it to exogeneity. Section
17.1 shows it is a bookkeeping artefact: written at the pre-seed field with the indicator stopped,
the same bound follows with no property of the arrival path. The finite-context adversary had
established this on the same day, in a section of a file that both the explorer and I cited for a
different finding. That is a correlated error inherited from a shared upstream document, and I
accept the adversary's conclusion that the agreement of the two routes is weaker evidence than it
looked: Section 6's correction shows the same thing from the other side, since each proof avoided
the other's instance of one error shape and committed its own.

**Revised ranking (updated again in Revision 3).**

1. **The hypothesis, not a step, and now for the third time.** The pairwise independence defect (G1)
   was live in both documents and is fatal to part (A) as literally stated; (A4c), written here to
   repair it, then omitted the mechanism's own randomisation and made my own upgraded part (C) false
   by about `0.45 n` (the adversary's H1). Three occasions, one cause: a probabilistic hypothesis
   assembled as a list of independence clauses can omit a family, and each time it did. (A4f) of
   Section 17.0 is written in the conditional form, over every draw at a round, and that form cannot
   omit a family because it quantifies over everything realised before the draw rather than
   enumerating what the draw is independent of. This is now the first thing to check in any new
   contextual statement on this project, ahead of any step of any proof.
2. **The coupling of part (A)** (Fact 1 and (6.1)), which needs exogeneity, is not repairable by any
   refinement of a filtration, and is necessary because part (A) is false without it. This is now
   the only genuine load on the arrival hypothesis, and it sits in one part out of three.
3. **The conditional expectation bookkeeping around the fallback**, where I made one error (G5,
   corrected in Section 6) and the explorer made another (D2). Both are repairable at `O(n^{-2})`
   and neither changes a statement, but the error shape recurred twice in two documents, so a third
   reader should check every place where an indicator multiplies a conditional expectation.
   Section 17.5 notes that in part (C) the shape cannot arise once Lemma P7c is used.
4. **The hypothesis `n >= exp(3L)`**, which the adversary shows is not cosmetic: outside it there is
   an explicit instance on which part (B) fails by `n/4` against a bound of `O(n^{6/7} log n)`. The
   first version of this line said `n/2`, quoting a summary table that the adversary has since
   corrected against its own derivation: with `E M_(2) = E max{t, 1-t} = 3/4` and a delivery of
   `1/2` per post-bidding round the deficit is `n/4`, and `3n/4` only in the degenerate regime
   `sigma_n >= 1/2` where the price is zero and revenue is zero.

**Bottom line, revised twice.** I still believe the three parts are true, now under (A4f): part (B)
under the seed clause alone, part (C) under the seed and mechanism clauses, part (A) under those
plus the requirement that a deviation cannot move the arrival path. I still do not claim they are
correct. What changed across the two revisions: the hypothesis was wrong twice and is now written in
a form that cannot be wrong in that way again; two steps of my own were wrong (the `H^*_C`
measurability and the assertion that the selection coin is fresh) and are repaired; the least secure
step I named was not the least secure step; parts (B) and (C) are stronger than either document
claimed and are now stated separately because their hypotheses differ; the benchmarks are endogenous
under the weakened hypothesis and the claim must be phrased along the realised path; and four of the
framing claims around the theorem are withdrawn. **The mechanism itself is unchanged and no bound,
statement or rate has moved in either revision.** Every defect found by the adversary or by me has
been in a hypothesis, in a conditioning field, or in a sentence about the result, and none in the
construction.
