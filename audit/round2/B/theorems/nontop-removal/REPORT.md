# Is the non-top branch of Theorem thm:private-mesp removable?

Verifier: second reader for EXPLORER.md Section 7.4 (f1-continuous-private). 18 September 2026.
Sources read line by line: sections/Private_information_setting.tex (all 66 lines),
sections/appendix_private.tex (all 201 lines), sections/setting.tex line 25 (definition of
B_{i,n}), sections/appendix_experiments.tex lines 35 to 55, sections/experiments.tex line 25,
audit/round2/B/PRIVATE_BOUND_NOTES.md, audit/round2/prompts/COMMON.md. No canonical file was
modified. No compute jobs were run, so there is no COMPUTE_LOG.

## 1. Verdict

The claim holds, with one correction to how it must be written. I could not break it.

The non-top branch (appendix_private.tex lines 136 to 141), the display at lines 149 to 152, the
threshold 2 s_n <= delta_i / 2, the unused equation eq:private-fallback-low, and the theorem's
sentence "The first bound is uniform over the declared deviations for each fixed instance, but not
over sequences whose positive capacity gaps vanish" can all be deleted. The equilibrium bound
becomes instance free:

    sup_{S'_{i,n} in B_{i,n}} [u_i(n; S'_{i,n}, S*_{-i,n}) - u_i(n; S*_n)]
        <= L_n + 1 + 2 b_n(n) + R_K(n) + O(n^{-2}),

for every agent i, top or not, every n >= 2K, and every scalar instance, so O_{inst,K} becomes
O_K in the theorem statement.

The correction: the argument does invoke a one-sided concentration inequality centred at the
deviator's capacity M_i. It is applied to the counterfactual capacity bid beta_i^max, not to the
realized bid beta'_i. The sentence at appendix_private.tex line 99, "No concentration around the
deviator's capacity is invoked", therefore cannot survive verbatim; it must be replaced by a
sentence that says which of the two objects is concentrated. Section 3 below settles that this
sentence is a remark about the realized bid and not a recorded obstruction.

## 2. The two objects, stated precisely

Both already exist in the manuscript, at appendix_private.tex lines 81 to 86.

- Realized bid beta'_i = L_n^{-1} sum_r Y'_{i,r}, with Y'_{i,r} = 1{U_{i,r} <= m'_{i,r}} and
  m'_{i,r} chosen by the deviator. It concentrates around nothing: the deviator can make it 0 or
  make it as large as the seeds allow, and its conditional mean L_n^{-1} sum_r m'_{i,r} is a
  deviation-chosen random variable. Any step that needed beta'_i near M_i would be false.
- Counterfactual capacity bid beta_i^max = L_n^{-1} sum_r 1{U_{i,r} <= M_i}. It is a function of
  the Stage-1 seeds U_{i,1..L_n} alone. It is a Binomial(L_n, M_i) / L_n variable whose law is the
  same under every deviation, exactly as the bids beta_j, j != i, are.

The manuscript already proves the pathwise link beta'_i <= beta_i^max (line 86, "even for adaptive
bid-stage targets"), because 1{U <= m'} <= 1{U <= M_i} whenever m' <= M_i. The claim uses the
realized bid only through this pathwise inequality and never through a distributional statement
about it. That is the distinction the whole argument turns on, and it is respected.

## 3. What the sentence at line 99 is about

Context decides it. Line 99 sits immediately after eq:private-price, whose two-sided bound
(V_i - 2 s_n)_+ <= tau_i <= V_i is derived from G_{-i} = {|beta_j - M_j| <= s_n for all j != i}.
The point being made is that the price bound, and hence everything built on it, uses only the
K - 1 nondeviating bids, so it survives an arbitrary deviation by i. Two independent pieces of
internal evidence show this is a remark about beta'_i and not a recorded reason that also rules
out beta_i^max:

1. The losing branch at line 128 is written so as to avoid any bound on i's bid at all. It gets
   tau <= (beta_W - s_n)_+ <= M_W from beta_{(2)} <= beta_{(1)} = beta_W plus the nondeviating
   winner's own concentration. The natural route, beta_{(2)} <= M_i + s_n, is the one the sentence
   is declining. That is a statement about the realized bid: it is being declined because at that
   point in the text no bound on beta'_i has been made available, not because one is impossible.
2. The manuscript itself defines beta_i^max and states its pathwise domination property one
   paragraph earlier, and uses the coupled Stage-1 sigma-field (line 125, "the Stage-1 history of
   the coupled executions") which contains beta_i^max. If the author had judged beta_i^max
   unusable, defining it and then asserting domination for adaptive targets would be pointless;
   domination is exactly the property that converts an upper tail for beta_i^max into an upper
   bound for beta'_i.

I found no statement anywhere in sections/ that rules out or even discusses the counterfactual
capacity bid's upper tail. I therefore read line 99 as a scope remark on eq:private-price, not as
an obstruction. It was cautious, and the caution was correctly aimed at beta'_i.

## 4. Mechanical checks

### 4.1 Is the bidding schedule reward independent

Yes, and it is fully deterministic. Private_information_setting.tex line 11: "In Stage 1, pull each
agent L_n times". Algorithm 1 lines 25 to 26: "for i = 1..K: pull i for L_n rounds", then choose
the winner. L_n = min{floor(n / 2K), ceil(n^{2/3} (log(en))^{1/3})} depends only on n and K. There
is no monitor, no elimination and no stopping rule inside Stage 1, so no history can shorten,
lengthen or reorder any agent's block. Consequences that the claim needs and that follow:

- Agent i receives exactly L_n Stage-1 pulls under every element of B_{i,n}.
- The map from round index to pulled agent in Stage 1 is the same in the deviation execution and
  in the baseline execution, so seed index r of agent i refers to the same round in both.
- The bids beta_j, j != i, are functions of the seeds alone, since S*_j delivers M_j in bidding
  regardless of history; this is what the manuscript already relies on for G_{-i}.

### 4.2 Are the seeds indexed so that the counterfactual bid is well defined

Yes. appendix_private.tex line 81 indexes by agent and local Stage-1 pull index and couples the
deviating reward to the capacity-target reward on the same uniform U_{i,r}; prop:tightness line 197
uses the same indexing. Because the Stage-1 schedule is deterministic (4.1), local pull index and
round index agree across executions in Stage 1, so beta_i^max is a well defined random variable on
the deviation execution's own probability space. Nothing about Stage 2 seed indexing is needed:
the claim uses only Stage-1 seeds.

The law of (U_{i,r})_{r <= L_n} is i.i.d. uniform under every deviation and also conditionally on
the deviator's private coins, which setting.tex line 25 makes independent randomness and which
appendix_private.tex line 81 conditions on. Hence P(beta_i^max > M_i + s_n) is one fixed number,
not a deviation-dependent one.

### 4.3 Can the deviation class disturb beta_i^max

B_{i,n} (setting.tex line 25) lets agent i choose m_{i,t} in [0, M_i] after selection and before
the reward, using n, its history, mechanism messages and counts, and independent private
randomness; honesty adds m_{i,t} >= mu_i. Routes I checked and why each is closed:

- Change its own or another agent's Stage-1 pull count, or the order of pulls: impossible, the
  schedule is deterministic (4.1).
- Trigger an early phase change during Stage 1: MESP has no Stage-1 test; the monitor starts after
  the price is announced.
- Exceed capacity on a seed, so that Y'_{i,r} > 1{U_{i,r} <= M_i}: impossible by feasibility plus
  monotonicity of the indicator. This is the only property of the deviation used, and it even
  survives dropping the theorem's "targets chosen before fresh seeds" assumption: a target that
  peeked at U_{i,r} would still satisfy 1{U_{i,r} <= m'} <= 1{U_{i,r} <= M_i}.
- Move others' bids: the deviation is unilateral and S*_{-i} bids capacity on every history.
- Move the tie-break priority: appendix_private.tex line 4, priorities and EXP3 coins are
  independent of reward seeds.
- Make the win event disagree between executions: line 86 already proves every deviating win is a
  maximum-bid win, ties included, under the common priority.

I did not find a route. The strongest available lever, adaptive bidding that watches its own
realized Stage-1 rewards, moves beta'_i but not beta_i^max, and beta'_i enters only through
beta'_i <= beta_i^max.

### 4.4 Does the probability budget close

Yes, with no change to s_n and with the stated constant 1 - n^{-4} preserved.
s_n = sqrt(log(2 K n^4) / (2 L_n)), so exp(-2 L_n s_n^2) = (2 K n^4)^{-1} exactly. The current
G_{-i} spends 2 (K - 1) two-sided Hoeffding tails, that is (K - 1) / (K n^4). The new event needs
one upper tail only, (2 K n^4)^{-1}. Total (2K - 1) / (2 K n^4) < n^{-4}. So the enlarged event
still has probability at least 1 - n^{-4} and every downstream bad-event charge in the appendix
(lines 128 and 143) is unchanged, not merely of the same order. The explorer's "at least
1 - 2 n^{-4}" is safe but pessimistic; the one-sided version costs nothing.

### 4.5 Measurability, which is the only place the change is not purely local

The enlarged event is not measurable with respect to the realized history: the platform observes
Y'_{i,r}, not 1{U_{i,r} <= M_i}. So it must be used only inside sigma-fields that contain the
Stage-1 seeds. Where it is needed:

- To identify the baseline primary target as min{tau_i, M_i} = tau_i. This is a statement about
  the coupled Stage-1 sigma-field, which the appendix already uses by name at line 125 ("measurable
  with respect to the Stage-1 history of the coupled executions, which is independent of every
  post-bid reward seed and coin"). Legitimate.
- Nowhere else. In particular eq:private-fallback-top is converted using tau_i <= V_i, which holds
  on the old G_{-i} and is measurable with respect to F_fb; that step is untouched. The new bound
  tau_i <= M_i is never needed inside a conditional expectation given F_fb.

Conditioning the post-bid bounds additionally on i's Stage-1 seeds changes no post-bid conditional
law, because post-bid reward seeds, priorities and EXP3 coins are independent of Stage-1 seeds
(line 4 and line 125). This is the step that must be written out rather than assumed; see Section 8.

## 5. Why tau_i <= M_i is exactly what the winning branch needs

The winning branch at appendix_private.tex lines 130 to 134 uses topness in three places. I checked
each against what a non-top agent has available on the enlarged event.

1. "eq:private-fallback-top gives E[U_i^fb | F_fb] <= (1 + mu_i - V_i) H + R_K(H)". The derivation
   from eq:private-fallback-core needs only 1 + mu_i - V_i >= 0 in order to replace bar Q_i by H,
   and V_i = max_{j != i} M_j <= 1 <= 1 + mu_i by the model (setting.tex line 5, M_i in [mu_i, 1]).
   So this holds for every agent. The qualifier "If i is top" at line 108 is not needed for the
   inequality; it is there only because the manuscript then prefers the sharper
   eq:private-fallback-low for non-top agents.
2. "On G_{-i} we have tau_i <= V_i". This is the right half of eq:private-price and holds for every
   agent, since it comes from the bids of j != i only.
3. "For a strategic agent the baseline primary target is tau_i". The profile S* sets the strategic
   winner's target to min{tau, M_i} and the honest winner's to max{mu_i, min{tau, M_i}}
   (Private_information_setting.tex line 37). Identifying min{tau_i, M_i} with tau_i is the single
   step that uses V_i <= M_i, and only through tau_i <= V_i <= M_i.

So the branch needs tau_i <= M_i and nothing else about topness. Lemma lem:private-monitor is
target-agnostic, the honest sub-case (tau_i <= mu_i, baseline earns one unit per primary pull) uses
no capacity comparison, and the losing branch at line 128 was already topness free.

On G_{-i} intersected with {beta_i^max <= M_i + s_n} and {i wins}: i wins means
beta'_i >= max_{j != i} beta_j, and the announced second order statistic with multiplicity is then
beta_{(2)} = max_{j != i} beta_j, so

    tau_i = (max_{j != i} beta_j - s_n)_+ <= (beta'_i - s_n)_+ <= (beta_i^max - s_n)_+ <= M_i,

which combines with 2 to give tau_i <= min{V_i, M_i}. Only the pathwise domination of the realized
bid is used, exactly as Section 2 requires.

Consistency check that the two branches do not contradict each other. When delta_i > 2 s_n, the old
branch says tau_i >= M_i + delta_i / 2 on G_{-i}, while the new inequality says tau_i <= M_i on a
non-top win. There is no contradiction: on the enlarged good event the two force
{non-top i wins} to be empty for those n, which is a stronger and simpler statement than the old
branch's "its tenure is short". When delta_i <= 2 s_n, that is, at the horizons the old branch could
not reach, the win event is possible and the new inequality is what handles it. The removal
therefore trades a short-tenure argument valid above an instance threshold for a
price-feasibility argument valid at every n.

## 6. The corrected theorem and the exact edits

Line numbers are those of the files as read on 18 September 2026. I am read-only, so nothing below
was applied.

### E1. sections/Private_information_setting.tex line 45 and line 51 (theorem statement)

Line 45: replace `=O_{\mathrm{inst},K}(n^{2/3}(\log n)^{1/3})=o(n),` by
`=O_K(n^{2/3}(\log n)^{1/3})=o(n),`.

Line 51: replace

    The first bound is uniform over the declared deviations for each fixed instance, but not over
    sequences whose positive capacity gaps vanish.

by

    The first bound is uniform over the declared deviations and over all scalar instances with
    \(K\) agents; no capacity gap enters it.

### E2. sections/appendix_private.tex lines 90 to 99 (the good bidding event)

Replace the block that begins `The deviation-independent event` and ends
`No concentration around the deviator's capacity is invoked.` by

```latex
The deviation-independent events
\[
 \mathcal G_{-i}:=\{|\beta_j-M_j|\le s_n\text{ for all }j\ne i\},
 \qquad
 \mathcal G_i:=\mathcal G_{-i}\cap\{\beta_i^{\max}\le M_i+s_n\}
\]
are functions of the Stage-1 seeds alone, because Stage 1 pulls each agent \(L_n\) times on a fixed
schedule and every \(j\ne i\) delivers \(M_j\) there. Each of the \(2(K-1)\) two-sided tails and the
single upper tail is at most \(\exp(-2L_ns_n^2)=(2Kn^4)^{-1}\), so
\(\Pr(\mathcal G_i)\ge1-n^{-4}\). On \(\mathcal G_{-i}\),
\begin{equation}
 (V_i-2s_n)_+\le\tau_i\le V_i.
 \label{eq:private-price}
\end{equation}
On \(\mathcal G_i\cap\{i\text{ wins}\}\) the announced second order statistic is
\(\beta_{(2)}=\max_{j\ne i}\beta_j\le\beta'_i\le\beta_i^{\max}\le M_i+s_n\), so
\begin{equation}
 \tau_i\le\min\{V_i,M_i\}.
 \label{eq:private-price-win}
\end{equation}
Only the upper tail of the counterfactual capacity bid \(\beta_i^{\max}\) is used. The realized bid
\(\beta'_i\) is not concentrated around anything, since the deviator chooses its bidding targets; it
enters only through the pathwise domination \(\beta'_i\le\beta_i^{\max}\).
```

### E3. sections/appendix_private.tex lines 108 to 120 (fallback utility)

Line 108: replace `If \(i\) is top, \(1+\mu_i-V_i\ge0\), and hence` by
`Since \(V_i\le1\le1+\mu_i\) for every agent,`.
Delete lines 114 to 120, that is the sentence beginning `If \(i\) is non-top and \(\delta_i:=\)`
together with equation \eqref{eq:private-fallback-low}. It has no other reference in the repository
(checked by grep over sections/).

### E4. sections/appendix_private.tex line 130 and line 134 (winning branch)

Line 130: replace `Suppose a top agent \(i\) wins, so \(V_i\le M_i\), and let` by
`Suppose the deviation wins bidding, and let`, and replace `On \(\mathcal G_{-i}\) we have
\(\tau_i\le V_i\), so` by `On \(\mathcal G_i\) we have \(\tau_i\le\min\{V_i,M_i\}\) by
\eqref{eq:private-price-win}, so`.

Line 134: replace `For a strategic agent the baseline primary target is \(\tau_i\)` by
`For a strategic agent the baseline primary target is \(\min\{\tau_i,M_i\}=\tau_i\)`.
The rest of the paragraph, including the honest sub-case, is unchanged.

### E5. sections/appendix_private.tex lines 136 to 141 (the non-top branch)

Delete the whole paragraph, from `If \(i\) is non-top, then \(\delta_i:=V_i-M_i>0\).` through
`Its baseline utility is nonnegative.`, including the displayed bound on \(q\).

### E6. sections/appendix_private.tex lines 143 to 153 (accounting)

Replace the block by

```latex
In all cases, monitoring and bidding bad events cost at most twice their probabilities times \(n\),
since per-pull agent utility lies in \([0,2]\). Integrating the uniform conditional inequalities
over private randomization gives, for every agent \(i\), top or not,
\[
 \sup_{S'_{i,n}\in\mathcal B_{i,n}}
 [u_i(n;S'_{i,n},S^\star_{-i,n})-u_i(n;S^\star_n)]
 \le L_n+1+2b_n(n)+R_K(n)+O(n^{-2}).
\]
Since \(L_n=O(n^{2/3}(\log n)^{1/3})\) and \(b_n(n),R_K(n)=O(\sqrt{n\log n})\) for fixed \(K\), this
is the claimed bound; no instance quantity enters it, and the price slack \(s_n\) enters the revenue
bound below but not the deviation gain.
```

### E7. sections/Private_information_setting.tex line 66 (proof skeleton)

Replace `For a top agent the last two steps give` by `For the winner the last two steps give`, and
replace the sentence

    A non-top agent faces \(\tau_i\ge M_i+\delta_i/2\) once \(2s_n\le\delta_i/2\), so the monitor
    ends its tenure after \(O(\log n/\delta_i^2)\) pulls and the same fallback bound leaves it
    \(O(R_K(n)/\delta_i)\).

by

    This covers a non-top winner as well: a deviating bid is pathwise below the capacity bid
    \(\beta_i^{\max}\), whose upper tail is in the good event, so on every winning history
    \(\tau_i\le M_i\) and the winner can meet the announced price. No capacity gap enters the bound.

Delete the final sentence of the paragraph, `The non-top branch of the proof applies once
\(2s_n\le\delta_i/2\) for the capacity gap \(\delta_i\), which for gaps of order \(10^{-2}\) exceeds
any horizon we can simulate.`

### E8. sections/experiments.tex line 25 (limitations)

Delete `and its non-top branch requires the capacity gap to exceed twice the bidding radius, which
for gaps of order \(10^{-2}\) exceeds any horizon we can simulate`, keeping the rest of the
sentence, which still says the mechanism is scalar and needs a known horizon.

### E9. sections/appendix_experiments.tex lines 46 to 52 (flagged, not drafted)

The sentences `For a focal agent that is not top, the proof's branch condition \(2s_n\le\delta_i/2\)
fails at every horizon we can run ... the upper bound is uninformative there` become false once E1
to E8 are applied, and must be rewritten by whoever owns the experiments. Two facts for that
rewrite, both checked here: the theorem constant printed in Table~\ref{tab:exploit} and
Table~\ref{tab:gap} is already instance free, and the two non-top focal instances of
Table~\ref{tab:instances} (`honest top`, focal agent 2, and `low-gap non-top`, focal agent 2)
currently appear in no results table in sections/generated/. Whether to report them, and with which
numbers, needs the generator in scratch/experiments/final/; I computed nothing and propose no
numbers.

## 7. What does not change

- The rate. It is still \(n^{2/3}(\log n)^{1/3}\), still set by \(L_n\), and Proposition
  prop:tightness still shows it is attained. Only the quantifier over instances changes.
- The revenue bound. It keeps its \(n s_n\) term, which comes from
  \((M_{(2)}-2s_n)_+\le\tau\), not from any deviation gain.
- The honest benchmark. Its proof uses a one-sided Hoeffding-Azuma bound on the honest agent's own
  bid from below (line 177), which is a different and already sound step.
- Lemma lem:private-monitor, Lemma lem:selected-reactive-exp3, eq:private-fallback-core and
  eq:private-fallback-top. None is touched.
- The losing branch at line 128. It never used any bound on the deviator's bid and still does not.
- eq:private-price. Its right half is still quoted in prose at line 130; its left half becomes
  unused once E5 is applied and may be kept for the revenue discussion.

A plausibility check that points the same way. The old non-top bound
\(L_n+O(1+\log n/\delta_i^2+R_K(n)/\delta_i)\) diverges as \(\delta_i\downarrow0\), while the
top-agent bound at \(\delta_i=0\) is finite and small. A guarantee that blows up as an agent becomes
a tie for top, when the tie case itself is fine, is the signature of an artifact of the proof rather
than of the mechanism. The removal makes the bound continuous in the gap.

## 8. The step I consider least secure, and residual risk

Least secure: the conditioning enlargement of Section 4.5. The event
\(\{\beta_i^{\max}\le M_i+s_n\}\) is not measurable with respect to the history the platform
observes, so every conditional bound that is intersected with it must be stated with respect to the
coupled Stage-1 sigma-field, which contains the Stage-1 seeds of agent \(i\), and the post-bid
bounds must be known to be unaffected by that extra conditioning. The manuscript already asserts the
two facts this needs, at line 4 ("All priorities and EXP3 coins are independent of reward seeds")
and at line 125 ("measurable with respect to the Stage-1 history of the coupled executions, which is
independent of every post-bid reward seed and coin"). I believe the step is correct, but it is the
one a referee can most easily mistake for sloppiness, and the rewrite must say explicitly that the
baseline comparison at line 134 is taken conditionally on the coupled Stage-1 sigma-field. I do not
claim the result is correct; I claim I could not break it, and that every other step reduces to an
inequality already proved in the appendix.

Second, weaker, uncertainty: Section 3 is an inference about what line 99 was for, from context and
from the shape of the losing branch. It is not a proof of authorial intent. It does not affect the
mathematics, and in any case the rewrite replaces that sentence rather than relying on it.

Not verified here, and out of scope:

- The explorer's further statement that "the same deletion applies to PROVER1's \(D_i(z)\) and
  PROVER2's \(e_{\mathrm{low}}\)". Those are contextual constructions with a per-cube price and a
  per-cube schedule; the Stage-1 determinism check of Section 4.1 has to be redone there, because a
  cube's bidding block is entered only when the cube is visited, which is context driven. I did not
  do that check.
- Any numerical claim. I ran no code and regenerated no table.
- Whether the deleted material should be kept as a remark. The new argument supersedes it at every
  \(n\), so I see no reason to keep it, but the sharper non-top fallback bound
  \(2R_K(n)/\delta_i\) of eq:private-fallback-low is strictly better than
  \((1+\mu_i-\tau_i)H+R_K(H)\) for large gaps and could be retained as a remark if anyone wants the
  gap-dependent constant.
