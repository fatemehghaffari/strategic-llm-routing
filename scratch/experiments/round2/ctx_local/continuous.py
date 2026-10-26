"""The continuous mechanism CG-MESP: the horizon at which each guarantee first says anything.

Source of every constant: audit/round2/B/theorems/f1-continuous-private/EXPLORER.md Section 3 (mechanism) and
Section 6 (Theorem 1 and its six error terms), with J'_n replaced throughout by the deterministic min{J_n, n},
as PROVER2.md Section 17.5 specifies. The bisection reproduces PROVER2.md Section 18; this module recomputes it
from the parameter definitions, extends it to parts (B) and (C) separately, to K and to the Lipschitz constant,
and adds the manuscript's public contextual error for the comparison PROVER2.md Section 18 point 2 asks for.

Nothing here is a simulation. Every number is the mechanism's own parameter or the theorem's own error term
evaluated exactly at the stated (n, D, K, L). Evidence category: EXACT COMPUTATION (of a formula).
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def params(n: float, D: int, K: int = 2, L_lip: float = 1.0) -> dict:
    """CG-MESP parameters and the six error terms of EXPLORER.md Section 6 at horizon n and dimension D."""
    g = math.ceil(n ** (1.0 / (D + 3)))
    h = 1.0 / g
    J = math.exp(D * math.log(g)) if g > 1 else 1.0
    Jp = min(J, n)                                     # min{J_n, n}, the deterministic replacement for J'_n
    Ln = math.ceil(n ** (2.0 / (D + 3)))
    ell = math.log(2 * K) + 5 * math.log(n)      # log(2 K n^5), written so large n does not overflow
    s = math.sqrt(ell / (2 * Ln))
    rho = math.sqrt(D) * h * math.log(math.e * n)
    sigma = 3 * s + rho
    e_bid = min(Jp * Ln, n)
    e_stage1 = min(K * Jp * Ln, n)
    e_osc = n * rho
    e_mon = Jp + 2 * math.sqrt(Jp * n * ell / 2)
    e_fb = 11 * math.sqrt(2 * K * Jp * n * math.log(K)) + 2 * K * math.log(K) * Jp * math.log2(2 * (n + 1))
    e_price = n * (4 * s + (4.0 / 3.0) * rho)
    e_rob = n * (4 * s + (5.0 / 3.0) * rho)
    return {"n": n, "D": D, "K": K, "g_n": g, "h_n": h, "J_n": J, "L_n": Ln, "ell_n": ell,
            "s_n": s, "rho_n": rho, "sigma_n": sigma,
            "e_bid": e_bid, "e_stage1": e_stage1, "e_osc": e_osc, "e_mon": e_mon, "e_fb": e_fb,
            "e_price": e_price, "e_rob": e_rob,
            "boundA": e_bid + e_osc + e_mon + e_fb,
            "slackB": e_stage1 + e_price,
            "slackC": e_stage1 + e_rob + e_mon + e_fb,
            "A2_satisfied": math.log(math.e * n) >= 3 * L_lip}


def public_En(n: float, D: int, d: int, L_lip: float = 1.0) -> float:
    """The manuscript's public contextual error, sections/contextual_samf_algorithm.tex line 9:
    E_n = L sqrt(d) n h_n + 4 sqrt(J_n n log n) + 3 min{J_n, n}, with h_n = (log(en)/n)^(1/(D+2))."""
    b = max(1, math.ceil((n / math.log(math.e * n)) ** (1.0 / (D + 2))))
    h = 1.0 / b
    J = math.exp(D * math.log(b)) if b > 1 else 1.0
    return L_lip * math.sqrt(d) * n * h + 4 * math.sqrt(J * n * math.log(max(n, 3))) + 3 * min(J, n)


def first_log10(D, K, L_lip, test, lo=1.0, hi=80.0, iters=300):
    """Smallest log10 n at which `test(n)` first holds, by bisection; returns nan if it never holds on [lo, hi]."""
    if not test(10 ** hi):
        return float("nan")
    if test(10 ** lo):
        return lo
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if test(10 ** mid):
            hi = mid
        else:
            lo = mid
    return hi


def thresholds(D: int, K: int = 2, L_lip: float = 1.0, d: int | None = None) -> dict:
    d = d if d is not None else max(1, D // K)
    P = lambda n: params(n, D, K, L_lip)
    out = {"D": D, "K": K, "d": d, "L_lip": L_lip,
           "log10_n_price_positive": first_log10(D, K, L_lip, lambda n: P(n)["sigma_n"] < 1.0),
           "log10_n_rho_below_1": first_log10(D, K, L_lip, lambda n: P(n)["rho_n"] < 1.0),
           "log10_n_A_below_n": first_log10(D, K, L_lip, lambda n: P(n)["boundA"] < n),
           "log10_n_A_below_2n": first_log10(D, K, L_lip, lambda n: P(n)["boundA"] < 2 * n),
           "log10_n_B_below_n": first_log10(D, K, L_lip, lambda n: P(n)["slackB"] < n),
           "log10_n_C_below_n": first_log10(D, K, L_lip, lambda n: P(n)["slackC"] < n),
           "log10_n_A2": math.log10(math.exp(3 * L_lip) / math.e) if L_lip > 0 else 0.0,
           "log10_n_public_En_below_n": first_log10(D, K, L_lip, lambda n: public_En(n, D, d, L_lip) < n)}
    # the binding threshold for "the mechanism says anything at all"
    out["log10_n_all_three"] = max(out["log10_n_price_positive"], out["log10_n_A_below_n"],
                                   out["log10_n_B_below_n"], out["log10_n_C_below_n"], out["log10_n_A2"])
    return out


def degeneracy_table(Ds=(1, 2, 3, 4, 6), ns=(10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8),
                     K: int = 2, L_lip: float = 1.0):
    """What the mechanism actually does at horizons anyone can run: sigma_n, and the price it would announce.

    The announced price is tau_C = (beta_(2),C - sigma_n)_+ and empirical bids never exceed 1, so sigma_n >= 1
    forces tau_C = 0 at every cube, whatever the instance. The Stage-2 winner then delivers min{0, M} = 0 if
    strategic, the monitor test 0 < r * 0 - b_n(r) never fires, and the mechanism collects nothing from a
    strategic winner outside its bidding blocks. This is a degeneracy of the mechanism at these horizons, not
    of the theorem, which is asymptotic.
    """
    rows = []
    for D in Ds:
        for n in ns:
            p = params(n, D, K, L_lip)
            rows.append({"D": D, "K": K, "n": int(n), "g_n": p["g_n"], "J_n": p["J_n"], "L_n": p["L_n"],
                         "s_n": p["s_n"], "rho_n": p["rho_n"], "sigma_n": p["sigma_n"],
                         "price_clipped_to_zero": int(p["sigma_n"] >= 1.0),
                         "K_J_L_over_n": min(1.0, p["e_stage1"] / n),
                         "boundA_over_n": p["boundA"] / n, "slackB_over_n": p["slackB"] / n,
                         "slackC_over_n": p["slackC"] / n})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for K in (2, 3):
        for L_lip in (0.5, 1.0, 2.0):
            for D in range(1, 13):
                rows.append(thresholds(D, K, L_lip))
    with (out / "continuous_thresholds.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  {out / 'continuous_thresholds.csv'} ({len(rows)} rows)")
    dg = degeneracy_table()
    with (out / "continuous_degeneracy.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(dg[0].keys()))
        w.writeheader()
        for r in dg:
            w.writerow(r)
    print(f"  {out / 'continuous_degeneracy.csv'} ({len(dg)} rows)")
    print("\nSmallest horizon at which each CG-MESP guarantee first says anything (K = 2, L = 1), log10 n:")
    print(f"{'D':>3} {'sigma<1':>9} {'(A)<n':>9} {'(B)<n':>9} {'(C)<n':>9} {'all':>9} {'public E_n<n':>13}")
    for D in range(1, 13):
        t = thresholds(D, 2, 1.0)
        print(f"{D:>3} {t['log10_n_price_positive']:>9.1f} {t['log10_n_A_below_n']:>9.1f} "
              f"{t['log10_n_B_below_n']:>9.1f} {t['log10_n_C_below_n']:>9.1f} {t['log10_n_all_three']:>9.1f} "
              f"{t['log10_n_public_En_below_n']:>13.1f}")


if __name__ == "__main__":
    main()
