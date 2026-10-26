# Task brief: private capacities, continuous contexts, behavioral deviations

Queued 18 September 2026. Third in the queue. This is the most ambitious target in the project and the one
most likely to return nothing usable. Read the deliverable section before starting, because it is written so
that the track has a floor.

## The target

A mechanism for the contextual model that simultaneously has private capacities, continuous context profiles,
and a deviation class of arbitrary feasible nonanticipating behavior rather than maps fixed before play. The
paper currently disposes of this in one sentence, that private contextual incentives remain open.

Read first, in full: `audit/round2/prompts/COMMON.md`, `audit/round2/B/CONTEXT_PROOF_CONTRACT.md`,
`sections/Private_information_setting.tex`, `sections/appendix_private.tex`,
`sections/contextual_samf_algorithm.tex`, `sections/appendix_contextual.tex`, and
`audit/round2/B/MATH_CANDIDATE_LEDGER.md` Sections 4 and 6.1. Ask the coordinator for the finite-context
provers' findings before you commit to a construction; that work is the finite special case of yours and may
have been refuted.

## Why the obvious route fails, which is where you start

Localising the scalar mechanism to grid cells does not scale. The bidding phase is paid once per cell, so
with many cells the exploration cost alone is linear; forcing it sublinear caps the number of cells, which
forces coarse cells, which reinflates the approximation error. Balancing the two gives a rate far worse than
the public contextual results, near one minus one over three times the dimension plus one. The monitoring
slack has the same problem: one martingale per cell costs the square root of cells times horizon rather than
the square root of horizon.

So the two terms to attack are the per-cell bidding block and the per-cell monitoring slack. Do not spend the
window on sharper analysis inside the cell-based frame. It is the accounting that is wrong, not the bookkeeping.

## Four routes, from least to most radical. You are not restricted to these

1. **Two scales.** A coarse grid for pricing over a fine grid for allocation, so the exploration cost and the
   approximation error are governed by different resolutions and stop fighting each other.
2. **One global monitor.** Replace the per-cell martingale with a single one comparing an agent's cumulative
   delivered reward against the cumulative announced price across all contexts. The slack becomes the square
   root of the horizon once, not per cell. Check whether the false-elimination control and the deterrence both
   survive when the test no longer localises.
3. **Estimate the capacity function, not the cell values.** An agent's capacity is a smooth function of the
   context, and the grid throws that away by estimating each cell separately. If bidding is treated as
   estimating one function from a smoothness class, its cost is the cost of one nonparametric estimate rather
   than many independent ones. The strategic content is new: the agent chooses what you observe while you
   estimate, so the estimator must be robust to adversarially chosen observations within the feasible set.
4. **Remove the bidding phase.** Bidding exists only to learn the runner-up's capacity. If the price at a
   context can be derived from other agents' ongoing realized performance near that context, there is no
   dedicated exploration block and the term that causes the whole obstruction disappears. This deletes the
   problem rather than balancing it, and it is the route I would try first.

Departures from cell-based geometry are welcome and expected. So are departures from second pricing: a menu, a
contract over a performance function, a bid that is a function rather than a number, or a scoring rule are all
in scope if you can make one work.

## Team structure: two workers with opposite dispositions, run against each other

This track is staffed by two agents with deliberately different jobs, because the two failure modes of an
ambitious search are wandering and wishful thinking, and each worker is the antidote to the other's.

**The sceptic.** Assumes the full combination is impossible and tries to prove it. Builds lower bounds,
looks for the information-theoretic reason the exploration cost cannot be avoided, and constructs explicit
instances that defeat each proposed construction. Its output is a theorem about what any mechanism must pay,
or a catalogue of counterexamples with the precise place each route dies. This worker exists so that the
track cannot return empty, because a sharp impossibility is a publishable result and a mapped obstruction is
a useful one.

**The explorer.** Assumes it is possible and looks for the technique that does it, deliberately outside the
frame this paper has used. Contract theory and menus, scoring rules and proper elicitation, nonparametric
function estimation under adversarially chosen observations, sequential testing and change detection,
optional stopping, online convex optimisation, posterior sampling, sleeping bandits, and anything else that
fits. It should read outside the strategic bandit literature on purpose, and it must verify every imported
result against a primary source before building on it. Its output is a mechanism and a proof, or the
strongest partial version it can actually establish.

They work independently and exchange findings through the coordinator, not directly. When the explorer
proposes a construction the sceptic attacks it, and when the sceptic claims an obstruction the explorer must
either respect it or break it. A construction that survives the sceptic goes to the two-prover protocol like
any other candidate. Neither worker may weaken the standard of proof to reach agreement, and a disagreement
recorded honestly is a better outcome than a compromise nobody checked.

## What the separation worker already established, and how it feeds this track

The separation track finished on 18 September and its report is at
`audit/round2/B/theorems/separation/REPORT.md`. Read it before starting. Three things in it are directly
usable here, and the sceptic role is assigned to that same worker because it already holds the context.

**The technique, which is the sceptic's main lead.** Its argument is a forced-noise argument: under Bernoulli
delivery an honest agent's mean lies strictly inside the unit interval, so both outcomes occur with
probability at least the gap, and therefore any mechanism that reacts to a realization pays an unavoidable
cost. The agent cannot suppress the variance because it does not choose the realization, only its mean. That
is exactly the shape the exploration lower bound needs. Estimating a runner-up's capacity near a context to
a given accuracy costs a number of Bernoulli samples that the instance dictates and no mechanism can talk its
way out of; if capacities are Lipschitz and contexts are continuous, that cost must be paid at every scale
at which the price matters. Whether that assembles into a bound on the total exploration any mechanism must
spend is the sceptic's first target, and it is a far more promising route than starting from scratch.

**The warning, which is where these arguments die.** The separation theorem's least secure part was not a
proof step but the class definition: a rule that protects the last active agent escapes the class, and no
repair covering that case was found. Defining the class of mechanisms tightly enough to prove something and
loosely enough to be interesting is the hard part of an impossibility result, not the probability
calculation. Expect to spend most of the effort there, and record honestly which natural mechanisms fall
outside whatever class you can handle.

**The tool, which is for the explorer.** That report proves a doubling-epoch version of the manuscript's own
adversarial-learning lemma from the potential argument directly, valid for any prefix, and pins the absolute
constant at three times two plus root two. Any mechanism that operates on regions whose local horizon is
unknown in advance needs exactly this, so it is a building block rather than something to rederive.

Also read Lemma 14 of Braverman, Mao, Schneider and Weinberg, which is the closest existing impossibility in
this literature: no truthful mechanism can beat the second-best arm in the worst case. It bounds the
benchmark, not the exploration cost, so it is a starting point and not an answer.

## Deliverable, and its floor

One of the following, in decreasing order of value.

1. A mechanism with a complete proof, for whatever combination of the three relaxations you can actually get.
   A theorem under a restricted but natural class beats a sketch of the full thing.
2. A lower bound. Show that any mechanism achieving the second-capacity benchmark against behavioral
   deviations on continuous contexts must pay a cost of a stated order. This would replace the paper's
   one-sentence admission with a theorem explaining why the problem is hard, and it is a genuine
   contribution. Do not expect it to be easy, but it is the more likely of the two to land.
3. A precise map of the obstruction: the exact place each of the four routes breaks, with a counterexample or
   an explicit cost accounting for each. This is the floor and it is still useful, because it turns an open
   problem into a structured one.

Returning route 3 honestly is a success. Returning route 1 with a gap in it is a failure.

## Standing rules

Read-only on every canonical file. Write only under `audit/round2/B/theorems/f1-continuous-private/` and the
scratchpad. Invent no lemma, citation, theorem or step; verify any literature fact against a primary source
and record the URL and date. No em dashes and no triple hyphens. Write incrementally. A weaker theorem with a
complete proof displaces a stronger one with a gap. Name the step you consider least secure, and do not claim
a result is correct.

New mathematics for this paper stops on 28 September. Anything unproved by then is recorded as an open
problem, which is where it already is, so there is no cost to trying.

---

# STATE OF THIS TRACK, 18 September 2026, after the sceptic reported

**The premise of this brief was wrong and the explorer must not follow it.** Sections above tell you to
leave the cell-based frame because a bidding block paid per region makes a fine partition unaffordable. The
sceptic showed that conclusion rests on an arithmetic error, and I verified the correction independently by
numerical minimisation over both parameters at horizons from ten to the eighth up to ten to the
twenty-fourth.

The error: the rate that condemned the route came from pinning the per-region bidding length at the scalar
value, which solves the scalar balance. With many regions the balance changes and the length must be
re-solved. Re-solving gives a per-region bidding length of `n^(2/(m+3))`, polynomially smaller than the
scalar `n^(2/3)`, a cell side of `n^(-1/(m+3))`, and a total cost of `n^((m+2)/(m+3))`. My fits reproduce
both the wrong exponent under pinning and the corrected one under re-solving, to five digits, for `m` in
one, two, three, four and six.

For `m = D` that is exactly the exponent of the existing public contextual result. So a private contextual
mechanism need not be worse than the public one, which is the opposite of what this brief assumed.

**Revised target.** Aim at `n^((d+2)/(d+3))`, using the adversary's finding that an agent's capacity depends
only on its own context block, so pricing lives in the per-agent dimension `d` rather than the full profile
dimension `D = Kd`. Fall back to `n^((D+2)/(D+3))` if the per-agent architecture cannot be made safe.

**What is genuinely in the way, now that the false obstruction is removed.** Read `SCEPTIC.md` in this
directory in full, then the second prover's Section 9 item 1. The real obstacles are that a cell-average bid
is not a capacity, that an announced price can exceed an agent's capacity at some contexts inside a cell and
not at others, and that bid domination loses its fixed comparison target. None of these is about counting
regions.

**The deepest one, and where I would attack.** Capacities are identifiable only from below: an agent of
capacity `M` can imitate any smaller capacity exactly. So a mechanism estimating a capacity function is
estimating a lower envelope of adversarially chosen observations rather than a regression function, and on a
continuum the agent also chooses where to reveal. The sceptic names this as the only place it can see where
the continuum is genuinely harder than the finite case, and it did not formalise it.

**Two proved facts to build on rather than rediscover.** The sceptic's Theorem S1 shows that any mechanism
stopping exploitation on a cumulative deficit against a square-root boundary concedes an amount of order the
square root of the horizon times a logarithm, so do not aim below that. Its earlier Grid-EXP3 theorem gives
the honest benchmark against arbitrary nonanticipating behaviour and arbitrary oblivious context sequences,
using no pooled estimate, which is exactly the component a per-agent pricing architecture needs to delegate
robustness to.

**One device neither our mechanism nor either candidate has.** Both prior mechanisms in this literature pay a
non-winner a number of rounds keyed to its revealed value, which is what makes revelation consequential for
an agent that will not win. Ours has no reward phase at all. The sceptic flags this as untested here because
a report is an empirical mean rather than an exact value, so the incentive is smeared.

**Safety caveat you must respect.** The known counterexample against per-agent cells shows that a strategic
agent's delivered mean is not measurable in its own coordinate, so pooling is unsafe for any quantity that
must be correct under arbitrary behaviour. It says nothing about pooling a quantity that need only be correct
at the proposed profile, where every agent delivers its capacity, which is own-coordinate measurable. That
distinction is a concern, not a result, and if you build on it you must prove it.
