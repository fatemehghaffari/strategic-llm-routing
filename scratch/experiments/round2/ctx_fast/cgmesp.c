/* CG-MESP, the continuous-context mechanism, as a constant-work-per-round C kernel.
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

/* ------------------------------------------------------------------ cell */
typedef struct {
    int64_t V;
    int64_t sm[KMAX];
    int64_t r;
    int64_t Z;
    int64_t fb;
    double  tau;
    double  minm;
    double  w[KMAX];
    int32_t ph;
    int32_t W;
    int32_t ep;
    int8_t  prio[KMAX];
    uint8_t created;
} cell_t;

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

    int64_t J = 1;
    for (int j = 0; j < K; j++) { J *= (int64_t)G; if (J > 200000000LL) return 2; }

    cell_t *cells = (cell_t *)calloc((size_t)J, sizeof(cell_t));
    if (!cells) return 3;
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

    double X[KMAX], Mv[KMAX], mv[KMAX], beta[KMAX], p[KMAX], cdf[KMAX];
    int key[KMAX];
    int64_t ncells = 0, permc = 0, fbuc = 0;

    for (int64_t t = 0; t < n; t++) {
        /* ---- arrival and the round's seed */
        if (cf->replay) {
            for (int j = 0; j < K; j++) X[j] = cf->Xrep[t * K + j];
        } else {
            for (int j = 0; j < K; j++) X[j] = rng_double(&rx);
        }
        const double Ut = cf->replay ? cf->Urep[t] : rng_double(&ru);

        int64_t idx = 0;
        for (int j = 0; j < K; j++) {
            int k = (int)(X[j] / h);
            if (k > G - 1) k = G - 1;
            key[j] = k;
            idx = idx * G + k;
        }
        cell_t *c = &cells[idx];
        if (!c->created) {
            c->created = 1; c->ph = 1; c->tau = 0.0; c->W = -1; c->ep = -1;
            c->minm = INFINITY;
            for (int j = 0; j < K; j++) { c->sm[j] = 0; c->w[j] = 1.0; }
            if (cf->replay) {
                if (permc >= cf->permrep_len) { free(cells); return 4; }
                for (int j = 0; j < K; j++) c->prio[j] = cf->permrep[permc * K + j];
            } else {  /* Fisher-Yates */
                int8_t pr[KMAX]; for (int j = 0; j < K; j++) pr[j] = (int8_t)j;
                for (int j = K - 1; j > 0; j--) {
                    int q = (int)(rng_double(&rm) * (double)(j + 1));
                    if (q > j) q = j;
                    int8_t tmp = pr[j]; pr[j] = pr[q]; pr[q] = tmp;
                }
                for (int j = 0; j < K; j++) c->prio[j] = pr[j];
            }
            permc++; ncells++;
        }
        c->V += 1;

        for (int j = 0; j < K; j++) {
            Mv[j] = cf->Ma[j] + cf->Mb[j] * X[j];
            mv[j] = cf->mua[j] + cf->mub[j] * X[j];
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

        if (c->ph == 1) {
            int i = (int)((c->V - 1) % K);
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
            c->sm[i] += y;
            o->rev += (uint64_t)y; o->rev_stage1 += (uint64_t)y;
            double du = (1.0 + mv[i]) - m;
            nadd(&nut[i], du); ut_naive[i] += du;
            o->stage1 += 1;
            if (c->V == (int64_t)K * L) {
                for (int j = 0; j < K; j++) beta[j] = (double)c->sm[j] / (double)L;
                int W = 0;
                for (int j = 1; j < K; j++)
                    if (beta[j] > beta[W] || (beta[j] == beta[W] && c->prio[j] > c->prio[W])) W = j;
                double b1 = -INFINITY, b2 = -INFINITY;
                for (int j = 0; j < K; j++) {
                    if (beta[j] > b1) { b2 = b1; b1 = beta[j]; } else if (beta[j] > b2) { b2 = beta[j]; }
                }
                double tau = b2 - sig; if (tau < 0.0) tau = 0.0;
                c->W = W; c->tau = tau; c->ph = 2;
                if (tau_out) tau_out[o->awarded] = tau;
                if (tauidx_out) tauidx_out[o->awarded] = idx;
                o->awarded += 1;
                o->tau_sum += tau; if (tau > 0.0) o->tau_pos += 1;
                if (tau > o->tau_max) o->tau_max = tau;
                /* Lemma P2: the winner can meet the price at every context of its cube */
                {
                    double start = (double)key[W] * h, stop = start + h;
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
                            double vv = cf->Ma[j] + cf->Mb[j] * ((double)key[j] * h + off);
                            if (vv > w1) { w2 = w1; w1 = vv; } else if (vv > w2) { w2 = vv; }
                        }
                        if (w2 > worst) worst = w2;
                    }
                    if (tau < worst - 4.0 * s - (4.0 / 3.0) * rho - 1e-12) o->viol_P4 += 1;
                }
            }
            continue;
        }

        if (c->ph == 2) {
            const int W = c->W; const double tau = c->tau;
            double m = (tau < Mv[W]) ? tau : Mv[W];
            if (cf->honest[W] && mv[W] > m) m = mv[W];
            if (devs[W] && (kind == 2 || kind == 3)) {
                double br = (c->r > 0) ? sqrt((double)c->r * ell / 2.0) : 0.0;
                double br1 = sqrt((double)(c->r + 1) * ell / 2.0);
                double inc = br1 - br;
                double lo = tau - cf->alpha_ride * inc; if (lo < 0.0) lo = 0.0;
                m = (lo < Mv[W]) ? lo : Mv[W];
                if (cf->honest[W] && m < mv[W]) m = mv[W];
            } else if (devs[W] && (kind == 4 || kind == 5)) {
                m = cf->honest[W] ? mv[W] : 0.0;
            }
            if (m < c->minm) c->minm = m;
            int y = (Ut <= m) ? 1 : 0;
            c->r += 1; c->Z += y;
            o->rev += (uint64_t)y; o->rev_stage2 += (uint64_t)y; o->stage2 += 1;
            double du = (1.0 + mv[W]) - m;
            nadd(&nut[W], du); ut_naive[W] += du;
            double br = (c->r > 0) ? sqrt((double)c->r * ell / 2.0) : 0.0;
            if ((double)c->Z < (double)c->r * tau - br) {
                c->ph = 3; c->fb = 0; o->switches += 1;
                if (c->minm >= tau - 1e-12) o->false_switches += 1;
            }
            continue;
        }

        /* Stage 3: fresh EXP3 fallback, doubling epochs */
        c->fb += 1;
        {
            int64_t sd = c->fb;
            int k = 0; { int64_t v = sd; while (v > 1) { v >>= 1; k++; } }
            if ((1LL << k) == sd) { for (int j = 0; j < K; j++) c->w[j] = 1.0; c->ep = k; }
            double gam = sqrt((double)K * log((double)K) / (double)(1LL << c->ep));
            if (gam > 0.5) gam = 0.5;
            double eta = gam / (double)K;
            double wsum = 0.0; for (int j = 0; j < K; j++) wsum += c->w[j];
            for (int j = 0; j < K; j++) p[j] = (1.0 - gam) * (c->w[j] / wsum) + gam / (double)K;
            double u;
            if (cf->replay) {
                if (fbuc >= cf->fburep_len) { free(cells); return 5; }
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
            if (y) c->w[Ia] *= exp(eta * ((double)y / p[Ia]));
            double wmax = 0.0; for (int j = 0; j < K; j++) if (c->w[j] > wmax) wmax = c->w[j];
            for (int j = 0; j < K; j++) c->w[j] /= wmax;
            o->rev += (uint64_t)y; o->rev_stage3 += (uint64_t)y; o->stage3 += 1;
            double du = (1.0 + mv[Ia]) - m;
            nadd(&nut[Ia], du); ut_naive[Ia] += du;
        }
    }

    for (int j = 0; j < K; j++) { o->util[j] = nval(&nut[j]); o->util_naive[j] = ut_naive[j]; }
    o->bench2 = nval(&nb2); o->bench2_naive = b2_naive;
    o->benchb = nval(&nbb); o->benchb_naive = bb_naive;
    o->ncells = ncells; o->perm_count = permc; o->fbu_count = fbuc;
    if (visits_out || r_out) {
        for (int64_t i = 0; i < J; i++) {
            if (visits_out) visits_out[i] = cells[i].V;
            if (r_out) r_out[i] = cells[i].r;
        }
    }
    free(cells);
    o->status = 0;
    return 0;
}
