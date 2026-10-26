# Adversary report on REPORT.md (removal of the non-top branch of thm:private-mesp)

Role: adversary. Goal was to break the proposed change. 18 September 2026.
Read line by line: audit/round2/prompts/COMMON.md, audit/round2/B/theorems/nontop-removal/REPORT.md,
sections/Private_information_setting.tex (66 lines), sections/appendix_private.tex (201 lines),
sections/setting.tex lines 1 to 21, sections/experiments.tex line 25,
sections/appendix_experiments.tex lines 35 to 55 and 138 to 145, aamas_body.tex, sections/Intro.tex.
No canonical file was modified. No compute jobs were run, so there is no COMPUTE_LOG.

Per the brief I did not re-run the pathwise-domination or price-below-capacity numerics.

## Verdict up front

I could not break the mathematics. The change survives every attack I ran. I found
one substantive defect in the REPORT's reasoning (Section A3 below: its Section 4.5 states a
sufficient condition that is not sufficient, though its Section 8 states the right one), and
four smaller defects in the edit set (A6, A7, A8, A9). None of them falsifies the claim; all of
them change what the edits must say. Details and the arithmetic are below, attack by attack.

## A1. Attack on the probability budget (REPORT Section 4.4). FAILED, the arithmetic is right.

I recomputed it independently. \(s_n^2=\log(2Kn^4)/(2L_n)\), so \(2L_ns_n^2=\log(2Kn^4)\) and
\(\exp(-2L_ns_n^2)=(2Kn^4)^{-1}\) exactly.

- Old \(\mathcal G_{-i}\): \(2(K-1)\) one-sided Hoeffding tails, total \((K-1)/(Kn^4)\le n^{-4}\).
- Added upper tail for \(\beta_i^{\max}\sim\mathrm{Bin}(L_n,M_i)/L_n\): one more, \((2Kn^4)^{-1}\).
- Total \((2K-1)/(2Kn^4)<n^{-4}\). So \(\Pr(\mathcal G_i)\ge1-n^{-4}\) with the same constant.

Downstream charges. Every bad-event charge in the appendix is of the form (probability) times \(2n\),
and only three probabilities appear: \(\Pr(\mathcal G_i^c)\le n^{-4}\), the monitor crossing \(n^{-3}\),
and the false switch \((2n^3)^{-1}\). None changes, because \(\mathcal G_i\subseteq\mathcal G_{-i}\)
and the monitor and false-switch bounds are conditional on the bidding history, which now merely has
one more event carved out of it. Line 128 (losing branch) quotes \(\mathcal G_{-i}\) and can keep
doing so. Attack failed.

One wording defect, not an error: E2 writes "each of the \(2(K-1)\) two-sided tails". There are
\(K-1\) two-sided events, that is \(2(K-1)\) one-sided tails. Say "one-sided tails".

## A2. Attack on the deletions (E3, E5). FAILED, both deletions are safe.

`grep -rn` over all `.tex` for `private-fallback-low`, `private-fallback-top`, `private-fallback-core`,
`private-price`:

- `eq:private-fallback-low` (label line 119) is referenced exactly once, at line 141, which E5 deletes.
  After E3 and E5 there is no dangling `\eqref`.
- The unlabeled display at lines 138 to 139 (the bound \(q\le4(1+\sqrt{2\ell_n})^2/\delta_i^2\)) has no
  reference anywhere; it is used only by line 141, also deleted.
- `eq:private-price` is referenced at line 136 (deleted by E5) and quoted in prose at line 130. After the
  edits the label survives with no `\eqref`, which LaTeX accepts. Its left half \((V_i-2s_n)_+\le\tau_i\)
  becomes unused in the equilibrium proof; it is the same inequality shape the revenue proof re-derives
  at line 160 for \(M_{(2)}\), so nothing silently depends on it.
- `eq:private-fallback-core` and `eq:private-fallback-top` are untouched and still used at line 130.

I also checked that no proof outside `appendix_private.tex` reaches into this material.
`appendix_public.tex` line 12 and `appendix_contextual.tex` lines 35 and 37 each run their own
capacity-gap argument for their own theorems; none cites the private non-top branch or
`eq:private-fallback-low`. Attack failed.

## A3. Attack on the conditioning enlargement (REPORT Sections 4.5 and 8). The attack lands on the REPORT, not on the claim.

This is the place the brief and the checker both named. I attacked it and found that the REPORT's
stated reason is insufficient, while the correct reason exists and is already in the manuscript.

What the REPORT says in 4.5: "eq:private-fallback-top is converted using \(\tau_i\le V_i\), which holds
on the old \(\mathcal G_{-i}\) and is measurable with respect to \(\mathcal F_{\mathrm{fb}}\); that step
is untouched. The new bound \(\tau_i\le M_i\) is never needed inside a conditional expectation given
\(\mathcal F_{\mathrm{fb}}\)."

Why that is not sufficient. The final accounting does not only use the conditional bound, it integrates
it against the indicator of the piece. It needs

  E[U_i^fb ; {i wins} ∩ G_i]  <=  E[ ((1+mu_i-tau_i)H + R_K(H)) ; {i wins} ∩ G_i ].

From `E[X | F] <= Z` one may multiply by `1_B` and integrate only when `B` is `F`-measurable. Here
\(B=\{i\text{ wins}\}\cap\mathcal G_i\) and \(\mathcal G_i\) contains \(\{\beta_i^{\max}\le M_i+s_n\}\),
which is by construction NOT \(\mathcal F_{\mathrm{fb}}\)-measurable: \(\mathcal F_{\mathrm{fb}}\) is the
deviation execution's history, which records \(Y'_{i,r}\), and \(Y'_{i,r}\) does not determine
\(\mathbf1\{U_{i,r}\le M_i\}\) unless \(m'_{i,r}=M_i\). So the fact that \(\tau_i\le M_i\) is never
needed *inside* the conditional expectation does not license the integration. The REPORT's 4.5 argument
is therefore not a proof of what 4.5 claims to prove.

Why the claim nonetheless survives. The repair is exactly what the REPORT's own Section 8 says, and it
is already asserted in the manuscript. Put
\(\mathcal F_{\mathrm{fb}}^{+}:=\mathcal F_{\mathrm{fb}}\vee\sigma(U_{i,1},\ldots,U_{i,L_n})\). Then:

1. `lem:selected-reactive-exp3` survives the enlargement. Its proof needs only (i) \(I_t\sim p_t\) given
   the pre-selection field, and (ii) the comparator \(j\ne i\) having conditional selected mean at least
   \(v\). The fallback EXP3 coins and fallback reward seeds are fresh and independent of Stage-1 seeds
   (appendix line 4), so (i) holds under \(\mathcal F_{\mathrm{fb}}^{+}\); (ii) holds because \(j\ne i\)
   plays \(S^\star\) and delivers the deterministic \(M_j\). The lemma explicitly permits the other
   agents "arbitrary feasible nonanticipating targets", so letting the deviator's fallback targets see
   \(U_{i,\cdot}\) costs nothing.
2. `lem:private-monitor` survives for the same reason: it is stated "conditional on the bidding history"
   for arbitrary predictable targets, and the primary seeds are fresh.
3. Most importantly, the manuscript already performs this enlargement. Line 125 partitions on
   \(\{i\text{ wins}\}\), which it calls "measurable with respect to the Stage-1 history of the coupled
   executions, which is independent of every post-bid reward seed and coin, so the conditional bounds
   below apply on each piece". The *coupled* Stage-1 history contains the baseline execution's Stage-1
   bids, and the baseline bid of agent \(i\) under \(S^\star\) IS \(\beta_i^{\max}\). So \(\mathcal G_i\)
   is already inside the sigma-field that line 125 names, and line 125's assertion covers it verbatim.

Verdict on A3: the conditioning does close, but not for the reason the REPORT gives in 4.5. Concretely,
the nine edits as written do not contain the sentence Section 8 says is required. E4 leaves
"\(\mathbb E[U_i^{\mathrm{fb}}\mid\mathcal F_{\mathrm{fb}}]\)" unchanged while changing the surrounding
event from \(\mathcal G_{-i}\) to \(\mathcal G_i\), and E6's replacement says only "integrating the
uniform conditional inequalities over private randomization", which is the pre-existing phrase and does
not name the enlarged field. Severity P2 (rigor and referee-exposure, not falsity). Minimal repair: in
E4, after "On \(\mathcal G_i\) we have \(\tau_i\le\min\{V_i,M_i\}\)", add one clause such as "and, since
\(\mathcal G_i\) belongs to the coupled Stage-1 field, which is independent of every post-bid seed and
coin, the conditional bounds below may be taken on \(\mathcal G_i\)". That is a reuse of line 125's own
words and invents nothing.

## A4. Attack on "a price at or below the winner's own capacity is all the winning branch needs". FAILED for the appendix; SUCCEEDED for the main text.

### A4a. Appendix enumeration is exhaustive. Attack failed.

I did not take the REPORT's list of three. I grepped `appendix_private.tex` for every occurrence of
"top", "non-top", \(V_i\) and \(M_{\mathrm{top}}\) and checked each site by hand.

- Line 96 `eq:private-price`: \((V_i-2s_n)_+\le\tau_i\le V_i\). Derived from \(\mathcal G_{-i}\), that is
  from the \(K-1\) other bids only. Holds for every \(i\). Not a use of topness.
- Line 103: "an agent of mean \(V_i\) is an EXP3 comparator and every other-agent mean is at most
  \(V_i\)". Both halves range over \(j\ne i\) only. The deviator's own fallback mean is *not* claimed to
  be at most \(V_i\), and is not used: `eq:private-fallback-core` bounds the non-\(i\) reward by
  \(V_i(H-\bar Q_i)\) and leaves \(\bar A_i\) as itself. Holds for every \(i\), top or not.
- Line 108, `eq:private-fallback-top`: the only requirement is \(1+\mu_i-V_i\ge0\) in order to replace
  \(\bar Q_i\) by \(H\) in \(\mathbb E[U_i^{\mathrm{fb}}\mid\mathcal F_{\mathrm{fb}}]\le(1+\mu_i-V_i)\bar
  Q_i+R_K(H)\). I checked the model: `setting.tex` line 5 gives \(\mu_i\in[0,1]\) and \(M_i\in[\mu_i,1]\),
  hence \(V_i=\max_{j\ne i}M_j\le1\le1+\mu_i\). E3's replacement is correct and the qualifier really was
  free. Not load bearing.
- Lines 114 to 120 `eq:private-fallback-low`: a sharper non-top bound, used only at line 141. Deleted.
- Line 130: "Suppose a top agent \(i\) wins, so \(V_i\le M_i\)". The clause \(V_i\le M_i\) is never used
  again in that paragraph; what is used is \(\tau_i\le V_i\), which is `eq:private-price`. Confirmed by
  reading the paragraph: the chain is \(\tau_i\le V_i\Rightarrow1+\mu_i-V_i\le1+\mu_i-\tau_i\).
- Line 134, baseline target. \(S^\star\) (Private_information_setting line 37) gives a strategic winner
  \(\min\{\tau,M_i\}\) and an honest winner \(\max\{\mu_i,\min\{\tau,M_i\}\}\). Identifying
  \(\min\{\tau_i,M_i\}=\tau_i\) is the one genuine use, and \(\tau_i\le M_i\) is exactly what it needs.
  It is needed twice, not once: for the per-pull baseline utility \(1+\mu_i-\tau_i\), and for the last
  clause of `lem:private-monitor` ("if every primary target is at least \(\tau\), the probability of any
  false switch is at most \((2n^3)^{-1}\)"), since the baseline target must be \(\ge\tau\). Both are
  supplied by the same inequality, so the REPORT's count of one is right in substance.
- Lines 136 to 141 and 149 to 151: the non-top branch itself. Deleted.
- Line 165 (revenue) and line 191 (`prop:tightness`): \(M_{\mathrm{top}}\) and unique-top are internal to
  those statements and do not touch the equilibrium proof.

Sites I checked separately because the brief asked:
- Honest sub-case, line 134. Two cases. \(\tau_i>\mu_i\): baseline target \(\max\{\mu_i,\tau_i\}=\tau_i\),
  identical to the strategic case, needs \(\tau_i\le M_i\) and nothing else. \(\tau_i\le\mu_i\): baseline
  target \(\mu_i\), per-pull utility exactly \(1\); the deviator is honest so \(m\ge\mu_i\) and its
  per-pull utility is at most \(1\) over at most \(N_n\) selected pulls. No capacity comparison of any
  kind. Also \(\mu_i\ge\tau_i=\tau\), so the monitor's false-switch clause applies to the baseline. Clean.
- Losing branch, line 128. It bounds \(\tau\le(\beta_W-s_n)_+\le M_W\) through the *winner's* own
  concentration, \(W\ne i\). No bound on \(\beta'_i\) and no bound on \(M_i\). Already topness free, and
  the enlarged event is not needed there. Confirmed.
- `lem:private-monitor`. Stated for "arbitrary \(\mathcal F_{r-1}\)-measurable targets \(m_r\in[0,M_i]\)"
  with no relation between \(M_i\) and \(\tau\). Target agnostic. Confirmed.
- Fallback comparator. Covered above at line 103.
- Revenue part (lines 157 to 168) and robustness part (lines 173 to 184). Both are statements about
  \(S^\star\) and about an honest agent respectively, with their own good events
  (\(\mathcal G\) over all \(K\) agents, \(2K\) tails giving exactly \(n^{-4}\); and a single one-sided
  Hoeffding-Azuma tail \((2Kn^4)^{-1}\)). Neither mentions the deviator's capacity, \(V_i\),
  `eq:private-price`, `eq:private-fallback-*`, or the non-top branch. Genuinely untouched.
- `prop:tightness`. Untouched, and its conclusion is a lower bound, so an instance-free upper bound does
  not conflict with it.

So within `appendix_private.tex` the enumeration is exhaustive. Attack failed.

### A4b. The main text keeps a fourth topness site that the nine edits do not touch. Attack SUCCEEDED (as a defect in the edit set).

`sections/Private_information_setting.tex` line 64, the "Fallback" step of the proof skeleton, reads:

    Since the deviator receives at most \(H\) fallback pulls and \(1+\mu_i-V_i\ge0\) for a top agent,
    its expected fallback utility is at most \((1+\mu_i-\tau_i)H+R_K(H)\) on the good bidding event,
    where \(\tau_i\le V_i\).

E1 edits line 45 and line 51, E7 edits line 66. Line 64 is edited by nothing. After the nine edits the
8-page skeleton therefore states the fallback bound **for a top agent only**, and then E7's new line 66
asserts that the accounting "covers a non-top winner as well ... and the winner can meet the announced
price", which silently reuses that very fallback bound for a non-top winner. A referee reading only the
main text, which AAMAS requires to carry every essential argument, sees the accounting step invoke a
fallback bound the paper just restricted to top agents. This is a real hole in the deliverable, not in
the mathematics: the inequality \(1+\mu_i-V_i\ge0\) is true for every agent by
\(V_i\le1\le1+\mu_i\), which is the same fact E3 inserts in the appendix.

Severity P2. Minimal repair, a tenth edit: on line 64 replace
`and \(1+\mu_i-V_i\ge0\) for a top agent` by `and \(V_i\le1\le1+\mu_i\) for every agent`.
Without it, E1 to E9 leave the main text internally inconsistent.

## A5. Attack on the line 99 sentence: is there a reason the manuscript could not use the counterfactual bid? FAILED, I found none, and the question is moot.

First, the intent question is moot and I will not litigate it. The REPORT's Section 3 is an inference
about what the author meant, and the brief is right that it is not a proof. But E2 deletes the sentence
and replaces it with a positive, checkable claim: "Only the upper tail of the counterfactual capacity
bid \(\beta_i^{\max}\) is used." I verified that claim directly by counting: the enlarged event adds
exactly one Hoeffding upper tail and nothing else (A1), and the realized bid enters only through the
pathwise inequality at line 86. So the correctness of the change does not rest on the reading of line 99.
What remains is whether some *structural* obstruction exists that the author saw and neither the checker
nor I have. I looked for one along five routes.

1. Adaptive Stage-1 schedule. If the number of Stage-1 pulls agent \(i\) receives could depend on play,
   \(\beta_i^{\max}\) would be defined on a different index set in the two executions and the pathwise
   domination would not be a statement about a fixed sum. Closed: `Private_information_setting.tex`
   line 11 and Algorithm 1 lines 25 to 26 give a fixed loop of \(L_n\) pulls per agent with
   \(L_n=\min\{\lfloor n/2K\rfloor,\lceil n^{2/3}(\log(en))^{1/3}\rceil\}\), a function of \(n\) and
   \(K\) only, and there is no Stage-1 test, elimination or stopping rule. The monitor starts after the
   price is announced (lines 27 to 30).
2. Non-realizability of the monotone coupling. The domination needs \(Y'=\mathbf1\{U\le m'\}\) with a
   uniform \(U\) that is fresh relative to the target. Closed: `setting.tex` line 5 gives
   \(Y_t\sim\mathrm{Bernoulli}(m_{I_t,t})\) with the target chosen first, the theorem's hypothesis states
   it again, and the manuscript already builds the coupling at line 81. The enlargement of the
   probability space by the latent \(U_{i,r}\) does not change any expectation of the deviation
   execution, so \(u_i(n;S'_{i,n},S^\star_{-i,n})\) is unaffected.
3. Feasibility that is not pathwise. If the deviation class allowed \(m_{i,t}>M_i\) on some histories
   (say under an average constraint), \(\mathbf1\{U\le m'\}\le\mathbf1\{U\le M_i\}\) could fail. Closed:
   `setting.tex` line 16 defines \(\mathcal B_{i,n}\) with \(m_{i,t}\in[0,M_i]\) after every history.
4. A price that depends on the deviator's own bid. Under a first-price rule the counterfactual execution
   would face a different price and the comparison would break. Closed: \(\tau=(\beta_{(2)}-s_n)_+\) and
   on \(\{i\text{ wins}\}\), \(\beta_{(2)}=\max_{j\ne i}\beta_j\), including ties with multiplicity, so
   the price is the same functional of the other bids in both executions (line 86, line 125, line 134).
5. Instance-dependent calibration. If \(s_n\) or \(L_n\) depended on the instance the "uniform over
   instances" conclusion would be empty. Closed: \(s_n=\sqrt{\log(2Kn^4)/(2L_n)}\), \(b_n(r)=\sqrt{r\log(2n^4)/2}\),
   \(R_K(H)=3\sqrt{KH\log K}+2K\log K\) and \(L_n\) all depend on \(n\) and \(K\) only.

The only real cost I can identify is one the REPORT does not spell out: the enlarged event is an analysis
object that the platform cannot verify, whereas \(\mathcal G_{-i}\) is also unverifiable but at least is
a statement about bids the platform sees. That is a presentational cost, not an obstruction, because the
proof never requires the mechanism to test the event. I could not construct a mathematical reason the
counterfactual is unusable. Attack failed.

## A6. Attack on E2's line range. SUCCEEDED (mechanical defect in the edit).

E2's heading says "lines 90 to 99", and its body says "Replace the block that begins
`The deviation-independent event` and ends `No concentration around the deviator's capacity is invoked.`".
These two instructions are not the same edit. Line 90 reads in full:

    which is independent of \(i\)'s bid. The deviation-independent event

Applying the line range deletes the clause "which is independent of \(i\)'s bid.", which closes the
display of \(\tau_i\) at lines 87 to 89 and is the statement quoted again at line 125 and at line 134
("the identical price \(\tau_i\), which depends only on the other bids"). E2's replacement text does not
restate it. Anyone applying E2 by line number and not by text anchor removes a load-bearing clause and
leaves the display of \(\tau_i\) with no sentence saying what is being asserted about it.

Severity P2 if applied mechanically, P3 if applied by text anchor. Repair: state the range as "from
`The deviation-independent event` on line 90 through line 99", keeping the first sentence of line 90.

## A7. Attack on E7's drafted main-text sentence. SUCCEEDED (a dropped quantifier).

E7 proposes for line 66:

    This covers a non-top winner as well: a deviating bid is pathwise below the capacity bid
    \(\beta_i^{\max}\), whose upper tail is in the good event, so on every winning history
    \(\tau_i\le M_i\) and the winner can meet the announced price. No capacity gap enters the bound.

Two defects, in the 8 pages, in the sentence that carries the whole change.

- "on every winning history \(\tau_i\le M_i\)" is false as written. It holds on every winning history
  **in the good event**; off \(\mathcal G_i\) the deviator's realized bid can exceed \(M_i+s_n\) and the
  price can exceed \(M_i\). The preceding clause gestures at the event but the assertion does not carry
  it, and dropping exactly this qualifier is the failure mode the whole change is about.
- "pathwise below" should be "pathwise at most": \(\beta'_i\le\beta_i^{\max}\) with equality whenever the
  deviator bids capacity, which is the baseline itself and the case in `prop:tightness`.

Severity P2. Repair: "... so on every winning history in the good event \(\tau_i\le M_i\)", and
"pathwise at most the capacity bid".

## A8. Attack on E6's constant against the printed tables. SUCCEEDED as a small consistency defect.

E6 writes the bound with an explicit \(+1\), namely \(L_n+1+2b_n(n)+R_K(n)+O(n^{-2})\), replacing the
current appendix display \(L_n+2b_n(n)+R_K(n)+O(1)\).

I reconstructed the "Thm." column of `sections/generated/tab_exploit.tex` and `tab_gap.tex` and it is
exactly \((L_n+2b_n(n)+R_K(n))/n\) with the \(O(1)\) dropped, at \(K=3\)
(\(n=2000\): \(L_n=326\), \(2b_n(n)=352.60\), \(R_K(n)=250.24\), sum \(928.84\), \(/n=0.4644\); the
remaining rows reproduce \(0.3203\), \(0.2652\), \(0.1840\), \(0.1283\) to four places). Both tables print
the same value for every instance at a given \(n\), which confirms the REPORT's claim in E9 that the
printed constant is already instance free.

The defect: once the appendix writes \(+1\) explicitly rather than \(O(1)\), the printed constant no
longer equals the displayed bound. At \(n=2000\) the displayed bound is \(0.4649\) per round and the
table prints \(0.4644\); at \(n=5000\), \(0.3205\) against \(0.3203\). Nothing is wrong, but a caption
that says "the explicit constant of Theorem~\ref{thm:private-mesp}" now names a quantity one unit larger
than what is printed. Severity P3. Repair: either keep \(O(1)\) in E6, or have whoever owns the generator
add the \(1\). I computed no new table numbers and propose none.

I also verified the accounting arithmetic of E6 symbolically, since it is the display the theorem now
rests on, and it closes:
Stage 1 saving \(\le L_n\);
winning branch post-bid gap \(\le1+2b_n(n)+R_K(n)\) (the two \((1+\mu_i-\tau_i)\) terms cancel exactly,
\(q+H=N_n\), and no monotonicity in \(\tau_i\) is needed);
baseline false switch \(\le2N_n(2n^3)^{-1}\le n^{-2}\);
monitor crossing \(\le2n\cdot n^{-3}=2n^{-2}\);
\(\mathcal G_i^c\) \(\le2n\cdot n^{-4}=2n^{-3}\);
losing branch post-bid \(\le2n(n^{-4}+(2n^3)^{-1})=2n^{-3}+n^{-2}\).
Sum \(L_n+1+2b_n(n)+R_K(n)+O(n^{-2})\). Every constant is a function of \(n\) and \(K\) only, and for
\(n<2K\) the trivial bound \(2n<4K\) is \(O_K(1)\), so \(O_{\mathrm{inst},K}\to O_K\) in E1 is justified.

## A9. Attack on the remaining downstream text. One site the REPORT does not list.

The REPORT lists E8 (`experiments.tex` line 25) and E9 (`appendix_experiments.tex` lines 46 to 52). I
swept for others.

- `sections/appendix_experiments.tex` line 141: "They say nothing about instances, classes, or horizons
  not computed, and in particular nothing about uniformity as capacity gaps vanish." Not listed in the
  REPORT. It does not become false, since it is a statement about what the experiments establish, and the
  experiments still establish nothing about vanishing gaps. But it is the experimental echo of the
  theorem caveat that E1 deletes, and leaving it invites a referee to ask why the experiments disclaim a
  uniformity the theorem now asserts. Severity P3, flag for the experiments owner alongside E9.
- `sections/generated/tab_gap.tex` caption already reads "the theorem's constant does not depend on it,
  so the bound is loosest at a tie". After the change this becomes true for all focal agents rather than
  only for the top focal agent used in that grid. No edit needed; it gets stronger.
- Abstract (`aamas_body.tex` line 3) and `sections/Intro.tex` lines 21 and 36 say "on every fixed scalar
  instance" and make no uniformity claim. They stay true and could optionally be strengthened. No edit
  required, and I would not add one under page pressure.
- `sections/mlxor_main.tex` line 34 carries \(O_{\mathrm{inst},K}\). COMMON.md lists `sections/mlxor_*` as
  not compiled and not canonical, so it is out of scope. Noting it only so it is not mistaken for a tenth
  edit site.
- `sections/Public_information_setting.tex` line 11 and `sections/appendix_contextual.tex` lines 35 and 37
  keep their own capacity-gap constants. These are different theorems with their own proofs and the
  change does not touch them. Nothing in them cites the private non-top branch.

## Summary of attacks

| # | attack | outcome |
|:-|:-|:-|
| A1 | probability budget and downstream charges | failed, arithmetic correct |
| A2 | deletions remove a silently used step | failed, both deletions safe |
| A3 | conditioning on an unobservable event | REPORT's 4.5 reason is insufficient; the claim survives via line 125; edits need one added clause |
| A4a | topness enumeration not exhaustive in the appendix | failed, exhaustive |
| A4b | topness site missed in the 8-page main text | succeeded, line 64 untouched, tenth edit needed |
| A5 | structural reason the counterfactual is unusable | failed, none found on five routes |
| A6 | E2 line range deletes a load-bearing clause | succeeded, mechanical defect |
| A7 | E7's main-text sentence drops the good event | succeeded, quantifier defect |
| A8 | E6's explicit \(+1\) versus the printed constant | succeeded, cosmetic inconsistency |
| A9 | downstream text the REPORT missed | one site, `appendix_experiments.tex` line 141, P3 |

## What I checked and what I did not

Checked: the full text of `sections/Private_information_setting.tex` and `sections/appendix_private.tex`;
every occurrence of "top", "non-top", \(V_i\), \(M_{\mathrm{top}}\), \(\delta_i\) in `sections/`; every
`\eqref` and `\label` in the private proofs; the model constraints in `sections/setting.tex` lines 5, 13
and 16; the exactness of the nine edits' line numbers against the files as they stand today (E3's 108 and
114 to 120, E4's 130 and 134, E5's 136 to 141, E6's 143 to 153 are all correct; E2's 90 is off by one
clause, see A6); the probability arithmetic; the accounting arithmetic; the printed theorem constant in
both generated tables; the measurability chain for the enlarged event; and each of the five structural
routes in A5.

Not checked: any numerical claim about exploitability, which I was told not to re-run and did not; the
contextual analogues (`D_i(z)`, `e_low`), which the REPORT also declares out of scope and which need
their own Stage-1 determinism check because a cube's bidding block is entered only when the cube is
visited; whether the two non-top focal instances of `tab_instances` should now be reported and with what
numbers, which needs the generator; and whether the paper still fits eight pages after the edits, since
E2 and E6 are net additions of a few lines while E3, E5 and E8 are deletions.

## Would I apply the nine edits as written

No, not as written. I would apply them with four amendments, none of which changes the mathematics:

1. A tenth edit at `sections/Private_information_setting.tex` line 64, replacing
   "and \(1+\mu_i-V_i\ge0\) for a top agent" by "and \(V_i\le1\le1+\mu_i\) for every agent". Without it
   the 8-page skeleton contradicts E7.
2. E2 applied by text anchor, not by the line range 90 to 99, so that "which is independent of \(i\)'s
   bid." survives. Also "one-sided tails", not "two-sided tails".
3. E4 to carry one clause saying the conditional bounds may be taken on \(\mathcal G_i\) because
   \(\mathcal G_i\) lies in the coupled Stage-1 field, which line 125 already declares independent of
   every post-bid seed and coin. This is the step the REPORT's own Section 8 says must be written out and
   that its Section 4.5 mis-justifies.
4. E7 to say "on every winning history in the good event" and "pathwise at most".

With those four amendments I believe the change is correct and I would apply it. I could not break it. I
am not claiming it is error-free; I am claiming that every attack I could construct either failed or
landed on the drafting rather than on the theorem, and that the one step I consider genuinely delicate,
the conditioning enlargement, is justified by a sentence the manuscript already contains and that the
edits leave in place.
