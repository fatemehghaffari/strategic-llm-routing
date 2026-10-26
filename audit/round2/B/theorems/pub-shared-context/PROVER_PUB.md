# PROVER-PUB — shared context for the three public-capability contextual results

Scope: `thm:grid-ucb-robust`, `thm:grid-etc`, `thm:contextual-public` (+ `prop:two-top-sharp`).
Sources read in full: `sections/sec2_model.tex`, `sections/sec4_contextual.tex`,
`sections/appendix_contextual.tex` (the file `sections/app_contextual_public.tex` inputs),
`sections/appendix_samf.tex` (for `lem:ucb-deficit`, `lem:race`, `eq:gap-free-ucb`),
`sections/contextual_samf_algorithm.tex` and `sections/contextual.tex` (the dead
`aamas_body.tex` build, read only to compare wording).
Not read, per instruction: anything under `audit/round2/B/theorems/sc1-shared-context/`.
The private continuum result is out of scope and is only mentioned once, under "Cost of adopting this",
because the restriction has a consequence there that the caller must weigh.

Notation for this report. **SC** = the restated shared-context model: one common context
`x_t ∈ [0,1]^d` i.i.d. from a Borel probability `ν_d` (this is (A1) for a single context),
`M_i, μ_i : [0,1]^d → [0,1]` `L`-Lipschitz with `μ_i ≤ M_i`, grid of side `h_n` on `[0,1]^d`,
`J_n = h_n^{-d}` cells, cell diameter `√d·h_n`. **PM** = the paper's current profile model,
`X_t ∈ [0,1]^D`, `D = Kd`. **Diag** = PM instantiated with `ν` = the law of `(x,…,x)`, `x ~ ν_d`.

---

## 0. Headline answer

**Yes to (b), with one correction and one caveat; (a) is half right.**

1. Restated in SC from the outset, all three results go through with `d` in place of `D`
   everywhere, `J_n = h_n^{-d}`, exponents `(d+1)/(d+2)` and `(d+2)/(d+3)`, inflation radius
   `√d·h_n`, and the constants `2^{D+1} → 2^{d+1}`. **The `√d` in the Lipschitz term is literally
   unchanged**, and the caller's reading of why is correct: in PM that `√d` is the diameter of an
   agent's *block*, not of the full cell, so it never was a `D` quantity. Every proof step survives;
   see §1–§6 for the step-by-step verification.

2. **(a) is half right.** The caller's specific observation is correct: on Diag, for the natural
   "trace" region `R_Δ = {(x,…,x) : x ∈ R_0}`, the diagonal has empty interior in `[0,1]^D` for
   `K ≥ 2`, so `∂R_Δ = cl(R_Δ)` and `ν(∂R_Δ) = ν_d(cl(R_0))`, which is `1` for `R_0 = [0,1]^d`.
   The stated remainders are then vacuous and `thm:grid-etc`'s hypotheses are unsatisfiable.
   **But nothing becomes false.** Two rescues exist inside PM, and I am obliged to report them:
   - taking cylinders `R = {X : x_1 ∈ R_0}` instead of traces gives `∂R = ∂R_0 × [0,1]^{(K-1)d}`,
     so `ν(∂R) = ν_d(∂R_0) = 0` whenever `R_0` has `ν_d`-null boundary. Sharp adaptivity on Diag
     is then fine, at the `D`-exponent.
   - the topological charge `n·ν((∂R)^{√D h_n})` is a *lossy surrogate*. The real error is the mass
     of cells that straddle `R` **in measure**, and `lem:cell-average-l1` (already in the paper)
     makes that mass vanish for *every* measurable `R` and every Borel `ν`, with no boundary
     condition at all. I give the proof in §2.3 and I am willing to sign it. With that step,
     the trace regions on Diag are fine too.
   So the honest verdict is: **Diag is proof-broken, not theorem-broken.** The one clause where
   Diag genuinely has no non-trivial applicable case is **FATA**, because `G_ij` is not chosen by
   the author — it is `{X : M_i(x_i) = M_j(x_j) = M_⋆(X)}`, which for non-constant capabilities
   has empty interior in `[0,1]^D` and therefore equals its own boundary. Witness in §2.4.
   Even there the *conclusion* survives on Diag in the example I built (§2.4), so I will not claim
   more than "the stated hypothesis is unsatisfiable".

3. **The real reasons to adopt SC are two, and neither is the one in the hypothesis.**
   - *The exponent.* `(d+2)/(d+3)` vs `(Kd+2)/(Kd+3)` is a large, real gain, and it is **not
     knowledge-free** in PM: lazy initialisation shrinks the exploration terms but leaves the
     Lipschitz term `L√d·n h_n` untouched, and that term alone already sits at the `D`-exponent.
     You must retune `h_n` and `q_n` to `d`. In SC that retuning is free because `d` is the
     dimension of the observed context space. §7.
   - *The two-top condition stops being degenerate.* **New finding, §4.3:** if `ν` is a product
     measure across agents (independent contexts) and `K = 2`, then "two agents attain the largest
     capacity at `ν`-a.e. profile" **forces both capability functions to be `ν`-a.s. constant and
     equal** (one-line Fubini). So in PM with independent blocks, `thm:contextual-public` and
     `thm:grid-ucb-robust`'s equilibrium clause apply essentially only to constant capabilities —
     i.e. the contextual hypothesis is near-vacuous exactly where the paper wants it. In SC the
     condition is satisfied by any pair with `M_i ≡ M_j` non-constant dominating the rest, which
     is precisely the router-with-redundant-providers story. **This is the strongest argument in
     the audit for the restriction, and it is an argument about content, not about rates.**

4. **One thing SC does not buy:** the `ν(∂G_ij(R)) = 0` condition on FATA stays, and I could not
   remove it. §2.4, §6, "Open or doubtful".

---

## 1. The conditional i.i.d. reduction (`lem:cell-law`)

### 1.1 The statement I sign, in SC

> **Lemma (cell law, SC).** Fix a deterministic cell `C ⊆ [0,1]^d` with `ν_d(C) > 0`.
> Condition on any realised ex ante strategy map profile `(m_{1,n},…,m_{K,n})` and on the
> membership-indicator sequence `(1{x_t ∈ C})_{t≤n}`. Then the ordered contexts at the visits to `C`
> are i.i.d. `ν_d(· | C)`. If the platform's selection at each visit is cell-blind, then, writing
> `m̄_{i,C} := E[m_{i,n}(x) | x ∈ C]`:
> **conditionally on everything determined before the `k`-th visit to `C` — the realised map
> profile, the membership-indicator sequence, the exact contexts and selections and realised
> rewards at visits `1,…,k−1`, the mechanism's coins drawn up to and including the selection coin
> at visit `k`, and hence the selected agent `I^{(k)}` — the realised reward `Y^{(k)}` is
> `Bernoulli(m̄_{I^{(k)},C})`.**
> Consequently the joint law of the whole cell execution `(I^{(1)},Y^{(1)},I^{(2)},…)` coincides
> with its law under the artificial realisation `Y^{(k)} = 1{U_{C,a,k} ≤ m̄_{a,C}}` on independent
> uniform tapes indexed by (cell, agent, that agent's own local pull count).

### 1.2 Does it survive perfect cross-agent dependence? Yes.

**The one-line reason: exactly one agent is selected per round, so the potential outcomes of the
other `K−1` agents at that round are never observed and never enter any bound.** Cross-agent
dependence of `(Y_1^{(k)},…,Y_K^{(k)})` is therefore invisible to the mechanism and to the analysis.

The exact conditional independence used is the one displayed above and nothing else: the reward at
a visit is conditionally Bernoulli with the selected agent's cell-average parameter *given
everything determined before it*. Two ingredients produce it, and I check both in SC:

- *(i)* Conditionally on everything determined before visit `k`, the pair (context `x^{(k)}`, the
  fresh uniform used for the reward) has law `ν_d(·|C) ⊗ Unif[0,1]`. This uses only that the single
  context sequence is i.i.d. and independent of reward randomness — (A1) for one context. No
  product structure across agents is available or needed; there is only one context variable now.
- *(ii)* Cell-blindness: conditionally on everything determined before the selection at visit `k`,
  and in particular *not* on `x^{(k)}` beyond its cell, `I^{(k)}` is a function of that past and an
  independent coin. Hence `I^{(k)} ⫫ x^{(k)}` given the past, and
  `P(Y^{(k)} = 1 | past, I^{(k)} = i) = E[m_{i,n}(x)|x∈C] = m̄_{i,C}`.

The final sentence of the lemma (law-equality with the independent-tape realisation) is a genuine
step, not a restatement, and it is the one that would be at risk if it were stated as "the tapes are
independent". It is proved by induction on `k`: the law of the execution is determined by the
transition kernel "given the past and the selection `i`, reward `~ Bern(m̄_{i,C})`", and that kernel
is identical under the true correlated randomness and under independent tapes. This is valid
precisely because the algorithm observes only the selected agent's reward.

**Verdict: the source already anticipated this.** `lem:cell-law` in `appendix_contextual.tex` says
verbatim "Coordinates are correlated across agents through the shared profile; the per-agent
concentration arguments below never use independence across agents", and `lem:etc-tail` says "The
observations of the two agents need not be independent of one another". In PM `ν` is an *arbitrary*
Borel law on `[0,1]^D`, so PM already permits perfectly dependent blocks — Diag is a legal `ν`.
SC therefore introduces **no new dependence at all**; it introduces a *guaranteed* dependence where
PM permitted an arbitrary one. Nothing in the reduction changes.

Two further checks I made rather than inherited:

- *Raising a map.* `m̄_{j,C}` depends only on `m_{j,n}` and `ν_d(·|C)`. A pointwise raise of
  `m_{i,n}` raises `m̄_{i,C}` in every cell (monotonicity of the integral) and moves no other cell
  average. Needed by §3.
- *In ETC exploration the dependence is not even latent.* The `q_n` exploration pulls of agent `a`
  in a cell occur at `q_n` **distinct** visits, so `a`'s and `b`'s exploration observations are
  driven by *different, independent* contexts. So in SC the `K` exploration empirical means in a
  cell are in fact mutually independent. `lem:etc-tail`'s "need not be independent" is slack here.

**Verdict for §1: verbatim, `D → d`, `X → x`, `x_{i,t} → x_t`. No hypothesis strengthens.**

---

## 2. Every boundary condition

### 2.1 The inflation radius

**Yes, `√D h_n → √d h_n`, and the step is correct in SC.** Proof of the step (I checked it rather
than inherited it): let the cell `C` (a closed cube of side `h_n` in `[0,1]^d`, diameter `√d h_n`)
meet both `R` and `R^c`, say `y ∈ C∩R`, `z ∈ C∩R^c`. Put `s⋆ := sup{s ∈ [0,1] : y + s(z−y) ∈ R}` and
`p := y + s⋆(z−y)`. Then `p ∈ cl(R)`; `p ∉ int(R)` (if `s⋆ < 1` the sup would be beaten, and `s⋆ = 1`
gives `p = z ∉ R`, `z ∈ cl(R)` would force `z ∈ ∂R ⊆` the conclusion anyway). So `p ∈ ∂R ∩ C`,
and every point of `C` is within `diam(C) = √d h_n` of `p`. Hence `C ⊆ (∂R)^{√d h_n}`. The same
argument in `[0,1]^D` gives `√D h_n`, which is where the source's constant comes from. ∎

Asymptotically the change is only a constant: under `ν_d(∂R) = 0`, `(∂R)^{ε} ↓ ∂R` as `ε ↓ 0`
(`∂R` closed), so continuity from above gives `ν_d((∂R)^{√d h_n}) → 0` either way. It matters only
at the level of the explicit remainder.

### 2.2 `ν(∂R) = 0`

Formally unchanged: `R` is now an ordinary measurable subset of `[0,1]^d` and `ν_d` an arbitrary
Borel probability there, so as an abstract hypothesis it is neither harder nor easier. **In
practice it is strictly easier**, and this is the substance of the caller's (a): on Diag it is
unsatisfiable for trace regions (`ν(∂R_Δ) = ν_d(cl(R_0)) > 0` whenever `ν_d(R_0) > 0`, `= 1` for
`R_0 = [0,1]^d`), whereas in SC boxes, balls, finite unions, and sublevel sets of continuous
functions all qualify as soon as `ν_d` charges no `(d−1)`-dimensional set.

### 2.3 NEW: the condition is removable for sharp adaptivity, in both models

The topological charge is lossy. Write `C_n(x)` for the cell containing `x`,
`θ_n(x) := ν_d(R | C_n(x))` on positive-mass cells, and
`κ_n(R) := ‖θ_n − 1_R‖_{L^1(ν_d)}`. By `lem:cell-average-l1` applied to `f = 1_R` — a lemma the
paper already proves for an **arbitrary** Borel measure on a compact metric space —
`κ_n(R) → 0` for every measurable `R` and every `ν_d`, with **no boundary condition**.

> **Claim (sign).** Static-grid UCB satisfies contextual sharp adaptivity for **every** measurable
> `R ⊆ [0,1]^d` with remainder `E_n + 2√2 · n · √(κ_n(R))`, and `κ_n(R) → 0`. Likewise for
> Static Grid-ETC with its own `E_n`.

*Proof.* Extend `lem:region` from `g = 1_R` to any bounded measurable `g` — the proof is unchanged,
since it only uses that the selection at a cell visit is independent of the context at that visit
given the past: `E Σ_{t : x_t ∈ C} 1{I_t = i} g(x_t) = E T_i(C) · E[g | C]`. Take
`g = 1_R·(b − m_{i,n})` and put `ψ_C := E[1_R (b − m_{i,n}) | C]`. The quantity to bound above in
the sharp-adaptivity inequality is exactly `Σ_C E T_i(C) ψ_C`. Two bounds:
`ψ_C ≤ θ_C` (since `b − m_i ≤ 1`), and
`ψ_C ≤ (b̄_C − m̄_{i,C}) + (1 − θ_C)` (since `m_i − b ≤ 1`). Fix `ε ∈ (0,½)` and split the cells:
- `θ_C ≤ ε`: contributes `≤ ε Σ_C E T_i(C) ≤ εn`.
- `θ_C ≥ 1 − ε`: contributes `≤ Σ_C E T_i(C)(b̄_C − m̄_{i,C})_+ + εn ≤ E_n + εn`, the first sum
  being exactly the existing per-cell deficit bound (Lipschitz comparison + `lem:ucb-deficit` +
  Jensen + Cauchy–Schwarz), restricted to a subset of cells.
- `θ_C ∈ (ε, 1−ε)`: contributes `≤ Σ E T_i(C) ≤ n · ν_d(∪ such cells)`, and for `x` in such a cell
  `|θ_n(x) − 1_R(x)| > ε`, so that mass is `≤ κ_n(R)/ε`.
Total `≤ E_n + 2nε + n κ_n(R)/ε`; optimise `ε = √(κ_n/2)` to get `E_n + 2√2 n √(κ_n)`. ∎

This is **new** (my addition), applies equally in PM and SC, and removes `ν(∂R) = 0` from
`thm:grid-etc`'s hypotheses and the `n ν((∂R)^{√d h_n})` term from `thm:grid-ucb-robust`. Cost: it
gives `o(n)` with no rate, whereas the topological version gives a rate when
`ν((∂R)^ε) = O(ε)`. I would state both.

### 2.4 `ν(∂G_ij(R)) = 0` — this one stays, in both models

In SC, `G_ij(R) = R ∩ {x : M_i(x) = M_j(x) = M_⋆(x)}`, an ordinary subset of `[0,1]^d` cut out by an
equality of Lipschitz functions. The condition is now **satisfiable and meaningful**: with
`M_1 ≡ M_2 ≥ max_l M_l` one gets `G_12(R) = R` and `∂G_12(R) = ∂R`. That is strictly better than
Diag, where the two-top set has empty interior in `[0,1]^D` for non-constant capabilities and
therefore equals its own boundary, so no non-trivial `R` satisfies the hypothesis. Witness for
Diag: `K = 2`, `d = 1`, `M_1(x_1) = x_1`, `M_2(x_2) = x_2`; then
`{X : 1,2 ∈ T(X)} = {x_1 = x_2} = Δ`, `∂Δ = Δ`, `ν(∂G_12(R)) = ν_d(R_0) = 1` for `R_0 = [0,1]`.
**However**, in that same example every visited cell satisfies `ν(G|C) = 1`, so the exchangeability
argument applies `ν`-a.e. and FATA *holds* — Diag's failure is again of the hypothesis, not of the
conclusion. I report this rather than claim a witness I do not have.

The condition is **not removable** in SC. The `ε`-then-`ε→0` device of §2.3 does not work here,
because near-exchangeability in a cell with `1 − θ_C = δ` requires a *quantitative* stability of
UCB/ETC counts under a perturbation `δ` of the arm means, and the threshold at which the two agents'
commitment probabilities separate is `δ ≍ q_n^{-1/2} → 0`. Bounding the mass of cells with
`1 − θ_C ≥ q_n^{-1/2}` by `κ_n(R) · q_n^{1/2}` is useless because `lem:cell-average-l1` gives no
rate on `κ_n`. The asymmetry with §2.3 is real: there the penalty was linear in a *fixed* `ε`.

**Verdict for §2: `√D → √d` genuine; `ν(∂R)=0` unchanged in form, strictly easier in practice,
and removable altogether by §2.3; `ν(∂G_ij(R))=0` unchanged in form, satisfiable in SC and
unsatisfiable on Diag, and not removable in either.**

---

## 3. Monotonicity — the index race under the common-uniform coupling

### 3.1 UCB (`thm:grid-ucb-robust`): exact, remainder zero, **verbatim**

Fix a cell `C`, condition on its membership sequence, realise rewards from
`1{U_{C,a,k} ≤ m̄_{a,C}}` (legitimate by the last clause of `lem:cell-law`, §1.1). Raising
`m_{i,n}` pointwise raises `m̄_{i,C}` in every cell and moves no other cell average, so it raises
`i`'s tape pointwise, hence its empirical means, hence its whole index sequence
`f_i(k) = m̂_i(k) + √(4 log n / k)`; every other agent's index sequence is a function of its own
count and its own tape and is untouched. `lem:race` gives `T'_j(C) ≤ T_j(C)` for every `j ≠ i`, on
every sample point when the cell's priority is drawn once before play. `lem:region` converts to
`E T_j(C ∩ R) = ν_d(R|C) E T_j(C)` — and `ν_d(R|C)` is a property of `ν_d` and `R` alone, identical
in both executions — so summing the finitely many cells gives `E T_j(R)` weakly smaller, remainder
exactly zero, for **every** measurable `R`, no boundary condition. The known-horizon width is what
keeps the index a function of the agent's own count (cf. `rem:anytime`).

Nothing here sees `D`, `d`, the number of agents, or the dependence structure. Verbatim.

### 3.2 Ties between agents — checked explicitly, not inherited

Ties in *index value* are what matter, and under a shared context with `M_i ≡ M_j` they occur with
probability bounded away from zero (identical cell averages ⇒ identical tape laws ⇒ frequent equal
empirical means at equal counts).

- `lem:race` handles them by construction: its proof compares the lexicographic pairs
  `(e_a(k'), a) > (e_j(k−1), j)` where `a` ranges over a **strict** priority order. Equal index
  values are therefore broken by a total strict order, and "raising agent 1 can only enlarge that
  counting term" is unaffected by how many ties there are. The conclusion `T'_j(t) ≤ T_j(t)` is
  pathwise.
- Under independent per-round tie coins the source gives the expectation version via a
  first-violation argument over two independent coin families. I read it; it is a sketch, but it is
  the same sketch in PM and SC and the tie *frequency* does not enter it. I flag it as the weakest
  written step in the whole chain, unchanged by the restriction.

### 3.3 ETC (`thm:grid-etc`): pathwise — I verified the tie step from scratch

The claim "raising one score can leave the winner unchanged or replace it by `i`; it cannot make
`j ≠ i` newly win" is the only place where a tie could bite, so I proved it rather than read it.
Commitment picks the lexicographic maximum of `(m̂_a, π_a)` where `π` is the cell's independent
uniform priority permutation, drawn once and shared by the two coupled executions. Let `W` be the
winner before and `W'` after raising `m̂_i` to `m̂'_i ≥ m̂_i`.
- If `W = i`: `(m̂_i, π_i)` was lex-max and only it rose, so `W' = i`.
- If `W = j ≠ i`: `(m̂_j, π_j)` still lex-beats every `(m̂_a, π_a)` with `a ≠ i`, unchanged. So
  `W' ∈ {j, i}` according to whether `(m̂'_i, π_i)` lex-beats `(m̂_j, π_j)`.
Hence `W' ∈ {W, i}` and `1{W' = j} ≤ 1{W = j}` for every `j ≠ i`, **pathwise, ties included**,
because the lexicographic order is total and strict. ∎ Two more checks:
- the exploration schedule in a cell is a function of the cell permutations and the context
  sequence only, so it is identical in the two executions, `j`'s exploration count is *equal*, and
  `j`'s exploration rewards use the same uniforms and the same map `m_{j,n}`;
- a truncated cell (`V_C < K q_n`) never commits, and there `T_j(C)` is determined by the
  permutations alone, hence equal in both executions.
Feasibility `1{U ≤ M_i(x)} ≥ 1{U ≤ m_{i,n}(x)}` is pointwise in `x` and needs no distributional
hypothesis. The coupling is over the *true* exact-context randomness, not over cell averages, so
it never touches §1's tape-replacement step.

**Verdict for §3: verbatim in SC for both rules; ties are handled by construction and I have
re-derived the ETC tie step. The shared context contributes nothing new here — this section is
pure re-labelling.**

---

## 4. The two-top condition and `prop:two-top-sharp`

### 4.1 Restatement in SC

> Two agents attain the largest capacity at `ν_d`-almost every context: for `ν_d`-a.e. `x` there
> are `i ≠ j` with `M_i(x) = M_j(x) = M_⋆(x)`, equivalently `|T(x)| ≥ 2` a.e.

The pair may vary with `x`; the proof uses no constant top set, no continuity, no null separator,
no component structure (the source says so and I confirmed it — the only place the rival enters is
through `max_{j≠i} M̄_{j,C}`, a single agent per cell, and the bound holds however the pointwise
argmax rotates).

### 4.2 The two places it is used, both verified in SC

- *`L¹` limit.* `Σ_C ν_d(C) η_{i,C} → E[(M_i(x) − max_{j≠i} M_j(x))_+]`, by `lem:cell-average-l1`
  applied to each `M_j` (the map `u ↦ (u_i − max_{j≠i} u_j)_+` moves by at most `Σ_l |u_l − u'_l|`).
  `lem:cell-average-l1` is stated and proved for an **arbitrary** Borel probability on a compact
  metric space with mesh `→ 0`; `[0,1]^d` is compact. No density, no full support, no positive mass
  on cells. Two-top a.e. makes the limit `0`. Verbatim.
- *Lipschitz rate.* For `x, x' ∈ C`, `|x − x'| ≤ √d h_n`, so `M_j(x) ≤ M̄_{j,C} + L√d h_n` on all of
  `C`; a.e. `x ∈ C` has `M_i(x) ≤ max_{j≠i} M_j(x)`; integrating,
  `M̄_{i,C} ≤ max_{j≠i} M̄_{j,C} + L√d h_n`, i.e. `η_{i,C} ≤ L√d h_n`. **Identical, `√d` untouched.**
  Same for `β_C ≤ L√d h_n` via `M_⋆(x) = max_j M_j(x) ≤ max_j M̄_{j,C} + L√d h_n`.

### 4.3 NEW — the condition is degenerate under a product `ν`, which is an argument *for* SC

> **Claim.** Let `K = 2` and `ν = ν_1 ⊗ ν_2` on `[0,1]^{2d}` (independent contexts). If
> `M_1(x_1) = M_2(x_2)` for `ν`-a.e. `(x_1,x_2)`, then `M_1 = M_2 = c` `ν_1`- resp. `ν_2`-a.s. for
> a constant `c`.

*Proof.* Fubini: for `ν_1`-a.e. `x_1`, `M_2(x_2) = M_1(x_1)` for `ν_2`-a.e. `x_2`. Fix one such
`x_1` and set `c := M_1(x_1)`; then `M_2 = c` `ν_2`-a.s., and feeding that back gives `M_1 = c`
`ν_1`-a.s. ∎

So in PM with independent blocks the two-top hypothesis (`K = 2`) is satisfied only by constant
capabilities, i.e. by instances in which the whole contextual apparatus is idle. For `K ≥ 3` the
hypothesis needs the pushforward laws `M_i(x_i)` to share atoms and remains severely restrictive
(a tie at the top must occur at a.e. profile, and each `{M_i(x_i) = M_j(x_j)}` is `ν`-null unless
the laws are atomic). I have proved only the `K = 2` case; see "Open or doubtful".

In SC the same condition is satisfied by, e.g., `M_1 ≡ M_2` any non-constant Lipschitz function
dominating the others — exactly two providers that are equally good on every query, which is the
motivating instance. **This is the substantive gain from the restriction: it is what makes the
paper's two-top condition a hypothesis about redundancy rather than a hypothesis about triviality.**

### 4.4 `prop:two-top-sharp` in SC — sharpness survives, verbatim

I walked the whole proof. `s_i := M_i` (strategic) or `M_i − μ_i` (honest);
`U_i := {x : T(x) = {i}}`. Each step:
- `g_0, A` by continuity from below on `U_i ∩ {s_i > 0} = ∪_k ({M_i − max_{j≠i} M_j ≥ 1/k} ∩ {s_i ≥ 1/k})`. ✓ works in `[0,1]^d`.
- good cell: `ν_d(A|C) ≥ ½` and `M̄_{i,C} − max_{j≠i} M̄_{j,C} ≥ 3g_0/4`; `m'_n := M_i − (g_0/2)1_A`
  on good cells, `M_i` elsewhere. Feasible; honest-feasible because `s_i ≥ g_0 > g_0/2` on `A`. ✓
- `δ_C = (g_0/2)ν_d(A|C) ∈ [g_0/4, g_0/2]`; deviating cell mean still exceeds every rival's by
  `≥ 3g_0/4 − g_0/2 = g_0/4`. ✓
- `ρ_n = 2(K−1)exp(−q_n g_0²/32)` from `lem:etc-tail` with `Δ = g_0/4` and a union over rivals. ✓
- per-visit gain `≥ (1−ρ_n)g_0/4 − ρ_n ≥ g_0/8` for large `n`; the `−ρ_n` is right because baseline
  per-pull utility is `1 + μ_i − M_i ∈ [0,1]` (using `μ_i ≤ M_i`). ✓
- good-cell mass `≥ ν_d(A)/2` for large `n`: `ν_d(A ∩ {f^{(n)} < ½}) ≤ 2‖f^{(n)} − 1_A‖_1 → 0` with
  `f^{(n)}(x) = ν_d(A|C_n(x))`, and the same for the gap condition via `lem:cell-average-l1`. ✓
- `Σ_{good} E[N_C] ≥ n ν_d(A)/2 − K q_n J_n ≥ n ν_d(A)/4` eventually, since `q_n J_n = o(n)`. ✓
- total `≥ (g_0/8)(n ν_d(A)/4) = g_0 ν_d(A) n / 32`. ✓ matches the source constant.
- converse: `min{η_{i,C}, E[s_i 1{x ∉ U_i} | C]}`; `L¹` limits are `(M_i − max_{j≠i} M_j)_+` (zero
  off `U_i`) and `s_i 1_{U_i^c}` (zero on `U_i`), so the limit of the min is `0` at a.e. `x`, and
  `min{a_n,b_n} ≤ min{a,b} + |a_n−a| + |b_n−b|` transfers it to `L¹`. ✓

The only `D`-dependence is inside `q_n, J_n` through `q_n J_n = o(n)`, which holds for any `d`.
**Sharpness survives verbatim, `D → d`.** And by §4.3 the proposition is now the *interesting* half:
under a product `ν`, `U_i` has positive mass for essentially every non-degenerate instance, so PM's
sharpness proposition is the one that always applies and PM's positive theorem is the one that
rarely does. SC reverses that.

---

## 5. The balance, with arithmetic, and the exponents

### 5.1 Static-grid UCB

`E_n = L√d · n h_n + 4√(J_n n log n) + 3 min{J_n, n}`, `J_n = h_n^{-d}`.
Balance the first two: `n h_n = √(n log n) · h_n^{-d/2}` ⟺ `h_n^{(d+2)/2} = (log n / n)^{1/2}` ⟺

    h_n ≍ (log(en)/n)^{1/(d+2)},    J_n ≍ (n/log n)^{d/(d+2)}.

Then
- `n h_n = n^{(d+1)/(d+2)} (log n)^{1/(d+2)}`;
- `√(J_n n log n) = n^{1/2 + d/(2(d+2))} (log n)^{1/2 − d/(2(d+2))} = n^{(d+1)/(d+2)} (log n)^{1/(d+2)}`
  (exponent of `n`: `(d+2+d)/(2d+4) = (d+1)/(d+2)`; of `log n`: `(d+2−d)/(2d+4) = 1/(d+2)`);
- `J_n ≤ n^{d/(d+2)} = o(n^{(d+1)/(d+2)})`, so the `3 min{J_n,n}` term is never binding.

    E_n = O( n^{(d+1)/(d+2)} (log n)^{1/(d+2)} ),   leading constant (L√d + 4).

### 5.2 Static Grid-ETC

Three errors: Lipschitz bias `n h`, exploration `q · h^{-d}`, simple regret `n q^{-1/2}`.
`n h = n q^{-1/2}` ⟹ `h = q^{-1/2}`; then `q h^{-d} = q^{1+d/2}` and equating with `n q^{-1/2}`:
`q^{(d+3)/2} = n`, so

    q_n = ⌈n^{2/(d+3)}⌉,   h_n ≍ n^{-1/(d+3)},   J_n = O(n^{d/(d+3)}),

and all three errors equal `n^{(d+2)/(d+3)}`. With `h_n` the largest dyadic `≤ n^{-1/(d+3)}` (so
`½ n^{-1/(d+3)} < h_n ≤ n^{-1/(d+3)}`): `J_n ≤ 2^d n^{d/(d+3)}`, `q_n ≤ 2 n^{2/(d+3)}`, hence

    q_n J_n ≤ 2^{d+1} n^{(d+2)/(d+3)},   n h_n ≤ n^{(d+2)/(d+3)}.

### 5.3 Exponents

| rule | PM | SC |
|---|---|---|
| Static-grid UCB | `n^{(D+1)/(D+2)}(log n)^{1/(D+2)}`, `D = Kd` | `n^{(d+1)/(d+2)}(log n)^{1/(d+2)}` |
| Static Grid-ETC | `n^{(D+2)/(D+3)}` | `n^{(d+2)/(d+3)}` |
| `thm:contextual-public` gain | `(2^{D+1} + c_1 + L√d) n^{(D+2)/(D+3)}` | `(2^{d+1} + c_1 + L√d) n^{(d+2)/(d+3)}` |
| `thm:contextual-public` revenue | `(K2^{D+1} + (K−1)c_1 + L√d) n^{(D+2)/(D+3)}` | `(K2^{d+1} + (K−1)c_1 + L√d) n^{(d+2)/(d+3)}` |

`c_1 = 2e^{-1/2}` unchanged. The `L√d` is unchanged in *both* columns; the caller's observation is
confirmed and the reason is that in PM it is the diameter of a `d`-dimensional block.

---

## 6. Product structure, density, full support, positive mass on cells

I scanned every step of the three proofs and every lemma they call.

| step | uses product structure across agents? | density? | full support? | positive cell mass? |
|---|---|---|---|---|
| `lem:cell-law` | **no** (source disclaims it explicitly) | no | no | only to define `m̄_{i,C}`; null cells are never visited |
| `lem:region` | no | no | no | same |
| `lem:ucb-deficit` | n/a (scalar bandit) | no | no | no |
| `lem:race` | n/a (deterministic combinatorics) | no | no | no |
| `eq:gap-free-ucb` | n/a | no | no | no |
| `lem:etc-tail` | **no** (source disclaims it explicitly) | no | no | no |
| `lem:cell-average-l1` | no | **no** — arbitrary Borel measure on a compact metric space | **no** | null cells set to zero |
| Lipschitz comparisons (`b̄_C`, `η_{i,C}`, `β_C`) | no | no | no | no |
| boundary charge | no | no | no | no |
| `E[N_C] ≤ n ν(C)`, `Σ_C E T_i(C) ≤ n` | no | no | no | no |
| `prop:two-top-sharp` | no | no | no | good cells have positive mass by construction |

**Nothing in the public-capability chain uses a product structure across agents, a density, full
support, or positive mass on cells.** The lemma that carries the most weight for a lower-dimensional
support — `lem:cell-average-l1` — is proved for an arbitrary Borel measure, and its proof (density
of continuous functions in `L¹` of a finite Borel measure on a compact metric space + modulus of
continuity + `L¹`-contractivity of conditional expectation) is indifferent to the support.

Where a lower-dimensional support *does* bite is **tuning, not correctness**: `J_n = h_n^{-D}`
over-counts the cells that exist, and `h_n` is chosen from `D`. See §7.

Two further checks:
- *Grid structure.* Cubes are used only for the diameter (`√d h_n`), the count (`h_n^{-d}`) and
  mesh `→ 0`. Any partition family with vanishing mesh works.
- *The "agents observe only their own contexts" caveat in `sec2_model.tex` collapses in SC*, since
  there is a single context that everyone sees. One fewer case to state.
- *"Independent ex ante mixtures" is an unnecessary qualifier* in all three theorems: the per-
  realisation bounds do not depend on the realised map, so conditioning and averaging works for an
  arbitrary joint mixture. Unchanged by the restriction, but worth fixing while editing.

---

## 7. Lazy initialisation — is the improvement knowledge-free?

**No, not in PM; yes in SC, for the only reason that matters.** Precisely:

- Lazy initialisation legitimately replaces `J_n` by `N_n := #{C : ν(C) > 0}` in the **exploration**
  terms only: `4√(J_n n log n)`, `3 min{J_n,n}` (UCB) and `q_n J_n` (ETC). On Diag with a product
  grid, `N_n = b_n^d = h_n^{-d}`, not `h_n^{-D}` (only the "diagonal" cells carry mass; cells
  meeting the diagonal on a shared face are a `ν`-null concern unless `ν_d` charges the grid
  hyperplanes).
- It does **nothing** to `L√d · n h_n` (UCB) or `2L√d · n h_n` (ETC), which do not contain `J_n`
  at all and which, at the `D`-tuned `h_n`, already sit at `n^{(D+1)/(D+2)}` resp.
  `n^{(D+2)/(D+3)}`. So with `D`-tuned parameters and lazy init on Diag:
  exploration `q_n N_n = n^{2/(D+3)} · n^{d/(D+3)} = n^{(d+2)/(D+3)}` (tiny), but the total is still
  `n^{(D+2)/(D+3)}`, driven by the Lipschitz term and the simple-regret term `n q_n^{-1/2}`.
- To reach `n^{(d+2)/(d+3)}` one must set `h_n ≍ n^{-1/(d+3)}` and `q_n = ⌈n^{2/(d+3)}⌉` — i.e.
  **retune to `d`**. Doing so *in PM* then works: with lazy init, exploration becomes
  `q_n N_n = n^{2/(d+3)} n^{d/(d+3)} = n^{(d+2)/(d+3)}` and all three terms balance again. Same
  story for UCB with `h_n ≍ (log(en)/n)^{1/(d+2)}`.
- Therefore: **the improvement is a retuning, not an adaptation.** In the restated SC model the
  retuning is free, because `d` is the dimension of the observed context space and the platform
  knows it by hypothesis. As "adaptation to an unknown low-dimensional support inside the profile
  model", it is not free and must not be claimed.

**Defect found in the live draft.** `sections/sec4_contextual.tex` (the file `aamas2027.tex`
actually builds) says:

> "Cells are initialized lazily, so every count of cells above may be replaced by the number of
> cells that carry positive mass. The exploration terms therefore adapt on their own to a context
> law supported on a lower-dimensional set, with no knowledge of that set, no estimate of its
> dimension, and no change to the rule."

The older, now-dead `sections/contextual_samf_algorithm.tex` has the same remark **followed by**:

> "The exponent does not improve: the Lipschitz term `L√d n h_n` is unaffected and already attains
> the stated rate, so a gain in the exponent requires retuning `h_n` to the lower dimension, which
> the platform does not know."

That sentence is correct and was dropped. As it now stands the live remark invites the reader to
infer an exponent improvement that does not hold. **Restore it** (or its SC analogue: if `ν_d`
concentrates on a `d' < d` dimensional subset of `[0,1]^d`, the exploration terms adapt but the
exponent still needs `h_n` tuned to `d'`).

---

## 8. Mandatory hostile pass

I tried to build an explicit counterexample to each result **in SC**. All three attempts failed;
here is what each attempt was and why it failed.

### 8.1 Against `thm:grid-ucb-robust` in SC

- *Attack: use the perfect cross-agent dependence to game the cell statistics.* **Fails.** Under
  `S_HDS` the agent's only lever is its ex ante map, and by §1 the cell instance depends on the map
  profile only through `(m̄_{a,C})_a`. The achievable set of `(m̄_{i,C})_C` for agent `i` is exactly
  `∏_C [0, M̄_{i,C}]` (resp. `[μ̄_{i,C}, M̄_{i,C}]` when honest), by scaling within each cell
  independently — identical to the PM deviation problem. No new channel exists.
- *Attack: rotate the top pair rapidly so no single rival is close in any cell.* **Fails.** The
  bound needed is `max_{j≠i} M̄_{j,C} ≥ M̄_{i,C} − L√d h_n`, and its proof integrates
  `M_i(x) ≤ max_{j≠i} M_j(x)` (true a.e. under two-top) against
  `max_{j≠i} M_j(x) ≤ max_{j≠i} M̄_{j,C} + L√d h_n` (true on all of `C`). The rival attaining the
  cell-average max is a single fixed agent per cell and the bound is indifferent to how the
  pointwise argmax rotates.
- *Attack on monotonicity: find a raise that increases `E T_j(R)`.* **Fails.** The only entry
  points would be a change to `m̄_{j,C}` (impossible — it depends on `m_{j,n}` and `ν_d(·|C)` only),
  to the partition (deterministic), or to the visit counts (context-driven, exogenous under (A1)).
  `lem:race` is deterministic and its tie handling is by a total strict order (§3.2).
- *Attack: make `Σ_C ν_d(C) η_{i,C}` not vanish with a singular `ν_d`.* **Fails** —
  `lem:cell-average-l1` holds for any Borel `ν_d` on the compact cube (§6).

### 8.2 Against `thm:grid-etc` in SC

- *Attack: break the pathwise monotonicity with ties, which are common under a shared context.*
  **Fails.** Re-derived from scratch in §3.3: the lexicographic commitment order is total and
  strict, so `W' ∈ {W, i}` on every sample point.
- *Attack: make the FATA hypothesis unsatisfiable while FATA has content.* **Succeeds as an
  unsatisfiability witness, fails as a falsity witness.** Take `d = 1`, `ν_1 = Leb`, `K = 2`,
  `M_1 ≡ ½`, `M_2(x) = ½ − dist(x, 𝒞)` with `𝒞` a fat Cantor set (closed, empty interior,
  `Leb(𝒞) > 0`); `M_2` is 1-Lipschitz, `M_2 ≤ M_1` with equality exactly on `𝒞`, so
  `G_12([0,1]) = 𝒞` and `∂G_12 = 𝒞` has positive mass: the stated remainder
  `n ν_1((∂G_12)^{√d h_n}) ≥ n Leb(𝒞)` is linear and the clause is vacuous. But I could **not**
  show FATA itself fails there: by the Lebesgue density theorem (equivalently
  `lem:cell-average-l1` on `1_𝒞`), `ν_1(𝒞|C) → 1_𝒞` in `L¹`, so on the cells carrying most of `𝒞`
  the two maps agree on a `(1−o(1))` fraction and `|m̄_{1,C} − m̄_{2,C}| ≤ 1 − θ_C = o(1)`; and on
  cells where `θ_C` is small the contribution `θ_C · E T_a(C)` is small. Making the two effects
  fail simultaneously needs a Cantor set whose relative complement density at scale `h_n` is
  `γ_n` with `q_n^{-1/2} ≪ γ_n → 0` on a positive-mass family of cells, simultaneously for all
  large `n` — a scale-tuned diagonal construction I did not complete. **Reported as open**, not as
  a witness.
- *Attack: the truncated-cell case.* **Fails.** A cell with `V_C < K q_n` never commits; agent
  counts there are functions of the permutations alone, identical across the coupled executions and
  exchangeable in `i,j`.

### 8.3 Against `thm:contextual-public` in SC

- *Attack: the deviator exploits knowing that when it shades, the rival is strong at the same `x`.*
  **Fails.** Agents are blind and play ex ante maps; the deviator cannot condition on the rival's
  realised rewards or on the platform's cell state. The bound
  `E[N_C] p'_{i,C} δ_C ≤ E[N_C](c_1 q_n^{-1/2} + η_{i,C})` uses only `lem:etc-tail` on two
  empirical means with `q_n` marginal-Bernoulli observations each — and those observations sit at
  *distinct* cell visits, so they are in fact independent even in SC (§1.2).
- *Attack: a deviation that performs well in exploration and shades after commitment.* **Succeeds
  — and it is already excluded.** The source's closing remark says exactly this: "The argument
  fails for phase-dependent strategies, which can perform well during exploration and lower the
  mean after commitment. This is why the theorem is restricted to maps fixed before play." SC does
  not change this; it is a limitation of `S_HDS`, inherited unchanged. Worth restating in the SC
  version because a shared context makes the phase visible to the *selected* agent through its own
  local count in the cell, which is the same exposure as in PM.
- *Attack: `ν_d` with atoms, or supported on a lower-dimensional subset of `[0,1]^d`.* **Fails.**
  No step uses a density or full support (§6).
- *Attack: exploit that only the exploration schedule, not the commitment, is symmetric under
  truncation.* **Fails.** Uniform permutation blocks are label-symmetric even when truncated, and
  the priority is a symmetric uniform permutation.

### 8.4 Against the diagonal embedding (part (a) of the hypothesis)

- *Attempt to show the diagonal embedding yields a FALSE statement.* **Fails.** I could not make
  any clause of any of the three theorems false on Diag. What Diag produces is (i) vacuous
  remainders for trace regions, (ii) an empty hypothesis set for `thm:grid-etc`'s FATA clause, and
  (iii) the wrong exponent unless one retunes. All three are proof/statement defects, not
  falsehoods. Reported honestly against the caller's stated expectation.

---

## 9. Verdict table

| # | claim | verdict in SC | note |
|---|---|---|---|
| 1 | `lem:cell-law`, conditional i.i.d. reduction | **verbatim** | source already disclaims cross-agent independence; only one agent is pulled per round |
| 2 | `lem:region` | **verbatim** | extends to bounded `g` for free (used in §2.3) |
| 3 | `lem:ucb-deficit`, `lem:race`, `eq:gap-free-ucb`, `lem:etc-tail`, `lem:cell-average-l1` | **verbatim** | all dimension-free; `lem:cell-average-l1` needs no density/support |
| 4 | `thm:grid-ucb-robust` — monotonicity, remainder 0 | **verbatim** | ties re-checked, §3.2 |
| 5 | `thm:grid-ucb-robust` — sharp adaptivity | **constants change** | `E_n` with `J_n = h_n^{-d}`; charge `n ν_d((∂R)^{√d h_n})` — removable by §2.3 |
| 6 | `thm:grid-ucb-robust` — robustness `E_n^K` | **constants change** | `8√(K J_n n log n) + 3K min{J_n,n}` with `J_n = h_n^{-d}` |
| 7 | `thm:grid-ucb-robust` — FATA | **constants change** | `n ν_d((∂G_ij(R))^{√d h_n})`; condition stays |
| 8 | `thm:grid-ucb-robust` — revenue & equilibrium under two-top | **constants change** | gain `≤ E_n`; two-top now non-degenerate (§4.3) |
| 9 | `thm:grid-etc` — sharp adaptivity, robustness | **constants change** | `O(n^{(d+2)/(d+3)} + n ν_d((∂R)^{√d h_n}))`; `2L√D → L√d` (see §11 item 4) |
| 10 | `thm:grid-etc` — monotonicity, pathwise | **verbatim** | lexicographic tie step re-derived, §3.3 |
| 11 | `thm:grid-etc` — FATA | **constants change; hypothesis stays** | unsatisfiable on Diag, satisfiable in SC; not removable (§2.4) |
| 12 | `thm:contextual-public` — equilibrium | **constants change** | `q_n J_n + c_1 n q_n^{-1/2} + n Σ_C ν_d(C) η_{i,C}`; Lipschitz form `(2^{d+1}+c_1+L√d) n^{(d+2)/(d+3)}` |
| 13 | `thm:contextual-public` — revenue | **constants change** | `(K2^{d+1}+(K−1)c_1+L√d) n^{(d+2)/(d+3)}` |
| 14 | `prop:two-top-sharp` | **verbatim** | constant `g_0 ν_d(A)/32` unchanged, §4.4 |
| 15 | naive diagonal embedding, sharp adaptivity on trace regions | **FAILS (vacuous), witness `R_0 = [0,1]^d`, `ν(∂R_Δ) = 1`** | true but empty; rescued by cylinders or by §2.3 |
| 16 | naive diagonal embedding, FATA | **FAILS (hypothesis unsatisfiable), witness `M_1(x)=M_2(x)=x`, `∂G_12 = Δ`, mass 1** | conclusion still holds in that example |
| 17 | naive diagonal embedding, exponent | **FAILS to improve without retuning** | lazy init helps exploration only, §7 |
| 18 | §2.3 removal of `ν(∂R)=0` from sharp adaptivity | **NEW, offered, believed correct** | applies in PM too; needs a second reader |
| 19 | §4.3 degeneracy of two-top under product `ν` | **NEW, proved for `K=2`** | `K ≥ 3` only sketched |

### 9.1 The statements I am willing to sign

**SC-1 (Static-grid UCB is contextual SAMF).** Assume (A1) for a single context `x_t ~ ν_d` i.i.d.
on `[0,1]^d`, `L`-Lipschitz `μ_i`, grid of side `h_n ≍ (log(en)/n)^{1/(d+2)}`, `J_n = h_n^{-d}`,
cell-local UCB at width `√(4 log n / T_a)` on the agent's local count in the cell and the global
horizon `n`. Put `E_n := L√d · n h_n + 4√(J_n n log n) + 3 min{J_n,n} = O(n^{(d+1)/(d+2)}(log n)^{1/(d+2)})`
and `E_n^K` the same with `8√(K J_n n log n) + 3K min{J_n,n}` in place of the last two terms. Then,
uniformly over `S_HDS` and its ex ante mixtures and for every `n ≥ 2`:
contextual sharp adaptivity for every measurable `R ⊆ [0,1]^d` with remainder
`E_n + n ν_d((∂R)^{√d h_n})` — and also with remainder `E_n + 2√2 n √(κ_n(R))` with **no** boundary
condition (§2.3);
`P(n) ≥ E Σ_t b(x_t) − E_n^K`;
contextual monotonicity exact with remainder zero, for every measurable `R`, every `n`, every
pointwise raise, no regularity and no boundary condition;
expected contextual FATA on `G_ij(R)` with remainder `n ν_d((∂G_ij(R))^{√d h_n})`.
If capacities are `L`-Lipschitz then `P(n; S^max) ≥ E Σ_t M_⋆(x_t) − E_n^K`, and if in addition
`|T(x)| ≥ 2` for `ν_d`-a.e. `x`, every unilateral deviation gains at most `E_n`.

**SC-2 (Static Grid-ETC contextual SAMF).** With `h_n` the largest dyadic `≤ n^{-1/(d+3)}`,
`J_n = O(h_n^{-d})`, `q_n = ⌈n^{2/(d+3)}⌉`, per-cell exploration through `q_n` independent uniform
permutations and commitment to the largest exploration empirical mean with an independent uniform
priority: uniformly over `S_HDS`, with constants depending only on fixed `K, d, L`, for every fixed
`R` with `ν_d(∂R) = 0` (or for every measurable `R`, with §2.3), contextual sharp adaptivity with
error `O(n^{(d+2)/(d+3)} + n ν_d((∂R)^{√d h_n})) = o(n)` and global robustness `O(n^{(d+2)/(d+3)})`;
contextual monotonicity exact and **pathwise** under the common-uniform coupling; and, if
`ν_d(∂G_ij(R)) = 0`, expected contextual FATA on `G_ij(R)`.

**SC-3 (Continuous public restricted equilibrium).** Suppose `|T(x)| ≥ 2` for `ν_d`-a.e. `x` and
`M_⋆` is public. Then for every `n`, every `i`, every deviation `m' ∈ S_HDS` (including arbitrary ex
ante mixtures):
`u_i(n; m', S^max_{−i}) − u_i(n; S^max) ≤ q_n J_n + c_1 n q_n^{-1/2} + n Σ_C ν_d(C) η_{i,C}`,
`c_1 = 2e^{-1/2}`, with the last sum `→ 0`; under `L`-Lipschitz `M_j`, `η_{i,C} ≤ L√d h_n` and the
gain is at most `(2^{d+1} + c_1 + L√d) n^{(d+2)/(d+3)}`. With no top-set condition,
`P(n; S^max) ≥ E Σ_t M_⋆(x_t) − [K q_n J_n + (K−1) c_1 n q_n^{-1/2} + n Σ_C ν_d(C) β_C]`, the bracket
`o(n)` and at most `(K 2^{d+1} + (K−1) c_1 + L√d) n^{(d+2)/(d+3)}` under Lipschitz capacities.

**SC-4 (`prop:two-top-sharp`).** Verbatim with `[0,1]^D → [0,1]^d`, `ν → ν_d`, `X → x`; constant
`g_0 ν_d(A)/32` unchanged.

---

## 10. Inherited versus new

Honest accounting. **Roughly 90% of what I sign is re-labelling.**

*Pure re-labelling (`D → d`, `X_t → x_t`, `x_{i,t} → x_t`, `M_j(x_j) → M_j(x)`, `ν → ν_d`,
`√D → √d`, `2^{D+1} → 2^{d+1}`):* `lem:region`, `lem:ucb-deficit`, `lem:race`, `eq:gap-free-ucb`,
`lem:etc-tail`, `lem:cell-average-l1`, all of the monotonicity arguments, all of the Lipschitz
comparisons, the whole of `thm:contextual-public` and `prop:two-top-sharp`, the balance arithmetic.

*Re-labelling plus a sentence:* `lem:cell-law` — one added sentence that the cross-agent
correlation is now perfect rather than merely permitted, and that this is immaterial because
exactly one agent is pulled per round.

*Checked rather than inherited (no change resulted, but the caller asked and I did not want to
inherit them):* the ETC lexicographic tie step (§3.3), the FATA exchangeability swap (which I
re-derived as a direct measure-preserving swap of `(U_{C,i,·}, priority_i) ↔ (U_{C,j,·},
priority_j)` restricted to one cell — cleaner than the tape route and valid because cells are
independent instances), the `√d h_n` inflation step (§2.1), the `b̄_C ≤ m̄⋆_C + L√d h_n` step (§11.4).

*Genuinely new, mine, not required by the question but material to it:*
- **N1** §4.3 — under a product `ν`, two-top forces constant capabilities (`K = 2`, proved). This
  is the content-level argument for the restriction and I think it belongs in the paper.
- **N2** §1.2 — the "one agent per round, so cross-agent dependence is never observed" framing,
  which is the single reason the whole chapter is dependence-agnostic.
- **N3** §2.3 — removal of `ν(∂R) = 0` from sharp adaptivity, in both models, with the explicit
  remainder `E_n + 2√2 n √(κ_n(R))`; and the argument in §2.4 for why the same device does **not**
  work for FATA.
- **N4** §7 — the accounting that lazy init is not an exponent improvement, and the identification
  of the dropped sentence in the live draft.
- **N5** §6 — "independent ex ante mixtures" is an unnecessary qualifier.

The caller's hypothesis (b) is therefore **confirmed, and it is confirmed cheaply**: the three
proofs were already written in a dimension-agnostic, dependence-agnostic way, and the restriction
is a re-labelling. I want to be blunt that this means **the restriction buys an exponent and a
non-degenerate hypothesis, not a new theorem.**

---

## 11. Cost of adopting this

**For my three results: a one-day edit. For the paper: more than a day, because of one knock-on
outside my scope.**

Line counts, from the live build (`aamas2027.tex` → `sec2_model`, `sec4_contextual`,
`app_contextual_public` → `appendix_contextual`, `app_noisy` → `appendix_samf`):

1. `sections/sec2_model.tex` — **~15 lines**. The contextual paragraph (`X_t := (x_{1,t},…,x_{K,t})`
   → `x_t`), "A continuum of profiles" (`X = [0,1]^D, D := Kd` → `[0,1]^d`), "Honest agents and top
   sets" (`b(X)`, `M_⋆(X)`, `T(X)`, `G_ij(R)`, `V_R(n)`, `T_i(R;n)` — all `X → x`), "Strategies"
   (the map's domain, and **delete** the sentence "If agents observe only their own contexts `x_i`,
   their maps must depend only on `x_i`", which is now empty). (A1)/(A2)/(A3) are unchanged.
2. `sections/sec4_contextual.tex` — **~45 lines**: the partition paragraph, the `E_n` display,
   `thm:grid-ucb-robust` (8 lines), the lazy remark (restore the dropped sentence, §7),
   the ETC paragraph, `thm:grid-etc` (6 lines), the `M̄_{j,C}/η/β` definitions,
   `thm:contextual-public` (12 lines), the sharpness paragraph, and the three SAMF definitions.
3. `sections/appendix_contextual.tex` — **~50 of its ~120 contextual lines touched**, all
   mechanically: §`app:cell-law`, §`app:contextual-ucb`, §`app:contextual-etc`,
   §`app:contextual-public`, `prop:two-top-sharp`. No new proof is required for any of the three
   theorems. If you also adopt §2.3, add ~10 lines (one extended `lem:region` + the `ε`-split).
4. **Two constants to reconcile while editing** (both pre-existing, neither caused by the
   restriction): the UCB proof writes `b̄_C ≤ m̄⋆_C + L√d h_n` while the ETC proof writes
   `b̄_C ≤ m̄⋆_C + 2L√D h_n` for the same comparison. The factor-1 version is the correct one,
   provided the comparator is the **cell-average-best** honest agent (`b(x) = max_h μ_h(x) ≤ max_h
   (μ̄_{h,C} + L√d h_n) = max_h μ̄_{h,C} + L√d h_n ≤ m̄⋆_C + L√d h_n`, using honesty `m̄_{h,C} ≥
   μ̄_{h,C}`). The appendix's phrasing "an honest agent attaining `b` at a point of `C`" points at
   the *pointwise* comparator, which only gives `2L`. Fix the phrasing, keep the constant 1, and
   change `2L√D` to `L√d` in the ETC proof.
5. Knock-on **in scope**: `thm:finite-context` and §`app:contextual-finite` are stated over finite
   sets of full *profiles* `X_F`. Under the restriction these become finite sets of common
   contexts; the proofs are again pure re-labelling, **~40 lines**.
6. Knock-on **out of scope but load-bearing, flagged because it dominates the cost**: the private
   continuum result `thm:ctx-private-continuum` carries `ρ_n := √D h_n log(en)` and the exponent
   `(D+2)/(D+3)`, and the paragraph **"Remark: the dependence on the number of agents is
   computational"** exists *only because* `D = Kd`. Under the restriction `D = d`, that remark, the
   EXP4 separation, the `e^{Θ(n^{d/(d+2)})}` expert set, and "so the barrier is computational and
   we can say exactly where it sits" all become moot or must be repurposed. `sec6_conclusion.tex`
   and the abstract likely echo it. That is a narrative rewrite, not a re-label, and it is the real
   price of the restriction. **Someone owning the private result must be asked before you commit.**

**Estimate: my three results, 1 day. The whole paper, 2–3 days, dominated by item 6.**

---

## 12. Open or doubtful

1. **§2.3 is new and unreviewed.** I believe the argument (it is four lines of case analysis on top
   of `lem:cell-average-l1`, which the paper already proves). But it *removes a hypothesis* from a
   published statement, so it should be read by a second prover before it goes in. The weakest link
   is the extension of `lem:region` from `1_R` to bounded `g`, which I checked and which is
   immediate from the same conditional-independence argument, but which the source does not state.
2. **FATA without `ν(∂G_ij(R)) = 0`: open.** I neither proved it nor produced a witness. §8.2 says
   exactly what a witness would have to look like (a scale-tuned fat Cantor set with relative
   complement density `γ_n` satisfying `q_n^{-1/2} ≪ γ_n → 0` on a positive-mass family of cells at
   scale `h_n`, simultaneously for all large `n`) and exactly what a proof would need (a rate on
   `κ_n(R)`, which `L¹` convergence does not supply). I lean towards the condition being necessary,
   but I will not sign either way.
3. **§4.3 for `K ≥ 3`: only sketched.** I proved the degeneracy rigorously for `K = 2`. For `K ≥ 3`
   under a product `ν` the condition requires the pushforward laws `M_i(x_i)` to share atoms and I
   believe it remains severely restrictive, but I did not prove a clean statement. If you want to
   use N1 as a justification for the restriction in the paper, get the `K ≥ 3` statement nailed or
   state it for `K = 2` and call it illustrative.
4. **`M_⋆` public.** `thm:contextual-public` says "let `M_⋆` be public, so that all-maximum play is
   available to every agent", but the proof only ever has agent `j` play its own `M_j`, which it
   knows. Either the publicity hypothesis is doing work I did not locate, or it is vestigial. Not
   an SC issue, but it should be resolved while the statement is being rewritten.
5. **The expectation version of `lem:race` under per-round tie coins** ("a first-violation argument
   then shows that raising `i` never costs it a pull") is a sketch in `appendix_samf.tex`. It is
   unchanged by the restriction, but ties become *more frequent* in SC when `M_i ≡ M_j`, so a
   reader will look at it harder. The pathwise version with a single priority drawn before play is
   airtight and is what I signed above; consider leading with it.
6. **Live/dead file divergence.** `sections/contextual.tex` and
   `sections/contextual_samf_algorithm.tex` (the `aamas_body.tex` build) hold an older copy of the
   same three theorems whose lazy-init remark is *more correct* than the live one (§7). Whatever is
   decided, these two files should be deleted or synchronised; right now the repository contains
   two mutually inconsistent statements of `thm:grid-ucb-robust`'s adaptivity claim.
7. **The arrival ladder does not relax.** The public contextual results need (A1) — `lem:cell-law`
   needs the within-cell contexts i.i.d. and `lem:region` needs the selection independent of the
   context at that visit. The router motivation for SC suggests query streams that are *not* i.i.d.
   The restriction therefore does not buy a weaker arrival assumption, and the SC write-up should
   not let the motivating story imply that it does.
8. **Phase-dependent deviations remain excluded** (the source's own closing remark). Under a shared
   context the selected agent still learns its phase from its own local count in the cell, exactly
   as in PM, so the exclusion is no more and no less comfortable than before — but it is more
   conspicuous once the model is "one query, several providers", and a referee will ask.
