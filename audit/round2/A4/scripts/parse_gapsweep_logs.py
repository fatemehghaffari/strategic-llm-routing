"""Recover completed capability-gap points from the Slurm logs.

Each array task writes its CSV only after every mechanism for its delta has
finished, so a task that has completed one mechanism has printed its numbers
but written nothing. This recovers those lines so the aggregate is never behind
the evidence.
"""
import glob
import re
import sys

import pandas as pd

PAT = re.compile(
    r"^delta=([0-9.]+) (\S+) rev ([0-9.]+) \(proposed ([0-9.]+)\) tau ([0-9.]+) "
    r"TV ([0-9.]+) prof (\S+)$")


def main(logglob, out):
    rows = []
    for f in sorted(glob.glob(logglob)):
        for line in open(f):
            m = PAT.match(line.strip())
            if not m:
                continue
            dl, mech, rev, pr, tau, tv, prof = m.groups()
            rows.append({"delta": float(dl), "mech": mech,
                         "equilibrium_revenue": float(rev),
                         "revenue_at_proposed": float(pr),
                         "announced_price_mean": float(tau),
                         "runner_up_curve_total_variation": float(tv),
                         "equilibrium_profile": prof})
    df = (pd.DataFrame(rows).drop_duplicates(subset=["delta", "mech"], keep="last")
          .sort_values(["mech", "delta"]))
    df.to_csv(out, index=False)
    print(f"{len(df)} points recovered -> {out}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
