#!/usr/bin/env python3
"""Publication plots: no embedded titles; captions belong in LaTeX."""
import csv
from pathlib import Path
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader((HERE / "paired_summary.csv").open()))
for r in rows:
    for x in ("n","reps","mean","ci_low","ci_high"): r[x] = float(r[x])

styles = {
 "underbid_05":("o","-"), "underbid_15":("s","--"),
 "primary_shade_05":("^","-."), "primary_shade_15":("v",":"),
 "bait_switch":("D","-"), "trigger_fallback_shade":("P","--"),
 "nontop_win_underperform":("X","-."),
}
colors = {
 "underbid_05":"#0072B2", "underbid_15":"#56B4E9",
 "primary_shade_05":"#D55E00", "primary_shade_15":"#E69F00",
 "bait_switch":"#009E73", "trigger_fallback_shade":"#CC79A7",
 "nontop_win_underperform":"#6F6F6F",
}
labels = {
 "underbid_05":"Underbid 0.05", "underbid_15":"Underbid 0.15",
 "primary_shade_05":"Primary shade 0.05", "primary_shade_15":"Primary shade 0.15",
 "bait_switch":"Bait-and-switch", "trigger_fallback_shade":"Fallback shade",
 "nontop_win_underperform":"Non-top underperformance",
}

def figure(instance, metric, outfile, normalize=False):
    fig, ax = plt.subplots(figsize=(6.25,3.55))
    subset = [r for r in rows if r["instance"]==instance and r["metric"]==metric]
    for behavior in styles:
        q = sorted([r for r in subset if r["behavior"]==behavior], key=lambda z:z["n"])
        if not q: continue
        scale = [r["n"] if normalize else 1 for r in q]
        y = [r["mean"]/s for r,s in zip(q,scale)]
        lo = [r["ci_low"]/s for r,s in zip(q,scale)]; hi=[r["ci_high"]/s for r,s in zip(q,scale)]
        marker, ls = styles[behavior]
        ax.plot([r["n"] for r in q], y, color=colors[behavior], marker=marker, linestyle=ls,
                linewidth=1.7, markersize=5, label=labels[behavior])
        ax.fill_between([r["n"] for r in q],lo,hi,color=colors[behavior],alpha=.10)
    ax.axhline(0,color="#555555",linewidth=.8)
    ax.set_xticks((2000,8000,20000), ("2k","8k","20k"))
    ax.set_xlabel("Horizon $n$")
    ax.set_ylabel("Paired utility gain / $n$" if normalize else "Paired difference")
    ax.grid(alpha=.22,linewidth=.5); ax.legend(frameon=False,ncol=2,fontsize=7.2)
    fig.tight_layout()
    for ext in ("pdf","svg"): fig.savefig(HERE/f"{outfile}.{ext}",bbox_inches="tight")
    plt.close(fig)

def unique_top_diagnostics():
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 2.75), sharex=True)
    specs = (("focal_utility", "Paired utility difference"),
             ("fallback_rounds", "Paired fallback-round difference"))
    for panel, (ax, (metric, ylabel)) in enumerate(zip(axs, specs)):
        subset = [r for r in rows if r["instance"]=="unique_top" and r["metric"]==metric]
        for behavior in styles:
            q = sorted([r for r in subset if r["behavior"]==behavior], key=lambda z:z["n"])
            if not q: continue
            x = [r["n"] for r in q]
            marker, ls = styles[behavior]
            ax.plot(x, [r["mean"] for r in q], color=colors[behavior], marker=marker,
                    linestyle=ls, linewidth=1.65, markersize=4.5, label=labels[behavior])
            ax.fill_between(x, [r["ci_low"] for r in q], [r["ci_high"] for r in q],
                            color=colors[behavior], alpha=.10)
        ax.axhline(0, color="#555555", linewidth=.8)
        ax.set_xticks((2000,8000,20000), ("2k","8k","20k"))
        ax.set_xlabel("Horizon $n$")
        ax.set_ylabel(ylabel)
        ax.grid(alpha=.22, linewidth=.5)
        ax.text(-.11,1.02,f"({chr(97+panel)})",transform=ax.transAxes,va="bottom",fontweight="bold")
    handles, legend_labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc="upper center", ncol=3, frameon=False,
               fontsize=7.2, bbox_to_anchor=(.5,1.01), columnspacing=1.5, handletextpad=.5)
    fig.tight_layout(rect=(0,0,1,.80), w_pad=2.2)
    for ext in ("pdf","svg"):
        fig.savefig(HERE/f"unique_top_diagnostics.{ext}", bbox_inches="tight")
    plt.close(fig)

for inst in ("unique_top","tied_top","near_gap","honest_top","low_gap_nontop"):
    figure(inst,"focal_utility",f"{inst}_utility_gain",True)
    figure(inst,"focal_utility",f"{inst}_utility_gain_absolute",False)
figure("unique_top","fallback_rounds","unique_top_fallback_rounds",False)
figure("low_gap_nontop","fallback_rounds","low_gap_nontop_fallback_rounds",False)
unique_top_diagnostics()
