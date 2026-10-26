"""Figures for the v2 comparison (arrival order, horizon, all baselines).

Reads only experiments/data/A4/v2_all_summary.csv and the per-round traces in
the v2 trace directory, so a restyle needs no simulation.
Colour marks the rule family (fixed order, never cycled); marker or line style
marks the provider profile within a family.
"""
import argparse
import glob
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trace import load  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "../../../../experiments/data/A4"))
TRACES = "<workspace>/v2"
OUT = os.path.join(DATA, "figures_generated", "v2")

# validated reference slots 1-5 (same as make_figures_a4.py)
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7"]
INK, INK2, MUTED, GRID = "#1b1b1b", "#4a4a4a", "#8a8a8a", "#e3e3e0"
FAM = {"plmesp": CAT[0], "second_best": CAT[1], "router": CAT[2], "esmaeili": CAT[3],
       "mesp_scalar": CAT[4]}
ORDERS = ["iid", "bursty", "drift", "grouped"]
ORDER_LABEL = {"iid": "shuffled", "bursty": "bursty", "drift": "drifting", "grouped": "grouped"}
ORDER_MARK = {"iid": "o", "bursty": "s", "drift": "^", "grouped": "D"}

ARMS = [  # (mech, profile, label, family)
    ("plmesp", "plmesp_star", "PL-MESP (ours), S*", "plmesp"),
    ("plmesp", "plmesp_low", "PL-MESP (ours), low-revenue eq.", "plmesp"),
    ("mesp_scalar", "mesp_star", "MESP (ours, one number), S*", "mesp_scalar"),
    ("second_best", "cao_eqmu", "Cao et al., eq. (shirk to $\\mu$)", "second_best"),
    ("second_best", "cao_eq0", "Cao et al., eq. (shirk to 0)", "second_best"),
    ("router_ucb", "average", "UCB router, average effort", "router"),
    ("router_ucb", "exploit_slow", "UCB router, exploited (slow)", "router"),
    ("router_ucb", "exploit_fast", "UCB router, exploited (fast)", "router"),
    ("router_eps", "average", "$\\epsilon$-greedy router, average effort", "router"),
    ("router_eps", "exploit_slow", "$\\epsilon$-greedy router, exploited (slow)", "router"),
    ("router_greedy", "average", "greedy router, average effort", "router"),
    ("router_greedy", "exploit_slow", "greedy router, exploited (slow)", "router"),
    ("esmaeili", "proposed", "Esmaeili et al., one observation", "esmaeili"),
]


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=7.5, length=3)
    ax.grid(True, axis="x", color=GRID, lw=0.7, zorder=0)


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def fig_order(d, n):
    """Revenue per round in each arrival order, one row per rule and profile."""
    x = d[d.n == n].groupby(["mech", "profile", "order"]).revenue_per_round.mean()
    hb = d.honest_bench.mean()
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    style(ax)
    for r, (mech, prof, lab, fam) in enumerate(ARMS):
        vals = [x.get((mech, prof, o), np.nan) for o in ORDERS]
        y = len(ARMS) - 1 - r
        ax.plot([np.nanmin(vals), np.nanmax(vals)], [y, y], color=FAM[fam], lw=2, alpha=0.35,
                solid_capstyle="round", zorder=2)
        for o, v in zip(ORDERS, vals):
            ax.plot(v, y, ORDER_MARK[o], ms=6, color=FAM[fam], mec="white", mew=0.8, zorder=3)
    ax.axvline(hb, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.annotate("honest benchmark", (hb, len(ARMS) - 0.4), fontsize=6.5, color=MUTED, ha="center")
    ax.set_yticks(range(len(ARMS)))
    ax.set_yticklabels([a[2] for a in ARMS][::-1], fontsize=7.2, color=INK2)
    ax.set_xlabel("platform revenue per round (mean over 10 model subsets)", fontsize=8, color=INK2)
    ax.set_xlim(-0.01, 0.75)
    ax.set_ylim(-0.7, len(ARMS) - 0.1)
    h = [plt.Line2D([], [], ls="", marker=ORDER_MARK[o], color=INK2, ms=6, label=ORDER_LABEL[o])
         for o in ORDERS]
    ax.legend(handles=h, title="arrival order", title_fontsize=7, fontsize=7, frameon=False,
              loc="lower right")
    ax.set_title(f"Same prompts, four arrival orders (n = {n:,})", fontsize=9.5, color=INK, loc="left")
    ax.annotate("a single visible mark: all four orders give the same revenue", (0, -0.13),
                xycoords="axes fraction", fontsize=6.5, color=MUTED)
    save(fig, f"v2_fig1_order_n{n}")


def fig_horizon(d):
    """Revenue against horizon, shuffled and bursty arrivals."""
    sel = [("plmesp", "plmesp_star", "-"), ("plmesp", "plmesp_low", "--"),
           ("second_best", "cao_eqmu", "-"), ("second_best", "cao_eq0", "--"),
           ("router_ucb", "average", "-"), ("router_ucb", "exploit_slow", "--"),
           ("mesp_scalar", "mesp_star", ":")]
    lab = {(a[0], a[1]): a[2] for a in ARMS}
    fam = {(a[0], a[1]): a[3] for a in ARMS}
    x = d.groupby(["mech", "profile", "order", "n"]).revenue_per_round.mean()
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), sharey=True)
    for ax, o in zip(axes, ["iid", "bursty"]):
        style(ax)
        ax.grid(True, axis="y", color=GRID, lw=0.7, zorder=0)
        for mech, prof, ls in sel:
            ns = sorted(n for (m_, p_, o_, n) in x.index if (m_, p_, o_) == (mech, prof, o))
            ax.plot(ns, [x[(mech, prof, o, n)] for n in ns], ls=ls, marker="o", ms=4, lw=2,
                    color=FAM[fam[(mech, prof)]], label=lab[(mech, prof)])
        ax.axhline(d.honest_bench.mean(), color=MUTED, lw=0.9, ls=(0, (4, 3)))
        ax.set_xscale("log")
        ax.set_xticks([3e5, 3e6, 3e7])
        ax.set_xticklabels(["$3{\\times}10^5$", "$3{\\times}10^6$", "$3{\\times}10^7$"])
        ax.minorticks_off()
        ax.set_xlabel("horizon n (rounds)", fontsize=8, color=INK2)
        ax.set_title(f"{ORDER_LABEL[o]} arrivals", fontsize=9, color=INK, loc="left")
    axes[0].set_ylabel("revenue per round", fontsize=8, color=INK2)
    axes[1].annotate("honest benchmark", (1.2e7, d.honest_bench.mean() + 0.012), fontsize=6.5, color=MUTED)
    axes[1].legend(fontsize=6.4, frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    save(fig, "v2_fig2_horizon")


def fig_trace_time(subset, n, order, seed=0, bins=300):
    """Running revenue over one run: who keeps serving, who slides."""
    runs = [("plmesp", "plmesp_star"), ("second_best", "cao_eqmu"), ("router_ucb", "exploit_slow"),
            ("mesp_scalar", "mesp_star")]
    lab = {(a[0], a[1]): a[2] for a in ARMS}
    fam = {(a[0], a[1]): a[3] for a in ARMS}
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    style(ax)
    ax.grid(True, axis="y", color=GRID, lw=0.7, zorder=0)
    for mech, prof in runs:
        f = os.path.join(TRACES, subset, str(n), order, f"{mech}_{prof}_seed{seed:02d}.npz")
        tr = load(f)
        m = tr["target"].astype(float)
        edges = np.linspace(0, len(m), bins + 1).astype(int)
        v = [m[a:b].mean() for a, b in zip(edges[:-1], edges[1:])]
        ax.plot(edges[1:] / len(m), v, lw=1.6, color=FAM[fam[(mech, prof)]], label=lab[(mech, prof)])
    ax.set_xlabel("fraction of the horizon", fontsize=8, color=INK2)
    ax.set_ylabel(f"revenue per round\n(average over {n // bins:,}-round windows)", fontsize=8, color=INK2)
    ax.set_title(f"One run, {ORDER_LABEL[order]} arrivals, n = {n:,} ({subset})", fontsize=9,
                 color=INK, loc="left")
    ax.legend(fontsize=6.6, frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    save(fig, f"v2_fig3_trace_{subset}_{order}_n{n}")


def fig_effort(subset, n, order, seed=0, bins=200):
    """Delivered quality per provider over time: UCB router vs PL-MESP."""
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), sharey=True)
    for ax, (mech, prof, title) in zip(axes, [("router_ucb", "exploit_slow", "UCB router"),
                                              ("plmesp", "plmesp_star", "PL-MESP (ours)")]):
        style(ax)
        ax.grid(True, axis="y", color=GRID, lw=0.7, zorder=0)
        tr = load(os.path.join(TRACES, subset, str(n), order, f"{mech}_{prof}_seed{seed:02d}.npz"))
        names = tr["meta"]["models"]
        honest = tr["meta"]["honest"]
        edges = np.linspace(0, n, bins + 1).astype(int)
        for i, nm in enumerate(names):
            sel = tr["agent"] == i
            xs, ys = [], []
            for a, b in zip(edges[:-1], edges[1:]):
                s = sel[a:b]
                xs.append(b / n)
                ys.append(tr["target"][a:b][s].mean() if s.sum() >= 20 else np.nan)
            ax.plot(xs, ys, lw=1.4, color=CAT[i % len(CAT)],
                    label=nm + (" (honest)" if honest[i] else ""))
        ax.set_title(title, fontsize=9, color=INK, loc="left")
        ax.set_xlabel("fraction of the horizon", fontsize=8, color=INK2)
    axes[0].set_ylabel("mean quality delivered when selected", fontsize=8, color=INK2)
    axes[1].legend(fontsize=6.4, frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    fig.suptitle(f"What providers deliver over time ({ORDER_LABEL[order]}, n = {n:,}, {subset})",
                 fontsize=9.5, color=INK, x=0.01, ha="left", y=1.03)
    save(fig, f"v2_fig4_effort_{subset}_{order}_n{n}")


def fig_service(d):
    """Share of the horizon left unserved (Cao, Esmaeili) and honest-winner conviction (MESP)."""
    x = d.groupby(["mech", "profile", "order", "n"])[["undelegated_fraction", "fire_rate"]].mean()
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    for ax, o in zip(axes, ["bursty", "grouped"]):
        style(ax)
        ax.grid(True, axis="y", color=GRID, lw=0.7, zorder=0)
        series = [("second_best", "cao_eqmu", "undelegated_fraction", "Cao et al.: share of horizon unserved", FAM["second_best"]),
                  ("mesp_scalar", "mesp_star", "fire_rate", "MESP (ours, one number): runs convicting an honest winner", FAM["mesp_scalar"]),
                  ("plmesp", "plmesp_star", "fire_rate", "PL-MESP (ours): runs convicting an honest winner", FAM["plmesp"])]
        for mech, prof, col, lab, c in series:
            ns = sorted(n for (m_, p_, o_, n) in x.index if (m_, p_, o_) == (mech, prof, o))
            ax.plot(ns, [x.loc[(mech, prof, o, n), col] for n in ns], marker="o", ms=4, lw=2, color=c, label=lab)
        ax.set_xscale("log")
        ax.set_xlim(2e5, 4.5e7)
        ax.set_xticks([3e5, 3e6, 3e7])
        ax.set_xticklabels(["$3{\\times}10^5$", "$3{\\times}10^6$", "$3{\\times}10^7$"])
        ax.minorticks_off()
        ax.set_ylim(-0.03, 1.03)
        ax.set_xlabel("horizon n (rounds)", fontsize=8, color=INK2)
        ax.set_title(f"{ORDER_LABEL[o]} arrivals", fontsize=9, color=INK, loc="left")
    axes[0].set_ylabel("fraction", fontsize=8, color=INK2)
    axes[1].legend(fontsize=6.4, frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    save(fig, "v2_fig5_service")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", default="k5_q50")
    a = ap.parse_args()
    d = pd.read_csv(os.path.join(DATA, "v2_all_summary.csv"))
    for n in (300000, 3000000):
        fig_order(d, n)
    fig_horizon(d)
    fig_service(d)
    for order in ("bursty", "iid"):
        fig_trace_time(a.subset, 3000000, order)
    fig_effort(a.subset, 3000000, "iid")


if __name__ == "__main__":
    main()
