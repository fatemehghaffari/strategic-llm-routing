"""Stage 6: aggregate tables, paired bootstrap intervals and Figures 1-5 from the request-level records.

    python analyze.py --fixed <dir with seed*/requests.csv> [--policies <dir>] --out results/aggregate --figs figures

Statistics. Accuracy intervals are question-level bootstrap percentiles (B = 2000 resamples of questions
with replacement, generations of the same question kept together across seeds). Differences between
budgets or policies are PAIRED: each resample draws questions, and the difference of the two conditions'
per-question mean correctness is averaged over the draw. Malformed, truncated and missing answers count
as wrong and are also reported separately. Latency is the batch wall time attributed to a request by its
share of the batch's output tokens (vLLM serves a whole batch at once); it is a relative computation
proxy, not a monetary cost. Energy (if gpu_power.csv exists): power integrated over the batch window
minus the idle power measured for 20 s before the model loaded, attributed by output-token share.
"""
import argparse, glob, json, os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

LEVELS = ["low", "medium", "high"]
SUB_ORDER = ["gsm8k_short", "gsm8k_long", "math_easy", "math_medium", "math_hard"]
SUB_LABEL = {"gsm8k_short": "GSM8K, short solution", "gsm8k_long": "GSM8K, long solution", "math_easy": "MATH-500, level 1-2", "math_medium": "MATH-500, level 3", "math_hard": "MATH-500, level 4-5"}
SUB_SHORT = {"gsm8k_short": "GSM8K\nshort", "gsm8k_long": "GSM8K\nlong", "math_easy": "MATH\nlevel 1-2", "math_medium": "MATH\nlevel 3", "math_hard": "MATH\nlevel 4-5"}
# one hue per benchmark, lighter -> darker with difficulty (sequential within a benchmark), validated palette hues
HUE = {"gsm8k_short": "#7fb2ea", "gsm8k_long": "#2a78d6", "math_easy": "#f5a989", "math_medium": "#eb6834", "math_hard": "#a8431a"}
LEVEL_HUE = {"low": "#9ec3ee", "medium": "#4f93df", "high": "#1b5bb0"}     # one hue, light -> dark with budget
POL_HUE = {"fixed_low": "#1b5bb0", "fixed_medium": "#1b5bb0", "fixed_high": "#1b5bb0", "task_adaptive": "#eb6834", "random_matched": "#8a8a8a"}
POL_LABEL = {"fixed_low": "fixed low", "fixed_medium": "fixed medium", "fixed_high": "fixed high", "task_adaptive": "task-adaptive", "random_matched": "random, matched proportions"}
INK, INK2, MUTED, GRID, PALE = "#1b1b1b", "#4a4a4a", "#8a8a8a", "#e3e3e0", "#c9c9c6"
B = 2000

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=7, length=3, width=0.8); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)

def load_dir(d):
    fs = sorted(glob.glob(os.path.join(d, "seed*", "requests.csv")))
    if not fs: return None
    df = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
    df["correct"] = df.correct.astype(bool)
    # arrival order of each request in the policy run, from the gateway logs (one row per request, in stream order)
    arr = {}
    for f in sorted(glob.glob(os.path.join(d, "seed*", "gateway_log_*_seed*.csv"))):
        base = os.path.basename(f)[len("gateway_log_"):-4]; pol, sd = base.rsplit("_seed", 1)
        for i, rid in enumerate(pd.read_csv(f).request_id): arr[(pol, int(sd), rid)] = i
    if arr: df["arrival"] = [arr.get((p_, int(s_), t_), np.nan) for p_, s_, t_ in zip(df.policy, df.seed, df.task_id)]
    return df

# ---------------------------------------------------------------- bootstrap --
def per_question(df, cond_col, cond, value="correct"):
    """mean over seeds of `value`, per task_id, for one condition"""
    s = df[df[cond_col] == cond].groupby("task_id")[value].mean()
    return s

def boot_mean(x, rng, b=B):
    x = np.asarray(x, float); n = len(x)
    idx = rng.integers(0, n, size=(b, n)); return x[idx].mean(1)

def ci(samples, level=0.95):
    lo, hi = np.percentile(samples, [(1 - level) / 2 * 100, (1 + level) / 2 * 100]); return float(lo), float(hi)

def acc_ci(df, cond_col, cond, rng):
    q = per_question(df, cond_col, cond); s = boot_mean(q.values, rng); return float(q.mean()), *ci(s), len(q)

def diff_ci(df, cond_col, a, b_, rng):
    qa, qb = per_question(df, cond_col, a), per_question(df, cond_col, b_)
    common = qa.index.intersection(qb.index); d = (qa[common] - qb[common]).values
    s = boot_mean(d, rng); return float(d.mean()), *ci(s), len(common)

# ---------------------------------------------------------------- energy --
def attach_energy(df, d):
    """Adds energy_j per request from <seed dir>/gpu_power.csv, when present."""
    df["energy_j"] = np.nan; df["idle_power_w"] = np.nan
    for sd in sorted(glob.glob(os.path.join(d, "seed*"))):
        f = os.path.join(sd, "gpu_power.csv")
        if not os.path.exists(f): continue
        try:
            p = pd.read_csv(f, header=None, names=["ts", "power_w", "util", "mem"], on_bad_lines="skip")
            p["t"] = (pd.to_datetime(p.ts.str.strip(), format="%Y/%m/%d %H:%M:%S.%f") - pd.Timestamp("1970-01-01")) / pd.Timedelta("1s")   # epoch seconds; the node clock is UTC
            p = p.dropna(subset=["power_w"]); p["power_w"] = p.power_w.astype(float)
        except Exception as e:
            print("power log unreadable:", f, e); continue
        idle = float(p.power_w.iloc[:18].mean())            # the first 20 s, before the model loads
        seed = int(os.path.basename(sd)[4:])
        m = df.seed == seed
        for (t0, t1), g in df[m].groupby(["batch_t0", "batch_t1"]):
            w = p[(p.t >= t0) & (p.t <= t1)]
            if len(w) < 2: continue
            e = float(np.trapezoid(np.clip(w.power_w - idle, 0, None), w.t))     # joules above idle over the batch
            share = g.total_output_tokens / g.total_output_tokens.sum()
            df.loc[g.index, "energy_j"] = e * share.values; df.loc[g.index, "idle_power_w"] = idle
    return df

# ---------------------------------------------------------------- tables --
def level_tables(df, rng, out):
    rows = []
    for (bench, lvl), g in df.groupby(["benchmark", "level"]):
        m, lo, hi, nq = acc_ci(g, "level", lvl, rng)
        rows.append(dict(scope=bench, subgroup="all", level=lvl, n_questions=nq, n_generations=len(g), accuracy=m, acc_lo=lo, acc_hi=hi,
                         reasoning_tokens=g.reasoning_tokens.mean(), reasoning_tokens_sd=g.reasoning_tokens.std(), answer_tokens=g.answer_tokens.mean(),
                         total_output_tokens=g.total_output_tokens.mean(), latency_s=g.est_wall_s.mean(), latency_s_p90=g.est_wall_s.quantile(0.9),
                         energy_j=g.energy_j.mean() if "energy_j" in g else np.nan, budget_exhausted=g.budget_exhausted.mean(), truncated=g.truncated.mean(), malformed=g.malformed.mean(),
                         seed_acc_sd=g.groupby("seed").correct.mean().std()))
    for (sub, lvl), g in df.groupby(["subgroup", "level"]):
        m, lo, hi, nq = acc_ci(g, "level", lvl, rng)
        rows.append(dict(scope=g.benchmark.iloc[0], subgroup=sub, level=lvl, n_questions=nq, n_generations=len(g), accuracy=m, acc_lo=lo, acc_hi=hi,
                         reasoning_tokens=g.reasoning_tokens.mean(), reasoning_tokens_sd=g.reasoning_tokens.std(), answer_tokens=g.answer_tokens.mean(),
                         total_output_tokens=g.total_output_tokens.mean(), latency_s=g.est_wall_s.mean(), latency_s_p90=g.est_wall_s.quantile(0.9),
                         energy_j=g.energy_j.mean() if "energy_j" in g else np.nan, budget_exhausted=g.budget_exhausted.mean(), truncated=g.truncated.mean(), malformed=g.malformed.mean(),
                         seed_acc_sd=g.groupby("seed").correct.mean().std()))
    T = pd.DataFrame(rows); T.to_csv(os.path.join(out, "table_A_levels.csv"), index=False)
    # paired differences between budgets
    rows = []
    for scope_col, scopes in (("benchmark", sorted(df.benchmark.unique())), ("subgroup", [s for s in SUB_ORDER if s in set(df.subgroup)])):
        for sc in scopes:
            g = df[df[scope_col] == sc]
            for a, b_ in (("medium", "low"), ("high", "medium"), ("high", "low")):
                dm, lo, hi, nq = diff_ci(g, "level", a, b_, rng)
                ta, tb = g[g.level == a].reasoning_tokens.mean(), g[g.level == b_].reasoning_tokens.mean()
                rows.append(dict(scope=sc, contrast=f"{a} - {b_}", n_questions=nq, acc_diff=dm, diff_lo=lo, diff_hi=hi,
                                 extra_reasoning_tokens=ta - tb, extra_total_tokens=g[g.level == a].total_output_tokens.mean() - g[g.level == b_].total_output_tokens.mean(),
                                 extra_latency_s=g[g.level == a].est_wall_s.mean() - g[g.level == b_].est_wall_s.mean()))
    D = pd.DataFrame(rows); D.to_csv(os.path.join(out, "table_B_contrasts.csv"), index=False)
    return T, D

def policy_tables(dp, rng, out):
    rows = []
    for pol, g in dp.groupby("policy"):
        m, lo, hi, nq = acc_ci(g, "policy", pol, rng)
        rows.append(dict(policy=pol, n_questions=nq, n_generations=len(g), accuracy=m, acc_lo=lo, acc_hi=hi, reasoning_tokens=g.reasoning_tokens.mean(),
                         total_output_tokens=g.total_output_tokens.mean(), latency_s=g.est_wall_s.mean(), energy_j=g.energy_j.mean() if "energy_j" in g else np.nan,
                         truncated=g.truncated.mean(), malformed=g.malformed.mean(), acc_gsm8k=g[g.benchmark == "gsm8k"].correct.mean(), acc_math500=g[g.benchmark == "math500"].correct.mean(),
                         share_low=(g.level == "low").mean(), share_medium=(g.level == "medium").mean(), share_high=(g.level == "high").mean(), seed_acc_sd=g.groupby("seed").correct.mean().std()))
    P = pd.DataFrame(rows); P.to_csv(os.path.join(out, "table_C_policies.csv"), index=False)
    rows = []
    for a, b_ in (("task_adaptive", "random_matched"), ("task_adaptive", "fixed_low"), ("task_adaptive", "fixed_high"), ("fixed_high", "fixed_low"), ("random_matched", "fixed_low")):
        if a in set(dp.policy) and b_ in set(dp.policy):
            dm, lo, hi, nq = diff_ci(dp, "policy", a, b_, rng)
            rows.append(dict(contrast=f"{a} - {b_}", n_questions=nq, acc_diff=dm, diff_lo=lo, diff_hi=hi,
                             extra_reasoning_tokens=dp[dp.policy == a].reasoning_tokens.mean() - dp[dp.policy == b_].reasoning_tokens.mean()))
    PD = pd.DataFrame(rows); PD.to_csv(os.path.join(out, "table_D_policy_contrasts.csv"), index=False)
    return P, PD

# ---------------------------------------------------------------- figures --
def fig1(T, figs):
    f, ax = plt.subplots(figsize=(3.6, 3.1), dpi=200); style(ax)
    for sub in [s for s in SUB_ORDER if s in set(T.subgroup)]:
        g = T[(T.subgroup == sub)].set_index("level").loc[LEVELS]
        ax.plot(g.reasoning_tokens, g.accuracy, color=HUE[sub], lw=2, marker="o", ms=4.5, mec="white", mew=1, label=SUB_LABEL[sub], zorder=3)
        ax.errorbar(g.reasoning_tokens, g.accuracy, yerr=[g.accuracy - g.acc_lo, g.acc_hi - g.accuracy], fmt="none", ecolor=HUE[sub], elinewidth=0.9, capsize=0, alpha=0.8)
    ax.set_xscale("log"); ax.set_xticks([128, 256, 512, 1024, 2048]); ax.set_xticklabels(["128", "256", "512", "1K", "2K"]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("mean reasoning tokens per request (log scale)", color=INK2, fontsize=7.5); ax.set_ylabel("accuracy (95% CI)", color=INK2, fontsize=7.5)
    lo = max(0.0, np.floor((T.acc_lo.min() - 0.05) * 10) / 10); ax.set_ylim(lo, 1.01); ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.legend(frameon=False, fontsize=6, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
    f.tight_layout(pad=0.3); f.savefig(os.path.join(figs, "fig1_accuracy_vs_computation.pdf")); f.savefig(os.path.join(figs, "png", "fig1_accuracy_vs_computation.png")); plt.close(f)

def fig2(D, figs):
    subs = [s for s in SUB_ORDER if s in set(D.scope)]; contrasts = ["medium - low", "high - medium", "high - low"]
    f, ax = plt.subplots(figsize=(3.6, 2.6), dpi=200); style(ax); x = np.arange(len(subs)); w = 0.26
    for k, c in enumerate(contrasts):
        g = D[(D.contrast == c)].set_index("scope").loc[subs]
        ax.bar(x + (k - 1) * w, g.acc_diff, width=w - 0.03, color=[LEVEL_HUE["low"], LEVEL_HUE["medium"], LEVEL_HUE["high"]][k], label=c.replace(" - ", " vs "), edgecolor="white", linewidth=1)
        ax.errorbar(x + (k - 1) * w, g.acc_diff, yerr=[g.acc_diff - g.diff_lo, g.diff_hi - g.acc_diff], fmt="none", ecolor=INK2, elinewidth=0.9, capsize=0)
    ax.axhline(0, color=PALE, lw=0.8); ax.set_xticks(x); ax.set_xticklabels([SUB_SHORT[s] for s in subs], fontsize=6.4, color=INK2)
    ax.set_ylabel("accuracy difference (paired, 95% CI)", color=INK2, fontsize=7.5); ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0)); ax.legend(frameon=False, fontsize=6.2, loc="upper left")
    f.tight_layout(pad=0.3); f.savefig(os.path.join(figs, "fig2_marginal_value.pdf")); f.savefig(os.path.join(figs, "png", "fig2_marginal_value.png")); plt.close(f)

def fig3(dp, figs, budgets, seed=0, policy="task_adaptive", nshow=120):
    g = dp[(dp.policy == policy) & (dp.seed == seed)].sort_values("arrival").head(nshow)
    f, (a1, a2) = plt.subplots(2, 1, figsize=(3.6, 3.2), dpi=200, sharex=True); style(a1); style(a2)
    for bench, c in (("gsm8k", HUE["gsm8k_long"]), ("math500", HUE["math_medium"])):
        h = g[g.benchmark == bench]
        a1.scatter(h.arrival, h.budget, s=9, color=c, label={"gsm8k": "GSM8K request", "math500": "MATH-500 request"}[bench], zorder=3)
        a2.scatter(h.arrival, h.reasoning_tokens, s=9, color=c, zorder=3)
    a1.set_yscale("log"); a1.set_yticks(list(budgets.values())); a1.set_yticklabels([f"{v}" for v in budgets.values()]); a1.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); a1.set_ylim(90, 2900)
    a1.set_ylabel("assigned budget", color=INK2, fontsize=7); a1.legend(frameon=False, fontsize=6.2, loc="center right")
    a2.set_yscale("log"); a2.set_yticks([128, 256, 512, 1024, 2048]); a2.set_yticklabels(["128", "256", "512", "1K", "2K"]); a2.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); a2.set_ylim(90, 2900)
    a2.set_ylabel("reasoning tokens generated", color=INK2, fontsize=7); a2.set_xlabel(f"arrival order of requests (task-adaptive policy, seed {seed})", color=INK2, fontsize=7.5)
    f.tight_layout(pad=0.3); f.savefig(os.path.join(figs, "fig3_adaptive_sequence.pdf")); f.savefig(os.path.join(figs, "png", "fig3_adaptive_sequence.png")); plt.close(f)

def fig4(P, figs, xcol="reasoning_tokens"):
    f, ax = plt.subplots(figsize=(3.6, 2.6), dpi=200); style(ax); P = P.rename(columns={"latency_s": "est_wall_s"})
    fx = P[P.policy.isin(["fixed_low", "fixed_medium", "fixed_high"])].set_index("policy").loc[["fixed_low", "fixed_medium", "fixed_high"]]
    ax.plot(fx[xcol], fx.accuracy, color=POL_HUE["fixed_low"], lw=2, marker="o", ms=4.5, mec="white", mew=1, label="fixed budget (low, medium, high)", zorder=3)
    ax.errorbar(fx[xcol], fx.accuracy, yerr=[fx.accuracy - fx.acc_lo, fx.acc_hi - fx.accuracy], fmt="none", ecolor=POL_HUE["fixed_low"], elinewidth=1, capsize=0)
    for pol, mk in (("task_adaptive", "D"), ("random_matched", "s")):
        if pol in set(P.policy):
            r = P[P.policy == pol].iloc[0]
            ax.errorbar([r[xcol]], [r.accuracy], yerr=[[r.accuracy - r.acc_lo], [r.acc_hi - r.accuracy]], fmt=mk, ms=5.5, color=POL_HUE[pol], mec="white", mew=1, ecolor=POL_HUE[pol], elinewidth=1, capsize=0, label=POL_LABEL[pol], zorder=4)
    ax.set_xlabel({"reasoning_tokens": "mean reasoning tokens per request", "total_output_tokens": "mean output tokens per request", "est_wall_s": "mean generation time per request (s)"}[xcol], color=INK2, fontsize=7.5)
    ax.set_ylabel("overall accuracy (95% CI)", color=INK2, fontsize=7.5); ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0)); ax.legend(frameon=False, fontsize=6.2, loc="lower right")
    f.tight_layout(pad=0.3); name = "fig4_policies" + ("" if xcol == "reasoning_tokens" else "_" + xcol)
    f.savefig(os.path.join(figs, f"{name}.pdf")); f.savefig(os.path.join(figs, "png", f"{name}.png")); plt.close(f)

def fig5_examples(df, out, k=3):
    """Questions whose outcome changes with the budget, chosen by a rule (most seeds flip from wrong at low to right at high), not by hand."""
    q = df.groupby(["task_id", "level"]).correct.mean().unstack()
    q = q.dropna(); q["flip"] = q["high"] - q["low"]; q = q.join(df.groupby("task_id")[["benchmark", "subgroup"]].first())
    pick = pd.concat([q.sort_values("flip", ascending=False).head(k), q.sort_values("flip").head(1)])   # the largest gains and the largest loss
    rows = []
    for tid, r in pick.iterrows():
        for lvl in LEVELS:
            g = df[(df.task_id == tid) & (df.level == lvl)]
            rows.append(dict(task_id=tid, benchmark=r.benchmark, subgroup=r.subgroup, level=lvl, budget=int(g.budget.iloc[0]), reasoning_tokens=g.reasoning_tokens.mean(),
                             latency_s=g.est_wall_s.mean(), correct_frac=g.correct.mean(), n_seeds=len(g), gold=g.gold.iloc[0], preds="; ".join(map(str, g.pred.tolist()))))
    E = pd.DataFrame(rows); E.to_csv(os.path.join(out, "table_E_examples.csv"), index=False); return E

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--fixed", required=True); ap.add_argument("--policies", default=None)
    ap.add_argument("--config", default="configs/model.json"); ap.add_argument("--out", default="results/aggregate"); ap.add_argument("--figs", default="figures")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); os.makedirs(os.path.join(a.figs, "png"), exist_ok=True)
    rng = np.random.default_rng(0); cfg = json.load(open(a.config)); budgets = cfg["backend_budgets"]
    df = load_dir(a.fixed); assert df is not None, "no fixed-mode records"
    df = attach_energy(df, a.fixed)
    T, D = level_tables(df, rng, a.out); fig1(T, a.figs); fig2(D, a.figs); E = fig5_examples(df, a.out)
    print("A: per-level"); print(T[T.subgroup == "all"][["scope", "level", "n_questions", "accuracy", "acc_lo", "acc_hi", "reasoning_tokens", "total_output_tokens", "latency_s", "energy_j", "budget_exhausted", "truncated", "malformed", "seed_acc_sd"]].round(3).to_string(index=False))
    print("B: paired contrasts"); print(D.round(3).to_string(index=False))
    summary = dict(n_questions=int(df.task_id.nunique()), n_generations=int(len(df)), seeds=sorted(df.seed.unique().tolist()), checkpoint=cfg["model_id"], revision=cfg["revision"])
    dp = load_dir(a.policies) if a.policies else None
    if dp is not None:
        dp = attach_energy(dp, a.policies); P, PD = policy_tables(dp, rng, a.out)
        fig3(dp, a.figs, budgets); fig4(P, a.figs); fig4(P, a.figs, "total_output_tokens"); fig4(P, a.figs, "est_wall_s")
        print("C: policies"); print(P.round(3).to_string(index=False)); print("D: policy contrasts"); print(PD.round(3).to_string(index=False))
        summary.update(policy_generations=int(len(dp)), policy_seeds=sorted(dp.seed.unique().tolist()))
    json.dump(summary, open(os.path.join(a.out, "summary.json"), "w"), indent=1)

if __name__ == "__main__": main()
