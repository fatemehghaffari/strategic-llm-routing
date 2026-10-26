"""Build one dataset's provider bank: train the four providers, store their predictions, measure the curves.

Run under Slurm (the login node is for downloads and quick checks only):

    python -m provider_bank.build --dataset fashion_mnist --data-root <scratchpad>/round2/A/data \\
        --out <scratchpad>/round2/A/runs/pilot/provider_bank/bank --jobs 8

Outputs, per dataset, under <out>/<dataset>/: models/*.joblib (the frozen providers), preds_i.npy (per-tree or
per-stage predictions on the held-out pool), labels.npy, ctx_bins.npy, ctx_conf.npy, meas_idx.npy,
play_idx.npy, curves.npz, curves.csv (the full unsmoothed curves) and meta.json (training sizes, timings and
all seeds). The curves are measured on the measurement half only.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np

from . import bank as B
from . import datasets as D
from . import providers as P


def build(dataset: str, data_root: Path, out: Path, jobs: int = 8, n_subsets: int = B.N_SUBSETS,
          curve_seed: int = 20260920) -> B.ResponseBank:
    t_start = time.time()
    Xtr, ytr, Xpool, ypool = D.load(dataset, data_root)
    classes = np.unique(ypool)
    assert np.array_equal(classes, np.unique(ytr)), "pool and training population have different class sets"
    meas, play = D.half_split(Xpool.shape[0])
    out_d = Path(out) / dataset
    (out_d / "models").mkdir(parents=True, exist_ok=True)
    import joblib

    preds, kinds, conf_cols, info = [], [], [], []
    for spec in P.SPECS:
        model, idx, fit_s = P.train(spec, Xtr, ytr, jobs)
        joblib.dump(model, out_d / "models" / f"{spec.name}.joblib", compress=1)
        t0 = time.time()
        Pmat, ctx, conf = P.prediction_bank(spec, model, Xpool, classes)
        agree = P.check_full_knob_equals_model(spec, model, Pmat, Xpool, classes)
        counts = [int(np.count_nonzero(ytr[idx] == c)) for c in classes]
        acc_full = float(np.mean(Pmat[B.N_TREES - 1] == P._encode(ypool, classes)))
        info.append({"name": spec.name, "family": spec.family, "kind": spec.kind, "frac": spec.frac,
                     "skew": spec.skew, "random_state": spec.random_state, "n_train": int(idx.size),
                     "train_class_counts": counts,
                     "fit_seconds": round(fit_s, 1), "predict_seconds": round(time.time() - t0, 1),
                     "full_knob_agreement_with_model_predict": round(agree, 6),
                     "accuracy_of_last_row_on_pool": round(acc_full, 6)})
        preds.append(Pmat)
        kinds.append(spec.kind)
        conf_cols.append(conf.astype(np.float32))
        print(f"[{dataset}] {spec.name}: n_train={idx.size} fit={fit_s:.1f}s agree={agree:.4f}", flush=True)

    ctx_bins = np.stack([B.vote_context_bins(p, len(classes), B.CHEAP_PASS) if k == "vote"
                         else B.prob_context_bins(c) for p, k, c in zip(preds, kinds, conf_cols)], axis=1)
    labels = P._encode(ypool, classes)
    meta = {"dataset": dataset, "providers": info, "classes": [int(c) for c in classes],
            "n_train_population": int(Xtr.shape[0]), "n_pool": int(Xpool.shape[0]),
            "n_measurement": int(meas.size), "n_play": int(play.size),
            "pool_seed": D.POOL_SEED, "split_seed": D.SPLIT_SEED, "curve_seed": curve_seed,
            "n_subsets": n_subsets, "cheap_pass": B.CHEAP_PASS, "n_bins": B.N_BINS,
            "evidence": "real labeled tasks and real provider answers; the effort choice is scripted"}
    bk = B.ResponseBank(dataset, preds, labels, ctx_bins, meas, play, kinds, menu=B.MENU,
                        n_classes=len(classes), meta=meta)
    t0 = time.time()
    bk.set_curves(B.measure_curves(bk, n_subsets=n_subsets, rng=np.random.default_rng(curve_seed)))
    meta["curve_seconds"] = round(time.time() - t0, 1)
    meta["build_seconds"] = round(time.time() - t_start, 1)
    bk.meta = meta
    bk.save(Path(out))
    np.save(out_d / "ctx_conf.npy", np.stack(conf_cols, axis=1))
    write_curves_csv(bk, out_d / "curves.csv")
    print(f"[{dataset}] built in {meta['build_seconds']:.0f}s; curves in {meta['curve_seconds']:.0f}s", flush=True)
    return bk


def write_curves_csv(bk: B.ResponseBank, path: Path):
    """The full unsmoothed curves, pooled and per context cell. Nothing is smoothed or interpolated."""
    c = bk.curves()
    names = [p["name"] for p in bk.meta.get("providers", [])] or [str(i) for i in range(bk.K)]
    with Path(path).open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "provider", "provider_name", "kind", "scope", "cell", "n_tasks", "knob",
                    "A", "se", "delta_from_previous_knob", "delta_se"])
        for i in range(bk.K):
            for j, k in enumerate(bk.menu):
                w.writerow([bk.dataset, i, names[i], bk.kinds[i], "pooled", -1, int(c.n_cell[i].sum()), k,
                            f"{c.A_pooled[i, j]:.6f}", f"{c.se_pooled[i, j]:.6f}",
                            "" if j == 0 else f"{c.d_pooled[i, j - 1]:.6f}",
                            "" if j == 0 else f"{c.d_se_pooled[i, j - 1]:.6f}"])
            for cell in range(B.N_BINS):
                if c.n_cell[i, cell] == 0:
                    continue
                for j, k in enumerate(bk.menu):
                    w.writerow([bk.dataset, i, names[i], bk.kinds[i], "cell", cell, int(c.n_cell[i, cell]), k,
                                f"{c.A_cell[i, cell, j]:.6f}", f"{c.se_cell[i, cell, j]:.6f}",
                                "" if j == 0 else f"{c.d_cell[i, cell, j - 1]:.6f}",
                                "" if j == 0 else f"{c.d_se_cell[i, cell, j - 1]:.6f}"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["fashion_mnist", "covertype"])
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--subsets", type=int, default=B.N_SUBSETS)
    a = ap.parse_args()
    bk = build(a.dataset, Path(a.data_root), Path(a.out), a.jobs, a.subsets)
    c = bk.curves()
    print(json.dumps({"dataset": a.dataset, "mu_pooled": [round(float(x), 5) for x in c.mu_pooled],
                      "M_pooled": [round(float(x), 5) for x in c.M_pooled]}, indent=1))


if __name__ == "__main__":
    main()
