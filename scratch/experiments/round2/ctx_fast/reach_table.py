"""The reach table of THRESHOLD_REPORT.md Section 7: for each dimension, the horizon at which the
mechanism's guarantees first say anything, and what it would cost to run it there.

Thresholds come from `ctx_local/continuous.py` (read only), by bisection on log10 n with K = 2 and
Lipschitz constant 1, which is how `PROVER2.md` Section 18 computes them.  Time uses throughput
measured on one machine as a function of the number of grid cells, interpolated in log J, not
extrapolated from the small-grid rate.  Memory is the two cell arrays of `cgmesp_v2.c`, 64 + 80
bytes per cell, before anything else.

Evidence category: EXACT COMPUTATION of a formula, plus a measured constant.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ctx_local"))
import continuous  # noqa: E402

# (number of grid cells, nanoseconds per round), measured with libcgmesp_v2.so on one cpu node
MEASURED = [(8.464e3, 20.5), (1.5876e4, 20.5), (3.28e5, 33.0), (8.04e5, 34.7),
            (1.4815e6, 40.0), (2.1467e6, 44.1), (6.25e6, 59.3)]


def ns_per_round(J):
    if J <= MEASURED[0][0]:
        return MEASURED[0][1]
    for (a, x), (b, y) in zip(MEASURED, MEASURED[1:]):
        if J <= b:
            return x + (y - x) * (math.log(J / a) / math.log(b / a))
    (a, x), (b, y) = MEASURED[-2], MEASURED[-1]
    return y + (y - x) * (math.log(J / b) / math.log(b / a))


def first_log10(D, K, test, lo=3.0, hi=45.0):
    if not test(10 ** hi):
        return float("nan")
    for _ in range(400):
        mid = 0.5 * (lo + hi)
        if test(10 ** mid):
            hi = mid
        else:
            lo = mid
    return hi


def main():
    print("| d | log10 n, price can be positive | log10 n, all three non-vacuous | "
          "grid cells at that horizon | cell arrays | single-core time | reached here |")
    print("|--:|--:|--:|--:|--:|--:|:--|")
    for D, note in ((1, "yes, and exceeded by 1.9 decades"), (2, "yes, and exceeded"),
                    (3, "launched"), (4, "no"), (5, "no"), (6, "no")):
        K = 2
        P = (lambda n: continuous.params(n, D, K, 1.0))
        t1 = first_log10(D, K, lambda n: P(n)["sigma_n"] < 1.0)
        ta = max(t1,
                 first_log10(D, K, lambda n: P(n)["boundA"] < n),
                 first_log10(D, K, lambda n: P(n)["slackB"] < n),
                 first_log10(D, K, lambda n: P(n)["slackC"] < n))
        n = 10 ** ta
        g = math.ceil(n ** (1.0 / (D + 3)))
        J = float(g) ** D
        byt = J * 144
        sec = n * ns_per_round(J) * 1e-9
        mem = (f"{byt / 1e6:.0f} MB" if byt < 1e9 else f"{byt / 1e9:.1f} GB" if byt < 1e12
               else f"{byt / 1e12:.1f} TB" if byt < 1e15 else f"{byt / 1e15:.2g} PB")
        tm = (f"{sec:.0f} s" if sec < 3600 else f"{sec / 3600:.1f} h" if sec < 2 * 86400
              else f"{sec / 86400:.1f} days" if sec < 3 * 3.15e7 else f"{sec / 3.15e7:.2g} core-years")
        print(f"| {D} | {t1:.1f} | {ta:.1f} | {J:.3g} | {mem} | {tm} | {note} |")


if __name__ == "__main__":
    main()
