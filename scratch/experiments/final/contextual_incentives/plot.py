#!/usr/bin/env python3
import csv
from pathlib import Path
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
COLORS={d:"#009E73" for d in ["constant","cell-aligned","grid-misaligned","near-boundary","random-fixed"]}
MARKERS={"constant":"o","cell-aligned":"s","grid-misaligned":"^","near-boundary":"D","random-fixed":"v"}
STYLES={"constant":"-","cell-aligned":"--","grid-misaligned":"-.","near-boundary":":","random-fixed":(0,(3,1,1,1))}

def main():
    rows=list(csv.DictReader((HERE/"summary.csv").open()))
    for metric,ylabel,name in [("utility_gain","Deviation utility gain","utility_gain"),("gain_per_round","Deviation utility gain per round","normalized_utility_gain")]:
        fig,ax=plt.subplots(figsize=(5.25,3.25))
        for dev in COLORS:
            rr=sorted((r for r in rows if r["deviation"]==dev),key=lambda r:int(r["n"])); x=[int(r["n"]) for r in rr]; y=[float(r[metric+"_mean"]) for r in rr]
            lo=[y[i]-float(r[metric+"_lo"]) for i,r in enumerate(rr)]; hi=[float(r[metric+"_hi"])-y[i] for i,r in enumerate(rr)]
            ax.errorbar(x,y,yerr=[lo,hi],label=dev,color=COLORS[dev],ls=STYLES[dev],marker=MARKERS[dev],lw=1.8,capsize=3)
        ax.axhline(0,color="#444444",lw=.9,ls="--"); ax.set_xscale("log"); ax.set_xlabel("Horizon $n$"); ax.set_ylabel(ylabel); ax.grid(alpha=.22); ax.legend(frameon=False,ncol=2,fontsize=8)
        fig.tight_layout(); fig.savefig(HERE/f"{name}.pdf"); fig.savefig(HERE/f"{name}.svg"); plt.close(fig)

if __name__=="__main__": main()
