"""PROVER2: one local instance of CL-MESP keyed on a label, with true types hidden from the platform.

Everything is vectorised over R independent replications; strategies of the same experiment share
all draws (priorities, Stage-1 (X,U), per-round (X,U,zeta)) through a common seed, so utility
differences are coupled exactly as in the proof of (A).

Linear cost: per-selection utility 1 + mu_k(X) - m.
"""
import math
import numpy as np


def params(n, K):
    L = min(n // (2 * K), math.ceil(n ** (2 / 3) * math.log(math.e * n) ** (1 / 3)))
    ell = math.log(2 * n ** 4)
    s = math.sqrt(math.log(2 * K * n ** 4) / (2 * L))
    gam = min(0.5, math.sqrt(K * math.log(K) / n))
    eta = gam / K
    RK = 3 * math.sqrt(K * n * math.log(K)) + 2 * K * math.log(K)
    return dict(L=L, ell=ell, s=s, gam=gam, eta=eta, RK=RK)


def clip_level(pi, lo, M, y):
    """Largest level c (vector over reps) with sum_a pi(a) clip(c, lo(a), M(a)) = y; pi (A,) or (R,A)."""
    pi = np.atleast_2d(pi)
    y = np.asarray(y, float)
    a, b = np.zeros_like(y), np.ones_like(y)
    for _ in range(60):
        c = (a + b) / 2
        v = (pi * np.clip(c[:, None], lo[None, :], M[None, :])).sum(1)
        below = v <= y + 1e-12
        a = np.where(below, c, a)
        b = np.where(below, b, c)
    return a


class Agent:
    """Base: S*_N (water-fill with known posterior)."""
    def __init__(self, M, mu, honest, pi, name="S*_N"):
        self.M, self.mu, self.honest, self.pi, self.name = M, mu, honest, pi, name
        self.lo = mu if honest else np.zeros_like(M)

    def stage1(self, x):
        return self.M[x]

    def start_primary(self, tau, hist):
        Mbar = self.pi @ self.M
        lobar = self.pi @ self.lo
        y = np.maximum(lobar, np.minimum(tau, Mbar))
        self.c = clip_level(self.pi, self.lo, self.M, y)

    def primary(self, x, Z, r, tau, b):
        return np.clip(self.c, self.lo[x], self.M[x])

    def fallback(self, x):
        return self.M[x]


class Pointwise(Agent):
    def start_primary(self, tau, hist):
        self.tau = tau

    def primary(self, x, Z, r, tau, b):
        m = np.minimum(tau, self.M[x])
        return np.maximum(m, self.lo[x])


class Shade(Agent):
    def __init__(self, *a, delta=0.02, **k):
        super().__init__(*a, **k)
        self.delta = delta
        self.name = f"shade{delta}"

    def start_primary(self, tau, hist):
        Mbar = self.pi @ self.M
        lobar = self.pi @ self.lo
        y = np.maximum(lobar, np.minimum(tau, Mbar) - self.delta)
        self.c = clip_level(self.pi, self.lo, self.M, y)


class Rider(Agent):
    """Deliver lo while the next test is guaranteed to pass, else full capacity; fallback: fb_mode."""
    def __init__(self, *a, fb_mode="cap", margin=0.0, **k):
        super().__init__(*a, **k)
        self.fb_mode = fb_mode
        self.margin = margin
        self.name = f"rider-fb{fb_mode}-h{margin}"

    def primary(self, x, Z, r, tau, b):
        safe = Z >= (r + 1) * tau - b(r + 1) + self.margin
        return np.where(safe, self.lo[x], self.M[x])

    def fallback(self, x):
        return self.M[x] if self.fb_mode == "cap" else self.lo[x]


class AllLow(Agent):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.name = "all-low-postbid"

    def primary(self, x, Z, r, tau, b):
        return self.lo[x]

    def fallback(self, x):
        return self.lo[x]


class Underbid(Agent):
    """Stage 1: deliver the constant label-level midpoint (Mbar_i + Vbar_i)/2 via water-fill; then S*_N."""
    def __init__(self, *a, target=None, **k):
        super().__init__(*a, **k)
        self.target = target
        self.name = "underbid-stage1"
        c = clip_level(self.pi, self.lo, self.M, np.array([target]))[0]
        self.m1 = np.clip(c, self.lo, self.M)

    def stage1(self, x):
        return self.m1[x]


class DLearn(Agent):
    """Winner learns pihat from its own Stage-1 types; target max(lohat, min(tau+g, Mhat)), largest level."""
    def __init__(self, *a, g=0.0, **k):
        super().__init__(*a, **k)
        self.g = g
        self.name = f"D-learn(g={g:.3f})"

    def start_primary(self, tau, hist):
        pihat = hist  # (R, A) empirical type law of own Stage-1 pulls
        Mhat = pihat @ self.M
        lohat = pihat @ self.lo
        t = np.maximum(lohat, np.minimum(tau + self.g, Mhat))
        R = len(tau)
        c = np.empty(R)
        for j in range(R):  # small R
            c[j] = clip_level(pihat[j], self.lo, self.M, np.array([t[j]]))[0]
        c = np.where(t >= Mhat - 1e-12, 1.0, c)
        self.c = c


def run(agents, n, R, seed, types=None, pi=None, dev_index=None, monitor=True):
    """types: None -> i.i.d. from pi; else array (n,) deterministic path.
    Returns dict with utilities (R,K), switched (R,), winner (R,), tau (R,), revenue (R,)."""
    K = len(agents)
    if pi is None:
        pi = agents[0].pi  # the true posterior at the label (the agents' pi is the true one)
    P = params(n, K)
    L, s, gam, eta = P["L"], P["s"], P["gam"], P["eta"]
    bfun = lambda r: np.sqrt(r * P["ell"] / 2)
    rng = np.random.default_rng(seed)
    A = len(agents[0].M)
    prio = np.argsort(rng.random((R, K)), axis=1)  # prio rank
    rank = np.argsort(prio, axis=1)
    util = np.zeros((R, K))
    rev = np.zeros(R)
    T1 = K * L
    # Stage 1
    if types is None:
        X1 = rng.choice(A, size=(T1, R), p=pi)
    else:
        X1 = np.repeat(types[:T1, None], R, axis=1)
    U1 = rng.random((T1, R))
    bids = np.zeros((R, K))
    hist = np.zeros((K, R, A))
    for t in range(T1):
        k = t % K
        x = X1[t]
        m = agents[k].stage1(x)
        Y = U1[t] <= m
        bids[:, k] += Y
        util[:, k] += 1 + agents[k].mu[x] - m
        rev += Y
        hist[k, np.arange(R), x] += 1
    # winner: largest bid, ties by priority (higher rank wins)
    key = np.rint(bids) + rank / K  # bids are integer counts here, priority rank in [0,1) breaks ties
    W = np.argmax(key, axis=1)
    bids /= L
    sb = np.sort(bids, axis=1)
    tau = np.maximum(sb[:, -2] - s, 0.0)
    for k in range(K):
        agents[k].start_primary(tau, hist[k] / L)
    switched = np.zeros(R, bool)
    Z = np.zeros(R)
    r = np.zeros(R)
    logw = np.zeros((R, K))
    idx = np.arange(R)
    for t in range(T1, n):
        if types is None:
            x = rng.choice(A, size=R, p=pi)
        else:
            x = np.full(R, types[t])
        U = rng.random(R)
        zc = rng.random(R)
        w = np.exp(logw - logw.max(1, keepdims=True))
        p = (1 - gam) * w / w.sum(1, keepdims=True) + gam / K
        I_fb = (zc[:, None] > np.cumsum(p, 1)).sum(1)
        I_fb = np.minimum(I_fb, K - 1)
        I = np.where(switched, I_fb, W)
        m = np.zeros(R)
        for k in range(K):
            mk = I == k
            if not mk.any():
                continue
            prim = mk & ~switched
            fb = mk & switched
            if prim.any():
                m[prim] = agents[k].primary(x, Z, r, tau, bfun)[prim]
            if fb.any():
                m[fb] = agents[k].fallback(x)[fb]
        Y = U <= m
        mu_sel = np.array([agents[k].mu for k in range(K)])[I, x]
        util[idx, I] += 1 + mu_sel - m
        rev += Y
        prim = ~switched
        Z = Z + np.where(prim, Y, 0)
        r = r + prim
        newsw = prim & (Z < r * tau - bfun(r)) & monitor
        fbm = switched
        if fbm.any():
            pI = p[idx, I]
            logw[idx[fbm], I[fbm]] += eta * Y[fbm] / pI[fbm]
        switched = switched | newsw
    return dict(util=util, switched=switched, W=W, tau=tau, rev=rev, P=P)
