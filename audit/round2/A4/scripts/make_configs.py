"""Emit the headline run grid as JSONL.  Nothing here is tuned to an outcome."""
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rb_common import OUT  # noqa: E402
from select_triples import flip_rate_table, pick  # noqa: E402

Q3 = ["MMLU", "HellaSwag", "GSM8K"]
Q7 = ["MMLU", "HellaSwag", "GSM8K", "Winogrande", "ARC", "MBPP", "MT-Bench"]
ALPHAS = ["a0.00", "a0.25", "a0.50", "a0.75", "het"]
N = 300000
NSEEDS = 10


def main(path):
    tri3 = pick(flip_rate_table(Q3))
    tri7 = pick(flip_rate_table(Q7))
    cfgs = []
    for label, models in tri3.items():
        for al in ALPHAS:
            cfgs.append({"kind": "finite", "family_set": "Q3", "families": Q3,
                         "triple": label, "models": models.split("|"), "alpha": al,
                         "shot": "5shot", "uniform_mass": False,
                         "n": N, "nseeds": NSEEDS})
    for label, models in tri7.items():
        for al in ALPHAS:
            for um in (False, True):
                cfgs.append({"kind": "finite",
                             "family_set": "Q7u" if um else "Q7",
                             "families": Q7, "triple": label,
                             "models": models.split("|"), "alpha": al,
                             "shot": "5shot", "uniform_mass": um,
                             "n": N, "nseeds": NSEEDS})
    for label, models in tri7.items():
        for al in ALPHAS:
            for rho in ("paper", "measured"):
                cfgs.append({"kind": "continuous", "family_set": f"cont_rho{rho}",
                             "triple": label, "models": models.split("|"),
                             "alpha": al, "d": 2, "k": 200, "rho_mode": rho,
                             "n": N, "nseeds": NSEEDS})
    with open(path, "w") as fh:
        for j, c in enumerate(cfgs):
            c["config_id"] = f"{c['family_set']}_{c['triple']}_{c['alpha']}"
            fh.write(json.dumps(c) + "\n")
    print(f"{len(cfgs)} configs -> {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, "configs.jsonl"))
