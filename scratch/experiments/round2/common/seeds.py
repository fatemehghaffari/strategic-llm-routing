"""Seed derivation (Scout A4, Section 6.2): one master, suite id, phase id, instance index, horizon, replicate.

trial_ss = SeedSequence([master, suite_id, phase_id, instance_index, n, rep])
children  = trial_ss.spawn(5): Stage-1 tape, primary tape, fallback tape, mechanism randomness, deviation randomness.
"""
from __future__ import annotations

import numpy as np

MASTER = 20260828
SUITES = {"scalar_incentives": 1, "scalar_performance": 2, "contextual_performance": 3, "contextual_incentives": 4,
          "gap_grid": 5, "ablations": 6, "exploitability": 7, "nonsynthetic": 8, "public_ucb": 9, "contextual_exact": 10}
PHASES = {"pilot": 0, "final": 1, "train": 2, "eval": 3, "analysis": 9}
CHILD = {"bid": 0, "primary": 1, "fallback": 2, "mechanism": 3, "deviation": 4}


def trial_seed_sequence(suite: str, phase: str, instance_index: int, n: int, rep: int, master: int = MASTER):
    return np.random.SeedSequence([master, SUITES[suite], PHASES[phase], int(instance_index), int(n), int(rep)])


def trial_streams(suite: str, phase: str, instance_index: int, n: int, rep: int, master: int = MASTER):
    """Return (seed_key string, seed_uint32, dict of child Generators)."""
    ss = trial_seed_sequence(suite, phase, instance_index, n, rep, master)
    children = ss.spawn(5)
    gens = {name: np.random.default_rng(children[i]) for name, i in CHILD.items()}
    key = f"{master}-{SUITES[suite]}-{PHASES[phase]}-{instance_index}-{n}-{rep}"
    return key, int(ss.generate_state(1)[0]), gens


def analysis_rng(suite: str, cell_index: int, metric_index: int, master: int = MASTER):
    return np.random.default_rng(np.random.SeedSequence([master, SUITES[suite], PHASES["analysis"], int(cell_index), int(metric_index)]))
