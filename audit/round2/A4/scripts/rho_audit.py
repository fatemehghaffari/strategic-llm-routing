"""How large is the continuum mechanism's oscillation allowance at a reachable
horizon, and at what horizon does the announced price stop being identically zero?

Pure arithmetic on the paper's own constants plus the MEASURED within-cell
oscillation of the capability surface.  No simulation.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instances as I  # noqa: E402
from rb_common import OUT  # noqa: E402
from select_triples import flip_rate_table, pick  # noqa: E402

Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]


def main():
    tri = pick(flip_rate_table(Q7))["midflip"].split("|")
    rows = []
    for n in (3 * 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 9, 10 ** 12, 10 ** 15):
        for d in (1, 2):
            inst, gm, a, rho, meta = I.continuous_instance(tri, "a0.50", n, d=d, k=200,
                                                           rho_mode="paper")
            L = I.cg_elicitation_length(n, d, inst.K)
            s = float(np.sqrt((np.log(2.0 * inst.K) + 4.0 * np.log(float(n))) / (2 * L)))
            rows.append({"n": n, "d": d, "b": meta["b"], "h_n": meta["h"],
                         "n_cells_populated": meta["n_cells"], "L_n_cg": L, "s_n": s,
                         "rho_paper": meta["rho_paper"],
                         "rho_measured_p95_within_cell": meta["rho_measured_p95"],
                         "total_price_shading_3s_plus_rho": 3 * s + meta["rho_paper"],
                         "elicitation_fraction": inst.K * meta["n_cells"] * L / n})
            print(rows[-1], flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rho_audit.csv"), index=False)


if __name__ == "__main__":
    main()
