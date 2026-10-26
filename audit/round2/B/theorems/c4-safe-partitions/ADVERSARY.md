# Adversary report on C4 (safe partitions), 18 September 2026

Target: `audit/round2/B/theorems/c4-safe-partitions/REPORT.md` (Sections 0 to 9.3), the material it
builds on (`audit/round2/B/scouts/CONTEXT_ONLY_PARTITIONS.md`, Sections 0, A, B, C), and the
canonical files it speaks about (`sections/contextual_samf_algorithm.tex`, `sections/contextual.tex`,
`sections/setting.tex`, `sections/appendix_contextual.tex`). All four were read in full, together
with `audit/round2/prompts/COMMON.md`.

No canonical file was modified. My own code, all of it new and independent of the worker's scripts
(which I did not read, precisely so that the reproductions would be independent), is in
`<scratchpad>/round2/adversary-c4/` (`sim.py`, `w1.py`, `w2.py`, `w3.py`, `w3b.py`). Every run took
under two minutes on the login node; no Slurm job was needed, so there is no COMPUTE_LOG entry.

Summary of the result of the attack, so that it is not buried:

- **Theorem 3 (monotonicity) survives.** I reproduced it, checked every hypothesis, and confirmed
  that the horizon-free form (b) really is horizon free. One genuine scope caveat, with a one line
  repair, in A1.1.
- **Theorem 4 (robustness at honest play) survives**, and I strengthened it: adding the freeze
  clause to COAT itself, with COAT's own schedules and nothing else changed, loses a linear amount
  on the same instance. This is the witness that most cleanly isolates reward dependence.
- **Theorem 5 is broken as a witness for reward dependence.** The theorem is true as stated, but on
  its own instance W2 the reward dependent clause of RA-ETC is almost surely inert, and the identical
  failure (`n/4` deviation gain, `0.175 n` benchmark loss, to four decimal places, at every horizon
  tested) is produced by a rule that satisfies (R1), (R2) and (R3). Section A1.3.
- **Consequently the headline of Section 0 item 1, "context only partitions are safe", is false**
  under the report's own definition of safe (Section 1.3), and the Corollary of Section 4.5 is false
  in its "if" direction. The body statements that these headlines summarise are true and are
  correctly proved; the summaries are strictly stronger than what is proved. Section A2. This is the
  shape the task warned about.
- The accelerate only escape is **larger** than the report thinks, not smaller: its sketch for
  breaking monotonicity does not work for the anytime sandwich it proposes, and there is a reason to
  believe accelerate only rules keep contextual monotonicity with an `o(n)` remainder, losing only
  exactness. Section A3.
- The dependence of the converse on "no known modulus for the delivered maps" is real, and the
  report's account of which theorems die is correct. Combined with A1.3 this is worse for the
  converse than the report says: under the amendment the only surviving witness is the one that does
  not distinguish reward dependent from context only rules. Section A4.
- COAT: Lemma 7, Lemma 7', the balancing in Theorem D.1, the exact pathwise monotonicity of
  Theorem D.2, and the "never worse in the exponent" claim all check out. Two rows of the Theorem 3
  numerical table do not reproduce. Section A5.
- Both citations check out against primary sources, including the verbatim quotations. Section A6.

## A1. The three witnesses

My simulator is an independent reimplementation of the segment reduction of Section 3: the dyadic
tree on `[0,1)` in the coordinate `u`, leaves carrying the manuscript's `ETC(q_l)` rule (`q_l`
uniform exploration permutations of `[K]`, then commitment to the largest exploration empirical mean
with a per leaf uniform priority permutation for ties, exploitation rewards ignored), fresh
statistics per leaf, nothing inherited. Cell means are computed exactly from the maps, not estimated.

Calibration against the report before I used it to attack anything. On instance W3 with
`c = 0.1875`, `theta_0 = 1/8`, `q_0 = 2000`, my deficit per round is 0.02083 at `n = 2e5` and
0.01829 at `n = 8e5`, against the report's 0.02082 and 0.01838; my COAT figures on the same instance
are 0.06054 and 0.01677 against the report's 0.06063 and 0.01676. So the two implementations agree
where they can be compared, and where they disagree (Section A5) the disagreement is informative.

### A1.1 Theorem 3, monotonicity: survives

Hypotheses of `thm:grid-etc` on instance W1, checked one at a time against the canonical files.

- `\mathcal X = [0,1]^D` with `D = Kd = 3`: yes, `d = 1`, `K = 3` (`sections/setting.tex` line 48).
- Intrinsic functions `L`-Lipschitz (the standing assumption of
  `sections/contextual_samf_algorithm.tex` line 3): `mu_1 = 0`, `mu_2 = 0.3`, `mu_3 = 0` are
  constants, so Lipschitz for every `L >= 0`. The theorem's constants depend on `K, D, L` only, so a
  degenerate `L` is not a loophole.
- Feasibility `0 <= m_i <= M_i(x_i)` pointwise and honesty `m_i >= mu_i` pointwise
  (`sections/setting.tex` line 59, line 51): `m_1 = 0.05 <= M_1 in {0.3, 0.9}`; `m_2 in {0.3, 1.0}`
  with `M_2 = 1` and `mu_2 = 0.3`; `m_3 in {0.7, 0}` with `mu_3 = 0`. All hold.
- `S_HDS` membership: the maps are measurable, stationary, fixed before play. Yes.
- The comparison is the manuscript's own: "the profile replacing `m_i` pointwise by `M_i`", and the
  quantity is `E T_j(R;n)` for `j != i` with `R = \mathcal X` (`sections/contextual.tex` line 10).
  The witness raises agent 1 and reports agent 3, so the direction is the forbidden one.
- Capacities are not required to be Lipschitz by `thm:grid-etc` (only the rate form of
  `thm:contextual-public` asks for that), so the step capacity `M_1` is legal.

Arithmetic, recomputed by hand. Root cell means `(0.05, 0.65, 0.35)` base and `(0.60, 0.65, 0.35)`
raised; `Lft` raised `(0.30, 0.30, 0.70)`; `Rgt` raised `(0.90, 1.00, 0.00)`. Base root gap
`0.65 - 0.35 = 0.30 > theta_0 = 0.125`, so freeze on agent 2; raised root gap
`0.65 - 0.60 = 0.05 < 0.125`, so split; `Lft` gap `0.40 > theta_1 = 0.0625`, freeze on agent 3;
`Rgt` gap `0.10 > 0.0625`, freeze on agent 2. All correct.

The horizon-free form (b) is the claim I was asked to check hardest, and it holds. With
`eps = 0.015` the Hoeffding exponent is `2 eps^2 = 4.5e-4`, so `6 K exp(-2 q_0 eps^2) <= 1/8`
needs `q_0 >= ln(144)/4.5e-4 = 11045`, a number and not a function of `n`; then
`E T_3(S^{1up}) - E T_3(S) >= n/2 - K q_1 - N_0 - 2 delta n >= n/4 - K q_1 - N_0` with
`K q_1 = 12 q_0` a constant. The margin is genuinely linear with a fixed rule at every horizon. I
also checked the inequality `T_3 >= V_Lft - K q_1 - N_0` on the good event in the two cases the
proof does not separate (`V_Lft` below `K q_1`, and `V_Lft` between `K q_1` and `N_1`): in the first
the right hand side is negative, in the second the leaf has already committed to agent 3, so the
inequality holds in both.

Reproduction, 6 seeds, `n = 200000`, `q_0 = 2000`, `theta_0 = 1/8`, `N_l = 8000 * 8^l`:

| rule | `E T_3` base | `E T_3` raised |
|:-|:-|:-|
| RA-ETC, no floor | 2000.0 | 90982.8 (s.e. 90.7) |
| RA-ETC, context-only floor | 2000.0 | 89989.2 (s.e. 95.8) |

against the report's 2000.0 / 91098.7 and 2000.0 / 90113.0. The differences are about one standard
error of the difference. The direction, the size (`0.45 n`) and the exactness of the base value are
confirmed.

**The one caveat, and its repair (P3, worth one line in the paper).** `sections/setting.tex` line 59
contains a conditional clause: "If agents observe only their own contexts `x_i`, their maps must
depend only on `x_i`." Under the default reading (the selected agent observes the full profile,
line 44) W1 is legal, because `m_2` and `m_3` are allowed to depend on `u = x_1`. Under the
parenthetical own context reading they are not: `nu` is supported on
`{(u,0,...,0)}`, so `x_2 = x_3 = 0` almost surely and `m_2, m_3` would have to be constants, and the
witness collapses. The repair is one symbol: put `nu` on the diagonal `{(u,u,...,u)}` instead of on
the first axis, exactly as the report already does for instance W4 in Section 4.6. The dyadic
reduction of Section 3 is unchanged (the level-`l` cube containing `(u,...,u)` is `I_l(u)^D`, and the
diagonal meets exactly two of its `2^D` children), every cell mean is unchanged, and every agent's
map is then a function of its own context. I checked that W2, W3 and W4 are already immune (their
maps are constants, or functions of the agent's own coordinate, or `nu` is already the diagonal).
Recommendation: state W1 on the diagonal, so the witness does not depend on which of the two
readings of the model a referee takes.

### A1.2 Theorem 4, robustness at honest play: survives, and can be strengthened

Hypotheses on instance W3 (`K = 2`, `D = 2`): `mu_1(x_1) = M_1(x_1) = 1 - x_1` is 1-Lipschitz and
lies in `[0,1]`; `mu_2 = M_2 = c` is constant; both agents are honest and forced to deliver their
capacity, so both maps are in `S_HDS`; `b(X) = max(1-u, c)`. Every hypothesis of `thm:grid-etc`
holds, and the instance is legal under both readings of the model, since agent 1's map is a function
of `x_1` alone and agent 2's is constant.

Arithmetic. With `c := (1/2 - theta_0)/2`, the true root gap is `1/2 - c = 1/4 + theta_0/2`, which
exceeds `theta_0` exactly when `theta_0 < 1/2`, with slack `1/4 - theta_0/2 = c`. On the event that
both empirical means are within `c/4`, the empirical gap is at least `1/2 - 3c/2`, and
`1/2 - 3c/2 - theta_0 = c/2 > 0`. The per round deficit after the freeze is
`int_0^1 (c - 1 + u)_+ du = c^2/2`. All correct, and at `c = 0.1875` this is `0.017578`.

Reproduced, 3 seeds: 0.02083 at `n = 2e5` and 0.01829 at `n = 8e5` (report: 0.02082, 0.01838),
against Static Grid-ETC and COAT, both of which decay.

Two attacks that failed.

1. *Is the margin an artefact of a horizon dependent rule?* The theorem asks for `q_0 -> infinity`,
   which makes the witness rule horizon dependent. It need not be: with `q_0` a fixed constant the
   failure probability is a constant `delta < 1` and the conclusion becomes
   `(1 - delta) (c^2/2) n - O(1)`, still linear. So a horizon-free form of Theorem 4 exists and the
   report understates its own result here.
2. *Does a vanishing threshold schedule escape?* No. The instance parameter `c` only has to satisfy
   `c < 1/2 - theta_0`, so a rule with `theta_0 -> 0` is defeated by any fixed `c in (0, 1/2)`, with
   loss `c^2 n / 2`. The theorem is therefore true for every threshold schedule with
   `liminf theta_0 < 1/2`, which is more than it claims.

**Strengthening, and the reason this is the witness to keep.** Theorems 3 and 4 both compare RA-ETC
with rules that differ from it in more than the reward clause (RA-ETC's schedules are `q_l = q_0 4^l`
and `D_l = K q_l` or `N_l`, COAT's are `q_l = 4^l` and `N_l = K 8^l`). A referee can therefore ask
whether the schedules, not the clause, are doing the work. They are not, for Theorem 4: I ran COAT
with its own schedules and with the single freeze sentence of Section 3 added, and nothing else
changed, on W3 with `theta_l = 2^{-l}/8`, 5 seeds:

| `n` | COAT | COAT with the freeze clause |
|:-|:-|:-|
| 200000  | 0.06069 | 0.02038 (sd 0.015) |
| 800000  | 0.01672 | 0.02366 (sd 0.013) |
| 3200000 | 0.03274 | 0.02375 (sd 0.013) |

(deficit per round). COAT's figure is the sawtooth the report describes and is on its way to zero;
the freeze variant's does not decay, and its large seed to seed spread is the signature of the
mechanism, since with `q_0 = 1` the root freezes on a single observation per agent and commits the
whole run to whichever agent that observation favoured. Note that Theorem 4's own proof does not
apply verbatim to this variant (it needs `q_0 -> infinity`), so this is a separate confirmation of
the mechanism, not of the theorem. It is the cleanest form of the converse available: *one sentence
added to COAT, every schedule identical, a linear loss at honest play with no deviation at all.*

### A1.3 Theorem 5, the `n/4` deviation: the theorem is true and the witness is broken

This is the attack that succeeded, and the counterexample is the report's own instance.

**The claim I am breaking.** Not the statement of Theorem 5, which I verified and reproduced
exactly. What I break is its use: Section 0 lists it as the third of "three explicit witnesses"
that reward dependent partitions fail; Section 4.7's one sentence for the paper says a partition
"must not depend on the rewards through a decision that can stop the refinement ... because each of
those hands a geometric choice to the agents"; Proposition 7(A) says of this very mechanism "and the
agents control it, because they control whether the top two separate"; and Section 6, recommendation
1, proposes to put this instance in the paper as the converse's witness, "four lines" of exact
arithmetic. On instance W2 no agent controls anything and no reward dependence is exercised.

**The observation.** On W2 the two top agents deliver exactly `1`. A Bernoulli(1) variable is
identically 1, so in every leaf, at every level, under `S^max` and under the deviation alike, the
exploration empirical means of agents 2 and 3 are both exactly 1 and `G_C = 0 <= theta_l` with
probability one. The freeze branch of RA-ETC is therefore never taken on any sample path. The
realized partition process of RA-ETC on W2 is almost surely equal to the partition process of the
rule obtained by deleting the reward sentence altogether.

**The counterexample rule.** Define **A0**: half open dyadic cubes of `[0,1)^D`, root at level 0;
each leaf runs `ETC(q_l)` with `q_l = q_0 4^l` on its own fresh statistics and its own coins; a leaf
is replaced by its `2^D` dyadic children at its `K q_l`-th visit. Nothing is inherited, including
visit counts. A0 satisfies (R1), (R2) and (R3), by exactly the verification the report gives for
COAT in its own Section 1.2: `P_{t+1}` differs from `P_t` only when the label of round `t` has now
been carried `K q_{lev}` times, which is a function of the label sequence alone, so (R1) holds;
statistics are label local and fresh, so (R2) holds; the primitives are the model's, so (R3) holds.
A0 is COAT with the single schedule `N_l = K 8^l` replaced by `N_l = K q_l`. It contains no reward
dependence of any kind.

**What A0 does on W2.** Every leaf splits at the end of its exploration phase, so every round of the
run is an exploration round, and exploration blocks are uniform permutations of `[K]`, so each agent
receives `n/K + O(n^{1/3})` selections whatever it delivers. Hence, with `mu_4 = 0`, `M_4 = 1`,
`m'_4 = 0`:

`u_4(n; m'_4, S^max_{-4}) - u_4(n; S^max) = (n/4)(1 - 0) - (n/4)(1 - 1) = n/4 - O(n^{1/3})`,

and `P(n; m'_4, S^max_{-4}) = (n/4)(0.9 + 1 + 1 + 0) = 0.725 n` against `E sum_t b(X_t) = 0.9 n`.
These are the same two numbers Theorem 5 reports, derived without any reward dependence.

**Measured**, 3 seeds each, `q_0 = 200`, `theta_0 = 1/8`:

| `n` | RA-ETC no floor, gain / `n` | A0 (context only), gain / `n` | RA-ETC deficit / `n` | A0 deficit / `n` |
|:-|:-|:-|:-|:-|
| 12500  | 0.2500 | 0.2500 | 0.1750 | 0.1750 |
| 50000  | 0.2500 | 0.2500 | 0.1750 | 0.1750 |
| 200000 | 0.2500 | 0.2500 | 0.1750 | 0.1750 |
| 800000 | 0.2500 | 0.2500 | 0.1750 | 0.1750 |

The RA-ETC column reproduces the report's table exactly. The A0 column is the counterexample: a rule
inside the report's own safe class, on the report's own instance, with the report's own two constants.

**Why the defence does not work.** One could answer that RA-ETC's leaf lifetime is reward determined
in general and that W2 merely happens to pin it at the minimum. That is exactly the point. The
hypothesis Theorem 5 actually uses is the one it names, "no context-only floor on a leaf's lifetime",
and that hypothesis is a property of the *schedule*, available to context-only rules and forbidden to
none of them. The tie that drives the mechanism is not a strategic choice either: it is forced by the
instance, since agents 2 and 3 have capacity 1 and `S^max` is the all-maximum profile, and it
persists unchanged under the deviation. The report's own answer to its Objection 2 makes this worse
rather than better: replacing the delivered `1` by `p in (0,1)` makes the split happen with
probability `1 - delta(q_0)` uniformly over levels, that is, it makes the reward clause *almost*
inert rather than exactly inert, and the failure survives for the same reason A0's does.

**Consequences, in decreasing order of importance.**

1. Section 6, recommendation 1, should not be followed. If the instance of Theorem 5 is the four
   lines that go into the paper as the converse's witness, the paper will be asserting that reward
   dependence causes a failure that its own safe class also exhibits, and a referee who deletes the
   reward clause from the displayed rule will get the same `n/4`. Theorem 4, in the COAT plus freeze
   clause form of A1.2, is the witness that survives that test; Theorem 3 is the witness for
   monotonicity.
2. Proposition 7(A)'s sentence "and the agents control it, because they control whether the top two
   separate" is not exercised by any instance in the file. Mechanism (A) is real, but the file
   contains no instance in which reward dependence, rather than the schedule, triggers it. Producing
   one is open: it would need an instance in which a unilateral deviation changes whether leaves die
   at the end of exploration, which requires the deviator to be one of the two tied tops, and at
   `S^max` the tie is forced. I tried and did not find one.
3. The classification line in Section 8 should read, for Theorem 5, "PROVED; but the instance does
   not exercise the reward dependence, and the same failure is attained by a rule satisfying (R1) to
   (R3)".

## A2. "Context-only partitions are safe" is false as stated

Section 1.3 defines a rule to be **safe** if it keeps contextual sharp adaptivity, contextual
monotonicity, contextual FATA, global robustness and the public restricted equilibrium, "with `o(n)`
remainders uniformly over `S_HDS`, on every instance of the model, with an algorithm that is allowed
to know `n, K, D` and nothing else". Section 0 item 1 is headed "*Context-only partitions are safe.*"

A0 of Section A1.3 satisfies (R1), (R2) and (R3), knows only `K`, `D` and a constant `q_0`, and on
instance W2 loses `0.175 n` of the honest benchmark and concedes an `n/4` unilateral deviation gain
at a profile satisfying the two-top hypothesis. So (R1) and (R2) and (R3) do not imply safety, and
the heading is false. (A cruder witness makes the same point: the one cell partition with
`q_n = n/K` is context only, trivially satisfies (R1) to (R3), and gives every agent `n/K`
selections whatever it delivers. A0 is the pointed version because it is anytime, dyadic, and
differs from COAT only in one schedule constant.)

What *is* proved, and what I checked line by line and believe, is the sentence that follows the
heading: under (R1) to (R3) every cell epoch is a fixed-mean instance with the future independence
the manuscript's proofs use (Lemma 1, Lemma 2), and the two executions of the monotonicity coupling
carry the same partition. Corollary 3 of Section 2.2 then says explicitly "What does **not** carry
over automatically is the aggregation over cell epochs", and Section 5 supplies the aggregation for
COAT's schedules and only for those. So the mathematics is right and the summary is stronger than
the mathematics. Three places where the overstatement is load bearing:

1. **Section 0 item 1's heading.** Repair: "Context-only partitions keep the cell law and the
   monotonicity coupling; safety additionally requires a schedule whose exploration fraction and
   whose mesh are controlled, which is what Section 5 supplies for COAT."
2. **The Corollary of Section 4.5**: "An RA-ETC rule with `theta_l -> 0` is safe in the sense of
   Section 1.3 if and only if its freeze-or-split decision is almost surely a function of the
   contexts alone." The "if" direction is false for the decision schedule `D_l = K q_l`, which the
   Definition of RA-ETC in Section 3 explicitly permits ("`D_l := K q_l` (no floor)"): on W2 that
   rule's decision *is* almost surely a function of the contexts alone, and it is not safe. The
   Corollary needs the added hypothesis that the decision schedule has a context-only floor with
   `K q_l / D_l -> 0`, which is exactly what the two rules named in its "if" proof (COAT, the static
   grid) have and what the no floor branch does not.
3. **Escape 4 of Section 4.7**, "A depth cap reached immediately ... they escape because their reward
   dependence never fires." The stated reason is not a reason: A0 is a rule whose reward dependence
   never fires on W2 and it is unsafe there. The correct reason is that the *particular*
   context-only rules named in escape 4 (a single cell, the static grid) are safe for their own
   reasons.

Severity: P1. The claim that reward dependence is what separates safe from unsafe is the paper's
intended message, and this shows the separation is not where the summary puts it. It is not P0,
because no proof in the file is wrong and the manuscript's own algorithm is unaffected.

## A3. The scope of the converse, and the escapes

I was asked to find more escapes or to close the named ones, and to settle the accelerate-only
monotonicity question if I could. I did not close any escape. I found that the accelerate only
escape is larger than the report believes, and that the report's own sketch for narrowing it does
not work.

### A3.1 The accelerate-only sketch does not work for the schedules it is offered for

Section 4.7 item 2 defines accelerate only rules by a sandwich `K q_l <= N_l^min <= N_l^max` between
two context-only schedules, gives the concrete anytime example `N_l^min = K 8^l`,
`N_l^max = 2 K 8^l`, and then sketches a monotonicity failure: "rescale `nu` into a single level-`l`
dyadic cube so that one leaf carries `Theta(n)` visits ... the timing difference
`N_l^max - N_l^min = Theta(n)`".

For that example, and for every sandwich with `N_l^max` a function of the level alone, the sketch is
unavailable at any fixed level: a level-`l` leaf carries at most `N_l^max = 2 K 8^l` visits, a
constant that does not depend on `n`, so the timing difference at a fixed level is `O(1)` and not
`Theta(n)`. Rescaling `nu` into a level-`l*` cube does not help, because the tree does not stop at
`l*`: the rule keeps splitting below it, and the mass that was rescaled into the cube is then spread
over the cube's descendants exactly as it was spread over the original tree.

Making `N_l^max = Theta(n)` at the operative level is possible only with a horizon-dependent
schedule, and such a schedule is outside the class the escape is about: a leaf that carries
`Theta(n)` visits at level `l` contributes `2^{-l} Theta(n)` to `S = sum_l 2^{-l} n_l`, and
`S = Theta(n)` makes the Lipschitz bias term linear, so robustness fails and the rule is not one of
the "statistically safe" accelerate only rules whose monotonicity was the question. I confirmed the
mechanism is otherwise real: the horizon-dependent accelerate only rule with `N_0^min = n/4`,
`N_0^max = 3n/4` on the report's own instance W1 splits the root at `3n/4` under the base profile and
at `n/4` under the raise, giving `E T_3` about `0.125 n` and `0.375 n` and a violation of `0.25 n`.
That rule is not robust on W1, so it settles nothing.

Conclusion: the OPEN line "accelerate-only rules lose monotonicity" is supported by a sketch whose
mechanism is not available for the anytime sandwich the escape names. It is more open than the file
says.

### A3.2 An argument that accelerate-only rules keep monotonicity to `o(n)`

Worse for the converse: here is the reason I now expect the opposite of the report's belief. I state
it as an argument with its gap named, not as a theorem.

Let a rule be *mesh shrinking on an instance* if for every fixed `L` all but `o(n)` of the rounds
are held by leaves of level at least `L`. Every rule for which the report's Lemma 7' bound
`S = sum_l 2^{-l} n_l = o(n)` holds is mesh shrinking, since `sum_{l < L} n_l <= 2^L S`; in
particular COAT is, and so is every accelerate only rule with the sandwich, by the report's own
Section 4.7 item 2. Then, in a leaf at level `l`:

- exploration contributes `O(S) = o(n)` rounds in total, so it cannot carry a linear difference;
- an exploitation round goes to agent 3 exactly when agent 3 is the leaf's ETC winner, an event of
  conditional probability `pi_3(bar m_C, q_l)` given the leaf's cell means;
- along the dyadic filtration `bar m_{a, C_l(u)} -> m_a(u)` for `nu`-almost every `u` and every
  agent `a` (martingale convergence; this is the same fact the report's own Lemma 8 uses in
  `L^1`), and `q_l -> infinity`, so `pi_3 -> 1{m_3(u) > max_{a != 3} m_a(u)}` at almost every `u` at
  which the pointwise argmax is unique.

Hence `E T_3 / n -> nu(m_3 > max_{a != 3} m_a)` up to the mass of the set where the argmax is not
unique, *for both executions*, and the raise replaces `m_1` by `M_1 >= m_1`, which can only shrink
that set. So the timing channel that the accelerate only rule opens is asymptotically invisible:
whatever level the leaf holding round `t` is at, its cell means are close to `m(u_t)` and its winner
is the pointwise winner. The gap in the argument is the tie set `{u : argmax_a m_a(u) is not
unique}`: there `pi_3` does not converge to an indicator, and a fully rigorous proof has to show
that a raise of agent 1 cannot increase agent 3's share on it. I checked the two easy cases (an
exact tie between agents 2 and 3, where agent 3's share is the symmetric fraction at every level and
in both executions; and a tie broken by agent 1's raise, where agent 3 loses) and did not find an
instance where it increases. I did try to build one, using an instance whose cell means alternate
their winner between consecutive levels, and failed for a reason that looks structural: the same
martingale convergence that drives the argument forbids the sign of `bar m_3 - bar m_2` from
alternating at every level on a set of positive mass.

If this is right, then the correct statement of the principle is weaker again than the report's
already weakened pair, namely: *(R1) is needed for exact pathwise monotonicity, and for nothing
else; every property in the `o(n)` sense survives a context-only sandwich.* Exactness is not nothing
(it is what `thm:grid-etc` advertises over `thm:grid-ucb-robust`), but it is a much smaller claim
than "the partition must not depend on the rewards".

There is a second consequence, which I think is the most useful thing in this section. The argument
shows that the monotonicity converse is *parasitic* on the robustness converse: Theorem 3's failure
needs the base execution to keep all `n` rounds at level 0, which is exactly mechanism (B) of
Proposition 7, the mechanism Theorem 4 exploits. So the file has one independent converse
(Theorem 4, freezing at a coarse scale on a reward event) with two visible symptoms, plus a third
witness that turns out not to exercise reward dependence at all (A1.3). That is a smaller claim than
"three witnesses", and it is the claim I would defend.

### A3.3 Escapes I looked for and did not find

- *Reward statistics no single agent can move* (escape 3, recorded as empty). I agree it is empty
  for leaf statistics of the delivered means. I checked one candidate the file does not consider: a
  trigger on the number of *distinct* agents selected in a leaf, which under `ETC(q_l)` exploration
  is deterministic and equal to `K`; that is a context-only trigger in disguise and adds nothing.
- *Reward dependence through a disjoint monitoring subsample.* If split decisions read only rounds
  that are never used for selection, the partition is still a function of rewards, so (R1) still
  fails and the two executions of the coupling still carry different trees. No escape.
- *Randomised split times whose distribution is reward dependent.* Same answer: the realised tree
  differs between the two executions.

## A4. The stated weakest point: the missing modulus for the delivered maps

Section 9.2.1 names as the least secure item the hypothesis that the platform has no known modulus
of continuity for the *delivered* maps, and works out which theorems die if it is removed. I checked
the dependency and the case analysis, and both are right.

*The dependency is real.* `sections/setting.tex` line 59 defines a strategy as a measurable map
`m_{i,n} : \mathcal X -> [0, M_i(x_i)]` with no regularity; `sections/contextual_samf_algorithm.tex`
line 3 imposes Lipschitzness on the *intrinsic* functions only; and the grid widths in the same file
are functions of `n` and `D` alone. So the platform has a modulus for `b` and none for `m_i`. Every
witness in Section 4 except Theorem 5 uses a delivered map that jumps: `m_2, m_3` at `u = 1/2` in
W1, `m_1 = 1 - u` against a threshold that does not shrink with the cell in W3, `m_3` in W4.

*The case analysis is right.* I re-derived the amended rule's behaviour. With every map
`L'`-Lipschitz and `theta_l := 2 L' sqrt(D) 2^{-l}`, a freeze at a level-`l` leaf implies that the
empirical winner's cell mean exceeds every other agent's by more than the largest possible
within-cell variation of any map, hence the winner dominates every other agent *pointwise* on the
leaf. Then:

- Theorem 3 dies, and for a sharper reason than the file gives. It is not only that the instance's
  maps jump. Raising agent 1 does not change `m_2` or `m_3`, so if the base execution freezes a cell
  on agent 2, agent 2 pointwise dominates agent 3 there, hence dominates it in every descendant, so
  the split that the raise induces cannot hand agent 3 a child. The mechanism, not just the
  instance, is unavailable. The same kills Theorem 3'.
- Theorem 4 dies: with `L = 1` and `D = 2` the amended `theta_0` is `2 sqrt 2`, and no rescaling
  rescues it, because rescaling the instance into a level-`l*` cube either raises the instance's own
  Lipschitz constant above `L'` (not allowed) or shrinks its variation below the amended threshold
  at that level (the freeze is then sound). Section 4.6's W4 dies the same way.
- Theorem 5 survives: its maps are constants, and `G_C = 0` at every scale, so no threshold of any
  size separates the tied tops.

*But the surviving witness is the broken one.* Combining this with Section A1.3: under a
smoothness-restricted `S_HDS` with a known constant, the only surviving witness of the converse is
the one that does not exercise reward dependence at all, and whose failure is reproduced by a rule
in the safe class. So the honest statement of the scope is one notch weaker than Section 9.2.1's:

- against the manuscript's actual class `S_HDS`, the converse stands, carried by Theorem 4
  (and by Theorem 3, which A3.2 suggests is a symptom of the same mechanism);
- against a smoothness-restricted class with a known constant, **nothing** in Section 4 separates
  reward-dependent from context-only partitions.

Section 6's last paragraph already tells the paper to keep the converse and any future smoothness
restriction consistent. That instruction should be strengthened to "if such a restriction is ever
added, the converse has no witness left".

I did not attempt the report's conjecture that Theorems 3 and 4 can be rebuilt against a smoothness
class with an *unknown* constant by scaling the instance's Lipschitz constant above whatever the
rule's threshold schedule implicitly assumes. It looks plausible to me for Theorem 4 (the rule's
`theta_l` is a fixed sequence, and an instance with `L` large enough makes the within-cell variation
exceed it at every level the budget reaches), and it is unproved in the file.

## A5. The adaptive tree

### A5.1 The counting argument and the rate: no error found

- Lemma 7(i) to (iv): correct as stated. (iii) uses that distinct level-`l` epochs have disjoint
  visit sets and that a leaf splits only after exactly `N_l` of its own visits, so at most
  `n_l / N_l` of them split; (iv) uses that a dyadic cube can be a leaf at most once because its
  parent splits at most once. Both are right, and (iv) is what makes the bound adaptive.
- Lemma 7': I recomputed every step. `sum_{l<=L} K A 2^{l(2+d)} <= 2 K A 2^{L(2+d)}` needs
  `2^{2+d}/(2^{2+d}-1) <= 2`, true for `d >= 0`. Minimality gives
  `2^{L(3+d)} < 2^{3+d} n/(KA)`, whence `2 K A 2^{L(2+d)} < 2^{3+d}(KA)^{1/(3+d)} n^{(2+d)/(3+d)}`,
  and the tail is at most `(1/2)(KA)^{1/(3+d)} n^{(2+d)/(3+d)}`; `2^{3+d} + 1/2 <= 2^{4+d}`. Correct.
- Theorem D.1: `K q_l e_l <= K 4^l 2^D n_{l-1}/(K 8^{l-1}) = 2^{D+3} 2^{-l} n_{l-1}`, summing to
  `2^{D+2} S`, and the constant `C_0 = 2^{D+4}(2^{D+2} + 2 L sqrt D + c_1 K)` follows. Correct.
- The per-visit exploitation bound `2 L diam(C cap supp nu) + c_1 K q_l^{-1/2}`: I re-derived the
  Lipschitz half independently. For `x_0` in `C cap supp nu` attaining nearly the minimum of `b` on
  the occupied part, and `h*` the honest agent attaining `b(x_0)`, honesty gives
  `m_{h*}(x) >= mu_{h*}(x_{h*}) >= b(x_0) - L diam`, so
  `max_i bar m_{i,C} >= bar b_C - 2 L diam`. This uses honesty of at least one agent and the
  Lipschitzness of the *intrinsic* means only, which is what the model supplies. Correct.
- "Never worse in the exponent": correct, since the covering assumption always holds with
  `d_nu = D`, `A = 1`, and then the exponent is `(D+2)/(D+3)`, the manuscript's own. The claim is
  about the exponent only; `C_0` is exponentially worse than the grid's and the file says so.

### A5.2 Exact pathwise monotonicity of COAT: no error found

This is the property the task singled out, and it holds. The split trigger is `V_C = N_l`, a
function of the context sequence alone, so the coupled executions carry literally the same tree,
with the same leaf creation and split rounds and therefore the same exploration rounds and the same
contexts on them. Inside a leaf, only agent `i`'s exploration empirical mean can rise
(`1{U <= M_i(X)} >= 1{U <= m_{i,n}(X)}` on common pulls, and every other agent's pulls, contexts and
uniforms are unchanged), and the commitment is the argmax with a fixed priority permutation, so the
winner is either the old winner or `i`, never a third agent; agent `j`'s exploration count is
unchanged and its exploitation indicator weakly falls. I checked the tie case explicitly: since only
one score moves, the relative order of the other agents is untouched, so no `j != i` can be promoted.
Pathwise, with remainder zero. This is the one place where (R1) is genuinely indispensable, and the
file is right to say so.

### A5.3 Smaller points on Section 5

- **Theorem D.3, the involution.** The justification given is that "the two agents' seed streams are
  i.i.d. with the *same* Bernoulli parameter and are therefore exchangeable". The realization fixed
  in Section 1.1 has one uniform `U_t` per round, not a seed stream per agent, so there is nothing to
  exchange. The conclusion is unaffected and in fact easier: FATA's hypothesis is
  `m_{i,n} = m_{j,n} = M_*` on `G` *pointwise*, so on a leaf contained in `G` swapping `i` and `j` in
  the permutations leaves every realized reward literally unchanged. P3, wording only.
- **Section 5.6, "COAT's deficit per round falls (0.0185, 0.0327, 0.0095)".** That sequence does not
  fall; it is the sawtooth the file itself describes two paragraphs earlier. P3, wording.
- **The Theorem 3 table (Section 4.1): two rows do not reproduce.** The two RA-ETC rows reproduce
  (A1.1). The row labelled "Static grid, one split" gives 92106.7; a grid with one split (two cells)
  gives 98130 in my runs, and 92130 is what a grid of *eight* cells gives, so the row is a level-3
  grid mislabelled as one split. The "COAT" row gives 79333.5; COAT as defined in Section 5.1
  (`N_l = K 8^l`, `q_l = 4^l`) gives 97628 in my runs, and I could not find parameters that produce
  79333.5. My implementation agrees with the file's on the W3 COAT figures to three decimal places
  (0.06054 against 0.06063, 0.01677 against 0.01676), so the disagreement is unlikely to be my
  simulator. P3 for the argument (the claim the table supports, that both context-only rules give the
  *same* count under both profiles, reproduces exactly), P2 for the record: a table in an audit file
  that a later reader will treat as evidence should be reproducible.

## A6. Citations, checked independently against primary sources

I treated the file's citation claims as claims, as instructed, and re-fetched the sources myself on
18 September 2026.

- **Perchet and Rigollet, arXiv:1110.6084**, "The multi-armed bandit problem with covariates",
  `https://arxiv.org/abs/1110.6084` (checked 18 September 2026): v1 27 October 2011, v2 8 June 2012,
  v3 24 May 2013; the abstract itself says the policy "adaptively decomposes the global problem" and
  "constructs an adaptive partition using a variant of the Successive Elimination (se) policy". So
  the ledger's description of ABSE as a static partition is wrong, and the file's F2 is right.
- The verbatim quotations in Section 7.1 match the full text at
  `https://ar5iv.labs.arxiv.org/html/1110.6084` (checked 18 September 2026): the burst condition is
  `if tau_B >= ell_B and |B| >= 2^{-k_0+1} and |I_B| >= 2`, and the soundness paragraph does read
  "These eliminated arms satisfy `f*(x) > f^{(i)}(x)` for all `x in B` so that such arms are
  uniformly suboptimal on bin `B`", justified by the Holder smoothness condition. The file's three
  reasons why ABSE violates (R1) and (R2) follow from those two quotations and are correct.
- **Slivkins, arXiv:0907.3986**, "Contextual Bandits with Similarity Information",
  `https://arxiv.org/abs/0907.3986` (checked 18 September 2026): v1 23 July 2009, v5 20 May 2014,
  JMLR 15 (2014), full version of a COLT 2011 paper. The selection and activation rules quoted in
  Section 7.2 match the full text at `https://ar5iv.labs.arxiv.org/html/0907.3986` (checked
  18 September 2026), including the activation condition `conf_t(B) <= r(B)`, the new ball centred at
  `(x_t, y)` with `y` the arm just selected, and the index
  `I_t(B) = r(B) + min_{B' in A_t}(I^pre_t(B') + D(B,B'))`, whose minimum over other active balls is
  the file's reason that (R2) fails as well.
- I also confirmed that `audit/round2/B/MATH_CANDIDATE_LEDGER.md` line 121 contains the sentence F2
  quotes, and note that the same line already warns that the check "was assigned to B2 and is not on
  disk ... they must not be cited without verification". F2 closes that.

No citation error found in the file. The one citation error it reports (in the ledger, not in a
canonical file) is real.

## A7. Findings, in severity order

| id | severity | where | finding | repair |
|:-|:-|:-|:-|:-|
| X1 | P1 | REPORT.md Section 0 item 2 third bullet, Section 4.4, Section 6 recommendation 1, Section 8 row for Theorem 5, Proposition 7(A) | Theorem 5 is true but its instance does not exercise reward dependence: on W2 the freeze branch is almost surely never taken, and the rule A0 (dyadic, splits at the `K q_l`-th visit, satisfying (R1) to (R3)) reproduces the `n/4` gain and the `0.175 n` benchmark loss to four decimals at every horizon tested | stop calling it a witness for reward dependence; do not put it in the paper as the converse's instance; use Theorem 4 (in the COAT plus freeze form) and Theorem 3 |
| X2 | P1 | REPORT.md Section 0 item 1 heading; Corollary of Section 4.5; escape 4 of Section 4.7 | (R1) and (R2) and (R3) do not imply "safe" in the sense of Section 1.3; A0 is the counterexample. The proved statement (cell law plus identical coupling partition) is correct and strictly weaker | reword the heading; add "with a schedule whose exploration fraction and mesh are controlled"; add the floor hypothesis `K q_l / D_l -> 0` to the Corollary |
| X3 | P2 | REPORT.md Section 4.7 item 2, Section 8 row "Accelerate-only rules lose monotonicity", Section 9.2.2 item 3 | the sketch's mechanism is unavailable for the anytime sandwich it is offered for (a fixed-level leaf carries `O(1)` visits, not `Theta(n)`), and a martingale-convergence argument points the other way: accelerate-only rules plausibly keep contextual monotonicity with an `o(n)` remainder and lose only exactness | keep the item OPEN but delete the sketch, or replace it with the horizon-dependent rule that is not robust anyway and say so |
| X4 | P2 | REPORT.md Section 9.2.1 | the case analysis is right, but combined with X1 it means that under a smoothness-restricted class with a known constant *no* witness in Section 4 separates reward-dependent from context-only rules, not "only Theorem 5 survives" | state the stronger consequence |
| X5 | P2 | REPORT.md Section 4.1 numerical table | two of four rows do not reproduce: "Static grid, one split" is a level-3 grid (my 92130 against the file's 92106.7; a genuine one-split grid gives 98130), and the COAT row (79333.5) I could not reproduce with the Section 5.1 parameters (I get 97628) | relabel the grid row; recheck the COAT row or drop it |
| X6 | P3 | REPORT.md Section 4.1, instance W1 | under the parenthetical own-context reading of `sections/setting.tex` line 59, `m_2` and `m_3` of W1 are not legal maps, since `x_2 = x_3 = 0` on `supp(nu)` | put `nu` on the diagonal `{(u,...,u)}` as W4 already does; nothing else changes |
| X7 | P3 | REPORT.md Theorem D.3 | the involution is justified by exchanging per-agent seed streams, but Section 1.1 fixes one uniform per round; the conclusion is unaffected and easier (the maps are pointwise equal on `G`) | reword |
| X8 | P3 | REPORT.md Section 5.6 | "COAT's deficit per round falls (0.0185, 0.0327, 0.0095)" is not a falling sequence | reword as the sawtooth it is |
| X9 | P3 | REPORT.md Theorem 4 | understated: the theorem does not need `q_0 -> infinity` (a constant `q_0` gives `(1-delta) c^2 n/2`), and it defeats every schedule with `theta_0 < 1/2` for *any* fixed `c < 1/2 - theta_0`, not only `c = (1/2 - theta_0)/2` | strengthen the statement |

Things I attacked and could not break: Theorem 3 including its horizon-free form; Theorem 4;
Lemma 6 and Proposition 7 as bookkeeping; Lemma 7, Lemma 7' and the balancing of Theorem D.1;
Theorem D.2's exact pathwise monotonicity; the "never worse in the exponent" claim; both citations.

## A8. What would have to be true for the claims I could not break to fail

- **Theorem 3** would fail if the model forbade the instance. Two ways: if `S_HDS` were restricted to
  maps with a known modulus (Section A4, and the file says so), or if the own-context reading of
  `sections/setting.tex` line 59 were the intended one *and* the diagonal repair of X6 were
  unavailable for some reason I did not see. It would also fail if `thm:grid-etc`'s monotonicity were
  not exact, which would make the comparison moot; I did not re-verify `thm:grid-etc` itself.
- **Theorem 4** would fail if the platform had a modulus for the delivered maps (Section A4), or if
  the witness rule were required to have `theta_l` depend on the leaf's own empirical variance in a
  way that adapts to the instance; I did not examine variance-adaptive thresholds at all, and that
  is the first place I would look next.
- **Theorem D.2** would fail only if COAT's split trigger were not a function of the contexts alone,
  for example if a child inherited any part of its parent's visit count or statistics. The file
  flags this and it is right.
- **Lemma 7'** would fail if `e_l` could exceed the covering number, which would need a dyadic cube
  to be a leaf twice.

## A9. What I did not check

- I did not re-verify the manuscript's own theorems (`thm:grid-etc`, `thm:grid-ucb-robust`,
  `thm:contextual-public`, `lem:cell-law`, `lem:etc-tail`, `lem:region`, `lem:cell-average-l1`,
  appendix A.3). I took them as given, exactly as the file does, and checked only that the file uses
  them within their stated hypotheses.
- I did not check Section 2.4 (DE-Grid) beyond reading it, and I did not check the Cesaro argument.
- I did not check Section 5.5 (COAT-UCB) arithmetic; it is an outline in the file and I treated it
  as one.
- I did not check Section 4.6's instance W4 numerically. Its arithmetic I did recompute by hand
  (`bar m_{3,root} = 0.225`, crossing at `u = 0.35/1.8 = 0.19444`, deficit `0.0340 n`) and it is
  correct, but the file itself records that the instance is not simulated.
- I did not check the sharp-adaptivity or FATA claims for RA-ETC (the file does not make any).
- I did not examine variance-adaptive or empirical-Bernstein thresholds, contextual behavioral
  strategy classes, non-i.i.d. contexts, or any lower bound.
- I did not read the worker's scripts, so my reproductions are independent but my non-reproductions
  in X5 are not diagnoses of its code.
