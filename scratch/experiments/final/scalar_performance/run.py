#!/usr/bin/env python3
"""Final scalar performance experiment for MESP-F.

Every plotted cell uses paired seeds across methods. Raw trial rows are retained.
"""
from __future__ import annotations

import argparse, csv, math, time
from dataclasses import dataclass
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent

@dataclass(frozen=True)
class Instance:
    name: str
    mu: tuple[float, ...]
    cap: tuple[float, ...]
    honest: tuple[bool, ...]

# Every instance has an honest arm and satisfies 0 <= mu_i <= M_i <= 1.
INSTANCES = (
    Instance("unique_top", (.10,.20,.40), (.90,.65,.40), (False,False,True)),
    Instance("tied_top", (.10,.20,.45), (.80,.80,.45), (False,False,True)),
    Instance("near_gap", (.10,.20,.50), (.80,.76,.50), (False,False,True)),
    Instance("honest_top", (.75,.20,.15), (.75,.70,.45), (True,False,False)),
)
METHODS = ("mespf", "ucb_capacity", "ucb_intrinsic", "uniform_capacity", "oracle_second_price")

def design(n,k):
    ell=min(n//(2*k), math.ceil(n**(2/3)*math.log(math.e*n)**(1/3)))
    return ell,n-k*ell,math.sqrt(math.log(2*k*n**4)/(2*ell))

def exp3(rng,cap,mu,h):
    k=len(cap); pulls=np.zeros(k,int); effort=np.zeros(k); rew=0
    if h<=0:return pulls,effort,rew
    gamma=min(.5,math.sqrt(k*math.log(k)/h)); eta=gamma/k; logw=np.zeros(k)
    for _ in range(h):
        z=logw-logw.max(); q=np.exp(z); q/=q.sum(); p=(1-gamma)*q+gamma/k
        a=int(rng.choice(k,p=p)); m=cap[a]; y=float(rng.random()<m)
        pulls[a]+=1; effort[a]+=m-mu[a]; rew+=y; logw[a]+=eta*y/p[a]
    return pulls,effort,rew

def finish(inst,n,reward,pulls,effort,elapsed,**extra):
    cap=np.array(inst.cap); m2=float(np.partition(cap,-2)[-2])
    out={"reward":reward,"reward_per_round":reward/n,
         "capacity_shortfall":float(cap.max()*n-reward),
         "capacity_shortfall_per_round":float(cap.max()-reward/n),
         "second_price_shortfall":float(m2*n-reward),
         "second_price_shortfall_per_round":float(m2-reward/n),
         "total_effort":float(effort.sum()),"effort_per_round":float(effort.sum()/n),
         "runtime_seconds":elapsed, **extra}
    for i in range(len(cap)): out[f"pull_share_{i}"]=pulls[i]/n
    return out

def mespf(inst,n,seed):
    rng=np.random.default_rng(seed); t0=time.perf_counter(); mu=np.array(inst.mu); cap=np.array(inst.cap); k=len(cap)
    if n<2*k:
        pulls=np.zeros(k,int); effort=np.zeros(k); reward=0
        for t in range(n):
            a=t%k; m=cap[a]; pulls[a]+=1; effort[a]+=m-mu[a]; reward+=rng.random()<m
        return finish(inst,n,reward,pulls,effort,time.perf_counter()-t0,
                      bidding_rounds=n,primary_rounds=0,fallback=0,fallback_rounds=0,tau=np.nan)
    ell,N,s=design(n,k); priority=rng.permutation(k); rank=np.empty(k,int); rank[priority]=np.arange(k)
    successes=rng.binomial(ell,cap); bids=successes/ell
    order=sorted(range(k),key=lambda i:(-bids[i],rank[i])); w=order[0]; tau=max(0.,bids[order[1]]-s)
    pulls=np.full(k,ell,int); effort=ell*(cap-mu); reward=float(successes.sum()); z=0; q=0; switched=False
    for r in range(1,N+1):
        m=max(mu[w],min(tau,cap[w])) if inst.honest[w] else min(tau,cap[w])
        y=float(rng.random()<m); z+=y; q=r; pulls[w]+=1; effort[w]+=m-mu[w]; reward+=y
        if z < r*tau-math.sqrt(r*math.log(2*n**4)/2): switched=True; break
    h=N-q if switched else 0
    if h:
        fp,fe,fr=exp3(rng,cap,mu,h); pulls+=fp; effort+=fe; reward+=fr
    return finish(inst,n,reward,pulls,effort,time.perf_counter()-t0,
                  bidding_rounds=k*ell,primary_rounds=q,fallback=int(switched),fallback_rounds=h,tau=tau)

def baseline(inst,n,method,seed):
    rng=np.random.default_rng(seed); t0=time.perf_counter(); mu=np.array(inst.mu); cap=np.array(inst.cap); k=len(cap)
    pulls=np.zeros(k,int); effort=np.zeros(k); reward=0.
    if method=="oracle_second_price":
        a=int(np.argmax(cap)); m=max(mu[a],float(np.partition(cap,-2)[-2])) if inst.honest[a] else float(np.partition(cap,-2)[-2])
        reward=float(rng.binomial(n,m)); pulls[a]=n; effort[a]=n*(m-mu[a])
    elif method=="uniform_capacity":
        pulls[:]=n//k; pulls[:n%k]+=1
        reward=float(sum(rng.binomial(int(pulls[a]),cap[a]) for a in range(k))); effort=pulls*(cap-mu)
    else:
        target=cap if method=="ucb_capacity" else mu; sums=np.zeros(k)
        for t in range(n):
            a=t if t<k else int(np.argmax(sums/pulls+np.sqrt(2*math.log(t+1)/pulls)))
            y=float(rng.random()<target[a]); pulls[a]+=1; sums[a]+=y; effort[a]+=target[a]-mu[a]; reward+=y
    return finish(inst,n,reward,pulls,effort,time.perf_counter()-t0,
                  bidding_rounds=0,primary_rounds=0,fallback=0,fallback_rounds=0,tau=np.nan)

def write_csv(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def bootstrap(x,rng,b=4000):
    x=np.asarray(x,float); means=np.mean(x[rng.integers(0,len(x),(b,len(x)))],axis=1)
    return float(np.mean(x)),float(np.quantile(means,.025)),float(np.quantile(means,.975))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--reps",type=int,default=120); ap.add_argument("--seed",type=int,default=20260828)
    ap.add_argument("--horizons",type=int,nargs="+",default=[2000,8000,20000]); a=ap.parse_args(); HERE.mkdir(parents=True,exist_ok=True)
    rows=[]
    for ii,inst in enumerate(INSTANCES):
      for n in a.horizons:
       for rep in range(a.reps):
        seed=int(np.random.SeedSequence([a.seed,ii,n,rep]).generate_state(1,dtype=np.uint64)[0])
        for method in METHODS:
            result=mespf(inst,n,seed) if method=="mespf" else baseline(inst,n,method,seed)
            rows.append({"instance":inst.name,"horizon":n,"rep":rep,"seed":seed,"method":method,**result})
    write_csv(HERE/"trials.csv",rows)
    metrics=("reward_per_round","capacity_shortfall_per_round","second_price_shortfall_per_round","effort_per_round",
             "runtime_seconds","bidding_rounds","primary_rounds","fallback","fallback_rounds")
    summaries=[]; brng=np.random.default_rng(a.seed+1)
    for inst in INSTANCES:
      for n in a.horizons:
       for method in METHODS:
        cell=[r for r in rows if r["instance"]==inst.name and r["horizon"]==n and r["method"]==method]
        rec={"instance":inst.name,"horizon":n,"method":method,"reps":len(cell)}
        for metric in metrics:
            mean,lo,hi=bootstrap([r[metric] for r in cell],brng); rec[f"{metric}_mean"]=mean; rec[f"{metric}_lo"]=lo; rec[f"{metric}_hi"]=hi
        summaries.append(rec)
    write_csv(HERE/"summary.csv",summaries)
    # Paired bootstrap contrasts preserve the common-random-number pairing.
    contrasts=[]
    for inst in INSTANCES:
      for n in a.horizons:
       base={int(r["rep"]):r for r in rows if r["instance"]==inst.name and r["horizon"]==n and r["method"]=="mespf"}
       for method in METHODS[1:]:
        comp={int(r["rep"]):r for r in rows if r["instance"]==inst.name and r["horizon"]==n and r["method"]==method}
        rec={"instance":inst.name,"horizon":n,"contrast":f"mespf_minus_{method}","reps":len(base)}
        for metric in ("reward_per_round","capacity_shortfall_per_round","effort_per_round"):
            mean,lo,hi=bootstrap([float(base[j][metric])-float(comp[j][metric]) for j in sorted(base)],brng)
            rec[f"{metric}_mean"]=mean; rec[f"{metric}_lo"]=lo; rec[f"{metric}_hi"]=hi
        contrasts.append(rec)
    write_csv(HERE/"paired_comparisons.csv",contrasts)
    print(f"wrote {len(rows)} trial rows; {a.reps} paired reps per cell")

if __name__=="__main__": main()
