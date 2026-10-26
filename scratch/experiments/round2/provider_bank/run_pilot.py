"""E4 pilot: acceptance tests (a) to (d) on the built provider banks.

Evidence category: real labeled tasks and real provider answers; the effort choice is scripted.

(a) monotonicity of A_i(., k) in the knob, listing every violation larger than two standard errors of the
    paired difference, pooled and per context cell;
(b) heterogeneity: pooled max_i M_i minus min_i M_i above 0.05;
(c) top structure: the pooled capacity gap M_(1) minus M_(2) against 2 s_n at n = 20,000 and K = 4;
(d) price tracking: MESP under the proposed profile on the pooled bank at n in {2000, 8000, 20000} with 20
    replicates, and the same seeds under a scripted bait and switch in which the winner drops to knob 1 after
    winning.

Everything is written incrementally so an interruption loses at most the horizon in flight.
"""
from __future__ import annotations

import argparse
import csv
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
from . import checks as C

DATASETS = ("fashion_mnist", "covertype")
HORIZONS = (2000, 8000, 20000)
REPS = 20
K_PILOT = 4
N_REF = 20000
HETEROGENEITY_MIN = 0.05


def pooled_instance(bk: B.ResponseBank) -> Instance:
    """Scalar instance read off the pooled measured curves; the focal agent is the largest capacity."""
    c = bk.curves()
    mu = tuple(float(x) for x in c.mu_pooled)
    Mv = tuple(float(x) for x in c.M_pooled)
    focal = int(np.argmax(Mv))
    honest = tuple(i for i in range(bk.K) if i != focal)
    return Instance(f"{bk.dataset}_pooled", f"{bk.dataset}_pooled", mu, Mv, honest, focal, 0)


# ================================================================ (a) monotonicity

def monotonicity(bk: B.ResponseBank, out_csv: Path) -> dict:
    c = bk.curves()
    menu = bk.menu
    rows, n_pooled, n_cell_cmp = [], 0, 0
    for i in range(bk.K):
        for j in range(len(menu) - 1):
            n_pooled += 1
            d, se = float(c.d_pooled[i, j]), float(c.d_se_pooled[i, j])
            if np.isfinite(se) and d < -2.0 * se:
                rows.append(["pooled", i, -1, int(c.n_cell[i].sum()), menu[j], menu[j + 1], d, se, d / se])
        for cell in range(B.N_BINS):
            if c.n_cell[i, cell] < 2:
                continue
            for j in range(len(menu) - 1):
                n_cell_cmp += 1
                d, se = float(c.d_cell[i, cell, j]), float(c.d_se_cell[i, cell, j])
                if np.isfinite(se) and d < -2.0 * se:
                    rows.append(["cell", i, cell, int(c.n_cell[i, cell]), menu[j], menu[j + 1], d, se, d / se])
    with Path(out_csv).open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scope", "provider", "cell", "n_tasks", "knob_from", "knob_to", "delta", "se", "z"])
        for r in rows:
            w.writerow(r[:6] + [f"{r[6]:.6f}", f"{r[7]:.6f}", f"{r[8]:.3f}"])
    pooled_v = [r for r in rows if r[0] == "pooled"]
    return {"n_pooled_comparisons": n_pooled, "n_cell_comparisons": n_cell_cmp,
            "n_pooled_violations": len(pooled_v), "n_cell_violations": len(rows) - len(pooled_v),
            "worst_pooled_z": (min([r[8] for r in pooled_v]) if pooled_v else None),
            "worst_cell_z": (min([r[8] for r in rows if r[0] == "cell"], default=None)),
            "violations_csv": str(out_csv), "pass": len(pooled_v) == 0}


# ================================================================ (d) mechanism runs

FIELDS = ["dataset", "dataset_index", "n", "rep", "profile", "L", "N", "s_n", "tau", "winner", "focal",
          "focal_won", "beta_second", "platform_reward", "reward_per_round", "switched", "false_switch",
          "detection_delay", "primary_rounds", "fallback_rounds", "total_effort", "effort_per_round",
          "compute_cost", "compute_cost_per_round", "mean_knob_played", "focal_utility",
          "primary_realized_rate", "tau_above_winner_capacity", "M2_measured", "M_top_measured"]


PROFILES = ("proposed", "bait_switch", "bait_switch_zero")


def _policy(profile_name: str):
    if profile_name == "proposed":
        return None
    if profile_name == "bait_switch":     # the scripted deviation of the brief: drop to knob 1 after winning
        return AD.BaitSwitchKnob1()
    if profile_name == "bait_switch_zero":  # supplementary: drop to target 0 (sabotage every primary round)
        return M.BaitSwitch()
    raise ValueError(profile_name)


def one_episode(bk: B.ResponseBank, inst: Instance, n: int, rep: int, dataset_index: int, profile_name: str):
    _, _, gens = S.trial_streams("nonsynthetic", "pilot", dataset_index, n, rep)
    pol = M.profile(inst, _policy(profile_name))
    out, ex = AD.episode_on_bank(bk, inst, n, M.VARIANTS["mesp"], pol, gens)
    q = int(out["primary_rounds"])
    pri = ex["records"]["primary"]
    rate = float(np.mean(pri["outcome"][:q])) if q else float("nan")
    row = {"dataset": bk.dataset, "dataset_index": dataset_index, "n": n, "rep": rep, "profile": profile_name,
           "L": out["L"], "N": out["N"], "s_n": out["s"], "tau": out["tau"], "winner": out["winner"],
           "focal": inst.focal, "focal_won": out["focal_won"], "beta_second": out["beta_second"],
           "platform_reward": out["platform_reward"], "reward_per_round": out["platform_reward"] / n,
           "switched": out["switched"], "false_switch": out["false_switch"],
           "detection_delay": out["detection_delay"], "primary_rounds": q,
           "fallback_rounds": out["fallback_rounds"], "total_effort": out["total_effort"],
           "effort_per_round": out["total_effort"] / n, "compute_cost": ex["compute_cost"],
           "compute_cost_per_round": ex["compute_cost"] / n, "mean_knob_played": ex["mean_knob_played"],
           "focal_utility": out["focal_utility"], "primary_realized_rate": rate,
           "tau_above_winner_capacity": int(out["tau"] > inst.M[out["winner"]] + 1e-12),
           "M2_measured": inst.M2, "M_top_measured": inst.M_top}
    return row


def run_mechanism(bk: B.ResponseBank, inst: Instance, dataset_index: int, out_csv: Path, horizons=HORIZONS,
                  reps: int = REPS) -> list[dict]:
    rows = []
    f = Path(out_csv).open("w", newline="")
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for n in horizons:
        t0 = time.time()
        for rep in range(reps):
            for profile_name in PROFILES:
                r = one_episode(bk, inst, n, rep, dataset_index, profile_name)
                rows.append(r)
                w.writerow(r)
        f.flush()
        print(f"[{bk.dataset}] n={n} done in {time.time() - t0:.0f}s", flush=True)
    f.close()
    return rows


def summarize(rows: list[dict], inst: Instance, dataset: str, play: dict | None = None) -> list[dict]:
    """Per horizon summary. `play` carries the play-half diagnostic capacities, which calibrate nothing."""
    out = []
    play = play or {}
    M2_play = play.get("M2")
    for n in sorted({r["n"] for r in rows}):
        d = DS.design(n, inst.K)
        sub = {p: [r for r in rows if r["n"] == n and r["profile"] == p] for p in PROFILES}
        star, bait, bzero = sub["proposed"], sub["bait_switch"], sub["bait_switch_zero"]
        assert [r["rep"] for r in star] == [r["rep"] for r in bait], "paired replicates are misaligned"
        assert all(s["winner"] == b["winner"] for s, b in zip(star, bait)), \
            "the two profiles agree in Stage 1, so they must select the same winner"
        tau = np.array([r["tau"] for r in star])
        m_tau, lo, hi, se = ST.t_interval(tau)
        rew = np.array([r["reward_per_round"] for r in star])
        m_rew, rlo, rhi, _ = ST.t_interval(rew)
        sw = int(sum(r["switched"] for r in star))
        sw_bad = int(sum(r["switched"] and not r["tau_above_winner_capacity"] for r in star))
        cp_lo, cp_hi = ST.clopper_pearson(sw, len(star))
        gain = np.array([b["focal_utility"] - s["focal_utility"] for s, b in zip(star, bait)])
        g, glo, ghi, _ = ST.t_interval(gain)
        det = [b["detection_delay"] for b in bait if b["switched"] and b["focal_won"]]
        bsw = int(sum(b["switched"] and b["focal_won"] for b in bait))
        n_focal_won = int(sum(b["focal_won"] for b in bait))
        gain0 = np.array([b["focal_utility"] - s["focal_utility"] for s, b in zip(star, bzero)])
        g0, g0lo, g0hi, _ = ST.t_interval(gain0)
        det0 = [b["detection_delay"] for b in bzero if b["switched"] and b["focal_won"]]
        bsw0 = int(sum(b["switched"] and b["focal_won"] for b in bzero))
        beta2 = np.array([r["beta_second"] for r in star])
        out.append({
            "dataset": dataset, "n": n, "K": inst.K, "L": d.L, "N": d.N, "s_n": d.s,
            "M2_measured": inst.M2, "M_top_measured": inst.M_top,
            "mean_tau": m_tau, "tau_ci_lo": lo, "tau_ci_hi": hi, "tau_se": se,
            "mean_tau_minus_M2": m_tau - inst.M2, "abs_mean_tau_minus_M2": abs(m_tau - inst.M2),
            "mean_tau_minus_M2_plus_sn": m_tau - (inst.M2 - d.s),
            "price_within_sn_of_M2": int(abs(m_tau - inst.M2) <= d.s),
            "mean_reward_per_round": m_rew, "reward_ci_lo": rlo, "reward_ci_hi": rhi,
            "reward_minus_M2": m_rew - inst.M2,
            "mean_effort_per_round": float(np.mean([r["effort_per_round"] for r in star])),
            "mean_compute_cost_per_round": float(np.mean([r["compute_cost_per_round"] for r in star])),
            "mean_knob_played": float(np.mean([r["mean_knob_played"] for r in star])),
            "switch_freq_proposed": sw / len(star), "switch_cp_lo": cp_lo, "switch_cp_hi": cp_hi,
            "switches_without_tau_above_capacity": sw_bad,
            "false_switch_proposed": int(sum(r["false_switch"] for r in star)),
            "mean_primary_realized_rate": float(np.nanmean([r["primary_realized_rate"] for r in star])),
            "realized_minus_tau": float(np.nanmean([r["primary_realized_rate"] - r["tau"] for r in star])),
            "winner_is_focal_freq": float(np.mean([r["focal_won"] for r in star])),
            "bait_switch_detected_when_focal_won": bsw, "bait_switch_trials": len(bait),
            "focal_won_trials": n_focal_won,
            "bait_median_detection_delay": (float(np.median(det)) if det else None),
            "bait_shortfall_tau_minus_mu_focal": m_tau - inst.mu[inst.focal],
            "bait_theory_delay_at_shortfall": (DS.detection_delay(n, m_tau - inst.mu[inst.focal])
                                               if m_tau - inst.mu[inst.focal] > 0 else None),
            "paired_utility_change_bait_minus_proposed": g, "paired_ci_lo": glo, "paired_ci_hi": ghi,
            "paired_focal_won_trials": int(sum(s["focal_won"] for s in star)),
            "bait_mean_reward_per_round": float(np.mean([b["reward_per_round"] for b in bait])),
            # supplementary deviation: the winner delivers target 0 (sabotage) on every primary round
            "bzero_detected_when_focal_won": bsw0,
            "bzero_median_detection_delay": (float(np.median(det0)) if det0 else None),
            "bzero_theory_delay_at_tau": (DS.detection_delay(n, m_tau) if m_tau > 0 else None),
            "bzero_paired_utility_change": g0, "bzero_paired_ci_lo": g0lo, "bzero_paired_ci_hi": g0hi,
            "bzero_mean_reward_per_round": float(np.mean([b["reward_per_round"] for b in bzero])),
            # diagnostics for the price test: the bid order statistic and the play-half capacities
            "mean_beta_second": float(beta2.mean()), "beta_second_minus_M2": float(beta2.mean()) - inst.M2,
            "M2_play_diagnostic": M2_play,
            "abs_mean_tau_minus_M2_play": (abs(m_tau - M2_play) if M2_play is not None else None),
            "price_within_sn_of_M2_play": (int(abs(m_tau - M2_play) <= d.s) if M2_play is not None else None),
        })
    return out


# ================================================================ driver

def run_dataset(dataset: str, bank_root: Path, out_dir: Path, dataset_index: int, reps: int = REPS,
                horizons=HORIZONS) -> dict:
    bk = B.ResponseBank.load(dataset, bank_root)
    inst = pooled_instance(bk)
    c = bk.curves()
    d_ref = DS.design(N_REF, K_PILOT)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    mono = monotonicity(bk, out_dir / f"{dataset}_monotonicity_violations.csv")
    # Diagnostic only: the same curves measured on the play half. They calibrate nothing; they quantify how far
    # the measured capacities travel from the half they were measured on to the half the mechanism plays.
    cp = B.measure_curves(bk, n_subsets=bk.meta.get("n_subsets", B.N_SUBSETS),
                          rng=np.random.default_rng(int(bk.meta.get("curve_seed", 0)) + 1), tasks=bk.play_idx)
    play = {"mu": [float(x) for x in cp.mu_pooled], "M": [float(x) for x in cp.M_pooled],
            "M2": float(np.sort(cp.M_pooled)[::-1][1]), "M_top": float(cp.M_pooled.max()),
            "A_pooled": [[float(x) for x in row] for row in cp.A_pooled],
            "max_abs_capacity_transfer": float(np.max(np.abs(cp.M_pooled - np.asarray(inst.M))))}
    Ms = np.sort(np.asarray(inst.M))[::-1]
    spread = float(Ms[0] - Ms[-1])
    gap = float(Ms[0] - Ms[1])
    res = {
        "dataset": dataset, "dataset_index": dataset_index,
        "evidence": "real labeled tasks and real provider answers; the effort choice is scripted",
        "providers": [p["name"] for p in bk.meta.get("providers", [])],
        "provider_training_sizes": [p["n_train"] for p in bk.meta.get("providers", [])],
        "n_pool": bk.meta.get("n_pool"), "n_measurement": bk.meta.get("n_measurement"),
        "n_play": bk.meta.get("n_play"), "n_subsets": bk.meta.get("n_subsets"),
        "mu_pooled": [float(x) for x in c.mu_pooled], "M_pooled": [float(x) for x in c.M_pooled],
        "focal": inst.focal, "honest": list(inst.honest),
        "a_monotonicity": mono,
        "b_heterogeneity": {"spread": spread, "threshold": HETEROGENEITY_MIN, "pass": spread > HETEROGENEITY_MIN},
        "play_half_diagnostic": play,
        "exact_low_knob_check": [C.compare_with_measured(bk, i) for i in range(bk.K)],
        "c_top_structure": {"M_sorted": [float(x) for x in Ms], "top_gap": gap,
                            "two_s_n_at_20000": 2 * d_ref.s, "s_n_at_20000": d_ref.s,
                            "regime": "clear top gap" if gap > 2 * d_ref.s else "near tie"},
        "cells_occupied": [[int(x) for x in row] for row in c.n_cell],
    }
    (out_dir / f"{dataset}_partial.json").write_text(json.dumps(res, indent=1))

    rows = run_mechanism(bk, inst, dataset_index, out_dir / f"{dataset}_mesp_trials.csv", horizons, reps)
    summ = summarize(rows, inst, dataset, play)
    with (out_dir / f"{dataset}_mesp_summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summ[0].keys()))
        w.writeheader()
        for s in summ:
            w.writerow(s)
    # The gate is evaluated on the horizons the pilot specifies; any extra horizon is supplementary and is
    # reported but does not decide the verdict.
    gate = [s for s in summ if s["n"] in HORIZONS]
    price_ok = all(s["price_within_sn_of_M2"] for s in gate)
    switch_ok = all(s["switches_without_tau_above_capacity"] == 0 for s in gate)
    res["d_price_tracking"] = {"summary": summ, "gate_horizons": list(HORIZONS),
                               "price_within_sn_all_gate_horizons": bool(price_ok),
                               "no_unexplained_switch": bool(switch_ok), "pass": bool(price_ok and switch_ok)}
    # The stated acceptance for this worker is item (d): the mean price is within s_n of the measured second
    # capacity and no switch occurs under the proposed profile unless tau exceeded the winner's capacity.
    # Items (a) to (c) are reported with numbers and their own pass flags, and the composite flag below is the
    # conjunction that the experiment decision's drop rule asks for.
    res["verdict"] = "GO" if res["d_price_tracking"]["pass"] else "NO-GO"
    res["verdict_components"] = {"a_monotonicity_no_pooled_violation": bool(mono["pass"]),
                                 "b_heterogeneity": bool(res["b_heterogeneity"]["pass"]),
                                 "c_regime": res["c_top_structure"]["regime"],
                                 "d_price_and_switches": bool(res["d_price_tracking"]["pass"])}
    (out_dir / f"{dataset}_pilot.json").write_text(json.dumps(res, indent=1))
    print(f"[{dataset}] verdict {res['verdict']}", flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--datasets", nargs="+", default=list(DATASETS))
    ap.add_argument("--reps", type=int, default=REPS)
    ap.add_argument("--horizons", type=int, nargs="+", default=list(HORIZONS))
    a = ap.parse_args()
    all_res = {}
    for ds in a.datasets:
        idx = DATASETS.index(ds)
        all_res[ds] = run_dataset(ds, Path(a.bank), Path(a.out), idx, a.reps, tuple(a.horizons))
    Path(a.out, "pilot_summary.json").write_text(json.dumps(all_res, indent=1))
    for ds, r in all_res.items():
        print(ds, r["verdict"])


if __name__ == "__main__":
    main()
