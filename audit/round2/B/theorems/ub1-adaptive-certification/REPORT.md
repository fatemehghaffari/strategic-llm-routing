# UB1: can adaptive certification plus a loser menu (ACM) provably beat MESP's n^{2/3}?

STATUS (16 Oct 2026): WORKING FILE. Appended after every read and every derivation step. Nothing below
is final until marked VERDICT. Labels: [PROVED] = derivation written and checked here; [SIM] = simulated
only; [BELIEF] = unverified; [LB1 CLAIM] = untrusted claim taken from the LB1 scout.

Scope: writes only in this directory and scratch/round2/ub1/. No canonical file modified. No git command.

## 0. Reading log

- Read SCOUT.md (LB1) Sections 0 to 5. Key facts taken as [LB1 CLAIM]: ACM phases E (alternating pulls,
  certify at first equal count t with mean_w - s(t) > mean_l + s(t), loser pulled to L = n/4 total),
  R (loser menu R(beta_l) = beta_l L/(1 - beta_l) rounds at demand tau = (beta_l - s(L))_+ under the
  anytime monitor), P (winner at demand tau under the monitor, EXP3 fallback on conviction).
  LB1's own correction: winner's certification cost is T_w (M_w - tau) with T_w about 2 ell/gap^2, so
  an underbid to c saves L (c - tau) less than that; the elicitation slack is O(log n/gap), not zero.
- Read sim_lb1.py. The ACM implementation matches the sketch. Note: the "pacer" option uses the KNOWN
  instance value 0.3 of the other agent; agents do not see each other's rewards in the model, so this is
  a strictly stronger deviator than B_{i,n} allows, fine as an upper bound on what B_{i,n} can do.
- Read sec2_model.tex. B_{i,n}: after selection, before seeing the reward, agent i chooses m_{i,t} in
  [0, M_i] using n, its own history (own selections, own targets, own rewards, mechanism messages and
  counts), private randomness. Agents are blind to the global round and to others' histories. Cost
  phi_i nondecreasing convex Lambda-Lipschitz with phi_i(1) - phi_i(0) <= 1 (N). Honest agents never
  deliver below mu_i. Benchmarks M_(2), mu_H^*.
- Read appendix_private.tex: lem:cost-convert (Jensen in the favourable direction), lem:private-monitor
  (boundary b_n(r) = sqrt(r log(2n^4)/2), any-time failure prob <= n^{-3}, winner's monitored utility
  <= q(1 + phi(mu) - phi(tau)) + Lambda(1 + 2 b_n(q))), lem:selected-reactive-exp3, the coupling
  argument (deviating bid beta'_i <= beta_i^max pathwise, same price tau_i), prop:tightness (constant
  underbid to (M_i + V_i)/2 gains L_n (phi(M_i) - phi(m')) - 4 n^{-3}).
- Read sec3_noisy.tex MESP definition: L_n = min(floor(n/2K), ceil(n^{2/3} log(en)^{1/3})),
  s_n = sqrt(log(2Kn^4)/(2 L_n)), b_n(r) = sqrt(r log(2n^4)/2), tau = (beta_(2) - s_n)_+. Proposed
  profile S*: deliver M_i in bidding and fallback; strategic winner delivers min(tau, M_i) in primary.

## 1. Step A: the ACM contract, written as the paper writes mechanisms (K = 2)

Inputs the mechanism knows: n and K = 2 only. It does NOT know the gap, Lambda, M_(2), mu_i, or which
agent is honest. (The BOUND I derive below has an instance-dependent n_0 through 1/(1 - M_(2)); the
mechanism itself is instance-free.)

Parameters (functions of n only):
- ell_n := log(2 n^4).
- L := floor(n / 4). (Variant for a cap-free per-instance statement: L := floor(n / log n); see 1.4.)
- s(t) := sqrt(ell_n / (2 t)) for t >= 1 (half-width after t pulls); b_n(r) := sqrt(r ell_n / 2) (monitor
  boundary, as in MESP). Identity used throughout: t s(t) = b_n(t).

Phase E (adaptive elicitation). Pull agents 1, 2, 1, 2, ... alternately. After both have t pulls let
hat m_i(t) be agent i's running mean over its own t pulls. The certification time is the stopping time
  T_c := min{ t <= L : exists i with hat m_i(t) - s(t) > hat m_j(t) + s(t), j != i },  T_c := L if none,
measurable w.r.t. the Phase-E filtration (all mechanism observations up to the 2t-th Phase-E pull). If
certification occurs at T_c, the certified agent is w, the other is l, and w is not pulled again in Phase
E. If no certification occurs by L, w := argmax_i hat m_i(L) with a uniform coin on ties. Agent l is
pulled until it has L pulls in total. Put beta_l := hat m_l(L) and tau := (beta_l - s(L))_+. Announce tau
to both agents (the paper's private-mechanism convention: the price is announced; a selected agent learns
its phase from its own selections and messages).
Phase-E length: T_c + L rounds. The winner has T_c pulls, the loser L.

Phase R (loser's menu). R := floor(beta_l L / (1 - beta_l)), truncated to the rounds remaining. Pull l for
R rounds demanding tau with the anytime monitor: after its r-th Phase-R pull with reward sum Z_r, if
Z_r < r tau - b_n(r), stop Phase R (conviction) and go to Phase P.

Phase P (monitored primary). Pull w for all remaining rounds demanding tau with the same anytime
monitor; on conviction, run explicit-exploration EXP3 over both agents for the remaining H rounds, with
fresh randomness (exactly MESP's Stage 3).

Proposed profile S*: every agent delivers M_i on every Phase-E pull and in fallback; in Phase R, a
strategic loser delivers min(tau, M_l), an honest loser max(mu_l, min(tau, M_l)); in Phase P the winner
delivers min(tau, M_w) (honest: max(mu_w, .)). Feasible on every history.

Pull-count identity (the whole analysis rests on it) [PROVED, by counting]: whoever is the winner has
exactly T_c + (n - T_c - L - R) = n - L - R pulls (fewer only if a monitored phase convicts), and R and
tau are functions of the LOSER's L Phase-E rewards alone. The winner's number of pulls does not depend
on its certification time; only the SPLIT between elicitation pulls (target constrained by certification)
and primary pulls (target tau) does.

### 1.1 Standing good event G (probability >= 1 - 3 n^{-3}) [PROVED]
For each agent i and each t <= L, by conditional Hoeffding-Azuma on the martingale Z_i(t) - A_i(t)
(A_i(t) = sum of its first t targets, each F_{t-1}-measurable; this is lem:private-monitor's first
display with b_n(t) = t s(t)): |hat m_i(t) - A_i(t)/t| <= s(t) fails with probability <= 2 exp(-2 t
s(t)^2) = 2 exp(-ell_n) = n^{-4}. Union over 2 agents and t <= L <= n: <= 2 n^{-3}. Add the Phase-R and
Phase-P monitor events (each <= n^{-3} by lem:private-monitor). On G:
 (G1) an agent following S* (target M_i at every Phase-E pull) has |hat m_i(t) - M_i| <= s(t) for all t <= L;
 (G2) a deviator's Phase-E running mean satisfies hat m'_i(t) <= A'_i(t)/t + s(t) <= M_i + s(t) for all t.

### 1.2 Non-emptiness of Phase P [PROVED under M_(2) <= 1/2, n >= n_0 with s(L) <= 1/8]
On G, beta_l <= M_(2) + s(L) <= 1/2 + s(L), so R <= L (1/2 + s)/(1/2 - s) <= L (1 + 8 s(L)) and
n - T_c - L - R >= n - 2L - L(1 + 8 s(L)) >= n/4 - 2 n s(L) > 0 when s(L) < 1/8.

### 1.3 On G the winner can always deliver tau: tau <= M_w [PROVED]
L-comparison case: hat m_w(L) >= beta_l, so tau <= hat m_w(L) - s(L) <= M_w by (G1)/(G2).
Certification case: hat m_w(t) - s(t) > hat m_l(t) + s(t) at t = T_c; on G this forces M_w >= M_l (the
lower-capability agent cannot be certified on G), hence tau <= beta_l <= M_l + s(L) - s(L) ... more
precisely tau = (beta_l - s(L))_+ <= M_l <= M_w. So the certified agent is a top agent on G.

### 1.4 Why L = n/4 and the cap M_(2) <= 1/2 go together
The "become the loser" deviation collects L + R(c) = L/(1 - c) pulls with c <= M_(2) + s(L); the
winner's tenure is n - L - R >= n - L/(1 - M_(2)) - O(n s(L)). The loser branch is unprofitable up to
O(n s(L)) iff L/(1 - M_(2)) <= n/2, i.e. L <= n (1 - M_(2))/2. With L = n/4 this is M_(2) <= 1/2. Taking
L = floor(n / log n) instead gives s(L) = sqrt(ell_n log n /(2n)), n s(L) = O(sqrt(n) log n), and the
condition becomes 1 - M_(2) >= 2/log n, true for every fixed instance with M_(2) < 1 once
n >= exp(2/(1 - M_(2))). This is the gap-free, cap-free PER-INSTANCE version (constant depends on the
instance only through n_0). [PROVED at the level of the inequality; the full theorem is Section 5.]

## 2. Step B: the winner's certification argument against the full class B_{i,n}

Setting for this section: K = 2, agent 1 is the deviator (strategic, any phi_1 in the paper's class),
agent 2 follows S*. The deviator's capability is M_1; the other's is M_2. Coupling, exactly as in
appendix_private.tex: agent-local uniform seeds U_{i,k} (k-th pull of agent i), common tie coin, common
EXP3 coins, shared by the baseline and the deviation. Agent 2's Phase-E rewards are then IDENTICAL in
the two executions (it delivers M_2 on its first L pulls in both; its k-th local pull uses U_{2,k}), so
beta_2, R(beta_2) and tau_2 := (beta_2 - s(L))_+ are deviation-independent random variables.

The partition: on each coupled path, the deviation either WINS (is certified, or wins the L-comparison)
or LOSES. Both events are measurable w.r.t. the Phase-E history of the deviating execution.

### 2.1 Case W: the deviation wins. [PROVED]
Then l = 2, tau = tau_2, R = R(beta_2), and the deviator's total pull count is n - L - R minus any
rounds lost to conviction/fallback (Section 1 identity). Its utility is bounded phase by phase.

(E) Elicitation pulls. Let t = T_c' be the deviator's number of Phase-E pulls, A'(t) its target sum.
 - Certified at t < L (or at t = L by the certification rule): hat m'_1(t) - s(t) > hat m_2(t) + s(t), so
   Z'_1(t) > t hat m_2(t) + 2 b_n(t) >= t (M_2 - s(t)) + 2 b_n(t) = t M_2 + b_n(t) on G. By (G2),
   A'(t) >= Z'_1(t) - b_n(t) > t M_2. Jensen (lem:cost-convert(a) with theta = M_2, Delta = 0) gives
   sum of Phase-E costs >= t phi_1(M_2) >= t phi_1(tau), since tau <= M_2 on G (beta_2 <= M_2 + s(L)).
   So U^E <= t (1 + phi_1(mu_1) - phi_1(tau)).
 - Wins the L-comparison: hat m'_1(L) >= hat m_2(L) >= M_2 - s(L), so A'(L) >= L M_2 - 2 b_n(L), and
   lem:cost-convert(a) gives U^E <= L (1 + phi_1(mu_1) - phi_1(tau)) + 2 Lambda b_n(L).
 Note what this does NOT need: no assumption that the deviator's targets are constant, stationary, or
 non-randomised. The certification condition is a statement about the deviator's own cumulative reward
 at a stopping time, and Azuma converts it to a statement about its cumulative target. The deviator's
 timing choices are irrelevant: whatever it does, being certified or winning at L pins its average
 delivered target over the elicitation window at >= M_2 (minus 2 b_n(L)/L in the second case).

(P) Primary pulls, q of them: lem:private-monitor verbatim, U^P <= q (1 + phi_1(mu_1) - phi_1(tau))
 + Lambda (1 + 2 b_n(q)).
(F) Fallback pulls, H of them: eq:private-fallback-top verbatim with V_1 = M_2 >= tau,
 E[U^F | F_fb] <= (1 + phi_1(mu_1) - phi_1(tau)) H + Lambda R_2(H).
Phase R: the deviator is not pulled. If agent 2 is convicted in Phase R (it delivers tau <= M_2, so this
has probability <= (2 n^3)^{-1} by lem:private-monitor's last claim), the winner gets extra pulls; this
is a bad event charged at 2n times its probability.

Summing with t + q + H = n - L - R on the good events:
 U'_1 <= (n - L - R)(1 + phi_1(mu_1) - phi_1(tau)) + Lambda (1 + 2 b_n(n) + R_2(n) + 2 b_n(L)).   (W-up)

Baseline on the same path (agent 1 at S*, which also wins, see 2.3): it is certified at T_c^* or wins
at L, pays phi_1(M_1) on its T_c^* elicitation pulls and phi_1(tau) on the n - L - R - T_c^* primary
pulls (false switch probability <= (2 n^3)^{-1}, charged at 2n times it):
 U*_1 >= (n - L - R)(1 + phi_1(mu_1) - phi_1(tau)) - T_c^* (phi_1(M_1) - phi_1(tau)).              (W-low)

Hence on Case-W paths, up to bad events,
 gain <= T_c^* (phi_1(M_1) - phi_1(tau)) + Lambda (1 + 2 b_n(n) + R_2(n) + 2 b_n(L)).            (W-gain)
This is LB1's "certification cost" correction, now as an upper bound over all of B_{i,n}, and the
deviator cannot beat the baseline by more than the baseline's own certification cost. The point LB1
argued informally ("revealing high ends elicitation sooner, and primary pulls pay more") is not needed
and not used; what is used is the pull-count identity plus the fact that certification pins the
deviator's average Phase-E target at >= M_2 >= tau.

### 2.2 The certification cost is O(sqrt(L ell_n)) UNIFORMLY in the gap. [PROVED]
Let Delta := M_1 - M_2 >= 0 (Case W with the deviator the higher agent; the misordered case
Delta < 0 can only happen via the L-comparison and is covered by the second branch below with T_c^* = L).
On (G1) for both agents at S*, certification of agent 1 occurs at the first t with
 (M_1 - s(t)) - s(t) > (M_2 + s(t)) + s(t), i.e. Delta > 4 s(t) = sqrt(8 ell_n / t), i.e. t > 8 ell_n/Delta^2,
so T_c^* <= min{ L, floor(8 ell_n / Delta^2) + 1 } =: T_bar(Delta). Also on G, M_1 - tau <= Delta + 2 s(L)
(because tau >= beta_2 - s(L) >= M_2 - 2 s(L)). Therefore, with phi_1 Lambda-Lipschitz,
 T_c^* (phi_1(M_1) - phi_1(tau)) <= Lambda T_bar(Delta) (Delta + 2 s(L)).
 - If Delta >= 2 s(L): T_bar <= 8 ell_n/Delta^2 + 1 and Delta + 2 s(L) <= 2 Delta, so the product is
   <= 16 ell_n/Delta + 2 Delta <= 16 ell_n / (2 s(L)) + 2 = 8 ell_n / s(L) + 2 = 8 sqrt(2 ell_n L) + 2.
 - If Delta < 2 s(L): T_bar <= L and Delta + 2 s(L) < 4 s(L), so the product is < 4 L s(L) = 4 b_n(L)
   = 2 sqrt(2 ell_n L).
In both cases: T_c^* (phi_1(M_1) - phi_1(tau)) <= Lambda (8 sqrt(2 ell_n L) + 2) <= 8 Lambda sqrt(2 n ell_n)
 + 2 Lambda for L <= n.                                                                            (CERT)
So the winner's elicitation slack is O(Lambda sqrt(n log n)) with NO gap in the bound. LB1's
"O(log n / gap^2)" form is the gap-regime expression; its maximum over the gap is attained at
Delta of order s(L) and equals O(sqrt(L ell_n)). This also settles the brief's item D (near ties): the
near-tie regime is where the bound is tightest, and it is still sqrt-type.

## 3. Open items / to-do
- [ ] Step A formal contract
- [ ] Step B verdict and checkpoint to coordinator
- [ ] Steps C, D, E only after coordinator's reply

### 2.3 Case L: the deviation loses. HERE ACM AS SKETCHED BREAKS. [PROVED: explicit deviation with linear gain]
Two routes to losing: (i) agent 2 is certified at some T_c (needs hat m'_1(T_c) < hat m_2(T_c) - 2 s(T_c));
(ii) no certification and hat m'_1(L) <= hat m_2(L). On route (ii), beta'_1 := hat m'_1(L) <= M_2 + s(L).
On route (i) the deviator is still pulled to L pulls AFTER certification, and nothing constrains its
post-certification targets: it can deliver 0 for the first T_c pulls (agent 2 is then certified within
T_c <= 8 ell_n/M_2^2 + 1 pulls, a constant), then deliver M_1 for the remaining L - T_c pulls, so that
beta'_1 = M_1 (1 - T_c/L) + O(s(L)) is ANY value up to M_1. The menu then pays it
 R(beta'_1) = beta'_1 L/(1 - beta'_1) rounds at demand tau' = beta'_1 - s(L), truncated at n - L - T_c.
Its utility as a loser (upper and lower bound agree to O(sqrt(n ell_n))) is
 u_L(c) = L (1 + phi_1(mu_1) - phi_1(c)) + min{cL/(1-c), n - L}(1 + phi_1(mu_1) - phi_1(c - s(L))) + O(sqrt(n ell_n))
       = g_1(c) + O(n s(L)),  g_1(c) := L (1 + phi_1(mu_1) - phi_1(c))/(1 - c) while cL/(1-c) <= n - L.
Its baseline utility as the winner is, by (W-low) and (CERT),
 u_W = (n - L - R(beta_2))(1 + phi_1(mu_1) - phi_1(tau_2)) - O(sqrt(n ell_n)),  tau_2 in [M_2 - 2s(L), M_2].
Counterexample 1 (linear cost, mu_1 > 0, the paper's model allows mu_i in [0, 1]): L = n/4, M_2 = 1/2,
M_1 >= 3/4. Pump to c = 3/4, where cL/(1-c) = 3L = n - L fills the horizon: u_L = L(1 + mu_1 - 3/4)
+ 3L(1 + mu_1 - 3/4) = n (1/4 + mu_1) + O(sqrt(n ell_n)). Baseline: u_W = (n - L/(1 - 1/2))(1/2 + mu_1)
= n (1/4 + mu_1/2) + O(sqrt(n ell_n)). Gain = n mu_1 / 2 - O(sqrt(n ell_n)): LINEAR for every mu_1 > 0.
For M_2 < 1/2 the gain is n [M_2 - 1/2 + mu_1/(4(1 - M_2))], positive e.g. at M_2 = 0.45, mu_1 = 0.2
(gain 0.041 n). LB1 took mu_i = 0, where this gain is n (M_2 - 1/2) <= 0; its option set contained
only constant "become-loser" underbids, which cannot pump.
Counterexample 2 (flat cost, mu_1 = 0): phi_1 identically 0 is in the paper's class (nondecreasing,
convex, Lipschitz, range 0 <= 1). Then every pull is worth 1 to agent 1 regardless of effort.
u_L(3/4) = L + 3L = n; u_W = n - L - R(beta_2) <= n - L. Gain >= L = n/4. LINEAR, for any M_2 <= 1/2.
Mechanism of the failure: the menu is paid on the loser's FINAL L-pull mean, which the top agent can
inflate after it has lost on purpose. The menu is an information rent for the runner-up, and the top
agent is entitled to collect it by posing as the runner-up with a reported type up to M_1.
Consequence: LB1's ACM, exactly as sketched and simulated, does NOT have an o(n) incentive slack over
B_{i,n} on the paper's model (nor on the linear model with mu_1 > 0). Its sqrt(n) claim is false as stated.

### 2.4 The repair: cap the loser's reported mean at its pre-certification upper confidence bound.
Define, in the certification case,
 beta_l := min{ hat m_l(L),  hat m_l(T_c) + s(T_c) },
and beta_l := hat m_l(L) in the L-comparison case; tau := (beta_l - s(L))_+ and R := floor(beta_l L/(1 - beta_l))
as before. Call the result ACM' (adaptive certification, capped menu).
[PROVED] On G, in every case beta_l <= M_w + s(L) where w is the realised winner, for arbitrary behaviour
of BOTH agents: certification case beta_l <= hat m_l(T_c) + s(T_c) < hat m_w(T_c) - s(T_c) <= M_w by (G2)
applied to the winner's own targets; L-comparison case beta_l = hat m_l(L) <= hat m_w(L) <= M_w + s(L).
So a deviator that loses collects at most the menu of a true runner-up of capability M_other + s(L).
[PROVED] At S* the cap is inactive up to s(L): hat m_l(T_c) + s(T_c) >= M_l on G1, so beta_l >= M_l - s(L),
tau >= M_l - 2 s(L), and the revenue argument is unchanged.
[PROVED] Case L for ACM' (deviator 1 loses, agent 2 at S*): beta'_1 <= M_2 + s(L) on both routes.
Phase E: A'_1(L) >= L hat m'_1(L) - b_n(L) >= L beta'_1 - b_n(L), so by lem:cost-convert(a)
U^E <= L (1 + phi_1(mu_1) - phi_1(beta'_1)) + Lambda b_n(L). Phase R (lem:private-monitor at demand
tau' = beta'_1 - s(L), at most R(beta'_1) pulls): U^R <= R(beta'_1)(1 + phi_1(mu_1) - phi_1(beta'_1)) +
Lambda s(L) R(beta'_1) + Lambda(1 + 2 b_n(n)). Agent 2 as winner can deliver tau' (tau' <= M_2), so
fallback has probability <= (2n^3)^{-1}. Hence
 U'_1 <= g_1(beta'_1) + Lambda s(L) R(beta'_1) + Lambda(1 + 2 b_n(n) + b_n(L)) + O(n^{-2}).          (L-up)
 Key inequality [PROVED]: g_1(c) = L (1 + phi_1(mu_1) - phi_1(c))/(1 - c) is NONDECREASING on [0,1) for
 every phi in the paper's class. Proof: g_1'(c) = L [ (1 + phi_1(mu_1) - phi_1(c)) - (1 - c) phi_1'(c) ]/(1-c)^2
 (a.e.; phi convex hence absolutely continuous with nondecreasing derivative), and
 (1 - c) phi_1'(c) <= int_c^1 phi_1' = phi_1(1) - phi_1(c) <= 1 + phi_1(0) - phi_1(c) <= 1 + phi_1(mu_1) - phi_1(c)
 by convexity, (N), and monotonicity in turn. Also 0 <= g_1'(c) <= 2L/(1-c)^2.
 So U'_1 <= g_1(M_2 + s(L)) + O(Lambda sqrt(n ell_n)) <= g_1(M_2) + 2L s(L)/(1/2 - s(L))^2 + O(Lambda sqrt(n ell_n))
 when M_2 <= 1/2, and g_1(M_2) = L (1 + phi_1(mu_1) - phi_1(M_2))/(1 - M_2).
 Baseline on the same path: either the baseline wins, u*_1 >= (n - L - R(beta_2))(1 + phi_1(mu_1) - phi_1(M_2))
 - CERT - O(n^{-2}) >= (n - L/(1 - M_2) - 8 L s(L))(1 + phi_1(mu_1) - phi_1(M_2)) - CERT, using tau_2 <= M_2
 and R(beta_2) <= R(M_2 + s(L)) <= L/(1 - M_2) + 8 L s(L) for M_2 <= 1/2; or the baseline also loses, which
 on G forces M_1 <= M_2 + 2 s(L) (near tie or misordering), and then u*_1 >= g_1(M_1 - s(L)) - O(sqrt(n ell_n))
 >= g_1(M_2 - s(L)) - ... hmm: in the misordered case M_1 < M_2 the deviation's cap is M_1 + s(L) via
 route (ii) (hat m'_1(L) <= M_1 + s(L) by (G2)) and via route (i) beta'_1 < M_2 but also <= M_1 + s(L)
 by (G2); so U'_1 <= g_1(min(M_1, M_2) + s(L)) + O(sqrt) and u*_1 >= g_1(M_1 - s(L)) - O(sqrt); the gain is
 <= g_1(M_1 + s) - g_1(M_1 - s) + O(sqrt) <= 16 L s(L) + O(sqrt(n ell_n)) [M_1 <= M_2 + 2s <= 1/2 + 2s].
 In the baseline-wins branch the gain is at most
  (1 + phi_1(mu_1) - phi_1(M_2)) [ 2L/(1 - M_2) - n ] + 16 L s(L) + CERT + O(Lambda sqrt(n ell_n)),
 and the bracket is <= 0 exactly when L <= n (1 - M_2)/2, i.e. M_2 <= 1/2 for L = n/4. Then
  gain on Case-L paths <= O(Lambda sqrt(n ell_n)).                                                  (L-gain)
 (The per-pull factor 1 + phi_1(mu_1) - phi_1(M_2) is in [0, 2] by (N), which is what lets the bracket's
 sign decide.)

### 2.5 Case W for ACM' [PROVED, small change to 2.1]
With the cap, tau and R in Case W depend on T_c (through hat m_2(T_c) + s(T_c)), hence on the deviator.
But on G1, hat m_2(T_c) + s(T_c) in [M_2, M_2 + 2 s(T_c)] and hat m_2(L) in [M_2 - s(L), M_2 + s(L)], so
beta_2 in [M_2 - s(L), M_2 + s(L)] whatever T_c is; thus tau in [M_2 - 2 s(L), M_2] and
R in [R(M_2 - s(L)), R(M_2 + s(L))], an interval of length <= 2 L s(L)/(1/2 - s(L))^2 <= 16 L s(L) for
M_2 <= 1/2. Replace "same tau, same R on the coupled path" by: deviation utility bound at (tau', R') and
baseline bound at (tau*, R*) differ by at most n Lambda |tau' - tau*| + 2 |R' - R*| <= 2 Lambda n s(L) + 32 L s(L)
= O(Lambda sqrt(n ell_n)). (W-gain) holds with this added. The elicitation step 2.1(E) used only tau <= M_2,
still true.

### 2.6 The coupling/mixing step [PROVED, same as MESP]
The deviator's private coins are conditioned on first. On each coupled path the deviation either wins
or loses (Phase-E measurable). Pathwise Z'_1(t) <= Z^max_1(t) (seed coupling), so on every path where the
deviation wins the baseline also wins (certification and the L-comparison are monotone in the deviator's
reward sums; the tie coin is common), and the baseline is certified no later. The baseline then has the
(W-low) lower bound with its own (tau*, R*) within the 2.5 window. On paths where the deviation loses,
2.4 covers both sub-cases (baseline wins / baseline loses). All bad events (G^c, false convictions,
fallback) are charged at 2n times their probability, total O(n^{-2}). Integrating over the coins gives
 sup_{B_{1,n}} gain <= C Lambda sqrt(n ell_n) + O(1), with an explicit C collected in Section 5 later.
Honest deviators: as in MESP, when tau <= mu_1 the baseline earns one unit per pull and no honest
deviation earns more per selected pull; when tau > mu_1 the strategic comparison applies. [BELIEF until
written out: the loser branch for an honest deviator needs g_1 evaluated with the honest floor; the same
monotonicity argument applies because honesty only restricts c >= mu_1.]

### 2.7 Caveat that is NOT about incentives: the honest-benchmark robustness guarantee is lost.
[PROVED by example] thm:private-mesp's third guarantee holds for EVERY behavioural profile. Under ACM or
ACM' with L = n/4, take h honest and top (certified within O(ell_n/Delta^2) pulls) and a strategic
runner-up that delivers 0 on its L - T_c remaining Phase-E pulls (irrational, but allowed in the
quantifier). Revenue shortfall against mu_h n is at least (L - T_c) mu_h = Theta(n). Any variant that
pulls the runner-up Theta(n) times without an honest-benchmark monitor has this Theta(L) loss; a monitor
cannot help because the mechanism does not know mu_h and the loser's own pre-certification mean may be
far below it. With L = n/log n the loss is O(n/log n): o(n) but not sqrt. So the sqrt rate on (1) and
(2) comes at the price of the robustness rate: L mu_H^* against n/sqrt(L); balancing gives n^{2/3}, which
is exactly MESP. [BELIEF, not proved] this trade-off is a genuine lower bound over mechanisms, which
would mean MESP's exponent is optimal for the TRIPLE of guarantees and ACM' is better only for the pair.

### 2.8 STEP-B VERDICT (checkpoint)
1. The winner's certification argument SURVIVES the full class B_{i,n}: (W-gain) + (CERT) give an
   elicitation slack <= Lambda (8 sqrt(2 n ell_n) + 2) with no gap dependence; the near-tie regime is the
   binding one and is still sqrt-type. LB1's O(log n/gap^2) correction is the large-gap expression of the
   same quantity. Timing, pacing, randomisation and history dependence are irrelevant to the bound
   because certification pins the deviator's cumulative Phase-E target at >= T_c M_2.
2. ACM as LB1 sketched it is BROKEN by a loser-branch deviation (lose on purpose early, pump the final
   mean, collect a menu sized for a type up to M_1): linear gain n mu_1/2 for linear cost with mu_1 > 0
   at the cap, and gain >= n/4 for a flat cost. Not visible in LB1's simulation (mu_1 = 0, constant
   underbids only).
3. Repair ACM': cap the loser's reported mean at hat m_l(T_c) + s(T_c). Then the loser branch closes
   under L <= n (1 - M_(2))/2 (M_(2) <= 1/2 for L = n/4; or L = n/log n and n >= exp(2/(1 - M_(2))) for
   a per-instance cap-free statement), for the paper's full convex class, via g(c) nondecreasing.
4. Cost of the repair's rate: the honest-benchmark robustness guarantee drops from O(n^{2/3}) to
   Theta(L). This is structural (2.7), not a proof gap.
Simulation check of item 2 requested next (small, login node), then wait for coordinator.

### 2.9 Simulation check of the pump deviation [SIM; script pump_check.py, log pump_check.log, this dir]
LB1's ACM exactly (L = n/4, ell = log(2n^4), menu beta L/(1 - beta), demand beta - s(L)); K = 2, linear
cost, agent 2 honest at S*; 50 coupled replicates; false convictions ignored (probability <= n^{-3}).
Deviation: deliver 0 until agent 2 is certified (happens on 100 percent of replicates within ~300 to 600
pulls), then deliver the constant that brings the final L-pull mean to c*. Gain per round (u_dev - u_base)/n:
 mu1=0.2, M1=0.9, M2=0.45: c*=0.75 -> +0.0606 (n=1e4), +0.0508 (3.16e4), +0.0464 (1e5); prediction
   n [M2 - 1/2 + mu1/(4(1-M2))] = 0.0409 n. Linear and positive; c*=0.6 and 0.8 are worse, as g predicts.
 mu1=0.1, M1=0.9, M2=0.5: c*=0.75 -> +0.0800, +0.0649, +0.0584 (prediction n mu1/2 = 0.05 n). Linear.
 mu1=0.0, M1=0.9, M2=0.45: all c* negative (prediction n (M2 - 1/2) = -0.05 n): LB1's instance class
   (mu = 0) cannot see this deviation.
The simulated gains exceed the leading-order prediction by a term decreasing in n, consistent with the
O(n s(L)) corrections in 2.3. This is a lower bound on exploitability over the two-parameter deviation
family {(pump target c*)} only; the proof of linear gain is 2.3.

## 3. Priority (1): is the triple trade-off of 2.7 a lower bound over mechanisms? (working notes, 16 Oct)

Notation. For a mechanism A knowing n, K only, with proposed profile S*_A(instance):
 Inc_A(I) := max_i sup_{B_{i,n}} gain;  Rev_A(I) := M_(2) n - P(n; S*);  Rob_A(I) := sup_S [mu_H^* n - P(n; S)].
Minimax versions take sup over K = 2 instances in the paper's class.

### 3.1 The 2.7 trade-off as written is NOT a lower bound over all mechanisms. [PROVED by example]
Rob alone is O(sqrt(n K log K)): explicit-exploration EXP3 run for all n rounds has, by the paper's own
lem:selected-reactive-exp3 with the honest agent of mean mu_H^* as comparator, P(n; S) >= mu_H^* n - R_K(n)
for EVERY behavioural profile. So "any Theta(n) runner-up elicitation costs Theta(L) robustness" is a
statement about mechanisms whose price is read off L unmonitored runner-up pulls (MESP with L_n, ACM, ACM'),
not about mechanisms in general. The quantity that trades against Rev is not "pulls of the runner-up";
it is "unmonitored or self-referentially monitored pulls of a non-honest agent".

### 3.2 Per fixed instance (gap Delta > 0 fixed, n -> infinity) the triple is probably O(sqrt(n log n)) + O(log n/Delta^2).
[BELIEF, sketch only, NOT verified] Mechanism CFP (certify, fresh price): Phase E as in ACM with cap
L_max = n/4; after certification at T_c, Phase F pulls the loser again, monitored at demand
hat m_l(T_c) - 2 s(T_c), until its fresh mean hat p(f) satisfies hat p(f) + 2 s(f) <= hat m_w(T_c) - s(T_c),
then announces p := hat p(f) + s(f) (on G this lies in [M_l, M_w]: an OVERSHOOT that is still feasible for
the winner, so the primary earns >= M_l per round and Rev <= O(sqrt(n ell_n)) with no undershoot term);
if no certification by L_max, price := fresh mean - 3 s(L_max) (feasible for a possibly misordered winner
since misordering on G forces M_l - M_w <= 2 s(L_max)); Phase P monitored; EXP3 fallback.
 Heuristic accounting: Inc = O(ell_n/Delta^2) [the loser's 2 T_c + f uncompensated pulls, and the winner's
 certification cost] + O(Lambda sqrt(n ell_n)); Rev = O(sqrt(n ell_n)); Rob = O(sqrt(n ell_n)) because under
 any profile a strategic loser delivering mu_h - eta is pulled only O(ell_n/eta^2) times after certification
 (loss O(ell_n/eta) <= O(sqrt(n ell_n))), and a strategic near-tie winner delivers >= mu_h - 4 s(L_max).
 If this holds up, MESP's exponent is a GAP-UNIFORMITY (minimax) phenomenon, not a per-instance one; the
 paper's theorem is stated uniformly ("no capacity gap enters it"), so the relevant question is minimax.
 The CFP sketch needs its own proof (the Phase-F stopping time, the overshoot's feasibility, the monitored
 Phase-F incentives); none written. Do not cite it as a result.

### 3.3 Minimax: every design I can write has max(Inc, Rev, Rob) of order n^{2/3} up to logs, attained near
Delta of order n^{-1/3}. [PROVED for the named designs by direct computation; CONJECTURE for all mechanisms]
 - MESP: all three n^{2/3}(log n)^{1/3} (the paper).
 - ACM' (Section 2): Inc, Rev = O(sqrt(n log n)) for M_(2) <= 1/2; Rob = Theta(n) (2.7). Pair, not triple.
 - CFP with cap L_max: certified regime Delta >~ s(L_max): loser's uncompensated pulls ~ ell/Delta^2 <= L_max,
   so Inc ~ L_max at Delta ~ s(L_max); near-tie regime Delta <~ s(L_max): undershoot 3 s(L_max) gives
   Rev, Rob ~ n/sqrt(L_max). Balance: L_max = n^{2/3}. CFP with L_max = n/4 has Inc = Theta(n) at
   Delta ~ n^{-1/2} (deliver 0 in a Phase F of length ~n).
 - Menus (ACM') decouple Inc from the runner-up's pull count but pay Rob, because a menu gives a loser
   Theta(L) pulls at a demand tied to the loser's OWN revealed level, which under an arbitrary profile may be
   far below mu_h. Monitoring the compensation at the loser's own level does not help for the same reason.
 Mechanism of the conjectured bound: in near ties the mechanism cannot tell who is top; its price must be
 undershot by about 1/sqrt(N_2) (Rev or Rob ~ n/sqrt(N_2)), where N_2 is the runner-up's pull count; those
 N_2 pulls are either uncompensated (Inc ~ N_2 times a cost saving) or compensated by tenure that an
 arbitrary profile converts into Rob ~ N_2. Hence max(Inc, Rev, Rob) >~ min_N max(N, n/sqrt(N)) = n^{2/3}.

### 3.4 Why I cannot prove 3.3 in this pass [honest obstruction]
 (a) The KL two-point step bounds the PRICE error given N_2, but Rev is not monotone in price error:
     overshooting into [M_(2), M_w] costs nothing (3.2). A lower bound on Rev needs the near-tie regime,
     where feasibility forces undershoot; making "forces" rigorous needs a statement about ALL ways a
     mechanism could react to a convicted winner (fallbacks that re-elicit, rotate, etc.).
 (b) "Compensation costs Rob" has to hold against adaptive mechanisms that shorten the compensation when
     the loser looks bad. The adversarial profile must look like a near-tie loser during elicitation and
     exploit the compensation afterwards; against ACM' this gives only Rob ~ N_2 n^{-1/3} (small), and the
     Theta(n) loss in 2.7 used an UNMONITORED stretch that a better design removes. So the Rob side of the
     conjecture is not even clearly true for all menu designs; it may be that a monitored menu achieves the
     triple in o(n^{2/3}). I could not settle this either way.
 (c) The Inc side needs a lower bound on the runner-up's deviation gain over its uncompensated pulls for
     ALL proposed profiles S*, including profiles where the runner-up delivers below M_(2) during elicitation
     (then Rev at S* pays instead). That is a genuine minimax-over-S* argument I do not have.
VERDICT ON (1): not a theorem in this pass. The 2.7 form is refuted (3.1). The per-instance version of the
conjecture is probably FALSE (3.2, unverified). The minimax version is a conjecture with consistent evidence
from every design tried (3.3) and three identified proof obstacles (3.4). A monitored-menu design (3.4(b))
is the thing an adversary of the conjecture should try first; if it reaches o(n^{2/3}) on the triple, the
conjecture is dead and the paper's exponent is beatable on all three.

## 4. Verify or refute 3.2 (CFP, certify-then-fresh-price). RESULT: REFUTED. (16 Oct, later)

Plan written before the analysis: (i) fix the price rule exactly (three candidates: overshoot, undershoot
with race-type Phase F, undershoot with fixed-length Phase F); (ii) for each, test the winner's stalling
deviation and the loser's Phase-F shading deviation at a fixed instance; (iii) answer the coordinator's
three questions. Setting: K = 2, agents at S* except the deviator, winner w (capability M_w), loser l
(M_l), Delta := M_w - M_l > 0 fixed, L_max := floor(n/8) so that E + F fit. All "on G" statements use the
good event of 1.1 extended to Phase F (union bound, probability >= 1 - 4 n^{-3}).

### 4.1 Observation that removes the need for a "fresh" phase [PROVED]
On G, certification at T_c gives LCB_w(T_c) := hat m_w(T_c) - s(T_c) > UCB_l(T_c) := hat m_l(T_c) + s(T_c),
and (G1) gives UCB_l(T_c) >= M_l, (G2) gives LCB_w(T_c) <= A_w(T_c)/T_c <= M_w. So any price in
[UCB_l(T_c), LCB_w(T_c)] is in [M_l, M_w] whatever the stopping bias. Fresh pulls are not needed for
feasibility; they only change accuracy. This is what the 3.2 sketch implicitly used.

### 4.2 Overshoot price (p in [M_l, M_w], e.g. p := UCB_l(T_c), or the Phase-F variant p := fresh mean + s(f)
stopped when fresh mean + s(f) <= LCB_w(T_c)). KILLED by the winner's stalling deviation. [PROVED]
 At S*: p* - M_l >= gamma := LCB_w(T_c) - M_l, and gamma >= s(T_c) - |hat m_l(T_c) - M_l| which is
 >= 0.19 Delta with probability at least 1 - e^{-1}-type constants (s(T_c) in [Delta/4, Delta/sqrt 2] on G
 and the loser's fluctuation at T_c has standard deviation about s(T_c) sqrt(2/ell_n)). So E[p*] >= M_l + c Delta
 with an absolute c > 0.1 for ell_n >= 30. In every overshoot variant the price is at most LCB_w(T_c), the
 winner's OWN lower confidence bound at certification.
 Deviation (in B_{w,n}: a deterministic schedule in the agent's own pull count using instance constants, as
 prop:tightness does): deliver M_l on the first T_stall := floor(n/log n) Phase-E pulls, then M_w. The
 intervals overlap during the stall (both agents near M_l), so nobody is certified; after the stall the
 running mean of w rises and certification occurs at T_c' = T_stall (1 + O(s(T_stall)/Delta)), at which
 point LCB_w(T_c') exceeds UCB_l(T_c') by at most one increment, so p' <= M_l + 2 s(T_c') + O(1/T_c')
 = M_l + O(sqrt(log^2 n / n)). The deviator's pull count n - T_c' - f' loses at most T_stall + f' = O(n/log n)
 pulls (f' is the Phase-F length, O(T_c') by the stopping rule) against the baseline, each worth at most 2.
 Gain >= n (phi_w(p*) - phi_w(p')) - O(n/log n) >= n lambda (c Delta - o(1)) - O(n/log n) = Theta(n)
 whenever phi_w has slope lambda > 0 on [M_l, M_l + c Delta] (linear cost: lambda = 1).
 Reason in one line: an overshoot price is a function of the winner's revealed capability, i.e. a
 first-price component, and the winner shades it by looking like a near-tie agent for a sublinear stall.

### 4.3 Undershoot price with race-type Phase F (pull l until fresh mean + s(f) <= LCB_w(T_c); p := fresh mean - s(f)).
Incentives are fine, revenue is linear-bad. [PROVED]
 Loser in F: its F tenure f(c) ~ 2 ell_n/(gamma + M_l - c)^2 is increasing in its delivered mean c, and
 U(c) = f(c)(1 + phi_l(mu_l) - phi_l(c)) is nondecreasing in c for every phi in the paper's class, by
 phi'(c)(gamma + M_l - c) <= phi'(c)(1 - c) <= phi(1) - phi(c) <= 1 + phi(mu) - phi(c) (same inequality as
 2.4; uses gamma + M_l <= M_w <= 1). So l delivers M_l in F. Winner: p is at most M_l, and stalling only
 lengthens F and raises p toward M_l, so w reveals early. But f* ~ 2 ell_n/gamma^2 with gamma = Theta(Delta),
 hence s(f*) = Theta(Delta) and Rev = 2 s(f*) n + ... = Theta(Delta n). Linear in n for fixed Delta.
 Reason: a responsive (race-type) tenure disciplines the loser only until the race is decided, which is at
 accuracy Theta(Delta); the undershoot then costs Theta(Delta) per primary round.

### 4.4 Undershoot price with fixed-length Phase F (f pulls of l monitored at d_F := hat m_l(T_c) - 2 s(T_c);
p := fresh mean - s(f), or any p <= M_l). KILLED by the loser's shading. [PROVED]
 On G, d_F <= M_l - s(T_c) and s(T_c) >= Delta/4 (T_c <= 8 ell_n/Delta^2 + 1). The loser delivering exactly
 d_F on every Phase-F pull is never convicted except with probability <= (2n^3)^{-1} (lem:private-monitor,
 last claim), receives the same f pulls and nothing afterwards, and saves f (phi_l(M_l) - phi_l(d_F))
 >= f lambda Delta/4. Rev = Theta(n s(f)) forces f = Theta(n) for a sqrt rate, and then Inc >= lambda Delta n/4.
 Trading off: Inc ~ lambda Delta f, Rev ~ n sqrt(ell_n/f), so max(Inc, Rev) >~ (lambda Delta ell_n)^{1/3} n^{2/3}
 at f ~ (n^2 ell_n/(lambda Delta)^2)^{1/3}. Doubling epochs do not help: the slack a loser opens in one epoch
 lowers the next epoch's demand, so the room stays Theta(Delta) (geometric sum dominated by the first term).
 Reason: once tenure stops responding to delivery, a non-compensated agent shades to its demand, and the
 demand can only be set at the accuracy available when it is fixed, which is Theta(Delta) after a race.

### 4.5 Answers to the coordinator's three questions
Q1 (does CFP get the triple at sqrt + instance term?): NO. Every price rule I can write fails on a fixed
instance at the linear scale: overshoot prices are stalled by the winner (4.2, Inc = Theta(n)); undershoot
prices with race-type tenure lose Theta(Delta n) revenue (4.3); undershoot prices with fixed-length fresh
pulls are shaded by the loser (4.4, Inc = Theta(Delta n) when Rev is sqrt). The failing step in the 3.2
sketch was the implicit assumption that the price's accuracy could be pushed below Theta(Delta) without
either compensating the loser or letting the winner influence the price. 3.2 is withdrawn.
Q2 (form of the gap dependence): the gap does NOT enter as an additive log n/Delta^2 term. Within adaptive,
uncompensated designs the best per-instance rate I can derive is max(Inc, Rev) of order
(lambda Delta log n)^{1/3} n^{2/3}: the SAME exponent as MESP, with the gap in the constant only (and MESP's
own realised exploitability on a fixed instance is Theta(Delta L_n) by prop:tightness, also gap-proportional).
So no design here produces a guarantee incomparable to the uniform theorems; nothing forces a retraction,
and there is no per-instance sqrt remark to add. The only way found to leave exponent 2/3 is compensation
(ACM', Section 2), which pays Rob = Theta(n).
Q3 (Delta near n^{-1/3}): moot for CFP since it is refuted outright. For the surviving adaptive family
(race, then f(T_c) monitored loser pulls, undershoot price) the per-instance rate (Delta log n)^{1/3} n^{2/3}
is largest at LARGE Delta and reaches the sqrt scale only for Delta <~ n^{-1/2} (the no-certification
regime, where the race itself bounds the loser's shading by s(L_max)). The binding regime for that family
is the large gap, not n^{-1/3}; I retract the n^{-1/3} sentence of 3.3 for this family. (For MESP, Inc is
~Delta L_n and Rev ~ n s_n is gap-free, so its binding regime for the pair is also Delta of order 1.)

### 4.6 One-paragraph summary for the open-problem text (what I would stand behind)
[PROVED here, K = 2] Adaptive certification removes the winner's elicitation term uniformly in the gap
(2.2), and a menu for the runner-up removes the runner-up's term for the whole convex class (2.4), so the
pair (incentive slack, M_(2)-revenue) can be brought to O(sqrt(n log n)) when M_(2) <= 1/2; but the menu
hands a possibly non-honest agent Theta(n) rounds at a demand tied to its own revealed level, so the
honest-benchmark robustness guarantee becomes Theta(n). Without compensation, every adaptive design we
tried keeps exponent 2/3 on each fixed instance (4.3, 4.4): responsive tenure disciplines the runner-up
only to accuracy of order the gap, and the price must then be either undershot by that much or set from
uncompensated pulls that the runner-up shades. Whether exponent 2/3 is necessary for the triple is open;
it is not necessary for any pair (EXP3 alone gives sqrt robustness; ACM' gives the sqrt pair).

### 4.7 Simulation check of the stalling deviation (4.2) [SIM; stall_check.py, stall_check.log, this dir]
Overshoot price p := min(UCB_l(T_c), LCB_w(T_c)); K = 2, linear cost, mu = 0, M_1 = 0.9, M_2 = 0.5,
L_max = n/8, 50 coupled replicates; only the certified-winner branch modelled, no monitor failures.
Baseline price p* = 0.696 to 0.702 (M_l + 0.49 Delta, larger than the 0.19 Delta lower bound of 4.2).
Stall of T_stall = 0.01 n pulls at M_2 then M_1: p' = 0.665 (n = 1e4), 0.639 (3.16e4), 0.603 (1e5),
0.572 (3.16e5); gain per round 0.021, 0.050, 0.087, 0.123, increasing toward the linear limit
(p* - M_l) = 0.2 as the stall's share of the horizon shrinks. T_stall = 0.03 n: 0.034, 0.073, 0.108, 0.138.
T_stall = 0.1 n fits under the L_max cap only at n = 3.16e5 (gain 0.119 per round). Linear gain confirmed.

### 4.8 Status of claims in this report after Section 4
- Section 2 (ACM' pair at K = 2, cap M_(2) <= 1/2; ACM as sketched broken; Rob = Theta(n)): stands, first pass only.
- Section 3.1 (Rob alone is sqrt via EXP3): stands. 3.2 (CFP): WITHDRAWN by Section 4. 3.3 and 3.4: the
  conjecture stands as a conjecture; the sentence locating the binding regime at n^{-1/3} is retracted for the
  uncompensated adaptive family (4.5 Q3), where the binding regime is the large gap.
- Nothing in this report requires a retraction in the paper. The paper's uniform theorems are unaffected.
