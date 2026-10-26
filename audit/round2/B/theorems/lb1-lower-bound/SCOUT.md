# LB1 scout: a lower bound over all mechanisms for the n^{2/3} rate

STATUS (13 Oct 2026): CHECKPOINT ONLY. Verdict below is provisional and awaits the coordinator's reply.
Scope: this file only. No canonical file read for writing, none modified, no git command run.

Sources read: sections/sec2_model.tex, sec3_noisy.tex, sec4_contextual.tex, appendix_private.tex
(prop:tightness), app_contextual_private.tex (prop:ctx-finite-tight, prop:ctx-continuum-exact,
rem:ctx-horizons), audit/round2/main/COMPETITOR_WWW2026.md, audit/round2/B/theorems/h1-impossibility/REPORT.md
(L1 imitation, T4 rent transfer, T7 one-sided shading, T8), audit/round2/B/MATH_CANDIDATE_LEDGER.md 6.6,
audit/round2/prompts/COMMON.md (standing rule on probabilistic hypotheses).

## 0. Checkpoint (sent to the coordinator before any development)

PROVISIONAL VERDICT: NO-GO on an n^{2/3} lower bound over all mechanisms, for a stronger reason than
"the argument does not close": the rate appears to be BEATABLE. A sketched mechanism (Section 1)
attains O(sqrt(n log n)) on both the incentive slack and the second-capability revenue loss in the
linear-cost scalar model with K = 2. If that sketch survives an adversarial pass, no n^{2/3} lower
bound exists, and the paper's exponent is a property of fixed-length elicitation, not of the problem.

1. Which quantity the two-point argument constrains. The KL step (two instances differing in the
runner-up's capability by Delta; N_2 pulls of the runner-up; KL of order N_2 Delta^2) bounds only the
REVENUE loss against M_(2): any mechanism with N_2 informative pulls of the runner-up loses about
n/sqrt(N_2) in revenue. It constrains the incentive bound only if one can show N_2 must cost incentive
slack of order N_2. That step fails: the runner-up's revelation pulls are revenue-free (it delivers
exactly the benchmark) and can be made incentive-free by a menu of extra pulls, so N_2 may be
Theta(n) and the revenue loss sqrt(n). The winner's elicitation, which is where MESP's L_n term
really lives (prop:tightness), can be shortened by adaptive certification (stop pulling the winner
once its lower confidence bound clears the other's upper bound), which inverts the underbidding
incentive: revealing high ends elicitation sooner and primary pulls pay more than elicitation pulls.

2. Reduction to existing results. The construction does not reduce to thm:separation (noise, class of
rules, no rate) nor to Cao's information-rent bound (benchmark, no noise). It is a genuinely
statistical argument. It simply does not deliver 2/3, and the obstruction is structural.

3. Probability a defensible n^{2/3} lower bound exists: about 10 percent, because of the candidate
upper bound. The 10 percent is the chance the candidate has a hole I have not found (listed in
Section 2). Recommended next step: an adversarial pass on the candidate mechanism, not a prover on
the lower bound.

## 1. The candidate upper bound that kills the lower bound (sketch, K = 2, linear cost, mu_i = 0)

Agents 1, 2 strategic with linear cost; capabilities M_1, M_2 in [0, 1/2] (the cap keeps the menu
below n; any fixed cap 1 - delta works with constants depending on delta). Honest set nonempty is
satisfied vacuously by letting one agent be honest with mu = 0. Parameters: L := n/4,
s := sqrt(log(2 n^4) / (2 L)), monitor boundary b_n(r) := sqrt(r log(2 n^4) / 2) as in MESP.

Phase E (adaptive elicitation). Pull the two agents alternately, keeping confidence intervals of
half-width s(t) = sqrt(log(2 n^4) / (2 t)) around each agent's running mean over its t pulls. The first
agent whose lower bound exceeds the other's upper bound is certified the winner w and is not pulled
again in this phase; the other agent l continues to be pulled until it has L pulls in total. If no
certification occurs before both have L pulls, w is the higher running mean (coin on ties). Let
beta_l be l's running mean over its L pulls and tau := (beta_l - s)_+.

Phase R (the loser's menu). Pull l for R(beta_l) := beta_l L / (1 - beta_l) further rounds, demanding
tau with the anytime cumulative monitor; on conviction, skip to Phase P.

Phase P (monitored primary). Pull w for the remaining rounds, demanding tau with the anytime monitor;
on conviction, fall back to l at demand tau (or to EXP3 over both, for the honest benchmark).

Proposed profile: deliver capability in Phase E; l delivers tau in Phase R; w delivers tau in Phase P.

Why the accounting lands at sqrt(n). Revenue: Phase E loses nothing (both deliver at least
min(M_1, M_2) = M_(2)); Phase R loses s per round on at most L rounds; Phase P loses s per round;
total about s n = O(sqrt(n log n)). Incentives, loser: revealing mean c gives L(1 - c) + R(c)(1 - c + s)
= L + s R(c), increasing in c, so revealing its capability is optimal with zero slack (the menu is the
Myerson envelope: (1 - c) R(c) = c L exactly compensates elicitation effort). Incentives, winner:
revealing c in (theta + 2 s, M_w] delays certification to about 4 log n / (c - theta)^2 pulls and
every delayed pull is worth (1 - c) instead of the primary (1 - tau) with tau < theta < c, so revealing
M_w is optimal; in the near-tie band c - theta < 2 s the underbidding gain is at most 2 s L =
O(sqrt(n log n)). Becoming the loser is worth at most L + R, which is below the primary tenure's
(1 - tau) n / 2 once L <= n / 4 and M_(2) <= 1/2. Primary shading is bounded by the monitor at
O(sqrt(n log n)), exactly as in MESP. The honest-benchmark part looks unchanged at sqrt(n) with an
EXP3 fallback, but I have not checked it.

Where MESP's n^{2/3} comes from, in this light: a fixed elicitation length L_n paid by the winner
(prop:tightness) balanced against n / sqrt(L_n). Both ingredients are design choices.

## 2. Where the candidate could break (what an adversary should attack first)

(a) The winner's certification argument assumes primary pulls pay more than elicitation pulls; with a
general convex cost this still bounds the gain by Lambda times min(L Delta, 4 log n / Delta) <=
2 Lambda sqrt(L log n), but I have only checked the inequality, not written it against the full
behavioural class B_{i,n}.
(b) The loser's menu is exact only for the linear cost. For a general convex phi it needs an
overcompensating menu R(c) = T(c) (exp(Lambda c / kappa) - 1), which requires the mechanism to know
Lambda and the nondegeneracy constant kappa of eq:nd. In the paper's model phi is private, so the
sqrt(n) claim is clean only in the linear model, which is the model the paper names as the
literature's standard.
(c) K >= 3: menus for losers below the runner-up cost revenue (they deliver below M_(2)); adaptive
elimination should drop them after about log n / gap^2 pulls with compensation O(sqrt(L log n)) each,
but this is unverified.
(d) Timing deviations inside Phase E (an agent shaping the other's certification time). I found none
that gain, because the loser's pull count is fixed at L and the winner's is minimised by revealing its
maximum, but a prover must check this against adaptive targets.
(e) Instances with M_(2) near 1: the menu needs L <= (1 - M_(2)) n / 4, so the sqrt(n) rate holds on
each fixed instance but not uniformly as M_(2) -> 1. The paper's statement is per fixed instance.

## 3. Simulation (coordinator's decision (b), 13 Oct 2026)

Script: scripts/sim_lb1.py. Output: out/grid_main.json, out/grid_main.log. Login node, single core,
minutes; no Slurm job. Logged in COMPUTE_LOG.md.

Instance (picked once): K = 2, linear cost. Agent 1 strategic, mu_1 = 0, M_1 = 0.5. Agent 2 honest,
mu_2 = 0.1, M_2 = 0.3. Second-capability benchmark 0.3, honest benchmark 0.1, gap 0.2.
Horizons 1e4, 1.78e4, 3.16e4, 5.62e4, 1e5; 100 replicates per cell; every deviation of a replicate
shares that replicate's uniform seed array U[agent][local pull], its tie coin and its EXP3 coins, so
gains are coupled differences. Reward sums are integer counters.

MESP: the paper's constants (L_n, s_n, b_n with log(2 K n^4) and log(2 n^4)), uniform tie, EXP3 fallback.
Candidate (ACM, adaptive certification plus loser menu), parameters fixed before any run and not
revisited: L = floor(n/4); ell = log(2 n^4); half-width s(t) = sqrt(ell / (2 t)); alternate pulls and
certify a winner at the first equal-count t with mean_w - s(t) > mean_l + s(t); loser pulled to L in
total; no certification by L means winner = higher mean (coin on ties); tau = (beta_l - s(L))_+;
menu R = floor(beta_l L / (1 - beta_l)) rounds of the loser at demand tau under the anytime monitor
Z_r < r tau - sqrt(r ell / 2); primary = winner at demand tau under the same monitor; conviction in
either monitored phase sends the remaining rounds to EXP3 over both agents (as in MESP).

Declared option set for agent 1 (32 options, fixed before running): constant elicitation underbid
c in {0.30, 0.32, ..., 0.48}; underbid-early-reveal-late (c in {0.3, 0.4} for the first 25/50/75 percent
of the maximal elicitation length, then M_1); reveal-early-underbid-late (M_1 for 25/50 percent, then
0.3); the boundary pacer (target chosen each pull to hold the own running mean at 0.3 + 2 s(t) - delta,
delta in {0, 0.02, 0.05}, using the known instance value 0.3 since agents do not see each other's
rewards); primary shading by delta in {0.01, 0.02, 0.05, 0.10}; the boundary tracker in the primary
(hold Z_r at margin 1 or 3 above r tau - b(r)); two combinations; becoming the loser (c in
{0, 0.2, 0.28}). For agent 2 (6 options): elicitation at c in {0.10, 0.15, 0.20, 0.25}; shading the
Phase-R demand by 0.02 or 0.05. The best gain is the maximum over the option set of the mean coupled
gain; it is a lower bound on exploitability for this set, not an equilibrium statement.

Smoke test at n = 1e4 (20 replicates) already shows the one place the sketch was quantitatively off:
under ACM the winner's constant underbid to 0.32 GAINS 259, because the certification time
T_w = 2 ell / gap^2 (about 1840 here) is paid at (M_1 - tau) per pull while the underbid costs only
(c - tau) per pull over L. The gain is T_w (M_1 - tau) - L (c - tau): the first term is
O(log n / gap), the second grows like n, so the deviation is unprofitable beyond n of about 3e4. The
elicitation gain of ACM is therefore bounded by O(log n / gap), not zero, and not sqrt(n). Full-grid
numbers follow.

## 4. Results of the main grid (100 coupled replicates per cell; out/summary.txt has every number)

Four numbers per arm. "Best all" is the maximum over the 32 declared options of agent 1; "best
elicitation" restricts to options that touch only the elicitation phase (constant underbid, early/late
timing, pacer, become-loser); "best agent 2" is over the 6 options of the honest runner-up.

| mech | n | revenue/round | bench M_(2) | bench honest | best all (per round) | best elicitation | best agent 2 |
| -- | -- | -- | -- | -- | -- | -- | -- |
| MESP | 1e4 | 0.2103 | 0.30 | 0.10 | 381 (0.0381) | 151 | 201 |
| MESP | 1.78e4 | 0.2201 | 0.30 | 0.10 | 540 (0.0304) | 226 | 301 |
| MESP | 3.16e4 | 0.2309 | 0.30 | 0.10 | 543 (0.0172) | 360 | 450 |
| MESP | 5.62e4 | 0.2392 | 0.30 | 0.10 | 558 (0.0099) | 537 | 671 |
| MESP | 1e5 | 0.2482 | 0.30 | 0.10 | 900 (0.0090) | 800 | 1000 |
| ACM | 1e4 | 0.2867 | 0.30 | 0.10 | 282 (0.0282) | 208 | 53 |
| ACM | 1.78e4 | 0.2792 | 0.30 | 0.10 | 334 (0.0188) | 100 | 95 |
| ACM | 3.16e4 | 0.2781 | 0.30 | 0.10 | 365 (0.0115) | 0 | 170 |
| ACM | 5.62e4 | 0.2789 | 0.30 | 0.10 | 680 (0.0121) | 0 | 286 |
| ACM | 1e5 | 0.2822 | 0.30 | 0.10 | 620 (0.0062) | 0 | 214 |

Fitted log-log slopes against n.
- MESP elicitation gain: 0.729 (theory L_n (M_1 - c) with L_n of order n^{2/3} (log n)^{1/3}; the best
  constant underbid is to 0.34 and equals 0.16 L_n to the unit). MESP honest-loser gain: 0.696, and it
  equals 0.2 L_n exactly (the loser's free underbid to its floor). This is the n^{2/3} term and it is
  where the sketch says it is: elicitation, paid by the winner and by the loser.
- ACM elicitation gain: positive only at the two smallest horizons (208, 100), then exactly zero (the
  best elicitation option is the proposed behaviour itself). A slope cannot be fitted to zeros; on the
  two positive points it is -1.27. The positive values are the certification cost T_w (M_1 - tau) with
  T_w = 2 ell / gap^2 (1838 to 2308 pulls here), an O(log n / gap) quantity that the growing cost
  L (c - tau) of staying uncertified overtakes by n of about 2e4.
- ACM honest-loser gain: 0.675, but it is the Phase-R monitor slack (shade the demand on R = 0.107 n
  reward pulls by the largest delta the boundary does not catch), bounded by b(R) = sqrt(R ell / 2),
  that is sqrt(n log n); the coarse delta grid makes it look steeper than it is. The loser's
  elicitation underbids are all strictly negative under ACM (the menu works): -165 to -44 at n = 1e4.
- "Best all" for BOTH mechanisms is the primary-phase monitor slack (boundary tracker or an
  undetected constant shade), the paper's own conjectured sqrt(n log n) term, attained equally by
  both; its slope (0.31 MESP, 0.40 ACM) is unreliable because the shading grid is coarse. It is not
  the discriminating statistic; the elicitation slopes are, as recorded in Section 3 before the grid ran.
- Revenue: ACM is nearer the benchmark at every horizon (shortfall per round 0.013 to 0.022 against
  MESP's 0.090 to 0.052). ACM's total shortfall equals (n - T_w - L) s(L) - 0.2 T_w to within 3
  percent at every n (decomposition in summary.txt), so it is of order n s(L) = sqrt(2 n ell), that
  is sqrt(n log n), minus an O(log n) credit from the winner over-delivering during certification.
  MESP's shortfall slope is 0.76 (theory n s_n + K L_n, order n^{2/3} (log n)^{1/3}).

The timing deviations the coordinator asked to test. Underbid-early-reveal-late under ACM: +183 at
n = 1e4 (the same certification-cost effect), +3 at 1.78e4, negative from 3.16e4 on (-239, -347,
-504 at best). The boundary pacer (hold the own mean at 0.3 + 2 s(t) - delta): +1 at 1e4 and negative
afterwards (-77, -158, -165, -264 at best over delta). Reveal-early-underbid-late: exactly 0 from
3.16e4 on, because the agent is certified during the high stretch and is never pulled again in Phase
E. Pacing the certification boundary costs about (2 s(L) - delta) per pull over L = n/4 pulls, which
is sqrt(n log n), against a one-off saving of O(log n / gap); it does not break the adaptive rule.

## 5. Reading of the result, and what remains open

What the simulation establishes: on this instance the candidate removes the n^{2/3} elicitation term
from both agents' deviation gains and from the revenue shortfall, leaving terms that are sqrt(n log n)
or O(log n / gap), while MESP's elicitation gains grow at the predicted 0.70 to 0.73 slope. The sketch
survives the attack it was most exposed to (timing inside adaptive elicitation). The one quantitative
correction is that the winner's certification cost is a constant of order 2 ell (M_1 - tau)/gap^2,
not negligible at n = 1e4 on a gap of 0.2, and it is what makes small underbids profitable at small n.

What it does not establish: it is a lower bound on exploitability over a declared option set, not an
equilibrium proof; it is one instance, linear cost, K = 2; the honest-benchmark part of ACM under
arbitrary joint behaviour was not exercised; the K >= 3 menu, general convex costs (Section 2(b)),
near-tie instances (gap of order s(L), where the certification cost becomes L s(L), still sqrt-type),
and the uniformity as M_(2) -> 1 are untested. These are the adversary's targets if (a) is commissioned.

Consequence for LB1: NO-GO stands, now with numerical support. Do not pursue an n^{2/3} lower bound
over all mechanisms. The paper's open-problem sentence can be sharpened to name the likely answer:
adaptive certification with a menu for the runner-up appears to make the elicitation term vanish,
leaving the monitor's sqrt(n log n) as the only term we know how to attain, and we do not know whether
that one is necessary.
