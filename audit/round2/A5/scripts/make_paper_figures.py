"""Every experiment figure of the paper, in one style, from committed data only.

    python audit/round2/A5/scripts/make_paper_figures.py --out figures/paper

Reads experiments/data/{A2,A3,A4,A5}, experiments/llm_effort/results, the J traces on scratch and
audit/round2/A5/B_sim/v3_agg_2026-09-29.csv. For every figure it writes the composite PDF + 300 dpi
PNG (used by the contact sheet); for every multi-panel figure it also writes one file per panel
(`fig_<name>_a.pdf`, ...) without panel letters, and, where the panels share their series, one
legend strip (`fig_<name>_legend.pdf`) so that LaTeX subfigures carry a single legend. Every
plotted number goes to values_paper.csv once; MANIFEST.md lists data, series, headline numbers and
the size of every per-panel file. Style: figstyle.py.
"""
import argparse, glob, json, os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "../../A4/scripts"))
import figstyle as fs  # noqa: E402
from figstyle import METHODS, REFS, INK, INK2, MUTED, GRID, PALE, SURFACE, SINGLE, DOUBLE, rec, style, letter, kfmt, pct, logticks, series, band, ref, handle, ref_handle, legend_below, bar_label, save, few_ticks, legend_strip  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "../../../.."))
D = os.path.join(REPO, "experiments/data")
JDIR = os.environ.get("J_TRACES") or (os.path.join(REPO, "experiments/data/J") if os.path.isdir(os.path.join(REPO, "experiments/data/J")) else "<workspace>/J")   # trace data for the dynamics figures
LLM = os.path.join(REPO, "experiments/llm_effort/results")
ORDER7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


def C(key): return METHODS[key][1]
def M(key): return METHODS[key][2]
def L(key): return METHODS[key][0]


def multi(out, name, panels, widths, height, shared=None, manifest=None, wspace=0.35, bottom=0.32, shared_ncol=None):
    """Composite + per-panel files + optional legend strip.

    panels: list of (letter, draw_fn, mode); draw_fn(ax, own) draws one panel and returns True when it
    placed a legend of its own; mode is "own" or "shared". widths: per-panel widths in inches for the
    standalone files (they sum to 7.0 minus the gaps). shared: (handles, labels) of the strip."""
    fs.RECORDING = True
    f, axs = plt.subplots(1, len(panels), figsize=(DOUBLE, height), gridspec_kw={"width_ratios": widths, "wspace": wspace})
    for ax, (let, fn, mode) in zip(np.atleast_1d(axs), panels):
        style(ax); fn(ax, mode == "own"); letter(ax, f"({let})")
    if shared is not None:
        f.subplots_adjust(left=0.075, right=0.995, top=0.9, bottom=bottom, wspace=wspace)
        f.legend(handles=shared[0], labels=shared[1], ncol=shared_ncol or len(shared[0]), loc="lower center", bbox_to_anchor=(0.5, 0.0))
        save(f, name, out, manifest, tight=False)
    else:
        save(f, name, out, manifest)
    files = []
    fs.RECORDING = False
    for (let, fn, mode), w in zip(panels, widths):
        f, ax = plt.subplots(figsize=(w, height)); style(ax); has = fn(ax, mode == "own")
        save(f, f"{name}_{let}", out); files.append(dict(file=f"{name}_{let}.pdf", width=w, height=height, legend="own legend" if has else ("shared strip" if mode == "shared" else "none")))
    if shared is not None:
        legend_strip(shared[0], shared[1], f"{name}_legend", out, ncol=shared_ncol); files.append(dict(file=f"{name}_legend.pdf", width="auto (one row)", height=0.35, legend="strip"))
    fs.RECORDING = True
    fs.MANIFEST[-1]["files"] = files


# ----------------------------------------------------------------------------- 1. premise
def fig_premise(out):
    cap = pd.read_csv(f"{D}/A4/capabilities_finite_5shot.csv")
    t = cap.pivot(index="model", columns="context", values="M")[ORDER7]
    best = sorted(set(t.idxmax(axis=0).values))                      # the models that are pointwise best somewhere
    hi_col = {m: c for m, c in zip(sorted(best, key=lambda m: -t.loc[m].mean()), ["#009E73", "#0072B2"])}
    f, ax = fs.panels(1, SINGLE, 2.1); x = np.arange(len(ORDER7))
    others = [m for m in t.index if m not in hi_col]
    for m in others:
        ax.plot(x, t.loc[m].values, lw=0.9, color="#c9c9c6", alpha=0.9, zorder=2)
        for c_, v in zip(ORDER7, t.loc[m].values): rec("fig_premise", "", m, c_, v, highlighted=False)
    for m in hi_col:
        ax.plot(x, t.loc[m].values, lw=1.9, color=hi_col[m], marker="o", ms=4.2, mec=SURFACE, mew=0.7, zorder=3, label=m)
        for c_, v in zip(ORDER7, t.loc[m].values): rec("fig_premise", "", m, c_, v, highlighted=True)
    for m, yv in {m: float(t.loc[m].values[-1]) for m in hi_col}.items():
        ax.annotate(m, (x[-1] + 0.12, yv), fontsize=7, va="center", color=INK, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels([("\n" + o) if i % 2 else o for i, o in enumerate(ORDER7)]); ax.set_xlim(-0.3, len(ORDER7) + 0.9)
    ax.set_ylabel("measured capability $M_i(x)$"); few_ticks(ax)
    hs = [Line2D([], [], color=hi_col[m], lw=1.9, marker="o", ms=4.2, mec=SURFACE, mew=0.7, label=m) for m in hi_col] + [Line2D([], [], color="#c9c9c6", lw=0.9, label=f"{len(others)} other models")]
    legend_below(ax, hs, ncol=3, y=-0.3)
    lo, hi = float(t.values.min()), float(t.values.max())
    save(f, "fig_premise", out, dict(panels="1", data="A4/capabilities_finite_5shot.csv (RouterBench, 5-shot): capability of 11 models on 7 benchmark families", series=f"highlighted: {list(hi_col)} (the two models that are pointwise best on some family); {len(others)} other models in light grey",
                                     headline=f"GPT-4 is pointwise best on six of the seven families and Claude-V2 on the seventh; capabilities range {lo:.3f} to {hi:.3f}", files=[dict(file="fig_premise.pdf", width=SINGLE, height=2.1, legend="own legend below")]))


# ----------------------------------------------------------------------------- 2. two worlds + best deviation
# Exact-size one-column panels (Figures 3 to 5 of the paper): every panel file is drawn at its print width and a
# common height, with its axes at a fixed position in inches, so neighbouring panels line up and print at 1:1.
COLW_IN = 241.1475 / 72.27                                # acmart sigconf column width (241.15 TeX pt) in inches
SMALL_TICK, SMALL_LABEL, SMALL_ANN = 6, 6.5, 6            # type sizes at print size


def exact_axes(f, w, h, left, right, bot, top, x0=0.0):
    W, H = f.get_size_inches(); return f.add_axes([(x0 + left) / W, bot / H, (w - left - right) / W, (h - bot - top) / H])


def small_ticks(ax):
    ax.tick_params(axis="both", labelsize=SMALL_TICK, pad=1.5, length=2)


def fig_two_worlds(out):
    # One-column figure: (a) and (b) print at 0.56 and 0.42 of the column. Each panel file is drawn at exactly that
    # width and at the same height, with its axes at the same vertical position, so the rows of (b) line up with the
    # rule names of (a) and (b) omits them. Bars, whiskers and reference lines carry no numbers; (b) names the best
    # deviation's kind; one legend strip under both panels names the encodings.
    h = pd.read_csv(f"{D}/A4/headline_summary.csv"); q = h[h.family_set == "Q3"]
    ncell = q.groupby(["triple", "alpha"]).ngroups
    g = q.groupby("mech")[["nonstrategic", "strategic", "oracle", "second_cap", "honest_bench"]].agg(["mean", "min"])
    order = [("plmesp", "ours"), ("mesp_scalar", "pooled"), ("router_ucb", "ucb"), ("router_eps", "eps"), ("router_greedy", "greedy")]
    d = pd.read_csv(f"{D}/A4/fine_shading_best.csv"); best = d.loc[d.groupby("mech").gain_per_round.idxmax()].set_index("mech")
    assert all(m in best.index for m, _ in order), "panel (b) shares the rows of panel (a), so it needs every rule"
    NAME = {"ours": "MESP", "pooled": "single-price\nMESP", "ucb": "UCB", "eps": "ε-greedy", "greedy": "greedy"}
    COLW = 241.1475 / 72.27                                 # acmart sigconf column width (241.15 TeX pt) in inches
    WA, WB, HH = 0.56 * COLW, 0.42 * COLW, 1.22
    BOT, TOP, LA, RA, LB, RB = 0.29, 0.04, 0.56, 0.09, 0.06, 0.05
    FT, FL, FA = 6, 6.5, 6                                  # tick labels, axis labels, annotations (pt, print size)
    ypos = np.arange(len(order))[::-1]; HB, ABR = 0.34, 0.42

    def rows(ax, names):
        ax.set_yticks(ypos); ax.set_yticklabels([NAME[k] for _, k in order] if names else [""] * len(order))
        for t in ax.get_yticklabels(): t.set_linespacing(0.9)
        ax.set_ylim(-0.6, len(order) - 0.4); ax.yaxis.is_category = True
        ax.tick_params(axis="y", length=0, labelsize=FT, pad=2); ax.tick_params(axis="x", labelsize=FT, pad=1.5, length=2)
        ax.spines["left"].set_visible(names)

    def pa(a):
        style(a, grid=None)
        for i, (mech, key) in enumerate(order):
            ns, nsmin = g.loc[mech, ("nonstrategic", "mean")], g.loc[mech, ("nonstrategic", "min")]
            st, stmin = g.loc[mech, ("strategic", "mean")], g.loc[mech, ("strategic", "min")]
            y1, y2 = ypos[i] + HB / 2 + 0.02, ypos[i] - HB / 2 - 0.02
            a.barh(y1, ns, HB, color=C(key), lw=0, zorder=3); a.barh(y2, st, HB, color=C(key), alpha=ABR, lw=0, zorder=3)
            a.errorbar([ns, st], [y1, y2], xerr=[[ns - nsmin, st - stmin], [0, 0]], fmt="none", ecolor=INK2, elinewidth=0.6, capsize=1.4, capthick=0.6, zorder=4)
            rec("fig_two_worlds", "a", key, "compliant", ns, worst_cell=nsmin); rec("fig_two_worlds", "a", key, "best-responding", st, worst_cell=stmin)
        for k2, col in (("oracle", "oracle"), ("second_cap", "second"), ("honest_bench", "honest")):
            ref(a, g[(k2, "mean")].mean(), col, axis="v", lw=0.9); rec("fig_two_worlds", "a", col, "reference", g[(k2, "mean")].mean())
        rows(a, True); a.set_xlim(0, 0.8); a.set_xticks([0, 0.2, 0.4, 0.6, 0.8]); a.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8"])
        a.set_xlabel("revenue per round", fontsize=FL, labelpad=1.5)

    def pb(b):
        style(b, grid=None); xmax = 0.12
        for i, (mech, key) in enumerate(order):
            r = best.loc[mech]; b.barh(ypos[i], r.gain_per_round, HB, color=C(key), lw=0, zorder=3)
            kind = "undercut" if r.deviation_kind == "undercut" else f"shade to {float(r.deviation_param):.0%}"
            b.text(r.gain_per_round + 0.025 * xmax, ypos[i], kind, va="center", ha="left", fontsize=FA, color=INK2, zorder=5)
            rec("fig_two_worlds", "b", key, "best single deviation, gain per round", r.gain_per_round, deviation_kind=r.deviation_kind, deviation_param=r.deviation_param, revenue_loss_per_round=r.revenue_loss_per_round)
        rows(b, False); b.set_xlim(0, xmax); b.set_xticks([0, 0.05, 0.10]); b.set_xticklabels(["0", "0.05", "0.10"])
        b.set_xlabel("deviator's gain per round", fontsize=FL, labelpad=1.5)

    def axes_in(f, w, left, right, x0=0.0):
        W, H = f.get_size_inches(); return f.add_axes([(x0 + left) / W, BOT / H, (w - left - right) / W, (HH - BOT - TOP) / H])

    # whisker handle: an errorbar container drawn on a throwaway axes, so the strip shows the same capped hairline
    _f, _a = plt.subplots(); whisk = _a.errorbar([0], [0], xerr=[[1], [0]], fmt="none", ecolor=INK2, elinewidth=0.6, capsize=1.4, capthick=0.6); plt.close(_f)
    bestcap = Line2D([], [], color=REFS["oracle"][1], ls=REFS["oracle"][2], lw=1.0)
    # column-major fill of a 2 x 3 strip: row 1 = compliant, best-responding, worst configuration; row 2 = the three reference lines
    hs = [Patch(color=MUTED, lw=0), bestcap, Patch(color=MUTED, alpha=ABR, lw=0), ref_handle("second"), whisk, ref_handle("honest")]
    labs = ["compliant", "best capability", "best-responding", "second capability", "worst configuration", "honest benchmark"]
    GAP = 0.02 * COLW
    fs.RECORDING = True
    f = plt.figure(figsize=(WA + GAP + WB, HH)); a = axes_in(f, WA, LA, RA); pa(a); letter(a, "(a)"); b = axes_in(f, WB, LB, RB, x0=WA + GAP); pb(b); letter(b, "(b)")
    save(f, "fig_two_worlds", out, dict(panels="a, b (horizontal bars, rules on the y axis of (a); (b) shares those rows)", data=f"A4/headline_summary.csv, family_set Q3 only: {ncell} cells = 3 triples (highflip, lowflip, midflip: Claude-Instant-V1|Claude-V1|GPT-4, Claude-Instant-V1|Claude-V1|Claude-V2, Claude-V2|Llama-70B|Mixtral-8x7B) x 5 intrinsic-level settings (alpha 0.00, 0.25, 0.50, 0.75, het), n = 300,000, 10 seeds per cell; bar = mean over the 15 cells, whisker to the worst cell; A4/fine_shading_best.csv, the largest gain_per_round over cells and deviation kinds per rule (undercut for the routers, a shade for the two mechanisms)",
        series="ours, pooled, ucb, eps, greedy; one-column layout, panel files at 0.56 and 0.42 of the column (exact size, 6 to 6.5 pt type), no value labels, legend strip in two rows", headline=f"(a) compliant / best-responding: ours {g.loc['plmesp',('nonstrategic','mean')]:.3f} / {g.loc['plmesp',('strategic','mean')]:.3f}, pooled {g.loc['mesp_scalar',('nonstrategic','mean')]:.3f} / {g.loc['mesp_scalar',('strategic','mean')]:.3f}, UCB {g.loc['router_ucb',('nonstrategic','mean')]:.3f} / {g.loc['router_ucb',('strategic','mean')]:.3f}; honest benchmark {g[('honest_bench','mean')].mean():.3f}; (b) best single deviation found: eps {best.loc['router_eps','gain_per_round']:.4f} (undercut), UCB {best.loc['router_ucb','gain_per_round']:.4f} (undercut), greedy {best.loc['router_greedy','gain_per_round']:.4f}, pooled {best.loc['mesp_scalar','gain_per_round']:.4f}, ours {best.loc['plmesp','gain_per_round']:.4f} (a shade; the committed fine_shading.csv puts the undercut against ours at 0.0001 in the worst cell)"))
    fs.RECORDING = False
    f = plt.figure(figsize=(WA, HH)); pa(axes_in(f, WA, LA, RA)); save(f, "fig_two_worlds_a", out, exact=True)
    f = plt.figure(figsize=(WB, HH)); pb(axes_in(f, WB, LB, RB)); save(f, "fig_two_worlds_b", out, exact=True)
    legend_strip(hs, labs, "fig_two_worlds_legend", out, ncol=3, fontsize=6.5)
    fs.RECORDING = True
    fs.MANIFEST[-1]["files"] = [dict(file="fig_two_worlds_a.pdf", width=round(WA, 4), height=HH, legend="shared strip"), dict(file="fig_two_worlds_b.pdf", width=round(WB, 4), height=HH, legend="shared strip"), dict(file="fig_two_worlds_legend.pdf", width="auto (two rows)", height=0.35, legend="strip")]


# ----------------------------------------------------------------------------- 3. provider scaling
def fig_scaling(out):
    d = pd.read_csv(f"{D}/A5/c3_provider_scaling.csv"); Ks = sorted(d.K.unique())
    f, ax = fs.panels(1, SINGLE, 1.9)
    sc = [d[d.K == k].second_cap.mean() for k in Ks]; hb = [d[d.K == k].honest_bench.mean() for k in Ks]
    ax.plot(Ks, sc, color=REFS["second"][1], ls=REFS["second"][2], lw=1.0, label=REFS["second"][0], zorder=1); ax.plot(Ks, hb, color=REFS["honest"][1], ls=REFS["honest"][2], lw=1.0, label=REFS["honest"][0], zorder=1)
    vals = {}
    for arm, key in (("plmesp:plmesp_star", "ours"), ("router_ucb:average", "ucb"), ("second_best:cao_eqmu", "cao")):
        v = [d[(d.arm == arm) & (d.K == k)].revenue_per_round.mean() for k in Ks]; vals[key] = v
        series(ax, Ks, v, key)
        for k, val in zip(Ks, v): rec("fig_scaling", "", key, k, val)
    for k, s_, h_ in zip(Ks, sc, hb): rec("fig_scaling", "", "second", k, s_); rec("fig_scaling", "", "honest", k, h_)
    ax.set_xlabel("number of providers $K$"); ax.set_ylabel("revenue per round"); ax.set_xticks(Ks); few_ticks(ax)
    legend_below(ax, ncol=3, y=-0.36)
    save(f, "fig_scaling", out, dict(panels="1", data="A5/c3_provider_scaling.csv, n = 3e6, mean over subsets", series="ours, ucb (compliant providers), cao; second capability and honest benchmark",
                                     headline=f"ours {vals['ours'][0]:.3f} at K=3 to {vals['ours'][-1]:.3f} at K=20; Cao {vals['cao'][0]:.3f} to {vals['cao'][-1]:.3f}; UCB {vals['ucb'][0]:.3f} to {vals['ucb'][-1]:.3f}", files=[dict(file="fig_scaling.pdf", width=SINGLE, height=1.9, legend="own legend below")]))


# ----------------------------------------------------------------------------- 4. arrival orders + real traffic
def fig_arrivals(out):
    # One-column figure: (a) and (b) print at 0.555 and 0.41 of the column, drawn at exactly those widths and the
    # height of Figure 3 (1.22 in), sharing one revenue axis (0 to 0.7), so (b) carries no y labels; bars have the same
    # physical width in both panels; Cao et al.'s unserved share sits level just above its bar; one legend strip.
    lb = pd.read_csv(f"{D}/A5/c3_leaderboard_replicate.csv"); orders = ["iid", "drift", "bursty", "grouped"]
    arms = [("plmesp:plmesp_star", "ours"), ("router_ucb:average", "ucb"), ("second_best:cao_eqmu", "cao")]
    v3 = pd.read_csv(f"{REPO}/audit/round2/A5/B_sim/v3_agg_2026-09-29.csv"); v3["arm"] = v3.mech + ":" + v3.profile
    m5 = v3[(v3.taskset == "merged5") & (v3.n.isin([300000, 3000000]))]
    un = [lb[(lb.arm == "second_best:cao_eqmu") & (lb.order == o) & (lb.n == 3000000)].unserved_fraction.mean() for o in orders]
    head = {key: [lb[(lb.arm == arm) & (lb.order == o) & (lb.n == 3000000)].revenue_per_round.mean() for o in orders] for arm, key in arms}
    rv = {key: [m5[(m5.arm == arm) & (m5.order == o)].revenue_per_round.mean() for o in ("iid", "real")] for arm, key in arms}
    WA, WB, HH = 0.555 * COLW_IN, 0.41 * COLW_IN, 1.22
    BOT, TOP, LA, RA, LB, RB = 0.15, 0.04, 0.36, 0.03, 0.05, 0.03
    YMAX = 0.7; WBAR, STEP = 0.2, 0.215                    # bar width and offset in (a)'s units (one unit per order)
    ua = (WA - LA - RA) / 4.0                              # inches per unit in (a), x range 4 units
    ub = (WB - LB - RB) / 2.0                              # inches per unit in (b), x range 2 units
    kb = ua / ub                                           # (b) bars get the same physical width as (a)'s

    def yaxis(ax, labels):
        ax.set_ylim(0, YMAX); ax.set_yticks([0, 0.2, 0.4, 0.6]); small_ticks(ax); ax.tick_params(axis="x", length=0); ax.xaxis.is_category = True
        if labels:
            ax.set_yticklabels(["0", "0.2", "0.4", "0.6"]); ax.set_ylabel("revenue per round", fontsize=SMALL_LABEL, labelpad=1.5)
        else:
            ax.tick_params(axis="y", labelleft=False, length=0); ax.spines["left"].set_visible(False)

    def pa(a):
        style(a, grid=None); x = np.arange(len(orders))
        for j, (arm, key) in enumerate(arms):
            a.bar(x + (j - 1) * STEP, head[key], WBAR, color=C(key), lw=0, zorder=3)
            for o, val in zip(orders, head[key]): rec("fig_arrivals", "a", key, o, val, n=3000000)
        for xi, (o, u_) in enumerate(zip(orders, un)):
            if u_ > 0: a.text(xi + STEP - WBAR / 2, head["cao"][xi] + 0.012, f"{u_:.0%}", ha="left", va="bottom", fontsize=SMALL_ANN - 0.5, color=INK2, zorder=5)
            rec("fig_arrivals", "a", "cao unserved share", o, u_)
        a.set_xlim(-0.5, 3.5); a.set_xticks(x); a.set_xticklabels(["indep.", "drift", "bursty", "grouped"]); yaxis(a, True)

    def pb(b):
        style(b, grid=None); x2 = np.arange(2)
        for j, (arm, key) in enumerate(arms):
            b.bar(x2 + (j - 1) * STEP * kb, rv[key], WBAR * kb, color=C(key), lw=0, zorder=3)
            for o, val in zip(("independent", "real"), rv[key]): rec("fig_arrivals", "b", key, o, val)
        b.set_xlim(-0.5, 1.5); b.set_xticks(x2); b.set_xticklabels(["indep.", "real"]); yaxis(b, False)

    GAP = (1.0 - 0.555 - 0.41) * COLW_IN
    fs.RECORDING = True
    f = plt.figure(figsize=(WA + GAP + WB, HH)); a = exact_axes(f, WA, HH, LA, RA, BOT, TOP); pa(a); letter(a, "(a)"); b = exact_axes(f, WB, HH, LB, RB, BOT, TOP, x0=WA + GAP); pb(b); letter(b, "(b)")
    save(f, "fig_arrivals", out, dict(panels="a, b (shared revenue axis 0 to 0.7)", data="A5/c3_leaderboard_replicate.csv (n = 3e6, 10 subsets); audit/round2/A5/B_sim/v3_agg_2026-09-29.csv merged5, both horizons", series="ours, ucb, cao; Cao unserved share annotated level above its bar; one legend strip; panel files at 0.555 and 0.41 of the column, 1.22 in tall, 6 to 6.5 pt type",
        headline=f"(a) ours {min(head['ours']):.3f} to {max(head['ours']):.3f} across orders, UCB {np.mean(head['ucb']):.3f}, Cao {head['cao'][0]:.3f} iid to {head['cao'][3]:.3f} grouped with unserved {un[1]:.0%}/{un[2]:.0%}/{un[3]:.0%}; (b) real order: ours {rv['ours'][1]:.3f}, UCB {rv['ucb'][1]:.3f}, Cao {rv['cao'][1]:.3f}"))
    fs.RECORDING = False
    f = plt.figure(figsize=(WA, HH)); pa(exact_axes(f, WA, HH, LA, RA, BOT, TOP)); save(f, "fig_arrivals_a", out, exact=True)
    f = plt.figure(figsize=(WB, HH)); pb(exact_axes(f, WB, HH, LB, RB, BOT, TOP)); save(f, "fig_arrivals_b", out, exact=True)
    legend_strip([Patch(color=C(k), lw=0) for _, k in arms], [L(k) for _, k in arms], "fig_arrivals_legend", out)
    fs.RECORDING = True
    fs.MANIFEST[-1]["files"] = [dict(file="fig_arrivals_a.pdf", width=round(WA, 4), height=HH, legend="shared strip"), dict(file="fig_arrivals_b.pdf", width=round(WB, 4), height=HH, legend="shared strip"), dict(file="fig_arrivals_legend.pdf", width="auto (one row)", height=0.35, legend="strip")]


# ----------------------------------------------------------------------------- 5. defences against provider behaviours
def fig_defences(out):
    c11 = pd.read_csv(f"{D}/A5/c11_router_static.csv"); c10 = pd.read_csv(f"{D}/A5/c10_real_order.csv")
    beh = [("average", "compliant"), ("exploit_slow", "shades\nslowly"), ("exploit_fast", "shades\nfast"), ("learning", "learns a\nbest reply")]
    f, ax = fs.panels(1, SINGLE, 1.9); x = np.arange(len(beh))
    st = [c11[(c11.order == "real") & (c11.mech == "router_static") & (c11.profile == p)].revenue_per_round.mean() for p, _ in beh]
    uc = [c10[(c10.order == "real") & (c10.mech == "router_ucb") & (c10.profile == p)].revenue_per_round.mean() for p, _ in beh]
    ours = {0: c10[(c10.order == "real") & (c10.mech == "plmesp") & (c10.profile == "plmesp_star")].revenue_per_round.mean(), 3: c10[(c10.order == "real") & (c10.mech == "plmesp") & (c10.profile == "learning")].revenue_per_round.mean()}
    series(ax, x, st, "static"); series(ax, x, uc, "ucb")
    ax.plot(list(ours), list(ours.values()), ls="none", marker=M("ours"), color=C("ours"), ms=6.5, mec=SURFACE, mew=0.8, label=L("ours"), zorder=4)
    for xi, v in zip(x, st): rec("fig_defences", "", "static", beh[xi][1].replace("\n", " "), v)
    for xi, v in zip(x, uc): rec("fig_defences", "", "ucb", beh[xi][1].replace("\n", " "), v)
    for xi, v in ours.items(): rec("fig_defences", "", "ours", beh[xi][1].replace("\n", " "), v)
    r = c10[(c10.order == "real")]; hb, sc = r.honest_bench.mean(), r.second_cap.mean(); ref(ax, sc, "second"); ref(ax, hb, "honest")
    rec("fig_defences", "", "second", "reference", sc); rec("fig_defences", "", "honest", "reference", hb)
    ax.set_xticks(x); ax.set_xticklabels([b for _, b in beh]); ax.set_ylabel("revenue per round"); ax.set_ylim(0, 0.8); few_ticks(ax)
    legend_below(ax, ncol=3, y=-0.42)
    save(f, "fig_defences", out, dict(panels="1", data="A5/c11_router_static.csv and A5/c10_real_order.csv, order = real, mean over 10 subsets and both horizons; ours has no shading points because a shading winner is convicted and the mechanism switches, so only compliant and learning are drawn",
                                      series="static, ucb, ours; second capability, honest benchmark", headline=f"static {st[0]:.3f} compliant to {st[1]:.3f} / {st[2]:.3f} / {st[3]:.3f} (slow / fast / learning); UCB {uc[0]:.3f} to {uc[1]:.3f} / {uc[2]:.3f} / {uc[3]:.3f}; ours {ours[0]:.3f} compliant, {ours[3]:.3f} learning; honest benchmark {hb:.3f}", files=[dict(file="fig_defences.pdf", width=SINGLE, height=1.9, legend="own legend below")]))


# ----------------------------------------------------------------------------- 3+5. combined: against the alternatives
def fig_alternatives(out):
    """(a) revenue against the number of providers; (b) revenue under real arrivals against provider behaviours.
    MESP's points under the two reduction schedules are read from experiments/data/A5/c13_mesp_shading.csv when that
    file exists (array 66019415). One-column figure: each panel prints at 0.485 of the column and 1.22 in tall, drawn at
    exactly that size with 6 to 6.5 pt type, thinner lines and smaller markers; one legend strip (above the panels)."""
    d = pd.read_csv(f"{D}/A5/c3_provider_scaling.csv"); Ks = sorted(d.K.unique())
    c11 = pd.read_csv(f"{D}/A5/c11_router_static.csv"); c10 = pd.read_csv(f"{D}/A5/c10_real_order.csv")
    c13p = f"{D}/A5/c13_mesp_shading.csv"; c13 = pd.read_csv(c13p) if os.path.exists(c13p) else None
    beh = [("average", "comply"), ("exploit_slow", "slow"), ("exploit_fast", "fast"), ("learning", "learn")]
    W, H = 0.485 * COLW_IN, 1.22
    BOT, TOP, LEFT, RA, RB = 0.29, 0.04, 0.30, 0.06, 0.10
    LWs, MSs, LWr = 1.3, 3.6, 0.9

    def labels(ax, xlabel):
        small_ticks(ax); ax.set_xlabel(xlabel, fontsize=SMALL_LABEL, labelpad=1.5); ax.set_ylabel("revenue per round", fontsize=SMALL_LABEL, labelpad=1.5)

    def pa(a):
        style(a, grid=None)
        sc = [d[d.K == k].second_cap.mean() for k in Ks]; hb = [d[d.K == k].honest_bench.mean() for k in Ks]
        a.plot(Ks, sc, color=REFS["second"][1], ls=REFS["second"][2], lw=LWr, zorder=1); a.plot(Ks, hb, color=REFS["honest"][1], ls=REFS["honest"][2], lw=LWr, zorder=1)
        for arm, key in (("plmesp:plmesp_star", "ours"), ("router_ucb:average", "ucb"), ("second_best:cao_eqmu", "cao")):
            v = [d[(d.arm == arm) & (d.K == k)].revenue_per_round.mean() for k in Ks]; series(a, Ks, v, key, lw=LWs, ms=MSs)
            for k, val in zip(Ks, v): rec("fig_alternatives", "a", key, k, val)
        a.set_xticks(Ks); a.set_xticklabels([str(k) for k in Ks]); a.set_xlim(Ks[0] - 1, Ks[-1] + 1); a.set_ylim(0.15, 0.65); a.set_yticks([0.2, 0.4, 0.6]); a.set_yticklabels(["0.2", "0.4", "0.6"])
        labels(a, "number of providers $K$")

    def pb(b):
        style(b, grid=None); x = np.arange(len(beh))
        st = [c11[(c11.order == "real") & (c11.mech == "router_static") & (c11.profile == p_)].revenue_per_round.mean() for p_, _ in beh]
        uc = [c10[(c10.order == "real") & (c10.mech == "router_ucb") & (c10.profile == p_)].revenue_per_round.mean() for p_, _ in beh]
        ours = {0: c10[(c10.order == "real") & (c10.mech == "plmesp") & (c10.profile == "plmesp_star")].revenue_per_round.mean(),
                3: c10[(c10.order == "real") & (c10.mech == "plmesp") & (c10.profile == "learning")].revenue_per_round.mean()}
        if c13 is not None:
            for xi, p_ in ((1, "exploit_slow"), (2, "exploit_fast")):
                v = c13[(c13.order == "real") & (c13.mech == "plmesp") & (c13.profile == p_)].revenue_per_round.mean()
                if np.isfinite(v): ours[xi] = v
        series(b, x, st, "static", lw=LWs, ms=MSs); series(b, x, uc, "ucb", lw=LWs, ms=MSs)
        xs = sorted(ours); b.plot(xs, [ours[k] for k in xs], ls="-" if len(xs) == 4 else "none", lw=LWs, marker=M("ours"), color=C("ours"), ms=MSs + 0.6, mec=SURFACE, mew=0.7, zorder=4)
        for xi, v in zip(x, st): rec("fig_alternatives", "b", "static", beh[xi][1], v)
        for xi, v in zip(x, uc): rec("fig_alternatives", "b", "ucb", beh[xi][1], v)
        for xi, v in ours.items(): rec("fig_alternatives", "b", "ours", beh[xi][1], v)
        r = c10[(c10.order == "real")]; hb, sc = r.honest_bench.mean(), r.second_cap.mean(); ref(b, sc, "second", lw=LWr); ref(b, hb, "honest", lw=LWr)
        rec("fig_alternatives", "b", "second", "reference", sc); rec("fig_alternatives", "b", "honest", "reference", hb)
        b.set_xticks(x); b.set_xticklabels([lab for _, lab in beh]); b.set_xlim(-0.3, len(beh) - 0.7); b.xaxis.is_category = True
        b.set_ylim(0, 0.8); b.set_yticks([0, 0.2, 0.4, 0.6, 0.8]); b.set_yticklabels(["0", "0.2", "0.4", "0.6", "0.8"])
        labels(b, "provider behavior")

    hs = [handle("ours"), handle("ucb"), handle("cao"), handle("static"), ref_handle("second"), ref_handle("honest")]
    for h_ in hs[:4]: h_.set_linewidth(LWs); h_.set_markersize(MSs)
    labs = [L("ours"), L("ucb"), L("cao"), L("static"), REFS["second"][0], REFS["honest"][0]]
    GAP = (1.0 - 2 * 0.485) * COLW_IN
    fs.RECORDING = True
    f = plt.figure(figsize=(2 * W + GAP, H)); a = exact_axes(f, W, H, LEFT, RA, BOT, TOP); pa(a); letter(a, "(a)"); b = exact_axes(f, W, H, LEFT, RB, BOT, TOP, x0=W + GAP); pb(b); letter(b, "(b)")
    save(f, "fig_alternatives", out, dict(panels="a, b", data="(a) A5/c3_provider_scaling.csv, n = 3e6; (b) A5/c11_router_static.csv and A5/c10_real_order.csv, order = real, mean over 10 subsets and both horizons, plus A5/c13_mesp_shading.csv for MESP under the two reduction schedules when present",
        series="ours, ucb, cao (a); static, ucb, ours (b); second capability and honest benchmark; panel files at 0.485 of the column, 1.22 in tall, 6 to 6.5 pt type; one legend strip", headline="(a) ours 0.385 at K=3 to 0.445 at K=20, Cao 0.359 to 0.246, UCB 0.323 to 0.405; (b) static 0.615 / 0.211 / 0.090 / 0.198, UCB 0.616 / 0.509 / 0.506 / 0.524, ours 0.630 compliant and 0.456 learning" + ("" if c13 is None else " plus MESP under slow and fast reduction from c13")))
    fs.RECORDING = False
    f = plt.figure(figsize=(W, H)); pa(exact_axes(f, W, H, LEFT, RA, BOT, TOP)); save(f, "fig_alternatives_a", out, exact=True)
    f = plt.figure(figsize=(W, H)); pb(exact_axes(f, W, H, LEFT, RB, BOT, TOP)); save(f, "fig_alternatives_b", out, exact=True)
    legend_strip(hs, labs, "fig_alternatives_legend", out, ncol=3)
    fs.RECORDING = True
    fs.MANIFEST[-1]["files"] = [dict(file="fig_alternatives_a.pdf", width=round(W, 4), height=H, legend="shared strip"), dict(file="fig_alternatives_b.pdf", width=round(W, 4), height=H, legend="shared strip"), dict(file="fig_alternatives_legend.pdf", width="auto (two rows)", height=0.35, legend="strip")]


# ----------------------------------------------------------------------------- 6. legitimacy
def fig_legitimacy(out):
    # One full-column panel at print size (COLW_IN x 1.25 in), 6 pt type, the short rule names of Figure 3; value
    # labels on every bar, false-switch rates beside the two mechanisms.
    lb = pd.read_csv(f"{D}/A5/c3_leaderboard_replicate.csv"); g = lb.groupby("arm").agg(rev=("revenue_per_round", "mean"), cc=("compliant_conviction_rate", "mean"), un=("unserved_fraction", "mean"))
    NAME = {"plmesp:plmesp_star": ("ours", "MESP", 1.0), "mesp_scalar:mesp_star": ("pooled", "single-price MESP", 1.0), "router_ucb:average": ("ucb", "UCB", 1.0), "router_eps:average": ("eps", "ε-greedy", 1.0),
            "router_greedy:average": ("greedy", "greedy", 1.0), "second_best:cao_eqmu": ("cao", "Cao et al., lenient", 1.0), "second_best:cao_eq0": ("cao", "Cao et al., equilibrium", 0.5)}
    g = g.loc[list(NAME)].sort_values("rev", ascending=False)
    W, H, BOT, TOP, LEFT, RIGHT = COLW_IN, 1.25, 0.29, 0.03, 0.98, 0.06
    f = plt.figure(figsize=(W, H)); ax = exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP); style(ax, grid=None)
    for i, (arm, r) in enumerate(g.iterrows()):
        key, lab, al = NAME[arm]; ax.barh(i, r.rev, 0.6, color=C(key), alpha=al, lw=0, zorder=3)
        txt = f"{r.rev:.3f}" + (f", {r.cc:.0%} false switch" if arm in ("plmesp:plmesp_star", "mesp_scalar:mesp_star") else "")
        ax.annotate(txt, (r.rev, i), xytext=(2.5, 0), textcoords="offset points", va="center", fontsize=SMALL_ANN, color=INK2)
        rec("fig_legitimacy", "", key, lab, r.rev, compliant_conviction=r.cc, unserved=r.un)
    ax.set_yticks(range(len(g))); ax.set_yticklabels([NAME[a][1] for a in g.index]); ax.set_ylim(len(g) - 0.45, -0.55); ax.yaxis.is_category = True
    ax.set_xlim(0, 0.8); ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8]); ax.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8"]); ax.set_xlabel("revenue per round", fontsize=SMALL_LABEL, labelpad=1.5)
    small_ticks(ax); ax.tick_params(axis="y", length=0, pad=2)
    save(f, "fig_legitimacy", out, dict(panels="1", data="A5/c3_leaderboard_replicate.csv, all 880 rows = 80 configurations (10 subsets x 4 orders x 2 horizons) x seeds, mean per arm; routers facing compliant providers; the exploited-router arms are in fig_two_worlds and fig_defences",
                                        series="ours, pooled, UCB, eps, greedy, Cao (lenient), Cao (equilibrium, lighter); false-switch rate of a compliant provider printed beside the two mechanisms; exact print size COLW_IN x 1.25 in, 6 pt type", headline=f"pooled {g.loc['mesp_scalar:mesp_star','rev']:.3f} with {g.loc['mesp_scalar:mesp_star','cc']:.0%} false switches; ours {g.loc['plmesp:plmesp_star','rev']:.3f} with {g.loc['plmesp:plmesp_star','cc']:.0%}; UCB {g.loc['router_ucb:average','rev']:.3f}; Cao {g.loc['second_best:cao_eqmu','rev']:.3f} and {g.loc['second_best:cao_eq0','rev']:.3f}, both leaving {g.loc['second_best:cao_eqmu','un']:.0%} of rounds unserved", files=[dict(file="fig_legitimacy.pdf", width=round(W, 4), height=H, legend="none")]), exact=True)


# ----------------------------------------------------------------------------- 7. monitor operating curve
def fig_monitors(out):
    """Monitor operating curve on the 0.05 shade: false-switch rate of a complying winner (x) against the median
    delay to detect a provider shading by 0.05 (y, log). Settings that never detect it within the horizon (median
    undefined, detect rate below one half) sit hollow in a band at the top labelled 'not detected'. Drawn at print
    size (full column, 1.45 in including a one-row legend), 6 to 6.5 pt type."""
    m = pd.read_csv(f"{D}/A4/monitor_frontier.csv"); m = m[(m.alpha == "a0.25") & (m.monitor.isin(["anytime", "fixedbuffer", "twosample"]))]
    W, H, BOT, TOP_, LEFT, RIGHT = COLW_IN, 1.45, 0.47, 0.04, 0.36, 0.08
    f = plt.figure(figsize=(W, H)); ax = exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP_); style(ax, grid=None); TOP = 1.2e5
    for key in ("fixedbuffer", "twosample", "anytime"):
        s_ = m[m.monitor == key]; k = "ours" if key == "anytime" else key
        det = s_[s_.detect_rate_mild >= 0.5]; nod = s_[s_.detect_rate_mild < 0.5]
        ax.plot(det.false_conviction_rate, det.median_delay_mild, ls="none", marker=M(k), color=C(k), ms=4.6 if k == "ours" else 3.8, mec=SURFACE, mew=0.6, zorder=4 if k == "ours" else 3)
        if len(nod): ax.plot(nod.false_conviction_rate, [TOP] * len(nod), ls="none", marker=M(k), color=C(k), ms=3.8, mfc=SURFACE, mew=0.9, zorder=3)
        for _, r in s_.iterrows(): rec("fig_monitors", "", k, r.false_conviction_rate, r.median_delay_mild, params=r.params, detect_rate_mild=r.detect_rate_mild, detect_rate_baitswitch=r.detect_rate_baitswitch, median_delay_baitswitch=r.median_delay_baitswitch, plotted_as="not detected" if r.detect_rate_mild < 0.5 else "median delay")
    for _, r in m[m.monitor == "anytime"].iterrows():
        bm = json.loads(r.params)["boundary_mult"]; ax.annotate(f"×{bm:g}", (r.false_conviction_rate, r.median_delay_mild), xytext=(4, 0), textcoords="offset points", fontsize=SMALL_ANN, color=INK2, va="center")
    ax.axhspan(TOP / 1.6, TOP * 1.6, color=PALE, alpha=0.5, lw=0, zorder=1); ax.text(0.5, TOP, "not detected", fontsize=SMALL_ANN, color=INK2, va="center", ha="center", zorder=5)
    ax.set_yscale("log"); logticks(ax, [10, 100, 1000, 10000], ["10", "100", "1K", "10K"], axis="y"); ax.set_ylim(6, TOP * 2.2)
    pct(ax, "x"); small_ticks(ax); ax.set_xlabel("false switches on a complying winner", fontsize=SMALL_LABEL, labelpad=1.5); ax.set_ylabel("median delay (pulls)", fontsize=SMALL_LABEL, labelpad=1.5)
    hs = [Line2D([], [], ls="none", marker=M("ours"), color=C("ours"), ms=4.6, mec=SURFACE, mew=0.6), Line2D([], [], ls="none", marker=M("fixedbuffer"), color=C("fixedbuffer"), ms=3.8, mec=SURFACE, mew=0.6),
          Line2D([], [], ls="none", marker=M("twosample"), color=C("twosample"), ms=3.8, mec=SURFACE, mew=0.6), Line2D([], [], ls="none", marker="o", mfc=SURFACE, mec=INK2, mew=0.9, ms=3.8)]
    f.legend(hs, ["anytime (ours)", "fixed buffer", "two-sample", "not detected"], loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=4, fontsize=SMALL_TICK, frameon=False, handletextpad=0.2, columnspacing=0.9)
    an = m[(m.monitor == "anytime")]; a1 = an[an.params.str.contains('"boundary_mult": 1.0')].iloc[0]
    ts = m[(m.monitor == "twosample") & (m.false_conviction_rate == 0)]
    save(f, "fig_monitors", out, dict(panels="1", data="A4/monitor_frontier.csv, alpha a0.25, 300 replicates, n = 300,000; x false-switch rate on a complying winner, y median delay to detect a 0.05 shade (median_delay_mild); settings with detect_rate_mild < 0.5 drawn hollow in the 'not detected' band (fixed buffer 0.2 with burn-in 1,000, 10,000 or none)",
                                      series="ours (anytime boundary at multipliers 0.25 to 2), fixed-buffer monitors, two-sample monitors; exact print size COLW_IN x 1.45 in with a one-row legend, 6 to 6.5 pt type", headline=f"ours at multiplier 1: {a1.false_conviction_rate:.0%} false switches, {a1.median_delay_mild:.0f} pulls to detect the 0.05 shade ({a1.median_delay_baitswitch:.0f} for a bait-and-switch); two-sample at 0% false switches: {ts.median_delay_mild.min():.0f} pulls; fixed buffer 0.2 never detects the 0.05 shade unless its burn-in is 100 (then 68% of runs)", files=[dict(file="fig_monitors.pdf", width=round(W, 4), height=H, legend="one row below")]), exact=True)


# ----------------------------------------------------------------------------- 8. dynamics (J1, J5)
def _load_trace(p):
    from trace import load
    return load(p)


def _dev_series(z, dev): return np.cumsum(np.where(z["agent"] == dev, z["agent_utility"], 0.0).astype(float))


def _gains(d, mech, refp, devp, dev):
    seeds = sorted({int(f[-6:-4]) for f in glob.glob(os.path.join(d, f"{mech}_{devp}_seed*.npz"))}); G = []
    for s in seeds:
        zr = _load_trace(os.path.join(d, f"{mech}_{refp}_seed{s:02d}.npz")); zd = _load_trace(os.path.join(d, f"{mech}_{devp}_seed{s:02d}.npz"))
        G.append(_dev_series(zd, dev) - _dev_series(zr, dev))
    return np.array(G), seeds


JSER = [("mesp_scalar", "proposed", "ours"), ("second_best", "proposed", "cao"), ("router_eps", "capability", "eps"), ("router_ucb", "capability", "ucb")]
SHADES = (("shadeall0.05", "-"), ("shadeall0.10", (0, (3, 1.5))))


def fig_dynamics(out):
    d20, d300 = f"{JDIR}/n20k_r2", f"{JDIR}/n300k"
    inst = json.load(open(f"{d20}/instance.json")); dev = inst["deviator"]; n = inst["n"]; t = np.arange(1, n + 1); st = 20
    inst3 = json.load(open(f"{d300}/instance.json")); n3 = inst3["n"]; t3 = np.arange(1, n3 + 1); st3 = 100
    G20 = {key: _gains(d20, mech, refp, "shadeall0.05", dev) for mech, refp, key in JSER}
    G300, R300 = {}, {}
    for mech, refp, key in JSER[:2]:
        for devp, ls in SHADES:
            G, seeds = _gains(d300, mech, refp, devp, dev); G300[(key, devp)] = (G.mean(0), len(seeds))
            R300[(key, devp)] = np.mean([np.cumsum(_load_trace(os.path.join(d300, f"{mech}_{devp}_seed{s:02d}.npz"))["reward"].astype(float)) / t3 for s in seeds], axis=0)
    head = {k: G20[k][0].mean(0)[-1] for k in G20}

    def pa(a, own):
        for mech, refp, key in JSER:
            G, seeds = G20[key]; m = G.mean(0)
            band(a, t[::st], np.percentile(G, 25, axis=0)[::st], np.percentile(G, 75, axis=0)[::st], key); series(a, t[::st], m[::st], key, nmark=6)
            for tt in (5000, 10000, 20000): rec("fig_dynamics", "a", key, tt, m[tt - 1], q25=np.percentile(G[:, tt - 1], 25), q75=np.percentile(G[:, tt - 1], 75), seeds=len(seeds))
        # the round at which the monitor switches the shading winner, averaged over seeds (first fallback round in the trace)
        sw = []
        for sd in range(10):
            z = _load_trace(os.path.join(d20, f"mesp_scalar_shadeall0.05_seed{sd:02d}.npz")); fb = np.flatnonzero(z["phase"] == 2)
            if len(fb): sw.append(int(fb[0]) + 1)
        if sw:
            a.axvline(np.mean(sw), color=INK2, lw=0.8, ls=(0, (2, 2)), zorder=2); a.annotate("switch", (np.mean(sw), 0), xytext=(3, 4), textcoords="offset points", fontsize=7, color=INK2, va="bottom")
            rec("fig_dynamics", "a", "ours", "mean switch round", float(np.mean(sw)), seeds=len(sw))
        a.axhline(0, color=PALE, lw=0.8); a.set_xlabel("round $t$"); kfmt(a); kfmt(a, "y"); a.set_ylabel("deviator's gain"); return False

    def pb(b, own):
        for mech, refp, key in JSER[:2]:
            for devp, ls in SHADES:
                m, ns = G300[(key, devp)]; series(b, t3[::st3], m[::st3], key, label=f"{L(key)}, shade {devp[-4:]}", ls=ls, nmark=6); rec("fig_dynamics", "b", key, devp, m[-1], seeds=ns)
        b.axhline(0, color=PALE, lw=0.8); b.set_xlabel("round $t$"); kfmt(b); kfmt(b, "y"); b.set_ylabel("deviator's gain"); return False

    def pc(c, own):
        for mech, refp, key in JSER[:2]:
            for devp, ls in SHADES:
                R = R300[(key, devp)]; series(c, t3[::st3], R[::st3], key, label=f"{L(key)}, shade {devp[-4:]}", ls=ls, nmark=6); rec("fig_dynamics", "c", key, devp, R[-1])
        c.set_xlabel("round $t$"); kfmt(c); c.set_ylabel("platform revenue"); c.set_ylim(0, 0.9); c.set_yticks([0, 0.3, 0.6, 0.9]); return False

    shared = ([handle(k) for _, _, k in JSER] + [Line2D([], [], color=INK2, lw=1.8, ls=ls) for _, ls in SHADES],
              [L(k) for _, _, k in JSER] + [f"shade {devp[-4:]}" for devp, _ in SHADES])
    multi(out, "fig_dynamics", [("a", pa, "shared"), ("b", pb, "shared"), ("c", pc, "shared")], [2.233, 2.233, 2.233], 1.9, shared=shared, wspace=0.42, shared_ncol=3,
          manifest=dict(panels="a, b, c", data=f"J traces {d20} (10 seeds) and {d300} (10 seeds); deviation shadeall: bid the capability, then deliver 0.05 (or 0.10) below the reference delivery in every later served round; common random numbers; IQR bands in (a)",
                        series="ours, cao, eps, ucb in (a); ours and cao at shade 0.05 solid / 0.10 dashed in (b, c), one legend strip for (b, c)", headline=f"(a) gain at n: ours {head['ours']:.0f}, Cao {head['cao']:.0f}, eps {head['eps']:.0f}, UCB {head['ucb']:.0f}; (b) at 300K ours {G300[('ours','shadeall0.05')][0][-1]:.0f} / {G300[('ours','shadeall0.10')][0][-1]:.0f}, Cao {G300[('cao','shadeall0.05')][0][-1]:.0f} / {G300[('cao','shadeall0.10')][0][-1]:.0f}; (c) platform revenue/round ours {R300[('ours','shadeall0.10')][-1]:.3f} vs Cao {R300[('cao','shadeall0.10')][-1]:.3f} at shade 0.10"))


# ----------------------------------------------------------------------------- 9. LLM effort
SUBL = {"gsm8k_short": ("GSM8K short", "#56B4E9", "o"), "gsm8k_long": ("GSM8K long", "#0072B2", "o"), "math_easy": ("MATH lvl 1-2", "#bdbdbd", "s"), "math_medium": ("MATH lvl 3", "#737373", "s"), "math_hard": ("MATH lvl 4-5", "#252525", "s")}
BUD = ["#9ec3ee", "#4f93df", "#1b5bb0"]; POL = {"fixed": ("fixed budgets", "#1b5bb0", "o"), "task_adaptive": ("task-adaptive", "#009E73", "D"), "random_matched": ("random, matched", "#7f7f7f", "s")}


def _llm_a(ax, T, lw=1.8, ms=5, elw=0.8):
    for sub, (lab, col, mk) in SUBL.items():
        g = T[T.subgroup == sub].set_index("level").loc[["low", "medium", "high"]]
        ax.plot(g.reasoning_tokens, g.accuracy, color=col, lw=lw, marker=mk, ms=ms, mec=SURFACE, mew=0.6, label=lab, zorder=3)
        ax.errorbar(g.reasoning_tokens, g.accuracy, yerr=[g.accuracy - g.acc_lo, g.acc_hi - g.accuracy], fmt="none", ecolor=col, elinewidth=elw, capsize=0, alpha=0.9)
        for lvl, r in g.iterrows(): rec("fig_llm", "a", sub, r.reasoning_tokens, r.accuracy, level=lvl, lo=r.acc_lo, hi=r.acc_hi)
    ax.set_xscale("log"); logticks(ax, [128, 512, 1024], ["128", "512", "1K"]); ax.set_xlim(105, 2100)
    lo = max(0.0, np.floor((T.acc_lo.min() - 0.02) * 20) / 20); ax.set_ylim(lo, 1.01); pct(ax); ax.set_yticks([0.6, 0.8, 1.0])


def _llm_b(ax, P, lw=1.8, ms=5, elw=0.8):
    P = P.rename(columns={"latency_s": "est_wall_s"}); fx = P.set_index("policy").loc[["fixed_low", "fixed_medium", "fixed_high"]]
    lab, col, mk = POL["fixed"]; ax.plot(fx.reasoning_tokens, fx.accuracy, color=col, lw=lw, marker=mk, ms=ms, mec=SURFACE, mew=0.6, label=lab, zorder=3)
    ax.errorbar(fx.reasoning_tokens, fx.accuracy, yerr=[fx.accuracy - fx.acc_lo, fx.acc_hi - fx.accuracy], fmt="none", ecolor=col, elinewidth=elw, capsize=0)
    for p_, r in fx.iterrows(): rec("fig_llm", "b", p_, r.reasoning_tokens, r.accuracy, lo=r.acc_lo, hi=r.acc_hi)
    for pol in ("task_adaptive", "random_matched"):
        r = P[P.policy == pol].iloc[0]; lab, col, mk = POL[pol]
        ax.errorbar([r.reasoning_tokens], [r.accuracy], yerr=[[r.accuracy - r.acc_lo], [r.acc_hi - r.accuracy]], fmt=mk, ms=ms + 0.6, color=col, mec=SURFACE, mew=0.6, ecolor=col, elinewidth=elw, capsize=0, label=lab, zorder=4)
        rec("fig_llm", "b", pol, r.reasoning_tokens, r.accuracy, lo=r.acc_lo, hi=r.acc_hi)
    pct(ax); ax.set_xlim(60, 1360); ax.set_xticks([250, 750, 1250]); ax.set_xticklabels(["250", "750", "1.25K"]); ax.set_ylim(0.855, 0.95); ax.set_yticks([0.86, 0.88, 0.90, 0.92, 0.94])


def fig_llm(out):
    # One-column figure at the size of Figure 3: each panel prints at 0.485 of the column, 1.22 in tall, drawn at
    # exactly that size with 6 to 6.5 pt type, thinner lines, smaller markers and hairline intervals; two legend strips.
    T = pd.read_csv(f"{LLM}/aggregate/table_A_levels.csv"); P = pd.read_csv(f"{LLM}/aggregate/table_C_policies.csv")
    W, H = 0.485 * COLW_IN, 1.22
    BOT, TOP, LEFT, RA, RB = 0.29, 0.04, 0.40, 0.05, 0.12
    LWs, MSs, ELW = 1.2, 3.2, 0.6

    def finish(ax):
        small_ticks(ax); ax.set_xlabel("tokens/request", fontsize=SMALL_LABEL, labelpad=1.5); ax.set_ylabel("accuracy", fontsize=SMALL_LABEL, labelpad=1.5)

    def pa(a): style(a, grid=None); _llm_a(a, T, LWs, MSs, ELW); finish(a)
    def pb(b): style(b, grid=None); _llm_b(b, P, LWs, MSs, ELW); finish(b)

    ta = P[P.policy == "task_adaptive"].iloc[0]; fh = P[P.policy == "fixed_high"].iloc[0]; rm = P[P.policy == "random_matched"].iloc[0]
    GAP = (1.0 - 2 * 0.485) * COLW_IN
    fs.RECORDING = True
    f = plt.figure(figsize=(2 * W + GAP, H)); a = exact_axes(f, W, H, LEFT, RA, BOT, TOP); pa(a); letter(a, "(a)"); b = exact_axes(f, W, H, LEFT, RB, BOT, TOP, x0=W + GAP); pb(b); letter(b, "(b)")
    save(f, "fig_llm", out, dict(panels="a, b", data="experiments/llm_effort/results/aggregate/table_A_levels.csv (subgroup rows) and table_C_policies.csv; Qwen3-4B, vLLM thinking_token_budget 128/512/2048; 150+150 held-out questions, 3 seeds",
        series="(a) five subgroups; (b) fixed budgets line, task-adaptive, random matched; panel files at 0.485 of the column, 1.22 in tall, 6 to 6.5 pt type; two legend strips", headline=f"(a) MATH level 4-5 {T[(T.subgroup=='math_hard')&(T.level=='low')].accuracy.iloc[0]:.1%} to {T[(T.subgroup=='math_hard')&(T.level=='high')].accuracy.iloc[0]:.1%}; GSM8K short {T[(T.subgroup=='gsm8k_short')&(T.level=='low')].accuracy.iloc[0]:.1%} to {T[(T.subgroup=='gsm8k_short')&(T.level=='high')].accuracy.iloc[0]:.1%}; (b) task-adaptive {ta.accuracy:.1%} at {ta.reasoning_tokens:.0f} tokens = fixed high {fh.accuracy:.1%} at {fh.reasoning_tokens:.0f}; random {rm.accuracy:.1%} at {rm.reasoning_tokens:.0f}"))
    fs.RECORDING = False
    f = plt.figure(figsize=(W, H)); pa(exact_axes(f, W, H, LEFT, RA, BOT, TOP)); save(f, "fig_llm_a", out, exact=True)
    f = plt.figure(figsize=(W, H)); pb(exact_axes(f, W, H, LEFT, RB, BOT, TOP)); save(f, "fig_llm_b", out, exact=True)
    ha = [Line2D([], [], color=c, lw=LWs, marker=m, ms=MSs, mec=SURFACE, mew=0.6, label=l) for (l, c, m) in SUBL.values()]
    legend_strip(ha, [h.get_label() for h in ha], "fig_llm_legend_a", out, ncol=3)
    hb = [Line2D([], [], color=POL["fixed"][1], lw=LWs, marker=POL["fixed"][2], ms=MSs, mec=SURFACE, mew=0.6, label=POL["fixed"][0])] + [Line2D([], [], color=POL[k][1], lw=0, marker=POL[k][2], ms=MSs + 0.6, mec=SURFACE, mew=0.6, label=POL[k][0]) for k in ("task_adaptive", "random_matched")]
    legend_strip(hb, [h.get_label() for h in hb], "fig_llm_legend_b", out, ncol=3)
    fs.RECORDING = True
    fs.MANIFEST[-1]["files"] = [dict(file="fig_llm_a.pdf", width=round(W, 4), height=H, legend="strip a"), dict(file="fig_llm_b.pdf", width=round(W, 4), height=H, legend="strip b"), dict(file="fig_llm_legend_a.pdf", width="auto (two rows)", height=0.35, legend="strip for (a)"), dict(file="fig_llm_legend_b.pdf", width="auto (one row)", height=0.35, legend="strip for (b)")]


# ----------------------------------------------------------------------------- 10. certified band and context threshold
def fig_certified(out):
    # One-column figure at the size of Figure 3: each panel prints at 0.485 of the column, 1.22 in tall, drawn at
    # exactly that size with 6 to 6.5 pt type; one legend strip below.
    g = pd.read_csv(f"{D}/A2/exact_grid.csv"); u = g[(g.family == "replicated_unique_top") & (g.Q == 1)].sort_values("n"); s = g[(g.family == "replicated_unique_top") & (g.K == 3) & (g.n == 8000)].sort_values("Q")
    W, H, BOT, TOP, LEFT, RIGHT = 0.485 * COLW_IN, 1.22, 0.29, 0.04, 0.38, 0.07
    LWs, MSs = 1.3, 3.4

    def finish(ax, xlabel):
        small_ticks(ax); ax.set_xlabel(xlabel, fontsize=SMALL_LABEL, labelpad=1.5); ax.set_ylabel("gain per round", fontsize=SMALL_LABEL, labelpad=1.5)

    def pa(a):
        style(a, grid=None); band(a, u.n, u.exploit_LB_per_round, u.exploit_UB_per_round, "ours", alpha=0.15)
        series(a, u.n, u.exploit_UB_per_round, "ours", label="upper bound", lw=LWs, ms=MSs); series(a, u.n, u.exploit_LB_per_round, "ours", label="lower bound", ls="--", marker="o", lw=LWs, ms=MSs)
        a.plot(u.n, u.prop61_gain / u.n, color=MUTED, lw=LWs, marker="o", ms=MSs - 0.4, mec=SURFACE, mew=0.6, label="hand-picked deviation", zorder=3)
        for _, r in u.iterrows(): rec("fig_certified", "a", "ours", r.n, r.exploit_UB_per_round, LB=r.exploit_LB_per_round, attained=r.prop61_gain / r.n)
        a.set_xscale("log"); a.set_yscale("log"); logticks(a, [2000, 8000, 20000], ["2K", "8K", "20K"]); logticks(a, [0.01, 0.03, 0.1], ["0.01", "0.03", "0.1"], axis="y")
        finish(a, "horizon $n$")

    def pb(b):
        style(b, grid=None); band(b, s.Q, s.exploit_LB_per_round, s.exploit_UB_per_round, "ours", alpha=0.15)
        series(b, s.Q, s.exploit_UB_per_round, "ours", label="upper bound", lw=LWs, ms=MSs); series(b, s.Q, s.exploit_LB_per_round, "ours", label="lower bound", ls="--", lw=LWs, ms=MSs)
        for _, r in s.iterrows(): rec("fig_certified", "b", "ours", r.Q, r.exploit_UB_per_round, LB=r.exploit_LB_per_round)
        b.set_xticks(sorted(s.Q.unique())); b.set_yticks([0.1, 0.2, 0.3]); finish(b, "task types $Q$")

    shared = ([handle("ours"), handle("ours", ls="--"), Line2D([], [], color=MUTED, lw=LWs, marker="o", ms=MSs - 0.4, mec=SURFACE, mew=0.6)], ["upper bound", "lower bound", "hand-picked deviation (a)"])
    for h_ in shared[0][:2]: h_.set_linewidth(LWs); h_.set_markersize(MSs)
    GAP = (1.0 - 2 * 0.485) * COLW_IN
    fs.RECORDING = True
    f = plt.figure(figsize=(2 * W + GAP, H)); a = exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP); pa(a); letter(a, "(a)"); b = exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP, x0=W + GAP); pb(b); letter(b, "(b)")
    save(f, "fig_certified", out, dict(panels="a, b", data="A2/exact_grid.csv family replicated_unique_top: (a) Q = 1 over n, exploit_LB/UB_per_round and prop61_gain/n; (b) K = 3, n = 8,000 over Q", series="ours (exact backward induction); one legend strip; panel files at 0.485 of the column, 1.22 in tall, 6 to 6.5 pt type",
        headline=f"(a) UB {u.exploit_UB_per_round.iloc[0]:.4f} at n = {int(u.n.iloc[0]):,} to {u.exploit_UB_per_round.iloc[-1]:.4f} at {int(u.n.iloc[-1]):,}, attained {u.prop61_gain.iloc[-1]/u.n.iloc[-1]:.4f}; (b) UB {s.exploit_UB_per_round.iloc[0]:.4f} at Q = 1, {s.exploit_UB_per_round.iloc[1]:.4f}, {s.exploit_UB_per_round.iloc[2]:.4f}, {s.exploit_UB_per_round.iloc[3]:.4f} at Q = 2, 3, 4"))
    fs.RECORDING = False
    f = plt.figure(figsize=(W, H)); pa(exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP)); save(f, "fig_certified_a", out, exact=True)
    f = plt.figure(figsize=(W, H)); pb(exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP)); save(f, "fig_certified_b", out, exact=True)
    legend_strip(shared[0], shared[1], "fig_certified_legend", out)
    fs.RECORDING = True
    fs.MANIFEST[-1]["files"] = [dict(file="fig_certified_a.pdf", width=round(W, 4), height=H, legend="shared strip"), dict(file="fig_certified_b.pdf", width=round(W, 4), height=H, legend="shared strip"), dict(file="fig_certified_legend.pdf", width="auto (one row)", height=0.35, legend="strip")]


# ----------------------------------------------------------------------------- 11. ablation ladder (stacked)
def fig_ladder(out):
    l = pd.read_csv(f"{D}/A2/ladder.csv"); q = l[(l.family == "replicated_unique_top") & (l.Q == 1) & (l.n == 20000)]
    rungs = [("pl_mesp", "full"), ("pl_windowed", "windowed"), ("pl_nomonitor", "no monitor"), ("pl_noslack", "no slack"), ("pl_nofallback", "round-robin"), ("pl_runnerup", "runner-up"), ("pl_rawprice", "raw requirement")]
    single = ~q.behavior.str.startswith("joint:") & (q.behavior != "profile"); joint = q.behavior.str.startswith("joint:")
    hb = float(q.honest_benchmark_per_round.iloc[0]); rows = []
    for v, lab in rungs:
        rows.append((v, lab, q[single & (q.variant == v)].gain_per_round_mean.max(), q[joint & (q.variant == v)].platform_reward_per_round_mean.min(), float(q[(q.variant == v) & (q.behavior == "profile")].false_switch_rate_per_monitored_profile.iloc[0])))

    def pa(a, own):
        style(a, "x")
        for i, (v, lab, best, worst, fsw) in enumerate(rows):
            a.barh(i, best, 0.62, color=C("ours") if v == "pl_mesp" else MUTED, zorder=3); a.annotate(f"{best:.3f}", (best, i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
            rec("fig_ladder", "a", v, lab, best)
        a.set_yticks(range(len(rows))); a.set_yticklabels([r[1] for r in rows]); a.invert_yaxis(); a.set_xlim(0, 0.56); a.set_xticks([0, 0.2, 0.4]); a.set_xlabel("best deviation per round"); return False

    def pb(b, own):
        style(b, "x")
        for i, (v, lab, best, worst, fsw) in enumerate(rows):
            b.barh(i, hb - worst, 0.62, color=C("ours") if v == "pl_mesp" else MUTED, zorder=3); b.annotate(f"{hb - worst:.3f}", (hb - worst, i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
            rec("fig_ladder", "b", v, lab, hb - worst, worst_joint_reward=worst, honest_benchmark=hb, false_switch_at_profile=fsw)
        b.set_yticks(range(len(rows))); b.set_yticklabels([r[1] for r in rows]); b.invert_yaxis(); b.set_xlim(0, 0.27); b.set_xticks([0, 0.1, 0.2]); b.set_xlabel("shortfall below honest"); return False

    fs.RECORDING = True
    f, (a, b) = plt.subplots(2, 1, figsize=(SINGLE, 2.5), sharey=True, gridspec_kw={"hspace": 0.5}); pa(a, True); letter(a, "(a)"); pb(b, True); letter(b, "(b)")
    save(f, "fig_ladder", out, dict(panels="a, b (stacked)", data="A2/ladder.csv, family replicated_unique_top, Q = 1, n = 20,000; (a) max over single-agent behaviours of gain_per_round_mean; (b) honest_benchmark_per_round minus the min over joint behaviours of platform reward; false-switch rate at the proposed profile",
                                    series="rungs: full, windowed (monitor), no monitor, no slack, round-robin (fallback), runner-up (unmonitored), raw price; per-panel files 1.6 x 1.6 in for a side-by-side single-column layout; the 99.5% false-conviction note moved to the caption", headline="best deviation 0.012 full vs 0.113 windowed vs 0.406 no monitor; shortfall 0.053 full vs 0.091 round-robin fallback vs 0.191 unmonitored runner-up / no monitor; no slack convicts a compliant winner in 99.5% of runs"))
    fs.RECORDING = False; files = []
    for let, fn in (("a", pa), ("b", pb)):
        f, ax = plt.subplots(figsize=(1.42, 1.55)); fn(ax, True); save(f, f"fig_ladder_{let}", out); files.append(dict(file=f"fig_ladder_{let}.pdf", width=1.6, height=1.6, legend="none"))
    fs.RECORDING = True; fs.MANIFEST[-1]["files"] = files


# ----------------------------------------------------------------------------- 12. monitor path (J3)
def fig_monitor_path(out):
    from trace import PHASE_CODES
    d20 = f"{JDIR}/n20k_r2"; inst = json.load(open(f"{d20}/instance.json")); z = _load_trace(f"{d20}/mesp_scalar_shadeall0.05_seed00.npz"); meta = z["meta"]
    pri = (z["phase"] == PHASE_CODES["primary"]) & (z["agent"] == meta["W"]); Z = np.cumsum(z["reward"][pri].astype(float)); r = np.arange(1, len(Z) + 1)
    tau = meta["tau"]; c0 = inst["c_boundary"]; deficit = r * tau - Z; tol = np.sqrt(r * c0); cross = int(np.argmax(deficit > tol)) + 1 if (deficit > tol).any() else len(r)
    W, H, BOT, TOP, LEFT, RIGHT = COLW_IN, 1.25, 0.29, 0.04, 0.36, 0.08
    f = plt.figure(figsize=(W, H)); ax = exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP); style(ax, grid=None)
    ax.plot(r[:cross], tol[:cross], color=MUTED, lw=1.3, label="tolerance $b_n(r)$", zorder=2); series(ax, r[:cross], deficit[:cross], "ours", label="shortfall $r\\tau - Z_r$", nmark=6, lw=1.3, ms=3.4)
    ax.axvline(cross, color=PALE, lw=0.8); ax.annotate(f"switch at pull {cross:,}", (cross, 0), xytext=(-4, 3), textcoords="offset points", ha="right", va="bottom", fontsize=SMALL_ANN, color=INK2)
    kfmt(ax); small_ticks(ax); ax.set_xlabel("winner's primary pulls $r$", fontsize=SMALL_LABEL, labelpad=1.5); ax.set_ylabel("reward units", fontsize=SMALL_LABEL, labelpad=1.5)
    ax.legend(loc="upper left", fontsize=SMALL_LABEL, handlelength=1.6, borderaxespad=0.3)
    rec("fig_monitor_path", "", "ours", cross, float(tol[cross - 1]), tau=tau, seed=0)
    save(f, "fig_monitor_path", out, dict(panels="1", data=f"{d20}/mesp_scalar_shadeall0.05_seed00.npz, primary pulls of the winner; tau = {tau:.4f}, c = {c0:.3f}", series="ours shortfall vs tolerance; exact print size COLW_IN x 1.25 in, 6 to 6.5 pt type", headline=f"shortfall crosses the tolerance at pull {cross:,}; tau {tau:.4f}", files=[dict(file="fig_monitor_path.pdf", width=round(W, 4), height=H, legend="own legend inside")]), exact=True)


# ----------------------------------------------------------------------------- 13. continuum
def fig_continuum(out):
    # Single-column figure in Section 4: three panels printed at one third of a column each, so the panel files
    # are drawn at that width (fonts stay at 7.5 to 8 pt). One colour per task dimension (validated triple) with the
    # line style as a second encoding; no in-panel labels or legends, one two-row legend strip under the panels.
    t = pd.read_csv(f"{D}/A3/threshold_summary.csv"); INST = {1: "C", 2: "E", 3: "D"}; LS = {1: "-", 2: (0, (4, 2)), 3: (0, (1, 1.5))}
    DCOL = {1: C("ours_cont"), 2: "#1A5FB4", 3: "#2E8B57"}
    PW, PH, LWc, MSc = 1.08, 1.0, 1.2, 2.8     # short, wide panels; type at 6 to 6.5 pt so the plot area stays wide at one third of a column
    def small(ax):
        ax.tick_params(labelsize=6, pad=1.2, length=2); ax.xaxis.label.set_size(6.5); ax.yaxis.label.set_size(6.5); ax.xaxis.labelpad = 1.2; ax.yaxis.labelpad = 1.2
    S = {d: t[(t.d == d) & (t.inst == INST[d])].sort_values("logn") for d in (1, 2, 3)}
    turn = {d: (S[d][S[d].positive_price_share > 0].logn.min(), S[d][S[d].positive_price_share >= 0.999].logn.min()) for d in (1, 2, 3)}
    s1 = t[(t.d == 1) & (t.inst == "C")].groupby("logn")[["positive_price_share", "conviction_share_crash", "false_switches_proposed"]].mean().reset_index()
    DET = dict(color=INK, ls="-", lw=0.9, marker="s", ms=3.6, mfc=SURFACE, mec=INK, mew=0.9)   # zero delivery detected: hollow black squares

    def pa(a, own):
        for d in (1, 2, 3):
            s = S[d]; series(a, s.logn, s.positive_price_share, "ours_cont", label=f"d = {d}", ls=LS[d], color=DCOL[d], lw=LWc, ms=MSc, nmark=5)
            for _, r in s.iterrows(): rec("fig_continuum", "a", f"d={d}", r.logn, r.positive_price_share)
        a.set_xlabel("$\\log_{10} n$"); a.set_ylabel("share of cells"); pct(a); a.set_ylim(-0.04, 1.08); a.set_yticks([0, 0.5, 1.0]); a.set_xlim(5.5, 12.5); a.set_xticks([6, 8, 10, 12]); small(a); return False

    def pb(b, own):
        for d in (1, 2, 3):
            s = S[d]; series(b, s.logn, s.rev_per_round, "ours_cont", label=f"d = {d}", ls=LS[d], color=DCOL[d], lw=LWc, ms=MSc, nmark=5)
            b.plot(s.logn, s.bench_M2_per_round, color=REFS["second"][1], ls=REFS["second"][2], lw=0.9, zorder=1)
            for _, r in s.iterrows(): rec("fig_continuum", "b", f"d={d}", r.logn, r.rev_per_round, bench_second=r.bench_M2_per_round)
        b.set_xlabel("$\\log_{10} n$"); b.set_ylabel("revenue per round"); b.set_ylim(0, 1.0); b.set_yticks([0, 0.5, 1.0]); b.set_xlim(5.5, 12.5); b.set_xticks([6, 8, 10, 12]); small(b); return False

    def pc(c, own):
        series(c, s1.logn, s1.positive_price_share, "ours_cont", label="d = 1", ls=LS[1], color=DCOL[1], lw=LWc, ms=MSc, nmark=5)
        c.plot(s1.logn, s1.conviction_share_crash, markevery=max(1, len(s1) // 6), zorder=4, label="zero delivery detected", **DET)
        for _, r in s1.iterrows(): rec("fig_continuum", "c", "zero delivery detected", r.logn, r.conviction_share_crash, positive_price_share=r.positive_price_share, false_switches=r.false_switches_proposed)
        c.set_xlabel("$\\log_{10} n$"); c.set_ylabel("share of cells"); pct(c); c.set_ylim(-0.04, 1.08); c.set_yticks([0, 0.5, 1.0]); c.set_xticks([5, 6, 7, 8, 9]); small(c); return False

    H = {d: Line2D([], [], color=DCOL[d], ls=LS[d], lw=LWc, marker="D", ms=MSc, mec=SURFACE, mew=0.8) for d in (1, 2, 3)}
    # column-major fill of a 2 x 3 strip: row 1 = d = 1, 2, 3; row 2 = second capability, zero delivery detected
    shared = ([H[1], ref_handle("second"), H[2], Line2D([], [], **DET), H[3]], ["d = 1", "second capability", "d = 2", "zero delivery detected", "d = 3"])
    multi(out, "fig_continuum", [("a", pa, "shared"), ("b", pb, "shared"), ("c", pc, "shared")], [PW, PW, PW], PH, shared=shared, wspace=0.38, shared_ncol=3,
          manifest=dict(panels="a, b, c", data="A3/threshold_summary.csv: d = 1 inst C (K = 2), d = 2 inst E (K = 2), d = 3 inst D (K = 3); (c) d = 1, instance C (K = 2): share of cells with a positive requirement (the d = 1 curve of (a)) and share of cells in which a provider that delivers nothing after winning is switched out; on instance E, whose capacities cross, the detection share plateaus at 50% from log10 n = 7.0, with zero false switches on both; predicted activation horizons (audit/round2/A3/THRESHOLD_REPORT.md) are no longer drawn",
                        series="CG-MESP at d = 1, 2, 3 (red / blue / green, solid / dashed / dotted, D markers), second-capability benchmark (black dotted), zero delivery detected (hollow black squares); one two-row legend strip, no in-panel labels; panel files drawn at 1.08 x 1.0 in with 6 to 6.5 pt type for a one-third-column layout",
                        headline=f"first positive price / all priced at log10 n: d=1 {turn[1][0]} / {turn[1][1]}, d=2 {turn[2][0]} / {turn[2][1]}, d=3 {turn[3][0]} / {turn[3][1]}; zero delivery detected in 0% of cells up to 6.4, {100*s1[s1.logn==6.6].conviction_share_crash.iloc[0]:.0f}% at 6.6, 100% from {s1[s1.conviction_share_crash>=0.999].logn.min()}; false switches under the proposed profile: {int(s1.false_switches_proposed.sum())}"))


# ----------------------------------------------------------------------------- 14. near tie
def fig_near_tie(out):
    g = pd.read_csv(f"{D}/A4/capability_gap_summary.csv"); p = g[(g.mech == "plmesp") & (g.delta > 0)].sort_values("delta")
    W, H, BOT, TOP, LEFT, RIGHT = COLW_IN, 1.42, 0.29, 0.17, 0.36, 0.08
    f = plt.figure(figsize=(W, H)); ax = exact_axes(f, W, H, LEFT, RIGHT, BOT, TOP); style(ax, grid=None)
    series(ax, p.delta, p.revenue_at_proposed, "ours", label="proposed profile", nmark=8, lw=1.3, ms=3.4)
    lo = p[p.equilibrium_revenue > 0.6].delta.max(); hi = p[p.equilibrium_revenue < 0.6].delta.min()
    for seg, lab in ((p[p.delta <= lo], "lowest-reward fixed point"), (p[p.delta >= hi], None)):      # the two branches are not joined across the transition
        ax.plot(seg.delta, seg.equilibrium_revenue, color=C("ours"), ls="--", lw=1.3, marker="o", ms=3.6, mfc=SURFACE, mec=C("ours"), mew=0.9, markevery=max(1, len(seg) // 5), label=lab, zorder=3)
    ax.axvspan(lo, hi, color=PALE, alpha=0.7, lw=0); ax.annotate("transition", (hi, 0.58), xytext=(4, 0), textcoords="offset points", fontsize=SMALL_ANN, color=INK2, va="center")
    for _, r in p.iterrows(): rec("fig_near_tie", "", "ours", r.delta, r.revenue_at_proposed, equilibrium_revenue=r.equilibrium_revenue)
    ax.set_xscale("log"); logticks(ax, [0.001, 0.01, 0.1], ["0.001", "0.01", "0.1"]); ax.set_ylim(0.3, 0.8); ax.set_yticks([0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    small_ticks(ax); ax.set_xlabel("top-two capability gap", fontsize=SMALL_LABEL, labelpad=1.5); ax.set_ylabel("revenue per round", fontsize=SMALL_LABEL, labelpad=1.5)
    f.legend(*ax.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=((LEFT + (W - LEFT - RIGHT) / 2) / W, 1.0), ncol=2, fontsize=SMALL_LABEL, frameon=False, handlelength=1.8, columnspacing=1.4)
    save(f, "fig_near_tie", out, dict(panels="1", data="A4/capability_gap_summary.csv, mech plmesp, delta > 0", series="ours at the proposed profile; the lowest-revenue member of the equilibrium family; exact print size COLW_IN x 1.42 in with a one-row legend above, 6 to 6.5 pt type", headline=f"equilibrium revenue {p[p.delta<=lo].equilibrium_revenue.iloc[-1]:.3f} up to gap {lo:.4f}, {p[p.delta>=hi].equilibrium_revenue.iloc[0]:.3f} from {hi:.4f}; proposed profile {p.revenue_at_proposed.iloc[0]:.3f} to {p.revenue_at_proposed.iloc[-1]:.3f}", files=[dict(file="fig_near_tie.pdf", width=round(W, 4), height=H, legend="one row above")]), exact=True)


# ----------------------------------------------------------------------------- 15. complementarity (appendix)
def fig_app_complementarity(out):
    d = pd.read_csv(f"{D}/A4/complementarity.csv"); d = d[d.scope == "ALL"]
    m = d.pivot(index="row_model", columns="col_model", values="row_wrong_col_right"); acc = d.groupby("row_model").row_accuracy.first(); order = list(acc.sort_values(ascending=False).index); m = m.loc[order, order]
    cmap = LinearSegmentedColormap.from_list("seq", ["#f2f6fb", "#c3d8f0", "#7fb0e0", "#3d84cd", "#1b4b86"])
    f, ax = plt.subplots(figsize=(SINGLE, 2.7)); im = ax.imshow(m.values * 100, cmap=cmap, vmin=0, vmax=float(m.values.max() * 100))
    ax.set_xticks(range(len(order))); ax.set_yticks(range(len(order))); ax.set_xticklabels(order, rotation=45, ha="right", color=INK2); ax.set_yticklabels(order, color=INK2)
    for i in range(len(order)):
        for j in range(len(order)):
            v = m.values[i, j] * 100
            if i != j: ax.annotate(f"{v:.0f}", (j, i), ha="center", va="center", fontsize=7, color="white" if v > 0.55 * m.values.max() * 100 else INK)
            rec("fig_app_complementarity", "", order[i], order[j], m.values[i, j])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(length=0); cb = f.colorbar(im, ax=ax, fraction=0.045, pad=0.03); cb.set_label("% of queries: row wrong, column right", fontsize=7.5, color=INK2); cb.ax.tick_params(labelsize=7.5, colors=INK2, length=2); cb.outline.set_visible(False)
    save(f, "fig_app_complementarity", out, dict(panels="1", data="A4/complementarity.csv scope ALL (RouterBench 5-shot, 34,764 queries)", series="11 x 11 matrix ordered by overall accuracy", headline=f"max cell {m.values.max():.1%}", files=[dict(file="fig_app_complementarity.pdf", width=SINGLE, height=2.7, legend="colour bar")]))


# ----------------------------------------------------------------------------- 16. J2 + J4 (appendix)
def fig_app_dynamics_extra(out):
    d20 = f"{JDIR}/n20k_r2"; inst = json.load(open(f"{d20}/instance.json")); dev = inst["deviator"]; n = inst["n"]; t = np.arange(1, n + 1); st = 20
    G20 = {key: _gains(d20, mech, refp, "shadeall0.05", dev)[0] for mech, refp, key in JSER}
    ph = pd.read_csv(f"{JDIR}/cao_phases.csv"); g = ph.groupby("n")[["explore", "exploit", "blind", "undelegated", "monitor_slack"]].mean().reset_index(); fr = g[["explore", "exploit", "blind"]].to_numpy() / g["n"].to_numpy()[:, None]
    labels = ["exploration (unpriced)", "exploitation (priced)", "blind trust (unpriced)"]; cols = [MUTED, C("cao"), PALE]

    def pa(a, own):
        for mech, refp, key in JSER:
            m = G20[key].mean(0) / t; series(a, t[::st], m[::st], key, nmark=6); rec("fig_app_dynamics_extra", "a", key, n, m[-1])
        a.axhline(0, color=PALE, lw=0.8); a.set_xlabel("round $t$ ($n$ = 20,000)"); kfmt(a); a.set_ylabel("deviator's gain per round"); a.set_ylim(-0.25, 0.08); a.legend(loc="lower left"); return True

    def pb(b, own):
        style(b, "x"); y = np.arange(len(g)); left = np.zeros(len(g))
        for k in range(3):
            b.barh(y, fr[:, k], left=left, height=0.55, color=cols[k], label=labels[k], edgecolor=SURFACE, linewidth=1.5)
            for i in range(len(g)):
                if fr[i, k] >= 0.09: b.text(left[i] + fr[i, k] / 2, y[i], f"{fr[i, k]:.0%}", ha="center", va="center", fontsize=7, color="white" if k == 1 else INK)
                rec("fig_app_dynamics_extra", "b", labels[k], int(g.n[i]), fr[i, k], monitor_slack=g.monitor_slack[i])
            left += fr[:, k]
        b.set_yticks(y); b.set_yticklabels([f"n = {int(v):,}" for v in g.n]); b.invert_yaxis(); b.set_xlim(0, 1); pct(b, "x"); b.set_xlabel("share of the horizon"); legend_below(b, ncol=2, y=-0.36); return True

    multi(out, "fig_app_dynamics_extra", [("a", pa, "own"), ("b", pb, "own")], [3.2, 3.65], 1.9, wspace=0.3,
          manifest=dict(panels="a, b", data=f"J traces {d20}; {JDIR}/cao_phases.csv (3 seeds)", series="(a) ours, cao, eps, ucb; (b) Cao phases", headline=f"Cao priced share 0 at 20K and 50K, {fr[2,1]:.0%} at 100K, {fr[3,1]:.0%} at 300K, {fr[4,1]:.0%} at 1M"))


# ----------------------------------------------------------------------------- 17. graded + noisy labels (appendix)
ARMS5 = [("plmesp:plmesp_star", "ours", L("ours")), ("mesp_scalar:mesp_star", "pooled", L("pooled")), ("router_ucb:average", "ucb", "UCB router, compliant"), ("router_ucb:exploit_slow", "ucb", "UCB router, shading"), ("second_best:cao_eqmu", "cao", L("cao"))]


def arms5_handles():
    return [handle(k, ls="--" if "shading" in n else None) for _, k, n in ARMS5], [n for _, _, n in ARMS5]


def fig_app_graded_noisy(out):
    c9 = pd.read_csv(f"{D}/A5/c9_graded.csv"); c5 = pd.read_csv(f"{D}/A5/c5_noisy_labels.csv"); lv = sorted(c5.variant.unique())

    def pa(a, own):
        style(a, "x"); y = np.arange(len(ARMS5)); h = 0.36
        for j, (var, lab, al) in enumerate((("emp", "empirical-variance score", 1.0), ("k10", "ten-level score", 0.5))):
            for i, (arm, key, name) in enumerate(ARMS5):
                s_ = c9[(c9.variant == var) & (c9.arm == arm)]; v = s_.revenue_per_round.mean(); cc = s_.compliant_conviction_rate.mean(); un = s_.unserved_fraction.mean()
                a.barh(i + (j - 0.5) * (h + 0.02), v, h, color=C(key), alpha=al, zorder=3)
                if j == 0:
                    txt = f"{v:.3f}" + (f"\n{cc:.0%} false switch" if arm in ("plmesp:plmesp_star", "mesp_scalar:mesp_star") else "") + (f"\n{un:.0%} unserved" if un > 0 else "")
                    a.annotate(txt, (c9[c9.arm == arm].revenue_per_round.max(), i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2, linespacing=1.0)
                rec("fig_app_graded_noisy", "a", name, var, v, compliant_conviction=cc, unserved=un)
        a.set_yticks(y); a.set_yticklabels(["MESP (ours)", "single-price MESP", "UCB, compliant", "UCB, shading", "Cao et al."]); a.invert_yaxis(); a.set_xlim(0, 1.25); a.set_xlabel("revenue per round"); return False

    def pb(b, own):
        for arm, key, name in ARMS5:
            v = [c5[(c5.variant == l_) & (c5.arm == arm)].revenue_per_round.mean() for l_ in lv]; series(b, lv, v, key, label=name, ls="--" if "shading" in name else None)
            for l_, val in zip(lv, v): rec("fig_app_graded_noisy", "b", name, l_, val)
        b.set_xlabel("task labels misclassified"); pct(b, "x"); b.set_ylabel("revenue per round"); b.set_ylim(0.45, 0.75); b.set_xticks(lv); return False

    def pc(c, own):
        for arm, key, name in ARMS5[:2]:
            cc = [c5[(c5.variant == l_) & (c5.arm == arm)].compliant_conviction_rate.mean() for l_ in lv]; series(c, lv, cc, key, label=name)
            for l_, val in zip(lv, cc): rec("fig_app_graded_noisy", "c", name, l_, val)
        c.set_xlabel("task labels misclassified"); pct(c, "x"); c.set_ylabel("false switches"); pct(c); c.set_ylim(-0.03, 1.03); c.set_xticks(lv); return False

    o5 = c5[(c5.arm == "plmesp:plmesp_star")].groupby("variant").compliant_conviction_rate.mean()
    hs, labs = arms5_handles(); hs += [Patch(color=MUTED), Patch(color=MUTED, alpha=0.5)]; labs += ["(a) dark bar: empirical-variance score", "(a) light bar: ten-level score"]
    multi(out, "fig_app_graded_noisy", [("a", pa, "shared"), ("b", pb, "shared"), ("c", pc, "shared")], [2.9, 2.1, 1.7], 1.9, shared=(hs, labs), wspace=0.4, bottom=0.42, shared_ncol=4,
          manifest=dict(panels="a, b, c", data="A5/c9_graded.csv (variants emp, k10; n = 3e6, 10 subsets, 20 seeds); A5/c5_noisy_labels.csv (label-noise levels 0, 0.05, 0.10, 0.20)", series="ours, pooled, ucb compliant, ucb shading (dashed), cao; one legend strip (two rows) that also names the two graded-score variants drawn as the dark and light bar of each pair in (a): empirical-variance scaled score (variant emp) and ten-level discretisation (variant k10)",
                        headline=f"(a) graded: ours {c9[(c9.variant=='emp')&(c9.arm=='plmesp:plmesp_star')].revenue_per_round.mean():.3f} with 0% false convictions, pooled {c9[(c9.variant=='emp')&(c9.arm=='mesp_scalar:mesp_star')].revenue_per_round.mean():.3f} with {c9[(c9.variant=='emp')&(c9.arm=='mesp_scalar:mesp_star')].compliant_conviction_rate.mean():.0%}; (b, c) ours false convictions {o5.get(0.0,0):.0%} / {o5.get(0.05,0):.0%} / {o5.get(0.1,0):.0%} / {o5.get(0.2,0):.0%} at noise 0 / 5 / 10 / 20%"))


# ----------------------------------------------------------------------------- 18. type scaling (appendix)
def fig_app_type_scaling(out):
    d = pd.read_csv(f"{D}/A5/c3_type_scaling.csv"); Qs = sorted(d.Q.unique())

    def pa(a, own):
        for arm, key, name in ARMS5:
            v = [d[(d.arm == arm) & (d.Q == q)].revenue_per_round.mean() for q in Qs]; series(a, Qs, v, key, label=name, ls="--" if "shading" in name else None)
            for q, val in zip(Qs, v): rec("fig_app_type_scaling", "a", name, q, val)
        sc = [d[d.Q == q].second_cap.mean() for q in Qs]; a.plot(Qs, sc, color=REFS["second"][1], ls=REFS["second"][2], lw=1.0, label=REFS["second"][0], zorder=1)
        a.set_xlabel("number of task types $Q$"); a.set_ylabel("revenue per round"); a.set_xticks(Qs); a.set_ylim(0.4, 0.8); return False

    def pb(b, own):
        for arm, key, name in ARMS5[:2]:
            cc = [d[(d.arm == arm) & (d.Q == q)].compliant_conviction_rate.mean() for q in Qs]; series(b, Qs, cc, key, label=name)
            for q, val in zip(Qs, cc): rec("fig_app_type_scaling", "b", name, q, val)
        b.set_xlabel("number of task types $Q$"); b.set_ylabel("false switches"); pct(b); b.set_ylim(-0.03, 1.03); b.set_xticks(Qs); return False

    hs, labs = arms5_handles(); o = d[d.arm == "plmesp:plmesp_star"].groupby("Q").revenue_per_round.mean()
    multi(out, "fig_app_type_scaling", [("a", pa, "shared"), ("b", pb, "shared")], [3.9, 2.95], 1.9, shared=(hs + [ref_handle("second")], labs + ["second capability"]), wspace=0.3,
          manifest=dict(panels="a, b", data="A5/c3_type_scaling.csv, Q in {7,13,23,33,48,63} on RouterBench fine partitions, 3 subsets, mean over both horizons (3e5, 3e6)", series="ours, pooled, ucb compliant, ucb shading, cao; second capability; one legend strip",
                        headline=f"ours {o.iloc[0]:.3f} at Q = 7 to {o.iloc[-1]:.3f} at Q = 63 with 0% false convictions; pooled convicts compliant providers in {d[(d.arm=='mesp_scalar:mesp_star')&(d.Q==7)].compliant_conviction_rate.mean():.0%} (Q = 7) to {d[(d.arm=='mesp_scalar:mesp_star')&(d.Q==63)].compliant_conviction_rate.mean():.0%} (Q = 63) of cells"))


# ----------------------------------------------------------------------------- 19. substitution (appendix)
def fig_app_substitution(out):
    d = pd.read_csv(f"{D}/A5/c3_substitution.csv"); beh = [("plmesp_star", "compliant"), ("cao_eqmu", "compliant"), ("switch_cheapest", "switches to the\ncheapest model"), ("learning_subst", "learns which model\nto substitute")]
    xs = {"compliant": 0, "switches to the\ncheapest model": 1, "learns which model\nto substitute": 2}
    f, ax = fs.panels(1, SINGLE, 1.9); d["mech"] = d.arm.str.split(":").str[0]; d["profile"] = d.arm.str.split(":").str[1]
    for mech, key in (("plmesp", "ours"), ("mesp_scalar", "pooled"), ("router_ucb", "ucb"), ("second_best", "cao")):
        pts = []
        for prof, lab in beh:
            s = d[(d.mech == mech) & (d.profile == prof)]
            if len(s): pts.append((xs[lab], s.revenue_per_round.mean(), s.unserved_fraction.mean(), lab))
        if not pts: continue
        pts.sort(); ax.plot([p[0] for p in pts], [p[1] for p in pts], color=C(key), marker=M(key), ms=6, mec=SURFACE, mew=0.8, lw=1.4, ls="-" if len(pts) > 1 else "none", label=L(key), zorder=3)
        for x_, y_, u_, lab in pts:
            rec("fig_app_substitution", "", key, lab.replace("\n", " "), y_, unserved=u_)
            if u_ > 0: ax.annotate(f"{u_:.0%}", (x_, y_), xytext=(7, -9), textcoords="offset points", fontsize=7, color=INK2)
    r = d.iloc[0]; ref(ax, r.second_cap, "second"); ref(ax, r.honest_bench, "honest"); ref(ax, r.oracle, "oracle")
    ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["compliant", "switches to\ncheapest model", "learns which\nto substitute"]); ax.set_ylabel("revenue per round"); ax.set_ylim(0, 0.7); ax.set_xlim(-0.45, 2.6)
    legend_below(ax, ncol=3, y=-0.42)
    o = d[d.arm == "plmesp:learning_subst"].revenue_per_round.mean(); u = d[d.arm == "router_ucb:learning_subst"].revenue_per_round.mean()
    save(f, "fig_app_substitution", out, dict(panels="1", data="A5/c3_substitution.csv, one 4-provider subset, n = 3e6, 10 seeds; a provider substitutes a cheaper model instead of shading effort", series="ours, pooled, ucb, cao; oracle, second capability, honest benchmark; the percentages beside the Cao et al. markers are the shares of rounds it leaves unserved (29%, 14%, 53%)",
                                             headline=f"learning substitution: ours {o:.3f} vs UCB {u:.3f} (UCB ahead); ours compliant {d[d.arm=='plmesp:plmesp_star'].revenue_per_round.mean():.3f}; Cao {d[d.arm=='second_best:learning_subst'].revenue_per_round.mean():.3f} with {d[d.arm=='second_best:learning_subst'].unserved_fraction.mean():.0%} unserved", files=[dict(file="fig_app_substitution.pdf", width=SINGLE, height=1.9, legend="own legend below")]))


# ----------------------------------------------------------------------------- 20. Cao per type (appendix)
def fig_app_cao_per_type(out):
    c7 = pd.read_csv(f"{D}/A5/c7_cao_per_type.csv"); c5 = pd.read_csv(f"{D}/A5/c5_noisy_labels.csv"); base = c5[c5.variant == 0.0]
    bars = [("per type, equilibrium profile", "cao", c7[(c7.n == 3000000) & (c7.arm == "cao_per_type:cao_eq0")].revenue_per_round.mean(), 0.5),
            ("per type, lenient profile", "cao", c7[(c7.n == 3000000) & (c7.arm == "cao_per_type:cao_eqmu")].revenue_per_round.mean(), 0.75),
            ("pooled, lenient profile", "cao", base[base.arm == "second_best:cao_eqmu"].revenue_per_round.mean(), 1.0),
            ("UCB router, compliant", "ucb", base[base.arm == "router_ucb:average"].revenue_per_round.mean(), 1.0),
            ("MESP (ours)", "ours", base[base.arm == "plmesp:plmesp_star"].revenue_per_round.mean(), 1.0)]
    f, ax = fs.panels(1, SINGLE, 1.7); style(ax, "x")
    for i, (lab, key, v, al) in enumerate(bars):
        ax.barh(i, v, 0.62, color=C(key), alpha=al, zorder=3); ax.annotate(f"{v:.3f}", (v, i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2); rec("fig_app_cao_per_type", "", key, lab, v)
    r = base.iloc[0]; ref(ax, r.second_cap, "second", axis="v"); ref(ax, r.honest_bench, "honest", axis="v")
    ax.set_yticks(range(len(bars))); ax.set_yticklabels([b[0] for b in bars]); ax.invert_yaxis(); ax.set_xlabel("revenue per round"); ax.set_xlim(0, 0.8); legend_below(ax, ncol=2, y=-0.42)
    save(f, "fig_app_cao_per_type", out, dict(panels="1", data="A5/c7_cao_per_type.csv (n = 3e6) beside A5/c5_noisy_labels.csv variant 0.00, same 10 subsets, n = 3e6", series="Cao per type (two price variants), Cao pooled, UCB compliant, ours; second capability, honest benchmark",
                                             headline=f"Cao per type {bars[0][2]:.3f} / {bars[1][2]:.3f}, Cao pooled {bars[2][2]:.3f}, UCB {bars[3][2]:.3f}, ours {bars[4][2]:.3f}; second capability {r.second_cap:.3f}", files=[dict(file="fig_app_cao_per_type.pdf", width=SINGLE, height=1.7, legend="own legend below")]))


# ----------------------------------------------------------------------------- 21. LLM extra (appendix)
def fig_app_llm_extra(out):
    B = pd.read_csv(f"{LLM}/aggregate/table_B_contrasts.csv"); subs = [s for s in SUBL if s in set(B.scope)]; contrasts = ["medium - low", "high - medium", "high - low"]
    req = pd.read_csv(f"{LLM}/requests/main_policies_seed0.csv"); gl = pd.read_csv(f"{LLM}/requests/main_policies_seed0_gateway_log_task_adaptive_seed0.csv"); gl["arrival"] = range(len(gl))
    g = req[req.policy == "task_adaptive"].merge(gl[["request_id", "arrival"]], left_on="task_id", right_on="request_id").sort_values("arrival").head(120)

    def pa(a, own):
        x = np.arange(len(subs)); w = 0.26
        for k, c_ in enumerate(contrasts):
            gg = B[B.contrast == c_].set_index("scope").loc[subs]
            a.bar(x + (k - 1) * w, gg.acc_diff, w - 0.03, color=BUD[k], label=c_.replace(" - ", " vs "), edgecolor=SURFACE, linewidth=1)
            a.errorbar(x + (k - 1) * w, gg.acc_diff, yerr=[gg.acc_diff - gg.diff_lo, gg.diff_hi - gg.acc_diff], fmt="none", ecolor=INK2, elinewidth=0.8, capsize=0)
            for s_, r in gg.iterrows(): rec("fig_app_llm_extra", "a", c_, s_, r.acc_diff, lo=r.diff_lo, hi=r.diff_hi)
        a.axhline(0, color=PALE, lw=0.8); a.set_xticks(x); a.set_xticklabels(["GSM8K\nshort", "GSM8K\nlong", "MATH\nlevel 1-2", "MATH\nlevel 3", "MATH\nlevel 4-5"]); a.set_ylabel("accuracy difference (95% CI)"); pct(a); a.legend(loc="upper left"); return True

    def pb(b1, b2):
        for ax in (b1, b2): style(ax)
        for bench, col, lab in (("gsm8k", "#0072B2", "GSM8K request"), ("math500", "#252525", "MATH-500 request")):
            h = g[g.benchmark == bench]; b1.scatter(h.arrival, h.budget, s=8, color=col, label=lab, zorder=3); b2.scatter(h.arrival, h.reasoning_tokens, s=8, color=col, zorder=3)
            for _, r in h.iterrows(): rec("fig_app_llm_extra", "b", bench, int(r.arrival), int(r.budget), reasoning_tokens=int(r.reasoning_tokens))
        for ax in (b1, b2): ax.set_yscale("log"); logticks(ax, [128, 512, 2048], ["128", "512", "2K"], axis="y"); ax.set_ylim(90, 2900)
        b1.set_ylabel("assigned budget"); b1.legend(loc="center right"); plt.setp(b1.get_xticklabels(), visible=False)
        b2.set_ylabel("reasoning tokens"); b2.set_xlabel("arrival order of requests")

    fs.RECORDING = True
    f = plt.figure(figsize=(DOUBLE, 2.3)); gs = f.add_gridspec(2, 2, width_ratios=[1.15, 1], hspace=0.12, wspace=0.26); a = f.add_subplot(gs[:, 0]); b1 = f.add_subplot(gs[0, 1]); b2 = f.add_subplot(gs[1, 1], sharex=b1)
    style(a); pa(a, True); letter(a, "(a)"); pb(b1, b2); letter(b1, "(b)")
    save(f, "fig_app_llm_extra", out, dict(panels="a, b", data="experiments/llm_effort/results/aggregate/table_B_contrasts.csv; results/requests/main_policies_seed0.csv + gateway log (arrival order)", series="(a) three contrasts per subgroup; (b) GSM8K and MATH-500 requests",
                                          headline=f"MATH level 4-5: medium vs low {B[(B.scope=='math_hard')&(B.contrast=='medium - low')].acc_diff.iloc[0]:+.3f}, high vs medium {B[(B.scope=='math_hard')&(B.contrast=='high - medium')].acc_diff.iloc[0]:+.3f}; GSM8K short high vs low {B[(B.scope=='gsm8k_short')&(B.contrast=='high - low')].acc_diff.iloc[0]:+.3f}"))
    fs.RECORDING = False
    f, ax = plt.subplots(figsize=(3.7, 2.3)); style(ax); pa(ax, True); save(f, "fig_app_llm_extra_a", out)
    f, (c1, c2) = plt.subplots(2, 1, figsize=(3.15, 2.3), sharex=True, gridspec_kw={"hspace": 0.12}); pb(c1, c2); save(f, "fig_app_llm_extra_b", out)
    fs.RECORDING = True
    fs.MANIFEST[-1]["files"] = [dict(file="fig_app_llm_extra_a.pdf", width=3.7, height=2.3, legend="own legend inside"), dict(file="fig_app_llm_extra_b.pdf", width=3.15, height=2.3, legend="own legend inside (two stacked rows)")]


# ----------------------------------------------------------------------------- contact sheet, manifest
def contact_sheet(out, names):
    import matplotlib.image as mpimg
    files = [os.path.join(out, "png", n + ".png") for n in names if os.path.exists(os.path.join(out, "png", n + ".png"))]
    ncol = 3; nrow = int(np.ceil(len(files) / ncol)); f, axs = plt.subplots(nrow, ncol, figsize=(15, 4.0 * nrow))
    for ax in axs.flat: ax.axis("off")
    for ax, p in zip(axs.flat, files):
        ax.imshow(mpimg.imread(p)); ax.set_title(os.path.basename(p)[:-4], fontsize=9, loc="left")
    f.tight_layout(); f.savefig(os.path.join(out, "contact_sheet.png"), dpi=90); plt.close(f)


def write_manifest(out, validator):
    lines = ["# Paper figures: manifest", "", "Produced by `audit/round2/A5/scripts/make_paper_figures.py` from committed data; style in `figstyle.py`.", "",
             "Style: one colour and marker per method everywhere. MESP (ours) #D55E00 circle; CG-MESP #D55E00 diamond; single-price MESP #E69F00 square dashed; Cao et al. #CC79A7 triangle; UCB router #0072B2 down-triangle; ε-greedy router #56B4E9 plus; greedy router #9ecae1 right-triangle; static router #7f7f7f x; one-pull exclusion #009E73 star; fixed-buffer monitor #8c564b hexagon; two-sample monitor #17becf pentagon. References: oracle black dash-dot, second capability black dotted, honest benchmark grey dashed. Type: axis labels 8 pt, ticks 7.5, legend 7, panel letters 8 bold, annotations 7. No titles inside figures. Vector PDF (fonttype 42) + 300 dpi PNG under png/, tight layout, 0.02 in border. Every plotted number is in values_paper.csv (recorded once, from the composite).", "",
             "Per-panel files: every multi-panel figure also exists as `fig_<name>_<letter>.pdf` (no panel letter inside; LaTeX adds it) at the widths listed below, which fill 7.0 in with 0.15 in gaps; `fig_<name>_legend.pdf` is a one-row legend strip for panels that share their series.", "",
             "Palette validator: " + validator, "", "The A4 frontier figure (a4_fig3) is not produced: its inputs undercut_summary.csv / undercut_comparison.csv are not in experiments/data/A4, so the known defect (routers above the oracle line) cannot be re-checked from committed data.", ""]
    for m in fs.MANIFEST:
        lines += [f"## {m['file']}", f"- panels: {m.get('panels','')}", f"- data: {m.get('data','')}", f"- series: {m.get('series','')}", f"- headline: {m.get('headline','')}"]
        for fl in m.get("files", []):
            lines.append(f"- file: `{fl['file']}`, width {fl['width']} in, height {fl['height']} in, legend: {fl['legend']}")
        lines.append("")
    open(os.path.join(out, "MANIFEST.md"), "w").write("\n".join(lines))


FIGS = [fig_premise, fig_two_worlds, fig_scaling, fig_arrivals, fig_defences, fig_legitimacy, fig_monitors, fig_dynamics, fig_llm, fig_certified, fig_ladder, fig_monitor_path, fig_continuum, fig_near_tie,
        fig_app_complementarity, fig_app_dynamics_extra, fig_app_graded_noisy, fig_app_type_scaling, fig_app_substitution, fig_app_cao_per_type, fig_app_llm_extra, fig_alternatives]

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=os.path.join(REPO, "figures/paper")); ap.add_argument("--only", default=None); ap.add_argument("--validator", default="not run")
    a = ap.parse_args(); os.makedirs(os.path.join(a.out, "png"), exist_ok=True)
    todo = [f for f in FIGS if a.only is None or f.__name__ in a.only.split(",")]
    for fn in todo:
        try: fn(a.out)
        except Exception as e:
            import traceback; traceback.print_exc(); print("FAILED", fn.__name__, type(e).__name__, e); fs.MANIFEST.append(dict(file=fn.__name__, panels="FAILED", data=str(e), series="", headline=""))
        fs.RECORDING = True
    pd.DataFrame(fs.VALUES).to_csv(os.path.join(a.out, "values_paper.csv" if a.only is None else "values_partial.csv"), index=False)
    if a.only is None:
        write_manifest(a.out, a.validator); contact_sheet(a.out, [f.__name__ for f in FIGS])
    print("values:", len(fs.VALUES), "rows; figures:", len(fs.MANIFEST))
