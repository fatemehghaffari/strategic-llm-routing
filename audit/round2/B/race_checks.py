import math, random
from ucb_mono_search import run

def race(seqs, n, prio):
    """Greedy merge on arbitrary per-arm sequences seqs[a][k] (k = count), lexicographic ties by prio."""
    K = len(seqs); T = [0]*K; pulls = []
    rank = {a: i for i, a in enumerate(prio)}
    for t in range(n):
        a = min(range(K), key=lambda a: (-seqs[a][T[a]], rank[a]))
        pulls.append(a); T[a] += 1
    return pulls, T

def envelope(seq):
    out = []; m = float('inf')
    for v in seq:
        m = min(m, v); out.append(m)
    return out

rng = random.Random(7)
# 1. envelope identity: race on f == race on running-min of f
bad = 0
for trial in range(20000):
    K = rng.choice([2,3,4,5]); n = rng.choice([5,10,20,40])
    seqs = [[rng.choice([rng.random(), rng.choice([0.0,0.25,0.5,0.75,1.0])]) for _ in range(n+1)] for _ in range(K)]
    prio = list(range(K)); rng.shuffle(prio)
    p1, _ = race(seqs, n, prio); p2, _ = race([envelope(s) for s in seqs], n, prio)
    if p1 != p2: bad += 1
print('envelope identity violations:', bad, 'of 20000')

# 2. static-race monotonicity: raise arm 0's sequence pointwise, arbitrary (non-monotone) sequences
bad = 0
for trial in range(20000):
    K = rng.choice([2,3,4,5]); n = rng.choice([5,10,20,40])
    seqs = [[rng.random() for _ in range(n+1)] for _ in range(K)]
    raised = [s[:] for s in seqs]
    raised[0] = [v + rng.random()*rng.choice([0,0,1]) for v in seqs[0]]
    prio = list(range(K)); rng.shuffle(prio)
    for t in range(1, n+1):
        _, TA = race(seqs, t, prio); _, TB = race(raised, t, prio)
        if any(TB[j] > TA[j] for j in range(1, K)): bad += 1; break
print('static race monotonicity violations (all times):', bad, 'of 20000')

# 3. known-horizon UCB, larger K and n, Bernoulli tapes, pointwise raise of arm 0
bad = 0; tot = 0
for K, n, c in [(3,20,0.5),(4,20,0.5),(5,30,0.5),(3,30,2.0),(4,40,1.0),(6,40,0.5)]:
    for trial in range(20000):
        base = [[rng.randint(0,1) for _ in range(n)] for _ in range(K)]
        raised = [r[:] for r in base]
        for k in range(n):
            if raised[0][k] == 0 and rng.random() < 0.5: raised[0][k] = 1
        prio = list(range(K))
        TA = run(base, n, K, c, 'hor', prio); TB = run(raised, n, K, c, 'hor', prio)
        tot += 1
        if any(TB[j] > TA[j] for j in range(1, K)): bad += 1
print('known-horizon UCB violations:', bad, 'of', tot)

# 4. trace the anytime counterexample found earlier (K=3, n=8, c=2)
base   = [[0,0,0,0,1,0,0,0],[0,0,1,0,0,1,1,1],[1,1,1,1,1,0,0,1]]
raised = [[1,0,0,1,1,1,0,1],[0,0,1,0,0,1,1,1],[1,1,1,1,1,0,0,1]]
def trace(tapes, n, K, c):
    T=[0]*K; S=[0]*K; out=[]
    for t in range(1,n+1):
        if t<=K: a=t-1; idx=None
        else:
            idx=[S[b]/T[b]+math.sqrt(c*math.log(t)/T[b]) for b in range(K)]
            a=max(range(K), key=lambda b:(idx[b], -b))
        S[a]+=tapes[a][T[a]]; T[a]+=1
        out.append((t, a, None if idx is None else [round(v,4) for v in idx], T[:]))
    return out
for name, tp in [('A (base)', base), ('B (raised arm 0)', raised)]:
    print(name)
    for row in trace(tp, 8, 3, 2.0): print('  ', row)
