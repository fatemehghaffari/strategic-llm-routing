#!/usr/bin/env python3
"""Witness W1 (ADVERSARY_OPEN.md, item 1): CG-MESP, K=2, d=1, linear cost (Lambda=1).

Path rule (satisfies (A3) verbatim and the *distributional* exogeneity (X) of FINAL.md:
the law of the whole path is the same under every strategy profile), but the bulk of the
horizon is routed by Z := 1 - (Y_1 XOR b0), b0 := 1{Pi_{C0} ranks agent 1 first}.

  round 1                : x = 0.5          (cube Cmid, agent 1's Stage-1 pull; Cmid never awards)
  rounds 2 .. 2L+1       : x = h/2          (cube C0, full Stage 1)
  rounds 2L+2 .. 4L+1    : x = 1 - h/2      (cube C1, full Stage 1)
  rounds 4L+2 .. n       : x = h/2 if Z=0 else 1-h/2

Primitives constant (L_Lip = 0): agent 1 strategic, mu_1 = M_1 = 1; agent 2 honest,
mu_2 = M_2 = 1. Both bid exactly 1 at C0 and C1, so Pi decides each cube.
Deviation (in B^ctx, deterministic): target 0 at round 1, S* afterwards.

Coupling: same seeds U_t, same priorities Pi_C, same EXP3 coins xi_t (the manuscript's coupling).
Control run (--control): Z := 1 - b0 (the Y_1 clause deleted).
Everything else is the mechanism of app_contextual_private.tex, 'The mechanism' paragraph.
Standard library only; deterministic seeds.
"""
import math, random, sys

K = 2

def params(n):
    g = math.ceil(n ** 0.25)
    h = 1.0 / g
    L = math.ceil(n ** 0.5)
    ell = math.log(2 * K * n ** 5)
    s = math.sqrt(ell / (2 * L))
    rho = h * math.log(math.e * n)
    sigma = 3 * s + rho
    return dict(g=g, h=h, L=L, ell=ell, s=s, rho=rho, sigma=sigma)

MU = [1.0, 1.0]
M = [1.0, 1.0]
HONEST = [False, True]

def run(n, P, U, xi, perms, deviate, control):
    g, h, L, ell, sigma = P['g'], P['h'], P['L'], P['ell'], P['sigma']
    cubes = {}
    util1 = 0.0
    Y1 = None
    Zroute = None
    logK = math.log(K)
    for t in range(1, n + 1):
        # ---- context (depends only on the past: Y_1 and Pi_{C0}) ----
        if t == 1:
            x = 0.5
        elif t <= 2 * L + 1:
            x = h / 2
        elif t <= 4 * L + 1:
            x = 1 - h / 2
        else:
            if Zroute is None:
                c0 = cubes[int((h / 2) / h)]
                b0 = 1 if c0['pi'][0] == 0 else 0   # agent index 0 is agent 1
                Zroute = (1 - b0) if control else 1 - (Y1 ^ b0)
            x = h / 2 if Zroute == 0 else 1 - h / 2
        cid = min(int(x / h), g - 1)
        if cid not in cubes:
            cubes[cid] = dict(V=0, sums=[0] * K, pi=perms[cid], tau=None, W=None,
                              Z=0, r=0, sw=False, fbt=0, ep=-1, w=None)
        c = cubes[cid]
        c['V'] += 1
        V = c['V']
        # ---- selection and target ----
        if V <= K * L:
            j = (V - 1) % K
            m = M[j]
            if deviate and t == 1 and j == 0:
                m = 0.0
            phase = 1
        elif not c['sw']:
            j = c['W']
            m = max(MU[j], c['tau']) if HONEST[j] else min(c['tau'], M[j])
            phase = 2
        else:
            c['fbt'] += 1
            lt = c['fbt']
            k = int(math.floor(math.log2(lt)))
            if k != c['ep']:
                c['ep'] = k
                c['w'] = [1.0] * K
            gam = min(0.5, math.sqrt(K * logK / 2 ** k))
            eta = gam / K
            W = sum(c['w'])
            p = [(1 - gam) * wi / W + gam / K for wi in c['w']]
            acc, j = 0.0, K - 1
            for jj in range(K):
                acc += p[jj]
                if xi[t] <= acc:
                    j = jj
                    break
            m = M[j]
            phase = 3
        Y = 1 if U[t] <= m else 0
        if t == 1:
            Y1 = Y
        if j == 0:
            util1 += 1 + MU[0] - m
        # ---- state updates ----
        if phase == 1:
            c['sums'][j] += Y
            if V == K * L:
                bids = [sm / L for sm in c['sums']]
                top = max(bids)
                cands = [a for a in range(K) if bids[a] == top]
                # highest priority = earliest in the permutation
                c['W'] = min(cands, key=lambda a: c['pi'].index(a))
                srt = sorted(bids, reverse=True)
                c['tau'] = max(srt[1] - sigma, 0.0)
        elif phase == 2:
            c['r'] += 1
            c['Z'] += Y
            r = c['r']
            if c['Z'] < r * c['tau'] - math.sqrt(r * ell / 2):
                c['sw'] = True
        else:
            if Y:
                c['w'][j] *= math.exp(eta * Y / p[j])
    return util1, Zroute, Y1

def bound(n, P, EJ=3.0, Lam=1.0):
    L, ell, rho = P['L'], P['ell'], P['rho']
    e_bid = min(EJ * L, n)
    e_osc = n * rho
    e_mon = EJ + 2 * math.sqrt(EJ * n * ell / 2)
    e_fb = 11 * math.sqrt(2 * K * EJ * n * math.log(K)) + 2 * K * math.log(K) * EJ * math.log2(2 * (n + 1))
    return e_bid + Lam * (e_osc + e_mon + e_fb) + 4 * n ** -3 + 4 / K * n ** -2

def analytic_gain(n, P, control=False):
    L, sigma = P['L'], P['sigma']
    tau = max(1 - sigma, 0.0)
    bulk = n - 4 * L - 1
    if control:
        return 1.0
    return 1.0 + 0.5 * bulk * (2 - tau)

def main():
    n = int(float(sys.argv[1])) if len(sys.argv) > 1 else 200000
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    control = '--control' in sys.argv
    P = params(n)
    rng = random.Random(20260929 + n + (7 if control else 0))
    gains, zb, zd = [], [], []
    for rr in range(runs):
        U = [None] + [rng.random() for _ in range(n)]
        xi = [None] + [rng.random() for _ in range(n)]
        perms = {}
        for cid in range(P['g']):
            pm = list(range(K)); rng.shuffle(pm); perms[cid] = pm
        if '--stratify' in sys.argv:
            # Pi is uniform, so averaging over the 4 equally likely (Pi_C0, Pi_C1) is exact
            h = P['h']; c0 = int((h/2)/h); c1 = min(int((1-h/2)/h), P['g']-1)
            perms[c0] = [0, 1] if rr % 2 == 0 else [1, 0]
            perms[c1] = [0, 1] if (rr // 2) % 2 == 0 else [1, 0]
        ub, Zb, _ = run(n, P, U, xi, perms, False, control)
        ud, Zd, _ = run(n, P, U, xi, perms, True, control)
        gains.append(ud - ub); zb.append(Zb); zd.append(Zd)
    mg = sum(gains) / runs
    sd = math.sqrt(sum((x - mg) ** 2 for x in gains) / max(runs - 1, 1))
    print(f"n={n} runs={runs} control={control} L={P['L']} g={P['g']} sigma={P['sigma']:.4f} tau={max(1-P['sigma'],0):.4f}")
    print(f"  empirical P(Z=1): baseline {sum(zb)/runs:.3f}  deviation {sum(zd)/runs:.3f}   (law of path, should both be ~0.5)")
    print(f"  mean gain {mg:.1f} (+- {1.96*sd/math.sqrt(runs):.1f})  = {mg/n:.4f} n")
    print(f"  analytic expected gain {analytic_gain(n,P,control):.1f} = {analytic_gain(n,P,control)/n:.4f} n")
    print(f"  Prop (i) bound (Lambda=1, E J'=3) {bound(n,P):.1f} = {bound(n,P)/n:.4f} n")

if __name__ == '__main__':
    if '--table' in sys.argv:
        for e in [5.0, 5.5, 6.0, 6.5, 7.0, 8.0, 10.0, 12.0]:
            n = int(10 ** e); P = params(n)
            print(f"log10 n={e:5.1f}  gain/n={analytic_gain(n,P)/n:.4f}  bound/n={bound(n,P)/n:.4f}  sigma={P['sigma']:.3f}")
    else:
        main()
