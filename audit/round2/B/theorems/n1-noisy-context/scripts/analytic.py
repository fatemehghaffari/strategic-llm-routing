"""Closed-form label-level quantities for the item-5 setup (uniform label noise).

For each subset and eps: posterior pi_b(a) = p(a) C(a,b) / sum_a' p(a') C(a',b);
mixture capability Mbar_j(b) = sum_a pi_b(a) M_j(a); label winner W_b, price proxy
tau_b = second largest Mbar(b) (the mechanism subtracts s on top); shortfall of the
POINTWISE S* winner, sum_a pi_b(a) (tau_b - M_W(a))_+; posterior error e_b = 1 - pi_b(b).
Benchmarks: true-type E M_(2)(X), label-level E Mbar_(2)(B).
"""
import os, sys
import numpy as np
sys.path.insert(0, "<repo>/audit/round2/A4/scripts")
from arrival_order_v2 import Q7, build_instance

SUBS = [l.strip().split("=") for l in open(
    "<repo>/audit/round2/A4/scripts/arrival_order_subsets_v2.txt") if l.strip()]


def conf(eps, Q):
    c = np.full((Q, Q), eps / (Q - 1)); np.fill_diagonal(c, 1 - eps); return c


def label_quantities(M, p, C):
    Q, K = M.shape
    joint = p[:, None] * C                      # (a, b)
    pb = joint.sum(0)
    pi = joint / pb[None, :]                    # pi[a, b]
    Mbar = pi.T @ M                             # (b, j)
    return pb, pi, Mbar


if __name__ == "__main__":
    print("subset eps  E[M2(X)]  E[Mbar2(B)]  max_b shortfall(pointwise S*)  labels w/ shortfall>0  sum_b P(b) e_b")
    for lab, mods in SUBS:
        inst, p = build_instance(mods.split("|"))
        M = inst.M; Q = M.shape[0]
        for eps in (0.0, 0.05, 0.1, 0.2):
            C = conf(eps, Q)
            pb, pi, Mbar = label_quantities(M, p, C)
            m2 = np.sort(M, 1)[:, -2]
            mb2 = np.sort(Mbar, 1)[:, -2]
            W = Mbar.argmax(1)
            short = np.array([np.sum(pi[:, b] * np.clip(mb2[b] - M[:, W[b]], 0, None)) for b in range(Q)])
            eb = 1 - np.diag(pi)
            print(f"{lab} {eps:.2f} {p @ m2:.4f} {pb @ mb2:.4f} {short.max():.4f} "
                  f"{[Q7[b] for b in range(Q) if short[b] > 1e-9]} {pb @ eb:.3f}")
