"""Recover completed rich-best-response cells from the Slurm logs.

Each task writes its CSV only when the whole shard finishes, but it prints one
line per completed cell as it goes. This parses those lines so that a partially
drained array still yields every cell that actually finished, at the full
horizon and the full seed count. The parsed rows are written to the aggregated
CSV directory exactly like the shard CSVs, and the aggregator prefers a shard
CSV when one exists.
"""
import glob
import os
import re
import sys

import pandas as pd

PAT = re.compile(r"^done (\S+) (\S+) (\S+) -> (\S+) rev ([0-9.]+) -> ([0-9.]+)$")


def main(logglob, out):
    rows = []
    for f in sorted(glob.glob(logglob)):
        for line in open(f):
            m = PAT.match(line.strip())
            if not m:
                continue
            tri, al, mech, prof, ns, st = m.groups()
            rows.append({"triple": tri, "alpha": al, "mech": mech, "profile": prof,
                         "nonstrategic_revenue": float(ns),
                         "strategic_revenue": float(st),
                         "degradation": float(ns) - float(st),
                         "source": os.path.basename(f)})
    df = pd.DataFrame(rows).drop_duplicates(
        subset=["triple", "alpha", "mech"], keep="last")
    df.to_csv(out, index=False)
    print(f"{len(df)} completed cells recovered from {logglob} -> {out}")
    return df


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
