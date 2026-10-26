"""ctypes driver for the CG-MESP C kernel, plus the instance table and the mechanism's parameters.

The instance table is the affine form of INST in scratch/experiments/round2/ctx_local/cg_struct.py
(read-only reference): every capacity and intrinsic map there is affine in the agent's own context
coordinate, so (a, b) with M_j(x) = a + b x reproduces the lambdas exactly, and `p - q*x` and
`p + (-q)*x` are the same IEEE double.

All derived parameters (g, L, ell, s, rho, sigma) are computed HERE, in Python, exactly as the
reference computes them, and passed to C, so no parameter can differ between the two.
"""
from __future__ import annotations

import ctypes
import math
import os

import numpy as np

KMAX = 4
HERE = os.path.dirname(os.path.abspath(__file__))
_LIB = None

# name -> (K, Ma, Mb, mua, mub, honest set, Lipschitz constant)
INST = {
    "C": (2, [0.94, 0.80], [0.01, -0.02], [0.10, 0.30], [0.0, 0.0], {1}, 0.02),
    "D": (3, [0.94, 0.80, 0.78], [0.01, -0.02, 0.01], [0.10, 0.30, 0.20], [0.0, 0.0, 0.0], {1}, 0.02),
    "E": (2, [0.70, 0.90], [0.20, -0.20], [0.10, 0.25], [0.0, 0.0], {1}, 0.20),
    "F": (3, [0.90, 0.70, 0.68], [-0.05, 0.02, 0.02], [0.80, 0.10, 0.10], [-0.05, 0.0, 0.0], {0}, 0.05),
    # NEW IN THIS PACKAGE (A3): instance D extended by a fourth agent, so that D = K d = 4 can be
    # probed.  It is instance D with one more near-tied runner-up and is not used anywhere else.
    "G": (4, [0.94, 0.80, 0.78, 0.76], [0.01, -0.02, 0.01, -0.01],
          [0.10, 0.30, 0.20, 0.15], [0.0, 0.0, 0.0, 0.0], {1}, 0.02),
}
KIND = {None: 0, "underbid": 1, "rider": 2, "both": 3, "crash": 4, "sabotage": 5}
GRIDPTS = 21


class Cfg(ctypes.Structure):
    _fields_ = [("n", ctypes.c_int64), ("K", ctypes.c_int32), ("g", ctypes.c_int32),
                ("gridpts", ctypes.c_int32), ("L", ctypes.c_int64),
                ("ell", ctypes.c_double), ("s", ctypes.c_double), ("rho", ctypes.c_double),
                ("sig", ctypes.c_double),
                ("Ma", ctypes.c_double * KMAX), ("Mb", ctypes.c_double * KMAX),
                ("mua", ctypes.c_double * KMAX), ("mub", ctypes.c_double * KMAX),
                ("honest", ctypes.c_int32 * KMAX),
                ("dev", ctypes.c_int32), ("kind", ctypes.c_int32), ("joint", ctypes.c_int32),
                ("alpha_ride", ctypes.c_double), ("seed", ctypes.c_uint64),
                ("replay", ctypes.c_int32),
                ("Xrep", ctypes.POINTER(ctypes.c_double)), ("Urep", ctypes.POINTER(ctypes.c_double)),
                ("permrep", ctypes.POINTER(ctypes.c_int8)), ("fburep", ctypes.POINTER(ctypes.c_double)),
                ("fburep_len", ctypes.c_int64), ("permrep_len", ctypes.c_int64),
                # LAST field: the dimension of the context space the mechanism grids.  Appended at
                # the end so that libcgmesp.so and libcgmesp_v2.so, which predate it, see the same
                # layout for every field they read.
                ("dctx", ctypes.c_int32)]


class Out(ctypes.Structure):
    _fields_ = [("util", ctypes.c_double * KMAX), ("util_naive", ctypes.c_double * KMAX),
                ("bench2", ctypes.c_double), ("bench2_naive", ctypes.c_double),
                ("benchb", ctypes.c_double), ("benchb_naive", ctypes.c_double),
                ("rev", ctypes.c_uint64), ("rev_stage1", ctypes.c_uint64),
                ("rev_stage2", ctypes.c_uint64), ("rev_stage3", ctypes.c_uint64),
                ("stage1", ctypes.c_int64), ("stage2", ctypes.c_int64), ("stage3", ctypes.c_int64),
                ("awarded", ctypes.c_int64), ("switches", ctypes.c_int64),
                ("false_switches", ctypes.c_int64), ("viol_P2", ctypes.c_int64),
                ("viol_P4", ctypes.c_int64), ("ncells", ctypes.c_int64),
                ("perm_count", ctypes.c_int64), ("fbu_count", ctypes.c_int64),
                ("tau_sum", ctypes.c_double), ("tau_max", ctypes.c_double),
                ("tau_pos", ctypes.c_int64), ("status", ctypes.c_int64)]


def lib():
    global _LIB
    if _LIB is None:
        # CGMESP_LIB selects the kernel build: libcgmesp.so (v1, the layout the verification suite
        # was first run against) or libcgmesp_v2.so (same arithmetic, cache-friendly layout and a
        # one-round software pipeline).  The two are checked bit for bit against each other.
        _LIB = ctypes.CDLL(os.path.join(HERE, os.environ.get("CGMESP_LIB", "libcgmesp.so")))
        _LIB.cg_run.restype = ctypes.c_int
        _LIB.cg_run.argtypes = [ctypes.POINTER(Cfg), ctypes.POINTER(Out),
                                ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int64),
                                ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(ctypes.c_int64)]
    return _LIB


def mech_params(name, n, tuned=True, g=None, Lbid=None, osc_mult=3.0, d=None):
    """The parameter block at the top of run() in ctx_local/cg_struct.py, with the dimension of the
    gridded context space made explicit.  `d` is that dimension: the revised model has one common
    context in [0,1)^d shared by all K agents, so every constant carries d and not K d.  Leaving
    `d` unset reproduces the earlier per-agent-context reading, d = K."""
    K = INST[name][0]
    Llip = INST[name][6]
    D = K if d is None else int(d)
    if tuned:
        g = math.ceil(n ** (1.0 / (D + 3)))
        Lbid = math.ceil(n ** (2.0 / (D + 3)))
    h = 1.0 / g
    ell = math.log(2 * K) + 5 * math.log(n)
    s = math.sqrt(ell / (2 * Lbid))
    rho = (math.sqrt(D) * h * math.log(math.e * n)) if tuned else (osc_mult * Llip * math.sqrt(D) * h)
    sig = 3 * s + rho
    return dict(K=K, D=D, g=g, L=Lbid, h=h, ell=ell, s=s, rho=rho, sigma=sig, L_lip=Llip)


def run(name, n, tuned=True, g=None, Lbid=None, osc_mult=3.0, dev=None, kind=None,
        alpha_ride=0.5, seed=0, joint=False, replay=None, want_tau=True, d=None,
        rho_override=None):
    """One CG-MESP episode through the C kernel.  `replay` is a dict of recorded numpy draws.
    `d` is the dimension of the common context space; None means d = K, the earlier reading."""
    K, Ma, Mb, mua, mub, honest, Llip = INST[name]
    P = mech_params(name, n, tuned, g, Lbid, osc_mult, d)
    DC = K if d is None else int(d)
    if rho_override is not None:
        # used only by verify_d1.py, which must hand the kernel the exact double the reference
        # computed for rho; the two expressions for rho_n agree to the last bit only by luck.
        P["rho"] = float(rho_override)
        P["sigma"] = 3 * P["s"] + P["rho"]
    cf = Cfg()
    cf.n = int(n); cf.K = K; cf.g = int(P["g"]); cf.gridpts = GRIDPTS; cf.L = int(P["L"])
    cf.ell = P["ell"]; cf.s = P["s"]; cf.rho = P["rho"]; cf.sig = P["sigma"]
    for j in range(K):
        cf.Ma[j] = Ma[j]; cf.Mb[j] = Mb[j]; cf.mua[j] = mua[j]; cf.mub[j] = mub[j]
        cf.honest[j] = 1 if j in honest else 0
    cf.dev = -1 if (dev is None or joint) else int(dev)
    cf.kind = KIND[kind]; cf.joint = 1 if joint else 0
    cf.alpha_ride = float(alpha_ride); cf.seed = int(seed); cf.dctx = DC

    keep = []
    if replay is None:
        cf.replay = 0
        cf.Xrep = None; cf.Urep = None; cf.permrep = None; cf.fburep = None
        cf.fburep_len = 0; cf.permrep_len = 0
    else:
        cf.replay = 1
        X = np.ascontiguousarray(replay["X"], dtype=np.float64)
        U = np.ascontiguousarray(replay["U"], dtype=np.float64)
        PM = np.ascontiguousarray(replay["perms"], dtype=np.int8)
        FB = np.ascontiguousarray(replay["fbu"], dtype=np.float64)
        keep = [X, U, PM, FB]
        cf.Xrep = X.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        cf.Urep = U.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        cf.permrep = PM.ctypes.data_as(ctypes.POINTER(ctypes.c_int8))
        cf.fburep = FB.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        cf.permrep_len = PM.shape[0]; cf.fburep_len = FB.shape[0]

    J = int(P["g"]) ** DC
    tau = np.full(J, np.nan) if want_tau else None
    tix = np.full(J, -1, dtype=np.int64) if want_tau else None
    vis = np.zeros(J, dtype=np.int64) if want_tau else None
    o = Out()
    rc = lib().cg_run(ctypes.byref(cf), ctypes.byref(o),
                      tau.ctypes.data_as(ctypes.POINTER(ctypes.c_double)) if want_tau else None,
                      tix.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)) if want_tau else None,
                      vis.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)) if want_tau else None,
                      None)
    del keep
    if rc != 0:
        raise RuntimeError(f"cg_run returned {rc}")
    aw = int(o.awarded)
    taus = tau[:aw].copy() if want_tau else np.zeros(0)
    Jp = int(o.ncells)
    e_bid = min(Jp * P["L"], n)
    e_stage1 = min(K * Jp * P["L"], n)
    e_osc = n * P["rho"]
    e_mon = Jp + 2 * math.sqrt(Jp * n * P["ell"] / 2)
    e_fb = 11 * math.sqrt(2 * K * Jp * n * math.log(K)) + 2 * K * math.log(K) * Jp * math.log2(2 * (n + 1))
    e_price = n * (4 * P["s"] + (4.0 / 3.0) * P["rho"])
    e_rob = n * (4 * P["s"] + (5.0 / 3.0) * P["rho"])
    res = dict(inst=name, n=int(n), K=K, D=DC, d=DC, g=int(P["g"]), L=int(P["L"]), J=Jp, h=P["h"],
               s=P["s"], rho=P["rho"], sigma=P["sigma"], ell=P["ell"],
               tuned=int(tuned), osc_mult=(None if tuned else osc_mult),
               dev=(None if dev is None else int(dev)), kind=kind, alpha_ride=alpha_ride,
               joint=int(joint), seed=int(seed),
               u0=float(o.util[0]), util=[float(o.util[j]) for j in range(K)],
               util_naive=[float(o.util_naive[j]) for j in range(K)],
               rev=float(o.rev), rev_int=int(o.rev),
               rev_stage1=int(o.rev_stage1), rev_stage2=int(o.rev_stage2), rev_stage3=int(o.rev_stage3),
               stage1=int(o.stage1), stage2=int(o.stage2), stage3=int(o.stage3),
               awarded=aw, switches=int(o.switches), false_switches=int(o.false_switches),
               viol_P2=int(o.viol_P2), viol_P4=int(o.viol_P4),
               mean_tau=float(np.mean(taus)) if aw else 0.0,
               max_tau=float(o.tau_max) if aw else float("nan"),
               tau_pos=int(o.tau_pos),
               positive_price_share=(float(o.tau_pos) / aw) if aw else float("nan"),
               zero_price_share=float(np.mean([tt <= 0 for tt in taus])) if aw else float("nan"),
               bench_M2=float(o.bench2), bench_honest=float(o.benchb),
               bench_M2_naive=float(o.bench2_naive), bench_honest_naive=float(o.benchb_naive),
               boundA=e_bid + e_osc + e_mon + e_fb, slackB=e_stage1 + e_price,
               slackC=e_stage1 + e_rob + e_mon + e_fb,
               e_bid=e_bid, e_stage1=e_stage1, e_osc=e_osc, e_mon=e_mon, e_fb=e_fb,
               e_price=e_price, e_rob=e_rob)
    res["_taus"] = taus
    res["_tauidx"] = tix[:aw].copy() if want_tau else None
    res["_visits"] = vis if want_tau else None
    return res
