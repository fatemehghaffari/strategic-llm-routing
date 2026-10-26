# Adversary report on candidate C2 (profile-local MESP), 18 September 2026

Role: adversary. My job was to break the candidate. I did not break the mathematics of either
proof. I did break the **hypotheses**, twice, with explicit numerical counterexamples in which the
deviation gain is `Theta(n)` and exceeds the claimed bound by factors of 3.61 and 6.25 (first
counterexample, `n = 40000` and `n = 160000`) and 1.45 and 2.50 (second, `n = 10^6` and
`n = 4 x 10^6`). The first shows that an assumption both documents make cannot be weakened; the
second shows that an assumption both documents make is, as literally written, too weak, and is
repaired by one word. Neither touches a proof step.

I also found that **each prover named the wrong step as its own weakest**. PROVER2's Lemma M does
not need Convention F-A at all; PROVER1's phantom continuation is sound but its filtration is
defined with a random index set and needs the correction PROVER1 itself gives only in its
Section 13. The place where exogeneity of the arrivals is genuinely irreplaceable is the
two-execution coupling (PROVER2 Lemma B(a), PROVER1 (L4d)), and that is where my first
counterexample lands.

Documents read in full: `audit/round2/prompts/COMMON.md`;
`audit/round2/B/theorems/c2-local-mesp/PROVER2.md` (1085 lines);
`audit/round2/B/theorems/c2-local-mesp/PROVER1.md` (1491 lines, including the Section 13 that
was added while I was working); `audit/round2/B/CONTEXT_PROOF_CONTRACT.md`;
`sections/Private_information_setting.tex`; `sections/appendix_private.tex`;
`audit/round2/B/MATH_CANDIDATE_LEDGER.md` Section 4; `audit/round2/B/PRIVATE_BOUND_NOTES.md`.
No canonical file was modified.

Code, seeds and raw outputs: `<scratchpad>/round2/adversary-c2/`
(`plmesp_adv.py` the mechanism; `run_exog.py` the deviation search; `run_break.py` the two
counterexamples; `run_fallback.py` Lemma F versus the doubling fallback; `run_dp.py` the exact
dynamic program for the primary phase; `run_monitor.py` the pathwise monitor test;
`run_award.py` the award rules; `run_short.py` profiles that never finish bidding; `job.sh`,
`logs/`).
Compute log is Section 13 of this file (I did not touch the shared `COMPUTE_LOG.md`, which now
belongs to Prover 1).

## 0. Findings, by severity

| # | severity | what | where |
|:-|:-|:-|:-|
| F1 | P2 | The theorem is **false**, not merely unproved, if arrivals may react to a realised reward. Explicit instance, `Theta(n)` gain, bound exceeded 3.61x at `n = 40000` and 6.25x at `n = 160000`. Closes PROVER2 Section 9 item 5 and PROVER1 Section 13.1 item 5, which both say they did not know. P2 and not higher because both documents already assume (H3) and neither claims otherwise; it becomes P0 the moment the paper states the result without the independence clause or describes exogeneity as a technicality. | Section 7.1 |
| F2 | P1 | (H3) and (H4) of PROVER2, and (A1) and (A2) of PROVER1, are lists of **pairwise** independences. Read literally they admit a `Theta(n)` deviation: bound exceeded 1.45x at `n = 10^6` and 2.50x at `n = 4 x 10^6`. This is a wrong quantifier in a hypothesis, with a counterexample. The proofs silently use mutual independence, which both documents state correctly one section later, so one word repairs it and no statement or rate changes. | Section 7.2 |
| F3 | P2 | PROVER2's self-declared least secure step is secure, and its stated reason is wrong. Lemma M does not need Convention F-A; the displayed (5.2) is ill formed, but the repair is a half step of the filtration, not the exogeneity hypothesis. | Section 2 |
| F4 | P2 | PROVER2's filtration `F_t` in Section 5.1 is not well defined across the two coupled executions ("the coins used at rounds 1..t" is execution dependent), so `D_z` in Section 5.6 is not `F_{t_1(z)}` for either execution. Repair is two lines and PROVER2's own justification paragraph already contains it. | Section 3 |
| F5 | P2 | PROVER1's Lemma 5 defines `H_r` by excluding `{V_{r'} : r' > r}` with `V_r = U_{z,W,L+r}` and `W` random, so the excluded index set is random and the independence sentence does not follow from the displayed definition. PROVER1's Section 13.2 gives the correct version; the proof text does not. Its second worry (double consumption of seeds) is unfounded. | Section 4 |
| F6 | P2 | PROVER2's Remark 6.2 asserts that no hypothesis permits sharing bidding effort across profiles. That is true under its own (H1) but **false on the manuscript's contextual model**, where `M_j` depends only on `z_j`, so profiles sharing a coordinate share a capacity. The `Q K L` bidding cost is therefore not forced by the model, only by the mechanism. | Section 5.3 |
| F7 | P3 | PROVER2's `e_bid = Q L_n` is not capped by the trivial bound, so (A) is vacuous whenever `Q L_n > 2n`; PROVER1's `min{Q L, n}` is strictly better. | Section 6.1 |
| F8 | P3 | PROVER2 D3's stated advantage of `ell_n = log(2 n^5)` (that the mechanism then needs no bound on `Q`) is illusory: PROVER1's mechanism needs no `Q` either. The `n^5` costs a factor `sqrt(5/4)` on the `n s_n` term of (B) and (C) for nothing. | Section 6.2 |

Verdict on the candidate: **not rejected**. I could not exhibit a deviation that beats the bound
under the intended hypotheses, in argument or in simulation, and I checked the steps listed in
Section 11. The two constructions are both correct after the repairs F3 to F5, which are
editorial. My recommendation on which to put in the paper is in Section 9.

## 1. The question I was told to answer first

*Does any statement in the theorem quantify over arrival processes in a way that makes
conditioning on the whole path illegitimate, and does the deviation class secretly become
smaller or larger once the agent is allowed to know the arrival path?*

**Larger, and the enlargement is free.** I checked this as a chain of four claims and each holds.

1. *The bound does not depend on `A`.* PROVER2's error terms are `e_bid = Q L_n`,
   `e_mon = Q + sqrt(2 Q n ell_n)`, `e_fb = Q R_K(n)`, `e_low`, plus bad-event terms. The only
   places the arrival path enters are `sum_z V_z = n`, `sum_z sqrt(V_z) <= sqrt(Q n)` and
   `sum_z V_z^2 <= n^2`, and all three hold for **every** path in `X_F^n`, not merely on average.
   So the per-path bound is a constant in `A`.
2. *The conditional supremum dominates the unconditional one.*
   `sup_{S'} E[gain(S')] <= E_A[ sup_{S'} E[gain(S') | A] ] <= E_A[bound] = bound`.
   The first inequality is the only one that needs care and it is the trivial direction: the
   supremum of an average is at most the average of the suprema.
3. *Conditioning hard-codes the path, so the conditional class contains the conditional image of
   `B^ctx_{i,n}`.* Under `Pr(. | A = a)` a strategy that did not see the future becomes a special
   case of an own-history strategy for the deterministic schedule `a`, and the per-path bounds are
   proved uniformly over all such strategies. PROVER1 states this as Section 10(a) and proves
   Theorem 1 for the explicitly larger class `B^ctx+_{i,n}`. Both documents therefore prove the
   same strength; PROVER1 merely says it out loud.
4. *No step uses that the deviator is ignorant of `A`.* I checked Lemma M, Lemma F, Lemma B and
   every branch of Section 5.6 of PROVER2, and Lemmas 3 to 8 and Sections 6.4 to 6.6 of PROVER1.
   Every one of them is a conditional statement that holds for an arbitrary realised target,
   uniformly. In particular the comparator hypothesis in the EXP3 lemma is about the
   **non-deviating** agents, who play `S^*` regardless of what anybody knows.

So the repair is genuine and not circular. It is also **strictly** an enlargement in the
contextual setting and not only formally: knowing `A` plus its own local phase, the deviator can
reconstruct the global round index `t` (the `v_z`-th visit to `z` is at a determined round), which
the contract's observation model otherwise withholds. PROVER1 (Section 1.4) says exactly this.

The one thing an agent cannot buy with `A` is information about the seeds, because (H3) makes `A`
independent of them. That is the whole content of "the enlargement is free", and it is also
precisely the sentence that fails in my counterexample F1, where the arrivals are a function of a
reward and therefore do carry seed information.

I also checked the one direction that could have gone wrong and did not: the baseline
`u_i(n; S^*_n)` is computed on the same conditioned space and `S^*` does not use `A`, so the
comparison is between the same two objects before and after conditioning.

## 2. Attack on PROVER2's named weakest step: Lemma M and Convention F-A (finding F3)

PROVER2 Section 9 says the passage (5.1) to (5.2) is its least secure step, that under the natural
filtration the displayed exponential inequality "would be false as stated", and that "the repair
is exactly Convention F-A, which is legitimate under (H3), and this is the single place where
exogeneity of the arrivals is doing indispensable work in the monitoring argument".

**The first half of that is right and the second half is wrong.** The display

```
 E[ exp(lambda (M^z_s - M^z_{s-1})) | F_{s-1} ] <= exp(lambda^2 psi^z_s / 8)
```

is indeed ill formed under the natural filtration, because its right-hand side is not
`F_{s-1}`-measurable. But that is a bookkeeping artefact of writing the step at `F_{s-1}` rather
than at the pre-seed field, and it is repaired without touching the arrival process.

**Repair (half a step of the filtration, no conditioning on `A`).** Let `(F_t)` be the natural
global filtration in which `X_t` is revealed at round `t`, and let
`F_t^- := sigma(F_{t-1}, X_t, I_t, m_{I_t,t})` be PROVER2's own pre-seed field. Fix `r` and the
stopping time `T_r`. Put `phi_s := psi^z_s 1{s <= T_r}` and

```
 c_t := sum_{s<=t} phi_s ,      N_t := exp( lambda M^z_{t and T_r} - (lambda^2/8) c_t ),  N_0 = 1.
```

Then `phi_s` is `F_s^-`-measurable (it depends on `X_s`, which `F_s^-` contains, and on the data
collected at `z` strictly before `s`, which `F_{s-1}` contains), and `N_{t-1}` is
`F_{t-1}`-measurable hence `F_t^-`-measurable. By (5.1) and Hoeffding's lemma applied
conditionally on `F_t^-`,

```
 E[ N_t | F_t^- ] = N_{t-1} e^{-(lambda^2/8) phi_t} E[ e^{lambda phi_t (Y_t - m_{I_t,t})} | F_t^- ]
                  <= N_{t-1} e^{-(lambda^2/8) phi_t} e^{(lambda^2/8) phi_t} = N_{t-1},
```

so `E[N_t] <= E[N_{t-1}] <= ... <= 1`, which is the only thing the Chernoff step needs. Nothing
here asks `psi^z_s` to be `F_{s-1}`-measurable, so nothing here asks for the arrival path.

**Consequence.** PROVER2's Lemma M(a), (b), (c), (d), (e) all survive under the natural
filtration. Convention F-A is still convenient and still legitimate, but the sentence "this is the
one place where the conditioning on the whole arrival path is indispensable rather than merely
convenient" is false, and so is the Section 9 claim that Lemma M is the place an adversary should
attack first.

**Where exogeneity actually is load bearing**, in decreasing order of how badly it is needed:

1. **Lemma B(a) / PROVER1 (L4d), the two-execution coupling.** Not repairable. If arrivals react
   to rewards, the two coupled executions visit profiles at different rounds, agent `i` receives a
   different number of Stage-1 pulls at `z` in the two executions, and the pathwise bid domination
   and the `l_i(z)` accounting both collapse. PROVER2 says this in Section 7 item 10 but ranks it
   second. It is first, and Section 7.1 below shows the theorem is then false.
2. **Lemma F (PROVER2) and Lemma 6 (PROVER1), through the measurability of `H` and of `H'_k`.**
   Not repairable as written, but repairable in principle: `H` is a bounded stopping time of the
   local fallback clock and the estimators are bounded by `1/eta_n`, so optional stopping replaces
   `H` by `E[H]` in the conclusion, which is all the applications use. PROVER1 Section 13.2 item 2
   identifies this correctly as the place conditioning on arrivals is bought and used; PROVER2
   does not mention it.
3. **The counting in Lemma M(a)'s union bound.** Conditioning on `A` turns the index set
   `{(z,r) : r <= V_z}` into a deterministic set of size `sum_z V_z = n`. Without it one pays a
   factor `Q` (which is what PROVER1 does, at `ell = log(2 n^4)` and `Q n^{-3}` total failure
   probability). Purely a constant.

So the honest summary for the paper is: exogeneity is used in the coupling, where it cannot be
removed, and is used for convenience in the two martingale lemmas, where it can.

## 3. Attack on PROVER2's second named weak point: the joint field `D_z` (finding F4)

PROVER2 Section 5.1 defines

```
 F_t := sigma( A, the seeds U_1,...,U_t, the coins used at rounds 1,...,t,
               and every quantity realized through round t ),
```

and deliberately keeps unused coins out, "since Lemma F needs the selection at a fallback round to
be conditionally random". Section 5.6 then conditions on `D_z`, "the joint field generated by
everything realized in **both** executions through round `t_1(z)`, together with `A`", and asserts
that Lemmas M and F apply conditionally on it.

**The defect.** "The coins used at rounds `1,...,t`" is execution dependent. At a round
`s <= t_1(z)` execution 2 may be in a local fallback at some other profile `z'` while execution 1
is still in Stage 2 there, so execution 2 consumes `xi_s` and execution 1 does not. There is
therefore no single `F_t` that serves both executions, and `D_z` is not `F_{t_1(z)}` for either of
them. Every sentence of the form "Lemma M applies conditionally on `D_z`" is, as written, about a
field that the lemma was not proved for.

**The repair, two lines.** Use the primitive filtration

```
 G_t := sigma( A, (Pi_z)_{z}, all agents' private coin arrays, (U_s, xi_s)_{s <= t} ),
```

for which every claim PROVER2 needs is immediate:

* both executions' realisations through round `t` are `G_t`-measurable, because each execution is a
  deterministic measurable function of the primitives;
* `(U_{t+1}, xi_{t+1})` is independent of `G_t`, which is exactly (5.1) and the freshness of the
  fallback coin;
* `D_z subset G_{t_1(z)}`, because `t_1(z)` is `sigma(A)`-measurable and both executions' round
  `<= t_1(z)` realisations are functions of `(A, Pi, private coins, (U_s, xi_s)_{s <= t_1(z)})`;
* `M^z` vanishes up to `t_1(z)` in each execution and is a `G`-martingale after it, so Lemma M(e)
  is literally the statement that the supermartingale may be started at `t_1(z)`;
* Lemma F still works, because the field just before a fallback round `t` is `G_{t-1}`, which does
  **not** contain `xi_t`. The exclusion PROVER2 engineered by hand is automatic.

So PROVER2's deliberate exclusion of unused coins is not merely unnecessary, it is the thing that
makes `F_t` ill defined across executions. Its own paragraph "Legitimacy of conditioning on the
joint field" already writes the right object ("for every `t` the pair `(U_t, xi_t)` is independent
of the field generated by `A`, the priorities, the private coins, and `(U_s, xi_s)` for `s < t`");
the fix is to promote that sentence to the definition in Section 5.1 and delete the parenthetical.

**I could not turn this into a counterexample**, and I do not believe one exists: the two
executions are coupled only through primitives, and the conclusion of every conditional lemma is
an inequality between conditional expectations given a field that contains no future primitive.
One placement of PROVER1's device is worth importing while fixing this: PROVER1 (F2) puts **all**
private coins into `F_0`, which makes each agent's target a deterministic function of the history
and the mechanism coins and removes the later sentence "integrating over the latter changes
nothing". That is cleaner and I recommend it.

## 4. Attack on PROVER1's named weakest step: the phantom continuation (finding F5)

PROVER1 Lemma 5 extends the primary reward sequence at `z` to `r = 1,...,n` with phantom targets
`m_r := tau_z` and phantom seeds `V_r := U_{z,W,L+r}`, and works in

```
 H_r := sigma( all primitives except { V_{r'} : r' > r } ).
```

**The defect.** `V_r = U_{z,W,L+r}` depends on the random winner `W`, so `{V_{r'} : r' > r}` is a
**random** index set and `H_r` is not generated by a fixed sub-family of the primitives. The
sentence "since the primitives are mutually independent, `V_r` is independent of `H_{r-1}`" is then
not a consequence of the displayed definition, because independence of a randomly selected member
of an independent array from a field that already determines the selector is a separate (true, but
separate) statement.

**The repair.** PROVER1 gives it in Section 13.2 item 1 but never puts it in the proof. Define

```
 H_r := sigma( all primitives except { U_{z,j,L+r'} : j in [K], r' > r } ),
```

that is, exclude **every** agent's post-bidding seed at `z` beyond index `r`, not just the
winner's. Then

* `W` and `tau_z` are `H_0`-measurable, because they are functions of `{U_{z,j,k} : k <= L}` and
  `pi_z`, none of which is excluded;
* `V_1, ..., V_r` are `H_r`-measurable for every realisation of `W`;
* for any `H_r`-measurable `m` with values in `[0,1]`,
  `E[ 1{U_{z,W,L+r+1} <= m} | H_r ] = sum_w 1{W=w} E[ 1{U_{z,w,L+r+1} <= m} | H_r ] = m`,
  since `W` is `H_r`-measurable and each `U_{z,w,L+r+1}` is an excluded independent uniform.

With that definition Lemma 5 goes through verbatim and every constant is unchanged.

**PROVER1's second worry is unfounded and the proposed product-space fallback is not needed.**
It writes that "the seeds `U_{z,j,L+r'}` with `r' > q` are consumed twice, once by the phantom
process and once by the real fallback pulls at `z`", and offers to enlarge the space. There is no
problem to fix. `H_r` is generated by primitives, not by the history, so the phantom increment at
index `r+1` is conditionally centred given `H_r` whatever the real execution later does with the
same variable; and the conclusion of Lemma 5 is only ever used at indices `r <= q`, where the
phantom coincides with the real process. I checked the one place this could have bitten, namely
whether the real target `m_r` for `r <= q` could depend on an excluded seed: it cannot, because
during local Stage 2 only `W` is pulled at `z`, so the history before `W`'s `r`-th primary pull
consumes `U_{z,j,L+r'}` only for `r' < r`.

**Adjudication of the junction the coordinator asked about.** Both treatments are sound after one
editorial correction each, and they fail in different, non-overlapping ways before it:

| | PROVER2 Lemma M | PROVER1 Lemma 5 |
|:-|:-|:-|
| device | global-time martingale, predictable indicator `psi^z_s`, stopped at the round of the `r`-th primary pull | local-index martingale, phantom continuation past `q`, seed-generated filtration `H_r` |
| seed convention | attached to rounds | attached to `(profile, agent, local pull index)`, which is the contract's convention (Section 1) |
| defect as written | (5.2) is ill formed at `F_{s-1}` | `H_r` has a random exclusion set |
| repair | state the step at the pre-seed field `F_t^-` (Section 2 above); no arrival conditioning needed | exclude all `K` agents' post-bidding seeds at `z` (PROVER1's own Section 13.2) |
| needs `sigma(A)` in the filtration? | no, after the repair | no |
| needs a phantom process? | no | yes, but only to make the union-bound range deterministic |
| union-bound cost | `n^{-4}` total, buys `ell_n = log(2 n^5)` | `n^{-3}` per profile, `Q n^{-3}` total, at `ell = log(2 n^4)` |

Neither is unsound and neither is obviously superior. PROVER2's is shorter after the repair, since
it needs no phantom process; PROVER1's is the one that matches the contract's seed indexing and
that survives verbatim if one later wants a version without conditioning on arrivals. My
recommendation is in Section 9.

## 5. Cross-profile contamination: excluded by construction, and I could not construct one

The brief asked me to build a deviator that uses one profile to move the price, the phase
boundary, the fallback state or the visit counts at another. I could not, and I can say exactly
why, and exactly what would have to change for one to exist.

### 5.1 The complete list of cross-profile channels

Enumerate every object the mechanism holds. Global: `n`, `K`, and the deterministic parameter
functions `L_n, ell_n, s_n, b_n(.), gamma_n, eta_n, R_K(.)`. Per profile `z`: `v_z`, the Stage-1
reward sums, `tau_z`, `W_z`, `r_z`, `Z_z`, the local EXP3 weights, and `Pi_z`. Nothing else
exists. The per-profile objects are updated only at visits to `z`, and every parameter is a
function of `n` and `K` alone. So a contamination channel must be one of exactly four things.

1. **A parameter that depends on realised data.** There is none; this is the whole content of
   "all tuning constants from the global horizon", and it is what makes the locality claim a
   construction rather than an estimate. If a later draft tuned `b_n` or `gamma` to a **local**
   visit count, the local phase at `z` would become a function of `v_z` only, which is still
   arrival-driven and still fine; but if it tuned anything to a global realised statistic
   (a pooled empirical mean, a global switch count, an adaptive confidence level), locality would
   break and Lemma L / Lemma 3 would have to be replaced by an estimate. That is the one design
   change a referee should be warned against.
2. **The price at `z`.** `tau_z = (beta_(2),z - s_n)_+`. When the deviator wins, the second order
   statistic with multiplicity equals `max_{j != i} beta_{j,z}`, a function of the other agents'
   Stage-1 rewards at `z`, which are `1{U <= M_j^z}` at rounds fixed by `A`. The deviator can move
   neither the rounds nor the targets. When the deviator **loses**, its own bid can be the second
   largest and it does move the announced price; this is the one honest channel, PROVER1 names it
   in Section 10(d) and both proofs close it the same way. The attack is: bid just under the
   winner so that `tau_z` exceeds the winner's capacity, force a monitor switch, and collect
   fallback pulls. It fails because `beta_(2),z <= beta_{W,z}` whenever `W` is a largest bidder,
   so on the good bidding event `tau_z <= (beta_{W,z} - s_n)_+ <= M_W^z` and `S^*` makes `W` meet
   the price. I also checked it by exhaustion: over 400000 random configurations
   with `K` in `{2,...,6}`, a dominated deviating bid for `i`, an independent uniform priority,
   and all bids forced onto the grid `{0, 1/L, ..., 1}` with `L <= 7` so that exact ties are
   frequent (800000 bid vectors examined), there was no case with `beta_(2) > beta_W`, no
   violation of the winner inclusion, no violation of the price identity
   `beta_(2) = max_{j != i} beta_j` on `{i wins}`, and no case with `tau_z > M_W^z` when `i`
   loses and the other bids are within `s_n` of their capacities
   (`run_award.py`, 0 violations of all four).
3. **The visit counts.** Exogenous by (H3). This is the channel my counterexample F1 opens.
4. **The seeds.** Fresh per round (PROVER2) or per `(z, j, k)` triple (PROVER1). This is the
   channel my counterexample F2 opens.

So the claim "cross-profile contamination is excluded by construction rather than bounded" is
correct, and the two ways to defeat it are precisely the two hypotheses I did break. That is a
better outcome for the paper than a bounded contamination term, and it should be said that way.

### 5.2 Deviations I actually ran and what they did

All under exogenous arrivals, agent 0 the deviator, coupled executions with common random numbers.
Deviations: Stage-1 underbidding to the midpoint `(M_i^z + V_i^z)/2`; Stage-1 underbidding all the
way down to the runner-up capacity `V_i^z` at every profile, which makes the deviator lose or tie
every auction;
smooth primary riding `m_r = tau - alpha/sqrt(r)` for `alpha in {0.25, 0.5, 1, 2, 4}`; the
"bank the slack" rider that delivers `0` whenever `Z_{r-1} >= r tau - b_n(r)`; a class `B^ctx+`
"dump the last `j` visits" rider that uses knowledge of the whole arrival path to deliver `0` on
the final `j` visits to each profile, for `j in {1, 5, 50, 500}`; immediate crash followed by a
constant fallback delivery level in `{0, 0.5, 0.9, 1.0}`; and the pairwise combinations of
underbidding with each rider. Arrival processes: i.i.d., deterministic alternating, a single
adversarial block split, and a 40-block burst pattern, all exogenous.

Nothing came within a factor of 10 of the bound and no per-profile inequality was violated.
Representative numbers at `n = 4000`, `K = 3`, `Q = 2`, agent 0 top at both profiles (the only
configuration in which bound (A) is not dominated by `e_low`): the bound is `2585.4`
(`e_bid = 1060`, `e_mon = 823`, `e_fb = 702`), the best deviation found gained `127.2`
(underbidding plus `alpha = 1` riding), and the per-profile allowance `L_n + 1 + 2 b_n(V_z) +
R_K(n) = 1293` was never approached. Larger horizons are in Section 8.

Two things in that table are worth recording as confirmations rather than attacks.

* **Proposition 6.1 is exact.** Pure Stage-1 underbidding gained `79.50` in every replication with
  zero variance, against the predicted `L_n (M_i^z - m'(z)) = 530 x 0.15 = 79.50`. The
  zero variance is the signature of the "post-Stage-1 executions coincide pathwise" argument, so
  the simulation is testing that argument and not just the number.
* **Every crash deviation loses and raises revenue.** `fbfarm` and the aggressive rider
  (`alpha = 4`) lost between `114` and `153` of utility. That is the accounting working: the
  fallback returns capacity delivery to the non-deviators.

### 5.3 A cross-profile channel that exists in the model and that neither prover uses (finding F6)

PROVER2 Remark 6.2 says the `Q L_n` term is real and adds that it "says nothing about whether a
cleverer mechanism could avoid paying `L_n` per profile (for example by sharing bidding effort
across profiles, which no hypothesis here permits since the primitives at different profiles are
unrelated)". Under PROVER2's own (H1), where `mu_i^z` and `M_i^z` are arbitrary per pair `(z,i)`,
that is correct. **On the manuscript's contextual model it is false.** The contract Section 2 fixes
`mu_i(x_i)` and `M_i(x_i)` as functions of agent `i`'s own coordinate, so two distinct full
profiles `z != z'` with `z_j = z'_j` have `M_j^z = M_j^{z'}` identically. A mechanism keyed on the
pair `(agent, own coordinate)` rather than on the full profile could therefore estimate each
agent's capacity once per distinct own coordinate. If agent `i` takes `Q_i` distinct coordinate
values across `X_F`, the bidding cost becomes `L sum_i Q_i` instead of `Q K L`, and with a product
structure `Q = prod_i Q_i` this is exponentially smaller (`K = 2`, ten coordinates each:
`Q K L = 200 L` against `sum_i Q_i L = 20 L`).

I am **not** claiming that the resulting mechanism satisfies the theorem. What the deviation
analysis would need is that the price faced by `i` at `z` still depends only on the other agents'
bids (it would: it is the second order statistic of the pooled bids at `z`'s coordinates), that
the bid-domination coupling still holds per pull (it would: it is pointwise), and that a profile
enters Stage 2 only once every coordinate bid it uses is complete (a scheduling condition that
needs its own argument and that I did not write). I record this as an opportunity and a correction
to the remark, not as a result. It matters because the headline regime `Q = o(n^{1/3}(log n)^{-1/3})`
is the paper's main limitation, and the model, unlike (H1), permits attacking it.

## 6. Short profiles, ties, `K = 2`, and the calibration

### 6.1 Profiles that never finish bidding, and profiles cut off mid-monitoring (finding F7)

Both treatments are right and one is better.

*Never finish bidding.* At a profile with `V_z < K L_n` every visit is a bidding pull, there is no
price and no monitor, and the deviator's entire harvest there is its Stage-1 effort saving, which
is at most one per pull because the per-pull utility difference is `M_i^z - m' <= 1`. This is
pathwise, needs no good event and no error term, and both documents say so. I confirmed it
(`run_short.py`): `K = 3`, `Q = 3`, `n = 40000`, `K L_n = 7944`, visit counts
`(19965, 19972, 63)`, so `z_2` never awards. A deviator that shades only at `z_2` gained exactly
`5.25` with zero variance across 8 replications, against the pathwise prediction
`l_0(z_2) . (M_0^{z_2} - m') = 21 x 0.25 = 5.25`, where `21` is the number of round-robin Stage-1
pulls agent `0` receives in `63` visits. A deviator cannot buy itself extra pulls at a low-mass
profile, because the Stage-1 schedule is reward independent.

The one difference that matters is the cap. PROVER1 charges `sum_z l_i(z) <= min{Q L, n}`, which
stays below the trivial bound `2n`; PROVER2 charges `e_bid = Q L_n` with no cap, so bound (A) is
worse than the trivial `2n` as soon as `Q L_n > 2n`, which happens exactly in the regime of many
tiny profiles that this branch is about. Not an error, but PROVER1's form should be adopted. The
same applies to the revenue and robustness charges (`min{Q K L, n}` against `Q K L_n`).

A second, smaller difference: PROVER2's Stage-1 schedule is a round robin, so at a truncated
profile every agent gets about `V_z / K` pulls; PROVER1's is a fixed permutation with `L`
consecutive pulls each, so at a truncated profile the agents late in `sigma_z` get **no** bidding
pull at all. Neither breaks anything (the profile is charged either way), but round robin degrades
more gracefully and is the better mechanism to specify.

*Cut off mid-monitoring.* This is the case both documents handle better than the manuscript does.
The manuscript's scalar revenue proof says "`q` is a bounded stopping time for the primary
filtration"; in the contextual setting the local primary phase can also end because the profile
stops arriving, which is not a stopping time of any filtration generated by the local rewards.
PROVER2 removes the issue with the unconditional martingale identity `E[M^z_n] = 0` (Lemma M(d));
PROVER1 removes it with the phantom continuation, which makes the union-bound range deterministic.
Both are correct and both are improvements on the scalar text. I checked the charge inequality
`A_q >= q tau - 1 - 2 b_n(q)` at the cut-off case directly: the proof of Lemma M(b) never uses why
the phase ended, only whether the test fired at `q` or at `q-1`, so a deviator that knows from `A`
exactly when a profile stops being visited and banks slack right up to the end gains at most
`1 + 2 b_n(V_z)` there. That is what the `dumplast` deviations in Section 5.2 test, and the largest
measured gain from them was a small fraction of the allowance.

### 6.2 `K = 2` and capacity ties (finding F8 on the calibration is in the second half)

I attacked ties in three places and none of them moved.

* *Bid ties.* Bids live on the grid `{0, 1/L_n, ..., 1}`, so exact ties have positive probability
  and are not a measure-zero nuisance. The winner-inclusion step (PROVER2 Lemma B(d), PROVER1
  (L4b)) is the only place a tie could matter, and it is written without a strict inequality: if
  the dominated bid still ties for the maximum, the whole bid multiset is unchanged and so are the
  tie set and the priority; if the dominating bid is strictly larger, it wins outright. Confirmed
  by the 400000-configuration exhaustion above with ties forced to be frequent.
* *Capacity ties inside a profile.* If `M_i^z = M_j^z = M_*(z)` then both are top, `tau_{i,z} <=
  V_i^z = M_i^z`, and the top branch applies to both. The non-top branch is entered only on
  `delta_i(z) > 0` strictly, so the knife edge `delta = 0` is never handed to the branch whose
  bound divides by `delta`. For revenue, `M_(2)(z)` counts multiplicity, so a tied top makes the
  benchmark the full first best at that profile. I ran the `K = 2` tie instance explicitly and
  found no violation.
* *`K = 2`.* `V_i^z` is the single other capacity, `beta_(2)` is the minimum of the two bids, and
  the fallback comparator is the single other agent. `K >= 2` is used only through `log K > 0` in
  `gamma_n` and `R_K`. Nothing degenerates. Neither proof uses a two-top condition anywhere, which
  is the honest contrast with `thm:finite-context` and `thm:contextual-public`, and both say so.
  Measured: `K = 2`, `Q = 2`, `M(z_0) = (0.90, 0.60)`, `M(z_1) = (0.80, 0.80)` so that `z_1` is an
  exact capacity tie, 21 deviations. At `n = 40000` (8 replications) bound (A) is `9647.0` and the
  best gain found is `788.5`; at `n = 160000` (12 replications) bound (A) is `22915.4` and the best
  gain found is `1679.4`. No per-profile allowance was approached, and pure Stage-1 underbidding
  gained exactly `L_n x 0.15` in both (`397.20` at `L_n = 2648`, `1039.05` at `L_n = 6927`) with
  zero variance.

*Calibration (finding F8).* PROVER2 D3 justifies `ell_n = log(2 n^5)` and the union bound over the
`sum_z V_z = n` pairs by saying "the mechanism then needs no bound on `Q` at all (H6), which
matters for the claim that the platform does not know the arrival law". That justification does
not hold: PROVER1's mechanism uses `s = sqrt(log(2 K n^4)/(2L))` and `b(r) = sqrt(r log(2n^4)/2)`,
which contain `K` and `n` and no `Q` either, and its **bad-event cost is `Q`-free too**, because
its accounting charges `2 n_z` rather than `2 n` at each profile and `sum_z n_z <= n`: the total
is the `8 n^{-2}` of its (6.10), not `Q n^{-2}`. So both mechanisms are `Q`-free, both bad-event
budgets are `Q`-free, and the extra power of `n` buys nothing. It costs a factor `sqrt(5/4) = 1.118` on the `n s_n` term, which is one of the two
leading terms of the revenue bound (B) and of the robustness bound (C). PROVER1's calibration is
the one to keep.

One calibration point goes the other way. PROVER1 sets `L := ceil(n^{2/3}(log(en))^{1/3})` with
**no cap**, dropping the manuscript's and PROVER2's `min{floor(n/(2K)), .}`. Nothing breaks (a
profile with `V_z < K L` simply never awards, by its own (M5), and the bound carries
`min{Q K L, n}`), but `K L > n` whenever `n < K^3 log(en)`, and then even a single-profile instance never
awards: the mechanism degenerates to pure round robin with no price, no monitor and no fallback,
and the theorem says nothing. PROVER2's cap makes `K L_n <= n/2` at every `n`, so Stage 1 always
finishes on a profile that receives at least half the rounds. Keep the cap.

## 7. The two counterexamples

Both are explicit instances with explicit deviations and arithmetic, both are numerical, and both
attack a hypothesis rather than a proof step. I state clearly for each what it does and does not
refute.

### 7.1 F1: arrivals that react to a realised reward make the theorem false, not merely unproved

PROVER2 Section 9 item 5 says: "Arrival processes that react to rewards. Excluded by (H3). Section
7 item 10 identifies Lemma B(a) as the first casualty. I did not look for a counterexample, so I
do not know whether the theorem is false in that case or merely unproved." PROVER1 Section 13.1
item 5 says the same. **It is false.**

**Instance.** `K = 2`, `Q = 2`, `X_F = {z_0, z_1}`. Agent `0` strategic, agent `1` honest.

```
 M(z_0) = (1.0, 0.0),   mu(z_0) = (0.0, 0.0)
 M(z_1) = (1.0, 1.0),   mu(z_1) = (0.0, 1.0)
```

Agent `0` is top at both profiles, so `delta_0 = infinity` and `e_low = 0`; this is the
configuration in which bound (A) is smallest and the theorem's hypothesis `4 s_n <= delta_i`
holds vacuously for every `n >= 2K`. The honest agent delivers `0` at `z_0` (its capacity there is
`0`) and `1` at `z_1`.

**Arrival process.** `X_1 = z_0`; for every `t >= 2`, `X_t = z_1` if `Y_1 = 1` and `X_t = z_0` if
`Y_1 = 0`. This is exogenous in every sense except the one that matters: it is a measurable
function of one realised reward. It is deterministic given that single bit, it is not i.i.d., and
it takes values in `X_F`, so it satisfies every clause of (H3) except independence from the seeds.

**Deviation** (in `B^ctx_{i,n}`, not even needing `B^ctx+`): agent `0` delivers `0` on its first
Stage-1 pull at `z_0` (round 1), delivers `0.5` on every later Stage-1 pull at `z_0`, and follows
`S^*_0` everywhere else.

**Arithmetic.** Under `S^*`, agent `0` delivers `M_0(z_0) = 1` at round 1, so `Y_1 = 1` and every
remaining round is at `z_1`. There both bids equal `1`, the price is `tau_{z_1} = 1 - s_n`, and
agent `0` earns `s_n` per primary pull when it wins the priority tie and `0` when it does not.
Under the deviation, `Y_1 = 0`, so every remaining round is at `z_0`. There agent `1` bids `0` and
agent `0` bids about `0.5`, so agent `0` wins, `tau_{z_0} = (0 - s_n)_+ = 0`, the monitor test
`Z_r < r . 0 - b_n(r)` can never fire, and agent `0` delivers `0` for all `n - 2 L_n` post-bidding
visits at a per-pull utility of `1 + mu_0(z_0) - 0 = 1`. The gain is
`(n - 2 L_n) + 0.5 L_n` minus the baseline's `z_1` earnings, which is `Theta(n)`.

**Measured.**

| `n` | mean gain (30 to 6 reps) | as a fraction of `n` | bound (A) | ratio |
|:-|:-|:-|:-|:-|
| 40000 | 34863.9 | 0.872 | 9647.0 | **3.61** |
| 160000 | 143165.8 | 0.895 | 22915.4 | **6.25** |

(`e_bid`, `e_mon`, `e_fb` at `n = 160000` are `13854.0`, `6230.1`, `2831.3`; `e_low = 0`.) The
ratio grows like `n^{1/3} (log n)^{-1/3}`, so the failure is not a finite-`n` artefact.

**What it refutes and what it does not.** It does not refute Theorem 4.3 or Theorem 1, which
assume (H3) and (A1). It settles the open item both provers left: the theorem is **false** without
exogeneity, so (H3) cannot be weakened to "arrivals are not chosen by an agent" or to any other
non-independence condition, and the manuscript must not describe the hypothesis as a technical
convenience. It also confirms that Lemma B(a) / (L4d) is the first casualty, as PROVER2 predicted:
in the two coupled executions the profile visited at round `t` is different for every `t >= 2`, so
the Stage-1 schedules differ, agent `0` receives `L_n` bidding pulls at `z_0` in one execution and
one in the other, and the pathwise bid domination has nothing to compare.

**The boundary case.** Let the arrival process be reward-dependent on an event of probability `eps`
and equal to a fixed exogenous path otherwise (draw an independent `Bernoulli(eps)` at the start).
The deviation gain is then exactly `eps . g_dep + (1 - eps) . g_indep`, and I measured
`g_indep = 1.0` and `g_dep = 34863.9` at `n = 40000`. So the bound is violated as soon as

```
 eps > (bound - g_indep)/(g_dep - g_indep) = (9647.0 - 1.0)/(34862.9) = 0.277   at n = 40000,
 eps > (22915.4 - 1.0)/(143164.8)          = 0.160                             at n = 160000,
```

and the threshold decays like `n^{-1/3} (log n)^{1/3}`. **For every fixed `eps > 0` the bound fails
for all large enough `n`.** There is no continuity to trade on: an arbitrarily small fixed amount
of dependence between the arrivals and the rewards produces a `Theta(n)` gain, because the gain is
linear in `eps` and linear in `n` while the bound is `n^{2/3}(log n)^{1/3}`. Any future attempt to
relax (H3) to approximate independence therefore has to quantify `eps` against `n`, not against a
constant.

### 7.2 F2: (H3) and (H4) read literally are pairwise independence, and that is not enough

PROVER2 (H4) reads: "There is an array `(U_t)_{t<=n}` of i.i.d. uniform `[0,1]` variables,
independent of `A`, of the mechanism coins, and of the agents' private coins."
PROVER1 (A2) reads: "There is an array of independent Uniform`[0,1]` variables `U = {...}`,
independent of `X`, of all priorities, of all mechanism coins and of all private coins."
Both are lists of separate independence statements. Section 5.1 of PROVER2 ("five mutually
independent families") and Section 4.1 of PROVER1 ("all mutually independent") state the strong
version, but Section 4.1 of PROVER2 is titled "The theorem, with every hypothesis explicit", and a
referee who reads only the hypothesis list gets the weak one. The weak one is not enough.

**Instance.** `K = 2`, `Q = 2`. Agent `0` strategic, agent `1` honest.

```
 M(z_0) = (1.00, 0.98),   mu(z_0) = (0.00, 0.98)
 M(z_1) = (0.50, 0.50),   mu(z_1) = (0.00, 0.50)
```

Arrivals i.i.d. uniform on `{z_0, z_1}`, which is as exogenous as it gets.

**Seeds.** Let `c_t` be agent `0`'s private coin at round `t`, an unbiased bit; let `B_t := 1{X_t = z_0}`;
let `V_t` be i.i.d. uniform `[0,1]` independent of everything; and set

```
 U_t := ( (B_t xor c_t) + V_t ) / 2 .
```

Then `(U_t)` is an i.i.d. uniform `[0,1]` array; `(U_t)` is independent of the whole arrival
sequence (given `A`, each `B_t` is fixed and `c_t` is an unbiased bit, so `B_t xor c_t` is
unbiased); `(U_t)` is independent of the private coin array (given `c`, each `B_t` is unbiased);
and `A` is independent of `c`. **Every pairwise independence in (H4) and in (A2) holds.** What
fails is joint independence: given both `A` and `c`, the seed is confined to `[0,1/2)` or to
`[1/2,1)`.

**Deviation.** Agent `0` observes the current profile (the contract's default observation model)
and its own private coin, so at `z_0` it knows `B_t = 1` and hence knows whether `U_t < 1/2`. It
therefore delivers, at every pull at `z_0`,

```
 Stage 1:  m = 0.5 if c_t = 1, m = 1.0 if c_t = 0     (mean reward 1.0 at mean cost 0.75)
 Stage 2:  m = 0.5 if c_t = 1, m = tau if c_t = 0     (mean reward tau at mean cost (0.5+tau)/2)
```

and plays `S^*_0` at `z_1`. Feasibility holds (`m <= M_0(z_0) = 1`) and the timing is respected:
the target is chosen before the seed is used. The mechanism sees an empirical bid of `1.0` and an
empirical reward rate of exactly `tau` in the primary phase, so agent `0` wins the auction, the
monitor never fires, and it holds the price `tau ~ 0.98` at a per-pull cost of `0.74` instead of
`0.98`.

**Measured** (mean over reps, agent `0`'s utility under the deviation minus under `S^*`, common
random numbers):

| `n` | gain | as a fraction of `n` | bound (A) | ratio |
|:-|:-|:-|:-|:-|
| 200000 | 19447.1 | 0.0972 | 26361.9 | 0.74 |
| 1000000 | 105958.9 | 0.1060 | 72899.8 | **1.45** |
| 4000000 | 442282.0 | 0.1106 | 176692.4 | **2.50** |

**What it refutes and what it does not.** It does not refute the mathematics: the proofs use the
strong hypothesis and are correct under it. It refutes the hypothesis list as written, and the
repair is one word in each document, for example

> (H4) The array `(U_t)_{t<=n}` is i.i.d. uniform `[0,1]` and the five families
> `A`, `(U_t)`, `(Pi_z)`, `(xi_t)` and the agents' private coin arrays are **mutually** independent.

It is worth recording that the manuscript's own scalar phrasing, "targets are chosen before fresh
conditionally independent Bernoulli seeds", is the correct strong condition, because it asks for
`E[Y_t | everything realised before the seed, target] = m` and my construction violates exactly
that. So the contextual documents are weaker than the source they localise, not stronger.

## 8. The deviation search under the intended hypotheses

This is the part of the job that failed, which is the outcome the candidate wanted. I report it
in full because the brief asks me to say what I tried.

**Method.** I reimplemented PL-MESP from PROVER2 Section 2 (`plmesp_adv.py`), not from either
prover's code, so the numbers are independent. Two executions are built on one probability space
with common arrivals, common round seeds `U_t`, common fallback coins `xi_t`, common priorities
`Pi_z` and common private coins, exactly as Lemma B prescribes; execution 2 is the baseline `S^*`
and execution 1 carries the deviation. I report the difference of agent `0`'s expected utility,
the total against bound (A), and the per-profile difference against the per-profile allowance the
proof actually gives (`L_n + 1 + 2 b_n(V_z) + R_K(n)` at a top profile,
`L_n + 8(1 + sqrt(2 ell_n))^2/delta^2 + 2 R_K(n)/delta` at a non-top one), which is a sharper test
than the aggregate because it removes `Q L_n` from the comparison at every other profile.

**Deviations tried (21).** `S^*`; Stage-1 underbidding to `(M_i + V_i)/2` at the profiles where
`i` is uniquely top; Stage-1 delivery of `V_i^z` at every profile, which makes the deviator
lose or tie every auction; smooth primary riding `m_r = tau - alpha/sqrt(r)` for `alpha` in `{0.25, 0.5, 1, 2, 4}`; the
"bank the slack" rider that delivers `0` whenever `Z_{r-1} >= r tau - b_n(r)`; `B^ctx+` riders that
use the whole arrival path to deliver `0` on the final `j` visits to each profile, `j` in
`{1, 5, 50, 500}`; immediate primary crash followed by a constant fallback delivery in
`{0, 0.5, 0.9, 1}`; and the products of underbidding with each rider and with the fallback farm.

**Instances.** `K = 3, Q = 2` with the deviator top at both profiles (the only configuration in
which bound (A) is not swamped by `e_low`); the same with a near-tie so that `1 + mu_i - tau` is
small; an honest deviator with `mu_i^{z_0} = 0.55` above the price, which is the Branch 3 / `Lambda`
case; and `K = 2` with an exact capacity tie at one profile (Section 6.2). **Arrivals.** i.i.d.; deterministic
alternating; a single adversarial block split (all of `z_0`, then all of `z_1`); and a 40-block
burst pattern. All four are exogenous, and the last two are as adversarial as (H3) permits.

**Result: no violation anywhere**, of the aggregate bound or of any per-profile allowance, at any
horizon, on any instance, under any arrival process. Representative full table at `n = 160000`,
`K = 3`, `Q = 2`, deviator top at both profiles, bound (A) `= 24454.3`
(`e_bid = 13854.0`, `e_mon = 6230.1`, `e_fb = 4370.2`, `e_low = 0`), per-profile allowance
`12226.7`, i.i.d. arrivals, 12 replications with common random numbers:

| deviation | gain | best per-profile gain |
|:-|:-|:-|
| underbid + rider `alpha = 1` | **1604.4** | 1523.5 |
| underbid + rider `alpha = 0.5` | 1322.1 | 1281.6 |
| rider `alpha = 2` | 1126.7 | 965.4 |
| underbid + dump last 50 | 1071.8 | 1065.7 |
| underbid alone | 1039.1 | 1039.0 |
| rider `alpha = 1` | 565.3 | 484.4 |
| dump last 500 | 327.0 | 266.0 |
| `S^*` | 0.0 | 0.0 |
| shade to `V_i^z` and lose every auction | -14627.6 | |
| bank the slack | -24471.6 | |
| crash then deliver `0` in the fallback | -37403.3 | |

The best deviation found is `6.6` percent of the bound and `12.5` percent of the per-profile
allowance. The adversarial exogenous arrival processes change nothing: best gain `1685.3` under a
single block split and `1806.5` under the 40-block burst pattern, against the same bound `24454.3`,
with the same `1523.5` per-profile Stage-1 component in all three cases. That insensitivity is
what (H3) predicts, and it is exactly what the manuscript's grid results cannot claim, since
`lem:cell-law` needs i.i.d. arrivals and the contract records a counterexample without them
(item 11.5).

**The honest-deviator branch behaves exactly as Branch 3 predicts.** On the instance with agent `0`
honest and `mu_0^{z_0} = 0.55` above the price there, every primary rider gains **exactly zero** at
`z_0` (`rider2.00`, `rider1.00`, `rider0.50`, `rider0.25`, `dumplast500` all show `z0: 0.0`), and
the deviator's whole harvest at that profile is its Stage-1 saving `1039.1`. That is the content
of Branch 3 / PROVER1's event `Lambda`: honesty pins the target at `mu_i^z > tau_{i,z}`, the
baseline earns exactly one unit per primary pull, and there is nothing left to shade. The branch is
not an artefact of the accounting, it is visible in the simulation.

**Three things in that table are confirmations rather than failures.**

* Pure Stage-1 underbidding gains `1039.05` with **zero variance across replications**, against
  the prediction `L_n (M_i^z - m'(z)) = 6927 x 0.15 = 1039.05`. Proposition 6.1 / Proposition 2 are
  exact, and the zero variance is the signature of the "post-Stage-1 executions coincide pathwise"
  argument, so the simulation tests the argument, not just the number.
* Every crash deviation loses heavily and raises platform revenue. That is the fallback accounting
  working: after a switch the non-deviators return to delivering capacity.
* No false switch was ever observed under `S^*`: zero switches in 20 replications at each of
  `n = 4000, 40000, 160000`, consistent with Lemma M(c)'s `(2 n^4)^{-1}`.

**Two component tests that are sharper than the end-to-end search.**

* *Lemma M(b), pathwise, under the optimal adaptive policy* (`run_monitor.py`). I computed the
  DP-optimal primary policy of Section 10.1 and ran it inside the mechanism, 2000 paths per cell,
  12 cells (`N` in `{500, 2000}`, `tau` in `{0.3, 0.6, 0.9}`, `M` in `{tau + 0.1, 1}`). Zero
  martingale-boundary crossings in 24000 paths; the slack in `A_q >= q tau - 1 - 2 b_n(q)` was
  never negative (minimum `101.5`); the worst realised per-path ratio of primary gain to
  `1 + 2 b_n(N)` was `0.626`, against an expected `0.500`. No violation.
* *Lemma F, under the best constant fallback delivery* (`run_fallback.py`). Covered in Section 9.1;
  worst ratio of measured deviator fallback utility to allowance `0.521` at `K = 2`, `0.234` at
  `K = 3`, `0.103` at `K = 5` (`n = 20000`), and `0.506` and `0.116` for `K = 2` and `K = 5` at
  `n = 100000`. This is the closest any attack came to any inequality of either document under the
  intended hypotheses.

**What the search does not test.** The non-top branch, which needs `4 s_n <= delta_i` and at
`n = 160000` needs a capacity gap above `0.26`; the asymptotic regime, since `Q K L_n` is `26`
percent of `n` at `n = 160000`, so bounds (B) and (C) are numerically vacuous there and only their
direction and trend are testable; and anything about instance sequences with vanishing gaps. Both
provers say the same and `PRIVATE_BOUND_NOTES.md` Note 3 quantifies it.

## 9. Adjudication of the differences between the two constructions

### 9.1 The fallback: PROVER2's prefix argument is sound, so the doubling can go

**The prefix argument is correct.** I checked it line by line and reproduced it.

* The potential inequality is a sum of per-round inequalities. `log(Wsum_{t+1}/Wsum_t) <= eta
  sum_i q_{i,t} hatY_{i,t} + eta^2 sum_i q_{i,t} hatY_{i,t}^2` holds at each round, and
  `log(Wsum_{H+1}/Wsum_1) >= eta sum_{t<=H} hatY_{j,t} - log K` holds for any `H`. So (5.3) holds
  at every prefix length, with `eta` fixed at whatever value the mechanism chose. This is the only
  property of the truncation that either document uses, and it is a property of a telescoping sum,
  not of the tuning.
* `0 <= eta_n hatY_{i,t} <= 1` needs only `p_{i,t} >= gamma_n/K = eta_n`, which explicit
  exploration guarantees at every round of every prefix.
* The expectation step gives `E[sum_{t<=H} Y_t] >= v H - 2 gamma_n H - K log K / gamma_n`, and the
  **loss** `2 gamma_n H + K log K / gamma_n` is increasing in `H` at fixed `gamma_n`, so the
  worst case over realised lengths is at `H = n`, which is exactly where the tuning is optimal:
  with `gamma_n = sqrt(K log K / n) <= 1/2` and `H <= n`,
  `2 gamma_n H + K log K/gamma_n <= 2 sqrt(K n log K) + sqrt(K n log K) = 3 sqrt(K n log K)`.
  The other case `gamma_n = 1/2` needs `n < 4 K log K` and then `sqrt(K n log K) >= n/2`, which is
  the manuscript's own case split.
* Realised lengths far shorter than the tuning length are the case the coordinator asked about.
  There the conclusion `E[sum Y] >= v H - R_K(n)` is often **vacuous** (the right-hand side is
  negative), but it is true, and every application uses it only through
  `bar A_i >= V_i^z bar Q_i - R_K(n)` and `bar Q_i <= R_K(n)/delta`, both of which degrade
  gracefully to the trivial `bar Q_i <= H`. Nothing divides by `H` anywhere. There is no failure
  mode here.

**Numerically.** I simulated one local fallback directly: `K` agents, a comparator delivering `1`
whenever selected, the deviator delivering a constant level `m`, and measured the deviator's
utility `(1 - m) Q_i`, which by Lemma F must not exceed `R_K(n)` when `V_i^z = 1` and `mu_i^z = 0`
(that is the exact statement `E[U^fb] <= (1 + mu - V) H + R`). Grid `H` in
`{100, 1000, 10000, n/4, n}` and `m` in `{0, 0.3, 0.6, 0.8, 0.9, 0.95, 0.99}`, `K = 3`,
`K` in `{2, 3, 5}`, at `n = 20000` and again at `n = 100000`. **No cell exceeded its allowance.**
Worst ratio of measured utility to allowance, over all cells at each `K`:

```
                  n = 20000                        n = 100000
   K = 2:  0.521 (single)  0.333 (doubling)   0.506 (single)  0.328 (doubling)
   K = 3:  0.234           0.147                    not run
   K = 5:  0.103           0.063              0.116           0.064
```

The ratios are stable in `n`, which is what the lemma predicts (both sides scale like `sqrt n`).

So the fallback allowance is not slack: at `K = 2` a deviator that simply delivers `0` in the
local fallback reaches 52 percent of `R_K(n)`, which is the closest any of my attacks came to any
inequality in either document under the intended hypotheses. It is still inside, and the gap
widens with `K` because `R_K(n)` grows like `sqrt K` while the deviator's share of the exploration
floor falls like `1/sqrt K`.

**Which mechanism is better, not just which analysis.** The same runs answer this and the answer
is not what either document assumes. Measured deviator utility at `K = 3`, `n = 20000`, `m = 0`:

| `H` | single EXP3 tuned to `n` (PROVER2) | doubling epochs (PROVER1) |
|:-|:-|:-|
| 100 | 29.7 | 20.0 |
| 1000 | 93.7 | 88.3 |
| 10000 | 137.0 | 322.3 |
| 20000 | 181.7 | 497.0 |

At `H` comparable to `n` the single tuning is the **less** exploitable of the two, by about a
factor of three, because the doubling throws away its weights at every epoch boundary and its
early epochs explore at `gamma_0 = 1/2`. At `H` much smaller than `n` the doubling is mildly
better, but there the absolute numbers are tiny and both are far inside their allowances. So the
simpler mechanism is also the better one in the regime that matters (a profile that falls back
early and then receives most of its visits). PROVER1 (Section 13.1 item 6) presents the doubling
as a feature, "the mechanism IS anytime in each LOCAL horizon". That adaptivity is real, but it
buys nothing here: the theorem is fixed horizon, the platform knows `n`, and `n` upper bounds
every local horizon, so the anytime property is paid for and not used.

**Verdict.** PROVER2's prefix version is sound; the doubling is unnecessary. Adopt the single
locally restarted EXP3 tuned to the global `n`. The cost is confined to one lower-order term:
summed over profiles, PROVER2 pays `Q R_K(n) = O(Q sqrt(K n log K))` against PROVER1's
`sum_z R^dbl_K(n_z) <= 11 sqrt(K Q n log K) + 11 Q K log K log_2(2n)` by Cauchy-Schwarz, so
PROVER2 is worse by a factor `sqrt(Q)` in the square-root part. For fixed `Q` both are
`O(sqrt(n log n))` and the dominant term is `Q K L_n = Theta(Q n^{2/3}(log n)^{1/3})`, so the
difference never touches a stated rate. PROVER2's own D1 says exactly this and I confirm it.

One caveat that neither document states: PROVER2's Lemma F charges `R_K(n)` per profile
**whether or not a fallback ever starts** (this is how `e_fb = Q R_K(n)` is assembled). That is
fine but it means the fallback term of the bound does not shrink when switches are rare, which
they are: I observed zero switches under `S^*` in 20 replications at each of
`n = 4000, 40000, 160000` (60 executions, no switch at any profile), consistent with the
`(2 n^4)^{-1}` bound of Lemma M(c).

### 9.2 The monitor junction: both sound, neither for the reason its author gives

Covered in Sections 2 and 4. Summary of the adjudication the coordinator asked for:

* PROVER2's Lemma M is sound **and does not need Convention F-A**. Its stated reason for needing
  it is wrong; the display (5.2) is merely written at the wrong field.
* PROVER1's Lemma 5 is sound **after** replacing the random exclusion set in `H_r` by the fixed
  one it gives in its own Section 13.2. As written in the proof it is defective, and the defect is
  not the one PROVER1 worries about: the double consumption of seeds by the phantom and by the
  real fallback is harmless, and the proposed enlargement of the probability space is not needed.
* Neither is "the sound one and the other unsound". They are two correct routes with different
  seed conventions. The genuine, non-editorial dependence on exogeneity is in the coupling, in
  both documents, and Section 7.1 shows what happens when it is dropped.

### 9.3 The enlarged deviation class is a genuine strengthening

Checked in Section 1. `B^ctx_{i,n} subset B^ctx+_{i,n}` strictly and materially (with the arrival
path plus the local phase an agent can reconstruct the global round index, which the contract's
observation model withholds); the baseline `S^*` does not use the arrival path, so the two sides of
the comparison are unchanged; the per-path bound is free of the arrival path and free of the
deviation, so the supremum may be taken inside; and no step anywhere uses the agent's ignorance of
the future. PROVER2 obtains the same strength implicitly through Convention F-A without saying so,
so the two documents prove equally strong statements and PROVER1's is the one that says what it
proves. I recommend stating the theorem for `B^ctx+`, because it is free, and because a referee
who worries about the conditioning step is answered by the class being larger rather than by an
argument.

### 9.4 Recommendation for the paper

Take PROVER2's mechanism with PROVER1's calibration and PROVER1's statement.

* Mechanism: PROVER2 Section 2, that is, round-robin Stage 1 (better than block Stage 1 at
  truncated profiles) and a **single** locally restarted EXP3 tuned to the global `n` (Section 9.1).
* Constants: PROVER1's `s = sqrt(log(2 K n^4)/(2L))` and `b(r) = sqrt(r log(2 n^4)/2)`, which are
  `Q`-free like PROVER2's and give an `n s_n` term smaller by `sqrt(5/4)` (Section 6.2).
* Statement: PROVER1's, that is, the class `B^ctx+_{i,n}`, the per-profile split of the error
  (top term at top profiles, non-top term at non-top profiles), and the caps `min{Q L, n}` and
  `min{Q K L, n}` (Section 6.1).
* Monitor: PROVER2's global-time martingale with the predictable indicator, written at the
  pre-seed field `F_t^-` as in Section 2 above. That version needs no phantom continuation and no
  arrival path in the filtration, so it is the shortest correct one and it is the one that will
  survive a referee who dislikes the conditioning.
* Filtration: PROVER1's device of putting all private coins into `F_0`, plus the primitive
  filtration `G_t` of Section 3 above.
* Hypotheses: the word "mutually" (Section 7.2), and an explicit sentence that exogeneity is not
  removable, with Section 7.1 as the reason.

## 10. The two confirmations the coordinator asked for

### 10.1 The Stage-2 boundary-tracking gain is still unproved, and neither document assumes it

Confirmed after reading both in full. The quantity `b_n(q)` appears in exactly one role in each
document, namely inside the charge

```
 A_q >= q tau_z - 1 - 2 b_n(q)      (PROVER2 Lemma M(b); PROVER1 (5.2))
```

which is a **lower** bound on the winner's delivered target sum and therefore an **upper** bound on
its utility. Every subsequent use is in that direction: PROVER2 (5.5), PROVER1 (6.9), the
summation `sum_z 2 b_n(V_z) <= sqrt(2 Q n ell_n)` by Cauchy-Schwarz, and the non-top tenure bound
`q <= 4(1 + sqrt(2 ell))^2/delta^2`, which is again an upper bound. Nowhere does either document
assert that a deviator can realise a gain of order `b_n(N_z)`, and nowhere is such an assertion
used as a step. Both say so explicitly and correctly: PROVER2 Section 9 item 3 ("I regard the
Stage-2 boundary-tracking gain as plausible and unproved, and it must not be stated as a
theorem"), PROVER1 Section 13.1 item 2 (same, and it declines to promote its own T4 observation).

**But it is more than plausible, and I can sharpen what the paper is allowed to say.** I solved
the primary phase at one profile **exactly**, as a finite Markov decision process over the whole
class of adaptive targets rather than over a heuristic family. The state after `r` primary pulls
is `(r, Z_r)` with `Z_r in {0,...,r}`; the monitor kills the phase at pull `r` exactly when
`Z_r < r tau - b_n(r)`; the per-pull utility `1 + mu - m` is linear in `m` and the reward is
`Bernoulli(m)`, so the value function is linear in `m` and the optimal policy is bang-bang between
`0` and `M`. Crediting the post-switch fallback with **zero** value makes the resulting number a
rigorous lower bound on the deviator's per-profile gain, because the real fallback utility is
nonnegative. Grid: `N` in `{200, 1000, 5000, 20000}`, `tau` in `{0.2, 0.5, 0.8, 0.95}`, `M` in
`{tau, tau + 0.2, 1}`, `mu` in `{0, 0.3}`, `ell = log(2 . 160000^5) = 60.608`
(`run_dp.py`).

```
 optimal primary gain over the S^* baseline N (1 + mu - tau), fallback credited zero,
 aggregated over the 24 cells (tau, M, mu) at each N:

   N       mean gain   min     max     b_n(N)    gain/b_n(N)   allowance 1 + 2 b_n(N)
     200      68.50   40.00   78.00     77.85       0.880             156.70
    1000     174.00  174.00  174.00    174.08       0.9995            349.16
    5000     389.50  389.00  390.00    389.26       1.0006            779.51
   20000     778.50  778.00  779.00    778.51       1.0000           1558.02
```

For `N >= 1000` the optimal gain equals `b_n(N)` to within 0.06 percent and is **independent of
`tau`, `M` and `mu`** across all 24 cells (the spread is one unit of utility, which is the
rounding of an integer reward count). At `N = 200` the monitor boundary is comparable to `N tau`
and the cap `m <= M` binds in the low-`tau` cells, so the gain is smaller. Worst ratio of optimal
gain to allowance over the whole 192-cell grid, including the `fb_rate > 0` cells: `0.5003`.
So the monitor term is **attained to leading order and the allowance
`1 + 2 b_n(N_z)` is tight within a factor of exactly two**, and summed over profiles the optimal
`sum_z b_n(N_z) <= sqrt(Q n ell_n / 2)` is exactly half of PROVER2's `e_mon`.

This does three things. It confirms `PRIVATE_BOUND_NOTES.md` Note 2 (the experiments lead's
dynamic-program observation) independently. It confirms that neither proof can be tightened in
this term by more than a factor of two. And it leaves the status unchanged: this is an exact
computation at particular parameters, not a proof of the `b_n(N)` scaling for all of them, so
**it still must not be stated as a theorem**, and the correct sentence for the paper is that an
exact dynamic program attains `b_n(N_z)` in our computations. Both provers are right to refuse to
promote it, and PROVER1 is right that its heuristic T4 shading is only suggestive.

For completeness on the heuristic side: the naive riders **lose**. The "bank the slack" policy,
which delivers `0` whenever the accumulated reward already guarantees surviving the next test,
lost `24471.6` of utility at `n = 160000`, because it stalls the cumulative reward while the
requirement `r tau` keeps growing and gets switched off. Only the smooth rider
`m_r = tau - alpha/sqrt(r)` gains, and its best measured gain at `n = 160000` was `1126.7` against
the two-profile allowance `sum_z (1 + 2 b_n(V_z)) = 2789`. The DP shows why the heuristics fall
short: the optimal policy is bang-bang and state dependent, not a smooth schedule.

### 10.2 The two reports about the candidate ledger are both right and are not in conflict

They are statements about different parts of the ledger's Section 4.

* **PROVER1's item 8 (the display over-counts).** The ledger's proof plan, step 5, produces a
  per-profile split: `L + 1 + 2 b(V_z) + R^dbl_K(V_z)` at a profile where `i` is top, and
  `L + O(1 + log n/delta_i(z)^2 + R^dbl_K(V_z)/delta_i(z))` where it is not. The ledger's displayed
  Theorem (i) instead sums `2 b(V_z) + R^dbl_K(V_z)` over **all** profiles and then adds the
  non-top terms. Since every term is nonnegative this is a valid weakening, but it is not what
  the plan proves, and it also uses `V_z` where the proof gives `n_z = (V_z - K L)_+`. PROVER1 is
  right and it says clearly that the display is valid, so "double counts" should be read as
  "is strictly weaker than the plan's own step 5", not "is wrong".
* **PROVER2's D1 (the ledger is `sqrt(Q)` tighter in the fallback term).** The ledger's doubling
  fallback gives `sum_z R^dbl_K(n_z) = O(sqrt(Q K n log K) + Q K log K log n)` after
  Cauchy-Schwarz, against PROVER2's `Q R_K(n) = O(Q sqrt(K n log K))`. The ratio is `sqrt(Q)` in
  the square-root part. PROVER2 is right.

So there is no contradiction: PROVER1 is comparing the ledger's **aggregated display** with the
ledger's **own plan**, and PROVER2 is comparing the ledger's **fallback term** with its own
different fallback. Both checks stand and the ledger is, in both respects, a correct upper bound.

One further ledger statement is worth flagging, which neither prover fully corrects. The ledger
asserts that the bound is "`o(n)` **iff** `Q = o(n^{1/3}(log n)^{-1/3})`". Only the "if" direction
follows from the upper bound. The converse would need a lower bound, and the best available is
PROVER1's Proposition 2 / PROVER2's Proposition 6.1, which give `c Q L` for **Local-MESP as
specified**, on instances with a unique top at every profile, and only when `Q K L <= n`. That is
not a lower bound over mechanisms, and Section 5.3 above gives a concrete reason to doubt that any
such lower bound holds on the manuscript's contextual model, where capacities at different
profiles are linked through the agents' own coordinates. The paper must write "if", not "iff".

## 11. What I checked, what I could not break, and what would have to be true

### 11.1 Steps I verified line by line and could not break

For each of these I reproduced the algebra and, where the step is an inequality between random
quantities, tried to construct a violating instance.

1. **PROVER2 Lemma M(a) tail.** The Chernoff choice `lambda = 4 b/r` gives `exp(-2 b^2/r)`, and
   `b_n(r)^2 = r ell_n/2` gives `exp(-ell_n) = (2 n^5)^{-1}` per tail. The stopped predictable
   range sum satisfies `c_n <= r` pathwise. The union over `sum_z V_z = n` index pairs and two
   tails costs `n^{-4}`. Correct. What would have to be true to break it: `psi^z_s` would have to
   fail to be measurable at the pre-seed field, which needs the local phase at `z` to depend on
   something realised at round `s` other than `X_s`. It does not, by Lemma L.
2. **PROVER2 Lemma M(b) charge.** The case analysis (no switch: the test failed at `q`; switch at
   `q >= 2`: apply at `q-1`; switch at `q = 1`: `A_1 >= 0 >= tau - 1`) is exhaustive and uses only
   `tau_z <= 1` and monotonicity of `b_n`. The proof never uses **why** the primary phase ended,
   which is exactly what makes it survive a profile cut off mid-monitoring and a deviator that
   knows from `A` when the cut-off is. Correct.
3. **PROVER2 Lemma M(c).** A switch at `r` with all targets at least `tau_z` forces the lower tail
   only; `sum_z V_z (2 n^5)^{-1} = (2 n^4)^{-1}`. Correct.
4. **PROVER2 Lemma M(d).** `E[M^z_n] = 0` and `M^z_n = Z^z_{q_z} - A^z_{q_z}`, with no optional
   stopping. This is a genuine improvement on the manuscript's scalar revenue proof, whose
   "bounded stopping time for the primary filtration" is not available once the phase can end
   because a profile stops arriving. Correct, and worth importing into the scalar appendix.
5. **PROVER2 Lemma F / PROVER1 Lemmas 6 and 7.** Checked in Section 9.1, including the constants
   `3 sqrt(K H log K) + 2 K log K` and the geometric sum `3 sqrt 2/(sqrt 2 - 1) = 10.2427` behind
   `C_0 = 11`. Correct.
6. **PROVER2 Lemma B / PROVER1 Lemma 4.** Bid domination is pointwise on a shared seed, so it is
   immune to any rule generating the target; the winner inclusion handles ties without a strict
   inequality; the price identity `beta_(2) = max_{j != i} beta_j` on `{i wins}` is the sorting
   fact. Verified by exhaustion (Section 5.1). Correct. What would have to be true to break it:
   the two executions would have to differ in which rounds are Stage-1 pulls at `z` or in which
   agent is pulled there. That is exactly what endogenous arrivals cause (Section 7.1).
7. **PROVER2 Branch 2, the cancellation.** The deviating post-bid utility is bounded by
   `(1 + mu_i - tau_{i,z}) N_z + 1 + 2 b_n(V_z) + R_K(n)` and the baseline collects
   `(1 + mu_i - tau_{i,z}) N_z` exactly, with the same coefficient on both sides. The coefficient
   identity needs `tau_{i,z} <= V_i^z <= M_i^z`, which is `i in T(z)` plus the good bidding event.
   Correct, and it is `PRIVATE_BOUND_NOTES.md` Note 1, which I re-derived and agree with. If a
   reader rejected it the cost would be an extra `2 n s_n`, which does not change the rate;
   PROVER1 says the same in its Section 13.2 item 3 and I confirm that assessment.
8. **PROVER2 Branch 4 / PROVER1 Section 6.6, the non-top tenure.** `q (tau - M_i) <= 1 + 2 b_n(q)`
   with `tau - M_i >= delta/2` and `1 <= sqrt q` gives `q <= 4(1 + sqrt(2 ell))^2/delta^2`.
   Correct. The branch is unobservable at simulable horizons (`4 s_n = 0.26` at `n = 160000`), as
   both documents and `PRIVATE_BOUND_NOTES.md` Note 3 say; I did not test it and no simulation can.
9. **Branch exhaustiveness.** `G_{-i,z}` fails; `G` holds and `i` loses; `G` holds, `i` wins,
   `i` top and (strategic or `tau > mu_i`); `G` holds, `i` wins, `i` top, honest, `tau <= mu_i`;
   `G` holds, `i` wins, `i` not top. Exhaustive, and the case "`i` honest, not top, `tau <= mu_i`"
   is empty because `tau >= M_i + delta/2 > M_i >= mu_i` there. Correct.
10. **The error arithmetic.** `sum_z 2 b_n(V_z) <= sqrt(2 Q n ell_n)`; `sum_z V_z^2 <= n^2`;
    `n s_n <= sqrt(5/2) n^{2/3}(log n)^{1/3}(1 + o(1))` under `ell_n = log(2 n^5)`;
    `2 exp(-2 L_n s_n^2) = n^{-5}`. All correct.
11. **Revenue (B) and robustness (C).** The two places I pushed hardest were whether the winner can
    be priced above its own capacity (it cannot: `tau_z <= (beta_W - s_n)_+ <= M_W^z` on the good
    bidding event, whoever wins, because `beta_(2) <= beta_W`), and whether a non-top agent winning
    by a bid fluctuation ruins the revenue (it does not: on the good event the winner's capacity is
    within `2 s_n` of the top and still at least `tau_z`). Correct.

### 11.2 What I did not check

* The continuous or grid extension. Neither document claims one and I make no claim either.
  PROVER2's Corollary 4.3 marks the boundary correctly (primitives constant on each cell) and its
  reason for the boundary (a bid then estimates a cell-average delivered mean, the price may exceed
  an agent's capacity at some contexts inside the cell, and the coupling loses its fixed comparison
  target) is right as far as I can tell, but I did not attempt to falsify it.
* The non-top branch empirically. Impossible at simulable horizons.
* Whether the monitor-slack term `sqrt(2 Q n ell_n)` is attained. Unproved by both; see Section 10.1.
* PROVER1's Section 11 tests and PROVER2's Section 10 tests. I reran the mechanism from the
  specification rather than auditing their code, so my numbers are independent of theirs. Where
  they overlap they agree (PROVER2's Section 10 finding 2, the exact `L_n (M_i - m')` underbidding
  gain with zero variance, reproduces exactly in my runs).
* Any external citation. Neither document imports one and I imported none, so nothing needed
  checking against a primary source.
* Whether `S^*` is an exact equilibrium, and whether high revenue holds at every equilibrium.
  Neither is claimed.

### 11.3 What would have to be true for the remaining steps to break

Stated because it is the most useful thing I can give short of a counterexample.

* **Lemma L / Lemma 3 (locality).** Would break if any parameter of the mechanism were tuned to a
  realised global statistic rather than to `n` and `K`. Then the local phase at `z` would depend on
  data at `z'`, the price at `z` would stop being a function of the other agents' bids at `z`, and
  the cross-profile attacks of Section 5.1 items 1 and 2 would open. The mechanism as specified
  has no such parameter, and the paper should say that this is what makes locality a construction.
* **The winner-inclusion coupling.** Would break if the deviator could receive a different number
  of Stage-1 pulls at `z` in the two executions. Two ways: endogenous arrivals (Section 7.1, and
  the theorem is then false), or a Stage-1 schedule that depends on realised rewards. PROVER1
  promotes reward-independence of the schedule to a hypothesis (M1) and is right to.
* **The monitor charge.** Would break if the seed used at a primary pull were not fresh given
  everything realised before the target is chosen. Section 7.2 is exactly that failure, and it is
  worth `Theta(n)`.
* **The fallback bound.** Would break if a non-deviating agent's conditional mean when selected in
  a local fallback could fall below `V_i^z`. Under `S^*` it is exactly its capacity, so this needs
  `S^*` to stop delivering capacity in Stage 3, for instance if the phase message of (M6) were
  removed and an agent could not tell a fallback pull from a primary pull. Both documents identify
  the message set as load bearing and PROVER1 makes it a hypothesis.
* **The additive decomposition `u_i = sum_z E[U_{i,z}]`.** Would break only if utilities were not
  additive over rounds, which they are by definition. This is the step that absorbs the
  cross-profile deviator and it is the one step in either document that cannot be attacked.

## 12. On the agreement between the two provers

I was told not to treat agreement as evidence, and I did not. Three observations.

**The agreement is weaker evidence than it looks, because the two documents share upstream
sources.** Both localise the same scalar proof (`sections/appendix_private.tex`), both work from
the same contract, both adopt the architecture of `MATH_CANDIDATE_LEDGER.md` Section 4 (PROVER2
says so in Section 8, PROVER1 in Section 12), and both adopt the tightened top-agent accounting of
`PRIVATE_BOUND_NOTES.md` Note 1. So agreement on the architecture, on the per-profile
decomposition and on the branch structure is largely inherited, not independent. Where they were
genuinely independent, they differ (seed indexing, fallback tuning, calibration, schedule), and I
adjudicated each of those in Section 9.

**A common-mode error is exactly what I found.** Finding F2 is present in both documents in the
same form, because both inherited the phrasing of the contract's Section 1 ("targets are chosen
before fresh conditionally independent Bernoulli seeds") and both expanded it into a list of
pairwise independences. Two isolated provers reproduced the same under-specification, and it costs
`Theta(n)`. That is the concrete reason not to treat agreement as evidence. Similarly, both left
the same question open (whether endogenous arrivals break the theorem or merely the proof), and
neither looked; the answer, F1, is that the theorem is false.

**What I did that does not rest on either document.** I reimplemented PL-MESP from the
specification rather than from either prover's code, so every number in Sections 5, 7, 8 and 10 is
independent of theirs. I solved the primary phase exactly as a finite MDP rather than trusting
either document's upper bound, which is what let me say that the monitor allowance is tight within
a factor of exactly two rather than "plausible". I re-derived every constant (`exp(-ell_n) =
(2n^5)^{-1}`, `2 exp(-2 L_n s_n^2) = n^{-5}`, `3 sqrt 2/(sqrt 2 - 1) = 10.2427`,
`n s_n <= sqrt(5/2) n^{2/3}(log n)^{1/3}`, `sum_z 2 b_n(V_z) <= sqrt(2 Q n ell_n)`) rather than
reading them. And I attacked the hypotheses, which is the layer at which two proofs of the same
statement are both blind by construction.

**What would still worry me if I were the coordinator.** Nothing in either document, and nothing I
found, rules out an error in the scalar source that both localise. I checked
`sections/appendix_private.tex` only where the contextual proofs use it, and I did find one thing:
the scalar revenue proof's "`q` is a bounded stopping time for the primary filtration" is exactly
the step that both provers had to replace (PROVER2 by the martingale identity M(d), PROVER1 by the
phantom continuation), each for its own reason. Their replacements are correct; the scalar text's
version is the one that should be looked at by whoever owns Theorem `thm:private-mesp`, because
the same objection ("the primary phase can end for a reason that is not a stopping time of the
local reward filtration") does not arise in the scalar case only because the horizon cut there is
deterministic. That is a remark for the scalar owner, not a finding against this candidate.

## 13. Compute log

All runs are fully synthetic simulations of PL-MESP as specified in PROVER2 Section 2, or of a
single component of it, written from the specification rather than from either prover's code, so
the numbers are independent of theirs. None of them is evidence that the theorem is true; the two
that matter (Section 7) are evidence that two hypotheses are false as written. Code, seeds and raw
output: `<scratchpad>/round2/adversary-c2/`.

Python venv `<scratchpad>/venv/bin/python`, single threaded, NumPy only.
I did not write to the shared `COMPUTE_LOG.md` in this directory, which now records Prover 1's
runs; this section is my log.

| where | script | what | runtime |
|:-|:-|:-|:-|
| login node | `run_exog.py 4000 4 iid B` | smoke test of the mechanism and 21 deviations | 3 s |
| login node | `run_break.py endo 40000 {6} {1.0, 0.1, 0.0}` | F1 and the `eps` boundary case | 1 s each |
| login node | `run_break.py endo 160000 6 1.0` | F1 at a larger horizon | 4 s |
| login node | `run_break.py pairwise {200000, 1000000} 2` | F2 | 2 s, 9 s |
| login node | `run_award.py` | award rules, 400000 configurations, 800000 bid vectors | 14 s |
| login node | `run_fallback.py {2,3,5} 20000 {2,3,2}` | Lemma F versus the doubling fallback | 28 s, 20 s, 45 s |
| login node | `run_dp.py` | exact MDP optimum of the primary phase, 192 cells | 75 s |
| login node | `run_monitor.py` | Lemma M(b) pathwise under the DP-optimal policy, 24000 paths | 38 s |
| login node | `run_short.py 40000 8 63` | a profile that never finishes bidding | 4 s |
| login node | `run_exog.py 40000 8 iid K2` | `K = 2` with an exact capacity tie, 21 deviations | 26 s |
| login node | switch counter under `S^*`, 20 replications at each of `n = 4000, 40000, 160000` | Lemma M(c) | 20 s |
| Slurm 64566919 | `job.sh` (partition `cpu`, account `<slurm-account>`, 1 core, 4 GB, 3 h) | F2 at `n = 4000000` (3 replications); seven exogenous deviation searches at `n = 160000` with 12 replications and 21 deviations each, over arrival processes i.i.d., single block split, 40-block burst and deterministic alternating, on instances B, T, H and K2; `run_fallback.py` for `K = 2` and `K = 5` at `n = 100000` | about 50 min, completed |

The login-node runs are each well under a minute apart from `run_dp.py` (75 s),
`run_monitor.py` (38 s), `run_fallback.py` (28 s) and one `run_exog.py` (26 s); everything longer
went to Slurm. Raw output of the Slurm job is `logs/advc2-64566919.out`. All seven exogenous
searches completed (i.i.d., single block split and 40-block burst arrivals on instance B; i.i.d.
arrivals on instances T, H and K2; alternating arrivals on K2; all at `n = 160000` with 12
replications and 21 deviations each), together with F2 at `n = 4000000`. **Across all seven, zero
`VIOLATION` and zero `EXCEEDS BOUND` markers were printed**, for the aggregate bound and for every
per-profile allowance. The best gain in the last configuration (alternating arrivals, `K = 2`,
exact capacity tie at `z_1`) was `1807.6` against bound (A) `= 22915.4`, with the same
`underbid = 1039.05 = L_n x 0.15` Stage-1 component and zero variance, so the deterministic
alternating arrival process behaves exactly like the i.i.d. one, as (H3) predicts. The two
`run_fallback.py` calls at `n = 100000` also completed and reproduce the login-node ratios at a
five times larger horizon (`0.506` and `0.328` at `K = 2`, `0.116` and `0.064` at `K = 5`).
**The Slurm job printed no violation marker of any kind, in any of its runs.** Total runtime about
50 minutes on one core.
