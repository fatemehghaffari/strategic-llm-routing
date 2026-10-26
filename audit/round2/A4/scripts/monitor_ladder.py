"""Monitor ablation ladder, including a TWO-SAMPLE-TEST rung.

Two axes, the ones the paper's own ladder uses:
  false conviction rate: how often a FULLY COMPLIANT primary winner, playing
      the proposed profile exactly, is convicted and ejected;
  detection delay: how many primary rounds a bait-and-switch winner survives
      before the monitor fires.

Rungs:
  anytime(c)      the paper's cumulative boundary, Z_r < r*tau - c*b_n(r)
  anytime_noslack the same test with the boundary removed
  twosample(B,a)  a batched two-sample test of the served stream against the
      winner's own elicitation sample, in the ROLE that model-equality testing
      plays (Gao, Liang and Guestrin, ICLR 2025, arXiv:2410.20247, detect a
      distorted served model with an MMD two-sample test).  THIS IS NOT THEIR
      TEST AND NOT THEIR SYSTEM.  It is a two-sample test used for the same
      job, so that the two designs can be compared on the same two axes.
      Their setting also differs: they compare full output distributions from
      about ten samples per prompt, we compare a stream of binary outcomes.
  none            no monitoring

The Section 3 separation theorem forbids rules that react to EVERY single
observation at a fixed rate.  A batched two-sample test is not such a rule, so
this is a real comparison and the two-sample rung may legitimately win on
delay.
"""
import argparse
import itertools
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import Instance, MechanismRun, ProfileStrategy  # noqa: E402
from rb_common import OUT  # noqa: E402

Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


class LadderStrategy(ProfileStrategy):
    """Everyone plays the proposed profile except the named winner-behaviour."""

    def __init__(self, inst, tm, primary_behaviour):
        super().__init__(inst, ["proposed"] * inst.K, tm)
        self.pb = primary_behaviour

    def target(self, i, phase, q, price, state=None):
        if phase != "primary" or self.pb == "compliant":
            return super().target(i, phase, q, price, state)
        M, mu = self.inst.M[q, i], self.inst.mu[q, i]
        comply = max(mu, min(price, M)) if self.inst.honest[i] else min(price, M)
        if self.pb == "baitswitch":                 # elicit high, then floor
            return mu if not self.inst.honest[i] else mu
        if self.pb == "baitswitch_mild":            # floor only halfway
            return 0.5 * (mu + comply)
        if self.pb.startswith("shade"):
            # Deliver a CONSTANT amount below the announced price.  A fixed
            # buffer c tolerates any persistent shading smaller than c by
            # construction, so this is the deviation that tests the other half
            # of the fixed-buffer trade-off: the deviator knows the mechanism's
            # published parameters and shades just inside them.
            c = float(self.pb[5:])
            return float(np.clip(price - c, mu if self.inst.honest[i] else 0.0, M))
        raise ValueError(self.pb)


# BASELINE 2: the FIXED-BUFFER monitor.  Braverman et al. compare a selected
# arm's running average against the announced price using a buffer that does
# NOT grow with the number of pulls, after a burn-in.  Our boundary grows like
# sqrt(r).  The prediction our analysis makes is that a fixed buffer must
# either convict compliant agents early, when few pulls have accumulated, or
# miss persistent deviators, when many have, and that no single setting avoids
# both.  The sweep is wide enough to draw the tradeoff curve rather than a point.
FIXED_BUFFERS = (0.005, 0.01, 0.02, 0.05, 0.10, 0.20)
BURNINS = (100, 1000, 10000, None)          # None means the n^{3/4} default

RUNGS = ([("anytime", {"boundary_mult": c}) for c in (0.25, 0.5, 1.0, 2.0)]
         + [("fixedbuffer", {"buffer": b, "burnin": w})
            for b in FIXED_BUFFERS for w in BURNINS]
         + [("anytime_noslack", {})]
         + [("twosample", {"batch": B, "twosample_alpha": a})
            for B in (50, 200, 1000) for a in (1e-2, 1e-4, 1e-6)]
         + [("twosample_elicit", {"batch": 200, "twosample_alpha": 1e-4})]
         + [("none", {})])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--alphas", default="a0.25,a0.50,a0.75")
    ap.add_argument("--triple", default=None)
    ap.add_argument("--behaviour", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    from select_triples import flip_rate_table, pick
    tri = a.triple or pick(flip_rate_table(Q7))["midflip"]
    models = tri.split("|")
    rows = []
    t0 = time.time()
    for al in a.alphas.split(","):
        # ONE context, so the ladder isolates the monitor and nothing else
        inst, p, gm, av = I.finite_instance(models, ["MMLU"], al)
        flat = Instance(M=inst.M, mu=inst.mu, key=np.zeros_like(inst.key),
                        honest=inst.honest, names=inst.names)
        tm = I.top_masks(flat)
        qs = np.zeros(a.n, dtype=int)
        pbs = (a.behaviour,) if a.behaviour else ("compliant", "baitswitch", "baitswitch_mild")
        for pb in pbs:
            strat = LadderStrategy(flat, tm, pb)
            for mon, kw in RUNGS:
                conv, delays, revs = 0, [], []
                for s in range(a.reps):
                    run = MechanismRun(flat, a.n, s, monitor=mon, **kw)
                    r = run.run(strat, qs, stop_on_switch=True)
                    # revenue up to the switch only; the ladder does not measure
                    # revenue, see REPORT.md section 5
                    revs.append(r["revenue_per_round"])
                    if r["convictions"]:
                        conv += 1
                        delays.append(list(r["conviction_rounds"].values())[0])
                rows.append({
                    "alpha": al, "models": tri, "primary_behaviour": pb,
                    "monitor": mon, "params": json.dumps(kw), "n": a.n,
                    "reps": a.reps, "conviction_rate": conv / a.reps,
                    "median_delay": float(np.median(delays)) if delays else np.nan,
                    "p90_delay": float(np.percentile(delays, 90)) if delays else np.nan,
                    "mean_delay": float(np.mean(delays)) if delays else np.nan,
                    "revenue_per_round_until_switch": float(np.mean(revs))})
                print(rows[-1], flush=True)
    pd.DataFrame(rows).to_csv(a.out, index=False)
    print("elapsed", time.time() - t0)


if __name__ == "__main__":
    main()
