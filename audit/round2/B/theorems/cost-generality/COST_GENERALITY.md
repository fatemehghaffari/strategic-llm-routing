# Cost generality audit

**Question.** Can the linear effort cost `m - mu_i` be replaced by a general cost, and what is the
weakest hypothesis under which every result in the paper survives?

**Scope.** `sections/sec2_model.tex`, `sec3_noisy.tex`, `sec4_contextual.tex`, `sec6_conclusion.tex`,
`appendix_samf.tex`, `appendix_public.tex`, `appendix_private.tex`, `appendix_contextual.tex`,
`app_contextual_private.tex`, `app_equilibrium.tex`. Read in full. Nothing outside
`audit/round2/B/theorems/cost-generality/` was written.

---

## 0. Headline

**Yes, with one hypothesis, and the hypothesis is exactly the one the application supplies.**

The right generalisation is

> per-pull utility `1 + phi_i(mu_i) - phi_i(m)`, effort cost `phi_i(m) - phi_i(mu_i)`,

with the **reward term unchanged** (no second change is needed), provided `phi_i` is normalised so that
its total range on `[0,1]` is at most the value of one selection. The paper's existing normalisation
(`per-pull utility in [0,2]`, which is `0 <= m - mu_i <= 1`) is exactly this condition, written for the
linear case.

Three findings, in order of importance.

1. **Convexity of `phi_i` is necessary and sufficient, and it is not a technical convenience.**
   The mechanism's monitor is a test on the *sum of delivered means*. It is blind, by construction and
   also information-theoretically, to how that sum is split across pulls. Under a **concave** cost an
   agent delivers mean `tau` by bang-bang (`M_i` a `tau/M_i` fraction of the time, `0` otherwise),
   producing an **observationally identical** Bernoulli stream at strictly lower cost, and gains a
   **linear** amount. So (H1) fails, and it fails against *any* mechanism in this observation model, not
   just MESP. Convexity is exactly the condition that makes the proposed profile's constant delivery
   cost-minimal. **The motivating application delivers convexity for free** (quality concave and
   saturating in compute ⇒ compute convex and increasing in quality), which turns the referee's
   objection into a strengthening.

2. **The Jensen step appears in exactly one of the three guarantees.** The revenue bound and the
   robustness bound live entirely in outcome/mean space and never touch `phi` at all: they are
   *verbatim* under (H1), (H2), (H3), and indeed under no hypothesis on `phi` whatsoever. Only the
   incentive bound has a Jensen step, and there the direction **helps** — it is the direction the proof
   needs, and reversing it is fatal. Likewise the **monitoring martingale is untouched** (confirmed,
   §3), the **fallback EXP3 lemmas are untouched**, and the **bid-domination step is untouched**.

3. **Lipschitzness is a second, independent requirement, and it does real work.** Convexity converts
   the monitor's mean-space slack `1 + 2b_n(q)` into a cost-space slack `q[phi(tau) - phi(tau - eps_q)]`;
   a Lipschitz constant converts that into `Lambda(1 + 2b_n(q))` and keeps the rate. Without it the
   rate genuinely degrades, with a witness (§4, row `thm:private-mesp(i)` under H2). (H3) *alone*,
   without convexity, fails by the same concave witness as (H1) — a Lipschitz concave cost is still
   concave.

**Recommendation.** Ship convexity + Lipschitz. It costs one paragraph in Section 2, one two-line lemma
in `appendix_private.tex`, and roughly 90 edited lines across the appendices. Do **not** ship (H1), and
do not ship (H3) alone.

---

## 1. The exact model assumption I would ship

Replace the two sentences in `sec2_model.tex` (lines 6-7 and line 21) by the following. I use `phi_i`
and not `c_i` because `c` is already the bid vector in `app_equilibrium.tex` and `c_{i,t}`/`C_i(n)` are
already the realised effort and its cumulative sum; a cost function called `c_i(.)` would collide with
`c = (c_1,...,c_K)` on nearly every page of `app_equilibrium.tex`.

> **Effort and cost.** Each agent `i` has a *cost function* `phi_i : [0,1] -> R` that is
> nondecreasing, convex, and `Lambda`-Lipschitz, normalised so that
> ```
>     phi_i(1) - phi_i(0) <= 1.                                       (N)
> ```
> Choosing target `m` when selected costs the agent `c_{i,t} := phi_i(m_{i,t}) - phi_i(mu_i)`, so a
> selection is worth `1 + phi_i(mu_i) - phi_i(m_{i,t}) in [0,2]`; effort may be negative. The linear
> model of the rest of this literature is `phi_i(m) = m`, for which `Lambda = 1` and (N) holds with
> equality.
>
> Honesty is unchanged and is a constraint on *delivered means*, not on costs: an honest agent never
> chooses `m_{i,t} < mu_i`. All benchmarks (`mu_H^star`, `M_(2)`, `b(X)`, `M_(2)(X)`) and the platform's
> revenue `P(n;S) = E sum_t m_{I_t,t}` are unchanged, being quantities in outcome space.

Three notes on the assumption, each of which I would put in the paper.

* **(N) is not cosmetic.** The proofs use "per-pull utility lies in `[0,2]`" and "an agent's utility in
  any phase is nonnegative" in at least a dozen places (`appendix_private.tex` l.138; `appendix_public.tex`
  l.12; `app_contextual_private.tex` l.~200 "We record the trivial pathwise facts"; `app_equilibrium.tex`
  (E2), the losing-branch charges, the `2n^{-2}` accounting). Without (N) the losing-branch discard
  ("baseline payoff is nonnegative") is false and the accounting collapses. If one insists on an
  unbounded cost range, the value of a selection must be raised to `R >= max_i (phi_i(1) - phi_i(0))`;
  then every `2` in an accounting charge becomes `R + max_i range_i` and every `kappa` becomes
  `R - max_i (phi_i(M_top) - phi_i(mu_i))`. I recommend against this: it buys nothing and re-costs
  every constant.
* **The reward term does not have to change.** This is the answer to the explicit sub-question. The
  only place the value `1` interacts with the cost is through `V_i <= 1 <= 1 + mu_i`
  (`appendix_private.tex` l.115), which generalises to `phi_i(V_i) <= 1 + phi_i(mu_i)`, i.e. exactly (N).
  Per-agent reward values `R_i >= range(phi_i)` would also work; a common `R = 1` is cleaner.
* **Convexity is WLOG, in a precise sense that strengthens the paper.** See Lemma A below. I would add
  it as a remark, because it pre-empts the referee who asks "why convex?".

### Lemma A (observational indistinguishability; new, two lines)

*Fix any mechanism that observes only `(I_t, Y_t)` with `Y_t | past ~ Bernoulli(m_{I_t,t})`. Let `pi` be
any distribution on `[0,M_i]` with mean `mbar`. Replacing agent `i`'s target draw `m ~ pi` at a pull by
the deterministic target `mbar` leaves the conditional law of `Y_t` — hence the law of the entire
observation process, hence every selection, price, switch time and the platform's revenue — unchanged,
while changing `i`'s cost at that pull from `E_pi[phi_i]` to `phi_i(mbar)`.*

*Proof.* `Y_t` is Bernoulli with parameter `E[m] = mbar` either way; a Bernoulli law is determined by its
mean. ∎

**Corollary A1.** The cheapest way for agent `i` to produce observable mean `mbar` is
`phihat_i(mbar)`, the lower convex envelope of `phi_i` on `[0,M_i]` (on `[mu_i, M_i]` if `i` is honest),
attained by a two-point mixture. Hence the model with cost `phi_i` is strategically equivalent to the
model with cost `phihat_i`, **for every mechanism in this observation class**: assuming convexity is
without loss of generality, up to replacing `phi_i` by `phihat_i`.

**Corollary A2 (the catch, and why (H1) is a genuine FAIL).** The equivalence of A1 changes the
*proposed profile*. Under a non-convex `phi_i` the strategic winner's cost-minimal way to meet the price
is a randomisation, not `min{tau, M_i}`. The paper's `S^star` as written
(`sec3_noisy.tex`: "A strategic primary winner delivers `min{tau, M_i}`") is then **not** a best response
and the equilibrium claim is false as stated. Repairing (H1) therefore means (a) redefining `S^star` to
be a mixed strategy, (b) turning the pathwise identities "its post-bid utility is **exactly**
`N_n(1 + mu_i - tau_i)`" (`appendix_private.tex` l.134; `app_contextual_private.tex` eq. `ctx-dev-post`
cancellation) into expectation identities, and (c) re-stating every appearance of `phi_i` as `phihat_i`.
That is a larger edit than adopting convexity and it makes the paper's own proposed profile randomised.
**Do not do it.** State Lemma A as a remark and assume convexity.

### The two structural constants

Two instance constants appear once convexity is assumed; both are `1` in the linear model.

```
  Lambda      := a Lipschitz constant for phi_i on [0,1]            (hypothesis)
  Lambda_eff  := max_i sup{ phi_i'(m) : m <= max relevant target }  (derived, if no Lambda assumed)
```
For a convex `phi_i` obeying (N), `phi_i'(m^-) <= (phi_i(1) - phi_i(m))/(1 - m) <= 1/(1-m)`, so
`Lambda_eff <= 1/(1 - M_(2))` in the scalar case and `Lambda_eff <= 1/(1 - max_x max{mu_i(x), M_(2)(x)})`
in the contextual case. This is the *only* place a general cost injects a new instance quantity, and it
is the reason I recommend assuming `Lambda` outright rather than deriving it.

### Lemma B (the one new lemma the appendix needs)

Every accounting step in the paper turns a *mean-space* lower bound delivered by the monitor or the
fallback into a *cost-space* lower bound. All of them are the same two lines. State it once in
`appendix_private.tex` and cite it everywhere.

> **Lemma B (cost of a monitored tenure).** Let `phi` be nondecreasing, convex and `Lambda`-Lipschitz on
> `[0,1]`.
> (a) If `m_1,...,m_q in [0,1]` and `sum_r m_r >= q*theta - Delta`, then
> `sum_r phi(m_r) >= q*phi(theta) - Lambda*Delta`.
> (b) If `pi` is any sub-probability measure of total mass `Qbar > 0` on `[0,1]` with
> `int m dpi >= Qbar*theta - Delta`, then `int phi dpi >= Qbar*phi(theta) - Lambda*Delta`.
>
> *Proof.* Jensen gives `sum_r phi(m_r) >= q phi((1/q) sum_r m_r)`, resp.
> `int phi dpi >= Qbar phi((1/Qbar) int m dpi)`; `phi` nondecreasing and `Lambda`-Lipschitz gives
> `phi(theta - Delta/q) >= phi(theta) - Lambda*Delta/q`. Trivial for `q = 0`. ∎

Every accounting step is then "apply Lemma B with `(theta, Delta) = (tau_i, 1 + 2b_n(q))`" (the monitor)
or "`(V_i, R_K(H))`" (the fallback). This is what makes the edit mechanical rather than a rewrite.

---

## 2. Verdict table

Columns are the three hypothesis classes **exactly as posed**:

* **(H1)** `phi_i` increasing and bounded on `[0,1]` (I read "bounded" as (N); if bounded by some
  `B > 1` instead, every entry below additionally loses the `[0,2]` range and the nonnegativity of
  per-phase utility, which is worse, not better).
* **(H2)** `phi_i` increasing, convex, bounded. Note: convex on `[0,1]` implies continuous on `[0,1)`,
  so the only discontinuity (H2) admits is an upward jump at `m = 1`, and that jump is real and matters
  (rows `thm:contextual-public`, `thm:grid-ucb-robust`).
* **(H3)** `phi_i` increasing and `Lambda`-Lipschitz. **Not convex.**

`verbatim` means the statement and every constant are unchanged after the substitution
`1 + mu_i - m  ->  1 + phi_i(mu_i) - phi_i(m)`, with no new hypothesis and no new constant.

### 2.1 Model and definitions (`sec2_model.tex`)

| Object | H1 | H2 | H3 |
|---|---|---|---|
| `def:restricted-equilibrium`, additive behavioural equilibrium | verbatim | verbatim | verbatim |
| strategy classes `S_HI`, `B_{i,n}`, `S_HDS`, `S_F`, `B^ctx_{i,n}` | verbatim | verbatim | verbatim |
| honesty (`m_{i,t} >= mu_i`) | verbatim (**must stay in mean space**, see §6) | verbatim | verbatim |
| benchmarks `mu_H^star`, `M_(2)`, `b(X)`, `M_(2)(X)`; revenue `P(n;S)` | verbatim | verbatim | verbatim |
| per-pull utility range `[0,2]`; "two executions differ by at most `2n`" | verbatim under (N) | verbatim under (N) | verbatim under (N), or `[0, 1+Lambda]` without (N) |

**The equilibrium notion does not depend on linearity.** `u_i(n;S) = E[T_i(n) - C_i(n)]` and the `o(n)`
comparison are unchanged in form. The notion needs only that per-pull utility be `O(1)`, which is (N);
without (N) the `o(n)` slack could be swamped and the definition would become vacuous. Nothing in the
definition refers to the shape of `phi`.

### 2.2 Public / SAMF results

| Result | H1 | H2 | H3 |
|---|---|---|---|
| sharp adaptivity (definition, `sec3_noisy.tex`) | **must be restated**: replace `E[C_i(n)]` by `E[Delta_i(n)] := E sum_{t: I_t=i}(m_{i,t} - mu_i)` | same | same |
| `thm:sharp-robustness` | verbatim *after* the restatement above | verbatim | verbatim |
| `thm:scalar-ucb` sharp adaptivity | verbatim after restatement | verbatim | verbatim |
| `thm:scalar-ucb` monotonicity, FATA; `lem:race`; `lem:ucb-deficit`; `rem:anytime` | verbatim | verbatim | verbatim |
| `thm:public-ucb` (public restricted equilibrium + revenue) | verbatim | verbatim | verbatim |
| `thm:separation` (one observation certifies nothing) | verbatim | verbatim | verbatim |

*Why `thm:sharp-robustness` needs the restatement.* `appendix_samf.tex` l.49 reads "Since
`c_{i,t} = m_{i,t} - mu_i`, the revenue identity `P(n;S) = sum_i (E[C_i(n)] + mu_i E[T_i(n)])` holds".
That identity is **false** for any nonlinear `phi`. The fix is not to patch the proof but to notice that
sharp adaptivity was never a statement about cost: it is a statement about delivered-mean shortfall,
which happens to coincide with cost under linearity. Restating it in mean space makes
`thm:sharp-robustness` cost-free, which is correct — it is a revenue theorem. Same three-word fix in
`appendix_contextual.tex` ("Using `c_i = m_i - mu_i` converts this deficit bound to contextual sharp
adaptivity", twice, plus the `c_i(z) = b(z) - mu_i(z_i) - (b(z) - m_i(z))` line).

*Why `thm:public-ucb` is verbatim even under (H1).* The declared class `S_HI` is **deterministic and
horizon-independent**: an agent picks one mean and uses it always. There is no per-pull splitting, so
there is no Jensen step, and a fixed deviation `m' < M_top` receives `O(log n)` pulls at utility at most
`2` each. This is worth stating in the paper: it is the one incentive result that survives an arbitrary
increasing cost, and it survives because of the *class*, not the cost.

### 2.3 Private scalar mechanism (`appendix_private.tex`, `sec3_noisy.tex`)

| Result | H1 | H2 | H3 |
|---|---|---|---|
| `lem:private-monitor` (a): `Pr{exists r: |Z_r - A_r| > b_n(r)} <= n^{-3}`; `A_q >= q tau - 1 - 2b_n(q)`; false-switch bound | verbatim | verbatim | verbatim |
| `lem:private-monitor`, utility clause `U_i^pri <= q(1+mu_i-tau)+1+2b_n(q)` | **FAILS**: witness W1/W2 | constants change: `1+2b_n(q) -> Lambda_eff (1+2b_n(q))` | **FAILS**: witness W2 |
| `lem:selected-reactive-exp3` | verbatim | verbatim | verbatim |
| bid domination (`beta'_i <= beta_i^max`, price identity `tau_i`, Stage-1 charge `<= L_n`) | verbatim | verbatim | verbatim |
| eq. `private-fallback-core` (`V_i H - R_K(H) <= Abar_i + V_i(H - Qbar_i)`) | verbatim | verbatim | verbatim |
| eq. `private-fallback-top` (`E[U^fb] <= (1+mu_i-V_i)H + R_K(H)`) | **FAILS** | constants change: `R_K(H) -> Lambda_eff R_K(H)` | **FAILS** |
| `thm:private-mesp` (i) equilibrium | **FAILS: linear, witness W1/W2** | constants change: `L_n + Lambda_eff(1+2b_n(n)+R_K(n))`; **rate not preserved in the worst case, witness W3** | **FAILS: linear, witness W2** |
| `thm:private-mesp` (ii) revenue `>= M_(2) n - O(.)` | verbatim | verbatim | verbatim |
| `thm:private-mesp` (iii) robustness `>= mu_H^star n - O(.)` | verbatim | verbatim | verbatim |
| `prop:tightness` (elicitation term attained) | order preserved, constant `M_i - m' -> phi_i(M_i) - phi_i(m')`; **needs `phi_i` strictly increasing** | same | same |
| `prop:noisy-tight`, monitoring half | order preserved, constant `-> lambda_i := inf phi_i'` near `tau`; needs `lambda_i > 0` | same | same |

**Under (H2) AND (H3) together** (convex + Lipschitz, the recommended ship): `thm:private-mesp`(i)
holds with `L_n + Lambda(1 + 2b_n(n) + R_K(n)) + O(1) = O_{K,Lambda}(n^{2/3}(log n)^{1/3})`, rate
preserved, and the sentence "uniform ... over all scalar instances with `K` agents; no capacity gap
enters it" survives with `Lambda` in place of `1`.

**Under (H2) alone** that uniformity sentence becomes **false** and must be qualified: the bound carries
`Lambda_eff <= 1/(1 - M_(2))`, an instance quantity.

### 2.4 Contextual private, finite profiles (`app_contextual_private.tex` §app:ctx-private-finite)

| Result | H1 | H2 | H3 |
|---|---|---|---|
| `lem:ctx-locality` | verbatim | verbatim | verbatim |
| `lem:ctx-monitor` (a),(c),(d),(e) | verbatim | verbatim | verbatim |
| `lem:ctx-monitor` (b), utility half | **FAILS** | `Lambda_eff` | **FAILS** |
| `lem:ctx-fallback` (prefix EXP3) | verbatim | verbatim | verbatim |
| `lem:ctx-bid` (a)-(e) | verbatim | verbatim | verbatim |
| `prop:ctx-finite-exact` (i), **losing branch** | verbatim | verbatim | verbatim |
| `prop:ctx-finite-exact` (i), **non-top winning branch** (eq. `ctx-nontop-profile`, `D_i(z)`, tenure bound `ctx-nontop-tenure`) | **verbatim** — this branch is pure mean-space plus the `[0,2]` range | verbatim | verbatim |
| `prop:ctx-finite-exact` (i), **top winning branch** (eq. `ctx-top-profile`, `ctx-dev-post`) | **FAILS: linear** | `1 + 2b_n(N_z) + R_K(n) -> Lambda_eff(.)` | **FAILS** |
| `prop:ctx-finite-exact` (ii) revenue | verbatim | verbatim | verbatim |
| `prop:ctx-finite-exact` (iii) robustness | verbatim | verbatim | verbatim |
| `prop:ctx-finite-tight` | order preserved, `c -> c_phi := min_z(phi_i(M_i^z) - phi_i(m'(z)))`; needs strict increase | same | same |
| `rem:ctx-finite-no-two-top`, `rem:ctx-finite-exogeneity` | verbatim | verbatim | verbatim |

The localisation is worth stating: under (H1) the **only** thing that breaks in the whole finite-profile
theorem is the top winning branch. The non-top branch survives an arbitrary increasing cost because its
tenure bound comes from `A^z_q <= M_i^z q` (feasibility, mean space) and its utility charge is the crude
`2q` (range). This is a good sanity check that the Jensen step is correctly localised.

### 2.5 Contextual private, continuum (`app_contextual_private.tex` §app:ctx-private-continuum)

| Result | H1 | H2 | H3 |
|---|---|---|---|
| `lem:ctx-osc`, `lem:ctx-bidconc` | verbatim | verbatim | verbatim |
| `lem:ctx-price-meet`, `lem:ctx-price-dom`, `lem:ctx-price-second`, `lem:ctx-honest-floor` | verbatim | verbatim | verbatim |
| `lem:ctx-monitor-cont` (a),(b),(d),(e) | verbatim | verbatim | verbatim |
| `lem:ctx-monitor-cont` (c), utility clause | **FAILS** | `Lambda_eff` | **FAILS** |
| `lem:ctx-fallback-cont` (doubling EXP3) | verbatim | verbatim | verbatim |
| `lem:ctx-dev-fallback` | **FAILS** | constants: `R^dbl_K(H) + rho_n H/3 -> Lambda_eff(R^dbl_K(H) + rho_n H/3)` | **FAILS** |
| `prop:ctx-continuum-exact` (i) | **FAILS: linear** | constants: `e_osc + e_mon + e_fb -> Lambda_eff(.)`; **and (H2) alone is insufficient unless `max_x max_i max{mu_i(x), M_(2)(x)} <= 1 - zeta`** | **FAILS** |
| `prop:ctx-continuum-exact` (ii) revenue | verbatim | verbatim | verbatim |
| `prop:ctx-continuum-exact` (iii) robustness | verbatim | verbatim | verbatim |
| `thm:ctx-private-continuum`, rate `n^{(D+2)/(D+3)}` | FAILS | preserved iff `Lambda_eff` finite; else degrades | FAILS |
| `rem:ctx-endogenous`, `rem:ctx-continuum-exogeneity`, `rem:ctx-horizons` | verbatim | verbatim | verbatim |
| `thm:ctx-net-separation` (A) | **FAILS** | `Lambda_eff` on `e_mon`, `e_1fb`, `e_net` | **FAILS** |
| `thm:ctx-net-separation` (B),(C) | verbatim | verbatim | verbatim |

**The continuum result needs Lipschitz more essentially than the scalar one.** Its oscillation charge
`e_osc = n rho_n` comes from `mu_i^sup(C) - mu_i^inf(C) <= omega`, a *mean-space* oscillation that has to
be converted to cost space: `phi_i(mu_i^sup(C)) - phi_i(mu_i^inf(C)) <= Lambda omega`. Convexity says
nothing about this. Since the continuum results *already* assume `mu_i, M_i` are `L`-Lipschitz in the
context, assuming `phi_i` is `Lambda`-Lipschitz in `m` is entirely in keeping and costs nothing
rhetorically.

### 2.6 Contextual public (`appendix_contextual.tex`)

| Result | H1 | H2 | H3 |
|---|---|---|---|
| `lem:cell-law`, `lem:region`, `lem:etc-tail`, `lem:cell-average-l1` | verbatim | verbatim | verbatim |
| `thm:finite-context` sharp adaptivity, monotonicity, FATA, robustness | verbatim after the mean-space restatement of sharp adaptivity | same | same |
| `thm:finite-context` public equilibrium | verbatim (class `S_F` is deterministic **and horizon-independent**) | verbatim | verbatim |
| `thm:grid-ucb-robust` monotonicity, FATA, revenue | verbatim | verbatim | verbatim |
| `thm:grid-ucb-robust` equilibrium; `thm:contextual-public` equilibrium | **FAILS if `phi_i` is discontinuous at `M_i`: witness W4.** Survives as `o(n)` for continuous `phi_i`, but the **rate `E_n` changes** to `n * omega_phi(c_1 q_n^{-1/2}) + (existing terms)` | **FAILS: witness W4** (a jump at `m = 1` is convex-admissible) | **verbatim rate, constants `c_1 q_n^{-1/2} + eta_{i,C} -> Lambda(.)`** |
| `thm:grid-etc` all parts | verbatim after restatement | verbatim | verbatim |
| `prop:two-top-sharp`, positive half | constant `g_0 nu(A)/32 -> lambda g_0 nu(A)/32`, needs `lambda := inf phi_i' > 0` | same | same |
| `prop:two-top-sharp`, converse half | same as `thm:contextual-public` equilibrium row | same | same |

**This is the one row where (H3) beats (H2)**, and it is instructive. In the contextual public setting
the deviation class `S_HDS` is a *map*, so an agent can shade at some contexts of a cell and not others.
The proof never Jensens: it bounds the gain by `E[N_C] p'_{i,C} delta_C^phi` and controls `p'_{i,C}`
through the *mean* gap `delta_C`. What it needs is a bound on the **chord slope**
`(phi(M_i) - phi(m))/(M_i - m)`, i.e. precisely Lipschitzness, and not convexity at all.

### 2.7 Equilibrium selection and collusion (`app_equilibrium.tex`)

| Result | H1 | H2 | H3 |
|---|---|---|---|
| nondegeneracy (ND) `M_top < 1`, `kappa = 1 - M_top` | **restate** as `(ND_phi)`: `kappa_phi := 1 - max_i (phi_i(M_top) - phi_i(mu_i)) > 0` | same | same |
| family `Sigma` of elicitation profiles, conditions (A)/(B) | verbatim (they are conditions on *bids*, i.e. on means) | verbatim | verbatim |
| `prop:mesp-equilibrium-set`, **sufficiency** | **FAILS** (inherits the `thm:private-mesp` failure) | constants: `L_n + Lambda_eff(1+2b_n(n)+R_K(n))`; case 2a's `N_n s_n -> Lambda_eff N_n s_n` | **FAILS** |
| `prop:mesp-equilibrium-set`, **necessity** ((E1) winning value, (E2) losing value) | `kappa -> kappa_phi` throughout; otherwise verbatim | same | same |
| `prop:mesp-equilibrium-set`, revenue formula `nu(c)` | verbatim | verbatim | verbatim |
| `cor:mesp-revenue-range` | verbatim | verbatim | verbatim |
| `cor:mesp-price-setter` | constant: `L_n(M_(2) - c'_k) -> L_n(phi_k(M_(2)) - phi_k(c'_k))`; revenue statement verbatim | same | same |
| `rem:mesp-reading` | "sublinear stake" argument verbatim; `kappa -> kappa_phi`; `(1/K_top) N_n (1 + mu_i - M_top) -> (1/K_top) N_n (1 + phi_i(mu_i) - phi_i(M_top))` | same | same |
| `prop:mesp-pairs` (i) | `(M_(2) - theta)_+ N_n -> (phi_W(M_(2)) - phi_W(theta))_+ N_n`; error `O(ns_n + sqrt(n log n)) -> O(Lambda(.))` | same | same |
| `prop:mesp-pairs` (ii) | `(1/2)N_n(M_top - theta) + L_n(M_top - theta) -> (.)(phi(M_top) - phi(theta))`; `kappa -> kappa_phi` | same | same |
| `prop:mesp-pairs` (iii) | `kappa -> kappa_phi`; logic verbatim | same | same |
| `lem:no-punishment` (no punishment technology) | verbatim; "strictly exceeds" weakens to "is at least", which is all the proof uses | verbatim | verbatim |
| `prop:plmesp-equilibrium-set` (i) | **FAILS** | `Q(1+R_K(n)) + sqrt(2Qn l_n) -> Lambda_eff(.)`; `QL_n` and `2 Viol(c)` verbatim | **FAILS** |
| `prop:plmesp-equilibrium-set` (ii),(iii) | `kappa -> kappa_phi`; otherwise verbatim | same | same |
| `cor:plmesp-revenue`, `rem:plmesp-frequency` | verbatim | verbatim | verbatim |
| `prop:plmesp-pairs` (i),(ii),(iii) | rate constants inherit `Lambda_eff`/`kappa_phi`; structure verbatim | same | same |
| `rem:concession-inversion`, `rem:ctx-collusion-honest` | verbatim | verbatim | verbatim |

**The separation of scales survives, which answers sub-question 4 directly.** The equilibrium
characterisation compares a Stage-1 stake against a primary-phase stake:

```
  elicitation stake at a profile   =  L_n (phi_i(M_i) - phi_i(c_i))  <=  L_n * 1  =  o(n)      [by (N)]
  primary stake                    >=  kappa_phi * N_n               =  Theta(n)   [by (ND_phi)]
```
Both scales are preserved under any `phi` obeying (N) and `(ND_phi)`. The sublinearity of the
elicitation stake is a consequence of (N) alone, not of linearity: no cost function with bounded range
can make one `L_n`-block of pulls worth a linear amount. The characterisation (A)/(B) itself is a
statement about bids, hence about means, hence untouched. **The entire equilibrium-selection story,
including the price-setter corollary, the pair results and the no-punishment lemma, is structurally
immune to the change of cost; only numerical constants move.**

---

## 3. The four suspected trouble spots, answered by name

### (1) The Jensen step: where it is, which direction, and whether it helps or hurts

There is **exactly one** such step in the paper, and it occurs in only one of the three guarantees.

**Where.** The monitor and the fallback both produce a lower bound on a *sum (or expectation) of chosen
means*:

```
  monitor  (lem:private-monitor, lem:ctx-monitor(b), lem:ctx-monitor-cont(b)):
        A_q = sum_{r<=q} m_r  >=  q*tau - 1 - 2 b_n(q)                   [pathwise on the good event]
  fallback (eq. private-fallback-core, lem:ctx-dev-fallback):
        Abar_i                 >=  V_i * Qbar_i - R_K(H)                 [in conditional expectation]
```
Both are then converted to the agent's utility, and in the linear model the conversion is the *identity*
`U^pri = q(1 + mu_i) - A_q`. Under a general cost the conversion needs a lower bound on
`sum_r phi_i(m_r)` from a lower bound on `sum_r m_r`, and that is an exchange of "cost of an average"
for "average of costs".

**Direction.** The proof needs
```
        (1/q) sum_r phi_i(m_r)  >=  phi_i( (1/q) sum_r m_r ),
```
which is **exactly Jensen for a convex `phi_i`**. So convexity **helps**: it is the direction the proof
needs. Concavity **hurts, fatally**, and the exact size of the damage is
`q * [phi_i(mbar) - phihat_i(mbar)]`, the gap between `phi_i` and its convex envelope, times the tenure.
With `q = Theta(n)` that is a linear loss.

**Separately, for each bound.**

* **Incentive bound.** The step is present, the direction helps, and reversing it is fatal. Witnesses
  W1, W2 below.
* **Revenue bound** (`thm:private-mesp`(ii), `prop:ctx-finite-exact`(ii), `prop:ctx-continuum-exact`(ii),
  `thm:ctx-net-separation`(B)). **The step is not present at all.** Revenue is `E sum_t m_{I_t,t}`; the
  proofs lower-bound `m_r >= tau` pathwise from the definition of `S^star` and `lem:ctx-price-meet`. No
  cost function appears in these proofs at any point. (The `E sqrt(N_z) <= sqrt(E N_z)` steps in the
  error accounting are Jensen in the *visit count*, not in the cost, and are unrelated.)
* **Robustness bound** (`thm:private-mesp`(iii), `prop:ctx-finite-exact`(iii),
  `prop:ctx-continuum-exact`(iii), `thm:ctx-net-separation`(C)). **The step is not present at all.** The
  honest agent's bid floor is a supermartingale bound on its own *targets*; the price comparison
  `beta_(2) >= beta_h` is in bid space; the monitor's `A_q >= q tau - 1 - 2b_n(q)` is used directly as a
  *target-sum* bound, which is what revenue is; the fallback comparator's guarantee is a conditional
  *mean*. Nothing is ever converted to cost.

So the user's worry — "a step harmless in one may be fatal in another" — is correct in spirit, but the
truth is sharper: the step *exists* in only one of the three, and there it is fatal if reversed.

**Secondary Jensen-adjacent issue.** The `S_HDS` / `S_F` contextual public classes allow an agent to
vary its target across contexts *within a cell*, which is the same splitting phenomenon in a different
guise. There, however, the proof routes through the commitment probability and needs a chord-slope
(Lipschitz) bound, not convexity. See row 2.6 and witness W4.

### (2) Is the monitoring martingale untouched? — **CONFIRMED, entirely untouched**

The monitor lives in outcome space and is unaffected by any change of cost. Explicitly:

* `lem:private-monitor` first claim: `Z_r - A_r` is a martingale with increments `Y_q - m_q` of
  conditional range `1`; Azuma at `b_n(r)`; union bound. **No cost anywhere.**
* `lem:ctx-monitor` (a),(c),(d),(e) and `lem:ctx-monitor-cont` (a),(b),(d),(e): identical; the
  predictability of `psi^z_s` is about phases and arrivals, the increment bound is about Bernoulli
  outcomes.
* `lem:ctx-bidconc` (predictable bid concentration): a martingale on `Y_s - m_{I_s,s}`. **No cost.**
* The `A_q >= q tau - 1 - 2 b_n(q)` conclusion (`lem:private-monitor`, `lem:ctx-monitor`(b) first half,
  `lem:ctx-monitor-cont`(b)) is a statement about the **target sum**. Untouched.

Only the **utility clauses** attached to these lemmas touch cost, namely
`lem:private-monitor`'s `U_i^pri <= q(1 + mu_i - tau) + 1 + 2b_n(q)`, `lem:ctx-monitor`(b) second half,
and `lem:ctx-monitor-cont`(c). Those are exactly the Lemma-B applications. **Refutation of nothing; the
suspicion is confirmed and it is the paper's good luck.**

The same verdict holds for the **fallback lemmas**: `lem:selected-reactive-exp3`, `lem:ctx-fallback`,
`lem:ctx-fallback-cont` are pure outcome-space EXP3 regret statements and are verbatim. Only their *use*
in `eq:private-fallback-top` and `lem:ctx-dev-fallback` needs Lemma B.

And for the **bid-domination step**: `Y' = 1{U <= m'} <= 1{U <= M_i} = Y^max` is a coupling of
outcomes; `lem:ctx-bid`(a)-(d) and `eq:ctx-win-inclusion` are verbatim. `lem:ctx-bid`(e) charges the
Stage-1 utility difference per pull, which becomes `phi_i(M_i^z) - phi_i(m'_{i,t}) in [0,1]` by (N) —
**verbatim, same constant**.

### (3) Tightness: do the lower bounds keep the same ORDER?

**Yes for the order; no for the matching constants.** The tightness claim weakens from "attained" to
"attained up to the condition number of `phi`".

* **`prop:tightness` (elicitation, scalar).** The coupling argument is untouched; on the good event the
  two executions' post-bid histories coincide pathwise and the utilities differ exactly by the Stage-1
  effort saving, which is now `L_n (phi_i(M_i) - phi_i(m'))` instead of `L_n(M_i - m')`. Same order
  `Theta(L_n) = Theta(n^{2/3}(log n)^{1/3})` **provided `phi_i(M_i) > phi_i(m')`**. Under a merely
  *nondecreasing* `phi_i` that is constant on `[(M_i+V_i)/2, M_i]`, the deviation saves **nothing** and
  the elicitation term is **not** attained. So the proposition needs a strict-increase hypothesis, which
  the linear model gets for free. Note the deviation cannot be improved by bang-bang in Stage 1 under a
  convex `phi_i` (Jensen again), and its saving is capped at `L_n` by (N) in any case.
* **`prop:ctx-finite-tight`.** Same: `c -> c_phi := min_z (phi_i(M_i^z) - phi_i(m'(z))) > 0`, gain
  `>= c_phi Q L_n - 4Qn^{-3}`. Order `Theta(QL_n)` preserved, so the sharpness of the
  `Q = o(n^{1/3}(log n)^{-1/3})` restriction is preserved.
* **`prop:noisy-tight`, monitoring half.** The deviator tracks the boundary from below with total mean
  shading `Omega(sqrt(n log n))`. Its cost saving is `sum_r [phi(tau) - phi(tau - delta_r)] >=
  lambda_i * Omega(sqrt(n log n))` where `lambda_i := inf{ phi_i'(m) : m near tau }`. Order preserved
  **provided `lambda_i > 0`**.
* **The constants separate.** The upper bound uses `phi(tau) - phi(tau - eps) <= Lambda eps`; the lower
  bound uses `>= lambda eps`. So the matching is now up to the ratio `Lambda / lambda`, the condition
  number of `phi_i` on the relevant range. In the linear model `Lambda = lambda = 1` and the two agree.
  The paper's own sentence "the `L_n` term ... is attained by MESP as specified up to the instance factor
  `M_i - m'`" already carries an instance factor, so this is a change of kind only for the monitoring
  half, where the current statement carries no instance factor at all and the general one does.
* **Under (H2) without Lipschitz on an instance with `M_(2) = 1`, tightness is LOST**, not merely
  weakened: the upper bound degrades to `Theta(n^{1/2 + (1-alpha)/3})` (witness W3) while the lower
  bound stays at `Omega(sqrt(n log n))`, a gap of order `n^{(1-alpha)/3}`. Actually W3 shows the *upper*
  bound is attained at the degraded rate, so the honest statement is that the **theorem's rate**, not
  the tightness, is what is lost there.

### (4) Sublinear elicitation cost vs linear primary gain — does the separation survive?

**Yes, verbatim, and it survives for a reason that has nothing to do with linearity.** See §2.7. The
elicitation stake at any profile is `L_n (phi_i(M_i) - phi_i(c_i)) <= L_n` by (N) alone; the primary
stake is `>= kappa_phi N_n`. The only change is `kappa -> kappa_phi` in `(ND)`. The qualitative
characterisation (cases (A) and (B)), the revenue formula `nu(c)`, `cor:mesp-revenue-range`, the
price-setter corollary and the collusion results are all statements about bids and prices, i.e. about
means, and are untouched. This is the most robust part of the paper under a change of cost.

### (5) Where the range `[0,2]` is used

Every such use is verbatim under (N), because (N) is exactly the statement that the range is preserved.
Inventory of the uses I found:

| Location | Use |
|---|---|
| `sec2_model.tex` l.21 | the statement itself |
| `appendix_public.tex` l.12 | "obtains `O(log n)` utility because utility per pull lies in `[0,2]`" |
| `appendix_private.tex` l.138 | "bad events cost at most twice their probabilities times `n`" |
| `appendix_private.tex` `prop:tightness` proof | "Off `E` the utilities differ by at most `2n`" |
| `app_contextual_private.tex` "trivial pathwise facts" paragraph | `[0,2]` and nonnegativity of any phase's utility |
| `app_contextual_private.tex` non-top branch | `U'^pri <= 2q`, `U'^fb <= 2 Qbar_i` |
| `app_contextual_private.tex` `prop:ctx-continuum-exact`(i) | `0 <= w_C <= 2`, `2 n_C Pr(.)` |
| `app_contextual_private.tex` `prop:ctx-finite-tight` proof | "Off `E` the utilities differ by at most `2n`" |
| `app_equilibrium.tex` (E2), case-analysis charges | `<= 2L_n + 1`, `2n^{-2}`, `2 Viol(c)` |
| `app_equilibrium.tex` `cor:mesp-price-setter` proof | "off that event the difference is at most `2n`" |
| `app_equilibrium.tex` `lem:no-punishment` | `O(V_z n^{-2})` charges |

Without (N) each `2` becomes `1 + max_i(phi_i(1) - phi_i(0))`, and, worse, the *nonnegativity* of a
phase's utility fails, which kills the discard of the losing branch in every one of the private proofs.
(N) is therefore load-bearing and should be stated as part of the model, not derived.

---

## 4. Counterexamples for every FAILS entry

All four are explicit, small, and checked numerically (`Bash` transcript in this session; the arithmetic
is reproduced inline below so it can be checked by hand).

### W1 — (H1) fails for `thm:private-mesp`(i): concave cost, linear gain

**Instance.** `K = 2`. Agent 1 strategic with `M_1 = 0.9`, `mu_1 = 0`. Agent 2 honest with
`M_2 = mu_2 = 0.5` (honest, and it always delivers exactly `0.5`). Honest set nonempty.
`M_top = 0.9 < 1`, so `(ND)` holds with `kappa = 0.1`. `V_1 = M_(2) = 0.5`.

**Cost.** `phi(m) = sqrt(m)` for both agents. Increasing, bounded, `phi(0) = 0`, `phi(1) = 1`, so (N)
holds with equality. **Concave**, so (H1) is satisfied and (H2) is not.

**Baseline `S^star`.** On the good event agent 1 wins the elicitation and the announced price is
`tau = (beta_(2) - s_n)_+ -> 0.5`. Agent 1's baseline primary target is `min{tau, M_1} = tau = 0.5`, at
per-pull utility
```
   1 + phi(0) - phi(0.5) = 1 - 0.70711 = 0.29289.
```

**Deviation.** Agent 1 bids `M_1 = 0.9` in Stage 1 (identical to baseline, wins identically), and in the
primary phase delivers `m_r = 0.9` on a `5/9` fraction of pulls and `m_r = 0` otherwise, interleaved
deterministically so that `A_r >= r tau` for every `r`. Because `m_r in {0, 0.9}` the outcomes are
`Y_r ~ Bern(m_r)`, `E[Y_r] = 0.5`, and `Z_r - A_r` is the same martingale as in the baseline; the
false-switch probability is the paper's own `(2n^3)^{-1}`. (If one prefers an exactly
indistinguishable deviation, randomise `m_r in {0, 0.9}` i.i.d. with `P(m_r = 0.9) = 5/9`; then `Y_r` is
i.i.d. `Bern(0.5)`, **exactly** the baseline observation law — Lemma A.)

**Cost per primary pull under the deviation.**
```
   (5/9) phi(0.9) + (4/9) phi(0) = 0.55556 * 0.94868 = 0.52705,
   per-pull utility = 1 - 0.52705 = 0.47295.
```

**Gain.** `0.47295 - 0.29289 = 0.18006` per primary pull, over `N_n >= n/2` primary pulls:
```
   gain >= 0.0900 n.
```
Linear. `thm:private-mesp`(i) asserts `O_K(n^{2/3}(log n)^{1/3})`. **Contradiction.**

**What is untouched.** The deviator still delivers mean `0.5` per pull, so the platform's revenue is
unchanged and `thm:private-mesp`(ii) and (iii) are unaffected. The failure is exclusively in the
incentive bound.

### W2 — (H3) fails for `thm:private-mesp`(i): Lipschitz is not enough

Same instance as W1. **Cost** `phi(m) = min{2m, (1+m)/2}` for both agents: increasing, `phi(0) = 0`,
`phi(1) = 1` so (N) holds, **`2`-Lipschitz** so (H3) holds with `Lambda = 2`, and **concave** so (H2)
fails.

```
   baseline per-pull utility  = 1 - phi(0.5)                       = 1 - 0.75000 = 0.25000
   deviation per-pull utility = 1 - [(5/9) phi(0.9) + (4/9) phi(0)] = 1 - 0.52778 = 0.47222
   gain per pull              = 0.22222      =>   gain >= 0.1111 n.
```
Linear. **(H3) alone is not a repair.** This is the single most important entry in the table: the
natural reflex ("assume Lipschitz, that always works") is wrong here, because the obstruction is a shape
condition and not a regularity condition.

### W3 — (H2) without Lipschitz: the RATE of `thm:private-mesp`(i) fails

**Instance.** `K = 2`, `M_1 = M_2 = 1`, `mu_1 = mu_2 = 0`, agent 2 honest (vacuously, `mu_2 = 0`).
So `M_(2) = 1`.

**Cost.** `phi(m) = 1 - (1 - m)^{1/4}`. Increasing; `phi'' = (3/16)(1-m)^{-7/4} > 0` so **convex**;
`phi(0) = 0, phi(1) = 1` so (N) holds. **Not Lipschitz**: `phi'(m) = (1/4)(1-m)^{-3/4} -> infinity` as
`m -> 1`. (H2) holds, (H3) fails.

**Baseline.** Both agents deliver `1` in Stage 1, so `beta_1 = beta_2 = 1` exactly and
`tau = 1 - s_n`. The winner's baseline primary target is `tau`, at per-pull utility
`1 - phi(1 - s_n) = s_n^{1/4}`.

**Deviation.** The boundary-tracking deviation of `prop:noisy-tight` (the paper's own construction):
shade below `tau` so that the cumulative mean deficit tracks `b_n(r)` from below, total shading
`Theta(sqrt(n log n))`, never convicted except on an event of probability `O(1/n)`. (Here the variance
of `Y_r` is `~ s_n`, far below `b_n(r)^2/r`, so the margin is ample.) Its extra utility is
```
   phi'(tau) * sum_r delta_r  ~  (1/4) s_n^{-3/4} * Theta(sqrt(n log n)).
```
With `L_n ~ n^{2/3}(log n)^{1/3}` and `s_n ~ sqrt(2) (log n)^{1/3} n^{-1/3}`, this is
```
   Theta( n^{3/4} (log n)^{1/4} )   >>   Theta( n^{2/3} (log n)^{1/3} ).
```

**Numerical check** (exact parameters `L_n = min{n/(2K), n^{2/3} log(en)^{1/3}}`,
`s_n = sqrt(log(2Kn^4)/(2L_n))`, `b_n(n) = sqrt(n log(2n^4)/2)`, `K = 2`):

| `n` | `s_n` | `phi'(tau)` | `phi'(tau) b_n(n)` | claimed `n^{2/3}(log n)^{1/3}` | ratio |
|---|---|---|---|---|---|
| `1e6` | 3.40e-2 | 3.16 | 1.67e4 | 2.40e4 | 0.70 |
| `1e9` | 3.89e-3 | 16.1 | 3.28e6 | 2.75e6 | **1.20** |
| `1e12` | 4.28e-4 | 84.1 | 6.27e8 | 3.02e8 | **2.07** |
| `1e15` | 4.61e-5 | 447 | 1.18e11 | 3.26e10 | **3.62** |

The ratio grows like `n^{1/12}`, so the claimed rate is exceeded for all large `n`. Generalising to
`phi(m) = 1 - (1-m)^alpha`, the rate is `Theta(n^{1/2 + (1-alpha)/3})`, which exceeds `n^{2/3}` exactly
when `alpha < 1/2`, and it is **attained**, not merely an artefact of the bound.

**Scope of W3.** It requires `M_(2)` at (or converging to) `1`. If `M_(2) <= 1 - zeta` for a fixed
`zeta > 0`, `phi'(tau) <= phi'(1-zeta) <= 1/zeta` is an instance constant and the rate is preserved —
which is the `Lambda_eff <= 1/(1 - M_(2))` entry in the table. This is why my recommendation is to assume
`Lambda` outright: it makes `thm:private-mesp`'s "uniform over all scalar instances with `K` agents; no
capacity gap enters it" true again.

### W4 — a jump at the capacity kills the contextual PUBLIC equilibrium under (H1) and (H2)

**Cost.** `phi(m) = 1{m = 1}`. Increasing, bounded, `phi(1) - phi(0) = 1` so (N) holds. It is also
**convex** on `[0,1]` (`phi(lambda) = 0 <= lambda = lambda phi(1) + (1-lambda) phi(0)`), so this is an
(H2) instance as well as an (H1) instance. Convexity on `[0,1]` forbids interior jumps but permits this
one at the right endpoint.

**Instance.** Any instance for `thm:contextual-public` with `M_i(x) = 1` for two agents at almost every
profile (so the two-top condition holds) and `mu_i = 0`.

**Baseline `S^max`.** Every agent delivers `M_i = 1`, costing `phi(1) = 1`; per-pull utility `0`.

**Deviation.** `m'_n := 1 - eps_n` with `eps_n := q_n^{-1/2}`, a legitimate element of `S_HDS` because
that class is **horizon-dependent**. Cost `phi(1 - eps_n) = 0`; per-pull utility `1`. The exploration
means differ by `eps_n = q_n^{-1/2}`, so by `lem:etc-tail` the deviator's commitment probability is
`Theta(1)` (the exponent `q_n eps_n^2 / 2 = 1/2` is `O(1)`). Gain `= Theta(n)`.

**Contrast.** The *scalar* public result `thm:public-ucb` is **not** broken by the same cost, because
`S_HI` is horizon-*independent*: `eps` must be fixed, the deviator then has a fixed positive gap and
receives `O(log n / eps^2) = O(log n)` pulls. (The theorem's own sentence "the bound is not uniform over
deviations whose gap vanishes" is exactly the crack that W4 walks through in the contextual case.)
`thm:private-mesp` is also **not** broken by this cost, because the announced price is strictly shaded
below capacity (`tau <= M_(2) - 0` and in fact `tau <= beta_(2) - s_n < 1`), so the baseline primary
target never sits on the jump.

**Fix.** Assuming `phi_i` Lipschitz removes W4 entirely. Assuming only `phi_i` continuous on `[0,1]`
restores the equilibrium claim as an `o(n)` statement but changes the rate `E_n` to
`n * omega_phi(c_1 q_n^{-1/2}) + (existing terms)`, where `omega_phi` is the modulus of continuity;
under `Lambda`-Lipschitz this is `Lambda c_1 n q_n^{-1/2}`, i.e. the existing term times `Lambda`.

---

## 5. Exact restatements of the theorems whose constants move

Throughout: `Lambda` is the Lipschitz constant of the `phi_i`,
`Lambda_1 := max_i (phi_i(M_i) - phi_i(0)) <= 1` by (N), and
`kappa_phi := 1 - max_i (phi_i(M_top) - phi_i(mu_i))`.

**`thm:private-mesp`.** Parts (ii) and (iii) are unchanged, word for word. Part (i) becomes

```
  sup_{S'_{i,n} in B_{i,n}} [ u_i(n; S'_{i,n}, S^star_{-i,n}) - u_i(n; S^star_n) ]
        <=  Lambda_1 * L_n  +  Lambda * ( 1 + 2 b_n(n) + R_K(n) )  +  O(1)
        =   O_{K,Lambda}( n^{2/3} (log n)^{1/3} )  =  o(n),
```
uniform over the declared deviations and over all scalar instances with `K` agents and cost functions
obeying the standing assumption; no capacity gap enters it.

**`lem:private-monitor`, utility clause.** On the complement of the deviation event, for a tenure of `q`
pulls,
```
  A_q >= q tau - 1 - 2 b_n(q)                                   [unchanged]
  U_i^pri <= q ( 1 + phi_i(mu_i) - phi_i(tau) ) + Lambda ( 1 + 2 b_n(q) ).
```

**`eq:private-fallback-top`.**
```
  E[ U_i^fb | F_fb ]  <=  ( 1 + phi_i(mu_i) - phi_i(V_i) ) H  +  Lambda R_K(H).
```

**`prop:tightness`.** For every `n` with `4 s_n < M_i - V_i`,
```
  u_i(n; S'_{i,n}, S^star_{-i,n}) - u_i(n; S^star_n)  >=  L_n ( phi_i(M_i) - phi_i(m') ) - 4 n^{-3},
```
which is `Theta(L_n)` provided `phi_i` is strictly increasing on `[m', M_i]`.

**`prop:ctx-finite-exact`(i), second display.** Note that the non-top sum is **not** multiplied by
`Lambda`:
```
  sup_{S'} [ ... ]  <=  min{Q L_n, n}
                      +  Lambda [ Q + sqrt(2 l_n Q n) + Q R_K(n) ]
                      +  sum_{z : i notin T(z)} [ 8 (1 + sqrt(2 l_n))^2 / delta_i(z)^2
                                                  + 2 R_K(n) / delta_i(z) ]
                      +  8 n^{-2}.
```
Parts (ii) and (iii) unchanged.

**`prop:ctx-continuum-exact`(i).**
```
  u_i(n; S'_{i,n}, S^star_{-i,n}) - u_i(n; S^star_n)
        <=  e_bid  +  Lambda ( e_osc + e_mon + e_fb )  +  4 n^{-3} + 4 K^{-1} n^{-2}.
```
Parts (ii) and (iii) unchanged. `thm:ctx-private-continuum`'s exponent `(D+2)/(D+3)` is unchanged, with
the constant carrying a factor `Lambda`.

**`prop:ctx-finite-tight`.** With `c_phi := min_z ( phi_i(M_i^z) - phi_i(m'(z)) ) > 0`,
```
  u_i(n; S'_{i,n}, S^star_{-i,n}) - u_i(n; S^star_n)  >=  c_phi Q L_n - 4 Q n^{-3}.
```

**`(ND)` in `app_equilibrium.tex`.** Replace
```
  M_top < 1,   kappa := 1 - M_top > 0
```
by
```
  kappa_phi := 1 - max_i ( phi_i(M_top) - phi_i(mu_i) ) > 0,                     (ND_phi)
```
used only to guarantee that a selection is worth an amount bounded away from zero: every feasible
target `m <= M_top` gives per-pull utility `1 + phi_i(mu_i) - phi_i(m) >= kappa_phi`. Under the standing
assumption, `(ND_phi)` follows from `M_top < 1` together with `phi_i` strictly increasing. Then replace
`kappa` by `kappa_phi` throughout `prop:mesp-equilibrium-set`, `prop:mesp-pairs`,
`prop:plmesp-equilibrium-set`(ii), `prop:plmesp-pairs` and `rem:mesp-reading`.

**`prop:mesp-equilibrium-set`, case (A) deviation bound.**
```
  sup_{S'_{i,n}} [ ... ]  <=  Lambda_1 L_n + Lambda ( 1 + 2 b_n(n) + R_K(n) ) + O(1).
```
In the necessity proof, case (2a), `N_n s_n -> Lambda N_n s_n` (still
`O(n^{2/3}(log n)^{1/3})`). The revenue formula `nu(c)` and `cor:mesp-revenue-range` are unchanged.

**`cor:mesp-price-setter`.** Agent `k`'s gain is `L_n ( phi_k(M_(2)) - phi_k(c'_k) ) - O(n^{-2})`; the
revenue loss `(M_(2) - c'_k) n - O(K L_n + n s_n)` is unchanged.

**`prop:mesp-pairs`.** (i) `W` gains `( phi_W(M_(2)) - phi_W(theta) )_+ N_n - O(Lambda n s_n + Lambda
sqrt(n log n))`; `k` gains `L_n ( phi_k(M_(2)) - phi_k(c_k) ) - O(n^{-2})`. The revenue statement and the
"sharp per-round transfer" are unchanged (they are in mean space). (ii) each member gains
`((1/2) N_n + L_n) ( phi(M_top) - phi(theta) ) - O(Lambda n s_n + Lambda sqrt(n log n))`, and the
non-self-enforcement gains are `>= (1/2) N_n kappa_phi - O(L_n)`. (iii) unchanged apart from
`kappa -> kappa_phi`.

**`prop:plmesp-equilibrium-set`(i).**
```
  sup_{S'} [ ... ]  <=  Q L_n  +  Lambda [ Q(1 + R_K(n)) + sqrt(2 Q n l_n) ]
                        +  2 Viol(c)  +  O(Q n^{-2}).
```
(ii): the per-profile gain is `>= (kappa_phi / K) N_z - 2 L_n - O(1)`; (iii) unchanged.

**Sharp adaptivity (definition, `sec3_noisy.tex`).** Replace the cumulative effort `C_i(n)` by the
cumulative **mean lift**
```
  Delta_i(n) := sum_{t <= n : I_t = i} ( m_{i,t} - mu_i ),
```
so that the condition reads `E_S[Delta_i(n)] >= (mu_H^star - mu_i) E_S[T_i(n)] - C sqrt(n log(en))`. Then
`thm:sharp-robustness` is verbatim, via the identity
`P(n;S) = sum_i ( E_S[Delta_i(n)] + mu_i E_S[T_i(n)] )`, which now holds for every cost function. The
same one-line substitution is needed twice in `appendix_contextual.tex` and once in
`appendix_samf.tex` l.20 and l.49.

**`thm:contextual-public` / `thm:grid-ucb-robust`, equilibrium.** The per-cell bound becomes
`p'_{i,C} delta_C^phi <= Lambda ( c_1 q_n^{-1/2} + eta_{i,C} )`, so `E_n -> Lambda E_n` with the
exploration charge `q_n J_n` unchanged (it is bounded by `Lambda_1 <= 1` per pull).

**`prop:two-top-sharp`.** With `lambda := inf_{m in [M_i - g_0/2, M_i]} phi_i'(m) > 0` the gain becomes
`>= (lambda g_0 nu(A) / 32) n`.

**Optional free extension (worth taking).** Nothing above breaks if the cost also depends on the
context, `phi_i(x_i, m)`, provided `phi_i(x, .)` is convex and `Lambda`-Lipschitz in `m` for each `x`
and `L_phi`-Lipschitz in `x` uniformly in `m`. The only change is that `eq:ctx-horizon` becomes
`log(en) >= 3 max{L, L_phi}` and `e_osc` acquires the constant `(Lambda L + L_phi)` in place of
`Lambda L`. A referee who raises the cost objection will almost certainly also want the cost to vary
with the task, so this is worth having in hand.

---

## 6. The honest-agent constraint and the benchmark definitions

**Honesty.** Keep it in mean space, exactly as written: an honest agent never chooses
`m_{i,t} < mu_i` (pointwise in context, in the contextual case). **Do not** restate it as "never exerts
negative effort", i.e. as `phi_i(m) >= phi_i(mu_i)`. The two are equivalent only when `phi_i` is
strictly increasing; under a merely nondecreasing `phi_i` the cost-space version is strictly weaker and
would break the three places that actually use honesty, all of which need the mean:

* the honest bid floor (`appendix_private.tex`, robustness proof: "Its predictable Stage-1 target sum is
  at least `L_n mu_H^star`"), and `lem:ctx-honest-floor`(ii)-(iii);
* the honest comparator's conditional mean in the fallback (`lem:selected-reactive-exp3`,
  `lem:ctx-fallback`, `lem:ctx-fallback-cont` all need `E[Y | selected] >= v`);
* the honest branch of the incentive proofs ("every honest deviation earns at most one unit per selected
  pull", `appendix_private.tex` l.134 and `app_contextual_private.tex`'s honest sub-case), which needs
  `m >= mu_i` to conclude per-pull utility `<= 1`; under a general cost this reads
  `1 + phi_i(mu_i) - phi_i(m) <= 1`, which follows from `m >= mu_i` and `phi_i` nondecreasing — verbatim.

So: **one added clause of clarification, no change of content.**

**Benchmarks.** `mu_H^star`, `M_top`, `M_(2)`, `V_i`, `K_top`, `b(X)`, `M_star(X)`, `M_(2)(X)`,
`T(X)`, the two-top condition, `g(z)` in `cor:plmesp-revenue`, and the platform's revenue
`P(n;S) = E sum_t Y_t = E sum_t m_{I_t,t}` are **all quantities in outcome or capability space and
need no restatement whatsoever**. This is the single cleanest thing to say to a referee: the mechanism
elicits, prices, monitors, and is judged entirely in the space of delivered means; the cost function
enters only through what an agent is willing to do, never through what the platform measures or
promises.

**One thing that does need a sentence.** `mu_i` should be described as the mean the agent produces at
zero effort (`phi_i(mu_i)` is the origin of its cost scale), not as "its intrinsic reward mean" full
stop, so that the reader knows why `phi_i(mu_i)` and not `phi_i(0)` appears in the utility.

---

## 7. Does a non-convex increasing cost break anything a convex one does not?

**Yes, and it breaks exactly one thing: the Jensen step in the winning branch of the incentive proof.**
Everything else in the paper — the monitor, the fallbacks, bid domination, the price lemmas, revenue,
robustness, the non-top winning branch, the losing branch, the equilibrium characterisation, the
collusion results, the two public-capability theorems, the separation theorem — is indifferent to
convexity. But that one thing is the paper's headline result, the break is linear, and it is not a
proof artefact: by Lemma A it is a genuine property of the observation model, so no repair of MESP and
no other mechanism observing only Bernoulli outcomes can restore it.

**So (H1) is not the cleanest hypothesis to ship; it is the wrong one.** What (H1) buys, via Lemma A,
is something better than shipping it: the remark that a non-convex cost is *strategically equivalent*
to its convex envelope, so convexity is WLOG up to replacing `phi_i` by `phihat_i` — at the price of
making the proposed profile a mixed strategy (Corollary A2). Put that remark in the paper and the
convexity assumption stops looking like an assumption of convenience.

**Scoreboard of the three classes.**

| | incentive (scalar private) | incentive (contextual private) | incentive (public, `S_HI`) | incentive (contextual public, `S_HDS`) | revenue | robustness | tightness |
|---|---|---|---|---|---|---|---|
| **H1** | FAILS (W1) | FAILS | verbatim | FAILS (W4) | verbatim | verbatim | order OK if strictly increasing |
| **H2** | rate degrades (W3), survives if `Lambda_eff` finite | needs `Lambda_eff` finite | verbatim | FAILS (W4) | verbatim | verbatim | order OK; constants separate by `Lambda/lambda` |
| **H3** | FAILS (W2) | FAILS | verbatim | verbatim | verbatim | verbatim | order OK |
| **H2 ∧ H3** | **verbatim rate, constants × `Lambda`** | **verbatim rate, × `Lambda`** | verbatim | verbatim | verbatim | verbatim | order OK |

---

## 8. Cost of adopting this

**Verdict: a careful one-to-two-day edit, not a rewrite.** The risk is in re-verifying constants, not in
finding new arguments.

**Lines that must change.** Counted by grepping for the utility term
(`1+\mu`, `\mu_i-m`, `\mu_i^{\inf/\sup}`, `[0,2]`, `c_{i,t}`, `C_i(n)`):

| File | lines touched | what |
|---|---|---|
| `sec2_model.tex` | 5 + ~8 new | cost definition (l.6-8), utility display (l.17), range sentence (l.21), contextual cost (l.56); new assumption paragraph |
| `sec3_noisy.tex` | ~8 | sharp-adaptivity display (restate in mean space), `thm:public-ucb` proof idea, `thm:private-mesp` statement, "Accounting" paragraph of the proof skeleton, `prop:noisy-tight` statement |
| `sec4_contextual.tex` | ~2 | two summary constants |
| `sec6_conclusion.tex` | ~2 | the "Standing modelling assumptions" paragraph already says "effort priced linearly in the delivered mean" — replace by the new assumption, and add one line to Limitations |
| `appendix_samf.tex` | 4 | l.20 and l.49 (the false revenue identity) + `lem:ucb-deficit` citation line |
| `appendix_public.tex` | 2 | l.10, l.12 |
| `appendix_private.tex` | ~12 + 8 new | l.8, 22, 29, 115, 118, 130, 132, 134, 138, `prop:tightness` statement and proof; **new Lemma B + proof (8 lines)** |
| `appendix_contextual.tex` | ~8 | two "`c_i = m_i - mu_i` converts" sentences, `thm:contextual-public` equilibrium proof (`a_C`, `delta_C`), `prop:two-top-sharp` constants |
| `app_contextual_private.tex` | ~28 | 27 grep hits (the `w_C` display, `lem:ctx-monitor`(b)/(c), `lem:ctx-dev-fallback`, `eq:ctx-dev-post`, the "cancellation is worth naming" paragraph, `prop:ctx-finite-tight`) |
| `app_equilibrium.tex` | ~25 | 24 grep hits ((ND), (E1), (E2), case 2a, `cor:mesp-price-setter`, `prop:mesp-pairs`(i)(ii)(iii), `lem:no-punishment`, `prop:plmesp-*`) |
| **total** | **~95 edited + ~16 new** | ≈ 2% of the 5,700 lines of body + appendix |

**Why it is mechanical.** Every one of the ~95 edits is one of four substitutions:

```
  (S1)  1 + mu_i - m                   ->   1 + phi_i(mu_i) - phi_i(m)                    [~60 lines]
  (S2)  1 + 2 b_n(q)                   ->   Lambda ( 1 + 2 b_n(q) )         [Lemma B(a)]  [~8 lines]
        R_K(H), R^dbl_K(H), rho_n H    ->   Lambda * (same)                 [Lemma B(b)]  [~8 lines]
  (S3)  kappa                          ->   kappa_phi                                     [~12 lines]
  (S4)  M_i - m'  (a saved-effort gap) ->   phi_i(M_i) - phi_i(m')                        [~7 lines]
```
Nothing requires a new argument beyond Lemma A (a remark) and Lemma B (two lines). No lemma is
restructured. No coupling changes. No probability estimate changes.

**What is genuinely new work, and where the time goes.**

1. Deciding the notation (`phi_i`, to avoid the collision with the bid vector `c` in
   `app_equilibrium.tex`) and sweeping for the collision. ~1 hour.
2. Writing the model paragraph, Lemma A + Corollaries, and Lemma B. ~2 hours.
3. The ~95 substitutions, done file by file. ~4 hours.
4. **Re-verifying that every constant in `prop:ctx-finite-exact` and `prop:ctx-continuum-exact` still
   sums correctly with the `Lambda` factors inserted in the right places and not the wrong ones.**
   This is the real cost, because the two propositions state "exact form" with every constant written
   out and a misplaced `Lambda` would be a referee-visible error. In particular the non-top branch of
   `prop:ctx-finite-exact`(i) must **not** acquire a `Lambda`, and `e_bid` / `e_stage1` must **not**.
   ~4 hours, and it should be done by someone who re-derives rather than pattern-matches.
5. Re-reading `sec6_conclusion.tex`'s Limitations section, which currently claims linear pricing as a
   standing assumption; it becomes a shorter and better paragraph. ~30 minutes.

**What it buys.** The paper stops being vulnerable on its own motivating example, and gains a
strictly stronger theorem: the guarantees hold for every convex increasing cost, which is precisely the
class the quality-compute literature the paper cites (`sreenivas2026contracting`, concave saturating
quality in effort) produces. The revenue and robustness theorems become *cost-free*, which is a
genuinely striking thing to be able to say.

**What it costs in page budget.** Roughly +10 lines net in the body (the assumption paragraph, minus the
shortened limitations paragraph) and +16 in the appendix. Per the standing page-budget decision, this
should not drive the choice; it is well inside noise.

---

## 9. Open or doubtful

1. **Is the `n^{5/6}` ceiling under (H2)-without-Lipschitz tight as a worst case over the class?** For
   each fixed `phi(m) = 1 - (1-m)^alpha` I exhibit a matching rate `Theta(n^{1/2 + (1-alpha)/3})`
   (W3), and the supremum over `alpha in (0,1)` is `n^{5/6}`, which is also the upper bound
   `(1 + 2b_n(n))/s_n` I derive. But no *single* `phi` in (H2) attains `n^{5/6}`, and I have not
   checked whether a `phi` with a more exotic modulus does. **Doubtful, low stakes** — the
   recommendation is to assume Lipschitz, which makes the question moot.

2. **Is convexity necessary, or only sufficient, for the incentive bound *at the stated rate*?** Lemma A
   shows convexity is necessary for `S^star` *as written* to be a best response, which is what makes
   (H1) a FAIL. What I have **not** proved is that no *other* proposed profile plus no other choice of
   `L_n, s_n, b_n` restores `O(n^{2/3}(log n)^{1/3})` under a non-convex `phi` — Corollary A2 suggests
   a randomised `S^star` does, at the cost of turning pathwise identities into expectation identities,
   but I have not carried out that rewrite and do not vouch for its constants. **Open.** I would not
   claim in the paper that convexity is necessary for the *mechanism*; only that it is necessary for
   the *stated profile*, which is the honest and checkable claim.

3. **The `Lambda_eff` bound in the contextual continuum case.** I asserted that (H2) alone suffices
   provided `max_x max_i max{mu_i(x), M_(2)(x)} <= 1 - zeta`, with `Lambda_eff <= 1/zeta`. I checked
   the two places this is needed (`lem:ctx-dev-fallback`'s `rho_n H / 3`, and the
   `mu_i^sup(C) <= mu_i^inf(C) + rho_n/3` step in `prop:ctx-continuum-exact`(i)). I did **not**
   exhaustively re-derive every one of the seven error terms with `Lambda_eff` inserted, because the
   recommendation is `Lambda`-Lipschitz, under which the question does not arise. **Doubtful if
   someone insists on (H2)-only for the continuum.**

4. **`thm:ctx-net-separation`.** I treated part (A) as structurally identical to
   `prop:ctx-continuum-exact`(i) and assigned it the same verdict. Its proof is not given in the
   appendix (the statement is given with its error terms and a balance argument, not a proof), so my
   verdict there is by structural analogy and not by line-by-line checking. **Flagged.** It is a
   "separation, not an algorithm" result, so the stakes are lower, but the table entry should be read
   as provisional.

5. **Whether the `S_HDS` randomisation-over-maps clause creates a second splitting channel.** The class
   "permits each agent to randomize independently over such maps before play". Utility is affine in
   that mixture, so mixing over maps cannot beat the best map and no Jensen issue arises there. I am
   confident of this. The *within-cell* splitting (a single map taking different values at different
   contexts of a cell) is the real channel, and it is the one W4 uses. **Settled, recorded here in case
   a reader conflates the two.**

6. **The experiments.** `sec5_experiments.tex` and `audit/round2/A*` compute exact optimal deviations
   under the linear cost. If the model assumption changes, the experiment code's utility function
   changes with it, and the reported exploitability numbers would need recomputation (or the paper
   must say explicitly that the experiments instantiate `phi(m) = m`). I did not read the experiment
   code. **Open, and it is the one place where "a one-day edit" could become two.** The cheapest
   honest fix is one sentence: "the experiments instantiate the linear case `phi_i(m) = m`".

7. **Strict monotonicity for the tightness results.** I recommend adding "`phi_i` strictly increasing"
   to the hypotheses of `prop:tightness`, `prop:ctx-finite-tight`, `prop:noisy-tight` and
   `prop:two-top-sharp`, and stating their constants in terms of `phi_i`. An alternative is to leave
   them stated with the constants `phi_i(M_i) - phi_i(m')` etc. and observe that they are positive
   whenever `phi_i` is strictly increasing there. I have **not** checked whether a flat `phi_i` on
   `[V_i, M_i]` creates any *other* problem beyond making these constants vanish; it should not, since
   a flat cost only makes the mechanism's job easier, but I did not verify it exhaustively.
   **Doubtful, low stakes.**
