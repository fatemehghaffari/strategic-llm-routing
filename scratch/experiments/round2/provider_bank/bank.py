"""Response bank for the E4 non-synthetic evaluation.

Evidence category: real labeled tasks and real provider answers; the effort choice is scripted.

Every outcome returned by this module is the correctness of an answer that a frozen scikit-learn provider
actually produced for a real labeled task drawn from a held-out pool, checked against that task's stored true
label. Nothing is drawn from a Bernoulli law. What is scripted is only the strategic part of the model: which
effort level (knob) the provider spends on the round, and, below its cheapest honest level, whether it returns
a deliberately wrong answer. The map from a target mean m to a knob is calibrated on a measurement half of the
pool that is disjoint from the play half on which the mechanism runs, so the realized frequency of correct
answers is a real quantity that can differ from the target the model assumes.

Knobs. The menu is {1, 2, 4, ..., 256}. For a forest provider the knob k is the number of trees evaluated: the
answer is the majority vote of a uniformly drawn subset of k of the 256 trained trees, with ties resolved to
the lowest class index. For the boosting provider the knob k is the number of stages used (staged_predict), so
its answer is deterministic given the task. Knob 0 is scripted sabotage: the provider returns a deliberately
wrong answer, which is the operational meaning of a target below the cheapest honest level. The recorded
compute cost of a round equals the knob value (0 for sabotage, since no tree is evaluated).

Capacities are menu relative by construction: M_i is the largest measured mean over this menu, not a property
of the provider in any wider sense.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

MENU = (1, 2, 4, 8, 16, 32, 64, 128, 256)
N_BINS = 5          # equal-width bins of the cheap-pass confidence in [0, 1]
CHEAP_PASS = 4      # trees (or boosting stages) used by the free confidence pass that defines the context
N_TREES = 256
N_SUBSETS = 8       # fresh random tree subsets per task when measuring a forest curve
CHUNK = 8192


def bin_of(share, n_bins: int = N_BINS) -> np.ndarray:
    """Equal-width bin index in {0, ..., n_bins - 1} of a confidence in [0, 1]."""
    s = np.asarray(share, dtype=float)
    return np.minimum(n_bins - 1, np.floor(s * n_bins)).astype(np.uint8)


def vote_context_bins(preds: np.ndarray, n_classes: int, cheap_pass: int = CHEAP_PASS,
                      n_bins: int = N_BINS) -> np.ndarray:
    """Context of a forest provider: vote share of the top class among its first `cheap_pass` trees."""
    head = preds[:cheap_pass].astype(np.int64)
    m = head.shape[1]
    flat = head + n_classes * np.arange(m, dtype=np.int64)[None, :]   # index = class + n_classes * task
    counts = np.bincount(flat.ravel(), minlength=n_classes * m).reshape(m, n_classes)
    share = counts.max(1) / float(cheap_pass)
    return bin_of(share, n_bins)


def prob_context_bins(top_prob, n_bins: int = N_BINS) -> np.ndarray:
    """Context of the boosting provider: top predicted probability after `CHEAP_PASS` stages."""
    return bin_of(np.asarray(top_prob, dtype=float), n_bins)


@dataclass
class Curves:
    """Unsmoothed measured curves on the measurement half. Nothing here is fitted or interpolated."""
    menu: tuple
    A_pooled: np.ndarray        # (K, J) context-free P(correct | knob)
    se_pooled: np.ndarray       # (K, J) task-clustered standard error
    A_cell: np.ndarray          # (K, N_BINS, J)
    se_cell: np.ndarray         # (K, N_BINS, J)
    n_cell: np.ndarray          # (K, N_BINS) measurement tasks per cell
    d_pooled: np.ndarray        # (K, J-1) paired mean of A(k_{j+1}) - A(k_j)
    d_se_pooled: np.ndarray     # (K, J-1)
    d_cell: np.ndarray          # (K, N_BINS, J-1)
    d_se_cell: np.ndarray       # (K, N_BINS, J-1)
    n_subsets: int

    @property
    def mu_pooled(self) -> np.ndarray:
        return self.A_pooled[:, 0].copy()

    @property
    def M_pooled(self) -> np.ndarray:
        return self.A_pooled.max(axis=1)

    @property
    def mu_cell(self) -> np.ndarray:
        return self.A_cell[:, :, 0].copy()

    @property
    def M_cell(self) -> np.ndarray:
        return np.nanmax(self.A_cell, axis=2)

    def to_npz(self, path: Path):
        np.savez_compressed(path, menu=np.asarray(self.menu), A_pooled=self.A_pooled, se_pooled=self.se_pooled,
                            A_cell=self.A_cell, se_cell=self.se_cell, n_cell=self.n_cell, d_pooled=self.d_pooled,
                            d_se_pooled=self.d_se_pooled, d_cell=self.d_cell, d_se_cell=self.d_se_cell,
                            n_subsets=np.asarray(self.n_subsets))

    @classmethod
    def from_npz(cls, path: Path) -> "Curves":
        z = np.load(path)
        return cls(tuple(int(x) for x in z["menu"]), z["A_pooled"], z["se_pooled"], z["A_cell"], z["se_cell"],
                   z["n_cell"], z["d_pooled"], z["d_se_pooled"], z["d_cell"], z["d_se_cell"], int(z["n_subsets"]))


class ResponseBank:
    """Frozen providers answering real labeled tasks, with the number of trees (or stages) as the effort knob."""

    def __init__(self, dataset: str, preds, labels, ctx_bins, meas_idx, play_idx, kinds,
                 menu=MENU, n_classes: int | None = None, curves: Curves | None = None, meta: dict | None = None):
        self.dataset = dataset
        self.preds = [np.ascontiguousarray(p, dtype=np.uint8) for p in preds]
        self.labels = np.ascontiguousarray(labels, dtype=np.uint8)
        self.ctx_bins = np.ascontiguousarray(ctx_bins, dtype=np.uint8)
        self.meas_idx = np.asarray(meas_idx, dtype=np.int64)
        self.play_idx = np.asarray(play_idx, dtype=np.int64)
        self.kinds = list(kinds)
        self.menu = tuple(int(k) for k in menu)
        self.n_classes = int(n_classes if n_classes is not None else max(int(p.max()) for p in self.preds) + 1)
        self._curves = curves
        self.meta = meta or {}
        assert self.ctx_bins.shape == (self.n_tasks, self.K)
        for p in self.preds:
            assert p.shape[1] == self.n_tasks

    # ================================================================ structure

    @property
    def K(self) -> int:
        return len(self.preds)

    @property
    def n_tasks(self) -> int:
        return int(self.labels.size)

    def n_units(self, provider: int) -> int:
        """Trees of a forest provider, or trained stages of the boosting provider."""
        return int(self.preds[provider].shape[0])

    def contexts(self, task: int) -> np.ndarray:
        """The full context profile of one task: one provider-local cheap-pass bin per provider (d = 1, D = K)."""
        return self.ctx_bins[int(task)].copy()

    def cell(self, task: int, provider: int | None = None):
        """Provider-local context cell of a task, or the full profile when `provider` is None."""
        if provider is None:
            return tuple(int(x) for x in self.ctx_bins[int(task)])
        return int(self.ctx_bins[int(task), int(provider)])

    def draw_task(self, rng) -> int:
        """A fresh task drawn uniformly with replacement from the play half."""
        return int(self.play_idx[rng.integers(self.play_idx.size)])

    def draw_tasks(self, rng, size) -> np.ndarray:
        return self.play_idx[rng.integers(self.play_idx.size, size=size)]

    # ================================================================ answering

    def _vote(self, provider: int, tasks: np.ndarray, knob: int, rand: np.ndarray | None, rng) -> np.ndarray:
        P = self.preds[provider]
        T = P.shape[0]
        m = tasks.size
        col = P[:, tasks].T                                    # (m, T) answers of every tree on every task
        if knob >= T:
            sel = col
        else:
            if rand is None:
                rand = rng.random((m, T))
            idx = np.argpartition(rand, knob - 1, axis=1)[:, :knob]
            sel = np.take_along_axis(col, idx.astype(np.int64), axis=1)
        flat = sel.astype(np.int64) + self.n_classes * np.arange(m, dtype=np.int64)[:, None]
        counts = np.bincount(flat.ravel(), minlength=self.n_classes * m).reshape(m, self.n_classes)
        return counts.argmax(axis=1).astype(np.uint8)          # argmax breaks ties at the lowest class index

    def answer_many(self, provider: int, tasks, knobs, rand=None, rng=None) -> np.ndarray:
        """Predicted class of `provider` on each task at each knob; 255 marks a sabotaged (deliberately wrong) answer."""
        tasks = np.asarray(tasks, dtype=np.int64)
        knobs = np.asarray(knobs, dtype=np.int64)
        out = np.empty(tasks.size, dtype=np.uint8)
        if rng is None:
            rng = np.random.default_rng(0)
        for k in np.unique(knobs):
            g = np.flatnonzero(knobs == k)
            if k <= 0:
                out[g] = 255
                continue
            if self.kinds[provider] == "stage":
                out[g] = self.preds[provider][int(k) - 1, tasks[g]]
                continue
            r = None if rand is None else np.asarray(rand)[g]
            for s in range(0, g.size, CHUNK):
                gg = g[s:s + CHUNK]
                rr = None if r is None else r[s:s + CHUNK]
                out[gg] = self._vote(provider, tasks[gg], int(k), rr, rng)
        return out

    def sample_many(self, provider: int, tasks, knobs, rand=None, rng=None):
        """Real outcomes (1 = the stored true label was returned) and the compute cost of each round."""
        tasks = np.asarray(tasks, dtype=np.int64)
        knobs = np.asarray(knobs, dtype=np.int64)
        ans = self.answer_many(provider, tasks, knobs, rand=rand, rng=rng)
        y = (ans == self.labels[tasks]).astype(np.uint8)
        y[knobs <= 0] = 0                                       # a sabotaged answer is wrong by construction
        cost = np.maximum(knobs, 0).astype(np.int64)
        return y, cost

    def sample(self, provider: int, task: int, knob: int, rng) -> int:
        """One real provider answer, scored against the stored true label. Returns 0 or 1."""
        y, _ = self.sample_many(provider, np.array([task]), np.array([knob]), rng=rng)
        return int(y[0])

    # ================================================================ calibration

    def set_curves(self, curves: Curves):
        self._curves = curves

    def curves(self) -> Curves:
        if self._curves is None:
            raise RuntimeError("curves have not been measured for this bank")
        return self._curves

    def accuracy_curve(self, provider: int, cell: int | None = None) -> np.ndarray:
        c = self.curves()
        return c.A_pooled[provider].copy() if cell is None else c.A_cell[provider, int(cell)].copy()

    def plan(self, provider: int, m: float, cell: int | None = None):
        """Knob plan whose calibrated mean is exactly m: (k_lo, k_hi, weight on k_lo, calibrated mean).

        The rule is the first upcrossing of the measured curve along the menu, so it is well defined even where
        the curve is not monotone in the knob. Knob 0 is scripted sabotage and is used only below the cheapest
        measured level, which is the operational meaning of a target below the intrinsic mean.
        """
        A = self.accuracy_curve(provider, cell)
        menu = self.menu
        m = float(m)
        if m <= 0.0:
            return 0, 0, 1.0, 0.0
        j = int(np.argmax(A >= m)) if np.any(A >= m) else -1
        if j < 0:                                               # target above every measured level: best knob
            b = int(np.argmax(A))
            return menu[b], menu[b], 1.0, float(A[b])
        if A[j] == m:
            return menu[j], menu[j], 1.0, float(m)
        if j == 0:                                              # below the cheapest level: mix with sabotage
            w = 1.0 - m / float(A[0]) if A[0] > 0 else 1.0
            w = min(1.0, max(0.0, w))
            return 0, menu[0], w, float((1.0 - w) * A[0])
        lo, hi = float(A[j - 1]), float(A[j])
        w = (hi - m) / (hi - lo)
        w = min(1.0, max(0.0, w))
        return menu[j - 1], menu[j], w, float(w * lo + (1.0 - w) * hi)

    def target_to_knob(self, provider: int, m: float, rng, cell: int | None = None) -> int:
        """Draw the knob (or the sabotage flag 0) that realizes the target mean m in calibration."""
        k_lo, k_hi, w, _ = self.plan(provider, m, cell)
        return int(k_lo) if float(rng.random()) < w else int(k_hi)

    def targets_to_knobs(self, provider: int, targets, coins, cells=None) -> np.ndarray:
        """Vectorized target_to_knob on a pre-drawn tape of mixture coins."""
        targets = np.asarray(targets, dtype=float)
        coins = np.asarray(coins, dtype=float)
        out = np.empty(targets.size, dtype=np.int64)
        if cells is None:
            for m in np.unique(targets):
                g = np.flatnonzero(targets == m)
                k_lo, k_hi, w, _ = self.plan(provider, float(m))
                out[g] = np.where(coins[g] < w, k_lo, k_hi)
        else:
            cells = np.asarray(cells)
            for c in np.unique(cells):
                for m in np.unique(targets[cells == c]):
                    g = np.flatnonzero((cells == c) & (targets == m))
                    k_lo, k_hi, w, _ = self.plan(provider, float(m), int(c))
                    out[g] = np.where(coins[g] < w, k_lo, k_hi)
        return out

    # ================================================================ persistence

    def save(self, root: Path):
        d = Path(root) / self.dataset
        d.mkdir(parents=True, exist_ok=True)
        for i, p in enumerate(self.preds):
            np.save(d / f"preds_{i}.npy", p)
        np.save(d / "labels.npy", self.labels)
        np.save(d / "ctx_bins.npy", self.ctx_bins)
        np.save(d / "meas_idx.npy", self.meas_idx)
        np.save(d / "play_idx.npy", self.play_idx)
        meta = dict(self.meta)
        meta.update({"dataset": self.dataset, "K": self.K, "menu": list(self.menu), "kinds": self.kinds,
                     "n_classes": self.n_classes, "n_tasks": self.n_tasks})
        (d / "meta.json").write_text(json.dumps(meta, indent=1))
        if self._curves is not None:
            self._curves.to_npz(d / "curves.npz")

    @classmethod
    def load(cls, dataset: str, root: Path) -> "ResponseBank":
        d = Path(root) / dataset
        meta = json.loads((d / "meta.json").read_text())
        preds = [np.load(d / f"preds_{i}.npy") for i in range(int(meta["K"]))]
        curves = Curves.from_npz(d / "curves.npz") if (d / "curves.npz").exists() else None
        return cls(dataset, preds, np.load(d / "labels.npy"), np.load(d / "ctx_bins.npy"),
                   np.load(d / "meas_idx.npy"), np.load(d / "play_idx.npy"), meta["kinds"],
                   menu=tuple(meta["menu"]), n_classes=int(meta["n_classes"]), curves=curves, meta=meta)


def _task_means(bank: ResponseBank, provider: int, tasks: np.ndarray, n_subsets: int, rng) -> np.ndarray:
    """Per-task mean correctness at every knob of the menu, averaged over fresh random subsets.

    Deterministic (boosting) providers use one evaluation per task; forest providers use `n_subsets`
    independently drawn subsets per task and per knob.
    """
    J = len(bank.menu)
    reps = 1 if bank.kinds[provider] == "stage" else n_subsets
    acc = np.zeros((J, tasks.size), dtype=np.float64)
    for j, k in enumerate(bank.menu):
        for _ in range(reps):
            for s in range(0, tasks.size, CHUNK):
                t = tasks[s:s + CHUNK]
                y, _ = bank.sample_many(provider, t, np.full(t.size, k), rng=rng)
                acc[j, s:s + CHUNK] += y
    return acc / reps


def _mean_se(x: np.ndarray):
    n = x.size
    if n == 0:
        return float("nan"), float("nan")
    if n == 1:
        return float(x[0]), float("nan")
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(n))


def measure_curves(bank: ResponseBank, n_subsets: int = N_SUBSETS, rng=None, tasks=None) -> Curves:
    """Measure A_i(x, k) and the pooled A_i(k). Unsmoothed; nothing is interpolated.

    The default task set is the measurement half, which is what the bank calibrates targets with. Passing the
    play half instead gives a diagnostic copy of the same curves on the tasks the mechanism actually plays;
    that copy is reported, never used to calibrate a target.
    """
    rng = rng if rng is not None else np.random.default_rng(0)
    K, J = bank.K, len(bank.menu)
    A_p = np.full((K, J), np.nan); se_p = np.full((K, J), np.nan)
    A_c = np.full((K, N_BINS, J), np.nan); se_c = np.full((K, N_BINS, J), np.nan)
    n_c = np.zeros((K, N_BINS), dtype=np.int64)
    d_p = np.full((K, J - 1), np.nan); ds_p = np.full((K, J - 1), np.nan)
    d_c = np.full((K, N_BINS, J - 1), np.nan); ds_c = np.full((K, N_BINS, J - 1), np.nan)
    tasks = bank.meas_idx if tasks is None else np.asarray(tasks, dtype=np.int64)
    for i in range(K):
        pk = _task_means(bank, i, tasks, n_subsets, rng)
        for j in range(J):
            A_p[i, j], se_p[i, j] = _mean_se(pk[j])
        for j in range(J - 1):
            d_p[i, j], ds_p[i, j] = _mean_se(pk[j + 1] - pk[j])
        cells = bank.ctx_bins[tasks, i]
        for c in range(N_BINS):
            g = np.flatnonzero(cells == c)
            n_c[i, c] = g.size
            if g.size == 0:
                continue
            for j in range(J):
                A_c[i, c, j], se_c[i, c, j] = _mean_se(pk[j][g])
            for j in range(J - 1):
                d_c[i, c, j], ds_c[i, c, j] = _mean_se((pk[j + 1] - pk[j])[g])
    return Curves(bank.menu, A_p, se_p, A_c, se_c, n_c, d_p, ds_p, d_c, ds_c, n_subsets)
