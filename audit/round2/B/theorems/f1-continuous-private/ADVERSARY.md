# F1 adversary report: attack on CG-MESP and on Theorem 1

Worker: the adversary on track F1, 18 September 2026. Output scope: this file and the scratchpad.
No canonical file was modified. No em dash and no triple hyphen appears in this file.

Read in full before starting: `audit/round2/prompts/COMMON.md`;
`audit/round2/B/theorems/f1-continuous-private/TASK.md`;
`audit/round2/B/theorems/f1-continuous-private/EXPLORER.md` (all 1291 lines);
`audit/round2/B/theorems/f1-continuous-private/PROVER2.md` (all 882 lines);
`audit/round2/B/theorems/c2-local-mesp/ADVERSARY.md` Sections 7.1 and 7.2;
`sections/Private_information_setting.tex`; `sections/appendix_private.tex`;
`sections/contextual_samf_algorithm.tex`.

My job was to break Theorem 1, and I did not break it. Under (A1) to (A6) as the two provers
intend them I could not construct a counterexample to any of parts (A), (B), (C), and I could not
find a step that fails. What I did find is a set of defects around the theorem rather than inside
it: one live hypothesis defect that makes the theorem false as literally stated in
`EXPLORER.md` Section 4, a misattribution of what the exogeneity hypothesis is actually carrying
that both provers share, a third instance of the measurability defect that `PROVER2.md` itself
identified and believed it had avoided, and four framing claims that overreach. Section 0 is the
list.

I state plainly where my attacks failed, because a failed attack on a named weak step is evidence.

## 0. Findings, by severity

| # | severity | what | where |
|:-|:-|:-|:-|
| G1 | P1 | **(A3) and (A4) of `EXPLORER.md` Section 4 are lists of pairwise independences, and read literally Theorem 1(A) is false.** Explicit instance with *constant* capacities (`L = 0`, so (A2) is vacuous), i.i.d. arrivals, `K = 2`, in which every displayed clause of (A3) and (A4) holds, joint independence fails, and a deviator gains `tau_C (2 - tau_C)/2` per post-bidding round, which tends to `0.4998 n`. This is `c2-local-mesp/ADVERSARY.md` F2 transplanted; it was repaired there in the finite documents and has been reintroduced verbatim here. `PROVER2.md` Section 2 asserts the five families are "mutually independent by (A3) and (A4)", which does not follow. One word repairs it and no rate changes. | Section 3 |
| G2 | P2 | **Both provers name the same least secure step, and the finite-case adversary had already shown, on 18 September, that that step is secure and that the stated reason for its insecurity is wrong.** `F_{s-1}`-measurability of the Stage-2 indicator is a bookkeeping artefact of writing the Chernoff step at `F_{s-1}` rather than at the pre-seed field; the half-step repair of `c2-local-mesp/ADVERSARY.md` Section 2 transfers to the cube monitor verbatim and uses no property of the arrival path. So the two loads **do** separate: exogeneity is indispensable for the coupling and is a convenience in the monitor. Neither prover cites that section, although both cite Section 7.1 of the same file. This is a correlated error inherited from a shared upstream document and it is the clearest evidence I have that the agreement of the two proofs is not independent evidence. | Section 4 |
| G3 | P2 | A **third** load on exogeneity that neither prover names and neither the explorer's Lemma 7 nor `PROVER2.md`'s Lemma P7 can carry without it: the fallback length `H_C^fb` is treated as known at the cube's fallback start, which is true only because `A` is in `F_0`. `c2-local-mesp/ADVERSARY.md` Section 2 item 2 identifies the finite analogue and says it is repairable by optional stopping; I did not write the repair and neither did anyone else. | Section 4.3 |
| G4 | P2 | **(A5) presupposes (A3): it is not a second, independent relaxation.** A strategy that conditions on the entire arrival path is not well defined when the path reacts to rewards, because the path at round `t+1` is then a function of a reward the agent has not yet produced. So "arbitrary nonanticipating deviations including conditioning on the whole path" and "arrivals need not be i.i.d." cannot be advertised as two separate strengthenings; the first buys the second's hypothesis. Under the smaller class `B^ctx` (past path only) the model is well posed and the theorem is then **false**, by the transplant of `c2-local-mesp/ADVERSARY.md` F1. | Section 4.4 |
| G5 | P3 | **The measurability defect `PROVER2.md` calls D2 recurs in `PROVER2.md`'s own proof.** Section 6 asserts that `E^*_C` and `H^*_C`, the good events of the *baseline* execution at cube `C`, are measurable with respect to the *deviating* execution's fallback start field at `C`. They are not: in Case 2 the baseline never switches at `C` and its monitor event depends on rewards at rounds after the deviating execution has already switched. Repairable in three lines at `O(n^{-2})` cost, exactly as D2 is. | Section 7.2 |
| G6 | P2 | **(A2) is load bearing and its failure is catastrophic, not graceful.** Explicit `K = 4`, `d = 1` instance, outside (A2), on which part (B) fails by `n/4` against a bound of `O(n^{6/7} log n)` (and by `3n/4` in the degenerate regime `sigma_n >= 1/2`). So "uniform over instances" must be read as "uniform over the `L`-Lipschitz instances with `log(en) >= 3L`", and the class covered at a given `n` is genuinely smaller than "all Lipschitz instances". `PROVER2.md` Section 10.4 states the qualification; no one exhibits the failure. | Section 6.3 |
| G7 | P3 | **`EXPLORER.md` Sections 0.3 and 7.4 and `PROVER2.md` Section 10.1 describe a manuscript that no longer exists.** The non-top branch, the `delta_i` constants and the caveat sentence were removed from `sections/appendix_private.tex` by commit `2e2a54f` (18 September 2026, 19:21 UTC), after `PROVER2.md` was committed at `3e3a180` (19:16 UTC). The quoted sentence "No concentration around the deviator's capacity is invoked" is at line 99 of the file at tag `baseline-2026-09-17` and is not in the file on the branch. Nothing is wrong with either argument; the by-product is already banked and must not be applied twice. | Section 8.1 |
| G8 | P2 | **Four framing claims overreach**, in the same shape as the item `PROVER2.md` Section 15 item 2 already flags. (i) "at the exponent of the existing public contextual result" is true of `thm:grid-etc` and `thm:contextual-public` but not of the manuscript's better public contextual rate `n^{(D+1)/(D+2)}` (`sections/contextual_samf_algorithm.tex` line 10), which is strictly smaller. (ii) The public theorem's revenue benchmark is `M_star`, the private one's is `M_(2)`: same exponent, strictly weaker benchmark. (iii) "no instance constant" is now shared with the scalar theorem, which acquired the same property at `2e2a54f`, so it separates Theorem 1 from the C2 candidates, not from the paper. (iv) For an agent that is never a winner the additive guarantee permits a gain of the same order as its entire baseline utility, so part (A) is informative only for agents whose baseline payoff is `Theta(n)`. | Section 8 |

**Verdict: not broken.** Under (A3) and (A4) read with mutual independence, and under (A2), I could
not construct a deviation, an instance or an arrival path that beats any of the three bounds, and I
could not find a false step in either proof. Every attack I was asked to run is reported below with
its outcome, including the ones that failed.

**SECOND PASS, added after the revision of `PROVER2.md` to 1353 lines.** Sections 14 to 16 at the
end of this file adjudicate G1 to G8 against the repairs and attack the four new objects. One new
finding:

| # | severity | what | where |
|:-|:-|:-|:-|
| H1 | P1 | **The new hypothesis (A4c) omits the mechanism's own randomisation, and Theorem 1C upgraded is false as stated.** Lemma P7c's proof uses "the selection coin is fresh given `G_u^{--}`", which (A4c) does not supply: (A4c) constrains the seed only, and Section 17.0 supplies an ordering of a filtration rather than a freshness statement. Explicit `K = 2` instance with constant capacities on which every clause of (A4c) holds, the arrival path is a function of the fallback selection coin, the honest comparator is never selected at one cube, Lemma P7c is false and part (C) upgraded fails by `0.45 n` against an `O(n^{4/5} log n)` budget. This is G1's defect recurring inside the repair of G1, and it is the third time on this project. One clause repairs it. **Part (B) upgraded is unaffected and really does hold under (A4c) alone.** | Section 15.1 |

G1 is closed for parts (A) and (B) and reopened for part (C); G2 to G8 are closed. The coordinator's
summary that "G8 is withdrawn" is the wrong way round: G8 was upheld and what Section 19 withdraws
are the author's own framing claims (Section 14.8).

**THIRD PASS, on revision 3 (1540 lines). Sections 17 to 22 at the end of this file. Verdict:
minor items only.** (A4f) is sufficient for CG-MESP as written; I attacked it with seven variants
of H1 and could not break it. The tower step replacing the assertion H1 broke is correct and
complete. The lemma-by-lemma attribution table is correct, with one over-attribution in the safe
direction. Nothing changed a statement, a bound or a rate, with one exception I found and repaired
in three lines: the substitution of `min{J_n, n}` for `J'_n` in the upgraded parts (B) and (C)
silently costs the path-adaptivity of the error terms, and Jensen restores it with `E[J'_n]`
(Section 20 item 3). Seven P3 items in total.

## 1. What I read, what I checked line by line, and what I did not

**Read in full:** `EXPLORER.md` Sections 0, 1, 3, 4, 5, 6, 7, 10, 11 and the headings of 2, 8, 9;
`PROVER2.md` in full; `c2-local-mesp/ADVERSARY.md` Sections 0, 2, 5.3, 6.1, 7.1, 7.2;
`sections/Private_information_setting.tex` in full; `sections/appendix_private.tex` lines 80 to 150;
`sections/contextual_samf_algorithm.tex` in full.

**Checked line by line, against both proofs:** Fact 0 and the oscillation arithmetic; Fact 1 and
Fact 2 (Lemma 2); the bidding concentration in both forms (Lemma 3 and Lemma P1), including the
index set, the conditioning field and the two union bounds; bid domination and winner inclusion
(Lemma 4 and (6.1)), including the tie break; the price lemma (Lemma 5 and Lemma P2) and its two
consequences; the comparator lemma (C3 and Lemma P3); Lemma 8 and Lemma P4; Lemma 9 and Lemma P5;
the monitor (Lemma 6 and Lemma P6) parts (a) to (e), including the Azuma exponent, the stopping
time, the union count and the failing pull case; the fallback (Lemma 7, Lemma P7) and the
deviator's share (Lemma 7b, Lemma P8) including the replacement of `Qbar_i` by `H`; the case
analysis of part (A) in both proofs; part (B) in both; part (C) in both; every Cauchy and Schwarz
step; and the whole of part (D).

**Checked against the canonical files:** that the mechanism's Stage-1 schedule is reward
independent as claimed; the exponents of `thm:grid-etc`, `thm:contextual-public` and the Grid-UCB
rate; the benchmark of each; and the current state of the scalar private theorem and its appendix.

**Not checked:** `EXPLORER.md` Section 2 (identifiability), Section 8 (PA-MESP), Section 9, and
the numerical work of Section 10. `PROVER2.md` Section 11's simulation code. Anything about
anytime horizons or non-Lipschitz capacities beyond Section 6.3 below. I did not re-derive the
EXP3 potential inequality or the constant `3(2 + sqrt 2)`; `separation/REPORT.md` and
`c2-local-mesp/ADVERSARY.md` Section 9.1 both cover it and I took that as settled.

**Compute:** five short login node scripts in
`<scratchpad>/round2/f1-adversary/` (`g1_check.py`, `g1b_check.py`, `osc.py`, `exponents.py`,
`cross.py`), seconds each, no Slurm job. There is nothing to add to a compute log. None of them
simulates the mechanism; they verify arithmetic identities and independence properties.

## 2. The attack plan and the outcome of each attack

| attack | outcome |
|:-|:-|
| Transplant the finite reward-reactive arrival counterexample to the continuum | **Works**, `Theta(n)`, but not worse in order than the finite case. Section 4.4 |
| Separate the two loads exogeneity carries | **Succeeded, and the separation is a correction to both proofs.** Section 4 |
| Transplant the pairwise independence counterexample | **Works and is live here**, with a stronger instance than the finite one. Section 3 |
| Arrival path that starves every cube just below the bidding threshold | Fails. Section 5.1 |
| Arrival path that concentrates in one cube | Fails. Section 5.1 |
| Arrival path correlated with the mechanism's phase boundaries | Fails, and I give the reason it cannot work. Section 5.2 |
| Arrival path that steers an agent's own Stage-1 pulls to its favourable contexts | Fails, by construction of the shading. Section 5.3 |
| Break the one sided bid bound: nondeterministic index set | Fails. Section 6.1 |
| Break the one sided bid bound: an agent that conditions on the whole future path | Fails under (A3), and is not well posed without it. Section 6.1, Section 4.4 |
| Find a downstream step that secretly needs a two sided bid bound | Fails; I enumerate every use of a bid in either direction. Section 6.2 |
| Find a use of the oscillation allowance that compounds | Fails; I enumerate all seven uses. Section 6.3 |
| Find a configuration where the allowance is too small | Succeeds only outside (A2), and then part (B) fails by `n/4`. Section 6.3 |
| Sweep both proofs for more random-index-set union bounds | No second instance beyond D1 in either proof; one related misstatement in `EXPLORER.md` Lemma 7. Section 7.1 |
| Sweep both proofs for more global-event-inside-a-conditional-expectation errors | One found, in `PROVER2.md`'s own proof. Section 7.2 |
| Find framing overreach of the shape `PROVER2.md` Section 15 item 2 identifies | Four found. Section 8 |

## 3. G1: the hypotheses as written are pairwise independence, and Theorem 1(A) is then false

This is `c2-local-mesp/ADVERSARY.md` finding F2, transplanted. That report repaired it in the two
finite documents by one word. `EXPLORER.md` Section 4 reintroduces the defective form, and
`PROVER2.md` inherits it, so the repair has to be made again. I give a **stronger** instance than
the finite one, because on a continuum the leakage channel can be made exact rather than one bit.

### 3.1 The hypotheses as written

`EXPLORER.md` Section 4:

> **(A3)** The arrival path `A := (X_1,...,X_n)` in `[0,1)^D` is independent of the reward-seed
> array, of every mechanism coin and of every agent's private coin array.
>
> **(A4)** `(U_t)_{t <= n}` are i.i.d. uniform on `[0,1]`, independent of `A`, of the mechanism
> coins and of the agents' private coins.

Each is a list of separate independence statements. `EXPLORER.md` Section 5.0 then says the
objects are "all mutually independent by (A3), (A4) and the construction", and `PROVER2.md`
Section 2 says they are "mutually independent by (A3) and (A4)". Neither implication is valid:
pairwise independence of three families does not give joint independence, and the two documents
use joint independence in every martingale step.

### 3.2 The instance

`K = 2`, `d = 1`, `D = 2`. Agent `1` is strategic, agent `2` is honest, and `K_H = {2}`.

```
 M_1 == 1 ,      mu_1 == 0        (agent 1, strategic)
 M_2 == 0.98 ,   mu_2 == 0.98     (agent 2, honest)
```

Both capacity functions and both intrinsic means are **constant**, hence `L`-Lipschitz with
`L = 0`, so (A2) reduces to `n >= 2K` and imposes nothing. Agent `1` is top at every profile, so no
top-set condition, no capacity gap and no boundary condition is at issue. Arrivals
`X_t = (x_{1,t}, x_{2,t})` are **i.i.d. uniform on `[0,1)^2`**, so the instance also satisfies the
stronger i.i.d. hypothesis that the manuscript's contextual theorems use; the "no i.i.d." claim is
not what is being attacked.

**The seeds.** Let `(c_t)_{t <= n}` be agent `1`'s private coin array, i.i.d. uniform on `[0,1)`,
independent of `A`. Define

    U_t  :=  frac( x_{1,t} + c_t ) .

Then:

* `(U_t)` is i.i.d. uniform on `[0,1)`, because `c_t` is uniform and independent of `x_{1,t}`;
* `(U_t)` is independent of `A`, because conditionally on `A` each `frac(x_{1,t} + c_t)` is uniform;
* `(U_t)` is independent of the private coin arrays, because conditionally on `c` each
  `frac(x_{1,t} + c_t)` is uniform;
* `A` is independent of the private coin arrays, by construction;
* the only mechanism coins are the priorities `Pi_C` and the EXP3 coins, which may be taken
  independent of everything.

So **every clause of (A3) and of (A4) as displayed holds exactly.** What fails is the joint
statement: `U_t` is a deterministic function of the pair `(x_{1,t}, c_t)`, both of which agent `1`
knows.

### 3.3 The deviation and the arithmetic

Agent `1` knows its own coordinate `x_{1,t}` at the round at which it is selected, since its own
feasible set `[0, M_1(x_{1,t})]` is defined by it and since (A5) lets it condition on the arrival
path; and it knows `c_t` by (A5). It therefore knows `U_t` exactly before choosing its target, and
the timing of (A4) is respected: the target is chosen first and only then is
`Y_t = 1{U_t <= m_{1,t}}` realised.

*Stage 1, at every cube.* Deliver `m_{1,t} := U_t`. Then `Y_t = 1` at every Stage-1 pull, so
`beta_{1,C} = 1` at every cube, the same bid as under `S^*`, which delivers `M_1 = 1` and also
always succeeds. Mean effort is `E[U] = 1/2` per pull instead of `1`, a saving of `e_bid / 2` in
total, which is inside the allowance and is not where the violation comes from.

*Stage 2.* Agent `1` bids `1` and agent `2` bids `0.98 +- s_n`, so agent `1` wins every cube and the
announced price is `tau_C = (beta_{2,C} - sigma_n)_+`, the same number as under `S^*` because it is
formed from the other agent's bid alone. Deliver

    m_{1,t}  :=  U_t   if  U_t <= tau_C ,      m_{1,t} := 0   otherwise .

Then `Y_t = 1{U_t <= tau_C}` exactly, a Bernoulli`(tau_C)` variable, so the realised reward sequence
has **the same law as the baseline's**: `Z_r - r tau_C` is the same mean zero bounded martingale as
under `S^*`, the monitor fires with the same probability, and on `H_C` no switch occurs. The effort
is `E[ U 1{U <= tau_C} ] = tau_C^2 / 2` per pull instead of `tau_C`.

*Gain.* Per Stage-2 pull the utility is `1 + mu_1 - tau_C^2/2` against the baseline's
`1 + mu_1 - tau_C`, a gain of

    tau_C - tau_C^2/2  =  tau_C ( 2 - tau_C ) / 2  >  0    for every  tau_C > 0 ,

over `n - e_stage1 = n (1 - o(1))` pulls. Verified at `2 x 10^6` draws in
`<scratchpad>/round2/f1-adversary/g1b_check.py`, which reproduces the mean reward, the mean effort
and the gain to five digits and confirms the pairwise independences:

| `tau_C` | mean reward delivered | mean effort | predicted `tau^2/2` | gain per pull | predicted |
|:-|:-|:-|:-|:-|:-|
| 0.05 | 0.04988 | 0.00124 | 0.00125 | 0.04876 | 0.04875 |
| 0.15 | 0.15002 | 0.01126 | 0.01125 | 0.13874 | 0.13875 |
| 0.50 | 0.50017 | 0.12501 | 0.12500 | 0.37499 | 0.37500 |
| 0.98 | 0.98017 | 0.48019 | 0.48020 | 0.49981 | 0.49980 |

Since `L = 0` gives `omega = 0` and `sigma_n = 3 s_n + rho_n` with
`rho_n = sqrt 2 h_n log(en) = O(n^{-1/5} log n)` and `s_n = O(n^{-1/5} sqrt(log n))`, one has
`tau_C -> 0.98` and the total gain tends to `0.98 . 1.02 / 2 . n = 0.4998 n`, against a bound
`O(n^{4/5} log n)`. The gain is positive at every horizon at which the mechanism is not degenerate,
that is at every `n` with `sigma_n < 0.98`; below that `tau_C = 0`, the mechanism prices at zero,
and both the theorem and the counterexample say nothing. The counterexample is therefore asymptotic
in exactly the same sense the theorem is, and the ratio of the gain to the bound grows like
`n^{1/5} / log n`.

### 3.4 What this refutes and what it does not

It does **not** refute the mathematics. Both proofs use joint independence at the one place it
matters, in the conditional Hoeffding step
`E[ e^{lambda (Y_t - m)} | F_{t-1} v sigma(I_t, coins) ] <= e^{lambda^2/8}`, which is exactly the
statement my instance violates: conditionally on the deviator's coin and the current context, `U_t`
is a point mass. The proofs are correct under mutual independence.

It refutes the hypothesis list. The repair is one word in each place, and no bound, statement or
rate changes:

> **(A4)** `(U_t)_{t <= n}` is an i.i.d. uniform `[0,1]` array, and the four families `A`,
> `(U_t)`, the mechanism coins `(Pi_C)` together with the EXP3 coins, and the agents' private coin
> arrays are **mutually** independent.

with (A3) then redundant. The manuscript's own scalar phrasing at
`sections/Private_information_setting.tex`, "Assume targets are chosen before fresh conditionally
independent Bernoulli seeds", is the correct strong condition and should be the model for the
contextual statement. I record, as `c2-local-mesp/ADVERSARY.md` did, that the contextual documents
are weaker than the source they localise, not stronger.

**Why the continuum version is stronger than the finite one.** The finite instance leaks one bit of
the seed per round (`c2-local-mesp/ADVERSARY.md` Section 7.2, gain measured at `0.11 n`) and the
gain is positive only when the price exceeds `1/2`. Here the context coordinate is a continuum, so
`frac(x_{0,t} + c_t)` leaks the seed **exactly** while remaining exactly pairwise independent of
both its arguments, and the gain `tau(2 - tau)/2` is positive at every positive price. This is the
one place where I found the continuum strictly worse than the finite case, and it is a defect of
the hypothesis rather than of the mechanism.

## 4. Exogeneity: the two loads separate, and only one of them is real

Both provers name the same least secure step. `EXPLORER.md` Section 11 item 2: "Lemma 6's
`F_{s-1}`-measurability of the Stage-2 indicator, which holds only under Convention F-A".
`PROVER2.md` Section 14: "the `F_0`-measurability of the arrival path (Convention A), on which two
different things depend at once. It is what makes `psi_s` predictable in Lemma P6 ... and it is
what makes the Stage-1 rounds identical across the two coupled executions in Fact 1."

I was asked to decide whether the two loads can be separated. **They can, and the finite-case
adversary had already separated them on 18 September** (`c2-local-mesp/ADVERSARY.md` Section 2,
finding F3). Neither `EXPLORER.md` nor `PROVER2.md` cites that section, although both cite Section
7.1 of the same file for the counterexample. I re-derived the separation for the cube monitor
rather than taking it on trust.

### 4.1 Load one, the monitor, does not need exogeneity (G2)

Let `(F_t)` be the natural global filtration in which `X_t` is revealed at round `t`, and let

    F_t^-  :=  sigma( F_{t-1}, X_t, I_t, m_{I_t,t} )

be the pre-seed field, which both documents already use implicitly when they say "the target is
chosen after selection and before the seed". Fix a cube `C` and an `r`, let `T_r` be the round of
the `r`-th Stage-2 pull at `C` (with `T_r := n` if fewer than `r` occur), put
`phi_s := psi_s 1{s <= T_r}`, `M_t := sum_{s <= t} phi_s ( Y_s - m_{I_s,s} )`,
`c_t := sum_{s <= t} phi_s`, and

    N_t  :=  exp( lambda M_t  -  (lambda^2/8) c_t ) ,   N_0 = 1 .

`phi_s` is `F_s^-`-measurable: it depends on `X_s`, which `F_s^-` contains, and on whether `C` has
awarded and not yet switched, which is a function of rewards at rounds strictly before `s`. `T_r`
is a stopping time for `(F_s^-)`. `N_{t-1}` is `F_{t-1}`-measurable, hence `F_t^-`-measurable.
Hoeffding's lemma applied conditionally on `F_t^-`, which is the exact content of (A4)'s timing
clause, gives

    E[ N_t | F_t^- ]  =  N_{t-1} e^{-(lambda^2/8) phi_t} E[ e^{lambda phi_t ( Y_t - m_{I_t,t} )} | F_t^- ]
                      <=  N_{t-1} ,

so `E[N_t] <= 1` for every `t`. Since `c_{T_r} = r` and `M_{T_r} = Z_r - A_r`, the Chernoff step
optimised at `lambda = 4 b_n(r)/r` gives `Pr( |Z_r - A_r| > b_n(r) ) <= 2 exp(-2 b_n(r)^2/r)
= 2 e^{-ell_n}`, which is precisely the bound both Lemma 6(a) and Lemma P6(a) need.

**Nothing in this asks `psi_s` to be `F_{s-1}`-measurable, and nothing in it uses a property of the
arrival path.** Parts (b), (c) and (d) of both monitor lemmas are pathwise consequences of the
event and are untouched. Part (e) is optional stopping for `M` at the bounded time `n` and needs
only the same conditional mean zero property.

**What is left of the arrival hypothesis in the monitor is a constant.** Under Convention A the
union bound runs over the `F_0`-measurable set of visited cubes; without it one unions over all
`J_n` grid cubes, which is a deterministic set of size at most `2^D n^{D/(D+3)}`, so the failure
probability becomes at most `2 J_n n e^{-ell_n} = 2^D n^{D/(D+3) - 4} / K`, which is still
`o(n^{-3})`. The `n` factor `PROVER2.md` corrects in D1 and the `J_n` factor here
are of the same kind and both are absorbed by `ell_n := log(2 K n^6)`.

**Consequence for the paper.** The sentence that must be written is not "exogeneity is what makes
the monitor a martingale test". It is: *exogeneity is indispensable in the coupling of part (A)
and is a bookkeeping convenience everywhere else.* Both provers have it the other way round, or at
best rank it wrongly, and they do so identically.

### 4.2 Load two, the coupling, is real and is not repairable

The step that genuinely needs (A3) is (6.1) of `PROVER2.md`, equivalently Lemma 4(a) and (c) of
`EXPLORER.md`. The two coupled executions are required to have the same Stage-1 rounds at every
cube and to pull the same agent at each. If the arrival path may react to a realised reward, the
paths of the two executions separate at the first round at which agent `i`'s target differs from
its capacity and the seed falls between them, after which the two executions visit different cubes
at different rounds, agent `i` receives a different number of Stage-1 pulls at a cube in the two
executions, and there is nothing to compare. No half step of a filtration repairs this, because it
is not a measurability statement but an identity of two random schedules.

### 4.3 Load three, which neither prover names (G3)

`EXPLORER.md` Lemma 7 says `H_C` is "an `F_0`-measurable integer under Convention F-A, since the
switch round is a stopping time and the remaining visits are determined by `A`". `PROVER2.md`
Lemma P7 says `H_C^fb` is "an `F_0`-measurable integer given the switch round". The corrected
reading is `PROVER2.md`'s: `H_C^fb` is measurable with respect to the fallback start field, which
is what the conditional statement needs, **and it is so only because `A` is in `F_0`**. Without
exogeneity the number of remaining visits to `C` is not known at the switch round; it depends on
future rewards, including the fallback rewards the lemma is about, so the EXP3 guarantee is being
applied at a horizon that the algorithm's own outcomes help determine.

This is a third load, distinct from the monitor and from the coupling, and it sits in parts (B) and
(C) as well as (A). `c2-local-mesp/ADVERSARY.md` Section 2 item 2 identifies the finite analogue
and says it is repairable in principle, by optional stopping at the bounded local fallback clock,
because the importance weighted estimates are bounded by `1/eta_k`. I did not write that repair for
the doubling epoch version, where the tuning constant itself changes with the epoch containing the
stopping time, and neither did anyone else on this track. Until it is written, the honest statement
is that all three parts of Theorem 1 use exogeneity, not only part (A).

### 4.4 The reward-reactive counterexample transplants, and (A5) presupposes (A3) (G4)

**The transplant works.** Take `K = 2`, `d = 1`, `D = 2`. Agent `1` is strategic with `M_1 == 1`,
`mu_1 == 0`; agent `2` is honest with `M_2 = mu_2 = x`, the identity on `[0,1)`, which is
`1`-Lipschitz, so (A1) holds and (A2) holds for `n >= e^3`. The indexing matters: the mechanism's
Stage-1 schedule pulls agent `((V_C - 1) mod K) + 1`, so the **first** visit to a cube pulls agent
`1`, the deviator, and `Y_1` is a reward the deviator produces.

Let the arrival path set `X_1 = (0,0)` and then, for every `t >= 2`,
`X_t = (0,0)` if `Y_1 = 0` and `X_t = (1 - h_n/2, 1 - h_n/2)` if `Y_1 = 1`. This is a measurable
function of one realised reward: deterministic given that single bit, not i.i.d., and satisfying
every clause of (A3) except independence from the seeds.

Under `S^*` agent `1` delivers `M_1 = 1` at round `1`, so `Y_1 = 1` and the whole remaining horizon
sits in the top corner cube, where agent `2`'s capacity is `1 - h_n/2`, so `beta_2 = 1 - h_n/2 +-
s_n`, `tau = (1 - h_n/2 - s_n - sigma_n)_+` and agent `1`'s per pull utility is
`1 + 0 - tau = sigma_n + s_n + h_n/2`. Under the deviation "deliver `0` at the first Stage-1 pull,
then follow `S^*`", `Y_1 = 0` and the whole remaining horizon sits in the origin cube, where
`M_2 = 0` at the arriving coordinate, so `beta_2 = 0`, `tau = 0`, the switch test
`Z_r < 0 - b_n(r)` can never fire, and agent `1` delivers `0` at a per pull utility of `1` for every
post-bidding round. The gain is `(1 - sigma_n - s_n - h_n/2)(n - 2 K L_n) - 1 = Theta(n)` for every
`n` with `sigma_n < 1`, against a bound `O(n^{4/5} log n)`. The construction is asymptotic in the
same sense as the theorem: below the horizon at which `sigma_n < 1` the mechanism prices at zero
everywhere and neither the theorem nor the counterexample says anything.

This is `c2-local-mesp/ADVERSARY.md` Section 7.1 with a continuous context in place of two discrete
ones, and it fails through exactly the channel that report identifies: the two coupled executions
receive different Stage-1 schedules. `EXPLORER.md` Section 7.5 item 6 anticipates it in one
sentence and `PROVER2.md` Section 14 does the same; both are right that it applies.

**It is not worse in order here.** The finite instance exceeds the bound by a factor growing like
`n^{1/3} (log n)^{-1/3}`; here the bound is larger, so the factor is only `n^{1/(D+3)}/ log n`.
Against a request to find whether the continuum makes it worse, the answer is no: the damage is
`Theta(n)` in both, and the continuum's larger error budget absorbs slightly more of it.

**But there is a structural point neither prover makes, and it bears on the headline.** (A5) lets
the deviator condition on "the entire arrival path". If the path reacts to rewards, that
conditioning variable is **not well defined**: `X_{t+1}` is then a function of `Y_t`, `Y_t` is
`1{U_t <= m_{i,t}}`, and `m_{i,t}` is by (A5) a function of `X_{t+1}`. The recursion has no
solution in general and the probability space of Section 5.0 cannot be built. So the two
relaxations the framing advertises as separate, "arbitrary nonanticipating behavioural deviations
including conditioning on the whole path" and "arrivals need not be i.i.d.", are not independent:
the first is definable only when arrivals are exogenous. Under the smaller class `B^ctx` of the
contract, in which the agent sees the path only up to the current round, the model with reactive
arrivals is well posed, and then the counterexample above applies and the theorem is false. Either
way (A3) cannot be weakened, and the paper should not present the two as separate strengthenings.

**`PROVER2.md` D6 is necessary but not sufficient.** D6 asks (A3) to say that the law of the
arrival path does not depend on the strategy profile. That is needed for the equilibrium comparison
to integrate the same law twice, and it is correct, but it does not by itself deliver the pathwise
identity of the two Stage-1 schedules, which is what the coupling uses. Both clauses are required.

## 5. Adversarial arrival paths: four attacks, all failed, and the reason they cannot work

All of this section assumes (A3), so the path is chosen in advance without access to the seeds, but
is otherwise arbitrary and is known to the deviator.

**The structural reason none of these works, stated first.** Every parameter the mechanism uses is
either a constant fixed before play (`g_n`, `h_n`, `L_n`, `ell_n`, `s_n`, `rho_n`, `sigma_n`) or a
function of a **per cube counter** (`V_C`, `r_C`, the local fallback clock). The mechanism reads the
global round index nowhere. Consequently every bound in either proof is a function of the vector
`(n_C)_C` and of `J'_n` alone, and the only freedom a path has is to choose that vector subject to
`sum_C n_C <= n` and `J'_n <= min{J_n, n}`. The optimisations below are therefore finite dimensional
and I could solve them.

### 5.1 Starvation and concentration (the two `PROVER2.md` checked)

*Starvation.* Give every cube `K L_n - 1` visits, so no cube ever awards. Then every round is a
Stage-1 pull, `n_C = 0` for every `C`, and the mechanism elicits and never prices. The total number
of rounds a path can spend this way is `J_n (K L_n - 1) <= K 2^{D+1} n^{(D+2)/(D+3)}`, which is
exactly `e_stage1` and is `o(n)`, so at least `n (1 - o(1))` rounds are spent at cubes that do
award. The fixed grid is what caps the damage, and this is the one place where a *static* grid is
strictly better than a data dependent partition. Confirmed; `PROVER2.md` Section 10.2 has it.

*Concentration.* Put every round in one cube. Then `J'_n = 1`, `e_bid = L_n`,
`e_mon = 1 + 2 sqrt(n ell_n/2)`, `e_fb = 11 sqrt(2 K n log K) + 2 K log K log_2(2(n+1))`, and
`e_osc = n rho_n` is unchanged. All three bounds degrade to the scalar MESP rates plus the
oscillation term. Confirmed.

### 5.2 A path correlated with the mechanism's own phase boundaries (the attack I was asked to run)

I tried five versions and all fail.

1. *Award every cube as late as possible.* Visit each cube once every `n / (K L_n)` rounds so that
   its `K L_n`-th visit falls at the horizon and `n_C = 0`. This wastes `K J'_n L_n <= e_stage1`
   rounds and nothing else; the accounting already charges exactly that.
2. *Award every cube as early as possible and then never return.* Give each cube exactly `K L_n`
   visits and move on. Same bound, same conclusion, and the deviator's Stage-1 harvest is then at
   its maximum `J_n L_n = e_bid`, which is the term the mechanism concedes.
3. *Award every cube and then give it exactly one post-bidding visit.* This maximises the number of
   cubes that reach Stage 2 with `n_C = 1`, which is the configuration that charges the `+1` of
   Lemma P6(b) as many times as possible. The total is `J'_n <= 2^D n^{D/(D+3)}`, which is exactly
   the first term of `e_mon`. So that additive `J'_n` is not slack; it is the value of this attack.
4. *Maximise the monitor slack.* The deviator's Stage-2 exploitation at a cube is bounded by
   `2 b_n(n_C)`, and `sum_C b_n(n_C) = sqrt(ell_n/2) sum_C sqrt(n_C)` subject to
   `sum_C n_C <= n` and at most `J'_n` nonzero terms is maximised at `n_C = n / J'_n`, giving
   `sqrt(J'_n n ell_n / 2)`, and then over `J'_n <= J_n` at `J'_n = J_n`. **So the path that spreads
   the horizon uniformly over all `J_n` cubes makes `e_mon` exactly tight**, and `e_mon` is
   `Theta(n^{(2D+3)/(2D+6)} sqrt(log n))`, strictly below `n^{(D+2)/(D+3)}`. The attack succeeds in
   making the term attained and fails to make it dominant. The same calculation makes `e_fb` tight,
   with the same conclusion.
5. *Correlate the award time of one cube with the switch time of another.* Impossible to exploit,
   because by Fact 2 no cube's state is a function of another cube's data, and because the
   mechanism never reads the global clock. I looked for a channel and there is none: the only
   cross-cube objects are the agents' own behaviours, and every per cube bound is uniform over what
   a deviator conditions on.

### 5.3 A path that steers an agent's Stage-1 pulls to its favourable contexts

Since the Stage-1 schedule is a deterministic function of `A`, a path may place agent `i`'s `L_n`
Stage-1 pulls at cube `C` at the corner of `C` where `M_i` is largest and place agent `j`'s at the
corner where `M_j` is smallest. The effect is exactly `Mbar_{i,C} - Mbar_{j,C}` shifted by at most
`2 omega`, so a path can install a wrong ranking inside a cube whenever the two capacities differ
by less than `2 omega`.

**This is already the worst case of both proofs and costs nothing extra.** Lemma P2's chain uses
`Mbar_{W,C} <= M_W(x_W) + omega` for **every** `X in C`, and Lemma P4's uses
`Mbar_{j,C} >= M_j(x_j) - omega` for **every** `j` and every `X in C`. Neither is a statement about
a typical context, so an adversarial placement of the Stage-1 contexts inside the cube changes
nothing. The price of covering this is precisely the `rho_n` in `sigma_n`, and it is the design
point that makes the mechanism path robust. I tried to find a quantity that is compared at a
*representative* context rather than uniformly over the cube, and found none.

### 5.4 Paths I invented and what happened

* *A path that visits `n` distinct cubes once each*, so that the mechanism only ever elicits and
  never prices. Impossible: `J_n = g_n^D <= 2^D n^{D/(D+3)} < n` for `n` beyond a fixed threshold,
  so the grid forces revisits. This is what keeps `e_bid = min{J'_n L_n, n}` strictly below `n`, so
  part (A) is never vacuous. `c2-local-mesp/ADVERSARY.md` F7 records that the finite candidate's
  `e_bid = Q L_n` had no such cap; the continuous mechanism does, from the grid rather than from the
  `min`.
* *A path whose cube visit counts are heavy tailed*, `n_C` proportional to `C`'s index. Strictly
  worse for the adversary than the uniform path, by the concavity in 5.2 item 4.
* *A path that abandons a cube in the middle of its Stage-2*, so that the monitor never resolves.
  Harmless: Lemma P6(e) is optional stopping at the bounded time `n` and needs no knowledge of why
  the phase ended, and Lemma P6(b) to (d) are statements about the realised prefix. This is the
  defect `c2-local-mesp/ADVERSARY.md` F7 records in the manuscript's scalar revenue proof, which
  both continuous proofs avoid by using `P = E sum_t m_{I_t,t}` instead of optional stopping.
* *A path that abandons a cube during its fallback*, so that the EXP3 doubling epoch is truncated
  mid epoch. Covered: the exponential potential inequality holds for every prefix, which is the
  first of the three checks in Lemma 7 and in Lemma P7, and `separation/REPORT.md` Lemma A is
  stated for a deterministic `T <= 2^k`. I did not re-derive that lemma.

**Conclusion of Section 5.** I could not construct an arrival path that beats any of the three
bounds. I regard this as the strongest evidence in favour of the construction that I produced,
because it is the hypothesis the theorem weakens and therefore the place a referee will push.

## 6. The one sided bid bound and the oscillation allowance

### 6.1 The one sided bound: the index set, and an agent that sees the future

**The index set is deterministic under every deviation.** The Stage-1 phase at cube `C` is exactly
its first `K L_n` visits, and the agent pulled at the `v`-th visit is `((v - 1) mod K) + 1`. `V_C`
counts arrivals in `C`, the grid is fixed before play, and neither the phase test nor the
round-robin reads a reward, a bid, a coin or a message. No deviation can change `V_C`, because no
deviation changes `X_t`. So the map `(j, C, r) -> t_{j,C,r}` is a function of `A` alone, in every
execution and under every element of `B^ctx+`. I checked this against the round rule of
`EXPLORER.md` Section 3 clause by clause and it holds; it is the design point the mechanism was
built around, and it is what `c4-safe-partitions/REPORT.md` says cannot be relaxed to a reward
dependent schedule. It holds for the **Stage-1** index set only; the Stage-2 and fallback index
sets are random, and no step uses their determinacy.

**Predictability against an agent that conditions on the whole path.** The target `m_{j,C,r}` is
measurable with respect to `F_{t-1} v sigma(I_t, j's private coins)` with `t = t_{j,C,r}`, and
`F_0` contains `sigma(A)`. The Azuma step therefore needs

    U_t  is uniform and independent of  F_{t-1} v sigma(I_t, private coins) ,

which contains `A`. Conditioning on the *entire* path, future included, is harmless precisely
because `A` is independent of the seed array: seeing the future tells the agent nothing about
`U_t`. This is the correct answer to the question, and it is exactly where G1 bites: the
independence that is needed is joint, not pairwise, and the displayed (A3) and (A4) do not supply
it. Under the corrected hypothesis I could not break the step; under the hypothesis as displayed
the step is false, by Section 3.

**Whether it holds for a deviator's own bid.** Yes, one sidedly. `Abar'_{i,C} <= Mbar_{i,C}`
pathwise by feasibility, and `beta'_{i,C} <= Abar'_{i,C} + s_n` on `E_C`, so
`beta'_{i,C} <= Mbar_{i,C} + s_n` uniformly over `B^ctx+`. `PROVER2.md`'s remark that "the
deviator's bid cannot concentrate" is true two sidedly and false one sidedly, and I confirm the
distinction. A deviator can force `beta'_{i,C} = 0` while `Mbar_{i,C} = 1`, so no lower bound on
its own bid is available and none may be used.

### 6.2 Does anything downstream need a two sided bound? A complete enumeration

I enumerated every place in either proof where a bid enters an inequality, and classified it.

| where | which agent's bid | direction | what supplies the target bound |
|:-|:-|:-|:-|
| Lemma P2 / Lemma 5, `beta_(2) <= beta_W` then `beta_W <= Mbar_W + s_n` | the realised winner, possibly the deviator | upper only | feasibility `Abar <= Mbar` |
| Lemma P3 / consequence C3, `beta_(2) <= beta_{j*}` then `beta_{j*} <= Mbar_{j*} + s_n` | a non-deviator | upper only | `S^*` gives `Abar = Mbar` |
| Lemma P4 / Lemma 8, part (B) | every agent, all at `S^*` | lower | `S^*` gives `Abar = Mbar` |
| Lemma P5(iii) / `G_H`, part (C) | the honest comparator `h_C` | lower | pointwise honesty gives `Abar >= v_C` |
| Part (C) case (ii), `beta_(2) >= beta_{h_C}` | order statistic, `h_C` not the winner | lower | the case hypothesis `W_C != h_C` |
| (6.1) / Lemma 4(b), `beta'_{i,C} <= beta^*_{i,C}` | the deviator | upper, **pathwise** | shared seed and feasibility |

**No step anywhere uses a lower bound on a deviator's bid.** The two lower bounds that do occur are
about agents whose target floor comes from something other than concentration: `S^*` in part (B)
and honesty in part (C). This is the whole content of `PROVER2.md`'s divergence from the explorer,
and I confirm it. I also confirm that it makes part (C) cleaner: there is no baseline execution in
part (C), so a counterfactual object would have to be invented for it, and `EXPLORER.md` does
invent one (`G_H`), whereas `PROVER2.md` uses the same Lemma P1 twice.

**The one thing I would flag.** Part (C) case (ii) needs `beta_(2),C >= beta_{h_C,C}`, which follows
from `W_C != h_C` only because `beta_(2)` is the second order statistic **with multiplicity**. If
the mechanism used the second *distinct* value the step would fail when several agents tie at
`h_C`'s bid. The mechanism does say "with multiplicity" (Section 3), so this is correct as written;
I record it because it is the kind of clause that gets lost in an eight page rewrite.

### 6.3 The oscillation allowance

**Every use, and whether any compounds.** I found seven applications of Fact 0 in the two proofs and
checked which budget each is charged to.

| use | statement | charged to |
|:-|:-|:-|
| 1 | Lemma P2: `Mbar_W <= M_W(x_W) + omega` | `sigma_n` |
| 2 | Lemma P3: `Mbar_{j*} <= M_{j*}^inf(C) + omega` | `sigma_n` |
| 3 | Lemma P4: `Mbar_j >= M_j(x_j) - omega`, through the order statistic | `e_price` |
| 4 | Lemma P5(i): `b(X) <= v_C + omega` | the part (C) slack |
| 5 | Lemma P8: `M_{j'}^sup(C) <= M_{j'}^inf(C) + omega` for non-deviators | `e_osc` |
| 6 | part (A) case 2: `mu_i^sup(C) <= mu_i^inf(C) + omega` | `e_osc` |
| 7 | part (A) case 2: `1 + mu_i^sup - nu_i(C) <= w_C + omega` | `e_osc`, via use 6 |

Uses 1 and 2 are the only two charged to `sigma_n`, and they occur in different lemmas, never in
the same chain, so `sigma_n >= s_n + omega` suffices for both and the specified `3 s_n + rho_n`
has a factor three of margin. Use 7 looks like a compounding of use 2 with use 6, because it
combines `nu_i(C) >= tau_C` (which spent an `omega` inside `sigma_n`) with `mu_i^sup <= mu_i^inf +
omega`. It is not: the first `omega` was already paid out of `sigma_n` when `tau_C` was formed and
does not reappear in the `e_osc` charge. I traced the `omega` bookkeeping of part (A) case 2 term
by term and the total per cube is `n_C rho_n` exactly, as both proofs state. **I could not find a
use that compounds.** I also confirm `PROVER2.md` D4: the `3 s_n` is unused, and the report's stated
reason for it does not match its own proofs.

**A configuration where the allowance is too small.** There is one, and it lies exactly on the other
side of (A2). This settles whether (A2) is technical.

*Instance, for each `n`.* `K = 4`, `d = 1`, `D = 4`, so the bound is `O(n^{6/7} log n)`. Let
`t : [0,1) -> [0,1]` be the triangle wave of period `h_n` with slope `4/h_n`, so `t` is
`L`-Lipschitz with `L = 4 g_n` and `t` is uniform on `[0,1]` over each period. Put

```
 M_1 = M_2 = t ,    M_3 = M_4 = 1 - t ,    mu_j == 0 for all j ,   K_H = {1} with mu_1 == 0 .
```

All four are `L`-Lipschitz, so (A1) holds; (A2) fails, since `log(en) >= 3 L = 12 g_n` is false.
Let the arrival path set all four coordinates equal to a common `y_t` sweeping `[0,1)`.

*Arithmetic, verified at `4 x 10^6` draws in `<scratchpad>/round2/f1-adversary/osc.py`.* Every
`Mbar_{j,C} = 1/2`, so all four bids are `1/2 +- s_n`, `beta_(2),C = 1/2 +- s_n` and
`tau_C = (1/2 - sigma_n)_+`. The winner, say agent `1`, has capacity `t(y_t)` uniform on `[0,1]`,
so under `S^*` it delivers `min{tau_C, t(y_t)}` with mean `tau_C - tau_C^2/2`, a deficit of
`tau_C^2/2` per pull against the announced price. The monitor therefore fires after
`O(ell_n / tau_C^4)` pulls, the cube switches, and the fallback runs EXP3 over four arms whose
conditional means are all `1/2`. So

    revenue per post Stage-1 round  ->  1/2 ,   while   E M_(2)(X)  =  E max{t, 1-t}  =  3/4 ,

measured `0.749953` against the predicted `0.75`, and `E[min(tau,t)] = 0.37515` against the
predicted `0.375` at `tau = 1/2`. Part (B) is therefore short by `n/4` against an error budget of
`O(n^{6/7} log n)`. In the regime `sigma_n >= 1/2` the failure is worse, not better: `tau_C = 0`,
no switch can occur, the winner delivers `0` and revenue is `0` against a benchmark of `3n/4`.

*What this shows and what it does not.* It is a sequence of instances with `L = 4 g_n` growing, not
a fixed instance, so it does not contradict Theorem 1: for any fixed `L`-Lipschitz instance (A2)
holds once `n >= exp(3L)`. What it shows is that **the guarantee is not uniform over the Lipschitz
class at a fixed horizon**, and that when (A2) fails the failure is by a constant fraction of `n`
rather than gracefully. So (A2) is load bearing and the mechanism cannot detect its violation,
because `L` is unknown to the platform by (A6) and, by `c4-safe-partitions/REPORT.md` Theorem 4,
estimating the modulus from rewards is itself unsafe. The correct reading of "uniform over
instances" is "uniform over the `L`-Lipschitz instances with `log(en) >= 3L`", which is
`PROVER2.md` Section 10.4's qualification supported by an explicit failure.

## 7. Sweep for the two recurring defect shapes

`PROVER2.md` Section 12 reports two defects in `EXPLORER.md` that it calls "the kind of error that
recurs": a union bound over a random index set (D1) and a global event asserted to lie in a cube's
local field (D2). I confirm both and I swept both documents for further instances.

### 7.1 Union bounds over random index sets

**D1 confirmed.** `EXPLORER.md` Lemma 6(a) counts "at most `n` pairs `(C,r)` ... because
`sum_C (Stage-2 pulls at C) <= n`". The number of Stage-2 pulls at a cube is random even after
conditioning on `A`, since it depends on the switch, so the count is over a random index set. The
corrected count is `J'_n` cubes times `n` values of `r`. `PROVER2.md`'s correction to
`Pr(H^c) <= n^{-3}/K` and its repair `ell_n := log(2 K n^6)` are both right, and I verified the
exponent arithmetic: `2 n^2 e^{-ell_n} = 2 n^2 / (2 K n^5) = n^{-3}/K`.

**No second instance.** I checked every other union bound in both documents. `EXPLORER.md` Lemma 3
and `PROVER2.md` Lemma P1 union over `(j, C)` with `C` ranging over the cubes that complete
bidding: that set is `F_0`-measurable under Convention A, so the count is legitimate, and it is
legitimate for the same reason that Section 4.1 above shows it is not *needed* (without exogeneity
one unions over the deterministic set of all `J_n` grid cubes at a cost of a constant). Part (C)'s
union for `G_H` and for `E^H_C` is the same shape and is likewise fine. The Cauchy and Schwarz sums
`sum_C b_n(n_C)` and `sum_C R^dbl_K(n_C)` are over `F_0`-measurable `n_C` and are correct.

**One related misstatement, not a union bound.** `EXPLORER.md` Lemma 7 asserts that `H_C`, the
number of fallback visits to `C`, is "an `F_0`-measurable integer under Convention F-A, since the
switch round is a stopping time". The switch round is not `F_0`-measurable and neither is `H_C`;
what is true is `PROVER2.md`'s version, that `H_C^fb` is measurable with respect to the fallback
start field. The distinction matters because it is the whole content of Section 4.3 above: the
conditional statement is fine, the `F_0` claim is not, and no step needs the `F_0` claim.

### 7.2 Global events inside conditional expectations, including one in `PROVER2.md` (G5)

**D2 confirmed.** `EXPLORER.md` Section 7.1 asserts that `G` "is determined by the Stage-1 data at
the cubes and is therefore measurable with respect to the fallback-start field `F_fb` at every
cube". False: `G` intersects over all cubes, and cubes interleave along `A`, so a cube `C''` may
still be in Stage 1 when `C` switches. The same defect recurs in Section 7.3 with `G_H`.
`PROVER2.md`'s repair, replacing `G` by `G_C` and using `U'^fb >= 0`, is correct.

**G5: the same defect is in `PROVER2.md`'s own proof, and `PROVER2.md` asserts the opposite.**
Section 6, in the paragraph "Legitimacy of the conditioning, which is where I diverge from
`EXPLORER.md`", lists the four events multiplying the conditional expectations of Lemmas P7 and P8
and says "`E^*_C` and `H^*_C` likewise, for the baseline execution, which lives on the same space".

`E^*_C` is fine: it is a function of the baseline's Stage-1 rewards at `C`, all of which occur at
rounds `t_{j,C,r}` that precede `C`'s Stage 2 in both executions.

`H^*_C` is **not**. In Case 2 the baseline does not switch at `C` (that is what the case needs), so
its Stage-2 phase at `C` runs through all `n_C` post-Stage-1 visits to `C`, the last of which is in
general far **after** the round at which the deviating execution switched at `C`. The event
`H^*_C = { |Z^*_r - A^*_r| <= b_n(r) for all r <= n }` therefore depends on seeds at rounds after
the deviating execution's fallback start, and is not measurable with respect to that field. The
identity `E[ U'^fb 1_{E_C cap H_C cap E^*_C cap H^*_C} ] = E[ 1_{...} E[U'^fb | F_fb] ]` is not
justified as written, for exactly the reason D2 gives for `G`.

**Repair, three lines, and it is the same repair D2 needs.** Write `good := E_C cap H_C cap E^*_C
cap H^*_C` and `F := E_C cap H_C cap E^*_C`, which is in `F_fb`. On `good`, pathwise,

    U'^post - U^{*,post}  <=  U'^fb  -  H w_C  +  q rho_n/3 + 1 + 2 b_n(q) .

Then, since `U'^fb >= 0` and `0 <= w_C <= 2`,

    E[ (U'^fb - H w_C) 1_good ]  <=  E[ (U'^fb - H w_C) 1_F ]  +  E[ H w_C 1_{F \ good} ]
                                 <=  E[ 1_F ( (2 rho_n/3) H + R^dbl_K(H) ) ]  +  2 n_C Pr( (H^*_C)^c ) ,

and, since `Pr((H^*_C)^c) <= 2 n e^{-ell_n} = n^{-4}/K` per cube and `sum_C n_C <= n`, the total
extra charge is `sum_C 2 n_C Pr((H^*_C)^c) <= 2 n^{-3}/K`, absorbed into the `O(n^{-2})` term the
corrected D1 already produces. **Neither the statement nor the rate changes.**
Severity P3, and I would not raise it at all except that `PROVER2.md` presents this paragraph as the
place its proof is correct and the explorer's is not.

**What this says about the two proofs agreeing.** `EXPLORER.md` handles `H` correctly (Section 7.1
states explicitly that `H` is not `F_fb`-measurable and confines it to pathwise uses) and handles
`G` wrongly. `PROVER2.md` handles `G` correctly (per cube throughout) and handles `H^*` wrongly.
Each proof avoided the other's instance of the same error and committed its own, in the one place
the other was careful. Two proofs that agree on every conclusion can still both be wrong in the same
*shape* in complementary *places*, and that is what happened here. It is the strongest reason I
have to say that the agreement of the two routes is weaker evidence than it looks.

## 8. Framing: what overreaches, in the shape `PROVER2.md` Section 15 item 2 identifies

`PROVER2.md` Section 15 item 2 records that the claim "the rate is attained" carries an instance
quantifier the theorem does not, because the tightness construction needs the top gap to exceed the
shading plus the oscillation. I confirm that: `EXPLORER.md` Section 7.5 item 2 asserts that `e_bid`
"is attained by the obvious analogue of Proposition `prop:tightness`", and the analogue requires
`M_i - max_{j != i} M_j > sigma_n + omega` on the relevant cubes, which is an instance condition.
`EXPLORER.md`'s own simulation confirms the dependence: on instance C (unique top at every context)
the Stage-1 gain matched `J L (M_0 - m')` to the digit, and on instance D the measured gain fell
short of the prediction, which the report attributes to "the context dependence of the runner-up
inside a cube". So the upper bound is uniform and the matching lower bound is not.

I was asked whether anything else overreaches in the same way. Four things do.

### 8.1 G7: the scalar by-product is already banked

`EXPLORER.md` Sections 0.3 and 7.4 present, as a by-product that would change the manuscript, the
removal of the non-top branch, the `delta_i` constants and the caveat sentence from
`thm:private-mesp`. `PROVER2.md` Section 10.1 confirms it independently and re-derives it.

**Both describe the manuscript at tag `baseline-2026-09-17`, not the branch.** On
`aamas2027-revision` the good event at `sections/appendix_private.tex` lines 92 to 95 is already
`G_i := G_{-i} cap { beta_i^max <= M_i + s_n }`; `eq:private-price-win` already reads
`tau_i <= min{V_i, M_i}`; line 106 already says "Only the upper tail of the capacity bid
`beta_i^max` is used"; line 144 already says "No capacity gap and no other instance quantity enters
it"; and `sections/Private_information_setting.tex` already says "The first bound is uniform over
the declared deviations and over all scalar instances with `K` agents; no capacity gap enters it".
There is no paragraph beginning "If `i` is non-top", no `eq:private-fallback-low` and no `delta_i`
anywhere in the section or the appendix.

The change landed in commit `2e2a54f`, "batch 13: remove the non-top branch and the last instance
constant from the private theorem", at 19:21 UTC on 18 September, which is after `PROVER2.md` was
committed at `3e3a180`, 19:16 UTC, and it came from the `nontop-removal` track. The sentence both
documents quote, "No concentration around the deviator's capacity is invoked", is at line 99 of the
file at the baseline tag and is not in the file now.

So nothing is wrong with either argument and there is nothing to do: the edit is banked, it must not
be applied twice, and the two reports' quotations of `sections/appendix_private.tex` are stale and
should carry a note saying so. I checked this by `git show baseline-2026-09-17:sections/appendix_private.tex`
against the working tree and by `git merge-base --is-ancestor 2e2a54f HEAD`.

### 8.2 "At the exponent of the existing public contextual result" understates the public result

There are two public contextual rates in `sections/contextual_samf_algorithm.tex`, not one.

* `thm:grid-ucb-robust`, the headline rule, at `E_n = O(n^{(D+1)/(D+2)} (log n)^{1/(D+2)})`, which
  gives **all four** of contextual sharp adaptivity, exact contextual monotonicity, expected
  contextual FATA, and, under `L`-Lipschitz capacities with two tops at almost every profile, a
  unilateral deviation bound `E_n` and revenue `E sum_t M_star(X_t) - E_n^K`.
* `thm:grid-etc` and `thm:contextual-public`, at `n^{(D+2)/(D+3)}`.

Since `(D+1)(D+3) = D^2 + 4D + 3 < (D+2)^2`, the first exponent is **strictly smaller** for every
`D >= 0`. `EXPLORER.md` Section 0.1 is careful and says "matches the exponent of the manuscript's
public contextual theorem `thm:grid-etc`", which is exactly right. A headline of the form "at the
exponent of the existing public contextual result" is not, because the natural reading picks the
better of the two. The paper must name `thm:grid-etc` when it makes this comparison.

### 8.3 The benchmark is strictly weaker, and the top-set condition has been absorbed, not removed

`thm:grid-ucb-robust` and `thm:contextual-public` deliver `P(n) >= E sum_t M_star(X_t) - o(n)`.
Theorem 1 part (B) delivers `P(n; S^*) >= E sum_t M_(2)(X_t) - o(n)`. Same exponent, different
benchmark, and `M_(2) <= M_star` pointwise with the gap equal to the top gap.

The two facts interlock. `thm:contextual-public` assumes two agents attain the largest capacity at
`nu`-almost every profile; **that assumption is exactly the statement `M_(2) = M_star` almost
everywhere.** So the claim that Theorem 1 "requires no top-set condition" is literally true and
materially misleading: on the instances where the public theorem's hypothesis holds, the two revenue
statements coincide, and on the instances where it fails, Theorem 1 does not remove the condition,
it pays for it by weakening the benchmark by precisely the top gap. `EXPLORER.md` Section 2.6 item 2
proves that no mechanism can do better uniformly over behaviour, so this is not a defect of the
mechanism; it is a defect of the sentence. The paper should say "the top-set condition is replaced
by the second-capacity benchmark", not "no top-set condition is needed".

### 8.4 "No instance constant" no longer separates Theorem 1 from the paper

As of `2e2a54f` the scalar `thm:private-mesp` also has no instance constant and no capacity gap.
The property therefore separates Theorem 1 from the two C2 finite contextual candidates, which
carry `delta_i`, `D_i(z)` and `e_low`, and from nothing in the manuscript. It also is not free: the
instance dependence has moved into the hypothesis `n >= exp(3L)`, which Section 6.3 above shows is
load bearing. "No instance constant in the bound, at the price of an instance dependent horizon
threshold" is the accurate sentence.

### 8.5 Part (A) is informative only for agents whose baseline payoff is linear

Under `S^*`, on the good events no cube ever switches, so an agent that wins no cube is pulled only
at Stage-1 and its total utility is at most `2 J'_n L_n = 2 e_bid`, which is
`O(n^{(D+2)/(D+3)})`. The permitted gain in part (A) is `e_bid + e_osc + e_mon + e_fb`, and
`e_osc = n rho_n` alone is `Theta(n^{(D+2)/(D+3)} log n)`. So for a never-winning agent the
guarantee permits a gain larger than its entire baseline payoff, and there is a real deviation of
that order: deliver `0` at every Stage-1 pull, which costs it nothing because it loses anyway and
gains `M_i(x_{i,t})` per pull, `Theta(J'_n L_n)` in total whenever `M_i` is bounded below.

This is not a defect of Theorem 1, and the scalar theorem has the same feature through
`prop:tightness`, but it means "additive behavioural equilibrium" is a statement about the winner.
A referee who asks "what does part (A) rule out for a losing agent" gets the answer "nothing", and
the paper should not let the word equilibrium carry more than that.

### 8.6 The horizon at which the theorem says anything, computed

Both reports say the mechanism is numerically vacuous at every simulable horizon
(`EXPLORER.md` Section 10.1, `PROVER2.md` Section 10.3). I computed the thresholds exactly, from
the parameters of `EXPLORER.md` Section 3 with `K = 2` and `J'_n = min{J_n, n}`, in
`<scratchpad>/round2/f1-adversary/cross.py` and `exponents.py`. The entries are the smallest `n`
at which each quantity first drops below the trivial value.

| `D` | `sigma_n < 1` | bound (A) `< n` | bound (B) slack `< n` |
|:-|:-|:-|:-|
| 1 | `10^{6.1}` | `10^{5.3}` | `10^{6.8}` |
| 2 | `10^{8.5}` | `10^{7.6}` | `10^{9.3}` |
| 3 | `10^{11.1}` | `10^{10.1}` | `10^{12.1}` |
| 4 | `10^{13.8}` | `10^{12.7}` | `10^{14.9}` |
| 6 | `10^{19.4}` | `10^{18.4}` | `10^{20.8}` |
| 10 | `10^{31.7}` | `10^{30.7}` | `10^{33.7}` |

Since `D = K d`, the smallest interesting case is `K = 2`, `d = 1`, which is already `10^{8.5}`, and
three agents with two dimensional contexts is `D = 6`, that is `10^{19.4}`. The threshold grows
like `exp(c D)`, not polynomially, because `J_n` carries a `2^D` and `rho_n` carries a `sqrt D`. A
referee will compute this, so the paper should state it rather than be shown it, and it should say
so in the same sentence in which it claims the exponent matches the public result: **the two rates
have the same exponent and very different constants**, since `thm:grid-ucb-robust`'s `E_n` has an
explicit constant `4 sqrt(J_n n log n) + 3 min{J_n, n}` with no `2^D` multiplying a bidding block.

## 9. Where the two proofs disagree, and which I believe

1. **The good event.** `EXPLORER.md` puts the deviator's counterfactual capacity bid
   `beta^cap_{i,C}` in `G`; `PROVER2.md` puts a one sided Azuma bound on the realised bid in `E_C`.
   **Both are correct and I believe `PROVER2.md`'s.** I checked the counterfactual's two required
   properties independently: `beta^cap_{i,C}` is a function of `A` and of the seeds at the
   `F_0`-measurable rounds `t_{i,C,r}`, so it is defined on the same draw in both executions and its
   law does not depend on the deviation; and the enlargement of the deviation class to see the whole
   path does not touch it, because the class governs what the agent conditions on and not which
   random variables the analysis may name. `PROVER2.md`'s route is better for three reasons it
   states and a fourth it does not: it also removes the only place where `EXPLORER.md`'s route needs
   the arrival path to be exogenous *for the definition of an object* rather than for a bound, since
   `beta^cap_{i,C}` is well defined only if the rounds `t_{i,C,r}` are the same in both executions.
2. **Global versus per cube conditioning.** `PROVER2.md` is right that `EXPLORER.md`'s `G` is not
   `F_fb`-measurable. `PROVER2.md` is wrong that its own `H^*_C` is (Section 7.2 above, G5). So the
   correct verdict is that **both proofs have one instance of the defect and each is in the place
   the other was careful**. Both repairs are three lines and neither changes a statement.
3. **The monitoring union bound.** `PROVER2.md` is right (D1). I verified the corrected arithmetic.
4. **Constants in `e_rob` and in `sigma_n`.** `PROVER2.md`'s are smaller and correct (D3, D4). I
   confirm that `sigma_n = s_n + rho_n/3` suffices for all of P2, P3, P4 and P5 and that the stated
   reason for `3 s_n` in `EXPLORER.md` Section 3 design point 1 does not match either proof.
5. **The least secure step, where I disagree with both.** `EXPLORER.md` ranks the counterfactual
   first and Convention F-A second; `PROVER2.md` ranks Convention A first and says the
   counterfactual is sound. My ranking is neither:
   * **first**, the joint independence of the seeds with the arrivals and the coins, because it is
     the only thing in this report that I could actually break (Section 3);
   * **second**, the coupling of the two Stage-1 schedules in part (A), which is the one genuine
     use of exogeneity and which the transplanted counterexample kills (Sections 4.2, 4.4);
   * **third**, the fallback horizon `H_C^fb` at a cube's fallback start (Section 4.3), which no
     one on this track has repaired;
   * and **not at all**, the `F_{s-1}`-measurability of the Stage-2 indicator, which both reports
     name and which is a bookkeeping artefact (Section 4.1).

### 9.1 The separation, stated as the answer to the question I was asked

Exogeneity is used in three distinct places and the three parts of the theorem need different
amounts of it.

* **Part (B) uses no exogeneity at all**, once Lemma P1 is restated with the pre-seed field and a
  stopping time. Part (B) invokes Lemma P1, Lemma P4 and Lemma P6(d) and **never invokes Lemma P7**,
  because on the good events `S^*` never triggers a switch and there is no fallback to analyse. So
  the second capacity revenue guarantee holds for arrivals that may react to past rewards, provided
  only that `X_s` is conditionally independent of `U_s` given the past.
* **Part (C) uses exogeneity only through the fallback horizon** (load three). If that is repaired
  by optional stopping at the bounded local fallback clock, as `c2-local-mesp/ADVERSARY.md`
  Section 2 item 2 says it can be for the finite analogue, part (C) also holds for reward reactive
  arrivals.
* **Part (A) genuinely needs exogeneity** and is false without it.

I did not write the stopping time version of Lemma P1 or the optional stopping version of Lemma P7,
so this is a route and not a theorem. But it is a route with a concrete payoff: the paper could
state (B) and (C) under "arrivals are nonanticipating with respect to the seeds" and (A) under
"arrivals are exogenous", which is a sharper and more defensible pair of hypotheses than the single
(A3) and is honest about where the counterexample lives.

## 10. What I attacked and could not break

I record these because a failed attack on a named step is the only evidence an adversary produces.

1. **Lemma P2 and Lemma 5, the price lemma.** Three inequalities, each checked: `beta_(2) <= beta_W`
   (definition of a largest bidder with multiplicity), `beta_W <= Abar_W + s_n` (Lemma P1, one
   sided, uniform over `B^ctx+`), `Abar_W <= Mbar_W` (feasibility), `Mbar_W <= M_W(x_W) + omega`
   (Fact 0, uniformly over `X in C`). I tried to break it by making the winner the deviator, by
   making the deviator the runner up and bidding high to raise the price above the winner's
   capacity, and by adversarial placement of Stage-1 contexts inside the cube. All fail, and the
   second fails for a reason worth recording: a runner up cannot raise `tau_C` above the winner's
   capacity because its own bid is itself bounded by its own capacity average, and `beta_(2) <=
   beta_W` then does the rest. The mechanism is self protecting here.
2. **Winner inclusion, (6.1) and Lemma 4(c).** The tie break argument is correct: `i` wins iff
   `beta_i > beta_j` for lower priority `j` and `beta_i >= beta_j` for higher priority `j`, and
   lowering `beta_i` while holding the others fixed preserves every failure of those inequalities.
   I checked that the priorities are drawn at a cube's first visit, hence at the same round in both
   executions, and that the arrival path cannot influence them.
3. **The claim that a deviator gets no post Stage-1 pull at a cube it loses.** Correct and
   structurally important: Stage 2 pulls only the winner, so a losing deviator cannot influence the
   switch at that cube, and the only way to reach the fallback is to win and then fail the monitor,
   which Lemma P8 prices.
4. **The monitor at the failing pull**, Lemma P6(b) with `q` the failing index. Checked both
   branches, including `A_q >= A_{q-1}`, `tau_C <= 1` and `b_n(q-1) <= b_n(q)`.
5. **Lemma P8's replacement of `Qbar_i` by `H`.** Checked the splitting inequality
   `nu_i(C) H - R^dbl_K(H) <= Abar_i + (nu_i(C) + rho_n/3)(H - Qbar_i)` and the sign of
   `1 + mu_i^sup(C) - nu_i(C)`, which is nonnegative because `nu_i(C) <= 1`. Both provers list this
   as a step deserving a third reader; I read it and I believe it. The measurability around it is
   G5, which is a separate matter.
6. **Part (B) via `P = E sum_t m_{I_t,t}`.** Correct and strictly simpler than the manuscript's
   scalar revenue argument, which does use a stopping time. I confirm `PROVER2.md`'s observation
   that no optional stopping is needed and `c2-local-mesp/ADVERSARY.md` Section 6.1's observation that the
   scalar version's stopping time claim is false at a cell that stops being visited.
7. **Part (C) case (i) versus case (ii), and the domination of case (ii).** Checked, including that
   `h_C` depends on the instance and the grid only, so it is a legitimate fixed comparator under
   arbitrary joint behaviour.
8. **Part (D).** Recomputed all seven bounds in
   `<scratchpad>/round2/f1-adversary/exponents.py` and confirmed
   `(D+2)/(D+3) > (2D+3)/(2D+6) > D/(D+3)` for `D = 1` to `11`, hence that `e_mon` and `e_fb` are
   strictly dominated. I also confirmed `(D+1)/(D+2) < (D+2)/(D+3)`, which is the basis of
   Section 8.2.
9. **All four adversarial arrival paths** of Section 5, plus four I invented.
10. **The oscillation allowance**, all seven uses, for compounding (Section 6.3).

## 11. What I did not check

1. **`EXPLORER.md` Section 2 in full.** I read Lemma 1, Corollary 2 and Proposition 3 and I believe
   them, but I did not attack them and nothing in this report depends on them. I did not check
   Proposition 4 or the four consequences of Section 2.6.
2. **`EXPLORER.md` Sections 8 and 9**, the per agent architecture PA-MESP and the route map. I take
   no position on the `d` versus `D` comparison or on the correction to the sceptic's Section 2.2.
3. **The EXP3 machinery.** I did not re-derive the exponential potential inequality, the prefix
   validity, the doubling sum or the constant `3(2 + sqrt 2)`. `separation/REPORT.md` Lemmas A and B
   and `c2-local-mesp/ADVERSARY.md` Section 9.1 both cover it and I treated it as settled. In
   particular I did not verify the selected reactive form, in which the reward of the selected arm
   is chosen after the selection coin; `PROVER2.md` Lemma P7 defines `r_{j,s}` conditionally on
   `I_s = j`, which I believe is the right definition, but I did not check the second moment step.
4. **`EXPLORER.md` Section 10 and `PROVER2.md` Section 11**, the two simulations. I did not rerun
   either. My own four scripts test arithmetic identities, not the mechanism.
5. **The optional stopping repairs I propose** in Sections 4.3 and 9.1. Both are sketched and
   neither is written, so Section 9.1's separation of the three parts is a route, not a theorem.
6. **Anything about anytime horizons, unknown `n`, or non-Lipschitz capacities**, beyond the
   instance of Section 6.3.
7. **Whether some other mechanism can beat `n^{(D+2)/(D+3)}`.** No lower bound is in either document
   and I did not attempt one.
8. **The consequences for other audit files** of Sections 8.1 and 7.2. In particular I did not check
   whether `nontop-removal/REPORT.md` and this track's two documents now say inconsistent things
   about `sections/appendix_private.tex`.

## 12. On the agreement of the two proofs, which is what I was asked to break

The two workers agree on all three parts and on the exponent, and they reached them by routes that
differ at the explorer's own declared weakest step. That is genuine and I did not overturn it. But
the agreement is weaker evidence than it looks, for four reasons that this report establishes.

1. **They inherited the same framing from the same upstream document and both carried the same
   error in it.** Both name the `F_{s-1}`-measurability of the Stage-2 indicator as the least secure
   step and both attribute it to exogeneity. `c2-local-mesp/ADVERSARY.md` Section 2, written on the
   same day, had already shown that the finite analogue of that step is secure and that the
   attribution is wrong. Both documents cite Section 7.1 of that file and neither cites Section 2.
   Agreement between two workers who read the same three upstream documents is agreement about those
   documents as much as about the mathematics.
2. **Both reintroduced a hypothesis defect that had already been found and repaired in the finite
   documents.** G1 is `c2-local-mesp/ADVERSARY.md` F2, and the adversary there gave the one word
   repair. `EXPLORER.md` Section 4 restated the pairwise form and `PROVER2.md` copied it and then
   asserted the joint conclusion. Two proofs that both start from the same hypothesis list cannot
   cross check the hypothesis list.
3. **Each committed the same shaped measurability error, in the place the other was careful.**
   `EXPLORER.md` is careful with `H` and wrong with `G`; `PROVER2.md` is careful with `G` and wrong
   with `H^*`. Neither caught the other's second instance, because each looked only where its own
   route differed.
4. **The independence of the second proof is partial where it matters most.** `PROVER2.md` says it
   took the mechanism, the hypotheses and the statement and derived the three parts. That is a
   genuine and valuable independence of *proof*. It is not independence of *specification*: the
   mechanism, the parameters, the proposed profile, the deviation class and the hypothesis list are
   all `EXPLORER.md`'s, and three of my eight findings (G1, G2, G4) are defects of the specification
   rather than of either proof. A second prover who is handed the specification cannot find them.

**What would change my verdict.** Theorem 1 as I read it, with (A3) and (A4) corrected to mutual
independence and with the three line repairs of D1, D2 and G5, is a statement I could not break, and
the one counterexample I have (Section 4.4) attacks a hypothesis the theorem makes. I would change
my verdict if the optional stopping repair of Section 4.3 turned out to be impossible, because then
parts (B) and (C) would rest on a step that is stated but not proved, or if a fourth reader found
that `beta^cap_{i,C}` is used somewhere `PROVER2.md` believes it is not.

## 13. Compute log

Four scripts, all on the login node with the project venv, seconds each. No Slurm job was
submitted, so there is nothing to add to `COMPUTE_LOG.md`. All in
`/scratch/.../scratchpad/round2/f1-adversary/`:

* `g1_check.py`, `g1b_check.py`: the two G1 instances of Section 3, `2 x 10^6` and `4 x 10^5` draws.
* `osc.py`: the oscillation instance of Section 6.3, `4 x 10^6` draws.
* `exponents.py`, `cross.py`: the part (D) terms and the vacuity thresholds of Section 8.6.

None of these simulates the mechanism. They verify arithmetic identities and independence
properties, and I claim nothing else for them.

# SECOND PASS, after the revision of `PROVER2.md` to 1353 lines

Resumed 18 September 2026. I read the revision in full before writing anything: the corrected
Section 2, the G5 repair in Section 6, and the four appended Sections 17 to 20. This pass has two
parts, kept separate as asked: Section 14 adjudicates my own eight findings against the repairs,
and Section 15 attacks the new material as new surface.

**Headline of this pass.** The repairs are real and mostly close what they claim. But the single
new hypothesis (A4c) does **not** do both jobs: it omits the mechanism's own randomisation, and
Lemma P7c uses that randomisation's freshness at the one step its proof depends on. I give an
explicit instance satisfying every clause of (A4c) on which Lemma P7c is false and **Theorem 1C
upgraded fails by `0.45 n`**. This is the G1 defect recurring inside the repair of G1, which is now
the third time this project has written an independence hypothesis as a list that omits a family.
Part (B) upgraded is unaffected and is correct as stated. Everything else in the new material
survived my attacks.

## 14. Adjudication of G1 to G8

### 14.1 G1 (P1): closed in Section 2, **reopened** in Section 17

**Section 2 closes it.** (A4m) names all four families and says mutually. The author's hand check of
my witness is correct on every point: `frac(x + c)` is uniform and independent of `x`, uniform and
independent of `c`, and a deterministic function of the pair; and "deliver `U_t` if `U_t <= tau_C`,
else `0`" reproduces Bernoulli(`tau_C`) at effort `tau_C^2/2`. I re-read it against my own
construction and there is no discrepancy. Under (A4m) my instance is excluded, since `U_t` is not
uniform given `G_t^-`.

**Section 17 reopens it in a different family.** (A4c) constrains only the seed `U_u`. It says
nothing about the mechanism coins, and Section 17.6 asserts that parts (B) and (C) need "nothing
further". That is false for part (C). See Section 15.1 below, which is the main finding of this
pass. **Verdict: G1 closed for part (A) and for part (B), not closed for part (C) as upgraded.**

### 14.2 G2 (P2): closed, and the repair is correct

Lemma P6c is the half step done properly and I checked it line by line. `phi_s := psi_s 1{s <= T_r}`
is `G_s^{--}`-measurable for the reason given; `N_{t-1}`, `phi_t` and `m_{I_t,t}` are
`G_t^{-}`-measurable; (A4c) gives the conditional Bernoulli law; Hoeffding's lemma gives
`E[N_t | G_t^{-}] <= N_{t-1}`; `c_n <= r` and `M_n = Z_r - A_r` under the zero extension give
`E[e^{lambda(Z_r - A_r)}] <= e^{lambda^2 r/8}`; and `lambda = 4 b_n(r)/r` gives `e^{-ell_n}`, since
`2 b_n(r)^2/r = ell_n`. All correct. The union bound over the deterministic `J_n` cubes and `r <= n`
is the right fix for D1 at the same time. **Verdict: closed.**

One unstated condition. `Pr(H^c) <= 2 J_n n e^{-ell_n} = J_n n^{-4}/K <= n^{-3}/K` needs `J_n <= n`,
and the same in Lemma P1c needs it for `<= n^{-4}`. `J_n <= 2^D n^{D/(D+3)} <= n` holds iff
`n >= 2^{D(D+3)/3}`, which is `10^{13}` at `D = 10`. It is implied by the horizons of Section 18 in
every case, but it is a hypothesis of the displayed bound and is not stated. P3.

### 14.3 G3 (P2): closed, and better than I expected

Lemma P7c does remove the third load, and it does it by the route the coordinator flagged as the
risky one, replacing optional stopping with tower steps. I attacked that route in Section 15.2 and
could not break the tower argument itself: every indicator in the pathwise potential inequality is
`G_u^{--}`-measurable, the terminal indicator `1{T_k >= 1}` appears only on the right hand side
inside a plain expectation and never inside a conditional one, and the epoch sum is pathwise in the
random `H`. I also checked the constant, which I had declined to check in my first pass: it is
right, and it is right for a reason the document does not repeat. **Verdict: closed, subject to
Section 15.1.**

### 14.4 G4 (P2): closed

Section 17.0's final paragraph states the well-posedness obstruction correctly and draws the right
consequence, that the upgraded parts must be stated for `B^ctx` and that `B^ctx+` is available only
under exogeneity. I verified that nothing in the upgraded proofs of (B) or (C) uses the larger
class: `S^*` itself is in `B^ctx` (it reads only the current own context and the announced `tau_C`
from the message), and part (C)'s three ingredients, the honest bid floor, the monitor and the
fallback comparator, are all consequences of pointwise honesty and of (A4c)'s timing, none of which
refers to the class. **Verdict: closed.**

One consequence the document states but the paper must not lose: part (C) under (A4c) is for
`B^ctx` and part (C) under (A4m) is for `B^ctx+`, and **neither dominates the other**. The upgrade
trades deviation class for arrival generality. A single theorem statement cannot have both.

### 14.5 G5 (P3): closed, transcribed correctly

The repair in Section 6 is the one I gave, with the arithmetic done correctly:
`Pr((H^*_C)^c) <= 2 n e^{-ell_n} = n^{-4}/K` per cube and `sum_C n_C <= n` give `2 n^{-3}/K`. I
confirm that `E^*_C` is in the fallback start field and `H^*_C` is not, for the reason stated.
**Verdict: closed.**

### 14.6 G6 (P2): closed as a statement, and I correct my own arithmetic

Section 20 item 4 quotes my instance as failing by `n/2`. That number is mine and it was wrong: my
Section 0 table said `n/2` and my Section 6.3 derivation said `n/4`. The derivation is right.
`E M_(2) = E max{t, 1-t} = 3/4` and the mechanism delivers `1/2` per post-bidding round, so the
deficit is `n/4`; it is `3n/4` only in the degenerate regime `sigma_n >= 1/2`, where `tau_C = 0`,
no switch can occur and revenue is `0`. I have corrected my own table. **Verdict: closed, with the
number corrected to `n/4`.**

### 14.7 G7 (P3): closed

Section 19.4 withdraws the stale block and states that nothing in it should be applied again. I
re-checked `sections/appendix_private.tex` on the branch and the situation is as described.
**Verdict: closed.**

### 14.8 G8 (P2): closed, and the coordinator's summary of it is the wrong way round

**All five parts of G8 were upheld, not withdrawn.** Section 19 is titled "Framing I withdraw or
correct", and what is withdrawn there is the *author's own* framing: 19.1 accepts that the exponent
comparison must name `thm:grid-etc` and not the headline public rule; 19.2 accepts that the top-set
condition is absorbed into the benchmark and withdraws the summary line "with no top-set, boundary,
mass or component condition"; 19.3 accepts that "no instance constant" no longer separates the
result from the manuscript; 19.5 accepts that part (A) is informative only for a winner. I checked
each against the canonical files again and each is correct.

I flag this because the message resuming me said "Your G8 framing findings are all withdrawn,
checked against the canonical files", and if that reading reaches the paper, the four sentences that
Section 19 correctly retires will be restated. **Verdict: closed, with the finding upheld and not
refuted.**

I also confirm the one thing Section 19.2 adds that I did not say, and it is a real improvement over
my version: what **is** genuinely removed, and remains a gain, is the boundary regularity, the
positive-mass condition, the finitely-many-top-stable-components condition, and for parts (B) and
(C) the arrival assumption altogether. That is the honest list.

## 15. Attack on the new material

Sections 17.0 to 17.6 are four new objects: one hypothesis (A4c) and three lemmas P6c, P1c, P7c,
plus two upgraded theorem statements. None had been adversarially reviewed. I attacked all of it.

### 15.1 H1 (P1): (A4c) omits the mechanism's own randomisation, and Theorem 1C upgraded is false as stated

This is the one thing in the revision that does not hold, and it is the "one hypothesis doing two
jobs" economy failing in exactly the way that economy fails.

**The gap.** (A4c) reads: "For every round `u`, conditionally on `G_u^{-}` the seed `U_u` is uniform
on `[0,1]`, and `Y_u = 1{U_u <= m_{I_u,u}}`." It constrains the **seed** and nothing else. Section
17.6 then says parts (B) and (C) need "nothing further".

Lemma P7c's proof contains the sentence "the weights, hence `q_u` and `p_u`, are functions of the
cube's own past fallback data, so they are `G_u^{--}`-measurable, and **the selection coin is fresh
given `G_u^{--}`**, so `E[ 1{I_u = j} | G_u^{--} ] = p_{j,u}`." The second clause is asserted, not
derived. (A4c) does not supply it. What Section 17.0 supplies is an **ordering**, `G_u^{--}` then
the mechanism coins at `u` then `U_u`, and an ordering of a filtration is not a freshness
statement: if `X_u` is a function of the round's selection coin, that coin is already
`G_u^{--}`-measurable, `E[1{I_u = j} | G_u^{--}]` is `0` or `1`, and the importance weighted
estimator `hat Y_j = Y 1{I = j}/p_j` is not conditionally unbiased for `r_{j,u}`. This is G1's
defect: a required independence omitted from the hypothesis list because the family it concerns was
not named. (A4m) of Section 2 does name the mechanism coins; (A4c) does not.

**The instance.** `K = 2`, `d = 1`, `D = 2`. Agent `1` honest with `mu_1 = M_1 == 0.9`; agent `2`
strategic with `M_2 == 1`, `mu_2 == 0`, and `K_H = {1}`. Constant primitives, so `L = 0` and (A2)
is vacuous. Two cubes `C` and `C'` of the grid. Let `(xi_u)` be the mechanism's fallback selection
coins, i.i.d. uniform, and let the arrival path be

    X_u in C   if the fallback at C would select agent 2 from xi_u ,   X_u in C'  otherwise,

which is well defined because `C`'s fallback weight vector `p_u` is a function of `C`'s own past
and is known before round `u`. Before either cube has switched, route rounds to the two cubes
alternately so that both complete Stage 1 and both award.

* Seeds: take `(U_u)` i.i.d. uniform and independent of everything. **(A4c) holds exactly**: given
  `G_u^{-}`, `U_u` is uniform and `Y_u = 1{U_u <= m}`. The arrival path is a function of the
  mechanism coins, **not** of the seeds, so it is "nonanticipating with respect to the seeds" in the
  sense of Section 17.0 remark 3.
* Deviation: agent `2` delivers `M_2 = 1` at its Stage-1 pulls and `0` at every later pull. This is
  in `B^ctx_{2,n}`; it conditions on nothing at all.

**The arithmetic.** At each cube agent `2` bids `1`, agent `1` bids `0.9 +- s_n`, so agent `2` wins
and `tau = (0.9 - sigma_n - s_n)_+ > 0` once `sigma_n < 0.9`. Agent `2` then delivers `0`, so
`Z_r = 0` and the test `Z_r < r tau - b_n(r)` fires at `r = O(ell_n / tau^2) = O(log n)`. Both cubes
switch, within `O(log n)` post-bidding rounds.

In `C`'s fallback, agent `1` is **never** selected, by construction of the path. Its EXP3 weight at
`C` therefore never updates, `q` stays uniform, `p_{2,u} = 1/2` at every round, and `C` receives a
visit on about half of all rounds. Every pull at `C` selects agent `2`, which delivers `0`. So

    reward collected at C  =  0 ,     H_C = n/2 - O(n^{(D+2)/(D+3)})  in expectation,

while Lemma P7c with the honest comparator `j* = 1` and `v = v_C = 0.9` claims at least
`0.9 E[H_C] - E[R^dbl_K(H_C)] = 0.45 n - O(sqrt n)`. **Lemma P7c is false on this instance.**

At `C'` the fallback is undisturbed and EXP3 recovers agent `1`, giving about `0.9` per round.
Total revenue is therefore about `0.9 . n/2 = 0.45 n`, while the honest benchmark is
`E sum_t b(X_t) = 0.9 n`. **Theorem 1C upgraded fails by about `0.45 n`** against an error budget of
`O(n^{4/5} log n)`.

**What this refutes and what it does not.** It does not touch the mathematics of Lemma P7c under a
hypothesis that makes the selection coin fresh, and it does not touch part (A), which is stated
under (A4m) and is therefore safe. It refutes Section 17.6's sentence "Parts (B) and (C): nothing
further". The repair is one clause, in the same shape as G1's:

> **(A4c-mech)** For every round `u`, conditionally on `G_u^{--}` the mechanism's randomisation at
> round `u`, namely the fallback selection coin and, if `C(X_u)` is met for the first time at `u`,
> the priority permutation `Pi_{C(X_u)}`, has its specified law and is independent of `G_u^{--}`.

With (A4c) and (A4c-mech) together I could not break Lemma P7c or Theorem 1C upgraded. No bound,
statement or rate changes.

**Part (B) upgraded is not affected, and this is worth saying because it sharpens the result.** I
checked every step of Theorem 1B upgraded for a use of the mechanism's randomisation and there is
none: Lemma P1c and Lemma P6c use only the seed; Lemmas P2 and P4 are pathwise consequences of
`E_C` and Fact 0 and hold for **whoever** wins, so the tie break needs no probabilistic property;
and Lemma P7 is never invoked because on `E_C cap H_C` no cube switches, with the complement charged
crudely at `n_C` rounds. **So part (B) really does hold under (A4c) alone**, which is a stronger
and cleaner statement than part (C)'s, and the paper should separate them rather than state them as
a pair.

### 15.2 The fallback lemma: I attacked the tower argument and it holds

This is where I was told to start, and I could not break it.

* **The pathwise potential inequality.** Standard, and it is genuinely per prefix, so the realised
  epoch length `T_k` needs no advance knowledge. The right hand side `(log K/eta_k) 1{T_k >= 1}` is
  correct, including the empty case.
* **Term by term expectation.** I checked all four terms. `E[phi_u 1{k(u)=k} hat Y_{j*,u}]`: the
  indicator is `G_u^{--}`-measurable and `E[hat Y_{j*,u} | G_u^{--}] = r_{j*,u} >= v`, so the sum is
  at least `v E[T_k]`. `E[phi_u 1{k} sum_i q_i hat Y_i]`: bounded **pathwise** by
  `Y_u/(1 - gamma_k)` because `p_i >= (1 - gamma_k) q_i`, so no conditional step is needed at all.
  `E[phi_u 1{k} eta_k sum_i q_i hat Y_i^2]`: uses
  `E[sum_i q_i hat Y_i^2 | G_u^{--}] <= sum_i (q_i/p_i) r_i <= K/(1 - gamma_k)`, which I verified
  using `Y^2 <= Y`. And `1{T_k >= 1}` on the right appears only inside a plain expectation, never
  inside a conditional one, so its non-measurability at any fixed `u` is harmless.
* **The one thing that could have gone wrong, and did not.** The obvious trap is that `T_k` is a
  stopping time of a clock the algorithm's own outcomes help determine, so that
  `E[sum_{u <= T_k} Z_u] = E[T_k] E[Z]` style reasoning would be invalid. The proof never does that:
  every sum is over `u <= n` with a `G_u^{--}`-measurable indicator, and the tower property applies
  round by round. The claim "an application of the tower property and not of optional stopping" is
  literally correct. This is the right way to do it and it is better than the optional stopping
  repair I sketched.
* **The constant, which I had declined to check in my first pass and now have.** The displayed
  per round penalty `2 gamma_k` looked wrong to me: the naive accounting gives
  `gamma/(1-gamma)` from the `q` versus `p` step plus `(e-2) gamma/(1-gamma)` from the second
  moment, up to `3.44 gamma` at `gamma = 1/2`, which would push `3 sqrt(K 2^k log K)` to about
  `4.4` and the doubling constant past `11`. It is not wrong. `separation/REPORT.md` Lemma A, lines
  629 to 638, multiplies the whole inequality by `(1 - gamma)` before rearranging, which absorbs
  both `1/(1-gamma)` factors and leaves exactly `v T - 2 gamma T - (K log K)/gamma`. Then
  `2 gamma_k 2^k + K log K/gamma_k = 3 sqrt(K 2^k log K)` at `gamma_k = sqrt(K log K/2^k)`, the
  `gamma_k = 1/2` branch is covered because `2^k < 4 K log K <= 9 K log K`, and the doubling sum is
  `3(2 + sqrt 2) <= 11`. **The constant is right**, and the same multiply by `(1 - gamma)` step
  works verbatim with `E[T_k]` in place of `T`. I record this because my first pass listed the EXP3
  machinery as unchecked and it is now checked.

### 15.3 Every place an indicator multiplies a conditional expectation in the new material

The author now names this as the recurring error shape, so I enumerated every instance in Sections
17.1 to 17.5.

| where | indicator | conditional expectation | verdict |
|:-|:-|:-|:-|
| Lemma P6c | `phi_s`, `G_s^{--}`-measurable | conditional on `G_t^{-}` in the supermartingale step | correct, `phi_t` is in `G_t^{-}` |
| Lemma P1c | `phi_s`, same | same | correct |
| Lemma P7c | `phi_u 1{k(u) = k}`, `G_u^{--}`-measurable | conditional on `G_u^{--}` | correct |
| Lemma P7c right hand side | `1{T_k >= 1}`, terminal | none; plain expectation | correct |
| Theorem 1B upgraded | none: no conditional expectation is taken anywhere | | correct |
| Theorem 1C upgraded, fallback | **none**, by design: the comparator bound needs no good event | correct, and this is the right design |
| Theorem 1C upgraded, Stage 2 | `1_{H_C}`, `1_{E^H_C}`, `1{case (ii)}` | Lemma P6(e), `E[Z_r - A_r] = 0` | see below |

**The one unstated step (P3).** Part (C) case (i) writes
`E[sum over Stage-2 pulls at C of Y_t] = E[sum of targets]` *within the case*, that is
`E[(Z_r - A_r) 1{case (i)}] = 0`, and case (ii) does the same. Lemma P6(e) gives only
`E[Z_r - A_r] = 0` unconditionally. The step is nevertheless correct, because
`{W_C = h_C}` is determined by the Stage-1 bids at `C`, hence at `C`'s award round, which precedes
every Stage-2 pull at `C`, so the stopped martingale argument applies with that indicator inserted.
`E^H_C` is likewise award-time measurable. `H_C` is **not**, and the proof correctly avoids
multiplying a conditional expectation by it, using instead `A_q >= 0` and charging
`E[q tau_C 1_{H_C^c}] <= n Pr(H_C^c)`. All of this is right and none of it is written down. One
sentence.

### 15.4 The irreducibility claim of 17.4: right in substance, imprecise as stated

"This is not a measurability statement and no refinement of a filtration repairs it" is correct, and
so is "part (A) is false without exogeneity", which is my own Section 4.4 and which the author
re-derived. But the hypothesis the argument actually needs is not exogeneity. It is

> the arrival path is the **same** random sequence in the two coupled executions,

which is implied by exogeneity and is formally weaker. I looked for a genuinely weaker sufficient
condition and the natural candidate fails: "arrivals exogenous until every cube has completed Stage
1, reactive thereafter" preserves Fact 1 and (6.1), but it destroys the accounting, because `n_C`
then differs between the two executions and the comparison of `U'^post` with `n_C w_C` is between
two different numbers of pulls, a difference of order `n`. So the weakening I could construct does
not work, which supports the claim without proving it. The accurate sentence for the paper is
"part (A) requires that the deviation cannot move the arrival path, which exogeneity delivers and
which is necessary since part (A) is false otherwise", not "exogeneity is irreducible".

### 15.5 Two smaller things in the new material

**15.5a (P3). Lemma P1c is stated for every cube, but `beta_{j,C}` exists only at cubes that
complete bidding.** The proof is correct on `{C completes bidding}`, where `c_n = L_n` exactly and
`M_n = L_n(beta_{j,C} - Abar_{j,C})`; off that event the quantity is undefined. One clause.

**15.5b (P3). Lemma P7c's final sentence, "and the same holds conditionally on any field with
respect to which the fallback start is determined", is asserted and is now unused.** Part (C)
upgraded explicitly does not condition, which is the whole improvement; part (A) keeps (A4m) and
the original Lemma P7. The conditional version is plausible, since `F_fb subseteq G_u^{--}` for
every `u` after the switch and every step is a tower step, but it is not proved. Either prove it or
delete it, because an unused conditional claim in a lemma is exactly where the next reader will
build.

**15.5c (P3, interpretation not correctness). Under (A4c) the benchmarks become endogenous.** Parts
(B) and (C) compare revenue with `E sum_t M_(2)(X_t)` and `E sum_t b(X_t)`, and under reward
reactive arrivals those sums are random quantities that the mechanism's own outputs help determine.
The inequalities are still true and still meaningful as one sided guarantees, but "the mechanism
attains the second capacity" is a different sentence when the contexts at which the second capacity
is evaluated depend on what the mechanism did. The paper should say that it compares against the
realised path, not against a property of the environment.

## 16. Verdict of the second pass

The revision closes G2, G3, G4, G5, G6, G7 and G8, and closes G1 for parts (A) and (B). It opens
one new P1, H1, in the hypothesis that was introduced to close G1: (A4c) omits the mechanism's
randomisation, Lemma P7c uses that randomisation's freshness, and I give an instance satisfying
every clause of (A4c) on which Lemma P7c and Theorem 1C upgraded are false by `0.45 n`. One clause
repairs it and nothing else changes.

That makes three separate occasions on which this project has written an independence hypothesis as
a list of clauses and omitted a family that a proof then used: the finite documents' (H3) and (H4),
the continuous documents' (A3) and (A4), and now (A4c). The pattern is not carelessness about a
particular family; it is that the hypotheses are being assembled clause by clause rather than copied
from the manuscript's scalar phrasing, which quantifies over "everything realised before the seed"
and therefore cannot omit anything. **I would make it a standing rule on this project that every
probabilistic hypothesis in a contextual statement is written in the "conditionally on everything
determined before it" form, and that no hypothesis is written as a list of independences.** That
form is what (A4c) was reaching for and it is one word away: replace "conditionally on `G_u^{-}` the
seed `U_u` is uniform" by a clause that also covers the mechanism's own draws, or equivalently
define `G_u^{--}` to be generated by the arrival and require every subsequent draw at round `u` to
be conditionally fresh given it.

Beyond H1, I attacked the new fallback lemma in the way the coordinator asked, including the place
where tower steps replace optional stopping, and it held; I checked the EXP3 constant I had
previously declined to check and it is right; I enumerated every indicator multiplying a conditional
expectation in the new material and found one unstated but correct step and no error; and I
confirmed that the smaller deviation class is genuinely enough for parts (B) and (C) and that
neither proof quietly uses the larger one.

# THIRD PASS, on revision 3 of `PROVER2.md` (1540 lines)

**I am reporting minor items only.** Nothing in this pass changes a statement, a bound or a rate.
I attacked (A4f) with seven variants of H1 and could not break it; I checked the tower step that
replaces the assertion I broke and it is complete and correct; I checked the lemma-by-lemma
attribution table entry by entry and found it correct, with one harmless over-attribution; and I
checked the claim that nothing has quietly moved, which is true of the mechanism and of every rate
and is **not literally true of three bounds**, one of which is a real if repairable weakening. The
seven items below are all P3 and each has a one line or three line fix.

## 17. Is (A4f) genuinely sufficient?

### 17.1 The seven variants I tried, and why each closes

I attacked the conditional form rather than the sentence about it. In each case I ask what the
hypothesis actually forbids, not what the author intended.

| variant | what it does | outcome |
|:-|:-|:-|
| V1 | `X_u` a function of the round's **fallback selection coin** (my H1) | closed by (f2): given a field containing `X_u`, `I_u` is degenerate, so it does not have law `p_u` |
| V2 | `X_u` a function of the round's **priority draw** | closed by (f1) at round `u`, and vacuous anyway since (f1) is unused |
| V3 | `X_u` a function of the round's **seed** | closed by (f3): `U_u` is then `X_u`-measurable, not uniform given it |
| V4 | `X_u` a function of a **future** draw, at round `u' > u` | closed at round `u'`, because `X_u` is realised before `u'` and the draw at `u'` must be fresh given it. This is the author's remark 3 and I confirm it |
| V5 | `X_u` a function of the **selected agent's pre-drawn coin array** | permitted, and harmless: (f3) still holds, no proof needs the agent's coin to be fresh, and under `B^ctx` no agent learns anything it did not already have |
| V6 | the round's **selection correlated with the round's seed** | closed, and this is the structural gain of the chained form: `I_u ~ p_u` given `G_u^1` and `U_u` uniform given `G_u^-` together give `U_u` independent of `I_u` given `G_u^1`, which a list of pairwise clauses would not |
| V7 | `X_u` a function of a coin the mechanism would draw at `u` **only if the cube were in Stage 3**, with the path's own choice deciding the phase | closed, and this is the sharpest one: routing to a Stage-3 cube on that coin makes the round a Stage-3 round, at which (f2) bites; routing to a Stage-2 cube uses no selection randomness, so there is nothing to exploit |

I also re-ran the two path attacks that are specific to the fallback and do not go through a draw:
a path that routes into a cube only when that cube's EXP3 probability of the honest comparator is
at its floor, and a path that routes in heavy bursts. Both fail for the same structural reason, and
it is worth recording because it is the reason Lemma P7c is robust: **a cube's EXP3 state advances
only at that cube's own visits, so the arrival path chooses when in global time the local sequence
happens but cannot change the local sequence.** Lemma P7c's analysis is over the local sequence.

### 17.2 The one thing I would still change (P3): (A4f) enumerates draws, not channels

Remark 3 of 17.0 says the conditional form means "I do not have to enumerate the channels". That is
right, and it is the correct diagnosis of all three failures. But **(A4f) is still an enumeration:
it lists three draws, (f1), (f2), (f3).** What the conditional form removes is the enumeration of
*channels* through which a listed draw could be compromised. It does not remove the enumeration of
*draws*. A fourth draw added to the mechanism later, a randomised grid offset, a randomised tie
break inside the monitor, a random restart of a cube, would again be outside the hypothesis, and
the failure mode would recur in exactly the shape it has recurred three times.

I checked that the list is **complete for CG-MESP as written**, which is the thing that makes the
hypothesis sufficient today. `EXPLORER.md` is unchanged at 1291 lines, so Section 3 is the same
mechanism, and its only randomisations are the one priority permutation per cube, drawn at the
cube's first visit, and the Stage-3 selection `I_t ~ p`; everything else, the grid, the lazy
instantiation, the round-robin, the award rule, the price, the monitor test, the epoch schedule, the
weight update and the messages, is a deterministic function of state. Together with the seed and the
unconstrained agent randomisation, (f1), (f2), (f3) covers every draw. **So (A4f) is sufficient.**

The robust form is one clause and I would use it, because it is the form that cannot be outgrown:

> **(A4f')** At every round `u` the mechanism's own randomisations and the reward seed are drawn in
> the order the mechanism specifies, and **each such draw has its specified law conditionally on the
> sigma-field generated by everything realised before it**, that field containing all earlier rounds,
> the arrival `X_u`, and all draws already made at round `u`. The selected agent's randomisation and
> its target are unconstrained and are realised before the seed. For CG-MESP the mechanism's draws
> are the priority permutation at a cube's first visit and the Stage-3 selection.

The last sentence is then an instantiation and not the hypothesis, so adding a draw to the mechanism
cannot silently escape it.

### 17.3 A wording item (P3)

(A4f) says "conditionally on the sigma-field generated by everything realised before it, **that field
containing** `G_{u-1}`, the arrival `X_u`, and whichever of the draws below have already been made".
"Containing" is a lower bound on the field, so the displayed hypothesis is ambiguous between the
minimal field and any larger one. Sufficiency is unaffected, because a larger field makes the
hypothesis stronger and the proofs use the minimal one. But 17.0 already defines `G_u^{0}`,
`G_u^{1}`, `G_u^{2}`, `G_u^{-}`, so the clauses should be pinned to them: `Pi` uniform given
`G_u^{0}`, `I_u ~ p_u` given `G_u^{1}`, `U_u` uniform given `G_u^{-}`. One word, "being" for
"containing", plus the three field names.

## 18. The tower step that replaces the assertion I broke

This is the exact repair site and it is short enough to check completely, so I did.

The claim is `E[ 1{I_u = j} | G_u^{--} ] = p_{j,u}`, with `G_u^{--} = G_u^{0}`. The derivation is:
(f2) gives `I_u ~ p_u` conditionally on `G_u^{1}`; `p_u` is a function of the cube's own past
fallback data and of `X_u`, hence `G_u^{0}`-measurable; `G_u^{0} subseteq G_u^{1}`; so

    E[ 1{I_u = j} | G_u^{0} ]  =  E[ E[ 1{I_u = j} | G_u^{1} ] | G_u^{0} ]  =  E[ p_{j,u} | G_u^{0} ]
                               =  p_{j,u} .

**Correct.** Every hypothesis of the two steps is met: the inclusion `G_u^0 subseteq G_u^1` holds by
the definition in 17.0, `p_u` is `G_u^0`-measurable because the EXP3 weights at `C` are updated only
at `C`'s own past fallback visits and the cube identity comes from `X_u`, and the conditional law in
(f2) is stated at `G_u^1`, which is the field the tower step needs. The old assertion is named as
the defect at the point of use, which is the right place for it.

I also checked the two consequences drawn immediately after, because they are where the clause is
actually spent. `E[ hat Y_{j,u} | G_u^{0} ] = r_{j,u}` follows from
`E[ Y_u 1{I_u = j} | G_u^{0} ] = p_{j,u} r_{j,u}` with `p_{j,u}` measurable, and
`E[ sum_i q_{i,u} hat Y_{i,u}^2 | G_u^{0} ] <= sum_i (q_{i,u}/p_{i,u}) r_{i,u} <= K/(1 - gamma_k)`
uses `Y^2 = Y`, `p_i >= (1 - gamma_k) q_i` and `r_i <= 1`. Both correct, and both use (f2) through
the same tower step and nothing else. There is no third use of a mechanism draw in Lemma P7c.

## 19. The lemma-by-lemma attribution table

I checked every entry in the direction that matters, which is under-attribution: a lemma claimed not
to use a clause that it does use. That is how H1 survived two readings.

| entry | claim | verdict |
|:-|:-|:-|
| Fact 0, P2, P3, P4, P5(i), P5(ii) | nothing probabilistic | **correct**. Each is a pathwise consequence of `E_C`, of Lipschitz continuity or of honesty, and each holds for **whoever** is a largest bidder, so no property of the tie break enters |
| P1c, P5(iii) | (f3) only | **correct**. The Stage-1 indicator is `G_s^{0}`-measurable because the round-robin reads only `V_C`, and the martingale step is the seed |
| P6c | (f3) only | **correct**, and the subtle point survives: the Stage-2 indicator depends on the winner, hence on `Pi_C`, but `Pi_C` was drawn at `C`'s first visit and is therefore past data in `G_{s-1}`, not a draw at round `s`. No law of `Pi_C` is used |
| P7c | (f2) Stage-3 branch and (f3) | **correct**, and Section 18 above verifies the single place (f2) is spent |
| Part (B) | (f3) only | **correct**. I re-verified it independently of the parallel with (C): on `E_C cap H_C` no cube switches so Lemma P7 is never invoked; off that event the charge is `n_C` rounds at `M_(2) <= 1` per cube, which needs no property of the fallback at all. **Part (B) therefore holds even if the Stage-3 selection is adversarial**, which is a stronger statement than the text makes and is worth saying |
| Part (C) | (f2) and (f3) | **correct** |
| Part (A) | all of (A4f) plus the unmovable path | **over-attributed, harmlessly**. (f1)'s law is unused in part (A) too: the coupling uses the same `Pi_C` in the two executions, which is an identity on one space and not a statement about a law. Over-attribution is the safe direction |
| "(f1) is used nowhere in parts (B) and (C)" | | **correct**. I checked the one place a tie break could matter, part (C)'s case split on `W_C = h_C`: case (i) gives the better bound and case (ii) is the one the theorem uses, so any tie break, adversarial included, leaves the bound intact |

No under-attribution found.

## 20. Did anything quietly move? The precise answer

The author's summary is that no bound, statement or rate has moved across either revision, and that
every defect has been in a hypothesis, a conditioning field, or a sentence about the result, never
in the construction. I checked this because the coordinator wants to state it in the paper.

**True:** the mechanism has not changed. `EXPLORER.md` is byte-identical at 1291 lines, so Section
3's parameters, grid, three stages, monitor boundary, epoch schedule and proposed profile are the
same object that was proposed on 18 September. No rate has changed: every error term is still
`O(n^{(D+2)/(D+3)} log(eKn))` and part (D) is untouched. Part (A)'s statement has not changed.

**Not literally true:** three bounds moved, and the deviation class of part (C) shrank.

1. `6 n^{-3}` became `O(n^{-2})` in part (A) and `3 n^{-3}` became `O(n^{-2})` in (B) and (C), from
   D1. Restored by `ell_n := log(2 K n^6)`. Lower order, and disclosed.
2. `e_rob` improved from `n(4 s_n + (5/3) rho_n)` to `n(4 s_n + (4/3) rho_n)`, from D3. An
   improvement, and disclosed.
3. **`J'_n` became `min{J_n, n}` throughout the upgraded parts (B) and (C).** This is a genuine
   weakening and it is the only one I found. `J'_n`, the number of cubes the path actually visits,
   satisfies `J'_n <= min{J_n, n}`, and under exogeneity it is `F_0`-measurable so the original
   theorem could state the error in terms of it. Under (A4f) it is random, so 17.5 replaces it by
   the deterministic upper bound. The consequence, which is not stated, is that **the upgraded
   statements lose the path-adaptivity the original had**: `PROVER2.md`'s own Section 10.2 check (ii)
   and my Section 5.1 both record that a path concentrating in one cube gives `J'_n = 1` and makes
   the three bounds degrade gracefully to the scalar MESP rates. The upgraded (B) and (C) do not
   degrade at all; they carry `min{J_n, n} = Theta(n^{D/(D+3)})` on every path.

**The weakening is recoverable, by three lines.** The Cauchy and Schwarz bounds are pathwise
inequalities in the vector `(n_C)_C` with `J'_n` nonzero entries, so they may be taken in expectation
against the random `J'_n`, and concavity does the rest:

    E[ min{J'_n L_n, n} ]                          <=  min{ E[J'_n] L_n , n }
    E[ J'_n + 2 sqrt(J'_n n ell_n/2) ]             <=  E[J'_n] + 2 sqrt( E[J'_n] n ell_n/2 )
    E[ 11 sqrt(2 K J'_n n log K) ]                 <=  11 sqrt( 2 K E[J'_n] n log K )

the first because `x -> min{x L_n, n}` is concave, the second and third by Jensen for the square
root. So the upgraded parts (B) and (C) may be stated with `E[J'_n]` in place of `min{J_n, n}`,
which restores the adaptive form and is never worse, since `E[J'_n] <= min{J_n, n}`. I would make
that change, because the graceful degradation on a concentrated path is one of the more attractive
properties of the result and it is currently lost exactly where the arrival process is allowed to be
adversarial, which is where a referee will ask about it.

**The accurate sentence for the paper**, replacing the tripartite one, which is not exhaustive
(D1 is a union-bound count, D3 and D4 are constants, and neither is a hypothesis, a conditioning
field or a sentence about the result):

> Across three adversarial passes, no defect has required any change to the mechanism, and none has
> changed a rate. The defects have been in the hypotheses (three times, each an independence a
> proof used and the hypothesis did not grant), in the conditioning fields of four steps, in one
> union-bound count, in two constants, and in four sentences describing the result.

That is a stronger and more checkable claim than the one it replaces, and I believe it is true.

## 21. The remaining minor items

**21.1 (P3).** "No conditional expectation is taken anywhere in this proof", in Theorem 1B upgraded,
is loose: `P = E[ sum_t m_{I_t,t} ]` is a tower step and therefore is one. The intended and correct
claim is that no conditional expectation is ever multiplied by an indicator, which is the shape that
produced D2, G5 and, in a different form, H1. Reword.

**21.2 (P3, carried from my second pass and still unstated).** Lemma P6c's
`Pr(H^c) <= 2 J_n n e^{-ell_n} <= n^{-3}/K` and Lemma P1c's `Pr(E^c) <= 2 K J_n e^{-ell_n} <= n^{-4}`
both need `J_n <= n`, that is `n >= 2^{D(D+3)/3}`, which is about `10^{13}` at `D = 10`. It is
implied by the horizons of Section 18 in every case in that table, and it is a hypothesis of the
displayed bound that is not displayed. One clause.

**21.3 (P3).** The endogenous-benchmark paragraph at the end of 17.5 is right and well put. I add
one thing it does not say: under (A4f) the guarantee is a statement about the realised path, so the
two upgraded parts no longer compare two mechanisms on a common environment. If the paper ever
compares CG-MESP with Grid-ETC or Grid-UCB under the weakened hypothesis, the comparison is not
well posed, because the two mechanisms would face different realised paths. Under exogeneity it is.
One sentence, in the place where the comparison with `thm:grid-etc` is made.

## 22. Verdict of the third pass

**Minor items only.** Seven P3 items, listed in Sections 17.2, 17.3, 20 item 3, 21.1, 21.2, 21.3,
and the harmless over-attribution in Section 19. None of them changes a statement, a bound or a
rate; the one that comes closest, the `J'_n` substitution, weakens two upgraded bounds and I give
the three line repair that restores them and makes them no worse than what is there now.

On the coordinator's four questions, in order: **(1)** (A4f) is sufficient, and I say so on the
basis of having verified that its list of draws is complete for CG-MESP as written rather than on
the basis of the argument given for it, which proves something slightly weaker than it claims; the
robust restatement is in 17.2. **(2)** The tower step is correct and complete, and so are the two
consequences drawn from it. **(3)** The attribution table is correct, with one over-attribution in
the safe direction. **(4)** The summary is true of the mechanism and of every rate and is not
literally true of three bounds; the precise version is in Section 20 and I believe that version is
worth stating in the paper.

Three passes have now found three hypothesis defects, four conditioning-field defects, one counting
defect, two constants and four framing defects, and not one defect in the mechanism or in any rate.
I have no further attack to propose.
