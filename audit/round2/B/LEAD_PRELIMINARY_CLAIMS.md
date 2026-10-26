# Lead's preliminary claims (Agent B, 17 September 2026): to be attacked, not trusted

Status of everything below: CLAIM. None of it has a reviewed proof. Scouts must try to break each item before using it, and must produce their own proofs independently. Numerical evidence was produced by the scripts `audit/round2/B/ucb_mono_search.py` and `audit/round2/B/race_checks.py` (copies of the lead's scratch scripts; run with the venv python).

## Claim L1 (static race monotonicity)

Setting: `K` arms; for each arm `a` a fixed sequence `f_a(0), f_a(1), ...` of real numbers ("the index of arm `a` when it has been pulled `k` times"); a fixed strict priority order on arms used to break ties; at each step pull the arm maximizing `(f_a(T_a), priority)` lexicographically. Claim: if `f_1'(k) >= f_1(k)` for every `k` and all other sequences are unchanged, then for every `j != 1` and every time `t`, `T_j'(t) <= T_j(t)`. No monotonicity of `f_a` in `k` is assumed.

Evidence: 20000 random instances with `K in {2,...,5}`, `n <= 40`, checked at all intermediate times: zero violations.

Consequence if true: any index policy whose index is a nondecreasing function of the arm's own reward prefix and its own count (plus constants such as the known horizon `n`) is pathwise monotone under the tape coupling `Y_{a,k} = 1{U_{a,k} <= m_{a,k}}` indexed by local pull count. Known-horizon UCB with index `hat m + sqrt(c log n / T)` qualifies. The anytime UCB1 index `hat m + sqrt(2 log t / T)` does not (its bonus depends on the global time), and Claim L3 gives a counterexample.

## Claim L2 (envelope identity)

With the setting of L1, let `e_a(k) = min_{k' <= k} f_a(k')`. Claim: the greedy merge on `(f_a)` and the greedy merge on `(e_a)` produce the same pull sequence. Evidence: 20000 random instances, zero discrepancies. If true, L1 reduces to the merge of nonincreasing sequences.

## Claim L3 (anytime UCB1 is not pathwise monotone), verified trace

`K = 3`, `n = 8`, index `hat m + sqrt(2 log t / T)` with `t` the global round, initialization in label order, ties to the lowest label. Reward tapes indexed by each arm's own pull count:
base: arm 0 `(0,0,0,0,1,0,0,0)`, arm 1 `(0,0,1,0,0,1,1,1)`, arm 2 `(1,1,1,1,1,0,0,1)`;
raised: arm 0 `(1,0,0,1,1,1,0,1)` (pointwise at or above base), arms 1 and 2 unchanged.
Base counts at `n = 8`: `(2,1,5)`. Raised counts: `(2,2,4)`. Arm 1's count increased from 1 to 2. Trace: in the base run rounds 4 to 7 pull arm 2 and round 8 pulls arm 0 (indices 2.0393, 2.0393, 1.9120, tie to arm 0); in the raised run round 4 pulls arm 0 (index 2.6651 ties arm 2, lowest label wins), rounds 5 to 7 pull arm 2, and at round 8 the indices are (1.9420, 2.0393, 2.0197), so arm 1 is pulled. This is a legitimate realization of the manuscript's rule (fixed initialization order and tie coins have positive probability), so the manuscript's UCB1 is not pathwise monotone under the local-count tape coupling for `K = 3`. The manuscript only claims expected monotonicity with `o(n)` remainder, so this is not a contradiction of the paper.

## Claim L4 (consequences for static grids, sketched, unproved)

If L1 holds: under Lemma `lem:cell-law`, each cell's local execution has the law of a fixed-mean instance with means `bar m_{a,C}`; couple executions through cell-average tapes `1{U_{C,a,k} <= bar m_{a,C}}`; then raising agent `i`'s map pointwise raises its cell-average tape pointwise in every cell, so `E T_j(C; n)` weakly decreases for every cell, and `E T_j(R; n) = sum_C nu(R | C) E T_j(C; n)` (cell-blind decisions are independent of the current profile) weakly decreases for every measurable `R` with zero remainder. Self-monotonicity (own count weakly increases when own tape is raised) follows from L1 since the total count is fixed.

## Claim L5 (two-top almost everywhere suffices for the public equilibrium under Lipschitz capacities), sketched, unproved

If capacities are `L`-Lipschitz and `|T(X)| >= 2` for `nu`-almost every `X`, then in every positive-mass cell `C` and for every agent `i` there is `j != i` top at some point of `C`, hence `bar M_{j,C} >= bar M_C - 2 L sqrt(D) h_n` where `bar M_C = E[M_*(X) | C]`. A unilateral deviation of `i` with cell-average shading `delta_C` therefore has cell gap at least `delta_C - 2 L sqrt(D) h_n` against a nondeviating rival, and its gain in `C` is at most `E T'_i(C) delta_C` by self-monotonicity and `a_C >= 0`. Summing the resulting per-cell bounds gives explicit rates (`O(n^{(D+2)/(D+3)})` for Grid-ETC; `O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})` for known-horizon Grid-UCB if L1 holds) with no finite-component, closed-null-boundary, or dominated-convergence step, and with no separate top/non-top case split. Necessity side: a unique-top open set of positive mass with a positive capacity gap admits a linear shading gain.
