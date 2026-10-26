#!/usr/bin/env python3
"""Executable checks of the construction and retained output."""
import csv
from pathlib import Path
import numpy as np
from run import DEVS, means, targets

p=Path(__file__).resolve().parent
rng=np.random.default_rng(44); x=rng.random((200000,3)); mu,cap=means(x)
assert np.all(mu <= cap) and np.all(cap <= 1) and np.all(mu >= 0)
assert np.all(cap[:,0] == cap[:,1]) and np.all(cap[:,2] < cap[:,0])
# Each arm's primitives are invariant when only other arms' local contexts change.
for i in range(3):
    xp=x.copy(); xp[:,[j for j in range(3) if j!=i]]=rng.random((len(x),2))
    mup,capp=means(xp); assert np.allclose(mu[:,i],mup[:,i]); assert np.allclose(cap[:,i],capp[:,i])
for n in [2000,8000,32000]:
    h=n**(-1/6); random_map=rng.choice([0.,.06,.12,.18],8)
    for dev in DEVS:
        m=targets(cap,x,dev,h,random_map); assert np.all(m >= mu) and np.all(m <= cap)
rows=list(csv.DictReader((p/'trials.csv').open()))
assert len(rows)==3600
for n in ['2000','8000','32000']:
  for dev in DEVS: assert sum(r['n']==n and r['deviation']==dev for r in rows)==240
print('all construction, feasibility, locality, top-set, and replication checks passed')
