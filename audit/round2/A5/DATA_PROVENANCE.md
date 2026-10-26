# Data provenance and licences, package A5 (WWW 2027 Tier 1 and Tier 2 data)

All checks and downloads were made on 28 September 2026 (UTC) from the login node through the
Hugging Face Hub API, unauthenticated. Raw data lives only in
`<workspace>/raw_data/`. The repository receives aggregates
only: no prompt, no response and no per-row record is committed.

## 1. WildChat-4.8M: used, real arrival traffic

- Source: `https://huggingface.co/datasets/allenai/WildChat-4.8M`, revision
  `c827c6df8fcf008219ffaffa4d1dd77491099367`, 86 parquet shards, 14 GB. Not gated.
- Licence, verbatim from the dataset card front matter: `license: odc-by`. The card's linked licence is
  the Open Data Commons Attribution License v1.0; the full text shipped with the dataset is copied to
  `audit/round2/A5/licenses/WildChat-4.8M_LICENSE.md`. Its preamble begins, verbatim:

  > The Open Data Commons Attribution License is a license agreement
  > intended to allow users to freely share, modify, and use this Database
  > subject only to the attribution requirements set out in Section 4.

- Obligation: attribution. Cite the WildChat paper (Zhao et al., arXiv:2405.01470) and name the dataset
  in the paper.
- Card statement on content, verbatim: "This version **only contains non-toxic user inputs and ChatGPT
  responses**, as flagged by the OpenAI Moderations API or Detoxify."
- Use here: arrival timestamps and a task-type label per user turn. Raw text is used only to compute
  labels and is not redistributed.

## 2. Datasets checked and NOT used

| Dataset | Status on 28 Sep 2026 | Reason |
|---|---|---|
| `allenai/WildChat-1M` | ungated, `license: odc-by` | superseded by 4.8M; 0.84M conversations is too short for 3e6-round windows |
| `lmsys/lmsys-chat-1m` | **gated (auto)**, no licence field | gated: the author must accept the terms personally |
| `lmsys/chatbot_arena_conversations` | **gated (auto)**, `license: cc` | gated, as above |
| `lmarena-ai/arena-human-preference-140k` | ungated, `license: cc-by-4.0` | preference pairs; not needed |

## 3. Open LLM Leaderboard: `contents` used; per-question details NOT downloaded

- Used: `https://huggingface.co/datasets/open-llm-leaderboard/contents`, revision
  `9c09a7cae43334062a82cb164f2ef255013dafa2`, one 1.1 MB parquet file. Not gated. **No licence is stated**
  on the card (its front matter carries only `dataset_info`). As with RouterBench in A4, that is an absence
  of a licence statement, not a grant; only aggregate derived tables are committed. The six benchmarks
  have their own licences, which should be cited if these tables appear in the paper.
- Each model row also carries its own `Hub License` (the model weights' licence), recorded per model in
  `experiments/data/A5/leaderboard_families.csv`.
- **Not downloaded:** `open-llm-leaderboard/<org>__<model>-details`, the per-question samples, which are
  **gated (auto)**, checked on `open-llm-leaderboard/Qwen__Qwen2.5-7B-Instruct-details` (82 files, 976 MB
  for that one model). They are needed only for the fine-grained (subcategory) table.

## 4. Models used for embedding

- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, revision
  `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`, `license: apache-2.0`. The classifier.
- `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`,
  `license: apache-2.0`. Downloaded and tested only; not used, being English-only.

## 5. RouterBench

Used unchanged from A4, which records its provenance and its open licence question in
`audit/round2/A4/DATA_PROVENANCE.md`. The 0-shot prompts are used only to build classifier centroids.
