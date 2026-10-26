"""One visual contract for every experiment figure of the paper.

Every method carries ONE colour, ONE marker and ONE line style in every figure (the user's rule:
MESP is always red with a circle). Red is used for nothing but ours. Reference quantities (oracle,
second capability, honest benchmark) are lines without markers in black or grey.

Type sizes are in points and independent of figure size: axis labels 8, tick labels 7.5, legend 7,
panel letters 8 bold, bar values and annotations 7, never smaller. No titles inside figures: a
multi-panel figure carries bare letters "(a)", "(b)" and the caption says the rest. Single column
3.33 in, double column 7.0 in; heights are set per figure and kept small; layouts are tight
(tight_layout pad 0.15, saved with bbox_inches tight and a 0.02 in border). Legends are compact and
sit inside the axes where a corner is free, otherwise just below. Vector PDF (TrueType fonts) and a
300 dpi PNG preview; every plotted number is recorded.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import matplotlib.ticker as mtick  # noqa: E402

# key -> (label, colour, marker, linestyle)
METHODS = {
    "ours":        ("MESP (ours)",           "#D62728", "o", "-"),
    "ours_cont":   ("CG-MESP (ours)",        "#D62728", "D", "-"),
    "pooled":      ("single-price MESP",     "#E69F00", "s", "--"),
    "cao":         ("Cao et al.",            "#CC79A7", "^", "-"),
    "ucb":         ("UCB router",            "#0072B2", "v", "-"),
    "eps":         ("ε-greedy router",  "#56B4E9", "P", "-"),
    "greedy":      ("greedy router",         "#9ecae1", ">", "-"),
    "static":      ("static router",         "#7f7f7f", "X", "-"),
    "onepull":     ("one-pull exclusion",    "#009E73", "*", "-"),
    "fixedbuffer": ("fixed-buffer monitor",  "#8c564b", "h", "-"),
    "twosample":   ("two-sample monitor",    "#17becf", "p", "-"),
}
# reference quantities: (label, colour, linestyle)
REFS = {
    "oracle":   ("oracle",            "#1b1b1b", "-."),
    "second":   ("second capability", "#1b1b1b", ":"),
    "honest":   ("honest benchmark",  "#7f7f7f", "--"),
}
# CSV arm names -> method keys
ARM = {"plmesp": "ours", "mesp_scalar": "pooled", "second_best": "cao", "cao_per_type": "cao",
       "router_ucb": "ucb", "router_eps": "eps", "router_greedy": "greedy", "router_static": "static",
       "esmaeili": "onepull", "anytime": "ours", "fixedbuffer": "fixedbuffer", "twosample": "twosample"}

INK, INK2, MUTED, GRID, PALE, SURFACE = "#1b1b1b", "#4a4a4a", "#8a8a8a", "#e3e3e0", "#c9c9c6", "white"
SINGLE, DOUBLE = 3.33, 7.0
LW, MS = 1.8, 5.2
FS_LABEL, FS_TICK, FS_LEGEND, FS_LETTER, FS_ANN = 8, 7.5, 7, 8, 7

plt.rcParams.update({
    "font.size": FS_TICK, "axes.labelsize": FS_LABEL, "axes.titlesize": FS_LETTER, "legend.fontsize": FS_LEGEND,
    "xtick.labelsize": FS_TICK, "ytick.labelsize": FS_TICK, "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID, "axes.linewidth": 0.8,
    "pdf.fonttype": 42, "ps.fonttype": 42, "figure.dpi": 150, "savefig.dpi": 300,
    "legend.frameon": False, "legend.handlelength": 1.3, "legend.handletextpad": 0.4, "legend.columnspacing": 0.9,
    "legend.borderaxespad": 0.0, "legend.labelspacing": 0.25, "legend.borderpad": 0.2,
    "axes.labelpad": 2.0, "xtick.major.pad": 2.0, "ytick.major.pad": 2.0,
    "axes.unicode_minus": False, "mathtext.default": "regular",
})

VALUES = []
MANIFEST = []
RECORDING = True          # per-panel re-renders of the same data switch this off so values are recorded once


def rec(figure, panel, series, x, y, **extra):
    """Record one plotted number (once per figure, from the composite pass)."""
    if RECORDING:
        VALUES.append(dict(figure=figure, panel=panel, series=series, x=x, y=y, **extra))


def style(ax, grid="y"):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, length=2.5, width=0.8)
    if grid:
        ax.grid(axis=grid, color=GRID, lw=0.6)
        ax.set_axisbelow(True)
    ax.margins(x=0.03)
    ax.xaxis.set_major_locator(mtick.MaxNLocator(nbins=5, steps=[1, 2, 2.5, 5, 10]))
    ax.yaxis.set_major_locator(mtick.MaxNLocator(nbins=5, steps=[1, 2, 2.5, 5, 10]))


def panels(n=1, width=SINGLE, height=2.0, **kw):
    f, axs = plt.subplots(1, n, figsize=(width, height), **kw)
    for a in (np.atleast_1d(axs)):
        style(a)
    return f, axs


def letter(ax, s):
    """Bare panel letter only; the description belongs to the caption."""
    s = s.strip()
    tag = s[:s.index(")") + 1] if s.startswith("(") and ")" in s else s
    ax.set_title(tag, loc="left", fontsize=FS_LETTER, fontweight="bold", color=INK, pad=2)


def kfmt(ax, axis="x"):
    f = mtick.FuncFormatter(lambda v, _: (f"{v/1e6:g}M" if abs(v) >= 1e6 else f"{v/1000:g}K" if abs(v) >= 1000 else f"{v:g}"))
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(f)


def pct(ax, axis="y", decimals=0):
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(mtick.PercentFormatter(1.0, decimals=decimals))


def few_ticks(ax, axis="y", n=5):
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_locator(mtick.MaxNLocator(nbins=n, steps=[1, 2, 2.5, 5, 10]))


def logticks(ax, ticks, labels=None, axis="x"):
    a = ax.xaxis if axis == "x" else ax.yaxis
    a.set_major_locator(mtick.FixedLocator(ticks))
    a.set_major_formatter(mtick.FixedFormatter(labels or [f"{t:g}" for t in ticks]))
    a.set_minor_formatter(mtick.NullFormatter())


def series(ax, x, y, key, label=None, ls=None, color=None, marker=None, lw=LW, ms=MS, alpha=1.0, zorder=3, nmark=8, **kw):
    """Plot one method series in its fixed style; markers on every point when sparse."""
    lab, c, m, l = METHODS[key]
    x = np.asarray(x); y = np.asarray(y, float)
    dense = len(x) > 10
    me = max(1, len(x) // nmark) if dense else None
    ax.plot(x, y, color=color or c, marker=marker or m, linestyle=ls or l, lw=lw, ms=ms, mec=SURFACE, mew=0.8,
            markevery=me, label=lab if label is None else label, alpha=alpha, zorder=zorder, solid_capstyle="round", **kw)


def band(ax, x, lo, hi, key, alpha=0.15):
    ax.fill_between(x, lo, hi, color=METHODS[key][1], alpha=alpha, lw=0, zorder=2)


def ref(ax, value, key, label=True, axis="h", lw=1.0, zorder=1, **kw):
    lab, c, ls = REFS[key]
    f = ax.axhline if axis == "h" else ax.axvline
    f(value, color=c, ls=ls, lw=lw, label=lab if label else None, zorder=zorder, **kw)


def handle(key, ls=None, marker=True):
    lab, c, m, l = METHODS[key]
    return Line2D([], [], color=c, marker=m if marker else None, linestyle=ls or l, lw=LW, ms=MS, mec=SURFACE, mew=0.8, label=lab)


def ref_handle(key):
    lab, c, ls = REFS[key]
    return Line2D([], [], color=c, linestyle=ls, lw=1.0, label=lab)


def legend_below(ax_or_fig, handles=None, ncol=3, y=-0.3, fontsize=None, **kw):
    """Compact legend just under the axes (or under the figure) where it covers no data."""
    kw.setdefault("loc", "upper center")
    kw.setdefault("bbox_to_anchor", (0.5, y))
    return ax_or_fig.legend(handles=handles, ncol=ncol, fontsize=fontsize or FS_LEGEND, **kw)


def bar_label(ax, x, y, text, dy=2, fontsize=FS_ANN, ha="center", va="bottom", color=INK2):
    ax.annotate(text, (x, y), xytext=(0, dy), textcoords="offset points", ha=ha, va=va, fontsize=fontsize, color=color)


def legend_strip(handles, labels, name, out, ncol=None, fontsize=None):
    """A one-row legend with no axes, saved on its own for LaTeX subfigure layouts."""
    f = plt.figure(figsize=(DOUBLE, 0.35))
    f.legend(handles=handles, labels=labels, loc="center", ncol=ncol or len(handles), frameon=False, fontsize=fontsize or FS_LEGEND)
    os.makedirs(os.path.join(out, "png"), exist_ok=True)
    f.savefig(os.path.join(out, name + ".pdf"), bbox_inches="tight", pad_inches=0.02)
    f.savefig(os.path.join(out, "png", name + ".png"), dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(f); print("wrote", name)


GRID_MINOR = "#f1f1ef"


def _numeric_labels(axis):
    """True when an axis carries numeric tick labels (or none yet), False for category labels."""
    import re as _re
    labs = [t.get_text() for t in axis.get_ticklabels() if t.get_text()]
    if not labs:
        return True
    for l in labs:
        l2 = _re.sub(r"[\$\s,%KkM×\-\u2212+]", "", l).replace("\\log_{10}", "")
        try:
            float(l2)
        except ValueError:
            return False
    return True


def apply_grids(f):
    """Major and minor grids on every numeric axis of every panel: major hairline, minor lighter.
    Category axes (bar labels, model names) get no minor ticks; image panels (heatmaps) get no grid."""
    for ax in f.axes:
        if ax.images or not ax.get_visible() or ax.get_label() == "<colorbar>":
            continue
        ax.grid(True, which="major", axis="both", color=GRID, lw=0.6, zorder=0)
        for name, axis in (("x", ax.xaxis), ("y", ax.yaxis)):
            if getattr(axis, "is_category", False):        # rule names on this axis, possibly hidden: no grid lines
                axis.set_minor_locator(mtick.NullLocator()); ax.grid(False, which="both", axis=name)
            elif axis.get_scale() == "log":
                ax.grid(True, which="minor", axis=name, color=GRID_MINOR, lw=0.4, zorder=0)
            elif _numeric_labels(axis):
                axis.set_minor_locator(mtick.AutoMinorLocator(2))
                ax.grid(True, which="minor", axis=name, color=GRID_MINOR, lw=0.4, zorder=0)
            else:
                axis.set_minor_locator(mtick.NullLocator())
        ax.tick_params(which="minor", length=0)
        ax.set_axisbelow(True)


def save(f, name, out, manifest=None, tight=True, exact=False):
    """exact=True keeps the figure size and axes positions as set (no tight layout, no cropping), for panels
    that must print at a given width and line up with a neighbouring panel."""
    os.makedirs(os.path.join(out, "png"), exist_ok=True)
    apply_grids(f)
    if tight and not exact:
        try:
            f.tight_layout(pad=0.15, w_pad=0.6, h_pad=0.4)
        except Exception:
            pass
    kw = {} if exact else dict(bbox_inches="tight", pad_inches=0.02)
    f.savefig(os.path.join(out, name + ".pdf"), **kw)
    f.savefig(os.path.join(out, "png", name + ".png"), dpi=300, **kw)
    plt.close(f)
    if manifest is not None:
        manifest = dict(manifest); manifest.setdefault("file", name + ".pdf")
        MANIFEST.append(manifest)
    print("wrote", name)
