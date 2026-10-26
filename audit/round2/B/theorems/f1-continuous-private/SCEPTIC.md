# F1 sceptic report: private capacities, continuous contexts, behavioural deviations

Worker: the separation worker, resumed 18 September 2026 as the sceptic on track F1.
Write scope: `audit/round2/B/theorems/f1-continuous-private/` and the scratchpad. No canonical file
was modified. No em dash and no triple hyphen appears in this file.

Read in full before starting: `audit/round2/prompts/COMMON.md`, `CONTEXT_PROOF_CONTRACT.md`,
`sections/Private_information_setting.tex`, `sections/appendix_private.tex`,
`sections/contextual_samf_algorithm.tex`, `sections/appendix_contextual.tex`,
`MATH_CANDIDATE_LEDGER.md` Sections 4, 5, 6.1 and 6.6, `c2-local-mesp/PROVER1.md`,
`c2-local-mesp/PROVER2.md`, `c2-local-mesp/ADVERSARY.md` Section 5.3 (finding F6),
`separation/REPORT.md`, and Braverman et al. Lemma 14 from the primary source.

## 0. Headline, stated first because it is negative for my own assignment

**I did not prove the impossibility, and I now believe the straightforward version of it is false.**
I found three independent structural facts, each checkable and each verified here, which say that
the cost accounting used to declare the cell-based route dead is wrong, and that the true achievable
exponent is very much better than the brief's. In decreasing order of how much they matter:

- **F-S1.** The brief's rate `1 - 1/(3(D+1))` comes from pinning the per-region bidding length at the
  *scalar* value `L = n^{2/3}(log n)^{1/3}`. That value is the solution of the scalar balance and is
  not the right one when there are many regions. Retuning `L` per region gives `n^{(D+2)/(D+3)}`,
  which is the public Grid-ETC rate. Section 1, with the algebra and a numerical confirmation that
  pinning `L` reproduces the brief's exponent exactly and retuning it gives mine.
- **F-S2.** Combining F-S1 with the adversary's finding F6 (capacities depend on the agent's own
  coordinate only) replaces the ambient dimension `D = Kd` by the per-agent dimension `d` in the
  *pricing* half of the problem. The pricing rate becomes `n^{(d+2)/(d+3)}`. For `K = 3, d = 1` that
  is `n^{0.75}` against the brief's `n^{0.9167}`. Section 2, including the reason per-agent pooling
  is unsafe for the *allocation* half and an architecture that separates the two.
- **F-S3.** The elicitation block does not have to be uniform across agents. Identifying which agent
  is top costs `O_inst(log n)` pulls of the top agent, whereas pricing accuracy costs `L` pulls of
  the *runner-up*. Both prior mechanisms already contain the device that makes a non-winner reveal
  at logarithmic cost. Section 3, with primary-source quotations.

What I did prove is one lower bound, for a class, in Section 4: any anytime cumulative-deficit
monitor with a small false-alarm probability admits an undetectable shading path worth
`Omega(sqrt(n))` on the monitored phase. This settles, as a statement about the *monitor*, the item
that `PRIVATE_BOUND_NOTES.md` Note 2, `MATH_CANDIDATE_LEDGER.md` Section 7.2 and `PROVER2.md`
Section 9 item 3 all record as "plausible and unproved" and instruct not to state as a theorem. It
does **not** compose into a lower bound on the equilibrium gain, and Section 5 says exactly why, and
catalogues the four unconditional attempts I made and the precise place each one dies.

Section 6 is the route map the brief asks for as the floor. Section 7 is what I did not do and the
step I consider least secure.

Everything labelled a *finding* is an accounting or structural statement I verified. Everything
labelled a *concern* is an intuition and, per the brief, the explorer is free to ignore it. Only
Section 4 contains a theorem, and I do not claim it is correct, only that I proved it from the
stated hypotheses.

## 0.1 Primary sources used here

| Source | URL | Read | Used for |
|:-|:-|:-|:-|
| Braverman, Mao, Schneider, Weinberg, "Multi-armed Bandit Problems with Strategic Arms", PMLR v99:383-416 | `https://proceedings.mlr.press/v99/braverman19b/braverman19b.pdf` | 18 Sep 2026 | Lemma 14 and its proof; Mechanism 1 lines 3 and 5; Mechanism 2 line 3 |
| Esmaeili, Shin, Slivkins, arXiv:2312.07929v2 | `https://arxiv.org/pdf/2312.07929v2` | 18 Sep 2026 | SP+SAMF Algorithm 1 line 5; PURE-SP Algorithm 2 line 6; Section 3.1 model |

Both were downloaded and converted with `gs -sDEVICE=txtwrite` during the separation task; the text
copies are in the scratchpad at `round2/separation/`. Nothing else is cited. The Bretagnolle and
Huber inequality used in Section 4 is proved from scratch in Lemma S0 so that no external reference
carries any weight.

## 0.2 Braverman et al. Lemma 14, read from the source, and why it is not the answer

Lemma 14: *let `mu` and `mu0` be the largest and second largest values among the `mu_i`; then for
any constant `alpha > 0`, no truthful mechanism can guarantee `(alpha mu + (1-alpha) mu0) T` revenue
in the worst case.* The proof (their Appendix, transcribed) fixes `L > exp(1/alpha)` instances with
`mu = b_i = 1/2 + i/(2L)` and `mu0 = 1/2`, writes `x_i T` for the expected pulls of the top arm and
`p_i T` for its expected payment, uses the dominant-strategy constraints `b_i x_i - p_i >= b_j x_j - p_j`
and `b_i x_i - p_i >= 0` to get the envelope bound `p_i <= b_i x_i + sum_{j<i} x_j (b_{j+1} - b_j)`,
combines it with the revenue requirement `p_i + (1 - x_i) mu0 >= alpha b_i + (1-alpha) mu0`, and
concludes `x_i >= alpha sum_{j<=i} 1/j > alpha ln i`, which exceeds `1` for `i > exp(1/alpha)`.

This is a mechanism-design envelope argument over a one-parameter family of *types*, and its
conclusion is that the *benchmark* cannot exceed the second-highest mean. It carries no exploration
cost, no horizon rate and no contextual content: `x_i` is a per-instance expected allocation share,
and the contradiction is `x_i > 1`, not a bound on `n`. It is a starting line exactly as the brief
says. I record two things I took from it and one I did not.

- Taken: the shape of a lower bound in this literature is an envelope argument over a family of
  instances plus a revenue requirement, not a regret-style change of measure. My Section 5 attempt
  (d) is the closest analogue I could build, and it fails for a reason I state there.
- Taken: their family is one-dimensional in the type, and the number of instances needed is
  `exp(1/alpha)`, a constant. Nothing in it scales with `n`, so it cannot be rescaled into a rate.
- Not taken: any claim that the second-capacity benchmark is the right target on a continuum. Their
  argument is scalar and I did not check whether the natural contextual analogue (no mechanism can
  guarantee more than `E sum_t M_(2)(X_t)`) holds; I believe it does by applying Lemma 14 pointwise
  on a positive-mass region, but I did not write that and it must not be cited as established.

# 1. Finding F-S1: the brief's obstruction rests on a mis-tuned per-region bidding length

The brief and `MATH_CANDIDATE_LEDGER.md` Section 4 ("Strongest counterexample or obstruction") both
compute the cell-localised cost as follows: with `J_n` cells the bidding cost is `J_n K L`, which
forces `J_n = o(n^{1/3}(log n)^{-1/3})` because `L = n^{2/3}(log n)^{1/3}`; balancing the Lipschitz
bias `n h_n` against `h_n^{-D} n^{2/3}(log n)^{1/3}` gives `h_n = (log n/n)^{1/(3(D+1))}` and the
rate `n^{1 - 1/(3(D+1))}`.

**The step that is wrong is holding `L` at its scalar value.** In the scalar mechanism `L_n` solves
its own balance: the bidding rounds `K L_n` are traded against the price slack `n s_n` with
`s_n ~ sqrt(log n / L_n)`, giving `K L_n = n L_n^{-1/2}` and hence `L_n = (n/K)^{2/3}` up to logs
(`sections/Private_information_setting.tex` says exactly this: "the choice `L_n ~ n^{2/3}(log n)^{1/3}`
balances the `K L_n` bidding rounds against the subsequent statistical loss `n s_n`"). When the
mechanism runs `J` independent local instances, the bidding rounds are `J K L` while the price slack
is still `n s ~ n L^{-1/2}`, so the balance is a different one and `L` must be solved again.

## 1.1 The retuned balance

Write the total cost, in revenue, of a cell-localised private mechanism on a grid of side `h` in
dimension `m` (take `m = D` for now; Section 2 replaces it by `d`), suppressing logarithms and
absolute constants:

    cost(h, L)  =  K h^{-m} L      (bidding rounds, one block of L pulls per agent per cell)
                +  n L^{-1/2}      (price slack: s ~ L^{-1/2}, charged at every round)
                +  n h             (Lipschitz bias of a cell-constant price).

Minimising in `L` at fixed `h`: `d/dL [K h^{-m} L + n L^{-1/2}] = K h^{-m} - (n/2) L^{-3/2} = 0`,
so

    L*(h) = ( n h^m / (2K) )^{2/3} ,

and both of the first two terms become `Theta( K^{1/3} n^{2/3} h^{-m/3} )`. Minimising the remaining
`c K^{1/3} n^{2/3} h^{-m/3} + n h` in `h` gives `h^{(m+3)/3} = Theta(n^{-1/3})`, that is

    h* = Theta( n^{-1/(m+3)} ) ,        cost = Theta( n^{(m+2)/(m+3)} ) ,
    L*  = Theta( ( n h*^m )^{2/3} ) = Theta( n^{2(m+3-m)/(3(m+3))} ) = Theta( n^{2/(m+3)} ) .

Note what `L*` is: `n^{2/(m+3)}`, which for `m = 1` is `n^{1/2}` and for `m = 3` is `n^{1/3}`, all
far below the scalar `n^{2/3}`. Pinning `L = n^{2/3}` therefore over-pays the bidding term by a
polynomial factor, and that over-payment is the whole of the brief's obstruction.

## 1.2 Numerical confirmation

I minimised `cost(h,L) = h^{-m} L + n L^{-1/2} + n h` over a fine logarithmic grid in `h` with `L`
set to `L*(h)`, for `n` from `10^6` to `10^24`, and fitted the slope of `log cost` against `log n`
(script `check_exponents.py`, 1 second on the login node):

| grid dimension `m` | fitted exponent, `L` retuned | `(m+2)/(m+3)` | fitted exponent, `L` pinned at `n^{2/3}` | `1 - 1/(3(m+1))` |
|:-|:-|:-|:-|:-|
| 1 | 0.75000 | 0.75000 | 0.83256 | 0.83333 |
| 2 | 0.80000 | 0.80000 | 0.88857 | 0.88889 |
| 3 | 0.83333 | 0.83333 | 0.91645 | 0.91667 |
| 4 | 0.85714 | 0.85714 | 0.93315 | 0.93333 |
| 6 | 0.88889 | 0.88889 | 0.95224 | 0.95238 |

The right-hand pair confirms that pinning `L` reproduces the brief's exponent to four digits, so I
have identified the brief's calculation correctly and am not attacking a straw version of it. The
left-hand pair confirms the retuned exponent.

## 1.3 The other two terms do not spoil it

Two further costs appear in a cell-localised MESP and must be checked at `h* = n^{-1/(m+3)}`,
`J = h*^{-m} = n^{m/(m+3)}`, `L* = n^{2/(m+3)}`.

- *Monitoring slack.* One anytime boundary per cell costs `sum_C b(n_C) = sum_C sqrt(n_C log n)`,
  which by Cauchy and Schwarz is at most `sqrt(J n log n) = n^{(2m+3)/(2(m+3))} sqrt(log n)`. Since
  `(2m+3)/(2m+6) < (2m+4)/(2m+6) = (m+2)/(m+3)`, this is strictly *smaller* than the balanced cost.
  The brief's claim that "one martingale per cell costs the square root of cells times horizon
  rather than the square root of horizon" is arithmetically right and is not an obstruction: it is
  a lower-order term at the balanced grid.
- *Fallback.* `sum_C R^dbl_K(n_C) = O( sqrt(K J n log K) )`, the same order as the monitoring slack
  by the same computation, hence also lower order. (This is the `Grid-EXP3` accounting of
  `separation/REPORT.md` Part 2, Step 5.)
- *Deviation gain from the bidding blocks.* Both C2 provers show the bidding term is attained: a
  deviator that is uniquely top at a region collects the Stage-1 effort saving once per region, so
  the gain contains `Theta(J L) = Theta(n^{(m+2)/(m+3)})`. This is `o(n)`, so it does not break the
  additive equilibrium, and it is the same order as the revenue cost. Nothing here forces a worse
  rate than `n^{(m+2)/(m+3)}`.

**Statement of the finding, with its exact status.** I have *not* proved that a cell-localised
continuous private mechanism exists or that its analysis closes; PROVER2's Section 9 item 1 lists
the real obstacles (a cell-average bid is not a capacity, the price may exceed an agent's capacity
at some contexts inside a cell and not at others, and the bid-domination coupling loses its fixed
comparison target). What I have shown is that the *reason the route was declared dead is an
arithmetic error*, and that the correct cell-based accounting lands at the public Grid-ETC exponent
rather than far below it. Route 1 of the brief should be reopened on this basis.

# 2. Finding F-S2: with the adversary's F6, the pricing problem lives in dimension `d`, not `D`

`ADVERSARY.md` Section 5.3 (finding F6) establishes, against PROVER2's Remark 6.2, that on the
manuscript's contextual model two distinct full profiles sharing agent `j`'s coordinate have the
same `M_j`, because the contract fixes `mu_i(x_i)` and `M_i(x_i)` as functions of agent `i`'s own
coordinate. I verified this against `CONTEXT_PROOF_CONTRACT.md` Section 2 and
`sections/setting.tex`: the primitives are `mu_i(x_{i,t})` and `M_i(x_{i,t})`, and the full profile
enters only through the platform's observation and the agents' information.

## 2.1 The consequence for the rate

An agent's capacity is one `L`-Lipschitz function on `[0,1]^d`, not `J` unrelated numbers. A
mechanism that keys its elicitation on the pair `(agent, own coordinate cell)` runs `K h^{-d}`
bidding blocks rather than `K h^{-D}`. Re-running Section 1.1 with `m = d`:

    h* = Theta( n^{-1/(d+3)} ),   L* = Theta( n^{2/(d+3)} ),   pricing cost = Theta( n^{(d+2)/(d+3)} ).

| `K` | `d` | `D = Kd` | brief's `1 - 1/(3(D+1))` | F-S1 retuned, `m = D` | F-S1 plus F6, `m = d` |
|:-|:-|:-|:-|:-|:-|
| 2 | 1 | 2 | 0.8889 | 0.8000 | 0.7500 |
| 3 | 1 | 3 | 0.9167 | 0.8333 | 0.7500 |
| 5 | 1 | 5 | 0.9444 | 0.8750 | 0.7500 |
| 3 | 2 | 6 | 0.9524 | 0.8889 | 0.8000 |

The third column is independent of `K` in the last entry group, which is the whole point: the
statistical problem is `K` separate `d`-dimensional estimation problems, and `K` enters only through
constants.

## 2.2 Where per-agent pooling is *not* safe, which the explorer must not miss

`MATH_CANDIDATE_LEDGER.md` Section 6.1 already records the obstruction to per-agent cells, and it is
real. Its instance, which I re-read and believe: one honest agent `h` with `mu_h = 0.2` on cell `A`
and `0.9` on cell `B` of equal mass, and one strategic agent with a constant own context that
delivers `1` when `h` is in `A` and `0` when `h` is in `B`. A per-agent pooled estimator reads the
strategic agent's mean as about `0.5` at its single own-coordinate cell while its conditional mean
given `B` is `0`, and a rule that allocates on the pooled estimate suffers a linear robustness loss.

The correct reading of that instance is narrower than "per-agent pooling is unsafe". What it shows
is: **a strategic agent's delivered mean is not a function of its own coordinate, so pooling is
unsafe for any quantity that must be correct under arbitrary behaviour.** It says nothing about
pooling a quantity that only has to be correct *at the proposed profile*, because at `S^*` every
agent delivers `M_j(x_j)`, which is own-coordinate measurable by the model.

That distinction suggests an architecture, which I record as a **concern-grade idea for the
explorer, not a result**:

- *Pricing* is elicited on a per-agent `d`-dimensional grid. Its correctness is needed at `S^*`
  (for the revenue statement) and, for the equilibrium statement, only through the price faced by
  the deviator, which is a function of the *other* agents' bids. A unilateral deviator cannot poison
  the bids that price it. This is exactly the structure that carries `thm:private-mesp` and both C2
  provers' Lemma B.
- *Robustness under arbitrary joint behaviour* is delegated entirely to a fallback that makes no use
  of pooled estimates. `separation/REPORT.md` Part 2 Theorem 3 supplies one off the shelf: cell-local
  EXP3 on a `D`-dimensional grid with doubling epochs attains
  `sum_t b(X_t) - O(n^{(D+1)/(D+2)} sqrt(K log K))` against *any* nonanticipating behavioural profile
  and *any* oblivious context sequence, with no cell law and no i.i.d. assumption. Its exponent
  `(D+1)/(D+2)` is better than the `(d+2)/(d+3)` pricing cost whenever `(D+1)/(D+2) < (d+2)/(d+3)`,
  which holds for `d = 1` and every `D >= 3`, and is in any case an additive term.

So the two halves want different grids, and nothing forces them onto the same one. I did not check
whether the two can be interleaved without the fallback's grid contaminating the pricing grid's
schedule, and the scheduling condition the adversary flags in F6 ("a profile enters Stage 2 only
once every coordinate bid it uses is complete") is unresolved and is the first thing to attack.

## 2.3 The sceptic's own warning about F-S2

F6 is the reason my assignment's natural argument is likely false, and I want to state the danger
precisely rather than only agree with the coordinator.

The counting argument "a bidding block must be paid in every region, a continuum has too many
regions, therefore the cost is unavoidable" has premise "the mechanism must estimate the price
region by region". F6 kills the premise for the *pricing* half. But a weaker premise survives and I
could not kill it: **whatever the mechanism does, it must resolve each `M_j` to some accuracy `eps`
on a set of coordinates of positive measure, and the class of `L`-Lipschitz functions on `[0,1]^d`
has metric entropy `Theta((L/eps)^d)` at scale `eps`, so no estimator, adaptive or not, can beat
`(L/eps)^d` "effective" observations.** That is a statement about the function class, not about a
partition, and it is exactly the shape the coordinator asks for. It gives the same `eps^{-(d+2)}`
sample count as the partition argument, because the partition estimator is minimax optimal for that
class. So F6 changes `D` to `d`; it does not, as far as I can see, remove the `eps^{-(d+2)}`
scaling. **I therefore do not expect a better rate than `n^{(d+2)/(d+3)}` from function estimation,
and the reason the counting argument fails as an impossibility is that `n^{(d+2)/(d+3)}` is `o(n)`,
not that the count is avoidable.** The count is real; it is just affordable.

I record this as the single most useful correction to my own brief: the continuum does not have
"too many regions". At the balanced scale it has `n^{d/(d+3)}` of them, which is a vanishing
fraction of `n`, and the reason the original accounting said otherwise is F-S1.

# 3. Finding F-S3: the elicitation block need not be uniform across agents

A second place where the received accounting over-charges. The bidding block of `MESP` and of both
C2 mechanisms pulls *every* agent `L` times in *every* region. Two different jobs are being done by
those pulls and they have very different costs.

- **Ranking.** The mechanism must find out which agent is top. Separating two agents whose capacities
  differ by `delta` needs `Theta(log(n)/delta^2)` pulls of each, an *instance constant* times
  `log n`, not `n^{2/3}`. A racing or successive-elimination schedule achieves it.
- **Pricing.** The mechanism must know the runner-up's capacity to accuracy `s`, which needs
  `Theta(1/s^2)` pulls of the *runner-up*. This is the term that forces `L`.

`MESP` conflates them and pays `L` for both. The consequence is precisely the term that both C2
provers show is attained: the top agent's Stage-1 pulls are inconsequential (it wins regardless, at
a price set by others), so it shades them for free, gaining `L (M_i - V_i)/2` per region. **A
schedule that stops pulling the top agent once its rank is certified reduces that free shirk to
`O_inst(log n)` per region**, while keeping the runner-up's `L` pulls, which are the ones pricing
needs.

The obvious objection is that the runner-up's own pulls then become the inconsequential ones: it
sets the price for somebody else and gains nothing from revealing. Both prior mechanisms already
contain the device that answers this, and I quote them from the primary sources.

- Braverman et al., Mechanism 1 line 5 (PMLR v99, Section 4.1): *"For each arm `i` satisfying
  `u + log(w_i) >= 0`, play it `floor(u + log(w_i))` times. Then, with probability
  `u + log(w_i) - floor(u + log(w_i))`, play arm `i` for one more round."* A non-winner's number of
  reward-phase pulls is logarithmic in its own reported value, which is exactly the marginal
  incentive that makes truthful reporting a dominant strategy at logarithmic cost. Mechanism 2 line
  5 is the same with `w_i` replaced by `w_i - M` and `B` pulls per unit.
- Esmaeili et al., SP+SAMF Algorithm 1 line 5 (arXiv:2312.07929v2): *"Tell the arms that this is the
  reward phase then pull each arm `i` for a number of rounds `N_i` where
  `E[N_i] = hat mu_i^{rho+3} ln(n)` and `hat mu_i` is the mean of arm `i` during SAMF phase
  rounds."* PURE-SP Algorithm 2 line 6 is the analogue with `E[N_i] = 2 m_i`.

So both prior mechanisms pay a *reward phase whose length increases in the revealed value*, and both
keep it at `O(log n)` or `O(1)` total. The manuscript's `MESP` has no reward phase. **Concern for
the explorer:** an asymmetric elicitation schedule (race to certify the ranking, then price off the
runner-up alone, then a logarithmic reward phase keyed to the revealed values) is not obviously
ruled out, and it attacks the one term that both C2 provers show is attained by the current design.
I did not check whether it survives the noisy-bid analogue of the dominant-strategy argument, which
is the obvious place it could fail: in Braverman's model a report is a chosen number, whereas here a
"report" is an empirical mean of `L` Bernoulli draws, so the marginal incentive is smeared by
`O(1/sqrt L)` and the exact dominant-strategy computation does not transfer.

**Status: concern, not a result.** It is an argument that a lower bound charging `L` to the top
agent per region would be proving something false about the problem rather than true.

# 4. Theorem S1: what a cumulative-deficit monitor must concede

This is the one theorem in this report. It is a lower bound for a class, and the class is the one
that every mechanism in this project uses for its exploitation phase.

## 4.1 The class

**Definition S1 (cumulative-deficit monitor).** Let `B : {0,1,2,...} -> [0, infinity)` be
deterministic, nondecreasing, with `B(0) = 0`. A mechanism *monitors agent `i` at announced price
`tau` with boundary `B` over a phase of planned length `N`* if, during the phase, agent `i` is
pulled at every round of the phase; writing `Y_1, Y_2, ...` for its rewards in the phase and
`Z_r := Y_1 + ... + Y_r`, the phase terminates at

    T := min{ r >= 1 : Z_r < r tau - B(r) } ,

with the convention `min emptyset = infinity`; if `T > N` the phase runs its full `N` pulls. What
the mechanism does before, and after termination, is unrestricted.

This is `MESP` Stage 2 verbatim with `B = b_n`, `b_n(r) = sqrt(r log(2 n^4)/2)`
(`sections/Private_information_setting.tex`). It is Braverman et al. Mechanism 2 line 3 with the
linear boundary `B(r) = r M`, `M = 8 B^{-1/2} ln(KT)`, after its burn-in. It is the Stage 2 of both
C2 mechanisms (`PROVER1.md` (M3), `PROVER2.md` Section 2) with `B = b`. It is what routes 2 and 4 of
the brief propose to keep while changing what is monitored.

## 4.2 The theorem

**Theorem S1 (boundary tracking).** Let a mechanism monitor a strategic agent `i` at price
`tau in (0,1)` with a nondecreasing boundary `B` over a phase of planned length `N >= 2`. Suppose
`B(r) = beta sqrt r` for `r >= 1`, with `beta >= sqrt(log(2N))`, and put

    theta := 1 - sqrt(log(2N)) / beta  in  [0,1) ,      r_0 := ceil( beta^2 / (4 tau^2) ) .

Consider the deviation `S'_i` which, at its `r`th pull of the phase, delivers

    m_r := tau                          for  r <= r_0 ,
    m_r := tau - theta ( B(r) - B(r-1) )  for  r > r_0 .

Then `S'_i` is feasible (`m_r in [0, tau] subseteq [0, M_i]`), it is implementable from the
announced price, the agent's own pull index and the public description of the mechanism, and:

(a) the phase is *not* terminated before its `N`th pull, except on an event of probability at most
    `1/(4N)`;
(b) on that complement the agent's effort saving over the phase is exactly

        theta ( B(N) - B(r_0) )  =  ( beta - sqrt(log(2N)) ) ( sqrt N - sqrt(r_0) ) .

Consequently, if under compliance the agent would have received all `N` pulls of the phase except on
an event of probability `delta`, and if per-pull utilities lie in `[0,2]`, then

    u_i(S'_i, .) - u_i(S^*_i, .)  >=  ( beta - sqrt(log 2N) )( sqrt N - sqrt r_0 ) - 2 n ( 1/(4N) + delta ) .

*Proof.* Feasibility: `B` is concave in `r` so `B(r) - B(r-1) = beta(sqrt r - sqrt(r-1)) <= beta/(2 sqrt(r-1))`
for `r >= 2`; at `r > r_0 >= beta^2/(4 tau^2)` this is at most `beta / (2 sqrt(beta^2/(4 tau^2))) = tau`,
so `m_r in [0, tau]`. Since `i` is strategic there is no lower honesty constraint, and `tau <= M_i`
because the monitor is only run on an agent the mechanism expects to meet the price (if
`tau > M_i` the statement is vacuous for `i`).

Let `F_r` be the history through the agent's `r`th pull of the phase and set

    M_r := sum_{q<=r} ( Y_q - E[Y_q | F_{q-1}] ) = sum_{q<=r} ( Y_q - m_q ) ,

a martingale whose increments lie in an interval of length `1` given the past, since `Y_q in {0,1}`.
Define the slack `S_r := Z_r - r tau + B(r)`, so termination at `r` is exactly `S_r < 0`. Then

    S_r  =  sum_{q<=r} ( Y_q - tau )  +  B(r)
         =  M_r + sum_{q<=r} ( m_q - tau ) + B(r)
         =  M_r  -  theta ( B(r) - B(r_0) )_+  +  B(r) ,

using `m_q - tau = 0` for `q <= r_0` and `= -theta (B(q) - B(q-1))` afterwards, which telescopes.
For `r <= r_0` this is `M_r + B(r) >= M_r + (1-theta) B(r)`; for `r > r_0` it is
`M_r + (1-theta) B(r) + theta B(r_0) >= M_r + (1-theta) B(r)` since `theta, B(r_0) >= 0`. Hence in
all cases

    S_r  >=  M_r + (1-theta) B(r) ,

so `{ S_r < 0 }` implies `{ M_r < -(1-theta) B(r) }`. By the Azuma and Hoeffding inequality in the
conditional-range form used by the manuscript itself (increments of conditional range `1`),

    Pr( M_r <= -u )  <=  exp( -2 u^2 / r )   for every `u >= 0` and every fixed `r`.

Take `u = (1-theta) B(r) = (1-theta) beta sqrt r = sqrt(log(2N)) sqrt r`, by the definition of
`theta`. Then `2u^2/r = 2 log(2N)` and each term is `exp(-2 log 2N) = (2N)^{-2}`. A union bound over
`r = 1, ..., N` gives

    Pr( exists r <= N : S_r < 0 )  <=  N (2N)^{-2}  =  1/(4N) ,

which is (a). On the complement, the agent is pulled `N` times and its total effort saving is
`sum_{r<=N} (tau - m_r) = theta sum_{r > r_0} (B(r) - B(r-1)) = theta (B(N) - B(r_0))`, which is
(b) after substituting `theta` and `B`.

For the last display: on the intersection of the survival event and the event that the compliant
baseline also receives all `N` pulls, the two executions award the agent the same number of pulls,
so their utilities differ by exactly the effort saving. The two exceptional events have total
probability at most `1/(4N) + delta`, and per-pull utilities lie in `[0,2]` over at most `n` rounds,
so they contribute at most `2n (1/(4N) + delta)`. `QED`

## 4.3 What it says about the manuscript's mechanism, with numbers

`MESP` has `beta = sqrt( log(2 n^4) / 2 )` and `N = N_n >= n/2`, and its Lemma
`lem:private-monitor` gives `delta <= (2 n^3)^{-1}` for the compliant baseline. Then
`beta >= sqrt(2 log n)`, `sqrt(log 2N) <= sqrt(log 2n)`, `r_0 = O(log n / tau^2)`, and for `n` large

    gain  >=  ( beta - sqrt(log 2N) ) ( sqrt N - sqrt r_0 ) - 2n/(4N) - 2n(2n^3)^{-1} .

The leading factor tends to `(sqrt 2 - 1) sqrt(log n) * sqrt(n/2) = 0.293 sqrt(n log n)`, and the
two correction terms are at most `1` and `n^{-2}`. Convergence is slow because of the `r_0` and
`log 2` corrections: the exact formula is at least `0.25 sqrt(n log n)` for every `n >= 10^3` and
`tau in [0.3, 0.6]` in the numerical check of Section 6, and exceeds `0.28 sqrt(n log n)` from about
`n = 10^5`. So `MESP`'s additive equilibrium gain is `Omega(sqrt(n log n))` from Stage 2 alone. This settles, as
a theorem, the item recorded as plausible and unproved in `PRIVATE_BOUND_NOTES.md` Note 2,
`MATH_CANDIDATE_LEDGER.md` Section 7.2 ("the experiments lead's Stage-2 boundary-tracking gain of
order `b_n(N_n)` is plausible but unverified and must not be stated as proved") and `PROVER2.md`
Section 9 item 3. It does not change `MESP`'s order, which is `n^{2/3}(log n)^{1/3}` from Stage 1.

## 4.4 What it says about the brief's routes 2 and 4, which is the point

**Corollary S1.1 (one global monitor still concedes `sqrt(n log(1/delta))`).** Route 2 replaces the
per-cell martingale by one global cumulative comparison. Theorem S1 applies to it with `N = Theta(n)`
and gives a concession of `Omega(beta sqrt n)`. If the mechanism wants a false-alarm probability
`delta` over `n` rounds with a `sqrt`-shaped boundary, `beta` is of order `sqrt(log(1/delta))`, so
the concession is `Omega( sqrt( n log(1/delta) ) )`, that is `Omega(sqrt(n log n))` for the
polynomially small `delta` the honest-benchmark proofs use. Route 2 therefore buys a real
improvement over the per-cell version but has a floor, and the floor is `sqrt(n log n)`.

**Corollary S1.2 (per-region monitors pay `sqrt(J n)`).** If the mechanism runs one monitor per
region with the same boundary shape, the deviator runs the strategy of Theorem S1 in every region at
once. The union bound in the proof is over all `sum_C N_C <= n` monitored pulls, so taking
`1 - theta = sqrt(log 2n)/beta` gives a failure probability at most `1/(4n)` for *all* regions
simultaneously, and the saving is `theta sum_C ( B(N_C) - B(r_0) )`, which by concavity and
`sum_C N_C = n` is maximised at equal regions and equals `Theta( beta sqrt(J n) )`. So a mechanism
with `J` local monitors concedes `Omega( sqrt( J n log n ) )`. **This is a matching lower bound for
the monitoring term of Section 1.3**, which was `O(sqrt(J n log n))`, so that term of the accounting
is exactly right and cannot be improved by analysis.

**Corollary S1.3 (route 4 does not delete the problem, it relocates it).** Route 4 removes the
dedicated bidding block by deriving the price from other agents' ongoing performance. Whatever it
prices on, it must still stop exploiting an agent that underdelivers, and if it does so through a
cumulative-deficit test the concession of Theorem S1 applies. Route 4 can therefore remove the
`J L` term but not the `sqrt(J n log n)` term unless it also abandons cumulative-deficit testing.

## 4.5 What Theorem S1 does not cover

1. **Randomised or history-dependent boundaries.** `B` is deterministic and known to the agent. A
   mechanism that randomises its boundary, or adapts it to the realised path, is outside the class.
   I did not attempt it; the natural repair is to let the agent shade by `theta` times the
   *conditional expected* boundary increment, which needs the agent to know the boundary's law, and
   the argument would then bound the gain only in expectation over the mechanism's coins. I did not
   write it.
2. **Non-`sqrt` boundaries.** The theorem is stated for `B(r) = beta sqrt r`. For a general
   nondecreasing `B` the same proof gives survival probability at least
   `1 - sum_{r<=N} exp(-2(1-theta)^2 B(r)^2/r)` and saving `theta(B(N) - B(r_0))`, so any boundary
   with `B(r) >= beta sqrt r` for `r >= r_0` is covered; boundaries that are smaller than
   `sqrt(r log N)` somewhere are *not* covered by the theorem, but they have a large false-alarm
   probability, which is the converse direction I did **not** prove (Section 5(c)).
3. **It is a bound on one phase, not on the mechanism.** It says a monitored exploitation phase
   concedes `beta sqrt N`. It does not say a mechanism must have such a phase. A mechanism with no
   exploitation phase at all, for instance one that always allocates by an adversarial rule, is
   outside the class entirely, and so is any mechanism that stops exploiting on a statistic other
   than a cumulative deficit against an announced price.
4. **The agent must be strategic.** An honest deviator cannot shade below `mu_i`, so the theorem
   applies to it only while `tau - theta Delta B(r) >= mu_i`, which holds for `r` beyond a constant.
   I did not write that version.
5. **No claim of optimality.** `theta` and `r_0` are chosen to make the proof clean, not to maximise
   the saving. A larger saving is presumably available; I did not look for it.

# 5. Four attempts at an unconditional lower bound, and the precise place each dies

The brief forbids closing a route with an argument that something looks hard, so each of these is
recorded with the exact line that fails and, where I have one, a concrete reason it is not
repairable by being more careful.

## 5(a) Uniform shading plus a change of measure. Dies on the cost of being caught.

*Attempt.* Agent `i` plays `S^*_i` shifted down by `eta` at every pull. Write `A := 1 + mu_i - tau`
for its per-pull baseline utility. Then

    gain  =  A ( E_dev[T_i] - E_base[T_i] )  +  eta E_dev[T_i] ,

and one bounds `|E_dev[T_i] - E_base[T_i]| <= n * TV(P_dev, P_base)` with
`TV <= sqrt(KL/2)` and `KL <= c_kappa eta^2 E[T_i] <= c_kappa eta^2 n` by the chain rule.

*Where it dies.* The first term is `Theta(n * TV) = Theta(eta n^{3/2})` and the second is
`Theta(eta n)`. The first always dominates, for every `eta > 0` and every `n > 1`. Making `eta`
small shrinks both at the same rate, so no choice of `eta` rescues it. The same happens with the
monotone coupling `Y = 1{U <= m}`, `Y' = 1{U <= m - eta}`: the probability that the two executions
ever diverge is `eta E[T_i]`, and a single divergence is allowed, by the bound, to cost the agent
all `n` of its remaining pulls, giving a risk of `eta n^2` against a gain of `eta n`.

*Why it is not a matter of being more careful.* The bound is tight for the class of all mechanisms.
There genuinely exists a mechanism that drops an agent for good on one adverse reward, and against
it a uniform shading is catastrophic. **The only way to exclude such a mechanism is exactly the
separation theorem of `separation/REPORT.md` Part 1**: a mechanism that reacts to a single pull and
excludes irreversibly collects `O(1)` reward on any Bernoulli-gap instance, so it cannot be a
candidate. That composition is the most promising route to an unconditional bound and it is
recorded as attempt 5(d) below, where it fails for a different reason.

## 5(b) Two instances differing in the runner-up's capacity. Dies because unilateral deviation is protected.

*Attempt.* Instance `A` has the runner-up at capacity `v`, instance `B` at `v - eta`. In `A`, the
top agent shading to `v - eta` produces the same observation law as compliance in `B`, so the
mechanism cannot react differently, and the shading gains `eta E_B[T_i] = Omega(eta n)`.

*Where it dies.* The mechanism's observations of the *runner-up* differ between the two instances,
because in `A` the runner-up still delivers `v`. A unilateral deviator cannot change that. The
mechanism needs `Theta(1/eta^2)` pulls of the runner-up to exploit the difference, but those pulls
are cheap: the runner-up delivers `M_(2)`, which is the benchmark itself, so sampling it costs no
revenue. The mechanism can therefore set `eta = n^{-1/2}` and sample the runner-up `n` times without
loss. The construction only bites if the runner-up is itself strategic and must be incentivised to
reveal, which makes the argument circular: the price for the runner-up's revelation is what we are
trying to bound.

*Explicit numbers.* `K = 2`, agent 1 strategic with `M_1 = 0.9`, `mu_1 = 0`, agent 2 honest with
`mu_2 = M_2 = v`, `v in {0.5, 0.5 - eta}`. Benchmark `v n`. A mechanism that pulls agent 2 for the
first `sqrt n` rounds, prices at its empirical mean minus `n^{-1/4}`, and then exploits agent 1 under
a cumulative monitor, gets `v n - O(n^{3/4})` on both instances. No lower bound of order better than
`n^{3/4}` survives, and Theorem S1 already gives `sqrt(n log n)` there.

## 5(c) Anti-concentration converse to Theorem S1. Not attempted to completion; a genuine gap.

*What is missing.* Theorem S1 assumes `B(r) >= beta sqrt r`. To make it a statement about *every*
monitor rather than every `sqrt`-shaped one, I need the converse: a boundary with false-alarm
probability at most `delta` over `N` compliant pulls must satisfy `B(N) >= c sqrt(N log(1/delta))`.
That is a binomial lower-tail anti-concentration statement. Slud's inequality (Annals of
Probability, 1977) is the standard tool and would give it immediately, but the brief forbids relying
on a literature fact I have not checked against the primary source, and I did not check it. A
Berry and Esseen route would also work and has the same problem.

*Why I did not fake it.* The Bretagnolle and Huber inequality, which I can prove in four lines and
which was my first instinct, does **not** give this. It lower-bounds the sum of the two error
probabilities of a test, and here the "test" `A = {terminate}` is not required to have small error
under the alternative, so the inequality is satisfied for every large `B` and yields nothing. I
checked this and record it so nobody repeats it.

*Consequence.* Corollaries S1.1 to S1.3 are conditional on the boundary being at least of order
`sqrt(r log N)`, which holds for `MESP`, for both C2 mechanisms and for any boundary derived from
Azuma or Hoeffding, but is an assumption and not a theorem. This is the largest unclosed gap in
Section 4.

## 5(d) Composing the separation theorem with shading. The route I believe in; the missing step named.

*Attempt.* Attempt 5(a) fails only because a mechanism is allowed to be arbitrarily sensitive to one
reward. Define a mechanism's *single-pull sensitivity* as

    sens  :=  sup over histories and pulls of agent i of  | E[T_i(n) | that pull gave 1] - E[T_i(n) | that pull gave 0] | .

If `sens <= S`, then the monotone coupling gives `|E_dev[T_i] - E_base[T_i]| <= S * eta E[T_i]`,
because the executions diverge at each pull with probability `eta` and each divergence costs at most
`S`. The gain is then

    gain  >=  eta E[T_i] ( 1 - A S )   which is  Omega(eta n)  as soon as  S < 1/A ,

and with `eta` as large as feasibility allows this is `Omega(n)`, which is far too strong and shows
the bookkeeping is wrong somewhere; the correct version caps `eta` by what the monitor tolerates and
lands back on Theorem S1.

*The missing step.* To use this one must show that a mechanism retaining the honest benchmark has
small `sens`. Part 1 of `separation/REPORT.md` proves something weaker: a mechanism whose *exclusion
kernel* reads a single pull loses the benchmark. It does not bound `sens` for a general mechanism,
and `sens` can be large for perfectly good reasons (a UCB index moves after one reward, and near a
tie that can swing many future pulls). I could not find a formulation of "insensitive" that is both
implied by the honest-benchmark guarantee and strong enough to drive the coupling. **This is the
same failure mode the separation report named as its own least secure point**: the class definition,
not the probability. I record it as the open problem rather than as an obstruction, because I have
no instance showing it cannot be done.

*What would settle it.* Either (i) a theorem of the form "honest-benchmark retention implies
`E[T_i(n)]` is `L`-Lipschitz in the agent's delivered-mean path in a suitable metric", which would
immediately give an unconditional `Omega(sqrt n)` gain bound by the argument above, or (ii) an
explicit mechanism with the honest benchmark and gain `o(sqrt n)`, which would refute it. I have
neither.

# 6. Numerical checks

Login node, seconds, no Slurm job submitted. Scripts in this directory: `check_exponents.py`
(Section 1.2) and `check_s1.py` (Theorem S1). Seeds fixed in the files.

**Theorem S1**, `MESP` boundary `b_n(r) = sqrt(r log(2n^4)/2)`, `N = n/2`, 2000 replications per row:

| `n` | `N` | `beta` | `theta` | `r_0` | observed `Pr(survive all N)` | realised saving | Theorem S1(b) | `1/(4N)` |
|:-|:-|:-|:-|:-|:-|:-|:-|:-|
| `10^4` | 5000 | 4.332 | 0.2995 | 53 (`tau=0.3`) | 1.0000 | 82.29 | 82.29 | `5.0e-5` |
| `10^4` | 5000 | 4.332 | 0.2995 | 14 (`tau=0.6`) | 1.0000 | 86.88 | 86.88 | `5.0e-5` |
| `10^5` | 50000 | 4.835 | 0.2982 | 65 (`tau=0.3`) | 1.0000 | 310.69 | 310.69 | `5.0e-6` |
| `10^5` | 50000 | 4.835 | 0.2982 | 17 (`tau=0.6`) | 1.0000 | 316.37 | 316.37 | `5.0e-6` |
| `10^6` | 500000 | 5.289 | 0.2973 | 78 (`tau=0.3`) | 1.0000 | 1098.01 | 1098.01 | `5.0e-7` |
| `10^6` | 500000 | 5.289 | 0.2973 | 20 (`tau=0.6`) | 1.0000 | 1104.87 | 1104.87 | `5.0e-7` |

The saving is deterministic on the survival event, so the last two columns must agree exactly and do.
The survival probability was `1` in every one of the 12000 runs, against the theorem's bound
`1 - 1/(4N)`. The compliant baseline triggered the boundary in `0` of 2000 runs at `n = 10^5`, which
is consistent with the manuscript's `(2n^3)^{-1}`. Comparing to `sqrt(n log n)`: the ratios are
`0.271, 0.286, 0.290, 0.295, 0.295, 0.297`, so `0.25 sqrt(n log n)` is a safe finite-`n` floor and
`0.293` is the limit computed in Section 4.3.

**Section 1.2 exponents** are reported in the table there; the script minimises the three-term cost
over a logarithmic grid of `10^5` values of `h` with `L` set to its analytic optimum, for `n` from
`10^6` to `10^24`, and fits the slope of `log cost` against `log n`.

# 7. Route map, which is the floor the brief asks for

| Route | Status after this report | Where it stands or dies |
|:-|:-|:-|
| 1. Two scales (coarse pricing grid over fine allocation grid) | **Reopened.** The reason it was declared dead is an arithmetic error (F-S1). The single-scale retuned version already gives `n^{(D+2)/(D+3)}`, and with F6 the pricing scale lives in dimension `d`, giving `n^{(d+2)/(d+3)}`. Two scales is then not a rescue but a refinement: the pricing and allocation grids are *already* different objects. | Section 1, Section 2 |
| 2. One global monitor | **Alive, with a proved floor.** It removes the `sqrt(J n log n)` monitoring term and replaces it by `sqrt(n log n)`, which Theorem S1 shows it cannot go below while it remains a cumulative-deficit test. Unchecked: whether a single global monitor still deters a deviator that shades only on a small region, since the global test aggregates and a localised shortfall of size `o(sqrt n)` is invisible; that is a deterrence question, not a false-alarm question, and I did not resolve it. | Corollary S1.1; open point recorded |
| 3. Estimate the capacity function, not the cell values | **Alive and now the main line.** F6 makes this the right frame: `M_j` is one `L`-Lipschitz function on `[0,1]^d`. My Section 2.3 argues the metric entropy of that class still forces `eps^{-(d+2)}` effective samples, so function estimation changes `D` to `d` but does not remove the count; the count is affordable. The genuinely new difficulty, which I did not resolve, is that the observations are adversarially chosen within `[0, M_j(x_j)]`, so the estimator recovers a lower envelope, not the function. | Section 2 |
| 4. Remove the bidding phase | **Partly closed.** It can remove the `J L` term, which is the term both C2 provers show is attained, and F-S3 says even a phase-based design can shrink that term to `O_inst(log n)` for the top agent. It cannot remove the `sqrt(J n log n)` or `sqrt(n log n)` monitoring concession while it still stops exploitation on a cumulative deficit (Corollary S1.3). | Section 3, Corollary S1.3 |

**Summary of the obstruction, corrected.** The obstruction is not that a continuum has too many
regions. At the correctly balanced scale it has `n^{d/(d+3)}` of them, a vanishing fraction of `n`.
The obstruction, to the extent that one survives, is (i) the monitoring concession
`Omega(sqrt(J n log n))`, which is provable and lower order, and (ii) the fact that capacities are
identifiable only from below, because an agent with capacity `M` can imitate any capacity `M' <= M`
exactly. Point (ii) is the one I would attack next and it is the only place I see where the
continuum could be genuinely harder than the finite case: on a continuum an agent can choose *where*
to reveal, and a mechanism that prices off a lower envelope of adversarially chosen observations has
no obvious guarantee. I did not formalise it.

# 8. What I did not do, and the step I consider least secure

**Not done.**

1. No mechanism, no positive result, no rate for the continuous private problem. Sections 1 and 2
   are cost accounting for a mechanism that does not exist; PROVER2's Section 9 item 1 lists the
   real obstacles to writing one and none of them is addressed here.
2. No unconditional lower bound. Section 5 is a record of four failures.
3. The anti-concentration converse of Section 5(c) is a real gap in Corollaries S1.1 to S1.3.
4. I did not check whether the contextual analogue of Braverman et al. Lemma 14 holds, that is
   whether `E sum_t M_(2)(X_t)` is the right ceiling on a continuum. I believe it follows by applying
   Lemma 14 on a positive-mass region, but I did not write it and it must not be cited.
5. I did not attack the C2 provers' work; that is the adversary's job and its report is separate.
6. Section 2.2's architecture (pricing on a per-agent `d`-grid, robustness delegated to a
   `D`-dimensional Grid-EXP3 fallback) is a sketch. The scheduling condition the adversary flags in
   F6, that a profile may enter Stage 2 only once every coordinate bid it uses is complete, is
   unresolved, and it is where I would expect an interleaving argument to break.

**Least secure step.** Theorem S1's proof is elementary and the numerical check is unambiguous, so
my doubt is not there. It is in **Definition S1, the class**, for exactly the reason my previous
report named: I defined the monitored phase so that agent `i` receives *every* pull of the phase
until termination. A mechanism that interleaves the monitored agent with others, or that restarts
the monitor, or that randomises the boundary, is outside the class, and the boundary-tracking
strategy's survival argument uses the deterministic known boundary in an essential way (the agent
computes `Delta B(r)` exactly). I expect the theorem to survive interleaving and restarts with a
worse constant, but I did not prove it, and per the brief I am not entitled to say it looks easy.

The second least secure item is the claim in Section 2.3 that metric entropy forces `eps^{-(d+2)}`
effective observations. That is the standard minimax statement for Lipschitz regression, but the
observations here are *not* a regression design: they are chosen by a strategic agent inside
`[0, M_j(x_j)]`, and the standard minimax lower bound does not apply verbatim. I stated it as a
belief and it should be treated as one.
