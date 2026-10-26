"""Experiment 2: Proposition I on CL-MESP.

Types a=0, c=1, d=2; labels a=0, c=1; W = agent 0 with M_W = (1, 0, 0); agents 1, 2: 1/2 everywhere.
P1: a then c (deterministic).  P2: a then i.i.d. (a w.p. eps, d otherwise).  Labels built from one
uniform V_t as in PROVER1.md 13.2, so all worlds share (labels, seeds U, fallback coins xi, priorities).
Checks: (1) (P1, S*) and (P2, sigma~) produce identical allocation logs pathwise;
(2) pathwise G + P = D (hence in expectation); (3) conviction of W at label a on P1 vs P2.
"""
import sys
import numpy as np
from clmesp import params, Profile, run

K, nA = 3, 3
M = np.array([[1.0, 0.5, 0.5], [0.0, 0.5, 0.5], [0.0, 0.5, 0.5]])
mu = np.zeros_like(M)
honest = [False] * 3
eps = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2
n = int(sys.argv[2]) if len(sys.argv) > 2 else 40000
R = int(sys.argv[3]) if len(sys.argv) > 3 else 30
L, ell, s, gam, eta = params(n, K)
print(f"eps={eps} n={n} L={L} s={s:.4f}  4s<=1/2: {4*s <= 0.5}")


class Shade:
    """sigma~: S* (pointwise) in the first half, 0 in the second half; reads t."""
    def __init__(self, base):
        self.base, self.t = base, 0
    def set_t(self, t): self.t = t
    def _z(self): return self.t >= n // 2
    def stage1(self, j, b, x, st): return 0.0 if (j == 0 and self._z()) else self.base.stage1(j, b, x, st)
    def primary(self, j, b, tau, x, st): return 0.0 if (j == 0 and self._z()) else self.base.primary(j, b, tau, x, st)
    def fallback(self, j, b, x, st): return 0.0 if (j == 0 and self._z()) else self.base.fallback(j, b, x, st)


def stats(out):
    NII = sum(1 for (t, b, j, m, y) in out['alloc'] if t >= n // 2 and j == 0)
    D = sum(m for (t, b, j, m, y) in out['alloc'] if t >= n // 2 and j == 0 and b == 0)
    conv_a = out['labels'][0]['switch']
    return out['util'][0], NII, D, conv_a


ident = 0; rows = []
for seed in range(R):
    rng = np.random.default_rng(777 + seed)
    V = rng.random(n); U = rng.random(n); xi = rng.random(n)
    perm = {0: rng.permutation(K), 1: rng.permutation(K)}
    h = n // 2
    B = np.zeros(n, dtype=int); B[h:] = (V[h:] > eps).astype(int)       # label a=0 iff V <= eps
    X1 = np.zeros(n, dtype=int); X1[h:] = 1                               # P1: c
    X2 = np.zeros(n, dtype=int); X2[h:] = np.where(V[h:] <= eps, 0, 2)    # P2: a or d
    kw = dict(U=U, xi=xi, perm=perm, mu=mu, log=True)
    o1 = run(B, X1, K, nA, Profile('pointwise', M, mu, honest), rng, **kw)
    o2s = run(B, X2, K, nA, Shade(Profile('pointwise', M, mu, honest)), rng, **kw)
    o2 = run(B, X2, K, nA, Profile('pointwise', M, mu, honest), rng, **kw)
    same = [(a[1], a[2], a[3], a[4]) for a in o1['alloc']] == [(a[1], a[2], a[3], a[4]) for a in o2s['alloc']]
    ident += same
    u1, N1, D1, c1 = stats(o1); u2s, N2s, D2s, c2s = stats(o2s); u2, N2, D2, c2 = stats(o2)
    G = u2s - u2; P = N2 - N1
    rows.append((G, P, D2, G + P - D2, c1, c2, u1 - u2s))
rows = np.array(rows, dtype=float)
print(f"pathwise identical logs (P1,S*) vs (P2,sigma~): {ident}/{R}")
print(f"max |u_W(P1,S*) - u_W(P2,sigma~)| pathwise: {np.abs(rows[:,6]).max():.3e}")
print(f"max |G + P - D| pathwise: {np.abs(rows[:,3]).max():.3e}")
print(f"mean G = {rows[:,0].mean():.1f}, mean P = {rows[:,1].mean():.1f}, mean D = {rows[:,2].mean():.1f}, "
      f"eps n/4 = {eps*n/4:.1f}, (1/2-2s) eps n/2 = {(0.5-2*s)*eps*n/2:.1f}")
print(f"P(W switched at label a): P1 {rows[:,4].mean():.3f}, P2 {rows[:,5].mean():.3f}")
