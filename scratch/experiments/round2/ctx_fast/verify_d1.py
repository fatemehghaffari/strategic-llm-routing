"""Verification of the COMMON-CONTEXT (d = 1) kernel against the unmodified slow reference.

The reference `run()` in `ctx_local/cg_struct.py` implements the earlier model, in which agent j
reads coordinate j of a K-dimensional context.  There is an exact embedding of the common-context
model into it: drive the reference on a DIAGONAL context path, `X_t = (x_t, x_t, ..., x_t)`.  Then
`M_j(X_t[j]) = M_j(x_t)` for every j, which is the common-context evaluation, and the reference's
cell key is the diagonal cell `(k_t, ..., k_t)`, in bijection with the one-dimensional cell `k_t`.
Every branch of the mechanism, the bidding schedule, the price, the monitor and the EXP3 fallback
are then the common-context mechanism, executed by code that was not modified.

The reference is not edited.  `np.random.default_rng` is intercepted by the same recorder used in
`verify.py`, with one addition: the first `.random((n, K))` call, which produces the context matrix,
is replayed with its first column broadcast across the K columns.  That changes the arrival law the
reference is driven with, which is a free choice, and not a single line of its code.

The grid side and the bidding block are passed explicitly as the common-context values
`g = ceil(n^{1/(d+3)})` and `L = ceil(n^{2/(d+3)})` with d = 1, and the oscillation multiplier is
set so that the reference's structural `rho = mult * L_lip * sqrt(K) * h` equals the mechanism's own
`rho_n = sqrt(d) h_n log(e n)`.  No other parameter is touched.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np

REF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ctx_local")
sys.path.insert(0, REF_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cgfast  # noqa: E402
from verify import Recorder, G_LAMBDAS  # noqa: E402


class DiagRecorder(Recorder):
    """As Recorder, but the context matrix is made diagonal: every agent sees the same context."""

    def __init__(self, rng, K):
        super().__init__(rng)
        self._K = K
        self._n_random = 0

    def random(self, *a, **k):
        v = self._rng.random(*a, **k)
        self._n_random += 1
        if self._n_random == 1 and isinstance(v, np.ndarray) and v.ndim == 2:
            v = np.repeat(v[:, :1], self._K, axis=1)
        self.big.append(v)
        return v


def run_reference_diag(name, n, g, Lbid, K, **kw):
    import cg_struct
    cg_struct.INST.setdefault("G", G_LAMBDAS)
    real = np.random.default_rng
    rec = {}

    def patched(seed):
        r = DiagRecorder(real(seed), K)
        rec["r"] = r
        return r

    np.random.default_rng = patched
    try:
        out = cg_struct.run(name, n, g, Lbid, **kw)
    finally:
        np.random.default_rng = real
    return out, rec["r"]


def compare(name, n, dev, kind, alpha_ride, seed, joint):
    K = cgfast.INST[name][0]
    L_lip = cgfast.INST[name][6]
    d = 1
    g = math.ceil(n ** (1.0 / (d + 3)))
    L = math.ceil(n ** (2.0 / (d + 3)))
    h = 1.0 / g
    rho_target = math.sqrt(d) * h * math.log(math.e * n)
    mult = rho_target / (L_lip * math.sqrt(K) * h)        # so the reference's rho equals rho_n
    rho_ref = mult * L_lip * math.sqrt(K) * h             # the exact double the reference will use
    ref, rr = run_reference_diag(name, n, g, L, K, dev=dev, kind=kind, alpha_ride=alpha_ride,
                                 seed=seed, osc_mult=mult, joint=joint)
    X = np.ascontiguousarray(rr.big[0][:, :1], dtype=np.float64).reshape(-1)   # the common context
    U = np.ascontiguousarray(rr.big[1], dtype=np.float64)
    perms = (np.array(rr.perms, dtype=np.int8).reshape(-1, K) if rr.perms
             else np.zeros((1, K), dtype=np.int8))
    fbu = np.array(rr.fbu, dtype=np.float64) if rr.fbu else np.zeros(1)
    fast = cgfast.run(name, n, tuned=True, d=d, dev=dev, kind=kind, alpha_ride=alpha_ride,
                      seed=seed, joint=joint, rho_override=rho_ref,
                      replay=dict(X=X, U=U, perms=perms, fbu=fbu))
    diffs = {}
    for f in ("J", "awarded", "switches", "false_switches", "viol_P2", "viol_P4", "stage1",
              "g", "L"):
        if int(ref[f]) != int(fast[f]):
            diffs[f] = (ref[f], fast[f])
    if float(ref["rev"]) != float(fast["rev"]):
        diffs["rev"] = (ref["rev"], fast["rev"])
    for j in range(K):
        if float(ref["util"][j]) != float(fast["util_naive"][j]):
            diffs[f"util[{j}]"] = (ref["util"][j], fast["util_naive"][j])
    for f, gf in (("bench_M2", "bench_M2_naive"), ("bench_honest", "bench_honest_naive")):
        if float(ref[f]) != float(fast[gf]):
            diffs[f] = (ref[f], fast[gf])
    for f in ("mean_tau", "s", "rho", "sigma", "h"):
        if abs(float(ref[f]) - float(fast[f])) > 0.0:
            diffs[f] = (ref[f], fast[f])
    tag = dict(inst=name, n=n, d=d, K=K, g=g, L=L, dev=dev, kind=kind, alpha=alpha_ride,
               seed=seed, joint=int(joint))
    return tag, diffs, ref, fast


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    specs = [(None, None, 0.0, False), (0, "underbid", 0.0, False), (0, "rider", 0.25, False),
             (0, "rider", 0.5, False), (0, "rider", 1.0, False), (0, "both", 0.5, False),
             (0, "crash", 0.0, False), (0, "sabotage", 0.0, True)]
    rows, nbad = [], 0
    # 5 x 10^6 is ABOVE the d = 1 price threshold: sigma_n = 0.739 there against a second capacity
    # of about 0.79, so the price is positive, the monitor can fire and the fallback runs.  Without
    # a horizon above the threshold this whole suite compares zeros on every interesting branch.
    for nm in ("C", "E", "D", "F", "G"):
        for n in (200000, 2000000, 5000000):
            for dev, kind, al, jt in specs:
                for sd in (0, 1):
                    tag, diffs, ref, fast = compare(nm, n, dev, kind, al, sd, jt)
                    ok = not diffs
                    nbad += (not ok)
                    rows.append(dict(tag=tag, ok=ok,
                                     diffs={k: [str(v[0]), str(v[1])] for k, v in diffs.items()},
                                     ref_switches=int(ref["switches"]),
                                     ref_awarded=int(ref["awarded"]),
                                     ref_viol_P2=int(ref["viol_P2"]),
                                     ref_viol_P4=int(ref["viol_P4"]),
                                     ref_mean_tau=float(ref["mean_tau"]),
                                     fast_stage3=int(fast["stage3"]),
                                     fast_tau_pos=int(fast["tau_pos"])))
                    if not ok:
                        print("FAIL " + json.dumps(tag) + " " + json.dumps(rows[-1]["diffs"]),
                              flush=True)
    tot = sum(r["tag"]["n"] for r in rows)
    print(f"{len(rows) - nbad}/{len(rows)} common-context cases bit-identical; "
          f"{tot:,} rounds; {sum(r['ref_switches'] for r in rows)} monitor firings; "
          f"{sum(r['fast_stage3'] for r in rows):,} Stage-3 rounds; "
          f"{sum(r['fast_tau_pos'] for r in rows)} positive-price cubes; "
          f"P2 violations {sum(r['ref_viol_P2'] for r in rows)}")
    if a.out:
        with open(a.out, "w") as f:
            json.dump(dict(n_cases=len(rows), n_fail=nbad, rows=rows), f, indent=1)
    sys.exit(1 if nbad else 0)


if __name__ == "__main__":
    main()
