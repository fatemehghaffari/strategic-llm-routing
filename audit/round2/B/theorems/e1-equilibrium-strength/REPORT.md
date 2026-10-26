# Track E1: how strong is the equilibrium of MESP

Worker notes, 18 September 2026. Output directory `audit/round2/B/theorems/e1-equilibrium-strength/`.
No canonical file was modified. Sources read in full before any claim below: `audit/round2/prompts/COMMON.md`,
`sections/Private_information_setting.tex`, `sections/appendix_private.tex`, `sections/setting.tex`,
`audit/round2/B/PRIVATE_BOUND_NOTES.md`, `audit/round2/B/CONTEXT_PROOF_CONTRACT.md`, `audit/round2/BASELINE.md`,
`scratch/experiments/round2/exploitability/dp.py`,
`scratch/experiments/round2/common/{design.py,instances.py,instances.json}`.

## 0. One-paragraph answer

The concern in the brief is real but it is not the mutual-underbidding equilibrium the brief expected, and the
mechanism that produces it is sharper. Underbidding by everyone is never an equilibrium here, because a
selection is worth `1 + mu_i - tau >= 1 - M_top > 0` per round to the agent that gets it, so a low price makes
winning more attractive, not less, and any agent that can outbid the winner does so for a linear gain. What is
unpinned is not the winner's bid but the LOSING bid, and the price is the losing bid. An agent that cannot
outbid the winner receives nothing in Stage 2 whatever it bids, so its entire stake in its own bid is the
Stage-1 effort `L_n (M_k - c_k) = O(n^{2/3} (log n)^{1/3})`, which is inside the `o(n)` slack of the paper's own
equilibrium notion. Consequently, WHENEVER THE TOP CAPACITY IS UNIQUE, MESP has a continuum of additive
behavioral equilibria, all with exactly the deviation bound the paper proves for `S^star`, whose revenue takes
every value in `[mu_H^star, M_(2)] n` up to `O(n^{2/3} (log n)^{1/3})` (assuming `mu_H^star <= M_(2)`, the case
in which the claim `M_(2) n` says anything; Corollary E1.1 has the general form); the worst of them sits exactly on the
honest-benchmark floor that the paper already proves against arbitrary play, so the `M_(2) n` revenue claim
buys nothing at the worst equilibrium. WHENEVER TWO AGENTS TIE AT THE TOP CAPACITY, the price setter is itself
a possible winner, its bid is backed by a linear stake, and every equilibrium in the family has revenue
`M_(2) n - o(n)`; the same dichotomy governs resistance to pairs. The two-top condition that the paper already
assumes for its public theorem (`sections/Public_information_setting.tex` line 3, `sections/appendix_public.tex`
line 18) is therefore exactly the condition under which the private mechanism's revenue guarantee survives
equilibrium selection and collusion. This is a limitation of the headline result, not an error in it: the
manuscript states at `sections/Private_information_setting.tex` line 66 that the theorem "does not assert high
revenue in every equilibrium" and at `sections/appendix_private.tex` line 201 that "a price-setting agent may
lower off-equilibrium revenue without obtaining a linear utility gain". Those two sentences are correct and
are, as far as I can tell, the whole of what the paper says about the question; what is new here is the exact
characterization, the exact worst-case revenue, the tie to the two-top condition, the coalition statement, and
a repair with its cost.

## 1. Notation and standing conventions

All notation is the manuscript's. `L_n, N_n, s_n, b_n(.)`, the price `tau = (beta_(2) - s_n)_+`, the monitor
`Z_r < r tau - b_n(r)`, the fallback `R_K(H) = 3 sqrt(K H log K) + 2 K log K` and the proposed profile `S^star`
are as in `sections/Private_information_setting.tex` lines 10 to 19 and 33. `V_i = max_{j != i} M_j`,
`M_top = max_i M_i`, `M_(2)` = second largest capacity counting ties, `K_top = |{i : M_i = M_top}|`,
`mu_H^star = max_{h in K_H} mu_h`, `M_(3)` = third largest capacity counting ties (`M_(3) := 0` if `K = 2`).
Per-pull utility is `1 + mu_i - m in [0, 2]`; `B_{i,n}` is the behavioral class of `sections/setting.tex`.
"Additive equilibrium" always means the manuscript's additive behavioral asymptotic equilibrium:
`sup_{S'_{i,n} in B_{i,n}} [u_i(n; S'_{i,n}, S_{-i,n}) - u_i(n; S_n)] = o(n)` for every `i`.

Throughout I use the manuscript's three lemmas as given and prove nothing about them:
`lem:private-monitor` (anytime monitor: `Pr{exists r <= n : |Z_r - A_r| > b_n(r)} <= n^{-3}`; a tenure of `q`
pulls has `U^pri <= q(1 + mu_i - tau) + 1 + 2 b_n(q)` on the complement; false-switch probability at most
`(2n^3)^{-1}` when every primary target is at least `tau`), `lem:selected-reactive-exp3` (fallback reward at
least `v H - R_K(H)` against a comparator of selected mean at least `v`), and the Stage-1 coupling
`beta'_i <= beta_i^max` with the price `tau_i = (max_{j != i} beta_j - s_n)_+` independent of `i`'s own bid
(`sections/appendix_private.tex`, subsection "Bidding coupling and fallback utility"). The revised top-agent
accounting of `audit/round2/B/PRIVATE_BOUND_NOTES.md` Note 1 (deletion of the `2 n s_n` term) is used and is
what makes the constants below match the manuscript's exactly; nothing here depends on that deletion
qualitatively.

NONDEGENERACY (ND): `M_top < 1`. Write `kappa := 1 - M_top > 0`. (ND) is used only to guarantee that a
selection is worth a bounded-away-from-zero amount: every feasible target `m <= M_top` gives per-pull utility
`1 + mu_i - m >= kappa`. The knife edge `M_top = 1` with `mu_i = 0` is discussed in Section 5.4; it is the only
case in which winning can be worthless and the characterization degenerates.

THE BID FAMILY. Call `c = (c_1, ..., c_K)` a feasible bid vector if `c_i in [0, M_i]` for every `i` and
`c_h >= mu_h` for every honest `h`. Let `S^c` be the profile that agrees with `S^star` everywhere except in
Stage 1, where agent `i` delivers the constant target `c_i` on each of its `L_n` bidding pulls:

- Stage 1: target `c_i`;
- primary phase: the winner delivers `min{tau, M_i}`, or `max{mu_i, min{tau, M_i}}` if honest;
- fallback: every agent delivers its capacity `M_i`.

`S^c` lies in `B_{i,n}^K` and is feasible on every history, exactly as `S^star = S^M` is. Let
`Sigma := {S^c : c feasible}`. This is the family in which the mutual-underbidding question lives: it varies
precisely the quantity that sets the price and leaves everything the manuscript proves about the monitor and
the fallback untouched. Deviations are never restricted to `Sigma`: every deviation below ranges over the full
behavioral class `B_{i,n}`, including adaptive Stage-1 targets, bait and switch, and arbitrary fallback play.

## 2. Theorem E1: the equilibrium set of MESP inside the bid family

THEOREM E1. Assume (ND) and fix a feasible bid vector `c` that does not depend on `n`. Then `S^c` is an
additive behavioral asymptotic equilibrium of MESP if and only if one of the following holds.

(A) There is an agent `W` with `c_W > V_W`. (Then necessarily `M_W > V_W`, so `K_top = 1`, `W` is the unique
top agent, `V_W = M_(2)`, and `c_W in (M_(2), M_top]`. The other `K - 1` bids are unrestricted.)

(B) `K_top >= 2` and `c_i = M_top` for every `i` in `K_top`. (The bids of non-top agents are unrestricted.)

In case (A) the deviation bound is the manuscript's own: for every agent `i`,

  `sup_{S'_{i,n} in B_{i,n}} [u_i(n; S'_{i,n}, S^c_{-i,n}) - u_i(n; S^c_n)] <= L_n + 2 b_n(n) + R_K(n) + O(1)`,

and the revenue is

  `P(n; S^c) = nu(c) n + O(K L_n + n s_n)`,  `nu(c) := max{ bar c, mu_W 1{W honest} }`,  `bar c := max_{k != W} c_k`.

In case (B), `P(n; S^c) >= M_(2) n - O(K L_n + n s_n + R_K(n))`, the manuscript's revenue rate.

(ND) is used only in the "only if" direction. The "if" direction, which is the negative result, needs no
condition beyond feasibility of `c`.

COROLLARY E1.1 (the revenue range of the equilibrium set). Assume (ND).
If `K_top >= 2`, every equilibrium in `Sigma` has revenue `M_(2) n - O(n^{2/3} (log n)^{1/3})`.
If `K_top = 1`, the set of equilibrium revenues in `Sigma` is exactly
`{ v n + O(n^{2/3} (log n)^{1/3}) : v in [mu_H^star, max{mu_H^star, M_(2)}] }`.
In particular the smallest equilibrium revenue is `mu_H^star n + O(n^{2/3} (log n)^{1/3})`, it is attained, and
it coincides with the bound that the robustness part of `thm:private-mesp` already proves against arbitrary
behavioral play. The gap between the paper's equilibrium revenue and the worst equilibrium revenue is
`(M_(2) - mu_H^star)_+ n`, linear whenever the best honest intrinsic mean is below the runner-up capacity.

COROLLARY E1.2 (the proposed profile is not selected by anyone's interest). Assume `K_top = 1` and let `k` be
an agent with `M_k = M_(2)`, the agent whose bid sets the price at `S^star`. Lowering only `c_k`, from `M_(2)`
to any feasible `c_k' < M_(2)`, raises `k`'s own utility by exactly `L_n (M_(2) - c_k') - O(n^{-2})` and lowers
platform revenue by `(M_(2) - c_k') n - O(K L_n + n s_n)`. So the move from the proposed profile to the worst
equilibrium is a sequence of strictly improving unilateral moves, not a coordinated one.

REMARK (the sharpest form of the witness, and what it presumes). Case (A) is satisfied by `c_W = M_W`, so the
family contains the profile in which THE WINNER PLAYS EXACTLY `S^star` and only the losing agents underbid.
The revenue claim therefore fails without the proposed winner deviating at all: on `unique_top` at
`n = 10000`, the profile `(M_1, 0, M_3)` is an additive equilibrium with revenue `0.3134` per round against
`0.5533` at `S^star` (Section 8.4). Like every equilibrium statement, the construction presumes the agents know
the game: a loser lowers its bid only if it knows it cannot win, since lowering a bid that would have won costs
a linear amount. That knowledge requirement falls on the losers, not on the winner, and it is the same
knowledge the manuscript's own deviations presume, since the supremum in `thm:private-mesp` is over strategies
that may depend on the instance.

Corollary E1.2 is the same computation as the manuscript's own `prop:tightness`
(`sections/appendix_private.tex`, "The bidding term is attained"), applied to the runner-up instead of to the
winner; the runner-up's version is cleaner, because the runner-up's post-bid histories are unaffected by its
own bid on the good event, so no coupling of the post-bid phase is needed.

### 2.1 Proof of Theorem E1, sufficiency

Let `G_A := {|beta_j - c_j| <= s_n for all j in A}` for a set `A` of agents that play `S^c`. Hoeffding's
inequality with `exp(-2 L_n s_n^2) = (2 K n^4)^{-1}` and a union bound over `|A| <= K` give
`Pr(G_A^c) <= n^{-4}`. This is the manuscript's own good event with `c` in place of `M`; no other property of
`c` is used.

CASE (A). Let `W` be the agent with `Delta := c_W - V_W > 0`, and let `bar c := max_{k != W} c_k <= V_W`, so
`c_W - bar c >= Delta`. Take `n` large enough that `2 s_n < Delta` (this depends on the instance and on `c`
only, and `s_n -> 0`).

Deviation by a loser. Fix `k != W` and `S'_k in B_{k,n}`. Couple the deviating Stage-1 rewards to
capacity-target rewards by the manuscript's uniform coupling, so `beta'_k <= beta_k^max` pathwise, and let
`E := G_{[K] minus {k}} intersect {beta_k^max <= M_k + s_n}`, an event of probability at least `1 - 2 n^{-4}`
whose description does not involve `S'_k`. On `E`,

  `beta'_k <= M_k + s_n <= V_W + s_n < c_W - s_n <= beta_W`,

so `k` loses the bidding. Also on `E`, `beta_(2) = max_{j != W} beta_j <= V_W + s_n`, hence `tau <= V_W < M_W`,
so `W`'s primary target `min{tau, M_W} = tau` (or `max{mu_W, tau}` if honest) is at least `tau`, and the last
claim of `lem:private-monitor` bounds the probability of any switch by `(2 n^3)^{-1}`. A losing agent is never
selected in the primary phase, so on `E` and on the no-switch event its post-bid utility is `0`. Since per-pull
utility is at most `2` and at most `n` pulls occur, its expected post-bid utility under the deviation is at
most `2 n (2 n^{-4} + (2 n^3)^{-1}) <= 2 n^{-2}` for `n >= 4`. Its deviating Stage-1 utility is at most
`L_n (1 + mu_k)` and its baseline Stage-1 utility is exactly `L_n (1 + mu_k - c_k)`, while its baseline
post-bid utility is nonnegative. Hence

  `u_k(n; S'_k, S^c_{-k}) - u_k(n; S^c) <= L_n c_k + 2 n^{-2} <= L_n + 2 n^{-2}`.

Deviation by the winner. Fix `S'_W in B_{W,n}`. The price `tau_W := (max_{j != W} beta_j - s_n)_+` is a
function of the other agents' Stage-1 rewards alone, hence identical in the deviating and the baseline
execution under the coupling; on `G_{-W} := G_{[K] minus {W}}`, `(bar c - 2 s_n)_+ <= tau_W <= bar c <= V_W < M_W`.
On the winning branch, `lem:private-monitor` at `tau = tau_W` gives primary utility at most
`q (1 + mu_W - tau_W) + 1 + 2 b_n(q)` outside an event of probability `n^{-3}`; the non-deviating agents deliver
their capacities in the fallback under `S^c` exactly as under `S^star`, so the comparator mean is `V_W` and
equation `private-fallback-top` gives
`E[U_W^fb | F_fb] <= (1 + mu_W - V_W) H + R_K(H) <= (1 + mu_W - tau_W) H + R_K(H)`, the last step by
`tau_W <= V_W` on `G_{-W}` (this is Note 1 of `PRIVATE_BOUND_NOTES.md`). With `H = N_n - q`, the deviating
post-bid utility is at most `(1 + mu_W - tau_W) N_n + 1 + 2 b_n(n) + R_K(n)`. On the losing branch the actual
winner `j` satisfies `tau <= (beta_j - s_n)_+ <= M_j` on `G_{-W}`, so it targets at least `tau`, the switch
probability is at most `(2 n^3)^{-1}`, and the deviator's post-bid utility is at most `2 n^{-2}`. In the
baseline, on `G_{[K]}`, `beta_W >= c_W - s_n > bar c + s_n >= max_{k != W} beta_k`, so `W` wins; its primary
targets are all at least `tau_W`, so a false switch has probability at most `(2 n^3)^{-1}` and costs at most
`2 N_n`; on the complement its post-bid utility is exactly `N_n (1 + mu_W - tau_W)` when `W` is strategic, and
the same when `W` is honest and `tau_W > mu_W`. When `W` is honest and `tau_W <= mu_W`, the baseline earns
exactly `1` per primary pull, which is the largest per-pull utility any honest strategy can earn, and any
deviation has at most `N_n` post-bid selections, so its post-bid gain is at most `2 N_n (2 n^3)^{-1}`.
Charging Stage 1 (at most `L_n c_W <= L_n`) and the bad events (at most `2 n (n^{-4} + n^{-3})`) gives

  `u_W(n; S'_W, S^c_{-W}) - u_W(n; S^c) <= L_n + 1 + 2 b_n(n) + R_K(n) + O(n^{-2})`.

Both bounds are `O(n^{2/3} (log n)^{1/3}) = o(n)`, so `S^c` is an additive equilibrium. This argument is the
manuscript's own equilibrium proof with `c` substituted for `M`; the only inputs that change are the centre of
the concentration event and the numerical value of `bar c`.

CASE (B). `K_top >= 2` and every top agent bids `M_top`. A non-top agent `k` has `M_k < M_top`, so on
`G_{[K] minus {k}} intersect {beta_k^max <= M_k + s_n}` it loses, and the loser computation above applies
verbatim with `V_W` replaced by `M_top`, giving gain at most `L_n + 2 n^{-2}`. A top agent `i` faces
`tau_i = (max_{j != i} beta_j - s_n)_+ in [(M_top - 2 s_n)_+, M_top]` on `G_{-i}` because another top agent
bids `M_top`; `tau_i <= M_top = M_i = V_i`, so the winner computation above applies verbatim and gives gain at
most `L_n + 1 + 2 b_n(n) + R_K(n) + O(n^{-2})`. (Case (B) with all non-top bids equal to capacity is exactly
`S^star`, so this reproves the manuscript's equilibrium claim as a special case.)

REVENUE. On `G_{[K]}` in case (A), `W` wins, `tau in [(bar c - 2 s_n)_+, bar c]`, the winner delivers
`nu := max{mu_W 1{W honest}, tau}` on every primary pull, and a switch has probability at most `(2 n^3)^{-1}`.
Stage-1 revenue is exactly `L_n sum_i c_i <= K L_n`, fallback revenue lies in `[0, n]`, and `Pr(G^c) <= n^{-4}`,
so `P(n; S^c) = nu(c) n + O(K L_n + n s_n + 1)`. In case (B) at least two bids concentrate at `M_top`, so
`tau >= M_top - 2 s_n = M_(2) - 2 s_n` on `G_{[K]}` and the manuscript's revenue proof applies unchanged.

### 2.2 Proof of Theorem E1, necessity

Assume (ND), let `c` be feasible and fixed, and suppose neither (A) nor (B) holds. Put `c^max := max_i c_i` and
`T := {i : c_i = c^max}`. In each case below I exhibit one agent and one deviation whose gain is at least a
fixed positive multiple of `n` for all large `n`, which contradicts the `o(n)` requirement. All deviations have
the same shape: deliver a constant `m'` on every Stage-1 pull, then follow `S^c_i`; so they lie in `B_{i,n}`
and are honest whenever the agent is honest, since `m' = M_i >= mu_i` in every case below. Two standing
estimates are used.

(E1) Winning value. If an agent `i` wins the bidding and on the good event faces `tau_i <= theta` with
`theta <= M_top` and `theta <= M_i`, then its primary target `min{tau_i, M_i} = tau_i`, all its primary targets
are at least `tau_i`, a switch has probability at most `(2 n^3)^{-1}`, and its post-bid utility is at least
`N_n (1 + mu_i - theta) - 2 N_n (2 n^3)^{-1}`, hence at least `N_n kappa - 1` by (ND); for an honest `i` the
same holds with `1 + mu_i - theta` replaced by `min{1, 1 + mu_i - theta} >= kappa`.

(E2) Losing value. If on the good event agent `i` loses the bidding and the actual winner `j` plays `S^c_j`
with `tau <= M_j`, its post-bid utility is at most `2 n^{-2}`, as computed in Section 2.1; its baseline utility
is then at most `L_n (1 + mu_i) + 2 n^{-2} <= 2 L_n + 1`.

CASE 1: `|T| = 1`, say `T = {W}`, and `c_W <= V_W` (so (A) fails). Let `k` attain `M_k = V_W`; then `k != W`
and `c_k < c^max = c_W`. Deviation for `k`: bid `M_k` throughout Stage 1.

- If `M_k > c_W`: for `n` with `2 s_n < M_k - c_W`, on the good event `k` outbids everyone and
  `tau_k = (max_{j != k} beta_j - s_n)_+ <= c_W <= V_W = M_k`, so (E1) applies with `theta = c_W`; by (E2) its
  baseline is at most `2 L_n + 1`. Its Stage-1 deviating utility is nonnegative. Hence the gain is at least
  `N_n kappa - 2 L_n - 2 - 4 n^{-3} >= (kappa/2) n - 2 L_n - 3`, and since `L_n = o(n)` this exceeds
  `(kappa/4) n` for all large `n`.
- If `M_k = c_W`: `beta_k` and `beta_W` are then i.i.d. `Bin(L_n, c_W)/L_n`, so by exchangeability and the
  mechanism's independent uniform priority `Pr(k beats W) = 1/2` exactly; intersecting with the good event for
  the other `K - 2` agents (probability at least `1 - n^{-4}`) leaves `k` winning with probability at least
  `1/2 - n^{-4}`, at a price `tau_k <= c_W = M_k`. (E1) and (E2) give a gain of at least
  `(1/2 - n^{-4}) (N_n kappa - 1) - 2 L_n - 2 >= (kappa/8) n` for all large `n`.

CASE 2: `|T| >= 2` at the common level `c^max`. Note first that each `j in T` wins with probability at most
`1/|T|`, because on the event that `j` wins it is in particular the largest of the `|T|` exchangeable bids
`{beta_l : l in T}` and ties are broken uniformly.

- (2a) Some `j in T` has `M_j > c^max`. Deviation for `j`: bid `M_j`. On the good event the deviation wins
  outright and faces `tau_j <= c^max <= M_j`, so by (E1) its post-bid utility is at least
  `N_n (1 + mu_j - c^max) - 1`. Its baseline post-bid utility is at most
  `(1/|T|) [N_n (1 + mu_j - tau_j) + 1 + 2 b_n(n) + R_K(n)] + 2 n^{-2}` by `lem:private-monitor`, the fallback
  bound and (E2), with `tau_j >= (c^max - 2 s_n)_+` on the good event, so
  `1 + mu_j - tau_j <= 1 + mu_j - c^max + 2 s_n`. Since `|T| >= 2` the gain is at least
  `(1/2) N_n (1 + mu_j - c^max) - N_n s_n - L_n - (1 + 2 b_n(n) + R_K(n)) - O(n^{-2})`, and
  `N_n s_n = O(n^{2/3} (log n)^{1/3})`, `b_n(n) + R_K(n) = O(sqrt(n log n))`, so the gain is at least
  `(kappa/8) n` for all large `n`.
- (2b) Every `j in T` has `M_j = c^max`, and some `k` outside `T` has `M_k > c^max`. Deviation for `k`: bid
  `M_k`; it wins outright on the good event at a price at most `c^max <= M_k`; by (E1) and (E2) the gain is at
  least `N_n kappa - 2 L_n - 3 >= (kappa/4) n` for large `n`.
- (2c) `M_i <= c^max` for every `i` and `M_j = c^max` for every `j in T`. Then `c^max = M_top` and
  `T subset K_top`. If some `k in K_top minus T`, then `c_k < M_top = M_k`; deviation for `k`: bid `M_top`. It
  then ties with the `|T|` members of `T`, so by exchangeability it wins with probability at least
  `1/(|T| + 1) - n^{-4} >= 1/K - n^{-4}`, at a price at most `M_top = M_k`; by (E1) and (E2) the gain is at
  least `(1/K) N_n kappa - 2 L_n - 3 >= kappa n /(4K)` for large `n`. Hence `K_top = T`, `|T| >= 2` and
  `c_i = M_top` on `K_top`, which is (B), contradicting the assumption that (B) fails.

This exhausts the cases, so a profile `S^c` that is an additive equilibrium satisfies (A) or (B). Q.E.D.

### 2.3 Proof of the corollaries

Corollary E1.1. Under (B), Section 2.1 gives the revenue bound. Under `K_top = 1` with unique top `W`, Theorem
E1 says the equilibria in `Sigma` are exactly the `c` with `c_W > M_(2)` and arbitrary other bids, and their
revenue is `nu(c) n + O(.)` with `nu(c) = max{bar c, mu_W 1{W honest}}` and `bar c = max_{k != W} c_k`. As
`c_{-W}` ranges over its feasible set, `bar c` ranges over the interval
`[max_{h in K_H, h != W} mu_h, M_(2)]`, with the convention that a maximum over the empty set is `0` (lower
endpoint: honest losers must bid at least `mu_h`, strategic losers may bid `0`; upper endpoint: some loser has
capacity `M_(2)`; intermediate values are attained by moving
that loser's bid, a continuous parameter). Hence `nu(c)` ranges over `[mu_H^star, max{mu_H^star, M_(2)}]`,
using `max{mu_W 1{W honest}, max_{h != W} mu_h} = mu_H^star`. The lower endpoint `mu_H^star` is attained, and
the robustness part of `thm:private-mesp` shows no profile whatever can go below it by more than
`O(K L_n + n s_n + b_n(n) + R_K(n))`.

Corollary E1.2. Let `K_top = 1`, `M_k = M_(2)`, and compare `S^c` and `S^{c'}` where `c` and `c'` differ only
in the `k`th coordinate, `c_k = M_(2) > c'_k`. Couple the two executions by the same reward uniforms indexed by
agent and local pull index, the same priority and the same EXP3 coins. On the event that every bid is within
`s_n` of its target in both executions (probability at least `1 - 2 n^{-4}`), `W` wins both and `k` is never
selected after Stage 1 in either, so `k`'s post-bid utility is `0` in both and its Stage-1 utilities differ by
exactly `L_n (M_(2) - c'_k)`. Off that event the difference is at most `2 n`, contributing `4 n^{-3}`. The
revenue statement is the revenue formula of Theorem E1 applied twice. Note that `k`'s gain does not depend on
whether `W` is honest and does not require any coordination with `W`.

## 3. What the characterization means, in one sentence each

1. THE PRICE IS SET BY AN AGENT WITH NO STAKE IN IT. The announced price is the highest losing bid, shaded. A
   loser receives nothing in the primary phase whatever it bids, so the only consequence of its bid for itself
   is the Stage-1 effort `L_n (M_k - c_k) = O(n^{2/3} (log n)^{1/3})`, inside the `o(n)` slack. Any equilibrium
   notion with slack `omega(L_n)` leaves the price free.
2. MUTUAL UNDERBIDDING IN THE USUAL SENSE DOES NOT OCCUR. A common low bid is never an equilibrium: at price
   `tau` a winner earns `1 + mu_i - tau >= kappa > 0` per round, so lowering the price raises the prize, and
   any agent that can outbid the current winner takes it for a linear gain (Case 2 of Section 2.2). The
   low-revenue equilibria are asymmetric: one agent bids above every other capacity and the rest bid low
   because they have already lost.
3. THE TWO-TOP CONDITION IS WHAT PINS THE PRICE. With `K_top >= 2` the price setter is itself a potential
   winner, its bid carries the linear stake `(1/K_top) N_n (1 + mu_i - M_top)`, and the price is forced to
   `M_top = M_(2)`. This is exactly the role the two-top condition plays in the public theorem
   (`sections/Public_information_setting.tex` line 3), and `sections/appendix_public.tex` line 18 already
   records its necessity there. The private mechanism inherits the same dichotomy, one level down: in the
   public setting a unique top agent shades its delivery; here it shades nothing, and instead the runner-up
   shades the price.
4. THE GUARANTEE THAT SURVIVES IS THE HONEST BENCHMARK. `P(n; S) >= mu_H^star n - O(n^{2/3} (log n)^{1/3})`
   holds at every profile, hence at every equilibrium, and Corollary E1.1 shows it is attained at an
   equilibrium when `K_top = 1`. On a unique-top instance the worst-case equilibrium revenue of MESP equals
   the revenue it guarantees against arbitrary, even adversarial, play.

## 4. Task 2: coalitions of two

### 4.1 Definitions

A pair deviation from a profile `S` by `{i, j}` is a pair `(S'_i, S'_j)` in `B_{i,n} x B_{j,n}` with the other
`K - 2` strategies unchanged. Call it PROFITABLE if there is `eps > 0` such that, for all large `n`, both
members gain at least `eps n`; call it SELF-ENFORCING if from the resulting profile neither member has a
unilateral deviation in its own behavioral class gaining `Omega(n)` (outsiders are not required to be content).
`S` is PAIR-PROOF if no profitable pair deviation exists, and PAIR-COALITION-PROOF if no profitable
self-enforcing pair deviation exists. These are the additive analogues of a strong equilibrium and of a
coalition-proof equilibrium, both restricted to coalitions of size two; if the paper states either, the
standard definition must be cited and the citation verified against its primary source, which I have not done.
Note that the model has no transfers, so a coalitional deviation must make both members better off on its own.

### 4.2 Theorem E2

> **Theorem E2.** Assume (ND) and consider pair deviations from `S^star` in which the two members change only
> their Stage-1 bids (the self-enforcement test allows arbitrary behavioral deviations).
>
> **(i) Unique top capacity (`K_top = 1`).** Let `W` be the top agent and `k` an agent with `M_k = M_(2)`. The
> pair `{W, k}` deviating to `c_W = M_W` and `c_k` equal to its lowest feasible bid (`mu_k` if `k` is honest,
> else `0`) is profitable and self-enforcing:
>
>   `W` gains `(M_(2) - theta)_+ N_n - O(n s_n + sqrt(n log n))`,  `k` gains `L_n (M_(2) - c_k) - O(n^{-2}) > 0`,
>
> where `theta := max{c_k, M_(3), mu_W 1{W honest}}`, and platform revenue falls by
> `(M_(2) - theta)_+ n - O(K L_n + n s_n)`. The resulting profile satisfies case (A) of Theorem E1, so no agent
> whatsoever, member or outsider, has a unilateral deviation gaining more than `L_n + 2 b_n(n) + R_K(n) + O(1)`.
> Hence `S^star` is neither pair-proof nor pair-coalition-proof, and the sharp per-round transfer from the
> platform to the pair is `M_(2) - max{M_(3), mu_k 1{k honest}, mu_W 1{W honest}}`, which is never below zero
> and never takes revenue below `mu_H^star`.
>
> **(ii) Exactly two top agents (`K_top = 2`).** Let `{i, j} = K_top`. The joint deviation to a common bid
> `theta in (max{M_(3), mu_i 1{i honest}, mu_j 1{j honest}}, M_top)` is profitable: each member gains
> `(1/2) N_n (M_top - theta) + L_n (M_top - theta) - O(n s_n + sqrt(n log n))`, and revenue falls by
> `(M_top - theta) n - O(K L_n + n s_n)`. But no profitable pair deviation of this form is self-enforcing: the
> only self-enforcing pair bid vector is `(M_top, M_top)`, which is `S^star` itself. Hence `S^star` is not
> pair-proof but is pair-coalition-proof, and every self-enforcing pair deviation leaves revenue at
> `M_(2) n - O(n^{2/3} (log n)^{1/3})`.
>
> **(iii) Three or more top agents (`K_top >= 3`).** No pair deviation of this form is profitable: some top
> agent outside the pair still bids `M_top`, so the price stays at `M_top - O(s_n)` and the only effect of the
> pair's bids is to redistribute the winning probability between them, which one of the two strictly loses.
> `S^star` is pair-proof.

PROOF. (i) Under `S^star`, on the good event `G_{[K]}`, `W` wins and `tau in [M_(2) - 2 s_n, M_(2)]`; under the
deviation, on the corresponding good event, `W` still wins (its bid is unchanged and only one other bid moved
down) and the second order statistic is `max{c_k, max_{l != W, k} M_l} = max{c_k, M_(3)}`, so
`tau' in [(theta_0 - 2 s_n)_+, theta_0]` with `theta_0 := max{c_k, M_(3)}`. `W`'s Stage-1 utility is unchanged
and its primary target moves from `max{mu_W 1{W hon}, tau}` to `max{mu_W 1{W hon}, tau'}`, so its per-round
primary utility rises by `max{mu_W 1{W hon}, tau} - max{mu_W 1{W hon}, tau'}`, which is
`M_(2) - theta +- 2 s_n` with `theta = max{theta_0, mu_W 1{W hon}}`; multiply by `N_n` and charge the false
switch (`2 N_n (2 n^3)^{-1}`) and the bad events. Agent `k`'s gain is Corollary E1.2. Self-enforcement and the
stronger unilateral statement are Theorem E1 case (A), which applies because `c_W = M_W > M_(2) = V_W`. The
revenue statement is the revenue formula of Theorem E1 evaluated at the two profiles.

(ii) Profitability: at `S^star` each member wins with probability exactly `1/2` (exchangeability of the two
bids, uniform priority) at a price in `[M_top - 2 s_n, M_top]`; after the deviation each still wins with
probability exactly `1/2`, because the two bids remain exchangeable and the other capacities are below
`theta`, at a price in `[(theta - 2 s_n)_+, theta]`. Every other term of the utility is unchanged under the
coupling, so each member gains `(1/2) N_n (M_top - theta) + L_n (M_top - theta)` up to `2 N_n s_n`, the false
switch and the bad events.

Non-self-enforcement: let `(c_i, c_j)` be the pair's bids and suppose `max(c_i, c_j) < M_top` or
`min(c_i, c_j) < M_top`. Three cases. If `c_i = c_j = theta < M_top`, then `i` unilaterally bidding `M_top`
wins outright instead of with probability `1/2`, at the same price (the price it faces is set by `j`'s bid,
which has not moved), so by (E1) and the `S^star` computation above it gains at least
`(1/2) N_n kappa - L_n - O(sqrt(n log n))`. If `c_i > c_j` then `j` loses; bidding `M_top >= c_i` it wins with
probability at least `1/2 - n^{-4}` at a price at most `M_top = M_j`, and its current post-bid utility is at
most `2 n^{-2}` by (E2), so it gains at least `(1/2) N_n kappa - 2 L_n - O(1)`. The case `c_j > c_i` is
symmetric. Hence the only self-enforcing pair bid vector is `(M_top, M_top)`. Since at that vector the price is
`M_top - O(s_n)`, revenue is preserved.

(iii) With `K_top >= 3`, at least one top agent `l` lies outside any pair, and it bids `M_top`. On the good
event no member can outbid it strictly, since every capacity is at most `M_top`, so the winner's bid is
`M_top` and the second order statistic is at least `M_top - s_n`: the price is `M_top - O(s_n)` whatever the
pair does. Take a member `m`. If `M_m < M_top`, then `m` loses on the good event whatever it bids, so by (E2)
every change of its bid moves its utility by at most `L_n + 2 n^{-2}`, which is not `Omega(n)`. If
`M_m = M_top`, its per-round value of winning is `1 + mu_m - M_top + O(s_n)` whatever the pair does, so the
only effect of the pair's bids on `m` is its winning probability. That probability is `1/|B|` if `m` bids
`M_top`, where `B` is the set of agents bidding `M_top` (exchangeability and the uniform priority), and `o(1)`
if it bids below. If both members bid `M_top` then `B = K_top` and both get exactly their `S^star` values, so
neither gains. If a member bids below `M_top` its probability drops from `1/K_top` to `o(1)` and it loses
`(1/K_top) N_n kappa - O(L_n)`, a linear amount, while only its partner can gain. So in every case at least
one member is not better off, and no pair deviation is profitable. Q.E.D.

The expectation in the brief (two agents jointly underbid, the price falls, the monitor does nothing because
the winner complies with the lower price) is confirmed in (i) and (ii), and the monitor is indeed irrelevant:
in both the winner's target `min{tau, M_W}` meets the announced price exactly, so `lem:private-monitor` gives a
false-switch probability of at most `(2 n^3)^{-1}` and the coalition is never detected. What the brief did not
anticipate is that (i) needs no coordination at all, because each member's part of the deviation is already
individually profitable (Corollary E1.2), and that in (ii) the agreement is not self-enforcing, so the
two-top condition protects the mechanism against pairs exactly as it protects it against equilibrium selection.

### 4.3 Why coalitions cannot attack the fallback instead

The remaining coalitional channel is the EXP3 phase: a pair could drive the mechanism into the fallback and
then share it at a low delivery level. The following proposition, which uses only `lem:selected-reactive-exp3`,
rules that out.

> **Proposition E3 (upward undercutting always pays in the fallback).** Condition on a fallback start with
> remaining horizon `H` and let `F in [0, 1)` and `eps in (0, 1 - F]`. Suppose that under the profile every
> agent delivers at most `F` on every fallback selection, and let `i` be an agent with `M_i >= F + eps`.
> Then the deviation "deliver `F + eps` on every fallback selection" gives `i` at least
> `H - R_K(H)/eps` fallback selections and hence fallback utility at least
> `(H - R_K(H)/eps) (1 + mu_i - F - eps)`, while its fallback utility under the profile is at most
> `(1 + mu_i) Q_i` with `Q_i` its number of selections there.
>
> PROOF. Under the deviation, `i` is a comparator of conditional selected mean at least `F + eps`, so
> `lem:selected-reactive-exp3` gives total fallback reward at least `(F + eps) H - R_K(H)`. Total fallback
> reward is also at most `(F + eps) Q_i + F (H - Q_i) = F H + eps Q_i`. Subtracting,
> `eps Q_i >= eps H - R_K(H)`. Each selection is worth `1 + mu_i - (F + eps)`. Q.E.D.

> **Proposition E3.1 (the fallback has no low-delivery equilibrium).** Condition on a fallback start with
> remaining horizon `H`, and consider profiles in which each agent `i` delivers a constant `f_i in [0, M_i]`
> (at least `mu_i` if honest) on every fallback selection, the analogue of `Sigma` for the fallback phase.
> Assume (ND). If no agent has a fallback deviation gaining `Omega(H)`, then `F := max_i f_i >= M_(2) - o(1)`,
> and hence the fallback revenue is at least `M_(2) H - o(H)`.
>
> PROOF. Write `T := {i : f_i >= F - H^{-1/4}}` and suppose `F <= M_(2) - eta` for a constant `eta > 0`; then at
> least two agents have capacity `M_j >= M_(2) >= F + eta`. Two cases.
>
> (a) Some such `j` is outside `T`, so `f_j < F - H^{-1/4}`. By `lem:selected-reactive-exp3` with the agent
> attaining `F` as comparator, total fallback reward is at least `F H - R_K(H)`, and it is at most
> `F(H - Q_j) + f_j Q_j`, so `Q_j <= R_K(H)/(F - f_j) <= R_K(H) H^{1/4} = O(H^{3/4})` and `j`'s fallback utility
> is `O(H^{3/4})`. Proposition E3 with `eps = eta/2` gives it at least
> `(H - 2 R_K(H)/eta)(1 + mu_j - F - eta/2) >= H kappa /2` for large `H`, a gain of `Omega(H)`.
>
> (b) Every such `j` is in `T`. The shares of the members of `T` sum to at most `H`, so some `j` in `T` with
> `M_j >= F + eta` has `Q_j <= H/|T|`, and `|T| >= 2` because at least two agents have capacity above `F` and
> both are in `T`. Its utility is `Q_j (1 + mu_j - f_j) <= (H/2)(1 + mu_j - F + H^{-1/4})`, while Proposition E3
> with `eps = eta/2` gives it at least `(H - 2 R_K(H)/eta)(1 + mu_j - F - eta/2)`. The difference is at least
> `(H/2)(1 + mu_j - F) - eta H/2 - O(H^{3/4})`, and `1 + mu_j - F >= kappa`, so for `eta < kappa/2` the gain is
> `Omega(H)`. Since `eta` was an arbitrary positive constant, `F >= M_(2) - o(1)`. The revenue statement is
> `lem:selected-reactive-exp3` at the comparator attaining `F`. Q.E.D.

This says the fallback, unlike the bidding stage, has no low-revenue equilibrium at all, with no top-set
assumption: the agent that sets the benchmark there is always a potential winner. The scope is the same
restriction as in Theorem E1, constant targets within the phase, and it cannot be lifted by the same argument,
because EXP3 carries no monitor: an agent that delivers high until the weights favour it and then drops is not
covered by `lem:selected-reactive-exp3`, whose comparator must have conditional mean at least `v` on every
selection. That is why the manuscript's robustness proof uses an honest agent, whose lower bound is uniform
over histories, as the fallback comparator.

Two consequences. First, a fallback agreement at any common delivery level `F` strictly below the capacity of
one of its members is not self-enforcing: taking `eps` constant, that member gains
`(1 + mu_i - F - eps) H - O(sqrt(H log K)/eps) - (1 + mu_i) Q_i`, which is linear in `H` as soon as its share
`Q_i` under the agreement is bounded away from `H`. Second, and this is the structural point, the fallback is
immune to the failure that afflicts Stage 1 because no agent is ever locked out of it: an agent that is
currently receiving nothing can always buy the pulls back by delivering slightly more, so every agent's
delivery carries a linear stake at all times. In Stage 2, by contrast, the Stage-1 bid allocates the entire
primary phase irrevocably, and the losers' bids, which set the price, are thereafter worthless to them. That
asymmetry is the diagnosis, and it is what the repair in Section 5.3 restores.

### 4.4 The honest benchmark survives collusion: verification

The brief asks for this to be checked, since it is the property that makes the negative results tolerable. I
read the robustness proof (`sections/appendix_private.tex`, subsection "Honest-benchmark robustness") line by
line looking for a hidden independence-across-agents assumption. There is none; each of its five steps is a
statement about one honest agent `h` and about the mechanism, and the other agents enter only through the
history.

1. `Pr{beta_h < mu_H^star - s_n} <= (2 K n^4)^{-1}`: conditional Hoeffding-Azuma on `h`'s own Stage-1 pulls,
   whose increments `Y - m` are conditionally centred given the entire past. The past may contain arbitrary
   correlated play by all other agents, and their targets may be chosen jointly and adaptively; the martingale
   property is unaffected. Valid under collusion.
2. `W = h` implies every primary target is at least `mu_h`: honesty is a constraint on `h`, not a choice of
   anyone else. Valid.
3. `W != h` implies `beta_(2) >= beta_h`, hence `tau >= (mu_H^star - 2 s_n)_+` on the good event: an order
   statistic inequality. Colluders cannot remove `beta_h` from the order statistic and cannot lower it. Valid.
4. `lem:private-monitor` charges the winner's target sum at rate at least `tau`: the lemma is stated for
   arbitrary predictable targets of the winner and does not care who chose them or whether the choice was
   coordinated with others. Valid.
5. `lem:selected-reactive-exp3` with comparator `h`: its statement explicitly allows all other agents to choose
   arbitrary feasible nonanticipating targets after selection, with no independence requirement among them.
   Valid.

So `P(n; S) >= mu_H^star n - O(K L_n + n s_n + b_n(n) + R_K(n))` holds for every joint behavioral profile,
including any coalition of any size up to `K - 1` (and up to `K`, since honesty binds even a colluding honest
agent). By Corollary E1.1 this bound is attained by an equilibrium when `K_top = 1`, so it is tight and it is
the only revenue guarantee of MESP that is robust to both equilibrium selection and collusion. The one
structural requirement, which the model supplies, is that `K_H` is nonempty and that honesty is a property of
the agent rather than a strategy it may abandon inside a coalition.

## 5. The published precedent, tested against MESP

### 5.1 What the precedent says

Source read by me, 18 September 2026: Mark Braverman, Jieming Mao, Jon Schneider and S. Matthew Weinberg,
"Multi-armed Bandit Problems with Strategic Arms", Proceedings of the Thirty-Second Conference on Learning
Theory, PMLR volume 99, pages 383 to 416, 2019. Landing page verified with curl at
`https://proceedings.mlr.press/v99/braverman19b.html` (title, authors, volume and page range as above); the
full text I read is the paper PDF from that record. Quotations below are from the PDF text layer with
whitespace normalized; the text layer drops the epsilon glyph, which I restore in square brackets.

Their model: each round the pulled arm receives a private reward `v` and chooses an amount `x` to pass to the
principal, keeping `v - x`; unpulled arms get 0. Per-pull arm utility is therefore `v - x`, which in their
unrestricted payment model may be negative ("sometimes the value you must report ... might be larger than the
value received in that round"). Their Section 4.2 opens: "One issue with Mechanism 1 is that, while the
principal achieves Theta(T) revenue when the arms play according to their dominant strategies, there can exist
[epsilon]-Nash equilibria for the arms which still leave the principal with negligible revenue. For instance,
if there are two arms with equal means mu_1 = mu_2 = mu, one possible [epsilon]-Nash equilibrium is for them
both to bid mu, and then for arm i* to immediately defect after it is chosen. This is not a dominant strategy,
since arm i* surrenders its bonus for not defecting, but since this bonus is at most 1, this is still an
[epsilon]-Nash equilibrium for any [epsilon] = o(T) which is larger than 1."

Their repair is Mechanism 2, whose line 5 reads "For each arm i satisfying u + log(w_i - M) >= 0, play it
B floor(u + log(w_i - M)) times", with `B = 2^{1/4} T^{3/4} / mu_min`, and whose Corollary 16 states: "Under
Mechanism 2, the principal will receive revenue at least mu^0 T - o(T) whenever arms play according to an
[epsilon]-Nash equilibrium, where mu^0 is the second largest mean in the set of means mu_i and
[epsilon] = o(T)." I read the proof of Corollary 16: the quantity it controls is
`G_mu(w) = ((mu - (w + M)) + mu + max(u + log w, 0) mu) B`, an upper bound on an arm's reward from every round
other than the winner's tenure, and the argument is that `G_mu` is maximized at `w = mu` with a quadratic
deficit `B mu gamma^2` at `w = mu (1 -+ gamma)`, so an `[epsilon]`-Nash arm must report within a factor
`gamma = (epsilon/T)^{1/3} = o(1)` of its true mean, whence the second highest report is `mu^0 (1 - o(1))`.

Two points matter for us. First, this is a published instance of exactly the question in the brief, so a
referee may well ask it. Second, and this is the part that decides what transfers: the device that pins down
every arm's bid is the term `B floor(u + log(w_i - M))`, a number of guaranteed pulls that is strictly
increasing in the arm's OWN report. It gives a losing arm a stake in its own bid. MESP gives every agent
exactly `L_n` Stage-1 pulls whatever it bids, which is precisely the absence of that device, and is why
Theorem E1 case (A) exists.

### 5.2 Their defection witness, tested against MESP

The witness does not transfer, for two independent reasons, and only the second of them is the monitor.

*(a) The prize does not vanish.* Their witness needs the winner to be indifferent between continuing and
defecting, which happens because with two equal means the winner pays `w^0 = mu` and receives `v` with
`E[v] = mu`, so its surplus from continuing is zero and only the bonus, at most 1, is at stake. In this paper's
model a selection is worth `1 + mu_i - m` with `m <= M_top`, so under (ND) the winner's surplus from
continuing is at least `kappa = 1 - M_top > 0` per round and the whole tenure is at stake, not a bounded bonus.
Their construction has no analogue here whenever `M_top < 1`.

*(b) The tenure is lost but it is not destroyed.* The exact computation: let `W` win at price `tau` and deliver
`0` from its first primary pull. Then `Z_r = 0`, so the monitor fires at the first `r` with `r tau > b_n(r)`,
that is after `q_0 = floor(log(2 n^4) / (2 tau^2)) + 1 = O(log n / tau^2)` pulls, and `W` collects
`(1 + mu_W) q_0` there. In the fallback, with the other agents playing `S^star`, equation
`private-fallback-top` bounds its continuation by `(1 + mu_W - V_W) H + R_K(H)`. Against the baseline
`(1 + mu_W - tau) N_n` this gives

  `u_W(defect) - u_W(comply) <= q_0 V_W + (tau - V_W) N_n + R_K(n) <= q_0 + R_K(n) = O(sqrt(n log n))`,

using `tau <= V_W` on the good event. So the defection gains at most `O(sqrt(n log n))`, which is inside the
theorem's slack: this is not new, it is a special case of `thm:private-mesp`, which already covers every
unilateral behavioral deviation. What is worth saying explicitly in the paper is the reason, and the accurate
statement of it is this: the monitor converts a defection into a restart of the competition rather than into a
forfeited bonus, and in the restarted competition the deviator is paid for selections only if it out-delivers
the other agents (Proposition E3). I checked whether the stronger and more attractive claim, that MESP
strictly punishes defection by a linear amount, is true. IT IS NOT, and the paper should not claim it: on a
unique-top instance the defector can, after the switch, deliver `M_(2) + eps` in the fallback, take all but
`R_K(H)/eps` of the remaining pulls by Proposition E3, and recover per-round utility `1 + mu_W - M_(2) - eps`,
which is within `2 s_n + eps` of what complying pays it. Defection is neutral here, not punished.

*(c) The consequence for revenue, which is what the witness was about.* Suppose every agent bids capacity and
the winner defects immediately. Stage-1 revenue is `L_n sum_i M_i`, the primary phase contributes `0` over
`O(log n)` rounds, and the fallback, with the other agents delivering capacity, yields at least
`M_top H - R_K(H)` by `lem:selected-reactive-exp3`. Total revenue is at least `M_top n - O(K L_n + R_K(n))`,
which is above the mechanism's own equilibrium revenue `M_(2) n`. The reason is worth one sentence in the
paper: the fallback charges no shading, so whoever takes the restarted competition must deliver at least the
best other capacity, whereas the priced tenure charges only `beta_(2) - s_n`; a defection therefore raises
platform revenue by at least `2 s_n` per remaining round rather than lowering it. So in MESP the defection
channel is not a low-revenue channel at all. Under arbitrary play the floor `mu_H^star n - o(n)` of the
robustness part applies regardless, and Propositions E3 and E3.1 say that no fallback agreement below the
second capacity is self-enforcing. The
low-revenue channel in MESP is the bidding channel of Theorem E1, which is a different failure from theirs:
theirs is a defection equilibrium sustained by a bounded continuation reward, ours is a pricing failure
sustained by an indifferent price setter.

### 5.3 Their repair, adapted, with its cost

> **Proposition E5 (bid-indexed bonus rounds).** Fix `G_n` with `2 L_n <= G_n` and `K G_n = o(n)`; take
> `G_n := ceil(n^{5/6})`. Modify MESP by reserving `K G_n` rounds at the end, redefining
> `N_n := n - K L_n - K G_n`, and, after Stage 1, giving agent `i` exactly `floor(G_n beta_i)` of the reserved
> rounds, the remainder being allocated cyclically; rewards in reserved rounds are ignored by the mechanism,
> and in the modified family `Sigma` every agent delivers its lowest feasible target there. Then for every
> `S^c in Sigma` and every agent `i`, replacing `c_i` by `M_i` changes `i`'s utility by at least
> `(G_n - L_n) (M_i - c_i) - O(1) >= (G_n/2) (M_i - c_i) - O(1)`. Consequently, for any slack
> `eps_n = o(G_n)`, every `S^c in Sigma` that is an `eps_n`-equilibrium has
> `M_i - c_i <= gamma_n := 2 (eps_n + O(1)) / G_n = o(1)` for every `i`, and therefore
> `P(n; S^c) >= M_(2) n - O(n gamma_n + n s_n + K L_n + K G_n)`.
>
> PROOF. Couple the two executions by the Stage-1 uniforms, so `beta_i^{(c)} <= beta_i^{(M)}` pathwise.
> (1) Stage-1 utility falls by exactly `L_n (M_i - c_i)`. (2) `E[floor(G_n beta_i)] >= G_n E[beta_i] - 1` and
> `E[beta_i] = c_i` resp. `M_i`, while each reserved round is worth `1 + mu_i - m >= 1` (a strategic agent
> delivers `0` there, an honest one `mu_i`), so the reserved-round utility rises by at least
> `G_n (M_i - c_i) - 1`. (3) The win event under the lower bid is contained pathwise in the win event under
> the higher bid; on the common part the post-bid continuations coincide in law because the price `tau_i`
> does not depend on `i`'s own bid; on the difference the change is (winner's post-bid utility) minus
> (loser's post-bid utility) `>= 0 - 2 n^{-2}` by (E2). Summing gives the claim. The revenue consequence is
> the good-event bound `beta_(2) >= M_(2) - gamma_n - s_n` inserted in the manuscript's revenue proof. Q.E.D.

Cost, stated plainly. (i) The mechanism gives away `K G_n = O(n^{5/6})` rounds on which it collects essentially
nothing, at every profile including the proposed one, so the revenue error term degrades from
`O(n^{2/3} (log n)^{1/3})` to `O(n^{5/6})`, and with the natural slack `eps_n` equal to the mechanism's own
deviation bound `O(n^{2/3} (log n)^{1/3})` the term `n gamma_n = O(n^{5/6} (log n)^{1/3})` dominates. The
revenue claim would become `M_(2) n - O(n^{5/6} (log n)^{1/3})`. (ii) The honest-benchmark bound degrades by the
same `O(K G_n)`. (iii) The guarantee is over `eps_n`-equilibria with `eps_n = o(n^{5/6})`, a class that does
contain the mechanism's own slack, so the package is coherent, but it is not a guarantee over all `o(n)`
equilibria; obtaining that would require `G_n = Theta(n)` and hence a linear revenue cost, because in this
model a bonus round yields the platform nothing. (iv) One genuine gain: the bonus cancels the Stage-1 shading
incentive, so the top-agent deviation bound improves to `O(b_n(n) + R_K(n)) = O(sqrt(n log n))` and
`prop:tightness` ceases to apply. (v) NOT PROVED HERE: the re-derivation of the equilibrium and robustness
parts of `thm:private-mesp` for the modified mechanism. The monitor and fallback arguments are untouched, and
only the accounting changes, but I have not written it out, and I would not put Proposition E5 in the paper
without doing so.

### 5.4 The knife edge excluded by (ND)

If `M_top = 1` and the agents that could outbid the winner all have `mu_i = 0`, then winning is worth
`1 + 0 - tau = 0` per round at `tau = 1`, and the deviations used in Section 2.2 have zero value. In that case
low-bid profiles can be equilibria for a different reason, and the characterization of Theorem E1 does not
apply. This is the same degeneracy that makes their two-equal-means witness work, and it is excluded here by
`M_top < 1`, which the paper may simply assume; I did not look for a sharper condition than (ND).

### 5.5 Repairs I considered and do not propose

- A RESERVE PRICE `tau = max{(beta_(2) - s_n)_+, rho}` pins the price from below by `rho`, but the platform
  does not know the capacities, so `rho` is either uninformative or exceeds `M_W` and forces a switch. It
  converts the revenue question into a question about the fallback game, which the paper does not analyze.
- A FIRST-PRICE RULE `tau = (beta_(1) - s_n)_+` makes the winner pay its own bid, so it bids just above the
  highest losing bid and the price is unpinned in exactly the same way.
- DROPPING THE LOCKED ALLOCATION, that is running the fallback rule for all `n` rounds, removes the failure
  entirely: by Proposition E3 no agent is ever locked out, every agent's delivery always carries a linear
  stake, and in the phase-stationary family every additive equilibrium has the top agent delivering at least
  `M_(2) - o(1)`, hence revenue `M_(2) n - o(n)` with no top-set assumption. I do not propose it, for a reason
  worth recording: the resulting equilibrium profile is "deliver just above the second largest capacity", which
  an agent cannot implement, because capacities are private and no price is announced. What the price
  announcement buys is exactly an implementable proposed profile, `min{tau, M_i}`, that needs only the agent's
  own capacity and the message. That trade, an implementable proposed profile against a pinned price, is the
  real content of the dichotomy in Theorem E1, and it is the honest way to present the limitation.

## 6. Findings, with severity, file and line

**E1-F1 (P2, contribution and referee risk). The revenue claim of `thm:private-mesp` is profile-specific, and
the worst equilibrium revenue is exactly the honest floor.**
File and lines: `sections/Private_information_setting.tex` line 66 ("The theorem is scalar, fixed-horizon,
additive, and does not assert high revenue in every equilibrium"); `sections/appendix_private.tex` line 201
("The result does not imply high revenue at every equilibrium; for example, a price-setting agent may lower
off-equilibrium revenue without obtaining a linear utility gain"). Claim affected: the revenue part of
`thm:private-mesp` and the abstract's "earns the second-highest capacity benchmark" (`neurips_2026.tex`
line 46). Nothing in the manuscript is false: both hedges are correct, and the second is a one-line informal
gesture at exactly the mechanism proved here. What is missing is the quantifier. Theorem E1 and Corollary E1.1
give it: on a unique-top instance there is a continuum of additive behavioral equilibria with the same
deviation bound as `S^star` and revenue anywhere in `[mu_H^star, M_(2)] n`, the minimum is attained, and it
equals the bound the paper already proves against arbitrary play; on a two-top instance every equilibrium in
the family has revenue `M_(2) n - o(n)`. Minimal repair: state the dichotomy (draft in Section 7) and keep the
theorem as it is. Downstream: none of the proofs change; the abstract sentence and the Intro sentence
"yield second-capacity revenue at an additive equilibrium" (`sections/Intro.tex` line 21) are already worded as
"at an" rather than "at every" equilibrium, and remain correct.

**E1-F2 (P2, contribution). No coalition statement exists, and `S^star` is not resistant to a pair unless
three agents tie at the top.** File: `sections/Private_information_setting.tex`, Theorem `thm:private-mesp`
(the supremum is over unilateral `S'_{i,n}` only). Theorem E2 gives the sharp statement: with `K_top = 1` a
self-enforcing pair transfers `M_(2) - max{M_(3), mu_H^star}` per round from the platform; with `K_top = 2` a
pair can gain but no profitable pair agreement is self-enforcing; with `K_top >= 3` no pair gains at all. The
honest benchmark survives every coalition (Section 4.4, five steps checked). Minimal repair: one sentence in
the main text plus Theorem E2 in the supplement.

**E1-F3 (P3 to P2, precision). The tightness proposition is stated for the wrong agent.**
File: `sections/appendix_private.tex`, `prop:tightness`, and `sections/Private_information_setting.tex` line 66
("underbidding to the midpoint between the two largest capacities saves `L_n (M_i - V_i) / 2`"). The bid that
matters for revenue is the runner-up's, not the winner's, and the runner-up's saving is
`L_n (M_(2) - mu_k 1{k honest})`, which is larger than `L_n (M_i - V_i) / 2` on instances with a small capacity
gap, is exact rather than a lower bound, and needs no coupling of the post-bid phase (Corollary E1.2). The
exact best-response computation confirms it to machine precision (Section 8: agent 1's exploitability at
`S^star` on `K2_unique_top` is `L_n x 0.30` at every horizon tested). Recommendation: keep `prop:tightness` and
add the runner-up version, or replace it, since the runner-up version is what explains the equilibrium set.

**E1-F4 (P2, related work). The description of the closest prior mechanism omits the result that this paper
does not have.** File: `sections/related_work.tex` line 5: "\citet{braverman2019strategic} let each arm keep
part of a realized reward and pass the rest to the principal; they give a dominant-strategy mechanism that
earns the second-largest mean and show that ordinary low-regret algorithms admit equilibria with sublinear
principal reward." Both halves are accurate (their Mechanism 1 and Corollary 13; their Section 3 and Theorem
11). What is omitted is their Mechanism 2 and Corollary 16, which upgrade the revenue guarantee from dominant
strategies to EVERY `epsilon`-Nash equilibrium with `epsilon = o(T)`, which is precisely the quantifier that
`thm:private-mesp` does not have. A referee who knows that paper will make the comparison. The bibliography
entry `braverman2019strategic` (`references.bib` lines 35 to 44) matches the primary record exactly (COLT 2019,
PMLR volume 99, pages 383 to 416), so only the prose needs changing. Recommendation: say what they achieve,
say what MESP achieves, and say why the difference exists (their step 5 gives each arm a number of pulls
increasing in its own report; MESP gives every agent `L_n` pulls whatever it bids) and what it would cost to
close it (Proposition E5). This turns an unfavorable comparison into an honest and defensible one, and it is
also where the genuine advantage should be stated: their mechanism observes a directly chosen payment and
cannot face bait and switch under noise, which is the problem the monitor solves.

**E1-F5 (P3, factual, for the coordinator).** `audit/round2/prompts/COMMON.md` lists the compiled sections and
omits `sections/related_work.tex`, which is compiled: `neurips_2026.tex` line 50 contains
`\input{sections/related_work}`. Any agent relying on that list for a completeness scan will miss a section
that contains six of the paper's twelve citations.

## 7. Draft text for the manuscript

Offered as a draft only; I made no canonical edit. Main text, to follow the proof skeleton in
`sections/Private_information_setting.tex` (replacing the clause "and does not assert high revenue in every
equilibrium", about eight lines):

> The theorem is scalar, fixed-horizon and additive, and its revenue claim is a statement about \(S^\star\).
> The equilibrium set is larger, and exactly one instance condition decides whether that matters. Consider the
> profiles \(S^c\) that agree with \(S^\star\) except that agent \(i\) delivers a constant \(c_i\in[0,M_i]\)
> (at least \(\mu_i\) if honest) during bidding, and assume \(M_{\mathrm{top}}<1\). If \(K_{\mathrm{top}}\ge2\),
> then \(S^c\) is an additive behavioral equilibrium if and only if every top agent bids \(M_{\mathrm{top}}\),
> and every such equilibrium earns \(M_{(2)}n-O(n^{2/3}(\log n)^{1/3})\). If the top capacity is unique, then
> \(S^c\) is an additive behavioral equilibrium if and only if the top agent bids above \(M_{(2)}\), the
> remaining bids are unconstrained, and the equilibrium revenues fill
> \([\mu_H^\star,\max\{\mu_H^\star,M_{(2)}\}]n\) up to the same order; the lower end is attained and coincides
> with the honest benchmark, which holds at every profile. The reason is that the price is the highest losing
> bid, and a losing agent's bid changes its own utility by at most \(L_n\), inside the additive slack, whereas
> any agent that can outbid the winner gains a linear amount; a second agent at \(M_{\mathrm{top}}\) makes the
> price setter a potential winner and restores that linear stake. The same condition governs pairs: with a
> unique top capacity the winner and the runner-up have a jointly profitable, self-enforcing deviation that
> lowers revenue to \(\max\{M_{(3)},\mu_H^\star\}n\), while with \(K_{\mathrm{top}}\ge2\) no jointly
> profitable pair deviation is self-enforcing. The honest benchmark is unaffected: its proof uses no
> independence across agents and therefore holds under arbitrary collusion.

Related work, replacing the second clause of `sections/related_work.tex` line 5 (about three lines):

> \citet{braverman2019strategic} let each arm keep part of a realized reward and pass the rest to the
> principal; they give a dominant-strategy mechanism that earns the second-largest mean, strengthen it with
> bonus rounds whose number grows with the arm's own report so that the second-largest mean is earned at every
> \(o(T)\)-Nash equilibrium, and show that ordinary low-regret algorithms admit equilibria with sublinear
> principal reward. Our price is likewise the second bid, but a bid here is delivered performance rather than
> a report, so we pay for elicitation in effort and do not reward a losing bid; consequently our revenue
> guarantee is a statement about the proposed profile unless two agents attain the top capacity.

## 8. Exact computations

### 8.1 What was computed and how

`bidprofile.py` (this directory) extends `scratch/experiments/round2/exploitability/dp.py` from the proposed
profile to an arbitrary feasible Stage-1 bid vector `c`, and adds an exact platform-revenue computation. For a
chosen agent it returns a certified bracket for its utility under `S^c` and a certified bracket for the
supremum of its utility over the full behavioral class against `S^c_{-i}`. Exactness, in detail:

- The deviator's one-step objective `1 + mu_i - m + m W(s,1) + (1 - m) W(s,0)` is affine in the target `m`, so
  an optimal target is an endpoint of `[lo_i, M_i]` (`lo_i = mu_i` if honest, else `0`), and two-action
  backward induction over (pull index, cumulative reward) is exact for Stage 1 and for the monitored primary
  phase, including the monitor boundary `Z_r < r tau - b_n(r)` at its exact arithmetic value. This is the same
  argument and the same code path as `dp.py`. The existing acceptance test `validate_dp.py` includes an
  affinity check (its item (iv), a 21-point target grid at random Stage-2 states); I did not rerun it, and
  verified affinity only by the algebra, which is immediate because the continuation values do not depend on
  the current target.
- The fallback is bracketed, not solved: the lower bracket gives the deviator zero fallback continuation, the
  upper bracket gives it `min{2H, (1 + mu_i - V_i) H + R_K(H)}` for a top deviator and
  `min{2H, 2 R_K(H)/delta_i}` for a non-top one, which are equations `private-fallback-top` and
  `private-fallback-low` of the appendix. Those bounds remain valid here because the non-deviating agents
  deliver capacity in the fallback under `S^c` exactly as under `S^star`.
- The other agents' bids are independent binomials, so the joint law of (highest other bid, number tied there,
  identity of the tie winner) is computed exactly by a small convolution, and the price and the winner's
  identity follow. A losing deviator's post-bid utility is bounded by 2 per round times the exact probability
  that the monitor falsely switches under the actual non-deviating winner at the realized price.
- Nothing asymptotic is used: no Hoeffding bound, no `n^{-3}` bound, no `O(.)`.

Instances are the round-2 table `scratch/experiments/round2/common/instances.json` unchanged.
`K2_unique_top`: `mu = (0.10, 0.35)`, `M = (0.90, 0.65)`, agent 1 honest, so `M_(2) = 0.65`,
`mu_H^star = 0.35`, `K_top = 1`. `K2_tied_top`: `mu = (0.10, 0.35)`, `M = (0.80, 0.80)`, agent 1 honest,
`K_top = 2`. `unique_top`: `mu = (0.10, 0.20, 0.35)`, `M = (0.90, 0.65, 0.40)`, agent 2 honest, `K_top = 1`,
`M_(3) = 0.40`. `tied_top`: `mu = (0.10, 0.20, 0.35)`, `M = (0.80, 0.80, 0.45)`, agent 2 honest, `K_top = 2`.
Full output is one JSON per configuration in `<scratchpad>/round2/e1/`; `aggregate_e1.py` prints the tables.
The JSON files are also copied to `results/` in this directory. Horizons are `n = 2000, 5000, 10000` for every
configuration and `20000` where a job had finished; three `K = 2` jobs and one `K = 3` job were still computing their
largest horizon when this report was finalized, and every number quoted below comes from a completed configuration.
Runs are logged in `COMPUTE_LOG.md`.

### 8.1a Independent validation of the exact computation

`validate_bp.py` runs the round-2 episode simulator (`scratch/experiments/round2/common/mechanism.py`, variant
`mesp`, seeds from `common/seeds.py` in the unused `analysis` phase) with every agent playing `S^star` except
for the constant Stage-1 target `c_i`, and compares the simulated mean utility of each agent and the simulated
mean platform reward with the exact brackets. Five configurations at `n = 2000`, 2000 to 4000 replicates each:

| configuration | agent utilities, simulated against exact | revenue, simulated against exact |
| - | - | - |
| `K2_unique_top`, (0.70, 0.35) | 1439.41 +- 1.10 against 1439.05; 326.00 against 326.00 | 516.15 +- 1.44 against 516.45 |
| `K2_tied_top`, (0.50, 0.50) | 756.93 +- 17.49 against 759.35; 954.13 +- 20.89 against 951.10 | 739.34 +- 2.12 against 739.55 |
| `unique_top`, (0.70, 0.00, 0.35) | 1123.83 +- 1.16 against 1124.00; 391.20 against 391.20; 326.00 against 326.00 | 473.09 +- 1.63 against 472.90 |
| `tied_top`, `S^star` | 372.40 +- 8.49 against 371.03; 453.63 +- 10.07 against 454.73; 293.40 against 293.40 | 1244.94 +- 1.05 against 1246.03 |
| `tied_top`, (0.50, 0.50, 0.45) | 614.12 +- 18.71 against 608.34; 686.20 +- 20.95 against 690.38; 324.57 +- 7.70 against 326.71 | 745.23 +- 1.73 against 746.43 |

Every simulated mean lies inside the exact bracket widened by three standard errors, including the tied cases
in which the winner's identity is decided by the mechanism's uniform priority (simulated win shares
0.502 / 0.498 / 0.000 on `tied_top` at `S^star`, and 0.4905 / 0.4790 / 0.0305 at the coalition profile, where
the third agent occasionally outbids both underbidders). The simulator and the exact computation share no code
beyond the design constants in `common/design.py`.

### 8.2 Result 1: the bad profile is an equilibrium, and a very good one

Per-round deviation gain (exact bracket) at the candidate low-revenue profiles, against the manuscript's own
finite-`n` constant `L_n + 2 b_n(n) + R_K(n)`. Agents marked H are honest. Every entry is a total, not a rate.

| instance | profile | n | agent 0 | agent 1 | agent 2 | thm const | revenue/round |
| - | - | - | - | - | - | - | - |
| K2_unique_top | `S^star` = (0.90, 0.65) | 10000 | [587.9, 610.4] | [302.1, 302.1] H | | 2229 | 0.5652 |
| K2_unique_top | `S^star` = (0.90, 0.65) | 20000 | [921.7, 949.2] | [490.2, 490.2] H | | 3406 | 0.5767 |
| K2_unique_top | bad = (0.70, 0.35) | 2000 | [226.7, 233.2] | [34.8, 40.0] H | | 839 | 0.2582 |
| K2_unique_top | bad = (0.70, 0.35) | 5000 | [431.7, 441.1] | [1.7, 4.0] H | | 1462 | 0.2662 |
| K2_unique_top | bad = (0.70, 0.35) | 10000 | [685.6, 695.5] | [0.0, 0.0] H | | 2229 | 0.2752 |
| K2_unique_top | bad = (0.70, 0.35) | 20000 | [1081.5, 1091.9] | [0.0, 0.0] H | | 3406 | 0.2849 |
| unique_top | `S^star` = (0.90, 0.65, 0.40) | 10000 | [563.2, 615.6] | [654.5, 654.6] | [50.3, 50.4] H | 2425 | 0.5533 |
| unique_top | bad = (0.70, 0.00, 0.35) | 2000 | [204.1, 215.4] | [0.0, 0.3] | [0.0, 0.0] H | 929 | 0.2364 |
| unique_top | bad = (0.70, 0.00, 0.35) | 5000 | [410.3, 431.9] | [0.0, 0.0] | [0.0, 0.0] H | 1601 | 0.2432 |
| unique_top | coalition = (0.90, 0.00, 0.40) | 10000 | [811.1, 836.0] | [0.0, 0.0] | [50.3, 50.4] H | 2425 | 0.3134 |

Readings.

1. At the low-revenue profiles every deviation gain is far below the manuscript's own slack, and the losing
   agents play EXACT best responses: their gains are `0.0` to machine precision from `n = 5000` upward. Those
   profiles are therefore not merely additive equilibria; the only agent with any gain at all is the winner,
   and its gain is Stage-1 effort it could save.
2. The winner's gain at the bad profile is the predicted `L_n c_W`. On `K2_unique_top`, `0.7 L_n / n` equals
   `0.114, 0.0868, 0.0705, 0.0572` at `n = 2000, 5000, 10000, 20000` and the exact computation gives
   `0.1166, 0.0882, 0.0696, 0.0546`.
   It decays like `n^{-1/3}`, as `L_n / n` must, so the profile satisfies the equilibrium definition with room
   to spare at every horizon tested.
3. Revenue at the bad profile is `0.2752` per round at `n = 10000` against `0.5652` at `S^star` on
   `K2_unique_top`; the design values are `mu_H^star = 0.35` and `M_(2) = 0.65`, and in both cases the
   difference from the design value is the price shading `2 s_n` (with `s_n = 0.1377` at this horizon) together
   with the Stage-1 accounting. The mechanism keeps `48.7` percent of its equilibrium revenue at the worst
   equilibrium at this horizon, and the asymptotic ratio is `mu_H^star / M_(2) = 0.538`.
4. At `S^star` the runner-up's gain from lowering its bid is EXACTLY `L_n (M_(2) - c_k')`:
   `97.8, 186.0, 302.1, 490.2` at `n = 2000, 5000, 10000, 20000` against `L_n x 0.30` on `K2_unique_top`
   (honest runner-up, so `c_k' = mu_1`), and `211.9, 403.0, 654.5` against `L_n x 0.65` on `unique_top`
   (strategic runner-up, `c_k' = 0`). This is Corollary E1.2 to machine precision at seven horizons, and it
   shows that the drift away from `S^star` needs no coordination.
5. The continuum of Corollary E1.1 is visible at a fixed horizon. On `K2_unique_top` at `n = 5000`, the three
   equilibria `(0.90, 0.65)`, `(0.70, 0.50)` and `(0.70, 0.35)` give revenue `0.5538`, `0.3976` and `0.2662`
   per round, while the largest deviation gain over all agents is `390.9`, `350.2` and `441.1` against a slack
   of `1462`. Moving the losing bid moves the revenue continuously and does not move the equilibrium property.
   At the interior point the honest loser's own gain is `[94.7, 97.0]`, the predicted
   `L_n (0.50 - mu_1) = 620 x 0.15 = 93`.

6. The sufficient condition `2 s_n < c_W - V_W` of Section 2.1 is far from necessary, and the computations say
   why. On `K2_unique_top` the gap is `c_W - V_W = 0.05` while `2 s_n = 0.275` at `n = 10000`, so the
   condition fails by a factor of five, yet the losing agent's exact gain is `0.0`. The reason is that `s_n` is
   a union-bound radius, whereas what actually decides whether a loser can seize the auction is the
   fluctuation of the bid difference, whose standard deviation is
   `sqrt(c_W(1 - c_W)/L_n + M_k(1 - M_k)/L_n) = 0.0208` here. The loser overtakes with probability about
   `0.008` by the normal approximation, worth about `0.008 x N_n (1 + mu_1 - tau) = 52`, against a Stage-1 cost
   of `L_n (M_k - mu_1) = 302` for bidding high enough to try. The finite-`n` criterion for case (A) is
   therefore `Pr(overtake) x N_n (1 + mu_k - tau_k) < L_n (M_k - c_k)`, not `2 s_n < c_W - V_W`; the exact
   computation, which uses no approximation at all, confirms the conclusion.

### 8.3 Result 2: with two top agents the same construction is killed

| instance | profile | n | agent 0 | agent 1 | agent 2 | thm const | revenue/round |
| - | - | - | - | - | - | - | - |
| K2_tied_top | `S^star` = (0.80, 0.80) | 10000 | [197.7, 208.5] | [193.5, 204.8] H | | 2229 | 0.6843 |
| K2_tied_top | joint = (0.50, 0.50) | 2000 | [659.0, 667.6] | [645.2, 645.2] H | | 839 | 0.3698 |
| K2_tied_top | joint = (0.50, 0.50) | 5000 | [1638.7, 1648.1] | [1838.0, 1838.0] H | | 1462 | 0.3758 |
| K2_tied_top | joint = (0.50, 0.50) | 10000 | [3242.7, 3252.5] | [3964.2, 3964.3] H | | 2229 | 0.3844 |
| K2_tied_top | asymmetric = (0.80, 0.50) | 5000 | [400.1, 409.5] | [1310.5, 1320.0] H | | 1462 | 0.4100 |
| K2_tied_top | asymmetric = (0.80, 0.50) | 10000 | [634.3, 644.2] | [2666.0, 2677.4] H | | 2229 | 0.4202 |
| tied_top | `S^star` = (0.80, 0.80, 0.45) | 10000 | [186.3, 211.3] | [184.6, 209.8] | [100.7, 100.7] H | 2425 | 0.6631 |
| tied_top | joint = (0.50, 0.50, 0.45) | 2000 | [524.0, 543.6] | [576.4, 596.1] | [10.3, 10.3] H | 929 | 0.3732 |
| tied_top | joint = (0.50, 0.50, 0.45) | 5000 | [1394.3, 1415.9] | [1552.2, 1573.8] | [36.4, 36.4] H | 1601 | 0.3805 |
| tied_top | joint = (0.50, 0.50, 0.45) | 10000 | [2858.0, 2881.0] | [3207.0, 3229.9] | [88.7, 88.7] H | 2425 | 0.3922 |

Readings.

1. The low-bid profile that is an equilibrium on a unique-top instance is destroyed by a second top agent. The
   per-round gain of agent 0 at the joint-underbid profile is `0.3295, 0.3278, 0.3243` at
   `n = 2000, 5000, 10000` on `K2_tied_top` and `0.2620, 0.2789, 0.2858` on `tied_top`: flat in `n`, hence
   linear in total, whereas the manuscript's slack grows like `n^{2/3} (log n)^{1/3}`. At `n = 5000` the gain
   `1638.7` already exceeds the slack `1462`; at `n = 10000` it is `3242.7` against `2229`, and the ratio
   grows.
2. At `S^star` on the same instances and the same horizon `n = 10000`, the per-round gain lies in
   `[0.0198, 0.0209]` for agent 0 of `K2_tied_top` and in `[0.0186, 0.0211]` for agent 0 of `tied_top`,
   decaying in `n` and far below the slack. The contrast between the two rows of the same instance at the same
   horizon is the whole of Theorem E1.
3. The asymmetric rows test case (B) of Theorem E1 directly: one top agent bids its capacity and the other
   underbids. The underbidding top agent has an exact gain of `1310.5` at `n = 5000` and `2666.0` at
   `n = 10000`, that is `0.262` and `0.267` per round, against the leading-order prediction for the simplest
   deviation, "bid `M_top` and tie", namely
   `(1/2) N_n (1 + mu_1 - tau) - L_n (M_top - c_1) = 1164.6` and `2442.1` with `tau = 0.8 - s_n`. The exact
   optimum is 13 and 9 percent above that simplest deviation, because the exact deviator may also adapt its
   Stage-1 targets to its own running count and ride the monitor boundary in Stage 2; the point here is only
   that the gain is linear. So case (B) really does force every top agent to bid `M_top`, and the two-top
   revenue conclusion does not depend on the top agents playing symmetrically.
4. The honest non-top agent's gain at `S^star` on `tied_top` is exactly `L_n (M_2 - mu_2) = 1007 x 0.10 = 100.7`
   at `n = 10000`, the same Corollary E1.2 arithmetic for a non-top honest agent.

### 8.4 Result 3: the coalition numbers

Exact utility gains for each agent, moving from `S^star` to the deviated profile (totals, not per round).

| instance | deviation | n | agent 0 | agent 1 | agent 2 | revenue/round, `S^star` to deviated |
| - | - | - | - | - | - | - |
| unique_top | pair {0,1} to (0.90, 0.00, 0.40) | 2000 | +255.5 | +211.9 | 0.0 | 0.5364 to 0.3027 |
| unique_top | pair {0,1} to (0.90, 0.00, 0.40) | 5000 | +785.0 | +403.0 | 0.0 | 0.5432 to 0.3056 |
| unique_top | pair {0,1} to (0.90, 0.00, 0.40) | 10000 | +1744.7 | +654.5 | 0.0 | 0.5533 to 0.3134 |
| unique_top | all three to (0.70, 0.00, 0.35) | 5000 | +1066.0 | +403.0 | +31.0 | 0.5432 to 0.2432 |
| tied_top | pair {0,1} to (0.50, 0.50, 0.45) | 10000 | +1350.0 | +1349.4 | +12.0 | 0.6631 to 0.3922 |
| K2_tied_top | pair {0,1} to (0.50, 0.50) | 10000 | +1507.1 | +1492.3 | | 0.6843 to 0.3844 |
| K2_tied_top | pair {0,1} to (0.80, 0.50) | 5000 | +1992.9 | -1182.9 | | 0.6660 to 0.4100 |

Readings.

1. The unique-top pair deviation gives the top agent exactly `(M_(2) - M_(3)) N_n = 0.25 N_n`, that is
   `255.5, 785.0, 1744.7` at `N_n = 1022, 3140, 6979`, the prediction of Theorem E2(i) to the digit at three
   horizons, and gives the runner-up exactly `L_n M_(2)`, that is `211.9, 403.0, 654.5`. Both members strictly
   gain, the outsider gains exactly nothing, no transfer is needed, and by Section 8.2 the resulting profile is
   self-enforcing: the runner-up's own deviation gain there is `0.0` and the winner's is `[811.1, 836.0]`
   against a slack of `2425`.
2. The tied-top pair deviation is also jointly profitable, `+1350.0` and `+1349.4` at `n = 10000` against the
   prediction `(1/2) N_n (M_top - theta) + L_n (M_top - theta) = 1046.9 + 302.1 = 1349.0`, so `S^star` is not a
   strong equilibrium there either. But the resulting profile is NOT self-enforcing: each member's own
   deviation gain at it is `2858` to `3230`, more than twice what the agreement pays it. That is Theorem
   E2(ii), and it is the reason the two-top condition protects revenue against pairs.
3. The last row is the asymmetric pair deviation on a two-top instance: one member gains `1992.9` and the other
   loses `1182.9`. Without transfers that is not a coalitional deviation at all, which is the content of
   Theorem E2(ii)'s case analysis.
4. The finite-horizon revenue drop splits exactly into the two predicted parts. On `unique_top` at
   `n = 10000`, the measured drop `0.5533 - 0.3134 = 0.2399` equals the price effect
   `(M_(2) - M_(3)) N_n / n = 0.25 x 0.6979 = 0.1745` plus the Stage-1 effect `L_n M_(2) / n = 0.0654`, which
   is the revenue the colluding runner-up stops delivering on its own bidding pulls. Both converge to the
   asymptotic statement `(M_(2) - M_(3)) n = 0.25 n` as `N_n / n -> 1` and `L_n / n -> 0`.

## 9. What is proved, what is assumed, and the step I trust least

### 9.1 Proved

- Theorem E1 sufficiency, in both cases, against the FULL behavioral class `B_{i,n}` (adaptive Stage-1 targets,
  bait and switch, arbitrary fallback play), with the manuscript's own constants. This is the negative result
  and it is the half I would defend in front of a referee. It reuses `lem:private-monitor`,
  `lem:selected-reactive-exp3`, the bidding coupling and equation `private-fallback-top` exactly as written,
  and substitutes `c` for `M` in the concentration event; no new lemma is introduced.
- Theorem E1 necessity, for profiles in `Sigma` with a fixed bid vector, by exhibiting for each excluded `c`
  one explicit deviation with gain at least a constant times `n`.
- Corollary E1.1 (revenue range, lower endpoint attained), Corollary E1.2 (exact runner-up gain), Theorem E2
  (pairs), Proposition E3 (no low-delivery fallback agreement), Proposition E5 (the adapted bonus repair, whose
  scope is the bid-choice inequality and its revenue consequence).
- The verification that the honest-benchmark bound holds under arbitrary collusion, by checking each of the
  five steps of the manuscript's robustness proof for a hidden independence-across-agents assumption.
- Every numerical statement in Section 8 is an exact computation with certified brackets, not a simulation.

### 9.2 Assumed

- (ND) `M_top < 1`. Used only to make winning worth a constant per round. Without it the knife edge of
  Section 5.4 opens and the characterization fails.
- The bid vector `c` is fixed, that is independent of `n`. For `n`-indexed bid vectors the two cases become
  asymptotic conditions (`liminf (c_W - V_W) > 0` in case (A); `c_i >= M_top - o(1)` on `K_top` in case (B));
  the sufficiency proof needs only `2 s_n < c_W - V_W` eventually, and the necessity proof needs the relevant
  capacity gaps to be `omega(s_n)`. I did not write out the `n`-indexed version.
- The profile family is `Sigma`: profiles that differ from `S^star` only in constant Stage-1 targets.
  Deviations are never restricted.
- The manuscript's three lemmas and the coupling are taken as correct. `lem:private-monitor` and
  `lem:selected-reactive-exp3` were checked in round 2 by another worker
  (`audit/round2/B/PRIVATE_BOUND_NOTES.md`); I re-read both and their proofs and found no step that the
  substitution of `c` for `M` disturbs, but I did not re-verify them.
- For Theorem E2 the pair's own deviation is a change of Stage-1 bids; the self-enforcement test allows
  arbitrary behavioral deviations by each member.

### 9.3 The step I trust least

The NECESSITY half, and specifically its restriction to `Sigma`. Inside `Sigma` the argument is complete,
because a losing agent's post-bid utility is bounded by `2 n` times the false-switch probability
`(2 n^3)^{-1}`, so losing really is worthless and the deviations of Section 2.2 dominate. Outside `Sigma` that
is no longer true: a general behavioral profile may have the primary winner deliberately fail the monitor, and
then every agent, including the losers, receives fallback selections, so "losing the bidding" is no longer
worth `O(n^{-2})` and the comparison that drives the necessity proof has an extra term I have not bounded.
Consequently the statement I would NOT put in the paper without more work is the strong form of the positive
half: "with `K_top >= 2`, EVERY additive behavioral equilibrium has revenue `M_(2) n - o(n)`". What is proved
is that statement restricted to `Sigma`.

Two things partially close the gap and are worth recording. First, Propositions E3 and E3.1 show that the
fallback has no low-delivery equilibrium in the constant-target family: its maximum delivery is at least
`M_(2) - o(1)` and its revenue is at least `M_(2) H - o(H)`, with no top-set assumption. So the extra term
cannot be sustained by an agreement among the agents, and the residual uncertainty is confined to fallback
strategies that vary within the phase, which `lem:selected-reactive-exp3` cannot bound because EXP3 carries no
monitor. Second, I checked
the simplest profile outside `Sigma` that could evade the necessity argument, namely the two top agents
randomizing independently between `M_top` and a common low bid `theta` with probability `p` and `1 - p`:
indifference between the two bids would require
`p (1/2) (1 + mu_1 - M_top) + (1 - p) (1 + mu_1 - theta) = (1 - p) (1/2) (1 + mu_1 - theta)`,
whose left side exceeds its right side term by term because both `1 + mu_1 - M_top >= 0` and
`1 + mu_1 - theta > 0`; so no such mixed equilibrium exists and bidding `M_top` is strictly better at the
linear scale. That is one family, not a proof.

A second, smaller reservation: Proposition E5 (the repair) proves the bid-pinning inequality and its revenue
consequence, but I have not re-derived the equilibrium and robustness parts of `thm:private-mesp` for the
modified mechanism. I would not put Proposition E5 in the paper without that.

### 9.4 Reproduction

```
VENV=<scratchpad>/venv/bin/python
$VENV audit/round2/B/theorems/e1-equilibrium-strength/bidprofile.py \
      --instance K2_unique_top --n 2000 5000 10000 --bids 0.70,0.35 --tag bad --out <outdir>
$VENV audit/round2/B/theorems/e1-equilibrium-strength/bidprofile.py \
      --instance K2_tied_top --n 2000 5000 --bids 0.50,0.50 --tag joint --out <outdir>
$VENV audit/round2/B/theorems/e1-equilibrium-strength/aggregate_e1.py <outdir>
```
`--bids M` reproduces the proposed profile; `run_e1.sh` is the Slurm wrapper used for the larger horizons.
Runtime is dominated by the `O(N_n^2)` primary-phase backward induction, once per distinct price; about
5 seconds per agent at `n = 2000` and about 3 minutes per agent at `n = 10000` for `K = 2`.

### 9.5 Suggested order of use

1. Take Corollary E1.1 and the eight-line main-text paragraph of Section 7 (E1-F1). This is the referee-proofing
   move and it costs eight lines.
2. Take the one-sentence coalition statement (E1-F2) and put Theorem E2 in the supplement.
3. Fix the related-work sentence (E1-F4); it is three lines and it removes the only comparison a referee could
   call misleading.
4. Consider replacing `prop:tightness` by the runner-up version (E1-F3), which is exact, shorter, and is the
   statement that explains the equilibrium set.
5. Treat Proposition E5 as a "future work" sentence, not as a theorem, unless someone re-derives the whole of
   `thm:private-mesp` for the modified mechanism.

# Part II: the same two questions for the profile-local contextual mechanism

Added 18 September 2026 on a resumed assignment. Read first, in full: `c2-local-mesp/PROVER2.md` and
`c2-local-mesp/ADVERSARY.md` (Sections 0, 1, 5, 9 and 10 line by line, the rest by section), and
`c2-local-mesp/COMPUTE_LOG.md`. I did not open `PROVER1.md` except through the adversary's adjudication of it.

## 9a. One-paragraph answer for Part II

The answer is different from Part I, and in the direction the brief hoped, but not for the reason the brief
gave. The conjectured cross-profile stake does not exist: by the candidate's own profile-locality lemma an
agent's bid at a profile moves nothing outside that profile, so a local loser's bid is exactly as free as in
the scalar mechanism and costs it `O(L_n)` per profile, `O(Q L_n) = o(n)` in total. What changes is the SCALE
at which each local auction is judged: the prize at a profile is its post-bidding length `N_z`, not `n`, so the
scalar dichotomy applies in full at profiles carrying a positive fraction of the visits and applies not at all
elsewhere. The equilibrium set is therefore a product over profiles of local equilibrium sets, and the revenue
guarantee over the whole set is the pointwise maximum of the paper's two guarantees, selected profile by
profile by the local two-top condition: `E sum_t [M_(2)(X_t) 1{|T(X_t)| >= 2} + b(X_t) 1{|T(X_t)| = 1}] - o(n)`,
attained at both ends on one instance. That is a strictly sharper statement than the scalar one. For
coalitions, the cross-profile channel is real as a joint deviation, market division between two agents that are
top at two profiles is linearly profitable even when the two-top condition holds everywhere, so `S^*` is not
pair-proof; but no market division is self-enforcing, because PL-MESP has no punishment technology at all (the
harshest action an agent has against another is to bid its capacity, which is exactly the proposed profile) and
because no observable depends on a deviator's bid at a profile before that profile's bidding ends. The exact
computations confirm the characterization inside a single instance, including the two different scalings (`L_n`
at a compliant profile, `N_z` at a violating one) and an exact zero for a local loser playing a local best
response. The one thing the computations add against the analysis is a finite-horizon caveat: a concession is
enforced here by the COST OF RE-ENTRY rather than by punishment, a deeper concession is harder to reverse, and
at horizons where `L_n` is a substantial fraction of `N_z` a deep market division is stable. The deterrent
switches on at a computable horizon, and the criterion predicted the switch correctly out of sample.

## 10. Scope and the mechanism analyzed

I analyze the composition the adversary recommends in its Section 9.4 and that the coordinator intends to put
in the paper: PROVER2's mechanism (one independent scalar MESP per exact context profile, round-robin Stage 1
of `K L_n` visits per profile, a single locally restarted EXP3 tuned once to the global horizon) with PROVER1's
calibration (`s_n = sqrt(log(2 K n^4)/(2 L_n))`, `b_n(r) = sqrt(r log(2 n^4)/2)`, that is the scalar constants).
Write `V_z` for the number of visits to profile `z`, `N_z := (V_z - K L_n)_+` for its local primary length,
`M_*(z)`, `T(z)`, `M_(2)(z)`, `b(z) = max_{h in K_H} mu_h^z` for the local primitives, and condition throughout
on the arrival path, as PROVER2 does (Convention F-A) and as (H3) permits, so that every `V_z` is a constant.
I take hypotheses (H1) to (H7) of `PROVER2.md` Section 4.1, with the adversary's repair F2 (the independences
are mutual, not pairwise) and its warning F1 (arrivals must not react to realized rewards). All three of those
are hypotheses of the candidate theorem; nothing below weakens or strengthens them.

Two structural facts from that material are the load-bearing inputs here, and I use them as given rather than
reproving them. First, **profile locality** (PROVER2 Lemma L, confirmed by the adversary's exhaustive channel
enumeration in its Section 5.1): every object the mechanism holds at `z` is a function of data collected at
visits to `z` and of coins attached to `z`, and every tuning constant is a function of `n` and `K` alone.
Second, **additive accounting** (PROVER2 equation (5.4)): `u_i = sum_z E[U_{i,z}]` pathwise and in expectation,
with no independence across profiles required, so a deviator that couples its behaviour across profiles is
handled by bounding each profile separately.

Nondegeneracy for Part II, (ND-ctx): `M_*(z) < 1` at every profile; put `kappa := 1 - max_z M_*(z) > 0`.

**The bid family.** `Sigma^ctx` is the set of profiles `S^c` indexed by an array `c = (c_{i,z})` with
`c_{i,z} in [0, M_i^z]` and `c_{h,z} >= mu_h^z` for honest `h`: agent `i` delivers the constant `c_{i,z}` on each
of its Stage-1 pulls at `z` and otherwise follows `S^*` (as local primary winner `min{tau_z, M_i^z}`, or the
honest version; capacity in the local fallback). `S^* = S^M`. Deviations always range over the full contextual
behavioural class `B^ctx_{i,n}` of the contract, including strategies that couple across profiles.

**Local conditions.** At a profile `z` say that `c_{.,z}` is
(A_z) if some agent `W` has `c_{W,z} > V_W^z := max_{j != W} M_j^z`, which forces `|T(z)| = 1` with `W` the
local top agent and `c_{W,z} > M_(2)(z)`; and
(B_z) if `|T(z)| >= 2` and `c_{i,z} = M_*(z)` for every `i in T(z)`.
Call `z` COMPLIANT if (A_z) or (B_z) holds and VIOLATING otherwise. These are the scalar conditions of
Theorem E1 evaluated at the local primitives.

## 11. The conjectured cross-profile stake does not exist, and what replaces it

The brief for this assignment conjectured that a loser's bid is no longer free in the contextual mechanism,
because bidding effort is paid once per profile and an agent that loses at one profile may win at another. That
is not so, and the reason is exactly the property that makes the candidate work.

By profile locality, agent `i`'s Stage-1 targets at `z` influence the mechanism's behaviour at `z` and nowhere
else: they enter `beta_{i,z}`, hence the local winner and the local price, and no other object the mechanism
holds. Winning at `z'` changes neither. So the stake an agent has in its own bid at `z` is exactly what it was
in the scalar mechanism, namely `L_n (M_i^z - c_{i,z})` of Stage-1 effort plus whatever its chance of winning
at `z` is worth, and the first is `O(L_n)` per profile and `O(Q L_n) = o(n)` in total. The contextual
mechanism does not couple the auctions; it runs `Q` of them side by side.

What does change, and this is the sharpening, is the SCALE at which each auction is judged. The equilibrium
definition tolerates `o(n)` in total, but the prize at `z` is worth `N_z`, not `n`. A deviation confined to `z`
can gain at most `2 V_z`, so at a profile visited `o(n)` times nothing is pinned at all, while at a profile
visited `Theta(n)` times the scalar dichotomy applies in full. The condition is therefore not "at every
profile" but "at almost every profile, measured in visits". That is Theorem C1.

## 12. Theorem C1: the equilibrium set of PL-MESP

> **Theorem C1.** Assume (H1) to (H7), (ND-ctx), fixed `K` and `Q`, and a fixed array `c` (independent of `n`),
> and condition on the arrival path. Then, with `Viol(c) := sum over violating z of V_z`:
>
> **(i) Sufficiency, per profile.** For every agent `i`,
> `sup_{S'_{i,n} in B^ctx_{i,n}} [u_i(n; S'_{i,n}, S^c_{-i,n}) - u_i(n; S^c_n)]`
> `<= Q (L_n + 1 + R_K(n)) + sqrt(2 Q n ell_n) + 2 Viol(c) + O(Q n^{-2})`,
> where the middle term is `sum_z 2 b_n(N_z) <= 2 sqrt(Q sum_z N_z ell_n / 2)` by Cauchy-Schwarz, which is
> PROVER2's own `e_mon` up to its additive `Q`.
>
> **(ii) Necessity, per profile.** If `z` is violating and `N_z > 0`, some agent has a deviation confined to
> `z` whose gain is at least `(kappa / K) N_z - 2 L_n - O(1)`. Consequently some single agent has a deviation
> whose gain is at least `(kappa / K^2) sum over violating z with N_z > 0 of N_z - 2 Q L_n - O(Q)`.
>
> **(iii) Characterization.** `S^c` is an additive behavioral asymptotic equilibrium if and only if
> `Viol(c) = o(n)`. In particular the local condition (A_z) or (B_z) must hold at every profile of positive
> visit frequency and need not hold anywhere else.

PROOF. (i) By additive accounting the total gain is the sum over profiles of the local gains, and a deviation
confined to `z` is evaluated against the local mechanism, which by profile locality is a scalar MESP with the
global constants `L_n, s_n, b_n(.)` and the local primary length `N_z`. At a compliant profile the proof of
Theorem E1 sufficiency (Section 2.1) applies word for word with `N_n` replaced by `N_z`, `V_W` by `V_W^z`,
`M_j` by `M_j^z`, and the fallback bound `R_K(H)` replaced by the prefix bound of PROVER2's Lemma F, which is
at most `R_K(n)` uniformly in the local length; the only inputs are the local monitor lemma (PROVER2 Lemma M,
which is stated for targets predictable in the global history and therefore covers a deviator that couples
across profiles), the local price identity `tau_z = (max_{j != i} beta_{j,z} - s_n)_+` on the event that `i`
wins at `z` (adversary Section 5.1 item 2), and the local bid-domination coupling (PROVER2 Lemma B, with
round-indexed seeds). At a violating profile bound the local gain by `2 V_z`. Summing gives the display. The
error terms are the manuscript's own: `Q L_n` is PROVER2's `e_bid`, `Q R_K(n)` its `e_fb`, and
`Q (1 + 2 b_n(n))` is dominated by its `e_mon = Q + sqrt(2 Q n ell_n)`.

(ii) At a violating `z`, Section 2.2 applied to the local primitives exhibits an agent `i` and a constant
Stage-1 target at `z` whose local gain is at least `(kappa / K) N_z` minus `2 L_n` and `O(1)`; the deviation is
"deliver that constant at every Stage-1 pull at `z`, and follow `S^c_i` everywhere else", which is a legitimate
element of `B^ctx_{i,n}` because it is a function of the current profile alone. Assign each violating profile
to one such agent and let `i^*` be an agent assigned profiles with the largest total `N_z`; by pigeonhole that
total is at least `1/K` of the whole. The deviation "use the violating target at every profile assigned to
`i^*`, and `S^c` elsewhere" is again in `B^ctx_{i^*,n}`, and by additive accounting its gain is the sum of the
per-profile gains, giving the second display.

(iii) If `Viol(c) = o(n)` then (i) is `o(n)` because `Q L_n = o(n)` for fixed `Q`. If `Viol(c) != o(n)` then
along a subsequence `Viol(c) >= eps n`, and since `N_z >= V_z - K L_n` the profiles concerned have
`sum N_z >= eps n - Q K L_n >= (eps/2) n` eventually, so (ii) gives an agent a gain of at least
`(kappa eps / (2 K^2)) n - 2 Q L_n`, which is not `o(n)`. Q.E.D.

> **Corollary C2 (the revenue of the equilibrium set is a pointwise interpolation).** Under the hypotheses of
> Theorem C1, at every additive equilibrium in `Sigma^ctx`,
>
>   `P(n; S^c) >= sum_z V_z g(z) - O(Q K L_n + n s_n + Q R_K(n))`,
>   `g(z) := M_(2)(z)` if `|T(z)| >= 2`,  `g(z) := b(z)` if `|T(z)| = 1`,
>
> and the bound is attained: taking (B_z) at every two-top profile and (A_z) with every loser at its lowest
> feasible bid at every unique-top profile gives an additive equilibrium whose revenue equals the right side up
> to the same error. Taking expectations over the arrival path,
> `min over equilibria of P(n; S) = E sum_{t<=n} [ M_(2)(X_t) 1{|T(X_t)| >= 2} + b(X_t) 1{|T(X_t)| = 1} ] +- o(n)`.

PROOF. Per profile, exactly as in Corollary E1.1: at a compliant two-top profile the price concentrates at
`M_*(z) = M_(2)(z)`; at a compliant unique-top profile the losers' bids are unconstrained and the local revenue
rate is `max{max_{k != W} c_{k,z}, mu_W^z 1{W honest}}`, which ranges over
`[b(z), max{b(z), M_(2)(z)}]` as the losers' bids range over their feasible sets; violating profiles contribute
at most `Viol(c) = o(n)`. Summing and charging the `Q K L_n` Stage-1 rounds, the `2 n s_n` price shading and
the `Q R_K(n)` fallback terms gives the display; the honest-benchmark part (C) of the candidate theorem shows
that no profile of any kind can go below `sum_z V_z b(z)` by more than the same order. Q.E.D.

This is a strictly better statement than the scalar one, and it is the answer to the question in the brief.
The two-top condition does not have to hold everywhere; it has to hold at the profiles that carry a positive
fraction of the visits, and where it fails the mechanism falls back exactly to the honest benchmark AT THAT
PROFILE rather than globally. The guaranteed revenue over the whole equilibrium set is the pointwise maximum of
the paper's two guarantees, selected profile by profile by the local two-top condition, and no coarser
statement is available: both endpoints are attained at genuine equilibria of the same instance.

**Remark C1.1 (what "almost every profile" means, honestly).** Under i.i.d. arrivals with law `nu` on a finite
`X_F`, `V_z / n -> nu(z)`, so the positive-frequency profiles are exactly the support of `nu` and Theorem
C1(iii) reads: the local condition must hold at `nu`-almost every profile, which for an instance with all
masses positive is the same as at every profile. The relaxation therefore bites exactly in the regime in which
the candidate theorem is stronger than the manuscript's grid results, namely the non-i.i.d. exogenous arrivals
that (H3) allows: a profile whose share of the visits vanishes, for example one visited `n^{3/4}` times, is
completely unconstrained, its local price may be anything down to the local honest floor, and its contribution
to revenue is `o(n)` either way. I would state it as "at every profile carrying a positive fraction of the
visits" rather than as "almost everywhere", because the second phrase suggests a measure-zero relaxation that
is unavailable when all masses are positive.

## 13. Coalitions in the contextual mechanism

### 13.1 The structural fact: PL-MESP has no punishment technology

Every cartel needs two things: a signal that a member defected, and an action that hurts the defector more than
the deal pays it. PL-MESP supplies neither, and the second failure is exact.

> **Lemma C3.0 (the harshest action is the proposed one).** Fix agents `i != j`, a profile `z`, and any
> behaviour of the agents other than `j`. Over all `S'_j in B^ctx_{j,n}`, agent `i`'s expected utility at
> visits to `z` is minimized, up to `1 + 2 b_n(n) + R_K(n) + O(V_z n^{-2})`, by `j` playing `S^*_j` at `z`.
>
> PROOF. Split `i`'s utility at `z`. (a) Its Stage-1 utility at `z` is `L_n (1 + mu_i^z - c_{i,z})`, a function
> of its own targets only: `j` cannot touch it. (b) On the event that `i` wins at `z`, its post-bidding utility
> is at most `N_z (1 + mu_i^z - tau_{i,z}) + 1 + 2 b_n(n) + R_K(n)` and at least
> `N_z (1 + mu_i^z - tau_{i,z}) - O(V_z n^{-2})` when it plays `S^*`, where
> `tau_{i,z} = (max_{l != i} beta_{l,z} - s_n)_+` does not depend on `i`'s own bid; this is decreasing in
> `tau_{i,z}`, and `tau_{i,z}` is nondecreasing in `beta_{j,z}`, which is stochastically largest at the
> capacity target. So `j` hurts `i` most by bidding `M_j^z`, which is `S^*_j`. (c) Raising `beta_{j,z}` also
> weakly lowers the probability that `i` wins at all, and on the event that `i` loses its post-bidding utility
> is nonnegative and is zero unless a local switch occurs at `z`; `j` can only create switches, never prevent
> `i` from being selected in a fallback, so every other choice of `j` weakly ADDS to `i`'s payoff. Hence the
> minimum over `S'_j` is attained, to the stated accuracy, at "bid capacity and, as local winner, deliver at
> least the price", which is `S^*_j`. Q.E.D.

The lemma holds verbatim in the scalar mechanism (`Q = 1`) and explains Part I in one line: the reason the
two-top joint underbid of Theorem E2(ii) is not self-enforcing is not a detail of that computation, it is that
the only threat available to a partner is competitive bidding, and competitive bidding is the proposed profile.
A cartel here can only agree to be softer than `S^*`; it can never agree to be harsher, so it has no way to
pay for a concession.

The signal fails too, and in a way worth recording. The mechanism tells an agent the local price `tau_z` only
when it selects that agent at `z` after Stage 1 there (PROVER2 Section 2, "Messages"). A LOSER at `z` is never
selected at `z` again unless a local switch occurs, so it never learns `tau_z`. Hence the only cartel member
who can verify a concession at `z` is the member who won `z`, and it learns it only after `t_1(z)`, the round
of the `K L_n`-th visit to `z`. Any punishment must therefore be delivered through a bid at a profile whose
Stage 1 is still open at that moment.

### 13.2 Theorem C3

> **Theorem C3.** Assume (H1) to (H7), (ND-ctx), fixed `K` and `Q`, and condition on the arrival path.
> Consider pair deviations from `S^*` inside `Sigma^ctx` (the two members change only their Stage-1 targets,
> at any profiles they like); self-enforcement is tested against arbitrary deviations in `B^ctx` by each member.
>
> **(i) Within a profile.** Theorem E2 applies at each profile with `n` replaced by `V_z`: at a unique-top
> profile the local top agent and the local runner-up have a jointly profitable and self-enforcing concession
> that lowers the local revenue rate to `max{M_(3)(z), b(z)}`; at a profile with `|T(z)| = 2` a joint underbid
> is profitable but not self-enforcing; at a profile with `|T(z)| >= 3` no pair gains.
>
> **(ii) Across profiles: market division is profitable.** Suppose two agents `i, j` are both in `T(z)` at two
> profiles `z_1, z_2` with `V_{z_1}, V_{z_2} = Theta(n)`, and that `T(z_1) = T(z_2) = {i, j}`. The scheme "`i`
> bids its capacity at `z_1` and its lowest feasible target at `z_2`, `j` the mirror image" is jointly
> profitable: each member's gain is
> `N_{z_m} (1 + mu^{z_m} - theta_m) - (1/2)[N_{z_1}(1 + mu^{z_1} - M_*(z_1)) + N_{z_2}(1 + mu^{z_2} - M_*(z_2))]`
> at its own profile `z_m`, where `theta_m` is the highest remaining bid there, and this is linear and positive
> whenever `M_*(z) - theta` is bounded away from zero. Platform revenue falls by
> `sum_m N_{z_m} (M_*(z_m) - max{theta_m, b(z_m)})`. So `S^*` is NOT pair-proof even when the two-top condition
> holds at every profile, and the local two-top condition does not protect against cross-profile pairs.
>
> **(iii) Across profiles: no market division is self-enforcing.** Call `z` CONCEDED under a pair deviation if
> some member `j` has `c_{j,z} < M_j^z`. Suppose every profile with `V_z = Omega(n)` has `|T(z)| >= 2`. Then no
> jointly profitable pair deviation in `Sigma^ctx` is self-enforcing. Consequently `S^*` is pair-coalition-proof
> and every self-enforcing pair deviation leaves revenue at `sum_z V_z M_(2)(z) - o(n)`.
>
> PROOF of (iii). Suppose the pair `{1,2}` deviates to `c` and the deviation is jointly profitable, so at least
> one profile with `V_z = Omega(n)` is conceded (if no such profile is conceded, then at every positive-frequency
> profile both members bid capacity, the prices and the winning probabilities are those of `S^*` up to the usual
> error, and the gain is `O(Q L_n + Q sqrt(n log n)) = o(n)` for both members). Fix `eps > 0` with
> `V_z >= eps n` for at least one conceded profile, and let `z^*` be the conceded profile with `V_{z^*} >= eps n`
> whose Stage 1 completes LAST, that is with the largest `t_1(z)`.
>
> First, some member conceding at `z^*` is in `T(z^*)`. Indeed, the price at `z^*` is
> `(beta_(2),z^* - s_n)_+` and every agent outside the pair bids its capacity, so if every member of
> `T(z^*) \ {W_{z^*}}` bid its capacity the second order statistic would already be `M_*(z^*)` up to `s_n` and no
> concession could lower the price; since `|T(z^*)| >= 2`, the set `T(z^*) \ {W_{z^*}}` is nonempty and must
> therefore contain a conceding member `j`.
>
> Second, `j` deviates unilaterally by bidding `M_j^{z^*} = M_*(z^*)` at `z^*` and changing nothing else. By
> (E1) applied locally it then wins at `z^*` with probability at least `1/K` at a price at most `M_*(z^*)`, so
> its gain at `z^*` is at least `(kappa / K) N_{z^*} - L_n - O(1)`, which is `Omega(n)`.
>
> Third, its loss elsewhere is `o(n)`. Its own bids elsewhere are unchanged, so by profile locality the only
> way its payoff at another profile `z'` can change is through the partner's reaction. That reaction cannot
> begin before `t_1(z^*)`, and this is exact rather than approximate: the mechanism's only use of `j`'s Stage-1
> targets at `z^*` is through `beta_{j,z^*}`, which is formed at `t_1(z^*)`, so no observable of any agent other
> than `j` is a function of those targets before that round; and after that round the partner's only signal is
> `tau_{z^*}`, which reaches it only if it is selected at `z^*` (Section 13.1). So the partner can react only at
> profiles with `t_1(z') > t_1(z^*)`. By Lemma C3.0 the harshest reaction available to the partner at such a
> `z'` is to play `S^*_partner` there. If `z'` is not conceded the partner is already playing `S^*` there, so
> the reaction changes nothing; if `z'` is conceded then `V_{z'} < eps n` by the choice of `z^*`, and the total
> effect of all such profiles is at most `2 sum_{conceded z' : V_{z'} < eps n} V_{z'} <= 2 Q eps n`. Taking
> `eps` smaller than `kappa / (2 K Q)` makes the third term smaller than half the second. Hence `j` has a
> unilateral gain of `Omega(n)` from the deviated profile, so the deviation is not self-enforcing. The revenue
> statement follows because a self-enforcing pair deviation concedes no positive-frequency profile, so every
> positive-frequency profile has two bids at `M_*(z)` and its price is `M_(2)(z) - O(s_n)`. Q.E.D.

What (iii) adds to Theorem C1 is worth isolating. If both members are restricted to constant bids, then the
deviated profile is itself a member of `Sigma^ctx`, a market division concedes at some profile and therefore
violates (A_z) and (B_z) there, and Theorem C1(ii) already says some agent has an `Omega(V_z)` gain, which is
non-self-enforcement. The content of (iii) is that TRIGGER strategies do not rescue the scheme: a partner whose
bid at one profile is a function of the price it saw at another is not in `Sigma^ctx`, and the two ingredients
that kill it are the timing (no observable depends on the deviator's bid at `z^*` before `t_1(z^*)`) and Lemma
C3.0 (after `t_1(z^*)` the partner's harshest available action is the one it is already taking).

Three remarks on (iii). First, the argument never uses the arrival order, although the order decides whether
the signal exists at all: when the Stage-1 windows of two profiles overlap, as they do under i.i.d. arrivals
with both profiles frequent, neither member can condition its bid at one profile on the price at the other and
the scheme is unenforceable for a second, independent reason. Second, the hypothesis that every
positive-frequency profile has `|T(z)| >= 2` is exactly the hypothesis of Theorem C1 case (B), so the coalition
result and the unilateral result hold under one and the same condition; where it fails, the concession at a
unique-top profile is self-enforcing, which is part (i), and the revenue loss there is already counted in
Corollary C2. Third, the cross-profile channel the brief asked about therefore EXISTS as a profitable joint
deviation and ADDS NOTHING as a self-enforcing one: the set of self-enforcing pair outcomes is exactly the set
described by the local dichotomy, profile by profile.

### 13.3 The honest benchmark under contextual collusion

Part (C) of the candidate theorem is already stated for arbitrary joint behavioural play. I checked its proof
(`PROVER2.md` Section 5.8) for a hidden independence-across-agents assumption, as I did for the scalar proof in
Section 4.4, and there is none. Its four steps are: a one-sided exponential supermartingale bound on the
honest agent's own local bid, which uses only honesty and the freshness of that agent's own reward seeds; the
order-statistic inequality `beta_(2),z >= beta_{h,z}` when `h` is not the local winner; the local monitor lemma,
which holds for arbitrary predictable targets of whoever won and therefore for coordinated ones; and Lemma F
with the honest agent as comparator, which requires only that `h`'s conditional mean when selected is at least
`b(z)`, again by honesty alone. The per-profile split that precedes all four is additive accounting, which
needs no independence at all. So `P(n; S) >= E sum_t b(X_t) - o(n)` holds under collusion by any subset of the
agents, up to and including all `K` of them, and by Corollary C2 it is attained at an equilibrium as soon as one
positive-frequency profile has a unique local top. The one hypothesis that matters is the one the adversary
found: arrivals must not react to realized rewards (its finding F1), and that is a hypothesis about the world
rather than about the agents.

## 14. Findings for Part II

**E1-F6 (P2, contribution, new result not a correction).** The candidate contextual theorem
(`c2-local-mesp/PROVER2.md` Section 4.3, parts (A), (B), (C)) is a statement about `S^*` and about arbitrary
play; it says nothing about the rest of the equilibrium set, exactly as the scalar theorem does not. Theorem C1
and Corollary C2 supply the missing quantifier, and in the contextual case the answer is strictly more
informative than in the scalar case: the guarantee over the whole equilibrium set is
`E sum_t [M_(2)(X_t) 1{|T(X_t)| >= 2} + b(X_t) 1{|T(X_t)| = 1}] - o(n)`, the pointwise maximum of the paper's
two guarantees selected profile by profile, and both endpoints are attained on the same instance. Parts (A),
(B) and (C) of the candidate are untouched. The condition that has to hold is local and only at
positive-frequency profiles, which is the sharpened form of the two-top condition the brief asked about.

**E1-F7 (P2, contribution).** `S^*` of PL-MESP is not resistant to a pair of agents that divides the profile
set between them, even when the local two-top condition holds at every profile; the joint gain and the revenue
loss are the displayed quantities of Theorem C3(ii). It is, however, pair-coalition-proof: no jointly
profitable pair deviation is self-enforcing (Theorem C3(iii)), for the structural reason of Lemma C3.0. At a
multiagent venue the market-division question is the first one a reviewer asks of a mechanism with several
independent auctions, and the answer here is favourable and cheap to state.

**E1-F8 (P3, design note with a reason).** The mechanism announces `tau_z` only to an agent it selects at `z`
(PROVER2 Section 2, "Messages"), so a losing agent never learns the local price. That clause is currently
justified only by the need to make `S^*` implementable. It has a second justification that should be recorded,
because it is a reason not to change it later: the announced price is the only channel through which one agent
can learn anything about another agent's bid, so restricting it to selected agents is what leaves a
cross-profile cartel without a verification device at the profiles it concedes. Broadcasting the price would
not by itself make market division self-enforcing, since Lemma C3.0 removes the punishment rather than the
signal, but it would remove the second of the two independent obstacles.

**E1-F9 (P3, precision, the contextual form of E1-F3).** PROVER2's Proposition 6.1 shows the `Q L_n` bidding
term is attained by the agent that is the unique local top, summed over the profiles where it is. The
runner-up version is again the one that explains the equilibrium set and is again exact: at each profile the
local runner-up gains exactly `L_n (M_(2)(z) - c')` by lowering its local bid to any feasible `c'`, with no
coupling of the post-bidding phase needed, and the sum over profiles is the path from `S^*` to the worst
equilibrium, taken in strictly improving unilateral steps at each profile independently.

**E1-F10 (P3, a simpler witness for the candidate's own `Q L_n` term).** PROVER2's Proposition 6.1 attains
`e_bid = Q L_n` by underbidding to the midpoint at the profiles where the deviator is the unique local top,
with constant `(M_i^z - V_i^z)/2`. A simpler and larger witness exists at any profile whose post-bidding length
is short: not bidding there at all. Abandoning the bid at `z` saves `L_n M_i^z` and forfeits at most
`(1/|T(z)|) N_z (1 + mu_i^z - tau_z)`, so it is a strict gain whenever
`N_z < |T(z)| L_n M_i^z / (1 + mu_i^z - tau_z)`, with no top-set condition and with the constant `M_i^z` rather
than `(M_i^z - V_i^z)/2`. The exact computation confirms it to within rounding (Section 17.3 reading 2:
predicted `627.9`, computed `626.8`). This matters for the paper only as a cleaner tightness example, and it
also makes the point that the `Q L_n` term is not an artifact of unique-top profiles.

## 15. What Part II proves, assumes, and the step I trust least

**Proved.** Theorem C1 sufficiency against the full contextual behavioural class `B^ctx_{i,n}`, including
strategies that couple across profiles, using the candidate's own Lemmas L, M, F, B and its additive
accounting, with the scalar argument of Section 2.1 run once per profile. Theorem C1 necessity for fixed
constant-bid arrays. Corollary C2. Lemma C3.0 and Theorem C3, with (iii) proved against arbitrary behavioural
responses by the partner.

**Assumed.** All of (H1) to (H7) of the candidate, with the adversary's F1 and F2 repairs; the profile family
`Sigma^ctx` (constant Stage-1 targets per profile, `S^*` elsewhere) for the profiles being characterized, never
for deviations; fixed `K`, `Q` and a fixed array `c`; (ND-ctx); and conditioning on the arrival path, which the
candidate's own proofs also do. For Theorem C3, pair deviations are bid changes; self-enforcement is tested
against everything.

**The step I trust least, again the necessity half, and for the same reason as in Part I.** Outside
`Sigma^ctx` a local winner may deliberately fail its local monitor, after which the losers at that profile
receive local fallback selections, so "losing the local bidding is worth `O(V_z n^{-2})`" fails and the
comparison driving Theorem C1(ii) acquires a term I have not bounded. Propositions E3 and E3.1 of Part I apply
locally and say the local fallback has no low-delivery equilibrium, which closes the same part of the gap as
before and no more. So the statement I would not put in the paper is "with `|T(z)| >= 2` at every
positive-frequency profile, EVERY additive behavioural equilibrium earns `sum_z V_z M_(2)(z) - o(n)`"; what is
proved is that statement restricted to `Sigma^ctx`.

A second and smaller reservation, specific to Part II: Theorem C3(iii) uses that the partner's reaction cannot
start before `t_1(z^*)`. That is exact for the mechanism as specified. It would stop being exact if a later
draft broadcast the price, gave any feedback to unselected agents, or let one profile's phase depend on another
profile's data, which is also the design change the adversary's Section 5.1 item 1 warns against for a
different reason. The two warnings are the same warning.

## 16. No repair is proposed for the contextual mechanism, and what one would cost

The instruction carried over from Part I is that I may not propose the bonus-round device for PL-MESP unless I
also re-derive the rest of the theorem for the modified mechanism, which I have not done and do not propose to
do here. For the record, the reason is not only the missing re-derivation. The device of Proposition E5 gives
each agent a number of bonus pulls increasing in its own bid; in the contextual mechanism a bid exists per
profile, so the device would have to be applied per profile, at a cost of `Q K G_n` rounds of essentially zero
revenue with `G_n = omega(eps_n)`. The candidate's headline limitation is already that the error terms carry a
factor `Q` and that the whole statement is vacuous unless `Q K L_n = o(n)`, that is unless
`Q = o(n^{1/3} (log n)^{-1/3} / K)` (PROVER2 Remark 4.1). Adding `Q K G_n` with `G_n` strictly larger than
`L_n` would tighten that regime further, by the same factor by which `G_n` exceeds `L_n`. A contextual repair
that pins the equilibrium price is therefore not a free upgrade: it trades the number of profiles the mechanism
can handle against the size of the equilibrium set, and the trade should be computed before it is offered.
The alternative I would put in the paper instead is Corollary C2, which costs nothing and states what is true.

## 17. Exact computations for Part II

`ctxprofile.py` (this directory) evaluates a profile-local bid array exactly. It reuses the machinery of
`bidprofile.py` once per profile, with the global constants `L_n`, `s_n`, `b_n(.)`, the LOCAL primary length
`N_z = V_z - K L_n`, and the fallback bound replaced by the prefix bound of the single local EXP3 tuned to `n`,
`min{2H, 2 gamma_n H + K log K / gamma_n, R_K(n)}` with `gamma_n = min{1/2, sqrt(K log K / n)}`. Utilities and
revenue are summed over profiles, which is exact by PROVER2's equation (5.4). The arrival path enters only
through the visit counts `V_z`, as the candidate's own proofs assume. Instances are in `ctxinstances.json`:

- `ctx_mixed`, `K = 2`, agent 1 honest, two profiles of equal share: `z1` with `mu = (0.10, 0.35)`,
  `M = (0.90, 0.65)` (unique local top, `M_(2)(z1) = 0.65`, `b(z1) = 0.35`) and `z2` with `M = (0.80, 0.80)`
  (two local tops, `M_(2)(z2) = 0.80`, `b(z2) = 0.35`).
- `ctx_division`, `K = 2`, agent 1 honest, two identical profiles of equal share with `M = (0.80, 0.80)`, so
  the local two-top condition holds everywhere.
- `ctx_rare`, the same two profiles with shares `0.75` and `0.25`.

Horizons are `n = 8000` for every configuration and `n = 20000` for the two that decide the characterization
(`ctx_mixed` violating at both profiles, and the `ctx_division` market division). The `n = 20000` runs of the
two capacity baselines and of `ctx_mixed` violating at `z1` only were still computing when this report was
finalized, so the coalition-gain comparison and the revenue comparison are quoted at `n = 8000`, where both
sides of each comparison exist; every number quoted comes from a completed configuration. The JSON files are
in `results/` and the tables come from `aggregate_ctx.py`.

### 17.1 The dichotomy is profile-local, and profile locality is visible in the numbers

At `n = 8000` (`L_n = 862`, `K L_n = 1724`, `V_z = 4000`, `N_z = 2276`, per-agent slack about `3446`):

| instance | bid array | revenue/round | at `z1`: exploit agent 0, agent 1 | at `z2`: exploit agent 0, agent 1 |
| - | - | - | - | - |
| ctx_mixed | `S^star` | 0.6660 | [377.1, 470.8], [258.6, 258.6] | [174.6, 197.9], [103.7, 149.4] |
| ctx_mixed | bad at `z1` only | 0.5268 | [460.6, 533.0], [0.0, 0.0] | [174.6, 197.9], [103.7, 149.4] |
| ctx_mixed | bad at both | 0.3776 | [460.6, 533.0], [0.0, 0.0] | [997.7, 1073.3], [1094.3, 1094.3] |

Readings.

1. **The local bad equilibrium exists at the unique-top profile and only there.** Replacing the bid vector at
   `z1` by `(0.70, 0.35)`, which satisfies (A_z1), leaves both agents with gains inside the slack and makes the
   local loser's gain exactly `0.0`: at `z1` the honest agent is playing an exact best response. Replacing the
   bid vector at `z2` by `(0.50, 0.50)`, which violates (B_z2), raises the local gains by an order of magnitude,
   to `1073` and `1094` from `198` and `149`.
2. **Profile locality is exact in the arithmetic, not approximate.** The `z2` columns of the first two rows are
   identical to the last printed digit: changing the entire bid vector at `z1` changes nothing whatever at
   `z2`. That is PROVER2's Lemma L and equation (5.4) showing up as an identity between two independent exact
   computations.
3. **The local revenue moves exactly as Corollary C2 predicts.** The revenue per visit at `z1` falls from
   `0.6201` to `0.3417` while `z2` stays at `0.7119`; the design values are `M_(2)(z1) = 0.65`, `b(z1) = 0.35`
   and `M_(2)(z2) = 0.80`, each less the local shading `2 s_n` and the Stage-1 accounting. The equilibrium-set
   floor of Corollary C2 for this instance is `(0.35 + 0.80)/2 = 0.575` per round asymptotically, against the
   claimed `(0.65 + 0.80)/2 = 0.725`; the measured pair is `0.5268` and `0.6660`.
4. **Corollary E1.2 holds locally and exactly.** At `S^star` the local runner-up's gain at `z1` is
   `258.6 = L_n (M_(2)(z1) - mu_1) = 862 x 0.30`, to machine precision, and it is the whole of that agent's
   gain at that profile.

### 17.2 Market division: jointly profitable, and what the numbers do and do not settle

`ctx_division` at `n = 8000`, both profiles two-top, division = agent 0 takes `z1` (bids `0.80` there, agent 1
bids its honest floor `0.35`) and agent 1 takes `z2` (bids `0.80` there, agent 0 bids `0`):

| bid array | revenue/round | agent 0 utility | agent 1 utility | agent 0 exploit | agent 1 exploit |
| - | - | - | - | - | - |
| `S^star` | 0.7119 | 1552.4 | 2552.4 | [349.2, 395.7] | [207.5, 298.8] |
| division | 0.3674 | 3248.7 | 3612.1 | [549.4, 638.3] | [905.9, 951.5] |

and, per profile, which is where the content is:

| bid array | profile | revenue/visit | agent 0 exploit there | agent 1 exploit there |
| - | - | - | - | - |
| `S^star` | `z1` and `z2` alike | 0.7119 | [174.6, 197.9] | [103.7, 149.4] |
| division | `z1` (agent 0 monopolizes, agent 1 concedes) | 0.3632 | [546.8, 612.5] | [518.0, 563.6] |
| division | `z2` (agent 1 monopolizes, agent 0 concedes) | 0.3716 | [2.6, 25.9] | [387.9, 387.9] |

1. **Theorem C3(ii) is confirmed exactly.** Both members gain, by `+1696.3` and `+1059.7`, and platform revenue
   falls from `0.7119` to `0.3674` per round, a loss of `0.3445 n`. The local two-top condition holds at both
   profiles, so this is a linear joint gain that the condition does not prevent: `S^*` is not pair-proof
   against a cross-profile pair.
2. **Theorem C3(iii) is NOT confirmed by these numbers, and I want to be exact about why.** At the division
   profile both members do have positive deviation gains (`638.3` and `951.5`), which is the direction the
   theorem predicts, but at `n = 8000` those gains are well inside the mechanism's own slack (about `3446`), so
   the computation cannot distinguish "not self-enforcing" from "self-enforcing at this horizon". Worse, the
   arithmetic says the second reading is the right one at this horizon: the theorem's own threshold for the
   contest at a conceded profile to pay is `N_z > K L_n / kappa`, here `2276 > 2 x 862 / 0.2 = 8620`, which
   fails by a factor of four. Concretely, for agent 0 to contest `z2` it must raise its bid there from `0` to
   `0.80`, costing `L_n x 0.80 = 690` of Stage-1 effort, while the prize is half of
   `N_{z2} (1 + mu_0 - M_top) = 2276 x 0.30`, that is `341`. The per-profile table shows exactly that: agent
   0's gain at the profile it conceded is `[2.6, 25.9]`, essentially zero, so its concession IS self-enforcing
   at this horizon. Agent 1's concession at `z1` is not, `[518.0, 563.6]`, but for an instance-specific reason
   rather than the theorem's: its honest floor `0.35` is already close to `0.80`, so contesting costs it only
   `L_n x 0.45` instead of `L_n x 0.80`. The remaining entries are Stage-1 shading and are exact: agent 1's
   `387.9` at the profile it monopolizes is `L_n (0.80 - 0.35) = 862 x 0.45`, the local Corollary E1.2 again.
3. **The exact finite-`n` criterion, and why it explains both entries.** What enforces a concession here is
   not a punishment but a RE-ENTRY COST: the conceder lowered a bid, a bid is delivered performance, and buying
   its way back in costs `L_n (M_j^z - c_{j,z})` of Stage-1 effort, while the prize is a `1/|T(z)|` share of
   `N_z (1 + mu_j^z - tau^post)`, where `tau^post = M_*(z) - s_n` is the price once the contest restores a
   second capacity bid. So, to leading order, the concession is self-enforcing exactly when

     `(1/|T(z)|) N_z (1 + mu_j^z - tau^post)  <  L_n (M_j^z - c_{j,z})`.

   At `n = 8000` (`N_z = 2276`, `L_n = 862`, `s_n = 0.1472`, `tau^post = 0.6528`) this reads, for agent 0 at
   the profile it conceded to `0`: prize `(1/2)(2276)(1.10 - 0.6528) = 508.9` against cost
   `862 x 0.80 = 689.6`, so it does not contest, and the measured gain there is `[2.6, 25.9]`. For the honest
   agent 1 at the profile it conceded to its floor `0.35`: prize `(1/2)(2276)(1.35 - 0.6528) = 793.4` against
   cost `862 x 0.45 = 387.9`, so it does contest, net about `405`, and the measured gain there is
   `[518.0, 563.6]`, the difference being the adaptive Stage-1 and monitor-boundary play that the exact
   deviator also has. Note the direction: a DEEPER concession is MORE enforceable, because it costs more to
   reverse, which is the opposite of the usual cartel logic and is specific to a mechanism in which bidding is
   delivered performance. The same criterion explains the scalar numbers of Section 8.3: at the two-top joint
   underbid on `K2_tied_top` at `n = 5000` the prize is `(1/2)(3760)(1.10 - 0.3316) = 1444.6` against a cost of
   `620 x 0.30 = 186`, so the agreement is far from enforceable, which is why the measured gain there is
   `1638.7` rather than a few hundred. Theorem E2(ii) and Theorem C3(iii) are the asymptotic form of this one
   inequality, which fails for every fixed concession once `N_z / L_n` is large enough.
4. **So the deterrent to market division is asymptotic, the crossover is computable, and it is close.** The
   criterion fails, that is the contest becomes profitable, when `N_z / L_n > |T| (M_j - c) / (1 + mu_j -
   tau^post)`, here `2 x 0.80 / 0.4472 = 3.58` for agent 0's deepest concession. At `n = 8000` the ratio is
   `2276 / 862 = 2.64` and the concession holds; at `n = 20000` it is `6732 / 1634 = 4.12` and the same
   arithmetic gives prize `(1/2)(6732)(1.10 - 0.688) = 1386.8` against cost `1634 x 0.80 = 1307.2`, so the
   concession should just fail. That is a prediction of the criterion at a horizon I had not computed when I
   wrote it, and Section 17.4 reports what the exact computation at `n = 20000` actually gave. In general the
   ratio `N_z / L_n` grows like `n^{1/3} (log n)^{-1/3} / Q`, so every fixed concession eventually becomes
   unenforceable and Theorem C3(iii) takes over, but the horizon at which that happens grows like the cube of
   `Q` and of the reciprocal of the winner's per-round surplus. At smaller horizons deep market divisions are
   stable. This is a finite-horizon limitation of the same kind as the non-top branch of the scalar theorem
   (`PRIVATE_BOUND_NOTES.md` note 3), it is a property of the mechanism rather than of my analysis, and it
   should be stated if the coalition result is stated.

### 17.3 The weight of a profile is `N_z`, and short profiles are not worth bidding at

`ctx_rare` is `ctx_division`'s instance with unequal shares: `V_{z1} = 6000` and `V_{z2} = 2000` at
`n = 8000`, so after the fixed Stage-1 toll of `K L_n = 1724` visits the post-bidding lengths are
`N_{z1} = 4276` and `N_{z2} = 276`. Both profiles are two-top, so both are violating under the joint underbid
`(0.50, 0.50)`.

| bid array | profile | `N_z` | revenue/visit | agent 0 exploit there | agent 1 exploit there |
| - | - | - | - | - | - |
| `S^star` | `z1` | 4276 | 0.6896 | [148.8, 195.6] | [140.1, 186.5] |
| `S^star` | `z2` | 276 | 0.7786 | [626.8, 626.8] | [290.6, 290.6] |
| joint underbid | `z1` | 4276 | 0.3917 | [1808.2, 1884.7] | [2094.3, 2094.3] |
| joint underbid | `z2` | 276 | 0.4790 | [326.6, 326.6] | [102.7, 102.7] |

Readings.

1. **The local gain scales with `N_z`, not with `V_z`.** The same violating bid vector is worth `1885` and
   `2094` at the profile with `N_z = 4276` and `327` and `103` at the profile with `N_z = 276`. A profile whose
   share of the post-bidding rounds vanishes therefore contributes a vanishing share of the deviation gain,
   which is the mechanism behind Theorem C1(iii). Note that `z2` carries `25` percent of the visits but only
   `6` percent of the post-bidding rounds, because Stage 1 takes `K L_n` visits at every profile whatever its
   frequency: the fixed toll protects short profiles from the equilibrium condition twice over.
2. **At `S^star` itself, an agent's best deviation at a short profile is to stop bidding there, and the exact
   number is the obvious one.** Agent 0's gain at `z2` under `S^star` is `626.8`, and abandoning the bid
   entirely saves `L_n M_0 = 862 x 0.80 = 689.6` of Stage-1 effort at the cost of its half share of the small
   prize, `(1/2) N_{z2} (1 + mu_0 - tau) = (1/2)(276)(1.10 - 0.6528) = 61.7`; the difference is `627.9`, which
   is the computed value to within rounding. So the deviation that attains PROVER2's `e_bid = Q L_n` term is
   not underbidding to a midpoint but simply not competing at profiles whose post-bidding length is below
   `|T(z)| L_n M_i / (1 + mu_i - tau)`, here `2 x 0.80 x 862 / 0.4472 = 3084` post-bidding rounds. This is a
   sharper and simpler witness for the same term than Proposition 6.1 of `PROVER2.md`, and it gives the
   constant `M_i` rather than `(M_i - V_i)/2`.
3. **The revenue at a short profile is mostly Stage-1 revenue and is insensitive to the bids that matter.** At
   `z2` the revenue per visit falls only from `0.7786` to `0.4790` under a bid vector that halves the price,
   because `1724` of its `2000` visits are bidding rounds whose revenue is the bids themselves.

### 17.4 The out-of-sample test of the re-entry criterion at `n = 20000`

The criterion of Section 17.2 reading 3 was written from the `n = 8000` data and predicted that agent 0's
concession, which held at `n = 8000`, should just fail at `n = 20000`, where `N_z = 6732`, `L_n = 1634`,
`s_n = 0.112`, so the prize `(1/2)(6732)(1.10 - 0.688) = 1386.8` first exceeds the cost `1634 x 0.80 = 1307.2`.
The exact computation at `n = 20000`, run afterwards, gives:

| profile | conceder | gain there at `n = 8000` | gain there at `n = 20000` |
| - | - | - | - |
| `z2`, conceded by agent 0 to `0` | agent 0 | [2.6, 25.9] | [319.3, 391.2] |
| `z1`, conceded by honest agent 1 to `0.35` | agent 1 | [518.0, 563.6] | [1697.6, 1773.2] |

The sign flip happens where the criterion says it should: agent 0's concession is worth essentially nothing to
break at `n = 8000` and is worth breaking at `n = 20000`. The magnitude is four to five times the leading-order
estimate of `79.6`, because that estimate is a difference of two nearly equal quantities and the exact deviator
also has the adaptive Stage-1 and monitor-boundary play worth ten to twenty percent of the prize, which is
enough to triple a small difference. Agent 1's gain grows by a factor `3.1` while `N_z` grows by a factor
`2.96`, the linear scaling that Theorem C1(ii) and Theorem C3(iii) predict. The total per-round gains under
the division are `[0.0687, 0.0798]` and `[0.1132, 0.1189]` at `n = 8000` against `[0.0678, 0.0769]` and
`[0.1216, 0.1254]` at `n = 20000`: flat in `n`, hence linear in total, so the division profile is not an
additive equilibrium and the market-division agreement is not self-enforcing at these horizons, which is what
Theorem C3(iii) asserts asymptotically. What the numbers add to the theorem is the horizon at which the
deterrent switches on, and the fact that it switches on later for the member with the deeper concession.

### 17.5 The two scalings, measured inside one instance

`ctx_mixed` with the bid array that is compliant at the unique-top profile `z1` (case (A_z1)) and violating at
the two-top profile `z2`, at two horizons. Between them `N_z` grows by a factor `6732 / 2276 = 2.96` and `L_n`
by a factor `1634 / 862 = 1.90`.

| profile | agent | gain at `n = 8000` | gain at `n = 20000` | measured ratio | scaling it matches |
| - | - | - | - | - | - |
| `z1`, compliant | 0 (local top) | [460.6, 533.0] | [874.0, 994.2] | 1.87 | `L_n` (1.90) |
| `z1`, compliant | 1 (local loser) | [0.0, 0.0] | [0.0, 0.0] | exact zero | exact best response |
| `z2`, violating | 0 | [997.7, 1073.3] | [2674.1, 2798.5] | 2.61 | `N_z` (2.96) |
| `z2`, violating | 1 | [1094.3, 1094.3] | [3395.8, 3404.1] | 3.11 | `N_z` (2.96) |

This is the whole of Theorem C1 in one table, measured rather than argued: at a compliant profile the best
deviation gain tracks the bidding length `L_n` and is therefore `o(n)`; at a violating profile it tracks the
post-bidding length `N_z` and is therefore linear; and the two behaviours coexist in the same instance, the
same run and the same horizon, because the mechanism treats the profiles independently. The exact zero in the
second row is the local loser playing a local exact best response, the contextual form of the scalar Section
8.2 reading 1.
