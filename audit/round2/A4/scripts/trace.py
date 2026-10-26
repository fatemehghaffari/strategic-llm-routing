"""Per-round trace of one mechanism run: everything needed to redraw any figure
without rerunning. One row per round t = 0..n-1.

  query    benchmark index of the prompt that arrived (every round, served or not)
  agent    selected provider, 255 if the round was not delegated (Cao after its
           monitor fires)
  phase    code in PHASE_CODES (elicit/primary/fallback for our mechanisms;
           explore/exploit/blind1/blind2 for Cao; undelegated)
  price    announced value in force for the selected agent, NaN outside the
           priced phase
  target   delivered mean m_t chosen by the selected agent (after feasibility)
  reward   realised Bernoulli reward Y_t (the platform's realised revenue)
  effort   m_t - mu_{I_t}(x_t): the selected agent's effort, negative below its
           intrinsic level
  agent_utility  1 + phi(mu) - phi(m) with the linear cost of A4, the selected
           agent's utility this round; every other agent earns 0 that round
Platform expected revenue in round t is `target`, realised revenue is `reward`.
"""
import json

import numpy as np

PHASE_CODES = {"elicit": 0, "primary": 1, "fallback": 2, "route": 3,
               "explore": 4, "exploit": 5, "blind1": 6, "blind2": 7, "undelegated": 8}


class Trace:
    def __init__(self, queries):
        n = len(queries)
        self.query = np.asarray(queries, dtype=np.uint8)
        self.agent = np.full(n, 255, dtype=np.uint8)
        self.phase = np.full(n, PHASE_CODES["undelegated"], dtype=np.uint8)
        self.price = np.full(n, np.nan, dtype=np.float32)
        self.target = np.zeros(n, dtype=np.float32)
        self.reward = np.zeros(n, dtype=np.uint8)
        self.effort = np.zeros(n, dtype=np.float32)
        self.agent_utility = np.zeros(n, dtype=np.float32)

    def log(self, t, q, i, phase, price, m, y, mu):
        self.agent[t] = i
        self.phase[t] = PHASE_CODES[phase]
        self.price[t] = price if price is not None else np.nan
        self.target[t] = m
        self.reward[t] = y
        self.effort[t] = m - mu
        self.agent_utility[t] = 1.0 + mu - m

    def save(self, path, meta):
        np.savez_compressed(path, query=self.query, agent=self.agent, phase=self.phase,
                            price=self.price, target=self.target, reward=self.reward,
                            effort=self.effort, agent_utility=self.agent_utility,
                            meta=np.frombuffer(json.dumps(meta, default=_js).encode(), dtype=np.uint8))


def _js(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


def load(path):
    z = np.load(path)
    d = {k: z[k] for k in z.files if k != "meta"}
    d["meta"] = json.loads(z["meta"].tobytes().decode())
    return d
