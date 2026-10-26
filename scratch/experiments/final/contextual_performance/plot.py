#!/usr/bin/env python3
"""Publication plots and paired comparisons for contextual performance."""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
COLORS = {"Grid-UCB":"#E69F00", "Grid-ETC":"#009E73", "LinUCB":"#CC79A7",
          "Global UCB":"#777777", "Finite-context UCB":"#56B4E9"}
MARKERS = {"Grid-UCB":"o", "Grid-ETC":"s", "LinUCB":"D", "Global UCB":"^",
           "Finite-context UCB":"P"}
METHODS = list(COLORS)

def read(name):
    with (HERE/name).open() as f: return list(csv.DictReader(f))

def save(fig, stem):
    fig.savefig(HERE/(stem+".pdf"), bbox_inches="tight")
    fig.savefig(HERE/(stem+".svg"), bbox_inches="tight")
    plt.close(fig)

def line(ax, rows, family, D, metric, ylabel):
    for method in METHODS:
        rs=[r for r in rows if r["family"]==family and int(r["D"])==D and r["method"]==method and float(r["grid_multiplier"])==1]
        if not rs: continue
        rs.sort(key=lambda r:int(r["n"])); x=np.array([int(r["n"]) for r in rs])
        y=np.array([float(r[metric+"_mean"])/int(r["n"]) if metric in {"oracle_regret","effort"} else float(r[metric+"_mean"]) for r in rs])
        lo=np.array([float(r[metric+"_lo"])/int(r["n"]) if metric in {"oracle_regret","effort"} else float(r[metric+"_lo"]) for r in rs])
        hi=np.array([float(r[metric+"_hi"])/int(r["n"]) if metric in {"oracle_regret","effort"} else float(r[metric+"_hi"]) for r in rs])
        ax.plot(x,y,color=COLORS[method],marker=MARKERS[method],label=method,linewidth=1.8)
        ax.fill_between(x,lo,hi,color=COLORS[method],alpha=.14,linewidth=0)
    ax.set_xscale("log"); ax.set_xlabel("Horizon"); ax.set_ylabel(ylabel); ax.grid(alpha=.25)

def main():
    rows=read("summary.csv")
    plt.rcParams.update({"font.size":8.5,"axes.spines.top":False,"axes.spines.right":False,"pdf.fonttype":42})
    # Two dimensions by three environment families.
    fig,axs=plt.subplots(2,3,figsize=(7.05,4.25),sharex=True,sharey=True)
    for col,fam in enumerate(["linear","smooth","checkerboard"]):
        for row,D in enumerate([2,6]):
            line(axs[row,col],rows,fam,D,"oracle_regret","Oracle regret / round")
            axs[row,col].text(.04,.94,f"{fam.capitalize()}, $D={D}$",transform=axs[row,col].transAxes,va="top")
    h,l=axs[0,0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=4,frameon=False)
    fig.subplots_adjust(bottom=.16,wspace=.18,hspace=.25); save(fig,"oracle_regret")

    fig,axs=plt.subplots(1,2,figsize=(7.05,2.55))
    for ax,D in zip(axs,[2,6]):
        line(ax,rows,"smooth",D,"allocation_accuracy","Optimal-allocation frequency")
        ax.text(.04,.94,f"Smooth, $D={D}$",transform=ax.transAxes,va="top")
    h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=4,frameon=False)
    fig.subplots_adjust(bottom=.26,wspace=.25); save(fig,"allocation_accuracy")

    # Exact finite context comparison.
    fig,ax=plt.subplots(figsize=(3.45,2.45)); line(ax,rows,"finite",2,"oracle_regret","Oracle regret / round")
    ax.legend(frameon=False,fontsize=7); save(fig,"finite_context")

    # Runtime/state count at the largest core horizon. Runtime is deliberately separate from statistical plots.
    chosen=[r for r in rows if r["family"]=="smooth" and int(r["D"])==6 and int(r["n"])==8000 and float(r["grid_multiplier"])==1]
    chosen.sort(key=lambda r:METHODS.index(r["method"]) if r["method"] in METHODS else 99)
    fig,axs=plt.subplots(1,2,figsize=(7.05,2.4)); names=[r["method"] for r in chosen]; xx=np.arange(len(names))
    for ax,metric,label in [(axs[0],"runtime_s","Runtime per trial (s)"),(axs[1],"parameter_count","Stored scalars")]:
        vals=[float(r[metric+"_mean"]) for r in chosen]
        ax.bar(xx,vals,color=[COLORS[n] for n in names]); ax.set_xticks(xx,names,rotation=25,ha="right"); ax.set_ylabel(label); ax.grid(axis="y",alpha=.25)
    fig.subplots_adjust(bottom=.3,wspace=.3); save(fig,"runtime_memory")

    # Grid multiplier sensitivity uses the same method colors and method-specific line styles.
    fig,ax=plt.subplots(figsize=(3.45,2.45))
    filt=[r for r in rows if r["family"]=="smooth" and int(r["D"])==2 and int(r["n"])==8000 and r["method"] in {"Grid-UCB","Grid-ETC"}]
    for method in ["Grid-UCB","Grid-ETC"]:
        rs=sorted([r for r in filt if r["method"]==method],key=lambda r:float(r["grid_multiplier"]))
        ax.plot([float(r["grid_multiplier"]) for r in rs],[float(r["oracle_regret_mean"])/8000 for r in rs],color=COLORS[method],marker=MARKERS[method],label=method)
    ax.set_xlabel("Grid-width multiplier"); ax.set_ylabel("Oracle regret / round"); ax.grid(alpha=.25); ax.legend(frameon=False)
    save(fig,"grid_sensitivity")

    # Paired bootstrap differences in oracle regret relative to LinUCB.
    raw=read("trials.csv"); groups={}
    for r in raw:
        if float(r["grid_multiplier"])!=1 or r["family"]=="finite": continue
        key=(r["family"],r["D"],r["n"],r["trial"]); groups.setdefault(key,{})[r["method"]]=float(r["oracle_regret"])
    rng=np.random.default_rng(7721); out=[]
    for fam in ["linear","smooth","checkerboard"]:
      for D in ["2","6"]:
       for n in ["2000","8000"]:
        cells=[v for (f,d,nn,_),v in groups.items() if (f,d,nn)==(fam,D,n)]
        for method in ["Grid-UCB","Grid-ETC","Global UCB"]:
            diff=np.array([v[method]-v["LinUCB"] for v in cells]); ix=rng.integers(0,len(diff),(5000,len(diff))); bm=diff[ix].mean(1)
            out.append(dict(family=fam,D=D,n=n,method=method,reps=len(diff),mean_difference=diff.mean(),ci95_lo=np.quantile(bm,.025),ci95_hi=np.quantile(bm,.975)))
    with (HERE/"paired_comparisons.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=out[0]);w.writeheader();w.writerows(out)

if __name__=="__main__": main()
