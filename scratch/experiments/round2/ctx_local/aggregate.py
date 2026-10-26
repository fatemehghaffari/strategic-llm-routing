"""Aggregate the exact PL-MESP cells and the contextual ladder into the summary CSVs the report quotes.

Outputs (all under the scratchpad, never in the repository):
  exact_grid.csv      one row per (family, Q, n): certified interval, theorem terms, diagnostics
  exact_profiles.csv  one row per (family, Q, n, profile)
  ladder.csv          one row per (family, Q, n, rung, behaviour): paired means and 95 percent t intervals
  regime.csv          the analytic (n, Q) region: Stage-1 completion, monitor activity, bound below trivial
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

R2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R2))
from common.design import design as make_design, R_K  # noqa: E402
from common.stats import t_interval  # noqa: E402
from ctx_local.plmesp_exact import theorem_constant  # noqa: E402


def monitor_first_binds(n: int, tau: float) -> float:
    """Smallest local primary index r at which the monitor test r tau - b_n(r) > 0 can fire at all.

    b_n(r) = sqrt(r log(2 n^4) / 2), so r tau > b_n(r) iff r > log(2 n^4) / (2 tau^2). Below that index the
    monitor cannot convict any winner however little it delivers, so a profile with N_z at or below this value
    carries an inert monitor. Returns infinity when the announced price is zero.
    """
    return math.inf if tau <= 0 else math.log(2 * n ** 4) / (2 * tau ** 2)


def load_exact(resdir: Path):
    rows, prows = [], []
    for f in sorted(resdir.glob("exact_*.json")):
        if ".FAILED." in f.name:
            continue
        r = json.loads(f.read_text())
        n, K, Q = r["n"], r["K"], r["Q"]
        d = make_design(n, K)
        tc = r["theorem"]
        taus, rmins, binding = [], [], 0
        for p in r["profiles"]:
            M2 = sorted(p["M"])[-2]
            tau = max(0.0, M2 - d.s)
            rmin = monitor_first_binds(n, tau)
            taus.append(tau)
            rmins.append(rmin)
            binding += int((not p["truncated"]) and p["N_z"] > rmin)
            prows.append({"family": r["family"], "Q": Q, "n": n, "K": K, "z": p["z"], "V_z": p["V_z"],
                          "N_z": p["N_z"], "truncated": int(p["truncated"]),
                          "focal_is_top": int(p["focal_is_top"]), "delta": p["delta"],
                          "M": ";".join(f"{x:g}" for x in p["M"]),
                          "tau_star": tau, "monitor_first_binds_at_r": rmin,
                          "monitor_active": int((not p["truncated"]) and p["N_z"] > rmin),
                          "exploit_LB": p["exploit_LB"], "exploit_UB": p["exploit_UB"],
                          "base_LB": p["base_LB"], "base_UB": p["base_UB"],
                          "revenue_LB": p["revenue_LB"], "revenue_UB": p["revenue_UB"]})
        # Theorem (B) and (C) error terms of PROVER2.md Section 4.2, with PROVER1's calibration and caps:
        #   (B) slack = min{Q K L_n, n} + 2 n s_n + Q R_K(n) + n^{-3}
        #   (C) slack = (B) slack + e_mon
        e_stage1 = min(Q * K * d.L, n)
        e_price = 2.0 * n * d.s
        slackB = e_stage1 + e_price + tc["e_fb"] + n ** -3
        slackC = slackB + tc["e_mon"] + n ** -3
        max_stage1_gain = sum((0 if p["truncated"] else d.L) * (p["M"][r["focal"]] -
                              (p["mu"][r["focal"]] if r["focal"] in r["honest"] else 0.0))
                              for p in r["profiles"])
        trunc_gain = sum(p["exploit_LB"] for p in r["profiles"] if p["truncated"])
        # Proposition 6.1 of PROVER2.md: shading the Stage-1 target to m' = (M_i + V_i)/2 at every profile at
        # which i is the UNIQUE top agent gains exactly l_z (M_i - m') = l_z (M_i - V_i)/2 there and nothing
        # elsewhere. This is the hand-picked deviation the tightness proposition exhibits.
        prop61 = 0.0
        for p in r["profiles"]:
            if p["truncated"] or not p["focal_is_top"]:
                continue
            Mi = p["M"][r["focal"]]
            Vi = max(m for j, m in enumerate(p["M"]) if j != r["focal"])
            if Mi > Vi + 1e-12:                      # uniquely top at z
                lo_i = p["mu"][r["focal"]] if r["focal"] in r["honest"] else 0.0
                prop61 += d.L * (Mi - max(0.5 * (Mi + Vi), lo_i))
        rows.append({
            "family": r["family"], "Q": Q, "n": n, "K": K, "focal": r["focal"],
            "L_n": d.L, "KL_n": K * d.L, "s_n": d.s, "b_n_of_n": float(d.b(n)),
            "stage1_share_of_horizon": min(1.0, Q * K * d.L / n),
            "n_truncated_profiles": r["n_truncated_profiles"], "n_monitor_active_profiles": binding,
            "N_z_min": min(p["N_z"] for p in r["profiles"]), "N_z_max": max(p["N_z"] for p in r["profiles"]),
            "monitor_first_binds_at_r": min(rmins),
            "exploit_LB": r["exploit_LB"], "exploit_UB": r["exploit_UB"],
            "exploit_LB_per_round": r["exploit_LB_per_round"], "exploit_UB_per_round": r["exploit_UB_per_round"],
            "interval_width": r["exploit_UB"] - r["exploit_LB"],
            "base_LB": r["base_LB"], "base_UB": r["base_UB"],
            "bidding_only_gain": max_stage1_gain, "prop61_gain": prop61, "truncated_profile_gain": trunc_gain,
            "revenue_LB_per_round": r["revenue_LB_per_round"], "revenue_UB_per_round": r["revenue_UB_per_round"],
            "benchmark_M2_per_round": r["benchmark_M2_per_round"],
            "benchmark_honest_per_round": r["benchmark_honest_per_round"],
            "revenue_deficit_LB_per_round": r["revenue_deficit_LB"] / r["n"],
            "revenue_deficit_UB_per_round": r["revenue_deficit_UB"] / r["n"],
            "revenue_bound_B_slack": slackB, "revenue_bound_B_slack_per_round": slackB / n,
            "B_slack_below_n": int(slackB < n),
            "honest_bound_C_slack": slackC, "honest_bound_C_slack_per_round": slackC / n,
            "C_slack_below_n": int(slackC < n),
            "theorem_constant": tc["constant"], "theorem_constant_per_round": tc["constant_per_round"],
            "e_bid": tc["e_bid"], "e_mon": tc["e_mon"], "e_fb": tc["e_fb"], "e_low": tc["e_low"],
            "constant_below_trivial_2n": int(tc["constant"] < 2 * n),
            "constant_below_n": int(tc["constant"] < n),
            "nontop_branch_active": int(tc["nontop_branch_active"]),
            "nontop_profiles": sum(1 for p in r["profiles"] if not p["focal_is_top"]),
            "ratio_UB_to_constant": r["ratio_UB_to_constant"],
            "ratio_LB_to_constant": r["ratio_LB_to_constant"],
            "dropped_mass_max": r["dropped_mass_max"], "seconds": r["seconds"]})
    return rows, prows


def load_ladder(resdir: Path):
    out = []
    for f in sorted(resdir.glob("ladder_*.csv")):
        by = defaultdict(list)
        keys = None
        with f.open() as fh:
            for row in csv.DictReader(fh):
                keys = row
                by[(row["variant"], row["behavior"])].append(row)
        if keys is None:
            continue
        base = {(v, b): rows for (v, b), rows in by.items()}
        ref = base.get(("pl_mesp", "profile"))
        for (v, b), rows in sorted(base.items()):
            fu = np.array([float(r["focal_utility"]) for r in rows])
            pr = np.array([float(r["platform_reward_per_round"]) for r in rows])
            sw = np.array([float(r["switches"]) for r in rows])
            fsw = np.array([float(r["false_switches"]) for r in rows])
            mp = np.array([float(r["monitored_profiles"]) for r in rows])
            dd = np.array([float(r["median_detection_delay"]) for r in rows])
            gh = np.array([float(r["gap_honest_per_round"]) for r in rows])
            mpr = np.array([float(r["mean_price"]) for r in rows])
            n = int(rows[0]["n"])
            # paired deviation gain against the same rung under the proposed profile
            ref_rows = base.get((v, "profile"))
            if ref_rows is not None and len(ref_rows) == len(rows):
                gain = fu - np.array([float(r["focal_utility"]) for r in ref_rows])
            else:
                gain = np.full(len(fu), np.nan)
            lo, hi = (t_interval(gain)[1:3] if np.isfinite(gain).all() else (float("nan"), float("nan")))
            plo, phi = t_interval(pr)[1:3]
            out.append({"family": rows[0]["family"], "Q": int(rows[0]["Q"]), "n": n, "K": int(rows[0]["K"]),
                        "variant": v, "behavior": b, "reps": len(rows),
                        "focal_utility_mean": float(fu.mean()),
                        "gain_vs_profile_mean": float(np.nanmean(gain)),
                        "gain_vs_profile_lo": lo, "gain_vs_profile_hi": hi,
                        "gain_per_round_mean": float(np.nanmean(gain)) / n,
                        "platform_reward_per_round_mean": float(pr.mean()),
                        "platform_reward_per_round_lo": plo, "platform_reward_per_round_hi": phi,
                        "switch_rate_per_monitored_profile": float(sw.sum() / max(mp.sum(), 1)),
                        "false_switch_rate_per_monitored_profile": float(fsw.sum() / max(mp.sum(), 1)),
                        "median_detection_delay": float(np.median(dd[dd >= 0])) if (dd >= 0).any() else -1.0,
                        "mean_price": float(np.mean(mpr[mpr >= 0])) if (mpr >= 0).any() else -1.0,
                        "honest_headroom_per_round": float(-gh.mean()),
                        "honest_benchmark_per_round": float(rows[0]["benchmark_honest_per_round"])})
    return out


def regime_table(Ks=(2, 3), ns=None, Qs=None):
    """Analytic feasibility and vacuity region. No simulation and no DP: these are the mechanism's own
    parameters evaluated exactly.

      completes      Q K L_n <= n, so every profile finishes Stage 1 under an even arrival path
      monitor_active N_z = n/Q - K L_n exceeds log(2 n^4) / (2 tau^2) for tau = 0.5, a representative price
      below_trivial  the published bound (A) with e_low = 0 is below the trivial bound 2n
      below_n        the published bound (A) with e_low = 0 is below n
    """
    ns = ns or [int(10 ** (k / 4)) for k in range(12, 49)]
    Qs = Qs or [q for q in range(1, 64)] + [int(round(2 ** (k / 4))) for k in range(24, 45)]
    rows = []
    for K in Ks:
        for n in ns:
            if n < 2 * K:
                continue
            d = make_design(n, K)
            for Q in Qs:
                N_z = n / Q - K * d.L
                tc = theorem_constant(n, K, Q)
                rows.append({"K": K, "n": n, "Q": Q, "L_n": d.L, "KL_n": K * d.L, "N_z_even_path": N_z,
                             "completes": int(Q * K * d.L <= n),
                             "monitor_active_tau_0.5": int(N_z > monitor_first_binds(n, 0.5)),
                             "constant": tc["constant"], "constant_per_round": tc["constant_per_round"],
                             "below_trivial_2n": int(tc["constant"] < 2 * n),
                             "below_n": int(tc["constant"] < n)})
    return rows


def nontop_threshold_table(Ks=(2, 3), deltas=(0.50, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05, 0.02, 0.01, 0.005)):
    """Smallest horizon at which the profile-local theorem's non-top branch condition 4 s_n <= delta_i holds.

    Below that horizon the theorem gives no non-top term at all, so comparing a certified interval against the
    published constant is invalid rather than merely uninformative. This is the profile-local analogue of the
    scalar adjudication recorded in audit/round2/A/EXPERIMENT_FINAL_REPORT.md Section 8 item 2.
    """
    rows = []
    for K in Ks:
        for delta in deltas:
            lo, hi = 100, 10 ** 30
            for _ in range(400):
                mid = int(math.isqrt(lo * hi))
                if mid < 2 * K + 1:
                    break
                try:
                    ok = 4.0 * make_design(mid, K).s <= delta
                except ValueError:
                    ok = False
                if ok:
                    hi = mid
                else:
                    lo = mid
                if hi / max(lo, 1) < 1.000001:
                    break
            rows.append({"K": K, "delta": delta, "n_min": hi, "log10_n_min": math.log10(hi)})
    return rows


def write(path: Path, rows):
    if not rows:
        print(f"  (no rows for {path.name})")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  {path} ({len(rows)} rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res, out = Path(a.results), Path(a.out)
    grid, prof = load_exact(res)
    write(out / "exact_grid.csv", sorted(grid, key=lambda r: (r["family"], r["n"], r["Q"])))
    write(out / "exact_profiles.csv", sorted(prof, key=lambda r: (r["family"], r["n"], r["Q"], r["z"])))
    write(out / "ladder.csv", sorted(load_ladder(res / "ladder"),
                                     key=lambda r: (r["family"], r["n"], r["Q"], r["variant"], r["behavior"])))
    write(out / "regime.csv", regime_table())
    write(out / "nontop_thresholds.csv", nontop_threshold_table())


if __name__ == "__main__":
    main()
