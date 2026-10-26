"""Assemble Instance objects from the MEASURED capability functions."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mechanisms import Instance  # noqa: E402
from rb_common import OUT  # noqa: E402

# alpha families: mu_i(x) = alpha_i * M_i(x).  RouterBench says nothing about
# what a provider would deliver if it spent the minimum, so this is ASSUMED and
# every headline number is reported as a function of alpha.
ALPHAS = {"a0.00": 0.0, "a0.25": 0.25, "a0.50": 0.5, "a0.75": 0.75,
          "het": None}
HET_ALPHAS = (0.2, 0.5, 0.8)   # assigned by DESCENDING global mean capability


def alpha_vector(tag, K, global_mean):
    if tag != "het":
        return np.full(K, ALPHAS[tag])
    order = np.argsort(-global_mean)          # best first
    a = np.empty(K)
    for rank, i in enumerate(order):
        a[i] = HET_ALPHAS[rank % len(HET_ALPHAS)]
    return a


def finite_instance(models, families, alpha_tag, out=OUT, shot="5shot",
                    uniform_mass=False, rng_seed=0):
    cap = pd.read_csv(os.path.join(out, f"capabilities_finite_{shot}.csv"))
    cap = cap[cap["model"].isin(models) & cap["context"].isin(families)]
    Mtab = cap.pivot(index="context", columns="model", values="M").loc[families, models]
    masses = pd.read_csv(os.path.join(out, f"context_masses_{shot}.csv")).set_index("context")
    n_q = masses.loc[families, "n_queries"].values.astype(float)
    if uniform_mass:
        n_q = np.full(len(families), n_q.mean())
    p = n_q / n_q.sum()
    # one "query row" per context; arrivals are drawn with the empirical mass
    M = Mtab.values.astype(float)
    key = np.arange(len(families))
    gm = (M * p[:, None]).sum(axis=0)
    a = alpha_vector(alpha_tag, len(models), gm)
    honest = np.zeros(len(models), dtype=bool)
    honest[int(np.argmin(gm))] = True
    inst = Instance(M=M, mu=a[None, :] * M, key=key, honest=honest, names=list(models))
    return inst, p, gm, a


def continuous_instance(models, alpha_tag, n, d=2, k=200, out=OUT, rho_mode="paper"):
    order = pd.read_csv(os.path.join(out, "model_order.csv"))["model"].tolist()
    cols = [order.index(m) for m in models]
    U = np.load(os.path.join(out, f"contexts_d{d}.npy"))
    S = np.load(os.path.join(out, f"capsurface_d{d}_k{k}.npy"))[:, cols]
    b = int(np.ceil(n ** (1.0 / (d + 3))))
    h = 1.0 / b
    cellcoord = np.minimum((U * b).astype(int), b - 1)
    key = np.zeros(len(U), dtype=np.int64)
    for j in range(d):
        key = key * b + cellcoord[:, j]
    uniq, key = np.unique(key, return_inverse=True)
    gm = S.mean(axis=0)
    a = alpha_vector(alpha_tag, len(models), gm)
    honest = np.zeros(len(models), dtype=bool)
    honest[int(np.argmin(gm))] = True
    inst = Instance(M=S, mu=a[None, :] * S, key=key, honest=honest, names=list(models))
    # oscillation allowance
    rho_paper = float(np.sqrt(d) * h * np.log(np.e * n))
    df = pd.DataFrame(S)
    df["cell"] = key
    osc = df.groupby("cell").agg(lambda s: s.max() - s.min())
    rho_measured = float(np.nanpercentile(osc.values, 95))
    rho = rho_paper if rho_mode == "paper" else (rho_measured if rho_mode == "measured" else 0.0)
    meta = {"n_cells": len(uniq), "b": b, "h": h, "rho_paper": rho_paper,
            "rho_measured_p95": rho_measured, "rho_used": rho, "d": d, "k": k}
    return inst, gm, a, rho, meta


def top_masks(inst):
    """(n_queries, K) boolean: is agent i the unique pointwise best at this query?"""
    mx = inst.M.max(axis=1, keepdims=True)
    return (inst.M >= mx - 1e-12)


def cg_elicitation_length(n, d, K):
    """Region-solved elicitation length for the continuum mechanism.

    Section 4.4 says the elicitation length is re-solved for the many-region
    problem rather than inherited from the single-context one, but does not
    print the constant.  Balancing the elicitation cost K*J*L against the
    statistical loss n*sqrt(log n /(2L)) at J = n^{D/(D+3)} regions gives
    L = n^{2/(D+3)} (log(en))^{1/3}, whose total elicitation cost
    K*n^{(D+2)/(D+3)} reproduces the exponent the theorem states.
    """
    return int(max(1, np.ceil(n ** (2.0 / (d + 3)) * np.log(np.e * n) ** (1 / 3))))
