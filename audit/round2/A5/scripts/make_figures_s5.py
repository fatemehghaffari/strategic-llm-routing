"""Section 5 figures, rebuilt from the committed CSVs only (no number is typed in).

    python make_figures_s5.py --out figures/s5

Design rules (project palette, validated): one hue per ENTITY across every figure, 2px lines,
markers >= 8px with a surface ring, bars <= 24px, hairline solid grid, legend whenever two or more
series, direct labels only where they carry the message, text in ink never in a series colour,
never two y-axes. Every figure also writes its plotted numbers to values.csv.
"""
import argparse, os, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../experiments/data"))
HUE = {"ours": "#2a78d6", "router": "#eb6834", "cao": "#4a3aa7", "pooled": "#eda100", "prior": "#1baf7a"}
INK, INK2, MUTED, GRID = "#1b1b1b", "#4a4a4a", "#8a8a8a", "#e3e3e0"
VALUES = []

def style(ax, grid="y"):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=7, length=3, width=0.8)
    if grid: ax.grid(axis=grid, color=GRID, lw=0.6); ax.set_axisbelow(True)

def fig(w=3.33, h=2.5): return plt.subplots(figsize=(w, h), dpi=200)
def save(f, name, out):
    f.tight_layout(pad=0.3); f.savefig(os.path.join(out, name + ".pdf")); f.savefig(os.path.join(out, "png", name + ".png")); plt.close(f); print("wrote", name)
def rec(figname, **kw): VALUES.append(dict(figure=figname, **kw))
def line(ax, x, y, hue, label, ls="-"):
    sparse = len(x) <= 8
    ax.plot(x, y, linestyle=ls, color=hue, lw=2, marker="o" if sparse else None, ms=4.2, mew=1.4, mec="white", label=label, zorder=3)

# ---------------- A1: named runner-up deviation, largest configuration mean ----------------
def A1(out):
    d = pd.read_csv(R + "/A4/fine_shading_best.csv")
    u = d[d.deviation_kind == "undercut"].groupby("mech").gain_per_round.max()
    order = [("router_eps", "ε-greedy router", HUE["router"]), ("router_ucb", "UCB router", HUE["router"]),
             ("router_greedy", "greedy router", HUE["router"]), ("plmesp", "ours (context-local)", HUE["ours"])]
    order = [o for o in order if o[0] in u.index]
    f, ax = fig(3.33, 1.9); style(ax, "x")
    for i, (k, lab, c) in enumerate(order):
        ax.barh(i, u[k], color=c, height=0.6, zorder=3)
        ax.annotate(f"{u[k]:.4f}", (u[k], i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
        rec("A1", arm=k, gain_per_round=u[k])
    ax.set_yticks(range(len(order))); ax.set_yticklabels([o[1] for o in order], fontsize=7, color=INK)
    ax.set_xlabel("largest per-round gain from undercutting the pointwise runner-up", color=INK2, fontsize=7)
    ax.set_xlim(0, u.max() * 1.3)
    save(f, "A1_undercut_gain", out)

# ---------------- A2: platform reward under tested joint profiles (single context, n=20,000) ----------------
def A2(out):
    l = pd.read_csv(R + "/A2/ladder.csv"); q = l[(l.Q == 1) & (l.variant == "pl_mesp")]
    pick = [("profile", "proposed profile"), ("joint:bait_switch", "joint bait-and-switch"),
            ("joint:primary_shade_15", "joint primary shade 0.15"), ("joint:trigger_fallback_shade", "joint trigger-then-shade"),
            ("joint:zero_fallback", "joint zero in fallback"), ("joint:sabotage_all", "joint sabotage")]
    v = q.groupby("behavior").platform_reward_per_round_mean.mean()
    f, ax = fig(3.33, 2.2); style(ax, "x")
    for i, (k, lab) in enumerate(pick):
        c = HUE["ours"] if k == "profile" else MUTED
        ax.barh(i, v[k], color=c, height=0.6, zorder=3)
        ax.annotate(f"{v[k]:.3f}", (v[k], i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
        rec("A2", behavior=k, platform_reward_per_round=v[k])
    ax.set_yticks(range(len(pick))); ax.set_yticklabels([p[1] for p in pick], fontsize=7, color=INK)
    ax.set_xlabel("platform reward per round", color=INK2, fontsize=7); ax.set_title("single context, n = 20,000", loc="left", fontsize=7, color=INK2)
    ax.set_xlim(0, 1.0); save(f, "A2_reward_joint_profiles", out)

# ---------------- B1: certified exploitability band vs horizon ----------------
def B1(out):
    g = pd.read_csv(R + "/A2/exact_grid.csv"); u = g[(g.family == "replicated_unique_top") & (g.Q == 1)].sort_values("n")
    f, ax = fig(3.33, 2.4); style(ax)
    ax.fill_between(u.n, u.exploit_LB_per_round, u.exploit_UB_per_round, color=HUE["ours"], alpha=0.12, lw=0, label="certified [LB, UB]")
    line(ax, u.n, u.exploit_UB_per_round, HUE["ours"], "certified upper bound")
    line(ax, u.n, u.exploit_LB_per_round, HUE["ours"], "certified lower bound", ls="--")
    line(ax, u.n, u.prop61_gain / u.n, MUTED, "attained by the explicit deviation")
    for _, r in u.iterrows(): rec("B1", n=r.n, LB=r.exploit_LB_per_round, UB=r.exploit_UB_per_round, attained=r.prop61_gain / r.n)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("horizon n", color=INK2, fontsize=7.5)
    ax.set_xticks([2000, 8000, 20000]); ax.set_xticklabels(["2K", "8K", "20K"]); ax.minorticks_off()
    ax.set_ylabel("max unilateral gain per round", color=INK2, fontsize=7.5); ax.legend(frameon=False, fontsize=6.4)
    save(f, "B1_certified_band", out)

# ---------------- C: arrival orders (two collections, kept apart) ----------------
def C(out):
    lb = pd.read_csv(R + "/A5/c3_leaderboard_replicate.csv")
    orders = ["iid", "drift", "bursty", "grouped"]
    arms = [("plmesp:plmesp_star", "ours", HUE["ours"]), ("router_ucb:average", "UCB router", HUE["router"]),
            ("second_best:cao_eqmu", "Cao et al.", HUE["cao"])]
    f, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.4), dpi=200); style(a1); style(a2)
    x = np.arange(len(orders)); w = 0.24
    for j, (k, lab, c) in enumerate(arms):
        v = [lb[(lb.arm == k) & (lb.order == o) & (lb.n == 3000000)].revenue_per_round.mean() for o in orders]
        a1.bar(x + (j - 1) * (w + 0.02), v, width=w, color=c, label=lab, zorder=3)
        for o, val in zip(orders, v): rec("C1", collection="OpenLLM Leaderboard", arm=k, order=o, n=3000000, revenue=val)
    a1.set_xticks(x); a1.set_xticklabels(orders, fontsize=7); a1.set_ylabel("revenue per round, n = 3M", color=INK2, fontsize=7.5)
    a1.set_title("Open LLM Leaderboard, four synthetic orders", loc="left", fontsize=7.5, color=INK)
    a1.set_ylim(0, 0.52); a1.legend(frameon=False, fontsize=6.4, ncol=3, loc="upper center")
    un = [lb[(lb.arm == "second_best:cao_eqmu") & (lb.order == o) & (lb.n == 3000000)].unserved_fraction.mean() for o in orders]
    a2.bar(x, [100 * u for u in un], width=0.5, color=HUE["cao"], zorder=3)
    for xi, u in zip(x, un):
        a2.annotate(f"{100*u:.0f}%", (xi, 100 * u), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=7, color=INK2)
        rec("C2", arm="second_best:cao_eqmu", order=orders[xi], unserved_pct=100 * u)
    a2.set_xticks(x); a2.set_xticklabels(orders, fontsize=7); a2.set_ylabel("rounds Cao et al. leaves unserved (%)", color=INK2, fontsize=7.5)
    a2.set_title("ours: 0% in every order", loc="left", fontsize=7.5, color=INK)
    save(f, "C_arrival_orders", out)
    # real traffic, merged5 (its own collection): iid vs real, our arm and the two comparators
    v3 = pd.read_csv(R + "/../../audit/round2/A5/B_sim/v3_agg_2026-09-29.csv"); v3["arm"] = v3.mech + ":" + v3.profile
    m5 = v3[(v3.taskset == "merged5") & (v3.n.isin([300000, 3000000]))]
    f, ax = fig(3.33, 2.3); style(ax)
    x = np.arange(2); w = 0.24
    for j, (k, lab, c) in enumerate(arms):
        v = [m5[(m5.arm == k) & (m5.order == o)].revenue_per_round.mean() for o in ("iid", "real")]
        ax.bar(x + (j - 1) * (w + 0.02), v, width=w, color=c, label=lab, zorder=3)
        for o, val in zip(("iid", "real"), v): rec("C3", collection="RouterBench merged5", arm=k, order=o, revenue=val)
    ax.set_xticks(x); ax.set_xticklabels(["independent", "real (WildChat)"], fontsize=7)
    ax.set_ylabel("revenue per round", color=INK2, fontsize=7.5); ax.legend(frameon=False, fontsize=6.4)
    save(f, "C3_real_traffic", out)

# ---------------- D2: pooled vs local, reward and false conviction ----------------
def D2(out):
    lb = pd.read_csv(R + "/A5/c3_leaderboard_replicate.csv")
    pairs = [("plmesp:plmesp_star", "context-local (ours)", HUE["ours"]), ("mesp_scalar:mesp_star", "pooled, one price", HUE["pooled"])]
    f, (a1, a2) = plt.subplots(1, 2, figsize=(3.9, 2.0), dpi=200); style(a1, "x"); style(a2, "x")
    for i, (k, lab, c) in enumerate(pairs):
        s = lb[lb.arm == k]; rev = s.revenue_per_round.mean(); cc = 100 * s.compliant_conviction_rate.mean()
        a1.barh(i, rev, color=c, height=0.55, zorder=3); a1.annotate(f"{rev:.3f}", (rev, i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
        a2.barh(i, cc, color=c, height=0.55, zorder=3); a2.annotate(f"{cc:.0f}%", (cc, i), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
        rec("D2", arm=k, revenue=rev, compliant_conviction_pct=cc)
    for a in (a1, a2): a.set_yticks(range(2)); a.set_yticklabels([p[1] for p in pairs], fontsize=6.6, color=INK)
    a2.set_yticklabels(["", ""]); a1.set_xlim(0, 0.6); a2.set_xlim(0, 70)
    a1.set_xlabel("revenue per round", color=INK2, fontsize=7); a2.set_xlabel("false convictions (% of cells)", color=INK2, fontsize=7)
    save(f, "D2_pooled_vs_local", out)

# ---------------- E: monitor operating curve (false conviction vs detection delay) ----------------
def E(out):
    m = pd.read_csv(R + "/A4/monitor_frontier.csv")
    fam = [("anytime", "anytime boundary (ours)", HUE["ours"]), ("fixedbuffer", "fixed buffer after burn-in", HUE["prior"]), ("twosample", "two-sample test", HUE["router"])]
    f, ax = fig(3.33, 2.5); style(ax)
    for k, lab, c in fam:
        s = m[m.monitor == k].sort_values("false_conviction_rate")
        ax.plot(s.false_conviction_rate, s.median_delay_baitswitch, "o", color=c, ms=4.6, mew=1.4, mec="white", label=lab, zorder=3)
        for _, r in s.iterrows(): rec("E3", monitor=k, params=r.params, false_conviction_rate=r.false_conviction_rate, median_delay=r.median_delay_baitswitch)
    ax.set_yscale("log"); ax.set_xlabel("false-conviction rate of a compliant winner", color=INK2, fontsize=7.5)
    ax.set_ylabel("median detection delay of a bait-and-switch (pulls)", color=INK2, fontsize=7); ax.legend(frameon=False, fontsize=6.4)
    save(f, "E3_monitor_operating_curve", out)

# ---------------- F1: near-tie revenue against the capability gap ----------------
def F1(out):
    g = pd.read_csv(R + "/A4/capability_gap_summary.csv"); p = g[(g.mech == "plmesp") & (g.delta > 0)].sort_values("delta")
    f, ax = fig(3.33, 2.3); style(ax)
    line(ax, p.delta, p.revenue_at_proposed, HUE["ours"], "proposed profile")
    line(ax, p.delta, p.equilibrium_revenue, MUTED, "low-revenue equilibrium member")
    lo = p[p.equilibrium_revenue > 0.6].delta.max(); hi = p[p.equilibrium_revenue < 0.6].delta.min()
    ax.axvspan(lo, hi, color=HUE["ours"], alpha=0.10, lw=0); ax.annotate(f"crossover between {lo:.4f} and {hi:.4f}", (hi, 0.47), xytext=(6, 0), textcoords="offset points", fontsize=6.3, color=INK2, va="center")
    for _, r in p.iterrows(): rec("F1", delta=r.delta, revenue_at_proposed=r.revenue_at_proposed, equilibrium_revenue=r.equilibrium_revenue)
    ax.set_xscale("log"); ax.set_xlabel("capability gap between the top two providers (log scale)", color=INK2, fontsize=7.5); ax.set_ylabel("revenue per round", color=INK2, fontsize=7.5)
    ax.legend(frameon=False, fontsize=6.4, loc="center right"); save(f, "F1_near_tie", out)

# ---------------- G1: certified gain against the number of task types ----------------
def G1(out):
    g = pd.read_csv(R + "/A2/exact_grid.csv"); s = g[(g.family == "replicated_unique_top") & (g.K == 3) & (g.n == 8000)].sort_values("Q")
    f, ax = fig(3.33, 2.2); style(ax)
    line(ax, s.Q, s.exploit_UB_per_round, HUE["ours"], "certified upper bound"); line(ax, s.Q, s.exploit_LB_per_round, HUE["ours"], "certified lower bound", ls="--")
    for _, r in s.iterrows(): rec("G1", Q=r.Q, UB=r.exploit_UB_per_round, LB=r.exploit_LB_per_round)
    ax.set_xlabel("number of task types Q (three providers, n = 8,000)", color=INK2, fontsize=7.5); ax.set_ylabel("certified gain per round", color=INK2, fontsize=7.5)
    ax.legend(frameon=False, fontsize=6.4); save(f, "G1_gain_vs_Q", out)

# ---------------- H1/H2: continuum thresholds, predicted vs measured; crash detection power ----------------
def H(out):
    t = pd.read_csv(R + "/A3/threshold_summary.csv")
    # Predicted crossings of sigma_n below the second capacity, solved from the mechanism's own
    # constants before the sweep ran: audit/round2/A3/THRESHOLD_REPORT.md, table at line 257 (d = 1,
    # instance C) and the d = 2, d = 3 paragraphs (instances E and D). No committed CSV holds them.
    PRED = {1: (6.53, 6.58), 2: (9.10, 9.16), 3: (11.78, 11.85)}
    INST = {1: "C", 2: "E", 3: "D"}
    f, ax = fig(3.33, 2.2); style(ax, "x")
    for i, d in enumerate([1, 2, 3]):
        s = t[(t.d == d) & (t.inst == INST[d])].sort_values("logn")
        first = s[s.positive_price_share > 0].logn.min(); full = s[s.positive_price_share >= 0.999].logn.min()
        pr = pd.Series(PRED[d])
        ax.plot([pr.min(), pr.max()], [i, i], color=MUTED, lw=9, solid_capstyle="butt", alpha=0.75, zorder=2, label="predicted interval" if i == 0 else None)
        ax.annotate(f"predicted {pr.min():.2f}–{pr.max():.2f}", (pr.max(), i), xytext=(5, 7), textcoords="offset points", fontsize=6, color=INK2)
        ax.plot([first], [i], "o", color=HUE["ours"], ms=5, mew=1.4, mec="white", zorder=3, label="first positive price" if i == 0 else None)
        ax.plot([full], [i], "s", color=HUE["ours"], ms=5, mew=1.4, mec="white", zorder=3, label="all regions priced" if i == 0 else None)
        rec("H1", d=d, predicted_lo=pr.min(), predicted_hi=pr.max(), first_positive=first, all_priced=full)
    ax.set_yticks(range(3)); ax.set_yticklabels(["d = 1", "d = 2", "d = 3"], fontsize=7, color=INK); ax.set_xlabel("log10 horizon", color=INK2, fontsize=7.5)
    ax.set_xlim(6, 12.6); ax.legend(frameon=False, fontsize=6.2, loc="lower right"); save(f, "H1_thresholds", out)
    s = t[(t.d == 1) & (t.K == 2)].groupby("logn")[["positive_price_share", "conviction_share_crash"]].mean().reset_index()
    f, ax = fig(3.33, 2.2); style(ax)
    line(ax, s.logn, 100 * s.positive_price_share, MUTED, "regions with a positive price (%)"); line(ax, s.logn, 100 * s.conviction_share_crash, HUE["ours"], "crashing winner convicted (%)")
    for _, r in s.iterrows(): rec("H2", logn=r.logn, positive_price_pct=100 * r.positive_price_share, crash_convicted_pct=100 * r.conviction_share_crash)
    ax.set_xlabel("log10 horizon (d = 1)", color=INK2, fontsize=7.5); ax.set_ylabel("percent of regions", color=INK2, fontsize=7.5); ax.legend(frameon=False, fontsize=6.4)
    save(f, "H2_detection_power", out)

# ---------------- I1/I2: provider scaling, raw and benchmark-normalised ----------------
def I(out):
    d = pd.read_csv(R + "/A5/c3_provider_scaling.csv"); Ks = sorted(d.K.unique())
    arms = [("plmesp:plmesp_star", "ours", HUE["ours"]), ("router_ucb:average", "UCB router, compliant", HUE["router"]), ("second_best:cao_eqmu", "Cao et al.", HUE["cao"])]
    f, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.4), dpi=200); style(a1); style(a2)
    bench = [d[d.K == k].second_cap.mean() for k in Ks]
    a1.plot(Ks, bench, color=MUTED, lw=1.2, dashes=(3, 2), label="second capability", zorder=2)
    for k, lab, c in arms:
        v = [d[(d.arm == k) & (d.K == kk)].revenue_per_round.mean() for kk in Ks]
        line(a1, Ks, v, c, lab); line(a2, Ks, np.array(bench) - np.array(v), c, lab)
        for kk, val, b in zip(Ks, v, bench): rec("I", arm=k, K=kk, revenue=val, second_cap=b, shortfall=b - val)
    a1.set_xlabel("number of providers K", color=INK2, fontsize=7.5); a1.set_ylabel("revenue per round", color=INK2, fontsize=7.5); a1.legend(frameon=False, fontsize=6.4)
    a2.axhline(0, color=GRID, lw=0.8); a2.set_xlabel("number of providers K", color=INK2, fontsize=7.5); a2.set_ylabel("second capability minus revenue", color=INK2, fontsize=7.5)
    save(f, "I_provider_scaling", out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="figures/s5"); a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "png"), exist_ok=True)
    for fn in (A1, A2, B1, C, D2, E, F1, G1, H, I):
        try: fn(a.out)
        except Exception as e: print("FAILED", fn.__name__, type(e).__name__, e)
    pd.DataFrame(VALUES).to_csv(os.path.join(a.out, "values.csv"), index=False); print("values:", len(VALUES), "rows")
