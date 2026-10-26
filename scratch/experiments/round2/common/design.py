"""Theorem-defined constants (single source of truth).

Private_information_setting.tex, lines 10 to 19:
  L_n = min{ floor(n/(2K)), ceil(n^(2/3) (log(e n))^(1/3)) }
  N_n = n - K L_n
  s_n = sqrt( log(2 K n^4) / (2 L_n) )
  b_n(r) = sqrt( r log(2 n^4) / 2 )
  switch after primary pull r iff Z_r < r tau - b_n(r)   (strict)
appendix_private.tex, lines 34 to 40 (fallback EXP3): gamma = min{1/2, sqrt(K log K / H)}, eta = gamma / K;
appendix_private.tex line 6: R_K(H) = 3 sqrt(K H log K) + 2 K log K, R_K(0) = 0.
contextual_samf_algorithm.tex: Grid-UCB h = (log(e n)/n)^(1/(D+2)); Grid-ETC h = n^(-1/(D+3)), q = ceil(n^(2/(D+3))).
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Design:
    n: int
    K: int
    L: int
    N: int
    s: float
    log2n4: float  # log(2 n^4), the monitor's confidence term

    def b(self, r):
        """Monitor boundary b_n(r) = sqrt(r log(2 n^4) / 2); accepts scalars or arrays."""
        import numpy as np
        return np.sqrt(np.asarray(r, dtype=float) * self.log2n4 / 2.0)

    def switch(self, r: int, Z: float, tau: float) -> bool:
        """Strict monitor test after primary pull r with reward sum Z."""
        return Z < r * tau - math.sqrt(r * self.log2n4 / 2.0)


def bidding_length(n: int, K: int) -> int:
    return min(n // (2 * K), math.ceil(n ** (2.0 / 3.0) * math.log(math.e * n) ** (1.0 / 3.0)))


def design(n: int, K: int, L: int | None = None) -> Design:
    """Mechanism constants. `L` overrides L_n for the bidding-length ablation (s_n is recomputed from L)."""
    if n < 2 * K:
        raise ValueError("MESP is defined for n >= 2K")
    if L is None:
        L = bidding_length(n, K)
    if L < 1 or K * L > n:
        raise ValueError("bidding length out of range")
    N = n - K * L
    s = math.sqrt(math.log(2 * K * n ** 4) / (2 * L))
    return Design(n=n, K=K, L=L, N=N, s=s, log2n4=math.log(2 * n ** 4))


def price(beta_second: float, s: float, mode: str = "conservative") -> float:
    """tau = (beta_(2) - s_n)_+ (mode 'conservative'); 'raw' gives beta_(2) (ablation R2)."""
    if mode == "conservative":
        return max(0.0, beta_second - s)
    if mode == "raw":
        return float(beta_second)
    raise ValueError(mode)


def exp3_constants(K: int, H: int) -> tuple[float, float]:
    if H <= 0:
        return 0.0, 0.0
    gamma = min(0.5, math.sqrt(K * math.log(K) / H))
    return gamma, gamma / K


def R_K(K: int, H: float) -> float:
    if H <= 0:
        return 0.0
    return 3.0 * math.sqrt(K * H * math.log(K)) + 2.0 * K * math.log(K)


def grid_ucb_width(n: int, D: int, mult: float = 1.0) -> float:
    return (math.log(math.e * n) / n) ** (1.0 / (D + 2)) * mult


def grid_etc(n: int, D: int, mult: float = 1.0, grid: str | None = None) -> tuple[float, int]:
    """Static Grid-ETC constants: cell side (per the grid rule) and q_n = ceil(n^(2/(D+3)))."""
    return grid_width(n, D, "etc", mult, grid), math.ceil(n ** (2.0 / (D + 3)))


def detection_delay(n: int, eps: float) -> float:
    """First-order crossing time of the cumulative monitor under a constant shortfall eps = tau - m."""
    return math.log(2 * n ** 4) / (2 * eps ** 2)


# Parametrizations requested by the main agent (17 September 2026) for the theory lead's pending candidates.

UCB_INDEX_DEFAULT = "horizon"   # main-agent decision, 17 September 2026: the anytime index is not pathwise monotone.


def ucb_bonus(T, t: int, n: int, index: str | None = None):
    """UCB exploration bonus. horizon (default): sqrt(4 log n / T) with the global horizon n and the agent's local
    count T; anytime: sqrt(2 log t / T) with t the instance's local time, retained for the comparison panel."""
    index = index or UCB_INDEX_DEFAULT
    import numpy as np
    T = np.maximum(np.asarray(T, dtype=float), 1.0)
    if index == "anytime":
        return np.sqrt(2.0 * math.log(max(t, 2)) / T)
    if index == "horizon":
        return np.sqrt(4.0 * math.log(n) / T)
    raise ValueError(index)


GRID_DEFAULT = "equalized"   # main-agent decision, 17 September 2026: exact tiling (the proof needs only a
# partition of the closed cube with a shrinking mesh). It removes the clipped last cell of the 'equal' rule and
# the never-committing regime of the 'dyadic' rule, both measured in the E3a pilot.


def grid_width(n: int, D: int, rule: str, mult: float = 1.0, grid: str | None = None) -> float:
    """Cell side length. rule 'etc': n^(-1/(D+3)); rule 'ucb': (log(en)/n)^(1/(D+2)).
    grid 'equal' uses that width with a clipped last cell; grid 'dyadic' uses 2^(-k_n) with
    k_n = ceil(log2(n)/(D+3)) (etc) or ceil(log2(n/log(en))/(D+2)) (ucb), so cells tile [0,1] exactly."""
    if grid == "equal":
        return (n ** (-1.0 / (D + 3)) if rule == "etc" else (math.log(math.e * n) / n) ** (1.0 / (D + 2))) * mult
    grid = grid or GRID_DEFAULT
    if grid == "equalized":
        # Exact tiling: b_n = round(1 / h_target) equal cells per axis, h = 1 / b_n. This removes the clipped last
        # cell of the 'equal' rule, whose thin cells are visited too rarely to finish exploring and are therefore
        # freely shadeable by an in-class deviator (measured in the E3a pilot).
        h0 = (n ** (-1.0 / (D + 3)) if rule == "etc" else (math.log(math.e * n) / n) ** (1.0 / (D + 2))) * mult
        return 1.0 / max(1, round(1.0 / h0))
    if grid == "dyadic":
        k = math.ceil(math.log2(n) / (D + 3)) if rule == "etc" else math.ceil(math.log2(n / math.log(math.e * n)) / (D + 2))
        return 2.0 ** (-k) * mult
    raise ValueError(grid)


def theorem_constant_nontop(n: int, K: int, delta: float, version: str = "revised") -> float:
    """Explicit finite-n constant for a NON-top deviator (capacity gap delta = V_i - M_i > 0).

    appendix_private.tex, equilibrium proof: the primary phase of a non-top winner lasts at most
    q <= 4 (1 + sqrt(2 log(2 n^4)))^2 / delta^2 pulls, each worth at most 2 utility, and its fallback utility is at
    most 2 R_K(n) / delta; Stage-1 effort saving is at most L_n. The proof's non-top branch additionally requires
    2 s_n <= delta / 2, which fails by many orders of magnitude at every horizon we can run when delta is small.
    The unquantified O(1) of the appendix is not included; the returned value is therefore a constant up to O(1).
    """
    d = design(n, K)
    q_max = 4.0 * (1.0 + math.sqrt(2.0 * math.log(2 * n ** 4))) ** 2 / delta ** 2
    base = d.L + 2.0 * float(d.b(n)) + R_K(K, n) + 2.0 * q_max + 2.0 * R_K(K, n) / delta
    return base if version == "revised" else base + 2.0 * n * d.s


def nontop_branch_active(n: int, K: int, delta: float) -> bool:
    """The proof's non-top branch needs 2 s_n <= delta / 2."""
    return 2.0 * design(n, K).s <= delta / 2.0


def theorem_constant_top(n: int, K: int, version: str = "revised") -> float:
    """Explicit finite-n constant of the top-agent equilibrium bound of Theorem thm:private-mesp.
    revised (theory lead, 17 September 2026): L_n + 2 b_n(n) + R_K(n); previous statement adds 2 n s_n."""
    d = design(n, K)
    base = d.L + 2.0 * float(d.b(n)) + R_K(K, n)
    if version == "revised":
        return base
    if version == "previous":
        return base + 2.0 * n * d.s
    raise ValueError(version)
