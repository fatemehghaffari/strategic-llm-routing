"""Thin adapter that runs the shared MESP simulator on real provider answers.

`common.mechanism.episode` realizes every reward as 1{U < m} on a pre-drawn uniform tape. This module does
not reimplement the mechanism: it replaces those tapes by objects with the same interface whose comparison
against a target m returns a real provider answer instead of a Bernoulli draw. Concretely, for the pull at
tape position r of agent i the tape holds a pre-drawn task from the play half, a pre-drawn mixture coin and a
pre-drawn row of tree-ordering randomness; `tape < m` turns the target m into a knob through the bank's
calibration (a menu knob, a mixture of two adjacent knobs, or knob 1 mixed with scripted sabotage), evaluates
that provider at that knob on that task, and returns whether the stored true label came back. Everything else
(bidding, price, monitor, EXP3 fallback, effort accounting in the model's convention c = m - mu) is the
unmodified shared module.

Evidence category: real labeled tasks and real provider answers; the effort choice is scripted.

Two points of care. First, the pre-drawn tapes are derived deterministically from the trial's child streams
and their length does not depend on the behavior, so two behaviors of the same replicate meet the same tasks
and the same tree orderings wherever they agree, exactly as the uniform tapes couple the synthetic suites.
Second, the primary tape must know which agent the mechanism selected. The winner is not passed to the tape,
so the adapter recomputes it from the Stage-1 outcomes it produced and from the uniform priority it recorded,
using the same rule as the mechanism, and reports it as `inferred_winner`; the tests assert that it equals the
winner the mechanism reports on every replicate, including forced ties.

Compute cost. The recorded cost of a round is the knob value (trees or stages evaluated; 0 for sabotage). The
monitored primary segment is evaluated as a whole array, so cost is summed over the rounds that were actually
played (the first `primary_rounds` of the segment). For the `exclude` fallback variant, whose monitored
segments are also array evaluations, the fallback cost is an upper bound rather than an exact count; every
other variant, including the `mesp` used in the pilot, is exact.
"""
from __future__ import annotations

import numpy as np

from common import mechanism as M
from common.design import design as make_design

from . import bank as B


class BaitSwitchKnob1(M.Policy):
    """Scripted bait and switch: bid at capacity, then drop to the cheapest knob after winning."""
    name = "bait_switch_knob1"

    def primary_target(self, ctx, r, Z, tau):
        return ctx.mu


class UnderbidKnob(M.Policy):
    """Scripted Stage-1 underbid: bid the calibrated mean of a cheaper knob, then play the proposed profile.

    This is the knob translation of the `underbid` deviation of the scalar suite. It saves
    (M_i - A_i(knob)) L_n of effort in bidding and shrinks the deviator's winning event, which is the trade the
    bid-domination step of the theorem bounds.
    """

    def __init__(self, bank: "B.ResponseBank", knob: int):
        self.bank = bank
        self.knob = int(knob)
        self.name = f"underbid_knob{self.knob}"

    def bid_target(self, ctx, r, z):
        return float(self.bank.accuracy_curve(ctx.i)[self.bank.menu.index(self.knob)])


class _Cell:
    """One tape position; `cell < m` is one real provider answer scored against the stored label."""
    __slots__ = ("tape", "agent", "index")

    def __init__(self, tape, agent, index):
        self.tape, self.agent, self.index = tape, agent, int(index)

    def __lt__(self, m):
        y = self.tape.outcomes(self.agent, np.array([self.index], dtype=np.int64), np.array([float(m)]))
        return np.bool_(bool(y[0]))


class _Row:
    """A contiguous run of tape positions for one agent; `row < m` returns the real outcomes of those rounds."""

    def __init__(self, tape, agent, start, stop):
        self.tape, self.agent, self.start, self.stop = tape, int(agent), int(start), int(stop)

    def __len__(self):
        return self.stop - self.start

    def __lt__(self, m):
        idx = np.arange(self.start, self.stop, dtype=np.int64)
        m_arr = np.asarray(m, dtype=float)
        if m_arr.ndim == 0:
            m_arr = np.full(idx.size, float(m_arr))
        if m_arr.size != idx.size:
            raise ValueError(f"target array of length {m_arr.size} against {idx.size} tape positions")
        return self.tape.outcomes(self.agent, idx, m_arr).astype(bool)

    def __getitem__(self, key):
        if isinstance(key, slice):
            s, e, step = key.indices(len(self))
            if step != 1:
                raise ValueError("strided tape slices are not supported")
            return _Row(self.tape, self.agent, self.start + s, self.start + e)
        return _Cell(self.tape, self.agent, self.start + int(key))


class _PhaseTape:
    """Pre-drawn tasks, mixture coins and tree-ordering randomness for one phase, allocated per agent."""

    def __init__(self, session, phase: str, length: int, seed: int, horizon: int | None = None):
        self.s = session
        self.phase = phase
        self.length = int(length)              # drawn length; independent of the behavior, so tapes couple
        self.horizon = int(length if horizon is None else horizon)
        self.seed = int(seed)
        self.store: dict[int, dict] = {}

    def data(self, agent: int) -> dict:
        d = self.store.get(agent)
        if d is None:
            bank = self.s.bank
            rng = np.random.default_rng([self.seed, int(agent)])
            task = bank.draw_tasks(rng, self.length)
            coin = rng.random(self.length)
            rand = (rng.random((self.length, bank.n_units(agent)), dtype=np.float32)
                    if bank.kinds[agent] != "stage" else None)
            d = {"task": task, "coin": coin, "rand": rand, "knob": np.full(self.length, -1, dtype=np.int64),
                 "outcome": np.zeros(self.length, dtype=np.uint8), "used": np.zeros(self.length, dtype=bool)}
            self.store[agent] = d
        return d

    def outcomes(self, agent: int, idx: np.ndarray, targets: np.ndarray) -> np.ndarray:
        bank = self.s.bank
        d = self.data(agent)
        tasks = d["task"][idx]
        cells = bank.ctx_bins[tasks, agent] if self.s.use_cells else None
        knobs = bank.targets_to_knobs(agent, targets, d["coin"][idx], cells=cells)
        rand = None if d["rand"] is None else d["rand"][idx]
        y, _ = bank.sample_many(agent, tasks, knobs, rand=rand, rng=self.s.rng_fallback)
        d["knob"][idx] = knobs
        d["outcome"][idx] = y
        d["used"][idx] = True
        return y


class _BidTape(_PhaseTape):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            i, r = key
            return _Cell(self, int(i), int(r))
        return _Row(self, int(key), 0, self.horizon)


class _PrimaryTape(_PhaseTape):
    """Bound to the agent the mechanism selected; the binding is checked against the mechanism's own winner."""

    def __init__(self, session, phase, length, seed, agent):
        super().__init__(session, phase, length, seed)
        self.agent = int(agent)

    def __len__(self):
        return self.horizon

    def __lt__(self, m):
        return _Row(self, self.agent, 0, self.horizon) < m

    def __getitem__(self, key):
        return _Row(self, self.agent, 0, self.horizon)[key]


class _FallbackTape(_PhaseTape):
    def __getitem__(self, key):
        if not isinstance(key, tuple):
            raise ValueError("the fallback tape is indexed by (round, agent)")
        t, a = key
        if isinstance(t, slice):
            s, e, step = t.indices(self.horizon)
            if step != 1:
                raise ValueError("strided tape slices are not supported")
            return _Row(self, int(a), s, e)
        return _Cell(self, int(a), int(t))


class _Source:
    def __init__(self, session, phase):
        self.s, self.phase = session, phase

    def random(self, shape, dtype=None):
        return self.s.make_tape(self.phase, shape)


class _RecordingGen:
    """Passes the mechanism's own randomness through unchanged and records the uniform tie priority."""

    def __init__(self, gen):
        self.gen = gen
        self.first_permutation = None

    def permutation(self, x):
        p = self.gen.permutation(x)
        if self.first_permutation is None:
            self.first_permutation = np.asarray(p).copy()
        return p

    def __getattr__(self, name):
        return getattr(self.gen, name)


class _Session:
    def __init__(self, bank: B.ResponseBank, inst, d, gens, use_cells: bool):
        self.bank, self.inst, self.d, self.use_cells = bank, inst, d, use_cells
        self.seed = {ph: int(gens[ph].integers(1 << 62)) for ph in ("bid", "primary", "fallback")}
        self.rng_fallback = np.random.default_rng([self.seed["bid"], 9999])
        self.mech = _RecordingGen(gens["mechanism"])
        self.tapes: dict[str, _PhaseTape] = {}
        self.inferred_winner = None

    def make_tape(self, phase: str, shape):
        K, L, N = self.inst.K, self.d.L, self.d.N
        if phase == "bid":
            tape = _BidTape(self, "bid", int(shape[1]), self.seed["bid"])
        elif phase == "primary":
            w = self.winner()
            tape = _PrimaryTape(self, "primary", int(shape), self.seed["primary"], w)
        else:
            tape = _FallbackTape(self, "fallback", N, self.seed["fallback"], horizon=int(shape[0]))
        self.tapes[phase] = tape
        return tape

    def beta(self) -> np.ndarray:
        bid = self.tapes["bid"]
        return np.array([bid.data(i)["outcome"].sum() for i in range(self.inst.K)], dtype=float) / self.d.L

    def winner(self) -> int:
        """The mechanism's selection rule, recomputed from the Stage-1 outcomes and the recorded priority."""
        K = self.inst.K
        beta = self.beta()
        priority = self.mech.first_permutation
        if priority is None:
            raise RuntimeError("the uniform tie priority has not been drawn yet")
        rank = np.empty(K, dtype=int)
        rank[priority] = np.arange(K)
        order = sorted(range(K), key=lambda i: (-beta[i], rank[i]))
        self.inferred_winner = int(order[0])
        return self.inferred_winner

    # ================================================================ reporting

    def extras(self, out: dict) -> dict:
        K = self.inst.K
        bid = self.tapes["bid"]
        bid_rec = {k: [bid.data(i)[k] for i in range(K)] for k in ("task", "knob", "rand", "outcome")}
        cost_bid = np.array([np.maximum(bid.data(i)["knob"], 0).sum() for i in range(K)], dtype=np.int64)
        out_sum = int(sum(int(bid.data(i)["outcome"].sum()) for i in range(K)))
        q = int(out["primary_rounds"])
        pri = self.tapes.get("primary")
        if pri is None:
            pri_rec = {k: np.zeros(0) for k in ("task", "knob", "rand", "outcome")}
            cost_pri = 0
        else:
            dp = pri.data(pri.agent)
            pri_rec = {k: dp[k] for k in ("task", "knob", "rand", "outcome")}
            cost_pri = int(np.maximum(dp["knob"][:q], 0).sum())
            out_sum += int(dp["outcome"][:q].sum())
        fb = self.tapes.get("fallback")
        cost_fb = 0
        fb_rec = {}
        if fb is not None:
            for i in range(K):
                if i not in fb.store:
                    continue
                df = fb.store[i]
                u = df["used"]
                cost_fb += int(np.maximum(df["knob"][u], 0).sum())
                out_sum += int(df["outcome"][u].sum())
                fb_rec[i] = {k: df[k] for k in ("task", "knob", "outcome", "used")}
        knobs_played = np.concatenate([np.maximum(bid.data(i)["knob"], 0) for i in range(K)] +
                                      ([np.maximum(pri_rec["knob"][:q], 0)] if pri is not None else []))
        return {"inferred_winner": self.inferred_winner, "beta_check": list(self.beta()),
                "compute_cost_bid": cost_bid, "compute_cost_primary": cost_pri, "compute_cost_fallback": cost_fb,
                "compute_cost": int(cost_bid.sum()) + cost_pri + cost_fb,
                "rounds_evaluated": int(out["stage1_rounds"] + out["primary_rounds"] + out["fallback_rounds"]),
                "outcome_sum": out_sum, "mean_knob_played": float(knobs_played.mean()),
                "records": {"bid": bid_rec, "primary": pri_rec, "fallback": fb_rec}}


def episode_on_bank(bank: B.ResponseBank, inst, n: int, variant: M.Variant, policies, gens,
                    use_cells: bool = False):
    """One MESP episode whose rewards are real provider answers. Returns (mechanism row, bank extras)."""
    d = make_design(n, inst.K, L=variant.L)
    sess = _Session(bank, inst, d, gens, use_cells)
    gens2 = {"bid": _Source(sess, "bid"), "primary": _Source(sess, "primary"),
             "fallback": _Source(sess, "fallback"), "mechanism": sess.mech, "deviation": gens["deviation"]}
    out = M.episode(inst, n, variant, policies, gens2)
    extras = sess.extras(out)
    if extras["inferred_winner"] != out["winner"]:
        raise AssertionError(f"tape bound to agent {extras['inferred_winner']} but the mechanism selected "
                             f"{out['winner']}; the adapter and the mechanism disagree")
    # The session and its tapes reference each other, and a tape holds one float32 row of tree-ordering
    # randomness per round per agent, which is hundreds of megabytes at large n. The cyclic collector would
    # free them eventually, but its trigger counts objects rather than bytes, so a long sweep can hold many
    # episodes' tapes at once. Breaking the cycle here makes every episode's tapes fall at once, except the
    # arrays the returned records deliberately keep alive.
    for tape in sess.tapes.values():
        tape.s = None
    sess.tapes.clear()
    extras["released"] = True
    return out, extras
