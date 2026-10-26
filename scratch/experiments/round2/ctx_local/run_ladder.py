"""Contextual ablation ladder: 8 mechanism rungs x behaviour profiles x instances x horizons, paired.

Seeds: common/seeds.py, suite 'contextual_incentives', phase 'final' (or 'pilot'), so no seed used here
appears in the scalar package's tables. Every rung and behaviour of a replicate shares the same tapes.
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import numpy as np

R2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R2))

from common import seeds as S  # noqa: E402
from ctx_local.plmesp_exact import family  # noqa: E402
from ctx_local import ctxmech as CM  # noqa: E402

FIELDS = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True)
    ap.add_argument("--Q", type=int, nargs="+", required=True)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--phase", default="final")
    ap.add_argument("--rungs", nargs="+", default=list(CM.CTX_VARIANTS))
    ap.add_argument("--behaviors", nargs="+", default=CM.CTX_BEHAVIORS)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fam_index = {f: k for k, f in enumerate(sorted({a.family}))}
    for n in a.n:
        for Q in a.Q:
            ctx = family(a.family, Q)
            path = out / f"ladder_{a.family}_Q{Q}_n{n}_{a.phase}.csv"
            if path.exists():
                print(f"skip {path.name}", flush=True)
                continue
            rows = []
            t0 = time.time()
            inst_index = 1000 * (fam_index[a.family] + 1) + Q
            for rep in range(a.reps):
                key, seed, gens_master = S.trial_streams("contextual_incentives", a.phase, inst_index, n, rep)
                for rung in a.rungs:
                    for beh in a.behaviors:
                        # one fresh generator set per replicate, identical across rungs and behaviours
                        _, _, gens = S.trial_streams("contextual_incentives", a.phase, inst_index, n, rep)
                        r = CM.run_episode(ctx, n, rung, beh, ctx.focal, gens)
                        r["rep"] = rep
                        r["seed_key"] = key
                        r["family"] = a.family
                        rows.append(r)
                if rep == 0:
                    print(f"  {a.family} Q={Q} n={n}: first replicate {time.time() - t0:.1f}s "
                          f"({len(rows)} cells)", flush=True)
            fields = list(rows[0].keys())
            with path.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                for r in rows:
                    w.writerow(r)
            print(f"{path.name}: {len(rows)} rows, {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
