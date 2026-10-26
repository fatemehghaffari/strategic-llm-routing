"""Figures for package A5. Reads ONLY the aggregated CSVs in experiments/data/A5/.

    python make_figures_a5.py --csv experiments/data/A5 --out figures/a5

Palette and conventions follow make_figures_a4.py: project categorical slots,
every series DIRECTLY LABELLED rather than put in a legend box, underlying
numbers committed as CSV.

a5_fig1_provider_scaling: platform revenue per round against the number of
providers. The scalar mechanism is deliberately NOT drawn here: this CSV
carries no compliant-conviction column, and its revenue is not comparable
without one (see fig 2).

a5_fig2_revenue_vs_legitimacy: revenue per round for every arm over the 880
leaderboard cells, with the compliant-conviction rate printed against the two
arms that record it. The scalar mechanism earns more than the contextual one
and convicts compliant providers almost half the time; the figure is built so
that the two facts cannot be read apart.
"""
import argparse, csv, os, collections

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7"]
INK, INK2, MUTED = "#1b1b1b", "#4a4a4a", "#8a8a8a"
GRID = "#e3e3e0"


def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=7, length=3, width=0.8)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def mean(xs):
    xs = [x for x in xs if x not in ("", None)]
    return sum(map(float, xs)) / len(xs) if xs else None


def fig1(csvdir, out):
    rows = list(csv.DictReader(open(os.path.join(csvdir, "c3_provider_scaling.csv"))))
    Ks = sorted({int(r["K"]) for r in rows})
    series = [
        ("plmesp:plmesp_star",      "ours",                     CAT[0], "-",  2.0),
        ("router_ucb:average",      "UCB router, compliant",    CAT[1], "-",  1.4),
        ("router_ucb:exploit_slow", "UCB router, exploited",    CAT[1], "--", 1.4),
        ("second_best:cao_eqmu",    "Cao et al.",               CAT[4], "-",  1.4),
    ]
    fig, ax = plt.subplots(figsize=(3.33, 2.5), dpi=200)
    style(ax)
    for key, lab, col, ls, lw in series:
        ys = [mean([r["revenue_per_round"] for r in rows
                    if r["arm"] == key and int(r["K"]) == k]) for k in Ks]
        ax.plot(Ks, ys, ls, color=col, lw=lw, marker="o", ms=2.6, zorder=3)
        ax.annotate(lab, (Ks[-1], ys[-1]), xytext=(3, 0), textcoords="offset points",
                    color=col, fontsize=6.4, va="center")
    for key, lab, dash in [("second_cap", "second capability", (3, 2)),
                           ("honest_bench", "honest benchmark", (1, 2))]:
        ys = [mean([r[key] for r in rows if int(r["K"]) == k]) for k in Ks]
        ax.plot(Ks, ys, color=MUTED, lw=0.9, dashes=dash, zorder=2)
        ax.annotate(lab, (Ks[-1], ys[-1]), xytext=(3, 0), textcoords="offset points",
                    color=MUTED, fontsize=6.0, va="center")
    ax.set_xlabel("number of providers $K$", color=INK2, fontsize=7.5)
    ax.set_ylabel("platform revenue per round", color=INK2, fontsize=7.5)
    ax.set_xticks(Ks)
    ax.set_xlim(min(Ks) - 0.6, max(Ks) + 7.2)
    fig.tight_layout(pad=0.3)
    p = os.path.join(out, "a5_fig1_provider_scaling.pdf")
    fig.savefig(p); plt.close(fig); print("wrote", p)


def fig2(csvdir, out):
    rows = list(csv.DictReader(open(os.path.join(csvdir, "c3_leaderboard_replicate.csv"))))
    agg = collections.OrderedDict()
    for r in rows:
        agg.setdefault(r["arm"], []).append(r)
    name = {
        "plmesp:plmesp_star": "ours (context-local)",
        "mesp_scalar:mesp_star": "pooled, one price",
        "router_ucb:average": "UCB router, compliant",
        "router_eps:average": "$\\varepsilon$-greedy router, compliant",
        "router_greedy:average": "greedy router, compliant",
        "router_ucb:exploit_slow": "UCB router, exploited",
        "router_ucb:exploit_fast": "UCB router, exploited (fast)",
        "router_eps:exploit_slow": "$\\varepsilon$-greedy router, exploited",
        "router_greedy:exploit_slow": "greedy router, exploited",
        "second_best:cao_eqmu": "Cao et al.",
        "second_best:cao_eq0": "Cao et al. (variant)",
    }
    items = []
    for arm, rs in agg.items():
        items.append((name.get(arm, arm),
                      mean([r["revenue_per_round"] for r in rs]),
                      mean([r.get("compliant_conviction_rate") for r in rs])))
    items.sort(key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(3.33, 2.9), dpi=200)
    style(ax)
    ax.grid(axis="y", lw=0); ax.grid(axis="x", color=GRID, lw=0.6)
    for i, (lab, rev, cc) in enumerate(items):
        if lab.startswith("ours"):
            col, a = CAT[0], 1.0
        elif lab.startswith("pooled"):
            col, a = CAT[3], 1.0
        elif "Cao" in lab:
            col, a = CAT[4], 0.9
        else:
            col, a = CAT[1], 0.55 if "exploited" in lab else 0.9
        ax.barh(i, rev, color=col, alpha=a, height=0.66, zorder=3)
        ax.annotate(f"{rev:.3f}", (rev, i), xytext=(3, 0), textcoords="offset points",
                    fontsize=6.2, va="center", color=INK2)
        if cc is not None:
            # inside the bar, so a long note cannot overflow the column
            ax.annotate(f"{cc:.0%} false convictions", (rev, i), xytext=(-4, 0),
                        textcoords="offset points", fontsize=5.8, va="center",
                        ha="right", color="white", weight="bold")
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([t[0] for t in items], fontsize=6.4, color=INK)
    ax.set_xlabel("platform revenue per round, 880 cells", color=INK2, fontsize=7.5)
    ax.set_xlim(0, max(t[1] for t in items) * 1.30)
    fig.tight_layout(pad=0.3)
    p = os.path.join(out, "a5_fig2_revenue_vs_legitimacy.pdf")
    fig.savefig(p); plt.close(fig); print("wrote", p)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="experiments/data/A5")
    ap.add_argument("--out", default="figures/a5")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fig1(a.csv, a.out); fig2(a.csv, a.out)
