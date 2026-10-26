"""J figures from the per-round traces written by audit/round2/A4/scripts/j_traces.py and the
phase scan written by j_cao_phases.py.

    python make_figures_j.py --traces <J/n20k_r2> --traces300k <J/n300k> --phases <J/cao_phases.csv> --out figures/s5

One declared deviation, the same under every mechanism (shadeall: bid the capability, then deliver
0.05 below what the reference profile delivers in every later served round), deviator = GPT-4.
J1: cumulative utility gain of the deviator over the reference profile, same seed (common random
    numbers), mean over seeds with an interquartile band, n = 20,000.
J2: the same prefix gain divided by rounds elapsed.
J3: our monitor's cumulative deficit r*tau - Z_r against its tolerance b_n(r), one seed, until the
    first crossing (the mechanism switches there).
J4: how Cao et al.'s mechanism splits the horizon as n grows (only exploitation is priced and
    monitored), honest profile.
J5: n = 300,000, where Cao et al.'s priced phase exists: (a) the deviator's cumulative gain and
    (b) the platform's realised revenue per round elapsed, shades 0.05 and 0.10, ours vs Cao et al.
"""
import argparse, os, json, glob, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../A4/scripts"))
from trace import load, PHASE_CODES  # noqa: E402

HUE = {"ours": "#2a78d6", "router": "#eb6834", "router2": "#b84a1f", "cao": "#4a3aa7", "pooled": "#eda100", "prior": "#1baf7a"}
INK, INK2, MUTED, GRID, PALE = "#1b1b1b", "#4a4a4a", "#8a8a8a", "#e3e3e0", "#c9c9c6"
SERIES = [("mesp_scalar", "proposed", "shadeall0.05", "ours", HUE["ours"]),
          ("second_best", "proposed", "shadeall0.05", "Cao et al.", HUE["cao"]),
          ("router_eps", "capability", "shadeall0.05", "ε-greedy router", HUE["router"]),
          ("router_ucb", "capability", "shadeall0.05", "UCB router", HUE["router2"])]

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=7, length=3, width=0.8); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)

def kfmt(ax, axis="x"):
    f = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:g}K" if abs(v) >= 1000 else f"{v:g}")
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(f)

def dev_series(z, dev):
    return np.cumsum(np.where(z["agent"] == dev, z["agent_utility"], 0.0).astype(float))

def seeds_in(d, mech, prof):
    return sorted({int(f[-6:-4]) for f in glob.glob(os.path.join(d, f"{mech}_{prof}_seed*.npz"))})

def gains(d, mech, ref, devp, dev):
    G = []
    for s in seeds_in(d, mech, devp):
        zr = load(os.path.join(d, f"{mech}_{ref}_seed{s:02d}.npz")); zd = load(os.path.join(d, f"{mech}_{devp}_seed{s:02d}.npz"))
        G.append(dev_series(zd, dev) - dev_series(zr, dev))
    return np.array(G)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--traces", required=True); ap.add_argument("--traces300k", default=None)
    ap.add_argument("--phases", default=None); ap.add_argument("--out", default="figures/s5")
    a = ap.parse_args(); os.makedirs(os.path.join(a.out, "png"), exist_ok=True)
    def save(f, name):
        f.tight_layout(pad=0.3); f.savefig(os.path.join(a.out, f"{name}.pdf")); f.savefig(os.path.join(a.out, "png", f"{name}.png")); plt.close(f)
    inst = json.load(open(os.path.join(a.traces, "instance.json"))); dev = inst["deviator"]; n = inst["n"]
    t = np.arange(1, n + 1); rows = []
    # ---------------- J1 / J2 ----------------
    f1, a1 = plt.subplots(figsize=(3.33, 2.5), dpi=200); f2, a2 = plt.subplots(figsize=(3.33, 2.5), dpi=200); style(a1); style(a2)
    for mech, ref, devp, lab, c in SERIES:
        G = gains(a.traces, mech, ref, devp, dev); m = G.mean(0)
        a1.plot(t, m, color=c, lw=2, label=lab, solid_capstyle="round")
        a1.fill_between(t, np.percentile(G, 25, axis=0), np.percentile(G, 75, axis=0), color=c, alpha=0.12, lw=0)
        a2.plot(t, m / t, color=c, lw=2, label=lab, solid_capstyle="round")
        for tt in (1000, 5000, 10000, n):
            rows.append(dict(figure="J1", horizon=n, mech=mech, deviation=devp, t=tt, mean_cum_gain=m[tt - 1], q25=np.percentile(G[:, tt - 1], 25), q75=np.percentile(G[:, tt - 1], 75), seeds=len(G)))
    for ax in (a1, a2):
        ax.axhline(0, color=PALE, lw=0.8); ax.set_xlabel(f"round t  (horizon n = {n:,})", color=INK2, fontsize=7.5); kfmt(ax); ax.legend(frameon=False, fontsize=6.3, loc="lower left")
    a1.set_ylabel("deviator's cumulative gain over honesty", color=INK2, fontsize=7); kfmt(a1, "y")
    a2.set_ylabel("cumulative gain / t", color=INK2, fontsize=7.5); a2.set_ylim(-0.25, 0.08)
    save(f1, "J1_cumulative_gain"); save(f2, "J2_gain_per_round")
    # ---------------- J3 ----------------
    s0 = seeds_in(a.traces, "mesp_scalar", "shadeall0.05")[0]
    z = load(os.path.join(a.traces, f"mesp_scalar_shadeall0.05_seed{s0:02d}.npz")); meta = z["meta"]
    pri = (z["phase"] == PHASE_CODES["primary"]) & (z["agent"] == meta["W"])
    Z = np.cumsum(z["reward"][pri].astype(float)); r = np.arange(1, len(Z) + 1); tau = meta["tau"]; c0 = inst["c_boundary"]
    deficit = r * tau - Z; tol = np.sqrt(r * c0); cross = int(np.argmax(deficit > tol)) + 1 if (deficit > tol).any() else len(r)
    f3, a3 = plt.subplots(figsize=(3.33, 2.4), dpi=200); style(a3)
    a3.plot(r[:cross], tol[:cross], color=MUTED, lw=2, label="tolerance b_n(r)"); a3.plot(r[:cross], deficit[:cross], color=HUE["ours"], lw=2, label="deficit r·τ − Z_r")
    a3.axvline(cross, color=PALE, lw=0.8); a3.annotate(f"first crossing at pull {cross:,}", (cross, tol[cross - 1]), xytext=(-6, 6), textcoords="offset points", ha="right", fontsize=6.6, color=INK2)
    a3.set_xlabel("winner's primary pulls r  (shading the price by 0.05)", color=INK2, fontsize=7.5); a3.set_ylabel("cumulative reward units", color=INK2, fontsize=7.5); kfmt(a3); a3.legend(frameon=False, fontsize=6.4, loc="upper left")
    save(f3, "J3_monitor_path")
    rows.append(dict(figure="J3", horizon=n, mech="mesp_scalar", deviation="shadeall0.05", seed=s0, tau=tau, first_crossing_pull=cross, conv_r_meta=meta.get("conv_r")))
    # ---------------- J4: Cao et al.'s phase split against n ----------------
    if a.phases:
        ph = pd.read_csv(a.phases); g = ph.groupby("n")[["explore", "exploit", "blind", "undelegated", "monitor_slack"]].mean().reset_index()
        f4, a4 = plt.subplots(figsize=(3.33, 2.1), dpi=200); style(a4); a4.grid(False)
        y = np.arange(len(g)); h = 0.55
        fr = g[["explore", "exploit", "blind"]].to_numpy() / g["n"].to_numpy()[:, None]
        labels = ["exploration (unpriced)", "exploitation (priced, monitored)", "blind trust (unpriced)"]; cols = [MUTED, HUE["cao"], PALE]
        left = np.zeros(len(g))
        for k in range(3):
            a4.barh(y, fr[:, k], left=left, height=h, color=cols[k], label=labels[k], edgecolor="white", linewidth=1.5)
            for i in range(len(g)):
                if fr[i, k] >= 0.09: a4.text(left[i] + fr[i, k] / 2, y[i], f"{fr[i, k]:.0%}", ha="center", va="center", fontsize=6.3, color="white" if k == 1 else INK)
            left += fr[:, k]
        a4.set_yticks(y); a4.set_yticklabels([f"n = {int(v):,}" for v in g["n"]], fontsize=7, color=INK2); a4.invert_yaxis()
        a4.set_xlim(0, 1); a4.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0)); a4.set_xlabel("share of the horizon", color=INK2, fontsize=7.5)
        a4.legend(frameon=False, fontsize=6.0, loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=1)
        save(f4, "J4_cao_phase_split")
        for _, rr in g.iterrows():
            rows.append(dict(figure="J4", horizon=int(rr.n), mech="second_best", explore_frac=rr.explore / rr.n, exploit_frac=rr.exploit / rr.n, blind_frac=rr.blind / rr.n, monitor_slack=rr.monitor_slack, seeds=int((ph.n == rr.n).sum())))
    # ---------------- J5: n = 300k, where their priced phase exists ----------------
    if a.traces300k:
        inst3 = json.load(open(os.path.join(a.traces300k, "instance.json"))); n3 = inst3["n"]; t3 = np.arange(1, n3 + 1); step = 50
        f5, (b1, b2) = plt.subplots(1, 2, figsize=(7.0, 2.5), dpi=200); style(b1); style(b2)
        spec = [("mesp_scalar", "proposed", "shadeall0.05", "ours, shade 0.05", HUE["ours"], "-"), ("mesp_scalar", "proposed", "shadeall0.10", "ours, shade 0.10", HUE["ours"], (0, (3, 1.5))),
                ("second_best", "proposed", "shadeall0.05", "Cao et al., shade 0.05", HUE["cao"], "-"), ("second_best", "proposed", "shadeall0.10", "Cao et al., shade 0.10", HUE["cao"], (0, (3, 1.5)))]
        for mech, ref, devp, lab, c, ls in spec:
            G = gains(a.traces300k, mech, ref, devp, dev); m = G.mean(0)
            b1.plot(t3[::step], m[::step], color=c, lw=2, ls=ls, label=lab)
            R = []
            for s in seeds_in(a.traces300k, mech, devp):
                zd = load(os.path.join(a.traces300k, f"{mech}_{devp}_seed{s:02d}.npz")); R.append(np.cumsum(zd["reward"].astype(float)) / t3)
            R = np.array(R).mean(0); b2.plot(t3[::step], R[::step], color=c, lw=2, ls=ls, label=lab)
            rows.append(dict(figure="J5", horizon=n3, mech=mech, deviation=devp, t=n3, mean_cum_gain=m[-1], platform_revenue_per_round=R[-1], seeds=len(G)))
        for ax in (b1, b2): ax.set_xlabel(f"round t  (horizon n = {n3:,})", color=INK2, fontsize=7.5); kfmt(ax)
        b1.axhline(0, color=PALE, lw=0.8); b1.set_ylabel("deviator's cumulative gain over honesty", color=INK2, fontsize=7); kfmt(b1, "y"); b1.legend(frameon=False, fontsize=6.3, loc="lower left")
        b2.set_ylabel("platform's realised revenue / t", color=INK2, fontsize=7.5); b2.set_ylim(0, 0.9); b2.legend(frameon=False, fontsize=6.3, loc="center right")
        b1.set_title("(a) what the deviation earns the provider", fontsize=7.5, color=INK, loc="left"); b2.set_title("(b) what the platform is left with", fontsize=7.5, color=INK, loc="left")
        save(f5, "J5_long_horizon")
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "values_J.csv"), index=False)
    print("wrote J1..J5;", len(rows), "value rows; J3 crossing at", cross, "meta conv_r", meta.get("conv_r"))

if __name__ == "__main__": main()
