import numpy as np, math
rng = np.random.default_rng(11)

# Grid-EXP3, D = K*d with K=2, d=1  ->  D=2
K, d = 2, 1; D = K*d
L = 0.6

def mu0(x): return 0.2 + L*x          # honest agent 0, L-Lipschitz, M_0 = mu_0 (no slack)
# agent 1 is strategic: M_1 = 1, mu_1 = 0, plays bait and switch on its OWN pull count

def R_K(H):  return 3*math.sqrt(K*H*math.log(K)) + 2*K*math.log(K)
def Rdbl(V):
    if V <= 0: return 0.0
    m = math.ceil(math.log2(V+1))
    return sum(R_K(2**k) for k in range(m))

def run(n, seed):
    r = np.random.default_rng(seed)
    bn = math.ceil(n**(1.0/(D+2))); hn = 1.0/bn; J = bn**D
    # deterministic adversarial context sequence (not i.i.d.)
    t = np.arange(n)
    x1 = ((t % 7) + 0.5)/7.0
    x2 = (((t//7) % 5) + 0.5)/5.0
    cell = np.minimum((x1/hn).astype(int), bn-1)*bn + np.minimum((x2/hn).astype(int), bn-1)
    gam = {}; eta = {}; w = {}; vis = np.zeros(J, dtype=int)
    pulls1 = 0; Ysum = 0.0; msum = 0.0
    switch_at = n//6                       # bait and switch after this many pulls of agent 1
    for s in range(n):
        c = cell[s]; vis[c] += 1; loc = vis[c]
        k = int(math.floor(math.log2(loc)))
        if loc == 2**k:                    # epoch start: fresh weights, gamma tuned to 2^k
            w[c] = np.ones(K)
            gam[c] = min(0.5, math.sqrt(K*math.log(K)/(2**k))); eta[c] = gam[c]/K
        q = w[c]/w[c].sum(); p = (1-gam[c])*q + gam[c]/K
        I = int(r.choice(K, p=p))
        if I == 0:
            m = mu0(x1[s])                 # honest, delivers its intrinsic mean
        else:
            pulls1 += 1
            m = 0.95 if pulls1 <= switch_at else 0.0     # behavioral bait and switch
        y = 1.0 if r.random() < m else 0.0
        Ysum += y; msum += m
        hat = np.zeros(K); hat[I] = y/p[I]
        w[c] = w[c]*np.exp(eta[c]*hat)
    bench = mu0(x1).sum()
    err = 2*L*math.sqrt(d)*n*hn + sum(Rdbl(v) for v in vis)
    return bench, msum, Ysum, err, hn, J, int((vis>0).sum())

for n in [2000, 8000, 32000]:
    B=[];P=[];E=[]
    for s in range(6):
        bench, msum, Ysum, err, hn, J, Jv = run(n, 1000+s)
        B.append(bench); P.append(msum); E.append(err)
    B=np.mean(B); P=np.mean(P); E=np.mean(E)
    print("n=%6d  h_n=%.4f J=%d visited=%d | benchmark=%.1f  P(n)=%.1f  slack=P-(bench-err)=%.1f  bound err=%.1f  rate n^{(D+1)/(D+2)}=%.1f"
          % (n, hn, J, Jv, B, P, P-(B-E), E, n**((D+1)/(D+2))))
    assert P >= B - E, "BOUND VIOLATED"
print("all horizons satisfy  P(n) >= sum_t b(x_t) - 2 L sqrt(d) n h_n - sum_C Rdbl(V_C)")
