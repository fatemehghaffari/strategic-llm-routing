# PROVER_SC2 — private capabilities on a continuum with a single shared context

Independent derivation. I did not open `audit/round2/B/theorems/sc1-shared-context/PROVER_SC1.md`
or anything else in this directory; the directory did not exist before I created it, and the only
file I wrote is this one. Sources read in full: `sections/sec2_model.tex`,
`sections/sec4_contextual.tex`, `sections/app_contextual_private.tex` (all 1435 lines, so both the
finite-profile subsection and the continuum subsection, including every remark).

Throughout, `L` is the Lipschitz constant and `L_n` the elicitation length, following the source's
own (unfortunate) collision. `d` is the dimension of the common context, `K` the number of agents,
and `D := Kd` the dimension of the profile space of the general model.

---

## 0. Setting, and the exact relation to the general model

**The shared-context model (SC).** At round `t` the platform observes a single context
`x_t` in `[0,1)^d`. Agent `i`'s capability is `M_i(x_t)` and its intrinsic mean `mu_i(x_t)`, with
`mu_i <= M_i` pointwise, both `L`-Lipschitz on `[0,1)^d` in the Euclidean norm, `L >= 0` unknown to
the platform. `K >= 2`; the honest set `K_H` is nonempty and fixed; honesty is pointwise
(`m_{h,t} >= mu_h(x_t)` after every history). Write

  `M_*(x) = max_j M_j(x)`, `M_(2)(x)` = second largest of `(M_1(x),...,M_K(x))` counting
  multiplicity, `b(x) = max_{h in K_H} mu_h(x)`.

Effort cost is `c_{i,t} = m_{i,t} - mu_i(x_t)`; utilities as in `sec2_model.tex`.

**SC is a sub-case of the general model, but the source's *rate* is not inherited.** Define
`tilde M_i(X) := M_i(x_i)` and `tilde mu_i(X) := mu_i(x_i)` on `[0,1)^D`. These are `L`-Lipschitz
in agent `i`'s own block, so they are a legitimate general-model instance, and on the diagonal
`Delta := {(x,...,x)}` they agree with the SC primitives. So an SC instance *is* a general-model
instance whose arrival path is constrained to lie in `Delta`. Consequently
Proposition `prop:ctx-continuum-exact` applies verbatim and gives exponent `(Kd+2)/(Kd+3)`.
That is the honest baseline, and it is what has to be beaten.

**Why the rate is not inherited, and what has to be re-done.** The exponent of the source is
produced by a three-way balance among elicitation `J_n L_n`, price slack `n s_n` and oscillation
`n h_n log n` with `J_n = g_n^D`. To do better one must change `(h_n, L_n)` and the cube count.
Two routes:

* *Route A (keep the `D`-grid, retune).* Run CG-MESP on `[0,1)^D` with `h_n = n^{-1/(d+3)}` and
  `L_n = n^{2/(d+3)}`. The diagonal meets exactly `g_n^d` of the `g_n^D` cubes, so the *visited*
  cube count `J'_n` is at most `g_n^d` and every per-cube charge is fine. But two union bounds in
  the source run over "the deterministic set of `J_n` grid cubes" (Lemma `lem:ctx-bidconc`,
  Lemma `lem:ctx-monitor-cont`(a)), and their numerical conclusions
  (`Pr(E^c) <= n^{-4}`, `Pr(H^c) <= n^{-3}/K`) need `J_n <= n`. With `J_n = g_n^{Kd} = n^{Kd/(d+3)}`
  that fails badly. One can repair it by restricting the union bound to the `g_n^d` cubes that meet
  `Delta` — but that is a step that uses the support of the arrival law, i.e. exactly the kind of
  step the hostile brief warns about. It is legitimate (`Delta` is a deterministic set fixed before
  play, and cubes off `Delta` are never visited, so no measurability of the visited set is
  introduced), but it is a **re-proof, not a re-labelling**.
* *Route B (grid the common space).* Tile `[0,1)^d` with `J_n = g_n^d` half-open cubes of side
  `h_n`. The cube containing `x_t` is in bijection with the `D`-cube containing `X_t` that meets
  `Delta`, so Route B is the *same mechanism* as Route A, presented on the space the platform
  actually observes, and the union bounds are over a deterministic set of `g_n^d` cubes with no
  reference to `Delta` at all.

I take Route B. It is what the candidate proposes, and it is the right presentation: the platform
observes `x_t in [0,1)^d`, so it knows `d`, and nothing in the mechanism ever refers to `D`.

---

## 1. The mechanism I am willing to sign: SC-MESP

Identical to CG-MESP of `app:ctx-private-continuum` with the cube of `x_t` in `[0,1)^d` in place of
the cube of `X_t` in `[0,1)^D`, and with these constants, **all computed from the global horizon `n`
and from `K, d` only** (a cube's visit count is not known when the mechanism starts, so no per-cube
tuning is available):

```
g_n := ceil( n^{1/(d+3)} ),    h_n := 1/g_n,    J_n := g_n^d
L_n := ceil( n^{2/(d+3)} )
ell_n := log(2 K n^5)
s_n  := sqrt( ell_n / (2 L_n) )
rho_n := sqrt(d) * h_n * log(en)                <-- sqrt(d), not sqrt(D); see §4(c)
sigma_n := 3 s_n + rho_n
b_n(r) := sqrt( r * ell_n / 2 ),  b_n(0) := 0
R^dbl_K(V) := 11 sqrt( K (V+1) log K ) + 2 K log K * log_2( 2(V+1) ),  R^dbl_K(0) := 0
```

Cubes are instantiated lazily. Each cube `C` keeps `V_C`, Stage-1 reward sums, `tau_C`, `W_C`, the
monitor count and sum, the fallback clock and EXP3 weights, and one uniform priority permutation
`Pi_C` drawn when `C` is first met.

* **Stage 1**, while `V_C <= K L_n`: pull agent `((V_C - 1) mod K) + 1`; the schedule reads no
  reward, no bid and no coin. At `V_C = K L_n` form `beta_{j,C} := L_n^{-1} sum_{r<=L_n} Y_{j,C,r}`,
  let `W_C` be a largest bidder with ties by highest `Pi_C` priority, let `beta_{(2),C}` be the
  second order statistic with multiplicity, and announce
  `tau_C := ( beta_{(2),C} - 3 s_n - rho_n )_+`.
  A cube receiving fewer than `K L_n` visits never awards, never prices and never monitors.
* **Stage 2**, until a local switch: pull `W_C`; switch at the first local primary index `r` with
  `Z_r < r tau_C - b_n(r)`.
* **Stage 3**, after a switch at `C`: explicit-exploration EXP3 over all `K` agents on the visits to
  `C`, restarted in doubling epochs on the local fallback clock, epoch `k` covering local fallback
  times `2^k,...,2^{k+1}-1` with fresh weights, `gamma_k = min{1/2, sqrt(K log K / 2^k)}`,
  `eta_k = gamma_k/K`. No local horizon is used.
* **Messages**: a selected agent is told the cube's phase and, in Stage 2 or 3, `tau_C`.
* **`S^*`**: capability `M_i(x_t)` at a Stage-1 pull and at a fallback pull;
  `min{tau_C, M_{W_C}(x_t)}` at a Stage-2 pull if strategic, `max{mu_i(x_t), min{tau_C, M_i(x_t)}}`
  if honest.

Running time `O(K + d)` per round, memory `O(K min{J_n, n})`; polynomial, with no enumeration of
`J_n`.

**Standing hypotheses (H).** `K >= 2`; `n >= 2K`; `mu_i <= M_i` on `[0,1)^d`, both `L`-Lipschitz,
`L` unknown; nonempty honest set; and

```
(H-osc)   log(en) >= 3L        [sufficient: n >= exp(3L)]
(H-grid)  J_n <= n             [holds for n >= 2^{d(d+3)/3}, a threshold depending on d alone]
```

**Probabilistic hypotheses, in conditional form only.** I use the source's (A3) exactly as quoted in
`app:ctx-private-continuum`, with `x_u` for `X_u`. Fix a round `u` and set
`G^0_u := sigma(G_{u-1}, x_u)`, `G^k_u := sigma(G^{k-1}_u, the mechanism's k-th randomisation at u)`,
`G^-_u := sigma(G^kappa_u, the selected agent's coin at u, m_{I_u,u})`, `G_u := sigma(G^-_u, U_u)`.

> **(A3), in the form used here.** At every round `u` the mechanism's randomisations are drawn in
> the order the mechanism specifies them, and then the reward seed. Each has its specified law
> conditionally on the field generated by everything realised before it: the `k`-th randomisation of
> the mechanism has its specified law conditionally on `G^{k-1}_u`, and `U_u` is uniform on `[0,1]`
> conditionally on `G^-_u`, with `Y_u = 1{U_u <= m_{I_u,u}}`. The selected agent's private
> randomisation and its target are drawn between the last mechanism randomisation and the seed and
> are unconstrained: whatever the agent's strategy specifies, they are part of everything realised
> before the seed, and the seed clause is stated conditionally on them.

For SC-MESP, `kappa = 2`: (f1) the priority `Pi_{C(x_u)}` if `C(x_u)` is met for the first time at
`u`, uniform on permutations of `[K]` conditionally on `G^0_u`; (f2) the selection, deterministic in
Stages 1 and 2 and drawn with law `p_u` conditionally on `G^1_u` in Stage 3; then (f3) the seed.
Nothing is assumed about how `x_u` is generated: it may be an arbitrary measurable function of
everything realised strictly before round `u`'s own draws, plus fresh randomness.

> **(A2), in the form used here.** The realised context sequence is the *same random object* in the
> two coupled executions of Part (i); equivalently, conditionally on everything realised before
> round `u`, the law of `x_u` does not depend on which of the two strategies agent `i` is playing.
> Exogeneity in the sense of `sec2_model.tex` delivers this and is formally stronger.

I deliberately do **not** write "the contexts are independent of the reward seeds", "the bids of
distinct agents are independent", or any similar list. No step below uses any such clause, and §5
checks that claim against the two clauses one would be tempted to write down.

---

## 2. The statement I sign

Define, with `J'_n` the number of cubes the realised path visits at least once (so `J'_n <=
min{J_n, n}`) and `n_C := (V_C - K L_n)_+`:

```
e_bid     := min{ E[J'_n] L_n , n }
e_stage1  := min{ K E[J'_n] L_n , n }
e_osc     := n rho_n
e_mon     := E[J'_n] + 2 sqrt( E[J'_n] n ell_n / 2 )
e_fb      := 11 sqrt( 2 K E[J'_n] n log K ) + 2 K log K E[J'_n] log_2(2(n+1))
e_price   := n ( 4 s_n + (4/3) rho_n )
```

> **Proposition SC (SC-MESP, exact form).** Assume (H). Run SC-MESP. Then:
>
> **(i)** under (A2) together with (A3), for every agent `i` and every
> `S'_{i,n}` in the enlarged behavioural class `B^{ctx+}_{i,n}`,
> ```
> u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)
>     <= e_bid + e_osc + e_mon + e_fb + 4 n^{-3} + 4 K^{-1} n^{-2} ;
> ```
> **(ii)** under the seed clause of (A3) alone, with every agent playing `S^*`,
> ```
> P(n; S^*_n) >= E sum_{t<=n} M_(2)(x_t) - ( e_stage1 + e_price + O(n^{-2}) ) ;
> ```
> **(iii)** under the Stage-3 selection clause and the seed clause of (A3), for every feasible
> behavioural profile in which each agent plays some strategy in `B^{ctx}_{j,n}` and every honest
> agent respects pointwise honesty — the deviating set being all of `[K]` if it likes,
> ```
> P(n; S) >= E sum_{t<=n} b(x_t) - ( e_stage1 + e_price + e_mon + e_fb + O(n^{-2}) ).
> ```
>
> Parts (ii) and (iii) place no condition whatever on the context process. No condition on the top
> set, on the boundary of any cube, on the mass of any cube, on any capability gap, and no property
> of the context law appears anywhere; the only instance-dependent hypothesis is (H-osc).

> **Corollary SC-rate.** Under (H), with `J_n <= 2^d n^{d/(d+3)}` and `E[J'_n] <= min{J_n, n}`:
> ```
> e_bid    <= 2^{d+1} n^{(d+2)/(d+3)}
> e_stage1 <= K 2^{d+1} n^{(d+2)/(d+3)}
> e_osc    <= sqrt(d) n^{(d+2)/(d+3)} log(en)
> n s_n    <= sqrt(ell_n/2) n^{(d+2)/(d+3)}
> e_price  <= ( 4 sqrt(ell_n/2) + (4/3) sqrt(d) log(en) ) n^{(d+2)/(d+3)}
> e_mon    <= 2^d n^{d/(d+3)} + 2^{d/2+1} sqrt(ell_n/2) n^{(2d+3)/(2d+6)}
> e_fb     <= 11 sqrt(2 K log K) 2^{d/2} n^{(2d+3)/(2d+6)}
>             + 2^{d+1} K log K n^{d/(d+3)} log_2(2(n+1))
> ```
> The three exponents occurring are `(d+2)/(d+3) = (2d+4)/(2d+6)`, `(2d+3)/(2d+6)` and `d/(d+3)`,
> and the first strictly dominates the other two. Hence for fixed `K, d` there is `n_2(K,d)` such
> that for `n >= max{ n_2(K,d), exp(3L) }` every error term is
> `O(n^{(d+2)/(d+3)} log(eKn))` with constants depending only on `K` and `d`. Sharper, and this is
> the form I prefer:
> * **(i)** `<= ( 2^{d+1} + sqrt(d) log(en) + 1 ) n^{(d+2)/(d+3)}` for `n >= n_2(K,d)`:
>   **the leading constant of part (i) is entirely free of `K`**;
> * **(ii), (iii)** `<= ( K 2^{d+1} + 4 sqrt(ell_n/2) + (4/3) sqrt(d) log(en) + 1 ) n^{(d+2)/(d+3)}`,
>   whose leading constant is **exactly linear in `K`**, through `e_stage1` alone.

---

## 3. Proof

### 3.1 The one place where the geometry genuinely changes

> **Lemma SC-osc (within-cube oscillation).** Put `omega := L sqrt(d) h_n`. For every cube `C` of
> the `[0,1)^d` grid and every `j`, `M_j^sup(C) - M_j^inf(C) <= omega` and likewise for `mu_j`; the
> same bound holds for the oscillation on `C` of `M_*`, `M_(2)` and `b`. Under (H-osc),
> `omega <= rho_n / 3`. And for every `x in C`, `M_j(x) - omega <= bar M_{j,C} <= M_j(x) + omega`,
> where `bar M_{j,C} := L_n^{-1} sum_{r<=L_n} M_j(x_{t_{j,C,r}})` averages `M_j` over the contexts
> at agent `j`'s own Stage-1 rounds in `C`.

*Proof.* Two contexts in the same cube differ by at most `h_n` in each of `d` coordinates, so by at
most `sqrt(d) h_n` in Euclidean norm; `M_j` and `mu_j` are `L`-Lipschitz, giving `omega`. `M_*`,
`M_(2)` and `b` are order statistics of the vector `(M_1(x),...,M_K(x))` (resp. of
`(mu_h(x))_{h in K_H}`), and order statistics are 1-Lipschitz in the supremum norm, so their
oscillation is at most the largest coordinate oscillation, again `omega`. By (H-osc),
`L sqrt(d) h_n <= (1/3) sqrt(d) h_n log(en) = rho_n/3`. The last claim holds because `bar M_{j,C}`
is an average of values of `M_j` at contexts of `C`, hence lies in `[M_j^inf(C), M_j^sup(C)]`, an
interval of length at most `omega` containing `M_j(x)`. ∎

This is the **only** role of `L` and of (H-osc): `L` never enters a bound, only the hypothesis. Two
observations that matter:

1. In the source, `omega := L sqrt(D) h_n`, but the source's own proof of `lem:ctx-osc` establishes
   the sharper `L sqrt(d) h_n` and then discards it (`sqrt(d) h_n <= sqrt(D) h_n`). So `sqrt(D)` is
   already slack in the general model by a factor `sqrt(K)` (see §7, disagreement 4).
2. (H-osc) is **dimension-free**: `omega <= rho_n/3` reads `L sqrt(d) h_n <= (1/3) sqrt(d) h_n
   log(en)`, and the dimension factor cancels on both sides. This is exactly why the threshold does
   not move when `D` is replaced by `d`; see §4(c).

### 3.2 Everything else transfers, and here is the audit

I read each lemma of `app:ctx-private-continuum` and recorded what it actually uses. The statement
of SC-MESP differs from CG-MESP only by the substitution

  "`C` = the `[0,1)^D`-cube containing `X_t`"  ↦  "`C` = the `[0,1)^d`-cube containing `x_t`",
  "`M_j(x_{j,t})`" ↦ "`M_j(x_t)`", `D ↦ d` in `g_n, J_n, L_n, rho_n`.

| source object | what its proof actually uses | transfers? |
|---|---|---|
| `eq:ctx-feas` (`bar A <= bar M`) | pointwise feasibility only | verbatim |
| `lem:ctx-osc` | Lipschitz + order statistics | **re-proved** as Lemma SC-osc, with `sqrt(d)` |
| `lem:ctx-bidconc` | seed clause; `phi_s` is `G^0_s`-measurable; union bound over the *deterministic* `J_n` cubes and `K` agents; needs `J_n <= n` | verbatim, with `J_n = g_n^d` |
| `lem:ctx-price-meet` | nothing probabilistic; `E_C`, feasibility, SC-osc | verbatim |
| `lem:ctx-price-dom` | nothing probabilistic; `E_C`, SC-osc | verbatim |
| `lem:ctx-price-second` | nothing probabilistic; `E_C`, SC-osc, monotonicity of the order statistic | verbatim |
| `lem:ctx-honest-floor` (i),(ii) | nothing probabilistic; (ii) pointwise honesty | verbatim |
| `lem:ctx-honest-floor` (iii) | seed clause (one-sided form of bid concentration) | verbatim |
| `lem:ctx-monitor-cont` | seed clause; `phi_s` is `G^0_s`-measurable; union over the deterministic `J_n` cubes and `r <= n`; needs `J_n <= n` | verbatim |
| `lem:ctx-fallback-cont` | Stage-3 selection clause + seed clause; pathwise potential inequality per doubling epoch; tower property | verbatim |
| `lem:ctx-dev-fallback` | the previous lemma + SC-osc (`M^sup <= M^inf + omega`) | verbatim |
| bid domination inside the proof of (i) | (A2): same Stage-1 rounds and same agent at each; `S^*_j` delivers a number determined by `x_t`; shared seed gives `1{U_t <= m'} <= 1{U_t <= M_i(x_t)}` pathwise | verbatim |
| cube locality | every branch reads only `C`'s own state | verbatim |
| the concavity/Jensen steps for `E[J'_n]` | concavity of `min{ · L_n, n}` and of the square roots | verbatim |

For each, the substitution changes no inequality. I re-derive the three proofs at the level of
detail at which something could go wrong.

**Part (i).** Fix `i` and `S'_{i,n} in B^{ctx+}_{i,n}`; couple the deviating and baseline executions
by the same context path, seed array, priorities, EXP3 coins and private coins. Utility decomposes
over cubes in both executions — a decomposition of a random variable, not an independence claim —
so it suffices to bound `E[U'_{i,C} - U^*_{i,C}]` cube by cube. Write `E_C, H_C` for the events of
Lemma `lem:ctx-bidconc` and Lemma `lem:ctx-monitor-cont` in the deviating execution, `E^*_C, H^*_C`
for the baseline, `bad_C` for the union of the complements, so
`Pr(bad_C) <= 2 n^{-5} + 2 K^{-1} n^{-4}` (per-cube: `Pr(E_C^c) <= 2K e^{-ell_n} = n^{-5}` and
`Pr(H_C^c) <= 2n e^{-ell_n} = 1/(K n^4)`, twice over for the two executions).

*Bid domination.* Under (A2) the Stage-1 schedule at `C` is a function of the context path alone, so
the two executions have the same Stage-1 rounds at `C` and pull the same agent at each; for `j != i`
the Stage-1 rewards are literally the same bits, because `S^*_j` delivers `M_j(x_t)`, a number
determined by the round's context, and the seed is shared. At `i`'s Stage-1 round `t`, feasibility
gives `m'_{i,t} <= M_i(x_t)`, so `1{U_t <= m'_{i,t}} <= 1{U_t <= M_i(x_t)}` and hence
`beta'_{i,C} <= beta^*_{i,C}` pathwise. The other bids agree and `Pi_C` is shared, so every
inequality defining "`i` is a largest bidder" is preserved:
```
{ i wins at C under the deviation }  ⊆  { i wins at C in the baseline },
```
and on that event `beta_{(2),C} = max_{j != i} beta_{j,C}` in both, so `tau_C` is the same number in
both and does not depend on anything `i` does. Pathwise; no concentration, no independence.

*Stage 1 at `C`.* Same rounds, per-pull utility difference `M_i(x_t) - m'_{i,t} in [0,1]`, so the
difference is at most `l_i(C) <= L_n`, and `sum_C l_i(C) <= min{J'_n L_n, n}`. Cubes with
`V_C < K L_n` contribute only this.

*Post Stage 1, on `E_C ∩ H_C ∩ E^*_C ∩ H^*_C`.* If `i` does not win under the deviation, the winner
`W != i` plays `S^*`, so by Lemma `lem:ctx-price-meet` (which holds on `E_C` whoever `W` is and
whatever anyone bid) its Stage-2 target is at least `tau_C` at every context of `C`; by
`lem:ctx-monitor-cont`(d) no switch occurs, `i` gets no post-Stage-1 pull, and the baseline's
post-Stage-1 utility is nonnegative, so the contribution is at most `0`. If `i` wins under the
deviation, it wins in the baseline at the same price. With `n_C = q + H` and
```
w_C := 1 + mu_i^inf(C) - tau_C        (i strategic)
w_C := min{1, 1 + mu_i^inf(C) - tau_C} (i honest),
```
nonnegative because `lem:ctx-price-meet` gives `tau_C <= M_i(x) <= 1 <= 1 + mu_i^inf(C)`:
`lem:ctx-monitor-cont`(c) with `mu_i^sup(C) <= mu_i^inf(C) + rho_n/3` (Lemma SC-osc) gives
`U'^pri <= q w_C + q rho_n/3 + 1 + 2 b_n(q)`; `lem:ctx-dev-fallback` together with
`lem:ctx-price-dom` (`tau_C <= nu_i(C)`, needing only `E_C`) gives
`E[U'^fb | fallback start] <= H w_C + (2/3) rho_n H + R^dbl_K(H)`. Adding,
`E[U'^post_{i,C}] <= n_C w_C + n_C rho_n + 1 + 2 b_n(n_C) + R^dbl_K(n_C)`. On `E^*_C` the baseline
delivers at least `tau_C` at every Stage-2 pull, so by `lem:ctx-monitor-cont`(d) in the baseline it
never switches, receives all `n_C` post-Stage-1 pulls, and earns at least `w_C` each:
`U^{*,post}_{i,C} >= n_C w_C`. Difference at most
`n_C rho_n + 1 + 2 b_n(n_C) + R^dbl_K(n_C)`.

*Legitimacy of the conditioning.* Unchanged from the source and worth repeating because it is the
delicate point. Only two conditional expectations are taken, both conditional on the field at `C`'s
fallback start, and the events multiplying them must lie in that field. `E_C` does (a function of
`C`'s Stage-1 rewards); `H_C` does (the Stage-2 martingale at `C` is frozen at the switch); `E^*_C`
does (the baseline lives on the same space and its Stage-1 rewards at `C` occur at the same rounds).
`H^*_C` does **not**, because in the winning case the baseline runs Stage 2 through all `n_C`
post-Stage-1 visits, past the deviating execution's switch. With `F := E_C ∩ H_C ∩ E^*_C` and
`good := F ∩ H^*_C`, on `good`
`U'^post - U^{*,post} <= U'^fb - H w_C + q rho_n/3 + 1 + 2 b_n(q)` pathwise, and since
`U'^fb >= 0` and `0 <= w_C <= 2`,
```
E[(U'^fb - H w_C) 1_good] <= E[(U'^fb - H w_C) 1_F] + E[H w_C 1_{F \ good}]
                          <= E[ 1_F ( (2/3) rho_n H + R^dbl_K(H) ) ] + 2 n_C Pr((H^*_C)^c),
```
with `Pr((H^*_C)^c) <= 2 n e^{-ell_n}` per cube and `sum_C n_C <= n`, so the extra charge is at most
`2 n^{-3}/K`. Nothing conditions on a future event.

*Off the good events and summation.*
`sum_C E[(U'_{i,C} - U^*_{i,C}) 1_{bad_C}] <= 2n sum_C Pr(bad_C) <= 2n · J_n · (2n^{-5} + 2K^{-1}n^{-4})
<= 4 n^{-3} + 4 K^{-1} n^{-2}` using (H-grid) `J_n <= n`. Then `sum_C n_C rho_n <= e_osc`;
`sum_C [1 + 2 b_n(n_C)] <= J'_n + 2 sqrt( J'_n (ell_n/2) sum_C n_C ) <= J'_n + 2 sqrt(J'_n n ell_n/2)`
and `sum_C R^dbl_K(n_C) <= 11 sqrt(2 K J'_n n log K) + 2 K log K J'_n log_2(2(n+1))`, both by
Cauchy–Schwarz with `sum_C n_C <= n` and `J'_n <= n`; taking expectations, with concavity for the
elicitation term and Jensen through the square roots, yields `e_bid`, `e_mon`, `e_fb`. The bound is
uniform in the context path and in the deviation, so integrating and then taking the supremum is
legitimate. ∎

**Part (ii).** All agents play `S^*`, so `bar A_{j,C} = bar M_{j,C}` for every `j, C`. By the seed
clause and the tower property applied at each fixed `t`, `P(n;S^*) = E[ sum_t m_{I_t,t} ]`, so no
optional stopping is needed anywhere. Discard the at most `min{K J'_n L_n, n}` Stage-1 rounds, where
the target is nonnegative and `M_(2) <= 1`. Work on `E_C ∩ H_C` cube by cube. By
`lem:ctx-price-meet` the Stage-2 target at an awarded cube is at least `tau_C` at every context, so
by `lem:ctx-monitor-cont`(d) **no cube ever switches**: every post-Stage-1 round is a Stage-2 round
and the fallback lemma is never invoked, which is why part (ii) needs only the seed clause. By
Lemma `lem:ctx-price-second` (with Lemma SC-osc supplying `omega <= rho_n/3`), for every
post-Stage-1 round `t` with `x_t in C`,
```
m_{I_t,t} >= tau_C >= M_(2)(x_t) - 4 s_n - (4/3) rho_n.
```
Summing over the post-Stage-1 rounds of `C` and over cubes, and charging `E_C^c ∪ H_C^c` at `n_C`
rounds each with `M_(2) <= 1` over the deterministic set of `J_n` cubes, gives (ii). No conditional
expectation is ever multiplied by an indicator; the mechanism's own randomisation never enters. ∎

**Part (iii).** Every agent may play anything feasible, subject to pointwise honesty for
`h in K_H`. Again `P(n;S) = E[sum_t m_{I_t,t}]` and the Stage-1 rounds are discarded. Fix an
awarding cube `C`, take `v_C := max_{h in K_H} mu_h^inf(C)` and `h_C` attaining it with a fixed tie
break, and work on `E^H_C ∩ H_C`, where `Pr((E^H_C)^c) <= e^{-ell_n}` and `beta_{h_C,C} >= v_C - s_n`.

If `W_C = h_C`, every Stage-2 target at `C` is at least `mu_{h_C}(x_t) >= v_C` by honesty, so the
Stage-2 target sum is at least `v_C q`; if a switch occurs, `lem:ctx-fallback-cont` with comparator
`h_C` and `v = v_C` — legitimate by the pathwise honest-floor statement, which holds whatever the
other agents do — gives fallback delivery at least `v_C H - E[R^dbl_K(H)]`. If `W_C != h_C`, then
`beta_{(2),C} >= beta_{h_C,C} >= v_C - s_n`, so `tau_C >= v_C - s_n - sigma_n = v_C - 4 s_n - rho_n`;
on `H_C`, `lem:ctx-monitor-cont`(b) gives `A_q >= q tau_C - 1 - 2 b_n(q)`, and a switch is handled by
the same comparator. The second case is the weaker. By Lemma SC-osc,
`v_C >= b(x_t) - omega >= b(x_t) - rho_n/3` for every `x_t in C`, so the post-Stage-1 contribution of
`C` is at least
```
sum_{post-Stage-1 t with x_t in C} b(x_t) - n_C (4 s_n + (4/3) rho_n) - 1 - 2 b_n(n_C) - R^dbl_K(n_C).
```
Summing over cubes with the two concavity steps, charging the Stage-1 rounds at `b <= 1` each and
the complements at `n sum_C Pr((E^H_C)^c ∪ H_C^c) = O(n^{-2})` over the deterministic set of `J_n`
cubes, gives (iii), uniformly over the joint behavioural profile. The one step to write down: the
two cases equate the expected Stage-2 reward at `C` with the expected target sum *within the case*,
i.e. `E[(Z_r - A_r) 1{case}] = 0`, whereas `lem:ctx-monitor-cont`(e) gives only `E[Z_r - A_r] = 0`.
This is correct because `{W_C = h_C}` and `E^H_C` are both determined by the Stage-1 bids at `C`,
hence at `C`'s award round, which precedes every Stage-2 pull at `C`, so the stopped-martingale
argument applies with that indicator inserted into `phi_s`. `H_C` is *not* award-time measurable and
the proof does not multiply a conditional expectation by it: it uses `A_q >= 0` and charges
`E[q tau_C 1_{H_C^c}] <= n Pr(H_C^c)`. ∎

### 3.3 (a) The balance, with the arithmetic

Write `h_n = n^{-a}` and `L_n = n^{c}`, ignore logarithms, and read off the three leading charges:

```
elicitation  :  K J_n L_n   = K h_n^{-d} L_n  =  K n^{ad + c}
price slack  :  n s_n       ≍ n sqrt(log n / L_n)  =  n^{1 - c/2} sqrt(log n)
oscillation  :  n rho_n     ≍ sqrt(d) n h_n log n  =  n^{1 - a} log n
```

Set the three exponents equal:

```
ad + c = 1 - c/2 = 1 - a.
```

From `1 - c/2 = 1 - a`:  `c = 2a`.
Substitute into `ad + c = 1 - a`:  `ad + 2a = 1 - a`, i.e. `a(d + 3) = 1`, so

```
a = 1/(d+3),   c = 2/(d+3),
h_n = n^{-1/(d+3)},   L_n = n^{2/(d+3)},   J_n = n^{d/(d+3)},
common value = n^{1-a} = n^{(d+2)/(d+3)}.
```

Check the non-binding terms at this point:
`e_mon ≍ sqrt(J_n n log n) = n^{(d/(d+3)+1)/2} sqrt(log n) = n^{(2d+3)/(2d+6)} sqrt(log n)`, and
`(d+2)/(d+3) = (2d+4)/(2d+6) > (2d+3)/(2d+6)`, strictly. `e_fb`'s leading part has the same exponent
`(2d+3)/(2d+6)`; its second part is `n^{d/(d+3)} log n`, and `d/(d+3) < (d+2)/(d+3)`. So both are
strictly dominated and the balance is genuinely three-way: **elicitation, price slack and
oscillation, and nothing else**. This is the Grid-ETC balance `h_n = n^{-1/(d+3)}`,
`q_n = n^{2/(d+3)}` of `thm:grid-etc` with `L_n` in the role of `q_n`, read at `d` instead of `D`.

**Resulting exponent: `(d+2)/(d+3)`, with a `log(en)` factor from the oscillation term.**

`K` does not appear in `a` or `c`: it sits in front of the elicitation charge as a multiplicative
constant, which shifts the optimum's constants and not its exponents. (See §7, item 8, for the
`K`-tuned variant.)

### 3.4 (b) Exact `K`-dependence, exponent versus constant

| term | bound | `K` in the exponent of `n` | `K` in the constant | appears in |
|---|---|---|---|---|
| `e_bid` | `2^{d+1} n^{(d+2)/(d+3)}` | none | **none** | (i) |
| `e_osc` | `sqrt(d) n^{(d+2)/(d+3)} log(en)` | none | **none** | (i) |
| `e_stage1` | `K 2^{d+1} n^{(d+2)/(d+3)}` | none | **exactly linear in `K`** | (ii),(iii) |
| `e_price` | `(4 sqrt(ell_n/2) + (4/3) sqrt(d) log(en)) n^{(d+2)/(d+3)}` | none | `sqrt(ell_n) = sqrt(log(2Kn^5))`, i.e. `O(sqrt(log K))` inside a square root | (ii),(iii) |
| `e_mon` | `2^d n^{d/(d+3)} + 2^{d/2+1} sqrt(ell_n/2) n^{(2d+3)/(2d+6)}` | none | `O(sqrt(log K))`, on a **sub-leading** power | (i),(iii) |
| `e_fb` | `11 sqrt(2K log K) 2^{d/2} n^{(2d+3)/(2d+6)} + 2^{d+1} K log K n^{d/(d+3)} log_2(2(n+1))` | none | `sqrt(K log K)` and `K log K`, both on **sub-leading** powers | (i),(iii) |
| residuals | `4 n^{-3} + 4 K^{-1} n^{-2}` | none | `1/K` | (i) |

Consequences I am willing to state:

* **`K` never enters the exponent of `n`.** It entered the source's exponent only through
  `D = Kd`, and with a common context there is no such route.
* **Part (i)'s leading constant is `K`-free**: `(i) <= (2^{d+1} + sqrt(d) log(en)) n^{(d+2)/(d+3)}`
  plus terms of order `sqrt(K log K) n^{(2d+3)/(2d+6)}` and `K log K n^{d/(d+3)} log n`. So
  `O_d(n^{(d+2)/(d+3)} log(en))` for `n >= n_2(K,d)`, not merely `O_{d,K}`.
* **Parts (ii) and (iii) are linear in `K` at leading order**, through `e_stage1 = K J_n L_n` and
  nothing else: all `K` agents must be elicited in every cube. `O_d(K n^{(d+2)/(d+3)} log(eKn))`.
* The thresholds beyond which the sub-leading `K` terms are dominated are: `sqrt(K log K) <=
  n^{1/(2d+6)}` and `K log K log n <= n^{2/(d+3)}`. For fixed `K` these hold for large `n`; they are
  what `n_2(K,d)` collects. **The result is asymptotic in `n` with `K, d` fixed; I do not claim it
  uniformly over `K` growing with `n`.**
* `ell_n = log(2Kn^5)` carries `K` because the bid union bound runs over `K` agents. That is the
  only place `K` enters `s_n`.

### 3.5 (c) `sqrt(d)` or `sqrt(D)`, and the horizon threshold

**`sqrt(d)`, and `sqrt(D)` would be waste.** `rho_n` is used in exactly six places, and in every one
of them it is used only through the inequality `omega <= rho_n/3`, where `omega` is the maximum
within-cube oscillation of any of `M_j`, `mu_j`, `M_*`, `M_(2)`, `b`:

1. `lem:ctx-price-meet`: `bar M_{W,C} <= M_W(x) + omega`;
2. `lem:ctx-price-dom`: `bar M_{j*,C} <= M_{j*}^inf(C) + omega`;
3. `lem:ctx-price-second`: `beta_{(2),C} >= M_(2)(x) - omega - s_n`;
4. `lem:ctx-dev-fallback`: `M_{j'}^sup(C) <= M_{j'}^inf(C) + omega`;
5. part (i): `mu_i^sup(C) <= mu_i^inf(C) + omega`;
6. `lem:ctx-honest-floor`(i): `b(x) <= v_C + omega`.

With the grid on the common space, `omega = L sqrt(d) h_n` (Lemma SC-osc), so `rho_n = sqrt(d) h_n
log(en)` is exactly what the six uses need. Writing `sqrt(D) = sqrt(K) sqrt(d)` would be *sound*
(larger `rho_n`, all six inequalities still hold) but would multiply `e_osc` and the `rho_n` part of
`e_price` by `sqrt(K)` for nothing. So: **`sqrt(d)`, and the candidate is right.**

**`n >= exp(3L)` is still exactly the right threshold, and it is unchanged.** The condition needed
is `omega <= rho_n/3`, i.e.

```
L sqrt(d) h_n  <=  (1/3) sqrt(d) h_n log(en)   ⟺   log(en) >= 3L   ⟺   n >= e^{3L - 1}.
```

The dimension factor and `h_n` cancel on both sides, which is *why* the threshold does not move when
`D` is replaced by `d`: it never depended on the dimension in the first place. The source's
`n >= exp(3L)` is sufficient (it implies `log(en) = 1 + log n >= 1 + 3L >= 3L`); the sharp form is
`n >= e^{3L-1}`. I keep `n >= exp(3L)` for continuity with the source and flag the slack.

What *does* change with `d` is the other, dimension-only threshold: (H-grid) `J_n <= n` holds once
`n >= 2^{d(d+3)/3}`, where the source needs `n >= 2^{D(D+3)/3}`. For `K = 5, d = 2` that is
`n >= 2^{6.7}` instead of `n >= 2^{86.7}`. The same collapse shows in `rem:ctx-horizons`, whose
tabulated onset horizons are `10^{8.5}` at `D = 2` and `10^{31.7}` at `D = 10`: with a shared
context and `d = 2`, `K = 5`, the relevant row is `D = 2`, not `D = 10`. That is a real, large
quantitative gain and it is worth stating in the paper.

### 3.6 (d) Which part needs which rung

**Unchanged from the source, and I checked each claim rather than inheriting it.**

* **Part (ii) uses the seed clause of (A3) only.** Its proof couples nothing, takes no conditional
  expectation against an indicator, and never invokes the fallback lemma, because on `E_C ∩ H_C` no
  cube ever switches (Lemma `lem:ctx-price-meet` plus `lem:ctx-monitor-cont`(d)). So the mechanism's
  own randomisations never enter. Nothing about the context process is used.
* **Part (iii) uses the Stage-3 selection clause and the seed clause of (A3).** The Stage-3 clause is
  needed because a switch can now occur (agents may deviate arbitrarily), and
  `lem:ctx-fallback-cont` needs `E[1{I_u = j} | G^0_u] = p_{j,u}`. The source's warning applies
  verbatim in the shared-context setting: without that clause a witness makes the context path a
  function of the round's own fallback coin, the honest comparator is never selected at a cube, its
  weight never updates, and the conclusion fails by a linear amount. Nothing else about the context
  process is used.
* **Part (i) uses all of (A3) and in addition (A2)**, at exactly one place: the two coupled
  executions must have the same Stage-1 rounds at every cube and pull the same agent at each. That
  is what makes the win-inclusion and the identity of the price across the two executions true
  pathwise. The accurate requirement is that the realised context sequence is the same random object
  in the two executions; exogeneity delivers it and is formally stronger.

**(A2) is necessary for part (i), and the source's witness has to be rebuilt.** The source's witness
(`rem:ctx-continuum-exogeneity`) uses `M_2 = mu_2 = x_2`, i.e. a capability depending on agent 2's
*own* coordinate; that is not a shared-context instance as written, so I construct one.

> **Proposition SC-A2 (part (i) is false under (A3) alone).** Take `d = 1`, `K = 2`,
> `M_1 ≡ 1`, `mu_1 ≡ 0` (agent 1 strategic), `M_2(x) = mu_2(x) = x` (agent 2 honest, so
> `K_H = {2}` is nonempty). Then `mu_i <= M_i`, both are `1`-Lipschitz, so `L = 1` and (H-osc) holds
> for `n >= e^3`. Let the context process be: `x_1 = 1/2`; and for `t >= 2`, `x_t = 0` if `Y_1 = 0`
> and `x_t = 1 - h_n/2` if `Y_1 = 1`. This process is nonanticipating with respect to each round's
> own draws — `x_t` for `t >= 2` is a function of `Y_1`, realised at round 1 — so (A3) holds in the
> conditional form above; it is not exogenous. Then the deviation `S'_{1,n}` that delivers `0` at
> agent 1's first Stage-1 pull and follows `S^*_1` afterwards lies in `B^{ctx}_{1,n}` and gains
> `Theta(n)`.

*Proof.* Round 1 is the first visit to the cube containing `1/2`, so it is a Stage-1 pull of agent 1
(the round-robin starts at label 1). In the baseline `S^*_1` delivers `M_1(1/2) = 1`, so `Y_1 = 1`
surely; under the deviation it delivers `0`, so `Y_1 = 0` surely. That cube receives exactly one
visit and never awards, so it contributes at most `1` to either utility.

*Deviating execution.* All rounds `t >= 2` sit at `x = 0`, in the cube `C_lo = [0, h_n)`. Agent 2 is
honest with `mu_2 = M_2`, so feasibility and honesty force `m_{2,t} = M_2(0) = 0`; its `L_n`
Stage-1 rewards at `C_lo` are all `0` and `beta_{2,C_lo} = 0`. Agent 1 follows `S^*_1` from round 2
on, delivering `M_1 = 1`, so `beta_{1,C_lo} = 1`. Hence `beta_{(2),C_lo} = 0` and `tau_{C_lo} = 0`.
Agent 1 is the unique largest bidder, wins, and delivers `min{tau, M_1} = 0`, for per-pull utility
`1 + mu_1 - 0 = 1`. Every Stage-2 target is `0 >= tau_{C_lo}`, so on `H_{C_lo}` no switch occurs
(`lem:ctx-monitor-cont`(d)); `Pr(H^c) <= n^{-3}/K`. Utilities are nonnegative always, so
`u'_1 >= (n - 1 - 2L_n)(1 - n^{-3})`.

*Baseline execution.* All rounds `t >= 2` sit at `x = 1 - h_n/2`, in the top cube. There
`M_2 = mu_2 = 1 - h_n/2`, delivered exactly, so on the bid event `E`,
`beta_{2} >= 1 - h_n/2 - s_n`. Agent 1 bids `1`, so it is a largest bidder and
`beta_{(2)} = beta_2` unless `beta_2 = 1`, in which case `beta_{(2)} = 1` as well; either way
`beta_{(2)} >= 1 - h_n/2 - s_n` and `tau >= 1 - h_n/2 - 4 s_n - rho_n`. If agent 1 wins it delivers
`tau`, earning `1 - tau <= h_n/2 + 4 s_n + rho_n =: eps_n` per pull; if it loses, agent 2 (honest)
delivers `mu_2 = 1 - h_n/2 >= tau`, so on `H` no switch occurs and agent 1 earns `0` post Stage 1.
Hence `u^*_1 <= L_n + n eps_n + 2n(Pr(E^c) + Pr(H^c))`.

At `d = 1`: `h_n ≍ n^{-1/4}`, `L_n ≍ n^{1/2}`, `s_n ≍ n^{-1/4} sqrt(log n)`,
`rho_n ≍ n^{-1/4} log n`, so `eps_n = O(n^{-1/4} log n)` and `n eps_n = O(n^{3/4} log n) = o(n)`.
The gain is `n(1 - o(1)) = Theta(n)`. ∎

The source's further remark also carries over unchanged: the natural weakening — contexts exogenous
until every cube has completed Stage 1, reactive afterwards — preserves the win-inclusion but
destroys the accounting, because `n_C` then differs between the two executions and
`U'^post` is compared with `n_C w_C` at two different pull counts, a difference of order `n`. That
is not a measurability statement and no refinement of a filtration repairs it.

### 3.7 (e) — see §2. The statement I sign is Proposition SC plus Corollary SC-rate.

I also sign the following, which is the same proof with no extra work and which subsumes both the
source and the shared-context case:

> **Remark (the real hypothesis is a Lipschitz sufficient context).** Suppose the platform observes
> at each round a variable `z_t in [0,1)^{D'}` such that every `M_i` and every `mu_i` is an
> `L`-Lipschitz function of `z_t` alone. Run SC-MESP on `[0,1)^{D'}` with `d` replaced by `D'`
> throughout. Proposition SC and Corollary SC-rate hold verbatim with `D'` in place of `d`, exponent
> `(D'+2)/(D'+3)`. The source is the case `z_t = X_t`, `D' = Kd`; the shared-context case is
> `z_t = x_t`, `D' = d`; a mixture in which `K_1` agents share one `d`-dimensional context and the
> rest have private ones is `D' = d + (K - K_1) d`. *Proof:* no step above uses that `M_i` depends
> on `x_i` only — that fact is used only inside the source's `lem:ctx-osc` to get `sqrt(d)` out of
> `sqrt(D)`, and here Lemma SC-osc gets `sqrt(D')` directly from Lipschitzness in `z`. Every other
> lemma refers to `M_j` and `mu_j` evaluated at the round's observed context and nowhere to the
> block structure.

**The point of the result.** `app:ctx-private-net` establishes that the per-agent exponent
`(d+2)/(d+3)` is attainable for every `K` under the same hypotheses, but only by running EXP4 over a
net with `exp(Theta(n^{d/(d+2)}))` elements — explicitly "not an algorithm". Proposition SC says
that **when the context is common, the per-agent exponent is attained by a polynomial-time
mechanism**, `O(K + d)` per round. The computational barrier the paper isolates is a barrier of
*profile dimension*, not of agent count: it disappears exactly when one cube of the observed space
resolves all `K` capabilities at once.

### 3.8 Tightness of the leading term, for this mechanism

> **Proposition SC-tight (the elicitation term is attained).** Fix `d >= 1` and `K = 2`. Take the
> shared-context instance `M_1 ≡ 1`, `mu_1 ≡ 0` (agent 1 strategic) and `M_2 ≡ mu_2 ≡ 1/2` (agent 2
> honest). Then `L = 0`, so (H-osc) holds at every `n >= 1`. Let the context sequence be any
> deterministic sequence visiting each of the `J_n` cubes at least `2 L_n` times, which is possible
> whenever `2 J_n L_n <= n`, i.e. for `n >= 2^{(d+2)(d+3)}`; being deterministic it satisfies (A2).
> Assume in addition `s_n < 1/8` and (H-grid). Then the deviation `S'_{1,n}` that delivers `3/4` at
> every Stage-1 pull and follows `S^*_1` afterwards lies in `B^{ctx}_{1,n}` and
> ```
> u_1(n; S'_{1,n}, S^*_{2,n}) - u_1(n; S^*_n) >= (1/4) J_n L_n - 4 n^{-3}
>                                            >= (1/4) n^{(d+2)/(d+3)} - 4 n^{-3}.
> ```

*Proof.* The deviation is measurable with respect to the phase message, hence in the class; `3/4` is
feasible (`M_1 = 1`) and agent 1 is strategic, so honesty does not bind. Couple the two executions
by the same context sequence, seeds, priorities, coins.

Agent 2 is honest with `mu_2 = M_2 = 1/2`, so feasibility and honesty force `m_{2,t} = 1/2` at every
selection in both executions; hence `bar A_{2,C} = 1/2` and `beta_{2,C}` is the same random variable
in both. Also `bar A'_{1,C} = 3/4` and `bar A^*_{1,C} = 1`. Apply Lemma `lem:ctx-bidconc` (seed
clause only) to each agent, each cube and each execution: on an event `E^both` with
`Pr((E^both)^c) <= 2 · 2 K J_n e^{-ell_n} <= 2 n^{-4}`,
`beta_{2,C} <= 1/2 + s_n`, `beta'_{1,C} >= 3/4 - s_n`, `beta^*_{1,C} >= 1 - s_n` at every cube. With
`s_n < 1/8`, `3/4 - s_n > 5/8 > 1/2 + s_n`, so agent 1 is the **strict** largest bidder at every
cube in both executions, `beta_{(2),C} = beta_{2,C}` in both, and both announce the same number
`tau_C = (beta_{2,C} - sigma_n)_+ <= 1/2 + s_n < 1 = M_1`.

After Stage 1 at `C`, both executions have winner 1, price `tau_C`, and both agents play `S^*`;
agent 1 delivers `min{tau_C, M_1} = tau_C`, agent 2 delivers `1/2`. The Stage-1 schedule is
reward-independent and the path is deterministic, so the visit rounds of `C` are the same in both;
an induction on the visits to `C` — same local state, same phase, same selection, same target, same
seed at the same round, hence same reward — shows the two post-Stage-1 local executions coincide
pathwise. So the post-Stage-1 utilities at `C` are equal.

The only difference is Stage 1. Per Stage-1 pull, agent 1's utility is `1 + mu_1 - m = 1 - m`, equal
to `0` in the baseline and `1/4` under the deviation. Each cube completes Stage 1 and gives agent 1
exactly `L_n` Stage-1 pulls, so the saving is `(1/4) L_n` per cube and `(1/4) J_n L_n` in total. Off
`E^both` the two utilities differ by at most `2n`, contributing at most `2n · 2n^{-4} = 4 n^{-3}`.
Finally `J_n L_n >= n^{d/(d+3)} · n^{2/(d+3)} = n^{(d+2)/(d+3)}`. ∎

This shows the leading term `e_bid` of part (i) is attained by SC-MESP up to the constant, so the
exponent `(d+2)/(d+3)` is not an artefact of the analysis **of this mechanism**. It says nothing
about other mechanisms; see §8.

---

## 4. Hostile pass 1 — the diagonal is a null set

**The objection.** Under the general model the shared-context law is carried by
`Delta = {(x,...,x)} ⊂ [0,1]^{Kd}`, a Lebesgue-null set. If any step of the source proof used full
support, a density, absolute continuity, or a product structure across agents, the shared-context
claim would not be a corollary and every such step would need re-proof.

**What I checked, and how.** I read `app:ctx-private-continuum` line by line and additionally ran
`grep -nEi 'densit|support|absolutely continuous|product measure|i\.i\.d|positive mass|full
support|Lebesgue'` and `grep -n '\\nu'` over `sections/app_contextual_private.tex`. Findings:

* **The context law `nu` does not appear in the continuum subsection at all.** Every hit of `\nu` in
  that subsection is `nu_i(C) := max_{j != i} M_j^inf(C)`, the comparator floor of
  `lem:ctx-price-dom` and `lem:ctx-dev-fallback` — an unfortunate notation collision with the
  context law `nu` of `sec4_contextual.tex`, but a different object. (Flagged in §7, item 12.)
* The three `i.i.d.` hits are at lines 154, 326 and 603, **all in the finite-profile subsection**:
  line 154 puts the seeds i.i.d. uniform in the finite-case probability space; line 326 is
  `lem:ctx-bid`(b), "an average of `L_n` i.i.d. Bernoulli(`M_j^z`) variables"; line 603 is
  `rem:ctx-finite-no-two-top` saying i.i.d. arrivals are *not* needed. The continuum subsection
  replaces both of the first two: the i.i.d. seed family becomes the conditional seed clause of
  (A3), and `lem:ctx-bid`(b) becomes `lem:ctx-bidconc`, a predictable-`phi_s` exponential
  supermartingale bound that uses no independence and no identical distribution whatsoever. So the
  continuum subsection contains **no** i.i.d. hypothesis, in any form.
* No hit for density, absolute continuity, positive mass, full support or Lebesgue measure anywhere
  in the file.
* Positive cube mass, boundary conditions and two-top conditions are used by
  `thm:grid-ucb-robust`, `thm:contextual-public` and `thm:finite-context` — the *public* results and
  the finite-context result. None of them is invoked by `prop:ctx-continuum-exact`, and none is
  invoked by Proposition SC.
* The two union bounds that could have needed the support run over "the deterministic set of `J_n`
  grid cubes" (the source says so explicitly, twice, adding "so no measurability of the set of
  visited cubes is needed either"). The only place the realised support enters at all is through
  `E[J'_n] <= min{J_n, n}`, and that is an upper bound used in the *favourable* direction, via
  Jensen on concave functions of `J'_n`.

**Verdict on this objection: it has no purchase.** The private continuum argument is measure-free in
the context variable: it is a pathwise, per-cube, martingale-in-global-time argument, and the
proposition's own closing sentence ("no mass and no property of the arrival law appears in any of
the seven error terms") is accurate. A law carried by a null set of `[0,1]^{Kd}` is therefore not a
problem *for the source proposition applied at `D = Kd`*.

**But the claim is still not a corollary**, and I want to be exact about why. What breaks under
literal inheritance is not the probability theory but the *parameters*: `prop:ctx-continuum-exact`
is stated for the mechanism whose grid is `g_n^D` cubes with `g_n = ceil(n^{1/(D+3)})`, and applying
it verbatim gives `(Kd+2)/(Kd+3)`. Improving the exponent requires either (Route A) restricting the
`D`-grid union bounds to the `g_n^d` cubes meeting `Delta` — a support-dependent, hence genuinely
new, step — or (Route B) gridding the observed space, which is what I did, and which requires
re-reading every lemma at the new resolution. I re-read them; §3.2 is the record. The only lemma
whose *content* changes is the oscillation lemma, and the change makes it sharper, not weaker.

---

## 5. Hostile pass 2 — perfect cross-agent dependence

**The objection.** With a common context, the agents' capabilities are perfectly dependent across
agents rather than independent. Does any comparison across agents hide an independence assumption?

**First, a structural answer.** In this model the capability functions `M_1,...,M_K` are *fixed,
deterministic* features of the instance. Randomness enters only through (a) the context process, (b)
the reward seeds, (c) the mechanism's priorities and fallback coins, and (d) the agents' private
coins. "The agents' capabilities are perfectly dependent" is therefore not a statement about a joint
law that any step could have assumed factorised; it is the statement that the deterministic vector
`(M_1(x),...,M_K(x))` is indexed by one argument instead of `K`. No proof step can be sensitive to
it unless it compares agents *through the context*, so those are the steps I checked.

**Second, the step-by-step check.** The candidate flags `beta_{(2),C}`, the price lemmas and bid
domination. All three:

* **The second order statistic `beta_{(2),C}`.** Every use is a *deterministic* manipulation of the
  realised bid vector:
  `beta_{(2),C} <= beta_{W,C}` (`W` is a largest bidder — definitional);
  `beta_{(2),C} <= beta_{j*,C}` for some `j* != i` (`lem:ctx-price-dom`: if `i` is a largest bidder
  the second statistic *is* `max_{j != i} beta_j`, and if not then `W != i` and
  `beta_{(2)} <= beta_W <= beta_{j*}`);
  `beta_{(2),C} >= beta_{h_C,C}` when `W_C != h_C` (definitional);
  `beta_{(2),C} >= M_(2)(x) - omega - s_n` under `S^*` (monotonicity of the second order statistic
  in each argument, applied to `K` per-agent inequalities). **None of these is a distributional
  statement.** The only probabilistic input is the event `E_C`, which is the intersection over
  `j in [K]` of per-agent concentration and is obtained by a **union bound**, `Pr(E_C^c) <= 2K
  e^{-ell_n}`. A union bound is valid under arbitrary dependence; it is in fact the *only* tool that
  would be valid here, and the source uses no other.
* **The price lemmas** (`lem:ctx-price-meet`, `lem:ctx-price-dom`, `lem:ctx-price-second`,
  `lem:ctx-honest-floor`(i),(ii)) contain nothing probabilistic at all — the source says so and I
  verified it. They are chains of: `E_C`, feasibility `bar A <= bar M`, Lemma SC-osc, monotonicity
  of `(·)_+` and of order statistics. Under perfect dependence each link is unchanged.
* **Bid domination.** `beta'_{i,C} <= beta^*_{i,C}` is pathwise, from `m'_{i,t} <= M_i(x_t)` and a
  shared seed. The bids of `j != i` are *identical random variables* in the two executions, not
  independent ones — the source's phrasing "the same random variable in both executions" is exactly
  the right one and needs no independence. The win-inclusion is then a chain of inequalities between
  realised numbers.
* **Concentration of a single agent's bid.** `lem:ctx-bidconc` bounds
  `|beta_{j,C} - bar A_{j,C}|` by an exponential supermartingale in *global* time with a
  `G^0_s`-measurable indicator. It does not require that agent `j`'s `L_n` Stage-1 rewards at `C` be
  independent, identically distributed, or drawn at equal means; it requires only the seed clause at
  each of those rounds. This matters here, because under a common context agent `j`'s `L_n` bidding
  rounds at `C` occur at visits `j, K+j, 2K+j, ...` of the cube and therefore at `L_n` *different*
  contexts, so the means genuinely differ across those rounds. The source's design already
  anticipates this: `beta_{j,C}` is compared with `bar A_{j,C}`, the average of the targets actually
  delivered, and never with a single capability value.
* **The fallback.** The comparator floor `v = nu_i(C) = max_{j != i} M_j^inf(C)` (deterrence) or
  `v = v_C = max_{h in K_H} mu_h^inf(C)` (robustness) is a deterministic number; the requirement is
  the *conditional* statement "`E[Y_u | G^0_u, I_u = j*] >= v` at every fallback round at `C`",
  which holds pathwise by `S^*` or by honesty. No independence across agents, and in particular the
  lemma explicitly allows the filtration to carry every agent's cross-cube history.

**Third, an attack built specifically on the shared context, and why it fails.** Here is the
sharpest thing perfect dependence buys an adversary. Because all agents face the same `x`, the
round-robin Stage-1 schedule assigns agent `j` the visits `≡ j (mod K)` of each cube, so an
adversarial context path can systematically give different agents *different* sub-populations of
contexts within the same cube. Take `d = 1`, `K = 2`, a cube `C = [a, a+h_n)`, `M_1` decreasing and
`M_2` increasing on `C`, and a path that alternates `x` between `a` and `a + h_n - `. Then agent 1
always bids at the left end (where it is strongest) and agent 2 always at the right end (where it is
strongest), so `bar M_{1,C} = M_1(a)` and `bar M_{2,C} = M_2(a + h_n -)`, both maximal. Suppose
agent 1 wins; it must then meet `tau_C` also at the right end, where `M_1` is *smallest*. Does the
price exceed its capability there?

No, and by exactly the margin the design pays for:
```
tau_C <= beta_{(2),C} - sigma_n <= beta_{W,C} - sigma_n <= bar A_{W,C} + s_n - sigma_n
      <= bar M_{W,C} + s_n - sigma_n <= M_W(x) + omega + s_n - 3 s_n - rho_n
      <= M_W(x) - 2 s_n - (2/3) rho_n
```
for **every** `x in C`, because `bar M_{W,C}` is an average of `M_W` over contexts of `C` and hence
within `omega <= rho_n/3` of `M_W(x)` at any `x in C`. The systematic within-cube bias that the
attack manufactures is bounded by the within-cube oscillation, which is precisely what `rho_n` is
there for, and `rho_n` is paid twice over. The attack fails, and — this is the point — it fails for
the same reason and with the same arithmetic as in the general model, where agent `j`'s bidding
rounds also see `L_n` different profiles. **The shared context does not create a new margin; it
recycles the one already purchased.**

**Fourth, the "informational" version of the objection.** With a common context an agent can
predict every rival's capability exactly from what it observes. Does that give it power the analysis
did not budget? No, for a reason that is already in the source's design: part (i) is proved against
`B^{ctx+}_{i,n}`, the class in which the deviator may condition on the *entire* context sequence,
hence on all future arrivals, on every visit count and on the exact global round index, in addition
to its own full history and every message. An agent granted that much cannot be helped by also being
able to infer `M_j(x)`. Every bound in §3 is uniform over that class and over the arrival path. So
perfect cross-agent dependence grants the deviator nothing new.

**Verdict on this objection: no hidden independence assumption exists, and the specific attack the
shared context enables is already priced.**

---

## 6. Hostile pass 3 — explicit counterexample attempts

I tried to build instances that break Proposition SC. Reported honestly, including the failures.

1. **Diagonal-support break of the union bounds.** *Attempt:* exploit that `J_n = g_n^d` counts
   cubes of the observed space while the "true" profile space has `g_n^{Kd}`. *Outcome: fails, and
   correctly so.* Route B never mentions the profile space; the union bounds run over the `g_n^d`
   cubes of `[0,1)^d`, a deterministic set fixed before play. The `J_n <= n` proviso becomes
   `n >= 2^{d(d+3)/3}`.
2. **Period-`K` within-cube oscillation attack.** Described in §5. *Outcome: fails*, absorbed by
   `rho_n >= 3 omega`.
3. **Adversarial path that starves a cube.** *Attempt:* under (A3) let the path give a cube exactly
   `K L_n - 1` visits, so it never awards, and repeat. *Outcome: fails* — such a cube contributes
   only its own Stage-1 charge, which is what `e_bid` and `e_stage1` already count, and (ii)/(iii)
   charge those rounds at benchmark `<= 1` each. The charge is `min{K J'_n L_n, n} <= n`, never
   worse than trivial.
4. **Price-inflation attack: bid high to push `tau_C` above the winner's capability and provoke a
   fallback in which the deviator is selected.** *Outcome: fails.* If the deviator `i` loses, then
   `beta_{(2),C} <= beta_{W,C}` with `W != i` playing `S^*`, so `lem:ctx-price-meet` gives
   `tau_C <= M_W(x)` at every context of `C` and no switch occurs on `H_C`. If `i` wins, then
   `lem:ctx-price-dom` gives `tau_C <= nu_i(C)`, so the fallback is worth at most
   `1 + mu_i^sup(C) - nu_i(C)` per round, which is at most `w_C + rho_n/3`, the baseline rate plus
   the oscillation charge already in `e_osc`. Triggering the fallback gains nothing of order `n_C`.
   Nothing about the shared context changes this.
5. **Exploiting that all agents' capabilities move together to make `M_(2)` and `M_*` collapse.**
   *Attempt:* `M_1 ≡ M_2 ≡ ... ≡ M_K`. *Outcome: not a counterexample*, and in fact favourable:
   `M_(2) = M_*`, so (ii)'s benchmark becomes full capacity. The source's third reading comment
   applies: the two-top condition is absorbed into the benchmark.
6. **Reactive path (A3-only) against part (i).** *Outcome: succeeds — as it must.* This is
   Proposition SC-A2 of §3.6, a `Theta(n)` gain, so (A2) is necessary for part (i) in the
   shared-context setting too. It is a counterexample to the claim *without* (A2), not to
   Proposition SC.
7. **Reactive path (A3-only) against parts (ii)/(iii).** *Attempt:* let the path chase whichever
   cube the mechanism is currently pricing badly. *Outcome: fails to break anything.* Parts (ii) and
   (iii) are proved pathwise per cube with union bounds over the deterministic grid; the conclusion
   is a comparison against the benchmark *evaluated on the realised path*. It remains true. What is
   lost is interpretive, not logical, and the source's `rem:ctx-endogenous` states it exactly: the
   benchmarks `E sum_t M_(2)(x_t)` and `E sum_t b(x_t)` are endogenous, so the sentence proved is
   "on the realised path, whatever it was, the mechanism collects within the stated error", not "the
   mechanism attains the second capability". That remark carries over verbatim and should be carried
   over in the paper.
8. **Vanishing capability gaps.** *Attempt:* let `M_i - V_i` shrink with `n` and hope the instance
   quantity `Gamma_i` of the finite-profile theorem reappears. *Outcome: fails, favourably.* By
   `lem:ctx-price-meet` the price is below the *realised* winner's capability at every context on
   `E_C`, so there is no non-top branch, no capability gap and no threshold of the form
   `4 s_n <= delta_i`. Proposition SC carries no instance quantity other than (H-osc). This is
   inherited, not new, but I verified it survives the substitution.
9. **`L` large.** *Attempt:* take `L ≍ log n` so (H-osc) barely holds. *Outcome: not a
   counterexample but a genuine limitation.* `L` never enters a bound, only (H-osc); the guarantee
   is simply vacuous until `n >= e^{3L-1}`. Same as the source.
10. **Attack the elicitation term.** *Outcome: succeeds in the intended sense* — Proposition
    SC-tight of §3.8 shows `e_bid` is attained by SC-MESP up to a constant, so the exponent is not
    improvable *for this mechanism* by a better analysis.

---

## 7. Disagreements with the candidate

The candidate is, in my judgement, **correct** — neither too strong nor too weak in its headline
claims. Every disagreement below is either a sharpening, a precision, or a claim the candidate did
not make and should.

1. **"Corollary" status (implicit).** The candidate presents the conclusion as
   `prop:ctx-continuum-exact` "with `d` replacing `D` throughout". That is an accurate *summary of
   the statement*, but it is **not a corollary of the proposition**: applying the proposition
   verbatim at `D = Kd` gives `(Kd+2)/(Kd+3)`. The result is a re-instantiation of the mechanism at
   a different resolution, and every lemma must be re-read (§3.2). I would not let the paper say
   "corollary".
2. **Part (i)'s constant is `K`-free.** The candidate asserts `O_{d,K}(n^{(d+2)/(d+3)} log(eKn))`
   for all three parts. True, but weaker than provable: part (i) is
   `O_d(n^{(d+2)/(d+3)} log(en))` for `n >= n_2(K,d)`, with leading constant
   `2^{d+1} + sqrt(d) log(en)`, since `e_bid` and `e_osc` carry no `K` at all and the `K`-carrying
   terms `e_mon`, `e_fb` sit at exponents `(2d+3)/(2d+6)` and `d/(d+3)`. Parts (ii) and (iii) are
   exactly linear in `K`, through `e_stage1` alone. I would state the three separately.
3. **`n >= exp(3L)`.** Agreed and unchanged, but the sharp form is `log(en) >= 3L`, i.e.
   `n >= e^{3L-1}`. More importantly I would add the *reason* it does not move: the dimension factor
   cancels on both sides of `omega <= rho_n/3`, so the threshold never depended on the dimension.
   The candidate asserts it is unchanged without saying why, and "unchanged" is exactly the kind of
   claim that needs the reason attached.
4. **`sqrt(d)` versus `sqrt(D)` — and a slack I found in the source.** I agree with `sqrt(d)`. I add
   that **the source's `rho_n := sqrt(D) h_n log(en)` is already slack by a factor `sqrt(K)` in the
   general model**: the proof of `lem:ctx-osc` itself establishes oscillation `<= L sqrt(d) h_n`
   (its own words: "any single agent's `d` coordinates differ by at most `sqrt(d) h_n <= sqrt(D)
   h_n`") and then throws the `sqrt(d)` away. Since all six uses of `rho_n` go through
   `omega <= rho_n/3`, the general-model `rho_n` may be reduced to `sqrt(d) h_n log(en)`, improving
   `e_osc` and the `rho_n` part of `e_price` by `sqrt(K)`. This is a conservative slack, so
   `prop:ctx-continuum-exact` remains true as stated; it is an improvement, not an erratum. I flag
   it because the shared-context statement should not inherit the slack, and because the paper may
   want it in the general theorem too.
5. **The `J_n <= n` threshold.** The candidate says "hypotheses unchanged". Strictly, the proviso
   hidden inside `lem:ctx-bidconc` ("for every `n` beyond a threshold depending only on `D`")
   becomes a threshold depending only on `d`: `n >= 2^{d(d+3)/3}` instead of `n >= 2^{Kd(Kd+3)/3}`.
   This is a change, and a large one: it is the same collapse that turns the `D = 10` row of
   `rem:ctx-horizons` (`10^{31.7}`) into the `D = 2` row (`10^{8.5}`) for `K = 5`, `d = 2`. The
   paper should claim this gain rather than describe the hypotheses as unchanged.
6. **Wording of the mechanism.** "run one independent local CG-MESP copy per cube" is
   self-referential: CG-MESP *is* the gridded mechanism. The correct description is "CG-MESP with
   the grid taken on the observed common space `[0,1)^d`", equivalently "one independent local MESP
   copy per cube of `[0,1)^d`".
7. **The candidate does not pin `h_n`.** It says "side `h_n`" and gives the exponent. `h_n` must be
   `1/ceil(n^{1/(d+3)})` and `L_n = ceil(n^{2/(d+3)})`; the balance (§3.3) is what forces both, and
   `L_n` must be `ceil`ed from above and `h_n` from a `ceil`ed `g_n` for the displayed constants
   `2^{d+1}` etc. to be correct.
8. **A `K`-tuned variant the candidate does not mention.** The mechanism as specified does not tune
   `L_n` to `K`, so `e_stage1` is linear in `K`. Minimising
   `max{ K L h^{-d}, n sqrt(ell_n/(2L)), sqrt(d) n h log(en) }` over `(h, L)` gives
   `L = (n A^{d+1} B^{-d} / K)^{2/(d+3)}` with `A = sqrt(ell_n/2)`, `B = sqrt(d) log(en)`, and
   optimal value `K^{1/(d+3)} A^{2/(d+3)} B^{d/(d+3)} n^{(d+2)/(d+3)}`. So the `K` in the leading
   constant of (ii)/(iii) can be improved from `K` to `K^{1/(d+3)}`, with no change of exponent.
   This mirrors `rem:ctx-finite-no-two-top`'s `bar Q`-tuned variant and would be worth a remark.
9. **The candidate does not state that (A2) is necessary here.** It says the hypotheses are
   unchanged, which is right, but the source's necessity witness is not a shared-context instance
   (it uses `M_2 = mu_2 = x_2`). I rebuilt it (Proposition SC-A2) and it works. The paper must not
   cite `rem:ctx-continuum-exogeneity`'s witness for the shared-context statement without this
   rebuild.
10. **The candidate does not state the endogenous-benchmark caveat.** `rem:ctx-endogenous` carries
    over verbatim and should be carried over: under (A3) the benchmarks in (ii)/(iii) are evaluated
    along a path the mechanism helped determine.
11. **The candidate does not state the result's actual significance.** "Mechanism polynomial time"
    is true but understated. The right sentence is: `app:ctx-private-net` shows the per-agent
    exponent `(d+2)/(d+3)` for general `K` requires an expert set of size `exp(Theta(n^{d/(d+2)}))`
    and is explicitly not an algorithm; with a common context the same exponent is attained by a
    mechanism costing `O(K + d)` per round. The computational barrier is one of *profile dimension*,
    not of agent count.
12. **A notation collision to fix before this reaches the paper.** `nu` is the context law in
    `sec4_contextual.tex` and `nu_i(C) := max_{j != i} M_j^inf(C)` is the comparator floor in
    `app:ctx-private-continuum`. A reader chasing the null-set objection will read `nu_i(C)` as a
    measure. Rename one of them.
13. **A minor inconsistency I noticed while reading, not caused by the candidate.**
    `sec2_model.tex` and `sec4_contextual.tex` set `X = [0,1]^D` (closed), while
    `app:ctx-private-continuum` sets `mu_i, M_i : [0,1)^D -> [0,1]` and tiles `[0,1)^D` with
    half-open cubes. The half-open version is the one that tiles exactly; the closed version does
    not, or double-counts faces. The shared-context statement should say `[0,1)^d` and the body
    should be reconciled.

---

## 8. Inherited versus new

Stated as honestly as I can.

**Inherited (re-labelling), roughly 85–90% of the mathematical content.** Every lemma of
`app:ctx-private-continuum` except the oscillation lemma transfers with the substitution "cube of
`[0,1)^d` containing `x_t`" for "cube of `[0,1)^D` containing `X_t`" and no change to any
inequality: bid concentration, the three price lemmas, the honest floor, the cube monitor, the
fallback with unknown local horizon, the deviator's fallback utility, cube locality, the bid
domination coupling, the legitimacy-of-conditioning argument, the two Cauchy–Schwarz/Jensen steps,
and the three main proofs. §3.2 is the per-lemma record; I re-read each rather than assuming, and
§3 reproduces the three main proofs at the level where a substitution could have gone wrong. The
mechanism itself is CG-MESP with a different grid, so nothing in the construction is new.

**New, and genuinely so, though small.**
1. *Lemma SC-osc.* The only lemma with changed content: `omega = L sqrt(d) h_n` from Lipschitzness
   in the single common context, plus the observation that the same bound covers `M_*`, `M_(2)` and
   `b` by 1-Lipschitzness of order statistics. Two lines, but it is the load-bearing line, since all
   six uses of `rho_n` funnel through it.
2. *The verification that the diagonal's null-set status is irrelevant* (§4). This is not a
   re-labelling: it is a claim about the source's proof that had to be checked, lemma by lemma and
   by grep, and it could have come out the other way. It came out clean because the private
   continuum argument is measure-free in the context variable.
3. *The verification that no comparison across agents hides an independence clause* (§5), and the
   identification of the one attack the shared context specifically enables (the period-`K`
   within-cube sampling bias) together with the proof that `rho_n` already pays for it.
4. *The re-solved balance* (§3.3). The arithmetic is structurally identical to the source's but it
   is a different optimisation (the `K` moves from the exponent to a constant) and it must be shown.
5. *Proposition SC-A2*, the (A2)-necessity witness, rebuilt inside the shared-context class because
   the source's witness is not one.
6. *Proposition SC-tight*, the shared-context analogue of `prop:ctx-finite-tight`, which the source
   states only for the finite-profile mechanism. It is a genuine new (if easy) proof.
7. *The abstract "Lipschitz sufficient context" remark* (§3.7), which subsumes both the source and
   the shared case and is, I think, the right way to state the general theorem.
8. *The identification of the slack `sqrt(D) -> sqrt(d)` in the source's `rho_n`* (§7, item 4).

**Where the value of the result lies.** Not in the proof, which is largely inherited, but in the
statement: it converts the paper's own separation (`thm:ctx-net-separation`: per-agent exponent for
general `K`, but only via a non-algorithm) into a *theorem about a polynomial-time mechanism* in the
case where the contexts are shared, and it collapses the numerically catastrophic onset horizons of
`rem:ctx-horizons` from `exp(c K d)` to `exp(c d)`. Both of those are statements about the paper's
architecture, and both are new.

---

## 9. Open or doubtful

1. **No lower bound over mechanisms.** Proposition SC-tight shows `e_bid` is attained *by SC-MESP*.
   I have **no** argument that `(d+2)/(d+3)` is optimal for any mechanism in the shared-context
   setting, and I do not claim it. The source is equally careful about the finite case
   ("It says nothing about whether a different mechanism could avoid paying `L_n` per profile"), and
   there the argument that it cannot is an instance argument ("the primitives at different profiles
   are unrelated") which is *weaker* here, because with a common context and Lipschitz primitives
   the cubes are **not** unrelated: `M_j` at one cube constrains `M_j` at a neighbouring cube to
   within `L h_n`. So a mechanism that pooled elicitation across neighbouring cubes is not obviously
   ruled out. I consider the optimality of the exponent genuinely open, and I would not let the
   paper insinuate otherwise.
2. **Is the linear `K` in (ii)/(iii) necessary?** Every agent must be elicited in every cube that
   awards, which costs `K L_n` per cube by construction. Whether some mechanism can price with
   `o(K)` elicitations per cube — e.g. by eliciting a random subset — I do not know. The `K`-tuned
   variant (§7, item 8) reduces the constant to `K^{1/(d+3)}` but does not remove the question.
3. **Uniformity in `K`.** Corollary SC-rate is asymptotic in `n` with `K, d` fixed; the thresholds
   `sqrt(K log K) <= n^{1/(2d+6)}` and `K log K log n <= n^{2/(d+3)}` are collected into
   `n_2(K, d)` and are not made explicit. I did not attempt a statement uniform over `K` growing
   with `n`, and I would not sign one without redoing §3.4 carefully.
4. **The mixed case.** §3.7's remark asserts the exponent `(D'+2)/(D'+3)` whenever the platform
   observes a `D'`-dimensional variable on which all primitives are `L`-Lipschitz. I believe this
   and I gave the reason (no step uses the block structure), but I checked it by re-reading rather
   than by writing the proof out again at full length as I did for the shared case. I would call it
   *high confidence, not fully written*.
5. **The `log(en)` factor.** The oscillation term carries `log(en)` because `rho_n` does, and
   `rho_n` carries it only so that `omega <= rho_n/3` holds without knowing `L`. If `L` were known,
   `rho_n = 3 L sqrt(d) h_n` removes the `log(en)` from `e_osc` and from part of `e_price`, and the
   balance shifts by logarithmic factors only. I have not worked out whether an adaptive estimate of
   `L` could do this without `L`; the source does not attempt it either.
6. **Numerical onset.** `rem:ctx-horizons` should be recomputed for the shared-context parameters
   before any number is quoted. My §3.5 claim is only that the relevant row moves from `D = Kd` to
   `d`, which follows from the parameter substitution; I did not redo the bisection.
7. **A presentational risk, not a mathematical one.** Because SC-MESP is CG-MESP on a different
   grid, there will be a temptation to state the shared-context result as a corollary and give no
   proof. §4 explains why that is wrong (the exponent does not follow from the proposition), and
   §3.2 is the minimum that has to be recorded. If the paper prints it as a corollary I would not
   sign it.
