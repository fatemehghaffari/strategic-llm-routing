# Task C1 + C0: known-horizon UCB, exact monotonicity, and Static Grid-UCB as a full contextual SAMF mechanism

Written by Agent B for the two provers and the hostile worker. Notation as in audit/round2/B/CONTEXT_PROOF_CONTRACT.md. No Unicode em dashes, no triple hyphens, anywhere. Never present an incomplete proof as complete.

## Algorithms (fixed)

KH-UCB(n, pi) (scalar, known horizon n, one ex ante priority): a uniformly random permutation pi of [K] is drawn once before play. At each round, if some agent has count zero, pull the pi-first such agent; otherwise pull the agent maximizing hat m_a + sqrt(4 log(n) / T_a), ties broken by pi. (This is Lattimore and Szepesvari's UCB(delta) with delta = 1/n^2 and index hat mu + sqrt(2 log(1/delta)/T); Bernoulli rewards are 1/2-subgaussian hence 1-subgaussian, so their Theorem 7.1 applies verbatim; provers must state the exact imported bound with constants and source.)

Finite-Context KH-UCB: one independent KH-UCB(n, pi_z) instance per exact profile z (global n in the logarithm, own priority per profile).

Static Grid KH-UCB: deterministic partition of [0,1)^D into half-open cubes of side h_n := (log(en)/n)^{1/(D+2)} (J_n := ceil(1/h_n)^D cells), one lazily initialized KH-UCB(n, pi_C) per cell with the GLOBAL n in the logarithm and its own ex ante priority pi_C, cell-blind decisions (the exact profile is used only to locate the cell).

Tape coupling (scalar and finite context): reward uniforms U_{a,k} indexed by agent and own pull index; Y_{a,k} = 1{U_{a,k} <= m_{a,k}}. Cell-average coupling (grid): conditional on all cell membership sequences, realize each cell C's execution with tapes 1{U_{C,a,k} <= bar m_{a,C}}, bar m_{a,C} := E[m_{a,n}(X) | X in C]; justify via lem:cell-law that this has the correct joint law of (I_t, Y_t) restricted to the cell.

## Target statements

S0 (static race lemma). Arms a in [K] with arbitrary sequences f_a : {0,1,...} -> [-inf, +inf]; fixed strict priority; greedy pull of argmax (f_a(T_a), a) lexicographic. If f_1' >= f_1 pointwise and f_a' = f_a otherwise, then T_j'(t) <= T_j(t) for all j != 1 and all t, and T_1'(t) >= T_1(t). (Prior work: Feng, Parkes, Xu ICML 2020 Lemmas B.2 and B.3; Esmaeili, Shin, Slivkins AAAI 2025 Theorem B.11 and Claim B.12, both for known-horizon UCB with the prefix argument. Provers must give a complete proof, may follow the prefix argument or an envelope argument, and must state exactly how the fixed priority is used.)

S1 (C0, scalar). Under KH-UCB(n, pi) and the tape coupling, for fixed means (S_HI, also horizon-dependent means) and for blind own-history behavioral strategies of the other agents: replacing agent i's strategy by the constant M_i gives T_j(t) weakly smaller for every j != i and every t <= n on every sample point (conditional on pi), and T_i weakly larger. Consequently thm:scalar-ucb holds for KH-UCB with monotonicity exact and pathwise (zero remainder), sharp adaptivity error O(sqrt(n log n)) with explicit constants from the imported bound, and exact expected FATA (label symmetry with a uniform pi). Remark to prove: the anytime index sqrt(2 log t / T) is NOT pathwise monotone (K = 3, n = 8 tape in audit/round2/B/LEAD_PRELIMINARY_CLAIMS.md Claim L3; verify it).

S2 (C0, finite context). Finite-Context KH-UCB satisfies thm:finite-context with monotonicity exact (zero remainder) for every R subseteq X_F, by conditioning on visit counts; other parts unchanged (state the constants).

S3 (C1 (iii), grid, exact expected monotonicity). For every allowed map profile in S_HDS, every i != j, and EVERY measurable R, replacing m_i pointwise by M_i gives E T_j(R; n) no increase, zero remainder, every n. Key identity to prove including cells visited fewer than K times and random visit counts: E[T_j(C cap R; n)] = nu(R | C) E[T_j(C; n)] for every cell C with nu(C) > 0 (the decision at the k-th visit of C is measurable with respect to the data of the first k minus 1 visits of C and the cell's coins, independent of the k-th visit's profile).

S4 (C1 (i), grid sharp adaptivity). For every agent i and every measurable R, remainder 2 L sqrt(D) n h_n + C_1 sqrt(J_n n log n) + C_2 J_n + n nu((partial R)^{sqrt(D) h_n}) with explicit C_1, C_2 depending on K only, under L-Lipschitz intrinsic means; the first three terms are O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)}).

S5 (C1 (ii), robustness). Already thm:grid-ucb-robust in the manuscript with the anytime index; provers only restate it for KH-UCB with explicit constants from the imported bound.

S6 (C1 (iv), FATA). Expected FATA on G_{ij}(R) with remainder n nu((partial G_{ij}(R))^{sqrt(D) h_n}), by label symmetry in cells inside G (uniform pi_C) and counting boundary cells.

S7 (C1 (v), revenue). If capacities are L-Lipschitz, P(n; S^max) >= E sum_t M_*(X_t) - [2 L sqrt(D) n h_n + C_1 sqrt(J_n n log n) + C_2 J_n].

S8 (C1 (vi), public equilibrium). If capacities are L-Lipschitz and nu(|T(X)| >= 2) = 1, every unilateral S_HDS deviation (deterministic or independent mixture) by any agent i gains at most C_3 sqrt(J_n n log n) + C_4 J_n + 2 L sqrt(D) n h_n = O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)}). Per-cell argument: gain_C <= E T'_i(C) delta_C (self-monotonicity from S0 under the cell-average coupling, and a_C >= 0); the rival inequality max_{j != i} bar M_{j,C} >= bar M_{i,C} - 2 L sqrt(D) h_n in every positive-mass cell; the imported deficit bound E[T'_i(C) | V_C = s] <= min{s, 3 + 16 log n / Delta'^2} with Delta' the deviator's cell gap to the best rival; the split min{s Delta', 16 log n / Delta' + 3 Delta'} <= 8 sqrt(s log n) + 3; Cauchy-Schwarz over cells with sum_C E V_C = n.

## Requirements from the main agent (non-negotiable)

1. State the exact imported UCB bound for Bernoulli rewards with constants and source (Lattimore and Szepesvari, Bandit Algorithms, Theorem 7.1 and Theorem 7.2, https://tor-lattimore.com/downloads/book/book.pdf; verify the statement yourself and record the URL and page), and explain why it applies to a cell with a random number s <= n of visits (condition on the membership sequence; the confidence level 1/n^2 is over the global horizon).
2. Prove the identity of S3 including cells visited fewer than K times (initialization rounds) and random visit counts.
3. Check ties and the one-priority-per-cell rule everywhere (initialization order and later ties both by pi_C); state what fails with per-round fresh tie coins (the lead's scout found that pathwise monotonicity fails but exact expected monotonicity holds; you may prove or skip the latter, but do not claim it without proof).
4. Keep S5 as already proved (do not reprove beyond restating constants).
5. Every quantifier explicit: every n, every map profile, every region; constants depend only on K, D, L.
6. Mixtures by conditioning on the realized map.
7. Zero-mass cells never visited; lazy initialization; sums over visited cells.
8. Do not claim minimax optimality in D.

## Output format

Sections: 0 status line (updated incrementally); 1 exact theorem statements ready for the paper; 2 lemmas with complete proofs (S0, imported bound, cell-average coupling law, the S3 identity); 3 proofs of S1 to S8; 4 assumption usage list; 5 self-audit; 6 verified references with URLs.

## Addendum (17 September 2026): three lessons carried over from the decided candidate C3

These are requirements, not suggestions. They come from the adjudicated C3 pipeline.

L1. No filtration, no nesting, no martingale citation anywhere. The following lemma is proved and adopted: for any sequence of finite Borel partitions `P_n` of a compact `X` with `mesh(P_n) -> 0`, any Borel probability `nu`, and any bounded Borel `f`, the cell-average function `f^{(n)}` (equal to `E[f | C]` on each positive-mass cell `C in P_n`, and `0` on null cells) satisfies `||f^{(n)} - f||_{L^1(nu)} -> 0`. Proof: pick `g` continuous with `||f - g||_1 <= eps` (continuous functions are dense in `L^1` of a finite Borel measure on a compact metric space); conditional expectation is an `L^1` contraction so `||(f-g)^{(n)}||_1 <= eps`; and `|g^{(n)} - g| <= omega_g(mesh(P_n))` pointwise by uniform continuity. Hence the grid need not be nested and Levy's upward theorem must not be invoked. If any step of your proof appears to need almost sure convergence of cell averages, reformulate it with Markov's inequality applied to the `L^1` defect (example: to show that the cells on which a bounded Borel `phi` has cell average at least `c` carry almost all of the mass of a set where `phi >= c + gap`, bound the exceptional mass by `||phi^{(n)} - phi||_1 / gap`).

L2. Track the Lipschitz constant as `L sqrt(d)`, where `d = D/K` is the per-agent dimension, not `L sqrt(D)`. A capacity or intrinsic mean `M_j` is a function of the block `x_j` alone, and inside a cell of side `h_n` that block varies by at most `sqrt(d) h_n` in Euclidean norm. Where the argument compares a function at two points of a cell, use the one-step form `M_j(x_j) <= E[M_j | C] + L sqrt(d) h_n` for every `X in C` (integrate the Lipschitz bound in the second variable) rather than chaining two Lipschitz steps through a distinguished point, which costs an unnecessary factor of two.

L3. Name the imported bandit bound exactly. State the exact inequality you import for the known-horizon index, with its constants, the subgaussian or bounded-reward hypothesis under which it holds, and a source whose statement you verified yourself in this session (record the URL and the page or theorem number you actually read). Explain why it applies to a cell whose number of visits `s <= n` is random (condition on the membership sequence; the confidence level is set from the global `n`). Separately, flag EVERY step at which the known-horizon index `hat m_a + sqrt(c log n / T_a)` is used in place of the manuscript's anytime index `hat m_a + sqrt(2 log t / T_a)`. The substitution is the entire content of this candidate and must never be assumed silently: the anytime index is provably not pathwise monotone (explicit tape in LEAD_PRELIMINARY_CLAIMS.md Claim L3), so any step that would be false for the anytime index must be marked as such.
