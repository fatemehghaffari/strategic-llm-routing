# Candidate C2, Local-MESP: finite-context private incentives. Prover 1 write-up

Author role: Prover 1, round-2 two-prover pipeline, 18 September 2026. Written in isolation.
Status of this document: it states exactly what I prove and exactly what I assume. It does not
claim that the result is correct; it claims that the argument below is complete as written and
invites an adversary to find the step that is not.

Conventions. `log` is natural, `log_2` is base two, `(x)_+ = max(x,0)`, `[K] = {1,...,K}`,
`1{.}` is an indicator. No Unicode em dashes and no triple hyphens appear anywhere.
All references of the form `lem:...`, `thm:...`, `eq:...` are to the canonical manuscript
(`sections/appendix_private.tex`, `sections/Private_information_setting.tex`,
`sections/setting.tex`, `sections/contextual.tex`, `sections/appendix_contextual.tex`).
The contract is `audit/round2/B/CONTEXT_PROOF_CONTRACT.md`, the ledger is
`audit/round2/B/MATH_CANDIDATE_LEDGER.md` Section 4, the tightened top-agent bound is
`audit/round2/B/PRIVATE_BOUND_NOTES.md` Note 1.

============================================================================================
## 0. Summary of what is proved

I prove a finite-context localisation of `thm:private-mesp`. The mechanism is Local-MESP as
specified in the ledger, with four places where I fix a detail the ledger leaves open
(Section 2, items M3, M5, M6, M7); those choices are hypotheses of the theorem, not
improvements smuggled in.

Proved here, in full, with all six delicate points settled:

* Theorem 1(i), additive behavioural equilibrium against a deviation class that is strictly
  larger than the ledger's `B^ctx_{i,n}`: the deviator may condition on the entire arrival
  sequence, including future arrivals, as well as on its own entire cross-profile history.
* Theorem 1(ii), revenue at `S^*` against the benchmark `E sum_t M_(2)(X_t)`.
* Theorem 1(iii), honest-benchmark robustness against every feasible behavioural profile
  (all K agents deviating, cross-profile adaptively, with knowledge of all arrivals).
* Proposition 2, a lower bound showing that the leading `Q L` term is attained, so the
  restriction `Q = o(n^{1/3} (log n)^{-1/3})` is not an artefact of the analysis.

The absolute constant of the doubling EXP3 sum is pinned: `C_0 = 11` works, and the exact
geometric constant is `3 sqrt(2)/(sqrt(2)-1) = 10.2427`.

What I do NOT prove is listed in Section 12, and the steps I consider least secure are in
Section 13.

============================================================================================
## 1. Model, classes, notation

### 1.1 Primitives

Fix `K >= 2` agents and a horizon `n` known to the platform. A finite set of full profiles
`X_F = {z_1, ..., z_Q}` is fixed; `Q` is finite. Write `z = (z_1, ..., z_K)` for a profile,
`z_i` for agent `i`'s coordinate. Agent `i` has an intrinsic mean `mu_i(z_i) in [0,1]` and a
capacity `M_i(z_i) in [mu_i(z_i), 1]`. A nonempty honest set `K_H` is fixed; an honest agent
never targets below its intrinsic mean at the current profile, after every history.

Per profile `z` put

    M_*(z) := max_j M_j(z_j),        T(z) := {j : M_j(z_j) = M_*(z)},
    M_(2)(z) := second largest of (M_1(z_1), ..., M_K(z_K)) counting ties,
    V_i(z) := max_{j != i} M_j(z_j), delta_i(z) := V_i(z) - M_i(z_i),
    b(z) := max_{h in K_H} mu_h(z_h).

Note `i in T(z)` iff `delta_i(z) <= 0`, and `M_(2)(z) = V_i(z)` for any `i in T(z)`.

Round `t <= n`: a profile `X_t in X_F` arrives and is observed by the platform and by the
selected agent; the platform selects `I_t`; agent `I_t` chooses a target
`m_{I_t,t} in [0, M_{I_t}(X_{t,I_t})]`; the platform observes `Y_t ~ Bernoulli(m_{I_t,t})`.
Effort cost `c_{i,t} = m_{i,t} - mu_i(X_{t,i})`. Utilities

    u_i(n;S) = E_S[ sum_{t<=n} 1{I_t=i} (1 + mu_i(X_{t,i}) - m_{i,t}) ],
    P(n;S)   = E_S[ sum_{t<=n} Y_t ] = E_S[ sum_{t<=n} m_{I_t,t} ].

The second identity for `P` is the tower property applied for each fixed `t <= n`; `n` is
deterministic, so no optional stopping is involved. Per selection the agent's utility
`1 + mu_i - m` lies in `[0,2]`.

### 1.2 Arrivals

(A1) Exogenous arrivals. The arrival process `X = (X_1, ..., X_n)`, taking values in `X_F^n`,
is independent of every reward seed, every mechanism priority, every mechanism randomisation
coin and every agent's private coin. It need NOT be i.i.d., need not be stationary, and its
law need not be known to the platform. It may even be deterministic.

Write `V_z := #{t <= n : X_t = z}` for the visit count of profile `z`, so `sum_z V_z = n`.

### 1.3 Reward seeds

(A2) Seed construction. There is an array of independent Uniform`[0,1]` variables
`U = { U_{z,j,k} : z in X_F, j in [K], k >= 1 }`, independent of `X`, of all priorities, of
all mechanism coins and of all private coins. If agent `j` is selected at a visit to `z` and
this is its `k`-th selection at `z` (its local pull index at `z`), the realized reward is

    Y = 1{ U_{z,j,k} <= m }                                                   (SEED)

where `m` is the target the agent chooses at that round. Each triple `(z,j,k)` is consumed at
most once, so the seed used at any round is independent of everything that happened strictly
earlier. This is the formal content of the manuscript's hypothesis "targets are chosen before
fresh conditionally independent Bernoulli seeds" (`thm:private-mesp`), specialised to the
seed indexing fixed in the contract Section 1 (own local pull index).

### 1.4 The deviation classes

`B^ctx_{i,n}` (contract Section 5, the ledger's class). After selection at round `t`, agent
`i` chooses `m_{i,t} in [0, M_i(X_{t,i})]` as a measurable function of `n`, the current
profile `X_t`, its own entire history across all profiles (its selection rounds, the profiles
at those rounds, its targets, its rewards, all mechanism messages it received) and independent
private randomness. If `i` is honest, `m_{i,t} >= mu_i(X_{t,i})` after every history.

`B^ctx+_{i,n}` (the class I actually use). The same, except that the agent may in addition
condition on the ENTIRE arrival sequence `(X_1, ..., X_n)`, hence on all future arrivals, on
all visit counts `V_z`, and on the exact global round index. Honesty is unchanged.

Clearly `B^ctx_{i,n} subseteq B^ctx+_{i,n}`, so every bound proved for the larger class holds
for the ledger's class. Delicate point (a) is settled by this inclusion; see Section 10(a).

A feasible behavioural profile for part (iii) is a tuple `(S_1, ..., S_K)` with
`S_j in B^ctx+_{j,n}` for every `j`, honest agents honest.

============================================================================================
## 2. The mechanism Local-MESP

Parameters, all computed from the GLOBAL horizon `n` only:

    L    := ceil( n^{2/3} (log(en))^{1/3} ),
    ell  := log(2 n^4),                  b(r) := sqrt( r ell / 2 ),   b(0) := 0,
    s    := sqrt( log(2 K n^4) / (2 L) ).

(Overloading: `b(z)` with a profile argument is the best honest intrinsic mean, `b(r)` with an
integer argument is the monitoring boundary. The argument type always disambiguates.)

The platform runs one independent local instance per profile, lazily created the first time a
profile is seen. It does not need to know `Q`, `X_F` or the arrival law. At a round with
`X_t = z` the platform advances the local instance of `z` by one local step.

* (M1) Local Stage 1 (bidding). The first `K L` visits to `z` are bidding pulls. Agent
  `sigma_z(1)` is pulled on local visits `1, ..., L`, agent `sigma_z(2)` on local visits
  `L+1, ..., 2L`, and so on, where `sigma_z` is a FIXED permutation of `[K]` that does not
  depend on any reward, on any bid, or on anything the agents do. (M1 fixes ledger item M3.)
  Agent `j`'s empirical bid is `beta_j(z) := L^{-1} sum_{k<=L} Y_{j,k}(z)`, the average of its
  `L` bidding rewards at `z`.
* (M2) Local award. If and when the `K L`-th visit to `z` occurs, the local winner `W_z` is a
  largest bidder, ties broken by an independent uniform priority permutation `pi_z` of `[K]`
  drawn once per profile before play. The local price
  `tau_z := ( beta_(2)(z) - s )_+` is announced to the selected agent at every later visit to
  `z`, where `beta_(2)(z)` is the second order statistic with multiplicity of
  `(beta_1(z), ..., beta_K(z))`.
* (M3) Local Stage 2 (primary). Every later visit to `z` pulls `W_z`. Writing `Z_r` for the
  sum of `W_z`'s rewards on its first `r` local primary pulls, the local instance switches to
  Stage 3 at the first `r` with `Z_r < r tau_z - b(r)`.
* (M4) Local Stage 3 (fallback). From the switch on, every visit to `z` is allocated by a
  fresh explicit-exploration EXP3 over all `K` agents, restarted in doubling epochs. Let the
  local fallback clock be `1, 2, 3, ...`. Epoch `k >= 0` covers clock times
  `2^k, ..., 2^{k+1}-1`, so its planned length is `2^k`; the last entered epoch is truncated
  when the profile receives no further visits. Epoch `k` uses fresh weights `w_{j,1} = 1`,
  `gamma_k := min{1/2, sqrt(K log K / 2^k)}`, `eta_k := gamma_k / K`,
  `q_{j,t} := w_{j,t}/sum_l w_{l,t}`, `p_{j,t} := (1-gamma_k) q_{j,t} + gamma_k/K`,
  `I_t ~ p_t` drawn with a fresh coin, `hat Y_{j,t} := Y_t 1{I_t=j}/p_{j,t}`,
  `w_{j,t+1} := w_{j,t} exp(eta_k hat Y_{j,t})`. No knowledge of the remaining local horizon
  is used. (M4 fixes ledger item M5: the epoch schedule is by planned length, not by realized
  length, and epoch parameters are tuned to the planned length.)
* (M5) If a profile receives fewer than `K L` visits, all of its visits are bidding pulls and
  it never awards, never prices and never monitors. (This is ledger delicate point (f).)
* (M6) Messages. The selected agent is told the current profile `z` (it observes `X_t`
  anyway), the local phase at `z` (bidding, primary, fallback), and `tau_z` when the phase is
  primary or later. Nothing else.
* (M7) All priorities `{pi_z}`, all EXP3 coins and all agents' private coins are mutually
  independent and independent of `U` and of `X`.

Proposed profile `S^*`. At a bidding pull at `z`, and at any fallback pull at `z`, agent `j`
delivers `M_j(z_j)`. At a primary pull at `z` a strategic winner delivers `min{tau_z, M_j(z_j)}`
and an honest winner delivers `max{ mu_j(z_j), min{tau_z, M_j(z_j)} }`. This is feasible at
every history and is implementable given the messages of (M6), so `S^*_j in B^ctx_{j,n}` for
every `j`, and honest agents' components are honest.

Call `S^*` LOCAL-MARKOV: the target agent `j` delivers at a visit to `z` is a deterministic
function of `(z, local phase at z, tau_z, j)` only. This is the property used in Lemma 3 below.

============================================================================================
## 3. The theorem

Define, for `H >= 1`,

    R_K(H)      := 3 sqrt(K H log K) + 2 K log K,        R_K(0) := 0,
    R^dbl_K(H)  := 11 ( sqrt(K H log K) + K log K log_2(2H) ),  R^dbl_K(0) := 0.

For a profile `z` write `n_z := (V_z - K L)_+` for its number of post-bidding visits and
`l_i(z)` for the number of Stage-1 pulls agent `i` receives at `z`, namely
`l_i(z) = min{ L, ( V_z - (sigma_z^{-1}(i) - 1) L )_+ }`; note `sum_z l_i(z) <= min{QL, n}`
and that `l_i(z)` is a deterministic function of `V_z`.

**Theorem 1 (Local-MESP on finite profiles).** Assume (A1), (A2), (M1) to (M7), `K >= 2`,
`n >= 2`, a finite `X_F` with `|X_F| = Q`, and a nonempty honest set. Then:

(i) (Additive behavioural equilibrium.) For every agent `i`, every
`S'_{i,n} in B^ctx+_{i,n}`,

    u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)
      <= E[ sum_z l_i(z) ]
         + sum_{z : i in T(z)} E[ 1 + 2 b(n_z) + R^dbl_K(n_z) ]
         + sum_{z : i notin T(z)} E[ D_i(z) ]
         + 8 n^{-2},

where for a profile `z` at which `i` is not top,

    D_i(z) := 8 (1 + sqrt(2 ell))^2 / delta_i(z)^2 + 2 R^dbl_K(n_z) / delta_i(z)
              if 4 s <= delta_i(z),
    D_i(z) := 2 n_z                                    otherwise.

Consequently, for every `n` with `4 s <= min{ delta_i(z) : z in X_F, i notin T(z) }`
(an inequality that holds for all `n` beyond an instance-dependent threshold, since `s -> 0`),

    sup_{S'_{i,n} in B^ctx+_{i,n}} [ u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n) ]
      <= min{Q L, n} + Q + sqrt( 2 ell Q n ) + 11 sqrt( K Q n log K )
         + 11 Q K log K log_2(2n)
         + sum_{z : i notin T(z)} [ 8 (1 + sqrt(2 ell))^2 / delta_i(z)^2
                                    + 2 R^dbl_K(n) / delta_i(z) ]
         + 8 n^{-2}
      = O( Q n^{2/3} (log n)^{1/3} + sqrt( Q n log n ) + sqrt( K Q n log K )
           + Q K log K log n ) + O_inst(1) ,

which is `o(n)` for fixed `K`, fixed instance and `Q = o( n^{1/3} (log n)^{-1/3} )`.

(ii) (Revenue.)

    P(n; S^*) >= E sum_{t<=n} M_(2)(X_t)
                 - [ min{Q K L, n} + 2 s n + 11 sqrt(K Q n log K)
                     + 11 Q K log K log_2(2n) + n^{-3} ]
              = E sum_{t<=n} M_(2)(X_t)
                 - O( Q K n^{2/3}(log n)^{1/3} + n^{2/3}(log n)^{1/3}
                      + sqrt(K Q n log K) + Q K log K log n ).

(iii) (Honest-benchmark robustness.) For every feasible behavioural profile
`S = (S_1, ..., S_K)` with `S_j in B^ctx+_{j,n}`,

    P(n; S) >= E sum_{t<=n} b(X_t)
               - [ min{Q K L, n} + 2 s n + Q + sqrt(2 ell Q n)
                   + 11 sqrt(K Q n log K) + 11 Q K log K log_2(2n) + 3 n^{-2} ]
            = E sum_{t<=n} b(X_t)
               - O( Q K n^{2/3}(log n)^{1/3} + n^{2/3}(log n)^{1/3} + sqrt(Q n log n)
                    + sqrt(K Q n log K) + Q K log K log n ).

All expectations are over arrivals, reward seeds, priorities, mechanism coins and private
coins. The constants are absolute except where `delta_i(z)` appears; part (i) is uniform over
deviations for each fixed instance but NOT over instance sequences whose positive capacity
gaps `delta_i(z)` vanish with `n`.

**Proposition 2 (the `Q L` term is attained).** Fix `K >= 2`, a finite `X_F` with `|X_F| = Q`,
and an instance in which one agent `i` is the unique top at every profile, and
`mu_i(z_i) < M_i(z_i)` for every `z` if `i` is honest. Let the arrival sequence be any
deterministic sequence with `V_z >= K L` for every `z in X_F` (this requires `n >= Q K L`).
Put `m'(z) := max{ (M_i(z_i) + V_i(z))/2 , mu_i(z_i) 1{i honest} }` and
`c := min_z ( M_i(z_i) - m'(z) ) > 0`. For every `n` with
`4 s < min_z ( M_i(z_i) - V_i(z) )`, the deviation `S'_{i,n}` that delivers `m'(z)` on every
Stage-1 pull at every `z` and follows `S^*_i` afterwards lies in `B^ctx_{i,n}` and satisfies

    u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n) >= c Q L - 4 Q n^{-3}.

Hence the `Q L` term of (i) cannot be removed, and the condition
`Q = o( n^{1/3} (log n)^{-1/3} )` is sharp up to the instance constant `c` and the constraint
`Q K L <= n` needed for the construction.

============================================================================================
## 4. The probability space, the global filtration, and conditioning on arrivals

### 4.1 One space carrying both executions

Fix `i` and a deviation `S'_{i,n} in B^ctx+_{i,n}`. Build one probability space carrying

* the arrival sequence `X`;
* the seed array `U = {U_{z,j,k}}` of (A2);
* the priorities `{pi_z}`, the EXP3 coins, and all agents' private coins;

all mutually independent as in (A1), (A2), (M7). On this space define TWO executions by the
same primitives:

* the BASELINE execution, in which every agent plays `S^*`;
* the DEVIATING execution, in which agent `i` plays `S'_{i,n}` and every `j != i` plays `S^*_j`.

Both are deterministic measurable functions of the primitives, because at every round the
selection rule, the agents' rules, and (SEED) are measurable functions of the primitives and
the history. Every expectation below is on this single space; `u_i(n; S'_{i,n}, S^*_{-i,n})`
is the expected utility of `i` in the deviating execution and `u_i(n;S^*_n)` its expected
utility in the baseline execution. Superscripts `'` and `*` distinguish the two executions.

### 4.2 Conditioning on the arrival sequence

Fix `x in X_F^n` with `Pr(X = x) > 0` (a positive-probability event, because `X_F^n` is
finite, so there are no regular-conditional-probability issues). By (A1), conditionally on
`{X = x}` the primitives `U`, the priorities, the mechanism coins and the private coins are
still mutually independent with their unconditional laws.

Conditionally on `{X = x}`:

* every visit count `V_z = V_z(x)` is a deterministic number, and the set of global rounds at
  which profile `z` is visited is a deterministic set `T_z(x) subseteq [n]` of size `V_z(x)`;
* the whole local schedule of every profile is deterministic: the `k`-th visit to `z` is the
  `k`-th smallest element of `T_z(x)`;
* every strategy in `B^ctx+_{i,n}` becomes a rule that depends only on `i`'s own history and
  private coins (the arrival sequence is now a constant), that is, an ordinary behavioural
  strategy for the deterministic schedule `x`.

Write `E_x[.] := E[. | X = x]` and, for a functional `F` of the two executions,
`E[F] = sum_x Pr(X=x) E_x[F]`. Every bound in Sections 5 to 8 is proved for each fixed `x`,
uniformly over `S'_{i,n}`, and only then averaged. This is exactly the ledger's step 1; it is
settled in Section 10(a).

### 4.3 The global filtration

Work conditionally on `{X = x}`. Let

    F_0 := sigma( all priorities {pi_z}, all agents' private coins ),
    F_t := F_0 v sigma( (I_r, m_{I_r,r}, Y_r)_{r <= t}, all mechanism coins drawn up to r=t ),

the global filtration of the execution under discussion (the construction is the same in both
executions). Two facts hold by (A2) and (M7), for every round `t`:

(F1) The seed used at round `t` is `U_{X_t, I_t, k}` where `k` is `I_t`'s local pull index at
`X_t` before round `t`, hence `k` and `I_t` are determined by `F_{t-1}` and the round-`t`
mechanism coin. That triple `(X_t, I_t, k)` has not been consumed before, so
`U_{X_t,I_t,k}` is independent of `F_{t-1} v sigma(round-t mechanism coin)`.

(F2) Therefore, with `m_t := m_{I_t,t}` the target chosen at round `t` (measurable with
respect to `F_{t-1} v sigma(round-t mechanism coin)`, since agents' private coins are already
in `F_0`),

    E[ Y_t | F_{t-1} v sigma(round-t mechanism coin) ] = m_t .

Putting ALL private coins into `F_0` is legitimate precisely because they are independent of
`U`, of the priorities and of the mechanism coins. It has the convenient effect of making
every agent's target a deterministic function of the history and the mechanism coins, so no
further conditioning on private randomisation is ever needed.

This filtration is GLOBAL: it does not decompose across profiles. Every lemma below is stated
against it. That is how delicate point (c) is settled; see Section 10(c).

============================================================================================
## 5. Structural lemmas

Throughout Section 5 we work conditionally on `{X = x}`.

### Lemma 3 (local decoupling of the mechanism and of the non-deviators)

Fix a profile `z`. In either execution, the following objects are measurable functions of
`( {U_{z,j,k} : j in [K], k >= 1}, pi_z, the EXP3 coins of z, the targets delivered by agent i
at visits to z )` alone:

  the local phase sequence at `z`, the bids `(beta_j(z))_{j}`, the winner `W_z`, the price
  `tau_z`, the identity of the agent selected at each visit to `z`, and the rewards observed
  at each visit to `z`.

In particular:

(L3a) For every `j != i`, the bid `beta_j(z)` equals `L^{-1} sum_{k<=L} 1{U_{z,j,k} <= M_j(z_j)}`
in BOTH executions. It does not depend on the deviation at all, nor on anything that happens
at any other profile.

(L3b) The quantity `tau_{z,i} := ( max_{j != i} beta_j(z) - s )_+` is a measurable function of
`{U_{z,j,k} : j != i, k <= L}` only. It is identical in the two executions, and the family
`( tau_{z,i} )_{z in X_F}` is independent across profiles.

(L3c) Nothing that happens at a profile `z` influences any local quantity at a profile
`z' != z`, except through the deviator's own targets at `z'`.

Proof. Induction on the visits to `z`, in local time. The mechanism's local instance at `z`
reads only its own local history: which agent to pull is determined by (M1) to (M5) from the
local phase, `pi_z`, the local bids, `tau_z`, the local primary reward sums, and the EXP3
state at `z`, and the parameters `L, s, b(.)` are deterministic functions of the global `n`.
Every non-deviating agent plays `S^*`, which is LOCAL-MARKOV (Section 2): at a visit to `z` it
delivers a deterministic function of `(z, local phase at z, tau_z)`. The reward at the `k`-th
selection of `j` at `z` is `1{U_{z,j,k} <= m}` by (SEED). Hence each local step at `z`
consumes only the listed inputs, and the induction closes. (L3a) is the case `j != i` in
Stage 1, where `S^*_j` prescribes `M_j(z_j)` regardless of phase information. (L3b) follows
from (L3a) and the independence of the seed array across profiles. (L3c) is the statement of
the induction read across profiles. QED

Remark. (L3c) is delicate point (d), settled: see Section 10(d). Note carefully what is NOT
claimed: the two local executions at `z` and `z'` are NOT independent random objects in the
deviating execution, because the deviator's targets at `z` and at `z'` may be correlated
through its own global history. What is claimed, and all that is used, is that the MECHANISM
at `z'` and the NON-DEVIATORS at `z'` read nothing from `z`.

### Lemma 4 (bid domination and the winner inclusion)

Fix a profile `z` with `V_z >= K L` and an agent `i`. Then, pathwise on the coupled space:

(L4a) `beta'_i(z) <= beta^*_i(z)`, where `beta'_i(z)` is `i`'s bid in the deviating execution
and `beta^*_i(z) = L^{-1} sum_{k<=L} 1{U_{z,i,k} <= M_i(z_i)}` its bid in the baseline.

(L4b) `{ i wins at z in the deviating execution } subseteq { i wins at z in the baseline }`.

(L4c) On `{ i wins at z in the deviating execution }`, the prices in the two executions
coincide and both equal `tau_{z,i}`.

(L4d) Agent `i` receives exactly `l_i(z)` Stage-1 pulls at `z` in BOTH executions, and its
`k`-th Stage-1 pull at `z` occurs at the SAME global round in both executions.

Proof. (L4d) first: by (M1), the Stage-1 schedule at `z` is the fixed permutation `sigma_z`
with `L` consecutive pulls each, and the visits to `z` are the deterministic rounds `T_z(x)`.
Hence the identity of the agent pulled at the `k`-th visit to `z` for `k <= K L` is a
deterministic function of `(x, sigma_z)`, the same in both executions, and `i` is pulled
exactly on the visits in its own block, of which `l_i(z)` occur.

(L4a): by (L4d), `i`'s `k`-th Stage-1 pull at `z` uses the seed `U_{z,i,k}` in both
executions. In the deviating execution its target `m'_{i,k}` satisfies
`m'_{i,k} <= M_i(z_i)` by feasibility, so
`1{U_{z,i,k} <= m'_{i,k}} <= 1{U_{z,i,k} <= M_i(z_i)}` pointwise, for every realisation.
Averaging over `k <= L` gives (L4a). Note that no predictability or measurability of
`m'_{i,k}` is needed: the inequality is pointwise in the realised target, so a deviator that
times its bid-stage behaviour using its history at OTHER profiles, or using future arrivals,
is covered. This is the pathwise part of delicate point (c).

(L4b): by (L3a) the bids of all `j != i` are identical in the two executions, and by (M2) the
priority permutation `pi_z` is the same. Suppose `i` wins in the deviating execution: for
every `j != i`, either `beta_j(z) < beta'_i(z)`, or `beta_j(z) = beta'_i(z)` and `i` precedes
`j` in `pi_z`. Since `beta^*_i(z) >= beta'_i(z)`, in the baseline every `j != i` satisfies
either `beta_j(z) < beta^*_i(z)`, or `beta_j(z) = beta^*_i(z)` and `i` precedes `j` in
`pi_z`. Hence `i` is a largest bidder in the baseline and wins its priority comparisons, so
`i` wins in the baseline.

(L4c): if `i` is a largest bidder then the second order statistic with multiplicity of
`(beta_1, ..., beta_K)` equals `max_{j != i} beta_j`: sorting descending, one copy of the
maximum is `beta_i`, and the next entry is the largest of the remaining multiset, which is
`max_{j != i} beta_j` when `i` attains the maximum. Hence
`tau_z = (max_{j != i} beta_j(z) - s)_+ = tau_{z,i}` in whichever execution `i` wins, and by
(L3a) the two values agree. QED

Remark on `K = 2`. (L4c) with `K = 2` reads `beta_(2) = beta_j` for the single `j != i`, and
the argument above is exactly the general one. Ties `beta_1 = beta_2` are resolved by `pi_z`
and change nothing, because (L4b) and (L4c) never use a strict inequality. This is half of
delicate point (e); see Section 10(e).

### Lemma 4b (Azuma-Hoeffding, conditional-range form; stated to keep the document self-contained)

Let `(H_r)_{r>=0}` be a filtration and `(D_r)_{r>=1}` adapted with `E[D_r | H_{r-1}] = 0` and
`D_r in [a_r, a_r + c]` almost surely, where `a_r` is `H_{r-1}`-measurable and `c > 0` is a
constant. Then for every `R >= 1` and `lambda > 0`,

    Pr{ sum_{r<=R} D_r >= lambda } <= exp( - 2 lambda^2 / (R c^2) ),

and the same bound holds for the lower tail.

Proof. Hoeffding's lemma applied conditionally on `H_{r-1}` gives
`E[ e^{u D_r} | H_{r-1} ] <= e^{u^2 c^2/8}` for every `u > 0`. Iterating the tower property
from `r = R` down to `r = 1` gives `E[ e^{u sum_{r<=R} D_r} ] <= e^{R u^2 c^2/8}`. Markov's
inequality and the choice `u = 4 lambda/(R c^2)` give the claim; the lower tail follows by
replacing `D_r` with `-D_r`. QED

The only external facts used anywhere in this document are Hoeffding's lemma (a mean-zero
random variable supported in an interval of length `c` has
`E e^{uD} <= e^{u^2 c^2/8}`) and, through it, Hoeffding's inequality for sums of independent
bounded variables. No result is imported from the bandit or mechanism-design literature: in
particular Lemma 6 below reproves the manuscript's EXP3 lemma from scratch rather than citing
any published doubling variant.

### Lemma 5 (anytime local monitor against a globally adaptive winner)

Fix a profile `z` with `V_z >= K L`, and consider either execution. Let `W = W_z` be the local
winner, let `q` be the number of local primary pulls at `z` (including the pull on which the
switch occurs, when there is one), let `m_r` be `W`'s target on its `r`-th local primary pull
and `Y_r` the corresponding reward, `A_r := sum_{u<=r} m_u`, `Z_r := sum_{u<=r} Y_u`,
`A_0 = Z_0 = 0`. Then

    Pr{ exists r <= q : |Z_r - A_r| > b(r) } <= n^{-3},                                (5.1)

and on the complementary event

    A_q >= q tau_z - 1 - 2 b(q),
    U_i^{pri}(z) <= q ( 1 + mu_i(z_i) - tau_z ) + 1 + 2 b(q)   when W = i,             (5.2)

where `U_i^{pri}(z)` is `i`'s realised utility on its local primary pulls at `z`. Moreover, if
every local primary target at `z` is at least `tau_z`, then

    Pr{ the local instance at z ever switches } <= (2 n^3)^{-1}.                       (5.3)

The bounds hold for an arbitrary winner whose targets are chosen at the pull as measurable
functions of the entire global history, the entire arrival sequence and its private coins.

Proof. Extend the primary reward sequence at `z` to the full range `r = 1, ..., n` by a
PHANTOM CONTINUATION, on the same probability space and with no extra randomness. Recall from
(M1) that `W` receives exactly `L` bidding pulls at `z`, so its `r`-th primary pull at `z` is
its local pull number `L + r` and uses the seed `V_r := U_{z,W,L+r}`. Define, for
`r = 1, ..., n`,

    m_r := the target actually chosen by W at its r-th primary pull at z,  if r <= q,
    m_r := tau_z,                                                          if r > q,
    Y_r := 1{ V_r <= m_r },     A_r := sum_{u<=r} m_u,    Z_r := sum_{u<=r} Y_u.

For `r <= q` these agree with the realised primary quantities. Define the sigma-fields

    H_r := sigma( all primitives except { U_{z,j,L+r'} : j in [K], r' > r } ),  r = 0,1,...,n.

The excluded index set is DETERMINISTIC: it does not refer to `W`, which is itself random.
(Excluding only `W`'s seeds would make the index set random and the definition circular; this
is why all `K` agents' post-bidding seeds at `z` are excluded.) Thus `H_r` contains the arrival
sequence, all priorities, all mechanism coins, all private coins, every seed at every profile
`z' != z`, every Stage-1 seed `U_{z,j,k}` with `k <= L`, and every post-bidding seed
`U_{z,j,L+r'}` with `r' <= r`. The excluded sets shrink with `r`, so `(H_r)_{r>=0}` is a
filtration, and `V_r = U_{z,W,L+r}` is a `H_r`-measurable function of `W` (which is
`H_0`-measurable) and the `H_r`-measurable vector `(U_{z,j,L+r})_{j in [K]}`.

Claim 1: `W`, `tau_z`, the bids `(beta_j(z))_j` and the events `{q >= r}` are `H_{r-1}`-
measurable. Indeed `W`, `tau_z` and the bids are determined by the Stage-1 seeds
`U_{z,j,k}, k <= L`, and by `pi_z`, all of which lie in `H_0`. The event `{q >= r}` is
determined by the survival conditions at clocks `1, ..., r-1`, hence by
`Z_1, ..., Z_{r-1}, tau_z` and `b(.)`, all in `H_{r-1}`.

Claim 2: `m_r` is `H_{r-1}`-measurable. For `r > q` this is immediate, since `m_r = tau_z` and
`{q < r}` is in `H_{r-1}` by Claim 1. For `r <= q`, `m_r` is a function of the global history
strictly before `W`'s `r`-th primary pull at `z`, of the arrival sequence and of the private
coins. That history is generated by primitives consumed at earlier rounds. The seeds at `z`
consumed strictly earlier are, for `W`, the indices `k <= L + r - 1`, and, for `j != W`, only
the Stage-1 indices `k <= L`, because while the local instance at `z` is still in its primary
phase no agent other than `W` is pulled at `z` after Stage 1. None of these is an excluded
index `U_{z,j,L+r'}` with `r' >= r`. Seeds at other profiles are never excluded. So the claim
holds.

Since the primitives are mutually independent, the vector `(U_{z,j,L+r})_{j in [K]}` is
independent of `H_{r-1}` and uniformly distributed, and `W` and `m_r` are `H_{r-1}`-measurable,
whence

    E[ Y_r - m_r | H_{r-1} ] = E[ 1{U_{z,W,L+r} <= m_r} | H_{r-1} ] - m_r = m_r - m_r = 0,

and, given `H_{r-1}`, the increment `Y_r - m_r` takes values in `{-m_r, 1-m_r}`, an interval
of length one whose endpoints are `H_{r-1}`-measurable. Lemma 4b with `c = 1` gives, for each fixed `R <= n` and each tail,

    Pr{ |Z_R - A_R| > b(R) } <= 2 exp( - 2 b(R)^2 / R ) = 2 exp( - ell ) = (n^4)^{-1},

using `2 b(R)^2 / R = ell = log(2 n^4)` and `2 e^{-ell} = 2/(2n^4) = n^{-4}`. A union bound
over `R = 1, ..., n` gives `Pr{exists R <= n : |Z_R - A_R| > b(R)} <= n^{-3}`, and since
`q <= V_z <= n` this implies (5.1). (The union over `R <= n` covers every realisable local
primary length precisely because `V_z <= n`; this is why the boundary `b(.)` and the
confidence levels are built from the GLOBAL `n`.)

A point an adversary should check. The seeds `V_r` with `r > q` are also consumed by the REAL
execution, namely by the fallback selections at `z`, whose local pull indices continue past
`L + q`. This is harmless. The filtration `H_r` is defined from the PRIMITIVES with a
deterministic excluded index set, not from the history, so the increment identity above holds
by construction whatever else those seeds are later used for; the phantom variables `Y_r`,
`A_r`, `Z_r` for `r > q` are analytical devices that appear only inside the union bound and
never describe the real execution; and the conclusions (5.1), (5.2), (5.3) are asserted only
for indices `r <= q`, where phantom and real coincide.

(5.2). On the complement, suppose first that no switch occurs, so `q` is the number of primary
visits and the survival condition `Z_r >= r tau_z - b(r)` held at `r = q`; combining with
`Z_q <= A_q + b(q)` gives `A_q >= q tau_z - 2 b(q)`. If the switch occurs at `r = q >= 2`,
apply the same two inequalities at `q - 1`, obtaining `A_{q-1} >= (q-1) tau_z - 2 b(q-1)`, and
then `A_q >= A_{q-1} >= q tau_z - tau_z - 2 b(q) >= q tau_z - 1 - 2 b(q)` using
`tau_z in [0,1]`, `m_q >= 0` and `b` nondecreasing. If the switch occurs at `q = 1` then
`A_1 >= 0 >= tau_z - 1 = q tau_z - 1` since `tau_z <= 1`. In all cases
`A_q >= q tau_z - 1 - 2 b(q)`. When `W = i`, `U_i^{pri}(z) = q(1 + mu_i(z_i)) - A_q`, and
substituting gives the second line of (5.2).

(5.3). If every realised primary target is at least `tau_z`, then so is every phantom target
(`m_r = tau_z` for `r > q`), hence `A_r >= r tau_z` for every `r <= n`. A switch at `r` means
`Z_r < r tau_z - b(r) <= A_r - b(r)`, that is `Z_r - A_r < -b(r)`. The one-sided union bound
over `r <= n` gives probability at most `n (2n^4)^{-1} = (2n^3)^{-1}`. QED

Remark. Lemma 5 is the manuscript's `lem:private-monitor` with three changes: the filtration
is global rather than "conditional on the bidding history"; the phantom continuation makes the
union bound over a deterministic range legitimate without any optional-stopping step; and the
targets are allowed to depend on the deviator's history at other profiles and on future
arrivals. The proof of `lem:private-monitor` in `sections/appendix_private.tex` is otherwise
identical line by line, and its constants are unchanged.

### Lemma 6 (one epoch of explicit-exploration EXP3, truncated, with reactive selected agents)

Consider one epoch of the local fallback at `z`, with planned length `B = 2^k`, parameters
`gamma = gamma_k` and `eta = eta_k` as in (M4), and realised length `H' <= B`, where `H'` is
measurable with respect to the epoch-start information (true here: conditionally on
`{X = x}`, `H' = min{B, V_z - (local clock at the epoch start) + 1}` is deterministic given
the epoch start). Let `G_ep` be the sigma-field generated by everything up to the epoch start.
Suppose some agent `j` satisfies `E[ Y_t | F_{t-1}, I_t = j ] >= v` at every round `t` of the
epoch, where `F_{t-1}` is the global filtration of Section 4.3. All other agents may choose
arbitrary feasible targets after selection, as measurable functions of the entire global
history, the arrival sequence and their private coins. Then

    E[ sum_{t in epoch} Y_t | G_ep ] >= v H' - R_K(B).                                  (6.1)

Proof. Condition on `G_ep` throughout and assume `H' >= 1`. Write `r_{l,t} := E[Y_t | F_{t-1},
I_t = l]` for the conditional mean of the reward if `l` is selected at round `t` of the epoch;
this is well defined by (F2), and `r_{l,t} in [0,1]`. Note `r_{j,t} >= v` by hypothesis.

Potential step (pathwise, for any prefix). Let `W_t := sum_l w_{l,t}`. Because
`p_{l,t} >= gamma/K = eta` we have `0 <= eta hat Y_{l,t} <= eta Y_t / p_{l,t} <= eta K/gamma
= 1`. Using `e^u <= 1 + u + u^2` on `[0,1]` and `log(1+u) <= u`,

    log( W_{t+1}/W_t ) = log( sum_l q_{l,t} e^{eta hat Y_{l,t}} )
                      <= eta sum_l q_{l,t} hat Y_{l,t} + eta^2 sum_l q_{l,t} hat Y_{l,t}^2 .

Summing over the rounds `t = 1, ..., H'` of the epoch and using
`log(W_{H'+1}/W_1) >= log( w_{j,H'+1}/W_1 ) = eta sum_t hat Y_{j,t} - log K`:

    sum_{t<=H'} hat Y_{j,t} - (log K)/eta
        <= sum_{t<=H'} sum_l q_{l,t} hat Y_{l,t} + eta sum_{t<=H'} sum_l q_{l,t} hat Y_{l,t}^2 .
                                                                                        (6.2)

This inequality is a sum of per-round inequalities, so it holds for EVERY prefix length `H'`,
not only for the planned `B`. This is the only property of the truncation that is used.

Expectation step. By (F2) and the independence of the EXP3 coin from `F_{t-1}`,

    E[ hat Y_{l,t} | F_{t-1} ] = p_{l,t}^{-1} E[ Y_t 1{I_t = l} | F_{t-1} ] = r_{l,t},
    E[ hat Y_{l,t}^2 | F_{t-1} ] = p_{l,t}^{-2} E[ Y_t^2 1{I_t = l} | F_{t-1} ]
                                 = r_{l,t} / p_{l,t}   (Y_t in {0,1}),

so, with `Q_t := sum_l q_{l,t} r_{l,t}` and `G_t := sum_l p_{l,t} r_{l,t} = E[Y_t | F_{t-1}]`,

    E[ sum_l q_{l,t} hat Y_{l,t} | F_{t-1} ] = Q_t,
    E[ sum_l q_{l,t} hat Y_{l,t}^2 | F_{t-1} ] = sum_l q_{l,t} r_{l,t} / p_{l,t}
                                               <= K / (1 - gamma),

the last because `p_{l,t} >= (1-gamma) q_{l,t}` and `r_{l,t} <= 1`. Also
`G_t >= (1-gamma) Q_t`. Taking expectations in (6.2) given `G_ep` and using the tower property
round by round (all the quantities `q_{l,t}, p_{l,t}` are `F_{t-1}`-measurable, and `H'` is
`G_ep`-measurable so the number of terms is not random):

    v H' - (log K)/eta <= E[ sum_{t<=H'} Q_t ] + eta H' K/(1-gamma)
                       <= (1-gamma)^{-1} E[ sum_{t<=H'} G_t ] + eta H' K/(1-gamma).

Multiplying by `1-gamma` and using `E[ sum_t G_t | G_ep ] = E[ sum_t Y_t | G_ep ]`:

    E[ sum_{t<=H'} Y_t | G_ep ] >= (1-gamma) v H' - (1-gamma)(log K)/eta - eta K H'
                                >= v H' - gamma (v+1) H' - K log K/gamma
                                >= v H' - 2 gamma H' - K log K / gamma,

using `eta = gamma/K` and `v <= 1`.

Constant. Since `H' <= B`, the loss is at most `2 gamma B + K log K/gamma` with
`gamma = min{1/2, sqrt(K log K/B)}`. If `B >= 4 K log K` then `gamma = sqrt(K log K/B) <= 1/2`
and the loss is at most `2 sqrt(K B log K) + sqrt(K B log K) = 3 sqrt(K B log K)`. If
`B < 4 K log K` then `gamma = 1/2` and the loss is at most `B + 2 K log K`; moreover
`B < 4 K log K <= 9 K log K` gives `B <= 3 sqrt(K B log K)`, so the loss is at most
`3 sqrt(K B log K) + 2 K log K`. In both cases the loss is at most `R_K(B)`. QED

Remark. Lemma 6 is the manuscript's `lem:selected-reactive-exp3` with two changes, both
needed here: the horizon used to tune `gamma` is the PLANNED epoch length `B`, while the
realised length `H'` may be smaller; and the filtration is global. The manuscript's proof
already produces the display `E sum Y >= v H - 2 gamma H - K log K/gamma` and the same case
split for `R_K`; the only new observation is that (6.2) telescopes over an arbitrary prefix,
so nothing in the argument requires `H' = B`. The comparator condition
`E[Y_t | F_{t-1}, I_t = j] >= v` is satisfied by every non-deviating agent `j` at a fallback
pull at `z`, with `v = M_j(z_j)`, because `S^*` delivers capacity in the fallback.

### Lemma 7 (doubling the epochs)

Consider the local fallback at `z` with total length `H >= 1` (deterministic given `{X=x}` and
the fallback start). Under the hypotheses of Lemma 6, with the same comparator `j` and the
same `v` in every epoch,

    E[ sum_{t in fallback at z} Y_t | F_fb ] >= v H - R^dbl_K(H),
    R^dbl_K(H) = 11 ( sqrt(K H log K) + K log K log_2(2H) ).                            (7.1)

Proof. By (M4), epoch `k` covers local fallback clock times `2^k, ..., 2^{k+1}-1`. The epochs
actually entered are `k = 0, 1, ..., m-1` with `m - 1 = floor(log_2 H)`, so `2^{m-1} <= H` and
`m <= log_2 H + 1 = log_2(2H)`. Each epoch's realised length `H'_k` is determined by `H` and
`k`, hence is measurable with respect to the epoch start. Apply Lemma 6 in epoch `k`
conditionally on the epoch-start sigma-field and take the tower expectation down to `F_fb`:

    E[ sum_{t in epoch k} Y_t | F_fb ] >= v H'_k - R_K(2^k).

Summing over `k = 0, ..., m-1` and using `sum_k H'_k = H`:

    E[ sum_{t in fallback} Y_t | F_fb ] >= v H - sum_{k=0}^{m-1} R_K(2^k).

Now
`sum_{k=0}^{m-1} 3 sqrt(K 2^k log K) = 3 sqrt(K log K) (2^{m/2} - 1)/(2^{1/2} - 1)`
and `2^{m/2} = sqrt(2 . 2^{m-1}) <= sqrt(2H)`, so this is at most
`3 sqrt(2)/(sqrt(2)-1) . sqrt(K H log K) = 10.2427 ... sqrt(K H log K)`.
Also `sum_{k=0}^{m-1} 2 K log K = 2 m K log K <= 2 K log K log_2(2H)`. Hence

    sum_{k=0}^{m-1} R_K(2^k) <= 10.2428 sqrt(K H log K) + 2 K log K log_2(2H)
                             <= 11 ( sqrt(K H log K) + K log K log_2(2H) ) = R^dbl_K(H).  QED

This settles delicate point (b), including the absolute constant: `C_0 = 11` works and
`C_0 = 3 sqrt(2)/(sqrt(2)-1) = 10.2427` is the exact constant of the square-root part.

### Lemma 8 (local fallback utility of the deviator)

Fix `z` with `V_z >= K L`, suppose the local instance at `z` enters fallback, let `F_fb` be the
global sigma-field at the fallback start, `H = H_z >= 1` the fallback length,
`bar Q_i := E[ #{fallback pulls of i at z} | F_fb ]`,
`bar A_i := E[ sum over i's fallback pulls at z of m_{i,t} | F_fb ]`. Then

    bar A_i >= V_i(z) bar Q_i - R^dbl_K(H),                                             (8.1)
    E[ U_i^{fb}(z) | F_fb ] <= ( 1 + mu_i(z_i) - V_i(z) ) H + R^dbl_K(H),               (8.2)
    E[ U_i^{fb}(z) | F_fb ] <= 2 R^dbl_K(H) / delta_i(z)   when delta_i(z) > 0.          (8.3)

Proof. Let `j*` attain `V_i(z) = max_{j != i} M_j(z_j)`. Agent `j*` follows `S^*`, so at every
fallback pull at `z` its conditional reward mean is exactly `M_{j*}(z_{j*}) = V_i(z)`. Lemma 7
with `v = V_i(z)` gives `E[ sum_t Y_t | F_fb ] >= V_i(z) H - R^dbl_K(H)`. On the other hand
`E[ sum_t Y_t | F_fb ] = E[ sum_t m_{I_t,t} | F_fb ] = bar A_i + sum_{j != i} M_j(z_j)
E[ #{fallback pulls of j} | F_fb ] <= bar A_i + V_i(z) (H - bar Q_i)`, which is (8.1).
Then `E[U_i^{fb}(z) | F_fb] = (1 + mu_i(z_i)) bar Q_i - bar A_i
<= (1 + mu_i(z_i) - V_i(z)) bar Q_i + R^dbl_K(H)`; since `V_i(z) <= 1 <= 1 + mu_i(z_i)` the
coefficient is nonnegative and `bar Q_i <= H` gives (8.2). For (8.3), feasibility gives
`bar A_i <= M_i(z_i) bar Q_i`, so (8.1) yields `delta_i(z) bar Q_i <= R^dbl_K(H)`, and
`U_i^{fb}(z) <= 2 . #{fallback pulls of i}` because per-pull utility is at most two. QED

These are the manuscript's `eq:private-fallback-core`, `eq:private-fallback-top` and
`eq:private-fallback-low` with `R_K(H)` replaced by `R^dbl_K(H)` and with the global
filtration.

============================================================================================
## 6. Proof of Theorem 1(i)

Fix `i`, fix `S'_{i,n} in B^ctx+_{i,n}`, and fix an arrival sequence `x` with `Pr(X=x)>0`. All
of Section 6 is conditional on `{X = x}`; write `E_x` and recall from Section 4.2 that every
`V_z`, `n_z`, `l_i(z)` and every local schedule is then a deterministic number.

### 6.1 Exact decomposition of the utility difference

For a profile `z` let `U_i(z)` be `i`'s realised utility on the visits to `z`,
`U_i(z) = sum_{t : X_t = z, I_t = i} ( 1 + mu_i(z_i) - m_{i,t} )`. Because `X_t = z` on those
rounds, and the rounds `[n]` are partitioned by the profiles,

    u_i(n; S'_{i,n}, S^*_{-i,n} | x) - u_i(n; S^*_n | x)
        = sum_{z in X_F} [ E_x U'_i(z) - E_x U^*_i(z) ] .                                (6.3)

This is an identity, not an estimate. It is where the cross-profile deviator is neutralised:
we never need the local executions to be independent of each other, only linearity of
expectation. Split `U_i(z) = U_i^{bid}(z) + U_i^{post}(z)` into the Stage-1 pulls and the rest.

### 6.2 The bidding term (pathwise, every profile)

By (L4d) agent `i` receives exactly `l_i(z)` Stage-1 pulls at `z` in both executions, at the
same global rounds. Its baseline target there is `M_i(z_i)` and its deviating target is some
`m' in [0, M_i(z_i)]`, so the per-pull utility difference is `M_i(z_i) - m' in [0,1]`. Hence

    U'^{bid}_i(z) - U^{*bid}_i(z) <= l_i(z)      pathwise, for every profile z.           (6.4)

In particular, if `V_z < K L` then (M5) makes every visit a bidding pull, `U^{post}_i(z) = 0`
in both executions, and the whole profile contributes at most `l_i(z)`. This is delicate
point (f), settled: see Section 10(f). Summing, `sum_z l_i(z) <= min{Q L, n}`.

### 6.3 The events

For the rest of Section 6 fix `z` with `V_z >= K L`. Define

    Win'   := { i wins the local award at z in the deviating execution },
    Win*   := { i wins the local award at z in the baseline execution },
    G(z)   := { |beta_j(z) - M_j(z_j)| <= s  for every j != i },
    Mon'   := { |Z_r - A_r| <= b(r) for every r <= n, deviating execution at z },
    Mon*   := the same event for the baseline execution at z,

where in `Mon'` and `Mon*` the sequences `(Z_r, A_r)` are the PHANTOM-EXTENDED primary
sequences of the proof of Lemma 5, so that the index range `r <= n` is deterministic.

By (L4b), `Win' subseteq Win*`. By (L3a) each `beta_j(z)`, `j != i`, is the mean of `L`
independent Bernoulli`(M_j(z_j))` variables, so Hoeffding and a union bound give

    Pr( G(z)^c ) <= 2 (K-1) exp(-2 L s^2) = (K-1)/(K n^4) <= n^{-4},                     (6.5)

because `2 L s^2 = log(2 K n^4)`. On `G(z)`, since `u -> max_{j != i} u_j` is 1-Lipschitz in
the supremum norm and `(.)_+` is nondecreasing and 1-Lipschitz,

    ( V_i(z) - 2 s )_+ <= tau_{z,i} <= V_i(z)      on G(z).                              (6.6)

By Lemma 5, `Pr(Mon'^c) <= n^{-3}` and `Pr(Mon*^c) <= n^{-3}`. The events `Win'`, `Win*`,
`G(z)` are measurable with respect to the Stage-1 data at `z` together with `pi_z`; in
particular they belong to the sigma-field `H_0` of Lemma 5, so Lemma 5 may be applied on them.

Post-bid utilities are always in `[0, 2 n_z]`, and baseline post-bid utility is always
nonnegative. These two facts absorb all bad events.

### 6.4 The losing branch

Work on `(Win')^c cap G(z)`. The local winner is some `W != i`, which follows `S^*`. On
`G(z)`, `tau_z = ( beta_(2)(z) - s )_+ <= ( beta_W(z) - s )_+ <= M_W(z_W)`, using that `W` is
a largest bidder and `|beta_W(z) - M_W(z_W)| <= s`. Hence `S^*`'s primary target of `W` is
`min{tau_z, M_W(z_W)} = tau_z` if `W` is strategic and `max{mu_W(z_W), tau_z} >= tau_z` if `W`
is honest. So on `(Win')^c cap G(z)` every realised primary target at `z` is at least `tau_z`,
and (extending by the phantom target `tau_z`) `A_r >= r tau_z` for every `r <= n`. A switch at
`r` then forces `Z_r - A_r < -b(r)`, so by the one-sided bound inside the proof of Lemma 5,

    Pr( (Win')^c cap G(z) cap { the local instance at z switches } ) <= (2 n^3)^{-1}.     (6.7)

Observe that this is the step that rules out the following attack: the deviator underbids or
overbids at `z` in order to raise the announced price above the winner's capacity and so
provoke a fallback in which the deviator itself gets selected. It cannot: whenever `i` loses,
`beta_(2)(z) <= beta_W(z)`, so the price is at most `M_W(z_W)` on `G(z)`, and the winner meets
it.

On `(Win')^c cap G(z) cap {no switch}` agent `i` receives no post-bid pull at `z`, so
`U'^{post}_i(z) = 0`. Therefore

    E_x[ U'^{post}_i(z) 1{(Win')^c} ] - E_x[ U^{*post}_i(z) 1{(Win')^c} ]
        <= 2 n_z ( n^{-4} + (2 n^3)^{-1} ) .                                             (6.8)

### 6.5 The winning branch, `i` top at `z` (`delta_i(z) <= 0`)

Work on `Win' cap G(z)`; by (L4c) both executions face the price `tau_{z,i}`, and by (6.6)
`tau_{z,i} <= V_i(z) <= M_i(z_i)`.

Deviating side. Let `q` be the deviating local primary length and `H_z = n_z - q` the
deviating local fallback length. On `Mon'`, (5.2) gives
`U'^{pri}_i(z) <= q (1 + mu_i(z_i) - tau_{z,i}) + 1 + 2 b(q)`, and off `Mon'` we use
`U'^{pri}_i(z) <= 2 n_z`. Lemma 8 (8.2), together with `tau_{z,i} <= V_i(z)` on `G(z)` and the
fact that `Win' cap G(z)` is `F_fb`-measurable, gives
`E_x[ U'^{fb}_i(z) | F_fb ] <= ( 1 + mu_i(z_i) - tau_{z,i} ) H_z + R^dbl_K(H_z)` on
`Win' cap G(z)`. Since `q + H_z = n_z` and `b`, `R^dbl_K` are nondecreasing,

    E_x[ U'^{post}_i(z) 1{Win' cap G(z)} ]
      <= E_x[ 1{Win' cap G(z)} ( (1 + mu_i(z_i) - tau_{z,i}) n_z + 1 + 2 b(n_z)
                                  + R^dbl_K(n_z) ) ]  + 2 n_z n^{-3}.                    (6.9)

Baseline side. On `Win' subseteq Win*` the baseline awards `z` to `i` at the same price
`tau_{z,i}`. Let `Lambda := { i honest } cap { tau_{z,i} <= mu_i(z_i) }`, an `H_0`-measurable
event.

* On `Lambda^c cap Win' cap G(z)` the baseline primary target of `i` is `tau_{z,i}`: if `i` is
  strategic this is `min{tau_{z,i}, M_i(z_i)} = tau_{z,i}` because `tau_{z,i} <= M_i(z_i)`; if
  `i` is honest and `tau_{z,i} > mu_i(z_i)` it is
  `max{mu_i(z_i), min{tau_{z,i}, M_i(z_i)}} = tau_{z,i}`. All baseline primary targets are then
  at least `tau_z`, and so is the phantom target `tau_z`; hence, exactly as in (6.7),
  `Lambda^c cap Win* cap G(z) cap {the baseline switches at z}` is contained in
  `{exists r <= n : Z_r - A_r < -b(r)}` for the baseline sequence, an event of probability at
  most `(2 n^3)^{-1}` by the one-sided bound inside the proof of Lemma 5;
  and on the further event that no baseline switch occurs, the baseline post-bid utility at
  `z` is exactly `n_z ( 1 + mu_i(z_i) - tau_{z,i} )`. Hence
  `E_x[ U^{*post}_i(z) 1{Lambda^c cap Win' cap G(z)} ] >= E_x[ 1{Lambda^c cap Win' cap G(z)}
  n_z (1 + mu_i(z_i) - tau_{z,i}) ] - 2 n_z (2 n^3)^{-1}`.
* On `Lambda cap Win' cap G(z)` the baseline primary target of `i` is `mu_i(z_i) >= tau_{z,i}`,
  so the same containment bounds the baseline switch probability by `(2 n^3)^{-1}`, and without a
  switch the baseline post-bid utility at `z` is exactly `n_z` (per-pull utility
  `1 + mu_i(z_i) - mu_i(z_i) = 1`). On the other side, `i` is honest, so every deviating target
  satisfies `m >= mu_i(z_i)`, every deviating post-bid selection is worth at most
  `1 + mu_i(z_i) - mu_i(z_i) = 1`, and there are at most `n_z` of them; so
  `U'^{post}_i(z) <= n_z`. The difference on this event is therefore at most
  `2 n_z (2 n^3)^{-1}`.

Now split `Win' cap G(z)` into `Lambda^c cap Win' cap G(z)` and `Lambda cap Win' cap G(z)`.
On the first piece, (6.9) restricted to it and the first bullet give a difference of at most
`1 + 2 b(n_z) + R^dbl_K(n_z) + 2 n_z n^{-3} + 2 n_z (2 n^3)^{-1}`, because the bracketed
`(1 + mu_i(z_i) - tau_{z,i}) n_z` in (6.9) is exactly the baseline value there and cancels. On
the second piece, the second bullet gives a difference of at most `2 n_z (2 n^3)^{-1}`, which
is smaller. Adding the `G(z)^c` piece (`U'^{post}_i(z) <= 2 n_z`, baseline `>= 0`, probability
at most `n^{-4}`) and the losing branch (6.8),

    E_x U'_i(z) - E_x U^*_i(z)
      <= l_i(z) + 1 + 2 b(n_z) + R^dbl_K(n_z)
         + 2 n_z [ n^{-3} + (2n^3)^{-1} + n^{-4} + n^{-4} + (2n^3)^{-1} ]
      <= l_i(z) + 1 + 2 b(n_z) + R^dbl_K(n_z) + 8 n_z n^{-3},                           (6.10)

using `n^{-4} <= n^{-3}` so that the bracket is at most `4 n^{-3}`.

The crucial cancellation is worth naming. The deviator's total post-bid utility at `z` is at
most `(1 + mu_i(z_i) - tau_{z,i}) n_z` plus the monitor slack `1 + 2 b(n_z)` plus the fallback
regret `R^dbl_K(n_z)`, and the baseline collects `(1 + mu_i(z_i) - tau_{z,i}) n_z` exactly.
Triggering the fallback therefore gains the deviator nothing of order `n_z`: by (8.2) the
fallback is worth at most `(1 + mu_i(z_i) - V_i(z))` per remaining round, and on `G(z)` this
is at most `(1 + mu_i(z_i) - tau_{z,i})`, which is exactly the baseline rate.

### 6.6 The winning branch, `i` not top at `z` (`delta_i(z) > 0`)

Suppose first `4 s <= delta_i(z)`. On `Win' cap G(z)`, (6.6) and
`V_i(z) = M_i(z_i) + delta_i(z) >= delta_i(z) >= 4 s` give

    tau_{z,i} - M_i(z_i) >= delta_i(z) - 2 s >= delta_i(z)/2 .

On `Mon'`, (5.2) gives `A_q >= q tau_{z,i} - 1 - 2 b(q)`, while feasibility gives
`A_q <= M_i(z_i) q`. Subtracting, with `d := delta_i(z)/2` and `b(q) = sqrt(q ell/2)`,

    q d <= q ( tau_{z,i} - M_i(z_i) ) <= 1 + 2 b(q) = 1 + sqrt(2 q ell)
        <= sqrt(q) ( 1 + sqrt(2 ell) )        (for q >= 1, since 1 <= sqrt(q); if q = 0
                                               there is nothing to prove),

so `sqrt(q) <= (1 + sqrt(2 ell))/d` and

    q <= 4 (1 + sqrt(2 ell))^2 / delta_i(z)^2 = O( log n / delta_i(z)^2 ).              (6.11)

Hence `U'^{pri}_i(z) <= 2 q <= 8 (1 + sqrt(2 ell))^2 / delta_i(z)^2` on `Mon' cap Win' cap
G(z)`. Lemma 8 (8.3) gives `E_x[ U'^{fb}_i(z) | F_fb ] <= 2 R^dbl_K(H_z)/delta_i(z) <=
2 R^dbl_K(n_z)/delta_i(z)`. The baseline post-bid utility is nonnegative. Adding the same bad
events as in (6.10),

    E_x U'_i(z) - E_x U^*_i(z)
      <= l_i(z) + 8 (1 + sqrt(2 ell))^2/delta_i(z)^2 + 2 R^dbl_K(n_z)/delta_i(z)
         + 8 n_z n^{-3} .                                                               (6.12)

If instead `4 s > delta_i(z)`, use `U'^{post}_i(z) <= 2 n_z` and baseline `>= 0`, giving
`E_x U'_i(z) - E_x U^*_i(z) <= l_i(z) + 2 n_z`.

### 6.7 Summation and integration

Sum (6.4), (6.10), (6.12) over `z in X_F` using the identity (6.3), and use
`sum_z n_z <= sum_z V_z = n`:

    u_i(n; S', S^*_{-i} | x) - u_i(n; S^* | x)
      <= sum_z l_i(z) + sum_{z : i in T(z)} [ 1 + 2 b(n_z) + R^dbl_K(n_z) ]
         + sum_{z : i notin T(z)} D_i(z) + 8 n^{-2},

with `D_i(z)` as in the statement of Theorem 1(i). The right-hand side is a deterministic
function of `x` and does NOT depend on `S'_{i,n}`. Averaging over `x` with weights
`Pr(X = x)` gives the first display of Theorem 1(i), and taking the supremum over
`S'_{i,n} in B^ctx+_{i,n}` is then legitimate because the bound is uniform.

For the simplified form, assume `4 s <= delta_i(z)` for every `z` at which `i` is not top.
Then:

* `sum_z l_i(z) <= min{Q L, n}` pathwise, since `l_i(z) <= L` and `sum_z l_i(z) <= sum_z V_z = n`.
* `E[ 2 b(n_z) ] = sqrt(2 ell) E[ sqrt(n_z) ] <= sqrt(2 ell) sqrt( E n_z )` by Jensen, and
  `sum_z sqrt(E n_z) <= sqrt( Q sum_z E n_z ) <= sqrt(Q n)` by Cauchy-Schwarz, so
  `sum_z E[2 b(n_z)] <= sqrt(2 ell Q n)`.
* `R^dbl_K(H) <= 11 sqrt(K H log K) + 11 K log K log_2(2n)` for every `0 <= H <= n` (the case
  `H = 0` holds because the right side is positive), so by the same two steps
  `sum_z E[R^dbl_K(n_z)] <= 11 sqrt(K log K) sqrt(Q n) + 11 Q K log K log_2(2n)`.
* the `1`s contribute at most `Q`, and `R^dbl_K(n_z) <= R^dbl_K(n)` in the non-top terms.

This yields the second display of Theorem 1(i). Finally `L = O(n^{2/3}(log n)^{1/3})`,
`ell = log 2 + 4 log n`, `R^dbl_K(n) = O(sqrt(K n log K) + K log K log n)`, so the leading term
is `min{QL, n} = O(Q n^{2/3} (log n)^{1/3})` and everything else is `O(sqrt(QKn log(Kn)))`,
`O(QK log K log n)` or an instance constant. Since `s -> 0` as `n -> infinity` (indeed
`s = Theta( (log n)^{1/3} n^{-1/3} )`), the hypothesis `4 s <= min_z delta_i(z)` holds for all
`n` beyond an instance threshold `n_0`, which depends only on `K` and on
`min_z delta_i(z)`; for `n < n_0` the trivial bound `2 n <= 2 n_0` applies, an instance
constant. This proves Theorem 1(i). QED

============================================================================================
## 7. Proof of Theorem 1(ii), revenue at `S^*`

All agents play `S^*`. Fix `x` and a profile `z`; we bound the expected sum of delivered
targets on the visits to `z` from below by `V_z M_(2)(z)` minus an error. Recall
`P(n;S) = E sum_t m_{I_t,t}`, so revenue is additive over profiles exactly as utility is.

If `V_z < K L`, all visits are bidding pulls, the delivered targets are the capacities
`M_j(z_j) >= 0`, and we simply charge `V_z M_(2)(z) <= V_z <= min{K L, V_z}`.

Let `V_z >= K L`. The `K L` bidding visits deliver `sum_j L M_j(z_j) >= 0` and we charge
`K L M_(2)(z) <= K L`. For the post-bid visits define
`G^all(z) := { |beta_j(z) - M_j(z_j)| <= s for every j in [K] }`. Every bid is now the mean of
`L` independent Bernoulli`(M_j(z_j))` variables, so
`Pr(G^all(z)^c) <= 2 K exp(-2 L s^2) = 2K/(2 K n^4) = n^{-4}`. Order statistics are 1-Lipschitz
in the supremum norm, so on `G^all(z)`

    | beta_(2)(z) - M_(2)(z) | <= s,   hence  tau_z >= M_(2)(z) - 2 s   and  tau_z <= M_(2)(z),
    tau_z = ( beta_(2)(z) - s )_+ <= ( beta_W(z) - s )_+ <= M_W(z_W),

so the winner's `S^*` primary target is `min{tau_z, M_W(z_W)} = tau_z` if strategic and
`max{mu_W(z_W), tau_z} >= tau_z` if honest. In both cases every primary target at `z` is at
least `tau_z`, hence PATHWISE `sum_{r <= q} m_r >= q tau_z`; no optional stopping is needed,
because we bound delivered targets, not rewards.

For the fallback, Lemma 7 applied with the comparator `j*` attaining `M_*(z)` and
`v = M_*(z) >= M_(2)(z)` gives
`E[ sum_{t in fallback at z} m_{I_t,t} | F_fb ] = E[ sum_{t in fallback at z} Y_t | F_fb ]
>= M_(2)(z) H_z - R^dbl_K(H_z)`. Since `q + H_z = n_z` is deterministic given `x`, and
`tau_z >= M_(2)(z) - 2 s` on `G^all(z)` while `M_(2)(z) - 2 s <= M_(2)(z)`,

    E_x[ post-bid delivered targets at z ]
       >= E_x[ 1{G^all(z)} ( (M_(2)(z) - 2 s) q + (M_(2)(z) - 2 s) H_z ) ] - R^dbl_K(n_z)
       >= ( M_(2)(z) - 2 s ) n_z - n_z n^{-4} - R^dbl_K(n_z),

using `M_(2)(z) - 2 s <= 1` and `Pr(G^all(z)^c) <= n^{-4}`, and revenue `>= 0` on
`G^all(z)^c`. Adding the bidding charge,

    E_x[ delivered targets at z ] >= V_z M_(2)(z)
        - [ min{K L, V_z} + 2 s n_z + R^dbl_K(n_z) + n_z n^{-4} ] .

Summing over `z`, using `sum_z min{K L, V_z} <= min{Q K L, n}`, `sum_z n_z <= n`, and the two
estimates of Section 6.7 for `sum_z E R^dbl_K(n_z)`, then averaging over `x`:

    P(n;S^*) >= E sum_{t<=n} M_(2)(X_t)
              - [ min{Q K L, n} + 2 s n + 11 sqrt(K Q n log K) + 11 Q K log K log_2(2n)
                  + n^{-3} ] .

With `L = Theta(n^{2/3}(log n)^{1/3})` and `s = Theta((log n)^{1/3} n^{-1/3})` this is the
stated rate. QED

Remark. The `n s` term is genuinely part of the mechanism's cost, not of the deviation gain:
the announced price sits up to `2 s` below `M_(2)`, and the mechanism only charges the winner
the announced price. This is the same asymmetry as in the scalar theorem and is the reason
`PRIVATE_BOUND_NOTES.md` Note 1 removes `2 n s` from (i) but not from (ii).

============================================================================================
## 8. Proof of Theorem 1(iii), honest-benchmark robustness

Let `S = (S_1, ..., S_K)` be ANY feasible behavioural profile with `S_j in B^ctx+_{j,n}` and
honest agents honest. Fix `x` and a profile `z`, and choose an honest `h = h_z` with
`mu_h(z_h) = b(z)`.

If `V_z < K L` we charge `V_z b(z) <= min{K L, V_z}` and are done. Let `V_z >= K L`. We charge
the `K L` bidding visits `K L b(z) <= K L`.

Bid concentration for the honest comparator. Agent `h` is pulled exactly `L` times in local
Stage 1 at `z` (by (M1), the Stage-1 schedule is reward-independent, so this holds under every
behavioural profile). On each of those pulls honesty forces `m >= mu_h(z_h) = b(z)`, and the
target is measurable with respect to the global history before the pull. By the martingale
construction of Lemma 5 applied to the `L` bidding pulls of `h` at `z` (increments
`Y - m` with conditional mean zero and conditional range one) and the one-sided
Azuma-Hoeffding bound,

    Pr{ beta_h(z) < b(z) - s } <= exp( - 2 L s^2 ) = (2 K n^4)^{-1}.                     (8.4)

Call the complement `B(z)`. On `B(z)` there are two cases.

* `W = h`. Honesty makes every primary target at `z` at least `b(z)`, so pathwise
  `sum_{r <= q} m_r >= b(z) q >= (b(z) - 2 s) q`.
* `W != h`. Then `beta_h(z)` is not the largest bid, so `beta_h(z) <= beta_(2)(z)` and
  `tau_z >= beta_h(z) - s >= b(z) - 2 s`. On the monitor good event `Mon(z)` of Lemma 5
  (probability at least `1 - n^{-3}`), (5.2) gives
  `sum_{r <= q} m_r = A_q >= q tau_z - 1 - 2 b(q) >= (b(z) - 2 s) q - 1 - 2 b(n_z)`.

In both cases, on `B(z) cap Mon(z)` the primary delivers at least
`(b(z) - 2 s) q - 1 - 2 b(n_z)`.

Fallback. Agent `h` is honest under `S`, so at every fallback pull at `z` its conditional
reward mean is at least `mu_h(z_h) = b(z)`. Lemma 7 with comparator `h` and `v = b(z)` gives
`E[ sum_{t in fallback at z} m_{I_t,t} | F_fb ] >= b(z) H_z - R^dbl_K(H_z)`. This is the step
for which the fresh restart over ALL agents is essential: it is what keeps an honest
comparator eligible after a statistically triggered switch, even though the platform cannot
identify the honest agents. Note also that `S^*` plays no role here; the bound holds when all
`K` agents deviate.

Adding, and charging the two bad events at at most `n_z` each,

    E_x[ delivered targets at z ] >= V_z b(z)
       - [ min{K L, V_z} + 2 s n_z + 1 + 2 b(n_z) + R^dbl_K(n_z)
           + n_z ( (2 K n^4)^{-1} + n^{-3} ) ] .

Summing over `z` and averaging over `x`, using `sum_z E[2 b(n_z)] <= sqrt(2 ell Q n)` and
`sum_z E[R^dbl_K(n_z)] <= 11 sqrt(K Q n log K) + 11 Q K log K log_2(2n)` as in Section 6.7,

    P(n;S) >= E sum_{t<=n} b(X_t)
              - [ min{Q K L, n} + 2 s n + Q + sqrt(2 ell Q n) + 11 sqrt(K Q n log K)
                  + 11 Q K log K log_2(2n) + 3 n^{-2} ] .      QED

============================================================================================
## 9. Proof of Proposition 2

Put `gap := min_z ( M_i(z_i) - V_i(z) ) > 0` and assume `4 s < gap`. The deviation
`S'_{i,n}` delivers the constant `m'(z)` on every Stage-1 pull at `z` and follows `S^*_i`
afterwards; it is measurable with respect to the messages of (M6) (the profile and the local
phase), so `S'_{i,n} in B^ctx_{i,n}`. Feasibility: `m'(z) <= M_i(z_i)` because
`(M_i(z_i)+V_i(z))/2 < M_i(z_i)` and, in the honest case, `mu_i(z_i) < M_i(z_i)` by
hypothesis; honesty: `m'(z) >= mu_i(z_i)` by the definition of `m'` as a maximum.

Couple the two executions as in Section 4.1. Let

    E := { |beta_j(z) - (its constant Stage-1 target)| <= s for every j in [K], every
           z in X_F, in both executions }.

In both executions every Stage-1 target is a constant (`M_j(z_j)` for `j != i`, `M_i(z_i)` in
the baseline and `m'(z)` in the deviation for `i`), so each bid is the mean of `L` independent
Bernoulli variables with that constant mean. There are at most `2 K Q` distinct bid variables
(the `j != i` bids are shared by the two executions by (L3a)), and each violates its band with
probability at most `2 exp(-2 L s^2) = (K n^4)^{-1}`. Hence
`Pr(E^c) <= 2 K Q (K n^4)^{-1} = 2 Q n^{-4}`.

On `E`, at every profile `z`: for `j != i`, `beta_j(z) <= M_j(z_j) + s <= V_i(z) + s`; in the
baseline `beta^*_i(z) >= M_i(z_i) - s > V_i(z) + 3 s > V_i(z) + s`; in the deviation
`beta'_i(z) >= m'(z) - s >= (M_i(z_i)+V_i(z))/2 - s = V_i(z) + (M_i(z_i)-V_i(z))/2 - s
> V_i(z) + 2 s - s = V_i(z) + s`, using `gap > 4 s`. So `i` is the strict largest bidder at
every `z` in both executions, and by (L4c) both face the same price
`tau_{z,i} = ( max_{j != i} beta_j(z) - s )_+`, which by (L3a) is the same random variable in
the two executions.

After local Stage 1 at `z` both executions run `S^*` with the same winner `i`, the same price,
the same local phase, the same priority `pi_z`, the same EXP3 coins and, by (L4d) and the fact
that the winner's `r`-th primary pull at `z` is its local pull `L + r` in both executions, the
same reward seeds. An induction on the visits to `z` therefore shows that on `E` the two
post-bid local executions at `z` coincide pathwise, so their post-bid utilities coincide. On
`E` the only difference is Stage 1, where the deviator saves exactly
`L ( M_i(z_i) - m'(z) ) >= L c` at each of the `Q` profiles (each profile has `V_z >= K L`, so
`l_i(z) = L`). Off `E` the two utilities differ by at most `2 n`. Hence

    u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n) >= c Q L - 2 n . 2 Q n^{-4}
                                                  = c Q L - 4 Q n^{-3}.       QED

============================================================================================
## 10. The six delicate points, settled one by one

### (a) Conditioning on arrivals when the agents may know future arrivals

Settled, and the class is enlarged rather than restricted.

Formally. Let `A := { x in X_F^n : Pr(X = x) > 0 }`, a finite set. For `S'_{i,n} in
B^ctx+_{i,n}`,

    u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)
        = sum_{x in A} Pr(X = x) [ E_x U'_i - E_x U^*_i ]
        <= sum_{x in A} Pr(X = x) G_i(x) = E[ G_i(X) ],

where `G_i(x)` is the deterministic bound of Section 6.7. Three things make this legitimate.

1. By (A1) the seeds `U`, the priorities, the mechanism coins and the private coins are
   independent of `X`, so conditioning on `{X = x}` leaves their joint law and their mutual
   independence unchanged. Every step of Sections 5 to 8 is carried out under `Pr( . | X = x)`
   and uses only that joint law, so nothing is lost.
2. Conditioning HARD-CODES the arrival sequence. A strategy that already knew the whole
   arrival sequence becomes, after conditioning, an ordinary own-history behavioural strategy
   for the deterministic schedule `x`. A strategy that did not know the future becomes a
   special case of the same thing. So the conditional strategy class contains the conditional
   images of both `B^ctx_{i,n}` and `B^ctx+_{i,n}`, and the per-`x` bound, which is uniform
   over ALL own-history behavioural strategies for the schedule `x`, covers them.
3. `G_i(x)` does not depend on `S'_{i,n}`, so the supremum may be taken inside the sum.

Knowing the future arrivals cannot help the deviator learn anything about the reward seeds,
exactly because of (A1): `X` is independent of `U`. That is why the enlargement is free.

Where this would break. If the arrival at round `t` were allowed to depend on past rewards
(endogenous arrivals), conditioning on `{X = x}` would tilt the law of `U`, the freshness
property (F1) would fail, and both Lemma 5 and Lemma 6 would collapse. The hypothesis in (A1)
is the exact hypothesis the manuscript already uses for the first four parts of
`thm:finite-context` (contract Section 11 item 6: "exogenous arrivals independent of reward
tapes"); Local-MESP needs nothing more. In particular i.i.d. arrivals are NOT needed anywhere
in Theorem 1, and no mass condition is needed either; contrast the public part of
`thm:finite-context`, which does need i.i.d. positive masses.

A second consequence of conditioning that the proof genuinely uses: given `{X = x}`, the local
fallback length `H_z` and each epoch's realised length `H'_k` become deterministic once the
fallback start is known. That is what makes Lemma 6 applicable with `H'` measurable at the
epoch start. Without conditioning on arrivals, `H'_k` would be a stopping time and the epoch
lemma would need an optional-stopping argument. Points (a) and (b) therefore interact: (a) is
what buys (b).

### (b) The per-epoch EXP3 lemma proved from the manuscript's own lemma, and the constant

Settled by Lemmas 6 and 7. The four things that had to be checked:

1. Truncation. The epoch is tuned to its PLANNED length `B = 2^k` but may realise a shorter
   `H' <= B`. The potential inequality (6.2) is obtained by summing a per-round inequality, so
   it holds verbatim for any prefix `H'`. Nothing in the argument requires the sum to reach
   `B`. The loss bound `2 gamma_k H' + K log K/gamma_k <= 2 gamma_k B + K log K/gamma_k` then
   gives exactly `R_K(2^k)` by the manuscript's own case split.
2. Measurability of `H'`. Needed so that `v H'` may be pulled out of the conditional
   expectation. Supplied by conditioning on arrivals, see (a).
3. Reactive selected agents and the global filtration. The estimator identities
   `E[hat Y_{l,t} | F_{t-1}] = r_{l,t}` and `E[hat Y_{l,t}^2 | F_{t-1}] = r_{l,t}/p_{l,t}` are
   proved against the GLOBAL filtration of Section 4.3, so a deviator that chooses its
   fallback target using its history at other profiles is covered. The comparator condition is
   `E[Y_t | F_{t-1}, I_t = j] >= v`, which the non-deviating agents satisfy exactly because
   `S^*` delivers capacity in the fallback; no counterfactual rewards for unselected agents
   are needed.
4. The absolute constant. With `m = floor(log_2 H) + 1` epochs,

       sum_{k=0}^{m-1} 3 sqrt(K 2^k log K) <= 3 sqrt(2)/(sqrt(2)-1) . sqrt(K H log K),
       3 sqrt(2)/(sqrt(2)-1) = 10.24264069 ...,
       sum_{k=0}^{m-1} 2 K log K <= 2 K log K log_2(2H),

   so `C_0 = 11` works in `R^dbl_K(H) = C_0 ( sqrt(K H log K) + K log K log_2(2H) )`. The
   ledger's assertion "the doubling sum of `R_K(2^k)` over epochs gives `C_0 <= 11`" is
   confirmed, and `10.2427` is the exact constant of the square-root part. A brute-force check
   (Section 11, test T1) verified `sum_{k<m} R_K(2^k) <= R^dbl_K(H)` for every `2 <= K <= 50`
   and every `1 <= H <= 20000`, with no violation.

Nothing is cited. In particular I do NOT import EXP3.1 or any other published doubling trick,
and I make no claim about what published doubling variants do; Lemma 6 is proved from the
potential argument that the manuscript's `lem:selected-reactive-exp3` already contains.

### (c) A deviator that uses one profile's history to time deviations at another

Settled, and written with the global filtration explicit. The attack to keep in mind: the
deviator watches profile `z'`, waits until its local instance there has entered fallback (or
until its own accumulated monitor slack at `z'` is large), and only then dumps its target at
`z`. Four separate mechanisms would have to be checked, and each is closed:

1. Utility accounting. The decomposition (6.3) is an exact identity, obtained from the
   partition of the rounds by profile and from linearity of expectation. No independence
   across profiles is needed or claimed. Correlations that the deviator induces between the
   profiles are irrelevant to a sum of per-profile expectations.
2. Bid domination. (L4a) is a POINTWISE inequality between indicator functions on the same
   seed, `1{U_{z,i,k} <= m'} <= 1{U_{z,i,k} <= M_i(z_i)}`. It holds for any realised value of
   `m'`, hence for any rule generating it, measurable or not with respect to anything. Timing
   the bid using another profile's history changes nothing.
3. Monitoring. Lemma 5 is stated for targets `m_r` that are measurable with respect to
   `H_{r-1} = sigma(all primitives except the seeds of the current and later primary pulls at
   z)`. That sigma-field contains the whole global history, the whole arrival sequence, and
   every other profile's data. So a rule "dump at `z` as soon as `z'` falls back" is inside
   the quantifier of Lemma 5, and the bound `A_q >= q tau_z - 1 - 2 b(q)` is unaffected.
4. Fallback. Lemma 6, item 3 above.

There is exactly one cross-profile channel the mechanism itself provides, namely the messages
of (M6): the deviator learns `tau_{z'}` and can infer something about the other agents'
capacities at `z'`. This is information, and every bound above is uniform over rules that use
it, so it buys nothing.

What the deviator cannot do, and why: it cannot change the number of visits to `z` (arrivals
are exogenous), it cannot change the number of Stage-1 pulls it receives at `z` (the Stage-1
schedule (M1) is reward-independent), it cannot change any other agent's bid at `z` (L3a), it
cannot change the price it faces at `z` (L3b, L4c), and it cannot change any local quantity at
`z'` by acting at `z` (L3c).

### (d) Whether triggering the fallback at one profile can change prices elsewhere

Settled: it cannot. This is Lemma 3, in particular (L3b) and (L3c). The local instance at `z'`
consumes only the visits to `z'`; its parameters `L`, `s`, `b(.)` are deterministic functions
of the global `n`; all its randomness (`{U_{z',j,k}}`, `pi_{z'}`, its EXP3 coins) is
independent of everything at `z`; and every non-deviating agent plays a LOCAL-MARKOV rule that
reads only `(z', local phase at z', tau_{z'})`. So `beta_j(z')` for `j != i` is literally
`L^{-1} sum_k 1{U_{z',j,k} <= M_j(z'_j)}`, and the price the deviator faces at `z'`, namely
`tau_{z',i} = ( max_{j != i} beta_j(z') - s )_+`, is a function of the seeds
`{U_{z',j,k} : j != i, k <= L}` alone.

One honest qualification. The ANNOUNCED price `tau_{z'} = (beta_(2)(z') - s)_+` does depend on
the deviator's own bid at `z'` when the deviator loses there, because then its bid can be the
second largest. This matters only in the losing branch, and it is the branch where a real
attack could have lived: the deviator could try to bid so high that the announced price
exceeds the winner's capacity, forcing the winner to fail the monitor and opening a fallback
in which the deviator gets selected. Section 6.4 closes it: if `i` loses then `i` is not a
largest bidder, so `beta_(2)(z') <= beta_W(z')`, and on `G(z')` this gives
`tau_{z'} <= M_W(z'_W)`; the winner therefore meets the price and (5.3) bounds the fallback
probability by `(2 n^3)^{-1}`. A random check of this inequality over 200000 random
configurations found no violation (Section 11, test T3).

### (e) `K = 2` and capacity ties within a profile

Settled; nothing special is needed, but the places where a tie could have mattered are these.

* `K = 2`. The second order statistic with multiplicity of a two-vector is its minimum, and on
  `{i wins}` it equals `beta_j` for the single `j != i`, which is the general identity used in
  (L4c). `V_i(z) = M_j(z_j)`, and `M_(2)(z) = min_j M_j(z_j)`. In Lemma 6, `K = 2` gives
  `log K = log 2 > 0`, so `gamma_k` and `R_K` are well defined; `K >= 2` is used only through
  `log K > 0`.
* Bid ties. Bids are multiples of `1/L`, so exact ties have positive probability and must be
  handled. They are, by the single uniform priority permutation `pi_z` drawn once per profile
  and SHARED by the two coupled executions. The proof of (L4b) treats the tie case explicitly
  and never uses a strict inequality. A random check over 400000 configurations with bids
  forced onto the grid `{0, 1/L, ..., 1}`, so that ties are frequent, found no violation of
  (L4b) or (L4c) (Section 11, test T3).
* Capacity ties within a profile. If `M_i(z_i) = M_j(z_j) = M_*(z)` for `i != j`, then both are
  in `T(z)`, `delta_i(z) = delta_j(z) = 0`, and both are handled by the TOP branch of Section
  6.5, which needs only `tau_{z,i} <= V_i(z) <= M_i(z_i)` and tolerates equality. The non-top
  branch is invoked only when `delta_i(z) > 0` strictly, so the boundary case is never
  assigned to it. For the revenue statement, `M_(2)(z)` counts ties, so a tied top makes
  `M_(2)(z) = M_*(z)` and the benchmark is the full first-best at that profile, which is
  exactly the scalar theorem's behaviour. A full tie `M_1(z_1) = ... = M_K(z_K)` is the
  extreme case and is covered by the same lines.
* A knife-edge remark. When `delta_i(z) = 0` the deviator is top at `z` and there is no
  positive-gap argument to bound its primary tenure; none is needed, because the top branch
  bounds the gain by the monitor slack and the fallback regret, not by a tenure bound. The
  non-top branch's instance threshold `4 s <= delta_i(z)` therefore never has to be applied at
  a tie.

### (f) Profiles with tiny mass where bidding never completes

Settled, and pathwise. By (M5) a profile with `V_z < K L` spends all its visits in local Stage
1. Three claims:

1. The number of Stage-1 pulls agent `i` receives at `z` is `l_i(z)`, a deterministic function
   of `V_z` and of the fixed permutation `sigma_z`. It is the SAME in the deviating and the
   baseline executions, by (L4d). A deviator cannot buy itself extra pulls at a low-mass
   profile.
2. On each such pull the baseline delivers `M_i(z_i)` and the deviation delivers some
   `m' in [0, M_i(z_i)]`, so the per-pull utility difference is at most `M_i(z_i) <= 1`, and
   the whole profile contributes at most `l_i(z) <= min{L, V_z}` to (6.3), PATHWISE. No
   probabilistic argument, no good event, no error term.
3. Summing, `sum_z l_i(z) <= min{Q L, n}`. So the harvest over many tiny profiles is exactly
   the `Q L` term that the theorem already carries, and by Proposition 2 that term is real,
   not an artefact.

For revenue and robustness the same profiles are charged `min{K L, V_z}` and summed to
`min{Q K L, n}`. Profiles that are never visited contribute nothing and need no conditional
quantity, exactly as zero-mass cells do in the contract's Section 3.

One more variant worth naming: a profile with `K L <= V_z` but `n_z = V_z - K L` small, say
`n_z = 0` or `1`. Then `b(n_z)` and `R^dbl_K(n_z)` are `O(sqrt(ell))` and `O(sqrt(K log K))`
respectively, and the top-branch bound (6.10) degenerates gracefully to
`l_i(z) + O(1 + sqrt(log n) + sqrt(K log K))`; the local fallback with `H_z = 0` contributes
`R^dbl_K(0) = 0`. Nothing in the proof divides by `n_z` or `V_z`.

============================================================================================
## 11. Numerical attempts to falsify the intermediate claims

All scripts and raw outputs are in
`<scratchpad>/round2/prover1-c2/` (`exp3_doubling.py`, `monitor.py`, `award_checks.py`,
`localmesp.py`, and the corresponding `out_*.txt`). They were run with the round-2 venv on the
login node, single core; see `COMPUTE_LOG.md` in this directory. These are simulations, not
proofs: a passing test is evidence that a claim is not obviously false, and a learned or
searched deviation is only a LOWER bound on exploitability for the class tested. None of them
is offered as evidence of equilibrium.

**T1, the doubling EXP3 bound (Lemma 6 and Lemma 7).** One local fallback of length `H`, agent
`0` the comparator delivering mean `v` when selected, every other agent delivering `0` when
selected (worst case for total reward), doubling epochs exactly as in (M4) with `gamma_k`
tuned to the planned `2^k`. Grid `K in {2,3,5,10}`, `H in {1,2,3,7,8,15,31,100,511,1000,4096,
10000}`, `v in {0.3,0.7,1.0}`, 120 to 400 repetitions each. Result: 0 violations of
`v H - E sum Y <= R^dbl_K(H)`; the worst observed ratio of the empirical shortfall to
`R^dbl_K(H)` was `0.3195`. Separately, the ANALYTIC inequality
`sum_{k=0}^{floor(log2 H)} R_K(2^k) <= R^dbl_K(H)` with `C_0 = 11` was checked by brute force
for every `2 <= K <= 50` and every `1 <= H <= 20000`: 0 violations. This is the check of the
constant demanded by the ledger.

**T2, the anytime monitor (Lemma 5).** For `n in {200, 2000}`, `tau in {0.3, 0.6, 0.9}` and
three predictable target policies, including a "bank the slack" policy that delivers `0`
whenever the cumulative reward is still above the next boundary, 4000 repetitions each: the
inequality `A_q >= q tau - 1 - 2 b(q)` on the non-crossing event was never violated (maximum
observed violation `0.0000`), and no boundary crossing was observed at all (the bound is
`n^{-3}`, so this is consistent but uninformative about the exponent). The non-top primary
length bound (6.11) was checked for `n in {2000, 20000}` and `delta in {0.1, 0.2, 0.4}` with a
winner of capacity `tau - delta/2`, 3000 repetitions each: the maximum realised tenure was
always below `4(1+sqrt(2 ell))^2/delta^2`, with slack factors between 1.6 and 12.

Note what T2 does NOT show: it does not show the `2 b(n_z)` term is attained. The "bank" policy
is a bad deviation, because refusing to deliver makes the cumulative requirement `r tau` grow
while the cumulative reward stalls; it gets switched off and loses the primary. The profitable
shading found in T4 is the smooth one, `m_r = tau - c/sqrt(r)`.

**T3, the award rules (Lemma 4 and the losing-branch price claim).** 400000 random
configurations with `K in {2,...,6}` and bids forced onto the grid `{0, 1/L, ..., 1}` with
`L <= 7`, so that exact ties are frequent, and a uniform priority permutation: 0 violations of
(L4b) (deviating win implies baseline win), 0 violations of (L4c) (both executions then face
`max_{j != i} beta_j`), and 0 cases with `beta_(2) > beta_W`. A further 200000 random
configurations with `|beta_j - M_j| <= s` for `j != i` and an arbitrary bid for `i`: 0 cases
with `tau_z > M_W(z_W)` when `i` loses. This is the check that the deviator cannot price the
winner out of the primary phase.

**T4, full Local-MESP with cross-profile deviators.** Exact event-level simulation of the
mechanism of Section 2 with `n = 6000`, `L = 705`, `s = 0.1602`, on a common coupling (same
seed array, same priorities, same EXP3 coins in the baseline and the deviating execution), 60
repetitions per configuration, 12 deviations including two that explicitly condition the
target at one profile on whether the OTHER profile has fallen back. Six scenarios:

    scenario                                                  best mean gain   Theorem 1(i) bound
    A  top at z1, far non-top at z2, alternating arrivals            242.0            5441.7
    B  deviator top at BOTH profiles                                 364.0            3471.6
    C  capacity tie M_0(z2) = M_1(z2), K = 2                         402.3            3471.6
    D  Q = 3, i.i.d. arrivals, one profile with V_z = 63 < K L       375.1            3473.3
    E  deviator honest with mu_0(z1) = 0.60 above the price          253.3            3471.6
    F  K = 3, top at z1 and non-top at z2                            291.8            7360.5

No configuration produced a mean gain above the bound; the best deviation found was always a
combination of Stage-1 underbidding (which realises the `L (M_i - m')` per profile of
Proposition 2) with smooth primary shading `m_r = tau - 1.5/sqrt(r)` (which eats into the
`2 b(n_z)` monitor slack). The cross-profile timed deviations never beat the profile-by-profile
ones, which is what Section 10(c) predicts. Scenario D is the test of delicate point (f):
the low-mass profile contributed exactly `l_0(z) = 63` to the bidding part of the bound, and
the measured gain there matched the pathwise argument. Scenario C is the test of delicate
point (e). Scenario E exercises the honest branch with `tau_{z,i} <= mu_i(z_i)`.

Caveat on T4. At `n = 6000` the non-top scope condition `4 s <= delta_i(z)` is severe
(`4 s = 0.64`), which is why scenarios A and F needed capacity gaps of `0.65` and `0.77` to
exercise the non-top branch at all. This is the finite-`n` scope limitation recorded in
`PRIVATE_BOUND_NOTES.md` Note 3, inherited verbatim by Theorem 1. The simulations therefore
cannot probe the non-top branch at realistic gaps, and I do not claim they do.

============================================================================================
## 12. Departures from the ledger's plan, and why

1. **Larger deviation class.** The ledger's Theorem targets `B^ctx_{i,n}`. I prove Theorem 1(i)
   for `B^ctx+_{i,n}`, in which the deviator also knows the entire arrival sequence. Reason:
   the conditioning step of (a) is cleanest when the class is already closed under hard-coding
   the arrivals, and the enlargement costs nothing. The result for the ledger's class follows
   by inclusion.

2. **Stage-1 order fixed and reward-independent (M1).** The ledger says "agents in a fixed
   reward-independent order"; I make this a hypothesis and use it twice, in (L4d) and in
   Section 10(f). Without it, the deviator's number of bidding pulls could depend on its own
   behaviour and the pathwise bound `l_i(z)` would fail. This is not a change of substance,
   only a promotion of a phrase to a hypothesis.

3. **Explicit epoch schedule (M4).** The ledger says "doubling epochs of planned local lengths
   `2^0, 2^1, ...`". I fix that epoch `k` covers local fallback clock `2^k, ..., 2^{k+1}-1` and
   that `gamma_k` is tuned to the PLANNED `2^k`, not to the realised length. The realised-length
   tuning is not implementable (the platform does not know how many more visits the profile
   will get), and the planned-length tuning is what Lemma 6 is proved for.

4. **Phantom continuation in Lemma 5.** The manuscript's `lem:private-monitor` is stated
   "conditional on the bidding history" and uses a union bound over `r <= n` without saying on
   what filtration the martingale lives once the primary phase has ended. With a globally
   adaptive deviator this needs care. I construct the extension explicitly on the same
   probability space, with the filtration `H_r` that removes only the not-yet-consumed primary
   seeds. This is a strengthening of the manuscript's lemma, not a repair of an error in the
   scalar case, but it IS needed for the contextual case, where the deviator's target at `z`
   may depend on everything happening at other profiles.

5. **Self-contained Azuma (Lemma 4b).** To avoid importing any theorem I have not verified, I
   state and prove the exact concentration inequality used, from Hoeffding's lemma. This also
   fixes the constant: each tail is `exp(-2 b(r)^2/r) = (2 n^4)^{-1}`, so the union over `r<=n`
   and two tails gives `n^{-3}`, matching the manuscript.

6. **The revenue argument avoids optional stopping.** The manuscript's revenue proof invokes a
   bounded stopping time and `E[sum_{r<=q}(Y_r - m_r) | F_bid] = 0`. Since
   `P(n;S) = E sum_t m_{I_t,t}` (an identity for a deterministic horizon), I bound delivered
   TARGETS directly and use `m_r >= tau_z` pathwise. One fewer step to check.

7. **Per-profile bound refined from `L` to `l_i(z)`.** The ledger charges `L` per profile. I
   charge `l_i(z) = min{L, (V_z - (sigma_z^{-1}(i)-1) L)_+}`, which gives
   `sum_z l_i(z) <= min{Q L, n}` and so keeps the bound nontrivial when `Q L` exceeds `n`.

8. **The ledger's display (i) double counts.** The ledger adds `sum_z [2 b(V_z) + R^dbl_K(V_z)]`
   over ALL profiles and then adds the non-top terms on top. That is a valid upper bound
   because every term is nonnegative, but it is not the bound the proof produces. Theorem 1(i)
   states the per-profile form (top term at top profiles, non-top term at non-top profiles)
   and derives the ledger's form as a weakening.

9. **The "o(n) iff `Q = o(n^{1/3}(log n)^{-1/3})`" claim.** The ledger states this as an
   equivalence. The upper bound gives only the "if". I prove the converse direction as far as
   I can, in Proposition 2, which needs `Q K L <= n` and a unique top at every profile and
   delivers `c Q L` with an instance constant `c`. I do NOT claim a matching lower bound for
   arbitrary instances, and I do not claim that MESP-type mechanisms in general cannot do
   better; the statement is about Local-MESP as specified.

10. **Non-top instance threshold made explicit.** The ledger says "for `n` with
    `2 s <= delta_i(z)/2`". I use the equivalent `4 s <= delta_i(z)` and state the alternative
    trivial branch explicitly rather than "absorbed into instance constants", so that the
    theorem is a true statement at every `n` and not only asymptotically.

11. **No claim about published doubling variants.** The ledger's dependency list mentions that
    Auer, Cesa-Bianchi, Freund, Schapire (2002) EXP3.1 uses a different doubling rule. I make
    no assertion about EXP3.1 in this document, because I did not verify it against the
    primary source; I prove what I need from the manuscript's own lemma, as the ledger
    instructs.

============================================================================================
## 13. What I did NOT establish, and the steps I consider least secure

### 13.1 Not established

1. **The continuous (grid) extension.** Nothing in this document says anything about
   `X = [0,1]^D`, cells, or Lipschitz capacities. The ledger's obstruction paragraph for the
   continuous private extension stands untouched. Local-MESP is a finite-profile result.
2. **Tightness of anything except the `Q L` term.** Proposition 2 shows `Q L` is attained up to
   the instance factor `c` and only when `Q K L <= n` and every profile has a unique top. I did
   NOT prove that the `sqrt(Q n log n)` monitor-slack term or the `sqrt(K Q n log K)` fallback
   term is attained. Simulation T4 found smooth shading gains of order `100` at a profile with
   `n_z = 1590` against a slack allowance `2 b(n_z) = 343`, which is suggestive and nothing
   more. The remark in `PRIVATE_BOUND_NOTES.md` Note 2 about a `b_n(N_n)` Stage-2 gain remains
   unproved here too, and must not be stated as a theorem.
3. **Optimality in `Q` or in `n`.** No lower bound over mechanisms is proved. The statement
   "`o(n)` iff `Q = o(n^{1/3}(log n)^{-1/3})`" is proved only in the direction supplied by
   Theorem 1(i), plus the partial converse of Proposition 2 in the regime `Q K L <= n`.
4. **Exact (non-additive) equilibrium, and revenue in every equilibrium.** Theorem 1(i) is an
   additive asymptotic statement about unilateral deviations from `S^*`. It does not say `S^*`
   is an exact equilibrium, and it does not say that every equilibrium has high revenue. The
   scalar manuscript's closing caveat applies verbatim.
5. **Endogenous arrivals.** If the arrival process may depend on past rewards, Theorem 1 is
   false as proved and I have no repair; see Section 10(a).
6. **Anytime guarantees.** `n` is known to the platform and used in `L`, `s`, `b(.)` and in the
   confidence levels. Nothing here is anytime in the global horizon. (The mechanism IS anytime
   in each LOCAL horizon, which is the point of the doubling fallback.)
7. **Richer agent observations.** Agents do not observe other agents' histories or the global
   round. If they did, `S^*` would still be feasible but Lemma 3 would need rechecking, since
   the non-deviators' behaviour would then be allowed to depend on other profiles.
8. **Multiple simultaneous deviators in the incentive statement.** Part (i) is unilateral.
   Part (iii) does allow all `K` agents to deviate, but it is a revenue statement, not an
   incentive statement, and it is against the honest benchmark `b`, not against `M_(2)`.
9. **Any external result.** I verified no paper against a primary source, because I import
   none. The only external facts used are Hoeffding's lemma and Hoeffding's inequality.
10. **The correctness of the manuscript's scalar theorem.** I reuse the STRUCTURE of the scalar
    proof and the tightened top-agent bound of `PRIVATE_BOUND_NOTES.md`, but I reprove every
    lemma I actually use (Lemmas 4b, 5, 6, 7, 8 above). If the scalar theorem has a defect
    outside those lemmas, this document does not inherit it, and it does not repair it either.

### 13.2 Steps I consider least secure, in decreasing order of my own doubt

1. **The phantom continuation and the filtration `H_r` in Lemma 5.** This is the single most
   technical step. Two things have to be right: the excluded index set of `H_r` must be
   deterministic (it is, because all `K` agents' post-bidding seeds at `z` are excluded, not
   only the winner's, which would make the definition circular), and the seeds `U_{z,j,L+r'}`
   with `r' > q` are consumed twice, once by the phantom process and once by the real fallback
   pulls at `z`. I argue this is harmless because `H_r` is generated by primitives rather than
   by the history, but an adversary should attack exactly here. A safe fallback if the
   construction is judged defective: enlarge the probability space with a second independent
   uniform array used only by the phantom continuation. That changes no constant and makes the
   double consumption disappear, at the cost of saying that the extension lives on a product
   space. I did not write that version because I believe the one above is correct.
2. **The measurability of the realised epoch length `H'_k` at the epoch start (Lemma 6).** This
   is bought by conditioning on arrivals, and it is the one place where points (a) and (b)
   are not independent of each other. If someone objects to conditioning on arrivals, Lemma 6
   must be redone with `H'` a stopping time, which I have not done. I believe conditioning is
   airtight (Section 10(a)), but the dependency is worth naming.
3. **The cancellation in Section 6.5.** The top-agent bound works because the deviating post-bid
   utility and the baseline post-bid utility are both driven by the SAME coefficient
   `1 + mu_i(z_i) - tau_{z,i}`, one from the monitor and one from `S^*`'s primary target. This
   is the tightened accounting of `PRIVATE_BOUND_NOTES.md` Note 1. It depends on
   `tau_{z,i} <= V_i(z) <= M_i(z_i)` holding on `G(z)`, and therefore on the price being
   deviation-independent (L3b) and on `i` being top. If a reader disagrees with (L3b), the
   whole top branch degrades to the manuscript's older bound with an extra `2 n_z s` per
   profile, that is an extra `2 n s` overall, which is `O(n^{2/3}(log n)^{1/3})` and does NOT
   change the rate. So this step is safe in the sense that its failure costs a constant factor,
   not the theorem.
4. **`S^*` is LOCAL-MARKOV (Lemma 3).** This is a property of the proposed profile and of the
   message set (M6), both of which I fixed as hypotheses. If the mechanism revealed anything
   global to the agents and `S^*` used it, (L3a) and hence (L3b) would fail and delicate point
   (d) would reopen. This is a hypothesis, not a proof step, but it is the hypothesis a reader
   is most likely to violate when re-specifying the mechanism.
5. **The non-top branch's finite-`n` scope.** The branch is vacuous until `4 s <= delta_i(z)`,
   which for gaps of order `10^{-2}` is far beyond any simulable horizon
   (`PRIVATE_BOUND_NOTES.md` Note 3, confirmed by the parameters in Section 11 T4, where
   `4 s = 0.64` at `n = 6000`). The theorem is correct as stated, but the non-top guarantee is
   not observable, and the paper must say so. I would put this in the limitations paragraph
   verbatim.
6. **The constant `8 n^{-2}` in Theorem 1(i).** It comes from adding bad-event costs across
   disjoint branches without tracking which branch is active, which is wasteful but valid. I
   did not try to make it tight, and a reader recomputing it may get a different small constant.

### 13.3 One sentence of self-assessment

I believe Theorem 1(i), (ii), (iii) and Proposition 2 are proved as stated under (A1), (A2),
(M1) to (M7), and I found no attack on them; but I did not succeed in falsifying them either
by argument or by the simulations of Section 11, and the absence of a counterexample is not a
proof, so the right reading of this document is: here is a complete chain of implications,
each of which a reader with the scalar proof in hand can check, together with an explicit list
of the places I would attack first.
