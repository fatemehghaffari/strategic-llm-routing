# Contextual proof contract (Agent B, 17 September 2026)

Purpose: a single authoritative record of the contextual model, classes, algorithms, theorems, and proof dependencies of the canonical manuscript, extracted from `sections/setting.tex`, `sections/contextual.tex`, `sections/contextual_samf_algorithm.tex`, `sections/appendix_contextual.tex`, and the scalar files they depend on (`sections/Stochastic_SAMF_Conditions.tex`, `sections/appendix_samf.tex`, `sections/Public_information_setting.tex`, `sections/appendix_public.tex`, `sections/Private_information_setting.tex`, `sections/appendix_private.tex`). Every scout and every proof worker must work against this contract. Where the manuscript is ambiguous, the resolution adopted here is marked AMBIGUITY and justified. Nothing in this file is a new result; new claims live in the scout files and the candidate ledger.

Notation: `E_S` is expectation under profile `S`; `1{.}` is an indicator; `(x)_+ = max(x,0)`; `log` is natural; `[K] = {1,...,K}`.

## 1. Scalar primitives inherited by the contextual model

- Agents `i in [K]`, `K >= 2` fixed. Horizon `n` known to the platform. Agent `i` has intrinsic mean `mu_i in [0,1]` and capacity `M_i in [mu_i, 1]`.
- Round `t`: the platform selects `I_t`; the selected agent chooses a target `m_{I_t,t} in [0, M_{I_t}]`; the platform observes `Y_t ~ Bernoulli(m_{I_t,t})`, conditionally independent of the past given the target (setting.tex, lines 5 to 8). Effort cost `c_{i,t} = m_{i,t} - mu_i`, which may be negative.
- Counts and costs: `T_i(n) = sum_{t<=n} 1{I_t=i}`, `C_i(n) = sum_{t<=n, I_t=i} c_{i,t}`.
- Utilities: `u_i(n;S) = E_S[T_i(n) - C_i(n)]`, `P(n;S) = E_S[sum_t Y_t] = E_S[sum_t m_{I_t,t}]`. Per-pull utility is `1 + mu_i - m_{i,t} in [0,2]`.
- Honest set `K_H` nonempty; an honest agent never targets below its intrinsic mean (after every history in the behavioral class; pointwise in the map classes). `mu_H^* = max_{h in K_H} mu_h`, `M_top = max_i M_i`, `K_top = {i : M_i = M_top}`, `M_(2)` = second-largest capacity counting ties, `V_i = max_{j != i} M_j`.
- Reward seeds: the manuscript's coupling arguments realize `Y = 1{U <= m}` with `U` uniform on `[0,1]`, one fresh independent uniform per pull, drawn after the target is chosen (Private theorem hypothesis: "targets are chosen before fresh conditionally independent Bernoulli seeds"). AMBIGUITY (resolved): the seed index used by the manuscript is the agent's own local pull index (Stage-1 pull `r` in appendix_private.tex; "reward uniforms on common exploration pulls" in appendix_contextual.tex). Any pathwise monotonicity claim must state the indexing of seeds explicitly.

## 2. Contextual model (setting.tex, subsection "Contextual environment")

- Each round begins with a full profile `X_t = (x_{1,t},...,x_{K,t}) ~ nu`, i.i.d. across rounds and exogenous: neither platform nor agents influence the law, and the arrival process is independent of all reward seeds, mechanism randomness, and agents' private coins (this independence is what the proofs use; see Section 11).
- Platform observes `X_t` before selecting. Unless stated otherwise, the selected agent observes the full profile `X_t` before choosing its target (setting.tex). Agents otherwise remain blind as in the scalar model: own selection, own target, own reward, mechanism messages; not the global round, not other agents' histories.
- Context-dependent primitives: `mu_i(x_i)`, `M_i(x_i) in [mu_i(x_i), 1]`, cost `c_{i,t} = m_{i,t} - mu_i(x_{i,t})`. Utilities unchanged in form.
- Finite case: `X_t in X_F = {z_1,...,z_Q}`, a fixed finite set of full profiles; `Q` fixed.
- Continuous case: `X_t in X subseteq [0,1]^D`, `x_{i,t} in [0,1]^d`, `D := Kd`. Sections 6 and 7 of the manuscript take `X = [0,1]^D`. No claims are made for general infinite spaces without this structure.
- Pointwise definitions at a profile `X = (x_1,...,x_K)`: best honest intrinsic mean `b(X) = max_{h in K_H} mu_h(x_h)`; largest feasible mean `M_*(X) = max_i M_i(x_i)`; top set `T(X) = {i : M_i(x_i) = M_*(X)}`.
- Region counts for measurable `R subseteq X`: `V_R(n) = sum_{t<=n} 1{X_t in R}`, `T_i(R;n) = sum_{t<=n} 1{X_t in R, I_t = i}`. Shared-top portion `G_{ij}(R) = R cap {X : i, j in T(X)}`.

## 3. Ambient dimension and grid geometry

- Ambient dimension is `D = Kd` (full profile). Grid cells are half-open cubes of side `h_n` partitioning `[0,1]^D`; `J_n = O(h_n^{-D})` cells; `diam(C) = sqrt(D) h_n` in the Euclidean norm.
- Lipschitz constants are with respect to the Euclidean norm on `[0,1]^D`; a function of `x_i in [0,1]^d` that is `L`-Lipschitz in `x_i` is `L`-Lipschitz in `X`.
- For a set `A`, `A^{eps}` denotes its closed `eps`-neighborhood. A cube meeting both `R` and `R^c` lies in `(partial R)^{sqrt(D) h_n}`. Continuity from above: if `partial R` is closed with `nu(partial R) = 0`, then `nu((partial R)^{eps}) -> 0` as `eps -> 0`.
- Zero-mass cells are never visited and need no conditional mean. Cells are initialized lazily (Grid-ETC explicitly; Grid-UCB by the gap-free accounting in the proof).

## 4. Information structure

- Platform knows `n`, `K`, `D`. It does not know `nu`, `mu_i`, `M_i`, `L`, `K_H`, or the top sets. Grid widths `h_n` and `q_n` do not depend on `L` or `nu`; only the constants in the theorems do.
- Public setting (Theorems `thm:public-ucb`, `thm:finite-context` equilibrium part, `thm:contextual-public`): `M_top` (scalar) or `M_*(.)` (contextual) is public. The all-maximum profile requires each agent only to know its own capacity map.
- Private setting (MESP): capacities private; the mechanism announces the price `tau` and reveals the history used in its decisions.
- Horizon: all contextual results are fixed-horizon (`n` known to the platform; maps in `S_HDS` and strategies in `B_{i,n}` may depend on `n`). No anytime guarantees are claimed for the continuous results.

## 5. Strategy classes

- `S_HI` (scalar): deterministic, horizon-independent fixed mean `m_i in [0, M_i]`; honest: `m_h >= mu_h`.
- `B_{i,n}` (scalar behavioral, known `n`): every feasible nonanticipating strategy; after selection and before the current reward, `m_{i,t}` may depend on `n`, own available history, mechanism messages and counts, and independent private randomness. Honesty: `m_{i,t} >= mu_i` after every history.
- `S_F` (finite contexts): deterministic, horizon-independent feasible maps `m_i : X_F -> [0, M_i(x_i)]` (pointwise feasibility), honest maps pointwise at or above `mu_h(z_h)`.
- `S_HDS` (continuous contexts): horizon-dependent stationary measurable maps `m_{i,n} : X -> [0, M_i(x_i)]`, chosen before play knowing `n`, used throughout; honest maps satisfy `m_{h,n}(X) >= mu_h(x_h)` for every `X`. Independent ex ante randomization over such maps is permitted; the realized map cannot adapt to rewards, visit counts, or mechanism phases. If agents observe only their own contexts, maps depend only on `x_i`.
- AMBIGUITY (resolved): in `S_HDS` the map may depend on the full profile `X` (default observation model), and it may depend on `n` and hence on `h_n` and the grid (the experiment's "cell-aligned" deviation does exactly this). A deviation may therefore be grid-aligned; the theorems must hold for such maps.
- AMBIGUITY (resolved): the manuscript defines no contextual behavioral class. For private contextual scouting, the natural lift, denoted here `B^ctx_{i,n}`, is: after selection at round `t`, agent `i` may choose `m_{i,t} in [0, M_i(x_{i,t})]` as a function of `n`, the current full profile `X_t`, its own entire history across all contexts (its selections, the profiles at those selections, its targets, its rewards, mechanism messages), and independent private randomness; honesty is `m_{i,t} >= mu_i(x_{i,t})` after every history. Any theorem for a smaller class must say so.

## 6. Definitions of the contextual properties (contextual.tex, lines 3 to 8; setting.tex, Definition 1)

For a declared class `S` and a fixed measurable `R`:

- Contextual sharp adaptivity with remainder `r_n` (agent `i`):
  `E_S sum_{t<=n} 1{X_t in R, I_t = i} c_{i,t} >= E_S sum_{t<=n} 1{X_t in R, I_t = i} [b(X_t) - mu_i(x_{i,t})] - r_n`, uniformly over `S in S^K`.
- Contextual monotonicity: for every allowed map profile, every `i != j`, and the profile obtained by replacing `m_i` pointwise by `M_i`, the latter gives `E T_j(R;n)` no increase beyond the stated remainder.
- Contextual FATA: whenever `m_i(X) = m_j(X) = M_*(X)` on `G_{ij}(R)`, `|E T_i(G_{ij}(R);n) - E T_j(G_{ij}(R);n)|` is at most the stated remainder. "Exact" means zero remainder.
- Robustness (global): `P(n) >= E sum_{t<=n} b(X_t) - error`.
- Uniformity convention (contextual.tex): finite UCB monotonicity is pointwise in each fixed comparison; the grid bounds are uniform after conditioning on realized ex ante maps and hence also for their independent mixtures.
- Restricted asymptotic equilibrium (Definition 1): for a declared class `S`, a profile `S in S^K` is an `S`-asymptotic equilibrium if for every `i` and every `S_i' in S`, `u_i(n; S_i', S_{-i}) <= u_i(n; S) + o(n)`.
- Additive behavioral asymptotic equilibrium: an `n`-indexed profile `S^*` with `sup_{S'_{i,n} in B_{i,n}} {u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)} = o(n)` for every `i`.
- Scalar stochastic SAMF (Stochastic_SAMF_Conditions.tex): sharp adaptivity `E_S C_i(n) >= (mu_H^* - mu_i) E_S T_i(n) - C sqrt(n log(en))` with universal `C`; monotonicity `E_{S^{i up}} T_j(n) <= E_S T_j(n) + o(n)` pointwise in fixed `S`; FATA `|E T_i - E T_j| = o(n)` for equal top reward laws.

## 7. Algorithms with all parameters

### 7.1 Symmetric scalar UCB1 (Stochastic_SAMF_Conditions.tex)
Initialize agents once each in a uniform random order; thereafter select an agent maximizing `hat m_i + sqrt(2 log t / T_i)` with `t` the current round of the instance; ties broken by an independent uniform draw each round. Anytime index (uses global time `t` of the instance), not the horizon.

### 7.2 Finite-Context UCB1 (contextual.tex, appendix_contextual.tex A.1)
An independent symmetric local-time UCB1 instance for every exact profile `z in X_F`; "local time" is the instance's own visit count `V_z`; no statistics are shared. Conditional on `V_z = s`, the instance is exactly an `s`-round fixed-mean UCB1 execution when maps are fixed.

### 7.3 Static Grid-UCB1 (contextual_samf_algorithm.tex; appendix A.3)
Deterministic partition of `[0,1]^D` into `J_n = O(h_n^{-D})` half-open cubes of side `h_n ~ (log(en)/n)^{1/(D+2)}`; independent cell-local symmetric UCB1 instances (local time = cell visit count); the exact profile is used only to locate the cell (cell-blind rule). Code (`scratch/experiments/final/contextual_performance/run.py`, class `CellUCB`): index `z/n + sqrt(2 log(max(2, n.sum()))/n)` with `n.sum()` the cell visit count, first-unseen deterministic initialization, argmax tie to the lowest label, key = clipped floor(`x/h`), `h = (log(en)/n)^{1/(D+2)} * mult`.

### 7.4 Static Grid-ETC (contextual_samf_algorithm.tex; appendix A.4)
Dyadic side `h_n` within a constant factor of `n^{-1/(D+3)}`; `J_n = O(h_n^{-D})`; `q_n = ceil(n^{2/(D+3)})`. In each lazily initialized cell: `q_n` independent uniform permutations of `[K]`; the first `K q_n` cell visits follow these blocks (last observed block possibly truncated); after all blocks finish, commit to an agent with the largest exploration empirical mean (over exactly `q_n` observations each), ties by an independent uniform priority permutation drawn once per cell; exploitation rewards are ignored. Code (`CellETC`, and `GridETC` in `contextual_incentives/run.py`) matches: `h = n^{-1/(D+3)}`, `q = ceil(n^{2/(D+3)})`, one permutation per block, fixed per-cell priority, post-exploration feedback ignored.

### 7.5 MESP (Private_information_setting.tex), scalar, needed by scout B4
For `n >= 2K`: `L_n = min{floor(n/(2K)), ceil(n^{2/3} (log(en))^{1/3})}`, `N_n = n - K L_n >= n/2`, `s_n = sqrt(log(2 K n^4)/(2 L_n))`, `b_n(r) = sqrt(r log(2 n^4)/2)`, `b_n(0) = 0`. Stage 1: pull each agent `L_n` times; empirical bid `beta_i`. Winner `W` = largest bidder (independent uniform priority for ties); announce `tau = (beta_(2) - s_n)_+` with `beta_(2)` the second order statistic with multiplicity. Stage 2: pull `W`; after its `r`-th primary pull with reward sum `Z_r`, switch if `Z_r < r tau - b_n(r)`. Stage 3: restart explicit-exploration EXP3 over all `K` agents for the `H` remaining rounds with `gamma = min{1/2, sqrt(K log K / H)}`, `eta = gamma/K`, estimator `hat Y_{i,t} = Y_t 1{I_t = i}/p_{i,t}`; `R_K(H) = 3 sqrt(K H log K) + 2 K log K`, `R_K(0) = 0`. For `n < 2K`: cyclic allocation. Proposed profile `S^*`: capacity in bidding and fallback; strategic primary winner delivers `min{tau, M_i}`; honest winner `max{mu_i, min{tau, M_i}}`.

## 8. Theorem statements and rates (verbatim content)

- `thm:finite-context` (Finite-context UCB1). Assume exogenous profile arrivals independent of reward tapes and deterministic horizon-independent context maps (`S_F`). For every `R subseteq X_F` and agent `i`: sharp adaptivity with remainder `O(sqrt(|R| n log(en)))`; contextual monotonicity with `o(n)` remainder (pointwise in the fixed comparison); exact expected FATA on `G_{ij}(R)`; robustness `P(n) >= E sum_t b(X_t) - O(K sqrt(Q n log(en)))`. If profiles are i.i.d. with positive fixed masses, `|T(z)| >= 2` for every `z`, and `M_*(z)` is public: the all-maximum profile is an `S_F`-asymptotic equilibrium and `P(n; S^max) >= E sum_t M_*(X_t) - O(log n)`.
- `thm:grid-ucb-robust` (Static-grid UCB1 robustness). `X = [0,1]^D`, intrinsic functions `L`-Lipschitz. Uniformly over `S_HDS`: `P(n) >= E sum_t b(X_t) - O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})`. Robustness only; no monotonicity, FATA, or equilibrium claimed for Grid-UCB1.
- `thm:grid-etc` (Static Grid-ETC contextual SAMF). Uniformly over `S_HDS`, constants depending only on fixed `K, D, L`, for every fixed `R` with `nu(partial R) = 0`: sharp adaptivity with error `O(n^{(D+2)/(D+3)} + n nu((partial R)^{sqrt(D) h_n})) = o(n)`; global robustness with error `O(n^{(D+2)/(D+3)})`; exact pathwise monotonicity under the natural common-uniform coupling (for every `R`, no boundary condition); if `nu(partial G_{ij}(R)) = 0`, expected contextual FATA on `G_{ij}(R)` with remainder `n nu((partial G)^{sqrt(D) h_n}) = o(n)`.
- `thm:contextual-public` (Continuous public restricted equilibrium). Assume capacities continuous; a fixed closed `B` with `nu(B) = 0` such that `X \ B` has finitely many connected components; on each component the top set is constant and has at least two agents whenever the component has positive mass; `M_*` public. Then under Static Grid-ETC, all-maximum play is an `S_HDS`-asymptotic equilibrium (including against independent ex ante mixtures) and `P(n; S^max) >= E sum_t M_*(X_t) - o(n)`. Rates: top-agent gain `O(n/sqrt(q_n)) + O(q_n J_n)`; non-top gain `o(n)` via dominated convergence (no explicit rate); boundary cells `n nu(B^{sqrt(D) h_n}) = o(n)`.
- Scalar dependencies: `thm:scalar-ucb` (UCB1 stochastic SAMF on `S_HI`: sharp adaptivity `O(sqrt(n log(en)))`, monotonicity `o(n)` pointwise in fixed profiles, exact expected FATA); `thm:sharp-robustness`; `thm:public-ucb` (`K_top >= 2`, `S_HI` equilibrium, revenue `M_top n - O(log n)`); `thm:private-mesp` (behavioral additive equilibrium with fixed-instance gain `O(n^{2/3} (log n)^{1/3})`, revenue `M_(2) n - O_K(n^{2/3} (log n)^{1/3})`, honest-benchmark robustness against arbitrary behavioral profiles at the same rate).

## 9. Regularity assumptions, exactly as used

- Grid-UCB1 and Grid-ETC sharp adaptivity and robustness: `mu_i` `L`-Lipschitz for every `i` (used only through `b = max_{h in K_H} mu_h`, which is then `L`-Lipschitz, and through honesty `m_{h,n} >= mu_h`). Inequality used: for the honest `h_C` attaining `b(x_C)` at a representative `x_C in C`, `b(x) <= m_{h_C,n}(x) + 2 L diam(C)` for all `x in C`. Capacities need not be Lipschitz for these two properties.
- Grid-ETC monotonicity: no regularity at all (pathwise coupling).
- Grid-ETC FATA: `nu(partial G_{ij}(R)) = 0` (boundary of the shared-top portion), not merely `nu(partial R) = 0`.
- `thm:contextual-public`: capacities continuous (used to get `bar d_{i,C_n(X)} -> d_i(X) > 0` for a non-top agent as cells shrink, and so that a top agent's cell mean equals `bar M_C := E[M_*(X) | C]` on cells interior to a stable piece); `B` closed and `nu`-null (so `nu(B^{sqrt(D) h_n}) -> 0`); finitely many components (so that a cube disjoint from `B` lies in one top-stable piece and so that the finite sum over pieces closes the argument).
- Finite-context theorems: no regularity; `Q` fixed; positive fixed masses only in the public part.

## 10. Top-set assumptions

- Scalar public: `K_top >= 2`. Necessity remark (appendix_public.tex): a unique top agent with downward slack above the runner-up can shade and save linear effort; knife-edge cases can still be equilibria.
- Finite-context public: `|T(z)| >= 2` for every `z in X_F` (statement says every `z`; positive masses assumed separately).
- Continuous public: top set constant on each component of `X \ B` and of size at least two on every positive-mass component. The manuscript itself flags this as "an additional structural assumption used by the proof and not implied by continuity".

## 11. Exactly where i.i.d. contexts are used

1. Lemma `lem:cell-law` (appendix A.2): conditional on the membership-indicator sequence of a cell `C`, the ordered exact profiles visiting `C` are i.i.d. `nu(. | C)`; cell-blind selected rewards of agent `i` are i.i.d. Bernoulli(`bar m_{i,C}`) with `bar m_{i,C} = E[m_{i,n}(X) | X in C]`; data from the first `r` cell visits are independent of profiles and membership indicators after the `r`-th cell visit. This is the only place i.i.d.-ness enters the grid proofs, and everything downstream uses it: the per-cell reduction to a fixed-mean instance (Grid-UCB1 robustness, Grid-ETC exploration), the factorization "commitment probability times conditional cell mean" for ETC exploitation, and the identity `E[1{X in R} 1{I = j}] = nu(R | C) Pr(I = j)` implicit in the region accounting.
2. Boundary accounting: expected visits to cells meeting `partial R` (or `B`) equal `n nu((partial R)^{sqrt(D) h_n})` because each `X_t ~ nu`.
3. Dominated convergence in `thm:contextual-public` integrates against `nu`.
4. Finite-context public part: "i.i.d. with positive fixed masses" so that `E V_z` is linear in `n`. The finite-context SAMF part needs only exogenous arrivals independent of reward tapes (appendix A.1, first paragraph: "The context process may otherwise be arbitrary and exogenous").
5. Counterexample recorded by the prior audit (CONTEXT_REFEREE.md item 4, verified by inspection): an exogenous deterministic alternating context sequence combined with a fixed exploration schedule can assign all favorable subcontexts to one agent; the cell-law lemma is false without i.i.d. profiles (or at least exchangeable within-cell profiles independent of the schedule).

## 12. Exactly where fixed ex ante maps are used

1. Lemma `lem:cell-law`: `bar m_{i,C}` is defined by integrating a fixed map; a target depending on local visit counts or phases destroys the i.i.d. Bernoulli reduction (bait-and-switch, appendix A.4 last paragraph and CONTEXT_REFEREE.md item 5).
2. Grid-ETC monotonicity coupling: "replacing `m_i` pointwise by `M_i`" is a comparison of two fixed maps with all other maps unchanged; the coupling of reward uniforms on common exploration pulls uses `1{U <= M_i(x_i)} >= 1{U <= m_{i,n}(X)}` on the same visit (same `X`), which is available only because exploration pulls occur at reward-independent visits.
3. Finite-context: fixed `S_F` maps make each local instance a fixed-mean UCB1 execution; the monotonicity remainder `o(n)` is pointwise in the two fixed profiles and is not uniform over horizon-dependent gaps (appendix_samf.tex monotonicity proof, last sentence). Sharp adaptivity and robustness there are gap-uniform and therefore also hold for horizon-dependent deterministic maps and, by conditioning, for independent mixtures.
4. `thm:contextual-public`: deviations are fixed maps `m'_{i,n}`; the proof's per-cell quantities `delta_C`, `p'_C` are defined from the fixed map; the closing sentence of appendix A.5 states that the proof fails for phase-dependent strategies.

## 13. Lemmas the contextual proofs import

- `lem:ucb-deficit` (appendix_samf.tex): fixed profile in `S_HI`, `m^* = max_k m_k`; for every `i` and comparator `a <= m^*`, `(a - m_i)_+ E T_i(n) <= C sqrt(n log(en))`, from `E T_i(n) <= 8 log(en)/Delta^2 + c_0` (Auer, Cesa-Bianchi, Fischer 2002) split at `Delta = sqrt(log(en)/n)`.
- Gap-free bound `eq:gap-free-ucb`: in an `s`-round fixed-mean instance, `E sum_{r<=s} (m^* - m_{I_r}) <= C sqrt(K s log(es)) + C K`.
- `lem:etc-tail`: two empirical means of `q` i.i.d. Bernoulli observations with means `a < b`, `Delta = b - a`: `Pr(hat a >= hat b) <= 2 e^{-q Delta^2 / 2}` and `Delta Pr(hat a >= hat b) <= C q^{-1/2}`; for `K` agents `E[bar m^* - bar m_{hat I}] <= C K q^{-1/2}`.
- `lem:cell-law` as in Section 11.
- Private lemmas (for scout B4): `lem:private-monitor` (time-uniform Azuma with `Pr{exists r <= n : |Z_r - A_r| > b_n(r)} <= n^{-3}`; on the complement `A_q >= q tau - 1 - 2 b_n(q)`; false-switch probability at most `(2 n^3)^{-1}` when all primary targets are at least `tau`), `lem:selected-reactive-exp3` (conditional on the fallback-start history, `E[sum_{t<=H} Y_t | F_fb] >= v H - R_K(H)` when a fixed comparator has conditional mean at least `v` whenever selected; `H` known at restart), bid coupling `beta'_i <= beta_i^max` pathwise, price `tau_i = (max_{j != i} beta_j - s_n)_+` independent of `i`'s bid, good event `G_{-i}` with probability at least `1 - n^{-4}` on which `(V_i - 2 s_n)_+ <= tau_i <= V_i`.

## 14. Ambiguities resolved (and how)

1. Seed indexing for couplings: by the agent's local pull index within the relevant instance (Section 1). A pathwise claim across executions in which the same local pull occurs at different visits (hence different profiles) does not follow from pointwise feasibility; it must be reproved (this matters for any UCB-type contextual monotonicity claim).
2. Whether `S_HDS` maps may depend on the grid: yes (Section 5).
3. Contextual behavioral class: not defined in the manuscript; `B^ctx_{i,n}` of Section 5 is the working definition for private contextual scouting.
4. Which functions are Lipschitz: the manuscript says "the intrinsic functions are `L`-Lipschitz"; the proofs use only `mu_i` Lipschitz (through `b`). Capacities are assumed continuous only in `thm:contextual-public`. Any new result that needs Lipschitz capacities must add that assumption explicitly.
5. "For every `z`" in the finite-context public theorem is read as every `z in X_F`; profiles of zero mass are irrelevant to utilities, so "every positive-mass `z`" would suffice.
6. The finite-context theorem's first four properties need exogenous arrivals independent of reward tapes but not i.i.d. arrivals (appendix A.1); only the public part needs i.i.d. positive masses.
7. Code versus manuscript for UCB1: the code initializes in label order and breaks ties toward the lowest label, whereas the manuscript uses a uniform random initialization order and independent uniform tie-breaking; the theorems are about the manuscript's rule. The code's Grid-UCB1 index uses the cell's local visit count in the logarithm, consistent with "local-time UCB1".
8. Baseline finding 3 (BASELINE.md): the contextual-incentives experiment has top set `{0,1}` everywhere; it does not exercise changing top identities.

## 15. Open items the manuscript itself declares

Private contextual incentives (Intro, Conclusion); non-i.i.d. contexts; irregular boundaries; contextual bait-and-switch behavior; Grid-UCB1 monotonicity (only robustness is claimed for Grid-UCB1); finite-component top stability is "not implied by continuity"; no explicit rate for the continuous public equilibrium gain.
