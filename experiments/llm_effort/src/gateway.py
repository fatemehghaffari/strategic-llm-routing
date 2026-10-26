"""The provider's gateway: holds the customer-visible configuration fixed and privately assigns a
backend reasoning budget to each request.

The client never sets a budget; it sends (model_id, service_tier, messages). The gateway's policy maps
request metadata available BEFORE generation (benchmark/category label, prompt text) to a budget.
Policies: fixed_low | fixed_medium | fixed_high | task_adaptive | random_matched.

Distinction stated for the paper: if a customer contractually specifies an exact reasoning-token limit
that the service guarantees to enforce, overriding it is not an authorised backend choice. Here the
customer specifies a service tier, not a token count.
"""
import numpy as np

class Gateway:
    def __init__(self, budgets, policy, seed=0, adaptive_rule=None, match_proportions=None):
        self.b = budgets; self.policy = policy; self.rng = np.random.default_rng(seed)
        self.rule = adaptive_rule or (lambda cat, prompt: "high" if cat == "competition_math" else "low")
        self.props = match_proportions; self.log = []

    def choose(self, request_id, category, prompt):
        if self.policy == "fixed_low": lvl = "low"
        elif self.policy == "fixed_medium": lvl = "medium"
        elif self.policy == "fixed_high": lvl = "high"
        elif self.policy == "task_adaptive": lvl = self.rule(category, prompt)
        elif self.policy == "random_matched":
            lv, pr = zip(*self.props.items()); lvl = str(self.rng.choice(lv, p=np.array(pr) / sum(pr)))
        else: raise ValueError(self.policy)
        self.log.append(dict(request_id=request_id, category=category, level=lvl, budget=self.b[lvl]))
        return lvl, self.b[lvl]
