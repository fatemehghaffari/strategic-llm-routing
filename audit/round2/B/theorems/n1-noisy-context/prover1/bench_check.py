"""Check the label-benchmark inequalities of Theorem N(B),(C) (PROVER1.md Lemma B).

Claim B1: for every label b (Lab = A), with e_b = 1 - pi_b(b),
    E[M_(2)(X) | B=b] - Mbar_(2)(b) <= e_b * max_a M_(2)(a).
Claim B2 (honest): E[b(X) | B=b] - bbar(b) <= e_b * max_a b(a), b(a) = max_h mu_h(a).
Also reports the SCOUT bound e_b (omega + omega_2) for comparison, and the tight example.
Random instances: K in 2..6, |A| in 2..7, random posteriors (Dirichlet), random M, mu.
"""
import numpy as np
rng = np.random.default_rng(20260929)
def second(v):
    return np.sort(v)[-2]
worst1 = worst2 = 0.0; viol1 = viol2 = 0; trials = 0; scout_ratio = 0.0
for it in range(200000):
    K = rng.integers(2, 7); A = rng.integers(2, 8)
    M = rng.random((A, K)) ** rng.choice([0.3, 1, 3])
    mu = M * rng.random((A, K))
    H = rng.random(K) < 0.5
    if not H.any(): H[rng.integers(K)] = True
    b = rng.integers(A)
    alpha = rng.choice([0.1, 1.0, 5.0])
    pi = rng.dirichlet(np.full(A, alpha))
    # push mass to b sometimes (small errors)
    if rng.random() < 0.5:
        w = rng.random(); pi = w * pi; pi[b] += 1 - w
    e = 1 - pi[b]
    if e < 1e-12: continue
    trials += 1
    M2 = np.array([second(M[a]) for a in range(A)])
    Mbar = pi @ M
    lhs1 = pi @ M2 - second(Mbar)
    rhs1 = e * M2.max()
    ba = mu[:, H].max(1)
    lhs2 = pi @ ba - (pi @ mu[:, H]).max()
    rhs2 = e * ba.max()
    if lhs1 > rhs1 + 1e-12: viol1 += 1
    if lhs2 > rhs2 + 1e-12: viol2 += 1
    if rhs1 > 1e-9: worst1 = max(worst1, lhs1 / rhs1)
    if rhs2 > 1e-9: worst2 = max(worst2, lhs2 / rhs2)
    om = (M.max(0) - M.min(0)).max(); om2 = M2.max() - M2.min()
    if e * (om + om2) > 1e-9: scout_ratio = max(scout_ratio, lhs1 / (e * (om + om2)))
print(f"trials {trials}; B1 violations {viol1}, worst ratio lhs/rhs {worst1:.4f}")
print(f"B2 violations {viol2}, worst ratio {worst2:.4f}")
print(f"worst ratio against SCOUT bound e_b(omega+omega_2): {scout_ratio:.4f}")
# tight example of SCOUT section 1.3(B)
for e in (0.05, 0.2, 0.5):
    M = np.array([[1, 1, 0], [0, 1, 1.0]]); pi = np.array([1 - e, e])
    M2 = np.array([second(r) for r in M])
    print(f"tight example e={e}: loss {pi @ M2 - second(pi @ M):.4f}, bound {e * M2.max():.4f}")
