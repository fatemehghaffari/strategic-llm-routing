#!/usr/bin/env python3
"""Item 3: randomized check of lem:cost-convert (a),(b) and of the Lambda placements in Prop (i),
with convex nondecreasing phi attaining (N) with equality (phi(1)-phi(0)=1), including the extreme
kink phi(m)=Lam*max(0, m-(1-1/Lam)) and phi(m)=m^p.  Also checks tightness: (b) is attained, so the
factor Lambda cannot be dropped.  Standard library only."""
import random, math
rng = random.Random(1)

def mk_phi():
    kind = rng.choice(['kink', 'pow', 'pl'])
    if kind == 'kink':
        Lam = rng.choice([1.0, 2.0, 5.0, 50.0])
        a = 1 - 1 / Lam
        return (lambda m: Lam * max(0.0, m - a)), Lam, f'kink{Lam}'
    if kind == 'pow':
        p = rng.choice([1.0, 1.5, 2.0, 7.0])
        return (lambda m: m ** p), p, f'pow{p}'
    # random convex piecewise-linear, range exactly 1
    k = rng.randint(2, 6)
    sl = sorted(rng.random() for _ in range(k))
    tot = sum(sl) / k
    sl = [s / tot for s in sl]           # average slope 1 -> range 1
    def phi(m, sl=sl, k=k):
        v, x = 0.0, 0.0
        for s in sl:
            step = min(1.0 / k, max(0.0, m - x)); v += s * step; x += 1.0 / k
        return v
    return phi, max(sl), 'pl'

worst = 0.0
for trial in range(200000):
    phi, Lam, name = mk_phi()
    theta = rng.random(); q = rng.randint(1, 30)
    ms = [rng.random() for _ in range(q)]
    wts = [rng.random() for _ in range(q)]            # measure pi with random weights
    Q = sum(wts); mean_mass = sum(w * m for w, m in zip(wts, ms))
    Delta = max(0.0, Q * theta - mean_mass)            # tightest Delta making the hypothesis hold
    lhs = sum(w * phi(m) for w, m in zip(wts, ms))
    rhs = Q * phi(theta) - Lam * Delta
    worst = min(worst, lhs - rhs)
print('min over trials of lhs-rhs in (b) (must be >= -1e-12):', worst)

# tightness: point mass at theta - Delta/Q in the steep region of the kink
Lam = 50.0; a = 1 - 1 / Lam; phi = lambda m: Lam * max(0.0, m - a)
theta, Q, Delta = 1.0, 10.0, 0.1
m = theta - Delta / Q
print('tightness (b): lhs', Q * phi(m), ' rhs', Q * phi(theta) - Lam * Delta)

# Prop (i) Stage-2 piece: saving of a deviator that under-delivers by b_n(q)/q per pull while
# staying inside the monitor band, kink cost: saving = Lam * b_n(q) exactly, matching Lambda(1+2b_n(q)).
n, K = 10**6, 2; ell = math.log(2 * K * n**5); q = 10**5; b = math.sqrt(q * ell / 2)
tau = 0.999
print('Stage-2 saving with kink Lam=50 at tau=0.999:', q * (phi(tau) - phi(tau - b / q)), ' Lambda*b_n(q)=', Lam * b)
