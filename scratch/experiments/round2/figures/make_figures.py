"""Figures for the revision (vector PDF, no embedded titles; captions belong in LaTeX).

Palette: the Okabe-Ito subset already used by the retained suite, validated with the visualization skill's
checker (lightness band, chroma floor, normal-vision separation all pass; the magenta and green pair sits in the
6 to 8 CVD band, so those two are never the only distinction in a panel and every series carries a marker and a
line style as well as a legend entry). No panel uses two y-axes. Grids are recessive; all text is ink coloured.
Every panel degrades gracefully when its input CSV is not present yet.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.design import theorem_constant_top  # noqa: E402

C = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "magenta": "#CC79A7",
     "sky": "#56B4E9", "vermillion": "#D55E00", "ink": "#1a1a1a", "muted": "#6b6b6b", "grid": "#d9d9d9"}
plt.rcParams.update({"font.size": 7.2, "axes.labelsize": 7.4, "legend.fontsize": 6.3, "xtick.labelsize": 6.6,
                     "ytick.labelsize": 6.6, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": C["muted"], "axes.labelcolor": C["ink"], "text.color": C["ink"],
                     "xtick.color": C["muted"], "ytick.color": C["muted"], "grid.color": C["grid"],
                     "pdf.fonttype": 42, "ps.fonttype": 42, "figure.dpi": 160})


def read_csv(p):
    p = Path(p)
    return list(csv.DictReader(p.open())) if p.exists() else []


def read_json_dir(p, pattern):
    return [json.loads(f.read_text()) for f in sorted(Path(p).glob(pattern))] if Path(p).exists() else []


def horizon_ticks(ax, ns):
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
    lab = [(f"{int(v/1000)}k" if v < 10 ** 6 else f"{v/10**6:g}M") if v >= 1000 else str(int(v)) for v in ns]
    ax.xaxis.set_major_locator(FixedLocator(list(ns))); ax.xaxis.set_major_formatter(FixedFormatter(lab))
    ax.xaxis.set_minor_locator(NullLocator())


def style_axis(ax, xlabel, ylabel, logx=True, logy=False):
    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")
    ax.grid(alpha=.5, linewidth=.5)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)


def panel_exploitability(ax, cells, search, instances=("unique_top", "tied_top")):
    """(a) certified exploitability band against the horizon, with the theorem constant and the searched values."""
    colors = {"unique_top": C["blue"], "tied_top": C["orange"]}
    marks = {"unique_top": "o", "tied_top": "s"}
    drawn = False
    for inst in instances:
        rs = sorted([r for r in cells if r["alias"] == inst and int(r["n"]) >= 2000], key=lambda r: int(r["n"]))
        if not rs:
            continue
        drawn = True
        n = np.array([int(r["n"]) for r in rs], float)
        lb = np.array([float(r["exploit_LB_per_round"]) for r in rs])
        ub = np.array([float(r["exploit_UB_I1_per_round"]) for r in rs])
        ax.fill_between(n, lb, ub, color=colors[inst], alpha=.22, linewidth=0)
        ax.plot(n, lb, color=colors[inst], marker=marks[inst], markersize=3.4, linewidth=1.4, label=inst.replace("_", " "))
        ax.plot(n, ub, color=colors[inst], linewidth=.9, linestyle=(0, (4, 2)))
        s = [x for x in search if x["instance"] == inst and x["class"] == "bangbang"]
        for x in s:
            ax.plot([x["n"]], [x["heldout_mean_per_round"]], marker="^", color=colors[inst], markersize=6.0,
                    markerfacecolor="white", markeredgewidth=1.1, linestyle="none", zorder=5)
    if drawn:
        K = 3
        grid = np.array([2000, 5000, 8000, 20000, 50000], float)
        ax.plot(grid, [theorem_constant_top(int(x), K) / x for x in grid], color=C["muted"], linewidth=1.0,
                linestyle=":", label="bound")
        if search:
            ax.plot([], [], marker="^", color=C["muted"], markerfacecolor="white", linestyle="none", markersize=6.0,
                    label="search")
        style_axis(ax, "Horizon $n$", "Utility gain per round", logx=True, logy=True)
        horizon_ticks(ax, [2000, 8000, 50000])
        ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5, -.26), ncol=2, handlelength=1.4,
                  borderpad=.1, columnspacing=1.0, labelspacing=.25, fontsize=5.8)
    return drawn


def panel_tradeoff(ax, ladder, n=20000, instance="unique_top"):
    """(b) best tested deviation per mechanism variant, with the revenue gap printed beside each row.

    A scatter of the two measures is unreadable here because every monitored variant sits at essentially the same
    point, so identity is carried by position on a category axis instead, and the revenue gap by a printed value.
    """
    rows = [r for r in ladder if int(r["n"]) == n and r["instance"] == instance]
    if not rows:
        return False
    by_v = {}
    for r in rows:
        by_v.setdefault(r["variant"], {})[r["profile"]] = r
    order = ["esp_nomon", "mesp_windowed", "esp_mon_nofb", "mesp_rawprice", "esp_ucbfb", "esp_excl", "mesp"]
    label = {"mesp": "MESP", "esp_nomon": "no monitor", "esp_excl": "exclusion", "esp_ucbfb": "UCB fallback",
             "mesp_rawprice": "no price correction", "mesp_windowed": "windowed monitor", "esp_mon_nofb": "round robin"}
    pts = []
    for v in order:
        d = by_v.get(v)
        if not d or "s_star" not in d:
            continue
        gains = [float(x["focal_gain_per_round_mean"]) for p, x in d.items() if p.startswith("focal_")]
        if not gains:
            continue
        seq = d.get("joint_sequential")
        survived = seq is not None and int(seq["honest_benchmark_violated"]) == 0
        pts.append((label[v], max(gains), float(d["s_star"]["gap_private_per_round_mean"]), survived))
    if not pts:
        return False
    y = np.arange(len(pts))
    for k, (lab, expl, rev, surv) in enumerate(pts):
        col = C["blue"] if surv else C["vermillion"]
        ax.plot([max(expl, 1e-4)], [k], marker="o" if surv else "s", markersize=5.2, color=col,
                markerfacecolor=col if surv else "white", markeredgewidth=1.1, linestyle="none")

    ax.set_yticks(y); ax.set_yticklabels([f"{p[0]}  ({p[2]:+.3f})" for p in pts], fontsize=6.0)
    ax.set_xscale("log"); ax.set_xlim(1.2e-4, 1.0)
    ax.grid(alpha=.5, linewidth=.5, axis="x"); ax.set_axisbelow(True)
    ax.set_xlabel(f"Deviation gain per round ($n={n//1000}$k)", labelpad=2)
    ax.plot([], [], marker="o", color=C["blue"], linestyle="none", markersize=5.2, label="honest benchmark held")
    ax.plot([], [], marker="s", color=C["vermillion"], markerfacecolor="white", linestyle="none", markersize=5.2,
            label="honest benchmark lost")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5, -.26), ncol=2, handlelength=1.0,
              borderpad=.1, columnspacing=1.0, fontsize=5.8)
    ax.set_ylim(-.7, len(pts) - .3)
    return True


def panel_contextual(ax, ctx, env="separator", grid="equalized"):
    """(c) exact in-class exploitability of Static Grid-ETC against the out-of-scope stress test.

    Two in-class deviators are drawn: the top deviator, whose exact gain reaches zero, and the mixed deviator
    that is non-top below the separator and top above it, whose gain is still positive at the largest horizon.
    Drawing only the first would overstate the result and only the second would hide that the gain can vanish.
    The stress test is the top deviator's, which is the largest out-of-scope gain measured.
    """
    def series(focal):
        rs = sorted([r for r in ctx if r["env"] == env and int(r["focal"]) == focal and r["grid"] == grid],
                    key=lambda r: int(r["n"]))
        rs = [r for r in rs if float(r["Kq_J_over_n"]) <= 1.0]   # above 1 the rule never commits
        return rs
    top, mixed = series(0), series(2)
    if not top or not mixed:
        return False
    floor = 4e-3   # zeros are drawn on this line; every positive measured value lies above it
    for rs, col, mk, lab, fill in ((top, C["green"], "o", "top dev., in class", True),
                                   (mixed, C["sky"], "v", "mixed dev., in class", False)):
        n = np.array([int(r["n"]) for r in rs], float)
        y = np.array([float(r["exploit_full_per_round"]) for r in rs])
        pos = y > floor
        ax.plot(n[pos], y[pos], color=col, marker=mk, markersize=3.6, linewidth=1.5,
                markerfacecolor=col if fill else "white", markeredgewidth=1.0,
                linestyle="-" if fill else (0, (3, 1.6)), label=lab)
        if (~pos).any():
            ax.plot(n[~pos], np.full((~pos).sum(), floor), color=col, marker=mk, markersize=3.6,
                    markerfacecolor="white", markeredgewidth=1.0, linestyle="none")
            ax.annotate("exactly 0", (n[~pos][0], floor), textcoords="offset points", xytext=(2, 4),
                        fontsize=5.6, color=C["ink"], ha="left")
    ns = np.array([int(r["n"]) for r in top], float)
    out = np.array([float(r["stress_per_round"]) for r in top])
    ax.plot(ns, out, color=C["vermillion"], marker="D", markersize=3.6, linewidth=1.5,
            linestyle=(0, (5, 2)), label="outside the class")
    style_axis(ax, "Horizon $n$", "Utility gain per round", logx=True, logy=True)
    horizon_ticks(ax, [8000, 128000, 2000000])
    ax.tick_params(axis="x", labelsize=5.9)
    ax.set_ylim(floor * .6, out.max() * 3.0)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5, -.26), ncol=1, handlelength=1.5,
              borderpad=.1, labelspacing=.22, fontsize=5.8)
    return True


def panel_provider(ax, rows, dataset="fashion_mnist", meta=None):
    """(d) provider bank: real labeled tasks and real provider answers, with the effort choice scripted.

    Shows the mechanism's reward under the proposed profile and under full sabotage, against the second measured
    capacity and the best honest intrinsic mean, for the monitored mechanism and for the same mechanism without a
    monitor. The separation under sabotage is the honest-benchmark claim on real outcomes.
    """
    rows = [r for r in rows if r.get("dataset", dataset) == dataset]
    if not rows:
        return False
    series = [("mesp", "proposed", C["blue"], "o", "-"), ("mesp", "bait_zero", C["blue"], "s", (0, (4, 2))),
              ("esp_nomon", "bait_zero", C["vermillion"], "D", (0, (1, 1)))]
    lab = {("mesp", "proposed"): "monitored, profile", ("mesp", "bait_zero"): "monitored, sabotage",
           ("esp_nomon", "bait_zero"): "unmonitored, sabotage"}
    drew = False
    for var, beh, col, mk, ls in series:
        rs = sorted([r for r in rows if r["variant"] == var and r["behavior"] == beh], key=lambda r: int(r["n"]))
        if not rs:
            continue
        x = [int(r["n"]) for r in rs]; y = [float(r["mean_reward_per_round"]) for r in rs]
        ax.plot(x, y, color=col, marker=mk, markersize=3.6, linewidth=1.5, linestyle=ls, label=lab[(var, beh)])
        drew = True
    if not drew:
        return False
    m2 = float(rows[0]["M2_play"])
    ax.axhline(m2, color=C["muted"], linewidth=.9, linestyle=":")
    ax.annotate("$M_{(2)}$", (2000, m2), textcoords="offset points", xytext=(0, 3), fontsize=5.8, color=C["muted"])
    muh = rows[0].get("mu_H_star_play") or rows[0].get("mu_H_star")
    if not muh and meta:
        mu_p, hon = meta.get("mu_pooled"), meta.get("honest")
        if mu_p and hon is not None:
            muh = max(mu_p[i] for i in hon)
    if muh:
        ax.axhline(float(muh), color=C["muted"], linewidth=.9, linestyle=(0, (2, 2)))
        ax.annotate("$\\mu_H^\\star$", (2000, float(muh)), textcoords="offset points", xytext=(0, -9),
                    fontsize=5.8, color=C["muted"])
    style_axis(ax, "Horizon $n$", "Platform reward per round", logx=True)
    horizon_ticks(ax, sorted({int(r["n"]) for r in rows}))
    ax.set_ylim(0, 1.0)
    ax.legend(frameon=False, loc="lower left", handlelength=1.7, borderpad=.2, labelspacing=.25, fontsize=5.8)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); runs = Path(a.runs); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cells = read_csv(runs / "final/exploitability/exploitability_grid.csv")
    search = read_json_dir(runs / "final/search", "search_*.json")
    ladder = read_csv(runs / "final/ablations/ladder_final.csv") or read_csv(runs / "pilot/ablations/ladder_pilot.csv")
    ctx = read_csv(runs / "pilot/contextual_exact/exact_exploitability.csv")
    prov = read_csv(runs / "final/provider_bank/fashion_mnist_final_summary.csv")
    pj = runs / "final/provider_bank/fashion_mnist_final.json"
    prov_meta = json.loads(pj.read_text()).get("meta") if pj.exists() else None
    fig, axs = plt.subplots(1, 4, figsize=(7.1, 2.35))
    ok = [panel_exploitability(axs[0], cells, search), panel_tradeoff(axs[1], ladder),
          panel_contextual(axs[2], ctx), panel_provider(axs[3], prov, meta=prov_meta)]
    for k, (ax, letter) in enumerate(zip(axs, "abcd")):
        ax.text(-.02, 1.06, f"({letter})", transform=ax.transAxes, fontsize=8, fontweight="bold", color=C["ink"])
        if not ok[k]:
            ax.text(.5, .5, "input not available yet", transform=ax.transAxes, ha="center", va="center",
                    color=C["muted"], fontsize=7)
            ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(w_pad=2.4)
    for ext in ("pdf", "png"):
        fig.savefig(out / f"main_experiments.{ext}", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}/main_experiments.pdf  (panels available: {sum(ok)} of 4: {dict(zip('abcd', ok))})")


if __name__ == "__main__":
    main()
