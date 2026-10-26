# PROVER2: candidate C1 plus C0 (known-horizon UCB, exact monotonicity, Static Grid KH-UCB as a full contextual SAMF mechanism)

Independent proof file. Written from TASK.md, CONTEXT_PROOF_CONTRACT.md, COMMON.md and the canonical manuscript sections only.

## 0. Status line

- 2026-09-17, FINAL. All nine target statements S0 to S8 are proved and classified COMPLETE; none was found to be false. Sections 1 to 6 are written. Summary of what is delivered:
  - S0: static race lemma for arbitrary extended-real index sequences with a fixed strict priority, with an exact identification of the non-raised arms' pull sequence with a deterministic reduced race (Lemma 2.1).
  - S1: scalar `KH-UCB(n,pi)` has PATHWISE monotonicity with zero remainder on the blind behavioral class, sharp adaptivity `4 sqrt(n log n) + 3`, robustness `mu_H^* n - K(4 sqrt(n log n)+3)`, exact FATA.
  - S2: finite-context version, monotonicity exact for every region, public part uniform over deviations at `4 sqrt(Qn log n) + 3Q`, no i.i.d. or positive-mass hypothesis.
  - S3 to S8: Static Grid KH-UCB is a full contextual SAMF mechanism at rate `O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})`, with exact expected monotonicity for EVERY measurable region (via the identity `E T_j(C cap R;n) = nu(R|C) E T_j(C;n)`, proved including initialization rounds, never-selected agents, random visit counts and zero-mass cells), sharp adaptivity, robustness, FATA, revenue, and a public restricted equilibrium whose deviation bound is uniform over `S_HDS` and needs only `nu(|T(X)|>=2)=1` and Lipschitz capacities.
  - Lipschitz constants are tracked as `L sqrt(d)`, `d = D/K` (lesson L2), improving the manuscript's `2 L sqrt(D)` by the factor `2 sqrt(K)`.
  - Imported bandit bound: Lattimore and Szepesvari, Theorem 7.1 and the display `E[T_i(n)] <= 3 + 16 log(n)/Delta_i^2` inside its proof, verified against the primary source in this session (Section 6), including that it is valid for arbitrary tie-breaking and in the reward-stack model.
  - Every step that needs the known-horizon index is flagged `[KH]` and listed in Section 5.2; the anytime index is shown NOT to be pathwise monotone by an explicit `K=3`, `n=8` tape found and verified in this session (Section 5.3), and per-round fresh tie coins are shown to break the pathwise conclusion too (Section 5.4).
  - Not claimed: expected monotonicity under fresh tie coins (OPEN), pathwise monotonicity for the grid (not claimed, and the reason is stated), any optimality in `D`.

## Conventions used throughout this file

Natural logarithms; `(x)_+ = max(x,0)`; `[K] = {1,...,K}`; `1{.}` is an indicator. `K >= 2` and the horizon `n >= 2` are fixed (for `n = 1` every statement below is trivial because every remainder listed is at least 1 and every deficit is at most 1). Expectations are over all reward seeds, all ex ante priorities, all agent private coins and, in the contextual sections, the context sequence. No martingale, filtration or nesting argument is used anywhere in this file; every conditioning is on a discrete random element with finitely many values (a context sequence, a cell membership sequence, a realized ex ante map) and every such conditioning is an elementary conditioning on an event of positive probability.

### Algorithms (restated verbatim from TASK.md, with the conventions made explicit)

`KH-UCB(n, pi)` on arm set `[K]`. A permutation `pi` of `[K]` is drawn once before play (uniformly, unless stated otherwise) and is the instance's single tie-breaking priority: `a` has higher priority than `a'` iff `pi^{-1}(a) < pi^{-1}(a')`. At round `t`, let `T_a` be `a`'s current pull count and `hat m_a` its current empirical mean of observed rewards. Define the index

  `Ind_a := +infinity` if `T_a = 0`, and `Ind_a := hat m_a + sqrt(4 log(n) / T_a)` otherwise.

The rule pulls the highest-priority element of `argmax_a Ind_a`. Because `Ind_a = +infinity` exactly when `T_a = 0`, this single sentence covers both the initialization phase (the first `K` rounds pull `pi(1), ..., pi(K)` in that order) and all later rounds; there is exactly one priority per instance and it is used at initialization and at every later tie. With `delta := 1/n^2` we have `sqrt(2 log(1/delta)/T_a) = sqrt(4 log(n)/T_a)`, so this is exactly `UCB(delta)` of Lattimore and Szepesvari (Algorithm 3) with `delta = 1/n^2` and a particular tie-breaking rule.

`Finite-Context KH-UCB`: one independent `KH-UCB(n, pi_z)` instance per exact profile `z in X_F`, with the global `n` inside the logarithm and an independent uniform priority `pi_z` per profile; no statistics are shared across profiles.

`Static Grid KH-UCB`: let `h_n := (log(en)/n)^{1/(D+2)} in (0,1]`, `N_n := ceil(1/h_n)`, and let

  `kappa(x) := ( min( floor(x_1/h_n), N_n - 1 ), ..., min( floor(x_D/h_n), N_n - 1 ) )`

be the cell map on `X = [0,1]^D`. The cells are the `J_n := N_n^D` nonempty sets `C_v := kappa^{-1}(v)`; each is a box whose side in every coordinate is at most `h_n`, so `diam(C) <= sqrt(D) h_n`, and they partition `[0,1]^D`. The platform runs one independent `KH-UCB(n, pi_C)` instance per cell, with the GLOBAL `n` inside the logarithm and an independent uniform priority `pi_C` per cell; the exact profile `X_t` is used only to compute `kappa(X_t)` (cell-blind decisions). Cells are initialized lazily; this is only a statement about storage, and the analysis below is written as if all `J_n` instances existed, which changes nothing because a cell that is never visited contributes zero to every sum. `J_n <= (1/h_n + 1)^D <= 2^D h_n^{-D}` since `h_n <= 1`.

Since `b` and every `m_{a,n}` take values in `[0,1]`, all per-visit deficits below lie in `[-1,1]`.

## 1. Exact theorem statements ready for the paper

Throughout, `C_uni := 4` and `C_add := 3` are absolute constants inherited from the imported bandit bound (Lemma 2.2 and Corollary 2.3 below); no constant below depends on the horizon, on the strategy profile, on `nu`, or on the gaps.

### Theorem 1 (scalar known-horizon UCB is stochastic SAMF, with exact pathwise monotonicity). Target C0/S1.

Let the platform run `KH-UCB(n, pi)` with `pi` uniform on the permutations of `[K]`, and realize rewards through the own-pull-index tape coupling of Lemma 2.4: independent uniforms `U_{a,k}`, `a in [K]`, `k >= 1`, and `Y_{a,k} = 1{U_{a,k} <= m_{a,k}}` where `m_{a,k}` is the target chosen by agent `a` at its `k`-th own pull.

(1a) Pathwise monotonicity, zero remainder, every `n`. Let every agent `a` use a blind nonanticipating strategy (class `B_{a,n}` of the manuscript: when selected, `a` chooses its target as a measurable function of `n`, its own past targets and rewards, and its own private randomness, and of nothing else; in particular not of the global round, not of other agents' histories, and not of its own selection times). Fix `i in [K]`. Let profile `A` be any such profile and let profile `B` replace agent `i`'s strategy by the constant target `M_i`, all other agents, all uniforms `U_{a,k}`, all private coins and `pi` being unchanged. Then on every sample point and for every `t <= n`,

  `T_j^B(t) <= T_j^A(t)` for every `j != i`, and `T_i^B(t) >= T_i^A(t)`.

Consequently `E T_j^B(n) <= E T_j^A(n)` for every `j != i`: stochastic monotonicity holds with remainder exactly `0`, not `o(n)`, and holds on the behavioral class, not only on `S_HI`. The same conclusion holds whenever profile `B` replaces `i`'s strategy by any strategy whose realized target sequence satisfies `m^B_{i,k} >= m^A_{i,k}` for every `k` on the coupled sample point (for instance any pair of fixed means `m_i <= m_i'`, or any pair of horizon-dependent fixed means).

(1b) Sharp adaptivity. For every profile in `S_HI` (also for horizon-dependent fixed means `m_{a,n}`), every agent `i` and every `n >= 2`,

  `E C_i(n) >= (mu_H^* - mu_i) E T_i(n) - (4 sqrt(n log n) + 3)`.

(1c) Robustness. Under the same hypotheses, `P(n;S) >= mu_H^* n - K(4 sqrt(n log n) + 3)`.

(1d) Exact FATA. If `m_i = m_j` (equal fixed means, hence equal reward laws), then `E T_i(n) = E T_j(n)` exactly, for every `n`. More generally this holds whenever the pair (strategy, tape) of `i` and of `j` is exchangeable.

Hence `KH-UCB(n, pi)` is stochastic SAMF on `S_HI` with sharp-adaptivity error `4 sqrt(n log n) + 3`, monotonicity remainder `0` (pathwise, and on the larger blind behavioral class), and exact expected FATA.

### Theorem 2 (finite contexts). Target C0/S2.

Assume exogenous profile arrivals: the context sequence `(X_1,...,X_n)`, with values in the fixed finite set `X_F = {z_1,...,z_Q}`, is independent of all reward uniforms, all priorities and all agent coins. Its law is otherwise arbitrary (no i.i.d. assumption). Let the platform run Finite-Context KH-UCB, and let all agents use deterministic maps in `S_F` (or horizon-dependent maps `m_{a,n} : X_F -> [0,1]` with `m_{a,n}(z) <= M_a(z_a)`, or independent ex ante mixtures of such maps). Then for every `n >= 2`:

(2a) For every `R subseteq X_F` and every agent `i`, contextual sharp adaptivity with remainder `4 sqrt(|R| n log n) + 3 |R|`.

(2b) Contextual monotonicity with remainder exactly `0`, for every `R subseteq X_F`, every `i != j` and every `n`: raising `m_i` pointwise to `M_i` (or to any map `m_i' >= m_i` pointwise) gives `E T_j'(R;n) <= E T_j(R;n)`. Conditional on the context sequence the inequality even holds pathwise under the tape coupling.

(2c) Exact expected FATA: if `m_i(z) = m_j(z) = M_*(z)` for every `z in G_ij(R)` then `E T_i(G_ij(R);n) = E T_j(G_ij(R);n)` exactly.

(2d) Robustness: `P(n) >= E sum_{t<=n} b(X_t) - (4K sqrt(Q n log n) + 3KQ)`.

(2e) Public part. Assume in addition that `M_*(.)` is public and that `|T(z)| >= 2` for every `z in X_F` that is visited with positive probability. Then at the all-maximum profile `S^max` (agent `a` plays `M_a(z_a)` at every `z`), for every agent `i` and every deviation `m_i'` in `S_F` (or any horizon-dependent map, or any independent mixture),

  `u_i(n; m_i', S^max_{-i}) - u_i(n; S^max) <= 4 sqrt(Q n log n) + 3Q`,

uniformly over deviations, and hence `S^max` is an `S_F`-asymptotic equilibrium. For each fixed deviation with positive gaps the same quantity is `O(Q log n)` with a constant depending on the gaps. Moreover `P(n; S^max) >= E sum_{t<=n} M_*(X_t) - (4K sqrt(Q n log n) + 3KQ)`, and if every positive capacity gap `M_*(z) - M_a(z_a)` at every visited profile is bounded below by a fixed `Delta_0 > 0`, this improves to `E sum_t M_*(X_t) - KQ(3 + 16 log(n)/Delta_0)`.

### Theorem 3 (Static Grid KH-UCB is a full contextual SAMF mechanism). Target C1.

Assume `X = [0,1]^D`, `D = Kd`, contexts `X_t` i.i.d. `nu` and independent of all reward uniforms, all cell priorities and all agent coins, and let all agents use maps in `S_HDS` (measurable `m_{a,n} : X -> [0,1]` with `m_{a,n}(X) <= M_a(x_a)` pointwise, fixed before play, honest ones satisfying `m_{h,n}(X) >= mu_h(x_h)` pointwise; independent ex ante mixtures allowed). Let the platform run Static Grid KH-UCB with `h_n = (log(en)/n)^{1/(D+2)}`. Write `E_n := L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 min{J_n, n}` and note

  `E_n <= (L sqrt(d) + 4 * 2^{D/2} + 3 * 2^D) * n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`.

Then for every `n >= 2`:

(3i) Contextual sharp adaptivity, uniformly over `S_HDS`. If every `mu_a` is `L`-Lipschitz on `[0,1]^d`, then for every agent `i` and EVERY measurable `R subseteq X`,

  `E sum_{t<=n} 1{X_t in R, I_t = i} c_{i,t} >= E sum_{t<=n} 1{X_t in R, I_t = i} [ b(X_t) - mu_i(x_{i,t}) ] - r_n(R)`,
  `r_n(R) := L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 min{J_n,n} + n nu( (boundary R)^{sqrt(D) h_n} ) <= E_n + n nu( (boundary R)^{sqrt(D) h_n} )`.

If `nu(boundary R) = 0` the last term is `o(n)`, so `r_n(R) = o(n)`; with no boundary assumption the first three terms are still `O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})`.

(3ii) Global robustness, uniformly over `S_HDS`: `P(n) >= E sum_{t<=n} b(X_t) - [ L sqrt(d) n h_n + 4K sqrt(J_n n log n) + 3K min{J_n,n} ]`. This is the manuscript's Theorem `thm:grid-ucb-robust` with explicit constants and with `L sqrt(d)` in place of `2 L sqrt(D)`.

(3iii) Exact expected contextual monotonicity, zero remainder, every `n`, EVERY measurable `R`, no regularity assumption at all. Let `m`, `m'` be two map profiles that agree for all agents other than `i` and satisfy `m_{i,n}' >= m_{i,n}` `nu`-almost everywhere (in particular `m_{i,n}' = M_i`). Then for every `j != i` and every measurable `R`, `E T_j'(R;n) <= E T_j(R;n)`. In addition, for every cell `C` the count `T_j'(C;n)` is stochastically dominated by `T_j(C;n)`, and `E T_i'(R;n) >= E T_i(R;n)` for every measurable `R` (the deviating agent's own expected regional count moves the other way).

(3iv) Expected contextual FATA. Let `G := G_ij(R)` and suppose `m_{i,n}(X) = m_{j,n}(X) = M_*(X)` for every `X in G`. Then

  `| E T_i(G;n) - E T_j(G;n) | <= n nu( (boundary G)^{sqrt(D) h_n} )`,

which is `o(n)` whenever `nu(boundary G) = 0`. No Lipschitz assumption is used.

(3v) Revenue at all-maximum play. If every `M_a` is `L`-Lipschitz on `[0,1]^d`, then

  `P(n; S^max) >= E sum_{t<=n} M_*(X_t) - [ L sqrt(d) n h_n + 4K sqrt(J_n n log n) + 3K min{J_n,n} ]`.

(3vi) Public restricted equilibrium with an explicit rate. If every `M_a` is `L`-Lipschitz, `M_*(.)` is public, and `nu( { X : |T(X)| >= 2 } ) = 1`, then for every agent `i` and every deviation `m_{i,n}'` in `S_HDS` (deterministic or an independent ex ante mixture),

  `u_i(n; m_{i,n}', S^max_{-i}) - u_i(n; S^max) <= L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 min{J_n,n} = E_n = O( n^{(D+1)/(D+2)} (log n)^{1/(D+2)} )`,

uniformly over deviations. In particular `S^max` is an `S_HDS`-asymptotic equilibrium. No continuity of capacities beyond `L`-Lipschitzness, no null closed set `B`, and no finite-component top-stability assumption is used.

No claim of minimax optimality in `D` is made anywhere.

## 2. Lemmas with complete proofs

Steps that are valid only because the index uses the known horizon `n` and not the running time `t` are flagged `[KH]`. Section 5.2 collects all of them and says what fails for the manuscript's anytime index.

### Lemma 2.1 (static race). Target S0.

Setup. Let `[K]` be a finite arm set, let `p` be a fixed strict priority, that is a bijection `p : [K] -> [K]` where `p(a) < p(a')` means that `a` has strictly higher priority than `a'`. For each `a in [K]` let `f_a : {0,1,2,...} -> [-infinity, +infinity]` be an arbitrary sequence with values in the extended reals. Order the keys `(v, a)` in `([-infinity,+infinity]) x [K]` by

  `(v, a) > (v', a')` iff `v > v'`, or `v = v'` and `p(a) < p(a')`.

This is a total order and, because `p` is injective, the keys of distinct arms are always distinct, so every finite set of arms has a unique key-maximal element. The greedy race is the deterministic sequence `I_1, I_2, ...` with counts `T_a(0) := 0`, and for `t >= 1`

  `I_t := the unique key-maximal element of { (f_a(T_a(t-1)), a) : a in [K] }`, `T_a(t) := T_a(t-1) + 1{I_t = a}`.

Claim. Let `f_1' >= f_1` pointwise (in the extended reals) and `f_a' = f_a` for every `a != 1`, run the greedy race with the SAME priority `p`, and write `T'` for its counts. Then for every `t >= 0`,

  (a) `T_1'(t) >= T_1(t)`, and (b) `T_j'(t) <= T_j(t)` for every `j != 1`.

Proof.

Step 1 (the non-1 pulls form a deterministic reduced race, independent of what arm 1 does). Consider the greedy race `R_2, R_3, ...` on the reduced arm set `[K] \ {1}` with the same sequences `(f_a)_{a != 1}` and the same priority restricted to `[K] \ {1}`; let `R_a(r)` denote the count of arm `a` after `r` steps of this reduced race. We claim that in ANY run of the full race (in particular in both of our runs), for every `t` and every `a != 1`,

  `T_a(t) = R_a(N(t))` where `N(t) := t - T_1(t)` is the number of non-1 pulls up to time `t`.

Induction on `t`. It holds at `t = 0`. Suppose it holds at `t-1`. If `I_t = 1`, then no count of a non-1 arm changes and `N(t) = N(t-1)`, so the identity persists. If `I_t = j != 1`, then `j` is key-maximal among all arms, hence a fortiori key-maximal among `[K] \ {1}` for the counts `(T_a(t-1))_{a != 1} = (R_a(N(t-1)))_{a != 1}`; by definition of the reduced race, the `(N(t-1)+1)`-st pull of the reduced race is exactly this key-maximal arm, that is `j`. Since `N(t) = N(t-1) + 1`, the identity persists. This proves the claim. Note that each `R_a` is nondecreasing in its argument.

Consequently (a) implies (b): `T_1'(t) >= T_1(t)` gives `N'(t) = t - T_1'(t) <= t - T_1(t) = N(t)`, hence `T_j'(t) = R_j(N'(t)) <= R_j(N(t)) = T_j(t)` for every `j != 1`, all at once.

Step 2 (proof of (a)). Suppose (a) fails and let `t >= 1` be minimal with `T_1'(t) < T_1(t)`. Counts change by at most one per step, and by minimality `T_1'(t-1) >= T_1(t-1)`, so

  `T_1(t) > T_1'(t) >= T_1'(t-1) >= T_1(t-1) >= T_1(t) - 1`,

whence all four middle quantities equal `k := T_1(t) - 1`, `T_1(t) = k+1`, and:
  (i) the unprimed run pulls arm 1 at step `t`;
  (ii) the primed run does not pull arm 1 at step `t`;
  (iii) `T_1'(t-1) = T_1(t-1) = k`.
By minimality of `t` and Step 1, `T_a'(t-1) <= T_a(t-1)` for every `a != 1`. Both runs have made `t-1` pulls in total, and by (iii) they agree on arm 1, so `sum_{a != 1} T_a'(t-1) = (t-1) - k = sum_{a != 1} T_a(t-1)`. A family of inequalities `T_a' <= T_a` with equal sums forces equality termwise:

  `T_a'(t-1) = T_a(t-1)` for every `a in [K]`.   (*)

Let `j != 1` be the arm pulled by the primed run at step `t` (it exists by (ii)). Using that the key-maximal arm strictly beats every other arm, and that `f_1'(k) >= f_1(k)` with the same priority slot for arm 1:

  `(f_j(T_j'(t-1)), j) > (f_1'(k), 1) >= (f_1(k), 1) > (f_j(T_j(t-1)), j)`,

where the first inequality is (ii) (the primed run prefers `j` to arm 1 at step `t`, and arm 1's primed count at `t-1` is `k` by (iii)), the middle inequality is the hypothesis `f_1' >= f_1` (same second coordinate), and the last is (i) (the unprimed run prefers arm 1 to `j`). By transitivity `(f_j(T_j'(t-1)), j) > (f_j(T_j(t-1)), j)`; both keys have the same second coordinate, so `f_j(T_j'(t-1)) > f_j(T_j(t-1))`. But by (*) the two arguments are equal, so the two keys are identical, and no key is strictly greater than itself. Contradiction. Hence no such `t` exists and (a) holds. By Step 1, (b) holds. QED

Where the fixed priority is used. Twice, and both uses are essential.
1. In Step 1, the tie-breaking rule must be a function of the set of currently key-maximal arms alone (here: the priority-first one), the same function at every round and in both runs. This is what makes the reduced race a deterministic sequence that is traversed by the non-1 pulls in order, no matter how arm 1 interleaves. A tie-breaking coin drawn fresh each round destroys this: the two runs reach a given tie at different rounds and therefore consume different coins.
2. In Step 2, the chain of three strict or weak inequalities compares the two runs through a single total order on keys. This requires the second coordinate of arm 1's key to be the same in both runs, and the comparison between arm `j` and arm 1 to be resolved by the same rule in both runs.

Remark 2.1.1 (monotone envelopes are not needed). An alternative route replaces each `f_a` by its running minimum and argues that the greedy merge is unchanged and that merging nonincreasing sequences takes the pooled multiset in decreasing order. The proof above avoids this and needs no structure on `f_a` whatsoever, in particular no monotonicity, no finiteness and no tie-freeness.

Remark 2.1.2 (per-round fresh tie coins break the pathwise conclusion). Take `K = 3` with the natural coupling that both runs read the same sequence of tie-breaking permutations `sigma_1, sigma_2, ...` (among the currently maximal arms, pull the `sigma_t`-first). Let `f_2(0) = f_3(0) = 0`, `f_2(1) = 5`, `f_1(0) = -1`, `f_1'(0) = +1`, `f_1(1) = f_1'(1) = -100`, and let `sigma_1` rank 2 before 3 and `sigma_2` rank 3 before 2. Unprimed run: at `t = 1` the maximal set is `{2,3}` and `sigma_1` selects arm 2; at `t = 2` the keys are `f_1(0) = -1`, `f_2(1) = 5`, `f_3(0) = 0`, so arm 2 is pulled again; hence `T_3(2) = 0`. Primed run: at `t = 1` arm 1 is the unique maximizer (`f_1'(0) = 1 > 0`) and is pulled; at `t = 2` the keys are `f_1'(1) = -100`, `f_2(0) = 0`, `f_3(0) = 0`, the maximal set is `{2,3}` and `sigma_2` selects arm 3; hence `T_3'(2) = 1 > 0 = T_3(2)`. So raising arm 1 strictly increased arm 3's count at time 2 on this sample point. Section 5.3 gives a counterexample of the same kind realized by actual Bernoulli tapes under `KH-UCB`, and states precisely what does and does not survive.

### Lemma 2.2 (the imported bandit bound, verbatim). Target: requirement 1 and lesson L3.

Imported statement (Lattimore and Szepesvari, Bandit Algorithms, free online edition, https://tor-lattimore.com/downloads/book/book.pdf, read on 17 September 2026). Algorithm 3 on the page headed "7.1 The Optimism Principle 103" is `UCB(delta)`: at each round `t in [n]`, play `A_t = argmax_i UCB_i(t-1, delta)` where, by display (7.2) on the same page,

  `UCB_i(t-1, delta) = +infinity` if `T_i(t-1) = 0`, and `= hat mu_i(t-1) + sqrt( 2 log(1/delta) / T_i(t-1) )` otherwise.

Theorem 7.1 (page headed "7.1 The Optimism Principle 105"), verbatim content: "Consider UCB as shown in Algorithm 3 on a stochastic k-armed 1-subgaussian bandit problem. For any horizon n, if delta = 1/n^2, then `R_n <= 3 sum_{i=1}^k Delta_i + sum_{i : Delta_i > 0} 16 log(n) / Delta_i`." Inside its proof, on the page headed "7.1 The Optimism Principle 108", the following display is established for every suboptimal arm `i` and is then substituted into the regret decomposition:

  (LS)  `E[T_i(n)] <= 3 + 16 log(n) / Delta_i^2`,  `Delta_i := mu^* - mu_i > 0`, `delta = 1/n^2`.

Theorem 7.2 on that same page states `R_n <= 8 sqrt(n k log(n)) + 3 sum_i Delta_i` and is proved from (LS) exactly as we reprove the gap-free consequence in Corollary 2.3.

Hypotheses actually used by that proof, checked line by line in this session.
1. Each arm `i` has a fixed reward distribution `P_i` with mean `mu_i` that is 1-subgaussian, and the rewards are realized in the reward-stack (tape) model of Section 4.6 of the same book (page headed "4.7 The Canonical Bandit Model for Uncountable Action Sets 66"): independent variables `X_{s,i}`, `s in [n]`, `i in [k]`, with `X_t = X_{T_{A_t}(t), A_t}`. This is exactly the own-pull-index tape coupling that we use, so no change of probability space is needed when we import the bound.
2. The horizon `n` is known to the algorithm, since `delta = 1/n^2`. `[KH]`
3. Tie-breaking is arbitrary. The proof uses the tie-breaking only through the implication "if `A_t = i` then `UCB_i(t-1,delta) >= UCB_1(t-1,delta)`", which holds for every tie-breaking rule because `A_t` is a maximizer of the index; the contradiction derived there is `UCB_i(t-1,delta) < mu_1 < UCB_1(t-1,delta)`, which contradicts `A_t = i` under any tie-breaking rule. Hence (LS) is valid for our fixed-priority rule, and in particular for `KH-UCB(n,pi)` for every realization of `pi`.
4. Bernoulli rewards. A random variable with values in `[0,1]` is `1/2`-subgaussian by Hoeffding's lemma, and a `sigma`-subgaussian variable is `sigma'`-subgaussian for every `sigma' >= sigma`; hence Bernoulli rewards are 1-subgaussian and (LS) applies verbatim with `sqrt(2 log(1/delta)/T) = sqrt(4 log n / T)`, which is the `KH-UCB` index.

### Corollary 2.3 (the two forms of the bound that we use).

Let `n >= 2`, let `pi` be any fixed permutation, and consider `KH-UCB(n, pi)` run on `K` arms whose rewards are i.i.d. Bernoulli with fixed means `theta_1, ..., theta_K`, realized by own-pull-index tapes. Let `theta^* := max_a theta_a`, `Delta_a := theta^* - theta_a`, and let `T_a(s)` be the count of arm `a` after `s` rounds.

(2.3a) For every `s in {0,1,...,n}` and every arm `a`: `E T_a(s) <= min{ s, 3 + 16 log(n)/Delta_a^2 }` when `Delta_a > 0`.

(2.3b) For every `s in {0,...,n}` and every arm `a`: `Delta_a E T_a(s) <= 4 sqrt(s log n) + 3`, and consequently the cell pseudo-regret obeys `sum_a Delta_a E T_a(s) = E sum_{r <= s} (theta^* - theta_{I_r}) <= 4K sqrt(s log n) + 3K`.

(2.3c) More generally, if `Delta` is any number with `0 <= Delta <= Delta_a`, then `Delta E T_a(s) <= 4 sqrt(s log n) + 3`.

Proof. (2.3a) `T_a(s) <= s` always. For the other bound, extend the run from `s` rounds to `n` rounds on the same tapes and the same priority. The index of `KH-UCB(n,pi)` depends on the horizon only through the constant `log n`, which is the same in both runs `[KH]`; therefore the first `s` rounds of the `n`-round run coincide, sample point by sample point, with the `s`-round run, and `T_a(s) <= T_a(n)` pointwise. Lemma 2.2 (LS) applied to the `n`-round run gives `E T_a(n) <= 3 + 16 log(n)/Delta_a^2`. (This is the precise answer to "why does a horizon-`n` confidence level apply to an instance that is run for only `s <= n` rounds": one does not reprove anything, one truncates a longer run of the very same algorithm.)

(2.3b) If `Delta_a = 0` there is nothing to prove. Otherwise, by (2.3a),
`Delta_a E T_a(s) <= min{ s Delta_a , 3 Delta_a + 16 log(n)/Delta_a } <= 3 Delta_a + min{ s Delta_a , 16 log(n)/Delta_a }`.
(The last step is the elementary inequality `min{A, B+C} <= B + min{A,C}` for `A,B,C >= 0`, with `A = s Delta_a`, `B = 3 Delta_a`, `C = 16 log(n)/Delta_a`: if `A <= C` the left side is at most `A <= B + A`, and if `A > C` it is at most `B + C`.) Now `min{A, B} <= sqrt(AB)` gives `min{ s Delta_a, 16 log(n)/Delta_a } <= sqrt(16 s log n) = 4 sqrt(s log n)`, and `Delta_a <= 1` because all means lie in `[0,1]`. Summing over `a` gives the pseudo-regret form, and `sum_a Delta_a E T_a(s) = E sum_{r<=s}(theta^* - theta_{I_r})` is the standard count decomposition (each round `r <= s` contributes `theta^* - theta_{I_r} = Delta_{I_r}`).

(2.3c) `Delta E T_a(s) <= Delta_a E T_a(s)` if `Delta <= Delta_a`, and the bound in (2.3b) is what we just proved; if `Delta_a = 0` then `Delta = 0`. QED

Note. `4 sqrt(s log n) + 3` is uniform over `(theta_1,...,theta_K)`: this is the gap-free form we need, since the cell-average means are unknown functions of `nu` and of the deviating map.

### Lemma 2.4 (own-pull-index tapes for blind agents; the scalar and finite-context coupling).

Setup. Scalar model of `setting.tex`. Let `(U_{a,k})_{a in [K], k >= 1}` be i.i.d. uniform on `[0,1]`, let `omega_1,...,omega_K` be the agents' private coins and `pi` the platform's priority, all mutually independent. Let agent `a` use a blind nonanticipating strategy `sigma_a`: at its `k`-th own pull it chooses

  `m_{a,k} := sigma_a( m_{a,1}, Y_{a,1}, ..., m_{a,k-1}, Y_{a,k-1} ; omega_a, n ) in [0, M_a]`,

and set `Y_{a,k} := 1{ U_{a,k} <= m_{a,k} }`. Let the platform run any rule that selects `I_t` as a measurable function of `(I_1, Y_1, ..., I_{t-1}, Y_{t-1}, pi)`, and set `Y_t := Y_{I_t, k}` with `k := T_{I_t}(t-1) + 1`.

Claims.
(i) The array `(m_{a,k}, Y_{a,k})_{a,k}` is well defined by the displayed recursion and is a measurable function of `(omega_a, (U_{a,k})_k)` for each `a` separately. In particular it does not depend on the platform's rule, on the other agents, or on the rounds at which the pulls occur.
(ii) The process `(I_t, m_{I_t,t}, Y_t)_{t <= n}` has exactly the law prescribed by the model: given the past and the current target, `Y_t` is Bernoulli at that target and conditionally independent of the past.
(iii) `[KH]` Define `f_a(0) := +infinity` and `f_a(k) := (1/k) sum_{l <= k} Y_{a,l} + sqrt(4 log(n)/k)` for `k >= 1`. Then the `KH-UCB(n,pi)` execution on this space is exactly the greedy race of Lemma 2.1 with sequences `(f_a)_{a in [K]}` and the strict priority induced by `pi`.

Proof. (i) is the definition of a recursion on `k` with `m_{a,k}` depending only on `(U_{a,1},...,U_{a,k-1}, omega_a)`; blindness is what makes the recursion closed, since `sigma_a` is not allowed to read the global round, the other agents' data, or its own selection times.

(ii) Induction on `t`. Write `H_{t-1}` for the platform-visible past together with the targets used so far. Given `H_{t-1}`, the selection `I_t = a` is determined by `H_{t-1}` and `pi`, and `k = T_a(t-1)+1` is `H_{t-1}`-measurable. The target `m_{a,k}` is a function of `(U_{a,1},...,U_{a,k-1}, omega_a)`. The pair `(a,k)` is consumed at exactly one round, namely the round of `a`'s `k`-th pull, so `U_{a,k}` has not been read before round `t`; being independent of `(omega, (U_{b,l}) : (b,l) != (a,k))` it is uniform conditionally on `H_{t-1}`, on `pi` and on `m_{a,k}`. Hence `P(Y_t = 1 | H_{t-1}, I_t = a, m_{a,k}) = m_{a,k}` and `Y_t` is conditionally independent of `H_{t-1}` given the target. This is the model's law.

(iii) At any round the `KH-UCB` index of arm `a` is `+infinity` if `T_a = 0` and otherwise `hat m_a + sqrt(4 log(n)/T_a)`, where `hat m_a` is the average of `a`'s first `T_a` observed rewards, that is of `Y_{a,1},...,Y_{a,T_a}`. So the index is exactly `f_a(T_a)`, a function of the arm and of its own count only, fixed before play by (i). The selection rule (highest-priority maximizer) is the key-maximal rule of Lemma 2.1. QED

`[KH]` is attached to (iii) because it is here that the index is a function of the arm's own count alone. With the anytime index `hat m_a + sqrt(2 log(t)/T_a)` the index is `f_a(T_a, t)`, a function of the count AND the global round, and the execution is not a static race; see Section 5.2 and the explicit tape in Section 5.3.

### Lemma 2.5 (conditional law of the profiles that visit a cell).

Let `X_1,...,X_n` be i.i.d. `nu` on `X`, let `kappa : X -> {1,...,J}` be measurable with cells `C_v := kappa^{-1}(v)`, and put `Z_t := kappa(X_t)`, `Z := (Z_1,...,Z_n)`. Fix `z = (z_1,...,z_n)` with `P(Z = z) > 0`; then `nu(C_{z_t}) > 0` for every `t`. For a cell `C` let `s_C(z) := #{ t : z_t = C }` and let `W_{C,1}, ..., W_{C,s_C(z)}` be the profiles at the visits to `C`, in increasing order of round (on the event `{Z = z}` the visit rounds are determined by `z`). Then, conditionally on `{Z = z}`, the family `( W_{C,k} : C, 1 <= k <= s_C(z) )` is independent, with `W_{C,k}` distributed as `nu( . | C)`; and it is independent of every random element that is independent of `(X_1,...,X_n)`, in particular of the tapes `(U_{C,a,l})` and the priorities `(pi_C)`.

Proof. `P(Z = z) = prod_{t <= n} nu(C_{z_t})` by independence. For Borel sets `A_1,...,A_n`,
`P( X_t in A_t for all t, Z = z ) = prod_t nu(A_t cap C_{z_t})`, hence
`P( X_t in A_t for all t | Z = z ) = prod_t nu(A_t | C_{z_t})`.
On `{Z=z}` the list `(W_{C,k})` is a deterministic reindexing of `(X_1,...,X_n)`, so the displayed product form is exactly the assertion. The final sentence holds because conditioning on an event of `sigma(X_1,...,X_n)` does not change the law of variables independent of `(X_1,...,X_n)` nor their independence from the `X`'s. QED

### Lemma 2.6 (cell-average coupling: the law of a cell's execution).

Consider Static Grid KH-UCB with a fixed map profile `(m_{a,n})_{a in [K]}` in `S_HDS`. Realize rewards as follows: uniforms `(U_{C,a,l})` indexed by cell, agent and the agent's own local pull index inside that cell, i.i.d. uniform on `[0,1]` and independent of the contexts and of the priorities `(pi_C)`; at the `k`-th visit to cell `C`, if the selected agent is `a` and this is `a`'s `l`-th pull inside `C`, the reward is `Y := 1{ U_{C,a,l} <= m_{a,n}(W_{C,k}) }`. For a cell with `nu(C) > 0` put `bar m_{a,C} := E[ m_{a,n}(X) | X in C ]`. Then:

(i) this realization has the law prescribed by the model (rewards conditionally Bernoulli with parameter `m_{a,n}(X_t)` given the profile and the selection, independent of the past);

(ii) for every `z` with `P(Z=z) > 0`, conditionally on `{Z = z}` the cells' within-cell selection and reward arrays `( (A_{C,k}, Y_{C,k})_{k <= s_C(z)} )_C` are independent across cells, and for each cell `C` the conditional law of `(A_{C,k}, Y_{C,k})_{k <= s_C(z)}` equals the law of the first `s_C(z)` rounds of a STANDALONE `KH-UCB(n, pi_C)` run on `K` arms whose rewards are i.i.d. Bernoulli with the cell-average means `bar m_{1,C}, ..., bar m_{K,C}`, realized by own-pull-index tapes;

(iii) consequently, for every cell `C`, every agent `j` and every `z`, `E[ T_j(C;n) | Z = z ] = E[ N_j( s_C(z) ) ]`, where `N_j(s)` is the count of arm `j` after `s` rounds of that standalone cell-average run; and `E T_j(C;n) = sum_z P(Z=z) E[N_j(s_C(z))]`.

Proof. (i) Each triple `(C,a,l)` is consumed at most once (the `l`-th pull of `a` inside `C` happens at most once), so at the round in question `U_{C,a,l}` is independent of everything already determined, and given `W_{C,k} = X_t` and the selection the reward is Bernoulli at `m_{a,n}(X_t)`. This is the argument of Lemma 2.4(ii) verbatim.

(ii) Fix `z` with `P(Z=z)>0` and condition on `{Z=z}`; then each `s_C := s_C(z)` is a constant and the rounds of the visits to `C` are determined. Write `H_{C,k} := ((A_{C,1},Y_{C,1}),...,(A_{C,k},Y_{C,k}))`. Because the rule is cell-blind and uses only cell `C`'s own statistics and `pi_C`, and because the index contains the constant `log n` rather than the running round `[KH]`, there are deterministic maps `g_k` with `A_{C,k} = g_k(H_{C,k-1}, pi_C)`; the local pull index `l_{C,k} := 1 + #{ k' < k : A_{C,k'} = A_{C,k} }` is a function of `(H_{C,k-1}, A_{C,k})`. Now condition further on `H_{C,k-1}`, on `pi_C`, on all data of the other cells, and on all uniforms consumed so far. By Lemma 2.5, `W_{C,k}` still has law `nu(.|C)` under this conditioning (the conditioning variables are functions of `Z`, of the priorities and tapes, and of `W_{C',k'}` for `(C',k') != (C,k)`, all independent of `W_{C,k}` given `Z = z`), and `U_{C,A_{C,k}, l_{C,k}}` is still uniform and independent of `W_{C,k}` (that triple has not been consumed). Hence, with `a := A_{C,k}`,

  `P( Y_{C,k} = 1 | H_{C,k-1}, pi_C, everything else listed ) = E[ m_{a,n}(W) ] , W ~ nu(.|C) , = bar m_{a,C}`,

which depends only on `a`. The standalone cell-average run has exactly the same selection maps `g_k` and exactly the same one-step conditional reward law (its reward at that round is `1{V_{a,l} <= bar m_{a,C}}` with a fresh uniform, hence Bernoulli(`bar m_{a,C}`) given the past). A law on a finite sequence of pairs is determined by its one-step conditional laws, so by induction on `k` the two conditional laws of `(A_{C,k},Y_{C,k})_{k<=s_C}` agree. The displayed conditional probability does not depend on the other cells' data, and the pairs `(W, U, pi)` are independent across cells given `Z = z`, so the cells are conditionally independent. (iii) is immediate from (ii). QED

Warning (this is the pitfall the grid section must not fall into). Lemma 2.6 is an equality of LAWS, cell by cell, conditionally on the membership sequence. It is NOT a pathwise identification of the actual execution with the cell-average execution, and the coupling on ACTUAL visits does not order the reward tapes between two different map profiles: agent `a`'s `l`-th pull inside `C` happens at different visits `k` in the two executions, so the actual reward `1{U_{C,a,l} <= m_{a,n}(W_{C,k})}` is attached to different profiles in the two runs and the two runs' tapes are not comparable entrywise. All monotonicity conclusions for the grid are therefore statements about laws and expectations (Theorem 3(iii)), obtained by transporting a pathwise statement proved INSIDE the cell-average model. Static Grid KH-UCB is not claimed to be pathwise monotone on the original space.

### Lemma 2.7 (cell-blind factorization identity). Target: the identity required by S3 and requirement 2.

Let `C` be a cell with `nu(C) > 0`, let `phi : X -> R` be bounded measurable, put `bar phi_C := E[ phi(X) | X in C ]`, and let `j in [K]`. Then, for every `n`, every map profile in `S_HDS` and every realization of the algorithm as in Lemma 2.6,

  `E[ sum_{t <= n} 1{ X_t in C } 1{ I_t = j } phi(X_t) ] = bar phi_C * E[ T_j(C;n) ]`.

In particular, taking `phi = 1_R` for a measurable `R`,

  `E[ T_j(C cap R ; n) ] = nu(R | C) * E[ T_j(C;n) ]`.

Proof. The random element `Z` takes finitely many values; sum over those `z` with `P(Z=z)>0`. Condition on `{Z = z}`. On this event, `V_C(n) = s_C(z)` is a constant and

  `sum_{t<=n} 1{X_t in C} 1{I_t = j} phi(X_t) = sum_{k=1}^{s_C(z)} 1{ A_{C,k} = j } phi( W_{C,k} )`.

Fix `k <= s_C(z)`. By the argument in the proof of Lemma 2.6(ii), `A_{C,k} = g_k(H_{C,k-1}, pi_C)` and, by induction on `k`, `H_{C,k-1}` is a measurable function of `(pi_C, (U_{C,a,l})_{a,l}, W_{C,1}, ..., W_{C,k-1})`. Conditionally on `{Z=z}`, all of these are independent of `W_{C,k}`, whose conditional law is `nu(.|C)` (Lemma 2.5). Hence

  `E[ 1{A_{C,k} = j} phi(W_{C,k}) | Z = z ] = E[ 1{A_{C,k}=j} | Z=z ] * bar phi_C`.

Summing over `k = 1,...,s_C(z)` gives `E[ ... | Z=z ] = bar phi_C * E[ T_j(C;n) | Z=z ]`. Multiplying by `P(Z=z)` and summing over `z` gives the identity. QED

The identity holds in the following cases, each of which is covered by the proof and none of which needs a separate argument.
1. Cells visited fewer than `K` times, that is during the initialization rounds of the cell instance. For `k <= K` we have `A_{C,k} = pi_C(k)`, a function of `pi_C` alone, which is independent of `W_{C,k}`; this is the case `H_{C,k-1}` carries no reward information. Nothing in the proof used that the cell instance had left initialization.
2. Cells in which some agent is never selected. No step of the proof refers to any agent being selected; the identity is proved term by term in `k`, and `1{A_{C,k}=j}` may be identically zero.
3. Random visit counts. The conditioning on `Z` makes `V_C(n)` deterministic; the randomness of the visit count is restored by the outer sum over `z`. In particular `1{ V_C(n) >= k }` is a function of `Z` alone, which is why it can be carried through the factorization.
4. Cells never visited: `s_C(z) = 0` and both sides are `0`.
5. Zero-mass cells: if `nu(C) = 0` then `P(X_t in C) = 0` for every `t`, so almost surely `V_C(n) = 0` and both sides of the second display are `0`; such a cell is excluded from the first display only because `bar phi_C` is undefined, and it is excluded from every sum over cells below.

### Lemma 2.8 (one-step cell-average Lipschitz bound; lesson L2).

Let `C` be a cell of side at most `h_n` with `nu(C) > 0`, let `a in [K]`, and let `g : [0,1]^d -> R` be `L`-Lipschitz for the Euclidean norm on the block `x_a`. Then for every `X in C`,

  `| g(x_a) - E[ g(x_a') | X' in C ] | <= L sqrt(d) h_n`.

Consequently, for any nonempty `S subseteq [K]` and any `L`-Lipschitz `g_a`, `a in S`,

  `E[ max_{a in S} g_a(x_a) | C ] <= max_{a in S} E[ g_a(x_a) | C ] + L sqrt(d) h_n`.

Proof. For `X, X'` in `C`, each coordinate of `X - X'` is at most `h_n` in absolute value, so the block difference `x_a - x_a'` has Euclidean norm at most `sqrt(d) h_n` (it has `d` coordinates), whence `|g(x_a) - g(x_a')| <= L sqrt(d) h_n`. Integrating `X'` against `nu(.|C)` gives the first display. For the second, for every `X in C` and every `a in S`, `g_a(x_a) <= E[g_a | C] + L sqrt(d) h_n <= max_{a' in S} E[g_{a'} | C] + L sqrt(d) h_n`; take the maximum over `a in S` and then the conditional expectation. QED

This is the form demanded by lesson L2: the Lipschitz constant enters as `L sqrt(d)` with `d = D/K` the per-agent block dimension, and only one Lipschitz step is taken (the comparison is between a point and the cell average, not between two points through a distinguished representative). The manuscript's `2 L sqrt(D) h_n` is larger by the factor `2 sqrt(K)`, so every bound below implies the corresponding bound with the manuscript's constant.

### Lemma 2.9 (label symmetry with one uniform priority per instance).

Consider a standalone `KH-UCB(n, pi)` run of `s <= n` rounds on `K` arms with i.i.d. Bernoulli tapes of means `theta_1,...,theta_K`, with `pi` uniform on the permutations of `[K]` and independent of the tapes. If `theta_i = theta_j` for some `i != j`, then `E N_i(s) = E N_j(s)` exactly, for every `s`.

Proof. Realize the tapes as `Y_{a,l} = 1{ V_{a,l} <= theta_a }` with `(V_{a,l})` i.i.d. uniform. Let `tau` be the transposition of `i` and `j` and define `V~_{a,l} := V_{tau(a), l}` and `pi~ := tau o pi`. Since `(V_{a,l})` is an i.i.d. array, `V~` has the same law as `V`; since `pi` is uniform and `tau` is a bijection of the permutation group, `pi~` is uniform; and `V~` and `pi~` are independent. So `(V~, pi~)` has the same law as `(V, pi)`. Next, the run is equivariant: because `theta_{tau(a)} = theta_a` for every `a`, the tilde tape satisfies `Y~_{a,l} = 1{V_{tau(a),l} <= theta_a} = 1{V_{tau(a),l} <= theta_{tau(a)}} = Y_{tau(a),l}`; by induction on rounds, the tilde run's counts and empirical means satisfy `T~_a = T_{tau(a)}` and `hat m~_a = hat m_{tau(a)}`, hence its indices satisfy `Ind~_a = Ind_{tau(a)}`; and `pi~^{-1}(a) = pi^{-1}(tau(a))` means that `a`'s priority rank in the tilde run equals `tau(a)`'s rank in the original run. Therefore the key-maximal arm of the tilde run at each round is `tau` applied to the key-maximal arm of the original run, that is `I~_r = tau(I_r)` for every `r`, and `N_a(s; V~, pi~) = N_{tau(a)}(s; V, pi)`. Taking expectations and using `(V~,pi~) =_d (V,pi)`,

  `E N_i(s) = E N_i(s; V~, pi~) = E N_{tau(i)}(s; V, pi) = E N_j(s)`. QED

The uniform priority is essential: with the deterministic label order as the priority, the first `K` rounds pull `1,2,...,K` and every later tie favours the lower label, so two equal-mean arms need not have equal expected counts at a finite horizon (for example `K = 2`, `n = 1`). The uniform priority is also harmless for monotonicity, because Lemma 2.1 and hence Theorem 1(1a) hold conditionally on each realization of the priority; one may therefore average over `pi` afterwards.

## 3. Proofs of S0 to S8

### S0 (static race lemma). COMPLETE.

This is exactly Lemma 2.1, proved there in full, together with the explicit statement (after the proof) of the two places where the fixed strict priority is used and of what breaks with per-round fresh tie coins. Nothing about the `f_a` is assumed: they may be arbitrary extended-real sequences, non monotone, with repeated values and with `+infinity` entries (which is how the initialization rounds are encoded).

### S1 (C0, scalar). COMPLETE.

Proof of Theorem 1(1a). Work on the coupled space of Lemma 2.4 and condition on `pi` and on the private coins (the conclusion is proved for every realization). By Lemma 2.4(i), for every agent `a` the sequence `(m_{a,k}, Y_{a,k})_{k>=1}` is a function of `(omega_a, (U_{a,k})_k)` alone; since profiles `A` and `B` differ only in agent `i`'s strategy and share all coins and all uniforms, for every `a != i` and every `k` we have `m^A_{a,k} = m^B_{a,k}` and `Y^A_{a,k} = Y^B_{a,k}`. This is exactly where blindness is used: an agent that could see the global round, or the identity of the rounds at which it was selected, would in general produce a different target at its `k`-th pull in the two runs, because the two runs select it at different rounds.

For agent `i`, feasibility gives `m^A_{i,k} <= M_i = m^B_{i,k}` for every `k`, hence pointwise on the sample point

  `Y^A_{i,k} = 1{ U_{i,k} <= m^A_{i,k} } <= 1{ U_{i,k} <= M_i } = Y^B_{i,k}`,

so the partial sums obey `sum_{l<=k} Y^A_{i,l} <= sum_{l<=k} Y^B_{i,l}` and therefore the index sequences of Lemma 2.4(iii) obey `f^A_i(k) <= f^B_i(k)` for every `k >= 1`, with `f^A_i(0) = f^B_i(0) = +infinity`, while `f^A_a = f^B_a` for `a != i`. By Lemma 2.4(iii) both executions are greedy races with the same strict priority induced by `pi`. Lemma 2.1, applied with agent `i` in the role of arm 1, gives for every `t <= n`

  `T_j^B(t) <= T_j^A(t)` for all `j != i`, and `T_i^B(t) >= T_i^A(t)`,

on this sample point. Since the sample point and `pi` were arbitrary, the statement holds pathwise, and taking expectations gives `E T_j^B(n) <= E T_j^A(n)`: monotonicity with remainder `0`. The identical argument applies whenever `m^B_{i,k} >= m^A_{i,k}` for every `k` on the sample point, for example for two fixed means `m_i <= m_i'` in `S_HI` or two horizon-dependent fixed means. QED

Proof of Theorem 1(1b). Fix a profile of fixed means `(m_a)_{a in [K]}` (possibly depending on `n`) and let `m^* := max_a m_a`. Choose an honest `h` with `mu_h = mu_H^*`; honesty gives `m_h >= mu_h = mu_H^*`, hence `m^* >= mu_H^*`. With fixed means, `C_i(n) = (m_i - mu_i) T_i(n)` exactly, so

  `E C_i(n) - (mu_H^* - mu_i) E T_i(n) = (m_i - mu_H^*) E T_i(n) >= - (mu_H^* - m_i)_+ E T_i(n)`.

By Lemma 2.4(ii) the rewards of arm `a` are i.i.d. Bernoulli(`m_a`) in the own-pull-index tape model, which is the model in which Lemma 2.2 is proved, and Bernoulli variables are 1-subgaussian; so Corollary 2.3(c) applies with `s = n` and `Delta := (mu_H^* - m_i)_+ <= (m^* - m_i)_+ = Delta_i`, giving `(mu_H^* - m_i)_+ E T_i(n) <= 4 sqrt(n log n) + 3`. QED

Proof of Theorem 1(1c). `P(n;S) = E sum_t m_{I_t,t} = sum_i m_i E T_i(n) = sum_i ( E C_i(n) + mu_i E T_i(n) )`. Adding `mu_i E T_i(n)` to each inequality of (1b) and summing over the `K` agents, with `sum_i E T_i(n) = n`, gives `P(n;S) >= mu_H^* n - K(4 sqrt(n log n) + 3)`. QED

Proof of Theorem 1(1d). By Lemma 2.4(ii) the execution is a standalone `KH-UCB(n,pi)` run with Bernoulli means `theta_a = m_a`; apply Lemma 2.9 with `s = n`. The exactness comes from the uniform `pi`, and is a statement about the algorithm as specified in TASK.md, not about the code's lowest-label rule. QED

Remark S1.1 (the anytime index is NOT pathwise monotone). Verified independently in this session by an explicit tape; see Section 5.3, which contains the full execution trace with index values, the interval conditions on the uniforms that make the sample point have positive probability under fixed means, and a variant with strictly separated indices at every round.

### S2 (C0, finite context). COMPLETE.

Setup for all four parts. The context sequence takes finitely many values in `X_F^n`; condition on `{ (X_1,...,X_n) = x }` for each such `x` of positive probability. Given this event, for every `z in X_F` the visit count `V_z = s_z(x)` and the visit rounds are determined. The instance at `z` uses only its own tapes `(U_{z,a,l})`, its own priority `pi_z` and its own past selections and rewards; the tapes and priorities are independent of the context sequence. Since the profile at every visit to `z` is exactly `z`, the reward of agent `a` at its `l`-th pull inside the instance is `1{ U_{z,a,l} <= m_{a,n}(z) }`, an i.i.d. Bernoulli(`m_{a,n}(z)`) tape; and distinct instances use disjoint sets of uniforms and independent priorities. Hence, conditionally on `{X = x}`, the instances are independent and the instance at `z` is exactly the first `s_z(x)` rounds of a standalone `KH-UCB(n, pi_z)` run on `K` Bernoulli arms with means `(m_{a,n}(z))_a` in the own-pull-index tape model. (This is Lemma 2.6 in the degenerate case in which the cell is a single exact profile, so no cell-average step is needed; equivalently it is Lemma 2.4 applied inside each instance.) No i.i.d. assumption on the contexts is used anywhere in (2a) to (2d) and (2e); only exogeneity, that is independence of the context sequence from the tapes and the priorities.

(2a) Sharp adaptivity. Fix `i` and `R subseteq X_F`. Since the map is fixed,
`E sum_{t<=n} 1{X_t in R, I_t=i} c_{i,t} - E sum_{t<=n} 1{X_t in R, I_t=i}[b(X_t) - mu_i(x_{i,t})] = sum_{z in R} ( m_{i,n}(z) - b(z) ) E T_i(z) >= - sum_{z in R} ( b(z) - m_{i,n}(z) )_+ E T_i(z)`.
Choose for each `z` an honest `h_z` attaining `b(z) = mu_{h_z}(z_{h_z})`; honesty gives `m_{h_z,n}(z) >= b(z)`, so `m^*(z) := max_a m_{a,n}(z) >= b(z)` and `(b(z) - m_{i,n}(z))_+ <= Delta_i(z) := m^*(z) - m_{i,n}(z)`. Conditionally on `{X = x}`, Corollary 2.3(c) with `s = s_z(x)` gives
`(b(z) - m_{i,n}(z))_+ E[ T_i(z) | X = x ] <= 4 sqrt( s_z(x) log n ) + 3 * 1{ s_z(x) >= 1 }`.
Averaging over `x` and using the concavity of the square root (Jensen),
`(b(z)-m_{i,n}(z))_+ E T_i(z) <= 4 sqrt( E V_z log n ) + 3 P(V_z >= 1)`.
Summing over `z in R` and using Cauchy-Schwarz, `sum_{z in R} sqrt(E V_z) <= sqrt( |R| sum_{z in R} E V_z ) <= sqrt(|R| n)`, and `sum_{z in R} P(V_z>=1) <= |R|`, so the total is at most `4 sqrt(|R| n log n) + 3|R|`. QED

(2b) Exact monotonicity. Condition on `{X = x}`. Let `m'_{i,n} >= m_{i,n}` pointwise on `X_F` (in particular `m'_{i,n} = M_i`), all other maps unchanged, all tapes and priorities shared. In each instance `z` the arm-`i` tape satisfies `1{U_{z,i,l} <= m_{i,n}(z)} <= 1{U_{z,i,l} <= m'_{i,n}(z)}` for every `l`, and all other arms' tapes are identical; by Lemma 2.4(iii) and Lemma 2.1 (applied inside instance `z`, whose priority `pi_z` is the same in both runs), `T'_j(z) <= T_j(z)` pathwise for every `j != i` and every `z`, and `T'_i(z) >= T_i(z)`. Summing over `z in R` gives `T'_j(R;n) <= T_j(R;n)` pathwise given the contexts, and hence `E T'_j(R;n) <= E T_j(R;n)`, with remainder exactly `0`, for every `R`, every `n` and every pair of maps in the stated relation. Independent ex ante mixtures are handled by conditioning on the realized maps. QED

(2c) Exact expected FATA. Let `G := G_ij(R)` and assume `m_{i,n}(z) = m_{j,n}(z) = M_*(z)` for `z in G`. Conditionally on `{X = x}`, instance `z in G` is a standalone run in which arms `i` and `j` have equal Bernoulli means, so Lemma 2.9 gives `E[T_i(z)|X=x] = E[T_j(z)|X=x]`. Averaging over `x` and summing over `z in G` gives `E T_i(G;n) = E T_j(G;n)` exactly. QED

(2d) Robustness. Conditionally on `{X=x}`, Corollary 2.3(b) applied to instance `z` gives
`E[ sum_{t : X_t = z} ( m^*(z) - m_{I_t,n}(z) ) | X = x ] <= 4K sqrt( s_z(x) log n ) + 3K`,
and `m^*(z) >= b(z)` as in (2a). Averaging (Jensen), summing over the `Q` profiles and using Cauchy-Schwarz as in (2a),
`E sum_{t<=n} [ b(X_t) - m_{I_t,n}(X_t) ] <= 4K sqrt(Q n log n) + 3KQ`,
and `P(n) = E sum_t m_{I_t,n}(X_t)`. QED

(2e) Public part. Write `T^0` for counts under `S^max` and `T'` for counts under the deviation `m'_{i,n}` of agent `i`. Utilities decompose profile by profile: `u_i(n;S) = E sum_t 1{I_t=i} ( 1 + mu_i(x_{i,t}) - m_{i,n}(X_t) ) = sum_z ( 1 + mu_i(z_i) - m_{i,n}(z) ) E T_i(z)`. Put `a^0_z := 1 + mu_i(z_i) - M_i(z_i) >= 0` (because `M_i(z_i) <= 1` and `mu_i(z_i) >= 0`) and `delta_z := M_i(z_i) - m'_{i,n}(z) >= 0` (feasibility). Then
`u_i(n; m'_i, S^max_{-i}) - u_i(n;S^max) = sum_z [ (a^0_z + delta_z) E T'_i(z) - a^0_z E T^0_i(z) ] <= sum_z delta_z E T'_i(z)`,
using `a^0_z >= 0` and `E T'_i(z) <= E T^0_i(z)`, which is (2b) read in the direction "raising agent `i`'s map from `m'_{i,n}` to `M_i` weakly increases agent `i`'s own count" (Lemma 2.1(a)).
Fix `z` visited with positive probability. By `|T(z)| >= 2` there is `j != i` with `M_j(z_j) = M_*(z) >= M_i(z_i)`; under the deviation agent `j` still plays `M_j(z_j)`, so in instance `z` the best arm mean is at least `M_i(z_i)` and agent `i`'s gap is at least `M_i(z_i) - m'_{i,n}(z) = delta_z`. Corollary 2.3(c) with `Delta := delta_z` therefore gives, conditionally on `{X=x}`, `delta_z E[T'_i(z)|X=x] <= 4 sqrt(s_z(x) log n) + 3*1{s_z(x)>=1}`. Averaging and summing over the at most `Q` visited profiles exactly as in (2a) gives the uniform bound `4 sqrt(Q n log n) + 3Q`, which is `o(n)`; hence `S^max` is an `S_F`-asymptotic equilibrium (Definition 1), and the bound holds simultaneously for all deviations, deterministic or mixed (condition on the realized map). For a FIXED deviation, let `Delta_dev := min{ delta_z : z visited with positive probability, delta_z > 0 }`; if this set is empty the gain is `0`, and otherwise Corollary 2.3(a) gives `delta_z E T'_i(z) <= 3 delta_z + 16 log(n)/delta_z <= 3 + 16 log(n)/Delta_dev`, so the gain is at most `Q(3 + 16 log(n)/Delta_dev) = O(Q log n)`, with a constant depending on the deviation, exactly as in the manuscript's scalar Theorem `thm:public-ucb`.
Revenue: `E sum_t [ M_*(X_t) - m_{I_t,n}(X_t) ] = sum_z sum_a (M_*(z) - M_a(z_a)) E T_a(z)`, and `M_*(z) = max_a M_a(z_a)` is the best arm mean of instance `z` under `S^max`, so Corollary 2.3(b) and the averaging of (2d) give `4K sqrt(Q n log n) + 3KQ`; under a uniform positive gap `Delta_0` for the non-top agents, Corollary 2.3(a) gives instead `KQ(3 + 16 log(n)/Delta_0)`. QED

Remark S2.1. Relative to the manuscript's Theorem `thm:finite-context`, the monotonicity remainder improves from `o(n)` (and only pointwise in the fixed comparison) to exactly `0` and pathwise given the contexts; the public part becomes uniform over deviations at rate `4 sqrt(Qn log n) + 3Q`; and the i.i.d. and positive-mass assumptions are not needed in any part, only exogeneity of the contexts.

### Common preliminaries for S3 to S8 (the grid)

Fix `n >= 2` and the grid of Section "Conventions". Cells with `nu(C) = 0` satisfy `P(X_t in C) = 0` for every `t <= n`, hence are almost surely never visited and contribute `0` to every expectation below; all sums over cells are over the finitely many cells with `nu(C) > 0`, and lazy initialization changes nothing. Write `V_C := V_C(n)`, `bar m_{a,C} := E[m_{a,n}(X)|X in C]`, `bar m^*_C := max_a bar m_{a,C}`, `Delta_{a,C} := bar m^*_C - bar m_{a,C} >= 0`, `bar b_C := E[b(X)|X in C]`. Note `sum_C E V_C = n` and `sum_C 1{V_C >= 1} <= min{J_n, n}` pathwise, since at most `n` cells can be visited in `n` rounds. Independent ex ante mixtures are always handled by conditioning on the realized map profile, which is independent of the contexts, the tapes and the priorities; every bound below is uniform over map profiles, so it survives the averaging. All boundaries and interiors are relative to the compact metric space `X = [0,1]^D`.

Two facts are used repeatedly.

(P1) Per-cell bandit bound. For every cell `C` with `nu(C) > 0`, every agent `a` and every number `Delta` with `0 <= Delta <= Delta_{a,C}`,

  `Delta * E T_a(C;n) <= 4 sqrt( E V_C * log n ) + 3 P(V_C >= 1)`.

Proof: condition on `{Z = z}`; by Lemma 2.6(iii) the conditional law of `T_a(C;n)` is that of `N_a(s_C(z))` in the standalone cell-average run, whose arm means are `(bar m_{a,C})_a` and whose gaps are `(Delta_{a,C})_a`; Corollary 2.3(c) gives `Delta E[T_a(C;n)|Z=z] <= 4 sqrt(s_C(z) log n) + 3*1{s_C(z) >= 1}`. Average over `z` and use Jensen for the concave square root. `[KH]` through Corollary 2.3.

(P2) Summation. `sum_C [ 4 sqrt(E V_C log n) + 3 P(V_C >= 1) ] <= 4 sqrt(J_n n log n) + 3 min{J_n, n}`, by Cauchy-Schwarz (`sum_C sqrt(E V_C) <= sqrt(J_n sum_C E V_C) = sqrt(J_n n)`) and by `sum_C 1{V_C>=1} <= min{J_n,n}` pathwise.

### S3 (C1 (iii), grid, exact expected monotonicity). COMPLETE.

Claim (Theorem 3(iii)). Let `m` and `m'` be map profiles in `S_HDS` that agree for every agent other than `i` and satisfy `m'_{i,n} >= m_{i,n}` `nu`-almost everywhere (the case `m'_{i,n} = M_i` is the statement of contextual monotonicity; feasibility gives `m_{i,n} <= M_i` pointwise, so that case is covered). Then for every `j != i`, every measurable `R` and every `n`, `E T'_j(R;n) <= E T_j(R;n)`, with zero remainder.

Proof. Step 1 (cell averages are ordered). For every cell `C` with `nu(C)>0`, `bar m'_{a,C} = bar m_{a,C}` for `a != i`, and `bar m'_{i,C} = E[m'_{i,n}|C] >= E[m_{i,n}|C] = bar m_{i,C}` because `m'_{i,n} >= m_{i,n}` holds `nu`-a.e. and `nu(.|C)` is absolutely continuous with respect to `nu`.

Step 2 (pathwise monotonicity inside the cell-average model). Fix a cell `C` and `s in {0,...,n}` and consider the two standalone cell-average runs of Lemma 2.6(ii), one with means `(bar m_{a,C})_a` and one with means `(bar m'_{a,C})_a`, both with the same priority `pi_C`. Couple them by common uniforms `(V_{a,l})`: `Y_{a,l} := 1{V_{a,l} <= bar m_{a,C}}` and `Y'_{a,l} := 1{V_{a,l} <= bar m'_{a,C}}`. By Step 1, `Y'_{i,l} >= Y_{i,l}` for every `l` and `Y'_{a,l} = Y_{a,l}` for `a != i`, on every sample point. By Lemma 2.4(iii) each run is a greedy static race with the index sequences `f_a(0) = +infinity`, `f_a(k) = (1/k) sum_{l<=k} Y_{a,l} + sqrt(4 log(n)/k)` `[KH]`, the primed sequences dominate the unprimed ones for arm `i` and coincide for the others, and both runs use the same strict priority induced by `pi_C`. Lemma 2.1 gives, pathwise and for every `s`,
  `N'_j(s) <= N_j(s)` for every `j != i`, and `N'_i(s) >= N_i(s)`.
Taking expectations, `E N'_j(s) <= E N_j(s)` for every `s in {0,...,n}` and every `j != i`.

Step 3 (transport to the real execution). The context sequence and therefore the membership sequence `Z` have the same law under both map profiles, because the contexts are exogenous: their law does not depend on the agents' maps. By Lemma 2.6(iii), for every `z` with `P(Z=z) > 0`,
  `E[T'_j(C;n)|Z=z] = E N'_j(s_C(z)) <= E N_j(s_C(z)) = E[T_j(C;n)|Z=z]`.
Multiplying by `P(Z=z)` and summing over `z` gives `E T'_j(C;n) <= E T_j(C;n)` for every cell `C` and every `j != i`. The same computation with the pathwise inequality of Step 2 shows that, conditionally on `Z=z`, `T'_j(C;n)` is stochastically dominated by `T_j(C;n)`; and `E T'_i(C;n) >= E T_i(C;n)`.

Step 4 (from cells to an arbitrary measurable region). By Lemma 2.7 applied to each profile separately (the identity holds for every fixed map profile), for every measurable `R`,
  `E T'_j(R;n) = sum_C E T'_j(C cap R; n) = sum_C nu(R|C) E T'_j(C;n) <= sum_C nu(R|C) E T_j(C;n) = sum_C E T_j(C cap R;n) = E T_j(R;n)`,
the sums being over the finitely many cells with `nu(C)>0` and the inequality being termwise with the nonnegative weights `nu(R|C) in [0,1]`. Summing `E T_i(C cap R;n) = nu(R|C) E T_i(C;n)` in the same way gives `E T'_i(R;n) >= E T_i(R;n)` as well, for arbitrary measurable `R`. QED

Discussion of the required identity (requirement 2). The identity `E T_j(C cap R;n) = nu(R|C) E T_j(C;n)` is Lemma 2.7 and is proved there for every measurable `R`, including cells visited fewer than `K` times, cells in which some agent is never selected, cells never visited, random visit counts and zero-mass cells; the five cases are listed and discharged immediately after the proof of Lemma 2.7. The heart of it is that the selection at the `k`-th visit of `C` is a function of the cell's first `k-1` visits and of `pi_C`, hence independent of the `k`-th visit's exact profile, whose conditional law is `nu(.|C)`.

Why this is an expectation statement and not a pathwise one. See the Warning after Lemma 2.6: on the original probability space the two executions attach agent `a`'s `l`-th local uniform to different visits and therefore to different profiles, so their actual reward tapes are not ordered. The pathwise argument lives entirely inside the cell-average model, where the arm means are constants; the transport in Step 3 is an equality of conditional laws. No pathwise monotonicity is claimed for Static Grid KH-UCB, and none is needed.

### S4 (C1 (i), grid sharp adaptivity). COMPLETE.

Claim (Theorem 3(i)). Assume every `mu_a : [0,1]^d -> [0,1]` is `L`-Lipschitz. For every agent `i`, every measurable `R subseteq X`, every `n >= 2` and every map profile in `S_HDS`,
  `E sum_{t<=n} 1{X_t in R, I_t=i} c_{i,t} >= E sum_{t<=n} 1{X_t in R, I_t=i} [b(X_t) - mu_i(x_{i,t})] - r_n(R)`,
  `r_n(R) = L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 min{J_n,n} + n nu((boundary R)^{sqrt(D) h_n})`.

Proof. Since `c_{i,t} = m_{i,n}(X_t) - mu_i(x_{i,t})`, the claim is equivalent to
  `E sum_{t<=n} 1{X_t in R, I_t = i} ( b(X_t) - m_{i,n}(X_t) ) <= r_n(R)`.

Step 1 (splitting the cells). Let `Int(R) := {C : nu(C)>0, C subseteq R}`, `Bdy(R) := {C : nu(C)>0, C cap R != empty, C cap R^c != empty}`; cells disjoint from `R` contribute nothing. Then
  `E sum_t 1{X_t in R, I_t=i}(b - m_{i,n}) = sum_{C in Int(R)} E sum_{t : X_t in C} 1{I_t=i}(b - m_{i,n}) + sum_{C in Bdy(R)} E sum_{t: X_t in C cap R} 1{I_t=i}(b-m_{i,n})`.

Step 2 (interior cells: the factorization). By Lemma 2.7 with the bounded measurable `phi := b - m_{i,n}` (`b = max_{h in K_H} mu_h(x_h)` is a maximum of finitely many continuous functions, hence continuous), the first sum equals `sum_{C in Int(R)} ( bar b_C - bar m_{i,C} ) E T_i(C;n)`.

Step 3 (one Lipschitz step, lesson L2). Fix `C` with `nu(C)>0`. By Lemma 2.8 applied to the finite family `{ mu_h : h in K_H }`,
  `bar b_C = E[ max_{h in K_H} mu_h(x_h) | C ] <= max_{h in K_H} E[ mu_h(x_h) | C ] + L sqrt(d) h_n`.
Honesty is pointwise, `m_{h,n}(X) >= mu_h(x_h)` for every `X` and every honest `h`, hence `E[mu_h(x_h)|C] <= bar m_{h,C} <= bar m^*_C`. Therefore
  `bar b_C <= bar m^*_C + L sqrt(d) h_n`, and so `bar b_C - bar m_{i,C} <= Delta_{i,C} + L sqrt(d) h_n`.
(The manuscript chains two Lipschitz steps through a representative point `x_C` and obtains `2 L sqrt(D) h_n`; the bound here is smaller by the factor `2 sqrt(K)` and implies the manuscript's.)

Step 4 (per-cell bandit bound and summation). Using Step 3, then (P1) with `Delta := Delta_{i,C}` and (P2),
  `sum_{C in Int(R)} (bar b_C - bar m_{i,C}) E T_i(C;n) <= sum_C Delta_{i,C} E T_i(C;n) + L sqrt(d) h_n sum_C E T_i(C;n) <= 4 sqrt(J_n n log n) + 3 min{J_n,n} + L sqrt(d) h_n E T_i(n)`,
and `E T_i(n) <= n`. (Terms of `Int(R)` were completed to all cells; every summand `Delta_{i,C} E T_i(C;n)` is nonnegative, so this only increases the bound.)

Step 5 (boundary cells). Let `C in Bdy(R)`. A cell is a product of intervals, hence convex and connected. If `C` did not meet `boundary R`, then `C` would be covered by the two disjoint relatively open sets `C cap interior(R)` and `C cap interior(R^c)`, both nonempty because `C` meets `R` and `R^c` and meets no boundary point, contradicting connectedness. So `C` contains a point of `boundary R` and, having diameter at most `sqrt(D) h_n`, satisfies `C subseteq (boundary R)^{sqrt(D) h_n}`. Since every summand `b - m_{i,n}` lies in `[-1,1]`,
  `sum_{C in Bdy(R)} E sum_{t : X_t in C cap R} 1{I_t=i} (b - m_{i,n}) <= sum_{C in Bdy(R)} E V_C = n sum_{C in Bdy(R)} nu(C) = n nu( union of Bdy(R) cells ) <= n nu( (boundary R)^{sqrt(D) h_n} )`,
where `E V_C = n nu(C)` because the contexts are i.i.d. `nu`, and the union is disjoint.

Step 6 (rate). With `h_n = (log(en)/n)^{1/(D+2)} <= 1` and `J_n <= 2^D h_n^{-D}`:
`n h_n = n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`;
`4 sqrt(J_n n log n) <= 4 * 2^{D/2} (n/log(en))^{D/(2(D+2))} sqrt(n log n) <= 4 * 2^{D/2} n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`, using `log n <= log(en)` and `1/2 - D/(2(D+2)) = 1/(D+2)`;
`3 min{J_n,n} <= 3 * 2^D n^{D/(D+2)} <= 3 * 2^D n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`.
Hence the first three terms of `r_n(R)` are at most `E_n <= (L sqrt(d) + 4*2^{D/2} + 3*2^D) n^{(D+1)/(D+2)} (log(en))^{1/(D+2)} = O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})` with a constant depending only on `K, D, L`.

Step 7 (boundary term is `o(n)` under the manuscript's hypothesis). `boundary R` is closed in the compact space `X`, so the closed neighbourhoods `(boundary R)^{eps}` decrease to `boundary R` as `eps` decreases to `0`; since `nu` is a finite measure, `nu((boundary R)^{eps}) -> nu(boundary R)`. If `nu(boundary R) = 0` and since `h_n -> 0`, the term `n nu((boundary R)^{sqrt(D) h_n})` is `o(n)`. Without any boundary hypothesis the first three terms still hold, so the statement is meaningful for EVERY measurable `R`; only its `o(n)` interpretation needs `nu(boundary R) = 0`.

Uniformity and mixtures. No step used anything about the maps except pointwise feasibility and pointwise honesty, so `r_n(R)` is uniform over `S_HDS`; mixtures follow by conditioning on the realized profile. QED

### S5 (C1 (ii), robustness). COMPLETE (restated, not reproved from scratch).

This is the manuscript's Theorem `thm:grid-ucb-robust`, already proved there for the anytime local-time rule. For `KH-UCB` cells the same three ingredients (cell-average law, one Lipschitz step, gap-free per-cell regret) give the explicit form of Theorem 3(ii). For completeness, the two-line derivation: by Lemma 2.7 with `phi = b - m_{a,n}` for each agent `a`,
  `E sum_{t<=n} [ b(X_t) - m_{I_t,n}(X_t) ] = sum_C sum_a ( bar b_C - bar m_{a,C} ) E T_a(C;n) <= sum_C [ L sqrt(d) h_n E V_C + sum_a Delta_{a,C} E T_a(C;n) ]`
by Step 3 of S4 and `sum_a E T_a(C;n) = E V_C`; then (P1) for each of the `K` agents and (P2) give
  `E sum_t [b(X_t) - m_{I_t,n}(X_t)] <= L sqrt(d) n h_n + 4K sqrt(J_n n log n) + 3K min{J_n, n}`,
and `P(n) = E sum_t m_{I_t,n}(X_t)`. The rate is `O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})` by Step 6 of S4 with the constant multiplied by `K`. QED

### S6 (C1 (iv), grid FATA). COMPLETE.

Claim (Theorem 3(iv)). Let `G := G_ij(R)` and suppose `m_{i,n}(X) = m_{j,n}(X) = M_*(X)` for every `X in G`. Then `| E T_i(G;n) - E T_j(G;n) | <= n nu( (boundary G)^{sqrt(D) h_n} )`.

Proof. Step 1 (cells inside `G`). Let `C subseteq G` with `nu(C)>0`. Then `bar m_{i,C} = E[M_*(X)|C] = bar m_{j,C}`. By Lemma 2.6(iii) the conditional law of `T_i(C;n)` given `{Z=z}` is that of `N_i(s_C(z))` in the standalone cell-average run with means `(bar m_{a,C})_a` and uniform priority `pi_C`; by Lemma 2.9 (equal means for arms `i,j`, uniform priority), `E N_i(s) = E N_j(s)` for every `s`. Hence `E[T_i(C;n)|Z=z] = E[T_j(C;n)|Z=z]` for every `z`, and `E T_i(C;n) = E T_j(C;n)`.

Step 2 (the rest). Cells disjoint from `G` contribute `0` to both counts. Every remaining cell meets both `G` and `G^c`, hence, by the connectedness argument of S4 Step 5, lies in `(boundary G)^{sqrt(D) h_n}`. Writing `Cross` for that family,
  `E T_i(G;n) - E T_j(G;n) = sum_{C subseteq G} ( E T_i(C;n) - E T_j(C;n) ) + sum_{C in Cross} ( E T_i(C cap G;n) - E T_j(C cap G;n) ) = sum_{C in Cross} ( E T_i(C cap G;n) - E T_j(C cap G;n) )`.
For each `C`, `T_i(C cap G;n)` and `T_j(C cap G;n)` are nonnegative and their sum is at most `V_C`, so the absolute value of their difference is at most `V_C`. Hence
  `| E T_i(G;n) - E T_j(G;n) | <= sum_{C in Cross} E V_C = n sum_{C in Cross} nu(C) <= n nu( (boundary G)^{sqrt(D) h_n} )`.
If `nu(boundary G) = 0` this is `o(n)` by the continuity from above of Step 7 of S4. QED

Note. No Lipschitz assumption is used, and the hypothesis is the one the manuscript uses for Grid-ETC FATA, namely a null boundary of the SHARED-TOP portion `G_ij(R)`, not of `R`. The one-uniform-priority-per-cell rule is exactly what makes Step 1 exact: with a deterministic label priority, Lemma 2.9 fails at finite horizons.

### S7 (C1 (v), revenue at all-maximum play). COMPLETE.

Claim (Theorem 3(v)). If every `M_a : [0,1]^d -> [0,1]` is `L`-Lipschitz, then under `S^max` (agent `a` uses the map `m_{a,n}(X) = M_a(x_a)`, which is feasible and, for honest agents, honest because `M_a(x_a) >= mu_a(x_a)`),
  `P(n;S^max) >= E sum_{t<=n} M_*(X_t) - [ L sqrt(d) n h_n + 4K sqrt(J_n n log n) + 3K min{J_n,n} ]`.

Proof. Under `S^max`, `bar m_{a,C} = bar M_{a,C} := E[M_a(x_a)|C]` and `bar m^*_C = max_a bar M_{a,C}`. By Lemma 2.8 applied to the family `{M_a : a in [K]}` (each `M_a` depends on the block `x_a` only and is `L`-Lipschitz),
  `E[M_*(X) | C] = E[ max_a M_a(x_a) | C ] <= max_a bar M_{a,C} + L sqrt(d) h_n = bar m^*_C + L sqrt(d) h_n`.
By Lemma 2.7 with `phi := M_* - m_{a,n}` for each `a` (bounded measurable; `M_*` is continuous as a finite maximum of continuous functions),
  `E sum_{t<=n} [ M_*(X_t) - m_{I_t,n}(X_t) ] = sum_C sum_a ( E[M_*|C] - bar M_{a,C} ) E T_a(C;n) <= sum_C [ L sqrt(d) h_n E V_C + sum_a Delta_{a,C} E T_a(C;n) ]`,
using `sum_a E T_a(C;n) = E V_C`. Apply (P1) to each of the `K` agents and then (P2):
  `E sum_t [M_*(X_t) - m_{I_t,n}(X_t)] <= L sqrt(d) n h_n + 4K sqrt(J_n n log n) + 3K min{J_n,n}`,
and `P(n;S^max) = E sum_t m_{I_t,n}(X_t)`. The rate is `O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})` by Step 6 of S4. QED

Note. Only here and in S8 are the capacities assumed Lipschitz; S4, S5, S6 and the whole of S3 do not use it. This matches item 4 of Section 14 of the proof contract: the manuscript's phrase "the intrinsic functions are `L`-Lipschitz" is about `mu_a`, and any statement that needs Lipschitz capacities must say so.

### S8 (C1 (vi), public restricted equilibrium with an explicit uniform rate). COMPLETE.

Claim (Theorem 3(vi)). Assume every `M_a` is `L`-Lipschitz, `M_*(.)` is public, and `nu( { X : |T(X)| >= 2 } ) = 1`. Fix an agent `i` and any deviation `m'_{i,n} in S_HDS` (deterministic map; mixtures at the end). Then
  `u_i(n; m'_{i,n}, S^max_{-i}) - u_i(n; S^max) <= L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 min{J_n,n} = E_n = O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})`.

Proof. Write `T^0` for counts under `S^max` and `T'` for counts under `(m'_{i,n}, S^max_{-i})`; both profiles are in `S_HDS`, so all the grid lemmas apply to both.

Step 1 (utility decomposition by cells). `u_i(n;S) = E[T_i(n) - C_i(n)] = E sum_{t<=n} 1{I_t = i} ( 1 + mu_i(x_{i,t}) - m_{i,n}(X_t) )`. The function `phi_S(X) := 1 + mu_i(x_i) - m_{i,n}(X)` is bounded measurable with values in `[0,2]`, so Lemma 2.7 gives `u_i(n;S) = sum_C a_C(S) E T_i(C;n)` with `a_C(S) := E[ phi_S(X) | C ]`. Put
  `a^0_C := E[ 1 + mu_i(x_i) - M_i(x_i) | C ] >= 0` (pointwise `M_i(x_i) <= 1` and `mu_i(x_i) >= 0`),
  `delta_C := E[ M_i(x_i) - m'_{i,n}(X) | C ] >= 0` (pointwise feasibility `m'_{i,n}(X) <= M_i(x_i)`),
so that `a_C(deviation) = a^0_C + delta_C`.

Step 2 (self-monotonicity removes the baseline term). By S3 Step 3 applied to the pair of profiles `(m'_{i,n}, S^max_{-i})` and `S^max`, which differ only in agent `i` and satisfy `M_i >= m'_{i,n}` pointwise, `E T'_i(C;n) <= E T^0_i(C;n)` for every cell `C`. Hence, cell by cell,
  `gain_C := (a^0_C + delta_C) E T'_i(C;n) - a^0_C E T^0_i(C;n) = a^0_C ( E T'_i(C;n) - E T^0_i(C;n) ) + delta_C E T'_i(C;n) <= delta_C E T'_i(C;n)`,
because `a^0_C >= 0`. Summing, `u_i(n; m'_i, S^max_{-i}) - u_i(n;S^max) = sum_C gain_C <= sum_C delta_C E T'_i(C;n)`.

Step 3 (rival inequality in every positive-mass cell; one Lipschitz step). Fix a cell `C` with `nu(C)>0`. By hypothesis, for `nu`-almost every `X` there are at least two agents attaining `M_*(X)`, so for `nu`-almost every `X` there is some `j != i` with `M_j(x_j) = M_*(X) >= M_i(x_i)`; hence `max_{j != i} M_j(x_j) >= M_i(x_i)` for `nu`-a.e. `X`, and in particular for `nu(.|C)`-a.e. `X`. Taking conditional expectations and then applying Lemma 2.8 to the family `{M_j : j != i}`,
  `bar M_{i,C} <= E[ max_{j != i} M_j(x_j) | C ] <= max_{j != i} bar M_{j,C} + L sqrt(d) h_n`.
Under the deviation, the cell-average means of the instance in `C` are `bar m'_{i,C} = bar M_{i,C} - delta_C` for agent `i` and `bar M_{j,C}` for `j != i`, so agent `i`'s gap to the best arm of that instance satisfies
  `Delta'_{i,C} >= max_{j != i} bar M_{j,C} - bar m'_{i,C} >= bar M_{i,C} - L sqrt(d) h_n - ( bar M_{i,C} - delta_C ) = delta_C - L sqrt(d) h_n`,
and `Delta'_{i,C} >= 0` always, so `Delta'_{i,C} >= ( delta_C - L sqrt(d) h_n )_+`.

Step 4 (per-cell bandit bound and summation). Split `delta_C <= ( delta_C - L sqrt(d) h_n )_+ + L sqrt(d) h_n`. By (P1) applied to the deviated profile with `Delta := (delta_C - L sqrt(d) h_n)_+ <= Delta'_{i,C}`,
  `( delta_C - L sqrt(d) h_n )_+ E T'_i(C;n) <= 4 sqrt( E V_C log n ) + 3 P(V_C >= 1)`.
Summing over cells with (P2), and using `sum_C E T'_i(C;n) = E T'_i(n) <= n` for the residual term,
  `sum_C delta_C E T'_i(C;n) <= 4 sqrt(J_n n log n) + 3 min{J_n,n} + L sqrt(d) n h_n = E_n`.
With Step 2 this proves the claim for a deterministic deviation. The bound does not depend on `m'_{i,n}`, so it is uniform over all deviations in `S_HDS`; for an independent ex ante mixture, condition on the realized map, apply the deterministic bound, and average. Since `E_n = O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)}) = o(n)`, Definition 1 is satisfied and `S^max` is an `S_HDS`-asymptotic equilibrium. QED

Remarks on S8.
1. The publicness of `M_*(.)` is used only to make `S^max` a profile the agents can play: each agent needs to know its own capacity map to play `M_a`, and `M_*` public is what makes the two-top condition meaningful as a public statement. The proof itself uses no information assumption.
2. Where `|T(X)| >= 2` is used: only in Step 3, and only through the `nu`-a.e. inequality `max_{j != i} M_j(x_j) >= M_i(x_i)`. If that inequality fails on a set of positive mass, a unique top agent can shade inside cells where it is uniquely top and keep a positive gap over the runner-up, exactly as in the manuscript's scalar necessity remark in `appendix_public.tex`; our bound then degrades to the trivial `2 E T'_i(n)`.
3. Relative to the manuscript's Theorem `thm:contextual-public` (for Grid-ETC), this statement needs neither a closed `nu`-null set `B`, nor finitely many connected components, nor a constant top set on each component, nor continuity beyond `L`-Lipschitzness; and it gives an explicit uniform rate instead of an unquantified `o(n)` obtained by dominated convergence. In particular the lesson-L1 issue (cell averages converging almost surely) never arises: the argument is a one-step inequality between `bar M_{i,C}` and `max_{j!=i} bar M_{j,C}` in each cell, valid at every finite `n`, with no limit taken inside the proof.
4. Non-top agents need no separate treatment. In the manuscript's Grid-ETC proof, non-top agents are handled by continuity plus dominated convergence; here the single inequality of Step 3 covers every agent `i`, top or not, because a non-top agent `i` has `max_{j != i} M_j(x_j) = M_*(X) >= M_i(x_i)` as well.

## 4. Assumption usage list

For each assumption: where it is used, and what breaks without it.

A1. Known horizon and the index `hat m_a + sqrt(4 log(n)/T_a)` (`[KH]`). Used in: Lemma 2.4(iii) (the execution is a static race), hence in S1(1a), S2(2b), S3 Step 2, S8 Step 2; and in Lemma 2.2 and Corollary 2.3 (the imported bound is for `UCB(delta)` with `delta = 1/n^2`, which is exactly this index). NOT used in: Lemma 2.5, Lemma 2.6, Lemma 2.7, Lemma 2.9, so the cell-average law, the region identity and all label-symmetry statements are index-agnostic. Section 5.2 is the full list, with what fails for the anytime index.

A2. Blindness of the agents in the scalar and finite-context models (an agent does not observe the global round, the other agents' histories, or its own selection times). Used in Lemma 2.4(i) and hence in S1(1a) and in the extension of S1 to behavioral other agents. Without it the other agents' target sequences are not functions of their own pull index alone, and the two coupled executions are no longer races with the same `f_a` for `a != i`.

A3. Fixed ex ante maps (`S_HDS`) in the contextual grid model. Used in Lemma 2.6 (the cell-average mean `bar m_{a,C}` must be a constant, so the map may not depend on the visit index, the phase, or past rewards) and hence everywhere in S3 to S8. This is the manuscript's own restriction; the bait-and-switch objection to phase-dependent contextual strategies applies here verbatim, and no contextual behavioral class is claimed.

A4. Contexts i.i.d. `nu`. Used in Lemma 2.5 (the conditional product form), and hence in Lemma 2.6, Lemma 2.7 and everything downstream; and in `E V_C = n nu(C)` for the boundary accounting of S4 Step 5 and S6 Step 2. NOT used in Theorem 2 (finite contexts), where exogeneity alone suffices.

A5. Exogeneity: the context sequence is independent of all reward uniforms, all priorities and all agent coins, and its law does not depend on the strategy profile. Used in Lemma 2.5, in the conditioning of Theorem 2, and critically in S3 Step 3 (the membership sequence has the SAME law under the two map profiles being compared).

A6. Cell-blind decisions (the exact profile is used only to locate the cell). Used in Lemma 2.6(ii) and Lemma 2.7 (the selection at the `k`-th visit does not look at that visit's exact profile). Without it the region identity `E T_j(C cap R;n) = nu(R|C) E T_j(C;n)` is false in general: a rule that inspects the exact profile can systematically select agent `j` on the `R`-side of a cell.

A7. One priority per instance, drawn uniformly, used at initialization and at every later tie. The fixedness (one draw per instance, no fresh coins) is used in Lemma 2.1 and hence in every monotonicity statement; the uniformity is used in Lemma 2.9 and hence in every FATA statement and in the exactness of Theorem 1(1d) and Theorem 2(2c). The two uses are compatible because monotonicity is proved conditionally on the priority. Section 5.4 shows what fails with per-round fresh tie coins.

A8. `L`-Lipschitz intrinsic means `mu_a` (as functions of the own block `x_a in [0,1]^d`). Used only in S4 Step 3 and S5 (through `b`). Not used in S3 or S6.

A9. `L`-Lipschitz capacities `M_a`. Used only in S7 and in S8 Step 3. The manuscript assumes only continuity of capacities in `thm:contextual-public`; Lipschitzness is what buys the explicit rate, and it must be stated as an added assumption.

A10. Pointwise honesty (`m_{h,n}(X) >= mu_h(x_h)` for honest `h` at every `X`). Used in S2(2a) and S4 Step 3 to get `bar b_C <= bar m^*_C + L sqrt(d) h_n`. Nowhere else.

A11. Two top agents almost everywhere: `nu(|T(X)| >= 2) = 1`. Used only in S8 Step 3. In the finite-context Theorem 2(2e) the corresponding assumption is `|T(z)| >= 2` at every positively visited `z`.

A12. `nu(boundary R) = 0`, respectively `nu(boundary G_ij(R)) = 0`. Used only to convert the exact boundary term `n nu((boundary .)^{sqrt(D) h_n})` into `o(n)` (S4 Step 7, S6 Step 2). All the stated inequalities hold for every measurable region without any boundary hypothesis.

A13. Bernoulli rewards with values in `[0,1]`. Used for 1-subgaussianity in Lemma 2.2 and for the monotone realization `Y = 1{U <= m}` in Lemma 2.4 and Lemma 2.6 (a raise of the target raises the realized reward pathwise at a common uniform). Any family of laws that is stochastically monotone in the target and uniformly subgaussian would do.

A14. `K`, `D = Kd` fixed; `n >= 2`. All constants depend only on `K`, `D`, `L` (the numerical constants `4` and `3` are absolute). No claim is made about the dependence on `D` being optimal.

## 5. Self-audit

### 5.1 Classification of the target statements

S0 static race lemma: COMPLETE (Lemma 2.1).
S1 scalar known-horizon UCB, pathwise monotonicity and SAMF: COMPLETE (Theorem 1, proved in Section 3), including the required remark that the anytime index is not pathwise monotone, which I verified with my own tape (Section 5.3).
S2 finite-context KH-UCB: COMPLETE (Theorem 2), with monotonicity exact and the public part strengthened to a bound uniform over deviations.
S3 grid exact expected monotonicity, including the region identity: COMPLETE (Theorem 3(iii), Lemma 2.7).
S4 grid sharp adaptivity: COMPLETE (Theorem 3(i)), with `L sqrt(d)` in place of `2 L sqrt(D)` and absolute constants `C_1 = 4`, `C_2 = 3`.
S5 grid robustness: COMPLETE as a restatement with explicit constants (Theorem 3(ii)); the manuscript's proof is not redone beyond the two displayed lines.
S6 grid FATA: COMPLETE (Theorem 3(iv)).
S7 revenue at all-maximum play: COMPLETE (Theorem 3(v)).
S8 public equilibrium with an explicit uniform rate: COMPLETE (Theorem 3(vi)).

No target statement was found to be false. Three statements that are NOT proved here and are not claimed anywhere in this file:
(N1) exact EXPECTED monotonicity for a tie-breaking rule that draws a fresh uniform coin every round: OPEN, see 5.4;
(N2) any pathwise monotonicity for Static Grid KH-UCB on the original probability space: not claimed, see the Warning after Lemma 2.6;
(N3) any monotonicity, in expectation, for the anytime index: pathwise monotonicity is FALSE (5.3); whether the expected version survives is OPEN and is not used anywhere here.

### 5.2 Every step where the known-horizon index replaces the anytime index

Flagged `[KH]` in the text. The complete list, with what happens for the manuscript's anytime index `hat m_a + sqrt(2 log t / T_a)`.

(K1) Lemma 2.4(iii): with the known-horizon index the index of arm `a` is `f_a(T_a)`, a function of the arm's own count alone, fixed before play by the tapes; the execution is therefore a static race and Lemma 2.1 applies. FAILS for the anytime index: the index is `f_a(T_a, t)` and, at FIXED counts, the ordering between two arms can reverse as `t` grows, because the common factor `sqrt(2 log t)` multiplies `1/sqrt(T_a)`, which differs across arms. Concretely, Step 1 of Lemma 2.1 (the non-`i` pulls follow a fixed reduced race) is false for the anytime index: in the two coupled executions the `r`-th non-`i` pull occurs at different global rounds, and can be a different arm.

(K2) Consequences of (K1): Theorem 1(1a) (scalar pathwise monotonicity), Theorem 2(2b) (finite-context exact monotonicity), S3 Step 2 (pathwise monotonicity inside the cell-average model) and S8 Step 2 (self-monotonicity of the deviator's own count) all use (K1) and all fail as written for the anytime index. Section 5.3 exhibits a positive-probability sample point on which the scalar conclusion itself, not just the proof, is false for the anytime index.

(K3) Lemma 2.2 and Corollary 2.3: the imported bound is stated and proved for `UCB(delta)` with `delta = 1/n^2`, that is exactly for the index `hat m + sqrt(4 log n / T)`. It does NOT cover `hat m + sqrt(2 log t / T)`, nor does it cover `hat m + sqrt(2 log n / T)` (the known-horizon index with `delta = 1/n`, which is the one used by Esmaeili, Shin and Slivkins; see Section 6). For the anytime index the manuscript's own citation (Auer, Cesa-Bianchi and Fischer) supplies a bound of the same shape, so this is a change of citation and of constants, not a gap. This is why S4, S5 and S7 are not essentially known-horizon results: they would survive, with different constants, for the anytime LOCAL-time cell rule of the manuscript.

(K4) Corollary 2.3(a), the truncation from `s` rounds to `n` rounds: uses that the index does not depend on the length of the run, which is true for both index families. Not an issue.

(K5) Lemma 2.6(ii) and Lemma 2.7: these need only that the selection at the `k`-th visit of a cell does not depend on that visit's exact profile. For the manuscript's local-time anytime rule the selection is still a function of the cell's own history and priority, and for a global-time anytime rule it is a function of the cell's history, the priority and the global round of that visit, which is determined by the membership sequence `Z` and therefore constant under the conditioning used in the proofs. So the cell-average law and the region identity `E T_j(C cap R;n) = nu(R|C) E T_j(C;n)` hold for the anytime index as well. I state this explicitly because it would be wrong to advertise the identity as a benefit of the known-horizon index.

(K6) Lemma 2.9 (label symmetry) and hence Theorem 1(1d), Theorem 2(2c), Theorem 3(iv): equivariance under relabeling holds for both index families. Not an issue.

Summary: the substitution of the known-horizon index is REQUIRED exactly for the monotonicity statements (S1, S2(2b), S3, and through S3 for S8), and is merely convenient elsewhere.

### 5.3 The anytime index is not pathwise monotone: an explicit tape found in this session

Setting: `K = 3`, priority `pi = (1,2,3)` (so initialization pulls 1, 2, 3 and every later tie goes to the smallest label), index `hat m_a + sqrt(2 log(t)/T_a)` with `t` the current round and counts taken before the round, horizon `n = 8`.

Reward tapes (agent by own pull index): `Y_1 = (0,0,...)`, `Y_2 = (0,0,...)`, `Y_3 = (1,1,1,1,0,...)`. Raised tape for agent 1: `Y_1' = (1,0,0,...)`, all other tapes unchanged. This is a pointwise raise.

Execution with `Y_1` (indices rounded to four decimals):
t=1,2,3: initialization, pull 1, 2, 3.
t=4: counts (1,1,1), means (0,0,1), indices (1.6651, 1.6651, 2.6651), pull 3.
t=5: counts (1,1,2), indices (1.7941, 1.7941, 2.2686), pull 3.
t=6: counts (1,1,3), indices (1.8930, 1.8930, 2.0929), pull 3.
t=7: counts (1,1,4), indices (1.9728, 1.9728, 1.9864), pull 3.
t=8: counts (1,1,5), means (0,0,0.8), indices (2.0393, 2.0393, 1.7120), tie between 1 and 2 broken by `pi` toward 1, pull 1.
Final counts (2,1,5).

Execution with `Y_1'`:
t=1,2,3: initialization, pull 1, 2, 3.
t=4: counts (1,1,1), means (1,0,1), indices (2.6651, 1.6651, 2.6651), tie between 1 and 3 broken by `pi` toward 1, pull 1.
t=5: counts (2,1,1), means (0.5,0,1), indices (1.7686, 1.7941, 2.7941), pull 3.
t=6: counts (2,1,2), indices (1.8386, 1.8930, 2.3386), pull 3.
t=7: counts (2,1,3), indices (1.8950, 1.9728, 2.1390), pull 3.
t=8: counts (2,1,4), indices (1.9420, 2.0393, 2.0197), pull 2.
Final counts (2,2,4).

Agent 2's count at `t = 8` rises from 1 to 2 when agent 1's tape is raised: pathwise monotonicity fails for the anytime index. The sample point has positive probability in the model: with fixed means `m_1 < M_1` in `(0,1)`, `m_2, m_3 in (0,1)`, it is the event `{ U_{1,1} in (m_1, M_1], U_{1,2} > M_1, U_{2,1} > m_2, U_{2,2} > m_2, U_{3,k} <= m_3 for k <= 4, U_{3,5} > m_3 }`, whose probability is `(M_1 - m_1)(1-M_1)(1-m_2)^2 m_3^4 (1-m_3) > 0`.

Minimality and honesty about the role of ties. An exhaustive search over all Bernoulli tapes with `K = 3` and a single flipped entry found no counterexample for `n <= 7` and found the above (lexicographically first) one at `n = 8`; a randomized search (300000 instances per `n`, `n <= 16`, arbitrary subsets of flipped entries) found no Bernoulli counterexample in which every post-initialization round has a unique index maximizer. So with Bernoulli rewards the failure I exhibit does pass through a tie resolved by the fixed priority, at `t = 4` in one run and at `t = 8` in the other. The tie is a positive-probability event and the tie-breaking rule is part of the algorithm, so the pathwise claim is false as stated. If one leaves the Bernoulli model and allows rewards in `[0,1]`, the ties disappear: replacing agent 1's first reward by `eps` in the first run (and by 1 in the second) and agent 3's first four rewards by `1 - eps'`, with `eps + eps' < 0.0136`, gives the same two final count vectors (2,1,5) and (2,2,4) with a unique index maximizer at every post-initialization round in both runs (checked numerically for three values of `(eps, eps')`).

Mechanism, stated for the paper. Under the anytime index the comparison between two arms at fixed counts depends on the global round, so an extra pull spent on the raised arm shifts every later comparison; the raised arm "uses up" a round that the other run spent on arm 3, and by round 8 arm 3 has one pull fewer, which lets arm 2 overtake it. Nothing similar can happen under `sqrt(4 log n / T)` because each arm's index sequence is fixed before play (Lemma 2.4(iii)).

### 5.4 Per-round fresh tie coins

What fails in the proof. Both uses of the fixed priority listed after Lemma 2.1 fail: the reduced race of Step 1 is no longer a deterministic sequence (the two runs reach a given tie at different rounds and consume different coins), and the comparison chain of Step 2 no longer compares the two runs through one order.

Counterexample at the level of the static race: Remark 2.1.2.

Counterexample for `KH-UCB` itself, found in this session: `K = 3`, `n = 8`, index `hat m_a + sqrt(4 log 8 / T_a)`, ties broken by a per-round uniform permutation, the SAME coin sequence in both runs (the natural coupling). Coins by round: (1,3,2), (2,3,1), (2,3,1), (3,1,2), (1,2,3), (2,3,1), (3,1,2), (2,1,3), each read as "prefer the first listed agent among the current maximizers". Tapes `Y_1 = (0,0,1,0,0,0,1,0)`, `Y_2 = (0,0,0,1,0,0,0,0)`, `Y_3 = (0,0,0,0,1,0,0,0)`; raised tape `Y_1' = (1,0,1,1,0,0,1,0)`. Round by round the counts after the pull are
run A: (1,0,0), (1,1,0), (1,1,1), (1,1,2), (2,1,2), (2,2,2), (2,2,3), (2,3,3);
run B: (1,0,0), (1,1,0), (1,1,1), (2,1,1), (2,2,1), (2,2,2), (3,2,2), (4,2,2).
At `t = 5`, agent 2's count is 1 in run A and 2 in run B: pathwise monotonicity fails. (The mechanism: at `t = 4` run A has a three-way tie that the coin gives to agent 3, while in run B agent 1 wins outright, after which the two runs face different tie sets at different rounds.)

What is NOT claimed. The lead's brief reports a scout finding that exact EXPECTED monotonicity survives fresh tie coins. I neither prove nor use that statement; it is listed as OPEN in 5.1 (N1). Nothing in this file depends on it, because the algorithm as specified in TASK.md draws one priority per instance, which is enough for monotonicity (pathwise, conditionally on the priority) and, being uniform, also enough for exact FATA (Lemma 2.9).

### 5.5 Rigor notes, caveats and what a referee should check first

1. All conditioning in Sections 2 and 3 is on a discrete random element (`Z`, the context sequence, the realized ex ante maps) or on independent factors of a product space; every conditional-expectation step is therefore an application of Fubini's theorem to independent factors, and no martingale, filtration or nesting argument appears. This is deliberate (lesson L1). In particular no almost sure convergence of cell averages is ever used: the cell-average quantities enter only through one-step inequalities valid at every finite `n` (Lemma 2.8 and S8 Step 3).
2. The one place where a reader may want to slow down is Lemma 2.6(ii): the claim is an equality of conditional LAWS, established by matching one-step conditional distributions, not a pathwise identification. The Warning after that lemma states the consequence for monotonicity, which is the single most dangerous place in this candidate.
3. The imported bound is used only in the form of Corollary 2.3, and only through the product `Delta * E T_a(s)`. I verified the source statement and the relevant display inside its proof myself in this session (Section 6), including that the proof is valid for an arbitrary tie-breaking rule and that it is carried out in the reward-stack model, which is the model we use.
4. Constants. `4` and `3` come from `16 log n` and `3` in (LS) through `min{A,B} <= sqrt(AB)`. If the paper prefers a single symbol, write `C_1 = 4`, `C_2 = 3`, `C_3 = 4`, `C_4 = 3`; they are absolute, and the `K` factors appear only where all arms are summed (S5, S7).
5. Limits of the grid results. They are for `S_HDS` only. Nothing here covers contextual behavioral deviations (the bait-and-switch objection of the manuscript applies unchanged), non-i.i.d. contexts (Lemma 2.5 is false without exchangeability of the within-cell profiles), or cell rules that read the exact profile.
6. Theorem 2's monotonicity needs the finite-context maps to be fixed per exact profile. If an agent used a strategy that depends on its whole own history ACROSS profiles, the per-instance tapes would no longer be static and Lemma 2.1 would not apply; Theorem 2(2b) would fail as written.
7. `h_n` is a deterministic sequence known to the platform; no result uses `L` or `nu` in the choice of `h_n`, only in the constants, as required by the proof contract.
8. I did not attempt any lower bound and make no optimality claim in `D`.

### 5.6 Numerical checks performed in this session

All under `<scratch>/round2/B/c1_prover2/` with the shared venv python; every run took under two minutes on the login node, so no Slurm job was needed and no COMPUTE_LOG entry is required for compute (the scripts are `search.py`, `minimal.py`, `trace.py`, `tiefree.py`, `tiefree_rand.py`, `tiefree_eps.py`, `trace_fresh.py`, `ownct.py`).
1. Randomized search for a pathwise monotonicity violation under `KH-UCB` with one fixed priority: 200000 random instances, `K = 3`, `n = 8`, no violation found. Consistent with Theorem 1(1a), which proves there is none.
2. Anytime index, fixed priority: violations found for both conventions `sqrt(2 log t/T)` and `sqrt(2 log(t-1)/T)`; the exhaustive minimal example is in 5.3.
3. `KH-UCB` with per-round fresh tie coins: violation found, reported in 5.4.
4. Tie-free variants: no Bernoulli tie-free counterexample for the anytime index in 300000 instances per `n` up to `n = 16`; a `[0,1]`-valued tie-free counterexample exists (5.3).
5. Own-count direction under the anytime index: in 200000 random instances per `n` in {6,8,10,12} the raised agent's own count never decreased. This is an OBSERVATION, not a claim; nothing here relies on it. It does indicate that the anytime failure mode is about the OTHER agents' counts, which is precisely the property the monotonicity axiom needs.

### 5.7 Downstream consequences for the manuscript if this candidate is adopted

1. The algorithm changes. The manuscript's Section "Stochastic SAMF and scalar UCB" specifies `hat m_i + sqrt(2 log t / T_i)` with independent uniform tie-breaking each round; C0 and C1 require `hat m_i + sqrt(4 log n / T_i)` and one uniform priority per instance, drawn once. Both changes are needed: Section 5.3 kills the first, Section 5.4 kills the second (for the pathwise conclusion).
2. The scalar theorem becomes horizon-dependent. The manuscript's scalar rule is anytime; `KH-UCB` needs `n`. The contextual results are already fixed-horizon, so only Section 3 of the paper changes character.
3. The experiment code (per the proof contract, `CellUCB` uses the local visit count inside the logarithm and breaks ties toward the lowest label) no longer matches the analyzed algorithm. Either the code is changed to the known-horizon index with a per-cell uniform priority, or the paper must say plainly that the experiments run a different, anytime variant for which only robustness is proved.
4. The gains are substantial and should be stated: Static Grid KH-UCB becomes a full contextual SAMF mechanism at rate `n^{(D+1)/(D+2)} (log n)^{1/(D+2)}`, strictly better than Grid-ETC's `n^{(D+2)/(D+3)}`, with exact (zero remainder) monotonicity, with FATA, with a revenue guarantee, and with a public equilibrium whose deviation bound is uniform over `S_HDS` and does not need the closed null set `B`, the finitely many components, or the constant top set per component. That last point removes the assumption the manuscript itself flags as "not implied by continuity".
5. Attribution. The known-horizon index plus a static-race argument is prior art (Section 6). The paper must cite it when it switches index, and should present the contribution as the contextual grid consequences (S3 to S8), not as the scalar monotonicity lemma.

## 6. Verified references with URLs

All checks were made on 17 September 2026 in this session. "Fetched" means I retrieved the document myself and read the cited passage; "listed" means the item appeared in a search result listing and I did not open it.

R1. Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, free online edition (content identical to the Cambridge University Press print edition, page numbers differ). Fetched: https://tor-lattimore.com/downloads/book/book.pdf (5.4 MB PDF, downloaded and converted to text with ghostscript). Read and used:
  - Algorithm 3 `UCB(delta)` and display (7.2) for the index, with the `+infinity` convention when `T_i(t-1) = 0`, on the page whose running header is "7.1 The Optimism Principle 103".
  - Theorem 7.1, on the page headed "7.1 The Optimism Principle 105": "Consider UCB as shown in Algorithm 3 on a stochastic k-armed 1-subgaussian bandit problem. For any horizon n, if delta = 1/n^2, then R_n <= 3 sum_{i=1}^k Delta_i + sum_{i : Delta_i > 0} 16 log(n)/Delta_i."
  - The display `E[T_i(n)] <= 3 + 16 log(n)/Delta_i^2` inside the proof of Theorem 7.1, on the page headed "7.1 The Optimism Principle 108". This is the inequality imported as (LS) in Lemma 2.2.
  - Theorem 7.2 on the same page: `R_n <= 8 sqrt(n k log(n)) + 3 sum_i Delta_i`, proved from the same display.
  - Section 4.6, reward-stack model, on the page headed "4.7 The Canonical Bandit Model for Uncountable Action Sets 66": "let X_t = X_{T_{A_t}(t), A_t}. This corresponds to sampling a stack of rewards for each arm at the beginning of the game". The proof of Theorem 7.1 states that it uses this model ("We make use of the third model in Section 4.6").
  I also checked in the proof text that tie-breaking is never used beyond "A_t is a maximizer of the index", which is what licenses the fixed-priority rule of `KH-UCB`.

R2. Seyed A. Esmaeili, Suho Shin, Aleksandrs Slivkins, "Robust and Performance Incentivizing Algorithms for Multi-Armed Bandits with Strategic Agents", arXiv:2312.07929; AAAI 2025 proceedings entry listed at https://ojs.aaai.org/index.php/AAAI/article/view/33510 (volume 39, issue 13, pages 13814 to 13822, per the search listing; not opened). Fetched: https://arxiv.org/abs/2312.07929 (metadata) and https://arxiv.org/html/2312.07929 (full text, read through the fetch tool). Verified there: their Definition 5.2 states monotonicity PATHWISE, "for any reward seed and any strategy seed, for all j != i: T_j(n, S_i^*, S_{-i}) <= T_j(n, S_i, S_{-i})"; their Fact B.10 records the stochastic dominance and expectation consequences; their Algorithm 3 pulls the arm with the highest `hat mu_i(t-1) + sqrt(2 ln(n) / T_i(t-1))`, with `n` the KNOWN horizon. Two points for the paper: (a) this is prior art for the known-horizon substitution and for the pathwise monotonicity property, and it must be cited when the index is changed; (b) their confidence width is `sqrt(2 ln n / T)`, that is `delta = 1/n` in the parametrization of R1, so the bound (LS), which needs `delta = 1/n^2`, does not apply verbatim to their index; TASK.md's `KH-UCB` uses `sqrt(4 log n / T)` and is the one covered by R1. I did not locate a "Theorem B.11" or "Claim B.12" by those numbers in the fetched HTML and do not rely on them.

R3. Zhe Feng, David C. Parkes, Haifeng Xu, "The Intrinsic Robustness of Stochastic Bandits to Strategic Manipulation", ICML 2020 (PMLR volume 119, pages 3092 to 3101, per the search listing at https://proceedings.mlr.press/v119/feng20c.html, listed, not opened). Fetched: https://arxiv.org/abs/1906.01528 and the full PDF https://arxiv.org/pdf/1906.01528, which I converted to text and read directly. Verified there:
  - their UCB uses the KNOWN horizon: `I_t = argmax_i { hat mu_i(t-1) + 3 sigma sqrt( ln T / n_i(t-1) ) + beta^{(i)}_{t-1}/n_i(t-1) }`, and their footnote 3 explicitly contrasts "a UCB variant that uses time-dependent confidence width `3 sigma sqrt( ln t / n_i(t-1) )`";
  - Lemma B.2: "Suppose t >= K and the principal runs UCB algorithm. Let Z^{LSI}_{t:t'}(-i) [resp. Z^{S(i)}_{t:t'}(-i)] denote the subsequence of Z^{LSI}_{t:t'} [resp. Z^{S(i)}_{t:t'}] after deleting all i's in the sequence. Then given any history h_{t-1} and time t, under Arm Coupling, either Z^{LSI}_{t:t'}(-i) is a subsequence of Z^{S(i)}_{t:t'}(-i) or vice versa."
  - Lemma B.3: "When the principal runs UCB algorithm, under Arm Coupling, given any history h_{t-1} and time t, we have n_i^{LSI}(t:T) >= n_i^{S(i)}(t:T) with probability 1 for any investment strategy S and T >= t >= K."
  These are the prefix/subsequence route to S0 that TASK.md attributes to them, for a known-horizon index; the attribution is accurate. My Lemma 2.1 is a strengthening in two respects: the non-`i` pull sequence is identified exactly with a single deterministic reduced race (rather than only being comparable by inclusion), and the conclusion `T_j' <= T_j` for all `j != 1` is obtained for arbitrary extended-real index sequences with no structure at all.

R4. Not relied upon and therefore not verified in this session: Auer, Cesa-Bianchi and Fischer (2002), which the manuscript cites for its anytime UCB1 bounds. Every bandit bound used in this file comes from R1.
