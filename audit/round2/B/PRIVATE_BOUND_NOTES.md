# Adjudication of three notes on Theorem thm:private-mesp (Agent B, 17 September 2026)

Sources checked line by line: sections/appendix_private.tex (Lemma lem:private-monitor, Lemma lem:selected-reactive-exp3, equations eq:private-price, eq:private-fallback-core, eq:private-fallback-top, eq:private-fallback-low, and the equilibrium proof), sections/Private_information_setting.tex (parameters and the profile S^*).

## Note 1: removal of the 2 n s_n term from the top-agent deviation bound. VERIFIED (holds).

Setting. Fix a top agent i (V_i <= M_i) and a deviation in B_{i,n}; condition on i's private coins; couple Stage-1 uniforms so that beta'_i <= beta_i^max pathwise. The price tau_i = (max_{j != i} beta_j - s_n)_+ is a function of the other agents' Stage-1 rewards only, hence identical under the deviation and under S^*_i on every coupled path. On the deviation-independent event G_{-i} (probability at least 1 - n^{-4}), eq:private-price gives (V_i - 2 s_n)_+ <= tau_i <= V_i.

Step 1 (primary phase, unchanged). Lemma lem:private-monitor with tau = tau_i: on the good monitor event (failure probability at most n^{-3}), if the primary phase lasts q pulls, U_i^pri <= q (1 + mu_i - tau_i) + 1 + 2 b_n(q). This is already in terms of tau_i.

Step 2 (fallback, restated). Eq:private-fallback-core reads V_i H - R_K(H) <= bar A_i + V_i (H - bar Q_i), i.e. bar A_i >= V_i bar Q_i - R_K(H). Hence
E[U_i^fb | F_fb] = (1 + mu_i) bar Q_i - bar A_i <= (1 + mu_i - V_i) bar Q_i + R_K(H) <= (1 + mu_i - V_i) H + R_K(H),
using 1 + mu_i - V_i >= 0 and bar Q_i <= H. On G_{-i}, tau_i <= V_i gives 1 + mu_i - V_i <= 1 + mu_i - tau_i, so
E[U_i^fb | F_fb] <= (1 + mu_i - tau_i) H + R_K(H)   on G_{-i}.
(G_{-i} is measurable with respect to the bidding history, which is contained in F_fb, so the restriction is legitimate.)

Step 3 (sum). With H = N_n - q, on G_{-i} intersected with the good monitor event,
deviating post-bid utility <= (1 + mu_i - tau_i) N_n + 1 + 2 b_n(n) + R_K(n).
The current manuscript instead bounds this by (1 + mu_i - V_i) N_n + 2 n s_n + 1 + 2 b_n(n) + R_K(n), which is weaker by exactly the 2 n s_n that comes from replacing tau_i by V_i - 2 s_n.

Step 4 (baseline on the same coupled path). Whenever the deviation wins bidding, maximum bidding also wins at the same tau_i. Strategic top agent: baseline primary target min{tau_i, M_i} = tau_i (since tau_i <= V_i <= M_i), so its post-bid utility is at least N_n (1 + mu_i - tau_i) unless a false switch occurs, whose expected cost is at most 2 N_n (2 n^3)^{-1} by the last claim of Lemma lem:private-monitor. Honest top agent: if tau_i > mu_i the baseline target is again tau_i and the same comparison holds; if tau_i <= mu_i, the baseline delivers mu_i, earning exactly 1 per primary pull, while any honest deviation (target at least mu_i) earns at most 1 per selected pull and has at most N_n selected pulls, so the deviation's post-bid utility is at most N_n <= baseline post-bid utility + 2 N_n (2 n^3)^{-1}. Neither honest branch uses s_n.

Step 5 (losing branch and Stage 1, unchanged). If the deviation loses bidding, the nondeviating winner targets at least tau on G_{-i} (tau <= (beta_W - s_n)_+ <= M_W), so fallback occurs with probability at most (2 n^3)^{-1} and the losing deviator's post-bid utility is at most 2 n (2 n^3)^{-1} = n^{-2}; its baseline utility is nonnegative. Stage-1 effort saving is at most L_n in every branch (per-pull utility difference at most M_i <= 1).

Step 6 (bad events). Complements of G_{-i} and of the monitor event cost at most 2 n (n^{-4} + n^{-3}) <= 4 n^{-2}.

Conclusion (top agent, strategic or honest):
sup_{S'_{i,n} in B_{i,n}} [u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)] <= L_n + 1 + 2 b_n(n) + R_K(n) + 2 N_n (2 n^3)^{-1} + 4 n^{-2} = L_n + 2 b_n(n) + R_K(n) + O(1).
The 2 n s_n term is gone. The order n^{2/3} (log n)^{1/3} is unchanged because of L_n; the remaining terms are O(sqrt(n log n)).

Non-top agent (also checked). The non-top branch never used 2 n s_n either: for n large enough that 2 s_n <= delta_i / 2 (note 3), tau_i - M_i >= delta_i / 2 on G_{-i}, the monitor bounds the primary length by q <= 4 (1 + sqrt(2 ell_n))^2 / delta_i^2 with ell_n = log(2 n^4), fallback utility is at most 2 R_K(n) / delta_i, so post-bid deviating utility is at most 2 q + 2 R_K(n) / delta_i and the baseline is nonnegative. The manuscript's displayed non-top bound "L_n + 2 n s_n + 2 b_n(n) + R_K(n) + O(1 + log n / delta_i^2 + R_K(n) / delta_i)" can be replaced by L_n + O(1 + log n / delta_i^2 + R_K(n) / delta_i) for n above the instance threshold, and by the trivial bound n below it (absorbed into the instance constant).

Replacement paragraph for appendix_private.tex (to replace the sentence starting "Suppose a top agent i wins" through the display of the top-agent supremum bound; the losing branch and the non-top branch stay as they are apart from deleting "2 n s_n"):

"Suppose a top agent i wins, so V_i <= M_i, and let q and H = N_n - q be the primary and fallback lengths. On G_{-i} we have tau_i <= V_i, so 1 + mu_i - V_i <= 1 + mu_i - tau_i and \eqref{eq:private-fallback-top} gives E[U_i^{fb} | F_fb] <= (1 + mu_i - tau_i) H + R_K(H). Together with Lemma~\ref{lem:private-monitor} at tau = tau_i, the deviating post-bid utility on the good events is at most (1 + mu_i - tau_i) N_n + 1 + 2 b_n(n) + R_K(n). On every coupled history where the deviation wins, maximum bidding also wins at the same price tau_i, which depends only on the other bids. For a strategic agent the baseline primary target is tau_i and its post-bid utility is at least N_n (1 + mu_i - tau_i) unless a false switch occurs, an event of probability at most (2 n^3)^{-1} costing at most 2 N_n. For an honest agent the same comparison applies when tau_i > mu_i; when tau_i <= mu_i the baseline earns one unit per primary pull while every honest deviation earns at most one unit per selected pull, so again it loses at most 2 N_n (2 n^3)^{-1} in expectation. Hence, integrating over private randomization and charging Stage 1 and the bad events,
sup_{S'_{i,n} in B_{i,n}} [u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n)] <= L_n + 2 b_n(n) + R_K(n) + O(1)."

Downstream: Theorem statement unchanged (rate O_{inst,K}(n^{2/3} (log n)^{1/3})); the proof-idea sentence mentioning "2 n s_n" would be updated; the revenue bound keeps its n s_n term (the price is below M_(2) by up to 2 s_n), so s_n remains part of the mechanism's cost, only not of the deviation gain.

## Note 2: tightness of the L_n term for MESP as specified. PROVED (one-paragraph lower bound below); the Stage-2 b_n tracking claim is NOT verified here and should not be stated as proved.

Proposition (Stage-1 underbidding gain on a unique-top instance). Fix K >= 2, an instance with a unique top agent i (M_i > V_i) and, if i is honest, mu_i < M_i. Let m' := max{ (M_i + V_i)/2, mu_i 1{i honest} } < M_i and let the deviation S'_{i,n} deliver m' on every Stage-1 pull and otherwise follow S^*_i (target min{tau, M_i}, or max{mu_i, min{tau, M_i}} if honest, in the primary phase; capacity in fallback). Then for all n with 4 s_n < M_i - V_i,
u_i(n; S'_{i,n}, S^*_{-i,n}) - u_i(n; S^*_n) >= L_n (M_i - m') - 4 n^{-3}.
In particular the L_n term of the equilibrium bound is attained up to the instance factor M_i - m' > 0, and the order n^{2/3} (log n)^{1/3} of Theorem thm:private-mesp is tight for MESP as specified.

Proof. Couple the two executions by the same reward uniforms indexed by (agent, local pull index), the same priorities, and the same EXP3 coins. Let E be the event that all K bids are within s_n of their targets: under S^* the targets are M_j; under the deviation they are M_j for j != i and m' for i. Hoeffding and a union bound give Pr(E^c) <= 2 K exp(-2 L_n s_n^2) = n^{-4} in each execution. On E in the baseline, beta_i >= M_i - s_n > V_i + s_n >= max_{j != i} beta_j, so i wins; on E in the deviation, beta'_i >= m' - s_n = (M_i + V_i)/2 - s_n > V_i + s_n >= max_{j != i} beta_j when 4 s_n < M_i - V_i, so i wins again. The price tau_i is the same function of the other agents' Stage-1 rewards in both executions, and after Stage 1 the deviation follows S^*_i with the same uniforms and coins, so on E (intersected over both executions, failure probability at most 2 n^{-4}) the post-bid histories, hence post-bid utilities, coincide pathwise. Stage-1 utilities differ by exactly L_n (m'-based) : L_n (1 + mu_i - m') - L_n (1 + mu_i - M_i) = L_n (M_i - m'). Off the good events utilities differ by at most 2 n, contributing at most 2 n times 2 n^{-4} = 4 n^{-3}. Feasibility: m' in [0, M_i], and m' >= mu_i when i is honest, so the deviation lies in B_{i,n} (indeed in the smaller stationary-per-phase class). QED.

Remark on the Stage-2 claim. The experiments lead reports that a dynamic program shows an additional gain of order b_n(N_n) = O(sqrt(n log n)) by tracking the monitoring boundary. This is plausible (the monitor tolerates a cumulative shortfall of b_n(q)) but is lower order than L_n and is not proved here; it must not enter the paper as a theorem.

## Note 3: the non-top branch needs 2 s_n <= delta_i / 2. CONFIRMED as a finite-n scope remark, not an error.

s_n = sqrt(log(2 K n^4) / (2 L_n)). The condition 2 s_n <= delta_i / 2 is L_n >= 8 log(2 K n^4) / delta_i^2. For delta_i = 0.005 and K = 3 this requires L_n >= 8 log(2 K n^4) / 2.5e-5 = 3.2e5 log(6 n^4); with n = 10^10 the right side is about 3.2e5 x 93.9 = 3.0e7 while L_n = n^{2/3} (log(en))^{1/3} = 4.6e6 x 2.85 = 1.3e7, so the condition first holds around n between 10^10 and 10^11, confirming "L_n beyond 10^7". The theorem is asymptotic in n for a fixed instance and remains correct; the branch can also be stated for all n with 2 s_n < delta_i by replacing delta_i / 2 with delta_i - 2 s_n in the primary-length bound q <= 4 (1 + sqrt(2 ell_n))^2 / (delta_i - 2 s_n)^2. Recommended limitations sentence: the non-top guarantee is not observable at feasible horizons when the capacity gap is of order 10^{-2} or smaller.
