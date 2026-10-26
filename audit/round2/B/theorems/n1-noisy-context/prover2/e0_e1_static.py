"""PROVER2 static checks (no simulation of the mechanism).

E0: benchmark loss  E M_(2)(X) - E Mbar_(2)(B)  and honest loss  E b(X) - E bbar(B)
    against the bounds of Lemma 5 / Part 3 (constant 1, Bayes error, refined omega'),
    and against the scout's eps*(omega+omega_2); tightness examples.
E1: water-fill optimality for convex costs (vs scipy SLSQP) and the honest dominance counterexample.
"""
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(20260929)


def second(v):
    return np.sort(v)[-2]


def e0_random(trials=20000):
    worst_ratio = 0.0          # loss / eps  (Lab = A, iota = id)
    worst_bayes = 0.0          # loss / bayes error
    worst_refined = -1.0       # loss - omega' * eps   (should be <= 0)
    scout_viol = 0             # cases where refined bound < scout bound fails (should be 0)
    hon_ratio = 0.0
    for _ in range(trials):
        A = rng.integers(2, 5)
        K = rng.integers(2, 6)
        M = rng.random((K, A)) ** rng.choice([0.3, 1, 3])       # M[j, a]
        mu = M * rng.random((K, A))
        honest = rng.random(K) < 0.5
        if not honest.any():
            honest[0] = True
        p = rng.dirichlet(np.ones(A))
        C = rng.dirichlet(np.ones(A) * rng.choice([0.3, 1, 5]), size=A)  # C[a, b]
        C = 0.5 * C + 0.5 * np.eye(A) * rng.random()  # push towards correct labels
        C /= C.sum(1, keepdims=True)
        joint = p[:, None] * C            # P(X=a, B=b)
        PB = joint.sum(0)
        keep = PB > 1e-12
        post = joint[:, keep] / PB[keep]  # post[a, b]
        labs = np.arange(A)[keep]
        PBk = PB[keep]
        M2 = np.array([second(M[:, a]) for a in range(A)])
        EM2X = (p * M2).sum()
        Mbar = M @ post                   # Mbar[j, b]
        EM2B = sum(PBk[k] * second(Mbar[:, k]) for k in range(len(labs)))
        loss = EM2X - EM2B
        eps = sum(PBk[k] * (1 - post[labs[k], k]) for k in range(len(labs)))
        bayes = sum(PBk[k] * (1 - post[:, k].max()) for k in range(len(labs)))
        # refined omega'
        om = 0.0
        for k, b in enumerate(labs):
            top2 = np.argsort(M[:, b])[-2:]
            for a in range(A):
                if a != b:
                    om = max(om, M2[a] - M[top2, a].min())
        omega = (M.max(1) - M.min(1)).max()
        omega2 = M2.max() - M2.min()
        if eps > 1e-9:
            worst_ratio = max(worst_ratio, loss / eps)
            worst_refined = max(worst_refined, loss - om * eps)
            if om > omega + omega2 + 1e-12:
                scout_viol += 1
        if bayes > 1e-9:
            worst_bayes = max(worst_bayes, loss / bayes)
        # honest
        bX = np.array([mu[honest, a].max() for a in range(A)])
        EbX = (p * bX).sum()
        mubar = mu @ post
        EbB = sum(PBk[k] * mubar[honest, k].max() for k in range(len(labs)))
        if eps > 1e-9:
            hon_ratio = max(hon_ratio, (EbX - EbB) / eps)
    print(f"E0 random ({trials} instances):")
    print(f"  max loss/eps           = {worst_ratio:.4f}   (bound 1)")
    print(f"  max loss/BayesErr      = {worst_bayes:.4f}   (bound 1)")
    print(f"  max loss - omega'*eps  = {worst_refined:.2e} (bound 0)")
    print(f"  omega' > omega+omega_2 : {scout_viol} cases (should be 0)")
    print(f"  max honest loss/eps    = {hon_ratio:.4f}   (bound 1)")


def e0_tight():
    for e in [0.05, 0.1, 0.2, 0.4]:
        post = np.array([[1 - e, e], [e, 1 - e]])  # post[a, b], symmetric, P_B uniform
        M = np.array([[1, 0], [1, 1], [0, 1]], float)  # scout example M(a)=(1,1,0), M(c)=(0,1,1)
        Mbar = M @ post
        loss = 1 - np.mean([second(Mbar[:, k]) for k in range(2)])
        mu = np.array([[1, 0], [0, 1]], float)
        hon = 1 - np.mean([(mu @ post)[:, k].max() for k in range(2)])
        print(f"E0 tight eps={e}: M_(2) loss = {loss:.4f}, honest loss = {hon:.4f} (both should equal eps)")


def psi_water(pi, lo, M, y, phi):
    # largest-level bisection for clip level
    lo_c, hi_c = 0.0, 1.0
    for _ in range(80):
        c = (lo_c + hi_c) / 2
        if (pi * np.clip(c, lo, M)).sum() < y:
            lo_c = c
        else:
            hi_c = c
    m = np.clip(hi_c, lo, M)
    return (pi * phi(m)).sum(), m


def e1(trials=400):
    worst = 0.0
    for _ in range(trials):
        A = rng.integers(2, 6)
        pi = rng.dirichlet(np.ones(A))
        M = rng.random(A)
        lo = M * rng.random(A) * (rng.random() < 0.5)
        pw = rng.uniform(1, 4)
        phi = lambda m, pw=pw: m ** pw / 1.0     # convex, nondecreasing, phi(1)-phi(0)=1
        y = rng.uniform((pi * lo).sum(), (pi * M).sum())
        v_w, m_w = psi_water(pi, lo, M, y, phi)
        best = np.inf
        for _ in range(5):
            x0 = lo + rng.random(A) * (M - lo)
            r = minimize(lambda m: (pi * phi(m)).sum(), x0, method="SLSQP",
                         bounds=list(zip(lo, M)),
                         constraints=[{"type": "eq", "fun": lambda m: (pi * m).sum() - y}],
                         options={"ftol": 1e-12, "maxiter": 500})
            if r.success and abs((pi * r.x).sum() - y) < 1e-7:
                best = min(best, r.fun)
        worst = max(worst, v_w - best)
    print(f"E1 water-fill minus SLSQP optimum, max over {trials}: {worst:.2e} (should be <= ~1e-8)")
    # honest counterexample
    pi = np.array([.5, .5]); mu = np.array([.9, 0.]); M = np.array([1., 1.]); tau = .5
    y = max((pi * mu).sum(), min(tau, (pi * M).sum()))
    _, m = psi_water(pi, mu, M, y, lambda m: m)
    print(f"E1 honest counterexample: water-fill {m.round(3)}, pointwise rule {np.maximum(mu, np.minimum(tau, M))}")


if __name__ == "__main__":
    e0_random()
    e0_tight()
    e1()
