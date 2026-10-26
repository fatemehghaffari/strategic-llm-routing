# H1: impossibility results for private capacities

Worker: the H1 theorem track, 18 September 2026. Output scope: this directory and the scratchpad.
No canonical file was read for writing and none was modified. No em dash and no LaTeX triple hyphen
appears in this file.

Read before starting: `audit/round2/prompts/COMMON.md`;
`audit/round2/B/theorems/f1-continuous-private/EXPLORER.md` Section 2 (the raw material);
`sections/setting.tex`; `sections/Private_information_setting.tex`;
`sections/appendix_private.tex`; `audit/round2/B/theorems/separation/REPORT.md` and its `ADVERSARY.md`.

I do not claim any result below is correct. I claim that for each result I state every hypothesis,
give a proof from the model in `sections/setting.tex`, say what the result does not cover, and say
whether a natural mechanism escapes it. Section 11 names the step I consider least secure.

## 0. Summary of verdicts on the raw material

The raw material is EXPLORER.md Section 2: Lemma 1 (imitation), Corollary 2 (no upper confidence
bound), Proposition 3 (revealed envelope), Proposition 4 (covering count).

| raw item | verdict | change needed |
| -- | -- | -- |
| Lemma 1, imitation | correct as stated | add the hypothesis that the other agents' rules do not observe agent `j`'s capacity, which the private setting supplies but which the statement leaves implicit |
| Corollary 2, no valid upper confidence bound | correct as stated, and stronger than stated | the suspected defect is not there. It holds pointwise at every query point, including a point where the agent has just revealed, and it holds conditionally on the realised record. It must be restated as a bound by the class maximum rather than by `1`, and the real scope limit is a different one: validity is required against arbitrary behaviour, not at a fixed profile |
| Proposition 3, revealed envelope | correct as an equality of constraint sets, incomplete as an identification claim | add the observational equivalence half, that is, exhibit for each `M >= E` a behaviour under which the observed record has the same probability. Proved below as T2 |
| Proposition 4, covering count | correct, and extends to adaptive designs | the volume step is valid; the stated hypotheses `eps <= 1/4`, `L >= 4 eps` are only used to make the conclusion non-vacuous. The sup-norm criterion is not the criterion the revenue objective needs, so I add an `L^1` version (T6) |

New results proved here and not present in the raw material: T3 (no revelation without allocation
feedback), T4 (the rent transfer theorem, which is the exact answer to "why the second capacity"),
T6 (the average-error covering bound), T7 (one-sided shading is necessary), and the corrected form
of T2.

I also verified one statement from EXPLORER Section 2.6, item 2, that no mechanism guarantees second
capacity revenue under arbitrary behaviour; it is correct, it is one line, and it is recorded as T8
because it is what forces the three part shape of `thm:private-mesp`. I did not audit items 1, 3 and
4 of that section, which are design commentary rather than theorems.

Prior art: T4 is a known result in a neighbouring model. Braverman, Mao, Schneider and Weinberg
(COLT 2019) Lemma 14 states that no truthful mechanism can guarantee revenue
`(alpha mu + (1 - alpha) mu') T` in the worst case, for any constant `alpha > 0`, where `mu` and
`mu'` are the largest and second largest arm means. Their model and their hypotheses are not ours,
and their proof uses a two sided incentive constraint that our model does not provide, so I reprove
a version with our hypotheses and attribute the statement. Details and URLs in Section 9. I did not
find a primary source for T1, T2, T3, T6 or T7 in the form stated; see Section 9 for what I checked
and for the antecedents I did find.

## 1. Setting, and the one lemma everything rests on

I use the model of `sections/setting.tex` verbatim. `K >= 2` agents, horizon `n`. In the scalar
model agent `i` has `mu_i in [0,1]` and `M_i in [mu_i, 1]`; when selected it chooses a target
`m in [0, M_i]` and the platform observes `Y_t ~ Bernoulli(m)`. Cost `c_{i,t} = m_{i,t} - mu_i`,
utility `u_i(n;S) = E_S[T_i(n) - C_i(n)]`, platform revenue `P(n;S) = E_S[sum_t Y_t] =
E_S[sum_t m_{I_t,t}]`. The platform observes realised rewards, never targets, means or costs.
`B_{i,n}` is the class of feasible nonanticipating behaviours. In the contextual model
`mu_i, M_i : [0,1)^d -> [0,1]` and `F_L` is the class of `L`-Lipschitz `M : [0,1)^d -> [0,1]`.

A *mechanism* is any rule that, using only the record (past selections, past realised rewards, its
own coins, the contexts when they exist, and the messages it has sent), chooses `I_t` and sends
messages. This includes MESP and every algorithm in the manuscript.

### L1 (imitation). Verified, with one hypothesis made explicit.

**Lemma L1.** Fix an agent `j`, a mechanism, and behaviours `sigma_{-j}` for the other agents that
are functions of their own histories, their own private randomness and the mechanism's messages
only, and in particular are not functions of `M_j`. Let `M' <= M` pointwise and let `sigma` be a
behaviour of `j` that is `M'`-feasible, that is, its target is at most `M'(x_{j,t})` almost surely
at every selected round. Then `sigma` is `M`-feasible, and the joint law of
`(contexts, selections, targets, rewards, mechanism coins, messages, agents' private coins)` is the
same in the instance where `j` has capacity `M` and plays `sigma` as in the instance where `j` has
capacity `M'` and plays `sigma`.

*Proof.* `M'`-feasibility gives `m <= M'(x_{j,t}) <= M(x_{j,t})` almost surely, which is
`M`-feasibility, so `sigma` is admissible in both instances. Build both probability spaces by the
same recursion: contexts from `nu`, mechanism coins, the selection `I_t` as the mechanism's
measurable function of the record, the selected agent's target as its behaviour's measurable
function of its own history and coins, and `Y_t` as `1{U_t <= m_{I_t,t}}` for a fresh uniform seed.
The capacity `M_j` enters this recursion at exactly one place, the constraint set from which the
selected agent's target is drawn, and at that place it is inactive because `sigma` already respects
the smaller constraint. Every other kernel is the same measurable function of the same arguments in
the two instances, by hypothesis on `sigma_{-j}` and by the definition of the mechanism. Two
recursions with identical kernels and identical initial data induce identical laws. `QED`

*What it does not cover.* If any other agent's rule, or the mechanism's rule, is allowed to depend
on `M_j` directly, the lemma is false and nothing below survives. This is the public information
setting of `sections/Public_information_setting.tex`, where `M_top` is known. So every impossibility
in this report is a statement about the private information setting only, and none of them
contradicts the public results. That is not a technicality: Section 5 shows the public theorem's
two-top-agents condition is exactly the escape hatch from T4.

*Where it is used.* T1, T2, T3, T4 and the corollaries. It is the only nontrivial input to all of
them; everything else is accounting.

## 2. T1: there is no uniformly valid upper confidence bound on a capacity

This is the item the brief asks me to attack hardest. My conclusion is that the raw Corollary 2 is
correct, that the suspected defect is absent, and that the true scope limit is elsewhere.

### 2.1 Statement

**Theorem T1.** Fix a mechanism, an agent `j`, a class `F` of capacity functions, a query point `y`
in the domain, a horizon `n` and `delta in [0,1)`. Let
`Mbar(y) := sup { M(y) : M in F }`. Let `U` be any `[0,1]`-valued statistic of the platform's
record after `n` rounds (any measurable function of contexts, selections, realised rewards,
messages and mechanism coins; it may depend on `n`, on `delta` and on the whole class). Suppose `F`
has the *upward cone property at `y`*: for every `M' in F` there is `M in F` with `M >= M'`
pointwise and `M(y) = Mbar(y)`. Suppose `U` is a valid upper confidence bound at `y`, that is,

    for every M in F, every M-feasible behaviour sigma of j, and every admissible sigma_{-j},
    Pr_{(M, sigma, sigma_{-j})}( U >= M(y) ) >= 1 - delta.

Then for every `M' in F`, every `M'`-feasible `sigma` and every admissible `sigma_{-j}`,

    Pr_{(M', sigma, sigma_{-j})}( U >= Mbar(y) ) >= 1 - delta ,

so `E[U] >= (1 - delta) Mbar(y)` and the expected slack obeys
`E[U - M'(y)] >= (1 - delta) Mbar(y) - M'(y)` on every instance. In particular, if
`F = F_L` or `F = F_L(mu_j) = { M in F_L : M >= mu_j }` then `Mbar(y) = 1`, and in the scalar model
with `F = [mu_j, 1]` then `Mbar = 1`: the only valid upper confidence bound is the trivial one.

*Proof.* Fix `M'`, an `M'`-feasible `sigma` and `sigma_{-j}`. The cone property gives `M in F` with
`M >= M'` and `M(y) = Mbar(y)`. Since `sigma` is `M'`-feasible it is `M`-feasible, so the validity
hypothesis applies to the pair `(M, sigma)`:
`Pr_{(M,sigma,sigma_{-j})}( U >= M(y) ) >= 1 - delta`, and `M(y) = Mbar(y)`. By L1 the law of the
record, hence of `U`, is the same under `(M, sigma)` as under `(M', sigma)`. Substituting gives the
display. The two consequences are Markov's inequality and subtraction. `QED`

**The cone property holds for the classes in play.** For `F_L`, given `M'` put
`M := max{ M', Mbar(y) - L | . - y | }` with `Mbar(y) = 1`. A maximum of two `L`-Lipschitz functions
into `[0,1]` is `L`-Lipschitz into `[0,1]`; `M >= M'`; `M(y) = 1`. For `F_L(mu_j)` the same `M`
works since `M >= M' >= mu_j`. For the scalar class `[mu_j, 1]` take `M = 1`. For the finite context
class of PROVER2 hypothesis (H1), with unrelated primitives at distinct contexts, take
`M(z) = M'(z)` for `z != y` and `M(y) = 1`.

### 2.2 The suspicion, examined

The brief suspects that smoothness constrains a capacity from above near a point where the agent has
revealed something, and therefore that the impossibility should need the query point to be far from
any revelation. It does not, and the reason is structural rather than quantitative.

Smoothness is a two sided transport: from `|M(y) - M(x)| <= L|y - x|` one gets an upper bound on
`M(y)` from an upper bound on `M(x)`, and a lower bound from a lower bound. The model never
produces an upper bound on `M(x)` at any `x`. Every observation is generated by a target
`m <= M(x)`, so every observation is a lower bound, and Lipschitz transport of lower bounds gives
lower bounds. This is why the conclusion survives at a query point where the agent revealed a
moment ago: revealing `m` at `y` certifies `M(y) >= m` and certifies nothing above `m`. The formal
form of this is T2 below, which shows the identified set after arbitrarily informative revelation is
the order filter above the revealed envelope, and that filter always contains a function equal to
the class maximum at `y`.

Three sharper forms, all proved by the same substitution.

(i) *Conditional on the record.* T1 as stated is an unconditional probability statement. The
stronger conditional version follows from L1 alone: under `(M', sigma)` and under the cone lift
`(M, sigma)` the record has the *same law*, so every record realisation with positive probability
under `M'` has the same probability under an instance whose capacity at `y` is `Mbar(y)`. No upper
bound is therefore valid even after conditioning on what was seen, and the failure is not confined
to a small probability event. T2 describes the whole set of instances consistent with a record.

(ii) *Uniform over `y`.* If `U(.)` is a function-valued statistic and the requirement is
`Pr( U(z) >= M(z) for all z ) >= 1 - delta`, take `M = Mbar` constant (in `F_L` this is
`M = 1`), which dominates every `M' in F_L`; the same substitution gives
`Pr( U == 1 ) >= 1 - delta`.

(iii) *Any monotone functional.* Nothing in the proof uses that `U` is a bound at a point. If `Phi`
is any functional on `F` that is nondecreasing for the pointwise order and `U` satisfies
`Pr(U >= Phi(M)) >= 1 - delta` uniformly, then `U >= sup_F Phi` with probability `1 - delta` on
every instance, provided the class has an upward cone for `Phi`. Applying it to
`Phi(M) = max_i M_i` shows that no valid upper bound on `M_top` exists either.

### 2.3 What T1 does not cover, and which mechanisms escape it

This is the section the `separation` failure mode demands. `separation/REPORT.md` and its
`ADVERSARY.md` record a theorem whose every step was correct and whose headline was false because
the class it defined was not the class it claimed to characterise. The analogous error here would be
to write "capacities cannot be estimated" or "optimism is impossible". Both are false. The exact
content is narrower, in five ways.

1. **It is about validity against arbitrary behaviour, not validity at a profile.** The hypothesis
quantifies over pairs `(M, sigma)` with `sigma` `M`-feasible. If instead one demands validity only
along a *prescribed* profile, that is, only for the pairs `(M, sigma^*(M))` where `sigma^*` is the
behaviour the mechanism proposes and which depends on `M`, then the substituted pair
`(M, sigma^*(M'))` is outside the requirement and the proof stops. This is not a loophole, it is how
the manuscript's own mechanism works: under `S^*` every agent delivers `M_i` during Stage 1, so
`beta_i + s_n` is a perfectly valid upper confidence bound on `M_i` at the proposed profile, with
probability `1 - n^{-4}` by Hoeffding. MESP therefore *does* use an upper bound, and T1 explains why
it may use it only in the equilibrium and revenue parts of `thm:private-mesp` and not in the
robustness part, which must hold for every feasible behavioural profile. I checked
`sections/Private_information_setting.tex` and the proof skeleton for a violation of this rule and
did not find one: the only upper tail used under arbitrary behaviour is an upper tail on the
empirical mean of the *capacity bid* `beta_i^max`, which is a concentration statement about
`L_n` Bernoulli draws of a fixed mean, not an inference about an unknown capacity from data.

2. **It says nothing about lower bounds.** Lower confidence bounds on a capacity are available and
cheap: any realised delivery is one, and T2 gives the sharpest one. The asymmetry, not the
difficulty, is the content.

3. **It says nothing about the delivered mean.** The quantity `beta_i` estimates the mean delivered
during bidding; that is an ordinary Bernoulli mean and two sided confidence intervals for it are
valid under arbitrary behaviour as long as the targets are predictable. T1 concerns the capacity,
which is the constraint set, not the realised parameter.

4. **A Bayesian escapes it.** Put a prior on `F` and condition on the record. The posterior is a
proper distribution on the order filter of T2 and its upper credible quantiles are non-trivial. What
T1 kills is *frequentist uniform* validity: a Bayesian upper quantile has no coverage guarantee
uniformly over `F`, because the coverage failure is concentrated exactly on the instances that
imitate. A referee who asks "why not Thompson sampling" should be answered this way and not with
T1 alone.

5. **A different observation channel escapes it.** If the platform observed refusals, that is, if an
agent that cannot meet an announced price were distinguishable from one that will not, an upper
bound would be available by revealed preference. In this model it is not, because a target below
the price is feasible for every capacity. If the manuscript ever adds a participation or opt out
action, T1 must be restated.

*A natural mechanism that escapes it.* Any mechanism whose guarantees under arbitrary behaviour use
capacities only through lower bounds. MESP is one, by construction: the price `tau = (beta_(2) -
s_n)_+` is built from the runner-up's realised deliveries and is compared against the winner's
capacity through the auction inequality `beta_(2) <= beta_W`, never through an estimate of `M_W`.

### 2.4 The reviewer question it answers

*Why is standard optimism, an upper confidence bound, unavailable here, when it is the default tool
in every neighbouring literature?* Because in a stochastic bandit the observed mean concentrates
around a fixed parameter from both sides, while here it concentrates around a target the agent
chose, and the capacity is only the constraint set from which the target was drawn. T1 says the
gap between the two is not a matter of a worse rate: no statistic is a valid upper bound at any
confidence level below one, at any query point, for any horizon, under any mechanism. The mechanism
therefore replaces optimism by incentive: the auction gives the agent a reason to reveal, and the
monitor makes over-revelation costly, which is the only way an upper bound can be obtained at all.
It also answers a second question, *why is an elicitation phase needed at all*, jointly with T3.

## 3. T2: what is identified is the order filter above the revealed envelope

The raw Proposition 3 proves an equality of *constraint* sets: the capacity functions compatible
with observed targets are those dominating the envelope. That is not yet an identification claim,
because compatibility with the constraints does not by itself say the observation is equally likely.
I add that half. I also keep the raw proposition's deliberate handicap, which is the right modelling
choice: give the platform the realised targets, which it does not have, so that the conclusion is an
upper bound on what any platform could know.

**Theorem T2.** Fix `L > 0` and `F_L`. Suppose that in some execution agent `j` was selected at
contexts `x_1, ..., x_r` and chose targets `m_1, ..., m_r`, and let `D` denote the realised record
together with these targets. Define the *revealed envelope*

    E(y) := max_{q <= r} ( m_q - L |y - x_q| )_+ ,     with E := 0 if r = 0 .

Then:

(a) `E in F_L`, and `{ M in F_L : m_q <= M(x_q) for all q } = { M in F_L : M >= E }`;

(b) for every `M in F_L` with `M >= E` there is an `M`-feasible behaviour `sigma_M` of agent `j`
under which `D` has exactly the same probability as under the behaviour that generated it, with the
mechanism and the other agents unchanged. Hence the set of capacity functions that are
observationally equivalent given `D` is exactly the order filter `{ M in F_L : M >= E }`;

(c) the platform's actual identified set, based on the record without the targets, contains this
filter.

*Proof.* (a) If `m_q <= M(x_q)` for all `q` then for every `y` and every `q`,
`M(y) >= M(x_q) - L|y - x_q| >= m_q - L|y - x_q|`, and `M >= 0`, so `M >= E`. Conversely if
`M >= E` then `M(x_q) >= E(x_q) >= m_q`. Each `y -> (m_q - L|y - x_q|)_+` is `L`-Lipschitz with
values in `[0,1]`, and a finite maximum of `L`-Lipschitz functions is `L`-Lipschitz, so `E in F_L`.

(b) Let `sigma_0` be the behaviour that generated `D`. Define `sigma_M` to play, at a history `h`
whose current context is `x`, the target `min{ sigma_0(h), M(x) }`. This is nonanticipating,
measurable, and `M`-feasible. Along every prefix of `D` the truncation is inactive, because the
target played there was some `m_q` and `m_q <= E(x_q) <= M(x_q)` by (a) and by `E(x_q) >= m_q`
(take the index `q` in the maximum). The probability of `D` is a product of the mechanism's kernels,
the other agents' kernels and the Bernoulli seeds along the prefixes of `D`, all of which are
unchanged, and of agent `j`'s own kernels along those prefixes, which are unchanged because the
truncation is inactive. So `Pr_{(M, sigma_M)}(D) = Pr_{(M_0, sigma_0)}(D)`. Conversely if `M` fails
`M >= E` then by (a) some `m_q > M(x_q)`, so `D` is not `M`-feasible and has probability zero.

(c) The record without the targets is a function of `D`, and a coarser observation cannot shrink the
set of instances that reproduce it. `QED`

**Four consequences.**

(i) *The knowledge set is an upper set with a least element and no greatest element below the class
maximum.* This is T1 restated structurally: since `max{E, 1 - L|. - y|} in F_L` dominates `E`, the
filter always contains an instance with capacity `1` at any prescribed `y`.

(ii) *Smoothness propagates lower bounds and only lower bounds.* One revelation of value `m` at `x`
certifies `M >= m - L|. - x|` on a ball and certifies nothing above. A continuum is therefore the
regime in which a single revelation is worth a neighbourhood; on a finite context set with unrelated
primitives a revelation at `z` is worth nothing at `z' != z`. I checked the direction of this claim
against `sections/setting.tex`, where the contextual primitives are Lipschitz in the agent's own
coordinate, and it is the right direction.

(iii) *The agent chooses the envelope, up to the fill distance of the design.* The pairs
`(x_q, m_q)` are chosen by the agent inside `[0, M(x_q)]`. For any `E_0 in F_L` with `E_0 <= M` the
agent can deliver `m_q = E_0(x_q)`, and then for every `y`, writing
`rho(y) := min_q |y - x_q|`,

    ( E_0(y) - 2 L rho(y) )_+  <=  E(y)  <=  E_0(y) .

*Proof.* Upper: `E_0(x_q) - L|y - x_q| <= E_0(y) + L|y-x_q| - L|y-x_q| = E_0(y)` and `E >= 0`.
Lower: with `q*` a nearest design index, `E(y) >= (E_0(x_{q*}) - L rho(y))_+ >=
(E_0(y) - 2 L rho(y))_+`. `QED`
So up to `2L` times the fill distance of the elicitation design, the agent dictates what the
platform learns, and the platform's only defence is the resolution of its own design. This is what
turns T2 into the covering statements T5 and T6.

(iv) *The platform learns willingness, not capacity.* If a behaviour `sigma` of agent `j` has
targets almost surely at most a level `c`, then `min{M, c} in F_L` whenever `M in F_L`, `sigma` is
`min{M,c}`-feasible, and by L1 the record has the same law as if the capacity were `min{M, c}`. So
no statistic distinguishes `M` from `min{M, c}`. Whatever the mechanism observes is capped by the
highest target the agent ever chose to play, and that is a decision of the agent, not of the
estimator.

**What T2 does not cover.** It is a statement about a single agent and about `F_L`; for a class
without the upward cone property the filter has a different top. It assumes the platform knows `L`;
if `L` is unknown the filter is larger, not smaller, so the negative direction is unaffected. It
gives no rate: it says which functions are indistinguishable, not how much revenue that costs. It
does not cover the intrinsic means `mu_i`, whose identification has a different structure because
honest agents are constrained from below by `mu_h` rather than from above.

**The reviewer question it answers.** *Why does the mechanism need an elicitation phase at all,
rather than learning capacities from the rewards it already observes?* Because the record identifies
only the filter above the envelope, and by (iii) and (iv) the envelope is the agent's choice, capped
by whatever level the agent had a reason to deliver. Rewards already observed are evidence about
willingness at the prices already offered, not about capacity. T3 turns this into a statement with
no rationality assumption in it at all.

## 4. T3: no revelation without allocation feedback

T1 and T2 say the platform cannot infer an upper bound. T3 says something the raw material does not
contain and that a referee will find more concrete: under a mechanism that allocates without looking
at rewards, the record contains *no information whatever* about any capacity, not merely no upper
bound. There is no rationality assumption beyond utility maximisation, no equilibrium, and no class
of capacity functions.

**Theorem T3.** Fix `n`, `K` and a mechanism whose selections and messages are measurable functions
of the round index, the contexts, and the mechanism's own coins only, and not of the realised
rewards. Then

(a) for every strategic agent `i` and every capacity `M_i`, the behaviour `sigma_i^0` that targets
`0` whenever selected maximises `u_i(n; .)` over `B_{i,n}` for every profile of the other agents;
for an honest agent `h` the behaviour that targets `mu_h` maximises `u_h` over honest behaviours;

(b) under the profile in which every agent plays the maximiser of (a), the law of the platform's
record is the same for every capacity profile `(M_1, ..., M_K)` in the model, so no statistic of the
record distinguishes any two capacity profiles;

(c) consequently no amount of such exploration, of any length up to `n`, identifies anything about
any capacity, however many rounds are spent and however small the noise.

*Proof.* (a) Because the selections are a fixed measurable function of the round, the contexts and
the mechanism's coins, the random variable `T_i(n)` and the set of rounds at which `i` is selected
have the same law under every behaviour of `i`. Hence `u_i = E[T_i] - E[C_i]` with `E[T_i]` a
constant, and `C_i = sum_{t: I_t = i} (m_{i,t} - mu_i)` is minimised pathwise, round by round, by
taking `m_{i,t}` as small as feasible, that is `0` for a strategic agent and `mu_i` for an honest
one. (b) Under that profile agent `i`'s targets are the constant `0`, respectively `mu_i`, which is
feasible for capacity `0`, respectively `mu_i`. Apply L1 once per agent, replacing `M_i` by that
constant while the other agents' behaviours, which do not depend on `M_i`, stay fixed. After `K`
applications the record has the law of the instance with capacity profile `(0 or mu_i)_i`, which
does not depend on the true capacities. (c) Immediate from (b). `QED`

**What it does not cover.** It assumes the allocation ignores rewards *throughout the horizon*.
Round robin, any fixed schedule, any explore then commit schedule whose exploration phase is fixed
in advance *and whose continuation ignores the exploration rewards*, and any context-only rule all
satisfy this. It does not cover UCB, EXP3, or MESP. It says nothing about instances where agents are
not utility maximisers; a behaviourally noisy agent may reveal by accident, which is precisely why
the manuscript's robustness statement is against arbitrary behaviour and not a prediction.

**The exact use for the paper.** MESP's Stage 1 is round robin, so *the elicitation block by itself*
falls under T3: if the mechanism stopped there, its `L_n` pulls per agent would be worth nothing.
What makes the block informative is that the Stage 1 record determines who wins Stage 2 and at what
price. So the elicitation phase is not an estimation device that a better estimator could shorten or
delete, and it is not a sampling budget: it is the only place in the mechanism where an agent has a
reason to reveal. This is the precise sense in which Route 4 of the F1 brief ("derive the price from
other agents' ongoing realised performance and delete the bidding block") fails, and it is a
stronger reason than the one recorded in EXPLORER Section 2.6 item 3.

**The reviewer question it answers.** *Why an elicitation phase, rather than learning capacities
from the rewards the mechanism already observes?* Because an observation is informative only to the
extent that the allocation rule made it worth producing. Under a reward-blind allocation the
information content is exactly zero, by T3; under a reward-sensitive allocation it is bounded by the
agent's willingness at the incentives offered, by T2 (iv); and an upper bound is never available, by
T1.

## 5. T4: the rent transfer theorem, and why the benchmark is the second capacity

This is the result I would put first in the paper. It is new here, it is not in the raw material,
and a version of it is known in a neighbouring model (Braverman, Mao, Schneider and Weinberg, COLT
2019, Lemma 14); Section 9 states exactly what is theirs and what is not.

### 5.1 The family and the hypotheses

Fix `K >= 2` and `V in [0,1)`. For `c in [V, 1]` let `I(c)` be the scalar instance with

    mu_i = 0 for every i ,   M_1 = c ,   M_j = V for j = 2, ..., K ,

honest set `K_H = [K]` (with `mu_i = 0` the honesty constraint `m >= mu_i` is vacuous, so this is
legal in the model of `sections/setting.tex` and imposes nothing on any agent). In `I(c)` the top
capacity is `max(c, V)` and the second capacity is `M_(2) = V` whenever `c >= V`.

Fix a mechanism and a family of proposed profiles `S^*(c)`, one per instance, and assume

**(PVM) private value measurability.** For every `j != 1`, the prescribed behaviour `S^*_j(c)` does
not depend on `c`.

(PVM) is not a restriction in substance: an agent knows its own capacity and not the others', so a
profile that instructed agent `j` to condition on `M_1` would not be implementable. Every direct
revelation mechanism satisfies it, since the prescribed report is a function of the agent's own
capacity. MESP satisfies it: `S^*_i` is "deliver `M_i` in bidding and fallback, deliver
`min{tau, M_i}` as primary winner", which reads only `M_i` and the announced price.

### 5.2 Statement

**Theorem T4 (rent transfer).** Fix `V < c <= M <= 1`, a mechanism and a family satisfying (PVM).
Write `N_1(c) := E_{S^*(c)}[T_1(n)]` and `A_1(c) := E_{S^*(c)}[sum_{t : I_t = 1} m_{1,t}]` on
`I(c)`. Suppose

  (H1) *revenue at the lower instance*: `P(n; S^*(c)) >= f n - R(n)` on `I(c)`, for some
  `f in [V, 1]` and `R(n) >= 0`;

  (H2) *equilibrium at the upper instance, against one deviation*: on `I(M)`,
  `u_1(n; S^*_1(c), S^*_{-1}) - u_1(n; S^*(M)) <= Delta(n)`.

Then

    P(n; S^*(M))  <=  n  -  ((1 - c)/(c - V)) ( (f - V) n - R(n) )  +  Delta(n) .

*Proof.* Throughout, `mu_1 = 0`, so `C_1 = sum_{t : I_t = 1} m_{1,t}` and `u_1 = N_1 - A_1`.

*Step 1 (revenue accounting, valid at every instance of the family).* Every agent `j != 1` has
`M_j = V`, so `m_{j,t} <= V` at every round it is selected. Hence
`P = E[sum_t m_{I_t,t}] <= A_1 + V (n - N_1)`.

*Step 2 (the lower instance forces pulls).* On `I(c)` we have `m_{1,t} <= c`, so `A_1(c) <= c N_1(c)`.
With Step 1 and (H1),
`f n - R <= c N_1(c) + V n - V N_1(c)`, that is `N_1(c) >= ((f - V) n - R)/(c - V)`.

*Step 3 (pulls at a low capacity are rent).* Again `A_1(c) <= c N_1(c)`, so
`u_1(n; S^*(c)) = N_1(c) - A_1(c) >= (1 - c) N_1(c) >= ((1-c)/(c-V)) ((f - V) n - R)`.

*Step 4 (imitation transfers the rent to the upper instance).* Read `S^*_1(c)` as the *instantiated*
behaviour of the capacity `c` agent, that is, the concrete map from histories to targets that the
profile prescribes once `c` is substituted, and not as a parametric rule such as "deliver your own
capacity"; the instantiated map is an element of `B_{1,n}` whenever its targets are feasible, and
agent 1 can execute it because it knows `c` and `c <= M`. Its targets are at most `c <= M`, so it is
feasible for capacity `M`. By (PVM) the other
agents play the same `S^*_{-1}` in `I(c)` and in `I(M)`, and their rules do not read `M_1`. By L1,
applied to agent 1 with the smaller capacity `c` and the larger capacity `M`, the joint law of the record *including agent 1's own targets* is the same
under `(I(M), (S^*_1(c), S^*_{-1}))` as under `(I(c), S^*(c))`. Since `u_1 = E[T_1 - C_1]` is the
expectation of a functional of that law, and `mu_1 = 0` in both instances, the two utilities are
equal. Now (H2), whose slack I write `Delta(n)`, gives `u_1(n; S^*(M)) >= u_1(n; S^*(c)) - Delta(n)`.

*Step 5 (rent caps revenue at the upper instance).* On `I(M)`, by Step 1 and `u_1 = N_1 - A_1`,
`P(n; S^*(M)) <= A_1(M) + V(n - N_1(M)) = V n + (1 - V) N_1(M) - u_1(n; S^*(M))`, and
`N_1(M) <= n`, `1 - V > 0`, so `P(n; S^*(M)) <= n - u_1(n; S^*(M))`.

Chaining Steps 5, 4 and 3 gives the display. `QED`

### 5.3 Corollaries

**C1 (full extraction at one level caps revenue at every higher level).** Take `f = c` in (H1). Then
`(1-c)(f - V)/(c - V) = 1 - c` and

    P(n; S^*(M))  <=  c n  +  ((1-c)/(c-V)) R(n)  +  Delta(n) .

In words: if the mechanism delivers the full capacity as revenue at capacity level `c`, then at
*every* higher capacity level its revenue is at most `c n`, up to the guarantee error and the
equilibrium slack. Extraction at a low type is paid for at every high type.

**C2 (the top capacity is not an attainable benchmark).** Suppose a mechanism guarantees
`P(n; S^*(c)) >= c n - o(n)` at every `c in (V, M]` for some `M > V`, with equilibrium slack `o(n)`
at `I(M)`. Fix `eta in (0, M - V)` and apply C1 at `c = V + eta`: `P(n; S^*(M)) <= (V + eta) n +
o(n)`. Letting `n -> infinity` and then `eta -> 0`,

    limsup_n  P(n; S^*(M)) / n  <=  V  =  M_(2) .

Since the guarantee claims `P(n; S^*(M)) >= M n - o(n)` and `M > V`, no such mechanism exists. The
deficit is the whole gap `M_top - M_(2)`, not a constant fraction of it.

**C3 (the quantitative trade-off for an intermediate benchmark).** Suppose the mechanism guarantees
`P(n; S^*(c)) >= (alpha c + (1 - alpha) V) n - o(n)` at every `c in (V, M]`, with `alpha in [0,1]`,
and equilibrium slack `o(n)` at `I(M)`. Then

    alpha  <=  (1 - V) / (1 + M - 2 V) ,   in particular   alpha <= 1/2 when M = 1 .

*Proof.* The theorem with `f = alpha c + (1-alpha)V` gives
`limsup P(M)/n <= 1 - alpha (1 - c)` for every `c in (V, M]`; let `c` decrease to `V` to get
`limsup P(M)/n <= 1 - alpha(1 - V)`. The guarantee at `c = M` gives
`alpha M + (1-alpha) V <= 1 - alpha(1 - V)`, which rearranges to the display. `QED`

**C4 (MESP sits at the ceiling C2 identifies).** MESP's benchmark is `alpha = 0`, that is
`f(c) = M_(2)`, for which the trade-off inequality is vacuous and C2 is silent. So the manuscript's
benchmark is the largest one in the family `alpha c + (1 - alpha) M_(2)` for which T4 imposes no
loss at all, and by C2 the natural larger benchmark `M_top` is impossible. This is the exact answer
to the reviewer question.

### 5.4 What T4 does not cover, and the natural mechanisms that escape it

This is the part most exposed to the `separation` failure mode, so I state the escapes explicitly.

1. **It does not show `M_(2)` is the exact maximum.** C3 leaves `alpha` up to `1/2` unrefuted when
`M = 1, V = 0`. I checked whether the linear relaxation used in the proof can be tightened and it
cannot: the constraints actually used, namely `u_1(c) >= (1-c) N_1(c)`, `A_1(c) <= c N_1(c)`,
`N_1(c) <= n`, monotonicity of `u_1` along the family, and the per instance revenue accounting, are
jointly satisfiable with `alpha = (1-V)/(1 + M - 2V)` and infeasible just above it, which I
verified numerically on a grid of instances (`scratchpad/round2/h1-impossibility/check3.py`; the
contradiction of C2 is checked in `check.py`). Closing the gap needs a constraint I do not have.
Braverman et al. close the analogous gap in their model using incentive constraints *in both
directions* along a ladder of instances; in our model upward imitation is infeasible, since an agent
of capacity `c` cannot execute a behaviour that targets above `c`, so their chain does not transfer.
I do not claim `M_(2)` is optimal. I claim `M_top` is impossible and the trade-off C3 holds.

2. **It needs a unique agent above `V`, and competition is the escape.** The family `I(c)` has one
agent with capacity above `V`. If instead two agents have capacity `M`, then at the imitating
instance the second top agent can still supply `M`, the mechanism can set `N_1 = 0`, and Step 3
gives no rent: the bound becomes vacuous. That is exactly the content of the two-top-agents
condition in the manuscript's public result and in `Condition 5.6` of Esmaeili, Shin and Slivkins
(2025). Note also that when two agents tie at the top, `M_(2) = M_top`, so the ceiling of C2 *is*
the top capacity and nothing is lost. T4 and the public theorem are therefore two faces of one
statement, and I would say so in the paper.

3. **It needs the guarantee to be a family guarantee.** A mechanism that is told `M_top` in advance,
or one whose guarantee is asserted only at a single instance, is untouched. This is the second
reason the public information results are not contradicted: there L1 itself fails, because the
mechanism reads `M_top`.

4. **It uses `mu_i = 0`.** With general `mu_1` the rent identity becomes
`u_1 = (1 + mu_1) N_1 - A_1` and Step 5 weakens to `P <= (1 + mu_1) n - u_1`, so the conclusion
carries an extra `mu_1 n`. The instances used are legal in the model, so the impossibility stands,
but it is an impossibility for *some* instance family, not for every one, which is all a benchmark
claim needs to be refuted.

5. **It bounds revenue at the proposed profile only.** It says nothing about revenue at other
equilibria, and nothing about the honest benchmark part of `thm:private-mesp`.

6. **(H2) is used only against one deviation.** This makes T4 stronger, not weaker: any notion of
equilibrium that contains `B_{1,n}`, including the additive behavioural equilibrium of
`sections/setting.tex`, supplies (H2).

### 5.5 The reviewer question it answers

*Why is the revenue benchmark the second highest capacity rather than the highest?* Because a
mechanism that extracted the highest would have to extract the full capacity at every lower instance
too, if its guarantee is to be a benchmark rather than a single instance claim; and extracting the
full capacity at a low instance forces the mechanism to keep pulling the only agent that can beat
`M_(2)`, which hands that agent a rent of `(1 - c)` per pull; and by L1 the high capacity agent can
take that rent by imitation. C2 says the resulting revenue at the top instance is at most
`M_(2) n + o(n)`. The second capacity is not a modelling convenience, it is the rent free level.

## 6. T5 and T6: elicitation is a covering problem, in sup norm and on average

The raw Proposition 4 is correct. I verified every step: the two functions are `L`-Lipschitz with
values in `[0, 2 eps] subset [0,1]` when `eps <= 1/4`; they agree at every design point because
`L |x_q - y| > eps`; a recovery map receiving identical data outputs the same function, so one of
the two errors is at least `eps/2`; and the volume step is valid because a Euclidean ball of radius
`eps/L` is contained in a cube of side `2 eps/L`, so `N (2 eps/L)^d >= 1`. The hypothesis
`L >= 4 eps` is used only to make the conclusion non-vacuous. Two things must be added before it can
answer a reviewer.

### 6.1 T5: the sup-norm bound, extended to adaptive designs

The raw statement fixes the design in advance. A referee's first reply to "you must elicit
everywhere" is "use an adaptive design". The same proof handles that, by choosing the hard instance
after seeing where the algorithm looked.

**Theorem T5.** Fix `eps in (0, 1/4]`, `L >= 2 eps`, `d >= 1`, and put `m := floor(L/(2 eps)) >= 1`
and `N := m^d`. Let `Alg` be a deterministic procedure that queries at most `r` points of
`[0,1)^d` adaptively (each query may depend on all previous queries and on the exact values
`M(x_1), ..., M(x_{q-1})` returned) and then outputs a function `hat M`. If

    sup_{M in F_L}  || hat M - M ||_infinity  <  eps / 2 ,

then `r >= N = floor( L / (2 eps) )^d`. If `Alg` is randomised, then `r <= N/2` forces
`sup_{M in F_L} E || hat M - M ||_infinity >= eps / 4`.

*Proof.* Partition `[0,1)^d` into `N` cubes of side `rho := 1/m` with centres `z_k`, and note
`eps/L <= 1/(2m) = rho/2`, so the balls `B_k := B(z_k, eps/L)` are contained in their cubes and are
pairwise disjoint. Run `Alg` on `M_1 :≡ eps`; every answer is `eps`, so in the deterministic case
the queries `x_1, ..., x_r` are fixed. Call a cell *clean* if no query lies in its ball `B_k`; at
most `r` cells are unclean, so if `r < N` some cell `k` is clean. Put
`M_2(.) := eps + ( eps - L |. - z_k| )_+`, which lies in `F_L`, takes values in
`[0, 2 eps] subset [0,1]`, and vanishes outside `B_k`. By induction on the query index, the run of
`Alg` on `M_2` makes the same queries and receives the same answers as the run on `M_1`, because
every query point misses `B_k`. So the output `g` is the same on both instances, while
`M_2(z_k) - M_1(z_k) = eps`, whence
`max{ ||g - M_1||_inf, ||g - M_2||_inf } >= eps/2`, a contradiction. Hence `r >= N`.

For a randomised `Alg` the clean set depends on the coins. Let `p_k` be the probability that cell
`k` is clean in the run on `M_1`. Since the balls are disjoint, the expected number of unclean cells
is at most `r`, so `sum_k p_k >= N - r >= N/2`, and some cell `k` has `p_k >= 1/2`. Build `M_2` from
that cell. On the event that `k` is clean, the two runs coincide and the outputs agree, so
`||g - M_1||_inf + ||g - M_2||_inf >= eps` there; taking expectations,
`E_{M_1}||g - M_1||_inf + E_{M_2}||g - M_2||_inf >= eps p_k >= eps/2`. `QED`

*Remark.* The bound `floor(L/(2 eps))^d` is exactly the raw Proposition 4's conclusion, reached
without the volume computation and without assuming the design is fixed in advance. The raw
hypothesis `L >= 4 eps` is what makes `m >= 2`, that is, what makes the conclusion say more than
"at least one query".

### 6.2 T6: the average-error bound, which is the one the revenue objective needs

Sup-norm recovery is not what the mechanism needs. Revenue loss is
`E_{X ~ nu} [ M_(2)(X) - tau(X) ] n`, an average, so a referee can object that a mechanism may be
inaccurate on a small region at no cost. The following says the count is the same up to a constant:
you must elicit in a constant fraction of the regions, not merely somewhere.

**Theorem T6.** Fix `L > 0`, `d >= 1`, an integer `m >= 1` and `rho := 1/m` with `L rho / 2 <= 1`.
Let `Alg` be any adaptive procedure as in T5 making at most `r <= m^d / 2` queries, with noiseless
answers, and outputting `hat M`. Then

    sup_{M in F_L}  E || hat M - M ||_{L^1([0,1)^d)}  >=  ( L omega_d / (2^{d+3} (d+1)) ) rho ,

where `omega_d` is the volume of the Euclidean unit ball. Consequently, writing
`X := L omega_d / ( 2^{d+3} (d+1) eps )`, if the worst-case average error is below `eps` and
`X > 2` and `L <= 2 m` for the integer `m := ceil(X) - 1`, then

    r  >  (1/2) ( X - 1 )^d ,

which is `c_d (L/eps)^d` up to lower order, with `c_d` depending only on `d`.

*Proof.* Partition `[0,1)^d` into `N := m^d` cubes of side `rho` with centres `z_k`, and set
`b_k(y) := ( L rho/2 - L |y - z_k| )_+`, supported in the ball `B_k := B(z_k, rho/2)`, which is
inscribed in the `k`th cube; the supports are pairwise disjoint. For `S subset [N]` put
`M_S := sum_{k in S} b_k`.

*`M_S in F_L`.* Values lie in `[0, L rho/2] subset [0,1]`. For the Lipschitz property, take `y, y'`.
If they lie in the same `B_k` or if at most one of them lies in any ball, the bound is that of a
single `b_k`, which is `L`-Lipschitz. If `y in B_k` and `y' in B_j` with `j != k`, let `p` and `q`
be the points where the segment `[y, y']` leaves `B_k` and enters `B_j`; then
`|M_S(y) - M_S(y')| <= b_k(y) + b_j(y') = (b_k(y) - b_k(p)) + (b_j(y') - b_j(q)) <= L |y - p| +
L |q - y'| <= L |y - y'|`, since `p` and `q` lie on the segment in this order and the balls are
disjoint.

*The data cannot see a cell it never queried.* Let `S` be uniform on the subsets of `[N]`,
independent of the procedure's coins `w`. For `k in [N]` let `A_k` be the event that the run on
`M_S` makes no query inside `B_k`. If `A_k` holds then, by induction on the query index, the run on
`M_{S xor {k}}` makes exactly the same queries and receives exactly the same answers, because `M_S`
and `M_{S xor {k}}` differ only inside `B_k`; in particular `A_k` also holds for `S xor {k}`, so
`A_k` is a function of `w` and of the coordinates of `S` other than `k`, and the two runs output the
same `hat M`.

*Assouad averaging.* Fix `w` and the coordinates of `S` other than `k`, and average over the two
values of the `k`th coordinate. On `A_k` the two outputs agree, so
`int_{B_k} |hat M - M_S| + int_{B_k} |hat M - M_{S xor {k}}| >= int_{B_k} b_k = ||b_k||_1`, and the
average of the two terms is at least `1_{A_k} ||b_k||_1 / 2`. Taking expectations and summing over
`k`,

    E || hat M - M_S ||_{L^1}  >=  (1/2) ||b_k||_1 sum_k Pr(A_k) .

Since the balls `B_k` are pairwise disjoint, the number of `k` for which a query lands in `B_k` is
at most the number of queries, so `sum_k (1 - Pr(A_k)) <= r` and `sum_k Pr(A_k) >= N - r >= N/2`.
Hence `E ||hat M - M_S||_{L^1} >= (N/4) ||b_k||_1`, and a supremum over `S` dominates the average.

*The bump mass.* In polar coordinates with `R := rho/2`,
`||b_k||_1 = L int_{B(0,R)} (R - |y|) dy = L S_{d-1} int_0^R (R - t) t^{d-1} dt =
L S_{d-1} R^{d+1} / (d (d+1)) = L omega_d R^{d+1} / (d+1)`, using `S_{d-1} = d omega_d`. I checked
this formula against Monte Carlo integration in `d = 1, 2, 3`
(`scratchpad/round2/h1-impossibility/check2.py`; agreement to four digits).

So `E_S ||hat M - M_S||_1 >= (N/4) L omega_d (rho/2)^{d+1}/(d+1) = L omega_d rho /
(2^{d+3} (d+1))`, using `N = rho^{-d}`, and a supremum dominates an average. This is the first
display. For the second, the first display is a contradiction with "average error below `eps`"
whenever `r <= m^d/2` and `L omega_d/(2^{d+3}(d+1) m) > eps`, that is whenever `m < X`. Taking
`m = ceil(X) - 1`, which is at least `X - 1` and at least `1` when `X > 2`, and whose hypothesis
`L rho/2 <= 1` reads `L <= 2m`, gives `r > m^d/2 >= (X-1)^d/2`. `QED`

### 6.3 What T5 and T6 do not cover

1. **They bound the number of elicitation *locations*, not the number of pulls.** They assume
noiseless exact revelation of `M` at the queried points, which is far more than the platform gets.
So they are lower bounds on a quantity the mechanism must pay, and they compose with a per location
cost only if that cost is separately justified. The standard Bernoulli count `eps^{-2}` pulls per
location is *not* proved here and I do not claim it. With it granted, the total is
`Theta(K L^d eps^{-(d+2)})` and balancing against the `n eps` price error gives
`eps = Theta(n^{-1/(d+3)})` and `Theta(n^{(d+2)/(d+3)})`, which is the manuscript's exponent; the
covering half of that arithmetic is proved, the Bernoulli half is not.

2. **They are statements about recovering `M`, not about setting a price.** A mechanism does not
have to estimate a capacity to price: it has to charge a price that is a lower bound at the contexts
where it binds. A mechanism that charges `0` in the unelicited regions is accurate in the safety
sense and merely loses the revenue there. So the honest reading is: on a region where no elicitation
happened, the mechanism must either lose revenue or charge a price it cannot certify. T6 quantifies
the first branch; T1 is what closes the second. A fully joint statement, "any safe mechanism loses
`Omega(L rho)` per unit mass on unelicited regions", needs a definition of safety that I did not
want to invent, and I did not prove it.

3. **They do not cover interpolation from a *model*.** If the capacity class were parametric, for
instance linear in the context with `p` parameters, the covering count collapses to `p` and nothing
here applies. The manuscript's class is Lipschitz, which is exactly the assumption that makes the
count exponential in `d`. A referee who dislikes the rate is really objecting to the class.

4. T6 is stated for the Lebesgue measure; for a general context law `nu` with a density bounded
below on its support the same proof gives the same bound with a constant depending on that lower
bound, and for a `nu` concentrated on a low dimensional set it fails, correctly.

### 6.4 The reviewer question they answer

*Why is exploration paid in every region rather than interpolated from neighbouring regions?*
Because interpolation is exactly what the envelope of T2 already does, and T2 (iii) shows the
interpolant is a lower bound whose error is `2 L` times the fill distance; T6 shows that error is
unavoidable on a constant fraction of the space unless a constant fraction of the regions is
elicited, even with noiseless data and an adaptive design. The exponential dependence on `d` is a
property of the Lipschitz class, not of the mechanism.

## 7. T7: a one sided bound on a Bernoulli mean must shade by the sampling scale

T1 says the price cannot be built from an upper bound. It must therefore be built from a lower
bound, and MESP builds it as `tau = (beta_(2) - s_n)_+` with
`s_n = sqrt( log(2 K n^4) / (2 L_n) )`. A referee will ask whether the shading `s_n`, which costs
`n s_n` in revenue, is an artefact of Hoeffding. It is not, up to the logarithm.

**Theorem T7.** Let `L >= 1` be an integer, `delta in [0, 1/2)`, and let `hat B : {0,1}^L -> [0,1]`
be any statistic of `L` independent Bernoulli draws such that

    for every p in [0,1],   Pr_p( hat B <= p ) >= 1 - delta .

Put `eps := 1/(4 sqrt L)`. Then

    Pr_{1/2}( hat B <= 1/2 - eps )  >=  1 - delta - sqrt(1/8)  >=  0.646 - delta .

If in addition `delta <= eps/2` and `eps <= 1/10`, then
`E_{1/2}[ 1/2 - hat B ] >= 0.34 eps = 0.085 / sqrt L`.

*Proof.* Write `Q` for the law of `L` draws at `p = 1/2` and `P` for the law at `p' = 1/2 - eps`.
For Bernoulli laws, `KL( Bern(p') || Bern(1/2) ) <= chi^2( Bern(p') || Bern(1/2) ) =
(p' - 1/2)^2 / ( (1/2)(1/2) ) = 4 eps^2`, so by tensorisation `KL(P || Q) <= 4 L eps^2 = 1/4`, and by
Pinsker `TV(P, Q) <= sqrt( KL/2 ) <= sqrt(1/8) < 0.354`. Let `A := { hat B > p' }`. Validity at `p'`
gives `P(A) <= delta`, so `Q(A) <= delta + TV(P,Q) < delta + 0.354`, which is the first display.
For the second, validity at `p = 1/2` gives `Pr_{1/2}( hat B <= 1/2 ) >= 1 - delta`, so
`1/2 - hat B >= 0` except on an event of probability at most `delta`, on which
`1/2 - hat B >= -1/2`. Hence
`E_{1/2}[1/2 - hat B] >= eps (0.646 - delta) - delta/2 >= eps(0.646 - eps/2) - eps/4 >= 0.34 eps`
under the stated bounds on `delta` and `eps`. `QED`

**Use and scope.** The quantity MESP shades is the runner-up's Stage 1 empirical mean, and the
price must lie below the runner-up's delivered level with high probability for the bid domination
and monitoring arguments to close. T7 says any statistic with that uniform one sided validity
undershoots by `Omega(1/sqrt{L_n})` at the hardest mean, so the `n s_n` revenue term is forced at
the order `n / sqrt{L_n}`, and the only slack between T7 and MESP is the factor
`sqrt( log(2 K n^4) )`, which comes from the union bound over `K` agents and from wanting the
failure probability to be negligible against a horizon `n` of revenue. What T7 does *not* cover: a
mechanism that deliberately overprices sometimes and recovers through a fallback is not required to
have a uniformly valid one sided statistic, and is untouched. Nor does T7 say anything about `L_n`
itself.

**The reviewer question it answers (partly).** *Is the exploration cost an artefact of the analysis
or information theoretic?* Split the manuscript's `O_K(n^{2/3}(log n)^{1/3})` into its two sources.
The bidding block length `L_n` enters the equilibrium gap, and the manuscript already shows it is
attained: `prop:tightness` in `sections/appendix_private.tex` exhibits a deviation that saves
`L_n (M_i - V_i)/2`, so the `L_n` term is not an analysis artefact. The price error `n s_n` is
forced at the order `n/sqrt{L_n}` by T7 within the class of mechanisms that price from a uniformly
valid one sided statistic. Balancing `L_n` against `n / sqrt{L_n}` gives `L_n = n^{2/3}` and the
exponent `2/3`. What is *not* proved, and what I would not claim, is a lower bound over *all*
mechanisms: the correct open statement is that no mechanism can simultaneously have equilibrium
slack `o(n^{2/3})` and revenue loss `o(n^{2/3})` on every scalar instance. I did not prove it. I
note one consequence of the accounting that a referee may notice: the trade-off is between
equilibrium slack and revenue, not between revenue and revenue, since for `K = 2` the bidding rounds
themselves are not lossy against the `M_(2)` benchmark, both agents delivering at least `M_(2)`
under `S^*`.

## 8. T8: no mechanism guarantees second capacity revenue under arbitrary behaviour

This is EXPLORER Section 2.6 item 2. I verified it and record it because it is what forces the three
part shape of `thm:private-mesp`, and because it is one line.

**Proposition T8.** Fix `K >= 2` and the scalar instance `mu_i = 0`, `M_i = 1` for every `i`, with
`K_H = [K]` (honesty is vacuous at `mu_i = 0`). The profile in which every agent targets `0`
whenever selected is feasible, is honest, and lies in `prod_i B_{i,n}`. Under it `P(n; S) = 0`,
while `M_(2) n = n`. Hence no mechanism, however designed, satisfies
`P(n; S) >= M_(2) n - o(n)` for every feasible behavioural profile `S`.

*Proof.* Immediate: `P(n;S) = E_S[sum_t m_{I_t,t}] = 0`. `QED`

**Consequence for the shape of the theorem.** A revenue claim of the form `M_(2) n - o(n)` can only
be a claim *at a proposed profile*, which is exactly part (B) of `thm:private-mesp`, and the claim
that survives arbitrary behaviour must use a different benchmark, which is exactly part (C) with
`mu_H^star n`. On the instance of T8 that benchmark is `0` and is attained, so part (C) is tight
there. The three part shape is therefore forced, and I would say so in one sentence in the paper
rather than leave a referee to suspect that (B) and (C) could be merged.

## 9. Prior art

Rule 3 of `COMMON.md` requires a primary source with a URL and a date for every external paper
relied on. Everything below was checked on 18 September 2026.

### 9.1 T4 is a known result in a neighbouring model, and must be attributed

**Braverman, Mao, Schneider and Weinberg, "Multi-armed Bandit Problems with Strategic Arms",
Proceedings of the Thirty Second Conference on Learning Theory, PMLR volume 99, 2019.** Checked:
arXiv abstract page `https://arxiv.org/abs/1706.09060` (submitted 27 June 2017) and the proceedings
PDF `http://proceedings.mlr.press/v99/braverman19b/braverman19b.pdf`, which I downloaded and
converted to text.

Their Lemma 14, verbatim from the proceedings PDF: "Let `mu` and `mu'` be the largest and second
largest values respectively among the `mu_i`. Then for any constant `alpha > 0`, no truthful
mechanism can guarantee `(alpha mu + (1 - alpha) mu') T` revenue in the worst case." The sentence
before it reads: "We additionally show that the performance of Mechanism 1 is as good as possible;
no mechanism can do better than the second-best arm in the worst case", and the introduction says
"the principal can extract the value of the second-best arm (which is the best possible, as we show
in Lemma 14)".

So *the statement that the second largest is the ceiling is theirs*, and the paper must say so. What
is different here:

- *Model.* In their model an arm receives a private reward `v_a` when pulled and passes on
  `x_a <= v_a`; there is no effort cost, no target mean, no Bernoulli observation of a chosen mean,
  and no honest agents. In ours the agent chooses a mean `m <= M_i`, pays `m - mu_i`, and the
  platform sees `Bernoulli(m)`. Their `mu'` is a reward level; our `M_(2)` is a capacity.
- *Hypothesis.* Theirs is a "truthful mechanism", meaning one that induces a dominant strategy for
  each arm, and their proof (which I read) uses the incentive inequality
  `b_i x_i - p_i >= b_i x_j - p_j` in *both* directions along a ladder of `L > exp(1/alpha)`
  instances. Ours is an additive equilibrium slack `o(n)` at one instance, against one deviation,
  with no dominant strategy and no direct revelation. Upward imitation is infeasible in our model,
  so their ladder does not transfer, which is why C3 is weaker than their Lemma 14.
- *Strength.* Their Lemma 14 rules out every constant `alpha > 0`; our C2 rules out `alpha = 1`
  with an explicit deficit of the whole gap `M_top - M_(2)`, and C3 gives a quantitative ceiling
  `alpha <= (1-V)/(1 + M - 2V)` which I do not claim is tight.

**Recommended wording for the paper.** "That the second capacity, and not the top capacity, is the
right revenue benchmark is known for the strategic bandit model of Braverman et al. (2019, Lemma
14). Their argument uses two sided incentive constraints, which our capacity constrained agents do
not satisfy; Proposition [T4] gives the corresponding statement for our model, and shows in addition
that the loss is the whole gap."

### 9.2 The closest statement inside this line of work

**Esmaeili, Shin and Slivkins, "Robust Performance Incentivizing Algorithms for Multi-Armed Bandits
with Strategic Agents", AAAI 2025, 39(13), 13814 to 13822, doi `10.1609/aaai.v39i13.33510`.**
Checked: `https://arxiv.org/abs/2312.07929` and the PDF `https://arxiv.org/pdf/2312.07929`, which I
downloaded and converted to text. This is `\citet{esmaeili}` in `references.bib`.

Their Theorem 5.1: "Under any sublinear regret MAB algorithm, it is not a dominant strategy for an
arm `i` to follow the maximum performance strategy `S^*_i`", with the stated intuition that the arm
prefers to lower its performance to only outperform the second highest agent. Their Section 5.1
shows non-existence of sub-optimal revenue equilibria for large `k_top` under their Condition 5.6,
which lower bounds the number of top arms.

Relation to this report. Theorem 5.1 is about dominant strategies under a sublinear regret bandit
algorithm, not about a revenue ceiling for an arbitrary mechanism, so it does not subsume T4; it is
the same economic force seen from the equilibrium side. Their Condition 5.6 is the same escape hatch
as item 2 of Section 5.4: enough top agents, and the rent disappears.

### 9.3 The imitation structure is a known type of model

**Green and Laffont, "Partially Verifiable Information and Mechanism Design", The Review of Economic
Studies 53(3), 447 to 456, 1986.** Publisher page
`https://academic.oup.com/restud/article-abstract/53/3/447/1577292`. I could not get the OUP page
body to render through WebFetch (the fetch returned navigation only) and the HBS copy returned HTTP
403, so the bibliographic details here come from the search result naming that publisher page and
from the RePEc record `RePEc:oup:restud:v:53:y:1986:i:3:p:447-456`. Anyone citing it should open the
primary once.

Why it matters. L1 says the set of instances an agent of capacity `M` can imitate is exactly
`{M' <= M}`, that is, the model is a partial verification model whose misreport correspondence is
the downward closed order ideal. That correspondence is transitive, so the nested range condition
of Green and Laffont holds and, in the static analogue, restricting attention to direct mechanisms
is without loss. I state this as an antecedent and an intuition, not as a step: our model is
dynamic, the "report" is a sequence of deliveries observed through Bernoulli noise, and I did not
verify that their revelation principle transfers. Do not write in the paper that it does.

### 9.4 What I searched for and did not find

For T1, T2, T3, T6 and T7 I did not find a primary source stating the result in the form given. The
searches I ran, all on 18 September 2026: "strategic agent can imitate lower ability only lower
bound identified upper confidence bound impossible mechanism learning capacity"; "second largest
mean upper bound impossibility strategic arms principal cannot obtain highest mean bandit
mechanism"; "optimal recovery Lipschitz functions sup norm point samples fill distance classical
lower bound information-based complexity". Negative search results are weak evidence, and I would
describe all of T1, T2, T3 as folklore observations made precise rather than as discoveries. Three
honest attributions to make in the paper:

- T5, the sup norm covering count, is the classical optimal recovery fact that approximating a
  Lipschitz function to `eps` in sup norm from point values requires an `eps/L` net. I did not find
  a primary source stating it in a citable form and I would present it as elementary, with the
  two line proof, and not claim it.
- T6's device is Assouad's subset averaging method, from Assouad, "Deux remarques sur l'estimation",
  Comptes Rendus de l'Academie des Sciences Paris, 296, 1021 to 1024, 1983. I verified only a
  secondary record of this reference (`https://www.semanticscholar.org/paper/Deux-remarques-sur-l'estimation-Assouad/7fc8b04f837d62422e7f3ffb79d84cbbad8327bc`)
  and did not open the primary; if the paper cites it, someone must check the primary. The standard
  textbook statement is in Tsybakov's "Introduction to Nonparametric Estimation" (2009), which I did
  not verify either. The novelty here, such as it is, is only that the argument is run against an
  adaptive *query* model with noiseless answers rather than against a regression design, which is
  what makes it immune to the objection the F1 sceptic raised in his Section 2.3.
- T7 is Le Cam's two point method with Pinsker's inequality, entirely standard; present it as an
  elementary calculation.

Finally, the static antecedent of C2 in auction theory is that the payment of a winner in a dominant
strategy incentive compatible single parameter mechanism is its critical value, a function of the
others' reports, which is why a second price and not a first price is the extractable level
(Myerson, "Optimal Auction Design", Mathematics of Operations Research 6(1), 58 to 73, 1981). I
tried `https://pubsonline.informs.org/doi/10.1287/moor.6.1.58` and got HTTP 403 and an EconPapers
URL that 404ed, so I did not verify a publisher page for it; if the paper cites Myerson, verify it
first. It is not needed: Braverman et al. Lemma 14 is the direct and verified antecedent.

## 10. What I would put in eight pages, and in what order

These results are worth pages only insofar as they answer objections. My ranking, with the objection
each buys off and an honest estimate of the space.

**Rank 1. T4 with C2, plus L1 as its one line input. About twelve lines, in Section
`sec:private`, immediately after `thm:private-mesp`.** It answers the single most likely referee
comment on the private section, "your benchmark is the second capacity, which looks like an artefact
of your mechanism". C2 converts that into "the top capacity is provably unattainable, and the
deficit is the whole gap". It also pays a second dividend for free: item 2 of Section 5.4 explains
why the public result needs at least two top agents and why `M_(2) = M_top` there, which currently
reads as a technical condition. State L1 as a display, C2 as a proposition, and give the five step
proof in three sentences; the steps are all one line each. Attribute Braverman et al. Lemma 14 in the
same breath, as in Section 9.1.

**Rank 2. T1, with L1 shared from Rank 1. About six lines, at the start of `sec:private`, before
the mechanism.** It answers "why is this not a UCB algorithm" and "why is the price shaded down
rather than set optimistically". It is the cheapest result in the report: given L1 the proof is one
substitution. State it for the scalar class as well as `F_L` so it also covers the contextual
section. Include, in one clause, the scope sentence that MESP *does* use an upper bound at the
proposed profile and never under arbitrary behaviour; without that clause the statement looks
inconsistent with the mechanism and a careful referee will say so.

**Rank 3. T3. Two lines, as a remark right after T1.** It answers "why an elicitation phase at all,
you already see rewards" more concretely than T1 does, because it says the information content is
exactly zero rather than one sided. The punch line worth printing is that MESP's Stage 1 is round
robin, so it is the coupling to Stage 2, not the sampling, that makes the block informative.

**Rank 4. T8. One sentence, inside the discussion of `thm:private-mesp`.** It justifies why the
theorem has three parts and why part (C) uses `mu_H^star` rather than `M_(2)`. It costs almost
nothing and it removes a "why not one theorem" comment.

**Rank 5. T7 with a pointer to `prop:tightness`. Three lines, in the discussion of the rate.** It
answers "is `n^{2/3}` an artefact". It must be stated with its scope, and the open problem must be
stated as an open problem in one clause; claiming a matching lower bound over all mechanisms would
be exactly the `separation` failure.

**Rank 6. T6, and T5 only as a remark. Four lines, in `sec:contextual`, proof in the appendix.**
It answers "why pay exploration in every cell rather than interpolating". Include it only if the
contextual section survives the page budget, since the objection it answers is second order compared
with the benchmark objection. If space is short, print the one sentence version: the envelope of T2
is the best possible interpolant and its error is `2L` times the fill distance, so a mechanism that
skips a constant fraction of the cells has average price error `Omega(L rho)` on the worst Lipschitz
instance even with noiseless data.

**Not in the paper: T2 in full.** Its content is used twice (the envelope is the right interpolant;
the agent chooses the envelope) and both uses are one sentence. Printing the theorem costs more than
it buys.

**One sentence that ties them together, and which I would print as the section's motivation.** Any
decision a mechanism must get right under arbitrary behaviour may depend on a capacity only through
a lower bound on it; upper bounds do not exist (T1), are not produced by observation (T3), and
cannot be substituted by estimation (T2). Second pricing with shading is the construction that obeys
this rule, which is why the mechanism has the shape it has. That is the answer to "why is your
mechanism this complicated", and it is worth more than any individual statement above.

## 11. The step I consider least secure, and what I did not do

I do not claim any result here is correct. In order of how much I would want a second reader on
them:

1. **The hypothesis (H1) of T4, read as a benchmark claim.** Every step of T4's proof is one line of
accounting plus one application of L1, and I am confident in each. What carries the weight is the
modelling decision that a revenue benchmark is a claim over a *family* of instances. A referee can
answer C2 by saying "my guarantee is `M_top n - o(n)` only on instances where the platform can
certify `M_top`", and T4 says nothing against that. I believe the family reading is the right one,
because the whole point of the private setting is that capacities are unknown, but this is a
judgement about what a benchmark means and not a theorem. If a referee rejects it, C2 collapses to a
statement about mechanisms with uniform guarantees. I would print the family explicitly in the paper
so that the reading is visible rather than implicit. This is the exact shape of the `separation`
failure: correct steps, and a headline that claims more about the class than the class supports.

2. **Step 4 of T4, the identification of the two utilities.** It is correct as written only because
`S^*_1(c)` is read as the instantiated map and because (PVM) makes the other agents' rules identical
across the two instances. Written carelessly, for instance with `S^*_1` described as "deliver your
capacity", the step is false. I flagged this in the proof and I would flag it in the paper.

3. **The claim in Section 5.4 item 1 that the relaxation cannot be tightened.** That is a claim about
*my* proof technique, supported by a numerical feasibility check on a grid of instances, not a
theorem. It could be wrong in the direction that matters, that is, a better argument might push
`alpha` to `0` and recover Braverman et al.'s conclusion in our model.

4. **T7's bearing on MESP.** T7 is an exact statement about statistics of Bernoulli samples. That it
applies to MESP's price rests on the claim that the price must be a uniformly valid one sided bound
on the runner-up's delivered mean, which is a property of MESP's proof, not a necessity for all
mechanisms. I stated this as scope, but it is the place where a referee could say the lower bound
does not bind.

5. **T6's constant.** The construction is elementary and I checked the bump mass numerically, but
the constant `omega_d / (2^{d+3}(d+1))` is unoptimised and I did not check the rounding in the
second display against a small `d` example by hand beyond the algebra given.

**What I did not do.** I did not modify, and did not need to compile, any canonical file. I did not
write any LaTeX; turning any of this into the manuscript is a separate task, and the wording in
Section 10 is a suggestion, not a patch. I did not verify MESP or CG-MESP against these results
beyond reading `sections/Private_information_setting.tex` and `sections/appendix_private.tex` for
places where an upper bound on a capacity is used under arbitrary behaviour; I found none, but that
is a read through and not a proof. I did not prove a lower bound over all mechanisms for the
`n^{2/3}` rate, and I state the open problem in Section 7 rather than gesture at it. I did not check
EXPLORER Section 2.6 items 1, 3 and 4, which are design commentary rather than theorems, except for
item 2, which is T8 here. I submitted no Slurm jobs; the only computation was three short local
scripts, logged in `COMPUTE_LOG.md` in this directory.
