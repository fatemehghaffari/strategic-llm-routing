"""BASELINE 3: the Second-Best Utility Guarantee Mechanism, in two settings.

Cao, Wang, Liu, Li, Tao and He, "Pay for The Second-Best Service: A
Game-Theoretic Approach Against Dishonest LLM Providers", WWW 2026, pages
249-260, DOI 10.1145/3774904.3792446, arXiv:2511.00847v5.

REIMPLEMENTED FROM THE PAPER. No code and no artifact were released. This is
THEIR mechanism run under THIS paper's observation model with the three
modifications documented in `mechanisms.run_second_best`. NOTHING HERE
REPRODUCES THEIR RESULTS IN THEIR OWN SETTING, WHERE THEY ARE CORRECT.

SETTING ONE, SCALAR. A fair head-to-head on single-context instances, where
both mechanisms are in scope. Each provider has one capability, which is
exactly their model. The comparison isolates elicitation budget, monitor design
and failure handling, because with L = 1 their proposed provider behaviour
reduces to delivering the smallest feasible mean meeting the announced value,
which is our own proposed profile, so BOTH MECHANISMS ARE SCORED UNDER
IDENTICAL PROVIDER BEHAVIOUR.

SETTING TWO, CONTEXTUAL. Their mechanism was NEVER CLAIMED for contextual
settings and is correct in the setting it does claim. It is run here on
contextual instances deliberately outside its stated scope, and the question is
NOT whose mechanism is better: it is what it costs to price a task-dependent
capability with a scalar rule. OUR OWN SCALAR MECHANISM SITS IN THE SAME COLUMN
for exactly that reason, so that the finding is about scalarness rather than
about any one design. Our contextual mechanism is the third column.

Contextual triples are selected by the ANALYTIC mass on which a single
announced price exceeds the winner's capability, computed in
`analytic_gap_triples.csv` before any of this was run: the minimum, the median
and the maximum over the 165 subsets.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from mechanisms import (Instance, MechanismRun, ProfileStrategy,  # noqa: E402
                        honest_benchmark_per_round, oracle_per_round,
                        run_second_best, second_capability_per_round)
from run_sim import draw_queries  # noqa: E402

Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]
# fixed before any run, by the analytic price-infeasibility mass
CTX_TRIPLES = {
    "infeas_none": "Claude-Instant-V1|Claude-V1|GPT-4",
    "infeas_mid": "CodeLlama-34B|Mixtral-8x7B|WizardLM-13B",
    "infeas_high": "Claude-V1|Llama-70B|WizardLM-13B",
}
SCALAR_TRIPLES = {
    "lowflip": "CodeLlama-34B|GPT-3.5|GPT-4",
    "midflip": "Claude-V2|GPT-3.5|WizardLM-13B",
    "highflip": "Claude-V2|CodeLlama-34B|WizardLM-13B",
    "dominant": "GPT-4|Yi-34B|Mistral-7B",
}
DEVIATIONS = ["proposed", "their_equilibrium", "baitswitch", "undercut0.02",
              "theta0.90"]


class TheirEquilibrium(ProfileStrategy):
    """Their Theorem 5.2 provider strategy, under L = 1.

    Truthful in the exploration phase, the smallest feasible mean meeting the
    announced value in the exploitation phase, and MINIMUM COST in the two
    blind-trust phases, where the paper explicitly permits providers to
    maximise their own utility. Scoring under identical behaviour instead maps
    their blind trust onto our fallback, where our proposed profile delivers
    capability, and that is GENEROUS TO THEM ON REVENUE. Both are reported.
    """

    def target(self, i, phase, q, price, state=None):
        M, mu = self.inst.M[q, i], self.inst.mu[q, i]
        if phase == "elicit":
            return M
        if phase == "primary" and price is not None:
            m = min(price, M)
            return max(mu, m) if self.inst.honest[i] else m
        return mu if not self.inst.honest[i] else mu


class BaitSwitch(ProfileStrategy):
    """Elicit at capability, then floor in the priced phase."""

    def __init__(self, inst, tm, second, deviator):
        super().__init__(inst, ["proposed"] * inst.K, tm, second=second)
        self.deviator = deviator

    def target(self, i, phase, q, price, state=None):
        if i == self.deviator and phase == "primary":
            return self.inst.mu[q, i]
        return super().target(i, phase, q, price, state)


def make_strategy(inst, tm, second, dev, devi):
    if dev == "their_equilibrium":
        return TheirEquilibrium(inst, ["proposed"] * inst.K, tm, second=second)
    if dev == "proposed" or devi is None:
        return ProfileStrategy(inst, ["proposed"] * inst.K, tm, second=second)
    if dev == "baitswitch":
        return BaitSwitch(inst, tm, second, devi)
    opts = ["proposed"] * inst.K
    opts[devi] = dev
    return ProfileStrategy(inst, opts, tm, second=second)


def scalarize(inst):
    return Instance(M=inst.M, mu=inst.mu, key=np.zeros_like(inst.key),
                    honest=inst.honest, names=inst.names)


def price_above_capability_mass(inst, p, tau, winner):
    """Arrival mass on which a single announced price exceeds the winner's
    capability. Zero by construction for a per-context price."""
    if winner < 0 or not np.isfinite(tau):
        return np.nan
    return float(p[(tau > inst.M[:, winner] + 1e-12)].sum())


def run_cell(setting, label, models, alpha, context, n, seeds, rows,
             gate_blind2=True, out_path=None):
    fams = [context] if setting == "scalar" else Q7
    inst, p, gm, av = I.finite_instance(models, fams, alpha)
    flat = scalarize(inst)
    tm = I.top_masks(inst)
    second = np.sort(inst.M, axis=1)[:, -2]
    qs0 = draw_queries(inst, p, n, 0)
    base = {"setting": setting, "triple": label, "models": "|".join(models),
            "alpha": alpha, "context": context if setting == "scalar" else "Q7",
            "n": n, "nseeds": len(seeds), "gate_blind2": gate_blind2,
            "oracle": oracle_per_round(inst, qs0),
            "second_cap": second_capability_per_round(inst, qs0),
            "honest_bench": honest_benchmark_per_round(inst, qs0)}
    mechs = ["second_best", "mesp_scalar"]
    if setting == "contextual":
        mechs.append("plmesp")
    for mech in mechs:
        for dev in DEVIATIONS:
            if dev == "their_equilibrium" and mech != "second_best":
                continue
            for devi in ([None] if dev in ("proposed", "their_equilibrium")
                         else range(inst.K)):
                res = []
                for s in seeds:
                    qs = draw_queries(inst, p, n, s)
                    used = flat if mech in ("second_best", "mesp_scalar") else inst
                    st = make_strategy(used, tm, second, dev, devi)
                    if mech == "second_best":
                        r = run_second_best(used, n, s, st, qs,
                                            gate_blind2=gate_blind2)
                        r["compliant_convictions"] = (
                            1.0 if (r["monitor_fired"]
                                    and dev in ("proposed", "their_equilibrium"))
                            else 0.0)
                        r["convictions"] = 1.0 if r["monitor_fired"] else 0.0
                        r["post_fire_revenue_per_round"] = (
                            0.0 if r["post_fire_rounds"] > 0 else np.nan)
                        r["detection_delay"] = (r["fired_at_exploitation_round"]
                                                if r["monitor_fired"] else np.nan)
                        r["price_above_cap_mass"] = price_above_capability_mass(
                            used, p, r["announced_second_best_utility"] + r["price"],
                            r["winner"])
                    else:
                        run = MechanismRun(used, n, s)
                        r = run.run(st, qs)
                        r["utility_per_round"] = (r["T"] - r["C"]) / n
                        r["monitor_fired"] = r["convictions"] > 0
                        r["undelegated_fraction"] = 0.0
                        r["post_fire_revenue_per_round"] = r[
                            "post_switch_revenue_per_round"]
                        dl = list(r["conviction_rounds"].values())
                        r["detection_delay"] = float(np.mean(dl)) if dl else np.nan
                        taus = [lo.tau for lo in run.locals.values()
                                if lo.phase != "elicit"]
                        wins = [lo.W for lo in run.locals.values()
                                if lo.phase != "elicit"]
                        r["price_above_cap_mass"] = (
                            price_above_capability_mass(used, p, float(np.mean(taus)),
                                                        wins[0])
                            if len(taus) == 1 else
                            float(r["primary_rounds_price_above_capability"]) / n)
                    res.append(r)
                u = np.mean([r["utility_per_round"] for r in res], axis=0)
                rows.append({
                    **base, "mech": mech, "deviation": dev,
                    "deviator_index": devi,
                    "deviator": models[devi] if devi is not None else "",
                    "revenue_per_round": float(np.mean(
                        [r["revenue_per_round"] for r in res])),
                    "monitor_fire_rate": float(np.mean(
                        [float(r["monitor_fired"]) for r in res])),
                    "compliant_conviction_rate": float(np.mean(
                        [float(r["compliant_convictions"] > 0) for r in res]))
                    if dev in ("proposed", "their_equilibrium") else np.nan,
                    "undelegated_fraction": float(np.mean(
                        [r.get("undelegated_fraction", 0.0) for r in res])),
                    "post_fire_revenue_per_round": float(np.nanmean(
                        [r["post_fire_revenue_per_round"] for r in res]))
                    if any(np.isfinite(r["post_fire_revenue_per_round"])
                           for r in res) else np.nan,
                    "detection_delay": float(np.nanmean(
                        [r["detection_delay"] for r in res]))
                    if any(np.isfinite(r["detection_delay"]) for r in res) else np.nan,
                    "price_above_cap_mass": float(np.nanmean(
                        [r["price_above_cap_mass"] for r in res])),
                    **{f"util_{j}": u[j] for j in range(inst.K)}})
        if out_path:
            pd.DataFrame(rows).to_csv(out_path, index=False)
        print(f"done {setting} {label} {alpha} {context} {mech} "
              f"({len(rows)} rows written)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300000)
    ap.add_argument("--nseeds", type=int, default=20)
    ap.add_argument("--alphas", default="a0.00,a0.25,a0.50,a0.75,het")
    ap.add_argument("--gate-blind2", type=int, default=1,
                    help="1 gates BOTH blind-trust phases on validated, which is "
                         "the reading on which their line-18 break means the "
                         "remaining queries are never delegated. 0 is the "
                         "alternative, generous to them, in which phase II still "
                         "runs after the monitor fires.")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    jobs = []
    for al in a.alphas.split(","):
        for lab, ms in SCALAR_TRIPLES.items():
            for ctx in ("MMLU", "GSM8K"):
                jobs.append(("scalar", lab, ms.split("|"), al, ctx))
        for lab, ms in CTX_TRIPLES.items():
            jobs.append(("contextual", lab, ms.split("|"), al, "Q7"))
    jobs = [j for k, j in enumerate(jobs) if k % a.nshards == a.shard]
    rows = []
    for setting, lab, models, al, ctx in jobs:
        run_cell(setting, lab, models, al, ctx, a.n, list(range(a.nseeds)), rows,
                 gate_blind2=bool(a.gate_blind2), out_path=a.out)
    pd.DataFrame(rows).to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
