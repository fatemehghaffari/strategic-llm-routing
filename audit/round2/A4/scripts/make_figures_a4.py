"""Figures for package A4.  Reads ONLY the aggregated CSVs in experiments/data/A4/.

    python make_figures_a4.py --csv experiments/data/A4 --out <dir>

An aesthetic change costs seconds and needs no compute and no scratch access.

Palette: categorical slots 1-5 of the project's validated light-mode palette
(blue, orange, aqua, yellow, violet); adjacent-pair CVD separation was checked
with the validator (worst adjacent pair deltaE 9.1 protan, 22.9 normal, all
checks PASS).  Contrast of aqua and yellow against the surface is below 3:1, so
every series is DIRECTLY LABELLED and the underlying table is committed as CSV,
which is the required relief.
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7"]
INK, INK2, MUTED = "#1b1b1b", "#4a4a4a", "#8a8a8a"
GRID = "#e3e3e0"
ORDER = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8, length=3, width=0.8)
    ax.grid(True, axis="y", color=GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)




def check_reference_lines(name, values, oracle, honest=None, tol=1e-9):
    """Guard: a rule that allocates cannot beat the pointwise-best oracle.

    Every delivered mean is at most the selected provider's capability, which
    is at most the pointwise maximum, so measured revenue can never exceed the
    oracle computed ON THE SAME CELLS.  If it does, the reference line and the
    points have been aggregated over different instances.  That happened once,
    in figure 3, and this function exists so that it fails loudly rather than
    shipping.  `values` maps a series label to its plotted value.
    """
    bad = {k: v for k, v in values.items() if v > oracle + tol}
    if bad:
        raise AssertionError(
            f"{name}: {bad} exceed the oracle {oracle:.4f}. The reference line "
            f"and the points are not on the same cell set.")
    if honest is not None:
        low = {k: v for k, v in values.items() if v < honest - tol}
        if low:
            print(f"  note [{name}]: {low} sit below the honest benchmark "
                  f"{honest:.4f}; see REPORT.md for why this is expected under "
                  f"strategic play at a finite horizon.")
    return True


def fig_capabilities(csvdir, out):
    """F1: the premise, measured.  Which provider is best depends on the task."""
    cap = pd.read_csv(os.path.join(csvdir, "capabilities_finite_5shot.csv"))
    t = cap.pivot(index="model", columns="context", values="M")[ORDER]
    summ = pd.read_csv(os.path.join(csvdir, "flips_summary_5shot.csv")).iloc[0]
    fig, ax = plt.subplots(figsize=(6.6, 3.6), dpi=200)
    style(ax)
    x = np.arange(len(ORDER))
    best = t.idxmax(axis=0)
    hi = sorted(set(best.values))
    for m in t.index:
        on = m in hi
        ax.plot(x, t.loc[m].values, lw=2.0 if on else 1.0,
                color=CAT[hi.index(m)] if on else MUTED,
                alpha=1.0 if on else 0.45, zorder=3 if on else 2,
                marker="o" if on else None, ms=4.5,
                markeredgecolor="white", markeredgewidth=0.8)
    # direct labels, de-overlapped: every series is named, which is the relief
    # the contrast check requires
    ends = t.iloc[:, -1].sort_values()
    lo, hi_y = float(t.values.min()), float(t.values.max())
    step = (hi_y - lo) * 0.048
    ypos, last = {}, -1e9
    for m, v in ends.items():
        y = max(float(v), last + step)
        ypos[m] = y
        last = y
    for m, y in ypos.items():
        on = m in hi
        ax.plot([x[-1] + 0.04, x[-1] + 0.22], [t.loc[m].values[-1], y],
                lw=0.5, color=GRID, zorder=1)
        ax.annotate(m, (x[-1] + 0.26, y), fontsize=6.5, va="center",
                    color=INK if on else MUTED,
                    fontweight="bold" if on else "normal")
    ax.set_xticks(x)
    ax.set_xticklabels(ORDER, fontsize=8)
    ax.set_xlim(-0.3, len(ORDER) + 1.6)
    ax.set_ylabel("measured capability $M_i(z)$", fontsize=8.5, color=INK2)
    ax.set_title("Measured capability of 11 LLMs on 7 benchmark families "
                 "(RouterBench, 5-shot)", fontsize=9.5, color=INK, loc="left")
    ax.text(0, -0.20,
            f"Rank flips between model pairs across context pairs: "
            f"{summ.raw_flip_rate:.1%} of {int(summ.raw_comparisons)} comparisons; "
            f"{summ.bonf_flip_rate:.1%} of the {int(summ.bonf_comparisons)} "
            f"Bonferroni-significant ones. Bold lines are the models that are "
            f"pointwise best somewhere.",
            transform=ax.transAxes, fontsize=6.6, color=MUTED, va="top", wrap=True)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "a4_fig1_capabilities.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(out, "a4_fig1_capabilities.png"), bbox_inches="tight")
    plt.close(fig)


LAB = {"plmesp": "PL-MESP\n(contextual)", "mesp_scalar": "MESP\n(scalar)",
       "router_greedy": "router\n(greedy)", "router_eps": "router\n(eps-greedy)",
       "router_ucb": "router\n(UCB)",
       "second_best": "second-best\n(WWW 2026,\nreimplemented)"}
ORDER_M = ["plmesp", "mesp_scalar", "second_best", "router_greedy", "router_eps",
           "router_ucb"]


def fig_two_worlds(csvdir, out, family_set="Q3", alpha="a0.50"):
    """F2, two panels.

    Left: revenue per round against non-strategic providers and against
    strategic ones, for every rule.  Right: what the SAME deviation, undercut
    the pointwise runner-up, costs each rule.  The two panels are the two
    halves of the comparison and neither should be read alone.
    """
    p1 = os.path.join(csvdir, "headline_summary.csv")
    p2 = os.path.join(csvdir, "undercut_summary.csv")
    if not os.path.exists(p1):
        print("headline_summary.csv missing; skipping figure 2")
        return
    d = pd.read_csv(p1)
    d = d[(d.family_set == family_set)] if (d.family_set == family_set).any() else d
    g = d.groupby("mech")[["nonstrategic", "strategic", "oracle", "second_cap",
                           "honest_bench"]].mean()
    order = [m for m in ORDER_M if m in g.index]
    g = g.loc[order]
    ncell = int(d.groupby(["family_set", "triple", "alpha"]).ngroups)

    have2 = os.path.exists(p2)
    fig, axes = plt.subplots(1, 2 if have2 else 1, figsize=(9.4 if have2 else 6.6, 3.6),
                             dpi=200, gridspec_kw={"width_ratios": [1.25, 1]} if have2 else None)
    ax = axes[0] if have2 else axes
    style(ax)
    check_reference_lines("figure 2a, non-strategic",
                          {m: float(g.loc[m, "nonstrategic"]) for m in order},
                          float(g["oracle"].mean()), float(g["honest_bench"].mean()))
    check_reference_lines("figure 2a, strategic",
                          {m: float(g.loc[m, "strategic"]) for m in order},
                          float(g["oracle"].mean()), float(g["honest_bench"].mean()))
    x = np.arange(len(order))
    w = 0.34
    b1 = ax.bar(x - w / 2 - 0.01, g["nonstrategic"], w, color=CAT[0],
                label="non-strategic providers", zorder=3)
    b2 = ax.bar(x + w / 2 + 0.01, g["strategic"], w, color=CAT[1],
                label="strategic providers", zorder=3)
    for bars in (b1, b2):
        for r in bars:
            ax.annotate(f"{r.get_height():.2f}",
                        (r.get_x() + r.get_width() / 2, r.get_height()),
                        ha="center", va="bottom", fontsize=6.2, color=INK2)
    for val, lab in ((g["oracle"].mean(), "oracle"),
                     (g["second_cap"].mean(), "second capability"),
                     (g["honest_bench"].mean(), "honest benchmark")):
        ax.axhline(val, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=2)
        ax.annotate(lab, (len(order) - 0.52, val), fontsize=6.2, color=MUTED, va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels([LAB[m] for m in order], fontsize=7.2)
    ax.set_ylabel("revenue per round", fontsize=8.5, color=INK2)
    ax.set_ylim(0, max(g[["nonstrategic", "strategic", "oracle"]].values.max() * 1.16, 0.1))
    ax.set_title("a. What strategic behaviour costs each rule", fontsize=9, color=INK,
                 loc="left")
    ax.legend(frameon=False, fontsize=7.2, loc="upper center",
              bbox_to_anchor=(0.5, -0.19), ncol=2)

    if have2:
        u = pd.read_csv(p2).set_index("mech")
        o2 = [m for m in ORDER_M if m in u.index]
        u = u.loc[o2]
        ax2 = axes[1]
        style(ax2)
        x2 = np.arange(len(o2))
        bars = ax2.bar(x2, u["mean_revenue_loss"], 0.5, color=CAT[2], zorder=3)
        ax2.errorbar(x2, u["mean_revenue_loss"],
                     yerr=[np.zeros(len(o2)),
                           (u["max_revenue_loss"] - u["mean_revenue_loss"]).values],
                     fmt="none", ecolor=INK2, elinewidth=0.9, capsize=3, zorder=4)
        for r, m in zip(bars, o2):
            ax2.annotate(f"{r.get_height():.3f}",
                         (r.get_x() + r.get_width() / 2, r.get_height()),
                         ha="center", va="bottom", fontsize=6.2, color=INK2)
        ax2.set_xticks(x2)
        ax2.set_xticklabels([LAB[m] for m in o2], fontsize=7.2)
        ax2.set_ylabel("revenue lost per round", fontsize=8.5, color=INK2)
        ax2.set_title("b. Cost of ONE deviation: undercut the runner-up",
                      fontsize=9, color=INK, loc="left")
        ax2.annotate("mean over cells; whisker reaches the worst cell",
                     (0, -0.30), xycoords="axes fraction", fontsize=6.4, color=MUTED)

    fig.suptitle(f"Calibrated simulation on measured RouterBench capabilities: "
                 f"context set {family_set}, {ncell} instance cells, n = 300,000",
                 fontsize=9.8, color=INK, x=0.012, ha="left", y=1.04)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "a4_fig2_two_worlds.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(out, "a4_fig2_two_worlds.png"), bbox_inches="tight")
    plt.close(fig)




def fig_complementarity(csvdir, out):
    """F1b, in FrugalGPT's Fig. 4 grammar: a pairwise complementarity matrix.

    Cell (row, col) is the share of queries on which the ROW model is wrong and
    the COLUMN model is right.  Sequential single-hue ramp, light to dark, as a
    magnitude encoding must be.
    """
    p = os.path.join(csvdir, "complementarity.csv")
    if not os.path.exists(p):
        print("complementarity.csv missing; skipping figure 1b")
        return
    d = pd.read_csv(p)
    d = d[d.scope == "ALL"]
    m = d.pivot(index="row_model", columns="col_model", values="row_wrong_col_right")
    acc = d.groupby("row_model").row_accuracy.first()
    order = list(acc.sort_values(ascending=False).index)
    m = m.loc[order, order]
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list(
        "seq", ["#f2f6fb", "#c3d8f0", "#7fb0e0", "#3d84cd", "#1b4b86"])
    fig, ax = plt.subplots(figsize=(6.4, 5.2), dpi=200)
    im = ax.imshow(m.values * 100, cmap=cmap, vmin=0, vmax=float(m.values.max() * 100))
    ax.set_xticks(range(len(order)))
    ax.set_yticks(range(len(order)))
    ax.set_xticklabels(order, rotation=45, ha="right", fontsize=6.8, color=INK2)
    ax.set_yticklabels(order, fontsize=6.8, color=INK2)
    for i in range(len(order)):
        for j in range(len(order)):
            v = m.values[i, j] * 100
            ax.annotate(f"{v:.0f}" if i != j else "",
                        (j, i), ha="center", va="center", fontsize=6.0,
                        color="white" if v > 0.55 * m.values.max() * 100 else INK)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.set_label("per cent of queries", fontsize=7.5, color=INK2)
    cb.ax.tick_params(labelsize=6.5, colors=INK2, length=2)
    cb.outline.set_visible(False)
    ax.set_title("Row model wrong, column model right (RouterBench, 5-shot, "
                 "34,764 queries)", fontsize=9, color=INK, loc="left")
    ax.annotate("rows and columns ordered by overall accuracy; a query counts as "
                "correct at a published score of 0.5 or more",
                (0, -0.42), xycoords="axes fraction", fontsize=6.2, color=MUTED)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "a4_fig1b_complementarity.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(out, "a4_fig1b_complementarity.png"), bbox_inches="tight")
    plt.close(fig)


def fig_frontier(csvdir, out):
    """F3, in FrugalGPT Fig. 5's grammar with our axes: each rule is a POINT.

    x: what a single deviator can take per round, from the undercut comparison.
    y: platform revenue per round at the proposed profile.
    The routers sit up and to the right; the mechanisms down and to the left.
    """
    p = os.path.join(csvdir, "undercut_summary.csv")
    if not os.path.exists(p):
        print("undercut_summary.csv missing; skipping figure 3")
        return
    u = pd.read_csv(p).set_index("mech")
    # Reference lines MUST come from the same cells as the points.  They used
    # to be averaged over headline_summary.csv, which spans five context sets
    # and a different triple list, and that put both routers above the oracle.
    cmp_p = os.path.join(csvdir, "undercut_comparison.csv")
    ref = None
    if os.path.exists(cmp_p):
        c = pd.read_csv(cmp_p)
        ref = (float(c.oracle.mean()), float(c.honest_bench.mean()),
               float(c.second_cap.mean()))
        ncell = int(c.groupby(["triple", "alpha"]).ngroups)
    order = [m for m in ORDER_M if m in u.index]
    if ref:
        check_reference_lines("figure 3",
                              {m: float(u.loc[m, "mean_revenue_before"]) for m in order},
                              ref[0], ref[1])
    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=200)
    style(ax)
    ax.grid(True, axis="both", color=GRID, lw=0.7, zorder=0)
    if ref:
        for val, lab in ((ref[0], "oracle"), (ref[2], "second capability"),
                         (ref[1], "honest benchmark")):
            ax.axhline(val, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
            ax.annotate(lab, (1.0, val), xycoords=("axes fraction", "data"),
                        fontsize=6.4, color=MUTED, va="bottom", ha="right")
    for k, m in enumerate(order):
        x = float(u.loc[m, "max_gain"])
        y = float(u.loc[m, "mean_revenue_before"])
        col = CAT[k % len(CAT)]
        ax.errorbar([x], [y], xerr=[[x - float(u.loc[m, "mean_gain"])], [0]],
                    fmt="none", ecolor=col, elinewidth=1.0, capsize=3, zorder=3)
        ax.scatter([x], [y], s=70, color=col, edgecolor="white", linewidth=1.0,
                   zorder=4)
        # per-rule label placement: the two high-revenue routers sit close
        # together, so they are pushed to opposite sides with leader lines
        off, ha = {"plmesp": ((11, 7), "left"),
                   "mesp_scalar": ((11, -13), "left"),
                   "router_greedy": ((0, 15), "center"),
                   "router_eps": ((8, 15), "left"),
                   "router_ucb": ((7, -21), "left"),
                   }.get(m, ((9, 5), "left"))
        ax.annotate(LAB[m].replace("\n", " "), (x, y), textcoords="offset points",
                    xytext=off, fontsize=7.2, color=INK, ha=ha,
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.6,
                                    shrinkA=0, shrinkB=4)
                    if abs(off[1]) > 12 else None)
    ax.set_xlabel("what one deviator can take, per round (undercut the runner-up)",
                  fontsize=8.5, color=INK2)
    ax.set_ylabel("platform revenue per round", fontsize=8.5, color=INK2)
    ax.set_xlim(left=-0.006, right=float(u["max_gain"].max()) * 1.25)
    ax.set_title(f"Revenue against exposure: each rule is one point "
                 f"({ncell} instance cells)" if ref else
                 "Revenue against exposure: each rule is one point",
                 fontsize=9.5, color=INK, loc="left")
    ax.annotate("marker is the WORST cell, whisker reaches the mean over cells; "
                "reference lines are computed on the SAME cells as the points",
                (0, -0.20), xycoords="axes fraction", fontsize=6.4, color=MUTED)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "a4_fig3_frontier.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(out, "a4_fig3_frontier.png"), bbox_inches="tight")
    plt.close(fig)


def _predicted_turn_on(s):
    """Horizon at which 3 s_n + rho_n drops below the second-capability
    benchmark, which is when the announced price first becomes positive."""
    x = np.log10(s.n.values)
    y = (3 * s.s_n + s.rho_n - s.bench_M2_per_round).values
    for i in range(1, len(x)):
        if y[i - 1] > 0 >= y[i]:
            t = y[i - 1] / (y[i - 1] - y[i])
            return 10 ** (x[i - 1] + t * (x[i] - x[i - 1]))
    return np.nan


def fig_threshold(csvdir_a3, out):
    """F4, in the strategic line's own idiom: measurement with theory overlaid."""
    p = os.path.join(csvdir_a3, "threshold_summary.csv")
    if not os.path.exists(p):
        print("A3 threshold_summary.csv missing; skipping figure 4")
        return
    d = pd.read_csv(p)
    panels = [(1, [("C", 2), ("D", 3)]), (2, [("C", 2), ("D", 3)])]
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.7), dpi=200)
    for ax, (dd, series) in zip(axes, panels):
        style(ax)
        ax.set_xscale("log")
        ax2 = ax.twinx()
        for sp in ("top", "right"):
            ax2.spines[sp].set_visible(False)
        ax2.tick_params(colors=INK2, labelsize=8, length=3, width=0.8)
        preds = []
        for k, (inst, K) in enumerate(series):
            s = d[(d.d == dd) & (d.inst == inst) & (d.K == K)].sort_values("n")
            if not len(s):
                continue
            # K = 2 is drawn wide underneath and K = 3 narrow on top, so that
            # when they coincide, which is the point, both remain visible
            ax.plot(s.n, s.positive_price_share, lw=4.5 if k == 0 else 1.6,
                    color=CAT[k], alpha=0.55 if k == 0 else 1.0,
                    marker="o" if k else None, ms=3.0, markeredgecolor="white",
                    markeredgewidth=0.5, zorder=3 + k,
                    label=f"K = {K}: share of regions priced")
            ax2.plot(s.n, s.rev_per_round, lw=3.4 if k == 0 else 1.4,
                     ls="-" if k == 0 else (0, (4, 2)), color=CAT[k + 2],
                     alpha=0.55 if k == 0 else 1.0, zorder=2 + k,
                     label=f"K = {K}: revenue per round")
            mn = s.loc[s.rev_per_round.idxmin()]
            ax2.scatter([mn.n], [mn.rev_per_round], s=42, marker="v",
                        color=CAT[k + 2], edgecolor="white", linewidth=0.8, zorder=5)
            preds.append(_predicted_turn_on(s))
        pr = float(np.nanmean(preds)) if preds else np.nan
        if np.isfinite(pr):
            ax.axvline(pr, color=INK, lw=1.2, ls=(0, (2, 2)), zorder=2)
            ax.annotate(f"predicted turn-on\nn = {pr:.2g}", (pr, 1.02),
                        xycoords=("data", "axes fraction"), fontsize=6.6,
                        color=INK, ha="center", va="bottom")
        ax.set_ylim(-0.04, 1.08)
        ax.set_xlabel("horizon n (log scale)", fontsize=8.5, color=INK2)
        ax.set_ylabel("share of regions with a positive price", fontsize=8, color=INK2)
        ax2.set_ylabel("revenue per round", fontsize=8, color=INK2)
        ax.set_title(f"{'a' if dd == 1 else 'b'}. d = {dd}", fontsize=9, color=INK,
                     loc="left")
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=6.4,
                  loc="center left", bbox_to_anchor=(0.02, 0.62))
    axes[0].annotate("triangle marks the revenue minimum, which sits at the turn-on",
                     (0, -0.30), xycoords="axes fraction", fontsize=6.4, color=MUTED)
    fig.suptitle("The predicted threshold, drawn as a line, and the measurement "
                 "crossing it there", fontsize=9.8, color=INK, x=0.012, ha="left",
                 y=1.05)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "a4_fig4_threshold.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(out, "a4_fig4_threshold.png"), bbox_inches="tight")
    plt.close(fig)




RULE_LAB = {"mesp": "monitored second price", "router_greedy": "router (greedy)",
            "router_eps": "router (eps-greedy)", "router_ucb": "router (UCB)"}
RULE_ORDER = ["mesp", "router_ucb", "router_eps", "router_greedy"]


def fig_utility_curves(csvdir, out, sweep="primary", context=None):
    """F5: the mechanism from the AGENT's side.

    One provider's delivered mean on x, its OWN utility per round on y, one
    curve per rule, one panel per arm role.  The marks on the x axis are the
    announced price, the runner-up's capability and the provider's own
    capability, which is where each prediction is supposed to bite.
    """
    p = os.path.join(csvdir, "utility_curves.csv")
    if not os.path.exists(p):
        print("utility_curves.csv missing; skipping figure 5")
        return
    d = pd.read_csv(p)
    d = d[d.sweep.isin(["all", "primary"])]
    if context is None:
        context = sorted(d.context.unique())[0]
    for inst in sorted(d.instance.unique()):
        for sw in sorted(d.sweep.unique()):
            sub = d[(d.instance == inst) & (d.sweep == sw) & (d.context == context)]
            if not len(sub):
                continue
            roles = [r for r in ("top", "runner_up", "third")
                     if r in set(sub.role)]
            fig, axes = plt.subplots(1, len(roles), figsize=(3.4 * len(roles), 3.5),
                                     dpi=200, sharex=False)
            if len(roles) == 1:
                axes = [axes]
            for ax, role in zip(axes, roles):
                style(ax)
                g0 = sub[sub.role == role]
                rules = [r for r in RULE_ORDER if r in set(g0.rule)]
                axw = None
                for k, rule in enumerate(rules):
                    g = g0[g0.rule == rule].sort_values("delivered_mean")
                    ax.plot(g.delivered_mean, g.agent_utility_per_round, lw=2.0,
                            color=CAT[k], zorder=4 - k, label=RULE_LAB[rule])
                    pk = g.loc[g.agent_utility_per_round.idxmax()]
                    ax.scatter([pk.delivered_mean], [pk.agent_utility_per_round],
                               s=34, color=CAT[k], edgecolor="white", linewidth=0.9,
                               zorder=6)
                    # the win probability underneath, on its own right-hand
                    # axis: any step in the utility curve IS this event, and
                    # showing it stops a reader reading the step as noise
                    if "win_probability" in g and g.win_probability.notna().any():
                        if axw is None:
                            axw = ax.twinx()
                            axw.set_ylim(-0.03, 1.03)
                            for sp in ("top", "right"):
                                axw.spines[sp].set_visible(False)
                            axw.tick_params(colors=MUTED, labelsize=6.5, length=2)
                            axw.set_ylabel("probability this provider wins",
                                           fontsize=7, color=MUTED)
                        axw.plot(g.delivered_mean, g.win_probability, lw=1.1,
                                 ls=(0, (3, 2)), color=CAT[k], alpha=0.5, zorder=1)
                r0 = g0.iloc[0]
                marks = [(r0.announced_price_mean, "price", (0, (2, 2))),
                         (r0.runner_up_capability, "runner-up cap.", (0, (5, 2))),
                         (r0.own_capability, "own cap.", "-")]
                drawn = []
                for xv, lab, ls in marks:
                    if not np.isfinite(xv):
                        continue
                    same = [d2 for d2 in drawn if abs(d2[0] - xv) < 1e-9]
                    if same:                      # two marks coincide: merge labels
                        same[0][1] = same[0][1] + " = " + lab
                        continue
                    ax.axvline(xv, color=MUTED, lw=0.9, ls=ls, zorder=2)
                    drawn.append([xv, lab])
                for xv, lab in drawn:
                    ax.annotate(lab, (xv, 1.005), xycoords=("data", "axes fraction"),
                                fontsize=5.8, color=MUTED, rotation=90, va="bottom",
                                ha="center")
                ax.set_xlabel("delivered mean", fontsize=8, color=INK2)
                if ax is axes[0]:
                    ax.set_ylabel("this provider's utility per round", fontsize=8,
                                  color=INK2)
                ax.set_title(f"{role.replace('_', ' ')}: {r0.agent}", fontsize=8.5,
                             color=INK, loc="left")
            axes[0].legend(frameon=False, fontsize=6.6, loc="best")
            axes[0].annotate("solid: utility (left axis).  dashed: probability this "
                             "provider wins the elicitation (right axis)",
                             (0, -0.42), xycoords="axes fraction", fontsize=6.2,
                             color=MUTED)
            tag = "constructed two-top" if "CONSTRUCT" in inst else "measured, unique top"
            ns = sorted(set(int(v) for v in sub.nseeds.dropna().unique()))
            nstr = (f"{ns[0]} seeds" if len(ns) == 1
                    else f"{min(ns)} to {max(ns)} seeds by series")
            fig.suptitle(f"Utility against effort, {context}, {tag}, sweep = {sw} "
                         f"(calibrated simulation, n = {int(r0.n):,}, {nstr})",
                         fontsize=9.2, color=INK, x=0.012, ha="left", y=1.06)
            fig.tight_layout()
            nm = ("a4_fig5_utility_" + ("twotop" if "CONSTRUCT" in inst else "unique")
                  + f"_{sw}_{context}")
            fig.savefig(os.path.join(out, nm + ".pdf"), bbox_inches="tight")
            fig.savefig(os.path.join(out, nm + ".png"), bbox_inches="tight")
            plt.close(fig)




def fig_capability_gap(csvdir, out):
    """F6: is the two-top condition a cliff at zero or a transition at a scale?

    Equilibrium revenue against the constructed top-to-second capability gap,
    on a log gap axis, with the honest benchmark and the second capability as
    reference lines and BOTH candidate scales marked: the price shading s_n and
    the standard deviation of the bid difference. The runner-up's
    utility-curve total variation is drawn beneath, because that flatness is
    the indifference that causes the collapse.
    """
    p = os.path.join(csvdir, "capability_gap_summary.csv")
    if not os.path.exists(p):
        p = os.path.join(csvdir, "capability_gap_from_logs.csv")
    if not os.path.exists(p):
        print("capability gap CSV missing; skipping figure 6")
        return
    d = pd.read_csv(p).sort_values("delta")
    # the log-recovery file has no benchmark or scale columns; fill them from
    # the design constants and the instance, both of which are fixed here
    if "s_n" not in d.columns:
        d["s_n"] = 0.049406
        d["sd_of_bid_difference"] = 0.006835
        d["second_cap"] = 0.7541
        d["honest_bench"] = 0.4104
    for mech, g in d.groupby("mech"):
        g = g.sort_values("delta")
        if len(g) < 3:
            continue
        # a log axis cannot show delta = 0; it is drawn at half the smallest
        # positive delta and the tick is labelled 0
        pos = g[g.delta > 0]
        floor = float(pos.delta.min()) / 2 if len(pos) else 1e-4
        x = g.delta.where(g.delta > 0, floor).values
        fig, (ax, axb) = plt.subplots(2, 1, figsize=(6.6, 4.6), dpi=200,
                                      sharex=True, height_ratios=[2, 1])
        for A in (ax, axb):
            style(A)
            A.set_xscale("log")
        ax.plot(x, g.equilibrium_revenue, lw=2.2, color=CAT[0], marker="o", ms=4,
                markeredgecolor="white", markeredgewidth=0.7, zorder=4,
                label="equilibrium revenue")
        ax.plot(x, g.revenue_at_proposed, lw=1.4, ls=(0, (4, 2)), color=CAT[1],
                zorder=3, label="revenue at the proposed profile")
        # the benchmarks DEPEND on delta by construction, because the
        # runner-up's capability is M_top - delta, so they are curves and not
        # horizontal lines; drawing them flat would misplace them
        for col, lab in (("second_cap", "second capability"),
                         ("honest_bench", "honest benchmark")):
            if col not in g.columns:
                continue
            ax.plot(x, g[col], color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
            ax.annotate(lab, (x[-1], float(g[col].values[-1])),
                        fontsize=6.4, color=MUTED, va="bottom", ha="right")
        for val, lab, col in ((float(g.s_n.iloc[0]), "price shading  $s_n$", CAT[4]),
                              (float(g.sd_of_bid_difference.iloc[0]),
                               "s.d. of the bid difference", CAT[2])):
            for A in (ax, axb):
                A.axvline(val, color=col, lw=1.2, ls=(0, (2, 2)), zorder=2)
            ax.annotate(lab, (val, 1.01), xycoords=("data", "axes fraction"),
                        fontsize=6.4, color=col, ha="center", va="bottom")
        ax.set_ylabel("revenue per round", fontsize=8.5, color=INK2)
        ax.legend(frameon=False, fontsize=7, loc="lower left")
        axb.plot(x, g.runner_up_curve_total_variation, lw=2.0, color=CAT[3],
                 marker="o", ms=3.5, markeredgecolor="white", markeredgewidth=0.6,
                 zorder=4)
        axb.set_ylabel("runner-up curve\ntotal variation", fontsize=7.5, color=INK2)
        axb.set_xlabel("constructed top-to-second capability gap  $\\delta$  "
                       "(log scale; the leftmost point is $\\delta = 0$)",
                       fontsize=8.5, color=INK2)
        fig.suptitle(f"The two-top condition bites at the bid-noise scale, not at "
                     f"gap zero ({mech}, CONSTRUCTED instances, calibrated "
                     f"simulation, n = 300,000, 10 seeds)",
                     fontsize=9.2, color=INK, x=0.012, ha="left", y=1.02)
        fig.tight_layout()
        nm = f"a4_fig6_capability_gap_{mech}"
        fig.savefig(os.path.join(out, nm + ".pdf"), bbox_inches="tight")
        fig.savefig(os.path.join(out, nm + ".png"), bbox_inches="tight")
        plt.close(fig)




def fig_second_best(csvdir, out):
    """F7: what happens on the paths where the monitor fires.

    Their mechanism stops serving when its test fires; ours restarts
    adversarial learning over every provider. This draws that difference, with
    the compliant-conviction rate beside it, in both settings.

    LABELLING: their mechanism was never claimed for contextual settings and is
    correct in the setting it does claim. The contextual panel runs the
    strongest available scalar rule deliberately outside its stated scope in
    order to measure the cost of scalarness, and OUR OWN scalar mechanism is in
    the same panel for that reason.
    """
    p = os.path.join(csvdir, "baseline_second_best_summary.csv")
    pb = os.path.join(csvdir, "baseline_second_best_baitswitch.csv")
    if not os.path.exists(p):
        print("baseline_second_best_summary.csv missing; skipping figure 7")
        return
    d = pd.read_csv(p)
    bs = pd.read_csv(pb) if os.path.exists(pb) else None
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.7), dpi=200)

    # panel a: the fair head-to-head, scalar setting, revenue
    ax = axes[0]
    style(ax)
    g = d[(d.setting == "scalar") & (d.deviation == "proposed")].set_index("mech")
    order = [m for m in ORDER_M if m in g.index]
    x = np.arange(len(order))
    ax.bar(x, [float(g.loc[m, "revenue_per_round"]) for m in order], 0.5,
           color=[CAT[ORDER_M.index(m) % len(CAT)] for m in order], zorder=3)
    for k, m in enumerate(order):
        ax.annotate(f"{float(g.loc[m, 'revenue_per_round']):.3f}",
                    (k, float(g.loc[m, "revenue_per_round"])), ha="center",
                    va="bottom", fontsize=6.4, color=INK2)
    for col, lab in (("second_cap", "second capability"),
                     ("honest_bench", "honest benchmark")):
        v = float(g[col].mean())
        ax.axhline(v, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
        ax.annotate(lab, (0.02, v), xycoords=("axes fraction", "data"), fontsize=6.2,
                    color=MUTED, va="bottom", ha="left")
    ax.set_xticks(x)
    ax.set_xticklabels([LAB[m] for m in order], fontsize=6.6)
    ax.set_ylabel("revenue per round", fontsize=8.5, color=INK2)
    ax.set_ylim(0, max(float(g.second_cap.mean()), g.revenue_per_round.max()) * 1.2)
    ax.set_title("a. scalar setting: a fair head-to-head", fontsize=8.6, color=INK,
                 loc="left")

    # panel b: the cost of scalarness, which is NOT visible in revenue
    ax = axes[1]
    style(ax)
    gc = d[(d.setting == "contextual") & (d.deviation == "proposed")].set_index("mech")
    order = [m for m in ORDER_M if m in gc.index]
    x = np.arange(len(order))
    w = 0.34
    a1 = ax.bar(x - w / 2 - 0.01,
                [float(gc.loc[m, "price_above_cap_mass"]) for m in order], w,
                color=CAT[1], zorder=3,
                label="arrival mass where the price exceeds\nthe winner's capability")
    a2 = ax.bar(x + w / 2 + 0.01,
                [float(gc.loc[m, "compliant_conviction_rate"]) for m in order], w,
                color=CAT[4], zorder=3,
                label="rate of convicting a fully compliant winner")
    for bars in (a1, a2):
        for r in bars:
            ax.annotate(f"{r.get_height():.3f}",
                        (r.get_x() + r.get_width() / 2, r.get_height()),
                        ha="center", va="bottom", fontsize=6.2, color=INK2)
    ax.set_xticks(x)
    ax.set_xticklabels([LAB[m] for m in order], fontsize=6.6)
    ax.set_ylabel("share", fontsize=8.5, color=INK2)
    ax.set_ylim(0, 0.42)
    ax.legend(frameon=False, fontsize=5.9, loc="upper center",
              bbox_to_anchor=(0.5, -0.24), ncol=1)
    ax.set_title("b. contextual instances: the cost of scalarness", fontsize=8.6,
                 color=INK, loc="left")

    # panel c: what a fired monitor costs
    ax = axes[2]
    style(ax)
    if bs is not None:
        gb = bs[bs.gate_blind2] if "gate_blind2" in bs.columns else bs
        gg = gb.groupby("mech")["post_fire_revenue_per_round"].mean().to_frame()
        order = [m for m in ORDER_M if m in gg.index]
        x = np.arange(len(order))
        vals = [float(gg.loc[m, "post_fire_revenue_per_round"])
                if np.isfinite(gg.loc[m, "post_fire_revenue_per_round"]) else 0.0
                for m in order]
        ax.bar(x, vals, 0.5,
               color=[CAT[ORDER_M.index(m) % len(CAT)] for m in order], zorder=3)
        for k, v in enumerate(vals):
            ax.annotate("0.000\n(stops serving)" if v == 0 else f"{v:.3f}", (k, v),
                        ha="center", va="bottom", fontsize=6.2, color=INK2)
        ax.set_xticks(x)
        ax.set_xticklabels([LAB[m] for m in order], fontsize=6.6)
        ax.set_ylim(0, max(vals) * 1.28 if max(vals) else 1)
    ax.set_ylabel("revenue per round AFTER the monitor fires", fontsize=7.6,
                  color=INK2)
    ax.set_title("c. what a fired monitor costs", fontsize=8.6, color=INK, loc="left")

    fig.suptitle("The second-best utility guarantee mechanism (WWW 2026), "
                 "REIMPLEMENTED FROM THE PAPER and run under our observation "
                 "model; not a reproduction of their results in their setting",
                 fontsize=8.4, color=INK, x=0.012, ha="left", y=1.05)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "a4_fig7_second_best.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(out, "a4_fig7_second_best.png"), bbox_inches="tight")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--family-set", default="Q3")
    ap.add_argument("--alpha", default="a0.50")
    ap.add_argument("--util-contexts", default="MMLU,GSM8K")
    ap.add_argument("--csv-a3", default="experiments/data/A3",
                    help="the committed A3 threshold CSVs, read but never written")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fig_capabilities(a.csv, a.out)
    fig_complementarity(a.csv, a.out)
    fig_two_worlds(a.csv, a.out, family_set=a.family_set, alpha=a.alpha)
    fig_frontier(a.csv, a.out)
    fig_threshold(a.csv_a3, a.out)
    for ctx in a.util_contexts.split(","):
        fig_utility_curves(a.csv, a.out, context=ctx)
    fig_capability_gap(a.csv, a.out)
    fig_second_best(a.csv, a.out)
    print("figures written to", a.out)


if __name__ == "__main__":
    main()
