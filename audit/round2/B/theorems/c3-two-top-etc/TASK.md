# Task C3: continuous public equilibrium for Static Grid-ETC under the two-top almost everywhere condition

Written by Agent B for the two provers and the hostile worker. Notation as in audit/round2/B/CONTEXT_PROOF_CONTRACT.md. Cite the manuscript's lemmas by their labels (lem:cell-law, lem:etc-tail, appendix A.4 coupling). No Unicode em dashes, no triple hyphens, anywhere.

## Setting (fixed)

X = [0,1)^D (half-open so that dyadic cubes partition it exactly; state and justify any change), D = Kd, profiles X_t i.i.d. nu (any Borel probability law), capacities M_i : [0,1)^d -> [0,1] Borel with M_i >= mu_i, intrinsic means mu_i Borel (Lipschitz not needed for this task except where stated). Strategy class S_HDS with independent ex ante mixtures. M_*(X) = max_i M_i(x_i), T(X) = {i : M_i(x_i) = M_*(X)}.

Static Grid-ETC on nested dyadic grids: k_n := ceil(log_2(n)/(D+3)), h_n := 2^{-k_n} (so n^{-1/(D+3)}/2 < h_n <= n^{-1/(D+3)}), J_n := h_n^{-D} = 2^{k_n D}, q_n := ceil(n^{2/(D+3)}); in each lazily initialized cell q_n independent uniform permutations of [K] as exploration blocks (first K q_n cell visits; the last observed block possibly truncated), then commitment to an agent with the largest exploration empirical mean (each over exactly q_n observations), ties by an independent uniform priority permutation drawn once per cell, exploitation rewards ignored. Cell-blind decisions.

For a cell C with nu(C) > 0: bar M_{j,C} := E[M_j(x_j) | X in C]; for agent i, eta_{i,C} := (bar M_{i,C} - max_{j != i} bar M_{j,C})_+; c_1 := 2 e^{-1/2}.

## Target Theorem T1 (equilibrium, measurable capacities)

Assume nu(|T(X)| >= 2) = 1 and M_* public. Then all-maximum play S^max is an S_HDS-asymptotic equilibrium under Static Grid-ETC: for every agent i (strategic or honest), every n, and every unilateral deviation m'_{i,n} in S_HDS (deterministic map, or independent ex ante mixture),
u_i(n; m'_{i,n}, S^max_{-i}) - u_i(n; S^max) <= q_n J_n + c_1 n q_n^{-1/2} + n sum_C nu(C) eta_{i,C},
and sum_C nu(C) eta_{i,C} -> 0 as n -> infinity (sum over the level-k_n dyadic cells), so the gain is o(n).

## Target Theorem T2 (explicit rate under Lipschitz capacities)

If in addition every M_i is L-Lipschitz (Euclidean norm on [0,1]^d), then eta_{i,C} <= 2 L sqrt(D) h_n for every positive-mass cell and every i, hence the gain is at most
q_n J_n + c_1 n q_n^{-1/2} + 2 L sqrt(D) n h_n <= (2^{D+1} + c_1 + 2 L sqrt(D)) n^{(D+2)/(D+3)}.
(Check the constant 2^{D+1}: q_n <= 2 n^{2/(D+3)} for n >= 1 and J_n <= 2^D n^{D/(D+3)}.)

## Target Theorem T3 (revenue at all-maximum play)

If every M_i is L-Lipschitz (no top-set condition), P(n; S^max) >= E sum_t M_*(X_t) - [K q_n J_n + (K-1) c_1 n q_n^{-1/2} + 2 L sqrt(D) n h_n]. If capacities are merely Borel, P(n; S^max) >= E sum_t M_*(X_t) - o(n).

## Target Theorem T4 (necessity)

Let U_i := {X : M_i(x_i) > max_{j != i} M_j(x_j)} and W_i := U_i for a strategic agent, W_i := U_i cap {mu_i(x_i) < M_i(x_i)} for an honest agent. If nu(W_i) > 0 then agent i has a unilateral S_HDS deviation with gain at least c n for all large n and an explicit c > 0 depending on the instance (give the constant, for example via a set of positive mass where the capacity gap and the slack both exceed some g > 0). Conversely T1 shows nu(W_i) = 0 for all i suffices. Knife-edge honest unique tops without slack remain equilibria.

## Requirements from the main agent (non-negotiable)

1. The grid is nested dyadic with k_n = ceil(log_2(n)/(D+3)); state where nesting is used.
2. The convergence sum_C nu(C) eta_{i,C} -> 0 must be proved with the exact filtration: F_k = sigma(level-k dyadic cells), bounded Borel f, E[f | F_k](X) -> f(X) nu-a.s. by Levy's upward theorem; cite a textbook theorem (for example Williams, Probability with Martingales, 1991, Theorem 14.2, or Durrett, Probability: Theory and Examples, Theorem 4.6.8 in the 5th edition, or Kallenberg) and VERIFY the citation against a primary or publisher source (record the URL or exact edition and page); check that the dyadic sigma-algebras generate the Borel sigma-algebra of [0,1)^D; then dominated convergence for the integral of eta_{i,C_{k_n}(X)}. State precisely why (M_i - max_{j != i} M_j)_+ = 0 nu-a.s. under nu(|T| >= 2) = 1.
3. Zero-mass cells: never visited; no conditional mean needed; make the sums well defined.
4. Truncated exploration blocks and cells with fewer than K q_n visits: no commitment, the deviator's utility change there is at most its exploration pulls (at most q_n per cell); prove the exploration accounting q_n J_n exactly (per-pull utility difference at most 1? justify the bound with 1 + mu_i - m in [0,2]).
5. Prove the per-cell inequality in full: factorization by lem:cell-law (expected exploitation utility = expected number of exploitation visits times commitment probability times conditional cell mean of the per-pull utility), the pathwise commitment coupling p'_C <= p_C (appendix A.4 coupling, including the tie priority), a_C >= 0, and the two cases Delta' > 0 and Delta' <= 0.
6. Confirm the constant c_1 = 2 e^{-1/2} of lem:etc-tail (maximize x times 2 exp(-q x^2/2)); and that the tail bound applies with the deviator's exploration observations i.i.d. Bernoulli(bar m'_{i,C}) by lem:cell-law.
7. Mixtures: condition on the realized map; constants do not depend on the map.
8. Quantifiers: every n, every deviation, every agent; the rate constants depend only on D, L, K.
9. Necessity with an explicit constant and a complete argument (win probability in fully explored interior cells via lem:etc-tail with the two-sided gap; cells inside a positive-mass open set, or use the dyadic filtration again to find cells where the deviator is the unique cell-best by a margin).

## Output format

Sections: 0 status line (updated incrementally); 1 exact theorem statements as they should appear in the paper; 2 lemmas with complete proofs; 3 proofs of T1 to T4; 4 list of every place where an assumption is used; 5 self-audit (what you could not close, if anything); 6 references with verified URLs. Never present an incomplete proof as complete.
