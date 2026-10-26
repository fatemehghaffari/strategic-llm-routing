# TABLES, package A4

Regenerate with, from the repository root:

```
$VENV/bin/python audit/round2/A4/scripts/make_tables.py \
    --csv experiments/data/A4 --out audit/round2/A4/TABLES.md
```

No compute and no scratch access is needed: every number below is read from the aggregated CSVs committed in `experiments/data/A4/`.


## CHECKS: every scalar quoted in REPORT.md, recomputed

| name | value | source CSV | expression |
|---|---|---|---|
| `rows_used_5shot` | 34764 | `rowcounts.csv` | `rowcounts[shot=='5shot'].rows_used` |
| `outcomes_used_5shot` | 382404 | `rowcounts.csv` | `rowcounts[shot=='5shot'].outcomes_used` |
| `rows_used_0shot` | 34778 | `rowcounts.csv` | `rowcounts[shot=='0shot'].rows_used` |
| `outcomes_used_0shot` | 382558 | `rowcounts.csv` | `rowcounts[shot=='0shot'].outcomes_used` |
| `maxabs_vs_table1_ARC` | 0.0426 | `validation_vs_paper_table1.csv` | `groupby(context).ours_minus_published.abs().max()['ARC']` |
| `maxabs_vs_table1_GSM8K` | 0.0060 | `validation_vs_paper_table1.csv` | `groupby(context).ours_minus_published.abs().max()['GSM8K']` |
| `maxabs_vs_table1_HellaSwag` | 0.1071 | `validation_vs_paper_table1.csv` | `groupby(context).ours_minus_published.abs().max()['HellaSwag']` |
| `maxabs_vs_table1_MBPP` | 0.0702 | `validation_vs_paper_table1.csv` | `groupby(context).ours_minus_published.abs().max()['MBPP']` |
| `maxabs_vs_table1_MMLU` | 0.0672 | `validation_vs_paper_table1.csv` | `groupby(context).ours_minus_published.abs().max()['MMLU']` |
| `maxabs_vs_table1_MT-Bench` | 0.2942 | `validation_vs_paper_table1.csv` | `groupby(context).ours_minus_published.abs().max()['MT-Bench']` |
| `maxabs_vs_table1_Winogrande` | 0.0322 | `validation_vs_paper_table1.csv` | `groupby(context).ours_minus_published.abs().max()['Winogrande']` |
| `maxabs_vs_table1_excl_MTBench` | 0.1071 | `validation_vs_paper_table1.csv` | `same, MT-Bench dropped` |
| `mass_MMLU` | 0.40392 | `context_masses_5shot.csv` | `mass[context=='MMLU']` |
| `mass_HellaSwag` | 0.28886 | `context_masses_5shot.csv` | `mass[context=='HellaSwag']` |
| `mass_GSM8K` | 0.21430 | `context_masses_5shot.csv` | `mass[context=='GSM8K']` |
| `mass_Winogrande` | 0.03645 | `context_masses_5shot.csv` | `mass[context=='Winogrande']` |
| `mass_ARC` | 0.04188 | `context_masses_5shot.csv` | `mass[context=='ARC']` |
| `mass_MBPP` | 0.01228 | `context_masses_5shot.csv` | `mass[context=='MBPP']` |
| `mass_MT-Bench` | 0.00230 | `context_masses_5shot.csv` | `mass[context=='MT-Bench']` |
| `raw_flip_rate_5shot` | 0.3013 | `flips_summary_5shot.csv` | `raw_flip_rate` |
| `sig_flip_rate_5shot` | 0.2470 | `flips_summary_5shot.csv` | `sig_flip_rate` |
| `bonf_flip_rate_5shot` | 0.2372 | `flips_summary_5shot.csv` | `bonf_flip_rate` |
| `frac_ctx_pairs_different_best_5shot` | 0.2857 | `flips_summary_5shot.csv` | `frac_ctx_pairs_different_best` |
| `mean_kendall_tau_between_contexts_5shot` | 0.3974 | `flips_summary_5shot.csv` | `mean_kendall_tau_between_contexts` |
| `min_kendall_tau_between_contexts_5shot` | -0.0545 | `flips_summary_5shot.csv` | `min_kendall_tau_between_contexts` |
| `raw_flips_5shot` | 348 | `flips_summary_5shot.csv` | `raw_flips` |
| `raw_comparisons_5shot` | 1155 | `flips_summary_5shot.csv` | `raw_comparisons` |
| `sig_flips_5shot` | 208 | `flips_summary_5shot.csv` | `sig_flips` |
| `sig_comparisons_5shot` | 842 | `flips_summary_5shot.csv` | `sig_comparisons` |
| `bonf_flips_5shot` | 144 | `flips_summary_5shot.csv` | `bonf_flips` |
| `bonf_comparisons_5shot` | 607 | `flips_summary_5shot.csv` | `bonf_comparisons` |
| `n_distinct_best_models_5shot` | 2 | `flips_summary_5shot.csv` | `n_distinct_best_models` |
| `raw_flip_rate_0shot` | 0.1749 | `flips_summary_0shot.csv` | `raw_flip_rate` |
| `sig_flip_rate_0shot` | 0.1040 | `flips_summary_0shot.csv` | `sig_flip_rate` |
| `bonf_flip_rate_0shot` | 0.0920 | `flips_summary_0shot.csv` | `bonf_flip_rate` |
| `frac_ctx_pairs_different_best_0shot` | 0.2857 | `flips_summary_0shot.csv` | `frac_ctx_pairs_different_best` |
| `mean_kendall_tau_between_contexts_0shot` | 0.6486 | `flips_summary_0shot.csv` | `mean_kendall_tau_between_contexts` |
| `min_kendall_tau_between_contexts_0shot` | 0.4771 | `flips_summary_0shot.csv` | `min_kendall_tau_between_contexts` |
| `raw_flips_0shot` | 201 | `flips_summary_0shot.csv` | `raw_flips` |
| `raw_comparisons_0shot` | 1149 | `flips_summary_0shot.csv` | `raw_comparisons` |
| `sig_flips_0shot` | 90 | `flips_summary_0shot.csv` | `sig_flips` |
| `sig_comparisons_0shot` | 865 | `flips_summary_0shot.csv` | `sig_comparisons` |
| `bonf_flips_0shot` | 56 | `flips_summary_0shot.csv` | `bonf_flips` |
| `bonf_comparisons_0shot` | 609 | `flips_summary_0shot.csv` | `bonf_comparisons` |
| `n_distinct_best_models_0shot` | 2 | `flips_summary_0shot.csv` | `n_distinct_best_models` |
| `n_model_pairs_never_flipping_5shot` | 19 | `flips_perpair_5shot.csv` | `(flip_rate==0).sum()` |
| `max_pair_flip_rate_5shot` | 0.5714 | `flips_perpair_5shot.csv` | `flip_rate.max()` |
| `cont_d2k200_raw_flip_rate` | 0.2070 | `flips_continuous.csv` | `row d==2 & k==200, column raw_flip_rate` |
| `cont_d2k200_frac_queries_best_differs_from_global` | 0.2037 | `flips_continuous.csv` | `row d==2 & k==200, column frac_queries_best_differs_from_global` |
| `cont_d2k200_mean_pointwise_max` | 0.8200 | `flips_continuous.csv` | `row d==2 & k==200, column mean_pointwise_max` |
| `cont_d2k200_mean_pointwise_second` | 0.7628 | `flips_continuous.csv` | `row d==2 & k==200, column mean_pointwise_second` |
| `cont_d2k200_global_max_mean` | 0.8167 | `flips_continuous.csv` | `row d==2 & k==200, column global_max_mean` |
| `cont_d2k200_global_second_mean` | 0.7341 | `flips_continuous.csv` | `row d==2 & k==200, column global_second_mean` |
| `cont_d2k200_n_cells` | 129 | `flips_continuous.csv` | `row d==2 & k==200, n_cells` |
| `embed_d2_cell_family_purity` | 0.8909 | `embedding_diagnostic.csv` | `row d==2, cell_family_purity` |
| `embed_d2_nmi` | 0.7754 | `embedding_diagnostic.csv` | `row d==2, normalised_mutual_info_cell_family` |
| `analytic_Q3_spearman_rho` | 0.5647 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column spearman_rho` |
| `analytic_Q3_ols_slope` | 0.0517 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column ols_slope` |
| `analytic_Q3_gap_mean` | 0.0227 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column gap_mean` |
| `analytic_Q3_gap_max` | 0.0712 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column gap_max` |
| `analytic_Q3_gap_at_flip0_mean` | 0.0075 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column gap_at_flip0_mean` |
| `analytic_Q3_frac_triples_gap_above_0.01` | 0.6182 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column frac_triples_gap_above_0.01` |
| `analytic_Q3_spearman_p` | 2.8e-15 | `analytic_gap_summary.csv` | `spearman_p` |
| `analytic_Q3_mean_scalar_mass_price_above_capability` | 0.1822 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column mean_scalar_mass_price_above_capability` |
| `analytic_Q3_frac_triples_scalar_price_infeasible_somewhere` | 0.6727 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column frac_triples_scalar_price_infeasible_somewhere` |
| `analytic_Q3_spearman_flip_vs_infeasible_mass` | 0.2313 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=False, column spearman_flip_vs_infeasible_mass` |
| `analytic_Q3u_spearman_rho` | 0.5748 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column spearman_rho` |
| `analytic_Q3u_ols_slope` | 0.0556 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column ols_slope` |
| `analytic_Q3u_gap_mean` | 0.0251 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column gap_mean` |
| `analytic_Q3u_gap_max` | 0.0774 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column gap_max` |
| `analytic_Q3u_gap_at_flip0_mean` | 0.0090 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column gap_at_flip0_mean` |
| `analytic_Q3u_frac_triples_gap_above_0.01` | 0.6485 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column frac_triples_gap_above_0.01` |
| `analytic_Q3u_spearman_p` | 6.88e-16 | `analytic_gap_summary.csv` | `spearman_p` |
| `analytic_Q3u_mean_scalar_mass_price_above_capability` | 0.2465 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column mean_scalar_mass_price_above_capability` |
| `analytic_Q3u_frac_triples_scalar_price_infeasible_somewhere` | 0.7394 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column frac_triples_scalar_price_infeasible_somewhere` |
| `analytic_Q3u_spearman_flip_vs_infeasible_mass` | 0.1622 | `analytic_gap_summary.csv` | `row Q3/uniform_mass=True, column spearman_flip_vs_infeasible_mass` |
| `analytic_Q7_spearman_rho` | 0.4367 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column spearman_rho` |
| `analytic_Q7_ols_slope` | 0.0554 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column ols_slope` |
| `analytic_Q7_gap_mean` | 0.0236 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column gap_mean` |
| `analytic_Q7_gap_max` | 0.0718 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column gap_max` |
| `analytic_Q7_gap_at_flip0_mean` | 0.0084 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column gap_at_flip0_mean` |
| `analytic_Q7_frac_triples_gap_above_0.01` | 0.6667 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column frac_triples_gap_above_0.01` |
| `analytic_Q7_spearman_p` | 4.52e-09 | `analytic_gap_summary.csv` | `spearman_p` |
| `analytic_Q7_mean_scalar_mass_price_above_capability` | 0.1959 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column mean_scalar_mass_price_above_capability` |
| `analytic_Q7_frac_triples_scalar_price_infeasible_somewhere` | 0.7758 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column frac_triples_scalar_price_infeasible_somewhere` |
| `analytic_Q7_spearman_flip_vs_infeasible_mass` | 0.4582 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=False, column spearman_flip_vs_infeasible_mass` |
| `analytic_Q7u_spearman_rho` | 0.4782 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column spearman_rho` |
| `analytic_Q7u_ols_slope` | 0.0630 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column ols_slope` |
| `analytic_Q7u_gap_mean` | 0.0263 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column gap_mean` |
| `analytic_Q7u_gap_max` | 0.0827 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column gap_max` |
| `analytic_Q7u_gap_at_flip0_mean` | 0.0045 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column gap_at_flip0_mean` |
| `analytic_Q7u_frac_triples_gap_above_0.01` | 0.7212 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column frac_triples_gap_above_0.01` |
| `analytic_Q7u_spearman_p` | 8.23e-11 | `analytic_gap_summary.csv` | `spearman_p` |
| `analytic_Q7u_mean_scalar_mass_price_above_capability` | 0.2935 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column mean_scalar_mass_price_above_capability` |
| `analytic_Q7u_frac_triples_scalar_price_infeasible_somewhere` | 0.8485 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column frac_triples_scalar_price_infeasible_somewhere` |
| `analytic_Q7u_spearman_flip_vs_infeasible_mass` | 0.4365 | `analytic_gap_summary.csv` | `row Q7/uniform_mass=True, column spearman_flip_vs_infeasible_mass` |
| `simgap_Q3_spearman_rho_flip_vs_simgap` | 0.1339 | `flip_regression_summary.csv` | `row Q3, column spearman_rho_flip_vs_simgap` |
| `simgap_Q3_ols_slope` | 0.0054 | `flip_regression_summary.csv` | `row Q3, column ols_slope` |
| `simgap_Q3_mean_sim_gap` | 0.0084 | `flip_regression_summary.csv` | `row Q3, column mean_sim_gap` |
| `simgap_Q3_mean_analytic_gap` | 0.0227 | `flip_regression_summary.csv` | `row Q3, column mean_analytic_gap` |
| `simgap_Q3_frac_sim_gap_positive` | 0.7152 | `flip_regression_summary.csv` | `row Q3, column frac_sim_gap_positive` |
| `simgap_Q3_spearman_analytic_vs_sim` | 0.4784 | `flip_regression_summary.csv` | `row Q3, column spearman_analytic_vs_sim` |
| `simgap_Q3_spearman_p` | 0.0864 | `flip_regression_summary.csv` | `spearman_p` |
| `simgap_Q7_spearman_rho_flip_vs_simgap` | -0.0473 | `flip_regression_summary.csv` | `row Q7, column spearman_rho_flip_vs_simgap` |
| `simgap_Q7_ols_slope` | -0.0262 | `flip_regression_summary.csv` | `row Q7, column ols_slope` |
| `simgap_Q7_mean_sim_gap` | 0.0110 | `flip_regression_summary.csv` | `row Q7, column mean_sim_gap` |
| `simgap_Q7_mean_analytic_gap` | 0.0236 | `flip_regression_summary.csv` | `row Q7, column mean_analytic_gap` |
| `simgap_Q7_frac_sim_gap_positive` | 0.7091 | `flip_regression_summary.csv` | `row Q7, column frac_sim_gap_positive` |
| `simgap_Q7_spearman_analytic_vs_sim` | 0.3742 | `flip_regression_summary.csv` | `row Q7, column spearman_analytic_vs_sim` |
| `simgap_Q7_spearman_p` | 0.546 | `flip_regression_summary.csv` | `spearman_p` |
| `simconv_scalar_Q3` | 0.2473 | `flip_regression.csv` | `[context_set=='Q3'].conv_mesp_scalar.mean()` |
| `simconv_contextual_Q3` | 0.0000 | `flip_regression.csv` | `[context_set=='Q3'].conv_plmesp.mean()` |
| `simconv_scalar_Q7` | 0.2521 | `flip_regression.csv` | `[context_set=='Q7'].conv_mesp_scalar.mean()` |
| `simconv_contextual_Q7` | 0.0000 | `flip_regression.csv` | `[context_set=='Q7'].conv_plmesp.mean()` |
| `twotop_Q3_K2_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=2, mean_mass_within_0.0` |
| `twotop_Q3_K2_mass_0.01` | 0.0615 | `two_top_summary.csv` | `row Q3/K=2, mean_mass_within_0.01` |
| `twotop_Q3_K2_mean_top_gap` | 0.1473 | `two_top_summary.csv` | `row Q3/K=2, mean_top_gap` |
| `twotop_Q3_K3_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=3, mean_mass_within_0.0` |
| `twotop_Q3_K3_mass_0.01` | 0.0556 | `two_top_summary.csv` | `row Q3/K=3, mean_mass_within_0.01` |
| `twotop_Q3_K3_mean_top_gap` | 0.1080 | `two_top_summary.csv` | `row Q3/K=3, mean_top_gap` |
| `twotop_Q3_K4_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=4, mean_mass_within_0.0` |
| `twotop_Q3_K4_mass_0.01` | 0.0547 | `two_top_summary.csv` | `row Q3/K=4, mean_mass_within_0.01` |
| `twotop_Q3_K4_mean_top_gap` | 0.0899 | `two_top_summary.csv` | `row Q3/K=4, mean_top_gap` |
| `twotop_Q3_K5_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=5, mean_mass_within_0.0` |
| `twotop_Q3_K5_mass_0.01` | 0.0731 | `two_top_summary.csv` | `row Q3/K=5, mean_mass_within_0.01` |
| `twotop_Q3_K5_mean_top_gap` | 0.0769 | `two_top_summary.csv` | `row Q3/K=5, mean_top_gap` |
| `twotop_Q3_K6_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=6, mean_mass_within_0.0` |
| `twotop_Q3_K6_mass_0.01` | 0.1002 | `two_top_summary.csv` | `row Q3/K=6, mean_mass_within_0.01` |
| `twotop_Q3_K6_mean_top_gap` | 0.0680 | `two_top_summary.csv` | `row Q3/K=6, mean_top_gap` |
| `twotop_Q3_K7_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=7, mean_mass_within_0.0` |
| `twotop_Q3_K7_mass_0.01` | 0.1303 | `two_top_summary.csv` | `row Q3/K=7, mean_mass_within_0.01` |
| `twotop_Q3_K7_mean_top_gap` | 0.0624 | `two_top_summary.csv` | `row Q3/K=7, mean_top_gap` |
| `twotop_Q3_K8_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=8, mean_mass_within_0.0` |
| `twotop_Q3_K8_mass_0.01` | 0.1604 | `two_top_summary.csv` | `row Q3/K=8, mean_mass_within_0.01` |
| `twotop_Q3_K8_mean_top_gap` | 0.0590 | `two_top_summary.csv` | `row Q3/K=8, mean_top_gap` |
| `twotop_Q3_K9_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=9, mean_mass_within_0.0` |
| `twotop_Q3_K9_mass_0.01` | 0.1890 | `two_top_summary.csv` | `row Q3/K=9, mean_mass_within_0.01` |
| `twotop_Q3_K9_mean_top_gap` | 0.0571 | `two_top_summary.csv` | `row Q3/K=9, mean_top_gap` |
| `twotop_Q3_K10_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=10, mean_mass_within_0.0` |
| `twotop_Q3_K10_mass_0.01` | 0.2148 | `two_top_summary.csv` | `row Q3/K=10, mean_mass_within_0.01` |
| `twotop_Q3_K10_mean_top_gap` | 0.0557 | `two_top_summary.csv` | `row Q3/K=10, mean_top_gap` |
| `twotop_Q3_K11_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q3/K=11, mean_mass_within_0.0` |
| `twotop_Q3_K11_mass_0.01` | 0.2363 | `two_top_summary.csv` | `row Q3/K=11, mean_mass_within_0.01` |
| `twotop_Q3_K11_mean_top_gap` | 0.0545 | `two_top_summary.csv` | `row Q3/K=11, mean_top_gap` |
| `twotop_Q7_K2_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=2, mean_mass_within_0.0` |
| `twotop_Q7_K2_mass_0.01` | 0.0599 | `two_top_summary.csv` | `row Q7/K=2, mean_mass_within_0.01` |
| `twotop_Q7_K2_mean_top_gap` | 0.1466 | `two_top_summary.csv` | `row Q7/K=2, mean_top_gap` |
| `twotop_Q7_K3_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=3, mean_mass_within_0.0` |
| `twotop_Q7_K3_mass_0.01` | 0.0561 | `two_top_summary.csv` | `row Q7/K=3, mean_mass_within_0.01` |
| `twotop_Q7_K3_mean_top_gap` | 0.1082 | `two_top_summary.csv` | `row Q7/K=3, mean_top_gap` |
| `twotop_Q7_K4_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=4, mean_mass_within_0.0` |
| `twotop_Q7_K4_mass_0.01` | 0.0560 | `two_top_summary.csv` | `row Q7/K=4, mean_mass_within_0.01` |
| `twotop_Q7_K4_mean_top_gap` | 0.0902 | `two_top_summary.csv` | `row Q7/K=4, mean_top_gap` |
| `twotop_Q7_K5_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=5, mean_mass_within_0.0` |
| `twotop_Q7_K5_mass_0.01` | 0.0733 | `two_top_summary.csv` | `row Q7/K=5, mean_mass_within_0.01` |
| `twotop_Q7_K5_mean_top_gap` | 0.0775 | `two_top_summary.csv` | `row Q7/K=5, mean_top_gap` |
| `twotop_Q7_K6_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=6, mean_mass_within_0.0` |
| `twotop_Q7_K6_mass_0.01` | 0.0983 | `two_top_summary.csv` | `row Q7/K=6, mean_mass_within_0.01` |
| `twotop_Q7_K6_mean_top_gap` | 0.0690 | `two_top_summary.csv` | `row Q7/K=6, mean_top_gap` |
| `twotop_Q7_K7_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=7, mean_mass_within_0.0` |
| `twotop_Q7_K7_mass_0.01` | 0.1257 | `two_top_summary.csv` | `row Q7/K=7, mean_mass_within_0.01` |
| `twotop_Q7_K7_mean_top_gap` | 0.0636 | `two_top_summary.csv` | `row Q7/K=7, mean_top_gap` |
| `twotop_Q7_K8_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=8, mean_mass_within_0.0` |
| `twotop_Q7_K8_mass_0.01` | 0.1527 | `two_top_summary.csv` | `row Q7/K=8, mean_mass_within_0.01` |
| `twotop_Q7_K8_mean_top_gap` | 0.0602 | `two_top_summary.csv` | `row Q7/K=8, mean_top_gap` |
| `twotop_Q7_K9_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=9, mean_mass_within_0.0` |
| `twotop_Q7_K9_mass_0.01` | 0.1775 | `two_top_summary.csv` | `row Q7/K=9, mean_mass_within_0.01` |
| `twotop_Q7_K9_mean_top_gap` | 0.0583 | `two_top_summary.csv` | `row Q7/K=9, mean_top_gap` |
| `twotop_Q7_K10_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=10, mean_mass_within_0.0` |
| `twotop_Q7_K10_mass_0.01` | 0.1986 | `two_top_summary.csv` | `row Q7/K=10, mean_mass_within_0.01` |
| `twotop_Q7_K10_mean_top_gap` | 0.0570 | `two_top_summary.csv` | `row Q7/K=10, mean_top_gap` |
| `twotop_Q7_K11_mass_exact` | 0.0000 | `two_top_summary.csv` | `row Q7/K=11, mean_mass_within_0.0` |
| `twotop_Q7_K11_mass_0.01` | 0.2143 | `two_top_summary.csv` | `row Q7/K=11, mean_mass_within_0.01` |
| `twotop_Q7_K11_mean_top_gap` | 0.0558 | `two_top_summary.csv` | `row Q7/K=11, mean_top_gap` |
| `rho_paper_n300000_d1` | 0.5671 | `rho_audit.csv` | `row n==300000 & d==1, rho_paper` |
| `totalshade_n300000_d1` | 0.9911 | `rho_audit.csv` | `row n==300000 & d==1, total_price_shading_3s_plus_rho` |
| `rho_measured_n300000_d1` | 0.2154 | `rho_audit.csv` | `row n==300000 & d==1, rho_measured_p95_within_cell` |
| `rho_paper_n300000_d2` | 1.4807 | `rho_audit.csv` | `row n==300000 & d==2, rho_paper` |
| `totalshade_n300000_d2` | 2.2767 | `rho_audit.csv` | `row n==300000 & d==2, total_price_shading_3s_plus_rho` |
| `rho_measured_n300000_d2` | 0.2303 | `rho_audit.csv` | `row n==300000 & d==2, rho_measured_p95_within_cell` |
| `rho_paper_n10000000_d1` | 0.3003 | `rho_audit.csv` | `row n==10000000 & d==1, rho_paper` |
| `totalshade_n10000000_d1` | 0.4916 | `rho_audit.csv` | `row n==10000000 & d==1, total_price_shading_3s_plus_rho` |
| `rho_measured_n10000000_d1` | 0.1802 | `rho_audit.csv` | `row n==10000000 & d==1, rho_measured_p95_within_cell` |
| `rho_paper_n10000000_d2` | 0.9311 | `rho_audit.csv` | `row n==10000000 & d==2, rho_paper` |
| `totalshade_n10000000_d2` | 1.3592 | `rho_audit.csv` | `row n==10000000 & d==2, total_price_shading_3s_plus_rho` |
| `rho_measured_n10000000_d2` | 0.1350 | `rho_audit.csv` | `row n==10000000 & d==2, rho_measured_p95_within_cell` |
| `rho_paper_n1000000000_d1` | 0.1220 | `rho_audit.csv` | `row n==1000000000 & d==1, rho_paper` |
| `totalshade_n1000000000_d1` | 0.1878 | `rho_audit.csv` | `row n==1000000000 & d==1, total_price_shading_3s_plus_rho` |
| `rho_measured_n1000000000_d1` | 0.1200 | `rho_audit.csv` | `row n==1000000000 & d==1, rho_measured_p95_within_cell` |
| `rho_paper_n1000000000_d2` | 0.4800 | `rho_audit.csv` | `row n==1000000000 & d==2, rho_paper` |
| `totalshade_n1000000000_d2` | 0.6652 | `rho_audit.csv` | `row n==1000000000 & d==2, total_price_shading_3s_plus_rho` |
| `rho_measured_n1000000000_d2` | 0.0650 | `rho_audit.csv` | `row n==1000000000 & d==2, rho_measured_p95_within_cell` |
| `rho_paper_n1000000000000_d1` | 0.0286 | `rho_audit.csv` | `row n==1000000000000 & d==1, rho_paper` |
| `totalshade_n1000000000000_d1` | 0.0415 | `rho_audit.csv` | `row n==1000000000000 & d==1, total_price_shading_3s_plus_rho` |
| `rho_measured_n1000000000000_d1` | 0.0450 | `rho_audit.csv` | `row n==1000000000000 & d==1, rho_measured_p95_within_cell` |
| `rho_paper_n1000000000000_d2` | 0.1607 | `rho_audit.csv` | `row n==1000000000000 & d==2, rho_paper` |
| `totalshade_n1000000000000_d2` | 0.2118 | `rho_audit.csv` | `row n==1000000000000 & d==2, total_price_shading_3s_plus_rho` |
| `rho_measured_n1000000000000_d2` | 0.0150 | `rho_audit.csv` | `row n==1000000000000 & d==2, rho_measured_p95_within_cell` |
| `cg_elicitation_fraction_n300k_d2` | 0.4786 | `rho_audit.csv` | `row n==300000 & d==2, elicitation_fraction` |
| `s_n_cg_n300k_d2` | 0.2653 | `rho_audit.csv` | `row n==300000 & d==2, s_n` |
| `horizon_Q3_n300000_mean_simgap` | 0.0109 | `horizon_sweep.csv` | `[context_set=='Q3' & n==300000].sim_gap.mean()` |
| `horizon_Q3_n1000000_mean_simgap` | -0.0243 | `horizon_sweep.csv` | `[context_set=='Q3' & n==1000000].sim_gap.mean()` |
| `horizon_Q3_n3000000_mean_simgap` | -0.0287 | `horizon_sweep.csv` | `[context_set=='Q3' & n==3000000].sim_gap.mean()` |
| `horizon_Q3_n10000000_mean_simgap` | -0.0272 | `horizon_sweep.csv` | `[context_set=='Q3' & n==10000000].sim_gap.mean()` |
| `horizon_Q3_n30000000_mean_simgap` | -0.0240 | `horizon_sweep.csv` | `[context_set=='Q3' & n==30000000].sim_gap.mean()` |
| `horizon_Q7_n300000_mean_simgap` | 0.0208 | `horizon_sweep.csv` | `[context_set=='Q7' & n==300000].sim_gap.mean()` |
| `horizon_Q7_n1000000_mean_simgap` | 0.0209 | `horizon_sweep.csv` | `[context_set=='Q7' & n==1000000].sim_gap.mean()` |
| `horizon_Q7_n3000000_mean_simgap` | 0.0167 | `horizon_sweep.csv` | `[context_set=='Q7' & n==3000000].sim_gap.mean()` |
| `horizon_Q7_n10000000_mean_simgap` | -0.0177 | `horizon_sweep.csv` | `[context_set=='Q7' & n==10000000].sim_gap.mean()` |
| `horizon_Q7_n30000000_mean_simgap` | -0.0311 | `horizon_sweep.csv` | `[context_set=='Q7' & n==30000000].sim_gap.mean()` |
| `horizall_spearman_rho_flip_vs_simgap` | 0.0549 | `horizon_all_summary.csv` | `spearman_rho_flip_vs_simgap` |
| `horizall_ols_slope` | -0.0001 | `horizon_all_summary.csv` | `ols_slope` |
| `horizall_mean_sim_gap` | -0.0239 | `horizon_all_summary.csv` | `mean_sim_gap` |
| `horizall_frac_sim_gap_positive` | 0.4727 | `horizon_all_summary.csv` | `frac_sim_gap_positive` |
| `horizall_mean_compconv_scalar` | 0.5370 | `horizon_all_summary.csv` | `mean_compconv_scalar` |
| `horizall_mean_compconv_contextual` | 0.0000 | `horizon_all_summary.csv` | `mean_compconv_contextual` |
| `horizall_frac_runs_scalar_price_above_cap` | 0.6121 | `horizon_all_summary.csv` | `frac_runs_scalar_price_above_cap` |
| `horizall_spearman_flip_vs_compconv_scalar` | 0.2781 | `horizon_all_summary.csv` | `spearman_flip_vs_compconv_scalar` |
| `horizall_spearman_flip_vs_compconv_scalar_p` | 0.0003 | `horizon_all_summary.csv` | `spearman_flip_vs_compconv_scalar_p` |
| `horizall_spearman_p` | 0.484 | `horizon_all_summary.csv` | `spearman_p` |
| `horizall_n` | 3000000 | `horizon_all_summary.csv` | `n` |
| `rev_nonstrat_Q3_a0.00_mesp_scalar` | 0.6952 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.00_mesp_scalar` | 0.2096 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q3_a0.00_mesp_scalar` | 0.4856 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.00_plmesp` | 0.6937 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.00_plmesp` | 0.2411 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q3_a0.00_plmesp` | 0.4526 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.00_router_eps` | 0.7185 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.00_router_eps` | 0.5984 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q3_a0.00_router_eps` | 0.1201 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.00_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.00_router_greedy` | 0.5932 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q3_a0.00_router_greedy` | 0.0951 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.00_router_ucb` | 0.7210 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.00_router_ucb` | 0.6806 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.00' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q3_a0.00_router_ucb` | 0.0405 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.00_mesp_scalar` | 0.6776 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.00_mesp_scalar` | 0.0245 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7_a0.00_mesp_scalar` | 0.6531 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.00_plmesp` | 0.6577 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.00_plmesp` | 0.2201 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7_a0.00_plmesp` | 0.4376 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.00_router_eps` | 0.7039 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.00_router_eps` | 0.6826 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7_a0.00_router_eps` | 0.0214 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.00_router_greedy` | 0.6661 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.00_router_greedy` | 0.6252 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7_a0.00_router_greedy` | 0.0409 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.00_router_ucb` | 0.7063 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.00_router_ucb` | 0.7063 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.00' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7_a0.00_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.00_mesp_scalar` | 0.6235 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.00_mesp_scalar` | 0.2733 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7u_a0.00_mesp_scalar` | 0.3502 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.00_plmesp` | 0.5956 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.00_plmesp` | 0.1171 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7u_a0.00_plmesp` | 0.4785 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.00_router_eps` | 0.6609 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.00_router_eps` | 0.6427 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7u_a0.00_router_eps` | 0.0182 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.00_router_greedy` | 0.6227 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.00_router_greedy` | 0.6227 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7u_a0.00_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.00_router_ucb` | 0.6616 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.00_router_ucb` | 0.6616 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.00' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7u_a0.00_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.00_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.00_mesp_scalar` | 0.0245 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.00_mesp_scalar` | 0.6526 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.00_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.00_plmesp` | 0.1490 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.00_plmesp` | 0.5103 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.00_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.00_router_eps` | 0.6929 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.00_router_eps` | 0.0027 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.00_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.00_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.00_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.00_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.00_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.00' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.00_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.00_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.00_mesp_scalar` | 0.0245 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.00_mesp_scalar` | 0.6526 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.00_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.00_plmesp` | 0.1377 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.00_plmesp` | 0.5216 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.00_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.00_router_eps` | 0.6929 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.00_router_eps` | 0.0027 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.00_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.00_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.00_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.00_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.00_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.00' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.00_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.25_mesp_scalar` | 0.6952 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.25_mesp_scalar` | 0.2819 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q3_a0.25_mesp_scalar` | 0.4134 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.25_plmesp` | 0.6937 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.25_plmesp` | 0.3246 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q3_a0.25_plmesp` | 0.3691 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.25_router_eps` | 0.7185 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.25_router_eps` | 0.6647 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q3_a0.25_router_eps` | 0.0538 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.25_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.25_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q3_a0.25_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.25_router_ucb` | 0.7210 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.25_router_ucb` | 0.7210 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.25' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q3_a0.25_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.25_mesp_scalar` | 0.6776 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.25_mesp_scalar` | 0.1228 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7_a0.25_mesp_scalar` | 0.5548 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.25_plmesp` | 0.6577 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.25_plmesp` | 0.3269 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7_a0.25_plmesp` | 0.3309 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.25_router_eps` | 0.7039 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.25_router_eps` | 0.4831 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7_a0.25_router_eps` | 0.2208 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.25_router_greedy` | 0.6661 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.25_router_greedy` | 0.6661 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7_a0.25_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.25_router_ucb` | 0.7063 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.25_router_ucb` | 0.7063 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.25' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7_a0.25_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.25_mesp_scalar` | 0.6821 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.25_mesp_scalar` | 0.2671 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7u_a0.25_mesp_scalar` | 0.4150 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.25_plmesp` | 0.6359 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.25_plmesp` | 0.4308 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7u_a0.25_plmesp` | 0.2051 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.25_router_eps` | 0.7093 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.25_router_eps` | 0.6826 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7u_a0.25_router_eps` | 0.0267 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.25_router_greedy` | 0.6724 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.25_router_greedy` | 0.6724 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7u_a0.25_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.25_router_ucb` | 0.7105 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.25_router_ucb` | 0.7105 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.25' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7u_a0.25_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.25_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.25_mesp_scalar` | 0.1217 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.25_mesp_scalar` | 0.5554 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.25_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.25_plmesp` | 0.1787 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.25_plmesp` | 0.4806 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.25_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.25_router_eps` | 0.6935 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.25_router_eps` | 0.0020 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.25_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.25_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.25_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.25_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.25_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.25' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.25_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.25_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.25_mesp_scalar` | 0.1217 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.25_mesp_scalar` | 0.5554 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.25_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.25_plmesp` | 0.1738 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.25_plmesp` | 0.4854 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.25_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.25_router_eps` | 0.6935 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.25_router_eps` | 0.0020 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.25_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.25_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.25_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.25_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.25_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.25' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.25_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.50_mesp_scalar` | 0.6952 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.50_mesp_scalar` | 0.3827 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q3_a0.50_mesp_scalar` | 0.3125 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.50_plmesp` | 0.6937 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.50_plmesp` | 0.4056 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q3_a0.50_plmesp` | 0.2881 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.50_router_eps` | 0.7185 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.50_router_eps` | 0.6837 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q3_a0.50_router_eps` | 0.0348 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.50_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.50_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q3_a0.50_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.50_router_ucb` | 0.7210 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.50_router_ucb` | 0.7144 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.50' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q3_a0.50_router_ucb` | 0.0066 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.50_mesp_scalar` | 0.7433 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.50_mesp_scalar` | 0.2818 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7_a0.50_mesp_scalar` | 0.4615 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.50_plmesp` | 0.7021 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.50_plmesp` | 0.3555 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7_a0.50_plmesp` | 0.3465 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.50_router_eps` | 0.7557 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.50_router_eps` | 0.7195 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7_a0.50_router_eps` | 0.0363 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.50_router_greedy` | 0.7111 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.50_router_greedy` | 0.7111 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7_a0.50_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.50_router_ucb` | 0.7593 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.50_router_ucb` | 0.7593 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.50' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7_a0.50_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.50_mesp_scalar` | 0.7431 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.50_mesp_scalar` | 0.2851 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7u_a0.50_mesp_scalar` | 0.4580 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.50_plmesp` | 0.6706 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.50_plmesp` | 0.4328 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7u_a0.50_plmesp` | 0.2378 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.50_router_eps` | 0.7527 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.50_router_eps` | 0.7480 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7u_a0.50_router_eps` | 0.0047 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.50_router_greedy` | 0.7162 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.50_router_greedy` | 0.7162 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7u_a0.50_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.50_router_ucb` | 0.7544 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.50_router_ucb` | 0.7544 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.50' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7u_a0.50_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.50_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.50_mesp_scalar` | 0.2634 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.50_mesp_scalar` | 0.4138 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.50_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.50_plmesp` | 0.2314 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.50_plmesp` | 0.4279 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.50_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.50_router_eps` | 0.6943 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.50_router_eps` | 0.0013 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.50_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.50_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.50_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.50_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.50_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.50' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.50_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.50_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.50_mesp_scalar` | 0.2634 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.50_mesp_scalar` | 0.4138 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.50_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.50_plmesp` | 0.2263 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.50_plmesp` | 0.4330 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.50_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.50_router_eps` | 0.6943 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.50_router_eps` | 0.0013 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.50_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.50_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.50_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.50_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.50_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.50' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.50_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.75_mesp_scalar` | 0.6952 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.75_mesp_scalar` | 0.4281 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q3_a0.75_mesp_scalar` | 0.2672 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.75_plmesp` | 0.6937 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.75_plmesp` | 0.5265 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q3_a0.75_plmesp` | 0.1671 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.75_router_eps` | 0.7185 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.75_router_eps` | 0.7118 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q3_a0.75_router_eps` | 0.0067 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.75_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.75_router_greedy` | 0.6750 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q3_a0.75_router_greedy` | 0.0132 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_a0.75_router_ucb` | 0.7210 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q3_a0.75_router_ucb` | 0.7178 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='a0.75' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q3_a0.75_router_ucb` | 0.0033 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.75_mesp_scalar` | 0.6776 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.75_mesp_scalar` | 0.4044 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7_a0.75_mesp_scalar` | 0.2731 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.75_plmesp` | 0.6577 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.75_plmesp` | 0.4733 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7_a0.75_plmesp` | 0.1844 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.75_router_eps` | 0.7039 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.75_router_eps` | 0.6488 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7_a0.75_router_eps` | 0.0551 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.75_router_greedy` | 0.6661 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.75_router_greedy` | 0.6551 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7_a0.75_router_greedy` | 0.0110 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_a0.75_router_ucb` | 0.7063 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7_a0.75_router_ucb` | 0.6944 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='a0.75' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7_a0.75_router_ucb` | 0.0119 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.75_mesp_scalar` | 0.6821 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.75_mesp_scalar` | 0.4736 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7u_a0.75_mesp_scalar` | 0.2084 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.75_plmesp` | 0.6359 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.75_plmesp` | 0.5153 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7u_a0.75_plmesp` | 0.1205 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.75_router_eps` | 0.7093 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.75_router_eps` | 0.7075 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7u_a0.75_router_eps` | 0.0018 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.75_router_greedy` | 0.6724 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.75_router_greedy` | 0.6707 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7u_a0.75_router_greedy` | 0.0016 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_a0.75_router_ucb` | 0.7105 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7u_a0.75_router_ucb` | 0.7105 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='a0.75' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7u_a0.75_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.75_mesp_scalar` | 0.6149 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.75_mesp_scalar` | 0.3638 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.75_mesp_scalar` | 0.2511 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.75_plmesp` | 0.6137 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.75_plmesp` | 0.2778 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.75_plmesp` | 0.3358 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.75_router_eps` | 0.6421 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.75_router_eps` | 0.6421 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.75_router_eps` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.75_router_greedy` | 0.6080 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.75_router_greedy` | 0.6080 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.75_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_a0.75_router_ucb` | 0.6321 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_a0.75_router_ucb` | 0.6321 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='a0.75' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhomeasured_a0.75_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.75_mesp_scalar` | 0.6149 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.75_mesp_scalar` | 0.3638 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.75_mesp_scalar` | 0.2511 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.75_plmesp` | 0.6137 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.75_plmesp` | 0.2702 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.75_plmesp` | 0.3435 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.75_router_eps` | 0.6421 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.75_router_eps` | 0.6421 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.75_router_eps` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.75_router_greedy` | 0.6080 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.75_router_greedy` | 0.6080 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.75_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_a0.75_router_ucb` | 0.6321 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_a0.75_router_ucb` | 0.6321 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='a0.75' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhopaper_a0.75_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_het_mesp_scalar` | 0.6952 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q3_het_mesp_scalar` | 0.4651 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q3_het_mesp_scalar` | 0.2301 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_het_plmesp` | 0.6937 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q3_het_plmesp` | 0.4804 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q3_het_plmesp` | 0.2133 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_het_router_eps` | 0.7185 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q3_het_router_eps` | 0.7105 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q3_het_router_eps` | 0.0080 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_het_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q3_het_router_greedy` | 0.6883 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q3_het_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q3_het_router_ucb` | 0.7210 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q3_het_router_ucb` | 0.7185 | `headline_summary.csv` | `[family_set=='Q3' & alpha=='het' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q3_het_router_ucb` | 0.0025 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_het_mesp_scalar` | 0.6776 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7_het_mesp_scalar` | 0.3734 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7_het_mesp_scalar` | 0.3041 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_het_plmesp` | 0.6577 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7_het_plmesp` | 0.4386 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7_het_plmesp` | 0.2191 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_het_router_eps` | 0.7039 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7_het_router_eps` | 0.6894 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7_het_router_eps` | 0.0145 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_het_router_greedy` | 0.6661 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7_het_router_greedy` | 0.6628 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7_het_router_greedy` | 0.0033 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7_het_router_ucb` | 0.7063 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7_het_router_ucb` | 0.7063 | `headline_summary.csv` | `[family_set=='Q7' & alpha=='het' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7_het_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_het_mesp_scalar` | 0.6821 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_Q7u_het_mesp_scalar` | 0.4443 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_Q7u_het_mesp_scalar` | 0.2377 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_het_plmesp` | 0.6359 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_Q7u_het_plmesp` | 0.4575 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='plmesp'].strategic.mean()` |
| `degrad_Q7u_het_plmesp` | 0.1783 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_het_router_eps` | 0.7093 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_Q7u_het_router_eps` | 0.7072 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='router_eps'].strategic.mean()` |
| `degrad_Q7u_het_router_eps` | 0.0021 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_het_router_greedy` | 0.6724 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_Q7u_het_router_greedy` | 0.6724 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='router_greedy'].strategic.mean()` |
| `degrad_Q7u_het_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_Q7u_het_router_ucb` | 0.7105 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_Q7u_het_router_ucb` | 0.7105 | `headline_summary.csv` | `[family_set=='Q7u' & alpha=='het' & mech=='router_ucb'].strategic.mean()` |
| `degrad_Q7u_het_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_het_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_het_mesp_scalar` | 0.3730 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhomeasured_het_mesp_scalar` | 0.3041 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_het_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_het_plmesp` | 0.2536 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhomeasured_het_plmesp` | 0.4057 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_het_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_het_router_eps` | 0.6950 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhomeasured_het_router_eps` | 0.0006 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_het_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_het_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhomeasured_het_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhomeasured_het_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhomeasured_het_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhomeasured' & alpha=='het' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhomeasured_het_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_het_mesp_scalar` | 0.6771 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='mesp_scalar'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_het_mesp_scalar` | 0.3730 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='mesp_scalar'].strategic.mean()` |
| `degrad_cont_rhopaper_het_mesp_scalar` | 0.3041 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_het_plmesp` | 0.6593 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='plmesp'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_het_plmesp` | 0.2485 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='plmesp'].strategic.mean()` |
| `degrad_cont_rhopaper_het_plmesp` | 0.4108 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_het_router_eps` | 0.6955 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='router_eps'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_het_router_eps` | 0.6950 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='router_eps'].strategic.mean()` |
| `degrad_cont_rhopaper_het_router_eps` | 0.0006 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_het_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='router_greedy'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_het_router_greedy` | 0.6662 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='router_greedy'].strategic.mean()` |
| `degrad_cont_rhopaper_het_router_greedy` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `rev_nonstrat_cont_rhopaper_het_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='router_ucb'].nonstrategic.mean()` |
| `rev_strat_cont_rhopaper_het_router_ucb` | 0.6847 | `headline_summary.csv` | `[family_set=='cont_rhopaper' & alpha=='het' & mech=='router_ucb'].strategic.mean()` |
| `degrad_cont_rhopaper_het_router_ucb` | 0.0000 | `headline_summary.csv` | `same rows, degradation.mean()` |
| `stratminushonest_mean_mesp_scalar` | 0.0386 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='mesp_scalar'].mean()` |
| `stratminushonest_min_mesp_scalar` | -0.0437 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='mesp_scalar'].min()` |
| `stratminushonest_mean_plmesp` | 0.0781 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='plmesp'].mean()` |
| `stratminushonest_min_plmesp` | -0.1953 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='plmesp'].min()` |
| `stratminushonest_mean_router_eps` | 0.4371 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='router_eps'].mean()` |
| `stratminushonest_min_router_eps` | 0.1519 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='router_eps'].min()` |
| `stratminushonest_mean_router_greedy` | 0.4234 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='router_greedy'].mean()` |
| `stratminushonest_min_router_greedy` | 0.1502 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='router_greedy'].min()` |
| `stratminushonest_mean_router_ucb` | 0.4578 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='router_ucb'].mean()` |
| `stratminushonest_min_router_ucb` | 0.1725 | `headline_summary.csv` | `(strategic - honest_bench)[mech=='router_ucb'].min()` |
| `n_headline_configs` | 70 | `headline_summary.csv` | `number of (family_set, triple, alpha) cells present` |
| `exploit_max_Q3_mesp_scalar` | 0.0232 | `exploitability.csv` | `[family_set=='Q3' & mech=='mesp_scalar'].best_gain_per_round.max()` |
| `exploit_max_Q3_plmesp` | 0.0713 | `exploitability.csv` | `[family_set=='Q3' & mech=='plmesp'].best_gain_per_round.max()` |
| `exploit_max_Q3_router_eps` | 0.0212 | `exploitability.csv` | `[family_set=='Q3' & mech=='router_eps'].best_gain_per_round.max()` |
| `exploit_max_Q3_router_greedy` | 0.0227 | `exploitability.csv` | `[family_set=='Q3' & mech=='router_greedy'].best_gain_per_round.max()` |
| `exploit_max_Q3_router_ucb` | 0.0138 | `exploitability.csv` | `[family_set=='Q3' & mech=='router_ucb'].best_gain_per_round.max()` |
| `exploit_max_Q7_mesp_scalar` | 0.0249 | `exploitability.csv` | `[family_set=='Q7' & mech=='mesp_scalar'].best_gain_per_round.max()` |
| `exploit_max_Q7_plmesp` | 0.1053 | `exploitability.csv` | `[family_set=='Q7' & mech=='plmesp'].best_gain_per_round.max()` |
| `exploit_max_Q7_router_eps` | 0.0417 | `exploitability.csv` | `[family_set=='Q7' & mech=='router_eps'].best_gain_per_round.max()` |
| `exploit_max_Q7_router_greedy` | 0.0206 | `exploitability.csv` | `[family_set=='Q7' & mech=='router_greedy'].best_gain_per_round.max()` |
| `exploit_max_Q7_router_ucb` | 0.0107 | `exploitability.csv` | `[family_set=='Q7' & mech=='router_ucb'].best_gain_per_round.max()` |
| `exploit_max_Q7u_mesp_scalar` | 0.1323 | `exploitability.csv` | `[family_set=='Q7u' & mech=='mesp_scalar'].best_gain_per_round.max()` |
| `exploit_max_Q7u_plmesp` | 0.1333 | `exploitability.csv` | `[family_set=='Q7u' & mech=='plmesp'].best_gain_per_round.max()` |
| `exploit_max_Q7u_router_eps` | 0.0080 | `exploitability.csv` | `[family_set=='Q7u' & mech=='router_eps'].best_gain_per_round.max()` |
| `exploit_max_Q7u_router_greedy` | 0.0049 | `exploitability.csv` | `[family_set=='Q7u' & mech=='router_greedy'].best_gain_per_round.max()` |
| `exploit_max_Q7u_router_ucb` | 0.0000 | `exploitability.csv` | `[family_set=='Q7u' & mech=='router_ucb'].best_gain_per_round.max()` |
| `exploit_max_cont_rhomeasured_mesp_scalar` | 0.0248 | `exploitability.csv` | `[family_set=='cont_rhomeasured' & mech=='mesp_scalar'].best_gain_per_round.max()` |
| `exploit_max_cont_rhomeasured_plmesp` | 0.0773 | `exploitability.csv` | `[family_set=='cont_rhomeasured' & mech=='plmesp'].best_gain_per_round.max()` |
| `exploit_max_cont_rhomeasured_router_eps` | 0.0072 | `exploitability.csv` | `[family_set=='cont_rhomeasured' & mech=='router_eps'].best_gain_per_round.max()` |
| `exploit_max_cont_rhomeasured_router_greedy` | 0.0000 | `exploitability.csv` | `[family_set=='cont_rhomeasured' & mech=='router_greedy'].best_gain_per_round.max()` |
| `exploit_max_cont_rhomeasured_router_ucb` | 0.0000 | `exploitability.csv` | `[family_set=='cont_rhomeasured' & mech=='router_ucb'].best_gain_per_round.max()` |
| `exploit_max_cont_rhopaper_mesp_scalar` | 0.0248 | `exploitability.csv` | `[family_set=='cont_rhopaper' & mech=='mesp_scalar'].best_gain_per_round.max()` |
| `exploit_max_cont_rhopaper_plmesp` | 0.0773 | `exploitability.csv` | `[family_set=='cont_rhopaper' & mech=='plmesp'].best_gain_per_round.max()` |
| `exploit_max_cont_rhopaper_router_eps` | 0.0072 | `exploitability.csv` | `[family_set=='cont_rhopaper' & mech=='router_eps'].best_gain_per_round.max()` |
| `exploit_max_cont_rhopaper_router_greedy` | 0.0000 | `exploitability.csv` | `[family_set=='cont_rhopaper' & mech=='router_greedy'].best_gain_per_round.max()` |
| `exploit_max_cont_rhopaper_router_ucb` | 0.0000 | `exploitability.csv` | `[family_set=='cont_rhopaper' & mech=='router_ucb'].best_gain_per_round.max()` |
| `compconv_Q3_mesp_scalar` | 0.3333 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q3_plmesp` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q3_router_eps` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q3_router_greedy` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q3_router_ucb` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7_mesp_scalar` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7_plmesp` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7_router_eps` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7_router_greedy` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7_router_ucb` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7u_mesp_scalar` | 0.3077 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7u_plmesp` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7u_router_eps` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7u_router_greedy` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_Q7u_router_ucb` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhomeasured_mesp_scalar` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhomeasured_plmesp` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhomeasured_router_eps` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhomeasured_router_greedy` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhomeasured_router_ucb` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhopaper_mesp_scalar` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhopaper_plmesp` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhopaper_router_eps` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhopaper_router_greedy` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `compconv_cont_rhopaper_router_ucb` | 0.0000 | `headline_worlds.csv` | `[world=='proposed'].groupby(family_set,mech).compliant_convictions.mean()` |
| `stratdrop_Q3_mesp_scalar` | 0.2294 | `strategic_profiles.csv` | `[family_set=='Q3' & mech=='mesp_scalar'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q3_plmesp` | 0.1990 | `strategic_profiles.csv` | `[family_set=='Q3' & mech=='plmesp'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q3_router_eps` | 0.0447 | `strategic_profiles.csv` | `[family_set=='Q3' & mech=='router_eps'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q3_router_greedy` | 0.0217 | `strategic_profiles.csv` | `[family_set=='Q3' & mech=='router_greedy'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q3_router_ucb` | 0.0106 | `strategic_profiles.csv` | `[family_set=='Q3' & mech=='router_ucb'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7_mesp_scalar` | 0.3104 | `strategic_profiles.csv` | `[family_set=='Q7' & mech=='mesp_scalar'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7_plmesp` | 0.2081 | `strategic_profiles.csv` | `[family_set=='Q7' & mech=='plmesp'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7_router_eps` | 0.0720 | `strategic_profiles.csv` | `[family_set=='Q7' & mech=='router_eps'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7_router_greedy` | 0.0118 | `strategic_profiles.csv` | `[family_set=='Q7' & mech=='router_greedy'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7_router_ucb` | 0.0025 | `strategic_profiles.csv` | `[family_set=='Q7' & mech=='router_ucb'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7u_mesp_scalar` | 0.2099 | `strategic_profiles.csv` | `[family_set=='Q7u' & mech=='mesp_scalar'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7u_plmesp` | 0.1895 | `strategic_profiles.csv` | `[family_set=='Q7u' & mech=='plmesp'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7u_router_eps` | 0.0106 | `strategic_profiles.csv` | `[family_set=='Q7u' & mech=='router_eps'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7u_router_greedy` | 0.0004 | `strategic_profiles.csv` | `[family_set=='Q7u' & mech=='router_greedy'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_Q7u_router_ucb` | 0.0000 | `strategic_profiles.csv` | `[family_set=='Q7u' & mech=='router_ucb'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhomeasured_mesp_scalar` | 0.3145 | `strategic_profiles.csv` | `[family_set=='cont_rhomeasured' & mech=='mesp_scalar'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhomeasured_plmesp` | 0.1164 | `strategic_profiles.csv` | `[family_set=='cont_rhomeasured' & mech=='plmesp'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhomeasured_router_eps` | 0.0014 | `strategic_profiles.csv` | `[family_set=='cont_rhomeasured' & mech=='router_eps'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhomeasured_router_greedy` | 0.0000 | `strategic_profiles.csv` | `[family_set=='cont_rhomeasured' & mech=='router_greedy'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhomeasured_router_ucb` | 0.0000 | `strategic_profiles.csv` | `[family_set=='cont_rhomeasured' & mech=='router_ucb'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhopaper_mesp_scalar` | 0.3145 | `strategic_profiles.csv` | `[family_set=='cont_rhopaper' & mech=='mesp_scalar'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhopaper_plmesp` | 0.0568 | `strategic_profiles.csv` | `[family_set=='cont_rhopaper' & mech=='plmesp'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhopaper_router_eps` | 0.0014 | `strategic_profiles.csv` | `[family_set=='cont_rhopaper' & mech=='router_eps'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhopaper_router_greedy` | 0.0000 | `strategic_profiles.csv` | `[family_set=='cont_rhopaper' & mech=='router_greedy'].revenue_drop_vs_proposed.mean()` |
| `stratdrop_cont_rhopaper_router_ucb` | 0.0000 | `strategic_profiles.csv` | `[family_set=='cont_rhopaper' & mech=='router_ucb'].revenue_drop_vs_proposed.mean()` |
| `frac_strategic_profiles_are_fixed_points` | 0.8714 | `strategic_profiles.csv` | `is_fixed_point.mean()` |
| `richbr_mesp_scalar_nonstrategic` | 0.7089 | `rich_br_from_logs.csv` | `groupby(mech).nonstrategic.mean() for mech=='mesp_scalar'` |
| `richbr_mesp_scalar_strategic` | 0.2490 | `rich_br_from_logs.csv` | `groupby(mech).strategic.mean() for mech=='mesp_scalar'` |
| `richbr_mesp_scalar_degradation` | 0.4599 | `rich_br_from_logs.csv` | `groupby(mech).degradation.mean() for mech=='mesp_scalar'` |
| `richbr_mesp_scalar_worst_degradation` | 0.7737 | `rich_br_from_logs.csv` | `groupby(mech).worst_degradation.mean() for mech=='mesp_scalar'` |
| `richbr_mesp_scalar_n_cells` | 20 | `rich_br_from_logs.csv` | `count for mech=='mesp_scalar'` |
| `richbr_mesp_scalar_undercut_cells` | 0 | `rich_br_from_logs.csv` | `profile.str.contains('undercut').sum() for mech=='mesp_scalar'` |
| `richbr_plmesp_nonstrategic` | 0.6871 | `rich_br_from_logs.csv` | `groupby(mech).nonstrategic.mean() for mech=='plmesp'` |
| `richbr_plmesp_strategic` | 0.3593 | `rich_br_from_logs.csv` | `groupby(mech).strategic.mean() for mech=='plmesp'` |
| `richbr_plmesp_degradation` | 0.3278 | `rich_br_from_logs.csv` | `groupby(mech).degradation.mean() for mech=='plmesp'` |
| `richbr_plmesp_worst_degradation` | 0.6646 | `rich_br_from_logs.csv` | `groupby(mech).worst_degradation.mean() for mech=='plmesp'` |
| `richbr_plmesp_n_cells` | 20 | `rich_br_from_logs.csv` | `count for mech=='plmesp'` |
| `richbr_plmesp_undercut_cells` | 0 | `rich_br_from_logs.csv` | `profile.str.contains('undercut').sum() for mech=='plmesp'` |
| `richbr_router_eps_nonstrategic` | 0.7305 | `rich_br_from_logs.csv` | `groupby(mech).nonstrategic.mean() for mech=='router_eps'` |
| `richbr_router_eps_strategic` | 0.6516 | `rich_br_from_logs.csv` | `groupby(mech).strategic.mean() for mech=='router_eps'` |
| `richbr_router_eps_degradation` | 0.0790 | `rich_br_from_logs.csv` | `groupby(mech).degradation.mean() for mech=='router_eps'` |
| `richbr_router_eps_worst_degradation` | 0.2161 | `rich_br_from_logs.csv` | `groupby(mech).worst_degradation.mean() for mech=='router_eps'` |
| `richbr_router_eps_n_cells` | 20 | `rich_br_from_logs.csv` | `count for mech=='router_eps'` |
| `richbr_router_eps_undercut_cells` | 17 | `rich_br_from_logs.csv` | `profile.str.contains('undercut').sum() for mech=='router_eps'` |
| `richbr_router_greedy_nonstrategic` | 0.6927 | `rich_br_from_logs.csv` | `groupby(mech).nonstrategic.mean() for mech=='router_greedy'` |
| `richbr_router_greedy_strategic` | 0.6440 | `rich_br_from_logs.csv` | `groupby(mech).strategic.mean() for mech=='router_greedy'` |
| `richbr_router_greedy_degradation` | 0.0487 | `rich_br_from_logs.csv` | `groupby(mech).degradation.mean() for mech=='router_greedy'` |
| `richbr_router_greedy_worst_degradation` | 0.1262 | `rich_br_from_logs.csv` | `groupby(mech).worst_degradation.mean() for mech=='router_greedy'` |
| `richbr_router_greedy_n_cells` | 20 | `rich_br_from_logs.csv` | `count for mech=='router_greedy'` |
| `richbr_router_greedy_undercut_cells` | 12 | `rich_br_from_logs.csv` | `profile.str.contains('undercut').sum() for mech=='router_greedy'` |
| `richbr_router_ucb_nonstrategic` | 0.7329 | `rich_br_from_logs.csv` | `groupby(mech).nonstrategic.mean() for mech=='router_ucb'` |
| `richbr_router_ucb_strategic` | 0.6792 | `rich_br_from_logs.csv` | `groupby(mech).strategic.mean() for mech=='router_ucb'` |
| `richbr_router_ucb_degradation` | 0.0537 | `rich_br_from_logs.csv` | `groupby(mech).degradation.mean() for mech=='router_ucb'` |
| `richbr_router_ucb_worst_degradation` | 0.0717 | `rich_br_from_logs.csv` | `groupby(mech).worst_degradation.mean() for mech=='router_ucb'` |
| `richbr_router_ucb_n_cells` | 20 | `rich_br_from_logs.csv` | `count for mech=='router_ucb'` |
| `richbr_router_ucb_undercut_cells` | 20 | `rich_br_from_logs.csv` | `profile.str.contains('undercut').sum() for mech=='router_ucb'` |
| `richbr_mesp_scalar_nonstrategic` | 0.7089 | `rich_br_summary.csv` | `row mech=='mesp_scalar', column nonstrategic` |
| `richbr_mesp_scalar_strategic` | 0.2490 | `rich_br_summary.csv` | `row mech=='mesp_scalar', column strategic` |
| `richbr_mesp_scalar_degradation` | 0.4599 | `rich_br_summary.csv` | `row mech=='mesp_scalar', column degradation` |
| `richbr_mesp_scalar_worst_degradation` | 0.7737 | `rich_br_summary.csv` | `row mech=='mesp_scalar', column worst_degradation` |
| `richbr_mesp_scalar_frac_fixed_point` | 1.0000 | `rich_br_summary.csv` | `row mech=='mesp_scalar', column frac_fixed_point` |
| `richbr_plmesp_nonstrategic` | 0.6871 | `rich_br_summary.csv` | `row mech=='plmesp', column nonstrategic` |
| `richbr_plmesp_strategic` | 0.3593 | `rich_br_summary.csv` | `row mech=='plmesp', column strategic` |
| `richbr_plmesp_degradation` | 0.3278 | `rich_br_summary.csv` | `row mech=='plmesp', column degradation` |
| `richbr_plmesp_worst_degradation` | 0.6646 | `rich_br_summary.csv` | `row mech=='plmesp', column worst_degradation` |
| `richbr_plmesp_frac_fixed_point` | 0.6000 | `rich_br_summary.csv` | `row mech=='plmesp', column frac_fixed_point` |
| `richbr_router_eps_nonstrategic` | 0.7305 | `rich_br_summary.csv` | `row mech=='router_eps', column nonstrategic` |
| `richbr_router_eps_strategic` | 0.6516 | `rich_br_summary.csv` | `row mech=='router_eps', column strategic` |
| `richbr_router_eps_degradation` | 0.0790 | `rich_br_summary.csv` | `row mech=='router_eps', column degradation` |
| `richbr_router_eps_worst_degradation` | 0.2160 | `rich_br_summary.csv` | `row mech=='router_eps', column worst_degradation` |
| `richbr_router_eps_frac_fixed_point` | 0.3500 | `rich_br_summary.csv` | `row mech=='router_eps', column frac_fixed_point` |
| `richbr_router_greedy_nonstrategic` | 0.6928 | `rich_br_summary.csv` | `row mech=='router_greedy', column nonstrategic` |
| `richbr_router_greedy_strategic` | 0.6440 | `rich_br_summary.csv` | `row mech=='router_greedy', column strategic` |
| `richbr_router_greedy_degradation` | 0.0487 | `rich_br_summary.csv` | `row mech=='router_greedy', column degradation` |
| `richbr_router_greedy_worst_degradation` | 0.1262 | `rich_br_summary.csv` | `row mech=='router_greedy', column worst_degradation` |
| `richbr_router_greedy_frac_fixed_point` | 0.8000 | `rich_br_summary.csv` | `row mech=='router_greedy', column frac_fixed_point` |
| `richbr_router_ucb_nonstrategic` | 0.7329 | `rich_br_summary.csv` | `row mech=='router_ucb', column nonstrategic` |
| `richbr_router_ucb_strategic` | 0.6792 | `rich_br_summary.csv` | `row mech=='router_ucb', column strategic` |
| `richbr_router_ucb_degradation` | 0.0537 | `rich_br_summary.csv` | `row mech=='router_ucb', column degradation` |
| `richbr_router_ucb_worst_degradation` | 0.0718 | `rich_br_summary.csv` | `row mech=='router_ucb', column worst_degradation` |
| `richbr_router_ucb_frac_fixed_point` | 0.9500 | `rich_br_summary.csv` | `row mech=='router_ucb', column frac_fixed_point` |
| `soe_plmesp_L-1_na_revenue_per_round` | 0.5995 | `baseline_single_observation_summary.csv` | `row rule==plmesp, L==-1, empty==na, column revenue_per_round` |
| `soe_plmesp_L-1_na_compliant_exclusions` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==plmesp, L==-1, empty==na, column compliant_exclusions` |
| `soe_plmesp_L-1_na_idle_fraction` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==plmesp, L==-1, empty==na, column idle_fraction` |
| `soe_single_observation_exclusion_L1_roundrobin_revenue_per_round` | 0.4695 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==roundrobin, column revenue_per_round` |
| `soe_single_observation_exclusion_L1_roundrobin_compliant_exclusions` | 2.2000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==roundrobin, column compliant_exclusions` |
| `soe_single_observation_exclusion_L1_roundrobin_idle_fraction` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==roundrobin, column idle_fraction` |
| `soe_single_observation_exclusion_L1_roundrobin_price_is_one_share` | 0.7333 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==roundrobin, column price_is_one_share` |
| `soe_single_observation_exclusion_L1_roundrobin_price_is_zero_share` | 0.2667 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==roundrobin, column price_is_zero_share` |
| `soe_single_observation_exclusion_L1_stop_revenue_per_round` | 0.0119 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==stop, column revenue_per_round` |
| `soe_single_observation_exclusion_L1_stop_compliant_exclusions` | 2.2000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==stop, column compliant_exclusions` |
| `soe_single_observation_exclusion_L1_stop_idle_fraction` | 0.7333 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==stop, column idle_fraction` |
| `soe_single_observation_exclusion_L1_stop_price_is_one_share` | 0.7333 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==stop, column price_is_one_share` |
| `soe_single_observation_exclusion_L1_stop_price_is_zero_share` | 0.2667 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==1, empty==stop, column price_is_zero_share` |
| `soe_single_observation_exclusion_L2_roundrobin_revenue_per_round` | 0.5870 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==roundrobin, column revenue_per_round` |
| `soe_single_observation_exclusion_L2_roundrobin_compliant_exclusions` | 2.8250 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==roundrobin, column compliant_exclusions` |
| `soe_single_observation_exclusion_L2_roundrobin_idle_fraction` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==roundrobin, column idle_fraction` |
| `soe_single_observation_exclusion_L2_roundrobin_price_is_one_share` | 0.3417 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==roundrobin, column price_is_one_share` |
| `soe_single_observation_exclusion_L2_roundrobin_price_is_zero_share` | 0.0583 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==roundrobin, column price_is_zero_share` |
| `soe_single_observation_exclusion_L2_stop_revenue_per_round` | 0.0020 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==stop, column revenue_per_round` |
| `soe_single_observation_exclusion_L2_stop_compliant_exclusions` | 2.8250 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==stop, column compliant_exclusions` |
| `soe_single_observation_exclusion_L2_stop_idle_fraction` | 0.9416 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==stop, column idle_fraction` |
| `soe_single_observation_exclusion_L2_stop_price_is_one_share` | 0.3417 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==stop, column price_is_one_share` |
| `soe_single_observation_exclusion_L2_stop_price_is_zero_share` | 0.0583 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==2, empty==stop, column price_is_zero_share` |
| `soe_single_observation_exclusion_L5_roundrobin_revenue_per_round` | 0.6189 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==roundrobin, column revenue_per_round` |
| `soe_single_observation_exclusion_L5_roundrobin_compliant_exclusions` | 3.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==roundrobin, column compliant_exclusions` |
| `soe_single_observation_exclusion_L5_roundrobin_idle_fraction` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==roundrobin, column idle_fraction` |
| `soe_single_observation_exclusion_L5_roundrobin_price_is_one_share` | 0.0583 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==roundrobin, column price_is_one_share` |
| `soe_single_observation_exclusion_L5_roundrobin_price_is_zero_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==roundrobin, column price_is_zero_share` |
| `soe_single_observation_exclusion_L5_stop_revenue_per_round` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==stop, column revenue_per_round` |
| `soe_single_observation_exclusion_L5_stop_compliant_exclusions` | 3.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==stop, column compliant_exclusions` |
| `soe_single_observation_exclusion_L5_stop_idle_fraction` | 0.9999 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==stop, column idle_fraction` |
| `soe_single_observation_exclusion_L5_stop_price_is_one_share` | 0.0583 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==stop, column price_is_one_share` |
| `soe_single_observation_exclusion_L5_stop_price_is_zero_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==5, empty==stop, column price_is_zero_share` |
| `soe_single_observation_exclusion_L20_roundrobin_revenue_per_round` | 0.6188 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==roundrobin, column revenue_per_round` |
| `soe_single_observation_exclusion_L20_roundrobin_compliant_exclusions` | 3.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==roundrobin, column compliant_exclusions` |
| `soe_single_observation_exclusion_L20_roundrobin_idle_fraction` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==roundrobin, column idle_fraction` |
| `soe_single_observation_exclusion_L20_roundrobin_price_is_one_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==roundrobin, column price_is_one_share` |
| `soe_single_observation_exclusion_L20_roundrobin_price_is_zero_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==roundrobin, column price_is_zero_share` |
| `soe_single_observation_exclusion_L20_stop_revenue_per_round` | 0.0001 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==stop, column revenue_per_round` |
| `soe_single_observation_exclusion_L20_stop_compliant_exclusions` | 3.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==stop, column compliant_exclusions` |
| `soe_single_observation_exclusion_L20_stop_idle_fraction` | 0.9998 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==stop, column idle_fraction` |
| `soe_single_observation_exclusion_L20_stop_price_is_one_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==stop, column price_is_one_share` |
| `soe_single_observation_exclusion_L20_stop_price_is_zero_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==20, empty==stop, column price_is_zero_share` |
| `soe_single_observation_exclusion_L100_roundrobin_revenue_per_round` | 0.6188 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==roundrobin, column revenue_per_round` |
| `soe_single_observation_exclusion_L100_roundrobin_compliant_exclusions` | 3.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==roundrobin, column compliant_exclusions` |
| `soe_single_observation_exclusion_L100_roundrobin_idle_fraction` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==roundrobin, column idle_fraction` |
| `soe_single_observation_exclusion_L100_roundrobin_price_is_one_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==roundrobin, column price_is_one_share` |
| `soe_single_observation_exclusion_L100_roundrobin_price_is_zero_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==roundrobin, column price_is_zero_share` |
| `soe_single_observation_exclusion_L100_stop_revenue_per_round` | 0.0006 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==stop, column revenue_per_round` |
| `soe_single_observation_exclusion_L100_stop_compliant_exclusions` | 3.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==stop, column compliant_exclusions` |
| `soe_single_observation_exclusion_L100_stop_idle_fraction` | 0.9990 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==stop, column idle_fraction` |
| `soe_single_observation_exclusion_L100_stop_price_is_one_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==stop, column price_is_one_share` |
| `soe_single_observation_exclusion_L100_stop_price_is_zero_share` | 0.0000 | `baseline_single_observation_summary.csv` | `row rule==single_observation_exclusion, L==100, empty==stop, column price_is_zero_share` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_peak_delivered_mean` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_peak_utility` | 0.1990 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_utility_at_full_capability` | 0.1990 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_total_variation` | 0.1843 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column total_variation` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_announced_price` | 0.6012 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column announced_price` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column own_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_mesp_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_mesp, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_peak_delivered_mean` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_peak_utility` | 0.3870 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_utility_at_full_capability` | 0.3870 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_total_variation` | 0.3844 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column total_variation` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column announced_price` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column own_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_eps_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_eps, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_peak_delivered_mean` | 0.6423 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_peak_utility` | 0.6012 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_utility_at_full_capability` | 0.5868 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_peak_minus_full_capability` | 0.0144 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_total_variation` | 0.9497 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column total_variation` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column announced_price` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column own_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_greedy_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_greedy, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_peak_delivered_mean` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_peak_utility` | 0.2685 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_utility_at_full_capability` | 0.2685 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_total_variation` | 0.2725 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column total_variation` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column announced_price` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column own_capability` |
| `util_measured_unique_top_GSM8K_all_runner_up_router_ucb_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_runner_up_router_ucb, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_third_mesp_peak_delivered_mean` | 0.2058 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_third_mesp_peak_utility` | 0.0404 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_third_mesp_utility_at_full_capability` | 0.0321 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_mesp_peak_minus_full_capability` | 0.0083 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_mesp_total_variation` | 0.0083 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column total_variation` |
| `util_measured_unique_top_GSM8K_all_third_mesp_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column announced_price` |
| `util_measured_unique_top_GSM8K_all_third_mesp_own_capability` | 0.4115 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column own_capability` |
| `util_measured_unique_top_GSM8K_all_third_mesp_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_mesp, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_peak_delivered_mean` | 0.2058 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_peak_utility` | 0.0167 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_utility_at_full_capability` | 0.0133 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_peak_minus_full_capability` | 0.0034 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_total_variation` | 0.0034 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column total_variation` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column announced_price` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_own_capability` | 0.4115 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column own_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_eps_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_eps, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_peak_delivered_mean` | 0.3121 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_peak_utility` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_utility_at_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_total_variation` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column total_variation` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column announced_price` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_own_capability` | 0.4115 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column own_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_greedy_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_greedy, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_peak_delivered_mean` | 0.4115 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_peak_utility` | 0.0013 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_utility_at_full_capability` | 0.0013 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_total_variation` | 0.0020 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column total_variation` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column announced_price` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_own_capability` | 0.4115 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column own_capability` |
| `util_measured_unique_top_GSM8K_all_third_router_ucb_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_third_router_ucb, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_top_mesp_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_top_mesp_peak_utility` | 0.4433 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_top_mesp_utility_at_full_capability` | 0.4433 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_mesp_total_variation` | 0.4274 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column total_variation` |
| `util_measured_unique_top_GSM8K_all_top_mesp_announced_price` | 0.6012 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column announced_price` |
| `util_measured_unique_top_GSM8K_all_top_mesp_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column own_capability` |
| `util_measured_unique_top_GSM8K_all_top_mesp_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_mesp, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_peak_utility` | 0.2716 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_utility_at_full_capability` | 0.2716 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_total_variation` | 0.3215 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column total_variation` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column announced_price` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column own_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_eps_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_eps, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_peak_delivered_mean` | 0.4141 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_peak_utility` | 0.2293 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_utility_at_full_capability` | 0.0836 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_peak_minus_full_capability` | 0.1457 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_total_variation` | 0.2693 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column total_variation` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column announced_price` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column own_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_greedy_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_greedy, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_peak_utility` | 0.3998 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column peak_utility` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_utility_at_full_capability` | 0.3998 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_total_variation` | 0.4006 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column total_variation` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column announced_price` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column own_capability` |
| `util_measured_unique_top_GSM8K_all_top_router_ucb_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_all_top_router_ucb, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_peak_delivered_mean` | 0.5929 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_peak_utility` | 0.1889 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column peak_utility` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_utility_at_full_capability` | 0.1744 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_peak_minus_full_capability` | 0.0145 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_total_variation` | 0.6954 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column total_variation` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column announced_price` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column own_capability` |
| `util_measured_unique_top_GSM8K_primary_runner_up_mesp_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_runner_up_mesp, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_peak_delivered_mean` | 0.2058 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_peak_utility` | 0.0321 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column peak_utility` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_utility_at_full_capability` | 0.0321 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_total_variation` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column total_variation` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column announced_price` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_own_capability` | 0.4115 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column own_capability` |
| `util_measured_unique_top_GSM8K_primary_third_mesp_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_third_mesp, column runner_up_capability` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_peak_delivered_mean` | 0.5963 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_peak_utility` | 0.5114 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column peak_utility` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_utility_at_full_capability` | 0.4677 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_peak_minus_full_capability` | 0.0437 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_total_variation` | 0.6804 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column total_variation` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_announced_price` | 0.6014 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column announced_price` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column own_capability` |
| `util_measured_unique_top_GSM8K_primary_top_mesp_runner_up_capability` | 0.6588 | `utility_curves_summary.csv` | `row measured_unique_top_GSM8K_primary_top_mesp, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_peak_delivered_mean` | 0.2866 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_peak_utility` | 0.0404 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column peak_utility` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_utility_at_full_capability` | 0.0288 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_peak_minus_full_capability` | 0.0116 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_total_variation` | 0.0116 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column total_variation` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_announced_price` | 0.5171 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column announced_price` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column own_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_mesp_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_mesp, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_peak_delivered_mean` | 0.2866 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_peak_utility` | 0.0167 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column peak_utility` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_utility_at_full_capability` | 0.0119 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_peak_minus_full_capability` | 0.0048 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_total_variation` | 0.0048 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column total_variation` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column announced_price` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column own_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_eps_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_eps, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_peak_delivered_mean` | 0.2866 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_peak_utility` | 0.1250 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column peak_utility` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_utility_at_full_capability` | 0.0892 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_peak_minus_full_capability` | 0.0358 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_total_variation` | 0.0358 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column total_variation` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column announced_price` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column own_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_greedy_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_greedy, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_peak_delivered_mean` | 0.5636 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_peak_utility` | 0.0012 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column peak_utility` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_utility_at_full_capability` | 0.0011 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_peak_minus_full_capability` | 0.0001 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_total_variation` | 0.0018 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column total_variation` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column announced_price` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column own_capability` |
| `util_measured_unique_top_MMLU_all_runner_up_router_ucb_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_runner_up_router_ucb, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_third_mesp_peak_delivered_mean` | 0.2614 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_third_mesp_peak_utility` | 0.0404 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column peak_utility` |
| `util_measured_unique_top_MMLU_all_third_mesp_utility_at_full_capability` | 0.0299 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_third_mesp_peak_minus_full_capability` | 0.0106 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_third_mesp_total_variation` | 0.0106 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column total_variation` |
| `util_measured_unique_top_MMLU_all_third_mesp_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column announced_price` |
| `util_measured_unique_top_MMLU_all_third_mesp_own_capability` | 0.5227 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column own_capability` |
| `util_measured_unique_top_MMLU_all_third_mesp_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_mesp, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_third_router_eps_peak_delivered_mean` | 0.2614 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_third_router_eps_peak_utility` | 0.0167 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column peak_utility` |
| `util_measured_unique_top_MMLU_all_third_router_eps_utility_at_full_capability` | 0.0123 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_third_router_eps_peak_minus_full_capability` | 0.0044 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_third_router_eps_total_variation` | 0.0044 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column total_variation` |
| `util_measured_unique_top_MMLU_all_third_router_eps_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column announced_price` |
| `util_measured_unique_top_MMLU_all_third_router_eps_own_capability` | 0.5227 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column own_capability` |
| `util_measured_unique_top_MMLU_all_third_router_eps_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_eps, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_peak_delivered_mean` | 0.4269 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_peak_utility` | 0.1043 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column peak_utility` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_utility_at_full_capability` | 0.0923 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_peak_minus_full_capability` | 0.0120 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_total_variation` | 0.1163 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column total_variation` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column announced_price` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_own_capability` | 0.5227 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column own_capability` |
| `util_measured_unique_top_MMLU_all_third_router_greedy_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_greedy, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_peak_delivered_mean` | 0.5227 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_peak_utility` | 0.0009 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column peak_utility` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_utility_at_full_capability` | 0.0009 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_total_variation` | 0.0010 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column total_variation` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column announced_price` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_own_capability` | 0.5227 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column own_capability` |
| `util_measured_unique_top_MMLU_all_third_router_ucb_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_third_router_ucb, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_top_mesp_peak_delivered_mean` | 0.5845 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_top_mesp_peak_utility` | 0.7611 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column peak_utility` |
| `util_measured_unique_top_MMLU_all_top_mesp_utility_at_full_capability` | 0.5399 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_top_mesp_peak_minus_full_capability` | 0.2212 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_top_mesp_total_variation` | 0.9536 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column total_variation` |
| `util_measured_unique_top_MMLU_all_top_mesp_announced_price` | 0.5171 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column announced_price` |
| `util_measured_unique_top_MMLU_all_top_mesp_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column own_capability` |
| `util_measured_unique_top_MMLU_all_top_mesp_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_mesp, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_top_router_eps_peak_delivered_mean` | 0.5914 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_top_router_eps_peak_utility` | 0.7701 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column peak_utility` |
| `util_measured_unique_top_MMLU_all_top_router_eps_utility_at_full_capability` | 0.5678 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_top_router_eps_peak_minus_full_capability` | 0.2023 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_top_router_eps_total_variation` | 1.0914 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column total_variation` |
| `util_measured_unique_top_MMLU_all_top_router_eps_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column announced_price` |
| `util_measured_unique_top_MMLU_all_top_router_eps_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column own_capability` |
| `util_measured_unique_top_MMLU_all_top_router_eps_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_eps, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_peak_delivered_mean` | 0.6258 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_peak_utility` | 0.4917 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column peak_utility` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_utility_at_full_capability` | 0.4406 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_peak_minus_full_capability` | 0.0511 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_total_variation` | 0.9039 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column total_variation` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column announced_price` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column own_capability` |
| `util_measured_unique_top_MMLU_all_top_router_greedy_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_greedy, column runner_up_capability` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_peak_delivered_mean` | 0.6189 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_peak_utility` | 0.7570 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column peak_utility` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_utility_at_full_capability` | 0.5857 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_peak_minus_full_capability` | 0.1712 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_total_variation` | 0.9266 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column total_variation` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column announced_price` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column own_capability` |
| `util_measured_unique_top_MMLU_all_top_router_ucb_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_all_top_router_ucb, column runner_up_capability` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_peak_delivered_mean` | 0.2866 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_peak_utility` | 0.0288 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column peak_utility` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_utility_at_full_capability` | 0.0288 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_total_variation` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column total_variation` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column announced_price` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column own_capability` |
| `util_measured_unique_top_MMLU_primary_runner_up_mesp_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_runner_up_mesp, column runner_up_capability` |
| `util_measured_unique_top_MMLU_primary_third_mesp_peak_delivered_mean` | 0.2614 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_primary_third_mesp_peak_utility` | 0.0299 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column peak_utility` |
| `util_measured_unique_top_MMLU_primary_third_mesp_utility_at_full_capability` | 0.0299 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_primary_third_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_primary_third_mesp_total_variation` | 0.0000 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column total_variation` |
| `util_measured_unique_top_MMLU_primary_third_mesp_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column announced_price` |
| `util_measured_unique_top_MMLU_primary_third_mesp_own_capability` | 0.5227 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column own_capability` |
| `util_measured_unique_top_MMLU_primary_third_mesp_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_third_mesp, column runner_up_capability` |
| `util_measured_unique_top_MMLU_primary_top_mesp_peak_delivered_mean` | 0.5157 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column peak_delivered_mean` |
| `util_measured_unique_top_MMLU_primary_top_mesp_peak_utility` | 0.8118 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column peak_utility` |
| `util_measured_unique_top_MMLU_primary_top_mesp_utility_at_full_capability` | 0.5399 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column utility_at_full_capability` |
| `util_measured_unique_top_MMLU_primary_top_mesp_peak_minus_full_capability` | 0.2719 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column peak_minus_full_capability` |
| `util_measured_unique_top_MMLU_primary_top_mesp_total_variation` | 0.5511 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column total_variation` |
| `util_measured_unique_top_MMLU_primary_top_mesp_announced_price` | 0.5188 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column announced_price` |
| `util_measured_unique_top_MMLU_primary_top_mesp_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column own_capability` |
| `util_measured_unique_top_MMLU_primary_top_mesp_runner_up_capability` | 0.5731 | `utility_curves_summary.csv` | `row measured_unique_top_MMLU_primary_top_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_peak_utility` | 0.4008 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_utility_at_full_capability` | 0.4008 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_total_variation` | 0.3858 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_announced_price` | 0.6050 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_peak_utility` | 0.4652 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_utility_at_full_capability` | 0.4652 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_total_variation` | 0.4896 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_eps, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_peak_delivered_mean` | 0.5080 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_peak_utility` | 0.1029 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_utility_at_full_capability` | 0.0836 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_peak_minus_full_capability` | 0.0193 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_total_variation` | 0.2949 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_greedy, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_peak_utility` | 0.2365 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_utility_at_full_capability` | 0.2365 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_total_variation` | 0.2373 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_runner_up_router_ucb, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_peak_delivered_mean` | 0.3294 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_peak_utility` | 0.0404 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_utility_at_full_capability` | 0.0271 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_peak_minus_full_capability` | 0.0133 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_total_variation` | 0.0133 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_mesp_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_peak_delivered_mean` | 0.6588 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_peak_utility` | 0.1064 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_utility_at_full_capability` | 0.1064 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_total_variation` | 0.1073 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_eps_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_eps, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_peak_delivered_mean` | 0.6313 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_peak_utility` | 0.3490 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_utility_at_full_capability` | 0.3353 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_peak_minus_full_capability` | 0.0137 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_total_variation` | 0.6427 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_greedy_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_greedy, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_peak_delivered_mean` | 0.6588 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_peak_utility` | 0.1583 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_utility_at_full_capability` | 0.1583 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_total_variation` | 0.1622 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_third_router_ucb_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_third_router_ucb, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_peak_utility` | 0.2139 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_utility_at_full_capability` | 0.2139 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_total_variation` | 0.1993 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_announced_price` | 0.6050 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_mesp_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_peak_delivered_mean` | 0.6571 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_peak_utility` | 0.0943 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_utility_at_full_capability` | 0.0891 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_peak_minus_full_capability` | 0.0052 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_total_variation` | 0.0950 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_eps_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_eps, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_peak_utility` | 0.2508 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_utility_at_full_capability` | 0.2508 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_total_variation` | 0.8816 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_greedy_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_greedy, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_peak_delivered_mean` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_peak_utility` | 0.2732 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_utility_at_full_capability` | 0.2732 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_total_variation` | 0.2747 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_all_top_router_ucb_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_all_top_router_ucb, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_peak_delivered_mean` | 0.6018 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_peak_utility` | 0.4092 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_utility_at_full_capability` | 0.3774 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_peak_minus_full_capability` | 0.0318 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_total_variation` | 0.9703 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_runner_up_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_peak_delivered_mean` | 0.3294 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_peak_utility` | 0.0271 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_utility_at_full_capability` | 0.0271 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_total_variation` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_own_capability` | 0.6588 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_third_mesp_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_third_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_peak_delivered_mean` | 0.5963 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_peak_utility` | 0.2581 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_utility_at_full_capability` | 0.2373 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_peak_minus_full_capability` | 0.0208 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_total_variation` | 0.4089 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_announced_price` | 0.6055 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_own_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_GSM8K_primary_top_mesp_runner_up_capability` | 0.6626 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_GSM8K_primary_top_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_peak_delivered_mean` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_peak_utility` | 0.2289 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_utility_at_full_capability` | 0.2289 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_total_variation` | 0.2207 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_announced_price` | 0.7676 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_mesp_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_peak_delivered_mean` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_peak_utility` | 0.4573 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_utility_at_full_capability` | 0.4573 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_total_variation` | 0.4706 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_eps, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_peak_delivered_mean` | 0.7839 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_peak_utility` | 0.3143 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_utility_at_full_capability` | 0.2937 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_peak_minus_full_capability` | 0.0206 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_total_variation` | 0.5299 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_greedy, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_peak_delivered_mean` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_peak_utility` | 0.2963 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_utility_at_full_capability` | 0.2963 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_total_variation` | 0.2987 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_runner_up_router_ucb, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_peak_delivered_mean` | 0.2866 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_peak_utility` | 0.0404 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_utility_at_full_capability` | 0.0288 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_peak_minus_full_capability` | 0.0116 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_total_variation` | 0.0116 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_mesp_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_peak_delivered_mean` | 0.2866 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_peak_utility` | 0.0124 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_utility_at_full_capability` | 0.0089 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_peak_minus_full_capability` | 0.0036 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_total_variation` | 0.0036 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_eps_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_eps, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_peak_delivered_mean` | 0.5254 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_peak_utility` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_utility_at_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_total_variation` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_greedy_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_greedy, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_peak_delivered_mean` | 0.5540 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_peak_utility` | 0.0013 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_utility_at_full_capability` | 0.0012 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_peak_minus_full_capability` | 0.0001 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_total_variation` | 0.0025 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_third_router_ucb_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_third_router_ucb, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_peak_delivered_mean` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_peak_utility` | 0.3110 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_utility_at_full_capability` | 0.3110 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_total_variation` | 0.3028 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_announced_price` | 0.7676 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_mesp_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_peak_delivered_mean` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_peak_utility` | 0.1155 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_utility_at_full_capability` | 0.1155 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_total_variation` | 0.1394 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_eps_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_eps, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_peak_delivered_mean` | 0.7839 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_peak_utility` | 0.3143 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_utility_at_full_capability` | 0.2937 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_peak_minus_full_capability` | 0.0206 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_total_variation` | 0.7144 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_greedy_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_greedy, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_peak_delivered_mean` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_peak_utility` | 0.2917 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_utility_at_full_capability` | 0.2917 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_total_variation` | 0.2941 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_all_top_router_ucb_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_all_top_router_ucb, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_peak_delivered_mean` | 0.7633 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_peak_utility` | 0.2279 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_utility_at_full_capability` | 0.2084 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_peak_minus_full_capability` | 0.0195 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_total_variation` | 0.7297 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_runner_up_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_peak_delivered_mean` | 0.2866 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_peak_utility` | 0.0288 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_utility_at_full_capability` | 0.0288 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_peak_minus_full_capability` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_total_variation` | 0.0000 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_own_capability` | 0.5731 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_third_mesp_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_third_mesp, column runner_up_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_peak_delivered_mean` | 0.7633 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column peak_delivered_mean` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_peak_utility` | 0.3639 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column peak_utility` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_utility_at_full_capability` | 0.3315 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column utility_at_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_peak_minus_full_capability` | 0.0324 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column peak_minus_full_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_total_variation` | 0.5824 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column total_variation` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_announced_price` | 0.7670 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column announced_price` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_own_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column own_capability` |
| `util_two_top_CONSTRUCTED_MMLU_primary_top_mesp_runner_up_capability` | 0.8252 | `utility_curves_summary.csv` | `row two_top_CONSTRUCTED_MMLU_primary_top_mesp, column runner_up_capability` |
| `fine_maxgain_mesp_scalar` | 0.0026 | `fine_shading_best.csv` | `[mech=='mesp_scalar'].gain_per_round.max()` |
| `fine_maxrevloss_mesp_scalar` | 0.0639 | `fine_shading_best.csv` | `[mech=='mesp_scalar'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_mesp_scalar` | 0.0260 | `fine_shading_best.csv` | `[mech=='mesp_scalar'].revenue_loss_per_round.mean()` |
| `fine_maxgain_plmesp` | 0.0105 | `fine_shading_best.csv` | `[mech=='plmesp'].gain_per_round.max()` |
| `fine_maxrevloss_plmesp` | 0.0513 | `fine_shading_best.csv` | `[mech=='plmesp'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_plmesp` | 0.0148 | `fine_shading_best.csv` | `[mech=='plmesp'].revenue_loss_per_round.mean()` |
| `fine_maxgain_router_eps` | 0.0648 | `fine_shading_best.csv` | `[mech=='router_eps'].gain_per_round.max()` |
| `fine_maxrevloss_router_eps` | 0.0983 | `fine_shading_best.csv` | `[mech=='router_eps'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_router_eps` | 0.0516 | `fine_shading_best.csv` | `[mech=='router_eps'].revenue_loss_per_round.mean()` |
| `fine_maxgain_router_greedy` | 0.0445 | `fine_shading_best.csv` | `[mech=='router_greedy'].gain_per_round.max()` |
| `fine_maxrevloss_router_greedy` | 0.0813 | `fine_shading_best.csv` | `[mech=='router_greedy'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_router_greedy` | 0.0252 | `fine_shading_best.csv` | `[mech=='router_greedy'].revenue_loss_per_round.mean()` |
| `fine_maxgain_router_ucb` | 0.0578 | `fine_shading_best.csv` | `[mech=='router_ucb'].gain_per_round.max()` |
| `fine_maxrevloss_router_ucb` | 0.0717 | `fine_shading_best.csv` | `[mech=='router_ucb'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_router_ucb` | 0.0513 | `fine_shading_best.csv` | `[mech=='router_ucb'].revenue_loss_per_round.mean()` |
| `fine_maxgain_mesp_scalar` | 0.0026 | `fine_shading_best.csv` | `[mech=='mesp_scalar'].gain_per_round.max()` |
| `fine_maxrevloss_mesp_scalar` | 0.0639 | `fine_shading_best.csv` | `[mech=='mesp_scalar'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_mesp_scalar` | 0.0260 | `fine_shading_best.csv` | `[mech=='mesp_scalar'].revenue_loss_per_round.mean()` |
| `fine_maxgain_plmesp` | 0.0105 | `fine_shading_best.csv` | `[mech=='plmesp'].gain_per_round.max()` |
| `fine_maxrevloss_plmesp` | 0.0513 | `fine_shading_best.csv` | `[mech=='plmesp'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_plmesp` | 0.0148 | `fine_shading_best.csv` | `[mech=='plmesp'].revenue_loss_per_round.mean()` |
| `fine_maxgain_router_eps` | 0.0648 | `fine_shading_best.csv` | `[mech=='router_eps'].gain_per_round.max()` |
| `fine_maxrevloss_router_eps` | 0.0983 | `fine_shading_best.csv` | `[mech=='router_eps'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_router_eps` | 0.0516 | `fine_shading_best.csv` | `[mech=='router_eps'].revenue_loss_per_round.mean()` |
| `fine_maxgain_router_greedy` | 0.0445 | `fine_shading_best.csv` | `[mech=='router_greedy'].gain_per_round.max()` |
| `fine_maxrevloss_router_greedy` | 0.0813 | `fine_shading_best.csv` | `[mech=='router_greedy'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_router_greedy` | 0.0252 | `fine_shading_best.csv` | `[mech=='router_greedy'].revenue_loss_per_round.mean()` |
| `fine_maxgain_router_ucb` | 0.0578 | `fine_shading_best.csv` | `[mech=='router_ucb'].gain_per_round.max()` |
| `fine_maxrevloss_router_ucb` | 0.0717 | `fine_shading_best.csv` | `[mech=='router_ucb'].revenue_loss_per_round.max()` |
| `fine_meanrevloss_router_ucb` | 0.0513 | `fine_shading_best.csv` | `[mech=='router_ucb'].revenue_loss_per_round.mean()` |
| `undercut_meangain_mesp_scalar` | 0.0006 | `undercut_summary.csv` | `row mech=='mesp_scalar', mean_gain` |
| `undercut_maxgain_mesp_scalar` | 0.0019 | `undercut_summary.csv` | `row mech=='mesp_scalar', max_gain` |
| `undercut_meanrevloss_mesp_scalar` | 0.0011 | `undercut_summary.csv` | `row mech=='mesp_scalar', mean_revenue_loss` |
| `undercut_maxrevloss_mesp_scalar` | 0.0039 | `undercut_summary.csv` | `row mech=='mesp_scalar', max_revenue_loss` |
| `undercut_meangain_plmesp` | 0.0000 | `undercut_summary.csv` | `row mech=='plmesp', mean_gain` |
| `undercut_maxgain_plmesp` | 0.0001 | `undercut_summary.csv` | `row mech=='plmesp', max_gain` |
| `undercut_meanrevloss_plmesp` | 0.0000 | `undercut_summary.csv` | `row mech=='plmesp', mean_revenue_loss` |
| `undercut_maxrevloss_plmesp` | 0.0001 | `undercut_summary.csv` | `row mech=='plmesp', max_revenue_loss` |
| `undercut_meangain_router_eps` | 0.0422 | `undercut_summary.csv` | `row mech=='router_eps', mean_gain` |
| `undercut_maxgain_router_eps` | 0.0648 | `undercut_summary.csv` | `row mech=='router_eps', max_gain` |
| `undercut_meanrevloss_router_eps` | 0.0516 | `undercut_summary.csv` | `row mech=='router_eps', mean_revenue_loss` |
| `undercut_maxrevloss_router_eps` | 0.0983 | `undercut_summary.csv` | `row mech=='router_eps', max_revenue_loss` |
| `undercut_meangain_router_greedy` | 0.0097 | `undercut_summary.csv` | `row mech=='router_greedy', mean_gain` |
| `undercut_maxgain_router_greedy` | 0.0363 | `undercut_summary.csv` | `row mech=='router_greedy', max_gain` |
| `undercut_meanrevloss_router_greedy` | 0.0315 | `undercut_summary.csv` | `row mech=='router_greedy', mean_revenue_loss` |
| `undercut_maxrevloss_router_greedy` | 0.0813 | `undercut_summary.csv` | `row mech=='router_greedy', max_revenue_loss` |
| `undercut_meangain_router_ucb` | 0.0272 | `undercut_summary.csv` | `row mech=='router_ucb', mean_gain` |
| `undercut_maxgain_router_ucb` | 0.0578 | `undercut_summary.csv` | `row mech=='router_ucb', max_gain` |
| `undercut_meanrevloss_router_ucb` | 0.0513 | `undercut_summary.csv` | `row mech=='router_ucb', mean_revenue_loss` |
| `undercut_maxrevloss_router_ucb` | 0.0717 | `undercut_summary.csv` | `row mech=='router_ucb', max_revenue_loss` |
| `twotopbest_Q3_K2_gap` | 0.0185 | `two_top_best_subsets.csv` | `row Q3/K=2, mean_top_gap` |
| `twotopbest_Q3_K2_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=2, mass_within_0.05` |
| `twotopbest_Q3_K3_gap` | 0.0220 | `two_top_best_subsets.csv` | `row Q3/K=3, mean_top_gap` |
| `twotopbest_Q3_K3_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=3, mass_within_0.05` |
| `twotopbest_Q3_K4_gap` | 0.0214 | `two_top_best_subsets.csv` | `row Q3/K=4, mean_top_gap` |
| `twotopbest_Q3_K4_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=4, mass_within_0.05` |
| `twotopbest_Q3_K5_gap` | 0.0214 | `two_top_best_subsets.csv` | `row Q3/K=5, mean_top_gap` |
| `twotopbest_Q3_K5_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=5, mass_within_0.05` |
| `twotopbest_Q3_K6_gap` | 0.0214 | `two_top_best_subsets.csv` | `row Q3/K=6, mean_top_gap` |
| `twotopbest_Q3_K6_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=6, mass_within_0.05` |
| `twotopbest_Q3_K7_gap` | 0.0214 | `two_top_best_subsets.csv` | `row Q3/K=7, mean_top_gap` |
| `twotopbest_Q3_K7_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=7, mass_within_0.05` |
| `twotopbest_Q3_K8_gap` | 0.0214 | `two_top_best_subsets.csv` | `row Q3/K=8, mean_top_gap` |
| `twotopbest_Q3_K8_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=8, mass_within_0.05` |
| `twotopbest_Q3_K9_gap` | 0.0214 | `two_top_best_subsets.csv` | `row Q3/K=9, mean_top_gap` |
| `twotopbest_Q3_K9_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q3/K=9, mass_within_0.05` |
| `twotopbest_Q3_K10_gap` | 0.0351 | `two_top_best_subsets.csv` | `row Q3/K=10, mean_top_gap` |
| `twotopbest_Q3_K10_mass005` | 0.6816 | `two_top_best_subsets.csv` | `row Q3/K=10, mass_within_0.05` |
| `twotopbest_Q3_K11_gap` | 0.0545 | `two_top_best_subsets.csv` | `row Q3/K=11, mean_top_gap` |
| `twotopbest_Q3_K11_mass005` | 0.5547 | `two_top_best_subsets.csv` | `row Q3/K=11, mass_within_0.05` |
| `twotopbest_Q7_K2_gap` | 0.0199 | `two_top_best_subsets.csv` | `row Q7/K=2, mean_top_gap` |
| `twotopbest_Q7_K2_mass005` | 0.9877 | `two_top_best_subsets.csv` | `row Q7/K=2, mass_within_0.05` |
| `twotopbest_Q7_K3_gap` | 0.0229 | `two_top_best_subsets.csv` | `row Q7/K=3, mean_top_gap` |
| `twotopbest_Q7_K3_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q7/K=3, mass_within_0.05` |
| `twotopbest_Q7_K4_gap` | 0.0229 | `two_top_best_subsets.csv` | `row Q7/K=4, mean_top_gap` |
| `twotopbest_Q7_K4_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q7/K=4, mass_within_0.05` |
| `twotopbest_Q7_K5_gap` | 0.0229 | `two_top_best_subsets.csv` | `row Q7/K=5, mean_top_gap` |
| `twotopbest_Q7_K5_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q7/K=5, mass_within_0.05` |
| `twotopbest_Q7_K6_gap` | 0.0229 | `two_top_best_subsets.csv` | `row Q7/K=6, mean_top_gap` |
| `twotopbest_Q7_K6_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q7/K=6, mass_within_0.05` |
| `twotopbest_Q7_K7_gap` | 0.0229 | `two_top_best_subsets.csv` | `row Q7/K=7, mean_top_gap` |
| `twotopbest_Q7_K7_mass005` | 1.0000 | `two_top_best_subsets.csv` | `row Q7/K=7, mass_within_0.05` |
| `twotopbest_Q7_K8_gap` | 0.0232 | `two_top_best_subsets.csv` | `row Q7/K=8, mean_top_gap` |
| `twotopbest_Q7_K8_mass005` | 0.9581 | `two_top_best_subsets.csv` | `row Q7/K=8, mass_within_0.05` |
| `twotopbest_Q7_K9_gap` | 0.0232 | `two_top_best_subsets.csv` | `row Q7/K=9, mean_top_gap` |
| `twotopbest_Q7_K9_mass005` | 0.9581 | `two_top_best_subsets.csv` | `row Q7/K=9, mass_within_0.05` |
| `twotopbest_Q7_K10_gap` | 0.0349 | `two_top_best_subsets.csv` | `row Q7/K=10, mean_top_gap` |
| `twotopbest_Q7_K10_mass005` | 0.6747 | `two_top_best_subsets.csv` | `row Q7/K=10, mass_within_0.05` |
| `twotopbest_Q7_K11_gap` | 0.0558 | `two_top_best_subsets.csv` | `row Q7/K=11, mean_top_gap` |
| `twotopbest_Q7_K11_mass005` | 0.5573 | `two_top_best_subsets.csv` | `row Q7/K=11, mass_within_0.05` |
| `gap_mesp_scalar_d0_equilibrium_revenue` | 0.3743 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0` |
| `gap_mesp_scalar_d0_revenue_at_proposed` | 0.7930 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0` |
| `gap_mesp_scalar_d0_runner_up_curve_total_variation` | 0.4972 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0` |
| `gap_mesp_scalar_d0.001_equilibrium_revenue` | 0.3743 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.001` |
| `gap_mesp_scalar_d0.001_revenue_at_proposed` | 0.7924 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.001` |
| `gap_mesp_scalar_d0.001_runner_up_curve_total_variation` | 0.4398 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.001` |
| `gap_mesp_scalar_d0.002_equilibrium_revenue` | 0.7960 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.002` |
| `gap_mesp_scalar_d0.002_revenue_at_proposed` | 0.7921 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.002` |
| `gap_mesp_scalar_d0.002_runner_up_curve_total_variation` | 0.3754 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.002` |
| `gap_mesp_scalar_d0.005_equilibrium_revenue` | 0.7960 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.005` |
| `gap_mesp_scalar_d0.005_revenue_at_proposed` | 0.7902 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.005` |
| `gap_mesp_scalar_d0.005_runner_up_curve_total_variation` | 0.1425 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.005` |
| `gap_mesp_scalar_d0.0075_equilibrium_revenue` | 0.7796 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.0075` |
| `gap_mesp_scalar_d0.0075_revenue_at_proposed` | 0.7886 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.0075` |
| `gap_mesp_scalar_d0.0075_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.0075` |
| `gap_mesp_scalar_d0.01_equilibrium_revenue` | 0.7773 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.01` |
| `gap_mesp_scalar_d0.01_revenue_at_proposed` | 0.7873 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.01` |
| `gap_mesp_scalar_d0.01_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.01` |
| `gap_mesp_scalar_d0.015_equilibrium_revenue` | 0.7780 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.015` |
| `gap_mesp_scalar_d0.015_revenue_at_proposed` | 0.7849 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.015` |
| `gap_mesp_scalar_d0.015_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.015` |
| `gap_mesp_scalar_d0.02_equilibrium_revenue` | 0.7807 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.02` |
| `gap_mesp_scalar_d0.02_revenue_at_proposed` | 0.7828 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.02` |
| `gap_mesp_scalar_d0.02_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.02` |
| `gap_mesp_scalar_d0.03_equilibrium_revenue` | 0.7626 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.03` |
| `gap_mesp_scalar_d0.03_revenue_at_proposed` | 0.7751 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.03` |
| `gap_mesp_scalar_d0.03_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.03` |
| `gap_mesp_scalar_d0.05_equilibrium_revenue` | 0.7433 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.05` |
| `gap_mesp_scalar_d0.05_revenue_at_proposed` | 0.7451 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.05` |
| `gap_mesp_scalar_d0.05_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.05` |
| `gap_mesp_scalar_d0.1_equilibrium_revenue` | 0.3288 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.1` |
| `gap_mesp_scalar_d0.1_revenue_at_proposed` | 0.6674 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.1` |
| `gap_mesp_scalar_d0.1_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.1` |
| `gap_mesp_scalar_d0.2_equilibrium_revenue` | 0.2827 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.2` |
| `gap_mesp_scalar_d0.2_revenue_at_proposed` | 0.5765 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.2` |
| `gap_mesp_scalar_d0.2_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.2` |
| `gap_mesp_scalar_d0.4_equilibrium_revenue` | 0.2284 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.4` |
| `gap_mesp_scalar_d0.4_revenue_at_proposed` | 0.4718 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.4` |
| `gap_mesp_scalar_d0.4_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech mesp_scalar, delta 0.4` |
| `gap_plmesp_d0_equilibrium_revenue` | 0.7279 | `capability_gap_summary.csv` | `row mech plmesp, delta 0` |
| `gap_plmesp_d0_revenue_at_proposed` | 0.7541 | `capability_gap_summary.csv` | `row mech plmesp, delta 0` |
| `gap_plmesp_d0_announced_price_mean` | 0.7440 | `capability_gap_summary.csv` | `row mech plmesp, delta 0` |
| `gap_plmesp_d0_runner_up_curve_total_variation` | 0.1197 | `capability_gap_summary.csv` | `row mech plmesp, delta 0` |
| `gap_plmesp_d0.001_equilibrium_revenue` | 0.7274 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.001` |
| `gap_plmesp_d0.001_revenue_at_proposed` | 0.7536 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.001` |
| `gap_plmesp_d0.001_announced_price_mean` | 0.7433 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.001` |
| `gap_plmesp_d0.001_runner_up_curve_total_variation` | 0.1061 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.001` |
| `gap_plmesp_d0.002_equilibrium_revenue` | 0.7268 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.002` |
| `gap_plmesp_d0.002_revenue_at_proposed` | 0.7530 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.002` |
| `gap_plmesp_d0.002_announced_price_mean` | 0.7425 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.002` |
| `gap_plmesp_d0.002_runner_up_curve_total_variation` | 0.0911 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.002` |
| `gap_plmesp_d0.005_equilibrium_revenue` | 0.7251 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.005` |
| `gap_plmesp_d0.005_revenue_at_proposed` | 0.7513 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.005` |
| `gap_plmesp_d0.005_announced_price_mean` | 0.7402 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.005` |
| `gap_plmesp_d0.005_runner_up_curve_total_variation` | 0.0913 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.005` |
| `gap_plmesp_d0.0055_equilibrium_revenue` | 0.7248 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0055` |
| `gap_plmesp_d0.0055_revenue_at_proposed` | 0.7511 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0055` |
| `gap_plmesp_d0.0055_announced_price_mean` | 0.7398 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0055` |
| `gap_plmesp_d0.0055_runner_up_curve_total_variation` | 0.0868 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0055` |
| `gap_plmesp_d0.006_equilibrium_revenue` | 0.7245 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.006` |
| `gap_plmesp_d0.006_revenue_at_proposed` | 0.7507 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.006` |
| `gap_plmesp_d0.006_announced_price_mean` | 0.7393 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.006` |
| `gap_plmesp_d0.006_runner_up_curve_total_variation` | 0.0875 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.006` |
| `gap_plmesp_d0.0065_equilibrium_revenue` | 0.4405 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0065` |
| `gap_plmesp_d0.0065_revenue_at_proposed` | 0.7504 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0065` |
| `gap_plmesp_d0.0065_announced_price_mean` | 0.7389 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0065` |
| `gap_plmesp_d0.0065_runner_up_curve_total_variation` | 0.0423 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0065` |
| `gap_plmesp_d0.0068_equilibrium_revenue` | 0.4404 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0068` |
| `gap_plmesp_d0.0068_revenue_at_proposed` | 0.7503 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0068` |
| `gap_plmesp_d0.0068_announced_price_mean` | 0.7387 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0068` |
| `gap_plmesp_d0.0068_runner_up_curve_total_variation` | 0.0411 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0068` |
| `gap_plmesp_d0.007_equilibrium_revenue` | 0.4403 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.007` |
| `gap_plmesp_d0.007_revenue_at_proposed` | 0.7501 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.007` |
| `gap_plmesp_d0.007_announced_price_mean` | 0.7384 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.007` |
| `gap_plmesp_d0.007_runner_up_curve_total_variation` | 0.0438 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.007` |
| `gap_plmesp_d0.0072_equilibrium_revenue` | 0.4403 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0072` |
| `gap_plmesp_d0.0072_revenue_at_proposed` | 0.7499 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0072` |
| `gap_plmesp_d0.0072_announced_price_mean` | 0.7382 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0072` |
| `gap_plmesp_d0.0072_runner_up_curve_total_variation` | 0.0436 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0072` |
| `gap_plmesp_d0.0075_equilibrium_revenue` | 0.4402 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0075` |
| `gap_plmesp_d0.0075_revenue_at_proposed` | 0.7497 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0075` |
| `gap_plmesp_d0.0075_announced_price_mean` | 0.7379 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0075` |
| `gap_plmesp_d0.0075_runner_up_curve_total_variation` | 0.0436 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.0075` |
| `gap_plmesp_d0.01_equilibrium_revenue` | 0.4393 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.01` |
| `gap_plmesp_d0.01_revenue_at_proposed` | 0.7480 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.01` |
| `gap_plmesp_d0.01_announced_price_mean` | 0.7354 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.01` |
| `gap_plmesp_d0.01_runner_up_curve_total_variation` | 0.0450 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.01` |
| `gap_plmesp_d0.015_equilibrium_revenue` | 0.4377 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.015` |
| `gap_plmesp_d0.015_revenue_at_proposed` | 0.7444 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.015` |
| `gap_plmesp_d0.015_announced_price_mean` | 0.7302 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.015` |
| `gap_plmesp_d0.015_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.015` |
| `gap_plmesp_d0.02_equilibrium_revenue` | 0.4360 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.02` |
| `gap_plmesp_d0.02_revenue_at_proposed` | 0.7410 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.02` |
| `gap_plmesp_d0.02_announced_price_mean` | 0.7254 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.02` |
| `gap_plmesp_d0.02_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.02` |
| `gap_plmesp_d0.03_equilibrium_revenue` | 0.4325 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.03` |
| `gap_plmesp_d0.03_revenue_at_proposed` | 0.7340 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.03` |
| `gap_plmesp_d0.03_announced_price_mean` | 0.7153 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.03` |
| `gap_plmesp_d0.03_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.03` |
| `gap_plmesp_d0.05_equilibrium_revenue` | 0.4255 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.05` |
| `gap_plmesp_d0.05_revenue_at_proposed` | 0.7202 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.05` |
| `gap_plmesp_d0.05_announced_price_mean` | 0.6957 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.05` |
| `gap_plmesp_d0.05_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.05` |
| `gap_plmesp_d0.1_equilibrium_revenue` | 0.4080 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.1` |
| `gap_plmesp_d0.1_revenue_at_proposed` | 0.6853 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.1` |
| `gap_plmesp_d0.1_announced_price_mean` | 0.6458 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.1` |
| `gap_plmesp_d0.1_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.1` |
| `gap_plmesp_d0.2_equilibrium_revenue` | 0.3732 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.2` |
| `gap_plmesp_d0.2_revenue_at_proposed` | 0.6155 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.2` |
| `gap_plmesp_d0.2_announced_price_mean` | 0.5462 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.2` |
| `gap_plmesp_d0.2_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.2` |
| `gap_plmesp_d0.4_equilibrium_revenue` | 0.3290 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.4` |
| `gap_plmesp_d0.4_revenue_at_proposed` | 0.5274 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.4` |
| `gap_plmesp_d0.4_announced_price_mean` | 0.4422 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.4` |
| `gap_plmesp_d0.4_runner_up_curve_total_variation` | 0.0000 | `capability_gap_summary.csv` | `row mech plmesp, delta 0.4` |
| `sb_contextual_mesp_scalar_proposed_revenue_per_round` | 0.5783 | `baseline_second_best_summary.csv` | `row setting contextual, mech mesp_scalar, proposed` |
| `sb_contextual_mesp_scalar_proposed_monitor_fire_rate` | 0.2727 | `baseline_second_best_summary.csv` | `row setting contextual, mech mesp_scalar, proposed` |
| `sb_contextual_mesp_scalar_proposed_compliant_conviction_rate` | 0.2727 | `baseline_second_best_summary.csv` | `row setting contextual, mech mesp_scalar, proposed` |
| `sb_contextual_mesp_scalar_proposed_undelegated_fraction` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech mesp_scalar, proposed` |
| `sb_contextual_mesp_scalar_proposed_post_fire_revenue_per_round` | 0.6513 | `baseline_second_best_summary.csv` | `row setting contextual, mech mesp_scalar, proposed` |
| `sb_contextual_mesp_scalar_proposed_price_above_cap_mass` | 0.1201 | `baseline_second_best_summary.csv` | `row setting contextual, mech mesp_scalar, proposed` |
| `sb_contextual_plmesp_proposed_revenue_per_round` | 0.5797 | `baseline_second_best_summary.csv` | `row setting contextual, mech plmesp, proposed` |
| `sb_contextual_plmesp_proposed_monitor_fire_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech plmesp, proposed` |
| `sb_contextual_plmesp_proposed_compliant_conviction_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech plmesp, proposed` |
| `sb_contextual_plmesp_proposed_undelegated_fraction` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech plmesp, proposed` |
| `sb_contextual_plmesp_proposed_price_above_cap_mass` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech plmesp, proposed` |
| `sb_contextual_second_best_proposed_revenue_per_round` | 0.6130 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, proposed` |
| `sb_contextual_second_best_proposed_monitor_fire_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, proposed` |
| `sb_contextual_second_best_proposed_compliant_conviction_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, proposed` |
| `sb_contextual_second_best_proposed_undelegated_fraction` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, proposed` |
| `sb_contextual_second_best_proposed_price_above_cap_mass` | 0.2363 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, proposed` |
| `sb_contextual_second_best_their_equilibrium_revenue_per_round` | 0.4889 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, their_equilibrium` |
| `sb_contextual_second_best_their_equilibrium_monitor_fire_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, their_equilibrium` |
| `sb_contextual_second_best_their_equilibrium_compliant_conviction_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, their_equilibrium` |
| `sb_contextual_second_best_their_equilibrium_undelegated_fraction` | 0.0000 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, their_equilibrium` |
| `sb_contextual_second_best_their_equilibrium_price_above_cap_mass` | 0.2363 | `baseline_second_best_summary.csv` | `row setting contextual, mech second_best, their_equilibrium` |
| `sb_scalar_mesp_scalar_proposed_revenue_per_round` | 0.5519 | `baseline_second_best_summary.csv` | `row setting scalar, mech mesp_scalar, proposed` |
| `sb_scalar_mesp_scalar_proposed_monitor_fire_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech mesp_scalar, proposed` |
| `sb_scalar_mesp_scalar_proposed_compliant_conviction_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech mesp_scalar, proposed` |
| `sb_scalar_mesp_scalar_proposed_undelegated_fraction` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech mesp_scalar, proposed` |
| `sb_scalar_mesp_scalar_proposed_price_above_cap_mass` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech mesp_scalar, proposed` |
| `sb_scalar_second_best_proposed_revenue_per_round` | 0.6056 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, proposed` |
| `sb_scalar_second_best_proposed_monitor_fire_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, proposed` |
| `sb_scalar_second_best_proposed_compliant_conviction_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, proposed` |
| `sb_scalar_second_best_proposed_undelegated_fraction` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, proposed` |
| `sb_scalar_second_best_proposed_price_above_cap_mass` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, proposed` |
| `sb_scalar_second_best_their_equilibrium_revenue_per_round` | 0.4490 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, their_equilibrium` |
| `sb_scalar_second_best_their_equilibrium_monitor_fire_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, their_equilibrium` |
| `sb_scalar_second_best_their_equilibrium_compliant_conviction_rate` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, their_equilibrium` |
| `sb_scalar_second_best_their_equilibrium_undelegated_fraction` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, their_equilibrium` |
| `sb_scalar_second_best_their_equilibrium_price_above_cap_mass` | 0.0000 | `baseline_second_best_summary.csv` | `row setting scalar, mech second_best, their_equilibrium` |
| `sbbait_contextual_mesp_scalar_detection_delay` | 44636.4184 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_mesp_scalar_post_fire_revenue_per_round` | 0.6773 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_mesp_scalar_undelegated_fraction` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_mesp_scalar_revenue_per_round` | 0.6114 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_mesp_scalar_detection_delay` | 44636.4184 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_mesp_scalar_post_fire_revenue_per_round` | 0.6773 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_mesp_scalar_undelegated_fraction` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_mesp_scalar_revenue_per_round` | 0.6114 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech mesp_scalar` |
| `sbbait_contextual_plmesp_detection_delay` | 4039.7769 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_plmesp_post_fire_revenue_per_round` | 0.6234 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_plmesp_undelegated_fraction` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_plmesp_revenue_per_round` | 0.6065 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_plmesp_detection_delay` | 1717.2532 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_plmesp_post_fire_revenue_per_round` | 0.6248 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_plmesp_undelegated_fraction` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_plmesp_revenue_per_round` | 0.6075 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech plmesp` |
| `sbbait_contextual_second_best_detection_delay` | 4483.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_contextual_second_best_post_fire_revenue_per_round` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_contextual_second_best_undelegated_fraction` | 0.1925 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_contextual_second_best_revenue_per_round` | 0.4968 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_contextual_second_best_detection_delay` | 4483.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_contextual_second_best_post_fire_revenue_per_round` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_contextual_second_best_undelegated_fraction` | 0.2652 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_contextual_second_best_revenue_per_round` | 0.4467 | `baseline_second_best_baitswitch.csv` | `row setting contextual, mech second_best` |
| `sbbait_scalar_mesp_scalar_detection_delay` | 14267.4323 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_mesp_scalar_post_fire_revenue_per_round` | 0.6872 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_mesp_scalar_undelegated_fraction` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_mesp_scalar_revenue_per_round` | 0.5892 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_mesp_scalar_detection_delay` | 14267.4323 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_mesp_scalar_post_fire_revenue_per_round` | 0.6872 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_mesp_scalar_undelegated_fraction` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_mesp_scalar_revenue_per_round` | 0.5892 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech mesp_scalar` |
| `sbbait_scalar_second_best_detection_delay` | 4754.8586 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `sbbait_scalar_second_best_post_fire_revenue_per_round` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `sbbait_scalar_second_best_undelegated_fraction` | 0.1885 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `sbbait_scalar_second_best_revenue_per_round` | 0.4891 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `sbbait_scalar_second_best_detection_delay` | 4754.8586 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `sbbait_scalar_second_best_post_fire_revenue_per_round` | 0.0000 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `sbbait_scalar_second_best_undelegated_fraction` | 0.2855 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `sbbait_scalar_second_best_revenue_per_round` | 0.4302 | `baseline_second_best_baitswitch.csv` | `row setting scalar, mech second_best` |
| `front_fc_a0.25_anytime_boundary_mult0.5` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 0.5}, false_conviction_rate` |
| `front_delay_a0.25_anytime_boundary_mult0.5` | 48.0 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 0.5}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.2_burnin100` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": 100}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.2_burnin100` | 100.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": 100}, median_delay_baitswitch` |
| `front_fc_a0.25_anytime_boundary_mult1.0` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 1.0}, false_conviction_rate` |
| `front_delay_a0.25_anytime_boundary_mult1.0` | 199.0 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 1.0}, median_delay_baitswitch` |
| `front_fc_a0.25_anytime_boundary_mult2.0` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 2.0}, false_conviction_rate` |
| `front_delay_a0.25_anytime_boundary_mult2.0` | 806.5 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 2.0}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.05_burnin1000` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": 1000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.05_burnin1000` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": 1000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.1_burnin1000` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": 1000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.1_burnin1000` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": 1000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.2_burnin1000` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": 1000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.2_burnin1000` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": 1000}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch1000_twosample_alpha1e-06` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 1000, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch1000_twosample_alpha1e-06` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 1000, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.02_burnin10000` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": 10000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.02_burnin10000` | 10000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": 10000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.05_burnin10000` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": 10000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.05_burnin10000` | 10000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": 10000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.1_burnin10000` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": 10000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.1_burnin10000` | 10000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": 10000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.2_burnin10000` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": 10000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.2_burnin10000` | 10000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": 10000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.02_burninnull` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": null}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.02_burninnull` | 12819.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": null}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.05_burninnull` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": null}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.05_burninnull` | 12819.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": null}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.1_burninnull` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": null}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.1_burninnull` | 12819.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": null}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.2_burninnull` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": null}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.2_burninnull` | 12819.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.2, "burnin": null}, median_delay_baitswitch` |
| `front_fc_a0.25_none_` | 0.0000 | `monitor_frontier.csv` | `alpha a0.25, none {}, false_conviction_rate` |
| `front_fc_a0.25_twosample_batch200_twosample_alpha1e-06` | 0.0033 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 200, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch200_twosample_alpha1e-06` | 200.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 200, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.01_burninnull` | 0.0150 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": null}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.01_burninnull` | 12819.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": null}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch50_twosample_alpha1e-06` | 0.0233 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 50, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch50_twosample_alpha1e-06` | 150.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 50, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch1000_twosample_alpha0.0001` | 0.0233 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 1000, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch1000_twosample_alpha0.0001` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 1000, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.1_burnin100` | 0.0250 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": 100}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.1_burnin100` | 100.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.1, "burnin": 100}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.01_burnin10000` | 0.0300 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": 10000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.01_burnin10000` | 10000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": 10000}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch200_twosample_alpha0.0001` | 0.1333 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 200, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch200_twosample_alpha0.0001` | 200.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 200, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.25_anytime_boundary_mult0.25` | 0.1800 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 0.25}, false_conviction_rate` |
| `front_delay_a0.25_anytime_boundary_mult0.25` | 10.0 | `monitor_frontier.csv` | `alpha a0.25, anytime {"boundary_mult": 0.25}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.02_burnin1000` | 0.2150 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": 1000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.02_burnin1000` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": 1000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.005_burninnull` | 0.2750 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": null}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.005_burninnull` | 12819.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": null}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.005_burnin10000` | 0.3400 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": 10000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.005_burnin10000` | 10000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": 10000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.05_burnin100` | 0.3650 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": 100}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.05_burnin100` | 100.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.05, "burnin": 100}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.01_burnin1000` | 0.5550 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": 1000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.01_burnin1000` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": 1000}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch50_twosample_alpha0.0001` | 0.6900 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 50, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch50_twosample_alpha0.0001` | 50.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 50, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.02_burnin100` | 0.7200 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": 100}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.02_burnin100` | 100.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.02, "burnin": 100}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.005_burnin1000` | 0.7800 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": 1000}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.005_burnin1000` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": 1000}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.01_burnin100` | 0.8800 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": 100}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.01_burnin100` | 100.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.01, "burnin": 100}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch1000_twosample_alpha0.01` | 0.9300 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 1000, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch1000_twosample_alpha0.01` | 1000.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 1000, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.25_fixedbuffer_buffer0.005_burnin100` | 0.9600 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": 100}, false_conviction_rate` |
| `front_delay_a0.25_fixedbuffer_buffer0.005_burnin100` | 100.0 | `monitor_frontier.csv` | `alpha a0.25, fixedbuffer {"buffer": 0.005, "burnin": 100}, median_delay_baitswitch` |
| `front_fc_a0.25_anytime_noslack_` | 1.0000 | `monitor_frontier.csv` | `alpha a0.25, anytime_noslack {}, false_conviction_rate` |
| `front_delay_a0.25_anytime_noslack_` | 1.0 | `monitor_frontier.csv` | `alpha a0.25, anytime_noslack {}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch50_twosample_alpha0.01` | 1.0000 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 50, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch50_twosample_alpha0.01` | 50.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 50, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_batch200_twosample_alpha0.01` | 1.0000 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 200, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.25_twosample_batch200_twosample_alpha0.01` | 200.0 | `monitor_frontier.csv` | `alpha a0.25, twosample {"batch": 200, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.25_twosample_elicit_batch200_twosample_alpha0.0001` | 1.0000 | `monitor_frontier.csv` | `alpha a0.25, twosample_elicit {"batch": 200, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.25_twosample_elicit_batch200_twosample_alpha0.0001` | 200.0 | `monitor_frontier.csv` | `alpha a0.25, twosample_elicit {"batch": 200, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.50_anytime_boundary_mult0.5` | 0.0000 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 0.5}, false_conviction_rate` |
| `front_delay_a0.50_anytime_boundary_mult0.5` | 162.0 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 0.5}, median_delay_baitswitch` |
| `front_fc_a0.50_anytime_boundary_mult1.0` | 0.0000 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 1.0}, false_conviction_rate` |
| `front_delay_a0.50_anytime_boundary_mult1.0` | 709.0 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 1.0}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch1000_twosample_alpha1e-06` | 0.0000 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 1000, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch1000_twosample_alpha1e-06` | 1000.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 1000, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.50_anytime_boundary_mult2.0` | 0.0000 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 2.0}, false_conviction_rate` |
| `front_delay_a0.50_anytime_boundary_mult2.0` | 2905.5 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 2.0}, median_delay_baitswitch` |
| `front_fc_a0.50_none_` | 0.0000 | `monitor_frontier.csv` | `alpha a0.50, none {}, false_conviction_rate` |
| `front_fc_a0.50_twosample_batch200_twosample_alpha1e-06` | 0.0033 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 200, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch200_twosample_alpha1e-06` | 800.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 200, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch1000_twosample_alpha0.0001` | 0.0233 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 1000, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch1000_twosample_alpha0.0001` | 1000.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 1000, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch50_twosample_alpha1e-06` | 0.0233 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 50, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch50_twosample_alpha1e-06` | 6300.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 50, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch200_twosample_alpha0.0001` | 0.1333 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 200, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch200_twosample_alpha0.0001` | 200.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 200, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.50_anytime_boundary_mult0.25` | 0.1800 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 0.25}, false_conviction_rate` |
| `front_delay_a0.50_anytime_boundary_mult0.25` | 31.0 | `monitor_frontier.csv` | `alpha a0.50, anytime {"boundary_mult": 0.25}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch50_twosample_alpha0.0001` | 0.6900 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 50, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch50_twosample_alpha0.0001` | 650.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 50, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch1000_twosample_alpha0.01` | 0.9300 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 1000, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch1000_twosample_alpha0.01` | 1000.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 1000, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.50_anytime_noslack_` | 1.0000 | `monitor_frontier.csv` | `alpha a0.50, anytime_noslack {}, false_conviction_rate` |
| `front_delay_a0.50_anytime_noslack_` | 1.0 | `monitor_frontier.csv` | `alpha a0.50, anytime_noslack {}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch50_twosample_alpha0.01` | 1.0000 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 50, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch50_twosample_alpha0.01` | 100.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 50, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_batch200_twosample_alpha0.01` | 1.0000 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 200, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.50_twosample_batch200_twosample_alpha0.01` | 200.0 | `monitor_frontier.csv` | `alpha a0.50, twosample {"batch": 200, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.50_twosample_elicit_batch200_twosample_alpha0.0001` | 1.0000 | `monitor_frontier.csv` | `alpha a0.50, twosample_elicit {"batch": 200, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.50_twosample_elicit_batch200_twosample_alpha0.0001` | 200.0 | `monitor_frontier.csv` | `alpha a0.50, twosample_elicit {"batch": 200, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.75_anytime_boundary_mult0.5` | 0.0000 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 0.5}, false_conviction_rate` |
| `front_delay_a0.75_anytime_boundary_mult0.5` | 14354.0 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 0.5}, median_delay_baitswitch` |
| `front_fc_a0.75_anytime_boundary_mult1.0` | 0.0000 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 1.0}, false_conviction_rate` |
| `front_delay_a0.75_anytime_boundary_mult1.0` | 63509.0 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 1.0}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch1000_twosample_alpha1e-06` | 0.0000 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 1000, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch1000_twosample_alpha1e-06` | 137000.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 1000, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.75_anytime_boundary_mult2.0` | 0.0000 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 2.0}, false_conviction_rate` |
| `front_delay_a0.75_anytime_boundary_mult2.0` | 189461.0 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 2.0}, median_delay_baitswitch` |
| `front_fc_a0.75_none_` | 0.0000 | `monitor_frontier.csv` | `alpha a0.75, none {}, false_conviction_rate` |
| `front_fc_a0.75_twosample_batch200_twosample_alpha1e-06` | 0.0033 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 200, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch200_twosample_alpha1e-06` | 98800.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 200, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch1000_twosample_alpha0.0001` | 0.0233 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 1000, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch1000_twosample_alpha0.0001` | 99000.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 1000, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch50_twosample_alpha1e-06` | 0.0233 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 50, "twosample_alpha": 1e-06}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch50_twosample_alpha1e-06` | 108850.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 50, "twosample_alpha": 1e-06}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch200_twosample_alpha0.0001` | 0.1333 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 200, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch200_twosample_alpha0.0001` | 124400.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 200, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.75_anytime_boundary_mult0.25` | 0.1800 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 0.25}, false_conviction_rate` |
| `front_delay_a0.75_anytime_boundary_mult0.25` | 2344.5 | `monitor_frontier.csv` | `alpha a0.75, anytime {"boundary_mult": 0.25}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch50_twosample_alpha0.0001` | 0.6900 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 50, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch50_twosample_alpha0.0001` | 52925.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 50, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch1000_twosample_alpha0.01` | 0.9300 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 1000, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch1000_twosample_alpha0.01` | 8500.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 1000, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.75_anytime_noslack_` | 1.0000 | `monitor_frontier.csv` | `alpha a0.75, anytime_noslack {}, false_conviction_rate` |
| `front_delay_a0.75_anytime_noslack_` | 1.0 | `monitor_frontier.csv` | `alpha a0.75, anytime_noslack {}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_elicit_batch200_twosample_alpha0.0001` | 1.0000 | `monitor_frontier.csv` | `alpha a0.75, twosample_elicit {"batch": 200, "twosample_alpha": 0.0001}, false_conviction_rate` |
| `front_delay_a0.75_twosample_elicit_batch200_twosample_alpha0.0001` | 200.0 | `monitor_frontier.csv` | `alpha a0.75, twosample_elicit {"batch": 200, "twosample_alpha": 0.0001}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch50_twosample_alpha0.01` | 1.0000 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 50, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch50_twosample_alpha0.01` | 1900.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 50, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `front_fc_a0.75_twosample_batch200_twosample_alpha0.01` | 1.0000 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 200, "twosample_alpha": 0.01}, false_conviction_rate` |
| `front_delay_a0.75_twosample_batch200_twosample_alpha0.01` | 6400.0 | `monitor_frontier.csv` | `alpha a0.75, twosample {"batch": 200, "twosample_alpha": 0.01}, median_delay_baitswitch` |
| `ladder_falseconv_anytime_boundary_mult:0.25` | 0.1800 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 0.25}, compliant` |
| `ladder_delay_anytime_boundary_mult:0.25` | 31.0 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 0.25}, baitswitch` |
| `ladder_falseconv_anytime_boundary_mult:0.5` | 0.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 0.5}, compliant` |
| `ladder_delay_anytime_boundary_mult:0.5` | 162.0 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 0.5}, baitswitch` |
| `ladder_falseconv_anytime_boundary_mult:1.0` | 0.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 1.0}, compliant` |
| `ladder_delay_anytime_boundary_mult:1.0` | 709.0 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 1.0}, baitswitch` |
| `ladder_falseconv_anytime_boundary_mult:2.0` | 0.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 2.0}, compliant` |
| `ladder_delay_anytime_boundary_mult:2.0` | 2905.5 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime, params {"boundary_mult": 2.0}, baitswitch` |
| `ladder_falseconv_anytime_noslack_` | 1.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime_noslack, params {}, compliant` |
| `ladder_delay_anytime_noslack_` | 1.0 | `monitor_ladder.csv` | `alpha a0.50, monitor anytime_noslack, params {}, baitswitch` |
| `ladder_falseconv_none_` | 0.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor none, params {}, compliant` |
| `ladder_delay_none_` | nan | `monitor_ladder.csv` | `alpha a0.50, monitor none, params {}, baitswitch` |
| `ladder_falseconv_twosample_batch:1000,twosample_alpha:0.0001` | 0.0233 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 1000, "twosample_alpha": 0.0001}, compliant` |
| `ladder_delay_twosample_batch:1000,twosample_alpha:0.0001` | 1000.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 1000, "twosample_alpha": 0.0001}, baitswitch` |
| `ladder_falseconv_twosample_batch:1000,twosample_alpha:0.01` | 0.9300 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 1000, "twosample_alpha": 0.01}, compliant` |
| `ladder_delay_twosample_batch:1000,twosample_alpha:0.01` | 1000.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 1000, "twosample_alpha": 0.01}, baitswitch` |
| `ladder_falseconv_twosample_batch:1000,twosample_alpha:1e-06` | 0.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 1000, "twosample_alpha": 1e-06}, compliant` |
| `ladder_delay_twosample_batch:1000,twosample_alpha:1e-06` | 1000.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 1000, "twosample_alpha": 1e-06}, baitswitch` |
| `ladder_falseconv_twosample_batch:200,twosample_alpha:0.0001` | 0.1333 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 200, "twosample_alpha": 0.0001}, compliant` |
| `ladder_delay_twosample_batch:200,twosample_alpha:0.0001` | 200.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 200, "twosample_alpha": 0.0001}, baitswitch` |
| `ladder_falseconv_twosample_batch:200,twosample_alpha:0.01` | 1.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 200, "twosample_alpha": 0.01}, compliant` |
| `ladder_delay_twosample_batch:200,twosample_alpha:0.01` | 200.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 200, "twosample_alpha": 0.01}, baitswitch` |
| `ladder_falseconv_twosample_batch:200,twosample_alpha:1e-06` | 0.0033 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 200, "twosample_alpha": 1e-06}, compliant` |
| `ladder_delay_twosample_batch:200,twosample_alpha:1e-06` | 800.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 200, "twosample_alpha": 1e-06}, baitswitch` |
| `ladder_falseconv_twosample_batch:50,twosample_alpha:0.0001` | 0.6900 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 50, "twosample_alpha": 0.0001}, compliant` |
| `ladder_delay_twosample_batch:50,twosample_alpha:0.0001` | 650.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 50, "twosample_alpha": 0.0001}, baitswitch` |
| `ladder_falseconv_twosample_batch:50,twosample_alpha:0.01` | 1.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 50, "twosample_alpha": 0.01}, compliant` |
| `ladder_delay_twosample_batch:50,twosample_alpha:0.01` | 100.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 50, "twosample_alpha": 0.01}, baitswitch` |
| `ladder_falseconv_twosample_batch:50,twosample_alpha:1e-06` | 0.0233 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 50, "twosample_alpha": 1e-06}, compliant` |
| `ladder_delay_twosample_batch:50,twosample_alpha:1e-06` | 6300.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample, params {"batch": 50, "twosample_alpha": 1e-06}, baitswitch` |
| `ladder_falseconv_twosample_elicit_batch:200,twosample_alpha:0.0001` | 1.0000 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample_elicit, params {"batch": 200, "twosample_alpha": 0.0001}, compliant` |
| `ladder_delay_twosample_elicit_batch:200,twosample_alpha:0.0001` | 200.0 | `monitor_ladder.csv` | `alpha a0.50, monitor twosample_elicit, params {"batch": 200, "twosample_alpha": 0.0001}, baitswitch` |

## 1. Provenance row counts

| shot   |   rows_published |   rows_after_dedup |   rows_after_dropna |   rows_unassigned_family |   rows_used |   outcomes_used |
|:-------|-----------------:|-------------------:|--------------------:|-------------------------:|------------:|----------------:|
| 0shot  |            36497 |              36497 |               36497 |                     1719 |       34778 |          382558 |
| 5shot  |            36511 |              36497 |               36483 |                     1719 |       34764 |          382404 |

## 2. Check against RouterBench Table 1 (max abs difference)

| context    |   max_abs_diff |
|:-----------|---------------:|
| ARC        |         0.0426 |
| GSM8K      |         0.006  |
| HellaSwag  |         0.1071 |
| MBPP       |         0.0702 |
| MMLU       |         0.0672 |
| MT-Bench   |         0.2942 |
| Winogrande |         0.0322 |

## 3. Measured capability M_i(z), 5-shot (STEP 2a: the table the brief asks for)

| model             |   MMLU |   HellaSwag |   GSM8K |   Winogrande |   ARC |   MBPP |   MT-Bench |
|:------------------|-------:|------------:|--------:|-------------:|------:|-------:|-----------:|
| Claude-Instant-V1 |  0.451 |       0.767 |   0.627 |        0.517 | 0.829 |  0.604 |      0.629 |
| Claude-V1         |  0.53  |       0.818 |   0.651 |        0.562 | 0.909 |  0.597 |      0.649 |
| Claude-V2         |  0.573 |       0.314 |   0.663 |        0.478 | 0.589 |  0.642 |      0.675 |
| CodeLlama-34B     |  0.523 |       0.513 |   0.457 |        0.585 | 0.663 |  0.518 |      0.528 |
| GPT-3.5           |  0.671 |       0.789 |   0.605 |        0.641 | 0.834 |  0.653 |      0.689 |
| GPT-4             |  0.825 |       0.902 |   0.659 |        0.859 | 0.954 |  0.686 |      0.806 |
| Llama-70B         |  0.607 |       0.709 |   0.523 |        0.503 | 0.803 |  0.33  |      0.586 |
| Mistral-7B        |  0.523 |       0.537 |   0.412 |        0.566 | 0.671 |  0.344 |      0.524 |
| Mixtral-8x7B      |  0.693 |       0.693 |   0.519 |        0.679 | 0.854 |  0.541 |      0.648 |
| WizardLM-13B      |  0.531 |       0.599 |   0.506 |        0.529 | 0.658 |  0.37  |      0.545 |
| Yi-34B            |  0.724 |       0.875 |   0.548 |        0.754 | 0.903 |  0.386 |      0.644 |


Best model per context: MMLU: GPT-4, HellaSwag: GPT-4, GSM8K: Claude-V2, Winogrande: GPT-4, ARC: GPT-4, MBPP: GPT-4, MT-Bench: GPT-4.


Arrival mass of each context (empirical, from the row counts):

| context    |    mass |   n_queries |
|:-----------|--------:|------------:|
| MMLU       | 0.40392 |       14042 |
| HellaSwag  | 0.28886 |       10042 |
| GSM8K      | 0.2143  |        7450 |
| Winogrande | 0.03645 |        1267 |
| ARC        | 0.04188 |        1456 |
| MBPP       | 0.01228 |         427 |
| MT-Bench   | 0.0023  |          80 |

## 4. Rank-flip rates, 5shot

|                                   | value               |
|:----------------------------------|:--------------------|
| raw_flip_rate                     | 0.3012987012987013  |
| raw_comparisons                   | 1155                |
| raw_flips                         | 348                 |
| sig_flip_rate                     | 0.2470308788598574  |
| sig_comparisons                   | 842                 |
| sig_flips                         | 208                 |
| bonf_flip_rate                    | 0.2372322899505766  |
| bonf_comparisons                  | 607                 |
| bonf_flips                        | 144                 |
| n_distinct_best_models            | 2                   |
| ctx_pairs_with_different_best     | 6                   |
| ctx_pairs_total                   | 21                  |
| frac_ctx_pairs_different_best     | 0.2857142857142857  |
| mean_kendall_tau_between_contexts | 0.3974025974025974  |
| min_kendall_tau_between_contexts  | -0.0545454545454545 |
| shot                              | 5shot               |
| n_models                          | 11                  |
| n_contexts                        | 7                   |

## 4. Rank-flip rates, 0shot

|                                   | value              |
|:----------------------------------|:-------------------|
| raw_flip_rate                     | 0.1749347258485639 |
| raw_comparisons                   | 1149               |
| raw_flips                         | 201                |
| sig_flip_rate                     | 0.1040462427745664 |
| sig_comparisons                   | 865                |
| sig_flips                         | 90                 |
| bonf_flip_rate                    | 0.0919540229885057 |
| bonf_comparisons                  | 609                |
| bonf_flips                        | 56                 |
| n_distinct_best_models            | 2                  |
| ctx_pairs_with_different_best     | 6                  |
| ctx_pairs_total                   | 21                 |
| frac_ctx_pairs_different_best     | 0.2857142857142857 |
| mean_kendall_tau_between_contexts | 0.6485726639925622 |
| min_kendall_tau_between_contexts  | 0.4770842982214229 |
| shot                              | 0shot              |
| n_models                          | 11                 |
| n_contexts                        | 7                  |

## 5. Continuous contexts (STEP 2b)

|   d |   k |   n_cells |   b |      n |   raw_flip_rate |   n_cell_pairs_compared |   n_distinct_best_cell |   frac_cells_best_differs_from_global |   frac_queries_best_differs_from_global |   mean_pointwise_max |   mean_pointwise_second |   global_max_mean |   global_second_mean |   median_cell_size |   min_cell_size |
|----:|----:|----------:|----:|-------:|----------------:|------------------------:|-----------------------:|--------------------------------------:|----------------------------------------:|---------------------:|------------------------:|------------------:|---------------------:|-------------------:|----------------:|
|   1 |  50 |        24 |  24 | 300000 |          0.1772 |         15180           |                      2 |                                0.125  |                                  0.2211 |               0.8227 |                  0.7646 |            0.8167 |               0.7343 |             1448.5 |            1448 |
|   1 | 200 |        24 |  24 | 300000 |          0.1771 |         15180           |                      2 |                                0.125  |                                  0.149  |               0.8189 |                  0.7593 |            0.8167 |               0.7344 |             1448.5 |            1448 |
|   1 | 800 |        24 |  24 | 300000 |          0.1728 |         15180           |                      2 |                                0.125  |                                  0.1478 |               0.8188 |                  0.7581 |            0.817  |               0.7351 |             1448.5 |            1448 |
|   2 |  50 |       129 |  13 | 300000 |          0.2159 |        453696           |                      4 |                                0.0775 |                                  0.2635 |               0.8244 |                  0.7699 |            0.8167 |               0.7341 |              235   |               2 |
|   2 | 200 |       129 |  13 | 300000 |          0.207  |        454080           |                      4 |                                0.062  |                                  0.2037 |               0.82   |                  0.7628 |            0.8167 |               0.7341 |              235   |               2 |
|   2 | 800 |       129 |  13 | 300000 |          0.1987 |        454080           |                      4 |                                0.062  |                                  0.1756 |               0.8192 |                  0.7602 |            0.8171 |               0.7353 |              235   |               2 |
|   3 |  50 |       415 |   9 | 300000 |          0.2254 |             4.66588e+06 |                      6 |                                0.1639 |                                  0.3074 |               0.8254 |                  0.77   |            0.8157 |               0.7327 |               44   |               1 |
|   3 | 200 |       415 |   9 | 300000 |          0.2144 |             4.71362e+06 |                      4 |                                0.1759 |                                  0.2755 |               0.8218 |                  0.7619 |            0.816  |               0.7323 |               44   |               1 |
|   3 | 800 |       415 |   9 | 300000 |          0.2022 |             4.72229e+06 |                      4 |                                0.1807 |                                  0.2899 |               0.821  |                  0.7583 |            0.8162 |               0.7334 |               44   |               1 |


Embedding diagnostic (how much of the benchmark family the TF-IDF/LSA cells recover):

|   d |   n_cells |   cell_family_purity |   normalised_mutual_info_cell_family |
|----:|----------:|---------------------:|-------------------------------------:|
|   1 |        24 |               0.6328 |                               0.446  |
|   2 |       129 |               0.8909 |                               0.7754 |
|   3 |       415 |               0.9266 |                               0.8553 |

## 6. Analytic scalar-vs-contextual gap, all 165 triples

| context_set   | uniform_mass   |   n_triples |   spearman_rho |   spearman_p |   pearson_r |   pearson_p |   ols_slope |   ols_intercept |   ols_r2 |   gap_at_flip0_mean |   gap_max |   gap_mean |   frac_triples_gap_above_0.01 |   mean_scalar_mass_price_above_capability |   frac_triples_scalar_price_infeasible_somewhere |   spearman_flip_vs_infeasible_mass |
|:--------------|:---------------|------------:|---------------:|-------------:|------------:|------------:|------------:|----------------:|---------:|--------------------:|----------:|-----------:|------------------------------:|------------------------------------------:|-------------------------------------------------:|-----------------------------------:|
| Q3            | False          |         165 |        0.56466 |            0 |     0.51163 |           0 |     0.05171 |         0.00641 |  0.26177 |             0.00747 |   0.07122 |    0.02271 |                       0.61818 |                                   0.18224 |                                          0.67273 |                            0.23127 |
| Q3            | True           |         165 |        0.57476 |            0 |     0.56516 |           0 |     0.05565 |         0.00755 |  0.3194  |             0.00904 |   0.07736 |    0.02508 |                       0.64848 |                                   0.24646 |                                          0.73939 |                            0.16219 |
| Q7            | False          |         165 |        0.43671 |            0 |     0.40405 |           0 |     0.05545 |         0.0069  |  0.16326 |             0.0084  |   0.07178 |    0.02361 |                       0.66667 |                                   0.19587 |                                          0.77576 |                            0.45823 |
| Q7            | True           |         165 |        0.47824 |            0 |     0.47937 |           0 |     0.06301 |         0.00733 |  0.2298  |             0.00451 |   0.0827  |    0.02631 |                       0.72121 |                                   0.29351 |                                          0.84848 |                            0.43646 |

## 7. SIMULATED gap at n = 300,000, all 165 triples

| context_set   |   n_triples |   spearman_rho_flip_vs_simgap |   spearman_p |   ols_slope |   ols_intercept |   ols_r2 |   spearman_analytic_vs_sim |   mean_sim_gap |   mean_analytic_gap |   max_sim_gap |   min_sim_gap |   frac_sim_gap_positive |
|:--------------|------------:|------------------------------:|-------------:|------------:|----------------:|---------:|---------------------------:|---------------:|--------------------:|--------------:|--------------:|------------------------:|
| Q3            |         165 |                       0.13392 |      0.08636 |     0.00536 |         0.00675 |  0.00123 |                    0.47837 |        0.00844 |             0.02271 |       0.07408 |      -0.07614 |                 0.71515 |
| Q7            |         165 |                      -0.04734 |      0.54594 |    -0.02616 |         0.0189  |  0.01217 |                    0.37421 |        0.01102 |             0.02361 |       0.07467 |      -0.07371 |                 0.70909 |

## 7b. The paper's two-top condition, measured

| context_set   |   K |   n_subsets |   mean_top_gap |   best_subset_min_mean_top_gap |   mean_mass_within_0.0 |   best_subset_mass_within_0.0 |   frac_subsets_mass_within_0.0_above_0.9 |   mean_mass_within_0.002 |   best_subset_mass_within_0.002 |   frac_subsets_mass_within_0.002_above_0.9 |   mean_mass_within_0.005 |   best_subset_mass_within_0.005 |   frac_subsets_mass_within_0.005_above_0.9 |   mean_mass_within_0.01 |   best_subset_mass_within_0.01 |   frac_subsets_mass_within_0.01_above_0.9 |   mean_mass_within_0.02 |   best_subset_mass_within_0.02 |   frac_subsets_mass_within_0.02_above_0.9 |   mean_mass_within_0.03 |   best_subset_mass_within_0.03 |   frac_subsets_mass_within_0.03_above_0.9 |   mean_mass_within_0.05 |   best_subset_mass_within_0.05 |   frac_subsets_mass_within_0.05_above_0.9 |   mean_mass_within_0.075 |   best_subset_mass_within_0.075 |   frac_subsets_mass_within_0.075_above_0.9 |   mean_mass_within_0.1 |   best_subset_mass_within_0.1 |   frac_subsets_mass_within_0.1_above_0.9 |   mean_mass_within_0.15 |   best_subset_mass_within_0.15 |   frac_subsets_mass_within_0.15_above_0.9 |   mean_mass_within_0.2 |   best_subset_mass_within_0.2 |   frac_subsets_mass_within_0.2_above_0.9 |
|:--------------|----:|------------:|---------------:|-------------------------------:|-----------------------:|------------------------------:|-----------------------------------------:|-------------------------:|--------------------------------:|-------------------------------------------:|-------------------------:|--------------------------------:|-------------------------------------------:|------------------------:|-------------------------------:|------------------------------------------:|------------------------:|-------------------------------:|------------------------------------------:|------------------------:|-------------------------------:|------------------------------------------:|------------------------:|-------------------------------:|------------------------------------------:|-------------------------:|--------------------------------:|-------------------------------------------:|-----------------------:|------------------------------:|-----------------------------------------:|------------------------:|-------------------------------:|------------------------------------------:|-----------------------:|------------------------------:|-----------------------------------------:|
| Q3            |   2 |          55 |         0.1473 |                         0.0185 |                      0 |                             0 |                                        0 |                   0.0162 |                          0.4453 |                                          0 |                   0.0248 |                          0.4453 |                                          0 |                  0.0615 |                         0.4453 |                                         0 |                  0.0801 |                         0.5547 |                                         0 |                  0.1286 |                         0.7637 |                                    0      |                  0.1948 |                         1      |                                    0.0182 |                   0.2857 |                          1      |                                     0.0182 |                 0.411  |                        1      |                                   0.1455 |                  0.5917 |                              1 |                                    0.2182 |                 0.7439 |                             1 |                                   0.4545 |
| Q3            |   3 |         165 |         0.108  |                         0.022  |                      0 |                             0 |                                        0 |                   0.0108 |                          0.4453 |                                          0 |                   0.028  |                          0.4453 |                                          0 |                  0.0556 |                         0.4453 |                                         0 |                  0.0805 |                         0.5547 |                                         0 |                  0.1724 |                         1      |                                    0.0061 |                  0.2647 |                         1      |                                    0.0121 |                   0.378  |                          1      |                                     0.0667 |                 0.5102 |                        1      |                                   0.2    |                  0.7413 |                              1 |                                    0.4364 |                 0.8783 |                             1 |                                   0.7212 |
| Q3            |   4 |         330 |         0.0899 |                         0.0214 |                      0 |                             0 |                                        0 |                   0.004  |                          0.4453 |                                          0 |                   0.032  |                          0.4453 |                                          0 |                  0.0547 |                         0.4453 |                                         0 |                  0.082  |                         0.5547 |                                         0 |                  0.212  |                         1      |                                    0.0182 |                  0.3183 |                         1      |                                    0.0333 |                   0.4534 |                          1      |                                     0.1182 |                 0.5806 |                        1      |                                   0.2758 |                  0.8304 |                              1 |                                    0.6152 |                 0.9321 |                             1 |                                   0.8424 |
| Q3            |   5 |         462 |         0.0769 |                         0.0214 |                      0 |                             0 |                                        0 |                   0.001  |                          0.4453 |                                          0 |                   0.0444 |                          0.4453 |                                          0 |                  0.0731 |                         0.4453 |                                         0 |                  0.1045 |                         0.5547 |                                         0 |                  0.2647 |                         1      |                                    0.0325 |                  0.3791 |                         1      |                                    0.0541 |                   0.5198 |                          1      |                                     0.1753 |                 0.6342 |                        1      |                                   0.3247 |                  0.8905 |                              1 |                                    0.7468 |                 0.9614 |                             1 |                                   0.9113 |
| Q3            |   6 |         462 |         0.068  |                         0.0214 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.0644 |                          0.2363 |                                          0 |                  0.1002 |                         0.2363 |                                         0 |                  0.1367 |                         0.3184 |                                         0 |                  0.3178 |                         1      |                                    0.0433 |                  0.4346 |                         1      |                                    0.0649 |                   0.5634 |                          1      |                                     0.2165 |                 0.6632 |                        1      |                                   0.3377 |                  0.931  |                              1 |                                    0.8398 |                 0.9791 |                             1 |                                   0.9524 |
| Q3            |   7 |         330 |         0.0624 |                         0.0214 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.0902 |                          0.2363 |                                          0 |                  0.1303 |                         0.2363 |                                         0 |                  0.1704 |                         0.2363 |                                         0 |                  0.3657 |                         1      |                                    0.0455 |                  0.477  |                         1      |                                    0.0606 |                   0.5835 |                          1      |                                     0.2303 |                 0.6689 |                        1      |                                   0.3152 |                  0.9589 |                              1 |                                    0.9061 |                 0.9906 |                             1 |                                   0.9788 |
| Q3            |   8 |         165 |         0.059  |                         0.0214 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.1203 |                          0.2363 |                                          0 |                  0.1604 |                         0.2363 |                                         0 |                  0.2005 |                         0.2363 |                                         0 |                  0.4084 |                         1      |                                    0.0364 |                  0.5054 |                         1      |                                    0.0424 |                   0.5858 |                          1      |                                     0.2121 |                 0.6561 |                        1      |                                   0.2606 |                  0.9784 |                              1 |                                    0.9515 |                 0.9973 |                             1 |                                   0.9939 |
| Q3            |   9 |          55 |         0.0571 |                         0.0214 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.1546 |                          0.2363 |                                          0 |                  0.189  |                         0.2363 |                                         0 |                  0.2234 |                         0.2363 |                                         0 |                  0.45   |                         1      |                                    0.0182 |                  0.5233 |                         1      |                                    0.0182 |                   0.5778 |                          1      |                                     0.1636 |                 0.6299 |                        1      |                                   0.1818 |                  0.9919 |                              1 |                                    0.9818 |                 1      |                             1 |                                   1      |
| Q3            |  10 |          11 |         0.0557 |                         0.0351 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.1933 |                          0.2363 |                                          0 |                  0.2148 |                         0.2363 |                                         0 |                  0.2363 |                         0.2363 |                                         0 |                  0.4968 |                         0.5547 |                                    0      |                  0.5373 |                         0.6816 |                                    0      |                   0.5662 |                          1      |                                     0.0909 |                 0.5952 |                        1      |                                   0.0909 |                  1      |                              1 |                                    1      |                 1      |                             1 |                                   1      |
| Q3            |  11 |           1 |         0.0545 |                         0.0545 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.2363 |                          0.2363 |                                          0 |                  0.2363 |                         0.2363 |                                         0 |                  0.2363 |                         0.2363 |                                         0 |                  0.5547 |                         0.5547 |                                    0      |                  0.5547 |                         0.5547 |                                    0      |                   0.5547 |                          0.5547 |                                     0      |                 0.5547 |                        0.5547 |                                   0      |                  1      |                              1 |                                    1      |                 1      |                             1 |                                   1      |
| Q7            |   2 |          55 |         0.1466 |                         0.0199 |                      0 |                             0 |                                        0 |                   0.0147 |                          0.4039 |                                          0 |                   0.0233 |                          0.4062 |                                          0 |                  0.0599 |                         0.4481 |                                         0 |                  0.0812 |                         0.5032 |                                         0 |                  0.1292 |                         0.7734 |                                    0      |                  0.1974 |                         0.9877 |                                    0.0182 |                   0.2924 |                          0.9877 |                                     0.0182 |                 0.4127 |                        1      |                                   0.1455 |                  0.5901 |                              1 |                                    0.2182 |                 0.742  |                             1 |                                   0.4545 |
| Q7            |   3 |         165 |         0.1082 |                         0.0229 |                      0 |                             0 |                                        0 |                   0.0099 |                          0.4039 |                                          0 |                   0.0265 |                          0.4404 |                                          0 |                  0.0561 |                         0.4527 |                                         0 |                  0.0832 |                         0.5032 |                                         0 |                  0.1706 |                         0.949  |                                    0.0061 |                  0.2664 |                         1      |                                    0.0121 |                   0.3854 |                          1      |                                     0.0667 |                 0.5124 |                        1      |                                   0.2    |                  0.7385 |                              1 |                                    0.4364 |                 0.8752 |                             1 |                                   0.7212 |
| Q7            |   4 |         330 |         0.0902 |                         0.0229 |                      0 |                             0 |                                        0 |                   0.0038 |                          0.4039 |                                          0 |                   0.0299 |                          0.4404 |                                          0 |                  0.056  |                         0.4527 |                                         0 |                  0.0853 |                         0.5032 |                                         0 |                  0.2064 |                         0.949  |                                    0.0182 |                  0.319  |                         1      |                                    0.0333 |                   0.4613 |                          1      |                                     0.1182 |                 0.5847 |                        1      |                                   0.2758 |                  0.8276 |                              1 |                                    0.6152 |                 0.9295 |                             1 |                                   0.8424 |
| Q7            |   5 |         462 |         0.0775 |                         0.0229 |                      0 |                             0 |                                        0 |                   0.001  |                          0.4039 |                                          0 |                   0.0408 |                          0.4039 |                                          0 |                  0.0733 |                         0.4162 |                                         0 |                  0.1062 |                         0.5032 |                                         0 |                  0.2535 |                         0.949  |                                    0.0325 |                  0.3779 |                         1      |                                    0.0541 |                   0.5266 |                          1      |                                     0.1753 |                 0.6381 |                        1      |                                   0.3247 |                  0.8865 |                              1 |                                    0.7468 |                 0.959  |                             1 |                                   0.9113 |
| Q7            |   6 |         462 |         0.069  |                         0.0229 |                      0 |                             0 |                                        0 |                   0.0001 |                          0.0023 |                                          0 |                   0.0586 |                          0.2143 |                                          0 |                  0.0983 |                         0.2143 |                                         0 |                  0.1354 |                         0.2889 |                                         0 |                  0.3006 |                         0.949  |                                    0.0433 |                  0.4317 |                         1      |                                    0.0649 |                   0.5691 |                          1      |                                     0.2165 |                 0.6659 |                        1      |                                   0.3377 |                  0.9254 |                              1 |                                    0.8398 |                 0.9766 |                             1 |                                   0.9524 |
| Q7            |   7 |         330 |         0.0636 |                         0.0229 |                      0 |                             0 |                                        0 |                   0      |                          0.0023 |                                          0 |                   0.0819 |                          0.2143 |                                          0 |                  0.1257 |                         0.2143 |                                         0 |                  0.1654 |                         0.2708 |                                         0 |                  0.3429 |                         0.949  |                                    0.0455 |                  0.4736 |                         1      |                                    0.0606 |                   0.5889 |                          1      |                                     0.2303 |                 0.6708 |                        1      |                                   0.3152 |                  0.9525 |                              1 |                                    0.9061 |                 0.9883 |                             1 |                                   0.9788 |
| Q7            |   8 |         165 |         0.0602 |                         0.0232 |                      0 |                             0 |                                        0 |                   0      |                          0.0023 |                                          0 |                   0.1091 |                          0.2143 |                                          0 |                  0.1527 |                         0.2143 |                                         0 |                  0.1918 |                         0.2708 |                                         0 |                  0.3805 |                         0.9217 |                                    0.0364 |                  0.5027 |                         1      |                                    0.0424 |                   0.5915 |                          1      |                                     0.2121 |                 0.6578 |                        1      |                                   0.2606 |                  0.9721 |                              1 |                                    0.9515 |                 0.9958 |                             1 |                                   0.9939 |
| Q7            |   9 |          55 |         0.0583 |                         0.0232 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.1403 |                          0.2143 |                                          0 |                  0.1775 |                         0.2143 |                                         0 |                  0.2108 |                         0.2708 |                                         0 |                  0.4164 |                         0.9217 |                                    0.0182 |                  0.5221 |                         0.9581 |                                    0.0182 |                   0.5836 |                          1      |                                     0.1636 |                 0.6319 |                        1      |                                   0.1818 |                  0.9867 |                              1 |                                    0.9818 |                 0.9993 |                             1 |                                   1      |
| Q7            |  10 |          11 |         0.057  |                         0.0349 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.1753 |                          0.2143 |                                          0 |                  0.1986 |                         0.2143 |                                         0 |                  0.2194 |                         0.2708 |                                         0 |                  0.4558 |                         0.5032 |                                    0      |                  0.5379 |                         0.6747 |                                    0      |                   0.5713 |                          1      |                                     0.0909 |                 0.5976 |                        1      |                                   0.0909 |                  0.9967 |                              1 |                                    1      |                 1      |                             1 |                                   1      |
| Q7            |  11 |           1 |         0.0558 |                         0.0558 |                      0 |                             0 |                                        0 |                   0      |                          0      |                                          0 |                   0.2143 |                          0.2143 |                                          0 |                  0.2143 |                         0.2143 |                                         0 |                  0.2143 |                         0.2143 |                                         0 |                  0.5032 |                         0.5032 |                                    0      |                  0.5573 |                         0.5573 |                                    0      |                   0.5573 |                          0.5573 |                                     0      |                 0.5573 |                        0.5573 |                                   0      |                  1      |                              1 |                                    1      |                 1      |                             1 |                                   1      |

## 8b. The continuum oscillation allowance, arithmetic only

|          n |   d |    b |      h_n |   n_cells_populated |           L_n_cg |      s_n |   rho_paper |   rho_measured_p95_within_cell |   total_price_shading_3s_plus_rho |   elicitation_fraction |
|-----------:|----:|-----:|---------:|--------------------:|-----------------:|---------:|------------:|-------------------------------:|----------------------------------:|-----------------------:|
| 300000     |   1 |   24 | 0.041667 |                  24 |   1308           | 0.14131  |    0.567147 |                       0.215425 |                          0.991079 |               0.31392  |
| 300000     |   2 |   13 | 0.076923 |                 129 |    371           | 0.265333 |    1.48074  |                       0.23035  |                          2.27674  |               0.47859  |
|      1e+06 |   1 |   32 | 0.03125  |                  32 |   2457           | 0.107752 |    0.462985 |                       0.218812 |                          0.78624  |               0.235872 |
|      1e+06 |   2 |   16 | 0.0625   |                 181 |    617           | 0.215023 |    1.30952  |                       0.19     |                          1.95459  |               0.335031 |
|      1e+07 |   1 |   57 | 0.017544 |                  57 |   8150           | 0.06376  |    0.300317 |                       0.18025  |                          0.491596 |               0.139365 |
|      1e+07 |   2 |   26 | 0.038462 |                 466 |   1627           | 0.142702 |    0.931102 |                       0.135    |                          1.35921  |               0.227455 |
|      1e+09 |   1 |  178 | 0.005618 |                 178 |  88236           | 0.021906 |    0.122041 |                       0.12     |                          0.187759 |               0.047118 |
|      1e+09 |   2 |   64 | 0.015625 |                2627 |  11109           | 0.061738 |    0.480021 |                       0.065    |                          0.665234 |               0.08755  |
|      1e+12 |   1 | 1000 | 0.001    |                1000 |      3.05923e+06 | 0.004284 |    0.028631 |                       0.045    |                          0.041484 |               0.009178 |
|      1e+12 |   2 |  252 | 0.003968 |               19834 | 193025           | 0.017057 |    0.160676 |                       0.015    |                          0.211847 |               0.011485 |
|      1e+15 |   1 | 5624 | 0.000178 |                5624 |      1.03968e+08 | 0.00082  |    0.006319 |                       0.015    |                          0.00878  |               0.001754 |
|      1e+15 |   2 | 1001 | 0.000999 |               32530 |      3.28777e+06 | 0.004613 |    0.050209 |                       0        |                          0.064049 |               0.000321 |

## 8. Horizon sweep, the three selected triples

| models                                | context_set   | alpha   |        n |   nseeds |    L_n |     s_n |   elicit_frac_contextual |   elicit_frac_scalar |   rev_plmesp |   revsd_plmesp |   compconv_plmesp |   conv_plmesp |   priceabovecap_plmesp |   rev_mesp_scalar |   revsd_mesp_scalar |   compconv_mesp_scalar |   conv_mesp_scalar |   priceabovecap_mesp_scalar |   oracle |   second_cap |   honest_bench |   sim_gap |
|:--------------------------------------|:--------------|:--------|---------:|---------:|-------:|--------:|-------------------------:|---------------------:|-------------:|---------------:|------------------:|--------------:|-----------------------:|------------------:|--------------------:|-----------------------:|-------------------:|----------------------------:|---------:|-------------:|---------------:|----------:|
| Claude-Instant-V1|Claude-V1|Claude-V2 | Q3            | a0.50   |   300000 |        5 |  10700 | 0.04941 |                  0.321   |              0.107   |      0.58266 |        0.00257 |                 0 |             0 |                      0 |           0.54141 |             0.0009  |                    0   |                0   |                     0.39767 |  0.67265 |      0.63438 |        0.25564 |   0.04125 |
| Claude-Instant-V1|Claude-V1|Claude-V2 | Q3            | a0.50   |  1000000 |        5 |  24561 | 0.03408 |                  0.22105 |              0.07368 |      0.59612 |        0.00112 |                 0 |             0 |                      0 |           0.62527 |             0.00609 |                    1   |                1   |                     0.07655 |  0.67236 |      0.63407 |        0.25572 |  -0.02915 |
| Claude-Instant-V1|Claude-V1|Claude-V2 | Q3            | a0.50   |  3000000 |        5 |  52321 | 0.02423 |                  0.15696 |              0.05232 |      0.60532 |        0.00078 |                 0 |             0 |                      0 |           0.64211 |             0.00042 |                    1   |                1   |                     0.01502 |  0.67226 |      0.63399 |        0.25583 |  -0.03679 |
| Claude-Instant-V1|Claude-V1|Claude-V2 | Q3            | a0.50   | 10000000 |        5 | 119625 | 0.01664 |                  0.10766 |              0.03589 |      0.61384 |        0.00069 |                 0 |             0 |                      0 |           0.64659 |             9e-05   |                    1   |                1   |                     0.0025  |  0.67218 |      0.63391 |        0.25588 |  -0.03275 |
| Claude-Instant-V1|Claude-V1|Claude-V2 | Q3            | a0.50   | 30000000 |        5 | 254042 | 0.01179 |                  0.07621 |              0.0254  |      0.6196  |        0.00035 |                 0 |             0 |                      0 |           0.64792 |             6e-05   |                    1   |                1   |                     0.00094 |  0.67222 |      0.63395 |        0.25585 |  -0.02832 |
| Claude-Instant-V1|Claude-V1|GPT-4     | Q3            | a0.50   |   300000 |        5 |  10700 | 0.04941 |                  0.321   |              0.107   |      0.62425 |        0.00216 |                 0 |             0 |                      0 |           0.60973 |             0.00366 |                    0   |                0   |                     0       |  0.81052 |      0.65074 |        0.29694 |   0.01452 |
| Claude-Instant-V1|Claude-V1|GPT-4     | Q3            | a0.50   |  1000000 |        5 |  24561 | 0.03408 |                  0.22105 |              0.07368 |      0.62973 |        0.00166 |                 0 |             0 |                      0 |           0.62183 |             0.00248 |                    0   |                0   |                     0       |  0.81058 |      0.65038 |        0.29673 |   0.0079  |
| Claude-Instant-V1|Claude-V1|GPT-4     | Q3            | a0.50   |  3000000 |        5 |  52321 | 0.02423 |                  0.15696 |              0.05232 |      0.63357 |        0.00099 |                 0 |             0 |                      0 |           0.6289  |             0.00226 |                    0   |                0   |                     0       |  0.81042 |      0.65027 |        0.29668 |   0.00468 |
| Claude-Instant-V1|Claude-V1|GPT-4     | Q3            | a0.50   | 10000000 |        5 | 119625 | 0.01664 |                  0.10766 |              0.03589 |      0.63773 |        0.00073 |                 0 |             0 |                      0 |           0.63533 |             0.00069 |                    0   |                0   |                     0       |  0.81039 |      0.65017 |        0.29663 |   0.0024  |
| Claude-Instant-V1|Claude-V1|GPT-4     | Q3            | a0.50   | 30000000 |        5 | 254042 | 0.01179 |                  0.07621 |              0.0254  |      0.64172 |        0.00026 |                 0 |             0 |                      0 |           0.63839 |             0.00058 |                    0   |                0   |                     0       |  0.81043 |      0.65022 |        0.29665 |   0.00333 |
| Claude-V2|Llama-70B|Mixtral-8x7B      | Q3            | a0.50   |   300000 |        5 |  10700 | 0.04941 |                  0.321   |              0.107   |      0.57438 |        0.00271 |                 0 |             0 |                      0 |           0.59749 |             0.01135 |                    1   |                1   |                     0.11417 |  0.69087 |      0.61462 |        0.25564 |  -0.02311 |
| Claude-V2|Llama-70B|Mixtral-8x7B      | Q3            | a0.50   |  1000000 |        5 |  24561 | 0.03408 |                  0.22105 |              0.07368 |      0.58398 |        0.00146 |                 0 |             0 |                      0 |           0.63572 |             0.00311 |                    1   |                1   |                     0.02697 |  0.69088 |      0.61461 |        0.25572 |  -0.05174 |
| Claude-V2|Llama-70B|Mixtral-8x7B      | Q3            | a0.50   |  3000000 |        5 |  52321 | 0.02423 |                  0.15696 |              0.05232 |      0.59067 |        0.00038 |                 0 |             0 |                      0 |           0.64463 |             0.00035 |                    1   |                1   |                     0.00837 |  0.69085 |      0.6145  |        0.25583 |  -0.05396 |
| Claude-V2|Llama-70B|Mixtral-8x7B      | Q3            | a0.50   | 10000000 |        5 | 119625 | 0.01664 |                  0.10766 |              0.03589 |      0.59712 |        0.0006  |                 0 |             0 |                      0 |           0.64837 |             5e-05   |                    1   |                1   |                     0.00158 |  0.69084 |      0.61447 |        0.25588 |  -0.05125 |
| Claude-V2|Llama-70B|Mixtral-8x7B      | Q3            | a0.50   | 30000000 |        5 | 254042 | 0.01179 |                  0.07621 |              0.0254  |      0.60256 |        0.00047 |                 0 |             0 |                      0 |           0.64959 |             4e-05   |                    1   |                1   |                     0.0006  |  0.69085 |      0.6145  |        0.25585 |  -0.04703 |
| Claude-V2|CodeLlama-34B|WizardLM-13B  | Q7            | a0.50   |   300000 |        5 |  10700 | 0.04941 |                  0.749   |              0.107   |      0.49567 |        0.00066 |                 0 |             0 |                      0 |           0.47346 |             0.00275 |                    0   |                0   |                     0.01094 |  0.60505 |      0.5254  |        0.25698 |   0.02221 |
| Claude-V2|CodeLlama-34B|WizardLM-13B  | Q7            | a0.50   |  1000000 |        5 |  24561 | 0.03408 |                  0.51578 |              0.07368 |      0.50139 |        0.00136 |                 0 |             0 |                      0 |           0.48356 |             0.00117 |                    0   |                0   |                     0.01144 |  0.60501 |      0.52547 |        0.25702 |   0.01783 |
| Claude-V2|CodeLlama-34B|WizardLM-13B  | Q7            | a0.50   |  3000000 |        5 |  52321 | 0.02423 |                  0.36625 |              0.05232 |      0.50908 |        0.00063 |                 0 |             0 |                      0 |           0.49198 |             0.00061 |                    0   |                0   |                     0.01166 |  0.60506 |      0.52549 |        0.25701 |   0.0171  |
| Claude-V2|CodeLlama-34B|WizardLM-13B  | Q7            | a0.50   | 10000000 |        5 | 119625 | 0.01664 |                  0.25121 |              0.03589 |      0.51372 |        0.00104 |                 0 |             0 |                      0 |           0.49826 |             0.00076 |                    0.2 |                0.2 |                     0.01177 |  0.60505 |      0.5255  |        0.25702 |   0.01547 |
| Claude-V2|CodeLlama-34B|WizardLM-13B  | Q7            | a0.50   | 30000000 |        5 | 254042 | 0.01179 |                  0.17783 |              0.0254  |      0.51627 |        0.00044 |                 0 |             0 |                      0 |           0.52893 |             0.00307 |                    1   |                1   |                     0.00494 |  0.60506 |      0.52551 |        0.25702 |  -0.01266 |
| Claude-V2|GPT-3.5|WizardLM-13B        | Q7            | a0.50   |   300000 |        5 |  10700 | 0.04941 |                  0.749   |              0.107   |      0.55438 |        0.00145 |                 0 |             0 |                      0 |           0.51046 |             0.00364 |                    0   |                0   |                     0       |  0.70916 |      0.59035 |        0.2576  |   0.04392 |
| Claude-V2|GPT-3.5|WizardLM-13B        | Q7            | a0.50   |  1000000 |        5 |  24561 | 0.03408 |                  0.51578 |              0.07368 |      0.5668  |        0.00091 |                 0 |             0 |                      0 |           0.51975 |             0.00099 |                    0   |                0   |                     0       |  0.70919 |      0.59037 |        0.25764 |   0.04706 |
| Claude-V2|GPT-3.5|WizardLM-13B        | Q7            | a0.50   |  3000000 |        5 |  52321 | 0.02423 |                  0.36625 |              0.05232 |      0.57321 |        0.00122 |                 0 |             0 |                      0 |           0.52659 |             0.0018  |                    0   |                0   |                     0       |  0.70913 |      0.59039 |        0.25777 |   0.04662 |
| Claude-V2|GPT-3.5|WizardLM-13B        | Q7            | a0.50   | 10000000 |        5 | 119625 | 0.01664 |                  0.25121 |              0.03589 |      0.57783 |        0.00082 |                 0 |             0 |                      0 |           0.53419 |             0.00164 |                    0   |                0   |                     0       |  0.70911 |      0.59039 |        0.2578  |   0.04364 |
| Claude-V2|GPT-3.5|WizardLM-13B        | Q7            | a0.50   | 30000000 |        5 | 254042 | 0.01179 |                  0.17783 |              0.0254  |      0.5809  |        0.00037 |                 0 |             0 |                      0 |           0.53815 |             0.0007  |                    0   |                0   |                     0       |  0.7091  |      0.59039 |        0.25783 |   0.04274 |
| CodeLlama-34B|GPT-3.5|GPT-4           | Q7            | a0.50   |   300000 |        5 |  10700 | 0.04941 |                  0.749   |              0.107   |      0.64863 |        0.00121 |                 0 |             0 |                      0 |           0.65229 |             0.00289 |                    0   |                0   |                     0       |  0.8167  |      0.69676 |        0.25698 |  -0.00366 |
| CodeLlama-34B|GPT-3.5|GPT-4           | Q7            | a0.50   |  1000000 |        5 |  24561 | 0.03408 |                  0.51578 |              0.07368 |      0.66044 |        0.00113 |                 0 |             0 |                      0 |           0.6625  |             0.00145 |                    0   |                0   |                     0.19812 |  0.81682 |      0.69684 |        0.25702 |  -0.00206 |
| CodeLlama-34B|GPT-3.5|GPT-4           | Q7            | a0.50   |  3000000 |        5 |  52321 | 0.02423 |                  0.36625 |              0.05232 |      0.669   |        0.0012  |                 0 |             0 |                      0 |           0.68254 |             0.02734 |                    0.2 |                0.2 |                     0.18343 |  0.81668 |      0.69674 |        0.25701 |  -0.01355 |
| CodeLlama-34B|GPT-3.5|GPT-4           | Q7            | a0.50   | 10000000 |        5 | 119625 | 0.01664 |                  0.25121 |              0.03589 |      0.6795  |        0.00025 |                 0 |             0 |                      0 |           0.79179 |             0.00252 |                    1   |                1   |                     0.02898 |  0.81668 |      0.69672 |        0.25702 |  -0.11229 |
| CodeLlama-34B|GPT-3.5|GPT-4           | Q7            | a0.50   | 30000000 |        5 | 254042 | 0.01179 |                  0.17783 |              0.0254  |      0.68386 |        0.00032 |                 0 |             0 |                      0 |           0.80718 |             0.00052 |                    1   |                1   |                     0.00845 |  0.81665 |      0.69671 |        0.25702 |  -0.12332 |

## 9. All 165 triples at the larger horizon

|     n |   n_triples |   spearman_rho_flip_vs_simgap |   spearman_p |   ols_slope |   ols_intercept |   ols_r2 |   mean_sim_gap |   frac_sim_gap_positive |   mean_compconv_scalar |   mean_compconv_contextual |   frac_runs_scalar_price_above_cap |   spearman_flip_vs_compconv_scalar |   spearman_flip_vs_compconv_scalar_p |
|------:|------------:|------------------------------:|-------------:|------------:|----------------:|---------:|---------------:|------------------------:|-----------------------:|---------------------------:|-----------------------------------:|-----------------------------------:|-------------------------------------:|
| 3e+06 |         165 |                       0.05492 |      0.48351 |    -0.00013 |        -0.02387 |        0 |       -0.02391 |                 0.47273 |                0.53697 |                          0 |                            0.61212 |                            0.27811 |                               0.0003 |

## 10. Two worlds, revenue per round, context set Q3

| mech          |   ('nonstrategic', 'a0.00') |   ('nonstrategic', 'a0.25') |   ('nonstrategic', 'a0.50') |   ('nonstrategic', 'a0.75') |   ('nonstrategic', 'het') |   ('strategic', 'a0.00') |   ('strategic', 'a0.25') |   ('strategic', 'a0.50') |   ('strategic', 'a0.75') |   ('strategic', 'het') |
|:--------------|----------------------------:|----------------------------:|----------------------------:|----------------------------:|--------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|
| mesp_scalar   |                      0.6952 |                      0.6952 |                      0.6952 |                      0.6952 |                    0.6952 |                   0.2096 |                   0.2819 |                   0.3827 |                   0.4281 |                 0.4651 |
| plmesp        |                      0.6937 |                      0.6937 |                      0.6937 |                      0.6937 |                    0.6937 |                   0.2411 |                   0.3246 |                   0.4056 |                   0.5265 |                 0.4804 |
| router_eps    |                      0.7185 |                      0.7185 |                      0.7185 |                      0.7185 |                    0.7185 |                   0.5984 |                   0.6647 |                   0.6837 |                   0.7118 |                 0.7105 |
| router_greedy |                      0.6883 |                      0.6883 |                      0.6883 |                      0.6883 |                    0.6883 |                   0.5932 |                   0.6883 |                   0.6883 |                   0.675  |                 0.6883 |
| router_ucb    |                      0.721  |                      0.721  |                      0.721  |                      0.721  |                    0.721  |                   0.6806 |                   0.721  |                   0.7144 |                   0.7178 |                 0.7185 |

## 10. Two worlds, revenue per round, context set Q7

| mech          |   ('nonstrategic', 'a0.00') |   ('nonstrategic', 'a0.25') |   ('nonstrategic', 'a0.50') |   ('nonstrategic', 'a0.75') |   ('nonstrategic', 'het') |   ('strategic', 'a0.00') |   ('strategic', 'a0.25') |   ('strategic', 'a0.50') |   ('strategic', 'a0.75') |   ('strategic', 'het') |
|:--------------|----------------------------:|----------------------------:|----------------------------:|----------------------------:|--------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|
| mesp_scalar   |                      0.6776 |                      0.6776 |                      0.7433 |                      0.6776 |                    0.6776 |                   0.0245 |                   0.1228 |                   0.2818 |                   0.4044 |                 0.3734 |
| plmesp        |                      0.6577 |                      0.6577 |                      0.7021 |                      0.6577 |                    0.6577 |                   0.2201 |                   0.3269 |                   0.3555 |                   0.4733 |                 0.4386 |
| router_eps    |                      0.7039 |                      0.7039 |                      0.7557 |                      0.7039 |                    0.7039 |                   0.6826 |                   0.4831 |                   0.7195 |                   0.6488 |                 0.6894 |
| router_greedy |                      0.6661 |                      0.6661 |                      0.7111 |                      0.6661 |                    0.6661 |                   0.6252 |                   0.6661 |                   0.7111 |                   0.6551 |                 0.6628 |
| router_ucb    |                      0.7063 |                      0.7063 |                      0.7593 |                      0.7063 |                    0.7063 |                   0.7063 |                   0.7063 |                   0.7593 |                   0.6944 |                 0.7063 |

## 10. Two worlds, revenue per round, context set Q7u

| mech          |   ('nonstrategic', 'a0.00') |   ('nonstrategic', 'a0.25') |   ('nonstrategic', 'a0.50') |   ('nonstrategic', 'a0.75') |   ('nonstrategic', 'het') |   ('strategic', 'a0.00') |   ('strategic', 'a0.25') |   ('strategic', 'a0.50') |   ('strategic', 'a0.75') |   ('strategic', 'het') |
|:--------------|----------------------------:|----------------------------:|----------------------------:|----------------------------:|--------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|
| mesp_scalar   |                      0.6235 |                      0.6821 |                      0.7431 |                      0.6821 |                    0.6821 |                   0.2733 |                   0.2671 |                   0.2851 |                   0.4736 |                 0.4443 |
| plmesp        |                      0.5956 |                      0.6359 |                      0.6706 |                      0.6359 |                    0.6359 |                   0.1171 |                   0.4308 |                   0.4328 |                   0.5153 |                 0.4575 |
| router_eps    |                      0.6609 |                      0.7093 |                      0.7527 |                      0.7093 |                    0.7093 |                   0.6427 |                   0.6826 |                   0.748  |                   0.7075 |                 0.7072 |
| router_greedy |                      0.6227 |                      0.6724 |                      0.7162 |                      0.6724 |                    0.6724 |                   0.6227 |                   0.6724 |                   0.7162 |                   0.6707 |                 0.6724 |
| router_ucb    |                      0.6616 |                      0.7105 |                      0.7544 |                      0.7105 |                    0.7105 |                   0.6616 |                   0.7105 |                   0.7544 |                   0.7105 |                 0.7105 |

## 10. Two worlds, revenue per round, context set cont_rhomeasured

| mech          |   ('nonstrategic', 'a0.00') |   ('nonstrategic', 'a0.25') |   ('nonstrategic', 'a0.50') |   ('nonstrategic', 'a0.75') |   ('nonstrategic', 'het') |   ('strategic', 'a0.00') |   ('strategic', 'a0.25') |   ('strategic', 'a0.50') |   ('strategic', 'a0.75') |   ('strategic', 'het') |
|:--------------|----------------------------:|----------------------------:|----------------------------:|----------------------------:|--------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|
| mesp_scalar   |                      0.6771 |                      0.6771 |                      0.6771 |                      0.6149 |                    0.6771 |                   0.0245 |                   0.1217 |                   0.2634 |                   0.3638 |                 0.373  |
| plmesp        |                      0.6593 |                      0.6593 |                      0.6593 |                      0.6137 |                    0.6593 |                   0.149  |                   0.1787 |                   0.2314 |                   0.2778 |                 0.2536 |
| router_eps    |                      0.6955 |                      0.6955 |                      0.6955 |                      0.6421 |                    0.6955 |                   0.6929 |                   0.6935 |                   0.6943 |                   0.6421 |                 0.695  |
| router_greedy |                      0.6662 |                      0.6662 |                      0.6662 |                      0.608  |                    0.6662 |                   0.6662 |                   0.6662 |                   0.6662 |                   0.608  |                 0.6662 |
| router_ucb    |                      0.6847 |                      0.6847 |                      0.6847 |                      0.6321 |                    0.6847 |                   0.6847 |                   0.6847 |                   0.6847 |                   0.6321 |                 0.6847 |

## 10. Two worlds, revenue per round, context set cont_rhopaper

| mech          |   ('nonstrategic', 'a0.00') |   ('nonstrategic', 'a0.25') |   ('nonstrategic', 'a0.50') |   ('nonstrategic', 'a0.75') |   ('nonstrategic', 'het') |   ('strategic', 'a0.00') |   ('strategic', 'a0.25') |   ('strategic', 'a0.50') |   ('strategic', 'a0.75') |   ('strategic', 'het') |
|:--------------|----------------------------:|----------------------------:|----------------------------:|----------------------------:|--------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|
| mesp_scalar   |                      0.6771 |                      0.6771 |                      0.6771 |                      0.6149 |                    0.6771 |                   0.0245 |                   0.1217 |                   0.2634 |                   0.3638 |                 0.373  |
| plmesp        |                      0.6593 |                      0.6593 |                      0.6593 |                      0.6137 |                    0.6593 |                   0.1377 |                   0.1738 |                   0.2263 |                   0.2702 |                 0.2485 |
| router_eps    |                      0.6955 |                      0.6955 |                      0.6955 |                      0.6421 |                    0.6955 |                   0.6929 |                   0.6935 |                   0.6943 |                   0.6421 |                 0.695  |
| router_greedy |                      0.6662 |                      0.6662 |                      0.6662 |                      0.608  |                    0.6662 |                   0.6662 |                   0.6662 |                   0.6662 |                   0.608  |                 0.6662 |
| router_ucb    |                      0.6847 |                      0.6847 |                      0.6847 |                      0.6321 |                    0.6847 |                   0.6847 |                   0.6847 |                   0.6847 |                   0.6321 |                 0.6847 |

## 10b. Strategic-world revenue minus the honest benchmark

| mech          |   mean |     min |    max |   count |
|:--------------|-------:|--------:|-------:|--------:|
| mesp_scalar   | 0.0386 | -0.0437 | 0.5768 |      70 |
| plmesp        | 0.0781 | -0.1953 | 0.4013 |      70 |
| router_eps    | 0.4371 |  0.1519 | 0.809  |      70 |
| router_greedy | 0.4234 |  0.1502 | 0.7826 |      70 |
| router_ucb    | 0.4578 |  0.1725 | 0.8132 |      70 |

## 11. Exploitability: best single deviation at the proposed profile

|                                       |   a0.00 |   a0.25 |   a0.50 |   a0.75 |    het |
|:--------------------------------------|--------:|--------:|--------:|--------:|-------:|
| ('Q3', 'mesp_scalar')                 |  0.0201 |  0.0146 |  0.0092 |  0.007  | 0.0075 |
| ('Q3', 'plmesp')                      |  0.0545 |  0.0397 |  0.0249 |  0.0131 | 0.0265 |
| ('Q3', 'router_eps')                  |  0.0069 |  0.0094 |  0.007  |  0.006  | 0.0067 |
| ('Q3', 'router_greedy')               |  0.0151 |  0      |  0      |  0.011  | 0      |
| ('Q3', 'router_ucb')                  |  0.0046 |  0      |  0.0011 |  0.0011 | 0.0012 |
| ('Q7', 'mesp_scalar')                 |  0.0209 |  0.0157 |  0.0111 |  0.0052 | 0.0105 |
| ('Q7', 'plmesp')                      |  0.0768 |  0.0566 |  0.0409 |  0.0185 | 0.0268 |
| ('Q7', 'router_eps')                  |  0.008  |  0.0057 |  0.0229 |  0.0175 | 0.002  |
| ('Q7', 'router_greedy')               |  0.0069 |  0      |  0      |  0.0058 | 0.0029 |
| ('Q7', 'router_ucb')                  |  0      |  0      |  0      |  0.0036 | 0      |
| ('Q7u', 'mesp_scalar')                |  0.0413 |  0.0398 |  0.0112 |  0.0479 | 0.0345 |
| ('Q7u', 'plmesp')                     |  0.1222 |  0.1019 |  0.0769 |  0.0314 | 0.0604 |
| ('Q7u', 'router_eps')                 |  0.0059 |  0.0048 |  0.0037 |  0.0012 | 0.0015 |
| ('Q7u', 'router_greedy')              |  0      |  0      |  0      |  0.0016 | 0      |
| ('Q7u', 'router_ucb')                 |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhomeasured', 'mesp_scalar')   |  0.0209 |  0.0157 |  0.0105 |  0.0047 | 0.0105 |
| ('cont_rhomeasured', 'plmesp')        |  0.056  |  0.0412 |  0.0289 |  0.0209 | 0.0229 |
| ('cont_rhomeasured', 'router_eps')    |  0.0024 |  0.0016 |  0.0008 |  0      | 0.0001 |
| ('cont_rhomeasured', 'router_greedy') |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhomeasured', 'router_ucb')    |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhopaper', 'mesp_scalar')      |  0.0209 |  0.0157 |  0.0105 |  0.0047 | 0.0105 |
| ('cont_rhopaper', 'plmesp')           |  0.0553 |  0.0372 |  0.0241 |  0.0082 | 0.0165 |
| ('cont_rhopaper', 'router_eps')       |  0.0024 |  0.0016 |  0.0008 |  0      | 0.0001 |
| ('cont_rhopaper', 'router_greedy')    |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhopaper', 'router_ucb')       |  0      |  0      |  0      |  0      | 0      |

## 12. Compliant convictions at the proposed profile (mean count per run)

|                                       |   compliant_convictions |
|:--------------------------------------|------------------------:|
| ('Q3', 'mesp_scalar')                 |                   0.333 |
| ('Q3', 'plmesp')                      |                   0     |
| ('Q3', 'router_eps')                  |                   0     |
| ('Q3', 'router_greedy')               |                   0     |
| ('Q3', 'router_ucb')                  |                   0     |
| ('Q7', 'mesp_scalar')                 |                   0     |
| ('Q7', 'plmesp')                      |                   0     |
| ('Q7', 'router_eps')                  |                   0     |
| ('Q7', 'router_greedy')               |                   0     |
| ('Q7', 'router_ucb')                  |                   0     |
| ('Q7u', 'mesp_scalar')                |                   0.308 |
| ('Q7u', 'plmesp')                     |                   0     |
| ('Q7u', 'router_eps')                 |                   0     |
| ('Q7u', 'router_greedy')              |                   0     |
| ('Q7u', 'router_ucb')                 |                   0     |
| ('cont_rhomeasured', 'mesp_scalar')   |                   0     |
| ('cont_rhomeasured', 'plmesp')        |                   0     |
| ('cont_rhomeasured', 'router_eps')    |                   0     |
| ('cont_rhomeasured', 'router_greedy') |                   0     |
| ('cont_rhomeasured', 'router_ucb')    |                   0     |
| ('cont_rhopaper', 'mesp_scalar')      |                   0     |
| ('cont_rhopaper', 'plmesp')           |                   0     |
| ('cont_rhopaper', 'router_eps')       |                   0     |
| ('cont_rhopaper', 'router_greedy')    |                   0     |
| ('cont_rhopaper', 'router_ucb')       |                   0     |


Local instances that completed elicitation:

| family_set       |   locals_past_elicitation |   locals_total |
|:-----------------|--------------------------:|---------------:|
| Q3               |                       2.6 |            2.6 |
| Q7               |                       5   |            5.8 |
| Q7u              |                       5.8 |            5.8 |
| cont_rhomeasured |                      96.2 |          103.4 |
| cont_rhopaper    |                      96.2 |          103.4 |

## 11b. The strategic profile reached, and what it costs

|                                       |   a0.00 |   a0.25 |   a0.50 |   a0.75 |    het |
|:--------------------------------------|--------:|--------:|--------:|--------:|-------:|
| ('Q3', 'mesp_scalar')                 |  0.3732 |  0.301  |  0.2001 |  0.1548 | 0.1177 |
| ('Q3', 'plmesp')                      |  0.3529 |  0.2694 |  0.1884 |  0.0684 | 0.116  |
| ('Q3', 'router_eps')                  |  0.1201 |  0.0538 |  0.0348 |  0.0067 | 0.008  |
| ('Q3', 'router_greedy')               |  0.0951 |  0      |  0      |  0.0132 | 0      |
| ('Q3', 'router_ucb')                  |  0.0405 |  0      |  0.0066 |  0.0033 | 0.0025 |
| ('Q7', 'mesp_scalar')                 |  0.5193 |  0.421  |  0.2974 |  0.1394 | 0.1704 |
| ('Q7', 'plmesp')                      |  0.3464 |  0.2396 |  0.2465 |  0.0931 | 0.1279 |
| ('Q7', 'router_eps')                  |  0.0214 |  0.2208 |  0.0363 |  0.0551 | 0.0145 |
| ('Q7', 'router_greedy')               |  0.0409 |  0      |  0      |  0.011  | 0.0033 |
| ('Q7', 'router_ucb')                  |  0      |  0      |  0      |  0.0119 | 0      |
| ('Q7u', 'mesp_scalar')                |  0.2604 |  0.3062 |  0.3018 |  0.0996 | 0.1289 |
| ('Q7u', 'plmesp')                     |  0.4435 |  0.168  |  0.1991 |  0.0834 | 0.1414 |
| ('Q7u', 'router_eps')                 |  0.0182 |  0.0267 |  0.0047 |  0.0018 | 0.0021 |
| ('Q7u', 'router_greedy')              |  0      |  0      |  0      |  0.0016 | 0      |
| ('Q7u', 'router_ucb')                 |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhomeasured', 'mesp_scalar')   |  0.5174 |  0.4202 |  0.2785 |  0.1243 | 0.1688 |
| ('cont_rhomeasured', 'plmesp')        |  0.1705 |  0.1456 |  0.105  |  0.0372 | 0.0973 |
| ('cont_rhomeasured', 'router_eps')    |  0.0027 |  0.002  |  0.0013 |  0      | 0.0006 |
| ('cont_rhomeasured', 'router_greedy') |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhomeasured', 'router_ucb')    |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhopaper', 'mesp_scalar')      |  0.5174 |  0.4202 |  0.2785 |  0.1243 | 0.1688 |
| ('cont_rhopaper', 'plmesp')           |  0.105  |  0.081  |  0.0406 |  0.0086 | 0.0329 |
| ('cont_rhopaper', 'router_eps')       |  0.0027 |  0.002  |  0.0013 |  0      | 0.0006 |
| ('cont_rhopaper', 'router_greedy')    |  0      |  0      |  0      |  0      | 0      |
| ('cont_rhopaper', 'router_ucb')       |  0      |  0      |  0      |  0      | 0      |


How many providers shade in the profile reached:

|                                       |   a0.00 |   a0.25 |   a0.50 |   a0.75 |   het |
|:--------------------------------------|--------:|--------:|--------:|--------:|------:|
| ('Q3', 'mesp_scalar')                 |    1.67 |    1.67 |    1.67 |    2    |  1.67 |
| ('Q3', 'plmesp')                      |    1.33 |    2    |    1.67 |    1.33 |  1.33 |
| ('Q3', 'router_eps')                  |    0.67 |    1.67 |    1    |    0.33 |  0.33 |
| ('Q3', 'router_greedy')               |    1.33 |    0    |    0    |    0.33 |  0    |
| ('Q3', 'router_ucb')                  |    0.33 |    0    |    0.33 |    0.33 |  0.33 |
| ('Q7', 'mesp_scalar')                 |    2    |    2    |    2    |    2    |  2    |
| ('Q7', 'plmesp')                      |    1.33 |    2    |    1.5  |    1.33 |  1.33 |
| ('Q7', 'router_eps')                  |    0.67 |    1.67 |    1    |    1.33 |  1    |
| ('Q7', 'router_greedy')               |    0.33 |    0    |    0    |    1    |  0.33 |
| ('Q7', 'router_ucb')                  |    0    |    0    |    0    |    0.33 |  0    |
| ('Q7u', 'mesp_scalar')                |    2    |    2    |    2    |    2    |  2    |
| ('Q7u', 'plmesp')                     |    3    |    0.67 |    2    |    1.67 |  1.67 |
| ('Q7u', 'router_eps')                 |    1    |    0.67 |    1    |    0.67 |  0.67 |
| ('Q7u', 'router_greedy')              |    0    |    0    |    0    |    0    |  0    |
| ('Q7u', 'router_ucb')                 |    0    |    0    |    0    |    0    |  0    |
| ('cont_rhomeasured', 'mesp_scalar')   |    2    |    2    |    2    |    2    |  2    |
| ('cont_rhomeasured', 'plmesp')        |    1.33 |    1.33 |    1    |    0.5  |  1    |
| ('cont_rhomeasured', 'router_eps')    |    0.33 |    0.33 |    0.33 |    0    |  0.33 |
| ('cont_rhomeasured', 'router_greedy') |    0    |    0    |    0    |    0    |  0    |
| ('cont_rhomeasured', 'router_ucb')    |    0    |    0    |    0    |    0    |  0    |
| ('cont_rhopaper', 'mesp_scalar')      |    2    |    2    |    2    |    2    |  2    |
| ('cont_rhopaper', 'plmesp')           |    1.33 |    1.33 |    1    |    0.5  |  1    |
| ('cont_rhopaper', 'router_eps')       |    0.33 |    0.33 |    0.33 |    0    |  0.33 |
| ('cont_rhopaper', 'router_greedy')    |    0    |    0    |    0    |    0    |  0    |
| ('cont_rhopaper', 'router_ucb')       |    0    |    0    |    0    |    0    |  0    |

## 11c. THE FAIR STRATEGIC COMPARISON: best response over one rich option class for every rule

| mech          |   n_cells |   nonstrategic |   strategic |   degradation |   worst_degradation |   cells_whose_profile_uses_undercut |
|:--------------|----------:|---------------:|------------:|--------------:|--------------------:|------------------------------------:|
| mesp_scalar   |        20 |         0.7089 |      0.249  |        0.4599 |              0.7737 |                                   0 |
| plmesp        |        20 |         0.6871 |      0.3593 |        0.3278 |              0.6646 |                                   0 |
| router_eps    |        20 |         0.7305 |      0.6516 |        0.079  |              0.2161 |                                  17 |
| router_greedy |        20 |         0.6928 |      0.644  |        0.0487 |              0.1262 |                                  12 |
| router_ucb    |        20 |         0.7329 |      0.6792 |        0.0537 |              0.0717 |                                  20 |


Profile reached in each completed cell:

| triple   | alpha   | mech          | profile                             |   nonstrategic_revenue |   strategic_revenue |
|:---------|:--------|:--------------|:------------------------------------|-----------------------:|--------------------:|
| lowflip  | a0.00   | plmesp        | theta0.00|theta0.00|proposed        |                 0.7497 |              0.0851 |
| lowflip  | a0.00   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.8017 |              0.0291 |
| lowflip  | a0.00   | router_greedy | theta1.00|theta0.975|theta0.75      |                 0.7441 |              0.6179 |
| lowflip  | a0.00   | router_eps    | theta0.95|theta0.75|theta0.75       |                 0.809  |              0.6073 |
| lowflip  | a0.00   | router_ucb    | theta0.99|theta1.00|undercut0.05    |                 0.8132 |              0.7415 |
| lowflip  | a0.25   | plmesp        | theta0.00|theta0.00|theta0.00       |                 0.7497 |              0.1874 |
| lowflip  | a0.25   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.8017 |              0.1517 |
| lowflip  | a0.25   | router_greedy | theta0.99|theta0.975|undercut0.02   |                 0.7441 |              0.6659 |
| lowflip  | a0.25   | router_eps    | theta0.99|theta0.75|theta0.75       |                 0.809  |              0.6584 |
| lowflip  | a0.25   | router_ucb    | theta0.99|theta1.00|undercut0.05    |                 0.8132 |              0.7415 |
| highflip | a0.00   | plmesp        | selective|theta0.00|theta0.00       |                 0.5691 |              0.2946 |
| highflip | a0.00   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.5461 |              0.0196 |
| highflip | a0.00   | router_greedy | undercut0.0|theta1.00|undercut0.05  |                 0.5771 |              0.5303 |
| highflip | a0.00   | router_eps    | undercut0.05|theta1.00|undercut0.02 |                 0.6005 |              0.5589 |
| highflip | a0.00   | router_ucb    | undercut0.05|theta1.00|undercut0.05 |                 0.6002 |              0.5653 |
| highflip | a0.25   | plmesp        | proposed|theta0.00|theta0.50        |                 0.5691 |              0.3345 |
| highflip | a0.25   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.5461 |              0.1045 |
| highflip | a0.25   | router_greedy | undercut0.0|theta1.00|undercut0.05  |                 0.5771 |              0.5303 |
| highflip | a0.25   | router_eps    | undercut0.05|theta1.00|undercut0.02 |                 0.6005 |              0.5589 |
| highflip | a0.25   | router_ucb    | undercut0.05|theta1.00|undercut0.05 |                 0.6002 |              0.5653 |
| highflip | a0.50   | plmesp        | proposed|theta0.00|theta0.25        |                 0.5691 |              0.3489 |
| highflip | a0.50   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.5461 |              0.229  |
| highflip | a0.50   | router_greedy | undercut0.0|theta1.00|undercut0.05  |                 0.5771 |              0.5303 |
| highflip | a0.50   | router_eps    | undercut0.05|theta0.99|undercut0.02 |                 0.6005 |              0.5581 |
| highflip | a0.50   | router_ucb    | undercut0.05|theta1.00|undercut0.05 |                 0.6002 |              0.5653 |
| highflip | a0.75   | plmesp        | proposed|theta0.00|proposed         |                 0.5691 |              0.4577 |
| highflip | a0.75   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.5461 |              0.3514 |
| highflip | a0.75   | router_greedy | theta0.75|theta0.99|undercut0.05    |                 0.5771 |              0.5556 |
| highflip | a0.75   | router_eps    | undercut0.05|theta0.95|theta0.95    |                 0.6005 |              0.5737 |
| highflip | a0.75   | router_ucb    | undercut0.05|theta1.00|theta0.975   |                 0.6002 |              0.5744 |
| highflip | het     | plmesp        | proposed|theta0.00|proposed         |                 0.5691 |              0.4651 |
| highflip | het     | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.5461 |              0.3661 |
| highflip | het     | router_greedy | undercut0.0|theta0.99|undercut0.05  |                 0.5771 |              0.53   |
| highflip | het     | router_eps    | undercut0.05|theta1.00|undercut0.02 |                 0.6005 |              0.5589 |
| highflip | het     | router_ucb    | undercut0.05|theta1.00|undercut0.05 |                 0.6002 |              0.5653 |
| dominant | a0.00   | plmesp        | proposed|theta0.00|theta0.00        |                 0.7752 |              0.16   |
| dominant | a0.00   | mesp_scalar   | proposed|theta0.00|theta0.00        |                 0.8028 |              0.0291 |
| dominant | a0.00   | router_greedy | undercut0.05|theta0.99|theta0.25    |                 0.797  |              0.7667 |
| dominant | a0.00   | router_eps    | undercut0.02|theta0.975|theta0.00   |                 0.81   |              0.7393 |
| dominant | a0.00   | router_ucb    | undercut0.05|theta1.00|theta0.975   |                 0.8127 |              0.7728 |
| dominant | a0.25   | plmesp        | proposed|theta0.00|theta0.00        |                 0.7752 |              0.274  |
| dominant | a0.25   | mesp_scalar   | proposed|theta0.00|theta0.00        |                 0.8028 |              0.1604 |
| dominant | a0.25   | router_greedy | undercut0.05|theta1.00|theta0.00    |                 0.797  |              0.7687 |
| dominant | a0.25   | router_eps    | theta0.50|theta0.75|theta0.975      |                 0.81   |              0.5939 |
| dominant | a0.25   | router_ucb    | undercut0.05|theta1.00|theta1.00    |                 0.8127 |              0.7727 |
| dominant | a0.50   | plmesp        | proposed|theta0.00|theta0.00        |                 0.7752 |              0.4152 |
| dominant | a0.50   | mesp_scalar   | proposed|theta0.00|theta0.00        |                 0.8028 |              0.3356 |
| dominant | a0.50   | router_greedy | undercut0.05|theta0.99|theta0.90    |                 0.797  |              0.7638 |
| dominant | a0.50   | router_eps    | undercut0.05|theta0.975|theta0.00   |                 0.81   |              0.7672 |
| dominant | a0.50   | router_ucb    | undercut0.05|theta1.00|theta0.99    |                 0.8127 |              0.7726 |
| dominant | a0.75   | plmesp        | proposed|theta0.00|theta0.00        |                 0.7752 |              0.557  |
| dominant | a0.75   | mesp_scalar   | proposed|theta0.00|theta0.00        |                 0.8028 |              0.5108 |
| dominant | a0.75   | router_greedy | undercut0.05|theta0.99|theta0.90    |                 0.797  |              0.7658 |
| dominant | a0.75   | router_eps    | undercut0.05|theta1.00|theta0.00    |                 0.81   |              0.7688 |
| dominant | a0.75   | router_ucb    | undercut0.05|theta1.00|theta0.99    |                 0.8127 |              0.7726 |
| dominant | het     | plmesp        | proposed|theta0.00|theta0.00        |                 0.7752 |              0.4536 |
| dominant | het     | mesp_scalar   | proposed|theta0.00|theta0.00        |                 0.8028 |              0.3772 |
| dominant | het     | router_greedy | theta0.975|theta0.99|theta0.75      |                 0.797  |              0.7839 |
| dominant | het     | router_eps    | undercut0.05|theta1.00|theta0.00    |                 0.81   |              0.7692 |
| dominant | het     | router_ucb    | undercut0.05|theta1.00|theta0.99    |                 0.8127 |              0.7726 |
| lowflip  | a0.50   | plmesp        | theta0.00|theta0.00|proposed        |                 0.7497 |              0.3527 |
| lowflip  | a0.50   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.8017 |              0.3182 |
| lowflip  | a0.50   | router_greedy | theta0.99|theta0.99|theta0.50       |                 0.7441 |              0.6213 |
| lowflip  | a0.50   | router_eps    | theta0.99|theta0.90|undercut0.02    |                 0.809  |              0.7116 |
| lowflip  | a0.50   | router_ucb    | theta1.00|theta1.00|undercut0.05    |                 0.8132 |              0.7416 |
| lowflip  | a0.75   | plmesp        | theta0.00|theta0.00|proposed        |                 0.7497 |              0.5004 |
| lowflip  | a0.75   | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.8017 |              0.4844 |
| lowflip  | a0.75   | router_greedy | theta0.975|theta0.95|theta0.99      |                 0.7441 |              0.7409 |
| lowflip  | a0.75   | router_eps    | theta0.00|theta0.99|undercut0.05    |                 0.809  |              0.7389 |
| lowflip  | a0.75   | router_ucb    | theta0.975|theta1.00|undercut0.05   |                 0.8132 |              0.7415 |
| lowflip  | het     | plmesp        | theta0.00|theta0.00|proposed        |                 0.7497 |              0.4172 |
| lowflip  | het     | mesp_scalar   | theta0.00|theta0.00|proposed        |                 0.8017 |              0.3799 |
| lowflip  | het     | router_greedy | theta0.975|theta0.99|undercut0.02   |                 0.7441 |              0.6684 |
| lowflip  | het     | router_eps    | theta0.00|theta1.00|undercut0.05    |                 0.809  |              0.7387 |
| lowflip  | het     | router_ucb    | theta0.95|theta1.00|undercut0.05    |                 0.8132 |              0.7415 |
| midflip  | a0.00   | plmesp        | selective|proposed|theta0.00        |                 0.6545 |              0.1738 |
| midflip  | a0.00   | mesp_scalar   | theta0.00|proposed|theta0.00        |                 0.685  |              0.0249 |
| midflip  | a0.00   | router_greedy | undercut0.0|undercut0.0|theta0.975  |                 0.6528 |              0.5784 |
| midflip  | a0.00   | router_eps    | undercut0.05|undercut0.05|theta0.00 |                 0.7026 |              0.6262 |
| midflip  | a0.00   | router_ucb    | undercut0.05|undercut0.05|theta1.00 |                 0.7054 |              0.6346 |
| midflip  | a0.25   | plmesp        | proposed|proposed|theta0.00         |                 0.6545 |              0.4583 |
| midflip  | a0.25   | mesp_scalar   | theta0.00|proposed|theta0.00        |                 0.685  |              0.113  |
| midflip  | a0.25   | router_greedy | theta0.90|theta0.95|theta0.95       |                 0.6528 |              0.6118 |
| midflip  | a0.25   | router_eps    | undercut0.05|undercut0.05|theta0.99 |                 0.7026 |              0.635  |
| midflip  | a0.25   | router_ucb    | undercut0.05|undercut0.05|theta1.00 |                 0.7054 |              0.6346 |
| midflip  | a0.50   | plmesp        | selective|proposed|theta0.00        |                 0.6545 |              0.3576 |
| midflip  | a0.50   | mesp_scalar   | theta0.00|proposed|theta0.00        |                 0.685  |              0.2446 |
| midflip  | a0.50   | router_greedy | theta0.90|theta0.95|theta0.95       |                 0.6528 |              0.6226 |
| midflip  | a0.50   | router_eps    | theta0.95|undercut0.05|theta0.99    |                 0.7026 |              0.6329 |
| midflip  | a0.50   | router_ucb    | theta0.99|undercut0.05|theta1.00    |                 0.7054 |              0.6357 |
| midflip  | a0.75   | plmesp        | selective|proposed|theta0.00        |                 0.6545 |              0.4613 |
| midflip  | a0.75   | mesp_scalar   | theta0.00|proposed|theta0.00        |                 0.685  |              0.378  |
| midflip  | a0.75   | router_greedy | theta0.75|theta0.75|theta0.90       |                 0.6528 |              0.6092 |
| midflip  | a0.75   | router_eps    | undercut0.0|undercut0.02|theta1.00  |                 0.7026 |              0.6017 |
| midflip  | a0.75   | router_ucb    | theta1.00|undercut0.05|theta1.00    |                 0.7054 |              0.6364 |
| midflip  | het     | plmesp        | selective|proposed|theta0.00        |                 0.6545 |              0.4321 |
| midflip  | het     | mesp_scalar   | theta0.00|proposed|theta0.00        |                 0.685  |              0.3727 |
| midflip  | het     | router_greedy | theta0.75|theta0.95|theta0.95       |                 0.6528 |              0.6183 |
| midflip  | het     | router_eps    | theta0.90|undercut0.05|theta0.99    |                 0.7026 |              0.6336 |
| midflip  | het     | router_ucb    | theta0.975|undercut0.05|theta1.00   |                 0.7054 |              0.6357 |

## 11c. THE FAIR STRATEGIC COMPARISON: best response over one rich option class for every rule

| mech          |   n_cells |   nonstrategic |   strategic |   degradation |   worst_degradation |   frac_fixed_point |
|:--------------|----------:|---------------:|------------:|--------------:|--------------------:|-------------------:|
| mesp_scalar   |        20 |         0.7089 |      0.249  |        0.4599 |              0.7737 |               1    |
| plmesp        |        20 |         0.6871 |      0.3593 |        0.3278 |              0.6646 |               0.6  |
| router_eps    |        20 |         0.7305 |      0.6516 |        0.079  |              0.216  |               0.35 |
| router_greedy |        20 |         0.6928 |      0.644  |        0.0487 |              0.1262 |               0.8  |
| router_ucb    |        20 |         0.7329 |      0.6792 |        0.0537 |              0.0718 |               0.95 |


Profile reached in each cell:

| triple   | alpha   | mech          | profile                             | is_fixed_point   |   nonstrategic_revenue |   strategic_revenue |
|:---------|:--------|:--------------|:------------------------------------|:-----------------|-----------------------:|--------------------:|
| dominant | a0.00   | mesp_scalar   | proposed|theta0.00|theta0.00        | True             |                 0.8028 |              0.0291 |
| dominant | a0.00   | plmesp        | proposed|theta0.00|theta0.00        | False            |                 0.7752 |              0.16   |
| dominant | a0.00   | router_eps    | undercut0.02|theta0.975|theta0.00   | True             |                 0.81   |              0.7393 |
| dominant | a0.00   | router_greedy | undercut0.05|theta0.99|theta0.25    | True             |                 0.797  |              0.7667 |
| dominant | a0.00   | router_ucb    | undercut0.05|theta1.00|theta0.975   | True             |                 0.8127 |              0.7728 |
| dominant | a0.25   | mesp_scalar   | proposed|theta0.00|theta0.00        | True             |                 0.8028 |              0.1604 |
| dominant | a0.25   | plmesp        | proposed|theta0.00|theta0.00        | False            |                 0.7752 |              0.274  |
| dominant | a0.25   | router_eps    | theta0.50|theta0.75|theta0.975      | False            |                 0.81   |              0.5939 |
| dominant | a0.25   | router_greedy | undercut0.05|theta1.00|theta0.00    | True             |                 0.797  |              0.7687 |
| dominant | a0.25   | router_ucb    | undercut0.05|theta1.00|theta1.00    | True             |                 0.8127 |              0.7727 |
| dominant | a0.50   | mesp_scalar   | proposed|theta0.00|theta0.00        | True             |                 0.8028 |              0.3356 |
| dominant | a0.50   | plmesp        | proposed|theta0.00|theta0.00        | False            |                 0.7752 |              0.4152 |
| dominant | a0.50   | router_eps    | undercut0.05|theta0.975|theta0.00   | False            |                 0.81   |              0.7672 |
| dominant | a0.50   | router_greedy | undercut0.05|theta0.99|theta0.90    | True             |                 0.797  |              0.7638 |
| dominant | a0.50   | router_ucb    | undercut0.05|theta1.00|theta0.99    | True             |                 0.8127 |              0.7726 |
| dominant | a0.75   | mesp_scalar   | proposed|theta0.00|theta0.00        | True             |                 0.8028 |              0.5108 |
| dominant | a0.75   | plmesp        | proposed|theta0.00|theta0.00        | True             |                 0.7752 |              0.557  |
| dominant | a0.75   | router_eps    | undercut0.05|theta1.00|theta0.00    | True             |                 0.81   |              0.7688 |
| dominant | a0.75   | router_greedy | undercut0.05|theta0.99|theta0.90    | True             |                 0.797  |              0.7658 |
| dominant | a0.75   | router_ucb    | undercut0.05|theta1.00|theta0.99    | True             |                 0.8127 |              0.7726 |
| dominant | het     | mesp_scalar   | proposed|theta0.00|theta0.00        | True             |                 0.8028 |              0.3772 |
| dominant | het     | plmesp        | proposed|theta0.00|theta0.00        | True             |                 0.7752 |              0.4536 |
| dominant | het     | router_eps    | undercut0.05|theta1.00|theta0.00    | False            |                 0.81   |              0.7692 |
| dominant | het     | router_greedy | theta0.975|theta0.99|theta0.75      | True             |                 0.797  |              0.7839 |
| dominant | het     | router_ucb    | undercut0.05|theta1.00|theta0.99    | True             |                 0.8127 |              0.7726 |
| highflip | a0.00   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.5461 |              0.0196 |
| highflip | a0.00   | plmesp        | selective|theta0.00|theta0.00       | False            |                 0.5691 |              0.2946 |
| highflip | a0.00   | router_eps    | undercut0.05|theta1.00|undercut0.02 | False            |                 0.6005 |              0.5589 |
| highflip | a0.00   | router_greedy | undercut0.0|theta1.00|undercut0.05  | True             |                 0.5771 |              0.5303 |
| highflip | a0.00   | router_ucb    | undercut0.05|theta1.00|undercut0.05 | True             |                 0.6002 |              0.5653 |
| highflip | a0.25   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.5461 |              0.1045 |
| highflip | a0.25   | plmesp        | proposed|theta0.00|theta0.50        | False            |                 0.5691 |              0.3345 |
| highflip | a0.25   | router_eps    | undercut0.05|theta1.00|undercut0.02 | False            |                 0.6005 |              0.5589 |
| highflip | a0.25   | router_greedy | undercut0.0|theta1.00|undercut0.05  | True             |                 0.5771 |              0.5303 |
| highflip | a0.25   | router_ucb    | undercut0.05|theta1.00|undercut0.05 | True             |                 0.6002 |              0.5653 |
| highflip | a0.50   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.5461 |              0.229  |
| highflip | a0.50   | plmesp        | proposed|theta0.00|theta0.25        | False            |                 0.5691 |              0.3489 |
| highflip | a0.50   | router_eps    | undercut0.05|theta0.99|undercut0.02 | False            |                 0.6005 |              0.5581 |
| highflip | a0.50   | router_greedy | undercut0.0|theta1.00|undercut0.05  | True             |                 0.5771 |              0.5303 |
| highflip | a0.50   | router_ucb    | undercut0.05|theta1.00|undercut0.05 | True             |                 0.6002 |              0.5653 |
| highflip | a0.75   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.5461 |              0.3514 |
| highflip | a0.75   | plmesp        | proposed|theta0.00|proposed         | True             |                 0.5691 |              0.4577 |
| highflip | a0.75   | router_eps    | undercut0.05|theta0.95|theta0.95    | False            |                 0.6005 |              0.5737 |
| highflip | a0.75   | router_greedy | theta0.75|theta0.99|undercut0.05    | True             |                 0.5771 |              0.5556 |
| highflip | a0.75   | router_ucb    | undercut0.05|theta1.00|theta0.975   | False            |                 0.6002 |              0.5744 |
| highflip | het     | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.5461 |              0.3661 |
| highflip | het     | plmesp        | proposed|theta0.00|proposed         | True             |                 0.5691 |              0.4651 |
| highflip | het     | router_eps    | undercut0.05|theta1.00|undercut0.02 | True             |                 0.6005 |              0.5589 |
| highflip | het     | router_greedy | undercut0.0|theta0.99|undercut0.05  | True             |                 0.5771 |              0.53   |
| highflip | het     | router_ucb    | undercut0.05|theta1.00|undercut0.05 | True             |                 0.6002 |              0.5653 |
| lowflip  | a0.00   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.8017 |              0.0291 |
| lowflip  | a0.00   | plmesp        | theta0.00|theta0.00|proposed        | True             |                 0.7497 |              0.0851 |
| lowflip  | a0.00   | router_eps    | theta0.95|theta0.75|theta0.75       | False            |                 0.809  |              0.6073 |
| lowflip  | a0.00   | router_greedy | theta1.00|theta0.975|theta0.75      | True             |                 0.7441 |              0.6179 |
| lowflip  | a0.00   | router_ucb    | theta0.99|theta1.00|undercut0.05    | True             |                 0.8132 |              0.7415 |
| lowflip  | a0.25   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.8017 |              0.1517 |
| lowflip  | a0.25   | plmesp        | theta0.00|theta0.00|theta0.00       | False            |                 0.7497 |              0.1874 |
| lowflip  | a0.25   | router_eps    | theta0.99|theta0.75|theta0.75       | False            |                 0.809  |              0.6584 |
| lowflip  | a0.25   | router_greedy | theta0.99|theta0.975|undercut0.02   | False            |                 0.7441 |              0.6659 |
| lowflip  | a0.25   | router_ucb    | theta0.99|theta1.00|undercut0.05    | True             |                 0.8132 |              0.7415 |
| lowflip  | a0.50   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.8017 |              0.3182 |
| lowflip  | a0.50   | plmesp        | theta0.00|theta0.00|proposed        | True             |                 0.7497 |              0.3527 |
| lowflip  | a0.50   | router_eps    | theta0.99|theta0.90|undercut0.02    | False            |                 0.809  |              0.7116 |
| lowflip  | a0.50   | router_greedy | theta0.99|theta0.99|theta0.50       | False            |                 0.7441 |              0.6213 |
| lowflip  | a0.50   | router_ucb    | theta1.00|theta1.00|undercut0.05    | True             |                 0.8132 |              0.7416 |
| lowflip  | a0.75   | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.8017 |              0.4844 |
| lowflip  | a0.75   | plmesp        | theta0.00|theta0.00|proposed        | True             |                 0.7497 |              0.5004 |
| lowflip  | a0.75   | router_eps    | theta0.00|theta0.99|undercut0.05    | True             |                 0.809  |              0.7389 |
| lowflip  | a0.75   | router_greedy | theta0.975|theta0.95|theta0.99      | True             |                 0.7441 |              0.7409 |
| lowflip  | a0.75   | router_ucb    | theta0.975|theta1.00|undercut0.05   | True             |                 0.8132 |              0.7415 |
| lowflip  | het     | mesp_scalar   | theta0.00|theta0.00|proposed        | True             |                 0.8017 |              0.3799 |
| lowflip  | het     | plmesp        | theta0.00|theta0.00|proposed        | True             |                 0.7497 |              0.4172 |
| lowflip  | het     | router_eps    | theta0.00|theta1.00|undercut0.05    | True             |                 0.809  |              0.7387 |
| lowflip  | het     | router_greedy | theta0.975|theta0.99|undercut0.02   | False            |                 0.7441 |              0.6684 |
| lowflip  | het     | router_ucb    | theta0.95|theta1.00|undercut0.05    | True             |                 0.8132 |              0.7415 |
| midflip  | a0.00   | mesp_scalar   | theta0.00|proposed|theta0.00        | True             |                 0.685  |              0.0249 |
| midflip  | a0.00   | plmesp        | selective|proposed|theta0.00        | True             |                 0.6545 |              0.1738 |
| midflip  | a0.00   | router_eps    | undercut0.05|undercut0.05|theta0.00 | False            |                 0.7026 |              0.6262 |
| midflip  | a0.00   | router_greedy | undercut0.0|undercut0.0|theta0.975  | True             |                 0.6528 |              0.5784 |
| midflip  | a0.00   | router_ucb    | undercut0.05|undercut0.05|theta1.00 | True             |                 0.7054 |              0.6346 |
| midflip  | a0.25   | mesp_scalar   | theta0.00|proposed|theta0.00        | True             |                 0.685  |              0.113  |
| midflip  | a0.25   | plmesp        | proposed|proposed|theta0.00         | False            |                 0.6545 |              0.4583 |
| midflip  | a0.25   | router_eps    | undercut0.05|undercut0.05|theta0.99 | False            |                 0.7026 |              0.635  |
| midflip  | a0.25   | router_greedy | theta0.90|theta0.95|theta0.95       | True             |                 0.6528 |              0.6118 |
| midflip  | a0.25   | router_ucb    | undercut0.05|undercut0.05|theta1.00 | True             |                 0.7054 |              0.6346 |
| midflip  | a0.50   | mesp_scalar   | theta0.00|proposed|theta0.00        | True             |                 0.685  |              0.2446 |
| midflip  | a0.50   | plmesp        | selective|proposed|theta0.00        | True             |                 0.6545 |              0.3576 |
| midflip  | a0.50   | router_eps    | theta0.95|undercut0.05|theta0.99    | True             |                 0.7026 |              0.6329 |
| midflip  | a0.50   | router_greedy | theta0.90|theta0.95|theta0.95       | True             |                 0.6528 |              0.6226 |
| midflip  | a0.50   | router_ucb    | theta0.99|undercut0.05|theta1.00    | True             |                 0.7054 |              0.6357 |
| midflip  | a0.75   | mesp_scalar   | theta0.00|proposed|theta0.00        | True             |                 0.685  |              0.378  |
| midflip  | a0.75   | plmesp        | selective|proposed|theta0.00        | True             |                 0.6545 |              0.4613 |
| midflip  | a0.75   | router_eps    | undercut0.0|undercut0.02|theta1.00  | False            |                 0.7026 |              0.6017 |
| midflip  | a0.75   | router_greedy | theta0.75|theta0.75|theta0.90       | False            |                 0.6528 |              0.6092 |
| midflip  | a0.75   | router_ucb    | theta1.00|undercut0.05|theta1.00    | True             |                 0.7054 |              0.6364 |
| midflip  | het     | mesp_scalar   | theta0.00|proposed|theta0.00        | True             |                 0.685  |              0.3727 |
| midflip  | het     | plmesp        | selective|proposed|theta0.00        | True             |                 0.6545 |              0.4321 |
| midflip  | het     | router_eps    | theta0.90|undercut0.05|theta0.99    | True             |                 0.7026 |              0.6336 |
| midflip  | het     | router_greedy | theta0.75|theta0.95|theta0.95       | True             |                 0.6528 |              0.6183 |
| midflip  | het     | router_ucb    | theta0.975|undercut0.05|theta1.00   | True             |                 0.7054 |              0.6357 |

## 14. BASELINE 1: the single-observation exclusion rule under our observation model

| rule                         |   L_elicit | empty_policy   |   n_cells |   revenue_per_round |   compliant_exclusions |   exclusions |   idle_fraction |   price_is_one_share |   price_is_zero_share |   second_cap |   honest_bench |
|:-----------------------------|-----------:|:---------------|----------:|--------------------:|-----------------------:|-------------:|----------------:|---------------------:|----------------------:|-------------:|---------------:|
| plmesp                       |         -1 | na             |        20 |              0.5995 |                  0     |        0     |          0      |             nan      |              nan      |       0.6367 |          0.236 |
| single_observation_exclusion |          1 | roundrobin     |        20 |              0.4695 |                  2.2   |        2.2   |          0      |               0.7333 |                0.2667 |       0.6367 |          0.236 |
| single_observation_exclusion |          1 | stop           |        20 |              0.0119 |                  2.2   |        2.2   |          0.7333 |               0.7333 |                0.2667 |       0.6367 |          0.236 |
| single_observation_exclusion |          2 | roundrobin     |        20 |              0.587  |                  2.825 |        2.825 |          0      |               0.3417 |                0.0583 |       0.6367 |          0.236 |
| single_observation_exclusion |          2 | stop           |        20 |              0.002  |                  2.825 |        2.825 |          0.9416 |               0.3417 |                0.0583 |       0.6367 |          0.236 |
| single_observation_exclusion |          5 | roundrobin     |        20 |              0.6189 |                  3     |        3     |          0      |               0.0583 |                0      |       0.6367 |          0.236 |
| single_observation_exclusion |          5 | stop           |        20 |              0      |                  3     |        3     |          0.9999 |               0.0583 |                0      |       0.6367 |          0.236 |
| single_observation_exclusion |         20 | roundrobin     |        20 |              0.6188 |                  3     |        3     |          0      |               0      |                0      |       0.6367 |          0.236 |
| single_observation_exclusion |         20 | stop           |        20 |              0.0001 |                  3     |        3     |          0.9998 |               0      |                0      |       0.6367 |          0.236 |
| single_observation_exclusion |        100 | roundrobin     |        20 |              0.6188 |                  3     |        3     |          0      |               0      |                0      |       0.6367 |          0.236 |
| single_observation_exclusion |        100 | stop           |        20 |              0.0006 |                  3     |        3     |          0.999  |               0      |                0      |       0.6367 |          0.236 |

## 15. Utility against effort, per arm role

| instance            | context   | sweep   | role      | rule          | agent                 |   own_capability |   own_intrinsic |   runner_up_capability |   announced_price |   peak_delivered_mean |   peak_utility |   utility_at_full_capability |   peak_minus_full_capability |   total_variation |   range |   n_grid |
|:--------------------|:----------|:--------|:----------|:--------------|:----------------------|-----------------:|----------------:|-----------------------:|------------------:|----------------------:|---------------:|-----------------------------:|-----------------------------:|------------------:|--------:|---------:|
| measured_unique_top | GSM8K     | all     | runner_up | mesp          | GPT-4                 |           0.6588 |          0.3294 |                 0.6588 |            0.6012 |                0.6588 |         0.199  |                       0.199  |                       0      |            0.1843 |  0.1714 |       61 |
| measured_unique_top | GSM8K     | all     | runner_up | router_eps    | GPT-4                 |           0.6588 |          0.3294 |                 0.6588 |            0.6014 |                0.6588 |         0.387  |                       0.387  |                       0      |            0.3844 |  0.3738 |       61 |
| measured_unique_top | GSM8K     | all     | runner_up | router_greedy | GPT-4                 |           0.6588 |          0.3294 |                 0.6588 |            0.6014 |                0.6423 |         0.6012 |                       0.5868 |                       0.0144 |            0.9497 |  0.3994 |       61 |
| measured_unique_top | GSM8K     | all     | runner_up | router_ucb    | GPT-4                 |           0.6588 |          0.3294 |                 0.6588 |            0.6014 |                0.6588 |         0.2685 |                       0.2685 |                       0      |            0.2725 |  0.2675 |       61 |
| measured_unique_top | GSM8K     | all     | third     | mesp          | Mistral-7B            |           0.4115 |          0.2058 |                 0.6588 |            0.6014 |                0.2058 |         0.0404 |                       0.0321 |                       0.0083 |            0.0083 |  0.0083 |       61 |
| measured_unique_top | GSM8K     | all     | third     | router_eps    | Mistral-7B            |           0.4115 |          0.2058 |                 0.6588 |            0.6014 |                0.2058 |         0.0167 |                       0.0133 |                       0.0034 |            0.0034 |  0.0034 |       61 |
| measured_unique_top | GSM8K     | all     | third     | router_greedy | Mistral-7B            |           0.4115 |          0.2058 |                 0.6588 |            0.6014 |                0.3121 |         0      |                       0      |                       0      |            0      |  0      |       61 |
| measured_unique_top | GSM8K     | all     | third     | router_ucb    | Mistral-7B            |           0.4115 |          0.2058 |                 0.6588 |            0.6014 |                0.4115 |         0.0013 |                       0.0013 |                       0      |            0.002  |  0.0008 |       61 |
| measured_unique_top | GSM8K     | all     | top       | mesp          | Claude-V2             |           0.6626 |          0.3313 |                 0.6588 |            0.6012 |                0.6626 |         0.4433 |                       0.4433 |                       0      |            0.4274 |  0.4151 |       61 |
| measured_unique_top | GSM8K     | all     | top       | router_eps    | Claude-V2             |           0.6626 |          0.3313 |                 0.6588 |            0.6014 |                0.6626 |         0.2716 |                       0.2716 |                       0      |            0.3215 |  0.2592 |       61 |
| measured_unique_top | GSM8K     | all     | top       | router_greedy | Claude-V2             |           0.6626 |          0.3313 |                 0.6588 |            0.6014 |                0.4141 |         0.2293 |                       0.0836 |                       0.1457 |            0.2693 |  0.1457 |       61 |
| measured_unique_top | GSM8K     | all     | top       | router_ucb    | Claude-V2             |           0.6626 |          0.3313 |                 0.6588 |            0.6014 |                0.6626 |         0.3998 |                       0.3998 |                       0      |            0.4006 |  0.3988 |       61 |
| measured_unique_top | GSM8K     | primary | runner_up | mesp          | GPT-4                 |           0.6588 |          0.3294 |                 0.6588 |            0.6014 |                0.5929 |         0.1889 |                       0.1744 |                       0.0145 |            0.6954 |  0.1112 |       61 |
| measured_unique_top | GSM8K     | primary | third     | mesp          | Mistral-7B            |           0.4115 |          0.2058 |                 0.6588 |            0.6014 |                0.2058 |         0.0321 |                       0.0321 |                       0      |            0      |  0      |       61 |
| measured_unique_top | GSM8K     | primary | top       | mesp          | Claude-V2             |           0.6626 |          0.3313 |                 0.6588 |            0.6014 |                0.5963 |         0.5114 |                       0.4677 |                       0.0437 |            0.6804 |  0.2351 |       61 |
| measured_unique_top | MMLU      | all     | runner_up | mesp          | Claude-V2             |           0.5731 |          0.2866 |                 0.5731 |            0.5171 |                0.2866 |         0.0404 |                       0.0288 |                       0.0116 |            0.0116 |  0.0116 |       61 |
| measured_unique_top | MMLU      | all     | runner_up | router_eps    | Claude-V2             |           0.5731 |          0.2866 |                 0.5731 |            0.5188 |                0.2866 |         0.0167 |                       0.0119 |                       0.0048 |            0.0048 |  0.0048 |       61 |
| measured_unique_top | MMLU      | all     | runner_up | router_greedy | Claude-V2             |           0.5731 |          0.2866 |                 0.5731 |            0.5188 |                0.2866 |         0.125  |                       0.0892 |                       0.0358 |            0.0358 |  0.0358 |       61 |
| measured_unique_top | MMLU      | all     | runner_up | router_ucb    | Claude-V2             |           0.5731 |          0.2866 |                 0.5731 |            0.5188 |                0.5636 |         0.0012 |                       0.0011 |                       0.0001 |            0.0018 |  0.0009 |       61 |
| measured_unique_top | MMLU      | all     | third     | mesp          | Mistral-7B            |           0.5227 |          0.2614 |                 0.5731 |            0.5188 |                0.2614 |         0.0404 |                       0.0299 |                       0.0106 |            0.0106 |  0.0106 |       61 |
| measured_unique_top | MMLU      | all     | third     | router_eps    | Mistral-7B            |           0.5227 |          0.2614 |                 0.5731 |            0.5188 |                0.2614 |         0.0167 |                       0.0123 |                       0.0044 |            0.0044 |  0.0044 |       61 |
| measured_unique_top | MMLU      | all     | third     | router_greedy | Mistral-7B            |           0.5227 |          0.2614 |                 0.5731 |            0.5188 |                0.4269 |         0.1043 |                       0.0923 |                       0.012  |            0.1163 |  0.1043 |       61 |
| measured_unique_top | MMLU      | all     | third     | router_ucb    | Mistral-7B            |           0.5227 |          0.2614 |                 0.5731 |            0.5188 |                0.5227 |         0.0009 |                       0.0009 |                       0      |            0.001  |  0.0006 |       61 |
| measured_unique_top | MMLU      | all     | top       | mesp          | GPT-4                 |           0.8252 |          0.4126 |                 0.5731 |            0.5171 |                0.5845 |         0.7611 |                       0.5399 |                       0.2212 |            0.9536 |  0.7266 |       61 |
| measured_unique_top | MMLU      | all     | top       | router_eps    | GPT-4                 |           0.8252 |          0.4126 |                 0.5731 |            0.5188 |                0.5914 |         0.7701 |                       0.5678 |                       0.2023 |            1.0914 |  0.7546 |       61 |
| measured_unique_top | MMLU      | all     | top       | router_greedy | GPT-4                 |           0.8252 |          0.4126 |                 0.5731 |            0.5188 |                0.6258 |         0.4917 |                       0.4406 |                       0.0511 |            0.9039 |  0.3666 |       61 |
| measured_unique_top | MMLU      | all     | top       | router_ucb    | GPT-4                 |           0.8252 |          0.4126 |                 0.5731 |            0.5188 |                0.6189 |         0.757  |                       0.5857 |                       0.1712 |            0.9266 |  0.7529 |       61 |
| measured_unique_top | MMLU      | primary | runner_up | mesp          | Claude-V2             |           0.5731 |          0.2866 |                 0.5731 |            0.5188 |                0.2866 |         0.0288 |                       0.0288 |                       0      |            0      |  0      |       61 |
| measured_unique_top | MMLU      | primary | third     | mesp          | Mistral-7B            |           0.5227 |          0.2614 |                 0.5731 |            0.5188 |                0.2614 |         0.0299 |                       0.0299 |                       0      |            0      |  0      |       61 |
| measured_unique_top | MMLU      | primary | top       | mesp          | GPT-4                 |           0.8252 |          0.4126 |                 0.5731 |            0.5188 |                0.5157 |         0.8118 |                       0.5399 |                       0.2719 |            0.5511 |  0.2792 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | runner_up | mesp          | Claude-V2 (duplicate) |           0.6626 |          0.3313 |                 0.6626 |            0.605  |                0.6626 |         0.4008 |                       0.4008 |                       0      |            0.3858 |  0.3731 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | runner_up | router_eps    | Claude-V2 (duplicate) |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.6626 |         0.4652 |                       0.4652 |                       0      |            0.4896 |  0.4559 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | runner_up | router_greedy | Claude-V2 (duplicate) |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.508  |         0.1029 |                       0.0836 |                       0.0193 |            0.2949 |  0.1029 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | runner_up | router_ucb    | Claude-V2 (duplicate) |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.6626 |         0.2365 |                       0.2365 |                       0      |            0.2373 |  0.2356 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | third     | mesp          | GPT-4                 |           0.6588 |          0.3294 |                 0.6626 |            0.6055 |                0.3294 |         0.0404 |                       0.0271 |                       0.0133 |            0.0133 |  0.0133 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | third     | router_eps    | GPT-4                 |           0.6588 |          0.3294 |                 0.6626 |            0.6055 |                0.6588 |         0.1064 |                       0.1064 |                       0      |            0.1073 |  0.0967 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | third     | router_greedy | GPT-4                 |           0.6588 |          0.3294 |                 0.6626 |            0.6055 |                0.6313 |         0.349  |                       0.3353 |                       0.0137 |            0.6427 |  0.349  |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | third     | router_ucb    | GPT-4                 |           0.6588 |          0.3294 |                 0.6626 |            0.6055 |                0.6588 |         0.1583 |                       0.1583 |                       0      |            0.1622 |  0.1573 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | top       | mesp          | Claude-V2             |           0.6626 |          0.3313 |                 0.6626 |            0.605  |                0.6626 |         0.2139 |                       0.2139 |                       0      |            0.1993 |  0.186  |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | top       | router_eps    | Claude-V2             |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.6571 |         0.0943 |                       0.0891 |                       0.0052 |            0.095  |  0.0855 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | top       | router_greedy | Claude-V2             |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.6626 |         0.2508 |                       0.2508 |                       0      |            0.8816 |  0.2507 |       61 |
| two_top_CONSTRUCTED | GSM8K     | all     | top       | router_ucb    | Claude-V2             |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.6626 |         0.2732 |                       0.2732 |                       0      |            0.2747 |  0.2723 |       61 |
| two_top_CONSTRUCTED | GSM8K     | primary | runner_up | mesp          | Claude-V2 (duplicate) |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.6018 |         0.4092 |                       0.3774 |                       0.0318 |            0.9703 |  0.2942 |       61 |
| two_top_CONSTRUCTED | GSM8K     | primary | third     | mesp          | GPT-4                 |           0.6588 |          0.3294 |                 0.6626 |            0.6055 |                0.3294 |         0.0271 |                       0.0271 |                       0      |            0      |  0      |       61 |
| two_top_CONSTRUCTED | GSM8K     | primary | top       | mesp          | Claude-V2             |           0.6626 |          0.3313 |                 0.6626 |            0.6055 |                0.5963 |         0.2581 |                       0.2373 |                       0.0208 |            0.4089 |  0.1669 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | runner_up | mesp          | GPT-4 (duplicate)     |           0.8252 |          0.4126 |                 0.8252 |            0.7676 |                0.8252 |         0.2289 |                       0.2289 |                       0      |            0.2207 |  0.2046 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | runner_up | router_eps    | GPT-4 (duplicate)     |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.8252 |         0.4573 |                       0.4573 |                       0      |            0.4706 |  0.4481 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | runner_up | router_greedy | GPT-4 (duplicate)     |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.7839 |         0.3143 |                       0.2937 |                       0.0206 |            0.5299 |  0.3143 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | runner_up | router_ucb    | GPT-4 (duplicate)     |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.8252 |         0.2963 |                       0.2963 |                       0      |            0.2987 |  0.2957 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | third     | mesp          | Claude-V2             |           0.5731 |          0.2866 |                 0.8252 |            0.767  |                0.2866 |         0.0404 |                       0.0288 |                       0.0116 |            0.0116 |  0.0116 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | third     | router_eps    | Claude-V2             |           0.5731 |          0.2866 |                 0.8252 |            0.767  |                0.2866 |         0.0124 |                       0.0089 |                       0.0036 |            0.0036 |  0.0036 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | third     | router_greedy | Claude-V2             |           0.5731 |          0.2866 |                 0.8252 |            0.767  |                0.5254 |         0      |                       0      |                       0      |            0      |  0      |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | third     | router_ucb    | Claude-V2             |           0.5731 |          0.2866 |                 0.8252 |            0.767  |                0.554  |         0.0013 |                       0.0012 |                       0.0001 |            0.0025 |  0.0009 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | top       | mesp          | GPT-4                 |           0.8252 |          0.4126 |                 0.8252 |            0.7676 |                0.8252 |         0.311  |                       0.311  |                       0      |            0.3028 |  0.2867 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | top       | router_eps    | GPT-4                 |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.8252 |         0.1155 |                       0.1155 |                       0      |            0.1394 |  0.1071 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | top       | router_greedy | GPT-4                 |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.7839 |         0.3143 |                       0.2937 |                       0.0206 |            0.7144 |  0.3143 |       61 |
| two_top_CONSTRUCTED | MMLU      | all     | top       | router_ucb    | GPT-4                 |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.8252 |         0.2917 |                       0.2917 |                       0      |            0.2941 |  0.291  |       61 |
| two_top_CONSTRUCTED | MMLU      | primary | runner_up | mesp          | GPT-4 (duplicate)     |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.7633 |         0.2279 |                       0.2084 |                       0.0195 |            0.7297 |  0.136  |       61 |
| two_top_CONSTRUCTED | MMLU      | primary | third     | mesp          | Claude-V2             |           0.5731 |          0.2866 |                 0.8252 |            0.767  |                0.2866 |         0.0288 |                       0.0288 |                       0      |            0      |  0      |       61 |
| two_top_CONSTRUCTED | MMLU      | primary | top       | mesp          | GPT-4                 |           0.8252 |          0.4126 |                 0.8252 |            0.767  |                0.7633 |         0.3639 |                       0.3315 |                       0.0324 |            0.5824 |  0.2046 |       61 |


Cross-check of the curve against the deviation code path:

| instance            | context   | role      | rule          | crosscheck_option   |   agent_utility_per_round |
|:--------------------|:----------|:----------|:--------------|:--------------------|--------------------------:|
| measured_unique_top | GSM8K     | runner_up | mesp          | undercut0.02        |                    0.1744 |
| measured_unique_top | GSM8K     | runner_up | mesp          | full_capability     |                    0.1744 |
| measured_unique_top | GSM8K     | runner_up | router_eps    | undercut0.02        |                    0.387  |
| measured_unique_top | GSM8K     | runner_up | router_eps    | full_capability     |                    0.387  |
| measured_unique_top | GSM8K     | runner_up | router_greedy | undercut0.02        |                    0.5868 |
| measured_unique_top | GSM8K     | runner_up | router_greedy | full_capability     |                    0.5868 |
| measured_unique_top | GSM8K     | runner_up | router_ucb    | undercut0.02        |                    0.2685 |
| measured_unique_top | GSM8K     | runner_up | router_ucb    | full_capability     |                    0.2685 |
| measured_unique_top | GSM8K     | third     | mesp          | undercut0.02        |                    0.0321 |
| measured_unique_top | GSM8K     | third     | mesp          | full_capability     |                    0.0321 |
| measured_unique_top | GSM8K     | third     | router_eps    | undercut0.02        |                    0.0133 |
| measured_unique_top | GSM8K     | third     | router_eps    | full_capability     |                    0.0133 |
| measured_unique_top | GSM8K     | third     | router_greedy | undercut0.02        |                    0      |
| measured_unique_top | GSM8K     | third     | router_greedy | full_capability     |                    0      |
| measured_unique_top | GSM8K     | third     | router_ucb    | undercut0.02        |                    0.0013 |
| measured_unique_top | GSM8K     | third     | router_ucb    | full_capability     |                    0.0013 |
| measured_unique_top | GSM8K     | top       | mesp          | undercut0.02        |                    0.4677 |
| measured_unique_top | GSM8K     | top       | mesp          | full_capability     |                    0.4677 |
| measured_unique_top | GSM8K     | top       | router_eps    | undercut0.02        |                    0.2716 |
| measured_unique_top | GSM8K     | top       | router_eps    | full_capability     |                    0.2716 |
| measured_unique_top | GSM8K     | top       | router_greedy | undercut0.02        |                    0.0836 |
| measured_unique_top | GSM8K     | top       | router_greedy | full_capability     |                    0.0836 |
| measured_unique_top | GSM8K     | top       | router_ucb    | undercut0.02        |                    0.3998 |
| measured_unique_top | GSM8K     | top       | router_ucb    | full_capability     |                    0.3998 |
| measured_unique_top | MMLU      | runner_up | mesp          | undercut0.02        |                    0.0288 |
| measured_unique_top | MMLU      | runner_up | mesp          | full_capability     |                    0.0288 |
| measured_unique_top | MMLU      | runner_up | router_eps    | undercut0.02        |                    0.0119 |
| measured_unique_top | MMLU      | runner_up | router_eps    | full_capability     |                    0.0119 |
| measured_unique_top | MMLU      | runner_up | router_greedy | undercut0.02        |                    0.0892 |
| measured_unique_top | MMLU      | runner_up | router_greedy | full_capability     |                    0.0892 |
| measured_unique_top | MMLU      | runner_up | router_ucb    | undercut0.02        |                    0.0011 |
| measured_unique_top | MMLU      | runner_up | router_ucb    | full_capability     |                    0.0011 |
| measured_unique_top | MMLU      | third     | mesp          | undercut0.02        |                    0.0299 |
| measured_unique_top | MMLU      | third     | mesp          | full_capability     |                    0.0299 |
| measured_unique_top | MMLU      | third     | router_eps    | undercut0.02        |                    0.0123 |
| measured_unique_top | MMLU      | third     | router_eps    | full_capability     |                    0.0123 |
| measured_unique_top | MMLU      | third     | router_greedy | undercut0.02        |                    0.0923 |
| measured_unique_top | MMLU      | third     | router_greedy | full_capability     |                    0.0923 |
| measured_unique_top | MMLU      | third     | router_ucb    | undercut0.02        |                    0.0009 |
| measured_unique_top | MMLU      | third     | router_ucb    | full_capability     |                    0.0009 |
| measured_unique_top | MMLU      | top       | mesp          | undercut0.02        |                    0.7532 |
| measured_unique_top | MMLU      | top       | mesp          | full_capability     |                    0.5399 |
| measured_unique_top | MMLU      | top       | router_eps    | undercut0.02        |                    0.6947 |
| measured_unique_top | MMLU      | top       | router_eps    | full_capability     |                    0.5678 |
| measured_unique_top | MMLU      | top       | router_greedy | undercut0.02        |                    0.3073 |
| measured_unique_top | MMLU      | top       | router_greedy | full_capability     |                    0.4406 |
| measured_unique_top | MMLU      | top       | router_ucb    | undercut0.02        |                    0.7157 |
| measured_unique_top | MMLU      | top       | router_ucb    | full_capability     |                    0.5857 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | mesp          | undercut0.02        |                    0.3774 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | mesp          | full_capability     |                    0.3774 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | router_eps    | undercut0.02        |                    0.4652 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | router_eps    | full_capability     |                    0.4652 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | router_greedy | undercut0.02        |                    0.0836 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | router_greedy | full_capability     |                    0.0836 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | router_ucb    | undercut0.02        |                    0.2365 |
| two_top_CONSTRUCTED | GSM8K     | runner_up | router_ucb    | full_capability     |                    0.2365 |
| two_top_CONSTRUCTED | GSM8K     | third     | mesp          | undercut0.02        |                    0.0271 |
| two_top_CONSTRUCTED | GSM8K     | third     | mesp          | full_capability     |                    0.0271 |
| two_top_CONSTRUCTED | GSM8K     | third     | router_eps    | undercut0.02        |                    0.1064 |
| two_top_CONSTRUCTED | GSM8K     | third     | router_eps    | full_capability     |                    0.1064 |
| two_top_CONSTRUCTED | GSM8K     | third     | router_greedy | undercut0.02        |                    0.3353 |
| two_top_CONSTRUCTED | GSM8K     | third     | router_greedy | full_capability     |                    0.3353 |
| two_top_CONSTRUCTED | GSM8K     | third     | router_ucb    | undercut0.02        |                    0.1583 |
| two_top_CONSTRUCTED | GSM8K     | third     | router_ucb    | full_capability     |                    0.1583 |
| two_top_CONSTRUCTED | GSM8K     | top       | mesp          | undercut0.02        |                    0.2373 |
| two_top_CONSTRUCTED | GSM8K     | top       | mesp          | full_capability     |                    0.2373 |
| two_top_CONSTRUCTED | GSM8K     | top       | router_eps    | undercut0.02        |                    0.0891 |
| two_top_CONSTRUCTED | GSM8K     | top       | router_eps    | full_capability     |                    0.0891 |
| two_top_CONSTRUCTED | GSM8K     | top       | router_greedy | undercut0.02        |                    0.2508 |
| two_top_CONSTRUCTED | GSM8K     | top       | router_greedy | full_capability     |                    0.2508 |
| two_top_CONSTRUCTED | GSM8K     | top       | router_ucb    | undercut0.02        |                    0.2732 |
| two_top_CONSTRUCTED | GSM8K     | top       | router_ucb    | full_capability     |                    0.2732 |
| two_top_CONSTRUCTED | MMLU      | runner_up | mesp          | undercut0.02        |                    0.2084 |
| two_top_CONSTRUCTED | MMLU      | runner_up | mesp          | full_capability     |                    0.2084 |
| two_top_CONSTRUCTED | MMLU      | runner_up | router_eps    | undercut0.02        |                    0.4573 |
| two_top_CONSTRUCTED | MMLU      | runner_up | router_eps    | full_capability     |                    0.4573 |
| two_top_CONSTRUCTED | MMLU      | runner_up | router_greedy | undercut0.02        |                    0.2937 |
| two_top_CONSTRUCTED | MMLU      | runner_up | router_greedy | full_capability     |                    0.2937 |
| two_top_CONSTRUCTED | MMLU      | runner_up | router_ucb    | undercut0.02        |                    0.2963 |
| two_top_CONSTRUCTED | MMLU      | runner_up | router_ucb    | full_capability     |                    0.2963 |
| two_top_CONSTRUCTED | MMLU      | third     | mesp          | undercut0.02        |                    0.0288 |
| two_top_CONSTRUCTED | MMLU      | third     | mesp          | full_capability     |                    0.0288 |
| two_top_CONSTRUCTED | MMLU      | third     | router_eps    | undercut0.02        |                    0.0089 |
| two_top_CONSTRUCTED | MMLU      | third     | router_eps    | full_capability     |                    0.0089 |
| two_top_CONSTRUCTED | MMLU      | third     | router_greedy | undercut0.02        |                    0      |
| two_top_CONSTRUCTED | MMLU      | third     | router_greedy | full_capability     |                    0      |
| two_top_CONSTRUCTED | MMLU      | third     | router_ucb    | undercut0.02        |                    0.0012 |
| two_top_CONSTRUCTED | MMLU      | third     | router_ucb    | full_capability     |                    0.0012 |
| two_top_CONSTRUCTED | MMLU      | top       | mesp          | undercut0.02        |                    0.3315 |
| two_top_CONSTRUCTED | MMLU      | top       | mesp          | full_capability     |                    0.3315 |
| two_top_CONSTRUCTED | MMLU      | top       | router_eps    | undercut0.02        |                    0.1155 |
| two_top_CONSTRUCTED | MMLU      | top       | router_eps    | full_capability     |                    0.1155 |
| two_top_CONSTRUCTED | MMLU      | top       | router_greedy | undercut0.02        |                    0.2937 |
| two_top_CONSTRUCTED | MMLU      | top       | router_greedy | full_capability     |                    0.2937 |
| two_top_CONSTRUCTED | MMLU      | top       | router_ucb    | undercut0.02        |                    0.2894 |
| two_top_CONSTRUCTED | MMLU      | top       | router_ucb    | full_capability     |                    0.2894 |

## 12b. The exact best response against each rule (fine shading and undercutting), best gain found

|                               |   a0.00 |   a0.25 |   a0.50 |   a0.75 |    het |
|:------------------------------|--------:|--------:|--------:|--------:|-------:|
| ('dominant', 'mesp_scalar')   |  0.0026 |  0.002  |  0.0013 |  0.0007 | 0.0013 |
| ('dominant', 'plmesp')        |  0.0083 |  0.0062 |  0.0041 |  0.0021 | 0.0041 |
| ('dominant', 'router_eps')    |  0.0341 |  0.0323 |  0.0306 |  0.0288 | 0.0327 |
| ('dominant', 'router_greedy') |  0.0199 |  0.0104 |  0.0228 |  0.0292 | 0.0125 |
| ('dominant', 'router_ucb')    |  0.0264 |  0.0193 |  0.0123 |  0.0053 | 0.0208 |
| ('highflip', 'mesp_scalar')   |  0.0019 |  0.0019 |  0.0019 |  0.0019 | 0.0019 |
| ('highflip', 'plmesp')        |  0.0058 |  0.0043 |  0.0029 |  0.0014 | 0.0012 |
| ('highflip', 'router_eps')    |  0.0213 |  0.0207 |  0.02   |  0.0194 | 0.02   |
| ('highflip', 'router_greedy') |  0.0169 |  0.013  |  0.0091 |  0.0073 | 0.0091 |
| ('highflip', 'router_ucb')    |  0.0149 |  0.0118 |  0.0087 |  0.0056 | 0.0087 |
| ('lowflip', 'mesp_scalar')    |  0.0025 |  0.0019 |  0.0012 |  0.0006 | 0.0012 |
| ('lowflip', 'plmesp')         |  0.0105 |  0.0079 |  0.0053 |  0.0026 | 0.004  |
| ('lowflip', 'router_eps')     |  0.0648 |  0.0601 |  0.0571 |  0.0541 | 0.0607 |
| ('lowflip', 'router_greedy')  |  0.0363 |  0.004  |  0.0007 |  0.0015 | 0.0105 |
| ('lowflip', 'router_ucb')     |  0.0578 |  0.0478 |  0.0377 |  0.0277 | 0.0498 |
| ('midflip', 'mesp_scalar')    |  0.002  |  0.0015 |  0.001  |  0.0005 | 0.001  |
| ('midflip', 'plmesp')         |  0.0058 |  0.0044 |  0.0029 |  0.0015 | 0.0029 |
| ('midflip', 'router_eps')     |  0.0646 |  0.0575 |  0.055  |  0.0525 | 0.058  |
| ('midflip', 'router_greedy')  |  0.0138 |  0.0445 |  0.0223 |  0.0265 | 0.0223 |
| ('midflip', 'router_ucb')     |  0.0496 |  0.041  |  0.0324 |  0.0238 | 0.0427 |


Revenue the platform loses at that deviation:

|                               |   a0.00 |   a0.25 |   a0.50 |   a0.75 |    het |
|:------------------------------|--------:|--------:|--------:|--------:|-------:|
| ('dominant', 'mesp_scalar')   |  0.0637 |  0.0465 |  0.0293 |  0.0133 | 0.0293 |
| ('dominant', 'plmesp')        |  0.0513 |  0.0382 |  0.0255 |  0.0127 | 0.0255 |
| ('dominant', 'router_eps')    |  0.038  |  0.038  |  0.038  |  0.038  | 0.038  |
| ('dominant', 'router_greedy') |  0.0537 |  0.0106 |  0.0066 |  0.0066 | 0.004  |
| ('dominant', 'router_ucb')    |  0.04   |  0.04   |  0.04   |  0.04   | 0.04   |
| ('highflip', 'mesp_scalar')   |  0.0039 |  0.0039 |  0.0039 |  0.0039 | 0.0039 |
| ('highflip', 'plmesp')        |  0.0153 |  0.0116 |  0.0079 |  0.0041 | 0.0033 |
| ('highflip', 'router_eps')    |  0.0232 |  0.0232 |  0.0232 |  0.0232 | 0.0232 |
| ('highflip', 'router_greedy') |  0.03   |  0.03   |  0.03   |  0.0073 | 0.03   |
| ('highflip', 'router_ucb')    |  0.0244 |  0.0244 |  0.0244 |  0.0244 | 0.0244 |
| ('lowflip', 'mesp_scalar')    |  0.0639 |  0.048  |  0.0316 |  0.0158 | 0.0316 |
| ('lowflip', 'plmesp')         |  0.0105 |  0.0079 |  0.0053 |  0.0026 | 0.0242 |
| ('lowflip', 'router_eps')     |  0.0983 |  0.0684 |  0.0684 |  0.0684 | 0.0684 |
| ('lowflip', 'router_greedy')  |  0.0813 |  0.0813 |  0.0007 |  0.0015 | 0.0813 |
| ('lowflip', 'router_ucb')     |  0.0717 |  0.0717 |  0.0717 |  0.0717 | 0.0717 |
| ('midflip', 'mesp_scalar')    |  0.0319 |  0.0312 |  0.0257 |  0.013  | 0.0257 |
| ('midflip', 'plmesp')         |  0.0166 |  0.0125 |  0.0083 |  0.0042 | 0.0083 |
| ('midflip', 'router_eps')     |  0.0889 |  0.066  |  0.066  |  0.066  | 0.066  |
| ('midflip', 'router_greedy')  |  0.0081 |  0.016  |  0.0081 |  0.0081 | 0.0081 |
| ('midflip', 'router_ucb')     |  0.0691 |  0.0691 |  0.0691 |  0.0691 | 0.0691 |

## 12b. The exact best response against each rule (fine shading and undercutting), best gain found

|                               |   a0.00 |   a0.25 |   a0.50 |   a0.75 |    het |
|:------------------------------|--------:|--------:|--------:|--------:|-------:|
| ('dominant', 'mesp_scalar')   |  0.0026 |  0.002  |  0.0013 |  0.0007 | 0.0013 |
| ('dominant', 'plmesp')        |  0.0083 |  0.0062 |  0.0041 |  0.0021 | 0.0041 |
| ('dominant', 'router_eps')    |  0.0341 |  0.0323 |  0.0306 |  0.0288 | 0.0327 |
| ('dominant', 'router_greedy') |  0.0199 |  0.0104 |  0.0228 |  0.0292 | 0.0125 |
| ('dominant', 'router_ucb')    |  0.0264 |  0.0193 |  0.0123 |  0.0053 | 0.0208 |
| ('highflip', 'mesp_scalar')   |  0.0019 |  0.0019 |  0.0019 |  0.0019 | 0.0019 |
| ('highflip', 'plmesp')        |  0.0058 |  0.0043 |  0.0029 |  0.0014 | 0.0012 |
| ('highflip', 'router_eps')    |  0.0213 |  0.0207 |  0.02   |  0.0194 | 0.02   |
| ('highflip', 'router_greedy') |  0.0169 |  0.013  |  0.0091 |  0.0073 | 0.0091 |
| ('highflip', 'router_ucb')    |  0.0149 |  0.0118 |  0.0087 |  0.0056 | 0.0087 |
| ('lowflip', 'mesp_scalar')    |  0.0025 |  0.0019 |  0.0012 |  0.0006 | 0.0012 |
| ('lowflip', 'plmesp')         |  0.0105 |  0.0079 |  0.0053 |  0.0026 | 0.004  |
| ('lowflip', 'router_eps')     |  0.0648 |  0.0601 |  0.0571 |  0.0541 | 0.0607 |
| ('lowflip', 'router_greedy')  |  0.0363 |  0.004  |  0.0007 |  0.0015 | 0.0105 |
| ('lowflip', 'router_ucb')     |  0.0578 |  0.0478 |  0.0377 |  0.0277 | 0.0498 |
| ('midflip', 'mesp_scalar')    |  0.002  |  0.0015 |  0.001  |  0.0005 | 0.001  |
| ('midflip', 'plmesp')         |  0.0058 |  0.0044 |  0.0029 |  0.0015 | 0.0029 |
| ('midflip', 'router_eps')     |  0.0646 |  0.0575 |  0.055  |  0.0525 | 0.058  |
| ('midflip', 'router_greedy')  |  0.0138 |  0.0445 |  0.0223 |  0.0265 | 0.0223 |
| ('midflip', 'router_ucb')     |  0.0496 |  0.041  |  0.0324 |  0.0238 | 0.0427 |


Revenue the platform loses at that deviation:

|                               |   a0.00 |   a0.25 |   a0.50 |   a0.75 |    het |
|:------------------------------|--------:|--------:|--------:|--------:|-------:|
| ('dominant', 'mesp_scalar')   |  0.0637 |  0.0465 |  0.0293 |  0.0133 | 0.0293 |
| ('dominant', 'plmesp')        |  0.0513 |  0.0382 |  0.0255 |  0.0127 | 0.0255 |
| ('dominant', 'router_eps')    |  0.038  |  0.038  |  0.038  |  0.038  | 0.038  |
| ('dominant', 'router_greedy') |  0.0537 |  0.0106 |  0.0066 |  0.0066 | 0.004  |
| ('dominant', 'router_ucb')    |  0.04   |  0.04   |  0.04   |  0.04   | 0.04   |
| ('highflip', 'mesp_scalar')   |  0.0039 |  0.0039 |  0.0039 |  0.0039 | 0.0039 |
| ('highflip', 'plmesp')        |  0.0153 |  0.0116 |  0.0079 |  0.0041 | 0.0033 |
| ('highflip', 'router_eps')    |  0.0232 |  0.0232 |  0.0232 |  0.0232 | 0.0232 |
| ('highflip', 'router_greedy') |  0.03   |  0.03   |  0.03   |  0.0073 | 0.03   |
| ('highflip', 'router_ucb')    |  0.0244 |  0.0244 |  0.0244 |  0.0244 | 0.0244 |
| ('lowflip', 'mesp_scalar')    |  0.0639 |  0.048  |  0.0316 |  0.0158 | 0.0316 |
| ('lowflip', 'plmesp')         |  0.0105 |  0.0079 |  0.0053 |  0.0026 | 0.0242 |
| ('lowflip', 'router_eps')     |  0.0983 |  0.0684 |  0.0684 |  0.0684 | 0.0684 |
| ('lowflip', 'router_greedy')  |  0.0813 |  0.0813 |  0.0007 |  0.0015 | 0.0813 |
| ('lowflip', 'router_ucb')     |  0.0717 |  0.0717 |  0.0717 |  0.0717 | 0.0717 |
| ('midflip', 'mesp_scalar')    |  0.0319 |  0.0312 |  0.0257 |  0.013  | 0.0257 |
| ('midflip', 'plmesp')         |  0.0166 |  0.0125 |  0.0083 |  0.0042 | 0.0083 |
| ('midflip', 'router_eps')     |  0.0889 |  0.066  |  0.066  |  0.066  | 0.066  |
| ('midflip', 'router_greedy')  |  0.0081 |  0.016  |  0.0081 |  0.0081 | 0.0081 |
| ('midflip', 'router_ucb')     |  0.0691 |  0.0691 |  0.0691 |  0.0691 | 0.0691 |

## 12c. THE SAME DEVIATION APPLIED TO EVERY RULE: undercut the pointwise runner-up

| mech          |   mean_gain |   max_gain |   mean_revenue_loss |   max_revenue_loss |   mean_revenue_after |   mean_revenue_before |   n_cells |
|:--------------|------------:|-----------:|--------------------:|-------------------:|---------------------:|----------------------:|----------:|
| mesp_scalar   |      0.0006 |     0.0019 |              0.0011 |             0.0039 |               0.577  |                0.5781 |        20 |
| plmesp        |      0      |     0.0001 |              0      |             0.0001 |               0.5997 |                0.5998 |        20 |
| router_eps    |      0.0422 |     0.0648 |              0.0516 |             0.0983 |               0.6788 |                0.7304 |        20 |
| router_greedy |      0.0097 |     0.0363 |              0.0315 |             0.0813 |               0.6647 |                0.6962 |        20 |
| router_ucb    |      0.0272 |     0.0578 |              0.0513 |             0.0717 |               0.6816 |                0.7329 |        20 |

## 7c. The most two-top-like subset at each size

| context_set   |   K | models                                                                                                                  |   mean_top_gap |   mass_within_0.01 |   mass_within_0.05 |   mass_within_0.10 |
|:--------------|----:|:------------------------------------------------------------------------------------------------------------------------|---------------:|-------------------:|-------------------:|-------------------:|
| Q3            |   2 | CodeLlama-34B|Mistral-7B                                                                                                |         0.0185 |             0.4453 |             1      |             1      |
| Q3            |   3 | Claude-Instant-V1|GPT-3.5|Mixtral-8x7B                                                                                  |         0.022  |             0      |             1      |             1      |
| Q3            |   4 | Claude-V1|Claude-V2|GPT-3.5|Mixtral-8x7B                                                                                |         0.0214 |             0      |             1      |             1      |
| Q3            |   5 | Claude-Instant-V1|Claude-V1|Claude-V2|GPT-3.5|Mixtral-8x7B                                                              |         0.0214 |             0      |             1      |             1      |
| Q3            |   6 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Mixtral-8x7B                                                |         0.0214 |             0      |             1      |             1      |
| Q3            |   7 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Llama-70B|Mixtral-8x7B                                      |         0.0214 |             0      |             1      |             1      |
| Q3            |   8 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B                           |         0.0214 |             0      |             1      |             1      |
| Q3            |   9 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B|WizardLM-13B              |         0.0214 |             0      |             1      |             1      |
| Q3            |  10 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B|WizardLM-13B|Yi-34B       |         0.0351 |             0      |             0.6816 |             1      |
| Q3            |  11 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|GPT-4|Llama-70B|Mistral-7B|Mixtral-8x7B|WizardLM-13B|Yi-34B |         0.0545 |             0.2363 |             0.5547 |             0.5547 |
| Q7            |   2 | CodeLlama-34B|Mistral-7B                                                                                                |         0.0199 |             0.4481 |             0.9877 |             0.9877 |
| Q7            |   3 | Claude-Instant-V1|GPT-3.5|Mixtral-8x7B                                                                                  |         0.0229 |             0      |             1      |             1      |
| Q7            |   4 | Claude-Instant-V1|CodeLlama-34B|GPT-3.5|Mixtral-8x7B                                                                    |         0.0229 |             0      |             1      |             1      |
| Q7            |   5 | Claude-Instant-V1|CodeLlama-34B|GPT-3.5|Llama-70B|Mixtral-8x7B                                                          |         0.0229 |             0      |             1      |             1      |
| Q7            |   6 | Claude-Instant-V1|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B                                               |         0.0229 |             0      |             1      |             1      |
| Q7            |   7 | Claude-Instant-V1|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B|WizardLM-13B                                  |         0.0229 |             0      |             1      |             1      |
| Q7            |   8 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B                           |         0.0232 |             0      |             0.9581 |             1      |
| Q7            |   9 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B|WizardLM-13B              |         0.0232 |             0      |             0.9581 |             1      |
| Q7            |  10 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|Llama-70B|Mistral-7B|Mixtral-8x7B|WizardLM-13B|Yi-34B       |         0.0349 |             0.0419 |             0.6747 |             1      |
| Q7            |  11 | Claude-Instant-V1|Claude-V1|Claude-V2|CodeLlama-34B|GPT-3.5|GPT-4|Llama-70B|Mistral-7B|Mixtral-8x7B|WizardLM-13B|Yi-34B |         0.0558 |             0.2143 |             0.5573 |             0.5573 |

## 16. The capability-gap sweep: is the two-top condition a cliff or a transition?

| mech        |   delta |     s_n |   sd_of_bid_difference |   equilibrium_revenue |   revenue_at_proposed |   announced_price_mean |   runner_up_curve_total_variation |   second_cap |   honest_bench |   oracle | equilibrium_profile               | is_fixed_point   |
|:------------|--------:|--------:|-----------------------:|----------------------:|----------------------:|-----------------------:|----------------------------------:|-------------:|---------------:|---------:|:----------------------------------|:-----------------|
| mesp_scalar |  0      | 0.04941 |                0.00684 |               0.37429 |               0.79297 |              nan       |                           0.49723 |      0.81664 |        0.25431 |  0.81664 | theta0.00|proposed|theta0.00      | False            |
| mesp_scalar |  0.001  | 0.04941 |                0.00684 |               0.37425 |               0.79238 |              nan       |                           0.43983 |      0.81564 |        0.25431 |  0.81664 | theta0.00|proposed|theta0.00      | False            |
| mesp_scalar |  0.002  | 0.04941 |                0.00684 |               0.79603 |               0.7921  |              nan       |                           0.37537 |      0.81464 |        0.25431 |  0.81664 | theta1.00|theta1.00|theta0.00     | True             |
| mesp_scalar |  0.005  | 0.04941 |                0.00684 |               0.79601 |               0.79024 |              nan       |                           0.14252 |      0.81164 |        0.25431 |  0.81664 | theta1.00|theta1.00|theta0.00     | True             |
| mesp_scalar |  0.0075 | 0.04941 |                0.00684 |               0.77962 |               0.78864 |              nan       |                           0       |      0.80914 |        0.25431 |  0.81664 | undercut0.005|theta0.00|theta0.00 | False            |
| mesp_scalar |  0.01   | 0.04941 |                0.00684 |               0.77725 |               0.78727 |              nan       |                           0       |      0.80664 |        0.25431 |  0.81664 | undercut0.005|theta0.00|theta0.00 | False            |
| mesp_scalar |  0.015  | 0.04941 |                0.00684 |               0.77802 |               0.78495 |              nan       |                           0       |      0.80164 |        0.25431 |  0.81664 | theta0.99|theta0.00|theta0.00     | False            |
| mesp_scalar |  0.02   | 0.04941 |                0.00684 |               0.78066 |               0.78282 |              nan       |                           0       |      0.79664 |        0.25431 |  0.81664 | undercut0.005|theta1.00|theta0.00 | False            |
| mesp_scalar |  0.03   | 0.04941 |                0.00684 |               0.76258 |               0.77514 |              nan       |                           0       |      0.78664 |        0.25431 |  0.81664 | theta0.95|theta0.00|theta0.00     | False            |
| mesp_scalar |  0.05   | 0.04941 |                0.00684 |               0.74326 |               0.74505 |              nan       |                           0       |      0.76664 |        0.25431 |  0.81664 | theta0.90|theta0.00|theta0.00     | False            |
| mesp_scalar |  0.1    | 0.04941 |                0.00684 |               0.32879 |               0.66737 |              nan       |                           0       |      0.71664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| mesp_scalar |  0.2    | 0.04941 |                0.00684 |               0.28275 |               0.57648 |              nan       |                           0       |      0.61664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| mesp_scalar |  0.4    | 0.04941 |                0.00684 |               0.22836 |               0.47175 |              nan       |                           0       |      0.50862 |        0.20832 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0      | 0.04941 |                0.00684 |               0.72787 |               0.75411 |                0.74398 |                           0.11967 |      0.81664 |        0.25431 |  0.81664 | proposed|proposed|theta0.00       | True             |
| plmesp      |  0.001  | 0.04941 |                0.00684 |               0.72735 |               0.75359 |                0.74329 |                           0.10608 |      0.81564 |        0.25431 |  0.81664 | proposed|proposed|theta0.00       | True             |
| plmesp      |  0.002  | 0.04941 |                0.00684 |               0.72678 |               0.75302 |                0.74254 |                           0.09112 |      0.81464 |        0.25431 |  0.81664 | proposed|proposed|theta0.00       | True             |
| plmesp      |  0.005  | 0.04941 |                0.00684 |               0.7251  |               0.75134 |                0.74019 |                           0.09129 |      0.81164 |        0.25431 |  0.81664 | proposed|proposed|theta0.00       | True             |
| plmesp      |  0.0055 | 0.04941 |                0.00684 |               0.72482 |               0.75106 |                0.7398  |                           0.08683 |      0.81114 |        0.25431 |  0.81664 | proposed|proposed|theta0.00       | True             |
| plmesp      |  0.006  | 0.04941 |                0.00684 |               0.7245  |               0.75073 |                0.73934 |                           0.08747 |      0.81064 |        0.25431 |  0.81664 | proposed|proposed|theta0.00       | True             |
| plmesp      |  0.0065 | 0.04941 |                0.00684 |               0.4405  |               0.75045 |                0.73894 |                           0.04232 |      0.81014 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.0068 | 0.04941 |                0.00684 |               0.4404  |               0.75025 |                0.73865 |                           0.04106 |      0.80984 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.007  | 0.04941 |                0.00684 |               0.44034 |               0.75009 |                0.73842 |                           0.04381 |      0.80964 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.0072 | 0.04941 |                0.00684 |               0.44028 |               0.74995 |                0.73821 |                           0.04357 |      0.80944 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.0075 | 0.04941 |                0.00684 |               0.44018 |               0.74974 |                0.73792 |                           0.04358 |      0.80914 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.01   | 0.04941 |                0.00684 |               0.43933 |               0.74799 |                0.73543 |                           0.04503 |      0.80664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.015  | 0.04941 |                0.00684 |               0.43767 |               0.74438 |                0.73021 |                           0       |      0.80164 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.02   | 0.04941 |                0.00684 |               0.43598 |               0.74098 |                0.72538 |                           0       |      0.79664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.03   | 0.04941 |                0.00684 |               0.43247 |               0.73398 |                0.71531 |                           0       |      0.78664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.05   | 0.04941 |                0.00684 |               0.42548 |               0.72023 |                0.69573 |                           0       |      0.76664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | False            |
| plmesp      |  0.1    | 0.04941 |                0.00684 |               0.40801 |               0.68533 |                0.64577 |                           0       |      0.71664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | False            |
| plmesp      |  0.2    | 0.04941 |                0.00684 |               0.37321 |               0.61552 |                0.54617 |                           0       |      0.61664 |        0.25431 |  0.81664 | proposed|theta0.00|theta0.00      | True             |
| plmesp      |  0.4    | 0.04941 |                0.00684 |               0.32899 |               0.52741 |                0.44218 |                           0       |      0.50862 |        0.20832 |  0.81664 | proposed|theta0.00|theta0.00      | True             |

## 17. BASELINE 3: the Second-Best Utility Guarantee Mechanism (WWW 2026), reimplemented from the paper

| setting    | mech        | deviation         |   n_cells |   revenue_per_round |   monitor_fire_rate |   compliant_conviction_rate |   undelegated_fraction |   post_fire_revenue_per_round |   detection_delay |   price_above_cap_mass |   second_cap |   honest_bench |
|:-----------|:------------|:------------------|----------:|--------------------:|--------------------:|----------------------------:|-----------------------:|------------------------------:|------------------:|-----------------------:|-------------:|---------------:|
| contextual | mesp_scalar | proposed          |        11 |              0.5783 |              0.2727 |                      0.2727 |                      0 |                        0.6513 |           83575.8 |                 0.1201 |       0.6008 |         0.1894 |
| contextual | plmesp      | proposed          |        11 |              0.5797 |              0      |                      0      |                      0 |                      nan      |             nan   |                 0      |       0.6008 |         0.1894 |
| contextual | second_best | proposed          |        11 |              0.613  |              0      |                      0      |                      0 |                      nan      |             nan   |                 0.2363 |       0.6008 |         0.1894 |
| contextual | second_best | their_equilibrium |        11 |              0.4889 |              0      |                      0      |                      0 |                      nan      |             nan   |                 0.2363 |       0.6008 |         0.1894 |
| scalar     | mesp_scalar | proposed          |        40 |              0.5519 |              0      |                      0      |                      0 |                      nan      |             nan   |                 0      |       0.5954 |         0.226  |
| scalar     | second_best | proposed          |        40 |              0.6056 |              0      |                      0      |                      0 |                      nan      |             nan   |                 0      |       0.5954 |         0.226  |
| scalar     | second_best | their_equilibrium |        40 |              0.449  |              0      |                      0      |                      0 |                      nan      |             nan   |                 0      |       0.5954 |         0.226  |


Against a bait and switch, which is what the no-reallocation behaviour exposes:

| setting    | mech        | gate_blind2   |   n_cells |   revenue_per_round |   monitor_fire_rate |   detection_delay |   post_fire_revenue_per_round |   undelegated_fraction |
|:-----------|:------------|:--------------|----------:|--------------------:|--------------------:|------------------:|------------------------------:|-----------------------:|
| contextual | mesp_scalar | False         |        36 |              0.6114 |              0.5028 |          44636.4  |                        0.6773 |                 0      |
| contextual | mesp_scalar | True          |        36 |              0.6114 |              0.5028 |          44636.4  |                        0.6773 |                 0      |
| contextual | plmesp      | False         |        33 |              0.6065 |              0.4424 |           4039.78 |                        0.6234 |                 0      |
| contextual | plmesp      | True          |        33 |              0.6075 |              0.4424 |           1717.25 |                        0.6248 |                 0      |
| contextual | second_best | False         |        42 |              0.4968 |              0.2857 |           4483    |                        0      |                 0.1925 |
| contextual | second_best | True          |        39 |              0.4467 |              0.2821 |           4483    |                        0      |                 0.2652 |
| scalar     | mesp_scalar | False         |       120 |              0.5892 |              0.31   |          14267.4  |                        0.6872 |                 0      |
| scalar     | mesp_scalar | True          |       120 |              0.5892 |              0.31   |          14267.4  |                        0.6872 |                 0      |
| scalar     | second_best | False         |       120 |              0.4891 |              0.3038 |           4754.86 |                        0      |                 0.1885 |
| scalar     | second_best | True          |       120 |              0.4302 |              0.3038 |           4754.86 |                        0      |                 0.2855 |

## 13b. Monitor FRONTIER at alpha = a0.25: false conviction of a compliant winner against detection delay

| monitor          | params                                     |   false_conviction_rate |   detect_rate_baitswitch |   median_delay_baitswitch |   p90_delay_baitswitch |   detect_rate_mild |   median_delay_mild | alpha   |   reps |      n |
|:-----------------|:-------------------------------------------|------------------------:|-------------------------:|--------------------------:|-----------------------:|-------------------:|--------------------:|:--------|-------:|-------:|
| anytime          | {"boundary_mult": 0.5}                     |                  0      |                        1 |                      48   |                   68.1 |              1     |               176   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.2, "burnin": 100}             |                  0      |                        1 |                     100   |                  100   |              0.685 |               102   | a0.25   |    300 | 300000 |
| anytime          | {"boundary_mult": 1.0}                     |                  0      |                        1 |                     199   |                  238.2 |              1     |               797.5 | a0.25   |    300 | 300000 |
| anytime          | {"boundary_mult": 2.0}                     |                  0      |                        1 |                     806.5 |                  886   |              1     |              3201.5 | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.05, "burnin": 1000}           |                  0      |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.1, "burnin": 1000}            |                  0      |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.2, "burnin": 1000}            |                  0      |                        1 |                    1000   |                 1000   |              0.18  |              1011.5 | a0.25   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 1e-06}  |                  0      |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.02, "burnin": 10000}          |                  0      |                        1 |                   10000   |                10000   |              1     |             10000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.05, "burnin": 10000}          |                  0      |                        1 |                   10000   |                10000   |              1     |             10000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.1, "burnin": 10000}           |                  0      |                        1 |                   10000   |                10000   |              1     |             10000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.2, "burnin": 10000}           |                  0      |                        1 |                   10000   |                10000   |              0     |               nan   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.02, "burnin": null}           |                  0      |                        1 |                   12819   |                12819   |              1     |             12819   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.05, "burnin": null}           |                  0      |                        1 |                   12819   |                12819   |              1     |             12819   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.1, "burnin": null}            |                  0      |                        1 |                   12819   |                12819   |              1     |             12819   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.2, "burnin": null}            |                  0      |                        1 |                   12819   |                12819   |              0     |               nan   | a0.25   |    300 | 300000 |
| none             | {}                                         |                  0      |                        0 |                     nan   |                  nan   |              0     |               nan   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 1e-06}   |                  0.0033 |                        1 |                     200   |                  200   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.01, "burnin": null}           |                  0.015  |                        1 |                   12819   |                12819   |              1     |             12819   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 1e-06}    |                  0.0233 |                        1 |                     150   |                  400   |              1     |              7300   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 0.0001} |                  0.0233 |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.1, "burnin": 100}             |                  0.025  |                        1 |                     100   |                  100   |              1     |               100   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.01, "burnin": 10000}          |                  0.03   |                        1 |                   10000   |                10000   |              1     |             10000   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 0.0001}  |                  0.1333 |                        1 |                     200   |                  200   |              1     |               400   | a0.25   |    300 | 300000 |
| anytime          | {"boundary_mult": 0.25}                    |                  0.18   |                        1 |                      10   |                   21   |              1     |                31   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.02, "burnin": 1000}           |                  0.215  |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.005, "burnin": null}          |                  0.275  |                        1 |                   12819   |                12819   |              1     |             12819   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.005, "burnin": 10000}         |                  0.34   |                        1 |                   10000   |                10000   |              1     |             10000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.05, "burnin": 100}            |                  0.365  |                        1 |                     100   |                  100   |              1     |               100   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.01, "burnin": 1000}           |                  0.555  |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 0.0001}   |                  0.69   |                        1 |                      50   |                  150   |              1     |               800   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.02, "burnin": 100}            |                  0.72   |                        1 |                     100   |                  100   |              1     |               100   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.005, "burnin": 1000}          |                  0.78   |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.01, "burnin": 100}            |                  0.88   |                        1 |                     100   |                  100   |              1     |               100   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 0.01}   |                  0.93   |                        1 |                    1000   |                 1000   |              1     |              1000   | a0.25   |    300 | 300000 |
| fixedbuffer      | {"buffer": 0.005, "burnin": 100}           |                  0.96   |                        1 |                     100   |                  100   |              1     |               100   | a0.25   |    300 | 300000 |
| anytime_noslack  | {}                                         |                  1      |                        1 |                       1   |                    2   |              1     |                 1   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 0.01}     |                  1      |                        1 |                      50   |                   50   |              1     |               100   | a0.25   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 0.01}    |                  1      |                        1 |                     200   |                  200   |              1     |               200   | a0.25   |    300 | 300000 |
| twosample_elicit | {"batch": 200, "twosample_alpha": 0.0001}  |                  1      |                        1 |                     200   |                  200   |              1     |               200   | a0.25   |    300 | 300000 |

## 13b. Monitor FRONTIER at alpha = a0.50: false conviction of a compliant winner against detection delay

| monitor          | params                                     |   false_conviction_rate |   detect_rate_baitswitch |   median_delay_baitswitch |   p90_delay_baitswitch |   detect_rate_mild |   median_delay_mild | alpha   |   reps |      n |
|:-----------------|:-------------------------------------------|------------------------:|-------------------------:|--------------------------:|-----------------------:|-------------------:|--------------------:|:--------|-------:|-------:|
| anytime          | {"boundary_mult": 0.5}                     |                  0      |                        1 |                     162   |                  245.1 |             1      |               646   | a0.50   |    300 | 300000 |
| anytime          | {"boundary_mult": 1.0}                     |                  0      |                        1 |                     709   |                  868.1 |             1      |              2827.5 | a0.50   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 1e-06}  |                  0      |                        1 |                    1000   |                 1000   |             1      |              2000   | a0.50   |    300 | 300000 |
| anytime          | {"boundary_mult": 2.0}                     |                  0      |                        1 |                    2905.5 |                 3323.4 |             1      |             11576   | a0.50   |    300 | 300000 |
| none             | {}                                         |                  0      |                        0 |                     nan   |                  nan   |             0      |               nan   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 1e-06}   |                  0.0033 |                        1 |                     800   |                 2200   |             0.9733 |             54100   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 0.0001} |                  0.0233 |                        1 |                    1000   |                 1000   |             1      |              1000   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 1e-06}    |                  0.0233 |                        1 |                    6300   |                18960   |             0.7967 |             78000   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 0.0001}  |                  0.1333 |                        1 |                     200   |                  600   |             1      |              3700   | a0.50   |    300 | 300000 |
| anytime          | {"boundary_mult": 0.25}                    |                  0.18   |                        1 |                      31   |                   79.1 |             1      |               112   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 0.0001}   |                  0.69   |                        1 |                     650   |                 2100   |             1      |              6750   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 0.01}   |                  0.93   |                        1 |                    1000   |                 1000   |             1      |              1000   | a0.50   |    300 | 300000 |
| anytime_noslack  | {}                                         |                  1      |                        1 |                       1   |                    4   |             1      |                 1   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 0.01}     |                  1      |                        1 |                     100   |                  300   |             1      |               400   | a0.50   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 0.01}    |                  1      |                        1 |                     200   |                  200   |             1      |               400   | a0.50   |    300 | 300000 |
| twosample_elicit | {"batch": 200, "twosample_alpha": 0.0001}  |                  1      |                        1 |                     200   |                  200   |             1      |               200   | a0.50   |    300 | 300000 |

## 13b. Monitor FRONTIER at alpha = a0.75: false conviction of a compliant winner against detection delay

| monitor          | params                                     |   false_conviction_rate |   detect_rate_baitswitch |   median_delay_baitswitch |   p90_delay_baitswitch |   detect_rate_mild |   median_delay_mild | alpha   |   reps |      n |
|:-----------------|:-------------------------------------------|------------------------:|-------------------------:|--------------------------:|-----------------------:|-------------------:|--------------------:|:--------|-------:|-------:|
| anytime          | {"boundary_mult": 0.5}                     |                  0      |                   1      |                   14354   |                29917.8 |             0.99   |             58222   | a0.75   |    300 | 300000 |
| anytime          | {"boundary_mult": 1.0}                     |                  0      |                   0.9933 |                   63509   |               116766   |             0.5167 |            188342   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 1e-06}  |                  0      |                   0.0167 |                  137000   |               196000   |             0      |               nan   | a0.75   |    300 | 300000 |
| anytime          | {"boundary_mult": 2.0}                     |                  0      |                   0.4833 |                  189461   |               245463   |             0.0033 |            241945   | a0.75   |    300 | 300000 |
| none             | {}                                         |                  0      |                   0      |                     nan   |                  nan   |             0      |               nan   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 1e-06}   |                  0.0033 |                   0.0167 |                   98800   |               163000   |             0.0033 |              3400   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 0.0001} |                  0.0233 |                   0.5167 |                   99000   |               225800   |             0.15   |            137000   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 1e-06}    |                  0.0233 |                   0.0633 |                  108850   |               222430   |             0.0467 |            107450   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 0.0001}  |                  0.1333 |                   0.5467 |                  124400   |               240440   |             0.3233 |            124800   | a0.75   |    300 | 300000 |
| anytime          | {"boundary_mult": 0.25}                    |                  0.18   |                   1      |                    2344.5 |                 8870.2 |             1      |              9773.5 | a0.75   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 0.0001}   |                  0.69   |                   0.9333 |                   52925   |               171985   |             0.8367 |             71150   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 1000, "twosample_alpha": 0.01}   |                  0.93   |                   1      |                    8500   |                28100   |             1      |             23500   | a0.75   |    300 | 300000 |
| anytime_noslack  | {}                                         |                  1      |                   1      |                       1   |                   20.2 |             1      |                 2   | a0.75   |    300 | 300000 |
| twosample_elicit | {"batch": 200, "twosample_alpha": 0.0001}  |                  1      |                   1      |                     200   |                  400   |             1      |               200   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 50, "twosample_alpha": 0.01}     |                  1      |                   1      |                    1900   |                 6455   |             1      |              2400   | a0.75   |    300 | 300000 |
| twosample        | {"batch": 200, "twosample_alpha": 0.01}    |                  1      |                   1      |                    6400   |                18420   |             1      |              9400   | a0.75   |    300 | 300000 |

## 13. Monitor ladder, alpha = a0.25

|                                                                   |   ('conviction_rate', 'baitswitch') |   ('conviction_rate', 'baitswitch_mild') |   ('conviction_rate', 'compliant') |   ('conviction_rate', 'shade0.05') |   ('conviction_rate', 'shade0.10') |   ('conviction_rate', 'shade0.19') |   ('median_delay', 'baitswitch') |   ('median_delay', 'baitswitch_mild') |   ('median_delay', 'compliant') |   ('median_delay', 'shade0.05') |   ('median_delay', 'shade0.10') |   ('median_delay', 'shade0.19') |
|:------------------------------------------------------------------|------------------------------------:|-----------------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|---------------------------------:|--------------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|
| ('anytime', '{"boundary_mult": 0.25}')                            |                                   1 |                                    1     |                              0.18  |                              1     |                              1     |                              1     |                             10   |                                  31   |                          1829   |                           356.5 |                           103.5 |                            28   |
| ('anytime', '{"boundary_mult": 0.5}')                             |                                   1 |                                    1     |                              0     |                              1     |                              1     |                              1     |                             48   |                                 176   |                           nan   |                          2341   |                           563.5 |                           155.5 |
| ('anytime', '{"boundary_mult": 1.0}')                             |                                   1 |                                    1     |                              0     |                              1     |                              1     |                              1     |                            199   |                                 797.5 |                           nan   |                          9915   |                          2520   |                           689   |
| ('anytime', '{"boundary_mult": 2.0}')                             |                                   1 |                                    1     |                              0     |                              1     |                              1     |                              1     |                            806.5 |                                3201.5 |                           nan   |                         40220   |                         10022   |                          2809.5 |
| ('anytime_noslack', '{}')                                         |                                   1 |                                    1     |                              1     |                              1     |                              1     |                              1     |                              1   |                                   1   |                             2   |                             1   |                             1   |                             1   |
| ('fixedbuffer', '{"buffer": 0.005, "burnin": 10000}')             |                                   1 |                                    1     |                              0.34  |                              1     |                              1     |                              1     |                          10000   |                               10000   |                         10000   |                         10000   |                         10000   |                         10000   |
| ('fixedbuffer', '{"buffer": 0.005, "burnin": 1000}')              |                                   1 |                                    1     |                              0.78  |                              1     |                              1     |                              1     |                           1000   |                                1000   |                          1000   |                          1000   |                          1000   |                          1000   |
| ('fixedbuffer', '{"buffer": 0.005, "burnin": 100}')               |                                   1 |                                    1     |                              0.96  |                              1     |                              1     |                              1     |                            100   |                                 100   |                           100   |                           100   |                           100   |                           100   |
| ('fixedbuffer', '{"buffer": 0.005, "burnin": null}')              |                                   1 |                                    1     |                              0.275 |                              1     |                              1     |                              1     |                          12819   |                               12819   |                         12819   |                         12819   |                         12819   |                         12819   |
| ('fixedbuffer', '{"buffer": 0.01, "burnin": 10000}')              |                                   1 |                                    1     |                              0.03  |                              1     |                              1     |                              1     |                          10000   |                               10000   |                         10000   |                         10000   |                         10000   |                         10000   |
| ('fixedbuffer', '{"buffer": 0.01, "burnin": 1000}')               |                                   1 |                                    1     |                              0.555 |                              1     |                              1     |                              1     |                           1000   |                                1000   |                          1005   |                          1000   |                          1000   |                          1000   |
| ('fixedbuffer', '{"buffer": 0.01, "burnin": 100}')                |                                   1 |                                    1     |                              0.88  |                              1     |                              1     |                              1     |                            100   |                                 100   |                           101.5 |                           100   |                           100   |                           100   |
| ('fixedbuffer', '{"buffer": 0.01, "burnin": null}')               |                                   1 |                                    1     |                              0.015 |                              1     |                              1     |                              1     |                          12819   |                               12819   |                         12819   |                         12819   |                         12819   |                         12819   |
| ('fixedbuffer', '{"buffer": 0.02, "burnin": 10000}')              |                                   1 |                                    1     |                              0     |                              1     |                              1     |                              1     |                          10000   |                               10000   |                           nan   |                         10000   |                         10000   |                         10000   |
| ('fixedbuffer', '{"buffer": 0.02, "burnin": 1000}')               |                                   1 |                                    1     |                              0.215 |                              1     |                              1     |                              1     |                           1000   |                                1000   |                          1017   |                          1000   |                          1000   |                          1000   |
| ('fixedbuffer', '{"buffer": 0.02, "burnin": 100}')                |                                   1 |                                    1     |                              0.72  |                              1     |                              1     |                              1     |                            100   |                                 100   |                           100   |                           100   |                           100   |                           100   |
| ('fixedbuffer', '{"buffer": 0.02, "burnin": null}')               |                                   1 |                                    1     |                              0     |                              1     |                              1     |                              1     |                          12819   |                               12819   |                           nan   |                         12819   |                         12819   |                         12819   |
| ('fixedbuffer', '{"buffer": 0.05, "burnin": 10000}')              |                                   1 |                                    1     |                              0     |                              0.96  |                              1     |                              1     |                          10000   |                               10000   |                           nan   |                         10000   |                         10000   |                         10000   |
| ('fixedbuffer', '{"buffer": 0.05, "burnin": 1000}')               |                                   1 |                                    1     |                              0     |                              0.995 |                              1     |                              1     |                           1000   |                                1000   |                           nan   |                          1000   |                          1000   |                          1000   |
| ('fixedbuffer', '{"buffer": 0.05, "burnin": 100}')                |                                   1 |                                    1     |                              0.365 |                              1     |                              1     |                              1     |                            100   |                                 100   |                           100   |                           100   |                           100   |                           100   |
| ('fixedbuffer', '{"buffer": 0.05, "burnin": null}')               |                                   1 |                                    1     |                              0     |                              0.955 |                              1     |                              1     |                          12819   |                               12819   |                           nan   |                         12819   |                         12819   |                         12819   |
| ('fixedbuffer', '{"buffer": 0.1, "burnin": 10000}')               |                                   1 |                                    1     |                              0     |                              0     |                              0.955 |                              1     |                          10000   |                               10000   |                           nan   |                           nan   |                         10000   |                         10000   |
| ('fixedbuffer', '{"buffer": 0.1, "burnin": 1000}')                |                                   1 |                                    1     |                              0     |                              0     |                              0.98  |                              1     |                           1000   |                                1000   |                           nan   |                           nan   |                          1000   |                          1000   |
| ('fixedbuffer', '{"buffer": 0.1, "burnin": 100}')                 |                                   1 |                                    1     |                              0.025 |                              0.36  |                              1     |                              1     |                            100   |                                 100   |                           100   |                           100   |                           100   |                           100   |
| ('fixedbuffer', '{"buffer": 0.1, "burnin": null}')                |                                   1 |                                    1     |                              0     |                              0     |                              0.955 |                              1     |                          12819   |                               12819   |                           nan   |                           nan   |                         12819   |                         12819   |
| ('fixedbuffer', '{"buffer": 0.2, "burnin": 10000}')               |                                   1 |                                    0     |                              0     |                              0     |                              0     |                              0.02  |                          10000   |                                 nan   |                           nan   |                           nan   |                           nan   |                         10000   |
| ('fixedbuffer', '{"buffer": 0.2, "burnin": 1000}')                |                                   1 |                                    0.18  |                              0     |                              0     |                              0     |                              0.525 |                           1000   |                                1011.5 |                           nan   |                           nan   |                           nan   |                          1000   |
| ('fixedbuffer', '{"buffer": 0.2, "burnin": 100}')                 |                                   1 |                                    0.685 |                              0     |                              0     |                              0.015 |                              0.875 |                            100   |                                 102   |                           nan   |                           nan   |                           100   |                           100   |
| ('fixedbuffer', '{"buffer": 0.2, "burnin": null}')                |                                   1 |                                    0     |                              0     |                              0     |                              0     |                              0.01  |                          12819   |                                 nan   |                           nan   |                           nan   |                           nan   |                         12819   |
| ('none', '{}')                                                    |                                   0 |                                    0     |                              0     |                              0     |                              0     |                              0     |                            nan   |                                 nan   |                           nan   |                           nan   |                           nan   |                           nan   |
| ('twosample', '{"batch": 1000, "twosample_alpha": 0.0001}')       |                                   1 |                                    1     |                              0.023 |                              1     |                              1     |                              1     |                           1000   |                                1000   |                        108000   |                         11000   |                          1000   |                          1000   |
| ('twosample', '{"batch": 1000, "twosample_alpha": 0.01}')         |                                   1 |                                    1     |                              0.93  |                              1     |                              1     |                              1     |                           1000   |                                1000   |                         66000   |                          1000   |                          1000   |                          1000   |
| ('twosample', '{"batch": 1000, "twosample_alpha": 1e-06}')        |                                   1 |                                    1     |                              0     |                              0.79  |                              1     |                              1     |                           1000   |                                1000   |                           nan   |                         78000   |                          2000   |                          1000   |
| ('twosample', '{"batch": 200, "twosample_alpha": 0.0001}')        |                                   1 |                                    1     |                              0.133 |                              0.995 |                              1     |                              1     |                            200   |                                 400   |                        102700   |                         33800   |                          2700   |                           200   |
| ('twosample', '{"batch": 200, "twosample_alpha": 0.01}')          |                                   1 |                                    1     |                              1     |                              1     |                              1     |                              1     |                            200   |                                 200   |                         17200   |                          1400   |                           400   |                           200   |
| ('twosample', '{"batch": 200, "twosample_alpha": 1e-06}')         |                                   1 |                                    1     |                              0.003 |                              0.18  |                              0.99  |                              1     |                            200   |                                1000   |                          3400   |                        134400   |                         43500   |                           600   |
| ('twosample', '{"batch": 50, "twosample_alpha": 0.0001}')         |                                   1 |                                    1     |                              0.69  |                              0.995 |                              1     |                              1     |                             50   |                                 800   |                         85950   |                         24950   |                          6150   |                           650   |
| ('twosample', '{"batch": 50, "twosample_alpha": 0.01}')           |                                   1 |                                    1     |                              1     |                              1     |                              1     |                              1     |                             50   |                                 100   |                          3200   |                           850   |                           350   |                           100   |
| ('twosample', '{"batch": 50, "twosample_alpha": 1e-06}')          |                                   1 |                                    1     |                              0.023 |                              0.315 |                              0.845 |                              1     |                            150   |                                7300   |                        108850   |                        122150   |                         76500   |                          5500   |
| ('twosample_elicit', '{"batch": 200, "twosample_alpha": 0.0001}') |                                   1 |                                    1     |                              1     |                              1     |                              1     |                              1     |                            200   |                                 200   |                           200   |                           200   |                           200   |                           200   |

## 13. Monitor ladder, alpha = a0.50

|                                                                   |   ('conviction_rate', 'baitswitch') |   ('conviction_rate', 'baitswitch_mild') |   ('conviction_rate', 'compliant') |   ('median_delay', 'baitswitch') |   ('median_delay', 'baitswitch_mild') |   ('median_delay', 'compliant') |
|:------------------------------------------------------------------|------------------------------------:|-----------------------------------------:|-----------------------------------:|---------------------------------:|--------------------------------------:|--------------------------------:|
| ('anytime', '{"boundary_mult": 0.25}')                            |                                   1 |                                    1     |                              0.18  |                             31   |                                 112   |                            1829 |
| ('anytime', '{"boundary_mult": 0.5}')                             |                                   1 |                                    1     |                              0     |                            162   |                                 646   |                             nan |
| ('anytime', '{"boundary_mult": 1.0}')                             |                                   1 |                                    1     |                              0     |                            709   |                                2827.5 |                             nan |
| ('anytime', '{"boundary_mult": 2.0}')                             |                                   1 |                                    1     |                              0     |                           2905.5 |                               11576   |                             nan |
| ('anytime_noslack', '{}')                                         |                                   1 |                                    1     |                              1     |                              1   |                                   1   |                               2 |
| ('none', '{}')                                                    |                                   0 |                                    0     |                              0     |                            nan   |                                 nan   |                             nan |
| ('twosample', '{"batch": 1000, "twosample_alpha": 0.0001}')       |                                   1 |                                    1     |                              0.023 |                           1000   |                                1000   |                          108000 |
| ('twosample', '{"batch": 1000, "twosample_alpha": 0.01}')         |                                   1 |                                    1     |                              0.93  |                           1000   |                                1000   |                           66000 |
| ('twosample', '{"batch": 1000, "twosample_alpha": 1e-06}')        |                                   1 |                                    1     |                              0     |                           1000   |                                2000   |                             nan |
| ('twosample', '{"batch": 200, "twosample_alpha": 0.0001}')        |                                   1 |                                    1     |                              0.133 |                            200   |                                3700   |                          102700 |
| ('twosample', '{"batch": 200, "twosample_alpha": 0.01}')          |                                   1 |                                    1     |                              1     |                            200   |                                 400   |                           17200 |
| ('twosample', '{"batch": 200, "twosample_alpha": 1e-06}')         |                                   1 |                                    0.973 |                              0.003 |                            800   |                               54100   |                            3400 |
| ('twosample', '{"batch": 50, "twosample_alpha": 0.0001}')         |                                   1 |                                    1     |                              0.69  |                            650   |                                6750   |                           85950 |
| ('twosample', '{"batch": 50, "twosample_alpha": 0.01}')           |                                   1 |                                    1     |                              1     |                            100   |                                 400   |                            3200 |
| ('twosample', '{"batch": 50, "twosample_alpha": 1e-06}')          |                                   1 |                                    0.797 |                              0.023 |                           6300   |                               78000   |                          108850 |
| ('twosample_elicit', '{"batch": 200, "twosample_alpha": 0.0001}') |                                   1 |                                    1     |                              1     |                            200   |                                 200   |                             200 |

## 13. Monitor ladder, alpha = a0.75

|                                                                   |   ('conviction_rate', 'baitswitch') |   ('conviction_rate', 'baitswitch_mild') |   ('conviction_rate', 'compliant') |   ('median_delay', 'baitswitch') |   ('median_delay', 'baitswitch_mild') |   ('median_delay', 'compliant') |
|:------------------------------------------------------------------|------------------------------------:|-----------------------------------------:|-----------------------------------:|---------------------------------:|--------------------------------------:|--------------------------------:|
| ('anytime', '{"boundary_mult": 0.25}')                            |                               1     |                                    1     |                              0.18  |                           2344.5 |                                9773.5 |                            1829 |
| ('anytime', '{"boundary_mult": 0.5}')                             |                               1     |                                    0.99  |                              0     |                          14354   |                               58222   |                             nan |
| ('anytime', '{"boundary_mult": 1.0}')                             |                               0.993 |                                    0.517 |                              0     |                          63509   |                              188342   |                             nan |
| ('anytime', '{"boundary_mult": 2.0}')                             |                               0.483 |                                    0.003 |                              0     |                         189461   |                              241945   |                             nan |
| ('anytime_noslack', '{}')                                         |                               1     |                                    1     |                              1     |                              1   |                                   2   |                               2 |
| ('none', '{}')                                                    |                               0     |                                    0     |                              0     |                            nan   |                                 nan   |                             nan |
| ('twosample', '{"batch": 1000, "twosample_alpha": 0.0001}')       |                               0.517 |                                    0.15  |                              0.023 |                          99000   |                              137000   |                          108000 |
| ('twosample', '{"batch": 1000, "twosample_alpha": 0.01}')         |                               1     |                                    1     |                              0.93  |                           8500   |                               23500   |                           66000 |
| ('twosample', '{"batch": 1000, "twosample_alpha": 1e-06}')        |                               0.017 |                                    0     |                              0     |                         137000   |                                 nan   |                             nan |
| ('twosample', '{"batch": 200, "twosample_alpha": 0.0001}')        |                               0.547 |                                    0.323 |                              0.133 |                         124400   |                              124800   |                          102700 |
| ('twosample', '{"batch": 200, "twosample_alpha": 0.01}')          |                               1     |                                    1     |                              1     |                           6400   |                                9400   |                           17200 |
| ('twosample', '{"batch": 200, "twosample_alpha": 1e-06}')         |                               0.017 |                                    0.003 |                              0.003 |                          98800   |                                3400   |                            3400 |
| ('twosample', '{"batch": 50, "twosample_alpha": 0.0001}')         |                               0.933 |                                    0.837 |                              0.69  |                          52925   |                               71150   |                           85950 |
| ('twosample', '{"batch": 50, "twosample_alpha": 0.01}')           |                               1     |                                    1     |                              1     |                           1900   |                                2400   |                            3200 |
| ('twosample', '{"batch": 50, "twosample_alpha": 1e-06}')          |                               0.063 |                                    0.047 |                              0.023 |                         108850   |                              107450   |                          108850 |
| ('twosample_elicit', '{"batch": 200, "twosample_alpha": 0.0001}') |                               1     |                                    1     |                              1     |                            200   |                                 200   |                             200 |
