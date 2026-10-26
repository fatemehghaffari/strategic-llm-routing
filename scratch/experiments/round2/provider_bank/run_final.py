"""E4 final run: MESP and three ablation variants on the provider bank, phase "final".

Evidence category: real labeled tasks and real provider answers; the effort choice is scripted.

One dataset per job. Cells are (variant, behavior, horizon); replicates are paired across behaviors and across
variants by the seed `trial_streams("nonsynthetic", "final", dataset_index, n, rep)`, so every behavior of a
replicate meets the same tasks and the same tree orderings wherever it agrees with the proposed profile.

Variants come from `common.mechanism.VARIANTS` and are driven through the same adapter, so no mechanism code is
duplicated here. Note that `common.design.ucb_bonus` now defaults to the known-horizon index
sqrt(4 log n / T), which changes `esp_ucbfb` only.

Price is reported against the band the proof states, (M_(2) - 2 s_n)_+ <= tau <= M_(2), and against the point
M_(2) - s_n that the mechanism's rule targets.

    python -m provider_bank.run_final --bank <bank root> --out <dir> --dataset covertype \\
        --reps 200 --horizons 2000 8000 20000 --supp-n 200000 --supp-reps 50
"""
from __future__ import annotations

import argparse
import csv
import gc
import json
import time
from pathlib import Path

import numpy as np

from common import design as DS
from common import mechanism as M
from common import seeds as S
from common import stats as ST
from common.instances import Instance

from . import adapter as AD
from . import bank as B
from .run_pilot import DATASETS, pooled_instance

GATE_VARIANTS = ("mesp", "esp_nomon", "esp_excl", "esp_ucbfb")
SUPP_VARIANTS = ("mesp", "esp_nomon")
UNDERBID_KNOB = 16
BEHAVIORS = ("proposed", "bait_knob1", "bait_zero", f"underbid_knob{UNDERBID_KNOB}")
BASELINE = "proposed"


def policy_for(behavior: str, bk: B.ResponseBank):
    if behavior == "proposed":
        return None
    if behavior == "bait_knob1":
        return AD.BaitSwitchKnob1()
    if behavior == "bait_zero":
        return M.BaitSwitch()
    if behavior.startswith("underbid_knob"):
        return AD.UnderbidKnob(bk, int(behavior[len("underbid_knob"):]))
    raise ValueError(behavior)


FIELDS = ["dataset", "dataset_index", "variant", "behavior", "n", "rep", "L", "N", "s_n", "tau", "winner",
          "focal", "focal_won", "beta_second", "beta_focal", "platform_reward", "reward_per_round", "switched",
          "false_switch", "detection_delay", "primary_rounds", "fallback_rounds", "exclusions",
          "fallback_reward", "total_effort", "effort_per_round", "compute_cost", "compute_cost_per_round",
          "mean_knob_played", "focal_utility", "primary_realized_rate", "primary_calibrated_rate",
          "primary_play_expected_rate", "tau_above_winner_capacity", "in_price_band", "M2_measured",
          "M2_play", "M_top_measured"]


def _knob_rate(bk: B.ResponseBank, provider: int, knobs: np.ndarray, curve: np.ndarray) -> float:
    """Mean accuracy that the given curve assigns to the knobs actually played (sabotage counts as 0)."""
    if knobs.size == 0:
        return float("nan")
    idx = {k: j for j, k in enumerate(bk.menu)}
    vals = np.array([0.0 if int(k) <= 0 else float(curve[provider, idx[int(k)]]) for k in knobs])
    return float(vals.mean())


def one_trial(bk, inst, play_A, n, rep, dataset_index, variant_name, behavior):
    _, _, gens = S.trial_streams("nonsynthetic", "final", dataset_index, n, rep)
    variant = M.VARIANTS[variant_name]
    pol = M.profile(inst, policy_for(behavior, bk))
    out, ex = AD.episode_on_bank(bk, inst, n, variant, pol, gens)
    q = int(out["primary_rounds"])
    pri = ex["records"]["primary"]
    knobs = np.asarray(pri["knob"][:q]) if q else np.zeros(0, dtype=int)
    W = int(out["winner"])
    d = DS.design(n, inst.K, L=variant.L)
    M2, s = inst.M2, d.s
    row = {
        "dataset": bk.dataset, "dataset_index": dataset_index, "variant": variant_name, "behavior": behavior,
        "n": n, "rep": rep, "L": out["L"], "N": out["N"], "s_n": out["s"], "tau": out["tau"], "winner": W,
        "focal": inst.focal, "focal_won": out["focal_won"], "beta_second": out["beta_second"],
        "beta_focal": out[f"beta_{inst.focal}"], "platform_reward": out["platform_reward"],
        "reward_per_round": out["platform_reward"] / n, "switched": out["switched"],
        "false_switch": out["false_switch"], "detection_delay": out["detection_delay"], "primary_rounds": q,
        "fallback_rounds": out["fallback_rounds"], "exclusions": out["exclusions"],
        "fallback_reward": out["fallback_reward"], "total_effort": out["total_effort"],
        "effort_per_round": out["total_effort"] / n, "compute_cost": ex["compute_cost"],
        "compute_cost_per_round": ex["compute_cost"] / n, "mean_knob_played": ex["mean_knob_played"],
        "focal_utility": out["focal_utility"],
        "primary_realized_rate": float(np.mean(pri["outcome"][:q])) if q else float("nan"),
        "primary_calibrated_rate": _knob_rate(bk, W, knobs, bk.curves().A_pooled),
        "primary_play_expected_rate": _knob_rate(bk, W, knobs, play_A),
        "tau_above_winner_capacity": int(out["tau"] > inst.M[W] + 1e-12),
        "in_price_band": int(max(0.0, M2 - 2 * s) - 1e-12 <= out["tau"] <= M2 + 1e-12),
        "M2_measured": M2, "M2_play": float(np.sort(play_A.max(axis=1))[::-1][1]), "M_top_measured": inst.M_top,
    }
    return row


def run_cells(bk, inst, play_A, dataset_index, out_csv: Path, plan) -> list[dict]:
    """`plan` is a list of (n, variants, reps). Rows are flushed after every (n, variant) block."""
    rows = []
    with Path(out_csv).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for n, variants, reps in plan:
            for vname in variants:
                t0 = time.time()
                for rep in range(reps):
                    for behavior in BEHAVIORS:
                        r = one_trial(bk, inst, play_A, n, rep, dataset_index, vname, behavior)
                        rows.append(r)
                        w.writerow(r)
                    if n >= 100000:
                        gc.collect()
                f.flush()
                print(f"[{bk.dataset}] n={n} {vname}: {reps} reps x {len(BEHAVIORS)} behaviors "
                      f"in {time.time() - t0:.0f}s", flush=True)
    return rows


def summarize(rows: list[dict], inst: Instance, bca_variant: str = "mesp") -> list[dict]:
    out = []
    base = {(r["variant"], r["n"], r["rep"]): r for r in rows if r["behavior"] == BASELINE}
    cells = sorted({(r["n"], r["variant"], r["behavior"]) for r in rows},
                   key=lambda c: (c[0], GATE_VARIANTS.index(c[1]) if c[1] in GATE_VARIANTS else 99,
                                  BEHAVIORS.index(c[2])))
    for n, vname, behavior in cells:
        sub = [r for r in rows if r["n"] == n and r["variant"] == vname and r["behavior"] == behavior]
        d = DS.design(n, inst.K, L=M.VARIANTS[vname].L)
        s, M2 = d.s, inst.M2
        tau = np.array([r["tau"] for r in sub])
        m_tau, tlo, thi, tse = ST.t_interval(tau)
        rew = np.array([r["reward_per_round"] for r in sub])
        m_rew, rlo, rhi, _ = ST.t_interval(rew)
        sw = int(sum(r["switched"] for r in sub))
        fs = int(sum(r["false_switch"] for r in sub))
        sw_lo, sw_hi = ST.clopper_pearson(sw, len(sub))
        fs_lo, fs_hi = ST.clopper_pearson(fs, len(sub))
        det = [r for r in sub if r["switched"] and r["focal_won"]]
        ratio_real, ratio_cal = [], []
        for r in det:
            for eps_key, store in (("primary_play_expected_rate", ratio_real),
                                   ("primary_calibrated_rate", ratio_cal)):
                eps = r["tau"] - r[eps_key]
                if eps > 0:
                    store.append(r["detection_delay"] / DS.detection_delay(n, eps))
        pair = [(r, base.get((vname, n, r["rep"]))) for r in sub]
        gain = np.array([a["focal_utility"] - b["focal_utility"] for a, b in pair if b is not None])
        g, glo, ghi, _ = ST.t_interval(gain) if gain.size else (0.0, 0.0, 0.0, 0.0)
        bca = (None, None)
        if behavior != BASELINE and vname == bca_variant and gain.size:
            rng = S.analysis_rng("nonsynthetic", n, BEHAVIORS.index(behavior))
            bca = ST.bca_paired(np.array([a["focal_utility"] for a, b in pair if b is not None]),
                                np.array([b["focal_utility"] for a, b in pair if b is not None]), rng)
        row = {
            "dataset": sub[0]["dataset"], "n": n, "variant": vname, "behavior": behavior, "trials": len(sub),
            "L": d.L, "N": d.N, "s_n": s, "M2_measured": M2, "M2_play": sub[0]["M2_play"],
            "M_top_measured": inst.M_top,
            "mean_tau": m_tau, "tau_ci_lo": tlo, "tau_ci_hi": thi, "tau_se": tse,
            "price_band_lo": max(0.0, M2 - 2 * s), "price_band_hi": M2,
            "in_price_band_rate": float(np.mean([r["in_price_band"] for r in sub])),
            "mean_tau_minus_M2_plus_sn": m_tau - (M2 - s),
            "abs_mean_tau_minus_M2_plus_sn_in_units_of_sn": abs(m_tau - (M2 - s)) / s,
            "mean_reward_per_round": m_rew, "reward_ci_lo": rlo, "reward_ci_hi": rhi,
            "reward_minus_M2": m_rew - M2,
            "mean_effort_per_round": float(np.mean([r["effort_per_round"] for r in sub])),
            "mean_compute_cost_per_round": float(np.mean([r["compute_cost_per_round"] for r in sub])),
            "mean_knob_played": float(np.mean([r["mean_knob_played"] for r in sub])),
            "focal_won_rate": float(np.mean([r["focal_won"] for r in sub])),
            "switch_rate": sw / len(sub), "switch_cp_lo": sw_lo, "switch_cp_hi": sw_hi,
            "false_switch_rate": fs / len(sub), "false_switch_cp_lo": fs_lo, "false_switch_cp_hi": fs_hi,
            "switches_without_tau_above_capacity": int(sum(r["switched"] and not r["tau_above_winner_capacity"]
                                                           for r in sub)),
            "detections_when_focal_won": len(det),
            "focal_won_trials": int(sum(r["focal_won"] for r in sub)),
            "median_detection_delay": float(np.median([r["detection_delay"] for r in det])) if det else None,
            "median_delay_over_theory_at_real_shortfall": float(np.median(ratio_real)) if ratio_real else None,
            "median_delay_over_theory_at_calibrated_shortfall": float(np.median(ratio_cal)) if ratio_cal else None,
            "mean_primary_realized_rate": float(np.nanmean([r["primary_realized_rate"] for r in sub])),
            "mean_primary_calibrated_rate": float(np.nanmean([r["primary_calibrated_rate"] for r in sub])),
            "mean_primary_play_expected_rate": float(np.nanmean([r["primary_play_expected_rate"] for r in sub])),
            "realized_minus_tau": float(np.nanmean([r["primary_realized_rate"] - r["tau"] for r in sub])),
            "paired_utility_change_vs_proposed": float(g), "paired_ci_lo": float(glo), "paired_ci_hi": float(ghi),
            "paired_bca_lo": bca[0], "paired_bca_hi": bca[1],
        }
        out.append(row)
    return out


def write_csv(rows, path: Path):
    if not rows:
        return
    with Path(path).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dataset", required=True, choices=list(DATASETS))
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--horizons", type=int, nargs="+", default=[2000, 8000, 20000])
    ap.add_argument("--supp-n", type=int, default=200000)
    ap.add_argument("--supp-reps", type=int, default=50)
    ap.add_argument("--variants", nargs="+", default=list(GATE_VARIANTS))
    ap.add_argument("--supp-variants", nargs="+", default=list(SUPP_VARIANTS))
    ap.add_argument("--summarize-only", action="store_true",
                    help="rebuild the summaries from an existing trials CSV (insurance against a wall-clock kill)")
    a = ap.parse_args()

    t0 = time.time()
    root, out_dir = Path(a.bank), Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    bk = B.ResponseBank.load(a.dataset, root)
    inst = pooled_instance(bk)
    dataset_index = DATASETS.index(a.dataset)
    # Play-half curves: a diagnostic measured on the tasks the mechanism plays. They calibrate nothing; they
    # give the real mean behind each knob, which is what the monitor actually sees.
    play_A = B.measure_curves(bk, n_subsets=bk.meta.get("n_subsets", B.N_SUBSETS),
                              rng=np.random.default_rng(int(bk.meta.get("curve_seed", 0)) + 1),
                              tasks=bk.play_idx).A_pooled
    np.save(out_dir / f"{a.dataset}_play_half_A_pooled.npy", play_A)

    trials_csv = out_dir / f"{a.dataset}_final_trials.csv"
    if a.summarize_only:
        with trials_csv.open(newline="") as f:
            rows = [{k: (int(v) if k in ("n", "rep", "winner", "focal", "focal_won", "switched", "false_switch",
                                         "detection_delay", "primary_rounds", "fallback_rounds", "exclusions",
                                         "L", "N", "platform_reward", "fallback_reward", "compute_cost",
                                         "in_price_band", "tau_above_winner_capacity")
                        else v if k in ("dataset", "variant", "behavior") else float(v))
                     for k, v in r.items()} for r in csv.DictReader(f)]
        print(f"[{a.dataset}] summarizing {len(rows)} stored trials", flush=True)
    else:
        plan = [(n, tuple(a.variants), a.reps) for n in a.horizons]
        if a.supp_n:
            plan.append((a.supp_n, tuple(a.supp_variants), a.supp_reps))
        rows = run_cells(bk, inst, play_A, dataset_index, trials_csv, plan)

    summ = summarize(rows, inst)
    write_csv([r for r in summ if r["n"] in a.horizons], out_dir / f"{a.dataset}_final_summary.csv")
    if a.supp_n:
        write_csv([r for r in summ if r["n"] == a.supp_n],
                  out_dir / f"{a.dataset}_final_supplementary_n{a.supp_n}.csv")
    meta = {
        "dataset": a.dataset, "phase": "final", "suite": "nonsynthetic",
        "evidence": "real labeled tasks and real provider answers; the effort choice is scripted",
        "reps": a.reps, "horizons": a.horizons, "supplementary_n": a.supp_n, "supplementary_reps": a.supp_reps,
        "variants": a.variants, "supplementary_variants": a.supp_variants, "behaviors": list(BEHAVIORS),
        "underbid_knob": UNDERBID_KNOB, "mu_pooled": [float(x) for x in bk.curves().mu_pooled],
        "M_pooled": [float(x) for x in bk.curves().M_pooled], "focal": inst.focal, "honest": list(inst.honest),
        "M2_measured": inst.M2, "M2_play": float(np.sort(play_A.max(axis=1))[::-1][1]),
        "ucb_index_default": getattr(DS, "UCB_INDEX_DEFAULT", "unknown"),
        "trials": len(rows), "seconds": round(time.time() - t0, 1),
    }
    (out_dir / f"{a.dataset}_final.json").write_text(json.dumps({"meta": meta, "summary": summ}, indent=1))
    print(f"[{a.dataset}] {len(rows)} trials in {meta['seconds']:.0f}s", flush=True)


if __name__ == "__main__":
    main()
