"""Nearest-centroid task-type classifier (fixed design, plan of 28 Sep 2026).
Embedding: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 @ e8f8c211 (Apache-2.0), L2-normalised,
first 128 tokens. Centroids: mean normalised embedding of RouterBench 0-shot prompts per merged type, after
stripping benchmark boilerplate (answer-format instructions, option lines, GSM8K in-prompt examples) so the
centroid reflects content rather than template. Assignment: argmax cosine to the five centroids.
Outputs (workspace only): per-shard parquet of (ts, lang_is_en, type, cos_best, cos_margin, turn_id),
centroids.npy, and a RouterBench self-consistency check (5-fold, centroids refit per fold)."""
import ast, glob, os, re, sys
import numpy as np, pandas as pd, pyarrow.parquet as pq, torch
from sentence_transformers import SentenceTransformer
W = sys.argv[1]
REV = len(sys.argv) > 2 and sys.argv[2] == "rev"   # second worker: shards in reverse, reuse saved centroids
TYPES = ["knowledge_qa", "math", "code", "commonsense", "open_chat"]
RID, REV = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
dev = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(RID, revision=REV, device=dev)
print("device", dev, flush=True)
def emb(texts, bs=512):
    return model.encode(list(texts), batch_size=bs, normalize_embeddings=True, convert_to_numpy=True,
                        show_progress_bar=False).astype(np.float32)
BOIL = re.compile(r"^(please answer with the letter.*|print only a single choice.*|answer:.*|[A-E]\) .*)$", re.I)
def clean(p, fam):
    try:
        v = ast.literal_eval(p); p = v[0] if isinstance(v, list) and v else p
    except Exception:
        pass
    if fam == "GSM8K":
        p = p.split("Question:")[-1]
    lines = [l for l in p.splitlines() if l.strip() and not BOIL.match(l.strip())]
    return "\n".join(lines).strip()
CPATH = os.path.join(W, "raw_data/centroids_merged5.npy")
rb = pd.read_parquet(os.path.join(W, "raw_data/routerbench_0shot_prompts.parquet"))
rb["text"] = [clean(p, f) for p, f in zip(rb.prompt, rb.family)]
E = emb(rb.text) if not (REV and os.path.exists(CPATH)) else None
y = rb.type.map({t: k for k, t in enumerate(TYPES)}).values
if E is None:
    C = np.load(CPATH)
else:
    C = np.stack([E[y == k].mean(0) for k in range(5)]); C /= np.linalg.norm(C, axis=1, keepdims=True)
    if not os.path.exists(CPATH):
        np.save(CPATH, C)
    else:
        C = np.load(CPATH)   # a requeued run reuses the first run's centroids exactly
if E is None:
    E = np.zeros((0, C.shape[1]), np.float32); y = y[:0]
rng = np.random.default_rng(20260928); fold = rng.integers(0, 5, len(y)); acc = []
conf = np.zeros((5, 5), int)
for f in range(5 if len(y) else 0):
    tr, te = fold != f, fold == f
    Cf = np.stack([E[tr & (y == k)].mean(0) for k in range(5)]); Cf /= np.linalg.norm(Cf, axis=1, keepdims=True)
    pr = (E[te] @ Cf.T).argmax(1)
    for a, b in zip(y[te], pr): conf[a, b] += 1
print("routerbench 5-fold nearest-centroid confusion (rows true, cols pred):", TYPES)
print(conf); print("per-type recall", (np.diag(conf) / conf.sum(1)).round(3), flush=True)
os.makedirs(os.path.join(W, "raw_data/wildchat_classified"), exist_ok=True)
for f in sorted(glob.glob(os.path.join(W, "raw_data/wildchat_user_turns/shard_*.parquet")), reverse=REV):
    out = os.path.join(W, "raw_data/wildchat_classified", os.path.basename(f))
    if os.path.exists(out):
        continue
    tmp = out + ".tmp"
    if os.path.exists(tmp):
        continue                      # the other worker has it
    open(tmp, "w").close()
    t = pq.read_table(f, columns=["ts", "lang", "text", "turn_id"]).to_pandas()
    S = emb(t.text.values) @ C.T
    srt = np.sort(S, 1)
    pd.DataFrame({"ts": t.ts.values.astype(np.int64), "lang_is_en": (t.lang.values == "English"),
                  "type": S.argmax(1).astype(np.uint8), "cos_best": srt[:, -1], "cos_margin": srt[:, -1] - srt[:, -2],
                  "turn_id": t.turn_id.values}).to_parquet(tmp + ".pq")
    os.replace(tmp + ".pq", out); os.remove(tmp)
    print("done", os.path.basename(f), len(t), flush=True)
