"""Emit the markdown tables and the summary sentences of EXPERIMENT_REPORT.md straight from the CSVs.

Every number quoted in the report is produced here, so no value is transcribed by hand. Run after
aggregate.py and paste the output, or read it to check a sentence.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import pandas as pd


def tidy(text: str) -> str:
    """House style: markdown separator rows use two hyphens, never three or more."""
    out = []
    for line in text.splitlines():
        if set(line.strip()) <= set("|:- "):
            line = re.sub(r"-{2,}", "--", line)
        out.append(line)
    return "\n".join(out)


def show_str(text):
    print(tidy(text))


def fmt(df, cols=None, nd=4):
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: f"{v:.{nd}f}" if pd.notna(v) else "")
    return d


def sec_exact(csvd):
    g = pd.read_csv(csvd / "exact_grid.csv")
    print("### Certified intervals, cells in which every profile finishes bidding and the theorem's")
    print("### non-top condition 4 s_n <= delta holds\n")
    v = g[(g.nontop_branch_active == 1) & (g.n_truncated_profiles == 0)]
    print(f"valid comparable cells: {len(v)} of {len(g)} computed")
    if len(v):
        print(f"certified UPPER bound as a fraction of the published constant: "
              f"{v.ratio_UB_to_constant.min():.3f} to {v.ratio_UB_to_constant.max():.3f}")
        print(f"certified LOWER bound as a fraction of the published constant: "
              f"{v.ratio_LB_to_constant.min():.3f} to {v.ratio_LB_to_constant.max():.3f}")
    print(f"cells in which the certified upper bound exceeds the published constant: "
          f"{int((g.ratio_UB_to_constant > 1).sum())}")
    print(f"cells in which the certified lower bound exceeds the published constant: "
          f"{int((g.ratio_LB_to_constant > 1).sum())}")
    print(f"maximum dropped Stage-1 count mass over all cells: {g.dropped_mass_max.max():.3e}")
    print(f"cells with a zero-width certified interval (the optimum never reaches a fallback): "
          f"{int((g.interval_width < 1e-9).sum())} of {len(g)}\n")
    cols = ["family", "n", "Q", "L_n", "N_z_min", "n_truncated_profiles", "n_monitor_active_profiles",
            "exploit_LB_per_round", "exploit_UB_per_round", "theorem_constant_per_round",
            "ratio_UB_to_constant", "nontop_branch_active"]
    for fam in sorted(g.family.unique()):
        x = g[g.family == fam].sort_values(["n", "Q"])
        print(f"\n#### {fam}\n")
        show_str(fmt(x[cols]).to_markdown(index=False))


def sec_localisation(csvd):
    g = pd.read_csv(csvd / "exact_grid.csv")
    print("\n### Localisation cost: exploitability and revenue against the profile count\n")
    cols = ["n", "Q", "stage1_share_of_horizon", "exploit_LB_per_round", "exploit_UB_per_round",
            "bidding_only_gain", "revenue_LB_per_round", "revenue_UB_per_round",
            "benchmark_M2_per_round", "revenue_bound_B_slack_per_round", "B_slack_below_n"]
    for fam in ("replicated_unique_top", "replicated_tied_top", "replicated_K2_unique", "regime_switch"):
        x = g[g.family == fam].sort_values(["n", "Q"])
        if not len(x):
            continue
        print(f"\n#### {fam}\n")
        show_str(fmt(x[cols]).to_markdown(index=False))
    print("\n### Where the profile count bites (analytic, regime.csv)\n")
    r = pd.read_csv(csvd / "regime.csv")
    rows = []
    for K in sorted(r.K.unique()):
        for n, grp in r[r.K == K].groupby("n"):
            c = grp[grp.completes == 1]
            b = grp[(grp.completes == 1) & (grp.below_trivial_2n == 1)]
            m = grp[(grp.completes == 1) & (grp["monitor_active_tau_0.5"] == 1)]
            rows.append({"K": K, "n": n, "L_n": int(grp.L_n.iloc[0]),
                         "Qmax_all_profiles_finish_bidding": int(c.Q.max()) if len(c) else 0,
                         "Qmax_bound_below_2n": int(b.Q.max()) if len(b) else 0,
                         "Qmax_monitor_active": int(m.Q.max()) if len(m) else 0})
    t = pd.DataFrame(rows)
    sel = t[t.n.isin([1000, 10000, 100000, 1000000, 10 ** 7, 10 ** 8, 10 ** 9, 10 ** 10, 10 ** 12])]
    show_str(sel.to_markdown(index=False))
    print("\n### Non-top branch: smallest horizon at which 4 s_n <= delta (nontop_thresholds.csv)\n")
    nt = pd.read_csv(csvd / "nontop_thresholds.csv")
    nt["delta"] = nt["delta"].map(lambda v: f"{v:.3f}")
    show_str(fmt(nt, nd=2).to_markdown(index=False))


def sec_ladder(csvd, ns=None, Qs=None):
    p = csvd / "ladder.csv"
    if not p.exists():
        print("\n(ablation ladder not available yet)\n")
        return
    L = pd.read_csv(p)
    print("\n### Contextual ablation ladder (synthetic paired simulation)\n")
    print(f"cells: {len(L)} rows over families {sorted(L.family.unique())}, "
          f"horizons {sorted(L.n.unique())}, profile counts {sorted(L.Q.unique())}, "
          f"rungs {sorted(L.variant.unique())}, behaviours {len(L.behavior.unique())}\n")
    for (fam, n, Q), g in L.groupby(["family", "n", "Q"]):
        if ns and n not in ns:
            continue
        if Qs and Q not in Qs:
            continue
        print(f"\n#### {fam}, n = {n}, Q = {Q}\n")
        rows = []
        for v, gg in g.groupby("variant"):
            uni = gg[~gg.behavior.str.startswith("joint:")]
            jnt = gg[gg.behavior.str.startswith("joint:")]
            best = uni.loc[uni.gain_per_round_mean.idxmax()] if len(uni) else None
            prop = gg[gg.behavior == "profile"]
            rows.append({
                "rung": v,
                "best tested unilateral deviation, per round": float(best.gain_per_round_mean) if best is not None else float("nan"),
                "which": str(best.behavior) if best is not None else "",
                "switch rate under the proposed profile": float(prop.switch_rate_per_monitored_profile.iloc[0]) if len(prop) else float("nan"),
                "revenue per round under the proposed profile": float(prop.platform_reward_per_round_mean.iloc[0]) if len(prop) else float("nan"),
                "worst joint honest headroom, per round": float(jnt.honest_headroom_per_round.min()) if len(jnt) else float("nan"),
                "mean announced price under the proposed profile": float(prop.mean_price.iloc[0]) if len(prop) and "mean_price" in prop else float("nan"),
            })
        t = pd.DataFrame(rows).sort_values("best tested unilateral deviation, per round")
        show_str(fmt(t, nd=5).to_markdown(index=False))


SHORTFALL = {"primary_shade_05": 0.05, "primary_shade_15": 0.15}


def sec_delay(csvd):
    """Monitor detection delay against the first-order crossing time log(2 n^4) / (2 (tau - m)^2).

    The shortfall is known exactly for the constant-shading behaviours (0.05 and 0.15) and equals the
    announced price for the behaviours that deliver zero, so the predicted delay is computed per cell from the
    measured mean price. Simulation, not exact computation.
    """
    p = csvd / "ladder.csv"
    if not p.exists():
        print("\n(detection delays not available yet)\n")
        return
    L = pd.read_csv(p)
    rows = []
    for _, r in L.iterrows():
        if r["variant"] != "pl_mesp" or r["median_detection_delay"] < 0:
            continue
        b = r["behavior"].replace("joint:", "")
        eps = SHORTFALL.get(b, r["mean_price"] if b in ("bait_switch", "trigger_fallback_shade",
                                                        "sabotage_all") else None)
        if eps is None or eps <= 0:
            continue
        pred = math.log(2 * r["n"] ** 4) / (2 * eps ** 2)
        rows.append({"family": r["family"], "n": int(r["n"]), "Q": int(r["Q"]), "behavior": r["behavior"],
                     "shortfall": eps, "median delay": r["median_detection_delay"],
                     "first-order prediction": pred,
                     "ratio": r["median_detection_delay"] / pred})
    if not rows:
        print("\n(no monitored switch with a known shortfall yet)\n")
        return
    print("\n### Monitor detection delay against the first-order formula (PL-MESP only)\n")
    show_str(fmt(pd.DataFrame(rows), nd=3).to_markdown(index=False))


def sec_checks(csvd):
    """Every scalar the prose of EXPERIMENT_REPORT.md quotes, recomputed from the CSVs in one place."""
    g = pd.read_csv(csvd / "exact_grid.csv")
    print("\n### Checks: the scalars the prose quotes, recomputed\n")
    v = g[(g.nontop_branch_active == 1) & (g.n_truncated_profiles == 0)]
    print(f"* exact cells computed: {len(g)}; families {sorted(g.family.unique())}; "
          f"horizons {sorted(g.n.unique())}; Q {sorted(g.Q.unique())}; K {sorted(g.K.unique())}")
    print(f"* valid comparable cells (all profiles finish bidding and 4 s_n <= delta): {len(v)}")
    if len(v):
        print(f"* certified UB / published constant over those: {v.ratio_UB_to_constant.min():.3f} to "
              f"{v.ratio_UB_to_constant.max():.3f}; LB / constant: {v.ratio_LB_to_constant.min():.3f} to "
              f"{v.ratio_LB_to_constant.max():.3f}")
    print(f"* cells where the certified interval exceeds the constant: "
          f"{int((g.ratio_UB_to_constant > 1).sum())} (upper end), "
          f"{int((g.ratio_LB_to_constant > 1).sum())} (lower end)")
    p61 = g[(g.prop61_gain > 0) & (g.n_truncated_profiles == 0)]
    if len(p61):
        r = p61.exploit_LB / p61.prop61_gain
        print(f"* certified LB / Proposition 6.1 deviation: {r.min():.2f} to {r.max():.2f} over "
              f"{len(p61)} cells in {p61.family.nunique()} families")
    # monotonicity of the certified upper bound in Q
    bad, degen = [], []
    for (f, n), gg in g.groupby(["family", "n"]):
        gg = gg.sort_values("Q")
        vv, tr = gg.exploit_UB_per_round.values, gg.n_truncated_profiles.values
        qq = gg.Q.values
        for k in range(1, len(vv)):
            if vv[k] < vv[k - 1] - 1e-12:
                (degen if (tr[k] > 0 and tr[k - 1] > 0) else bad).append((f, n, int(qq[k - 1]), int(qq[k]),
                                                                          vv[k - 1] - vv[k]))
    print(f"* the certified upper bound per round decreases in Q at {len(bad)} step(s) where not both cells "
          f"are fully truncated, and at {len(degen)} step(s) where both are (largest drop "
          f"{max([x[-1] for x in degen], default=0.0):.6f} per round)")
    # saturation value M_i / K on the replicated families
    for fam, mik in (("replicated_unique_top", 0.90 / 3), ("replicated_tied_top", 0.80 / 3),
                     ("replicated_K2_unique", 0.90 / 2)):
        x = g[(g.family == fam) & (g.n_truncated_profiles == g.Q)]
        if len(x):
            print(f"* {fam}: fully truncated cells give {x.exploit_UB_per_round.min():.4f} to "
                  f"{x.exploit_UB_per_round.max():.4f} per round against M_i / K = {mik:.4f}")
    # regime thresholds
    r = pd.read_csv(csvd / "regime.csv")
    agree = dis = monodis = 0
    for (K, n), gg in r.groupby(["K", "n"]):
        c = gg[gg.completes == 1]
        b = gg[(gg.completes == 1) & (gg.below_trivial_2n == 1)]
        m = gg[(gg.completes == 1) & (gg["monitor_active_tau_0.5"] == 1)]
        qc = c.Q.max() if len(c) else 0
        qb = b.Q.max() if len(b) else 0
        qm = m.Q.max() if len(m) else 0
        agree += int(qc == qb)
        dis += int(qc != qb)
        monodis += int(qm != qc)
    print(f"* regime sweep: {agree + dis} horizon-by-K cells; completion and below-2n thresholds agree in "
          f"{agree} and differ in {dis}; the monitor threshold differs from completion in {monodis}")
    print(f"* B slack below n in {int(g.B_slack_below_n.sum())} of {len(g)} cells; C slack below n in "
          f"{int(g.C_slack_below_n.sum())}")
    x = g[g.B_slack_below_n == 1]
    if len(x):
        print(f"* in those cells the exact revenue deficit per round is "
              f"{x.revenue_deficit_UB_per_round.min():.4f} to {x.revenue_deficit_UB_per_round.max():.4f} "
              f"against a slack of {x.revenue_bound_B_slack_per_round.min():.4f} to "
              f"{x.revenue_bound_B_slack_per_round.max():.4f}")


def sec_search(resd):
    """The grid search over the two-parameter deviation class: a LOWER bound for the class searched."""
    files = sorted((resd / "search").glob("*.csv")) if (resd / "search").exists() else []
    if not files:
        print("\n(deviation search not available yet)\n")
        return
    df = pd.concat([pd.read_csv(f).assign(source=f.stem) for f in files], ignore_index=True)
    print("\n### Deviation search: best searched gain against the certified interval\n")
    print(f"grid: delta in {sorted(df.delta.unique())}, c in {sorted(df.c.unique())}; "
          f"{df.reps.max()} paired replicates per point\n")
    print("The check that is exact on both sides compares the searched VALUE with the certified upper bound\n"
          "on the value, V_FUB. Comparing a simulated GAIN with the certified gain interval is not valid: it\n"
          "subtracts a noisy baseline from an exact bound, and at the cells where the certified optimum is\n"
          "deterministic it produces spurious exceedances of about a tenth of a percent.\n")
    col = "value_exceeds_V_FUB" if "value_exceeds_V_FUB" in df else "exceeds_certified_UB"
    print(f"points at which the searched VALUE exceeds V_FUB: {int(df[col].sum())} of {len(df)}\n")
    rows = []
    for (src, fam, n, Q), g in df.groupby(["source", "family", "n", "Q"]):
        b = g.loc[g.searched_gain_mean.idxmax()]
        rows.append({"source": src, "family": fam, "n": n, "Q": Q, "best_delta": b.delta, "best_c": b.c,
                     "best_searched_gain": b.searched_gain_mean, "lo": b.searched_gain_lo,
                     "hi": b.searched_gain_hi, "certified_LB": b.certified_LB, "certified_UB": b.certified_UB,
                     "fraction_of_certified_LB": b.searched_gain_mean / b.certified_LB if b.certified_LB > 0 else float("nan"),
                     "searched_value": b.get("searched_value_mean", float("nan")),
                     "V_FUB": b.get("V_FUB", float("nan")),
                     "value_exceeds_V_FUB": int(b.get("value_exceeds_V_FUB", 0))})
    show_str(fmt(pd.DataFrame(rows).sort_values(["family", "n", "Q"]), nd=3).to_markdown(index=False))


def sec_continuous(csvd, resd):
    print("\n### CG-MESP: the horizon at which each guarantee first says anything (analytic)\n")
    t = pd.read_csv(csvd / "continuous_thresholds.csv")
    x = t[(t.K == 2) & (t.L_lip == 1.0)][["D", "log10_n_price_positive", "log10_n_A_below_n",
                                          "log10_n_B_below_n", "log10_n_C_below_n", "log10_n_all_three",
                                          "log10_n_public_En_below_n"]]
    show_str(fmt(x, nd=1).to_markdown(index=False))
    print("\n### CG-MESP at runnable horizons (analytic)\n")
    d = pd.read_csv(csvd / "continuous_degeneracy.csv")
    show_str(fmt(d[d.D.isin([2, 3])][["D", "n", "g_n", "J_n", "L_n", "s_n", "rho_n", "sigma_n",
                                      "price_clipped_to_zero", "K_J_L_over_n", "boundA_over_n"]],
                 nd=4).to_markdown(index=False))
    for name, title in (("cg_structural.json", "structural regime: lemmas and the three inequalities"),
                        ("cg_oscillation.json", "necessity of the oscillation allowance"),
                        ("cg_tuned.json", "the mechanism at its own tuned parameters")):
        f = resd / "cg" / name
        if not f.exists():
            print(f"\n({name} not available yet)\n")
            continue
        print(f"\n### CG-MESP, {title} ({name})\n")
        rows = json.loads(f.read_text())
        df = pd.DataFrame(rows)
        if name == "cg_structural.json":
            df = df[["inst", "n", "K", "g", "L", "J", "awarded", "mean_tau", "viol_P2", "viol_P4",
                     "switches", "false_switches", "best_searched_gain", "boundA", "A_holds",
                     "revenue_deficit_B", "slackB", "B_holds", "honest_deficit_C", "slackC", "C_holds"]]
        show_str(fmt(df, nd=4).to_markdown(index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--results", required=True)
    ap.add_argument("--section", default="all")
    a = ap.parse_args()
    csvd, resd = Path(a.csv), Path(a.results)
    if a.section in ("all", "checks"):
        sec_checks(csvd)
    if a.section in ("all", "exact"):
        sec_exact(csvd)
    if a.section in ("all", "local"):
        sec_localisation(csvd)
    if a.section in ("all", "ladder"):
        sec_ladder(csvd)
    if a.section in ("all", "ladder"):
        sec_delay(csvd)
    if a.section in ("all", "search"):
        sec_search(resd)
    if a.section in ("all", "continuous"):
        sec_continuous(csvd, resd)


if __name__ == "__main__":
    main()
