# PROVER-SC-1: the shared-context specialisation of `prop:ctx-continuum-exact`

Source read in full: `sections/sec2_model.tex`; `sections/sec4_contextual.tex`;
`sections/app_contextual_private.tex`, subsection `app:ctx-private-continuum` (lines 626--1307),
including the mechanism paragraph, the hypothesis block, `lem:ctx-osc`, `lem:ctx-bidconc`,
`lem:ctx-price-meet`, `lem:ctx-price-dom`, `lem:ctx-price-second`, `lem:ctx-honest-floor`,
`lem:ctx-monitor-cont`, `lem:ctx-fallback-cont`, `lem:ctx-dev-fallback`, the error-term paragraph,
`prop:ctx-continuum-exact` with all three proofs, the proof of `thm:ctx-private-continuum`, and the
remarks `rem:ctx-endogenous`, `rem:ctx-continuum-exogeneity`, `rem:ctx-horizons`. The predecessor
subsection `app:ctx-private-finite` was read in full as well, since the continuum proof refers to it.
`app:ctx-private-net` was read, to make sure the present claim is not confused with the separation
stated there.

**Verdict in one line.** The claim is **TRUE as stated**, and the proof is an honest re-labelling: I
could not find a single step of `prop:ctx-continuum-exact` that uses the profile rather than the cell
label, and I could not build a counterexample. The three conclusions hold verbatim with $d$ in place
of $D$, the horizon threshold $n \ge \exp(3L)$ is unchanged (the $\sqrt{d}$ cancels on both sides of
$\omega \le \rho_n/3$), the exponent carries no $K$, and $K$ enters the leading constant of part (i)
not at all and the leading constant of parts (ii)/(iii) linearly. The one thing that is *not* free,
and that I flag rather than paper over, is that the improvement comes from **re-tuning** $(h_n,L_n)$
to $d$; lazy cell instantiation alone does not deliver it.

---

## 0. Notation and conventions inherited from the source

I keep every symbol of `app:ctx-private-continuum` unchanged and change only the space the grid is
laid on. Throughout, $K\ge 2$, $n$ is the known horizon, $\log$ is natural, and $\log_2$ is binary.
Following the source I write the context space as $[0,1)^d$ and tile it by half-open cubes; the
model section writes $[0,1]^D$, and the source subsection writes $[0,1)^D$. This discrepancy is
inherited, harmless and I do not repair it: nothing in any proof uses more about the cells than that
they form a fixed deterministic finite partition of the context space into sets of diameter at most
$\sqrt{d}\,h_n$. Folding the top faces into the last cell along each axis leaves every statement
below true verbatim.

---

## 1. The shared-context model

Identical to `sec:model-contextual` except for the arrival object.

**Contexts.** Each round carries a single **common context** $x_t \in [0,1)^d$, observed by the
platform before it selects, and observed by the selected agent before it chooses its target.

**Primitives.** For each $i\in[K]$ there are $\mu_i, M_i : [0,1)^d \to [0,1]$ with $\mu_i \le M_i$,
both $L$-Lipschitz in the Euclidean norm, $L\ge 0$ unknown to the platform. At round $t$ agent $i$'s
capability is $M_i(x_t)$ and its intrinsic mean is $\mu_i(x_t)$; if selected it chooses
$m_{i,t}\in[0,M_i(x_t)]$ and pays $c_{i,t}=m_{i,t}-\mu_i(x_t)$; the platform observes
$Y_t = \mathbf 1\{U_t\le m_{I_t,t}\}$.

Note that $\mu_i, M_i$ have exactly the domain they have in the source's hypothesis block, namely
$[0,1)^d$. The *only* change from the source model is that all $K$ of them are evaluated at the same
point of that domain. In the profile language this is $X_t=(x_t,\dots,x_t)$, a point of the diagonal
$\Delta:=\{(x,\dots,x)\}\subset[0,1)^{Kd}$.

**Derived quantities.** $M_\star(x):=\max_j M_j(x)$; $M_{(2)}(x)$ the second largest of
$(M_1(x),\dots,M_K(x))$ counting multiplicity; $b(x):=\max_{h\in\mathcal K_H}\mu_h(x)$ for a fixed
nonempty honest set $\mathcal K_H$. Honesty is pointwise: $h\in\mathcal K_H$ satisfies
$m_{h,t}\ge \mu_h(x_t)$ after every history.

**Strategy classes.** $\mathcal B^{\mathrm{sc}}_{i,n}$: after being selected at round $t$, agent $i$
chooses $m_{i,t}\in[0,M_i(x_t)]$ as an arbitrary measurable function of $n$, the current common
context $x_t$, its own entire history across all cells (its selection rounds, the contexts there, its
targets, its realised rewards, and every message the mechanism sent it, including cell phase labels
and cell prices), and its independent private randomisation. $\mathcal B^{\mathrm{sc}+}_{i,n}$ is the
same class enlarged by allowing the agent to condition in addition on the entire arrival sequence
$(x_1,\dots,x_n)$, hence on all future arrivals, on every visit count and on the exact global round
index. These are the source's $\mathcal B^{\mathrm{ctx}}_{i,n}$ and
$\mathcal B^{\mathrm{ctx}+}_{i,n}$ with $x_t$ in place of $X_t$, and the source's sentence about the
enlargement applies unchanged: it is free under (A2) and is not available under (A3) alone.

**Arrival hypotheses.** (A2) and (A3) exactly as in `sec:model-contextual`, restated for $x_t$. In
particular (A3) is used in, and only in, the conditional form quoted verbatim in §3 below. I do not
restate it as a list of independence clauses anywhere.

---

## 2. The mechanism SC-CG-MESP

This is CG-MESP with the grid on the common context space. The platform knows $n$, $K$ and $d$; it
does not know the arrival law, $L$, any $\mu_i$, any $M_i$, or $\mathcal K_H$. Put

$$g_n:=\lceil n^{1/(d+3)}\rceil,\quad h_n:=1/g_n,\quad J_n:=g_n^{\,d},\qquad
L_n:=\lceil n^{2/(d+3)}\rceil,\qquad \ell_n:=\log(2Kn^5),$$

$$s_n:=\sqrt{\frac{\ell_n}{2L_n}},\qquad
\rho_n:=\sqrt{d}\,h_n\log(en),\qquad \sigma_n:=3s_n+\rho_n,\qquad
b_n(r):=\sqrt{\frac{r\ell_n}{2}},\ \ b_n(0):=0,$$

$$R_K(H):=3\sqrt{KH\log K}+2K\log K,\qquad
R^{\mathrm{dbl}}_K(V):=11\sqrt{K(V+1)\log K}+2K\log K\log_2(2(V+1)),$$

with $R_K(0):=R^{\mathrm{dbl}}_K(0):=0$. The grid is the $J_n$ half-open cubes of side $h_n$ tiling
$[0,1)^d$; $C(x)$ is the cube containing $x$, and the position of $x$ inside its cube is used only to
locate the cube, so the rule is cell blind. Cubes are instantiated lazily on first arrival, so $J_n$
never has to be enumerated. Each cube keeps a visit counter $V_C$, the Stage-1 reward sums, the price
$\tau_C$, the winner $W_C$, the monitor count and reward sum, the local fallback clock and EXP3
weights, and one independent uniform priority permutation $\Pi_C$ drawn when $C$ is first met.

At round $t$ the platform observes $x_t$, sets $C:=C(x_t)$, increments $V_C$ and acts by $C$'s local
phase.

*Stage 1*, while $V_C\le KL_n$: pull agent $((V_C-1)\bmod K)+1$, so agent $i$'s $r$th bidding pull at
$C$ is the $((r-1)K+i)$th visit to $C$, and the schedule reads no reward, no bid and no coin; when
$V_C=KL_n$, form $\beta_{i,C}:=L_n^{-1}\sum_{r\le L_n}Y_{i,C,r}$, let $W_C$ be a largest bidder with
ties broken by highest $\Pi_C$ priority, let $\beta_{(2),C}$ be the second order statistic with
multiplicity, and announce

$$\tau_C:=\bigl(\beta_{(2),C}-\sigma_n\bigr)_+=\bigl(\beta_{(2),C}-3s_n-\rho_n\bigr)_+ .$$

A cube receiving fewer than $KL_n$ visits in the whole horizon never awards, never prices and never
monitors. *Stage 2*, until a local switch: pull $W_C$ and switch at the first local primary index $r$
with $Z_r<r\tau_C-b_n(r)$. *Stage 3*, after a switch at $C$: explicit-exploration EXP3 over all $K$
agents, restricted to visits to $C$, restarted in doubling epochs on the local fallback clock, epoch
$k\ge0$ covering local fallback times $2^k,\dots,2^{k+1}-1$ with fresh weights $w_{j,1}=1$,
$\gamma_k:=\min\{1/2,\sqrt{K\log K/2^k}\}$ and $\eta_k:=\gamma_k/K$; no local horizon is used. A
selected agent is told the current cube's phase and, in Stage 2 or 3, $\tau_C$.

$S^\star$: capability $M_i(x_t)$ at a bidding pull and at a fallback pull, and
$\min\{\tau_C, M_{W_C}(x_t)\}$, or $\max\{\mu_{W_C}(x_t),\min\{\tau_C,M_{W_C}(x_t)\}\}$ if honest, at
a Stage-2 pull.

**Running time.** With cubes hashed by their integer index vector, the per-round work is $O(d)$ to
locate the cube plus $O(K)$ to update the cube's state and, in Stage 3, to sample from $p_u$; total
$O(n(d+K))$ time and $O(\min\{J_n,n\}\cdot K)$ memory. Polynomial, indeed near-linear. Nothing of the
kind in `app:ctx-private-net` is involved.

---

## 3. The proposition

The hypotheses are stated in the source's form. (A3) is quoted in the conditional form and is not
converted to a list.

> **(A3), in the form used here.** Fix a round $u$ and define
> $\mathcal G^0_u:=\sigma(\mathcal G_{u-1},x_u)$,
> $\mathcal G^{k}_u:=\sigma(\mathcal G^{k-1}_u,\ \text{the mechanism's }k\text{th randomisation at }u)$,
> $\mathcal G^-_u:=\sigma(\mathcal G^{\kappa}_u,\ \text{the selected agent's coin at }u,\ m_{I_u,u})$,
> $\mathcal G_u:=\sigma(\mathcal G^-_u,U_u)$, where $\kappa$ is the number of randomisations the
> mechanism specifies at a round and the randomisations are indexed in the order the mechanism
> specifies them. At every round $u$ the mechanism's randomisations are drawn in the order the
> mechanism specifies them, and then the reward seed. Each of them has its specified law
> conditionally on the field generated by everything realised before it: the $k$th randomisation of
> the mechanism has its specified law conditionally on $\mathcal G^{k-1}_u$, and the seed $U_u$ is
> uniform on $[0,1]$ conditionally on $\mathcal G^-_u$, with $Y_u=\mathbf 1\{U_u\le m_{I_u,u}\}$. The
> selected agent's private randomisation and its target are drawn between the last mechanism
> randomisation and the seed and are unconstrained: whatever the agent's strategy specifies, they are
> part of everything realised before the seed, and the seed clause is stated conditionally on them.

For SC-CG-MESP, $\kappa=2$: (f1) the priority permutation $\Pi_{C(x_u)}$, if that cube is met for the
first time at round $u$, uniform on the permutations of $[K]$; (f2) the mechanism's selection, which
in Stages 1 and 2 is the deterministic function of the cube's state that the mechanism specifies and
in Stage 3 is a draw $I_u$ with the law $p_u$ computed from the cube's own EXP3 state; and then (f3)
the seed. Nothing is assumed about how the common contexts are generated: $x_u$ may be an arbitrary
measurable function of the entire past, including past rewards and past randomisations, plus fresh
randomness, provided only that it is realised before the round's own draws.

Error terms, with $J'_n$ the number of cubes the realised arrival path visits at least once:

$$e_{\mathrm{bid}}:=\min\{\mathbb E[J'_n]L_n,\,n\},\qquad
e_{\mathrm{stage1}}:=\min\{K\,\mathbb E[J'_n]L_n,\,n\},\qquad
e_{\mathrm{osc}}:=n\rho_n,$$

$$e_{\mathrm{mon}}:=\mathbb E[J'_n]+2\sqrt{\mathbb E[J'_n]\,n\ell_n/2},\qquad
e_{\mathrm{fb}}:=11\sqrt{2K\,\mathbb E[J'_n]\,n\log K}+2K\log K\,\mathbb E[J'_n]\log_2(2(n+1)),$$

$$e_{\mathrm{price}}:=n\bigl(4s_n+\tfrac43\rho_n\bigr).$$

---

> ### Proposition SC (Shared-context continuous-grid MESP, exact form)
>
> Assume $K\ge2$; a single common context $x_t\in[0,1)^d$ observed by the platform; capabilities and
> intrinsic means $\mu_i\le M_i:[0,1)^d\to[0,1]$, both $L$-Lipschitz in the Euclidean norm with $L\ge0$
> unknown to the platform; a fixed nonempty honest set; and
>
> $$\log(en)\ \ge\ 3L,\qquad\text{that is}\qquad n\ \ge\ \exp(3L). \tag{H}$$
>
> Run SC-CG-MESP. Then:
>
> **(i)** under **(A2)**, for every agent $i$ and every $S'_{i,n}\in\mathcal B^{\mathrm{sc}+}_{i,n}$,
> $$u_i(n;S'_{i,n},S^\star_{-i,n})-u_i(n;S^\star_n)\ \le\
> e_{\mathrm{bid}}+e_{\mathrm{osc}}+e_{\mathrm{mon}}+e_{\mathrm{fb}}+4n^{-3}+4K^{-1}n^{-2};$$
>
> **(ii)** under the seed clause of **(A3)** alone, with every agent playing $S^\star$,
> $$P(n;S^\star_n)\ \ge\ \mathbb E\sum_{t\le n}M_{(2)}(x_t)\ -\
> \bigl(e_{\mathrm{stage1}}+e_{\mathrm{price}}+O(n^{-2})\bigr);$$
>
> **(iii)** under the Stage-3 selection clause and the seed clause of **(A3)**, for every feasible
> behavioural profile in which each agent plays some strategy in $\mathcal B^{\mathrm{sc}}_{j,n}$ and
> every honest agent respects pointwise honesty, the deviating set being all of $[K]$ if it likes,
> $$P(n;S)\ \ge\ \mathbb E\sum_{t\le n}b(x_t)\ -\
> \bigl(e_{\mathrm{stage1}}+e_{\mathrm{price}}+e_{\mathrm{mon}}+e_{\mathrm{fb}}+O(n^{-2})\bigr).$$
>
> Parts (ii) and (iii) place no condition whatever on the arrival process. No condition on the top
> set, on the boundary of any cube, or on the mass of any cube is used anywhere, and no capability
> gap, no mass and no property of the arrival law appears in any of the seven error terms; the only
> instance-dependent hypothesis is (H).
>
> **Read-off.** For $n\ge n_1(d):=2^{d(d+3)/3}$ (which is $2.6$ for $d=1$, $10.1$ for $d=2$, $64$ for
> $d=3$) one has $J_n\le n$, and, using $\mathbb E[J'_n]\le\min\{J_n,n\}$ and
> $J_n=g_n^{\,d}\le 2^d n^{d/(d+3)}$,
> $$e_{\mathrm{bid}}\le 2^{d+1}n^{\frac{d+2}{d+3}},\qquad
> e_{\mathrm{stage1}}\le K2^{d+1}n^{\frac{d+2}{d+3}},\qquad
> e_{\mathrm{osc}}=\sqrt d\,nh_n\log(en)\le \sqrt d\,n^{\frac{d+2}{d+3}}\log(en),$$
> $$ns_n\le\sqrt{\ell_n/2}\;n^{\frac{d+2}{d+3}},\qquad
> e_{\mathrm{price}}\le\Bigl(4\sqrt{\ell_n/2}+\tfrac43\sqrt d\log(en)\Bigr)n^{\frac{d+2}{d+3}},$$
> $$e_{\mathrm{mon}}\le 2^dn^{\frac{d}{d+3}}+2^{\frac d2+1}\sqrt{\ell_n/2}\;n^{\frac{2d+3}{2d+6}},\qquad
> e_{\mathrm{fb}}\le 11\sqrt{2K\log K}\,2^{\frac d2}n^{\frac{2d+3}{2d+6}}
> +2^{d+1}K\log K\,n^{\frac{d}{d+3}}\log_2(2(n+1)).$$
> The three exponents occurring are $(d+2)/(d+3)=(2d+4)/(2d+6)$, $(2d+3)/(2d+6)$ and $d/(d+3)$, and
> the first strictly dominates the other two. Hence all three bounds are
> $O_{d,K}\bigl(n^{(d+2)/(d+3)}\log(eKn)\bigr)$, with the exponent independent of $K$.

**Corollary SC (general $\phi_i$).** Suppose instead $x_{i,t}=\phi_i(x_t)$ for maps
$\phi_i:[0,1)^d\to[0,1)^{d}$ with $\mathrm{Lip}(\phi_i)\le \Lambda$, and $\mu_i,M_i$ $L$-Lipschitz on
$[0,1)^{d}$. Put $\widetilde M_i:=M_i\circ\phi_i$, $\widetilde\mu_i:=\mu_i\circ\phi_i$; these are
$L\Lambda$-Lipschitz on $[0,1)^d$, and feasibility, honesty and the benchmarks
$M_{(2)}(X_t)$, $b(X_t)$ are exactly the corresponding quantities built from
$(\widetilde M_j,\widetilde\mu_j)$ at the single point $x_t$. Proposition SC therefore applies
verbatim with $L$ replaced by $L\Lambda$, so the only change is that (H) becomes
$n\ge\exp(3L\Lambda)$. **It is the same proof**, not an adaptation: the identity case is
$\phi_i=\mathrm{id}$, $\Lambda=1$. The platform does not need to know $\phi_i$, nor $\Lambda$, nor
even that a $\phi_i$ exists; it grids the observed variable, and $\phi_i$ appears only in the
analysis. The $\phi_i$ need not be injective, need not be distinct, and need not have the same domain
and codomain dimension.

---

## 4. Proof

### 4.1 The reduction principle (what the source proof actually depends on)

The whole of §4 rests on the following, which is a reading of `app:ctx-private-continuum` and not a
new argument. Inspect every occurrence of the symbol $D$ in that subsection. There are exactly seven
kinds, and they fall into exactly two roles:

* **the mechanism's parameters** $g_n=\lceil n^{1/(D+3)}\rceil$, $J_n=g_n^D$, the tiling of
  $[0,1)^D$, the platform's knowledge of $D$, and the counting bound $J_n\le2^Dn^{D/(D+3)}$
  — i.e. **the number of cells**;
* **$\omega:=L\sqrt D h_n$ in `lem:ctx-osc` and $\rho_n:=\sqrt D h_n\log(en)$**
  — i.e. **the within-cell oscillation of the primitives, and the allowance that pays for it**.

Nothing else in the subsection mentions $D$, and no step uses that $[0,1)^D$ is a product across
agents, that different agents' coordinates are different, that a context law exists, or that any cell
carries positive mass. Consequently:

> **Reduction principle.** `prop:ctx-continuum-exact` and all nine lemmas it uses are theorems about a
> triple (observed context space $\mathcal Z$; a fixed deterministic partition of $\mathcal Z$ into
> $J_n$ cells that the mechanism uses only as a label; a number $\omega$ that bounds, on every cell,
> the oscillation of every $M_j$ and every $\mu_j$), together with (A3) and, for part (i), (A2). They
> hold whenever $\omega\le\rho_n/3$ and $J_n\le n$.

In the shared-context case $\mathcal Z=[0,1)^d$, the partition is the $J_n=g_n^{\,d}$ cubes of side
$h_n$, and $\omega=L\sqrt d\,h_n$. Verifying the two side conditions is §4.2--4.3; §4.4 then walks
every lemma and every step of the three proofs and records that each transfers.

### 4.2 The oscillation constant and the horizon condition (H)

**Lemma SC-osc** (= `lem:ctx-osc` with $d$). Write $\omega:=L\sqrt d\,h_n$. Then
$M_j^{\sup}(C)-M_j^{\inf}(C)\le\omega$ and the same for $\mu_j$, for every $j$ and every cube $C$;
the same bound holds for the oscillation on $C$ of $M_\star$, of $M_{(2)}$ and of $b$. Moreover
$\omega\le\rho_n/3$, and for every $x\in C$, $M_j(x)-\omega\le\bar M_{j,C}\le M_j(x)+\omega$, where
$\bar M_{j,C}:=L_n^{-1}\sum_{r\le L_n}M_j(x_{t_{j,C,r}})$ and $t_{j,C,r}$ is the round of $j$'s $r$th
Stage-1 pull at $C$.

*Proof.* Two common contexts in the same cube differ by at most $h_n$ in each of the $d$ coordinates,
hence by at most $\sqrt d\,h_n$ in Euclidean norm, and each $\mu_j,M_j$ is $L$-Lipschitz; so each
oscillates by at most $L\sqrt d h_n=\omega$ on a cube. Order statistics are 1-Lipschitz in the
supremum norm, so $M_\star$, $M_{(2)}$ and $b$, being pointwise maxima and order statistics of the
$M_j$ resp. of $(\mu_h)_{h\in\mathcal K_H}$ at the *same* point $x$, oscillate by at most $\omega$ as
well. By (H), $L\sqrt d h_n\le\frac13\sqrt d h_n\log(en)=\rho_n/3$. The last claim holds because
$\bar M_{j,C}$ is an average of values of $M_j$ at contexts of $C$, hence lies in
$[M_j^{\inf}(C),M_j^{\sup}(C)]$. $\square$

**This is the whole of the answer to check 2, and it is the only place where one could have hoped for
a change of threshold.** The oscillation is $L\sqrt d h_n$, not $L\sqrt D h_n$. The allowance is
$\rho_n=\sqrt d h_n\log(en)$, not $\sqrt D h_n\log(en)$. The condition $\omega\le\rho_n/3$ reads

$$L\sqrt d\,h_n\ \le\ \tfrac13\sqrt d\,h_n\log(en)\iff L\le\tfrac13\log(en)\iff \log(en)\ge 3L,$$

and **the factor $\sqrt d$ cancels on both sides**, exactly as $\sqrt D$ did. So (H) is unchanged:
$n\ge\exp(3L)$ still suffices, and it neither weakens nor strengthens. (As in the source, (H) is the
slightly conservative sufficient form: $\log(en)=1+\log n\ge3L$ is equivalent to $n\ge e^{3L-1}$.)

Two footnotes on faithfulness. First, in the source `lem:ctx-osc` proves the genuine oscillation bound
$L\sqrt d h_n$ and then *weakens* it to $L\sqrt Dh_n$ so that it matches $\rho_n$'s $\sqrt D$; so the
source carries a factor $\sqrt{K}$ of slack at that point, and the shared-context version simply does
not create it. Second, `lem:ctx-osc`'s statement about $M_\star,M_{(2)},b$ is a statement about order
statistics of functions evaluated at a *common* argument; in the source they are evaluated at
different coordinates of the same profile, which is the harder case. The shared-context case is the
easier one, not a new one.

### 4.3 The counting condition $J_n\le n$

$J_n=g_n^{\,d}\le 2^dn^{d/(d+3)}$, so $J_n\le n$ as soon as $2^d\le n^{3/(d+3)}$, i.e.
$n\ge n_1(d)=2^{d(d+3)/3}$: $2.6$ for $d=1$, $10.1$ for $d=2$, $64$ for $d=3$. The source needs the
same with $D$, i.e. $n\ge 2^{D(D+3)/3}$, which at $K=3,d=2$ is $2^{18}=2.6\times10^5$. This is a
strict improvement and it is used in `lem:ctx-bidconc` ($2KJ_ne^{-\ell_n}=J_nn^{-5}\le n^{-4}$) and
`lem:ctx-monitor-cont`(a) ($2J_nne^{-\ell_n}=J_n/(Kn^4)\le n^{-3}/K$). Below that threshold every
bound of this section already exceeds the trivial bound $n$, exactly as the source says.

### 4.4 Step-by-step transfer

Everything below is the source's argument with $x_t$ read for $X_t$, a cube of $[0,1)^d$ read for a
cube of $[0,1)^D$, and $M_j(x_t)$ read for $M_j(x_{j,t})$. I state at each step which hypothesis is
used and what, if anything, had to be checked.

**(a) Cube locality.** The local phase at $C$, the bids $\beta_{\cdot,C}$, the price $\tau_C$, the
winner $W_C$, the switch time and the conditional selection distribution used at each Stage-3 visit to
$C$ are measurable functions of the visit count $V_C$, the rewards realised at visits to $C$, the
priority $\Pi_C$, and the fallback coins used at visits to $C$; no quantity computed at $C$ depends on
anything realised at a visit to another cube. *Proof:* every branch of the round rule reads only $C$'s
own state, and $C$'s state is updated only at visits to $C$. Unaffected by the shared context, because
the mechanism sees $x_t$ only through $C(x_t)$.

**(b) Feasibility, pathwise.** $\bar A_{j,C}\le\bar M_{j,C}$, where $\bar A_{j,C}$ averages the
targets actually delivered at $j$'s Stage-1 pulls at $C$. Immediate from $m_{j,C,r}\le M_j(x_{t_{j,C,r}})$.
No probability. Transfers.

**(c) `lem:ctx-bidconc`, predictable bid concentration, uniform over all behaviour.** Put
$\phi_s:=\mathbf 1\{$round $s$ is agent $j$'s Stage-1 pull at $C$ with local index at most $L_n\}$.
Whether round $s$ has that description is determined by $x_s$ and by the visit count and phase of $C$,
which are determined by $x_1,\dots,x_s$ and by rewards at rounds strictly before $s$; so $\phi_s$ is
$\mathcal G^0_s$-measurable and a fortiori $\mathcal G^-_s$-measurable. With
$M_t:=\sum_{s\le t}\phi_s(Y_s-m_{I_s,s})$, $c_t:=\sum_{s\le t}\phi_s$ and
$N_t:=\exp(\lambda M_t-\lambda^2c_t/8)$, the seed clause plus Hoeffding's lemma give
$\mathbb E[N_t\mid\mathcal G^-_t]\le N_{t-1}$ and $\mathbb E[N_n]\le1$; on the event that $C$
completes bidding $c_n=L_n$ and $M_n=L_n(\beta_{j,C}-\bar A_{j,C})$; Markov with $\lambda=4s_n$ gives
$\Pr\{|\beta_{j,C}-\bar A_{j,C}|>s_n\}\le 2e^{-\ell_n}$. With
$E_C:=\{|\beta_{j,C}-\bar A_{j,C}|\le s_n$ for every $j\in[K]\}$, $\Pr(E_C^c)\le2Ke^{-\ell_n}=n^{-5}$
and, by a union bound over the **deterministic** set of $J_n$ grid cubes and the $K$ agents,
$\Pr(E^c)\le 2KJ_ne^{-\ell_n}=J_nn^{-5}\le n^{-4}$ using §4.3.

*What had to be checked, and this is the heart of the adversarial question about perfect dependence:*
the union bound over $j\in[K]$ is a **union bound**, not an independence step. No step of
`lem:ctx-bidconc` asserts, needs, or uses that the $K$ bids are independent, or that any bid
concentrates around a capability. Each $\beta_{j,C}$ is compared with $\bar A_{j,C}$, *its own*
delivered-target average, through a martingale written in the **global** filtration. Perfect
dependence of $(M_1,\dots,M_K)$ as functions is therefore invisible to this lemma. This is the correct
answer to "the agents' capabilities are perfectly dependent across agents rather than independent":
the source proof never used cross-agent independence to begin with, which one can see directly from
the fact that it is stated "uniform over all behaviour", and behaviour is allowed to be arbitrarily
correlated across agents.

**(d) `lem:ctx-price-meet`, the winner meets the price at every context of its cube.** On $E_C$, for
every $x\in C$, $\tau_C\le(M_W(x)-2s_n-\tfrac23\rho_n)_+\le M_W(x)$. *Proof:* $W$ is a largest bidder
so $\beta_{(2),C}\le\beta_{W,C}$ (an order-statistic fact, no probability); on $E_C$,
$\beta_{W,C}\le\bar A_{W,C}+s_n$; by (b), $\bar A_{W,C}\le\bar M_{W,C}$; by Lemma SC-osc,
$\bar M_{W,C}\le M_W(x)+\omega\le M_W(x)+\rho_n/3$ for every $x\in C$. Chaining,
$\beta_{(2),C}-\sigma_n\le M_W(x)+\rho_n/3+s_n-3s_n-\rho_n=M_W(x)-2s_n-\frac23\rho_n$; taking positive
parts preserves the inequality. Holds whoever $W$ is, whether or not $W$ is deviating, and whatever
any agent bid.

*Checked:* $\bar M_{W,C}$ averages $M_W$ over the contexts at $W$'s **own** Stage-1 rounds at $C$,
which are different rounds from the other agents' Stage-1 rounds and hence different contexts. That
was already the case in the source. All the lemma needs is
$\bar M_{W,C}\in[M_W^{\inf}(C),M_W^{\sup}(C)]$, which Lemma SC-osc supplies. The oscillation of $M_W$
over a cell is $L\sqrt d h_n$ here, as asked in check 2, and $\rho_n=\sqrt d h_n\log(en)$ dominates it
by a factor 3 under (H).

Two consequences used repeatedly, verbatim from the source: on $E_C$, at every Stage-2 pull at $C$ the
winner's $S^\star$ target $\min\{\tau_C,M_W(x_t)\}$ equals $\tau_C$ and the honest variant is at least
$\tau_C$, so $S^\star$ delivers a constant during Stage 2 at a cube and the cube's monitor is a test
against a constant; and if the deviator $i$ is the winner then $\tau_C\le M_i(x)$ at every context of
$C$, so $S^\star_i$ is feasible against the announced price everywhere in the cube — there is no
non-top branch, no capability gap, and no threshold of the form $4s_n\le\delta_i$.

**(e) `lem:ctx-price-dom`.** Fix $i$, all $j\ne i$ playing $S^\star$, and put
$\nu_i(C):=\max_{j\ne i}M_j^{\inf}(C)$. On $E_C$, $\tau_C\le\nu_i(C)$. *Proof:* let $j^*$ attain
$\max_{j\ne i}\beta_{j,C}$; if $i$ is a largest bidder then $\beta_{(2),C}=\max_{j\ne i}\beta_{j,C}$,
otherwise $W\ne i$ and $\beta_{(2),C}\le\beta_{W,C}\le\beta_{j^*,C}$; either way
$\beta_{(2),C}\le\beta_{j^*,C}$ with $j^*\ne i$. Since $j^*$ plays $S^\star$,
$\bar A_{j^*,C}=\bar M_{j^*,C}$, so on $E_C$
$\beta_{j^*,C}\le\bar M_{j^*,C}+s_n\le M_{j^*}^{\inf}(C)+\omega+s_n$, whence
$\tau_C\le M_{j^*}^{\inf}(C)+\omega+s_n-3s_n-\rho_n\le M_{j^*}^{\inf}(C)-2s_n-\frac23\rho_n\le\nu_i(C)$.
Transfers; no cross-agent independence.

**(f) `lem:ctx-price-second`.** Under $S^\star$ by everyone, on $E_C$ and for every $x\in C$,
$\tau_C\ge M_{(2)}(x)-4s_n-\frac43\rho_n$. *Proof:* $\bar A_{j,C}=\bar M_{j,C}$ for every $j$, so on
$E_C$, $\beta_{j,C}\ge\bar M_{j,C}-s_n\ge M_j(x)-\omega-s_n$ for **every** $j$ simultaneously; the
second order statistic is nondecreasing in each argument, so
$\beta_{(2),C}\ge M_{(2)}(x)-\omega-s_n$; subtract $\sigma_n$ and use $\omega\le\rho_n/3$.
*Checked:* this is the one lemma that needs all $K$ bid inequalities **at once**, and it gets them
from $E_C$, which is an intersection over $j$ obtained by a union bound in (c). Not by independence.
With a common context, $M_{(2)}(x)$ is the second largest of $K$ values of functions of the same
variable; monotonicity of order statistics is unaffected.

**(g) `lem:ctx-honest-floor`.** $v_C:=\max_{h\in\mathcal K_H}\mu_h^{\inf}(C)$, $h_C$ attaining it with
a fixed tie break. (i) $b(x)\le v_C+\omega$ for every $x\in C$: let $h$ attain $b(x)=\mu_h(x)$; then
$\mu_h(x)\le\mu_h^{\inf}(C)+\omega\le v_C+\omega$. (ii) under any behaviour respecting pointwise
honesty, $m_{h_C,t}\ge\mu_{h_C}(x_t)\ge\mu_{h_C}^{\inf}(C)=v_C$ at every round with $x_t\in C$ at
which $h_C$ is selected. (iii) on $E^H_C:=\{\beta_{h_C,C}\ge\bar A_{h_C,C}-s_n\}$, of probability at
least $1-e^{-\ell_n}$ by the one-sided form of (c), $\beta_{h_C,C}\ge v_C-s_n$. Transfers verbatim.

**(h) `lem:ctx-monitor-cont`, the monitor, and its boundary.** This is check 3. The boundary
$b_n(r)=\sqrt{r\ell_n/2}$ with $\ell_n=\log(2Kn^5)$ **contains no $D$ and no $d$**, and is therefore
literally unchanged. What had to be re-examined is the predictable indicator, which is the only place
the profile is read. Let $\psi_s:=\mathbf 1\{$round $s$ is a Stage-2 pull at $C\}$, $T_r$ the round of
the $r$th such pull with $T_r:=n$ if there are fewer than $r$, and $\phi_s:=\psi_s\mathbf1\{s\le T_r\}$.
Then $\phi_s$ is $\mathcal G^0_s$-measurable: whether round $s$ is a Stage-2 pull at $C$ is determined
by **$x_s$** (does it lie in $C$), by the visit count of $C$, which is determined by $x_1,\dots,x_s$,
and by whether $C$ has awarded and not yet switched, a function of rewards at rounds strictly before
$s$; and $\{s\le T_r\}$ says that fewer than $r$ Stage-2 pulls at $C$ have occurred before $s$, again
a function of the past. The rest is the source's supermartingale
$N_t=\exp(\lambda M_t-\lambda^2 c_t/8)$ with $\mathbb E[N_n]\le1$, giving
$\Pr(|Z_r-A_r|>b_n(r))\le2e^{-\ell_n}$, and the union bound over the deterministic set of $J_n$ cubes
and $r\le n$: $2J_nne^{-\ell_n}=J_n/(Kn^4)\le n^{-3}/K$ by §4.3. Parts (b)--(e) are pathwise
consequences or an optional stopping at the bounded time $n$; the only profile-flavoured object in
them is part (c)'s $\sum_{r\le q}(1+\mu_W(x_{W,r})-\tau_C)$, which reads
$\sum_{r\le q}(1+\mu_W(x_{t_r})-\tau_C)$ with $x_{t_r}$ the common context at the $r$th Stage-2 pull.
Nothing else referred to the profile. Transfers.

**(i) `lem:ctx-fallback-cont` and `lem:ctx-dev-fallback`, the fallback.** This is check 5. Structure:
$\phi_u:=\mathbf1\{$round $u$ is a fallback visit to $C\}$ and the doubling-epoch index $k(u)$ are
$\mathcal G^0_u$-measurable, because the local clock counts previous fallback visits to $C$ and $x_u$
tells whether round $u$ is a visit to $C$; the weights, hence $q_u,p_u$, are functions of the cube's
own past fallback data, so $\mathcal G^0_u$-measurable; the Stage-3 selection clause of (A3) then
gives $\mathbb E[\mathbf 1\{I_u=j\}\mid\mathcal G^0_u]=p_{j,u}$ by the tower property. The pathwise
per-epoch potential inequality is summed with $T_k\le 2^k$ and
$\gamma_k=\min\{1/2,\sqrt{K\log K/2^k}\}$, giving
$\mathbb E[\sum_{\text{fallback pulls at }C}Y_u]\ge v\,\mathbb E[H]-\mathbb E[R^{\mathrm{dbl}}_K(H)]$
for any comparator $j^*$ with conditional mean at least $v$ whenever selected at $C$. Nothing in this
depends on the dimension or on the profile: $R^{\mathrm{dbl}}_K$ is a function of $K$ and the local
length only. The deviator's version, `lem:ctx-dev-fallback`, uses in addition that every non-deviator
$j'$ delivers at most $M_{j'}^{\sup}(C)\le M_{j'}^{\inf}(C)+\omega\le\nu_i(C)+\rho_n/3$, which is
Lemma SC-osc; it yields
$\mathbb E[U^{\mathrm{fb}}_i(C)\mid\text{fallback start}]\le(1+\mu_i^{\sup}(C)-\nu_i(C))H
+R^{\mathrm{dbl}}_K(H)+\frac13\rho_nH$, and $\le H$ for honest $i$.

*Accounting, including the number of cells.* The per-cube charges are summed by Cauchy--Schwarz:
$\sum_C R^{\mathrm{dbl}}_K(n_C)\le 11\sqrt{K\log K}\sqrt{J'_n\sum_C(n_C+1)}
+2K\log K\,J'_n\log_2(2(n+1))\le 11\sqrt{2KJ'_nn\log K}+2K\log K\,J'_n\log_2(2(n+1))$, using
$\sum_Cn_C\le n$ and $J'_n\le n$; and $\sum_C[1+2b_n(n_C)]\le J'_n+2\sqrt{J'_n n\ell_n/2}$. Both are
concave in $J'_n$ through a square root, so Jensen gives the displayed $e_{\mathrm{fb}}$,
$e_{\mathrm{mon}}$ with $\mathbb E[J'_n]$. **The number of cells is now $J_n=g_n^{\,d}\le2^dn^{d/(d+3)}$
rather than $g_n^{\,D}$**, which is the only change, and it makes both terms
$O(n^{(2d+3)/(2d+6)})$, strictly below the pricing exponent $(d+2)/(d+3)$. The fallback is therefore
not binding, exactly as in the source.

**(j) Bid domination and elicitation, part (i).** This is check 4. Couple the deviating execution
(primes) with the baseline (stars) by the same arrival path, seed array, priorities, EXP3 coins and
private coins. Under **(A2)** the Stage-1 schedule at $C$ is a function of the arrival path alone — the
$k$th visit to $C$ goes to agent $((k-1)\bmod K)+1$, and the schedule reads no reward, no bid and no
coin — so the two executions have the same Stage-1 rounds at $C$ and pull the same agent at each. For
$j\ne i$ the Stage-1 rewards are identical because $S^\star_j$ delivers the deterministic number
$M_j(x_t)$ there whatever the history. At $i$'s Stage-1 round $t$, feasibility gives
$m'_{i,t}\le M_i(x_t)$, so with the shared seed
$\mathbf 1\{U_t\le m'_{i,t}\}\le\mathbf 1\{U_t\le M_i(x_t)\}$ and hence
$\beta'_{i,C}\le\beta^\star_{i,C}$ pathwise. Since the other bids agree and the tie break $\Pi_C$ is
shared, every inequality defining that $i$ is a largest bidder is preserved, so

$$\{i\text{ wins at }C\text{ under the deviation}\}\subseteq\{i\text{ wins at }C\text{ in the baseline}\},$$

and on that event $\beta_{(2),C}=\max_{j\ne i}\beta_{j,C}$ in both executions, so $\tau_C$ is the same
number in both and does not depend on anything $i$ does.

*Explicitly checked, since ties are unavoidable here.* If $i$ wins under the deviation then
$\beta'_{i,C}\ge\beta_{j,C}$ for all $j\ne i$ and $i$ has the highest $\Pi_C$ priority in the
deviating tie set. In the baseline the maximum bid is
$\max\{\beta^\star_{i,C},\max_{j\ne i}\beta_{j,C}\}=\beta^\star_{i,C}$, since
$\beta^\star_{i,C}\ge\beta'_{i,C}\ge\max_{j\ne i}\beta_{j,C}$. If $\beta^\star_{i,C}>\beta'_{i,C}$ then
no $j\ne i$ can attain it and $i$ wins outright; if $\beta^\star_{i,C}=\beta'_{i,C}$ the tie set and
the priority are unchanged and $i$ wins again. This matters more in the shared-context case than in
the source, because with $M_1\equiv M_2$ exact bid ties have large probability; the argument is
written without a strict inequality and survives.

*Stage-1 accounting.* The two executions are pulled at the same rounds and the per-pull utility
difference is $M_i(x_t)-m'_{i,t}\in[0,1]$, so the Stage-1 difference at $C$ is at most the number
$l_i(C)\le L_n$ of Stage-1 pulls $i$ receives there, and $\sum_C l_i(C)\le\min\{J'_nL_n,n\}$. Cubes
with $V_C<KL_n$ contribute only this term, since they never award.

*Post Stage-1.* On $E_C\cap\mathcal H_C\cap E^\star_C\cap\mathcal H^\star_C$: if $i$ does not win at
$C$ under the deviation, the winner $W\ne i$ plays $S^\star$, so by (d) its Stage-2 target is at least
$\tau_C$ at every context of $C$, by (h)(d) no switch occurs, $i$ receives no post Stage-1 pull, and
the baseline's post Stage-1 utility is nonnegative, so the contribution is at most $0$. If $i$ wins,
it wins in the baseline too at the same price; with $n_C=q+H$ and

$$w_C:=1+\mu_i^{\inf}(C)-\tau_C\ \text{(strategic)},\qquad
w_C:=\min\{1,1+\mu_i^{\inf}(C)-\tau_C\}\ \text{(honest)},$$

nonnegative because (d) gives $\tau_C\le M_i(x)\le1\le1+\mu_i^{\inf}(C)$, the monitor bound (h)(c)
with $\mu_i^{\sup}(C)\le\mu_i^{\inf}(C)+\rho_n/3$ gives
$U'^{\mathrm{pri}}\le qw_C+q\rho_n/3+1+2b_n(q)$, and (i) with (e) (which supplies
$\nu_i(C)\ge\tau_C$ and needs only $E_C$) gives
$\mathbb E[U'^{\mathrm{fb}}\mid\text{fallback start}]\le Hw_C+\frac23\rho_nH+R^{\mathrm{dbl}}_K(H)$;
adding,
$\mathbb E[U'^{\mathrm{post}}_{i,C}]\le n_Cw_C+n_C\rho_n+1+2b_n(n_C)+R^{\mathrm{dbl}}_K(n_C)$.
On $E^\star_C$ the baseline delivers at least $\tau_C$ at every Stage-2 pull, so by (h)(d) it never
switches at $C$, receives all $n_C$ post Stage-1 pulls with per-pull utility at least $w_C$, and the
difference is at most $n_C\rho_n+1+2b_n(n_C)+R^{\mathrm{dbl}}_K(n_C)$.

*Legitimacy of the conditioning* is the source's argument, unchanged: only two conditional
expectations are taken, both at $C$'s fallback-start field; $E_C$, $\mathcal H_C$ and $E^\star_C$ are
measurable there ($\mathcal H_C$ because the Stage-2 martingale at $C$ is frozen once the switch
occurs); $\mathcal H^\star_C$ is not, and is charged separately at
$2n_C\Pr((\mathcal H^\star_C)^c)\le 2n_C\cdot 2ne^{-\ell_n}$, summing to $2n^{-3}/K$. The global events
$E,\mathcal H$ are deliberately not used.

*Bad events and summation.* $\Pr(\mathrm{bad}_C)\le 2n^{-5}+2K^{-1}n^{-4}$ per cube, and
$\sum_C\mathbb E[(U'_{i,C}-U^\star_{i,C})\mathbf 1_{\mathrm{bad}_C}]\le 2n\cdot n\cdot
(2n^{-5}+2K^{-1}n^{-4})=4n^{-3}+4K^{-1}n^{-2}$. Finally $\sum_Cn_C\le n$ gives
$\sum_Cn_C\rho_n\le e_{\mathrm{osc}}$, and the two Cauchy--Schwarz steps of (i) give
$e_{\mathrm{mon}}$ and $e_{\mathrm{fb}}$, with concavity/Jensen for $\mathbb E[J'_n]$. The bound is
uniform in the arrival path and in the deviation, so integrating and then taking the supremum is
legitimate. This proves **(i)**. $\square$

**(k) Part (ii).** All agents play $S^\star$, so $\bar A_{j,C}=\bar M_{j,C}$ for every $j$ and $C$. By
the seed clause and the tower property $P(n;S^\star)=\mathbb E[\sum_{t\le n}m_{I_t,t}]$. Discard the
at most $\min\{KJ'_nL_n,n\}$ Stage-1 rounds, at which the target is nonnegative and $M_{(2)}\le1$.
Work on $E_C\cap\mathcal H_C$ cube by cube. By (d) the Stage-2 target at an awarded cube is at least
$\tau_C$ at every context, so by (h)(d) no cube ever switches: every post Stage-1 round is a Stage-2
round and the fallback lemma is never invoked. By (f), for every post Stage-1 round $t$ with
$x_t\in C$, $m_{I_t,t}\ge\tau_C\ge M_{(2)}(x_t)-4s_n-\frac43\rho_n$. Summing over cubes and charging
$E_C^c\cup\mathcal H_C^c$ at $n_C$ rounds each over the deterministic set of $J_n$ cubes gives (ii).
No fallback regret term is needed; no conditional expectation is ever multiplied by an indicator; the
mechanism's own randomisation never enters; and (d), (f) hold for whoever wins, so the tie break needs
no probabilistic property. **Only the seed clause of (A3) is used.** $\square$

**(l) Part (iii).** Every agent may play any strategy subject to feasibility and, for
$h\in\mathcal K_H$, pointwise honesty. Again $P(n;S)=\mathbb E[\sum_tm_{I_t,t}]$ and the Stage-1
rounds are discarded. Fix an awarding cube $C$, take $v_C,h_C$ from (g) and work on
$E^H_C\cap\mathcal H_C$. If $W_C=h_C$, every Stage-2 target at $C$ is at least
$\mu_{h_C}(x_t)\ge v_C$ by honesty, so the Stage-2 target sum is at least $v_Cq$; if a switch occurs,
the fallback lemma with the comparator $h_C$ and $v=v_C$, legitimate by (g)(ii) which is pathwise and
holds whatever the other agents do, gives at least $v_CH-\mathbb E[R^{\mathrm{dbl}}_K(H)]$. If
$W_C\ne h_C$ then $\beta_{(2),C}\ge\beta_{h_C,C}\ge v_C-s_n$, so $\tau_C\ge v_C-4s_n-\rho_n$; on
$\mathcal H_C$, (h)(b) gives $A_q\ge q\tau_C-1-2b_n(q)$, and a switch is covered by the fallback lemma
with comparator $h_C$ again. By (g)(i), $v_C\ge b(x_t)-\omega\ge b(x_t)-\rho_n/3$ for every
$x_t\in C$, so the post Stage-1 contribution of $C$ is at least
$\sum b(x_t)-n_C(4s_n+\frac43\rho_n)-1-2b_n(n_C)-R^{\mathrm{dbl}}_K(n_C)$. Summing with the two
concavity steps and charging the complements over the deterministic set of $J_n$ cubes gives (iii),
uniformly over the joint behavioural profile. The source's two care points transfer unchanged: the
case split $\{W_C=h_C\}$ and $E^H_C$ are both determined by the Stage-1 bids at $C$, hence at $C$'s
award round, which precedes every Stage-2 pull at $C$, so the stopped martingale argument of (h)
applies with that indicator inserted into $\phi_s$; and $\mathcal H_C$ is not award-time measurable
and is not multiplied by a conditional expectation, being handled by $A_q\ge0$ and
$\mathbb E[q\tau_C\mathbf 1_{\mathcal H_C^c}]\le n\Pr(\mathcal H_C^c)$. **Only the Stage-3 selection
clause and the seed clause of (A3) are used.** $\square$

**(m) Read-off.** $g_n\le 2n^{1/(d+3)}$ so $J_n\le 2^dn^{d/(d+3)}$; $L_n\le 2n^{2/(d+3)}$;
$h_n\le n^{-1/(d+3)}$; $L_n\ge n^{2/(d+3)}$ so $ns_n\le\sqrt{\ell_n/2}\,n^{(d+2)/(d+3)}$. Substituting
gives the seven displayed bounds of the Proposition; the exponents are $(2d+4)/(2d+6)$,
$(2d+3)/(2d+6)$, $(2d)/(2d+6)$ and the first strictly dominates. $\square$

---

## 5. Report on the eight required checks

**1. Cell-blindness / conditional i.i.d. reduction.** *It is not used by this proposition at all, and
I want to be exact about that.* The conditional i.i.d. statement of `sec:ctx-partition` ("conditional
on any realized ex ante strategy map, this cell-blind restriction makes each agent's observations in a
cell i.i.d. Bernoulli with its conditional cell-average mean") belongs to the public results,
`thm:grid-ucb-robust` and `thm:grid-etc`, which are stated over $\mathcal S_{\mathrm{HDS}}$ under
(A1). `prop:ctx-continuum-exact` never invokes it; its proof says so explicitly ("this is a
decomposition of a random variable and not an independence claim"). What the proposition does use is
two things:
  * **cube locality** — a construction-level measurability statement: no quantity computed by the
    mechanism at $C$ depends on anything realised at a visit to another cube. Verified in §4.4(a);
    it survives because the mechanism reads $x_t$ only through $C(x_t)$.
  * **the conditional law of each fresh draw given everything realised before it**, i.e. (A3) in the
    quoted form. The precise conditional independences used are exactly three, and no others:
    (α) $\mathbb E[Y_u\mid \mathcal G^-_u]=m_{I_u,u}$ with conditional range 1, used in §4.4(c),(h);
    (β) $\mathbb E[\mathbf 1\{I_u=j\}\mid\mathcal G^0_u]=p_{j,u}$ at a Stage-3 round, used in
    §4.4(i); (γ) the priority $\Pi_C$ has its uniform law given the field preceding it, used only to
    make the tie break well defined. Each is a statement about one draw conditionally on everything
    determined before it, and none is a statement about two named quantities being independent of each
    other. Every one of them is about a **round**, not about a **context coordinate**, and so is
    entirely blind to whether the $K$ agents' capabilities are driven by one variable or by $K$.

  For completeness, since the question was asked: the conditional i.i.d. statement itself *would* still
  hold under shared contexts and (A1). Given the cell, the within-cell common contexts are i.i.d. from
  $\nu(\cdot\mid C)$ across visits; the selection at a visit is cell-blind hence conditionally
  independent of the position of $x$ inside $C$; so a fixed agent's observations at its own visits to
  $C$ are i.i.d. Bernoulli with mean $\mathbb E[m_j(x)\mid x\in C]$. Perfect dependence of
  $(M_1,\dots,M_K)$ across agents does not disturb this, because two agents are never selected at the
  same round and different rounds carry independent contexts and independent seeds. So even the
  statement that is *not* needed survives.

**2. The price lemma and the oscillation.** Verified in §4.2 and §4.4(d). The oscillation of $M_i$
over a cell is $L\sqrt d\,h_n$ here (in the source the true value is also $L\sqrt d h_n$, weakened
there to $L\sqrt D h_n$ to match $\rho_n$). With $\rho_n=\sqrt d\,h_n\log(en)$ the requirement
$\omega\le\rho_n/3$ becomes $\log(en)\ge 3L$ **with the $\sqrt d$ cancelling on both sides**, so
$n\ge\exp(3L)$ is exactly the right threshold and is **unchanged**. `lem:ctx-price-meet` then gives,
on $E_C$ and for every $x\in C$, $\tau_C\le (M_W(x)-2s_n-\frac23\rho_n)_+\le M_W(x)$ — the winner
meets the price at **every** context of its cell, whoever it is and however it bid.

**3. Monitoring martingale and boundary.** Verified in §4.4(h). The boundary $b_n(r)=\sqrt{r\ell_n/2}$
and $\ell_n=\log(2Kn^5)$ contain no dimension at all and are literally unchanged. The one thing that
referred to the profile is the predictable indicator $\psi_s$; it is $\mathcal G^0_s$-measurable
because whether round $s$ is a Stage-2 pull at $C$ is determined by $x_s$, by the visit count of $C$
(a function of $x_1,\dots,x_s$), and by whether $C$ has awarded and not yet switched (a function of
rewards strictly before $s$). The union bound runs over the deterministic set of $J_n=g_n^{\,d}$ grid
cubes, which is what changes, improving the side condition $J_n\le n$ from $n\ge 2^{Kd(Kd+3)/3}$ to
$n\ge2^{d(d+3)/3}$. Part (c)'s $\mu_W(x_{W,r})$ reads $\mu_W(x_{t_r})$. Nothing else.

**4. Bid domination / elicitation.** Verified in §4.4(j). All five ingredients transfer: the Stage-1
schedule is a function of the arrival path alone (reward-independent round robin over visits to $C$);
non-deviators' Stage-1 rewards are identical across the two executions because $S^\star_j$ delivers
the deterministic $M_j(x_t)$; the deviator's bid is dominated pathwise by feasibility at the **common**
context and the shared seed; the win-inclusion and price-identity survive ties, which I checked
explicitly because with a common context exact ties (e.g. $M_1\equiv M_2$) are common; and the Stage-1
utility difference is at most one per pull, giving $\sum_Cl_i(C)\le\min\{J'_nL_n,n\}$. The elicitation
charge is therefore $e_{\mathrm{bid}}\le 2^{d+1}n^{(d+2)/(d+3)}$, with **no $K$**.

**5. Fallback and its regret accounting.** Verified in §4.4(i). The per-cell fallback is EXP3 over $K$
arms with doubling restarts on the cell's own fallback clock, charged $R^{\mathrm{dbl}}_K(n_C)$; the
lemma's measurability is in terms of rounds, not coordinates, and the Stage-3 selection clause is used
exactly once and is not a formality. Summation over cells by Cauchy--Schwarz with $\sum_Cn_C\le n$ and
$J'_n\le n$ gives
$e_{\mathrm{fb}}\le 11\sqrt{2K\log K}\,2^{d/2}n^{(2d+3)/(2d+6)}+2^{d+1}K\log K\,n^{d/(d+3)}\log_2(2(n+1))$.
The **number of cells is now $J_n=g_n^{\,d}$**, which is the only quantity that changes, and both
fallback exponents, $(2d+3)/(2d+6)$ and $d/(d+3)$, are strictly below $(d+2)/(d+3)$. The fallback is
not binding.

**6. The balance.** Minimise over $h\in(0,1]$ and $L\ge1$ the quantity
$F(h,L):=\max\{K h^{-d}L,\ n\sqrt{\ell_n/(2L)},\ \sqrt d\,nh\log(en)\}$. Write
$T_1:=Kh^{-d}L$ (elicitation: $KL$ pulls in each of $h^{-d}$ cells), $T_2:=n\sqrt{\ell_n/(2L)}=ns_n$
(price slack), $T_3:=\sqrt d\,nh\log(en)=n\rho_n$ (oscillation). $T_1$ is increasing in $L$ and
decreasing in $h$; $T_2$ is decreasing in $L$ and free of $h$; $T_3$ is increasing in $h$ and free of
$L$. So the minimum of the max is attained where all three agree.

  $T_1=T_2$: $Kh^{-d}L=n\sqrt{\ell_n/2}\,L^{-1/2}$, i.e. $L^{3/2}=nh^d\sqrt{\ell_n/2}/K$, i.e.
  $$L=(nh^d)^{2/3}\Bigl(\tfrac{\sqrt{\ell_n/2}}{K}\Bigr)^{2/3}. \tag{6.1}$$
  $T_2=T_3$: $n\sqrt{\ell_n/2}\,L^{-1/2}=\sqrt d\,nh\log(en)$, i.e.
  $$L=\frac{\ell_n/2}{d\,h^2\log^2(en)}. \tag{6.2}$$
  Equating (6.1) and (6.2) and writing $c_1:=(\sqrt{\ell_n/2}/K)^{2/3}$,
  $c_2:=\ell_n/(2d\log^2(en))$:
  $$c_1n^{2/3}h^{2d/3}=c_2h^{-2}\ \Longrightarrow\ h^{(2d+6)/3}=\frac{c_2}{c_1}n^{-2/3}
  \ \Longrightarrow\ h^\star=\Bigl(\frac{c_2}{c_1}\Bigr)^{\frac{3}{2d+6}}n^{-\frac{1}{d+3}},$$
  and substituting into (6.2),
  $$L^\star=c_2(h^\star)^{-2}=c_2\Bigl(\frac{c_1}{c_2}\Bigr)^{\frac{3}{d+3}}n^{\frac{2}{d+3}}.$$
  Both $c_1$ and $c_2$ are $\mathrm{polylog}$ in $n$ and $K$ (and $c_1$ carries $K^{-2/3}$), so
  $$h^\star=\Theta\bigl(n^{-1/(d+3)}\bigr),\qquad L^\star=\Theta\bigl(n^{2/(d+3)}\bigr)$$
  up to factors polylogarithmic in $n$ and $K$, and the common value is
  $$F(h^\star,L^\star)=T_3=\sqrt d\,nh^\star\log(en)=\Theta\bigl(n^{1-\frac{1}{d+3}}\log n\bigr)
  =\Theta\bigl(n^{\frac{d+2}{d+3}}\log n\bigr).$$
  This confirms the claimed $h_n=n^{-1/(d+3)}$, $L_n=n^{2/(d+3)}$ and the value
  $\Theta(n^{(d+2)/(d+3)}\log n)$. The mechanism uses the pure powers
  $h_n=1/\lceil n^{1/(d+3)}\rceil$ and $L_n=\lceil n^{2/(d+3)}\rceil$ rather than $h^\star,L^\star$,
  i.e. it does not chase the polylog corrections into the tuning; the price of that is a factor
  bounded by a constant times $\log(eKn)$, which is exactly the $\log(eKn)$ carried in the statement.
  Checking the three terms at the mechanism's actual values:
  $$T_1\le K\,2^d n^{\frac{d}{d+3}}\cdot 2n^{\frac{2}{d+3}}=K2^{d+1}n^{\frac{d+2}{d+3}},\qquad
  T_2\le\sqrt{\ell_n/2}\,n^{\frac{d+2}{d+3}},\qquad
  T_3\le\sqrt d\,n^{\frac{d+2}{d+3}}\log(en),$$
  all three $\Theta(n^{(d+2)/(d+3)})$ up to logs, as required. Note $T_1$ as written carries the $K$
  of $e_{\mathrm{stage1}}$; the deviator's own elicitation charge $e_{\mathrm{bid}}$ is $T_1/K$ and so
  is $K$-free.

**7. Where $K$ still enters.** *In the constants only, never in the exponent.* Precisely:

  | term | appears in | bound | $K$-dependence |
  |---|---|---|---|
  | $e_{\mathrm{bid}}$ | (i) | $2^{d+1}n^{\frac{d+2}{d+3}}$ | **none** |
  | $e_{\mathrm{osc}}$ | (i) | $\sqrt d\,n^{\frac{d+2}{d+3}}\log(en)$ | **none** |
  | $e_{\mathrm{mon}}$ | (i), (iii) | $2^dn^{\frac{d}{d+3}}+2^{\frac d2+1}\sqrt{\ell_n/2}\,n^{\frac{2d+3}{2d+6}}$ | only through $\ell_n=\log(2Kn^5)$, i.e. $O(\sqrt{\log K})$ |
  | $e_{\mathrm{fb}}$ | (i), (iii) | $11\sqrt{2K\log K}\,2^{\frac d2}n^{\frac{2d+3}{2d+6}}+2^{d+1}K\log K\,n^{\frac d{d+3}}\log_2(2(n+1))$ | $\sqrt{K\log K}$ and $K\log K$, on strictly sub-dominant powers |
  | $e_{\mathrm{stage1}}$ | (ii), (iii) | $K2^{d+1}n^{\frac{d+2}{d+3}}$ | **linear in $K$**, on the dominant power |
  | $e_{\mathrm{price}}$ | (ii), (iii) | $(4\sqrt{\ell_n/2}+\frac43\sqrt d\log(en))n^{\frac{d+2}{d+3}}$ | only through $\ell_n$, i.e. $O(\sqrt{\log K})$ |
  | additive | (i) | $4n^{-3}+4K^{-1}n^{-2}$ | decreasing in $K$ |

  Consequently:
  * the **exponent** $(d+2)/(d+3)$ carries no $K$ whatever;
  * in **part (i)** the coefficient of the dominant power $n^{(d+2)/(d+3)}$ is
    $2^{d+1}+\sqrt d\log(en)$, which is **free of $K$ entirely**; $K$ appears only on the strictly
    smaller powers $n^{(2d+3)/(2d+6)}$ and $n^{d/(d+3)}$, as $\sqrt{K\log K}$ and $K\log K$;
  * in **parts (ii) and (iii)** the coefficient of $n^{(d+2)/(d+3)}$ is
    $K2^{d+1}+4\sqrt{\ell_n/2}+\frac43\sqrt d\log(en)$, i.e. **linear in $K$** and otherwise only
    $\sqrt{\log K}$;
  * $K$ also sits inside the mechanism (Stage 1 is $KL_n$ visits per cell; the fallback is over $K$
    arms; $\ell_n$ carries $2K$), which is where the linear $K$ of $e_{\mathrm{stage1}}$ comes from.

  For contrast, the source has the exponent $(Kd+2)/(Kd+3)$ and a leading constant $2^{Kd+1}$
  — exponential in $K$ in both places.

**8. (A2) versus (A3).** Unchanged, and I verified the necessity rather than assuming it.
  * **Part (i) needs (A2)**, at exactly one place: §4.4(j)'s requirement that the two coupled
    executions have the same Stage-1 rounds at every cube and pull the same agent at each. The
    accurate statement of what is needed is that the arrival path is the same random sequence in the
    two coupled executions, that is, that a deviation cannot move the path; exogeneity delivers that
    and is formally stronger. It is still **necessary** in the shared-context case, and
    `rem:ctx-continuum-exogeneity`'s witness ports directly with $d=1$: $K=2$, $M_1\equiv1$,
    $\mu_1\equiv0$, $M_2(x)=\mu_2(x)=x$ on $[0,1)$, and a path that sits in the origin cell if the
    first reward is $0$ and in the top cell if it is $1$. The deviation that delivers $0$ at the first
    Stage-1 pull and then follows $S^\star$ moves the entire remaining horizon to the origin cell,
    where $\beta_{(2)}\approx0$, hence $\tau\approx0$, hence per-pull utility $1+\mu_1-0=1$; the
    baseline sits in the top cell where $\tau\approx1-\sigma_n$ and the per-pull utility is
    $\approx\sigma_n$. The gain is $\Theta(n)$ at every horizon with $\sigma_n<1$. The natural
    weakening — arrivals exogenous until every cell completes Stage 1 and reactive afterwards —
    preserves the win-inclusion but destroys the accounting, because $n_C$ then differs between the
    two executions and the comparison of $U'^{\mathrm{post}}$ with $n_Cw_C$ is between two different
    numbers of pulls, a difference of order $n$. No refinement of a filtration repairs this.
  * **Part (ii) needs only the seed clause of (A3)**; **part (iii) needs only the Stage-3 selection
    clause and the seed clause of (A3)**. Neither couples two executions and neither reads the arrival
    path, so neither acquires any new requirement in the shared-context case. `rem:ctx-endogenous`
    applies verbatim: under (A3) the benchmarks $\mathbb E\sum_tM_{(2)}(x_t)$ and
    $\mathbb E\sum_tb(x_t)$ are evaluated along the realised path, which the mechanism helps
    determine, so the honest reading of (ii) and (iii) is a comparison against that path and not
    against a fixed law.

---

## 6. Adversarial self-check

I tried four distinct attacks. None of them works, and I record why in enough detail that a reader can
check the failure of each attack rather than take my word for it.

**Attack 1: find a step that needs the profile rather than the cell label, specifically a step that
compares agents to each other.** The steps that compare agents are: the choice of the winner as a
largest bidder; $\beta_{(2),C}\le\beta_{W,C}$ in `lem:ctx-price-meet`; $\beta_{(2),C}\le\beta_{j^*,C}$
with $j^*\ne i$ in `lem:ctx-price-dom`; the monotonicity of the second order statistic in
`lem:ctx-price-second`; $\beta_{(2),C}\ge\beta_{h_C,C}$ in part (iii); the comparator choice in the
fallback lemmas; and the bid domination of §4.4(j). **Every one of these is a deterministic statement
about order statistics of $K$ real numbers, or a pathwise feasibility/honesty inequality.** Not one of
them is a probabilistic comparison between agents. The only probabilistic inputs about several agents
at once are the union bounds defining $E_C$ and $E^H_C$, and a union bound is valid for arbitrarily
dependent events. I state this as the sharp form of the answer: **cross-agent independence is nowhere
used in `prop:ctx-continuum-exact`, so perfect cross-agent dependence cannot break it.** One can see
this from the shape of the source's own claims — `lem:ctx-bidconc` is asserted "uniform over all
behaviour" and part (iii) is asserted for a profile in which all $K$ agents may deviate jointly, and
jointly deviating agents may be arbitrarily correlated. If cross-agent independence had been load
bearing anywhere, those two statements would already have been false.

  There is one place where the shared context makes a difference of degree rather than of kind: with
  $M_1\equiv M_2$ exact bid ties have large probability instead of merely positive probability. I
  therefore re-verified the tie handling in the win-inclusion argument explicitly (§4.4(j)), rather
  than inheriting it. It holds, because the argument is written without a strict inequality and shares
  $\Pi_C$ across the two executions.

**Attack 2: information. With a common context the deviator learns its rivals' capabilities exactly.**
This cannot help, for two independent reasons, and the second is decisive. First, in the source model
the selected agent already observes the **full** profile, so it already knew $x_{j,t}$ and hence
$M_j(x_{j,t})$ if it knows $M_j(\cdot)$; the shared-context deviator is not better informed. Second,
and this is the decisive point, part (i) is stated over $\mathcal B^{\mathrm{sc}+}_{i,n}$, in which
the deviator may condition on the **entire arrival sequence**, hence on all future contexts, all visit
counts and the exact global round index. Its information is already maximal, and no dependence
structure among the $M_j$ can add to a class that is already closed under conditioning on everything
about the arrival path. Any attack based on "the deviator now knows more" therefore has no room to
operate.

**Attack 3: the diagonal is a null set of $[0,1]^{Kd}$; find something in the source proof that fails
on a null set.** I looked for: a density; full support; positive cell mass; a boundary condition
$\nu(\partial R)=0$; a two-top condition holding $\nu$-almost everywhere; a claim about the
cell-average $\bar M_{j,C}=\mathbb E[M_j\mid X\in C]$ requiring $\nu(C)>0$; and an a.e. statement of
any kind. **None occurs in `prop:ctx-continuum-exact` or in any of the nine lemmas it uses.** The
proposition's own closing sentence says so and the proofs bear it out: the error terms are built from
$\mathbb E[J'_n]$, the expected number of **visited** cells, bounded pathwise by $\min\{J_n,n\}$; the
quantities $M_j^{\inf}(C),M_j^{\sup}(C),\nu_i(C),v_C$ are infima and suprema over $C$, not
conditional expectations; $\bar M_{j,C}$ is an empirical average over the agent's own realised Stage-1
rounds at $C$, defined pathwise; and parts (ii)/(iii) place no condition on the arrival process at
all. By contrast the **public** results in `sec4_contextual.tex` do use such things —
`thm:grid-ucb-robust` carries $n\nu((\partial R)^{\sqrt Dh_n})$, `thm:grid-etc` requires
$\nu(\partial R)=0$, `thm:contextual-public` requires two tops $\nu$-almost everywhere, and the
cell-average $\bar M_{j,C}$ there *is* a conditional expectation. So this attack would have real bite
against the public theorems; it has none against the proposition I am specialising. A concentrated or
lower-dimensional law only makes $\mathbb E[J'_n]$ smaller and every bound better.

**Attack 4: a concrete counterexample.** I constructed the sharpest candidate I could:
$d=1$, $K=2$, $M_1(x)=M_2(x)=x$ on $[0,1)$ (perfect dependence and perpetual ties),
$\mu_1=\mu_2=0$, $\mathcal K_H=\{2\}$, and arrivals concentrated on a single cell $C_0$ so that the
diagonal support is as degenerate as possible. Trace: both agents bid the same distribution with
$\bar A_{j,C_0}=\bar M_{j,C_0}$; the tie is broken by $\Pi_{C_0}$; on $E_{C_0}$,
$\beta_{(2),C_0}\ge M_{(2)}(x)-\omega-s_n=M_\star(x)-\omega-s_n$, so
$\tau_{C_0}\ge M_\star(x)-4s_n-\frac43\rho_n$, and by `lem:ctx-price-meet`
$\tau_{C_0}\le M_W(x)$ for every $x\in C_0$ — the mechanism prices at essentially the full capability
and the winner's surplus is $O(s_n+\rho_n)$ per round. That is the intended behaviour, not a break:
$M_{(2)}=M_\star$ here, so part (ii) is a strong conclusion and it holds. For deterrence, a deviator
underbidding in Stage 1 only shrinks its win event, and when it wins it faces the same price, so its
gain is the $l_i(C_0)\le L_n$ elicitation saving plus the monitor/fallback slack — exactly what the
bound says. I could not turn any part of this into a violation. I also checked the degenerate ordering
case $M_1\equiv M_2+c$ for a constant $c>0$ (agent 1 uniquely top at every context, a case the finite
tightness result `prop:ctx-finite-tight` exploits): there the deviator does collect $\approx L_n$ per
awarding cell, which is $e_{\mathrm{bid}}\approx J_nL_n=n^{(d+2)/(d+3)}$ — attaining the bound, not
violating it. **Honest report: no counterexample. The candidate instances I built all confirm the
bound, and one of them (the uniquely-top instance) suggests that $e_{\mathrm{bid}}$ is attained, which
is consistent with `prop:ctx-finite-tight` and means the $(d+2)/(d+3)$ exponent cannot be improved by
sharpening this analysis alone.** I have not proved a matching lower bound and do not claim one.

---

## 7. What is genuinely new versus inherited

**Plainly: this is mostly a re-labelling. I would put it at roughly one new sentence of mathematics
and one new observation about why the sentence is true, on top of an unchanged proof.**

**Inherited, verbatim, with $x_t$ read for $X_t$ and a cube of $[0,1)^d$ read for a cube of
$[0,1)^{Kd}$:** the mechanism; the hypothesis block; `lem:ctx-bidconc`, `lem:ctx-price-meet`,
`lem:ctx-price-dom`, `lem:ctx-price-second`, `lem:ctx-honest-floor`, `lem:ctx-monitor-cont`,
`lem:ctx-fallback-cont`, `lem:ctx-dev-fallback`; all three proofs of the proposition, including the
"legitimacy of the conditioning" paragraph, the $\mathcal H^\star_C$ charge, the case-split
measurability argument in part (iii), and the read-off; `rem:ctx-endogenous` and
`rem:ctx-continuum-exogeneity` with its witness. None of these required a new idea; several required
a check (which coordinate the predictable indicator reads; whether an order-statistic step was secretly
probabilistic; whether ties still behave), and each check passed.

**Genuinely new, and it is small:**
1. **The observation that `prop:ctx-continuum-exact` depends on the context space only through
   (number of cells, within-cell oscillation of the primitives), and through nothing else.** This is
   the Reduction principle of §4.1. It is a reading of the existing proof, not a new argument, but it
   is the thing that makes the specialisation a two-line change instead of a re-derivation, and it is
   worth stating in the paper because it also yields Corollary SC (general $\phi_i$) for free and
   makes clear what any future specialisation has to check.
2. **The arithmetic that the $\sqrt d$ cancels in $\omega\le\rho_n/3$, so the instance-dependent
   hypothesis $n\ge\exp(3L)$ is exactly preserved.** One line, but it is the only hypothesis that
   refers to the instance and it would have been easy to assume it degrades or improves; it does
   neither.
3. **The structural explanation of why the shared case escapes the $K$-exponent.** In
   `app:ctx-private-net` the obstruction is a fallback whose comparator class is a set of rankings of
   $Kq^d$ (agent, cell) pairs, a sleeping-bandit problem with each agent in its own cell. Under a
   common context, $c_j(t)=c(t)$ for every $j$: all agents occupy the same cell at every round, the
   sleeping structure collapses, and the fallback is just $J_n$ independent $K$-armed bandits, one per
   cell. That is why a polynomial-time mechanism attains $(d+2)/(d+3)$ here, whereas in the general
   model the same exponent is only reached by the non-algorithmic net construction. This is a remark,
   not a theorem, but it is the sentence a reader will want.
4. **Corollary SC**, the $\phi_i$ version, which is the identity case applied to
   $M_i\circ\phi_i$, $\mu_i\circ\phi_i$ and costs only $L\mapsto L\Lambda$ in (H). It is the same
   proof; I say so in the statement.

**A related observation that is not needed but is worth one remark in the paper.** In the identity
shared-context case the diagonal $\Delta$ meets exactly $g_n^{\,d}$ of the $g_n^{\,Kd}$ cubes of the
profile grid, because a point $(x,\dots,x)$ has the same block index in all $K$ blocks. So the
*profile*-gridded CG-MESP, run with the parameters re-tuned to $h_n=n^{-1/(d+3)}$,
$L_n=n^{2/(d+3)}$ and with lazy instantiation, also achieves the claim, with $\rho_n=\sqrt{Kd}h_n\log(en)$
costing an extra factor $\sqrt K$ in $e_{\mathrm{osc}}$ and $e_{\mathrm{price}}$. **One caveat, which
is why I do not state it as a proposition:** `lem:ctx-bidconc` and `lem:ctx-monitor-cont`(a) union
bound over the *deterministic* set of grid cubes, and with a profile grid at that resolution that set
has $g_n^{\,Kd}\gg n$ elements, so the union bound as written fails. It can be repaired by union
bounding over the $g_n^{\,d}$ diagonal cubes, which is still a deterministic set — but knowing that
set is knowing the diagonal, at which point one may as well grid $[0,1)^d$. So the honest statement is:
gridding the common space is the clean route, and the profile-grid route needs the same knowledge plus
a repaired union bound.

---

## 8. Smallest horizon at which this says anything

I redid the bisection of `rem:ctx-horizons` with $d$ in place of $D$. Method: exactly the source's,
i.e. the parameters of §2 with $\mathbb E[J'_n]$ at its worst case $\min\{J_n,n\}$, bisection on
$\log_{10}n$, reporting the smallest $n$ at which each quantity first drops below its trivial value
($1$ for $\sigma_n$; $n$ for the bound of (i) and for the slack of (ii)).

**Validation.** Before producing new numbers I reproduced the source's table with $D$ in place of $d$
at $K=2$. All eighteen published figures came out identically:
$D=1$: $10^{6.1}$, $10^{5.2}$, $10^{6.8}$ — $D=2$: $10^{8.5}$, $10^{7.5}$, $10^{9.3}$ —
$D=3$: $10^{11.1}$, $10^{10.0}$, $10^{12.0}$ — $D=4$: $10^{13.7}$, $10^{12.7}$, $10^{14.9}$ —
$D=6$: $10^{19.4}$, $10^{18.4}$, $10^{20.8}$ — $D=10$: $10^{31.7}$, $10^{30.7}$, $10^{33.7}$.
So the figures below are computed by a procedure known to agree with the source's on the source's own
inputs.

**Shared context.** Smallest $n$ (as $10^{\log_{10}n}$) at which each quantity first drops below its
trivial value:

| $d$ | $K$ | $\sigma_n<1$ | bound of (i) $<n$ | slack of (ii) $<n$ | (for comparison) same three at $D=Kd$ |
|---|---|---|---|---|---|
| 1 | 2 | $10^{6.1}$ | $10^{5.2}$ | $10^{6.8}$ | $D=2$: $10^{8.5}$, $10^{7.5}$, $10^{9.3}$ |
| 1 | 3 | $10^{6.1}$ | $10^{5.4}$ | $10^{6.8}$ | $D=3$: $10^{11.1}$, $10^{10.1}$, $10^{12.1}$ |
| 2 | 2 | $10^{8.5}$ | $10^{7.5}$ | $10^{9.3}$ | $D=4$: $10^{13.7}$, $10^{12.7}$, $10^{14.9}$ |
| 2 | 3 | $10^{8.5}$ | $10^{7.7}$ | $10^{9.4}$ | $D=6$: $10^{19.4}$, $10^{18.4}$, $10^{20.8}$ |
| 3 | 2 | $10^{11.1}$ | $10^{10.0}$ | $10^{12.0}$ | $D=6$: $10^{19.4}$, $10^{18.4}$, $10^{20.8}$ |
| 3 | 3 | $10^{11.1}$ | $10^{10.1}$ | $10^{12.1}$ | $D=9$: $10^{28.5}$, $10^{27.6}$, $10^{30.4}$ |

Four things should be read off rather than discovered.

* **The thresholds are governed by $d$ and are essentially independent of $K$.** Going from $K=2$ to
  $K=3$ moves them by at most $0.2$ decades; going from $d$ to $d+1$ moves them by about $2.5$
  decades. This is the numerical face of check 7: $K$ is in the constants, $d$ is in the exponent and
  in the factors $2^d$, $\sqrt d$.
* **The saving over the general model is large but does not rescue the theorem numerically.** At
  $K=3$, $d=2$ the revenue slack becomes useful at $10^{9.4}$ instead of $10^{20.8}$ — eleven orders
  of magnitude — but $10^{9.4}$ is still a horizon no simulation will reach. The source's own verdict
  stands: the result is asymptotic in a strong sense and no experiment can exhibit it. The
  shared-context specialisation makes $d=1$ genuinely borderline ($10^{5.2}$--$10^{6.8}$) and $d=2$
  arguable, and that is the whole of the numerical gain.
* **The ordering of the three thresholds is preserved**: the incentive bound (i) bites first, then
  $\sigma_n<1$, then the revenue slack of (ii). The gap (ii)-minus-(i) is about $1.6$--$2.0$ decades
  throughout, as in the source.
* **The $K=2$ rows are numerically identical to the source's $D=1,2,3$ rows**, which is not a
  coincidence and is a further consistency check: the source's table was computed at $K=2$, and at
  $K=2$ the formulas depend on the grid dimension alone plus the $K$'s inside $\ell_n$,
  $e_{\mathrm{stage1}}$ and $e_{\mathrm{fb}}$.

The threshold still grows like $\exp(cd)$ rather than polynomially, because $J_n$ carries a factor
$2^d$ and $\rho_n$ a factor $\sqrt d$; the shared-context case replaces $\exp(cKd)$ by $\exp(cd)$ and
does not change the shape.

---

## 9. Open or doubtful

Listed honestly; none of these is needed for Proposition SC, but each is something a reader might
wrongly infer.

1. **The improvement is not free of knowledge: the platform must know $d$ and must know that a single
   $d$-dimensional variable drives every agent.** The gain comes from re-tuning $h_n$ and $L_n$ to
   $d$. Lazy cell instantiation alone does **not** deliver it. The remark after
   `thm:grid-ucb-robust` ("the exploration terms therefore adapt on their own to a context law
   supported on a lower-dimensional set, with no knowledge of that set") is about the *exploration*
   terms; here the analogues are $e_{\mathrm{bid}},e_{\mathrm{stage1}},e_{\mathrm{mon}},e_{\mathrm{fb}}$,
   which do adapt automatically through $\mathbb E[J'_n]$. But $e_{\mathrm{osc}}=n\rho_n$ and
   $e_{\mathrm{price}}$ are controlled by $h_n$ and $L_n$ and by nothing else, so they do not adapt.
   **I have not proved any dimension-adaptive version and do not claim one.** A mechanism that attains
   the $d$ exponent without being told $d$ is open as far as this note is concerned.
2. **No lower bound.** I have not shown $(d+2)/(d+3)$ is optimal in the shared-context model. The
   uniquely-top instance of Attack 4 shows that $e_{\mathrm{bid}}\approx J_nL_n$ is attained by an
   explicit deviation, in the same way as `prop:ctx-finite-tight` does for the finite case, so the
   analysis cannot be improved by sharpening constants; but that is an argument about this mechanism
   and this analysis, not about the problem.
3. **This does not close the open problem of `app:ctx-private-net`.** That problem concerns $K$
   agents occupying **different** cells at a round. Under a common context they always occupy the same
   cell, which is exactly the degenerate case in which the sleeping-bandit difficulty disappears. The
   paper must not present Proposition SC as a resolution of the separation; the correct sentence is
   that the shared-context model is a special case in which the computational barrier does not arise.
4. **The profile-grid route** described at the end of §7 (run CG-MESP on $[0,1)^{Kd}$ with parameters
   re-tuned to $d$) I have argued for but not written out, and it has a genuine gap as stated in the
   source's form: the union bounds of `lem:ctx-bidconc` and `lem:ctx-monitor-cont`(a) run over the
   deterministic set of all grid cubes, which is too large at that resolution. It is repairable by
   union bounding over the $g_n^{\,d}$ diagonal cubes, but that requires knowing the diagonal. I flag
   it rather than assert it.
5. **The $[0,1]^d$ versus $[0,1)^d$ convention** is inherited from the source, which writes
   $\mathcal X=[0,1]^D$ in `sec2_model.tex` and tiles $[0,1)^D$ in `app_contextual_private.tex`.
   Nothing depends on it; I mention it only so that a copy edit does not mistake it for an error
   introduced here.
6. **Nothing here touches `thm:equilibrium-set` or the collusion discussion of
   `sec:ctx-equilibrium`.** Those are separate statements and I have not checked whether they
   specialise; in particular the shared-context case makes "two agents attain the top capability at
   almost every profile" a statement about a single variable, which may change which profiles survive.
   I did not examine it and make no claim.

