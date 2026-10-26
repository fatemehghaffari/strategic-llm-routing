#!/usr/bin/env python3
"""Theorem-aligned incentive experiments for Static Grid-ETC."""
from __future__ import annotations

import argparse, csv, math
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
DEVS = ["constant", "cell-aligned", "grid-misaligned", "near-boundary", "random-fixed"]


def means(x):
    """Continuous local capacities, D=Kd=3, with exact top set {0,1}."""
    cap = np.column_stack((np.full(len(x), .72),
                           np.full(len(x), .72),
                           .53 + .08*x[:, 2]))
    mu = .16 + .04*x
    return mu, cap


def targets(cap, x, dev, h, random_map):
    m = cap.copy(); z = x[:, 0]
    if dev == "constant": shade = np.full(len(x), .10)
    elif dev == "cell-aligned": shade = .14*((np.floor(z/h).astype(int) % 2) == 0)
    elif dev == "grid-misaligned": shade = .14*(z < .37)
    elif dev == "near-boundary": shade = .16*(np.abs(z-.5) <= .09)
    elif dev == "random-fixed":
        # Drawn ex ante and then fixed: measurable, piecewise-constant map.
        shade = random_map[np.minimum((z*8).astype(int), 7)]
    else: raise ValueError(dev)
    m[:, 0] = np.maximum(mu_floor(x[:, 0]), cap[:, 0]-shade)
    return m


def mu_floor(x0): return .16 + .04*x0


class GridETC:
    def __init__(self, k, h, q, seed):
        self.k, self.h, self.q, self.seed, self.cells = k, h, q, seed, {}
    def key(self, x):
        b=math.ceil(1/self.h)
        return tuple(np.minimum((x/self.h).astype(int), b-1))
    def state(self, key):
        if key not in self.cells:
            # Stable cell-specific randomness, independent of observed rewards.
            ss=np.random.SeedSequence([self.seed, *key]); rng=np.random.default_rng(ss)
            self.cells[key]={"v":0,"n":np.zeros(self.k,int),"z":np.zeros(self.k),
                             "perms":[rng.permutation(self.k) for _ in range(self.q)],
                             "priority":rng.permutation(self.k)}
        return self.cells[key]
    def choose(self, x):
        st=self.state(self.key(x)); v=st["v"]
        if v < self.k*self.q: a=int(st["perms"][v//self.k][v%self.k]); exploring=True
        else:
            score=st["z"]/self.q; mx=score.max()
            top=set(np.flatnonzero(score==mx)); a=next(int(j) for j in st["priority"] if j in top); exploring=False
        st["v"]+=1
        return a,st,exploring
    def update(self, st, a, y, exploring):
        if exploring: st["n"][a]+=1; st["z"][a]+=y


def path(x, mu, target, uniforms, n, h, q, coupling_seed):
    alg=GridETC(3,h,q,coupling_seed); util=reward=effort=arm0_pulls=explore=0.
    for t in range(n):
        a,st,is_exp=alg.choose(x[t]); y=float(uniforms[t,a] < target[t,a]); alg.update(st,a,y,is_exp)
        reward += target[t,a]; effort += target[t,a]-mu[t,a]; explore += is_exp
        if a==0: util += 1+mu[t,0]-target[t,0]; arm0_pulls += 1
    return util,reward,effort,arm0_pulls,explore,len(alg.cells)


def one(spec):
    rep,n,dev,seed=spec; rng=np.random.default_rng(seed)
    K=3; d=1; D=K*d
    x=rng.random((n,D)); mu,cap=means(x)
    uniforms=rng.random((n,K)); h=n**(-1/(D+3)); q=math.ceil(n**(2/(D+3)))
    random_map=rng.choice([0.,.06,.12,.18], size=8, replace=True)
    altered=targets(cap,x,dev,h,random_map)
    base=path(x,mu,cap,uniforms,n,h,q,777000+rep)
    devi=path(x,mu,altered,uniforms,n,h,q,777000+rep)
    return dict(rep=rep,seed=seed,n=n,deviation=dev,K=K,d=d,D=D,h=h,q=q,
                baseline_utility=base[0],deviation_utility=devi[0],utility_gain=devi[0]-base[0],
                gain_per_round=(devi[0]-base[0])/n,baseline_reward=base[1],deviation_reward=devi[1],
                reward_change=devi[1]-base[1],baseline_effort=base[2],deviation_effort=devi[2],
                baseline_arm0_pulls=base[3],deviation_arm0_pulls=devi[3],
                exploration_rounds=base[4],visited_cells=base[5])


def summarize(rows, B=4000):
    rng=np.random.default_rng(20260828); out=[]
    for n in sorted({r["n"] for r in rows}):
      for dev in DEVS:
        rs=[r for r in rows if r["n"]==n and r["deviation"]==dev]; z={"n":n,"deviation":dev,"reps":len(rs)}
        for metric in ["utility_gain","gain_per_round","reward_change","deviation_arm0_pulls","baseline_arm0_pulls"]:
            a=np.array([r[metric] for r in rs]); boot=a[rng.integers(0,len(a),(B,len(a)))].mean(1)
            z[metric+"_mean"]=a.mean(); z[metric+"_lo"]=np.quantile(boot,.025); z[metric+"_hi"]=np.quantile(boot,.975)
        out.append(z)
    return out


def write_csv(path, rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--reps",type=int,default=240); ap.add_argument("--workers",type=int,default=1); ap.add_argument("--quick",action="store_true"); a=ap.parse_args()
    reps=4 if a.quick else max(240,a.reps); horizons=[2000,8000] if a.quick else [2000,8000,32000]
    specs=[]
    for n in horizons:
      for dev_i,dev in enumerate(DEVS):
       for rep in range(reps): specs.append((rep,n,dev,86000000+n*1000+dev_i*100000+rep))
    if a.workers==1: rows=[one(s) for s in specs]
    else:
      with ProcessPoolExecutor(max_workers=a.workers) as ex: rows=list(ex.map(one,specs,chunksize=4))
    OUT.mkdir(parents=True,exist_ok=True); write_csv(OUT/"trials.csv",rows); write_csv(OUT/"summary.csv",summarize(rows))
    print(f"wrote {len(rows)} paired trials; minimum reps per plotted cell={reps}")

if __name__=="__main__": main()
