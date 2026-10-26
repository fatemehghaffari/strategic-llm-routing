# F1 explorer report: private capacities, continuous contexts, behavioural deviations

Worker: the explorer on track F1, 18 September 2026. Output scope:
`audit/round2/B/theorems/f1-continuous-private/EXPLORER.md` and the scratchpad. No canonical file
was modified. No em dash and no triple hyphen appears in this file.

Read in full before starting: `audit/round2/prompts/COMMON.md`;
`audit/round2/B/theorems/f1-continuous-private/TASK.md` including the section headed
"STATE OF THIS TRACK, 18 September 2026", which is the operative instruction;
`SCEPTIC.md` in this directory; `c2-local-mesp/PROVER2.md` Sections 2 to 4 and Section 9;
`c2-local-mesp/PROVER1.md` Sections 2 and 3; `c2-local-mesp/ADVERSARY.md` Sections 5 and 6;
`audit/round2/B/CONTEXT_PROOF_CONTRACT.md`; `sections/Private_information_setting.tex`;
`sections/appendix_private.tex`; `audit/round2/B/theorems/separation/REPORT.md` Part 2;
`audit/round2/B/theorems/c4-safe-partitions/REPORT.md` Section 0.

I do not claim any result below is correct. I claim I wrote a mechanism, a statement with every
hypothesis named, and a proof of each part from lemmas proved here. Section 11 names the step I
consider least secure and lists what I did not do.

## 0. Headline

**0.1 The main positive result.** Section 3 gives a mechanism, **CG-MESP** (continuous grid
monitored empirical second price), Section 4 its hypotheses and Section 6 a theorem for it with
three parts: an additive
behavioural equilibrium, second-capacity revenue, and honest-benchmark robustness under arbitrary
joint behaviour, all on a continuum of contexts with private capacities, at rate

    O( n^{(m+2)/(m+3)} log n )

with `m` the dimension of the grid the mechanism prices on. Taking `m = D` (the profile grid) this
is proved in full and matches the exponent of the manuscript's public contextual theorem
`thm:grid-etc`. The hypotheses are: Lipschitz capacities and Lipschitz intrinsic means (the
manuscript assumes Lipschitz intrinsic means and continuous capacities), exogenous arrivals, and
`n >= exp(3L)`. **It does not need i.i.d. arrivals**, which every contextual theorem in the
manuscript does need (contract Section 11), and it needs no top-set condition, no boundary
regularity, no positive-mass condition and no `nu`-null boundary.

**0.2 The three obstacles named by PROVER2 Section 9 item 1 are removed by one device.** They are:
a cell-average bid is not a capacity; the announced price may exceed an agent's capacity at some
contexts inside a cell and not at others; bid domination loses its fixed comparison target. The
device is a **price shaded by an oscillation allowance**

    tau_C := ( beta_(2),C  -  3 s_n  -  rho_n )_+ ,     rho_n := sqrt(m) h_n log(en) ,

which is larger than the manuscript's `s_n` by `2 s_n + rho_n`. Lemma 5 shows that on a good
bidding event the *realised winner*, whoever it is and however it bid, has `M_W(x_W) > tau_C` at
**every** context of the cell. So the proposed profile delivers the constant `tau_C` pointwise
inside a cell, the cell-average bid never has to be a capacity, and the monitor is again a test
against a constant. Bid domination never had a fixed comparison target: its target is the
counterfactual capacity-play bid `beta^max_{i,C}` under the same seeds, which is a random variable
in the scalar proof too (`sections/appendix_private.tex`, "Bidding coupling").

**0.3 A by-product that simplifies the scalar theorem.** Putting the deviator's own counterfactual
bid `beta^max_i` into the good event (it is deviation independent, because the Stage-1 schedule is
reward independent) makes the price at most the winner's capacity on **every** winning history,
so the non-top branch of `thm:private-mesp` becomes vacuous. That removes the instance constants
`delta_i` and the threshold `4 s_n <= delta_i` from the deviation bound, and with them the caveat
"not uniform over sequences whose positive capacity gaps vanish". Section 7.4. This is a claim
about the manuscript's own scalar proof and it should be checked by a second reader before use.

**0.4 The formalisation the coordinator asked for.** Section 2 formalises identifiability from
below: an imitation lemma, a one-sided identifiability corollary (the platform's knowledge of a
capacity function is always an *upper set* of functions, so no statistic of the platform's
information is an upper confidence bound on any agent's capacity at any context), and the
continuum-specific consequence that **smoothness propagates lower bounds only**. Section 2.6 draws
the design rule this implies and shows the rule is exactly what CG-MESP obeys and what
three otherwise attractive designs violate, including the sceptic's F-S3 and route 4 of the brief.

**0.5 The per-agent architecture, honestly.** Section 8 builds the per-agent version (`m = d`) and
proves its pricing half: the elicitation cost, the price slack and the monitoring slack really are
`O(K n^{(d+2)/(d+3)} log n)`, so the coordinator's exponent is correct **for pricing**. The
mechanism does not close, and Section 8.3 names the exact place. The fallback that carries
honest-benchmark robustness must also *deter*, which requires it to supply a comparator value within
`O(n^{-1/(d+3)})` of the announced price. That comparator value is
`V_i(X) = max_{j != i} M_j(x_j)`, a genuine function of the whole profile, so the fallback must
operate on `D`-dimensional regions **at the pricing resolution**, which costs
`Omega( n^{(D+d+3)/(2(d+3))} )`. That exceeds `n^{(d+2)/(d+3)}` unless `D <= d+1`, that is unless
`K = 2` and `d = 1`, and it exceeds CG-MESP's own `n^{(D+2)/(D+3)}` as soon as `D >= 3`. So:
**the per-agent architecture reaches `n^{3/4}` when `K = 2, d = 1`, and is worse than CG-MESP
otherwise.** Section 8.4 also records that the sceptic's comparison inequality
`(D+1)/(D+2) < (d+2)/(d+3)` is equivalent to `D <= d` and is never satisfiable in this model, so its
Section 2.2 conclusion that the Grid-EXP3 fallback is cheaper than the pricing cost is false as
stated. Section 8.6 is the one route I found that would reach `n^{(d+2)/(d+3)}` for all `K`, and I
did not take it.

**0.6 What I did not get.** No lower bound. No proof that the `J L` elicitation term is necessary.
No mechanism for non-Lipschitz capacities. No anytime version. The per-agent theorem is not proved.

## 1. Setting and notation

I follow `CONTEXT_PROOF_CONTRACT.md` throughout. Agents `i in [K]`, `K >= 2`, horizon `n` known to
the platform. Context space `X = [0,1)^D`, `D = Kd`, profiles `X_t = (x_{1,t},...,x_{K,t})` with
`x_{i,t} in [0,1)^d`. Primitives `mu_i : [0,1)^d -> [0,1]` and `M_i : [0,1)^d -> [0,1]` with
`M_i >= mu_i`, both functions of agent `i`'s own coordinate only (contract Section 2; adversary
finding F6). At a round the platform selects `I_t`, the selected agent chooses
`m_{I_t,t} in [0, M_{I_t}(x_{I_t,t})]`, and `Y_t = 1{ U_t <= m_{I_t,t} }` for a fresh uniform seed
`U_t`. Cost `c_{i,t} = m_{i,t} - mu_i(x_{i,t})`; per-pull utility `1 + mu_i(x_i) - m_{i,t} in [0,2]`.

`M_*(X) = max_i M_i(x_i)`, `M_(2)(X)` the second largest of `(M_1(x_1),...,M_K(x_K))` counted with
multiplicity, `V_i(X) = max_{j != i} M_j(x_j)`, `b(X) = max_{h in K_H} mu_h(x_h)`,
`P(n;S) = E_S sum_{t<=n} Y_t`.

Deviation class: `B^ctx_{i,n}` of contract Section 5, enlarged as in `separation/REPORT.md` (H2) so
that an agent may also condition on the entire arrival path. Write `B^ctx+_{i,n}`. Honest agents
satisfy `m_{h,t} >= mu_h(x_{h,t})` after every history.

`log` is natural, `(x)_+ = max(x,0)`, `|.|` is the Euclidean norm.

## 2. Identifiability from below, formalised

This section answers the item the coordinator names as the deepest obstacle. Nothing in it is
specific to any mechanism. Section 2.5 turns it into a design rule and Section 2.6 applies the rule
to four proposals, three of which it kills.

### 2.1 The model of what the platform can learn

Fix an agent `j`. A *capacity function* is an element of a class `F`; the running choice is
`F_L := { M : [0,1)^d -> [0,1] , M is L-Lipschitz }` and, where honesty matters,
`F_L(mu) := { M in F_L : M >= mu }`. A *behaviour* `sigma` for agent `j` is a nonanticipating rule
that, at each round at which `j` is selected, outputs a target `m in [0,1]` measurable with respect
to `j`'s own history and private randomness. Say `sigma` is *`M`-feasible* if `m <= M(x_{j,t})`
almost surely at every selected round. The platform's *record* at the end of round `n` is
`I_n := sigma( X_1,...,X_n, I_1,...,I_n, Y_1,...,Y_n, own coins, own messages )`; it does **not**
contain any target.

### 2.2 Lemma 1 (imitation)

**Lemma 1.** Let `M, M' in F` with `M' <= M` pointwise, and let `sigma` be `M'`-feasible. Then
`sigma` is `M`-feasible, and for any mechanism and any behaviours of the other agents, the joint law
of `(X_1..X_n, I_1..I_n, Y_1..Y_n, all mechanism coins, all messages)` is the same when agent `j`
has capacity `M` and plays `sigma` as when it has capacity `M'` and plays `sigma`.

*Proof.* `M'`-feasibility means `m <= M'(x_{j,t}) <= M(x_{j,t})` a.s., which is `M`-feasibility.
The capacity function enters the construction of the probability space at exactly one place, the
constraint set of the selected agent's target; it appears in no transition kernel. Given the
targets, the conditional law of `Y_t` is `Bernoulli(m_{I_t,t})` in both instances, the mechanism's
kernels are the same measurable functions of the record, and the other agents' kernels are
functions of their own histories, which are generated by the same recursion. The two joint laws are
therefore built from identical kernels and identical initial data. `QED`

The lemma is elementary. Its value is that it is the exact sense in which "an agent of capacity `M`
can imitate any smaller capacity": not approximately, not in distribution over a subclass, but as
an identity of laws on the platform's entire record, for every mechanism and every horizon.

### 2.3 Corollary 2 (one-sided identifiability: there is no upper confidence bound)

**Corollary 2.** Fix a mechanism, an agent `j`, a context `y in [0,1)^d`, a horizon `n` and
`delta in [0,1)`. Let `U` be any `[0,1]`-valued statistic of the platform's record `I_n`. Suppose
`U` is a valid upper confidence bound at `y`, that is, for every `M in F_L`, every `M`-feasible
behaviour of `j` and every behaviour of the others,

    Pr( U >= M(y) )  >=  1 - delta .

Then for every `M' in F_L`, every `M'`-feasible behaviour and every behaviour of the others,
`Pr( U = 1 ) >= 1 - delta`. That is, the only valid uniform upper confidence bound on a capacity is
the trivial one.

*Proof.* Fix `M'` and an `M'`-feasible `sigma`. Put `M := max{ M', 1 - L |. - y| }` pointwise. It is
a maximum of two `L`-Lipschitz functions into `[0,1]`, hence lies in `F_L`; it satisfies `M >= M'`
and `M(y) = 1`. By Lemma 1 the law of `I_n`, and hence of `U`, is the same under `(M, sigma)` as
under `(M', sigma)`. Applying the hypothesis at the instance `M` gives
`Pr_{(M,sigma)}( U >= M(y) ) = Pr_{(M,sigma)}(U >= 1) >= 1 - delta`, and the two probabilities
agree. `QED`

If honesty is imposed, the same proof works inside `F_L(mu_j)`, since `M >= M' >= mu_j`. The
corollary is stated for a single `y`; the version "no statistic upper bounds `M_j` at any point" is
immediate.

### 2.4 Proposition 3 (the identifiable set is the order filter above a lower envelope)

To make the statement as strong as possible, give the platform *more* than it has: let it observe
the realised targets, not only the rewards.

**Proposition 3.** Suppose agent `j` was pulled at contexts `x_1,...,x_r` and the platform observed
the realised targets `m_1,...,m_r`. Define the *revealed envelope*

    E(y)  :=  max_{q <= r} ( m_q - L |y - x_q| )_+ ,        E := 0 if r = 0 .

Then `E in F_L`, and `{ M in F_L : M is consistent with the observation }  =  { M in F_L : M >= E }`.

*Proof.* Consistency means `m_q <= M(x_q)` for every `q`. If `M` is consistent then for every `y`
and every `q`, `M(y) >= M(x_q) - L|y - x_q| >= m_q - L|y-x_q|`, and `M >= 0`, so `M >= E`.
Conversely if `M in F_L` and `M >= E` then `M(x_q) >= E(x_q) >= m_q`. Finally each
`y -> (m_q - L|y-x_q|)_+` is `L`-Lipschitz with values in `[0,1]`, and a finite maximum of
`L`-Lipschitz functions is `L`-Lipschitz. `QED`

Three consequences, in order of how much they matter.

(i) **The knowledge set is an upper set.** It has a least element `E` and no greatest element other
than the class maximum. This is Corollary 2 restated structurally.

(ii) **Smoothness propagates lower bounds and only lower bounds.** One reveal of value `m` at `x`
certifies `M(y) >= m - L|y-x|` on a whole ball, and certifies nothing above. So, contrary to the
intuition that a continuum is harder because there are more points to learn, *the continuum is the
regime in which a single revelation is worth a neighbourhood*. On a finite context set with
unrelated primitives (PROVER2 hypothesis (H1)) a reveal at `z` is worth nothing at `z' != z`.

(iii) **The agent chooses the envelope.** The pairs `(x_q, m_q)` are chosen by the agent inside
`[0, M(x_q)]`, so for any `E_0 in F_L` with `E_0 <= M` the agent can deliver `m_q = E_0(x_q)` and
the revealed envelope is then sandwiched, `E_0 - 2 L dist(., {x_q}) <= E <= E_0`. Up to twice `L`
times the fill distance of the pull design, the agent dictates what the platform learns. This is
the "chooses where to reveal" point, and the sandwich says the platform's only defence is the fill
distance of its design, that is, the resolution of its elicitation.

### 2.5 Proposition 4 (the elicitation count is a covering number, with no probability in it)

The sceptic's Section 2.3 asserts that metric entropy forces `(L/eps)^d` effective observations and
flags, correctly, that the standard minimax lower bound does not apply because the observations are
not a regression design. The following is the design version, which needs no minimax theorem, no
noise and no strategic behaviour, and is therefore not exposed to that objection.

**Proposition 4.** Fix `eps in (0, 1/4]` and `L >= 4 eps`. Let `x_1,...,x_r in [0,1)^d` be any
design and let `hat M` be any map from `(x_q, M(x_q))_{q <= r}` (full noiseless revelation) to
functions on `[0,1)^d`. If

    sup_{M in F_L}  || hat M - M ||_infinity  <  eps / 2 ,

then `{x_1,...,x_r}` is an `eps/L`-net of `[0,1)^d`, and consequently
`r >= ( floor( L / (2 eps) ) )^d`.

*Proof.* Suppose some `y in [0,1)^d` has `|y - x_q| > eps/L` for every `q`. Put `M_1 :≡ eps` and
`M_2(.) := eps + ( eps - L |. - y| )_+`. Both are `L`-Lipschitz with values in `[0, 2 eps] subset
[0,1]`, so both lie in `F_L`. At every design point `M_2(x_q) = eps = M_1(x_q)`, because
`L|x_q - y| > eps`. Hence `hat M` receives identical data on the two instances and outputs the same
function `g`. But `M_2(y) - M_1(y) = eps`, so
`max{ ||g - M_1||_inf , ||g - M_2||_inf } >= eps/2`, contradicting the hypothesis. Therefore the
design is an `eps/L`-net. A set of `N` points whose `eps/L`-balls cover `[0,1)^d` satisfies
`N (2 eps/L)^d >= 1` in volume, hence `N >= (L/(2 eps))^d`; taking the integer floor gives the
display. `QED`

**How Proposition 4 produces the target exponent, and what part of that is not proved.** The price
must be accurate to `eps` at every context, or the revenue loses `n eps`. Proposition 4 says the
mechanism must elicit each agent at a `eps/L`-net, that is, at `Theta((L/eps)^d)` distinct
locations. It says nothing about how many *pulls* each location costs. If one grants the standard
Bernoulli count, that resolving a mean to accuracy `eps` costs `Theta(eps^{-2})` pulls, the total
elicitation is `Theta( K L^d eps^{-(d+2)} )` rounds, and balancing against `n eps` gives
`eps = Theta(n^{-1/(d+3)})` and total cost `Theta(n^{(d+2)/(d+3)})`, with a per-location block of
`eps^{-2} = n^{2/(d+3)}` pulls. That is exactly the coordinator's re-solved balance, and exactly the
sceptic's `L* = n^{2/(m+3)}`. **The covering half is proved here; the Bernoulli half is not a
theorem in this report and I do not claim it.** What Proposition 4 does add over the sceptic's
Section 2.3 is that the count survives the objection the sceptic himself raised against it: it is
a statement about designs and function classes, with no estimator, no noise model and no
assumption that the observations are unbiased.

### 2.6 The design rule that Section 2 implies, and what it kills

**Rule (envelope safety).** Any decision a mechanism must get right *under arbitrary behaviour*
may depend on an agent's capacity only through a quantity that (i) is monotone nondecreasing in the
revealed envelope and (ii) is required only to be a **lower** bound on that agent's capacity at the
contexts where the decision binds. A decision requiring an upper bound on any agent's capacity
cannot be uniformly correct, by Corollary 2.

Four consequences.

1. **Second pricing with shading is envelope safe, and this is why the literature's mechanisms
   have the shape they have.** The one thing the price must satisfy uniformly is
   `tau <= M_W(x_W)` at every context where the winner is charged; the price is built from the
   runner-up's revealed envelope and is therefore a lower bound on it, and the auction guarantees
   `beta_(2) <= beta_W`, which is a lower bound on the *winner's* envelope. Section 5 Lemma 5 is
   exactly this argument made quantitative on a cell.
2. **No mechanism can guarantee second-capacity revenue uniformly over behaviour.** Take `K = 2`,
   no contexts, `M_1 = M_2 = 1`, `mu_1 = mu_2 = 0`, both strategic. The profile in which both
   agents always deliver `0` is feasible and gives `P(n;S) = 0`, while `E sum_t M_(2)(X_t) = n`.
   Hence part (B) of any theorem here is necessarily a statement at a proposed profile, and part
   (C) is necessarily against the honest benchmark. This is one line, but it is the reason the
   three-part shape of `thm:private-mesp` is not a stylistic choice.
3. **Route 4 of the brief ("remove the bidding phase; derive the price from other agents' ongoing
   realised performance near the context") is envelope safe for the price but not for the
   revenue.** Deriving `tau` from other agents' realised deliveries keeps `tau` a lower bound on
   those agents' capacities, which is all the monitor needs. What it loses is that nothing makes
   those agents deliver their capacity at the contexts where the price is being formed, so the
   revenue statement (B) collapses to a statement about what the agents happened to deliver. A
   dedicated bidding block is not an estimation device that a cleverer estimator could replace; it
   is the *only* place in the mechanism where an agent has a reason to reveal, because the auction
   is decided there. Corollary 2 says no amount of observation substitutes for that reason.
4. **The sceptic's F-S3 (an asymmetric elicitation schedule: race to certify the ranking, then
   price off the runner-up alone) is unsafe for a different reason, and the reason is the C4
   converse.** A racing schedule stops pulling an agent on a *reward* event. The bid-domination
   coupling (`sections/appendix_private.tex`, "Bidding coupling"; PROVER1 Lemma 4; PROVER2 Lemma B)
   needs the deviating and the capacity-play executions to pull the same agent at the same round
   during elicitation, so that the same seed is used and `Y' <= Y^max` holds pathwise. Under a
   racing schedule the two executions diverge in *which agent is pulled when* as soon as one bid
   differs, and the coupling has nothing to compare. This is the same failure that
   `c4-safe-partitions/REPORT.md` Section 0 proves for reward-dependent partitions: not that the
   per-block statistics break, but that the two executions of the coupling carry different
   schedules. F-S3 therefore needs either a context-only sandwich on the race (the accelerate-only
   escape of C4 Section 4.7) or a new argument. I did not build one.

## 3. The mechanism CG-MESP

The platform knows `n`, `K` and `D`. It does not know `nu`, `L`, any `mu_i`, any `M_i`, or `K_H`.

**Parameters.**

```
g_n     := ceil( n^{1/(D+3)} ) ,   h_n := 1/g_n ,   J_n := g_n^D          (grid)
L_n     := ceil( n^{2/(D+3)} )                                            (bidding block)
ell_n   := log( 2 K n^5 )
s_n     := sqrt( ell_n / (2 L_n) )                                        (bid radius)
rho_n   := sqrt(D) h_n log(en)                                            (oscillation allowance)
sigma_n := 3 s_n + rho_n                                                  (price shading)
b_n(r)  := sqrt( r ell_n / 2 ) ,  b_n(0) := 0                             (monitor boundary)
R_K(H)  := 3 sqrt( K H log K ) + 2 K log K ,  R_K(0) := 0
R^dbl_K(V) := 11 sqrt( K (V+1) log K ) + 2 K log K log_2( 2(V+1) ) ,  R^dbl_K(0) := 0
```

**Grid.** The `J_n` half-open cubes of side `h_n` tiling `[0,1)^D`. `C(X)` is the cube containing
`X`. The position of `X` inside its cube is used only to locate the cube: the rule is cell blind.
Cubes are instantiated lazily on first arrival, so `J_n` never has to be enumerated. Note
`diam(C) = sqrt(D) h_n` and, for `X, X' in C`, `|x_i - x'_i| <= sqrt(d) h_n <= sqrt(D) h_n` for
every `i`, so every `L`-Lipschitz function of any single agent's coordinate varies by at most
`L sqrt(D) h_n` on a cube.

**State per cube `C`.** A visit counter `V_C`; the Stage-1 reward sums; the price `tau_C`; the
winner `W_C`; the monitor count `r_C` and reward sum `Z_C`; the local fallback clock and EXP3
weights; one independent uniform priority permutation `Pi_C` of `[K]`, drawn when `C` is first met.

**Round `t`.** Observe `X_t`, set `C := C(X_t)`, increment `V_C`, act by `C`'s local phase.

* **Stage 1 (bidding), while `V_C <= K L_n`.** Pull agent `((V_C - 1) mod K) + 1`. Agent `i`'s
  `r`-th bidding pull at `C` is the `((r-1) K + i)`-th visit to `C`. The schedule is a
  deterministic function of the arrival path alone: it reads no reward, no bid and no coin.
  When `V_C = K L_n`, form `beta_{i,C} := L_n^{-1} sum_{r <= L_n} Y_{i,C,r}`, let `W_C` be a
  largest bidder with ties broken by highest `Pi_C` priority, let `beta_(2),C` be the second order
  statistic with multiplicity, announce

      tau_C := ( beta_(2),C - sigma_n )_+ ,

  and set `r_C := 0`, `Z_C := 0`. If `C` receives fewer than `K L_n` visits in the whole horizon,
  every visit to `C` is a bidding pull, and `C` never awards, never prices and never monitors.
* **Stage 2 (monitored primary), until a local switch.** Pull `W_C`; set `r_C := r_C + 1`,
  `Z_C := Z_C + Y_t`; if `Z_C < r_C tau_C - b_n(r_C)`, declare a local switch at `C`.
* **Stage 3 (local fallback), after a switch at `C`.** Explicit-exploration EXP3 over all `K`
  agents, restricted to visits to `C`, restarted in doubling epochs on the local fallback clock:
  epoch `k >= 0` covers local fallback times `2^k, ..., 2^{k+1}-1`, uses fresh weights
  `w_{j,1} = 1`, `gamma_k := min{1/2, sqrt(K log K / 2^k)}`, `eta_k := gamma_k/K`,
  `p_{j} := (1-gamma_k) q_j + gamma_k/K`, `hat Y_j := Y_t 1{I_t=j}/p_j`,
  `w_j := w_j exp(eta_k hat Y_j)`. No local horizon is used.
* **Messages.** A selected agent is told the current cube's phase and, in Stage 2 or 3, `tau_C`.

**Proposed profile `S^*`.** At a bidding pull and at a fallback pull at `C`, agent `j` delivers
`M_j(x_{j,t})`. At a Stage-2 pull at `C` the winner delivers `min{ tau_C, M_{W_C}(x_{W_C,t}) }` if
strategic and `max{ mu_{W_C}(x_{W_C,t}), min{ tau_C, M_{W_C}(x_{W_C,t}) } }` if honest. This is
feasible after every history and implementable from the messages, so `S^*_j in B^ctx+_{j,n}` for
every `j`, and honest components are honest. Lemma 5 shows that on a probability `1 - n^{-4}` event
the inner minimum is `tau_C` at every context of every awarded cube, so `S^*` delivers a *constant*
during Stage 2 at a cube.

**Three design points, each of which is doing work.**

1. The shading is `sigma_n = 3 s_n + rho_n`, not the manuscript's `s_n`. The `rho_n` pays for the
   within-cube oscillation of the capacity functions; the `3 s_n` pays for two bid radii and for
   the counterfactual bid of a deviator (Section 7.4).
2. The Stage-1 schedule is reward independent and context determined. This is what makes the bid
   domination coupling legitimate and it is the hypothesis that `c4-safe-partitions/REPORT.md`
   shows cannot be relaxed to a reward-dependent schedule.
3. The fallback restarts in doubling epochs because a cube's remaining local horizon is unknown.
   The constant `3(2 + sqrt 2) <= 11` is the one pinned in `separation/REPORT.md` Lemma B.

## 4. Hypotheses

**(A1) Agents and primitives.** `K >= 2`. `mu_i, M_i : [0,1)^d -> [0,1]` with `mu_i <= M_i`, and
both `L`-Lipschitz in the Euclidean norm, for a constant `L >= 0` **unknown to the platform**. A
fixed nonempty honest set `K_H subset [K]`.

**(A2) Horizon.** `n` is known to the platform, `n >= 2K`, and `log(en) >= 3 L`, that is
`n >= n_1(L) := exp(3L)`. All guarantees are fixed horizon; no anytime claim is made.

**(A3) Exogenous arrivals.** The arrival path `A := (X_1,...,X_n)` in `[0,1)^D` is independent of
the reward-seed array, of every mechanism coin and of every agent's private coin array. It is
otherwise arbitrary: **it need not be i.i.d.**, need not have a density, may be deterministic, and
may be chosen adversarially without access to the seeds and the coins.

**(A4) Reward generation.** `(U_t)_{t <= n}` are i.i.d. uniform on `[0,1]`, independent of `A`, of
the mechanism coins and of the agents' private coins. At round `t` the platform selects `I_t`, the
selected agent chooses `m_{I_t,t} in [0, M_{I_t}(x_{I_t,t})]`, and only then is
`Y_t := 1{U_t <= m_{I_t,t}}` realised.

**(A5) Deviator class.** For the equilibrium part, the deviating agent `i` uses any
`S'_{i,n} in B^ctx+_{i,n}`: after being selected at round `t` it chooses
`m_{i,t} in [0, M_i(x_{i,t})]` as an arbitrary measurable function of `n`, the entire arrival path,
its own whole history across all cubes, every message it received, and its private randomness;
honest agents satisfy `m_{i,t} >= mu_i(x_{i,t})` after every history. All other agents play
`S^*_{-i}`.

**(A6) Platform knowledge.** `n`, `K`, `D` only.

Note what is **not** assumed: no i.i.d. arrivals, no positive masses, no top-set condition, no
`nu`-null boundary, no finitely many top-stable components, no continuity of `nu`, no knowledge of
`L`. Compare `thm:grid-etc` and `thm:contextual-public`, which need i.i.d. arrivals (contract
Section 11), fixed ex ante maps (contract Section 12), and, for the equilibrium, all of the
structural conditions in contract Section 10.

## 5. Lemmas

### 5.0 Probability space, conditioning, and standing notation

Both executions compared in any coupling live on one space carrying: the arrival path `A`, the seed
array `(U_t)_{t<=n}`, the priorities `(Pi_C)`, the EXP3 coins, and every agent's private coin array,
all mutually independent by (A3), (A4) and the construction.

**Convention F-A.** All filtrations contain `sigma(A)` from time zero: `F_0 supseteq sigma(A)` and
`F_t := F_0 v sigma( U_1..U_t, coins used through round t )`. This is legitimate by (A3), it is
PROVER2's Convention F-A and it is the single place exogeneity is indispensable (PROVER2 Section 9,
least secure step). Under it every cube visit count `V_C`, every Stage-1 round, every Stage-1
schedule entry and every cube's set of rounds is `F_0`-measurable, hence deterministic once we
condition on `A`. All expectations below are conditional on `A` unless said otherwise; the
statements are uniform in `A`, so integrating at the end is immediate.

For a cube `C` write `n_C := (V_C - K L_n)_+` for its post-bidding visits, `t_{j,C,r}` for the
round of agent `j`'s `r`-th Stage-1 pull at `C` (an `F_0`-measurable integer),

    bar m_{j,C} := L_n^{-1} sum_{r <= L_n} M_j( x_{j, t_{j,C,r}} )              (F_0-measurable),
    M_j^inf(C)  := inf_{X in C} M_j(x_j) ,   M_j^sup(C) := sup_{X in C} M_j(x_j) .

**Fact 0 (oscillation).** For `X, X' in C` and any `j`, `|x_j - x'_j| <= sqrt(d) h_n`, so under (A1)
`|M_j(x_j) - M_j(x'_j)| <= L sqrt(d) h_n <= L sqrt(D) h_n <= rho_n / 3`, the last step by (A2)
(`log(en) >= 3L`). The same holds for `mu_j`, for `V_i`, for `M_*` and for `b`, each being a
pointwise maximum of `L`-Lipschitz functions of single coordinates. In particular
`M_j^sup(C) - M_j^inf(C) <= rho_n/3` and `bar m_{j,C} in [M_j^inf(C), M_j^sup(C)]`.

### 5.1 Lemma 2 (cube locality)

**Lemma 2.** The phase, the bids, the price, the winner, the switch time and the fallback
distribution at cube `C` are measurable functions of the rewards collected at visits to `C`, of
`Pi_C`, of the fallback coins used at `C`, and of `A`. In particular a switch at `C` changes
nothing at any other cube, and `tau_C` depends only on the Stage-1 rewards at `C`.

*Proof.* Every parameter of Section 3 is a deterministic function of `n`, `K`, `D`. Every per-cube
state variable is updated only at visits to `C` and only from data produced at those visits. The
grid is fixed before play. Induction on `t`. `QED`

Lemma 2 is a structural statement, not an estimate, and it is exactly the property ADVERSARY
Section 5.1 verifies for the finite mechanisms. It is what makes the accounting additive over cubes
even though a deviator may correlate its behaviour across cubes.

### 5.2 Lemma 3 (the good bidding event)

For each cube `C` and agent `j` let `beta^cap_{j,C}` be the bid `j` would produce at `C` if it
delivered `M_j(x_{j,t})` at each of its Stage-1 pulls at `C`, computed with the seeds
`(U_{t_{j,C,r}})_{r <= L_n}`. Under `S^*` this is the realised bid; under a unilateral deviation by
`i` it is the realised bid for `j != i` and the counterfactual capacity bid for `j = i`. Put

    G := { |beta^cap_{j,C} - bar m_{j,C}| <= s_n  for every j in [K] and every cube C that
           completes bidding } .

**Lemma 3.** `Pr(G) >= 1 - n^{-4}`, and `G` does not depend on any agent's behaviour.

*Proof.* Condition on `A`. The rounds `t_{j,C,r}` are `F_0`-measurable and distinct across
`(j,C,r)`, and each `1{U_{t_{j,C,r}} <= M_j(x_{j,t_{j,C,r}})}` is Bernoulli with `F_0`-measurable
mean `M_j(x_{j,t_{j,C,r}})`, independent across `(j,C,r)` because the seeds are. Hoeffding gives
`Pr( |beta^cap_{j,C} - bar m_{j,C}| > s_n ) <= 2 exp(-2 L_n s_n^2) = 2 e^{-ell_n} = (K n^5)^{-1}`.
At most `n` cubes are visited, so at most `K n` pairs `(j,C)` occur; the union bound gives
`K n (K n^5)^{-1} = n^{-4}`. Each `beta^cap_{j,C}` is a function of `A` and the seeds only, so `G`
is behaviour independent. Integrating over `A` preserves the bound. `QED`

### 5.3 Lemma 4 (bid domination and winner inclusion)

**Lemma 4.** Fix `i` and `S'_{i,n} in B^ctx+_{i,n}`, and couple the deviating execution with the
baseline execution under `S^*` by the same `A`, the same seed array, the same priorities, the same
EXP3 coins and the same private coins. Then, pathwise:

(a) The two executions have the same Stage-1 rounds at every cube and pull the same agent at each,
    and for `j != i` the Stage-1 rewards at every cube are identical.
(b) `beta'_{i,C} <= beta^cap_{i,C}` for every cube `C` that completes bidding.
(c) `{ i wins at C in the deviating execution } subset { i wins at C in the baseline execution }`.
(d) On `{ i wins at C in the deviating execution }`, `beta_(2),C = max_{j != i} beta_{j,C}` and
    `tau_C = ( max_{j != i} beta^cap_{j,C} - sigma_n )_+`, a function of `A`, of the seeds at the
    other agents' Stage-1 pulls at `C`, and of nothing agent `i` does.

*Proof.* (a) The Stage-1 rounds at `C` are the first `K L_n` visits to `C`, and the agent pulled at
the `v`-th visit is `((v-1) mod K) + 1`. Both are functions of `A` alone, hence identical in the two
executions. For `j != i` the target at such a round is `M_j(x_{j,t})`, a function of `A`, and the
seed `U_t` is shared, so `Y_{j,t}` is identical. (b) At agent `i`'s Stage-1 round `t` the deviating
target satisfies `m'_{i,t} <= M_i(x_{i,t})` by feasibility, so
`1{U_t <= m'_{i,t}} <= 1{U_t <= M_i(x_{i,t})}`; average over `r <= L_n`. (c) `i` wins in the
deviating execution iff `beta'_{i,C} > beta_{j,C}` for every `j` with lower `Pi_C` priority and
`beta'_{i,C} >= beta_{j,C}` for every `j` with higher priority. By (a) the `beta_{j,C}`, `j != i`,
are the same in both executions, and by (b) `beta^cap_{i,C} >= beta'_{i,C}`, so each of those
inequalities is preserved. (d) On that event `i`'s bid is a largest one, so the second order
statistic with multiplicity is the largest of the others' bids, which by (a) equals
`max_{j != i} beta^cap_{j,C}`. `QED`

Point (b) is the answer to PROVER2's "Lemma B loses its fixed comparison target". The comparison
target is not `M_i`, and was not `M_i` in the scalar proof either
(`sections/appendix_private.tex` defines `beta_i^max` for exactly this purpose). It is the
counterfactual capacity bid at the same rounds under the same seeds, which exists verbatim on a
continuum because the Stage-1 schedule is context determined.

### 5.4 Lemma 5 (the realised winner can meet the price at every context of its cube)

This is the lemma that removes PROVER2's second obstacle.

**Lemma 5.** On `G`, for every cube `C` that completes bidding, with winner `W := W_C`, and for
**every** `X in C`,

    tau_C  <=  M_W(x_W)  -  2 s_n  -  (2/3) rho_n   <   M_W(x_W) .

This holds whether `W` is a non-deviator or the deviator, and whatever the deviator bid.

*Proof.* `W` is a largest bidder, so `beta_(2),C <= beta_{W,C}`. If `W != i` then
`beta_{W,C} = beta^cap_{W,C}`; if `W = i` then `beta_{W,C} = beta'_{i,C} <= beta^cap_{i,C}` by
Lemma 4(b). Either way `beta_(2),C <= beta^cap_{W,C}`. On `G`,
`beta^cap_{W,C} <= bar m_{W,C} + s_n <= M_W^sup(C) + s_n`. By Fact 0, for every `X in C`,
`M_W^sup(C) <= M_W(x_W) + rho_n/3`. Hence
`beta_(2),C <= M_W(x_W) + rho_n/3 + s_n` and
`tau_C <= beta_(2),C - sigma_n <= M_W(x_W) + rho_n/3 + s_n - 3 s_n - rho_n`. `QED`

Three consequences, used repeatedly below.

* **(C1) `S^*` delivers a constant in Stage 2.** On `G`, at every Stage-2 pull at an awarded cube
  `C`, `min{tau_C, M_W(x_W)} = tau_C`. So a strategic winner following `S^*` delivers exactly
  `tau_C` at every such pull and an honest one delivers `max{mu_W(x_W), tau_C} >= tau_C`. The cube
  has been reduced to a scalar instance for the purposes of the monitor, and the fact that the
  bid was a cube average rather than a capacity has been paid for entirely by the shading.
* **(C2) There is no non-top branch.** On `G`, if the deviator wins at `C`, Lemma 5 with `W = i`
  gives `tau_C < M_i(x_i)` at every `X in C`, so `S^*_i` is feasible against the announced price at
  every context. No hypothesis on `V_i - M_i`, no instance gap `delta_i`, and no threshold on `n`
  of the form `4 s_n <= delta_i` appear anywhere.
* **(C3) The fallback comparator dominates the price.** On `G`, if the deviator wins at `C`, put
  `nu_i(C) := max_{j != i} M_j^inf(C)`. Let `j*` attain `max_{j != i} beta^cap_{j,C}`. Then
  `tau_C <= beta^cap_{j*,C} - sigma_n <= bar m_{j*,C} + s_n - sigma_n <= M_{j*}^sup(C) - 2 s_n -
  rho_n <= M_{j*}^inf(C) + rho_n/3 - 2 s_n - rho_n <= nu_i(C)`. So `tau_C <= nu_i(C) <= 1`, and
  therefore `1 + mu_i(x_i) - nu_i(C) >= 0` and `1 + mu_i(x_i) - nu_i(C) <= 1 + mu_i(x_i) - tau_C`.

### 5.5 Lemma 8 (the price is close to the second capacity, at `S^*`)

**Lemma 8.** Suppose every agent plays `S^*`. On `G`, for every cube `C` that completes bidding and
every `X in C`,

    tau_C  >=  M_(2)(X)  -  4 s_n  -  (4/3) rho_n .

*Proof.* On `G`, `|beta_{j,C} - bar m_{j,C}| <= s_n` for every `j`, and the `k`-th order statistic
is 1-Lipschitz in the supremum norm on `R^K`, so `beta_(2),C >= bar m_(2),C - s_n` where
`bar m_(2),C` is the second largest of `(bar m_{j,C})_j`. By Fact 0,
`bar m_{j,C} >= M_j^inf(C) >= M_j(x_j) - rho_n/3` for every `X in C` and every `j`; the second
order statistic is monotone in each argument, so `bar m_(2),C >= M_(2)(X) - rho_n/3`. Hence
`tau_C >= M_(2)(X) - rho_n/3 - s_n - sigma_n`. `QED`

### 5.6 Lemma 9 (per-cube honest comparator, pathwise)

**Lemma 9.** Assume (A1) and a nonempty `K_H`. For a cube `C` put
`v_C := max_{h in K_H} M_h^{inf,mu}(C)` where `M_h^{inf,mu}(C) := inf_{X in C} mu_h(x_h)`, and let
`h_C` attain the maximum (fixed tie-break). Then (i) `b(X) <= v_C + (2/3) rho_n` for every
`X in C`; (ii) whenever `h_C` is selected at a round with `X_t in C`, its conditional reward mean
is at least `v_C`, under any behaviour respecting honesty.

*Proof.* (i) Fix `X in C` and let `h` attain `b(X) = mu_h(x_h)`. By Fact 0,
`mu_h(x_h) <= M_h^{inf,mu}(C) + rho_n/3 <= v_C + rho_n/3`. (ii) Honesty gives
`m_{h_C,t} >= mu_{h_C}(x_{h_C,t}) >= M_{h_C}^{inf,mu}(C) = v_C` pointwise, and the seed is fresh.
`QED`

`h_C` depends on the instance and the grid only, never on play, so it is a legitimate fixed
comparator. This is `separation/REPORT.md` Lemma C with the cube constant taken as an infimum over
the cube instead of at a representative point, which removes a factor of two and, more importantly,
makes (ii) pathwise rather than in expectation.

### 5.7 Lemma 6 (anytime cube monitor against a globally adaptive winner)

Fix a cube `C`. Let `psi_s := 1{ round s is a Stage-2 pull at C }`, let `r_C(s)` be the number of
Stage-2 pulls at `C` up to and including round `s`, let `Y^C_r` be the reward at the `r`-th such
pull and `m^C_r` its target, and put `Z_r := sum_{q<=r} Y^C_q`, `A_r := sum_{q<=r} m^C_q`, with
`Z_0 = A_0 = 0`. Extend both by `0` increments beyond the number of Stage-2 pulls actually taken.
Let

    H := { for every cube C and every r <= n : | Z_r - A_r | <= b_n(r) } .

**Lemma 6.** Under (A3), (A4) and Convention F-A, and for any behaviour of every agent:

(a) `Pr(H) >= 1 - n^{-4}`, in each of the two coupled executions separately;
(b) on `H`, if the Stage-2 phase at `C` lasted `q` pulls (counting its failing pull when there is
    one), then `A_q >= q tau_C - 1 - 2 b_n(q)`;
(c) on `H`, the realised utility of the Stage-2 winner over that phase satisfies
    `U^pri <= q ( 1 + mu_W^sup(C) - tau_C ) + 1 + 2 b_n(q)`, where
    `mu_W^sup(C) := sup_{X in C} mu_W(x_W)`;
(d) on `H`, if every Stage-2 target at `C` is at least `tau_C`, no switch occurs at `C`;
(e) unconditionally, `E[ Z_r - A_r ] = 0` for the total number `r` of Stage-2 pulls at `C`.

*Proof.* `psi_s` is `F_{s-1}`-measurable: whether round `s` is a Stage-2 pull at `C` is determined
by `X_s` and `V_C` (both `F_0`-measurable under Convention F-A) and by whether `C` has already
awarded and not yet switched, which is a function of rewards at rounds before `s`. Consider
`N_t := sum_{s <= t} psi_s ( Y_s - m_{I_s,s} )`. The selected agent's target is measurable with
respect to `F_{s-1} v sigma(I_s, its private coin)`, and by (A4) the seed `U_s` is independent of
that field, so `E[ Y_s - m_{I_s,s} | F_{s-1} v sigma(I_s, coin) ] = 0` and, `psi_s` being
`F_{s-1}`-measurable, `E[ N_s - N_{s-1} | F_{s-1} ] = 0` with conditional range at most `1`. Hence
`N` is a martingale with conditionally bounded increments; the Hoeffding conditional moment bound
`E[ e^{lambda (Y_s - m)} | . ] <= e^{lambda^2/8}` gives, for each fixed `r`, by the stopped
exponential supermartingale evaluated at the (bounded) round of the `r`-th Stage-2 pull at `C`,
`Pr( |Z_r - A_r| > b_n(r) ) <= 2 exp( -2 b_n(r)^2 / r ) = 2 e^{-ell_n} = (K n^5)^{-1}`. The pairs
`(C,r)` with `r` no larger than the number of Stage-2 pulls at `C` number at most `n` in total,
because `sum_C (Stage-2 pulls at C) <= n`, and for larger `r` the increments are `0` so the event
cannot fail; the union bound gives `n (K n^5)^{-1} <= n^{-4}`, which is (a). (b): if no switch
occurred at any `r <= q` then `Z_q >= q tau_C - b_n(q)` and, on `H`, `A_q >= Z_q - b_n(q)`, so
`A_q >= q tau_C - 2 b_n(q)`; if the switch occurred at `q` apply this at `q-1` and use
`A_q >= A_{q-1}`, `tau_C <= 1` and `b_n(q-1) <= b_n(q)`. (c) is
`U^pri = sum_{r<=q} (1 + mu_W(x_{W,r}) - m^C_r) <= q(1 + mu_W^sup(C)) - A_q` with (b). (d): the
targets give `A_r >= r tau_C`, so on `H`, `Z_r >= A_r - b_n(r) >= r tau_C - b_n(r)` for every `r`,
which is exactly the negation of the switch test. (e) is optional stopping for the bounded stopping
time `n` applied to `N`, which needs no knowledge of why the phase ended; this is PROVER2's Lemma
M(d) and it is what makes cubes that stop being visited mid-monitoring harmless. `QED`

The least secure step in Lemma 6 is the `F_{s-1}`-measurability of `psi_s`, which holds **only**
because Convention F-A puts the whole arrival path in `F_0`. PROVER2 names the same step as the
least secure one in the finite case and the objection transfers verbatim; (A3) is what licenses it.

### 5.8 Lemma 7 (cube fallback with unknown local horizon, and the deviator's share)

**Lemma 7.** Fix a cube `C` at which a switch occurred, and let `H_C` be the number of fallback
visits to `C` (an `F_0`-measurable integer under Convention F-A, since the switch round is a
stopping time and the remaining visits are determined by `A`; the algorithm never uses `H_C`).
Suppose an agent `j*` has conditional reward mean at least `v` whenever it is selected at a visit
to `C`. Then

    E[ sum over fallback pulls at C of Y_t ]  >=  v H_C  -  R^dbl_K(H_C) .

*Proof.* This is `separation/REPORT.md` Lemma A and Lemma B applied to the cube's fallback clock,
with three checks. First, epoch `k` is tuned to its *planned* length `2^k` and its realised length
`T_k = min{2^k, (H_C - 2^k + 1)_+} <= 2^k` may be shorter; Lemma A there is stated for a
deterministic `T <= H_0` and is proved from the exponential potential inequality, which holds for
every prefix, so truncation is covered. Second, the filtration may carry the entire arrival path
and the agents' whole cross-cube histories, which Lemma A permits because it only requires `p_s` to
be `G_{s-1}`-measurable and the selection coin and the seed to be fresh; both hold by construction
and by (A4). Third, the doubling sum is Lemma B there, with the absolute constant `3(2+sqrt 2)`
rounded up to `11`, giving exactly `R^dbl_K` as defined in Section 3. `QED`

**Lemma 7b (the deviator's fallback utility at a cube).** Suppose agent `i` deviates, all others
play `S^*`, and a switch occurred at cube `C` with `H_C` fallback visits. Let `bar Q_i` and
`bar A_i` be the conditional expectations, given the fallback-start history, of `i`'s fallback pull
count and of the sum of its fallback targets at `C`, and put `nu_i(C) := max_{j != i} M_j^inf(C)`.
Then

    E[ U_i^fb(C) ]  <=  ( 1 + mu_i^sup(C) - nu_i(C) ) H_C  +  R^dbl_K(H_C)  +  (rho_n/3) H_C ,

and, for an honest `i`, also `E[U_i^fb(C)] <= H_C`.

*Proof.* Let `j` attain `nu_i(C)`. Under `S^*`, `j` delivers `M_j(x_{j,t}) >= M_j^inf(C) = nu_i(C)`
at every fallback pull, so Lemma 7 applies with `v = nu_i(C)`. Every other non-deviator `j'`
delivers `M_{j'}(x_{j'}) <= M_{j'}^sup(C) <= M_{j'}^inf(C) + rho_n/3 <= nu_i(C) + rho_n/3` by
Fact 0 and the definition of `nu_i(C)`. Splitting the total fallback reward into `i`'s share and
the others',

    nu_i(C) H_C - R^dbl_K(H_C)  <=  bar A_i + ( nu_i(C) + rho_n/3 )( H_C - bar Q_i ) ,

so `bar A_i >= nu_i(C) bar Q_i - R^dbl_K(H_C) - (rho_n/3) H_C`. Then
`E[U_i^fb(C)] = E[ sum (1 + mu_i(x_i) - m) ] <= (1 + mu_i^sup(C)) bar Q_i - bar A_i
<= (1 + mu_i^sup(C) - nu_i(C)) bar Q_i + R^dbl_K(H_C) + (rho_n/3) H_C`, and
`1 + mu_i^sup(C) - nu_i(C) >= 0` because `nu_i(C) <= 1`, so `bar Q_i` may be replaced by `H_C`. For
an honest `i`, each fallback pull contributes `1 + mu_i(x_i) - m <= 1` since `m >= mu_i(x_i)`. `QED`

Note that Lemma 7b never needs `i` to be top and never divides by a capacity gap. The scalar proof's
non-top fallback bound `2 R_K(H)/delta_i` (`sections/appendix_private.tex`, equation
`eq:private-fallback-low`) is not used anywhere in this report, which is why no `delta_i` appears
in the theorem.

## 6. Theorem 1 (CG-MESP on a continuum with private capacities)

Let `J'_n` be the number of cubes the realised arrival path visits at least once, so
`J'_n <= min{ J_n, n }` and `J_n <= 2^D n^{D/(D+3)}`. Define

```
e_bid    := min{ J'_n L_n , n }                                   (deviator's Stage-1 harvest)
e_stage1 := min{ K J'_n L_n , n }                                 (all Stage-1 rounds)
e_osc    := n rho_n                                               (within-cube oscillation)
e_mon    := J'_n + 2 sqrt( J'_n n ell_n / 2 )                     (monitoring slack)
e_fb     := 11 sqrt( 2 K J'_n n log K ) + 2 K log K J'_n log_2( 2(n+1) )
e_price  := n ( 4 s_n + (4/3) rho_n )
e_rob    := n ( 4 s_n + (5/3) rho_n )
```

**Theorem 1.** Assume (A1) to (A6) and run CG-MESP of Section 3. Then:

**(A) Additive behavioural equilibrium.** For every agent `i` and every `S'_{i,n} in B^ctx+_{i,n}`,

    u_i(n; S'_{i,n}, S^*_{-i,n})  -  u_i(n; S^*_n)
        <=  e_bid + e_osc + e_mon + e_fb + 6 n^{-3} .

**(B) Second-capacity revenue.**

    P(n; S^*_n)  >=  E[ sum_{t<=n} M_(2)(X_t) ]  -  ( e_stage1 + e_price + 3 n^{-3} ) .

**(C) Honest-benchmark robustness.** For every feasible behavioural profile `S` in which every
agent plays some strategy in `B^ctx+_{j,n}` and every honest agent respects pointwise honesty (the
deviating set may be all of `[K]`),

    P(n; S)  >=  E[ sum_{t<=n} b(X_t) ]  -  ( e_stage1 + e_rob + e_mon + e_fb + 3 n^{-3} ) .

**(D) Rates.** For fixed `K`, `D` and `L`, all three error terms are
`O( n^{(D+2)/(D+3)} log(e K n) )`; explicitly, `e_bid <= 2^{D+1} n^{(D+2)/(D+3)}`,
`e_stage1 <= K 2^{D+1} n^{(D+2)/(D+3)}`,
`e_osc <= sqrt(D) n^{(D+2)/(D+3)} log(en)`,
`e_price <= (4 sqrt(ell_n/2) + (4/3) sqrt D log(en)) n^{(D+2)/(D+3)}`, and both `e_mon` and `e_fb`
are `O( 2^{D/2} sqrt(K log(eKn)) n^{(2D+3)/(2D+6)} ) + O( 2^D K log K n^{D/(D+3)} log n )`, whose
exponents `(2D+3)/(2D+6)` and `D/(D+3)` are both strictly below `(D+2)/(D+3) = (2D+4)/(2D+6)`.
Consequently `S^*` is an additive behavioural asymptotic equilibrium in the sense of contract
Definition 1, `P(n;S^*) = E sum_t M_(2)(X_t) - o(n)`, and the honest benchmark holds at the same
order, uniformly over all deviations and all instances satisfying (A1) with the given `L`.

**Uniformity.** Unlike `thm:private-mesp` and unlike both C2 candidates, part (A) is uniform over
instances: the bound contains no instance constant, no capacity gap `delta_i` and no threshold of
the form `4 s_n <= delta_i`. The only instance-dependent hypothesis is `n >= exp(3L)` in (A2), and
`L` enters the *hypothesis* rather than the *bound*. The reason is Lemma 5 and consequence (C2);
Section 7.4 explains why the same removal applies to the scalar theorem.

## 7. Proof of Theorem 1

Throughout, condition on the arrival path `A` (Convention F-A); every bound below is uniform in `A`
and integrating at the end is immediate. Write `G` for the good bidding event of Lemma 3 and `H` for
the monitoring event of Lemma 6, in both coupled executions; `Pr( G^c ) <= n^{-4}` and
`Pr( H^c ) <= 2 n^{-4}` over the two executions, so `Pr( (G cap H)^c ) <= 3 n^{-4}`.

### 7.1 Part (A)

Couple the deviating and the baseline execution as in Lemma 4. By Lemma 2 the mechanism's state at
a cube is a function of that cube's own data, so utilities decompose additively over cubes,
`u_i = sum_C E[ U_{i,C} ]`, with no independence across cubes required; a deviator that correlates
its behaviour across cubes is handled by bounding each term uniformly over everything it may
condition on.

**Stage 1, pathwise, every cube.** At agent `i`'s Stage-1 pulls at `C` the two executions are pulled
at the same rounds (Lemma 4(a)). Their per-pull utilities differ by
`M_i(x_{i,t}) - m'_{i,t} in [0,1]`, so the Stage-1 difference at `C` is at most `l_i(C)`, the number
of Stage-1 pulls `i` receives at `C`, which is at most `L_n`. Since `sum_C l_i(C)` is also at most
the total number of rounds, `sum_C l_i(C) <= min{ J'_n L_n , n } = e_bid`. This bound is pathwise
and holds on every event.

**Cubes that never award.** If `V_C < K L_n` every visit is a Stage-1 pull, and the display above is
the whole contribution.

**Post-Stage-1, on `G cap H`, when `i` loses at `C` in the deviating execution.** The winner
`W != i` plays `S^*`, so by consequence (C1) of Lemma 5 its Stage-2 target is exactly `tau_C` if
strategic and at least `tau_C` if honest, at every context of `C`. By Lemma 6(d) no switch occurs
at `C`. Hence `C` has no fallback and `i` receives no post-Stage-1 pull there, so
`U'_{i,C}^{post} = 0 <= U_{i,C}^{post}` and the contribution to the gain is at most `0`.

**Post-Stage-1, on `G cap H`, when `i` wins at `C` in the deviating execution.** By Lemma 4(c) `i`
also wins at `C` in the baseline execution, and by Lemma 4(d) both face the same price `tau_C`.
Write `n_C = q + H_C` with `q` the Stage-2 tenure and `H_C` the fallback length, and put

    w_C  :=  1 + mu_i^inf(C) - tau_C     if i is strategic,
    w_C  :=  min{ 1 , 1 + mu_i^inf(C) - tau_C }   if i is honest,

which is nonnegative because `tau_C <= M_i(x_i) <= 1 <= 1 + mu_i^inf(C)` by Lemma 5.

*Upper bound on the deviation.* Lemma 6(c) gives
`U'^{pri} <= q ( 1 + mu_i^sup(C) - tau_C ) + 1 + 2 b_n(q)`, and for an honest `i` also
`U'^{pri} <= q` since every honest target is at least `mu_i(x_i)`. Taking the smaller of the two and
using `mu_i^sup(C) <= mu_i^inf(C) + rho_n/3` (Fact 0),

    U'^{pri}  <=  q w_C  +  q rho_n/3  +  1 + 2 b_n(q) .

Lemma 7b gives `E[U'^{fb}] <= ( 1 + mu_i^sup(C) - nu_i(C) ) H_C + R^dbl_K(H_C) + (rho_n/3) H_C`,
and for an honest `i` also `E[U'^{fb}] <= H_C`. By consequence (C3) of Lemma 5, `nu_i(C) >= tau_C`,
so `1 + mu_i^sup(C) - nu_i(C) <= w_C + rho_n/3` in the strategic case and, taking the smaller of the
two bounds, `E[U'^{fb}] <= H_C w_C + (2 rho_n/3) H_C + R^dbl_K(H_C)` in both cases. Adding,

    E[ U'^{post}_{i,C} ]  <=  n_C w_C  +  n_C rho_n  +  1 + 2 b_n(n_C) + R^dbl_K(n_C) .

*Lower bound on the baseline.* On `G`, `S^*_i` delivers exactly `tau_C` (strategic) or
`max{ mu_i(x_i), tau_C }` (honest) at every Stage-2 pull at `C`, both at least `tau_C`, so by
Lemma 6(d) the baseline never switches at `C` and receives all `n_C` post-Stage-1 pulls. Its
per-pull utility is `1 + mu_i(x_i) - tau_C >= w_C` in the strategic case and
`min{1, 1 + mu_i(x_i) - tau_C} >= w_C` in the honest case. Hence
`U^{post}_{i,C} >= n_C w_C`.

*Difference.* `E[ U'^{post}_{i,C} - U^{post}_{i,C} ] <= n_C rho_n + 1 + 2 b_n(n_C) + R^dbl_K(n_C)`.

**Where each event is used, because the two conditionings are not interchangeable.** `G` is
determined by the Stage-1 data at the cubes and is therefore measurable with respect to the
fallback-start field `F_fb` at every cube, so `E[ U'^{fb}_{i,C} 1_G ] = E[ 1_G E[U'^{fb}_{i,C} |
F_fb] ]` and Lemma 7b may be applied inside the indicator; consequence (C3), which is what turns
`nu_i(C)` into `tau_C`, also only needs `G`. `H` is **not** `F_fb`-measurable, so it is used only
where the monitor bound is invoked pathwise, namely Lemma 6(c) for the deviator's Stage-2 utility
and Lemma 6(d) for the baseline's survival, both of which are pathwise statements on `H`. The
complement is charged once, at `2 n Pr( (G cap H)^c ) <= 6 n^{-3}`.

**Summation.** Adding the Stage-1 term and the post-Stage-1 terms over cubes on `G cap H`, and
charging the complement at `2 n` because per-pull utilities lie in `[0,2]`,

    gain  <=  e_bid  +  n rho_n  +  sum_C [ 1 + 2 b_n(n_C) ]  +  sum_C R^dbl_K(n_C)  +  2 n . 3 n^{-4} .

By Cauchy and Schwarz, `sum_C b_n(n_C) = sum_C sqrt( n_C ell_n / 2 ) <= sqrt( J'_n n ell_n / 2 )`,
so `sum_C [1 + 2 b_n(n_C)] <= e_mon`. Also
`sum_C 11 sqrt( K (n_C + 1) log K ) <= 11 sqrt( K J'_n log K sum_C (n_C+1) ) <= 11 sqrt( 2 K J'_n n log K )`
using `J'_n <= n`, and the logarithmic part of `R^dbl_K` sums to at most
`2 K log K J'_n log_2(2(n+1))`, so `sum_C R^dbl_K(n_C) <= e_fb`. Finally `6 n . n^{-4} <= 6 n^{-3}`.
This is part (A). `QED`
### 7.2 Part (B)

All agents play `S^*`, so `beta_{j,C} = beta^cap_{j,C}` for every `j` and every `C`.

By the tower property and (A4), `P(n;S^*) = E[ sum_{t<=n} m_{I_t,t} ]`; no optional stopping and no
stopping-time argument is needed, which removes the gap the manuscript's revenue proof papers over
with "`q` is a bounded stopping time for the primary filtration" (a claim that is false at a cube
that simply stops being visited, as ADVERSARY Section 6.1 records).

Discard the Stage-1 rounds, at most `min{ K J'_n L_n, n } = e_stage1` of them, on which the target
is nonnegative. On `G cap H`: by consequence (C1) the Stage-2 target at an awarded cube is at least
`tau_C` at every context, so by Lemma 6(d) no cube ever switches, so every post-Stage-1 round is a
Stage-2 round and its target is at least `tau_C`. By Lemma 8, for every post-Stage-1 round `t`
with `X_t in C`,

    m_{I_t,t}  >=  tau_C  >=  M_(2)(X_t) - 4 s_n - (4/3) rho_n .

Hence on `G cap H`, `sum_{post-Stage-1 t} m_{I_t,t} >= sum_{post-Stage-1 t} M_(2)(X_t) - e_price`.
Off `G cap H` the targets are nonnegative and `M_(2) <= 1`, so the loss is at most
`n Pr((G cap H)^c) <= 3 n^{-3}`. Adding back the at most `e_stage1` Stage-1 rounds, each with
`M_(2)(X_t) <= 1`, gives part (B). `QED`

### 7.3 Part (C)

Now every agent may behave arbitrarily, subject only to feasibility and to honesty for
`h in K_H`, so `G` is unavailable. Replace it by the honest bid event

    G_H := { beta_{h_C,C} >= v_C - s_n  for every cube C that completes bidding } ,

with `h_C` and `v_C` as in Lemma 9. Agent `h_C`'s Stage-1 targets at `C` are predictable and at
least `mu_{h_C}(x_{h_C,t}) >= v_C` by honesty, so the one-sided conditional Hoeffding and Azuma
inequality gives `Pr( beta_{h_C,C} < v_C - s_n ) <= exp( -2 L_n s_n^2 ) = (2 K n^5)^{-1}` for each
cube, and a union bound over the at most `n` visited cubes gives `Pr(G_H^c) <= n^{-4}`.

Discard the at most `e_stage1` Stage-1 rounds. Fix a cube `C` that awards and work on `G_H cap H`.

*Case (i): `W_C = h_C`.* Every Stage-2 target at `C` is at least `mu_{h_C}(x_{h_C,t}) >= v_C`. By
Lemma 6(e), `E[ sum over Stage-2 pulls at C of Y_t ] = E[ sum of targets ] >= v_C E[q]`. If a switch
occurs, Lemma 7 with comparator `h_C` and `v = v_C` (legitimate by Lemma 9(ii), which is pathwise
and holds under arbitrary behaviour of the others) gives fallback reward at least
`v_C H_C - R^dbl_K(H_C)`. Adding, the post-Stage-1 reward at `C` is at least
`v_C n_C - R^dbl_K(n_C)`.

*Case (ii): `W_C != h_C`.* Then `beta_(2),C >= beta_{h_C,C} >= v_C - s_n`, so
`tau_C >= v_C - s_n - sigma_n = v_C - 4 s_n - rho_n`. On `H`, Lemma 6(b) gives
`A_q >= q tau_C - 1 - 2 b_n(q)` for the Stage-2 tenure `q`, and Lemma 6(e) turns the target sum into
expected reward. If a switch occurs, Lemma 7 again gives at least `v_C H_C - R^dbl_K(H_C)` on the
fallback. Adding, the post-Stage-1 reward at `C` is at least
`n_C ( v_C - 4 s_n - rho_n ) - 1 - 2 b_n(n_C) - R^dbl_K(n_C)`.

Case (ii) dominates case (i). By Lemma 9(i), `v_C >= b(X_t) - (2/3) rho_n` for every `X_t in C`, so
the post-Stage-1 reward at `C` is at least
`sum_{post-Stage-1 t in C} b(X_t) - n_C ( 4 s_n + (5/3) rho_n ) - 1 - 2 b_n(n_C) - R^dbl_K(n_C)`.
Summing over cubes, using the same two Cauchy and Schwarz steps as in Section 7.1 for
`sum_C [1 + 2 b_n(n_C)] <= e_mon` and `sum_C R^dbl_K(n_C) <= e_fb`, charging the at most `e_stage1`
Stage-1 rounds at `b <= 1` each, and charging `(G_H cap H)^c` at `n Pr((G_H cap H)^c) <= 3 n^{-3}`,
gives part (C). `QED`

### 7.4 By-product: the non-top branch and the instance gaps are removable in the scalar theorem

`thm:private-mesp` states its deviation bound only "for each fixed instance" and explicitly "not
over sequences whose positive capacity gaps vanish", and its proof has a separate non-top branch
controlled by `delta_i = V_i - M_i` with the threshold `2 s_n <= delta_i / 2`. The appendix's
bidding-coupling paragraph says deliberately "No concentration around the deviator's capacity is
invoked".

That choice is what forces the branch. The random variable `beta_i^max` defined there is an average
of `L_n` independent Bernoulli`(M_i)` variables whose seeds sit at the deterministic Stage-1 rounds
of agent `i`, so it is **independent of everything the deviator does**, and the event
`{ |beta_i^max - M_i| <= s_n }` is deviation independent exactly as `G_{-i}` is. Enlarging the good
event to `G_{-i} cap { |beta_i^max - M_i| <= s_n }`, whose probability is still at least
`1 - 2 n^{-4}`, gives on `{ i wins }` that `beta_(2) = max_{j != i} beta_j <= beta'_i <= beta_i^max
<= M_i + s_n`, hence `tau_i <= M_i`. So on the enlarged good event a winning deviator can always
meet the price, the non-top branch is vacuous, and the bound becomes
`L_n + 1 + 2 b_n(n) + R_K(n) + O(n^{-3})` with no `delta_i` anywhere and no threshold on `n`.

I checked this against the appendix's text and I believe it is right, but it is a claim about a
proof I did not write and it should be verified by a second reader before it is used. If it holds,
the manuscript can delete the sentence "The first bound is uniform over the declared deviations for
each fixed instance, but not over sequences whose positive capacity gaps vanish", which is one of
the weakest-looking qualifications in the paper, and can delete the non-top paragraph of
`appendix_private.tex`. The same deletion applies to PROVER1's `D_i(z)` and PROVER2's `e_low`.

### 7.5 What Theorem 1 does not give

1. **No monotonicity, no FATA, no sharp adaptivity.** CG-MESP is a private-information mechanism; it
   is not claimed to be contextual SAMF. The manuscript's `thm:grid-etc` gives those for the public
   Grid-ETC and nothing here replaces it.
2. **No claim that the rate is optimal.** `e_bid` is attained by the obvious analogue of
   Proposition `prop:tightness` (shade to the midpoint on every Stage-1 pull of every cube; the
   post-Stage-1 executions then coincide pathwise on the good event, giving a gain
   `c J'_n L_n - O(n^{-3})`), so the mechanism as specified cannot do better; whether some other
   mechanism can is open, and Proposition 4 addresses only the covering half of the question.
3. **No anytime guarantee.** `n` is used in `g_n`, `L_n`, `ell_n`, `s_n`, `rho_n` and `b_n`.
4. **Lipschitz capacities are needed**, which the manuscript assumes only in the weaker form
   "continuous" and only in `thm:contextual-public`. Without a modulus the price cannot be shaded
   safely, and `c4-safe-partitions/REPORT.md` Theorem 4 is the warning about what happens to a
   mechanism that tries to estimate the modulus from rewards.
5. **The threshold `n >= exp(3L)`** is an instance-dependent horizon requirement. It can be traded
   for a worse rate: taking `rho_n := sqrt(D) h_n log(en)^{1+a}` for `a > 0` weakens the threshold
   to `log(en)^{1+a} >= 3L` while inflating `e_osc` by `(log n)^a`. It cannot be removed, because
   `L` is unknown and the shading must dominate the oscillation.
6. **Arrivals that react to rewards are excluded** by (A3). ADVERSARY Section 7.1 exhibits an
   instance in the finite case where dropping this makes the theorem false, not merely unproved; the
   same construction applies here.

## 8. The per-agent architecture: what it buys, and the exact place it stops

The coordinator's target is `n^{(d+2)/(d+3)}`, justified by the adversary's F6 (capacities depend on
the agent's own coordinate). This section builds the mechanism, shows that the **pricing half really
is `d`-dimensional**, and then shows that the **deterrence half is `D`-dimensional for a reason that
is not an artefact of my construction**, with the consequence that the target exponent is reached
only when `K = 2` and `d = 1`. I do not prove a theorem for this mechanism; Section 8.7 says what is
missing.

### 8.1 PA-MESP

Grid on `[0,1)^d`: `g'_n := ceil(n^{1/(d+3)})`, `h'_n := 1/g'_n`, `J^1_n := (g'_n)^d` cells.
`L_n := ceil(n^{2/(d+3)})`, `rho'_n := sqrt(d) h'_n log(en)`, `sigma_n := 3 s_n + rho'_n`, and
`s_n`, `ell_n`, `b_n` as in Section 3 with `d` in place of `D`. State: one bid counter and reward
sum per pair `(j, c)` with `j in [K]` and `c` a cell of `[0,1)^d`.

At round `t` write `c_j(t)` for the cell of `x_{j,t}`. Call the round *unresolved* if some `j` has
fewer than `L_n` recorded pulls at `(j, c_j(t))`.

* **Elicitation.** If the round is unresolved, pull the smallest-indexed such `j` and record the
  reward at `(j, c_j(t))`. The rule reads only the arrival path and the counters, never a reward, so
  it is context only in the sense of `c4-safe-partitions/REPORT.md` requirement R1.
* **Pricing.** If the round is resolved, form `beta_{j,c_j(t)}` for each `j`, let `W_t` be a largest
  bidder (fixed priority permutation for ties, drawn once before play) and
  `tau_t := ( beta_(2),t - sigma_n )_+` with `beta_(2),t` the second order statistic with
  multiplicity of `( beta_{1,c_1(t)}, ..., beta_{K,c_K(t)} )`.
* **Monitoring.** One monitor per agent, global over contexts: for agent `j`, with `Z^j_r` the sum
  of its rewards on its first `r` priced pulls and `T^j_r` the sum of the prices charged at those
  pulls, switch `j` at the first `r` with `Z^j_r < T^j_r - b_n(r)`.
* **Fallback.** On the first switch of any agent, run Grid-EXP3 (separation Section 2.1) on a
  `D`-dimensional grid of side `h''_n` with doubling epochs, for the remaining rounds.
* **Proposed profile.** As in Section 3, with `tau_t` in place of `tau_C`.

Elicitation cost: every elicitation round advances one of the `K J^1_n` counters and each counter
stops at `L_n`, so at most `min{ K J^1_n L_n, n } = O( K 2^d n^{(d+2)/(d+3)} )` rounds are spent on
elicitation, whatever the arrival path and whatever the agents do.

### 8.2 What transfers verbatim (the pricing half)

Every lemma of Section 5 that concerns bids and prices holds for PA-MESP with the same proof, with
"cube" replaced by "the pair `(j, c_j(t))`" and `rho_n` by `rho'_n`:

* **Lemma 3** (good bidding event): the elicitation schedule is a deterministic function of the
  arrival path, so each `beta^cap_{j,c}` is an average of `L_n` independent Bernoulli variables with
  `F_0`-measurable means; `Pr(G) >= 1 - n^{-4}` unchanged.
* **Lemma 4** (bid domination, winner inclusion, price independence): unchanged. The two coupled
  executions pull the same agent at the same round throughout elicitation, because the schedule
  reads only counters and contexts.
* **Lemma 5** (`tau_t <= M_{W_t}(x_{W_t,t})` at every round on `G`): unchanged, and now pointwise in
  `t` rather than per cube. The proof only uses `beta_(2),t <= beta_{W_t, c_{W_t}(t)} <=
  beta^cap_{W_t, c_{W_t}(t)} <= bar m + s_n <= M_{W_t}(x_{W_t,t}) + L sqrt(d) h'_n + s_n`.
* **Lemma 8** (`tau_t >= M_(2)(X_t) - 4 s_n - (4/3) rho'_n` at `S^*`): unchanged.
* **Lemma 6** (monitor): holds with the per-agent monitor, because the prices `tau_t` are
  predictable and the indicator "round `t` is a priced pull of agent `j`" is `F_{t-1}`-measurable
  under Convention F-A. The monitoring slack improves from `sum_C b_n(n_C) <= sqrt(J'_n n ell_n/2)`
  to `sum_j b_n(r_j) <= sqrt(K n ell_n / 2)`, that is from `n^{(2D+3)/(2D+6)}` to `sqrt(K n log n)`.

So the elicitation cost, the price slack `n(4 s_n + (4/3) rho'_n)` and the monitoring slack are all
`O( K n^{(d+2)/(d+3)} log n )` or better. **The pricing half of the problem is `d`-dimensional and
the coordinator's exponent is correct for it.**

### 8.3 The deterrence half is `D`-dimensional, and the reason is not removable

The deviation accounting needs a fallback comparator value `nu_i` with `nu_i >= tau_t - epsilon`,
because the deviator's fallback utility is bounded by `(1 + mu_i - nu_i) H + R` while the baseline
earns `(1 + mu_i - tau_t)` per round; any shortfall `tau_t - nu_i` is a *per-round linear* gain to a
deviator that triggers the fallback deliberately. The comparator value that the fallback can deliver
on a region `R` is `nu_i(R) = max_{j != i} inf_{X in R} M_j(x_j)`, and `max_{j != i} M_j(x_j)` is
`V_i(X)`, a function of the whole profile. So the fallback must operate on regions on which `V_i` is
almost constant, which is a `D`-dimensional requirement.

Quantitatively: by Lemma 5 applied to the runner-up, `tau_t <= M_{j*}(x_{j*,t}) - 2 s_n -
(2/3) rho'_n` where `j*` attains the second bid, and `nu_i(R) >= M_{j*}(x_{j*,t}) - L sqrt(d) h''_n`
for a `D`-cube `R` of side `h''_n` containing `X_t`. Hence `nu_i(R) >= tau_t - epsilon` requires

    L sqrt(d) h''_n  <=  epsilon + 2 s_n + (2/3) rho'_n ,

and `epsilon` costs `n epsilon`, so it must be `O(n^{-1/(d+3)})`. Since `s_n` and `rho'_n` are both
`O( n^{-1/(d+3)} log n )`, the fallback grid must satisfy `h''_n = O( n^{-1/(d+3)} log n )`, which
is the **pricing** resolution, in the **profile** dimension. Grid-EXP3 on `(h''_n)^{-D}` cells then
costs `sqrt( K (h''_n)^{-D} n log K ) = Omega( n^{(D + d + 3)/(2(d+3))} )`.

**Consequence (the exponent table).** Write `alpha_CG := (D+2)/(D+3)` (Theorem 1),
`alpha_price := (d+2)/(d+3)` and `alpha_fb := (D+d+3)/(2(d+3))`. PA-MESP, with a fallback fine
enough to deter, has exponent `max{ alpha_price, alpha_fb }`, and

    alpha_fb <= alpha_price   <=>   D + d + 3 <= 2d + 4   <=>   D <= d + 1   <=>   K = 2 and d = 1 .

| `K` | `d` | `D` | `alpha_price` | `alpha_fb` | PA-MESP `max` | CG-MESP `alpha_CG` | better |
|:-|:-|:-|:-|:-|:-|:-|:-|
| 2 | 1 | 2 | 0.7500 | 0.7500 | 0.7500 | 0.8000 | PA |
| 3 | 1 | 3 | 0.7500 | 0.8750 | 0.8750 | 0.8333 | CG |
| 4 | 1 | 4 | 0.7500 | 1.0000 | 1.0000 | 0.8571 | CG (PA vacuous) |
| 2 | 2 | 4 | 0.8000 | 0.9000 | 0.9000 | 0.8571 | CG |
| 3 | 2 | 6 | 0.8000 | 1.1000 | 1.1000 | 0.8889 | CG (PA vacuous) |

So the per-agent architecture is a real improvement in exactly one case, `K = 2` and `d = 1`, where
it reaches `n^{3/4}` against CG-MESP's `n^{4/5}`, and it is worse or vacuous otherwise. **The
coordinator's fallback instruction, "fall back to `(D+2)/(D+3)` if the per-agent architecture cannot
be made safe", is the operative one for `K >= 3`.**

### 8.4 Correction to the sceptic's Section 2.2

The sceptic writes that the Grid-EXP3 fallback exponent `(D+1)/(D+2)` "is better than the
`(d+2)/(d+3)` pricing cost whenever `(D+1)/(D+2) < (d+2)/(d+3)`, which holds for `d = 1` and every
`D >= 3`". That inequality is

    (D+1)(d+3) < (d+2)(D+2)  <=>  3D + d + 3 < 2d + 2D + 4  <=>  D < d + 1 ,

so it holds only for `D <= d`, which is impossible in this model (`D = Kd`, `K >= 2`, `d >= 1`). For
`d = 1` and `D = 3` the two numbers are `0.8` and `0.75`, so the claimed inequality is false in the
very case named. Section 8.3 shows the situation is worse than that comparison suggests anyway,
because a fallback tuned to its own balance at `(D+1)/(D+2)` is too coarse to deter: the binding
requirement is `h''_n` at the pricing resolution, not at the Grid-EXP3 balance.

### 8.5 Why per-agent pooling cannot rescue the fallback

One might hope to run the fallback on the per-agent grid too, keying each round by the cells
`(c_1(t),...,c_K(t))` but maintaining `d`-dimensional per-agent statistics. This is exactly the
construction that `MATH_CANDIDATE_LEDGER.md` Section 6.1 refutes, and the refutation is the right
one for this purpose: under arbitrary behaviour an agent's *delivered* mean is not a function of its
own coordinate (the witness has a strategic agent with a constant own context delivering `1` when
the honest agent's context is in `A` and `0` when it is in `B`), so a per-agent statistic is not a
valid estimate of anything the fallback needs. The honest agents are the exception, since
`mu_h(x_h)` is own-coordinate measurable and honesty is a pointwise lower bound; but the fallback
must *select* among the agents, and the selection rule reads all `K` statistics, of which `K-1` may
be meaningless. That is a `D`-dimensional decision made from `d`-dimensional summaries, and the
counterexample says it is wrong by a linear margin.

This is the precise content of the brief's safety caveat. Pooling on the per-agent grid is safe for
a quantity that has to be correct **only at `S^*`**, where every agent delivers `M_j(x_j)`; that is
the price, and Section 8.2 proves it. It is unsafe for a quantity that has to be correct **under
arbitrary behaviour**; that is the fallback, and Section 8.5 is the reason. The two halves of the
mechanism therefore live in different dimensions, and the worse one governs.

### 8.5b Imported techniques, what the agent controls, and why each survives

The brief requires this check before any proof is invested in. Every technique used in Sections 3 to
7 is either elementary or internal to this project, and **no external paper is relied on anywhere in
this report**, so there is no primary source to record. Specifically:

| Technique | What the agent controls | Why it survives |
|:-|:-|:-|
| Hoeffding on the bids (Lemma 3) | the targets, hence the means | the bound is applied to `beta^cap`, whose means are `M_j(x_{j,t})`, fixed by the instance and the arrival path, not by the agent; the agent's own bid is then dominated pathwise (Lemma 4b) rather than concentrated |
| Azuma with predictable targets (Lemma 6) | the target at each pull, adaptively, from the whole cross-cube history | the increment `Y - m` is centred *given* the target, by (A4); the agent chooses `m`, not the seed, which is the forced-noise point the separation report makes |
| Cauchy and Schwarz over cubes | nothing; `n_C` is arrival determined by (A3) | a reward-dependent partition would make `n_C` agent controlled, which is exactly the C4 converse |
| EXP3 potential argument, prefix and doubling (Lemma 7) | the delivered mean when selected, reactively | the manuscript's own `lem:selected-reactive-exp3` is proved for exactly this, and the prefix and doubling extensions are `separation/REPORT.md` Lemma A and Lemma B, both internal |
| Covering argument (Proposition 4) | the revealed values, but the proposition grants full noiseless revelation | granting the agent's best case only strengthens the conclusion |

Section 8.6 below names a technique from outside (an experts-over-a-net bandit algorithm) and gives
a rate for it. **That rate is my own arithmetic from a covering count, it is not taken from any
paper, I verified no source for it, and nothing in this report depends on it.** It is recorded as a
direction, not as a fact.

### 8.6 The one route that would reach `n^{(d+2)/(d+3)}` for all `K`, not taken

The fallback's job is to attain `sum_t b(X_t) - o(n)` under arbitrary behaviour and to give the
deviator no more than `V_i(X_t)` per round. Both are comparisons against a *policy* of the form
`X -> argmax_j f_j(x_j)` with `f_j` `L`-Lipschitz on `[0,1]^d`. That policy class is parameterised
by `K` functions of `d` variables, so an `eps`-net of it has `log N(eps) = O( K (L/eps)^d )`. An
experts-over-a-net bandit algorithm with regret `sqrt( K n log N(eps) )` against the net, plus the
approximation error `eps n`, would give `sqrt( K^2 n (L/eps)^d ) + eps n`, minimised at
`eps = Theta( (K^2 L^d)^{1/(d+2)} n^{-1/(d+2)} )` and worth `Theta( n^{(d+1)/(d+2)} )` up to
`K`-factors; and `(d+1)/(d+2) < (d+2)/(d+3)` for every `d >= 0`, so the whole mechanism would land
at `n^{(d+2)/(d+3)}`. **I did not do this and I am not claiming it.** Three things would have to be
supplied: a selected-reactive version of EXP4 (the manuscript's `lem:selected-reactive-exp3` is for
`K` arms and the comparator argument does not obviously survive an expert set whose members are
policies over the arms); an argument that the expert net can be built without knowing `L` or `nu`;
and an acknowledgement that the per-round cost is exponential in `(L/eps)^d`, which makes it a
theoretical object rather than an algorithm. This is the only route I found that would make the
per-agent architecture reach the coordinator's exponent for `K >= 3`, and it is where I would look
next.

### 8.7 What is missing from PA-MESP, precisely

Even granting a fallback, I have not written the deviation accounting for PA-MESP, and three steps
are genuinely different from Section 7.1 rather than notational:

1. **The winner changes from round to round**, so the per-cube decomposition of Section 7.1 does not
   apply and the accounting must be per agent and per round. The Stage-1 harvest is still
   `min{ J^1_n L_n, n }`, but the comparison of the deviating and baseline continuations after a
   round at which the two executions award differently is no longer a comparison of two cube-local
   phases. Lemma 4(c) gives winner inclusion at each round separately, which is what one wants, but
   the baseline and the deviation can then have different *global* monitor states.
2. **The per-agent monitor couples the rounds.** A deviator that underdelivers at one profile moves
   its own global monitor, which then binds at other profiles. Theorem S1 of `SCEPTIC.md` applies to
   the global monitor and gives a floor of `Omega(sqrt(n log n))` on what it concedes, which is
   within budget, but a *deterrence* statement (that a localised shortfall of size `o(sqrt n)` is
   still punished) is not available and the sceptic flags the same point in its route table for
   route 2.
3. **The interleaving condition the adversary flags in F6** is resolved by the schedule of
   Section 8.1 (a round is priced only when all `K` pairs at that round are complete) but the
   *revenue* statement then has to charge the unresolved rounds, and an adversarial arrival path can
   interleave resolved and unresolved rounds so that the mechanism is in elicitation on exactly the
   rounds where `M_(2)` is large. The bound `min{K J^1_n L_n, n}` on the number of such rounds is
   pathwise, so the charge is correct, but it is charged at `M_(2) <= 1` per round and there is no
   better bound.

## 9. Route map, updated, and messages for the sceptic

The sceptic's Section 7 table is updated as follows. Items marked **new** are settled or moved here.

| Route | Status after this report | Where |
|:-|:-|:-|
| 1. Cell based, retuned per-region bidding length | **Closed positively for `m = D`.** Theorem 1 is a complete mechanism and proof at `n^{(D+2)/(D+3)}`, under weaker hypotheses than the manuscript's public contextual theorem: no i.i.d. arrivals, no top-set condition, no null boundary. The three obstacles PROVER2 named are removed by the shading `3 s_n + rho_n` (Lemma 5). **new** | Sections 3 to 7 |
| 2. One global monitor | **Alive, and it is what PA-MESP uses.** The per-agent global monitor lowers the monitoring slack from `sqrt(J n log n)` to `sqrt(K n log n)`; Theorem S1 floors it at `sqrt(n log n)`, which is within budget either way. The monitoring term was never the binding one. **new: it is not binding at the balanced grid in either architecture.** | Section 8.2 |
| 3. Estimate the capacity function | **Reframed, and the reframing is negative for the estimation reading.** Section 2 shows the platform can never hold an upper bound on a capacity, so there is no estimator in the usual sense; what exists is a revealed lower envelope that the agent chooses (Proposition 3). The mechanism should therefore not estimate at all: it should price off an envelope and shade. Proposition 4 replaces the sceptic's belief about metric entropy with a proved covering statement that does not depend on a regression model. **new** | Section 2 |
| 4. Remove the bidding phase | **Closed negatively, with a reason.** Section 2.6 item 3: a dedicated elicitation block is not an estimator that a better estimator could replace, it is the only place where an agent has a reason to reveal. Removing it keeps the price envelope safe but forfeits the revenue statement (B). Corollary S1.3 already closed the monitoring half. **new** | Section 2.6 |
| F-S3 (asymmetric elicitation: race then price) | **In tension with the C4 converse.** A race stops pulling an agent on a reward event, so the bid-domination coupling has different schedules in its two executions. This is the same failure mode as reward-dependent partitions. An accelerate-only sandwich might escape it. **new** | Section 2.6 item 4 |
| F-S2 (`d` in place of `D`) | **Correct for pricing, false for the mechanism.** The pricing half is `d`-dimensional (Section 8.2, proved). The deterrence half is `D`-dimensional at the pricing resolution (Section 8.3), so the overall exponent is `max{(d+2)/(d+3), (D+d+3)/(2(d+3))}`, which equals `(d+2)/(d+3)` only when `K = 2, d = 1`. The sceptic's comparison inequality in Section 2.2 is never satisfiable (Section 8.4). **new** | Sections 8.3, 8.4 |

**Three things the sceptic should attack first.**

1. **Lemma 5**, which is the load-bearing step of Theorem 1. It says the realised winner, whoever it
   is and however it bid, can meet the announced price at every context of its cube. If it is wrong,
   Theorem 1 fails completely, because everything downstream (the constant Stage-2 target, the
   absent non-top branch, the uniformity over instances) rests on it.
2. **Section 7.4**, the claim that the scalar theorem's non-top branch and its `delta_i` constants
   are removable. That is a claim about the manuscript's own proof and it is easy to check.
3. **Section 8.3**, the claim that the fallback must operate at the pricing resolution in the
   profile dimension. If that requirement can be weakened, for example by a fallback that suspends a
   failing agent for a finite, growing number of rounds instead of restarting EXP3, the per-agent
   architecture reaches `n^{(d+2)/(d+3)}` for all `K`. Section 8.6 and the note below record why I
   did not take that route: a suspension rule can be made to exclude *every honest agent* under part
   (C), where honest agents may play anything above `mu_h` and may therefore fail the monitor
   legitimately after bidding high; that is the reason `thm:private-mesp` restarts EXP3 instead of
   removing a suspect, and it is not a matter of constants.

## 10. Numerical falsification attempt against my own claims

Fully synthetic simulation of CG-MESP exactly as specified in Section 3, run to look for a violated
inequality. It is not evidence that Theorem 1 is true. Code, seeds and raw outputs:
`<scratchpad>/round2/explorer-f1/` (`cgmesp.py`, `lemma_test.py`, `tight.py`, `lemma_test.log`,
`f1tight-*.out`). Compute: three login-node runs of a few minutes each and one Slurm job,
`sbatch job_tight.sh`, partition `cpu`, account `<slurm-account>`, job id **64573336**,
2 cores, 4 GB, wall time under 20 minutes, 18 September 2026.

### 10.1 The honest parameters are numerically vacuous, and this must be said first

At the parameters of Section 3 the shading is
`sigma_n = 3 s_n + rho_n`. With `K = 2`, `D = 2`, `n = 20000` one gets `g_n = 8`, `L_n = 53`,
`s_n = 0.693`, `rho_n = 1.927` and `sigma_n = 4.006`, so `tau_C = 0` at every cube and the mechanism
prices at zero. At `n = 80000`, `sigma_n` is still `3.4`. Getting `sigma_n` below `0.1` needs
`L_n > 5 . 10^3` and hence, through `L_n = ceil(n^{2/(D+3)})` and `K J_n L_n <= n`, a horizon around
`10^9`. This is the same wall that `PRIVATE_BOUND_NOTES.md` Note 3 records for the scalar theorem
and that PROVER1 Section 11 and PROVER2 Section 10 record for the finite contextual one, and it is
worse here because `J'_n K L_n` is a larger fraction of `n`. **Any simulation of this mechanism at
simulable horizons is therefore a test of the lemmas and the inequalities, not of the rates or the
constants.**

### 10.2 What was tested instead

Every lemma of Section 5 holds for **any** grid side `h` and bidding length `L` with
`rho_n >= 3 L_lip sqrt(D) h`; only the *rates* of Theorem 1(D) need the balanced choice. So the
simulation sets `g` and `L` by hand at values where `tau_C` is non-degenerate, keeps
`rho_n := 3 L_lip sqrt(D) h_n` at its minimal admissible value and `ell_n = log(2 K n^5)` at its
honest value, and checks the lemmas and the three inequalities. Instances (all `d = 1`, so `D = K`):

* **A**: `K=2`, `M = (0.90+0.02x, 0.95-0.03x)`, `mu = (0.10, 0.40-0.02x)`, agent 1 honest, `L_lip=0.03`.
* **B**: `K=3`, `M = (0.86+0.04x, 0.93-0.05x, 0.89+0.01x)`, `mu = (0.05, 0.30+0.02x, 0.12)`,
  agent 1 honest, `L_lip = 0.05`.
* **C**: `K=2`, `M = (0.94+0.01x, 0.80-0.02x)`, `mu = (0.10, 0.30)`, agent 1 honest, `L_lip = 0.02`;
  agent 0 is the **unique top at every context**, which is the configuration in which the `e_bid`
  term is attainable.
* **D**: `K=3` version of C.

Arrival processes: i.i.d. uniform, and a deterministic golden-ratio sweep
`x_{j,t} = frac( t . 0.618... (j+1) )`, which is **not i.i.d.** and tests (A3) against the
manuscript's stronger requirement. Deviations for agent 0, all in `B^ctx+_{0,n}`: Stage-1
underbidding to the midpoint at every cube; the Theorem S1 boundary-tracking rider
`m_r = ( tau_C - alpha ( b_n(r) - b_n(r-1) ) )_+` for `alpha in {0.25, 0.5, 1}`; a greedy rider that
delivers the smallest amount surviving the next test; immediate crash; and the combination of
underbidding with the `alpha = 0.5` rider. Four to six seeds per cell, common random numbers across
deviations.

### 10.3 Findings

1. **No violation of Lemma 5 in any awarded cube, in any configuration.** Over the eight
   configurations of `lemma_test.log` and the three of `f1tight-*.out`, the count `l5` of cubes with
   `tau_C > min_{x in C} M_{W_C}(x)` was `0` out of every awarded cube (9, 6, 16, 8, 27, ... awarded
   cubes per run). The good event `G` held at every cube in every run, so the test confirms the
   *conclusion* of Lemma 5 but **does not exercise the case `G` fails**, which is the case the lemma
   is silent about and where a violation would be permitted. That is a real weakness of this check.
2. **No violation of Lemma 8** (`tau_C >= M_(2)(X) - 4 s_n - (4/3) rho_n` at `S^*`) and **no
   violation of the monitor envelope** `|Z_r - A_r| <= b_n(r)`, in any run.
3. **No switch ever occurred under `S^*`**, consistent with Lemma 6(d) and with the fact that the
   proposed profile delivers exactly `tau_C`.
4. **The `e_bid` term is attained, to the digit.** On instance C with `n = 200000`, `g = 3`,
   `L = 4000` (`J = 9`, `J L = 36000`), pure Stage-1 underbidding gained `2789.79`, against the
   prediction `J L ( M_0 - m' ) = 36000 . 0.0775 = 2790`. The gain had zero variance across seeds,
   which is the signature of the coupled argument (post-Stage-1 the two executions coincide
   pathwise), so the simulation is testing the argument and not only the number. This is the
   contextual analogue of `prop:tightness` and of PROVER1's Proposition 2. Doubling the horizon to
   `n = 400000` with `L = 8000` doubles `J L` to `72000` and the measured gain to `5579.68`, exactly
   twice `2789.79`, which is the scaling `e_bid` predicts and no other term predicts.
5. **The Theorem S1 rider is attained too, and the two channels are exactly additive.** On the same
   configuration, `alpha = 0.5` riding gained `2962.51`, against Theorem S1(b) summed over cubes,
   `0.5 . sum_C b_n(n_C) = 0.5 . 9 . sqrt(14222 . 61.5 / 2) = 2975`. Underbidding plus riding gained
   `5752.29`, against `2789.79 + 2962.51 = 5752.30`. At `n = 400000` the rider gained `4323.41`, a
   ratio of `1.459` over the horizon doubling against the `sqrt 2 = 1.414` that `sum_C b_n(n_C)`
   predicts (the excess is the growth of `ell_n`), and the combination gained `9903.10` against
   `5579.68 + 4323.41 = 9903.09`. The `e_bid` and `e_mon` channels are therefore separate, additive
   and scaling as predicted, exactly as PROVER2 Section 10 finding 3 reports for the finite case.
6. **Aggressive riding backfires on instance C, but this is instance dependent and I record the
   exception.** On C, `alpha = 1`, which sits on the boundary, lost `41473` at `n = 200000` and
   `65213` at `n = 400000`: it triggers switches and the fallback restores the other agents. On
   instance D (`K = 3`, agent 0 uniquely top, `J = 27`, `L = 2500`, mean `tau = 0.422`) the same
   rider *gained* `76.67`, because the lower price leaves the rider far from the boundary; there the
   riders contributed almost nothing (`30` to `77`) and the whole gain was the Stage-1 term, which
   again matched its prediction: `5134.31` measured against `J L . (M_0 - m') = 67500 . 0.077 =
   5197` (the small shortfall is the context dependence of the runner-up inside a cube). Bound (A)
   was `169443` against a largest measured gain of `5187`. Every crash deviation lost as well
   (`-874` to `-3147` across instances), and, as the accounting predicts, *raised* platform revenue.
7. **Theorem 1(A) held in every configuration with a wide margin.** On instance C the bound is
   `81694` (`e_bid = 36000`, `e_mon = 14999`, `e_fb = 25038`, `e_osc = 5657`) and the largest gain
   found was `5752`, a factor of `14`; at `n = 400000` the bound is `140344` and the largest gain
   found was `9903`, a factor of `14` again. On instance B with `K = 3` the bound is `166335` and every
   deviation tested *lost*.
8. **Theorem 1(B) and (C) held, and are not vacuous in this recalibrated regime.** Instance A,
   `n = 200000`, `g = 3`: revenue `143255` against `E sum_t M_(2)(X_t) = 182000`, a deficit of
   `38745` against the bound `153977`; the honest benchmark was `78001` and revenue exceeded it by a
   factor of `1.8`. The deficit is accounted for almost exactly by the shading: `72000` Stage-1
   rounds plus `128000` rounds priced at `tau ~ 0.603` against `M_(2) ~ 0.91`.
9. **The non-i.i.d. arrival process changes nothing measurable.** The golden-ratio sweep reproduces
   every qualitative finding, with `l5 = l8 = monv = 0` and revenue within `5%` of the i.i.d. runs
   at the same parameters. This is what (A3) predicts and it is the one thing this mechanism can
   claim that `thm:grid-etc` and `thm:contextual-public` cannot.

### 10.4 What this does not test

The rates, the constants, the regime `J'_n K L_n / n -> 0`, the case where `G` fails, the case where
a deviator wins a cube at which it is not top (which on the good event cannot happen, by consequence
(C2), and which is therefore untestable by construction), the per-agent mechanism of Section 8, and
anything about Section 2, which contains no probabilistic claim to simulate.

## 11. What I did not do, and the step I consider least secure

**Not done.**

1. **No lower bound.** Nothing here shows the exponent `(D+2)/(D+3)` is necessary. Proposition 4
   proves only the covering half of the heuristic that produces it, and it is a statement about
   designs, not about mechanisms. The sceptic's four failed attempts (its Section 5) remain the
   state of that question.
2. **No theorem for PA-MESP.** Section 8 proves its pricing lemmas and locates the obstruction
   quantitatively, and Section 8.7 lists the three steps I did not write. The `K = 2`, `d = 1` case,
   where the exponent would be `3/4`, is the one worth completing and I did not complete it.
3. **No monotonicity, FATA or sharp adaptivity for CG-MESP.** Only the three private-information
   properties are claimed.
4. **No treatment of arrivals that react to rewards** (excluded by (A3)), of non-Lipschitz
   capacities, or of an unknown horizon.
5. **No proof that the elicitation block can be shortened** in the way the sceptic's F-S3 proposes.
   Section 2.6 item 4 argues it conflicts with the C4 converse but does not exhibit a counterexample,
   so F-S3 is *unresolved*, not refuted.
6. **The route of Section 8.6** (an EXP4-style `d`-dimensional fallback over a net of `K`-tuples of
   Lipschitz functions) is a sketch with a rate computation and nothing else. The selected-reactive
   version of EXP4, which is the load-bearing step, is not written.
7. **No verification at asymptotic horizons.** Section 10 records that at every simulable horizon the
   shading `sigma_n = 3 s_n + rho_n` exceeds `1`, so the honestly parameterised mechanism prices at
   zero and the simulation tests the lemmas only in a deliberately recalibrated regime. This is the
   same limitation `PRIVATE_BOUND_NOTES.md` Note 3, PROVER1 Section 11 and PROVER2 Section 10 all
   record for the finite case, and it is worse here because `J'_n K L_n` is a larger fraction of `n`.

**Least secure step, in decreasing order of my own doubt.**

1. **Lemma 5, and specifically the inclusion of the deviator's counterfactual bid
   `beta^cap_{i,C}` in the good event `G`.** Everything distinctive about Theorem 1 follows from
   Lemma 5: the constant Stage-2 target, the absence of a non-top branch, the uniformity over
   instances, and the removal of the `delta_i` constants. The lemma's proof is three inequalities
   and I believe each of them, but the *definition* of `G` is the delicate object, because `G` must
   be simultaneously (i) behaviour independent, so that conditioning on it does not distort the
   deviator's law, and (ii) informative about a random variable, `beta^cap_{i,C}`, that does not
   exist in the deviating execution except through the coupling. I argue in Section 5.2 that
   `beta^cap_{i,C}` is a function of the arrival path and the seed array alone, which makes both
   points work, and this is exactly the reason the manuscript's own coupling paragraph is entitled
   to compare `beta'_i` with `beta_i^max`. But the manuscript deliberately declines to put
   `beta_i^max` in its good event ("No concentration around the deviator's capacity is invoked"),
   and I do not know whether that was caution or a reason I have not seen. **This is the first thing
   an adversary should attack, and if it falls, the non-top branch returns and Theorem 1 keeps its
   rate but loses its uniformity over instances.**
2. **Lemma 6's `F_{s-1}`-measurability of the Stage-2 indicator**, which holds only under Convention
   F-A. PROVER2 names the same step as its least secure one and the objection transfers verbatim.
   (A3) is what licenses it and (A3) is a real restriction: ADVERSARY Section 7.1 shows the finite
   theorem is false without it.
3. **The composition of Lemma 7b with the per-cube accounting in Section 7.1**, specifically the
   step that replaces `bar Q_i` by `H_C` using `1 + mu_i^sup(C) - nu_i(C) >= 0`. That is the place
   where the two coupled executions and the fallback expectation interact, and it is the analogue of
   PROVER2's secondary worry about its joint conditioning field `D_z`. I believe it but it deserves
   a second reader.
4. **Section 8.3's claim that the deterrence requirement forces the fallback grid to the pricing
   resolution.** The derivation is four lines and I believe it, but it assumes the fallback's only
   instrument is a comparator value on a region. A fallback that punishes by suspension rather than
   by competition would not be covered, and I give the reason I did not pursue suspension
   (Section 9) rather than a proof that it cannot work.

**One sentence of self-assessment.** I believe Theorem 1 is right and I am not confident of it; the
single place I would look first is the definition of the good event in Lemma 3 and its use in
Lemma 5, and the single claim in this report that would most change the paper if it survives review
is Section 7.4, which is about the manuscript's existing scalar theorem rather than about anything
new.
