"""CG-MESP at parameters satisfying the structural condition, and at its own horizon-tuned parameters.

Two regimes are run, and the report must never mix them.

  STRUCTURAL. The grid side h and the bidding block L are set by hand and the shading is
  sigma = 3 s + rho with rho = alpha L sqrt(D) h. The lemmas of EXPLORER.md Section 5 and of PROVER2.md
  Sections 3 to 5 hold for ANY (h, L) with alpha >= 1, because the oscillation allowance only has to dominate
  the within-cube oscillation of an L-Lipschitz capacity, which is at most L sqrt(D) h. Running here tests the
  INEQUALITIES and says nothing about the rates. This is the regime PROVER2.md Section 11 and the explorer's
  `tight.py` used, and this module follows their construction; the instances, the deviations, the alpha sweep
  and the part (B) and (C) checks below are this package's additions.

  TUNED. The mechanism's own h_n = 1/ceil(n^{1/(D+3)}), L_n = ceil(n^{2/(D+3)}) and
  rho_n = sqrt(D) h_n log(en). At every horizon anyone can run, sigma_n >= 1, the announced price is clipped
  to zero at every cube, and the mechanism degenerates. This is measured rather than avoided.

Evidence category: SYNTHETIC SIMULATION. The deviation values are LOWER bounds on exploitability for the
deviations tried; no upper bound and no equilibrium claim is made anywhere in this module.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

# Instances: per-agent scalar contexts (d = 1), so D = K. Capacity and intrinsic maps are L-Lipschitz.
INST = {
    # uniquely top agent 0 at every context, near-tied runner-up: the e_bid term is visible
    "C": dict(K=2, M=[lambda x: 0.94 + 0.01 * x, lambda x: 0.80 - 0.02 * x],
              mu=[lambda x: 0.10 + 0.0 * x, lambda x: 0.30 + 0.0 * x], honest=[1], L=0.02),
    # three agents, agent 1 honest, capacities crossing
    "D": dict(K=3, M=[lambda x: 0.94 + 0.01 * x, lambda x: 0.80 - 0.02 * x, lambda x: 0.78 + 0.01 * x],
              mu=[lambda x: 0.10 + 0.0 * x, lambda x: 0.30 + 0.0 * x, lambda x: 0.20 + 0.0 * x],
              honest=[1], L=0.02),
    # genuinely oscillating capacities at the full Lipschitz rate, which is the case the allowance pays for
    "E": dict(K=2, M=[lambda x: 0.70 + 0.20 * x, lambda x: 0.90 - 0.20 * x],
              mu=[lambda x: 0.10 + 0.0 * x, lambda x: 0.25 + 0.0 * x], honest=[1], L=0.20),
    # honest agent is the top agent, so the honest benchmark is high and part (C) can bind
    "F": dict(K=3, M=[lambda x: 0.90 - 0.05 * x, lambda x: 0.70 + 0.02 * x, lambda x: 0.68 + 0.02 * x],
              mu=[lambda x: 0.80 - 0.05 * x, lambda x: 0.10 + 0.0 * x, lambda x: 0.10 + 0.0 * x],
              honest=[0], L=0.05),
}

GRIDPTS = 21          # contexts per axis used for the pointwise lemma checks inside a cube


def run(name, n, g, Lbid, dev=None, kind=None, alpha_ride=0.5, seed=0, ctx="iid",
        osc_mult=3.0, tuned=False, joint=False):
    """One CG-MESP episode. `osc_mult` is the multiplier in rho = osc_mult * L sqrt(D) h (structural regime);
    `tuned` instead uses the mechanism's own h_n, L_n and rho_n at this n."""
    I = INST[name]
    K, M, mu, honest, Llip = I["K"], I["M"], I["mu"], set(I["honest"]), I["L"]
    D = K
    if tuned:
        g = math.ceil(n ** (1.0 / (D + 3)))
        Lbid = math.ceil(n ** (2.0 / (D + 3)))
    h = 1.0 / g
    ell = math.log(2 * K) + 5 * math.log(n)
    s = math.sqrt(ell / (2 * Lbid))
    rho = (math.sqrt(D) * h * math.log(math.e * n)) if tuned else (osc_mult * Llip * math.sqrt(D) * h)
    sig = 3 * s + rho

    def bnd(r):
        return math.sqrt(r * ell / 2.0) if r > 0 else 0.0

    rng = np.random.default_rng(seed)
    Xs = (rng.random((n, K)) if ctx == "iid"
          else np.array([[(t * (0.6180339887 * (j + 1))) % 1.0 for j in range(K)] for t in range(n)]))
    U = rng.random(n)
    cells = {}
    util = np.zeros(K)
    rev = 0.0
    bench2 = 0.0
    benchb = 0.0
    sw = 0
    false_sw = 0
    viol_P2 = 0
    viol_P4 = 0
    awarded = 0
    taus = []
    stage1 = 0
    devs = {dev} if (dev is not None and not joint) else (set(range(K)) - honest if joint else set())
    for t in range(n):
        X = Xs[t]
        key = tuple(min(g - 1, int(x / h)) for x in X)
        if key not in cells:
            cells[key] = dict(V=0, sm=np.zeros(K), ph=1, tau=None, W=None, r=0, Z=0.0, minm=math.inf,
                              prio=rng.permutation(K), fb=0, w=np.ones(K), ep=-1)
        c = cells[key]
        c["V"] += 1
        Mv = np.array([M[j](X[j]) for j in range(K)])
        mv = np.array([mu[j](X[j]) for j in range(K)])
        bench2 += float(np.sort(Mv)[-2])
        benchb += float(max(mv[j] for j in honest))
        if c["ph"] == 1:
            i = (c["V"] - 1) % K
            m = Mv[i]
            if i in devs and kind in ("underbid", "both", "sabotage"):
                if kind == "sabotage":
                    m = mv[i] if i in honest else 0.0
                else:
                    alt = float(np.max(np.delete(Mv, i)))
                    m = min(Mv[i], max(0.5 * (Mv[i] + alt), mv[i] if i in honest else 0.0))
            y = 1.0 if U[t] <= m else 0.0
            c["sm"][i] += y
            rev += y
            util[i] += 1 + mv[i] - m
            stage1 += 1
            if c["V"] == K * Lbid:
                beta = c["sm"] / Lbid
                W = sorted(range(K), key=lambda j: (beta[j], c["prio"][j]))[-1]
                tau = max(0.0, float(np.sort(beta)[-2]) - sig)
                c["W"], c["tau"], c["ph"] = W, tau, 2
                taus.append(tau)
                awarded += 1
                # Lemma P2 / explorer Lemma 5: the winner can meet the price at EVERY context of its cube
                gr = np.linspace(key[W] * h, key[W] * h + h, GRIDPTS)
                if tau > min(M[W](v) for v in gr) + 1e-12:
                    viol_P2 += 1
                # Lemma P4 / explorer Lemma 8: the price is not far below the second capacity, at S^*
                if dev is None and not joint:
                    worst = -math.inf
                    for a in range(GRIDPTS):
                        vals = sorted(M[j](key[j] * h + h * a / (GRIDPTS - 1)) for j in range(K))
                        worst = max(worst, vals[-2])
                    if tau < worst - 4 * s - (4.0 / 3.0) * rho - 1e-12:
                        viol_P4 += 1
            continue
        if c["ph"] == 2:
            W, tau = c["W"], c["tau"]
            m = min(tau, Mv[W])
            if W in honest:
                m = max(mv[W], m)
            if W in devs and kind in ("rider", "both"):
                inc = bnd(c["r"] + 1) - bnd(c["r"])
                m = min(max(0.0, tau - alpha_ride * inc), Mv[W])
                if W in honest:
                    m = max(m, mv[W])
            elif W in devs and kind in ("crash", "sabotage"):
                m = mv[W] if W in honest else 0.0
            c["minm"] = min(c["minm"], m)
            y = 1.0 if U[t] <= m else 0.0
            c["r"] += 1
            c["Z"] += y
            rev += y
            util[W] += 1 + mv[W] - m
            if c["Z"] < c["r"] * tau - bnd(c["r"]):
                c["ph"] = 3
                c["fb"] = 0
                sw += 1
                if c["minm"] >= tau - 1e-12:
                    false_sw += 1
            continue
        c["fb"] += 1
        sd = c["fb"]
        k = int(math.floor(math.log2(sd)))
        if 2 ** k == sd:
            c["w"] = np.ones(K)
            c["ep"] = k
        gam = min(0.5, math.sqrt(K * math.log(K) / 2 ** c["ep"]))
        eta = gam / K
        q = c["w"] / c["w"].sum()
        p = (1 - gam) * q + gam / K
        Ia = int(rng.choice(K, p=p))
        m = (mv[Ia] if Ia in honest else 0.0) if (Ia in devs and kind in ("sabotage",)) else Mv[Ia]
        y = 1.0 if U[t] <= m else 0.0
        yh = np.zeros(K)
        yh[Ia] = y / p[Ia]
        c["w"] *= np.exp(eta * yh)
        c["w"] /= c["w"].max()
        rev += y
        util[Ia] += 1 + mv[Ia] - m
    Jp = len(cells)
    e_bid = min(Jp * Lbid, n)
    e_stage1 = min(K * Jp * Lbid, n)
    e_osc = n * rho
    e_mon = Jp + 2 * math.sqrt(Jp * n * ell / 2)
    e_fb = 11 * math.sqrt(2 * K * Jp * n * math.log(K)) + 2 * K * math.log(K) * Jp * math.log2(2 * (n + 1))
    e_price = n * (4 * s + (4.0 / 3.0) * rho)
    e_rob = n * (4 * s + (5.0 / 3.0) * rho)
    return dict(inst=name, n=n, K=K, D=D, g=g, L=Lbid, J=Jp, h=h, s=s, rho=rho, sigma=sig,
                osc_mult=(None if tuned else osc_mult), tuned=int(tuned),
                u0=float(util[0]), util=[float(x) for x in util], rev=rev, stage1=stage1,
                awarded=awarded, switches=sw, false_switches=false_sw,
                viol_P2=viol_P2, viol_P4=viol_P4,
                mean_tau=float(np.mean(taus)) if taus else 0.0,
                zero_price_share=float(np.mean([tt <= 0 for tt in taus])) if taus else float("nan"),
                bench_M2=bench2, bench_honest=benchb,
                boundA=e_bid + e_osc + e_mon + e_fb, slackB=e_stage1 + e_price,
                slackC=e_stage1 + e_rob + e_mon + e_fb,
                e_bid=e_bid, e_stage1=e_stage1, e_osc=e_osc, e_mon=e_mon, e_fb=e_fb)


def structural_block(name, n, g, Lbid, seeds=6, osc_mult=3.0):
    specs = [("proposed", None, 0.0), ("underbid", "underbid", 0.0), ("rider25", "rider", 0.25),
             ("rider50", "rider", 0.5), ("rider100", "rider", 1.0), ("both", "both", 0.5),
             ("crash", "crash", 0.0)]
    vals, base = {}, None
    for tag, kind, al in specs:
        us = []
        for sd in range(seeds):
            r = run(name, n, g, Lbid, dev=(None if kind is None else 0), kind=kind, alpha_ride=al,
                    seed=sd, osc_mult=osc_mult)
            us.append(r["u0"])
            if kind is None and sd == 0:
                base = r
        vals[tag] = float(np.mean(us))
    # part (C): every strategic agent sabotages
    revs, benchs = [], []
    for sd in range(seeds):
        r = run(name, n, g, Lbid, dev=0, kind="sabotage", seed=sd, osc_mult=osc_mult, joint=True)
        revs.append(r["rev"])
        benchs.append(r["bench_honest"])
    out = dict(base)
    out["deviation_gain"] = {k: round(vals[k] - vals["proposed"], 2) for k in vals}
    out["best_searched_gain"] = max(vals[k] - vals["proposed"] for k in vals)
    out["A_holds"] = int(out["best_searched_gain"] <= out["boundA"])
    out["revenue_deficit_B"] = out["bench_M2"] - out["rev"]
    out["B_holds"] = int(out["revenue_deficit_B"] <= out["slackB"])
    out["joint_sabotage_revenue"] = float(np.mean(revs))
    out["joint_sabotage_benchmark"] = float(np.mean(benchs))
    out["honest_deficit_C"] = float(np.mean(benchs) - np.mean(revs))
    out["C_holds"] = int(out["honest_deficit_C"] <= out["slackC"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, default=6)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    print("=== STRUCTURAL regime: the lemmas and the three inequalities, at sigma = 3 s + 3 L sqrt(D) h ===")
    for name, n, g, Lb in (("C", 200000, 3, 4000), ("C", 400000, 3, 8000), ("D", 200000, 3, 2500),
                           ("E", 200000, 3, 4000), ("E", 400000, 4, 5000), ("F", 200000, 3, 2500)):
        r = structural_block(name, n, g, Lb, seeds=a.seeds)
        rows.append(r)
        print(json.dumps({k: r[k] for k in ("inst", "n", "K", "g", "L", "J", "mean_tau", "viol_P2", "viol_P4",
                                            "awarded", "switches", "false_switches", "best_searched_gain",
                                            "boundA", "A_holds", "revenue_deficit_B", "slackB", "B_holds",
                                            "honest_deficit_C", "slackC", "C_holds", "deviation_gain")}),
              flush=True)
    print("\n=== Necessity of the oscillation allowance: Lemma P2 violations against the multiplier ===")
    osc_rows = []
    for name, n, g, Lb in (("E", 200000, 3, 4000), ("E", 200000, 6, 2000)):
        for mult in (0.0, 0.25, 0.5, 1.0, 2.0, 3.0):
            v2 = v4 = aw = 0
            for sd in range(a.seeds):
                r = run(name, n, g, Lb, seed=sd, osc_mult=mult)
                v2 += r["viol_P2"]
                v4 += r["viol_P4"]
                aw += r["awarded"]
            osc_rows.append({"inst": name, "n": n, "g": g, "L": Lb, "osc_mult": mult,
                             "awarded_cubes": aw, "viol_P2": v2, "viol_P4": v4,
                             "P2_violation_rate": v2 / max(aw, 1), "P4_violation_rate": v4 / max(aw, 1)})
            print(json.dumps(osc_rows[-1]), flush=True)
    print("\n=== TUNED regime: the mechanism at its own parameters, at runnable horizons ===")
    tuned_rows = []
    for name in ("C", "D", "E"):
        for n in (20000, 200000, 2000000):
            r = run(name, n, 0, 0, seed=0, tuned=True)
            tuned_rows.append({k: r[k] for k in ("inst", "n", "K", "D", "g", "L", "J", "h", "s", "rho", "sigma",
                                                 "mean_tau", "zero_price_share", "awarded", "switches",
                                                 "rev", "bench_M2", "bench_honest", "stage1", "boundA",
                                                 "slackB", "slackC")})
            tuned_rows[-1]["revenue_per_round"] = r["rev"] / n
            tuned_rows[-1]["bench_M2_per_round"] = r["bench_M2"] / n
            tuned_rows[-1]["stage1_share"] = r["stage1"] / n
            print(json.dumps(tuned_rows[-1]), flush=True)
    (out / "cg_structural.json").write_text(json.dumps(rows, indent=1))
    (out / "cg_oscillation.json").write_text(json.dumps(osc_rows, indent=1))
    (out / "cg_tuned.json").write_text(json.dumps(tuned_rows, indent=1))
    print(f"\nwrote {out}/cg_structural.json, cg_oscillation.json, cg_tuned.json")


if __name__ == "__main__":
    main()
