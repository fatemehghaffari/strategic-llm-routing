# Where package A4's data lives

Per `experiments/README.md`, the AGGREGATED CSVs that every number and every figure in this
package is built from are committed at **`experiments/data/A4/`**, and raw per-replicate Slurm
output stays in the session scratch directory and is not committed.

A figure can be restyled and regenerated from what is committed, with no compute and no access to
scratch, in about 3 seconds:

    $VENV/bin/python audit/round2/A4/scripts/make_figures_a4.py \
        --csv experiments/data/A4 --csv-a3 experiments/data/A3 \
        --out experiments/data/A4/figures_generated

Figure 4 reads `experiments/data/A3/threshold_summary.csv`, which is committed and owned by
package A3; this package reads it and never writes to that directory.

Every scalar quoted in `REPORT.md` is recomputed from the same directory by:

    $VENV/bin/python audit/round2/A4/scripts/make_tables.py \
        --csv experiments/data/A4 --out audit/round2/A4/TABLES.md

## Row for the table in `experiments/README.md`

The main agent owns that file, so I have not edited it. The row to add is:

| `experiments/data/A4/` | RouterBench calibrated simulation | measured capability tables, rank-flip statistics, the two-top measurement, the analytic and simulated contextual-versus-scalar gap, the two-world headline grid, the undercut comparison, the monitor ladder, the horizon sweep, and the figure PDFs as last generated |

## What is in the directory

| file | what it holds |
|---|---|
| `capabilities_finite_{0,5}shot.csv` | the measured capability M_i(z) of each model on each benchmark family, with query counts and standard errors |
| `context_masses_{0,5}shot.csv` | empirical arrival mass of each context |
| `rowcounts.csv`, `validation_vs_paper_table1.csv` | provenance: rows used, and our numbers against RouterBench's published Table 1 |
| `flips_summary_*.csv`, `flips_pairwise_*.csv`, `flips_perpair_*.csv`, `flips_triples_*.csv`, `kendall_*.csv` | the rank-flip measurement, raw and significance-filtered |
| `flips_continuous.csv`, `embedding_diagnostic.csv`, `capsurface_meta.csv`, `model_order.csv` | the continuous-context version and how much of the benchmark family the embedding recovers |
| `two_top_condition.csv`, `two_top_summary.csv`, `two_top_best_subsets.csv` | the two-top condition measured for every subset of every size at every tolerance |
| `analytic_gap_triples.csv`, `analytic_gap_summary.csv` | the contextual-versus-scalar gap in closed form, and its regression on the flip rate |
| `flip_regression.csv`, `flip_regression_summary.csv` | the same gap, simulated, on all 165 triples |
| `horizon_sweep.csv`, `horizon_all_triples.csv`, `horizon_all_summary.csv` | how that gap and the compliant-conviction rate move with the horizon |
| `headline_runs.csv`, `headline_worlds.csv`, `headline_summary.csv`, `strategic_profiles.csv`, `exploitability.csv` | the two-world grid, the profile best response reaches, and the best deviation found |
| `fine_shading.csv`, `fine_shading_best.csv`, `undercut_comparison.csv`, `undercut_summary.csv` | the fine deviation grid and the like-for-like undercut comparison across rules |
| `monitor_ladder.csv`, `monitor_frontier.csv` | the monitor ablation ladder including the two-sample and fixed-buffer rungs, and the frontier that matches false conviction against detection delay |
| `rich_br.csv`, `rich_br_summary.csv` | the fair strategic comparison: best response over one rich option class for every rule |
| `baseline_single_observation*.csv` | the single-observation exclusion rule run under our observation model |
| `utility_curves.csv`, `utility_curves_summary.csv`, `utility_curves_crosscheck.csv` | utility against effort per arm role, and the cross-check against the undercut table |
| `complementarity.csv` | the pairwise complementarity matrix, in the routing literature's form |
| `two_top_*.csv` | the two-top condition measured for every subset of every size at every tolerance |
| `rho_audit.csv` | the arithmetic of the continuum oscillation allowance |
| `baseline_second_best*.csv` | the Second-Best Utility Guarantee Mechanism (WWW 2026), reimplemented from the paper, in the scalar and contextual settings, with the head-to-head summary restricted to cells carrying every mechanism and `*_allcells.csv` holding the unmatched rows |
| `capability_gap_sweep.csv`, `capability_gap_summary.csv`, `capability_gap_from_logs.csv` | the capability-gap sweep that locates where the two-top condition bites |
| `figures_generated/` | the two proposed figures as last generated, PDF and PNG |
