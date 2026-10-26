import numpy as np, math
rng=np.random.default_rng(31337)
def trial(n, tau, reps=2000):
    N = n//2                      # N_n >= n/2
    beta = math.sqrt(math.log(2*n**4)/2)
    theta = 1 - math.sqrt(math.log(2*N))/beta
    r0 = math.ceil(beta**2/(4*tau**2))
    r = np.arange(1, N+1)
    B = beta*np.sqrt(r)
    dB = np.diff(np.concatenate([[0.0], B]))
    m = np.where(r <= r0, tau, tau - theta*dB)          # deviating targets
    assert m.min() >= -1e-12 and m.max() <= tau+1e-12, (m.min(), m.max())
    surv=0; saving = (tau - m).sum()
    for _ in range(reps):
        Y = (rng.random(N) < m).astype(float)
        Z = np.cumsum(Y)
        if np.all(Z >= r*tau - B): surv += 1
    # analytic saving from the theorem
    an = (beta - math.sqrt(math.log(2*N)))*(math.sqrt(N) - math.sqrt(r0))
    return N, beta, theta, r0, surv/reps, saving, an, 1/(4*N)
print(" n      N      beta   theta   r0   P(survive)  saving  thm-saving  thm-fail-bound")
for n in [10**4, 10**5, 10**6]:
    for tau in [0.3, 0.6]:
        N,beta,theta,r0,ps,sv,an,fb = trial(n, tau)
        print("%7d %7d %6.3f %6.4f %5d %10.4f %8.2f %10.2f %12.2e   tau=%.1f"%(n,N,beta,theta,r0,ps,sv,an,fb,tau))
# also: does the COMPLIANT baseline survive (false-alarm check)?
for n in [10**5]:
    N=n//2; beta=math.sqrt(math.log(2*n**4)/2); r=np.arange(1,N+1); B=beta*np.sqrt(r)
    bad=0
    for _ in range(2000):
        Y=(rng.random(N)<0.6).astype(float); Z=np.cumsum(Y)
        if np.any(Z < r*0.6 - B): bad+=1
    print("compliant false-alarm rate at n=1e5:", bad/2000, " manuscript bound (2n^3)^-1 =", 1/(2*n**3))
