#!/usr/bin/env python3
"""Item 2 (ADVERSARY_OPEN.md): the two remainder constants of the proof of Prop. ctx-continuum-exact (i).

Manuscript:  H*-charge  2 n_C Pr(H*_C^c), summed with sum_C n_C <= n  ->  2 n^{-3}/K   (not in the display)
             bad-charge 2n sum_C Pr(bad_C) <= 2n * n * (2n^-5 + 2n^-4/K) = 4n^-3 + 4n^-2/K (display)
Correct:     H*-charge  sum_C 2 E[n_C 1{H*_C^c}] <= 2n Pr(U_C H*_C^c) <= 2n * J_n * n^-4/K = 2 J_n n^-3/K
             bad-charge sum over the J_n grid cubes: 2n * J_n * (2n^-5 + 2n^-4/K) = 4 J_n n^-4 + 4 J_n n^-3/K
Total correct remainder R = 4 J_n n^-4 + 6 J_n n^-3 / K; displayed D = 4 n^-3 + 4 n^-2 / K.
R <= D  iff  J_n <= 2n/3 (sufficient, and necessary for the 1/K terms at K large).
This script finds, per d, every n >= 2K (K=2) with J_n <= n (the paper's own proviso) but J_n > 2n/3,
(the bound of (i) exceeds n at all such n; see the horizon table of rem:ctx-horizons).
Analytic (not computed here): the random-count step is not a formality: a path that dumps the rest of the horizon
into a cube once its baseline monitor has left its band makes sum_C E[n_C 1{H*_C^c}] ~ n Pr(U H*^c),
which exceeds n * max_C Pr(H*_C^c) by the factor ~ (number of cubes that reach Stage 2).
"""
import math

def J(n, d):
    return math.ceil(n ** (1.0 / (d + 3))) ** d

for d in range(1, 11):
    bad = []
    n = 4
    # J_n is a step function; scan n up to where J_n <= 2n/3 surely (n >= (1.5*2^d)^((d+3)/3))
    top = int(max(64, (1.5 * 2 ** d) ** ((d + 3) / 3.0) * 4))
    top = min(top, 10 ** 7)
    for n in range(4, top + 1):
        Jn = J(n, d)
        if Jn <= n and Jn > 2 * n / 3:
            bad.append(n)
    rng = (min(bad), max(bad), len(bad)) if bad else None
    print(f"d={d:2d}: n with J_n<=n but J_n>2n/3 (range, count): {rng};  n_1(d)=2^(d(d+3)/3)={2**(d*(d+3)/3):.1f}")
