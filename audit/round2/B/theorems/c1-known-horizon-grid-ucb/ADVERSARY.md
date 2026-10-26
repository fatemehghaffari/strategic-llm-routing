# ADVERSARY report: candidate C1 (known-horizon cell-local Grid-UCB) plus C0

STATUS: COMPLETE (17 September 2026). VERDICT: no counterexample to the target
statements S0 to S8. Eight adjacent or stronger statements are broken with explicit
instances; see the ranked list of weakest points at the end.

## Headline

No counterexample to S0, S1, S2, S3, S4, S6, S7 or S8 has been found. The two
priority attacks, (A) the region identity and (B) the one-priority-per-cell race
argument, both FAIL to break the targets; both survive exact enumeration and
exhaustive small-case search, and in my assessment they are the two SOUNDEST parts
of the candidate rather than the weakest.

Statements that ARE false, each with an explicit verified instance below, because a
prover who states any of them would be wrong:
- A3: the region identity, if the cell's COINS may depend on the exact within-cell
  position (off by 0.155 at `n = 5` in an explicit instance).
- B4: pathwise monotonicity of the cell LOCAL-TIME index, which is the rule the
  manuscript describes and the experiment code runs (`K = 3`, 6 cell visits).
- C1: pathwise grid monotonicity under the ACTUAL-VISIT coupling (`K = 3`, 6 cell
  visits, exhaustively minimal).
- D1: contextual sharp adaptivity for an arbitrary region WITHOUT the boundary
  term (fails by `n/8`).
- D2: expected contextual FATA WITHOUT `nu(partial G) = 0` (fails by about
  `0.14 n`).
- D3: the public equilibrium WITHOUT two-top almost everywhere (gain about
  `0.16 n`).
- H1: EXACT FATA with a per-cell priority that is fixed but not uniform.
- F1: the pairing of split point and constant stated in TASK.md S8 (the
  inequality itself is true, but the stated split does not yield the stated
  constant).
Attacks B5 and C2 kill two shortcuts a prover is likely to take; they are not
statements of the candidate.

No Slurm job was submitted: every run above finished in at most a few minutes on
the login node.

Scripts: `<scratchpad>/round2/B/c1_adversary/` (venv python named in COMMON.md).
All expectations below are exact rationals from full enumeration over context
sequences and reward realizations, not Monte Carlo, unless stated.

***

## Attack A1. The region identity, exact enumeration (does NOT break the target)

Target: `E T_j(C cap R; n) = nu(R | C) E T_j(C; n)` for a cell `C` with
`nu(C) > 0`, measurable `R`, cell-local KH-UCB with one ex ante priority `pi_C`.

Instances (all with an ATOMIC conditional law on the cell, which is the hardest
case for "the position leaks through the rewards", since the reward then reveals
the position exactly):

- A1.1 One cell, two pieces of very unequal mass, rewards that reveal the piece
  deterministically. `K = 2`; positions `A` (mass 1/50) and `B` (mass 49/50), both
  in cell `C`; `R = {A}`, so `nu(R|C) = 1/50`; maps `m_0(A) = 1, m_0(B) = 0`,
  `m_1(A) = 0, m_1(B) = 1`. Every reward is a deterministic function of the
  position, so the cell's own data determine the entire past position sequence.
  `n = 2,3,4,5,6`: identity holds exactly for every agent.
- A1.2 `K = 3` with `n = 1,2,3` so that the cell is visited FEWER THAN K times with
  high probability: initialization is incomplete, agent 2 is never selected on
  many paths, and the first-visit case is included as `n = 1`. Identity holds
  exactly (for `n = 1` both sides are `nu(R|C) Pr(visit)` times the indicator of
  the priority-first agent).
- A1.3 Two cells (`C` with pieces `A`, mass 1/100, and `B`, mass 39/100; cell `Z`
  with mass 60/100), so `V_C` is random, heavily dependent on the realized context
  sequence, and dependent on which agent is selected in the OTHER cell.
  `R = {A, Z}` cuts `C` into pieces of mass ratio 1 : 39. `n = 3,4,5,6`: identity
  holds exactly.
- A1.4 `K = 3`, two cells, distinct non-identity priorities per cell
  (`pi_C = (2,0,1)`, `pi_Z = (1,2,0)`), `n = 5`: holds exactly.
- A1.5 Three pieces in one cell with masses 1/7, 2/7, 4/7 and `R` a union of two
  of them, `n = 3,4,5,6`: holds exactly.

Outcome: DOES NOT BREAK. Script `attackA.py`, 0 violations.

## Attack A2. Where exactly the leak would have to be, and what does leak

The lead's stated reason ("the decision at visit `k` is measurable with respect to
the data of the first `k-1` visits and the cell's coins, hence independent of the
`k`-th visit's profile") is the right one, and the enumeration confirms it, but
the reason is worth stating in the form that survives every attack I tried:

  Let `B = (1{X_t in C})_{t <= n}` be the membership sequence and
  `X^{(1)}, X^{(2)}, ...` the ordered profiles visiting `C`. Conditionally on `B`,
  the `X^{(k)}` are i.i.d. `nu(. | C)` and independent of everything else.
  `{V_C >= k}` is `B`-measurable. The selected agent at the `k`-th visit,
  `I^C_k`, is a function of `(B, pi_C, X^{(1..k-1)}, U^{(1..k-1)})`. Hence
  `E[1{V_C >= k} 1{I^C_k = j} 1{X^{(k)} in R}] = Pr(V_C >= k, I^C_k = j) nu(R|C)`,
  and summing over `k` gives the identity. The same computation with a bounded
  `g` in place of `1_R` gives the form the equilibrium proof actually needs,
  `E sum_{k <= V_C} 1{I^C_k = i} g(X^{(k)}) = E[T_i(C)] E[g(X) | C]`.

Three things I attacked and which do NOT create a leak:

1. Heavy dependence of `V_C` on the realized contexts, and dependence between
   `V_C` and the identity of the selected agent: irrelevant, because both are
   functions of `(B, past positions)` and the `k`-th position is independent of
   those GIVEN `B`, and `{V_C >= k}` is `B`-measurable. Verified in A1.3.
2. The rewards of visits `1..k-1` revealing the earlier positions exactly (atomic
   `nu(.|C)`, deterministic maps): irrelevant, because the earlier positions are
   independent of the `k`-th position. Verified in A1.1.
3. The GLOBAL round. I re-ran the enumeration with the manuscript's ANYTIME index
   `hat m + sqrt(2 log t / T)` (global `t`, cell-local counts): the identity still
   holds exactly (`n = 3,4,5`, script `attackA2.py`). Reason: the global round of
   the `k`-th visit to `C` is `B`-measurable, hence independent of `X^{(k)}`.
   CONSEQUENCE FOR THE PROVERS: the region identity is NOT where the known-horizon
   index is needed. It holds for the manuscript's rule too. The index change is
   needed only for the race argument (S0/S1), never for S3's identity. A proof
   that claims the identity needs `log n` is overclaiming.

## Attack A3 (BREAKS A STRONGER STATEMENT). The identity is false if the cell's
COINS depend on the exact within-cell position

Cell blindness of the INDEX is not enough; the cell's priority permutation must
also be independent of the within-cell positions. Explicit instance (script
`attackA2.py`, rule `sel_leaky`, exact enumeration):

`K = 2`; positions `A` (mass 1/10), `B` (mass 4/10) in cell `C`, `Z` (mass 5/10)
in cell `Z`; `R = {A, Z}`, `nu(R|C) = 1/5`; maps `m_0 = (A:1, B:0, Z:1/2)`,
`m_1 = (A:0, B:1, Z:1/2)`. Rule: cell-local KH-UCB with `c = 4`, but the cell's
priority is `(0,1)` if the cell's FIRST visit fell in `A` and `(1,0)` if it fell
in `B`. Then for `n = 5`:
`E T_0(C cap R) = 7173/20000 = 0.35865` while
`nu(R|C) E T_0(C) = 4073/20000 = 0.20365`; the identity is off by `0.155`, which
is `3.1 %` of `n` in this instance and scales linearly in `n`.

Outcome: BREAKS ONLY A STRONGER STATEMENT (a version of the identity whose
hypothesis is only "the index ignores the within-cell position"). It does not
break S3, but it shows the hypothesis is not vacuous. REQUIREMENT FOR THE PROVERS:
the statement of the cell-blindness hypothesis must be "`I^C_k` is a measurable
function of `(B, pi_C, X^{(1..k-1)}, U^{(1..k-1)})`", i.e. the LAZY draw of `pi_C`
at the cell's first visit must use randomness independent of the contexts (a draw
indexed by the global round of the first visit, or by the number of cells
initialized so far, is fine, because both are `B`-measurable; a draw seeded by the
first visit's exact profile is NOT, and the manuscript's phrase "cells are
initialized lazily" does not by itself exclude it).

***

## Attack B1. One priority per cell versus interleaving in global time (does NOT break)

Target: the race argument transfers from the scalar instance to a cell whose
visits are interleaved with other cells in global time.

What I checked and what makes it work. Conditionally on the membership sequence,
the cell `C` execution is a deterministic function of exactly three objects: the
number of visits `V_C`, the priority `pi_C`, and the cell's own reward tape. It
touches global time nowhere, BECAUSE the bonus is `sqrt(4 log n / T_a)` with the
constant `n`. In the monotonicity comparison the contexts are coupled, so `V_C`
and the whole membership sequence are IDENTICAL in the two executions; therefore
the `k`-th visit to `C` occurs at the SAME global round in both, and the cell's
local state at that visit is the state of a `V_C`-round scalar instance. This is
the precise sense in which interleaving is harmless and I could not defeat it.

Search evidence (script `attackB4.py`, tape-driven, fixed priority, index
`hat m + sqrt(4 log n / T)`): `K in {3,4}`, `n in {8,10,12}`, 2.25 million random
raise pairs on 0/1 tapes, checked at the final time: 0 violations.

Consequences I verified about the hypotheses of the per-cell priority:
- The per-cell priorities need NOT be independent across cells and need not be
  uniform for MONOTONICITY: the monotonicity argument is applied cell by cell
  conditionally on `pi_C`, so any fixed (even deterministic and identical across
  cells) priority works. Uniformity of `pi_C` is needed only for FATA (label
  symmetry) and for the paper's "removes finite-horizon label asymmetry" remark.
- Lazy versus pre-drawn priorities: identical in law, and identical pathwise in
  the coupling, PROVIDED the lazy draw is not a function of the exact profile.
  If `pi_C` is the value at index `tau_1(C)` of an independent i.i.d. stream,
  where `tau_1(C)` is the global round of `C`'s first visit, then `tau_1(C)` is
  membership measurable and distinct cells consume distinct indices, so the
  `pi_C` are i.i.d. uniform and independent of the within-cell positions, and
  they are the same in the two coupled executions. Attack A3 above shows what
  fails if the lazy draw is seeded by the first visit's position.

Outcome: DOES NOT BREAK.

## Attack B4 (BREAKS A STATEMENT THAT THE MANUSCRIPT AND THE CODE ACTUALLY USE).
The cell LOCAL-TIME index is not pathwise monotone even with one fixed priority

This is the attack the Addendum's rule L3 demands be made explicit, and it is
sharper than the lead's Claim L3. The manuscript describes Static Grid-UCB1 as
"independent cell-local symmetric local-time UCB1 instances (local time = cell
visit count)" and the experiment code (`scratch/experiments/final/
contextual_performance/run.py`, class `CellUCB`) uses
`z/n + sqrt(2 log(max(2, n.sum()))/n)` with `n.sum()` the cell VISIT COUNT. That
index is not a function of the arm's own count alone, so S0 does not apply, and
it is in fact NOT pathwise monotone. Minimal exhaustive counterexample (script
`attackB4min.py`, exhaustive over all 0/1 tapes, smallest `n` for `K = 3`):

`K = 3`, `n = 6` cell visits, index `hat m_a + sqrt(2 log(max(2, v-1)) / T_a)`
with `v` the current visit index, fixed priority `0 > 1 > 2`, initialization in
priority order. Own-count-indexed tapes:
  base: arm 0 `(0,0,0,0,0,0)`, arm 1 `(0,0,0,0,0,0)`, arm 2 `(1,0,0,0,0,0)`;
  raised: arm 0 `(1,0,0,0,0,0)`, arms 1 and 2 unchanged.
Bonuses: `v = 4` gives `sqrt(2 log 3 / T)`, `v = 5` gives `sqrt(2 log 4 / T)`,
`v = 6` gives `sqrt(2 log 5 / T)`.
  Base run: visits 1 to 3 initialize (rewards 0, 0, 1); visit 4 indices
  `(1.482, 1.482, 2.482)` pull arm 2 (reward 0); visit 5 indices
  `(1.665, 1.665, 1.677)` pull arm 2 (reward 0); visit 6 indices
  `(1.794, 1.794, 1.369)` tie between 0 and 1, priority gives arm 0.
  Counts `(2, 1, 3)`.
  Raised run: visit 4 indices `(2.482, 1.482, 2.482)`, the tie goes to arm 0
  (reward 0); visit 5 indices `(1.677, 1.665, 2.665)` pull arm 2 (reward 0);
  visit 6 indices `(1.769, 1.794, 1.769)` pull arm 1. Counts `(2, 2, 2)`.
Arm 1's count RISES from 1 to 2 when arm 0's tape is raised pointwise.

Random search confirms this is not isolated: `attackB4.py`, `K = 3, n = 8`;
`K = 3, n = 12`; `K = 4, n = 10` all produce violations within a few hundred
random raise pairs, while the `log n` index produced 0 in 2.25 million.

Outcome: BREAKS the pathwise monotonicity of the rule the manuscript and the code
actually run. It does NOT break C1, whose rule is `log n`. REQUIREMENT: the
provers must flag that C1 changes the grid index in TWO ways relative to the
manuscript (the manuscript's cell rule uses the cell's local time in the
logarithm, not the global round and not `log n`), and the paper must not describe
C1's rule as "the same algorithm with a different confidence level" or reuse the
experiment code's numbers as evidence for the monotone rule. This counterexample
also shows that S0's hypothesis "the index is a fixed function of the arm's own
count and own reward prefix" is exactly the right hypothesis and is violated by
the natural cell-local reading of the manuscript.

## Attack B5. Tie coins indexed by the global round inside a cell (does NOT break
C1, but corrects a natural but wrong intuition)

A natural defence of per-round fresh tie coins in the grid is: "the two coupled
executions see the same contexts, so cell `C`'s `k`-th visit is at the same global
round in both, so the same coin is used at the same visit; hence the scalar
counterexample of `scouts/MONOTONE_UCB.md` Section C.1 cannot be reproduced."
That defence is WRONG, and provers must not use it. The coin alignment is not the
issue; the state divergence is. With coins indexed by the visit index (equivalently
by the global round, since the two agree between the coupled runs), the scalar
tape of Section C.1 transfers verbatim to a single cell that is visited at every
round: base tapes arm 1 `(0,...)`, arm 2 `(0,1,1,1,...)`, arm 3 `(0,...)`, raised
arm 1 `(1,0,0,...)`, coin at visit 4 ranking `2 > 3 > 1` and at visit 6 ranking
`3 > 2 > 1`; the raised run postpones the `{2,3}` tie from visit 4 to visit 6,
where the other coin applies, and `T_3` rises from 1 to 2. So one fixed `pi_C` per
cell is genuinely necessary for the PATHWISE statement; what survives with fresh
coins is only the exact EXPECTED statement (scout B1 Theorem C.1), and that
theorem applies inside a cell verbatim because the cell's steps are its visits.

Outcome: DOES NOT BREAK C1 as specified; it kills a shortcut a prover might take.

***

## Attack C1 (BREAKS A STRONGER STATEMENT). Pathwise monotonicity under the
ACTUAL-VISIT coupling is false: the missing counterexample, supplied

The ledger asserts that the actual-visit coupling fails while the cell-average one
works, but scout B1's Section F is not on disk. Here is the counterexample,
obtained by EXHAUSTIVE search over 0/1 maps and all position sequences (script
`attackC_min.py`), smallest in `n` and then `K`:

Coupling attacked: same contexts, same per-visit per-agent reward uniforms
`U_{C,k,a}`, same priority; the reward of the agent selected at cell visit `k` is
`1{U_{C,k,a} <= m_a(X^{(k)})}`.

Instance. One cell with two within-cell pieces `a` and `b`; `K = 3`; six cell
visits at positions `(a, a, a, b, a, a)`; index `hat m + sqrt(4 log 6 / T)`,
priority `0 > 1 > 2`; maps `m_0 = (a:0, b:0)`, `m_1 = (a:0, b:0)`,
`m_2 = (a:1, b:0)`; raised map `m_0' = (a:1, b:0) >= m_0` pointwise. (All maps are
0/1 valued, so the uniforms are irrelevant and the run is deterministic.)
  Base: pulls `0, 1, 2, 2, 0, 1`, counts `(2, 2, 2)`.
  Raised: pulls `0, 1, 2, 0, 2, 2`, counts `(2, 1, 3)`.
Agent 2's count RISES from 2 to 3.

Mechanism, which is the point worth recording: the failure is NOT that the
deviator's own-count-indexed tape stops being dominated (here it is dominated:
`(0,0)` becomes `(1,0)`). It is that the NON-DEVIATING agents' own-count-indexed
tapes CHANGE. Agent 2's second pull occurs at the `b` visit in the base run
(reward 0) and at an `a` visit in the raised run (reward 1), so its tape changes
from `(1,0,...)` to `(1,1,...)`. S0 assumes `f_a' = f_a` for `a != 1`, and under
the actual-visit coupling that hypothesis is false whenever a map is
non-constant inside the cell. Under the cell-average coupling each agent's tape is
`1{U_{C,a,k} <= bar m_{a,C}}`, fixed once the cell means are fixed, so the
hypothesis holds.

Outcome: BREAKS ONLY THE STRONGER (pathwise, actual-visit) STATEMENT; it confirms
that S3 must be an expectation statement and that the cell-average coupling is not
a convenience but a necessity. Note also that `K = 2` cannot produce such an
example: with two arms, at any time the two runs' histories agree, the deviator's
sum is weakly larger and the rival's is identical, so the raised run repeats the
base choice; the first divergence argument closes. So `K >= 3` is necessary here,
exactly as in the scalar counterexamples.

## Attack C2. What the cell-average coupling does NOT give

A reminder that a prover could get wrong: the cell-average coupling is a coupling
of the LAWS of the two cell executions; it does not live on the same probability
space as the contexts. Consequently S3 is a statement about `E T_j(R; n)` only.
The pathwise statement `T_j(R; n; M_i) <= T_j(R; n; m_i)` on the original space
(same contexts, same uniforms) is FALSE by attack C1 already for `R` the whole
space. Any sentence of the form "exact and pathwise" (the phrase the manuscript
uses for Grid-ETC in `thm:grid-etc`) must NOT be carried over to the UCB rule.

***

## Attack G. Lemma `lem:cell-law` itself, at the level of the JOINT law
(does NOT break)

The whole candidate rests on the claim that, conditionally on the membership
sequence, a cell's execution has the law of a fixed-mean instance with means
`bar m_{a,C}`. I tested that claim directly rather than assuming it: for 200
random instances (`K in {2,3}`, atomic `nu(. | C)` with 2 to 4 pieces, random
rational maps, random priority, `s` up to 6 visits) I computed the EXACT
distribution of the full history `(I_1, Y_1, ..., I_s, Y_s)` under
  (a) the real process (position drawn per visit, reward `Bernoulli(m_a(X^{(k)}))`)
  (b) the cell-average tape model (reward `Bernoulli(bar m_{a,C})`),
and compared them as exact rationals. Maximum discrepancy 0 in all 200 instances
(script `attackG.py`). This is the strongest evidence I can produce short of a
proof, and it also certifies the step at which a prover is most likely to hand
wave ("the rewards agent `i` actually delivers are i.i.d. Bernoulli given the
past"): the correct justification is that the selection at visit `k` is
independent of the `k`-th visit's potential rewards, so the selected agent's
reward is `Bernoulli(bar m_{sel,C})` conditionally on the whole past, and the
history law follows by induction on the visit index. No optional stopping, no
martingale, no filtration is needed, in line with the Addendum's rule L1.

## Attack F1. The split algebra of S4 and S8 (does NOT break; the ledger's
constant is better than TASK.md's)

Checked numerically over `n in {2,3,5,10,10^2,10^3,10^6,10^9}`,
`s in {1,...,n}` and 4000 values of `Delta` in `(0,1]`:
- `Delta min{s, 3 + 16 log n / Delta^2} <= 4 sqrt(s log n) + 3`: 0 violations.
- `min{s Delta, 16 log n / Delta + 3 Delta} <= 8 sqrt(s log n) + 3` (TASK.md S8
  form): 0 violations, but it is loose by a factor 2; the constant 4 is correct
  (split at `Delta = 4 sqrt(log n / s)`, not at `sqrt(log n / s)` as TASK.md says;
  with the split at `sqrt(log n/s)` the large-`Delta` branch gives
  `16 log n / Delta <= 16 sqrt(s log n)`, i.e. constant 16, so the split point
  stated in TASK.md S8 and in the ledger does not give the stated constant 8).
  RECOMMENDATION: provers should state the split point as
  `Delta_0 = 4 sqrt(log n / s)` and the constant 4, or state constant 16 with the
  split point `sqrt(log n / s)`; the pair (split at `sqrt(log n/s)`, constant 8)
  in TASK.md is not self consistent, although the inequality with constant 8 is
  true by the better split.

## Attack F2. The imported bound, verified from the primary source and tested
for a random number of cell visits (does NOT break)

Primary source read in this session: Lattimore and Szepesvari, "Bandit
Algorithms", PDF at https://tor-lattimore.com/downloads/book/book.pdf (downloaded
17 September 2026, 5400750 bytes, text extracted with
`gs -dBATCH -dNOPAUSE -sDEVICE=txtwrite`, pages 104 to 108 of Chapter 7 "The
Optimism Principle"). What the source actually says, checked word by word:
- Eq. (7.2), p. 104: `UCB_i(t-1, delta) = +inf if T_i(t-1) = 0`, otherwise
  `hat mu_i(t-1) + sqrt(2 log(1/delta) / T_i(t-1))`. Algorithm 3 is
  `A_t = argmax_i UCB_i(t-1, delta)`, with ties unspecified (arbitrary).
- Theorem 7.1, p. 105: "Consider UCB as shown in Algorithm 3 on a stochastic
  `k`-armed 1-subgaussian bandit problem. For any horizon `n`, if
  `delta = 1/n^2`, then `R_n <= 3 sum_{i} Delta_i + sum_{i : Delta_i > 0} 16 log(n)/Delta_i`."
- The per-arm form the candidate needs is displayed inside the proof of Theorem
  7.2 (p. 108): `E[T_i(n)] <= 3 + 16 log(n) / Delta_i^2`.
- The proof structure (pp. 106 to 108) is `E[T_i(n)] <= u_i + n Pr(G_i^c)` with
  `Pr(G_i^c) <= n delta + exp(-u_i c^2 Delta_i^2 / 2)` and
  `u_i = ceil(2 log(1/delta) / ((1-c)^2 Delta_i^2))`, `c = 1/2`.
Consequences I checked for the candidate's use:
(a) With `delta = 1/n^2` the index is `hat m + sqrt(4 log n / T)`, which is
    exactly the candidate's index with `c = 4`. Bernoulli rewards are
    `1/2`-subgaussian hence 1-subgaussian, so the hypothesis holds.
(b) Ties: the proof's contradiction step uses the STRICT inequality
    `UCB_i(t-1) < UCB_1(t-1)`, so an arbitrary tie rule, in particular the fixed
    `pi_C`, is covered. The bound is therefore compatible with the one-priority
    rule that S0 needs. This should be stated; it is the only place where the
    imported theorem and the monotonicity argument could have been in conflict.
(c) Random number of visits: run the same algorithm (same `delta = 1/n^2`) for
    `s <= n` rounds. In the proof, the union bound (7.7) runs over `s` values
    instead of `n` (so it is still at most `n delta`), and (7.5) becomes
    `E[T_i(s)] <= u_i + s Pr(G_i^c) <= u_i + n Pr(G_i^c)`. Both terms are bounded
    exactly as in the book, so `E[T_i(s)] <= 3 + 16 log n / Delta^2` for every
    deterministic `s <= n`. Conditioning on `V_C = s` is legitimate because the
    cell execution depends on the membership sequence only through the number of
    visits. Then `E T_i(C) <= E[min{V_C, 3 + 16 log n/Delta^2}] <= min{E V_C, ...}`
    by concavity of `min{., c}`. No step of this needs `s` to be independent of
    the cell's rewards beyond what `lem:cell-law` already gives.
(d) Numerical check: exact dynamic programming over `(count, sum)` states for
    `K in {2,3}`, `n in {6,8,12,16,20}`, every `s <= n`, 12 random mean vectors
    each: `E[T_a(s)] <= 3 + 16 log n / Delta_a^2` in every case, 0 violations
    (script `attackF.py`), the tightest observed ratio being 0.063.

## Attack E. The per-cell equilibrium inequality of S8 (does NOT break)

Exact enumeration, 120 random finite-position instances (`K in {2,3}`, 1 or 2
cells, `n <= 6`, random capacities with and without the two-top condition
enforced, random intrinsic means, random feasible deviations, half of them with
the HONEST floor `m'_i >= mu_i` binding, random per-cell priorities). Checked,
exactly, in every cell:
1. the factorization `U_i(C) = E T_i(C) E[1 + mu_i - m_i | C]` (this is attack A's
   identity with a general bounded `g`, and it is what turns per-cell counts into
   per-cell utilities): 0 failures;
2. self-monotonicity `E T'_i(C) <= E T_i(C)`: 0 failures;
3. `gain_C <= E T'_i(C) delta_C`: 0 failures, with equality attained (the
   inequality is tight, so no constant can be saved there).
The honest floor never helps the deviator: it only shrinks the feasible set, and
`a_C = E[1 + mu_i - M_i | C] >= 0` holds for honest and strategic agents alike
because `M_i <= 1`. Small `n`: the claimed bound can exceed `n`, in which case it
is vacuous but true, since the total utility difference is at most `2n`.

The composed chain was checked separately (script `attackE2.py`, 120 further exact
instances with the two-top condition NOT enforced, so that `eta_{i,C}` is often
large): `gain_C <= E T'_i(C) delta_C <= [4 sqrt(E V_C log n) + 3] + eta_{i,C} E V_C`
in every cell of every instance, 0 violations, tightest observed ratio of gain to
bound 0.096. The case split inside the chain that a prover must not forget is
`Delta'_C <= 0` (the deviator is still the cell's best arm), where the deficit
bound is vacuous and one instead uses `delta_C <= eta_{i,C}` directly.

Outcome: DOES NOT BREAK.

## Attack D (BREAKS NOTHING IN THE TARGET, but shows two remainders cannot be
dropped and one hypothesis cannot be weakened)

D1. The boundary term of S4 is necessary, and S4 is vacuous for regions that cut
cells. One cell, two equal-mass pieces `R` and `S`; honest agent `h` with
`mu_h = 1/2` everywhere delivering `1/2`; agent `i` delivering `0` on `R` and `1`
on `S`. Both cell averages are `1/2`, so the cell gap is `0` and the UCB deficit
bound gives NOTHING, while the `R`-restricted deficit is
`E sum_{X in R, I = i} [b(X) - m_i(X)] = n/8` exactly (verified: `n = 2,4,6,8`
give `0.25, 0.5, 0.75, 1.002`, i.e. `0.125 n`). A region `R` of this shape can be
taken grid aligned so that it cuts EVERY cell in half, and then
`nu((partial R)^{sqrt D h_n}) = 1` and the S4 remainder is `n`, so S4 remains
TRUE but says nothing. REQUIREMENT: S4's "for every measurable `R`" must be
stated together with the boundary term, and the paper must not claim contextual
sharp adaptivity "for every region" without the qualifier, since the failure is
linear, not `o(n)`.

D2. The boundary term of S6 (FATA) is necessary, with a linear failure. Same
cell; on the piece `R` (which is `G_{ij}`) agents 0 and 1 both deliver
`M_* = 1/2`; off `R`, agent 0 delivers `1` and agent 1 delivers `0` (so both are
top somewhere and the FATA hypothesis holds ON `G`). Exact values:
`n = 4`: `E T_0(G) = 1.2031`, `E T_1(G) = 0.7969`, difference `0.406 = 0.102 n`;
`n = 8`: difference `1.113 = 0.139 n`. So without `nu(partial G_{ij}(R)) = 0`
expected FATA fails by a linear amount. (Script `attackD.py`.)

D3. The two-top-almost-everywhere hypothesis of S8 is necessary. One cell,
`K = 2`, `M_0 = 0.9`, `M_1 = 0.3`, `mu_0 = mu_1 = 0`; agent 0 is the unique top
everywhere. Deviating from `M_0 = 0.9` to `0.6` (still strictly above the rival)
gains, exactly, `0.300, 0.631, 0.967, 1.331` at `n = 2,4,6,8`, i.e. about
`0.16 n`, growing linearly. This is the "only if" side that the paper should
state alongside S8.

***

## Attack H1 (BREAKS A STRONGER STATEMENT). Exact FATA needs the per-cell
priority to be UNIFORM, not merely fixed before play

Monotonicity (S0, S1, S3) needs only that `pi_C` be fixed; the argument is applied
conditionally on `pi_C` and works for any deterministic priority, even one that is
the same in every cell. Exact FATA does NOT: with a fixed priority, agents with
IDENTICAL means get different expected counts. Exact dynamic programming, equal
means `1/2` for all agents, index `hat m + sqrt(4 log n / T)`:

| `K` | `n` | fixed priority `0>1>2` | uniform priority |
|:-|:-|:-|:-|
| 3 | 4 | `E T = (1.625, 1.250, 1.125)` | `(4/3, 4/3, 4/3)` |
| 3 | 6 | `(2.09375, 2.0, 1.90625)` | `(2, 2, 2)` |
| 3 | 8 | `(2.765625, 2.71875, 2.515625)` | `(8/3, 8/3, 8/3)` |
| 2 | 8 | `(4.0078125, 3.9921875)` | `(4, 4)` |

So the word "exact" in S1, S2 and S6 is false if `pi_C` is an arbitrary fixed
permutation; it requires `pi_C` uniform on the `K!` permutations and independent
of the tapes and the contexts. The candidate's statement ("a uniformly random
permutation drawn once before play") is correct; the risk is that a prover proves
monotonicity "for any fixed priority" and then reuses the same sentence for FATA.
(Script `attackH.py`.)

## Attack H2. The gap-free cell bound for the known-horizon index (does NOT break)

The manuscript's `eq:gap-free-ucb` is `C sqrt(K s log(es)) + C K` with the cell's
OWN length `s` inside the logarithm; that form cannot be used with a random `s`
without care. For the known-horizon index the clean replacement, which is what
S5 and S7 should quote, is obtained from the same per-arm bound:
`sum_a Delta_a E T_a(s) <= s Delta_0 + 3 sum_a Delta_a + 16 K log n / Delta_0`,
optimized at `Delta_0 = 4 sqrt(K log n / s)`, giving
  `E sum_{r <= s} (bar m^*_C - bar m_{I_r, C}) <= 8 sqrt(K s log n) + 3 K`
for every deterministic `s <= n`, with `log n` and not `log s`. This is exactly
Lattimore and Szepesvari Theorem 7.2 (`R_n <= 8 sqrt(n k log n) + 3 sum_i Delta_i`,
p. 108 of the book PDF) with `n` replaced by `s` in the count and left as `n` in
the logarithm. Verified by exact dynamic programming (`K in {2,3}`,
`n in {6,8,12,16}`, every `s <= n`, 8 random mean vectors each): 0 violations,
tightest ratio 0.057. Summing over cells with Cauchy-Schwarz gives
`8 sqrt(K J_n n log n) + 3 K J_n`, so the explicit constants for S5 and S7 are
`C_1 = 8 sqrt(K)` and `C_2 = 3K`; for S4, which concerns a single agent, no `K` is
needed at all and the constants are `C_1 = 4`, `C_2 = 3`.

## Attack B6 (end to end). Exact test of S3 on interleaved cells

250 random exact instances (`K in {2,3}`; 1, 2 or 3 cells; 2 to 4 positions with
random rational masses, so most cells are split by the region; random rational
maps; `n` from 2 to 5; random per-cell priorities, including deterministic
priorities identical across cells; deviations of four kinds, including one that
raises `m_i` only inside ONE cell and one that leaves `m_i = M_i` unchanged), each
checked for EVERY one of the `2^{npos} - 1` regions `R` and every agent, both
directions (`E T_j(R)` must not rise for `j != i`, `E T_i(R)` must not fall):
0 violations (script `attackB1fast.py`). Together with attack A1 and attack G this
exhausts the small cases I can enumerate exactly.

Two edge cases I checked explicitly inside this family:
- a cell where the deviation equals the capacity almost everywhere: the two cell
  averages coincide, the two cell executions are the SAME function of the same
  tape, and the difference is exactly zero (not merely `<= 0`);
- a cell of zero mass: never visited, `E T_j(C) = 0` on both sides, and
  `nu(R | C)` is undefined but never used.
Neither is a problem, but the write-up must say the sum runs over positive-mass
cells and that the identity is asserted only for those.

***

## Attack S0. The static race lemma itself (does NOT break)

Attacked exactly as stated in S0, with the features the scout's own search did not
combine: `K` up to 6, `n` up to 16, index values drawn from `{0,1}`, `{0,1,2}`,
`{-2,...,2}`, `{0,...,5}` and from pools CONTAINING both `+inf` and `-inf` so that
extended-real values appear at counts other than zero as well; count-zero values
forced to `+inf`, to `-inf`, or left ordinary; raises applied to a random subset of
counts and sometimes raising a finite value to `+inf` or `-inf` to `0` or `+inf`;
uniformly random priority; and the conclusion checked at EVERY intermediate time
`t <= n` for every `j != 1` AND for arm 1 itself (`T_1'(t) >= T_1(t)`). 300000
random instances, 0 violations (script `attackS0.py`).

Three specific failure modes I looked for and did not find:
- an arm that is `-inf` at every count and is starved differently in the two runs
  (it is starved identically: the lemma's total order handles `-inf` ties by
  priority);
- a raise that turns a finite value into `+inf` at a count the base run never
  reaches (harmless: by the envelope identity only the running minimum matters);
- "raise now, crash later" sequences, where raising arm 1 early exposes a very low
  later value (harmless for the same reason).
The scout's proof (envelope identity plus the sorted-order characterization) is the
one I would keep; I found no gap in it. The single hypothesis that cannot be
weakened is the fixed priority: attack B5 above.

## Where a proof of C1 is weakest, ranked (my verdict after failing to break it)

1. `lem:cell-law` as the manuscript states it. The manuscript's proof is three
   sentences and says "the rewards agent `i` actually delivers in the cell are
   i.i.d. Bernoulli(`bar m_{i,C}`) given the past". That sentence is TRUE (attack
   G verifies the joint law exactly) but it is the load-bearing step of the entire
   candidate and it is asserted, not proved. The prover must prove, by induction
   on the visit index, that the law of `(I_1, Y_1, ..., I_s, Y_s)` conditionally on
   `V_C = s` equals the law of an `s`-round fixed-mean instance with means
   `bar m_{a,C}`. Nothing else in the candidate is as consequential.
2. The exact hypothesis under which the region identity holds. Attack A3 shows
   that "cell blind" must cover the cell's COINS and not only its index. State it
   as `I^C_k` measurable with respect to `(B, pi_C, X^{(1..k-1)}, U^{(1..k-1)})`.
3. The index substitution. The manuscript's grid rule uses the cell's LOCAL TIME
   in the logarithm and the code does too; attack B4 gives a six-visit
   counterexample showing that rule is not pathwise monotone even with a fixed
   priority. Every occurrence of `log n` must be flagged, per Addendum L3, and the
   paper must not present C1 as a re-analysis of the algorithm it ran in the
   experiments.
4. "Exact" versus "pathwise". S3 is an expectation statement and cannot be
   upgraded: attack C1 is an explicit pathwise counterexample under the
   actual-visit coupling, with `K = 3` and six cell visits. The phrase "exact and
   pathwise" that `thm:grid-etc` uses must not migrate to the UCB theorem.
5. Which hypotheses each conclusion needs. Monotonicity needs only a FIXED
   per-cell priority; exact FATA needs a UNIFORM one (attack H1). Sharp adaptivity
   and FATA need their boundary terms, and the failure without them is linear, not
   `o(n)` (attacks D1 and D2). S8 needs two-top almost everywhere, and the failure
   without it is linear (attack D3).
6. Constants. The split point in TASK.md S8 (`Delta = sqrt(log n / s)`) does not
   produce the stated constant 8; the correct pairing is `4 sqrt(log n / s)` with
   constant 4, or `sqrt(log n/s)` with constant 16 (attack F1). The imported
   per-arm bound is `3 + 16 log n / Delta^2` and the gap-free cell bound is
   `8 sqrt(K s log n) + 3K` (attack H2).
7. Two small statement-level mismatches that a referee will notice.
   (a) The manuscript's context space is `X = [0,1]^D` while TASK.md partitions
   `[0,1)^D` into half-open cubes; points with a coordinate equal to 1 then lie in
   no cell. Either close the last cube in each coordinate or state `X = [0,1)^D`.
   (b) `J_n := ceil(1/h_n)^D` counts truncated boundary cubes whose side is at
   most `h_n`, so `diam(C) <= sqrt(D) h_n` still holds; but `J_n <= 2^D h_n^{-D}`
   needs `h_n <= 1`, which holds because `log(en)/n <= 1` for every `n >= 1`. Say
   so, since the rate depends on it.
8. A quantifier the provers can strengthen for free: S3 holds for ANY pointwise
   raise `m_i' >= m_i` of feasible maps, not only for the raise to `M_i`, because
   the only thing used is `bar m'_{i,C} >= bar m_{i,C}` in every cell. Stating the
   weaker version is safe but leaves value on the table.
9. A boundary of the result that must be stated, not silently crossed: the blind
   behavioral extension (scout B1 Proposition E.1) is SCALAR. In the contextual
   model the selected agent observes the full profile, so a behavioral agent's
   own-count-indexed tape depends on the positions at which it is pulled, which
   differ between the two coupled executions. That is exactly the mechanism of
   attack C1. No contextual monotonicity claim may be made outside `S_HDS`.

## Verified references

- Lattimore and Szepesvari, "Bandit Algorithms", Cambridge University Press 2020,
  PDF https://tor-lattimore.com/downloads/book/book.pdf, downloaded and read in
  this session (17 September 2026), Chapter 7 "The Optimism Principle", pp. 104 to
  108: Eq. (7.2) index, Algorithm 3, Theorem 7.1
  (`R_n <= 3 sum_i Delta_i + sum_{i : Delta_i > 0} 16 log(n)/Delta_i` for
  `delta = 1/n^2`, 1-subgaussian, any horizon `n`), the per-arm display
  `E[T_i(n)] <= 3 + 16 log(n)/Delta_i^2` inside the proof of Theorem 7.2, and
  Theorem 7.2 (`R_n <= 8 sqrt(n k log n) + 3 sum_i Delta_i`). Quoted verbatim in
  attack F2 above.
- Feng, Parkes and Xu (ICML 2020, arXiv 1906.01528) and Esmaeili, Shin and
  Slivkins (AAAI 2025, arXiv 2312.07929) are cited in the ledger as prior art for
  the race lemma. I did NOT re-verify them in this session and I do not rely on
  them anywhere above; the provers must check them against the primary source
  themselves before the paper credits them.

## Self-audit of this report

- Everything reported as an exact value is an exact rational from full
  enumeration or exact dynamic programming, not Monte Carlo. The random searches
  (attacks B4, C1, S0) are searches for counterexamples: finding none is weak
  evidence of truth and is reported as such, while every counterexample I do
  report was re-verified by hand or by exhaustive enumeration.
- Index comparisons in the enumerations use exact equality detection (equal counts
  and equal empirical means) plus 60-digit decimal arithmetic with a guard that
  raises if two unequal states produce indices within `1e-40`; the guard never
  fired.
- I did not test `D >= 2` geometry, the Lipschitz constants, or the asymptotic
  rates numerically; those are algebra, and I checked the rate arithmetic by hand
  (`n h_n`, `sqrt(J_n n log n)` and `J_n` at `h_n = (log(en)/n)^{1/(D+2)}` are
  `n^{(D+1)/(D+2)} (log n)^{1/(D+2)}`, the same, and `n^{D/(D+2)}` respectively,
  so the balance in the ledger is correct).
- I did not attack S5 (restatement of the manuscript theorem) beyond the constants
  in attack H2, as instructed.
- Not claimed error free: the absence of a counterexample after these searches is
  not a proof, and the two attacks the lead considered weakest (the region
  identity and the one-priority race argument) are, in my assessment, the two
  SOUNDEST parts of the candidate. The parts most likely to produce a referee
  complaint are items 1, 3, 4 and 5 of the ranked list above.
