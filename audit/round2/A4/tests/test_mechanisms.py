"""Tests for the calibrated-simulation engine.  Written before the analysis.

Covered, at minimum, as the brief requires:
  * phase accounting: every round is charged to exactly one phase, and the
    phase totals sum to the horizon, in every mechanism and every partition;
  * no agent ever delivers above its capability, on any round, under any
    strategy including the deviations;
  * reward-sum integrality: realised rewards are Bernoulli, so their sum is a
    non-negative integer no larger than the horizon;
  * the scalar mechanism and the contextual mechanism agree, trajectory by
    trajectory, when there is exactly one context.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mechanisms import (BoundaryTrackStrategy, Instance, MechanismRun,  # noqa: E402
                        ProfileStrategy, SelectiveStrategy, Strategy, design_constants,
                        honest_benchmark_per_round, oracle_per_round,
                        run_mesp_reference, run_router,
                        second_capability_per_round)

RNG = np.random.default_rng(11223344)


def make_instance(nq=400, K=3, Q=4, alpha=0.5, seed=7):
    r = np.random.default_rng(seed)
    key = r.integers(0, Q, size=nq)
    base = r.random((Q, K)) * 0.6 + 0.2
    M = np.clip(base[key] + r.normal(0, 0.03, size=(nq, K)), 0.02, 0.99)
    mu = alpha * M
    honest = np.zeros(K, dtype=bool)
    honest[0] = True
    return Instance(M=M, mu=mu, key=key, honest=honest,
                    names=[f"a{i}" for i in range(K)])


def queries_for(inst, n, seed=3):
    return np.random.default_rng(seed).integers(0, inst.M.shape[0], size=n)


# --------------------------------------------------------------------------- #
# phase accounting
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("Q", [1, 2, 4, 9])
@pytest.mark.parametrize("monitor", ["anytime", "twosample", "none"])
def test_phase_accounting_sums_to_horizon(Q, monitor):
    inst = make_instance(Q=Q)
    n = 4000
    qs = queries_for(inst, n)
    run = MechanismRun(inst, n, seed=1, monitor=monitor, batch=50)
    res = run.run(Strategy(inst, np.ones(inst.K)), qs)
    assert sum(res["phase_rounds"].values()) == n
    assert res["phase_rounds"]["route"] == 0
    assert int(res["T"].sum()) == n


@pytest.mark.parametrize("Q", [1, 3])
def test_phase_accounting_elicitation_block_is_exact(Q):
    """Each local instance that finished elicitation spent exactly K*L_n rounds there."""
    inst = make_instance(Q=Q)
    n = 6000
    L, _, _ = design_constants(n, inst.K)
    run = MechanismRun(inst, n, seed=2)
    res = run.run(Strategy(inst, np.ones(inst.K)), queries_for(inst, n))
    done = [lo for lo in run.locals.values() if lo.phase != "elicit"]
    spent = sum(int(lo.cnt.sum()) for lo in run.locals.values())
    assert res["phase_rounds"]["elicit"] == spent
    for lo in done:
        assert int(lo.cnt.sum()) == inst.K * L
        assert (lo.cnt == L).all()


def test_no_local_exceeds_its_own_accounting():
    inst = make_instance(Q=5)
    n = 8000
    run = MechanismRun(inst, n, seed=5)
    res = run.run(Strategy(inst, np.ones(inst.K)), queries_for(inst, n))
    total = 0
    for lo in run.locals.values():
        total += int(lo.cnt.sum()) + lo.r
    assert total + res["phase_rounds"]["fallback"] == n


# --------------------------------------------------------------------------- #
# feasibility: nobody ever delivers above its capability
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("theta", [0.0, 0.3, 1.0])
@pytest.mark.parametrize("Q", [1, 4])
def test_target_never_exceeds_capability_stationary(theta, Q):
    inst = make_instance(Q=Q)
    n = 3000
    strat = Strategy(inst, np.full(inst.K, theta))
    for q in range(inst.M.shape[0]):
        for i in range(inst.K):
            for phase in ("elicit", "primary", "fallback"):
                for price in (None, 0.0, 0.5, 1.0):
                    if phase != "primary" and price is not None:
                        continue
                    st = {"r": 3, "Z": 1.0, "tau": price or 0.0,
                          "b": design_constants(n, inst.K)[2]}
                    m = strat.target(i, phase, q, price, st if phase == "primary" else None)
                    assert m <= inst.M[q, i] + 1e-12
                    assert m >= -1e-12


def test_engine_asserts_on_infeasible_strategy():
    inst = make_instance(Q=2)

    class Cheat(Strategy):
        def target(self, i, phase, q, price, state=None):
            return self.inst.M[q, i] + 0.05

    n = 500
    run = MechanismRun(inst, n, seed=9)
    with pytest.raises(AssertionError):
        run.run(Cheat(inst, np.ones(inst.K)), queries_for(inst, n))


@pytest.mark.parametrize("Q", [1, 4])
def test_deviation_strategies_are_feasible(Q):
    inst = make_instance(Q=Q)
    n = 3000
    qs = queries_for(inst, n)
    top = inst.M.argmax(axis=1) == 1
    for strat in (SelectiveStrategy(inst, np.ones(inst.K), 1, top),
                  BoundaryTrackStrategy(inst, np.ones(inst.K), 1)):
        res = MechanismRun(inst, n, seed=4).run(strat, qs)
        assert sum(res["phase_rounds"].values()) == n


def test_honest_agent_never_delivers_below_its_intrinsic_level():
    """The engine pins honest agents at m >= mu pointwise, whatever theta says."""
    inst = make_instance(Q=3)
    n = 3000
    qs = queries_for(inst, n)
    theta = np.zeros(inst.K)
    res = MechanismRun(inst, n, seed=6).run(Strategy(inst, theta), qs)
    # agent 0 is the honest one; pinned at mu means it pays exactly zero effort
    assert res["C"][0] == pytest.approx(0.0, abs=1e-9)
    assert (res["C"][1:] <= 1e-9).all()


# --------------------------------------------------------------------------- #
# reward-sum integrality
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("Q", [1, 5])
def test_reward_sum_is_an_integer_in_range(seed, Q):
    inst = make_instance(Q=Q)
    n = 3000
    res = MechanismRun(inst, n, seed=seed).run(Strategy(inst, np.ones(inst.K)),
                                               queries_for(inst, n))
    y = res["revenue_realized"]
    assert isinstance(y, int)
    assert 0 <= y <= n
    assert float(y) == int(y)


def test_router_reward_sum_and_allocation():
    inst = make_instance(Q=4)
    n = 3000
    for rule in ("greedy", "epsgreedy", "ucb"):
        res = run_router(inst, n, 1, Strategy(inst, np.ones(inst.K)),
                         queries_for(inst, n), rule=rule)
        assert int(res["T"].sum()) == n
        assert 0 <= res["revenue_per_round"] <= 1


# --------------------------------------------------------------------------- #
# the scalar and the contextual mechanism agree at exactly one context
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("theta_dev", [1.0, 0.4])
def test_single_context_contextual_equals_scalar(seed, theta_dev):
    """PL-MESP with Q = 1 reproduces the standalone transcription of Algorithm 1."""
    inst = make_instance(Q=1)
    n = 5000
    qs = queries_for(inst, n, seed=seed)
    theta = np.ones(inst.K)
    theta[1] = theta_dev
    a = MechanismRun(inst, n, seed=seed).run(Strategy(inst, theta), qs)
    b = run_mesp_reference(inst, n, seed, Strategy(inst, theta), qs)
    assert a["revenue_target"] == pytest.approx(b["revenue_target"], rel=0, abs=1e-9)
    assert (a["T"] == b["T"]).all()
    assert a["C"] == pytest.approx(b["C"], abs=1e-9)


def test_single_context_disagrees_from_multi_context_when_it_should():
    """Sanity: the Q = 1 agreement is not vacuous, Q > 1 genuinely differs."""
    inst = make_instance(Q=4)
    n = 5000
    qs = queries_for(inst, n)
    a = MechanismRun(inst, n, seed=1).run(Strategy(inst, np.ones(inst.K)), qs)
    flat = Instance(M=inst.M, mu=inst.mu, key=np.zeros_like(inst.key),
                    honest=inst.honest, names=inst.names)
    b = MechanismRun(flat, n, seed=1).run(Strategy(flat, np.ones(flat.K)), qs)
    assert a["n_locals"] == 4 and b["n_locals"] == 1
    assert a["revenue_target"] != pytest.approx(b["revenue_target"], abs=1e-6)


# --------------------------------------------------------------------------- #
# design constants and prices
# --------------------------------------------------------------------------- #
def test_design_constants_match_the_paper():
    for n in (2000, 50000, 1000000):
        for K in (2, 3, 5):
            L, s, b = design_constants(n, K)
            assert L == min(n // (2 * K), int(np.ceil(n ** (2 / 3) * np.log(np.e * n) ** (1 / 3))))
            import math
            assert s == pytest.approx(math.sqrt(math.log(2 * K * n ** 4) / (2 * L)))
            assert b(7) == pytest.approx(math.sqrt(7 * math.log(2 * n ** 4) / 2))
            assert b(0) == 0.0


def test_price_is_the_shaded_second_bid():
    inst = make_instance(Q=1)
    n = 6000
    run = MechanismRun(inst, n, seed=1)
    run.run(Strategy(inst, np.ones(inst.K)), queries_for(inst, n))
    lo = run.locals[0]
    beta = lo.sum / lo.cnt
    assert lo.tau == pytest.approx(max(0.0, float(np.sort(beta)[-2]) - run.s))
    assert lo.W == int(np.lexsort((lo.priority, -beta))[0])


def test_oscillation_allowance_lowers_the_price():
    inst = make_instance(Q=3)
    n = 6000
    qs = queries_for(inst, n)
    plain = MechanismRun(inst, n, seed=1, price_shade=0.0)
    plain.run(Strategy(inst, np.ones(inst.K)), qs)
    shaded = MechanismRun(inst, n, seed=1, price_shade=0.05)
    shaded.run(Strategy(inst, np.ones(inst.K)), qs)
    for k in plain.locals:
        if plain.locals[k].phase != "elicit":
            assert shaded.locals[k].tau <= plain.locals[k].tau + 1e-12


# --------------------------------------------------------------------------- #
# benchmarks
# --------------------------------------------------------------------------- #
def test_benchmark_ordering():
    inst = make_instance(Q=4, alpha=0.5)
    qs = queries_for(inst, 5000)
    o = oracle_per_round(inst, qs)
    s = second_capability_per_round(inst, qs)
    h = honest_benchmark_per_round(inst, qs)
    assert o >= s >= 0
    assert o >= h


def test_honest_benchmark_scales_with_alpha():
    for a in (0.0, 0.25, 0.5, 1.0):
        inst = make_instance(Q=3, alpha=a)
        qs = queries_for(inst, 3000)
        inst0 = make_instance(Q=3, alpha=1.0)
        assert honest_benchmark_per_round(inst, qs) == pytest.approx(
            a * honest_benchmark_per_round(inst0, qs), rel=1e-9)


# --------------------------------------------------------------------------- #
# end to end: the two mechanisms of the headline comparison coincide at Q = 1
# --------------------------------------------------------------------------- #
def test_headline_comparison_collapses_at_one_context():
    """Through run_sim.evaluate, the contextual and the scalar arm of the
    headline comparison must be the same mechanism when there is one context."""
    import run_sim  # noqa: E402
    inst = make_instance(Q=1)
    n = 5000
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    for opts in (["proposed"] * 3, ["theta1.00", "proposed", "theta0.50"]):
        a = run_sim.evaluate("plmesp", inst, None, n, 5, opts, tm)
        b = run_sim.evaluate("mesp_scalar", inst, None, n, 5, opts, tm)
        assert a["revenue_target"] == pytest.approx(b["revenue_target"], abs=1e-9)
        assert (a["T"] == b["T"]).all()
        assert a["n_locals"] == b["n_locals"] == 1


def test_router_uses_the_context_when_told_to():
    """The context-aware router keeps one estimate per context, the blind one
    keeps a single estimate; on an instance whose best agent differs by context
    they must not produce the same allocation."""
    from mechanisms import run_router as rr
    r = np.random.default_rng(1)
    nq, K, Q = 200, 3, 2
    key = np.tile(np.arange(Q), nq // Q)
    M = np.empty((nq, K))
    M[key == 0] = [0.9, 0.3, 0.3]
    M[key == 1] = [0.3, 0.9, 0.3]
    inst = Instance(M=M, mu=0.1 * M, key=key, honest=np.array([True, False, False]),
                    names=list("abc"))
    n = 20000
    qs = r.integers(0, nq, size=n)
    s = Strategy(inst, np.ones(K))
    aware = rr(inst, n, 1, s, qs, rule="ucb", context_aware=True)
    blind = rr(inst, n, 1, s, qs, rule="ucb", context_aware=False)
    assert aware["revenue_per_round"] > blind["revenue_per_round"] + 0.05


# --------------------------------------------------------------------------- #
# BASELINE 1: the single-observation exclusion rule under our observation model
# --------------------------------------------------------------------------- #
def test_single_observation_rule_accounting():
    """Phase accounting, feasibility and integrality for the exclusion rule."""
    from mechanisms import run_single_observation_exclusion as soe
    inst = make_instance(Q=1)
    n = 4000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    for empty in ("stop", "roundrobin"):
        r = soe(inst, n, 3, ProfileStrategy(inst, ["proposed"] * inst.K, tm), qs,
                empty=empty)
        assert int(r["T"].sum()) + r["idle_rounds"] == n
        assert isinstance(r["revenue_realized"], int)
        assert 0 <= r["revenue_realized"] <= n
        assert 0 <= r["exclusions"] <= inst.K
        if empty == "roundrobin":
            assert r["idle_rounds"] == 0


def test_single_pull_elicitation_can_only_announce_zero_or_one():
    """With ONE Bernoulli pull per agent the elicited bids are 0 or 1, so the
    announced price is 0 or 1 and is never a capability.  This is the sharp
    form of what Theorem `thm:separation` is about."""
    from mechanisms import run_single_observation_exclusion as soe
    inst = make_instance(Q=1)
    n = 2000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    prices = {soe(inst, n, s, ProfileStrategy(inst, ["proposed"] * inst.K, tm), qs,
                  L_elicit=1)["announced_price"] for s in range(40)}
    assert prices <= {0.0, 1.0}
    assert len(prices) == 2, "both prices should occur over 40 seeds"


def test_single_observation_rule_excludes_a_compliant_winner():
    """A winner playing the proposed profile exactly is still excluded, because
    exclusion is decided from one Bernoulli draw."""
    from mechanisms import run_single_observation_exclusion as soe
    inst = make_instance(Q=1, alpha=0.5)
    n = 20000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    rs = [soe(inst, n, s, ProfileStrategy(inst, ["proposed"] * inst.K, tm), qs,
              L_elicit=1) for s in range(30)]
    # on the seeds where a positive price is announced, compliant winners go
    assert sum(r["compliant_exclusions"] for r in rs) > 0
    # and the mechanism collects far less than the monitored second price does
    mesp = [MechanismRun(inst, n, s).run(
        ProfileStrategy(inst, ["proposed"] * inst.K, tm), qs) for s in range(5)]
    assert (np.mean([r["revenue_per_round"] for r in rs])
            < 0.5 * np.mean([r["revenue_per_round"] for r in mesp]))


# --------------------------------------------------------------------------- #
# BASELINE 2: the fixed-buffer monitor rung
# --------------------------------------------------------------------------- #
def test_fixed_buffer_rung_respects_its_burn_in():
    """No conviction can occur before the burn-in, whatever the buffer."""
    inst = make_instance(Q=1, alpha=0.0)
    n = 30000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    burn = 500
    run = MechanismRun(inst, n, 1, monitor="fixedbuffer", buffer=0.0, burnin=burn)
    res = run.run(ProfileStrategy(inst, ["theta0.00"] * inst.K, tm), qs)
    for r in res["conviction_rounds"].values():
        assert r >= burn


def test_fixed_buffer_is_monotone_in_the_buffer():
    """A larger buffer is more permissive, so it cannot convict strictly more."""
    inst = make_instance(Q=1, alpha=0.3)
    n = 20000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    strat = ProfileStrategy(inst, ["proposed", "theta0.00", "proposed"], tm)
    convs = []
    for buf in (0.0, 0.05, 0.2, 0.9):
        res = MechanismRun(inst, n, 4, monitor="fixedbuffer", buffer=buf,
                           burnin=100).run(strat, qs)
        convs.append(res["convictions"])
    assert convs == sorted(convs, reverse=True)


# --------------------------------------------------------------------------- #
# the RICH option class
# --------------------------------------------------------------------------- #
def test_rich_options_are_all_feasible_and_distinct():
    from mechanisms import RICH_OPTIONS
    inst = make_instance(Q=3)
    n = 2000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    revs = {}
    for o in RICH_OPTIONS:
        opts = ["proposed"] * inst.K
        opts[1] = o
        res = MechanismRun(inst, n, 2).run(ProfileStrategy(inst, opts, tm), qs)
        assert sum(res["phase_rounds"].values()) == n
        revs[o] = res["revenue_target"]
    # the undercut family is not the same as any constant theta
    assert len({round(revs[o], 6) for o in RICH_OPTIONS}) > 5


def test_undercut_sits_just_above_the_pointwise_runner_up():
    from mechanisms import RICH_OPTIONS  # noqa: F401
    inst = make_instance(Q=4)
    second = np.sort(inst.M, axis=1)[:, -2]
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    st = ProfileStrategy(inst, ["undercut0.02"] * inst.K, tm, second=second)
    for q in range(0, inst.M.shape[0], 37):
        for i in range(inst.K):
            m = st.target(i, "primary", q, 0.5, None)
            assert m <= inst.M[q, i] + 1e-12
            if inst.M[q, i] >= second[q] + 0.02:
                assert m == pytest.approx(second[q] + 0.02)


# --------------------------------------------------------------------------- #
# the second-best utility guarantee mechanism, reimplemented from the paper
# --------------------------------------------------------------------------- #
def test_second_best_phase_accounting_and_integrality():
    from mechanisms import run_second_best
    inst = make_instance(Q=1)
    n = 20000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    for lo in ("to_winner", "none"):
        r = run_second_best(inst, n, 3, ProfileStrategy(inst, ["proposed"] * inst.K, tm),
                            qs, leftover=lo)
        assert sum(r["phase_rounds"].values()) == n
        assert int(r["T"].sum()) + r["phase_rounds"]["undelegated"] == n
        assert isinstance(r["revenue_realized"], int)
        assert 0 <= r["revenue_realized"] <= n


def test_second_best_design_constants_follow_the_paper():
    """B = T^{2 eps} and M = T^{-eps} ln(KT), with eps = 1/3 by default."""
    from mechanisms import run_second_best
    inst = make_instance(Q=1)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    for n in (8000, 27000):
        r = run_second_best(inst, n, 1, ProfileStrategy(inst, ["proposed"] * inst.K, tm),
                            queries_for(inst, n))
        assert r["eps"] == pytest.approx(1.0 / 3.0)
        assert r["B"] == int(np.ceil(n ** (2.0 / 3.0)))
        assert r["M_slack"] == pytest.approx(n ** (-1.0 / 3.0) * np.log(inst.K * n))


class _BaitSwitch(ProfileStrategy):
    """Elicit at capability, then floor in the priced phase.

    Flooring in EVERY phase does not trip either monitor and should not: if
    every provider bids low, the announced standard collapses with them and
    delivering low meets it. Only a bait and switch, which bids high and then
    delivers low against a standard set by that bid, is a violation.
    """

    def __init__(self, inst, tm, deviator):
        super().__init__(inst, ["proposed"] * inst.K, tm)
        self.deviator = deviator

    def target(self, i, phase, q, price, state=None):
        if i == self.deviator and phase == "primary":
            return self.inst.mu[q, i]
        return super().target(i, phase, q, price, state)


def test_second_best_stops_serving_when_its_monitor_fires():
    """Their line 18 breaks, so no query is delegated after the monitor fires."""
    from mechanisms import run_second_best
    inst = make_instance(Q=1, alpha=0.3)
    n = 30000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    top = int(inst.M[0].argmax())
    fired = []
    for s in range(12):
        r = run_second_best(inst, n, s, _BaitSwitch(inst, tm, top), qs,
                            leftover="to_winner")
        fired.append(r["monitor_fired"])
        if r["monitor_fired"]:
            assert r["post_fire_rounds"] > 0
            assert r["phase_rounds"]["undelegated"] == r["post_fire_rounds"]
            assert r["phase_rounds"]["blind1"] == 0
            assert r["phase_rounds"]["blind2"] == 0
    assert any(fired), "the monitor should fire against a bait and switch"


def test_our_mechanism_records_post_switch_revenue():
    """Our fallback keeps serving, so post-switch revenue exists and is positive."""
    inst = make_instance(Q=1, alpha=0.3)
    n = 30000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    top = int(inst.M[0].argmax())
    seen = False
    for s in range(12):
        r = MechanismRun(inst, n, s).run(_BaitSwitch(inst, tm, top), qs)
        if r["convictions"]:
            seen = True
            assert r["post_switch_rounds"] > 0
            assert r["post_switch_revenue_per_round"] > 0
    assert seen, "expected at least one conviction over these seeds"


def test_flooring_everywhere_trips_neither_monitor():
    """The control for the two tests above: if every provider floors, the
    announced standard collapses with them and neither monitor fires."""
    from mechanisms import run_second_best
    inst = make_instance(Q=1, alpha=0.0)
    n = 20000
    qs = queries_for(inst, n)
    tm = inst.M >= inst.M.max(axis=1, keepdims=True) - 1e-12
    st = ProfileStrategy(inst, ["theta0.00"] * inst.K, tm)
    assert not run_second_best(inst, n, 1, st, qs)["monitor_fired"]
    assert MechanismRun(inst, n, 1).run(st, qs)["convictions"] == 0
