"""Mechanism baselines and ablation ladder (E2), evaluated under specified agent behaviors.

Type P comparison: one behavior profile, every mechanism variant, paired by seed and by tape.
Type M comparison: each mechanism under the best tested deviation (reported as a lower bound on exploitability).
Behavior profiles include joint adversarial ones, which the honest-benchmark claim of Theorem thm:private-mesp
covers (it is uniform over feasible behavioral profiles, not only unilateral deviations).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import instances as I, mechanism as M, seeds as S, stats as ST  # noqa: E402
from common.design import design as make_design, detection_delay  # noqa: E402

LADDER = ["mesp", "esp_nomon", "esp_mon_nofb", "esp_excl", "esp_ucbfb", "esp_ucbfb_warm", "esp_exp3_warm",
          "esp_runnerup", "mesp_rawprice", "mesp_conf1n", "mesp_noslack", "mesp_windowed"]


def policies(inst: I.Instance, profile: str) -> list[M.Policy]:
    """Behavior profile for all K agents. Honest agents always play S_star (feasible and honest)."""
    if profile == "s_star":
        return [M.SStar()] * inst.K
    if profile == "all_max":
        return [M.AllMax()] * inst.K
    if profile.startswith("focal_"):
        return M.profile(inst, M.behavior(profile[len("focal_"):]))
    strategic = [i for i in range(inst.K) if not inst.is_honest(i)]
    pol = [M.SStar()] * inst.K
    if profile == "joint_bait":
        for i in strategic:
            pol[i] = M.BaitSwitch()
    elif profile == "joint_sequential":
        for i in strategic:
            pol[i] = M.TriggerFallbackShade()
    elif profile == "joint_fallback_zero":
        for i in strategic:
            pol[i] = M.ZeroFallback()
    else:
        raise ValueError(profile)
    return pol


PROFILES = ["s_star", "all_max", "focal_underbid_05", "focal_underbid_15", "focal_primary_shade_05",
            "focal_primary_shade_15", "focal_bait_switch", "focal_trigger_fallback_shade", "focal_boundary_ride",
            "joint_bait", "joint_sequential", "joint_fallback_zero"]


def cell(inst, n, variant, profile, reps, phase):
    rows = []
    for rep in range(reps):
        g = S.trial_streams("ablations", phase, inst.index, n, rep)[2]
        rows.append(M.episode(inst, n, M.VARIANTS[variant], policies(inst, profile), g))
    return rows


def summarize(inst, n, variant, profile, rows, base_rows):
    d = make_design(n, inst.K)
    rew = np.array([r["platform_reward"] for r in rows], float) / n
    gap_h = np.array([r["gap_honest"] for r in rows], float) / n
    gap_p = np.array([r["gap_private"] for r in rows], float) / n
    eff = np.array([r["total_effort"] for r in rows], float) / n
    sw = np.array([r["switched"] for r in rows], int); fs = np.array([r["false_switch"] for r in rows], int)
    fb = np.array([r["fallback_rounds"] for r in rows], float)
    dd = np.array([r["detection_delay"] for r in rows if r["detection_delay"] > 0], float)
    gain = np.array([a["focal_utility"] - b["focal_utility"] for a, b in zip(rows, base_rows)], float) / n
    out = {"instance": inst.alias, "n": n, "variant": variant, "profile": profile, "reps": len(rows),
           "L": d.L, "s": d.s, "M2": inst.M2, "mu_H_star": inst.mu_H_star}
    for name, x in [("reward_per_round", rew), ("gap_honest_per_round", gap_h), ("gap_private_per_round", gap_p),
                    ("effort_per_round", eff), ("fallback_rounds", fb), ("focal_gain_per_round", gain)]:
        m, lo, hi, se = ST.t_interval(x); out[name + "_mean"] = m; out[name + "_lo"] = lo; out[name + "_hi"] = hi
    out["switch_rate"] = float(sw.mean()); out["switch_lo"], out["switch_hi"] = ST.clopper_pearson(int(sw.sum()), len(sw))
    out["false_switch_rate"] = float(fs.mean()); out["false_switch_lo"], out["false_switch_hi"] = ST.clopper_pearson(int(fs.sum()), len(fs))
    out["detection_delay_median"] = float(np.median(dd)) if dd.size else float("nan")
    out["detection_delay_n"] = int(dd.size)
    out["honest_benchmark_violated"] = int(out["gap_honest_per_round_lo"] > 0)  # reward per round below mu_H^star
    out["mean_tau"] = float(np.mean([r["tau"] for r in rows]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", nargs="+", default=["unique_top", "tied_top"])
    ap.add_argument("--n", type=int, nargs="+", default=[2000, 20000])
    ap.add_argument("--variants", nargs="+", default=LADDER)
    ap.add_argument("--profiles", nargs="+", default=PROFILES)
    ap.add_argument("--reps", type=int, default=40); ap.add_argument("--phase", default="pilot")
    ap.add_argument("--out", required=True); ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    jobs = [(inst_name, n, v, p) for inst_name in a.instances for n in a.n for v in a.variants for p in a.profiles]

    def run(job):
        inst_name, n, v, p = job
        inst = I.get(inst_name)
        rows = cell(inst, n, v, p, a.reps, a.phase)
        base = rows if p == "s_star" else cell(inst, n, v, "s_star", a.reps, a.phase)
        return summarize(inst, n, v, p, rows, base)

    if a.workers == 1:
        res = [run(j) for j in jobs]
    else:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=a.workers) as ex:
            res = list(ex.map(_run_global, [(a.reps, a.phase) + j for j in jobs], chunksize=1))
    with (out / f"ladder_{a.phase}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0])); w.writeheader(); w.writerows(res)
    print(f"wrote {len(res)} cells to {out}/ladder_{a.phase}.csv")


def _run_global(args):
    reps, phase, inst_name, n, v, p = args
    inst = I.get(inst_name)
    rows = cell(inst, n, v, p, reps, phase)
    base = rows if p == "s_star" else cell(inst, n, v, "s_star", reps, phase)
    return summarize(inst, n, v, p, rows, base)


if __name__ == "__main__":
    main()
