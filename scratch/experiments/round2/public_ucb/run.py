"""Public-capacity UCB: in-class (S_HI) exploitability, FATA, and the index comparison (E3c).

Symmetric UCB of Stochastic_SAMF_Conditions.tex: uniform random initialization order, index
hat m_a + bonus(T_a), independent uniform tie-breaking. The bonus is the known-horizon sqrt(4 log n / T_a) by
default (main-agent decision) with the anytime sqrt(2 log t / T_a) retained for comparison.

Coupling: agent a's r-th pull reads U[rep, a, r], the coupling used in the proofs, so raising an agent's fixed
target raises its own rewards pathwise and leaves every other agent's reward tape untouched.

Outputs: (1) the paired utility gain of each fixed target for the focal agent against all-maximum play, whose
maximum over the grid is the grid-resolved in-class exploitability; (2) expected pull-count differences between
two tied top agents (FATA) for symmetric and index-order initialization; (3) pathwise monotonicity violation
counts for both indices, which is the measurement behind the remark that the anytime index is not monotone.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import instances as I, seeds as S, stats as ST  # noqa: E402
from common.design import ucb_bonus  # noqa: E402


def run_ucb(targets, mu, U, n, index, init="symmetric", ties="perround", rng=None):
    """Vectorized symmetric UCB over R replicates. U has shape (R, K, n). Returns pulls (R, K) and reward (R,)."""
    R, K, _ = U.shape
    targets = np.asarray(targets, float)
    cnt = np.zeros((R, K), int); sm = np.zeros((R, K)); reward = np.zeros(R)
    order = np.tile(np.arange(K), (R, 1))
    if init == "symmetric":
        order = np.argsort(rng.random((R, K)), axis=1)
    prio = np.argsort(rng.random((R, K)), axis=1) if ties == "priority" else None
    rank = np.empty((R, K), int)
    if prio is not None:
        np.put_along_axis(rank, prio, np.tile(np.arange(K), (R, 1)), axis=1)
    rows = np.arange(R)
    coins = rng.random((R, n)) if ties == "perround" else None
    for t in range(n):
        if t < K:
            a = order[:, t]
        else:
            with np.errstate(divide="ignore", invalid="ignore"):
                idx = sm / cnt + ucb_bonus(cnt, t + 1, n, index)
            mx = idx.max(axis=1, keepdims=True)
            is_max = idx >= mx - 1e-12
            if ties == "perround":
                nmax = is_max.sum(axis=1)
                pick = np.floor(coins[:, t] * nmax).astype(int)
                a = np.argmax(np.cumsum(is_max, axis=1) == (pick + 1)[:, None], axis=1)
            else:
                masked = np.where(is_max, rank, K + 1)
                a = np.argmin(masked, axis=1)
        y = (U[rows, a, cnt[rows, a]] < targets[a]).astype(float)
        cnt[rows, a] += 1; sm[rows, a] += y; reward += y
    return cnt, reward


def tape(inst, n, reps, phase, rep0=0):
    key = S.trial_seed_sequence("public_ucb", phase, inst.index, n, rep0)
    g = np.random.default_rng(key)
    return g.random((reps, inst.K, n)), np.random.default_rng(S.trial_seed_sequence("public_ucb", phase, inst.index, n, rep0 + 10 ** 6))


def sweep(inst, n, reps, index, phase, grid_pts=41, init="symmetric", ties="perround"):
    U, _ = tape(inst, n, reps, phase)
    i = inst.focal; base_t = np.array(inst.M, float)
    lo = inst.mu[i] if inst.is_honest(i) else 0.0
    grid = np.linspace(lo, inst.M[i], grid_pts)
    rows = []
    cnt0, _ = run_ucb(base_t, inst.mu, U, n, index, init, ties, np.random.default_rng(S.trial_seed_sequence("public_ucb", phase, inst.index, n, 7)))
    u_base = cnt0[:, i] * (1 + inst.mu[i] - base_t[i])
    for m in grid:
        t = base_t.copy(); t[i] = m
        cnt, rew = run_ucb(t, inst.mu, U, n, index, init, ties, np.random.default_rng(S.trial_seed_sequence("public_ucb", phase, inst.index, n, 7)))
        u = cnt[:, i] * (1 + inst.mu[i] - m)
        d = (u - u_base) / n
        mean, clo, chi, se = ST.t_interval(d)
        rows.append({"instance": inst.alias, "n": n, "index": index, "init": init, "ties": ties, "reps": reps,
                     "target": float(m), "gain_per_round": mean, "gain_lo": clo, "gain_hi": chi,
                     "focal_share": float(cnt[:, i].mean() / n), "reward_per_round": float(rew.mean() / n)})
    best = max(rows, key=lambda r: r["gain_per_round"])
    return rows, best


def fata(inst, n, reps, index, phase, init, ties="perround"):
    """Two tied top agents at capacity: expected pull-count difference per round."""
    U, _ = tape(inst, n, reps, phase)
    cnt, _ = run_ucb(np.array(inst.M, float), inst.mu, U, n, index, init, ties,
                     np.random.default_rng(S.trial_seed_sequence("public_ucb", phase, inst.index, n, 11)))
    tops = [a for a in range(inst.K) if abs(inst.M[a] - inst.M_top) < 1e-12]
    if len(tops) < 2:   # FATA compares two agents with the same top reward law; a unique top agent has no partner
        return {"instance": inst.alias, "n": n, "index": index, "init": init, "reps": reps, "top_agents": len(tops),
                "share_diff_per_round": float("nan"), "lo": float("nan"), "hi": float("nan"), "abs_mean": float("nan")}
    d = (cnt[:, tops[0]] - cnt[:, tops[1]]) / n
    mean, lo, hi, se = ST.t_interval(d)
    return {"instance": inst.alias, "n": n, "index": index, "init": init, "reps": reps, "top_agents": len(tops),
            "share_diff_per_round": mean, "lo": lo, "hi": hi, "abs_mean": float(np.abs(d).mean())}


def monotonicity(inst, n, reps, index, phase, shade=0.10, raise_agent=0, ties="perround", init="symmetric"):
    """Raise one agent's fixed target to capacity on a shared tape; count paths where another agent gains pulls."""
    U, _ = tape(inst, n, reps, phase)
    g = lambda: np.random.default_rng(S.trial_seed_sequence("public_ucb", phase, inst.index, n, 13))
    low = np.array(inst.M, float); low[raise_agent] = max(0.0, inst.M[raise_agent] - shade)
    c_lo, _ = run_ucb(low, inst.mu, U, n, index, init, ties, g())
    c_hi, _ = run_ucb(np.array(inst.M, float), inst.mu, U, n, index, init, ties, g())
    others = [a for a in range(inst.K) if a != raise_agent]
    inc = (c_hi[:, others] > c_lo[:, others])
    return {"instance": inst.alias, "n": n, "index": index, "reps": reps, "shade": shade,
            "paths_with_violation": int(inc.any(axis=1).sum()),
            "violation_rate": float(inc.any(axis=1).mean()),
            "max_increase": int((c_hi[:, others] - c_lo[:, others]).max()),
            "mean_change_others": float((c_hi[:, others] - c_lo[:, others]).mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", nargs="+", default=["unique_top", "tied_top"])
    ap.add_argument("--n", type=int, nargs="+", default=[2000, 8000, 20000])
    ap.add_argument("--reps", type=int, default=200); ap.add_argument("--phase", default="final")
    ap.add_argument("--fata-n", type=int, nargs="+", default=None)
    ap.add_argument("--mono-n", type=int, nargs="+", default=[50, 200, 1000])
    ap.add_argument("--mono-reps", type=int, default=4000)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    sweeps, bests, fatas, monos = [], [], [], []
    for name in a.instances:
        inst = I.get(name)
        for n in (a.fata_n or []):
            if sum(1 for x in inst.M if abs(x - inst.M_top) < 1e-12) < 2 or n in a.n:
                continue
            for index in ["horizon", "anytime"]:
                for init in ["symmetric", "fixed"]:
                    f = fata(inst, n, max(a.reps, 4000), index, a.phase, init); fatas.append(f)
                    print(f"  FATA {inst.alias:12s} n={n:6d} {index:8s} init={init:9s}: share difference {f['share_diff_per_round']:+.7f} "
                          f"[{f['lo']:+.7f}, {f['hi']:+.7f}] (mean absolute {f['abs_mean']:.6f})")
        for n in a.n:
            for index in ["horizon", "anytime"]:
                rows, best = sweep(inst, n, a.reps, index, a.phase)
                sweeps += rows; bests.append({**best, "note": "grid-resolved in-class (S_HI) exploitability"})
                print(f"{inst.alias:12s} n={n:6d} {index:8s}: best fixed target {best['target']:.4f} gain {best['gain_per_round']:+.5f}/round "
                      f"[{best['gain_lo']:+.5f}, {best['gain_hi']:+.5f}], focal share {best['focal_share']:.3f}")
            if sum(1 for x in inst.M if abs(x - inst.M_top) < 1e-12) >= 2 and (a.fata_n is None or n in a.fata_n):
                for index in ["horizon", "anytime"]:
                    for init in ["symmetric", "fixed"]:
                        f = fata(inst, n, a.reps, index, a.phase, init); fatas.append(f)
                        print(f"  FATA {inst.alias:12s} n={n:6d} {index:8s} init={init:9s}: share difference {f['share_diff_per_round']:+.7f} "
                              f"[{f['lo']:+.7f}, {f['hi']:+.7f}] (mean absolute {f['abs_mean']:.6f})")
    for name in a.instances:
        inst = I.get(name)
        for n in a.mono_n:
            for index in ["horizon", "anytime"]:
                m = monotonicity(inst, n, a.mono_reps, index, a.phase); monos.append(m)
                print(f"  monotonicity {inst.alias:12s} n={n:5d} {index:8s}: {m['paths_with_violation']} of {m['reps']} paths "
                      f"({m['violation_rate']:.4f}), largest increase {m['max_increase']}")
    for rows, name in [(sweeps, "sweep"), (bests, "best"), (fatas, "fata"), (monos, "monotonicity")]:
        with (out / f"public_ucb_{name}.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"wrote 4 CSVs to {out}")


if __name__ == "__main__":
    main()
