# STATUS: DONE

# F1 final: CG-MESP, statement and proof after three adversarial passes

Written 29 September 2026 for round 3, result 3. Sources: `TASK.md`, `EXPLORER.md` (mechanism,
Section 3), `PROVER2.md` (proof, revisions 1 to 3), `ADVERSARY.md` (three passes, Sections 0 to 22).
This file is self-contained: every lemma the theorem uses is stated and proved here, and nothing is
imported from the other files except the definitions of the mechanism, which are restated. No
canonical file was modified. No em dash and no triple hyphen appears in this file.

I do not claim the result is correct. I claim that every step below was written out and checked,
and `CHECK.md` in this folder is an independent line-by-line pass over this file.

## 0. What is new relative to `PROVER2.md` revision 3

Nothing in the mechanism, and no rate. The changes are the seven P3 items of `ADVERSARY.md`
Section 22, the `J'_n` repair of `ADVERSARY.md` Section 20 item 3, the conditional form of every
probabilistic hypothesis, and three simplifications that remove steps rather than add them:

1. **Part (C) no longer needs any within-case martingale identity.** `PROVER2.md` Section 17.5 used
   `E[(Z_r - A_r) 1{case}] = 0` inside each case (`ADVERSARY.md` 15.3). Here revenue is written as
   `E sum_t m_{I_t,t}` once, globally, and the Stage-2 target sum is bounded below **pathwise**, so
   no conditional expectation is multiplied by a case indicator anywhere in part (C).
2. **Part (A) no longer needs the fallback length to be measurable at the fallback start.** Lemma 7
   and Lemma 8 are proved in conditional form with `E[H | G^fb]` in place of `H`, and the proof of
   part (A) only ever multiplies them by an event that is in `G^fb`; this removes load three
   (`ADVERSARY.md` G3) from part (A) as well as from part (C).
3. **The grid dimension is a parameter `m`.** The observed context lives in `[0,1)^m` and every
   primitive is `L`-Lipschitz on it. The profile model of `EXPLORER.md` is `m = D = Kd`; the
   one-context-per-round model of the current manuscript is `m = d`. The proof uses `m` in exactly
   two places, the cell count `J_n = g_n^m` and the oscillation bound `L sqrt(m) h_n`, which is the
   organising observation of `sc1-shared-context/PROVER_SC1.md`; nothing else in this file depends on
   which model is meant.

### 0.1 Where each P3 item and the `J'_n` repair were fixed

| item | the defect | fix | where in this file |
|:-|:-|:-|:-|
| `ADVERSARY.md` 17.2 | (A4f) enumerates the mechanism's draws, so a draw added later would escape it | the hypothesis quantifies over **every** randomisation the mechanism specifies, in the order specified; the list (f1) to (f3) is an instantiation for CG-MESP, stated as a consequence, not as the hypothesis | Section 3.2, (A4f) and Remark 3.2a |
| `ADVERSARY.md` 17.3 | "that field **containing** ..." is a lower bound on the field, so the hypothesis is ambiguous | every clause is pinned to a named field: `Pi` given `G^0_u`, `I_u` given `G^1_u`, `U_u` given `G^-_u`, with "being" and not "containing" | Section 3.1 (fields) and 3.2 |
| `ADVERSARY.md` 19 | the attribution table said part (A) uses all of (A4f); the adversary says (f1) is unused there | **corrected in both directions.** No step uses the *uniformity* of the priority law. But the coupling of part (A) (Lemma 9) does use that the priority is a *fresh* draw whose law does not depend on the strategy profile, which is what (f1) supplies; so (f1) stays in part (A)'s hypothesis with its use named. `CHECK.md` Section 8 records why the adversary's version is slightly too strong | Section 3.4 (attribution table), Lemma 9 |
| `ADVERSARY.md` 20 item 3 | the upgraded (B) and (C) replaced the random `J'_n` by `min{J_n, n}`, losing path adaptivity | all error terms are stated with `E[J'_n]`, by concavity and Jensen; this is never worse than `min{J_n, n}` | Section 4 (error terms), proofs of (A), (B), (C) (summation steps) |
| `ADVERSARY.md` 21.1 | "no conditional expectation is taken anywhere in this proof" is loose, since `P = E sum_t m` is a tower step | the sentence is replaced by the accurate one: no conditional expectation is ever multiplied by an indicator in parts (B) and (C) | Section 7 (end of proof of (B)), Section 8 (end of proof of (C)) |
| `ADVERSARY.md` 21.2 | `Pr(H^c) <= n^{-3}/K` and `Pr(E^c) <= n^{-4}` silently need `J_n <= n` | the remainders are stated with `J_n` explicit, valid at every `n`, and the simplified form is stated with its condition `n >= 2^{m(m+3)/3}` displayed | Lemma 1, Lemma 6(a), Theorem remainders `r_n` |
| `ADVERSARY.md` 21.3 | under (A4f) a comparison with Grid-ETC or Grid-UCB is not well posed | one sentence at the comparison | Section 10.2 |
| `J'_n` substitution (`ADVERSARY.md` 20 item 3, the three line repair) | as above | as above, with the three concavity inequalities written out | Section 4.1 |

Two further standing items from the brief:

* **`PROVER2.md` Section 18 (horizons).** The theorem is asymptotic in a strong sense. The table is
  recomputed in `check_horizons.py` and reproduced in Section 10.1, with the reading that goes with it.
* **Conditional form (A4f).** Every probabilistic hypothesis in this file is written as "each draw
  has its specified law conditionally on the field generated by everything realised before it", and
  none is written as a list of independences.

## 1. Model and notation

Agents `j in [K]`, `K >= 2`, horizon `n` known to the platform. At round `t` a context `X_t` in
`[0,1)^m` is revealed to the platform before it selects, and to the selected agent before it
chooses its target. Agent `j` has an
intrinsic mean `mu_j : [0,1)^m -> [0,1]` and a capacity `M_j : [0,1)^m -> [0,1]` with
`mu_j <= M_j`. The platform selects `I_t`; the selected agent chooses a target
`m_{I_t,t} in [0, M_{I_t}(X_t)]`; the reward is `Y_t = 1{U_t <= m_{I_t,t}}` for the round's seed
`U_t`. Costs are linear: a pull is worth `1 + mu_j(X_t) - m_{j,t} in [0,2]` to the selected agent
(the manuscript's convex costs are outside this file; see Section 10.4).

*The two instances of the model.* (i) Per-agent contexts: `X_t = (x_{1,t},...,x_{K,t})` with
`x_{j,t} in [0,1)^d`, `m = D = Kd`, and agent `j`'s primitives depend on `x_{j,t}` only; if they are
`L`-Lipschitz in `x_j` they are `L`-Lipschitz on `[0,1)^m`, since `|x_j - x'_j| <= |X - X'|`.
(ii) One shared context: `X_t in [0,1)^d` and `m = d`. Everything below is stated for a general
`m` and applies to both.

Benchmarks: `M_(2)(X)` is the second largest of `(M_1(X),...,M_K(X))` counted with multiplicity;
`b(X) := max_{h in K_H} mu_h(X)` for the honest set `K_H`; `P(n;S) := E_S sum_{t<=n} Y_t`;
`u_i(n;S) := E_S sum_{t<=n} 1{I_t = i}(1 + mu_i(X_t) - m_{i,t})`.

*Private randomisation.* Agent `j`'s private randomisation is a single random variable `theta_j`
(uniform on `[0,1]` without loss of generality) realised before play; write
`theta := (theta_1,...,theta_K)`.

*Deviation classes.* `B^ctx_{i,n}`: after being selected at round `t`, agent `i` chooses
`m_{i,t} in [0, M_i(X_t)]` as a measurable function of `n`, the contexts `X_1,...,X_t`, its own
history (its selection rounds, targets, rewards) across all cubes, every message it has received,
and `theta_i`. `B^ctx+_{i,n}`: the same, and in addition the entire arrival path
`A := (X_1,...,X_n)`. An honest agent satisfies `m_{h,t} >= mu_h(X_t)` after every history. Nothing
below uses any restriction on what an agent may condition on beyond these two definitions; every
bound is uniform over the class named in its statement.

`log` is natural, `(x)_+ := max{x, 0}`, `|.|` is the Euclidean norm.

## 2. The mechanism CG-MESP (unchanged from `EXPLORER.md` Section 3, with `D` written `m`)

The platform knows `n`, `K`, `m` and nothing else: not `L`, not any `mu_j` or `M_j`, not `K_H`,
not how contexts are generated.

**Parameters.**

```
g_n     := ceil( n^{1/(m+3)} ) ,   h_n := 1/g_n ,   J_n := g_n^m          (grid)
L_n     := ceil( n^{2/(m+3)} )                                            (bidding block)
ell_n   := log( 2 K n^5 )
s_n     := sqrt( ell_n / (2 L_n) )                                        (bid radius)
rho_n   := sqrt(m) h_n log(en)                                            (oscillation allowance)
sigma_n := 3 s_n + rho_n                                                  (price shading)
b_n(r)  := sqrt( r ell_n / 2 ) ,  b_n(0) := 0                             (monitor boundary)
R^dbl_K(V) := 11 sqrt( K (V+1) log K ) + 2 K log K log_2( 2(V+1) ) ,  R^dbl_K(0) := 0
```

**Grid.** The `J_n` half-open cubes of side `h_n` tiling `[0,1)^m`; `C(X)` is the cube containing
`X`. The position of `X` inside its cube is used only to locate the cube. Cubes are instantiated
lazily on first arrival.

**State per cube `C`.** Visit counter `V_C`; Stage-1 reward sums; price `tau_C`; winner `W_C`;
monitor count `r_C` and reward sum `Z_C`; local fallback clock and EXP3 weights; one priority
permutation `Pi_C` of `[K]`, drawn when `C` is first met.

**Round `t`.** Observe `X_t`, set `C := C(X_t)`, increment `V_C`, act by `C`'s phase.

* **Stage 1 (bidding), while `V_C <= K L_n`.** Pull agent `((V_C - 1) mod K) + 1`, so agent `j`'s
  `r`-th bidding pull at `C` is the `((r-1)K + j)`-th visit to `C`. When `V_C = K L_n`, form
  `beta_{j,C} := L_n^{-1} sum_{r <= L_n} Y_{j,C,r}`, let `W_C` be a largest bidder with ties broken
  by highest `Pi_C` priority, let `beta_(2),C` be the second order statistic **with multiplicity**,
  announce `tau_C := (beta_(2),C - sigma_n)_+`, and set `r_C := 0`, `Z_C := 0`. A cube with fewer
  than `K L_n` visits in the horizon never awards, prices or monitors.
* **Stage 2 (monitored primary), until a local switch.** Pull `W_C`; `r_C := r_C + 1`,
  `Z_C := Z_C + Y_t`; if `Z_C < r_C tau_C - b_n(r_C)`, declare a local switch at `C`.
* **Stage 3 (local fallback), after a switch at `C`.** Explicit-exploration EXP3 over all `K`
  agents on the visits to `C`, restarted in doubling epochs of the local fallback clock: epoch
  `k >= 0` covers local fallback times `2^k,...,2^{k+1}-1`, with fresh weights `w_j = 1`,
  `gamma_k := min{1/2, sqrt(K log K / 2^k)}`, `eta_k := gamma_k / K`, `q_j := w_j / sum_l w_l`,
  `p_j := (1 - gamma_k) q_j + gamma_k/K`, selection `I_t ~ p`, estimate
  `hat Y_j := Y_t 1{I_t = j}/p_j`, update `w_j := w_j exp(eta_k hat Y_j)`.
* **Messages.** A selected agent is told the current cube's phase and, in Stages 2 and 3, `tau_C`.

**Proposed profile `S^*`.** At a bidding pull and at a fallback pull, agent `j` delivers
`M_j(X_t)`. At a Stage-2 pull at `C` the winner delivers `min{tau_C, M_{W_C}(X_t)}` if strategic and
`max{mu_{W_C}(X_t), min{tau_C, M_{W_C}(X_t)}}` if honest. `S^*_j in B^ctx_{j,n}` for every `j`, and
its honest components are honest.

**The mechanism's randomisations**, listed because (A4f) quantifies over them: the priority
permutation `Pi_C`, drawn at the first visit to `C`, and the Stage-3 selection `I_t`. The grid, the
lazy instantiation, the round robin, the award rule, the price, the monitor test, the epoch
schedule, the weight update and the messages are deterministic functions of the state. The Stage-1
and Stage-2 selections are deterministic functions of the cube's state.

## 3. Hypotheses

### 3.1 Deterministic hypotheses, and the fields

**(H1) Primitives.** `K >= 2`; `mu_j, M_j : [0,1)^m -> [0,1]` with `mu_j <= M_j`, all
`L`-Lipschitz in the Euclidean norm for a constant `L >= 0` unknown to the platform; a fixed
nonempty honest set `K_H`.

**(H2) Horizon.** `n` is known to the platform, `n >= 2K`, and `log(en) >= 3L`, that is
`n >= exp(3L)`. All guarantees are fixed horizon.

**The natural fields.** `G_0 := sigma(theta)`. At round `u`, in the order in which things happen:

```
G^0_u := sigma( G_{u-1}, X_u )                                        post arrival
G^1_u := sigma( G^0_u, Pi_{C(X_u)} )  if C(X_u) is first met at u,
         G^1_u := G^0_u               otherwise                       post priority draw
G^2_u := sigma( G^1_u, I_u )                                          post selection
G^-_u := sigma( G^2_u, m_{I_u,u} )                                    pre seed
G_u   := sigma( G^-_u, U_u ) .
```

Since `theta` is in `G_0`, a target chosen by a strategy in `B^ctx` is `G^2_u`-measurable, so
`G^-_u = G^2_u` for such strategies; the separate name is kept because it is the field the seed
clause is stated on. **The path-augmented fields** are `hat G^k_u := sigma(G^k_u, A)` for each of
the fields above, with `hat G_0 := sigma(theta, A)`.

### 3.2 The probabilistic hypotheses, in conditional form

> **(A4f) Fresh draws.** At every round `u`, each randomisation that the mechanism specifies at
> round `u`, taken in the order the mechanism specifies, and after them the reward seed `U_u`, has
> its specified law conditionally on the field generated by everything realised before it, that
> field **being** `G_{u-1}` together with `X_u`, the randomisations already made at round `u`, and,
> for the seed, the selected agent's target. The specified law of a randomisation may depend on the
> past (as the Stage-3 law `p_u` does). The selected agent's target is unconstrained beyond
> feasibility and the class of its strategy, and the seed clause is stated conditionally on it:
> `Y_u = 1{U_u <= m_{I_u,u}}` with `U_u` uniform on `[0,1]` conditionally on `G^-_u`.

For CG-MESP the randomisations are the two listed at the end of Section 2, so (A4f) reads, with
the fields pinned:

* **(f1)** on the event that `C(X_u)` is first met at round `u` (an event in `G^0_u`), the
  conditional law of `Pi_{C(X_u)}` given `G^0_u` is uniform on the permutations of `[K]`;
* **(f2)** in Stage 3 at `C(X_u)`, the conditional law of `I_u` given `G^1_u` is `p_u`, the law
  computed from `C(X_u)`'s EXP3 state (in Stages 1 and 2, `I_u` is the specified deterministic
  function of the cube's state and there is nothing to assume);
* **(f3)** conditionally on `G^-_u`, `U_u` is uniform on `[0,1]`; hence the conditional law of
  `Y_u` given `G^-_u` is Bernoulli(`m_{I_u,u}`).

> **(A4f-P) Fresh draws given the path.** (A4f) with every field replaced by its path-augmented
> version `hat G`: each randomisation and the seed has its specified law conditionally on
> everything realised before it **together with the entire arrival path** `A`.

> **(X) Exogeneity.** The joint law of `(A, theta)` is the same under every strategy profile.

**Remark 3.2a (the quantifier, `ADVERSARY.md` 17.2).** (A4f) quantifies over *every* randomisation
the mechanism specifies, whatever it is. (f1) to (f3) are its instantiation for CG-MESP as specified
in Section 2, which I checked is complete: the only randomisations are `Pi_C` and the Stage-3
selection. A randomisation added to the mechanism later (a random grid offset, a randomised tie
break in the monitor, a random restart) is covered by (A4f) without rewriting it; only the
instantiation list would change.

**Remark 3.2b (the fields, `ADVERSARY.md` 17.3).** Each clause is stated on one named field, the
minimal one. A larger field would make the hypothesis stronger, and nothing below needs more.
(A4f-P) is the one place a larger field is assumed, and it is a separate named hypothesis.

**Remark 3.2c (relations).** (A4f-P) implies (A4f): each specified law is a function of the natural
field, so the tower property carries the conditional law from `hat G^k_u` down to `G^k_u`. (A4f)
places no condition on how contexts are generated: `X_u` may be any measurable function of the
entire past, including past rewards, past mechanism draws and `theta`, together with fresh
randomness, provided only that it is realised before round `u`'s own draws. (A4f-P) holds whenever
`A` is deterministic, or more generally whenever the whole array of seeds and mechanism coins is
independent of the pair `(A, theta)` **jointly** (pairwise independence of `A` and `theta` from the
array would not do, by the witness of Remark 3.2d(i)). (X) says that no agent can move the arrival path.

**Remark 3.2d (what the conditional form excludes, with the three witnesses of this project).**
(i) `ADVERSARY.md` G1: `U_t = frac(x_t + c_t)` with `c_t` the deviator's coin is pairwise
independent of everything, but is `G^-_t`-measurable (the coin is part of `theta_i`), so (f3) fails.
(ii) `ADVERSARY.md` H1: `X_u` a function of the round's fallback selection coin makes `I_u`
`G^1_u`-measurable, so (f2) fails. (iii) The manuscript's own (A2) note: `X_{u+1}` a fixed function
of `U_u` is permitted by (A4f), which constrains the seed given its past only, but violates (A4f-P),
since given `A` the seed is pinned. This is why part (A), whose class `B^ctx+` lets a target read
`X_{u+1}`, is stated under (A4f-P) and not under (A4f).

**Remark 3.2e (`B^ctx+` needs (A4f-P) and (X); `ADVERSARY.md` G4).** If arrivals react to rewards,
a strategy in `B^ctx+` that reads the whole path is not well defined in general: `X_{u+1}` depends
on `Y_u`, which depends on `m_{i,u}`, which may depend on `X_{u+1}`. So parts (B) and (C) under
(A4f) are stated for `B^ctx`, and `B^ctx+` is used only under (A4f-P).

### 3.3 Well-posedness of the probability model

Under (A4f), for a given strategy profile, the joint law of the execution is determined by the law
of the arrival mechanism, the specified conditional laws of the mechanism's draws and of the seeds,
and the strategies (Ionescu-Tulcea, round by round in the order of Section 3.1). Every expectation
below is under that law. Lemma 9 constructs the two executions compared in part (A) on one space.

### 3.4 Which hypothesis each result uses

| result | uses | does not use |
|:-|:-|:-|
| Fact 0, Fact 1, Fact 2, Lemmas 2, 3, 4, 5(i), 5(ii) | nothing probabilistic (pathwise) | any clause |
| Lemma 1, Lemma 5(iii), Lemma 6 | (f3) | (f1), (f2), any condition on arrivals |
| Lemma 7, Lemma 8 | (f2) Stage-3 branch and (f3) | (f1), any condition on arrivals |
| Lemma 9 (canonical coupling) | (X), and (f1), (f2), (f3) in the form (A4f-P) | the *uniformity* of `Pi_C` |
| Part (B) | (f3) | (f1), (f2): holds even if the Stage-3 selection is adversarial |
| Part (C) over `B^ctx` | (f2), (f3) | (f1) |
| Part (C) over `B^ctx+` | (f2), (f3) in the form (A4f-P) | (f1) |
| Part (A) over `B^ctx+` | (X) and (A4f-P), all three clauses, through Lemma 9 | the uniformity of `Pi_C` |

The last row is the correction of `ADVERSARY.md` Section 19 (P3). No step uses that `Pi_C` is
uniform: every lemma about a winner holds for whoever wins, and a tie break of any law leaves every
bound intact. But part (A) compares two executions, and it can put them on one space with the
*same* `Pi_C` only because in each execution `Pi_C` is a fresh draw, independent of the past given
the path, with a law that does not depend on the strategy profile. That is what (f1) supplies. A
priority whose conditional law reacted to the deviator's earlier rewards would make the two
executions' tie breaks differ and would break the winner inclusion (9.1) below; `CHECK.md`
Section 8 gives an instance (`K = 2`, constant primitives, a priority that favours agent `1` iff its
first Stage-1 reward was `0`) on which part (A) then fails by `Theta(n)`. So (f1) is used in part
(A), through Lemma 9, and only its uniformity is idle.

## 4. Error terms

`J'_n` is the number of cubes the realised path visits at least once (a random variable; under (X)
its law is the same in every execution). `E[J'_n] <= min{J_n, n}`. Define

```
e_bid    := min{ E[J'_n] L_n , n }                                    (deviator's Stage-1 harvest)
e_stage1 := min{ K E[J'_n] L_n , n }                                  (all Stage-1 rounds)
e_osc    := n rho_n                                                   (within-cube oscillation)
e_mon    := E[J'_n] + 2 sqrt( E[J'_n] n ell_n / 2 )                   (monitoring slack)
e_fb     := 11 sqrt( 2 K E[J'_n] n log K ) + 2 K log K E[J'_n] log_2( 2(n+1) )
e_price  := n ( 4 s_n + (4/3) rho_n )
r_n      := J_n n^{-4} + J_n n^{-3} / K                               (failure remainder)
```

If `n >= n_J(m) := 2^{m(m+3)/3}` then `J_n <= n` and `r_n <= n^{-3} + n^{-2}/K`
(`log10 n_J` is `0.40, 1.00, 1.81, 2.81, 5.42, 13.04` at `m = 1, 2, 3, 4, 6, 10`; every one of these
is below the horizon at which the corresponding bound is non-trivial, Section 10.1). Proof:
`g_n <= 2 n^{1/(m+3)}` since `ceil(x) <= 2x` for `x >= 1`, so `J_n <= 2^m n^{m/(m+3)}`, which is
at most `n` iff `2^m <= n^{3/(m+3)}`.

### 4.1 The `J'_n` repair (`ADVERSARY.md` Section 20 item 3)

Every proof below first proves a **pathwise** bound of the form `f(J'_n)` and then takes
expectations. The three functions that occur are

```
f_1(x) := min{ x L_n , n } ,   f_1^K(x) := min{ K x L_n , n } ,
f_2(x) := x + 2 sqrt( x n ell_n / 2 ) ,
f_3(x) := 11 sqrt( 2 K x n log K ) + 2 K log K x log_2( 2(n+1) ) ,
```

each concave on `[0, infinity)` (a minimum of affine functions, or an affine function plus a
nonnegative multiple of `sqrt x`). By Jensen, `E f(J'_n) <= f(E J'_n)`, which gives `e_bid`,
`e_stage1`, `e_mon` and `e_fb` as displayed. Since each `f` is nondecreasing and
`E[J'_n] <= min{J_n, n}`, the displayed terms are never larger than the worst-case forms of
`PROVER2.md` Section 17.5, and on a path concentrated in few cubes they are much smaller.

## 5. The theorem

**Theorem (CG-MESP).** Assume (H1) and (H2) and run CG-MESP.

**(A) Additive behavioural equilibrium.** Assume in addition (X) and (A4f-P). For every agent `i`,
strategic or honest, and every `S'_{i,n} in B^ctx+_{i,n}` (honest if `i in K_H`),

    u_i(n; S'_{i,n}, S^*_{-i,n})  -  u_i(n; S^*_n)  <=  e_bid + e_osc + e_mon + e_fb + 6 r_n .

**(B) Second-capacity revenue.** Assume in addition clause (f3) of (A4f) only. If every agent plays
`S^*`,

    P(n; S^*_n)  >=  E[ sum_{t<=n} M_(2)(X_t) ]  -  ( e_stage1 + e_price + r_n ) .

**(C) Honest-benchmark robustness.** Assume in addition clauses (f2) and (f3) of (A4f). For every
profile `S` in which each agent `j` plays some strategy in `B^ctx_{j,n}` and every honest agent is
pointwise honest (all `K` agents may deviate, jointly and with arbitrary correlation through the
history),

    P(n; S)  >=  E[ sum_{t<=n} b(X_t) ]  -  ( e_stage1 + e_price + e_mon + e_fb + r_n ) .

The same holds for profiles in `B^ctx+` under (A4f-P).

**(D) Rates.** For fixed `K` and `m` every error term is `O( n^{(m+2)/(m+3)} log(eKn) )`, with
constants depending on `K` and `m` only and on no property of the instance or of the arrival path.

In (B) and (C) the benchmark is evaluated along the realised arrival path, which under (A4f) the
mechanism's own outputs may help determine (Remark 10.3). In (A) the error terms do not contain
`L`, `mu`, `M`, a capacity gap or any mass; `L` enters only through (H2).

## 6. Lemmas

### 6.0 Admissible filtrations

A filtration `(F_u)_{0 <= u <= n}` with subfields `F_{u-1} subseteq F^0_u subseteq F^1_u
subseteq F^2_u subseteq F^-_u subseteq F_u` is **admissible for an execution** if
`G^k_u subseteq F^k_u` for every `k` and `u` (so the execution is adapted, round by round, in the
order of Section 3.1), and the clauses of (A4f) that the lemma at hand uses hold with every `G`
replaced by `F` (call it (f3)-admissible, (f2,f3)-admissible, and so on). Under (A4f), or under its
clause (f3) alone for the (f3) lemmas, the natural filtration `G` is admissible in this sense. Under
(A4f-P) the path-augmented filtration `hat G` is admissible. Lemma 9 gives one filtration
admissible for two executions at once. Lemmas 1, 5(iii) and 6 need (f3)-admissibility only, and
Lemmas 7 and 8 need (f2,f3)-admissibility; they use nothing else about the filtration.

For a cube `C`: `Comp_C` is the event that `C` completes bidding (`V_C >= K L_n`); `a_C` is its
award round (the `K L_n`-th visit), `+infinity` off `Comp_C`; `n_C := (V_C - K L_n)_+`;
`t_{j,C,r}` is the round of agent `j`'s `r`-th Stage-1 pull at `C`;
`M_j^inf(C) := inf_{X in C} M_j(X)`, `M_j^sup(C) := sup_{X in C} M_j(X)`, and likewise for `mu_j`.
On `Comp_C` put

```
beta_{j,C} := L_n^{-1} sum_{r <= L_n} Y_{j,C,r}           (the bid)
Abar_{j,C} := L_n^{-1} sum_{r <= L_n} m_{j,C,r}           (average realised target)
Mbar_{j,C} := L_n^{-1} sum_{r <= L_n} M_j( X_{t_{j,C,r}} ) (average capacity at those rounds)
```

Feasibility gives, pathwise and for every behaviour,

    Abar_{j,C}  <=  Mbar_{j,C} .                                                        (6.1)

`T_C` is the round at which `C` switches (`+infinity` if it never does); `G^fb_C := F_{T_C}` is the
stopped field `{ B : B cap {T_C <= u} in F_u for every u }`, the information at `C`'s fallback
start. `H_C` (or `H`) is the number of fallback visits to `C`.

### 6.1 Three pathwise facts

**Fact 0 (oscillation).** Put `omega := L sqrt(m) h_n`. For `X, X'` in one cube,
`|X - X'| <= sqrt(m) h_n`, so every `mu_j` and every `M_j` oscillates by at most `omega` on a cube,
and so do `M_(2)` and `b`, being order statistics or maxima of `L`-Lipschitz functions evaluated at
the same point (order statistics are 1-Lipschitz in the supremum norm). By (H2),
`omega <= (1/3) sqrt(m) h_n log(en) = rho_n/3`. Since `Mbar_{j,C}` averages values of `M_j` on `C`,

    M_j(X) - omega  <=  M_j^inf(C)  <=  Mbar_{j,C}  <=  M_j^sup(C)  <=  M_j(X) + omega   for every X in C.   (6.2)

*Proof.* Coordinates of two points of a half-open cube of side `h_n` differ by less than `h_n`, so
the Euclidean distance is below `sqrt(m) h_n`; the rest is the Lipschitz property and (H2). `QED`

**Fact 1 (the Stage-1 schedule is a function of the path).** In every execution, whatever any agent
does: `V_C`, `n_C`, `Comp_C`, `a_C`, the set of Stage-1 rounds of `C`, the agent pulled at each,
the rounds `t_{j,C,r}`, and `J'_n` are functions of `A` alone; and whether round `s` is a Stage-1
round at `C`, and of which agent, is a function of `X_1,...,X_s`.

*Proof.* `V_C` counts arrivals in `C`; Stage 1 at `C` is exactly its first `K L_n` visits and the
agent at the `v`-th visit is `((v-1) mod K) + 1`. Neither reads a reward, a bid, a draw or a
message. `QED`

**Fact 2 (cube locality and predictability).** The bids, winner, price, monitor statistics, switch
round and fallback state at `C` are functions of `A`, `Pi_C`, the rewards and targets at visits to
`C`, and the Stage-3 selections at `C`. Consequently: whether round `s` is a Stage-2 pull at `C`,
whether it is a fallback visit to `C`, the local fallback clock, the epoch index `k(s)`, and the
weights `q_s` and `p_s` at `C` are all `G^0_s`-measurable, being functions of `X_1,...,X_s` and of
data at rounds strictly before `s`; `T_C` is a stopping time of `(G_u)`; the events `Comp_C`,
`{W_C = j}` and the value `tau_C` are functions of `A`, `Pi_C` and the Stage-1 data of `C`, hence
`G_{a_C}`-measurable on `{a_C < infinity}`.

*Proof.* Every per-cube state variable is updated only at visits to that cube, from data produced
there; parameters and the grid are fixed before play; induction on the round. The switch at `C` at
round `u` is decided from `Z_C` and `r_C` after `Y_u`, hence `{T_C = u} in G_u`. `QED`

### 6.2 Bidding

**Lemma 1 (predictable bid concentration, uniform over all behaviour).** Uses (f3) only. For every
cube `C`, every agent `j` and every behaviour of all `K` agents,

    Pr( Comp_C cap { |beta_{j,C} - Abar_{j,C}| > s_n } )  <=  2 e^{-ell_n}  =  n^{-5}/K .

Hence with `E_C := Comp_C^c cup { |beta_{j,C} - Abar_{j,C}| <= s_n for all j }` and
`E := intersection of E_C over the J_n grid cubes`, `Pr(E_C^c) <= n^{-5}` and
`Pr(E^c) <= J_n n^{-5}`. The one-sided event `{beta_{j,C} < Abar_{j,C} - s_n}` has probability at
most `e^{-ell_n} = n^{-5}/(2K)` on `Comp_C`. `E_C` is `G_{a_C}`-measurable on `Comp_C`.

*Proof.* Put `phi_s := 1{round s is a Stage-1 pull of agent j at C}`, which is
`G^0_s`-measurable by Fact 1, hence `F^-_s`-measurable. Put
`M_t := sum_{s <= t} phi_s (Y_s - m_{I_s,s})`, `c_t := sum_{s <= t} phi_s` and, for real `lambda`,
`N_t := exp(lambda M_t - lambda^2 c_t / 8)`, `N_0 := 1`. `N_{t-1}`, `phi_t` and `m_{I_t,t}` are
`F^-_t`-measurable and, by (f3), `Y_t` given `F^-_t` is Bernoulli(`m_{I_t,t}`), so
`Y_t - m_{I_t,t}` has conditional mean `0` and lies in an interval of length `1`; Hoeffding's lemma
gives `E[exp(lambda phi_t (Y_t - m_{I_t,t})) | F^-_t] <= exp(lambda^2 phi_t / 8)` (trivial if
`phi_t = 0`). So `E[N_t | F^-_t] <= N_{t-1}` and, by the tower property, `E[N_n] <= 1`. Always
`c_n <= L_n`, so `E[exp(lambda M_n)] <= exp(lambda^2 L_n / 8)`. On `Comp_C`, `c_n = L_n` and
`M_n = L_n (beta_{j,C} - Abar_{j,C})`. Markov with `lambda = 4 s_n` gives
`Pr(Comp_C cap {beta - Abar > s_n}) <= Pr(M_n > L_n s_n) <= exp(2 L_n s_n^2 - 4 L_n s_n^2)
= exp(-2 L_n s_n^2) = e^{-ell_n}`, since `s_n^2 = ell_n/(2 L_n)`. The lower tail is the same with
`-lambda`. `2 e^{-ell_n} = n^{-5}/K`; a union over `j in [K]` gives `n^{-5}`, and a union over the
deterministic set of `J_n` grid cubes gives `J_n n^{-5}`. Measurability: `beta_{j,C}` and
`Abar_{j,C}` are functions of rewards and targets at the Stage-1 rounds of `C`, all at or before
`a_C`. `QED`

### 6.3 The three price lemmas and the honest floor

Fix a cube `C` and work on `Comp_C`; `W := W_C` is a largest bidder,
`tau_C = (beta_(2),C - sigma_n)_+`, `sigma_n = 3 s_n + rho_n`.

**Lemma 2 (the realised winner meets the price at every context of its cube).** On `E_C cap Comp_C`,
for every `X in C`, `tau_C <= (M_W(X) - 2 s_n - (2/3) rho_n)_+ <= M_W(X)`, whoever `W` is and
whatever any agent did.

*Proof.* `beta_(2),C <= beta_{W,C}` (a largest bidder); on `E_C`, `beta_{W,C} <= Abar_{W,C} + s_n`;
by (6.1) `Abar_{W,C} <= Mbar_{W,C}`; by (6.2) `Mbar_{W,C} <= M_W(X) + rho_n/3`. So
`beta_(2),C - sigma_n <= M_W(X) - 2 s_n - (2/3) rho_n`, and `x -> x_+` is nondecreasing. `QED`

*Consequence 2a.* On `E_C cap Comp_C`, the `S^*` target of the winner at every Stage-2 pull at `C`
is exactly `tau_C` if the winner is strategic and at least `tau_C` if honest.

**Lemma 3 (a non-deviating comparator dominates the price).** Fix `i` and suppose every `j != i`
delivers `M_j(X_t)` at its Stage-1 pulls at `C`. On `E_C cap Comp_C`, with
`nu_i(C) := max_{j != i} M_j^inf(C)`, `tau_C <= nu_i(C)`.

*Proof.* Let `j*` attain `max_{j != i} beta_{j,C}`. If `i` is a largest bidder,
`beta_(2),C = beta_{j*,C}`; otherwise `W != i` and `beta_(2),C <= beta_{W,C} <= beta_{j*,C}`.
Since `j*` delivers capacity, `Abar_{j*,C} = Mbar_{j*,C}`, so on `E_C`,
`beta_{j*,C} <= Mbar_{j*,C} + s_n <= M_{j*}^sup(C) + s_n <= M_{j*}^inf(C) + omega + s_n`, by (6.2)
and Fact 0. Hence
`beta_(2),C - sigma_n <= M_{j*}^inf(C) - 2 s_n - (2/3) rho_n <= nu_i(C)`, and `nu_i(C) >= 0`. `QED`

**Lemma 4 (the price is close to the second capacity at `S^*`).** If every agent delivers capacity
at its Stage-1 pulls at `C`, then on `E_C cap Comp_C`, for every `X in C`,
`tau_C >= M_(2)(X) - 4 s_n - (4/3) rho_n`.

*Proof.* `Abar_{j,C} = Mbar_{j,C}` for every `j`, so on `E_C`
`beta_{j,C} >= Mbar_{j,C} - s_n >= M_j(X) - rho_n/3 - s_n` by (6.2). The second order statistic is
nondecreasing in each argument, so `beta_(2),C >= M_(2)(X) - rho_n/3 - s_n`, and
`tau_C >= beta_(2),C - sigma_n`. `QED`

**Lemma 5 (honest floor).** Put `v_C := max_{h in K_H} mu_h^inf(C)` and let `h_C in K_H` attain it
(smallest label on ties); both depend on the instance and the grid only. (i) `b(X) <= v_C + omega`
for every `X in C`. (ii) Under any behaviour respecting pointwise honesty, `m_{h_C,t} >= v_C` at
every round with `X_t in C` at which `h_C` is selected. (iii) Uses (f3). With
`E^H_C := Comp_C^c cup {beta_{h_C,C} >= Abar_{h_C,C} - s_n}`, `Pr((E^H_C)^c) <= n^{-5}/(2K)`, and
on `E^H_C cap Comp_C`, `beta_{h_C,C} >= v_C - s_n`.

*Proof.* (i) Let `h` attain `b(X) = mu_h(X)`; by Fact 0 `mu_h(X) <= mu_h^inf(C) + omega <=
v_C + omega`. (ii) `m_{h_C,t} >= mu_{h_C}(X_t) >= mu_{h_C}^inf(C) = v_C`. (iii) The probability is
the one-sided form of Lemma 1; by (ii) at the Stage-1 pulls, `Abar_{h_C,C} >= v_C`. `QED`

### 6.4 Monitor

Fix a cube `C`. Let `Y^C_r`, `m^C_r` be the reward and target at the `r`-th Stage-2 pull at `C`,
`Z_r := sum_{q <= r} Y^C_q`, `A_r := sum_{q <= r} m^C_q`, both extended by zero increments beyond the
number of Stage-2 pulls actually taken, `Z_0 = A_0 = 0`. Put
`H_C := { |Z_r - A_r| <= b_n(r) for every r <= n }` and `H := intersection of H_C over the J_n grid
cubes`.

**Lemma 6 (anytime cube monitor).** Uses (f3) only, and no property of the arrival path. For any
behaviour of every agent:

(a) `Pr(|Z_r - A_r| > b_n(r)) <= 2 e^{-ell_n}` for each `r <= n`; so `Pr(H_C^c) <= n^{-4}/K` and
    `Pr(H^c) <= J_n n^{-4}/K`;
(b) on `H_C`, if the Stage-2 phase at `C` lasted `q` pulls (counting the failing pull if there is
    one, and `q = n_C` if there is no switch), then `A_q >= q tau_C - 1 - 2 b_n(q)`;
(c) on `H_C`, the Stage-2 winner's realised utility over that phase is at most
    `q (1 + mu_W^sup(C) - tau_C) + 1 + 2 b_n(q)`;
(d) on `H_C`, if every Stage-2 target at `C` is at least `tau_C`, no switch occurs at `C`;
(e) on `{T_C <= u}`, the event `H_C` is determined by the data at `C` up to round `T_C`; that is,
    `H_C cap {T_C < infinity}` is `G^fb_C`-measurable.

*Proof.* (a) Fix `r`. Let `psi_s := 1{round s is a Stage-2 pull at C}`, `T_r` the round of the
`r`-th such pull (`n` if fewer), `phi_s := psi_s 1{s <= T_r}`. By Fact 2 `psi_s` is
`G^0_s`-measurable, and `{s <= T_r}` says fewer than `r` Stage-2 pulls at `C` occurred before `s`,
a function of the past; so `phi_s` is `F^0_s`-measurable. With `M_t`, `c_t`, `N_t` built from this
`phi` exactly as in Lemma 1, `E[N_n] <= 1`. Under the zero extension `M_n = Z_r - A_r` and
`c_n <= r`, so `E[exp(lambda (Z_r - A_r))] <= exp(lambda^2 r / 8)`, and Markov with
`lambda = 4 b_n(r)/r` gives `exp(-2 b_n(r)^2 / r) = e^{-ell_n}` for each tail. Union over
`r <= n`: `2 n e^{-ell_n} = n^{-4}/K`; union over the `J_n` grid cubes: `J_n n^{-4}/K`.
No `phi_s` is claimed to be `F_{s-1}`-measurable, and none needs to be (`ADVERSARY.md` G2).
(b) If no switch occurred through `q`, the test did not fire at `q`: `Z_q >= q tau_C - b_n(q)`, and
on `H_C` `A_q >= Z_q - b_n(q) >= q tau_C - 2 b_n(q)`. If the switch occurred at `q >= 1`, apply this
at `q - 1` and use `A_q >= A_{q-1}`, `tau_C <= 1`, `b_n(q-1) <= b_n(q)`.
(c) The winner's utility is `sum_{r <= q}(1 + mu_W(X) - m^C_r) <= q(1 + mu_W^sup(C)) - A_q`; use (b).
(d) `A_r >= r tau_C` for every `r`, so on `H_C`, `Z_r >= A_r - b_n(r) >= r tau_C - b_n(r)`: the
test never fires.
(e) After the switch no Stage-2 pull occurs at `C`, so for every `r` the pair `(Z_r, A_r)` is a
function of the Stage-2 data at rounds up to `T_C`. `QED`

### 6.5 Fallback

**Lemma 7 (cube fallback with a local horizon not known in advance).** Uses (f2) and (f3). Fix a
cube `C`, a deterministic `v in [0,1]` and an agent `j*`, and suppose that at every round `u` that
is a fallback visit to `C`,

    E[ Y_u 1{I_u = j*} | F^0_u ]  >=  v p_{j*,u} .                                     (6.3)

(Sufficient: whenever `j*` is selected at a fallback visit to `C`, its target is at least `v`; then
(6.3) follows from (f3) and (f2) by the tower property, since `1{I_u = j*}` is `F^-_u`-measurable.)
Then, almost surely,

    E[ sum over fallback pulls at C of Y_u | G^fb_C ]  >=  v E[H | G^fb_C]  -  E[ R^dbl_K(H) | G^fb_C ] ,

and in particular `E[sum over fallback pulls at C of Y_u] >= v E[H] - E[R^dbl_K(H)]`. `H` is **not**
assumed `G^fb_C`-measurable.

*Proof.* Let `phi_u := 1{round u is a fallback visit to C}` and `k(u)` the epoch index there; both
are `F^0_u`-measurable (Fact 2), as are `q_u`, `p_u`. **The one use of the mechanism's
randomisation:** by (f2) the law of `I_u` given `F^1_u` is `p_u`, `p_u` is
`F^0_u`-measurable and `F^0_u subseteq F^1_u`, so
`E[1{I_u = j} | F^0_u] = E[ E[1{I_u = j} | F^1_u] | F^0_u ] = p_{j,u}` (`ADVERSARY.md` 18). Put
`r_{j,u} := E[Y_u 1{I_u = j} | F^0_u] / p_{j,u}` (`p_{j,u} >= gamma_k/K > 0`), so
`r_{j,u} in [0,1]`, `r_{j*,u} >= v` by (6.3), and, since `Y_u^2 = Y_u`,

    E[ hat Y_{j,u} | F^0_u ] = r_{j,u} ,    E[ sum_l q_{l,u} hat Y_{l,u}^2 | F^0_u ] = sum_l q_{l,u} r_{l,u}/p_{l,u} <= K/(1 - gamma_{k(u)}) ,

the last because `p_l >= (1 - gamma) q_l`. Pathwise, `sum_l q_{l,u} hat Y_{l,u} = Y_u q_{I_u}/p_{I_u}
<= Y_u/(1 - gamma_{k(u)})`.

*Pathwise potential inequality.* In epoch `k`, `eta_k hat Y_j <= eta_k / p_j <= 1`. With
`W := sum_j w_j`, `log(W_after/W_before) = log sum_j q_j e^{eta_k hat Y_j} <= eta_k sum_j q_j hat Y_j
+ eta_k^2 sum_j q_j hat Y_j^2` (using `e^x <= 1 + x + x^2` for `x <= 1` and `log(1+y) <= y`), and
`log W_end >= eta_k sum hat Y_{j*}` with `W_start = K`. So for every prefix of epoch `k`, and in
particular for its realised length `T_k := sum_u phi_u 1{k(u) = k} <= 2^k`,

    sum_{u : phi_u = 1, k(u) = k} ( hat Y_{j*,u} - sum_l q_{l,u} hat Y_{l,u} - eta_k sum_l q_{l,u} hat Y_{l,u}^2 )
        <=  (log K / eta_k) 1{T_k >= 1} .                                              (6.4)

*Expectations against an event of the fallback start.* Fix `B in G^fb_C`. A fallback visit at `u`
requires `T_C <= u - 1`, and `B cap {T_C <= u-1} in F_{u-1} subseteq F^0_u`, so
`1_B phi_u 1{k(u) = k}` is `F^0_u`-measurable. Multiply (6.4) by `1_B >= 0`, take expectations, and
apply the tower property at `F^0_u` round by round (no optional stopping, and `T_k` need not be known
in advance). With `S_k := sum_u phi_u 1{k(u)=k} Y_u`:

    v E[1_B T_k] - E[1_B S_k]/(1 - gamma_k) - (gamma_k/(1 - gamma_k)) E[1_B T_k]  <=  (K log K/gamma_k) E[1_B 1{T_k >= 1}] ,

using `eta_k K = gamma_k` and `log K/eta_k = K log K/gamma_k`. Multiply by `1 - gamma_k > 0` and use
`v <= 1`:

    E[1_B S_k]  >=  v E[1_B T_k]  -  E[ 1_B ( 2 gamma_k T_k + (K log K/gamma_k) 1{T_k >= 1} ) ] .

Pathwise, `2 gamma_k T_k + (K log K/gamma_k) 1{T_k >= 1} <= c_k 1{T_k >= 1}` with
`c_k := 3 sqrt(K 2^k log K)` if `2^k >= 4 K log K` (then `gamma_k = sqrt(K log K/2^k)` and the two
terms are `2 sqrt(K 2^k log K)` and `sqrt(K 2^k log K)`), and
`c_k := 3 sqrt(K 2^k log K) + 2 K log K` otherwise (then `gamma_k = 1/2`, `2 gamma_k T_k = T_k <= 2^k
< 2 sqrt(K 2^k log K)` and `K log K/gamma_k = 2 K log K`). `T_k >= 1` iff `2^k <= H`, so with
`k_max := floor(log_2 H)`,

    sum_k c_k 1{T_k >= 1}  <=  3 sqrt(K log K) (2^{(k_max+1)/2} - 1)/(sqrt 2 - 1) + 2 K log K (k_max + 1)
                           <=  3 (2 + sqrt 2) sqrt(K H log K) + 2 K log K log_2(2H)  <=  R^dbl_K(H) ,

using `2^{(k_max+1)/2} <= sqrt(2H)`, `sqrt 2/(sqrt 2 - 1) = 2 + sqrt 2` and `3(2 + sqrt 2) < 10.25 <
11`; for `H = 0` both sides are `0`. Summing over the finitely many `k` and using `sum_k T_k = H`,
`E[1_B sum_k S_k] >= v E[1_B H] - E[1_B R^dbl_K(H)]` for every `B in G^fb_C`, which is the
conditional inequality. `QED`

**Lemma 8 (the deviator's fallback utility at a cube).** Uses (f2) and (f3). Suppose every `j != i`
delivers `M_j(X_u)` at its fallback pulls at `C`, and `i` behaves arbitrarily (honestly if
`i in K_H`). Let `nu_i(C) := max_{j != i} M_j^inf(C)`, `Hbar := E[H | G^fb_C]`,
`Rbar := E[R^dbl_K(H) | G^fb_C]`, and `U^fb_i(C)` the utility of `i` from its fallback pulls at
`C`. Then almost surely

    E[ U^fb_i(C) | G^fb_C ]  <=  (1 + mu_i^sup(C) - nu_i(C)) Hbar  +  Rbar  +  (rho_n/3) Hbar ,

and if `i` is honest also `E[U^fb_i(C) | G^fb_C] <= Hbar`.

*Proof.* Let `j0 != i` attain `nu_i(C)`; its fallback target is `M_{j0}(X_u) >= M_{j0}^inf(C) =
nu_i(C)`, so Lemma 7 applies with `j* = j0`, `v = nu_i(C)`: `E[S | G^fb] >= nu_i(C) Hbar - Rbar`
for the total fallback reward `S`. Write `Q_i := sum_u phi_u 1{I_u = i}` and
`A_i := sum_u phi_u 1{I_u = i} m_{i,u}`, and `Qbar_i`, `Abar_i` for their conditional expectations
given `G^fb_C`. For `B in G^fb_C`, `1_B phi_u 1{I_u = i}` is `F^-_u`-measurable, so by (f3)
`E[1_B phi_u 1{I_u = i} Y_u] = E[1_B phi_u 1{I_u = i} m_{i,u}]`: `i`'s share of `S` has conditional
expectation `Abar_i`. Likewise the others' share has conditional expectation
`E[sum_u phi_u 1{I_u != i} M_{I_u}(X_u) | G^fb]`, and for `j != i`,
`M_j(X_u) <= M_j^sup(C) <= M_j^inf(C) + omega <= nu_i(C) + rho_n/3`; so that share is at most
`(nu_i(C) + rho_n/3)(Hbar - Qbar_i)`. Hence

    nu_i(C) Hbar - Rbar  <=  Abar_i + (nu_i(C) + rho_n/3)(Hbar - Qbar_i) ,
    so  Abar_i  >=  nu_i(C) Qbar_i - Rbar - (rho_n/3) Hbar .

Pathwise `U^fb_i(C) = sum_u phi_u 1{I_u = i}(1 + mu_i(X_u) - m_{i,u}) <= (1 + mu_i^sup(C)) Q_i - A_i`,
so `E[U^fb_i(C) | G^fb] <= (1 + mu_i^sup(C) - nu_i(C)) Qbar_i + Rbar + (rho_n/3) Hbar`. Since
`nu_i(C) <= 1`, the coefficient is nonnegative, and `Qbar_i <= Hbar`. For honest `i` each fallback
pull is worth `1 + mu_i(X_u) - m_{i,u} <= 1`. `QED`

### 6.6 The coupling used in part (A)

**Lemma 9 (canonical coupling).** Assume (X) and (A4f-P). Fix `i` and `S'_{i,n} in B^ctx+_{i,n}`.
On one probability space let `(A, theta)` have its (profile independent) law and, independent of it
and of each other, let `(U_t)_{t <= n}` and `(xi_t)_{t <= n}` be i.i.d. uniform on `[0,1]` and
`(Pi_C)_{C in grid}` i.i.d. with the law specified by (f1). Build two executions from these objects
by the mechanism's rules, the deviating one `(S'_i, S^*_{-i})` (primes) and the baseline `S^*`
(stars): the seed at round `t` is `U_t`, the Stage-3 selection at round `t` is the
`xi_t`-quantile of `p_t` (the least `j` with `p_{1,t} + ... + p_{j,t} >= xi_t`), and the priority of
cube `C` is `Pi_C`. Then:

(a) each execution has the law it has in the model;
(b) the filtration `F_u := sigma(A, theta, U_s, xi_s : s <= u, Pi_C : C met by round u)`, with the
    subfields obtained by adding round `u`'s objects in the order of Section 3.1, is admissible for
    both executions;
(c) pathwise, the two executions have the same path `A`, hence by Fact 1 the same Stage-1 rounds at
    every cube, the same agent at each, the same `n_C`, `a_C` and `J'_n`, and the same `Pi_C`; and
    for `j != i` the Stage-1 rewards of `j` coincide.

*Proof.* (a) By Section 3.3 an execution's law is determined by the law of `(A, theta)`, which by
(X) is the same under both profiles, and by the conditional law of each successive variable given
everything before it and the path: `Pi` (the law of (f1)), `I_u` (a point mass in Stages 1 and 2, `p_u`
in Stage 3, by (f2)), the target (a measurable function of the preceding variables, since a strategy
in `B^ctx+` is a function of the path, the agent's history and messages, and `theta_i`), and `U_u`
(uniform, by (f3)); (A4f-P) is exactly the statement that these are the conditional laws given the
path. In the construction each draw is a fixed function of the preceding variables and of one
coordinate (`Pi_C`, `xi_u` or `U_u`) that has not been used before and is independent of
everything already realised, including `A`, so it has the same conditional law. Induction over the
finite sequence of variables gives equality of the joint laws. (b) The same independence gives
(f1) to (f3) in `F`. (c) The path is `A` in both; Fact 1; for `j != i`, the Stage-1 target of `j`
is `M_j(X_t)` in both executions and the seed `U_t` is shared. `QED`

*What Lemma 9 uses.* Freshness of all three kinds of draw given the path, and that their laws do not
depend on the profile; this is how (f1) enters part (A). It does not use that the law of `Pi_C` is
uniform: any fixed law would do.

## 7. Proof of part (B)

Hypothesis used: (f3), in the natural filtration `G`. All agents play `S^*`.

*Revenue as a target sum.* By (f3), `E[Y_t | G^-_t] = m_{I_t,t}`, so by the tower property
`P(n; S^*) = E sum_{t <= n} m_{I_t,t}`. This is the only conditional expectation in the proof.

*A pathwise bound.* Let `bad := E^c cup H^c` (Lemmas 1 and 6, over the `J_n` grid cubes). Split the
rounds into Stage-1 rounds and post Stage-1 rounds at awarded cubes. At a Stage-1 round
`m_{I_t,t} >= 0 >= M_(2)(X_t) - 1`. Off `bad`, at every awarded cube `C`: by Consequence 2a every
Stage-2 target is at least `tau_C`; by Lemma 6(d) no switch ever occurs at `C`, so every post
Stage-1 round at `C` is a Stage-2 round; and by Lemma 4, `m_{I_t,t} >= tau_C >= M_(2)(X_t) - 4 s_n
- (4/3) rho_n` at each of them. On `bad` each post Stage-1 round costs at most `1`. The Stage-1
rounds number at most `sum_C min{V_C, K L_n} <= min{K J'_n L_n, n}`, and `sum_C n_C <= n`. Hence,
pathwise,

    sum_t M_(2)(X_t) - sum_t m_{I_t,t}  <=  min{K J'_n L_n, n}  +  n (4 s_n + (4/3) rho_n)  +  n 1_bad .

*Expectations.* `E min{K J'_n L_n, n} <= e_stage1` by Section 4.1, and
`n Pr(bad) <= n (J_n n^{-5} + J_n n^{-4}/K) = r_n`. This is part (B). `QED`

*What the proof does not use.* No fallback term appears because on the complement of `bad` no cube
switches, so Lemmas 7 and 8 are never invoked; the complement is charged crudely. No step uses a
property of the Stage-3 selection or of the tie break, so part (B) holds even if the Stage-3
selection is adversarial and whatever the law of `Pi_C`. **No conditional expectation is multiplied
by an indicator anywhere in this proof** (the accurate form of the sentence `ADVERSARY.md` 21.1
corrects; the tower step `P = E sum_t m_{I_t,t}` is a conditional expectation, but it is taken once
and never against an event). Nothing couples two executions, and nothing is assumed about how
contexts arrive beyond (f3).

## 8. Proof of part (C)

Hypotheses used: (f2) and (f3) in the natural filtration `G` (for `B^ctx`), or in `hat G` under
(A4f-P) (for `B^ctx+`). `S` is any profile in which honest agents are pointwise honest.

*Revenue as a target sum.* As in part (B), `P(n; S) = E sum_t m_{I_t,t}`.

*Stage 2, pathwise.* Fix an awarded cube `C`, with `v_C`, `h_C` from Lemma 5, Stage-2 length `q_C`
and fallback length `H_C`, so `q_C + H_C = n_C`. Let `bad_C := (E^H_C)^c cup H_C^c`.

* If `W_C = h_C`: every Stage-2 target is at least `v_C` by Lemma 5(ii), so `A_{q_C} >= q_C v_C`.
* If `W_C != h_C` and not `bad_C`: `beta_(2),C >= beta_{h_C,C}`, because `beta_(2),C` is the second
  order statistic **with multiplicity** and `h_C` is not the winner; so by Lemma 5(iii)
  `tau_C >= beta_(2),C - sigma_n >= v_C - 4 s_n - rho_n`, and by Lemma 6(b)
  `A_{q_C} >= q_C (v_C - 4 s_n - rho_n) - 1 - 2 b_n(q_C)`.
* If `W_C != h_C` and `bad_C`: `A_{q_C} >= 0 >= q_C (v_C - 4 s_n - rho_n) - n_C`.

In all three cases, pathwise,

    A_{q_C}  >=  q_C (v_C - 4 s_n - rho_n)  -  1 - 2 b_n(n_C)  -  n_C 1_{bad_C} .          (8.1)

*Fallback, in expectation.* At every fallback visit to `C` at which `h_C` is selected its target is
at least `v_C` (Lemma 5(ii)), so Lemma 7, unconditional form, with `j* = h_C` and `v = v_C` gives
`E[sum over fallback pulls at C of m_{I_u,u}] = E[sum over fallback pulls at C of Y_u] >=
v_C E[H_C] - E[R^dbl_K(H_C)]`, the equality by (f3) and the tower property. No good event is
involved: the comparator's floor is pathwise honesty.

*Summation.* Add (8.1) and the fallback bound, use `v_C >= v_C - 4 s_n - rho_n` on the fallback
rounds, `q_C + H_C = n_C`, `R^dbl_K(H_C) <= R^dbl_K(n_C)`, and, by Lemma 5(i),
`v_C >= b(X_t) - rho_n/3` at every round with `X_t in C`:

    E[ sum of post Stage-1 targets at C ]  >=  E[ sum_{post Stage-1 t, X_t in C} b(X_t) ]  -  E[ n_C ] (4 s_n + (4/3) rho_n)
                                              -  E[ 1_{Comp_C} (1 + 2 b_n(n_C)) + R^dbl_K(n_C) ]  -  E[ n_C 1_{bad_C} ] .

Summing over the `J_n` grid cubes (a finite sum, so it commutes with `E`), charging each Stage-1
round `b <= 1`, and using pathwise `sum_C 1_{Comp_C}(1 + 2 b_n(n_C)) <= f_2(J'_n)` and
`sum_C R^dbl_K(n_C) <= f_3(J'_n)` (at most `J'_n` cubes complete bidding; Cauchy and Schwarz gives
`sum_C sqrt(n_C) <= sqrt(J'_n n)` and `sum_{C : n_C >= 1} sqrt(n_C + 1) <= sqrt(J'_n (n + J'_n))
<= sqrt(2 J'_n n)` since `J'_n <= n`; and `R^dbl_K(0) = 0`), Section 4.1 gives

    P(n; S)  >=  E sum_t b(X_t)  -  ( e_stage1 + e_price + e_mon + e_fb )  -  E sum_C n_C 1_{bad_C} ,

and `E sum_C n_C 1_{bad_C} <= n Pr(union_C bad_C) <= n (J_n n^{-5}/(2K) + J_n n^{-4}/K) <= r_n`.
This is part (C). `QED`

*Remarks.* (i) No conditional expectation is multiplied by an indicator in this proof: the Stage-2
bound (8.1) is pathwise, the fallback bound is Lemma 7's unconditional form, and the complement is
charged pathwise. This removes the within-case martingale step of `PROVER2.md` 17.5
(`ADVERSARY.md` 15.3), which was correct but is no longer needed. (ii) (f1) is not used: case (i)
and case (ii) are both handled whatever the tie break. (iii) (f2) is necessary: `ADVERSARY.md` H1
is an instance satisfying (f3) and every other hypothesis on which part (C) fails by about `0.45 n`.
(iv) The honest slack is `e_price = n(4 s_n + (4/3) rho_n)`, the same as in part (B), which is
`PROVER2.md`'s constant and smaller than `EXPLORER.md`'s `e_rob`.

## 9. Proof of part (A)

Hypotheses used: (X), (A4f-P). Fix `i` and `S'_{i,n} in B^ctx+_{i,n}` and work on the space of
Lemma 9, with the filtration `F` of Lemma 9(b), which is admissible for both executions; so Lemmas
1, 6, 7 and 8 hold in each execution with respect to `F`. Primes denote the deviating execution and
stars the baseline. `U_{i,C}` is `i`'s utility from rounds with `X_t in C`, split into its Stage-1
part `U^(1)_{i,C}` and its post Stage-1 part `U^post_{i,C}`; `u_i = E sum_C U_{i,C}` in both
executions. Every per-pull utility is in `[0,2]`.

**Step 1: Stage 1.** By Lemma 9(c), `i` is pulled at the same Stage-1 rounds of `C` in both
executions, and at such a round the utilities differ by `M_i(X_t) - m'_{i,t} in [0,1]`. So
`U'^(1)_{i,C} - U^{*(1)}_{i,C} <= l_i(C) := #(i's Stage-1 pulls at C) <= L_n` pathwise, and
`sum_C l_i(C) <= min{J'_n L_n, n}`, whose expectation is at most `e_bid`.

**Step 2: winner inclusion and the common price.** By Lemma 9(c) the Stage-1 rounds and seeds at
`C` are shared, and feasibility gives `1{U_t <= m'_{i,t}} <= 1{U_t <= M_i(X_t)}`, so
`beta'_{i,C} <= beta^*_{i,C}` pathwise; the other bids and `Pi_C` coincide. `i` is the winner iff,
for every `j != i`, either `beta_{i,C} > beta_{j,C}` or `beta_{i,C} = beta_{j,C}` and `i` has
higher `Pi_C` priority; raising `beta_{i,C}` preserves each alternative. Hence

    { i wins C in the deviation }  subseteq  { i wins C in the baseline } ,               (9.1)

and on this event `beta_(2),C = max_{j != i} beta_{j,C}` in both, so `tau'_C = tau^*_C =: tau_C`.

**Step 3: the events.** For a cube `C` with `Comp_C`, let
`good_C := E'_C cap H'_C cap E^*_C cap H^*_C`. Off `good_C`, `U'^post_{i,C} <= 2 n_C` and
`U^{*,post}_{i,C} >= 0`, so

    sum_C E[ (U'^post_{i,C} - U^{*,post}_{i,C}) 1_{good_C^c} ]  <=  2 n Pr( union_C good_C^c )
                                                                  <=  2 n ( 2 J_n n^{-5} + 2 J_n n^{-4}/K ) .

**Step 4: case 1, `i` does not win `C` in the deviation, on `good_C`.** The winner `W != i` plays
`S^*`, so by Consequence 2a (on `E'_C`) its Stage-2 targets are at least `tau_C`, and by Lemma 6(d)
(on `H'_C`) `C` never switches in the deviation. So `i` gets no post Stage-1 pull at `C`:
`U'^post_{i,C} = 0 <= U^{*,post}_{i,C}`. Pathwise; no expectation is taken.

**Step 5: case 2, `i` wins `C` in the deviation, on `good_C`.** Let `Gamma_C := good_C cap
{i wins C in the deviation}`. Put `w_C := 1 + mu_i^inf(C) - tau_C` if `i` is strategic and
`w_C := min{1, 1 + mu_i^inf(C) - tau_C}` if honest; `0 <= w_C <= 2` since by Lemma 2
`tau_C <= M_i(X) <= 1`. Write `n_C = q + H` with `q` the Stage-2 length and `H` the fallback length
in the deviation.

*Baseline, lower bound.* By (9.1) `i` wins in the baseline at price `tau_C`; on `E^*_C` Lemma 2
gives `tau_C <= M_i(X)` on `C`, so `S^*_i` delivers `tau_C` (strategic) or `max{mu_i(X_t), tau_C}`
(honest), in both cases at least `tau_C`; on `H^*_C` Lemma 6(d) gives no switch; so all `n_C` post
Stage-1 pulls at `C` are `i`'s, each worth `1 + mu_i(X_t) - tau_C >= w_C` (strategic) or
`min{1, 1 + mu_i(X_t) - tau_C} >= w_C` (honest). Hence `U^{*,post}_{i,C} >= n_C w_C`.

*Deviation, Stage 2.* By Lemma 6(c) on `H'_C` and `mu_i^sup(C) <= mu_i^inf(C) + rho_n/3`,
`U'^pri <= q(1 + mu_i^inf(C) - tau_C) + q rho_n/3 + 1 + 2 b_n(q)`. If `i` is honest also
`U'^pri <= q`. In both cases `U'^pri <= q w_C + q rho_n/3 + 1 + 2 b_n(q)` (if `w_C = 1` use the
second bound, otherwise the first).

*Combination, pathwise on `Gamma_C`.*

    U'^post_{i,C} - U^{*,post}_{i,C}  <=  ( U'^fb - H w_C )  +  q rho_n/3  +  1  +  2 b_n(n_C) .       (9.2)

*The fallback term, with the conditioning made legitimate* (`ADVERSARY.md` G5 and D2). Let
`F'_C := E'_C cap H'_C cap E^*_C cap {i wins C in the deviation} cap {T'_C < infinity}`. It is in the
stopped field `G'^fb_C := F_{T'_C}`: `E'_C`, `E^*_C` and the winner event are functions of the
Stage-1 data at `C`, which are `F_{a_C}`-measurable with `a_C` an `F_0`-measurable round strictly
before `T'_C`; and `H'_C cap {T'_C < infinity}` is in it by Lemma 6(e). `H^*_C` is **not** in it
(the baseline keeps monitoring `C` after the deviation's switch), and it is kept out. On
`{T'_C = infinity}`, `U'^fb = H = 0`, so

    E[(U'^fb - H w_C) 1_{Gamma_C}]  =  E[(U'^fb - H w_C) 1_{F'_C cap H^*_C}]
                                    <=  E[(U'^fb - H w_C) 1_{F'_C}]  +  E[H w_C 1_{F'_C minus H^*_C}]
                                    <=  E[ 1_{F'_C} ( E[U'^fb | G'^fb_C] - w_C Hbar ) ]  +  2 E[ n_C 1_{(H^*_C)^c} ] ,

using `U'^fb >= 0` in the first inequality and, in the second, that `1_{F'_C} w_C` is bounded and
`G'^fb_C`-measurable (`tau_C` is `F_{a_C}`-measurable), so `E[1_{F'_C} w_C H] = E[1_{F'_C} w_C Hbar]`
with `Hbar := E[H | G'^fb_C]`. In the deviation every `j != i` plays `S^*`, so Lemma 8 applies, and
on `F'_C subseteq E'_C` Lemma 3 gives `nu_i(C) >= tau_C`; with `mu_i^sup <= mu_i^inf + rho_n/3`,

    E[U'^fb | G'^fb_C]  <=  (w_C + (2/3) rho_n) Hbar + Rbar      on F'_C

(for honest `i` with `w_C = 1`, use Lemma 8's second bound `<= Hbar`). Therefore

    E[(U'^fb - H w_C) 1_{Gamma_C}]  <=  E[ 1_{F'_C}( (2/3) rho_n H + R^dbl_K(H) ) ]  +  2 E[ n_C 1_{(H^*_C)^c} ] ,

where `Hbar`, `Rbar` were replaced by `H`, `R^dbl_K(H)` inside `E[1_{F'_C} . ]` because
`F'_C in G'^fb_C`. The fallback length `H` is never asserted to be `G'^fb_C`-measurable.

**Step 6: summation.** Adding Steps 1 to 5 over the `J_n` grid cubes, with `q rho_n/3 +
(2/3) rho_n H <= rho_n n_C`, `R^dbl_K(H) <= R^dbl_K(n_C)`, the pathwise bounds
`sum_C 1_{Comp_C}(1 + 2 b_n(n_C)) <= f_2(J'_n)` and `sum_C R^dbl_K(n_C) <= f_3(J'_n)` of
Section 8, `sum_C n_C 1_{(H^*_C)^c} <= n 1_{(H^*)^c}`, and Section 4.1,

    u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)
        <=  e_bid + e_osc + e_mon + e_fb + (4 J_n n^{-4} + 4 J_n n^{-3}/K) + 2 J_n n^{-3}/K ,

and the remainder is at most `6 r_n`. (A cube with `n_C = 0` contributes nothing in Step 5, since
then `q = H = 0` and `U'^post = 0`.) This is part (A). `QED`

*Where exogeneity is used.* Only in Lemma 9, to put the two executions on one space with one path;
everything else in the proof is a lemma that holds in any admissible filtration. Part (A) is false
without it (`ADVERSARY.md` Section 4.4: a path that reacts to the first reward lets an agent
sacrifice one Stage-1 pull and move the rest of the horizon to a cube where its competitor is
worthless, gaining `Theta(n)`). The accurate sentence is `PROVER2.md` 17.4's: part (A) requires that
a deviation cannot move the arrival path.

## 9b. Proof of part (D)

`g_n <= 2 n^{1/(m+3)}`, `h_n <= n^{-1/(m+3)}`, `L_n <= 2 n^{2/(m+3)}`, `J_n <= 2^m n^{m/(m+3)}`,
and `E[J'_n] <= J_n`. Hence `e_bid <= J_n L_n <= 2^{m+1} n^{(m+2)/(m+3)}`,
`e_stage1 <= K 2^{m+1} n^{(m+2)/(m+3)}`, `e_osc = sqrt(m) n h_n log(en) <= sqrt(m) n^{(m+2)/(m+3)}
log(en)`, `n s_n = n sqrt(ell_n/(2 L_n)) <= sqrt(ell_n/2) n^{(m+2)/(m+3)}` so
`e_price <= (4 sqrt(ell_n/2) + (4/3) sqrt(m) log(en)) n^{(m+2)/(m+3)}`,
`e_mon <= 2^m n^{m/(m+3)} + 2^{m/2 + 1} sqrt(ell_n/2) n^{(2m+3)/(2m+6)}`, and
`e_fb <= 11 sqrt(2 K log K) 2^{m/2} n^{(2m+3)/(2m+6)} + 2^{m+1} K log K n^{m/(m+3)} log_2(2(n+1))`.
The exponents `(2m+3)/(2m+6)` and `m/(m+3)` are strictly below `(m+2)/(m+3) = (2m+4)/(2m+6)`, and
`ell_n = log(2 K n^5) <= 5 log(eKn)`. So every error term is `O(n^{(m+2)/(m+3)} log(eKn))` with
constants depending on `K` and `m` only, and `r_n = O(n^{-2})` once `n >= n_J(m)`. Consequently
`S^*` is an additive behavioural asymptotic equilibrium over `B^ctx+` under (X) and (A4f-P),
`P(n; S^*) >= E sum_t M_(2)(X_t) - o(n)` under (f3), and `P(n; S) >= E sum_t b(X_t) - o(n)` under
(f2) and (f3), each uniformly over the `L`-Lipschitz instances satisfying (H2). `QED`

## 10. What the theorem says and does not say

### 10.1 The result is asymptotic, and the horizons are these (`PROVER2.md` Section 18)

Recomputed from the parameter definitions of Section 2 by `check_horizons.py` in this folder
(standard library only, one second). Smallest `log10 n` from which each quantity stays below its
trivial value, `K = 2`, on the worst-case path (`E[J'_n] = min{J_n, n}`), remainders ignored:

| `m` | `sigma_n < 1` (a positive price is possible) | bound (A) `< n` | slack (B) `< n` | slack (C) `< n` |
|:-|:-|:-|:-|:-|
| 1 | 6.06 | 5.25 | 6.77 | 6.93 |
| 2 | 8.50 | 7.54 | 9.35 | 9.47 |
| 3 | 11.07 | 10.05 | 12.04 | 12.15 |
| 4 | 13.75 | 12.74 | 14.87 | 14.96 |
| 6 | 19.40 | 18.39 | 20.81 | 20.89 |
| 10 | 31.70 | 30.71 | 33.66 | 33.70 |

These agree with `PROVER2.md` Section 18 and `ADVERSARY.md` Section 8.6 to within `0.1` in every
entry that both report (those tables are indexed by `D`; here `m = D`). `K = 3` and `K = 5` move
the entries by at most `0.45`. On a path concentrated in one cube (`J'_n = 1`) the (A) threshold
drops by `0.8` decades at `m = 1`, falling to `0.13` at `m = 10`, and the (B)
threshold by under `0.1`: the `J'_n` repair of Section 4.1 is real but does not move the horizons,
which are set by `e_osc` and `e_price`, and those do not depend on `J'_n`.

Reading. In the per-agent model `m = Kd`, so two agents with scalar contexts need `n` of order
`10^{8.5}` before the mechanism can announce a positive price, and three agents with two-dimensional
contexts `10^{19.4}`; the thresholds grow like `exp(c m)` because `J_n` carries `2^m` and `rho_n`
carries `sqrt m`. In the shared-context model `m = d` the `d = 1` row applies whatever `K` is. No
simulation at the horizons run so far (`10^{6.3}`) exhibits part (B) at `m = 1` (its threshold is
`10^{6.77}`), and at `m >= 2` the threshold is `10^{9.35}` rounds or more. Below `sigma_n < 1` the mechanism prices at zero, every bound holds vacuously, and the
theorem says nothing. A paper using this result should state the table rather than let a referee
compute it.

### 10.2 Comparisons, and the sentence under the weakened hypothesis (`ADVERSARY.md` 21.3)

* The exponent `(m+2)/(m+3)` is that of the manuscript's explore-then-commit public contextual
  variant (Grid-ETC) on a grid of the same dimension, not that of its headline public rule
  (Grid-UCB), whose exponent `(m+1)/(m+2)` is strictly smaller since `(m+1)(m+3) < (m+2)^2`.
* Same exponent, very different constants: CG-MESP pays a bidding block of `K L_n` rounds in each
  of up to `J_n` cubes, and `J_n` carries `2^m`; the public error has no such block.
* The benchmark is `M_(2)`, not `M_star`. The public theorem's condition that two agents attain the
  top capacity almost everywhere is exactly `M_(2) = M_star` almost everywhere, so that condition is
  absorbed into the benchmark, not removed. What is genuinely removed is the boundary regularity,
  the positive-mass condition, the top-stable-components condition and, for parts (B) and (C), any
  assumption on arrivals.
* **Under (A4f) alone, parts (B) and (C) are statements about the realised path, which the
  mechanism's own outputs may help determine; a comparison of CG-MESP with Grid-ETC or Grid-UCB is
  then not well posed, because the two mechanisms would face different realised paths. The
  comparison is well posed under (X), where both face the same path law.**

### 10.3 The benchmarks are endogenous under (A4f)

Parts (B) and (C) compare revenue with `E sum_t M_(2)(X_t)` and `E sum_t b(X_t)`. Under (A4f) the
path may react to past rewards and draws, so these sums are evaluated along a path the mechanism
helps determine. The inequalities hold as stated; the sentence they prove is "along the realised
path, whatever it was, the mechanism collects within the stated error of the second capacity
(respectively the best honest intrinsic mean) evaluated along that same path", not "the mechanism
attains a property of the environment". Under (X) the two readings coincide.

### 10.4 What is not covered

* **Convex costs.** This file uses linear costs, as the audited material does. The manuscript's
  convex, `Lambda`-Lipschitz costs change Lemma 6(c), Lemma 8 and part (A) through a cost
  conversion step and multiply the monitoring and fallback terms by `Lambda`; that step is not
  checked here.
* **(H2) is load bearing.** Outside it there is an explicit sequence of instances (`ADVERSARY.md`
  6.3, `K = 4`, triangle-wave capacities with `L = 4 g_n`) on which part (B) fails by `n/4`, and by
  `3n/4` when `sigma_n >= 1/2`. "Uniform over instances" means uniform over the `L`-Lipschitz
  instances with `n >= exp(3L)`.
* **Part (A) is informative only for an agent that wins.** A never-winning agent's baseline utility
  is `O(J'_n L_n)`, the same order as the permitted gain, and it has a real deviation of that order
  (deliver `0` at every Stage-1 pull).
* **No lower bound**, so no optimality claim for `(m+2)/(m+3)`; the matching lower bound on the
  elicitation term needs an instance quantifier (a top gap above `sigma_n + omega`) that the upper
  bound does not.
* No anytime version, no non-Lipschitz capacities, no characterisation of the equilibrium set.

### 10.5 The record, stated accurately (`ADVERSARY.md` Section 20)

Across three adversarial passes and this consolidation, no defect has required a change to the
mechanism and none has changed a rate. The defects have been in the hypotheses (three times, each an
independence a proof used and the hypothesis did not grant), in the conditioning fields of four
steps, in one union-bound count, in two constants, and in four sentences describing the result.

## 11. The step I consider least secure

1. **Lemma 9, the identification of laws.** It is the one place where hypotheses about the model
   ((X) and (A4f-P)) are turned into a pathwise identity between two executions, and part (A) rests
   on it entirely. The argument is the standard Ionescu-Tulcea uniqueness, but it depends on the
   deviation class being exactly "a measurable function of the path, the own history, the messages
   and `theta_i`", and on `theta` having a profile-independent law jointly with `A`. A model in
   which an agent's private randomness could be correlated with the seeds is excluded by (A4f-P),
   and one in which it could be correlated with future arrivals in a profile-dependent way is
   excluded by (X); I believe the two together are exactly what is needed, and `CHECK.md` should
   attack this.
2. **Lemma 7 in conditional form** (the `1_B` tower argument with `B` in a stopped field), which is
   what lets part (A) avoid asserting that `H` is known at the fallback start. The measurability
   step `1_B phi_u in F^0_u` is short and I checked it twice; it is still the step with the most
   quantifiers.
3. The passage from `D` to a general `m` (Section 0 item 3) is notational, but it is new relative to
   the adversarially checked documents, and a reader should confirm that `m` enters only through
   `J_n` and `omega`.
