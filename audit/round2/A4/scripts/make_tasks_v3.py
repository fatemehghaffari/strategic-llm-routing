"""Write the v3 task lists (one line of run_v3.py arguments per Slurm array task)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SUBS = [l.strip() for l in open(os.path.join(HERE, "arrival_order_subsets_v2.txt")) if l.strip()]
RULES9 = ["plmesp", "mesp_scalar", "second_best", "router_greedy", "router_eps", "router_ucb",
          "esmaeili", "router_audit_d002", "router_audit_d005"]
AUD = ["router_audit_d002", "router_audit_d005"]
AUD_PROF = "exploit_slow,exploit_fast,average,evade"
V2_RULES = "plmesp,mesp_scalar,second_best,router_greedy,router_eps,router_ucb,esmaeili"
V2_PROF = "plmesp_star,plmesp_low,mesp_star,cao_eq0,cao_eqmu,exploit_slow,exploit_fast,average,proposed"


def lines(which):
    L = []
    for sub in SUBS:
        lab = sub.split("=")[0]
        if which == "main":
            for r in RULES9:                                   # item 2, 3e6
                for o in ("iid", "bursty"):
                    L.append(f"i2 {lab} q7 {r} learning {o} 3000000 0 10|{sub}")
                L.append(f"i2 {lab} merged5 {r} learning iid 3000000 0 10|{sub}")
            for r in RULES9:                                   # item 2, 3e7, sharded by seed
                for s in range(10):
                    L.append(f"i2 {lab} q7 {r} learning iid 30000000 {s} 1|{sub}")
            for r in AUD:                                      # item 3, one task per profile
                for pr in AUD_PROF.split(","):
                    for o in ("iid", "bursty", "drift", "grouped"):
                        for n in (300000, 3000000):
                            L.append(f"i3 {lab} q7 {r} {pr} {o} {n} 0 20|{sub}")
                    for o in ("iid", "bursty"):
                        for s in range(5):
                            L.append(f"i3 {lab} q7 {r} {pr} {o} 30000000 {s} 1|{sub}")
            for n in (300000, 3000000):                        # item 1 bridge: merged5 shuffled, per rule
                for r in V2_RULES.split(","):
                    L.append(f"i1 {lab} merged5 {r} {V2_PROF} iid {n} 0 20|{sub}")
        elif which == "real":
            for r in RULES9:
                L.append(f"i2 {lab} merged5 {r} learning real 3000000 0 10|{sub}")
            for r in AUD:
                for pr in AUD_PROF.split(","):
                    for n in (300000, 3000000):
                        L.append(f"i3 {lab} merged5 {r} {pr} real {n} 0 20|{sub}")
            for n in (300000, 3000000):
                for r in V2_RULES.split(","):
                    L.append(f"i1 {lab} merged5 {r} {V2_PROF} real {n} 0 20|{sub}")
        elif which == "fb05":
            # 5% false-ban audit variants (29 Sep 2026): the item 3 grid of "main" and "real".
            for r in ("router_audit_d002_fb05", "router_audit_d005_fb05"):
                for pr in AUD_PROF.split(","):
                    for o in ("iid", "bursty", "drift", "grouped"):
                        for n in (300000, 3000000):
                            L.append(f"i3 {lab} q7 {r} {pr} {o} {n} 0 20|{sub}")
                    for o in ("iid", "bursty"):
                        for s in range(5):
                            L.append(f"i3 {lab} q7 {r} {pr} {o} 30000000 {s} 1|{sub}")
                    for n in (300000, 3000000):
                        L.append(f"i3 {lab} merged5 {r} {pr} real {n} 0 20|{sub}")
        elif which == "static":
            # router_static (29 Sep 2026): the static benchmark router on the router grids above.
            # item 1 bridge (both orders, 3e5 and 3e6, 20 seeds) and item 2 learning at 3e6.
            r = "router_static"
            for o in ("iid", "real"):
                for n in (300000, 3000000):
                    L.append(f"i1 {lab} merged5 {r} {V2_PROF} {o} {n} 0 20|{sub}")
            for o in ("iid", "bursty"):
                L.append(f"i2 {lab} q7 {r} learning {o} 3000000 0 10|{sub}")
            for o in ("iid", "real"):
                L.append(f"i2 {lab} merged5 {r} learning {o} 3000000 0 10|{sub}")
    return L


if __name__ == "__main__":
    which = sys.argv[1]
    L = lines(which)
    with open(os.path.join(HERE, f"tasks_v3_{which}.txt"), "w") as f:
        f.write("\n".join(L) + "\n")
    print(which, len(L))
