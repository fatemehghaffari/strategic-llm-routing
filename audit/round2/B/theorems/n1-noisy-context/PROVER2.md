# N1 PROVER 2: label-keyed local MESP under context-label noise

DONE

STATUS: DONE 2026-09-29. All parts written; numerics in prover2/ (e0-e5). Header was IN PROGRESS until this line was set.
Nothing else read yet beyond: the STATEMENT portions of SCOUT.md (Sec. 1.1-1.3, 5.1), the paper's model
(sections/sec2_model.tex) and the mechanism/statement block of sections/app_contextual_private.tex
(lines 1-223, i.e. up to and including the standing-conditioning paragraph, before Lemma ctx-locality).
No c2 file, no PROVER1 file, no paper proof read at the time Part 1 was written.

Naming. The paper calls the mechanism CL-MESP; the brief calls it PL-MESP. Same object: one independent
copy of monitored empirical second price per key. Here the key is the classifier LABEL. The reference
theorem is `prop:ctx-finite-exact` (the exact form of `thm:ctx-private-finite`), called "Prop. X" below.

---------------------------------------------------------------------------------------------------

## Part 0. Model, draws, hypothesis, statements

### 0.1 Primitives
- Agents `[K]`, `K >= 2`, honest set `K_H` nonempty. Horizon `n >= 2K`.
- Types `A` (finite), labels `Lab` (finite), `Q_B := |Lab|` (only labels that occur matter).
- Agent `j` has `mu_j(a) <= M_j(a)` in `[0,1]` for `a in A`, and ONE cost function `phi_j` on `[0,1]`,
  nondecreasing, convex, `Lambda`-Lipschitz, `phi_j(1) - phi_j(0) <= 1` (paper's (N), called (CN) here to
  avoid a clash with the noise hypothesis). The linear case `phi_j(m) = m` is `Lambda = 1`.
  (The cost function does not depend on the type; only the origin `mu_j(a)` does. This is the paper's model.)
- Posterior `pi_b` on `A` for each label `b` (a fixed probability vector, not known to the platform).
- Mixture primitives: `Mbar_j(b) := sum_a pi_b(a) M_j(a)`, `mubar_j(b) := sum_a pi_b(a) mu_j(a)`,
  `Vbar_i(b) := max_{j != i} Mbar_j(b)`, `dbar_i(b) := Vbar_i(b) - Mbar_i(b)`, `Mbar_(2)(b)` the second
  largest of `(Mbar_j(b))_j` with multiplicity, `bbar(b) := max_{h in K_H} mubar_h(b)`.
- Per-label effective cost of agent `j` at label `b`: with `lo_j(a) := mu_j(a)` if `j` honest, `0` otherwise,
  and `lobar_j(b) := sum_a pi_b(a) lo_j(a)`, for `y in [lobar_j(b), Mbar_j(b)]`
  `psi_{j,b}(y) := min { sum_a pi_b(a) phi_j(m(a)) : lo_j(a) <= m(a) <= M_j(a), sum_a pi_b(a) m(a) = y }`,
  `kappa_{j,b} := sum_a pi_b(a) phi_j(mu_j(a))`.

### 0.2 Mechanism (unchanged CL-MESP, keyed on labels)
Exactly the paper's CL-MESP (parameters `L_n, l_n = log(2n^4), s_n = sqrt(log(2Kn^4)/(2L_n)),
b_n(r) = sqrt(r l_n / 2), gamma_n, eta_n, R_K`) with "context `z`" replaced by "label `b`": lazily
instantiated local copy per label; Stage 1 round robin for the first `K L_n` visits; bids `beta_{j,b}`;
winner `W_b` = largest bid, ties by the priority `Pi_b`; price `tau_b = (beta_(2),b - s_n)_+`; Stage 2 pulls
`W_b` and switches when `Z_b < r_b tau_b - b_n(r_b)`; Stage 3 local EXP3 tuned to `n`. Messages to the
selected agent: the label, the local phase, the price once announced. The platform observes `B_t`,
never `X_t`.

### 0.3 Agents' information and the round
At round `t`: the platform sees `B_t`, draws its round-`t` coin `zeta_t` (used only in Stage 3), selects
`I_t` (a function of `B_1..B_t`, past rewards, `Pi`, `zeta_1..zeta_t`); the selected agent reads the
task, i.e. observes `X_t`, and chooses `m_t in [0, M_{I_t}(X_t)]`; the seed `U_t` is drawn and
`Y_t = 1{U_t <= m_t}`. Agent `I_t` pays `phi(m_t) - phi(mu(X_t))`; per-selection utility
`1 + phi(mu(X_t)) - phi(m_t) in [0,2]` by (CN) and monotonicity.

Deviation class `D_{i,n}`: `m_{i,t}` is any measurable function of `n`, the WHOLE label sequence
`B = (B_1..B_n)` (hence every visit count and the global round index), the current `X_t`, agent `i`'s
own history (its selection rounds, the labels and TRUE TYPES there, its targets, rewards, messages) and
its private coin array `xi_i`; feasible `m in [0, M_i(X_t)]`, honest agents `m >= mu_i(X_t)`. Not future
true types. (Contains the paper's `B^ctx+` with context read as label, plus the extra knowledge of the
true types of own past rounds.)

### 0.4 Enumeration of ALL draws and hypothesis (N), conditional form
Complete list of primitive draws, in this order:
1. `B = (B_1..B_n)`, the label sequence (arbitrary law; "exogenous": no agent's behaviour moves it, which
   is automatic here because it is drawn first and is a primitive);
2. the agents' private coin arrays `xi_1, .., xi_K` (arbitrary joint law given `B`);
3. the priorities `(Pi_b)_{b in Lab}`;
4. for `t = 1, .., n`, in this order: the mechanism coin `zeta_t`, the true type `X_t`, the seed `U_t`.

Every other random quantity (selections, bids, prices, switches, targets, rewards, messages) is a
measurable function of these draws and of the strategies. No draw is omitted: the platform has no other
randomness (Stage 1 and Stage 2 are deterministic given rewards), the rewards are functions of `(m_t, U_t)`,
the agents randomise only through `xi` (a behavioural strategy that randomises at round `t` is
represented by a coordinate of `xi_i` that it reads at round `t`).

**(N)** Each draw of items 3-4 has its specified law conditionally on `sigma(B)` together with every draw
listed before it: `Pi_b` uniform on permutations of `[K]`, `zeta_t` Uniform[0,1], `X_t` has law
`pi_{B_t}`, `U_t` Uniform[0,1].

Remarks. (a) Since each specified law is a fixed function of `B` only, (N) is equivalent to: conditionally
on `B`, the family `(xi, Pi, zeta_1, X_1, U_1, ..., zeta_n, X_n, U_n)` is such that `xi` has arbitrary law
and everything after it is independent of `xi` and mutually independent with the stated marginals. I use
only the conditional form. (b) Sufficient: `(X_t, B_t)` i.i.d. with joint law `p(a)C(a,b)` and independent
of seeds, coins and priorities, private coins depending on `B` at most. (c) (N) forbids an agent's coins
from predicting a future true type; that is why `D_{i,n}` excludes future `X`. (d) (N) is the analogue of the
paper's (A3-P) with the label path in the role of the arrival path, plus the new clause on `X_t`.

Filtrations (all include `sigma(B, xi, Pi)`):
- `G_t := sigma(B, xi, Pi, (zeta_s, X_s, U_s)_{s < t}, zeta_t)`: pre-type field at round `t` (selection
  `I_t`, label, phase, price are `G_t`-measurable);
- `G_t^- := G_t v sigma(X_t)`: pre-seed field (the target `m_t` is `G_t^-`-measurable);
- `F_t := G_t^- v sigma(U_t)`.

Consequences of (N) used below (the only probabilistic inputs):
- (P1) `P(X_t = a | G_t) = pi_{B_t}(a)`; (P2) `P(U_t <= u | G_t^-) = u`.
- (P3) Freezing. Since `m_t` is `G_t^-`-measurable and `A` is finite, `m_t = sum_a 1{X_t = a} F_t(a)` with
  each `F_t(a)` `G_t`-measurable (take `F_t(a) :=` the target the strategy would choose on the realised
  pre-type history if the type were `a`; this is a measurable function of the `G_t`-variables because the
  strategy is a measurable function of its inputs). Hence, for any bounded `g`,
  `E[g(X_t, m_t) | G_t] = sum_a pi_{B_t}(a) g(a, F_t(a))`. INDICATOR AUDIT: the step
  `E[1{X_t=a} F_t(a) | G_t] = F_t(a) pi(a)` pulls out `F_t(a)` because it is `G_t`-measurable; the indicator
  multiplies a quantity measurable before `X_t`, never after.
- (P4) `E[Y_t | G_t^-] = m_t` and `E[Y_t | G_t] = mbar_t := sum_a pi_{B_t}(a) F_t(a)`, the *effective mean*;
  `Y_t - mbar_t` lies in `[-mbar_t, 1 - mbar_t]`, an interval of length 1 with `G_t`-measurable endpoints.
- (P5) Effective cost. `E[phi_i(m_t) - phi_i(mu_i(X_t)) | G_t] = sum_a pi(a) phi_i(F_t(a)) - kappa_{i,b}
  >= psi_{i,b}(mbar_t) - kappa_{i,b}` when `I_t = i`, `B_t = b`, because `F_t(.)` is a feasible allocation
  with `pi`-mean `mbar_t` (feasibility of `F_t(a)` for every `a`: the strategy maps every history into the
  feasible set, including the counterfactual type `a`).

### 0.5 Facts about `psi` (proved in Part 1, Lemma 1)
`psi_{j,b}` is convex, nondecreasing, `Lambda`-Lipschitz on `[lobar, Mbar]`; `1 + kappa_{j,b} - psi_{j,b}(y)
in [0, 2]`; and it is attained by the WATER-FILL allocation `m_c(a) := clip(c, lo_j(a), M_j(a))` with `c` the
level giving `pi`-mean `y`, for every convex `phi_j` (common across types) and every `pi`.

### 0.6 Proposed profile `S*_N`
Stage 1 and Stage 3: deliver `M_j(X_t)`. Stage-2 winner `j` at label `b` with price `tau`: deliver the
water-fill allocation `m_c(X_t)` with `c` chosen so that the `pi_b`-mean equals
`y*_j(b, tau) := max{ lobar_j(b), min{ tau, Mbar_j(b) } }`
(for a strategic agent `lobar = 0`; for an honest agent `lobar = mubar_j(b)`). Requires the agent to know
`pi_b` (variant D-known); the knowledge-free variant D-learn is Part 4. With linear cost any allocation with
mean `y*` is equally good; water-fill is the choice that is also cost-optimal for every convex cost and
pointwise dominates the pointwise rule `min{tau, M_j(a)}` (Lemma 1(d)).

### 0.7 Statements (final forms; proofs in the Parts indicated)

Write `N_b := (V_b - K L_n)_+` (post-bidding visits to label `b`), `l_i(b)` the number of Stage-1 pulls of
`i` at `b`; under the conditioning on `B` both are deterministic. `W_i := {b : N_b >= 1, dbar_i(b) <= 2 s_n}`.

**Theorem N.** Assume (N), `K >= 2`, `n >= 2K`, a nonempty honest set, costs as in 0.1. Run label-keyed
CL-MESP.

(A) [Part 1] For every agent `i` and every `S' in D_{i,n}`,
`u_i(S', S*_{N,-i}) - u_i(S*_N) <= E[ sum_b l_i(b) ] + Lambda E[ sum_{b in W_i} (1 + b_n(N_b) + R_K(n)) ]
 + n^{-2} + 2 n^{-3}.`
Consequently the supremum over `D_{i,n}` is at most
`min{Q_B L_n, n} + Lambda [ Q_B + sqrt(l_n Q_B n / 2) + Q_B R_K(n) ] + n^{-2} + 2n^{-3}`, and labels with
`dbar_i(b) > 2 s_n` contribute ONLY their Stage-1 term (no gap-dependent term at all).

(B) [Part 2] `P(n; S*_N) >= E sum_t Mbar_(2)(B_t) - [ min{Q_B K L_n, n} + 2 s_n n + n^{-3} + n^{-2}/2 ]`.
Benchmark loss: if each label names a type (`Lab subset A`, error `e_b := 1 - pi_b(b)`), then
`E sum_t M_(2)(X_t) - E sum_t Mbar_(2)(B_t) <= omega' sum_t P(X_t != B_t) <= eps_bar n`, with
`omega' := max_{b, a != b} [M_(2)(a) - min_{j in top2(b)} M_j(a)]_+ <= min{1, omega + omega_2}` and
`eps_bar := n^{-1} sum_t P(X_t != B_t)`. The constant 1 in front of `eps_bar n` is EXACT (attained).

(C) [Part 3] For every profile `S` with each `S_j in D_{j,n}` and honest agents pointwise honest,
`P(n; S) >= E sum_t bbar(B_t) - [ min{Q_B K L_n, n} + 2 s_n n + E sum_{b: N_b>=1}(1 + b_n(N_b) + R_K(n)) + n^{-3} ]`,
and `E sum_t b(X_t) - E sum_t bbar(B_t) <= eps_bar n` (exact constant 1; equality `0` with one honest agent).

(Conviction) [Part 1, Lemma 4] Under `S*_N`, for each label the winner's monitor fires with probability at
most `(2n^3)^{-1} + (2n^4)^{-1}`; summed over labels the expected number of convicted winners is at most
`min{Q_B, n/(K L_n)} ((2n^3)^{-1} + (2n^4)^{-1})`.

(D) Rates as in Prop. X with `Q -> Q_B`.

**Proposition I** [Part 5]: stated and proved there, with a corrected corollary and a caveat on its reading.

---------------------------------------------------------------------------------------------------

## Part 1. Core argument: the equilibrium bound (A)

Written before reading any c2 file or any proof in the paper. The only external input is the EXP3 fallback
guarantee [F] below, stated as I need it; it is checked against the paper's lemma in Part 1b.

Throughout, condition on `B`: under (N) every visit count `V_b`, every Stage-1 round, `N_b`, `l_i(b)` and the
post-bidding visit rounds `u_{b,1} < ... < u_{b,N_b}` are deterministic, and every statement below is
uniform in `B`, so integrating over `B` at the end is free. All conditional expectations are given `B`
implicitly (it is in every field). `T_b` := round of the last Stage-1 visit to `b`; `F^b := F_{T_b}`.

### Lemma 1 (effective cost, water-fill)
Fix `j, b`, write `pi, lo, M, lobar, Mbar, psi, kappa` without indices.
(a) `psi` is attained, convex, nondecreasing and `Lambda`-Lipschitz on `[lobar, Mbar]`, and
`0 <= 1 + kappa - psi(y) <= 2`.
(b) For every `y in [lobar, Mbar]` there is `c in [0,1]` with `sum_a pi(a) clip(c, lo(a), M(a)) = y`, and the
water-fill `m_c` attains `psi(y)`, for every convex `phi` and every `pi`.
(c) For a STRATEGIC agent (`lo = 0`) and `y = y*(tau) = min{tau, Mbar}`, `m_c(a) >= min{tau, M(a)}` for all `a`
(choosing `c = 1` when `tau >= Mbar`). For an HONEST agent this dominance is FALSE in general (see below).

Proof. (a) The feasible set is a nonempty compact polytope (`y` is a convex combination of `lobar` and
`Mbar`, realised by the same combination of `lo` and `M`) and `phi` is continuous (Lipschitz), so the min is
attained. Convexity: convex combinations of optimal allocations for `y1, y2` are feasible for the combined
`y`. Monotone: from an optimum `m` at `y > y'`, `m' := lo + theta (m - lo)`, `theta = (y' - lobar)/(y - lobar)`,
is feasible with mean `y'` and `m' <= m`. Lipschitz: from an optimum `m` at `y < y''`,
`m'' := m + theta (M - m)`, `theta = (y'' - y)/(Mbar - y)`, has mean `y''` and
`sum pi [phi(m'') - phi(m)] <= Lambda sum pi (m'' - m) = Lambda (y'' - y)`. Range: for the optimum `m`,
`1 + kappa - psi(y) = 1 + sum pi [phi(mu(a)) - phi(m(a))]`, and each bracket is in `[-1, 1]` by (CN).
(b) `c -> sum pi clip(c, lo, M)` is continuous, equals `lobar` at 0 and `Mbar` at 1. Let `g` be the right
derivative of `phi` at `c` if `c < 1`, the left derivative if `c = 1`; `g in [0, Lambda]` and
`phi(x) >= phi(c) + g (x - c)` on `[0,1]`. Claim: for each `a` and every feasible `x in [lo(a), M(a)]`,
`phi(x) - phi(m_c(a)) >= g (x - m_c(a))`. If `m_c(a) = c`: supporting line. If `m_c(a) = M(a) < c`: then
`x <= M(a)` and the chord slope `(phi(M) - phi(x))/(M - x) <= phi'_-(M) <= phi'_-(c) <= g`. If
`m_c(a) = lo(a) > c`: `x >= lo(a)` and `(phi(x) - phi(lo))/(x - lo) >= phi'_+(lo) >= phi'_+(c) >= g` (when
`c = 1` this case is empty). Weighting by `pi` and using equal means gives
`sum pi phi(x) >= sum pi phi(m_c)`.
(c) If `tau < Mbar`: `sum pi min(c, M) = tau` forces `c >= tau` (the left side is `<= c`), so
`min(c, M(a)) >= min(tau, M(a))`. If `tau >= Mbar`, `c = 1` gives `m_c = M`. Honest counterexample:
`pi = (1/2, 1/2)`, `mu = (0.9, 0)`, `M = (1, 1)`, `tau = 0.5`: `y* = max(0.45, 0.5) = 0.5`, water-fill
`(0.9, 0.1)`, pointwise rule `max(mu, min(tau, M)) = (0.9, 0.5)`. []

So the scout's parenthetical "water-filling dominates the pointwise S* at every type" holds for strategic
agents only. Nothing in Theorem N depends on it (it only concerns the item-5 compliance METRIC).

### Lemma 2 (bids)
Fix `b` with `V_b >= K L_n`; agent `k`'s Stage-1 rounds `t_{k,1..L}` at `b` are deterministic. Put
`beta^max_k := L^{-1} sum_r 1{U_{t_{k,r}} <= M_k(X_{t_{k,r}})}`,
`beta^min_k := L^{-1} sum_r 1{U_{t_{k,r}} <= mu_k(X_{t_{k,r}})}`. These are functions of draws only.
(a) Given `B`, `beta^max_k` is a mean of `L` i.i.d. Bernoulli(`Mbar_k(b)`), `beta^min_k` of Bernoulli(`mubar_k(b)`).
(b) `G_b := cap_k {|beta^max_k - Mbar_k(b)| <= s_n}` has `P(G_b^c | B) <= K * 2 e^{-2 L s_n^2} = n^{-4}`;
`U_b := cap_k {beta^max_k <= Mbar_k(b) + s_n}` has `P(U_b^c | B) <= (2n^4)^{-1}`;
`H_b := {beta^min_{h*} >= bbar(b) - s_n}` (`h*` an honest maximiser of `mubar_h(b)`) has
`P(H_b^c | B) <= (2Kn^4)^{-1}`.
(c) Pathwise, under ANY profile, `beta^min_k 1{k honest} <= beta_k <= beta^max_k`; a non-deviator following
`S*_N` has `beta_k = beta^max_k`.
(d) On `U_b`, under any profile, the winner `W` satisfies `tau_b <= Mbar_W(b)`.
(e) With others at `S*_N` and `i` arbitrary: on `G_b`, if `i` wins then `dbar_i(b) <= 2 s_n` and
`tau_b <= min{Vbar_i(b), Mbar_i(b)}`.
(f) Monotone coupling: in the coupled executions (deviation `(S'_i, S*_{-i})` and baseline `S*_N`, same draws),
if `i` wins at `b` in the deviation it wins at `b` in the baseline, with the same price.
(g) Under `S*_N`, on `G_b`, `tau_b >= Mbar_(2)(b) - 2 s_n`.

Proof. (a) The pairs `(X_t, U_t)` at the `L` distinct deterministic rounds: by (N), applied draw by draw in
the enumeration order, their joint conditional law given `B` is the product of `pi_b x Unif`; hence the
indicators are i.i.d. with mean `sum_a pi_b(a) M_k(a)`. (b) Hoeffding, `2 e^{-2Ls^2} = 2/(2Kn^4)`; union over
`k in [K]` (a deterministic index set). (c) Stage-1 rewards are `1{U <= m}` with
`lo_k(X) <= m <= M_k(X)` at the same `(X, U)`. (d) `tau = (beta_(2) - s)_+ <= (beta_W - s)_+ <=
(beta^max_W - s)_+ <= Mbar_W` on `U_b`. (e) `Mbar_i + s >= beta^max_i >= beta_i >= max_{j != i} beta_j =
max_{j != i} beta^max_j >= Vbar_i - s`, so `dbar_i <= 2s`; `tau = (max_{j != i} beta_j - s)_+` is at most
`(Vbar_i + s - s)_+ = Vbar_i` and at most `(beta_i - s)_+ <= Mbar_i`. (f) Other agents' Stage-1 targets are
`M_j(X_t)` at the same rounds in both executions, so their bids coincide. The deviation bid `beta'_i <=
beta^max_i = beta_i^{base}`. If `i` wins in the deviation then every `j != i` has `beta_j <= beta'_i`, with
`Pi_b` ranking `i` above `j` when equal. In the baseline, `beta_j <= beta'_i <= beta^max_i`; equality
`beta_j = beta^max_i` forces `beta_j = beta'_i`, and the same `Pi_b` breaks the tie for `i`. The price in both
is `(max_{j != i} beta_j - s)_+` (second order statistic with multiplicity, `i` the winner). (g) The second
order statistic is 1-Lipschitz in sup norm, so `beta_(2) >= Mbar_(2) - s` and `tau >= beta_(2) - s`. []

### Lemma 3 (primary accounting, any winner behaviour)
Fix `b` with `N := N_b >= 1`, winner `W` and price `tau` (both `F^b`-measurable). Primary pulls are at
`u_1 < ... < u_N` until the switch; `rho` := number of primary pulls (`rho = N` if no switch). Let
`mbar_k` := `W`'s effective mean at `u_k` (P4), `D_k := 1{k <= rho} (Y_{u_k} - mbar_k)`, `M_r := sum_{k<=r} D_k`.
Then (a) `{k <= rho}` is `G_{u_k}`-measurable, `E[D_k | G_{u_k}] = 0`, `D_k` has a `G_{u_k}`-measurable range
interval of length at most 1, so `E[M_N | F^b] = 0`; (b) pathwise
`sum_{k <= rho} mbar_k >= rho tau - 1 - b_n(rho) - M_N`.

Proof. (a) `{k <= rho}` = no switch at primary pulls `1..k-1`, a function of `Y_{u_1..u_{k-1}}`, which are
`F_{u_{k-1}} subset G_{u_k}`-measurable. INDICATOR AUDIT: the indicator is measurable BEFORE the round's
type and seed, so `E[1{k<=rho}(Y - mbar) | G_{u_k}] = 1{k<=rho} E[Y - mbar | G_{u_k}] = 0` by (P4).
Tower over `F^b subset G_{u_1}`. (b) `M_N = Z_rho - sum_{k<=rho} mbar_k`. No switch occurred at pull
`rho - 1` (vacuous if `rho = 1`, where `Z_0 = 0`), so `Z_rho >= Z_{rho-1} >= (rho-1) tau - b_n(rho-1) >=
rho tau - 1 - b_n(rho)`. []

### Lemma 4 (no false switch)
In the setting of Lemma 3, if `mbar_k >= tau` on `{k <= rho}` for every `k`, then
`P(a switch occurs at b | F^b) <= N e^{-l_n} = N/(2n^4) <= (2n^3)^{-1}`.

Proof. A switch at pull `r` means `r <= rho` and `Z_r < r tau - b_n(r)`; then
`M_r = Z_r - sum_{k<=r} mbar_k <= Z_r - r tau < -b_n(r)`. `M_r` is a sum of `r` martingale differences with
predictable ranges of length `<= 1`, so Azuma-Hoeffding gives `P(M_r < -b_n(r) | F^b) <= exp(-2 b_n(r)^2 / r)
= e^{-l_n}`. Union over `r in {1..N}`: DETERMINISTIC index set given `B` (union-bound audit). []

### [F] Fallback input (to be verified against the paper's Lemma ctx-fallback in Part 1b)
Let a switch occur at `b` at pull `rho < N`; the fallback runs at the `H := N - rho` visits
`u_{rho+1..N}` (`H` is measurable at the switch round `sigma := u_rho`). Suppose some agent `j*` and a
constant `v` satisfy: at every fallback round `t`, on `{I_t = j*}`, `E[Y_t | G_t] >= v`. Then
`E[ sum_{fallback} Y_t | F_sigma ] >= v H - R_K(n)`.

### Proof of (A)
Couple the two executions on one space with the same draws `(B, xi, Pi, zeta, X, U)`; (N) is a property of
the draws, so it holds for both. Decompose agent `i`'s realised utility into, for each `b`, its Stage-1 part
`U^1(b)` and its post-bidding part `U^2(b)`.

Stage 1. The Stage-1 schedule is the same in both executions. At each of `i`'s Stage-1 pulls, the
difference of per-pull utilities is `phi_i(M_i(X_t)) - phi_i(m'_t) <= phi_i(1) - phi_i(0) <= 1`. Hence
`E sum_b [U^1_dev(b) - U^1_base(b)] <= E sum_b l_i(b)`.

Post-bidding. Fix `b` with `N := N_b >= 1`. Both executions' histories up to `T_b` are functions of draws up
to `T_b`, so `F^b` carries both. Claim:
`E[U^2_dev(b) - U^2_base(b) | F^b] <= 1_{G_b cap W'_b} Lambda (1 + b_n(N) + R_K(n)) + N^2/n^4 + 2N 1_{G_b^c}`,
with `W'_b` := {`i` wins at `b` in the deviation}.

Case 1: `G_b cap W'_b`. By Lemma 2(e,f) `b in W_i`, `i` wins in the baseline too, with the same price
`tau <= w := min{Vbar_i, Mbar_i}`. Put `y* := max{lobar_i, tau}`, `c_0 := 1 + kappa - psi(y*) in [0,2]`
(indices `i, b` dropped).

- Baseline. `y*_i(b, tau) = max{lobar, min{tau, Mbar}} = y*` since `tau <= Mbar`. By Lemma 1(b) and (P3) the
  winner's conditional per-pull utility given `G_{u_k}` is exactly `c_0` and its effective mean is
  `y* >= tau`. Fallback utility is `>= 0`. By Lemma 3(a)-style optional stopping (the indicator
  `{k <= rho_0}` is `G_{u_k}`-measurable), `E[U^2_base | F^b] >= c_0 E[rho_0 | F^b] >= c_0 N - 2N P(switch | F^b)
  >= c_0 N - N^2/n^4` by Lemma 4.
- Deviation, primary. By (P5), `E[u_k | G_{u_k}] <= 1 + kappa - psi(mbar_k)` on `{k <= rho}`. Let `g := 0` if
  `y* = lobar`, else `g := psi'_-(tau) in [0, Lambda]` (left derivative at `tau in (lobar, Mbar]`, a
  subgradient). Then `psi(mbar) >= psi(y*) + g (mbar - y*)` on `[lobar, Mbar]` (for `g = 0` by monotonicity).
  If `g > 0`, `y* = tau` and Lemma 3(b) gives `sum_{k<=rho} (mbar_k - tau) >= -(1 + b_n(rho) + M_N)`. As `g` is
  `F^b`-measurable and `E[M_N | F^b] = 0`,
  `E[sum_{k<=rho} psi(mbar_k) | F^b] >= psi(y*) E[rho | F^b] - Lambda (1 + b_n(N))`, so the primary utility is at
  most `c_0 E[rho | F^b] + Lambda (1 + b_n(N))`.
- Deviation, fallback (only on a switch). `j* in argmax_{j != i} Mbar_j` follows `S*_N` (delivers `M_{j*}(X_t)`),
  so `E[Y_t | G_t] = Vbar_i` on `{I_t = j*}`; by [F], `E[sum_fb Y_t | F_sigma] >= Vbar_i H - R_K(n)`. Every other
  `j != i` has `E[Y_t | G_t] = Mbar_j <= Vbar_i` on `{I_t = j}` (indicator `G_t`-measurable), so
  `E[sum_fb 1{I_t != i} Y_t | F_sigma] <= Vbar_i E[H - Q_i | F_sigma]`, `Q_i` := number of fallback pulls of `i`.
  Subtracting, `E[sum_fb 1{I_t = i} mbar_t | F_sigma] >= Vbar_i E[Q_i | F_sigma] - R_K(n) >= w E[Q_i | F_sigma] -
  R_K(n)`. Let `y** := max{lobar, w} >= y*` and `g' := 0` if `y** = lobar`, else `psi'_-(w) in [0, Lambda]`. Then
  `E[sum_fb 1{I_t=i} psi(mbar_t) | F_sigma] >= psi(y**) E[Q_i | F_sigma] - Lambda R_K(n)`, so the fallback utility
  is at most `(1 + kappa - psi(y**)) E[Q_i | F_sigma] + Lambda R_K(n) <= c_0 H + Lambda R_K(n)` (monotonicity of
  `psi`, `0 <= 1 + kappa - psi(y**)`, `Q_i <= H`).
- Adding, `E[U^2_dev | F^b] <= c_0 E[rho + H | F^b] + Lambda(1 + b_n(N) + R_K(n)) = c_0 N + Lambda(...)`.

Case 2: `G_b minus W'_b`. The winner `j != i` follows `S*_N`; by Lemma 2(d) (`G_b subset U_b`) `tau <= Mbar_j`, so
its effective mean `y*_j >= min{tau, Mbar_j} = tau`, and Lemma 4 bounds the switch probability by
`N/(2n^4)`. Agent `i` is selected at `b` after bidding only in a fallback, at utility `<= 2` per pull:
`E[U^2_dev | F^b] <= N^2/n^4`, while `U^2_base >= 0`.

Case 3: `G_b^c`: `U^2_dev - U^2_base <= 2N`.

Summation. `E sum_b [...] <= Lambda E sum_{b in W_i} (1 + b_n(N_b) + R_K(n)) + E sum_b (N_b^2 + 2 N_b)/n^4`,
using `P(G_b^c | B) <= n^{-4}` (`G_b` is `F^b`-measurable). `sum_b N_b^2 <= n^2`, `sum_b N_b <= n`. This proves
(A). For the consequence: `sum_b l_i(b) <= min{Q_B L_n, n}`, `|W_i| <= Q_B`, and Cauchy-Schwarz
`sum_{b in W_i} b_n(N_b) <= sqrt(l_n |W_i| n / 2)`. []

Conviction statement. Under `S*_N`, on `U_b` the winner's effective mean is `>= tau` (Lemma 2(d)), so by
Lemma 4 the monitor fires with probability `<= (2n^3)^{-1}`; `P(U_b^c) <= (2n^4)^{-1}`. Only labels with
`V_b >= K L_n` have a winner, at most `min{Q_B, n/(K L_n)}` of them (deterministic given `B`).

### Remarks on what Part 1 did and did not use
- Label locality is automatic: the mechanism and every `S*_N` agent act at `b` on `b`-local messages and the
  current `X_t` only, so the deviator is the only cross-label channel, and every bound above holds for an
  arbitrary `G`-adapted deviator behaviour at `b`.
- The mixture enters ONLY through (P3)-(P5): conditionally on the pre-type field the reward is
  Bernoulli(`mbar`) and the expected cost is at least `psi(mbar) - kappa`. This is where (N) is used
  essentially: the posterior at every round, given everything before it, must be `pi_{B_t}`; otherwise the
  effective mean is not a function of the allocation alone and the price set in Stage 1 refers to a
  different mixture.
- The non-top labels with `dbar_i(b) > 2 s_n` contribute nothing beyond Stage 1, because a non-top agent
  cannot win on `G_b` at all (Lemma 2(e)); and labels with `0 < dbar_i(b) <= 2 s_n` get the same bound as top
  labels because the fallback comparison uses `w = min{Vbar_i, Mbar_i}`. This is SHARPER than the non-top term
  `D_i(z)` of Prop. X (see Part 1b for the comparison).

---------------------------------------------------------------------------------------------------

## Part 1b. Check of [F] and comparison with the paper's proof (read only AFTER Part 1 was written)

Read after Part 1: `sections/app_contextual_private.tex` lines 224-695 (Lemmas ctx-locality, ctx-monitor,
ctx-fallback, ctx-bid, proofs of Prop. X (i)-(iii), Prop. ctx-finite-tight, two remarks), and the statement
(Sec. 3) and Sec. 6.6 of c2 PROVER1 (to confirm that "c2 Theorem 1" has the same form as Prop. X).

[F] is Lemma ctx-fallback verbatim, with the arrival path `A` replaced by the label path `B`. Its
hypothesis is "at every Stage-3 visit at which `j` is selected, `j`'s conditional expected reward given
the past is at least `v`", where the past is the global field before the selection plus the selection
(`r_{j,t} = E[Y_t | J_{t-1}, I_t = j]`). In the noisy model this is exactly `E[Y_t | G_t]` on `{I_t = j}`:
the target does not read `zeta_t` except through `I_t`, and `X_t` is drawn after `zeta_t` and is fresh given
`G_t` by (N), so `r_{j*,t} = sum_a pi_b(a) M_{j*}(a) = Mbar_{j*}(b)` for a non-deviator in Stage 3, and
`r_{h,t} >= mubar_h(b)` for an honest `h` (every counterfactual target `F_t(a) >= mu_h(a)`). I re-derived the
lemma's arithmetic: `sum_i q_i Yhat_i^2 <= q_I/p_I^2`, whose conditional mean is `<= sum_i q_i/p_i <=
K/(1-gamma)`; `(1-gamma) sum_i q_i r_i <= sum_i p_i r_i` because `r_i >= 0`; hence
`E sum Y >= vH - 2 gamma H - K log K / gamma <= R_K(n)` loss for both branches of `gamma_n`. Its proof never
uses a counterfactual reward of an unselected arm, so selected-reactive behaviour of the deviator and the
noisy type are harmless. [F] VERIFIED.

Comparison with the paper's proof of Prop. X(i) (same structure as c2 PROVER1 Sec. 6):
1. Paper's good event `G(z)` controls only the OTHER agents' bids. My `G_b` also controls the deviator's
   capacity bid `beta^max_i` (one more Hoeffding term, `P(G_b^c) <= K/(Kn^4) = n^{-4}`, the same total as the
   paper's). With it, a non-top agent with `dbar_i > 2 s_n` cannot win on `G_b` (Lemma 2(e)), so the paper's
   whole non-top branch (tenure bound `4(1+sqrt(2 l))^2/delta^2`, fallback `2R_K/delta`, and the `2N_z` charge
   when `4 s_n > delta`) is unnecessary; and when `0 < dbar_i <= 2 s_n` the top-branch argument goes through
   with `w = min{Vbar_i, Mbar_i}` in the fallback. **Consequence for the paper itself** (take `pi_b` a point
   mass, i.e. no noise): Prop. X(i) holds with the non-top sum replaced by
   `Lambda sum_{z : 0 < delta_i(z) <= 2 s_n} E[1 + b_n(N_z) + R_K(n)]`, which makes the bound UNIFORM over
   instances (no `delta_i(z)` anywhere, no instance threshold `4 s_n <= min delta`), contrary to the paper's
   remark that (i) "is not uniform over instance sequences whose positive capacity gaps vanish". This needs
   independent confirmation before anyone edits the paper; I did not touch any paper file.
2. Paper's monitor slack is `1 + 2b_n` (pathwise, on a two-sided good event); mine is `1 + b_n` (in
   expectation, via `E[M_N | F^b] = 0` with `g` `F^b`-measurable). Both valid; mine is smaller.
3. Paper's revenue bound (ii) carries `Q R_K(n)` (it accounts for the fallback); mine replaces it by
   `n^{-2}/2` by charging the whole post-bid block on the switch event, whose probability is
   `<= N_b/(2n^4)`. Both valid.
4. Paper's honest winner with `tau <= mu` is a separate case; in my write-up it is the case `y* = lobar`,
   `g = 0`, handled by the same lines.
Nothing in the paper's proof contradicts a step of Part 1. The paper's Lemma ctx-bid (d) is my Lemma 2(f)
with the same tie argument.

---------------------------------------------------------------------------------------------------

## Part 2. Revenue (B) and the benchmark loss

### 2.1 Revenue at `S*_N`
All agents play `S*_N`. Revenue is additive over labels. Stage-1 rounds: revenue `>= 0`, benchmark
`Mbar_(2) <= 1`, total charge `sum_b min{V_b, K L_n} <= min{Q_B K L_n, n}`. Fix `b` with `N_b >= 1`. On `G_b`:
`tau >= Mbar_(2)(b) - 2 s_n` (Lemma 2(g)), `tau <= Mbar_W` (Lemma 2(d)), so the winner's effective mean is
`y*_W >= tau` and Lemma 4 gives `P(switch | F^b) <= N_b/(2n^4)`. Charging the whole post-bid block (at most
`N_b`) on a switch and on `G_b^c`:
`E[sum_post Y | F^b] >= E[sum_{k<=rho} y*_W] >= N_b (Mbar_(2) - 2s_n) - N_b^2/(2n^4)` on `G_b` (fallback
revenue `>= 0`; optional stopping as in Part 1 since `y*_W` is `F^b`-measurable and the indicator
`{k <= rho}` is `G_{u_k}`-measurable), and `>= N_b Mbar_(2) - N_b` off `G_b`. Summing,

`P(n; S*_N) >= E sum_t Mbar_(2)(B_t) - [ min{Q_B K L_n, n} + 2 s_n n + n^{-3} + n^{-2}/2 ]`. []

### 2.2 Benchmark loss: constant 1, attained (scout's 2 eps is loose by a factor 2)
**Lemma 5.** For every label `b` and every type `a0 in A`,
`sum_a pi_b(a) M_(2)(a) - Mbar_(2)(b) <= sum_{a != a0} pi_b(a) [M_(2)(a) - m_2^{a0}(a)]_+ <= 1 - pi_b(a0)`,
where `m_2^{a0}(a) := min{M_{j1}(a), M_{j2}(a)}` for two agents `j1 != j2` attaining the top two capabilities
at `a0`.

Proof. `Mbar_(2)(b) >= min{Mbar_{j1}(b), Mbar_{j2}(b)} >= sum_a pi_b(a) m_2^{a0}(a)` (two agents each with
mixture at least the right side; min of sums >= sum of mins), and `m_2^{a0}(a0) = M_(2)(a0)`. The last
inequality uses `0 <= M <= 1`. []

**Corollary 6.** Under (N), `E[M_(2)(X_t) | B] = sum_a pi_{B_t}(a) M_(2)(a)` (P1). Hence, for ANY map
`iota: Lab -> A` (e.g. the type the label names),
`E sum_t M_(2)(X_t) - E sum_t Mbar_(2)(B_t) <= sum_t P(X_t != iota(B_t))`, and the best choice gives the
Bayes error `sum_t (1 - E max_a pi_{B_t}(a))`. With `Lab = A` and `iota = id` this is `eps_bar n`. The refined
form with `omega' := max_{b, a != iota(b)} [M_(2)(a) - m_2^{iota(b)}(a)]_+` is `<= omega' eps_bar n`, and
`omega' <= min{1, omega + omega_2}` (because `M_(2)(a) <= M_(2)(iota b) + omega_2` and
`M_j(a) >= M_j(iota b) - omega >= M_(2)(iota b) - omega` for `j` in the top two at `iota(b)`), so this dominates
the scout's `eps(omega + omega_2)` everywhere.

Tightness. The scout's own example (types `a, c`, `M(a) = (1,1,0)`, `M(c) = (0,1,1)`, symmetric error `e`)
has per-label loss exactly `e`, so total loss `eps n`: the example ATTAINS the constant 1 and the scout's
"tight up to the factor 2" is really "the 2 is wrong, 1 is exact". Numerically confirmed (Part 6, E0).

---------------------------------------------------------------------------------------------------

## Part 3. Honest benchmark (C)

Let `S` be any profile, `S_j in D_{j,n}`, honest agents pointwise honest (the whole of `[K]` may deviate).
Fix `b` with `N_b >= 1` and `h*` an honest maximiser of `mubar_h(b)`, so `bbar(b) = mubar_{h*}(b)`.

- Bid floor. `beta_{h*} >= beta^min_{h*}` pathwise (Lemma 2(c)); on `H_b`, `beta_{h*} >= bbar - s_n`,
  `P(H_b^c | B) <= (2Kn^4)^{-1}` (Lemma 2(b); `h*` is a deterministic index).
- Case `W != h*` on `H_b`: `beta_(2) >= beta_{h*}` (the multiset minus one copy of the max contains
  `beta_{h*}`), so `tau >= bbar - 2 s_n`. Lemma 3 (any winner behaviour) and `E[M_N | F^b] = 0`:
  `E[sum_{k<=rho} mbar_k | F^b] >= tau E[rho | F^b] - 1 - b_n(N_b)`. Fallback, by [F] with comparator `h*`
  (`r_{h*,t} >= bbar` by pointwise honesty): `E[sum_fb Y | F_sigma] >= bbar H - R_K(n)`. Adding,
  `E[sum_post Y | F^b] >= N_b bbar - 2 s_n N_b - 1 - b_n(N_b) - R_K(n)`.
- Case `W = h*`: every effective mean at a primary pull is `>= bbar`; with the fallback,
  `E[sum_post Y | F^b] >= N_b bbar - R_K(n)`.
- Off `H_b`: charge `N_b`.

Summing (Stage-1 charge as in 2.1):
`P(n; S) >= E sum_t bbar(B_t) - [ min{Q_B K L_n, n} + 2 s_n n + E sum_{b: N_b >= 1} (1 + b_n(N_b) + R_K(n)) + n^{-3} ]`,
and `sum_b b_n(N_b) <= sqrt(l_n Q_B n / 2)`. []

Benchmark loss. Same argument as Lemma 5 with `h(a0)` an honest maximiser at `a0`:
`bbar(b) >= mubar_{h(a0)}(b) >= pi_b(a0) b(a0)`, so the per-label loss is `<= sum_{a != a0} pi_b(a) b(a) <=
1 - pi_b(a0)` and the total is `<= eps_bar n` (Bayes error in general). With ONE honest agent,
`bbar(b) = sum_a pi_b(a) mu_h(a) = E[mu_h(X_t) | B_t = b]`, so the loss is exactly 0 (tower property under
(N)). Tightness of the constant 1: two honest agents with `mu_1 = 1{a}`, `mu_2 = 1{c}`, symmetric error `e`:
`bbar = 1 - e` at both labels, `b(X) = 1`: loss `eps n` exactly. So the scout's "at most 2 eps" is again
loose by a factor 2.

---------------------------------------------------------------------------------------------------

## Part 4. D-learn: nobody knows `pi`

Profile `S*_L`. As `S*_N` except the Stage-2 winner `j` at `b`: let `pihat_{j,b}` be the empirical law of the
TRUE TYPES `j` observed at its own `L_n` Stage-1 pulls at `b` (information it has; inside `D_{j,n}`). Put
`Mhat := sum_a pihat(a) M_j(a)`, `lohat := sum_a pihat(a) lo_j(a)`, target
`that := max{ lohat, min{ tau + gam_n, Mhat } }`, and deliver `clip(chat, lo_j(X_t), M_j(X_t))` with `chat` the
LARGEST level whose `pihat`-mean is `that` (so `chat = 1` when `that = Mhat`), where

`gam_n := sqrt( (|A| log 2 + log(K n^4)) / (2 L_n) )`.

(This is the scout's `gamma` with `4 log n` replaced by `log(K n^4)`, so that a union over the `K` possible
winners costs `n^{-4}`.)

**Lemma 7.** `E^TV_b := cap_j {TV(pihat_{j,b}, pi_b) <= gam_n}` has `P((E^TV_b)^c | B) <= n^{-4}`. On
`E^TV_b cap U_b`, the winner's true effective mean `ybar := sum_a pi_b(a) clip(chat, lo(a), M(a))` satisfies
`y* <= ybar <= y* + 2 gam_n` with `y* = max{lobar, min{tau, Mbar}} = max{lobar, tau}`.

Proof. Given `B`, `j`'s Stage-1 types at `b` are `L` i.i.d. draws from `pi_b` (N); `TV = max_S (pihat(S) - pi(S))`
over `2^{|A|}` sets, Hoeffding each: `2^{|A|} e^{-2 L gam^2} = 1/(K n^4)`; union over `j`. For `f: A -> [0,1]`,
`|sum (pihat - pi) f| <= TV`. Three cases for `that`. (i) `that = tau + gam <= Mhat`: `ybar >= that - gam = tau`,
`ybar <= tau + 2 gam`. (ii) `that = Mhat < tau + gam`: `chat = 1`, `ybar = Mbar >= tau` on `U_b`, and
`Mbar <= Mhat + gam < tau + 2 gam`. (iii) `that = lohat > min{tau + gam, Mhat}`: if `lohat = Mhat` then `chat = 1`
and case (ii) applies; else `lohat > tau + gam`, so `ybar >= lohat - gam > tau` and `ybar <= lohat + gam <=
lobar + 2 gam`. Always `ybar >= lobar`. []

Because a clip allocation is cost-optimal under `pi` for the mean it produces under `pi` (Lemma 1(b) holds
for every `pi`), the winner's per-pull expected utility is `1 + kappa - psi(ybar) >= c_0 - 2 Lambda gam_n`.

**Theorem N-learn.** Under the hypotheses of Theorem N, with `S*_L` in place of `S*_N`:
(A-L) `u_i(S', S*_{L,-i}) - u_i(S*_L) <= [bound (A)] + 2 Lambda gam_n E sum_{b in W_i} N_b + 2n^{-3}
<= [bound (A)] + 2 Lambda gam_n n + 2 n^{-3}`;
(B-L) (B) holds with an extra `n^{-3}`; (C) is unchanged (it is uniform over profiles);
conviction of the winner per label `<= (2n^3)^{-1} + (2n^4)^{-1} + n^{-4}`.

Proof. The deviation side of Part 1 does not involve the baseline profile. Baseline side of Case 1: on
`G_b cap E^TV_b` the baseline winner's effective mean is `>= tau` (Lemma 7), so Lemma 4 applies, and its
per-pull utility is `>= c_0 - 2 Lambda gam_n`; off `E^TV_b` charge `2N_b`. Case 2: the non-deviating winner
meets the price on `E^TV_b cap U_b`. Revenue: the winner's effective mean is `>= tau` on the same event. []

Correction to the scout: the extra term is `2 Lambda gam n` (`2 gam n` for linear cost), not `n gam`: the
target has to be raised by `gam` to survive the estimation error from below, and the same error can add
another `gam` from above. It is `O(sqrt((|A| + log n)/L_n) n) = O(sqrt(|A|) n^{2/3})`, the order of `2 s_n n`
up to the `sqrt(|A| / log n)` factor, as the scout says. Note `|A|` (true types) enters here, not only `Q_B`.

---------------------------------------------------------------------------------------------------

## Part 5. Proposition I (arbitrary true-type order)

Model. The true-type path `x_1..x_n` is deterministic and arbitrary (exogenous); labels are drawn
`B_t ~ C(x_t, .)` conditionally on everything before (so, for a fixed path, independent across rounds). A
LABEL-ONLY mechanism selects `I_t` and sends messages as measurable functions of `(B_1..B_t)`, past
`(I_s, Y_s)` and its own coins (fresh given the past). The selected agent observes `x_t`, its own history
and messages. Linear costs, `mu = 0` for the agent `W` below.

Instance (`K = 3`, types `{a, c, d}`, labels `{alpha, gamma}`, correct label `a -> alpha`, `c, d -> gamma`):
`C(a, alpha) = 1`, `C(c, alpha) = C(d, alpha) = eps` (per-type errors `0, eps, eps`, all `<= eps`),
`M_W(a) = M_W(c) = 1`, `M_W(d) = 0`, and agents 2, 3 with `M_j(c) = M_j(d)`, `mu_j(c) = mu_j(d)` (for the
PL-MESP reading: `M_2(a) = M_3(a) = p`, `M_2(c) = M_3(c) = 1`). Fix `p in (0,1)` (the scout: `p = 1/2`) and
`theta in (0,1)` (the scout: `1/2`), `theta n` an integer.
Paths: `P1`: `x_t = a` for `t <= theta n`, `x_t = d` after. `P2`: `a`, then `c`.
Other agents: any strategies that read the type only through `(M_j(x), mu_j(x))` (e.g. `S*`-type rules),
hence cannot tell `c` from `d`.
`W`'s strategies: cooperative `sigma^C` = deliver `min{p, M_W(x_t)}` at label `alpha`, `M_W(x_t)` (full
capacity, as a non-winner) at label `gamma`; shading `sigma^S` = deliver `p` at type `a` and `0` at type `c`.

**Proposition I (as proved here).** For every `eps in (0,1]`, every `p, theta in (0,1)` and every label-only
mechanism:
(a) Coupling. On one space with the same label draws, mechanism coins and seeds, `(P1, sigma^C)` and
`(P2, sigma^S)` produce the SAME labels, selections, messages, targets of every agent, and rewards,
pathwise. In particular their joint laws coincide.
(b) Dichotomy. Let `E_2 := E #{t > theta n : B_t = alpha} = eps (1 - theta) n` and define the withheld
fraction `alpha_w` by `E #{t > theta n : B_t = alpha, I_t = W} = (1 - alpha_w) E_2` under `(P1, sigma^C)`.
Then `u_W(P2; sigma^S) - u_W(P2; sigma^C) >= (p - alpha_w) eps (1 - theta) n`. With `p = theta = 1/2`:
`>= (1/2 - alpha_w) eps n / 2`, hence `>= eps n / 8` when `alpha_w <= 1/4`, exactly and with no `O(sqrt n)`.

Proof. (a) Induction on `t`: the pasts coincide; `C(d, .) = C(c, .)` and `C(a, .)` are shared, so the same
label draw gives the same `B_t`; the mechanism's selection and messages are the same function of the same
inputs; `W`'s target is `p` at `a` in both, and `0` at every second-half round in both
(`min{p, M_W(d)} = M_W(d) = 0` under `sigma^C` on `P1`, `0` at `c` under `sigma^S` on `P2`); the other agents'
targets are the same function of the same inputs; the same seed gives the same reward.
(b) On `P2`, `sigma^S` and `sigma^C` coincide in the first `theta n` rounds, so (same coupling) the
first-block histories and utilities coincide pathwise. Second block, `sigma^S`: each selection of `W` is
worth `1 - 0 = 1`, and by (a) its expected number of label-`alpha` selections is `(1 - alpha_w) E_2`; label-`gamma`
selections are worth `>= 0`. Second block, `sigma^C`: a label-`alpha` selection is worth `1 - p` and there are at
most `#{t > theta n : B_t = alpha}` of them, of mean `E_2`; a label-`gamma` selection is worth `1 - 1 = 0`. So the
difference is `>= (1 - alpha_w) E_2 - (1 - p) E_2`. []

What needed changing in the scout's statement.
1. The scout compares shading with "deliver 1/2 throughout". As stated that comparison is NOT valid for an
   arbitrary label-only mechanism: second-block label-`gamma` rounds are type `c`, where `W` is capable, and a
   mechanism may route label-`gamma` rounds to `W` exactly when `W` has been delivering `1/2` (e.g. "select `W`
   at `gamma` iff its last `alpha`-reward was 1"), giving the "1/2 throughout" comparator label-`gamma`
   selections worth `1/2` each on about half of the `(1 - eps)(1 - theta) n` label-`gamma` rounds, i.e. extra utility
   of order `(1 - eps)(1 - theta) n / 4` and making the claimed gain negative for small `eps`. The fix used
   above: the cooperative comparator delivers full capacity at label `gamma` (utility 0 per selection there),
   which is also what `S*` prescribes for a non-winner. The shading strategy must also deliver 0 at label-`gamma`
   `c`-rounds, since that is what the cooperative agent does at `d` on `P1` (the scout leaves this unspecified).
2. The `O(sqrt n)` is unnecessary when `alpha_w` is defined through expected counts; and `eps n / 8` is one point
   of `(p - alpha_w) eps (1 - theta) n`, which approaches `(1 - alpha_w) eps n` as `p -> 1`, `theta -> 0`.
3. READING. The dichotomy is real but weaker than "order robustness is lost, necessarily". On `P1` the
   withheld rounds are rounds where the cooperative `W` delivers 0 while agents 2, 3 deliver 1: withholding them is
   efficient for the platform and costs `W` only rounds on which it was being paid for nothing. So Prop. I shows
   that no label-only mechanism can protect POINTWISE compliance (the compliance notion of c2's `S*`) under an
   arbitrary type order; it does not show that every label-only mechanism loses an equilibrium-plus-revenue
   guarantee under arbitrary order. For PL-MESP specifically the loss is real and larger: its conviction is
   permanent, so with a path `a, d, a` (resp. `a, c, a`) the cooperative `W` on `P1` loses the whole final `a`-block
   (Part 6, E4), where it is fully compliant even pointwise. A mechanism with re-admission after a switch is
   not excluded by Prop. I, and I did not attempt to prove or refute its existence.

---------------------------------------------------------------------------------------------------

## Part 6. Numerical sanity checks (folder `prover2/`)

Python: the existing venv `.../0be94e74-.../scratchpad/venv/bin/python` (numpy 2.5.3, scipy 1.18.1). All runs
single-core, under 2 minutes each. Outputs saved next to the scripts (`*.out`).

- `e0_e1_static.py` -> `e0_e1_static.out`.
  E0: 20000 random instances (2-4 types, 2-5 agents, random confusion). Max of loss/eps = 0.743, loss/Bayes
  error = 0.848, loss minus `omega' eps` = 2e-16 (bound 0), `omega' > omega + omega_2` in 0 cases, honest
  loss/eps = 0.752. Tightness: the scout's example and the two-honest example give loss exactly `eps` at
  `eps = 0.05, 0.1, 0.2, 0.4`. So the constant is 1, not 2.
  E1: water-fill equals the SLSQP optimum of `psi` to 1e-11 over 400 random convex-cost instances; the honest
  counterexample to "water-fill dominates the pointwise rule" is confirmed (`(0.9, 0.1)` vs `(0.9, 0.5)`).
- `label_mesp_sim.py` (one label's local CL-MESP, true types hidden from the platform, EXP3 fallback, common
  random numbers across strategies so gains are coupled as in the proof) and `e2_e3_equilibrium.py`
  -> `e2_e3_n30000.out`, `e2_e3_n100000.out`. Posterior `pi = (0.8, 0.1, 0.1)` (label error 0.2), `K = 3`,
  agent 2 honest. Bound printed is `l_i + 1 + b_n(N) + R_K(n)` (`Lambda = 1`).
  At `n = 1e5` (R = 100): `S*_N` is never convicted (0/100); the pointwise rule (item-5 behaviour) is convicted
  in 100/100 (40/100 at `n = 3e4`), reproducing the item-5 failure and its cure. Top-agent deviations: best
  gain is the monitor RIDER with a margin of 15 (deliver 0 whenever the next test is guaranteed to pass,
  capacity otherwise): gain 1405 +- 16 against `b_n(N) = 1409` and total bound 8141. So the `b_n(N)` term with
  constant 1 is essentially ATTAINED (the paper's `2 b_n` is loose by a factor 2). Stage-1 underbid gains
  300 = `L (Mbar_0 - mid)` exactly. Label-mean shading by 0.005 gains 425 (undetected, `delta N`), by
  0.02/0.05 is convicted and loses. All gains `<=` bound. D-learn baseline loses 5967 against `S*_N`, within
  `2 gam_n N = 11900`, i.e. about `gam_n N`.
  E3 (non-top agent 1 with `dbar_1 = 0.005 < 2 s_n = 0.138`): it wins 27% of runs; best deviation gain
  373 +- 121 (`~ 0.27 b_n(N)`), far below the bound and far below the paper's charge `2 N_z` for this regime;
  consistent with the sharpening of Part 1b.
- `e4_prop_I.py` -> `e4_prop_I.out` (label-alpha instance; `p = 1/2`). (a) `(P1, coop)` and `(P2, shade)` give
  bit-identical utilities and revenues in every replication. (b) CL-MESP convicts the cooperative `W` on `P1`
  in 100% of runs. With a final `a`-block (paths `a, d, a` / `a, c, a`), the cooperative `W` on `P1` gets 8283
  against 19774 on `P2`: a linear penalty on a fully compliant winner, and shading on `P2` is deterred (gain
  -11491). Without a final block, shading on `P2` gains 323 +- 39 (conviction takes time). With the monitor
  switched off, shading gains 793 (eps 0.1) and 1663 (eps 0.2), about `tau * m_2`: the other horn.
- `e5_bursty.py` -> `e5_bursty.out`: same label frequencies but types in deterministic blocks
  `(8B, B, B)`: `S*_N` is never convicted for `B <= 500` and always convicted for `B = 2000` at `n = 1e5`:
  (N) is not a proof artefact; order matters once blocks exceed the monitor's `sqrt(n log n)` scale.

---------------------------------------------------------------------------------------------------

## Part 7. Summary, audit list, least secure step

### What is proved (all under (N), label-keyed CL-MESP unchanged, general convex `Lambda`-Lipschitz costs)
- (A) PROVED, with a bound at least as strong as "c2 Theorem 1(i) with `Q -> Q_B`, `delta -> dbar`": the
  non-top gap term disappears (labels with `dbar_i > 2 s_n` cost only their Stage-1 term, labels with
  `0 < dbar_i <= 2 s_n` cost the same as top labels), and the monitor slack is `1 + b_n` not `1 + 2 b_n`.
- (B) PROVED; benchmark loss `<= eps_bar n` (in fact `<=` Bayes error x n, and `<= omega' eps_bar n`),
  constant 1 exact.
- (C) PROVED; loss `<= eps_bar n`, exactly 0 with one honest agent, constant 1 exact.
- Conviction of `S*_N` winners: PROVED, `<= (2n^3)^{-1} + (2n^4)^{-1}` per label.
- D-learn: PROVED with extra `2 Lambda gam_n n + 2n^{-3}`, `gam_n = sqrt((|A| log 2 + log(K n^4))/(2 L_n))`.
- (D) rates: immediate from the bounds; sublinear iff `Q_B = o(n^{1/3} (log n)^{-1/3})` (for D-learn also
  `|A| = o(n^{2/3})`).
- Proposition I: PROVED in the corrected form of Part 5 (pathwise coupling; gain
  `>= (p - alpha_w) eps (1 - theta) n`, exact).

### Where the scout's statements are false or needed changing
1. `2 eps` -> `eps` (both benchmarks); the scout's own example attains `eps`, so "tight up to factor 2" is wrong
   in the other direction.
2. D-learn extra term is `2 gam n` (times `Lambda`), not `n gam`; and `gam` should carry `log(K n^4)` for the
   union over possible winners.
3. "Water-filling dominates the pointwise S* at every type": true for strategic agents, false for honest ones.
4. Conviction bound should include the bid-tail term `(2n^4)^{-1}` per label.
5. Prop. I corollary: the comparator "deliver 1/2 throughout" makes the inequality false for some label-only
   mechanisms (it can be rewarded at label-`gamma` rounds); replace by the cooperative comparator (capacity at
   non-winning labels) and specify the shader's label-`gamma` behaviour. The `O(sqrt n)` is unnecessary.
6. Reading of Prop. I: it rules out protecting POINTWISE compliance under arbitrary order for every
   label-only mechanism; it does not show that every label-only mechanism loses order robustness. For
   PL-MESP (permanent conviction) the loss is real and linear (E4).
7. Linear cost is not needed: the theorem holds for the paper's convex costs with the factor `Lambda`.

### Audit of indicator x conditional expectation (every occurrence)
- (P3): `1{X_t = a} F_t(a)`, `F_t(a)` is `G_t`-measurable: pulled out correctly.
- Lemma 3, Lemma 4, baseline optional stopping, revenue 2.1: `1{k <= rho}` is `G_{u_k}`-measurable (depends on
  earlier rewards at `b` only).
- Fallback: `1{I_t = j}` is `G_t`-measurable (selection precedes the type and the seed).
- Case 1: the slope `g` and the price `tau` multiply `M_N`; both are `F^b`-measurable, so `E[g M_N | F^b] = 0`.
- Events `G_b`, `U_b`, `H_b`, `E^TV_b`, `W'_b` are `F^b`-measurable, so their indicators multiply the
  conditional bounds legitimately.
### Audit of union bounds over index sets
- Over agents `k in [K]` (Lemma 2, Lemma 7): deterministic.
- Over monitor times `r <= N_b` (Lemma 4): deterministic given `B` (the visit count is a function of `B`).
- Over labels: never a union bound; bad events are charged `2 N_b P(bad_b | B)` and summed with
  `sum_b N_b <= n`, `sum_b N_b^2 <= n^2`, so `Q_B` never multiplies a failure probability.

### Least secure step
The sharpening in Lemma 2(e) + Case 1 of Part 1 for labels where `i` is NOT top but wins
(`0 < dbar_i(b) <= 2 s_n`), and its consequence (Part 1b) that the paper's own Prop. X(i) can be made uniform
over instances. The argument is short (the deviator's bid is pathwise below its capacity bid, which is in the
good event; the fallback comparison is made at `w = min{Vbar_i, Mbar_i}`), I checked it twice and E3 supports
it on one instance, but it contradicts an explicit remark in both the paper and c2, so it is the step an
adversary should attack first. Second least secure: the three-case analysis of Lemma 7 (D-learn), in
particular the choice of the LARGEST water level so that `that = Mhat` forces full capacity.
