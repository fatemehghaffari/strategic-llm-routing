"""Exact checks on the two cheapest knobs of a forest provider.

At knob 1 and knob 2 the subset vote can be averaged over all subsets in closed form, so these two points of
the measured curve can be verified without Monte Carlo, and the knob-1 to knob-2 step can be explained.

Write T for the number of trees, y for a task's true label, n_y for the number of trees answering y on that
task, and N_{>y} for the number answering a class with a larger index. Drawing an unordered pair uniformly,

    A(1) = E[ n_y / T ],
    A(2) = E[ ( n_y (n_y - 1) + 2 n_y N_{>y} ) / (T (T - 1)) ]      (ties to the lowest class index),
    A(2) = E[ ( n_y (n_y - 1) + n_y (T - n_y) ) / (T (T - 1)) ] = A(1)   (ties broken uniformly at random).

The second line counts the pairs of two correct trees, plus the pairs of one correct and one incorrect tree
whose incorrect class index is above y, which the stated tie rule resolves to y. The third line is an identity:
with two voters and a random tie-break the accuracy is exactly that of one voter, so the whole of A(2) - A(1)
is the tie rule, not the providers. This is why the knob-1 to knob-2 step of a measured curve can be negative
while the rest of the curve rises, and why the sign differs across providers.
"""
from __future__ import annotations

import numpy as np

from .bank import ResponseBank


def class_counts(bank: ResponseBank, provider: int, tasks: np.ndarray) -> np.ndarray:
    """Counts of each class among all of a provider's trees, per task."""
    P = bank.preds[provider][:, tasks].T.astype(np.int64)     # (m, T)
    m, T = P.shape
    flat = P + bank.n_classes * np.arange(m, dtype=np.int64)[:, None]
    return np.bincount(flat.ravel(), minlength=bank.n_classes * m).reshape(m, bank.n_classes)


def exact_low_knobs(bank: ResponseBank, provider: int, tasks=None) -> dict:
    """Exact A(1) and A(2) under both tie rules, averaged over the given tasks (default: measurement half)."""
    tasks = bank.meas_idx if tasks is None else np.asarray(tasks, dtype=np.int64)
    if bank.kinds[provider] == "stage":
        return {"applies": False}
    counts = class_counts(bank, provider, tasks)
    T = int(bank.preds[provider].shape[0])
    lab = bank.labels[tasks].astype(np.int64)
    rows = np.arange(tasks.size)
    n_y = counts[rows, lab].astype(np.float64)
    upper = counts.cumsum(axis=1)[:, -1] - counts.cumsum(axis=1)[rows, lab]   # classes with index above y
    a1 = float(np.mean(n_y / T))
    a2_low = float(np.mean((n_y * (n_y - 1) + 2.0 * n_y * upper) / (T * (T - 1))))
    a2_rand = float(np.mean((n_y * (n_y - 1) + n_y * (T - n_y)) / (T * (T - 1))))
    return {"applies": True, "A1_exact": a1, "A2_exact_lowest_index_tiebreak": a2_low,
            "A2_exact_random_tiebreak": a2_rand, "step_from_tiebreak": a2_low - a1,
            "n_tasks": int(tasks.size)}


def compare_with_measured(bank: ResponseBank, provider: int) -> dict:
    """Exact values against the Monte Carlo curve, in units of the measured standard error."""
    ex = exact_low_knobs(bank, provider)
    if not ex["applies"]:
        return ex
    c = bank.curves()
    j1, j2 = bank.menu.index(1), bank.menu.index(2)
    se1, se2 = float(c.se_pooled[provider, j1]), float(c.se_pooled[provider, j2])
    ex.update({"A1_measured": float(c.A_pooled[provider, j1]), "A2_measured": float(c.A_pooled[provider, j2]),
               "A1_z": (c.A_pooled[provider, j1] - ex["A1_exact"]) / se1 if se1 > 0 else None,
               "A2_z": (c.A_pooled[provider, j2] - ex["A2_exact_lowest_index_tiebreak"]) / se2 if se2 > 0 else None})
    return ex
