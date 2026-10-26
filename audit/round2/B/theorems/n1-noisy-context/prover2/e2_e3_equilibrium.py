"""E2/E3: deviation gains and convictions at one label under i.i.d. label noise (hypothesis (N)).

E2: top agent 0 (unique top of the mixture), menu of deviations vs S*_N; conviction of S*_N vs the
    pointwise rule; D-learn baseline.
E3: non-top agent 1 with a small mixture gap (dbar <= 2 s_n): it can win; gain vs the bound.
Bound printed: l_i + Lambda (1 + b_n(N) + R_K(n)) (+ tiny), Lambda = 1 (linear cost).
"""
import math, sys, time
import numpy as np
from label_mesp_sim import (Agent, Pointwise, Shade, Rider, AllLow, Underbid, DLearn, run, params)

n = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
R = int(sys.argv[2]) if len(sys.argv) > 2 else 100
K = 3
pi = np.array([0.8, 0.1, 0.1])  # posterior at the label (label names type 0, e_b = 0.2)


def mk(Ms, mus, hon, dev_cls=None, dev_i=0, **kw):
    ags = []
    for k in range(K):
        if k == dev_i and dev_cls is not None:
            ags.append(dev_cls(Ms[k], mus[k], hon[k], pi, **kw))
        else:
            ags.append(Agent(Ms[k], mus[k], hon[k], pi))
    return ags


def experiment(title, Ms, mus, hon, dev_i, menu, seed):
    P = params(n, K)
    Mbar = np.array([pi @ M for M in Ms])
    Vbar = max(Mbar[j] for j in range(K) if j != dev_i)
    N = n - K * P["L"]
    bound = P["L"] + 1 + math.sqrt(N * P["ell"] / 2) + P["RK"]
    print(f"\n== {title}: n={n}, R={R}, L={P['L']}, s={P['s']:.4f}, Mbar={Mbar.round(4)}, "
          f"dbar_{dev_i}={Vbar - Mbar[dev_i]:.4f}, 2s={2*P['s']:.4f}")
    print(f"   bound l_i + 1 + b(N) + R_K(n) = {bound:.0f}   (b(N)={math.sqrt(N*P['ell']/2):.0f}, R_K={P['RK']:.0f})")
    base = run(mk(Ms, mus, hon), n, R, seed)
    ub = base["util"][:, dev_i]
    print(f"   baseline S*_N: u={ub.mean():.1f}, win-rate={np.mean(base['W']==dev_i):.2f}, "
          f"any-conviction={base['switched'].mean():.3f}, rev/n={base['rev'].mean()/n:.4f}, "
          f"E Mbar_(2)={np.sort(Mbar)[-2]:.4f}")
    for name, cls, kw in menu:
        t0 = time.time()
        out = run(mk(Ms, mus, hon, cls, dev_i, **kw), n, R, seed)
        d = out["util"][:, dev_i] - ub
        print(f"   {name:28s} gain={d.mean():9.1f} +- {1.96*d.std(ddof=1)/math.sqrt(R):7.1f}   "
              f"win={np.mean(out['W']==dev_i):.2f} conv={out['switched'].mean():.3f}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    # E2: agent 0 unique top of the mixture. Types: 0 (label's own), 1, 2.
    Ms = [np.array([0.9, 0.3, 0.6]), np.array([0.7, 0.8, 0.5]), np.array([0.5, 0.6, 0.9])]
    mus = [np.zeros(3), np.zeros(3), np.array([0.2, 0.2, 0.3])]
    hon = [False, False, True]
    Mbar = np.array([pi @ M for M in Ms])
    mid = (Mbar[0] + Mbar[1]) / 2
    P = params(n, K)
    A = 3
    g = math.sqrt((A * math.log(2) + math.log(K * n ** 4)) / (2 * P["L"]))
    menu = [
        ("pointwise S* (item-5 rule)", Pointwise, {}),
        ("shade 0.005", Shade, dict(delta=0.005)),
        ("shade 0.02", Shade, dict(delta=0.02)),
        ("shade 0.05", Shade, dict(delta=0.05)),
        ("rider h=0, fallback cap", Rider, dict(fb_mode="cap")),
        ("rider h=0, fallback low", Rider, dict(fb_mode="low")),
        ("rider h=5", Rider, dict(fb_mode="cap", margin=5.0)),
        ("rider h=15", Rider, dict(fb_mode="cap", margin=15.0)),
        ("all low post-bid", AllLow, {}),
        ("stage-1 underbid to mid", Underbid, dict(target=mid)),
        ("D-learn winner (baseline swap)", DLearn, dict(g=g)),
    ]
    experiment("E2 top agent 0", Ms, mus, hon, 0, menu, seed=11)
    # E3: agent 1 non-top with small gap.
    Ms3 = [np.array([0.9, 0.3, 0.6]), np.array([0.875, 0.5, 0.55]), np.array([0.5, 0.6, 0.9])]
    menu3 = [
        ("rider h=0, fallback low", Rider, dict(fb_mode="low")),
        ("rider h=15", Rider, dict(fb_mode="cap", margin=15.0)),
        ("all low post-bid", AllLow, {}),
        ("shade 0.02", Shade, dict(delta=0.02)),
        ("pointwise S* (item-5 rule)", Pointwise, {}),
    ]
    experiment("E3 non-top agent 1, small gap", Ms3, mus, hon, 1, menu3, seed=12)
