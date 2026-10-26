"""Answer extraction and grading, re-runnable offline from the saved raw outputs (regrade.py).

Extraction order, on the text AFTER the </think> segment:
  1. the LAST 'Final answer' marker; the answer is the text after it, which may run over several
     lines (the model often writes 'Final answer: $$\\n\\boxed{16}\\n$$' or '<answer>79</answer>');
     inside that tail a \\boxed{...} wins, else the tail with tags, markdown and math delimiters
     stripped, cut at the first blank line;
  2. else the LAST \\boxed{...} anywhere in the answer text;
  3. else the last number in the answer text.
Grading: GSM8K golds are integers, so the prediction is reduced to its first number (units such as
'pounds', '$', 'cm' and trailing periods are dropped). MATH-500: normalised string equality of the
prediction and the gold answer, with numeric equality when both parse as numbers, after a
conservative LaTeX normalisation (\\boxed, \\left/\\right, \\dfrac/\\tfrac -> \\frac, \\text{...}
unwrapping, spaces, trailing punctuation, '^\\circ', '\\%', '$', 'a/b' and '\\frac{a}{b}' both to the
same fraction form). Limitations: no symbolic equivalence (x+1 vs 1+x is graded wrong); such pairs
bias every budget equally. Malformed or missing answers grade as wrong.
"""
import re

FINAL = re.compile(r"[Ff]inal\s+[Aa]nswer\s*[:：]?", re.M)

def answer_part(text):
    """The customer-visible answer: the text after the last </think>."""
    if text is None: return ""
    return text.split("</think>")[-1] if "</think>" in text else text

def extract(text):
    """Returns (prediction string or None, method)."""
    t = answer_part(text)
    if not t.strip(): return None, "missing"
    ms = list(FINAL.finditer(t))
    if ms:
        tail = t[ms[-1].end():]
        b = _first_boxed(tail)
        if b is not None: return b.strip(), "final_answer_boxed"
        tail = re.split(r"\n\s*\n", tail.strip(), maxsplit=1)[0]        # the paragraph that follows the marker
        tail = re.sub(r"</?answer>", " ", tail)                          # the literal template tags
        tail = tail.replace("$$", " ").replace("**", " ").replace("$", " ").replace("`", " ")
        tail = re.sub(r"\\\[|\\\]|\\\(|\\\)", " ", tail).strip()
        if tail: return tail, "final_answer_line"
    b = _last_boxed(t)
    if b is not None: return b.strip(), "boxed"
    nums = re.findall(r"-?\d[\d,]*\.?\d*", t)
    if nums: return nums[-1], "last_number"
    return None, "malformed"

def _boxed_at(s, i):
    j = s.find("{", i)
    if j < 0: return None
    depth, k = 0, j
    while k < len(s):
        if s[k] == "{": depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0: return s[j + 1:k]
        k += 1
    return None

def _first_boxed(s):
    i = s.find("\\boxed")
    return None if i < 0 else _boxed_at(s, i)

def _last_boxed(s):
    i = s.rfind("\\boxed")
    return None if i < 0 else _boxed_at(s, i)

def normalize(a):
    if a is None: return None
    a = str(a).strip()
    b = _first_boxed(a)
    if b is not None: a = b
    a = a.strip().strip("$").strip()
    a = a.replace("\\left", "").replace("\\right", "").replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\displaystyle", "")
    a = re.sub(r"\\text\{([^}]*)\}", r"\1", a); a = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", a); a = re.sub(r"\\textbf\{([^}]*)\}", r"\1", a)
    a = a.replace("^\\circ", "").replace("^{\\circ}", "").replace("\\%", "").replace("%", "").replace("\\!", "").replace("\\,", "").replace("\\;", "").replace("\\ ", "")
    a = a.replace(" ", "").replace("\n", "").rstrip(".").rstrip(",").rstrip(";")
    a = re.sub(r"^(dollars|usd)", "", a, flags=re.I); a = re.sub(r"(dollars|cents|units|degrees)$", "", a, flags=re.I)
    m = re.fullmatch(r"-?\\frac\{(-?\d+)\}\{(-?\d+)\}", a) or re.fullmatch(r"-?\\frac(\d)(\d)", a)
    if m:
        sign = -1 if a.startswith("-") else 1
        try: return _num(sign * int(m.group(1)) / int(m.group(2)))
        except Exception: pass
    m = re.fullmatch(r"(-?\d+)/(\d+)", a)
    if m:
        try: return _num(int(m.group(1)) / int(m.group(2)))
        except Exception: pass
    try: return _num(float(a.replace(",", "")))
    except Exception: pass
    # a general expression: canonicalise fraction spelling inside it (1/5 <-> \frac{1}{5}) and leave the rest
    a = re.sub(r"\\frac\{(-?\d+)\}\{(\d+)\}", r"\1/\2", a)
    return a

def _num(x):
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.6g}"

def numeric_gold(gold):
    try: float(str(gold).replace(",", "")); return True
    except Exception: return False

def correct(pred_text, gold):
    """(is_correct, extraction method, prediction string)."""
    pred, how = extract(pred_text)
    if pred is None: return False, how, None
    g = normalize(str(gold))
    if numeric_gold(gold):
        # integer / decimal gold: the prediction is its first number, so '100 pounds.' and '$3.00.' grade on the number
        p = normalize(pred)
        if p is None or not re.fullmatch(r"-?\d+(\.\d+)?(e[+-]?\d+)?", p):
            m = re.search(r"-?\d[\d,]*\.?\d*", pred.replace("\\frac", " \\frac"))
            p = normalize(m.group(0)) if m else p
        return (p == g), how, pred
    return (normalize(pred) == g), how, pred

if __name__ == "__main__":
    T = "<think>stuff 7 and 8</think>\n"
    tests = [(T + "... Final answer: 72", "72", True), (T + "so \\boxed{\\frac{1}{2}} done", "\\frac12", True), (T + "Final answer: $18", "18", True),
             (T + "answer is 3.5", "7/2", True), (T + "Final answer: 1,200", "1200", True), (T + "I think 4", "5", False), ("", "5", False),
             (T + "Final answer: \\boxed{x^2+1}", "x^2+1", True), (T + "Final answer: 90^\\circ", "90", True),
             # the pilot's failure patterns
             (T + "Final answer: $$\n\\boxed{16}\n$$", "16", True), (T + "Final answer: <answer>79</answer>", "79", True),
             (T + "Final answer: 100 pounds.", "100", True), (T + "Final answer: ** $\\boxed{4}$", "4", True), (T + "Final answer: 12 cm.", "12", True),
             (T + "Final answer: $3.00.", "3", True), (T + "Final answer: $450", "450", True), (T + "Final answer: 398.", "398", True),
             (T + "Final answer: 4005.", "4005", True), (T + "### Final Answer\n\n$$\n\\boxed{-2}\n$$", "-2", True),
             (T + "Final answer: $\\boxed{\\begin{pmatrix} \\dfrac{1}{5} \\\\ -\\dfrac{18}{5} \\end{pmatrix}}$", "\\begin{pmatrix} 1/5 \\\\ -18/5 \\end{pmatrix}", True),
             (T + "Final answer: \\dfrac{13}{18}", "\\frac{13}{18}", True), (T + "Final answer: **\n\n$$\\boxed{2}$$", "2", True),
             (T + "Final answer: 7\n\nBut wait, 8 also", "7", True), (T + "Final answer: 2107", "2107", True),
             # the number inside the think segment must not be used
             ("<think>the answer is 5</think>\nno conclusion here", "5", False), (T + "Final answer: 16", "61", False)]
    bad = 0
    for t, g, want in tests:
        got, how, pred = correct(t, g); ok = got == want; bad += (not ok)
        print(("ok  " if ok else "BAD "), repr(t[-40:]), "| gold", g, "| pred", repr(pred), how)
    print("failures:", bad)
