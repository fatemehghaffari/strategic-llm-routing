"""UB1 diagnostic: does the 'lose on purpose, then pump the mean' deviation gain linearly under LB1's ACM?
K=2, linear cost. Agent 1 strategic (deviator), agent 2 honest at S*. Coupled agent-local seeds.
Baseline: agent 1 delivers M1 in Phase E, tau in Phase P. Deviation: agent 1 delivers 0 until agent 2 is
certified (or until pull index L otherwise), then delivers M1 for its remaining Phase-E pulls; as the loser
it delivers tau' in Phase R. Phase-R/P monitors as in sim_lb1.py; false convictions ignored here
(probability <= n^-3) except that we report whether any happened."""
import sys, math, numpy as np
def run(n, mu1, M1, M2, nrep, seed=7, cstar=0.75):
    L = n // 4; ell = math.log(2 * n**4); s = math.sqrt(ell / (2 * L))
    rng = np.random.default_rng(seed)
    U1 = rng.random((nrep, n)); U2 = rng.random((nrep, n))
    t = np.arange(1, L + 1); st = np.sqrt(ell / (2 * t))
    # agent 2 (honest, S*): delivers M2 on all L elicitation pulls
    Y2 = (U2[:, :L] <= M2).astype(np.int64); C2 = np.cumsum(Y2, 1); m2 = C2 / t
    beta2 = C2[:, -1] / L; tau2 = np.maximum(beta2 - s, 0); R2 = np.floor(beta2 * L / (1 - beta2)).astype(int)
    # ---- baseline: agent 1 delivers M1
    Y1 = (U1[:, :L] <= M1).astype(np.int64); C1 = np.cumsum(Y1, 1); m1 = C1 / t
    cert1 = (m1 - st) > (m2 + st); any1 = cert1.any(1)
    Tc = np.where(any1, cert1.argmax(1) + 1, L)
    win_base = any1 | ((~any1) & (C1[:, -1] >= C2[:, -1]))   # ties -> agent 1 (coupled coin ignored)
    # winner utility: Tc pulls at M1, then n - L - R2 - Tc pulls at tau2 (no false switch assumed)
    u_base = Tc * (1 + mu1 - M1) + (n - L - R2 - Tc) * (1 + mu1 - tau2)
    # ---- deviation: deliver 0 until agent 2 certified, then M1
    # agent 2 is certified at first t with m2 - st > m1' + st where m1' = 0 while delivering 0
    cert2 = (m2 - st) > (0 + st); any2 = cert2.any(1)
    Tc2 = np.where(any2, cert2.argmax(1) + 1, L)
    # deviator's Phase-E targets: 0 for first Tc2 pulls, M1 after
    # post-certification target chosen so that the final L-pull mean is about cstar (capped at M1)
    cpost = np.minimum(M1, cstar * L / np.maximum(L - Tc2, 1))
    tgt = np.where(np.arange(L)[None, :] < Tc2[:, None], 0.0, cpost[:, None])
    Y1d = (U1[:, :L] <= tgt).astype(np.int64); beta1d = Y1d.sum(1) / L
    cost_E = tgt.sum(1)                      # linear cost: sum of targets
    tau1d = np.maximum(beta1d - s, 0); R1d = np.floor(beta1d * L / (1 - beta1d)).astype(int)
    R1d = np.minimum(R1d, n - L - Tc2)
    u_dev = L * (1 + mu1) - cost_E + R1d * (1 + mu1 - tau1d)
    # check the deviation actually loses on every replicate (agent 2 certified)
    return dict(n=n, L=L, Tc_base=Tc.mean(), win_base=win_base.mean(), Tc2=Tc2.mean(), lost=any2.mean(),
                beta1d=beta1d.mean(), R1d=R1d.mean(), R2=R2.mean(),
                u_base=u_base.mean(), u_dev=u_dev.mean(), gain=(u_dev - u_base).mean(),
                gain_se=(u_dev - u_base).std(ddof=1) / math.sqrt(nrep),
                pred=n * (M2 - 0.5 + mu1 / (4 * (1 - M2))) if M1 >= 0.75 else float('nan'))
if __name__ == '__main__':
    for (mu1, M1, M2) in [(0.2, 0.9, 0.45), (0.0, 0.9, 0.45), (0.1, 0.9, 0.5)]:
      for cstar in [0.6, 0.7, 0.75, 0.8]:
        for n in [10000, 31623, 100000]:
            r = run(n, mu1, M1, M2, nrep=50, cstar=cstar)
            print(f"c*={cstar} ", end='')
            print(f"mu1={mu1} M1={M1} M2={M2} n={n:6d} Tc*={r['Tc_base']:.0f} lost={r['lost']:.2f} Tc2={r['Tc2']:.0f} "
                  f"beta'={r['beta1d']:.3f} R'={r['R1d']:.0f} R2={r['R2']:.0f} u_base={r['u_base']:.0f} u_dev={r['u_dev']:.0f} "
                  f"gain={r['gain']:.0f} (se {r['gain_se']:.0f}) gain/n={r['gain']/n:.4f} pred/n={r['pred']/n:.4f}", flush=True)
