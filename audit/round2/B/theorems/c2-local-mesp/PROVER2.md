# C2, profile-local MESP: independent attempt (Prover 2)

Status of this document. Sections 1 to 3 were written before I opened Section 4 of
`audit/round2/B/MATH_CANDIDATE_LEDGER.md`, as the role brief requires; Section 8 records the
differences after I read it. I did not open `PROVER1.md`. Nothing here is claimed to be correct;
Section 9 lists what I did not establish and the step I consider least secure.

Conventions. All notation follows `audit/round2/B/CONTEXT_PROOF_CONTRACT.md`. `log` is natural,
`(x)_+ = max(x,0)`, `1{.}` is an indicator, `[K] = {1,...,K}`. I write `mu_i^z := mu_i(z_i)` and
`M_i^z := M_i(z_i)` for the primitives of agent `i` at the full profile `z = (z_1,...,z_K)`,
`M_*(z) := max_i M_i^z`, `T(z) := {i : M_i^z = M_*(z)}`, `V_i^z := max_{j != i} M_j^z`,
`M_(2)(z) :=` the second largest of `(M_1^z, ..., M_K^z)` counting multiplicity (so
`M_(2)(z) = V_i^z` for any `i in T(z)`), and `b(z) := max_{h in K_H} mu_h^z`.


## 1. What I set out to prove, and the five stress points

Target: a monitored empirical second-price mechanism that keys on the exact context profile,
gives (i) an additive behavioral asymptotic equilibrium against the fully global-history-adaptive
class `B^ctx_{i,n}` of the contract, (ii) revenue `E sum_t M_(2)(X_t) - o(n)`, and (iii)
`P(n;S) >= E sum_t b(X_t) - o(n)` for every feasible behavioral profile.

The five stress points named in my brief, and where each is answered in this document:

1. *Filtration of the martingale arguments, with targets predictable in the global history.*
   Every martingale argument below is stated in the global filtration **enlarged by the entire
   arrival path** (Section 5.1, convention F-A). This is legitimate because arrivals are
   independent of the reward seeds and of every coin, and it is what makes a local monitor
   survive a deviator whose target at a visit to `z` depends on everything it has seen at all
   other profiles. See Lemma M (Section 5.3): the only probabilistic input is that, given
   everything except the current round's seed, the reward is Bernoulli at the chosen target.
2. *Unknown local horizon in the fallback.* Solved by tuning the local EXP3 fallback to the
   **global** horizon `n`, which upper bounds every local horizon, and proving a truncated
   (prefix) version of the selected-reactive EXP3 lemma: Lemma F (Section 5.4). No doubling
   trick is needed, and the loss `R_K(n) = 3 sqrt(Kn log K) + 2K log K` per profile is lower
   order than the bidding term.
3. *Cross-profile contamination.* Ruled out by construction, not by an estimate: the mechanism's
   decision at a round is a measurable function of the current profile, the data collected at
   earlier visits to that same profile, and coins attached to that profile only (Lemma L,
   Section 5.2). A fallback at `z` changes no statistic, price, or phase at any `z' != z`.
4. *Profiles with too few visits.* Stage 1 at `z` occupies the first `K L_n` visits to `z` and
   need not finish. A profile that never leaves Stage 1 is charged its own visit count, at most
   `K L_n`; the total over `Q` profiles is `Q K L_n = o(n)` for fixed `Q`.
5. *Ties in capacity inside a profile, and `K = 2`.* Ties are handled exactly as in the scalar
   mechanism (second order statistic with multiplicity, uniform priority), and the top branch of
   the proof only needs `tau_{i,z} <= V_i^z <= M_i^z`, which is what `i in T(z)` says. `K = 2` is
   the case `V_i^z = M_j^z` for the single other agent `j`; nothing in the proof degenerates.
   No two-top condition of any kind is used. This is in contrast to the public contextual
   results, which need `|T(z)| >= 2`.

A sixth point, not on the list but the one I found most delicate, is the **seed indexing of the
bid-domination coupling**. Ambiguity 1 of the contract warns that a pathwise claim across two
executions in which the same *local* pull index occurs at different rounds does not follow from
pointwise feasibility. I avoid the issue entirely: seeds are attached to **rounds**, and the
Stage-1 schedule at a profile is a deterministic function of the arrival path, so the round
carrying agent `i`'s `r`-th Stage-1 pull at `z` is the same in both coupled executions
(Section 5.5). No relabeling of seeds is performed anywhere in this document.


## 2. The mechanism: PL-MESP (profile-local monitored empirical second price)

Written before reading the ledger.

**Platform knowledge.** `n` and `K` only. Not `Q`, not `X_F`, not the arrival law, not
`mu_i(.)`, `M_i(.)`, or `K_H`. Profiles are instantiated lazily on first arrival.

**Parameters** (all functions of `n` and `K` alone). For `n >= 2K`:

```
L_n   := min{ floor(n/(2K)), ceil( n^{2/3} (log(en))^{1/3} ) }            (Stage-1 length per agent)
ell_n := log(2 n^5)
s_n   := sqrt( ell_n / (2 L_n) )                                          (bid confidence radius)
b_n(r):= sqrt( r ell_n / 2 ),   b_n(0) := 0                               (monitoring boundary)
gamma_n := min{ 1/2, sqrt( K log K / n ) },   eta_n := gamma_n / K        (fallback EXP3)
R_K(n)  := 3 sqrt(K n log K) + 2 K log K,   R_K(0) := 0
```

For `n < 2K`, allocate cyclically and stop; finitely many horizons, absorbed into instance
constants. Note that `ell_n` and hence `s_n`, `b_n` use `n^5`, not `n^4` as in the scalar
mechanism, and contain no `Q` and no `K`: the extra power of `n` pays for the union bound over
the at most `n` (profile, local index) pairs that can occur in `n` rounds. This is the device
that lets the platform not know `Q`.

**Per-profile state.** For each profile `z` met so far the platform keeps: the local visit count
`v_z`; the Stage-1 reward sums; the announced price `tau_z`; the identity `W_z` of the local
winner; the local primary count `r_z` and reward sum `Z_z`; local EXP3 weights. It keeps one
independent uniform priority permutation `Pi_z` of `[K]`, drawn when `z` is first met.

**Round `t`.** Observe `X_t = z`, increment `v_z`, and act according to `z`'s local phase.

*Stage 1 (bidding), while `v_z <= K L_n`.* Pull agent `((v_z - 1) mod K) + 1`. (Deterministic
round robin in label order. Agent `i`'s `r`-th Stage-1 pull at `z` is the `((r-1)K + i)`-th visit
to `z`.) When `v_z = K L_n`, form the empirical bids
`beta_{i,z} := L_n^{-1} sum_{r<=L_n} Y_{i,z,r}`, let `W_z` be a largest bidder, ties resolved by
the highest `Pi_z` priority, announce
`tau_z := (beta_{(2),z} - s_n)_+`, `beta_{(2),z}` the second order statistic with multiplicity,
and set `r_z <- 0`, `Z_z <- 0`.

*Stage 2 (monitored primary), while no switch has occurred at `z`.* Pull `W_z`; set
`r_z <- r_z + 1` and `Z_z <- Z_z + Y_t`; if `Z_z < r_z tau_z - b_n(r_z)`, declare a local switch
at `z` and move `z` to Stage 3. The test uses only rewards collected at `z`.

*Stage 3 (local fallback), after a switch at `z`.* Run explicit-exploration EXP3 over all `K`
agents, restricted to visits to `z`, with fresh weights `w_{i,1} = 1` and the parameters
`gamma_n, eta_n` above, i.e. `p_{i,t} = (1-gamma_n) q_{i,t} + gamma_n/K`,
`hatY_{i,t} = Y_t 1{I_t = i} / p_{i,t}`, `w_{i,t+1} = w_{i,t} exp(eta_n hatY_{i,t})`, the local
time `t` counting visits to `z` since the switch. The fallback is tuned to `n`, not to the
number of remaining visits to `z`, which the platform cannot know.

**Messages.** When the platform selects an agent at round `t` it tells it the current profile's
phase ("bidding", "primary", "fallback") and, once Stage 1 at that profile is over, the price
`tau_z`. This is needed for `S^*` below to be implementable, because a selected agent cannot
otherwise distinguish a primary pull from a fallback pull. Since all guarantees below are uniform
over the whole class `B^ctx_{i,n}`, giving agents this extra information cannot hurt them.

**Proposed profile `S^*`** (profile-local, phase-dependent, feasible on every history): at a
visit to `z`, agent `i` delivers `M_i^z` in Stage 1 and in Stage 3; as the Stage-2 winner it
delivers `min{tau_z, M_i^z}` if strategic and `max{mu_i^z, min{tau_z, M_i^z}}` if honest.


## 3. My proof outline, written before reading the ledger

O1. **Condition on the arrival path.** Arrivals are exogenous and independent of seeds and coins,
so we may condition on `A := (X_1,...,X_n)` throughout and integrate at the very end. Under this
conditioning every visit count `V_z`, every Stage-1 pull round, and the length of every local
fallback become deterministic, while the seeds and coins keep their laws. All filtrations below
contain `sigma(A)` from time zero.

O2. **Profile locality (Lemma L).** By construction the mechanism's phase, price, winner, switch
time and fallback distribution at `z` are measurable functions of the data collected at visits to
`z` and of `Pi_z` and the fallback coins used at `z`. Hence a switch at `z` changes nothing at any
other profile, and the price `tau_z` depends only on the Stage-1 rewards delivered at `z`. Agents
can still correlate across profiles; the mechanism cannot.

O3. **Additive accounting.** `u_i = sum_z E[U_{i,z}]` where `U_{i,z}` is the realized utility of
`i` at visits to `z`. Additivity of expectation needs no independence across profiles, so a
deviator that couples its behavior across profiles is handled by bounding each term separately,
uniformly over everything it may condition on.

O4. **The monitor in the global filtration (Lemma M).** Put a predictable indicator on the rounds
that are primary pulls at `z` and form the global-time martingale
`M^z_t = sum_{s<=t} 1{s is a primary pull at z} (Y_s - m_{I_s,s})`. Its increments are, given
everything up to the target choice, centered and of range at most 1, whatever the deviator has
seen elsewhere. A supermartingale exponential bound, stopped at the round of the `r`-th primary
pull, gives the fixed-`r` tail `exp(-2 b_n(r)^2 / r) = (2n^5)^{-1}`. Conditional on `A` the number
of (profile, local index) pairs is `sum_z V_z = n`, so the union bound costs `n^{-4}` in total and
no knowledge of `Q` is needed.

O5. **The fallback with an unknown local horizon (Lemma F).** Prove a prefix version of the
selected-reactive EXP3 lemma: with `gamma_n` tuned to `n`, for any `H <= n` actually played the
reward is at least `vH - R_K(n)` where `v` bounds the comparator's conditional mean when selected.
The exponential-potential inequality holds for every prefix, and the tuning is only used at the
end through `2 gamma_n H + K log K / gamma_n <= R_K(n)`. Conditional on `A`, `H` is measurable at
the fallback start, but the algorithm still cannot use it, which is exactly why the prefix version
is the one needed.

O6. **Bid domination with round-indexed seeds (Lemma B).** Stage-1 schedules are deterministic
given `A`, so the two coupled executions pull the same agent at the same round during Stage 1 at
`z` and see the same seed there. Feasibility gives `Y' <= Y^max` pathwise on every Stage-1 pull of
the deviator, all other Stage-1 rewards at `z` are identical, hence `beta'_{i,z} <= beta^max_{i,z}`
and `{deviation wins z} subset {baseline wins z}`, with the common price
`tau_{i,z} := (max_{j != i} beta_{j,z} - s_n)_+`, a function of the other agents' Stage-1 rewards
at `z` only.

O7. **Per-profile top branch.** On the good bidding event at `z` (`|beta_{j,z} - M_j^z| <= s_n`
for `j != i`) we have `tau_{i,z} <= V_i^z <= M_i^z` when `i in T(z)`. The monitor bounds the
deviator's primary utility at `z` by `q(1 + mu_i^z - tau_{i,z}) + 1 + 2 b_n(q)`; Lemma F bounds
its fallback utility by `(1 + mu_i^z - V_i^z) H + R_K(n) <= (1 + mu_i^z - tau_{i,z}) H + R_K(n)`;
the baseline gets at least `(1 + mu_i^z - tau_{i,z}) N_z` up to a false switch of probability
`(2n^4)^{-1}`, with the separate honest sub-branch when `tau_{i,z} <= mu_i^z`. Following the
adjudicated Note 1 of `PRIVATE_BOUND_NOTES.md`, the comparison is made at `tau_{i,z}` and never
at `V_i^z - 2 s_n`, so no `n s_n` term enters the deviation gain.

O8. **Per-profile non-top branch.** If `i` is not in `T(z)`, then `delta_i^z := V_i^z - M_i^z > 0`,
and once `2 s_n <= delta_i^z / 2` the monitor caps the local primary tenure at
`4 (1 + sqrt(2 ell_n))^2 / (delta_i^z)^2` and Lemma F caps the expected local fallback pull count
at `R_K(n)/delta_i^z`. The baseline is nonnegative.

O9. **Summation.** Stage 1 costs at most `L_n` of gain per profile; `sum_z b_n(V_z) <=
sqrt(Q n ell_n / 2)` by Cauchy-Schwarz; the bad events cost `O(n^{-2})`. Revenue and the honest
benchmark repeat the monitor and fallback steps for the announced price and for the best honest
agent at each profile respectively, with the price shortfall `2 s_n` charged once per round,
giving the `n s_n` term that the scalar theorem also has.

Anticipated failure modes I checked against, and their resolutions, are collected in Section 7.


## 4. The theorem, with every hypothesis explicit

### 4.1 Hypotheses

**(H1) Agents and primitives.** `K >= 2` agents. A finite set `X_F` of full profiles,
`Q := |X_F| < infinity`. For every `z in X_F` and `i in [K]`, `mu_i^z in [0,1]` and
`M_i^z in [mu_i^z, 1]`. A fixed nonempty honest set `K_H subset [K]`, the same at all profiles.
No regularity of any kind (no Lipschitz, no continuity, no top-set condition, no positive mass) is
assumed, and no relation between the primitives at different profiles is assumed.

**(H2) Horizon.** `n` is known to the platform and `n >= 2K`. Guarantees are fixed-horizon; no
anytime claim is made.

**(H3) Exogenous arrivals.** The arrival sequence `A := (X_1, ..., X_n)` takes values in `X_F` and
is independent of the reward-seed array, of every mechanism coin, and of every agent's private
coin array. It is otherwise arbitrary: it need not be i.i.d., need not have positive masses, may
be deterministic, and may be adversarial as long as it is chosen without access to the seeds and
coins. (Contrast: the manuscript's grid results need i.i.d. arrivals through Lemma `lem:cell-law`,
and the contract records at item 11.5 a counterexample when i.i.d.-ness is dropped there.)

**(H4) Reward generation.** There is an array `(U_t)_{t<=n}` of i.i.d. uniform `[0,1]` variables,
independent of `A`, of the mechanism coins, and of the agents' private coins. At round `t` the
platform selects `I_t`, the selected agent chooses a target `m_{I_t,t} in [0, M_{I_t}^{X_t}]`, and
only then is `Y_t := 1{U_t <= m_{I_t,t}}` realized. (This is the contract's "targets are chosen
before fresh conditionally independent Bernoulli seeds", with seeds attached to rounds.)

**(H5) Deviator class.** The deviating agent `i` may use any `S'_{i,n} in B^ctx_{i,n}` as defined
in Section 5 of the contract: after being selected at round `t`, it chooses
`m_{i,t} in [0, M_i^{X_t}]` as an arbitrary measurable function of `n`, the current profile `X_t`,
its own entire history across all profiles (the rounds at which it was selected, the profiles
there, its targets, its realized rewards, and every message the mechanism sent it, including
local phase labels and local prices), and its independent private randomness. If `i in K_H` then
`m_{i,t} >= mu_i^{X_t}` after every history. All other agents play `S^*_{-i}`.

**(H6) Platform knowledge.** The platform knows `n` and `K`. It does not know `Q`, `X_F`, the
arrival law, any `mu_i(.)`, any `M_i(.)`, or `K_H`.

**(H7) Instance constants.** For agent `i` put
`delta_i := min{ V_i^z - M_i^z : z in X_F, i not in T(z) }` when that set is nonempty, and
`delta_i := +infinity` otherwise (i is top at every profile). `delta_i > 0` because `X_F` is
finite.

### 4.2 Error terms

With the parameters of Section 2, and `ell_n = log(2n^5)`:

```
e_bid(n)   := Q L_n
e_mon(n)   := Q + sqrt( 2 Q n ell_n )
e_fb(n)    := Q R_K(n)
e_price(n) := 2 n s_n
e_stage1(n):= Q K L_n
e_low(n)   := Q_i^- [ 8 (1 + sqrt(2 ell_n))^2 / delta_i^2 + 2 R_K(n) / delta_i ]
             where Q_i^- := #{ z : i not in T(z) } <= Q   (so e_low = 0 if delta_i = inf)
```

### 4.3 Theorem (profile-local MESP)

*Assume (H1) to (H7) and run PL-MESP of Section 2. Then:*

**(A) Additive behavioral equilibrium.** *For every agent `i` and every `n >= 2K` such that
`4 s_n <= delta_i`,*
```
 sup_{S'_{i,n} in B^ctx_{i,n}} [ u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n) ]
   <= e_bid(n) + e_mon(n) + e_fb(n) + e_low(n) + 6 n^{-3}.
```
*If `i` is top at every profile (`delta_i = infinity`) the bound holds for every `n >= 2K` with
`e_low = 0`. For the finitely many smaller horizons the left side is at most `2n`.*

**(B) Second-capacity revenue.** *For every `n >= 2K`,*
```
 P(n; S^*_n) >= E[ sum_{t<=n} M_(2)(X_t) ] - ( e_stage1(n) + e_price(n) + e_fb(n) + n^{-3} ).
```

**(C) Honest-benchmark robustness.** *For every feasible behavioral profile `S` in which every
agent plays some strategy in `B^ctx_{j,n}` and every honest agent respects pointwise honesty
(the deviating set may be all of `[K]`),*
```
 P(n; S) >= E[ sum_{t<=n} b(X_t) ] - ( e_stage1(n) + e_price(n) + e_mon(n) + e_fb(n) + 2 n^{-3} ).
```

**(D) Rates.** *For fixed `K`, fixed `Q`, and a fixed instance, all three error terms are
`O(n^{2/3} (log n)^{1/3})`; explicitly, `L_n <= n^{2/3}(log(en))^{1/3} + 1`,
`n s_n <= sqrt(5/2) n^{2/3} (log n)^{1/3} (1 + o(1))`, `sqrt(2 Q n ell_n) = O(sqrt(Q n log n))`
and `R_K(n) = O(sqrt(K n log K))`. In particular `S^*` is an additive behavioral asymptotic
equilibrium in the sense of Definition 1 of the contract, the revenue is
`E sum_t M_(2)(X_t) - o(n)`, and the honest benchmark holds at the same order. The equilibrium
bound is uniform over the declared deviations for each fixed instance but not over sequences of
instances whose positive gaps `delta_i` vanish.*

**Remark 4.1 (explicit `Q` dependence).** The dominant terms are `Q K L_n` and `2 n s_n`. If the
platform is additionally told an upper bound `Qbar >= Q`, taking
`L_n := min{floor(n/(2K)), ceil( (n/(Qbar K))^{2/3} (log(en))^{1/3} )}` balances them and gives
error `O((Qbar K)^{1/3} n^{2/3} (log n)^{1/3})`. With `Q` unknown the statement above keeps
`Q K L_n`. All three bounds are vacuous unless `Q K L_n = o(n)`, i.e. unless
`Q = o( n^{1/3} (log n)^{-1/3} / K )`.

**Remark 4.2 (no two-top condition and no regularity).** Unlike `thm:finite-context` (public part)
and `thm:contextual-public`, nothing here requires `|T(z)| >= 2`, positive profile masses,
continuity, or i.i.d. arrivals. The price of this is that the guarantee is about the second
capacity `M_(2)(z)` rather than the first, which is the same trade the scalar `thm:private-mesp`
makes.

**Corollary 4.3 (known finite partition).** Let `X` be an arbitrary measurable context space and
suppose the platform is given a finite measurable partition `X = R_1 union ... union R_Q` such
that every `mu_i(.)` and every `M_i(.)` is constant on each `R_l`. Run PL-MESP keyed on the
partition cell instead of the exact profile. Then (A), (B), (C) hold verbatim with `z` ranging
over cells and `M_(2)(.)`, `b(.)` evaluated at the (constant) cell values. *Proof:* within a cell
every agent's feasible target set is the fixed interval `[0, M_i^{R_l}]` and every primitive is
constant, so the proof below applies word for word; it never uses that cells are singletons, only
that primitives are constant on them. This is the exact point at which a genuinely continuous
grid version breaks: on a cell over which `M_i(.)` varies, a bid estimates an average delivered
mean rather than a fixed capacity, the monitor may charge an agent a price above its local
capacity at some contexts inside the cell, and Lemma B below no longer has a fixed comparison
target `M_i`.


## 5. Proof

Throughout, `S^*` is the profile-local proposed profile of Section 2 and all statements are for
`n >= 2K`.

### 5.1 Probability space, filtrations, and the standing conditioning

The primitives of the space are five mutually independent families: the arrival sequence `A`; the
reward seeds `(U_t)_{t<=n}` i.i.d. uniform `[0,1]`; the mechanism's tie priorities `(Pi_z)_{z in
X_F}`, i.i.d. uniform permutations of `[K]`; the mechanism's selection coins `(xi_t)_{t<=n}`,
i.i.d. uniform `[0,1]`, used only by local fallbacks; and the agents' private coin arrays. This is
exactly (H3) and (H4).

Define the global filtration `F_t := sigma(A, the seeds U_1, ..., U_t, the coins used at rounds
1, ..., t, and every quantity realized through round t)`; note that coins not yet used, in
particular the fallback coin of a future round, are deliberately NOT in `F_t`, since Lemma F needs
the selection at a fallback round to be conditionally random and the pre-seed field
`F_t^- := sigma(F_{t-1}, X_t, I_t, m_{I_t,t})`, the information present at round `t` after the
target has been chosen and before `U_t` is used.

**Convention F-A (standing).** Every filtration below contains `sigma(A)` from time zero, that is,
we condition on the entire arrival path and integrate over it only at the very end. This is
legitimate by (H3) and (H4): `U_t` is independent of `(F_t^-, A)`, so

```
 E[ Y_t | F_t^- , A ] = m_{I_t,t},     and given (F_t^-, A) the variable Y_t - m_{I_t,t}
                                        lies in an interval of length 1.                    (5.1)
```

Conditioning on `A` only enlarges the deviation class: a strategy in `B^ctx_{i,n}` induces, given
`A`, a strategy that may in addition use the whole arrival path, and all bounds below are proved
for that larger class and uniformly in `A`, so integrating over `A` recovers the unconditional
claim. Under Convention F-A every visit count `V_z`, every Stage-1 pull round, and the length of
every local Stage-3 phase (given its start) are deterministic. Write `N_z := (V_z - K L_n)_+` for the
number of post-bidding visits to `z`. This is the whole content of the answer to "which filtration
are the martingale arguments in": the enlarged one, and (5.1) is the only probabilistic input, so
the arguments are indifferent to how much of the global history the deviator's target depends on.

I also record the trivial pathwise facts used repeatedly: per-pull agent utility
`1 + mu_i^z - m in [0,2]`, so any two executions differ in total utility by at most `2n`; and the
per-pull utility is nonnegative, so an agent's utility in any phase is nonnegative.

### 5.2 Lemma L (profile locality)

**Lemma L.** *In PL-MESP, for every profile `z`, the local phase at `z`, the bids `beta_{.,z}`,
the price `tau_z`, the winner `W_z`, the switch time, and the conditional selection distribution
used at each Stage-3 visit to `z` are measurable functions of: the visit count `v_z`, the rewards
realized at visits to `z`, the priority `Pi_z`, and the coins `xi_t` at visits to `z`. In
particular no quantity computed by the mechanism at `z` depends on anything realized at a visit to
any `z' != z`.*

*Proof.* Immediate from the description in Section 2: every branch reads only `z`'s own state, and
`z`'s state is updated only at visits to `z`. QED

Two consequences used below. First, a monitor switch at one profile cannot alter a price, a phase,
a statistic or a selection law at another profile: cross-profile contamination is excluded by
construction rather than bounded. Second, `tau_z` is a function of the Stage-1 rewards delivered at
`z` alone; when a deviator `i` wins at `z`, `tau_z = tau_{i,z} := (max_{j != i} beta_{j,z} - s_n)_+`
does not involve `i`'s own bid.

The deviator is of course *not* profile-local: its target at a visit to `z` may depend on
everything it has seen anywhere. Lemmas M, F and B are all proved under exactly that generality.

### 5.3 Lemma M (anytime monitor under the global filtration)

Fix a profile `z`. Call round `s` a *primary pull at `z`* if `X_s = z` and `z`'s local phase at
`s` is Stage 2; let `psi^z_s` be the indicator of that event. The local phase at `s` is determined
by the data collected at visits to `z` strictly before `s` (Lemma L), so `psi^z_s` is
`F_{s-1} or sigma(X_s)`-measurable; **under Convention F-A, `sigma(X_s) subset sigma(A) subset
F_0`, so `psi^z_s` is `F_{s-1}`-measurable**, that is, predictable. This is the one place where the
conditioning on the whole arrival path is indispensable rather than merely convenient, and it is
flagged again in Section 9. Let `r^z(s) := sum_{u<=s} psi^z_u`, `q_z := r^z(n)` the local
primary tenure, and, for `r <= q_z`, `Z^z_r` and `A^z_r` the sums of realized rewards and of
chosen targets over the first `r` primary pulls at `z`.

**Lemma M.** *Under (H1) to (H5) and Convention F-A, whatever feasible nonanticipating targets the
Stage-2 winners choose at all profiles:*

*(a) (tail) `Pr{ exists z in X_F, exists r <= V_z : |Z^z_r - A^z_r| > b_n(r) } <= n^{-4}`.*

*(b) (charge) On the complement of the event in (a), for every `z` with `q_z >= 1`,*
```
 A^z_{q_z} >= q_z tau_z - 1 - 2 b_n(q_z),
 and hence the winner's realized primary utility at z is at most
 q_z (1 + mu_{W_z}^z - tau_z) + 1 + 2 b_n(q_z).
```
*(c) (no false switch) If at profile `z` every primary target is at least `tau_z`, then the
probability that a switch occurs at `z` is at most `V_z (2 n^5)^{-1}`; summed over profiles, the
probability that any such switch occurs anywhere is at most `(2 n^4)^{-1}`.*

*(d) (unbiased primary revenue) `E[ Z^z_{q_z} - A^z_{q_z} ] = 0`, and the same identity holds
conditionally on the Stage-1 data at `z` together with `A`.*

*(e) (conditional form) For a fixed `z`, the per-profile statements inside (a) and (c), and the
identity (d), hold verbatim conditionally on any `F_t` with `t <= t_1(z)`, where `t_1(z)` is the
round of the `K L_n`-th visit to `z`; in particular conditionally on the field `D_z` used in
Section 5.6. This is because `M^z` is identically zero up to `t_1(z)` and the exponential
supermartingale bound below is itself conditional.*

*Proof.* Define the global-time process `M^z_t := sum_{s<=t} psi^z_s (Y_s - m_{I_s,s})`, with
`M^z_0 := 0`. By (5.1) and the `F_s^-`-measurability of `psi^z_s`,
`E[ psi^z_s (Y_s - m_{I_s,s}) | F_s^- ] = 0`, hence by the tower property
`E[ M^z_t - M^z_{t-1} | F_{t-1} ] = 0`: `M^z` is a martingale for `(F_t)` (which contains
`sigma(A)`). Moreover, conditionally on `F_s^-`, the increment lies in an interval of length
`psi^z_s`, so Hoeffding's lemma gives
`E[ exp(lambda psi^z_s (Y_s - m_s)) | F_s^- ] <= exp(lambda^2 psi^z_s / 8)`, and, taking the tower
expectation and using that `psi^z_s` is `F_{s-1} or sigma(X_s)`-measurable while `X_s` is
`sigma(A)`-measurable under Convention F-A, hence `F_{s-1}`-measurable,
```
 E[ exp(lambda (M^z_s - M^z_{s-1})) | F_{s-1} ] <= exp(lambda^2 psi^z_s / 8).            (5.2)
```
(d) is `E[M^z_n] = 0`, valid because `M^z` is a martingale with `M^z_n = Z^z_{q_z} - A^z_{q_z}`;
the conditional version follows because the Stage-1 data at `z` is `F_{t_1(z)}`-measurable, where
`t_1(z)` is the round of the `K L_n`-th visit to `z`, and `M^z` is constant up to that round.

For (a), fix `r >= 1` and let `T_r := min{ t : r^z(t) = r }` (`= +infinity` if `q_z < r`). The
stopped process `M^z_{t and T_r}` has predictable quadratic-range sum
`c_t := sum_{s<=t} psi^z_s 1{s <= T_r} <= r` pathwise. By (5.2),
`exp(lambda M^z_{t and T_r} - lambda^2 c_t / 8)` is a supermartingale started at 1, so
`E[ exp(lambda M^z_{n and T_r}) ] <= E[ exp(lambda^2 c_n/8) ] <= exp(lambda^2 r / 8)`, and the
Chernoff choice `lambda = 4 b / r` gives `Pr( M^z_{n and T_r} > b ) <= exp(-2 b^2 / r)`, likewise
for the lower tail. On `{q_z >= r}` we have `M^z_{n and T_r} = Z^z_r - A^z_r`. With
`b = b_n(r) = sqrt(r ell_n / 2)` each tail is `exp(-ell_n) = (2 n^5)^{-1}`. Under Convention F-A
the relevant index set is `{(z,r) : z in X_F, r <= V_z}`, of cardinality `sum_z V_z <= n`, so the
union over both tails costs at most `n * 2 * (2n^5)^{-1} = n^{-4}`, uniformly in `A`; integrating
over `A` preserves the bound. This is the step that makes knowledge of `Q` unnecessary.

For (b): if no switch occurred at `z` then the test failed at `r = q_z`, i.e.
`Z^z_{q_z} >= q_z tau_z - b_n(q_z)`, while on the complement of (a)
`Z^z_{q_z} <= A^z_{q_z} + b_n(q_z)`, whence `A^z_{q_z} >= q_z tau_z - 2 b_n(q_z)`. If a switch
occurred at `q_z` then the test failed at `q_z - 1` (or `q_z = 1`, where `A >= 0 >= tau - 1`
suffices), so `A^z_{q_z} >= A^z_{q_z -1} >= (q_z - 1) tau_z - 2 b_n(q_z - 1) >= q_z tau_z - 1 -
2 b_n(q_z)` using `tau_z <= 1` and monotonicity of `b_n`. The utility statement is
`U^pri = q_z (1 + mu^z_{W_z}) - A^z_{q_z}`.

(e) follows because every step above is an inequality between conditional expectations given
`F_{t-1}` for `t > t_1(z)`, and `M^z_{t} = 0` for `t <= t_1(z)`, so the supermartingale may be
started at `t_1(z)` instead of at 0.

For (c): if every primary target at `z` is at least `tau_z` then a switch at `r` forces
`Z^z_r - A^z_r <= Z^z_r - r tau_z < -b_n(r)`, the lower tail only, whose probability is at most
`(2n^5)^{-1}` for each `r <= V_z`; summing over `r <= V_z` and then over profiles gives the two
claims. QED

**Remark 5.1.** The only place the deviator's global-history adaptivity could have bitten is (5.1),
and it does not: conditioning on `F_s^-` already contains everything the deviator saw anywhere,
and the seed is fresh. The manuscript's scalar Lemma `lem:private-monitor` conditions on "the
bidding history" and calls the targets `F_{r-1}`-measurable in a local filtration; the statement
above replaces that by a global-time martingale with a predictable indicator, which is what the
contextual case needs, and in addition removes the implicit optional-stopping step in the
manuscript's revenue proof (part (d) here is an unconditional martingale identity, not an optional
stopping theorem applied to a bounded stopping time).

### 5.4 Lemma F (selected-reactive EXP3 with a truncated, unknown horizon)

**Lemma F.** *Fix a profile `z` and a fallback start there. Let `F_fb` be the field generated by
`A` and everything realized up to and including the switching round at `z`. Under Convention F-A
the number `H` of visits to `z` after the switch is `F_fb`-measurable, and `H <= n`. Suppose that
there is an agent `j` and a value `v in [0,1]` such that at every Stage-3 visit to `z` at which
`j` is selected, `j`'s conditional expected reward given the past is at least `v`. The other
agents, including a deviator, may choose arbitrary feasible nonanticipating targets after
selection, depending on their entire global histories. Then, with the local fallback run with the
parameters `gamma_n, eta_n` of Section 2, which are tuned to `n` and not to `H`,*
```
 E[ sum over the H Stage-3 visits to z of Y | F_fb ] >= v H - R_K(n),
 R_K(n) = 3 sqrt(K n log K) + 2 K log K.
```

*Proof.* Condition on `F_fb`; `H` is then a constant, `1 <= H <= n` (if `H = 0` there is nothing to
prove). Index the Stage-3 visits to `z` by `t = 1, ..., H` and let `J_{t-1}` be the global field
just before the selection at the `t`-th such visit (it contains `A`, so the identity of the round
is known). The weights `w_{.,t}` and hence `p_{.,t}` are `J_{t-1}`-measurable, `I_t` is drawn from
`p_t` using the fresh coin at that round, and `r_{i,t} := E[ Y_t | J_{t-1}, I_t = i ]` is well
defined; by hypothesis `r_{j,t} >= v` for all `t <= H`. The targets of the other agents are chosen
after selection and may depend on anything in `J_{t-1}` and on their own coins; no counterfactual
rewards for unselected agents are needed.

Since `p_{i,t} >= gamma_n / K = eta_n`, we have `0 <= eta_n hatY_{i,t} <= 1`, so `e^x <= 1 + x +
x^2` on `[0,1]` gives, with `Wsum_t := sum_i w_{i,t}` the local weight sum,
`log(Wsum_{t+1}/Wsum_t) <= eta_n sum_i q_{i,t} hatY_{i,t} + eta_n^2 sum_i q_{i,t} hatY_{i,t}^2`.
Summing over `t = 1..H` and bounding below by the single term `j`,
```
 sum_{t<=H} hatY_{j,t} - log K / eta_n
   <= sum_{t<=H} sum_i q_{i,t} hatY_{i,t} + eta_n sum_{t<=H} sum_i q_{i,t} hatY_{i,t}^2.  (5.3)
```
This inequality is pathwise and holds for the `H` rounds actually played, whatever `eta_n` is;
this is the only change from the manuscript's lemma, which fixes `eta` from the exact `H`.
Conditionally on `J_{t-1}`: `E[hatY_{j,t}] = r_{j,t} >= v`;
`E[sum_i q_{i,t} hatY_{i,t}] = sum_i q_{i,t} r_{i,t} =: Q_t`;
`E[sum_i q_{i,t} hatY_{i,t}^2] = sum_i q_{i,t} E[Y_t^2 1{I_t=i}]/p_{i,t}^2
 <= sum_i q_{i,t}/p_{i,t} <= K/(1 - gamma_n)`, using `p_{i,t} >= (1-gamma_n) q_{i,t}`. Writing
`G_t := sum_i p_{i,t} r_{i,t} = E[Y_t | J_{t-1}]` we have `G_t >= (1 - gamma_n) Q_t`. Taking
expectations in (5.3) and multiplying by `(1 - gamma_n)`,
```
 (1-gamma_n) v H <= (1-gamma_n) K log K / gamma_n + E[ sum_{t<=H} Y_t ] + gamma_n H,
```
so `E[sum_{t<=H} Y_t] >= v H - 2 gamma_n H - K log K / gamma_n` using `v <= 1` and
`gamma_n <= 1`. If `gamma_n = sqrt(K log K / n) <= 1/2` then, since `H <= n`,
`2 gamma_n H + K log K / gamma_n <= 3 sqrt(K n log K)`. Otherwise `gamma_n = 1/2` and
`n < 4 K log K`, so `2 gamma_n H + K log K/gamma_n <= n + 2 K log K <= 3 sqrt(K n log K) + 2 K log K`
because `sqrt(K n log K) >= sqrt(n * n/4) = n/2`. Either way the loss is at most `R_K(n)`. QED

**Remark 5.2.** Two facts make the unknown local horizon harmless. First, (5.3) is a prefix
inequality, so a run tuned to `n` and stopped after `H <= n` rounds still pays only
`2 gamma_n H + K log K/gamma_n`. Second, the fallback is never restarted at `z`, so no
"anytime" or doubling device is needed; a doubling version tuned to local time would also work and
would give `O(sqrt(K H log K) + K log K log H)`, but it is not needed because the crude bound
`R_K(n)` per profile is already of lower order than `L_n`. Note also that the fallback at `z` uses
only visits to `z`: the "rounds" of the lemma are separated by arbitrarily many rounds at other
profiles, during which the deviator acts and learns. Nothing in the proof cares, because
`J_{t-1}` contains all of it.

### 5.5 Lemma B (bid domination with round-indexed seeds)

Fix agent `i` and a deviation `S'_{i,n} in B^ctx_{i,n}`. Build both executions on the one space of
Section 5.1, with the same `A`, the same seeds `(U_t)`, the same priorities `(Pi_z)`, the same
fallback coins `(xi_t)`, and the same private coins; in execution 1 agent `i` plays `S'_{i,n}`, in
execution 2 (the baseline) it plays `S^*_i`; all other agents play `S^*` in both.

**Lemma B.** *Under Convention F-A: (a) for every `z`, the set of rounds constituting Stage 1 at
`z`, and the identity of the agent pulled at each of them, are the same in both executions, and
are deterministic; (b) for every `j != i` and every `z`, `beta_{j,z}` is the same random variable
in both executions and is an average of `L_n` i.i.d. Bernoulli(`M_j^z`) variables whenever Stage 1
at `z` completes; (c) `beta'_{i,z} <= beta^{max}_{i,z}` pathwise, where the prime denotes
execution 1 and `max` execution 2; (d) `{ i wins at z in execution 1 } subset { i wins at z in
execution 2 }`, and on the former event both executions announce the same price
`tau_{i,z} = (max_{j != i} beta_{j,z} - s_n)_+`; (e) agent `i`'s Stage-1 utility at `z` in
execution 1 exceeds its Stage-1 utility at `z` in execution 2 by at most `L_n`.*

*Proof.* (a) Stage 1 at `z` occupies the first `min{V_z, K L_n}` visits to `z` and assigns the
`k`-th visit to agent `((k-1) mod K) + 1`. Both the visit rounds and this assignment are functions
of `A` alone, hence deterministic under Convention F-A and identical across executions. This is
the point flagged as ambiguity 1 in the contract: no seed relabeling is used, the seed at a given
Stage-1 pull is the seed `U_t` of that round, and it is literally the same variable in both
executions.

(b) Agent `j != i` plays `S^*_j`, which delivers `M_j^z` at every Stage-1 visit to `z`, whatever
the history; so its Stage-1 rewards at `z` are `1{U_t <= M_j^z}` at the same rounds in both
executions. Given `A` these are i.i.d. Bernoulli(`M_j^z`).

(c) On the round `t` carrying agent `i`'s `r`-th Stage-1 pull at `z`, feasibility gives
`m'_{i,t} <= M_i^z`, hence `Y'_t = 1{U_t <= m'_{i,t}} <= 1{U_t <= M_i^z} = Y^{max}_t`. Summing over
`r <= L_n` and dividing by `L_n` gives (c). Note that `m'_{i,t}` may depend on everything the
deviator has seen at every profile; the inequality is pathwise regardless.

(d) Suppose `i` wins at `z` in execution 1, so `beta'_{i,z} >= beta_{j,z}` for all `j != i` and `i`
has the highest `Pi_z` priority inside the set of agents tied at `beta'_{i,z}`. In execution 2,
`beta^{max}_{i,z} >= beta'_{i,z} >= beta_{j,z}` for all `j != i` by (b) and (c), so `i` is again a
largest bidder; if the inequality `beta^{max}_{i,z} > beta'_{i,z}` is strict then no `j != i` ties
with `i` and `i` wins outright, and otherwise the tie set and the priority are unchanged, so `i`
wins again. When `i` wins, the second order statistic with multiplicity equals
`max_{j != i} beta_{j,z}`, which by (b) is the same in both executions.

(e) Per Stage-1 pull at `z` the utility difference is `M_i^z - m'_{i,t} <= 1`, and there are at
most `L_n` such pulls. QED

**Remark 5.3.** (d) is the only pathwise statement carried past Stage 1. After Stage 1 the two
executions may diverge completely at `z` (different switch times, different fallbacks), and they
are compared only through conditional expectations given the Stage-1 data at `z`, exactly as in the
scalar proof. They may also diverge at other profiles in execution 1 through the deviator's own
choices, which is why the comparison must be, and below is, made profile by profile with bounds
uniform over everything else.

### 5.6 Proof of (A): additive behavioral equilibrium

Fix `i` and `S'_{i,n} in B^ctx_{i,n}`, and build the two coupled executions of Section 5.5. For a
profile `z` let `U'_{i,z}` and `U_{i,z}` be agent `i`'s realized utilities at visits to `z` in
execution 1 and execution 2, split into a Stage-1 part and a post-bidding part. Since expectation
is additive and `T_i(n) - C_i(n) = sum_z U_{i,z}` pathwise,
```
 u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n) = sum_{z in X_F} ( E[U'_{i,z}] - E[U_{i,z}] ).  (5.4)
```
No independence across profiles is used or needed in (5.4); this is the step that absorbs a
deviator whose behavior at `z` depends on its entire history at all other profiles.

By Lemma B(e) the Stage-1 parts contribute at most `L_n` per profile, so at most `e_bid(n) =
Q L_n` in total, on every path. It remains to bound the post-bidding parts.

**Conditioning.** Fix `z` with `V_z >= K L_n` (otherwise `N_z = 0`, there is no post-bidding part
at `z`, and the profile contributes nothing beyond its Stage-1 term). Let `t_1(z)` be the round of
the `K L_n`-th visit to `z` and let `D_z` be the joint field generated by everything realized in
both executions through round `t_1(z)`, together with `A`. Then `D_z` is `sigma(A)`-enlarged past
information, so Lemma M (conditional form, see the proof of Lemma M: `M^z` vanishes before
`t_1(z)`, so its exponential supermartingale bound holds given `D_z`) and Lemma F apply
conditionally on `D_z` in each execution separately. Under Convention F-A, `V_z` and `N_z` are
constants, and by Lemma B the events
```
 E^win_z := { i wins at z in execution 1 },     G_{-i,z} := { |beta_{j,z} - M_j^z| <= s_n, all j != i }
```
and the price `tau_{i,z}` are `D_z`-measurable, and on `E^win_z` agent `i` also wins at `z` in
execution 2 at the same price. Write `Bad^1_z` for the failure of the monitor event of Lemma M(a)
at `z` in execution 1 and `FS^2_z` for the event that a switch occurs at `z` in execution 2.

*Legitimacy of conditioning on the joint field.* Both executions are measurable functions of the
same primitive families of Section 5.1, and for every `t` the pair `(U_t, xi_t)` is independent of
the field generated by `A`, the priorities, the private coins, and `(U_s, xi_s)` for `s < t`.
Consequently: each execution is marginally a correct run of PL-MESP against its own profile, since
at each of its rounds the seed and the fallback coin are fresh given that execution's own past;
and every conditional bound in Lemmas M and F remains valid when the conditioning field is the
joint one, because their only probabilistic inputs are (5.1), that the current seed is fresh given
everything else realized so far, and that the current fallback coin is fresh given the past. The
joint field `D_z` contains no seed and no coin of a round after `t_1(z)`.

**Branch 0: `G_{-i,z}` fails.** Bounding the post-bidding difference at `z` by `2 V_z`, summing
over `z`, using `sum_z V_z = n` and the union bound of Lemma B(b) with Hoeffding
(`2 exp(-2 L_n s_n^2) = n^{-5}` per completed (agent, profile) bid, at most `n` such pairs given
`A`), the total contribution is at most `2 n * n^{-4} = 2 n^{-3}`.

All remaining branches are on `G_{-i,z}`.

**Branch 1: `i` loses bidding at `z` in execution 1.** Then `i` receives no post-bidding pull at
`z` unless a switch occurs at `z`. The execution-1 winner `W_z != i` plays `S^*`, and on
`G_{-i,z}` we have `tau_z <= (beta_{W_z,z} - s_n)_+ <= M_{W_z}^z` (because `W_z` is a largest
bidder and its bid is within `s_n` of `M_{W_z}^z`), so `S^*` makes it deliver at least `tau_z` at
every primary pull; by Lemma M(c) a switch at `z` then has probability at most `V_z (2 n^5)^{-1}`
given `D_z`. Hence `E[U'^{post}_{i,z} | D_z] <= 2 V_z * V_z (2n^5)^{-1}`, while
`E[U^{post}_{i,z} | D_z] >= 0`. Summing over `z` and using `sum_z V_z^2 <= n^2` gives at most
`n^{-3}`.

All remaining branches are on `E^win_z and G_{-i,z}`.

**Branch 2: `i in T(z)`, and either `i` is strategic or `i` is honest with `tau_{i,z} > mu_i^z`.**
Since `i in T(z)`, `tau_{i,z} <= V_i^z <= M_i^z` on `G_{-i,z}`.

*Deviation side.* Let `q` be the primary tenure of `i` at `z` in execution 1 and `H = N_z - q` the
length of the local fallback. On the complement of `Bad^1_z`, Lemma M(b) gives
`U'^{pri}_{i,z} <= q (1 + mu_i^z - tau_{i,z}) + 1 + 2 b_n(q)`, and `q <= V_z` with `b_n`
increasing. Lemma F with the comparator `j` attaining `M_j^z = V_i^z` (any `j != i` with maximal
capacity at `z`; it exists since `K >= 2` and it plays `S^*`, delivering `M_j^z` at every Stage-3
visit to `z`) gives `E[sum Y | F_fb] >= V_i^z H - R_K(n)`; since every agent other than `i`
delivers at most `V_i^z` in the fallback, `E[sum Y | F_fb] <= barA_i + V_i^z (H - barQ_i)`, so
`barA_i >= V_i^z barQ_i - R_K(n)` and, using `1 + mu_i^z - V_i^z >= 0` (true because
`V_i^z <= 1`), `barQ_i <= H` and `tau_{i,z} <= V_i^z`,
```
 E[ U'^{fb}_{i,z} | F_fb ] = (1 + mu_i^z) barQ_i - barA_i <= (1 + mu_i^z - V_i^z) H + R_K(n)
                          <= (1 + mu_i^z - tau_{i,z}) H + R_K(n).
```
Since `1 + mu_i^z - tau_{i,z} >= 0` and `q + H = N_z`, taking conditional expectations given `D_z`
and adding the cost `2 V_z Pr(Bad^1_z | D_z)` of the monitor bad event,
```
 E[ U'^{post}_{i,z} | D_z ] <= (1 + mu_i^z - tau_{i,z}) N_z + 1 + 2 b_n(V_z) + R_K(n)
                              + 2 V_z Pr(Bad^1_z | D_z).                                   (5.5)
```

*Baseline side.* In execution 2, `i` wins at `z` and `S^*_i` makes it deliver exactly `tau_{i,z}`
at every primary pull (`min{tau, M_i^z} = tau` for a strategic `i`;
`max{mu_i^z, min{tau, M_i^z}} = tau` for an honest `i` with `tau > mu_i^z`). If no switch occurs
it is pulled at all `N_z` post-bidding visits to `z`, so
```
 E[ U^{post}_{i,z} | D_z ] >= (1 + mu_i^z - tau_{i,z}) N_z - 2 N_z Pr(FS^2_z | D_z),       (5.6)
```
and by Lemma M(c) applied to execution 2, in which all primary targets at `z` equal `tau_{i,z}`,
`Pr(FS^2_z | D_z) <= V_z (2 n^5)^{-1}`.

Subtracting, on this branch
`E[ (U'^{post} - U^{post})_{i,z} | D_z ] <= 1 + 2 b_n(V_z) + R_K(n) + 2 V_z Pr(Bad^1_z|D_z)
 + 2 V_z * V_z (2n^5)^{-1}`.

**Branch 3: `i in T(z)`, `i` honest, `tau_{i,z} <= mu_i^z`.** Honesty forces every deviating target
at `z` to be at least `mu_i^z`, so each post-bidding pull is worth at most 1 to `i`, and it has at
most `N_z` such pulls: `E[U'^{post}_{i,z} | D_z] <= N_z`. In execution 2, `S^*_i` delivers exactly
`mu_i^z` at each primary pull, worth exactly 1, so `E[U^{post}_{i,z}|D_z] >= N_z - 2 N_z
Pr(FS^2_z|D_z)` with `Pr(FS^2_z|D_z) <= V_z (2n^5)^{-1}` as above (the target `mu_i^z >= tau_{i,z}`
satisfies the hypothesis of Lemma M(c)). The difference is at most `2 V_z * V_z (2n^5)^{-1}`, with
no monitoring or fallback term at all.

**Branch 4: `i not in T(z)`.** Put `delta := V_i^z - M_i^z >= delta_i > 0` and assume
`4 s_n <= delta_i`. On `G_{-i,z}`, `tau_{i,z} >= (V_i^z - 2 s_n)_+ = V_i^z - 2 s_n >= M_i^z +
delta/2` (the positive part is inactive because `V_i^z >= delta >= 4 s_n`). On the complement of
`Bad^1_z`, Lemma M(b) and feasibility `A^z_q <= M_i^z q` give
`q (tau_{i,z} - M_i^z) <= 1 + 2 b_n(q)`, hence `q delta / 2 <= 1 + sqrt(2 q ell_n) <= sqrt q
(1 + sqrt(2 ell_n))` for `q >= 1`, hence
```
 q <= q^*(delta) := 4 (1 + sqrt(2 ell_n))^2 / delta^2 .
```
In the fallback, `barA_i <= M_i^z barQ_i` by feasibility and `barA_i >= V_i^z barQ_i - R_K(n)` as
in Branch 2, so `barQ_i <= R_K(n)/delta` and `E[U'^{fb}_{i,z}|F_fb] <= 2 barQ_i <=
2 R_K(n)/delta`. Since per-pull utility is at most 2 and the baseline utility is nonnegative,
```
 E[ (U'^{post} - U^{post})_{i,z} | D_z ] <= 2 q^*(delta) + 2 R_K(n)/delta + 2 V_z Pr(Bad^1_z|D_z)
   <= 8 (1 + sqrt(2 ell_n))^2 / delta_i^2 + 2 R_K(n)/delta_i + 2 V_z Pr(Bad^1_z|D_z).
```

**Summation.** Add the branch bounds over `z in X_F`, take expectations over `D_z` and then over
`A`, and use: `sum_z 1 = Q`; `sum_z 2 b_n(V_z) = sqrt(2 ell_n) sum_z sqrt(V_z) <= sqrt(2 ell_n)
sqrt(Q n) = sqrt(2 Q n ell_n)` by Cauchy-Schwarz and `sum_z V_z = n`; `sum_z R_K(n) = Q R_K(n)`;
`sum_z 2 V_z Pr(Bad^1_z) <= 2 n Pr(Bad^1) <= 2 n * n^{-4}` by Lemma M(a); `sum_z 2 V_z^2 (2n^5)^{-1}
<= n^{-3}`; plus `2 n^{-3}` from Branch 0 and `n^{-3}` from Branch 1. Adding `e_bid(n)` gives
```
 sup_{S'} [ u_i(n;S',S^*_{-i}) - u_i(n;S^*) ]
   <= Q L_n + Q + sqrt(2 Q n ell_n) + Q R_K(n) + e_low(n) + 6 n^{-3},
```
which is claim (A). All the conditional bounds are uniform over the deviation and over the deviator's
private randomization, so integrating over the latter changes nothing. QED for (A)

**Remark 5.4 (where the `n s_n` term would have appeared).** Following Note 1 of
`PRIVATE_BOUND_NOTES.md`, Branch 2 compares both sides at the common price `tau_{i,z}` and never
replaces `tau_{i,z}` by `V_i^z - 2 s_n`. If one did, each profile would contribute `2 s_n N_z` and
the total would acquire `2 n s_n`, which is of the same order as `L_n` and so would not change the
rate, but would be avoidable slack. The revenue and robustness parts genuinely do pay `2 n s_n`,
because there the price itself is the quantity being collected.

### 5.7 Proof of (B): second-capacity revenue

All agents play `S^*`. There is a single execution here, so put `D_z := F_{t_1(z)}`, the field of
everything realized through the last Stage-1 round at `z`, which contains `A` by Convention F-A;
Lemma M(e) and Lemma F apply conditionally on it. Fix `z` with `V_z >= K L_n`. Let
`Gbid_z := { |beta_{j,z} - M_j^z| <= s_n for all j in [K] }`, which is `D_z`-measurable and, by
Lemma B(b) applied to every agent (all of them now play `S^*`), has
`Pr(union_z Gbid_z^c) <= n^{-4}`: given `A` there are at most `n` (agent, profile) pairs whose
Stage-1 block completes, and each fails with probability at most `2 exp(-2 L_n s_n^2) = n^{-5}`. Since order
statistics are 1-Lipschitz in the supremum norm, on `Gbid_z`
```
 (M_(2)(z) - 2 s_n)_+ <= tau_z <= M_(2)(z),   and   tau_z <= (beta_{W_z,z} - s_n)_+ <= M_{W_z}^z,
```
so on `Gbid_z` the Stage-2 winner's target `min{tau_z, M^z_{W_z}}` (or its honest version) is at
least `tau_z` at every primary pull. By Lemma M(d), conditionally on `D_z`, the expected realized
reward over the primary pulls at `z` equals `E[A^z_{q_z}|D_z] >= tau_z E[q_z | D_z]`. By Lemma F
with the comparator `j in T(z)`, which delivers `M_*(z) >= M_(2)(z) >= tau_z` at every Stage-3
visit, the expected fallback reward at `z` is at least `tau_z E[H_z|D_z] - R_K(n)`. Since
`q_z + H_z = N_z`,
```
 E[ reward collected at post-bidding visits to z | D_z ] >= tau_z N_z - R_K(n)
   >= M_(2)(z) N_z - 2 s_n N_z - R_K(n)      on Gbid_z.
```
On `Gbid_z^c` bound the reward below by 0 and the loss by `V_z`. The `min{V_z, K L_n} <= K L_n`
bidding visits at `z` are charged at most one each. Summing over profiles, using
`E sum_z M_(2)(z) V_z = E sum_{t<=n} M_(2)(X_t)`, `sum_z N_z <= n` and
`E[ sum_z V_z 1{Gbid_z^c} ] <= n Pr(union_z Gbid_z^c) <= n^{-3}`,
```
 P(n;S^*) >= E sum_{t<=n} M_(2)(X_t) - ( Q K L_n + 2 n s_n + Q R_K(n) + n^{-3} ),
```
which is (B). Ties in capacity at a profile are included because `M_(2)(z)` counts multiplicity;
in particular if all `K` capacities at `z` coincide then `M_(2)(z) = M_*(z)` and the mechanism
collects the full capacity there up to the same error. QED for (B)

### 5.8 Proof of (C): honest-benchmark robustness

Now every agent may play an arbitrary strategy in `B^ctx_{j,n}`, subject to pointwise honesty for
`j in K_H`; `S` denotes the resulting profile. Fix `z` with `V_z >= K L_n` and pick
`h = h(z) in K_H` with `mu_h^z = b(z)`. Condition on `D_z := F_{t_1(z)}` as in Section 5.7.

*Bid event.* Agent `h`'s Stage-1 targets at `z` are predictable and at least `b(z)` by honesty, so
by the same exponential supermartingale argument as in Lemma M (one-sided, with `L_n` increments
of conditional range 1),
`Pr{ beta_{h,z} < b(z) - s_n } <= exp(-2 L_n s_n^2) = (2 n^5)^{-1}`. Let `G^h_z` be the complement;
given `A` there are at most `n / (K L_n) <= n` profiles with completed Stage 1, so
`Pr( union_z (G^h_z)^c ) <= (2 n^4)^{-1}`.

*Primary phase.* Two cases on `G^h_z`. If `W_z = h`, then honesty makes every primary target at
`z` at least `b(z)`, so `A^z_{q_z} >= b(z) q_z` pathwise. If `W_z != h`, then
`beta_{(2),z} >= beta_{h,z} >= b(z) - s_n` (the second order statistic with multiplicity is the
maximum over `j != W_z`, and `h != W_z`), so `tau_z >= (b(z) - 2 s_n)_+`, and on the complement of
the monitor bad event Lemma M(b) gives
`A^z_{q_z} >= q_z tau_z - 1 - 2 b_n(q_z) >= (b(z) - 2 s_n) q_z - 1 - 2 b_n(V_z)`. In both cases
Lemma M(d) converts the target sum into expected realized reward:
`E[ Z^z_{q_z} | D_z ] = E[ A^z_{q_z} | D_z ] >= (b(z) - 2 s_n) E[q_z|D_z] - 1 - 2 b_n(V_z)
 - 2 V_z Pr(Bad_z | D_z)`, where the last term covers the monitor bad event (on which we bound the
realized reward below by 0 and the right-hand side above by `V_z`; the factor 2 is slack).

*Fallback.* Whenever a switch occurs at `z`, Lemma F applies with comparator `h`, whose conditional
mean when selected is at least `b(z)` by honesty whatever its strategy: expected fallback reward at
`z` is at least `b(z) H_z - R_K(n)`.

*Summation.* Adding, and charging at most one per bidding visit,
```
 P(n;S) >= E sum_{t<=n} b(X_t) - ( Q K L_n + 2 n s_n + Q + sqrt(2 Q n ell_n) + Q R_K(n) + 2 n^{-3} ),
```
where the `2 n^{-3}` collects `n Pr(union_z (G^h_z)^c) <= (2n^3)^{-1}` and
`2 n Pr(Bad) <= 2 n^{-3}`. This is (C), and it is uniform over the joint feasible behavioral
profile: the argument never assumed that any agent other than `h` does anything in particular, and
`h` itself is only required to be honest. QED for (C)

### 5.9 Proof of (D)

`L_n <= n^{2/3}(log(en))^{1/3} + 1`. `s_n = sqrt(ell_n/(2L_n))` with `ell_n = log 2 + 5 log n`, so
`n s_n <= n sqrt( (log 2 + 5 log n) / (2 n^{2/3} (log(en))^{1/3}) ) = sqrt(5/2) \, n^{2/3}
(log n)^{1/3} (1+o(1))`, provided the cap `floor(n/(2K))` in `L_n` is inactive, which holds as soon
as `n >= 8 K^3 log(en)`; the finitely many smaller horizons are absorbed into the instance
constant. `sqrt(2 Q n ell_n) = O(sqrt(Q n log n))` and `R_K(n) = O(sqrt(K n log K))` are both
`O(sqrt(n log n))` for fixed `K, Q` and hence of strictly smaller order than `n^{2/3}(log n)^{1/3}`.
`e_low(n) = O(Q log n / delta_i^2 + Q sqrt(n log n)/delta_i)` is also of smaller order for a fixed
instance. Hence all three error terms are `O_{K,Q,inst}(n^{2/3}(log n)^{1/3}) = o(n)`. QED for (D)


## 6. The bidding term is attained (tightness of `Q L_n`)

**Proposition 6.1.** *Assume (H1) to (H6). Fix `i` and let `U_i := { z in X_F : T(z) = {i} }` be the
set of profiles at which `i` is the unique top agent; assume `mu_i^z < M_i^z` for every `z in U_i`
if `i` is honest. Put `m'(z) := (M_i^z + V_i^z)/2` if `i` is strategic and
`m'(z) := max{ (M_i^z + V_i^z)/2, mu_i^z }` if `i` is honest, and let `S'_{i,n}` deliver `m'(z)` at
every Stage-1 pull at every `z in U_i` and follow `S^*_i` at every other profile and in every
other phase. Let `l_z` be the number of Stage-1 pulls agent `i` receives at `z`, a deterministic
function of `V_z` (equal to `L_n` whenever `V_z >= K L_n`). Then for every `n` with
`4 s_n < min_{z in U_i} (M_i^z - V_i^z)`,*
```
 u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n) >= sum_{z in U_i} (M_i^z - m'(z)) E[ l_z ] - 4 n^{-3}.
```
*In particular, if `V_z >= K L_n` almost surely for every `z in U_i` (for instance, i.i.d. arrivals
with positive masses and `n` large), the gain is at least `L_n sum_{z in U_i} (M_i^z - m'(z))`,
so the `Q L_n` term of (A), and with it the order `n^{2/3} (log n)^{1/3}` and the linear growth in
the number of profiles, is attained by PL-MESP as specified, up to instance factors.*

*Proof.* Couple the two executions as in Section 5.5 (same `A`, seeds, priorities, fallback coins,
private coins). All Stage-1 targets in both executions are deterministic constants, so by Hoeffding
each completed (agent, profile) Stage-1 block deviates from its target mean by more than `s_n` with
probability at most `2 exp(-2 L_n s_n^2) = n^{-5}`; given `A` there are at most `n` such blocks in
each execution, so the event `E` that all of them concentrate in both executions has
`Pr(E^c) <= 2 n^{-4}`.

On `E`, consider `z in U_i` with a completed Stage 1. In execution 2,
`beta_{i,z} >= M_i^z - s_n > V_i^z + s_n >= max_{j != i} beta_{j,z}`; in execution 1,
`beta'_{i,z} >= m'(z) - s_n >= (M_i^z + V_i^z)/2 - s_n > V_i^z + s_n >= max_{j != i} beta_{j,z}`,
both because `4 s_n < M_i^z - V_i^z`. So `i` wins at `z` in both executions, and by Lemma B(b) the
price `tau_z = (max_{j != i} beta_{j,z} - s_n)_+` is the same random variable in both. At
`z not in U_i` the Stage-1 targets agree in the two executions, so the bids, winner, and price
agree. By Lemma L the mechanism's state at `z` is a function of `z`'s own data, and `S^*_i` is
itself profile-local and depends only on the local phase and price, so after Stage 1 the two
executions coincide pathwise at every profile: identical selections, identical targets, identical
seeds, identical rewards. Hence on `E` the two utilities differ exactly by the Stage-1 effort
saving `sum_{z in U_i} l_z (M_i^z - m'(z))`. Off `E` they differ by at most `2n`, contributing at
most `2n * 2 n^{-4} = 4 n^{-3}`. Feasibility and honesty of `m'` are immediate. QED

**Remark 6.2.** Proposition 6.1 also shows that the `Q` in `e_bid` is not an artifact: a deviator
that is uniquely top at many profiles collects the bidding saving once per profile. It does not
show that the `Q K L_n` of the revenue bound is attained, and it says nothing about whether a
cleverer mechanism could avoid paying `L_n` per profile (for example by sharing bidding effort
across profiles, which no hypothesis here permits since the primitives at different profiles are
unrelated).


## 7. Attacks I checked against

Each of the following was a candidate hole; the resolution is given with the place in the proof
that carries it.

1. *Trigger a local switch deliberately and farm the fallback.* Covered by Branch 2: the fallback
   bound `(1 + mu_i^z - V_i^z) H + R_K(n)` matches the baseline rate `(1 + mu_i^z - tau_{i,z}) H`
   whenever `tau_{i,z} <= V_i^z`, which is exactly what `G_{-i,z}` gives.
2. *Deliver zero in the fallback to be selected often.* Impossible: Lemma F forces
   `barA_i >= V_i^z barQ_i - R_K(n)`, so an agent delivering `0` has `barQ_i <= R_K(n)/V_i^z`.
   The utility bound `2 barQ_i` is then `O(sqrt(n log n))`.
3. *Shade at profile `z'` to lower the price at `z`.* Impossible by Lemma L: `tau_z` is a function
   of the Stage-1 rewards delivered at `z` only, and by Lemma B(b) the other agents' Stage-1
   rewards at `z` are unchanged by anything the deviator does.
4. *Use information gathered at `z'` to ride the monitoring boundary at `z` more efficiently.*
   Covered: Lemma M conditions on `F_s^-`, which contains the deviator's entire observed history at
   all profiles, and the boundary crossing probability does not depend on how the target was
   chosen. The total slack a deviator can extract from boundaries is
   `sum_z (1 + 2 b_n(V_z)) <= Q + sqrt(2 Q n ell_n)`, maximized by spreading visits evenly across
   profiles, which is what the Cauchy-Schwarz step accounts for.
5. *Split a deviation across profiles so that no single profile looks anomalous.* Covered by (5.4):
   the accounting is additive in expectation and every per-profile bound is uniform over the
   deviator's behavior everywhere else.
6. *A profile that never completes Stage 1.* It has `N_z = 0` and contributes only its Stage-1
   term, at most `L_n` to the deviation gain and at most `K L_n` to the revenue and robustness
   losses.
7. *A profile visited zero times.* Contributes nothing; it is never instantiated. This is why
   knowing `X_F` or `Q` is unnecessary and why the union bounds count `sum_z V_z = n` rather than
   `Q n`.
8. *An honest deviator at a profile where the price falls below its intrinsic mean.* Branch 3,
   which uses no monitoring and no fallback estimate.
9. *Capacity ties inside a profile, including `K = 2` and including all `K` capacities equal.*
   Branch 2 only needs `tau_{i,z} <= V_i^z <= M_i^z`, which is the definition of `i in T(z)`, and
   the fallback comparator only needs some `j != i` with `M_j^z = V_i^z`, which exists for
   `K >= 2`. No two-top condition is used anywhere.
10. *Arrivals chosen adversarially.* Permitted by (H3) as long as they are chosen without access to
    the seeds and coins; every bound above is proved conditionally on `A` and is uniform in `A`.
    An arrival process that reacts to realized rewards is *not* permitted, and Lemma B(a) is
    exactly where it would fail: the coupled executions would then visit profiles at different
    rounds and the pathwise bid domination would be lost.
11. *Seed relabeling across executions.* Avoided; see Lemma B(a) and Remark 5.3.
12. *The mechanism telling agents the phase.* All bounds are uniform over `B^ctx_{i,n}`, which
    already lets the deviator condition on everything it observes, so enlarging the message set
    cannot increase the supremum in (A). Without the phase message `S^*` would not be
    implementable, since a selected agent cannot otherwise tell a primary pull from a fallback pull.


## 8. Differences from Section 4 of the candidate ledger, and which I believe is right

I read `audit/round2/B/MATH_CANDIDATE_LEDGER.md` Section 4 only after Sections 1 to 7 above were
written to this file. The overall architecture agrees, which I take as mild independent
corroboration of the architecture and of nothing else: independent per-profile MESP instances, all
parameters from the global horizon, conditioning on the arrival sequence, no i.i.d. requirement,
the second-capacity benchmark `E sum_t M_(2)(X_t)`, the `Q L` bidding term with the same
`Q = o(n^{1/3} (log n)^{-1/3})` regime, and announcing the local phase to the selected agent. The
substantive differences follow.

**D1. The fallback tuning (the main design difference).** The ledger restarts the local fallback in
doubling epochs of planned local lengths `2^0, 2^1, ...`, with `gamma_k` tuned to `2^k`, and pays
`R^dbl_K(H) = C_0 (sqrt(K H log K) + K log K log_2(2H))` with `C_0` left for the provers. I run a
single local EXP3 tuned to the **global** `n` and prove a prefix version of the selected-reactive
lemma (Lemma F), paying `R_K(n) = 3 sqrt(K n log K) + 2 K log K` per profile.
*Which is right:* both are correct, and I believe mine is the better one to put in the paper, for
three reasons: it needs one lemma rather than a lemma plus an epoch sum, it inherits the
manuscript's existing constant instead of introducing an unfixed `C_0`, and it removes a
mechanism-level complication (epoch boundaries) from an already dense algorithm description. The
ledger's version is strictly tighter in a lower-order term: summed over profiles it gives
`O(sqrt(Q K n log K) + Q K log K log n)` against my `Q R_K(n) = O(Q sqrt(K n log K))`, better by a
factor `sqrt(Q)`. Since both are `O(sqrt(n log n))` for fixed `Q` and the dominant term is
`Q K L_n = Theta(Q n^{2/3} (log n)^{1/3})`, the difference never affects a stated rate. If one
wants the sharper form, Lemma F applied per epoch gives it: with `sum_{k <= log_2(2H)} 3 sqrt(K
2^k log K) <= 3 sqrt(2)/(sqrt 2 - 1) sqrt(K H log K) <= 10.25 sqrt(K H log K)` and `2 K log K` per
epoch, one may take `C_0 = 11`, which is the value the ledger conjectures. I did not need it and
did not verify the epoch bookkeeping in detail.

**D2. Seed indexing in the bid-domination coupling.** The ledger's step 2 says "index reward
uniforms by (profile, agent, local pull index)". That is precisely the construction the contract
flags at ambiguity 1 as not automatic. It is in fact legitimate here, but only because of the
ledger's own step 1: conditional on the arrival path, the Stage-1 schedule at a profile is
deterministic, so the (profile, agent, local pull index) triple is a fixed round and the relabeling
is a bijection that does not depend on the execution. My Lemma B(a) makes that observation and then
does not need the relabeling at all: seeds stay attached to rounds.
*Which is right:* both give the same conclusion; mine removes a step that an adversary would
reasonably attack, so I would write it my way and would regard the ledger's phrasing as needing the
one added sentence.

**D3. Calibration of the confidence radius and boundary, and knowledge of `Q`.** The ledger keeps
the scalar `s = sqrt(log(2 K n^4)/(2L))` and `b(r) = sqrt(r log(2 n^4)/2)` and pays bad events
`Q (n^{-4} + n^{-3})`, each costing `2n`, i.e. `O(Q n^{-2})`. I use `ell_n = log(2 n^5)` in both,
and count the union bound conditional on the arrival path over the `sum_z V_z = n` (profile, local
index) pairs that can occur, which gives a total failure probability `n^{-4}` and a total bad-event
cost `O(n^{-3})`, with parameters that contain neither `Q` nor `K`.
*Which is right:* both are valid for fixed `Q`; I believe mine is better because the mechanism then
needs no bound on `Q` at all (H6), which matters for the claim that the platform does not know the
arrival law, and because the bad-event budget does not degrade as `Q` grows toward the
`n^{1/3}` ceiling. The cost is a constant factor `sqrt(5/4)` on the `n s_n` term.

**D4. The monitor martingale.** The ledger's step 3 asserts that `lem:private-monitor` "holds for
targets predictable with respect to the GLOBAL filtration" and lists writing this out with the
global filtration explicit as a delicate point for the provers. Lemma M above is my way of doing
it: a global-time martingale with a predictable indicator for "this round is a primary pull at
`z`", an exponential supermartingale stopped at the round of the `r`-th such pull, and the union
bound taken conditional on the arrival path. I think the explicit time change matters: the naive
alternative, a filtration indexed by the local pull count, has to be checked for nestedness in the
presence of a deviator that acts at other profiles between two consecutive local pulls, and the
increment is not conditionally centered with a *predictable* range unless one conditions on the
chosen target, which is what (5.1) plus the tower step does.

**D5. Optional stopping in the revenue proof.** The manuscript's scalar revenue proof says "`q` is
a bounded stopping time for the primary filtration". In the contextual setting the local primary
phase can end for a second reason, namely that the profile stops arriving, which is not a stopping
time of any filtration generated by the local rewards. The ledger does not mention this. My Lemma
M(d) avoids the issue: `E[Z^z_{q_z} - A^z_{q_z}] = 0` is the identity `E[M^z_n] = 0` for a
martingale over global time, with no stopping argument. (Conditioning on the arrival path also
repairs the manuscript's phrasing, since then the horizon cut is deterministic; but the identity is
cleaner.)

**D6. Explicit finite-`n` statement versus `O(.)`.** The ledger's target statement is in `O(.)`
form. I state (A), (B), (C) with explicit error terms and explicit hypotheses (H1) to (H7) and an
explicit finite-`n` threshold `4 s_n <= delta_i` for the non-top branch. I believe the explicit
form is required by the brief and is what an adversary should be handed.

**D7. Scope remarks the ledger does not make.** I add Corollary 4.3 (the theorem holds verbatim for
a known finite partition on which all primitives are constant, which is the precise boundary of the
argument) and Remark 4.1 (with a known `Qbar` the bidding length can be retuned to
`(n/(Qbar K))^{2/3}(log n)^{1/3}`, improving the error to `O((Qbar K)^{1/3} n^{2/3} (log n)^{1/3})`).
I did not verify the ledger's continuous-extension obstruction paragraph and make no claim about it;
my Corollary 4.3 deliberately stops where the primitives stop being constant, and I state there why.

**D8. What the ledger got right that I would not have flagged on my own.** Its delicate point (a),
that conditioning on arrivals is legitimate because the deviation class only grows, is exactly
right and I had left it implicit; I have since made it explicit in Convention F-A. Its observation
that the `Q L` term forces `Q = o(n^{1/3}(log n)^{-1/3})` is the same regime I derive in Remark 4.1.


## 9. What I did not establish, and the step I consider least secure

I do not claim this result is correct. What I claim is: I wrote a mechanism, a statement with
explicit hypotheses, and a proof of each of (A), (B), (C) from four lemmas that I proved here, and
I checked the attacks listed in Section 7. What follows is what is missing.

**Not established.**

1. *Continuous contexts.* Nothing here extends to a grid over a continuous space. Corollary 4.3
   marks the exact boundary: the proof needs each agent's feasible target set to be a fixed interval
   `[0, M_i^z]` at every round of the local instance. On a cell over which `M_i(.)` varies, the bid
   estimates a cell-average delivered mean, the price may exceed an agent's capacity at some
   contexts inside the cell while being below it at others, and Lemma B loses its fixed comparison
   target. I make no claim about the ledger's proposed continuous rate.
2. *Optimality of the mechanism.* Proposition 6.1 shows the `L_n` per profile is attained *by
   PL-MESP as specified*. It is not a lower bound for all mechanisms, and in particular I have not
   ruled out a mechanism that shares bidding effort across profiles under some assumption linking
   the primitives across profiles (there is no such assumption in (H1)).
3. *The claimed `Omega` in the deviation gain beyond Stage 1.* I did not prove that the monitoring
   slack `2 b_n(V_z)` is attainable; like `PRIVATE_BOUND_NOTES.md` Note 2, I regard the Stage-2
   boundary-tracking gain as plausible and unproved, and it must not be stated as a theorem.
4. *Uniformity across instances.* (A) is uniform over deviations for a fixed instance only. As the
   gaps `delta_i` shrink the non-top threshold `4 s_n <= delta_i` recedes, exactly as in the scalar
   theorem; `PRIVATE_BOUND_NOTES.md` Note 3 records that for gaps of order `10^{-2}` this threshold
   is beyond simulable horizons, and the same is true here.
5. *Arrival processes that react to rewards.* Excluded by (H3). Section 7 item 10 identifies Lemma
   B(a) as the first casualty. I did not look for a counterexample, so I do not know whether the
   theorem is false in that case or merely unproved.
6. *Anytime guarantees.* Everything is fixed-horizon; the mechanism uses `n` in `L_n`, `s_n`,
   `b_n`, and `gamma_n`.
7. *Agents observing only their own context.* (H5) gives the selected agent the full profile, as in
   the manuscript's default. The proof does not use this either way, since all bounds are uniform
   over the larger class, but I did not state a separate own-context-only version.
8. *No numerical verification of the asymptotics.* Section 10 records a finite-`n` simulation; at
   simulable horizons `Q K L_n` is a large fraction of `n`, so the simulation tests the inequalities
   and the qualitative claims, not the rates.

**Least secure step.** Lemma M, specifically the passage from (5.1) to (5.2) and the stopped
exponential supermartingale, in combination with the fact that the predictable indicator `psi^z_s`
is `F_{s-1}`-measurable *only because Convention F-A puts the whole arrival path in `F_0`*. If one
insisted on the natural filtration in which `X_s` is revealed at round `s`, then `psi^z_s` would be
`F_{s-1} or sigma(X_s)`-measurable but not `F_{s-1}`-measurable, and the line
`E[exp(lambda (M^z_s - M^z_{s-1})) | F_{s-1}] <= exp(lambda^2 psi^z_s / 8)` would be false as
stated (the right-hand side would not be `F_{s-1}`-measurable). The repair is exactly Convention
F-A, which is legitimate under (H3), and this is the single place where exogeneity of the arrivals
is doing indispensable work in the monitoring argument. An adversary should attack there first, and
second at Lemma B(a), which is the other place exogeneity is indispensable.

A secondary worry: the per-profile conditioning field `D_z` in Section 5.6 is the *joint* past of
the two coupled executions through the last Stage-1 round at `z`. I give the justification in the
paragraph "Legitimacy of conditioning on the joint field" of Section 5.6, and I believe it is
right, but it is the one place where the two-execution coupling and the martingale arguments
interact and it deserves a second reader.


## 10. Numerical falsification attempt against my own claims

This is a fully synthetic simulation of PL-MESP exactly as specified in Section 2, run to look for a
violated inequality. It is not evidence that the theorem is true. Code, seeds, and raw outputs:
`<scratchpad>/round2/prover2-c2/plmesp.py` and `logs/`; submissions logged in `COMPUTE_LOG.md`.

Setup. `K = 3`, `Q = 2`, agent 2 honest, agent 0 the deviator. Instance A:
`M(z_0) = (0.90, 0.60, 0.50)`, `M(z_1) = (0.50, 0.80, 0.80)`, `mu(z_0) = (0.1,0.1,0.1)`,
`mu(z_1) = (0.2,0.1,0.1)` (agent 0 uniquely top at `z_0`, non-top at `z_1` with `delta = 0.3`).
Instance B: `M(z_1) = (0.80, 0.80, 0.50)` instead, so agent 0 is top at both profiles and
`e_low = 0`, which is the only setting in which bound (A) is not vacuous at simulable horizons.
Arrivals: i.i.d. uniform on `{z_0, z_1}`, and separately the deterministic alternating sequence
`z_0, z_1, z_0, ...`, which is not i.i.d. and tests (H3). 30 repetitions, common random numbers
across deviations.

Deviations tested for agent 0, all in `B^ctx_{0,n}`: Stage-1 underbidding to `(M_i + V_i)/2`;
greedy bait and switch (deliver 0 whenever surviving the next pull with reward 0 is still
possible); immediate crash then match the runner up; immediate crash then deliver 0 forever;
cross-profile adaptive (crash at the first profile, then free ride at every profile once any
switch has occurred anywhere); boundary riders that hold the cumulative delivery at
`r tau - alpha b_n(r)` for `alpha in {0.25, 0.5, 1.0}`; and the combination of underbidding with
the `alpha = 0.5` rider.

Findings.

1. *No inequality was violated.* In instance B, bound (A) is `10420` at `n = 40000` and `24454` at
   `n = 160000`; the largest gain found was `805` and `1843` respectively (underbidding plus the
   `alpha = 0.5` rider). At `n = 640000` the bound is `57990` and the largest gain found was `2708`.
2. *Proposition 6.1 is confirmed to the digit.* The pure underbidding gain equals
   `L_n (M_i - m') = 0.15 L_n` exactly in every run (`397.20` at `L_n = 2648`, `642.75` at
   `L_n = 4285`, `1039.05` at `L_n = 6927`, `2708.4` at `L_n = 18056`), with zero variance across
   seeds, which is what the pathwise-identical-post-Stage-1 argument predicts.
3. *The `L_n` and `b_n` channels are separate and additive.* The combined deviation gained exactly
   the sum of the two individual gains (`1039.0 + 803.8 = 1842.8`). Underbidding scales as
   `n^{2/3}(log n)^{1/3}` (observed ratios `2.62` and `2.61` over horizon quadruplings, predicted
   `2.60`) and the rider as `sqrt(n)` (observed `2.19`, `2.01`, predicted `2`). This is the
   expected shape of `e_bid + e_mon` and is consistent with Note 2 of `PRIVATE_BOUND_NOTES.md`:
   the boundary-tracking gain is real but of lower order, and I still do not claim it as a theorem.
4. *Aggressive riding backfires.* The `alpha = 1` rider, which sits on the boundary, triggers
   switches and loses `25000` to `105000` of utility. Every crash and bait-and-switch deviation
   loses heavily and, as the accounting predicts, *raises* platform revenue, because the fallback
   restores capacity delivery by the other agents.
5. *No false switch was ever observed under `S^*`* (0 in all runs, across all horizons and both
   arrival processes), consistent with the `(2 n^4)^{-1}` bound of Lemma M(c).
6. *Non-i.i.d. arrivals change nothing measurable.* The deterministic alternating arrival sequence
   reproduces the i.i.d. numbers to within noise (for example, `underbid` gain `397.20` in both,
   base utility `9621.0` versus `9647.4`), which is what (H3) predicts and what the manuscript's
   grid results could not claim.
7. *Both benchmarks are approached from below at the predicted rate.* The revenue deficit against
   `E sum_t M_(2)(X_t)` was `6.9%`, `5.4%`, `3.9%` of `n` at `n = 40000, 160000, 640000`, and the
   honest-benchmark deficit under the all-adversarial profile (both strategic agents delivering 0
   everywhere, the honest agent delivering `mu`) was `2.6%`, `1.7%`, `1.1%`. Both bounds (B) and (C)
   are numerically vacuous at these horizons, since `Q K L_n` alone is `16%` to `42%` of `n`; the
   simulation therefore tests the direction and the trend, not the constants.

What this does not test: the non-top branch (Branch 4) is essentially unreachable at these
horizons, because a non-top agent with `delta = 0.3` wins a local auction only on a bid deviation
of order `delta`, of probability roughly `exp(-2 L_n delta^2)`; and the asymptotic regime where
`Q K L_n / n` is small needs horizons far beyond what is simulable, exactly as
`PRIVATE_BOUND_NOTES.md` Note 3 records for the scalar theorem.
