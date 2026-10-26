# C4: which partitions are safe when the arm rewards are chosen by strategic agents

Worker report, 18 September 2026. Output directory `audit/round2/B/theorems/c4-safe-partitions/`.
No canonical file was modified. Code, seeds and raw outputs:
`<scratchpad>/round2/c4-safe-partitions/` (`partitions.py`, `fastsim.py`, `w1.py`, `w2.py`,
`w2b.py`, `w3.py`, `rate.py`, `job_rate.sh`, `logs/`). Compute log: `COMPUTE_LOG.md` in this
directory.

Documents read in full before starting: `audit/round2/prompts/COMMON.md`;
`audit/round2/B/theorems/c4-safe-partitions/TASK.md`;
`audit/round2/B/scouts/CONTEXT_ONLY_PARTITIONS.md` (Sections 0, A, B, C, all that is on disk);
`audit/round2/B/CONTEXT_PROOF_CONTRACT.md`; `audit/round2/B/MATH_CANDIDATE_LEDGER.md` Section 5
and Section 6.1; `audit/round2/B/theorems/c2-local-mesp/ADVERSARY.md`;
`sections/contextual_samf_algorithm.tex`; `sections/appendix_contextual.tex`;
`sections/contextual.tex`.

Every statement below is classified in Section 8 as PROVED, PROVED UNDER STATED HYPOTHESES,
NUMERICALLY CONFIRMED, INCOMPLETE, or OPEN. I do not claim any of it is error free; Section 9
names the step I consider least secure and says why.

## 0. Answer in one page

Revised 18 September 2026 after the adversary report in `ADVERSARY.md`, which found two P1 defects
of the shape "correct proofs, headline broader than the proofs". Both are accepted in full; I
reproduced both with my own simulator before rewriting. What changed: the claim "context-only
partitions are safe" was false and is withdrawn; Theorem 5 was presented as a witness for reward
dependence and does not exercise it, so it is demoted and its role reassigned. Section 4.8 records
the correction in detail. Nothing that was proved has been withdrawn.

**The question.** Which partition rules keep the contextual results of the manuscript when the
arm rewards are chosen by strategic agents, and is there a rule that adapts to the geometry of
the context law without the horizon, the Lipschitz constant, or the context law itself.

**The answer.**

1. *Being a function of the contexts alone buys the two things the manuscript's proofs need, and it
   does not by itself buy safety.* If the partition process is a measurable function of the contexts
   alone (requirement R1), with fresh label-local statistics (R2), under exogenous arrivals (R3),
   then every cell epoch is a fixed-mean instance with the future independence the manuscript's
   proofs use (Lemma 1, Lemma 2), and the two executions of the monotonicity coupling carry the
   *same* partition, which is exactly what that proof needs. What (R1) to (R3) do **not** give is the
   aggregation over cell epochs, and Corollary 3 says so. Safety in the sense of Section 1.3
   additionally requires a schedule condition (R4): the total exploration must be sublinear and the
   visit-weighted mesh must shrink. A context-only rule that violates (R4) is unsafe, and Section 4.8
   gives one: rule A0, which is COAT with its split threshold lowered to the end of the exploration
   phase. So the correct statement is **(R1) to (R3) plus (R4)**, and Section 5 is the proof that
   COAT satisfies (R4) with an explicit rate.

2. *What reward dependence costs, given (R4).* Each failure below is stated for a rule that would
   satisfy (R4) if its reward clause were deleted, so that the clause and not the schedule is doing
   the work. (Theorem 3 is also true for the no-floor decision schedule, but there the deleted-clause
   rule is A0, which violates (R4), so the floored variant is the one to quote.) The test is applied
   explicitly in Section 4.9 and stated in Section 9.2.0.

   - **Theorem 4, the headline witness (robustness at honest play).** Add one sentence to a
     context-only rule, "freeze this leaf instead of splitting it if its top two exploration means
     differ by more than `theta_l`", and change nothing else. The rule loses a linear amount of the
     honest benchmark with **no deviation at all**, every agent honest and at capacity, intrinsic
     means Lipschitz, on an instance satisfying every hypothesis of `thm:grid-etc`. The deficit per
     round converges to the predicted `c^2/2`: measured 0.02067, 0.01833, 0.01776 against
     `c^2/2 = 0.017578`, against the *same rule with the sentence deleted*, whose deficit is bounded
     by `o(n)` by Theorem D.1 (Section 4.9 gives the table and says plainly which half of the
     comparison is measured and which half is proved). It holds with a single fixed `q_0` at every
     horizon, and for every `c in (0, 1/2 - theta_0)`. The reason is
     structural: freezing is a test that a cell is decided, and such a test is sound only if the
     threshold dominates the within-cell variation of the *delivered* means. The platform does not
     know a Lipschitz constant, and in this model the delivered maps need not be Lipschitz at all,
     because the agents choose them.
   - **Theorem 3 (monotonicity).** The same sentence costs exact pathwise monotonicity and expected
     monotonicity with any `o(n)` remainder: raising agent 1's map pointwise to its capacity raises
     `E T_3` from `q_0` to `n/2 - o(n)`, in the direction the axiom forbids. Three honest agents,
     constant intrinsic means, i.i.d. contexts. Measured: `E T_3` goes from 2000 to 91139 at
     `n = 200000`, while three context-only rules give the identical count under both maps. The
     adversary's Section A3.2 argues that this failure is a second symptom of Theorem 4's mechanism
     rather than an independent one; I have not settled that and record it in Section 4.8.
   - **Theorem 5 is no longer offered as a witness for reward dependence.** It is true, and its
     instance is one on which the reward clause is almost surely inert, so the identical failure is
     produced by a rule satisfying (R1) to (R3). Its correct role is the one it now has in
     Section 4.4: it is the witness for the *necessity of (R4)*, which is why (R4) is in the
     definition of the safe class at all.
   - **Section 4.6**, inheriting an ancestor's elimination verdict costs a linear amount at honest
     play, for the same smoothness reason.

3. *There is a context-only adaptive rule, and it is the one the scout named.* COAT, dyadic
   splitting triggered by a leaf's own since-creation visit count with fresh statistics per leaf,
   uses neither `n`, nor `L`, nor `nu`, is anytime, and attains
   `O((KA)^{1/(d_nu+3)} n^{(d_nu+2)/(d_nu+3)})` under a dyadic covering assumption of exponent
   `d_nu`, with exact pathwise monotonicity, expected FATA, and the continuous public equilibrium.
   Section 5 supplies Section D of the scout file: the counting argument (Lemma 7) and Theorems
   D.1 to D.5 with proofs. The adversary checked every lemma, constant, the balancing, the Lipschitz
   step and the pathwise monotonicity including the tie case, and found no error.

**Principle, in the form I can defend.** A partition rule is safe when its geometry is fixed by the
contexts and its schedule keeps exploration sublinear and the mesh shrinking. Reward dependence is
harmful not because it breaks the cell law, which survives it (Lemma 6), but because a reward event
that stops the refinement makes the effective mesh, and hence the Lipschitz bias, a quantity the
agents choose, and because it makes the two executions of the monotonicity coupling carry different
partitions. It is not true that every use of rewards in a partition is harmful, and it is not true
that avoiding rewards is sufficient.

**Scope of the converse, because it is the claim worth acting on.** It defeats a *family* of rules,
not reward-adaptive splitting in general, and after the adversary's report it rests on Theorem 4 as
the one independent witness, with Theorem 3 as the monotonicity symptom. Theorem 4 defeats every
threshold schedule with `theta_0 < 1/2` (and, by the adversary's sharpening, for any fixed
`c < 1/2 - theta_0`, and with a constant `q_0`). Theorem 3 defeats one rule on one instance in both
modes at once. Theorem 3' lifts that to a class under hypotheses I verify only for the witness.
Two natural rules escape and are named in Section 4.7: partitions that also read independent
platform coins (safe, fold them into `Z`), and *accelerate-only* rules whose split times are
sandwiched between two context-only schedules and which never freeze a leaf on a reward event. The
accelerate-only escape is **larger** than I first thought: my sketch that they lose monotonicity does
not work for the anytime sandwich it was offered for, the adversary gives a martingale argument that
they keep monotonicity to `o(n)`, I close one gap in that argument and a second gap remains, and the
question is recorded OPEN in Section 4.7 with both arguments attached. If the argument is completed,
(R1) is needed only for *exact pathwise* monotonicity and for nothing else.

**The hypothesis all of this leans on** is that the platform has no known modulus for the
*delivered* maps. Section 9.2 sets out what happens if that is removed: after the demotion of
Theorem 5, **no** witness in Section 4 survives it, which is worse than what I wrote before.

**What COAT buys and costs.** It buys one thing over the two-line doubling remark: the exponent
`(d_nu+2)/(d_nu+3)` in place of `(D+2)/(D+3)`. That gain is conditional on `d_nu < D`, a property of
the context law the platform cannot verify, and in the default reading of the model (independent
per-agent contexts with densities) `d_nu = D` exactly and the gain is zero. It is never worse in the
exponent, and it is worse in constants and in finite-horizon behaviour. Section 5.0 states this
plainly and Section 5.6 has the numbers.

**Citations (job 3).** Both were verified from primary sources on 18 September 2026 and both
differ from a context-only partition, but the ledger's one-line description of one of them is
wrong: Perchet and Rigollet's ABSE is **not** a static partition. Section 7. The adversary re-fetched
both sources independently and confirmed every quotation.


## 1. Primitives, the three requirements, and the notion of safety

Notation follows `audit/round2/B/CONTEXT_PROOF_CONTRACT.md`. `X = [0,1)^D` half open (so dyadic
cubes tile it exactly), `D = Kd`, profiles `X_t = (x_{1,t},...,x_{K,t})` i.i.d. `nu`, agents
`i in [K]`, capacities `M_i(x_i)`, intrinsic means `mu_i(x_i)`, honest benchmark
`b(X) = max_{h in K_H} mu_h(x_h)`, class `S_HDS` of horizon-dependent stationary measurable maps
`m_{i,n} : X -> [0, M_i(x_i)]` fixed before play.

### 1.1 Primitives and the coupling convention

Fix `n`; every statement below holds for each `n`, which is what makes the anytime claims of
Section 5 possible. Conditionally on the agents' ex ante randomization `omega_A` (so that the maps
`m_{i,n}` are fixed measurable feasible maps), the primitives are

- contexts `X_1, X_2, ...` i.i.d. `nu`;
- reward uniforms `U_1, U_2, ...` i.i.d. Uniform[0,1], one per round, used as
  `Y_t = 1{U_t <= m_{I_t,n}(X_t)}`;
- an independent random element `Z` (the burn-in contexts of a sample-split design, or nothing);
- platform coins `xi = (xi_lambda)_lambda`, one independent family per cell-epoch label
  (exploration permutations, priority permutations, tie coins);

and these four families are mutually independent given `omega_A`.

Seed indexing. The manuscript's couplings index reward uniforms by the agent's own local pull index
inside the relevant instance (contract, Sections 1 and 14.1). Indexing by the global round `t` gives
the same law for a single execution. In every coupling used below both executions have the same
exploration rounds for agent `i` in every cell epoch, so the two indexings coincide there and no
reproof is needed. Indexing by an agent's overall pull count across cells would *not* coincide and
is never used. (This is the scout's Section B.1 convention; I checked it against
`appendix_contextual.tex`, proof of `thm:grid-etc` monotonicity, which couples "reward uniforms on
common exploration pulls of agent `i`".)

### 1.2 Partition processes, labels, and the three requirements

A partition process is a sequence `P_1, P_2, ...` of countable measurable partitions of `X`. For
`C in P_t` set `tau_t(C) := min{s <= t : C in P_u for all u in [s,t]}`. The **cell-epoch label** of
round `t` is `Lambda_t := (C_t, tau_t(C_t))`, where `C_t in P_t` is the cell containing `X_t`.
Rounds carrying the same label are the visits of one cell during one uninterrupted life; the label
determines the cell as a set, written `C(lambda)`, and its dyadic level `lev(lambda)`.

- **(R1) label-adapted partition.** There are measurable maps `pi_t` with
  `P_t = pi_t(Z, Lambda_1, ..., Lambda_{t-1})`. Which cells exist at round `t` depends on the past
  only through the labels the past rounds carried, never through the exact positions of past
  contexts beyond their labels, and never through rewards, selections, or platform coins.
- **(R2) label-local fresh statistics.** `I_t = phi(Lambda_t, H_t(Lambda_t), xi_{Lambda_t})` for a
  fixed measurable rule `phi`, where `H_t(lambda) := ((I_s, Y_s) : s < t, Lambda_s = lambda)`. No
  data from another label (in particular none from a parent cell), no exact position `X_t`, no
  global clock.
- **(R3) exogeneity.** `(X_t)`, `(U_t)`, `Z`, `xi` mutually independent given `omega_A`.

Examples. The static grid: `P_t = grid(h_n)`, (R1) trivially. Doubling epochs with a fresh grid per
epoch (Section 2.4): (R1) trivially. Sample splitting on a burn-in: `Z = (X_1,...,X_{n_0})`,
`P_t = tree(Z)` for `t > n_0`, (R1) with `pi_t` ignoring the labels. COAT (Section 5): `P_{t+1}`
equals `P_t` unless the label `Lambda_t` has now been carried by exactly `N_{lev(Lambda_t)}` rounds,
in which case `C(Lambda_t)` is replaced by its `2^D` dyadic children; this is a function of the
label sequence, so (R1) holds. That children count from zero is essential: if a child inherited its
parent's visits by position, `P_{t+1}` would depend on the exact positions of earlier contexts and
(R1) would fail.

Selection-triggered splits (splitting on `T_i(C)` rather than on `V_C`) are reward dependent,
because selections depend on rewards through the cell rule. Visit-count-triggered splits are not,
because `V_C` is a function of the contexts alone.

### 1.3 What "safe" means here

The manuscript asks four things of a contextual rule (contract, Section 6): contextual sharp
adaptivity, contextual monotonicity, contextual FATA, and global robustness, plus, in the public
setting, that all-maximum play is a restricted asymptotic equilibrium. I call a partition rule
**safe** if it keeps all of these with `o(n)` remainders uniformly over `S_HDS`, on every instance
of the model, with an algorithm that is allowed to know `n, K, D` and nothing else.

Safety is not implied by (R1) to (R3). Those three requirements give the per-cell statistics and the
coupling; they say nothing about how many cells there are or how large they are, and Corollary 3
records this explicitly. A fourth, purely schedular requirement is needed:

- **(R4) admissible schedule.** Pathwise, the total exploration is sublinear and the visit-weighted
  mesh shrinks: writing `e_l` for the number of visited level-`l` leaf epochs, `n_l` for the rounds
  held at level `l`, and `q_l` for the leaf exploration size at level `l`,
  `sum_l K q_l e_l = o(n)` and `S := sum_l 2^{-l} n_l = o(n)`.

The first clause bounds the price of re-exploring fresh leaves and the second bounds the Lipschitz
bias, and Lemma 7 and Lemma 7' are the proof that COAT satisfies both with an explicit rate. The
static grid satisfies (R4) trivially. Section 4.8 exhibits a rule satisfying (R1) to (R3) and
failing (R4), which is unsafe, so (R4) is not redundant.

The point of the whole section is therefore not that safety is the same thing as context-only
geometry. It is that (R1) to (R3) are what the manuscript's per-cell proofs and its monotonicity
coupling need, that (R4) is what the aggregation needs, and that a reward-dependent freeze decision
destroys (R4) in a way no schedule can repair, because the level at which a leaf stops refining
becomes a reward event.

## 2. The safe class: results already on disk, written out

Everything in this section is due to `audit/round2/B/scouts/CONTEXT_ONLY_PARTITIONS.md`, Sections
A.2, B.3, B.4 and C.2'. I have checked each proof line by line against
`sections/appendix_contextual.tex` and reproduce them here in full, with three corrections marked
CORRECTION.

### 2.1 Lemma 1 (product structure of the contexts given the labels)

**Lemma 1** (scout Lemma B.1). Assume (R1) and (R3). Conditional on `Z` and on
`Lambda_{1:n} = lambda_{1:n}` (an event of positive conditional probability), the contexts
`X_1, ..., X_n` are independent with `X_t ~ nu( . | C(lambda_t))`. Consequently, for every label
`lambda`, the ordered contexts of the rounds carrying `lambda` are i.i.d. `nu( . | C(lambda))`, and
the contexts of rounds carrying different labels are independent.

*Proof.* Work conditionally on `Z = z`; by (R3), `X_{1:n}` is i.i.d. `nu` given `Z = z`. Fix
`lambda_{1:n}`. By (R1), `P_1 = pi_1(z)` is deterministic, and given
`Lambda_{1:t-1} = lambda_{1:t-1}` the partition `P_t = pi_t(z, lambda_{1:t-1})` is deterministic, so
there is a deterministic set `D_t := C(lambda_t) in P_t` (if `lambda_t` names no cell of that
partition the event is empty and there is nothing to prove). Since `P_t` is a partition,
`{Lambda_t = lambda_t} cap {Lambda_{1:t-1} = lambda_{1:t-1}} = {X_t in D_t} cap {Lambda_{1:t-1} = lambda_{1:t-1}}`.
By induction `{Lambda_{1:n} = lambda_{1:n}} = cap_{t <= n} {X_t in D_t}`, a product set. Hence for
measurable `A_1, ..., A_n`,
`Pr(X_t in A_t for all t, Lambda_{1:n} = lambda_{1:n} | Z = z) = prod_t nu(A_t cap D_t)`,
while `Pr(Lambda_{1:n} = lambda_{1:n} | Z = z) = prod_t nu(D_t) > 0`. Dividing gives
`prod_t nu(A_t | D_t)`. The two consequences are restrictions of a product law to subfamilies of
coordinates. QED

Remark (why exact positions may be conditioned away). The lemma conditions on the entire label
sequence, including the labels of future rounds. This is what the manuscript's `lem:cell-law` also
does ("conditional on its membership-indicator sequence"), and it is what makes "conditional on
`V_C = s`, the cell is an `s`-round fixed-mean instance" legitimate. Under (R1) the labels carry no
information about positions beyond cell membership, which is why the conditional law stays a
product of cell-conditional laws.

### 2.2 Lemma 2 (cell-epoch law and future independence)

**Lemma 2** (scout Lemma B.2). Assume (R1), (R2), (R3) and fixed maps. Condition on `Z` and
`Lambda_{1:n} = lambda_{1:n}`. Let `lambda` be a label with `C := C(lambda)`, `nu(C) > 0`, carried
by the rounds `t_1 < ... < t_s`. Then:

(i) for every `r <= s`, conditionally on `((I_{t_u}, Y_{t_u}))_{u < r}` and `xi_lambda`, the
selection `I_{t_r}` is the output of `phi` on those data, and
`Pr(Y_{t_r} = 1 | ((I_{t_u},Y_{t_u}))_{u<r}, xi_lambda, I_{t_r} = i) = bar m_{i,C}` where
`bar m_{i,C} := E[m_{i,n}(X) | X in C]`. That is, `(I_{t_r}, Y_{t_r})_{r <= s}` has the law of the
first `s` rounds of an execution of the scalar rule `phi(lambda, ., xi_lambda)` on a `K`-armed
fixed-mean Bernoulli instance with means `(bar m_{i,C})_{i in [K]}`;

(ii) executions of distinct labels are conditionally independent;

(iii) for every `r < s`, the data `((I_{t_u}, Y_{t_u}))_{u <= r}` and any function of them and of
`xi_lambda` are independent of `(X_{t_u})_{u > r}` and of the contexts of every round carrying
another label;

(iv) in particular, for measurable `R` and any function `W` of the first `r` rounds' data of
`lambda`, `E[1{X_{t_u} in R} W] = nu(R | C) E[W]` for `u > r`.

*Proof.* Conditionally on `(Z, Lambda_{1:n})`, Lemma 1 makes the contexts independent with
`X_{t_r} ~ nu( . | C)`, and by (R3) the uniforms `U_{t_r}` and the coins `xi_lambda` are independent
of everything else and of each other (conditioning on a function of the contexts alone does not
disturb the other independent families). Induct on `r`. By (R2), `I_{t_r}` is a function of
`H := ((I_{t_u},Y_{t_u}))_{u<r}` and `xi_lambda`, which are functions of `(X_{t_u},U_{t_u})_{u<r}`
and `xi_lambda`; hence `X_{t_r}` and `U_{t_r}` are independent of `(H, xi_lambda, I_{t_r})`.
Therefore
`Pr(Y_{t_r} = 1 | H, xi_lambda, I_{t_r} = i) = E[Pr(U_{t_r} <= m_{i,n}(X_{t_r}) | X_{t_r})] = int m_{i,n} dnu( . | C) = bar m_{i,C}`,
and `Y_{t_r}` is conditionally independent of `(H, xi_lambda)` given `I_{t_r}`. This is the
transition structure of a fixed-mean bandit execution of `phi`, proving (i). (ii) holds because the
executions are functions of disjoint subfamilies of the independent primitives
`(X_t, U_t)_{t in lambda}, xi_lambda`. (iii) and (iv) hold because the first `r` rounds' data are
functions of `(X_{t_u}, U_{t_u})_{u <= r}` and `xi_lambda`, independent of `(X_{t_u})_{u>r}` and of
the other labels' contexts by Lemma 1 and (R3). QED

CORRECTION 1. The scout's statement of (i) says "against `K` independent Bernoulli reward streams".
The potential rewards of different agents at one visit are **not** independent: they are generated
from the same context `X_{t_r}` (and, in the manuscript's realization, may share a uniform). What
the proof gives, and all that is used, is the displayed conditional law of the *selected* reward,
which is exactly the standard stochastic bandit transition structure. The manuscript is careful
about this in two places (`lem:cell-law`: "Coordinates are correlated across agents through the
shared profile; the per-agent concentration arguments below never use independence across agents";
`lem:etc-tail`: "The observations of the two agents need not be independent of one another"), and
the statement above is phrased to match. No downstream step changes.

**Corollary 3 (what carries over verbatim).** Every per-cell step in the manuscript's grid proofs
uses `lem:cell-law` only through (i) to (iv): the gap-free UCB bound conditional on `V_C = s`
(robustness), `lem:ucb-deficit` inside a cell (sharp adaptivity, the public-equilibrium step),
`lem:etc-tail` applied to `q` exploration samples with means `bar m_{i,C}` (ETC), the factorization
"commitment probability times conditional cell mean" (ETC exploitation, sharp adaptivity, FATA,
public equilibrium, and `lem:region`), and label symmetry inside a cell (FATA). Hence every such
step holds per cell epoch for any partition process satisfying (R1) to (R3), with `C` the cell of
the epoch and `s` the epoch's visit count. What does **not** carry over automatically is the
aggregation over cell epochs: their number and their diameters are now random. That is the content
of Section 5, and it is exactly the gap that requirement (R4) of Section 1.3 fills. A rule can
satisfy (R1) to (R3), and hence this corollary, and still be unsafe, because this corollary says
nothing about how many epochs there are; Section 4.8 gives such a rule.

### 2.3 Occupied-cell accounting

Let `N_occ(n) := #{C : V_C(n) >= 1}` and `N_nu(h) := #{C in grid(h) : nu(C) > 0}`. Visited cells
have positive mass almost surely, so `N_occ(n) <= min{J_n, n, N_nu(h_n)}` pathwise, and
`E N_occ(n) = sum_C (1 - (1 - nu(C))^n)`.

Grid-UCB1 (proof of `thm:grid-ucb-robust`): the per-cell bound summed with Cauchy-Schwarz gives,
pathwise in the visit counts,
`sum_C [C sqrt(K V_C log(en)) + C K 1{V_C >= 1}] <= C sqrt(K N_occ n log(en)) + C K N_occ`,
so by Jensen (`E sqrt(N_occ) <= sqrt(E N_occ)`),
`E sum_t [b(X_t) - m_{I_t,n}(X_t)] <= 2 L sqrt(D) n h_n + C sqrt(K N_nu(h_n) n log(en)) + C K N_nu(h_n)`.

Grid-ETC (proof of `thm:grid-etc`): exploration costs at most `K q_n` per visited cell, so
`K q_n J_n` may be replaced by `K q_n N_occ <= K q_n N_nu(h_n)`:
`E sum_t [b(X_t) - m_{I_t,n}(X_t)] <= K q_n N_nu(h_n) + 2 L sqrt(D) n h_n + C K n q_n^{-1/2}`.

The same replacement applies verbatim to the sharp-adaptivity error and to the exploration term
`q_n J_n` in `thm:contextual-public`, and to nothing else (monotonicity and FATA do not count
cells). This is PROVED: it is literally the manuscript's proof with each sum restricted to visited
cells, and unvisited cells contribute zero to every sum. The manuscript already states the
conclusion in one sentence after `thm:grid-ucb-robust` ("Cells are initialized lazily, so every
count of cells above may be replaced by the number of cells that carry positive mass").

The exponent does not move, because `h_n` is tuned to `D`. If `supp(nu)` satisfies
`N_nu(2^{-l}) <= A 2^{l d_nu}` and `d_nu` were known, retuning `h_n` would give the exponents
`(d_nu+1)/(d_nu+2)` (UCB) and `(d_nu+2)/(d_nu+3)` (ETC). The adaptivity problem for context-only
partitions is exactly the problem of choosing the scale without knowing `l -> N_nu(2^{-l})`, and
Section 5 solves it.

### 2.4 Doubling epochs with a fresh static grid (DE-Grid): the cheap anytime statement

In epoch `k = 0, 1, 2, ...` (rounds `t in [2^k, 2^{k+1})`, the last truncated at `n`) run Static
Grid-ETC, or Grid-UCB1, with horizon parameter `n_k = 2^k`: fresh grid of side `h_{n_k}`, fresh
`q_{n_k}`, fresh statistics in every cell, nothing carried across epochs. The labels are
`(epoch, cell)` and the partition process is deterministic, so (R1) to (R3) hold. Each epoch's
primitives are independent of the past and the maps are fixed, so each per-epoch statement is the
manuscript's theorem at horizon `n_k`, applied conditionally on the past.

- Rate: `sum_{k <= log2 n} C n_k^{(D+2)/(D+3)} <= C n^{(D+2)/(D+3)} / (1 - 2^{-(D+2)/(D+3)})`.
- Monotonicity: exact pathwise (each epoch is a Grid-ETC execution with an identical partition and
  identical exploration rounds in the two coupled executions; sum over epochs).
- FATA: expected, remainder `sum_k n_k nu((partial G)^{sqrt(D) h_{n_k}}) = o(n)` by Cesaro, since
  the factors `nu((partial G)^{sqrt D h_{n_k}})` tend to zero.
- Public equilibrium: the per-epoch deviation gain is `g(n_k) = o(n_k)` by `thm:contextual-public`,
  and `sum_k g(n_k) = o(n)` by the same Cesaro argument.

PROVED given the manuscript's theorems as black boxes. This removes the known horizon from every
continuous contextual result at the cost of two sentences. It is not adaptive to `d_nu`.

## 3. The witness rules

To make the converse an argument about *reward dependence* and not about anything else, the witness
must differ from the manuscript's own algorithm in exactly one sentence.

**Definition (RA-ETC).** Fix a threshold schedule `(theta_l)_{l >= 0}` with `theta_l >= 0`, an
exploration schedule `(q_l)`, and optionally a context-only decision schedule `(N_l)` with
`N_l >= K q_l`. Cells are half-open dyadic cubes of `[0,1)^D`; the initial partition is the single
cube `[0,1)^D`. A leaf `C` at level `l` carries fresh statistics and runs the manuscript's cell rule
`ETC(q_l)`: its first `K q_l` visits follow `q_l` independent uniform permutations of `[K]`, after
which it commits to the agent with the largest exploration empirical mean, ties broken by an
independent uniform priority permutation drawn once for the leaf; exploitation rewards are ignored.
At the leaf's `D_l`-th visit, where `D_l := K q_l` (no floor) or `D_l := N_l` (context-only floor),
let `G_C` be the difference between the largest and the second largest of the leaf's `K` exploration
empirical means. Then

> if `G_C > theta_l` the leaf is **frozen** (its commitment stands for the rest of the run and it is
> never split); otherwise it is **split** into its `2^D` dyadic children, each with fresh state.

Everything except the displayed sentence is a function of the contexts and of the platform's own
coins. The displayed sentence is the whole of the reward dependence. Note for later: with the
decision schedule `D_l = K q_l` and an instance on which the top two are tied, the displayed sentence
is never triggered, and the rule degenerates to a context-only rule. That is what breaks the witness
of Section 4.4, and it is why Section 4.9 insists on comparing a rule against itself with the
sentence deleted.

**Why this is the right witness.** It is the principle of the two reward-adaptive schemes in the
non-strategic literature, in the manuscript's own notation:

- Perchet and Rigollet's ABSE bursts a bin `B` when, verbatim from Policy 3 of the arXiv v3 text
  (Section 7.1 below), `tau_B >= ell_B and |B| >= 2^{-k_0+1} and |I_B| >= 2`, where `I_B` is the set
  of arms **not yet eliminated** by the bin's successive elimination, and elimination is
  `Ybar^(i) < Ybar^max - gamma U(tau, T)`. The clause `|I_B| >= 2` says exactly "the top two are
  within the confidence window", which is `G_C <= theta_l` with `theta_l` the window. A bin with a
  single surviving arm is never split and its SE keeps pulling that arm: that is "frozen".
- Slivkins' contextual zooming activates a child ball of half the radius centred at
  `(x_t, y)` when the selected ball satisfies `conf_t(B) <= r(B)`, where `y` is the arm the index
  rule selected. Which balls exist, and therefore the induced partition of the context space, is a
  function of which arms the index rule chose, hence of the observed payoffs.

RA-ETC keeps ABSE's split criterion and discards ABSE's inheritance of the surviving arm set;
Section 4.6 shows that restoring the inheritance makes matters worse, not better, so the witness is
not weakened by the simplification.

**A reduction used in all three instances.** Every instance below puts `nu` on the segment
`S = {(u, 0, ..., 0) : u in [0,1)}` with `u ~ Uniform[0,1)`. The level-`l` dyadic cube containing
`(u,0,...,0)` is `I_l(u) x [0,2^{-l})^{D-1}` where `I_l(u)` is the level-`l` dyadic interval
containing `u`. So on `supp(nu)` the level-`l` partition is indexed by `I_l(u)`, splitting a leaf
into its `2^D` children leaves exactly two of them with positive mass, and the whole tree restricted
to `supp(nu)` is the dyadic tree on `[0,1)` in the coordinate `u`. Only positive-mass cells are ever
visited (Section 2.3), so the simulations and the proofs may work with the dyadic tree on `[0,1)`.
This also means `supp(nu)` has dyadic covering exponent `d_nu = 1` with `A = 1`, which is what makes
Section 5 relevant to the same instances.

## 4. The converse

**How to read this section after the adversary report.** The converse is carried by Theorem 4
(Section 4.3), promoted to the headline witness in Section 4.9 in the form that isolates the reward
clause by comparing a rule with itself. Theorem 3 (Section 4.1) is the monotonicity companion, and
whether it is an independent converse or a symptom of Theorem 4's mechanism is open (Section 4.7.1).
Theorem 5 (Section 4.4) is **not** a converse: its instance never takes the freeze branch, and
Section 4.8 records the correction and the counterexample rule A0 that goes with it. The test that
separates a real witness from a spurious one is stated in Section 9.2.0 and is applied to all three:
delete the reward clause from the rule and rerun the instance.

### 4.1 Theorem 3: pathwise and expected monotonicity fail by a linear margin

**Instance W1.** `K = 3`, `d = 1`, `D = 3`, and `nu` the law of `(U, U, U)` with
`U ~ Uniform[0,1)`, that is the diagonal version of the reduction of Section 3 (see the scope repair
at the end of this subsection; the first-axis version is legal under the default reading of the
model and gives figures within a standard error, but the diagonal version is legal under both
readings). All three agents are
honest. Intrinsic means are the constants `mu_1 = 0`, `mu_2 = 0.3`, `mu_3 = 0`, so
`b(X) = 0.3` for every `X` and every `mu_i` is `L`-Lipschitz for every `L >= 0`. Capacities:
`M_1(x_1) = 0.3` for `x_1 in [0,1/2)` and `0.9` for `x_1 in [1/2,1)`; `M_2 = M_3 = 1`. Write
`Lft := {u < 1/2}` and `Rgt := {u >= 1/2}`. The base profile `S = (m_1, m_2, m_3)` is

`m_1 = 0.05` everywhere; `m_2 = 0.3` on `Lft` and `1.0` on `Rgt`; `m_3 = 0.7` on `Lft` and `0.0` on `Rgt`.

All three maps are feasible (`0 <= m_i <= M_i` pointwise), honest (`m_i >= mu_i` pointwise), and lie
in `S_HDS`. The comparison profile `S^{1 up}` replaces `m_1` by `M_1` pointwise, which is exactly
the manuscript's contextual monotonicity comparison. Exact cell means:

|        | agent 1 | agent 2 | agent 3 |
|:-|:-|:-|:-|
| root, base   | 0.05 | 0.65 | 0.35 |
| root, raised | 0.60 | 0.65 | 0.35 |
| `Lft`, raised | 0.30 | 0.30 | 0.70 |
| `Rgt`, raised | 0.90 | 1.00 | 0.00 |

**Theorem 3.** Run RA-ETC with `theta_l = 2^{-l}/8`, `q_l = q_0 4^l`, and either decision schedule,
with `N_0 = o(n)`. Then

(a) *horizon-dependent form.* For every `n` there is a choice `q_0 = O(log n)` with

`E T_3(X; n; S^{1 up}) - E T_3(X; n; S) >= n/2 - O(log n) - N_0`.

(b) *horizon-free form.* There is an absolute constant `q_0` (a number, not a function of `n`) such
that for every `n`

`E T_3(X; n; S^{1 up}) - E T_3(X; n; S) >= n/4 - K q_1 - N_0`.

Form (b) matters because it shows the failure is not an artefact of letting the witness rule read
the horizon: a single fixed rule fails at every horizon.

Hence RA-ETC has neither exact pathwise contextual monotonicity nor expected contextual
monotonicity with any `o(n)` remainder, on an instance on which Static Grid-ETC has exact pathwise
monotonicity with remainder zero (`thm:grid-etc`) and every hypothesis of `thm:grid-etc` holds.

*Proof.* The root exists from round 1 and its epoch is, by Lemma 2 applied to the single label of
the root, a fixed-mean instance with means `bar m_{i,root}`; note that this uses only (R2) and (R3),
not (R1), because the root's identity is deterministic. Its `K q_0` exploration visits give each
agent exactly `q_0` observations, so `hat m_{i,root}` is an average of `q_0` i.i.d.
Bernoulli(`bar m_{i,root}`) variables. By Hoeffding and a union bound,
`Pr(max_i |hat m_{i,root} - bar m_{i,root}| > eps) <= 2 K exp(-2 q_0 eps^2)`. Take `eps = 0.015`.

*Base profile.* On the good event, `hat m_1 <= 0.065`, `hat m_2 in [0.635, 0.665]`,
`hat m_3 in [0.335, 0.365]`. The two largest are agent 2 then agent 3, and
`G_root >= 0.635 - 0.365 = 0.27 > 1/8 = theta_0`. So the root freezes and commits to agent 2 for
the whole run. Agent 3's only selections are its `q_0` exploration visits at the root, so
`T_3 = q_0` on the good event, and `T_3 <= n` always.

*Raised profile.* On the good event, `hat m_1 in [0.585, 0.615]`, `hat m_2 in [0.635, 0.665]`,
`hat m_3 in [0.335, 0.365]`, so the two largest are agents 2 and 1 and
`G_root <= 0.665 - 0.585 = 0.08 < 1/8`. The root splits. The two positive-mass children are `Lft`
and `Rgt`, born at the root's `D_0`-th visit, which is a stopping time. By Lemma 6 below, applied
conditionally on the creation history, each child's epoch is a fixed-mean instance with the child's
cell means run on its own fresh statistics, so the same Hoeffding bound applies to each child's
`q_1 = 4 q_0` exploration observations per agent, conditionally on that history and hence also
unconditionally after averaging. On the
corresponding good event: in `Lft` the means are `(0.30, 0.30, 0.70)`, so
`G_Lft >= 0.685 - 0.315 = 0.37 > theta_1 = 1/16` and `Lft` freezes on agent 3; in `Rgt` the means
are `(0.90, 1.00, 0.00)`, so `G_Rgt >= 0.985 - 0.915 = 0.07 > 1/16` and `Rgt` freezes on agent 2.
Hence agent 3 receives every exploitation visit of `Lft`, plus `q_1` exploration visits in each of
`Lft` and `Rgt`, plus `q_0` at the root:
`T_3 >= V_Lft(n) - K q_1 - N_0` where `V_Lft(n) = #{t <= n : u_t < 1/2}`.

*Combining.* Let `G` be the intersection of the three good events; a union bound gives
`Pr(G^c) <= 6 K exp(-2 q_0 eps^2) =: delta`. Then
`E T_3(S^{1 up}) >= E[(V_Lft - K q_1 - N_0) 1_G] >= n/2 - K q_1 - N_0 - n delta`
and `E T_3(S) <= q_0 + n delta`. Choosing `q_0 = ceil((2 eps^2)^{-1} log(6 K n))` makes
`delta <= 1/n` and `q_1 = 4 q_0 = O(log n)`, which gives (a). For (b), fix `q_0` large enough that
`delta = 6 K exp(-2 q_0 eps^2) <= 1/8` with `eps = 0.015`, a choice that does not involve `n`; then
`E T_3(S^{1 up}) - E T_3(S) >= n/2 - K q_1 - N_0 - 2 delta n >= n/4 - K q_1 - N_0`. QED

The Hoeffding constant is loose: in the simulation of `w1.py` the good event never failed in six
seeds at `q_0 = 2000`, and `E T_3` under the base profile was exactly `q_0 = 2000` every time, so
the true `delta` at `q_0 = 2000` is far below the `1/8` the bound needs.

**Numerical confirmation, corrected.** The adversary (`ADVERSARY.md`, X5) found that two rows of my
first table were mislabelled: the row headed "Static grid, one split" used the witness rule's
level-scaled exploration `q_l = q_0 4^l`, so it was an eight-cell grid, and the row headed "COAT"
used the witness rule's schedules rather than the ones defined in Section 5.1. Both are labelling
errors in the table, not disagreements between simulators: the adversary's independent figures for a
genuine one-split grid (98130) and for COAT as defined in Section 5.1 (97628) are reproduced below.
Rerun in `w1b.py`, on the diagonal support (the X6 repair below), 6 seeds, `n = 200000`,
`q_0 = 2000`, `theta_0 = 1/8`, `N_l = 8000 * 8^l`, with each grid row using a single `q = 2000`:

| rule | `E T_3` under `S` | `E T_3` under `S^{1 up}` |
|:-|:-|:-|
| RA-ETC, no floor | 2000.0 (s.e. 0.0) | 91138.5 (s.e. 79.1) |
| RA-ETC, context-only floor | 2000.0 (s.e. 0.0) | 90131.0 (s.e. 76.6) |
| Static grid, one split, two cells, `q = 2000` | 98140.2 (s.e. 78.3) | 98140.2 (s.e. 78.3) |
| Static grid, eight cells, `q = 2000` | 92140.2 (s.e. 78.3) | 92140.2 (s.e. 78.3) |
| COAT exactly as in Section 5.1 (`q_l = 4^l`, `N_l = K 8^l`) | 97799.5 (s.e. 78.1) | 97799.5 (s.e. 78.1) |

The three context-only rows agree with the adversary's independent figures to within about two
standard errors (98140 against 98130, 92140 against 92130, 97800 against 97628). Every context-only
rule gives the identical count under the two profiles, pathwise identical as its monotonicity proof
predicts, because the raise does not change which agent wins any cell here; the reward-adaptive rule
moves `E T_3` by `0.45 n`.

**Scope repair (adversary X6), already applied above.** `sections/setting.tex` line 59 has a
conditional clause: "If agents observe only their own contexts `x_i`, their maps must depend only on
`x_i`." Under the default reading (the selected agent observes the full profile) W1 as first stated
is legal, because `m_2` and `m_3` may depend on `u = x_1`. Under the parenthetical own-context
reading they are not, since `nu` was supported on `{(u,0,0)}` so that `x_2 = x_3 = 0` almost surely.
The repair is to put `nu` on the diagonal `{(u,u,u)}`, exactly as instance W4 of Section 4.6 already
does. The dyadic reduction of Section 3 is unchanged, the level-`l` cube containing `(u,u,u)` being
`I_l(u)^3`, which the diagonal meets in exactly two of its eight children; every cell mean is
unchanged; and every agent's map is then a function of its own context. The table above is computed
on the diagonal and its figures are within a standard error of the first-axis ones, so nothing
depends on the choice. W2, W3 and W4 are already immune, their maps being constants or functions of
the agent's own coordinate. **W1 should be stated on the diagonal**, so that the witness does not
depend on which reading a referee takes.

### 4.2 Theorem 3': the same failure for a class of rules, not one rule

The construction used only two features of RA-ETC: that the root's decision flips when agent 1's
root cell mean is raised, and that after a split the children commit to their own cell-best agent.

**Theorem 3'.** Let `A` be any partition-based algorithm on `[0,1)^D`, `D >= 1`, with dyadic leaves,
fresh label-local statistics (R2), whose root is either frozen or split into its `2^D` children at a
decision time `D_0`, and whose local rule, on a fixed-mean instance of length `s`, commits to an
agent with the largest mean with probability `1 - o(1)` as `s -> infinity` whenever the largest and
second-largest means differ by a fixed positive amount. Suppose `A` is *reward-decisive at the
root*: there are root mean vectors `v` and `v'` with `v'_1 > v_1` and `v'_a = v_a` for `a != 1` such
that `Pr(freeze | v) -> 1` and `Pr(split | v') -> 1`. Write `V := max_a v_a` and assume
`max_a v'_a = V`, that `V` is attained by some agent `a != 1, 3`, that `V/2 < v_3 < V`, and that
`2 v'_1 - v_1 <= 1`. Then
there is an instance in the manuscript's model, with all agents honest and all intrinsic means
constant, on which

`E T_3(X;n; S^{1 up}) - E T_3(X;n; S) >= n/2 - o(n)`.

*Proof.* Choose `m_3` constant on `Lft` and on `Rgt` with `bar m_{3,root} = v_3` and
`bar m_{3,Lft} = beta` for some `beta in (V, 2 v_3)`, which is a nonempty interval exactly because
`V/2 < v_3`; the value on `Rgt` is then `2 v_3 - beta in [0, V)`, so the map is feasible with
capacity `M_3 = 1`, and agent 3 is strictly the largest on `Lft` by `beta - V > 0` under both
profiles. Take `m_1 := v_1` constant and `M_1 := v_1` on `Lft`, `2 v'_1 - v_1` on `Rgt`, which is a feasible
capacity because `2 v'_1 - v_1 <= 1`, has root average `v'_1`, and satisfies
`bar M_{1,Lft} = bar m_{1,Lft} = v_1`. Choose `m_a` for
`a != 1, 3` constant equal to `v_a`. Then the root means are `v` under the base profile and `v'`
under the raise, while the `Lft` means have agent 3 strictly largest under both profiles by a fixed
positive margin. Under the base profile the root freezes and commits to an agent with the largest
root mean, which is not agent 3, so `T_3 = o(n)`; under the raise the root splits and the left child
commits to agent 3, so `T_3 >= V_Lft - o(n)`. QED

I have not proved that every reward-dependent rule is reward-decisive at the root; that is the
honest limit of this direction and is recorded as OPEN in Section 8. A rule that is *never*
reward-decisive, at any cell and any instance, has a partition process that is almost surely a
function of the contexts alone, which is (R1).

### 4.3 Theorem 4: robustness fails by a linear margin at honest play

The next witness needs no deviation at all. Every agent is honest and delivers its capacity; only
the platform is hurt.

**Instance W3.** `K = 2`, `d = 1`, `D = 2`, `nu` as in the reduction. Agent 1 is honest with
`mu_1(x_1) = M_1(x_1) = 1 - x_1` (Lipschitz with `L = 1`), so it always delivers `1 - u`. Agent 2 is
honest with `mu_2(x_2) = M_2(x_2) = c`, a constant; since `x_2 = 0` on `supp(nu)`, agent 2 always
delivers `c`. Both maps are in `S_HDS` and honest, and `b(X) = max(1 - u, c)`.

**Theorem 4 (with the adversary's two sharpenings, X9).** Run RA-ETC with any threshold schedule
with `theta_0 < 1/2`, any exploration schedule with `q_0 = o(n)`, and either decision schedule with
`N_0 = o(n)`. Let `c` be **any** constant in `(0, 1/2 - theta_0)`, not only `(1/2 - theta_0)/2`.
Then on instance W3 with that `c`

`E sum_{t<=n} [b(X_t) - m_{I_t,n}(X_t)] >= (c^2/2) n - o(n)`,

whereas Static Grid-ETC has error `O(n^{(D+2)/(D+3)}) = O(n^{4/5})` and COAT has error
`O(n^{3/4})` (Theorem D.1) on the same instance. If `theta_0 >= 1/2` but `theta_l -> 0`, the same
conclusion holds after rescaling `nu` into the level-`l*` dyadic cube at the corner, where `l*` is
the first level with `theta_{l*} < 1/2`; every ancestor of that cube then carries the same cell
means and splits, and the level-`l*` cube freezes.

*Proof.* `bar m_{1,root} = int_0^1 (1-u) du = 1/2` and `bar m_{2,root} = c`, so the true root gap is
`1/2 - c > theta_0`, with slack `s_0 := 1/2 - theta_0 - c > 0` by the choice of `c`. At the special
value `c = (1/2 - theta_0)/2` the slack is `c` itself, which is the case written out below; for a
general `c in (0, 1/2 - theta_0)` replace `c/4` by `min(c, s_0)/4` throughout and every inequality
goes through unchanged. As in
Theorem 3, the root's `q_0` exploration observations per agent are i.i.d. with these means, so by
Hoeffding and a union bound the event `G` that both empirical means are within `c/4` of their cell
means has `Pr(G^c) <= 4 exp(-q_0 c^2/8) -> 0`. On `G` the empirical gap exceeds
`1/2 - c - c/2 = 1/2 - 3c/2 > theta_0` (because `1/2 - theta_0 = 2c` gives
`1/2 - 3c/2 - theta_0 = c/2 > 0`), so the root freezes, and the empirical winner is agent 1. Hence
on `G` every round after the decision selects agent 1, and the benchmark deficit is
`sum_t [max(1 - u_t, c) - (1 - u_t)] = sum_t (c - 1 + u_t)_+`, whose expectation per round is
`int_{1-c}^1 (c - 1 + u) du = c^2/2`. Subtracting the at most `N_0` pre-decision rounds and the
`n Pr(G^c)` rounds on the bad event gives the display. QED

**The theorem does not need `q_0 -> infinity`** (adversary X9, and it is right that I understated my
own result). With `q_0` a fixed constant the good event has a constant probability
`1 - delta(q_0) > 0` rather than `1 - o(1)`, and the conclusion becomes
`(1 - delta(q_0)) (c^2/2) n - N_0`, still linear at every horizon with a single fixed rule. So
Theorem 4, like Theorem 3, has a horizon-free form, and that is the form the paper should state.

**Numerical confirmation** (`w3c.py`, `c = 0.1875`, `theta_0 = 1/8`, `q_0 = 2000`, 3 seeds):
predicted per-round deficit `c^2/2 = 0.017578`.

| `n` | RA-ETC no floor | RA-ETC floor | COAT | Static Grid-ETC |
|:-|:-|:-|:-|:-|
| 200000  | 0.02082 | 0.02082 | 0.06063 | 0.00557 |
| 800000  | 0.01838 | 0.01838 | 0.01676 | 0.00224 |
| 3200000 | 0.01779 | 0.01779 | 0.03279 | 0.00135 |

(deficit per round). The reward-adaptive rule converges to the predicted constant `0.017578` and
does not decay; the static grid decays. COAT's numbers at these horizons are dominated by the
exploration of the deepest level it has just opened, which is a sawtooth (Section 5.5); its bound
is `O(n^{3/4})` but its constant is worse than the grid's on a two-dimensional instance. That is an
honest caveat on COAT and is repeated in Section 6.

**What Theorem 4 says and does not say.** It does not say that ABSE is a bad algorithm. ABSE's
stopping rule is sound because ABSE *assumes* the reward functions are `(beta, L)`-Holder with a
known `L`, and its window is calibrated so that separation at the bin's scale implies uniform
dominance on the bin (Perchet and Rigollet, the paragraph quoted in Section 7.1: "the parameters of
the SE policy run at the birth of bin `B` are chosen exactly such that arms `i` with average gap
`|fbar*_B - fbar^(i)_B| >= C |B|^beta` are eliminated ... The smoothness condition ensures that
these eliminated arms satisfy `f*(x) > f^(i)(x)` for all `x in B`"). The manuscript's platform has
no such assumption available: the delivered map `m_{i,n}` is chosen by agent `i` anywhere in
`[0, M_i(x_i)]`, is assumed only measurable, and `L` is not known to the platform (contract
Section 4: "Grid widths `h_n` and `q_n` do not depend on `L` or `nu`"). So the content of Theorem 4
is: **a reward-adaptive refinement rule imports a smoothness assumption about the arms, and in a
strategic model the arms choose whether it holds.** A context-only rule imports none.

### 4.4 Theorem 5: not a witness for reward dependence, but the witness for (R4)

**Read this first.** In the first version of this file Theorem 5 was offered as the third of three
witnesses that reward-dependent partitions fail. That was wrong, it was found by the adversary
(`ADVERSARY.md`, Section A1.3), and I reproduced the refutation with my own simulator before
rewriting. The theorem below is true and its proof is correct; what was wrong was what I said it
showed. The refutation is short enough to state here and is developed in Section 4.8:

> On instance W2 the two top agents deliver exactly `1`, so their exploration empirical means are
> exactly `1` in every leaf at every level, so the gap statistic `G_C` is `0` with probability one
> and the freeze branch of RA-ETC is never taken on any sample path. The realized partition is
> almost surely identical to that of the rule obtained by **deleting the reward sentence
> altogether**. That rule, call it A0, satisfies (R1), (R2) and (R3), and produces the same `n/4`
> deviation gain and the same `0.175 n` benchmark loss. My own check, `check_adv.py`: setting
> `theta_0 = 10^9`, which deletes the freeze branch, gives gain per round `0.2500` and deficit per
> round `0.1750` at `n = 12500, 50000, 200000, 800000`, identical to RA-ETC to four decimals.

Moreover the tie that drives the mechanism is forced by the instance, not chosen by any agent:
agents 2 and 3 have capacity `1` and `S^max` is the all-maximum profile, and the tie persists
unchanged under the deviation. So no agent controls the split decision here, and Proposition 7(A)'s
sentence "the agents control it, because they control whether the top two separate" is not exercised
by this instance or by any other in this file.

**What the theorem does show, and it is worth keeping.** It shows that a rule satisfying (R1) to
(R3) can concede an `n/4` unilateral deviation gain and miss the honest benchmark by `0.175 n` at a
profile satisfying the two-top hypothesis of `thm:contextual-public`. That is the reason (R4) is in
the definition of the safe class. Read that way the theorem is a *positive* result about what the
safe class must contain, not a converse, and I now state it as such.

**Instance W2.** `K = 4`, `d = 1`, `D = 4`, `nu` as in the reduction. Agent 1 is honest with
`mu_1 = M_1 = 0.9`, so `b(X) = 0.9`. Agents 2, 3, 4 are strategic with `mu_j = 0` and `M_j = 1`, so
`M_*(X) = 1` and `|T(X)| = 3 >= 2` at every profile: the hypothesis of `thm:contextual-public`
("two agents attain the largest capacity at `nu`-almost every profile") holds. The proposed profile
`S^max` has agents 2, 3, 4 deliver `1`. The deviation is `m'_4 := 0`.

**Theorem 5 (restated after the correction).** Run any dyadic rule with fresh label-local
statistics whose leaves split at the end of their exploration phase, `D_l = K q_l` with
`q_l = q_0 4^l`. This includes A0, which is context only and satisfies (R1) to (R3), and it includes
RA-ETC with no context-only floor and any threshold schedule `theta_l >= 0`, whose freeze branch is
almost surely never taken on this instance. Then on instance W2, for every `n`:

(a) under `S^max` and under `(m'_4, S^max_{-4})` alike, every leaf splits at the end of its
exploration phase, so every one of the `n` rounds is an exploration round and each agent receives
`n/K + O(n^{1/3})` selections;

(b) `u_4(n; m'_4, S^max_{-4}) - u_4(n; S^max) = n/4 - O(n^{1/3})`;

(c) `P(n; m'_4, S^max_{-4}) = 0.725 n + O(n^{1/3})` while `E sum_t b(X_t) = 0.9 n`, so the honest
benchmark is missed by `0.175 n - O(n^{1/3})`.

By contrast `thm:contextual-public` gives, for Static Grid-ETC on this instance,
`eta_{4,C} = (bar M_{4,C} - max_{j != 4} bar M_{j,C})_+ = 0` for every cell, hence a deviation gain
of at most `q_n J_n + c_1 n q_n^{-1/2} = O(n^{(D+2)/(D+3)}) = o(n)`, and `thm:grid-etc` gives
robustness error `O(n^{(D+2)/(D+3)})`.

*Proof.* (a) Under either profile the two largest cell means in every cell are `bar m_{2,C} =
bar m_{3,C} = 1`. A Bernoulli(1) variable is identically 1, so both agents' exploration empirical
means are exactly 1 in every leaf and `G_C = 0 <= theta_l`. Hence every leaf is split at its `K q_l`
th visit, and no leaf ever exploits. The exploration blocks are uniform permutations of `[K]`, so
within each completed block every agent is selected exactly once. A leaf that splits has completed
exactly `q_l` full blocks, because `D_l = K q_l` is a multiple of `K`; so the only incomplete block
in the whole run is the current one of each leaf alive at the horizon, costing at most `K - 1` of
imbalance each. By the reduction of Section 3 the positive-mass leaves at level `l` number at most
`2^l`, and reaching level `l(n)` requires `sum_{l < l(n)} K q_l 2^l <= n`, that is
`(K q_0 / 7) 8^{l(n)} <= n`, so the number of leaves alive at the horizon is
`O((n / (K q_0))^{1/3})` and the total imbalance is `O(n^{1/3})`. Hence
`T_j(n) = n/K + O(n^{1/3})` for every `j`.

(b) Per-pull utility is `1 + mu_4 - m_4`, equal to `0` under `S^max` and to `1` under the
deviation, and the pull counts are `n/4 + O(n^{1/3})` in both cases by (a), because the deviation
does not change `G_C` (which is determined by agents 2 and 3).

(c) `P(n) = E sum_t m_{I_t}(X_t) = sum_j T_j(n) bar m_j = (n/4)(0.9 + 1 + 1 + 0) + O(n^{1/3})`. QED

**Numerical confirmation** (`w2b.py`, 3 seeds, `q_0 = 200`, `theta_0 = 1/8`):

| `n` | 12500 | 25000 | 50000 | 100000 | 200000 | 400000 | 800000 |
|:-|:-|:-|:-|:-|:-|:-|:-|
| RA-ETC no floor, gain / n | 0.2500 | 0.2500 | 0.2500 | 0.2500 | 0.2500 | 0.2500 | 0.2500 |
| RA-ETC no floor, deficit / n | 0.1750 | 0.1750 | 0.1750 | 0.1750 | 0.1750 | 0.1750 | 0.1750 |
| Static Grid-ETC, gain / n | 0.0048 | 0.0030 | 0.0018 | 0.0011 | 0.0013 | 0.0008 | 0.0005 |
| Static Grid-ETC, deficit / n | -0.095 | -0.089 | -0.090 | -0.091 | -0.094 | -0.099 | -0.095 |

exactly the predicted constants, over a factor of 64 in the horizon (a negative deficit means the
benchmark is exceeded).

**Adversarial check on Theorem 5** (`w2c.py`, `n = 400000`, `q_0 = 64`, `theta_0 = 1/8`). Replacing
the exact tie between agents 2 and 3 by a gap `eta` gives gain / `n` equal to `0.2500` for
`eta in {0, 0.002, 0.005, 0.01}`, then `0.0936` at `eta = 0.02`, `0.0117` at `0.05`, `0.0014` at
`0.1`, `0.0002` at `0.2`. The mechanism therefore needs the top two to be tied to within the
smallest threshold the rule reaches, `theta_{l(n)}`, which at these parameters is about
`0.125 * 2^{-4} = 0.008`. This is not a weakness of the witness: the hypothesis of
`thm:contextual-public` is that two agents attain the largest capacity *exactly*, so the exact-tie
case is the theorem's own regime and there the failure holds for every `n`. It does mean that the
statement to make in the paper is about tied tops, not about near ties.

**Two objections to Theorem 5 that I raised against myself, and their answers.**

*Objection 1: the witness rule has no depth cap and ABSE has one, so the tree cannot in fact split
for ever.* Correct, and the answer is that the cap does not help, because any cap worth setting is
at or beyond the depth the budget reaches anyway. Suppose the rule freezes every leaf at level
`l_max`. Then the tree still splits at every level below `l_max`, and the deviator's pulls are the
exploration pulls at levels `0` to `l_max`, which total
`sum_{l <= l_max} K q_l e_l`. Under the reduction of Section 3, `e_l <= 2^l`, so this is
`K q_0 sum_{l <= l_max} 8^l = Theta(K q_0 8^{l_max})`, and the deviation gain is
`Theta(min(n, K q_0 8^{l_max}))`. It is linear in `n` if and only if
`8^{l_max} = Omega(n / (K q_0))`, that is if and only if the cap is at or beyond the level the
exploration budget reaches. ABSE's own cap is exactly there: the burst condition requires
`|B| >= 2^{-k_0+1}` and its Theorem 5.1 takes the finest bins to be of side
`(K log K / n)^{1/(2 beta + d)}`, while each bin of side `|B|` runs its SE for
`ell_B asymp |B|^{-2 beta}` rounds up to logarithms, so the total work at the finest level is
`2^{k_0 d} |B|^{-2 beta} asymp n`. A cap set anywhere short of that would leave the algorithm idle
at the end of the horizon, which no tuning would do. So the cap converts "for ever" into "until the
budget is exhausted", and the budget is `n`.

*Objection 2: the tie is at mean 1, so the rewards are deterministic and `G_C = 0` exactly; that is
a degenerate instance.* The adversary pointed out that my answer below, correct as far as it goes,
cuts against me rather than for me: perturbing the tie makes the reward clause *almost* inert rather
than exactly inert, so the failure survives for the same reason A0's does, and the perturbation
therefore does not rescue the instance as a witness for reward dependence. I keep the answer because
it is what makes the (R4) reading of the theorem robust, and it should be read that way.
Restating the objection and the answer: The determinism is a convenience, not the mechanism. Replace the two top
agents' delivered mean `1` by any common value `p in (0,1)`, keeping `M_2 = M_3 = 1` so that the
two-top hypothesis still holds and the deviation is still available. The two agents' exploration
empirical means are then averages of `q_l` i.i.d. Bernoulli(`p`) observations with the *same* mean,
so `G_C` is of order `sqrt(p(1-p)/q_l)`; with `q_l = q_0 4^l` and `theta_l = theta_0 2^{-l}` the
comparison `G_C <= theta_l` becomes `|N(0,1)|` of order `1 <= theta_0 sqrt(q_0) / sqrt(2 p(1-p))`,
which does not depend on the level. So a single constant `q_0`, chosen large enough given
`theta_0`, makes every leaf split with probability at least `1 - delta(q_0)` with
`delta(q_0) = exp(-Omega(q_0 theta_0^2))`, and the per-leaf failure probability decays in `l` like
`exp(-Omega(q_0 theta_0^2 4^l))` against `2^{l d_nu}` leaves, so a union bound over levels
`l >= 1` costs `O(delta(q_0))`. The conclusion becomes "gain at least `(1 - delta(q_0)) n/4 -
O(n^{1/3})`" instead of an exact identity, which is still `Theta(n)` once `delta(q_0) < 1/2`.
Taking `p = 0.7` also makes the benchmark loss worse, not better: the exploration average falls to
`(0.9 + 0.7 + 0.7 + 0)/4 = 0.575` against `b = 0.9`. What the mechanism genuinely needs is that the
two top agents have *equal* cell means, which is the hypothesis of `thm:contextual-public` itself,
not that their rewards be deterministic.

**Faithfulness to ABSE, with the correction applied.** The following observation is still correct
and still worth recording, but note what it does and does not establish after Section 4.8: it shows
that ABSE's own criterion also refines at every level on a tied instance, which is why ABSE would
also be unsafe here; it does **not** show that the refinement is caused by reward dependence, since
a rule with no reward clause does the same. ABSE eliminates arm `i` from bin `B` only when
`Ybar^(i) < Ybar^max - gamma U(tau, T)` with `U > 0`. Two arms with exactly equal means are
therefore never separated at any bin size, `|I_B| >= 2` holds at every bin, and ABSE bursts at every
level down to its depth cap `k_0`. So the mechanism of Theorem 5 is ABSE's own, not an artefact of
the witness rule; what protects ABSE in its own setting is the depth cap `k_0` together with the
inherited arm set `I_{B'} <- I_B`, which stops the eliminated arms from being resampled in every
child. Section 4.6 takes up the inheritance.

### 4.5 Lemma 6: the cell-epoch law is *not* what breaks

The scout's Section B.5.b classified robustness for reward-dependent splitting with fresh
statistics as INCOMPLETE, on the ground that "the epoch length is now a stopping time of the epoch's
own rewards ... Lemma B.1 fails (conditioning on labels now conditions on rewards), so 'conditional
on `V_C = s`, an `s`-round fixed-mean instance' is no longer available; a proof would have to go
through a virtual continuation of each epoch to its maximal length and charge the maximal length. I
have not written such a proof." The virtual continuation works, and it does not even need a maximal
length. The obstruction is elsewhere.

**Lemma 6.** Consider a *leaf-local tree rule*: the partition process is a dyadic tree; the root
exists from round 1; a leaf `C` created at round `tau_C` is replaced, at the round of its `rho_C`-th
visit, either by its `2^D` dyadic children with fresh state or by a frozen copy of itself that is
never replaced again, where `rho_C in {1,2,...} u {infinity}` is a stopping time of the leaf's own
data filtration (leaf time) and the freeze-or-split choice is measurable with respect to the leaf's
own data and coins at that time. Assume (R2) and (R3) and fixed maps. Put
`V_C := #{t in (tau_C, n] : X_t in C}`. Then, conditionally on `F_{tau_C}` and on the event that `C`
is created, there is a *virtual* execution of the leaf's rule on a `K`-armed fixed-mean Bernoulli
instance with means `(bar m_{i,C})_i`, of length `V_C`, such that

(a) the leaf's actual execution is the prefix of the virtual execution of length
`min(rho_C, V_C)`, and the leaf's actual selections and rewards are those of that prefix;

(b) `V_C` is a function of the post-`tau_C` contexts alone, hence independent of the virtual
execution's reward uniforms and coins;

(c) the virtual execution satisfies (i) to (iv) of Lemma 2 with `C` in place of `C(lambda)`.

Consequently, if the leaf's local rule has an anytime per-instance bound `E Reg_s <= f(s)` with
`Reg_s` nondecreasing in `s` (which is the case for every deficit functional the manuscript uses,
since each is a sum of nonnegative per-round terms), then

`E[ leaf C's benchmark deficit | F_{tau_C} ] <= E[ f(s_C) | F_{tau_C} ] + 2 L diam(C cap supp nu) E[s_C | F_{tau_C}]`,
where `s_C := min(rho_C, V_C)` is the leaf's actual epoch length, which may be replaced by `V_C`
when `rho_C` is a genuine stopping time of the leaf's rewards and one does not want to keep track of
it. The second term is the Lipschitz comparison `bar b_C <= bar m^*_C + 2 L diam(C cap supp nu)` of
the manuscript's appendix A.3, restricted to the occupied part of the cell as in Section 2.3.

*Proof.* `tau_C` is a stopping time of the filtration generated by `((X_t, U_t))_t` and the coins,
because the event `{tau_C <= t}` is determined by the rounds up to `t`. By the strong Markov
property for i.i.d. sequences, conditionally on `F_{tau_C}` the primitives
`((X_t, U_t))_{t > tau_C}` are i.i.d. with their original law and independent of `F_{tau_C}`. Let
`s_1 < s_2 < ...` be the rounds after `tau_C` with `X_s in C`; `C` is `F_{tau_C}`-measurable, so by
the standard thinning fact the sequence `(X_{s_r})_r` is i.i.d. `nu( . | C)` and is independent of
the index set `{s_r}` and hence of `V_C`, and `(U_{s_r})_r` and `xi_C` are independent of it and of
each other. Define the virtual execution by running `phi(C, . , xi_C)` on `(X_{s_r}, U_{s_r})_{r <= V_C}`,
as if the leaf never died; the induction of Lemma 2 applies verbatim and gives (c), and (b) is the
thinning fact. For (a): the actual and virtual processes are the *same* process for as long as the
leaf is alive, because the local rule is label-local and uses only the leaf's own past data and
coins, and the leaf is alive exactly until leaf time `min(rho_C, V_C)`; `rho_C` is a stopping time
of the leaf's own data, so the prefix is well defined. The consequence follows by conditioning on
`V_C` (legitimate by (b)) and by monotonicity of `Reg_s`. QED

Note that the virtual continuation beyond leaf time `s_C` uses rounds that in reality belong to the
leaf's descendants, so the virtual executions of different leaves share randomness and their lengths
`V_C` do not sum to `n`. Nothing below sums virtual deficits: the bound is applied to each leaf's
own prefix, and the prefixes occupy disjoint rounds.

Three remarks.

1. No cap on the epoch length is needed, and the stopping time `rho_C` may depend on the epoch's own
   rewards in any way. This covers ABSE's `tau_B >= ell_B` (whose `tau_B` counts successive
   elimination rounds and is therefore reward dependent) and RA-ETC with either decision schedule.
2. Applying the lemma recursively down the tree is legitimate, because the creation time of a child
   is the round of the parent's `rho`-th visit, again a stopping time.
3. `lem:region`, the identity `E T_j(C cap R) = nu(R|C) E T_j(C)`, also survives, because it is
   (iv) of Lemma 2 applied to the virtual execution and to the prefix, and the prefix length is a
   stopping time of data that are independent of the current visit's position inside `C`.

**Proposition 7 (the exact diagnosis).** Under the hypotheses of Lemma 6 with a decision time
`rho_C = D_{lev(C)}` that is a deterministic function of the level (which is the case for RA-ETC
with either decision schedule, for COAT, and for the static grid), the expected total benchmark
deficit is at most

`E[ sum over created leaves C of ( f_{lev(C)}(s_C) + 2 L diam(C cap supp nu) s_C ) ]`, where the
actual epoch lengths satisfy `sum_C s_C = n`,

and every quantity inside the expectation except `nu` and `L` is determined by the tree. Therefore
reward dependence can hurt in exactly two places:

(A) *the number of leaves per level.* If the decision time has no context-only lower bound, a leaf
may die at the end of its exploration phase, so the number of level-`(l+1)` leaves is bounded only
by `2^D n_l / (K q_l)` and the exploration term `sum_l K q_l e_l` can be as large as `n`. This is the
mechanism of Theorem 5, and it is exactly what the first clause of (R4) excludes. I wrote in the
first version that "the agents control it, because they control whether the top two separate", and
that sentence is not supported: on the only instance in this file where mechanism (A) fires the tie
is forced by the instance, the freeze branch is never taken, and a rule with no reward clause
exhibits the same failure (Section 4.8). Mechanism (A) is a schedule failure, available to
context-only rules; whether a unilateral deviation can trigger it is OPEN.

(B) *the level at which a leaf freezes.* A leaf frozen at level `l` pays
`2 L diam(C cap supp nu)` per visit for the rest of the run. Which leaves freeze at which level is
a reward event, so the agents control the effective mesh. This is the mechanism of Theorem 4, and it
is already fatal at honest play.

If the freeze-or-split choice and the decision time are both functions of the contexts alone, (A) is
bounded by `e_{l+1} <= 2^D n_l / N_l` and (B) does not arise, because the leaf's level is then
determined by its own visit count. That is COAT, and Section 5 carries out the resulting count.

**Corollary (characterization inside the RA-ETC family), corrected.** Consider RA-ETC rules with
`theta_l -> 0` **and a decision schedule satisfying `K q_l / D_l -> 0`**, that is with a context-only
floor that leaves each leaf a vanishing exploration fraction. Such a rule is safe in the sense of
Section 1.3 if and only if its freeze-or-split decision is almost surely a function of the contexts
alone. The floor hypothesis is not removable: without it the rule `D_l = K q_l`, which the Definition
of Section 3 explicitly permits, is unsafe even when its decision *is* almost surely a function of
the contexts alone, by Section 4.8. The "if" direction is Section 5 (always split up to a context-only
depth cap is COAT; always split up to a fixed level and then freeze is the static grid, which is
`thm:grid-etc`). The "only if" direction is Theorem 4 for the freezing branch and Theorem 5 for the
never-freezing branch of a rule with no context-only floor. I have not proved the "only if"
direction for an arbitrary reward-dependent decision rule outside this family; see Section 8.

### 4.6 Inheritance makes it worse, not better

ABSE controls (A) by passing the parent's surviving arm set to each child
(`I_{B'} <- I_B` in Policy 3), so an arm eliminated at a coarse scale is never resampled in any
descendant. Two things then go wrong in the manuscript's model.

*Inherited observations are biased in the child.* This is the scout's Section B.5.a, whose example
is complete and which I have checked: one cell `[0,1)`, one agent with map `m(x) = x`, two
observations at positions `X_1, X_2`, split at `1/2` if and only if `Y_1 = 1`, each observation
given to the child containing its position. Conditionally on the split having occurred and on
`X_1 in [0,1/2)`, the inherited observation has `Y_1 = 1`, that is conditional mean 1, while the
left child's cell mean is `E[m(X) | X in [0,1/2)] = 1/4`. So a split-conditioned child's inherited
data have the wrong mean. ABSE avoids this by resetting the averages and inheriting only the arm
set, so this particular objection does not apply to ABSE; it applies to any design that inherits
observations.

*Permanent elimination is a linear robustness failure.* **Instance W4**: `K = 3`, `d = 1`, `D = 3`,
`nu` the law of `(U,U,U)` with `U ~ Uniform[0,1)` (again a curve, so the tree reduces to the dyadic
tree in `u`). All three agents honest and at capacity: `mu_1 = M_1 = 0.5`, `mu_2 = M_2 = 0.55`,
`mu_3(x) = M_3(x) = (0.9 - 1.8 x)_+`, which is Lipschitz with `L = 1.8`. Then
`bar m_{3,root} = 0.225`, and `b(u) = max(0.55, (0.9 - 1.8u)_+)`. Any rule that eliminates an agent
from a cell when its empirical cell mean trails the leader by more than a window, and never
reinstates it in a descendant, eliminates agent 3 at the root with probability `1 - o(1)` as soon as
the root's exploration length grows (its root gap is `0.325`), and therefore never selects agent 3
anywhere. The benchmark deficit is then at least
`n int_0^{0.1944} (0.9 - 1.8u - 0.55) du = 0.034 n - o(n)`,
while Static Grid-ETC and COAT have `o(n)` on this instance. The cause is the same as in Theorem 4:
elimination at scale `|B|` is justified only if the delivered means vary by less than the window
inside `B`, which is a smoothness assumption about the arms.

So the two ways of paying for a reward-triggered refinement, re-exploring every child and inheriting
the parent's verdict, fail for the same reason in opposite directions. Note that both failures are
at honest play: they are statements about the platform, not only about incentives.

### 4.7 Exactly what the converse covers, and which rules escape it

This is the part of the file I most expect to be attacked, so I state the scope without hedging.

**What is defeated, and in what mode.**

| result | what it defeats | mode of failure | margin |
|:-|:-|:-|:-|
| Theorem 3 | the rule RA-ETC with `theta_l = 2^{-l}/8`, either decision schedule, on one instance | both: exact pathwise monotonicity fails, and so does expected monotonicity with any `o(n)` remainder, since the two expectations differ by `Theta(n)` | `n/2 - O(log n)` |
| Theorem 3' | a class: any dyadic rule with fresh label-local statistics that is reward decisive at the root and whose local rule commits to a cell-best agent | expected, hence also pathwise | `n/2 - o(n)` |
| Theorem 4, the headline witness | every RA-ETC threshold schedule with `theta_0 < 1/2`, and in outline every schedule with `theta_l -> 0`, for either decision schedule, with a fixed horizon-free `q_0` | expected benchmark deficit; also pathwise, since the deficit is a sum of nonnegative per-round terms whose conditional means are constant after the freeze | `(c^2/2) n - o(n)` for any `c in (0, 1/2 - theta_0)` |
| Theorem 5 | **nothing about reward dependence.** It defeats every rule whose leaves split at the end of their exploration phase, a class containing both RA-ETC with no floor and the context-only rule A0, so it separates rules satisfying (R4) from rules violating it, not reward-dependent from context-only ones | expected, and exactly, not asymptotically | deviation gain `n/4 - O(n^{1/3})`, benchmark loss `0.175 n - O(n^{1/3})` |
| Section 4.6 | any rule that inherits an ancestor's elimination verdict, ABSE included | expected benchmark deficit | `0.034 n - o(n)` |

The direction of the monotonicity failure is the one the axiom forbids: raising agent 1's map
*increases* agent 3's expected allocation. A failure in the other direction would be uninteresting.

**What is not defeated.** There is no theorem in this file of the form "every reward-dependent
partition rule is unsafe". Theorem 3' is the closest, and its hypotheses (reward decisiveness at the
root, commitment to a cell-best agent, and the arithmetic conditions on `v, v'`) are assumptions I
verify only for RA-ETC. Anyone who reads the converse as a general impossibility is over-reading it.

**Which natural rules escape, and what happens to them.**

1. *Independent platform randomness.* A partition that depends on the contexts and on platform coins
   drawn independently of everything else escapes the letter of (R1), which forbids coins, but is
   safe: fold the coins into the element `Z` of Section 1.1 and every proof in Section 2 goes
   through unchanged. (R1) should be read as forbidding dependence on rewards and selections, not as
   forbidding exogenous randomness.

2. *Accelerate-only rules, and this is the substantive escape.* Let the rule use rewards only to
   make a leaf split **earlier**, never later: fix two context-only schedules
   `K q_l <= N_l^min <= N_l^max` and let a level-`l` leaf split at the first of its own visits at or
   after `N_l^min` at which some reward event fires, and in any case at visit `N_l^max`. No leaf is
   ever frozen. Such a rule escapes Theorems 4 and 5 completely, and keeps robustness and sharp
   adaptivity at the COAT rate. The reason is Proposition 7 read backwards: the ceiling kills
   mechanism (B), because no leaf survives past `N_l^max` visits, so the mesh shrinks at a
   context-only rate and the bias term is `sum_l 2^{-l} n_l` with `n_l <= N_l^max e_l`; and the
   floor kills mechanism (A), because a leaf's exploration fraction is at most
   `K q_l / N_l^min` and the number of level-`(l+1)` leaves is at most `2^D n_l / N_l^min`, so
   Lemma 7 and Lemma 7' apply verbatim with `N_l^min` in (iii) and `N_l^max` in (ii). With the COAT
   schedule sandwich `N_l^min = N_l^max = K 8^l` this is COAT itself; with
   `N_l^min = K 8^l`, `N_l^max = 2 K 8^l` it is a genuinely reward-dependent rule that is
   nonetheless statistically safe. Classification: PROVED IN OUTLINE (the counting is Lemma 7 with
   two schedules; I did not rewrite it).

   Whether such a rule keeps monotonicity is **OPEN**, and my first version got the sign of the
   evidence wrong. Section 4.7.1 sets out what I claimed, why it fails, the argument that points the
   other way, the part of that argument I closed, and the part that is still open.

   This is the analogue, for this workstream, of the escape the separation worker recorded. It
   matters because it means the honest principle is **not** "the partition must be a function of the
   contexts alone" but the weaker and more accurate pair: *for robustness and sharp adaptivity it is
   enough that the split times be sandwiched between two context-only schedules and that no leaf be
   frozen on a reward event; for monotonicity nothing weaker than (R1) is known to suffice.*

3. *Rules whose split trigger no single agent can move.* If the split trigger is measurable with
   respect to a statistic that no unilateral deviation in `S_HDS` can change, the rule is
   context-only in effect and everything in Section 2 applies. I know of no natural rule of this
   kind: every leaf statistic used in the literature is a function of the delivered means, and in
   this model the delivered means are the agents' choice. I record this as an escape hatch that is
   empty rather than as one that is closed.

4. *A depth cap reached immediately.* A rule whose depth cap is `0` is a single cell and a rule whose
   cap is reached before any reward is seen is a static grid. The static grid is safe by
   `thm:grid-etc`. The reason is **not** that its reward dependence never fires, which was the reason
   I gave and which Section 4.8 shows is no reason at all, since A0's reward dependence never fires
   either and A0 is unsafe. The reason is that the static grid satisfies (R4): its exploration total
   is `K q_n J_n = o(n)` and its mesh is `sqrt(D) h_n -> 0`. A single cell is context only, satisfies
   neither clause of (R4), and is unsafe on any instance with a non-constant `b`.

#### 4.7.1 The accelerate-only question, restated after the adversary report

**What I claimed, and why it fails.** I sketched a monotonicity failure: "rescale `nu` into a single
level-`l` dyadic cube so that one leaf carries `Theta(n)` visits ... the timing difference
`N_l^max - N_l^min = Theta(n)`". The adversary showed the sketch is unavailable for the anytime
sandwich it was offered for, and it is right. With `N_l^max` a function of the level alone, a
level-`l` leaf carries at most `N_l^max = 2 K 8^l` visits, a constant that does not depend on `n`, so
the timing difference at a fixed level is `O(1)`. Rescaling `nu` into a level-`l*` cube does not help,
because the rule keeps splitting below `l*` and the rescaled mass is spread over the cube's
descendants exactly as it was spread over the original tree. Making `N_l^max = Theta(n)` at the
operative level needs a horizon-dependent schedule, and such a rule has `S = Theta(n)`, so its
Lipschitz bias is already linear and it is not one of the statistically safe rules whose
monotonicity was the question. (The adversary confirmed the mechanism is otherwise real: the
horizon-dependent rule with `N_0^min = n/4`, `N_0^max = 3n/4` on instance W1 splits the root at
`3n/4` under the base profile and at `n/4` under the raise, giving `E T_3` about `0.125 n` and
`0.375 n`, a violation of `0.25 n`. That rule is not robust on W1, so it settles nothing.) I withdraw
the sketch.

One arithmetic point that made me too confident, and which I now see cuts the other way: the total
timing slack summed over all levels *is* of order `n`, since `sum_l e_l (N_l^max - N_l^min)` is
comparable to `sum_l n_l = n`. So the slack is not small; what makes it harmless, if it is harmless,
is that the two executions' winners agree on all but `o(n)` of it.

**The argument that points the other way (the adversary's, Section A3.2, restated).** Call a rule
*mesh shrinking on an instance* if for every fixed `L` all but `o(n)` of the rounds are held by
leaves of level at least `L`. Every rule with `S = sum_l 2^{-l} n_l = o(n)` is mesh shrinking, since
`sum_{l < L} n_l <= 2^L S`; in particular COAT is, and so is every accelerate-only rule with the
sandwich. Then:

- exploration contributes `O(S) = o(n)` rounds in total, so it cannot carry a linear difference;
- an exploitation round goes to agent 3 exactly when agent 3 is its leaf's ETC winner, an event of
  conditional probability `pi_3(bar m_C, q_l)` given the leaf's cell means;
- along the dyadic filtration `bar m_{a, C_l(u)} -> m_a(u)` for `nu`-almost every `u` and every `a`,
  by martingale convergence, and `q_l -> infinity`.

At every `u` at which the pointwise argmax of `m(u)` is unique, the gap is eventually bounded below,
so `pi_3 -> 1{argmax = 3}` in both executions, and the raise replaces `m_1` by `M_1 >= m_1`, which
can only shrink the set where agent 3 is the argmax. So on the unique-argmax set the timing channel
is asymptotically invisible and monotonicity holds to `o(n)`.

**The gap I closed.** The adversary left the tie set `T := {u : the argmax of m(u) is not unique}`
as the gap, and checked two special cases by hand. On the part of `T` where the cell means of the
tied agents are *exactly* equal in every cell containing `u`, which is what happens when the tied
maps are equal on a whole neighbourhood in the tree, the limit of `pi_3` is the symmetric share
`s_3(v) := 1{v_3 = max_a v_a} / |argmax_a v_a|`, by exchangeability of the tied agents under the
uniform exploration permutations and the uniform priority. That function is **non-increasing in
`v_1`** pointwise: raising `v_1` either leaves the argmax set untouched, or adds agent 1 to it, which
strictly decreases `1/|argmax|`, or makes agent 1 the unique argmax, which sends `s_3` to zero.
Hence `E[s_3(m(u))]` cannot increase under the raise, and this part of `T` is harmless. This covers
both special cases the adversary checked and the general exact-tie case.

**The gap that remains, stated precisely.** Let `f := m_3 - m_2` on the part of `T` where agents 2
and 3 are the tied argmax. Martingale convergence gives `bar f_{C_l(u)} -> f(u) = 0` for a.e. such
`u`, but it does **not** forbid `sign(bar f_{C_l(u)})` from alternating in `l` infinitely often, and
the ETC winner at level `l` is determined by that sign whenever `|bar f_{C_l(u)}| >> q_l^{-1/2}`,
which with `q_l = 4^l` is `|bar f_{C_l(u)}| >> 2^{-l}`. So the open case is exactly:

> a set of positive `nu`-measure on which `|bar f_{C_l(u)}|` decays more slowly than `2^{-l}` while
> its sign alternates in `l`, and an accelerate-only rule whose reward trigger systematically places
> the raised execution on the levels where agent 3 wins and the base execution on the levels where
> it loses.

I do not know whether such an instance exists. Two remarks, one on each side. Against: the
alternation has to be sustained on a positive-mass set for all large `l`, and `bar f_{C_l}` is a
martingale converging to `0`, so the alternation must be produced by increments of size comparable
to the value, which is a strong self-similarity requirement; the adversary tried to build one and
failed for what it calls a structural reason. For: nothing in the martingale convergence theorem
rules it out, and a Haar-type construction with `bar f_{C_l(u)} = (-1)^l l 2^{-l}` along a nested
sequence satisfies both `bar f -> 0` and `|bar f| >> 2^{-l}`, so the obstruction is not measure
theoretic but combinatorial, namely whether the rule's trigger can be made to select the favourable
level at a constant fraction of rounds.

**Classification: OPEN**, with the balance of evidence now against my original belief. If the
argument is completed, the correct statement of the principle is weaker again: *(R1) is needed for
exact pathwise monotonicity and for nothing else; every property in the `o(n)` sense survives a
context-only sandwich, given (R4).* Exactness is not nothing, since it is what `thm:grid-etc`
advertises over `thm:grid-ucb-robust`, but it is a much smaller claim than "the partition must not
depend on the rewards", and the paper should not be written as if the larger claim were established.

**A second consequence I accept.** The adversary observes that Theorem 3's failure needs the base
execution to keep all `n` rounds at level 0, which is mechanism (B) of Proposition 7, the mechanism
Theorem 4 exploits, so the monotonicity converse may be a symptom of the robustness converse rather
than an independent result. I have not settled that either. It does not weaken Theorem 3, which is
proved, but it means the file has one independent converse with two visible symptoms, not two
converses, and that is the claim I would defend.

**Two sentences for the paper.** A partition may depend on the contexts and on the platform's own
coins, and its schedule must keep the total exploration sublinear and the mesh shrinking, which is
what the fixed grid does trivially and what the adaptive tree does by its counting argument. It must
not depend on the rewards through a decision that stops the refinement or retires an agent, because
that makes the effective mesh a quantity the agents choose, and it costs a linear amount at honest
play on an explicit instance. The first sentence cannot be dropped: a context-only rule with a bad
schedule is unsafe (Section 4.8).

### 4.8 The correction: a context-only rule that is not safe, and what follows

This section records the adversary's two P1 findings, my independent reproduction of both, and every
statement elsewhere in this file that they change.

**The rule A0.** Half-open dyadic cubes of `[0,1)^D`, root at level 0. Each leaf runs `ETC(q_l)` with
`q_l = q_0 4^l` on its own fresh statistics and its own coins. A leaf is replaced by its `2^D` dyadic
children at its `K q_l`-th visit, that is at the end of its exploration phase. Nothing is inherited,
including visit counts. A0 is COAT with the single schedule `N_l = K 8^l` replaced by `N_l = K q_l`,
and it contains no reward dependence of any kind.

A0 satisfies (R1), (R2) and (R3), by exactly the verification Section 5.1 gives for COAT:
`P_{t+1}` differs from `P_t` only when the label of round `t` has now been carried `K q_{lev}` times,
which is a function of the label sequence alone, so (R1) holds; statistics are label local and fresh,
so (R2) holds; the primitives are the model's, so (R3) holds. A0 violates (R4): every one of its
rounds is an exploration round, so `sum_l K q_l e_l = n`, not `o(n)`.

**A0 is not safe.** On instance W2 of Section 4.4, A0 gives every agent `n/K + O(n^{1/3})`
selections whatever it delivers, so agent 4 gains `n/4 - O(n^{1/3})` by deviating to the zero map at
a profile satisfying the two-top hypothesis of `thm:contextual-public`, and the platform receives
`0.725 n` against an honest benchmark of `0.9 n`. This is Theorem 5's own arithmetic, and
Theorem 5's proof applies to A0 verbatim, because the proof only uses that every leaf splits at the
end of its exploration phase.

**Reproduced independently.** The adversary built its own simulator, calibrated it against my W3
figures first (its 0.02083 and 0.01829 against my 0.02082 and 0.01838; its COAT 0.06054 and 0.01677
against my 0.06063 and 0.01676), and then ran A0 on W2. I then checked it in my own simulator by
setting `theta_0 = 10^9`, which deletes the freeze branch and turns RA-ETC into A0
(`check_adv.py`):

| `n` | RA-ETC gain / `n` | A0 gain / `n` | RA-ETC deficit / `n` | A0 deficit / `n` |
|:-|:-|:-|:-|:-|
| 12500  | 0.2499 | 0.2499 | 0.1749 | 0.1749 |
| 50000  | 0.2500 | 0.2500 | 0.1750 | 0.1750 |
| 200000 | 0.2500 | 0.2500 | 0.1750 | 0.1750 |
| 800000 | 0.2500 | 0.2500 | 0.1750 | 0.1750 |

Identical to four decimals, and the exploration fraction is `1.000` for both.

**Consequences, and where each is applied.**

1. *"Context-only partitions are safe" is false* under the Section 1.3 definition of safe, and A0 is
   the counterexample. Applied: Section 0 item 1 rewritten; Section 1.3 now carries (R4) as an
   explicit fourth requirement and says that (R1) to (R3) do not imply safety.
2. *Theorem 5 is not a witness for reward dependence.* Applied: Section 4.4 rewritten and the
   theorem restated for the class of rules that split at the end of the exploration phase, which
   contains both A0 and RA-ETC with no floor; its role is now to establish that (R4) is necessary.
3. *The Corollary of Section 4.5 was false in its "if" direction*, because the decision schedule
   `D_l = K q_l` that the Definition of RA-ETC explicitly permits gives a rule whose decision is
   almost surely a function of the contexts alone on W2 and which is not safe. Applied: the
   Corollary now carries the hypothesis `K q_l / D_l -> 0`.
4. *Proposition 7(A)'s sentence "and the agents control it, because they control whether the top two
   separate" is not exercised by any instance in this file.* Mechanism (A) is real as bookkeeping,
   but I have no instance in which reward dependence rather than the schedule triggers it. Producing
   one is OPEN: it needs a unilateral deviation that changes whether leaves die at the end of
   exploration, which needs the deviator to be one of the tied tops, and at `S^max` the tie is
   forced. The adversary tried and did not find one; so did I, after the report, and did not.
   Applied: Proposition 7(A) now carries this caveat, and Section 8 records it OPEN.
5. *Escape 4 of Section 4.7 gave the wrong reason.* "They escape because their reward dependence
   never fires" is not a reason, since A0's reward dependence never fires either. Applied: the
   reason is now that the particular rules named there (a single cell, the static grid) satisfy (R4).
6. *Section 6's recommendation 1 should not be followed as written.* Applied: it now names
   Theorem 4 and Theorem 3 as the instances to put in the paper, and warns that a referee who
   deletes the reward clause from Theorem 5's displayed rule gets the same `n/4`.

**What the correction does not touch.** No proof in this file is wrong. Lemmas 1, 2, 6, 7, 7', 8,
Corollary 3, Proposition 7 as bookkeeping, Theorems 3, 3', 4, D.1 to D.5, Sections 2.3, 2.4, 4.6 and
7 all stand, and the adversary checked most of them independently and found no error. What changed is
which of them the summary is allowed to lean on.

### 4.9 Theorem 4 promoted: the converse in the form that isolates the reward clause

Theorems 3 and 4 both compare RA-ETC against rules that differ from it in more than the reward
clause, because RA-ETC's schedules (`q_l = q_0 4^l`, `D_l = K q_l` or `N_l`) are not COAT's
(`q_l = 4^l`, `N_l = K 8^l`). A referee can therefore ask whether the schedules rather than the
sentence are doing the work. After Section 4.8 that question has to be answered, not waved at, and
the answer is to compare a rule with itself.

**The comparison.** Take any context-only rule that satisfies (R4), and add exactly one sentence:

> at the leaf's decision visit, freeze the leaf instead of splitting it if its top two exploration
> empirical means differ by more than `theta_l`.

Nothing else changes: same cells, same `q_l`, same `N_l`, same local rule, same coins. Theorem 4 says
the result loses `(c^2/2) n - o(n)` of the honest benchmark on instance W3, with every agent honest
and at capacity, while the rule without the sentence loses `o(n)` by Theorem D.1 or by
`thm:grid-etc`. That is the converse in its cleanest form: **one sentence, every schedule identical,
a linear loss at honest play with no deviation at all.**

**Numerical record.** Two versions of the comparison, both in
`<scratchpad>/round2/c4-safe-partitions/`.

(i) *COAT's own schedules* (`q_l = 4^l`, `N_l = K 8^l`), `theta_l = 2^{-l}/8`, `w3d.py`, 5 seeds,
deficit per round:

| `n` | COAT | COAT plus the sentence |
|:-|:-|:-|
| 200000 | 0.06076 (sd 0.001) | 0.02072 (sd 0.017) |
| 800000 | 0.01659 (sd 0.000) | 0.13952 (sd 0.174) |

The adversary's independent run of the same comparison gives 0.06069 against 0.02038 at `n = 2e5`,
0.01672 against 0.02366 at `n = 8e5`, and 0.03274 against 0.02375 at `n = 3.2e6`. Both runs show the
same thing: COAT's figure is the sawtooth of Section 5.6 and is on its way to zero, the freeze
variant's does not decay. The large seed-to-seed spread is the signature of the mechanism and not
noise to be averaged away: with `q_0 = 1` the root freezes on a single observation per agent and
commits the whole run to whichever agent that observation favoured. Note that Theorem 4's proof does
not apply verbatim to this variant, since the proof wants `q_0` large enough for the Hoeffding event;
this run is a confirmation of the mechanism, not of the theorem.

(ii) *The theorem's own schedules* (`q_l = 2000 * 4^l`, `N_l = 8000 * 8^l`), `w3e.py`, 5 seeds:

| `n` | rule X, context only | X plus the sentence | Static Grid-ETC |
|:-|:-|:-|:-|
| 200000 | 0.09561 (se 0.00008) | 0.02067 (se 0.00004) | 0.00406 |
| 800000 | 0.06662 (se 0.00002) | 0.01833 (se 0.00003) | 0.00238 |
| 3200000 | 0.07272 (se 0.00003) | 0.01776 (se 0.00001) | 0.00109 |

(Slurm job 64574905; larger horizons were still running when this was written.)

**Read this table honestly, because it does not show what a reader might want it to show.** The
freeze variant converges to the predicted constant `c^2/2 = 0.017578` (0.02067, 0.01833, 0.01776)
and does not decay. Rule X does not decay monotonically either: 0.09561, 0.06662, 0.07272 is the
same sawtooth as COAT's, since each newly opened level pays its exploration at once, and its
envelope is what the `O(n^{3/4})` bound controls. At these horizons rule X is still *above* the
freeze variant, because its own exploration constant is large, and the two curves have not crossed
at any horizon I can simulate in this implementation; extrapolating the envelope puts the crossing
near `n = 10^8`. So the separation that is visible in simulation is against Static Grid-ETC, a
context-only rule satisfying (R4) with a good constant, which is a factor of 16 below the freeze
variant at `n = 3.2e6` and falling cleanly. **The separation between X and X plus the sentence is
proved, not measured**, and I say so rather than implying a crossing that is not there. What the
table does establish numerically is the half that matters most and that no proof replaces: adding the
sentence turns a quantity that is bounded by `o(n)` into one that has visibly converged to a positive
constant.

## 5. COAT: Section D of the scout file

### 5.0 What COAT buys and what it costs, stated plainly

**What it buys, item by item.**

1. *The horizon.* COAT contains no `n`, so every continuous contextual result becomes anytime. This
   is real but it is **not** a reason to prefer COAT, because DE-Grid (Section 2.4) buys the same
   thing in two sentences and keeps the manuscript's algorithm unchanged.
2. *Adaptivity to the geometry of the context law.* The exponent becomes
   `(d_nu+2)/(d_nu+3)` in place of `(D+2)/(D+3)`, where `d_nu` is the dyadic covering exponent of
   `supp(nu)`. This is the only thing COAT buys over DE-Grid.
3. *No new knowledge is required.* The algorithm does not use `n`, `L`, `nu`, `A` or `d_nu`, and it
   is never worse in the exponent, since `d_nu <= D` with `A = 1` always. So the adaptivity is free
   in the sense that the platform does not have to bet on it.
4. *It stays in the safe class.* It keeps exact pathwise monotonicity, expected FATA and the public
   equilibrium (Theorems D.2 to D.4), which is the whole point: adaptivity without leaving (R1).

**What it costs, item by item.**

1. *The gain is conditional on `d_nu < D`, a property of the instance that the platform cannot
   verify.* This is the honest headline and it should be in the paper in these words. In the
   default reading of the manuscript's model, where the `K` agents' contexts are independent and
   each has a density on `[0,1]^d`, the profile law has a density on `[0,1]^D` and `d_nu = D`
   exactly, so COAT buys nothing at all. The gain appears when the profile arrivals are degenerate:
   correlated contexts, a shared latent driver such as a common time-of-day feature, a low-rank or
   manifold-supported profile law, or discrete or mixed contexts. At the other extreme `d_nu = 0`
   (finitely many profiles) COAT gives `n^{2/3}`, which interpolates towards but does not reach the
   manuscript's own finite-context rate `O(sqrt(K Q n log(en)))`, because COAT does not know `Q`.
   The algorithm adapts automatically; the *claim* is conditional, and the condition is unverifiable
   from data the platform holds.
2. *Constants.* `C_0 = 2^{D+4}(2^{D+2} + 2 L sqrt(D) + c_1 K)` is exponential in `D` and worse than
   the static grid's. Measured: on a two-dimensional instance (Section 5.6, `w3c.py`) COAT loses to
   Static Grid-ETC at every horizon tested, by factors of 11, 8 and 24. The crossover is far out.
3. *The deficit is not monotone in `n`.* Each newly opened level pays its whole exploration cost at
   once, so the bound is attained in a sawtooth; a plot of deficit against `n` will not look like a
   clean power law at any horizon a referee can simulate (Section 5.6 shows it jumping from 36118 at
   `n = 4e6` to 252811 at `n = 8e6`).
4. *Page budget.* It replaces the static grid theorem rather than adding to it, and the covering
   assumption plus the algorithm plus the statement is about two thirds of a two-column page.

**Bottom line.** COAT is an exponent result, conditional on a property of the context law that the
platform does not know and cannot check, never worse in the exponent and usually worse in constants.
If it goes in the paper, it should be stated as "the same guarantees, with the ambient dimension `D`
replaced by the covering exponent of the support, and no new inputs", with the sentence "when the
profile law has a density on the cube, `d_nu = D` and nothing changes" said out loud.

### 5.1 The algorithm and the standing assumption

**COAT-ETC.** Parameters, for level `l >= 0`: split threshold `N_l := K 8^l` and exploration size
`q_l := 4^l`, so `K q_l <= N_l` with equality only at `l = 0`. No `n`, no `L`, no `nu`, no `d_nu`.

```
State: a set LEAVES of half-open dyadic cubes (initially {[0,1)^D} at level 0); for each leaf, a
   since-creation visit count V (initially 0) and a fresh ETC(q_l) state, created lazily.
Round t:
   observe X_t; let C in LEAVES be the leaf containing X_t and l its level;  V_C <- V_C + 1;
   select I_t = the output of C's ETC(q_l) on C's own history and coins; observe Y_t; update C;
   if V_C = N_l:  remove C from LEAVES and add its 2^D dyadic children, each with V = 0 and a
                  fresh ETC(q_{l+1}) state.
```

`ETC(q)` is the manuscript's cell rule: `q` independent uniform permutations of `[K]` as exploration
blocks (`K q` visits, last observed block possibly truncated), then commitment to the largest
exploration empirical mean with ties broken by an independent uniform priority permutation drawn
once for the leaf, exploitation rewards ignored.

`P_{t+1}` differs from `P_t` only when the label of round `t` has now been carried `N_{lev}` times,
which is a function of the label sequence; so (R1) holds, and (R2) and (R3) hold by construction.
Nothing is inherited, including visit counts. Hence Lemmas 1 and 2 and Corollary 3 apply.

**Standing assumption (dyadic covering).** There are `A >= 1` and `d_nu in [0, D]` with
`N_nu(2^{-l}) := #{level-l dyadic cubes C : nu(C) > 0} <= A 2^{l d_nu}` for every `l >= 0`. This is
always true with `d_nu = D` and `A = 1`. The algorithm does not know `A` or `d_nu`; they appear only
in the bound.

### 5.2 Lemma 7: the counting argument

Let `e_l` be the number of level-`l` leaf epochs visited at least once during the run and `n_l` the
number of rounds whose leaf is at level `l`.

**Lemma 7.** Pathwise, for every `n`: (i) `sum_l n_l = n`; (ii) `n_l <= N_l e_l = K 8^l e_l`;
(iii) `e_0 = 1` and `e_{l+1} <= 2^D n_l / N_l`; (iv) `e_l <= N_nu(2^{-l}) <= A 2^{l d_nu}`.

*Proof.* (i) Every round has exactly one leaf. (ii) A level-`l` leaf epoch has at most `N_l` visits
by construction, and the visit sets of distinct epochs are disjoint. (iii) A level-`l` leaf produces
children only after exactly `N_l` of its own visits, and the visit sets of distinct level-`l` leaves
are disjoint, so at most `n_l / N_l` level-`l` leaves split, each producing `2^D` children. (iv) A
given level-`l` dyadic cube can be a leaf at most once in the whole run, since it is created only
when its unique parent splits, which happens at most once; and a visited cell has positive mass
almost surely. QED

**Lemma 7'.** Put `S := sum_{l >= 0} 2^{-l} n_l`. Then pathwise
`S <= 2^{4 + d_nu} (K A)^{1/(d_nu+3)} n^{(d_nu+2)/(d_nu+3)}` whenever `n >= K A`, and `S <= n`
always.

*Proof.* Let `L` be the smallest nonnegative integer with `2^{L(3+d_nu)} >= n/(KA)`. By (ii) and
(iv), `2^{-l} n_l <= 2^{-l} K 8^l A 2^{l d_nu} = K A 2^{l(2+d_nu)}`, so
`sum_{l <= L} 2^{-l} n_l <= K A sum_{l<=L} 2^{l(2+d_nu)} <= 2 K A 2^{L(2+d_nu)}`. By minimality
`2^{L(3+d_nu)} < 2^{3+d_nu} n/(KA)`, hence
`2 K A 2^{L(2+d_nu)} = 2 K A (2^{L(3+d_nu)})^{(2+d_nu)/(3+d_nu)} < 2^{3+d_nu} (KA)^{1/(3+d_nu)} n^{(2+d_nu)/(3+d_nu)}`.
For the tail, `sum_{l>L} 2^{-l} n_l <= 2^{-(L+1)} n <= (1/2) (KA/n)^{1/(3+d_nu)} n` by the defining
inequality for `L`. Adding gives the claim. QED

### 5.3 Theorem D.1: robustness and contextual sharp adaptivity

**Theorem D.1.** Under COAT-ETC, for every `n >= 1`, uniformly over `S_HDS` and its independent
ex ante mixtures,

`E sum_{t<=n} [ b(X_t) - m_{I_t,n}(X_t) ] <= K + C_0 (K A)^{1/(d_nu+3)} n^{(d_nu+2)/(d_nu+3)}`,
where `C_0 := 2^{D+4} (2^{D+2} + 2 L sqrt(D) + c_1 K)` and `c_1 = 2 e^{-1/2}`.

For every measurable `R` with `nu(partial R) = 0`, contextual sharp adaptivity holds with remainder
that bound plus a boundary term which is `o(n)`.

*Proof.* Condition throughout on `Lambda_{1:n}`, the whole label sequence. This is the conditioning
of Lemma 1 and Lemma 2, and it is legitimate here precisely because COAT satisfies (R1): the label
sequence is a function of the contexts alone, so conditioning on it fixes the entire tree, the set of
leaf epochs, each epoch's level `l`, and each epoch's visit count `s`, while leaving the conditional
law of every epoch's rewards equal to that of a fixed-mean instance. In particular `e_l`, `n_l` and
`S` of Lemma 7 become deterministic under the conditioning, and the two random objects that a
reward-adaptive rule would have made reward dependent, namely which cells are leaves and for how
long, are here frozen by the conditioning at no cost. Fix one such leaf epoch, of a leaf `C` at
level `l` with `s` visits. By Corollary 3 the epoch is a fixed-mean instance with means
`bar m_{i,C}`, so the manuscript's
Grid-ETC per-cell accounting applies with `q_l` in place of `q_n`: at most `min(s, K q_l)`
exploration visits, each charged at most 1; and on each of the `(s - K q_l)_+` exploitation visits
the expected deficit relative to `b` is at most `2 L diam(C cap supp nu) + c_1 K q_l^{-1/2}` by the
Lipschitz comparison of appendix A.3 (restricted to the occupied part of the cell, Section 2.3, and
`diam(C cap supp nu) <= sqrt(D) 2^{-l}`) together with `lem:etc-tail`. With `q_l = 4^l`,
`c_1 K q_l^{-1/2} = c_1 K 2^{-l}`. The exploitation bound is applied `(s - K q_l)_+` times with `s`
fixed by the conditioning, which is what makes "expected per-visit deficit times number of
exploitation visits" a product rather than a covariance: the number of visits is
`Lambda_{1:n}`-measurable and the per-visit conditional deficit is bounded by a constant. Writing
`beta := 2 L sqrt(D) + c_1 K`, summing over the epochs of the conditioned tree and then averaging
over `Lambda_{1:n}`,

`E sum_t [b - m_{I_t}] <= E[ sum_l ( K q_l e_l + beta 2^{-l} n_l ) ]`.

For `l >= 1`, Lemma 7(iii) gives `K q_l e_l <= K 4^l 2^D n_{l-1} / (K 8^{l-1}) = 2^{D+3} 2^{-l} n_{l-1}`,
and `K q_0 e_0 = K`. Hence
`sum_l K q_l e_l <= K + 2^{D+3} sum_{m >= 0} 2^{-(m+1)} n_m = K + 2^{D+2} S`, and the total is at
most `K + (2^{D+2} + beta) S`. Lemma 7' and `d_nu <= D` give the display.

For a region `R`, the same computation applies to the leaves contained in `R`; a leaf at level `l`
meeting both `R` and `R^c` lies in `(partial R)^{sqrt(D) 2^{-l}}`, and such visits are charged one
unit each. For any `L'`, the boundary charge is at most
`sum_{l <= L'} N_l e_l + E[ #{t <= n : X_t in (partial R)^{sqrt(D) 2^{-L'}}} ]
 <= 2 K A 2^{L'(3 + d_nu)} + n nu((partial R)^{sqrt(D) 2^{-L'}})`
by Lemma 7(ii), (iv). Choose `L' = L'(n) -> infinity` with `2^{L'(3+D)} = o(n)`; the first term is
`o(n)` and the second is `o(n)` by continuity from above, since `partial R` is closed and
`nu(partial R) = 0`. Converting the deficit into effort by `c_i = b - mu_i - (b - m_i)` exactly as
in the manuscript gives contextual sharp adaptivity. QED

Two remarks. With `d_nu = D` and `A = 1` the exponent is `(D+2)/(D+3)`, the same as Static
Grid-ETC, so nothing is lost in the worst case. Nothing in the proof uses `n`, `L`, `nu`, `A` or
`d_nu` inside the algorithm; they appear only in the bound.

### 5.4 Theorems D.2 to D.5

**Theorem D.2 (exact pathwise contextual monotonicity).** For every `n`, every measurable `R`, every
map profile in `S_HDS`, every agent `i`, and every pointwise raise of `m_{i,n}` (in particular the
raise to `M_i`), COAT-ETC satisfies `T_j(R;n) <= T_j(R;n)` in the raised versus base execution,
pathwise, for every `j != i`, under the natural common-uniform coupling, with no regularity and no
boundary condition.

*Proof.* Couple the two executions with identical contexts, identical exploration permutations and
priority permutations per leaf, identical reward uniforms for agents other than `i`, and identical
reward uniforms on the common exploration pulls of agent `i`. Because COAT satisfies (R1), the
partition process is a measurable function of the contexts alone, so the two executions have
literally the same tree: the same leaves, the same creation and split times, and therefore the same
exploration rounds, and each agent's exploration pulls in each leaf occur at the same rounds and
hence at the same contexts. The manuscript's Grid-ETC monotonicity argument now applies inside every
leaf verbatim: feasibility gives `1{U <= M_i(X)} >= 1{U <= m_{i,n}(X)}` on each common exploration
pull, exploration choices are identical, so only `i`'s exploration empirical mean can rise; with the
leaf's priority permutation fixed, raising one score can leave the winner unchanged or replace it by
`i`, and it cannot make `j != i` newly win. So `j`'s exploration counts are equal in the two
executions and each of `j`'s exploitation indicators weakly decreases. Summing over leaves and over
the rounds with `X_t in R` gives the claim pathwise. QED

This is exactly where (R1) is indispensable, and exactly where Theorem 3 shows a reward-dependent
rule fails: there the two executions have different trees, so there is nothing to couple.

**Lemma 8 (mesh-uniform cell-average convergence).** Let `nu` be Borel on `[0,1]^D` and `f` bounded
Borel. For a finite or countable Borel partition `P`, let `f^{(P)}` be `E[f | C]` on each
positive-mass `C in P` and `0` on null cells, and put
`rho_f(r) := sup { ||f^{(P)} - f||_{L^1(nu)} : P a Borel partition with mesh(P) <= r }`. Then
`rho_f(r) -> 0` as `r -> 0`.

*Proof.* This is the manuscript's `lem:cell-average-l1` with the observation that its proof depends
on `P` only through `mesh(P)`. Fix `eps > 0` and a continuous `g` with `||f - g||_{L^1(nu)} <= eps`.
Conditional expectation is an `L^1` contraction, so `||f^{(P)} - g^{(P)}||_1 <= eps`; and for `X` in
a positive-mass cell `C`, `|g^{(P)}(X) - g(X)| <= sup_{Y in C} |g(Y) - g(X)| <= omega_g(mesh P)` with
`omega_g` the modulus of continuity of `g`, uniform by compactness. Hence
`||f^{(P)} - f||_1 <= 2 eps + omega_g(r)` for every `P` with `mesh(P) <= r`, so
`limsup_{r -> 0} rho_f(r) <= 2 eps`. QED

**Theorem D.3 (expected contextual FATA).** Let `G := G_{ij}(R)` and suppose `m_{i,n} = m_{j,n} =
M_*` on `G` and `nu(partial G) = 0`. Then `|E T_i(G;n) - E T_j(G;n)| = o(n)`, with the same
boundary remainder as in Theorem D.1.

*Proof.* Condition on `Lambda_{1:n}`. By (R1) this conditioning is on a function of the contexts
alone, so it fixes the tree, which cells are leaves, which leaves are contained in `G`, and every
leaf's visit count, and by Lemma 2 it leaves each epoch's conditional reward law equal to that of a
fixed-mean instance, with distinct epochs conditionally independent by Lemma 2(ii).

Fix a leaf `C` contained in `G` and let `sigma` be the transposition of the labels `i` and `j`. The
hypothesis gives `bar m_{i,C} = bar m_{j,C}`. Consider the map `Psi` on the leaf's private
randomness that replaces each of its `q_l` exploration permutations `pi` by `sigma . pi`, replaces
its priority permutation `rho` by `sigma . rho`, and exchanges the reward seeds of `i` and `j`.
`Psi` is an involution; it is measure preserving, because the exploration and priority permutations
are uniform on the symmetric group and left composition with a fixed `sigma` preserves the uniform
law. (My first version justified the reward half of `Psi` by exchanging per-agent seed streams. The
realization fixed in Section 1.1 has one uniform `U_t` per round, not a stream per agent, so there is
nothing to exchange, as the adversary pointed out in X7. The conclusion is unaffected and in fact
easier: FATA's hypothesis is `m_{i,n} = m_{j,n} = M_*` on `G` *pointwise*, so on a leaf contained in
`G` the two agents deliver the same mean at the same context, and swapping them in the permutations
leaves every realized reward literally unchanged, so `Psi` need not touch the seeds at all.) The leaf's rule commutes with `Psi`: the
number of exploration visits `K q_l` and the position at which the last observed block is truncated
depend on the leaf's visit count only, which `Psi` does not touch; the commitment is the argmax of
the exploration empirical means with ties broken by the priority; and `Psi` permutes the empirical
means and the priority by the same `sigma`. Hence the execution `Psi(omega)` is the execution
`omega` with the roles of `i` and `j` exchanged, so `T_i(C)(Psi(omega)) = T_j(C)(omega)`, and
measure preservation gives `E[T_i(C) | Lambda_{1:n}] = E[T_j(C) | Lambda_{1:n}]`. The conditioning
does not obstruct this, which is the whole point: the conditioning event is determined by the
contexts, and `Psi` acts only on the leaf's coins and seeds, which are independent of the contexts
by (R3), so `Psi` is still measure preserving after conditioning.

Summing over the leaves contained in `G` and averaging over `Lambda_{1:n}` gives equality of the two
expected counts on that part. Leaves contained in `G^c` contribute no shared-top counts. Every
remaining leaf crosses `partial G`, and its visits are charged one unit each, giving the boundary
bound of Theorem D.1 with `partial G` in place of `partial R`. QED

Here too (R1) is what makes the conditioning harmless. Under a reward-dependent tree the event
"`C` is a leaf" is not `Psi`-invariant: `Psi` changes the rewards in the ancestors of `C`, where `i`
and `j` need not have equal cell means, and so it changes which cells exist. That is exactly the
step that has no substitute, and it is why Theorem 3 can move a count by `Theta(n)`.

**Theorem D.4 (continuous public restricted equilibrium).** Suppose two agents attain the largest
capacity at `nu`-almost every profile and `M_*` is public. Then under COAT-ETC, for every `n`, every
agent `i` and every deviation `m' in S_HDS` including independent ex ante mixtures,

`u_i(n; m', S^max_{-i}) - u_i(n; S^max) <= K + (2^{D+2} + c_1) S_max + E[ sum_C N_C eta_{i,C} ]`,
where `S_max := 2^{4+d_nu} (KA)^{1/(d_nu+3)} n^{(d_nu+2)/(d_nu+3)}` is the pathwise bound of
Lemma 7',

which is `o(n)` uniformly over deviations; and if every `M_j` is `L`-Lipschitz then
`eta_{i,C} <= L sqrt(d) 2^{-lev(C)}` and the whole bound is
`K + (2^{D+2} + c_1 + L sqrt(d)) S_max = O((KA)^{1/(d_nu+3)} n^{(d_nu+2)/(d_nu+3)})`. Here
`N_C` is the leaf's exploitation visit count and
`eta_{i,C} := (bar M_{i,C} - max_{j != i} bar M_{j,C})_+`.

*Proof.* Fix a deterministic deviation; independent mixtures follow by conditioning because the
bound does not depend on the map. By (R1) both executions have the same tree and explore the same
rounds, so their exploration utilities differ by at most one per exploration pull, hence by at most
`sum_l K q_l e_l <= K + 2^{D+2} S` in total (Theorem D.1's computation). Fix a positive-mass leaf
`C` at level `l` and put `a_C := E[1 + mu_i - M_i | C] >= 0` and `delta_C := E[M_i - m' | C] in [0,1]`.
The coupling of Theorem D.2 gives `p'_{i,C} <= p_{i,C}` for the commitment probabilities, and it is
available here only because (R1) makes the tree identical under `S^max` and under the deviation; a
reward-adaptive rule would have two different trees and no such inequality. Conditionally on
`Lambda_{1:n}` the leaf's exploitation visit count `N_C = (min(N_l, V_C) - K q_l)_+` is a constant,
while the commitment event is a function of the leaf's rewards, so the two factorize and the leaf's
exploitation gain is at most
`N_C ( p'_{i,C}(a_C + delta_C) - p_{i,C} a_C ) <= N_C p'_{i,C} delta_C`; averaging over
`Lambda_{1:n}` restores the expectation. This is the same conditioning device as in Theorem D.1 and
it is the reason no covariance term appears.
Let `Delta' := max_{j != i} bar M_{j,C} - (bar M_{i,C} - delta_C)`. If `Delta' > 0`, committing
requires beating a best rival whose exploration mean averages `q_l` observations of mean
`bar M_{j,C}` by Lemma 2, so `lem:etc-tail` gives `p'_{i,C} Delta' <= c_1 q_l^{-1/2} = c_1 2^{-l}`
and hence `p'_{i,C} delta_C <= c_1 2^{-l} + eta_{i,C}`; if `Delta' <= 0` then
`delta_C <= eta_{i,C}` and the same bound holds. Summing, using `sum over level-l leaves of N_C <= n_l`,
gives `c_1 S + E[sum_C N_C eta_{i,C}]`.

It remains to show `E[sum_C N_C eta_{i,C}] = o(n)`. Write `lev_t` for the level of the leaf holding
round `t`. For any `L'`,
`sum_C N_C eta_{i,C} <= #{t : lev_t <= L'} + sum_t eta_{i, C_t} 1{lev_t > L'}`.
By Lemma 7(ii) and (iv), `#{t : lev_t <= L'} <= 2 K A 2^{L'(3 + d_nu)}` pathwise. For the second
term, condition on `P_t`, which is a function of `X_1, ..., X_{t-1}` and hence independent of `X_t`,
so that `E[eta_{i,C_t} 1{lev_t > L'} | P_t] = sum over leaves C of P_t with level > L' of nu(C) eta_{i,C}`.
Let `P_t'` be `P_t` with every leaf of level at most `L'` replaced by its level-`(L'+1)` dyadic
descendants; then `mesh(P_t') <= sqrt(D) 2^{-L'-1}`, and since `eta >= 0` the displayed sum is at
most `sum over all cells C of P_t' of nu(C) eta_{i,C}`. The
map `u -> (u_i - max_{j != i} u_j)_+` changes by at most `sum_a |u_a - u'_a|`, so by Lemma 8 applied
to each `M_a`,
`sum_{C in P_t'} nu(C) eta_{i,C} <= E[(M_i(x_i) - max_{j != i} M_j(x_j))_+] + sum_a rho_{M_a}(sqrt(D) 2^{-L'-1})`,
and the last expectation is zero because two agents attain the largest capacity almost everywhere.
Hence `E[sum_t eta_{i,C_t} 1{lev_t > L'}] <= n sum_a rho_{M_a}(sqrt(D) 2^{-L'-1})`. Choosing
`L' = L'(n) -> infinity` with `2^{L'(3+D)} = o(n)` makes both terms `o(n)`. Under `L`-Lipschitz
capacities, all `X, X'` in a level-`l` cube satisfy `|x_j - x'_j| <= sqrt(d) 2^{-l}`, so
`M_j(x_j) <= bar M_{j,C} + L sqrt(d) 2^{-l}` on `C`; almost every `X in C` has
`M_i(x_i) <= max_{j != i} M_j(x_j)`, and integrating gives `eta_{i,C} <= L sqrt(d) 2^{-l}`, whence
`E[sum_C N_C eta_{i,C}] <= L sqrt(d) S`. QED

**Theorem D.5 (anytime).** COAT-ETC uses neither `n`, nor `L`, nor `nu`. Consequently the bounds of
Theorems D.1, D.3 and D.4 hold at every horizon `n` simultaneously with the same constants, for a
single execution of the algorithm, and Theorem D.2 holds pathwise at every `n`. This is not claimed
as a high-probability statement uniform in `n`; it is the statement that for each `n` the expected
bound holds for the same algorithm.

### 5.5 The UCB version and what is not claimed

**COAT-UCB.** `N_l := 4^l`; the leaf rule is the manuscript's cell-local symmetric UCB1 on the
leaf's own local time. The gap-free bound `eq:gap-free-ucb` gives, for an `s`-round fixed-mean
instance, `E sum (m^* - m_{I_r}) <= C sqrt(K s log(es)) + C K`. Repeating Section 5.2 with
`e_{l+1} <= 2^D n_l / 4^l`:

- shallow levels `l <= L`: `e_l <= A 2^{l d_nu}` gives
  `sum_{l<=L} [ C sqrt(K 4^l log(e n)) + C K ] A 2^{l d_nu} <= 2 C A sqrt(K log(en)) 2^{L(1+d_nu)} + 2 C K A 2^{L d_nu}`,
  and the bias term `2 L sqrt(D) sum_{l<=L} 2^{-l} n_l <= 2 L sqrt(D) A sum_{l<=L} 2^{l(1+d_nu)} <= 4 L sqrt(D) A 2^{L(1+d_nu)}`;
- deep levels `l > L`: `C sqrt(K N_l log(en)) e_l <= 2^{D+2} C sqrt(K log(en)) 2^{-l} n_{l-1}`, so
  the tail is at most `2^{D+1} C sqrt(K log(en)) 2^{-L} n`, and the bias tail is
  `2 L sqrt(D) 2^{-L} n`.

Balancing at `2^{L(2+d_nu)} = n/A` gives
`E sum_t [b(X_t) - m_{I_t,n}(X_t)] = O( sqrt(K log(en)) A^{1/(d_nu+2)} n^{(d_nu+1)/(d_nu+2)} )`
with a constant depending on `D` and `L`. Robustness and sharp adaptivity only, as for Grid-UCB1 in
the contract. If the platform is willing to use `n`, taking `N_l = 4^l ceil(log(en))` improves the
log factor to `(log n)^{1/(d_nu+2)}` and, with the manuscript's known-horizon index
`hat m_a + sqrt(4 log n / T_a)`, the exact-monotonicity argument of `thm:grid-ucb-robust` also goes
through leaf by leaf (the index is a function of the agent's own local count and own tape, the tree
is the same in both executions by (R1), and `lem:region` holds per leaf by Lemma 2(iv)); but then
the rule is no longer anytime.

**What is not claimed.** No optimality. The ledger's Section 6.1 records that Rigollet and Zeevi's
Theorem 4.1 gives a lower bound with exponent `(d+1)/(d+2)` in the *per-agent* dimension `d` for the
honest special case, and that whether `Omega(n^{(D+1)/(D+2)})` holds against `S_HDS` is OPEN. COAT's
exponent `(d_nu+2)/(d_nu+3)` is not claimed minimax optimal in any regime, and the `+3` rather than
`+2` is the ETC price the manuscript already pays for pathwise monotonicity.

### 5.6 Numerical record for COAT

All runs in `<scratchpad>/round2/c4-safe-partitions/`; Slurm job 64568006, partition `cpu`.

*Counting.* On the segment instance (`d_nu = 1`, `A = 1`, `K = 4`) the measured number of leaf
epochs and the measured exploration total match Lemma 7 exactly: 63 epochs is
`sum_{l=0}^{5} 2^l`, and 149796 exploration rounds is `K sum_{l=0}^{5} 4^l 2^l = 4 * 37449`. At the
next level, 127 epochs and 1198372 exploration rounds, again exact.

*Rate.* `rate.py`, `K = 4`, `D = 4`, four honest agents with Lipschitz intrinsic means on the curve
`{(u,u,u,u)}`, 3 seeds. Deficit at `n = 5e5, 1e6, 2e6, 4e6, 8e6, 1.6e7, 3.2e7`:
`32608, 32415, 32732, 36118, 252811, ..., 261769`. The ratio deficit / `n^{3/4}` stays in
`[0.19, 1.73]` over that range, so the `O(n^{3/4})` bound of Theorem D.1 (with `d_nu = 1`) is
respected; the sawtooth is the exploration cost of each newly opened level, exactly as Lemma 7
predicts, and it makes a fitted exponent meaningless at these horizons. **The rate is proved, not
measured.**

*Adaptivity.* `rate2.py`, the same curve but with the platform's ambient dimension `D = 8` (so
Static Grid-ETC must use `h_n = n^{-1/11}`), 3 seeds. Deficit:

| `n` | COAT | Static Grid-ETC |
|:-|:-|:-|
| 250000  | 4622  | 20630  |
| 1000000 | 32728 | 38921  |
| 4000000 | 37880 | 319686 |

COAT's deficit per round is 0.0185, 0.0327, 0.0095, which is the sawtooth described in the previous
paragraph and not a falling sequence (adversary X8), but it is an order of magnitude below the
grid's at the largest horizon and its trend is downward, while the grid's (0.0825, 0.0389, 0.0799)
is flat, because at these horizons the `D`-tuned grid is stuck at four occupied cells and is
bias-bound. This is the adaptivity claim in the one regime where it bites.

*Honest caveat.* On a low-dimensional instance where the `D`-tuned grid is already fine enough,
COAT is worse at moderate `n`: in `w3c.py` (`D = 2`) COAT's deficit per round is 0.061, 0.017,
0.033 at `n = 2e5, 8e5, 3.2e6` against the grid's 0.0056, 0.0022, 0.0014. COAT's constant
`C_0 = 2^{D+4}(2^{D+2} + 2 L sqrt D + c_1 K)` is large, and the gain is asymptotic and appears only
when `d_nu` is genuinely smaller than `D`.

## 6. Comparison and what I would put in the paper

| rule | partition depends on | sharp adaptivity | monotonicity | FATA | robustness | public equilibrium | anytime | adapts to `d_nu` |
|:-|:-|:-|:-|:-|:-|:-|:-|:-|
| Static Grid-ETC (manuscript) | nothing | yes | exact pathwise | expected | `O(n^{(D+2)/(D+3)})` | yes | no | no |
| DE-Grid (Section 2.4) | nothing | yes | exact pathwise | expected | same rate | yes | yes | no |
| Sample-split k-d tree | contexts (burn-in) | yes on the play phase | exact pathwise on the play phase | no diameter control | no diameter control | not available | no | dominated |
| COAT-ETC (Section 5) | contexts | yes | exact pathwise | expected | `O((KA)^{1/(d_nu+3)} n^{(d_nu+2)/(d_nu+3)})` | yes | yes | yes |
| A0, context only, splits at the end of exploration (Section 4.8) | nothing | no | not examined | not examined | **fails by `Theta(n)`** (Theorem 5) | **fails by `Theta(n)`** (Theorem 5) | yes | n.a. |
| RA-ETC with a context-only floor | contexts and rewards | no (Theorem 4) | **fails by `Theta(n)`** (Theorem 3) | not examined | **fails by `Theta(n)`** (Theorem 4) | not examined | n.a. | n.a. |
| RA-ETC with no floor | contexts and rewards | no | **fails by `Theta(n)`** | not examined | **fails by `Theta(n)`** (Theorem 4); also Theorem 5, but that failure is shared with A0 | **fails by `Theta(n)`**, shared with A0 | n.a. | n.a. |
| ABSE-style with inherited arm sets | contexts and rewards | no | not examined | not examined | **fails by `Theta(n)`** (Section 4.6) | not examined | n.a. | n.a. |

Recommendation, in the order I would spend page budget.

1. **The principle and the converse, three sentences plus one instance.** This is the highest value
   per line in the whole file, because it gives the fixed grid a reason rather than leaving it as
   the obvious baseline, and because the converse now has a witness rather than an announcement.
   **The instance to use is W3 (Theorem 4), not W2 (Theorem 5).** My first version recommended W2 and
   that recommendation was wrong: a referee who deletes the reward clause from the displayed rule
   gets the same `n/4`, because on W2 the clause is almost surely inert (Section 4.8). W3 is the
   instance where deleting the clause changes the answer, it needs no deviation at all (every agent
   honest and at capacity), and its arithmetic is exact: two agents, `mu_1(x_1) = 1 - x_1`,
   `mu_2 = c`, loss `c^2 n / 2`. Theorem 3's W1, stated on the diagonal, is the companion instance
   for monotonicity. What the sentences should say is in Section 4.7's "Two sentences for the paper",
   and they must include the schedule clause, because context-only geometry alone is not enough.
2. **The occupied-cell sentence** (Section 2.3). Already in the manuscript after
   `thm:grid-ucb-robust`; it costs nothing and it is what makes the `d_nu` discussion meaningful.
3. **The doubling remark** (Section 2.4), two sentences, removes the known horizon.
4. **COAT**, if about two thirds of a two-column page can be spared. It replaces rather than adds
   to the static grid theorem, and Section 5.6's caveat should be stated honestly: the adaptive
   exponent is asymptotic and the constant is worse than the grid's when `d_nu = D`.

I would not state the general converse (Theorem 3') in the paper; its hypotheses take more space
than the instance.

Two things the paper must not overclaim, both from Section 4.7 and Section 9.2. First, the converse
is about a family of rules that contains the defining mechanism of the published reward-adaptive
schemes, not about those schemes run verbatim; the sentence to write is "a partition may depend on
the contexts and on the platform's own coins, and must not depend on the rewards through a decision
that stops the refinement, freezes a cell, or retires an agent", not "reward-adaptive partitions are
impossible". Second, if a later draft ever restricts `S_HDS` to smooth delivered maps with a known
constant, Theorems 3 and 4 no longer apply and only Theorem 5's tied-tops mechanism survives; the
converse and that modelling choice have to be kept consistent.

## 7. The two assigned citations, verified from primary sources

Both checks were done on 18 September 2026. In each case I downloaded the full text and quoted from
the raw HTML rather than from a summary; the local copies are
`<scratchpad>/round2/c4-safe-partitions/abse.html`, `zoom.html`, `ucbogram.html`.

### 7.1 Perchet and Rigollet, ABSE

- arXiv:1110.6084, "The multi-armed bandit problem with covariates", Vianney Perchet and Philippe
  Rigollet. v1 27 October 2011, v2 8 June 2012, v3 24 May 2013.
  `https://arxiv.org/abs/1110.6084`, checked 18 September 2026.
- Published as The Annals of Statistics 41(2), 693 to 721, April 2013, DOI 10.1214/13-AOS1101.
  `https://projecteuclid.org/journals/annals-of-statistics/volume-41/issue-2/The-multi-armed-bandit-problem-with-covariates/10.1214/13-AOS1101.full`,
  checked 18 September 2026.
- Full text of v3 read at `https://ar5iv.labs.arxiv.org/html/1110.6084`, downloaded 18 September
  2026.

Verbatim from Policy 3 (ABSE), the burst step:

> `if tau_B >= ell_B and |B| >= 2^{-k_0+1} and |I_B| >= 2` /conditions to burst(B)/ `then for
> B' in burst(B) do I_{B'} <- I_B` /assign remaining arms as initial arms/ `Initialize se policy
> pi_hat_{B'} with T = n |B'|^d, gamma = 2 and arms I = I_{B'}. N_{B'} <- 0.`

Verbatim from Policy 1 (successive elimination), the elimination step, with
`U(tau, T) = 2 sqrt(2 logbar(T/tau)/tau)`:

> `if Ybar^{(i)} >= Ybar^max - gamma U(tau,T) then` ... Exploration ... `else S <- S \ {i}.`
> Elimination

Verbatim from the paragraph that explains why this is sound:

> "the parameters of the se policy `pi_hat_B` run at the birth of bin `B` are chosen exactly such
> that arms `i` with average gap `|fbar^*_B - fbar^{(i)}_B| >= C |B|^beta` are eliminated by the end
> of the `ell_B` rounds with high probability. The smoothness condition ensures that these
> eliminated arms satisfy `f^*(x) > f^{(i)}(x)` for all `x in B` so that such arms are uniformly
> suboptimal on bin `B`. Among the kept arms, none is uniformly better than another, so bin `B` is
> burst and the process is repeated on the children of `B`."

Assumptions: each reward function is `(beta, L)`-Holder and a margin condition holds with parameter
`alpha`; regret `C n (K log K / n)^{beta(alpha+1)/(2beta+d)}` for `alpha < infinity` and
`C K log n` for `alpha = infinity` (Theorem 5.1).

**How it differs from a context-only partition.** Three ways, each decisive. (1) The burst condition
contains `|I_B| >= 2`, a reward event: whether a bin is refined depends on whether elimination left
two arms. (2) `tau_B` is the SE round counter, which advances only over the surviving set, so the
burst *time* is reward dependent as well. (3) Children inherit the parent's surviving arm set, so
an agent's data in a child are not fresh in the sense of (R2) and an elimination is permanent for
all descendants. So ABSE violates (R1) and, through (3), also (R2). Its soundness rests on the
Holder assumption about the reward functions with a known constant, which in the manuscript's model
is an assumption about what the agents choose to deliver and is therefore not available; that is
the content of Theorem 4 and Section 4.6.

**FINDING (P1, citation description).** `audit/round2/B/MATH_CANDIDATE_LEDGER.md` line 121 says
"Rigollet and Zeevi's UCBogram and Perchet and Rigollet's ABSE are static partitions of the
covariate space for non-strategic arms". This is wrong for ABSE, whose partition is adaptive by
construction (the A in ABSE is "adaptively binned") and, worse for the purposes of this section,
*reward* adaptive. If that sentence were carried into the paper it would be a wrong description of
prior art and it would also give away the novelty claim, since ABSE would then look like a
context-only adaptive partition, which is exactly what it is not. The corrected sentence is: ABSE is
a reward-adaptive partition and is therefore outside the safe class, together with contextual
zooming.

I also checked the UCBogram half of that sentence, which is correct: Rigollet and Zeevi, arXiv
1003.1630, "Nonparametric Bandits with Covariates", submitted 8 March 2010,
`https://arxiv.org/abs/1003.1630`, full text at `https://ar5iv.labs.arxiv.org/html/1003.1630`,
checked 18 September 2026. Section 3.1 defines "the regular partition of `X`", the `M^d` hypercubes
`B_k`, and Theorem 3.1 fixes `M = floor((n/log n)^{1/(2 beta + d)})`: a static partition chosen from
the horizon alone. Two incidental facts from that paper are directly relevant here: it removes the
known horizon by "the so-called doubling argument ... which consists of resetting the game at times
`2^k`", which is exactly DE-Grid of Section 2.4; and it notes that the UCBogram "requires the
operator to pull each arm at least once in each bin and therefore to incur a regret of at least
order `M^d`", which is the manuscript's exploration term `K q_n J_n` and the reason the
occupied-cell accounting of Section 2.3 is worth one sentence.

### 7.2 Slivkins, contextual zooming

- arXiv:0907.3986, "Contextual Bandits with Similarity Information", Aleksandrs Slivkins. v1 23 July
  2009, v5 20 May 2014. `https://arxiv.org/abs/0907.3986`, checked 18 September 2026. The arXiv
  page and the paper's own acknowledgement say it is the full version of a COLT 2011 conference
  paper.
- Published as Journal of Machine Learning Research 15, 2533 to 2568, 2014.
  `https://www.jmlr.org/papers/v15/slivkins14a.html`, checked 18 September 2026.
- Full text read at `https://ar5iv.labs.arxiv.org/html/0907.3986`, downloaded 18 September 2026.

Verbatim, the two rules (Section 4, and Algorithm 4.2), with
`conf_t(B) = 4 sqrt(log T / (1 + n_t(B)))` where `n_t(B)` is the number of times `B` has been
selected before round `t`, and `I^pre_t(B) = nu_t(B) + r(B) + conf_t(B)`:

> "selection rule. Select a relevant ball `B` with the maximal index (break ties arbitrarily).
> Select an arbitrary arm `y` such that `(x_t, y) in dom_t(B)`."
>
> "activation rule. Suppose the selection rule selects a relevant ball `B` such that
> `conf_t(B) <= r(B)` after this round. Then, letting `y` be the arm selected in this round, a ball
> with center `(x_t, y)` and radius `(1/2) r(B)` is activated."

and the paper's own description of what it does:

> "The algorithm adaptively maintains a partition of the similarity space, 'zooming in' on both the
> 'popular' regions on the context space and the high-payoff regions of the arms space."

**How it differs from a context-only partition.** The active balls live in the joint context-arm
space; a new ball is centred at `(x_t, y)` where `y` is the arm the index rule selected, and the
activation fires when `conf_t(B) <= r(B)`, that is when the ball has been selected often enough,
which again is a decision of the index rule. Both the centres and the activation times are
functions of the observed payoffs, so the induced partition of the context space is reward adaptive
and (R1) fails. In addition the index takes a minimum over all active balls
(`I_t(B) = r(B) + min_{B'} (...)`), so a ball's decision uses data from other balls and (R2) fails
too. This is the precise sense in which the manuscript's claim to novelty here is correct:
contextual zooming zooms towards high payoff, and in a strategic model the payoff is the agents'
choice, so the zooming target is the agents' choice.

## 8. Classification of every statement in this file

| statement | classification | evidence |
|:-|:-|:-|
| Lemma 1, Lemma 2, Corollary 3 (Section 2.1, 2.2) | PROVED | scout's proofs, transcribed and checked line by line against `appendix_contextual.tex`; CORRECTION 1 to the phrasing of Lemma 2(i) |
| Occupied-cell accounting (Section 2.3) | PROVED | the manuscript's own proof with each sum restricted to visited cells |
| DE-Grid (Section 2.4) | PROVED modulo the manuscript's theorems as black boxes | per-epoch application plus a Cesaro argument |
| Theorem 3, linear monotonicity failure | PROVED, and NUMERICALLY CONFIRMED, independently reproduced by the adversary within a standard error | Hoeffding proof; `w1b.py` on the diagonal, 6 seeds, `E T_3` moves from 2000.0 to 91138.5 at `n = 2e5` |
| Whether Theorem 3 is an independent converse or a symptom of Theorem 4's mechanism | OPEN | the adversary's Section A3.2 argues it is a symptom; I have not settled it |
| Theorem 3', the same for a class of rules | PROVED UNDER STATED HYPOTHESES | the hypotheses (reward decisiveness at the root, commitment to the cell best) are assumptions, not verified for any named algorithm other than RA-ETC |
| Theorem 4, linear robustness failure at honest play | PROVED for schedules with `theta_0 < 1/2`, for every `c in (0, 1/2 - theta_0)`, and with a fixed `q_0` (horizon free); PROVED IN OUTLINE for `theta_0 >= 1/2` with `theta_l -> 0`; NUMERICALLY CONFIRMED and independently reproduced | `w3c.py`: measured deficit per round 0.0208, 0.0184, 0.0178 against the predicted `c^2/2 = 0.017578` |
| Theorem 5, linear deviation gain and linear robustness loss | PROVED (exact arithmetic); NUMERICALLY CONFIRMED; **but not a witness for reward dependence**, since its instance never takes the freeze branch and a rule satisfying (R1) to (R3) attains the same two constants (Section 4.8, and `check_adv.py` reproduces it in my own simulator). Its role is now to show that (R4) is necessary | `w2b.py`, `check_adv.py` |
| (R1) to (R3) imply safety in the sense of Section 1.3 | **FALSE**, withdrawn; the counterexample is A0 | Section 4.8 |
| (R1) to (R4) for COAT and for the static grid | PROVED | Section 5, and `thm:grid-etc` |
| Theorem 4 promoted to the headline witness, in the one-sentence-added form | PROVED for the theorem's own schedules; the COAT-schedule variant is a confirmation of the mechanism, not of the theorem (its `q_0 = 1` is outside the proof's Hoeffding regime) | Section 4.9, `w3d.py`, `w3e.py`, and the adversary's independent run |
| Whether a unilateral deviation can trigger mechanism (A) of Proposition 7 | OPEN | no instance in this file does; the adversary tried and failed, and so did I |
| Lemma 6, the cell-epoch law survives reward-dependent splitting | PROVED | strong Markov plus the thinning fact plus the induction of Lemma 2; this reverses the scout's B.5.b guess |
| Proposition 7, the diagnosis | PROVED | bookkeeping on top of Lemma 6 |
| Corollary, characterization inside the RA-ETC family | PROVED for the two branches named | the general "only if" for arbitrary reward-dependent rules is OPEN |
| Section 4.6, inherited observations are biased | PROVED | the scout's example, checked; it does not apply to ABSE, which resets averages |
| Section 4.6, permanent elimination costs a linear amount (instance W4) | PROVED UNDER STATED HYPOTHESES | the hypotheses are that an eliminated agent is never reinstated in a descendant and that elimination at the root happens with probability `1 - o(1)`; NOT simulated |
| Lemma 7, Lemma 7' (counting) | PROVED; NUMERICALLY CONFIRMED exactly | epoch counts 63 and 127 and exploration totals 149796 and 1198372 match the closed forms exactly |
| Theorem D.1, COAT rate `O((KA)^{1/(d_nu+3)} n^{(d_nu+2)/(d_nu+3)})` | PROVED | the rate is proved, not measured; the measured deficit stays inside `[0.19, 1.73] n^{3/4}` over `n` from `5e5` to `3.2e7` |
| Lemma 8, mesh-uniform cell-average convergence | PROVED | the manuscript's `lem:cell-average-l1` proof depends on the partition only through its mesh |
| Theorem D.2, exact pathwise monotonicity of COAT | PROVED | identical tree in both executions by (R1), then the manuscript's coupling leaf by leaf |
| Theorem D.3, expected FATA of COAT | PROVED | label symmetry inside a leaf, conditioning only on context-only quantities |
| Theorem D.4, public restricted equilibrium of COAT | PROVED | the `eta` term needs Lemma 8 and the conditioning on `P_t`; this is the step named in Section 9 |
| Theorem D.5, anytime | PROVED as stated (per-horizon expectations, not a uniform-in-`n` high-probability statement) | the algorithm contains no `n` |
| Section 5.5, COAT-UCB rate `O(sqrt(K log(en)) A^{1/(d_nu+2)} n^{(d_nu+1)/(d_nu+2)})` | PROVED IN OUTLINE | the balancing is written out; constants not chased |
| Section 7, both citations | VERIFIED from primary sources with URL and date | full texts downloaded and quoted from raw HTML |
| Whether every reward-dependent rule is unsafe | OPEN | Theorem 3' needs a non-degeneracy hypothesis |
| Theorem 3(b), the horizon-free form of the monotonicity failure | PROVED | a single fixed `q_0` gives margin `n/4 - K q_1 - N_0` at every `n` |
| Theorem 5 under a finite depth cap | PROVED UNDER A DESIGN CONVENTION | linear if and only if the cap is at or beyond the budget-determined depth, which is where ABSE sets it (Section 4.4, Objection 1) |
| Theorem 5 with a non-deterministic tie (`p in (0,1)` instead of `1`) | PROVED with a `1 - delta(q_0)` qualifier | Section 4.4, Objection 2 |
| Accelerate-only rules keep robustness and sharp adaptivity | PROVED IN OUTLINE | Section 4.7 item 2, Lemma 7 with two schedules |
| Accelerate-only rules lose monotonicity | OPEN, and the balance of evidence is now against it; my sketch is withdrawn because its mechanism is unavailable for the anytime sandwich | Section 4.7.1, with the adversary's martingale argument, the tie-set case I closed, and the sign-alternation case that remains |
| The converse under a smoothness-restricted `S_HDS` with known constant | FAILS except for Theorem 5 | Section 9.2.1, stated against myself |
| FATA and sharp adaptivity for RA-ETC | NOT EXAMINED | I did not attempt to break or prove them |
| Optimality of `(d_nu+2)/(d_nu+3)` | OPEN | the ledger's Section 6.1 already records what is and is not known |

## 9. Findings, the least secure step, and what I did not do

### 9.1 Findings

**F1 (P1, canonical file).** `sections/contextual_samf_algorithm.tex` line 23: "Cells are
initialized lazily, so every count of cells above may be replaced by the number of cells that carry
positive mass, **and the rates improve automatically when the context law concentrates on a
lower-dimensional set**." The first half is correct (Section 2.3). The second half is false as a
statement about rates. In `E_n = L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 min{J_n, n}` at
`h_n = (log(en)/n)^{1/(D+2)}` the first and second terms are both of order
`n^{(D+1)/(D+2)} (log n)^{1/(D+2)}`. Replacing `J_n` by `N_nu(h_n) <= A h_n^{-d_nu}` shrinks the
second and third terms to `n^{1/2 + d_nu/(2(D+2))}` and `A (n/log en)^{d_nu/(D+2)}` but leaves the
first untouched, so the order of `E_n` is unchanged: the bound improves, the rate does not, because
`h_n` is tuned to `D` and not to `d_nu`. The same holds for Grid-ETC. Smallest defensible repair, one
clause: "... may be replaced by the number of cells that carry positive mass, which shrinks the
exploration and initialization terms when the context law concentrates on a lower-dimensional set,
though not the exponent, since `h_n` is tuned to `D`." Downstream: this is the sentence that would
otherwise make COAT look redundant; with the repair it becomes the motivation for it.

**F2 (P1, wrong description of prior art).** `audit/round2/B/MATH_CANDIDATE_LEDGER.md` line 121
calls ABSE a static partition. It is adaptive and reward adaptive (Section 7.1, verbatim Policy 3).
If carried into the paper this would be a wrong citation description and would blunt the novelty
claim. The UCBogram half of the same sentence is correct and I verified it too.

**F3 (P2, closes an announced but undelivered claim).** The scout's Section B.5.c records
"pathwise monotonicity is false, by a linear margin ... (Section E.3, three agents, `D = 1`, an
'ambiguous cell' split rule)" and Section E.3 is not on disk. Theorem 3 supplies an instance and a
proof, with three agents and a reward-adaptive split rule; the margin is `n/2 - O(log n)`. The
claim is confirmed.

**F4 (P2, strengthens the converse beyond what was claimed, as corrected).** The scout claimed only
that monotonicity fails. One further failure at a linear margin is proved here and was not recorded:
robustness fails at honest play for any threshold schedule with `theta_0 < 1/2` (Theorem 4). It is
the more important of the two for the paper, because it is about the platform rather than about
incentives, because it needs no deviation, and because it identifies the real cause: a reward-adaptive
refinement imports a smoothness assumption about the arms, and in a strategic model the arms choose
whether it holds. The third failure I claimed, the `n/4` deviation of Theorem 5, is **withdrawn as a
converse**: its instance does not exercise the reward clause and a context-only rule attains the same
constants (Section 4.8). What it does establish is that the safe class needs a schedule condition,
which is now (R4).

**F4' (P1, self-reported, from `ADVERSARY.md` X1 and X2).** Two claims in the first version of this
file were broader than their proofs. "Context-only partitions are safe" is false under my own
Section 1.3 definition, with counterexample A0; and Theorem 5 was presented as a witness for reward
dependence when its instance never takes the freeze branch. Both are accepted, both are reproduced in
my own simulator, and both are repaired in Section 4.8. I record them at P1 against myself because a
reader who found either independently would rightly distrust the surrounding material. Neither
touches a proof.

**F5 (P2, corrects an INCOMPLETE to a positive result).** The scout's Section B.5.b and the ledger
line 117 classify "robustness for reward-dependent splitting with fresh statistics" as INCOMPLETE
and attribute the obstruction to the epoch length being a stopping time. Lemma 6 shows the
cell-epoch law survives, with no cap on the epoch length and with an arbitrary reward-dependent
stopping rule. The obstruction is the aggregation and the coupling, not the statistics. This matters
for the paper's wording: the reason to insist on context-only partitions is incentive-geometric, not
statistical.

**F6 (P2, supplies Section D).** Theorems D.1 to D.5 with proofs, and the counting argument
(Lemma 7, Lemma 7') that was the missing piece. The announced rate `n^{(d_nu+2)/(d_nu+3)}` is
correct, with the explicit constant `2^{D+4}(2^{D+2} + 2 L sqrt(D) + c_1 K) (KA)^{1/(d_nu+3)}`.

**F7 (P3, honesty about COAT).** COAT's constant is worse than the static grid's when `d_nu = D`,
and its deficit is a sawtooth in `n` because each newly opened level costs `K sum_{l} q_l e_l` at
once. On a two-dimensional instance it loses to the grid at every horizon I tested. The paper should
claim the exponent, not a practical improvement, and should say where the gain appears (Section 5.6,
the `D = 8` table).

**F8 (P3, phrasing).** The scout's Lemma B.2(i) says "against `K` independent Bernoulli reward
streams". The potential rewards of different agents at one visit share the context and are not
independent; what the proof gives, and all that is used, is the conditional law of the selected
reward. The manuscript is careful about this in two places; the scout's phrasing should be aligned.

Nothing in this file contradicts any theorem of the manuscript. The manuscript uses a static grid,
which is in the safe class, and its contextual theorems are untouched. The material is additive,
except for F1, which is a one-clause repair.

### 9.2 The step I consider least secure, and how it would be broken

I was warned that in this project every worker that named its own weakest step named the wrong one,
and that the adversary which followed broke a **hypothesis** rather than a proof step. So I looked
for the fragile hypothesis first, and I am naming one, not a proof line. My earlier draft of this
section named the `eta` term of Theorem D.4; I re-checked that step and now believe it is secure
(the reasons are in 9.2.3 below), and it is not what I would attack.

#### 9.2.0 What the adversary actually found, and what it says about this section

I named a hypothesis rather than a proof step, and the hypothesis I named is real and the adversary
confirmed it (its Section A4). But it did not find the two P1 defects that way, and neither did I:
both were **claims whose scope exceeded their proofs**, not hypotheses and not proof steps. I had
even written the sentence that refutes one of them (Corollary 3: "what does **not** carry over
automatically is the aggregation over cell epochs") and still wrote a heading that contradicted it,
and I had written in Theorem 5's own proof that `G_C = 0` with probability one and still called it a
witness for a mechanism that fires only when `G_C` matters.

So the lesson for anyone auditing this file next is: the summaries are the attack surface, not the
lemmas. The concrete test that would have caught both defects in five minutes is one I should have
run and did not: **delete the reward clause from the witness rule and rerun the instance.** If the
numbers do not move, the instance is not a witness for reward dependence. I have now run that test on
every witness in this file. W3 (Theorem 4) passes it, W1 (Theorem 3) passes it, W2 (Theorem 5) fails
it. Section 4.9 is built around that test.

One consequence for the item below: after the demotion of Theorem 5, the case analysis under a
smoothness-restricted class gets worse, not better. I had written "only Theorem 5 survives"; since
Theorem 5 does not distinguish reward-dependent from context-only rules, the correct statement is
that **no** witness in this file survives that amendment.

#### 9.2.1 The single least secure item

**The converse rests on the hypothesis that the platform has no known modulus of continuity for the
*delivered* reward maps, and that none need exist.** Everything negative in Section 4 except
Theorem 5 is an exploitation of that hypothesis, and the hypothesis is a modelling choice of the
manuscript, not a theorem.

Why it is the weak point. A reward-adaptive refinement stops refining when it judges a cell
"decided". That judgement is sound if and only if the threshold dominates the variation of the
delivered means inside the cell. Perchet and Rigollet say so themselves in the passage quoted in
Section 7.1: separation at scale `|B|^beta` implies uniform dominance *because of* the smoothness
condition. In the manuscript's model the delivered map is `m_{i,n} : X -> [0, M_i(x_i)]`, assumed
only measurable (contract Section 5), the platform's parameters are `L`-free (contract Section 4),
and the manuscript's own monotonicity theorem is advertised as needing "no regularity at all". So
the hypothesis is genuinely the manuscript's. But it is exactly the assumption a referee, or an
adversary, is most likely to attack, and the attack is short:

> Suppose the model is amended so that every map in `S_HDS` is `L'`-Lipschitz with `L'` known to the
> platform, on the ground that an agent cannot vary its effort arbitrarily fast across contexts.
> Then set `theta_l := 2 L' sqrt(D) 2^{-l} + (noise term)`. Freezing now implies uniform dominance
> inside the cell, so a frozen cell commits to a pointwise-best agent, and raising agent 1's map can
> only take regions away from other agents, never hand them one.

Under that amendment: **Theorem 3 dies**, because its instance uses delivered maps that jump at
`u = 1/2` (`m_2` and `m_3`), which is what lets a cell-best agent fail to be pointwise best.
**Theorem 4 dies**, because its instance has `L = 1` and the amended threshold would be
`theta_0 >= 2 sqrt(2) > 1/2`, outside the range the theorem needs; the amended rule would keep
splitting the root and would freeze only at a level where the threshold is genuinely below the
local variation, which is the correct behaviour. **Section 4.6 dies** for the same reason.
**Theorem 5 survives**, because its instance's delivered maps are constants, hence Lipschitz with
every constant, and its mechanism is that the two top agents have exactly equal cell means at every
scale, so no threshold of any size separates them and the rule refines until the budget is gone.

So the honest scope of the converse, corrected after `ADVERSARY.md` A4:

- Against the manuscript's actual class `S_HDS`, the converse stands, carried by Theorem 4, with
  Theorem 3 as the monotonicity symptom (and possibly not an independent one, Section 4.7.1).
- Against a smoothness-restricted class with a *known* constant, **nothing** in Section 4 separates
  reward-dependent from context-only partitions. Theorem 5 survives the amendment, because its maps
  are constants and `G_C = 0` at every scale, but by Section 4.8 it does not distinguish the two
  classes, so its survival is worth nothing here. The adversary also gives a sharper reason why
  Theorem 3 dies under the amendment: raising agent 1 does not change `m_2` or `m_3`, so if the base
  execution freezes a cell on agent 2 then agent 2 pointwise dominates agent 3 there and hence in
  every descendant, so the induced split cannot hand agent 3 a child; the mechanism, not merely the
  instance, is unavailable.
- Against a smoothness-restricted class with an *unknown* constant, I believe Theorems 3 and 4 can
  be rebuilt by scaling the instance's Lipschitz constant above whatever the rule's threshold
  schedule implicitly assumes (that is the same rescaling device used for Theorem 4's general
  schedule), but I have not written it and I do not claim it.

What would have to be true for the converse to fail: the paper would have to restrict `S_HDS` to a
smoothness class **and** give the platform the constant. Restricting without giving the constant is
not enough, and giving the constant while leaving `S_HDS` unrestricted is not enough either. If the
paper ever adds such a restriction for another reason, this whole section needs revisiting, and the
sentence in Section 0 about the principle would have to be weakened to Theorem 5's mechanism alone.

#### 9.2.2 The steps I would attack next, in order

1. *Whether Theorem 3 is an independent converse at all.* The adversary's Section A3.2 argues that
   Theorem 3's failure requires the base execution to keep all `n` rounds at level 0, which is
   mechanism (B) of Proposition 7, the mechanism Theorem 4 exploits, so the monotonicity converse may
   be a symptom rather than a second result. If that is right, the file has one converse, not two,
   and the paper should say so. I have not settled it. This is now the largest open question about
   what is actually proved here.
2. *Theorem 3'.* Its hypotheses (reward decisiveness at the root, commitment to a cell-best agent,
   `V/2 < v_3 < V`, `2 v'_1 - v_1 <= 1`) are chosen so that the construction closes. I have verified
   them for RA-ETC only. Anyone wanting a general impossibility should treat Theorem 3' as a
   template, not as a theorem about all rules.
3. *The accelerate-only escape.* My sketch that such rules lose monotonicity is withdrawn
   (Section 4.7.1); the adversary's martingale argument points the other way, I closed its tie-set
   gap in the exactly-tied case, and a sign-alternation case remains open. If the argument is
   completed, (R1) is needed only for exact pathwise monotonicity, and the paper's principle has to
   be stated as the sandwich condition plus (R4) rather than as context-only. This remains the most
   consequential open item for what the paper should say.
4. *Theorem 4 against a variance-adaptive threshold.* The adversary names this as the first place it
   would look next and says it did not examine it. A rule whose `theta_l` is set from the leaf's own
   empirical variance or by an empirical-Bernstein bound is still reward dependent, so (R1) still
   fails and Theorem 3's coupling is still unavailable, but whether instance W3 still defeats it is
   not something I checked.

#### 9.2.3 Why I no longer name the `eta` term of Theorem D.4

On re-examination each link is short and checkable. `P_t` is the partition at the start of round `t`
and under (R1) is a function of `X_1, ..., X_{t-1}`, so it is independent of `X_t`; COAT applies a
split at round `t` only from round `t+1`, so there is no off-by-one. The refinement `P_t'` is a
deterministic function of `P_t` and `L'`. The inequality
`|F(u) - F(u')| <= sum_a |u_a - u'_a|` for `F(u) = (u_i - max_{j != i} u_j)_+` is the manuscript's
own and is elementary. Lemma 8 is the manuscript's `lem:cell-average-l1` with the observation that
its proof bounds `||f^{(P)} - f||_1` by `2 eps + omega_g(mesh P)` with `g` chosen *before* `P`, so
the bound is uniform over partitions of a given mesh. And `E[(M_i - max_{j != i} M_j)_+] = 0` is the
two-top hypothesis. The step is also not load bearing: under Lipschitz capacities Theorem D.4 has an
explicit rate that does not use any of it, and that is the only case in which the manuscript's own
`thm:contextual-public` gives a rate.

#### 9.2.4 Standing caveat

I do not claim any statement in this file is correct. Each proof is written out so that it can be
checked; every numerical claim names the script, the seeds and the horizon; and Section 8 marks
which statements are proved, which are proved only under stated hypotheses, which are outlines and
which are open.

### 9.3 What I did not do

From the first version:


- I did not attempt to prove or break contextual sharp adaptivity or FATA for RA-ETC. Theorem 4
  already breaks robustness, which sharp adaptivity implies in the manuscript's accounting, but I
  did not write that implication out.
- I did not simulate instance W4 (permanent elimination); it is proved under stated hypotheses only.
- I did not attempt a lower bound, and I make no optimality claim for COAT.
- I did not examine COAT under non-i.i.d. or non-exogenous contexts; (R3) is used throughout and the
  contract's Section 11 item 5 records that the cell law is false without it.
- I did not examine a contextual behavioral class; everything here is `S_HDS` and its independent
  ex ante mixtures, and the last paragraph of the manuscript's appendix A.5 already records that the
  phase-dependent case is out of reach for the static grid too.

Added after `ADVERSARY.md`:

- I did not settle whether Theorem 3 is an independent converse or a symptom of Theorem 4's
  mechanism (Section 4.7.1, last paragraph).
- I did not find an instance in which a unilateral deviation, rather than the schedule, triggers
  mechanism (A) of Proposition 7. The adversary tried and failed; so did I.
- I did not examine variance-adaptive or empirical-Bernstein thresholds, which is where the
  adversary says it would look next for a rule that escapes Theorem 4.
- I did not settle the accelerate-only monotonicity question; Section 4.7.1 states what I closed and
  what remains.
- I did not re-verify the manuscript's own theorems; like the adversary, I take
  `thm:grid-etc`, `thm:contextual-public`, `lem:cell-law`, `lem:etc-tail`, `lem:region` and
  `lem:cell-average-l1` as given and check only that I use them within their stated hypotheses.
