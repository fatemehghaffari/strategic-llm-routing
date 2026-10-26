"""Experiment 1: false convictions and revenue of three winner rules under label noise.

Arms: 'pointwise' (paper's S*: min(tau, M_W(X_t))), 'label' (S*_N, known posterior),
'learn' (S^L, own Stage-1 empirical posterior, margin kappa_n). Orders: 'iid' pairs (satisfies (N)),
'bursty' (Markov true types with stay probability rho, i.i.d. classifier given the type: violates (N1)).
Reports: fraction of runs with ANY switch (every switch here is of a winner that follows its own rule),
revenue per round (sum of targets / n), benchmark E Mbar_(2)(B) and E M_(2)(X).
"""
import sys, math, time
import numpy as np
from clmesp import params, Profile, run

K, nA = 3, 3
# M[a, j]: rows types, columns agents
M = np.array([[0.90, 0.60, 0.50],
              [0.85, 0.55, 0.50],
              [0.00, 0.70, 0.50]])
mu = np.zeros_like(M)
honest = [False, False, False]
p = np.array([0.4, 0.3, 0.3])
eps = 0.3
C = np.full((nA, nA), eps / (nA - 1)); np.fill_diagonal(C, 1 - eps)
joint = p[:, None] * C
pb = joint.sum(0)
pi = (joint / pb[None, :]).T          # pi[b, a]
Mbar = pi @ M
m2bar = np.sort(Mbar, 1)[:, -2]; m2 = np.sort(M, 1)[:, -2]
n = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
R = int(sys.argv[2]) if len(sys.argv) > 2 else 30
L, ell, s, gam, eta = params(n, K)
kappa = math.sqrt((nA * math.log(2) + 4 * math.log(n)) / (2 * L))
print(f"n={n} L={L} s={s:.4f} kappa={kappa:.4f} ell={ell:.2f}")
print("pi[b,a]=", np.round(pi, 3).tolist())
print("Mbar[b,j]=", np.round(Mbar, 3).tolist())
W = Mbar.argmax(1)
tau_proxy = m2bar
sh = [float(pi[b] @ np.clip(tau_proxy[b] - M[:, W[b]], 0, None)) for b in range(nA)]
print("pointwise shortfall sh_b (price proxy Mbar_(2)) =", np.round(sh, 4).tolist())
print(f"benchmarks: E Mbar_(2)(B) = {pb @ m2bar:.4f}, E M_(2)(X) = {p @ m2:.4f}, "
      f"epsbar*max M_(2) = {eps * m2.max():.4f}")


def draw(order, rng, rho=0.995):
    if order == 'iid':
        X = rng.choice(nA, size=n, p=p)
    else:
        X = np.empty(n, dtype=int); X[0] = rng.choice(nA, p=p)
        stay = rng.random(n) < rho; fresh = rng.choice(nA, size=n, p=p)
        for t in range(1, n):
            X[t] = X[t - 1] if stay[t] else fresh[t]
    u = rng.random(n); cdf = np.cumsum(C, 1)
    B = (u[:, None] > cdf[X]).sum(1)
    return B, X


if __name__ == "__main__":
    res = {}
    t0 = time.time()
    for order in ('iid', 'bursty'):
        for arm in ('pointwise', 'label', 'learn'):
            conv = []; revs = []
            for seed in range(R):
                rng = np.random.default_rng(1000 + seed)
                B, X = draw(order, rng)
                prof = Profile(arm, M, mu, honest, pi=pi, kappa=kappa)
                out = run(B, X, K, nA, prof, np.random.default_rng(5000 + seed))
                conv.append(any(st['switch'] for st in out['labels'].values()))
                revs.append(out['rev'] / n)
            res[(order, arm)] = (np.mean(conv), np.mean(revs))
            print(f"{order:7s} {arm:9s} conv={np.mean(conv):.3f} ({sum(conv)}/{R}) rev={np.mean(revs):.4f} "
                  f"[{time.time() - t0:.0f}s]", flush=True)
