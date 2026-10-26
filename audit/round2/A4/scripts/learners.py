"""Learning providers: every strategic provider runs EXP3 over an effort grid.

Decisions fixed by the main agent (28 Sep 2026):
  * arms theta in {0, 0.1, ..., 1}; delivered mean m = floor + theta (M_i(x) - floor)
    with the strategic floor 0 (Section 2 lets a strategic provider deliver
    anything in [0, M_i(x)]);
  * one EXP3 learner per (provider, phase), shared across task types; the phase
    is the strategy-facing name the rule passes (elicit / primary / fallback for
    our mechanisms, Cao's explore / exploit / blind mapped the same way through
    SB_PHASE, route for routers and the audit router);
  * epochs of n / 2000 rounds (2,000 updates per learner; changed from n / 200
    on 28 Sep because 200 updates over 11 arms are too few to learn); at each epoch start every learner draws an
    arm, and at its end every learner that was used is credited with its
    provider's utility per round over the epoch, so traffic lost counts 0;
  * the honest provider (Mixtral-8x7B) stays at its floor mu and does not learn.

OBSERVATION MODEL (author's specification, 28 Sep 2026, binding). A learning
provider observes ONLY
  (i)   its own history: its own targets, its own realised utility, and any
        message the mechanism sends to it (the announced price when it is the
        selected winner, passed as `price`), plus the task type and its own
        capability / intrinsic level at the prompt it is serving;
  (ii)  for every round, whether or not it was chosen;
  (iii) the round number t.
Nothing about other providers and no mechanism internals. This is enforced by
construction: each provider has its own `ProviderLearner` holding only its own
state, and the `Learner` dispatcher gives it exactly (i) when it is selected
and (ii)+(iii) on every round via `tick(t, chosen)`. No object is shared
between providers.

THE CLOCK. The dispatcher advances t once per delegated round, i.e. once per
call of `target`, which every rule makes exactly once per delegated round. It
equals the global round until a rule stops delegating (Cao after its monitor
fires, the one-observation rule once all are excluded); after that no provider
is chosen or earns anything, so no learner has anything left to learn. Knowing
t makes the learners STRONGER than the model's blind providers (Section 2).
"""
import numpy as np

ARMS = np.round(np.linspace(0.0, 1.0, 11), 2)
N_EPOCHS = 2000
ETA_MULT = 5.0     # learning-rate multiplier on the EXP3 update; tuned on the B2 toy ONLY (swept
                   # 1, 5, 20, 80; 5 came closest to the known router outcome), frozen 28 Sep 2026
SETTLE_FRAC, SETTLE_TV = 0.10, 0.05
CONCENTRATION = 0.5   # a near-uniform learner also has small TV change; require a dominant arm too
SCHEDULE = "fixed"   # "fixed": the 28 Sep learner (constant gamma, the "naive learners" robustness check);
                     # "decay": anytime EXP3, gamma_e = eta_e = min(1, sqrt(A ln A / ((e - 1)(e + 1))))
                     # at epoch e = 0, 1, ..., weights exp(ETA_MULT * eta_e * S_hat / A) on the cumulative
                     # importance-weighted reward S_hat (author's choice (a), 29 Sep 2026)
OBSERVATION_MODEL = ("own targets, own realised utility, messages addressed to it (price when "
                     "selected winner), own capability/intrinsic level at the prompt it serves; "
                     "chosen-or-not every round; the round number t. Nothing about other providers "
                     "or mechanism internals.")


class ProviderLearner:
    """One provider's learners, one EXP3 per phase. Sees only its own data."""

    def __init__(self, phases, n_epochs, epoch_len, rng, eta_mult, schedule="fixed"):
        self.phases = list(phases)
        self.epoch_len = epoch_len
        self.schedule = schedule
        self.S = {ph: np.zeros(len(ARMS)) for ph in phases}   # cumulative reward estimates ("decay")
        self.gamma = float(min(1.0, np.sqrt(len(ARMS) * np.log(len(ARMS))
                                            / ((np.e - 1) * n_epochs))))
        self.eta_mult = eta_mult
        self.w = {ph: np.ones(len(ARMS)) for ph in self.phases}
        self.rng = rng
        self.log = []
        self._draw()

    def _gamma_e(self):
        if self.schedule == "fixed":
            return self.gamma
        A, e = len(ARMS), len(self.log)
        return float(min(1.0, np.sqrt(A * np.log(A) / ((np.e - 1) * (e + 1)))))

    def _draw(self):
        self.p = {}
        self.arm = {}
        g = self._gamma_e()
        for ph, w in self.w.items():
            if self.schedule == "decay":
                z = self.eta_mult * g * self.S[ph] / len(ARMS)
                w = np.exp(z - z.max())
            p = (1 - g) * w / w.sum() + g / len(ARMS)
            self.p[ph] = p
            self.arm[ph] = int(self.rng.choice(len(ARMS), p=p))
        self.used = set()
        self.util = 0.0
        self.chosen = 0

    def act(self, phase, M_own, mu_own, price):
        """(i): called only when this provider is selected."""
        ph = phase if phase in self.w else "route"
        self.used.add(ph)
        m = ARMS[self.arm[ph]] * M_own
        self.util += 1.0 + mu_own - m               # its own utility this round
        return m

    def tick(self, t, chosen):
        """(ii) + (iii): every round."""
        self.chosen += int(chosen)
        if (t + 1) % self.epoch_len == 0:
            r = self.util / self.epoch_len / 2.0     # utility per round, scaled to [0, 1]
            for ph in self.used:
                a = self.arm[ph]
                if self.schedule == "decay":
                    self.S[ph][a] += r / self.p[ph][a]
                    continue
                self.w[ph][a] *= np.exp(self.eta_mult * self.gamma * (r / self.p[ph][a]) / len(ARMS))
                if self.w[ph].max() > 1e200:
                    self.w[ph] /= self.w[ph].max()
            self.log.append({"epoch": len(self.log), "reward": round(2 * r, 5),
                             "chosen_rounds": self.chosen,
                             "gamma": round(self._gamma_e(), 5),
                             "arms": {ph: float(ARMS[a]) for ph, a in self.arm.items()},
                             "used": sorted(self.used),
                             "probs": {ph: np.round(p, 3).tolist() for ph, p in self.p.items()}})
            self._draw()


class Learner:
    """Dispatcher with the strategy interface every rule calls."""

    def __init__(self, inst, n, seed, n_epochs=N_EPOCHS, phases=None, eta_mult=None, schedule=None):
        self.inst = inst
        self.epoch_len = max(1, int(n // n_epochs))
        phases = phases or ["elicit", "primary", "fallback", "route"]
        root = np.random.default_rng(424242 + seed)
        self.eta_mult = ETA_MULT if eta_mult is None else float(eta_mult)
        self.schedule = SCHEDULE if schedule is None else schedule
        self.agents = {i: ProviderLearner(phases, n_epochs, self.epoch_len,
                                          np.random.default_rng(root.integers(2 ** 63)), self.eta_mult,
                                          self.schedule)
                       for i in range(inst.K) if not inst.honest[i]}
        self.t = 0

    def target(self, i, phase, q, price, state=None):
        inst = self.inst
        M, mu = float(inst.M[q, i]), float(inst.mu[q, i])
        if i in self.agents:
            m = self.agents[i].act(phase, M, mu, price)
        else:
            m = mu                                    # honest provider at its floor
        for j, a in self.agents.items():
            a.tick(self.t, j == i)
        self.t += 1
        return m

    @property
    def log(self):
        return {str(i): a.log for i, a in self.agents.items()}

    def convergence(self):
        """Per (provider, phase) that was ever used: total-variation distance between
        its arm distribution at the start of the last SETTLE_FRAC of epochs and at the
        end. Converged only if every such learner moves less than SETTLE_TV AND ends with
        some arm of probability >= CONCENTRATION (a learner that never left the uniform
        distribution also moves little, and must not count as settled)."""
        out, ok = {}, True
        for i, a in self.agents.items():
            E = len(a.log)
            if E < 10:
                out[str(i)] = "too few epochs"
                ok = False
                continue
            e0 = int((1 - SETTLE_FRAC) * E)
            for ph in a.phases:
                if not any(ph in rec["used"] for rec in a.log[e0:]):
                    continue
                p0 = np.asarray(a.log[e0]["probs"][ph])
                p1 = np.asarray(a.log[-1]["probs"][ph])
                tv = 0.5 * float(np.abs(p1 - p0).sum())
                out.setdefault(str(i), {})[ph] = {"tv": round(tv, 4), "p_max": round(float(p1.max()), 3),
                                                  "mode_arm": float(ARMS[int(np.argmax(p1))])}
                ok = bool(ok and tv < SETTLE_TV and p1.max() >= CONCENTRATION)
        return ok, out

    def meta(self):
        g = next(iter(self.agents.values())).gamma if self.agents else None
        conv, tv = self.convergence()
        return {"learner": "EXP3 per (provider, phase)", "arms": ARMS.tolist(),
                "epoch_len_rounds": self.epoch_len, "gamma": g, "schedule": self.schedule,
                "observation_model": OBSERVATION_MODEL, "eta_mult": self.eta_mult,
                "converged": conv, "settle_tv": tv,
                "settle_rule": f"TV over last {SETTLE_FRAC:.0%} of epochs < {SETTLE_TV} and max arm prob >= {CONCENTRATION}",
                "clock": "delegated rounds; equals t until a rule stops delegating; "
                         "stronger than the model's blind providers",
                "epochs": self.log}


# --------------------------------------------------------------------------- #
# Learning across repeated runs (author's decision, 29 Sep 2026).
# Within one run PL-MESP's elicitation happens once and conviction is permanent, so
# no within-run schedule can learn them (toy, 29 Sep: decaying EXP3 fixed the UCB
# router toy but not PL-MESP). Here every strategic provider plays E independent
# runs ("episodes") of the same rule. Its EXP3 learner per phase persists across
# episodes; within an episode it holds one arm per phase (a stationary policy),
# and at the episode's end every phase it used is credited with its utility per
# round over the whole episode (lost traffic counts 0), so a lost elicitation or a
# conviction is charged to the arm that caused it. Exploration decays over
# episodes (anytime EXP3, SCHEDULE "decay"). The rule itself restarts from scratch
# every episode, identically for every rule. Observation model unchanged.
# --------------------------------------------------------------------------- #
class EpisodicLearner:
    """Persistent learners; call new_episode(n) before each run, end_episode() after."""

    def __init__(self, inst, n_episodes, seed, phases=None, eta_mult=None):
        self.inst = inst
        self.n_episodes = n_episodes
        phases = phases or ["elicit", "primary", "fallback", "route"]
        root = np.random.default_rng(525252 + seed)
        self.eta_mult = ETA_MULT if eta_mult is None else float(eta_mult)
        self.agents = {i: ProviderLearner(phases, n_episodes, 1,
                                          np.random.default_rng(root.integers(2 ** 63)),
                                          self.eta_mult, "decay")
                       for i in range(inst.K) if not inst.honest[i]}
        self.n = None
        self.episode = 0

    def new_episode(self, n):
        self.n = int(n)
        self.t = 0
        for a in self.agents.values():
            a.used, a.util, a.chosen = set(), 0.0, 0

    def target(self, i, phase, q, price, state=None):
        inst = self.inst
        M, mu = float(inst.M[q, i]), float(inst.mu[q, i])
        if i in self.agents:
            m = self.agents[i].act(phase, M, mu, price)
            self.agents[i].chosen += 1
        else:
            m = mu
        self.t += 1
        return m

    def end_episode(self):
        for a in self.agents.values():
            a.epoch_len = self.n              # credit = utility per round over the episode
            a.tick(self.n - 1, False)         # (n - 1 + 1) % n == 0: update, log, redraw
        self.episode += 1

    @property
    def log(self):
        return {str(i): a.log for i, a in self.agents.items()}

    def convergence(self):
        return Learner.convergence(self)

    def meta(self):
        conv, tv = self.convergence()
        return {"learner": "episodic EXP3 per (provider, phase), decaying exploration",
                "arms": ARMS.tolist(), "episodes": self.n_episodes, "episode_len_rounds": self.n,
                "observation_model": OBSERVATION_MODEL, "eta_mult": self.eta_mult,
                "converged": conv, "settle_tv": tv,
                "settle_rule": f"TV over last {SETTLE_FRAC:.0%} of episodes < {SETTLE_TV} and max arm prob >= {CONCENTRATION}",
                "epochs": self.log}
