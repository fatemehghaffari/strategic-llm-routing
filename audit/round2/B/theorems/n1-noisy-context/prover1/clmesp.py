"""Compact simulator of CL-MESP keyed on labels (PROVER1.md Section 2), for the N1 checks.

Round t: label B[t] (mechanism sees it), true type X[t] (selected agent sees it).
Parameters exactly as in the paper: L = min(n//(2K), ceil(n^{2/3} log(en)^{1/3})), ell = log(2n^4),
s = sqrt(log(2Kn^4)/(2L)), b(r) = sqrt(r ell/2), EXP3 gamma = min(1/2, sqrt(K log K/n)).
A strategy object gives the target: stage1(j,b,x,st), primary(j,b,tau,x,st), fallback(j,b,x,st).
Returns per-run records (switch per label, winner, tau, revenue as sum of targets, per-agent utility,
allocation log if asked).
"""
import math
import numpy as np


def params(n, K):
    L = min(n // (2 * K), math.ceil(n ** (2 / 3) * math.log(math.e * n) ** (1 / 3)))
    ell = math.log(2 * n ** 4)
    s = math.sqrt(math.log(2 * K * n ** 4) / (2 * L))
    gam = min(0.5, math.sqrt(K * math.log(K) / n))
    return L, ell, s, gam, gam / K


def waterfill(w, lo, hi, level):
    """sup c in [0,1] with sum w * clip(c, lo, hi) <= level; returns the response vector."""
    f = lambda c: float(np.sum(w * np.clip(c, lo, hi)))
    if f(1.0) <= level + 1e-15:
        return np.clip(1.0, lo, hi)
    a, b = 0.0, 1.0
    for _ in range(60):
        m = 0.5 * (a + b)
        if f(m) <= level:
            a = m
        else:
            b = m
    return np.clip(a, lo, hi)


class Profile:
    """Proposed profiles. kind in {'pointwise', 'label', 'learn'}; M[a, j], mu[a, j]; pi[b] (array over types)."""

    def __init__(self, kind, M, mu, honest, pi=None, kappa=0.0):
        self.kind, self.M, self.mu, self.honest, self.pi, self.kappa = kind, M, mu, honest, pi, kappa
        self.cache = {}

    def stage1(self, j, b, x, st):
        return self.M[x, j]

    def fallback(self, j, b, x, st):
        return self.M[x, j]

    def response(self, j, b, tau, st):
        key = (j, b)
        if key in self.cache:
            return self.cache[key]
        M, mu = self.M[:, j], self.mu[:, j]
        lo = mu if self.honest[j] else np.zeros_like(mu)
        if self.kind == 'pointwise':
            r = np.minimum(tau, M)
            if self.honest[j]:
                r = np.maximum(mu, r)
        else:
            if self.kind == 'label':
                w = self.pi[b]; t = tau
            else:
                cnt = st['types'][j]; w = cnt / cnt.sum(); t = tau + self.kappa
            lev = min(t, float(w @ M))
            if self.honest[j]:
                lev = max(float(w @ mu), lev)
            r = waterfill(w, lo, M, lev)
        self.cache[key] = r
        return r

    def primary(self, j, b, tau, x, st):
        return self.response(j, b, tau, st)[x]


class Mixed:
    """Agent i plays dev (an object with the same interface), the others play base."""

    def __init__(self, base, i, dev):
        self.base, self.i, self.dev = base, i, dev

    def _p(self, j):
        return self.dev if j == self.i else self.base

    def stage1(self, j, b, x, st): return self._p(j).stage1(j, b, x, st)
    def primary(self, j, b, tau, x, st): return self._p(j).primary(j, b, tau, x, st)
    def fallback(self, j, b, x, st): return self._p(j).fallback(j, b, x, st)


def run(B, X, K, nA, prof, rng, U=None, xi=None, perm=None, mu=None, log=False, t_index=False):
    n = len(B)
    L, ell, s, gam, eta = params(n, K)
    if U is None:
        U = rng.random(n)
    if xi is None:
        xi = rng.random(n)
    labels = {}
    rev = 0.0
    util = np.zeros(K)
    alloc = [] if log else None
    for t in range(n):
        b = int(B[t]); x = int(X[t])
        st = labels.get(b)
        if st is None:
            st = dict(v=0, sums=np.zeros(K), types=np.zeros((K, nA)), phase=1, W=-1, tau=0.0, r=0, Z=0.0,
                      logw=np.zeros(K), switch=False,
                      perm=(perm[b] if perm is not None else rng.permutation(K)))
            labels[b] = st
        st['v'] += 1
        v = st['v']
        if hasattr(prof, 'set_t'):
            prof.set_t(t)
        if st['phase'] == 1:
            j = (v - 1) % K
            m = prof.stage1(j, b, x, st)
            y = 1.0 if U[t] <= m else 0.0
            st['sums'][j] += y; st['types'][j, x] += 1
            if v == K * L:
                bids = st['sums'] / L
                mx = bids.max()
                tied = [k for k in range(K) if bids[k] == mx]
                W = min(tied, key=lambda k: list(st['perm']).index(k))
                st['W'] = W
                st['tau'] = max(float(np.sort(bids)[-2]) - s, 0.0)
                st['phase'] = 2
        elif st['phase'] == 2:
            j = st['W']
            m = prof.primary(j, b, st['tau'], x, st)
            y = 1.0 if U[t] <= m else 0.0
            st['r'] += 1; st['Z'] += y
            if st['Z'] < st['r'] * st['tau'] - math.sqrt(st['r'] * ell / 2):
                st['phase'] = 3; st['switch'] = True; st['switch_r'] = st['r']
        else:
            lw = st['logw'] - st['logw'].max()
            q = np.exp(lw); q /= q.sum()
            p = (1 - gam) * q + gam / K
            j = int(np.searchsorted(np.cumsum(p), xi[t]))
            j = min(j, K - 1)
            m = prof.fallback(j, b, x, st)
            y = 1.0 if U[t] <= m else 0.0
            st['logw'][j] += eta * y / p[j]
        rev += m
        if mu is not None:
            util[j] += 1 + mu[x, j] - m
        if log:
            alloc.append((t, b, j, m, y))
    return dict(labels=labels, rev=rev, util=util, alloc=alloc, L=L, s=s, ell=ell)
