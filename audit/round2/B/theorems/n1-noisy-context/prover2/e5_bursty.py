"""E5: hypothesis (N) is needed. Same label posterior pi = (0.8, 0.1, 0.1) in frequency, but the true types
arrive in blocks (8B of type 0, B of type 1, B of type 2, repeated). S*_N (water-fill, known pi) winner."""
import numpy as np
from label_mesp_sim import Agent, run
pi = np.array([0.8, 0.1, 0.1])
Ms = [np.array([0.9, 0.3, 0.6]), np.array([0.7, 0.8, 0.5]), np.array([0.5, 0.6, 0.9])]
mus = [np.zeros(3), np.zeros(3), np.array([0.2, 0.2, 0.3])]
hon = [False, False, True]
n = 100000
for B in [1, 10, 100, 500, 2000]:
    cyc = np.array([0] * (8 * B) + [1] * B + [2] * B)
    path = np.tile(cyc, n // len(cyc) + 1)[:n]
    # randomise the phase so Stage 1 sees the right mixture on average
    ags = [Agent(Ms[k], mus[k], hon[k], pi) for k in range(3)]
    o = run(ags, n, 40, 3, types=path)
    print(f"block B={B:5d}: conviction of S*_N winner = {o['switched'].mean():.2f}, winner={np.bincount(o['W'],minlength=3)}")
