"""Brute-force search for a pathwise monotonicity violation of index policies
with per-arm reward tapes indexed by local pull count (common-uniform coupling).
Raising arm 0's tape pointwise; ask whether T_j(n) for some j != 0 increases.
Index variants: 'hor' = mean + sqrt(c*log(n)/T) (known horizon, local count only)
                'any' = mean + sqrt(c*log(t)/T) (anytime, global time t)
Ties: fixed common priority order (a realization of coupled tie uniforms).
Init: pull arms in fixed order 0..K-1 once each (a realization of the random order).
"""
import itertools, math, random, sys

def run(tapes, n, K, c, variant, prio):
    T = [0]*K; S = [0]*K
    for t in range(1, n+1):
        if t <= K:
            a = t-1
        else:
            L = math.log(n) if variant == 'hor' else math.log(t)
            best = None; bestv = None
            for a_ in prio:  # earlier in prio wins ties
                v = S[a_]/T[a_] + math.sqrt(c*L/T[a_])
                if bestv is None or v > bestv + 1e-12:
                    best, bestv = a_, v
            a = best
        S[a] += tapes[a][T[a]]; T[a] += 1
    return T

def search(K, n, c, variant, trials, seed):
    rng = random.Random(seed)
    prio = list(range(K))
    found = []
    for _ in range(trials):
        base = [[rng.randint(0,1) for _ in range(n)] for _ in range(K)]
        raised = [row[:] for row in base]
        for k in range(n):
            if raised[0][k] == 0 and rng.random() < 0.5: raised[0][k] = 1
        TA = run(base, n, K, c, variant, prio); TB = run(raised, n, K, c, variant, prio)
        for j in range(1, K):
            if TB[j] > TA[j]:
                found.append((base, raised, TA, TB, j)); break
        if len(found) >= 3: break
    return found

if __name__ == '__main__':
    for variant in ['hor', 'any']:
        for K in [2, 3]:
            for n in [6, 8, 10, 14]:
                for c in [0.5, 2.0]:
                    f = search(K, n, c, variant, 60000, 1)
                    print(variant, 'K', K, 'n', n, 'c', c, 'violations found:', len(f))
                    if f:
                        base, raised, TA, TB, j = f[0]
                        print('  base tapes  ', base); print('  raised tapes', raised)
                        print('  counts A', TA, 'counts B', TB, 'arm', j, 'increased')
