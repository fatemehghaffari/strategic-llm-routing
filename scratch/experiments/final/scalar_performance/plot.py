#!/usr/bin/env python3
import csv
from pathlib import Path
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
COLORS={"mespf":"#0072B2","ucb_capacity":"#56B4E9","ucb_intrinsic":"#B3B3B3","uniform_capacity":"#DDAA33","oracle_second_price":"#000000"}
LABELS={"mespf":"MESP-F","ucb_capacity":"Capacity UCB","ucb_intrinsic":"Intrinsic UCB","uniform_capacity":"Uniform capacity","oracle_second_price":"Oracle second price"}
MARKERS={"mespf":"o","ucb_capacity":"s","ucb_intrinsic":"^","uniform_capacity":"D","oracle_second_price":"X"}

def load():
    with (HERE/"summary.csv").open() as f:return list(csv.DictReader(f))

def plot_metric(rows,metric,ylabel,filename,instances=("unique_top","tied_top","near_gap","honest_top")):
    fig,axs=plt.subplots(2,2,figsize=(7.1,4.8),sharex=True); axs=axs.ravel()
    for ax,inst in zip(axs,instances):
      for method in COLORS:
        rr=sorted((r for r in rows if r["instance"]==inst and r["method"]==method),key=lambda r:int(r["horizon"]))
        x=[int(r["horizon"]) for r in rr]; y=[float(r[f"{metric}_mean"]) for r in rr]
        lo=[float(r[f"{metric}_lo"]) for r in rr]; hi=[float(r[f"{metric}_hi"]) for r in rr]
        ax.plot(x,y,color=COLORS[method],marker=MARKERS[method],label=LABELS[method],lw=1.7,ms=4)
        ax.fill_between(x,lo,hi,color=COLORS[method],alpha=.12)
      ax.set_xscale("log"); ax.set_xlabel("Horizon"); ax.set_ylabel(ylabel); ax.text(.04,.93,inst.replace("_"," "),transform=ax.transAxes,va="top",fontsize=9)
      ax.grid(alpha=.2)
    handles,labels=axs[0].get_legend_handles_labels(); fig.legend(handles,labels,loc="upper center",ncol=3,frameon=False,bbox_to_anchor=(.5,1.01))
    fig.tight_layout(rect=(0,0,1,.90)); fig.savefig(HERE/f"{filename}.pdf",bbox_inches="tight"); fig.savefig(HERE/f"{filename}.svg",bbox_inches="tight"); plt.close(fig)

def plot_diagnostics(rows):
    rr=[r for r in rows if r["method"]=="mespf"]; fig,axs=plt.subplots(1,3,figsize=(7.1,2.25))
    specs=[("bidding_rounds","Bidding rounds"),("fallback","Fallback probability"),("fallback_rounds","Fallback rounds")]
    for ax,(metric,label) in zip(axs,specs):
      for inst,color,marker in zip(("unique_top","tied_top","near_gap","honest_top"),("#0072B2","#D55E00","#009E73","#CC79A7"),("o","s","^","D")):
        z=sorted((r for r in rr if r["instance"]==inst),key=lambda r:int(r["horizon"])); x=[int(r["horizon"]) for r in z]
        ax.plot(x,[float(r[f"{metric}_mean"]) for r in z],color=color,marker=marker,label=inst.replace("_"," "),lw=1.7,ms=4)
      ax.set_xscale("log"); ax.set_xlabel("Horizon"); ax.set_ylabel(label); ax.grid(alpha=.2)
    handles,labels=axs[0].get_legend_handles_labels(); fig.legend(handles,labels,loc="upper center",ncol=4,frameon=False,bbox_to_anchor=(.5,1.03))
    fig.tight_layout(rect=(0,0,1,.84)); fig.savefig(HERE/"mespf_diagnostics.pdf",bbox_inches="tight"); fig.savefig(HERE/"mespf_diagnostics.svg",bbox_inches="tight"); plt.close(fig)

if __name__=="__main__":
    r=load(); plot_metric(r,"reward_per_round","Reward per round","reward_per_round"); plot_metric(r,"capacity_shortfall_per_round","Capacity shortfall per round","capacity_shortfall"); plot_metric(r,"effort_per_round","Effort per round","effort_per_round"); plot_diagnostics(r)
