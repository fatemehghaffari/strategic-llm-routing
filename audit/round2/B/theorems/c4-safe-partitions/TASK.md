# Task brief: which partitions are safe against strategic agents, and an adaptive one

Queued 18 September 2026, to launch when a concurrency slot frees. Priority raised from the last round's
"do not select", which was a page-budget decision that no longer applies.

## Why this exists

The contextual section's weakest point is that its construction is the obvious baseline. A fixed grid with
fresh per-cell statistics is what anyone would try first, and the paper offers no reason it is the right
choice rather than the easy one. The material below turns that into a characterization: it is not that a
fixed grid is convenient, it is that a partition may depend on the contexts and must not depend on the
rewards, and the standard reward-adaptive alternative is manipulable.

## What is already proved, and must be written out rather than redone

In `audit/round2/B/scouts/CONTEXT_ONLY_PARTITIONS.md`:

- Section A.2, occupied-cell accounting. Every cell count in the grid bounds may be replaced by the number
  of positive-mass cells, so the bounds scale with the covering number of the context support at scale `h_n`.
- Section B.3 and B.4, Lemmas B.1 and B.2, the generalized cell law. For any partition process that is a
  measurable function of the contexts alone (R1), with label-local fresh statistics (R2), under exogenous
  arrivals (R3), every cell epoch is a fixed-mean instance with the future-independence the existing proofs
  need. Complete proofs are on disk.
- Section C.2', DE-Grid. Doubling epochs with a fresh static grid per epoch give anytime versions of every
  grid theorem at the same rates, which removes the known horizon from the contextual results.

## What is not proved and is the actual work, in priority order

1. **The converse, which is what makes the principle worth stating.** Section B.5.b classifies
   reward-dependent splitting as INCOMPLETE, not false, and the claim that its pathwise monotonicity fails by
   a linear margin is recorded as announced but not on disk. Either prove it with an explicit instance and an
   explicit deviation, or establish the weaker honest statement and say exactly what remains open. Do not
   assert manipulability without a witness. If reward-adaptive splitting turns out to be fine, that is an
   equally publishable finding and you should say so.
2. **COAT**, the context-only adaptive tree: dyadic splitting triggered by a leaf's own since-creation visit
   count, fresh statistics per leaf, needing neither the horizon nor the Lipschitz constant nor the context
   law, anytime. Section C.2 states the algorithm; Section D, which was to contain Theorems D.1 to D.5 and
   the rate `n^{(d_nu+2)/(d_nu+3)}` under a dyadic covering assumption, is not on disk and does not exist.
   The counting argument for the rate is the missing piece.
3. **The citations.** The ledger records that the primary-source check on Perchet and Rigollet's ABSE and on
   Slivkins' contextual zooming was assigned and never done, and that they must not be cited without it.
   Verify both from primary sources, record the URL and the date, and state precisely how each differs from a
   context-only partition. This matters because the paper's claim to novelty here is exactly that contextual
   zooming is reward-adaptive and therefore outside the safe class.

## Standing rules

Read `audit/round2/prompts/COMMON.md` first and obey it. Read-only on every canonical file; write only under
`audit/round2/B/theorems/c4-safe-partitions/` and the scratchpad. Invent no lemma, citation or step. No em
dashes and no triple hyphens. Write incrementally. A weaker theorem with a complete proof displaces a
stronger one with a gap, and an explicit counterexample displaces both.
