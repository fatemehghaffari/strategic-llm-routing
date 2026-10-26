"""The four frozen providers of each E4 dataset, and the per-tree (or per-stage) prediction bank.

Heterogeneity comes from the training data, never from tampering with the trained models' answers. All four
providers see the same held-out pool and are frozen before any measurement. The effort knob is the number of
trees evaluated at inference (for the three forest providers) or the number of boosting stages used (for the
gradient-boosting provider); both are recorded as the round's compute cost.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np

from .bank import CHEAP_PASS, N_TREES, prob_context_bins, vote_context_bins

SKEW_WEIGHT = 8.0     # relative sampling weight of the favored classes in the class-skewed subset


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    family: str          # rf | et | hgb
    kind: str            # vote (a subset of trees is voted) | stage (boosting stages, deterministic)
    frac: float          # share of the training population used
    skew: bool
    random_state: int


SPECS = (
    ProviderSpec("rf_uniform20", "rf", "vote", 0.20, False, 0),
    ProviderSpec("rf_classskew20", "rf", "vote", 0.20, True, 1),
    ProviderSpec("et_uniform05", "et", "vote", 0.05, False, 2),
    ProviderSpec("hgb_uniform30", "hgb", "stage", 0.30, False, 3),
)


def subset_indices(y: np.ndarray, spec: ProviderSpec) -> np.ndarray:
    """Training rows for one provider: a uniform share, or the same budget skewed towards the lower classes."""
    n = y.size
    rng = np.random.default_rng([20260919, spec.random_state])
    target = int(round(spec.frac * n))
    if not spec.skew:
        return np.sort(rng.choice(n, size=target, replace=False))
    classes = np.unique(y)
    favored = classes[: int(math.ceil(len(classes) / 2))]
    w = np.array([SKEW_WEIGHT if c in favored else 1.0 for c in classes])
    share = w / w.sum()
    picks = []
    for c, s in zip(classes, share):
        idx = np.flatnonzero(y == c)
        k = min(idx.size, int(round(target * s)))
        picks.append(rng.choice(idx, size=k, replace=False))
    return np.sort(np.concatenate(picks))


def build_model(spec: ProviderSpec, n_jobs: int):
    from sklearn.ensemble import (ExtraTreesClassifier, HistGradientBoostingClassifier, RandomForestClassifier)
    if spec.family == "rf":
        return RandomForestClassifier(n_estimators=N_TREES, random_state=spec.random_state, n_jobs=n_jobs)
    if spec.family == "et":
        return ExtraTreesClassifier(n_estimators=N_TREES, random_state=spec.random_state, n_jobs=n_jobs)
    if spec.family == "hgb":
        return HistGradientBoostingClassifier(max_iter=N_TREES, early_stopping=False,
                                              random_state=spec.random_state)
    raise ValueError(spec.family)


def train(spec: ProviderSpec, X, y, n_jobs: int):
    idx = subset_indices(y, spec)
    model = build_model(spec, n_jobs)
    t0 = time.time()
    model.fit(X[idx], y[idx])
    return model, idx, time.time() - t0


def _encode(labels: np.ndarray, classes: np.ndarray) -> np.ndarray:
    pos = np.searchsorted(classes, labels)
    assert np.all(classes[pos] == labels)
    return pos.astype(np.uint8)


def prediction_bank(spec: ProviderSpec, model, X_pool: np.ndarray, classes: np.ndarray):
    """Per-unit predictions on the held-out pool as encoded class indices, plus the cheap-pass context bins.

    Forest providers: row t is the prediction of tree t, so the answer at knob k is the majority of any k rows.
    Boosting provider: row k is the prediction after k + 1 stages, which is deterministic given the task.
    The context is the provider-local cheap pass: the top-class vote share among the first CHEAP_PASS trees, or
    the top predicted probability after CHEAP_PASS stages, quantized to equal-width bins.
    """
    n = X_pool.shape[0]
    assert np.array_equal(np.asarray(model.classes_), classes), "a provider is missing a class of the pool"
    if spec.kind == "vote":
        P = np.empty((N_TREES, n), dtype=np.uint8)
        for t, est in enumerate(model.estimators_):
            P[t] = est.predict(X_pool).astype(np.uint8)
        ctx = vote_context_bins(P, len(classes), CHEAP_PASS)
        conf = _vote_share(P[:CHEAP_PASS], len(classes))
        return P, ctx, conf
    P = np.empty((N_TREES, n), dtype=np.uint8)
    conf = None
    for k, dec in enumerate(model.staged_decision_function(X_pool)):
        dec = np.asarray(dec)
        if dec.ndim == 1:
            raise ValueError("the boosting context assumes a multiclass decision function")
        P[k] = dec.argmax(1).astype(np.uint8)
        if k == CHEAP_PASS - 1:
            e = np.exp(dec - dec.max(axis=1, keepdims=True))
            conf = (e / e.sum(axis=1, keepdims=True)).max(axis=1)
    assert conf is not None
    return P, prob_context_bins(conf), conf


def _vote_share(head: np.ndarray, n_classes: int) -> np.ndarray:
    h = head.astype(np.int64)
    m = h.shape[1]
    flat = h + n_classes * np.arange(m, dtype=np.int64)[None, :]
    counts = np.bincount(flat.ravel(), minlength=n_classes * m).reshape(m, n_classes)
    return counts.max(1) / float(head.shape[0])


def check_full_knob_equals_model(spec: ProviderSpec, model, P: np.ndarray, X_pool: np.ndarray,
                                 classes: np.ndarray, n_check: int = 2000, rng=None) -> float:
    """Agreement rate between the knob-256 answer and the frozen model's own prediction, on a random sample.

    For the boosting provider the two must agree exactly (the last stage is the model). For a forest they need
    not: scikit-learn's forest averages the trees' class probabilities while the knob-256 answer is the trees'
    majority vote, which is the rule the effort knob interpolates. The rate is reported, not asserted.
    """
    rng = rng if rng is not None else np.random.default_rng(0)
    idx = rng.choice(X_pool.shape[0], size=min(n_check, X_pool.shape[0]), replace=False)
    ref = _encode(np.asarray(model.predict(X_pool[idx])), classes)
    if spec.kind == "stage":
        return float(np.mean(P[N_TREES - 1, idx] == ref))
    sub = P[:, idx].T.astype(np.int64)
    m = idx.size
    flat = sub + len(classes) * np.arange(m, dtype=np.int64)[:, None]
    counts = np.bincount(flat.ravel(), minlength=len(classes) * m).reshape(m, len(classes))
    return float(np.mean(counts.argmax(1) == ref))
