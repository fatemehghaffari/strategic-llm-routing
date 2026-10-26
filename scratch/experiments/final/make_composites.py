#!/usr/bin/env python3
"""Create the two compact, title-free figures recommended for the main paper."""
import csv
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator

ROOT = Path(__file__).resolve().parent
SI = ROOT / "scalar_incentives"
SP = ROOT / "scalar_performance"
CP = ROOT / "contextual_performance"
CI = ROOT / "contextual_incentives"

COLORS = {
    "mespf": "#0072B2", "ucb_capacity": "#56B4E9",
    "ucb_intrinsic": "#B3B3B3", "uniform_capacity": "#DDAA33",
    "oracle_second_price": "#000000", "Grid-UCB": "#E69F00",
    "Grid-ETC": "#009E73", "LinUCB": "#CC79A7", "Global UCB": "#777777",
}
LABELS = {
    "mespf": "MESP-F", "ucb_capacity": "Capacity UCB",
    "ucb_intrinsic": "Intrinsic UCB", "uniform_capacity": "Uniform",
    "oracle_second_price": "Oracle second price", "Global UCB": "Context-blind UCB",
}
MARKERS = ["o", "s", "^", "D", "P", "X", "v"]
LINES = ["-", "--", "-.", ":", (0, (5, 2)), (0, (3, 1, 1, 1)), (0, (1, 1))]

def read(path):
    with path.open() as f: return list(csv.DictReader(f))

def save(fig, name):
    fig.tight_layout()
    fig.savefig(ROOT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(ROOT / f"{name}.svg", bbox_inches="tight")
    fig.savefig(ROOT / f"{name}.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

def incentive_composite():
    scalar, contextual = read(SI / "paired_summary.csv"), read(CI / "summary.csv")
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 2.55))
    chosen = ["underbid_05", "underbid_15", "primary_shade_05", "bait_switch", "trigger_fallback_shade"]
    for j, dev in enumerate(chosen):
        rr = sorted((r for r in scalar if r["instance"] == "unique_top" and r["behavior"] == dev and r["metric"] == "focal_utility"), key=lambda r:int(r["n"]))
        x=[int(r["n"]) for r in rr]; y=[float(r["mean"])/int(r["n"]) for r in rr]
        lo=[float(r["ci_low"])/int(r["n"]) for r in rr]; hi=[float(r["ci_high"])/int(r["n"]) for r in rr]
        axs[0].plot(x,y,color=COLORS["mespf"],marker=MARKERS[j],linestyle=LINES[j],lw=1.45,ms=4,label=dev.replace("_"," "))
        axs[0].fill_between(x,lo,hi,color=COLORS["mespf"],alpha=.07)
    for j, dev in enumerate(["constant","cell-aligned","grid-misaligned","near-boundary","random-fixed"]):
        rr=sorted((r for r in contextual if r["deviation"]==dev),key=lambda r:int(r["n"]))
        x=[int(r["n"]) for r in rr]; y=[float(r["gain_per_round_mean"]) for r in rr]
        lo=[float(r["gain_per_round_lo"]) for r in rr]; hi=[float(r["gain_per_round_hi"]) for r in rr]
        axs[1].plot(x,y,color=COLORS["Grid-ETC"],marker=MARKERS[j],linestyle=LINES[j],lw=1.45,ms=4,label=dev)
        axs[1].fill_between(x,lo,hi,color=COLORS["Grid-ETC"],alpha=.07)
    for ax,panel,ticks,labels in zip(axs,["(a)", "(b)"],
                                    [[2000,8000,20000],[2000,8000,32000]],
                                    [["2k","8k","20k"],["2k","8k","32k"]]):
        ax.axhline(0,color="#444444",lw=.7); ax.set_xscale("log"); ax.set_xlabel("Horizon $n$"); ax.set_ylabel("Paired utility gain / $n$"); ax.grid(alpha=.18); ax.text(-.08,1.03,panel,transform=ax.transAxes,va="bottom",fontsize=8.5)
        ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_major_formatter(FixedFormatter(labels)); ax.xaxis.set_minor_locator(NullLocator())
        ax.legend(frameon=False,fontsize=6.1,loc="lower center",bbox_to_anchor=(.5,1.02),ncol=2)
    save(fig,"main_incentives")

def performance_composite():
    scalar, contextual = read(SP / "summary.csv"), read(CP / "summary.csv")
    fig, axs = plt.subplots(1, 4, figsize=(7.1, 2.15))
    methods_s=["mespf","ucb_capacity","ucb_intrinsic","uniform_capacity","oracle_second_price"]
    for ax,inst,panel in zip(axs[:2],["unique_top","honest_top"],["(a)","(b)"]):
        for j,m in enumerate(methods_s):
            rr=sorted((r for r in scalar if r["instance"]==inst and r["method"]==m),key=lambda r:int(r["horizon"]))
            x=[int(r["horizon"]) for r in rr]; y=[float(r["reward_per_round_mean"]) for r in rr]
            lo=[float(r["reward_per_round_lo"]) for r in rr]; hi=[float(r["reward_per_round_hi"]) for r in rr]
            ax.plot(x,y,color=COLORS[m],marker=MARKERS[j],linestyle=LINES[j],lw=1.35,ms=3.8,label=LABELS[m]); ax.fill_between(x,lo,hi,color=COLORS[m],alpha=.08)
        ax.set_ylabel("Reward / round" if panel == "(a)" else "", fontsize=7)
        if panel == "(b)": ax.tick_params(labelleft=False)
        ax.text(.02,.98,panel,transform=ax.transAxes,va="top",fontsize=8.5,fontweight="bold")
    methods_c=["Grid-UCB","Grid-ETC","LinUCB","Global UCB"]
    for ax,fam,panel in zip(axs[2:],["linear","checkerboard"],["(c)","(d)"]):
        for j,m in enumerate(methods_c):
            rr=sorted((r for r in contextual if r["family"]==fam and r["D"]=="2" and r["grid_multiplier"]=="1.0" and r["method"]==m),key=lambda r:int(r["n"]))
            x=[int(r["n"]) for r in rr]; y=[float(r["oracle_regret_mean"])/int(r["n"]) for r in rr]
            lo=[float(r["oracle_regret_lo"])/int(r["n"]) for r in rr]; hi=[float(r["oracle_regret_hi"])/int(r["n"]) for r in rr]
            ax.plot(x,y,color=COLORS[m],marker=MARKERS[j],linestyle=LINES[j],lw=1.35,ms=3.8,label=LABELS.get(m,m)); ax.fill_between(x,lo,hi,color=COLORS[m],alpha=.08)
        ax.set_ylabel("Regret / $n$" if panel == "(c)" else "", fontsize=7)
        if panel == "(d)": ax.tick_params(labelleft=False)
        ax.text(.02,.98,panel,transform=ax.transAxes,va="top",fontsize=8.5,fontweight="bold")
    for idx,ax in enumerate(axs):
        ax.set_xscale("log"); ax.grid(alpha=.18)
        ax.tick_params(axis="both",labelsize=6.5,pad=1.5)
        ticks=[2000,8000,20000] if idx < 2 else [2000,8000]
        labels=["2k","8k","20k"] if idx < 2 else ["2k","8k"]
        ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_major_formatter(FixedFormatter(labels)); ax.xaxis.set_minor_locator(NullLocator())
    h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc="upper center",ncol=5,frameon=False,fontsize=6.1,bbox_to_anchor=(.5,1.015))
    h,l=axs[2].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=4,frameon=False,fontsize=6.1,bbox_to_anchor=(.5,-.01))
    fig.subplots_adjust(top=.79,bottom=.25,wspace=.38)
    fig.savefig(ROOT/"main_performance.pdf",bbox_inches="tight"); fig.savefig(ROOT/"main_performance.svg",bbox_inches="tight"); fig.savefig(ROOT/"main_performance.png",dpi=180,bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    incentive_composite(); performance_composite()
