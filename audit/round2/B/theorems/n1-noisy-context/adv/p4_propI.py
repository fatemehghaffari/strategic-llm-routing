"""ADVERSARY priority 4: the scout's Prop. I corollary against the two counterexample mechanisms
(PROVER1 Sec. 17 item 9; PROVER2 Part 5 item 1), and the identity G + P = D of PROVER1.
Everything coupled on common label draws V and seeds U across worlds and strategies.
"""
import sys
import numpy as np

n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
R = int(sys.argv[2]) if len(sys.argv) > 2 else 200
eps = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
h = n // 2
rng = np.random.default_rng(1)
V = rng.random((n, R)); U = rng.random((n, R))


def sim_mech1(world, wstrat):
    """PROVER1 instance. types a=0,c=1,d=2; labels a=0,c=1. W: M=(1,0,0); others 1/2, type-blind.
    world 'P1': a then c (label a w.p. eps in 2nd half); 'P2': a then (a w.p. eps else d), label = class.
    Mechanism: label a -> W; label c (2nd half) -> W iff W's 2nd-half label-a reward rate >= 1/4 (W if none yet).
    wstrat(t, x, label) -> target. Returns utility of W, N^II_W, D (W's targets at 2nd-half label-a rounds)."""
    MW = np.array([1.0, 0.0, 0.0])
    uW = np.zeros(R); NII = np.zeros(R); D = np.zeros(R)
    ya = np.zeros(R); na = np.zeros(R)
    for t in range(n):
        if t < h:
            x = np.zeros(R, int); lab = np.zeros(R, int)
        else:
            isa = V[t] <= eps
            lab = np.where(isa, 0, 1)
            x = np.where(isa, 0, 2) if world == 'P2' else np.full(R, 1)
        rate_ok = np.where(na > 0, ya / np.maximum(na, 1) >= 0.25, True)
        selW = (lab == 0) | ((t >= h) & rate_ok)
        m = np.minimum(wstrat(t, x, lab), MW[x])
        Y = U[t] <= m
        uW += np.where(selW, 1 - m, 0.0)
        if t >= h:
            NII += selW
            D += np.where(selW & (lab == 0), m, 0.0)
            upd = selW & (lab == 0)
            ya += np.where(upd, Y, 0); na += upd
    return uW, NII, D


coop = lambda t, x, lab: np.where(lab == 0, 0.5, 1.0)          # min(1/2, M) at label a, capacity at label c
shade_tilde = lambda t, x, lab: np.where(t < h, coop(t, x, lab), 0.0)  # what coop does on P1 types: 0 in 2nd half
u1, N1, _ = sim_mech1('P1', coop)
u2s, N2s, _ = sim_mech1('P2', shade_tilde)
u2c, N2c, D2c = sim_mech1('P2', coop)
G = (u2s - u2c).mean(); P = (N2c - N1).mean(); D = D2c.mean()
print(f"[mech1, PROVER1 instance] n={n} eps={eps} R={R}")
print(f"  pathwise (P1,coop)==(P2,shade~): {np.array_equal(u1, u2s)}")
print(f"  alpha (withheld 2nd-half label-a share on P1, coop) = 0 by construction")
print(f"  scout's claimed lower bound on the shading gain: (1/2-alpha) eps n/2 = {0.5*eps*n/2:.0f}")
print(f"  measured G = u(P2,shade) - u(P2,'1/2 throughout') = {G:.0f}  (analytic eps n/4 - (1-eps) n/2 = {eps*n/4-(1-eps)*n/2:.0f})")
print(f"  identity: G + P = {G+P:.1f},  D = {D:.1f}  (P={P:.0f})")
# method rule: delete the cross-label clause (label c never goes to W in 2nd half)
def sim_mech1_ctrl(world, wstrat):
    MW = np.array([1.0, 0.0, 0.0]); uW = np.zeros(R)
    for t in range(n):
        if t < h:
            x = np.zeros(R, int); lab = np.zeros(R, int)
        else:
            isa = V[t] <= eps; lab = np.where(isa, 0, 1)
            x = np.where(isa, 0, 2) if world == 'P2' else np.full(R, 1)
        selW = lab == 0
        m = np.minimum(wstrat(t, x, lab), MW[x]); uW += np.where(selW, 1 - m, 0.0)
    return uW
Gc = (sim_mech1_ctrl('P2', shade_tilde) - sim_mech1_ctrl('P2', coop)).mean()
print(f"  CONTROL (cross-label punishment clause deleted): G = {Gc:.0f}  (scout bound {0.5*eps*n/2:.0f} now holds)")


def sim_mech2(world, wstrat, p=0.5):
    """PROVER2 instance. types a=0,c=1,d=2; labels alpha=0,gamma=1. W: M=(1,1,0); others (p,1,1).
    P1: a then d; P2: a then c; 2nd half label alpha w.p. eps else gamma.
    Mechanism: alpha -> W; gamma -> W iff W's last alpha reward was 1."""
    MW = np.array([1.0, 1.0, 0.0]); uW = np.zeros(R); last = np.ones(R, bool)
    nalpha2 = np.zeros(R)
    for t in range(n):
        if t < h:
            x = np.zeros(R, int); lab = np.zeros(R, int)
        else:
            lab = np.where(V[t] <= eps, 0, 1); x = np.full(R, 2 if world == 'P1' else 1)
        selW = (lab == 0) | last
        m = np.minimum(wstrat(t, x, lab), MW[x]); Y = U[t] <= m
        uW += np.where(selW, 1 - m, 0.0)
        last = np.where(lab == 0, Y, last)
        if t >= h: nalpha2 += (lab == 0)
    return uW, nalpha2.mean()

p = 0.5
coopC = lambda t, x, lab: np.where(lab == 0, p, 1.0)                     # PROVER2's cooperative comparator
half = lambda t, x, lab: np.full(x.shape, 0.5)                            # scout's "deliver 1/2 throughout"
shadeS = lambda t, x, lab: np.where(x == 0, p, 0.0)                      # p at type a, 0 at type c
uS, E2 = sim_mech2('P2', shadeS); uC, _ = sim_mech2('P2', coopC); uH, _ = sim_mech2('P2', half)
uP1C, _ = sim_mech2('P1', coopC)
print(f"\n[mech2, PROVER2 instance] p={p}, E_2 = {E2:.0f}, alpha_w = 0 (alpha always to W)")
print(f"  pathwise (P1,coop)==(P2,shade): {np.array_equal(uP1C, uS)}")
print(f"  gain vs PROVER2 cooperative comparator = {(uS-uC).mean():.0f}  >= (p-alpha_w) E_2 = {p*E2:.0f}")
print(f"  gain vs scout's '1/2 throughout'      = {(uS-uH).mean():.0f}  (scout's bound (1/2-alpha)E_2 = {0.5*E2:.0f})")
