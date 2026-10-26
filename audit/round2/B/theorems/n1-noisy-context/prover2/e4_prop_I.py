"""E4: Proposition I on the label-alpha local instance of CL-MESP (label-gamma instance omitted: by label
locality it does not affect label alpha).  Types: a=0, c=1, d=2.  W = agent 0: M_W = (1, 1, 0); agents 1,2:
M = (p, 1, 1), all mu = 0.  Label-alpha visit sequence: n1 visits of type a, then m2 = eps*n_mid visits of type
d (P1) or c (P2), then n3 visits of type a.
Strategies of W: coop = pointwise min(tau, M_W(x)) as winner, capacity otherwise; shade = coop except 0 at c.
Checks: (a) (P1, coop) and (P2, shade) give identical outcomes pathwise; (b) PL-MESP convicts coop W on P1
and W then loses the final a-block; (c) on P2 shading vs coop; (d) same with the monitor switched off.
"""
import sys
import numpy as np
from label_mesp_sim import Agent, Pointwise, run

R = int(sys.argv[1]) if len(sys.argv) > 1 else 50
p = 0.5
MW = np.array([1.0, 1.0, 0.0]); MO = np.array([p, 1.0, 1.0]); z = np.zeros(3)
pi_dummy = np.array([1.0, 0.0, 0.0])


class Shade(Pointwise):
    def primary(self, x, Z, r, tau, b):
        return np.where(x == 1, 0.0, super().primary(x, Z, r, tau, b))

    def fallback(self, x):
        return np.where(x == 1, 0.0, self.M[x])


def agents(Wcls):
    return [Wcls(MW, z, False, pi_dummy), Pointwise(MO, z, False, pi_dummy), Pointwise(MO, z, False, pi_dummy)]


for (n1, n_mid, n3, eps) in [(20000, 20000, 0, 0.1), (20000, 20000, 20000, 0.1), (20000, 20000, 20000, 0.2)]:
    m2 = int(eps * n_mid)
    P1 = np.array([0] * n1 + [2] * m2 + [0] * n3)
    P2 = np.array([0] * n1 + [1] * m2 + [0] * n3)
    n = len(P1)
    print(f"\n== blocks a:{n1}, mid:{m2} (eps={eps}), a:{n3}; label-alpha visits n={n}, R={R}")
    for mon in [True, False]:
        o1 = run(agents(Pointwise), n, R, 7, types=P1, monitor=mon)
        o2s = run(agents(Shade), n, R, 7, types=P2, monitor=mon)
        o2c = run(agents(Pointwise), n, R, 7, types=P2, monitor=mon)
        same = np.array_equal(o1["util"], o2s["util"]) and np.array_equal(o1["rev"], o2s["rev"])
        gain = o2s["util"][:, 0] - o2c["util"][:, 0]
        print(f"  monitor={mon}: (P1,coop)==(P2,shade) pathwise: {same}; W wins {np.mean(o1['W']==0):.2f}; "
              f"conviction on P1 {o1['switched'].mean():.2f}, on P2-coop {o2c['switched'].mean():.2f}")
        print(f"     u_W(P1,coop)={o1['util'][:,0].mean():.0f}  u_W(P2,coop)={o2c['util'][:,0].mean():.0f}  "
              f"shading gain on P2 = {gain.mean():.0f} +- {1.96*gain.std(ddof=1)/np.sqrt(R):.0f}  "
              f"(p*m2 = {p*m2:.0f})")
