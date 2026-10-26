"""Build the real arrival sequences from the classified WildChat turns.
Outputs (workspace, not the repo): real_sequences/wildchat48m_all.npz and wildchat48m_en.npz with
  type      uint8, index into TYPES (fixed order)
  timestamp int64, UTC seconds (timestamp of the assistant reply)
sorted by (timestamp, turn_id) for a deterministic order within a second.
Repo: experiments/data/A5/real_traffic_mix_hourly.csv (counts and shares per UTC hour, both streams) and
real_sequences_summary.csv."""
import glob, os, sys
import numpy as np, pandas as pd
W, OUT = sys.argv[1], sys.argv[2]
TYPES = ["knowledge_qa", "math", "code", "commonsense", "open_chat"]
d = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(W, "raw_data/wildchat_classified/shard_*.parquet")))])
d = d.sort_values(["ts", "turn_id"], kind="stable").reset_index(drop=True)
os.makedirs(os.path.join(W, "real_sequences"), exist_ok=True)
summ, hourly = [], []
for name, g in [("all", d), ("en", d[d.lang_is_en])]:
    np.savez_compressed(os.path.join(W, "real_sequences", f"wildchat48m_{name}.npz"),
                        type=g["type"].values.astype(np.uint8), timestamp=g["ts"].values.astype(np.int64),
                        types=np.array(TYPES))
    cnt = np.bincount(g["type"].values, minlength=5)
    summ.append(dict(stream=name, length=len(g), t_first_utc=pd.to_datetime(g.ts.min(), unit="s"),
                     t_last_utc=pd.to_datetime(g.ts.max(), unit="s"),
                     **{f"mass_{t}": c / len(g) for t, c in zip(TYPES, cnt)}))
    h = pd.crosstab(g.ts // 3600, g["type"]).reindex(columns=range(5), fill_value=0)
    h.columns = TYPES
    h["total"] = h.sum(1)
    for t in TYPES:
        h[f"share_{t}"] = h[t] / h["total"]
    h.index = pd.to_datetime(h.index * 3600, unit="s")
    h.index.name = "hour_utc"
    h.insert(0, "stream", name)
    hourly.append(h.reset_index())
pd.DataFrame(summ).to_csv(os.path.join(OUT, "real_sequences_summary.csv"), index=False)
pd.concat(hourly).to_csv(os.path.join(OUT, "real_traffic_mix_hourly.csv"), index=False)
print(pd.DataFrame(summ).to_string())
