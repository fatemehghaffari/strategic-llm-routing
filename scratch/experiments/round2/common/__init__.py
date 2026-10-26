"""Shared code for the round-2 experiment suites (AAMAS 2027 revision).

Every suite imports the mechanism constants from `design.py` so that one
definition of L_n, N_n, s_n, b_n(r), the EXP3 constants, and the Grid-ETC
constants is used everywhere; `scratch/tests/test_round2_common.py` asserts
these against the formulas of sections/Private_information_setting.tex and
sections/contextual_samf_algorithm.tex.
"""
