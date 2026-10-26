# Scout B2: context-only adaptive partitions for the contextual strategic bandit (17 September 2026)

STATUS: IN PROGRESS. Complete: Sections 0, A, B, C. Remaining: D, E, F, G, H.

Role: read-only research scout for Agent B. Nothing here edits the manuscript. Every statement is classified in Section H at the end as PROVED, PROVED UNDER STRONGER ASSUMPTIONS, INCOMPLETE, FALSE, or OPEN. Notation follows audit/round2/B/CONTEXT_PROOF_CONTRACT.md (the "contract"). Lead claims L1 to L5 are treated as hypotheses only.

Sections: A (what a context-only partition buys), B (generalized cell-law lemma), C (candidate algorithms), D (theorems and proofs), E (counterexamples), F (comparison table and recommendation), G (literature check with URLs), H (classification).

## 0. Summary of conclusions (written last, placed first)

1. A context-only adaptive partition is one whose evolution is a measurable function of the contexts alone (plus independent platform coins). Because contexts are exogenous and independent of rewards, such a partition is not manipulable in the sense that matters for the manuscript's proofs: conditional on the partition path, every cell-epoch is an isolated fixed-mean instance with fresh statistics (Lemma B.2 below generalizes `lem:cell-law`). Reward-dependent or selection-dependent splitting breaks pathwise monotonicity by a linear amount even against fixed ex ante maps (Section E.3), and inherited statistics are biased in the child cell (Section E.2).
2. The best candidate is not sample splitting and not a k-d tree. It is a dyadic tree that splits a leaf when its own since-creation visit count reaches a level threshold, with a fresh ETC (or UCB) instance in every leaf and no inherited statistics ("COAT" below). It needs neither `n`, nor `L`, nor `nu`. It keeps every property of Static Grid-ETC (sharp adaptivity, exact pathwise monotonicity, expected FATA, robustness, the continuous public equilibrium under the manuscript's structural assumptions), is anytime, and attains the rate `n^{(d_nu+2)/(d_nu+3)}` when the support of `nu` is covered by at most `A 2^{l d_nu}` dyadic cubes of level `l` (Section D). The proof is a counting argument on top of Lemma B.2; it is complete below.
3. Sample splitting is dominated: the burn-in rounds must be played by some rule, and a short burn-in cannot estimate the occupancy counts that govern the rate (Section C.1 and C.3). Equal-mass and k-d partitions carry no diameter guarantee; the Lipschitz bias is a bound in the occupied diameter, and what one gets is the bias `(L/m) sum_C diam(C cap supp nu)` rather than `L h` (Section D.4, Section E.4).
4. The static grid with lazy initialization already pays only for occupied cells. This is a free one-sentence remark for the manuscript (Section A), but it does not change the rate exponent because `h_n` is tuned to `D`.
5. Recommendation (Section F): add the occupied-cell remark; add a two-line doubling remark if an anytime statement is wanted; consider COAT-ETC only if roughly two thirds of a two-column page can be spared, since it replaces (rather than adds to) the static grid theorem. Nothing here is required for the paper's thesis.

END OF SECTION 0

## A. What a context-only partition buys and what it cannot

### A.1 The bias term is a diameter bound on the occupied part of a cell

The Lipschitz step in the manuscript (appendix A.3) reads: for a representative `x_C in C` and an honest `h_C` attaining `b(x_C)`, `b(x) <= m_{h_C,n}(x) + 2 L |x - x_C|` for all `x in C`, hence `bar b_C <= bar m_C^* + 2 L diam(C)`. Two facts follow that hold for any partition.

(A.1.a) The representative may be taken in `C cap supp(nu)` when `nu(C) > 0` (that set is nonempty, and the bound is only integrated against `nu(. | C)`). So the bias per visit is `2 L diam(C cap supp nu)`, not `2 L diam(C)`. For a grid this is at most `2 L sqrt(D) h_n` and nothing is gained; for irregular partitions it is what one actually controls.

(A.1.b) The bias is a bound in the diameter and only in the diameter; the mass of the cell enters only as the number of visits charged. Equal-mass constructions therefore do not control the bias unless they also control diameters (Section D.4).

### A.2 Lazy initialization already restricts every count to occupied cells

Let `N_occ(n) := #{C : V_C(n) >= 1}` (cells visited at least once) and `N_nu(h) := #{C in grid(h) : nu(C) > 0}`. Since visited cells have positive mass almost surely, `N_occ(n) <= min{J_n, n, N_nu(h_n)}` pathwise, and `E N_occ(n) = sum_C (1 - (1 - nu(C))^n)`.

Grid-UCB1 (proof of `thm:grid-ucb-robust`): the per-cell bound `C sqrt(K s log(es)) + C K 1{s >= 1}` summed with Cauchy-Schwarz gives, pathwise in the visit counts,
`sum_C [C sqrt(K V_C log(en)) + C K 1{V_C >= 1}] <= C sqrt(K N_occ n log(en)) + C K N_occ`,
so by Jensen (`E sqrt(N_occ) <= sqrt(E N_occ)`)
`E sum_t [b(X_t) - m_{I_t,n}(X_t)] <= 2 L sqrt(D) n h_n + C sqrt(K N_nu(h_n) n log(en)) + C K N_nu(h_n)`.   (A.1)

Grid-ETC (proof of `thm:grid-etc`): exploration costs at most `K q_n` per visited cell, so `K q_n J_n` may be replaced by `K q_n N_occ <= K q_n N_nu(h_n)`:
`E sum_t [b(X_t) - m_{I_t,n}(X_t)] <= K q_n N_nu(h_n) + 2 L sqrt(D) n h_n + C K n q_n^{-1/2}`.   (A.2)
The same replacement applies verbatim to the sharp-adaptivity error, to the exploration-savings term `q_n J_n` in `thm:contextual-public`, and to nothing else (the monotonicity and FATA arguments do not count cells).

This is PROVED (it is literally the manuscript's proof with the sum restricted to visited cells; unvisited cells contribute zero to every sum).

### A.3 Quantification through covering numbers, and why the exponent does not move

Suppose `supp(nu)` has dyadic upper box dimension at most `d_nu` with constant `A`, meaning `N_nu(2^{-l}) <= A 2^{l d_nu}` for all `l >= 0` (always true with `d_nu = D`, `A = 1`). At the manuscript's choices `h_n = (log(en)/n)^{1/(D+2)}` (UCB) and `h_n asymp n^{-1/(D+3)}`, `q_n = ceil(n^{2/(D+3)})` (ETC), (A.1) and (A.2) give
UCB: `2 L sqrt(D) n^{(D+1)/(D+2)} (log en)^{1/(D+2)} + C sqrt(A K) n^{1/2 + d_nu/(2(D+2))} (log en)^{1/2 - d_nu/(2(D+2))} + C K A (n/log en)^{d_nu/(D+2)}`;
ETC: `K A n^{(2 + d_nu)/(D+3)} + 2 L sqrt(D) C' n^{(D+2)/(D+3)} + C K n^{(D+2)/(D+3)}`.
In both, the bias term is untouched and dominates; the exploration and initialization terms shrink from `n^{(D+1)/(D+2)}` to `n^{1/2 + d_nu/(2(D+2))}` (UCB) and from `n^{(D+2)/(D+3)}` to `n^{(2+d_nu)/(D+3)}` (ETC). The exponent of the total does not improve, because `h_n` was balanced for `d_nu = D`. If `d_nu` were known one would take `h_n = (log(en)/n)^{1/(d_nu+2)}` (UCB) or `h_n asymp n^{-1/(d_nu+3)}`, `q_n = ceil(n^{2/(d_nu+3)})` (ETC) and obtain the exponents `(d_nu+1)/(d_nu+2)` and `(d_nu+2)/(d_nu+3)` with constants `A^{1/(d_nu+2)}` and `A^{1/(d_nu+3)}` respectively (direct substitution into (A.1), (A.2)).

What remains unknown to the platform and therefore cannot be used in `h_n`: `d_nu`, `A` (and more generally the function `l -> N_nu(2^{-l})`), `L` (constants only; the manuscript's `h_n` is already `L`-free), and the boundary moduli `r -> nu((partial R)^r)`. The adaptivity problem for context-only partitions is exactly the problem of choosing the scale without knowing `l -> N_nu(2^{-l})`. Section C.3 (scale selection from a burn-in sample) and Section D (visit-count-triggered splitting) are the two ways to do it; only the second works without paying for the burn-in.

### A.4 What a context-only partition cannot buy

- It cannot remove the Lipschitz bias `2 L diam(C cap supp nu)`; every rate below still has the shape `bias + exploration + simple regret`.
- It cannot use reward information to place splits where the maps vary, without losing pathwise monotonicity (Section E.3); the manuscript's monotonicity is a coupling statement that needs identical partitions under the two map profiles.
- It cannot protect against phase-dependent (bait-and-switch) behavior; those strategies are outside `S_HDS` for every algorithm considered here, and an adaptive tree has more exploration phases than a grid, not fewer (Section E.1).
- It cannot adapt to unknown smoothness in the sense of a Holder exponent `beta`; the manuscript's model is Lipschitz (`beta = 1`) with unknown `L`, and `L` only enters constants, so there is nothing to adapt to. (Holder adaptivity is a different problem; see Section G on Gur, Momeni and Wager.)

END OF SECTION A

## B. A generalized cell-law lemma for context-only partition processes

### B.1 Primitives and the coupling convention

Fix `n` (all statements hold for every `n`, which is what makes the anytime claims below possible). The primitives are:
- contexts `X_1, X_2, ...` i.i.d. `nu` on `X = [0,1)^D` (half-open so that dyadic cubes partition it exactly);
- reward uniforms `U_1, U_2, ...` i.i.d. Uniform[0,1], one per round, used as `Y_t = 1{U_t <= m_{I_t,n}(X_t)}`;
- an independent random element `Z` (burn-in contexts of a sample-split design, or nothing);
- platform coins `xi = (xi_lambda)_lambda`, one independent family per cell-epoch label (permutations, priorities, tie coins);
- agents' ex ante randomization `omega_A`; conditional on `omega_A` the maps `m_{i,n}` are fixed measurable feasible maps. Everything below is conditional on `omega_A`, and the four families above are mutually independent conditionally on `omega_A`.

Seed indexing. The manuscript indexes reward uniforms by the agent's local pull index within an instance (contract, Section 1 and Section 14.1). Indexing by the global round `t` gives the same law for every single execution. For the monotonicity couplings below both executions have the same exploration rounds for agent `i` in every cell-epoch, so indexing by round coincides with the manuscript's "reward uniforms on common exploration pulls" and no reproof is needed. Indexing by the agent's overall pull count would not coincide (exploitation pulls differ between the two executions) and is not used.

### B.2 Partition processes, labels, and the three structural requirements

A partition process is a sequence `P_1, P_2, ...` of countable measurable partitions of `X`. Give every cell a creation time: for `C in P_t`, `tau_t(C) := min{s <= t : C in P_u for all u in [s, t]}`. The cell-epoch label of round `t` is `Lambda_t := (C_t, tau_t(C_t))` with `C_t in P_t` the cell containing `X_t`. Rounds with the same label are the visits of one cell during one uninterrupted life; the label determines the cell as a set, so I write `C(lambda)` for it and `lev(lambda)` for its level when the cells are dyadic.

Requirement (R1), label-adapted partition: there are measurable maps `pi_t` with `P_t = pi_t(Z, Lambda_1, ..., Lambda_{t-1})`. In words: which cells exist at round `t` depends on the past only through which labels the past rounds carried (their counts, their order), never through the exact positions of past contexts beyond their labels, and never through rewards, selections, or platform coins.

Requirement (R2), label-local fresh statistics: `I_t = phi(Lambda_t, H_t(Lambda_t), xi_{Lambda_t})` for a fixed measurable rule `phi`, where `H_t(lambda) := ((I_s, Y_s) : s < t, Lambda_s = lambda)` is the history of the label's own earlier rounds. No data from other labels (in particular none from a parent cell), no exact position `X_t`, no global clock.

Requirement (R3), exogeneity: `(X_t)_t`, `(U_t)_t`, `Z`, `xi` are mutually independent (conditionally on `omega_A`).

Examples. The static grid: `P_t = grid(h_n)`, (R1) trivially. Sample splitting: `Z = (X_1, ..., X_{n_0})`, `P_t = tree(Z)` for `t > n_0`, (R1) with `pi_t` ignoring the labels (the burn-in rounds get their own labels and are analyzed separately). COAT (Section C.2, Section D): `P_{t+1}` equals `P_t` unless the label `Lambda_t` has now been carried by exactly `N_{lev(Lambda_t)}` rounds, in which case `C(Lambda_t)` is replaced by its `2^D` dyadic children; this is a function of the label sequence, so (R1) holds. Children counting since creation is essential: if children inherited the parent's visits by position, `P_{t+1}` would depend on exact positions of earlier contexts and (R1) would fail.

### B.3 Lemma B.1 (product structure of the contexts given the labels)

Statement. Assume (R1) and (R3). Conditional on `Z` and on `Lambda_{1:n} = lambda_{1:n}` (an event of positive conditional probability), the contexts `X_1, ..., X_n` are independent and `X_t ~ nu(. | C(lambda_t))`. Consequently, for every label `lambda`, the ordered contexts of the rounds carrying `lambda` are i.i.d. `nu(. | C(lambda))`, and the contexts of rounds carrying different labels are independent.

Proof. Work conditionally on `Z = z` (by (R3), `X_{1:n}` is i.i.d. `nu` given `Z = z`). Fix `lambda_{1:n}`. By (R1), `P_1 = pi_1(z)` is deterministic; given `Lambda_{1:t-1} = lambda_{1:t-1}` the partition `P_t = pi_t(z, lambda_{1:t-1})` is deterministic and there is a deterministic set `D_t := C(lambda_t) in P_t` (if `lambda_t` names no cell of that partition the event is empty). Since `P_t` is a partition, `{Lambda_t = lambda_t} cap {Lambda_{1:t-1} = lambda_{1:t-1}} = {X_t in D_t} cap {Lambda_{1:t-1} = lambda_{1:t-1}}`. By induction `{Lambda_{1:n} = lambda_{1:n}} = cap_{t <= n} {X_t in D_t}`, a product set. For measurable `A_1, ..., A_n`,
`Pr(X_t in A_t for all t, Lambda_{1:n} = lambda_{1:n} | Z = z) = prod_t nu(A_t cap D_t)`,
and `Pr(Lambda_{1:n} = lambda_{1:n} | Z = z) = prod_t nu(D_t) > 0` by assumption. Dividing gives `prod_t nu(A_t | D_t)`, which is the claim. The two consequences are restrictions of a product law to subfamilies of coordinates. QED.

Remark (why exact positions may be conditioned away). The lemma conditions on the entire label sequence, including labels of future rounds. This is what the manuscript's `lem:cell-law` also does ("conditional on its membership-indicator sequence"), and it is what makes "conditional on `V_C = s`, the cell is an `s`-round fixed-mean instance" a legitimate statement. Under (R1) the labels carry no information about positions beyond cell membership, which is why the conditional law stays a product of cell-conditional laws.

### B.4 Lemma B.2 (cell-epoch law and future independence)

Statement. Assume (R1), (R2), (R3), and fixed maps. Condition on `Z` and `Lambda_{1:n} = lambda_{1:n}`. For a label `lambda` with `C := C(lambda)`, `nu(C) > 0`, carried by the rounds `t_1 < ... < t_s`:
(i) the sequence `(I_{t_r}, Y_{t_r})_{r <= s}` has the law of the first `s` rounds of an execution of the scalar rule `phi(lambda, ., xi_lambda)` against `K` independent Bernoulli reward streams with fixed means `bar m_{i,C} := E[m_{i,n}(X) | X in C]`, `i in [K]`;
(ii) executions of distinct labels are conditionally independent;
(iii) for every `r < s`, the data `((I_{t_u}, Y_{t_u}))_{u <= r}` and any function of them and of `xi_lambda` are independent of `(X_{t_u})_{u > r}` and of the contexts of every round carrying another label;
(iv) in particular, for every measurable `R` and every function `W` of the data of the first `r` rounds of `lambda`, `E[1{X_{t_u} in R} W] = nu(R | C) E[W]` for `u > r`.

Proof. Conditional on `(Z, Lambda_{1:n})`, by Lemma B.1 the contexts are independent with `X_{t_r} ~ nu(. | C)`, and by (R3) the uniforms `U_{t_r}` and the coins `xi_lambda` are independent of everything else and of each other (conditioning on a function of the contexts alone does not disturb the independent families). Induct on `r`. `I_{t_r}` is, by (R2), a function of `H := ((I_{t_u}, Y_{t_u}))_{u < r}` and `xi_lambda`, which are functions of `(X_{t_u}, U_{t_u})_{u < r}` and `xi_lambda`; hence `X_{t_r}` and `U_{t_r}` are independent of `(H, xi_lambda, I_{t_r})`. Therefore
`Pr(Y_{t_r} = 1 | H, xi_lambda, I_{t_r} = i) = E[Pr(U_{t_r} <= m_{i,n}(X_{t_r}) | X_{t_r})] = int m_{i,n}(x) nu(dx | C) = bar m_{i,C}`,
and `Y_{t_r}` is conditionally independent of `(H, xi_lambda)` given `I_{t_r}`. This is exactly the transition structure of a fixed-mean bandit execution of `phi` (one can realize it with the same law by fresh Bernoulli(`bar m_{i,C}`) draws), proving (i). (ii): the executions are functions of disjoint subfamilies of the independent primitives `(X_{t}, U_{t})_{t in lambda}, xi_lambda`. (iii) and (iv): the first `r` rounds' data are functions of `(X_{t_u}, U_{t_u})_{u <= r}` and `xi_lambda`, which are independent of `(X_{t_u})_{u > r}` and of the other labels' contexts by Lemma B.1 and (R3). QED.

Corollary B.3 (what carries over verbatim). Every per-cell step in the manuscript's grid proofs uses `lem:cell-law` only through (i) to (iv): the gap-free UCB bound conditional on `V_C = s` (robustness), `lem:etc-tail` applied to `q` exploration samples with means `bar m_{i,C}` (ETC), the factorization "commitment probability times conditional cell mean" (ETC exploitation, sharp adaptivity, FATA, public equilibrium), and label symmetry inside a cell (FATA). Hence every such step holds per cell-epoch for any partition process satisfying (R1) to (R3), with `C` the cell of the epoch and `s` the epoch's visit count. What does not carry over automatically is the aggregation over cell-epochs (their number and diameters are now random); that is the content of Section D.

Remark on global clocks. If the local rule used the global round `t` (as anytime UCB1 with `log t` would), (R2) fails as stated, but conditional on the labels the global rounds of a label's visits are deterministic numbers; the label's execution is then a fixed-mean execution of a rule with a deterministic exogenous clock. The manuscript's cell rules use local time, so this is not needed.

### B.5 What breaks when the partition depends on rewards or selections

Let the partition process instead satisfy (R1') `P_t = pi_t(Z, F_{t-1})` with `F_{t-1}` the full past (contexts, selections, rewards). Three distinct things happen; they must be kept apart because the prior audit's failures mix them.

(B.5.a) Inherited statistics are biased. If after a split the child reuses parent observations, those observations are not a fixed-mean sample in the child even though each was an unbiased draw when taken. Minimal example (details in Section E.2): one cell `[0,1)`, one agent with map `m(x) = x`, two observations at positions `X_1, X_2`; split at `1/2` iff `Y_1 = 1`; give each observation to the child containing its position. In the left child, conditional on the split having happened, the inherited observation from round 1 has mean `1`, whereas the child's cell mean is `1/4`. So in a split-conditioned child, inherited data have the wrong mean, in addition to the prior audit's observation (CONTEXT_REFEREE.md, "Why the current adaptive-tree theorem does not survive", item 2) that the parent's selections were not made by the child's rule.

(B.5.b) Fresh statistics after a reward-dependent split: the cell-epoch is still, sequentially, a fixed-mean instance (at round `t`, given `F_{t-1}`, `X_t ~ nu(. | C_t)` and `Y_t ~ Bernoulli(bar m_{I_t, C_t})`), but the epoch length is now a stopping time of the epoch's own rewards and the number and diameters of epochs depend on the maps. Lemma B.1 fails (conditioning on labels now conditions on rewards), so "conditional on `V_C = s`, an `s`-round fixed-mean instance" is no longer available; a proof would have to go through a virtual continuation of each epoch to its maximal length and charge the maximal length. I have not written such a proof; robustness for reward-dependent splitting with fresh statistics and deterministic diameter control is INCOMPLETE, not false.

(B.5.c) Pathwise monotonicity is false, by a linear margin, already against fixed ex ante maps: raising agent `i`'s map can change the split decision and thereby hand agent `j` a region it did not have (Section E.3, three agents, `D = 1`, an "ambiguous cell" split rule). The manuscript's monotonicity proof needs the two coupled executions to have identical partitions and identical exploration rounds; (R1) is exactly the condition that guarantees this, since both executions share the contexts.

Selection-dependent partitions (splits triggered by `T_i(C)` rather than `V_C`) are reward-dependent, because selections depend on rewards through the cell rule; the same three points apply. Visit-count-triggered splits (`V_C` is a function of contexts only) satisfy (R1).

END OF SECTION B

## C. Candidate algorithms

### C.0 Conventions shared by all candidates

- Cells are half-open dyadic cubes of `[0,1)^D` unless said otherwise; the level-`l` cube containing `x` is `Q_l(x) := prod_k [floor(2^l x_k) 2^{-l}, (floor(2^l x_k) + 1) 2^{-l})`, side `2^{-l}`, diameter `sqrt(D) 2^{-l}`.
- Two local rules, both cell-blind and label-local (requirement (R2)): `ETC(q)` is the manuscript's rule (`q` independent uniform permutations of `[K]` as exploration blocks, commitment to the largest exploration mean, ties by an independent uniform priority permutation, exploitation rewards ignored); `UCB` is the manuscript's symmetric local-time UCB1.
- Every cell-epoch has fresh statistics and fresh coins. Nothing is inherited, including visit counts.
- Agents can affect only rewards (through fixed maps in `S_HDS`). They cannot affect contexts, hence cannot affect any partition satisfying (R1). Where "manipulation" is discussed below it means: a change of one agent's map changes the partition (impossible under (R1)) or changes another agent's allocation non-monotonically (Section E.3 for reward-dependent rules).

### C.1 Candidate 1: sample-split k-d (equal-mass) partition, "SSKD"

```
Input: n, burn-in length n_0 < n, depth j (m = 2^j leaves), local rule ETC(q) or UCB.
Rounds 1..n_0 (burn-in): select agents by a fallback rule (Static Grid-ETC with horizon n_0,
    or COAT of C.2); store the contexts X_1..X_{n_0} only.
Tree: root = [0,1)^D with sample S_root = {X_1..X_{n_0}}.
  for depth = 1..j, for every node B at depth-1 with sample S_B and coordinate k = ((depth-1) mod D)+1:
      c = empirical median of the k-th coordinate of S_B (upper median; points with x_k <= c go left);
      children: B_left = B cap {x_k <= c}, B_right = B cap {x_k > c}; split S_B accordingly.
  Leaves: m = 2^j boxes, each holding about n_0/m burn-in points.
Rounds n_0+1..n: let C be the leaf containing X_t; run the leaf's fresh local rule; select its output.
```
Structure: `Z = (X_1, ..., X_{n_0})`, `P_t = leaves(Z)` for `t > n_0`: (R1) holds with `pi_t` depending on `Z` only; (R2), (R3) hold. Corollary B.3 applies to the play phase conditional on `Z`.
- Manipulation: none of the tree. A map chosen by an agent who is shown the tree before round `n_0 + 1` is still a fixed map conditional on `Z`, so every play-phase bound (which is uniform over fixed maps) survives even if the platform reveals the partition after the burn-in (Section D.6).
- Monotonicity: exact pathwise on the play phase (ETC leaves; same coupling as Grid-ETC, partition identical in both executions since it is a function of `Z`), and on the burn-in if the fallback is Grid-ETC or COAT-ETC. FATA: per interior leaf exact in expectation; boundary leaves are those meeting `partial G`; without a diameter bound their total mass is not controlled by a tube of `partial G` (Section D.4). Public equilibrium: the manuscript's argument needs cells that shrink `nu`-a.e.; not available without diameter control.
- Rate (robustness, ETC leaves, conditional on `Z`): `E[deficit of play phase | Z] <= K q m + 2 L (n - n_0) sum_C nu(C) diam(C cap supp nu) + C K (n - n_0) q^{-1/2}`, plus the burn-in's own deficit (at most `n_0`, or the fallback's bound). With equal empirical masses the middle term is about `2 L n m^{-1} sum_C diam(C cap supp nu)`, which is `2 L n sqrt(D) 2^{-j/D}` only if the leaves are roughly cubes of side `2^{-j/D}`; Section D.4 shows what can be proved and what fails.
- Verdict: dominated by the lazy grid (Section A) and by COAT (Section C.2). Two independent reasons: (a) no diameter control; (b) the burn-in rounds must be played by some rule, and a burn-in shorter than a constant fraction of `n` cannot estimate the occupancy profile that governs the rate (Section C.3), while a burn-in of length `n/2` inherits the fallback's non-adaptive rate.

### C.2 Candidate 2: context-only adaptive tree with fresh cell-epochs, "COAT"

```
Parameters (no n, no L, no nu): for level l >= 0,
   ETC version:  split threshold N_l = K 8^l,   exploration size q_l = 4^l   (so K q_l <= N_l);
   UCB version:  split threshold N_l = 4^l (or 4^l ceil(log(en)) if n is known).
State: a set LEAVES of dyadic cubes (initially {[0,1)^D} at level 0); for each leaf, a since-creation
   visit count V (initially 0) and a fresh local-rule state (ETC(q_l) or UCB), created lazily.
Round t:
   observe X_t; let C in LEAVES be the leaf containing X_t, l = level(C);  V_C <- V_C + 1;
   select I_t = output of C's local rule (ETC(q_l) or UCB) given C's own history;  observe Y_t; update C's rule;
   if V_C = N_l:  remove C from LEAVES; add its 2^D dyadic children (level l+1), each with V = 0 and a fresh rule.
```
Structure: `P_{t+1}` differs from `P_t` only when the label of round `t` has been carried `N_l` times; (R1) holds; (R2), (R3) hold by construction. The algorithm never uses `n`, so all statements are anytime.
- Manipulation: impossible; the whole partition path is a deterministic function of `(X_1, ..., X_n)`.
- Monotonicity (ETC version): exact pathwise for every `R` and every `n` (Theorem D.2). FATA: expected, with an explicit remainder (Theorem D.3). Sharp adaptivity and robustness: Theorem D.1 with rate `O(n^{(d_nu+2)/(d_nu+3)})` under the dyadic covering assumption. Public equilibrium: Theorem D.4, same structural assumptions as `thm:contextual-public`.
- Balance of terms (ETC version), per level-`l` epoch with `s` visits: exploration at most `min{s, K 4^l}`; per exploitation visit bias `2 L sqrt(D) 2^{-l}` and simple regret `C K q_l^{-1/2} = C K 2^{-l}`. Summed with `e_l` = number of visited level-`l` epochs and `n_l` = visits at level `l`: `sum_l [K 4^l e_l + (2 L sqrt(D) + C K) 2^{-l} n_l]`, with `e_l <= min{N_nu(2^{-l}), 2^D n_{l-1} / N_{l-1}}` and `n_l <= e_l N_l`. The two sums balance at `2^l asymp (n/K)^{1/(d_nu+3)}`; see D.1.
- UCB version: robustness only (no monotonicity claim, as for Grid-UCB1), rate `O(n^{(d_nu+1)/(d_nu+2)} sqrt(log n))` with `N_l = 4^l`, or `O(n^{(d_nu+1)/(d_nu+2)} (log n)^{1/(d_nu+2)})` with `N_l = 4^l ceil(log(en))` (Theorem D.1').

### C.2' Candidate 2': doubling epochs with a fresh static grid per epoch, "DE-Grid"

```
Epoch k = 0, 1, 2, ...: rounds t in [2^k, 2^{k+1}) (the last epoch truncated at n), epoch length n_k = 2^k.
In epoch k run Static Grid-ETC (or Grid-UCB1) with horizon parameter n_k: fresh grid of side h_{n_k},
   fresh q_{n_k}, fresh statistics in every cell; nothing is carried across epochs.
```
Structure: deterministic partition process (labels are (epoch, cell)); (R1) to (R3) hold. Every per-epoch statement is the manuscript's theorem at horizon `n_k`, applied conditionally on the past (the epoch's primitives are independent of the past, and the maps are fixed).
- Rate: `sum_{k <= log2 n} C n_k^{(D+2)/(D+3)} <= C n^{(D+2)/(D+3)} / (1 - 2^{-(D+2)/(D+3)})`; anytime; not adaptive to `d_nu`.
- Monotonicity: exact pathwise (each epoch is a Grid-ETC execution with identical partition and exploration rounds in both coupled executions; sum over epochs). FATA: expected, remainder `sum_k n_k nu((partial G)^{sqrt(D) h_{n_k}}) = o(n)` (Cesaro: the summands' factors tend to zero). Public equilibrium: per epoch the deviation gain is `g(n_k) = o(n_k)` by `thm:contextual-public`; `sum_k g(n_k) = o(n)` by the same Cesaro argument. All PROVED given the manuscript's theorems as black boxes (Section D.7).
- Verdict: the cheapest way to an anytime statement (two lines in the paper), nothing else.

### C.3 Candidate 3: scale selection from burn-in occupancy, "SSO"

```
Input: n; burn-in n_0 = floor(n/2); local rule UCB (robustness) or ETC (SAMF).
Rounds 1..n_0: fallback rule (Static Grid at the D-tuned scale, or COAT); store contexts only.
For l = 0..l_max := floor(log2 n): Nhat(l) = #{level-l dyadic cubes containing at least one burn-in context}.
UCB: l_hat = argmin_l [ n 2^{-l} + sqrt(n Nhat(l) log(en)) + K Nhat(l) ]  (ties to the smaller l).
ETC: l_hat = argmin_l [ n 2^{-l} + n^{2/3} Nhat(l)^{1/3} ], q = ceil((n / max(Nhat(l_hat),1))^{2/3}).
Rounds n_0+1..n: static grid at level l_hat with fresh cells; local rule as chosen.
```
Structure: `Z = (X_1, ..., X_{n_0})`, play-phase partition a function of `Z`; (R1) to (R3) hold.
- What it buys: the play phase attains the `d_nu`-adaptive exponent (Theorem D.5, robustness, UCB version, proved for `d_nu >= 2` with an elementary variance bound and for all `d_nu` given a negative-association Chernoff bound for occupancy counts).
- What it costs: the burn-in's deficit. If the fallback is the static grid, the total is `O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})` and nothing is gained in the exponent; if the fallback is COAT, COAT alone already gives the adaptive rate. A short burn-in `n_0 = n^{gamma}` does not work: the occupancy count of `n_0` draws can underestimate that of `n` draws by a factor up to `n/n_0` (the map `m -> E N_m(l) = sum_C (1 - (1 - nu(C))^m)` is concave with `E N_0 = 0`, hence `E N_n(l) <= (n/n_0) E N_{n_0}(l)` and this is attained up to constants by a measure with mass `1/n` spread over `n` cells), and the relevant scale for the play phase is the one for `n` draws.
- Verdict: correct but dominated by COAT; at most a footnote.

END OF SECTION C
