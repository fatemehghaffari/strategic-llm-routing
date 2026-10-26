"""Turn the raw per-shard Slurm output into the AGGREGATED CSVs that every
number and every figure in package A4 is built from.

Raw per-shard output stays in scratch.  Everything this script writes goes to
experiments/data/A4/ in the repository, so a figure can be restyled and
regenerated with no compute and no access to scratch.
"""
import argparse
import glob
import os

import numpy as np
import pandas as pd
from scipy import stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    # ---- headline grid ---------------------------------------------------- #
    fs = sorted(glob.glob(os.path.join(a.raw, "headline_*.csv")))
    if fs:
        h = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        h = h.sort_values(["family_set", "triple", "alpha", "mech", "world",
                           "deviation", "deviator"], na_position="first")
        h.to_csv(os.path.join(a.out, "headline_runs.csv"), index=False)
        print("headline_runs.csv", h.shape, "from", len(fs), "shards")

        # worlds table: one row per (config, mech, world)
        w = h[h.world != "deviation"].copy()
        w.to_csv(os.path.join(a.out, "headline_worlds.csv"), index=False)

        # exploitability: the best single deviation at the proposed profile
        d = h[h.world == "deviation"].copy()
        best = (d.sort_values("gain_per_round")
                 .groupby(["family_set", "triple", "alpha", "mech"], as_index=False)
                 .last())
        best = best[["family_set", "triple", "alpha", "mech", "models",
                     "deviator", "deviation", "gain_per_round",
                     "revenue_per_round", "oracle", "second_cap", "honest_bench"]]
        best = best.rename(columns={"gain_per_round": "best_gain_per_round",
                                    "revenue_per_round": "revenue_at_best_deviation"})
        best.to_csv(os.path.join(a.out, "exploitability.csv"), index=False)
        print("exploitability.csv", best.shape)

        # the headline: non-strategic vs strategic revenue, per mechanism
        piv = (w.pivot_table(index=["family_set", "triple", "alpha", "mech"],
                             columns="world", values="revenue_per_round")
                .reset_index())
        ben = (w[w.world == "nonstrategic"]
               .set_index(["family_set", "triple", "alpha", "mech"])
               [["oracle", "second_cap", "honest_bench"]])
        piv = piv.join(ben, on=["family_set", "triple", "alpha", "mech"])
        piv["degradation"] = piv["nonstrategic"] - piv["strategic"]
        piv["degradation_rel"] = piv["degradation"] / piv["nonstrategic"].replace(0, np.nan)
        piv.to_csv(os.path.join(a.out, "headline_summary.csv"), index=False)
        print("headline_summary.csv", piv.shape)

        # which provider shades in the strategic profile, and how much revenue
        # that costs: the "loser's elicitation effort is unpinned" effect
        st = w[w.world == "strategic"].copy()
        pr = (w[w.world == "proposed"]
              .set_index(["family_set", "triple", "alpha", "mech"])["revenue_per_round"])
        st["revenue_at_proposed"] = st.set_index(
            ["family_set", "triple", "alpha", "mech"]).index.map(pr)
        st["revenue_drop_vs_proposed"] = st["revenue_at_proposed"] - st["revenue_per_round"]
        st["n_shading_agents"] = st["profile"].apply(
            lambda s: sum(1 for o in s.split("|") if o.startswith("theta")
                          and float(o[5:]) < 1.0))
        st[["family_set", "triple", "alpha", "mech", "models", "honest_agent",
            "profile", "is_fixed_point", "br_sweeps", "n_shading_agents",
            "revenue_per_round", "revenue_at_proposed", "revenue_drop_vs_proposed",
            "oracle", "second_cap", "honest_bench"]].to_csv(
            os.path.join(a.out, "strategic_profiles.csv"), index=False)

    # ---- flip regression -------------------------------------------------- #
    fs = sorted(glob.glob(os.path.join(a.raw, "flipreg_*.csv")))
    if fs:
        fr = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        tri3 = pd.read_csv(os.path.join(a.out, "triples_Q3.csv"))[["models", "flip_rate"]]
        tri7 = pd.read_csv(os.path.join(a.out, "triples_Q7.csv"))[["models", "flip_rate"]]
        tri3["context_set"], tri7["context_set"] = "Q3", "Q7"
        tri = pd.concat([tri3, tri7], ignore_index=True)
        ana = pd.read_csv(os.path.join(a.out, "analytic_gap_triples.csv"))
        ana = ana[~ana.uniform_mass][["models", "context_set", "gap"]]
        ana = ana.rename(columns={"gap": "analytic_gap"})
        fr = fr.merge(tri, on=["models", "context_set"]).merge(
            ana, on=["models", "context_set"])
        fr = fr.sort_values(["context_set", "flip_rate", "models"])
        fr.to_csv(os.path.join(a.out, "flip_regression.csv"), index=False)
        rows = []
        for cs, sub in fr.groupby("context_set"):
            sp = stats.spearmanr(sub.flip_rate, sub.sim_gap)
            sl = stats.linregress(sub.flip_rate, sub.sim_gap)
            ana_sp = stats.spearmanr(sub.analytic_gap, sub.sim_gap)
            rows.append({"context_set": cs, "n_triples": len(sub),
                         "spearman_rho_flip_vs_simgap": sp.statistic,
                         "spearman_p": sp.pvalue,
                         "ols_slope": sl.slope, "ols_intercept": sl.intercept,
                         "ols_r2": sl.rvalue ** 2,
                         "spearman_analytic_vs_sim": ana_sp.statistic,
                         "mean_sim_gap": float(sub.sim_gap.mean()),
                         "mean_analytic_gap": float(sub.analytic_gap.mean()),
                         "max_sim_gap": float(sub.sim_gap.max()),
                         "min_sim_gap": float(sub.sim_gap.min()),
                         "frac_sim_gap_positive": float((sub.sim_gap > 0).mean())})
        pd.DataFrame(rows).to_csv(os.path.join(a.out, "flip_regression_summary.csv"),
                                  index=False)
        print("flip_regression.csv", fr.shape)

    # ---------------- fine shading against the routers ---------------------- #
    fs = sorted(glob.glob(os.path.join(a.raw, "fineshade_*.csv")))
    if fs:
        fd = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        fd = fd.sort_values(["context_set", "triple", "alpha", "mech", "deviator",
                             "deviation_kind", "deviation_param"])
        fd.to_csv(os.path.join(a.out, "fine_shading.csv"), index=False)
        best = (fd.sort_values("gain_per_round")
                  .groupby(["context_set", "triple", "alpha", "mech"], as_index=False)
                  .last())
        best = best[["context_set", "triple", "alpha", "mech", "models", "deviator",
                     "deviation_kind", "deviation_param", "gain_per_round",
                     "baseline_revenue_per_round", "revenue_per_round",
                     "revenue_loss_per_round", "oracle", "second_cap", "honest_bench",
                     "compliant_convictions"]]
        best.to_csv(os.path.join(a.out, "fine_shading_best.csv"), index=False)

        # LIKE FOR LIKE: the SAME deviation (undercut the pointwise runner-up)
        # applied to every rule, which is the comparison that isolates what the
        # mechanism buys
        u = fd[fd.deviation_kind == "undercut"]
        ub = (u.sort_values("gain_per_round")
                .groupby(["triple", "alpha", "mech"], as_index=False).last())
        ub.to_csv(os.path.join(a.out, "undercut_comparison.csv"), index=False)
        us = ub.groupby("mech").agg(
            mean_gain=("gain_per_round", "mean"), max_gain=("gain_per_round", "max"),
            mean_revenue_loss=("revenue_loss_per_round", "mean"),
            max_revenue_loss=("revenue_loss_per_round", "max"),
            mean_revenue_after=("revenue_per_round", "mean"),
            mean_revenue_before=("baseline_revenue_per_round", "mean"),
            n_cells=("gain_per_round", "size")).reset_index()
        us.to_csv(os.path.join(a.out, "undercut_summary.csv"), index=False)
        print("fine_shading.csv", fd.shape, "best", best.shape,
              "undercut cells", ub.shape)


    # ---- the FAIR strategic comparison (rich option class) ----------------- #
    fs = sorted(glob.glob(os.path.join(a.raw, "richbr_*.csv")))
    if fs:
        rb = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        rb = rb.sort_values(["context_set", "triple", "alpha", "mech"])
        rb.to_csv(os.path.join(a.out, "rich_br.csv"), index=False)
        rb.groupby("mech").agg(
            n_cells=("mech", "size"),
            nonstrategic=("nonstrategic_revenue", "mean"),
            strategic=("strategic_revenue", "mean"),
            degradation=("degradation", "mean"),
            worst_degradation=("degradation", "max"),
            frac_fixed_point=("is_fixed_point", "mean")).reset_index().to_csv(
            os.path.join(a.out, "rich_br_summary.csv"), index=False)
        print("rich_br.csv", rb.shape)

    # ---- BASELINE 1: the single-observation exclusion rule ------------------ #
    fs = sorted(glob.glob(os.path.join(a.raw, "baselines*.csv")))
    if fs:
        bl = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        bl["empty_policy"] = bl["empty_policy"].fillna("na")
        bl.to_csv(os.path.join(a.out, "baseline_single_observation.csv"), index=False)
        pr = bl[bl.deviation == "proposed"]
        pr.groupby(["rule", "L_elicit", "empty_policy"]).agg(
            n_cells=("rule", "size"),
            revenue_per_round=("revenue_per_round", "mean"),
            compliant_exclusions=("compliant_exclusions", "mean"),
            exclusions=("exclusions", "mean"),
            idle_fraction=("idle_fraction", "mean"),
            price_is_one_share=("price_is_one_share", "mean"),
            price_is_zero_share=("price_is_zero_share", "mean"),
            second_cap=("second_cap", "mean"),
            honest_bench=("honest_bench", "mean")).reset_index().to_csv(
            os.path.join(a.out, "baseline_single_observation_summary.csv"), index=False)
        dev = bl[bl.deviation != "proposed"].copy()
        if len(dev):
            base_u = {}
            for _, r in pr.iterrows():
                for j in range(3):
                    base_u[(r.triple, r.alpha, r.rule, r.L_elicit, r.empty_policy,
                            j)] = r.get(f"util_{j}", np.nan)
            dev["gain_per_round"] = [
                r.get(f"util_{int(r.deviator_index)}", np.nan)
                - base_u.get((r.triple, r.alpha, r.rule, r.L_elicit, r.empty_policy,
                              int(r.deviator_index)), np.nan)
                for _, r in dev.iterrows()]
            (dev.sort_values("gain_per_round")
                .groupby(["triple", "alpha", "rule", "L_elicit", "empty_policy"],
                         as_index=False).last()).to_csv(
                os.path.join(a.out, "baseline_single_observation_exploit.csv"),
                index=False)
        print("baseline_single_observation.csv", bl.shape)

    # ---- utility against effort -------------------------------------------- #
    # utilwin_* is listed FIRST: it carries the win-probability series and the
    # higher seed count, and drop_duplicates keeps the first occurrence.
    fs = (sorted(glob.glob(os.path.join(a.raw, "utilwin_*.csv")))
          + sorted(glob.glob(os.path.join(a.raw, "utilcurves_*.csv")))
          + sorted(glob.glob(os.path.join(a.raw, "utilfast_*.csv"))))
    if fs:
        uc = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        # The focused companion job repeats some cells of the full grid job.
        # The repeats agree exactly, so they are redundant rather than
        # conflicting, but they must not be left in: a reader who sorts the
        # file by delivered_mean without splitting on `sweep` sees two
        # different series interleaved and reads it as a bimodal curve.
        key = ["instance", "context", "sweep", "role", "rule", "delivered_mean",
               "crosscheck_option"]
        key = [c for c in key if c in uc.columns]
        before = len(uc)
        uc = uc.drop_duplicates(subset=key, keep="first")
        # a single unambiguous series identifier, so no figure or reader can
        # accidentally merge two series that share a delivered-mean grid
        uc["series_id"] = (uc.instance + " | " + uc.context + " | sweep=" + uc.sweep
                           + " | " + uc.role + " | " + uc.rule)
        uc = uc.sort_values(["series_id", "delivered_mean"])
        uc.to_csv(os.path.join(a.out, "utility_curves.csv"), index=False)
        print(f"  utility_curves: dropped {before - len(uc)} duplicate rows")
        # one file per sweep as well, so the two can never be confused
        for sw, gsw in uc[uc.sweep != "crosscheck"].groupby("sweep"):
            gsw.to_csv(os.path.join(a.out, f"utility_curves_{sw}.csv"), index=False)
        cur = uc[uc.sweep != "crosscheck"]
        rows = []
        for k, g in cur.groupby(["instance", "context", "sweep", "role", "rule"]):
            g = g.sort_values("delivered_mean")
            u = g.agent_utility_per_round.values
            m = g.delivered_mean.values
            pk = int(np.argmax(u))
            rows.append({
                "instance": k[0], "context": k[1], "sweep": k[2], "role": k[3],
                "rule": k[4], "agent": g.agent.iloc[0],
                "own_capability": g.own_capability.iloc[0],
                "own_intrinsic": g.own_intrinsic.iloc[0],
                "runner_up_capability": g.runner_up_capability.iloc[0],
                "announced_price": g.announced_price_mean.iloc[0],
                "peak_delivered_mean": float(m[pk]),
                "peak_utility": float(u[pk]),
                "utility_at_full_capability": float(u[-1]),
                "peak_minus_full_capability": float(u[pk] - u[-1]),
                "total_variation": float(np.abs(np.diff(u)).sum()),
                "range": float(u.max() - u.min()), "n_grid": len(u)})
        smo = []
        for k, g in cur.groupby(["instance", "context", "sweep", "role", "rule"]):
            g = g.sort_values("delivered_mean")
            u = g.agent_utility_per_round.values
            se = g.agent_utility_sd.values / np.sqrt(int(g.nseeds.iloc[0]))
            d1 = np.abs(np.diff(u))
            smo.append({"instance": k[0], "context": k[1], "sweep": k[2],
                        "role": k[3], "rule": k[4], "n_grid": len(u),
                        "mean_abs_step": float(d1.mean()),
                        "max_abs_step": float(d1.max()),
                        "mean_standard_error": float(se.mean()),
                        "step_tolerance": float(max(2 * se.mean(), 0.01)),
                        "smooth": bool(d1.max() <= max(2 * se.mean(), 0.01) + 1e-9)})
        pd.DataFrame(smo).to_csv(
            os.path.join(a.out, "utility_curves_smoothness.csv"), index=False)
        pd.DataFrame(rows).to_csv(
            os.path.join(a.out, "utility_curves_summary.csv"), index=False)
        cc = uc[uc.sweep == "crosscheck"]
        if len(cc):
            cc.to_csv(os.path.join(a.out, "utility_curves_crosscheck.csv"), index=False)
        print("utility_curves.csv", uc.shape)


    # ---- the capability-gap sweep ------------------------------------------ #
    fs = sorted(glob.glob(os.path.join(a.raw, "gapsweep_*.csv")))
    if fs:
        gp = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        gp = gp.sort_values(["mech", "delta"])
        gp.to_csv(os.path.join(a.out, "capability_gap_sweep.csv"), index=False)
        keep = ["mech", "delta", "s_n", "sd_of_bid_difference",
                "equilibrium_revenue", "revenue_at_proposed", "announced_price_mean",
                "runner_up_curve_total_variation", "second_cap", "honest_bench",
                "oracle", "equilibrium_profile", "is_fixed_point"]
        gp[keep].to_csv(os.path.join(a.out, "capability_gap_summary.csv"), index=False)
        print("capability_gap_sweep.csv", gp.shape)


    # ---- BASELINE 3: the second-best utility guarantee mechanism ----------- #
    fs = (sorted(glob.glob(os.path.join(a.raw, "secondbest_*.csv")))
          + sorted(glob.glob(os.path.join(a.raw, "secondbestgen_*.csv"))))
    if fs:
        sb = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        sb = sb.sort_values(["setting", "triple", "alpha", "context", "mech",
                             "deviation"])
        sb.to_csv(os.path.join(a.out, "baseline_second_best.csv"), index=False)
        if "gate_blind2" not in sb.columns:
            sb["gate_blind2"] = True
        head = sb[sb.deviation.isin(["proposed", "their_equilibrium"])
                  & (sb.gate_blind2 != False)]
        # MATCHED CELL SETS. A head-to-head averaged over different instances
        # per mechanism is not a comparison; that error put both routers above
        # the oracle in figure 3 once and it is structurally excluded here.
        # Only cells carrying EVERY mechanism of their setting are summarised,
        # and the count that survives is reported so partial coverage is
        # visible rather than silent.
        cellkey = ["setting", "triple", "alpha", "context"]
        keep = []
        for st, gst in head.groupby("setting"):
            want = set(gst.mech.unique())
            for _, gc in gst.groupby(cellkey):
                if set(gc.mech.unique()) >= want:
                    keep.append(gc)
        matched = (pd.concat(keep, ignore_index=True) if keep
                   else head.iloc[0:0].copy())
        head_all, head = head, matched
        head_all.to_csv(os.path.join(a.out,
                                     "baseline_second_best_allcells.csv"), index=False)
        print(f"  second-best head-to-head: {len(head)} of {len(head_all)} rows "
              f"are on cells carrying every mechanism")
        if "gate_blind2" not in sb.columns:
            sb["gate_blind2"] = True
        g = head.groupby(["setting", "mech", "deviation"]).agg(
            n_cells=("mech", "size"),
            revenue_per_round=("revenue_per_round", "mean"),
            monitor_fire_rate=("monitor_fire_rate", "mean"),
            compliant_conviction_rate=("compliant_conviction_rate", "mean"),
            undelegated_fraction=("undelegated_fraction", "mean"),
            post_fire_revenue_per_round=("post_fire_revenue_per_round", "mean"),
            detection_delay=("detection_delay", "mean"),
            price_above_cap_mass=("price_above_cap_mass", "mean"),
            second_cap=("second_cap", "mean"),
            honest_bench=("honest_bench", "mean")).reset_index()
        g.to_csv(os.path.join(a.out, "baseline_second_best_summary.csv"), index=False)
        # detection delay and post-fire revenue against a bait and switch, which
        # is the row the no-reallocation behaviour exists to expose
        bs = sb[sb.deviation == "baitswitch"]
        if len(bs):
            bs.groupby(["setting", "mech", "gate_blind2"]).agg(
                n_cells=("mech", "size"),
                revenue_per_round=("revenue_per_round", "mean"),
                monitor_fire_rate=("monitor_fire_rate", "mean"),
                detection_delay=("detection_delay", "mean"),
                post_fire_revenue_per_round=("post_fire_revenue_per_round", "mean"),
                undelegated_fraction=("undelegated_fraction", "mean")).reset_index(
                ).to_csv(os.path.join(a.out, "baseline_second_best_baitswitch.csv"),
                         index=False)
        print("baseline_second_best.csv", sb.shape)


    # ---- monitor ladder --------------------------------------------------- #
    fs = sorted(glob.glob(os.path.join(a.raw, "monitor_ladder*.csv")))
    if fs:
        ml = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        # later shards supersede earlier ones for the same cell (the ladder was
        # rerun with a longer wall clock and with extra rungs)
        ml = (ml.sort_values("reps")
                .drop_duplicates(subset=["alpha", "primary_behaviour", "monitor",
                                         "params"], keep="last")
                .sort_values(["alpha", "primary_behaviour", "monitor", "params"]))
        ml.to_csv(os.path.join(a.out, "monitor_ladder.csv"), index=False)
        print("monitor_ladder.csv", ml.shape, "from", len(fs), "shards")

        # the FRONTIER: false conviction of a compliant winner against
        # detection delay, matched rung by rung.  Comparing delays without
        # matching the false conviction rate is meaningless, because any
        # monitor can be made fast by making it trigger-happy.
        front = []
        for al, s2 in ml.groupby("alpha"):
            key = ["monitor", "params"]
            c = s2[s2.primary_behaviour == "compliant"]
            if not len(c):
                continue
            fc = c.set_index(key)["conviction_rate"].rename("false_conviction_rate")
            b = s2[s2.primary_behaviour == "baitswitch"].set_index(key)[
                ["conviction_rate", "median_delay", "p90_delay"]]
            b.columns = ["detect_rate_baitswitch", "median_delay_baitswitch",
                         "p90_delay_baitswitch"]
            m = s2[s2.primary_behaviour == "baitswitch_mild"].set_index(key)[
                ["conviction_rate", "median_delay"]]
            m.columns = ["detect_rate_mild", "median_delay_mild"]
            t = pd.concat([fc, b, m], axis=1).reset_index()
            t["alpha"] = al
            t["reps"] = int(s2.reps.iloc[0])
            t["n"] = int(s2.n.iloc[0])
            front.append(t)
        # the constant-shading deviators: the half of the fixed-buffer trade-off
        # that a floored deviator cannot test
        sh = ml[ml.primary_behaviour.str.startswith("shade")]
        if len(sh):
            sh.pivot_table(index=["monitor", "params"],
                           columns="primary_behaviour",
                           values=["conviction_rate", "median_delay"]).to_csv(
                os.path.join(a.out, "monitor_constant_shading.csv"))
            print("monitor_constant_shading.csv", sh.shape)
        if front:
            ft = pd.concat(front, ignore_index=True).sort_values(
                ["alpha", "false_conviction_rate", "median_delay_baitswitch"])
            ft.to_csv(os.path.join(a.out, "monitor_frontier.csv"), index=False)
            print("monitor_frontier.csv", ft.shape)

    # ---- horizon sweep ---------------------------------------------------- #
    fs = sorted(glob.glob(os.path.join(a.raw, "horizon_*.csv")))
    if fs:
        hz = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        hz = hz.sort_values(["context_set", "models", "n"])
        hz.to_csv(os.path.join(a.out, "horizon_sweep.csv"), index=False)
        print("horizon_sweep.csv", hz.shape)
    fs = sorted(glob.glob(os.path.join(a.raw, "horizall_*.csv")))
    if fs:
        hz = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
        tri = pd.read_csv(os.path.join(a.out, "triples_Q3.csv"))[["models", "flip_rate"]]
        hz = hz.merge(tri, on="models", how="left").sort_values(["flip_rate", "models"])
        hz.to_csv(os.path.join(a.out, "horizon_all_triples.csv"), index=False)
        sp = stats.spearmanr(hz.flip_rate, hz.sim_gap)
        sl = stats.linregress(hz.flip_rate, hz.sim_gap)
        pd.DataFrame([{"n": int(hz.n.iloc[0]), "n_triples": len(hz),
                       "spearman_rho_flip_vs_simgap": sp.statistic,
                       "spearman_p": sp.pvalue, "ols_slope": sl.slope,
                       "ols_intercept": sl.intercept, "ols_r2": sl.rvalue ** 2,
                       "mean_sim_gap": float(hz.sim_gap.mean()),
                       "frac_sim_gap_positive": float((hz.sim_gap > 0).mean()),
                       "mean_compconv_scalar": float(hz.compconv_mesp_scalar.mean()),
                       "mean_compconv_contextual": float(hz.compconv_plmesp.mean()),
                       "frac_runs_scalar_price_above_cap":
                           float((hz.priceabovecap_mesp_scalar > 0).mean()),
                       "spearman_flip_vs_compconv_scalar":
                           stats.spearmanr(hz.flip_rate,
                                           hz.compconv_mesp_scalar).statistic,
                       "spearman_flip_vs_compconv_scalar_p":
                           stats.spearmanr(hz.flip_rate,
                                           hz.compconv_mesp_scalar).pvalue}]).to_csv(
            os.path.join(a.out, "horizon_all_summary.csv"), index=False)
        print("horizon_all_triples.csv", hz.shape)


if __name__ == "__main__":
    main()
