"""Horizon thresholds for CG-MESP, recomputed from the parameter definitions of FINAL.md Section 2.

Pure standard library (math only). Deterministic; no randomness. Written for CHECK.md Section 9.

For grid dimension m (m = D = Kd for per-agent contexts, m = d for one shared context) and K agents:
  g_n = ceil(n^{1/(m+3)}), h_n = 1/g_n, J_n = g_n^m, L_n = ceil(n^{2/(m+3)}), ell_n = log(2 K n^5),
  s_n = sqrt(ell_n/(2 L_n)), rho_n = sqrt(m) h_n log(e n), sigma_n = 3 s_n + rho_n,
and, with J standing for E[J'_n] (worst case min{J_n, n}):
  e_bid    = min{J L_n, n}
  e_stage1 = min{K J L_n, n}
  e_osc    = n rho_n
  e_mon    = J + 2 sqrt(J n ell_n / 2)
  e_fb     = 11 sqrt(2 K J n log K) + 2 K log K J log2(2(n+1))
  e_price  = n (4 s_n + (4/3) rho_n)
Bound (A) = e_bid + e_osc + e_mon + e_fb; slack (B) = e_stage1 + e_price;
slack (C) = e_stage1 + e_price + e_mon + e_fb. The O(n^{-2}) remainders are ignored (they are < 1e-6
at every threshold below). Each threshold is the smallest n, on a grid of log10 n with step 0.01, above
which the quantity stays below its trivial value (1 for sigma_n, n for the bounds) for the rest of the
scanned range; a coarse bisection is not used because of the ceilings.
"""
import math


def params(n, m, K):
    g = math.ceil(n ** (1.0 / (m + 3)) - 1e-12)
    h = 1.0 / g
    J = float(g) ** m
    L = math.ceil(n ** (2.0 / (m + 3)) - 1e-12)
    ell = math.log(2 * K) + 5 * math.log(n)
    s = math.sqrt(ell / (2 * L))
    rho = math.sqrt(m) * h * (1 + math.log(n))
    return g, h, J, L, ell, s, rho


def terms(n, m, K, Jmode="worst"):
    g, h, J, L, ell, s, rho = params(n, m, K)
    Jp = min(J, n) if Jmode == "worst" else 1.0
    e_bid = min(Jp * L, n)
    e_st1 = min(K * Jp * L, n)
    e_osc = n * rho
    e_mon = Jp + 2 * math.sqrt(Jp * n * ell / 2)
    e_fb = 11 * math.sqrt(2 * K * Jp * n * math.log(K)) + 2 * K * math.log(K) * Jp * math.log2(2 * (n + 1))
    e_price = n * (4 * s + (4.0 / 3) * rho)
    sigma = 3 * s + rho
    A = e_bid + e_osc + e_mon + e_fb
    B = e_st1 + e_price
    C = e_st1 + e_price + e_mon + e_fb
    return dict(sigma=sigma, A=A / n, B=B / n, C=C / n, J=J)


def threshold(m, K, key, Jmode="worst", lo=1.0, hi=45.0, step=0.01):
    xs = [lo + k * step for k in range(int((hi - lo) / step) + 1)]
    ok = [terms(10 ** x, m, K, Jmode)[key] < 1.0 for x in xs]
    # smallest x such that ok holds from x to the end of the range
    last_bad = None
    for x, o in zip(xs, ok):
        if not o:
            last_bad = x
    if last_bad is None:
        return lo
    if last_bad >= xs[-1]:
        return float("inf")
    return last_bad + step


def main():
    print("J_n <= n threshold n >= 2^{m(m+3)/3}:")
    for m in [1, 2, 3, 4, 6, 10]:
        print("  m=%2d  log10 threshold = %.2f" % (m, m * (m + 3) / 3 * math.log10(2)))
    for K in [2, 3, 5]:
        print("\nK = %d, worst-case path (E[J'_n] = min{J_n, n}); entries are log10 n" % K)
        print("  m   sigma<1   (A)<n   (B)<n   (C)<n")
        for m in [1, 2, 3, 4, 6, 10]:
            r = [threshold(m, K, k) for k in ("sigma", "A", "B", "C")]
            print("  %2d   %6.2f  %6.2f  %6.2f  %6.2f" % ((m,) + tuple(r)))
    print("\nK = 2, concentrated path (J'_n = 1); entries are log10 n")
    print("  m   sigma<1   (A)<n   (B)<n   (C)<n")
    for m in [1, 2, 3, 4, 6, 10]:
        r = [threshold(m, 2, k, Jmode="one") for k in ("sigma", "A", "B", "C")]
        print("  %2d   %6.2f  %6.2f  %6.2f  %6.2f" % ((m,) + tuple(r)))
    # spot values at n = 10^6.3 (the largest horizon run in the experiments) for m = 1, K = 2
    n = 10 ** 6.3
    t = terms(n, 1, 2)
    print("\nm=1, K=2, n=10^6.3: sigma=%.3f  A/n=%.3f  B/n=%.3f  C/n=%.3f" % (t["sigma"], t["A"], t["B"], t["C"]))


if __name__ == "__main__":
    main()
