# SCOUT B1: monotone index policies and known-horizon UCB (17 September 2026)

STATUS: IN PROGRESS. Sections are appended as they are finished; anything below the last completed section heading is not yet reviewed.

Scope (from the role brief): known-horizon UCB with index `hat m_a + sqrt(c log n / T_a)`; exact pathwise monotonicity under a common-uniform coupling when one arm's target map is raised pointwise; minimal counterexamples; consequences for Static Grid-UCB; unknown horizon; literature; final classification.

Conventions: `log` is natural; `[K] = {1,...,K}`; `(x)_+ = max(x,0)`; `1{.}` indicator. All scripts live under `<scratchpad>/round2/B/scoutB1/` and were run with the venv python named in COMMON.md. No canonical file was edited.

## Summary of findings (written first so that an interruption loses nothing)

1. Claim L1 (static race monotonicity, fixed priority) is TRUE. Complete proof in Section B via Claim L2 (envelope identity, also TRUE, proved in Section B) and a sorted-order characterization of the greedy merge of nonincreasing sequences.
2. Under the manuscript's per-round independent uniform tie-breaking the pathwise statement is FALSE (explicit K = 3, n = 8 reward tape in Section C), but exact expected monotonicity (zero remainder) is TRUE for the known-horizon index; proof in Section C by a two-stage coin construction. Consequence: known-horizon UCB with either tie rule is exactly expectation-monotone; with one ex ante priority it is also pathwise monotone under the local-count tape coupling.
3. Claim L3 (anytime UCB1 is not pathwise monotone) is VERIFIED exactly (Section D). Exact expected monotonicity of anytime UCB1 remains OPEN: 1200 exact dynamic-programming instances show no violation, and no proof is available because the index depends on the global round.
4. The static race lemma is not new: Feng, Parkes and Xu (ICML 2020, arXiv 1906.01528, Lemmas B.2 and B.3) and Esmaeili, Shin and Slivkins (AAAI 2025, arXiv 2312.07929, Theorem B.11 and Claim B.12) prove pathwise monotonicity of known-horizon UCB by a prefix argument under the same coupling; Section H states precisely what they cover, where their write-ups are incomplete (ties), and what is new here (envelope identity for arbitrary non-monotone index sequences, the per-round tie rule in expectation, the blind behavioral extension, and the cell-average coupling for static grids).
5. Static Grid-UCB with the known-horizon index gives, with complete proofs in Section F: contextual sharp adaptivity and robustness at rate O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)}) plus the boundary term; exact expected contextual monotonicity for every measurable R with zero remainder (via the cell-average tape coupling, not the actual-visit coupling, which fails pathwise: counterexample in Section F(iv)); expected FATA with boundary term; the public restricted equilibrium under the weaker assumption "capacities continuous and |T(X)| >= 2 for nu-almost every X", with explicit gain rate under Lipschitz capacities; revenue at all-maximum play at the same explicit rate with no top-set assumption.
6. A doubling schedule with fresh statistics per epoch preserves all of the above with the same rates (Section G).

## A. Attack log on Claims L1 and L2

Model attacked (exactly Claim L1): `K` arms; arm `a` has a fixed sequence `f_a(0), f_a(1), ...` in the extended reals; a fixed strict priority order `succ` on arms; at each step the arm maximizing `(f_a(T_a), a)` in the lexicographic order (value first, then priority) is pulled. "Raising arm 1" means `f_1'(k) >= f_1(k)` for every `k`, all other sequences and the priority unchanged.

Scripts (all under `<scratchpad>/round2/B/scoutB1/`, venv python, total runtime under one minute on the login node):

- `race_attack.py`: 300000 random instances, `K in {2,3,3,4,5}`, `n in {4,6,8,10,14}`, values drawn from `{0,1}`, `{0,1,2}`, `{-2,...,2}` or `{0,...,5}` (so ties within an arm and across arms are frequent and the sequences are non-monotone in the count), with count-zero value `+inf`, `-inf`, or ordinary; raise applied to a random subset of counts by `0, 1, 2` or `5`; uniformly random priority; L1 checked at every intermediate time `t <= n` and every `j != 1`; L2 checked as equality of the entire pull sequence. Outcome: 0 violations of L1, 0 violations of L2.
- `ucb_attack.py`, mode `fixed`: 200000 instances of the known-horizon index `hat m_a(k) + sqrt(c log n / k)` (`c in {0.25, 0.5, 1, 2}`, `n in {5,...,12}`, `K in {2,3,3,4}`), Bernoulli tapes indexed by local pull count under the coupling `Y_{a,r} = 1{U_{a,r} <= m_a}` with arm 1 raised to a random `M_1 >= m_1`, count-zero index `+inf`, one fixed priority for initialization and all later ties, checked at every `t <= n`. Outcome: 0 violations.

Attempted counterexample families and why each fails (each was also part of the random search above):

1. Ties within an arm (`f_a(k) = f_a(k+1)`): irrelevant to the lexicographic rule; no violation.
2. Ties across arms at equal value: resolved by the fixed priority; the proof in Section B shows the priority enters only through the total order on pairs `(value, arm)`.
3. Priority realizations: every priority permutation was tested; the lemma is stated for an arbitrary fixed priority, so a random ex ante priority (as in the manuscript's random initialization order) is covered by conditioning.
4. Initialization with `+inf` at count zero (arms pulled once each in priority order first) and with `-inf` (arms pulled only when everything else is exhausted): both are instances of the lemma with extended-real values; no violation.
5. Per-round versus fixed tie-breaking: with fresh per-round coins the pathwise claim FAILS (Section C gives an explicit tape); with a fixed priority it holds. This is the only genuine failure mode found, and it is outside the hypotheses of L1.
6. `K = 2` versus `K >= 3`: `K = 2` is trivial (Section B, Remark); all `K` up to 5 were tested with no violation.
7. Sequences non-monotone in the count, including "raise now, crash later" patterns such as `f_1 = (0, 10, 0, 10, ...)` raised at odd counts only: the envelope identity (L2) shows that only the running minimum matters, so a raise that exposes a later low value cannot help any other arm; no violation.
8. Delayed pulls, changed local pull counts, changed global times: under the local-count tape coupling the index sequence of each arm is a fixed function of its own count, so the global time at which a local pull occurs is irrelevant. This is exactly what fails for the anytime index (Section D).
9. Shrinking gaps: the lemma is pathwise and gap-free; nothing to attack.
10. Horizon-dependent maps: the horizon enters the index only as a constant; the lemma is applied for each fixed `n`.
11. Context cells: the lemma applies to a cell-local execution only under the cell-average tape model (Section F(iv)); under the actual-visit coupling pathwise monotonicity is FALSE (explicit counterexample in Section F(iv)).

## B. Complete proof of L2 and L1 (fixed priority)

### Setting and notation

Let `V` be a totally ordered set (in applications the extended reals `[-inf, +inf]`). For each arm `a in [K]` let `f_a : {0, 1, 2, ...} -> V` be an arbitrary function (no monotonicity in the count is assumed). Let `succ` be a strict total order on `[K]` (the priority). Order the pairs `(v, a) in V x [K]` lexicographically: `(v, a) > (w, b)` iff `v > w`, or `v = w` and `a succ b`. Since priorities are distinct, two pairs with distinct arms are never equal.

The greedy merge `G(f)` is the sequence `(I_t)_{t >= 1}` defined by `T_a(0) = 0` and, at step `t`, `I_t = argmax_a (f_a(T_a(t-1)), a)` (unique by the total order on pairs), `T_a(t) = T_a(t-1) + 1{I_t = a}`. All statements are for every step `t >= 1`; a finite horizon `n` is the restriction to `t <= n`, for which only the values `f_a(k)`, `k <= n - 1`, matter.

Envelope: `e_a(k) := min_{0 <= k' <= k} f_a(k')`, a nonincreasing function of `k` with `e_a <= f_a`.

### Lemma B.1 (envelope identity, Claim L2)

For every family `(f_a)` and every priority, `G(f) = G(e)` step by step.

Proof. By induction on `t`. Suppose the two merges agree up to step `t - 1`, so they are in the same state `T = (T_a)_a` at the start of step `t`. Let `a^*` be the arm chosen by `G(f)` at step `t`. It suffices to show that `(e_{a^*}(T_{a^*}), a^*) > (e_b(T_b), b)` for every `b != a^*`; then `G(e)` also chooses `a^*`.

Fix `b != a^*`. Choose `k <= T_{a^*}` with `f_{a^*}(k) = e_{a^*}(T_{a^*})`, taking `k = T_{a^*}` if `f_{a^*}(T_{a^*}) = e_{a^*}(T_{a^*})` and otherwise any `k < T_{a^*}` attaining the minimum.

Case 1: `k = T_{a^*}`. By the greedy choice at step `t`, `(f_{a^*}(T_{a^*}), a^*) > (f_b(T_b), b)`. Since `e_b(T_b) <= f_b(T_b)`, we get `e_b(T_b) <= f_b(T_b) <= f_{a^*}(T_{a^*}) = e_{a^*}(T_{a^*})`, and if `e_b(T_b) = e_{a^*}(T_{a^*})` then `f_b(T_b) = f_{a^*}(T_{a^*})`, so the greedy choice forces `a^* succ b`. Hence `(e_{a^*}(T_{a^*}), a^*) > (e_b(T_b), b)`.

Case 2: `k < T_{a^*}`. Arm `a^*` was pulled at count `k` at some earlier step `s < t` (this is a fact about the run of `G(f)`, which by the induction hypothesis is also the run of `G(e)` up to step `t - 1`). At step `s` the greedy rule gives `(f_{a^*}(k), a^*) > (f_b(T_b(s-1)), b)`. Counts are nondecreasing, so `T_b(s-1) <= T_b(t-1) = T_b`, hence `e_b(T_b) <= f_b(T_b(s-1)) <= f_{a^*}(k) = e_{a^*}(T_{a^*})`. If equality `e_b(T_b) = e_{a^*}(T_{a^*})` holds, then `f_b(T_b(s-1)) = f_{a^*}(k)` and the greedy choice at step `s` forces `a^* succ b`. Hence `(e_{a^*}(T_{a^*}), a^*) > (e_b(T_b), b)`.

In both cases `G(e)` picks `a^*` at step `t`, so the runs agree at step `t`. The base case `t = 1` is Case 1 with all counts zero. QED.

### Lemma B.2 (sorted-order characterization for nonincreasing sequences)

Assume every `e_a` is nonincreasing in `k`. For `v in V`, `j in [K]` and `a != j` define `N_a(v, j) := #{k' >= 0 : (e_a(k'), a) > (v, j)}` (possibly infinite). Then for every `j` and `k >= 1`, the step `tau_j(k)` at which `G(e)` pulls arm `j` for the `k`-th time satisfies
`tau_j(k) = k + sum_{a != j} N_a(e_j(k-1), j)`,
with the convention that `tau_j(k) = +inf` (the `k`-th pull never happens) iff the right side is infinite.

Proof. (a) The pulled pairs `(e_{I_t}(T_{I_t}(t-1)), I_t)` are nonincreasing in `t`: after a pull of arm `a` its next pair is `(e_a(T_a + 1), a) <= (e_a(T_a), a)` because `e_a` is nonincreasing, and every other arm's pair was already below the pulled pair.

(b) Write `v := e_j(k-1)`. Suppose arm `j` is pulled for the `k`-th time at step `tau`. Every pull of an arm `a != j` before step `tau` has pair `>= (v, j)` by (a), hence `> (v, j)` because distinct arms give distinct pairs; so at most `N_a(v, j)` pulls of arm `a` precede step `tau`. Conversely, if `(e_a(k'), a) > (v, j)` and arm `a` had been pulled at most `k'` times before step `tau`, then at step `tau` arm `a`'s current pair is `(e_a(T_a), a) >= (e_a(k'), a) > (v, j)` (nonincreasing), contradicting the greedy choice of `j`. So exactly `N_a(v, j)` pulls of each `a != j` precede step `tau`, and exactly `k - 1` pulls of `j` do; therefore `tau = k + sum_{a != j} N_a(v, j)`. (c) If some `N_a(v, j) = +inf`, then at every step at which `T_j = k - 1`, arm `a` has a current pair `> (v, j) = (e_j(k-1), j)` by the same argument, so arm `j` is never pulled a `k`-th time. (d) If all `N_a(v, j)` are finite, then while `T_j <= k - 1` arm `j`'s current pair is `>= (v, j)`, so any pull of `a != j` consumes one of the `N_a(v, j)` pairs above `(v, j)`; after at most `sum_a N_a(v, j)` such pulls arm `j` is pulled, and the `k`-th pull of `j` occurs. QED.

### Theorem B.3 (static race monotonicity, Claim L1)

Let `(f_a)_{a in [K]}` be arbitrary, `succ` a fixed strict priority, and `f_1'(k) >= f_1(k)` for every `k >= 0`, with `f_a' = f_a` for `a != 1`. Let `T_a(t)` and `T_a'(t)` be the counts of `G(f)` and `G(f')`. Then for every `j != 1` and every step `t >= 1`,
`T_j'(t) <= T_j(t)`, and consequently `T_1'(t) >= T_1(t)`.

Proof. By Lemma B.1, `G(f) = G(e)` and `G(f') = G(e')`, where `e_1'(k) = min_{k' <= k} f_1'(k') >= min_{k' <= k} f_1(k') = e_1(k)` and `e_a' = e_a` for `a != 1`. All envelopes are nonincreasing, so Lemma B.2 applies to both merges. For `j != 1`, `k >= 1`, `v = e_j(k-1)`: `N_a'(v, j) = N_a(v, j)` for `a notin {1, j}`, and `N_1'(v, j) >= N_1(v, j)` because `(e_1'(k'), 1) >= (e_1(k'), 1) > (v, j)` whenever `(e_1(k'), 1) > (v, j)`. Hence `tau_j'(k) >= tau_j(k)` for every `k` (including the infinite case), and `T_j'(t) = #{k >= 1 : tau_j'(k) <= t} <= #{k >= 1 : tau_j(k) <= t} = T_j(t)`. Finally `T_1'(t) = t - sum_{j != 1} T_j'(t) >= t - sum_{j != 1} T_j(t) = T_1(t)`. QED.

Remark (K = 2). For two arms the theorem has a two-line proof: at the first step `t` with `T_1'(t) < T_1(t)` both runs are in the same state at the start of step `t`, the base pulls arm 1, so `(f_1(k), 1) > (f_2(l), 2)`, hence `(f_1'(k), 1) > (f_2(l), 2)` and the raised run also pulls arm 1, a contradiction. For `K >= 3` the states of the two runs diverge and the envelope reduction is needed.

Remark (structure). The proof shows more than the count inequality: the sequence of non-1 pulls (arm labels in order) of `G(f')` is a prefix of that of `G(f)` at every time, because both equal the sorted enumeration of the non-1 pairs `(e_a(k), a)`, `a != 1`, and raising arm 1 only moves arm-1 pairs earlier in that enumeration. This "prefix property" is the form in which the prior literature states the result (Section H).

### Corollary B.4 (known-horizon UCB with one ex ante priority is pathwise monotone)

Fix `K`, `n`, a deterministic nonnegative bonus function `beta(k)` (for example `beta(k) = sqrt(c log n / k)` for any `c > 0`; only the horizon `n` and the own count `k` may enter), and a priority permutation `pi` of `[K]`. The policy UCB(`beta`, `pi`): at each round, if some arm has count zero pull the `pi`-first such arm; otherwise pull the arm maximizing `hat m_a(T_a) + beta(T_a)`, ties broken by `pi`. Let the reward tapes be `y_a = (y_{a,1}, ..., y_{a,n}) in [0,1]^n`, indexed by the arm's own pull count, and `hat m_a(k) = k^{-1} sum_{r <= k} y_{a,r}`. If `y_1' >= y_1` coordinatewise and `y_a' = y_a` for `a != 1`, then `T_j'(t) <= T_j(t)` for every `j != 1` and `t <= n`, and `T_1'(t) >= T_1(t)`.

Proof. UCB(`beta`, `pi`) is the greedy merge with `f_a(0) = +inf` and `f_a(k) = hat m_a(k) + beta(k)` for `k >= 1`, with priority `pi`. Coordinatewise `y_1' >= y_1` gives `hat m_1'(k) >= hat m_1(k)` for every `k`, hence `f_1' >= f_1` pointwise. Apply Theorem B.3. QED.

Corollary B.5 (coupling form, scalar fixed means). Let `U_{a,r}`, `a in [K]`, `r <= n`, be independent uniforms, `pi` an independent uniform permutation, and for fixed means `m_a in [0,1]` put `Y_{a,r} = 1{U_{a,r} <= m_a}`. Replace `m_1` by any `M_1 >= m_1`. Then on every sample point, for every `j != 1` and every `t <= n`, `T_j(t; M_1, m_{-1}) <= T_j(t; m_1, m_{-1})` and `T_1(t; M_1, m_{-1}) >= T_1(t; m_1, m_{-1})`. In particular `E T_j(n; M_1, m_{-1}) <= E T_j(n; m_1, m_{-1})` with zero remainder, uniformly over all means and horizons.

Hypotheses made explicit. (i) The index of arm `a` at count `k` is a function of `(k, y_{a,1..k}, n)` only, nondecreasing in the reward prefix; it may be non-monotone in `k`, and `+inf` or `-inf` are allowed. (ii) One priority permutation is used for initialization and all ties for the entire instance; a uniform ex ante draw is covered by conditioning. (iii) Reward seeds are indexed by the arm's own pull count. (iv) The quantifier is: for every sample point, for every `t <= n` simultaneously.

## C. Per-round independent uniform tie-breaking (the manuscript's rule)

### C.1 Pathwise monotonicity FAILS under per-round coins (explicit tape)

Rule: initialization in a fixed order (labels 1, 2, 3), then index `hat m_a + sqrt(log n / T_a)` (`c = 1`), `n = 8`, `K = 3`; at a round with a tie, a fresh permutation `pi_t` indexed by the global round decides. Coupling: same tapes (local-count indexed), same coin table `(pi_t)_t` in both runs.

Tapes (local pull index 1 to 8): base arm 1 `(0,0,0,0,0,0,0,0)`; arm 2 `(0,1,1,1,1,1,1,1)`; arm 3 `(0,0,0,0,0,0,0,0)`. Raised arm 1 `(1,0,0,0,0,0,0,0)`, coordinatewise at or above base. Coins: `pi_4` ranks `2 succ 3 succ 1`; `pi_6` ranks `3 succ 2 succ 1`; all other rounds irrelevant. Constants: `B(1) = sqrt(log 8) = 1.4421`, `B(2) = 1.0197`, `B(3) = 0.8326`.

Base run: rounds 1 to 3 initialize (rewards 0, 0, 0). Round 4: all three indices equal `1.4421`; `pi_4` picks arm 2 (reward 1). Round 5: arm 2 has `1/2 + 1.0197 = 1.5197 > 1.4421`, pulled (reward 1). Round 6: arm 2 has `2/3 + 0.8326 = 1.4992 > 1.4421`, pulled. Counts after round 6: `(1, 4, 1)`; in particular `T_3(6) = 1`.

Raised run: rounds 1 to 3 initialize (rewards 1, 0, 0). Round 4: arm 1 has `1 + 1.4421`, pulled (reward 0). Round 5: arm 1 has `1/2 + 1.0197 = 1.5197 > 1.4421`, pulled (reward 0). Round 6: arm 1 has `1/3 + 0.8326 = 1.1659 < 1.4421`; arms 2 and 3 tie at `1.4421`; `pi_6` picks arm 3. Counts after round 6: `(3, 1, 2)`, so `T_3'(6) = 2 > T_3(6) = 1`.

Verified by `ucb_attack.py` (function `hand_example`): base history `[1,2,3,2,2,2,2,2]`, raised history `[1,2,3,1,1,3,2,2]` (labels shifted by one in the code). With the same tapes and a fixed priority `1 succ 2 succ 3` both runs are monotone (base `[1,2,3,1,2,2,2,2]`, raised `[1,2,3,1,1,2,2,2]`). Random search (`ucb_attack.py`, mode `perround`) finds violations in 314 of 200000 instances, including `K = 3` and `K = 4`.

Mechanism: the raised run delays the tie between arms 2 and 3 from round 4 to round 6, where a different coin applies. Any coupling that indexes tie coins by the global round, by the full count vector, or by (tied set, counts of the tied arms) suffers the same failure, because the tie situations of the two runs differ.

### C.2 Exact EXPECTED monotonicity HOLDS under per-round coins (Theorem C.1)

Theorem C.1. Let `(f_a)` be arbitrary sequences with values in a totally ordered set, `f_1' >= f_1` pointwise, `f_a' = f_a` for `a != 1`. Consider the randomized greedy merge in which at each step the pulled arm is uniform on the set of arms attaining `max_a f_a(T_a)`, using coins independent across steps. Then for every `j != 1` and every `t >= 1`, `E T_j'(t) <= E T_j(t)` and `E T_1'(t) >= E T_1(t)`, where the expectations are over the tie coins only. Moreover there exists a coupling of the two randomized runs (depending on the identity of the raised arm) under which `T_j'(t) <= T_j(t)` for all `j != 1` and all `t` simultaneously on every sample point.

Proof. Step 1 (two-stage coin representation). Let `(xi_l)_{l >= 1}` and `(eta_t)_{t >= 1}` be independent uniform `[0,1]` variables. Run the process as follows. At step `t`, let `S_t` be the tied set and `L_t` the number of pulls of arms other than 1 before step `t`. If `1 notin S_t`, pull the arm of `S_t` selected by `xi_{L_t + 1}` (say the `ceil(xi |S_t|)`-th element of `S_t` in label order). If `S_t = {1}`, pull arm 1. If `1 in S_t` and `|S_t| >= 2`: pull arm 1 if `eta_t <= 1/|S_t|`, otherwise pull the arm of `S_t \ {1}` selected by `xi_{L_t + 1}`. Given the past, the pulled arm is uniform on `S_t`: the coin `xi_{L_t+1}` has not been consumed by any earlier step (it is consumed exactly at the `(L_t + 1)`-th non-1 pull) and `eta_t` is fresh, so the conditional law is `1/|S_t|` on each element. Hence this process has the law of the per-round uniform tie-breaking merge.

Step 2 (the non-1 pull sequence is a function of the `xi` coins only). Let `sigma_l` be the arm pulled at the `l`-th non-1 pull, and let `R_l := (T_a)_{a != 1}` be the non-1 count vector after `l - 1` non-1 pulls, which is a function of `sigma_1, ..., sigma_{l-1}`. Let `A_l := argmax_{a != 1} f_a(T_a)` evaluated at `R_l` and `g(l) := max_{a != 1} f_a(T_a)` at `R_l`. At the step of the `l`-th non-1 pull, the tied set minus arm 1 is exactly `A_l` (arm 1 is either tied or strictly below the non-1 maximum at that step, otherwise no non-1 pull would occur), and the pulled arm is the `xi_l`-selection from `A_l`. Therefore `(sigma_l)_l` is a deterministic function of `(xi_l)_l` and of the sequences `(f_a)_{a != 1}`, which are the same in both runs. Under the coupling that uses the same `(xi_l)` and the same `(eta_t)` in both runs, `sigma' = sigma` on every sample point, and hence `A_l' = A_l`, `g'(l) = g(l)` for every `l`.

Step 3 (arm 1 against the aggregate). Given `sigma`, both runs are two-arm races between arm 1 (sequence `f_1` or `f_1'`) and the aggregate arm with sequence `g`, in which a tie at aggregate count `l` is resolved in favor of arm 1 iff `eta_t <= 1/(|A_l| + 1)`. Let `t` be the first step with `T_1'(t) < T_1(t)`, if any. Then `T_1'(t-1) = T_1(t-1) =: k` (as in Remark K = 2 of Section B) and both runs have made `l = t - 1 - k` non-1 pulls, so they are in the same joint state at the start of step `t`, with the same `g(l)`, `|A_l|` and coin `eta_t`. The base run pulls arm 1 at step `t`, so either `f_1(k) > g(l)`, or `f_1(k) = g(l)` and `eta_t <= 1/(|A_l| + 1)`. Since `f_1'(k) >= f_1(k)`, in the first case `f_1'(k) > g(l)`, and in the second case either `f_1'(k) > g(l)` or `f_1'(k) = g(l)` with the same coin outcome; in every case the raised run pulls arm 1 at step `t`, a contradiction. Hence `T_1'(t) >= T_1(t)` for all `t` on every sample point of the coupling.

Step 4 (conclusion). `T_j(t) = #{l <= t - T_1(t) : sigma_l = j}` and `T_j'(t) = #{l <= t - T_1'(t) : sigma_l = j}` with the same `sigma` and `t - T_1'(t) <= t - T_1(t)`, so `T_j'(t) <= T_j(t)` on every sample point of the coupling. Each run has the correct marginal law by Step 1, so `E T_j'(t) <= E T_j(t)`. QED.

Corollary C.2 (known-horizon UCB with the manuscript's tie rule). Symmetric UCB with index `hat m_a + sqrt(c log n / T_a)`, initialization in a uniform random order (law-equivalent to per-round uniform choice among unseen arms, i.e. to `f_a(0) = +inf` in Theorem C.1) and independent uniform tie-breaking each round satisfies, for fixed means and the tape coupling of Corollary B.5, `E T_j(t; M_1, m_{-1}) <= E T_j(t; m_1, m_{-1})` for every `j != 1` and `t <= n`, with zero remainder, uniformly over means and horizons; and `E T_1` weakly increases. Proof: condition on the tapes; for fixed tapes the index sequences are fixed and `f_1' >= f_1` pointwise; apply Theorem C.1 and integrate. The pathwise statement under the same-round-coin coupling is false by C.1.

Numerical confirmation: `expected_mono_dp.py` and `expected_mono_dp2.py` compute exact expectations by dynamic programming over `(count, sum)` states (1700 instances, `K in {2,3}`, `n <= 11`, `c in {0.1,...,2}`, means on a grid of step `0.1`): 0 violations for per-round coins and 0 for the fixed-priority average. `race_perround_expected.py` (static race, fixed sequences, exact expectation over coins, 30000 instances): 0 violations.

## D. Anytime UCB1 (log t): verification of Claim L3

Replication (`ucb_attack.py`, function `l3_trace`; index `hat m + sqrt(2 log t / T)`, initialization in label order, ties to the lowest label, tapes exactly as in Claim L3). Base history `[1,2,3,3,3,3,3,1]`, counts `(2,1,5)`; raised history `[1,2,3,1,3,3,3,2]`, counts `(2,2,4)`. Round-by-round indices agree with the lead's numbers to four decimals: base round 4 `(1.6651, 1.6651, 2.6651)` pull 3; base round 8 `(2.0393, 2.0393, 1.9120)` pull 1 by tie; raised round 4 `(2.6651, 1.6651, 2.6651)` pull 1 by tie; raised round 8 `(1.9420, 2.0393, 2.0197)` pull 2. VERIFIED: arm 2's count rises from 1 to 2 when arm 1's tape is raised. Since label-order initialization and these tie outcomes have positive probability under the manuscript's rule, the manuscript's UCB1 is not pathwise monotone under the local-count tape coupling.

Mechanism. The anytime index of arm `a` at local count `k` is `hat m_a(k) + sqrt(2 log t / k)`, which depends on the global round `t`. Raising arm 1 pulls it earlier (round 4 instead of round 8), which pushes arm 3's pulls one round later; arm 3's local count 5 is then reached at round 8 instead of round 7, at a larger `log t`, but more importantly the comparison between arms 2 and 1 at round 8 happens at counts `(2, 1)` in the raised run instead of `(1, 1)`. The index sequences are no longer fixed functions of the own count, so Theorem B.3 does not apply. On the same tapes, the known-horizon index with `c = 2` and the same fixed priority is monotone (base counts `(2,2,4)`, raised `(2,2,4)`), as Corollary B.4 guarantees.

What this does and does not say about `thm:scalar-ucb`. The theorem claims expected monotonicity with an `o(n)` remainder, pointwise in the two fixed profiles, proved from the fixed-gap bound and exchangeability; L3 does not contradict it. L3 shows only that the stronger pathwise statement is false for the anytime index, so any pathwise or zero-remainder claim for the manuscript's rule would be wrong. Whether anytime UCB1 is exactly expectation-monotone is OPEN: `anytime_expected_dp.py` (exact dynamic programming, 1200 instances, `K in {2,3}`, `n <= 12`, per-round uniform ties and uniform initialization order) found no violation, but the proof technique of Sections B and C is unavailable because the index depends on `t`, and I have neither a proof nor a counterexample. If the paper wants an exact statement, the known-horizon index is the safe choice.

## E. Behavioral extension (blind own-history-dependent strategies)

Coupling. Fix `n`, the index `hat m + beta(T)` of Corollary B.4, and either tie rule. For each agent `a` let `omega_a` be its private randomness and `U_{a,1}, U_{a,2}, ...` its reward seeds indexed by its own pull count; all of these and the platform's coins are independent. A blind behavioral strategy `S_a` is a sequence of measurable maps `g_{a,k}` from (own past rewards `Y_{a,1..k-1}`, own past targets, `omega_a`, `n`) to a target `m_{a,k} in [0, M_a]`; the agent observes no global round, no other agent's data and (under UCB) no mechanism message. The reward at its `k`-th pull is `Y_{a,k} = 1{U_{a,k} <= m_{a,k}}`.

Proposition E.1. Under this coupling, for every profile `S_{-1}` of blind behavioral strategies of the other agents and every blind behavioral strategy `S_1` of agent 1:
(a) with one ex ante priority, `T_j(t; M_1, S_{-1}) <= T_j(t; S_1, S_{-1})` for every `j != 1` and `t <= n` on every sample point, and `T_1` weakly increases;
(b) with per-round uniform tie-breaking, the same inequalities hold in expectation (over the platform's coins), for every fixed realization of `(omega_a, U_a)_a`.

Proof. Because agent `a` is blind, its `k`-th target is `m_{a,k} = g_{a,k}(Y_{a,1..k-1}, past targets, omega_a, n)`, and by induction on `k` the pair `(m_{a,k}, Y_{a,k})` is a function of `(U_{a,1..k}, omega_a, n)` alone, independent of the rounds at which the pulls occur and of the other agents. Hence each agent's reward tape `(Y_{a,k})_k` is fixed once `(U_a, omega_a)` is fixed, and the index sequence `f_a(k) = hat m_a(k) + beta(k)` is a fixed function of the own count. Under `S_1`, feasibility gives `m_{1,k} <= M_1`, so `1{U_{1,k} <= m_{1,k}} <= 1{U_{1,k} <= M_1}`: the tape of agent 1 under the constant strategy `M_1` dominates its tape under `S_1` coordinatewise, on the same seeds. Apply Corollary B.4 for (a) and Theorem C.1 (conditional on the tapes) for (b). QED.

Two caveats that are essential. (1) The comparison must be against a strategy whose realized target sequence dominates on the coupled path; the constant `M_1` (or any constant `M >= sup m_{1,k}`) qualifies. "Raising" a behavioral strategy history by history (`g'_{1,k} >= g_{1,k}` at every history) does NOT give coordinatewise tape dominance: with `g_1(empty) = 0.1`, `g_1((0)) = 0.9`, `g_1((1)) = 0.1` and `g_1' = max(g_1, 0.5)`, seeds `U_{1,1} = 0.3`, `U_{1,2} = 0.5` give base tape `(0, 1)` and raised tape `(1, 0)`, so the lemma does not apply and no monotonicity claim is made for such pairs. (2) If the other agents observe the global round or any information that differs between the two coupled runs (for example mechanism messages in MESP, or the full context profile in the contextual model, Section F(iv)), their tapes are no longer fixed and the proposition fails.

