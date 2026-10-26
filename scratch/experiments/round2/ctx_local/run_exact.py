"""Driver for the exact PL-MESP grid. One JSON per cell; the aggregator turns them into CSVs.

Usage:
  run_exact.py --family replicated_unique_top --Q 1 2 3 4 --n 2000 8000 20000 --out DIR
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from ctx_local.plmesp_exact import family, solve_instance  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True)
    ap.add_argument("--Q", type=int, nargs="+", required=True)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--skip-existing", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for n in a.n:
        for Q in a.Q:
            f = out / f"exact_{a.family}_Q{Q}_n{n}.json"
            if a.skip_existing and f.exists():
                print(f"skip {f.name}", flush=True)
                continue
            t0 = time.time()
            try:
                r = solve_instance(family(a.family, Q), n)
            except Exception as e:                       # record, do not silently drop a cell
                f.with_name(f.stem + ".FAILED.json").write_text(json.dumps({"family": a.family, "Q": Q, "n": n,
                                                                            "error": repr(e)}, indent=1))
                print(f"FAILED {a.family} Q={Q} n={n}: {e!r}", flush=True)
                continue
            r["family"] = a.family
            f.write_text(json.dumps(r, indent=1))
            tc = r["theorem"]
            print(f"{a.family} Q={Q} n={n}: exploit [{r['exploit_LB']:.2f}, {r['exploit_UB']:.2f}] "
                  f"([{r['exploit_LB_per_round']:.6f}, {r['exploit_UB_per_round']:.6f}] per round) "
                  f"vs constant {tc['constant']:.1f} ({tc['constant_per_round']:.4f}/round, "
                  f"vacuous={tc['constant_is_vacuous']}); revenue/round "
                  f"[{r['revenue_LB_per_round']:.5f}, {r['revenue_UB_per_round']:.5f}] vs M_(2) "
                  f"{r['benchmark_M2_per_round']:.5f}; truncated {r['n_truncated_profiles']}/{Q}; "
                  f"{time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
