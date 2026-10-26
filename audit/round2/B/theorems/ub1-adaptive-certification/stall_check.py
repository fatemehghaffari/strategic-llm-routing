"""UB1 diagnostic for REPORT 4.2: the winner's stalling deviation against the overshoot price p := UCB_l(T_c).
K=2, linear cost, mu=0. Agent 1 (deviator, M1), agent 2 at S* (M2 < M1). Race: alternate pulls, certify at
first equal count t with LCB_i(t) > UCB_j(t); cap L_max = n//8. Price p := min(hat m_l(T_c) + s(T_c), LCB_w(T_c))
(in [M_l, M_w] on G). Winner pulled for remaining rounds delivering p (no monitor failure modelled; the
monitor never convicts a winner delivering p). Baseline: deliver M1 throughout the race. Stall: deliver M2 for
the first T_stall pulls, then M1. Coupled agent-local seeds."""
import math, numpy as np
def run(n, M1, M2, Tstall, nrep=50, seed=11):
    Lmax = n // 8; ell = math.log(2 * n**4)
    rng = np.random.default_rng(seed)
    U1 = rng.random((nrep, Lmax)); U2 = rng.random((nrep, Lmax))
    t = np.arange(1, Lmax + 1); st = np.sqrt(ell / (2 * t))
    Y2 = (U2 <= M2).astype(np.int64); m2 = np.cumsum(Y2, 1) / t
    def play(tgt):
        Y1 = (U1 <= tgt).astype(np.int64); m1 = np.cumsum(Y1, 1) / t
        c1 = (m1 - st) > (m2 + st); c2 = (m2 - st) > (m1 + st)
        a1 = c1.any(1); a2 = c2.any(1)
        f1 = np.where(a1, c1.argmax(1) + 1, Lmax + 1); f2 = np.where(a2, c2.argmax(1) + 1, Lmax + 1)
        win1 = f1 <= f2
        Tc = np.minimum(np.minimum(f1, f2), Lmax)
        idx = np.arange(nrep)
        ml = np.where(win1, m2[idx, Tc - 1], m1[idx, Tc - 1]); mw = np.where(win1, m1[idx, Tc - 1], m2[idx, Tc - 1])
        sT = np.sqrt(ell / (2 * Tc))
        p = np.minimum(ml + sT, mw - sT)                      # overshoot price in [M_l, M_w] on G
        p = np.where(f1 <= Lmax, p, np.nan)                   # only the certified-winner branch is modelled
        costE = np.cumsum(tgt, 1)[idx, Tc - 1]                # linear cost of agent 1's race pulls
        u1 = np.where(win1, Tc * 1.0 - costE + (n - 2 * Tc) * (1 - p), np.nan)
        return dict(u1=u1, p=p, Tc=Tc, win1=win1, cert=f1 <= Lmax)
    base = play(np.full((nrep, Lmax), M1))
    tgt = np.where(np.arange(Lmax)[None, :] < Tstall, M2, M1)
    dev = play(np.broadcast_to(tgt, (nrep, Lmax)))
    ok = base['cert'] & dev['cert'] & base['win1'] & dev['win1']
    g = dev['u1'] - base['u1']
    return dict(n=n, frac_ok=ok.mean(), Tc_base=base['Tc'][ok].mean(), Tc_dev=dev['Tc'][ok].mean(),
                p_base=base['p'][ok].mean(), p_dev=dev['p'][ok].mean(),
                gain=g[ok].mean(), gain_se=g[ok].std(ddof=1) / math.sqrt(ok.sum()), gain_per_n=g[ok].mean() / n)
if __name__ == '__main__':
    for n in [10000, 31623, 100000, 316228]:
        for frac in [0.01, 0.03, 0.1]:
            r = run(n, 0.9, 0.5, Tstall=int(frac * n))
            print(f"n={n:7d} Tstall={frac:.2f}n ok={r['frac_ok']:.2f} Tc*={r['Tc_base']:.0f} Tc'={r['Tc_dev']:.0f} "
                  f"p*={r['p_base']:.4f} p'={r['p_dev']:.4f} gain={r['gain']:.0f} (se {r['gain_se']:.0f}) gain/n={r['gain_per_n']:.4f}", flush=True)
