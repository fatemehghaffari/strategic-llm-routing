"""N1 scout: PL-MESP under label noise, candidate variants.

Copied from audit/round2/A4/scripts/extras_c.py (item 5, --item noisy) and reduced to the
PL-MESP arms. The existing scripts are imported, never edited.

Setup identical to item 5: v2 subsets, Mixtral-8x7B honest, mu = min(M, M_Mistral-7B),
Q7 types with RouterBench 5-shot masses, true type drawn i.i.d. from the masses, reordered
by `order` (iid / bursty), label = true type with prob 1-eps, else uniform over the others,
independently of everything. Quality follows the TRUE type; the mechanism keys on the LABEL.
Row index q = true*Q + label (as in extras_c.noisy_instance).

Arms (mechanism:profile):
  plmesp:pointwise   the paper's S*: primary winner delivers min(tau_b, M(true)) pointwise
                     (this is item 5's plmesp_star).
  plmesp:label       candidate D: label-level S*: primary winner water-fills so that its
                     mean over the posterior pi_b = law(true | label b) equals tau_b:
                     m(a) = clip(c, lo(a), M(a)), sum_a pi_b(a) m(a) = tau_b. Knows pi_b.
  plmesp:label_learn candidate D, implementable: pi_b replaced by the empirical law of the
                     true types the agent itself served in its own Stage-1 pulls at label b,
                     and the water level targets tau_b + gamma, gamma = sqrt((Q log 2 +
                     4 log n) / (2 N)), N = its Stage-1 pull count at b.
  tol:pointwise      candidate A: monitor boundary widened to Z_r < r (tau_b - kappa_b) - b(r),
                     kappa_b = e_b tau_b, e_b = 1 - pi_b(b) (known confusion and masses);
                     winner plays the pointwise S*.
  tol:label_tol      candidate A, strategic best response: water-fill to tau_b - kappa_b.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

A4 = "<repo>/audit/round2/A4/scripts"
sys.path.insert(0, A4)
from arrival_order import reorder  # noqa: E402
from arrival_order_v2 import Q7, build_instance  # noqa: E402
from extras_c import noisy_instance, confusion  # noqa: E402
from mechanisms import MechanismRun  # noqa: E402
from run_sim import draw_queries  # noqa: E402


def waterfill(pi, lo, M, level):
    """c with sum_a pi(a) clip(c, lo(a), M(a)) = level (clipped to feasibility)."""
    if level <= pi @ lo:
        return -1.0
    if level >= pi @ M:
        return 2.0
    a, b = 0.0, 1.0
    for _ in range(60):
        c = 0.5 * (a + b)
        if pi @ np.clip(c, lo, M) < level:
            a = c
        else:
            b = c
    return b


class LabelStrategy:
    def __init__(self, inst0, p, C, mode, n, kappa_frac=None):
        self.M0, self.mu0, self.honest = inst0.M, inst0.mu, inst0.honest
        self.Q, self.K = inst0.M.shape
        joint = p[:, None] * C
        self.pi = joint / joint.sum(0, keepdims=True)          # pi[a, b]
        self.mode, self.n = mode, n
        self.kappa_frac = kappa_frac
        self.cnt = np.zeros((self.K, self.Q, self.Q))            # agent, label, true
        self.cache = {}

    def lo(self, i):
        return self.mu0[:, i] if self.honest[i] else np.zeros(self.Q)

    def target(self, i, phase, q, price, state=None):
        a, b = divmod(int(q), self.Q)
        M = self.M0[a, i]
        if phase == "elicit":
            self.cnt[i, b, a] += 1
        if phase != "primary" or price is None:
            return M
        if self.mode == "pointwise":
            m = min(price, M)
            return max(self.mu0[a, i], m) if self.honest[i] else m
        key = (i, b, price)
        c = self.cache.get(key)
        if c is None:
            if self.mode == "label":
                pi, level = self.pi[:, b], price
            elif self.mode == "label_learn":
                N = self.cnt[i, b].sum()
                pi = self.cnt[i, b] / max(N, 1)
                gam = np.sqrt((self.Q * np.log(2) + 4 * np.log(self.n)) / (2 * max(N, 1)))
                level = price + gam
            elif self.mode == "label_tol":
                pi, level = self.pi[:, b], price * (1 - self.kappa_frac[b])
            else:
                raise ValueError(self.mode)
            c = waterfill(pi, self.lo(i), self.M0[:, i], level)
            self.cache[key] = c
        return float(np.clip(c, self.lo(i)[a], M))


class TolRun(MechanismRun):
    """Anytime monitor with a per-label tolerance kappa_b = e_b * tau_b."""

    def __init__(self, inst, n, seed, kappa_frac, **kw):
        super().__init__(inst, n, seed, **kw)
        self.kf = kappa_frac

    def _get(self, k):
        lo = super()._get(k)
        lo.kf = self.kf[k]
        return lo

    def _convict(self, lo, y):
        return lo.Z < lo.r * lo.tau * (1 - lo.kf) - self.boundary_mult * lo.b(lo.r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", required=True)
    ap.add_argument("--n", type=int, default=3000000)
    ap.add_argument("--seeds", default="0-9")
    ap.add_argument("--orders", default="iid")
    ap.add_argument("--eps", default="0.05,0.1,0.2")
    ap.add_argument("--arms", default="plmesp:pointwise,plmesp:label,plmesp:label_learn,tol:pointwise,tol:label_tol")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    label, models = a.subset.split("=")
    models = models.split("|")
    inst, p = build_instance(models)
    Q, K = inst.M.shape
    s0, s1 = map(int, a.seeds.split("-"))
    rows = []
    for eps in map(float, a.eps.split(",")):
        C = confusion(eps, Q)
        ninst, _ = noisy_instance(inst, p, C)
        joint = p[:, None] * C
        pi = joint / joint.sum(0, keepdims=True)
        ebar = 1 - np.diag(pi)
        pb = joint.sum(0)
        Mbar = pi.T @ inst.M
        bench_label = float(pb @ np.sort(Mbar, 1)[:, -2])
        bench_true = float(p @ np.sort(inst.M, 1)[:, -2])
        for order in a.orders.split(","):
            for arm in a.arms.split(","):
                mech, mode = arm.split(":")
                for s in range(s0, s1 + 1):
                    qs = reorder(draw_queries(inst, p, a.n, s), order, s, Q)
                    gen = np.random.default_rng(99991 + s)
                    u = gen.random(len(qs))
                    cum = np.cumsum(C, axis=1)
                    obs = np.minimum((u[:, None] > cum[qs]).sum(axis=1), Q - 1)
                    rq = (qs * Q + obs).astype(np.int64)
                    st = LabelStrategy(inst, p, C, mode, a.n, kappa_frac=ebar)
                    run = (TolRun(ninst, a.n, s, ebar) if mech == "tol" else MechanismRun(ninst, a.n, s))
                    r = run.run(st, rq)
                    rows.append(dict(subset=label, eps=eps, order=order, arm=arm, seed=s, n=a.n,
                                     revenue=r["revenue_per_round"],
                                     fired=int(r["convictions"] > 0),
                                     n_convictions=int(r["convictions"]),
                                     compliant_convictions=int(r["compliant_convictions"]),
                                     fallback_frac=r["phase_rounds"]["fallback"] / a.n,
                                     bench_label=bench_label, bench_true=bench_true,
                                     mislabel=float(np.mean(obs != qs))))
                    pd.DataFrame(rows).to_csv(a.out, index=False)
                print(f"done {label} eps={eps} {order} {arm}", flush=True)


if __name__ == "__main__":
    main()
