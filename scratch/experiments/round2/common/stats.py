"""Interval estimators (Scout A4, Section 3.3): Student t primary, BCa secondary, Clopper-Pearson for proportions."""
from __future__ import annotations

import numpy as np
from scipy import stats


def t_interval(x, level: float = 0.95):
    x = np.asarray(x, dtype=float)
    n = x.size
    m = float(x.mean())
    if n < 2:
        return m, float("nan"), float("nan"), float("nan")
    sd = float(x.std(ddof=1))
    se = sd / np.sqrt(n)
    h = stats.t.ppf(0.5 + level / 2, n - 1) * se
    return m, m - h, m + h, se


def bca_paired(dev, base, rng, level: float = 0.95, n_resamples: int = 9999):
    dev = np.asarray(dev, dtype=float); base = np.asarray(base, dtype=float)
    if np.allclose(dev - base, (dev - base)[0]):
        d = float((dev - base)[0]); return d, d
    res = stats.bootstrap((dev, base), lambda a, b, axis=-1: np.mean(a - b, axis=axis), paired=True,
                          confidence_level=level, n_resamples=n_resamples, method="BCa", rng=rng)
    return float(res.confidence_interval.low), float(res.confidence_interval.high)


def clopper_pearson(k: int, n: int, level: float = 0.95):
    if n == 0:
        return float("nan"), float("nan")
    a = 1 - level
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return float(lo), float(hi)
