"""Pathwise monotonicity of Static Grid-ETC (Theorem thm:grid-etc claims it is exact and pathwise).

Coupling: identical contexts, identical reward uniforms by (round, agent), identical exploration permutations and
cell priorities (the retained GridETC seeds cell randomness by (seed, cell key), so a shared coupling seed gives
identical permutations). Raising agent i's map pointwise to capacity must not increase any other agent's pull count
on any path.
"""
from __future__ import annotations

import importlib.util
import sys
import os
from pathlib import Path

import numpy as np

MAIN = Path(os.environ["R2_CODE_ROOT"])
_spec = importlib.util.spec_from_file_location("ci_run", MAIN / "scratch/experiments/final/contextual_incentives/run.py")
ci = importlib.util.module_from_spec(_spec); sys.modules["ci_run"] = ci; _spec.loader.exec_module(ci)


def counts(x, mu, targets, uniforms, n, h, q, coupling_seed, K=3):
    alg = ci.GridETC(K, h, q, coupling_seed); pulls = np.zeros(K, int)
    for t in range(n):
        a, st, is_exp = alg.choose(x[t])
        y = float(uniforms[t, a] < targets[t, a]); alg.update(st, a, y, is_exp); pulls[a] += 1
    return pulls


def one_path(args):
    rep, n, shade, raise_agent = args
    rng = np.random.default_rng(900000 + rep)
    K = 3; D = 3
    x = rng.random((n, D)); mu, cap = ci.means(x); uniforms = rng.random((n, K))
    h = n ** (-1 / (D + 3)); q = int(np.ceil(n ** (2 / (D + 3))))
    low = cap.copy(); low[:, raise_agent] = np.maximum(mu[:, raise_agent], cap[:, raise_agent] - shade)
    p_low = counts(x, mu, low, uniforms, n, h, q, 777000 + rep)
    p_high = counts(x, mu, cap, uniforms, n, h, q, 777000 + rep)
    return p_low, p_high


def check(reps, n, shade=0.10, raise_agent=0, workers=8):
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(one_path, [(r, n, shade, raise_agent) for r in range(reps)], chunksize=4))
    viol = []
    for r, (lo, hi) in enumerate(res):
        for j in range(len(lo)):
            if j != raise_agent and hi[j] > lo[j]:
                viol.append((r, j, int(lo[j]), int(hi[j])))
    return res, viol


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--reps", type=int, default=2000); ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=8); a = ap.parse_args()
    res, viol = check(a.reps, a.n, workers=a.workers)
    d = np.array([hi - lo for lo, hi in res])
    print(f"n={a.n} paths={a.reps}: violations {len(viol)}; other agents' pull-count change when agent 0 is raised: "
          f"mean {d[:, 1:].mean():.2f}, max {d[:, 1:].max()}, min {d[:, 1:].min()}; raised agent change mean {d[:, 0].mean():+.2f}")
    for v in viol[:5]:
        print("  violation:", v)
