import numpy as np, math

rng = np.random.default_rng(20260918)

# ---------- Part 1 check: single-pull-reactive mechanism on a Bernoulli instance ----------
# Instance: all agents honest, mu_i = M_i = m (so gap kappa = min(m, 1-m)).
# Mechanism: PURE-SP style.  price tau in (0,1); phi(y,tau)=1{y<tau}; exclusion irreversible,
# allocation = round robin over the active set; no reward when active set empty.
def part1(K=4, n=200000, m=0.5, tau=0.5, reps=4000):
    kappa = min(m, 1-m); rho = 1.0
    tot = np.zeros(reps); tenure = []
    for r in range(reps):
        active = list(range(K)); reward = 0.0; T = np.zeros(K)
        t = 0; idx = 0
        while t < n and active:
            i = active[idx % len(active)]
            y = rng.random() < m
            reward += m            # P(n) = E[sum m_{I_t,t}]
            T[i] += 1
            if (0 if y else 1):    # y==0 < tau  -> exclude
                active.remove(i)
                if active: idx = idx % len(active)
            else:
                idx += 1
            t += 1
        tot[r] = reward; tenure.append(T.copy())
    tenure = np.array(tenure)
    print("PART 1: K=%d n=%d m=%g tau=%g  kappa=%g rho=%g" % (K, n, m, tau, kappa, rho))
    print("  mean total platform reward P(n)      = %.4f" % tot.mean())
    print("  Theorem 1' bound (1-kappa)K/(kappa*rho) = %.4f" % ((1-kappa)*K/(kappa*rho)))
    print("  mean per-agent tenure E[T_h]         = %.4f" % tenure.mean())
    print("  Lemma 2 bound 1/(kappa*rho)          = %.4f" % (1.0/(kappa*rho)))
    print("  honest benchmark mu_H^* n            = %.1f" % (m*n))

part1()
part1(K=3, n=100000, m=0.8, tau=0.3, reps=4000)

# ---------- Part 1 check: k-window rule ----------
def part1_window(K=2, n=100000, m=0.5, k=3, rho=1.0, reps=4000):
    kappa = min(m, 1-m); tenure = []
    for r in range(reps):
        active = list(range(K)); T = np.zeros(K); hist = {i: [] for i in range(K)}
        t = 0; idx = 0
        while t < n and active:
            i = active[idx % len(active)]
            y = 1 if rng.random() < m else 0
            hist[i].append(y); T[i] += 1
            fire = False
            if len(hist[i]) % k == 0 and all(v == 0 for v in hist[i][-k:]):
                fire = rng.random() < rho
            if fire:
                active.remove(i)
                if active: idx = idx % len(active)
            else:
                idx += 1
            t += 1
        tenure.append(T.copy())
    tenure = np.array(tenure)
    print("PART 1 window: K=%d k=%d m=%g  E[T_h]=%.3f  Theorem 2 bound k(1+1/(rho kappa^k))=%.3f"
          % (K, k, m, tenure.mean(), k*(1+1/(rho*kappa**k))))

part1_window(k=1); part1_window(k=2); part1_window(k=3); part1_window(k=5)
