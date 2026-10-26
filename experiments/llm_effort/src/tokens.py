"""Reasoning / answer token split for a Qwen3 completion, from the generated token ids.

The offline vLLM engine returns the raw text with the <think> ... </think> segment inline (the
reasoning parser only acts in the OpenAI-compatible server), so the split is done here on the
token ids. vLLM's thinking_token_budget counts the tokens generated after the <think> token and
forces </think> once the count would exceed the budget, so `reasoning_tokens` here is the number
the budget bounds.
"""

def think_ids(tok):
    s, e = tok.convert_tokens_to_ids("<think>"), tok.convert_tokens_to_ids("</think>")
    assert isinstance(s, int) and isinstance(e, int) and s != tok.unk_token_id and e != tok.unk_token_id, "no think tokens in vocab"
    return s, e

def split_reasoning(token_ids, tok, think=None):
    """Returns dict(reasoning_tokens, answer_tokens, think_opened, think_closed)."""
    s, e = think or think_ids(tok)
    ids = list(token_ids)
    opened = s in ids
    start = ids.index(s) + 1 if opened else 0
    if e in ids[start:]:
        end = start + ids[start:].index(e)
        return dict(reasoning_tokens=end - start, answer_tokens=len(ids) - end - 1, think_opened=opened, think_closed=True)
    # never closed: everything after <think> (or everything, if it never opened) is reasoning
    return dict(reasoning_tokens=len(ids) - start, answer_tokens=0, think_opened=opened, think_closed=False)
