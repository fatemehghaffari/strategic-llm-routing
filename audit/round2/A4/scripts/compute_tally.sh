#!/bin/bash
# Tally the actual wall clock and core-hours of every A4 Slurm job.
#   bash compute_tally.sh <jobid,jobid,...>
sacct -X -j "$1" --parsable2 --noheader --format=JobID,JobName,State,Elapsed,TotalCPU | python3 -c "
import sys, collections
def secs(t):
    t = t.strip(); d = 0
    if '-' in t:
        d, t = t.split('-'); d = int(d)
    p = [float(x) for x in t.split(':')]
    while len(p) < 3: p = [0] + p
    return d*86400 + p[0]*3600 + p[1]*60 + p[2]
agg = collections.defaultdict(lambda: [0, 0.0, 0.0, collections.Counter()])
for l in sys.stdin:
    f = l.rstrip('\n').split('|')
    if len(f) < 4: continue
    name, state, el = f[1], f[2].split()[0], f[3]
    a = agg[name]; a[0] += 1; a[1] += secs(el); a[2] = max(a[2], secs(el)); a[3][state] += 1
tot = 0.0
print('| job | tasks | longest task | sum of task elapsed (core-hours) | states |')
print('|---|---|---|---|---|')
for k, (n, s, mx, st) in sorted(agg.items()):
    tot += s
    print(f'| {k} | {n} | {mx/3600:.2f} h | {s/3600:.2f} | {dict(st)} |')
print(f'| **total** | | | **{tot/3600:.2f}** | |')
"
