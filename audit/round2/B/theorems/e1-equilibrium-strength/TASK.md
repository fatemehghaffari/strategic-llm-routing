# Task brief: how strong is the equilibrium, for the private scalar mechanism

Queued 18 September 2026. First in the queue. Launch when a concurrency slot frees.

## Why this exists

Every incentive result in this paper is a statement that one profile is an equilibrium against unilateral
deviations, in expectation, up to a sublinear additive slack. The private theorem says in its own text that
it "does not assert high revenue in every equilibrium". Nobody has asked what the rest of the equilibrium
set looks like, and nobody has asked what two agents can do together. At a multiagent systems venue these
are the first two questions a mechanism-design reviewer asks, and the paper has no answer to either.

This track attacks the mechanism that already exists and is already proved, so its foundation is solid. That
is deliberate: it strengthens the paper's strongest result rather than its weakest.

Read first, in full: `audit/round2/prompts/COMMON.md`, `sections/Private_information_setting.tex`,
`sections/appendix_private.tex`, `audit/round2/B/PRIVATE_BOUND_NOTES.md`, and
`audit/round2/B/CONTEXT_PROOF_CONTRACT.md` for the strategy classes and notation.

## Task 1. What else is an equilibrium

Characterize the set of additive equilibria of the monitored empirical second-price mechanism in the declared
behavioral class, not just the proposed profile.

The concern to settle first, because it is the one most likely to be real. A winner's per-round utility is
decreasing in the announced price, and the price is the second-highest bid shaded down. Bidding is costly,
because a bid is delivered performance during the bidding phase. So every agent prefers a lower price, and
the price is driven by the others' bids. That combination is what sustains mutual underbidding in costly-bid
settings, and if it survives the monitor and the fallback here, then the mechanism has a family of
low-revenue equilibria and the revenue guarantee holds only at a profile the agents have no reason to select.

Settle it. Either exhibit a family of low-bid profiles that are additive equilibria, with the deviation check
done against the full behavioral class including the monitor and the fallback, or prove that the monitor, the
price shading, or the fallback comparator rules them out. A negative answer is the more valuable one if it is
true, because it is a limitation of the paper's headline result that a referee would otherwise find.

If bad equilibria exist, then say what can be done about them, in this order of preference: a revenue bound
over the whole equilibrium set, which is the useful statement; a modification of the mechanism that shrinks
the set, with its cost stated; or a clean statement that selection is open.

## Task 2. Coalitions

Every guarantee here is unilateral. Quantify what a coalition of two can extract.

My expectation, which you should try to refute rather than confirm: two agents who jointly underbid drag the
price down, and the monitoring boundary does nothing about it, because both of them then comply with the
lower price and never trigger a switch. If that is right, produce the sharp statement, meaning the per-round
gain to the coalition and the revenue loss to the platform, as a function of the instance. Check whether the
fallback, the exclusion rule, or the honest-agent comparator limits it.

Then state what survives. The honest-benchmark guarantee is claimed for arbitrary joint behavioral play, so
it should survive collusion by construction; verify that it does, since it is the property that would make a
negative coalition result tolerable.

## What good output looks like

A theorem, in either direction, with a complete proof. A sharp negative result is worth more than a vague
positive one. Do not repair the mechanism unless the repair is proved and its cost is stated.

Numerical work is encouraged and is likely to be decisive here. Small exact computations over two-agent and
three-agent instances, using the exact backward-induction machinery already in
`scratch/experiments/round2/exploitability/dp.py`, can confirm or kill a candidate bad equilibrium far faster
than analysis. Python venv:
`<scratch>/venv/bin/python`.
Nothing heavy on the login node; use sbatch, partition cpu, account <slurm-account>.

## Standing rules

Read-only on every canonical file. Write only under
`audit/round2/B/theorems/e1-equilibrium-strength/` and the scratchpad. Invent no lemma, citation or step. No
em dashes and no triple hyphens. Write incrementally so partial work survives an interruption. Do not claim a
result is correct; state what you proved and what you assumed, and name the step you consider least secure.
