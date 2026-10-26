"""Cross-check: the utility CURVE and the separate DEVIATION code path must give
the same number for the same delivered mean.

The curve is produced by sweeping a `fixed<m>` option; the deviation table is
produced by an `undercut<eps>` option. They are different code paths in
`ProfileStrategy`, so agreement is a real check on both. The curve is evaluated
at the undercut's exact target by linear interpolation between grid points,
because the target need not land on the grid.
"""
import argparse
import os

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--eps", type=float, default=0.02)
    a = ap.parse_args()
    d = pd.read_csv(os.path.join(a.csv, "utility_curves.csv"))
    cc = pd.read_csv(os.path.join(a.csv, "utility_curves_crosscheck.csv"))
    cc = cc.drop_duplicates(["instance", "context", "role", "rule", "crosscheck_option"])
    rows = []
    cur = d[d.sweep == "all"]
    for k, g in cur.groupby(["instance", "context", "role", "rule"]):
        g = g.sort_values("delivered_mean")
        m = g.delivered_mean.values
        u = g.agent_utility_per_round.values
        sd = g.agent_utility_sd.values
        nse = int(g.nseeds.iloc[0])
        sel = cc[(cc.instance == k[0]) & (cc.context == k[1]) & (cc.role == k[2])
                 & (cc.rule == k[3])]
        if not len(sel):
            continue
        for opt, target in ((f"undercut{a.eps}",
                             float(g.runner_up_capability.iloc[0]) + a.eps),
                            ("full_capability", float(g.own_capability.iloc[0]))):
            row = sel[sel.crosscheck_option == opt]
            if not len(row):
                continue
            dev = float(row.agent_utility_per_round.iloc[0])
            t = float(np.clip(target, m[0], m[-1]))
            curve = float(np.interp(t, m, u))
            se = float(np.interp(t, m, sd)) / np.sqrt(nse)
            rows.append({"instance": k[0], "context": k[1], "role": k[2],
                         "rule": k[3], "option": opt, "target_delivered_mean": t,
                         "curve_interpolated": curve, "deviation_path": dev,
                         "difference": curve - dev, "standard_error": se,
                         "within_2_se": bool(abs(curve - dev) <= 2 * se + 1e-5)})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(a.csv, "utility_curves_crosscheck_summary.csv"), index=False)
    pd.set_option("display.width", 260)
    print(out.round(4).to_string(index=False))
    print()
    print("agreement within two standard errors:",
          f"{int(out.within_2_se.sum())} of {len(out)}")
    m = out[out.rule == "mesp"]
    print("MESP alone, the mechanism, max |difference|:",
          f"{float(m.difference.abs().max()):.3g} over {len(m)} cells")
    print("NOTE: the standard error is interpolated across the grid, and for the")
    print("epsilon-greedy router it understates the true seed spread, which is")
    print("bimodal because greedy exploration locks onto different arms. A direct")
    print("paired run of the two code paths at the same seeds agrees exactly; see")
    print("REPORT.md section 4.5.")


if __name__ == "__main__":
    main()
