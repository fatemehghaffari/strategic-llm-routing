# ADVERSARY — hostile pass on `thm:ctx-private-continuum` / `prop:ctx-continuum-exact`

Read in full: `sections/sec2_model.tex`, `sections/sec4_contextual.tex`,
`sections/app_contextual_private.tex` (`app:ctx-private-continuum`, lines 631–1310, every lemma and
all three proofs; plus `app:ctx-private-finite` for `lem:ctx-locality`, `lem:ctx-monitor`,
`lem:ctx-fallback`, which the continuum proofs cite), and both prover reports
(`PROVER_SC1.md`, `PROVER_SC2.md`), treated as claims.

## Verdict, up front

**I broke something.** There is one finding I am willing to call a counterexample to a printed
theorem, with a fully specified instance, a Θ(n) gain, and a script that runs. It is **not** a break
of the mechanism and **not** a break of the appendix's accounting; it is a break of the
**hypothesis chain**, and the defective sentences are printed in three places. The repair is one
clause, but until that clause is added, Theorem `thm:ctx-private-continuum`(i) as printed in
`sec4_contextual.tex` is **false**, and the class over which `prop:ctx-continuum-exact`(i)
quantifies is **not well defined** under the hypothesis it names.

| # | Finding | Label |
|---|---|---|
| **1** | An (A2)-legal arrival path whose contexts reveal the round's reward seed. A single strategic agent then reproduces the baseline's reward path round for round at half the cost. Gain `0.44 n` at `n = 10^9` against a printed bound of `1.2e8`; ratio → ∞. | **Counterexample to the THEOREM as printed in `sec4`** (part (i), which invokes (A2) only), and to the printed claim "Each condition implies the next" in `sec2` ((A2) ⇏ (A3)). |
| **2** | Same instance, one round later: with the context revealing the *previous* round's seed, (A3) holds for every strategy in `B^ctx`, and the Θ(n) deviation lives in `B^ctx+`. | **Counterexample to a LEMMA-level claim**: "The enlargement is free under (A2)" (`app_contextual_private.tex` l. 21–23). `prop:ctx-continuum-exact`(i) survives only if its quantifier over `B^ctx+` is silently restricted. |
| **3** | "the leading constant of the incentive bound [carries K] not at all" is true only of the asymptotic leading term. At every horizon at which the bound of (i) is non-vacuous, for `K ≥ 20`, the `K`-carrying terms are the **majority** of the paper's own exact bound. Numbers below. | **Gap in a written claim** (quantitatively misleading, not false). |
| **4** | `e_fb` charges the deviator the **full EXP3 regret** `11√(K H log K)` where the deviator can only collect its own exploration share `≈ √(H log K / K)`. The one term that carries `K` is loose by a factor ≈ `K`. | **Looseness a referee will flag**, in exactly the term finding 3 is about. |
| **5** | The grid is `J_n` half-open cubes tiling `[0,1)^d`, but `sec2` and `sec4` declare `X = [0,1]^d` and `sec4` asserts the cells "tile the closed cube exactly". Contexts on the upper faces belong to no cube. | **Gap in the written proof**, trivially reparable (`ω` is unchanged). |
| **6** | `lem:ctx-fallback-cont` is stated unconditionally but is applied conditionally on the fallback-start field, with `H` treated as measurable there (`lem:ctx-dev-fallback`, and the `1_F` step in the proof of (i)). The continuum proof never performs the explicit "condition on the arrival path `A`" step that the *finite* proof (l. 160–172) does perform. | **Gap in the written proof.** It is the same hole as finding 1, seen from the inside. |

Everything else I attacked held. §7 lists the failed attacks; §8 names the single weakest step.

---

## 1. THE BREAK — an (A2)-legal path that leaks the round's seed

### 1.1 What the paper says

* `sec2_model.tex` l. 59: **"(A2) Exogenous.** No agent's behaviour can change the realised sequence
  of contexts. They need not be independent, identically distributed, or random at all."
* `sec2_model.tex` l. 63: "**Each condition implies the next.**" (i.e. (A1) ⇒ (A2) ⇒ (A3).)
* `sec4_contextual.tex`, `thm:ctx-private-continuum`: "(i) **under (A2)**, no unilateral deviation
  gains more than `O_{d,K}(n^{(d+2)/(d+3)} log(eKn))`". (A3) is **not** named in part (i); (ii) and
  (iii) are named "under (A3) alone", so the reader is told (A2) is the *stronger* rung.
* The whole of `app:ctx-private-continuum` runs on (A3)'s seed clause:
  `E[Y_u | G^-_u] = m_{I_u,u}` with `G^-_u ⊇ σ(x_u)`.

(A2) is a condition on **contexts only**. (A3) is a condition on **the round's own draws**. Neither
implies the other, and the gap is not academic: (A2) says nothing about what a context *reveals*
about the round's seed.

### 1.2 The instance

Fully specified; `d = 1`, `K = 2`.

| object | value |
|---|---|
| capabilities | `M_1(x) ≡ 1`, `M_2(x) ≡ 0.9` |
| intrinsic means | `μ_1(x) ≡ 0`, `μ_2(x) ≡ 0` |
| Lipschitz constant | `L = 0`, so `n ≥ e^{3L} = 1`: **the one instance hypothesis holds at every horizon** |
| honest set | `K_H = {2}` (nonempty; honesty `m ≥ μ_2 = 0` is vacuous, so `S*_2` is honest) |
| deviator | agent 1, strategic |
| seed array | `(U_1,…,U_n)` i.i.d. Uniform[0,1], `Y_t = 1{U_t ≤ m_{I_t,t}}` — the paper's own object, named in the coupling of the proof of (i) ("the same arrival path, **seed array**, priorities, EXP3 coins and private coins") |
| **arrival path, variant A** | `x_t := h_n · U_t` |
| **arrival path, variant B** | `x_1 := 0`, `x_{t+1} := h_n · U_t` |

Both paths lie entirely in the single cube `[0, h_n)`, so `J'_n = 1`. **No agent's behaviour changes
the seed array, hence no agent's behaviour changes the realised context sequence: (A2) holds
verbatim, in the exact words printed in `sec2`.** The path is not i.i.d., not stationary, and
correlated with the rewards — all of which (A2) explicitly permits ("They need not be independent,
identically distributed, or random at all").

### 1.3 The deviation

Agent 1 plays `S*` in Stage 1 (so the bid domination step, the win inclusion and the price are
untouched; `β_1 = 1 > β_2 ≈ 0.9`, agent 1 wins, `τ_C = (β_2 − σ_n)_+`). At a Stage-2 pull at round
`t` it recovers `Û_t = x_t / h_n` (variant A) or `Û_t = x_{t+1}/h_n` (variant B) and plays

```
m_{1,t} = min(1, Û_t + 1e-9)   if Û_t ≤ τ_C
m_{1,t} = 0                    otherwise
```

Feasible (`m ≤ M_1 = 1`), and in `B^ctx` for variant A (it uses only the **current** context, which
the model says the selected agent observes) and in `B^ctx+` for variant B (it uses one future
context).

**Why the monitor cannot see it.** `Y_t = 1{U_t ≤ m_{1,t}} = 1{U_t ≤ τ_C}` — which is *exactly* the
reward the baseline `S*` (which plays `m = τ_C`) produces from the same seed. The two executions
have the **same reward sequence, round for round**, hence the same `Z_r`, the same monitor
trajectory, the same switch decision (none). The monitor `Z_r < rτ_C − b_n(r)` is a test on
rewards, and the reward paths are identical; no choice of `b_n`, `s_n` or `ρ_n` can separate them.
Only the cost differs:

```
baseline cost per Stage-2 round  = τ_C
deviation cost per Stage-2 round = U_t · 1{U_t ≤ τ_C},   expectation τ_C²/2
gain rate = τ_C − τ_C²/2 = τ_C(2 − τ_C)/2  →  0.9 − 0.405 = 0.495  as σ_n → 0.
```

`Θ(n)`. Beats any `o(n)` bound.

### 1.4 Numbers (verified, script in §1.6)

Simulation, `d = 1`, `K = 2`, seeds `default_rng(0)`, exact CG-MESP parameters
(`g_n = ⌈n^{1/4}⌉`, `L_n = ⌈n^{1/2}⌉`, `ℓ_n = log(2Kn⁵)`, `s_n = √(ℓ_n/2L_n)`,
`ρ_n = √d h_n log(en)`, `σ_n = 3s_n + ρ_n`, `b_n(r) = √(rℓ_n/2)`), bound = the **exact** bound of
`prop:ctx-continuum-exact`(i), `e_bid + e_osc + e_mon + e_fb + 4n^{-3} + 4K^{-1}n^{-2}`, evaluated
both at the realised `E[J'_n] = 1` and at the worst case `min{J_n, n}`:

| n | σ_n | τ_C | realised gain | = c·n | bound (i), `J'=1` | ratio | bound (i), worst case | ratio |
|---|---|---|---|---|---|---|---|---|
| 1e7 | 0.6418 | 0.2595 | 2.257e6 | 0.226 n | 3.105e6 | 0.73 | 3.930e6 | 0.57 |
| **1e8** | 0.3993 | 0.5032 | **3.765e7** | 0.377 n | **1.975e7** | **1.91** | 2.363e7 | 1.59 |
| **1e9** | 0.2443 | 0.6575 | **4.413e8** | 0.441 n | **1.231e8** | **3.59** | 1.415e8 | 3.12 |

Monitor minimum slack `min_r (Z_r − rτ_C + b_n(r))` was `+6.33` at `n = 1e8` and `+7.59` at
`n = 1e9`, i.e. **no switch in either execution** — the deviator never reaches the fallback, so
`e_fb` and `e_mon` are not even in play; the violated term is the whole bound.

The `n = 1e7` row is the honest one: there the bound is still larger than the gain, because the
mechanism's own `σ_n = 0.64` has crushed `τ_C` to `0.26` and `e_osc = nρ_n = 3.0e6` is still large.
The crossing is at `n ≈ 5·10^7` and the violation then grows without bound. Analytic continuation
(gain rate `τ*(2−τ*)/2` with `τ* = 0.9 − σ_n`, `n_C = n − KL_n`):

| n | τ_C | gain/n | E[gain] | bound (i), `J'=1` | ratio |
|---|---|---|---|---|---|
| 1e10 | 0.752 | 0.469 | 4.69e9 | 7.61e8 | 6.2 |
| 1e12 | 0.846 | 0.488 | 4.88e11 | 2.87e10 | 17.0 |
| 1e14 | 0.881 | 0.493 | 4.93e13 | 1.05e12 | 46.9 |
| 1e16 | 0.893 | 0.494 | 4.94e15 | 3.78e13 | 130.6 |

Variant B, explicit check at `n = 2·10^7` (`τ_C = 0.3368`): the reward sequences of the two
executions differ in **1 round out of 19,991,054** (the last round, where `x_{n+1}` does not exist
and the deviator falls back to `S*`); neither execution switches; gain `5.5997e6 = 0.2800 n`,
identical to variant A to six digits.

### 1.5 What exactly is refuted, and what is not

I want this labelled precisely, because a defender has a move and I want to close it in advance.

**Variant A refutes:**
1. `sec2_model.tex` l. 63, "**Each condition implies the next**". Variant A satisfies (A2) and
   violates (A3): `x_u = h_n U_u` is `G^0_u`-measurable, so `U_u` is *not* uniform given
   `G^-_u ⊇ G^0_u`. The implication (A2) ⇒ (A3) is simply false as the two are written; they are
   conditions on disjoint objects.
2. `thm:ctx-private-continuum`(i) **as printed in `sec4_contextual.tex`**, which names (A2) and
   nothing else, and whose reading is fixed by (ii)/(iii) saying "under (A3) **alone**". Under the
   printed hypotheses of that theorem, variant A is admissible and the gain is `0.44 n`.

**Variant A does not refute** `prop:ctx-continuum-exact`, whose hypothesis block does say "The
probabilistic hypothesis is (A3)" and whose §"Which clause each result uses" says part (i) uses all
of (A3) plus (A2). Variant A is outside *those* hypotheses.

**Variant B refutes** the appendix's own sentence (l. 21–23): "**The enlargement is free under (A2)**:
the baseline `S*` never uses the arrival path, the per-path bounds below are free of the arrival
path and of the deviation, and no step uses an agent's ignorance of the future." In variant B:
* (A2) holds;
* (A3) holds — in full, seed clause and mechanism clauses — for the baseline `S*` **and for every
  strategy in `B^ctx`**, because `x_u = h_n U_{u−1}` is `G_{u−1}`-measurable and reveals nothing
  about `U_u`;
* the class `B^ctx+`, which the proposition explicitly quantifies over, nevertheless contains a
  strategy that gains `0.44 n`.

So the defence "(A3) is violated by your deviation" is exactly the point: it means the enlargement
is **not** free under (A2). A theorem of the form "for every `S' ∈ B^ctx+`, gain ≤ B" cannot be
rescued by observing that the witness violates a standing hypothesis; that is a statement that the
class is ill-posed under the hypothesis it is stated under, and the paper says the opposite. The
appendix was aware of the phenomenon — "It is not available under (A3) alone, where arrivals may
react to rewards and conditioning a target on a future arrival that is itself a function of that
target is not well posed" — but drew the line in the wrong place. **The line is not "arrivals react
to rewards"; it is "arrivals are informative about the current round's own draws."** Reacting to
*seeds* rather than to *rewards* is invisible to (A2), because a deviation cannot move a seed.

### 1.6 The repair (one clause)

Strengthen (A2) to:

> **(A2) Exogenous.** No agent's behaviour can change the realised sequence of contexts, **and the
> context sequence is independent of the mechanism's randomisations and of the reward seed array.**
> They need not be independent of one another, identically distributed, or random at all.

With that clause: conditioning on the whole path leaves every seed uniform given the pre-seed field,
so (A2) ⇒ (A3) becomes true, `B^ctx+` becomes well posed, and the proof's closing sentence — "The
bound is uniform in the arrival path and in the deviation, so integrating and then taking the
supremum is legitimate" (l. 1181) — becomes justified rather than assumed. Alternatively, state
part (i) over `B^ctx` and drop the `+`; then variant A still refutes the `sec2`/`sec4` version but
the appendix is safe.

Note this also fixes finding 6: the implicit conditioning on the arrival path, which the finite
proof performs explicitly (l. 160–172: "Under this conditioning every visit count `V_z`, every
Stage-1 pull round and the length of every local fallback are deterministic") and the continuum
proof performs silently, is legitimate exactly when the added clause holds.

### 1.7 Scripts

Two files, run with any Python ≥ 3.9 + numpy. (On this filesystem:
`<home>/projects/SAMBA/.venv_unity_gpu/bin/python`.)

`params.py`:

```python
import math
def params(n, K, D):
    g = math.ceil(n**(1.0/(D+3))); h = 1.0/g; J = g**D
    Ln = math.ceil(n**(2.0/(D+3))); ell = math.log(2*K*n**5)
    s = math.sqrt(ell/(2*Ln)); rho = math.sqrt(D)*h*math.log(math.e*n)
    return dict(g=g,h=h,J=J,Ln=Ln,ell=ell,s=s,rho=rho,sig=3*s+rho)

def bound_i(n,K,D,EJp=None):
    p = params(n,K,D); J=p['J']; Ln=p['Ln']; ell=p['ell']
    if EJp is None: EJp = min(J,n)
    e_bid = min(EJp*Ln,n); e_osc = n*p['rho']
    e_mon = EJp + 2*math.sqrt(EJp*n*ell/2.0)
    e_fb  = 11*math.sqrt(2*K*EJp*n*math.log(K)) + 2*K*math.log(K)*EJp*math.log2(2*(n+1))
    return e_bid+e_osc+e_mon+e_fb+4*n**-3+4*n**-2/K, p, dict(
        e_bid=e_bid,e_osc=e_osc,e_mon=e_mon,e_fb=e_fb,
        e_price=n*(4*p['s']+4.0/3.0*p['rho']),
        e_stage1=min(K*EJp*Ln,n))
```

`attack_seedleak.py` (variant A, chunked so `n = 10^9` fits in memory):

```python
import math, numpy as np
from params import params, bound_i

def run(n, K=2, D=1, M1=1.0, M2=0.9, seed=0, chunk=10_000_000):
    p = params(n,K,D); Ln=p['Ln']; ell=p['ell']; sig=p['sig']
    rng = np.random.default_rng(seed); ns1 = K*Ln
    U1 = rng.random(ns1)                       # Stage 1, round robin, agent 2 on even visits
    beta1, beta2 = 1.0, float(np.mean(U1[1::2] <= M2))
    assert beta1 > beta2                       # agent 1 is the unique largest bidder
    tau = max(0.0, beta2 - sig)                # beta_(2),C = beta_2
    nC = n - ns1; Z = 0; r0 = 0; worst = math.inf; cb = cd = 0.0; done = 0
    while done < nC:
        m = min(chunk, nC-done); U = rng.random(m)
        Uhat = (p['h']*U)/p['h']               # what the deviator reads off the context x_t
        mdev = np.where(Uhat<=tau, np.minimum(1.0,Uhat+1e-9), 0.0)
        y, ydev = (U<=tau), (U<=mdev)
        assert (y==ydev).all() and (mdev<=M1).all()   # identical reward path; feasible
        Zc = Z + np.cumsum(y); r = r0 + np.arange(1,m+1)
        worst = min(worst, float((Zc - r*tau + np.sqrt(r*ell/2.0)).min()))
        Z = int(Zc[-1]); r0 += m; done += m
        cb += tau*m; cd += float(np.sum(mdev))
    gain = cb - cd
    B,_,e = bound_i(n,K,D,EJp=1)
    print(n, "tau",tau, "gain",gain, "=",gain/n,"n", "bound",B, "ratio",gain/B,
          "monitor slack",worst)

for n in [10**7, 10**8, 10**9]: run(n)
```

Variant B is the same with `Uhat` read from `x_{t+1}` instead of `x_t` (one differing round at
`t = n`).

---

## 2. Finding 3 — "the leading constant is free of K", quantified

`sec4_contextual.tex` l. 150: "`K` enters only the constants, and the leading constant of the
incentive bound not at all." That is **true asymptotically**: of the four terms in (i),
`e_bid ≤ 2^{d+1} n^{(d+2)/(d+3)}` and `e_osc ≤ √d n^{(d+2)/(d+3)} log(en)` carry no `K`, while the
`K`-carrying `e_mon` and `e_fb` sit at the strictly smaller exponents `(2d+3)/(2d+6)` and
`d/(d+3)`. I re-derived the read-off arithmetic of the proof of `thm:ctx-private-continuum` term by
term and found **no error**: every displayed constant is correct and the exponent ordering is
correct.

But the crossover is polynomial in `K`, and it lands **above** the horizon at which the theorem
first says anything. Bisection on `log10 n` with `E[J'_n]` at its worst case `min{J_n, n}`, the
same method as `rem:ctx-horizons`. **Validation:** at `K = 2` my code reproduces all eighteen
printed figures of `rem:ctx-horizons` to the printed precision — `D = 1`: `10^6.1`, `10^5.2`,
`10^6.8`; `D = 2`: `10^8.5`, `10^7.5`, `10^9.3`; `D = 3`: `10^11.1`, `10^10.0`, `10^12.0`;
`D = 4`: `10^13.7`, `10^12.7`, `10^14.9`; `D = 6`: `10^19.4`, `10^18.4`, `10^20.8`; `D = 10`:
`10^31.7`, `10^30.7`, `10^33.7`. **That remark is arithmetically correct.** The table below is the
same computation carried to two decimals and extended in `K`:

| d | K | bound (i) first `< n` | `K`-free terms first lead | share of `e_mon + e_fb` in the bound at onset |
|---|---|---|---|---|
| 1 | 2 | 10^5.25 | 10^3.85 | 33 % |
| 1 | 5 | 10^5.67 | 10^5.15 | 44 % |
| 1 | **20** | 10^6.39 | **10^7.10** | **58 %** |
| 1 | **100** | 10^7.29 | **10^9.43** | **72 %** |
| 1 | **1000** | 10^8.68 | **10^12.94** | **85 %** |
| 2 | 100 | 10^9.45 | 10^10.24 | 57 % |
| 2 | 1000 | 10^11.04 | 10^14.37 | 76 % |
| 3 | 1000 | 10^13.48 | 10^15.90 | 68 % |

Read: for `K ≥ 20` there is a window — 0.7 decades at `K = 20`, **4.3 decades at `K = 1000`** — in
which the theorem is non-vacuous and the `K`-carrying terms are the *majority* of the paper's own
exact bound. `rem:ctx-horizons` tabulates `K = 2` only, where the claim happens to look clean, and
`PROVER_SC1`'s table goes only to `K = 3` and concludes "the thresholds are ... essentially
independent of `K`". That conclusion is an artifact of stopping at `K = 3`.

**Label: not a break.** The asymptotic statement is correct. But "the leading constant of the
incentive bound [carries K] not at all" is, at every horizon a reader could care about and any `K`
past about 20, the wrong summary of the paper's own inequality. I would add "for
`n ≳ (K log K)^{d+3}`" to that sentence.

## 3. Finding 4 — the `K`-carrying term is loose by a factor ≈ `K`

`lem:ctx-dev-fallback` bounds the deviator's fallback utility by
`(1 + μ_i^sup − ν_i(C))H + R^dbl_K(H) + ρ_n H/3`, where `R^dbl_K(H) ≈ 11√(K H log K)` is the EXP3
**regret**. That is a regret bound used as a deviation-gain bound, and the two differ by `K`. Trace
the worst case (`w_C = 0`, i.e. `τ_C = 1`, `μ_i = 0`): the deviator triggers a switch, then delivers
`0` forever. EXP3 down-weights it, so its pull count is its own exploration share,
`Σ_k γ_k 2^k / K ≈ 3.4 √(H log K / K)`, and its gain is `(1+μ_i)` times that. The lemma charges
`11 √(K H log K)`. The ratio is `≈ 3K`. Since `e_fb` is the term that carries `K` into (i) and
(iii), and since finding 3 is entirely about that term, this is worth fixing rather than noting: the
attainable fallback gain is `O(√(J'_n n log K / K))`, which *decreases* in `K`, and with it the
window in finding 3 largely closes. A referee who checks `lem:ctx-dev-fallback` against the actual
EXP3 dynamics will ask about this.

## 4. Finding 5 — the grid does not cover the declared context space

`sec2_model.tex` l. 74 and `sec4_contextual.tex` l. 18: `X = [0,1]^d`, and "the `J_n = b_n^d` cells
tile **the closed cube** exactly". `app_contextual_private.tex` l. 651: "the `J_n` **half-open**
cubes of side `h_n` tiling `[0,1)^d`", with primitives declared on `[0,1)^d` (l. 688). `J_n = g_n^d`
half-open cubes of side `1/g_n` tile `[0,1)^d`, **not** `[0,1]^d`: a context with any coordinate
equal to 1 lies in no cube and `C(x)` is undefined. Both prover reports noticed the discrepancy and
both dismissed it ("harmless", "nothing depends on it"). They are right that it is reparable — fold
the top faces into the last cell along each axis, so the extreme cells become `[1−h_n, 1]`; two
points of such a cell still differ by at most `h_n` per coordinate, so `ω = L√d h_n` and
`ω ≤ ρ_n/3` are unchanged — but as printed the mechanism is undefined on a set the model says is in
the context space, and `lem:ctx-osc` is stated for a partition that does not exist. **Label: gap in
the written proof, trivially reparable.** I also checked the harder version of this attack (brief
item 2): with `g_n = ⌈n^{1/(d+3)}⌉` and `h_n = 1/g_n` the side length divides `1` exactly, so there
are **no** truncated or partially covered cells and no cell has diameter larger than `√d h_n`; and
`ω ≤ ρ_n/3` ⟺ `L ≤ log(en)/3`, in which `√d` cancels on both sides exactly as claimed. **That
attack fails; the `n ≥ e^{3L}` threshold really is dimension-free.**

## 5. Finding 6 — a lemma stated unconditionally and used conditionally

`lem:ctx-fallback-cont` concludes `E[Σ Y_u] ≥ v E[H] − E[R^dbl_K(H)]`, an **unconditional**
expectation. `lem:ctx-dev-fallback` states
`E[U^fb_i(C) | fallback start] ≤ (1 + μ_i^sup − ν_i(C))H + R^dbl_K(H) + ρ_n H/3` — conditional on
the fallback-start field, with `H` appearing **un-expectated on the right**, hence treated as
measurable with respect to that field. The proof of (i) then multiplies it by `1_F`. Two things are
needed and neither is supplied:
1. the **conditional** form of `lem:ctx-fallback-cont` on the fallback-start field `G_fb` (all its
   steps do go through, since every tower step is on a `G^0_u ⊇ G_fb` for `u` after the switch —
   but the lemma as stated does not give it);
2. `H` being `G_fb`-measurable, which holds **only** after conditioning on the arrival path.

The finite-profile proof does the corresponding step explicitly and says why (l. 160–172: condition
on `A`, "every bound below is uniform in `A`, so integrating recovers the unconditional claim", and
then "every visit count `V_z`, every Stage-1 pull round and the length of every local fallback are
deterministic"). The continuum proof does it silently, in one clause at the very end of the proof of
(i) (l. 1181). **Label: gap in the written proof.** It is the same hole as finding 1 viewed from the
inside: conditioning on the path is exactly the step that fails when (A2) is read as printed.

---

## 6. What I checked and could not break

Recorded so the effort is not repeated. Each of these I pushed until I was convinced, not until I
got bored.

**(a) The read-off arithmetic.** Re-derived every displayed constant in the proof of
`thm:ctx-private-continuum`: `e_bid ≤ 2^{D+1} n^{(D+2)/(D+3)}` (from `J_n ≤ 2^D n^{D/(D+3)}`,
`L_n ≤ n^{2/(D+3)}+1`), `e_osc = √D n h_n log(en)`, `e_mon`'s two pieces, `e_fb`'s two pieces,
`e_price`, and the exponent ordering `(2D+4)/(2D+6) > (2D+3)/(2D+6) > D/(D+3)`. **All correct.**
Also re-derived the three concavity/Cauchy–Schwarz steps (`Σ_C[1+2b_n(n_C)] ≤ J' + 2√(J'nℓ_n/2)`,
`Σ_C R^dbl_K(n_C) ≤ 11√(2KJ'n log K) + 2K log K J' log₂(2(n+1))`, and Jensen for `e_bid`). All
correct.

**(b) The concentration constants.** `Pr(E^c) ≤ 2KJ_n e^{−ℓ_n} = J_n n^{−5} ≤ n^{−4}`;
`Pr(H^c) ≤ 2J_n n e^{−ℓ_n} = J_n/(Kn⁴) ≤ n^{−3}/K`; the Chernoff step `exp(−2L_n s_n²) = e^{−ℓ_n}`
with `λ = 4s_n`; `exp(−2b_n(r)²/r) = e^{−ℓ_n}` with `b_n(r) = √(rℓ_n/2)`; and the off-good-event
charge `2n·n·(2n^{−5} + 2K^{−1}n^{−4}) = 4n^{−3} + 4K^{−1}n^{−2}`. All correct. The union bounds run
over the **deterministic** set of grid cubes, so no measurability of the visited set is needed —
that really is airtight.

**(c) Brief item 3 — adversarial (A2) arrival tuned against `h_n = n^{−1/(d+3)}`.** I tried both
extremes and they are exactly balanced, not broken.
*Starvation:* give each of `J' = n/(KL_n − 1)` cubes exactly `KL_n − 1` visits, so **no cube ever
awards**. The deviator shirks every bidding pull and collects `≈ n/K`. The bound gives
`e_bid = J'L_n ≈ n/K`. **Tight, not violated.** This configuration needs `J' ≤ J_n`, i.e.
`K ≥ n^{1/(d+3)}`, in which regime `n/K ≤ n^{(d+2)/(d+3)}` — the two constraints are exactly
complementary, which is not an accident.
*Spreading:* `J_n` cubes with `n^{3/(d+3)}` visits each; every cube awards iff `K ≤ n^{1/(d+3)}`,
and then the deviator collects `J_n L_n = n^{(d+2)/(d+3)}` — again **exactly** `e_bid`.
*Concentration:* all visits in one cube. `e_bid` collapses to `L_n`, `e_mon` and `e_fb` collapse,
and only `e_osc = nρ_n` survives; this is the configuration finding 1 uses, and the honest remark is
that at `J'_n = 1` the bound of (i) is essentially `nρ_n` alone.
I could not find a `J'_n` in between that beats both branches of the `min`.

**(d) Brief item 4 — the shared context tells the deviator its rivals' capabilities exactly.** With
(A3) intact this buys nothing, and I now think the reason is structural rather than lucky:
* the deviator cannot raise its own bid (feasibility gives `β'_i ≤ β*_i` pathwise under the shared
  seed), so the only bid-side move is to *lose on purpose*;
* losing is never profitable, because `w_C = 1 + μ_i^inf(C) − τ_C ≥ 0` (as `τ_C ≤ 1 ≤ 1 + μ_i`), so
  the baseline's post-Stage-1 utility at a cube it wins is `≥ 0` and the deviating execution's is
  `0`;
* when it loses, the winner plays `S*` and `lem:ctx-price-meet` holds **whoever won and whatever
  anyone bid**, so no switch occurs and it cannot manufacture a fallback to free-ride in;
* when it wins, `τ_C = max_{j≠i} β_j − σ_n` does not involve its own bid, so timing its underbidding
  across cubes changes which cubes it wins, never at what price.
I tried timing the underbidding using knowledge of where the path goes next (which cubes will award,
which will be starved, which will be visited many times) — the Stage-1 saving is capped at `l_i(C) ≤
L_n` per cube by feasibility alone, and knowing the future only lets the deviator *attain* that cap
rather than exceed it. **Fails.**

**(e) Brief item 5 — `3s_n + ρ_n` versus the monitor boundary, jointly inconsistent at finite `n`.**
I could not construct one, and I now believe the two constants do not interact at all. The monitor's
soundness (`lem:ctx-monitor-cont`(d), no switch when every target `≥ τ_C`) holds on `H_C` for *every*
`r ≤ n` simultaneously and for any `τ_C ∈ [0,1]` — it is a statement about `|Z_r − A_r| ≤ b_n(r)`
and does not see `σ_n`. The monitor's completeness (`(b)`, `A_q ≥ qτ_C − 1 − 2b_n(q)`) likewise. So
"too much shading" and "too little shading" are not two sides of one constraint here; the only
casualty of over-shading is revenue, through `e_price`, and the only casualty of under-shading
would be `lem:ctx-price-meet`, which has `2s_n + (2/3)ρ_n` of slack left over after it is proved.
In my simulation the realised slack `min_r (Z_r − rτ_C + b_n(r))` was `+6.3` (`n = 10^8`) with
`b_n(n) ≈ 6.8·10^4` — an enormous margin, confirming the monitor never binds on a compliant winner
at any horizon I could reach. **Fails.**

**(f) Brief item 6 — the honest comparator's floor moves with the task.** The natural attack is to
make two honest agents cross inside a cube: `μ_1` high on the left half, `μ_2` high on the right, so
`b(x) = max_h μ_h(x)` is high everywhere while `v_C = max_h μ_h^inf(C)` is the max of two *low*
numbers. It fails, and for a reason worth recording: `lem:ctx-honest-floor`(i) takes the `inf` of
the **same** `h` that attains `b(x)`, so the loss is one agent's own oscillation `ω ≤ ρ_n/3`, never
the oscillation of the upper envelope. I checked every use of `v_C` in the proof of (iii) — the
Stage-2 branch (`W_C = h_C`, honesty pathwise), the Stage-1 bid branch
(`β_(2),C ≥ β_{h_C,C} ≥ v_C − s_n`, valid because `h_C ≠ W_C` forces `β_{h_C} ≤ β_(2)`), and the
fallback comparator (`E[Y_u | G^0_u, I_u = h_C] ≥ v_C` pathwise by honesty, hence no good event
needed) — and none of them treats the honest agent as having a horizon-fixed floor. **Fails.**

**(g) The case analysis of the proof of (i).** I walked all four combinations of
{wins under the deviation, loses under the deviation} × {wins in the baseline, loses in the
baseline}. The one that looks dangerous — wins in the baseline, loses under the deviation, which
`eq:ctx-win-inclusion` permits — is safe precisely because `w_C ≥ 0`. The honest-deviator
`w_C = min{1, 1 + μ_i^inf − τ_C}` branch and the "taking the smaller of the two bounds" step both
check out arithmetically in both sub-cases. `n_C = (V_C − KL_n)_+` is a function of the arrival
path alone, so it is the same number in both executions — which is what makes the comparison of
`U'^post` with `n_C w_C` a comparison of two sums over the *same* number of pulls, the thing
`rem:ctx-continuum-exogeneity` correctly identifies as what breaks under a reactive path.

**(h) Ties, perfect cross-agent dependence, vanishing gaps, large `L`, cube starvation** (the list
the brief said was closed). I re-verified the tie handling in `eq:ctx-win-inclusion` independently
(the argument is written with non-strict inequalities and a shared `Π_C`, so it survives `β'_i =
β_j` and `β*_i > β'_i = β_j` alike) and the absence of any cross-agent independence claim (every
inter-agent step is a deterministic order-statistic or feasibility inequality; the only
multi-agent probabilistic inputs are union bounds). **Both provers are right about these.** I found
nothing to add.

---

## 7. The single weakest step

If everything above were repaired, this is where a referee would still go, and it is where I spent
the most time before finding 1 crystallised:

> **The proof of `prop:ctx-continuum-exact`(i) conditions on the arrival path without saying so, and
> `sec2`'s (A2) does not license it.**

One sentence carries the whole of part (i): "The bound is uniform in the arrival path and in the
deviation, so integrating and then taking the supremum is legitimate" (l. 1181), together with the
unwritten assumption that makes `H` measurable at a cube's fallback start and makes the
`B^ctx → B^ctx+` enlargement free. The finite-profile proof discharges exactly this by conditioning
on `A` in a displayed paragraph and checking that `(∗)` survives the conditioning; the continuum
proof does not repeat that check, and the reason it cannot is that (A2), as printed, does not imply
`(∗)` survives. Everything else in this subsection — the three price lemmas, the two martingales,
the doubling-epoch fallback, the error-term bookkeeping — is, as far as I can break it, correct and
in several places tight. The vulnerability is entirely in the hypothesis that connects "a deviation
cannot move the path" to "the seeds are still fresh once you know the path", and the paper asserts
that connection in one unproved sentence in `sec2` ("Each condition implies the next") which is
false as the two conditions are written.
