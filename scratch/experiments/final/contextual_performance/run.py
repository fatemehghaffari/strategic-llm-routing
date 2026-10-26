#!/usr/bin/env python3
"""Final contextual-performance experiments.

All methods in a trial see the same context path and arm-by-round uniforms.
Reported reward/regret uses conditional means, reducing irrelevant Bernoulli
noise while preserving the feedback noise seen by the learning algorithms.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

OUT = Path(os.environ.get("CP_OUT", Path(__file__).resolve().parent))
COLS = ["trial", "seed", "family", "D", "K", "d", "n", "method", "index", "tiling",
        "grid_multiplier", "expected_reward", "oracle_regret",
        "honest_shortfall", "allocation_accuracy", "effort", "runtime_s",
        "state_count", "parameter_count"]


def environment(x: np.ndarray, family: str) -> tuple[np.ndarray, np.ndarray]:
    """Intrinsic means and feasible capacities for x with shape (n,K,d)."""
    n, k, d = x.shape
    base = x.mean(axis=2)
    mu = .12 + .10 * base + .015 * np.arange(k)[None, :]
    if family == "linear":
        # Exactly affine and arm-local: M_i depends only on x_i. LinUCB still
        # receives the full profile, whose cross-arm coefficients are zero.
        weights = np.linspace(.7, 1.3, d); weights /= weights.sum()
        own_affine = np.einsum("nkd,d->nk", x, weights)
        M = .34 + .38 * own_affine + .025 * np.arange(k)[None, :]
    elif family == "smooth":
        cross = np.sin(2 * np.pi * x[:, :, 0])
        second = np.cos(2 * np.pi * x[:, :, min(1, d - 1)])
        M = .48 + .16 * cross + .09 * second + .025 * np.arange(k)[None, :]
    elif family == "checkerboard":
        parity = (np.floor(4 * x).astype(int).sum(axis=2) % 2)
        M = .38 + .30 * parity + .035 * np.arange(k)[None, :]
    elif family == "finite":
        parity = (np.rint(2 * x).astype(int).sum(axis=2) % 2)
        M = .40 + .22 * parity + .04 * np.arange(k)[None, :]
    else:
        raise ValueError(family)
    return np.clip(mu, 0, .4), np.clip(np.maximum(M, mu), 0, .95)


class UCB:
    """Context-blind UCB1. `horizon` selects the confidence width: a known horizon N gives
    sqrt(4 log N / T_a), which is the index the paper specifies and the one its monotonicity
    argument requires; horizon=None gives the anytime width sqrt(2 log t / T_a)."""
    def __init__(self, k: int, horizon: int | None = None):
        self.k = k; self.n = np.zeros(k, int); self.z = np.zeros(k); self.horizon = horizon
    def width(self, t):
        return np.sqrt((4 * np.log(max(2, self.horizon)) if self.horizon
                        else 2 * np.log(max(2, t))) / self.n)
    def choose(self, _x, t, rng):
        unseen = np.flatnonzero(self.n == 0)
        if unseen.size: return int(unseen[0])
        return int(np.argmax(self.z / self.n + self.width(t)))
    def update(self, _x, a, y): self.n[a] += 1; self.z[a] += y
    def complexity(self): return 1, 2 * self.k


class CellUCB:
    """Cell-local UCB on a fixed grid.

    `horizon` selects the confidence width exactly as in UCB above, with the agent's LOCAL count in
    the cell and the GLOBAL horizon. `tiling` selects the grid: "exact" partitions each axis into
    b = round(1/h) equal parts, which tiles the closed cube; "clipped" uses ceil(1/h) parts and
    absorbs the remainder into the last cell, which creates thin cells that never finish exploring.
    The paper specifies the exact tiling."""
    def __init__(self, k: int, h: float, exact=False, horizon: int | None = None, tiling="exact"):
        self.k, self.h, self.exact, self.cells = k, h, exact, {}
        self.horizon, self.tiling = horizon, tiling
        self.b = max(1, int(round(1 / h))) if tiling == "exact" else math.ceil(1 / h)
    def key(self, x):
        if self.exact: return tuple(x.ravel())
        return tuple(np.minimum((x.ravel() * self.b).astype(int), self.b - 1))
    def choose(self, x, _t, _rng):
        key = self.key(x)
        n, z = self.cells.setdefault(key, (np.zeros(self.k, int), np.zeros(self.k)))
        unseen = np.flatnonzero(n == 0)
        if unseen.size: a = int(unseen[0])
        else:
            w = np.sqrt((4 * np.log(max(2, self.horizon)) if self.horizon
                         else 2 * np.log(max(2, n.sum()))) / n)
            a = int(np.argmax(z / n + w))
        return a
    def update(self, x, a, y):
        n, z = self.cells[self.key(x)]; n[a] += 1; z[a] += y
    def complexity(self): return len(self.cells), 2 * self.k * len(self.cells)


class CellETC:
    def __init__(self, k: int, h: float, q: int, tiling="exact"):
        self.k, self.h, self.q, self.cells = k, h, q, {}
        self.b = max(1, int(round(1 / h))) if tiling == "exact" else math.ceil(1 / h)
    def key(self, x):
        return tuple(np.minimum((x.ravel() * self.b).astype(int), self.b - 1))
    def choose(self, x, _t, _rng):
        key = self.key(x)
        if key not in self.cells:
            self.cells[key] = {"n": np.zeros(self.k, int), "z": np.zeros(self.k),
                               "v": 0, "perm": _rng.permutation(self.k),
                               "priority": _rng.permutation(self.k)}
        st = self.cells[key]
        if st["v"] < self.k * self.q:
            if st["v"] and st["v"] % self.k == 0: st["perm"] = _rng.permutation(self.k)
            a = int(st["perm"][st["v"] % self.k])
        else:
            vals = st["z"] / self.q; best = np.flatnonzero(vals == vals.max())
            rank = np.empty(self.k, int); rank[st["priority"]] = np.arange(self.k)
            a = int(best[np.argmin(rank[best])])
        st["v"] += 1
        return a
    def update(self, x, a, y):
        st = self.cells[self.key(x)]
        # The counter was incremented in choose; post-exploration feedback is ignored.
        if st["v"] <= self.k * self.q: st["n"][a] += 1; st["z"][a] += y
    def complexity(self): return len(self.cells), (2 * self.k + 1) * len(self.cells)


class LinUCB:
    def __init__(self, k: int, D: int, alpha=1.0):
        self.k, self.p, self.alpha = k, D + 1, alpha
        self.Ainv = [np.eye(self.p) for _ in range(k)]
        self.b = [np.zeros(self.p) for _ in range(k)]
    def choose(self, x, _t, _rng):
        f = np.r_[1., x.ravel()]
        vals = []
        for a in range(self.k):
            ai = self.Ainv[a]
            vals.append(self.b[a] @ ai @ f + self.alpha * math.sqrt(f @ ai @ f))
        return int(np.argmax(vals))
    def update(self, x, a, y):
        f = np.r_[1., x.ravel()]; ai = self.Ainv[a]; af = ai @ f
        self.Ainv[a] = ai - np.outer(af, af) / (1 + f @ af)
        self.b[a] += y * f
    def complexity(self): return 1, self.k * (self.p * self.p + self.p)


def run_one(spec):
    trial, family, D, n, mult, seed, index, tiling = spec
    known = n if index == "known" else None
    k = 2 if D % 2 == 0 else 3
    d = D // k
    rng = np.random.default_rng(seed)
    if family == "finite":
        levels = np.array([.15, .50, .85])
        x = levels[rng.integers(0, 3, size=(n, k, d))]
    else:
        x = rng.random((n, k, d))
    mu, cap = environment(x, family)
    uniforms = rng.random((n, k))
    hu = (math.log(math.e * n) / n) ** (1 / (D + 2)) * mult
    he = n ** (-1 / (D + 3)) * mult
    q = math.ceil(n ** (2 / (D + 3)))
    algos = {
        "Grid-UCB": CellUCB(k, hu, horizon=known, tiling=tiling),
        "Grid-ETC": CellETC(k, he, q, tiling=tiling),
        "LinUCB": LinUCB(k, D),
        "Global UCB": UCB(k, horizon=known),
    }
    if family == "finite":
        algos["Finite-context UCB"] = CellUCB(k, 1., exact=True, horizon=known)
    oracle = cap.max(axis=1)
    honest = mu.max(axis=1)
    out = []
    for name, alg in algos.items():
        start = time.perf_counter(); reward = effort = correct = 0.
        for t in range(n):
            a = alg.choose(x[t], t + 1, rng)
            y = float(uniforms[t, a] < cap[t, a])
            alg.update(x[t], a, y)
            reward += cap[t, a]
            effort += cap[t, a] - mu[t, a]
            correct += (a == int(np.argmax(cap[t])))
        states, params = alg.complexity()
        out.append(dict(trial=trial, seed=seed, family=family, D=D, K=k, d=d, n=n,
                        method=name, grid_multiplier=mult, index=index, tiling=tiling,
                        expected_reward=reward,
                        oracle_regret=float(oracle.sum() - reward),
                        honest_shortfall=float(honest.sum() - reward),
                        allocation_accuracy=correct / n, effort=effort,
                        runtime_s=time.perf_counter() - start,
                        state_count=states, parameter_count=params))
    return out


def bootstrap(rows, metrics, B=2000):
    rng = np.random.default_rng(20260828)
    keys = ["family", "D", "n", "method", "grid_multiplier", "index", "tiling"]
    groups = {}
    for r in rows: groups.setdefault(tuple(r[k] for k in keys), []).append(r)
    summary = []
    for key, rs in groups.items():
        z = dict(zip(keys, key)); z["reps"] = len(rs)
        for metric in metrics:
            a = np.array([float(r[metric]) for r in rs]); idx = rng.integers(0, len(a), (B, len(a)))
            means = a[idx].mean(axis=1)
            z[metric + "_mean"] = a.mean()
            z[metric + "_lo"] = np.quantile(means, .025)
            z[metric + "_hi"] = np.quantile(means, .975)
        summary.append(z)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=100)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--index", choices=("known", "anytime"), default="known",
                    help="confidence width; 'known' is the index the paper specifies")
    ap.add_argument("--tiling", choices=("exact", "clipped"), default="exact",
                    help="grid geometry; 'exact' is the tiling the paper specifies")
    args = ap.parse_args()
    reps = 2 if args.quick else args.reps
    horizons = [500, 2000] if args.quick else [2000, 8000]
    specs = []
    trial = 0
    # Core: continuous families at low and high full-profile dimension.
    for family in ["linear", "smooth", "checkerboard"]:
        for D in [2, 6]:
            for n in horizons:
                for rep in range(reps):
                    trial += 1; specs.append((trial, family, D, n, 1., 910000 + trial, args.index, args.tiling))
    # Exact finite-context benchmark.
    for n in horizons:
        for rep in range(reps):
            trial += 1; specs.append((trial, "finite", 2, n, 1., 910000 + trial, args.index, args.tiling))
    # Grid-width sensitivity, plotted separately; all points retain 100 reps.
    if not args.quick:
        for mult in [.75, 1.5]:
            for rep in range(reps):
                trial += 1; specs.append((trial, "smooth", 2, 8000, mult, 910000 + trial, args.index, args.tiling))
    if args.workers == 1:
        nested = [run_one(s) for s in specs]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as ex: nested = list(ex.map(run_one, specs, chunksize=2))
    rows = [r for rr in nested for r in rr]
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "trials.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    metrics = ["expected_reward", "oracle_regret", "honest_shortfall",
               "allocation_accuracy", "effort", "runtime_s", "state_count", "parameter_count"]
    summary = bootstrap(rows, metrics)
    with (OUT / "summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=summary[0]); w.writeheader(); w.writerows(summary)
    print(f"wrote {len(rows)} method-runs from {len(specs)} paired trials")


if __name__ == "__main__": main()
