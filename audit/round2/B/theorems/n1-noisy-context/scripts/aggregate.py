import glob, sys
import pandas as pd
D = "<repo>/audit/round2/B/theorems/n1-noisy-context/out"
df = pd.concat([pd.read_csv(f) for f in glob.glob(D + "/iid_*.csv") + glob.glob(D + "/bursty_*.csv")])
df.to_csv(D + "/n1_all_runs.csv", index=False)
g = df.groupby(["order", "eps", "arm"]).agg(runs=("seed", "size"), revenue=("revenue", "mean"),
                                           fired=("fired", "mean"), compliant=("compliant_convictions", lambda x: (x > 0).mean()),
                                           fallback=("fallback_frac", "mean"), bench_label=("bench_label", "mean"),
                                           bench_true=("bench_true", "mean"))
pd.set_option("display.width", 200)
print(g.round(4))
g.to_csv(D + "/n1_summary.csv")
# per-subset revenue difference label vs pointwise
p = df.pivot_table(index=["order", "eps", "subset"], columns="arm", values="revenue")
print((p.sub(p.get("plmesp:pointwise"), axis=0)).round(4))
