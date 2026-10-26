# Agent B (sim-core): learning providers, audit-and-ban, v3 driver

STATUS: IN PROGRESS 2026-09-28T16:59:45Z

## Milestones
- [x] B1 learners.py, run_router_audit, run_v3.py (28 Sep)
- [x] B2 sanity checks (28 Sep; results below)
- [~] B3 grids: items 1 (bridge) and 3 launched 28 Sep as job 65007446 (1,580 tasks, cpu-preempt); item 1/3 real-order tasks (300) auto-submit when the queue has room; item 2 HELD
- [ ] B4 aggregate + figures

## Fixed decisions (from main agent)
Learning: EXP3 over theta in {0,...,1}, m = floor + theta (M - floor), strategic floor 0; one learner per
(provider, phase) shared across task types; epochs of ~n/200 global rounds; reward = utility per global round
over the epoch. Uses the global clock: learners are STRONGER than the model's blind agents.
Honest Mixtral-8x7B at its floor mu in every rule.
Audit-and-ban: per-type UCB router + anytime-valid sequential test per (provider, type), delta in {0.02,0.05},
false-alarm 1/n, permanent ban. Reference: SELF only (own first ceil(4 log n) selections at that type).

## Learner observation model (author, 28 Sep, binding)
A learning provider observes ONLY (i) its own history: its own targets, own realised utility, messages the
mechanism sends to it (the announced price when it is the selected winner), and its own capability and
intrinsic level at the prompt it serves; (ii) for every round, whether or not it was chosen; (iii) the round
number t. Nothing about other providers, no mechanism internals. Enforced by construction in
`learners.py`: one `ProviderLearner` per provider holding only its own state; the `Learner` dispatcher
passes (i) on selection and (ii)+(iii) every round via `tick(t, chosen)`. The same text is written to every
learning trace's meta (`strategy.observation_model`).
Clock caveat: t advances once per delegated round; it equals the global round until a rule stops
delegating (Cao after its monitor fires, the one-observation rule once all are excluded), after which no
provider earns anything.

## Changes to the brief
- 28 Sep (main agent): epochs n/2000 rounds (2,000 updates per learner), not n/200. Convergence
  diagnostic: each learner's arm distribution per epoch in the trace meta; a run counts as settled if
  every used (provider, phase) learner moves < 0.05 in total variation over the last 10% of epochs;
  cells report `converged_share`, and unsettled cells are labelled NOT CONVERGED, never presented as
  equilibria. The EXP3 learning rate may be tuned on the B2 two-provider toy ONLY, then frozen
  (`learners.ETA_MULT`) for every real run.
- 28 Sep (author, via coordinator): the benchmark-referenced audit variant is DROPPED. No baseline gets
  information the model says the platform lacks. router_audit runs with the self reference only.

## B1. Code (28 Sep)
- `audit/round2/A4/scripts/learners.py`: `Learner` dispatcher + one `ProviderLearner` per strategic provider
  (EXP3 per phase, 11 arms, epochs n/2000, ETA_MULT = 5 frozen, convergence diagnostic).
- `mechanisms.run_router_audit`: addition only, trace hook. UCB per type + per-(provider, type) test with SELF
  reference over the first ceil(4 log n) selections at that type; ban when S < -sqrt(r c) - r rad,
  c = (log 2 + 2 log n)/2 (anytime Hoeffding, union over r <= n), rad = sqrt(log(2nKQ)/(2 warm)) (the
  reference's own estimation error, union over all (provider, type)). Both terms are needed for the 1/n
  false-alarm level the brief fixes. At n = 3e5-3e6 with warm = 51-60, rad = 0.40.
- `run_v3.py`: v2 (rule, profile) pairs delegate to the unchanged v2 `one_run`; new: `learning` for every rule,
  `router_audit_d002/_d005` with profiles exploit_slow, exploit_fast, average, evade, learning;
  `--taskset q7|merged5`; `--orders ... ,real` (Agent A's stream; seed = start offset; never tiled).
  evade = capability for the first `warm` selections at a type (sets the reference), then
  max(0, M - delta - rad + 3 * 0.5/sqrt(warm)): the most shading the test cannot see, backed off by three
  reference standard errors.

## B2. Sanity checks (28 Sep)
**(a) v2 reproduction: PASS, exact.** k4_q90, q7, n = 3e5, bursty, 20 seeds: run_v3 equals v2 to every digit
for plmesp_star 0.666966, plmesp_low 0.408039, cao_eq0 0.181632, cao_eqmu 0.510728, UCB exploit_slow
0.502526, UCB average 0.655757, esmaeili 0.000055.

**(b) two-provider toy (`toy_learners.py`): the known outcome is NOT reached, for structural reasons.**
One type; A strategic (M 0.9, mu 0.3); H honest at 0.42. Known stationary answer in both rules: A's
route/primary arm theta = 0.5 (m = 0.45, the cheapest arm beating 0.42 and meeting the price 0.386).
Learning-rate sweep on the toy (n = 1e6, mode arm / its probability):

| ETA_MULT | UCB router | PL-MESP primary | PL-MESP convictions |
|---|---|---|---|
| 1 | 0.1-0.5 / 0.10-0.16 (near uniform) | 0.0-0.1 / 0.09-0.23 | 3 of 3 seeds |
| 5 | 0.6 / 0.29, 0.5 / 0.41 | 0.1 / 0.17, 0.0 / 0.28 | 2 of 2 |
| 20 | 0.2 / 0.48, 0.1 / 0.41 | 0.0 / 0.09, 0.2 / 0.89 | 1 of 2 |
| 80 | 0.0 / 0.92, 0.3 / 0.92 | 0.0 / 0.09, 0.2 / 0.92 | 1 of 2 |

Revenue is ~0.42 (the honest level) in every cell. Two reasons, neither a learning-rate problem:
1. The UCB router ranks A by its CUMULATIVE mean, so shading in one epoch barely moves this epoch's traffic;
   per epoch, shading pays. Faster learners therefore converge to shading, not to the stationary answer.
2. PL-MESP's conviction is permanent: EXP3's forced exploration eventually plays a low primary arm, the
   monitor convicts, and that type stays in fallback for the rest of the horizon.
ETA_MULT = 5 frozen (closest to the known router outcome). This is recorded as a FAILED sanity check, not
papered over: learning results must be read as "what EXP3 learners do", not as equilibria.
Convergence rule tightened: settled = TV < 0.05 over the last 10% of epochs AND a dominant arm (p >= 0.5);
without the second condition a learner that never left uniform counts as settled (seen at ETA_MULT = 1).

**(c) audit false bans: PASS; audit power: very low.** 5 subsets x 2 deltas x 10 seeds, n = 3e5, shuffled:
average-profile (constant, compliant) providers and the honest provider: 0 bans in 100 runs. evade: 0 bans
(as designed). exploit_slow: 1 ban in 100 runs. With a 60-selection self reference, holding false alarms at
1/n needs rad = 0.40 >> delta, and UCB stops selecting a provider whose quality falls, so the test never
gets the evidence. A faithful self-referenced audit at the brief's false-alarm level is close to powerless.
Not loosened: that would be tuning a baseline.

## Infrastructure change
- 28 Sep (main agent): all arrays on `--partition=cpu-preempt` with `--requeue` (cpu estimated start ~2 Oct);
  tasks idempotent (outputs overwritten), single tasks < ~1 h; 3e7 cells sharded by seed.

## ITEM 2 ON HOLD (main agent, 28 Sep)
The item 2 learning grid is HELD pending the author's decision on the learner design after the failed toy.
**No item 2 task was ever submitted** (the one array attempt was rejected by the submit limit before
anything ran; the held task list is `tasks_v3_main_i2_HELD.txt`, 1,170 tasks).
**EXP3 exploration schedule in use: FIXED, not decaying.** gamma = sqrt(A ln A / ((e - 1) E)) with A = 11 arms
and E = 2,000 epochs, i.e. gamma = 0.088 for the whole run (uniform mixing weight gamma/A = 0.008 per arm), and
the weight update exp(ETA_MULT * gamma * r_hat / A) with ETA_MULT = 5, also fixed. The forced exploration never
decays, which is why PL-MESP learners eventually play a low primary arm and are convicted (toy, B2(b)).

## B3. Pre-registered grids (written 28 Sep, before any grid run)
Subsets: the 10 of `arrival_order_subsets_v2.txt`. Honest Mixtral at mu; everything else as in the brief.
Taskset q7 for the synthetic orders (comparable with v2); merged5 for `real` (Agent A's stream is in the
five merged types), plus merged5 shuffled as the bridge between the two tasksets.
- **Item 2 (learning)**, all 9 rules (plmesp, mesp_scalar, second_best, router_greedy, router_eps,
  router_ucb, esmaeili, router_audit_d002, router_audit_d005) x profile `learning`:
  q7 {iid, bursty} at 3e6, 10 seeds; q7 iid at 3e7, 10 seeds; merged5 {iid, real} at 3e6, 10 seeds.
- **Item 3 (audit)**, router_audit_d002/_d005 x {exploit_slow, exploit_fast, average, evade}:
  q7 {iid, bursty, drift, grouped} at 3e5 and 3e6, 20 seeds; q7 {iid, bursty} at 3e7, 5 seeds;
  merged5 real at 3e5 and 3e6, 20 seeds.
- **Item 1 (real order)**, every v2 rule x profile (plmesp_star, plmesp_low, mesp_star, cao_eq0, cao_eqmu,
  router x {exploit_slow, exploit_fast, average}, esmaeili proposed): merged5 {iid, real} at 3e5 and 3e6,
  20 seeds.
Every run keeps a full per-round trace under <workspace>/v3/B/.
Reported per cell: revenue, sd, fire rate, undelegated share, converged share (learning), per-provider utility.

## B3 launch notes (28-29 Sep)
- Task sizing: on cpu-preempt nodes a run is ~3x slower than on the login node (3e5 audit run ~18 s), so
  item 3 is one task per (subset, rule, profile, order, horizon) and 3e7 per seed; item 1 per rule.
- Submit limit: QOS `normal` allows 2,000 queued jobs per user (Agent C holds ~134), hence item 1/3 first
  (1,580) and the 300 real-order tasks queued behind them automatically.
- Real stream: Agent A's `<workspace>/real_sequences/wildchat48m_all.npz`
  (5,167,182 user turns, WildChat-4.8M, all languages; keys `type`, `types`, `timestamp`). A 3e6 window
  covers ~58% of the stream, so windows from different seeds overlap heavily: seeds vary the start, not an
  independent sample of traffic.
- **Caveat for the main agent:** in the real stream open_chat is ~54% of prompts (0.48 over the whole
  stream), and the open_chat capability comes from RouterBench's 80 MT-Bench rows, the family A4 found does
  NOT reproduce the published means. Real-order revenue therefore leans on the weakest capability estimate.
