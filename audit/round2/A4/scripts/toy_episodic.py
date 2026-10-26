"""Episodic-learner check on the B2(b) two-provider toy (29 Sep 2026).
Known answer in both rules: A's route / primary arm -> 0.5 (elicit -> 0.5 under PL-MESP).
usage: toy_episodic.py <rule: ucb|plmesp> <seed> <episode_len> <episodes> <eta_mult> <out.json>"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mechanisms import MechanismRun, run_router
from learners import EpisodicLearner, ARMS
from toy_learners import inst

def main(rule, seed, n, E, eta, out):
    I = inst(); qs = np.zeros(n, dtype=np.int64)
    L = EpisodicLearner(I, E, seed, eta_mult=eta)
    hist = []
    for e in range(E):
        L.new_episode(n)
        s = 10_000 * seed + e
        if rule == "ucb":
            r = run_router(I, n, s, L, qs, rule="ucb"); conv = None
        else:
            run = MechanismRun(I, n, s); r = run.run(L, qs); conv = int(r["convictions"])
        arms = dict(L.agents[0].arm)
        L.end_episode()
        hist.append({"ep": e, "rev": r["revenue_per_round"], "conv": conv,
                     "arms": {k: float(ARMS[v]) for k, v in arms.items()}})
        if (e + 1) % 25 == 0 or e == E - 1:
            p = {ph: np.round(L.agents[0].p[ph], 3).tolist() for ph in L.agents[0].phases}
            last = hist[-25:]
            summ = {"episodes_done": e + 1, "rev_last25": float(np.mean([h["rev"] for h in last])),
                    "conv_last25": (None if conv is None else float(np.mean([h["conv"] > 0 for h in last]))),
                    "probs": p, "converged": L.convergence()[0]}
            json.dump({"rule": rule, "seed": seed, "n": n, "E": E, "eta": eta, "summary": summ,
                       "hist": hist}, open(out, "w"))

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], int(a[1]), int(float(a[2])), int(a[3]), float(a[4]), a[5])
