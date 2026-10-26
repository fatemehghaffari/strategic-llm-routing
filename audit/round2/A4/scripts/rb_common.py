"""Shared constants and loaders for the RouterBench calibrated simulation (audit/round2/A4)."""
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_load import safe_read_pickle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

# The eleven models whose per-query outcome columns RouterBench publishes.
MODELS = [
    "WizardLM/WizardLM-13B-V1.2",
    "claude-instant-v1",
    "claude-v1",
    "claude-v2",
    "gpt-3.5-turbo-1106",
    "gpt-4-1106-preview",
    "meta/code-llama-instruct-34b-chat",
    "meta/llama-2-70b-chat",
    "mistralai/mistral-7b-chat",
    "mistralai/mixtral-8x7b-chat",
    "zero-one-ai/Yi-34B-Chat",
]
SHORT = {
    "WizardLM/WizardLM-13B-V1.2": "WizardLM-13B",
    "claude-instant-v1": "Claude-Instant-V1",
    "claude-v1": "Claude-V1",
    "claude-v2": "Claude-V2",
    "gpt-3.5-turbo-1106": "GPT-3.5",
    "gpt-4-1106-preview": "GPT-4",
    "meta/code-llama-instruct-34b-chat": "CodeLlama-34B",
    "meta/llama-2-70b-chat": "Llama-70B",
    "mistralai/mistral-7b-chat": "Mistral-7B",
    "mistralai/mixtral-8x7b-chat": "Mixtral-8x7B",
    "zero-one-ai/Yi-34B-Chat": "Yi-34B",
}

# The seven benchmark families that RouterBench's own Table 1 reports.  The
# assignment is by the published `eval_name` string and nothing else.
FAMILY_RULES = [
    ("MMLU", lambda e: e.startswith("mmlu-")),
    ("HellaSwag", lambda e: e == "hellaswag"),
    ("GSM8K", lambda e: e == "grade-school-math"),
    ("Winogrande", lambda e: e == "winogrande"),
    ("ARC", lambda e: e == "arc-challenge"),
    ("MBPP", lambda e: e == "mbpp"),
    ("MT-Bench", lambda e: e.startswith("mtbench")),
]
FAMILIES = [f for f, _ in FAMILY_RULES]


def family_of(eval_name):
    for fam, rule in FAMILY_RULES:
        if rule(eval_name):
            return fam
    return "UNASSIGNED"


def load_shot(shot):
    """Load one published RouterBench pickle and return the tidy score frame."""
    assert shot in ("0shot", "5shot")
    df = safe_read_pickle(os.path.join(DATA, f"routerbench_{shot}.pkl"))
    out = pd.DataFrame({"sample_id": df["sample_id"].astype(str),
                        "eval_name": df["eval_name"].astype(str)})
    out["family"] = out["eval_name"].map(family_of)
    for m in MODELS:
        out[m] = pd.to_numeric(df[m], errors="coerce").astype(float)
    out["prompt"] = df["prompt"].astype(str)
    return out
