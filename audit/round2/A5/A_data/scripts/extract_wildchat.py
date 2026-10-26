"""Extract user turns from one WildChat-4.8M shard (raw text stays in the workspace, never the repo).
One query = one user turn. Arrival time = timestamp of the assistant turn that answers it (user turns
carry no timestamp in this release); a user turn with no following assistant turn is dropped.
Keeps every language, flags English (turn-level `language` field), truncates text to 2,000 chars."""
import sys, os
import numpy as np, pyarrow as pa, pyarrow.parquet as pq
src, dst = sys.argv[1], sys.argv[2]
f = pq.ParquetFile(src)
cols = {k: [] for k in ["ts", "lang", "text", "turn_id", "model", "conv_hash"]}
stats = dict(conversations=0, user_turns=0, dropped_no_reply=0)
for rg in range(f.num_row_groups):
    t = f.read_row_group(rg, columns=["conversation_hash", "model", "conversation"]).to_pylist()
    for r in t:
        stats["conversations"] += 1
        conv = r["conversation"]
        for k, u in enumerate(conv):
            if u["role"] != "user":
                continue
            stats["user_turns"] += 1
            nxt = conv[k + 1] if k + 1 < len(conv) else None
            if nxt is None or nxt["role"] != "assistant" or nxt["timestamp"] is None:
                stats["dropped_no_reply"] += 1
                continue
            cols["ts"].append(int(nxt["timestamp"].timestamp()))
            cols["lang"].append(u["language"] or "")
            cols["text"].append((u["content"] or "")[:2000])
            cols["turn_id"].append(int(u["turn_identifier"]) if u["turn_identifier"] is not None else -1)
            cols["model"].append(r["model"] or "")
            cols["conv_hash"].append(r["conversation_hash"] or "")
pq.write_table(pa.table(cols), dst, compression="zstd")
print(os.path.basename(src), stats, "kept", len(cols["ts"]), "english", sum(l == "English" for l in cols["lang"]))
