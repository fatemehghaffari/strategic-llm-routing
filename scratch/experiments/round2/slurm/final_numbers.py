"""Print the E4 final-run tables for the report (login node, seconds)."""
import csv
import json
import os
import sys
from pathlib import Path

SP = Path(os.environ["R2_WORK"]) / "round2/A"   # writable scratch directory holding runs/
F = SP / "runs/final/provider_bank"


def num(x, nd=4):
    try:
        return round(float(x), nd)
    except (TypeError, ValueError):
        return x


def load(ds):
    rows = []
    for name in (f"{ds}_final_summary.csv", f"{ds}_final_supplementary_n200000.csv"):
        p = F / name
        if p.exists():
            rows += list(csv.DictReader(p.open()))
    return rows


for ds in sys.argv[1:]:
    j = json.loads((F / f"{ds}_final.json").read_text())["meta"]
    print("=" * 120)
    print(ds, "trials", j["trials"], "seconds", j["seconds"], "ucb_index", j["ucb_index_default"])
    print("  mu", [num(x) for x in j["mu_pooled"]], "M", [num(x) for x in j["M_pooled"]],
          "focal", j["focal"], "M2", num(j["M2_measured"]), "M2_play", num(j["M2_play"]))
    rows = load(ds)
    print("\n-- price and revenue, proposed profile, every variant")
    for r in rows:
        if r["behavior"] != "proposed":
            continue
        print(f"  n={int(r['n']):>7} {r['variant']:<10} trials={r['trials']:>3} s_n={num(r['s_n'])} "
              f"tau={num(r['mean_tau'])} [{num(r['tau_ci_lo'])},{num(r['tau_ci_hi'])}] "
              f"band=[{num(r['price_band_lo'])},{num(r['price_band_hi'])}] in_band={num(r['in_price_band_rate'],3)} "
              f"tau-(M2-s_n)={num(r['mean_tau_minus_M2_plus_sn'])} "
              f"({num(r['abs_mean_tau_minus_M2_plus_sn_in_units_of_sn'],3)} s_n) "
              f"rew={num(r['mean_reward_per_round'])} rew-M2={num(r['reward_minus_M2'])} "
              f"eff={num(r['mean_effort_per_round'])} trees={num(r['mean_compute_cost_per_round'],1)} "
              f"realized-tau={num(r['realized_minus_tau'])} focal_won={num(r['focal_won_rate'],3)}")
    print("\n-- switch, false switch, detection, paired utility (all cells)")
    for r in rows:
        det = (f"det={r['detections_when_focal_won']}/{r['focal_won_trials']} "
               f"median={num(r['median_detection_delay'],1)} "
               f"obs/theory_real={num(r['median_delay_over_theory_at_real_shortfall'],3)} "
               f"obs/theory_calib={num(r['median_delay_over_theory_at_calibrated_shortfall'],3)}")
        print(f"  n={int(r['n']):>7} {r['variant']:<10} {r['behavior']:<16} "
              f"sw={num(r['switch_rate'],3)} [{num(r['switch_cp_lo'],3)},{num(r['switch_cp_hi'],3)}] "
              f"fs={num(r['false_switch_rate'],3)} [{num(r['false_switch_cp_lo'],3)},{num(r['false_switch_cp_hi'],3)}] "
              f"badsw={r['switches_without_tau_above_capacity']} {det} "
              f"dU={num(r['paired_utility_change_vs_proposed'],1)} "
              f"[{num(r['paired_ci_lo'],1)},{num(r['paired_ci_hi'],1)}] "
              f"bca=[{num(r['paired_bca_lo'],1)},{num(r['paired_bca_hi'],1)}] "
              f"rew={num(r['mean_reward_per_round'])} trees={num(r['mean_compute_cost_per_round'],1)} "
              f"eff={num(r['mean_effort_per_round'])}")
