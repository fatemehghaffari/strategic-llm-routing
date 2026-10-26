#!/usr/bin/env python3
"""Final paired scalar-incentive experiments for MESP-F.

Each (instance, horizon, replicate) uses the same seed for the prescribed
profile and every unilateral deviation.  The resulting differences are thus
paired common-random-number (CRN) estimates.  All rewards remain freshly
sampled after the selected arm chooses its target.
"""
from __future__ import annotations

import argparse
import csv
import math
import multiprocessing as mp
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Instance:
    name: str
    mu: tuple[float, ...]
    cap: tuple[float, ...]
    honest: tuple[bool, ...]
    focal: int


# Every instance has an honest arm.  The focal arm is always strategic.
INSTANCES = (
    Instance("unique_top", (.10, .20, .35), (.90, .65, .40), (False, False, True), 0),
    Instance("tied_top", (.10, .20, .35), (.80, .80, .45), (False, False, True), 0),
    Instance("near_gap", (.10, .20, .45), (.80, .76, .50), (False, False, True), 0),
    Instance("honest_top", (.75, .20, .15), (.75, .70, .45), (True, False, False), 1),
    # Designed so the strategic runner-up wins Stage 1 often enough to test
    # the low-gap non-top bait-and-switch deviation.
    Instance("low_gap_nontop", (.10, .20, .45), (.80, .795, .50), (False, False, True), 1),
)

BEHAVIORS = (
    "profile", "underbid_05", "underbid_15", "primary_shade_05",
    "primary_shade_15", "bait_switch", "trigger_fallback_shade",
    "nontop_win_underperform",
)


def design(n: int, k: int) -> tuple[int, int, float]:
    ell = min(n // (2 * k), math.ceil(n ** (2 / 3) * math.log(math.e * n) ** (1 / 3)))
    return ell, n - k * ell, math.sqrt(math.log(2 * k * n**4) / (2 * ell))


def target(inst: Instance, behavior: str, arm: int, phase: str, tau: float) -> float:
    mu, cap, honest = inst.mu[arm], inst.cap[arm], inst.honest[arm]
    if phase == "bid":
        m = cap
        if arm == inst.focal and behavior == "underbid_05": m = cap - .05
        if arm == inst.focal and behavior == "underbid_15": m = cap - .15
    elif phase == "primary":
        m = min(tau, cap)
        if honest: m = max(mu, m)
        if arm == inst.focal and behavior == "primary_shade_05": m = tau - .05
        if arm == inst.focal and behavior == "primary_shade_15": m = tau - .15
        if arm == inst.focal and behavior in {"bait_switch", "trigger_fallback_shade",
                                              "nontop_win_underperform"}: m = 0
    else:
        m = cap
        if arm == inst.focal and behavior == "trigger_fallback_shade": m = 0
    return float(np.clip(max(mu, m) if honest else m, 0, cap))


def exp3(rng: np.random.Generator, inst: Instance, behavior: str, h: int) -> tuple[np.ndarray, np.ndarray, int]:
    k = len(inst.cap); pulls = np.zeros(k, int); efforts = np.zeros(k); reward = 0
    if h <= 0: return pulls, efforts, reward
    gamma = min(.5, math.sqrt(k * math.log(k) / h)); eta = gamma / k
    logw = np.zeros(k)
    fb_targets = np.asarray(inst.cap, dtype=float).copy()
    if behavior == "trigger_fallback_shade": fb_targets[inst.focal] = 0.
    fb_targets = np.where(np.asarray(inst.honest), np.maximum(fb_targets, inst.mu), fb_targets)
    for _ in range(h):
        z = logw - logw.max(); q = np.exp(z); q /= q.sum()
        p = (1 - gamma) * q + gamma / k
        u = rng.random(); a = int(np.searchsorted(np.cumsum(p), u, side="right")); m = fb_targets[a]
        y = int(rng.random() < m)
        pulls[a] += 1; efforts[a] += m - inst.mu[a]; reward += y
        logw[a] += eta * y / p[a]
    return pulls, efforts, reward


def trial(inst: Instance, n: int, seed: int, behavior: str) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed); k = len(inst.cap)
    if n < 2 * k:
        raise ValueError("final experiment uses only n >= 2K")
    ell, primary_budget, s = design(n, k)
    priority = rng.permutation(k); rank = np.empty(k, int); rank[priority] = np.arange(k)
    bid_m = np.array([target(inst, behavior, i, "bid", 0) for i in range(k)])
    successes = rng.binomial(ell, bid_m); beta = successes / ell
    order = sorted(range(k), key=lambda i: (-beta[i], rank[i]))
    winner = order[0]; tau = max(0., beta[order[1]] - s)
    pulls = np.full(k, ell, int); effort = ell * (bid_m - np.asarray(inst.mu)); reward = int(successes.sum())
    z = 0; q = 0; switched = False
    threshold_const = math.log(2 * n**4) / 2
    # The primary target is constant for every behavior tested here.  Generate
    # the full Bernoulli stream at once and locate the first threshold crossing;
    # this is distributionally identical to the roundwise implementation.
    m = target(inst, behavior, winner, "primary", tau)
    stream = rng.random(primary_budget) < m
    cs = np.cumsum(stream); rr = np.arange(1, primary_budget + 1)
    crossing = np.flatnonzero(cs < rr * tau - np.sqrt(rr * threshold_const))
    q = int(crossing[0] + 1) if crossing.size else primary_budget
    switched = bool(crossing.size); z = int(cs[q - 1])
    pulls[winner] += q; effort[winner] += q * (m - inst.mu[winner]); reward += z
    h = primary_budget - q if switched else 0
    if h:
        fp, fe, fr = exp3(rng, inst, behavior, h)
        pulls += fp; effort += fe; reward += fr
    assert pulls.sum() == n
    utility = pulls - effort
    return {
        "instance": inst.name, "n": n, "behavior": behavior, "seed": seed,
        "focal": inst.focal, "focal_utility": utility[inst.focal],
        "platform_reward": reward, "total_effort": effort.sum(),
        "winner": winner, "focal_won": int(winner == inst.focal), "tau": tau,
        "fallback": int(switched), "primary_rounds": q, "fallback_rounds": h,
        "stage1_rounds": k * ell, "total_rounds": int(pulls.sum()),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def run_pair(job: tuple[Instance, int, int]) -> list[dict]:
    inst, n, pair_seed = job
    ans = []
    for behavior in BEHAVIORS:
        if behavior == "nontop_win_underperform" and inst.name != "low_gap_nontop": continue
        ans.append(trial(inst, n, pair_seed, behavior))
    return ans


def boot_ci(x: np.ndarray, rng: np.random.Generator, draws: int = 4000) -> tuple[float, float]:
    means = np.empty(draws); m = len(x)
    for j in range(draws): means[j] = x[rng.integers(0, m, m)].mean()
    return tuple(np.quantile(means, [.025, .975]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=120)
    ap.add_argument("--tied-reps", type=int, default=240)
    ap.add_argument("--horizons", type=int, nargs="+", default=[2000, 8000, 20000])
    ap.add_argument("--seed", type=int, default=20260828)
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args(); HERE.mkdir(parents=True, exist_ok=True)
    jobs = []
    for ii, inst in enumerate(INSTANCES):
        reps = args.tied_reps if inst.name in {"tied_top", "low_gap_nontop"} else args.reps
        for n in args.horizons:
            for rep in range(reps):
                pair_seed = int(np.random.SeedSequence([args.seed, ii, n, rep]).generate_state(1)[0])
                jobs.append((inst, n, pair_seed))
    if args.workers == 1:
        batches = map(run_pair, jobs)
        rows = [r for batch in batches for r in batch]
    else:
        with mp.get_context("spawn").Pool(args.workers) as pool:
            rows = [r for batch in pool.imap(run_pair, jobs, chunksize=2) for r in batch]
    write_csv(HERE / "trials.csv", rows)
    index = {(r["instance"], r["n"], r["seed"], r["behavior"]): r for r in rows}
    paired = [] ; brng = np.random.default_rng(args.seed + 1)
    for inst in INSTANCES:
        for n in args.horizons:
            behaviors = [b for b in BEHAVIORS if b != "profile" and
                         (b != "nontop_win_underperform" or inst.name == "low_gap_nontop")]
            seeds = sorted({int(r["seed"]) for r in rows if r["instance"] == inst.name and r["n"] == n})
            for b in behaviors:
                for metric in ("focal_utility", "platform_reward", "fallback", "fallback_rounds"):
                    x = np.array([float(index[(inst.name,n,s,b)][metric]) -
                                  float(index[(inst.name,n,s,"profile")][metric]) for s in seeds])
                    lo, hi = boot_ci(x, brng)
                    paired.append({"instance":inst.name,"n":n,"behavior":b,"metric":metric,
                                   "reps":len(x),"mean":x.mean(),"ci_low":lo,"ci_high":hi})
    write_csv(HERE / "paired_summary.csv", paired)
    print(f"wrote {len(rows)} trials and {len(paired)} paired summaries")


if __name__ == "__main__": main()
