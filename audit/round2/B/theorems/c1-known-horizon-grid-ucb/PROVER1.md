# PROVER1: Task C1 + C0 (known-horizon UCB, exact monotonicity, Static Grid KH-UCB)

Prover 1, 17 September 2026. Notation as in `audit/round2/B/CONTEXT_PROOF_CONTRACT.md`.
No Unicode em dashes and no LaTeX triple hyphens are used anywhere in this file.
`log` is natural, `[K] = {1,...,K}`, `(x)_+ = max(x,0)`, `1{.}` is an indicator.
Everything below was proved by me in this session; where I rely on an external source I state the
exact imported inequality, its hypotheses, and the page I read (Section 6).

## 0. Status line

STATUS: COMPLETE (all target statements closed).

| target | statement | classification |
|:-|:-|:-|
| S0 | static race lemma, fixed strict priority | PROVED (Theorem 2.3) |
| S1 | scalar KH-UCB: pathwise exact monotonicity, sharp adaptivity, exact FATA | PROVED: Theorem A, proved in Section 3.1; anytime counterexample re-verified in Section 3.3 |
| S2 | Finite-Context KH-UCB, monotonicity exact for every `R subseteq X_F` | PROVED: Theorem B, proved in Section 3.4 |
| S3 | grid exact expected monotonicity, every measurable `R`, zero remainder | PROVED: Theorem C(iii), proved in Section 3.6; pathwise version under the actual-visit coupling NOT CLAIMED |
| S4 | grid contextual sharp adaptivity with explicit remainder | PROVED: Theorem C(i), proved in Section 3.7 |
| S5 | grid robustness, restated with explicit constants | PROVED: Theorem C(ii), restated in Section 3.8 |
| S6 | grid expected FATA with boundary remainder | PROVED: Theorem C(iv), proved in Section 3.9 |
| S7 | grid revenue at all-maximum play, Lipschitz capacities | PROVED: Theorem C(v), proved in Section 3.10 |
| S8 | grid public restricted equilibrium, two-top a.e., explicit rate | PROVED: Theorem C(vi), proved in Section 3.11 |

Improvements over the target statements that I prove and recommend adopting:
(a) the Lipschitz bias constant is `L sqrt(d)`, not `2 L sqrt(D)`, in S4, S5, S7 (lesson L2 applied in
its one-step form); in S8 the constant is `2 L sqrt(d)`, and the factor 2 there is genuinely needed;
(b) the deficit constants are absolute (`C_1 = 4`, `C_2 = 3`), not merely `K`-dependent, in S4 and S8;
the gap-free constants are `8 sqrt(K)` and `3K` in S5 and S7;
(c) the per-cell split is `min{s Delta, 16 log n / Delta + 3 Delta} <= 4 sqrt(s log n) + 3`, a factor 2
better than the `8 sqrt(s log n) + 3` in TASK.md;
(d) S2's finite-context monotonicity is exact AND pathwise conditional on the arrival sequence, and the
finite-context public equilibrium gain admits the deviation-uniform rate `4 sqrt(Q n log n) + 3 Q`,
which the manuscript's `o(n)` statement does not (it is explicitly non-uniform there).

Three things I do NOT claim, stated here so they cannot be read into the proofs:
1. Pathwise contextual monotonicity for Static Grid KH-UCB under the actual-visit coupling. My proof of
S3 is an equality-in-law argument through an auxiliary own-count tape model, so it delivers exact
EXPECTED monotonicity only. Section 3.6.3 explains precisely why pointwise feasibility does not give
pathwise domination there, and I give no counterexample either, so the pathwise statement is OPEN.
2. Anything about the manuscript's anytime index `hat m + sqrt(2 log t / T)`. Section 3.12 lists every
step that fails for it; the pathwise monotonicity of anytime UCB1 is FALSE (tape re-verified in this
session) and its exact expected monotonicity is OPEN.
3. Minimax optimality in `D` of any rate below.

## 1. Exact theorem statements, ready for the paper

### 1.0 The algorithms, fixed once and for all

Throughout, `n >= 2` is the horizon, known to the platform before play.

**KH-UCB(n, pi)** (scalar, known horizon, one ex ante priority). A permutation `pi` of `[K]` is drawn
once before play, uniformly at random and independently of everything else. Write `T_a` for agent `a`'s
current number of selections and `hat m_a` for its empirical mean of realized rewards. At each round:
if some agent has `T_a = 0`, select the `pi`-first such agent; otherwise select the agent maximizing
the index
```
  f_a := hat m_a + sqrt(4 log n / T_a),
```
ties broken by `pi` (the `pi`-first agent among the maximizers). Equivalently, the index is `+infinity`
at `T_a = 0` and the rule is: select the lexicographic maximizer of `(f_a, pi-rank of a)`. The same `pi`
is used for the initialization and for every later tie. This is `UCB(delta)` of Lattimore and
Szepesvari (Bandit Algorithms, Algorithm 3, page 103) with `delta = 1/n^2`, since
`sqrt(2 log(1/delta) / T_a) = sqrt(4 log n / T_a)`.

**Finite-Context KH-UCB.** One independent KH-UCB(n, pi_z) instance per exact profile `z in X_F`, with
the GLOBAL `n` in the logarithm and its own priority `pi_z` drawn independently and uniformly; local
time is the instance's own visit count; no statistics are shared across profiles.

**Static Grid KH-UCB(n).** Let
```
  h_n := (log(en)/n)^{1/(D+2)},   N_n := ceil(1/h_n),   J_n := N_n^D .
```
Partition `X = [0,1]^D` into the `J_n` cells
`C_v := prod_{l=1}^D I_{v_l}`, `v in {0,...,N_n-1}^D`, where `I_j := [j h_n, (j+1) h_n)` for
`j < N_n - 1` and `I_{N_n-1} := [(N_n-1) h_n, 1]`. This is a genuine partition of `[0,1]^D`, every cell
is convex, `diam(C) <= sqrt(D) h_n` in the Euclidean norm, and every agent block `x_a in [0,1]^d` varies
by at most `sqrt(d) h_n` inside a cell. Each cell carries an independent KH-UCB(n, pi_C) instance,
initialized lazily at the cell's first visit, using the GLOBAL `n` in the logarithm, its own local
counts `T_{a,C}` and empirical means, and its own uniform priority `pi_C` drawn before play. Decisions
are cell blind: the exact profile is used only to locate the cell.

(Remark on the partition. The manuscript and TASK.md write the partition of `[0,1)^D`; taking the last
interval in each coordinate closed, as above, covers the face `{x_l = 1}` and changes nothing else. This
is the only change I make to the stated algorithm.)

### 1.1 Scalar (task C0, target S1)

**Theorem A (scalar KH-UCB is stochastic SAMF, with exact pathwise monotonicity).**
Fix `K >= 2` and `n >= 2` and run KH-UCB(n, pi). Realize rewards by the own-count tape coupling: seeds
`U_{a,r}`, `a in [K]`, `r in [n]`, i.i.d. uniform on `[0,1]`, independent of `pi`, and the reward at
agent `a`'s `r`-th selection is `Y_{a,r} = 1{U_{a,r} <= m_{a,r}}`, where `m_{a,r}` is the target chosen
at that selection. Then:

(i) (Exact pathwise monotonicity.) Let agent `i` use any strategy whose realized targets satisfy
`m_{i,r} <= M_i` for all `r` (in particular any fixed mean `m_i in [0,M_i]`, any horizon-dependent fixed
mean, and any blind behavioral strategy in `B_{i,n}`), and let every other agent use an arbitrary blind
behavioral strategy in `B_{j,n}`. Let `T_a(t)` be the counts under this profile and `T_a^{i up}(t)` the
counts when agent `i` is replaced by the constant target `M_i`, all other agents' strategies, all seeds
`U_{a,r}`, all private coins and `pi` held fixed. Then on EVERY sample point, for every `t <= n`
simultaneously,
```
  T_j^{i up}(t) <= T_j(t)   for every j != i,       T_i^{i up}(t) >= T_i(t).
```
In particular the stochastic monotonicity remainder is zero, for every `n`, uniformly over profiles.

(ii) (Sharp adaptivity.) For every profile in `S_HI` (and, more generally, for every profile of
horizon-dependent fixed means), every agent `i` and every `n >= 2`,
```
  E C_i(n) >= (mu_H^* - mu_i) E T_i(n) - (4 sqrt(n log n) + 3).
```

(iii) (Robustness.) For every such profile, `P(n) >= mu_H^* n - 8 sqrt(K n log n) - 3K`.

(iv) (Exact expected FATA.) If agents `i` and `j` have the same delivered reward law (for fixed means:
`m_i = m_j`), then `E T_i(n) = E T_j(n)` exactly, for every `n`.

**Theorem A' (public scalar equilibrium, deviation-uniform).** Assume `K_top >= 2` and run KH-UCB(n,pi)
with `S^max` (every agent delivers `M_a`). Then for every agent `i` and every deviation `m_i' in [0,M_i]`,
```
  u_i(n; m_i', S^max_{-i}) - u_i(n; S^max) <= 4 sqrt(n log n) + 3,
```
and `P(n; S^max) >= M_top n - 8 sqrt(K n log n) - 3K`. (The manuscript's `thm:public-ucb` gives `o(n)`
with a constant that blows up as the deviation gap vanishes; the bound here is uniform over deviations.)

### 1.2 Finite contexts (task C0, target S2)

**Theorem B (Finite-Context KH-UCB).** Assume arrivals `X_t in X_F = {z_1,...,z_Q}` are exogenous and
independent of all reward seeds and of all priorities (they need not be i.i.d.), and that all agents use
deterministic maps in `S_F` (horizon-dependent maps are allowed; independent ex ante mixtures follow by
conditioning). Then for every `n >= 2`:

(i) (Contextual sharp adaptivity.) For every `R subseteq X_F` and every agent `i`,
```
  E sum_{t<=n} 1{X_t in R, I_t = i} c_{i,t}
   >= E sum_{t<=n} 1{X_t in R, I_t = i} [b(X_t) - mu_i(x_{i,t})] - (4 sqrt(|R| n log n) + 3|R|).
```

(ii) (Contextual monotonicity, exact AND pathwise.) Fix `i != j` and `R subseteq X_F`, write
`T_j(R;n)` for the count under the profile `(m_i, m_{-i})` and `T_j^{i up}(R;n)` for the count under
`(M_i, m_{-i})`. Conditional on the whole arrival sequence, and on every sample point of the
per-profile own-count tape coupling, `T_j^{i up}(R;n) <= T_j(R;n)`; hence `E T_j^{i up}(R;n) <= E T_j(R;n)`
with zero remainder, for every `n`.

(iii) (Exact expected FATA.) If `m_i(z) = m_j(z) = M_*(z)` for every `z in G_{ij}(R)`, then
`E T_i(G_{ij}(R);n) = E T_j(G_{ij}(R);n)` exactly.

(iv) (Robustness.) `P(n) >= E sum_{t<=n} b(X_t) - 8 sqrt(K Q n log n) - 3 K Q`.

(v) (Public equilibrium.) If in addition `|T(z)| >= 2` for every `z in X_F` and `M_*(.)` is public, then
under `S^max` every unilateral deviation `m_i' in S_F` by any agent `i` satisfies
```
  u_i(n; m_i', S^max_{-i}) - u_i(n; S^max) <= 4 sqrt(Q n log n) + 3 Q,
```
uniformly over deviations, and
`P(n; S^max) >= E sum_{t<=n} M_*(X_t) - 8 sqrt(K Q n log n) - 3 K Q`. If moreover the arrivals are
i.i.d. with fixed positive masses and all capacity gaps `M_*(z) - M_k(z_k)` of non-top agents are fixed
and positive, the revenue bound improves to
`P(n; S^max) >= E sum_t M_*(X_t) - sum_{z} sum_{k not in T(z)} (3 (M_*(z)-M_k(z_k)) + 16 log n/(M_*(z)-M_k(z_k))) = E sum_t M_*(X_t) - O(log n)`,
with a constant depending on those gaps.

### 1.3 Continuous contexts, Static Grid KH-UCB (task C1, targets S3 to S8)

Standing assumptions for Theorem C: `X = [0,1]^D`, `D = Kd`, profiles `X_t` i.i.d. `nu` and exogenous
(independent of all reward seeds, all priorities `pi_C` and all agents' private coins); all agents use
maps in `S_HDS`, that is measurable `m_{a,n} : X -> [0, M_a(x_a)]` fixed before play, possibly randomized
independently ex ante; the platform runs Static Grid KH-UCB(n). Constants below are absolute or depend
only on `K, D, L` as indicated.

**Theorem C (Static Grid KH-UCB is contextual SAMF at exponent `(D+1)/(D+2)`).** For every `n >= 2`:

(i) (Contextual sharp adaptivity; needs `mu_a` `L`-Lipschitz for every `a`.) For every agent `i` and
EVERY measurable `R subseteq X`, uniformly over `S_HDS`,
```
  E sum_{t<=n} 1{X_t in R, I_t = i} c_{i,t}
   >= E sum_{t<=n} 1{X_t in R, I_t = i} [b(X_t) - mu_i(x_{i,t})]
      - [ L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 J_n + n nu((partial R)^{sqrt(D) h_n}) ].
```
The first three terms are at most
`(L sqrt(d) + 4 . 2^{D/2} + 3 . 2^D) n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`.

(ii) (Global robustness; same hypothesis.) Uniformly over `S_HDS`,
```
  P(n) >= E sum_{t<=n} b(X_t) - [ L sqrt(d) n h_n + 8 sqrt(K J_n n log n) + 3 K J_n ]
       >= E sum_{t<=n} b(X_t) - (L sqrt(d) + 8 sqrt(K) 2^{D/2} + 3 K 2^D) n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}.
```

(iii) (Exact expected contextual monotonicity; no regularity, no boundary condition.) For every map
profile in `S_HDS`, every `i != j`, every `n`, and EVERY measurable `R subseteq X`, replacing `m_{i,n}`
pointwise by `M_i` gives
```
  E T_j(R;n) under (M_i, m_{-i,n})  <=  E T_j(R;n) under (m_{i,n}, m_{-i,n}),
```
with zero remainder. Moreover `E T_i(R;n)` does not decrease. The same holds when ties inside a cell are
broken by fresh per-round uniform coins instead of `pi_C` (Proposition 2.6).

(iv) (Expected contextual FATA.) If `m_{i,n}(X) = m_{j,n}(X) = M_*(X)` for every `X in G := G_{ij}(R)`,
then for every `n`,
```
  | E T_i(G;n) - E T_j(G;n) | <= n nu((partial G)^{sqrt(D) h_n}),
```
which is `o(n)` whenever `nu(partial G) = 0`.

(v) (Revenue at all-maximum play; needs `M_a` `L`-Lipschitz for every `a`.) Under `S^max`,
```
  P(n; S^max) >= E sum_{t<=n} M_*(X_t) - [ L sqrt(d) n h_n + 8 sqrt(K J_n n log n) + 3 K J_n ].
```

(vi) (Public restricted equilibrium; needs `M_a` `L`-Lipschitz for every `a` and
`nu(|T(X)| >= 2) = 1`.) Under `S^max`, for every agent `i` and every unilateral deviation
`m'_{i,n} in S_HDS` (deterministic, or an independent ex ante mixture of such maps),
```
  u_i(n; m'_{i,n}, S^max_{-i}) - u_i(n; S^max)
     <= 4 sqrt(J_n n log n) + 3 J_n + 2 L sqrt(d) n h_n
      = O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)}),
```
with the explicit constant `(2 L sqrt(d) + 4 . 2^{D/2} + 3 . 2^D)`. Hence `S^max` is an
`S_HDS`-asymptotic equilibrium, with a rate that is uniform over deviations.

No claim of minimax optimality in `D` is made for any of these rates.

## 2. Lemmas, with complete proofs

### 2.1 The static race lemma (target S0)

**Setting.** Let `(V, <=)` be a totally ordered set; in all applications `V = [-infinity, +infinity]`.
For each arm `a in [K]` let `f_a : {0,1,2,...} -> V` be an arbitrary function; NO monotonicity of
`f_a` in its argument is assumed. Let `succ` be a strict total order on `[K]` (the priority). Order
pairs in `V x [K]` lexicographically: `(v,a) > (w,b)` iff `v > w`, or `v = w` and `a succ b`. Because
priorities are strict and distinct, two pairs with different arm labels are never equal, so this is a
strict total order on the `K` pairs available at any state.

The greedy merge `G(f)` is the sequence `(I_t)_{t>=1}` defined by `T_a(0) = 0` and, at step `t >= 1`,
```
  I_t := the unique argmax over a in [K] of the pair (f_a(T_a(t-1)), a),
  T_a(t) := T_a(t-1) + 1{I_t = a}.
```
A finite horizon `n` is the restriction to `t <= n`; only the values `f_a(k)` with `k <= n-1` matter
there, and the horizon-`n` run is the length-`n` prefix of the infinite run, because the rule is a step
by step recursion.

Define the running minimum (the envelope) `e_a(k) := min_{0 <= k' <= k} f_a(k')`. It is nonincreasing in
`k` and satisfies `e_a <= f_a` pointwise. The minimum of a finite subset of a totally ordered set exists.

**Lemma 2.1 (envelope identity).** For every family `(f_a)_{a in [K]}` and every fixed priority `succ`,
the greedy merges on `(f_a)` and on `(e_a)` coincide step by step: `G(f) = G(e)`.

*Proof.* Induction on `t`. Suppose the two merges agree on steps `1,...,t-1`; then at the start of step
`t` they are in the same state `T = (T_a)_{a in [K]}` (the empty hypothesis when `t = 1`, where
`T = 0`). Let `a^*` be the arm that `G(f)` pulls at step `t`. It suffices to prove
```
  (e_{a^*}(T_{a^*}), a^*) > (e_b(T_b), b)   for every b != a^*,          (2.1)
```
because then `G(e)` also pulls `a^*` at step `t`.

Fix `b != a^*`. Choose `k <= T_{a^*}` attaining the envelope: if `f_{a^*}(T_{a^*}) = e_{a^*}(T_{a^*})`
take `k := T_{a^*}`; otherwise take any `k < T_{a^*}` with `f_{a^*}(k) = e_{a^*}(T_{a^*})` (such a `k`
exists by definition of the running minimum).

Case 1: `k = T_{a^*}`. The greedy choice at step `t` gives
`(f_{a^*}(T_{a^*}), a^*) > (f_b(T_b), b)`. Since `e_b(T_b) <= f_b(T_b)`, we get
`e_b(T_b) <= f_b(T_b) <= f_{a^*}(T_{a^*}) = e_{a^*}(T_{a^*})`. If `e_b(T_b) < e_{a^*}(T_{a^*})` then
(2.1) holds. If `e_b(T_b) = e_{a^*}(T_{a^*})` then the chain of inequalities is an equality chain, so
`f_b(T_b) = f_{a^*}(T_{a^*})`, and then the greedy choice at step `t` forces `a^* succ b`, so (2.1)
holds again.

Case 2: `k < T_{a^*}`. Since `T_{a^*}(0) = 0` and the count of `a^*` increases by exactly one at each of
its pulls, arm `a^*` was pulled at some step `s < t` at which its count was `k`, that is
`T_{a^*}(s-1) = k`. By the induction hypothesis, step `s` is a step of both merges and the state at its
start is the same in both. The greedy choice at step `s` gives
`(f_{a^*}(k), a^*) > (f_b(T_b(s-1)), b)`. Counts are nondecreasing in `t`, so
`T_b(s-1) <= T_b(t-1) = T_b`, whence `e_b(T_b) = min_{k' <= T_b} f_b(k') <= f_b(T_b(s-1))`. Therefore
```
  e_b(T_b) <= f_b(T_b(s-1)) <= f_{a^*}(k) = e_{a^*}(T_{a^*}).
```
If the outer inequality is strict, (2.1) holds. If it is an equality, then
`f_b(T_b(s-1)) = f_{a^*}(k)` and the greedy choice at step `s` forces `a^* succ b`, so (2.1) holds.

In both cases `G(e)` pulls `a^*` at step `t`, which completes the induction. QED

**Lemma 2.2 (sorted-order characterization for nonincreasing sequences).** Assume every `e_a` is
nonincreasing. For `v in V`, `j in [K]` and `a != j` put
```
  N_a(v,j) := #{ k' >= 0 : (e_a(k'), a) > (v, j) }  in {0,1,2,...} union {+infinity}.
```
Let `tau_j(k)` be the step at which `G(e)` pulls arm `j` for the `k`-th time, with `tau_j(k) := +infinity`
if that pull never occurs. Then for every `j` and every `k >= 1`,
```
  tau_j(k) = k + sum_{a != j} N_a(e_j(k-1), j),                                   (2.2)
```
with the convention that the right side is `+infinity` as soon as one summand is.

*Proof.* Because `e_a` is nonincreasing, the set `{k' : (e_a(k'),a) > (v,j)}` is an initial segment
`{0,...,N_a(v,j)-1}` of the nonnegative integers (if `(e_a(k'),a) > (v,j)` and `k'' < k'` then
`e_a(k'') >= e_a(k')` so `(e_a(k''),a) >= (e_a(k'),a) > (v,j)`).

(a) *The pulled pairs are nonincreasing along the run.* Let `P_t := (e_{I_t}(T_{I_t}(t-1)), I_t)` be the
pair of the arm pulled at step `t`, which is the maximum of the `K` current pairs at step `t`. At step
`t+1` the only current pair that changed is that of `I_t`, which became
`(e_{I_t}(T_{I_t}(t-1)+1), I_t) <= P_t` because `e_{I_t}` is nonincreasing and the label is unchanged.
Every other current pair was already `< P_t`. Hence `P_{t+1} <= P_t`.

(b) *Exact count of the other arms' pulls before `tau_j(k)`.* Write `v := e_j(k-1)`. Assume
`tau := tau_j(k) < +infinity`. At step `tau`, arm `j` has count `k-1`, so its current pair is `(v,j)`,
and `P_tau = (v,j)`. Let `a != j` and let `r` be the number of pulls of `a` at steps `s < tau`. Each such
pull has pair `P_s >= P_tau = (v,j)` by (a), and `P_s != (v,j)` because the labels differ, so
`P_s > (v,j)`; the counts of `a` used at its successive pulls are `0,1,...,r-1`, so
`(e_a(k'),a) > (v,j)` for all `k' <= r-1`, whence `r <= N_a(v,j)`. Conversely, if `r < N_a(v,j)`, then
at step `tau` arm `a`'s current pair is `(e_a(r), a) > (v,j)`, contradicting the greedy choice of `j` at
step `tau`. Hence `r = N_a(v,j)` exactly. Since `j` is pulled exactly `k-1` times before `tau`,
`tau = 1 + (k-1) + sum_{a != j} N_a(v,j)`, which is (2.2).

(c) *If some `N_a(v,j) = +infinity` then `tau_j(k) = +infinity`.* Immediate from (b): a finite `tau`
would force `N_a(v,j)` pulls of `a` before step `tau`, impossible if that number is infinite.

(d) *If all `N_a(v,j)` are finite then `tau_j(k) < +infinity`.* Suppose not, and let `k^* <= k-1` be the
total number of pulls arm `j` ever receives (finite by assumption). For all sufficiently large `t`,
`T_j(t) = k^*`, so `j`'s current pair is `(w, j)` with `w := e_j(k^*) >= e_j(k-1) = v` (envelopes are
nonincreasing and `k^* <= k-1`). Since the run is infinite and `j` is pulled finitely often, some
`a != j` is pulled at infinitely many steps `s` with `T_j(s-1) = k^*`; at each such step the greedy
choice gives `(e_a(T_a(s-1)), a) > (w, j) >= (v, j)`, and the counts `T_a(s-1)` are pairwise distinct
across those steps. Hence `N_a(v,j) = +infinity`, a contradiction. QED

**Theorem 2.3 (S0: static race monotonicity).** Let `(f_a)_{a in [K]}` be arbitrary, let `succ` be a
fixed strict priority, and let `f_1'(k) >= f_1(k)` for every `k >= 0`, with `f_a' = f_a` for every
`a != 1`. Let `T_a(t)` and `T_a'(t)` be the counts of `G(f)` and `G(f')`. Then for every `j != 1` and
every `t >= 1`,
```
  T_j'(t) <= T_j(t),     and consequently    T_1'(t) >= T_1(t).
```

*Proof.* By Lemma 2.1, `G(f) = G(e)` and `G(f') = G(e')`, where
`e_1'(k) = min_{k'<=k} f_1'(k') >= min_{k'<=k} f_1(k') = e_1(k)` for every `k`, and `e_a' = e_a` for
`a != 1`. All envelopes are nonincreasing, so Lemma 2.2 applies to both merges.

Fix `j != 1` and `k >= 1`, and put `v := e_j(k-1) = e_j'(k-1)` (equal because `j != 1`). For
`a not in {1,j}`, `N_a'(v,j) = N_a(v,j)`. For `a = 1`, if `(e_1(k'),1) > (v,j)` then
`(e_1'(k'),1) >= (e_1(k'),1) > (v,j)`, so the defining set for `N_1'` contains that for `N_1` and
`N_1'(v,j) >= N_1(v,j)`. By (2.2), `tau_j'(k) >= tau_j(k)` for every `k >= 1`, including the case where
one or both sides are `+infinity`. Therefore
```
  T_j'(t) = #{k >= 1 : tau_j'(k) <= t} <= #{k >= 1 : tau_j(k) <= t} = T_j(t).
```
Finally `T_1'(t) = t - sum_{j != 1} T_j'(t) >= t - sum_{j != 1} T_j(t) = T_1(t). QED

**How the fixed priority is used, exactly.** In three places, all essential.
(1) It makes the argmax unique, so both merges are deterministic functions of `(f_a)` and the greedy
recursion is well defined. (2) In Lemma 2.1, Cases 1 and 2, the equality subcase is resolved by the
SAME order `succ` at step `t` and at the earlier step `s`; nothing would let us conclude if the tie at
step `s` had been resolved by a coin that is no longer available at step `t`. (3) In Lemma 2.2(b), the
strictness `P_s > (v,j)` for `s < tau` uses that pairs with distinct labels are never equal, which is
exactly the statement that the priority is a strict total order. If ties are instead broken by fresh
per-round coins, the conclusion is FALSE pathwise; see Proposition 2.6 and the tape in Section 2.6.

**Remark 2.3.1 (what Theorem 2.3 does not need).** No monotonicity of `f_a` in `k`; no finiteness of the
values (`+infinity` and `-infinity` are allowed, which is how count-zero initialization is encoded); no
bound on `K`; no relation between arms. The statement is simultaneous over all `t`.

**Prior work.** The same conclusion for known-horizon UCB is in Feng, Parkes and Xu (ICML 2020, arXiv
1906.01528), Lemmas B.2 and B.3, and in Esmaeili, Shin and Slivkins (AAAI 2025, arXiv 2312.07929),
Theorem B.11 and Claim B.12, both by a prefix argument; see Section 6. The proof above is written out in
full here because the paper needs it for arbitrary, non-monotone index sequences and with the tie rule
made explicit, and because requirement 3 of TASK.md asks for the tie analysis.

**Corollary 2.4 (KH-UCB with one ex ante priority is pathwise monotone).** Fix `K`, `n >= 2`, any
deterministic bonus function `beta : {1,2,...} -> R` (for instance `beta(k) = sqrt(4 log n / k)`; only
`n` and the own count may enter), and a priority `pi`. Run KH-UCB as in Section 1.0 with index
`f_a(0) := +infinity` and `f_a(k) := hat m_a(k) + beta(k)` for `k >= 1`, where
`hat m_a(k) = k^{-1} sum_{r <= k} y_{a,r}` and `y_a = (y_{a,1},...,y_{a,n}) in [0,1]^n` is arm `a`'s
reward tape indexed by its own pull count. If `y_1' >= y_1 coordinatewise` and `y_a' = y_a` for `a != 1`,
then `T_j'(t) <= T_j(t)` for every `j != 1` and every `t <= n`, and `T_1'(t) >= T_1(t)`.

*Proof.* Coordinatewise domination of the tape gives `hat m_1'(k) >= hat m_1(k)` for every `k >= 1` and
hence `f_1' >= f_1` pointwise (at `k = 0` both are `+infinity`). The policy is exactly the greedy merge
of Section 2.1 with priority `pi`: at a state where some arm has count `0`, its pair is
`(+infinity, a)`, so the lexicographic maximum is the `pi`-first count-zero arm, which is the
initialization rule; at a state where all counts are positive, the lexicographic maximum is the
`pi`-first index maximizer. Apply Theorem 2.3 and restrict to `t <= n`. QED

**Corollary 2.5 (blind behavioral form).** Fix `n >= 2`. Let each agent `a` have private randomness
`omega_a` and reward seeds `U_{a,1},...,U_{a,n}` i.i.d. uniform on `[0,1]`, with
`(omega_a, U_a)_{a in [K]}` and `pi` mutually independent. Under KH-UCB the platform sends no messages,
so a blind behavioral strategy of agent `a` is a sequence of measurable maps `g_{a,k}` from (its own
past targets and rewards, `omega_a`, `n`) to a target in `[0, M_a]`; the reward at its `k`-th selection
is `Y_{a,k} = 1{U_{a,k} <= m_{a,k}}` with `m_{a,k} = g_{a,k}(...)`. Then for every profile `S_{-i}` of
blind behavioral strategies of the other agents and every blind behavioral strategy `S_i` of agent `i`,
on every sample point and for every `t <= n`,
```
  T_j(t; M_i, S_{-i}) <= T_j(t; S_i, S_{-i})  for all j != i,   T_i(t; M_i, S_{-i}) >= T_i(t; S_i, S_{-i}),
```
where `M_i` denotes the constant-target strategy.

*Proof.* By induction on `k`, the pair `(m_{a,k}, Y_{a,k})` is a measurable function of
`(U_{a,1},...,U_{a,k}, omega_a, n)` only: `m_{a,1} = g_{a,1}(omega_a,n)`, `Y_{a,1} = 1{U_{a,1} <= m_{a,1}}`,
and if the claim holds up to `k-1` then `m_{a,k}` is a function of the listed quantities and
`Y_{a,k} = 1{U_{a,k} <= m_{a,k}}`. Blindness is what makes this true: the agent does not observe the
global round, the other agents' data, or any mechanism message, so nothing that differs between the two
coupled executions enters `g_{a,k}`. Consequently each agent's tape `(Y_{a,k})_{k <= n}` is a fixed
function of `(U_a, omega_a)`, identical in the two executions for `a != i`. For agent `i`, feasibility
`m_{i,k} <= M_i` gives `1{U_{i,k} <= m_{i,k}} <= 1{U_{i,k} <= M_i}` for every `k`, so the constant
strategy dominates the tape coordinatewise on the same seeds. Apply Corollary 2.4. QED

**Caveat 2.5.1 (do not over-read Corollary 2.5).** The comparison is between an arbitrary feasible blind
strategy and the CONSTANT `M_i`. Raising a behavioral strategy history by history does NOT give
coordinatewise tape domination and no monotonicity claim is made for such pairs: with
`g(empty) = 0.1`, `g((0)) = 0.9`, `g((1)) = 0.1`, `g' = max(g, 0.5)` and seeds `U_1 = 0.3`, `U_2 = 0.5`,
the base tape is `(0,1)` and the raised tape is `(1,0)`, which are incomparable. Also, if any other
agent observes something that differs between the two executions (a mechanism message, the global round,
or, in the contextual model, the profile `X_t`), its tape is no longer a fixed function of its own seeds
and the corollary does not apply. This is precisely why the grid results below are proved for `S_HDS`
and not for a contextual behavioral class.

### 2.2 Per-round tie coins: pathwise fails, expectation survives

**Proposition 2.6 (exact expected monotonicity under fresh per-round uniform tie coins).** Let `(f_a)`
be arbitrary sequences in a totally ordered set, `f_1' >= f_1` pointwise, `f_a' = f_a` for `a != 1`.
Consider the randomized greedy merge in which at each step the pulled arm is uniform on the set of arms
attaining `max_a f_a(T_a)`, with coins independent across steps. Then there is a coupling of the two
randomized runs, each with its correct marginal law, under which `T_j'(t) <= T_j(t)` for every `j != 1`
and every `t` on every sample point; in particular `E T_j'(t) <= E T_j(t)` and `E T_1'(t) >= E T_1(t)`
for every `t`, with zero remainder.

*Proof.* Step 1 (two-stage coin representation). Let `(xi_l)_{l >= 1}` and `(eta_t)_{t >= 1}` be
mutually independent uniform `[0,1]` variables. Run the process as follows. At step `t` let `S_t` be the
set of arms attaining the maximum and let `L_t` be the number of pulls of arms other than `1` at steps
`< t`. If `1 not in S_t`, pull the element of `S_t` selected by `xi_{L_t+1}` (the
`ceil(xi_{L_t+1} |S_t|)`-th element of `S_t` in label order). If `S_t = {1}`, pull arm `1`. If
`1 in S_t` and `|S_t| >= 2`, pull arm `1` if `eta_t <= 1/|S_t|`, and otherwise pull the element of
`S_t \ {1}` selected by `xi_{L_t+1}`.
By induction on `t`, the history of the first `t-1` steps is a measurable function of
`(xi_1,...,xi_{L_t})` and `(eta_1,...,eta_{t-1})` alone, and it determines `L_t` and `S_t`. Hence,
conditionally on that history, `xi_{L_t+1}` and `eta_t` are independent and uniform, and a direct
computation gives conditional probability `1/|S_t|` for each element of `S_t`: in the third case,
`Pr(pull 1) = 1/|S_t|` and, for `b in S_t \ {1}`,
`Pr(pull b) = (1 - 1/|S_t|) . 1/(|S_t| - 1) = 1/|S_t|`. So the process has exactly the law of the
per-round uniform tie-breaking merge.

Step 2 (the non-1 pull sequence is a function of the `xi` coins alone). Let `sigma_l` be the arm pulled
at the `l`-th non-1 pull and let `R_l` be the count vector of the arms `!= 1` just before that pull; `R_l`
is a function of `sigma_1,...,sigma_{l-1}`. Let `A_l := argmax_{a != 1} f_a(T_a)` evaluated at `R_l`. At
the step of the `l`-th non-1 pull, the pulled arm is not `1` and attains the global maximum, so the
global maximum equals `max_{a != 1} f_a(T_a)` and `S_t \ {1} = A_l`; by the construction of Step 1 the
pulled arm is the `xi_{L_t+1} = xi_l` selection from `A_l`. Hence `(sigma_l)_{l >= 1}` is a
deterministic function of `(xi_l)_{l >= 1}` and of the sequences `(f_a)_{a != 1}`, which are the same in
both runs. Couple the two runs by using the same `(xi_l)` and the same `(eta_t)`. Then
`sigma' = sigma`, `A_l' = A_l` and `g(l) := max_{a != 1} f_a(T_a)` evaluated at `R_l` is the same in
both runs, for every `l`.

Step 3 (arm 1 against the aggregate). Suppose, for contradiction, that `t` is the first step with
`T_1'(t) < T_1(t)`. Then `T_1'(t-1) = T_1(t-1) =: k`, and since both runs have taken `t-1` steps, both
have made `l := t-1-k` non-1 pulls; by Step 2 these are the same arms in the same order, so both runs are
in the same state at the start of step `t`, with the same `g(l)` and `|A_l|`, and the same coin `eta_t`.
The base run pulls arm `1` at step `t` (as `T_1(t) = k+1` and `T_1'(t) = k`). By the rule this means
either `f_1(k) > g(l)`, or `f_1(k) = g(l)` and `eta_t <= 1/(|A_l|+1)`. Since `f_1'(k) >= f_1(k)`: in the
first case `f_1'(k) > g(l)` and the raised run also pulls arm `1`; in the second case either
`f_1'(k) > g(l)` (arm `1` is the unique maximizer, pulled) or `f_1'(k) = g(l)` and the same coin gives
`eta_t <= 1/(|A_l|+1)`, so arm `1` is pulled. Both cases contradict `T_1'(t) = k`. Hence
`T_1'(t) >= T_1(t)` for every `t` on every sample point of the coupling.

Step 4 (conclusion). The non-1 pulls up to step `t` are `sigma_1,...,sigma_{t - T_1(t)}` in the base run
and `sigma_1,...,sigma_{t - T_1'(t)}` in the raised run, with the SAME sequence `sigma`. Since
`t - T_1'(t) <= t - T_1(t)`, for every `j != 1`,
`T_j'(t) = #{l <= t - T_1'(t) : sigma_l = j} <= #{l <= t - T_1(t) : sigma_l = j} = T_j(t)`. Each run has
its correct marginal law by Step 1, so the expectation statements follow. QED

**Fact 2.6.1 (pathwise monotonicity FAILS under fresh per-round coins, even for the known-horizon
index).** `K = 3`, `n = 8`, index `hat m_a + sqrt(log n / T_a)` (bonus constant `c = 1`), initialization
in label order, and a tie coin table that at round 4 ranks `2 succ 3 succ 1` and at round 6 ranks
`3 succ 2 succ 1` (all other rounds irrelevant). Tapes indexed by own pull count:
base arm 1 `(0,0,0,0,0,0,0,0)`, arm 2 `(0,1,1,1,1,1,1,1)`, arm 3 `(0,0,0,0,0,0,0,0)`;
raised arm 1 `(1,0,0,0,0,0,0,0)` (coordinatewise at or above base), arms 2 and 3 unchanged.
I re-ran this in this session (`checks.py`, function `c1_trace`, venv python): base pull history
`[1,2,3,2,2,2,2,2]` with counts `(1,6,1)`; raised pull history `[1,2,3,1,1,3,2,2]` with counts
`(3,3,2)`. Arm 3's count rises from `1` to `2` when arm 1's tape is raised, so the pathwise conclusion of
Corollary 2.4 is false for the per-round tie rule. The mechanism: raising arm 1 moves the tie between
arms 2 and 3 from round 4 to round 6, where a different coin applies. Any coupling that indexes tie
coins by the global round, by the full count vector, or by (tied set, counts of the tied arms) fails for
the same reason. Proposition 2.6 shows that the EXPECTED statement nevertheless survives, with zero
remainder, because one can index the tie coins by the number of non-1 pulls instead.

**Sanity searches run in this session** (`checks.py`, venv python, under one minute on the login node):
200000 random static-race instances (`K in {2,3,3,4,5}`, `n in {4,6,8,10,14}`, integer value sets
including heavy ties, count-zero value `+infinity`, `-infinity` or ordinary, random priority, random
pointwise raise of arm 1, checked at every intermediate `t` and every `j != 1`): 0 violations of
Theorem 2.3. 100000 random KH-UCB instances (`K in {2,3,3,4}`, `n in {5,...,12}`,
`c in {0.25,0.5,1,2,4}`, Bernoulli tapes from the coupling `Y_{a,r} = 1{U_{a,r} <= m_a}` with arm 1
raised to a random `M_1 >= m_1`, random priority, checked at every `t`): 0 violations of Corollary 2.4.
These are sanity checks, not evidence; the proofs above are the evidence.

### 2.3 The imported bandit bound, and why it applies to a cell with a random number of visits

**The exact imported inequality.** Source: T. Lattimore and C. Szepesvari, *Bandit Algorithms*,
Cambridge University Press 2020, PDF at https://tor-lattimore.com/downloads/book/book.pdf, downloaded
and read in this session on 17 September 2026.
- Definition 5.2 (page 77): a random variable `X` is `sigma`-subgaussian if
`E[exp(lambda X)] <= exp(lambda^2 sigma^2 / 2)` for all `lambda in R`.
- Corollary 5.5 (page 78): if `X_1,...,X_m` are independent with `X_u - theta` `sigma`-subgaussian and
`hat theta = m^{-1} sum_{u<=m} X_u`, then for every `eps >= 0`,
`Pr(hat theta >= theta + eps) <= exp(-m eps^2/(2 sigma^2))` and
`Pr(hat theta <= theta - eps) <= exp(-m eps^2/(2 sigma^2))`.
- Exercise 5.11(a) (page 84): a zero-mean `X in [a,b]` almost surely is `(b-a)/2`-subgaussian
(Hoeffding's lemma). Hence a centered Bernoulli is `1/2`-subgaussian, and since
`exp(lambda^2 (1/2)^2/2) <= exp(lambda^2/2)`, it is also `1`-subgaussian. Every `[0,1]`-valued reward is
likewise `1/2`-subgaussian and hence `1`-subgaussian.
- Algorithm 3 `UCB(delta)` (page 103): index `+infinity` if `T_a(t-1) = 0`, else
`hat theta_a(t-1) + sqrt(2 log(1/delta)/T_a(t-1))`; with `delta = 1/n^2` this is exactly
`hat theta_a + sqrt(4 log n / T_a)`, our KH-UCB index.
- Theorem 7.1 (page 105): for `UCB(delta)` with `delta = 1/n^2` on a `k`-armed `1`-subgaussian bandit
run for `n` rounds, `R_n <= 3 sum_{a} Delta_a + sum_{a : Delta_a > 0} 16 log(n)/Delta_a`; its proof
establishes, and Theorem 7.2 (page 108) reuses verbatim, the per-arm bound
`E[T_a(n)] <= 3 + 16 log(n)/Delta_a^2` for every suboptimal arm `a`.
- Theorem 7.2 (page 108): with `delta = 1/n^2`, `R_n <= 8 sqrt(n k log n) + 3 sum_a Delta_a`.

The book states these for an instance run for exactly `n` rounds. Our cells run for a RANDOM number
`s <= n` of rounds while the confidence level stays `1/n^2` (the global horizon). I therefore do not
import Theorem 7.1 as a black box; I reprove it in the form I need, following the book's argument, so
that the dependence on `s` is explicit. The only external ingredients are Corollary 5.5 and Hoeffding's
lemma above.

**Lemma 2.7 (KH-UCB deficit and gap-free bounds for an `s`-round instance with global confidence `n`).**
Fix `n >= 2`, `K >= 2` and an integer `s` with `1 <= s <= n`. Run KH-UCB(n, pi) (index
`hat theta_a + sqrt(4 log n / T_a)`, `+infinity` at count zero, any fixed tie rule, possibly randomized
but independent of the reward tapes) for `s` rounds on `K` arms whose rewards are drawn from the
own-count tapes `(Z_{a,r})_{a in [K], r >= 1}`, independent across all `(a,r)`, with `Z_{a,r}` supported
in `[0,1]` and `E Z_{a,r} = theta_a`. Let `theta^* := max_a theta_a` and `Delta_a := theta^* - theta_a`.
Then:
```
 (i)   E T_a(s) <= min{ s , 3 + 16 log(n)/Delta_a^2 }                     for every a with Delta_a > 0;
 (ii)  Delta_a E T_a(s) <= 4 sqrt(s log n) + 3                            for every a;
 (iii) E sum_{r=1}^{s} (theta^* - theta_{A_r}) <= 8 sqrt(K s log n) + 3K.
```

*Proof.* (i) `T_a(s) <= s` is trivial. For the other bound, fix a suboptimal `a` and let `1` denote an
arm with `theta_1 = theta^*` (relabelling). All rewards are `[0,1]`-valued, hence `1`-subgaussian after
centering. Write `hat theta_{b,r} := r^{-1} sum_{u <= r} Z_{b,u}` and let `U_b(t)` denote arm `b`'s
index at round `t`, i.e. `+infinity` if `T_b(t-1) = 0` and `hat theta_{b, T_b(t-1)} + sqrt(4 log n / T_b(t-1))`
otherwise. Put `u := ceil(16 log(n)/Delta_a^2) >= 1` and define the event
```
  G := { theta_1 < min_{t <= s} U_1(t) }  cap  { hat theta_{a,u} + sqrt(4 log n / u) < theta_1 }.
```
*Claim: on `G`, `T_a(s) <= u`.* Suppose `T_a(s) > u`. Then at some round `t <= s` arm `a` is pulled while
`T_a(t-1) = u`, so its index at that round is `hat theta_{a,u} + sqrt(4 log n/u) < theta_1 < U_1(t)`,
so `a` is not a maximizer at round `t`, contradicting that it was pulled (the contradiction is
independent of the tie rule, because the inequality is strict). This proves the claim, hence
`T_a(s) <= u + s 1{G^c}` pointwise, and `E T_a(s) <= u + s Pr(G^c)`.

*Bounding `Pr(G^c)`.* Since `T_1(t-1) <= s - 1 <= n` for every `t <= s`,
```
  Pr( theta_1 >= min_{t<=s} U_1(t) )
   <= Pr( there is r in {1,...,n} with hat theta_{1,r} + sqrt(4 log n / r) <= theta_1 )
   <= sum_{r=1}^{n} Pr( hat theta_{1,r} <= theta_1 - sqrt(4 log n / r) )
   <= sum_{r=1}^{n} exp( - r (4 log n / r) / 2 ) = n . n^{-2} = 1/n,
```
by Corollary 5.5 with `sigma = 1` and a union bound (the count-zero case contributes nothing because the
index is then `+infinity`). Next, `sqrt(4 log n/u) <= sqrt(4 log n Delta_a^2/(16 log n)) = Delta_a/2`,
so
```
  Pr( hat theta_{a,u} + sqrt(4 log n/u) >= theta_1 )
   <= Pr( hat theta_{a,u} >= theta_a + Delta_a/2 ) <= exp( - u Delta_a^2/8 ) <= exp(-2 log n) = n^{-2},
```
again by Corollary 5.5 with `sigma = 1` and `u >= 16 log(n)/Delta_a^2`. Hence
`Pr(G^c) <= 1/n + n^{-2}` and, using `s <= n` and `u <= 16 log(n)/Delta_a^2 + 1`,
```
  E T_a(s) <= u + n(1/n + n^{-2}) = u + 1 + 1/n <= 16 log(n)/Delta_a^2 + 2 + 1/n <= 3 + 16 log(n)/Delta_a^2 .
```
This is the book's constant, now valid for every `s <= n`.

(ii) If `Delta_a = 0` there is nothing to prove. Otherwise, using `min{A, B + C} <= min{A,B} + C` for
`C >= 0` and `min{A,B} <= sqrt(AB)`,
```
  Delta_a E T_a(s) <= min{ s Delta_a , 16 log(n)/Delta_a + 3 Delta_a }
                   <= min{ s Delta_a , 16 log(n)/Delta_a } + 3 Delta_a
                   <= sqrt( s Delta_a . 16 log(n)/Delta_a ) + 3 = 4 sqrt(s log n) + 3,
```
since `Delta_a <= 1` (all means lie in `[0,1]`).

(iii) Let `Delta > 0` be free. Since `sum_a E T_a(s) = s` and `Delta_a <= 1`,
```
  E sum_{r<=s}(theta^* - theta_{A_r}) = sum_a Delta_a E T_a(s)
   <= Delta sum_{a : Delta_a <= Delta} E T_a(s) + sum_{a : Delta_a > Delta} ( 3 Delta_a + 16 log(n)/Delta_a )
   <= s Delta + 3K + 16 K log(n)/Delta .
```
Choosing `Delta := 4 sqrt(K log(n)/s)` gives `s Delta = 4 sqrt(K s log n)` and
`16 K log(n)/Delta = 4 sqrt(K s log n)`, hence the bound `8 sqrt(K s log n) + 3K`. QED

**Why this applies to a cell with a random number of visits.** In the grid, a cell `C` is visited
`V_C` times, a random variable with `V_C <= n`. Lemma 2.9 below shows that, CONDITIONALLY on the entire
membership-indicator sequence `B := (1{X_t in C})_{t <= n}` (which fixes `V_C = s` as a deterministic
number and fixes at which global rounds the visits occur), the cell execution has exactly the law of the
`s`-round own-count-tape instance of Lemma 2.7 with arm means `bar m_{a,C}`. Lemma 2.7 is stated for a
deterministic `s <= n`, so it applies conditionally on every value of `B`; the conclusions are then
averaged over `B`. The confidence level `1/n^2` is set from the GLOBAL horizon `n` and does not depend
on `s`; this is what makes the union bound over `r in {1,...,n}` legitimate and uniform over cells. No
statement is made about a cell rule that would use the cell's own visit count inside the logarithm.

### 2.4 The conditional cell law

**Lemma 2.8 (conditional cell law).** Let `X_1,...,X_n` be i.i.d. `nu` on `X` and let `C` be a Borel set
with `nu(C) > 0`. Let `B := (B_1,...,B_n)` with `B_t := 1{X_t in C}`, and on `{sum_t B_t = s}` let
`X^{(1)},...,X^{(s)}` be the profiles at the visits to `C`, in order of time. Then for every
`beta in {0,1}^n` with `sum_t beta_t = s >= 1`, conditionally on `{B = beta}` the random vectors
`X^{(1)},...,X^{(s)}` are i.i.d. with law `nu(. | C)`, and the profiles at the rounds `t` with
`beta_t = 0` are i.i.d. `nu(. | C^c)` and independent of them. Moreover `Pr(B = beta)` does not depend
on the agents' maps, the reward seeds, the priorities `pi_C`, or any platform randomness.

*Proof.* Let `t_1 < ... < t_s` be the rounds with `beta_t = 1`. For Borel sets `A_1,...,A_s` contained in
`C`, and Borel `A'_t subseteq C^c` for the remaining rounds, independence of the `X_t` gives
```
  Pr( X_{t_1} in A_1, ..., X_{t_s} in A_s, X_t in A'_t for beta_t = 0 )
    = prod_{u=1}^{s} nu(A_u) . prod_{t : beta_t = 0} nu(A'_t),
```
while `Pr(B = beta) = nu(C)^s (1 - nu(C))^{n-s}`. Dividing gives the product
`prod_u nu(A_u|C) . prod_t nu(A'_t | C^c)`, which is the assertion. The last sentence holds because the
profiles are exogenous: their law is `nu^{otimes n}` and is independent of all other primitives of the
model by assumption. QED

Two consequences used repeatedly:
(C1) conditionally on `B = beta`, the profile `X^{(k)}` of the `k`-th visit is independent of
`(X^{(1)},...,X^{(k-1)})` and of all reward seeds and priorities;
(C2) if `nu(C) = 0` then `Pr(some X_t in C) = 0`, so a zero-mass cell is never visited, is never
initialized, and contributes `0` to every count; no conditional mean `bar m_{a,C}` is needed.

### 2.5 The cell-average coupling law

For a cell `C` with `nu(C) > 0` and a fixed (realized) map profile `(m_{a,n})_{a in [K]}`, define
```
  bar m_{a,C} := E[ m_{a,n}(X) | X in C ] = nu(C)^{-1} int_C m_{a,n}(x) nu(dx)  in [0,1].
```

**Lemma 2.9 (cell-average coupling law).** Fix a realized map profile, a cell `C` with `nu(C) > 0`, a
membership pattern `beta` with `s := sum_t beta_t >= 1`, and condition on `{B = beta}`. Let
`(A_k, Y_k)_{k <= s}` be the cell-local selections and realized rewards of Static Grid KH-UCB, in order
of cell visits. Let `(Z_{a,r})_{a in [K], r >= 1}` be an array of independent Bernoulli(`bar m_{a,C}`)
variables, independent of `pi_C`, and let `(tilde A_k, tilde Y_k)_{k <= s}` be produced by running the
same cell rule (same index, same priority law `pi_C`) with `tilde Y_k := Z_{tilde A_k, T_{tilde A_k}(k)}`,
where `T_a(k)` is `a`'s count after `k` cell rounds. Then
```
  Law( (A_k, Y_k)_{k <= s} | B = beta )  =  Law( (tilde A_k, tilde Y_k)_{k <= s} ).
```

*Proof.* Condition further on `pi_C = p` (the priority is independent of everything else and has the
same law in both constructions); then both rules are deterministic functions of the observed history, so
it suffices to match the joint law of `(A_1,Y_1,...,A_s,Y_s)`, which takes values in the countable set
`([K] x {0,1})^s`. Write `phi_k` for the (deterministic, `p`-dependent) selection map, so that
`A_k = phi_k(A_1,Y_1,...,A_{k-1},Y_{k-1})` and similarly for `tilde A_k`; this covers the initialization
rounds, where `phi_k` is the "`p`-first agent with count zero" and depends on the history only through
the counts.

Fix a history `h = (a_1,y_1,...,a_{k-1},y_{k-1})` that is consistent with `phi`, i.e. `a_u = phi_u(h_{u-1})`
for all `u <= k-1`. It suffices to show that in both models
```
  Pr( Y_k = 1 | history_{k-1} = h ) = bar m_{a_k, C},   where a_k := phi_k(h),               (2.3)
```
whenever `Pr(history_{k-1} = h) > 0`; then an induction on `k` gives equality of the two joint laws,
since the selections are the same deterministic functions of the history in both models.

*Real model.* The realized reward of agent `a` at the `k`-th visit of `C` is
`W_{a,k} := 1{ U^{(k)}_a <= m_{a,n}(X^{(k)}) }`, where `U^{(k)}_a` are the (independent, uniform) reward
seeds attached to that visit and `X^{(k)}` is the profile of that visit. By Lemma 2.8 and the exogeneity
of the profiles, conditionally on `B = beta` the pair `(X^{(k)}, (U^{(k)}_a)_a)` is independent of
`(X^{(u)}, (U^{(u)}_a)_a)_{u < k}` and of `pi_C`, and the event `{history_{k-1} = h}` is measurable with
respect to the latter. Hence
```
  Pr(Y_k = 1 | history_{k-1} = h) = Pr( U^{(k)}_{a_k} <= m_{a_k,n}(X^{(k)}) )
    = E[ m_{a_k,n}(X^{(k)}) ] = E[ m_{a_k,n}(X) | X in C ] = bar m_{a_k,C},
```
using `X^{(k)} ~ nu(.|C)` and the independence of `U^{(k)}_{a_k}` from `X^{(k)}`.

*Auxiliary model.* The history `h` determines the counts `T_a(k-1) =: r_a - 1`, and the values
`tilde Y_u` recorded in `h` are exactly the variables `Z_{a, 1}, ..., Z_{a, r_a - 1}` for each `a`; so
`{history_{k-1} = h}` is an event measurable with respect to
`{ Z_{a,r} : a in [K], 1 <= r <= r_a - 1 }`. The variable used at round `k` is `Z_{a_k, r_{a_k}}`, whose
index is not in that set, so it is independent of the event, and
`Pr(tilde Y_k = 1 | history_{k-1} = h) = E Z_{a_k, r_{a_k}} = bar m_{a_k,C}`.

Both models satisfy (2.3), so by induction on `k` the joint laws coincide; averaging over `pi_C`
completes the proof. QED

**Remark 2.9.1 (what Lemma 2.9 buys and what it does not).** It buys equality of LAW, hence equality of
all expectations of functions of the cell-local selection sequence, including `E T_a(C;n)`. It does not
buy a pathwise statement in the original probability space: the auxiliary array `(Z_{a,r})` is indexed
by the agent's own pull count inside the cell, whereas the real rewards `W_{a,k}` are indexed by the
cell visit. When agent `i`'s map is raised pointwise, `W_{i,k}` increases at every VISIT `k` on the same
seed, but the `r`-th pull of agent `i` occurs at different visits in the two executions, so the real
own-count tape is not coordinatewise monotone and Theorem 2.3 cannot be applied to it. This is exactly
the ambiguity recorded in Section 14.1 of the contract, and it is why S3 is an exact EXPECTED statement.

### 2.6 The region identity (requirement 2)

**Lemma 2.10 (region identity).** Fix a realized map profile, a cell `C` with `nu(C) > 0`, and any
measurable `R subseteq X`. Then for every `n`,
```
  E T_j(C cap R; n) = nu(R | C) . E T_j(C; n)     for every agent j,
```
where `nu(R|C) := nu(R cap C)/nu(C)`. Consequently, for every measurable `R`,
```
  E T_j(R;n) = sum_{C : nu(C) > 0} nu(R|C) E T_j(C;n).
```

*Proof.* Every round `t` with `X_t in C` is a cell visit; if it is the `k`-th one, then `X_t = X^{(k)}`
and `I_t = A_k`. Hence, pathwise,
```
  T_j(C cap R; n) = sum_{k >= 1} 1{k <= V_C} 1{ X^{(k)} in R } 1{ A_k = j }.
```
Fix a membership pattern `beta` with `s = sum_t beta_t >= 1` and condition on `{B = beta}`; then
`V_C = s` is deterministic, and for `k <= s`,
```
  E[ 1{X^{(k)} in R} 1{A_k = j} | B = beta ] = nu(R|C) . Pr( A_k = j | B = beta ).
```
This is the only nontrivial step and it holds because `A_k` is a measurable function of
`(X^{(1)},...,X^{(k-1)})`, the reward seeds of the first `k-1` visits of `C`, and `pi_C`, while by
Lemma 2.8 (consequence (C1)) `X^{(k)}` is, conditionally on `{B = beta}`, independent of all of those and
distributed as `nu(.|C)`. Summing over `k <= s`,
```
  E[ T_j(C cap R; n) | B = beta ] = nu(R|C) sum_{k <= s} Pr(A_k = j | B = beta)
                                  = nu(R|C) E[ T_j(C;n) | B = beta ].
```
For `beta = 0` (the cell is not visited) both sides are `0`. Averaging over `beta` gives the identity.
The second display follows because the cells partition `X` and, by (C2), cells with `nu(C) = 0`
contribute `0` to both `T_j(R;n)` and `T_j(C;n)`. QED

**The three cases requirement 2 asks about, explicitly.**
1. *Cells visited fewer than `K` times.* The display above is a sum over `k <= s` term by term and never
uses `s >= K`. For `k <= K` the selection `A_k` is the `pi_C`-first agent with count zero, a function of
`pi_C` alone; it is in particular still independent of `X^{(k)}`, which is all the argument needs. So
lightly visited cells, including cells visited once, are covered with no change.
2. *Cells where some agent is never selected.* Then `T_j(C;n) = 0` for that agent on those sample points
and the identity reads `0 = nu(R|C) . 0` on them; nothing in the proof requires `T_j(C;n) > 0`. The
identity is an identity of expectations of nonnegative integer variables and holds term by term in `k`.
3. *Random visit counts.* Handled by conditioning on the full membership pattern `B`, which makes
`V_C = s` deterministic. Note that `B` is NOT independent of `T_j(C;n)` (more visits means more
selections), which is why one must condition rather than factor naively; after conditioning, the
factorization is exact and the remaining average over `B` is over a distribution that does not depend on
the agents' maps (Lemma 2.8, last sentence).

### 2.7 Lipschitz cell comparisons and boundary cells

Throughout, `C` is a cell of the Static Grid partition, `nu(C) > 0`, `x = (x_1,...,x_K)` and
`x' = (x'_1,...,x'_K)` range over `C`, and `|.|` is the Euclidean norm.

**Lemma 2.11 (one-step cell comparison; lesson L2).** Let `g : [0,1]^d -> R` be `L`-Lipschitz and let
`G(x) := g(x_a)` for a fixed agent index `a`. Then for every `x in C`,
```
  | G(x) - E[G | C] | <= L sqrt(d) h_n .
```
*Proof.* Inside `C` the block `x_a` ranges over a cube of side `h_n` in `[0,1]^d`, so
`|x_a - x'_a| <= sqrt(d) h_n` for `x, x' in C` and `|G(x) - G(x')| <= L sqrt(d) h_n`. Integrate the
inequality `G(x) - L sqrt(d) h_n <= G(x') <= G(x) + L sqrt(d) h_n` in `x'` against `nu(.|C)`. QED

**Lemma 2.12 (best-honest cell comparison).** Assume every `mu_a` is `L`-Lipschitz on `[0,1]^d` and every
honest agent uses an honest map (`m_{h,n}(X) >= mu_h(x_h)` for every `X`). Put
`bar b_C := E[b(X)|C]` and `bar m^*_C := max_{a in [K]} bar m_{a,C}`. Then
```
  bar b_C <= bar m^*_C + L sqrt(d) h_n .
```
*Proof.* For `x in C` let `h(x) in K_H` attain `b(x) = mu_{h(x)}(x_{h(x)})`. By Lemma 2.11 applied to
`mu_{h(x)}`, `b(x) = mu_{h(x)}(x_{h(x)}) <= E[mu_{h(x)} | C] + L sqrt(d) h_n <= max_{h in K_H} E[mu_h | C] + L sqrt(d) h_n`.
Integrating in `x` against `nu(.|C)` gives `bar b_C <= max_{h in K_H} E[mu_h|C] + L sqrt(d) h_n`.
Honesty gives `E[mu_h|C] <= E[m_{h,n}|C] = bar m_{h,C} <= bar m^*_C` for every honest `h`. QED

**Lemma 2.13 (best-capacity cell comparison).** Assume every `M_a` is `L`-Lipschitz on `[0,1]^d`. Put
`bar M_{*,C} := E[M_*(X)|C]` and, under `S^max` (`m_{a,n} = M_a`), `bar m^*_C = max_a bar M_{a,C}`. Then
`bar M_{*,C} <= bar m^*_C + L sqrt(d) h_n`. *Proof.* Identical to Lemma 2.12 with `M_a` in place of
`mu_a` and the maximum over all agents in place of the maximum over honest agents. QED

**Lemma 2.14 (rival cell comparison; used only in S8).** Assume every `M_a` is `L`-Lipschitz and
`nu(|T(X)| >= 2) = 1`. Then for every cell `C` with `nu(C) > 0` and every agent `i`,
```
  max_{j != i} bar M_{j,C} >= bar M_{i,C} - 2 L sqrt(d) h_n .
```
*Proof.* The set `{X : |T(X)| >= 2}` has `nu`-measure `1`, so its intersection with `C` has measure
`nu(C) > 0` and is therefore nonempty; pick `X_0` in it and pick `j in T(X_0)` with `j != i`, which is
possible because `|T(X_0)| >= 2`. Then `M_j(x_{0,j}) = M_*(X_0) >= M_i(x_{0,i})`. By Lemma 2.11 applied
to `M_j` and to `M_i` (with `X_0 in C`),
```
  bar M_{j,C} >= M_j(x_{0,j}) - L sqrt(d) h_n >= M_i(x_{0,i}) - L sqrt(d) h_n >= bar M_{i,C} - 2 L sqrt(d) h_n .
```
QED

**Remark 2.14.1 (why the factor 2 is unavoidable here but not in Lemmas 2.12 and 2.13).** Lemmas 2.12
and 2.13 compare ONE function at a point with its own cell average, so a single Lipschitz step suffices
and the constant is `L sqrt(d)`. Lemma 2.14 compares the cell averages of TWO different functions
(`M_i` and `M_j`) which are ordered only at the single point `X_0`, so the chain must pass through
`X_0` and costs two steps. This is the only place in this file where a two-step Lipschitz chain occurs.

**Lemma 2.15 (boundary cells).** Let `R subseteq X` be any set and let `C` be a cell that meets both `R`
and `R^c`. Then `C subseteq (partial R)^{sqrt(D) h_n}`, the closed `sqrt(D) h_n`-neighbourhood of
`partial R`. Consequently
```
  sum_{C : C cap R != empty, C cap R^c != empty} E V_C = n . nu( union of those cells )
     <= n . nu( (partial R)^{sqrt(D) h_n} ).
```
*Proof.* `C` is a product of intervals, hence convex, hence connected. If `C cap partial R = empty`,
then `C subseteq int(R) cup int(R^c)`, a union of two disjoint open sets; `C cap R subseteq int(R)` is
nonempty and `C cap R^c subseteq int(R^c)` is nonempty, so `C` would be disconnected, a contradiction.
Hence `C` contains a point `y in partial R`, and every `x in C` satisfies `|x - y| <= diam(C) <= sqrt(D) h_n`.
For the display, `E V_C = n nu(C)` because the `X_t` are i.i.d. `nu`, and the cells are disjoint. QED

## 3. Proofs of S1 to S8

**Lemma 2.10 in integrated form (used throughout Section 3).** For every cell `C` with `nu(C) > 0`,
every agent `j`, and every bounded measurable `phi : X -> R`,
```
  E sum_{t <= n} 1{X_t in C, I_t = j} phi(X_t) = E[phi(X) | X in C] . E T_j(C;n).
```
The proof is verbatim that of Lemma 2.10 with `1_R` replaced by `phi`; the only property used is that,
conditionally on the membership pattern, `A_k` is independent of `X^{(k)}` and `X^{(k)} ~ nu(.|C)`.
Taking `phi = 1_R` recovers Lemma 2.10.

### 3.1 Proof of Theorem A (target S1, scalar)

(i) For fixed means, horizon-dependent fixed means, or blind behavioral strategies, Corollary 2.5 is
exactly the assertion (Corollary 2.4 suffices when all agents use fixed means, since then each tape is
`Y_{a,r} = 1{U_{a,r} <= m_a}` and raising `m_i` to `M_i` raises agent `i`'s tape coordinatewise on the
same seeds). The statement holds conditionally on `pi`, hence also unconditionally, and simultaneously
for all `t <= n`. Zero remainder, every `n`, no gap assumption.

(ii) Fix a profile of (possibly horizon-dependent) fixed means `m_1,...,m_K` with `m_h >= mu_h` for every
honest `h`. Pick an honest `h^*` with `mu_{h^*} = mu_H^*`; then `m^* := max_a m_a >= m_{h^*} >= mu_H^*`.
For fixed means `C_i(n) = (m_i - mu_i) T_i(n)`, so
```
  E C_i(n) - (mu_H^* - mu_i) E T_i(n) = (m_i - mu_H^*) E T_i(n) >= - (mu_H^* - m_i)_+ E T_i(n)
      >= - (m^* - m_i) E T_i(n) = - Delta_i E T_i(n),
```
where the last inequality uses `(mu_H^* - m_i)_+ <= (m^* - m_i)_+ = Delta_i` because `mu_H^* <= m^*`.
With fixed means, scalar KH-UCB run for `n` rounds is exactly the own-count-tape instance of Lemma 2.7
with `s = n`, `theta_a = m_a`, so Lemma 2.7(ii) gives `Delta_i E T_i(n) <= 4 sqrt(n log n) + 3`.

(iii) `P(n) = E sum_t m_{I_t} = n m^* - E sum_t (m^* - m_{I_t}) >= n mu_H^* - (8 sqrt(K n log n) + 3K)`
by Lemma 2.7(iii) with `s = n` and `m^* >= mu_H^*`.

(iv) Assume `m_i = m_j =: m`. Let `sigma` be the transposition of the labels `i` and `j`. The execution
is a deterministic function `Psi` of the tape array `z = (z_{a,r})` and the priority `p`. Define
`z^sigma_{a,r} := z_{sigma(a),r}` and let `p^sigma` be the priority that ranks `a` above `b` exactly when
`p` ranks `sigma(a)` above `sigma(b)`. A one-line induction on `t` shows that the selection sequence of
`Psi(z^sigma, p^sigma)` is the `sigma`-image of that of `Psi(z,p)`: at every step the index of arm `a`
in the transformed run equals the index of arm `sigma(a)` in the original run (same count, same tape
prefix), and the tie order is transported the same way, so the lexicographic maximizer is transported by
`sigma`. Hence `T_a(Psi(z^sigma,p^sigma)) = T_{sigma(a)}(Psi(z,p))` for every `a` and every `t`. The map
`(z,p) -> (z^sigma, p^sigma)` preserves the joint law: the tapes of `i` and `j` are i.i.d. Bernoulli with
the SAME parameter `m` and independent of the other tapes, and `p` is uniform so `p^sigma` is uniform.
Therefore `E T_i(n) = E T_i(Psi(z^sigma,p^sigma)) = E T_j(n)`, exactly, for every `n`. QED

### 3.2 Proof of Theorem A' (scalar public equilibrium, deviation-uniform)

Fix `i` and a deviation `m_i' in [0, M_i]`; write `delta := M_i - m_i' >= 0` and
`a_i := 1 + mu_i - M_i`, which is in `[0,2]` and in particular `a_i >= 0` because `M_i <= 1` and
`mu_i >= 0`. With fixed means, `u_i(n;S) = E[T_i(n)(1 + mu_i - m_i)]`, so
```
  gain = (a_i + delta) E T_i'(n) - a_i E T_i(n) = delta E T_i'(n) + a_i (E T_i'(n) - E T_i(n)) <= delta E T_i'(n),
```
because `a_i >= 0` and, by Theorem A(i) applied to the raise from `m_i'` to `M_i`, `E T_i'(n) <= E T_i(n)`
(self-monotonicity: agent `i`'s own count weakly increases when its own tape is raised). Now, in the
deviating profile the arms' means are `m_i' = M_i - delta` for `i` and `M_a` for `a != i`. Since
`K_top >= 2`, there is `j != i` with `M_j = M_top >= M_i`, so the gap of agent `i` in that profile is
```
  Delta_i' = max_{a != i} M_a - (M_i - delta) >= M_top - M_i + delta >= delta >= 0 .
```
If `Delta_i' = 0` then `delta = 0` and `gain <= 0`. If `Delta_i' > 0`, Lemma 2.7(ii) with `s = n` gives
`delta E T_i'(n) <= Delta_i' E T_i'(n) <= 4 sqrt(n log n) + 3`. The revenue statement is
`P(n;S^max) = M_top n - E sum_t (M_top - M_{I_t}) >= M_top n - 8 sqrt(K n log n) - 3K` by Lemma 2.7(iii).
QED

### 3.3 Remark: the anytime index is not pathwise monotone (Claim L3 re-verified)

I re-ran the tape of Claim L3 in this session (`checks.py`, function `l3_trace`, venv python).
`K = 3`, `n = 8`, index `hat m_a + sqrt(2 log t / T_a)` with `t` the GLOBAL round, initialization in
label order, ties to the lowest label; tapes indexed by each arm's own pull count:
```
  base:   arm 1 (0,0,0,0,1,0,0,0), arm 2 (0,0,1,0,0,1,1,1), arm 3 (1,1,1,1,1,0,0,1)
  raised: arm 1 (1,0,0,1,1,1,0,1)  (coordinatewise at or above base), arms 2 and 3 unchanged.
```
Output: base pull history `[1,2,3,3,3,3,3,1]`, counts `(2,1,5)`; raised pull history
`[1,2,3,1,3,3,3,2]`, counts `(2,2,4)`. Arm 2's count rises from `1` to `2` when arm 1's tape is raised.
This realization has positive probability under the manuscript's rule (a fixed initialization order and
these tie outcomes are in the support of the uniform initialization order and the uniform tie coins), so
the manuscript's anytime UCB1 is NOT pathwise monotone under the own-count tape coupling. The mechanism
is that the anytime index of an arm at own count `k` is `hat m_a(k) + sqrt(2 log t/k)`, a function of the
global round `t` as well as of `k`; raising arm 1 moves its pulls earlier, which shifts the global rounds
at which the other arms reach given counts, so the index sequences are no longer fixed functions of the
own count and Theorem 2.3 does not apply. On the very same tapes, the known-horizon index with
`beta(k) = sqrt(4 log n/k)` and a fixed priority gives base and raised counts `(2,2,4)`, as Corollary 2.4
guarantees. This does not contradict `thm:scalar-ucb`, which claims only expected monotonicity with an
`o(n)` remainder; it does show that no pathwise or zero-remainder claim can be made for the anytime rule.
Whether anytime UCB1 is exactly expectation-monotone is OPEN: I have neither a proof nor a
counterexample, and I make no claim about it.

### 3.4 Proof of Theorem B (target S2, finite contexts)

Condition throughout on the entire arrival sequence `(X_1,...,X_n) = (z^{(1)},...,z^{(n)})`, which is
legitimate because the arrivals are exogenous and independent of all reward seeds and priorities. Under
this conditioning each `V_z` is a deterministic number `s_z <= n` with `sum_z s_z = n`, and the instance
at profile `z` is exactly the own-count-tape instance of Lemma 2.7 with `s = s_z`, arm means
`theta_a = m_a(z)`, and priority `pi_z` (independent of the tapes). No averaging over contexts is
needed, because the profile at every visit to `z` is literally `z`.

(ii) Monotonicity. Realize the tapes as `Y_{z,a,r} = 1{U_{z,a,r} <= m_a(z)}`. Replacing `m_i` pointwise
by `M_i` raises, in every instance `z` simultaneously, agent `i`'s tape coordinatewise on the same
seeds. Corollary 2.4 applied in each instance separately gives `T_j^{i up}(z;n) <= T_j(z;n)` for every
`j != i`, every `z`, and every intermediate local time, on every sample point. Summing over `z in R`
gives `T_j^{i up}(R;n) <= T_j(R;n)` pathwise given the arrivals, hence in expectation, with zero
remainder, for every `R subseteq X_F` and every `n`. Averaging over the arrival sequence preserves the
inequality. (Note this is stronger than target S2, which asks only for exactness.)

(i) Sharp adaptivity. Fix `i` and `R`. Since `c_{i,t} = m_i(X_t) - mu_i(x_{i,t})`,
```
  E sum_t 1{X_t in R, I_t=i} c_{i,t} - E sum_t 1{X_t in R, I_t=i}[b(X_t)-mu_i(x_{i,t})]
     = - sum_{z in R} (b(z) - m_i(z)) E T_i(z;n) >= - sum_{z in R} Delta_{i,z} E T_i(z;n),
```
where `Delta_{i,z} := max_a m_a(z) - m_i(z) >= (b(z)-m_i(z))_+` because some honest agent `h` attains
`b(z) = mu_h(z_h) <= m_h(z) <= max_a m_a(z)`. By Lemma 2.7(ii) conditionally on the arrivals,
`Delta_{i,z} E[T_i(z;n) | arrivals] <= 4 sqrt(s_z log n) + 3`; taking expectations and using Jensen
(`E sqrt(V_z) <= sqrt(E V_z)`) gives `Delta_{i,z} E T_i(z;n) <= 4 sqrt(E V_z log n) + 3`. Summing over
`z in R` and applying Cauchy-Schwarz (`sum_{z in R} sqrt(E V_z) <= sqrt(|R| sum_{z in R} E V_z) <= sqrt(|R| n)`),
the total is at most `4 sqrt(|R| n log n) + 3 |R|`.

(iii) FATA. For `z in G_{ij}(R)` the two agents have equal means `m_i(z) = m_j(z) = M_*(z)` in that
instance; the label-swap argument of Theorem A(iv), applied to the instance at `z` conditionally on
`V_z = s_z` (tapes of `i` and `j` i.i.d. with the same parameter, `pi_z` uniform), gives
`E[T_i(z;n)|arrivals] = E[T_j(z;n)|arrivals]`. Summing over `z in G_{ij}(R)` and averaging over the
arrivals gives `E T_i(G_{ij}(R);n) = E T_j(G_{ij}(R);n)` exactly.

(iv) Robustness. `E sum_t [b(X_t) - m_{I_t}(X_t)] <= sum_z E sum_{visits to z} (max_a m_a(z) - m_{A}(z))`
`<= sum_z (8 sqrt(K E V_z log n) + 3K) <= 8 sqrt(K Q n log n) + 3 K Q` by Lemma 2.7(iii), Jensen and
Cauchy-Schwarz, using `b(z) <= max_a m_a(z)`. Hence
`P(n) = E sum_t m_{I_t}(X_t) >= E sum_t b(X_t) - 8 sqrt(K Q n log n) - 3 K Q`.

(v) Public equilibrium. Fix `i` and a deviation `m_i' in S_F`, and put `delta_z := M_i(z_i) - m_i'(z) >= 0`
and `a_z := 1 + mu_i(z_i) - M_i(z_i) >= 0`. Exactly as in Section 3.2, instance by instance,
```
  gain = sum_z [ (a_z + delta_z) E T_i'(z;n) - a_z E T_i(z;n) ] <= sum_z delta_z E T_i'(z;n),
```
using `a_z >= 0` and the self-monotonicity `E T_i'(z;n) <= E T_i(z;n)` from Corollary 2.4. Since
`|T(z)| >= 2`, there is `j != i` with `M_j(z_j) = M_*(z) >= M_i(z_i)`, so the deviating gap of `i` at `z`
is `Delta_{i,z}' >= delta_z`, and Lemma 2.7(ii) with Jensen gives
`delta_z E T_i'(z;n) <= 4 sqrt(E V_z log n) + 3`. Cauchy-Schwarz over the `Q` profiles gives
`gain <= 4 sqrt(Q n log n) + 3 Q`. The first revenue bound is (iv) with `b` replaced by `M_*` (no
regularity needed, since each instance is a single profile). For the `O(log n)` version, assume i.i.d.
arrivals with fixed positive masses and fixed positive non-top gaps `g_{k,z} := M_*(z) - M_k(z_k) > 0`;
then Lemma 2.7(i) gives `E T_k(z;n) <= 3 + 16 log n / g_{k,z}^2` and
`E sum_t [M_*(X_t) - M_{I_t}(x_{I_t,t})] = sum_z sum_{k not in T(z)} g_{k,z} E T_k(z;n)
<= sum_z sum_{k not in T(z)} (3 g_{k,z} + 16 log n/g_{k,z})`, which is `O(log n)`. QED

Independent ex ante mixtures over maps in `S_F` are covered by conditioning on the realized maps: every
bound above is uniform over deterministic map profiles, so it survives averaging (requirement 6).

### 3.5 The three grid terms and the rate

**Lemma 3.5.** With `h_n = (log(en)/n)^{1/(D+2)}`, `N_n = ceil(1/h_n)` and `J_n = N_n^D`, for every
`n >= 2`:
```
  h_n <= 1;   J_n <= 2^D h_n^{-D} = 2^D (n/log(en))^{D/(D+2)};
  n h_n = n^{(D+1)/(D+2)} (log(en))^{1/(D+2)};
  sqrt(J_n n log n) <= 2^{D/2} n^{(D+1)/(D+2)} (log(en))^{1/(D+2)};
  J_n <= 2^D n^{(D+1)/(D+2)} (log(en))^{1/(D+2)} .
```
*Proof.* `log(en) = 1 + log n <= n` for `n >= 1`, so `h_n <= 1` and `1/h_n >= 1`, whence
`N_n <= 1/h_n + 1 <= 2/h_n` and `J_n <= 2^D h_n^{-D}`. The identity for `n h_n` is the definition. For
the third line, `J_n n log n <= 2^D (n/log(en))^{D/(D+2)} n log n`, so
`sqrt(J_n n log n) <= 2^{D/2} n^{(D+1)/(D+2)} (log n)^{1/2} (log(en))^{-D/(2(D+2))}`, and since
`log n <= log(en)` and `1/2 - D/(2(D+2)) = 1/(D+2)`, this is at most
`2^{D/2} n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`. The last line follows from
`J_n <= 2^D n^{D/(D+2)} <= 2^D n^{(D+1)/(D+2)}` and `(log(en))^{1/(D+2)} >= 1`. QED

In particular `L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 J_n <= (L sqrt(d) + 4 . 2^{D/2} + 3 . 2^D) n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`,
and the same with `(8 sqrt(K), 3K)` in place of `(4,3)`.

### 3.6 Proof of Theorem C(iii) (target S3: exact expected contextual monotonicity)

Fix `n >= 2`, a realized map profile `(m_{a,n})_{a in [K]}` in `S_HDS`, an agent `i`, an agent `j != i`,
and ANY measurable `R subseteq X`. Write `E^{(0)}` for expectations under `(m_{i,n}, m_{-i,n})` and
`E^{(1)}` for expectations under `(M_i, m_{-i,n})`, all other primitives (the law `nu` of the profiles,
the seeds, the priorities `pi_C`) unchanged.

**Step 1 (the cell decomposition and the identity).** By Lemma 2.10,
```
  E^{(b)} T_j(R;n) = sum_{C : nu(C)>0} nu(R|C) . E^{(b)} T_j(C;n),   b in {0,1},
```
the sum being over the at most `J_n` cells of positive mass; zero-mass cells are never visited
(consequence (C2)) and contribute `0` to both sides; `nu(R|C)` is a nonnegative number determined by
`nu`, `R` and `C` alone, and is therefore IDENTICAL in the two executions. So it suffices to prove
`E^{(1)} T_j(C;n) <= E^{(0)} T_j(C;n)` for every cell `C` with `nu(C) > 0`.

**Step 2 (cell by cell, through the auxiliary model).** Fix such a cell `C` and a membership pattern
`beta` with `s := sum_t beta_t >= 1`. By Lemma 2.8, the law of `B` is the same under both map profiles
(the profiles are exogenous), so it suffices to compare the conditional expectations. By Lemma 2.9,
```
  E^{(b)}[ T_j(C;n) | B = beta ] = E[ tilde T_j^{(b)}(s) ],
```
where `tilde T^{(b)}` is the count vector of the `s`-round KH-UCB(n, pi_C) instance run on independent
Bernoulli own-count tapes with arm means `(bar m^{(b)}_{a,C})_a`, and
```
  bar m^{(0)}_{i,C} = E[m_{i,n}(X)|C] <= E[M_i(x_i)|C] = bar m^{(1)}_{i,C},
  bar m^{(0)}_{a,C} = bar m^{(1)}_{a,C}   for every a != i,
```
the inequality because `m_{i,n}(X) <= M_i(x_i)` pointwise (feasibility of `S_HDS` maps) and the integral
is monotone. Now realize BOTH auxiliary instances on one probability space: draw `pi_C` once, draw an
array `(U_{C,a,r})_{a in [K], r <= s}` of i.i.d. uniforms once, and set
`Z^{(b)}_{a,r} := 1{ U_{C,a,r} <= bar m^{(b)}_{a,C} }`. Each `Z^{(b)}` has the required law (independent
Bernoulli with the stated means), and `Z^{(1)}_{i,r} >= Z^{(0)}_{i,r}` for every `r` while
`Z^{(1)}_{a,r} = Z^{(0)}_{a,r}` for `a != i`. Corollary 2.4 (with arm `i` in the role of arm `1`, and the
single ex ante priority `pi_C` used for the initialization and for every later tie) gives, on every
sample point and for every local time `k <= s`,
```
  tilde T_j^{(1)}(k) <= tilde T_j^{(0)}(k)  for every j != i,     tilde T_i^{(1)}(k) >= tilde T_i^{(0)}(k).
```
Taking `k = s` and expectations, `E^{(1)}[T_j(C;n)|B=beta] <= E^{(0)}[T_j(C;n)|B=beta]` and
`E^{(1)}[T_i(C;n)|B=beta] >= E^{(0)}[T_i(C;n)|B=beta]`. For `beta = 0` both sides vanish. Averaging over
`beta` (same law in both executions) closes Step 2, and with Step 1 proves
`E^{(1)} T_j(R;n) <= E^{(0)} T_j(R;n)` and `E^{(1)} T_i(R;n) >= E^{(0)} T_i(R;n)`, with zero remainder,
for every `n` and every measurable `R`.

**Step 3 (mixtures).** If agents randomize independently ex ante over maps, condition on the realized
profile of maps: Steps 1 and 2 hold for every realization, with the same zero remainder, so the
inequality survives averaging (requirement 6). The comparison in the theorem is between agent `i`'s
mixture and the deterministic map `M_i`; conditioning on `i`'s realized map and averaging gives it.

**Step 4 (per-round tie coins).** If the cell rule breaks ties by a fresh uniform coin at each cell
round instead of by `pi_C` (and initializes by choosing uniformly among the count-zero agents, which is
the `f_a(0) = +infinity` case of Proposition 2.6), replace Corollary 2.4 by Proposition 2.6 in Step 2,
applied conditionally on the realized tapes `Z^{(0)}, Z^{(1)}` (for fixed tapes the index sequences are
fixed and `f_i^{(1)} >= f_i^{(0)}` pointwise). The conclusion is unchanged, with zero remainder. The
pathwise conclusion of Step 2 is then false (Fact 2.6.1), but it is not needed. QED

**3.6.1 Where the one-priority-per-cell rule is checked.** Twice, and both are needed.
(a) *Initialization.* The first `min(s,K)` visits of a cell have some agent with count zero. In the
greedy-merge encoding, `f_a(0) = +infinity` for every `a`, so the lexicographic maximum is the
`pi_C`-first count-zero agent, which is the algorithm's initialization rule. Both coupled executions use
the SAME `pi_C`, hence the same initialization order, and the raise of agent `i`'s tape cannot change it.
This is what makes cells visited fewer than `K` times harmless: there the two executions have identical
selection sequences and the inequality holds with equality.
(b) *Every later tie.* Lemma 2.1 (Case 1 and Case 2) and Lemma 2.2(b) each resolve an equality case by
the same strict order at two different steps of the run; a fresh coin at each step would not be available
at the second of those steps. Fact 2.6.1 exhibits the resulting failure with an explicit tape.
I therefore recommend that the paper state the algorithm with ONE priority permutation per instance,
drawn uniformly ex ante and used for both purposes. A rule that used `pi_C` for initialization and an
independent fixed permutation for later ties is not covered by Theorem 2.3 as stated and I do not claim
it.

**3.6.2 Random visit counts, light cells, zero-mass cells.** All handled by the conditioning on `B` in
Step 2: `V_C = s` is deterministic given `B`, Lemma 2.7 and Corollary 2.4 are statements about a
deterministic number of rounds, and the law of `B` does not depend on the maps. Cells with `s < K`, and
cells in which some agent is never selected, are included with no special treatment (see 3.6.1(a) and
the three cases listed after Lemma 2.10). Cells with `nu(C) = 0` are never visited and are omitted from
every sum.

**3.6.3 Why this is an expectation statement and not a pathwise one.** Under the natural actual-visit
coupling (same profiles `X^{(k)}`, same seeds `U^{(k)}_a` per visit, same `pi_C`), raising `m_{i,n}`
pointwise gives `1{U^{(k)}_i <= M_i(x^{(k)}_i)} >= 1{U^{(k)}_i <= m_{i,n}(X^{(k)})}` at every VISIT `k`.
But the index of agent `i` at own count `r` is a function of the rewards of its first `r` selections, and
those selections occur at different visits in the two executions as soon as the executions diverge; the
own-count tape of agent `i` is therefore NOT coordinatewise monotone, and Theorem 2.3 is not applicable.
This is the ambiguity recorded in Section 14.1 of the contract. I neither prove nor disprove pathwise
contextual monotonicity for Static Grid KH-UCB; it is OPEN, and the theorem is stated in expectation.
(For Static Grid-ETC the corresponding pathwise statement IS available, because there the exploration
pulls occur at reward-independent visits, so the same visit carries the comparison; that argument does
not transfer to an adaptive index rule.)

### 3.7 Proof of Theorem C(i) (target S4: contextual sharp adaptivity)

Fix `n >= 2`, a realized map profile in `S_HDS`, an agent `i`, and any measurable `R`. Since
`c_{i,t} = m_{i,n}(X_t) - mu_i(x_{i,t})`, the claim is equivalent to
```
  Lambda := E sum_{t<=n} 1{X_t in R, I_t = i} [ b(X_t) - m_{i,n}(X_t) ]
          <= L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 J_n + n nu((partial R)^{sqrt(D) h_n}).   (3.1)
```
Split the cells into three groups: `C subseteq R`, `C subseteq R^c`, and cells meeting both.

*Cells `C subseteq R^c`* contribute `0` to `Lambda`.

*Cells `C subseteq R` with `nu(C) > 0`.* Apply Lemma 2.10 in integrated form with
`phi = b - m_{i,n}` (bounded and measurable, `|phi| <= 1`) and `j = i`, noting `C cap R = C`:
```
  E sum_{t<=n} 1{X_t in C, I_t=i} [b(X_t) - m_{i,n}(X_t)] = ( bar b_C - bar m_{i,C} ) E T_i(C;n).
```
By Lemma 2.12, `bar b_C - bar m_{i,C} <= (bar m^*_C - bar m_{i,C}) + L sqrt(d) h_n = Delta_{i,C} + L sqrt(d) h_n`
with `Delta_{i,C} := bar m^*_C - bar m_{i,C} >= 0`. Hence the contribution of `C` is at most
```
  Delta_{i,C} E T_i(C;n) + L sqrt(d) h_n E T_i(C;n) <= Delta_{i,C} E T_i(C;n) + L sqrt(d) h_n E V_C .
```
For the first term, condition on the membership pattern `B = beta` with `V_C = s <= n`: by Lemma 2.9 the
cell execution has the law of the `s`-round instance of Lemma 2.7 with means `bar m_{a,C}`, so
Lemma 2.7(ii) gives `Delta_{i,C} E[T_i(C;n)|B=beta] <= 4 sqrt(s log n) + 3`. Averaging over `beta` and
using Jensen (`E sqrt(V_C) <= sqrt(E V_C)`),
`Delta_{i,C} E T_i(C;n) <= 4 sqrt(E V_C log n) + 3`.

*Cells meeting both `R` and `R^c`.* Bound the summand crudely by `b(X_t) - m_{i,n}(X_t) <= 1` (as
`b <= 1` and `m_{i,n} >= 0`), so the contribution of such a cell is at most
`E sum_t 1{X_t in C cap R} <= E V_C = n nu(C)`. By Lemma 2.15 the union of these cells is contained in
`(partial R)^{sqrt(D) h_n}`, so their total contribution is at most `n nu((partial R)^{sqrt(D) h_n})`.

*Summation.* There are at most `J_n` cells, and `sum_C E V_C <= n` (with equality over all cells). By
Cauchy-Schwarz, `sum_{C subseteq R} sqrt(E V_C) <= sqrt(J_n sum_C E V_C) <= sqrt(J_n n)`. Therefore
```
  Lambda <= L sqrt(d) h_n n + 4 sqrt(J_n n log n) + 3 J_n + n nu((partial R)^{sqrt(D) h_n}),
```
which is (3.1). Lemma 3.5 converts the first three terms into
`(L sqrt(d) + 4 . 2^{D/2} + 3 . 2^D) n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}`. Every bound used is uniform
over map profiles in `S_HDS`, so conditioning on the realized maps extends it to independent ex ante
mixtures. QED

**Remark.** Compared with the target remainder `2 L sqrt(D) n h_n + C_1 sqrt(J_n n log n) + C_2 J_n + n nu((partial R)^{sqrt(D) h_n})`
of TASK.md, the Lipschitz constant is `L sqrt(d)` rather than `2 L sqrt(D)` (lesson L2, applied in the
one-step form of Lemma 2.11: the honest comparison never leaves a single function, so no two-step chain
through a distinguished point occurs), and `C_1 = 4`, `C_2 = 3` are absolute constants, not
`K`-dependent. Since `sqrt(d) <= 2 sqrt(D)`, the stated target follows a fortiori.

### 3.8 Proof of Theorem C(ii) (target S5: robustness; restatement with constants)

This is `thm:grid-ucb-robust` of the manuscript, already proved there for the anytime index; as
instructed by requirement 4 I only restate it for KH-UCB with the constants coming from Lemma 2.7(iii).
Fix a realized map profile in `S_HDS`. For a cell `C` with `nu(C) > 0`, apply Lemma 2.10 in integrated
form once per agent, with `phi = b - m_{a,n}`:
```
  E sum_{t<=n} 1{X_t in C} [b(X_t) - m_{I_t,n}(X_t)] = sum_a (bar b_C - bar m_{a,C}) E T_a(C;n)
     = E[ sum_{k <= V_C} ( bar b_C - bar m_{A_k,C} ) ].
```
By Lemma 2.12, `bar b_C <= bar m^*_C + L sqrt(d) h_n`, so the right side is at most
`L sqrt(d) h_n E V_C + E[ sum_{k<=V_C} (bar m^*_C - bar m_{A_k,C}) ]`. Conditioning on `B = beta` and
applying Lemma 2.9 and then Lemma 2.7(iii) with `s = V_C <= n` gives
`E[ sum_{k<=V_C} (bar m^*_C - bar m_{A_k,C}) | B = beta ] <= 8 sqrt(K s log n) + 3K`; averaging, using
Jensen, summing over the at most `J_n` cells and applying Cauchy-Schwarz as in Section 3.7:
```
  E sum_{t<=n} [ b(X_t) - m_{I_t,n}(X_t) ] <= L sqrt(d) n h_n + 8 sqrt(K J_n n log n) + 3 K J_n .
```
Since `P(n) = E sum_t m_{I_t,n}(X_t)`, this is Theorem C(ii); Lemma 3.5 gives the stated rate. QED

### 3.9 Proof of Theorem C(iv) (target S6: expected FATA)

Let `G := G_{ij}(R)` and assume `m_{i,n}(X) = m_{j,n}(X) = M_*(X)` for every `X in G`. Decompose
`T_i(G;n) = sum_C T_i(C cap G; n)` over the cells.

*Cells with `C cap G = empty`* contribute `0` to both counts.

*Cells `C subseteq G` with `nu(C) > 0`.* Then `bar m_{i,C} = bar m_{j,C} = E[M_*(X)|C]` (both maps equal
`M_*` on all of `C`), and `T_i(C cap G;n) = T_i(C;n)`. By Lemma 2.9 the cell execution has the law of the
auxiliary instance with independent own-count tapes; in that instance the tapes of `i` and `j` are
i.i.d. Bernoulli with the SAME parameter, the other tapes are independent of them, and `pi_C` is uniform.
The label-swap argument of Theorem A(iv), applied verbatim to the auxiliary instance conditionally on
`B = beta`, gives `E[T_i(C;n)|B=beta] = E[T_j(C;n)|B=beta]` for every `beta`; averaging,
`E T_i(C;n) = E T_j(C;n)`.

*Cells meeting both `G` and `G^c`.* Since `T_i(C cap G;n) + T_j(C cap G;n) <= V_C`, we have
`|E T_i(C cap G;n) - E T_j(C cap G;n)| <= E V_C = n nu(C)`; by Lemma 2.15 (applied with `R = G`) the union
of these cells lies in `(partial G)^{sqrt(D) h_n}`, so their total contribution to the difference is at
most `n nu((partial G)^{sqrt(D) h_n})`.

Adding up, `|E T_i(G;n) - E T_j(G;n)| <= n nu((partial G)^{sqrt(D) h_n})`. If `nu(partial G) = 0` then,
since `partial G` is closed and `(partial G)^{eps}` decreases to `partial G` as `eps` decreases to `0`,
continuity from above of the finite measure `nu` gives `nu((partial G)^{eps}) -> 0`, and `h_n -> 0`, so
the remainder is `o(n)`. Uniformity over `S_HDS` and mixtures: the premise is a condition on the two
maps, and for every pair of maps satisfying it the bound is the same, so conditioning on the realized
maps extends the statement to mixtures supported on maps satisfying the premise. QED

### 3.10 Proof of Theorem C(v) (target S7: revenue at all-maximum play)

Assume every `M_a` is `L`-Lipschitz and every agent plays `m_{a,n} = M_a`. Repeat Section 3.8 verbatim
with `b` replaced by `M_*` and Lemma 2.12 replaced by Lemma 2.13 (`bar M_{*,C} <= bar m^*_C + L sqrt(d) h_n`,
where now `bar m^*_C = max_a bar M_{a,C}`):
```
  E sum_{t<=n} [ M_*(X_t) - M_{I_t}(x_{I_t,t}) ] <= L sqrt(d) n h_n + 8 sqrt(K J_n n log n) + 3 K J_n,
```
and `P(n;S^max) = E sum_t M_{I_t}(x_{I_t,t})`. QED

### 3.11 Proof of Theorem C(vi) (target S8: public restricted equilibrium)

Assume every `M_a` is `L`-Lipschitz and `nu(|T(X)| >= 2) = 1`. Fix an agent `i` and a deviation
`m'_{i,n} in S_HDS`, deterministic for now; all other agents play `M_a`. Write `T'` for counts under the
deviation and `T` for counts under `S^max`.

**Step 1 (per-cell decomposition of the gain).** Agent `i`'s utility is
`u_i = E sum_{t<=n} 1{I_t = i} (1 + mu_i(x_{i,t}) - m_{i,n}(X_t))`. By Lemma 2.10 in integrated form
applied in each cell with `phi = 1 + mu_i(x_i) - m_{i,n}(X)`,
```
  u_i(n; S^max) = sum_{C : nu(C)>0} a_C . E T_i(C;n),
  u_i(n; m'_{i,n}, S^max_{-i}) = sum_{C : nu(C)>0} (a_C + delta_C) . E T'_i(C;n),
```
where
```
  a_C := E[ 1 + mu_i(x_i) - M_i(x_i) | C ] >= 0     (pointwise 1 + mu_i - M_i >= 0 since M_i <= 1, mu_i >= 0),
  delta_C := E[ M_i(x_i) - m'_{i,n}(X) | C ] >= 0   (pointwise, by feasibility of the deviation).
```
Zero-mass cells never contribute. Hence
```
  gain = sum_C [ (a_C + delta_C) E T'_i(C;n) - a_C E T_i(C;n) ]
       = sum_C [ delta_C E T'_i(C;n) + a_C ( E T'_i(C;n) - E T_i(C;n) ) ]
      <= sum_C delta_C E T'_i(C;n),
```
because `a_C >= 0` and, by Theorem C(iii) Step 2 applied to the raise of agent `i`'s map from
`m'_{i,n}` to `M_i` (self-monotonicity: `tilde T_i` weakly increases in Corollary 2.4),
`E T'_i(C;n) <= E T_i(C;n)` for every cell.

**Step 2 (per-cell bound).** Fix a cell `C` with `nu(C) > 0`. In the deviating execution the auxiliary
cell means are `bar m'_{i,C} = bar M_{i,C} - delta_C` for agent `i` and `bar M_{a,C}` for `a != i`. Put
```
  Delta'_C := max_{a != i} bar M_{a,C} - ( bar M_{i,C} - delta_C ) .
```
By Lemma 2.14, `max_{a != i} bar M_{a,C} >= bar M_{i,C} - 2 L sqrt(d) h_n`, hence
`Delta'_C >= delta_C - 2 L sqrt(d) h_n`. Condition on `B = beta` with `V_C = s <= n` and use Lemma 2.9.
Two cases.
- If `Delta'_C > 0`, agent `i` is suboptimal in the cell instance with gap exactly `Delta'_C`, so
Lemma 2.7(ii) gives `Delta'_C E[T'_i(C;n)|B=beta] <= 4 sqrt(s log n) + 3`, and therefore
```
  delta_C E[T'_i(C;n)|B=beta] <= (Delta'_C + 2 L sqrt(d) h_n) E[T'_i(C;n)|B=beta]
                               <= 4 sqrt(s log n) + 3 + 2 L sqrt(d) h_n s,
```
using `E[T'_i(C;n)|B=beta] <= s`.
- If `Delta'_C <= 0`, then `delta_C <= 2 L sqrt(d) h_n` and
`delta_C E[T'_i(C;n)|B=beta] <= 2 L sqrt(d) h_n s`.
In both cases `delta_C E[T'_i(C;n)|B=beta] <= 4 sqrt(s log n) + 3 + 2 L sqrt(d) h_n s`.

**Step 3 (summation).** Averaging over `beta`, using Jensen and then Cauchy-Schwarz over the at most
`J_n` positive-mass cells with `sum_C E V_C <= n`,
```
  gain <= sum_C [ 4 sqrt(E V_C log n) + 3 + 2 L sqrt(d) h_n E V_C ]
       <= 4 sqrt(J_n n log n) + 3 J_n + 2 L sqrt(d) n h_n
        <= (2 L sqrt(d) + 4 . 2^{D/2} + 3 . 2^D) n^{(D+1)/(D+2)} (log(en))^{1/(D+2)}
```
by Lemma 3.5. Since `sqrt(d) <= sqrt(D)`, this implies the target bound with `2 L sqrt(D) n h_n`.

**Step 4 (mixtures and conclusion).** For an independent ex ante mixture, condition on agent `i`'s
realized map: the bound of Step 3 is the same for every deterministic map in `S_HDS`, so the mixture's
gain, being an average of the conditional gains, obeys it too (requirement 6). Because the bound is
`o(n)`, `S^max` is an `S_HDS`-asymptotic equilibrium in the sense of Definition 1 of the manuscript, and
the rate is uniform over deviations. QED

**Remark 3.11.1 (what the two-top-almost-everywhere hypothesis is doing).** It is used exactly once, in
Lemma 2.14, to guarantee that in EVERY positive-mass cell the deviator faces a rival whose cell average
is within `2 L sqrt(d) h_n` of its own. No case split into top and non-top agents is needed and no
component structure, closed null separator, or continuity beyond Lipschitzness of capacities is used.
If the hypothesis fails on a set `W_i` of positive mass on which `i` is the unique top agent, the
conclusion is false in general: shading by half the capacity gap on `W_i` keeps `i` best there and saves
effort at a linear rate. I did not verify that necessity direction in detail and do not claim it here.

### 3.12 Every step at which the known-horizon index is used in place of the anytime index (lesson L3)

The substitution `hat m_a + sqrt(2 log t / T_a) -> hat m_a + sqrt(4 log n / T_a)` is the entire content
of this candidate. The following steps use it, and each would fail or become unproven for the anytime
index. FAILS means a counterexample exists; UNPROVEN means I have neither proof nor counterexample.

1. Corollary 2.4 and Corollary 2.5 (scalar pathwise monotonicity). FAILS for the anytime index: explicit
tape in Section 3.3 (`K = 3`, `n = 8`), re-verified in this session. The reason is structural: Theorem 2.3
needs each arm's index to be a function of its OWN count and its own reward prefix only; the anytime
bonus depends on the global round.
2. Theorem A(i) (target S1, monotonicity). FAILS, same tape.
3. Theorem B(ii) (target S2, finite-context monotonicity, pathwise and exact). FAILS: embed the tape of
Section 3.3 in a single profile `z` that is visited `8` times.
4. Theorem C(iii) Step 2 (target S3, grid exact expected monotonicity). UNPROVEN for the anytime index.
The auxiliary cell instance would then be a bandit whose index depends on the cell's local time `k` as
well as on the own count, so Corollary 2.4 is unavailable; the tape of Section 3.3, transplanted into a
single cell (any `nu` supported in one cell, with cell averages in `(0,1)` so the tape has positive
probability), shows that the PATHWISE version of Step 2 is false even in the auxiliary model. Whether the
expectation survives is exactly the open question of Section 3.3.
5. Theorem C(vi) Step 1 (target S8, self-monotonicity `E T'_i(C;n) <= E T_i(C;n)`). UNPROVEN for the
anytime index, for the same reason as item 4. This is the only place where S8 needs monotonicity; the
rest of S8 (Lemma 2.14 and the deficit bound) is index-agnostic up to constants.
6. Theorem A'(scalar public) and Theorem B(v) (finite-context public), Step "self-monotonicity".
UNPROVEN for the anytime index; the manuscript's `thm:public-ucb` avoids this by a fixed-gap argument
that is not uniform over deviations, which is why its bound degrades as the deviation gap vanishes.
7. Lemma 2.7 and everything built on it (targets S4, S5, S6, S7, and the deficit half of S8). These do
NOT require the known-horizon index: the anytime index admits the analogous fixed-gap and gap-free bounds
(this is what the manuscript already uses, citing Auer, Cesa-Bianchi and Fischer 2002). Only the
constants change. I nevertheless state everything for the known-horizon index so that a single algorithm
serves all six parts of Theorem C.
8. The union bound in the proof of Lemma 2.7, `sum_{r=1}^{n} delta = n delta = 1/n`, uses that the
confidence level `1/n^2` is set from the GLOBAL horizon and is the same in every cell. A rule that used
the cell's own visit count in the logarithm would need a different argument, and I prove nothing about
such a rule.

## 4. Assumption usage list

For each hypothesis, exactly which statements use it and where.

1. **Known horizon `n`, used in the index as `sqrt(4 log n / T)`, and one ex ante priority per instance.**
Used in: Corollaries 2.4 and 2.5; Theorem A(i); Theorem B(ii); Theorem C(iii) Step 2; Theorem C(vi)
Step 1; Theorem A'(self-monotonicity); Theorem B(v)(self-monotonicity). Also in Lemma 2.7, where the
confidence level `1/n^2` is global (see item 8 of Section 3.12). See Section 3.12 for the full flag list.

2. **Exogenous profiles, independent of reward seeds, priorities and private coins.** Used in Lemma 2.8
(conditional cell law), and hence in Lemma 2.9, Lemma 2.10 and everything in Sections 3.6 to 3.11. Also
used in Theorem C(iii) Step 2 to assert that the LAW OF THE MEMBERSHIP SEQUENCE is unchanged when a map
changes. For finite contexts (Theorem B parts (i) to (iv)) exogeneity and independence of the reward
tapes suffice; the arrivals need not be i.i.d. there, as the manuscript's appendix A.1 also says.

3. **Profiles i.i.d. `nu`.** Used in: Lemma 2.8 (this is where i.i.d. enters, and it is the only place);
`E V_C = n nu(C)` in Lemmas 2.15, 3.7 to 3.11; the boundary accounting of Theorem C(i) and C(iv). It is
NOT used in Theorem B parts (i) to (iv). It is used in Theorem B(v) only for the `O(log n)` revenue
refinement. The counterexample of contract item 11.5 (deterministic alternating contexts) shows the cell
law is false without it.

4. **Fixed ex ante maps (`S_HDS`, or `S_F` in the finite case).** Used in Lemma 2.9: `bar m_{a,C}` is the
integral of a FIXED map, and the induction (2.3) needs the target at a visit to be a function of the
profile at that visit only. A target that depends on the cell's local visit count, on a phase, or on past
rewards destroys the reduction. Used in Theorem B through the statement "conditional on the arrivals the
instance at `z` is a fixed-mean instance". Mixtures are handled by conditioning on the realized map
(requirement 6), used in Theorem B (final paragraph), Theorem C(iii) Step 3, C(i) last sentence, and
C(vi) Step 4.

5. **Honesty of honest agents (`m_{h,n} >= mu_h` pointwise).** Used only in Lemma 2.12, hence in
Theorem C(i) and C(ii), and in the finite-context analogue inside Theorem B(i) and B(iv). Not used
anywhere else.

6. **`mu_a` `L`-Lipschitz for every `a`.** Used only through Lemma 2.11 and Lemma 2.12, hence only in
Theorem C(i) and C(ii). Capacities need not be Lipschitz for those two parts.

7. **`M_a` `L`-Lipschitz for every `a`.** Used in Lemma 2.13 (hence Theorem C(v)) and Lemma 2.14 (hence
Theorem C(vi)). Not used in C(i) to C(iv).

8. **`nu(|T(X)| >= 2) = 1` (two top agents almost everywhere).** Used exactly once, in Lemma 2.14, hence
only in Theorem C(vi). In the finite-context Theorem B(v) the corresponding hypothesis is `|T(z)| >= 2`
for every `z`, used once in the same way (with no Lipschitz error, since a profile is a point).
`K_top >= 2` plays the same single role in Theorem A'.

9. **Feasibility `m_{a,n}(X) in [0, M_a(x_a)]` and `M_a <= 1`, `mu_a >= 0`.** Feasibility is used in
Corollary 2.5 (tape domination), Theorem C(iii) Step 2 (`bar m_{i,C} <= bar M_{i,C}`), and
Theorem C(vi) Step 1 (`delta_C >= 0`). The bounds `M_a <= 1`, `mu_a >= 0` are used only for `a_C >= 0`
in Theorem C(vi) Step 1, for `a_i >= 0` in Theorem A', and for `Delta_a <= 1` in Lemma 2.7(ii) and (iii).

10. **Boundary conditions on `R`.** Theorem C(iii) needs NONE: it holds for every measurable `R`, with
zero remainder. Theorem C(i) carries the additive boundary term `n nu((partial R)^{sqrt(D) h_n})` for
every measurable `R`, which is `o(n)` exactly when `nu(partial R) = 0` (continuity from above).
Theorem C(iv) needs `nu(partial G_{ij}(R)) = 0` to make its remainder `o(n)`, and the boundary of the
SHARED-TOP portion is what matters, not the boundary of `R`.

11. **Cell geometry.** Convexity of cells is used in Lemma 2.15 (a connected set meeting `R` and `R^c`
meets `partial R`). `diam(C) <= sqrt(D) h_n` is used in Lemma 2.15; the finer per-block bound
`|x_a - x'_a| <= sqrt(d) h_n` is used in Lemma 2.11 and hence in Lemmas 2.12, 2.13, 2.14 (lesson L2).

12. **Lesson L1 (no filtration, no nesting, no martingale).** No step of this file uses a filtration, a
nested grid, Levy's upward theorem, or any martingale convergence statement. The cell-average
convergence lemma of L1 is not needed here either: all the approximation errors are controlled by the
explicit Lipschitz rate `L sqrt(d) h_n` of Lemma 2.11, and the only limit taken is
`nu((partial R)^{eps}) -> nu(partial R)` by continuity from above of a finite measure, which is
elementary. Lemma 2.7 is proved by a union bound over a DETERMINISTIC index range `r in {1,...,n}` and
Hoeffding-type tail bounds for sums of a fixed number of independent variables; no stopped process
appears. The single place where a "random index" could have tempted a martingale argument is the
comparison of `hat theta_{1, T_1(t-1)}` with `theta_1`, and it is handled by the union bound over all
possible values `r` of `T_1(t-1)`, exactly as in the source.

## 5. Self-audit

**What I verified myself in this session, and how.**
- I read the primary source for the imported bandit bound (Lattimore and Szepesvari, PDF downloaded to
scratch, text extracted with ghostscript and read directly) and recorded the exact statements of
Definition 5.2 (page 77), Corollary 5.5 (page 78), Exercise 5.11(a) (page 84), Algorithm 3 (page 103),
Theorem 7.1 (page 105) and Theorem 7.2 (page 108). I did NOT import Theorem 7.1 as a black box: the
book's statement is for an instance run for exactly `n` rounds, whereas a cell runs for a random
`s <= n` rounds, so I reproved the per-arm bound in the form `E T_a(s) <= 3 + 16 log(n)/Delta_a^2` for
every `s <= n` (Lemma 2.7(i)), following the book's argument, with every constant recomputed. The same
for the gap-free bound (Lemma 2.7(iii)), where I recomputed the optimization and obtained the book's
`8 sqrt(K s log n) + 3K` with `n` in the logarithm and `s` in the square root.
- I re-verified the anytime counterexample of Claim L3 by running the rule on the stated tape
(Section 3.3): base counts `(2,1,5)`, raised counts `(2,2,4)`. VERIFIED, exactly as claimed.
- I verified the per-round tie-coin counterexample (Fact 2.6.1): base counts `(1,6,1)`, raised counts
`(3,3,2)`, so arm 3's count rises. VERIFIED. (The scout's Section C.1 reports the counts after round 6,
`(1,4,1)` and `(3,1,2)`; my run to the full horizon `n = 8` gives `(1,6,1)` and `(3,3,2)`. The
conclusion, `T_3` strictly increases, is the same, and the two are consistent: the prefix through round
6 agrees with the scout's trace.)
- I re-derived the static race lemma (Theorem 2.3) from scratch, checking each equality case of the
priority argument; I then also ran 200000 random static-race instances and 100000 random KH-UCB
instances as a sanity check (0 violations). These searches are sanity checks only; the proofs are the
evidence.
- I ran a small Monte Carlo of Static Grid KH-UCB (`grid_check.py`, `D = 2`, `K = 2`, `h = 0.5`,
`n = 60`, 4000 replications per profile) to sanity check Lemma 2.10 and Theorem C(iii): the ratio
`E T_j(C cap R;n) / E T_j(C;n)` came out `0.503` in the two cells with `nu(R|C) = 0.5` and `0.000` in the
two cells with `nu(R|C) = 0`, and `E T_j(R;n)` fell from `7.98` to `5.52` when the other agent's map was
raised to capacity. Consistent with the proofs; again, a sanity check only.

**Compute.** No Slurm job was submitted. All computation was three short scripts (`checks.py`,
`grid_check.py`, and a ghostscript text extraction of the downloaded book PDF) run with the venv python
on the login node, together well under five minutes. No COMPUTE_LOG.md was created because my role brief
restricts me to this single output file.

**Claims of others that I used, and their status with me.**
- The scout report `scouts/MONOTONE_UCB.md` Sections B and C: I did not use it as evidence. I reproved
Lemmas 2.1, 2.2, Theorem 2.3 and Proposition 2.6 independently; my proofs agree with the scout's
structure, and in re-checking the scout's Theorem C.1 I found the two-stage coin argument correct
(the point that needs care, and that I checked explicitly, is that the history up to step `t` is a
function of `xi_{1..L_t}` and `eta_{1..t-1}`, so `xi_{L_t+1}` is fresh).
- `LEAD_PRELIMINARY_CLAIMS.md` Claims L1, L2, L3: L1 and L2 are now Theorem 2.3 and Lemma 2.1 with
proofs; L3 is verified above. Claim L4 is now Theorem C(iii) with a complete proof, except that L4's
sentence "so `E T_j(C;n)` weakly decreases for every cell, and `E T_j(R;n) = sum_C nu(R|C) E T_j(C;n)`"
required the conditioning of Lemma 2.10 to be done on the whole membership pattern, not on `V_C` alone;
`V_C` alone is not enough, because the identity needs `A_k` to be independent of `X^{(k)}`, which is a
statement about the conditional law of the ordered visiting profiles. Claim L5 is superseded by
Lemma 2.14 plus Theorem C(vi); note that L5 writes the rival inequality with `bar M_C` where
`bar M_{i,C}` is needed (the two coincide only when `i` is top throughout the cell), and the ledger's
Section 3 records the same correction; my Lemma 2.14 uses `bar M_{i,C}` and is correct as stated.
- `MATH_CANDIDATE_LEDGER.md` Section 1: its statement of C1 is what I proved, with the improvements
listed in Section 0 above. Its assertion that the deficit bound is "valid for any `s <= n` since its
confidence level is `1/n^2` over the horizon" is correct but was not proved there; Lemma 2.7 proves it.

**Gaps, weaknesses and things I could not close.**
1. **Pathwise contextual monotonicity for Static Grid KH-UCB is OPEN.** Section 3.6.3 explains why the
actual-visit coupling does not give it. I neither prove it nor refute it. The theorem is therefore stated
in expectation, which is what C1(iii) asks for. If a referee asks whether Grid-KH-UCB can match
Grid-ETC's PATHWISE monotonicity, the honest answer is "not known".
2. **Exact expected monotonicity of anytime UCB1 is OPEN.** I make no claim either way; the pathwise
version is false (Section 3.3).
3. **The necessity direction for the two-top-almost-everywhere hypothesis is not proved here** (Remark
3.11.1). I state only that the hypothesis is used once and where; I did not verify the converse.
4. **Theorem C(vi) bounds the gain of a unilateral deviation by agent `i` when all other agents play
`S^max`.** It is not a bound on gains against arbitrary other profiles, and it is not a statement about
behavioral (history-dependent) contextual deviations; the contract's `B^ctx_{i,n}` is outside the scope
of every theorem in this file, because Corollary 2.5's blindness hypothesis fails as soon as an agent
observes `X_t` (Caveat 2.5.1).
5. **The grid partition.** TASK.md and the manuscript write the partition of `[0,1)^D` while the context
space is `[0,1]^D`. I closed the face `{x_l = 1}` into the last cell in each coordinate (Section 1.0).
This is cosmetic but must be written down, or the cells do not partition `X` and the sum in Lemma 2.10
is not exhaustive.
6. **`n >= 2` is needed** so that `log n > 0` and the index is well defined; all statements are for
`n >= 2` and are vacuous or trivial below that. If the paper prefers `log(en)` in the index, every bound
above holds verbatim with `log n` replaced by `log(en)`, since the proof of Lemma 2.7 only uses
`delta = n^{-2} <= exp(-2 log n)`.
7. **Constants.** I have not tried to optimize `4`, `3`, `8 sqrt(K)`, `3K`, `2^{D/2}`, `2^D`. The
`2^{D/2}` and `2^D` come from `ceil(1/h_n) <= 2/h_n`; they can be reduced to `(1 + h_n)^{D/2}` and
`(1+h_n)^D` when `h_n` is small, which matters for readability only.
8. **Uniformity in `K` and `D`.** Every constant is explicit and depends only on `K`, `D`, `L` as
stated; none of them is uniform in `D` (they are exponential in `D`, as `J_n` is), and no minimax
optimality in `D` is claimed anywhere (requirement 8).
9. **What I did not check.** I did not verify the manuscript's Grid-ETC proofs, the private mechanism, or
any experiment. I did not read the other prover's or the adversary's files, as instructed. I did not
re-derive the ICML 2020 and AAAI 2025 lemmas line by line; I verified their existence, numbering and
scope from the sources listed in Section 6 and I do not rely on them for any step.

**Explicit statement required by COMMON.md rule 9.** I do not claim this file is error free. The parts I
consider most likely to need a second reading are: the equality cases in the proof of Lemma 2.1, part (d)
of Lemma 2.2, the induction (2.3) in Lemma 2.9, and the independence claim in Lemma 2.10 (that `A_k` is
independent of `X^{(k)}` conditionally on the membership pattern), because the whole of S3, S4, S6, S7
and S8 rests on it.

## 6. Verified references, with URLs

All fetched or downloaded and read on 17 September 2026.

1. T. Lattimore and C. Szepesvari, *Bandit Algorithms*, Cambridge University Press, 2020. PDF:
https://tor-lattimore.com/downloads/book/book.pdf (downloaded in this session, 5400750 bytes; text
extracted with ghostscript `-sDEVICE=txtwrite` and read). Pages read and used:
   - page 77, Definition 5.2 (`sigma`-subgaussian: `E exp(lambda X) <= exp(lambda^2 sigma^2/2)`);
   - page 78, Corollary 5.5 (`Pr(hat mu >= mu + eps) <= exp(-n eps^2/(2 sigma^2))` and the lower tail,
     for independent `sigma`-subgaussian summands);
   - page 84, Exercise 5.11(a) (Hoeffding's lemma: zero mean and support in `[a,b]` implies
     `(b-a)/2`-subgaussian; hence a centered Bernoulli, and any centered `[0,1]`-valued variable, is
     `1/2`-subgaussian and a fortiori `1`-subgaussian);
   - page 103, Algorithm 3 `UCB(delta)`, index `+infinity` at count zero and
     `hat mu_a + sqrt(2 log(1/delta)/T_a)` otherwise;
   - page 105, Theorem 7.1 (with `delta = 1/n^2`, `R_n <= 3 sum_a Delta_a + sum_{a : Delta_a>0} 16 log(n)/Delta_a`),
     whose proof establishes `E T_a(n) <= 3 + 16 log(n)/Delta_a^2`;
   - page 108, Theorem 7.2 (with `delta = 1/n^2`, `R_n <= 8 sqrt(n k log n) + 3 sum_a Delta_a`), which
     restates the per-arm bound `E T_a(n) <= 3 + 16 log(n)/Delta_a^2` and performs the gap split.
   Hypotheses of Theorems 7.1 and 7.2 as printed: a stochastic `k`-armed bandit in `E^k_{SG}(1)`, that
   is all arms `1`-subgaussian, and the algorithm is Algorithm 3 run for the same `n` that defines
   `delta`. My Lemma 2.7 restates and reproves these for an `s`-round instance with `s <= n` and
   `delta = 1/n^2`.

2. Z. Feng, D. C. Parkes and H. Xu, "The Intrinsic Robustness of Stochastic Bandits to Strategic
Manipulation", ICML 2020; arXiv: https://arxiv.org/abs/1906.01528 (fetched by me in this session: title
and authors confirmed; the abstract page shows v1 4 June 2019 and a revision 12 November 2020 and does
not print the venue, so the ICML 2020 attribution should be checked against the PMLR proceedings page
before submission). Relevant content: footnote 3 (the
`log T` width is used because it is convenient for equilibrium lower bounds), Lemma B.2 (arm coupling,
non-`i` subsequence) and Lemma B.3 (own pulls under the maximal investment strategy dominate pathwise).
Status in this file: cited as prior work for the conclusion of Theorem 2.3; NOT used as a step.

3. S. A. Esmaeili, S. Shin and A. Slivkins, "Robust Performance Incentivizing Algorithms for
Multi-Armed Bandits with Strategic Agents", AAAI 2025, vol. 39, no. 13, pp. 13814 to 13822, DOI
10.1609/aaai.v39i13.33510, https://ojs.aaai.org/index.php/AAAI/article/view/33510 (fetched by me in this
session: title, authors, volume, issue, pages, DOI and year confirmed as printed here); arXiv version
"Robust and Performance Incentivizing Algorithms for Multi-Armed Bandits with Strategic Agents",
https://arxiv.org/abs/2312.07929 (fetched by me in this session; v1 13 December 2023, v2 9 March 2025;
the arXiv abstract page lists no venue).
Relevant content: Appendix A Algorithm 3 (UCB index `hat mu_i + sqrt(2 ln(n)/T_i)`, ties arbitrary),
Definition 5.2 (pathwise monotonicity "for any reward seed and any strategy seed"), Theorem B.11 and
Claim B.12 (UCB is monotone, by coupling rewards by own pull count and the prefix property, credited to
Feng, Parkes and Xu). Status in this file: cited as prior work for the conclusion of Theorem 2.3 and for
the two-top condition; NOT used as a step.

4. P. Auer, N. Cesa-Bianchi and P. Fischer, "Finite-time Analysis of the Multiarmed Bandit Problem",
Machine Learning 47:235 to 256, 2002. This is the source the manuscript cites for its anytime UCB1
bound `E T_i(n) <= 8 log(n)/Delta_i^2 + 1 + pi^2/3`. Status in this file: mentioned only in Section 3.12
item 7, to record that the deficit half of the analysis does not depend on the index choice. I did not
re-verify its constants in this session and no step of this file uses it.

**Note on items 2 and 3.** I fetched the three URLs above myself in this session and confirmed titles,
authors and (for the AAAI entry) volume, issue, pages, DOI and year. I did NOT re-read the internal
lemma numbers (Feng et al. Lemmas B.2 and B.3; Esmaeili et al. Theorem B.11 and Claim B.12), which I
take from `MATH_CANDIDATE_LEDGER.md` Section 0; no step of this file depends on them, but the paper must
cite both works when stating the race lemma, since that lemma is not new, and someone should confirm the
lemma numbers against the PDFs before submission. The ICML 2020 venue of item 2 is not printed on the
arXiv abstract page and should be confirmed on the PMLR proceedings page.
