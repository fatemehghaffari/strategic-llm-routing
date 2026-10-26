"""ADVERSARY priority 1: can a NON-top agent with deltabar_i just above 2 s_n gain more than its Stage-1 term?
PROVER2 claims: dbar > 2s  => gain <= l_i + O(n^-2)       (no 1/delta^2, no 2N);
                0 < dbar <= 2s => gain <= l_i + 1 + b_n(N) + R_K(n).
Paper prop:ctx-finite-exact(i): 2N_z if 4s > delta, else 8(1+sqrt(2l))^2/delta^2 + 2R_K/delta.
Uses PROVER2's one-label simulator (read-only import). Agent 1 is the deviator.
Usage: p1_nontop.py n R
"""
import sys, math, time
sys.path.insert(0, __file__.rsplit('/adv/', 1)[0] + '/prover2')
import numpy as np
from label_mesp_sim import Agent, Rider, AllLow, Shade, run, params

n = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
R = int(sys.argv[2]) if len(sys.argv) > 2 else 200
K = 3


class ZeroStage1Rider(Rider):
    """Stage 1: deliver 0 (maximal saving); afterwards rider h=15 (irrelevant unless it wins)."""
    def stage1(self, x):
        return np.zeros_like(self.M[x])


class GreedyRider(Rider):
    """Stage 1 full capacity (maximises the win chance); primary: deliver lo whenever the NEXT test passes
    with margin h; fallback: deliver lo (utility 2 per pull if selected)."""
    pass


def inst(pi, dbar):
    # three types; agent 0 top, agent 2 low honest; agent 1 at Mbar_0 - dbar.
    M0 = np.array([0.9, 0.3, 0.6]); M2 = np.array([0.5, 0.6, 0.9])
    Mb0 = pi @ M0
    # agent 1: constant capability equal to Mbar_0 - dbar (so its mixture is exactly that)
    M1 = np.full(3, Mb0 - dbar)
    return [M0, M1, M2], [np.zeros(3), np.zeros(3), np.array([0.2, 0.2, 0.3])], [False, False, True]


P = params(n, K)
L, s, ell, RK = P['L'], P['s'], P['ell'], P['RK']
N = n - K * L
bN = math.sqrt(N * ell / 2)
print(f"n={n} R={R} L={L} s={s:.4f} 2s={2*s:.4f} 4s={4*s:.4f} N={N} b_n(N)={bN:.0f} R_K={RK:.0f}")
for label, pi in [("noise-free", np.array([1.0, 0.0, 0.0])), ("noisy e_b=0.2", np.array([0.8, 0.1, 0.1]))]:
    for dbar in [0.005, 2*s - 0.005, 2*s + 0.005, 4*s - 0.005]:
        Ms, mus, hon = inst(pi, dbar)
        mk = lambda cls=None, **kw: [Agent(Ms[0], mus[0], hon[0], pi),
                                     (cls or Agent)(Ms[1], mus[1], hon[1], pi, **kw),
                                     Agent(Ms[2], mus[2], hon[2], pi)]
        base = run(mk(), n, R, 5)
        ub = base['util'][:, 1]
        l_i = L
        p2b = l_i + (0 if dbar > 2*s else 1 + bN + RK)
        paper = l_i + (2*N if 4*s > dbar else 8*(1+math.sqrt(2*ell))**2/dbar**2 + 2*RK/dbar)
        print(f"\n[{label}] dbar={dbar:.4f} ({'>' if dbar>2*s else '<='} 2s)  baseline win-rate(agent1)={np.mean(base['W']==1):.3f}"
              f"  PROVER2 bound={p2b:.0f}  paper bound={paper:.0f}")
        for name, cls, kw in [("greedy rider h=15, fb low", GreedyRider, dict(fb_mode='low', margin=15.0)),
                              ("greedy rider h=0, fb low", GreedyRider, dict(fb_mode='low', margin=0.0)),
                              ("all low post-bid", AllLow, {}),
                              ("shade 0.02", Shade, dict(delta=0.02)),
                              ("zero Stage-1 then rider", ZeroStage1Rider, dict(fb_mode='low', margin=15.0))]:
            out = run(mk(cls, **kw), n, R, 5)
            d = out['util'][:, 1] - ub
            print(f"   {name:28s} gain={d.mean():9.1f} +- {1.96*d.std(ddof=1)/math.sqrt(R):7.1f}  max={d.max():8.1f}"
                  f"  win={np.mean(out['W']==1):.3f}  ratio to P2 bound={d.mean()/p2b:.3f}")
