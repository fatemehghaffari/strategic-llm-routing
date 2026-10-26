# Data provenance and licence, package A4 (RouterBench calibrated simulation)

All checks and all downloads below were performed on **24 September 2026 (UTC)** from the
the cluster login node with `curl`. Nothing else was downloaded and nothing was substituted.

## 1. THE LICENCE QUESTION, WHICH IS NOT CLOSED

Read this section before any number in `REPORT.md` is used.

**The code is MIT. The data carries no licence statement that I could find anywhere.**

### 1a. Code: MIT, explicit

- Repository: `https://github.com/withmartian/routerbench`, default branch `main`.
- Head commit at the time of checking: `cc67d1008bd8f3cf1e8040cc3ba4034d31b93c0c`,
  authored 2024-06-13T05:12:08Z, message
  `Merge pull request #9 from withmartian/jason/add-license` / `feat: add license`.
- GitHub's licence API reports `{"key": "mit", "spdx_id": "MIT"}` for the repository.
- Verbatim, the first lines of `https://raw.githubusercontent.com/withmartian/routerbench/main/LICENSE`:

  > MIT License
  >
  > Copyright (c) LangChain, Inc.
  >
  > Permission is hereby granted, free of charge, to any person obtaining a copy
  > of this software and associated documentation files (the "Software"), to deal
  > in the Software without restriction, including without limitation the rights
  > to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  > copies of the Software, and to permit persons to whom the Software is
  > furnished to do so, subject to the following conditions:

  (The copyright holder is stated as LangChain, Inc., not Martian. That is what the file says.)

MIT permits research use and redistribution, including of derived work. For the code the
question is closed.

### 1b. Data: NO licence found, which is an absence of permission, not a grant

The per-query outcomes are published on Hugging Face, not in the GitHub repository:
`https://huggingface.co/datasets/withmartian/routerbench`.

What I checked, and what I found:

| check | result |
|---|---|
| `GET /api/datasets/withmartian/routerbench?full=true`, field `cardData` | no `license` key. The card declares only `task_categories`, `language`, `tags`, `pretty_name`, `size_categories`. |
| repository file tree (`/api/datasets/.../tree/main`) | five files only: `.gitattributes`, `README.md`, `routerbench_0shot.pkl`, `routerbench_5shot.pkl`, `routerbench_raw.pkl`. **No LICENSE file.** |
| repository refs (`/api/datasets/.../refs`) | one branch `main`, no tags, single commit `784021482c3f320c6619ed4b3bb3b41a21424fcb` (2024-03-27T07:27:17Z). No other revision to check. |
| rendered dataset page HTML | the string `licen` does not occur anywhere in it. |
| dataset `README.md` (1027 bytes, fetched at the pinned revision) | no licence statement. It does say the datasets "are designed to be used with Martian's routerbench package". |
| the paper, arXiv:2403.12031v2 | the only licence statement in it is arXiv's own: "License: arXiv.org perpetual non-exclusive license". That governs the paper, not the data. The paper states: "The code and data are available at https://github.com/withmartian/routerbench." |
| arXiv abstract page | licence link `http://arxiv.org/licenses/nonexclusive-distrib/1.0/`, the arXiv default, again about the paper. |

**The honest reading.** There is no licence on the data. The strongest thing that can be said
in favour of use is indirect: the paper says "the code and data are available at" a repository
that carries an MIT licence, the authors published the data publicly and un-gated with an
explicit invitation to use it, and it has been downloaded 1,568 times per the HF API. The
strongest thing against is direct: no grant of rights was made for the data, and "publicly
downloadable" is not a licence.

**What I did, and what needs the author's decision.** I proceeded, because the data is the
authors' own publication of derived evaluation outcomes, offered for exactly this kind of
reuse, and because the only thing this package redistributes is AGGREGATE DERIVED STATISTICS:
per-model per-benchmark mean scores (77 numbers), local averages over embeddings, and
simulation outputs. **No prompt, no model response, and no per-query row is committed
anywhere in this repository.** That is a defensible position but it is a judgement call, not a
licence, and it is the author's to ratify or reject.

- **If the author judges the absence of a licence to be disqualifying, everything in
  `audit/round2/A4/` and `experiments/data/A4/` must be withdrawn from the paper.** I have
  kept the package self-contained so that withdrawing it costs nothing else.
- Two mitigations worth considering either way: (i) write to `jason@withmartian.com`, the
  correspondence address in the paper, and ask for an explicit licence; (ii) cite the dataset
  by its DOI `10.57967/hf/1996` and state in the paper that only aggregate statistics are used.
- Separate matter: the underlying benchmarks (MMLU, HellaSwag, GSM8K, ARC, Winogrande, MBPP,
  MT-Bench) carry their own licences. This package does not touch them: it never redistributes
  their prompts or labels, only per-model accuracy averages computed from RouterBench's
  published score columns.

## 2. What was downloaded

Pinned revision used for both files: `784021482c3f320c6619ed4b3bb3b41a21424fcb`
(the only commit on `main`).

    https://huggingface.co/datasets/withmartian/routerbench/resolve/784021482c3f320c6619ed4b3bb3b41a21424fcb/routerbench_0shot.pkl
    https://huggingface.co/datasets/withmartian/routerbench/resolve/784021482c3f320c6619ed4b3bb3b41a21424fcb/routerbench_5shot.pkl

| file | bytes | sha256 |
|---|---|---|
| `routerbench_0shot.pkl` | 99,567,659 | `ba4f77f19517610a707c374e99322d7750c30fc4ae7ff5527888595a1e65d36d` |
| `routerbench_5shot.pkl` | 171,091,324 | `fbd7d3d16fba2759a18fa0ad44409d3e0e92ba80d03d90827eed1a6d084c9ffe` |

`routerbench_raw.pkl` (1,198,134,681 bytes) was NOT downloaded; nothing here needs it.
Download start 2026-09-24T15:33:25Z, end 2026-09-24T15:33:32Z.
Files live at `<scratchpad>/llm/data/` and are never copied into any git tree.

**Safety note.** The published artefacts are Python pickles, which execute arbitrary code on
load. They are loaded through `scripts/safe_load.py`, a restricted unpickler that refuses every
global outside `numpy`, `pandas`, `collections`, `builtins`, `copyreg`, `_codecs` and that
denies `eval`, `exec`, `compile`, `open`, `__import__` and `getattr` by name. Both files load
cleanly under that restriction, so nothing outside those modules was instantiated.

## 3. Row counts, exactly

Both files are pandas DataFrames with 37 columns: `sample_id`, `prompt`, `eval_name`, one
performance-score column per model, one `|model_response` column per model, one `|total_cost`
column per model, and `oracle_model_to_route_to`. Eleven models.

| | 0-shot | 5-shot |
|---|---|---|
| rows as published | 36,497 | 36,511 |
| after dropping duplicate `sample_id` | 36,497 | 36,497 |
| after dropping rows with any missing model score | 36,497 | 36,483 |
| rows whose `eval_name` is outside the seven families the paper's Table 1 reports | 1,719 | 1,719 |
| **rows used** | **34,778** | **34,764** |
| **per-model-per-query outcomes used** | **382,558** | **382,404** |

The paper states "In total, there are 405,467 samples in RouterBench, covering 11 models, 8
datasets, and 64 tasks." 36,497 x 11 = 401,467 for the published 0-shot table; the difference
is the RAG subset, which uses three additional models (You.com, sonar-small-online,
sonar-medium-online) that have no column in these two files. This package uses only the eleven
models that are columns in the published tables.

The 1,719 excluded rows are 21 `eval_name` values that do not belong to any of the seven
families of Table 1: `abstract2title`, `accounting_audit`, `bias_detection`,
`consensus_summary`, `test-match`, `Chinese_character_riddles`, and fifteen further
`chinese*` task names. They are excluded because the paper's own Table 1 does not report them
and I could not establish which of the eight datasets they belong to. They are 4.7 per cent of
rows.

## 4. Provenance check against the paper's own Table 1

Our per-model per-family means, computed from the pickles, are compared against Table 1 of
arXiv:2403.12031v2, using the protocol the paper states (5-shot for MMLU, HellaSwag, GSM8K,
ARC, Winogrande; 0-shot for MBPP and MT-Bench). Full table:
`experiments/data/A4/validation_vs_paper_table1.csv`.

| family | max abs difference, ours minus published |
|---|---|
| GSM8K | 0.0060 |
| Winogrande | 0.0322 |
| ARC | 0.0426 |
| MMLU | 0.0672 |
| MBPP | 0.0702 |
| HellaSwag | 0.1071 |
| **MT-Bench** | **0.2942** |

Six of the seven families reproduce to within 0.11, and five to within 0.07, which is what one
expects when the exact row subset behind a published table is not recorded. **MT-Bench does
not reproduce**: our means are uniformly 0.165 to 0.294 BELOW the published ones for all eleven
models. MT-Bench is 80 rows, 0.23 per cent of the rows used. I could not resolve the
discrepancy; the most likely explanation is that Table 1 was computed from
`routerbench_raw.pkl` or from a larger MT-Bench split than the 80 rows these two files carry.

Consequence for this package: MT-Bench is one of seven contexts in the Q=7 runs and carries
0.23 per cent of the arrival mass, so nothing depends on it. Every headline result is also
reported on the Q=3 context set (MMLU, HellaSwag, GSM8K), which excludes it. Capability numbers
used here are always computed from the pickles, never copied from Table 1; the comparison above
is a provenance check, not a dependency.

## DECISION, recorded by the lead, 24 Sep 2026

The user's instruction: state plainly which dataset we use, and note whether
others have used it. We proceed on that basis rather than withdrawing the
package.

The position we will state in the paper, all of which is verified:

1. We use the RouterBench dataset of Hu et al. (arXiv:2403.12031), published
   at github.com/withmartian/routerbench, and we say so.
2. The dataset was released by its authors expressly for this purpose. From
   the paper's own abstract, verified against the arXiv record: a
   "comprehensive dataset comprising over 405k inference outcomes from
   representative LLMs to support the development of routing strategies",
   with "The code and data are available at" the repository.
3. The repository's code carries an explicit MIT licence (head commit
   cc67d1008bd8f3cf1e8040cc3ba4034d31b93c0c, GitHub licence API reports
   spdx_id MIT). The data files carry no separate licence statement that we
   could find, which we do not conceal.
4. The work is cited by 60 papers on the Semantic Scholar graph as of today,
   several of which are themselves routing evaluations or benchmarks and so
   are consumers of the data rather than only of the paper. Community use is
   therefore established practice.
5. We redistribute only aggregate derived statistics. No prompt, no model
   response and no per-query row leaves this package.

This is a judgement about norms, not a legal opinion, and it is the user's
judgement to have made. If the position changes the package is
self-contained and withdrawing it costs nothing else in the paper.

## 5. Papers reimplemented, and their licences

Two mechanisms in this package are REIMPLEMENTATIONS FROM A PAPER, because neither released code
or an artifact. Neither reimplementation reproduces the original results in the original setting.

| work | how it was obtained, and when | licence of the text | what was taken |
|---|---|---|---|
| Esmaeili et al., AAAI 2025, DOI 10.1609/aaai.v39i13.33510, arXiv:2403.15115 | as described in this paper's own related-work section, 24 September 2026 | arXiv default (non-exclusive distribution) | the rule as our related work states it: one pull per agent, second-highest bid as the price, exclusion below it |
| Cao, Wang, Liu, Li, Tao, He, WWW 2026, pages 249 to 260, DOI 10.1145/3774904.3792446, arXiv:2511.00847v5 | arXiv HTML v5 full text including Appendix A, fetched 25 September 2026 | **CC BY-NC-ND 4.0**, as stated on the arXiv HTML page | Mechanism 1 line by line: the phase structure, `B = T^{2 eps}`, `M = T^{-eps} ln(KT)`, `delta_i`, `T_R`, the line-16 fixed-slack test and its break, and both blind-trust phases; plus the two theorem assumptions and the Hoeffding step that fixes `b = R` |

CC BY-NC-ND permits reading and redistribution of the unmodified text with attribution; it does
not restrict independently implementing an algorithm described in it. No text, figure or table
from either paper is reproduced in this repository. What is committed is our own code and our own
measurements, and both papers are cited by DOI wherever their mechanism appears.
