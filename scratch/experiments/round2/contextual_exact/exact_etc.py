"""Exact in-class (S_HDS) exploitability of Static Grid-ETC by cell decomposition (E3a).

Under fixed maps, Lemma lem:cell-law makes each agent's rewards in a cell i.i.d. with the cell-average target;
Grid-ETC's exploration ignores rewards and commitment is a function of the exploration counts. For a unilateral
deviator i with cell-average target m in cell C, with the others at capacity,

  U_C(m) = (1 + mu_bar_{i,C} - m) [ E min(V_C, K q_n) / K + p_i(m; C) E (V_C - K q_n)_+ ],

V_C ~ Binomial(n, nu(C)), p_i the exact commitment probability (deviator count Binomial(q_n, m) against the others'
Binomial(q_n, M_bar_{j,C}) with uniform priority on ties). The supremum over full-profile maps is the sum of
per-cell maxima over m in [0, M_bar_{i,C}]; over own-context maps it separates by the deviator's own interval.
Grid options: 'equal' (h = n^(-1/(D+3)), clipped last cell, as in the retained code) and 'dyadic' (h = 2^(-k_n)).
"""
from __future__ import annotations

import itertools
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.stats import binom

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.design import grid_width, grid_etc  # noqa: E402


@dataclass(frozen=True)
class Env:
    """K agents with d = 1 local contexts, product uniform law; mu_i and M_i are callables of the own coordinate
    with breakpoints listed for exact quadrature."""
    name: str
    K: int
    mu: tuple          # callables
    M: tuple           # callables
    breaks: tuple      # per agent, list of interior breakpoints
    honest: tuple


def env_current() -> Env:
    """contextual_incentives/run.py means(): capacities (.72, .72, .53 + .08 x_3), mu_i = .16 + .04 x_i."""
    return Env("current", 3, (lambda x: .16 + .04 * x,) * 3,
               (lambda x: .72 + 0 * x, lambda x: .72 + 0 * x, lambda x: .53 + .08 * x), ((), (), ()), (1, 2))


def env_separator() -> Env:
    """Scout A2 Section 5.4: M_0 = M_1 = .75, M_2(x) = .75 - .25 (.6 - x)_+; top set {0,1} below x_2 = .6, {0,1,2} above."""
    return Env("separator", 3, (lambda x: .16 + .04 * x, lambda x: .16 + .04 * x, lambda x: .20 + .04 * x),
               (lambda x: .75 + 0 * x, lambda x: .75 + 0 * x, lambda x: .75 - .25 * np.maximum(0.0, .6 - x)), ((), (), (.6,)), (1,))


ENVS = {"current": env_current, "separator": env_separator}


def intervals(h: float):
    b = math.ceil(1.0 / h - 1e-12)
    edges = [k * h for k in range(b)] + [1.0]
    return [(edges[k], edges[k + 1]) for k in range(b)]


def avg(f, lo, hi, breaks):
    pts = [p for p in breaks if lo < p < hi]
    val, _ = quad(f, lo, hi, points=pts or None, limit=200)
    return val / (hi - lo)


def others_win_weights(q: int, others_m: list[float], K: int) -> np.ndarray:
    """w[k] = P(deviator with exploration count k is committed) against others with counts Binomial(q, m_j)."""
    k = np.arange(q + 1)
    a = np.stack([binom.cdf(k - 1, q, m) for m in others_m]); bpm = np.stack([binom.pmf(k, q, m) for m in others_m])
    poly = np.zeros((len(others_m) + 1, q + 1)); poly[0] = 1.0
    for j in range(len(others_m)):
        new = np.zeros_like(poly); new[0] = poly[0] * a[j]; new[1:] = poly[1:] * a[j] + poly[:-1] * bpm[j]; poly = new
    w = poly[0].copy()
    for t in range(1, len(others_m) + 1):
        w += poly[t] / (t + 1)
    return w


class CellModel:
    def __init__(self, env: Env, n: int, i: int, grid: str = "equal", mult: float = 1.0, m_grid: int = 2001):
        self.env, self.n, self.i, self.grid = env, n, i, grid
        K = env.K; D = K
        self.h = grid_width(n, D, "etc", mult, grid); self.q = grid_etc(n, D, mult)[1]
        self.ivals = intervals(self.h)
        # per-agent per-interval averages
        self.mu_bar = [[avg(env.mu[j], lo, hi, env.breaks[j]) for (lo, hi) in self.ivals] for j in range(K)]
        self.M_bar = [[avg(env.M[j], lo, hi, env.breaks[j]) for (lo, hi) in self.ivals] for j in range(K)]
        self.lengths = [hi - lo for (lo, hi) in self.ivals]
        self.cells = list(itertools.product(range(len(self.ivals)), repeat=K))
        Kq = K * self.q
        self.explore = {}; self.exploit = {}; self.w = {}
        for c in self.cells:
            nu = float(np.prod([self.lengths[c[j]] for j in range(K)]))
            v = np.arange(0, Kq)
            below = float(np.sum((Kq - v) * binom.pmf(v, n, nu)))       # E (Kq - V)_+
            e_exploit = n * nu - Kq + below                              # E (V - Kq)_+
            self.exploit[c] = e_exploit; self.explore[c] = (n * nu - e_exploit) / K
            others = [self.M_bar[j][c[j]] for j in range(K) if j != i]
            self.w[c] = others_win_weights(self.q, others, K)
        # The commitment pmf depends only on (q, m), not on the cell, so it is computed once for the master grid.
        self.mgrid = np.linspace(0.0, 1.0, m_grid)
        self._kk = np.arange(self.q + 1)
        self._pm_grid = binom.pmf(self._kk[None, :], self.q, self.mgrid[:, None])

    def p_commit(self, c, m, pm=None):
        m = np.atleast_1d(np.asarray(m, dtype=float))
        if pm is None:
            pm = binom.pmf(self._kk[None, :], self.q, m[:, None])
        return pm @ self.w[c]

    def _U_grid(self, c, mask=None):
        """U on the master grid (optionally restricted by a boolean mask), using the cached pmf."""
        i = self.i
        g = self.mgrid if mask is None else self.mgrid[mask]
        pm = self._pm_grid if mask is None else self._pm_grid[mask]
        return g, (1 + self.mu_bar[i][c[i]] - g) * (self.explore[c] + (pm @ self.w[c]) * self.exploit[c])

    def U(self, c, m, pm=None):
        i = self.i
        return (1 + self.mu_bar[i][c[i]] - np.asarray(m)) * (self.explore[c] + self.p_commit(c, m, pm) * self.exploit[c])

    def utility_of_map(self, cell_avg):
        """cell_avg: function cell -> deviator's cell-average target."""
        return float(sum(self.U(c, cell_avg(c))[0] for c in self.cells))

    def baseline(self):
        return self.utility_of_map(lambda c: self.M_bar[self.i][c[self.i]])

    def sup_full(self, refine: int = 3):
        total = 0.0; argmax = {}
        masks = {}
        for c in self.cells:
            Mb = self.M_bar[self.i][c[self.i]]
            lo_t = self.mu_bar[self.i][c[self.i]] if self.i in self.env.honest else 0.0
            key = (round(lo_t, 12), round(Mb, 12))
            if key not in masks:
                masks[key] = (self.mgrid >= lo_t - 1e-12) & (self.mgrid <= Mb + 1e-12)
            g, u = self._U_grid(c, masks[key]); k = int(np.argmax(u)); best = (float(g[k]), float(u[k]))
            step = self.mgrid[1] - self.mgrid[0]
            for _ in range(refine):
                g2 = np.linspace(max(lo_t, best[0] - step), min(Mb, best[0] + step), 201); u2 = self.U(c, g2); k2 = int(np.argmax(u2))
                if u2[k2] > best[1]:
                    best = (float(g2[k2]), float(u2[k2]))
                step = g2[1] - g2[0]
            total += best[1]; argmax[c] = best[0]
        return total, argmax, self.n * (1 + self.q) * (self.mgrid[1] - self.mgrid[0]) / (100 ** refine)

    def sup_own(self):
        """Own-context maps: one cell average per own-axis interval."""
        i = self.i; total = 0.0; arg = {}
        for k in range(len(self.ivals)):
            cells = [c for c in self.cells if c[i] == k]
            Mb = self.M_bar[i][k]; lo_t = self.mu_bar[i][k] if i in self.env.honest else 0.0
            mask = (self.mgrid >= lo_t - 1e-12) & (self.mgrid <= Mb + 1e-12)
            g = self.mgrid[mask]; pm = self._pm_grid[mask]
            u = sum(self.U(c, g, pm) for c in cells); kk = int(np.argmax(u)); total += float(u[kk]); arg[k] = float(g[kk])
        return total, arg

    def stress_explore_then_shade(self):
        """Outside S_HDS: deliver M during own exploration pulls, then 0 (strategic) or mu (honest) in exploitation."""
        i = self.i; tot = 0.0
        for c in self.cells:
            Mb = self.M_bar[i][c[i]]; mub = self.mu_bar[i][c[i]]; low = mub if i in self.env.honest else 0.0
            tot += (1 + mub - Mb) * self.explore[c] + (1 + mub - low) * self.p_commit(c, Mb)[0] * self.exploit[c]
        return tot

    def exploration_share(self):
        return sum(self.explore[c] for c in self.cells) * self.env.K / self.n


def hand_picked_cell_avg(model: CellModel, dev: str, random_map=None):
    """Cell-average targets of the five maps in contextual_incentives/run.py for the focal agent 0 (own axis)."""
    i = model.i; assert i == 0
    mu0 = lambda x: .16 + .04 * x; cap0 = .72

    def shade_fn(dev):
        h = model.h
        if dev == "constant": return lambda z: .10 + 0 * z
        if dev == "cell-aligned": return lambda z: .14 * ((np.floor(z / h).astype(int) % 2) == 0)
        if dev == "grid-misaligned": return lambda z: .14 * (z < .37)
        if dev == "near-boundary": return lambda z: .16 * (np.abs(z - .5) <= .09)
        if dev == "random-fixed": return lambda z: random_map[np.minimum((z * 8).astype(int), 7)]
        raise ValueError(dev)
    s = shade_fn(dev)
    target = lambda z: np.maximum(mu0(z), cap0 - s(np.asarray(z)))
    avgs = []
    for (lo, hi) in model.ivals:
        # exact average of a piecewise-constant-shade map: integrate numerically with breakpoints at the map's jumps
        pts = sorted({.37, .41, .59} | {k / 8 for k in range(1, 8)} | {k * model.h for k in range(1, 40)})
        pts = [p for p in pts if lo < p < hi]
        val, _ = quad(lambda z: float(target(np.array([z]))[0]), lo, hi, points=pts or None, limit=400)
        avgs.append(val / (hi - lo))
    return lambda c: avgs[c[i]]
