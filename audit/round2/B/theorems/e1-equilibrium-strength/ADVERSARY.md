# Adversarial pass on E1 (equilibrium strength of MESP, scalar and contextual)

Adversary notes, 18 September 2026. Output file only; no canonical file was read-modified, nothing outside this
file and the scratchpad was written. Read in full before any claim below: `audit/round2/prompts/COMMON.md`,
this directory's `REPORT.md` (Part I and Part II), `TASK.md`, `bidprofile.py`, `sections/setting.tex`,
`sections/Private_information_setting.tex`, `sections/appendix_private.tex` (Lemma `lem:private-monitor`,
Lemma `lem:selected-reactive-exp3`, the equilibrium and robustness proofs),
`scratch/experiments/round2/common/{design.py,instances.py,instances.json}`.

My job was to break the report. Summary of what happened, in the coordinator's order of priority:

| # | target | verdict |
| - | - | - |
| 0 | the exact machinery (`bidprofile.py`) | no bug found; four headline numbers reproduced by an independent simulator I wrote from the LaTeX |
| 1 | "a loser's whole stake in its own bid is its Stage-1 effort" | HOLDS inside the family the report uses; FALSE as the unconditional sentence the report and its draft manuscript text actually write. Explicit instance with a linear loser stake below |
| 2 | the strong form of the positive half (two top agents) | not broken. I could not build the counterexample and I now believe it is true; I give the argument and the single lemma it still needs |
| 3 | "PL-MESP has no punishment technology" (Lemma C3.0) | Lemma C3.0 itself survives every channel I tried. One real logical gap in the proof of Theorem C3(iii) that uses it, with a one-line repair |
| 4 | "a deeper concession is more enforceable" | holds, and it can be derived rather than measured; the report names only one of its two causes, and the second is the load-bearing one |

Severity: the only finding I would call P2 is A1 (Section 1.2 below): a sentence proposed for the manuscript
that is false as written; the rest is P3 precision plus one P3 gap in a proof of Part II. Nothing I found makes the report's
central dichotomy wrong.

## 0. The machinery, checked and cross-checked

### 0.1 Line-by-line read of `bidprofile.py`

I read the whole file against `sections/Private_information_setting.tex` lines 8 to 16 and 37 and against the
appendix, looking for the class of bug that produces confident wrong numbers. What I checked and what I found:

- `stage2_dp`: the recursion index. `V` after the loop pass `rr` is the value with `N - rr` pulls remaining;
  `alive_next` uses `bound[rr+1]`, the monitor test after pull `rr+1`, and the fallback entry uses
  `Fm[:, N-rr-1]`, the remaining horizon `N-(rr+1)`. Both are right. The reachability mask `Vn[:, :rr+1]`
  (at most `rr` successes after `rr` pulls) is right. The two-action maximum over `{lo_i, M_i}` is legitimate
  because the continuation `W` does not depend on the current target, so the one-step objective is affine in
  `m`; I verified the affinity by algebra rather than by rerunning `validate_dp.py`, as the report says.
- `stage2_constant`: `Eq` adds `p.sum()` before the pull, so it counts the pull the agent is alive to take;
  `Psw` accumulates the mass killed at each test and zeroes it. Correct.
- `tie_poly` / `others_law` / `winner_law`: the convolution `new[t] = poly[t] a + poly[t-1] b` is the right
  recursion for (max `<= c`, exactly `t` tied at `c`), and `winner_law` gives agent `j` the tie with
  probability `1/(t+1)` against `t` remaining maximizers. The assertion that `winner_law` sums to the max law
  is in the code and passes. Ties are therefore handled exactly, not asymptotically.
- Terminal payoff `terminal(...)`: the winning mass at own count `z` is `P(max other < z) + P(tie won)` and the
  losing mass is the complement with the tie share removed. Correct, and `Pwin` agrees with it.
- Brackets: `V_F0` uses fallback value `0` (a valid lower bound on the sup, since the true fallback value is
  nonnegative and the strategy that attains `V_F0` is feasible), `V_FUB` uses `min{2H, (1+mu-V_i)H + R_K(H)}`
  for a top deviator and `min{2H, 2R_K(H)/delta_i}` otherwise, which are `eq:private-fallback-top` and
  `eq:private-fallback-low` verbatim and are valid here because the non-deviators still deliver capacity in the
  fallback under `S^c`. So `exploit_LB = V_F0 - base_UB` and `exploit_UB = V_FUB - base_LB` do bracket the
  supremum. Correct.
- The deviator's information set in the DP is (own Stage-1 count) then (announced `tau`, own `r`, own `Z`).
  That is exactly what `sections/setting.tex` line 11 gives a blind agent plus the price announcement, so the
  DP is not accidentally giving the deviator other agents' histories. Correct, and it is the reason the DP is a
  true supremum over `B_{i,n}` rather than over a subclass.

One inexactness, which I judge harmless and record only for completeness. `loser_ub[c]` is computed at the
price `taus[c]` built from the MAXIMUM other count `c`, but when agent `i` loses, the announced price is built
from the SECOND order statistic overall, which is at most that. The false-switch probability is not monotone in
`tau` (the Bernoulli variance `tau(1-tau)` is not), so `loser_ub` is not provably an upper bound at the exact
realized price. It cannot matter numerically: every quantity involved is at most `2 N` times a probability of
order `n^{-3}` (`= 2 x 10^-8` at `n = 10^4`), against quoted gains of order `10^2` to `10^3`. If anyone wants
the bracket to be airtight rather than merely correct to eight digits, replace `psw_each` by the maximum of the
switch probability over prices `tau' <= taus[c]`, which costs one extra pass.

### 0.2 Independent verification of four headline numbers

I wrote `<scratchpad>/round2/e1adv/indep_mesp.py` from `sections/Private_information_setting.tex` alone (the
Stage-1 loop, the uniform priority, `tau = (beta_(2) - s_n)_+`, the strict monitor test, the EXP3 restart with
`gamma = min{1/2, sqrt(K log K / H)}`, `eta = gamma/K` from `appendix_private.tex`). It shares no code with
`dp.py`, `bidprofile.py`, or `common/mechanism.py`; it imports only `numpy` and `math`. Monte Carlo, 400 to
4000 episodes.

| instance, `n`, bid vector | quantity | report / `bidprofile.py` | my independent run |
| - | - | - | - |
| `K2_unique_top`, 10000, `S^star` | revenue per round | 0.5652 | 0.56535 +- 0.00030 |
| `K2_unique_top`, 10000, (0.70, 0.35) | revenue per round | 0.2752 | 0.27539 +- 0.00031 |
| `unique_top`, 10000, `S^star` | revenue per round | 0.5533 | 0.55339 +- 0.00028 |
| `unique_top`, 10000, (0.90, 0.00, 0.40) | revenue per round | 0.3134 | 0.31322 +- 0.00027 |
| `unique_top`, 10000, coalition move | agent 0 gain, agent 1 gain, agent 2 gain | +1744.7, +654.5, 0.0 | +1747.1, +654.6, 0.0 |
| `K2_unique_top`, 2000, (0.70, 0.35) | agent utilities | 1439.05, 326.00 | 1438.4 +- 0.6, 326.00 |

Every entry agrees within one to two Monte Carlo standard errors. I also reran `bidprofile.py` itself at
`n = 2000` on `K2_unique_top` with bids `(0.70, 0.35)` and reproduced the report's row to the digit:
`[226.66, 233.15]`, `[34.76, 39.96]`, revenue per round `0.25822`. So the exact numbers in Section 8 of the
report are not an artifact of that script.

## 1. Attack on "a loser's entire stake in its own bid is its Stage-1 effort"

The claim (`REPORT.md` Section 0, Section 3 item 1, and the draft manuscript paragraph of Section 7). I
attacked it along the five channels the brief named, plus one it did not.

### 1.1 The five named channels, all closed inside `Sigma`, and why

A loser is paid after Stage 1 only if a switch occurs, so the fallback, a later switch and the monitor firing
on the winner are one channel, not three. The loser influences that channel in exactly one way: its own bid can
be the second order statistic, so it moves `tau = (beta_(2) - s_n)_+`, and `tau` is the monitor's target rate.
The question is therefore sharp: can a loser raise `tau` above what the winner will deliver?

Under `S^c` the winner's primary target is `min{tau, M_W}`, or `max{mu_W, min{tau, M_W}}` if honest, so it
TRACKS the price. A switch then needs `min{tau, M_W} < tau`, that is `tau > M_W`. Two facts close it.

1. Bid domination plus the concentration event. On `G := {beta_j <= M_j + s_n for all j != W}`, which has
   probability at least `1 - n^{-4}` (this is the manuscript's own event; for a deviating loser use the
   coupling `beta'_k <= beta_k^max` first), `tau <= max_{j != W} M_j - s_n + s_n = V_W`.
2. `V_W <= M_W` in both cases of Theorem E1: in case (A) `V_W < c_W <= M_W` by the defining inequality, and in
   case (B) the winner is a top agent on `G`, so `V_W = M_top = M_W`.

Hence `tau <= M_W`, every primary target is at least `tau`, and the last clause of `lem:private-monitor` caps
the false-switch probability at `(2n^3)^{-1}`. The loser's post-bid utility is at most
`2 N_n (2n^3)^{-1} + 2 n Pr(G^c) <= 2 n^{-2}`. The report's arithmetic is right and I found no slack in it.

Two things worth recording that the report does not say.

- The inequality in case (B) is TIGHT and the `-s_n` shading in the price is what buys it: `beta_(2)` exceeds
  `M_top` with probability about `1/4` when two agents bid `M_top`, and it is only the subtraction of `s_n`
  that puts the announced price back below the winner's capacity. With the raw price `tau = beta_(2)` (the
  ablation `price(mode="raw")` in `common/design.py`) the winner is asked for more than it can deliver on a
  constant-probability event, which is exactly a loser-created switch. I checked how large that channel is: the
  shortfall is `|beta_(2) - M_top| = O(L_n^{-1/2})`, so the monitor's crossing time
  `log(2 n^4)/(2 eps^2) = Theta(L_n log n)` is `o(n)` but is about `1.2 x 10^5` rounds at `n = 10^4` against
  `N_n = 7986`, and in 400 independent raw-price episodes on `K2_tied_top` at `n = 10^4` no switch occurred at
  all. So the shading is load-bearing asymptotically and invisible at computable horizons. This is a remark
  about the mechanism's design, not a correction to the report.
- Ties are not a channel. In case (A) the defining inequality is strict and a loser with `M_k = V_W < c_W`
  cannot reach `beta_W`; the case `M_k = c^max`, where a tie does give `1/2`, is precisely one of the cases the
  necessity proof uses to EXCLUDE a profile, not one it has to survive. The exact computation handles ties by
  the exact multiplicity law (`tie_poly`, `winner_law`), which I checked, so the numerical confirmation is not
  assuming the tie away.

The fifth channel, "the price it faces if it is later selected", does not exist: `alg:mesp` lines 28 to 33 put
the monitor inside the primary loop and the fallback runs to the end of the horizon with no return to a priced
tenure, so a loser that is ever selected again is selected in EXP3, where no price and no monitor apply and its
per-pull utility is `1 + mu_k - m` with `m` of its own choosing. That channel removes a stake rather than
creating one.

### 1.2 Where the claim IS false: the winner's reaction to the price (finding A1, P2)

The sentence is true given that the other agents play `S^c`. It is false as a statement about the mechanism,
and the report writes it as a statement about the mechanism in two places: Section 3 item 1 ("the only
consequence of its bid for itself is the Stage-1 effort") and, worse, in the text drafted FOR THE MANUSCRIPT in
Section 7 ("a losing agent's bid changes its own utility by at most `L_n`, inside the additive slack"). The
price is announced to every agent (`sections/setting.tex` line 11), so the winner's continuation may condition
on it, and then a loser's bid decides which continuation it faces.

Explicit instance, `K2_unique_top` (`mu = (0.10, 0.35)`, `M = (0.90, 0.65)`, agent 1 honest), `n = 10000`,
`L_n = 1007`, `N_n = 7986`, `s_n = 0.1378`. Profile `S^T`: agent 0 bids `0.90`; as winner it delivers
`min{tau, 0.90}` if `tau < 0.5` and delivers `0` if `tau >= 0.5`; in the fallback agent 0 delivers `0.40` and
agent 1 delivers `0.65`. Agent 1's own bid then decides its own payoff, measured on my independent simulator,
400 episodes:

| agent 1's bid `c_1` | `tau` | winner complies | agent 1's utility | revenue per round |
| - | - | - | - | - |
| 0.35 (its honest floor) | 0.2122 | yes | 1007.0 | 0.2951 |
| 0.50 | 0.3622 | yes | 856.0 | 0.4301 |
| 0.65 (its capacity) | 0.5122 | no, the monitor fires in `O(log n)` rounds | 5908.4 +- 3.1 | 0.6585 |

Agent 1 moves its own utility by `+4901`, that is `0.49 n`, by moving its own bid, against the claimed cap of
`L_n (M_k - c_k) = 1007 x 0.30 = 302`. The mechanism is the arithmetic: a fallback pull is worth
`1 + 0.35 - 0.65 = 0.70` to it and it takes essentially all of them because it out-delivers `0.40`.

Honest statement of what this does and does not do. It does NOT contradict Theorem E1, which is scoped to
`Sigma`, and it does not produce a bad equilibrium: at `tau = 0.5122` agent 0 would earn
`N_n (1 + 0.10 - 0.5122) = 4694` by complying against `617` by tanking, so `S^T` fails agent 0's own incentive
constraint and is not an equilibrium. What it does is show that the reason a loser has no stake is a property
of the PROFILE, not of the mechanism, and that the sentence has to carry its hypothesis into the paper. Minimal
repair, one clause: "under `S^c`, a losing agent's bid changes its own utility by at most `L_n`". Severity P2
only because the sentence as drafted is meant to go into the manuscript, where a referee can construct the
above in a minute; as a statement inside the scope of Theorem E1 it is correct.

## 2. Attack on the strong form of the positive half (two top agents)

Target: "with `K_top >= 2`, EVERY additive behavioral equilibrium has revenue `M_(2) n - o(n)`", which the
report proves only inside `Sigma` and names as the step it trusts least (Section 9.3). I was asked to build a
profile outside `Sigma`, with two top agents, that is an equilibrium and earns less than `M_(2) n`. I could not,
I now believe the statement is true, and the reduction below says exactly what is missing.

### 2.1 The structural fact that kills every trigger construction I tried

`sections/setting.tex` line 11: agents are BLIND. An agent observes its own selections, its own targets and
rewards, and the announced price, and NEITHER the global round NOR any other agent's history. Two consequences
that the report never uses and that I think are the right frame for the whole necessity question.

- Stage 1 is effectively simultaneous even though the mechanism pulls agents in index order: no agent can
  condition its own bid on another agent's bid, because the only cross-agent message, `tau`, is announced after
  all `K L_n` bidding rounds (`alg:mesp` line 27).
- After Stage 1 the ONLY agent with an action is the primary winner, until a switch, and a switch is under the
  winner's own control. A losing agent is not merely unpaid, it is unable to act.

So there is no way for any agent to condition anything on a deviation in the bidding before the allocation is
locked, and no way for a loser to retaliate afterwards. Every punishment-supported low-bid profile I wrote down
died on one of those two sentences. This is worth adding to the report: it is the reason the necessity half is
much more robust outside `Sigma` than "restricted to constant bids" suggests.

### 2.2 Two clean statements I verified, outside `Sigma`

SECURITY LEVEL. Under ANY behaviour of the other agents, a top agent `i` that bids `M_i` throughout Stage 1,
complies with `min{tau, M_i}` if it wins, and delivers `M_i` in any fallback, earns at least
`(1/K) N_n (1 + mu_i - M_top) - L_n - o(n) = (kappa_i/K) N_n - o(n)`. Proof: on the concentration event every
other bid is at most `M_top + s_n`, so `i`'s capacity bid is a maximizer and the uniform priority gives it the
tenure with probability at least `1/K_top - o(1)`; the price it then faces is at most `M_top`; and while it
complies no other agent is ever selected, so nobody can react. Hence every top agent's payoff at EVERY additive
equilibrium is at least `(kappa/K) n - o(n)`. This is a max-min bound, it needs no profile family, and it is the
lever under everything below.

NO-SWITCH CASE, ANY POST-BID BEHAVIOUR. Suppose the fallback is reached with probability `o(1)` or carries
`o(n)` rounds, and let the bids be deterministic with top level `b_1`. Then every top agent other than the single
highest bidder has payoff `o(n)` and the security level is violated, UNLESS all top agents bid within `2 s_n` of
`M_top`, in which case the price is `M_top - O(s_n) = M_(2) - O(s_n)` and revenue is `M_(2) n - o(n)`. The
computation needs no accounting: a top agent `j` that loses can bid `M_top` and either win outright at price
`b_1` for `N_n (1 + mu_j - b_1) >= kappa_j N_n > 0`, or tie for at least half of it, while `b_1 <= M_top < 1`
under (ND). So the positive half survives the removal of BOTH restrictions of `Sigma` (constant bids and
`S^star` post-bid play) as long as the horizon does not end up in the fallback.

### 2.3 The four constructions I tried, and the arithmetic that killed each

Instance used throughout: `K = 2` or `3`, two top agents, `M_top = 0.8`, `mu = 0.1`, so `kappa = 0.3`,
`M_(2) = M_top`.

1. BOTH TOP AGENTS UNDERBID AND TIE at `theta < M_top`, any post-bid behaviour. Each earns
   `(1/2) N_n (1 + mu - theta)`; either one bidding `M_top` wins outright at the unchanged price `theta` and
   earns `N_n (1 + mu - theta)`, a gain of `(1/2) N_n (1 + mu - theta) = Omega(n)`. No punishment exists (2.1).
   Dead. This is the report's Section 8.3 row, and its exact computation agrees: gain `3242.7` against slack
   `2229` at `n = 10^4`.
2. ONE TOP AGENT MONOPOLIZES AT A LOW PRICE (the case-(A) shape transplanted to a two-top instance). The other
   top agent gets `0` and can tie at `M_top` for `(1/2) kappa N_n > 0`. Dead, and this is exactly why case (A)
   needs a UNIQUE top: the monopolist's bid must exceed every other CAPACITY, not merely every other bid.
3. DIVERT THE HORIZON INTO A CHEAP FALLBACK: the winner deliberately fails its own monitor early (delivering
   `0` against `tau` crosses `r tau - b_n(r)` after `log(2 n^4)/(2 tau^2) = O(log n)` pulls), and the agents
   then share a low-delivery fallback. This is the construction the report itself says it cannot rule out. It
   fails twice over, and both failures are quantitative.
   - The winner will not do it when the price is LOW, which is the only case in which the primary phase was
     cheap for the platform. Complying pays it `1 + mu_W - tau` per round; the fallback pays it at most its
     share of `1 + mu_W - F`, where `F` is the fallback delivery level. Since a share is at most one and
     `F >= tau` at any fallback equilibrium (next item), tanking gains at most `O(s_n H + R_K(H)) = o(n)`, and
     when `tau` is low it loses `Omega(n)`. So a low price and a tanked tenure are incompatible.
   - The fallback pays the agents no more per round than the priced tenure does. At a fallback equilibrium the
     delivery level is `M_(2)`, so a fallback round is worth `1 + mu_i - M_(2) = kappa_i` to whoever takes it,
     which is exactly the LEAST a primary round at price `tau <= M_(2)` can be worth to the winner. Diverting
     rounds to the fallback therefore never enlarges the agents' pie and never shrinks the platform's revenue
     rate below `M_(2)`.
4. GIVE THE LOSING TOP AGENT ITS SHARE IN THE FALLBACK, so that it tolerates a low price in the primary.
   Profile: the winner runs a cheap tenure of `q = Omega(n)` rounds at a low `tau`, then tanks, and the two top
   agents split the remaining `H = N_n - q` fallback rounds. The losing top agent `j` then holds
   `p_j kappa_j H <= kappa_j H / 2 + o(n)`; bidding `M_top` instead wins the whole tenure with probability at
   least `1/2` and pays it at least `(1/2) kappa_j N_n`. The gain is at least
   `(kappa_j/2)(N_n - H) = (kappa_j/2) q = Omega(n)`. The fallback share cannot pay for the primary rounds the
   tanking destroyed, because a fallback round is worth `kappa_j` and a primary round is worth at least
   `kappa_j`, and `j` gets only a fraction of the former and all of the latter. Dead.

### 2.4 What the strong form actually reduces to, and the one lemma it still needs

Everything above turns on one input, which is NOT proved anywhere in the manuscript or the report outside the
constant-target family:

> FALLBACK LEMMA (open). Condition on a fallback start with `H = Omega(n)` rounds remaining. In any profile from
> which no agent has a deviation confined to the fallback gaining `Omega(H)`, the expected fallback revenue is
> at least `(M_(2) - o(1)) H`.

`REPORT.md` Proposition E3.1 proves it when every agent's fallback target is a constant. Two things I can add.

- The class it has to be proved for is much smaller than "all behavioral strategies", and the report does not
  notice this. In the fallback an agent observes only its own selections, its own targets, and its own rewards,
  which are Bernoulli draws of its own targets and therefore carry no information about anyone else; it has no
  clock. So a fallback strategy is, without loss, a randomized sequence `g_i(k)` indexed by the agent's OWN
  selection count. No agent can detect another's deviation, so no fallback cartel can be enforced, which is the
  same structural point as 2.1 one phase later.
- In that class the Bertrand argument extends beyond constants, but not with the tools the paper has.
  Undercutting UPWARD to a constant `v` makes the deviator a comparator of conditional mean `v`, so
  `lem:selected-reactive-exp3` gives total fallback reward at least `v H - R_K(H)`, and if the others' targets
  have running averages at most `A < v` their total delivery is at most `A(H - Q_i)`, whence
  `Q_i >= H - R_K(H)/(v - A)`: the deviator takes essentially every pull at a cost of `A + o(1)` each. Taking
  `v = A + H^{-1/4}` this is a gain of `(1 + mu_i - A)H - O(H^{3/4})` against a share of the same pie, so any
  level below the second capacity is undercut from above and only `M_(2)` survives. I checked the two evasions
  one would try: front-loading (deliver `M_top` on the first `J` own-selections, then nothing) gives revenue
  `O(J)` but is beaten by front-loading longer, because EXP3 allocates on CUMULATIVE reward and the extra
  `O(J)` of delivery buys an `Omega(H)` share; and randomizing over levels has no equilibrium, by the same
  computation the report does in Section 9.3 one phase earlier. What I cannot do with
  `lem:selected-reactive-exp3` alone is handle a comparator whose per-pull mean is not uniformly bounded below,
  which is exactly the report's own diagnosis.

CONCLUSION OF ATTACK 2. I did not break the strong form and I do not believe it is breakable. What I would put
in the report in place of "I would not put this in the paper" is the reduction: with `K_top >= 2`, the strong
form is TRUE given the Fallback Lemma, by 2.1, 2.2 and 2.3, and the Fallback Lemma is a statement about EXP3
against blind own-count-indexed sequences, not about MESP. That is a much smaller open question than the one
the report currently reports, and it is one sentence away from being the paper's honest statement.

## 3. Attack on "PL-MESP has no punishment technology" (Lemma C3.0 and Theorem C3(iii))

I attacked Lemma C3.0 along every channel the brief named: forcing a fallback, manipulating a price, timing a
switch, exploiting the announcement rule, and acting at another profile. The lemma survives all five. One of
its proof steps is asserted rather than argued and I give the argument. One step in the proof of Theorem
C3(iii), which is the result the lemma is used for, does not follow from what precedes it; the repair is one
line and the conclusion is unaffected.

### 3.1 Channels tried against Lemma C3.0, all closed

Fix `i != j` and a profile `z`, and let `j` try to make `i` worse off at `z` than `S^*_j` does.

1. RAISE THE PRICE `i` PAYS. `tau_{i,z} = (max_{l != i} beta_{l,z} - s_n)_+` is nondecreasing in `beta_{j,z}`
   and `beta_{j,z}` is stochastically largest at the capacity target, which is `S^*_j`. Nothing above capacity
   exists. Closed by feasibility.
2. LOWER `i`'s CHANCE OF WINNING. Same monotonicity, same bound, same maximizer.
3. FORCE `i` INTO A FALLBACK AT `z`. `j` cannot: the local monitor reads only the local winner's rewards, so
   if `i` wins, only `i` decides whether a switch happens. If `j` wins, `j` can tank, but that opens a local
   fallback in which `i` collects selections worth `1 + mu_i^z - m >= 0` each, against the `0` it collects
   while `j` complies. Weakly better for `i`. Closed.
4. PUSH THE PRICE ABOVE THE WINNER'S CAPACITY, so that the winner is switched out and the pulls are
   redistributed. This is the only version of 3 that `j` could run while LOSING, and it is closed by
   `beta_(2),z <= beta_{W,z}`, hence `tau_z <= (beta_{W,z} - s_n)_+ <= M_W^z` on the good bidding event. The
   `c2-local-mesp` adversary verified the same inequality by exhaustion over 800000 bid vectors (its Section
   5.1 item 2). It is also the scalar inequality of my Section 1.1, so the two mechanisms close it the same way.
5. USE THE ANNOUNCEMENT RULE. The price reaches only agents the platform selects at `z` after Stage 1
   (`PROVER2.md` Section 2, "Messages"), so a local loser never learns `tau_z`; and the phase message is the
   only other message. I did find one signalling channel the report does not mention: the message "fallback"
   tells every agent selected at `z` after a switch that the LOCAL WINNER under-delivered, which is a genuine
   cross-agent signal, and a member of a cartel can therefore broadcast one bit at `z` by deliberately tanking
   a tenure it won. It buys nothing, because it is a signal and not a punishment, and by Lemma C3.0 the
   punishment is what is missing. Worth one sentence in the report, since it is the only way one agent can make
   another agent's information set depend on its own behaviour.

So the substance of Lemma C3.0 is right, and I would go further than the report does: `S^*` is the
maximally aggressive strategy at EVERY stage at once (highest bid, therefore highest price and highest win
probability; compliance, therefore no fallback for the losers; capacity in the fallback, therefore the largest
possible share of any fallback that does occur). That is a strong and unusual property and it deserves to be
stated as such.

### 3.2 A step of the proof of Lemma C3.0 that is asserted, not argued (finding A2, P3)

The proof compares an upper bound on `i`'s utility at one price with a lower bound at another and says the
quantity "is decreasing in `tau_{i,z}`", with the lower bound stated only "when it plays `S^*`". For an
arbitrary fixed `S'_i` a lower price is not obviously better for `i`: it weakens the monitor, so `i` keeps a
tenure it might have preferred to lose, and in the limit `tau_z = 0` the monitor can NEVER fire
(`Z_r >= 0 > -b_n(r)`), so `i` is locked into the primary for all `N_z` visits. The missing argument is that
being switched out is never worth more than continuing: to be switched, `i` must deliver below `tau_z`, which
is at most the best other local capacity; to collect pulls in the local fallback it must deliver at least the
best other local capacity, since the others deliver capacity there; and the free share it gets from explicit
exploration is only `gamma_n/K = O(sqrt(log K / (K n)))` of the remaining visits, that is `o(V_z)`. So the
primary rate `1 + mu_i^z - m` with `m < tau_z` strictly exceeds the fallback rate
`1 + mu_i^z - max_{l != i} M_l^z`, and `i`'s value at `z` really is nonincreasing in `tau_z` for any fixed
strategy. With that paragraph the lemma holds as stated; without it, it holds only for `i` playing `S^*_i`,
which is all that Theorem C3(iii) actually uses.

### 3.3 A real gap in the proof of Theorem C3(iii) (finding A3, P3, repairable in one line)

The proof defines `z` to be CONCEDED if SOME member `j` has `c_{j,z} < M_j^z`, picks `z^*` to be the conceded
profile with `V_z >= eps n` whose Stage 1 ends last, and then asserts: "since `|T(z^*)| >= 2`, the set
`T(z^*) \ {W_{z^*}}` is nonempty and must therefore contain a conceding member `j`". That does not follow. A
profile can be conceded by a member that is NOT locally top, whose bid does not enter the price at all (the two
local top agents still bid capacity, so `beta_(2),z` is unchanged). Such a concession is real (it saves that
member `L_n (M_j^z - c_{j,z})` of Stage-1 effort, which is the local Corollary E1.2) and it is invisible to the
price. If the LAST conceded profile is of that kind, the proof's second step, "`j` re-enters at `z^*` and gains
`(kappa/K) N_{z^*}`", has no `j` to apply to: the non-top conceder cannot win at `z^*` and gains nothing by
raising its bid.

Repair, one line, and the conclusion is unchanged: call `z` PRICE-CONCEDED if some member of
`T(z) \ {W_z}` bids below `M_*(z)`, and choose `z^*` among price-conceded profiles with `V_z >= eps n`. Such a
profile exists whenever the pair deviation is jointly profitable at the linear scale, because the only sources
of gain are (a) saved Stage-1 effort, which is `O(Q L_n) = o(n)` in total, and (b) a lower local price or a
higher local win probability, and both of those require a member of `T(z) \ {W_z}` to bid below `M_*(z)` at a
profile with `V_z = Omega(n)`. With that definition the first step of the proof is immediate rather than
asserted, and everything after it (the timing argument and Lemma C3.0) goes through verbatim.

### 3.4 The timing argument, which is the part that really carries Theorem C3(iii)

I tried to break the timing claim and could not. `beta_{j,z^*}` is formed at the `K L_n`-th visit to `z^*`, no
mechanism object at any profile depends on `j`'s Stage-1 targets at `z^*` before that round (Lemma L plus the
round-robin Stage-1 schedule, which fixes the pull rounds from the arrival path alone), and the partner's only
possible signal afterwards is `tau_{z^*}`, which it receives only if the platform selects it at `z^*` after
Stage 1, that is only if it won there or a switch happened. So the partner can react only at profiles whose
Stage 1 is still open, and the choice of `z^*` makes all conceded such profiles small. I note, and the report
should too, that this is the load-bearing ingredient: Lemma C3.0 alone would NOT give Theorem C3(iii), because
withdrawing a concession at the partner's own monopolised profile is worth `Omega(N_{z'})` to the defector and
is a perfectly good punishment in payoff terms. It is unavailable purely because it cannot be timed. The report
presents C3.0 and the timing as two ingredients; they are not symmetric, and the honest statement is that the
punishment EXISTS in the payoff sense and is ruled out by the information and timing structure.

## 4. Attack on "a deeper concession is more enforceable" (Section 17.2 reading 3)

The claim was found by computation and the brief asked me to be suspicious of it. It is TRUE, it can be derived
rather than measured, and the derivation shows that the report attributes it to one cause when there are two,
the second of which is the more interesting.

### 4.1 The derivation

At a conceded profile `z` the monopolist `i` bids `M_*(z)` and the conceder `j` bids `c_{j,z} < M_*(z)`. The
price is the second order statistic, which is `j`'s own bid: `tau_z = (c_{j,z} - s_n)_+`. `j` collects
`L_n (1 + mu_j^z - c_{j,z})` and nothing after Stage 1. If `j` contests by bidding `M_j^z = M_*(z)` it ties,
wins with probability `1/|T(z)|`, and the price becomes `tau^post = M_*(z) - s_n`, so its gain is

  `(1/|T(z)|) N_z (1 + mu_j^z - tau^post)  -  L_n (M_j^z - c_{j,z})`,

which is the report's criterion. Both terms behave as the report says: the cost is linear in the DEPTH
`M_j^z - c_{j,z}` of the concession, and the prize does not depend on the depth at all. Deeper concessions are
therefore harder to reverse, and the report's explanation, that a bid is delivered performance so re-entry must
be paid for, is the right explanation of the COST half.

### 4.2 What the report does not say, and should (finding A4, P3)

The inversion needs BOTH halves, and the second one is a second-price fact, not a re-entry fact. In an ordinary
cartel the defector's prize GROWS with the depth of the concession, because it undercuts a high cartel price
and keeps most of it. Here it cannot: the low price at a conceded profile is created BY THE CONCEDER'S OWN BID,
being the second order statistic, and the act of contesting destroys it. The defector cannot both win the
tenure and enjoy the price it was conceding, so its prize is pinned at `N_z (1 + mu_j - M_*(z) + s_n)/|T(z)|`
whatever it conceded. The accurate one-sentence version is therefore: "the cost of reversing a concession grows
with its depth while the prize does not, because the concession IS the price and contesting it removes it". I
would state it that way, because a referee who reads only "re-entry costs a bid" will ask why the defector does
not simply enjoy the low price, and the answer is one clause long.

### 4.3 The evasion that would break it, and why it does not

The criterion assumes re-entry is all or nothing: to win, `j` must move its whole Stage-1 bid up to `M_*(z)`.
A cheaper partial re-entry is conceivable, because the bid is an empirical mean of `L_n` Bernoulli draws and
`j` could buy a fractional chance of winning by bidding at an intermediate level. It does not help, and the
reason is quantitative. `beta_j` and `beta_i` differ at the scale
`sqrt(2 M (1 - M)/L_n) = O(L_n^{-1/2})`, so the win probability rises from negligible to a constant only when
`j`'s bid level is within `O(L_n^{-1/2})` of `M_*(z)`; any bid level materially below that wins with
exponentially small probability. So every re-entry with a non-negligible chance costs
`L_n (M_j^z - c_{j,z}) - O(sqrt(L_n))`, which is the criterion's cost up to a `o(L_n)` correction. This is also
why the exact computation reports gains slightly ABOVE the leading-order criterion: `bidprofile.py`'s Stage-1
backward induction lets the deviator choose `M_i` or its floor pull by pull as a function of its own running
count, which is exactly the optimal partial re-entry, and it is worth the `O(sqrt(L_n))` the criterion drops.
The report's "ten to twenty percent of the prize" is that term.

Two smaller checks. Raising the bid without winning (an intermediate bid that only lifts the price the
monopolist pays) is a punishment and not a unilateral improvement, so it does not enter the criterion, and it
is unavailable as a threat for the timing reason of Section 3.4. And the prize uses the RESTORED price
`M_*(z) - s_n`, which is right: after the contest there are two capacity bids at `z`.

### 4.4 Numerical check, reproduced and extended

I reran `ctxprofile.py` on `ctx_division` at `n = 8000` with the market-division array and reproduced the
report's Section 17.2 tables to the digit: local revenue per visit `0.3632` and `0.3716`, total `0.3674` per
round, total exploitabilities `[549.4, 638.3]` and `[905.9, 951.5]`, and the per-profile entries
`[546.8, 612.5]`, `[518.0, 563.6]`, `[2.6, 25.9]`, `[387.9, 387.9]`. The criterion's arithmetic at that
horizon (`N_z = 2276`, `L_n = 862`, `s_n = 0.1472`) is prize `508.9` against cost `689.6` for agent 0's
concession, and the measured `[2.6, 25.9]` agrees.

One caveat about the calibration, which the report states but does not follow through. `ctxprofile.py` uses
`common/design.py`, that is the SCALAR constants `s_n = sqrt(log(2 K n^4)/(2 L_n))`, whereas PL-MESP as
specified in `PROVER2.md` Section 2 uses `ell_n = log(2 n^5)` in both `s_n` and `b_n`. That is a declared
choice ("PROVER1's calibration"), but it moves `s_n` from `0.1627` to `0.1472` at `n = 8000`, and `s_n` enters
the crossover criterion directly through `tau^post`. I redid the crossover with PROVER2's own constants:
prize `526.6` against cost `689.6` at `n = 8000` (no contest) and prize `1427` against cost `1307` at
`n = 20000` (contest). The predicted crossover therefore survives the calibration change, but the report should
say that it checked, because the whole finite-horizon claim turns on a difference of two nearly equal numbers.

## 5. Other claims I checked, and two further precision findings

### 5.1 Checked and found correct

- THE CASE ANALYSIS OF THE NECESSITY PROOF (Section 2.2) is exhaustive and each case's deviation does what it
  says. Case 1 is not vacuous (`c_W <= V_W = M_k` forces `M_k >= c_W`, so its two sub-cases cover everything),
  and case 2c correctly forces `c^max = M_top`, `T = K_top`, which is case (B).
- COROLLARY E1.1's endpoints. `nu(c) = max{bar c, mu_W 1{W honest}} >= mu_H^star` holds in both branches
  (if `W` is honest the maximum sees `mu_W`; if not, every honest agent is a loser and is counted in `bar c`),
  and the upper endpoint `M_(2)` is attained by the loser of capacity `M_(2)`. The interval is right.
- COROLLARY E1.2's exact constant, verified by my independent simulator rather than by their exact code: on
  `unique_top` at `n = 10000` the runner-up's gain from dropping its bid to zero is `+654.6 +- 0.1` against the
  predicted `L_n M_(2) = 1007 x 0.65 = 654.55`, and the top agent's gain is `+1747.1` against the predicted
  `(M_(2) - M_(3)) N_n = 0.25 x 6979 = 1744.75`. Theorem E2(i) is confirmed by a route that shares no code with
  `bidprofile.py`.
- SECTION 8.2 READING 6's finite-`n` overtaking criterion. `sd = sqrt(0.7 x 0.3/1007 + 0.65 x 0.35/1007)
  = 0.0208`, overtaking probability `Phi(-0.05/0.0208) = 0.0082`, value `0.0082 x 6979 x 0.8377 = 48`, against
  a Stage-1 cost of `302`. The report's `52` and `302` are right and the conclusion (exact gain `0.0`) is
  consistent with them.
- THE HONEST-BENCHMARK-UNDER-COLLUSION CHECK (Section 4.4). I re-read the same five steps of
  `sections/appendix_private.tex` independently. Step 3 is the only one where collusion could plausibly enter
  and it is an order-statistic inequality (`beta_(2) >= beta_h` whenever `h` is not the winner) that no
  coalition can touch, because a coalition cannot remove an honest agent's bid from the order statistic and
  cannot lower it below `mu_h - s_n`. I agree with the verdict, including the observation that honesty must be
  a property of the agent rather than a strategy it may abandon inside a coalition.
- SECTION 5.2(b), "defection is neutral, not punished". Same inequality as my Section 2.3 item 3, and the
  report is right to refuse the stronger claim that MESP punishes defection: the defector recovers
  `1 + mu_W - M_(2) - eps` per round in the fallback, within `2 s_n + eps` of what complying pays it.

### 5.2 Finding A5 (P3): "pointwise maximum" is the wrong word in Part II

Corollary C2 defines `g(z) := M_(2)(z)` if `|T(z)| >= 2` and `g(z) := b(z)` if `|T(z)| = 1`, which is correct.
The prose around it, in Section 9a, after Corollary C2, and in finding E1-F6 (the text most likely to reach the
manuscript), calls this "the pointwise maximum of the paper's two guarantees selected profile by profile". It is
not a maximum, it is a selection, and the difference is not cosmetic: at a unique-top profile the equilibrium-set
floor is `b(z)`, which is normally STRICTLY BELOW `M_(2)(z)`, so `max{M_(2)(z), b(z)}` would overstate the
guarantee at exactly the profiles where the result is negative. The report's own `ctx_mixed` numbers show it:
the floor is `(0.35 + 0.80)/2 = 0.575` per round, whereas the pointwise maximum would read
`(0.65 + 0.80)/2 = 0.725`, which is the `S^*` value, not the equilibrium-set value. Fix: write "the paper's two
guarantees, selected profile by profile by the local two-top condition", and delete "maximum".

### 5.3 Finding A6 (P3): one sentence of Theorem E2(iii)'s proof is false as stated

The proof of pair-proofness for `K_top >= 3` says: "On the good event no member can outbid it strictly ... so
the winner's bid is `M_top` and the second order statistic is at least `M_top - s_n`: the price is
`M_top - O(s_n)` whatever the pair does." The second half is false when the pair contains two of exactly three
top agents and both members underbid: the outside top agent `l` then wins alone and the second order statistic
is the larger of the two members' bids, which can be anything. The theorem's conclusion is unaffected, because
what the rest of the argument actually needs is the conditional statement: ON THE EVENT THAT A MEMBER WINS, it
must have bid `M_top`, so `l`'s bid is in the order statistic and the price is `M_top - O(s_n)`. Replace the
sentence with that. Worth noticing separately: in that configuration the pair CAN destroy `Omega(n)` of revenue
while both members strictly lose, so pair-proofness at `K_top >= 3` protects revenue only against pairs that
are trying to gain, which is all the definition claims but is not what the phrase "`S^*` is pair-proof"
suggests to a reader.

## 6. What would have to be true for the surviving claims to break

Stated so that the next reader knows where to aim rather than repeating my work.

1. THE NEGATIVE HALF (case (A) profiles are equilibria) would break if a losing agent could, by its own bid
   alone, either (i) push the announced price above the winner's capacity, or (ii) change the winner's
   continuation. (i) needs `beta_(2) > beta_W` with non-negligible probability, which is impossible because
   `beta_(2) <= beta_(1) = beta_W` by definition and the price is shaded by a further `s_n`. (ii) needs the
   winner's strategy to condition on `tau`, which `S^c` does not do but a general profile does: this is my
   Section 1.2 and it is the whole content of the scope caveat. There is no third route that I found.
2. THE POSITIVE HALF (two top agents force `M_(2) n`) would break if and only if EXP3 admitted a low-revenue
   equilibrium among blind own-selection-count-indexed delivery sequences, that is if the Fallback Lemma of my
   Section 2.4 were false. If someone exhibits such a fallback profile, the rest of the counterexample is
   mechanical: pair it with a high price, have the winner tank after `q = Omega(n)` priced rounds, and check
   that the losing top agent's fallback share exceeds `(1/2) kappa N_n`. I could not build the fallback half,
   and the Bertrand structure (undercutting UPWARD is nearly free and takes nearly every pull) says it does not
   exist. I would put the remaining doubt at "small but not zero", entirely because
   `lem:selected-reactive-exp3` cannot handle a comparator whose per-pull mean is not uniformly bounded below,
   so nobody in this project has a tool that decides it.
3. LEMMA C3.0 would break if any agent had an action that hurts another more than capacity bidding plus
   compliance plus capacity in the fallback. Since the three components are each at the boundary of the
   feasible set and each moves the victim's payoff monotonically the same way, the only way to break it is to
   break the monotonicity, that is to find a victim strategy for which a LOWER price is worse. I showed in
   Section 3.2 why that cannot happen (being switched out is never worth more than continuing), but that
   argument uses that the others deliver capacity in the local fallback; if a future draft changed `S^*`'s
   fallback behaviour, Lemma C3.0 would have to be redone.
4. THEOREM C3(iii) would break if a partner could react to a defection at `z^*` before `t_1(z^*)` or at a
   conceded profile of positive frequency whose Stage 1 ends later. Both are excluded by construction, and both
   would be reopened by exactly the design changes the `c2-local-mesp` adversary already warns against
   (broadcasting the price, any feedback to unselected agents, any tuning constant that depends on realised
   data). The report says this; I am confirming it after trying to break it.
5. THE RE-ENTRY CRITERION would break if partial re-entry were cheap, that is if the win probability rose
   materially at a bid level well below `M_*(z)`. It does not, because bids concentrate at scale `L_n^{-1/2}`.

## 7. Compute record

All runs on the login node, none longer than three minutes, so no Slurm job was submitted; account
`<slurm-account>` and partition `cpu` were therefore not used. Python
`<scratchpad>/venv/bin/python`. Working directory `<scratchpad>/round2/e1adv/`.

| what | script | runtime |
| - | - | - |
| reproduce `K2_unique_top`, `n = 2000`, bids (0.70, 0.35) | `bidprofile.py` (theirs) | 11 s |
| reproduce `ctx_division`, `n = 8000`, market division, all profiles and agents | `ctxprofile.py` (theirs) | 60 s |
| reproduce the out-of-sample entry of Section 17.4, `ctx_division` `z2`, agent 0, `n = 20000` | `ctx20k.py` (mine, calling theirs) | 157 s |
| independent Monte Carlo of MESP, six configurations at `n = 2000` and `n = 10000` | `indep_mesp.py` (mine, from the LaTeX) | about 6 min total |
| loser-stake counterexample of Section 1.2, three bid levels, 400 episodes each | `indep_mesp.py` | 2 min |
| raw-price ablation check of Section 1.1, 400 episodes | inline | 1 min |

The `n = 20000` reproduction returned `exploit in [319.26, 391.20]` against the report's `[319.3, 391.2]`, so
the out-of-sample prediction of Section 17.4, which is the most fragile number in Part II because it is a
difference of two nearly equal quantities, is confirmed on a rerun.

## 8. Bottom line

I did not break the report's central dichotomy, and I tried hard: the negative half is right and its proof is
right, the positive half is right inside its stated family and I believe it is right outside it, Lemma C3.0 is
right, and the surprising finite-horizon claim is right and can be derived. What I found is one sentence that
is false outside the family it was proved in and is currently drafted for the manuscript (Section 1.2), one
proof step of Theorem C3(iii) that does not follow (Section 3.3), one asserted monotonicity (Section 3.2), one
wrong word in the contextual headline (Section 5.2), one false intermediate sentence in Theorem E2(iii)
(Section 5.3), and one harmless inexactness in the exact code (Section 0.1). I also think the report
undersells itself in two places: the blindness of agents (`sections/setting.tex` line 11) makes the necessity
half far more robust outside `Sigma` than "restricted to constant bids" suggests (Section 2.1 and 2.2), and the
strong form reduces to a single statement about EXP3 rather than about MESP (Section 2.4).
