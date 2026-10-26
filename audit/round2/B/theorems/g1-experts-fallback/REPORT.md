# G1: an experts-over-policies fallback, and whether it removes the profile-dimension exponent

Worker report, 18 September 2026. Output directory
`audit/round2/B/theorems/g1-experts-fallback/`. No canonical file was modified. No Unicode em dash
and no LaTeX triple hyphen appears in this file. Code, seeds and raw output:
`<scratchpad>/round2/g1-experts-fallback/` (`exponents.py`, `exp4check.py`, `exp4check2.py`,
`scaling.py`). Compute log: `COMPUTE_LOG.md` in this directory.

Read in full before starting: `audit/round2/prompts/COMMON.md`;
`audit/round2/B/theorems/f1-continuous-private/EXPLORER.md` (Sections 0 to 11, with Sections 8.3,
8.5, 8.6, 9 and 11 read twice); `audit/round2/B/theorems/f1-continuous-private/PROVER2.md`
(Sections 5, 9, 12, 13); `audit/round2/B/theorems/separation/REPORT.md` Part 2 (Sections 2.1 to
2.8); `audit/round2/B/theorems/c4-safe-partitions/REPORT.md` Section 0;
`sections/appendix_private.tex`; `sections/contextual_samf_algorithm.tex`.

I do not claim any result below is correct. Section 10 names the step I consider least secure and
lists what I did not do.

## 0. Answer in one page

The route named and dropped in `EXPLORER.md` Section 8.6 is **information-theoretically sound and
computationally infeasible**, and I can now say exactly why in both directions.

**0.1 The obstruction in `EXPLORER.md` Section 8.3 is real but not intrinsic, and the reason is a
single structural point.** Section 8.3 argues that the fallback must supply a comparator *value*
that is within `O(n^{-1/(d+3)})` of the announced price, that this value is
`V_i(X) = max_{j != i} M_j(x_j)`, a function of the whole profile, and therefore that a fallback
built from regions must use `D`-dimensional regions at the pricing resolution. Every step of that
argument is correct **for a fallback whose comparator is constant on a region**. It is not correct
for a fallback whose comparator is a *policy*, because a policy comparator supplies a value that
varies with the profile in exactly the way `V_i` does, and pays for that variation in `log N`, not
in `N`. Section 3.2 makes the point precise: with a policy comparator the requirement
"`nu_i >= tau_t - epsilon`" is satisfied **pointwise with `epsilon = 0`** up to the net resolution,
because `tau_t <= M_{j*}(x_{j*,t}) <= V_i(X_t)` at every round at which the deviator wins, and the
policy `argmax_{j != i} M_j(x_j)` attains `V_i(X_t)` at every round. There is no region and no
discretisation of the profile anywhere.

**0.2 The guarantee is the right one, after one correction the sketch does not make.** The class
must be a net over **guaranteed floors**, not over delivered maps. A comparator in this mechanism is
never "the function an agent delivers"; it is a function `g_j` with the property that agent `j`
delivers at least `g_j(x_j)` whenever it is selected. For deterrence, `g_j = M_j` for `j != i`
(non-deviators play `S^*` and deliver exactly `M_j`). For the honest benchmark, `g_h = mu_h` for
`h in K_H` and `g_j = 0` for the rest. Both vectors are `K`-tuples of `L`-Lipschitz functions of a
single agent's own `d`-dimensional coordinate, so both lie in the class, and **the question of
whether an honest agent's delivered map is smooth never arises**: only a smooth *lower envelope* is
needed, and the benchmark `b(X) = max_{h in K_H} mu_h(x_h)` is defined from that envelope. This is
the same device as `separation/REPORT.md` Lemma C, lifted from a cell to a policy. Section 3.

**0.3 The counting and the balance check out, and the exponent is better than the sketch says for
the fallback and equal to it for the mechanism.** An elementary net (Lemma N1, proved here, no
citation load bearing) gives `log N <= K (sqrt d / delta)^d log(1 + 1/eps)` with
`delta = eps / (sqrt d log(en))`, a construction that needs **no knowledge of `L`**, using only the
standing hypothesis `log(en) >= 3L` that `EXPLORER.md` (A2) already assumes. An EXP4 regret
`O(sqrt(K H log N))` then balances against the approximation cost `2 eps n` at
`eps = Theta((K^2 (sqrt d log(en))^d log n / n)^{1/(d+2)})`, worth
`Theta(n^{(d+1)/(d+2)})` up to logarithms. Since `(d+1)/(d+2) < (d+2)/(d+3)` strictly for every
`d >= 0`, with gap `1/((d+2)(d+3))` in the exponent, **the fallback is not the binding term**, and
the mechanism's exponent is the pricing exponent `(d+2)/(d+3)` for every `K`. I re-solved every
parameter from scratch rather than importing the sketch's numbers; the three way pricing balance
(`elicitation = price slack = oscillation`) is unchanged and forces
`h'_n = n^{-1/(d+3)}`, `L_n = n^{2/(d+3)}` independently of the fallback. Section 4 and the table in
Section 4.4.

**0.4 A second defect in the sketch, which I had to repair before anything closed.** The fallback of
`EXPLORER.md` Section 8.1 is **global**: on the first switch of any agent it takes over all remaining
rounds. With a global fallback the deterrence accounting fails by a linear margin whatever the
comparator class is, because the deviator collects fallback pulls at rounds at which it would not
have won in the baseline, and at such a round the baseline pays it `0` while the fallback pays it
`1 + mu_i - V_i(X_t) >= 0`. The repair is to **localise the fallback to the rounds the switched agent
would have won**: `W_t` is computable from the elicited bids at every resolved round, so the
mechanism can run a separate fallback instance on the round subsequence `{t : W_t = j}` for each
switched `j`, and leave every other round with its unswitched winner. Section 2.3 and Section 5.1.
This is a change to the mechanism, not to the analysis, and without it the route does not close.

**0.5 What does not work: implementability.** `log N` is small, `N` is `exp(Theta(n^{d/(d+2)}))`.
Running EXP4 explicitly is infeasible at every horizon at which the mechanism is otherwise
meaningful. I did not find an efficient implementation and I do not claim the mechanism has one.
Section 6 does three things instead. (i) It states plainly what the mechanism is: an
information-theoretic object, not an algorithm, and it says exactly what that costs the paper.
(ii) It identifies the computational problem the fallback poses as the **best-ordering benchmark for
sleeping experts with adversarial availability**, by an explicit reduction (Proposition E1): the
comparator class `{argmax_j f_j(x_j)}` on a per-agent grid of `J` cells is exactly the class of
rankings of the `K J` pairs `(agent, cell)`, with exactly one action per agent awake at each round.
(iii) It reports what is known about that problem, from primary sources: with adversarial payoffs
and adversarial availability an efficient no-regret algorithm would imply an algorithm for PAC
learning DNF (Kanade and Steinke, ITCS 2012), and Proposition E1 transfers this to the fallback
**when `K` is allowed to grow**. For **fixed `K`**, which is the regime of this paper, the transfer
gives only agnostic learning of monotone disjunctions over bounded-Hamming-weight examples, and I
could not settle whether that is hard. Section 6.4 states the resulting open problem precisely and
notes an asymmetry that makes me suspect the fallback problem is *easier* than the fully adversarial
one: the benchmark here is the best ordering of the *floors*, which are constant in time, so the
offline optimisation is a sort and not a linear ordering problem. That is the most promising place
to look next and I did not look there.

**0.6 The strategic hazard is real but lands elsewhere than the brief expects.** The `c4` witnesses
break rules that make an *irreversible decision* on rewards (freeze, eliminate, inherit a verdict,
split), and they break them because the *analysis* of those rules needs the cell epochs to be
fixed-mean instances. An experts algorithm updates on rewards but its guarantee is adversarial and
its proof never needs exogeneity of the rewards, so the hazard does not reach it: this is already
true of the manuscript's own EXP3 fallback and nothing changes when EXP3 becomes EXP4. What the
hazard does kill is the cheap alternative I found and rejected in Section 7.2: "on a switch, promote
the best remaining bidder" is efficient, `d`-dimensional, and sufficient for deterrence, and it
destroys part (C), because under arbitrary joint behaviour the bids carry no information and an
honest agent can be switched legitimately. Section 7.

**0.7 Bottom line for the paper.** The route removes the exponential dependence on `K` from the
*statement*. Theorem G1 (Section 5) is a mechanism with an additive behavioural equilibrium,
second-capacity revenue and the honest benchmark under arbitrary joint behaviour, on a continuum of
contexts with private capacities, at rate `O(n^{(d+2)/(d+3)} log(eKn))` with `d` the per-agent
dimension, for every `K`, against the `O(n^{(D+2)/(D+3)})` of CG-MESP with `D = Kd`. It is not
efficiently implementable and the paper must say so in the theorem's own neighbourhood, not in a
footnote. My recommendation in Section 8 is that this is worth one paragraph and a remark in the
appendix, not a headline, unless Section 6.4's open problem is settled.

## 1. Setting, notation and standing hypotheses

I use `CONTEXT_PROOF_CONTRACT.md` and `EXPLORER.md` Section 1 verbatim, so only the differences are
recorded. Agents `i in [K]`, `K >= 2`; per-agent context space `[0,1)^d`; profile space
`X = [0,1)^D` with `D = Kd`; `X_t = (x_{1,t},...,x_{K,t})`. Primitives `mu_i, M_i : [0,1)^d -> [0,1]`
with `mu_i <= M_i`, functions of agent `i`'s own coordinate only. At a round the platform selects
`I_t`, the selected agent chooses `m_{I_t,t} in [0, M_{I_t}(x_{I_t,t})]`, and
`Y_t = 1{U_t <= m_{I_t,t}}` for a fresh uniform seed. Cost `m - mu_i(x_i)`, per-pull utility
`1 + mu_i(x_i) - m in [0,2]`.

`M_(2)(X)` is the second largest of `(M_1(x_1),...,M_K(x_K))` with multiplicity,
`V_i(X) = max_{j != i} M_j(x_j)`, `b(X) = max_{h in K_H} mu_h(x_h)`, `P(n;S) = E_S sum_{t<=n} Y_t`.
`B^ctx+_{i,n}` is the contract's deviation class enlarged as in `separation/REPORT.md` (H2) so an
agent may condition on the whole arrival path. `log` is natural; `(x)_+ = max(x,0)`.

**Hypotheses.** Identical to `EXPLORER.md` (A1) to (A6), which I restate only where they bind:

* **(A1)** `K >= 2`; `mu_i, M_i` are `L`-Lipschitz in the Euclidean norm on `[0,1)^d`, with `L >= 0`
  **unknown to the platform**; a fixed nonempty honest set `K_H`.
* **(A2)** `n` known, `n >= 2K`, and `log(en) >= 3 L`, that is `n >= exp(3L)`. Fixed horizon only.
* **(A3)** The arrival path `A = (X_1,...,X_n)` is exogenous: its law does not depend on the strategy
  profile, and it is independent of the reward-seed array, of every mechanism coin and of every
  agent's private coins. It need not be i.i.d., need not have a density, and may be deterministic.
  (I adopt `PROVER2.md` defect D6: "exogenous" must include "the law does not depend on the declared
  profile", because the equilibrium statement compares two executions.)
* **(A4)** Seeds `(U_t)` i.i.d. uniform, independent of `A` and of all coins; the target is chosen
  before the seed is revealed.
* **(A5)** The deviator uses any `S'_{i,n} in B^ctx+_{i,n}`; all others play `S^*_{-i}`; honest agents
  satisfy `m_{h,t} >= mu_h(x_{h,t})` after every history.
* **(A6)** The platform knows `n`, `K`, `d` only.

**Convention F-A.** As in `EXPLORER.md` Section 5.0 and `PROVER2.md` Section 2: the base field `F_0`
contains the entire arrival path, and every filtration statement below is made relative to it. This
is licensed by (A3) and it is the hypothesis that `ADVERSARY.md` Section 7.1 shows cannot be dropped.

## 2. The mechanism PA-MESP-N

`PA-MESP-N` is `EXPLORER.md`'s `PA-MESP` (Section 8.1) with two changes: the fallback is localised
(Section 2.3), and it runs EXP4 over a net of policies rather than EXP3 over a grid of profile cells
(Section 2.4). Everything else is unchanged and I flag below exactly which of `EXPLORER.md`'s lemmas
transfer without alteration.

### 2.1 Parameters

```
g'_n   := ceil( n^{1/(d+3)} ) ,   h'_n := 1/g'_n ,   J_n := (g'_n)^d      (per-agent grid)
L_n    := ceil( n^{2/(d+3)} )                                            (elicitation length)
ell_n  := log( 2 K n^6 )                                                 (PROVER2 defect D1)
s_n    := sqrt( ell_n / (2 L_n) )                                        (bid radius)
rho_n  := sqrt(d) h'_n log(en)                                           (oscillation allowance)
sigma_n:= 3 s_n + rho_n                                                  (price shading)
b_n(r) := sqrt( r ell_n / 2 ) ,  b_n(0) := 0                             (monitor boundary)
eps_n  := n^{-1/(d+2)}                                                   (net resolution)
delta_n:= eps_n / ( 4 sqrt d log(en) )                                   (net grid side)
```

`C_j(t)` denotes the cell of `x_{j,t}` in the `J_n`-cell grid of side `h'_n` on `[0,1)^d`. Cells are
instantiated lazily. For `X, X'` in the same cell of agent `j`'s grid, every `L`-Lipschitz function of
`x_j` varies by at most `L sqrt d h'_n <= rho_n / 3`, using (A2); this is `EXPLORER.md` Fact 0 and I
use it in that form.

### 2.2 Elicitation, pricing and monitoring (unchanged from PA-MESP)

* **Elicitation.** Call round `t` *unresolved* if some `j` has fewer than `L_n` recorded pulls at the
  pair `(j, C_j(t))`. If the round is unresolved, pull the smallest-indexed such `j` and record its
  reward at `(j, C_j(t))`. The rule reads only the arrival path and the counters, never a reward, a
  bid or a coin; it satisfies `c4-safe-partitions/REPORT.md` requirement R1.
* **Pricing.** If the round is resolved, set `beta_{j,c} := L_n^{-1} sum of the L_n recorded rewards
  at (j,c)`, let `W_t` be a largest element of `(beta_{1,C_1(t)},...,beta_{K,C_K(t)})` with ties broken
  by a uniform priority permutation `Pi` drawn once before play, let `beta_(2),t` be the second order
  statistic with multiplicity, and announce `tau_t := ( beta_(2),t - sigma_n )_+`.
* **Monitoring.** One monitor per agent, global over contexts. For agent `j`, let `Z^j_r` be the sum
  of its rewards on its first `r` *primary* pulls and `T^j_r` the sum of the prices charged at those
  pulls. Declare `j` **switched** at the first `r` with `Z^j_r < T^j_r - b_n(r)`. Switching is
  permanent.

### 2.3 The localised fallback (change 1)

At a resolved round `t`, the mechanism computes `W_t` from the bids, which are frozen once
elicitation at the relevant pairs is complete.

* If `W_t` is **not switched**, pull `W_t`, charge it the price `tau_t`, and advance its monitor.
* If `W_t = j` is **switched**, the round is handed to the fallback instance `F_j`. There is at most
  one instance per agent; instance `F_j` sees the round subsequence `{ t : W_t = j, j switched
  before t }`, and these subsequences are disjoint over `j`.

**Why this is not cosmetic.** `PA-MESP` as written in `EXPLORER.md` Section 8.1 runs one global
fallback "for the remaining rounds" after the first switch of any agent. Under that rule the
deterrence accounting fails by a linear margin, for a reason independent of the comparator class.
A deviator `i` that triggers its own switch then receives fallback pulls at rounds at which `W_t != i`;
in the baseline execution it is not selected at such a round and earns `0`, while in the fallback it
earns `1 + mu_i(x_{i,t}) - (comparator value)`, which is nonnegative and typically close to `1`,
because the comparator value is at most `1`. Summed over `Theta(n)` rounds this is a linear gain. The
per-cube mechanism CG-MESP does not have this defect, because there a cube at which `i` loses never
enters the fallback at all (`EXPLORER.md` Section 7.1, paragraph "when `i` loses at `C`"), and the
defect appears only when the fallback becomes global. Localising restores the property that every
fallback round of a deviator is a round it would have won, which is the property the accounting needs.

### 2.4 EXP4 over a policy net (change 2)

**The net.** Let `G_n` be the grid of side `delta_n` on `[0,1)^d`, with `delta_n^{-d}` cells (ceilings
suppressed). Let `Val_n := { 0, eps_n/2, eps_n, ... } cap [0,1]`, of size at most `1 + 2/eps_n`. Put

```
  Phi_n := { f = (f_1,...,f_K) : each f_j is constant on each cell of G_n
                                 and takes values in Val_n } ,
  pi_f(X) := argmin over the largest coordinate, that is the smallest j attaining
             max_j f_j(x_j)  (ties by index),
  Pi_n := { pi_f : f in Phi_n } ,       N := |Phi_n| .
```

`Pi_n` is the expert set. Note that `Phi_n` is a set of *piecewise constant* functions; it is not
required to consist of Lipschitz functions, and it is fixed before play and depends on `n`, `d` and
`K` only, not on `L`, `nu`, `mu` or `M`. Section 4.1 proves the approximation property that makes
`delta_n` the right side.

**The algorithm at a fallback instance.** Instance `F_j` maintains a local clock `s = 1, 2, ...`
counting the rounds handed to it. It runs in doubling epochs: epoch `k >= 0` covers local times
`2^k, ..., 2^{k+1}-1`, starts with fresh weights `w_e = 1` for every `e in Pi_n`, and uses

```
  gamma_k := min{ 1/2 , sqrt( K log N / 2^k ) } ,   eta_k := gamma_k / K ,
  q_e := w_e / sum_{e'} w_{e'} ,  xi_a := sum_{e : e(X_t) = a} q_e ,
  p_a := (1 - gamma_k) xi_a + gamma_k / K ,
  I_t ~ p  with fresh randomness ,
  hatY_a := Y_t 1{I_t = a} / p_a ,   w_e := w_e exp( eta_k hatY_{e(X_t)} ) .
```

No local horizon is used. All `K` agents remain arms of every fallback instance forever; nobody is
ever removed. That is the manuscript's own reason for restarting EXP3 rather than suspending
(`sections/appendix_private.tex`, closing paragraph) and Section 7.2 below records why it cannot be
relaxed here either.

### 2.5 The proposed profile

`S^*`: at an elicitation pull and at a fallback pull, agent `j` delivers `M_j(x_{j,t})`. At a primary
pull the winner delivers `min{ tau_t, M_{W_t}(x_{W_t,t}) }` if strategic and
`max{ mu_{W_t}(x_{W_t,t}), min{ tau_t, M_{W_t}(x_{W_t,t}) } }` if honest. This is feasible after every
history and implementable from the messages, so `S^*_j in B^ctx+_{j,n}` for every `j`, and honest
components are honest.

## 3. First question: is the guarantee the right one?

The brief is right that "low regret against a policy class" is a different statement from what the
fallback has to do. This section states what the fallback has to do, shows that it is **not** a regret
statement, and shows that the object that supplies it is nevertheless a policy comparator.

### 3.1 The fallback's two jobs, stated exactly

Read off from `EXPLORER.md` Sections 7.1 and 7.3 and from `sections/appendix_private.tex`, the
fallback carries exactly two loads.

**(J1) Deterrence (part A).** Agent `i` deviates, everyone else plays `S^*`. On the rounds handed to
a fallback instance, `i`'s expected utility must not exceed what the baseline would have paid it on
those same rounds, up to an `o(n)` additive term. The baseline pays `1 + mu_i(x_{i,t}) - tau_t` at a
round `i` wins. So the requirement is

    E[ U_i^fb ]  <=  sum over i's fallback pulls of ( 1 + mu_i(x_{i,t}) - tau_t )  +  o(n) .

**(J2) Robustness (part C).** Every agent behaves arbitrarily subject to feasibility and to honesty
for `h in K_H`. On the rounds handed to a fallback instance, the *platform's* reward must be at least
`sum_t b(X_t) - o(n)`.

Neither is a two-sided regret statement. (J2) is a one-sided lower bound on the algorithm's reward
against one named comparator. (J1) is (J2) applied with a different comparator, plus a conservation
step: the fallback's total reward is high, the non-deviators cannot supply it, therefore the deviator
must, and supplying it costs the deviator exactly what the baseline charged it. This is the structure
of `eq:private-fallback-core` in `sections/appendix_private.tex` and of `EXPLORER.md` Lemma 7b, and
it is preserved verbatim below.

### 3.2 Comparators are floors, and the ceiling is what breaks Section 8.3

**Definition (floor vector).** Fix a fallback instance and a set of rounds it receives. A vector
`g = (g_1,...,g_K)` of functions `[0,1)^d -> [0,1]` is a **floor vector for that instance** if, at
every round `t` it receives and for every `a in [K]`,

    E[ Y_t | (history before the selection at t), I_t = a ]  >=  g_a( x_{a,t} ) .

It is a **ceiling vector** if the same display holds with `<=`. A floor vector is exactly what
`lem:selected-reactive-exp3` and `separation/REPORT.md` Lemma A need, and it is the only thing they
need: no counterfactual reward for an unselected arm is ever required.

Two observations, and they are the whole of the route.

**(O1) The comparator of (J1) and (J2) is `max_a g_a(x_a)` for a floor vector `g` whose components are
`L`-Lipschitz.** For (J2) take `g_h := mu_h` for `h in K_H` and `g_j := 0` otherwise; honesty is
exactly the floor property, feasibility gives `Y >= 0` for the others, and
`max_a g_a(x_a) = b(X)`. For (J1) take `g_j := M_j` for `j != i` and `g_i := 0`; under `S^*` a
non-deviator delivers exactly `M_j(x_{j,t})` at a fallback pull, and `max_a g_a(x_a) = V_i(X)`. Each
component is `L`-Lipschitz by (A1), or identically zero.

**(O2) For (J1) the same vector is also a ceiling on the non-deviators, pointwise, with no
discretisation.** Under `S^*` a non-deviator `j != i` delivers exactly `M_j(x_{j,t})`, and
`M_j(x_{j,t}) <= max_{j' != i} M_{j'}(x_{j',t}) = V_i(X_t)` at every round, by definition of a
maximum. There is no region, no infimum over a region, and no oscillation term.

(O2) is the exact point at which `EXPLORER.md` Section 8.3 stops applying. That section computes
`nu_i(R) = max_{j != i} inf_{X in R} M_j(x_j)` for a region `R`, which is smaller than `V_i(X_t)` by
the oscillation of `V_i` over `R`, and then has to make `R` small in the profile dimension to control
that oscillation. A policy comparator never forms the infimum: the comparator's value at round `t` is
`V_i(X_t)` itself, and the only loss is the net's approximation error `2 eps_n`, which is a free
parameter bought at `log N`, not at `N`. The requirement of Section 8.3, "`nu_i >= tau_t - epsilon`
with `epsilon = O(n^{-1/(d+3)})`", is then met with `epsilon = 2 eps_n` and, more to the point, the
underlying inequality `tau_t <= V_i(X_t)` holds *pointwise and exactly* at every round the deviator
wins (Lemma N3(c) below). The four-line derivation in Section 8.3 is correct; its hypothesis, that
the fallback's only instrument is a value constant on a region, is what fails.

### 3.3 The honest comparator is in the class, and its lack of smoothness is irrelevant

The brief asks what happens when the honest agent's delivered map is not smooth. It need not be, and
it does not matter, for a reason that is worth stating because it is the same reason
`separation/REPORT.md` Lemma C works.

An honest agent `h` may deliver any `m_{h,t} >= mu_h(x_{h,t})`, adaptively, discontinuously, and
differently on each visit to the same context. The comparator does not use that map. It uses
`mu_h`, which is `L`-Lipschitz by (A1) and is a pointwise lower bound on the delivery after every
history. The benchmark of part (C) is `b(X) = max_{h in K_H} mu_h(x_h)`, which is defined from `mu`
and not from the delivery, so the comparator and the benchmark are the *same* object. Smoothness is
used once, to build a finite net that covers `mu_h`, and nowhere else. The same remark applies to
part (A): under `S^*` the delivery of a non-deviator equals `M_j(x_j)` exactly, which is `L`-Lipschitz
by (A1), so there the floor and the ceiling coincide and are both smooth by hypothesis.

Where this would fail, and it is worth recording because it is the boundary of the route: if the
paper ever weakened (A1) to "`mu_i` continuous with no modulus", the net could not be built without
knowing the modulus, exactly as `EXPLORER.md` Section 7.5 item 4 records for the price shading. The
route inherits that hypothesis and does not add to it.

### 3.4 What "close to the best policy in the net" would and would not give

I do not use, and the route does not need, a statement of the form "the algorithm is close to the
best policy in `Pi_n`". Such a statement is not even well posed here: the "reward of an unplayed
policy" is a counterfactual over a reactive agent's behaviour, and `MATH_CANDIDATE_LEDGER.md`
Section 6.1 and `separation/REPORT.md` Part 1 are both about how badly counterfactual reasoning fails
in this model. What Lemma N2 below gives is the one-sided statement

    E[ sum over the instance's rounds of Y_t ]  >=  sum over those rounds of g_{e(X_t)}( x_{e(X_t),t} )
                                                     -  R^dbl_{K,N}( H ) ,

for **one** expert `e` chosen by the analyst and **one** floor vector `g` valid for that instance. The
algorithm does not know `e`, does not know `g`, and does not have to. This is exactly the shape of
`lem:selected-reactive-exp3`, and its whole content is that a floor is enough. The comparator is not
"the best policy"; it is "a policy whose recommendations are backed by a floor", which is a weaker
object, available here, and sufficient.

The net enters only through the approximation step: the analyst's ideal comparator `argmax_a g_a(x_a)`
is generally not in `Pi_n`, so a net member `f` with `||f_a - g_a||_inf <= eps_n / 2` is used instead,
and Lemma N1(b) converts that into a loss of at most `eps_n` per round in the floor value. Both steps
are one-sided and neither needs a counterfactual.

## 4. Second question: the counting and the balance, re-derived

I did not take the sketch's exponent on trust. Every count below is proved here, and Section 4.4
re-solves all three free parameters (`h'_n`, `L_n`, `eps_n`) simultaneously rather than importing
`h'_n` and `L_n` from `EXPLORER.md` Section 8.2.

### 4.1 Lemma N1 (net cardinality and approximation, elementary, no citation load bearing)

**Lemma N1.** Let `q := ceil(1/delta_n)`, so `G_n` has at most `q^d` cells, and let
`v := 1 + ceil(2/eps_n)` bound `|Val_n|`. Then

(a) `N = |Phi_n| <= v^{K q^d}`, that is `log N <= K q^d log( 1 + ceil(2/eps_n) )`;

(b) for every `g = (g_1,...,g_K)` with each `g_a : [0,1)^d -> [0,1]` either `L`-Lipschitz or
identically `0`, and under (A2), there is `f in Phi_n` with `max_a ||f_a - g_a||_inf <= eps_n/2`;

(c) for such an `f` and every `X`, writing `pi_f(X)` for the arm it recommends,

    g_{pi_f(X)}( x_{pi_f(X)} )  >=  max_a g_a(x_a)  -  eps_n .

*Proof.* (a) A member of `Phi_n` is a choice of one element of `Val_n` for each of the `K q^d` pairs
(agent, cell of `G_n`). (b) For a cell `c` of `G_n` pick any point `z_c in c` and let `f_a` take on `c`
the nearest element of `Val_n` to `g_a(z_c)`, which is within `eps_n/4` since `Val_n` has step
`eps_n/2` and covers `[0,1]`. For `x in c`, `|g_a(x) - g_a(z_c)| <= L sqrt d delta_n` because the cell
has diameter at most `sqrt d delta_n`, and
`L sqrt d delta_n = L eps_n / (4 log(en)) <= eps_n/4` by (A2), which gives `log(en) >= 3L >= L`. Adding
the two errors gives `eps_n/2`. The identically zero components are represented exactly. (c) Let
`a^* attain max_a g_a(x_a)` and `a := pi_f(X)`. Then
`g_a(x_a) >= f_a(x_a) - eps_n/2 >= f_{a^*}(x_{a^*}) - eps_n/2 >= g_{a^*}(x_{a^*}) - eps_n`. `QED`

Note what (b) does **not** need: the platform never knows `L`. The net is built from `n`, `K`, `d`
alone, and (A2) is exactly the hypothesis that makes `log(en)` a legitimate surrogate for `L`. This is
the same device that `EXPLORER.md` uses for the shading `rho_n = sqrt d h'_n log(en)`, so the route
adds no hypothesis. This closes the second of the three gaps `EXPLORER.md` Section 8.6 lists.

Rates: with `eps_n = n^{-1/(d+2)}` and `delta_n = eps_n/(4 sqrt d log(en))`,

    log N  <=  K ( 1 + 4 sqrt d log(en) n^{1/(d+2)} )^d log( 1 + 2 n^{1/(d+2)} )
           =   O( K (4 sqrt d)^d (log(en))^d n^{d/(d+2)} log n ) ,

so `log N = O(n^{d/(d+2)} polylog(n))` and `N = exp(Theta(n^{d/(d+2)}))`. Both facts matter: the first
is what makes the rate work, the second is Section 6.

### 4.2 Lemma N2 (selected-reactive EXP4 with a floor vector, unknown local horizon)

This is the load-bearing step `EXPLORER.md` Section 8.6 says is not written. It is the manuscript's
`lem:selected-reactive-exp3` with three changes: the expert set is a set of policies rather than the
arms; the comparator value varies with the round; and the instance's round set is random and
predictable rather than a known horizon. The third change also removes a hypothesis that both
`separation/REPORT.md` Lemma A (deterministic `T`) and `EXPLORER.md` Lemma 7 (`H_C` is
`F_0`-measurable) need, and I record that as a by-product.

Set `R_{K,N}(H) := 3 sqrt( K H log N ) + 2 K log N`, `R_{K,N}(0) := 0`, and
`R^dbl_{K,N}(V) := 11 sqrt( K (V+1) log N ) + 2 K log N log_2( 2(V+1) )`, `R^dbl_{K,N}(0) := 0`.

**Lemma N2.** Fix a fallback instance `F_j`. For each global round `t` let
`psi_t := 1{ round t is handed to F_j }` and suppose `psi_t` is `F_{t-1}`-measurable. Let `g` be a
floor vector for `F_j` in the sense of Section 3.2 and let `e in Pi_n` be any expert. Let
`H := sum_t psi_t`. Then, for any behaviour of every agent,

    E[ sum_t psi_t Y_t ]  >=  E[ sum_t psi_t g_{e(X_t)}( x_{e(X_t),t} ) ]  -  E[ R^dbl_{K,N}(H) ] .

*Proof.* Fix an epoch `k` and let `phi_t := psi_t 1{round t falls in epoch k of F_j}`, which is again
`F_{t-1}`-measurable because the instance's local clock is a function of `(psi_s)_{s<t}`. Write
`T_k := sum_t phi_t <= 2^k`. Within the epoch the weights are fresh and `gamma := gamma_k`,
`eta := gamma/K`. Because `p_a >= gamma/K = eta` we have `0 <= eta hatY_{a,t} <= 1`, so from
`e^x <= 1 + x + x^2` on `[0,1]`, with `W` the total weight and `q` the normalised weights,

    W_{t+1}/W_t  <=  1 + eta sum_{e'} q_{e'} hatY_{e'(X_t)} + eta^2 sum_{e'} q_{e'} hatY_{e'(X_t)}^2 ,

at rounds with `phi_t = 1` and `W_{t+1} = W_t` otherwise. Taking logarithms, using
`log(1+u) <= u`, telescoping over the epoch, and using `log W_end >= log w_e = eta sum_t phi_t
hatY_{e(X_t)}`, we get the pathwise inequality

    sum_t phi_t hatY_{e(X_t)}  <=  (log N)/eta  +  sum_t phi_t sum_a xi_{a,t} hatY_{a,t}
                                   +  eta sum_t phi_t sum_a xi_{a,t} hatY_{a,t}^2 ,      (*)

where `xi_{a,t} := sum_{e' : e'(X_t) = a} q_{e',t}` and I used
`sum_{e'} q_{e'} hatY_{e'(X_t)} = sum_a xi_a hatY_a` and the same identity for the squares. `(*)` is
pathwise and holds however many rounds the epoch actually receives.

Now condition. Write `r_{a,t} := E[Y_t | F_{t-1}, I_t = a]`, which is well defined because the selected
agent's target is `F_{t-1} v sigma(I_t, its coin)`-measurable and the seed is fresh by (A4). Since
`phi_t` and `xi_t` are `F_{t-1}`-measurable and `I_t ~ p_t` with fresh randomness,

    E[ phi_t hatY_{a,t} | F_{t-1} ]  =  phi_t r_{a,t} ,
    E[ phi_t sum_a xi_a hatY_a^2 | F_{t-1} ]  =  phi_t sum_a xi_a r_a / p_a  <=  phi_t K/(1-gamma) ,

using `Y^2 <= Y`, `p_a >= (1-gamma) xi_a` and `r_a <= 1`. Also
`E[phi_t Y_t | F_{t-1}] = phi_t sum_a p_a r_a >= (1-gamma) phi_t sum_a xi_a r_a`. Taking total
expectations in `(*)`, using `r_{e(X_t),t} >= g_{e(X_t)}(x_{e(X_t),t})` (the floor property) and
`eta = gamma/K`,

    E[ sum_t phi_t g_{e(X_t)} ]  <=  (K log N)/gamma  +  (1-gamma)^{-1} E[ sum_t phi_t Y_t ]
                                     +  gamma E[T_k]/(1-gamma) .

Multiplying by `(1-gamma) <= 1`, rearranging, using `g <= 1` and `T_k <= 2^k`,

    E[ sum_t phi_t Y_t ]  >=  E[ sum_t phi_t g_{e(X_t)} ]  -  2 gamma 2^k  -  (K log N)/gamma .

The two cases `gamma_k = sqrt(K log N/2^k)` and `gamma_k = 1/2` (the latter only when
`2^k < 4 K log N`, where `2^k < 2 sqrt(K 2^k log N)`) bound the loss by `R_{K,N}(2^k)`, exactly as in
`separation/REPORT.md` Lemma A with `log N` in place of `log K`. Summing over the epochs started, whose
number is `ceil(log_2(H+1))` and whose planned lengths satisfy `2^{m} <= 2(H+1)`, and applying
`separation/REPORT.md` Lemma B with `log N` in place of `log K`, gives
`sum_k R_{K,N}(2^k) <= R^dbl_{K,N}(H)` pathwise; taking expectations gives the claim. `QED`

**By-product.** Lemma N2 never uses a deterministic epoch length and never needs the instance's total
round count to be `F_0`-measurable. It needs only that the indicator "round `t` belongs to this
instance and this epoch" is `F_{t-1}`-measurable, which is the same predictability that
`EXPLORER.md` Lemma 6 and `PROVER2.md` Lemma P6 need for the monitor and which both name as their
least secure step. If Lemma N2 is right, the corresponding hypotheses of `separation/REPORT.md`
Lemma A (Section 2.7 item 7, "oblivious contexts only, because the realized epoch lengths become
random") and of `EXPLORER.md` Lemma 7 can be weakened the same way. **I have not checked what else in
those two reports depends on the stronger form, and this by-product should not be used before someone
does.**

### 4.3 Lemma N3 (prices, per round) and Lemma N4 (honest bid), imported

These are `EXPLORER.md` Lemmas 3, 4, 5, 8 and 9 in their `PA-MESP` form, which `EXPLORER.md`
Section 8.2 states transfer with the same proofs and which `PROVER2.md` Section 12 reports checking in
the `CG-MESP` form. I restate only the four consequences I use and I do not reprove them.

Let `G := { |beta_{j,c} - bar M_{j,c}| <= s_n for every (j,c) whose elicitation completes }` where
`bar M_{j,c}` is the average of the `L_n` capacity-play means at that pair, together with the
deviator's counterfactual bid; `Pr(G) >= 1 - n^{-4}` (`EXPLORER.md` Lemma 3, whose proof needs the
elicitation schedule to be reward independent, which Section 2.2 is).

(a) *(bid domination and winner inclusion)* On the coupling of the deviating and baseline executions
by common seeds, coins and priority, `beta'_{i,c} <= beta^cap_{i,c}` pathwise, the two executions run
identical elicitation schedules, and if `i` wins at round `t` in the deviating execution it wins at
round `t` in the baseline execution and both face the same price, because when `i` wins the second
order statistic equals `max_{j != i} beta_{j,C_j(t)}`, which does not involve `i`'s bid.

(b) *(the winner can meet the price)* On `G`, at every resolved round,
`tau_t <= M_{W_t}( x_{W_t,t} )`.

(c) *(the price is below the runner-up capacity)* On `G`, at every resolved round, with `j^*` the agent
attaining `beta_(2),t`, `tau_t <= M_{j^*}( x_{j^*,t} )`. In particular, at a round at which `i` wins,
`j^* != i` and therefore `tau_t <= V_i(X_t)`.

(d) *(the price is close to the second capacity at `S^*`)* At `S^*` and on `G`,
`tau_t >= M_(2)(X_t) - 4 s_n - (4/3) rho_n` at every resolved round.

(e) *(honest bid)* Under arbitrary joint behaviour with honest agents honest, the event
`G_H := { beta_{h,c} >= inf_{x in c} mu_h(x) - s_n for every honest h and every completed pair }` has
`Pr(G_H) >= 1 - n^{-4}`, and `inf_{x in c} mu_h(x) >= mu_h(x_{h,t}) - rho_n/3` for `x_{h,t} in c`.

The derivation of (b) and (c) is the three-inequality chain of `EXPLORER.md` Lemma 5, which spends
`L sqrt d h'_n + s_n <= 3 s_n + rho_n = sigma_n` and uses (A2) through
`rho_n >= 3 L sqrt d h'_n`. I checked the chain; I did not reprove the concentration.

### 4.4 The balance, solved from scratch in all three parameters

The mechanism has three free parameters, `h'_n` (per-agent grid), `L_n` (elicitation length) and
`eps_n` (net resolution). The error terms of Theorem G1 are

```
e_bid    := min{ J_n L_n , n }                    deviator's own elicitation harvest
e_elicit := min{ K J_n L_n , n }                  all elicitation rounds
e_osc    := n rho_n = sqrt d n h'_n log(en)       within-cell oscillation (enters only inside e_price)
e_price  := n ( 4 s_n + (4/3) rho_n )             price slack
e_mon    := K ( 1 + 2 b_n(n) )                    monitoring slack, per agent, global
e_net    := eps_n n                               net approximation
e_fb     := 11 K sqrt( (n+K) log N ) + 2 K^2 log N log_2( 2(n+1) )    fallback regret
```

Only `e_bid`, `e_elicit`, `e_osc`, `e_price` involve `(h'_n, L_n)`; only `e_net`, `e_fb` involve
`eps_n`; `e_mon` involves neither. **The two balances are therefore independent**, which is the
structural reason the route works and the reason `EXPLORER.md` Section 8.3's coupling was the whole
obstruction.

**Pricing balance.** Minimising `max{ K h^{-d} L , n sqrt(ell_n/(2L)) , sqrt d n h log(en) }` over
`h in (0,1]`, `L >= 1`: equating the first two and the last two gives `L = n h^{d+1}` and
`L = h^{-2}` up to logarithms, hence `h^{d+3} = 1/n`, that is
`h'_n = n^{-1/(d+3)}`, `L_n = n^{2/(d+3)}`, value `Theta( n^{(d+2)/(d+3)} log n )`. This is
`EXPLORER.md` Section 8.2's choice and it is also the manuscript's Grid-ETC balance
(`sections/contextual_samf_algorithm.tex`: "Lipschitz bias `n h_n`, exploration `q_n h_n^{-D}`, and
simple regret `n/sqrt(q_n)`"), with `d` in place of `D` and `L_n` in the role of `q_n`. **Nothing about
the fallback enters it, so it cannot be improved by retuning the fallback.**

**Fallback balance.** Minimising `eps n + 11 K sqrt(n log N(eps))` with
`log N(eps) = O( K (4 sqrt d log(en))^d eps^{-d} log(1/eps) )` gives
`eps^{d+2} = Theta( K^4 (4 sqrt d log(en))^d log(1/eps) / n )`, hence
`eps_n = Theta( ( K^4 (4 sqrt d log(en))^d log n / n )^{1/(d+2)} )` and value
`Theta( n^{(d+1)/(d+2)} polylog(n) )`. Taking the cleaner `eps_n = n^{-1/(d+2)}` of Section 2.1 gives
the same exponent with a slightly worse constant, which is what I use.

**The comparison.** `(d+1)/(d+2) < (d+2)/(d+3)` for every `d >= 0`, with
`(d+2)/(d+3) - (d+1)/(d+2) = 1/((d+2)(d+3)) > 0`; I checked this symbolically in `exponents.py` for
`d = 0,...,11`. So the fallback is **strictly not binding**, and the mechanism's exponent is the
pricing exponent for every `K`. The margin is not thin in the sense of being a coincidence, but it is
thin in size: at `d = 3` the two exponents are `0.8000` and `0.8333`. The gap shrinks like `1/d^2`, so
a fallback whose regret were worse than `sqrt(K H log N)` by a factor `H^{alpha}` with
`alpha > 1/((d+2)(d+3))` would break the conclusion. That is the sensitivity a referee should test and
it is the reason Section 6.4's `T^{2/3}`-style oracle-efficient rates matter: see Section 6.3.

**Exponent table** (`exponents.py`; `price` is `(d+2)/(d+3)`, `fb_grid` is `EXPLORER.md`
Section 8.3's `(D+d+3)/(2(d+3))`, `fb_net` is `(d+1)/(d+2)`, `CG` is `(D+2)/(D+3)`):

| `K` | `d` | `D` | price | fb_grid | fb_net | PA with grid fallback | PA with net fallback | CG-MESP |
|:-|:-|:-|:-|:-|:-|:-|:-|:-|
| 2 | 1 | 2 | 0.7500 | 0.7500 | 0.6667 | 0.7500 | 0.7500 | 0.8000 |
| 3 | 1 | 3 | 0.7500 | 0.8750 | 0.6667 | 0.8750 | 0.7500 | 0.8333 |
| 4 | 1 | 4 | 0.7500 | 1.0000 | 0.6667 | 1.0000 | 0.7500 | 0.8571 |
| 5 | 1 | 5 | 0.7500 | 1.1250 | 0.6667 | 1.1250 | 0.7500 | 0.8750 |
| 2 | 2 | 4 | 0.8000 | 0.9000 | 0.7500 | 0.9000 | 0.8000 | 0.8571 |
| 3 | 2 | 6 | 0.8000 | 1.1000 | 0.7500 | 1.1000 | 0.8000 | 0.8889 |
| 4 | 2 | 8 | 0.8000 | 1.3000 | 0.7500 | 1.3000 | 0.8000 | 0.9091 |
| 3 | 3 | 9 | 0.8333 | 1.2500 | 0.8000 | 1.2500 | 0.8333 | 0.9167 |
| 5 | 3 | 15 | 0.8333 | 1.7500 | 0.8000 | 1.7500 | 0.8333 | 0.9444 |

The "PA with net fallback" column is constant in `K`. That is the whole point of the route and it is
what `EXPLORER.md` Section 8.3's table does not contain.

**Robustness of the balance.** The conclusion does not depend on choosing `eps_n` optimally. Taking
the much coarser `eps_n = n^{-1/(d+3)}`, the pricing resolution, gives
`log N = O(n^{d/(d+3)} polylog)` and `e_fb = O( n^{(2d+3)/(2d+6)} polylog )`, and
`(2d+3)/(2d+6) < (2d+4)/(2d+6) = (d+2)/(d+3)`, so the fallback is still not binding. There is roughly a
one-exponent-unit cushion, and I take that as evidence that the balance is not an artefact of a
convenient parameter choice. This is the check the brief asks for, and it passes.

## 5. Theorem G1 and its proof

### 5.1 Lemma N5 (the per-agent monitor with a predictable price)

**Lemma N5.** For agent `j` let `psi^j_t := 1{ round t is a primary pull of j }`, let `Y^j_r` and
`m^j_r` be the reward and target at its `r`-th primary pull and `tau^j_r` the price charged there, and
put `Z_r := sum_{q<=r} Y^j_q`, `A_r := sum_{q<=r} m^j_q`, `T_r := sum_{q<=r} tau^j_q`, extended by zero
increments beyond the realised count. Let `H := { |Z_r - A_r| <= b_n(r) for every j and every r <= n }`.
Under (A3), (A4) and Convention F-A, and for any behaviour of every agent:

(a) `Pr(H^c) <= 2 K n e^{-ell_n} = n^{-5}`;
(b) on `H`, if `j`'s primary phase lasted `q` pulls counting its failing pull when there is one, then
    `A_q >= T_q - 1 - 2 b_n(q)`;
(c) on `H`, `j`'s realised primary utility satisfies
    `U^pri_j <= sum_{r<=q} ( 1 + mu_j(x_{j,r}) - tau^j_r ) + 1 + 2 b_n(q)`;
(d) on `H`, if every primary target of `j` is at least the price charged at that pull, `j` never
    switches;
(e) `E[ Z_r - A_r ] = 0` for `r` the total number of primary pulls of `j`.

*Proof.* Identical to `EXPLORER.md` Lemma 6 and `PROVER2.md` Lemma P6 with the cube replaced by the
agent, with two substitutions. First, `psi^j_t` is `F_{t-1}`-measurable: whether round `t` is resolved
and who `W_t` is are determined by `X_t` (in `F_0` by Convention F-A) and by the elicitation counters
and recorded rewards at rounds before `t`, and whether `j` has switched is determined by rewards at
rounds before `t`. Second, the comparison level is the predictable sequence `tau^j_r` rather than a
constant `tau_C`; the martingale `N_t := sum_{s<=t} psi^j_s (Y_s - m_{j,s})` and the Hoeffding
conditional moment bound do not involve the comparison level at all, and (b) follows from the
negation of the switch test `Z_r >= T_r - b_n(r)` exactly as before, using `tau^j_q <= 1` for the
failing pull. The union bound is over `K` agents and `n` values of `r` and two tails, giving
`2 K n e^{-ell_n} = 2 K n / (2 K n^6) = n^{-5}` with `ell_n = log(2 K n^6)`; this is the corrected
count of `PROVER2.md` defect D1, applied here to a per-agent rather than a per-cube monitor, where the
index set `{(j,r)}` is genuinely deterministic and the objection D1 raises does not arise. `QED`

### 5.2 Theorem G1

Recall `e_bid`, `e_elicit`, `e_osc`, `e_price`, `e_mon`, `e_net`, `e_fb` from Section 4.4, and put
`e_1fb := 11 sqrt( K (n+1) log N ) + 2 K log N log_2( 2(n+1) )` (one fallback instance).

**Theorem G1.** Assume (A1) to (A6) and run PA-MESP-N of Section 2. Then:

**(A) Additive behavioural equilibrium.** For every agent `i` and every `S'_{i,n} in B^ctx+_{i,n}`,

    u_i(n; S'_{i,n}, S^*_{-i,n})  -  u_i(n; S^*_n)
        <=  e_bid  +  ( 1 + 2 b_n(n) )  +  e_net  +  e_1fb  +  4 n^{-3} .

**(B) Second-capacity revenue.**

    P(n; S^*_n)  >=  E[ sum_{t<=n} M_(2)(X_t) ]  -  ( e_elicit + e_price + 2 n^{-3} ) .

**(C) Honest-benchmark robustness.** For every feasible behavioural profile `S` in which every agent
plays some strategy in `B^ctx+_{j,n}` and every honest agent respects pointwise honesty (the deviating
set may be all of `[K]`),

    P(n; S)  >=  E[ sum_{t<=n} b(X_t) ]  -  ( e_elicit + e_price + e_mon + e_net + e_fb + 2 n^{-3} ) .

**(D) Rates.** For fixed `K` and `d` there is `n_2(K,d)` such that for `n >= max{ n_2(K,d), exp(3L) }`
all three error terms are `O( n^{(d+2)/(d+3)} log(e K n) )`, with constants depending on `K` and `d`
only and on no other feature of the instance. Explicitly
`e_bid <= 2^{d+1} n^{(d+2)/(d+3)}`, `e_elicit <= K 2^{d+1} n^{(d+2)/(d+3)}`,
`e_osc <= sqrt d n^{(d+2)/(d+3)} log(en)`,
`e_price <= (4 sqrt(ell_n/2) + (4/3) sqrt d log(en)) n^{(d+2)/(d+3)}`,
`e_mon <= K(1 + sqrt(2 n ell_n))`, `e_net = n^{(d+1)/(d+2)}`, and
`e_fb = O( K^{3/2} (4 sqrt d)^{d/2} (log en)^{(d+1)/2} n^{(d+1)/(d+2)} )
     + O( K^2 (4 sqrt d)^d (log en)^{d} n^{d/(d+2)} (log n)^2 )`,
whose exponents `(d+1)/(d+2)`, `d/(d+2)` and `1/2` are all strictly below `(d+2)/(d+3)`.
Consequently `S^*` is an additive behavioural asymptotic equilibrium in the sense of contract
Definition 1, `P(n;S^*) = E sum_t M_(2)(X_t) - o(n)`, and the honest benchmark holds at the same order,
uniformly over all deviations and all instances satisfying (A1) with the given `L`.

**What is new relative to `EXPLORER.md` Theorem 1.** The exponent is `(d+2)/(d+3)` rather than
`(D+2)/(D+3)`, for every `K`, which is the point. The bound in part (A) has no oscillation term,
because the accounting is per round rather than per cube and the true `mu_i(x_{i,t})` is available at
each round. The monitoring slack is `K(1 + 2 b_n(n))` rather than `EXPLORER.md`'s
`J'_n + 2 sqrt(J'_n n ell_n/2)`, because the monitor is per agent. Everything else is weaker or equal.

### 5.3 Proof of part (A)

Couple the deviating and the baseline execution by common seeds, coins and priority as in Lemma
N3(a), and condition on the arrival path throughout (Convention F-A); every bound is uniform in `A`.
Write `G` for the good elicitation event and `H` for the monitoring event; `Pr((G cap H)^c) <= 2 n^{-4}`
across the two executions.

**Step 1 (elicitation, pathwise, every event).** The elicitation rule reads only the counters and the
contexts, so the two executions pull the same agent at the same round throughout elicitation. At agent
`i`'s elicitation pulls the per-pull utilities differ by `M_i(x_{i,t}) - m'_{i,t} in [0,1]`, and the
number of such pulls is at most `min{ J_n L_n, n } = e_bid`, since each advances one of the `J_n`
counters of the pairs `(i, c)` and each stops at `L_n`. Contribution at most `e_bid`.

**Step 2 (only `i` can be switched).** Work on `G cap H`. For `j != i` playing `S^*`, at a primary pull
with `W_t = j` the target is `min{ tau_t, M_j(x_{j,t}) } = tau_t` if `j` is strategic, by Lemma N3(b),
and at least `tau_t` if `j` is honest. By Lemma N5(d), `j` never switches. Hence on `G cap H` the only
fallback instance that ever exists in the deviating execution is `F_i`, and it receives exactly the
rounds `F := { t resolved : W'_t = i, i switched before t }`. In particular `i` receives no
post-elicitation pull at any round with `W'_t != i`. This is the step that the localisation of
Section 2.3 buys and that a global fallback does not give.

**Step 3 (the primary phase of `i`).** Let `q` be the number of `i`'s primary pulls in the deviating
execution, all at rounds with `W'_t = i`. By Lemma N3(a) every such round is a baseline win at the
identical price `tau_t`. Put, for a round `t`,

    w_t  :=  1 + mu_i(x_{i,t}) - tau_t            if i is strategic,
    w_t  :=  min{ 1 , 1 + mu_i(x_{i,t}) - tau_t } if i is honest,

which is nonnegative because `tau_t <= M_i(x_{i,t}) <= 1 <= 1 + mu_i(x_{i,t})` by Lemma N3(b) at a
round `i` wins. Lemma N5(c) gives `U'^pri_i <= sum over those q rounds of w_t + 1 + 2 b_n(q)` in the
strategic case, and `U'^pri_i <= q` in the honest case because every honest target is at least
`mu_i(x_{i,t})`; taking the smaller of the two gives `U'^pri_i <= sum_t w_t + 1 + 2 b_n(q)` in both.

**Step 4 (the fallback phase of `i`).** `psi_t := 1{t in F}` is `F_{t-1}`-measurable by the argument of
Lemma N5. Define the floor vector `g^{(i)}` by `g^{(i)}_j := M_j` for `j != i` and `g^{(i)}_i := 0`. It
is a floor vector for `F_i`: a non-deviator `j != i` delivers exactly `M_j(x_{j,t})` at a fallback pull
under `S^*`, and `i` delivers at least `0`. By Lemma N1(b) choose `f in Phi_n` with
`max_a ||f_a - g^{(i)}_a||_inf <= eps_n/2` and put `e := pi_f`. Lemma N2 and Lemma N1(c) give

    E[ sum_{t in F} Y_t ]  >=  E[ sum_{t in F} ( V_i(X_t) - eps_n ) ]  -  E[ R^dbl_{K,N}(|F|) ] .

By (A4) and the tower property `E[sum_{t in F} Y_t] = E[sum_{t in F} m_{I_t,t}]`. Split the right side
by whether `I_t = i`. For `I_t = j != i` the target is `M_j(x_{j,t}) <= V_i(X_t)` pointwise, by the
definition of `V_i` as a maximum over `j != i`. Hence, writing `Q := { t in F : I_t = i }`,

    E[ sum_{t in Q} m_{i,t} ]  >=  E[ sum_{t in Q} V_i(X_t) ]  -  eps_n E|F|  -  E[R^dbl_{K,N}(|F|)] ,

and therefore

    E[ U'^fb_i ]  =  E[ sum_{t in Q} ( 1 + mu_i(x_{i,t}) - m_{i,t} ) ]
                 <=  E[ sum_{t in Q} ( 1 + mu_i(x_{i,t}) - V_i(X_t) ) ]  +  eps_n n  +  E[R^dbl_{K,N}(n)] .

By Lemma N3(c), at a round at which `i` wins the runner-up is not `i`, so `tau_t <= V_i(X_t)` and
`1 + mu_i(x_{i,t}) - V_i(X_t) <= w_t` in the strategic case; in the honest case `U'^fb_i <= |Q|` because
every honest target is at least `mu_i(x_{i,t})`, and `w_t = min{1, .}`, so taking the smaller of the two
bounds gives `E[U'^fb_i] <= E[ sum_{t in Q} w_t ] + e_net + e_1fb` in both cases. Since `w_t >= 0` and
`Q subset F`, this is at most `E[ sum_{t in F} w_t ] + e_net + e_1fb`.

**Step 5 (the baseline).** In the baseline every agent plays `S^*`, so by Step 2 applied to `i` as well
no agent ever switches on `G cap H`, and `i` receives every round it wins as a primary pull, earning
`w_t` there. By Lemma N3(a) `F` is contained in the set of baseline wins of `i`, and the `q` rounds of
Step 3 are too, and these two sets are disjoint because a round of `F` is after `i`'s switch. Hence the
baseline post-elicitation utility is at least `sum over the q rounds of w_t + sum_{t in F} w_t`.

**Step 6 (summation).** Subtracting Step 5 from Steps 3 and 4 leaves
`1 + 2 b_n(q) + e_net + e_1fb`, and `b_n` is nondecreasing so `b_n(q) <= b_n(n)`. Adding Step 1 and
charging `(G cap H)^c` at `2 n Pr((G cap H)^c) <= 4 n^{-3}` because per-pull utilities lie in `[0,2]`
gives part (A). `QED`

### 5.4 Proof of part (B)

All agents play `S^*`, so `beta_{j,c} = beta^cap_{j,c}` for every pair. By (A4) and the tower property,
`P(n;S^*) = E[ sum_{t<=n} m_{I_t,t} ]`; no optional stopping is used. Discard the elicitation rounds, at
most `min{ K J_n L_n, n } = e_elicit` of them, on which the target is nonnegative. On `G cap H`: by
Lemma N3(b) the primary target at every resolved round is exactly `tau_t` (strategic winner) or at
least `tau_t` (honest winner), so by Lemma N5(d) no agent ever switches, so every resolved round is a
primary round; and by Lemma N3(d), `m_{I_t,t} >= tau_t >= M_(2)(X_t) - 4 s_n - (4/3) rho_n`. Off
`G cap H` targets are nonnegative and `M_(2) <= 1`, costing at most `n Pr((G cap H)^c) <= 2 n^{-3}`.
Adding back the discarded rounds at `M_(2) <= 1` each gives part (B). `QED`

### 5.5 Proof of part (C)

Now every agent may behave arbitrarily subject to feasibility and to honesty on `K_H`, so `G` is
unavailable; replace it by `G_H` of Lemma N3(e), with `Pr(G_H^c) <= n^{-4}`. Work on `G_H cap H` and
discard the at most `e_elicit` elicitation rounds, charged at `b <= 1` each. Fix a resolved round `t`
and let `h_t in K_H` attain `b(X_t)`.

*Case (i): `W_t = h_t` and `h_t` not switched.* The primary target at `t` is at least
`mu_{h_t}(x_{h_t,t}) = b(X_t)` by honesty, and `E[Y_t | F_{t-1}, I_t] = m_{I_t,t}` by (A4).

*Case (ii): `W_t != h_t` and `W_t` not switched.* By Lemma N3(e),
`beta_(2),t >= beta_{h_t, C_{h_t}(t)} >= inf_{x in C_{h_t}(t)} mu_{h_t}(x) - s_n >= b(X_t) - rho_n/3 - s_n`,
so `tau_t >= b(X_t) - 4 s_n - (4/3) rho_n`. Lemma N5(b) applied to `W_t` gives, over its primary pulls,
`A_q >= T_q - 1 - 2 b_n(q)`, and Lemma N5(e) turns the target sum into expected reward. Summed over the
at most `K` agents this costs `K(1 + 2 b_n(n)) = e_mon` in total.

*Case (iii): `W_t = j` switched.* The round is handed to `F_j`. Define the floor vector `g^H` by
`g^H_h := mu_h` for `h in K_H` and `g^H_a := 0` otherwise; it is a floor vector for every instance, by
honesty for `h in K_H` and by `Y >= 0` for the rest, and `max_a g^H_a(x_a) = b(X)`. By Lemma N1 choose
`f` with `max_a ||f_a - g^H_a||_inf <= eps_n/2` and apply Lemma N2 with `e := pi_f` to each instance:

    E[ sum over F_j's rounds of Y_t ]  >=  E[ sum over those rounds of ( b(X_t) - eps_n ) ]
                                           -  E[ R^dbl_{K,N}( H_j ) ] .

The instances' round sets are disjoint, `sum_j H_j <= n`, and by Cauchy and Schwarz
`sum_j 11 sqrt( K (H_j+1) log N ) <= 11 sqrt(K log N) sqrt( K sum_j (H_j+1) ) <= 11 K sqrt( (n+K) log N )`,
while the logarithmic parts sum to at most `2 K^2 log N log_2(2(n+1))`. Together these are `e_fb`, and
the approximation losses sum to at most `eps_n n = e_net`.

Adding the three cases, charging `e_elicit` for the elicitation rounds and
`n Pr((G_H cap H)^c) <= 2 n^{-3}` for the bad event, gives part (C). `QED`

**A remark on the constant.** I use `e_price = n(4 s_n + (4/3) rho_n)` in part (C) where
`EXPLORER.md` uses `e_rob = n(4 s_n + (5/3) rho_n)`; the improvement is `PROVER2.md` defect D3 and it
costs nothing.

### 5.6 Proof of part (D)

`J_n = (g'_n)^d <= (n^{1/(d+3)}+1)^d <= 2^d n^{d/(d+3)}` and `L_n <= 2 n^{2/(d+3)}`, so
`e_bid <= J_n L_n <= 2^{d+1} n^{(d+2)/(d+3)}` and `e_elicit <= K e_bid`. `h'_n <= n^{-1/(d+3)}` gives
`e_osc <= sqrt d n^{(d+2)/(d+3)} log(en)`. `n s_n = n sqrt(ell_n/(2 L_n)) <= sqrt(ell_n/2)
n^{(d+2)/(d+3)}` gives the stated `e_price`. `b_n(n) = sqrt(n ell_n/2)` gives `e_mon`. `e_net` is
`n^{(d+1)/(d+2)}` by definition. For `e_fb`, Section 4.1 gives
`log N = O(K (4 sqrt d)^d (log en)^d n^{d/(d+2)} log n)`, so
`11 K sqrt((n+K) log N) = O( K^{3/2} (4 sqrt d)^{d/2} (log en)^{d/2} (log n)^{1/2} n^{(1/2)(1 + d/(d+2))} )`
and `(1/2)(1 + d/(d+2)) = (d+1)/(d+2)`; the logarithmic part is
`O(K^2 (4 sqrt d)^d (log en)^d n^{d/(d+2)} (log n)^2)`. The four exponents that occur are
`(d+2)/(d+3)`, `(d+1)/(d+2)`, `d/(d+2)` and `1/2`, and the first strictly dominates the other three for
every `d >= 1`, with margins `1/((d+2)(d+3))`, `(d+2)/(d+3) - d/(d+2)` and `(d+2)/(d+3) - 1/2 >= 1/6`.
Choosing `n_2(K,d)` so that the polylogarithmic factors attached to the smaller exponents are absorbed
gives part (D). `QED`

## 6. Third question: implementability. This is where the route fails

The brief expected this to be the real obstacle. It is. I state the position plainly and then say
exactly how much of it I could prove.

### 6.1 The mechanism as specified is not an algorithm

`log N = O(n^{d/(d+2)} polylog)`, so `N = exp(Theta(n^{d/(d+2)}))`. The fallback maintains one weight
per expert and computes `xi_a = sum_{e : e(X_t) = a} q_e` at every round, so a direct implementation
costs `Theta(N)` per round. Concretely, at `K = 3` and `d = 1` and `n = 10^9`, which is the smallest
horizon at which `EXPLORER.md` Section 10.1 finds the shading `sigma_n` below `0.1` and the mechanism
therefore numerically non-vacuous at all, the net has
`|Val_n| = 2001` values on `86894` cells per agent, so `log_2 N = 2.9 * 10^6` and
`N = 2^{2.9 * 10^6}`. At `d = 2` and `n = 10^9` it is `2^{1.2 * 10^{10}}`
(`<scratchpad>/round2/g1-experts-fallback/`, inline computation recorded in `COMPUTE_LOG.md`).
No implementation, no approximation of the weights by sampling, and no amount of hardware makes this
a procedure. **PA-MESP-N as specified is an information-theoretic object and the paper must not
present it as an algorithm.**

This is not a defect that better engineering removes. It is the standard position of EXP4
(Auer, Cesa-Bianchi, Freund and Schapire, SIAM J. Comput. 32(1):48 to 77, 2002, Theorem 7.1, regret
`O(sqrt(K T ln N))`, running time linear in `N` per round), and the reason the contextual bandit
literature exists.

### 6.2 What computational problem the fallback actually poses

**Proposition E1 (the comparator class is the sleeping-experts ranking class).** Let
`A := { (j,c) : j in [K], c a cell of G_n }`, so `|A| = K q^d`. At every round exactly `K` elements of
`A` are *awake*, namely `(j, C_j(t))` for `j in [K]`, one per agent, and which ones are awake is
determined by the arrival path alone. For a total order `sigma` of `A` let `rho_sigma` be the rule
"select the awake action that `sigma` ranks highest". Then
`{ rho_sigma : sigma a total order of A } = { pi_f : f : A -> R }`, and `Pi_n` of Section 2.4 is the
restriction of this class to `f` taking values in `Val_n`.

*Proof.* Given `f`, the induced order (break ties by index) has `rho_sigma = pi_f`. Given `sigma`,
put `f(a) := |A| - rank_sigma(a)`; then `pi_f` picks the awake action of largest `f`, which is the one
`sigma` ranks highest. `QED`

So the fallback is a **sleeping bandit problem with adversarial availability, measured against the
best-ordering benchmark** of Kleinberg, Niculescu-Mizil and Sharma (COLT 2008; Machine Learning 80,
2010). That is the exact identification, and it is what makes the literature applicable.

### 6.3 What the literature says, from primary sources

All four facts below were read on 18 September 2026; URLs in Section 11.

1. **The benchmark is the one that is known to be hard.** Kleinberg, Niculescu-Mizil and Sharma
   introduce the best-ordering benchmark for sleeping experts and bandits and give algorithms with
   near-optimal regret; per the statement of the problem in Kanade and Steinke, they give a
   computationally efficient no-regret algorithm **when the payoffs are stochastic**, and Kanade,
   Steinke and Thaler (2009) give one **when the availability is stochastic**. The case this
   mechanism is in, adversarial payoffs and adversarial availability, is the one they left open.
2. **That open case is hard.** Kanade and Steinke, "Learning Hurdles for Sleeping Experts",
   ITCS 2012 (journal version ACM Trans. Comput. Theory, 2013), Theorem 1: *if there exists a
   computationally efficient no-regret algorithm for the sleeping experts problem (with respect to
   ranking strategies), then the class of polynomial size DNFs is PAC-learnable under arbitrary
   distributions.* Their setting is full information and an oblivious adversary, so the bandit case
   and the adaptive case are at least as hard (their words: "Since our results show computational
   difficulties in designing efficient no-regret algorithms, they are equally applicable to the more
   challenging case of an adaptive adversary"). Their availability sets have size at most `k+1` and
   the bounded case reduces to agnostic learning of monotone disjunctions over examples of Hamming
   weight at most `k`; their Proposition 9 says proper agnostic learning of that is NP-hard for every
   `k >= 2`, that is already for three available actions.
3. **An optimization oracle does not rescue it generically.** Hazan and Koren, "The Computational
   Power of Optimization in Online Learning", STOC 2016 (arXiv:1504.02089, v1 8 April 2015, v4
   27 January 2016), give an online algorithm attaining vanishing regret with respect to `N` experts
   in `~O(sqrt N)` oracle-model computation time **and a matching lower bound showing this cannot be
   improved in the oracle model**. Their result is about prediction with expert advice with an
   optimization oracle; it does not mention contextual bandits, and I do not claim it does. Its
   bearing here is exactly this: even granting a free oracle that returns the leading expert in
   hindsight, a *generic* reduction needs `~sqrt(N) = 2^{1.4 * 10^6}` oracle calls at the parameters
   of Section 6.1, so any efficient implementation must exploit the structure of `Pi_n` and cannot be
   a black-box reduction.
4. **The efficient adversarial contextual bandit results all buy efficiency with an assumption this
   mechanism does not have.** Oracle-efficient algorithms for adversarial contextual bandits are
   known under i.i.d. or transductive contexts (Rakhlin and Sridharan, ICML 2016; Syrgkanis,
   Krishnamurthy and Schapire, ICML 2016; Syrgkanis, Luo, Krishnamurthy and Schapire, NeurIPS 2016),
   at regret `T^{3/4}` and then `T^{2/3}` rather than `sqrt T`; and Agarwal, Hsu, Kale, Langford, Li
   and Schapire (ICML 2014) is efficient with i.i.d. contexts **and** i.i.d. rewards. I did not verify
   these four against primary sources because nothing below depends on them; they are recorded as
   leads, not as facts, and anyone using them must check them. Two remarks on them, which do not need
   verification. First, i.i.d. contexts is exactly the hypothesis `CG-MESP` and `PA-MESP-N` are proud
   of not needing ((A3); `EXPLORER.md` Section 0.1), so buying efficiency that way gives back the one
   thing the continuous private mechanism has over `thm:grid-etc`. Second, and more usefully, a
   `T^{2/3}`-type fallback regret would still close: balancing `(K log N)^{1/3} n^{2/3} + eps n` with
   `log N = Theta(K (L/eps)^d)` gives `eps = Theta(n^{-1/(d+3)})` and cost `Theta(n^{(d+2)/(d+3)})`,
   exactly the pricing exponent, so the mechanism's rate would survive an oracle-efficient fallback
   with the degraded exponent. That is the single most useful consequence of this section for anyone
   continuing the work.

### 6.4 What is proved hard here, what is not, and the open problem

**Proposition E2 (the hardness of item 2 transfers, when `K` grows).** Let an instance of the
`(k+1)`-sleeping experts problem of Kanade and Steinke Figure 2 be given: actions
`A' = {perp} union [M]`, availability `S_t = {perp} union { i : x^t_i = 1 }` with `||x^t||_H <= k`, payoffs
`p_t` in `[0,1]`, both chosen obliviously. Then there is an instance of the fallback problem with
`K = k+1` agents, `d = 1`, `M+1` cells per agent, capacities `M_j = 1`, intrinsic means `mu_j = 0`,
an arrival path satisfying (A3), and agent behaviours in `B^ctx+`, such that any algorithm for the
fallback problem whose regret against the ranking benchmark is `R` yields an algorithm for the
sleeping experts instance whose regret against the best ordering is at most `R`.

*Proof.* Agent `0` has a constant context (one cell) and delivers `p_t(perp)` when selected. Agents
`1,...,k` have context space with `M+1` cells, the extra one being a dummy. Enumerate
`{ i : x^t_i = 1 } = { i_1, ..., i_w }`, `w <= k`; put agent `r`'s context in cell `i_r` for `r <= w`
and in the dummy cell for `r > w`, and let agent `r` deliver `p_t(i_r)` at a literal cell and `0` at
the dummy cell. The arrival path is a function of `(x^t)` alone, hence exogenous, and every delivery
is a nonanticipating function of `t`, hence in `B^ctx+`; `M_j = 1` makes every delivery feasible and
`mu_j = 0` makes honesty vacuous. Map the algorithm's choice back: agent `0` to `perp`, agent `r` at a
literal cell to that literal, agent `r` at the dummy cell to `perp` (whose payoff `p_t(perp) >= 0` is at
least the dummy's `0`). This gives `ALG_sleeping >= ALG_fallback`. For the benchmark, embed any
ranking `sigma` of `A'` by `f_0(the single cell) := score_sigma(perp)`, `f_r(i) := score_sigma(i)` for
every `r` and every literal cell `i`, and `f_r(dummy) := -1`; then `pi_f` selects the agent holding the
`sigma`-highest available literal, or agent `0`, matching `rho_sigma`, so
`OPT_fallback >= OPT_sleeping`. Subtracting gives
`R_sleeping = OPT_sleeping - ALG_sleeping <= OPT_fallback - ALG_fallback = R`. `QED`

**Corollary E3.** If for every `K` there is an efficient algorithm with regret `O(poly * T^{1-delta})`
against the ranking benchmark for the fallback problem with `K` agents and adversarial payoffs, then
polynomial size DNFs are PAC-learnable under arbitrary distributions. **This is a statement about `K`
growing.** For fixed `K`, Proposition E2 plus Kanade and Steinke's Lemma 8 gives only efficient
online, hence batch, agnostic learning of monotone disjunctions over examples of Hamming weight at
most `K-1`, and I do not know whether that is hard. Their Proposition 9 shows the *proper* version is
NP-hard for `K >= 3`, which does not settle the improper version, and improper additive
approximation for bounded-arity problems of this shape is often possible. **So: for `K` growing the
route is computationally hopeless; for fixed `K`, which is the regime of this paper, it is open.**

**And the caveat that matters most, stated against my own reduction.** Proposition E2 constructs an
instance with **time-varying** payoffs, and the ranking benchmark it invokes is measured on those
realised payoffs. Lemma N2 does not need that benchmark. It needs only the **floor** benchmark: the
comparator's credited value at round `t` is `g_{e(X_t)}(x)` for a floor vector `g` that is **constant
in time**, and in both of the fallback's jobs (Section 3.2) the floors are `M_j` or `mu_h`, fixed
functions of the instance. For a benchmark defined by time-invariant floors the offline optimisation
is a sort, not a linear ordering problem, and Kanade and Steinke's reduction does not apply. So
Proposition E2 does **not** show the problem PA-MESP-N poses is hard; it shows that the obvious
superset of it is hard. I record this explicitly because the temptation to over-read the reduction is
strong and I nearly did.

**The open problem, stated exactly.** Is there an algorithm, polynomial in `K`, `J` and `T`, for the
following? There are `K` agents and `J` cells; at round `t` agent `j` occupies a cell `c_j(t)` chosen
by an oblivious adversary; there are unknown floors `g_{j,c} in [0,1]`; when the algorithm selects
agent `j` at round `t` the agent delivers an adaptively chosen `m_t in [g_{j,c_j(t)}, 1]` and the
algorithm observes `Bernoulli(m_t)`; the requirement is
`E sum_t m_t >= sum_t max_j g_{j, c_j(t)} - o(T)` with an explicit `poly(K,J) T^{1-delta}` remainder.
Note the two extremes: if the adversary always delivers exactly the floor, this is a stochastic
sleeping bandit and Kleinberg, Niculescu-Mizil and Sharma solve it efficiently; if the benchmark were
measured on the realised deliveries instead of the floors it is the hard case of item 2. The
mechanism needs precisely the intermediate problem, where the adversary may over-deliver but is not
credited for it. **I did not solve it and I do not conjecture either way. It is the one place where
the route can still be saved, and it is a clean, self-contained question that does not mention this
paper's model.**

### 6.5 What this costs the paper, said plainly

I would not present PA-MESP-N as a mechanism. Three consequences, in order of how much they matter.

1. **The theorem must carry the words "not efficiently implementable" in its own neighbourhood**, not
   in a footnote or a "future work" line. `COMMON.md` rule 8 and the brief are both explicit, and a
   reviewer who discovers `N = 2^{2.9 * 10^6}` after being told the mechanism achieves
   `n^{(d+2)/(d+3)}` will not be generous. The manuscript's other constructions (MESP, Grid-UCB,
   Grid-ETC, CG-MESP) are all polynomial time, so the contrast is sharp and must be owned.
2. **The correct framing is a separation, and it is a real contribution in that framing.** Theorem G1
   says the exponential dependence on `K` in `(D+2)/(D+3)` with `D = Kd` is **not
   information-theoretically necessary**: with unbounded computation the per-agent exponent
   `(d+2)/(d+3)` is achievable for every `K`, under strictly weaker hypotheses than the manuscript's
   public contextual theorem (no i.i.d. arrivals, no top-set condition, no null boundary). Read that
   way it converts the worst remaining weakness of the contextual half from "our rate is bad" into
   "the bad rate is a computational artefact, and here is the exact open problem that would remove
   it". That is a defensible AAMAS contribution and it is honest.
3. **Keep CG-MESP as the constructive result.** `EXPLORER.md` Theorem 1 is efficient and gives
   `n^{(D+2)/(D+3)}`. My recommendation is: CG-MESP in the body; Theorem G1 as one paragraph plus an
   appendix remark stating the separation, the non-implementability and the open problem of
   Section 6.4; and no claim anywhere that the per-agent exponent is achieved by an algorithm.

## 7. Fourth question: the strategic hazard

The brief asks whether an experts algorithm, which updates on rewards by construction, collides with
`c4-safe-partitions/REPORT.md`, which proves that partition and selection rules adapting on rewards
break the guarantees by a linear margin. The short answer is no, for a reason that is worth being
precise about, and the hazard lands on a different construction which I therefore did not use.

### 7.1 What the c4 witnesses break, and why an experts algorithm is out of their scope

The c4 failures are all of one shape. A rule makes an **irreversible decision from rewards** (freeze
a leaf, inherit an ancestor's elimination verdict, split on a selection count) and the *analysis* of
that rule needs the cell epoch to be a fixed-mean instance so that the decision is sound. The
mechanism of the failure, in c4's own words for its headline witness Theorem 4, is that "freezing is
a test that a cell is decided, and such a test is sound only if the threshold dominates the
within-cell variation of the *delivered* means", and the delivered means need not be smooth or even
fixed, because the agents choose them.

An experts algorithm makes no such test. Lemma N2 is proved for arbitrary reactive behaviour of every
agent, and its proof uses the reward process only through `r_{a,t} = E[Y_t | F_{t-1}, I_t = a]`, a
quantity the agent is free to choose after seeing everything. There is no counterfactual, no fixed
mean, no cell-average, and no decision that has to be correct. This is already true of the
manuscript's EXP3 fallback (`sections/appendix_private.tex`,
`lem:selected-reactive-exp3`: "Other agents may choose arbitrary feasible nonanticipating targets
after selection"), and moving from `K` arms to a policy net changes nothing in that respect: the
estimate `hatY_{e(X_t)}` is the same importance-weighted observation of the *selected* arm.

There is one reward-dependent routing decision in PA-MESP-N that is new relative to CG-MESP, namely
"if `W_t` is switched, hand round `t` to `F_{W_t}`". It is reward dependent, and I checked the three
places where that could bite. (i) It does not touch the partition: the grid is static, so c4's (R1)
holds trivially and its (R4) holds because the total elicitation is `O(n^{(d+2)/(d+3)}) = o(n)` and the
mesh `h'_n -> 0`. (ii) It does not touch the elicitation schedule, which reads only counters and
contexts; this is the hypothesis the bid-domination coupling needs (Lemma N3(a)) and the one c4's
converse says cannot be relaxed. (iii) It does make the two coupled executions differ in which rounds
are fallback rounds, which is precisely why Step 4 of Section 5.3 is written per round and compares
the fallback set `F` with the baseline's win set rather than comparing two phases; the containment
`F subset {baseline wins of i}` is what makes that legitimate, and it comes from winner inclusion,
which is pathwise.

c4's (R2), "label-local fresh statistics", is **violated** by PA-MESP-N, which reads all `K` agents'
statistics and a global per-agent monitor. That is not a defect: (R1) to (R4) are the conditions for
the contextual SAMF axioms (monotonicity, FATA, sharp adaptivity), and PA-MESP-N, like CG-MESP and
like the manuscript's MESP, claims none of them. Section 9 item 3 repeats this warning because it is
easy to lose.

### 7.2 The construction the hazard does kill, which I found and rejected

While looking for an efficient fallback I found one, and it is instructive that it fails for exactly
the c4 reason.

**The rejected mechanism.** On a switch of agent `j`, at each subsequent round with `W_t = j`, select
`argmax_{a != j} beta_{a, C_a(t)}`, the best remaining elicited bidder. This is deterministic, costs
`O(K)` per round, uses only `d`-dimensional per-agent statistics, and **it is sufficient for
deterrence**: the promoted agent `a` plays `S^*` and delivers `M_a(x_{a,t})`, and the same three-line
chain that proves Lemma N3(c) gives `M_a(x_{a,t}) >= tau_t - O(s_n + rho_n)` at every round, so the
per-round shortfall is `O(s_n + rho_n)` and `n(s_n + rho_n) = O(n^{(d+2)/(d+3)} log n)` is inside the
budget. So part (A) closes efficiently and in the per-agent dimension.

**Why it is dead.** Part (C) is the hypothesis where every agent behaves arbitrarily. There the bids
`beta_{a,c}` carry no information: every agent may underbid, so `argmax_a beta_{a,c_a(t)}` need not be
an honest agent and need not deliver anything. Worse, an honest agent may fail the monitor
legitimately, because honesty only bounds its delivery from below by `mu_h` and the price may exceed
`mu_h`, so a promotion rule can switch and then permanently demote every honest agent. That is
`EXPLORER.md` Section 9's reason for not taking the suspension route, it is the manuscript's own
reason for restarting EXP3 rather than removing a suspect
(`sections/appendix_private.tex`, closing paragraph: "after a statistically triggered switch it keeps
every honest agent available as a comparator"), and it is the c4 lesson in its purest form: a
reward-triggered irreversible demotion is a test that an agent is bad, and the test is unsound because
the delivered maps are chosen by the agents. I record it because it is a genuine trap: it is
efficient, it is `d`-dimensional, it makes part (A) work, and it silently destroys part (C).

### 7.3 Incentive properties of the fallback itself

Three checks, all of which the EXP3 fallback already had and which survive the move to EXP4.

1. **Manipulating the weights.** A deviator can change which experts look good, by its own deliveries.
   It gains nothing: Lemma N2 holds for arbitrary reactive behaviour of every arm including the
   deviator, and the conservation step of Step 4 turns any extra selection of the deviator into an
   extra obligation to deliver `V_i(X_t)`. Being selected more is not a gain when selection is priced
   by delivery.
2. **The exploration floor.** Explicit exploration gives every agent probability at least
   `gamma_k/K` at every fallback round, so an agent that delivers `0` still collects
   `Theta(gamma_k H)` pulls worth `1 + mu_i` each. This is a real gain to a deviator and it is exactly
   the term `e_1fb` pays for; `separation/REPORT.md` Section 2.7 item 4 makes the same point about
   Grid-EXP3 and the same sentence must accompany any use of this result. Section 8 measures this
   channel and finds it is the dominant one.
3. **Triggering the fallback deliberately.** This is what part (A) is about and Step 4 of
   Section 5.3 is the answer: the deviator's fallback utility is bounded by the baseline's payment at
   the same rounds plus `e_net + e_1fb`. The localisation of Section 2.3 is what makes "the same
   rounds" the right set.

## 8. Numerical falsification attempt against my own claims

Fully synthetic simulation, run to look for a violated inequality. It is **not** evidence that
Theorem G1 is true. Code, seeds and raw output: `<scratchpad>/round2/g1-experts-fallback/`
(`exponents.py`, `exp4check.py`, `exp4check2.py`, `scaling.py`). All runs are login-node runs of
seconds to a minute; no Slurm job was needed and none was submitted, so there is no job id.
Constraints are recorded in `COMPUTE_LOG.md`.

**8.0 What cannot be tested, said first.** At the mechanism's honest parameters the shading
`sigma_n = 3 s_n + rho_n` exceeds `1` at every simulable horizon, so `tau_t = 0` everywhere and the
mechanism prices at zero; this is `EXPLORER.md` Section 10.1's wall and it is worse here only in that
the net adds a second vacuous term (`e_1fb` exceeds `n` until `n` is astronomical, since
`log N ~ n^{d/(d+2)}`). At `K = 3`, `T = 2048` and the toy net of Section 8.2, `R^dbl_{K,N}(T) = 2423`
against `T = 2048`, so **every bound tested below is vacuous at the tested horizon and only the
inequalities and the scaling can be examined, not the rates or the constants.** I therefore test the
lemmas at hand-chosen parameters, and I report raw gaps rather than only "bound held".

**8.1 Exponent arithmetic (`exponents.py`).** The table of Section 4.4 is machine-computed in exact
rational arithmetic. `(d+1)/(d+2) < (d+2)/(d+3)` with difference exactly `1/((d+2)(d+3))`, verified for
`d = 0,...,11`. The "PA with net fallback" column is constant in `K`, equal to `(d+2)/(d+3)`, and is
strictly below the `CG-MESP` column in every row of the table.

**8.2 Lemma N2 and the part (C) comparator (`exp4check2.py`).** `K = 3`, `J = 3` cells,
`|Val| = 2`, so the net is enumerated exactly with `N = 2^{K J} = 512` experts, `T = 2048`, contexts
drawn uniformly over the `J^K` cell profiles, 5 seeds per configuration. Agent `0` is honest with
floors `g_0 = (0, 0.5, 1)` and delivers exactly its floor; agents `1` and `2` have floor `0` and are
reactive, in four modes: `zero` (always deliver `0`), `bait` with `B in {64, 256}` (deliver `1` for the
first `B` selections, then `0` forever), and `mimic` (deliver just under the honest agent's floor for
`B` selections, then `0`). Result: **no violation of Lemma N2 in any run**. Raw regret
`sum_t b(X_t) - sum_t Y_t`, over 5 seeds: `zero` mean `194.6` max `215.5`; `bait B=64` mean `99.1`;
`bait B=256` mean `-158.2` (the algorithm beats the benchmark, because over-delivery is free reward,
which is the asymmetry Section 6.4 rests on); `mimic` mean `75.9`. All are far below the stated
allowance `2 eps T + R^dbl = 4471`, and all are below `sqrt(K T log N) = 165` times a small constant.

**8.3 The deterrence conservation inequality of Step 4 (`exp4check2.py`).** Same net. Agents `1, 2`
play `S^*` with capacities `M_1 = (0.3, 0.9, 0.5)`, `M_2 = (0.8, 0.2, 0.6)` on the three cells, so
`V_i(X)` varies over the rounds; agent `0` is the deviator, in modes `zero`, `bait B=128`, `half`
(always deliver `0.5`). The quantity tested is
`Abar_i >= sum_{t in Q_i} V_i(X_t) - 2 eps H - R^dbl`. **No violation in any of the nine runs.** The
raw gap `sum_{t in Q_i} V_i - Abar_i`, which is the deviator's total gain over the comparator, is
`293.5` to `318.7` for `zero`, `205.0` to `227.7` for `bait`, and `151.6` to `184.9` for `half`, against
an allowance of `4471`.

**8.4 The dominant channel and its scaling (`scaling.py`).** The `zero` deviator receives
`Q_i = 444` of `2048` fallback pulls while delivering nothing; this is the explicit-exploration floor
of Section 7.3 item 2 and it is the term that has to scale like `sqrt(K H log N)`. Measured mean gap
over 4 seeds:

| `T` | mean gap | gap / `sqrt(K T log N)` | ratio to previous `T` |
|:-|:-|:-|:-|
| 1024 | 188.2 | 1.359 | |
| 2048 | 307.7 | 1.572 | 1.635 |
| 4096 | 492.9 | 1.780 | 1.602 |
| 8192 | 749.1 | 1.913 | 1.520 |
| 16384 | 1129.0 | 2.039 | 1.507 |

The normalised column stays well below the doubling constant `3(2+sqrt 2) = 10.243` of
`separation/REPORT.md` Lemma B, and the horizon-doubling ratio falls monotonically toward
`sqrt 2 = 1.414`, which is the scaling `R^dbl_{K,N}` predicts and no other term predicts. This is the
same signature `EXPLORER.md` Section 10.3 finding 5 reports for its own `e_mon` channel.

**8.5 What none of this tests.** The full PA-MESP-N (I simulated the fallback in isolation, not the
elicitation, pricing, monitoring and coupling); the rates; the constants; any horizon at which the
honest parameters are non-vacuous; the case where the good events fail; the localisation of
Section 2.3 (which is an argument about two coupled executions and I did not build the coupling in
code); and the reduction of Section 6.4, which has no probabilistic content.

## 9. Defects and corrections found in the documents I was sent

**G1-D1 (P1, against `EXPLORER.md` Section 8.1).** The `PA-MESP` fallback is global ("on the first
switch of any agent, run Grid-EXP3 ... for the remaining rounds"). With a global fallback the
deterrence accounting fails by a linear margin for a reason independent of the fallback's comparator
class: the deviator collects fallback pulls at rounds it would not have won, where the baseline pays
it zero and the fallback pays it `1 + mu_i - (comparator) >= 0`. The repair is the localisation of
Section 2.3. This does not affect any theorem in `EXPLORER.md`, because `PA-MESP` carries none; it
affects the claim in Section 8.3 that the only missing piece is the comparator's dimension, since with
a global fallback the mechanism does not close even with a perfect comparator. Minimal repair: one
sentence in Section 8.1.

**G1-D2 (P2, against `EXPLORER.md` Section 8.3).** The derivation is correct under an unstated
hypothesis, "the fallback's comparator is a value constant on a region", and the section's conclusion
("the reason is not removable") is stronger than the derivation supports. Section 8.3's own closing
sentence in Section 11 item 4 concedes the hypothesis ("it assumes the fallback's only instrument is a
comparator value on a region"), so this is a wording defect in Section 8.3 and Section 0.5 rather than
an error. Minimal repair: add the hypothesis to the statement in Sections 0.5 and 8.3, and change "is
not removable" to "is not removable by any fallback whose comparator is constant on a region".

**G1-D3 (P3, against `EXPLORER.md` Section 8.6).** The sketch's rate `Theta(n^{(d+1)/(d+2)})` for the
fallback is right, and its three listed gaps are the right three, but it lists the wrong one as the
hard one. "An argument that the expert net can be built without knowing `L` or `nu`" is two lines
(Lemma N1(b), using the standing hypothesis (A2)); "a selected-reactive version of EXP4" is a page
(Lemma N2); and "the per-round cost is exponential" is the one that does not have a proof in either
direction (Section 6.4). The sketch also does not notice that the comparator has to exclude the
deviator, which needs the class to contain `K` different floor vectors rather than one.

**G1-D4 (P3, against `separation/REPORT.md` Section 2.7 item 7 and `EXPLORER.md` Lemma 7).** Both
require the epoch lengths to be deterministic or `F_0`-measurable, and both flag it. Lemma N2's proof
shows the requirement can be replaced by predictability of the indicator "this round belongs to this
instance and this epoch", which is weaker. I have not checked what else in those reports uses the
stronger form, so this is offered as a lead and not as a correction.

## 10. What I did not do, and the step I consider least secure

**Not done.**

1. **No efficient implementation, and no proof that none exists.** Section 6.4 states the open
   problem. This is the honest headline: the route is not closed, it is moved from a rate question to
   a complexity question.
2. **No lower bound.** Nothing here shows `(d+2)/(d+3)` is necessary, and nothing shows the fallback's
   `(d+1)/(d+2)` is necessary.
3. **No monotonicity, FATA or sharp adaptivity.** PA-MESP-N is a private-information mechanism and
   claims only the three properties of Theorem G1. It violates c4's (R2) (Section 7.1) and no SAMF
   axiom should be attributed to it.
4. **I did not reprove the imported price lemmas.** Lemma N3 is `EXPLORER.md` Lemmas 3, 4, 5, 8, 9 in
   `PA-MESP` form. `EXPLORER.md` Section 8.2 asserts they transfer with the same proofs and
   `PROVER2.md` Section 12 reports checking the `CG-MESP` forms. I checked the inequality chains and
   the shading arithmetic; I did not redo the concentration arguments, and Lemma N3 is therefore an
   assumption of this report as much as a lemma of it.
5. **No anytime version, no non-Lipschitz capacities, no reward-reactive arrivals.** All three are
   excluded exactly as in `EXPLORER.md` Section 7.5.
6. **No simulation of the whole mechanism**, only of the fallback (Section 8.5).
7. **I did not verify the four oracle-efficient contextual bandit references of Section 6.3 item 4
   against primary sources.** Nothing in this report depends on them and they are recorded as leads.

**Least secure step, in decreasing order of my own doubt.**

1. **Step 4 of Section 5.3, the composition of Lemma N2 with the coupled per-round accounting.** This
   is where four things interact at once: the conditional expectation in Lemma N2 is over the fallback
   instance's own randomness; the set `F` is random and determined by the deviating execution; the
   containment `F subset {baseline wins of i}` is pathwise but is used inside an expectation; and the
   good events `G` and `H` are used on both sides. `PROVER2.md` defect D2 is exactly a failure of this
   kind in `EXPLORER.md` Section 7.1 (an event assumed measurable with respect to a conditioning field
   when it is not), and I have written Step 4 to avoid the analogous error by keeping every inequality
   per round and pathwise before taking a single expectation, but **I have not verified that
   `1_{G cap H}` can be moved inside the conditional expectation of Lemma N2 in the way Step 4 needs**,
   and the repair `PROVER2.md` suggests (replace the global event by its per-instance component) is
   less obviously available here, because the good elicitation event `G` involves pairs `(j,c)` whose
   elicitation may still be running when a fallback instance is already active. **This is the first
   thing an adversary should attack.** If it fails, the fix is likely to be a per-instance good event
   and an `O(n^{-2})` charge, as in `PROVER2.md` D2, but I did not write it.
2. **Lemma N2's predictability hypothesis**, that `psi_t` and the epoch indicator are
   `F_{t-1}`-measurable. This holds only under Convention F-A, which puts the whole arrival path in
   `F_0`. `EXPLORER.md` Section 11 item 2 and `PROVER2.md` Section 14 both name the same step as their
   least secure one and the objection transfers verbatim; (A3) licenses it and
   `ADVERSARY.md` Section 7.1 shows the finite theorem is false without it.
3. **Proposition E1's identification of `Pi_n` with ranking policies**, which I believe, and
   **Proposition E2's embedding**, where the mapping of a dummy-cell selection back to `perp` and the
   claim `OPT_fallback >= OPT_sleeping` are the two steps I would re-check. Nothing in Theorem G1
   depends on either.
4. **Lemma N3, which I imported rather than proved** (item 4 above).

**One sentence of self-assessment.** I believe the information-theoretic half of this route is right
and the implementability half is genuinely open, and if one thing here is wrong I expect it to be
Step 4 of Section 5.3 rather than anything about the net or the counting; I am not claiming the result
is correct.

## 11. Primary sources consulted, with URL and date read

All read 18 September 2026.

1. P. Auer, N. Cesa-Bianchi, Y. Freund, R. E. Schapire, "The Nonstochastic Multiarmed Bandit Problem",
   SIAM Journal on Computing 32(1):48 to 77, 2002. Read the author-hosted full text at
   `https://cesa-bianchi.di.unimi.it/Pubblicazioni/J18.pdf`. Verified: the header
   ("SIAM J. COMPUT. Vol. 32, No. 1, pp. 48 to 77", 2002); Section 7 introduces Exp4; Theorem 7.1
   reads "For any `K, T > 0`, for any `gamma in (0,1]`, and for any family of experts which includes
   the uniform expert, `Gmax - E[G_Exp4] <= (e-1) gamma Gmax + K ln N / gamma`"; and the introduction
   states the resulting bound as `O(sqrt(K T ln N))`. **Used for**: the fact that the `sqrt(K T log N)`
   rate for experts over a policy set is standard prior art and is not novel here. **Not used for**:
   Lemma N2, which is proved from the potential argument and is not a corollary of Theorem 7.1 (it
   needs a floor vector, a per-round comparator value, doubling epochs and a predictable round set,
   none of which are in that theorem).
2. R. Kleinberg, A. Niculescu-Mizil, Y. Sharma, "Regret Bounds for Sleeping Experts and Bandits",
   COLT 2008; journal version Machine Learning 80(2 to 3), 2010. Read
   `https://mlanthology.org/colt/2008/kleinberg2008colt-regret/` (title, authors, venue, year,
   abstract) and `https://link.springer.com/article/10.1007/s10994-010-5178-7` (redirected to a login
   wall, so the journal version's text was not read). **Used for**: the name and definition of the
   best-ordering benchmark, and the fact that both full-information and bandit, stochastic and
   adversarial, settings are treated there.
3. V. Kanade, T. Steinke, "Learning Hurdles for Sleeping Experts", ITCS 2012 (dated 1 September 2012
   on the manuscript); journal version ACM Transactions on Computation Theory, 2013. Read the full
   text at `http://www.cs.ox.ac.uk/people/varun.kanade/docs/learning-KS12.pdf`. Verified verbatim:
   the abstract ("In this paper, both the payoff function and the availability of actions is
   adversarial. Kleinberg et al. (2008) gave a computationally efficient no-regret algorithm in the
   setting where payoffs are stochastic. Kanade et al. (2009) gave an efficient no-regret algorithm in
   the setting where action availability is stochastic. However, the question of whether there exists
   a computationally efficient no-regret algorithm in the adversarial setting was posed as an open
   problem by Kleinberg et al. (2008). We show that such an algorithm would imply an algorithm for PAC
   learning DNF"); Theorem 1; the oblivious-adversary remark and its transfer to adaptive adversaries;
   Figure 2 and Lemma 8 for the `(k+1)`-sleeping experts reduction with `S^t = {perp} union {i : x^t_i =
   1}`; Proposition 9 (proper agnostic learning of MON-DISJ over `X_k` is not efficient for `k >= 2`
   unless `NP = RP`). **Used for**: Section 6.3 item 2, Corollary E3 and its `K`-growing caveat.
   The ACM DOI page `https://dl.acm.org/doi/abs/10.1145/2505983` returned HTTP 403 and was not read.
4. E. Hazan, T. Koren, "The Computational Power of Optimization in Online Learning", STOC 2016.
   Read the arXiv abstract page `https://arxiv.org/abs/1504.02089` (v1 8 April 2015, v4 27 January
   2016). Verified verbatim from the abstract: a novel online algorithm attaining vanishing regret
   with respect to `N` experts in total `~O(sqrt N)` computation time, "and a lower bound showing that
   this running time cannot be improved (up to log factors) in the oracle model". **Used for**:
   Section 6.3 item 3, and only in the precise form stated there. **Explicitly not used for**: any
   claim about contextual bandits; the abstract does not mention them, and the widespread paraphrase
   "oracle-efficient methods do not exist for adversarial contextual bandits" is not what the paper's
   abstract says.

No other external result is relied on anywhere in this report. Every lemma in Sections 4 and 5 is
either proved here, imported from another report in this project with the import flagged, or, in the
case of Lemma N3, imported and flagged as an assumption.
