# Adversarial pass on three unreviewed results (18 September 2026)

Role: adversary. The goal was to break the three results, not to confirm them. A counterexample is a
success. Nothing outside this file and the scratchpad was written; no canonical file was read other
than read-only. No Unicode em dash and no LaTeX triple hyphen appears here.

Targets:

- **Result 1**, separation theorem: `audit/round2/B/theorems/separation/REPORT.md` Part 1.
- **Result 2**, monitor lower bound: `audit/round2/B/theorems/f1-continuous-private/SCEPTIC.md`
  Section 4 (Theorem S1) and Section 5(c).
- **Result 3**, Grid-EXP3 robustness: `audit/round2/B/theorems/separation/REPORT.md` Part 2.

Scratch scripts: `<scratchpad>/round2/adversary/` (`lastactive.py`, `rr.py`, `const.py`,
`const2.py`, `converse.py`). Login node only, seconds each, no Slurm job submitted, so there is no job id to log.

## Verdict table

| # | Target | Outcome of the attack |
|:-|:-|:-|
| 1 | Theorem 1 and 1' as *stated* (with `rho`-responsiveness) | **Not broken.** Proofs re-checked line by line and are correct. |
| 2 | The *headline* claim of Part 1 and its summary-table row 1 (no responsiveness clause) | **Broken.** Explicit mechanism inside Definition 1, with a genuine scalar price and the kernel applied unconditionally at every pull, that attains `mu_H^* n - O(n^{2/3})`. Section 1.2 below. |
| 3 | Section 1.7 item 4, "cumulative monitors are outside the class by construction" | **Broken.** `MESP`'s monitor is inside Definition 1 as literally written. The kernel formulation restricts nothing. Section 1.3. |
| 4 | The recorded open problem (rules protecting the last active agent) | **Closed against the mechanism.** Explicit two-instance counterexample, both instances all honest with a Bernoulli gap, on which every such rule loses `>= 0.0248 n - 4`. Section 1.4. |
| 5 | Theorem S1 arithmetic and the claimed constant `0.293` | **The caller's correction is confirmed on the value.** `MESP`'s Stage-2 phase has planned length `n - K L_n`, not `n/2`, so the limiting coefficient is `sqrt 2 - 1 = 0.414`. `0.293` is a valid lower bound that the report states as a limit. Section 2.1. |
| 6 | Corollary S1.2 (`sqrt(J n log n)` "matching lower bound") | **Broken as a lower bound.** The proof maximises where it must minimise. Repairable only under a balanced-visits hypothesis. Section 2.2. |
| 7 | Section 5(c), the anti-concentration converse | **Gap closed**, and closed without Slud, by an elementary method-of-types bound. Slud verified against the primary source anyway. The report's claim that Berry and Esseen "would also work" is false. Section 2.3. |
| 8 | Theorem S1 class (interleaving, restarts, randomised boundaries) | Interleaving and restarts do **not** escape, and the "every pull of the phase" hypothesis is unused. Reward-independent randomised boundaries also do not escape. Path-adapted stopping rules remain genuinely open. Section 2.4. |
| 9 | Result 3, obliviousness hypothesis (H1) | **Fixable, not genuine.** An optional-skipping version of Lemma A removes (H1) entirely, with one honest caveat about what the benchmark then means. Section 3.1. |
| 10 | Result 3, doubling constant `3(2 + sqrt 2)` and Lemmas A, B, C | **Not broken.** Re-derived independently; constant and epoch count are right. Section 3.3. |

# RESULT 1. The separation theorem

## 1.1 Attack on the proofs themselves: failed

I re-derived Lemma 1, Lemma 2, Theorem 1, Theorem 1', Proposition 1, Theorem 2 and Corollary 2
independently before reading the report's proofs a second time.

- Lemma 1. The conditional exclusion probability given `(H_{t-1}, I_t = h, m)` is exactly
  `m p_1 + (1-m) p_0`; dropping either summand gives `>= kappa max{p_0,p_1}`. Correct. The bound is
  pointwise in `m`, so agent randomisation over targets is genuinely covered.
- Lemma 2. `A_{j+1} subseteq A_j cap {not excluded at sigma_j}` is right because exclusion is
  irreversible, and `sigma_j` is a stopping time, so the conditioning is legitimate.
  `E[T] = sum_j Pr(A_j)` is the standard tail sum. I could not manufacture a measurability failure:
  the only delicate point, that `{T_h(n) >= j}` is `H_{sigma_j - 1}`-measurable, holds because the
  event is decided by the selection at round `sigma_j`, which is `H_{sigma_j-1}`-measurable by
  Definition 1 step 2. The worker's own second concern is unfounded.
- Theorem 1'. `(1-kappa) K / (kappa rho)`. The numerical row `K=4, kappa=1/2, rho=1` gives exactly
  `4`, the observed `4.03` is Monte Carlo noise around an equality case, not a violation: with
  `mu = M = 1/2` and `phi(0,tau)=1` the per-pull hazard is exactly `kappa rho = 1/2`, so Lemma 2 and
  Theorem 1' hold with equality. I confirmed this is an equality case and not an error.
- Theorem 2 and Corollary 2. The block argument is correct; `kappa^k` is the right per-block
  probability and the `k-1` leftover pulls are accounted for.

No error found in any proof step of Part 1. Everything below attacks the class and the framing.

## 1.2 COUNTEREXAMPLE to the headline claim: a zero-price warm-up stays inside Definition 1

The report's own opening summary says: "Any mechanism that reacts to a single pull and excludes
irreversibly collects only `O(1)` total reward on every instance whose honest agents have a Bernoulli
gap", and summary-table row 1 repeats it without a responsiveness clause. That claim is false.

**Mechanism W.** Fix a price `tau* in (0,1)` and `L := ceil(n^{2/3})`. Kernel
`phi_i(y, tau) := 1{ y < tau }`, the PURE-SP kernel, the same for every agent, **applied
unconditionally at every pull of every active agent**, exclusion irreversible. Announced price

    tau_t := 0        for t <= n - L,
    tau_t := tau*     for t > n - L.

Allocation: symmetric UCB1 over the active set. `tau_t` is a genuine scalar announced price, it is
`H_{t-1}`-measurable (it depends only on `t`), and no clause of Definition 1 is violated: there is no
suspension of the kernel, no history-dependent switch inside `phi`, no reactivation, no protection of
any agent. Mechanism W is a single-pull-reactive exclusion mechanism in the sense of Definitions 1
and 2, *verbatim*.

It is not `rho`-responsive for any `rho > 0`, because `phi(0,0) = phi(1,0) = 1{y<0} = 0`: while the
announced price is zero, neither outcome triggers exclusion. So Theorem 1 and Theorem 1' do not
apply, and the conclusion fails badly:

- Up to round `n - L` nobody is ever excluded, whatever the pulled agent delivers, so on any instance
  of Theorem 1' (every agent honest with Bernoulli gap at least `kappa`) every one of those rounds
  delivers a conditional mean at least `kappa`, and `P(n;S) >= kappa (n - L)` **unconditionally, for
  every allocation rule and every feasible profile**. That alone refutes the `O(1)` claim: the
  mechanism collects `Omega(n)`, not a constant.
- With symmetric UCB1 as the allocation rule and profiles inside the manuscript's declared class for
  `thm:sharp-robustness` (`sections/Stochastic_SAMF_Conditions.tex` line 13, which is quantified over
  a declared class `S^K`, not over all behaviors), the warm-up collects
  `mu_H^* (n - L) - O(K sqrt(n log(en)))`, so `P(n;S) >= mu_H^* n - O(n^{2/3})` and mechanism W
  **retains the honest benchmark** in full.

The first bullet is unconditional and is the one that does the refuting; the second is the sharper
reading and inherits whatever class `thm:sharp-robustness` is proved for.

This is exactly the escape the caller asked me to look for under "exclusion that depends on the
announced price in a way the kernel formulation hides". The price channel is the hiding place: the
kernel is a fixed function of `(y, tau)`, but `tau` is an arbitrary `H_{t-1}`-measurable number, so
the mechanism turns the kernel on and off through the price without ever leaving the class.

**How much of the escape is real.** The escape is not free, and the exact price of it is worth
stating, because it is the correct form of the theorem. Extend Lemma 2 as follows.

**Lemma 1A (responsive-pull budget).** Let the mechanism be an exclusion mechanism (Definition 1),
let `h` be honest with Bernoulli gap at least `kappa`, and call a pull of `h` *responsive* if
`max{phi_h(0,tau_t), phi_h(1,tau_t)} >= rho` at that pull. Let `N_h(n)` be the number of responsive
pulls `h` receives in `n` rounds. Then `Pr(N_h(n) >= j) <= (1-kappa rho)^{j-1}` and
`E[N_h(n)] <= 1/(kappa rho)`.

*Proof.* Verbatim Lemma 2 with `sigma_j` redefined as the round of `h`'s `j`th responsive pull. The
event "the `j`th responsive pull occurs" is decided before that round's reward, `sigma_j` is a
stopping time, and Lemma 1 applies at it because responsiveness holds there by definition. `QED`

**Corollary 1A (the honest form of the separation).** For an exclusion mechanism on an instance in
which every agent is honest with Bernoulli gap at least `kappa`,

    P(n;S)  <=  (1-kappa) ( K/(kappa rho)  +  E[U_n] ) ,

where `U_n` is the number of pulls at which the kernel is *not* `rho`-responsive. Consequently, to
attain `P(n;S) >= mu_H^* n - o(n)` the mechanism must leave `(1 - o(1)) n` of its pulls
`rho`-unresponsive for every fixed `rho > 0`.

Corollary 1A contains Theorem 1' (`U_n = 0`), it is proved by the same two lines, and it is not
refuted by mechanism W: W has `E[U_n] = n - L`, and indeed collects about `mu_H^* n`. It also kills
the obvious repair of mechanism W: a mechanism that audits at a *density* `d` (a `rho`-responsive
kernel at a `d` fraction of pulls, randomly placed) has `E[N_h] <= 1/(kappa rho)` responsive pulls per
agent regardless of `d`, hence `E[T_h] <= 1/(d kappa rho)`, hence total reward `O(K/(d kappa rho))`.
Keeping a constant fraction of `mu_H^* n` therefore forces `d = O(1/n)`, that is `O(1)` responsive
pulls *in total over the whole run*. That is the sharp and defensible statement, and I recommend the
paper state Corollary 1A rather than Theorem 1'.

**Severity.** P1 against the report's summary and against any sentence in the paper of the form
"single-pull reaction loses the benchmark". The *theorem* is untouched; the *claim* is false.

## 1.3 REFUTATION of Section 1.7 item 4: cumulative monitors are inside Definition 1

Section 1.7 item 4 asserts that `MESP`'s monitor and Braverman et al. Mechanism 2 are outside the
class "by construction", because they read a running sum rather than `Y_t`. That is false as
Definition 1 is written.

Nothing in Definition 1 restricts the *information content* of `tau_t`: it is any
`H_{t-1}`-measurable element of `[0,1]` (step 1), and the agents already observe all of `H_{t-1}`
(step 3), so nothing is hidden from anybody by the construction below.

The set of possible pasts `(t, (I_s, Y_s)_{s<t})` is countable. Fix an injection `e` of that
countable set into `[0,1]`; `e` is measurable, and `e^{-1}` is measurable on the countable image
`e(S)`. Put `tau_t := e(t, (I_s,Y_s)_{s<t})` and

    phi_i(y, tau) := 1{ Z_{r-1}(e^{-1}(tau)) + y  <  r(e^{-1}(tau)) * p  -  b_n( r(e^{-1}(tau)) ) }   for tau in e(S),
    phi_i(y, tau) := 0                                                                                 otherwise,

where `r` is the pulled agent's pull index, `Z_{r-1}` its running reward sum and `p` the real price,
all recovered from the decoded past. `phi_i` is Borel measurable because `e(S)` is countable. This
mechanism is an exclusion mechanism in the sense of Definition 1, with the kernel applied
unconditionally at every pull, and it *is* `MESP`'s cumulative monitor.

So Definition 1 imposes no restriction whatsoever beyond irreversibility: any exclusion rule whose
per-pull exclusion probability is measurable with respect to `(H_{t-1}, Y_t)` is in the class.
Inspection of Lemma 1 confirms this from the other side: the proof uses only that `p_0` and `p_1` are
`H_{t-1}`-measurable, never that they are functions of a low-dimensional statistic. Part 1 is
therefore a theorem about *always-responsive irreversible exclusion*, and the words "single pull"
carry none of the content.

Consequences.

1. The separation as advertised (single-pull certification versus cumulative certification) is **not
   what is proved**. What is proved is that uniform per-pull responsiveness is fatal. A *cumulative*
   monitor that happened to be `rho`-responsive at every pull would be killed by the same theorem,
   and `MESP` survives not because its statistic is cumulative but because its per-pull exclusion
   probability is zero on all but an `o(1)` fraction of pulls. This is the same phenomenon as
   mechanism W in Section 1.2, and Corollary 1A is what unifies them.
2. Section 1.7 item 4 and summary-table row 4 (`MESP` is not in the class) must be withdrawn or
   rewritten. `MESP` is outside the class *because it is not responsive and because it reactivates*,
   not because of the statistic it reads.
3. The two "in the class" readings of prior work in Sections 1.8.2 and 1.8.4 are unaffected: PURE-SP
   and Braverman Mechanism 1 really are `rho`-responsive with `rho = 1` at every pull (given a
   positive price), which is the hypothesis that does the work.

**Severity.** P1. The fix is definitional and costs nothing mathematically: state the class as
"irreversible exclusion with `H_{t-1}`-measurable per-pull exclusion probabilities", state
Corollary 1A, and drop the claim that a single-pull kernel is a restriction.

## 1.4 CLOSING THE RECORDED OPEN PROBLEM: rules that protect the last active agent do lose

Section 1.9 records as open whether the conclusion can be recovered for rules with at most `K-1`
exclusions, and Section 1.7 item 3 exhibits a `K = 2` rule that protects the last active agent and
collects `n/2 - O(1)` on the instance "one honest agent with `mu = M = 1/2`, one shirker". The
worker's attempted repair (a bait and switch forcing commitment) failed. Here is a repair that works.

The instance in Section 1.7 item 3 is favourable to the rule because the two agents are trivially
distinguishable. Take instead two instances that are *statistically close* and both all honest.

**Class.** `K = 2`. Exclusion mechanism as in Definition 1, irreversible, no reward when no agent is
active, except that the kernel is suspended when only one agent is active (the escape rule). Assume
`rho`-responsiveness at every pull taken while both agents are active. Allocation and price
processes arbitrary and adaptive. This class contains the rule of Section 1.7 item 3.

**The two instances.** Let `eps := 1/32`.

- Instance A: `mu_1 = M_1 = 1/2 + eps = 17/32`, `mu_2 = M_2 = 1/2 - eps = 15/32`.
- Instance B: the same with the labels swapped.

Both agents are honest, and because `M_i = mu_i` the honesty constraint `m in [mu_i, M_i]` forces
`m_{i,t} = mu_i` at every pull: **there is no behavioral freedom at all**, so the instances are
exactly of the type of Theorem 1'. Bernoulli gap `kappa = min{mu_i, 1 - M_i} = 15/32 = 0.46875` in
both. `mu_H^* = 17/32` in both.

**Theorem A1.** Every mechanism in the class above satisfies, on at least one of instances A and B,

    mu_H^* n - P(n)  >=  0.0248 n - 4      for every n >= 1,

when `rho = 1`. (For general `rho` the constant is given by the closed form below and is positive for
every `rho > 0`.)

*Proof.* Write `r_0 := 4`. While both agents are active a pull occurs every round and by Lemma 1 it
excludes the pulled agent with conditional probability at least `kappa rho = 0.46875`. Hence

    Pr( no exclusion in the first r_0 rounds )  <=  (1 - kappa rho)^{r_0}  =  0.53125^4  =  0.0797 .

Let `W := {an exclusion occurs by round r_0 and the excluded agent is agent 1}` and
`W' := {an exclusion occurs by round r_0 and the excluded agent is agent 2}`. At most one exclusion
ever occurs (the survivor is protected), so `W` and `W'` are disjoint and
`W union W' = {an exclusion occurs by round r_0}`, an event measurable with respect to the first
`r_0` rounds.

The mechanism is the same in both instances; the selection kernel, the price map and the exclusion
coin have identical conditional laws given the past. Only the reward channel differs, and by the
chain rule, whichever agent is pulled,

    KL( P_A restricted to r_0 rounds || P_B restricted to r_0 rounds )
      =  r_0 * kl( 1/2+eps , 1/2-eps )  =  r_0 * 2 eps log( (1/2+eps)/(1/2-eps) )  =  0.03129 ,

since `kl(1/2+eps, 1/2-eps) = kl(1/2-eps, 1/2+eps)`. Pinsker gives
`TV <= sqrt(0.03129/2) = 0.1251`. Therefore

    P_A(W) + P_B(W')  >=  P_A(W) + P_A(W') - TV  =  P_A(exclusion by r_0) - TV  >=  1 - 0.0797 - 0.1251 = 0.7952 ,

so `max{ P_A(W), P_B(W') } >= 0.3976`.

Suppose without loss of generality that instance A attains the maximum. On `W`, agent 1 is gone by
round `r_0`, so every later round delivers at most `1/2 - eps` and the first `r_0` rounds deliver at
most `1` each:

    P_A(n)  <=  P_A(W) [ r_0 + n(1/2 - eps) ]  +  (1 - P_A(W)) n(1/2 + eps)
            =   n(1/2 + eps)  -  2 eps n P_A(W)  +  r_0 P_A(W) ,

hence `mu_H^* n - P_A(n) >= 2 eps n P_A(W) - r_0 >= 2 (1/32) (0.3976) n - 4 = 0.02485 n - 4`. `QED`

Verification of the constants: `<scratchpad>/round2/adversary/lastactive.py`. It also reports the
same computation for `rho = 1/2` (`eps = 0.0221`, `r_0 = 8`, loss `>= 0.0168 n - 8`) and `rho = 1/4`
(`eps = 0.0152`, `r_0 = 17`, loss `>= 0.0116 n - 17`), so the conclusion holds for every `rho > 0`
with a constant that degrades only like `sqrt(kappa rho)`.

**Why this is the repair the worker could not find.** The worker looked for an instance forcing a
*commitment* and observed correctly that such a rule is not forced to exclude the agents it stops
pulling. The correct pressure is different: responsiveness forces the rule to spend its single
exclusion within `O(1/(kappa rho))` pulls, and `O(1)` Bernoulli pulls cannot identify which of two
`2 eps`-separated agents is the better one. The rule is not forced to commit; it is forced to commit
*blind*.

**Illustration with a concrete rule** (`<scratchpad>/round2/adversary/rr.py`, `n = 20000`, 400
replications, seed 20260918): the Section 1.7 item 3 rule itself, that is `phi(y,tau) = 1{y < tau}`
with `tau = 1/2`, round robin over the active set, last active agent protected.

| instance | `eps` | observed `P(n)/n` | benchmark `mu_H^*` | observed loss per round | analytic prediction |
|:-|:-|:-|:-|:-|:-|
| `mu = (0.6, 0.4)` | `0.1` | 0.4985 | 0.6 | 0.1015 | 0.1053 |
| `mu = (17/32, 15/32)` | `1/32` | 0.4906 | 0.53125 | 0.0406 | 0.0390 |

The analytic prediction is `2 eps * q_1 / (1 - (1-q_1)(1-q_2))` with `q_i = 1 - mu_i`, the
probability that the better agent is deleted first under round robin. At `eps = 1/32` that
probability is `0.624`: the protected survivor is the *worse* agent more often than not, because
round robin pulls agent 1 first and the kernel fires on a zero.

**Scope of Theorem A1.** It is weaker than Theorem 1' in form: it gives `Omega(n)` loss on one of two
instances rather than `O(1)` total reward on every instance. That is unavoidable, since the rule
genuinely collects `mu_H^* n - O(1)` on the report's own instance. It is nevertheless exactly what
the separation needs, because the honest-benchmark property is quantified over instances: no rule in
this class satisfies `P(n) >= mu_H^* n - o(n)` on every instance with a Bernoulli gap. For `K > 2`
the same two instances with `K-2` further agents give the same conclusion for rules making at most
one exclusion; I did **not** prove the general "at most `K-1` exclusions" case, and I flag that the
natural generalisation needs the `K`-ary version of the two-point argument, which I did not write.

## 1.5 Attacks that failed

- *Decaying randomised exclusion.* The kernel `phi_i(y,tau)` cannot depend on `t` directly, but it
  can through `tau_t`; a kernel with `max{phi(0,tau_t), phi(1,tau_t)} = c/t` has essential infimum
  `rho = 0` over a run, so it is outside the responsive class, and Corollary 1A prices it exactly:
  `E[T_h] <= sum` of the per-pull hazards inverted, which for `c/t` gives `E[T_h] = O(n/c)` pulls but
  also gives `sum_t kappa c/t = Theta(c log n)` expected exclusions, so the total reward is
  `O(n)` only if `c = O(1/log n)`. This is not an escape from Theorem 1', which assumes a uniform
  `rho`; it is an instance of the escape already priced by Corollary 1A. Nothing new.
- *Reactivation.* Already outside the class by irreversibility and already recorded. I did not find
  a way to make reactivation matter beyond what Section 1.7 item 3 says.
- *Making Theorem 1' fail on its own hypotheses.* I tried instances with `mu_H^* > 1 - kappa`
  (impossible, `mu_h <= M_h <= 1-kappa`), with an empty active set reached early (helps the theorem),
  with agents randomising their targets (Lemma 1 is pointwise in `m`, so no help), and with
  `phi` depending on the agent's index and on a frozen bid (Remark (a) covers it). All failed.
- *The aside "delivering 0 is the myopically optimal per-pull choice of a strategic agent, whose
  per-pull utility is `1 + mu_i - m`".* This is a per-pull statement only and ignores the
  continuation value of not being excluded, which is the entire subject of the theorem. It is not
  load-bearing (Theorem 1 only needs the profile to be *feasible*), but it should be deleted or
  qualified. P3.

# RESULT 2. The monitor lower bound (Theorem S1)

I did not re-run the deviation numerically; the caller had already done that. I re-derived the proof,
the constant, and the two items the caller asked about.

## 2.1 The caller's correction is CONFIRMED on the value and the report understates by `sqrt 2`

I first tried to refute the caller and got as far as a wrong refutation. The resolution is that both
numbers are right about different quantities, and the report's sentence is wrong about which one it
is computing.

`MESP` has `beta = sqrt( log(2 n^4)/2 ) ~ sqrt(2 log n)`. Write `N` for Theorem S1's planned phase
length. Then `theta = 1 - sqrt(log 2N)/beta -> 1 - 1/sqrt 2 = 0.29289` for any `N` polynomial in `n`,
and the saving is `theta beta (sqrt N - sqrt r_0) ~ 0.29289 * sqrt(2 log n) * sqrt N`. Hence

    N = n/2  :  saving ~ 0.29289 * sqrt(2 log n) * sqrt(n/2)  =  (1 - 1/sqrt 2) sqrt(n log n)  =  0.29289 sqrt(n log n) ,
    N = n    :  saving ~ 0.29289 * sqrt(2 log n) * sqrt(n)    =  (sqrt 2 - 1)   sqrt(n log n)  =  0.41421 sqrt(n log n) .

**Which `N` is `MESP`'s?** Stage 2 pulls the winner at every remaining round, so the planned phase
length is `N_n = n - K L_n` with `L_n asymp n^{2/3}(log n)^{1/3}`
(`sections/Private_information_setting.tex` lines 11 and 12, and the Stage-2 loop at line 29), that
is `N_n = n (1 - o(1))`, **not** `n/2`. The report writes "`N = N_n >= n/2`", which is a correct but
very lossy bound, and then says the leading factor "tends to `(sqrt 2 - 1) sqrt(log n) * sqrt(n/2)
= 0.293 sqrt(n log n)`". Substituting a lower bound for `N_n` and then calling the result a limit is
the error. The limit is `sqrt 2 - 1`.

Numerical confirmation, exact formula at `tau = 0.3`, `K = 2`, `L_n = n^{2/3}(log n)^{1/3}`
(`<scratchpad>/round2/adversary/const2.py`), column is saving `/ sqrt(n log n)`:

| `n` | `N = n/2` | `N = n - K L_n` | `N = n` |
|:-|:-|:-|:-|
| `10^4` | 0.27114 | 0.33143 | 0.36208 |
| `10^6` | 0.29541 | 0.38677 | 0.39476 |
| `10^9` | 0.29692 | 0.40241 | 0.40339 |
| `10^12` | 0.29602 | 0.40606 | 0.40617 |
| `10^18` | 0.29498 | 0.40884 | 0.40884 |
| `10^40` | 0.29383 | 0.41179 | 0.41179 |

The middle column, which is `MESP`'s actual Stage-2 length, converges to
`sqrt 2 - 1 = 0.41421`. The left column, the report's substitution, converges to
`1 - 1/sqrt 2 = 0.29289`.

**On the caller's stated reason.** The caller said `0.293` "is one minus one over root two, which is
the ratio of the saving to the monitoring boundary, a different quantity". That identification is
also correct: `theta -> 1 - 1/sqrt 2` exactly, and `theta` is by construction the ratio of the saving
to `B(N)`. The two routes to `0.293` coincide because `beta sqrt(n/2) ~ sqrt(n log n)`, so with
`N = n/2` the saving is simultaneously `0.293 sqrt(n log n)` and `0.293 B(N)`. The report's algebra
is internally consistent; what is wrong is the choice of `N`, not the manipulation of `theta`.

**Propagation.** Two places, both in the same direction.

1. Section 4.3, the sentence quoted above. Repair: either write "at least `0.293 sqrt(n log n)`,
   using `N_n >= n/2`", or state the sharp form, "the saving is
   `theta ( b_n(N_n) - b_n(r_0) ) ~ (sqrt 2 - 1) sqrt(n log n)` with `N_n = n - K L_n`".
2. Section 6's numerical table and its closing sentence "`0.293` is the limit computed in
   Section 4.3". The table was computed with `N = n/2` (its own `N` column shows `5000` at
   `n = 10^4`), so its ratios `0.271 ... 0.297` are ratios for the pessimised phase length. With
   `N_n = n - K L_n` the same rows give `0.331 ... 0.406`. The finite-`n` floor
   "at least `0.25 sqrt(n log n)` for every `n >= 10^3`" stays valid, being conservative.

No other occurrence of the constant exists in the document; I grepped for `0.29`, `0.41`, `0.293`,
`0.414` and `sqrt 2 - 1`. The order `Omega(sqrt(n log n))`, Corollaries S1.1 and S1.3 and the route
map are unaffected, since they quote orders and not constants.

**Severity P2.** Nothing false is asserted about `MESP`'s guarantee, because `0.293 sqrt(n log n)` is
a valid lower bound; but the word "tends to" is wrong, and the number understates the concession by
a factor `sqrt 2`. If the paper quotes a constant it must quote `sqrt 2 - 1`, or say "at least".

## 2.2 A real error found instead: Corollary S1.2 proves the opposite of what it concludes

Corollary S1.2 says: the saving with `J` per-region monitors is `theta sum_C (B(N_C) - B(r_0))`,
"which by concavity and `sum_C N_C = n` **is maximised at equal regions** and equals
`Theta(beta sqrt(J n))`", and concludes "a mechanism with `J` local monitors **concedes**
`Omega(sqrt(J n log n))`", and then calls this "a matching lower bound for the monitoring term".

The middle step gives an *upper* bound on the deviator's saving and the conclusion needs a *lower*
bound. The visit counts `N_C` are chosen by the mechanism and by the context sequence, not by the
deviator. If the realised pulls concentrate on one region, `sum_C sqrt(N_C) = sqrt n` and the saving
is `Theta(beta sqrt n)`, a factor `sqrt J` below the claim. Concavity says exactly that `sqrt(J n)`
is the *best* case for the deviator, so quoting the maximum as the concession is backwards.

Minimal repair: add the hypothesis that the realised visit counts are balanced, `N_C = Theta(n/J)`
for a constant fraction of the regions, which holds under the i.i.d. context assumption the
manuscript uses elsewhere but is an assumption, and state the general bound as
`Omega( beta sum_C sqrt(N_C) )`, which is between `beta sqrt n` and `beta sqrt(J n)`. Also the
subtraction `J theta B(r_0)` is not negligible and needs `n/J >> r_0 = Theta(log n / tau^2)`.

**Severity P1**, because the corollary is used to claim the `O(sqrt(J n log n))` accounting term "is
exactly right and cannot be improved by analysis". As stated that claim is not proved.

## 2.3 CLOSING Section 5(c): the anti-concentration converse holds, and Slud is not needed

The gap: Theorem S1 assumes `B(r) >= beta sqrt r`; to make it a statement about every monitor one
needs the converse, that a small compliant false-alarm probability forces a boundary of that order.

### 2.3.1 Slud, checked against the primary source

Eric V. Slud, "Distribution Inequalities for the Binomial Law", *The Annals of Probability* 5(3),
404-412, June 1977, DOI `10.1214/aop/1176995801`, read 18 September 2026 at
`https://projecteuclid.org/journals/annals-of-probability/volume-5/issue-3/Distribution-Inequalities-for-the-Binomial-Law/10.1214/aop/1176995801.full`.
Abstract, verbatim: "We prove that the probability of at least `k` successes, in `n` Bernoulli trials
with success-probability `p`, is larger than its normal approximant if `p <= 1/4` and `k >= np` or if
`p <= 1/2` and `np <= k <= n(1-p)`."

So Slud's inequality is `Pr(X >= k) >= 1 - Phi( (k-np)/sqrt(np(1-p)) )` under those conditions, which
are conditions on the **upper** tail with `p <= 1/2`. The monitor's false alarm is a **lower**-tail
event for `Z_N ~ Binomial(N, tau)`. Converting, `Pr(Z_N <= N tau - u) = Pr(W >= N(1-tau) + u)` with
`W ~ Binomial(N, 1-tau)`, and Slud's hypotheses then require `1 - tau <= 1/2`, that is
**`tau >= 1/2`**, plus `u <= N(2 tau - 1)`.

Therefore the report's remark that Slud "would give it immediately" is only correct when the
announced price is at least `1/2`. In `MESP` the price is `tau = (beta_(2) - s_n)_+`, which is not
constrained to be at least `1/2`, so the shortcut the report declined to use would not in fact have
closed the gap in the generality claimed. This is worth recording independently of the closure below.

### 2.3.2 The report's fallback claim is wrong: Berry and Esseen cannot work

Section 5(c) says "A Berry and Esseen route would also work and has the same problem". It would not
work. Berry and Esseen bounds the Kolmogorov distance to the normal by `C rho / (sigma^3 sqrt N)`,
which is `Theta(N^{-1/2})`. The probability that has to be lower bounded here is `delta`, which for
`MESP` is `(2 n^3)^{-1}` with `N = Theta(n)`, that is far below the Berry and Esseen error term. The
route is not merely unverified, it is unusable in this regime; only a bound with a multiplicative
error, such as Slud's or the one below, can work. **Severity P2**, a wrong statement about a method
in a section that a reader may act on.

### 2.3.3 The gap, closed elementarily and for every `tau`

The following is self-contained, uses no external result, and covers all `tau in (0,1)`.

**Lemma A2 (method of types, one line each).** Let `X ~ Binomial(N, p)` and let `0 <= k <= N`, `q :=
k/N`. Then `Pr(X = k) >= exp( -N * KL(q || p) ) / (N+1)`, where
`KL(q||p) = q log(q/p) + (1-q) log((1-q)/(1-p))`.

*Proof.* Under `Binomial(N, q)` the value `k = Nq` is a mode, and there are `N+1` possible values, so
`C(N,k) q^k (1-q)^{N-k} >= 1/(N+1)`, that is `C(N,k) >= exp(N H(q))/(N+1)` with
`H(q) = -q log q - (1-q) log(1-q)`. Multiply by `p^k (1-p)^{N-k} = exp( N ( q log p + (1-q) log(1-p) ) )`
and collect terms. `QED`

**Proposition A3 (converse).** Let a monitor with deterministic nondecreasing boundary `B` have
compliant false-alarm probability at most `delta` over `N` pulls at price `tau` (the compliant agent
delivers `tau` at every pull, so `Z_r ~ Binomial(r, tau)`). Then for every `r <= N` with
`B(r) < r tau`,

    r * KL( k_r / r || tau )  >=  log( 1 / ( (r+1) delta ) ) ,      k_r := ceil( r tau - B(r) ) - 1 ,

and consequently, using `KL(q||p) <= (q-p)^2/(p(1-p))`,

    B(r) + 1  >=  sqrt( r * tau (1-tau) * log( 1/((r+1) delta) ) ) .

*Proof.* The false-alarm event contains `{Z_r = k_r}` because `k_r < r tau - B(r)`; apply Lemma A2
with `u := r tau - k_r in (B(r), B(r)+1]` and bound `KL` by the chi-square divergence of two Bernoulli
laws, which is `(q-p)^2/(p(1-p))`. `QED`

Both steps verified numerically (`<scratchpad>/round2/adversary/converse.py`): `0` violations of
Lemma A2 over all `k` for `N in {10,50,200,1000}` and `p in {0.05,0.2,0.3,0.5,0.7,0.9}`, and `0`
violations of `KL <= chi^2` over a grid of `6000` pairs.

The chi-square step loses a factor of `2` in the exponent. Keeping the exact exponent instead and
expanding `KL(tau - u/r || tau) = (u/r)^2 / (2 tau (1-tau)) * (1 + O(u/(r tau)))`, valid because
`u/r -> 0` in the regime of interest, gives the sharp form

    B(r)  >=  sqrt( 2 r tau (1-tau) log( 1/((r+1) delta) ) ) * (1 - o(1)) .

**Proposition A4 (the converse composes with Theorem S1, with the same constant).** Run Theorem S1's
deviation, but note that under it the targets `m_r` depend only on `r`, so `Z_r` is a sum of
*independent* Bernoulli variables and the exact Chernoff bound applies in place of Azuma: the phase
terminates at `r` only if `Z_r` falls below its own mean by `(1-theta) B(r)`, an event of probability
at most `exp( - (1-theta)^2 B(r)^2 / (2 r tau(1-tau)) ) (1+o(1))`. A union bound over `r <= N` keeps
this below `1/(4N)` as soon as

    (1-theta)^2 B(N)^2 / (2 N tau(1-tau))  >=  log(4N) .

Combining with Proposition A3's sharp form, a positive `theta` exists whenever

    theta  <=  1 - sqrt( log(4N) / log( 1/((N+1) delta) ) ) ,

which is positive exactly when `delta = o( 1/N^{1+c} )` for some `c > 0`. The saving is then
`theta B(N) = Omega( sqrt( N tau(1-tau) log(1/delta) ) )` for **every** monitor with compliant
false-alarm probability `delta`, with no assumption on the shape of `B`.

For `MESP`'s own parameters (`delta = (2n^3)^{-1}`) and the conservative `N = n/2` the ratio is
exact, `log(4N)/log(1/((N+1)delta)) = log(2n)/log(4n^2) = 1/2` for every `n`, and for the true
`N_n = n - K L_n` it tends to the same `1/2`, so the composed bound gives
`theta <= 1 - 1/sqrt 2 = 0.2929`, **numerically identical to Theorem S1's own `theta`**. The
numerical check also compares the exact smallest admissible boundary with the formula and with
`MESP`'s: at `n = 10^6`, `tau = 0.3`, `N = n/2`, the smallest `B(N)` with per-pull false alarm at most
`delta` is `2858`, Proposition A3's chi-square formula gives the valid lower bound `2469`, and `MESP` uses
`3740`. So `MESP`'s boundary is about `1.31` times the information-theoretic minimum, and the
converse is not vacuous.

**Conclusion on Section 5(c).** The gap is closed, for every `tau in (0,1)`, without Slud, without
Berry and Esseen, and without any unverified literature fact. Corollaries S1.1 and S1.3 can be
restated unconditionally over the class "cumulative-deficit monitor with compliant false-alarm
probability `delta = o(N^{-1-c})`". Corollary S1.2 still needs the separate repair of Section 2.2
above. The one thing Proposition A3 does not give is the *nonasymptotic* constant: the `(1 - o(1))`
in the sharp form must be made explicit before the composed corollary is stated as a theorem, and I
did not do that.

## 2.4 Attacks on the class of Definition S1

1. **"The monitored agent receives every pull of the phase."** This hypothesis is **never used** in
   the proof. `F_r` is the history through the agent's `r`th pull, the martingale `M_r` is indexed by
   the agent's own pulls, the termination rule `T = min{r : Z_r < r tau - B(r)}` is indexed by the
   agent's own pull count, and the union bound is over `r <= N` where `N` is the number of *its*
   pulls. Interleaving the monitored agent with other agents therefore changes nothing except the
   meaning of `N`, which becomes the agent's own pull count. The concession is
   `Omega(beta sqrt(N_i))` where `N_i` is the number of pulls the mechanism gives agent `i`, so a
   mechanism can only escape by giving the monitored agent `o(n)` pulls, which costs it the revenue
   it was monitoring for. **Not an escape**; the hypothesis should simply be deleted from
   Definition S1, which strengthens the theorem at zero cost.
2. **Restarts.** Suppose the mechanism resets `Z` and `r` at `S` points, giving segments of lengths
   `N_1, ..., N_S` with `sum N_s = N`. The deviator runs the strategy in each segment. The union
   bound is over `sum N_s = N` pulls, unchanged, and the saving is
   `theta sum_s ( B(N_s) - B(r_0) ) = theta beta ( sum_s sqrt(N_s) - S sqrt(r_0) )`. By concavity
   `sum_s sqrt(N_s) >= sqrt N` always, with equality only for one segment, and the sum grows with the
   number of segments up to `sqrt(S N)`. So restarting **increases** the concession, as long as
   `N_s >> r_0`. Restarts are not an escape, they are a self-inflicted wound. (The mechanism's only
   gain from restarting is a smaller per-segment boundary, which is exactly what lets the deviator
   shade again from a clean slate.)
3. **Randomised boundaries that do not depend on the rewards.** Let the boundary be drawn from a law
   independent of the reward sequence, with overall compliant false alarm at most `delta`. Write
   `f(B) := Pr(false alarm | B)`, so `E[f(B)] <= delta`. By Markov, `Pr( f(B) > N delta ) < 1/N`. On
   the complementary event, of probability at least `1 - 1/N`, the realised boundary satisfies
   Proposition A3 with `delta` replaced by `N delta`, hence `B(r) >= sqrt(2 r tau(1-tau) log(1/((r+1) N delta)))
   (1-o(1))`. The deviator shades against that deterministic envelope. It is terminated with
   probability at most `1/N + 1/(4N)`, which contributes at most `2n(1/N + 1/(4N)) = O(1)` to the
   utility accounting when `N = Theta(n)`. For `MESP`'s `delta = (2n^3)^{-1}` the envelope loses only
   `log N` out of `log(1/delta) = 3 log n`, so the concession survives with a slightly smaller
   constant. **Not an escape.**
4. **Path-adapted termination rules.** A rule that stops on a general stopping time of the reward
   path, rather than on a deficit against a predictable boundary, is genuinely outside everything
   above and outside Proposition A3, since `f(B)` no longer factorises. I tried to close it by change
   of measure: if the deviator's law `P'` differs from compliance `P` by a total shading `G` spread
   over `N` pulls, then `KL(P'||P) <= G^2/(N tau(1-tau))`, so by Pinsker
   `P'(terminate) <= delta + G/sqrt(2 N tau(1-tau))`. This yields survival probability at least
   `1/2` for `G = Theta(sqrt N)`, which is *weaker* than Theorem S1 in two ways: no `log` factor, and
   only constant survival probability, whereas the utility accounting needs survival with probability
   `1 - O(1/n)`. Pushing Pinsker to that confidence forces `G = O(sqrt N / n)`, which is vacuous. So
   change of measure cannot give this and I record the general adapted-stopping case as **open**,
   with the note that it is the natural remaining generalisation and that the obstruction is the same
   one that defeats Bretagnolle and Huber in the report's own Section 5(c).

# RESULT 3. The Grid-EXP3 robustness theorem

## 3.1 The named weak point, (H1) obliviousness, is FIXABLE, and the fix is short

Section 2.8 names Step 1, the freezing of the context sequence, as the least secure step, and
Section 2.7 item 7 says an adapted adversary choosing `x_t` after seeing the platform's coins is not
covered, because the realised epoch lengths become random and Lemma A is stated for a deterministic
`T`. I attacked this from both sides. The adversary does not win, and the hypothesis can be removed.

**Why the adversary does not win.** The obvious adapted attack is to route contexts so as to keep
every cell in a fresh epoch, paying the `R_K(2^k)` start-up cost as often as possible. The extreme
version sends every round to a different cell, so `V_C = 1` at `n` cells and the total exploration
cost is `n R_K(1) = Theta(n sqrt(K log K))`, which is linear. But this attack is available to an
*oblivious* adversary already, and it is capped by the grid: there are only `J_n <= 2^D n^{D/(D+2)}`
cells, so `J'_n = o(n)` and `sqrt(J'_n n) = o(n)`. Adaptivity buys the adversary nothing here,
because the mechanism's per-cell state is not observable in any way the adversary can exploit beyond
choosing cells, and cell choice is already worst-cased in Step 5.

**The fix: Lemma A holds with `T` a stopping time.** The report's own proof already does the work.
Inequality `(*)` is pathwise and holds for every prefix length, so it holds at a random prefix
length. Only the passage to expectations has to be redone, and the standard optional-skipping form
suffices. Let `t_s` be the global round of the epoch's `s`th local visit, a stopping time of the
global filtration because the context `x_t` is revealed at the start of round `t`, before selection.
Define `G_{s}` to be the global history through the end of round `t_s`, and enlarge `G_{s-1}` to
contain `x_{t_s}` (legitimate, since the context is revealed before the platform's selection coin).
Then

- `{ T >= s } = { t_s <= n and the cell is visited an s-th time in this epoch }` is
  `G_{s-1}`-measurable;
- `p_s` is `G_{s-1}`-measurable (it is a function of the cell's weights, which are determined by the
  epoch's earlier local visits);
- `I_{t_s}` is drawn with fresh randomness independent of `G_{s-1}` and of the round's Bernoulli seed.

Rewrite each term of `(*)` as a sum over `s = 1, ..., H_0` with the factor `1{T >= s}`:

    E[ sum_{s<=T} hatY_{j,s} ]      = sum_s E[ 1{T>=s} E[ hatY_{j,s} | G_{s-1} ] ] = sum_s E[ 1{T>=s} r_{j,s} ] >= v E[T] ,
    E[ sum_{s<=T} sum_i q_i hatY_i ] = sum_s E[ 1{T>=s} Q_s ] <= (1-gamma)^{-1} E[ sum_{s<=T} Y_s ] ,
    E[ sum_{s<=T} sum_i q_i hatY_i^2 ] <= K/(1-gamma) * E[T] <= K H_0/(1-gamma) ,

the first and second because `1{T>=s}` is `G_{s-1}`-measurable, so it passes through the conditional
expectation. Every subsequent line of the report's proof of Lemma A is unchanged with `T` replaced by
`E[T]` on the left and `H_0` used only in the final case analysis, which already only used `T <= H_0`.
The conclusion becomes

    E[ sum_{s<=T} Y_s ]  >=  v E[T]  -  R_K(H_0) ,      T any stopping time with T <= H_0 ,

which is what Steps 2 and 3 need. Step 3 then sums `E[T_{C,k}]` over `k` to `E[V_C]`, and the
start-up costs are collected as `E[ sum_k 1{V_C >= 2^k} R_K(2^k) ] = E[ R^dbl_K(V_C) ]`, where the
indicator is legitimate because `{V_C >= 2^k}`, the event that epoch `k` of cell `C` ever starts, is
measurable at the epoch's start. Step 5's Cauchy and Schwarz bound
`sum_C sqrt(V_C+1) <= sqrt(J'_n (n + J'_n)) <= sqrt(2 J'_n n)` is **pathwise**, hence survives taking
expectations with no Jensen step. So Theorem 3's display holds verbatim with `sum_t b(x_t)` replaced
by `E[ sum_t b(X_t) ]`, for adapted contexts.

**The one honest caveat, which must be stated if the extension is used.** For an adapted adversary
the realised context sequence depends on the platform's own coins, so `E[sum_t b(X_t)]` is a
*policy-dependent* benchmark: it is the honest benchmark evaluated on the contexts that this
algorithm's run actually produced, not on the contexts a comparator policy would have faced. That is
the standard and unavoidable weakness of adaptive-adversary guarantees, and it is weaker than the
oblivious statement in a way that no proof can remove. My judgement: state Theorem 3 for oblivious
contexts as the headline, and add the adapted extension as a remark with this caveat attached. Do not
state the adapted version without it.

**Verdict on the named weak point: not genuine as a proof gap, genuine as a semantic one.** Step 1 is
a convenience, not a necessity; the mathematics extends in about fifteen lines. What does not extend
is the meaning of the benchmark.

## 3.2 The doubling constant is right

The caller asked specifically. I re-derived Lemma B without looking at the report's algebra.

- Epochs `0, ..., m-1` cover `2^m - 1` local visits, so `m` is the least integer with `2^m >= V+1`,
  that is `m = ceil(log_2(V+1))`. Checks: `V=1 -> m=1`, `V=2 -> m=2`, `V=3 -> m=2`, `V=4 -> m=3`. All
  correct against the schedule "epoch `k` covers local visits `2^k` to `2^{k+1}-1`".
- `sum_{k=0}^{m-1} (sqrt 2)^k = ((sqrt 2)^m - 1)/(sqrt 2 - 1) <= (sqrt 2 + 1) 2^{m/2}` using
  `1/(sqrt 2 - 1) = sqrt 2 + 1`.
- `m <= log_2(V+1) + 1` gives `2^{m/2} <= sqrt(2(V+1))`, which is the `sqrt 2` the worker worried
  about, and it is the correct side: `2^{m/2} <= sqrt(V+1)` would be **false**, as `V=2`, `m=2`
  shows (`2^{m/2} = 2 > sqrt 3 = 1.732`).
- Total: `3 (sqrt 2 + 1) sqrt 2 = 3 (2 + sqrt 2) = 10.2426`, and `11` is a valid round-up.

So the constant is right and the worker's third self-doubt is resolved in favour of the report. The
additive part `2 K log K m` with `m <= log_2(2(V+1))` is also right.

## 3.3 Other attacks on Part 2, all failed

- **Lemma A algebra.** Re-derived independently. `e^x <= 1+x+x^2` on `[0,1]` holds; `eta hatY <= 1`
  needs `p_{i,s} >= gamma/K = eta`, which the exploration floor gives; `q_i <= p_i/(1-gamma)`;
  `E[hatY_i^2|G] <= r_i/p_i`; `E[Y_s|G] >= (1-gamma) Q_s`. The two-case bound on
  `2 gamma T + (K log K)/gamma` by `R_K(H_0)` is correct in both branches, including the
  `H_0 < 4 K log K` branch where `H_0 <= 2 sqrt(K H_0 log K)`.
- **Lemma C.** Two points in the same cube of side `h_n` in `[0,1]^D` differ by at most `h_n` per
  coordinate, and an agent's block occupies `d` coordinates, so the Euclidean distance within a block
  is at most `sqrt d h_n`. A maximum of `L sqrt d h_n`-close functions is `L sqrt d h_n`-close. The
  factor `2` in `b(X) <= v_C + 2 L sqrt d h_n` is needed and is there.
- **Grid tuning.** Balancing `2 L sqrt d n h` against `11 sqrt(K n h^{-D} log K)` gives
  `n h^{D+2} = Theta(1)`, that is `h = n^{-1/(D+2)}`, which is the grid used. The exponent
  `(D+1)/(D+2)` is the right one for this decomposition, and the additive term
  `n^{D/(D+2)} log n` is genuinely `o(n^{(D+1)/(D+2)})`.
- **Attack via cell fragmentation.** Covered in Section 3.1: capped by `J_n`.
- **Attack via the enlarged filtration in (H2).** `H_{t-1}` is allowed to contain all agents' private
  coins and the entire context sequence. This makes `p_t` more, not less, constrained, and the EXP3
  argument only needs `p_s` to be `G_{s-1}`-measurable and `I_s` to be conditionally independent of
  the round's Bernoulli seed, both of which survive. The selected agent's target being
  `H_{t-1} v sigma(I_t)`-measurable is exactly what makes `r_{i,s}` well defined. I could not break
  the "selected reactive" bookkeeping; the worker's second self-doubt is unfounded.
- **The honest description in Section 2.7 item 10.** I checked the claim that Theorem 3 removes the
  `(log n)^{1/(D+2)}` factor of `thm:grid-ucb-robust`: the leading constant here is
  `11 sqrt 2 * 2^{D/2} sqrt(K log K)` with no `log n`, so the claim is right as arithmetic. The rest
  of item 10 is an honest self-limitation and I have nothing to add to it.

## 3.4 What would have to be true to break Result 3

I did not break it. For it to be false, one of the following would have to fail: (i) the per-epoch
EXP3 potential argument with a comparator whose conditional mean is bounded below at every visit of
the cell, which I re-derived; (ii) the pathwise Lipschitz comparison of Lemma C, which is a two-line
geometric fact; (iii) the pathwise Cauchy and Schwarz aggregation over cells. The only route I see to
a genuine counterexample is a mechanism-level misreading, for instance if the manuscript's contextual
model let an agent's capacity or the honest floor depend on the platform's past selections, in which
case Lemma C (ii) would lose its pointwise lower bound. That is not the model in
`sections/setting.tex`.

# 4. Consolidated findings, severities and minimal repairs

| Sev | Where | Finding | Minimal repair |
|:-|:-|:-|:-|
| P1 | `separation/REPORT.md` summary bullet "Part 1", Section 4 table row 1, and any paper sentence of the form "single-pull reaction loses the benchmark" | False without the responsiveness clause. Mechanism W of Section 1.2 is in the class, applies its kernel unconditionally at every pull, and collects `Omega(n)` unconditionally and `mu_H^* n - O(n^{2/3})` with a UCB warm-up | Always carry `rho`-responsiveness, and state Corollary 1A (responsive-pull budget) as the headline instead |
| P1 | `separation/REPORT.md` Section 1.7 item 4 and Section 4 table row 4 | "Cumulative monitors are outside the class by construction" is false. `MESP`'s monitor is inside Definition 1 as literally written, via the price channel, so the class is not a single-pull class | Redefine the class as irreversible exclusion with `H_{t-1}`-measurable per-pull exclusion probabilities, and say `MESP` escapes by non-responsiveness and reactivation, not by its statistic |
| P1 | `f1-continuous-private/SCEPTIC.md` Corollary S1.2 | The proof maximises `sum_C sqrt(N_C)` and then quotes the maximum as a concession; the direction is wrong, and the claim that the `O(sqrt(J n log n))` accounting term is matched is unproved | Add a balanced-visits hypothesis `N_C = Theta(n/J)`, or state the bound as `Omega(beta sum_C sqrt(N_C))` |
| P2 | `f1-continuous-private/SCEPTIC.md` Section 4.3 and Section 6 | The limiting constant is `sqrt 2 - 1 = 0.414`, not `0.293`; `0.293` comes from substituting `N >= n/2` for the true Stage-2 length `N_n = n - K L_n` and then calling the result a limit | Write "at least `0.293 sqrt(n log n)`", or state the sharp limit `sqrt 2 - 1` |
| P2 | `f1-continuous-private/SCEPTIC.md` Section 5(c) | "A Berry and Esseen route would also work" is false in this regime: its error is `Theta(N^{-1/2})` and the probability to be bounded below is `delta = Theta(n^{-3})` | Delete the remark; use Lemma A2 and Proposition A3 of Section 2.3.3 instead |
| P2 | `f1-continuous-private/SCEPTIC.md` Section 5(c) | Slud's inequality, checked at the primary source, is an upper-tail statement requiring `p <= 1/2`, so for the monitor's lower tail it needs `tau >= 1/2` and would not have closed the gap for general prices | Record the restriction, or use the elementary route which has none |
| P2 | `f1-continuous-private/SCEPTIC.md` Definition S1 | The hypothesis "the agent is pulled at every round of the phase" is never used | Delete it; the theorem then covers interleaved monitoring with `N` the agent's own pull count |
| P2 | `separation/REPORT.md` Section 1.9 | The open problem about rules with at most `K-1` exclusions is closed for `K = 2` by Theorem A1 of Section 1.4 | Replace "open" by Theorem A1, and keep the general `K` case as the remaining open part |
| P2 | `separation/REPORT.md` Section 2.7 item 7 and Section 2.8 | Obliviousness is removable by an optional-skipping version of Lemma A; the limitation is semantic, not mathematical | Add the extension as a remark with the policy-dependent-benchmark caveat |
| P3 | `separation/REPORT.md` Theorem 1 statement | "Delivering `0` is the myopically optimal per-pull choice" ignores the continuation value of not being excluded, which is the theorem's whole subject. The utility form `1 + mu_i - m` itself is correct (`sections/setting.tex` line 20) | Delete the aside or say "per-pull myopically optimal, ignoring continuation" |

## 4.1 What would have to be true for the unbroken claims to break

- **Theorem 1 and 1'.** They would break if a `rho`-responsive irreversible exclusion mechanism could
  give an honest agent with a Bernoulli gap a super-constant expected tenure. Lemma 1 forbids this
  pointwise in the agent's target, so a counterexample would need either an honest target outside
  `[kappa, 1-kappa]`, contradicting the Bernoulli gap, or an exclusion coin correlated with the
  future, contradicting Definition 1 step 4. I see no route.
- **Theorem S1.** It would break if the deviation `m_r = tau - theta(B(r)-B(r-1))` were infeasible or
  if the Azuma step were misapplied. I checked feasibility at `r = r_0 + 1`, which is the binding
  index, and the conditional-range-`1` form of Azuma, which is the same form the manuscript uses at
  `sections/Private_information_setting.tex` line 58. The remaining route is a mechanism whose
  termination rule is a general path-adapted stopping time rather than a deficit against a
  predictable boundary; that case is open and is the only place I would still look.
- **Theorem 3.** It would break if the honest comparator's conditional mean could fail to be bounded
  below at some visit of its cell, which needs the honest floor `mu_h(x)` to depend on the platform's
  past selections. It does not in `sections/setting.tex`.

## 4.2 What I did not do

- I did not attempt the general `K` case of Theorem A1 (rules making at most `K-1` exclusions with
  `K > 2`). Only `K = 2` is proved.
- I did not make the `(1 - o(1))` in Proposition A3's sharp form explicit, so the composed
  Proposition A4 is asymptotic and is not yet a finite-`n` theorem.
- I did not close the path-adapted stopping-rule case for Theorem S1, and I recorded why change of
  measure cannot close it.
- I did not re-run the caller's numerical validation of Theorem S1's deviation, as instructed. Every
  number in Section 2.1 is a closed-form evaluation, not a simulation.
- I did not check Part 2's numerical Section 3.2 or Part 1's Section 3.1 beyond the two rows I
  recomputed analytically.
