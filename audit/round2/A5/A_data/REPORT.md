STATUS: IN PROGRESS 2026-09-28T16:59:44Z

# Agent A (data) report

Milestones are appended below as they complete.

## Milestone 1 (28 Sep 2026): dataset choice, extraction

- **Chosen stream: WildChat-4.8M** (`allenai/WildChat-4.8M`, revision `c827c6df8fcf008219ffaffa4d1dd77491099367`),
  ODC-BY 1.0, not gated. 3,199,860 conversations, April 2023 to July 2025.
- Not used: `lmsys/lmsys-chat-1m` and `lmsys/chatbot_arena_conversations` are **gated** (auto-approval
  behind an agreement). Under the project rule the author must accept those terms personally, so they were
  not downloaded. `lmarena-ai/arena-human-preference-140k` (CC-BY-4.0) is ungated but is a preference dataset;
  it was not needed.
- **Unit and timestamp.** One query = one user turn. WildChat-4.8M stores no timestamp on user turns, only on
  assistant turns, so a user turn's arrival time is the timestamp of the assistant turn that answers it
  (typically seconds later). No user turn lacked a following assistant turn.
- Extracted 5,167,182 user turns, 2,552,378 of them English (turn-level `language` field). **English alone
  (2.55M) cannot fill a 3e6-round window**, so both an all-language stream and an English stream are
  produced; the all-language stream is classified with a multilingual embedding.
- Raw text stays in `<workspace>/raw_data/`, never the repo.

## Pre-registered labelling rubric for the 200-prompt hand check (written before any classification)

Each real prompt gets exactly one of the five fixed types, judged from the user's request alone:
- **math**: asks to solve, compute or prove something quantitative (arithmetic, algebra, word problems,
  statistics calculations).
- **code**: asks to write, fix, explain or run code, or concerns a programming language, library or query
  language.
- **knowledge_qa**: a factual or academic question with a definite answer (science, history, medicine, law,
  definitions, exam or quiz questions, including multiple choice).
- **commonsense**: everyday physical or social reasoning, or choosing the most plausible continuation of a
  situation, without specialised knowledge.
- **open_chat**: everything else: creative writing, role-play, advice, opinion, translation, summarising,
  rewriting, emails, casual conversation, and requests too vague to place.
Ties: a request that mixes types gets the type of its main deliverable (a story about maths is open_chat; a
proof requested in prose is math). The sample is 200 prompts drawn uniformly at random (seed 20260928) from
the classified all-language stream, stratified 150 English and 50 non-English. **Labeller disclosure: the
labels are assigned by the AI agent (Agent A), not by a human annotator.**

## Milestone 2 (28 Sep 2026): Open LLM Leaderboard access, and the pre-registered model selection

- The per-question `open-llm-leaderboard/<org>__<model>-details` datasets are **gated** (`gated: auto`,
  checked on `Qwen__Qwen2.5-7B-Instruct-details`). Under the project rule they were **not** downloaded; the
  author must accept the terms personally. They are needed only for the fine (~50 subcategory) table.
- `open-llm-leaderboard/contents` (revision `9c09a7cae43334062a82cb164f2ef255013dafa2`) is **ungated**,
  4,576 evaluated models, with one raw score per model on each of the six v2 benchmarks (IFEval, BBH,
  MATH Lvl 5, GPQA, MuSR, MMLU-Pro). The coarse table is built from it. No licence is stated on its card.
- Quantised variants barely exist in the table (2 of 4,576 rows are `4bit`), so substitution-as-shading uses
  **size ladders within one model generation** instead of quantisation.

**Selection rule, fixed before any capability table was computed:** `Official Providers == True`,
instruction-tuned models only, one row per model (bfloat16 if present, else float16), from four
generations that publish at least three sizes, excluding long-context (`-1M`), coder, math and
language-specific variants:
- Qwen2.5-Instruct: 0.5B, 1.5B, 3B, 7B, 14B, 32B, 72B
- Llama 3.x Instruct: 3.2-1B, 3.2-3B, 3.1-8B, 3.1-70B, 3.3-70B
- Gemma-2-it: 2B, 9B, 27B
- Mistral instruct line: Mistral-7B-Instruct-v0.3, Ministral-8B-2410, Mistral-Nemo-2407 (12B),
  Mistral-Small-2409 (22B), Mistral-Large-2411 (123B)
That is 20 models. Within a family, variants are ordered by parameter count; the smallest is the cheap
substitute whose capability defines the intrinsic level.

## Milestone 3 (28 Sep 2026): capability tables, classifier running, human-label package specified

- `experiments/data/A5/capabilities_merged5_5shot.csv` and `_0shot.csv`: RouterBench on the five merged
  types, with `type_masses_merged5_*.csv`. 5-shot query counts: knowledge_qa 15,498; commonsense 11,309;
  math 7,450; code 427; open_chat 80.
- `experiments/data/A5/leaderboard_capabilities_coarse.csv` (20 models x 6 benchmarks) and
  `leaderboard_families.csv` (4 families, variants ordered by size, the cheapest flagged). **Caveat:** `n` is
  each benchmark's documented item count (IFEval 541, BBH 5,761, MATH Lvl 5 1,324, GPQA 1,192, MuSR 756,
  MMLU-Pro 12,032), taken from the leaderboard's documentation as I recall it and not re-verified here, and
  `se` is the binomial approximation. Both columns are labelled `_approx`.
- `leaderboard_capabilities_fine.csv`: **not produced**, because the per-question details are gated.
- Classifier: RouterBench 5-fold self-check, recall per type: knowledge_qa 0.82, math 1.00, code 1.00,
  commonsense 0.85, **open_chat 0.44** (its centroid is 80 heterogeneous MT-Bench prompts, which include
  maths and coding items). The number that matters is the hand check on real traffic, below.
- Human-label package (the coordinator's request, 28 Sep), all in the workspace
  `raw_data/human_label/`, never the repo:
  `sample_200.csv` (blinded: item_id, language, is_english, full prompt text, empty prompt_en, human_label,
  unsure, note; no label of any kind), `agent_labels.csv` and `classifier_labels.csv` (separate, keyed by
  item_id), `sample_flags.csv` (WildChat turn-level toxic and redacted flags; flagged items kept), and
  `_key.csv` (item_id to shard, turn_id and timestamp).
