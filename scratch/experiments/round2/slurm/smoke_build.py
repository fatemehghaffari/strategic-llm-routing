"""Login-node smoke test of the E4 build path on a subsample (seconds, not the real bank)."""
import sys
import os
from pathlib import Path

import numpy as np

WT = Path(os.environ["R2_CODE_ROOT"])
sys.path.insert(0, str(WT / "scratch" / "experiments" / "round2"))
SP = Path(__file__).resolve().parents[1]

from provider_bank import build as BU, datasets as D, bank as B  # noqa: E402

_real = D.load


def small(dataset, root):
    Xtr, ytr, Xpool, ypool = _real(dataset, root)
    r = np.random.default_rng(0)
    a = r.choice(Xtr.shape[0], 4000, replace=False)
    b = r.choice(Xpool.shape[0], 800, replace=False)
    return Xtr[a], ytr[a], Xpool[b], ypool[b]


D.load = small
BU.D.load = small
out = SP / "runs" / "pilot" / "provider_bank" / "smoke"
bk = BU.build(sys.argv[1] if len(sys.argv) > 1 else "fashion_mnist", SP / "data", out, jobs=8, n_subsets=2)
c = bk.curves()
print("mu", np.round(c.mu_pooled, 4))
print("M ", np.round(c.M_pooled, 4))
print("A pooled\n", np.round(c.A_pooled, 4))
print("cells", c.n_cell)
bk2 = B.ResponseBank.load(bk.dataset, out)
assert bk2.K == 4 and np.array_equal(bk2.labels, bk.labels)
print("reload ok; curves.csv lines:", sum(1 for _ in (out / bk.dataset / "curves.csv").open()))
