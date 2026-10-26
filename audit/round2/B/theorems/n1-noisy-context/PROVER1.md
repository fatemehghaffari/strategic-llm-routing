# STATUS: DONE

Running status: DONE 29 Sep 2026. All parts written; numerics in prover1/.

# N1, Prover 1: CL-MESP keyed on the classifier label (variant D), Theorem N and Proposition I

Role: Prover 1, written in isolation (no PROVER2 file read). Sources read: `SCOUT.md` (for the
statements only), `c2-local-mesp/PROVER1.md` (all), `c2-local-mesp/ADVERSARY.md` Sections 0 to 4,
`f1-continuous-private/PROVER2.md` Section 20, `f1-continuous-private/FINAL.md` Sections 0 to 5,
`sections/app_contextual_private.tex` lines 1 to 696 (the canonical finite-context proof,
`prop:ctx-finite-exact`). No canonical file was modified. No em dash and no triple hyphen appears
in this file. Scripts and outputs: `n1-noisy-context/prover1/`.

Conventions. `log` natural, `(x)_+ = max(x,0)`, `[K] = {1..K}`, `1{.}` indicator. "The paper"
means `sections/app_contextual_private.tex`; "c2P1" means `c2-local-mesp/PROVER1.md`.
Which mechanism: the task names the finite-context private mechanism of `thm:ctx-private-finite`.
Its canonical form in the paper (CL-MESP: round-robin Stage 1, round-indexed seeds, one fallback
EXP3 tuned once to `n`, no doubling) differs in inessential details from c2P1's Local-MESP
(block Stage 1, seed array indexed by local pull, doubling fallback). I prove everything for the
paper's form, because that is what goes into the paper, and I say at each lemma what c2P1 does.
The cost is linear (the paper's `phi_i = id`, `Lambda = 1`); Section 16 says what changes for a
general cost.

============================================================================================
## 0. Summary

Proved in this file (subject to the adversarial reading this file invites):

* **Theorem N (A)**: additive behavioural equilibrium of the label-level profile `S*_N`, with
  exactly the constants of the paper's `prop:ctx-finite-exact`(i) after replacing contexts by labels
  (`Q -> Q_B`) and every capability or mean by its posterior mixture. The deviation class is
  larger than the scout's: the deviator may condition on the entire label path, the round index,
  and everything realised in the past, including all past true types (not only those of its own
  selections), all past seeds and all other agents' private coins. It may not see future true
  types, and Section 3 explains why that exclusion is a hypothesis, not a proof artefact.
* **Theorem N (B)**: revenue against `E sum_t Mbar_(2)(B_t)`, with the paper's error terms. When
  the labels name types (`Lab = A`), `E sum_t Mbar_(2)(B_t) >= E sum_t M_(2)(X_t) - epsbar n
  max_a M_(2)(a)`, where `epsbar` is the average misclassification probability. **This improves
  the scout's `2 eps` to `eps max_a M_(2)(a) <= eps`, and the new constant is attained exactly**
  (the scout's own example; ratio 1.0000 in 2 x 10^5 random instances, `prover1/bench_check.py`).
* **Theorem N (C)**: honest-benchmark robustness against every joint profile, against
  `E sum_t bbar(B_t)`; equal to `E sum_t b(X_t)` with one honest agent (tower), and within
  `epsbar n max_a b(a)` in general when `Lab = A` (scout: `2 eps`).
* **Theorem N (Conv)**: a winner that is label-level compliant is switched to fallback with
  probability at most `(2Kn^4)^{-1} + V_b (2n^4)^{-1}` at label `b`, **whatever the other `K - 1`
  agents do**; summed, at most `Q_B (2Kn^4)^{-1} + (2n^3)^{-1}`.
* **Theorem N (D)**: rates unchanged, `Q_B` in place of `Q`.
* **Corollary L (D-learn)**: the same four parts for the profile in which no one knows the
  posterior, with an extra `2 kappa_n n` in (A) (scout: `n gamma`; I get a factor 2 and explain
  why) and extra failure mass `O(K n^{-3})`.
* **Proposition I**: a mechanism-independent exact identity. For every label-measurable mechanism,
  on an explicit instance with two exogenous true-type paths `P1` (violating (N)) and `P2`
  (satisfying (N)), `G + P = D`, where `G` is the shading gain on `P2`, `P` is the number of
  allocations withheld from a pointwise-compliant winner on `P1`, and `D` is that winner's
  delivered mass on the second-half label-`a` rounds of `P2`. For CL-MESP, `D >= (1/2 - 2 s_n)
  eps n/2 - n^{-2}` and Theorem N(A) gives `G = o(n)`, so `P >= eps n/4 - o(n)`: **the
  pointwise-compliant winner loses order `eps n` allocations on `P1`.** A direct remark shows it is
  in fact convicted with probability tending to one.

Changes to the scout's statements (details in Section 17): the benchmark constants (improved and
made tight); the D-learn constant (`n gamma` becomes `2 kappa_n n`); Proposition I is restated as
an identity, because the scout's corollary ("shading earns 1 per allocated second-half label-`a`
round, deliver 1/2 earns at most 1/2") omits allocations at the OTHER label, through which a
general mechanism can punish, and with them included the scout's inequality does not follow; the
three types `a, c, d` need a class map (labels name classes of types, `d` in class `c`), otherwise
type `d` has misclassification probability one; and the shading strategy must read the round index
(or simulate the `P1` history), which the scout's class did not provide.

Least secure step (Section 15): the canonical-coupling lemma (Lemma C), specifically that the
two executions compared in part (A) may be put on one space with the SAME true types, which is
where (N) is load bearing and where a deviator's knowledge of past true types enters. I give a full
proof; its failure mode and what survives are in Section 15.

============================================================================================
## 1. Model

### 1.1 Primitives

* Agents `j in [K]`, `K >= 2`; horizon `n >= 2K` known to the platform.
* A finite set `A` of true types and a finite set `Lab` of labels, `Q_B := |Lab|`.
* Agent `j` has capability `M_j : A -> [0,1]` and intrinsic mean `mu_j : A -> [0,1]` with
  `mu_j <= M_j` pointwise. A nonempty honest set `K_H` is fixed.
* A posterior kernel `pi = (pi_b)_{b in Lab}`, `pi_b` a probability on `A`. In the classifier
  reading, `pi_b(a) = P(X = a | B = b)`; the theorem uses only the kernel.
* Cost is linear: a selected agent with target `m` at true type `a` has per-selection utility
  `1 + mu_j(a) - m in [0, 2]`.

Round `t <= n`: a label `B_t` and a true type `X_t` are attached to the query. The platform
observes `B_t`; it never observes `X_t`. The platform selects `I_t`; agent `I_t` observes `B_t`,
`X_t` (it reads the prompt) and the mechanism's message, and chooses `m_{I_t,t} in
[0, M_{I_t}(X_t)]`; the platform observes `Y_t = 1{U_t <= m_{I_t,t}}`. Utilities and revenue

    u_i(n;S) = E_S sum_t 1{I_t = i} (1 + mu_i(X_t) - m_{i,t}),    P(n;S) = E_S sum_t Y_t.

Posterior-mixture primitives, for `b in Lab`:

    Mbar_j(b) := sum_a pi_b(a) M_j(a),      mubar_j(b) := sum_a pi_b(a) mu_j(a),
    Mbar_*(b) := max_j Mbar_j(b),           Tbar(b) := { j : Mbar_j(b) = Mbar_*(b) },
    Mbar_(2)(b) := second largest of (Mbar_1(b), ..., Mbar_K(b)) counting multiplicity,
    Vbar_i(b) := max_{j != i} Mbar_j(b),    deltabar_i(b) := Vbar_i(b) - Mbar_i(b),
    bbar(b) := max_{h in K_H} mubar_h(b).

True-type versions `M_(2)(a)`, `b(a) := max_{h in K_H} mu_h(a)` as in the paper. When `Lab = A`
(the classifier outputs a type), put `e_b := 1 - pi_b(b)` and
`epsbar := n^{-1} sum_{t<=n} P(X_t != B_t)`.

### 1.2 Every random draw, listed

This list is complete for the mechanism of Section 2; Section 3 quantifies over it.

| # | draw | when | who draws | specified law |
|:-|:-|:-|:-|:-|
| D0 | label path `B = (B_1..B_n)` | before round 1 (exogenous) | nature | arbitrary law, jointly with D1 |
| D1 | private coin arrays `theta = (theta_1..theta_K)` | before round 1 | agents | arbitrary law jointly with `B` |
| D2 | true type `X_t` | round `t`, first | nature | `pi_{B_t}` |
| D3 | priority `Pi_b`, a permutation of `[K]` | round `t`, if `B_t = b` is first met at `t` | mechanism | uniform |
| D4 | fallback selection `I_t` | round `t`, if `B_t`'s local phase is Stage 3 | mechanism | `p_t`, the EXP3 law of `B_t`'s state |
| D5 | reward seed `U_t` | round `t`, after the target | nature | Uniform`[0,1]` |

Not draws: Stage-1 and Stage-2 selections (deterministic functions of the label's state),
targets (a function of the selected agent's information and its coin array), rewards
(`Y_t = 1{U_t <= m}`), messages, bids, prices, switches. Tie-breaks: the only randomised tie-break
is D3 (bid ties at the award). Every other tie (the water-filling level, see Section 2.2) is broken
by a deterministic rule stated with the rule. Agents' per-round private randomisation is
represented by the arrays D1 drawn before round 1 (any per-round coin can be read off a fixed
uniform array), which is why D1 must be "before" every D2 and D5; Section 3 makes this a
hypothesis rather than a convention.

============================================================================================
## 2. The mechanism and the proposed profiles

### 2.1 CL-MESP keyed on labels (variant D)

The paper's CL-MESP with "context" read as "label", verbatim. Parameters from `n, K` only:

    L := min{ floor(n/(2K)), ceil( n^{2/3} (log(en))^{1/3} ) },   ell := log(2 n^4),
    s := sqrt( log(2 K n^4) / (2L) ),   b_n(r) := sqrt( r ell / 2 ),  b_n(0) := 0,
    gamma_n := min{ 1/2, sqrt(K log K / n) },  eta_n := gamma_n / K,
    R_K(H) := 3 sqrt(K H log K) + 2 K log K,  R_K(0) := 0.

Per label `b`, created lazily: visit count `v_b`, Stage-1 reward sums, price `tau_b`, winner `W_b`,
primary count `r_b` and sum `Z_b`, EXP3 weights, priority `Pi_b` (D3).

* Stage 1 at `b` while `v_b <= KL`: pull agent `((v_b - 1) mod K) + 1`. At `v_b = KL`: bids
  `beta_{j,b} := L^{-1} sum_{r<=L} Y_{j,b,r}`, winner `W_b` a largest bidder (ties by `Pi_b`), price
  `tau_b := (beta_{(2),b} - s)_+`.
* Stage 2 at `b` until a switch: pull `W_b`; switch at the first `r` with
  `Z_b < r tau_b - b_n(r)`.
* Stage 3 at `b` after a switch: explicit-exploration EXP3 over all `K` agents restricted to visits
  to `b`, fresh weights, parameters `gamma_n, eta_n`, never restarted.
* A label with `V_b < KL` visits in the horizon never awards, prices or monitors.
* Messages: the label `b`, its phase, and `tau_b` after Stage 1.

The platform needs no knowledge of `A`, `pi`, `Q_B`, the label law, `M`, `mu` or `K_H`.

### 2.2 The label-level profile `S*_N` (D-known) and its water-filling rule

Agent `j` knows `pi` (this is dropped in 2.3). Stage 1 and Stage 3 at any label: deliver
`M_j(X_t)`. Primary winner at label `b` with price `tau`: put `lo_j := mu_j` if `j` is honest,
`lo_j := 0` otherwise, the level

    lambda_j(b, tau) := max{ mubar_j(b) 1{j honest}, min{ tau, Mbar_j(b) } }  in [ sum_a pi_b(a) lo_j(a), Mbar_j(b) ],

and deliver `w_c(X_t) := clip(c, lo_j(X_t), M_j(X_t))` with the deterministic choice

    c := sup{ c' in [0,1] : sum_a pi_b(a) clip(c', lo_j(a), M_j(a)) <= lambda_j(b, tau) }.

The map `c' -> sum_a pi_b(a) clip(c', lo_j(a), M_j(a))` is continuous and nondecreasing from
`sum pi lo_j` at `c' = 0` to `Mbar_j(b)` at `c' = 1`, so the supremum is attained and the
`pi_b`-mean of the delivered response is exactly `lambda_j(b, tau)`. Two facts are used:

* (W1) the label mean `sum_a pi_b(a) w_c(a) = lambda_j(b,tau)`, hence `>= min{tau, Mbar_j(b)}`,
  and `= tau` when `j` is strategic and `tau <= Mbar_j(b)`, or honest and
  `mubar_j(b) < tau <= Mbar_j(b)`;
* (W2) if `j` is honest and `tau <= mubar_j(b)`, the level is `mubar_j(b) = sum pi lo_j`, hence
  `w_c(a) = mu_j(a)` at every `a` with `pi_b(a) > 0` (a clip at a value `>= lo` whose `pi`-mean
  equals the `pi`-mean of `lo` equals `lo` on the support). Outside the support the value is
  irrelevant for every expectation below, since such types occur at label `b` with probability 0.

Feasibility: `w_c in [lo_j, M_j]`; honesty: `w_c >= mu_j` for honest `j`. Any other allocation with
the same label mean gives the same expected utility under linear cost; water-filling is chosen
because it is deterministic and, pointwise, never below the paper's pointwise rule
`min{tau, M_j(a)}` when `tau <= Mbar_j(b)` (so it is also "compliant" in the item-5 metric).

Locality: `S*_N`'s target at a visit to `b` is a function of `(b, phase at b, tau_b, j, X_t)`.

### 2.3 D-learn, profile `S^L`

No one knows `pi`. Agent `j`'s estimate at label `b` is the empirical law `pihat_{j,b}` of the
true types at its own `L` Stage-1 pulls at `b` (it saw them). Margin

    kappa_n := sqrt( ( |A| log 2 + 4 log n ) / (2L) ).

Stage 1 and Stage 3: deliver `M_j(X_t)`. Primary winner at `b`: the rule of 2.2 with `pi_b`
replaced by `pihat_{j,b}` everywhere (in `Mbar`, `mubar`, the level and the choice of `c`) and
`tau` replaced by `tau + kappa_n`:

    lambdahat_j := max{ muhat_j 1{honest}, min{ tau + kappa_n, Mhat_j } },
    Mhat_j := sum_a pihat_{j,b}(a) M_j(a),   muhat_j := sum_a pihat_{j,b}(a) mu_j(a),

and `c := sup{ c' : sum_a pihat(a) clip(c', lo_j(a), M_j(a)) <= lambdahat_j }`. Feasible, honest,
and a function of `(b, phase, tau_b, j, X_t, j's own Stage-1 types at b)`.

============================================================================================
## 3. Hypotheses

### 3.1 Deterministic hypotheses

(H) `K >= 2`, `n >= 2K`, `A` and `Lab` finite, primitives as in 1.1, `K_H` nonempty, linear cost,
and the posterior kernel `pi` is FIXED (does not depend on `t`).

### 3.2 The natural fields

Within one execution, let `O_0 := sigma(B, theta)` and, at round `t`, in the order of Section 1.2,

    O^X_t := sigma(O_{t-1}, X_t)                        after the true type
    O^P_t := sigma(O^X_t, Pi_{B_t}) if B_t first met at t, else O^X_t      after the priority
    O^I_t := sigma(O^P_t, I_t)                          after the selection
    O^-_t := sigma(O^I_t, m_{I_t,t})                    after the target (pre seed)
    O_t   := sigma(O^-_t, U_t).

Since `B` and `theta` are in `O_0`, every one of these fields already carries the entire label
path; there is no separate "path-augmented" version, because the only path the model conditions on
is the label path, which is D0.

### 3.3 The probabilistic hypotheses, in conditional form

> **(X) Exogeneity.** The joint law `nu` of `(B, theta)` is the same under every strategy profile.

> **(N) Fresh draws given the label path.** At every round `t`, each draw the model makes at round
> `t`, in the order of Section 1.2 (the true type `X_t`; then every randomisation the mechanism
> specifies at round `t`, in the order it specifies them; then the seed `U_t`), has its specified
> law conditionally on the field generated by everything realised before it, that field **being**
> respectively `O_{t-1}`, the field after the previous draws of round `t`, and `O^-_t`. The
> specified law of `X_t` is `pi_{B_t}`; that of a mechanism randomisation is the one the mechanism
> specifies (it may depend on the past, as `p_t` does); that of `U_t` is Uniform`[0,1]`.

Instantiation for CL-MESP (the draws of Section 1.2 are all the draws; checked against 2.1):

* (N1) conditionally on `O_{t-1}`, `X_t` has law `pi_{B_t}`;
* (N2) on the event (in `O^X_t`) that `B_t` is first met at `t`, conditionally on `O^X_t`, `Pi_{B_t}`
  is uniform on the permutations of `[K]`;
* (N3) on the event (in `O^P_t`) that `B_t` is in Stage 3, conditionally on `O^P_t`, `I_t` has law
  `p_t`;
* (N4) conditionally on `O^-_t`, `U_t` is Uniform`[0,1]`.

Remarks.

**3.3a (why this form).** Each clause quantifies over everything realised before its draw, so it
cannot omit a family. In particular it covers, without listing them: the agents' coins (in
`O_0`), past true types of all rounds, past targets, past mechanism coins, the whole label path,
and the round-`t` true type for the round-`t` mechanism coin and seed.

**3.3b (what (N1) says).** Given the whole label path, the agents' coins and the entire past, the
true type is a fresh draw from the posterior of its label. This is **posterior stationarity**. It
forbids: bursty or drifting true-type order even with a perfect i.i.d. classifier (then the type
at `t` predicts the type at `t+1` given the labels); a classifier whose error depends on time or on
what providers did; true types that react to past rewards; an agent whose coin array carries
information about future true types; true types correlated with the fallback coin (that is
(N3), which conditions on `X_t`). It allows an arbitrary, even adversarial, label path chosen in
advance (D0 has an arbitrary law), and agents who know it.

**3.3c (sufficient condition).** (N) and (X) hold if the pairs `(X_t, B_t)` are i.i.d. with a law
`p(a) C(a,b)`, the coin arrays are `theta = F(B, theta')` with `theta'` independent of the pairs,
priorities and fallback coins are drawn from fresh independent uniforms, and seeds are fresh
independent uniforms. Then `pi_b(a) = p(a)C(a,b) / sum_a' p(a')C(a',b)`.

**3.3d (the witnesses of this project, and the new one).** (i) `U_t = frac(g(X_t) + c_t)` with
`c_t` a coordinate of the deviator's coin: pairwise independent of everything, but
`O^-_t`-measurable, so (N4) fails. (ii) `X_t` a function of the previous round's fallback coin:
violates (N1). (iii) New here: `X_{t+1} = X_t` with probability `rho` (bursty order) and an i.i.d.
classifier: every pairwise and every "type independent of seeds" clause holds, and the pairs have
the stationary marginal, but (N1) fails because `X_t in O_{t-1}` shifts the law of `X_{t+1}`. This
is the scout's "bursty" simulation, where D convicts in 22 percent of runs.

**3.3e (no future true types).** The deviation class below may not read `X_{t'}` for `t' > t`.
If it could, a target at `t` realised before `X_{t'}` would make `X_{t'}` non-fresh given
`O_{t'-1}` in the execution, so (N1) would fail for that execution: the exclusion is the same
statement as (N1), not an extra restriction.

### 3.4 Which hypothesis each result uses

| result | uses |
|:-|:-|
| Lemma C (canonical coupling) | (X), (N1) to (N4) |
| Lemmas 1, 2 (Stage 1, bids) | pathwise, plus (N1), (N4) on the canonical space |
| Lemma 3 (monitor) | (N1), (N4) |
| Lemmas 4, 5 (fallback) | (N1), (N3), (N4) |
| Theorem N (A) | all, through Lemma C |
| Theorem N (B), (C), (Conv) | (N1), (N3), (N4) and (X) (for the canonical space; no comparison of two executions) |
| Lemma B (benchmarks) | (N1) only through `E[f(X_t) | B] = sum_a pi_{B_t}(a) f(a)` |
| Proposition I | none of (N); it is about paths that violate it |

No step uses the uniformity of `Pi_b` (every lemma about a winner holds for whoever wins); part
(A) uses that `Pi_b` is a fresh draw with a profile-independent law, through Lemma C.

============================================================================================
## 4. Deviation classes

**`B^N_{i,n}` (the scout's class, enlarged by `t`).** After selection at round `t`, agent `i`
chooses `m_{i,t} in [0, M_i(X_t)]` as a measurable function of `n`, `t`, the label path `B`, its
coin array `theta_i`, the current true type `X_t`, the current message, and its own history (its
selection rounds, the labels and true types there, its targets, rewards and messages). Honest:
`m_{i,t} >= mu_i(X_t)` after every history.

**`B^N#_{i,n}` (the class I prove things for).** The same, except that the target may be any
measurable function of everything realised before it in its execution, that is, it is
`O^I_t`-measurable. This includes all past true types, all past rewards and seeds, all past
mechanism coins, all agents' coin arrays and the whole label path. It excludes future true types
(Remark 3.3e) and the current seed. `B^N_{i,n} subseteq B^N#_{i,n}`, and the paper's class
`B^ctx_{i,n}` read with "context" = label is contained in `B^N_{i,n}` (the paper's agent does not
see `B`), so every bound below holds for all three.

A feasible profile for (C) is `(S_1..S_K)` with `S_j in B^N#_{j,n}`, honest agents honest. Under
(N), for each such profile the execution's law is well defined (Ionescu-Tulcea, round by round in
the order of Section 1.2).

`S*_N` and `S^L` are in `B^N_{j,n}` for every `j` (implementable from `X_t`, the message and, for
`S^L`, the agent's own Stage-1 types).

============================================================================================
## 5. Statements

Notation: `V_b` visits to `b`, `N_b := (V_b - KL)_+`, `l_i(b) := #{ r <= L : (r-1)K + i <= V_b }`;
`sum_b l_i(b) <= min{Q_B L, n}`, `sum_b min{V_b, KL} <= min{Q_B K L, n}`. All are functions of `B`.

**Theorem N.** Assume (H), (X), (N). Run CL-MESP keyed on labels.

**(A) Additive behavioural equilibrium.** For every agent `i` (strategic or honest) and every
`S'_{i,n} in B^N#_{i,n}` (honest if `i in K_H`),

    u_i(n; S'_{i,n}, S*_{N,-i}) - u_i(n; S*_N)
      <= E[ sum_b l_i(b) ] + sum_{b : i in Tbar(b)} E[ 1{V_b >= KL} (1 + 2 b_n(N_b) + R_K(n)) ]
         + sum_{b : i notin Tbar(b)} E[ 1{V_b >= KL} Dbar_i(b) ] + 8 n^{-2},

    Dbar_i(b) := 8 (1 + sqrt(2 ell))^2 / deltabar_i(b)^2 + 2 R_K(n) / deltabar_i(b)   if 4 s <= deltabar_i(b),
    Dbar_i(b) := 2 N_b                                                            otherwise.

For `n` with `4 s <= min{ deltabar_i(b) : i notin Tbar(b) }`, the right side is at most

    min{Q_B L, n} + Q_B + sqrt(2 ell Q_B n) + Q_B R_K(n)
      + sum_{b : i notin Tbar(b)} [ 8(1+sqrt(2 ell))^2/deltabar_i(b)^2 + 2 R_K(n)/deltabar_i(b) ] + 8 n^{-2}.

**(B) Revenue.**

    P(n; S*_N) >= E sum_t Mbar_(2)(B_t) - [ min{Q_B K L, n} + 2 s n + Q_B R_K(n) + n^{-3} ].

If `Lab = A`, then `E sum_t Mbar_(2)(B_t) >= E sum_t M_(2)(X_t) - epsbar n max_a M_(2)(a)`, and
the constant `max_a M_(2)(a)` cannot be lowered (Lemma B(iii)).

**(C) Honest-benchmark robustness.** For every feasible profile `S` with every `S_j in
B^N#_{j,n}` and honest agents honest (all `K` agents may deviate jointly),

    P(n; S) >= E sum_t bbar(B_t)
               - [ min{Q_B K L, n} + 2 s n + Q_B + sqrt(2 ell Q_B n) + Q_B R_K(n) + 3 n^{-2} ].

If `|K_H| = 1`, `E sum_t bbar(B_t) = E sum_t b(X_t)`. If `Lab = A`,
`E sum_t bbar(B_t) >= E sum_t b(X_t) - epsbar n max_a b(a)`.

**(Conv) Compliant winners are not convicted.** Fix an agent `j` and a label `b`. Suppose `j`
delivers `M_j(X_t)` at its Stage-1 pulls at `b`, and at every primary pull at `b` a target
`f_t(X_t)`, with `f_t` an `O_{t-1}`-measurable response, whose label mean
`sum_a pi_b(a) f_t(a)` is at least `min{tau_b, Mbar_j(b)}` (`S*_N` does, by (W1)). Then for
every behaviour of the other agents in `B^N#`,

    P( W_b = j and the monitor at b switches | B ) <= (2 K n^4)^{-1} + N_b (2 n^4)^{-1},

and `P(j is switched out at some label | B) <= Q_B (2Kn^4)^{-1} + (2n^3)^{-1}`. If all agents play
`S*_N`, `P(any switch anywhere | B) <= #{b : V_b >= KL} (2n^4)^{-1} + (2n^3)^{-1}`.

**(D) Rates.** For fixed `K` and a fixed instance, all error terms are
`O(Q_B n^{2/3} (log n)^{1/3} + sqrt(Q_B n log n) + Q_B sqrt(K n log K))`, `o(n)` if
`Q_B = o(n^{1/3} (log n)^{-1/3})`. (Only the "if" is claimed; the converse would need the analogue
of the paper's `prop:ctx-finite-tight`, which I expect carries over with labels, but did not
re-verify.)

**Corollary L (D-learn).** Same hypotheses, profile `S^L` in place of `S*_N`. Then (A) holds with
the additional term `2 kappa_n sum_{b : i in Tbar(b)} E[N_b] <= 2 kappa_n n` and `8 n^{-2}` replaced
by `8 n^{-2} + 2(K+1) n^{-3}`; (B) holds with `n^{-3}` replaced by `(K+1) n^{-3}`; (C) holds verbatim
(it does not involve the profile); (Conv) holds for `S^L` with the right side increased by
`n^{-4}` per label. `kappa_n = O(sqrt(|A| + log n) n^{-1/3} (log n)^{-1/6})`, so the extra term is
`O(n^{2/3} ((log n)^{1/3} + |A|^{1/2} (log n)^{-1/6}))`, the same rate for fixed `|A|`.

**Proposition I (order robustness is lost under label noise).** Fix `eps in (0, 1]` and an even
`n >= 2K`. Types `A = {a, c, d}`, labels `Lab = {a, c}`, class map `kappa(a) = a`,
`kappa(c) = kappa(d) = c`. Classifier: `B_t ~ C(X_t, .)` independently given `X`, with
`C(a, a) = 1`, `C(c, a) = eps`, `C(c, c) = 1 - eps`, `C(d, c) = 1`; so the per-type
misclassification probability `P(B != kappa(X) | X)` is `0, eps, 0`. Agents `K = 3`, all strategic
with `mu = 0`: `M_W(a) = 1`, `M_W(c) = M_W(d) = 0`, `M_j = 1/2` at every type for `j = 2, 3`.
True-type paths, exogenous and independent of everything else:

    P1: X_t = a for t <= n/2, X_t = c for t > n/2           (deterministic);
    P2: X_t = a for t <= n/2, X_t i.i.d. with P(a) = eps, P(d) = 1 - eps for t > n/2.

Let `M` be any label-measurable mechanism: its selection at `t` is a measurable function of
`B_1..B_t`, its past selections and rewards, its own coins, and its messages are functions of the
same. Let agents 2 and 3 play any strategies that do not read true types. Let `sigma` be any
strategy of `W` that is feasible on `P1`, and `sigma~` the strategy on `P2` that at every round
delivers what `sigma` would deliver if the true types so far (and now) were those of `P1` (it reads
`t`). Then:

(a) The joint law of labels, mechanism coins, selections, messages and rewards is the same under
`(P1, sigma)` and `(P2, sigma~)`, and `u_W(P1; sigma) = u_W(P2; sigma~)`. On `P2`, `sigma~` is
feasible and delivers `0` at every round `t > n/2`.

(b) Suppose in addition that `sigma` and `sigma~` coincide on `P2` at rounds `t <= n/2` (true when
`sigma` reads types only through the current type, since the first-half types agree). Write
`N^II_W` for the number of rounds `t > n/2` allocated to `W`, and `D := E_{P2,sigma}[ sum_{t > n/2,
B_t = a, I_t = W} m_{W,t} ]`. Then, exactly,

    G + P = D,    G := u_W(P2; sigma~) - u_W(P2; sigma),
                  P := E_{P2,sigma}[N^II_W] - E_{P1,sigma}[N^II_W],

provided `sigma` delivers `0` at every label-`c` round `t > n/2` on `P2` (forced: the type there is
`d`, `M_W(d) = 0`).

(c) `P2` satisfies (N) and (X) with `pi_a = delta_a`, `pi_c = delta_d`; `P1` violates (N1). For
CL-MESP, with `sigma = S*` (the paper's pointwise profile, which on `P2` equals `S*_N`) and the
other agents on `S*`: `D >= (1/2 - 2s)(eps n/2) - n^{-2}`, and by Theorem N(A) on `P2`,
`G <= Delta_n := 2L + 1 + 2 b_n(n) + R_K(n) + 32(1+sqrt(2 ell))^2 + 4 R_K(n) + 8 n^{-2}` whenever
`4 s <= 1/2`. Hence

    E_{P2,S*}[N^II_W] - E_{P1,S*}[N^II_W]  >=  (1/2 - 2s) eps n/2 - Delta_n - n^{-2}  =  eps n/4 - O(n^{2/3} (log n)^{1/3}).

(d) (Remark, direct.) For CL-MESP on `P1` the pointwise-compliant `W` is switched out at label `a`
with probability at least `1 - P(R^a < k_n) - 3 n^{-3}`, where `R^a ~ Bin(n/2, eps)` is the number
of second-half label-`a` rounds and `k_n := 1 + sqrt(2 n ell)/(1/2 - 2s)`.

Reading: `P2` satisfies every hypothesis of Theorem N and `W` is its label-level compliant top
agent; `P1` differs only in the ORDER of true types. A mechanism that deters shading on `P2` must,
by (b), withhold from the pointwise-compliant `W` on `P1` at least `D - G` allocations. So "no
false conviction of pointwise-compliant winners for arbitrary exogenous order" (which c2 has with
noise-free contexts) and "shading gain `o(n)`" cannot both hold under label noise, for any
label-measurable mechanism that gives its compliant top agent a constant share of its label on
`P2`. With `eps = 0` the construction is void (`R^a = 0`), consistent with c2.

============================================================================================
## 6. The canonical space and the primitive filtration

### Lemma C (canonical coupling)

Let `Omega` carry: `(B, theta) ~ nu`; and, conditionally on `(B, theta)`, four mutually independent
families whose conditional law does not depend on `theta`:
`X = (X_t)_{t<=n}` independent with `X_t ~ pi_{B_t}`; `Pi = (Pi_b)_{b in Lab}` i.i.d. uniform
permutations; `xi = (xi_t)` i.i.d. Uniform`[0,1]`; `U = (U_t)` i.i.d. Uniform`[0,1]`.
For a profile `S` (each `S_j in B^N#_{j,n}`) define the execution `E^S` on `Omega` round by round:
label `B_t`; at the award at `b` the tie-break is `Pi_b`; in Stage 3 `I_t := G(p_t, xi_t)` with
`G(p,u) := min{ l : p_1 + ... + p_l >= u }`; the selected agent's target is the value its strategy
assigns to the realised history, `X_t`, its message and `theta_{I_t}`; `Y_t := 1{U_t <= m_{I_t,t}}`.

**Claim.** Under (X) and (N), for every such `S`, the law of the model's execution under `S` (the
sequence `(B, theta)`, then per round `X_t`, the priority drawn if any, `I_t`, `m_{I_t,t}`, `U_t`)
equals the law of the same sequence realised by `E^S` on `Omega`.

Proof. The law of a finite sequence of random elements (here with values in finite sets or
`[0,1]`) is determined by the law of the first element and the conditional law of each element
given the preceding ones (the chain rule for regular conditional laws; equivalently the uniqueness
half of Ionescu-Tulcea). In the model: `(B, theta) ~ nu` by (X); the conditional law of each draw
given its predecessors is the one in (N1) to (N4); the target is a fixed measurable function of its
predecessors (the strategy). On `Omega`: `(B,theta) ~ nu`. Write `P_{t-1} := sigma(B, theta, Pi,
(X_s, xi_s, U_s)_{s<t})`. The predecessors of `X_t` in `E^S` are measurable with respect to
`P_{t-1}` (every quantity of the execution before `X_t` is a function of those primitives), `X_t`
is independent of `P_{t-1}` given `B` with law `pi_{B_t}`, and `pi_{B_t}` is a function of a
predecessor (`B`); by the tower property the conditional law of `X_t` given its predecessors is
`pi_{B_t}`. The priority used when `b` is first met at `t` is `Pi_b`; its predecessors are functions
of `(B, theta, (Pi_{b'})_{b' met before t}, X_{<=t}, (xi_s, U_s)_{s<t})`, which do not involve
`Pi_b`, so its conditional law is uniform. `I_t = G(p_t, xi_t)` with `p_t` a function of the
predecessors and `xi_t` independent of all of them, so its conditional law is `p_t`. The target is
the same function of its predecessors as in the model. `U_t` is independent of all predecessors
(which are functions of `P_{t-1}`, `X_t`, `xi_t`), so it is uniform given them. All kernels agree,
so the laws agree. QED

Consequences. (i) `u_i(n; S)` and `P(n; S)` may be computed on `Omega` for every profile.
(ii) For part (A), the deviating execution `E' := E^{(S'_i, S*_{N,-i})}` and the baseline
`E* := E^{S*_N}` live on the SAME `Omega`, with the same labels, the same true types, the same
seeds, the same priorities, the same fallback coins and the same coin arrays. This is where the
true types become "common" to the two executions: under (N) they are primitives, not outcomes.
(iii) `B` takes finitely many values, so we may and do condition on `{B = beta}` for a fixed
`beta` of positive probability and integrate at the end; conditionally, `theta` has law
`nu(. | beta)` and the four families keep their laws and their independence. From now on all
probabilities are conditional on `B = beta`, and every visit count, every Stage-1 round, every
round `t_{b,r}` of the `(KL + r)`-th visit to `b`, and `N_b` are deterministic.

Where each clause of (N) was used: (N1) for `X_t` fresh with law `pi_{B_t}` given everything
before, including `theta` and past true types; (N2) and (N3) for the mechanism draws; (N4) for the
seed given the target. If any clause failed, the kernels would differ and the two executions of
part (A) could not be put on one space with common types and seeds: this is the load (Section 15).

### 6.1 The primitive filtration

On `Omega` (given `B`): `P_0 := sigma(B, theta, Pi)`, `P^X_t := sigma(P_{t-1}, X_t)`,
`P^I_t := sigma(P^X_t, xi_t)`, `P_t := sigma(P^I_t, U_t)`. It is the same for both executions of
part (A) (the adversary's F4 repair of c2, which I adopt from the start). Facts, for every
execution `E^S`:

* (F0) The execution's history through round `t` is `P_t`-measurable; the phase of `B_t` at round
  `t` and the Stage-1 and Stage-2 selections are `P_{t-1}`-measurable; `I_t` and the target are
  `P^I_t`-measurable.
* (F1) Given `P_{t-1}`, `X_t ~ pi_{B_t}`; `xi_t` is independent of `P^X_t`; `U_t` is independent
  of `P^I_t`.
* (F2) Response functions. Because the target is a function of predecessors, and all predecessors
  except `X_t` and `I_t` are `P_{t-1}`-measurable, on `{I_t = j}` the target is `f^j_t(X_t)` for a
  map `f^j_t : A -> [0, M_j]` whose values `f^j_t(a)` are `P_{t-1}`-measurable. (For `B^N#` this is
  the definition; `f^j_t(a)` is "what `j` would deliver if the type were `a`".) Honest `j`:
  `f^j_t >= mu_j` pointwise.
* (F3) Consequently, for every `P_{t-1}`-measurable `g : A -> R`,

      E[ 1{I_t = j} g(X_t) | P_{t-1} ] = p_{j,t} sum_a pi_{B_t}(a) g(a),
      E[ Y_t 1{I_t = j} | P_{t-1} ]   = p_{j,t} rbar_{j,t},   rbar_{j,t} := sum_a pi_{B_t}(a) f^j_t(a),

  where `p_{j,t}` is the Stage-3 law, or the point mass on the deterministic selection in Stages 1
  and 2. Proof: `I_t = G(p_t, xi_t)` with `xi_t` independent of `(P_{t-1}, X_t)`, `X_t` has law
  `pi_{B_t}` given `P_{t-1}`, and `E[Y_t | P^I_t] = m_t` by (F1).
  In Stages 1 and 2, `mbar_t := rbar_{I_t,t} = E[Y_t | P_{t-1}] = E[m_t | P_{t-1}]` is the
  **predictable mean** of the round. Feasibility gives `mbar_t <= Mbar_{I_t}(B_t)`; honesty gives
  `mbar_t >= mubar_{I_t}(B_t)`.

**The one place the deviator's knowledge of past true types enters.** `P_{t-1}` contains every
past true type (the deviator's own and everyone else's) and the deviator's coin array, and the
deviator's response `f^i_t` may depend on all of it. Nothing in (F1) to (F3) is affected, because
`X_t` is independent of `P_{t-1}`. So past types are information the deviator has and the
mechanism lacks, but they carry no information about the current type (N1), nor about seeds or
coins; every lemma below is stated against `P_{t-1}` and is therefore uniform over deviators that
use them. The only thing a deviator could exploit is information about the CURRENT or FUTURE types
beyond `pi_{B_t}`, and (N1) is precisely the statement that there is none.

============================================================================================
## 7. Lemmas

Fix `B = beta`. For a label `b` with `V_b >= KL` write `t_1(b)` for the round of its `KL`-th visit
and `t_r := t_{b,r}` for that of its `(KL + r)`-th visit, `r = 1..N_b`. In an execution, `q_b` is the
primary tenure (number of primary pulls, including the one at which a switch is declared;
`q_b = N_b` if no switch).

### Lemma 1 (Stage-1 coupling; pathwise on `Omega`, executions `E'` and `E*` of part (A))

(a) The Stage-1 rounds at `b` and the agent pulled at each are functions of `B`, the same in both.
(b) For `j != i`, `beta_{j,b} = L^{-1} sum 1{U_t <= M_j(X_t)}` over `j`'s Stage-1 rounds at `b`, the
same random variable in both; given `B` these `L` indicators are i.i.d. Bernoulli(`Mbar_j(b)`).
(c) `beta'_{i,b} <= beta*_{i,b}` pathwise.
(d) `{i wins at b in E'} subseteq {i wins at b in E*}`, and on the former both announce
`tau_{i,b} := (max_{j != i} beta_{j,b} - s)_+`.
(e) `i`'s Stage-1 utility at `b` in `E'` exceeds that in `E*` by at most `l_i(b)`, pathwise.
(f) For every `j`, `pihat_{j,b}` is the same in both executions and is the empirical law of `L`
i.i.d. `pi_b` draws.

Proof. (a) Round robin on the visits to `b`, which are determined by `B`. (b) `S*_N` (and `S^L`)
deliver `M_j(X_t)` in Stage 1 whatever the history; the round, `X_t` and `U_t` are the same
primitives in both executions (Lemma C(ii)). Given `B`, the pairs `(X_t, U_t)` at distinct rounds
are independent, `X_t ~ pi_b`, `U_t` uniform, so `P(U_t <= M_j(X_t)) = Mbar_j(b)`. (c) At `i`'s
Stage-1 round `t`, `m'_{i,t} <= M_i(X_t)` by feasibility, so
`1{U_t <= m'_{i,t}} <= 1{U_t <= M_i(X_t)}`, pointwise; no measurability of `m'` is used, so a
deviator that times its bid using past types, other labels or the future labels is covered.
(d) and (e) are the paper's `lem:ctx-bid`(d),(e) verbatim given (b), (c) and the common `Pi_b`;
the per-pull utility difference is `(1 + mu_i(X_t) - m') - (1 + mu_i(X_t) - M_i(X_t)) =
M_i(X_t) - m' in [0,1]`, with the SAME `X_t` on both sides. (f) as (b).

Reuse. c2P1 Lemma 3 (L3a), Lemma 4 (L4a to L4d); paper `lem:ctx-bid`. Change: the capability at a
Stage-1 pull is `M_j(X_t)`, random. What makes the pathwise steps survive is that `X_t` is the
same in both executions, which is Lemma C and nothing else. Re-verified above.

### Lemma 2 (concentration of bids and of type estimates; given `B`, any profile unless stated)

(i) Under a profile in which every `j != i` delivers capability in Stage 1 (part (A)):
`G(b) := { |beta_{j,b} - Mbar_j(b)| <= s  for all j != i }` has `P(G(b)^c) <= 2(K-1) e^{-2 L s^2}
= (K-1)/(K n^4) <= n^{-4}`, and on `G(b)`: `(Vbar_i(b) - 2s)_+ <= tau_{i,b} <= Vbar_i(b)`.
(ii) Under `S*_N` or `S^L` for all agents: `G^all(b) := { |beta_{j,b} - Mbar_j(b)| <= s for all j }`
has `P(G^all(b)^c) <= n^{-4}`; on it `Mbar_(2)(b) - 2s <= tau_b <= Mbar_(2)(b)` and
`tau_b <= Mbar_{W_b}(b)`.
(iii) If agent `j` delivers `M_j(X_t)` at its Stage-1 pulls at `b`, then under ANY behaviour of the
others, `P(beta_{j,b} > Mbar_j(b) + s) <= e^{-2Ls^2} = (2Kn^4)^{-1}`.
(iv) If `h` is honest (any strategy in `B^N#`), under any behaviour of the others,
`P(beta_{h,b} < mubar_h(b) - s) <= (2Kn^4)^{-1}`.
(v) `P( TV(pihat_{j,b}, pi_b) > kappa_n ) <= n^{-4}`, where `TV(p,q) := max_{S subseteq A} (p(S) - q(S))`.

Proof. (i), (ii), (iii): the indicators are i.i.d. Bernoulli(`Mbar_j(b)`) by Lemma 1(b) (which
used only that `j` delivers capability), so Hoeffding applies; `2 L s^2 = log(2Kn^4)`. The price
bounds: the second order statistic and `max_{j != i}` are 1-Lipschitz in the sup norm and `(.)_+`
is 1-Lipschitz and nondecreasing; `tau_b <= (beta_{W} - s)_+ <= Mbar_W(b)` on `G^all(b)`.
(iv) At `h`'s Stage-1 rounds `t` (deterministic given `B`), the increments `D_t := Y_t - mbar_t`
satisfy `E[D_t | P_{t-1}] = 0` by (F3), lie in an interval of length one with `P_{t-1}`-measurable
endpoints, and `mbar_t >= mubar_h(b)` by honesty and (F2). The Azuma bound (c2P1 Lemma 4b, whose
proof uses only Hoeffding's lemma conditionally) gives `P(sum D_t < -L s) <= e^{-2Ls^2}`, and
`beta_{h,b} - mubar_h(b) >= L^{-1} sum D_t`. (v) The types at `j`'s Stage-1 rounds at `b` are
i.i.d. `pi_b` given `B` (Lemma 1(f)); for each of the `2^{|A|}` subsets `S`, Hoeffding gives
`P(pihat(S) - pi_b(S) > kappa) <= e^{-2 L kappa^2}`; the union gives
`2^{|A|} e^{-2L kappa_n^2} = 2^{|A|} e^{-|A| log 2 - 4 log n} = n^{-4}`.

The union counts: in (i) and (ii) over the `K - 1` (or `K`) agents, a fixed number; in (v) over the
`2^{|A|}` subsets, fixed. When these are later summed over labels, the labels with `V_b >= KL` form
a `B`-measurable set, deterministic under the conditioning, of size at most `min{Q_B, n/(KL)}`.

### Lemma 3 (anytime label monitor, centred at the predictable mean)

Any profile in `B^N#`, given `B`. Fix `b` with `V_b >= KL`, and let `W = W_b`. For `r <= q_b` put
`Z_r := sum_{u<=r} Y_{t_u}`, `Abar_r := sum_{u<=r} mbar_{t_u}` (predictable means of the winner's
primary pulls). Then, for every event `Gamma in P_{t_1(b)}`:

(a) `P( Gamma cap { exists r <= q_b : |Z_r - Abar_r| > b_n(r) } ) <= P(Gamma) N_b n^{-4}`
    `<= P(Gamma) n^{-3}`;
(b) on the complement of the event in (a), `Abar_{q_b} >= q_b tau_b - 1 - 2 b_n(q_b)`;
(c) `P( Gamma cap { exists r <= q_b : Z_r - Abar_r < - b_n(r) } ) <= P(Gamma) N_b (2n^4)^{-1}`; in
    particular, if on `Gamma` every primary predictable mean at `b` is at least `tau_b`, then
    `P(Gamma cap {a switch occurs at b}) <= P(Gamma) N_b (2n^4)^{-1}`.

Proof. Let `psi_s := 1{round s is a primary pull at b}`, `P_{s-1}`-measurable by (F0), zero for
`s <= t_1(b)`. Put `M_t := sum_{s<=t} psi_s (Y_s - mbar_s)`. By (F3) (Stage-2 selection is
deterministic, so `p` is a point mass), `E[psi_s (Y_s - mbar_s) | P_{s-1}] = 0`, and given
`P_{s-1}` the increment lies in `psi_s [-mbar_s, 1 - mbar_s]`, an interval of length `psi_s` with
`P_{s-1}`-measurable endpoints; Hoeffding's lemma gives
`E[ e^{lambda (M_s - M_{s-1})} | P_{s-1} ] <= e^{lambda^2 psi_s / 8}`. Fix `r in [1, N_b]` and let
`T_r := t_r` if `q_b >= r` and `T_r := infinity` otherwise. Then
`psi_s 1{s <= T_r} = psi_s 1{fewer than r primary pulls at b occurred before s}` (if `q_b >= r`, a
primary pull `s <= t_r` is the `k`-th with `k <= r`; if `q_b < r`, every primary pull has fewer than
`r` before it), which is `P_{s-1}`-measurable, so
`c_t := sum_{s <= t} psi_s 1{s <= T_r} <= r` is predictable and
`exp(lambda M_{t and T_r} - lambda^2 c_t/8)` is a `(P_t)`-supermartingale for `t >= t_1(b)` with
value 1 at `t_1(b)`. Hence `E[ e^{lambda M_{n and T_r}} | P_{t_1(b)} ] <= e^{lambda^2 r/8}` and the
Chernoff choice `lambda = 4 beta'/r` gives `P( M_{n and T_r} > beta' | P_{t_1(b)} ) <= e^{-2 beta'^2/r}`,
and likewise the lower tail. On `{q_b >= r}`, `M_{n and T_r} = Z_r - Abar_r`. With
`beta' = b_n(r)` each tail is `e^{-ell} = (2n^4)^{-1}`. The index set is `{1, ..., N_b}`,
deterministic given `B`; the union over it and both tails gives (a), the lower tail alone gives
(c)'s first claim, and multiplying by `1_Gamma` inside `E[ . | P_{t_1(b)}]` is legitimate because
`Gamma in P_{t_1(b)}`. For the second claim of (c): on `Gamma`, `Abar_r >= r tau_b` for every
`r <= q_b`, and a switch at `r` means `Z_r < r tau_b - b_n(r) <= Abar_r - b_n(r)`. (b) is the paper's
`lem:ctx-monitor`(b) verbatim, with `Abar` for `A`: if no switch, `Z_q >= q tau - b_n(q)` and
`Z_q <= Abar_q + b_n(q)`; if the switch is at `q >= 2`, apply at `q - 1` and use
`Abar_q >= Abar_{q-1}`, `tau <= 1`, `b_n` nondecreasing; if at `q = 1`, `Abar_1 >= 0 >= tau - 1`. QED

Reuse and what changed. c2P1 Lemma 5 (phantom continuation, local index) and the paper's
`lem:ctx-monitor` (global time, predictable indicator). I use the paper's global-time device; the
change is the **centring**: the increment is `Y_s - mbar_s` with `mbar_s = E[Y_s | P_{s-1}]`, the
mean BEFORE the type is drawn, instead of `Y_s - m_s` with `m_s = E[Y_s | pre-seed field]`. Both are
martingale differences of range one (`Y_s in {0,1}`), so the constants are unchanged. The pre-type
centring is what the label-level notion of compliance needs: a label-level compliant winner's
realised targets `w_c(X_s)` can be below `tau` at some types, and only their `pi_b`-mean is at least
`tau`, so (c) must be stated for `Abar`. The scout's device (extend c2P1's excluded index set by the
future true types at `b`) is not needed in global time: `X_s` is simply not in `P_{s-1}`. The
filtration contains every past true type, so (a) to (c) are uniform over deviators that use them.
The union bound is over a set that is deterministic because we conditioned on `B` (c2 adversary
F5 and "random index sets" concern: none here). No phantom process is needed: the conclusions are
only asserted at `r <= q_b`, and the stopped supermartingale handles the random tenure.

### Lemma 4 (label fallback, EXP3 prefix form, in the primitive filtration)

Any profile in `B^N#`, given `B`. Fix `b` with `V_b >= KL`, `q0 in {1, ..., N_b - 1}` and an event
`Gamma in P_{t_{q0}}` with `Gamma subseteq {q_b = q0}` (the switch is declared at the `q0`-th primary
pull). Suppose some `j` has `rbar_{j,t} >= v` at every fallback round `t = t_r`, `r > q0`, on
`Gamma`. Then, with `H := N_b - q0`,

    E[ 1_Gamma sum_{r > q0} Y_{t_r} ] >= P(Gamma) ( v H - R_K(n) ).

Proof. The paper's `lem:ctx-fallback` with `J_{t-1} := P_{t-1}` and with `1_Gamma` carried through:
at each fallback round `t`, the weights and `p_t` are `P_{t-1}`-measurable, `1_Gamma` is
`P_{t-1}`-measurable (`Gamma in P_{t_{q0}} subseteq P_{t-1}`), and by (F3)
`E[hatY_{l,t} | P_{t-1}] = rbar_{l,t}`, `E[hatY_{l,t}^2 | P_{t-1}] = rbar_{l,t}/p_{l,t}`,
`E[Y_t | P_{t-1}] = sum_l p_{l,t} rbar_{l,t}`. The potential inequality is pathwise for the `H`
rounds played; multiply by `1_Gamma`, take expectations round by round with the tower property at
`P_{t-1}` (legitimate: `1_Gamma` is `P_{t-1}`-measurable at every such round, and the number of
terms `H` is deterministic given `B` and `q0`), and follow the paper's constants:
`E[1_Gamma sum Y] >= P(Gamma)(vH - 2 gamma_n H - K log K/gamma_n) >= P(Gamma)(vH - R_K(n))`. QED

Reuse. Paper `lem:ctx-fallback`; c2P1 Lemmas 6, 7 (which use doubling; not needed here). Change:
the comparator condition is on the PREDICTABLE mean `rbar_{j,t} = sum_a pi_b(a) f^j_t(a)`, not on a
pointwise capability; `S*_N` and `S^L` deliver `M_j(X_t)` in Stage 3, so `rbar_{j,t} = Mbar_j(b)`.
The field `J_{t-1}` must NOT contain `X_t`: the paper's "field just before the selection" is ambiguous
once the type is random and drawn before the selection, and `P_{t-1}` is the right choice, since the
EXP3 estimator identities need `E[hatY | J]` for a field on which `p_t` is measurable and `xi_t` is
fresh; both `P_{t-1}` and `P^X_t` qualify, but only with `P_{t-1}` is the comparator mean the
constant `Mbar_j(b)`. The fallback length is deterministic given `B` and `q0`, so the paper's
reliance on the standing conditioning is preserved (here via `B`, not via the type path).

### Lemma 5 (the deviator's fallback utility at a label)

Setting of Lemma 4, in an execution in which every `j != i` delivers `M_j(X_t)` at its fallback
pulls at `b`. Then

    E[ 1_Gamma U^fb_i(b) ] <= P(Gamma) ( (1 + mubar_i(b) - Vbar_i(b)) H + R_K(n) ),
    E[ 1_Gamma U^fb_i(b) ] <= P(Gamma) 2 R_K(n) / deltabar_i(b)     if deltabar_i(b) > 0.

Proof. Assume `P(Gamma) > 0`. Put `Qbar := E[1_Gamma sum_t p_{i,t}]/P(Gamma)` and
`Abar := E[1_Gamma sum_t p_{i,t} rbar_{i,t}]/P(Gamma)`, sums over the fallback rounds. By (F3) with
`g = 1 + mu_i - f^i_t` (a `P_{t-1}`-measurable function of the type) and `1_Gamma in P_{t-1}`,

    E[ 1_Gamma U^fb_i(b) ] = E[ 1_Gamma sum_t 1{I_t = i}(1 + mu_i(X_t) - f^i_t(X_t)) ]
                           = P(Gamma) ( (1 + mubar_i(b)) Qbar - Abar ).

This is the step where the deviator's type-dependent utility `mu_i(X_t)` is averaged: it is legitimate
only because the selection coin is independent of the type given `P_{t-1}` (N3, via (F3)).
Lemma 4 with `j*` attaining `Vbar_i(b)` (`rbar_{j*,t} = Vbar_i(b)`) gives
`E[1_Gamma sum Y] >= P(Gamma)(Vbar_i H - R_K(n))`, while by (F3)
`E[1_Gamma sum Y] = P(Gamma)(Abar + sum_{j != i} Mbar_j(b) E_Gamma[#j]) <= P(Gamma)(Abar + Vbar_i(H - Qbar))`.
So `Abar >= Vbar_i Qbar - R_K(n)`, whence the first display using `1 + mubar_i - Vbar_i >= 0` and
`Qbar <= H`. For the second, `rbar_{i,t} <= Mbar_i(b)` by feasibility, so `Abar <= Mbar_i Qbar`, so
`deltabar_i Qbar <= R_K(n)`, and per-pull utility is at most 2. QED

Reuse: c2P1 Lemma 8 and the paper's display following `lem:ctx-bid`; same algebra with barred
quantities, re-verified above.

### Lemma 6 (label-level compliance of the proposed winners)

Let `j` win at `b` with price `tau`, and let `mbar` be its predictable mean at a primary pull.
(i) Under `S*_N`: `mbar = lambda_j(b, tau)`, so `min{tau, Mbar_j(b)} <= mbar <= max{ mubar_j(b)
1{j honest}, tau }` (the upper bound when `tau <= Mbar_j(b)`), with `mbar = tau` in the cases of
(W1), and per-pull utility exactly `1` almost surely in the case of (W2).
(ii) Under `S^L`, on `{TV(pihat_{j,b}, pi_b) <= kappa_n}`:
`min{tau, Mbar_j(b)} <= mbar <= max{ mubar_j(b) 1{j honest}, tau } + 2 kappa_n`, and `mbar >= mubar_j(b)`
if `j` is honest.

Proof. (i) is (W1) and (W2) of Section 2.2 with (F2): the response is the deterministic
`w_c(.)`, a function of `P_{t-1}`-measurable data, so `mbar = sum_a pi_b(a) w_c(a)`. The upper
bound: `lambda_j = max{mubar_j 1{h}, min{tau, Mbar_j}} <= max{mubar_j 1{h}, tau}`.
(ii) Let `f := clip(c, lo_j, M_j)`, `f in [0,1]^A`; for any `f in [0,1]^A`,
`|sum_a (pi_b - pihat)(a) f(a)| <= TV(pihat, pi_b)` (write `f = int_0^1 1{f >= u} du` and use
`|p(S) - q(S)| <= TV` for every `S`). The `pihat`-mean of `f` is `lambdahat_j` (continuity of the
clip mean in `c`, as in 2.2). If `c = 1` then `f = M_j` and `mbar = Mbar_j(b)`. If `c < 1`, then
`lambdahat_j < Mhat_j` (if `lambdahat_j = Mhat_j`, `c' = 1` is admissible and the supremum is 1),
so `min{tau + kappa_n, Mhat_j} <= lambdahat_j < Mhat_j` forces `tau + kappa_n <= lambdahat_j`, and
`mbar >= lambdahat_j - kappa_n >= tau`. Upper: `mbar <= lambdahat_j + kappa_n <= max{muhat_j 1{h},
tau + kappa_n} + kappa_n <= max{mubar_j 1{h}, tau} + 2 kappa_n`, using `muhat_j <= mubar_j + kappa_n`.
Honest: `f >= mu_j` pointwise. QED

Where the scout's `n gamma` becomes `2 kappa_n n`: the margin `kappa_n` protects the lower bound
against an estimate that is too optimistic; the same estimation error can make the delivered mean
exceed the intended level by another `kappa_n`. Both are paid by the winner, and part (A) compares
with a deviator who delivers exactly `tau` on average, so both appear.

============================================================================================
## 8. Proof of Theorem N (A)

Fix `i`, `S'_{i,n} in B^N#_{i,n}`, the two executions `E'` (deviation) and `E*` (baseline) on
`Omega` (Lemma C), and `B = beta`. Primes and stars mark the execution. Let `U_i(b)` be `i`'s
realised utility on the visits to `b`. The rounds are partitioned by labels, so

    u_i(n; S', S*_{N,-i} | beta) - u_i(n; S*_N | beta) = sum_b ( E[U'_i(b)] - E[U*_i(b)] ),    (8.1)

an identity (linearity of expectation; no independence across labels is used). Split
`U_i(b) = U^bid_i(b) + U^post_i(b)`. By Lemma 1(e), `U'^bid_i(b) - U*^bid_i(b) <= l_i(b)` pathwise;
if `V_b < KL` there is no post-bid visit and the label contributes at most `l_i(b)`.

Fix `b` with `V_b >= KL`, write `N := N_b`, `tau := tau_{i,b}`, and define the events

    Win' := { i wins at b in E' },  G := G(b) (Lemma 2(i)),  Gamma_W := Win' cap G,  Gamma_L := (Win')^c cap G.

All three are in `P_{t_1(b)}`: they are functions of the Stage-1 data at `b` of `E'` and of `Pi_b`,
and the Stage-1 data of `E'` at `b` are functions of primitives realised by `t_1(b)` (F0). This is
the joint field on which both executions are compared (c2 adversary F4): it is a field of
PRIMITIVES, so it is the same object whichever execution a lemma is applied to, and every lemma of
Section 7 was proved for events in it. Post-bid utilities lie in `[0, 2N]` in both executions.

**The event `G^c`.** `E[(U'^post - U*^post) 1_{G^c}] <= 2N P(G^c) <= 2N n^{-4}`.

**The losing branch `Gamma_L`.** The winner `W != i` of `E'` plays `S*_N`. On `G`,
`tau_b = (beta_{(2),b} - s)_+ <= (beta_{W,b} - s)_+ <= Mbar_W(b)`, because `W` is a largest bidder
and `|beta_{W,b} - Mbar_W(b)| <= s` (`W != i`). By Lemma 6(i) every primary predictable mean of `W`
is `lambda_W(b, tau_b) >= min{tau_b, Mbar_W(b)} = tau_b`. Lemma 3(c) with `Gamma = Gamma_L` gives
`P(Gamma_L cap {switch in E'}) <= N (2n^4)^{-1}`. Without a switch `i` has no post-bid pull at `b`
in `E'`. Hence `E[U'^post 1_{Gamma_L}] <= 2N . N (2n^4)^{-1} <= N n^{-3}`, and `U*^post >= 0`.
(This is the step that rules out "bid so as to price the winner out": when `i` loses, the price is
at most the winner's label mean on `G`, and the winner meets it on average. Note it is the label
mean `Mbar_W(b)` that bounds the price, because the bids estimate label means; a pointwise
capability `M_W(a)` at some type `a` may well be below `tau_b`, which is exactly the item-5
failure, and is harmless here because Lemma 3(c) needs only the predictable mean.)

**The winning branch, `i in Tbar(b)`.** On `Gamma_W` both executions face `tau` (Lemma 1(d)), and
by Lemma 2(i) `tau <= Vbar_i(b) <= Mbar_i(b)`. Write `mubar := mubar_i(b)`.

*Deviating side, primary.* On `Gamma_W` the `r`-th post-bid visit, if `r <= q'`, is a primary pull
of `i` at round `t_r` with response `f'_{t_r}` (F2). The event `Gamma_W cap {q' >= r}` is in
`P_{t_r - 1}` (`{q' >= r}` is decided by the rewards of primary pulls `1..r-1`). By (F3), with
`g = 1 + mu_i - f'_{t_r}`,

    E[ 1_{Gamma_W} U'^pri ] = sum_{r<=N} E[ 1_{Gamma_W} 1{q' >= r} (1 + mu_i(X_{t_r}) - f'_{t_r}(X_{t_r})) ]
                            = E[ 1_{Gamma_W} ( q' (1 + mubar) - Abar'_{q'} ) ].                 (8.2)

(An indicator multiplies a conditional expectation here, and it is legitimate because the indicator
is `P_{t_r - 1}`-measurable; this is exactly where the deviator's ignorance of the CURRENT type is
used, and where a deviator who knew `X_{t_r}` in advance could have correlated its survival with
the type.) Let `Mon'` be the complement of the event of Lemma 3(a) in `E'`. On `Mon'`, by Lemma
3(b), `q'(1+mubar) - Abar'_{q'} <= q'(1 + mubar - tau) + 1 + 2 b_n(q')`, a nonnegative quantity;
everywhere `q'(1+mubar) - Abar'_{q'} <= 2N`. So, by Lemma 3(a) with `Gamma = Gamma_W`,

    E[ 1_{Gamma_W} U'^pri ] <= E[ 1_{Gamma_W} ( q'(1 + mubar - tau) + 1 + 2 b_n(q') ) ] + 2N . N n^{-4}.

*Deviating side, fallback.* Decompose on the switch index: for `q0 < N`,
`Gamma_W cap {q' = q0} in P_{t_{q0}}`, and the non-deviators of `E'` deliver capability in Stage 3.
Lemma 5 and `Vbar_i(b) >= tau` give

    E[ 1_{Gamma_W} U'^fb ] = sum_{q0 < N} E[ 1_{Gamma_W cap {q' = q0}} U'^fb ]
                          <= E[ 1_{Gamma_W} ( (1 + mubar - tau)(N - q') + R_K(n) ) ].

*Deviating side, total.* With `b_n` nondecreasing and `2N . N n^{-4} <= 2N n^{-3}`,

    E[ 1_{Gamma_W} U'^post ] <= E[ 1_{Gamma_W} ( (1 + mubar - tau) N + 1 + 2 b_n(N) + R_K(n) ) ] + 2N n^{-3}.   (8.3)

The same derivation holds with `Gamma_W` replaced by any sub-event in `P_{t_1(b)}`; we use it on
`Gamma_W cap Lambda^c` below, where `Lambda := {i honest} cap {tau <= mubar} in P_{t_1(b)}`.

*Baseline side on `Gamma_W cap Lambda^c`.* In `E*`, `i` wins at price `tau <= Mbar_i(b)` and plays
`S*_N`; if strategic, or honest with `tau > mubar`, (W1) gives predictable mean exactly `tau` at
every primary pull. By the identity (8.2) for `E*` (with `f*` the water-filling response, whose
`pi_b`-mean is `tau`), `E[1 U*^pri] = E[1 q*(1 + mubar - tau)]` on this event, and `U*^fb >= 0`. By
Lemma 3(c), `P(Gamma_W cap Lambda^c cap {switch in E*}) <= N (2n^4)^{-1}`, and `q* = N` without a
switch. Since `0 <= 1 + mubar - tau <= 2`,

    E[ 1_{Gamma_W cap Lambda^c} U*^post ] >= E[ 1_{Gamma_W cap Lambda^c} N (1 + mubar - tau) ] - 2N . N(2n^4)^{-1}.

Subtracting from (8.3) restricted to `Gamma_W cap Lambda^c`, the leading terms cancel exactly (the
same coefficient `1 + mubar - tau` multiplies `N` on both sides), and the difference on this event
is at most `P(Gamma_W cap Lambda^c)(1 + 2 b_n(N) + R_K(n)) + 2N n^{-3} + N n^{-3}`.

*`Gamma_W cap Lambda`* (`i` honest, `tau <= mubar`). Baseline: (W2), target `mu_i(X_t)` almost
surely, per-pull utility 1, predictable mean `mubar >= tau`, so by Lemma 3(c) the baseline switch
has probability at most `N(2n^4)^{-1}` on this event, and `E[1 U*^post] >= E[1 q*] >=
N P(Gamma_W cap Lambda) - N . N (2n^4)^{-1}`. Deviation: honesty gives every target `>= mu_i(X_t)`,
so every post-bid selection is worth at most 1, and `U'^post <= N`. Difference at most
`N n^{-3}/2`.

*Sum for `i in Tbar(b)`.* Adding `G^c`, `Gamma_L`, `Gamma_W cap Lambda^c`, `Gamma_W cap Lambda`
(disjoint, covering the post-bid part) and the Stage-1 term,

    E[U'_i(b)] - E[U*_i(b)] <= l_i(b) + 1 + 2 b_n(N) + R_K(n) + N (2 n^{-4} + n^{-3} + 3 n^{-3} + n^{-3}/2)
                            <= l_i(b) + 1 + 2 b_n(N) + R_K(n) + 8 N n^{-3}.                      (8.4)

**The winning branch, `i notin Tbar(b)`, `4 s <= deltabar := deltabar_i(b)`.** On `G`,
`Vbar_i(b) = Mbar_i(b) + deltabar >= 4s`, so `tau >= Vbar_i(b) - 2s` and
`tau - Mbar_i(b) >= deltabar - 2s >= deltabar/2`. On `Gamma_W cap Mon'`: Lemma 3(b) gives
`Abar'_{q'} >= q' tau - 1 - 2 b_n(q')`, and feasibility with (F2) gives
`Abar'_{q'} <= q' Mbar_i(b)` (each predictable mean is a `pi_b`-average of a response `<= M_i`).
Subtracting, `q' deltabar/2 <= 1 + sqrt(2 q' ell) <= sqrt(q')(1 + sqrt(2 ell))` for `q' >= 1`, so
`q' <= 4(1 + sqrt(2 ell))^2/deltabar^2`. With `U'^pri <= 2 q'` pathwise and Lemma 3(a),
`E[1_{Gamma_W} U'^pri] <= 8(1+sqrt(2ell))^2/deltabar^2 + 2N n^{-3}`. Lemma 5 (second display),
summed over `q0` as above, gives `E[1_{Gamma_W} U'^fb] <= 2 R_K(n)/deltabar`. The baseline is
nonnegative. With `G^c` and `Gamma_L`,

    E[U'_i(b)] - E[U*_i(b)] <= l_i(b) + 8(1+sqrt(2 ell))^2/deltabar^2 + 2 R_K(n)/deltabar + 8 N n^{-3}.   (8.5)

If `4s > deltabar`: `E[U'_i(b)] - E[U*_i(b)] <= l_i(b) + 2N`. The knife edge `deltabar = 0` belongs to
`i in Tbar(b)` and never reaches (8.5).

**Summation.** Sum (8.4), (8.5) and the trivial branch over `b` through (8.1), with
`sum_b N_b <= n`: the first display of (A) holds conditionally on `B = beta`, with a right side that
does not depend on `S'`. Integrating over `beta` gives the first display; the supremum over
`B^N#_{i,n}` may then be taken because the bound is uniform. The simplified display:
`sum_b l_i(b) <= min{Q_B L, n}` pathwise; `E[2 b_n(N_b)] <= sqrt(2 ell) sqrt(E N_b)` (Jensen) and
`sum_b sqrt(E N_b) <= sqrt(Q_B n)` (Cauchy-Schwarz over the `Q_B` labels); the `1`s and the
`R_K(n)`s contribute at most `Q_B` and `Q_B R_K(n)`. QED

Every place an indicator multiplies a conditional expectation in this proof, listed (the recurring
error shape of this project): (8.2) for `E'` and for `E*` (indicator `1_{Gamma} 1{q >= r}` in
`P_{t_r - 1}`, conditional expectation given `P_{t_r - 1}`); Lemma 5 inside the fallback bound
(indicator `1_{Gamma_W cap {q' = q0}}` in `P_{t_{q0}} subseteq P_{t-1}` at every fallback round
`t`); Lemma 3(a),(c) (indicator in `P_{t_1(b)}`, supermartingale started at `t_1(b)`). In each the
indicator is measurable with respect to the conditioning field; no other conditional expectation is
multiplied by an indicator.

Union bounds over random index sets, listed: Lemma 3 unions over `r <= N_b` (deterministic given
`B`); the bad events are summed over labels with `V_b >= KL` (a `B`-measurable set) with weights
`N_b`, `sum_b N_b <= n`; Lemma 2 unions over agents and subsets (fixed). No union is taken over a
set that depends on rewards, targets or types.

============================================================================================
## 9. Proof of Theorem N (B), and the benchmark lemma

All agents play `S*_N`; given `B`. `P(n;S) = E sum_t Y_t = E sum_t m_{I_t,t}` (tower at each fixed
`t`). Fix `b`. If `V_b < KL` charge `V_b Mbar_(2)(b) <= min{V_b, KL}` (deliveries are `>= 0`). Let
`V_b >= KL`, `N := N_b`; charge the `KL` Stage-1 visits `KL`. Let `G^all := G^all(b) in P_{t_1(b)}`
(Lemma 2(ii)). On `G^all`, the winner's predictable mean is `lambda_W(b, tau_b) >= min{tau_b,
Mbar_W(b)} = tau_b` (Lemmas 2(ii), 6(i)).

Primary: as in (8.2), `E[1_{G^all} sum_{r <= q} m_{t_r}] = E[1_{G^all} Abar_q] >= E[1_{G^all} tau_b q]`
(the indicator `1_{G^all} 1{q >= r}` is in `P_{t_r - 1}`, and `E[m_{t_r} | P_{t_r-1}] = mbar_{t_r}`
by (F3)). Fallback: for each `q0 < N`, `G^all cap {q = q0} in P_{t_{q0}}`; Lemma 4 with a comparator
`j in Tbar(b)` (`rbar_{j,t} = Mbar_*(b) >= Mbar_(2)(b) >= tau_b`) gives
`E[1_{G^all cap {q=q0}} sum_{r > q0} m_{t_r}] = E[1_{G^all cap {q=q0}} sum_{r > q0} Y_{t_r}] >=
E[1_{G^all cap {q = q0}} (tau_b (N - q0) - R_K(n))]` (first equality: tower at `P^I_t`, indicator in
`P_{t-1}`). Summing over `q0` and adding the primary,

    E[ sum_{r<=N} m_{t_r} ] >= E[ 1_{G^all} tau_b N ] - R_K(n) >= (Mbar_(2)(b) - 2s) N - N n^{-4} - R_K(n),

using `tau_b >= Mbar_(2)(b) - 2s` on `G^all`, and, if `Mbar_(2)(b) - 2s >= 0`,
`E[1_{G^all}] >= 1 - n^{-4}`, while if it is negative the bound is trivial. Hence

    E[ delivered at b ] >= V_b Mbar_(2)(b) - [ min{V_b, KL} + 2 s N_b + R_K(n) 1{V_b >= KL} + N_b n^{-4} ].

Sum over `b` (`sum_b min{V_b, KL} <= min{Q_B K L, n}`, `sum_b N_b <= n`, at most `Q_B` labels) and
integrate over `B`: `sum_b V_b Mbar_(2)(b) = sum_t Mbar_(2)(B_t)`. This is (B). QED

**Lemma B (label benchmark versus true-type benchmark).** Assume `Lab = A`, (N1).
(i) For every `b`: `E[M_(2)(X_t) | B, B_t = b] - Mbar_(2)(b) <= e_b max_a M_(2)(a)`.
(ii) For every `b`: `E[b(X_t) | B, B_t = b] - bbar(b) <= e_b max_a b(a)`; and if `K_H = {h}`,
`bbar(b) = E[b(X_t) | B, B_t = b]`.
(iii) The constant in (i) is attained: `K = 3`, `A = {a, c}`, `M(a) = (1,1,0)`, `M(c) = (0,1,1)`,
`pi_a = (1-e, e)`, `pi_c = (e, 1-e)`, `e <= 1/2`: `M_(2) = 1` at both types,
`Mbar_(2) = 1 - e` at both labels, so the loss is `e = e max_a M_(2)(a)`.
Consequently `E sum_t Mbar_(2)(B_t) >= E sum_t M_(2)(X_t) - epsbar n max_a M_(2)(a)` and
`E sum_t bbar(B_t) >= E sum_t b(X_t) - epsbar n max_a b(a)`.

Proof. By (N1) on `Omega`, `E[g(X_t) | B] = sum_a pi_{B_t}(a) g(a)`. (i) Let `j1 != j2` be two agents
with `min{M_{j1}(b), M_{j2}(b)} = M_(2)(b)` (the top two at type `b`). The second largest entry of a
vector is at least the minimum of any two of its entries, and `Mbar_j(b) >= pi_b(b) M_j(b) =
(1 - e_b) M_j(b)` because `M_j >= 0`; so `Mbar_(2)(b) >= (1 - e_b) M_(2)(b)`. On the other side
`sum_a pi_b(a) M_(2)(a) <= (1 - e_b) M_(2)(b) + e_b max_a M_(2)(a)`. Subtract. (ii) Same with
`h* in K_H` attaining `b(b) = mu_{h*}(b)`: `bbar(b) >= mubar_{h*}(b) >= (1 - e_b) b(b)`. With one honest
agent `bbar(b) = mubar_h(b) = sum_a pi_b(a) mu_h(a)`. (iii) Direct computation. For the sums:
`E[e_{B_t}] = E[P(X_t != B_t | B)] = P(X_t != B_t)`, and `sum_t P(X_t != B_t) = epsbar n`. QED

Numerical check (`prover1/bench_check.py`, output `out_bench_check.txt`): 199613 random instances
(`K` in 2..6, `|A|` in 2..7, Dirichlet posteriors, random `M`, `mu`, honest sets): no violation of
(i) or (ii); the worst ratio of loss to bound is `1.0000` for both, i.e. the bounds are attained;
the worst ratio against the scout's `e_b(omega + omega_2)` is also `1.0000` (attained when
`omega_2 = 0`, as in (iii)). So the scout's bound is valid but loose by up to a factor 2, and its
"tight up to the factor 2" is resolved: the right constant is `max_a M_(2)(a) <= 1`, attained.

Remarks. The mixing gap can be negative (the label benchmark can exceed the type benchmark; the
scout found this on 3 of 10 item-5 subsets), so (i) is one-sided. When `Lab != A` (labels are
coarser classes, as in Proposition I), (i) and (ii) have no analogue without a relation between
the primitives and the class map; only the label benchmark is meaningful then.

============================================================================================
## 10. Proof of Theorem N (C)

Any feasible profile `S`, every `S_j in B^N#_{j,n}`, honest agents honest; given `B`. Fix `b`, and
`h in K_H` with `mubar_h(b) = bbar(b)`. If `V_b < KL` charge `min{V_b, KL}`. Let `V_b >= KL`,
`N := N_b`, charge `KL` for Stage 1. Let `Bev := {beta_{h,b} >= bbar(b) - s} in P_{t_1(b)}`; by
Lemma 2(iv), `P(Bev^c) <= (2Kn^4)^{-1}` (Stage-1 schedule reward independent, so `h` gets `L` pulls
under every profile). Let `Mon` be the complement of the event of Lemma 3(a) at `b`.

Primary. `E[sum_{r<=q} m_{t_r}] = E[Abar_q] >= E[1_{Bev} Abar_q]` (identity as in (8.2), `Abar >= 0`).
On `Bev cap {W = h}`: every primary predictable mean is `>= mubar_h(b) = bbar(b)` by honesty and (F2),
so `Abar_q >= bbar(b) q`. On `Bev cap {W != h} cap Mon`: `beta_{h,b} <= beta_{(2),b}` (the second
order statistic with multiplicity dominates every bid other than one copy of the maximum), so
`tau_b >= bbar(b) - 2s`, and Lemma 3(b) gives `Abar_q >= q tau_b - 1 - 2 b_n(q)`. In both cases
`Abar_q >= (bbar(b) - 2s) q - 1 - 2 b_n(N)`. On `Mon^c`, `Abar_q >= 0 >= (bbar(b) - 2s) q - 1 -
2b_n(N) - N`. With Lemma 3(a) (`Gamma = Omega`), `E[1_{Bev} Abar_q] >= E[1_{Bev}((bbar(b) - 2s)q)]
- 1 - 2 b_n(N) - N . N n^{-4}`.

Fallback. For `q0 < N`, `Bev cap {q = q0} in P_{t_{q0}}`, and `h`'s predictable mean at every
fallback pull is `>= mubar_h(b) = bbar(b)` by honesty, whatever `h`'s strategy and whatever the
others do; Lemma 4 gives `E[1_{Bev cap {q=q0}} sum_{r>q0} m_{t_r}] >= E[1_{Bev cap {q = q0}}
(bbar(b)(N - q0) - R_K(n))]`.

Adding, `E[delivered at b] >= V_b bbar(b) - [min{V_b, KL} + 2sN + 1 + 2 b_n(N) + R_K(n) +
N ((2Kn^4)^{-1} + n^{-3})]`. Summing over labels with the Jensen and Cauchy-Schwarz steps of
Section 8, `sum_b N((2Kn^4)^{-1} + n^{-3}) <= n^{-2}(1 + (2Kn^2)^{-1}) <= 3 n^{-2}`, and integrating
over `B` gives (C). The two benchmark statements are Lemma B(ii). QED

No independence across agents, and no property of any agent other than `h`'s honesty, is used.

============================================================================================
## 11. Proof of Theorem N (Conv)

Given `B`, fix `j`, `b` with `V_b >= KL`, and any behaviour of the others in `B^N#`. Let
`E_j := {beta_{j,b} <= Mbar_j(b) + s}`; `P(E_j^c) <= (2Kn^4)^{-1}` by Lemma 2(iii). On
`{W_b = j} cap E_j` (an event in `P_{t_1(b)}`), `tau_b = (beta_{(2),b} - s)_+ <= (beta_{j,b} - s)_+ <=
Mbar_j(b)`, so the hypothesis gives predictable means `>= min{tau_b, Mbar_j(b)} = tau_b` at every
primary pull, and Lemma 3(c) gives `P({W_b = j} cap E_j cap {switch}) <= N_b (2n^4)^{-1}`. Hence
`P(W_b = j, switch) <= (2Kn^4)^{-1} + N_b (2n^4)^{-1}`. Summing over the labels with `V_b >= KL`
(`B`-measurable, at most `Q_B`), with `sum_b N_b <= n`, gives the second claim. If all agents play
`S*_N`, `P(switch at b) <= sum_j P(E_j^c) + P({switch} cap E_{W_b}) <= K (2Kn^4)^{-1} +
N_b(2n^4)^{-1}`, where the second term is ONE application of Lemma 3(c) to the event
`E_{W_b} = union_j ({W_b = j} cap E_j) in P_{t_1(b)}` (not `K` applications). Summing gives the third
claim. QED

What (Conv) says, and does not say. It is the formal version of the scout's "zero false
convictions": a winner that meets the price on average over the queries carrying its label is
switched out with probability `O(n^{-3})` per label, uniformly over what everyone else does.
It is NOT a statement about the paper's pointwise rule `min{tau, M_j(X_t)}`, whose label mean is
`tau - sh_b` with the scout's shortfall `sh_b = sum_a pi_b(a) (tau - M_j(a))_+`; for that rule
Lemma 3(a),(b) show the switch occurs within about `(1 + 2 b_n)/sh_b` primary pulls on the good
event, which is the item-5 mechanism of failure.

============================================================================================
## 12. Proof of Corollary L (D-learn)

Replace `S*_N` by `S^L` throughout. Lemma 1(f) makes `pihat_{j,b}` the same in `E'` and `E*`.
Put `T(b) := {TV(pihat_{j,b}, pi_b) <= kappa_n for every j in [K]} in P_{t_1(b)}`;
`P(T(b)^c) <= K n^{-4}` (Lemma 2(v)).

(A). Replace `G` by `G cap T(b)` (probability of the complement at most `(K+1) n^{-4}`).
Losing branch: on `G cap T(b)`, `tau_b <= Mbar_W(b)` as before, and Lemma 6(ii) gives predictable
mean `>= min{tau_b, Mbar_W(b)} = tau_b`; the rest is unchanged. Winning branch, `i in Tbar(b)`:
the deviating side is unchanged (it never used the baseline profile, only the non-deviators'
Stage-3 rule, which is still "deliver capability"). Baseline, on `Gamma_W cap Lambda^c`:
Lemma 6(ii) with `tau <= Mbar_i(b)` gives predictable mean in `[tau, tau + 2 kappa_n]` (for honest
`i` with `tau > mubar`, `max{mubar, tau} = tau`), so by (8.2) and Lemma 3(c),
`E[1 U*^post] >= E[1 N(1 + mubar - tau - 2 kappa_n)] - 2N . N(2n^4)^{-1}`: the cancellation now
leaves `2 kappa_n N` on this event. On `Gamma_W cap Lambda`: predictable mean in
`[mubar, mubar + 2 kappa_n]`, so the baseline expected per-pull utility is at least `1 - 2 kappa_n`
(by (F3), `E[1 + mu_i(X) - f(X) | P_{t-1}] = 1 + mubar - mbar`), the switch probability is still
`<= N(2n^4)^{-1}` (mean `>= mubar >= tau`), and the deviator gets at most 1 per pull: difference
`<= 2 kappa_n N + N n^{-3}/2`. Non-top branch: unchanged. Bad events: `2N (K+1) n^{-4}` in place of
`2N n^{-4}`, i.e. an extra `2KN n^{-4}`, summing to at most `2K n^{-3} <= 2(K+1) n^{-3}`.
(B). Replace `G^all` by `G^all cap T(b)`, probability of complement `<= (K+1) n^{-4}`; on it the
winner's predictable mean is `>= min{tau_b, Mbar_W(b)} = tau_b` by Lemma 6(ii); the rest unchanged,
with `N_b n^{-4}` replaced by `(K+1) N_b n^{-4}`. (C) does not involve the profile. (Conv): the
hypothesis "predictable mean `>= min{tau_b, Mbar_j(b)}`" holds on `{TV(pihat_{j,b}, pi_b) <=
kappa_n}`, so add `n^{-4}`. QED

Rate of the extra term: `kappa_n^2 = (|A| log 2 + 4 log n)/(2L)` with `L >= n^{2/3}(log(en))^{1/3}`
for `n` beyond `2K`-dependent small values, so `2 kappa_n n = O(n^{2/3} (|A| + log n)^{1/2}
(log n)^{-1/6})`.

============================================================================================
## 13. Proof of Proposition I

### 13.1 Every random draw in Proposition I

Nature: the true-type path (`P1` deterministic; `P2` with i.i.d. second-half types) and, given it,
the labels `B_t ~ C(X_t, .)` independently. Mechanism: its coins, represented by an i.i.d.
Uniform`[0,1]` sequence `zeta = (zeta_t)` read in order (any randomisation whose conditional law is a
measurable function of the observable past is `G_t(observables, zeta_t)`), plus nothing else. Agents:
coin arrays `theta` drawn before round 1, independent of the paths. Seeds `U_t` i.i.d. uniform. The
hypothesis is that the path is exogenous: `(theta, zeta, U)` are mutually independent and
independent of `(X, B)`, and `B` given `X` is as stated. No (N) is assumed.

### 13.2 (a): one space, pathwise equality

Build one space with `(theta, zeta, U)` and an independent i.i.d. Uniform`[0,1]` sequence `V`. Put
`B_t := a` for `t <= n/2` and, for `t > n/2`, `B_t := a` if `V_t <= eps`, `c` otherwise. World 1
(`P1`): `X_t := a` for `t <= n/2`, `c` after. World 2 (`P2`): `X_t := a` for `t <= n/2`; for
`t > n/2`, `X_t := a` if `V_t <= eps`, `d` otherwise. In world 1, `B_t ~ C(c, .)` i.i.d. in the
second half and `B_t = a = kappa(a)` in the first, as required; in world 2, `X_t` has the law of
`P2` and `B_t = a` iff `X_t = a`, which is `C(a, .) = delta_a`, `C(d, .) = delta_c`, as required;
in both, `(X, B)` is independent of `(theta, zeta, U)`. So each world's execution has its model
law on this space.

Induction on `t`: suppose the observables (labels, mechanism coins used, selections, messages,
targets, rewards) of rounds `< t` coincide in world 1 under `(sigma, others)` and world 2 under
`(sigma~, others)`. Round `t`: the labels coincide by construction; the mechanism's selection and
message are the same function of the same observables and `zeta_t`; if the selected agent is 2 or
3, its target is the same function of its own history (which contains no true type), its message
and `theta_j`; if it is `W`, in world 2 `sigma~` delivers `sigma(t, htilde, xtilde_t, message,
theta_W)` where `htilde` is `W`'s world-2 history with every true type replaced by the `P1` type of
its round, which by the induction hypothesis is exactly `W`'s world-1 history, and `xtilde_t` is the
`P1` type at `t`, so the target equals world 1's. The seed is the same, so the reward is. QED for
the observables. Feasibility of `sigma~` on `P2`: for `t <= n/2`, `xtilde_t = a = X_t`; for
`t > n/2`, `sigma` is feasible on `P1` at type `c`, so it delivers in `[0, M_W(c)] = {0}`, and `0`
is feasible at every type. `W`'s realised utility is `sum_t 1{I_t = W}(1 - m_{W,t})` (`mu_W = 0`),
a function of the observables, hence equal in the two worlds pathwise, hence in expectation.

### 13.3 (b): the identity

Compare `(P2, sigma~)` and `(P2, sigma)`. By hypothesis they deliver the same targets as functions
of the observables at rounds `t <= n/2`, so the same induction (both in world 2, same primitives)
shows the first-half observables coincide pathwise, and so do `W`'s first-half utilities. Second
half, world 2: under `sigma~`, `W` delivers `0`, so its second-half utility is `N^II_W` exactly.
Under `sigma`, at a label-`c` round the type is `d`, `M_W(d) = 0`, so `W` delivers `0` (utility 1);
at a label-`a` round the type is `a` and `W` delivers `m_{W,t}` (utility `1 - m_{W,t}`). So its
second-half utility is `N^II_W - sum_{t > n/2, B_t = a, I_t = W} m_{W,t}`. Therefore

    G = E_{P2,sigma~}[N^II_W] - E_{P2,sigma}[N^II_W] + D = E_{P1,sigma}[N^II_W] - E_{P2,sigma}[N^II_W] + D = -P + D,

the middle step by (a) (`N^II_W` is a function of the observables). QED

### 13.4 (c): CL-MESP

`P2` satisfies (X) and (N) with `Lab = {a, c}`, `pi_a = delta_a`, `pi_c = delta_d`: given `B`, the
true types are the deterministic function `X_t = a` if `B_t = a`, `d` if `B_t = c`, and seeds,
priorities, fallback coins and agent coins are fresh and independent of the path. `P1` violates
(N1): at label `a` the type is `a` for `t <= n/2` and `c` for `t > n/2`, so no fixed kernel `pi_a`
works (with `eps > 0` both occur with positive probability).

Take `sigma = S*` (the paper's pointwise profile: capability in Stages 1 and 3, `min{tau, M_W(X_t)}`
in Stage 2) for `W`, and `S*` for agents 2 and 3 (their capability is `1/2` at every type, so `S*`
does not read types). On `P2`, `S*_W = S*_{N,W}`: at label `a` the posterior is `delta_a` and the
water-filling at level `min{tau, 1} = tau` delivers `tau = min{tau, M_W(a)}`; at label `c` the level
is `min{tau, 0} = 0`. The hypothesis of (b) holds since `S*` reads the current type only. The
deviation `sigma~` ("S* in the first half, 0 in the second") is in `B^N#_{W,n}`.

Theorem N(A) on `P2`, `i = W`: `Mbar_W(a) = 1 > 1/2 = Vbar_W(a)`, so `W in Tbar(a)`;
`Mbar_W(c) = 0`, `Vbar_W(c) = 1/2`, `deltabar_W(c) = 1/2`. For `4s <= 1/2`, (A) gives
`G <= E[l_W(a) + l_W(c)] + 1 + 2 b_n(n) + R_K(n) + 8(1+sqrt(2 ell))^2 . 4 + 2 R_K(n) . 2 + 8n^{-2}
<= Delta_n`.

`D` on `P2` under `S*`: `n/2 >= KL` (since `L <= n/(2K)`), so Stage 1 at `a` ends in the first half.
`W`'s Stage-1 rewards at `a` are `1{U_t <= 1} = 1`, so `beta_{W,a} = 1`. On
`G(a) := {|beta_{j,a} - 1/2| <= s, j = 2, 3}` (`P(G(a)^c) <= 4 e^{-2Ls^2} <= n^{-4}`), since
`s < 1/2`, `W` is the strict largest bidder and `tau_a in [1/2 - 2s, 1/2]`; `W` delivers `tau_a` at
every primary pull (type `a`), so its predictable mean is `tau_a`, and by Theorem N(Conv)'s argument
(Lemma 3(c)) the switch at `a` has probability at most `V_a (2n^4)^{-1} <= (2n^3)^{-1}`. On
`G(a) cap {no switch}` every second-half label-`a` round is a primary pull of `W` with target
`tau_a >= 1/2 - 2s`. With `R^a := #{t > n/2 : B_t = a} ~ Bin(n/2, eps)`, `R^a <= n/2`:

    D >= (1/2 - 2s) E[R^a] - (n/2)(n^{-4} + (2n^3)^{-1}) >= (1/2 - 2s) eps n/2 - n^{-2}.

Then `P = D - G >= (1/2 - 2s) eps n/2 - Delta_n - n^{-2}`, with `2s eps n/2 <= s n =
O(n^{2/3}(log n)^{1/3})` and `Delta_n = O(n^{2/3}(log n)^{1/3})`. QED

### 13.5 (d): direct conviction on `P1`

On `P1` the first half is as above: on `G(a)`, `W` wins `a` at `tau_a in [1/2 - 2s, 1/2]` and delivers
`tau_a` on the `r1 := n/2 - KL` first-half primary pulls (a deterministic type path is a degenerate
kernel, so (F1) to (F3) and Lemma 3 hold on `P1` with `pi` replaced by the point mass at the current
type; Lemma 3 used only the conditional law of `X_t` given `P_{t-1}`, not its stationarity). In the
second half `W`'s label-`a` targets are `min{tau_a, M_W(c)} = 0`. On `G(a) cap Mon` (Lemma 3(a),
probability of failure at most `n^{-4} + n^{-3}`), if no switch has occurred by primary index
`r = r1 + k`, then `r tau_a - b_n(r) <= Z_r <= Abar_r + b_n(r) = r1 tau_a + b_n(r)`, so
`k tau_a <= 2 b_n(r) <= sqrt(2 n ell)`, i.e. `k <= sqrt(2n ell)/(1/2 - 2s)`. So if `R^a >= k_n`, the
switch occurs. Hence `P(W switched out at a) >= 1 - P(R^a < k_n) - n^{-4} - n^{-3}`. For fixed
`eps > 0`, `k_n = O(sqrt(n log n)) = o(eps n)`, so `P(R^a < k_n) -> 0` exponentially (Hoeffding),
and the pointwise-compliant winner is convicted with probability tending to one, after which it
receives the label-`a` fallback allocations only, `O(R_K(n))` in expectation by Lemma 5 (its
capability there is 0 against `1/2`). QED

### 13.6 What Proposition I does and does not show

* It is an exact identity for every label-measurable mechanism, not an inequality with an
  `O(sqrt n)` slack: `G + P = D`. The scout's corollary (shading gain at least
  `(1/2 - alpha) eps n/2 - O(sqrt n)`) does not follow from it for a general mechanism, because a
  mechanism may punish at the OTHER label (`P` counts all second-half allocations, including the
  label-`c` rounds, each worth 1 to `W`). With that channel included the dichotomy is between the
  shading gain `G` and the total withholding `P`, and the identity says they sum to `D`.
* The dichotomy is quantitative only when `D` is of order `eps n`, i.e. when the mechanism, on the
  (N)-path `P2`, lets its compliant top agent deliver on a constant share of the second-half
  label-`a` rounds. A mechanism that simply never allocates `W` in the second half has `D = 0`, no
  shading gain and no withholding relative to `P2`; it is excluded by nothing in the identity, and
  it is not a good mechanism (it would give up the top agent at label `a` on every instance), but
  Proposition I does not formalise "good". The statement that is fully proved is the CL-MESP one,
  (c) and (d).
* With `eps = 0` the construction is void (`R^a = 0`, `D = 0`), consistent with c2's
  order-robust theorem for noise-free contexts.
* It does not prove the scout's positive counterpart `N(delta)` (posterior drift `delta` in TV costs
  `2 delta n`). I believe the analogue holds by replacing `pi_b` in (F3) by a `delta`-close kernel and
  shading the price by `2 delta`, but I did not write it.

============================================================================================
## 14. Reuse of c2 and of the paper, lemma by lemma

| source lemma | what it says there | what changes here | re-verified where |
|:-|:-|:-|:-|
| c2P1 Section 4.2, paper "standing conditioning" | condition on the context path `A`; everything local becomes deterministic | condition on the LABEL path `B` only; true types stay random and become primitives of a canonical space (Lemma C); this is the rewrite the scout flagged | Section 6 |
| c2P1 Lemma 3 (L3a to L3c), paper `lem:ctx-locality` | mechanism and non-deviators at `z` read only `z` | unchanged for the mechanism; non-deviators' Stage-1 rule "deliver `M_j(X_t)`" is identical in both executions because `X_t` is common | Lemma 1(b) |
| c2P1 Lemma 4, paper `lem:ctx-bid` | pathwise bid domination, winner inclusion, common price, `l_i(z)` | pathwise steps need the same `X_t` in both executions; bids now estimate LABEL means `Mbar_j(b)` | Lemma 1 |
| c2P1 (6.5), (6.6), paper (eq:ctx-price) | Hoeffding for bids, `(V - 2s)_+ <= tau <= V` | Bernoulli(`Mbar_j(b)`) i.i.d. given `B` (needs (N1), (N4)); `V -> Vbar` | Lemma 2 |
| c2P1 Lemma 4b | conditional Azuma | used verbatim | Lemma 2(iv), Lemma 3 |
| c2P1 Lemma 5, paper `lem:ctx-monitor` | anytime monitor, `A_q >= q tau - 1 - 2b(q)`, compliant switch `<= (2n^3)^{-1}` | centring at the PRE-TYPE predictable mean; the compliant clause is about label means; union over `r <= N_b` deterministic given `B` | Lemma 3 |
| c2P1 Lemmas 6, 7; paper `lem:ctx-fallback` | EXP3 prefix bound with reactive agents | field `P_{t-1}` (before the type); comparator condition on predictable means; fallback length deterministic given `B` and the switch index; indicator of an event in `P_{t_{q0}}` carried through | Lemma 4 |
| c2P1 Lemma 8, paper fallback display | deviator's fallback utility | the type-dependent `mu_i(X_t)` is averaged using independence of the selection coin from the type given `P_{t-1}` (N3) | Lemma 5 |
| c2P1 Section 6.4, paper losing branch | the winner meets the price, so no induced fallback | the winner meets the price ON AVERAGE over its label, which is all Lemma 3(c) needs | Section 8 |
| c2P1 Section 6.5, paper top branch | exact cancellation at the common price | the cancelled coefficient is `1 + mubar_i(b) - tau`, obtained by the identity (8.2) with a `P_{t_r-1}`-measurable indicator on both sides; honest case via (W2) | Section 8 |
| c2P1 Section 6.6, paper non-top branch | tenure `O(log n / delta^2)` | predictable means `<= Mbar_i(b)` by feasibility | Section 8 |
| c2P1 Sections 7, 8; paper (ii), (iii) | revenue and honest robustness | predictable means in place of pathwise targets; benchmark comparison Lemma B is new | Sections 9, 10 |
| c2 adversary F2 | pairwise versus mutual independence | (N) in conditional form, witnesses 3.3d | Section 3 |
| c2 adversary F4 | joint field `D_z` ill defined across executions | primitive filtration `P_t` from the start | Section 6.1 |
| c2 adversary F5 | random excluded index set | not applicable (global time) | Lemma 3 |
| c2 adversary F1 | endogenous arrivals make (i) false | same here for labels; and Proposition I shows a second, noise-specific failure for endogenous-looking ORDER of true types even with exogenous labels | Section 13 |

============================================================================================
## 15. The least secure step, and what survives if it fails

**Least secure: Lemma C together with hypothesis (N).** Everything in part (A) that is pathwise
(Lemma 1: common Stage-1 rounds, common bids of non-deviators, bid domination, winner inclusion,
common price, the `l_i(b)` charge) needs the two executions to see the SAME true type at every
round. In c2 this came free, because the context was observed and conditioned on. Here the true
type is unobserved by the mechanism and random, and the two executions can only share it if the
type is a primitive whose law does not react to anything either execution did. Lemma C derives
that from (N1) (fresh given everything before, including the agents' coins and all past types) and
(X), by the chain rule for the law of the execution. I believe the proof is complete. The ways it
could still be wrong, in the order I would attack:

1. A modelling gap in "everything realised before": if the model lets an agent draw private
   randomness AFTER seeing `X_t` in a way correlated with future types (for example, the agent is
   also the prompt source), (N1) as stated forbids it, but a reader may not notice that the
   hypothesis says this. Remark 3.3e is the sentence that says it.
2. The "types are primitives" step silently assumes the true type at round `t` is well defined in
   both executions at the same round. That holds because labels, hence visit schedules, are
   exogenous (D0, (X)). If the label of a round could depend on the providers' past behaviour
   (e.g. the classifier is retrained on provider outputs), the schedules separate and part (A)
   fails exactly as c2 adversary F1 shows for contexts.
3. (F2): the response function `f_t(a)` must be `P_{t-1}`-measurable. It is, because the only
   round-`t` inputs to a target are `X_t` and the selection event (the priority is in `P_0`, the
   message is a function of the label's state). A mechanism that sent a message depending on a
   round-`t` coin other than the selection would need (F2) re-checked.

What survives if Lemma C fails: parts (B), (C) and (Conv) do not compare two executions. Each of
their lemmas (2(ii) to 2(v), 3, 4) is a statement about ONE execution and uses only (N1), (N3),
(N4) for that execution: they may be re-proved on the natural filtration `O_t` of Section 3.2
directly (replace `P_{t-1}` by `O_{t-1}` throughout; (F1) to (F3) are then (N1), (N3), (N4)
themselves), with no canonical space. Only part (A), Corollary L(A), and Proposition I(c) (which
uses (A)) would fall. Proposition I(a), (b), (d) do not use Lemma C.

**Second least secure: the class `B^N#`.** It lets the deviator read other agents' coin arrays and
all past seeds. Every lemma is uniform over `P_{t-1}`-measurable responses, so this is covered;
but a reader who finds the class unnatural can restrict to `B^N`, and nothing changes.

**Third: Proposition I(b) is an identity whose interpretation needs `D` of order `eps n`.** For
CL-MESP this is proved ((c), (d)); for a general mechanism it is an assumption about the mechanism
(Section 13.6), and the scout's mechanism-independent corollary is false without it (Section 17,
item 9).

============================================================================================
## 16. What I did not establish

1. General (non-linear) costs. With convex `phi_i`, the label-level cost of a response with label
   mean `lambda` is minimised by water-filling (for strictly convex `phi`, the KKT conditions of
   `min sum_a pi_b(a) phi(m(a))` subject to the mean and the box give `m = clip(c, lo, M)`), which is
   why I chose that rule. But part (A)'s cancellation would then need the paper's
   `lem:cost-convert` for the function `C_b(lambda) := min{ sum_a pi_b(a) phi_i(m(a)) : mean
   lambda, lo <= m <= M }` rather than for `phi_i`; I expect `C_b` to be convex, nondecreasing and
   `Lambda`-Lipschitz, which is what the paper's argument needs, but I did not verify it.
2. The converse direction of (D) (the `Q_B L` term is attained). I expect the paper's
   `prop:ctx-finite-tight` to carry over with labels, and did not re-verify.
3. The scout's `N(delta)` positive counterpart.
4. That the D-learn margin `kappa_n` is necessary or optimal; only that it suffices.
5. That label-level compliance is the ONLY notion enforceable: the scout's Remark I' (type-level
   compliance is unidentifiable from labels) is plausible and I did not write it out.
6. Anything about correlated equilibria, multiple deviators in (A), or exact equilibrium.

============================================================================================
## 17. Statements of `SCOUT.md` that I found false or had to change

1. **(N) as the scout writes it** is correct in spirit; I kept its content, restated it in the
   named-field conditional form of `f1 FINAL.md`, and derived the scout's product form as Lemma C
   (a consequence, not the hypothesis). The scout's claim "(N) is equivalent to: given `B`, all
   primitives are mutually independent" is true on the canonical space, but "primitive" there must
   include the true types, and the equivalence needs (X).
2. **The deviation class**: enlarged (round index, all past types, all past realised quantities).
   The scout's "NOT future true types" is not an extra restriction but is (N1) itself (Remark 3.3e).
3. **(B) benchmark constant.** Scout: `E Mbar_(2)(B) >= E M_(2)(X) - eps(omega + omega_2) >=
   E M_(2)(X) - 2 eps`, "tight up to the factor 2". Valid, but the right bound is
   `eps max_a M_(2)(a) <= eps`, and it is attained exactly (the scout's own example). Also the
   scout's `TV(P_B, p) <= eps` step is unnecessary: the per-round tower argument gives the sum
   directly, with `epsbar` the AVERAGE per-round misclassification probability (no stationarity of
   the label law needed). Requires `Lab = A`.
4. **(C) with several honest agents.** Scout: loss at most `2 eps`. Right bound: `eps max_a b(a)`.
5. **Honest conviction.** Scout: "each label's monitor fires with probability at most
   `(2n^3)^{-1}`". Precisely: `(2Kn^4)^{-1} + N_b(2n^4)^{-1}` per label for a compliant winner,
   whatever the others do; the total over labels is `Q_B (2Kn^4)^{-1} + (2n^3)^{-1}`, not
   `Q_B (2n^3)^{-1}` (the scout's per-label figure summed over labels would give the latter; the
   union over `(b, r)` with `sum_b N_b <= n` is tighter). For D-learn the scout's
   `Q_B(n^{-3} + n^{-4})` becomes `Q_B((2Kn^4)^{-1} + n^{-4}) + (2n^3)^{-1}`.
6. **D-learn in (A).** Scout: extra `n gamma`. Correct figure for the scout's own rule: `2 kappa_n n`
   (estimation error acts in both directions; Lemma 6(ii)). With `kappa_n` equal to the scout's
   `gamma`.
7. **(D) "sub-linear iff".** Only "if" is proved here.
8. **Proposition I, construction.** (a) Type `d` is misclassified with probability one unless labels
   name CLASSES of types (`d` in class `c`); I made the class map explicit. (b) The shading strategy
   must read the round index (or simulate the `P1` history); the scout's class did not include `t`.
9. **Proposition I, corollary: false as stated for a general label-measurable mechanism.** The scout
   claims shading beats compliance on `P2` by at least `(1/2 - alpha) eps n/2 - O(sqrt n)`, with
   `alpha` the withheld fraction of second-half label-`a` rounds on `P1`. Counterexample mechanism:
   label `a` always goes to `W`; label `c` goes to `W` in the second half as long as `W`'s
   second-half label-`a` reward rate is at least `1/4`, and to agent 2 otherwise. On `P1` with the
   cooperative `W`, `alpha = 0`. On `P2`, compliance (`1/2` at label `a`) keeps the label-`c` rounds
   (each worth 1 to `W`), shading loses them: `G = D - P = eps n/4 - (1 - eps) n/2 + O(sqrt n)`,
   NEGATIVE for `eps < 2/3`, while the scout's bound says `>= eps n/4 - O(sqrt n)`. The identity
   `G + P = D` (with `P` counting ALL second-half allocations) is what is true. For CL-MESP, which
   cannot punish across labels (Lemma 1, locality), the scout's conclusion does hold, and (c), (d)
   prove it.
10. **Remark on the scout's reading of the simulation.** Consistent with my own runs
    (`prover1/out_exp_conv.txt`): under i.i.d. pairs the label-level rules are never switched out
    (0/40 and 0/40), the pointwise rule always is (40/40); under bursty order the label-level rule is
    switched out in 11/40 runs, D-learn in 4/40.

============================================================================================
## 18. Numerical checks (`prover1/`)

All run on the login node with the project venv, single core, under a minute each. These are
falsification attempts of intermediate claims and sanity checks of the statements; none is
evidence of equilibrium.

1. `bench_check.py` -> `out_bench_check.txt`: Lemma B(i), (ii) on 199613 random instances, no
   violation, worst ratio `1.0000` (attained); tight example reproduced at `e = 0.05, 0.2, 0.5`.
2. `clmesp.py`: event-level simulator of CL-MESP keyed on labels with the paper's parameters, the
   water-filling rule of Section 2.2, D-learn, EXP3 fallback, common-random-number interface
   (shared labels, types, seeds, fallback coins, priorities, as in Lemma C).
3. `exp_conv.py 60000 40` -> `out_exp_conv.txt`: `K = 3`, three types, uniform noise
   `eps = 0.3`, pointwise shortfalls `sh = (0.074, 0.083, 0)`. Fraction of runs with any switch:
   i.i.d. pairs: pointwise `40/40`, label-level `0/40`, D-learn `0/40`; bursty order (stay
   probability 0.995, violates (N1)): pointwise `40/40`, label-level `11/40`, D-learn `4/40`.
   Revenue per round: label `0.533`, D-learn `0.571` (the margin is paid by the winner),
   pointwise `0.551` (bought with false convictions). Benchmark `E Mbar_(2)(B) = 0.5647`,
   `E M_(2)(X) = 0.5550` (here mixing raises the benchmark; Lemma B(i) is one-sided).
4. `exp_dev.py 60000 1 20` -> `out_exp_dev.txt`: agent 0 (top at labels 0 and 1) deviating from
   `S*_N`, common random numbers, 20 seeds. Mean gains: pointwise rule `-2525` (it is switched out),
   Stage-1 underbid by `0.15`: `+1088`, smooth primary shading `tau - 1.5/sqrt(r)`: `+513`, both:
   `+1601`; the Theorem N(A) bound at these visit counts is `28918` (dominated by
   `2 R_K(n)/deltabar` and `Q_B L`; at `n = 6 x 10^4` it is not informative about the rate, as in
   c2P1 T4).
5. `exp_propI.py 0.2 40000 30` -> `out_exp_propI.txt`: Proposition I with CL-MESP. The allocation
   logs of `(P1, S*)` and `(P2, sigma~)` are identical pathwise in 30/30 runs, and so are `W`'s
   utilities (max difference `0`); `G + P - D` is `0` pathwise up to `3e-9` (floating point); mean
   `G = -809` (shading is caught on `P2`), `P = 2481 >= eps n/4 = 2000`, `D = 1672 >=
   (1/2 - 2s) eps n/2 = 1269`; `W` is switched out at label `a` in 30/30 runs on `P1` and 0/30 on
   `P2`.
