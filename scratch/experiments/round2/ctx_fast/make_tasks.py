"""Build the task list for a horizon sweep and pack it into balanced array-element bundles.

Packing is longest-processing-time-first onto `--bins` bundles, with cost estimated as n times a
measured nanoseconds-per-round constant, so that no array element runs much longer than the others.
"""
from __future__ import annotations

import argparse
import os

D2_CONFIGS = ["proposed", "underbid", "rider25", "rider50", "rider100", "both", "crash",
              "sabotage_joint"]
TAIL_CONFIGS = ["proposed", "crash", "sabotage_joint"]


def d2_tasks(seeds=4):
    grid = [6.0, 7.0, 7.5, 8.0, 8.25, 8.5, 8.75, 9.0, 9.1, 9.2, 9.3, 9.5, 9.8, 10.0, 10.25, 10.5]
    out = []
    for inst in ("C", "E"):
        for lg in grid:
            for cfg in D2_CONFIGS:
                for sd in range(seeds):
                    out.append((inst, lg, cfg, sd))
    return out


def d3_tasks():
    out = []
    for inst in ("D", "F"):
        for lg in [7.0, 8.0, 9.0, 10.0, 10.5, 11.0, 11.5]:
            for cfg in D2_CONFIGS:
                for sd in range(3):
                    out.append((inst, lg, cfg, sd))
        for lg in [11.8, 12.0]:
            for cfg in TAIL_CONFIGS:
                for sd in range(2):
                    out.append((inst, lg, cfg, sd))
    out.append(("D", 12.3, "proposed", 0))
    out.append(("D", 12.3, "sabotage_joint", 0))
    out.append(("F", 12.3, "proposed", 0))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--which", choices=["d2", "d3"], required=True)
    ap.add_argument("--bins", type=int, default=200)
    ap.add_argument("--out", required=True)
    ap.add_argument("--nsr", type=float, default=20.0)
    a = ap.parse_args()
    tasks = d2_tasks() if a.which == "d2" else d3_tasks()
    cost = [(10 ** t[1] * a.nsr * 1e-9, t) for t in tasks]
    cost.sort(key=lambda z: -z[0])
    bins = [[] for _ in range(a.bins)]
    load = [0.0] * a.bins
    for c, t in cost:
        i = min(range(a.bins), key=lambda k: load[k])
        bins[i].append(t)
        load[i] += c
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    nonempty = [b for b in bins if b]
    with open(a.out, "w") as f:
        for b in nonempty:
            f.write(";".join(f"{i} {lg:.2f} {c} {s}" for (i, lg, c, s) in b) + "\n")
    print(f"{len(tasks)} tasks -> {len(nonempty)} bundles; "
          f"max bundle {max(load):.0f} s, total {sum(load) / 3600:.1f} core-h")


if __name__ == "__main__":
    main()
