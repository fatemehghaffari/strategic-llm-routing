"""ADVERSARY priority 4: independent check of the benchmark-loss claims.
P1: sum_a pi_b(a) M2(a) - Mbar2(b) <= e_b * max_a M2(a)              (Lab = A, iota = id)
P2: ... <= sum_{a != a0} pi_b(a) [M2(a) - m2^{a0}(a)]_+ <= 1 - pi_b(a0) for EVERY a0 (Bayes form, any Lab)
Honest: b analogues. Adversarial search: random + hill-climbing on the ratio loss / bound."""
import numpy as np
rng = np.random.default_rng(7)

def second(v): return np.sort(v)[-2]

def check(M, mu, H, pi):
    A = M.shape[1]
    M2 = np.array([second(M[:, a]) for a in range(A)])
    Mbar = M @ pi
    loss = pi @ M2 - second(Mbar)
    out = []
    for a0 in range(A):
        top2 = np.argsort(M[:, a0])[-2:]
        m2 = M[top2].min(0)
        bP2 = sum(pi[a] * max(M2[a] - m2[a], 0) for a in range(A) if a != a0)
        bP1 = (1 - pi[a0]) * M2.max()
        out.append((loss, bP2, bP1, 1 - pi[a0]))
    bh = np.array([mu[list(H), a].max() for a in range(A)])
    lossh = pi @ bh - max(mu[h] @ pi for h in H)
    outh = [(lossh, (1 - pi[a0]) * bh.max()) for a0 in range(A)]
    return out, outh

worst = dict(P2=-1, P1=-1, bayes=-1, h=-1)
for it in range(100000):
    K = rng.integers(2, 6); A = rng.integers(2, 6)
    M = rng.random((K, A)) ** rng.choice([0.3, 1, 3])
    mu = M * rng.random((K, A))
    H = set(rng.choice(K, size=rng.integers(1, K + 1), replace=False).tolist())
    pi = rng.dirichlet(np.full(A, rng.choice([0.2, 1, 5])))
    out, outh = check(M, mu, H, pi)
    for (loss, bP2, bP1, bay) in out:
        worst['P2'] = max(worst['P2'], loss - bP2)
        worst['P1'] = max(worst['P1'], loss - bP1)
        worst['bayes'] = max(worst['bayes'], loss - bay)
    for (lh, bh) in outh:
        worst['h'] = max(worst['h'], lh - bh)
print("max violation (loss - bound), negative or ~0 means the bound holds:")
for k, v in worst.items(): print(f"  {k:6s} {v:.3e}")
