/* CG-MESP, the continuous-context mechanism, as a constant-work-per-round C kernel.
 *
 * v3 adds `dctx`, the dimension of the CONTEXT SPACE the mechanism grids, which the revised model
 * (one common context per round, shared by all K agents) separates from K.  The grid is over
 * [0,1)^dctx and has g^dctx cells; agent j's capacity and intrinsic mean are read at coordinate
 * `j % dctx` of the round's context.  With dctx = K this is exactly the previous per-agent-context
 * model and reproduces v1 and v2 bit for bit; with dctx = 1 every agent reads the same coordinate,
 * which is the common-context model.  `dctx` is the LAST field of cfg_t so that the older builds,
 * which do not know about it, see an unchanged layout.
 *
 * This is a line-for-line port of run() in scratch/experiments/round2/ctx_local/cg_struct.py
 * (read-only reference).  It exists only because the reference cannot reach the horizons at which
 * the mechanism's own thresholds say its guarantees start to say anything (PROVER2.md Section 18:
 * D = 2 needs n of order 10^9.8).
 *
 * Two modes:
 *   replay  = 1 : every random draw is read from an array recorded from the reference's own
 *                 numpy Generator.  Used to prove bit-equality with the reference.
 *   replay  = 0 : draws come from three independent xoshiro256++ streams (contexts, seeds,
 *                 mechanism).  Three streams, not one, so that the context path and the Bernoulli
 *                 seeds are identical across deviation runs at a fixed seed, which is the pairing
 *                 the reference gets from pre-drawing Xs and U.
 *
 * Numerics at 10^10 rounds:
 *   - every reward sum (rev, per-cell Z, per-cell Stage-1 sums) is a uint64/int64 counter, because
 *     rewards are 0 or 1.  No floating-point drift is possible in the monitor or in revenue.
 *   - the two benchmark sums and the K utility sums are accumulated BOTH naively (to reproduce the
 *     reference bit for bit) and by Neumaier compensated summation (to report a trustworthy value
 *     at 10^10 rounds).  Both are returned; their difference is a diagnostic.
 *
 * Evidence category: SYNTHETIC SIMULATION.  Deviation values are lower bounds on exploitability
 * for the deviations tried.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/mman.h>

#define KMAX 4

/* ------------------------------------------------------------------ xoshiro256++ */
static inline uint64_t rotl64(const uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
typedef struct { uint64_t s[4]; } rng_t;
static inline uint64_t splitmix64(uint64_t *x) {
    uint64_t z = (*x += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
static void rng_seed(rng_t *r, uint64_t seed, uint64_t stream) {
    uint64_t x = seed * 0x9E3779B97F4A7C15ULL + stream * 0xD1B54A32D192ED03ULL + 0x853C49E6748FEA9BULL;
    for (int i = 0; i < 4; i++) r->s[i] = splitmix64(&x);
    for (int i = 0; i < 32; i++) {  /* warm up */
        const uint64_t t = r->s[1] << 17;
        r->s[2] ^= r->s[0]; r->s[3] ^= r->s[1]; r->s[1] ^= r->s[2]; r->s[0] ^= r->s[3];
        r->s[2] ^= t; r->s[3] = rotl64(r->s[3], 45);
    }
}
static inline uint64_t rng_next(rng_t *r) {
    const uint64_t result = rotl64(r->s[0] + r->s[3], 23) + r->s[0];
    const uint64_t t = r->s[1] << 17;
    r->s[2] ^= r->s[0]; r->s[3] ^= r->s[1]; r->s[1] ^= r->s[2]; r->s[0] ^= r->s[3];
    r->s[2] ^= t; r->s[3] = rotl64(r->s[3], 45);
    return result;
}
/* same 53-bit construction numpy's Generator.random() uses */
static inline double rng_double(rng_t *r) { return (double)(rng_next(r) >> 11) * 0x1.0p-53; }

/* ------------------------------------------------------------------ Neumaier sum */
typedef struct { double s, c; } nsum_t;
static inline void nadd(nsum_t *a, double v) {
    double t = a->s + v;
    if (fabs(a->s) >= fabs(v)) a->c += (a->s - t) + v; else a->c += (v - t) + a->s;
    a->s = t;
}
static inline double nval(const nsum_t *a) { return a->s + a->c; }

/* ------------------------------------------------------------------ cell, split hot / cold
 *
 * v2 differs from v1 (cgmesp.c) only in memory layout and in software pipelining; it computes the
 * same numbers by the same operations in the same order, and the two are checked bit for bit.
 * The grid has up to a few million cells at the horizons this sweep reaches, so the cell array is
 * far larger than the last-level cache and every round is a random access into it.  The fields a
 * Stage-2 round touches are packed into one 64-byte line (`hot_t`); the Stage-1 bid counters and
 * the Stage-3 EXP3 weights, which are touched in a few per cent of rounds at large n, live in a
 * second array (`cold_t`).  The next round's arrival is drawn one round early, from its own
 * independent stream, purely so that its cell can be prefetched; the drawn values are unchanged.
 */
typedef struct {
    int64_t V, r, Z;
    double  tau, minm;
    int32_t ph, W;
    uint8_t created;
    uint8_t pad[15];
} hot_t;

typedef struct {
    int64_t sm[KMAX];
    double  w[KMAX];
    int64_t fb;
    int32_t ep;
    int8_t  prio[KMAX];
} cold_t;

/* ------------------------------------------------------------------ config / output */
typedef struct {
    int64_t n;
    int32_t K, g, gridpts;
    int64_t L;
    double ell, s, rho, sig;
    double Ma[KMAX], Mb[KMAX], mua[KMAX], mub[KMAX];
    int32_t honest[KMAX];
    int32_t dev, kind, joint;
    double alpha_ride;
    uint64_t seed;
    int32_t replay;
    const double *Xrep;
    const double *Urep;
    const int8_t *permrep;
    const double *fburep;
    int64_t fburep_len, permrep_len;
    int32_t dctx;                 /* LAST: dimension of the context space; 0 or K means "as before" */
} cfg_t;

typedef struct {
    double util[KMAX], util_naive[KMAX];
    double bench2, bench2_naive, benchb, benchb_naive;
    uint64_t rev, rev_stage1, rev_stage2, rev_stage3;
    int64_t stage1, stage2, stage3;
    int64_t awarded, switches, false_switches, viol_P2, viol_P4;
    int64_t ncells, perm_count, fbu_count;
    double tau_sum, tau_max;
    int64_t tau_pos;
    int64_t status;
} out_t;

/* kind codes: 0 none, 1 underbid, 2 rider, 3 both, 4 crash, 5 sabotage */

int cg_run(const cfg_t *cf, out_t *o, double *tau_out, int64_t *tauidx_out,
           int64_t *visits_out, int64_t *r_out)
{
    const int K = cf->K, G = cf->g, GP = cf->gridpts;
    const int64_t n = cf->n, L = cf->L;
    const double h = 1.0 / (double)G, ell = cf->ell, s = cf->s, rho = cf->rho, sig = cf->sig;
    if (K > KMAX || K < 1) return 1;

    const int DC = (cf->dctx > 0) ? cf->dctx : K;
    if (DC > KMAX) return 6;
    int64_t J = 1;
    for (int j = 0; j < DC; j++) { J *= (int64_t)G; if (J > 200000000LL) return 2; }

    /* 2 MB-aligned and hinted for transparent huge pages: the cell array is hundreds of megabytes
     * at these horizons and a 4 kB-page random walk over it thrashes the TLB. */
    size_t hbytes = ((size_t)J * sizeof(hot_t) + (2u << 20) - 1) & ~(size_t)((2u << 20) - 1);
    size_t cbytes = ((size_t)J * sizeof(cold_t) + (2u << 20) - 1) & ~(size_t)((2u << 20) - 1);
    hot_t *hot = (hot_t *)aligned_alloc(2u << 20, hbytes);
    cold_t *cold = (cold_t *)aligned_alloc(2u << 20, cbytes);
    if (!hot || !cold) { free(hot); free(cold); return 3; }
#ifdef MADV_HUGEPAGE
    madvise(hot, hbytes, MADV_HUGEPAGE);
    madvise(cold, cbytes, MADV_HUGEPAGE);
#endif
    memset(hot, 0, hbytes);
    memset(cold, 0, cbytes);
    memset(o, 0, sizeof(out_t));
    o->tau_max = -INFINITY;

    /* deviator set, exactly as in the reference */
    int devs[KMAX]; for (int j = 0; j < K; j++) devs[j] = 0;
    if (cf->joint) { for (int j = 0; j < K; j++) if (!cf->honest[j]) devs[j] = 1; }
    else if (cf->dev >= 0) devs[cf->dev] = 1;
    const int kind = cf->kind;
    const int checkP4 = (cf->dev < 0 && !cf->joint);

    rng_t rx, ru, rm;
    rng_seed(&rx, cf->seed, 1); rng_seed(&ru, cf->seed, 2); rng_seed(&rm, cf->seed, 3);

    nsum_t nb2 = {0,0}, nbb = {0,0}, nut[KMAX];
    double b2_naive = 0.0, bb_naive = 0.0, ut_naive[KMAX];
    for (int j = 0; j < K; j++) { nut[j].s = 0; nut[j].c = 0; ut_naive[j] = 0.0; }

    double Mv[KMAX], mv[KMAX], beta[KMAX], p[KMAX], cdf[KMAX];
    int64_t ncells = 0, permc = 0, fbuc = 0;

    /* arrivals are drawn PD rounds ahead, from their own stream, purely so that the cell they will
     * land in can be prefetched; the drawn values and their order are unchanged. */
#define PD 8            /* rounds of lookahead */
#define PB 16           /* ring size, strictly greater than PD so the live slot is never overwritten */
#define PM (PB - 1)
    static const int pd = PD;
    double Xb[PB][KMAX];
    int keyb[PB][KMAX];
    int64_t idxb[PB];
    for (int64_t q = 0; q < pd && q < n; q++) {
        int64_t ix = 0;
        for (int j = 0; j < DC; j++)
            Xb[q][j] = cf->replay ? cf->Xrep[q * DC + j] : rng_double(&rx);
        for (int j = 0; j < DC; j++) {
            int k = (int)(Xb[q][j] / h); if (k > G - 1) k = G - 1;
            keyb[q][j] = k; ix = ix * G + k;
        }
        idxb[q] = ix;
        __builtin_prefetch(&hot[ix], 1, 3);
    }

    for (int64_t t = 0; t < n; t++) {
        const int slot = (int)(t & PM);
        const double *X = Xb[slot];
        const int *key = keyb[slot];
        const int64_t idx = idxb[slot];
        const int64_t tf = t + pd;
        if (tf < n) {                      /* draw the arrival PD rounds ahead and prefetch its cell */
            int fs = (int)(tf & PM);
            int64_t ix = 0;
            for (int j = 0; j < DC; j++)
                Xb[fs][j] = cf->replay ? cf->Xrep[tf * DC + j] : rng_double(&rx);
            for (int j = 0; j < DC; j++) {
                int k = (int)(Xb[fs][j] / h); if (k > G - 1) k = G - 1;
                keyb[fs][j] = k; ix = ix * G + k;
            }
            idxb[fs] = ix;
            __builtin_prefetch(&hot[ix], 1, 3);
            __builtin_prefetch(&cold[ix], 1, 1);
        }
        const double Ut = cf->replay ? cf->Urep[t] : rng_double(&ru);

        hot_t *hc = &hot[idx];
        cold_t *cc = &cold[idx];
        if (!hc->created) {
            hc->created = 1; hc->ph = 1; hc->tau = 0.0; hc->W = -1; cc->ep = -1;
            hc->minm = INFINITY;
            for (int j = 0; j < K; j++) { cc->sm[j] = 0; cc->w[j] = 1.0; }
            if (cf->replay) {
                if (permc >= cf->permrep_len) { free(hot); free(cold); return 4; }
                for (int j = 0; j < K; j++) cc->prio[j] = cf->permrep[permc * K + j];
            } else {  /* Fisher-Yates */
                int8_t pr[KMAX]; for (int j = 0; j < K; j++) pr[j] = (int8_t)j;
                for (int j = K - 1; j > 0; j--) {
                    int q = (int)(rng_double(&rm) * (double)(j + 1));
                    if (q > j) q = j;
                    int8_t tmp = pr[j]; pr[j] = pr[q]; pr[q] = tmp;
                }
                for (int j = 0; j < K; j++) cc->prio[j] = pr[j];
            }
            permc++; ncells++;
        }
        hc->V += 1;

        for (int j = 0; j < K; j++) {
            const double xj = X[j % DC];
            Mv[j] = cf->Ma[j] + cf->Mb[j] * xj;
            mv[j] = cf->mua[j] + cf->mub[j] * xj;
        }
        /* second largest capacity */
        double m1 = -INFINITY, m2 = -INFINITY;
        for (int j = 0; j < K; j++) {
            if (Mv[j] > m1) { m2 = m1; m1 = Mv[j]; } else if (Mv[j] > m2) { m2 = Mv[j]; }
        }
        nadd(&nb2, m2); b2_naive += m2;
        double bh = -INFINITY;
        for (int j = 0; j < K; j++) if (cf->honest[j] && mv[j] > bh) bh = mv[j];
        nadd(&nbb, bh); bb_naive += bh;

        if (hc->ph == 1) {
            int i = (int)((hc->V - 1) % K);
            double m = Mv[i];
            if (devs[i] && (kind == 1 || kind == 3 || kind == 5)) {
                if (kind == 5) m = cf->honest[i] ? mv[i] : 0.0;
                else {
                    double alt = -INFINITY;
                    for (int j = 0; j < K; j++) if (j != i && Mv[j] > alt) alt = Mv[j];
                    double flr = cf->honest[i] ? mv[i] : 0.0;
                    double mid = 0.5 * (Mv[i] + alt);
                    double hi = (flr > mid) ? flr : mid;
                    m = (Mv[i] < hi) ? Mv[i] : hi;
                }
            }
            int y = (Ut <= m) ? 1 : 0;
            cc->sm[i] += y;
            o->rev += (uint64_t)y; o->rev_stage1 += (uint64_t)y;
            double du = (1.0 + mv[i]) - m;
            nadd(&nut[i], du); ut_naive[i] += du;
            o->stage1 += 1;
            if (hc->V == (int64_t)K * L) {
                for (int j = 0; j < K; j++) beta[j] = (double)cc->sm[j] / (double)L;
                int W = 0;
                for (int j = 1; j < K; j++)
                    if (beta[j] > beta[W] || (beta[j] == beta[W] && cc->prio[j] > cc->prio[W])) W = j;
                double b1 = -INFINITY, b2 = -INFINITY;
                for (int j = 0; j < K; j++) {
                    if (beta[j] > b1) { b2 = b1; b1 = beta[j]; } else if (beta[j] > b2) { b2 = beta[j]; }
                }
                double tau = b2 - sig; if (tau < 0.0) tau = 0.0;
                hc->W = W; hc->tau = tau; hc->ph = 2;
                if (tau_out) tau_out[o->awarded] = tau;
                if (tauidx_out) tauidx_out[o->awarded] = idx;
                o->awarded += 1;
                o->tau_sum += tau; if (tau > 0.0) o->tau_pos += 1;
                if (tau > o->tau_max) o->tau_max = tau;
                /* Lemma P2: the winner can meet the price at every context of its cube */
                {
                    double start = (double)key[W % DC] * h, stop = start + h;
                    double delta = stop - start, step = delta / (double)(GP - 1);
                    double mn = INFINITY;
                    for (int a = 0; a < GP; a++) {
                        double v = (a == GP - 1) ? stop : ((double)a * step + start);
                        double MM = cf->Ma[W] + cf->Mb[W] * v;
                        if (MM < mn) mn = MM;
                    }
                    if (tau > mn + 1e-12) o->viol_P2 += 1;
                }
                /* Lemma P4: the price is not far below the second capacity */
                if (checkP4) {
                    double worst = -INFINITY;
                    for (int a = 0; a < GP; a++) {
                        double off = h * (double)a / (double)(GP - 1);
                        double w1 = -INFINITY, w2 = -INFINITY;
                        for (int j = 0; j < K; j++) {
                            double vv = cf->Ma[j] + cf->Mb[j] * ((double)key[j % DC] * h + off);
                            if (vv > w1) { w2 = w1; w1 = vv; } else if (vv > w2) { w2 = vv; }
                        }
                        if (w2 > worst) worst = w2;
                    }
                    if (tau < worst - 4.0 * s - (4.0 / 3.0) * rho - 1e-12) o->viol_P4 += 1;
                }
            }
            goto next_round;
        }

        if (hc->ph == 2) {
            const int W = hc->W; const double tau = hc->tau;
            double m = (tau < Mv[W]) ? tau : Mv[W];
            if (cf->honest[W] && mv[W] > m) m = mv[W];
            if (devs[W] && (kind == 2 || kind == 3)) {
                double br = (hc->r > 0) ? sqrt((double)hc->r * ell / 2.0) : 0.0;
                double br1 = sqrt((double)(hc->r + 1) * ell / 2.0);
                double inc = br1 - br;
                double lo = tau - cf->alpha_ride * inc; if (lo < 0.0) lo = 0.0;
                m = (lo < Mv[W]) ? lo : Mv[W];
                if (cf->honest[W] && m < mv[W]) m = mv[W];
            } else if (devs[W] && (kind == 4 || kind == 5)) {
                m = cf->honest[W] ? mv[W] : 0.0;
            }
            if (m < hc->minm) hc->minm = m;
            int y = (Ut <= m) ? 1 : 0;
            hc->r += 1; hc->Z += y;
            o->rev += (uint64_t)y; o->rev_stage2 += (uint64_t)y; o->stage2 += 1;
            double du = (1.0 + mv[W]) - m;
            nadd(&nut[W], du); ut_naive[W] += du;
            double br = (hc->r > 0) ? sqrt((double)hc->r * ell / 2.0) : 0.0;
            if ((double)hc->Z < (double)hc->r * tau - br) {
                hc->ph = 3; cc->fb = 0; o->switches += 1;
                if (hc->minm >= tau - 1e-12) o->false_switches += 1;
            }
            goto next_round;
        }

        /* Stage 3: fresh EXP3 fallback, doubling epochs */
        cc->fb += 1;
        {
            int64_t sd = cc->fb;
            int k = 0; { int64_t v = sd; while (v > 1) { v >>= 1; k++; } }
            if ((1LL << k) == sd) { for (int j = 0; j < K; j++) cc->w[j] = 1.0; cc->ep = k; }
            double gam = sqrt((double)K * log((double)K) / (double)(1LL << cc->ep));
            if (gam > 0.5) gam = 0.5;
            double eta = gam / (double)K;
            double wsum = 0.0; for (int j = 0; j < K; j++) wsum += cc->w[j];
            for (int j = 0; j < K; j++) p[j] = (1.0 - gam) * (cc->w[j] / wsum) + gam / (double)K;
            double u;
            if (cf->replay) {
                if (fbuc >= cf->fburep_len) { free(hot); free(cold); return 5; }
                u = cf->fburep[fbuc];
            } else u = rng_double(&rm);
            fbuc++;
            /* numpy Generator.choice(K, p=p): cdf = p.cumsum(); cdf /= cdf[-1];
               idx = cdf.searchsorted(u, 'right') clipped to K-1  */
            double acc = 0.0;
            for (int j = 0; j < K; j++) { acc += p[j]; cdf[j] = acc; }
            for (int j = 0; j < K; j++) cdf[j] /= cdf[K - 1];
            int Ia = 0; while (Ia < K && cdf[Ia] <= u) Ia++;
            if (Ia > K - 1) Ia = K - 1;
            double m = Mv[Ia];
            if (devs[Ia] && kind == 5) m = cf->honest[Ia] ? mv[Ia] : 0.0;
            int y = (Ut <= m) ? 1 : 0;
            if (y) cc->w[Ia] *= exp(eta * ((double)y / p[Ia]));
            double wmax = 0.0; for (int j = 0; j < K; j++) if (cc->w[j] > wmax) wmax = cc->w[j];
            for (int j = 0; j < K; j++) cc->w[j] /= wmax;
            o->rev += (uint64_t)y; o->rev_stage3 += (uint64_t)y; o->stage3 += 1;
            double du = (1.0 + mv[Ia]) - m;
            nadd(&nut[Ia], du); ut_naive[Ia] += du;
        }
    next_round: ;
    }
#undef PD
#undef PB
#undef PM

    for (int j = 0; j < K; j++) { o->util[j] = nval(&nut[j]); o->util_naive[j] = ut_naive[j]; }
    o->bench2 = nval(&nb2); o->bench2_naive = b2_naive;
    o->benchb = nval(&nbb); o->benchb_naive = bb_naive;
    o->ncells = ncells; o->perm_count = permc; o->fbu_count = fbuc;
    if (visits_out || r_out) {
        for (int64_t i = 0; i < J; i++) {
            if (visits_out) visits_out[i] = hot[i].V;
            if (r_out) r_out[i] = hot[i].r;
        }
    }
    free(hot); free(cold);
    o->status = 0;
    return 0;
}
