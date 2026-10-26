"""Loaders and fixed held-out splits for the two E4 datasets.

Fashion-MNIST (MIT) and UCI Covertype (CC BY 4.0) are read from the session scratchpad; the download URLs,
checksums and license statements are recorded in audit/round2/A/DATA_LICENSES.md. Nothing here writes into a
git tree, and no row of either dataset is copied out of the scratchpad.

Held-out pools. Fashion-MNIST uses its official 10,000 image test set, so the pool is the one the dataset
authors set aside and the 60,000 training images are the population the providers are trained from. Covertype
has no official split, so a fixed-seed random 100,000-row subset is held out and the remaining 481,012 rows are
the training population. Each pool is then split 50/50 with a fixed seed into a measurement half (where the
curves A_i(x, k) are measured) and a play half (where the mechanism draws its tasks), so no task used to
calibrate a target is ever played.
"""
from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np

POOL_SEED = 20260917      # which rows of Covertype are held out
SPLIT_SEED = 20260918     # measurement half against play half, both datasets
N_HOLDOUT_COVERTYPE = 100_000


def read_idx(path: Path) -> np.ndarray:
    with gzip.open(path, "rb") as f:
        magic = int.from_bytes(f.read(4), "big")
        ndim = magic & 0xFF
        dims = [int.from_bytes(f.read(4), "big") for _ in range(ndim)]
        buf = f.read()
    return np.frombuffer(buf, dtype=np.uint8).reshape(dims)


def load_fashion_mnist(data_root: Path):
    d = Path(data_root) / "fashion_mnist"
    Xtr = read_idx(d / "train-images-idx3-ubyte.gz").reshape(-1, 784)
    ytr = read_idx(d / "train-labels-idx1-ubyte.gz")
    Xte = read_idx(d / "t10k-images-idx3-ubyte.gz").reshape(-1, 784)
    yte = read_idx(d / "t10k-labels-idx1-ubyte.gz")
    assert Xtr.shape == (60000, 784) and Xte.shape == (10000, 784)
    return (np.ascontiguousarray(Xtr, dtype=np.float32), ytr.astype(np.int64),
            np.ascontiguousarray(Xte, dtype=np.float32), yte.astype(np.int64))


def load_covertype(data_root: Path):
    import pandas as pd
    d = Path(data_root) / "covertype"
    df = pd.read_csv(d / "covtype.data.gz", header=None)
    arr = df.to_numpy()
    assert arr.shape == (581012, 55), arr.shape
    X = np.ascontiguousarray(arr[:, :54], dtype=np.float32)
    y = arr[:, 54].astype(np.int64)
    rng = np.random.default_rng(POOL_SEED)
    perm = rng.permutation(X.shape[0])
    pool = np.sort(perm[:N_HOLDOUT_COVERTYPE])
    train = np.sort(perm[N_HOLDOUT_COVERTYPE:])
    return X[train], y[train], X[pool], y[pool]


def load(dataset: str, data_root: Path):
    """Returns (X_train_population, y_train_population, X_pool, y_pool) for the named dataset."""
    if dataset == "fashion_mnist":
        return load_fashion_mnist(data_root)
    if dataset == "covertype":
        return load_covertype(data_root)
    raise ValueError(dataset)


def half_split(n_pool: int, seed: int = SPLIT_SEED):
    """Fixed-seed 50/50 split of the pool into (measurement positions, play positions)."""
    rng = np.random.default_rng(seed)
    p = rng.permutation(n_pool)
    h = n_pool // 2
    return np.sort(p[:h]), np.sort(p[h:2 * h])
