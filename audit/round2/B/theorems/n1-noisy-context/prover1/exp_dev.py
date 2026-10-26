"""Experiment 3: unilateral deviations of agent 0 against S*_N (known posterior) under i.i.d. pairs.

Common random numbers: the two executions share labels, true types, seeds, fallback coins and
priorities (Lemma C). Reports mean gain u_0(dev) - u_0(S*_N) with a standard error, and the
Theorem N(A) bound (first display, evaluated at the realised visit counts, averaged).
"""
import sys, math
import numpy as np
from clmesp import params, Profile, Mixed, run
import exp_conv as E   # reuses the instance (prints its header once)

K, nA, M, mu, pi, p, C = E.K, E.nA, E.M, E.mu, E.pi, E.p, E.C
n = E.n; R = int(sys.argv[3]) if len(sys.argv) > 3 else 20
L, ell, s, gam, eta = params(n, K)
RK = 3 * math.sqrt(K * n * math.log(K)) + 2 * K * math.log(K)
Mbar = pi @ M


class Dev:
    def __init__(self, kind, base):
        self.kind, self.base = kind, base
    def stage1(self, j, b, x, st):
        m = self.base.stage1(j, b, x, st)
        return max(0.0, m - 0.15) if self.kind in ('underbid', 'both') else m
    def primary(self, j, b, tau, x, st):
        if self.kind == 'pointwise':
            return min(tau, M[x, j])
        m = self.base.primary(j, b, tau, x, st)
        if self.kind in ('shade', 'both'):
            r = st['r'] + 1
            return max(0.0, m - 1.5 / math.sqrt(r))
        if self.kind == 'typegame':
            # same label mean, allocation skewed towards types seen less often in its own history
            resp = self.base.response(j, b, tau, st)
            return resp[x]
        return m
    def fallback(self, j, b, x, st):
        return self.base.fallback(j, b, x, st)


def bound(B):
    tot = 0.0
    for b in range(nA):
        V = int((B == b).sum()); N = max(V - K * L, 0)
        l0 = sum(1 for r in range(1, L + 1) if (r - 1) * K + 1 <= V)
        tot += l0
        if V < K * L:
            continue
        top = Mbar[b, 0] >= Mbar[b].max() - 1e-12
        if top:
            tot += 1 + 2 * math.sqrt(N * ell / 2) + RK
        else:
            d = max(Mbar[b, k] for k in range(K) if k != 0) - Mbar[b, 0]
            tot += (8 * (1 + math.sqrt(2 * ell)) ** 2 / d ** 2 + 2 * RK / d) if 4 * s <= d else 2 * N
    return tot + 8 / n ** 2


for kind in ('pointwise', 'underbid', 'shade', 'both'):
    gains = []; bds = []
    for seed in range(R):
        rng = np.random.default_rng(2000 + seed)
        B, X = E.draw('iid', rng)
        U = rng.random(n); xi = rng.random(n); perm = {b: rng.permutation(K) for b in range(nA)}
        base = Profile('label', M, mu, E.honest, pi=pi)
        o_star = run(B, X, K, nA, base, rng, U=U, xi=xi, perm=perm, mu=mu)
        base2 = Profile('label', M, mu, E.honest, pi=pi)
        o_dev = run(B, X, K, nA, Mixed(base2, 0, Dev(kind, base2)), rng, U=U, xi=xi, perm=perm, mu=mu)
        gains.append(o_dev['util'][0] - o_star['util'][0]); bds.append(bound(B))
    g = np.array(gains)
    print(f"dev={kind:9s} mean gain {g.mean():8.1f} (se {g.std(ddof=1)/math.sqrt(R):6.1f}); "
          f"Theorem N(A) bound {np.mean(bds):9.1f}; L={L}", flush=True)
