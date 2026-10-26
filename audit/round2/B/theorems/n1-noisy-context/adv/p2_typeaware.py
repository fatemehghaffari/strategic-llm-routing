"""ADVERSARY priority 2: deviations that exploit the true types the deviator sees and the mechanism does not.
Instance built so that type-aware play makes rewards DETERMINISTIC given the type (M in {0,1}), removing the
seed noise the monitor's b_n is calibrated to, and letting the deviator track the monitor exactly.
Deviator = top agent 0. Posterior pi=(0.6,0.25,0.15). M_0=(1,0,1) so Mbar_0=0.75.
  type-rider(h): deliver 0 if the NEXT test passes with margin h whatever happens, else M_0(x) (0 or 1)
  type-burst: deliver M_0(x) only at type 0, 0 at type 2 (mean 0.6 < tau?) -- a fixed type-level shading
  seed-rider(h): PROVER2's Rider (lo or capacity), for comparison
Bound (PROVER2 (A)): l_i + 1 + b_n(N) + R_K(n).
"""
import sys, math
sys.path.insert(0, __file__.rsplit('/adv/', 1)[0] + '/prover2')
import numpy as np
from label_mesp_sim import Agent, Rider, run, params

n = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
R = int(sys.argv[2]) if len(sys.argv) > 2 else 100
K = 3
pi = np.array([0.6, 0.25, 0.15])
Ms = [np.array([1.0, 0.0, 1.0]), np.array([0.7, 0.6, 0.5]), np.array([0.5, 0.6, 0.9])]
mus = [np.zeros(3), np.zeros(3), np.array([0.2, 0.2, 0.3])]
hon = [False, False, True]


class TypeRider(Agent):
    def __init__(self, *a, margin=0.0, **k):
        super().__init__(*a, **k); self.margin = margin
    def primary(self, x, Z, r, tau, b):
        # worst case next reward is 0 under "deliver 0"; test at r+1 passes iff Z >= (r+1)tau - b(r+1)
        safe = Z >= (r + 1) * tau - b(r + 1) + self.margin
        return np.where(safe, 0.0, self.M[x])


class TypeOnlyZero(Agent):
    """deliver capacity only at type 0; 0 at type 2 (and type 1, capacity 0 anyway)."""
    def primary(self, x, Z, r, tau, b):
        return np.where(x == 0, self.M[x], 0.0)


class BlindRider(Agent):
    """CONTROL (method rule): the same riding rule with the type clause deleted: when unsafe deliver a
    type-blind level 0.75 at types where capacity allows it (types 0, 2), 0 at type 1 (forced by feasibility).
    Its pi-mean when unsafe is 0.75*(0.6+0.15)=0.5625 < Mbar_0, so the comparison is only qualitative."""
    def __init__(self, *a, margin=0.0, **k):
        super().__init__(*a, **k); self.margin = margin
    def primary(self, x, Z, r, tau, b):
        safe = Z >= (r + 1) * tau - b(r + 1) + self.margin
        return np.where(safe, 0.0, np.minimum(0.75, self.M[x]))


P = params(n, K); L, s, ell, RK = P['L'], P['s'], P['ell'], P['RK']
N = n - K * L; bN = math.sqrt(N * ell / 2)
bound = L + 1 + bN + RK
Mbar = np.array([pi @ M for M in Ms])
print(f"n={n} R={R} L={L} s={s:.4f} Mbar={Mbar.round(3)} b_n(N)={bN:.0f} R_K={RK:.0f} bound={bound:.0f}")
mk = lambda cls=None, **kw: [(cls or Agent)(Ms[0], mus[0], hon[0], pi, **kw), Agent(Ms[1], mus[1], hon[1], pi),
                             Agent(Ms[2], mus[2], hon[2], pi)]
base = run(mk(), n, R, 3)
ub = base['util'][:, 0]
print(f"baseline: win={np.mean(base['W']==0):.2f} conv={base['switched'].mean():.3f} tau={base['tau'].mean():.4f}")
for name, cls, kw in [("type-rider h=0", TypeRider, dict(margin=0.0)), ("type-rider h=3", TypeRider, dict(margin=3.0)),
                      ("type-rider h=10", TypeRider, dict(margin=10.0)), ("type-rider h=15", TypeRider, dict(margin=15.0)),
                      ("type-only-zero", TypeOnlyZero, {}),
                      ("seed-rider h=15 (P2's)", Rider, dict(fb_mode='cap', margin=15.0)),
                      ("seed-rider h=10", Rider, dict(fb_mode='cap', margin=10.0)),
                      ("CONTROL blind-rider h=15", BlindRider, dict(margin=15.0)),
                      ("CONTROL blind-rider h=10", BlindRider, dict(margin=10.0))]:
    out = run(mk(cls, **kw), n, R, 3)
    d = out['util'][:, 0] - ub
    print(f"  {name:24s} gain={d.mean():9.1f} +- {1.96*d.std(ddof=1)/math.sqrt(R):7.1f} conv={out['switched'].mean():.3f}"
          f"  gain/b_n(N)={d.mean()/bN:.3f}  gain/bound={d.mean()/bound:.3f}")
