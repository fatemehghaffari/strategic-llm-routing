"""Regenerate audit/round2/A4/TABLES.md from the aggregated CSVs.

    python make_tables.py --csv experiments/data/A4 --out audit/round2/A4/TABLES.md

Every scalar quoted anywhere in REPORT.md is recomputed here, printed with the
CSV it comes from and the expression that produces it, so that the prose can be
checked line by line without rerunning anything.
"""
import argparse
import os

import numpy as np
import pandas as pd
from scipy import stats

CHECKS = []


def chk(name, value, source, expr, fmt="{:.4f}"):
    CHECKS.append((name, fmt.format(value) if isinstance(value, (int, float, np.floating,
                                                                np.integer)) else str(value),
                   source, expr))
    return value


def load(d, f):
    p = os.path.join(d, f)
    return pd.read_csv(p) if os.path.exists(p) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    D = a.csv
    body = []

    # ---------------- provenance ----------------------------------------- #
    rc = load(D, "rowcounts.csv")
    v = load(D, "validation_vs_paper_table1.csv")
    if rc is not None:
        r5 = rc[rc.shot == "5shot"].iloc[0]
        chk("rows_used_5shot", int(r5.rows_used), "rowcounts.csv",
            "rowcounts[shot=='5shot'].rows_used", "{:d}")
        chk("outcomes_used_5shot", int(r5.outcomes_used), "rowcounts.csv",
            "rowcounts[shot=='5shot'].outcomes_used", "{:d}")
        r0 = rc[rc.shot == "0shot"].iloc[0]
        chk("rows_used_0shot", int(r0.rows_used), "rowcounts.csv",
            "rowcounts[shot=='0shot'].rows_used", "{:d}")
        chk("outcomes_used_0shot", int(r0.outcomes_used), "rowcounts.csv",
            "rowcounts[shot=='0shot'].outcomes_used", "{:d}")
        body.append("## 1. Provenance row counts\n\n" + rc.to_markdown(index=False))
    if v is not None:
        mm = v.groupby("context")["ours_minus_published"].apply(lambda s: s.abs().max())
        for c, x in mm.items():
            chk(f"maxabs_vs_table1_{c}", float(x), "validation_vs_paper_table1.csv",
                f"groupby(context).ours_minus_published.abs().max()['{c}']")
        chk("maxabs_vs_table1_excl_MTBench", float(mm.drop("MT-Bench").max()),
            "validation_vs_paper_table1.csv", "same, MT-Bench dropped")
        body.append("\n## 2. Check against RouterBench Table 1 (max abs difference)\n\n"
                    + mm.round(4).rename("max_abs_diff").to_frame().to_markdown())

    # ---------------- measured capability + flips ------------------------- #
    cap = load(D, "capabilities_finite_5shot.csv")
    order = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]
    if cap is not None:
        t = cap.pivot(index="model", columns="context", values="M")[order]
        body.append("\n## 3. Measured capability M_i(z), 5-shot "
                    "(STEP 2a: the table the brief asks for)\n\n"
                    + t.round(3).to_markdown())
        body.append("\n\nBest model per context: "
                    + ", ".join(f"{c}: {m}" for c, m in t.idxmax(axis=0).items()) + ".\n")
        mass = load(D, "context_masses_5shot.csv")
        if mass is not None:
            body.append("\nArrival mass of each context (empirical, from the row counts):\n\n"
                        + mass.round(5).to_markdown(index=False))
            for _, r in mass.iterrows():
                chk(f"mass_{r['context']}", float(r["mass"]), "context_masses_5shot.csv",
                    f"mass[context=='{r['context']}']", "{:.5f}")
    for shot in ("5shot", "0shot"):
        fs = load(D, f"flips_summary_{shot}.csv")
        if fs is None:
            continue
        r = fs.iloc[0]
        for k in ("raw_flip_rate", "sig_flip_rate", "bonf_flip_rate",
                  "frac_ctx_pairs_different_best", "mean_kendall_tau_between_contexts",
                  "min_kendall_tau_between_contexts"):
            chk(f"{k}_{shot}", float(r[k]), f"flips_summary_{shot}.csv", k)
        for k in ("raw_flips", "raw_comparisons", "sig_flips", "sig_comparisons",
                  "bonf_flips", "bonf_comparisons", "n_distinct_best_models"):
            chk(f"{k}_{shot}", int(r[k]), f"flips_summary_{shot}.csv", k, "{:d}")
        body.append(f"\n## 4. Rank-flip rates, {shot}\n\n"
                    + fs.T.rename(columns={0: "value"}).to_markdown())
    pp = load(D, "flips_perpair_5shot.csv")
    if pp is not None:
        chk("n_model_pairs_never_flipping_5shot", int((pp.flip_rate == 0).sum()),
            "flips_perpair_5shot.csv", "(flip_rate==0).sum()", "{:d}")
        chk("max_pair_flip_rate_5shot", float(pp.flip_rate.max()),
            "flips_perpair_5shot.csv", "flip_rate.max()")

    fc = load(D, "flips_continuous.csv")
    ed = load(D, "embedding_diagnostic.csv")
    if fc is not None:
        r = fc[(fc.d == 2) & (fc.k == 200)].iloc[0]
        for k in ("raw_flip_rate", "frac_queries_best_differs_from_global",
                  "mean_pointwise_max", "mean_pointwise_second", "global_max_mean",
                  "global_second_mean"):
            chk(f"cont_d2k200_{k}", float(r[k]), "flips_continuous.csv",
                f"row d==2 & k==200, column {k}")
        chk("cont_d2k200_n_cells", int(r.n_cells), "flips_continuous.csv",
            "row d==2 & k==200, n_cells", "{:d}")
        body.append("\n## 5. Continuous contexts (STEP 2b)\n\n"
                    + fc.round(4).to_markdown(index=False))
    if ed is not None:
        r = ed[ed.d == 2].iloc[0]
        chk("embed_d2_cell_family_purity", float(r.cell_family_purity),
            "embedding_diagnostic.csv", "row d==2, cell_family_purity")
        chk("embed_d2_nmi", float(r.normalised_mutual_info_cell_family),
            "embedding_diagnostic.csv", "row d==2, normalised_mutual_info_cell_family")
        body.append("\n\nEmbedding diagnostic (how much of the benchmark family the "
                    "TF-IDF/LSA cells recover):\n\n" + ed.round(4).to_markdown(index=False))

    # ---------------- analytic gap ---------------------------------------- #
    ag = load(D, "analytic_gap_summary.csv")
    if ag is not None:
        for _, r in ag.iterrows():
            tag = f"{r.context_set}{'u' if r.uniform_mass else ''}"
            for k in ("spearman_rho", "ols_slope", "gap_mean", "gap_max",
                      "gap_at_flip0_mean", "frac_triples_gap_above_0.01"):
                chk(f"analytic_{tag}_{k}", float(r[k]), "analytic_gap_summary.csv",
                    f"row {r.context_set}/uniform_mass={r.uniform_mass}, column {k}")
            chk(f"analytic_{tag}_spearman_p", float(r.spearman_p),
                "analytic_gap_summary.csv", "spearman_p", "{:.3g}")
            for k in ("mean_scalar_mass_price_above_capability",
                      "frac_triples_scalar_price_infeasible_somewhere",
                      "spearman_flip_vs_infeasible_mass"):
                chk(f"analytic_{tag}_{k}", float(r[k]), "analytic_gap_summary.csv",
                    f"row {r.context_set}/uniform_mass={r.uniform_mass}, column {k}")
        body.append("\n## 6. Analytic scalar-vs-contextual gap, all 165 triples\n\n"
                    + ag.round(5).to_markdown(index=False))

    fr = load(D, "flip_regression_summary.csv")
    if fr is not None:
        for _, r in fr.iterrows():
            for k in ("spearman_rho_flip_vs_simgap", "ols_slope", "mean_sim_gap",
                      "mean_analytic_gap", "frac_sim_gap_positive",
                      "spearman_analytic_vs_sim"):
                chk(f"simgap_{r.context_set}_{k}", float(r[k]),
                    "flip_regression_summary.csv", f"row {r.context_set}, column {k}")
            chk(f"simgap_{r.context_set}_spearman_p", float(r.spearman_p),
                "flip_regression_summary.csv", "spearman_p", "{:.3g}")
        body.append("\n## 7. SIMULATED gap at n = 300,000, all 165 triples\n\n"
                    + fr.round(5).to_markdown(index=False))
    frd = load(D, "flip_regression.csv")
    if frd is not None:
        for cs, s in frd.groupby("context_set"):
            chk(f"simconv_scalar_{cs}", float(s.conv_mesp_scalar.mean()),
                "flip_regression.csv", f"[context_set=='{cs}'].conv_mesp_scalar.mean()")
            chk(f"simconv_contextual_{cs}", float(s.conv_plmesp.mean()),
                "flip_regression.csv", f"[context_set=='{cs}'].conv_plmesp.mean()")

    tt = load(D, "two_top_summary.csv")
    if tt is not None:
        body.append("\n## 7b. The paper's two-top condition, measured\n\n"
                    + tt.round(4).to_markdown(index=False))
        for _, r in tt.iterrows():
            tag = f"{r.context_set}_K{int(r.K)}"
            chk(f"twotop_{tag}_mass_exact", float(r["mean_mass_within_0.0"]),
                "two_top_summary.csv", f"row {r.context_set}/K={int(r.K)}, mean_mass_within_0.0")
            chk(f"twotop_{tag}_mass_0.01", float(r["mean_mass_within_0.01"]),
                "two_top_summary.csv", f"row {r.context_set}/K={int(r.K)}, mean_mass_within_0.01")
            chk(f"twotop_{tag}_mean_top_gap", float(r.mean_top_gap),
                "two_top_summary.csv", f"row {r.context_set}/K={int(r.K)}, mean_top_gap")


    # ---------------- oscillation allowance -------------------------------- #
    ra = load(D, "rho_audit.csv")
    if ra is not None:
        for _, r in ra.iterrows():
            if int(r.n) in (300000, 10 ** 7, 10 ** 9, 10 ** 12) and int(r.d) in (1, 2):
                chk(f"rho_paper_n{int(r.n)}_d{int(r.d)}", float(r.rho_paper),
                    "rho_audit.csv", f"row n=={int(r.n)} & d=={int(r.d)}, rho_paper")
                chk(f"totalshade_n{int(r.n)}_d{int(r.d)}",
                    float(r.total_price_shading_3s_plus_rho), "rho_audit.csv",
                    f"row n=={int(r.n)} & d=={int(r.d)}, total_price_shading_3s_plus_rho")
                chk(f"rho_measured_n{int(r.n)}_d{int(r.d)}",
                    float(r.rho_measured_p95_within_cell), "rho_audit.csv",
                    f"row n=={int(r.n)} & d=={int(r.d)}, rho_measured_p95_within_cell")
        r = ra[(ra.n == 300000) & (ra.d == 2)].iloc[0]
        chk("cg_elicitation_fraction_n300k_d2", float(r.elicitation_fraction),
            "rho_audit.csv", "row n==300000 & d==2, elicitation_fraction")
        chk("s_n_cg_n300k_d2", float(r.s_n), "rho_audit.csv", "row n==300000 & d==2, s_n")
        body.append("\n## 8b. The continuum oscillation allowance, arithmetic only\n\n"
                    + ra.round(6).to_markdown(index=False))

    # ---------------- horizon --------------------------------------------- #
    hz = load(D, "horizon_sweep.csv")
    if hz is not None:
        body.append("\n## 8. Horizon sweep, the three selected triples\n\n"
                    + hz.round(5).to_markdown(index=False))
        for cs, s in hz.groupby("context_set"):
            for n in sorted(s.n.unique()):
                sub = s[s.n == n]
                chk(f"horizon_{cs}_n{n}_mean_simgap", float(sub.sim_gap.mean()),
                    "horizon_sweep.csv", f"[context_set=='{cs}' & n=={n}].sim_gap.mean()")
    ha = load(D, "horizon_all_summary.csv")
    if ha is not None:
        r = ha.iloc[0]
        for k in ("spearman_rho_flip_vs_simgap", "ols_slope", "mean_sim_gap",
                  "frac_sim_gap_positive", "mean_compconv_scalar",
                  "mean_compconv_contextual", "frac_runs_scalar_price_above_cap",
                  "spearman_flip_vs_compconv_scalar",
                  "spearman_flip_vs_compconv_scalar_p"):
            chk(f"horizall_{k}", float(r[k]), "horizon_all_summary.csv", k)
        chk("horizall_spearman_p", float(r.spearman_p), "horizon_all_summary.csv",
            "spearman_p", "{:.3g}")
        chk("horizall_n", int(r.n), "horizon_all_summary.csv", "n", "{:d}")
        body.append("\n## 9. All 165 triples at the larger horizon\n\n"
                    + ha.round(5).to_markdown(index=False))

    # ---------------- headline -------------------------------------------- #
    hs = load(D, "headline_summary.csv")
    if hs is not None:
        for fsx in sorted(hs.family_set.unique()):
            sub = hs[hs.family_set == fsx]
            piv = sub.pivot_table(index=["mech"], columns="alpha",
                                  values=["nonstrategic", "strategic"])
            body.append(f"\n## 10. Two worlds, revenue per round, context set {fsx}\n\n"
                        + piv.round(4).to_markdown())
        for al in sorted(hs.alpha.unique()):
            for fsx in sorted(hs.family_set.unique()):
                sub = hs[(hs.alpha == al) & (hs.family_set == fsx)]
                for m in sorted(sub.mech.unique()):
                    r = sub[sub.mech == m]
                    chk(f"rev_nonstrat_{fsx}_{al}_{m}", float(r.nonstrategic.mean()),
                        "headline_summary.csv",
                        f"[family_set=='{fsx}' & alpha=='{al}' & mech=='{m}'].nonstrategic.mean()")
                    chk(f"rev_strat_{fsx}_{al}_{m}", float(r.strategic.mean()),
                        "headline_summary.csv",
                        f"[family_set=='{fsx}' & alpha=='{al}' & mech=='{m}'].strategic.mean()")
                    chk(f"degrad_{fsx}_{al}_{m}", float(r.degradation.mean()),
                        "headline_summary.csv", "same rows, degradation.mean()")
        # how far the strategic-world revenue sits above the honest benchmark,
        # which is the floor the robustness theorem guarantees
        hs2 = hs.copy()
        hs2["strat_minus_honest"] = hs2.strategic - hs2.honest_bench
        body.append("\n## 10b. Strategic-world revenue minus the honest benchmark\n\n"
                    + hs2.groupby("mech").strat_minus_honest.agg(
                        ["mean", "min", "max", "count"]).round(4).to_markdown())
        for m, s3 in hs2.groupby("mech"):
            chk(f"stratminushonest_mean_{m}", float(s3.strat_minus_honest.mean()),
                "headline_summary.csv",
                f"(strategic - honest_bench)[mech=='{m}'].mean()")
            chk(f"stratminushonest_min_{m}", float(s3.strat_minus_honest.min()),
                "headline_summary.csv",
                f"(strategic - honest_bench)[mech=='{m}'].min()")
        chk("n_headline_configs", int(hs.groupby(
            ["family_set", "triple", "alpha"]).ngroups), "headline_summary.csv",
            "number of (family_set, triple, alpha) cells present", "{:d}")

    ex = load(D, "exploitability.csv")
    if ex is not None:
        body.append("\n## 11. Exploitability: best single deviation at the proposed profile\n\n"
                    + ex.pivot_table(index=["family_set", "mech"], columns="alpha",
                                     values="best_gain_per_round").round(4).to_markdown())
        for (fsx, m), s in ex.groupby(["family_set", "mech"]):
            chk(f"exploit_max_{fsx}_{m}", float(s.best_gain_per_round.max()),
                "exploitability.csv",
                f"[family_set=='{fsx}' & mech=='{m}'].best_gain_per_round.max()")

    hw = load(D, "headline_worlds.csv")
    if hw is not None:
        cc = hw[hw.world == "proposed"].groupby(["family_set", "mech"])[
            "compliant_convictions"].mean()
        body.append("\n## 12. Compliant convictions at the proposed profile "
                    "(mean count per run)\n\n" + cc.round(3).to_frame().to_markdown())
        for (fsx, m), x in cc.items():
            chk(f"compconv_{fsx}_{m}", float(x), "headline_worlds.csv",
                f"[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()")
        el = hw[hw.world == "proposed"].groupby("family_set")[
            ["locals_past_elicitation", "locals_total"]].mean()
        body.append("\n\nLocal instances that completed elicitation:\n\n"
                    + el.round(2).to_markdown())

    sp = load(D, "strategic_profiles.csv")
    if sp is not None:
        body.append("\n## 11b. The strategic profile reached, and what it costs\n\n"
                    + sp.pivot_table(index=["family_set", "mech"], columns="alpha",
                                     values="revenue_drop_vs_proposed").round(4).to_markdown())
        body.append("\n\nHow many providers shade in the profile reached:\n\n"
                    + sp.pivot_table(index=["family_set", "mech"], columns="alpha",
                                     values="n_shading_agents").round(2).to_markdown())
        for (fsx, m), s2 in sp.groupby(["family_set", "mech"]):
            chk(f"stratdrop_{fsx}_{m}", float(s2.revenue_drop_vs_proposed.mean()),
                "strategic_profiles.csv",
                f"[family_set=='{fsx}' & mech=='{m}'].revenue_drop_vs_proposed.mean()")
        chk("frac_strategic_profiles_are_fixed_points", float(sp.is_fixed_point.mean()),
            "strategic_profiles.csv", "is_fixed_point.mean()")

    rbl = load(D, "rich_br_from_logs.csv")
    if rbl is not None:
        g = rbl.groupby("mech").agg(
            n_cells=("mech", "size"),
            nonstrategic=("nonstrategic_revenue", "mean"),
            strategic=("strategic_revenue", "mean"),
            degradation=("degradation", "mean"),
            worst_degradation=("degradation", "max")).reset_index()
        rbl2 = rbl.copy()
        rbl2["has_undercut"] = rbl2.profile.str.contains("undercut")
        g = g.merge(rbl2.groupby("mech").has_undercut.sum().rename(
            "cells_whose_profile_uses_undercut").reset_index(), on="mech")
        body.append("\n## 11c. THE FAIR STRATEGIC COMPARISON: best response over one rich "
                    "option class for every rule\n\n" + g.round(4).to_markdown(index=False))
        for _, r in g.iterrows():
            for k in ("nonstrategic", "strategic", "degradation", "worst_degradation"):
                chk(f"richbr_{r.mech}_{k}", float(r[k]), "rich_br_from_logs.csv",
                    f"groupby(mech).{k}.mean() for mech=='{r.mech}'")
            chk(f"richbr_{r.mech}_n_cells", int(r.n_cells), "rich_br_from_logs.csv",
                f"count for mech=='{r.mech}'", "{:d}")
            chk(f"richbr_{r.mech}_undercut_cells",
                int(r.cells_whose_profile_uses_undercut), "rich_br_from_logs.csv",
                f"profile.str.contains('undercut').sum() for mech=='{r.mech}'", "{:d}")
        body.append("\n\nProfile reached in each completed cell:\n\n"
                    + rbl[["triple", "alpha", "mech", "profile",
                           "nonstrategic_revenue", "strategic_revenue"]]
                    .round(4).to_markdown(index=False))

    rbs = load(D, "rich_br_summary.csv")
    if rbs is not None:
        body.append("\n## 11c. THE FAIR STRATEGIC COMPARISON: best response over one rich "
                    "option class for every rule\n\n" + rbs.round(4).to_markdown(index=False))
        for _, r in rbs.iterrows():
            for k in ("nonstrategic", "strategic", "degradation", "worst_degradation",
                      "frac_fixed_point"):
                chk(f"richbr_{r.mech}_{k}", float(r[k]), "rich_br_summary.csv",
                    f"row mech=='{r.mech}', column {k}")
    rbd = load(D, "rich_br.csv")
    if rbd is not None:
        body.append("\n\nProfile reached in each cell:\n\n"
                    + rbd[["triple", "alpha", "mech", "profile", "is_fixed_point",
                           "nonstrategic_revenue", "strategic_revenue"]]
                    .round(4).to_markdown(index=False))

    bs = load(D, "baseline_single_observation_summary.csv")
    if bs is not None:
        body.append("\n## 14. BASELINE 1: the single-observation exclusion rule under "
                    "our observation model\n\n" + bs.round(4).to_markdown(index=False))
        for _, r in bs.iterrows():
            tag = f"{r.rule}_L{int(r.L_elicit)}_{r.empty_policy or 'na'}"
            for k in ("revenue_per_round", "compliant_exclusions", "idle_fraction",
                      "price_is_one_share", "price_is_zero_share"):
                v = r[k]
                if pd.notna(v):
                    chk(f"soe_{tag}_{k}", float(v),
                        "baseline_single_observation_summary.csv",
                        f"row rule=={r.rule}, L=={int(r.L_elicit)}, "
                        f"empty=={r.empty_policy}, column {k}")

    ucs = load(D, "utility_curves_summary.csv")
    if ucs is not None:
        body.append("\n## 15. Utility against effort, per arm role\n\n"
                    + ucs.round(4).to_markdown(index=False))
        for _, r in ucs.iterrows():
            tag = f"{r.instance}_{r.context}_{r.sweep}_{r.role}_{r.rule}"
            for k in ("peak_delivered_mean", "peak_utility",
                      "utility_at_full_capability", "peak_minus_full_capability",
                      "total_variation", "announced_price", "own_capability",
                      "runner_up_capability"):
                v = r[k]
                if pd.notna(v):
                    chk(f"util_{tag}_{k}", float(v), "utility_curves_summary.csv",
                        f"row {tag}, column {k}")
    ucc = load(D, "utility_curves_crosscheck.csv")
    if ucc is not None:
        body.append("\n\nCross-check of the curve against the deviation code path:\n\n"
                    + ucc[["instance", "context", "role", "rule", "crosscheck_option",
                           "agent_utility_per_round"]].round(4).to_markdown(index=False))

    # ---------------- fine shading ----------------------------------------- #
    fb = load(D, "fine_shading_best.csv")
    if fb is not None:
        body.append("\n## 12b. The exact best response against each rule "
                    "(fine shading and undercutting), best gain found\n\n"
                    + fb.pivot_table(index=["triple", "mech"], columns="alpha",
                                     values="gain_per_round").round(4).to_markdown())
        body.append("\n\nRevenue the platform loses at that deviation:\n\n"
                    + fb.pivot_table(index=["triple", "mech"], columns="alpha",
                                     values="revenue_loss_per_round").round(4).to_markdown())
        for (m,), s2 in fb.groupby(["mech"]):
            chk(f"fine_maxgain_{m}", float(s2.gain_per_round.max()),
                "fine_shading_best.csv", f"[mech=='{m}'].gain_per_round.max()")
            chk(f"fine_maxrevloss_{m}", float(s2.revenue_loss_per_round.max()),
                "fine_shading_best.csv", f"[mech=='{m}'].revenue_loss_per_round.max()")
            chk(f"fine_meanrevloss_{m}", float(s2.revenue_loss_per_round.mean()),
                "fine_shading_best.csv", f"[mech=='{m}'].revenue_loss_per_round.mean()")

    # ---------------- fine shading ----------------------------------------- #
    fb = load(D, "fine_shading_best.csv")
    if fb is not None:
        body.append("\n## 12b. The exact best response against each rule "
                    "(fine shading and undercutting), best gain found\n\n"
                    + fb.pivot_table(index=["triple", "mech"], columns="alpha",
                                     values="gain_per_round").round(4).to_markdown())
        body.append("\n\nRevenue the platform loses at that deviation:\n\n"
                    + fb.pivot_table(index=["triple", "mech"], columns="alpha",
                                     values="revenue_loss_per_round").round(4).to_markdown())
        for m, s2 in fb.groupby("mech"):
            chk(f"fine_maxgain_{m}", float(s2.gain_per_round.max()),
                "fine_shading_best.csv", f"[mech=='{m}'].gain_per_round.max()")
            chk(f"fine_maxrevloss_{m}", float(s2.revenue_loss_per_round.max()),
                "fine_shading_best.csv", f"[mech=='{m}'].revenue_loss_per_round.max()")
            chk(f"fine_meanrevloss_{m}", float(s2.revenue_loss_per_round.mean()),
                "fine_shading_best.csv", f"[mech=='{m}'].revenue_loss_per_round.mean()")

    us = load(D, "undercut_summary.csv")
    if us is not None:
        body.append("\n## 12c. THE SAME DEVIATION APPLIED TO EVERY RULE: undercut the "
                    "pointwise runner-up\n\n" + us.round(4).to_markdown(index=False))
        for _, r in us.iterrows():
            chk(f"undercut_meangain_{r.mech}", float(r.mean_gain),
                "undercut_summary.csv", f"row mech=='{r.mech}', mean_gain")
            chk(f"undercut_maxgain_{r.mech}", float(r.max_gain),
                "undercut_summary.csv", f"row mech=='{r.mech}', max_gain")
            chk(f"undercut_meanrevloss_{r.mech}", float(r.mean_revenue_loss),
                "undercut_summary.csv", f"row mech=='{r.mech}', mean_revenue_loss")
            chk(f"undercut_maxrevloss_{r.mech}", float(r.max_revenue_loss),
                "undercut_summary.csv", f"row mech=='{r.mech}', max_revenue_loss")
    tb = load(D, "two_top_best_subsets.csv")
    if tb is not None:
        body.append("\n## 7c. The most two-top-like subset at each size\n\n"
                    + tb.round(4).to_markdown(index=False))
        for _, r in tb.iterrows():
            chk(f"twotopbest_{r.context_set}_K{int(r.K)}_gap", float(r.mean_top_gap),
                "two_top_best_subsets.csv",
                f"row {r.context_set}/K={int(r.K)}, mean_top_gap")
            chk(f"twotopbest_{r.context_set}_K{int(r.K)}_mass005",
                float(r["mass_within_0.05"]), "two_top_best_subsets.csv",
                f"row {r.context_set}/K={int(r.K)}, mass_within_0.05")

    gp = load(D, "capability_gap_summary.csv")
    if gp is None or not len(gp):
        gp = load(D, "capability_gap_from_logs.csv")
    if gp is not None:
        body.append("\n## 16. The capability-gap sweep: is the two-top condition a "
                    "cliff or a transition?\n\n" + gp.round(5).to_markdown(index=False))
        for _, r in gp.iterrows():
            tag = f"{r.mech}_d{r.delta:g}"
            for k in ("equilibrium_revenue", "revenue_at_proposed",
                      "announced_price_mean", "runner_up_curve_total_variation"):
                if k in gp.columns and pd.notna(r[k]):
                    chk(f"gap_{tag}_{k}", float(r[k]),
                        "capability_gap_summary.csv", f"row mech {r.mech}, delta {r.delta:g}")

    sbs = load(D, "baseline_second_best_summary.csv")
    if sbs is not None:
        body.append("\n## 17. BASELINE 3: the Second-Best Utility Guarantee "
                    "Mechanism (WWW 2026), reimplemented from the paper\n\n"
                    + sbs.round(4).to_markdown(index=False))
        for _, r in sbs.iterrows():
            tag = f"{r.setting}_{r.mech}_{r.deviation}"
            for k in ("revenue_per_round", "monitor_fire_rate",
                      "compliant_conviction_rate", "undelegated_fraction",
                      "post_fire_revenue_per_round", "price_above_cap_mass"):
                if k in sbs.columns and pd.notna(r[k]):
                    chk(f"sb_{tag}_{k}", float(r[k]),
                        "baseline_second_best_summary.csv",
                        f"row setting {r.setting}, mech {r.mech}, {r.deviation}")
    sbb = load(D, "baseline_second_best_baitswitch.csv")
    if sbb is not None:
        body.append("\n\nAgainst a bait and switch, which is what the "
                    "no-reallocation behaviour exposes:\n\n"
                    + sbb.round(4).to_markdown(index=False))
        for _, r in sbb.iterrows():
            for k in ("detection_delay", "post_fire_revenue_per_round",
                      "undelegated_fraction", "revenue_per_round"):
                if pd.notna(r[k]):
                    chk(f"sbbait_{r.setting}_{r.mech}_{k}", float(r[k]),
                        "baseline_second_best_baitswitch.csv",
                        f"row setting {r.setting}, mech {r.mech}")

    # ---------------- monitor ladder -------------------------------------- #
    mf = load(D, "monitor_frontier.csv")
    if mf is not None:
        for al, s2 in mf.groupby("alpha"):
            body.append(f"\n## 13b. Monitor FRONTIER at alpha = {al}: false conviction of a "
                        f"compliant winner against detection delay\n\n"
                        + s2.round(4).to_markdown(index=False))
            for _, r in s2.iterrows():
                tag = (f"{al}_{r.monitor}_"
                       + str(r.params).replace(" ", "").replace("{", "").replace("}", "")
                       .replace(chr(34), "").replace(":", "").replace(",", "_"))
                chk(f"front_fc_{tag}", float(r.false_conviction_rate),
                    "monitor_frontier.csv", f"alpha {al}, {r.monitor} {r.params}, "
                    "false_conviction_rate")
                if pd.notna(r.median_delay_baitswitch):
                    chk(f"front_delay_{tag}", float(r.median_delay_baitswitch),
                        "monitor_frontier.csv", f"alpha {al}, {r.monitor} {r.params}, "
                        "median_delay_baitswitch", "{:.1f}")

    ml = load(D, "monitor_ladder.csv")
    if ml is not None:
        for al in sorted(ml.alpha.unique()):
            s = ml[ml.alpha == al]
            piv = s.pivot_table(index=["monitor", "params"], columns="primary_behaviour",
                                values=["conviction_rate", "median_delay"])
            body.append(f"\n## 13. Monitor ladder, alpha = {al}\n\n" + piv.round(3).to_markdown())
        a50 = ml[ml.alpha == "a0.50"]
        for mon, par in a50[["monitor", "params"]].drop_duplicates().itertuples(index=False):
            s = a50[(a50.monitor == mon) & (a50.params == par)]
            c = s[s.primary_behaviour == "compliant"]
            b = s[s.primary_behaviour == "baitswitch"]
            tag = f"{mon}_{par.replace(' ', '').replace('{', '').replace('}', '').replace(chr(34), '')}"
            if len(c):
                chk(f"ladder_falseconv_{tag}", float(c.conviction_rate.iloc[0]),
                    "monitor_ladder.csv", f"alpha a0.50, monitor {mon}, params {par}, compliant")
            if len(b):
                chk(f"ladder_delay_{tag}", float(b.median_delay.iloc[0]),
                    "monitor_ladder.csv", f"alpha a0.50, monitor {mon}, params {par}, baitswitch",
                    "{:.1f}")

    # ---------------- write ------------------------------------------------ #
    head = ["# TABLES, package A4\n",
            "Regenerate with, from the repository root:\n",
            "```\n$VENV/bin/python audit/round2/A4/scripts/make_tables.py \\\n"
            "    --csv experiments/data/A4 --out audit/round2/A4/TABLES.md\n```\n",
            "No compute and no scratch access is needed: every number below is read "
            "from the aggregated CSVs committed in `experiments/data/A4/`.\n",
            "\n## CHECKS: every scalar quoted in REPORT.md, recomputed\n",
            "| name | value | source CSV | expression |",
            "|---|---|---|---|"]
    for n_, val, src, expr in CHECKS:
        head.append(f"| `{n_}` | {val} | `{src}` | `{expr}` |")
    head.append("")
    with open(a.out, "w") as fh:
        fh.write("\n".join(head) + "\n" + "\n".join(body) + "\n")
    print(f"{len(CHECKS)} checks, {len(body)} tables -> {a.out}")


if __name__ == "__main__":
    main()
