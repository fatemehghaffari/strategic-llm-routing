"""B2(b) toy with a hand-derivable answer (A5, Agent B).

One task type. Provider A strategic, M = 0.9, mu = 0.3. Provider H honest,
M = mu = 0.42 (it delivers 0.42 always). Arms theta in {0, 0.1, ..., 1}, m = theta * M.
  router (UCB): A is selected only if its mean beats 0.42; the cheapest winning
    arm is theta = 0.5 (m = 0.45). theta = 0.4 gives 0.36 and loses the traffic.
  PL-MESP: A wins the elicitation iff its elicited value beats 0.42, and the price
    is 0.42 - s_n (~0.386 at n = 1e6). theta = 0.4 (0.36) is convicted within
    ~4e4 primary rounds; theta = 0.5 is the cheapest compliant arm.
Known answer in both: A's route / primary arm -> 0.5 (and elicit arm -> 0.5 under PL-MESP).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mechanisms import Instance, MechanismRun, run_router
from learners import Learner

def inst():
    return Instance(M=np.array([[0.9, 0.42]]), mu=np.array([[0.3, 0.42]]), key=np.arange(1),
                    honest=np.array([False, True]), names=["A", "H"])

def summarise(st, ph):
    lg = st.log["0"]
    E = len(lg); last = lg[int(0.9 * E):]
    p = np.mean([np.asarray(r["probs"][ph]) for r in last], axis=0)
    return {"mode_arm": float(np.round(np.argmax(p) * 0.1, 1)), "p_mode": float(p.max()),
            "p_arm_0.5": float(p[5]), "converged": st.convergence()[0]}

def main(n=1_000_000, seeds=3, eta=None, schedule=None):
    out = {}
    for s in range(seeds):
        I = inst(); qs = np.zeros(n, dtype=np.int64)
        st = Learner(I, n, s, eta_mult=eta, schedule=schedule)
        r = run_router(I, n, s, st, qs, rule="ucb")
        out[f"router_seed{s}"] = {**summarise(st, "route"), "rev": r["revenue_per_round"]}
        st = Learner(I, n, s, eta_mult=eta, schedule=schedule)
        run = MechanismRun(I, n, s); r = run.run(st, qs)
        lo = list(run.locals.values())[0]
        out[f"plmesp_seed{s}"] = {"primary": summarise(st, "primary"), "elicit": summarise(st, "elicit"),
                                  "rev": r["revenue_per_round"], "tau": lo.tau, "W": lo.W,
                                  "convictions": r["convictions"]}
    return out

if __name__ == "__main__":
    eta = float(sys.argv[1]) if len(sys.argv) > 1 else None
    sched = sys.argv[2] if len(sys.argv) > 2 else None
    n = int(float(sys.argv[3])) if len(sys.argv) > 3 else 1_000_000
    print(json.dumps(main(n=n, eta=eta, schedule=sched), indent=1))
