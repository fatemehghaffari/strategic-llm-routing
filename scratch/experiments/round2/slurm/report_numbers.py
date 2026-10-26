"""Collect the E4 pilot numbers into a compact block for the report (login node, seconds)."""
import json
import sys
import os
from pathlib import Path

import numpy as np

SP = Path(os.environ["R2_WORK"]) / "round2/A"   # writable scratch directory holding runs/
P = SP / "runs/pilot/provider_bank/pilot"
BK = SP / "runs/pilot/provider_bank/bank"
sys.path.insert(0, str(Path(os.environ["R2_CODE_ROOT"]) / "scratch/experiments/round2"))
from common.design import design, detection_delay  # noqa: E402

for ds in sys.argv[1:]:
    d = json.loads((P / f"{ds}_pilot.json").read_text())
    meta = json.loads((BK / ds / "meta.json").read_text())
    print("=" * 100)
    print(ds, "verdict", d["verdict"], d["verdict_components"])
    print("pool", d["n_pool"], "meas", d["n_measurement"], "play", d["n_play"], "subsets", d["n_subsets"])
    for p in meta["providers"]:
        print(f"  {p['name']:<16} n_train={p['n_train']:>7} fit={p['fit_seconds']:>6}s "
              f"classes={p['train_class_counts']}")
    mu, M = d["mu_pooled"], d["M_pooled"]
    pl = d["play_half_diagnostic"]
    for i, p in enumerate(meta["providers"]):
        print(f"  {p['name']:<16} mu={mu[i]:.4f} M={M[i]:.4f} (play mu={pl['mu'][i]:.4f} M={pl['M'][i]:.4f})"
              f"  argmax knob={meta['menu'][int(np.argmax(d['play_half_diagnostic']['A_pooled'][i]))]}")
    print("  capacity transfer max |meas - play| =", round(pl["max_abs_capacity_transfer"], 5))
    print("(a)", json.dumps(d["a_monotonicity"]))
    for e in d["exact_low_knob_check"]:
        print("   exact:", json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in e.items()}))
    print("(b)", json.dumps(d["b_heterogeneity"]))
    print("(c)", json.dumps(d["c_top_structure"]))
    print("  cells", d["cells_occupied"])
    for s in d["d_price_tracking"]["summary"]:
        n = s["n"]
        dd = design(n, 4)
        mu_play_focal = pl["mu"][d["focal"]]
        real_eps = s["mean_tau"] - mu_play_focal
        print(f"  n={n:>7} L={s['L']:>6} N={s['N']:>7} s_n={s['s_n']:.4f} tau={s['mean_tau']:.4f} "
              f"[{s['tau_ci_lo']:.4f},{s['tau_ci_hi']:.4f}] tau-(M2-s_n)={s['mean_tau_minus_M2_plus_sn']:+.4f} "
              f"|tau-M2|={s['abs_mean_tau_minus_M2']:.4f} within_s_n={s['price_within_sn_of_M2']} "
              f"rew={s['mean_reward_per_round']:.4f} (M2={s['M2_measured']:.4f}) eff={s['mean_effort_per_round']:+.4f} "
              f"cost={s['mean_compute_cost_per_round']:.1f} sw={s['switch_freq_proposed']:.2f} "
              f"badsw={s['switches_without_tau_above_capacity']} realized-tau={s['realized_minus_tau']:+.4f} "
              f"focal_won={s['winner_is_focal_freq']:.2f}")
        print(f"          bait knob1: shortfall_calib={s['bait_shortfall_tau_minus_mu_focal']:+.4f} "
              f"shortfall_real={real_eps:+.4f} detected={s['bait_switch_detected_when_focal_won']}/"
              f"{s['focal_won_trials']} median_delay={s['bait_median_detection_delay']} "
              f"theory_calib={s['bait_theory_delay_at_shortfall']} "
              f"theory_real={round(detection_delay(n, real_eps), 0) if real_eps > 0 else None} "
              f"paired_dU={s['paired_utility_change_bait_minus_proposed']:.1f} "
              f"[{s['paired_ci_lo']:.1f},{s['paired_ci_hi']:.1f}] rew={s['bait_mean_reward_per_round']:.4f}")
        print(f"          bait zero : detected={s['bzero_detected_when_focal_won']}/{s['focal_won_trials']} "
              f"median_delay={s['bzero_median_detection_delay']} theory={round(s['bzero_theory_delay_at_tau'], 1)} "
              f"paired_dU={s['bzero_paired_utility_change']:.1f} rew={s['bzero_mean_reward_per_round']:.4f}")
