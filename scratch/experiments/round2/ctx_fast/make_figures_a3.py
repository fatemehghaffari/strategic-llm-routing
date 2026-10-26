"""Figures for the CG-MESP horizon sweep across its own thresholds (package A3), vector PDF.

Style follows scratch/experiments/round2/figures/make_figures_a2.py: the same Okabe-Ito subset, the
same rcParams, no embedded titles, no two y-axes, every series carrying a marker and a line style as
well as a legend entry, and every panel degrading gracefully when its input is not there.

Input:  threshold_summary.csv  (from ctx_fast/aggregate.py)
Usage:  make_figures_a3.py --csv <dir with threshold_summary.csv> --out <dir>
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "magenta": "#CC79A7",
     "sky": "#56B4E9", "vermillion": "#D55E00", "ink": "#1a1a1a", "muted": "#6b6b6b", "grid": "#d9d9d9"}
plt.rcParams.update({"font.size": 7.2, "axes.labelsize": 7.4, "legend.fontsize": 6.3, "xtick.labelsize": 6.6,
                     "ytick.labelsize": 6.6, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": C["muted"], "axes.labelcolor": C["ink"], "text.color": C["ink"],
                     "xtick.color": C["muted"], "ytick.color": C["muted"], "grid.color": C["grid"],
                     "pdf.fonttype": 42, "ps.fonttype": 42, "figure.dpi": 160})

# instance -> (colour, marker, line style, label)
INST = {"C": (C["blue"], "o", "-", "C  (K = 2, unique top, near tie)"),
        "E": (C["orange"], "s", "--", "E  (K = 2, crossing capacities)"),
        "D": (C["green"], "^", "-.", "D  (K = 3, three agents)"),
        "F": (C["magenta"], "D", ":", "F  (K = 3, honest top agent)")}
DCOL = {1: C["blue"], 2: C["orange"], 3: C["green"], 4: C["magenta"]}
DMARK = {1: "o", 2: "s", 3: "^", 4: "D"}
FLOOR = 1e-5
# analytic thresholds, computed from the mechanism's own parameters by bisection, as a function of
# the dimension of the gridded context space alone (K = 2, Lipschitz constant 1)
THR = {1: dict(price=6.06, A=5.25, B=6.76, C=7.14),
       2: dict(price=8.49, A=7.53, B=9.35, C=9.80),
       3: dict(price=11.06, A=10.14, B=12.08, C=12.64),
       4: dict(price=13.75, A=12.72, B=14.90, C=15.52)}
DIM = 1          # the dimension the main figure is drawn for; set by main()


def read_csv(p):
    p = Path(p)
    return list(csv.DictReader(p.open())) if p.exists() else []


def style_axis(ax, xlabel, ylabel, logy=False):
    if logy:
        ax.set_yscale("log")
    ax.grid(alpha=.5, linewidth=.5)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def empty(ax, msg):
    ax.text(.5, .5, msg, ha="center", va="center", transform=ax.transAxes, color=C["muted"], fontsize=6.4)
    ax.set_xticks([])
    ax.set_yticks([])


def series(rows, inst, field, dim=None):
    dim = DIM if dim is None else dim
    rs = sorted([r for r in rows if r["inst"] == inst and int(r["d"]) == dim
                 and r.get(field) not in (None, "")],
                key=lambda r: float(r["logn"]))
    xs, ys = [], []
    for r in rs:
        try:
            v = float(r[field])
        except ValueError:
            continue
        if math.isnan(v):
            continue
        xs.append(float(r["logn"]))
        ys.append(v)
    return xs, ys


def mark_thresholds(ax, Ds=None, which="price", ytext=None):
    for D in (Ds if Ds is not None else (DIM,)):
        x = THR[D][which]
        ax.axvline(x, color=C["muted"], lw=.7, ls=(0, (4, 3)))
        if ytext is not None:
            ax.text(x, ytext, f" d = {D}", rotation=90, va="bottom", ha="left", fontsize=5.6,
                    color=C["muted"])


def panel_price_share(ax, rows):
    if not rows:
        return empty(ax, "sweep not available")
    for inst, (col, mk, ls, lab) in INST.items():
        xs, ys = series(rows, inst, "positive_price_share")
        if xs:
            ax.plot(xs, ys, color=col, marker=mk, ms=3.0, lw=1.1, ls=ls, label=lab)
    ax.set_ylim(-.06, 1.10)
    mark_thresholds(ax, ytext=-.04)
    ax.text(.03, .45, "dashed: where $\\sigma_n < 1$",
            transform=ax.transAxes, fontsize=5.4, color=C["muted"], ha="left", va="center")
    style_axis(ax, "horizon, $\\log_{10} n$", "share of awarded regions\nwith a positive price")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(-.03, .80), fontsize=5.6)


def panel_monitor(ax, rows):
    """The monitor is inert while the price is zero and convicts a crashing winner once it is not."""
    if not rows:
        return empty(ax, "sweep not available")
    drew = False
    for inst, (col, mk, ls, lab) in INST.items():
        xs, ys = series(rows, inst, "conviction_share_crash")
        if xs:
            drew = True
            ax.plot(xs, ys, color=col, marker=mk, ms=3.0, lw=1.2, ls="-",
                    label=f"crash, {inst}")
        xs, ys = series(rows, inst, "conviction_share_rider100")
        if xs:
            ax.plot(xs, ys, color=col, marker=mk, ms=2.2, lw=.9, ls=(0, (3, 2)), alpha=.8)
    if not drew:
        return empty(ax, "sweep not available")
    fired = sum(int(r["switches_proposed"]) for r in rows)
    ax.axhline(0.0, color=C["muted"], lw=.7)
    ax.set_ylim(-.06, 1.10)
    mark_thresholds(ax, ytext=-.04)
    ax.text(.97, .16, "dashed: ride the boundary at scale 1\n"
                      f"proposed profile: {fired} firings, all runs",
            transform=ax.transAxes, fontsize=5.4, color=C["ink"], ha="right", va="center")
    style_axis(ax, "horizon, $\\log_{10} n$", "share of awarded regions\nat which the monitor convicts")
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(-.02, .42), fontsize=5.8)


def panel_sigma_tau(ax, rows):
    if not rows:
        return empty(ax, "sweep not available")
    xs, ys = series(rows, "C", "sigma_n")
    if xs:
        ax.plot(xs, ys, color=C["ink"], lw=1.2, ls="-", marker="o", ms=2.4,
                label="shading $\\sigma_n = 3 s_n + \\rho_n$")
    for inst, (col, mk, ls, lab) in INST.items():
        xs, ys = series(rows, inst, "mean_tau")
        if xs:
            ax.plot(xs, ys, color=col, marker=mk, ms=3.0, lw=1.0, ls=ls,
                    label="mean announced price, " + inst)
    ax.axhline(1.0, color=C["vermillion"], lw=.8, ls=":")
    ax.set_ylim(-.12, None)
    ax.text(.03, .20, "$\\sigma_n \\geq 1$ forces\na price of zero",
            transform=ax.transAxes, fontsize=5.4, color=C["vermillion"], ha="left", va="center")
    style_axis(ax, "horizon, $\\log_{10} n$", "shading and announced price")
    ax.legend(frameon=False, loc="upper right", ncol=1, handlelength=1.8, fontsize=5.6)


def panel_revenue(ax, rows):
    if not rows:
        return empty(ax, "sweep not available")
    drew = False
    for inst, (col, mk, ls, lab) in INST.items():
        xs, ys = series(rows, inst, "rev_per_round")
        xb, yb = series(rows, inst, "bench_M2_per_round")
        if not xs:
            continue
        drew = True
        ax.plot(xs, ys, color=col, marker=mk, ms=3.0, lw=1.1, ls=ls, label=f"revenue per round, {inst}")
        if xb:
            ax.plot(xb, yb, color=col, lw=.7, ls=(0, (1, 2)), alpha=.75)
    if not drew:
        return empty(ax, "sweep not available")
    mark_thresholds(ax)
    ax.text(.97, .93, "dotted: the $M_{(2)}$ benchmark", transform=ax.transAxes, fontsize=5.4,
            color=C["muted"], ha="right", va="top")
    style_axis(ax, "horizon, $\\log_{10} n$", "platform revenue per round")
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, loc="center left", ncol=1, bbox_to_anchor=(-.03, .60), fontsize=5.6)


def panel_gain(ax, rows):
    if not rows:
        return empty(ax, "sweep not available")
    drew = False
    for inst, (col, mk, ls, lab) in INST.items():
        rs = sorted([r for r in rows if r["inst"] == inst and int(r["d"]) == DIM
                     and r.get("best_searched_gain", "") != ""], key=lambda r: float(r["logn"]))
        rs = [r for r in rs if not math.isnan(float(r["best_searched_gain"]))]
        if not rs:
            continue
        drew = True
        x = [float(r["logn"]) for r in rs]
        g = [max(max(float(r["best_searched_gain"]), 0.0) / float(r["n"]), FLOOR) for r in rs]
        b = [float(r["boundA"]) / float(r["n"]) for r in rs]
        ax.plot(x, g, color=col, marker=mk, ms=3.0, lw=1.1, ls=ls,
                label=f"best of 6 deviations, {inst}")
        ax.plot(x, b, color=col, lw=.7, ls=(0, (1, 2)), alpha=.75)
    if not drew:
        return empty(ax, "sweep not available")
    ax.axhline(1.0, color=C["vermillion"], lw=.8, ls=":")
    ax.set_ylim(FLOOR / 3, 30)
    ax.text(.97, .05, f"dotted: the part (A) budget / n\nfloor at {FLOOR:g}",
            transform=ax.transAxes, fontsize=5.4, color=C["muted"], ha="right", va="bottom")
    style_axis(ax, "horizon, $\\log_{10} n$", "per round, additive equilibrium", logy=True)
    ax.legend(frameon=False, loc="center left", ncol=1, bbox_to_anchor=(-.03, .40), fontsize=5.6)


def panel_slacks(ax, rows):
    if not rows:
        return empty(ax, "sweep not available")
    for inst, (col, mk, ls, lab) in INST.items():
        for f, lsx, name in (("boundA_over_n", "-", "(A)"), ("slackB_over_n", "--", "(B)"),
                             ("slackC_over_n", ":", "(C)")):
            xs, ys = series(rows, inst, f)
            if xs and inst in ("C", "D"):
                ax.plot(xs, ys, color=col, lw=1.0, ls=lsx, marker=mk, ms=2.2,
                        label=f"{name}, {inst}")  # noqa: E501
    ax.axhline(1.0, color=C["vermillion"], lw=.9, ls=":")
    ax.text(.97, .96, "below the dotted line the\nguarantee says something", transform=ax.transAxes,
            fontsize=5.4, color=C["vermillion"], ha="right", va="top")
    style_axis(ax, "horizon, $\\log_{10} n$", "error term / n", logy=True)
    ax.legend(frameon=False, loc="lower left", ncol=2, columnspacing=.6, fontsize=5.6)


def _slack_lines(ax, rows, field, lab):
    """The slack depends only on n and D, not on the instance, so it is drawn once per D."""
    seen = set()
    for D, col, ls in ((DIM, C["ink"], (0, (3, 2))),):
        rs = sorted({(float(r["logn"]), float(r[field]) / float(r["n"]))
                     for r in rows if int(r["d"]) == D})
        if not rs or D in seen:
            continue
        seen.add(D)
        ax.plot([x for x, _ in rs], [y for _, y in rs], color=col, lw=.9, ls=ls,
                label=f"{lab}, D = {D}")


def panel_partB(ax, rows):
    if not rows:
        return empty(ax, "sweep not available")
    for inst, (col, mk, ls, lab) in INST.items():
        rs = sorted([r for r in rows if r["inst"] == inst and int(r["d"]) == DIM],
                    key=lambda r: float(r["logn"]))
        if not rs:
            continue
        ax.plot([float(r["logn"]) for r in rs],
                [float(r["revenue_deficit_B"]) / float(r["n"]) for r in rs],
                color=col, marker=mk, ms=3.0, lw=1.1, ls=ls, label=f"realised deficit, {inst}")
    _slack_lines(ax, rows, "slackB", "slack (B) / n")
    ax.axhline(1.0, color=C["vermillion"], lw=.8, ls=":")
    style_axis(ax, "horizon, $\\log_{10} n$", "part (B): $M_{(2)}$ revenue deficit per round", logy=True)
    ax.legend(frameon=False, loc="lower left", ncol=1, fontsize=5.8)


def panel_partC(ax, rows):
    rs_all = [r for r in rows if r.get("honest_deficit_C", "") != ""]
    if not rs_all:
        return empty(ax, "joint-sabotage runs not available")
    for inst, (col, mk, ls, lab) in INST.items():
        rs = sorted([r for r in rs_all if r["inst"] == inst and int(r["d"]) == DIM],
                    key=lambda r: float(r["logn"]))
        if not rs:
            continue
        ax.plot([float(r["logn"]) for r in rs],
                [float(r["honest_deficit_C"]) / float(r["n"]) for r in rs],
                color=col, marker=mk, ms=3.0, lw=1.1, ls=ls, label=f"realised deficit, {inst}")
    _slack_lines(ax, rs_all, "slackC", "slack (C) / n")
    ax.axhline(0.0, color=C["muted"], lw=.7)
    ax.axhline(1.0, color=C["vermillion"], lw=.8, ls=":")
    ax.set_ylim(-.6, 4.2)
    ax.text(.03, .30, "the realised deficit is negative at\nevery horizon reached: under joint\n"
                      "sabotage the platform stays above\nthe honest benchmark",
            transform=ax.transAxes, fontsize=5.6, color=C["muted"], va="top")
    style_axis(ax, "horizon, $\\log_{10} n$", "part (C): honest-benchmark deficit per round")
    ax.legend(frameon=False, loc="upper right", ncol=1, fontsize=5.8)


def panel_dim_price(ax, rows):
    """The price turns on where the dimension says it should, and K does not move it."""
    drew = False
    for dim in (1, 2, 3):
        for inst in ("C", "D"):        # near-identical second capacities, K = 2 against K = 3
            rs = sorted([r for r in rows if r["inst"] == inst and int(r["d"]) == dim
                         and r.get("positive_price_share", "") != ""],
                        key=lambda r: float(r["logn"]))
            if len(rs) < 2:
                continue
            drew = True
            K = int(rs[0]["K"])
            ax.plot([float(r["logn"]) for r in rs],
                    [float(r["positive_price_share"]) for r in rs],
                    color=DCOL.get(dim, C["muted"]), marker=DMARK.get(dim, "o"), ms=2.6, lw=1.0,
                    ls=("-" if K == 2 else "--"), alpha=.9,
                    label=f"d = {dim}, K = {K}, instance {inst}")
    if not drew:
        return empty(ax, "sweep not available")
    for dim in (1, 2, 3):
        ax.axvline(THR[dim]["price"], color=C["muted"], lw=.7, ls=(0, (4, 3)))
        ax.text(THR[dim]["price"], -.04, f" d = {dim}", rotation=90, va="bottom", ha="left",
                fontsize=5.4, color=C["muted"])
    ax.set_ylim(-.06, 1.10)
    ax.text(.985, .60, "instances C and D have the same\nsecond capacity to within 0.007 and\n"
                       "differ only in K", transform=ax.transAxes, fontsize=5.4, color=C["muted"],
            ha="right", va="center")
    style_axis(ax, "horizon, $\\log_{10} n$", "share of awarded regions\nwith a positive price")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(-.02, 1.02), fontsize=5.4, ncol=1)


def panel_dim_revenue(ax, rows):
    """Revenue per round: it falls until the price turns on and rises after, at every dimension."""
    drew = False
    for dim in (1, 2, 3):
        for inst in ("C", "D"):
            rs = sorted([r for r in rows if r["inst"] == inst and int(r["d"]) == dim],
                        key=lambda r: float(r["logn"]))
            if len(rs) < 2:
                continue
            drew = True
            K = int(rs[0]["K"])
            ax.plot([float(r["logn"]) for r in rs],
                    [float(r["rev_per_round"]) for r in rs],
                    color=DCOL.get(dim, C["muted"]), marker=DMARK.get(dim, "o"), ms=2.6, lw=1.0,
                    ls=("-" if K == 2 else "--"), alpha=.9,
                    label=f"d = {dim}, K = {K}, instance {inst}")
    if not drew:
        return empty(ax, "sweep not available")
    rs = [r for r in rows if r["inst"] == "C"]
    if rs:
        ax.axhline(float(rs[0]["bench_M2_per_round"]), color=C["vermillion"], lw=.8, ls=":")
        ax.text(.985, .81, "dotted: the $M_{(2)}$ benchmark of instance C",
                transform=ax.transAxes, fontsize=5.4, color=C["vermillion"], ha="right", va="top")
    for dim in (1, 2, 3):
        ax.axvline(THR[dim]["price"], color=C["muted"], lw=.7, ls=(0, (4, 3)))
    ax.set_ylim(0, 1.0)
    style_axis(ax, "horizon, $\\log_{10} n$", "platform revenue per round")
    ax.legend(frameon=False, loc="upper left", fontsize=5.4, ncol=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dim", type=int, default=1)
    a = ap.parse_args()
    global DIM
    DIM = a.dim
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = read_csv(Path(a.csv) / "threshold_summary.csv")

    fig, axes2 = plt.subplots(2, 3, figsize=(7.1, 4.6))
    axes = axes2.ravel()
    panel_price_share(axes[0], rows)
    panel_monitor(axes[1], rows)
    panel_sigma_tau(axes[2], rows)
    panel_revenue(axes[3], rows)
    panel_gain(axes[4], rows)
    panel_slacks(axes[5], rows)
    for ax, lab in zip(axes, "abcdef"):
        ax.text(-.26, 1.06, f"({lab})", transform=ax.transAxes, fontsize=7.6, fontweight="bold")
    fig.tight_layout(pad=.5, w_pad=1.9, h_pad=1.7)
    fig.savefig(out / "continuous_threshold.pdf")
    plt.close(fig)
    print(f"  {out / 'continuous_threshold.pdf'}")

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.7))
    panel_dim_price(axes[0], rows)
    panel_dim_revenue(axes[1], rows)
    for ax, lab in zip(axes, "ab"):
        ax.text(-.16, 1.05, f"({lab})", transform=ax.transAxes, fontsize=7.6, fontweight="bold")
    fig.tight_layout(pad=.45, w_pad=2.2)
    fig.savefig(out / "continuous_threshold_dim.pdf")
    plt.close(fig)
    print(f"  {out / 'continuous_threshold_dim.pdf'}")

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.6))
    panel_partB(axes[0], rows)
    panel_partC(axes[1], rows)
    for ax, lab in zip(axes, "ab"):
        ax.text(-.16, 1.05, f"({lab})", transform=ax.transAxes, fontsize=7.6, fontweight="bold")
    fig.tight_layout(pad=.45, w_pad=2.2)
    fig.savefig(out / "continuous_threshold_supp.pdf")
    plt.close(fig)
    print(f"  {out / 'continuous_threshold_supp.pdf'}")


if __name__ == "__main__":
    main()
