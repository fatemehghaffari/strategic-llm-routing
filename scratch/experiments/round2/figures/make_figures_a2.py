"""Proposed figures for the profile-local and continuous mechanisms (package A2), vector PDF.

Style follows figures/make_figures.py: the same Okabe-Ito subset, the same rcParams, no embedded titles, no two
y-axes, every series carrying a marker and a line style as well as a legend entry, and every panel
degrading gracefully when its input CSV is not there yet.

Inputs (all produced by ctx_local/aggregate.py and ctx_local/continuous.py):
  exact_grid.csv, exact_profiles.csv, ladder.csv, regime.csv, continuous_thresholds.csv

Usage:
  make_figures_a2.py --csv <scratchpad>/round2/A2/csv --out <scratchpad>/round2/A2/figures
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np
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

HORIZON_COLOR = {2000: C["sky"], 8000: C["blue"], 20000: C["orange"], 50000: C["green"],
                 200000: C["vermillion"], 1000000: C["magenta"]}
HORIZON_MARK = {2000: "v", 8000: "o", 20000: "s", 50000: "^", 200000: "D", 1000000: "P"}


def read_csv(p):
    p = Path(p)
    return list(csv.DictReader(p.open())) if p.exists() else []


def style_axis(ax, xlabel, ylabel, logx=False, logy=False):
    if logx:
        ax.set_xscale("log")
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


# == panels

def panel_exploit_vs_Q(ax, grid, family="replicated_unique_top", ns=(8000, 20000, 50000, 200000)):
    """(a) certified exploitability per round against the profile count, with the theorem's own constant."""
    rows = [r for r in grid if r["family"] == family]
    if not rows:
        return empty(ax, "exact grid not available")
    drew = False
    for n in ns:
        rs = sorted([r for r in rows if int(r["n"]) == n], key=lambda r: int(r["Q"]))
        if not rs:
            continue
        drew = True
        Q = [int(r["Q"]) for r in rs]
        lo = [float(r["exploit_LB_per_round"]) for r in rs]
        hi = [float(r["exploit_UB_per_round"]) for r in rs]
        col = HORIZON_COLOR.get(n, C["muted"])
        ax.fill_between(Q, lo, hi, color=col, alpha=.18, linewidth=0)
        ax.plot(Q, hi, marker=HORIZON_MARK.get(n, "o"), ms=3.2, lw=1.1, color=col,
                label=f"certified, n = {n:,}".replace(",", " "))
        ax.plot(Q, lo, marker=HORIZON_MARK.get(n, "o"), ms=2.4, lw=.8, ls=":", color=col)
        tc = [float(r["theorem_constant_per_round"]) for r in rs]
        ax.plot(Q, tc, lw=.9, ls="--", color=col, alpha=.75)
        trunc = [(q, h) for q, h, r in zip(Q, hi, rs) if int(r["n_truncated_profiles"]) > 0]
        if trunc:
            ax.plot([q for q, _ in trunc], [h for _, h in trunc], "x", ms=4.5, mew=1.0, color=col)
    if not drew:
        return empty(ax, "exact grid not available")
    ax.set_ylim(0, min(2.2, ax.get_ylim()[1]))
    style_axis(ax, "number of context profiles Q", "per-round gain and bound")
    ax.legend(frameon=False, loc="upper left", ncol=1)
    ax.set_ylim(0, min(1.45, ax.get_ylim()[1]))
    ax.text(.03, .62, "solid and dotted: the certified interval\ndashed: the theorem's constant\n"
                      "x: a profile never finishes bidding",
            transform=ax.transAxes, ha="left", va="top", fontsize=5.4, color=C["muted"])


def panel_revenue_vs_Q(ax, grid, family="replicated_unique_top", ns=(8000, 20000, 50000, 200000)):
    """(b) revenue per round against the profile count, with the second-capacity benchmark."""
    rows = [r for r in grid if r["family"] == family]
    if not rows:
        return empty(ax, "exact grid not available")
    drew = False
    for n in ns:
        rs = sorted([r for r in rows if int(r["n"]) == n], key=lambda r: int(r["Q"]))
        if not rs:
            continue
        drew = True
        Q = [int(r["Q"]) for r in rs]
        col = HORIZON_COLOR.get(n, C["muted"])
        ax.plot(Q, [float(r["revenue_LB_per_round"]) for r in rs], marker=HORIZON_MARK.get(n, "o"),
                ms=3.2, lw=1.1, color=col, label=f"revenue, n = {n:,}".replace(",", " "))
        ax.plot(Q, [float(r["stage1_share_of_horizon"]) for r in rs], lw=.9, ls="-.", color=col, alpha=.7)
    if not drew:
        return empty(ax, "exact grid not available")
    b = float(rows[0]["benchmark_M2_per_round"])
    ax.axhline(b, color=C["ink"], lw=.9, ls="--")
    ax.text(.02, b + .012, "second capacity $M_{(2)}$", transform=ax.get_yaxis_transform(),
            fontsize=5.8, color=C["ink"])
    style_axis(ax, "number of context profiles Q", "per-round revenue and bidding share")
    ax.set_ylim(0, 1.12)
    ax.legend(frameon=False, loc="center right")
    ax.text(.02, .03, "dash-dot: share of the horizon spent bidding, $QKL_n/n$",
            transform=ax.transAxes, fontsize=5.4, color=C["muted"])


def panel_ladder(ax, ladder, family="replicated_unique_top", n=200000, Q=3):
    """(c) the contextual ablation ladder: best tested deviation per round, per mechanism rung."""
    rows = [r for r in ladder if r["family"] == family and int(r["n"]) == n and int(r["Q"]) == Q]
    if not rows:
        return empty(ax, "ablation ladder not available")
    order = ["pl_mesp", "pl_windowed", "pl_noslack", "pl_rawprice", "pl_nofallback", "pl_runnerup",
             "pl_nomonitor", "pl_shared"]
    label = {"pl_mesp": "PL-MESP", "pl_windowed": "windowed monitor", "pl_noslack": "monitor, no slack",
             "pl_rawprice": "no price correction", "pl_nofallback": "no fallback (round robin)",
             "pl_runnerup": "runner-up, unmonitored", "pl_nomonitor": "no monitor",
             "pl_shared": "statistics shared across profiles"}
    ys, vals, heads, keep = [], [], [], []
    for v in order:
        rs = [r for r in rows if r["variant"] == v]
        uni = [r for r in rs if not r["behavior"].startswith("joint:")]
        jnt = [r for r in rs if r["behavior"].startswith("joint:")]
        if not uni:
            continue
        ys.append(label[v])
        vals.append(max(float(r["gain_per_round_mean"]) for r in uni))
        heads.append(min(float(r["honest_headroom_per_round"]) for r in jnt) if jnt else float("nan"))
        keep.append(v)
    if not ys:
        return empty(ax, "ablation ladder not available")
    y = np.arange(len(ys))
    cols = [C["blue"] if v == "pl_mesp" else C["muted"] for v in keep]
    ax.barh(y, vals, color=cols, height=.62, edgecolor="none")
    span = max(max(vals), 1e-9)
    for k, hh in enumerate(heads):
        if not np.isfinite(hh):
            continue
        ax.text(span * 1.04, k, f"{hh:+.3f}", va="center", ha="left", fontsize=5.4,
                color=(C["green"] if hh >= 0 else C["vermillion"]))
    ax.set_xlim(0, span * 1.30)
    ax.set_yticks(y)
    ax.set_yticklabels(ys)
    ax.invert_yaxis()
    style_axis(ax, "best tested deviation, per round", "")
    ax.grid(axis="y", visible=False)
    ax.text(.99, .02, f"n = {n:,}, Q = {Q}".replace(",", " "), transform=ax.transAxes, ha="right",
            va="bottom", fontsize=5.6, color=C["muted"])


def panel_continuous(ax, thr, K=2, L=1.0):
    """(d) the horizon at which each continuous guarantee first says anything, against the dimension."""
    rows = [r for r in thr if int(r["K"]) == K and abs(float(r["L_lip"]) - L) < 1e-9]
    if not rows:
        return empty(ax, "continuous thresholds not available")
    rows = sorted(rows, key=lambda r: int(r["D"]))
    D = [int(r["D"]) for r in rows]
    series = [("log10_n_price_positive", "price can be positive", C["vermillion"], "D", "-"),
              ("log10_n_A_below_n", "bound (A) below n", C["blue"], "o", "-"),
              ("log10_n_B_below_n", "slack (B) below n", C["orange"], "s", "-"),
              ("log10_n_C_below_n", "slack (C) below n", C["green"], "^", "-"),
              ("log10_n_public_En_below_n", "public error below n", C["muted"], "v", "--")]
    for key, lab, col, mk, ls in series:
        ax.plot(D, [float(r[key]) for r in rows], marker=mk, ms=3.2, lw=1.1, ls=ls, color=col, label=lab)
    ax.axhspan(0, 9, color=C["sky"], alpha=.13, linewidth=0)
    ax.text(D[-1], 3.4, "horizons that can be run ", fontsize=5.8, color=C["ink"], va="center", ha="right")
    ax.set_ylim(0, max(float(r["log10_n_C_below_n"]) for r in rows) * 1.22)
    style_axis(ax, "context dimension D = K d", "smallest horizon, $\\log_{10} n$")
    ax.legend(frameon=False, loc="upper left")


def panel_regime(ax, regime, K=3):
    """(s1) the (n, Q) region in which the profile-local mechanism is implementable and its bound informative."""
    rows = [r for r in regime if int(r["K"]) == K]
    if not rows:
        return empty(ax, "regime table not available")
    ns = sorted({int(r["n"]) for r in rows})
    comp, below, mon = [], [], []
    for n in ns:
        rs = [r for r in rows if int(r["n"]) == n]
        c = [int(r["Q"]) for r in rs if int(r["completes"])]
        b = [int(r["Q"]) for r in rs if int(r["below_trivial_2n"]) and int(r["completes"])]
        m = [int(r["Q"]) for r in rs if int(r["monitor_active_tau_0.5"]) and int(r["completes"])]
        comp.append(max(c) if c else 0)
        below.append(max(b) if b else 0)
        mon.append(max(m) if m else 0)
    same = all(a == b for a, b in zip(comp, below))
    ax.plot(ns, comp, lw=1.3, color=C["blue"], marker="o", ms=2.8,
            label=("every profile finishes bidding, and\nthe bound is below the trivial bound" if same
                   else "every profile finishes bidding"))
    if not same:
        ax.plot(ns, below, lw=1.2, ls="--", color=C["orange"], marker="s", ms=2.6,
                label="and the bound is below the trivial bound")
    ax.plot(ns, mon, lw=1.0, ls=":", color=C["vermillion"], marker="^", ms=2.4,
            label="and the monitor can fire at a price of 0.5")
    ax.set_xscale("log")
    style_axis(ax, "horizon n", "largest number of profiles Q", logx=True, logy=True)
    ax.legend(frameon=False, loc="upper left")
    ax.text(.98, .04, f"K = {K}; even arrival path", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=5.8, color=C["muted"])


def panel_nontop(ax, nt, Ks=(2, 3)):
    """(s3) the horizon at which the theorem's non-top branch condition 4 s_n <= delta first holds."""
    if not nt:
        return empty(ax, "non-top threshold table not available")
    for K, col, mk, ls in ((2, C["blue"], "o", "-"), (3, C["orange"], "s", "--")):
        rs = sorted([r for r in nt if int(r["K"]) == K], key=lambda r: float(r["delta"]))
        if not rs:
            continue
        ax.plot([float(r["delta"]) for r in rs], [float(r["log10_n_min"]) for r in rs],
                marker=mk, ms=3.2, lw=1.1, ls=ls, color=col, label=f"K = {K}")
    ax.axhspan(0, 9, color=C["sky"], alpha=.13, linewidth=0)
    ax.text(.98, .18, "horizons that can be run", transform=ax.transAxes, ha="right", fontsize=5.8,
            color=C["ink"])
    ax.set_xscale("log")
    style_axis(ax, "capacity gap $\\delta_i$ at a non-top profile", "smallest horizon, $\\log_{10} n$",
               logx=True)
    ax.legend(frameon=False, loc="upper right")
    ax.text(.02, .06, "K = 2 and K = 3 differ by at most\n0.01 in the exponent", transform=ax.transAxes,
            fontsize=5.6, color=C["muted"])


def panel_exploit_vs_n(ax, grid, family="replicated_unique_top", Qs=(1, 2, 3)):
    """(s2) certified exploitability against the horizon at fixed profile count."""
    cols = {1: C["blue"], 2: C["orange"], 3: C["green"], 4: C["magenta"], 6: C["vermillion"]}
    drew = False
    for Q in Qs:
        rs = sorted([r for r in grid if r["family"] == family and int(r["Q"]) == Q
                     and int(r["n_truncated_profiles"]) == 0], key=lambda r: int(r["n"]))
        if len(rs) < 2:
            continue
        drew = True
        n = [int(r["n"]) for r in rs]
        lo = [float(r["exploit_LB"]) for r in rs]
        hi = [float(r["exploit_UB"]) for r in rs]
        ax.fill_between(n, lo, hi, color=cols.get(Q, C["muted"]), alpha=.18, linewidth=0)
        ax.plot(n, hi, marker="o", ms=3.0, lw=1.1, color=cols.get(Q, C["muted"]), label=f"Q = {Q}")
        ax.plot(n, lo, marker="o", ms=2.2, lw=.8, ls=":", color=cols.get(Q, C["muted"]))
    if not drew:
        return empty(ax, "fewer than two complete horizons per Q")
    style_axis(ax, "horizon n", "certified deviation gain (total)", logx=True, logy=True)
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
    allns = sorted({int(r["n"]) for r in grid if r["family"] == family})
    lab = [(f"{v // 1000}k" if v < 10 ** 6 else f"{v / 10 ** 6:g}M") if v >= 1000 else str(v) for v in allns]
    ax.xaxis.set_major_locator(FixedLocator(allns))
    ax.xaxis.set_major_formatter(FixedFormatter(lab))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.legend(frameon=False, loc="upper left")
    ax.text(.98, .04, "cells in which every profile finishes bidding", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=5.8, color=C["muted"])


# == drivers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--family", default="replicated_unique_top")
    ap.add_argument("--ladder-family", default=None)
    ap.add_argument("--ladder-n", type=int, default=200000)
    ap.add_argument("--ladder-Q", type=int, default=3)
    a = ap.parse_args()
    csvd, out = Path(a.csv), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    grid = read_csv(csvd / "exact_grid.csv")
    ladder = read_csv(csvd / "ladder.csv")
    regime = read_csv(csvd / "regime.csv")
    thr = read_csv(csvd / "continuous_thresholds.csv")

    fig, axes2 = plt.subplots(2, 2, figsize=(7.1, 4.4))
    axes = axes2.ravel()
    panel_exploit_vs_Q(axes[0], grid, a.family)
    panel_revenue_vs_Q(axes[1], grid, a.family)
    panel_ladder(axes[2], ladder, a.ladder_family or a.family, a.ladder_n, a.ladder_Q)
    panel_continuous(axes[3], thr)
    for ax, lab in zip(axes, "abcd"):
        ax.text(-.23, 1.05, f"({lab})", transform=ax.transAxes, fontsize=7.6, fontweight="bold")
    fig.tight_layout(pad=.6, w_pad=3.0, h_pad=1.8)
    fig.savefig(out / "main_contextual.pdf")
    plt.close(fig)
    print(f"  {out / 'main_contextual.pdf'}")

    nt = read_csv(csvd / "nontop_thresholds.csv")
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.35))
    panel_regime(axes[0], regime)
    panel_exploit_vs_n(axes[1], grid, a.family)
    panel_nontop(axes[2], nt)
    for ax, lab in zip(axes, "abc"):
        ax.text(-.20, 1.05, f"({lab})", transform=ax.transAxes, fontsize=7.6, fontweight="bold")
    fig.tight_layout(pad=.45, w_pad=1.9)
    fig.savefig(out / "supp_contextual_regime.pdf")
    plt.close(fig)
    print(f"  {out / 'supp_contextual_regime.pdf'}")


if __name__ == "__main__":
    main()
