"""Summarise grid_main.json: per-mechanism best gains by deviation family and log-log slopes."""
import json, sys, math
import numpy as np
rows = json.load(open(sys.argv[1]))
fam = {'elic': lambda k: k.startswith('E-') or k.startswith('become'),
       'prim': lambda k: k.startswith('P-'),
       'comb': lambda k: '+' in k}
def best(g, pred):
    items = [(k, v) for k, v in g.items() if pred(k)]
    k, v = max(items, key=lambda kv: kv[1][0]); return k, v[0], v[1]
def slope(ns, ys):
    ns = np.array(ns, float); ys = np.array(ys, float)
    ok = ys > 0
    if ok.sum() < 2: return float('nan')
    return float(np.polyfit(np.log(ns[ok]), np.log(ys[ok]), 1)[0])
for mech in ('MESP', 'ACM'):
    rs = [r for r in rows if r['mech'] == mech]
    print(f"\n== {mech} ==")
    print(f"{'n':>7} {'rev/n':>7} {'bench2':>6} {'benchH':>6} {'Tw':>5} {'tau':>6} | {'best all':>9} {'/round':>8} {'best elic':>9} {'/round':>8} {'best prim':>9} {'best ag2':>9} {'/round':>8}")
    ns=[]; ba=[]; be=[]; bp=[]; b2=[]; rev=[]
    for r in rs:
        n = r['n']; g1 = r['gains1']; g2 = r['gains2']
        ka, va, sa = best(g1, lambda k: True); ke, ve, se_ = best(g1, fam['elic']); kp, vp, sp = best(g1, fam['prim'])
        k2, v2, s2 = max(((k, v[0], v[1]) for k, v in g2.items()), key=lambda x: x[1])
        ns.append(n); ba.append(va); be.append(ve); bp.append(vp); b2.append(v2); rev.append(r['rev_per_round'])
        print(f"{n:7d} {r['rev_per_round']:7.4f} {r['bench2']:6.2f} {r['benchH']:6.2f} {r['Tw_mean']:5.0f} {r['tau_mean']:6.3f} | {va:9.1f} {va/n:8.5f} {ve:9.1f} {ve/n:8.5f} {vp:9.1f} {v2:9.1f} {v2/n:8.5f}")
        print(f"        best all: {ka} (se {sa:.1f}); best elic: {ke} (se {se_:.1f}); best prim: {kp} (se {sp:.1f}); best ag2: {k2} (se {s2:.1f})")
    print(f"  log-log slope vs n: best-all {slope(ns, ba):.3f} | best-elicitation {slope(ns, be):.3f} | best-primary {slope(ns, bp):.3f} | best-agent2 {slope(ns, b2):.3f}")
    print(f"  revenue shortfall per round (bench2 - rev/n): " + ' '.join(f"{(0.3 - x):.4f}" for x in rev) + f"  slope of total shortfall vs n: {slope(ns, [(0.3 - x) * n for x, n in zip(rev, ns)]):.3f}")
    # elicitation family detail
    print("  elicitation-family gains by n (E-const best c, E-late best, E-earlyhigh best, E-pace best, become-loser best):")
    for r in rs:
        g1 = r['gains1']
        def bb(p):
            k, v, s = best(g1, p); return f"{k}={v:.0f}"
        print(f"   n={r['n']:7d}: {bb(lambda k: k.startswith('E-const'))}; {bb(lambda k: k.startswith('E-late'))}; {bb(lambda k: k.startswith('E-early'))}; {bb(lambda k: k.startswith('E-pace'))}; {bb(lambda k: k.startswith('become'))}")
# theory lines
print("\nTheory reference: MESP L_n (M_1 - 0.3)=0.2 L_n upper envelope of the elicitation underbid; b_n(n)=sqrt(n log(2n^4)/2):")
for n in (10000, 17783, 31623, 56234, 100000):
    L = min(n // 4, math.ceil(n ** (2/3) * math.log(math.e * n) ** (1/3)))
    print(f"   n={n:7d}: L_n={L:5d} 0.2 L_n={0.2*L:7.1f}  b_n(n)={math.sqrt(n*math.log(2*n**4)/2):7.1f}  ACM 2 ell/gap^2={2*math.log(2*n**4)/0.04:7.0f}")
