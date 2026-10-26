"""Draw the pre-registered hand-check sample: 150 English + 50 non-English user turns, uniform at random
(seed 20260928), from the classified stream, and write, in the workspace only:
  human_label/sample_200.csv       blinded sheet for human annotators: item_id, language, is_english,
                                   prompt (FULL text from the original shard), prompt_en (empty: no machine
                                   translation), human_label, unsure, note (all empty). No labels of any kind.
  human_label/classifier_labels.csv item_id, classifier_type, cos_best, cos_margin
  human_label/sample_flags.csv      item_id, toxic, redacted (WildChat turn-level flags; nothing is dropped)
  human_label/_key.csv              item_id -> shard, turn_id, ts (for provenance; no text, no labels)
Agent labels are written separately to human_label/agent_labels.csv by hand."""
import glob, os, sys
import numpy as np, pandas as pd, pyarrow.parquet as pq
W = sys.argv[1]
TYPES = ["knowledge_qa", "math", "code", "commonsense", "open_chat"]
cl = pd.concat([pd.read_parquet(f).assign(shard=os.path.basename(f)) for f in
                sorted(glob.glob(os.path.join(W, "raw_data/wildchat_classified/shard_*.parquet")))])
rng = np.random.default_rng(20260928)
pick = []
for en, k in [(True, 150), (False, 50)]:
    g = cl[cl.lang_is_en == en]
    pick.append(g.iloc[rng.choice(len(g), k, replace=False)])
s = pd.concat(pick).reset_index(drop=True)
s.insert(0, "item_id", [f"wc{k:03d}" for k in range(len(s))])     # order drawn
full = {}
for sh, g in s.groupby("shard"):
    want = set(int(x) for x in g.turn_id)
    src = os.path.join(W, "raw_data/wildchat48m/data", sh.replace("shard_", "train-").replace(".parquet", "-of-00086.parquet"))
    f = pq.ParquetFile(src)
    for rg in range(f.num_row_groups):
        for r in f.read_row_group(rg, columns=["conversation"]).to_pylist():
            for u in r["conversation"]:
                if u["role"] == "user" and u["turn_identifier"] in want:
                    full[u["turn_identifier"]] = (u["content"], u["language"], bool(u["toxic"]), bool(u["redacted"]))
miss = [t for t in s.turn_id if int(t) not in full]
assert not miss, f"missing {len(miss)}"
d = os.path.join(W, "raw_data/human_label"); os.makedirs(d, exist_ok=True)
g = lambda t, k: full[int(t)][k]
pd.DataFrame({"item_id": s.item_id, "language": [g(t, 1) for t in s.turn_id], "is_english": s.lang_is_en.values,
              "prompt": [g(t, 0) for t in s.turn_id], "prompt_en": "", "human_label": "", "unsure": "", "note": ""}
             ).to_csv(os.path.join(d, "sample_200.csv"), index=False)
pd.DataFrame({"item_id": s.item_id, "classifier_type": [TYPES[k] for k in s["type"]], "cos_best": s.cos_best,
              "cos_margin": s.cos_margin}).to_csv(os.path.join(d, "classifier_labels.csv"), index=False)
pd.DataFrame({"item_id": s.item_id, "toxic": [g(t, 2) for t in s.turn_id], "redacted": [g(t, 3) for t in s.turn_id]}
             ).to_csv(os.path.join(d, "sample_flags.csv"), index=False)
s[["item_id", "shard", "turn_id", "ts"]].to_csv(os.path.join(d, "_key.csv"), index=False)
print(len(s), int(s.lang_is_en.sum()), "flags toxic", sum(g(t, 2) for t in s.turn_id), "redacted", sum(g(t, 3) for t in s.turn_id))
