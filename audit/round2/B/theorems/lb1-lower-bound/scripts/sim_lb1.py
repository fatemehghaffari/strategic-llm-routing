"""LB1 simulation: MESP (paper constants) against the adaptive-certification menu candidate (ACM).

Scalar instance, K = 2, linear cost. Agent 1 strategic (mu = 0, M = 0.5), agent 2 honest
(mu = 0.1, M = 0.3). Second-capability benchmark 0.3, honest benchmark 0.1.

All quantities are computed replicate by replicate with coupled uniforms: U[i][k] is the seed of agent
i's k-th pull (local index), shared by the baseline and every deviation of that replicate. Reward sums
are integer counters. Vectorised across replicates; the only sequential loops are the adaptive
deviations and the EXP3 fallback.

Declared option sets are fixed in OPTIONS_1 and OPTIONS_2 before any run; nothing is tuned afterwards.
"""
import sys, json, math, time
import numpy as np

MU = np.array([0.0, 0.1]); M = np.array([0.5, 0.3])
HONEST = np.array([False, True])
BENCH2 = 0.3; BENCH_H = 0.1

# ---------------------------------------------------------------- mechanism constants
def mesp_consts(n, K=2):
    L = min(n // (2 * K), math.ceil(n ** (2 / 3) * math.log(math.e * n) ** (1 / 3)))
    s = math.sqrt(math.log(2 * K * n ** 4) / (2 * L))
    ell = math.log(2 * n ** 4)
    return L, s, ell

def acm_consts(n):
    L = n // 4                      # picked once: the sketch's L = n/4
    ell = math.log(2 * n ** 4)      # picked once: the same log level as MESP's monitor
    s = math.sqrt(ell / (2 * L))
    return L, s, ell

def bnd(r, ell):                    # anytime monitor boundary b(r) = sqrt(r ell / 2)
    return np.sqrt(r * ell / 2.0)

# ---------------------------------------------------------------- strategies
# A strategy is described by a dict; the simulator interprets fields.
#  'elic': ('const', c) | ('late', c, f) | ('earlyhigh', f) | ('pace', delta) | None (= deliver M)
#  'prim': ('shade', delta) | ('track', margin) | None (= deliver tau)
#  'rew':  ('shade', delta) | None   (agent 2 in ACM Phase R; agent 1 if it becomes the loser)
def opt(name, elic=None, prim=None, rew=None):
    return dict(name=name, elic=elic, prim=prim, rew=rew)

OPTIONS_1 = [opt('S*')]
OPTIONS_1 += [opt(f'E-const({c:.2f})', elic=('const', c)) for c in np.arange(0.30, 0.49, 0.02)]
OPTIONS_1 += [opt(f'E-late(c={c},f={f})', elic=('late', c, f)) for c in (0.30, 0.40) for f in (0.25, 0.5, 0.75)]
OPTIONS_1 += [opt(f'E-earlyhigh(f={f})', elic=('earlyhigh', f)) for f in (0.25, 0.5)]
OPTIONS_1 += [opt(f'E-pace(d={d})', elic=('pace', d)) for d in (0.0, 0.02, 0.05)]
OPTIONS_1 += [opt(f'P-shade(d={d})', prim=('shade', d)) for d in (0.01, 0.02, 0.05, 0.10)]
OPTIONS_1 += [opt(f'P-track(m={m})', prim=('track', m)) for m in (1.0, 3.0)]
OPTIONS_1 += [opt('E-const(0.32)+P-shade(0.02)', elic=('const', 0.32), prim=('shade', 0.02)),
              opt('E-const(0.32)+P-track(1)', elic=('const', 0.32), prim=('track', 1.0))]
OPTIONS_1 += [opt(f'become-loser(c={c})', elic=('const', c)) for c in (0.0, 0.2, 0.28)]

OPTIONS_2 = [opt('S*')]
OPTIONS_2 += [opt(f'E-const({c:.2f})', elic=('const', c)) for c in (0.10, 0.15, 0.20, 0.25)]
OPTIONS_2 += [opt(f'R-shade(d={d})', rew=('shade', d)) for d in (0.02, 0.05)]

# ---------------------------------------------------------------- helpers
def elic_targets(agent, strat, Lmax, Z_fn=None):
    """Precomputable elicitation targets of shape (Lmax,) for non-adaptive rules; None for 'pace'."""
    cap = M[agent]; lo = MU[agent] if HONEST[agent] else 0.0
    e = strat['elic']
    k = np.arange(Lmax)
    if e is None:
        return np.full(Lmax, cap)
    if e[0] == 'const':
        return np.full(Lmax, float(np.clip(e[1], lo, cap)))
    if e[0] == 'late':
        c, f = e[1], e[2]
        return np.where(k < f * Lmax, np.clip(c, lo, cap), cap)
    if e[0] == 'earlyhigh':
        f = e[1]
        return np.where(k < f * Lmax, cap, np.clip(0.30, lo, cap))
    return None  # pace: adaptive

def pace_draws(U, Lmax, delta, ell, cap, lo):
    """Boundary pacer: keep own running mean at (0.3 + 2 s(t) - delta), using the known instance value
    0.3 for the other agent and equal pull counts during alternation. Returns (Y, targets)."""
    R = U.shape[0]
    Y = np.zeros((R, Lmax), dtype=np.int64); T = np.zeros((R, Lmax))
    Z = np.zeros(R, dtype=np.int64)
    for t in range(1, Lmax + 1):
        thr = 0.3 + 2 * math.sqrt(ell / (2 * t)) - delta
        m = np.clip(t * thr - Z, lo, cap)
        y = (U[:, t - 1] <= m).astype(np.int64)
        Y[:, t - 1] = y; T[:, t - 1] = m; Z += y
    return Y, T

def monitored_phase(U, targets_fn, tau, horizon, ell, R):
    """Pull one agent for up to `horizon[r]` rounds with the anytime monitor Z_r < r tau - b(r).
    targets_fn(r, Z_prev) -> target vector (adaptive allowed). Returns (rounds_used, convicted,
    delivered_sum, utility_increment is computed by caller via targets)."""
    pass

def run_monitor_const(U, m, tau, horizon, ell):
    """Constant target m (per replicate, shape (R,)); U shape (R, Hmax). horizon shape (R,) int.
    Returns rounds used q (R,), convicted (R,) bool, sum of targets delivered (R,) float."""
    R, Hmax = U.shape
    Y = (U <= m[:, None]).astype(np.int64)
    Z = np.cumsum(Y, axis=1)
    r = np.arange(1, Hmax + 1)
    viol = Z < (r[None, :] * tau[:, None] - bnd(r, ell)[None, :])
    viol &= (r[None, :] <= horizon[:, None])
    anyv = viol.any(axis=1)
    first = np.where(anyv, viol.argmax(axis=1) + 1, horizon)
    q = np.minimum(first, horizon)
    return q, anyv & (first <= horizon), q * m

def run_monitor_track(U, cap, lo, tau, margin, horizon, ell):
    """Boundary tracker: target each pull so that Z_r stays about `margin` above r tau - b(r)."""
    R, Hmax = U.shape
    Z = np.zeros(R, dtype=np.int64); q = np.zeros(R, dtype=np.int64)
    conv = np.zeros(R, dtype=bool); deliv = np.zeros(R)
    active = np.ones(R, dtype=bool)
    for r in range(1, Hmax + 1):
        active &= (r <= horizon)
        if not active.any():
            break
        need = r * tau - math.sqrt(r * ell / 2) + margin - Z   # want Z_r >= this
        m = np.clip(need, lo, cap)
        y = (U[:, r - 1] <= m).astype(np.int64)
        Z = np.where(active, Z + y, Z)
        deliv = np.where(active, deliv + m, deliv)
        q = np.where(active, r, q)
        v = active & (Z < r * tau - math.sqrt(r * ell / 2))
        conv |= v
        active &= ~v
    return q, conv, deliv

def exp3_fallback(rng, H, start_u, n_rep):
    """Explicit-exploration EXP3 over 2 agents, everyone delivering capability. H (R,) int horizons.
    Returns pulls of agent 1 (R,), delivered sum (R,)."""
    R = n_rep; Hmax = int(H.max()) if H.size else 0
    w = np.ones((R, 2)); pulls1 = np.zeros(R, dtype=np.int64); deliv = np.zeros(R)
    Hf = np.maximum(H, 1).astype(float)
    gamma = np.minimum(0.5, np.sqrt(2 * math.log(2) / Hf)); eta = gamma / 2
    for t in range(Hmax):
        act = t < H
        if not act.any():
            break
        q = w / w.sum(axis=1, keepdims=True)
        p = (1 - gamma)[:, None] * q + (gamma / 2)[:, None]
        u = rng.random(R); I = (u > p[:, 0]).astype(int)       # 0 -> agent 1, 1 -> agent 2
        y = (rng.random(R) <= M[I]).astype(np.int64)
        yhat = np.zeros((R, 2)); yhat[np.arange(R), I] = y / p[np.arange(R), I]
        w = np.where(act[:, None], w * np.exp(eta[:, None] * yhat), w)
        pulls1 += act & (I == 0)
        deliv += np.where(act, M[I], 0.0)
    return pulls1, deliv

# ---------------------------------------------------------------- one mechanism run (vectorised over replicates)
def run(mech, n, strat1, strat2, U1, U2, rng_fb, rng_tie):
    """Returns dict with u1, u2 (R,), revenue (R,), and diagnostics."""
    R = U1.shape[0]
    if mech == 'MESP':
        L, s, ell = mesp_consts(n); Lw = L
    else:
        L, s, ell = acm_consts(n); Lw = L
    # ---- elicitation draws (local pull index 0..L-1 for each agent)
    out = {}
    T1 = elic_targets(0, strat1, L); T2 = elic_targets(1, strat2, L)
    if T1 is None:
        Y1, T1m = pace_draws(U1[:, :L], L, strat1['elic'][1], ell, M[0], 0.0)
    else:
        T1m = np.broadcast_to(T1, (R, L)); Y1 = (U1[:, :L] <= T1m).astype(np.int64)
    T2m = np.broadcast_to(T2, (R, L)); Y2 = (U2[:, :L] <= T2m).astype(np.int64)
    C1 = np.cumsum(Y1, axis=1); C2 = np.cumsum(Y2, axis=1)
    E1 = np.cumsum(T1m, axis=1); E2 = np.cumsum(T2m, axis=1)   # cumulative targets (effort/revenue)
    u1 = np.zeros(R); u2 = np.zeros(R); rev = np.zeros(R)
    if mech == 'MESP':
        t1 = np.full(R, L); t2 = np.full(R, L)
        b1 = C1[:, -1] / L; b2 = C2[:, -1] / L
        tie = rng_tie.random(R) < 0.5
        win1 = (b1 > b2) | ((b1 == b2) & tie)
        beta_l = np.where(win1, b2, b1)
        used = np.full(R, 2 * L)
        Tw = np.full(R, L)
    else:
        t = np.arange(1, L + 1)
        st = np.sqrt(ell / (2 * t))
        m1 = C1 / t; m2 = C2 / t
        cert1 = (m1 - st) > (m2 + st); cert2 = (m2 - st) > (m1 + st)
        any1 = cert1.any(axis=1); any2 = cert2.any(axis=1)
        f1 = np.where(any1, cert1.argmax(axis=1) + 1, L + 1)
        f2 = np.where(any2, cert2.argmax(axis=1) + 1, L + 1)
        tie = rng_tie.random(R) < 0.5
        bL1 = C1[:, -1] / L; bL2 = C2[:, -1] / L
        nocert = (f1 > L) & (f2 > L)
        win1 = np.where(nocert, (bL1 > bL2) | ((bL1 == bL2) & tie), f1 <= f2)
        Tw = np.where(nocert, L, np.where(win1, f1, f2))      # winner's elicitation pulls
        t1 = np.where(win1, Tw, L); t2 = np.where(win1, L, Tw)
        beta_l = np.where(win1, bL2, bL1)
        used = t1 + t2
    tau = np.maximum(beta_l - s, 0.0)
    # elicitation accounting
    idx = np.arange(R)
    e1 = E1[idx, t1 - 1]; e2 = E2[idx, t2 - 1]
    u1 += t1 * (1 + MU[0]) - e1; u2 += t2 * (1 + MU[1]) - e2; rev += e1 + e2
    out['Tw'] = Tw; out['win1'] = win1; out['tau'] = tau
    k1 = t1.copy(); k2 = t2.copy()      # next local pull index per agent
    remaining = n - used
    # ---- ACM Phase R: loser's menu
    if mech == 'ACM':
        Rmenu = np.floor(beta_l * L / np.maximum(1 - beta_l, 1e-9)).astype(np.int64)
        Rmenu = np.minimum(Rmenu, remaining)
        # loser target in Phase R: S* = max(mu, min(tau, M)); 'rew' shade lowers it
        for ag, isl in ((0, ~win1), (1, win1)):
            if not isl.any():
                continue
            strat = strat1 if ag == 0 else strat2
            lo = MU[ag] if HONEST[ag] else 0.0
            tgt = np.maximum(lo, np.minimum(tau, M[ag]))
            if strat['rew'] is not None and strat['rew'][0] == 'shade':
                tgt = np.maximum(lo, tgt - strat['rew'][1])
            Uag = U1 if ag == 0 else U2
            kk = k1 if ag == 0 else k2
            Hmax = int(Rmenu[isl].max()) if isl.any() else 0
            sub = np.where(isl)[0]
            if Hmax > 0:
                # gather U rows at local indices kk..kk+Hmax-1
                cols = np.minimum(kk[sub, None] + np.arange(Hmax)[None, :], n - 1)
                Us = Uag[sub[:, None], cols]
                q, conv, deliv = run_monitor_const(Us, tgt[sub], tau[sub], Rmenu[sub], ell)
            else:
                q = np.zeros(len(sub), dtype=np.int64); conv = np.zeros(len(sub), bool); deliv = np.zeros(len(sub))
            if ag == 0:
                u1[sub] += q * (1 + MU[0]) - deliv; k1[sub] += q
            else:
                u2[sub] += q * (1 + MU[1]) - deliv; k2[sub] += q
            rev[sub] += deliv; remaining[sub] -= q
        out['Rmenu'] = Rmenu
    # ---- primary phase: winner at demand tau
    fb_H = np.zeros(R, dtype=np.int64)
    for ag, isw in ((0, win1), (1, ~win1)):
        if not isw.any():
            continue
        strat = strat1 if ag == 0 else strat2
        lo = MU[ag] if HONEST[ag] else 0.0
        sub = np.where(isw)[0]
        Uag = U1 if ag == 0 else U2; kk = k1 if ag == 0 else k2
        Hmax = int(remaining[sub].max())
        cols = np.minimum(kk[sub, None] + np.arange(Hmax)[None, :], n - 1)
        Us = Uag[sub[:, None], cols]
        tgt = np.maximum(lo, np.minimum(tau[sub], M[ag]))
        if strat['prim'] is not None and strat['prim'][0] == 'shade':
            tgt = np.maximum(lo, tgt - strat['prim'][1])
            q, conv, deliv = run_monitor_const(Us, tgt, tau[sub], remaining[sub], ell)
        elif strat['prim'] is not None and strat['prim'][0] == 'track':
            q, conv, deliv = run_monitor_track(Us, M[ag], lo, tau[sub], strat['prim'][1], remaining[sub], ell)
        else:
            q, conv, deliv = run_monitor_const(Us, tgt, tau[sub], remaining[sub], ell)
        if ag == 0:
            u1[sub] += q * (1 + MU[0]) - deliv
        else:
            u2[sub] += q * (1 + MU[1]) - deliv
        rev[sub] += deliv; remaining[sub] -= q
        fb_H[sub] = np.where(conv, remaining[sub], 0)
        out['conv_' + str(ag)] = conv.mean()
    # ---- fallback: EXP3 over both, everyone delivering capability
    if (fb_H > 0).any():
        sub = np.where(fb_H > 0)[0]
        p1, deliv = exp3_fallback(rng_fb, fb_H[sub], None, len(sub))
        u1[sub] += p1 * (1 + MU[0] - M[0]); u2[sub] += (fb_H[sub] - p1) * (1 + MU[1] - M[1])
        rev[sub] += deliv
    out['u1'] = u1; out['u2'] = u2; out['rev'] = rev; out['fb_frac'] = (fb_H > 0).mean()
    return out

# ---------------------------------------------------------------- driver
def main(ns, nrep, outpath):
    results = []
    for n in ns:
        n = int(n)
        for mech in ('MESP', 'ACM'):
            t0 = time.time()
            rng = np.random.default_rng(20261013 + n)
            U1 = rng.random((nrep, n)); U2 = rng.random((nrep, n))
            base = run(mech, n, OPTIONS_1[0], OPTIONS_2[0], U1, U2, np.random.default_rng(1), np.random.default_rng(2))
            rec = dict(mech=mech, n=n, nrep=nrep, rev_per_round=float(base['rev'].mean() / n),
                       rev_se=float(base['rev'].std(ddof=1) / math.sqrt(nrep) / n),
                       bench2=BENCH2, benchH=BENCH_H, Tw_mean=float(np.mean(base['Tw'])),
                       win1_frac=float(base['win1'].mean()), tau_mean=float(base['tau'].mean()),
                       fb_frac_base=float(base['fb_frac']), gains1={}, gains2={})
            for strat in OPTIONS_1[1:]:
                o = run(mech, n, strat, OPTIONS_2[0], U1, U2, np.random.default_rng(1), np.random.default_rng(2))
                g = o['u1'] - base['u1']
                rec['gains1'][strat['name']] = (float(g.mean()), float(g.std(ddof=1) / math.sqrt(nrep)), float(o['win1'].mean()))
            for strat in OPTIONS_2[1:]:
                o = run(mech, n, OPTIONS_1[0], strat, U1, U2, np.random.default_rng(1), np.random.default_rng(2))
                g = o['u2'] - base['u2']
                rec['gains2'][strat['name']] = (float(g.mean()), float(g.std(ddof=1) / math.sqrt(nrep)), float(o['win1'].mean()))
            b1 = max(rec['gains1'].items(), key=lambda kv: kv[1][0]); b2 = max(rec['gains2'].items(), key=lambda kv: kv[1][0])
            rec['best1'] = (b1[0], b1[1][0]); rec['best2'] = (b2[0], b2[1][0])
            rec['secs'] = time.time() - t0
            results.append(rec)
            print(f"{mech:5s} n={n:7d} rev/n={rec['rev_per_round']:.4f} Tw={rec['Tw_mean']:.0f} tau={rec['tau_mean']:.3f} "
                  f"best1={b1[0]} gain={b1[1][0]:.1f} ({b1[1][0]/n:.5f}/round) best2={b2[0]} gain={b2[1][0]:.1f} [{rec['secs']:.0f}s]", flush=True)
            with open(outpath, 'w') as f:
                json.dump(results, f, indent=1)
    return results

if __name__ == '__main__':
    ns = [float(x) for x in sys.argv[1].split(',')]
    nrep = int(sys.argv[2]); outpath = sys.argv[3]
    main(ns, nrep, outpath)
