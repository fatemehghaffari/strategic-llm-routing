
### Checks: the scalars the prose quotes, recomputed

* exact cells computed: 144; families ['heterogeneous', 'regime_switch', 'replicated_K2_unique', 'replicated_near_gap', 'replicated_tied_top', 'replicated_unique_top', 'rotating_top', 'unbalanced_unique_top']; horizons [np.int64(2000), np.int64(8000), np.int64(20000), np.int64(50000)]; Q [np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(7), np.int64(8)]; K [np.int64(2), np.int64(3)]
* valid comparable cells (all profiles finish bidding and 4 s_n <= delta): 57
* certified UB / published constant over those: 0.105 to 0.540; LB / constant: 0.075 to 0.540
* cells where the certified interval exceeds the constant: 0 (upper end), 0 (lower end)
* certified LB / Proposition 6.1 deviation: 2.65 to 38.65 over 60 cells in 7 families
* the certified upper bound per round decreases in Q at 0 step(s) where not both cells are fully truncated, and at 17 step(s) where both are (largest drop 0.008325 per round)
* replicated_unique_top: fully truncated cells give 0.3000 to 0.3015 per round against M_i / K = 0.3000
* replicated_tied_top: fully truncated cells give 0.2667 to 0.2680 per round against M_i / K = 0.2667
* replicated_K2_unique: fully truncated cells give 0.4500 to 0.4513 per round against M_i / K = 0.4500
* regime sweep: 74 horizon-by-K cells; completion and below-2n thresholds agree in 74 and differ in 0; the monitor threshold differs from completion in 5
* B slack below n in 27 of 144 cells; C slack below n in 25
* in those cells the exact revenue deficit per round is -0.0429 to 0.1430 against a slack of 0.4125 to 0.9781
### Certified intervals, cells in which every profile finishes bidding and the theorem's
### non-top condition 4 s_n <= delta holds

valid comparable cells: 57 of 144 computed
certified UPPER bound as a fraction of the published constant: 0.105 to 0.540
certified LOWER bound as a fraction of the published constant: 0.075 to 0.540
cells in which the certified upper bound exceeds the published constant: 0
cells in which the certified lower bound exceeds the published constant: 0
maximum dropped Stage-1 count mass over all cells: 7.592e-13
cells with a zero-width certified interval (the optimum never reaches a fallback): 62 of 144


#### heterogeneous

| family        |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| heterogeneous |  2000 |   1 |   326 |      1022 |                      0 |                           1 |                 0.1064 |                 0.1409 |                       0.4649 |                 0.303  |                      1 |
| heterogeneous |  2000 |   2 |   326 |        22 |                      0 |                           0 |                 0.236  |                 0.236  |                       6.881  |                 0.0343 |                      0 |
| heterogeneous |  2000 |   3 |   326 |         0 |                      3 |                           0 |                 0.2506 |                 0.2506 |                       7.2256 |                 0.0347 |                      0 |
| heterogeneous |  2000 |   4 |   326 |         0 |                      4 |                           0 |                 0.2505 |                 0.2505 |                     138.91   |                 0.0018 |                      0 |
| heterogeneous |  2000 |   5 |   326 |         0 |                      5 |                           0 |                 0.2512 |                 0.2512 |                      41.9797 |                 0.006  |                      0 |
| heterogeneous |  2000 |   6 |   326 |         0 |                      6 |                           0 |                 0.25   |                 0.25   |                    3212.49   |                 0.0001 |                      0 |
| heterogeneous |  8000 |   1 |   862 |      5414 |                      0 |                           1 |                 0.071  |                 0.0893 |                       0.2653 |                 0.3366 |                      1 |
| heterogeneous |  8000 |   2 |   862 |      1414 |                      0 |                           2 |                 0.1171 |                 0.1349 |                       2.4307 |                 0.0555 |                      0 |
| heterogeneous |  8000 |   3 |   862 |        80 |                      0 |                           1 |                 0.2299 |                 0.2299 |                       2.6308 |                 0.0874 |                      0 |
| heterogeneous |  8000 |   4 |   862 |         0 |                      4 |                           0 |                 0.2501 |                 0.2501 |                      41.8567 |                 0.006  |                      0 |
| heterogeneous |  8000 |   5 |   862 |         0 |                      5 |                           0 |                 0.2503 |                 0.2503 |                      13.393  |                 0.0187 |                      0 |
| heterogeneous |  8000 |   6 |   862 |         0 |                      6 |                           0 |                 0.2503 |                 0.2503 |                     935.96   |                 0.0003 |                      0 |
| heterogeneous | 20000 |   1 |  1634 |     15098 |                      0 |                           1 |                 0.0526 |                 0.0645 |                       0.1841 |                 0.3505 |                      1 |
| heterogeneous | 20000 |   2 |  1634 |      5098 |                      0 |                           2 |                 0.0904 |                 0.1022 |                       1.279  |                 0.0799 |                      0 |
| heterogeneous | 20000 |   3 |  1634 |      1764 |                      0 |                           3 |                 0.1002 |                 0.1182 |                       1.4197 |                 0.0832 |                      0 |
| heterogeneous | 20000 |   4 |  1634 |        98 |                      0 |                           3 |                 0.2391 |                 0.2391 |                      19.0424 |                 0.0126 |                      0 |
| heterogeneous | 20000 |   5 |  1634 |         0 |                      5 |                           0 |                 0.2501 |                 0.2501 |                       6.4526 |                 0.0388 |                      0 |
| heterogeneous | 20000 |   6 |  1634 |         0 |                      6 |                           0 |                 0.25   |                 0.25   |                     410.835  |                 0.0006 |                      0 |

#### regime_switch

| family        |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| regime_switch |  2000 |   2 |   326 |        22 |                      0 |                           0 |                 0.2058 |                 0.2058 |                       0.8265 |                 0.249  |                      1 |
| regime_switch |  2000 |   4 |   326 |         0 |                      4 |                           0 |                 0.2254 |                 0.2254 |                       1.507  |                 0.1496 |                      1 |
| regime_switch |  2000 |   6 |   326 |         0 |                      6 |                           0 |                 0.225  |                 0.225  |                       2.1634 |                 0.104  |                      1 |
| regime_switch |  8000 |   2 |   862 |      1414 |                      0 |                           2 |                 0.0471 |                 0.0778 |                       0.4745 |                 0.164  |                      1 |
| regime_switch |  8000 |   4 |   862 |         0 |                      4 |                           0 |                 0.2251 |                 0.2251 |                       0.8698 |                 0.2588 |                      1 |
| regime_switch |  8000 |   6 |   862 |         0 |                      6 |                           0 |                 0.2253 |                 0.2253 |                       1.252  |                 0.1799 |                      1 |
| regime_switch | 20000 |   2 |  1634 |      5098 |                      0 |                           2 |                 0.0348 |                 0.0584 |                       0.331  |                 0.1764 |                      1 |
| regime_switch | 20000 |   4 |  1634 |        98 |                      0 |                           2 |                 0.2091 |                 0.2091 |                       0.6093 |                 0.3431 |                      1 |
| regime_switch | 20000 |   6 |  1634 |         0 |                      6 |                           0 |                 0.225  |                 0.225  |                       0.8791 |                 0.256  |                      1 |
| regime_switch | 50000 |   2 |  3092 |     15724 |                      0 |                           2 |                 0.0265 |                 0.0417 |                       0.232  |                 0.1799 |                      1 |
| regime_switch | 50000 |   4 |  3092 |      3224 |                      0 |                           4 |                 0.0816 |                 0.0963 |                       0.4293 |                 0.2244 |                      1 |
| regime_switch | 50000 |   6 |  3092 |         0 |                      6 |                           0 |                 0.225  |                 0.225  |                       0.6208 |                 0.3625 |                      1 |

#### replicated_K2_unique

| family               |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| replicated_K2_unique |  2000 |   1 |   326 |      1348 |                      0 |                           1 |                 0.1    |                 0.1223 |                       0.4202 |                 0.2911 |                      1 |
| replicated_K2_unique |  2000 |   2 |   326 |       348 |                      0 |                           2 |                 0.1322 |                 0.1747 |                       0.7371 |                 0.237  |                      1 |
| replicated_K2_unique |  2000 |   3 |   326 |        14 |                      0 |                           0 |                 0.4253 |                 0.4253 |                       1.037  |                 0.4101 |                      1 |
| replicated_K2_unique |  2000 |   4 |   326 |         0 |                      4 |                           0 |                 0.45   |                 0.45   |                       1.3282 |                 0.3388 |                      1 |
| replicated_K2_unique |  2000 |   5 |   326 |         0 |                      5 |                           0 |                 0.45   |                 0.45   |                       1.6137 |                 0.2789 |                      1 |
| replicated_K2_unique |  2000 |   6 |   326 |         0 |                      6 |                           0 |                 0.4513 |                 0.4513 |                       1.8952 |                 0.2382 |                      1 |
| replicated_K2_unique |  2000 |   7 |   326 |         0 |                      7 |                           0 |                 0.45   |                 0.45   |                       2.0326 |                 0.2214 |                      1 |
| replicated_K2_unique |  2000 |   8 |   326 |         0 |                      8 |                           0 |                 0.45   |                 0.45   |                       2.1457 |                 0.2097 |                      1 |
| replicated_K2_unique |  8000 |   1 |   862 |      6276 |                      0 |                           1 |                 0.0635 |                 0.0754 |                       0.2434 |                 0.3097 |                      1 |
| replicated_K2_unique |  8000 |   2 |   862 |      2276 |                      0 |                           2 |                 0.0943 |                 0.1177 |                       0.4308 |                 0.2732 |                      1 |
| replicated_K2_unique |  8000 |   3 |   862 |       942 |                      0 |                           3 |                 0.1156 |                 0.1499 |                       0.6089 |                 0.2461 |                      1 |
| replicated_K2_unique |  8000 |   4 |   862 |       276 |                      0 |                           4 |                 0.3055 |                 0.3055 |                       0.7823 |                 0.3905 |                      1 |
| replicated_K2_unique |  8000 |   5 |   862 |         0 |                      5 |                           0 |                 0.45   |                 0.45   |                       0.9526 |                 0.4724 |                      1 |
| replicated_K2_unique |  8000 |   6 |   862 |         0 |                      6 |                           0 |                 0.4503 |                 0.4503 |                       1.1207 |                 0.4018 |                      1 |
| replicated_K2_unique |  8000 |   7 |   862 |         0 |                      7 |                           0 |                 0.4503 |                 0.4503 |                       1.2872 |                 0.3499 |                      1 |
| replicated_K2_unique |  8000 |   8 |   862 |         0 |                      8 |                           0 |                 0.45   |                 0.45   |                       1.4524 |                 0.3098 |                      1 |
| replicated_K2_unique | 20000 |   1 |  1634 |     16732 |                      0 |                           1 |                 0.0461 |                 0.0538 |                       0.1704 |                 0.3158 |                      1 |
| replicated_K2_unique | 20000 |   2 |  1634 |      6732 |                      0 |                           2 |                 0.0714 |                 0.0867 |                       0.3035 |                 0.2857 |                      1 |
| replicated_K2_unique | 20000 |   3 |  1634 |      3398 |                      0 |                           3 |                 0.0917 |                 0.1145 |                       0.4306 |                 0.2658 |                      1 |
| replicated_K2_unique | 20000 |   4 |  1634 |      1732 |                      0 |                           4 |                 0.1081 |                 0.138  |                       0.5544 |                 0.2489 |                      1 |
| replicated_K2_unique | 20000 |   5 |  1634 |       732 |                      0 |                           5 |                 0.2648 |                 0.2648 |                       0.6763 |                 0.3916 |                      1 |
| replicated_K2_unique | 20000 |   6 |  1634 |        65 |                      0 |                           0 |                 0.4302 |                 0.4302 |                       0.7967 |                 0.5399 |                      1 |
| replicated_K2_unique | 20000 |   7 |  1634 |         0 |                      7 |                           0 |                 0.4501 |                 0.4501 |                       0.916  |                 0.4914 |                      1 |
| replicated_K2_unique | 20000 |   8 |  1634 |         0 |                      8 |                           0 |                 0.45   |                 0.45   |                       1.0345 |                 0.435  |                      1 |

#### replicated_near_gap

| family              |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| replicated_near_gap |  2000 |   1 |   326 |      1022 |                      0 |                           1 |                 0.0563 |                 0.0878 |                       0.4649 |                 0.1888 |                      1 |
| replicated_near_gap |  2000 |   2 |   326 |        22 |                      0 |                           0 |                 0.2497 |                 0.2497 |                       0.8265 |                 0.3021 |                      1 |
| replicated_near_gap |  2000 |   3 |   326 |         0 |                      3 |                           0 |                 0.2672 |                 0.2672 |                       1.1712 |                 0.2281 |                      1 |
| replicated_near_gap |  2000 |   4 |   326 |         0 |                      4 |                           0 |                 0.2672 |                 0.2672 |                       1.507  |                 0.1773 |                      1 |
| replicated_near_gap |  2000 |   5 |   326 |         0 |                      5 |                           0 |                 0.268  |                 0.268  |                       1.8372 |                 0.1459 |                      1 |
| replicated_near_gap |  2000 |   6 |   326 |         0 |                      6 |                           0 |                 0.2668 |                 0.2668 |                       2.1634 |                 0.1233 |                      1 |
| replicated_near_gap |  8000 |   1 |   862 |      5414 |                      0 |                           1 |                 0.0388 |                 0.057  |                       0.2653 |                 0.2147 |                      1 |
| replicated_near_gap |  8000 |   2 |   862 |      1414 |                      0 |                           2 |                 0.0404 |                 0.076  |                       0.4745 |                 0.1601 |                      1 |
| replicated_near_gap |  8000 |   3 |   862 |        80 |                      0 |                           3 |                 0.2442 |                 0.2442 |                       0.6745 |                 0.362  |                      1 |
| replicated_near_gap |  8000 |   4 |   862 |         0 |                      4 |                           0 |                 0.2668 |                 0.2668 |                       0.8698 |                 0.3067 |                      1 |
| replicated_near_gap |  8000 |   5 |   862 |         0 |                      5 |                           0 |                 0.267  |                 0.267  |                       1.062  |                 0.2514 |                      1 |
| replicated_near_gap |  8000 |   6 |   862 |         0 |                      6 |                           0 |                 0.267  |                 0.267  |                       1.252  |                 0.2133 |                      1 |
| replicated_near_gap | 20000 |   1 |  1634 |     15098 |                      0 |                           1 |                 0.028  |                 0.04   |                       0.1841 |                 0.2173 |                      1 |
| replicated_near_gap | 20000 |   2 |  1634 |      5098 |                      0 |                           2 |                 0.0334 |                 0.0571 |                       0.331  |                 0.1725 |                      1 |
| replicated_near_gap | 20000 |   3 |  1634 |      1764 |                      0 |                           3 |                 0.0766 |                 0.0766 |                       0.4717 |                 0.1624 |                      1 |
| replicated_near_gap | 20000 |   4 |  1634 |        98 |                      0 |                           4 |                 0.2526 |                 0.2526 |                       0.6093 |                 0.4145 |                      1 |
| replicated_near_gap | 20000 |   5 |  1634 |         0 |                      5 |                           0 |                 0.2668 |                 0.2668 |                       0.7449 |                 0.3582 |                      1 |
| replicated_near_gap | 20000 |   6 |  1634 |         0 |                      6 |                           0 |                 0.2667 |                 0.2667 |                       0.8791 |                 0.3034 |                      1 |

#### replicated_tied_top

| family              |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| replicated_tied_top |  2000 |   1 |   326 |      1022 |                      0 |                           1 |                 0.0347 |                 0.0515 |                       0.4649 |                 0.1109 |                      1 |
| replicated_tied_top |  2000 |   2 |   326 |        22 |                      0 |                           0 |                 0.2549 |                 0.2549 |                       0.8265 |                 0.3084 |                      1 |
| replicated_tied_top |  2000 |   3 |   326 |         0 |                      3 |                           0 |                 0.2672 |                 0.2672 |                       1.1712 |                 0.2281 |                      1 |
| replicated_tied_top |  2000 |   4 |   326 |         0 |                      4 |                           0 |                 0.2672 |                 0.2672 |                       1.507  |                 0.1773 |                      1 |
| replicated_tied_top |  2000 |   5 |   326 |         0 |                      5 |                           0 |                 0.268  |                 0.268  |                       1.8372 |                 0.1459 |                      1 |
| replicated_tied_top |  2000 |   6 |   326 |         0 |                      6 |                           0 |                 0.2668 |                 0.2668 |                       2.1634 |                 0.1233 |                      1 |
| replicated_tied_top |  8000 |   1 |   862 |      5414 |                      0 |                           1 |                 0.0203 |                 0.0296 |                       0.2653 |                 0.1114 |                      1 |
| replicated_tied_top |  8000 |   2 |   862 |      1414 |                      0 |                           2 |                 0.0919 |                 0.0919 |                       0.4745 |                 0.1936 |                      1 |
| replicated_tied_top |  8000 |   3 |   862 |        80 |                      0 |                           3 |                 0.2517 |                 0.2517 |                       0.6745 |                 0.3732 |                      1 |
| replicated_tied_top |  8000 |   4 |   862 |         0 |                      4 |                           0 |                 0.2668 |                 0.2668 |                       0.8698 |                 0.3067 |                      1 |
| replicated_tied_top |  8000 |   5 |   862 |         0 |                      5 |                           0 |                 0.267  |                 0.267  |                       1.062  |                 0.2514 |                      1 |
| replicated_tied_top |  8000 |   6 |   862 |         0 |                      6 |                           0 |                 0.267  |                 0.267  |                       1.252  |                 0.2133 |                      1 |
| replicated_tied_top | 20000 |   1 |  1634 |     15098 |                      0 |                           1 |                 0.0141 |                 0.0201 |                       0.1841 |                 0.1089 |                      1 |
| replicated_tied_top | 20000 |   2 |  1634 |      5098 |                      0 |                           2 |                 0.0267 |                 0.0348 |                       0.331  |                 0.1051 |                      1 |
| replicated_tied_top | 20000 |   3 |  1634 |      1764 |                      0 |                           3 |                 0.1407 |                 0.1407 |                       0.4717 |                 0.2983 |                      1 |
| replicated_tied_top | 20000 |   4 |  1634 |        98 |                      0 |                           4 |                 0.2573 |                 0.2573 |                       0.6093 |                 0.4223 |                      1 |
| replicated_tied_top | 20000 |   5 |  1634 |         0 |                      5 |                           0 |                 0.2668 |                 0.2668 |                       0.7449 |                 0.3582 |                      1 |
| replicated_tied_top | 20000 |   6 |  1634 |         0 |                      6 |                           0 |                 0.2667 |                 0.2667 |                       0.8791 |                 0.3034 |                      1 |

#### replicated_unique_top

| family                |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| replicated_unique_top |  2000 |   1 |   326 |      1022 |                      0 |                           1 |                 0.091  |                 0.1258 |                       0.4649 |                 0.2707 |                      1 |
| replicated_unique_top |  2000 |   2 |   326 |        22 |                      0 |                           0 |                 0.2786 |                 0.2786 |                       0.8265 |                 0.3371 |                      1 |
| replicated_unique_top |  2000 |   3 |   326 |         0 |                      3 |                           0 |                 0.3006 |                 0.3006 |                       1.1712 |                 0.2567 |                      1 |
| replicated_unique_top |  2000 |   4 |   326 |         0 |                      4 |                           0 |                 0.3006 |                 0.3006 |                       1.507  |                 0.1995 |                      1 |
| replicated_unique_top |  2000 |   5 |   326 |         0 |                      5 |                           0 |                 0.3015 |                 0.3015 |                       1.8372 |                 0.1641 |                      1 |
| replicated_unique_top |  2000 |   6 |   326 |         0 |                      6 |                           0 |                 0.3001 |                 0.3001 |                       2.1634 |                 0.1387 |                      1 |
| replicated_unique_top |  8000 |   1 |   862 |      5414 |                      0 |                           1 |                 0.0606 |                 0.079  |                       0.2653 |                 0.2978 |                      1 |
| replicated_unique_top |  8000 |   2 |   862 |      1414 |                      0 |                           2 |                 0.084  |                 0.12   |                       0.4745 |                 0.2528 |                      1 |
| replicated_unique_top |  8000 |   3 |   862 |        80 |                      0 |                           3 |                 0.2728 |                 0.2728 |                       0.6745 |                 0.4045 |                      1 |
| replicated_unique_top |  8000 |   4 |   862 |         0 |                      4 |                           0 |                 0.3001 |                 0.3001 |                       0.8698 |                 0.3451 |                      1 |
| replicated_unique_top |  8000 |   5 |   862 |         0 |                      5 |                           0 |                 0.3004 |                 0.3004 |                       1.062  |                 0.2828 |                      1 |
| replicated_unique_top |  8000 |   6 |   862 |         0 |                      6 |                           0 |                 0.3004 |                 0.3004 |                       1.252  |                 0.2399 |                      1 |
| replicated_unique_top | 20000 |   1 |  1634 |     15098 |                      0 |                           1 |                 0.0447 |                 0.0566 |                       0.1841 |                 0.3075 |                      1 |
| replicated_unique_top | 20000 |   2 |  1634 |      5098 |                      0 |                           2 |                 0.0668 |                 0.0904 |                       0.331  |                 0.2732 |                      1 |
| replicated_unique_top | 20000 |   3 |  1634 |      1764 |                      0 |                           3 |                 0.0813 |                 0.1161 |                       0.4717 |                 0.2461 |                      1 |
| replicated_unique_top | 20000 |   4 |  1634 |        98 |                      0 |                           4 |                 0.2831 |                 0.2831 |                       0.6093 |                 0.4646 |                      1 |
| replicated_unique_top | 20000 |   5 |  1634 |         0 |                      5 |                           0 |                 0.3001 |                 0.3001 |                       0.7449 |                 0.4029 |                      1 |
| replicated_unique_top | 20000 |   6 |  1634 |         0 |                      6 |                           0 |                 0.3    |                 0.3    |                       0.8791 |                 0.3413 |                      1 |

#### rotating_top

| family       |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| rotating_top |  2000 |   1 |   326 |      1022 |                      0 |                           1 |                 0.0747 |                 0.1095 |                       0.4649 |                 0.2356 |                      1 |
| rotating_top |  2000 |   2 |   326 |        22 |                      0 |                           0 |                 0.229  |                 0.229  |                      16.5327 |                 0.0138 |                      0 |
| rotating_top |  2000 |   3 |   326 |         0 |                      3 |                           0 |                 0.2505 |                 0.2505 |                      16.8773 |                 0.0148 |                      0 |
| rotating_top |  2000 |   4 |   326 |         0 |                      4 |                           0 |                 0.2422 |                 0.2422 |                      32.9193 |                 0.0074 |                      0 |
| rotating_top |  2000 |   5 |   326 |         0 |                      5 |                           0 |                 0.2479 |                 0.2479 |                      33.2495 |                 0.0075 |                      0 |
| rotating_top |  2000 |   6 |   326 |         0 |                      6 |                           0 |                 0.2417 |                 0.2417 |                      49.2819 |                 0.0049 |                      0 |
| rotating_top |  8000 |   1 |   862 |      5414 |                      0 |                           1 |                 0.0498 |                 0.0682 |                       0.2653 |                 0.2572 |                      1 |
| rotating_top |  8000 |   2 |   862 |      1414 |                      0 |                           2 |                 0.1013 |                 0.1192 |                       5.3599 |                 0.0222 |                      0 |
| rotating_top |  8000 |   3 |   862 |        80 |                      0 |                           3 |                 0.2304 |                 0.2304 |                       5.5599 |                 0.0414 |                      0 |
| rotating_top |  8000 |   4 |   862 |         0 |                      4 |                           0 |                 0.2418 |                 0.2418 |                      10.6404 |                 0.0227 |                      0 |
| rotating_top |  8000 |   5 |   862 |         0 |                      5 |                           0 |                 0.247  |                 0.247  |                      10.8326 |                 0.0228 |                      0 |
| rotating_top |  8000 |   6 |   862 |         0 |                      6 |                           0 |                 0.242  |                 0.242  |                      15.908  |                 0.0152 |                      0 |
| rotating_top | 20000 |   1 |  1634 |     15098 |                      0 |                           1 |                 0.0365 |                 0.0484 |                       0.1841 |                 0.2631 |                      1 |
| rotating_top | 20000 |   2 |  1634 |      5098 |                      0 |                           2 |                 0.0783 |                 0.0902 |                       2.619  |                 0.0344 |                      0 |
| rotating_top | 20000 |   3 |  1634 |      1764 |                      0 |                           3 |                 0.091  |                 0.1142 |                       2.7598 |                 0.0414 |                      0 |
| rotating_top | 20000 |   4 |  1634 |        98 |                      0 |                           4 |                 0.2314 |                 0.2314 |                       5.1854 |                 0.0446 |                      0 |
| rotating_top | 20000 |   5 |  1634 |         0 |                      5 |                           0 |                 0.2468 |                 0.2468 |                       5.321  |                 0.0464 |                      0 |
| rotating_top | 20000 |   6 |  1634 |         0 |                      6 |                           0 |                 0.2417 |                 0.2417 |                       7.7432 |                 0.0312 |                      0 |

#### unbalanced_unique_top

| family                |     n |   Q |   L_n |   N_z_min |   n_truncated_profiles |   n_monitor_active_profiles |   exploit_LB_per_round |   exploit_UB_per_round |   theorem_constant_per_round |   ratio_UB_to_constant |   nontop_branch_active |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| unbalanced_unique_top |  2000 |   1 |   326 |      1022 |                      0 |                           1 |                 0.091  |                 0.1258 |                       0.4649 |                 0.2707 |                      1 |
| unbalanced_unique_top |  2000 |   2 |   326 |         0 |                      1 |                           1 |                 0.1668 |                 0.2001 |                       0.8265 |                 0.2421 |                      1 |
| unbalanced_unique_top |  2000 |   3 |   326 |         0 |                      2 |                           1 |                 0.2204 |                 0.2204 |                       1.1712 |                 0.1882 |                      1 |
| unbalanced_unique_top |  2000 |   4 |   326 |         0 |                      3 |                           1 |                 0.2572 |                 0.2572 |                       1.507  |                 0.1707 |                      1 |
| unbalanced_unique_top |  2000 |   5 |   326 |         0 |                      4 |                           0 |                 0.2739 |                 0.2739 |                       1.8372 |                 0.1491 |                      1 |
| unbalanced_unique_top |  2000 |   6 |   326 |         0 |                      5 |                           0 |                 0.2824 |                 0.2824 |                       2.1634 |                 0.1305 |                      1 |
| unbalanced_unique_top |  8000 |   1 |   862 |      5414 |                      0 |                           1 |                 0.0606 |                 0.079  |                       0.2653 |                 0.2978 |                      1 |
| unbalanced_unique_top |  8000 |   2 |   862 |        81 |                      0 |                           2 |                 0.1405 |                 0.1588 |                       0.4745 |                 0.3345 |                      1 |
| unbalanced_unique_top |  8000 |   3 |   862 |         0 |                      2 |                           1 |                 0.1741 |                 0.1923 |                       0.6745 |                 0.285  |                      1 |
| unbalanced_unique_top |  8000 |   4 |   862 |         0 |                      3 |                           1 |                 0.1838 |                 0.2019 |                       0.8698 |                 0.2321 |                      1 |
| unbalanced_unique_top |  8000 |   5 |   862 |         0 |                      4 |                           1 |                 0.1881 |                 0.2061 |                       1.062  |                 0.1941 |                      1 |
| unbalanced_unique_top |  8000 |   6 |   862 |         0 |                      5 |                           1 |                 0.1903 |                 0.2084 |                       1.252  |                 0.1664 |                      1 |
| unbalanced_unique_top | 20000 |   1 |  1634 |     15098 |                      0 |                           1 |                 0.0447 |                 0.0566 |                       0.1841 |                 0.3075 |                      1 |
| unbalanced_unique_top | 20000 |   2 |  1634 |      1765 |                      0 |                           2 |                 0.0649 |                 0.0884 |                       0.331  |                 0.2672 |                      1 |
| unbalanced_unique_top | 20000 |   3 |  1634 |         0 |                      1 |                           2 |                 0.129  |                 0.1409 |                       0.4717 |                 0.2986 |                      1 |
| unbalanced_unique_top | 20000 |   4 |  1634 |         0 |                      2 |                           2 |                 0.1558 |                 0.1677 |                       0.6093 |                 0.2751 |                      1 |
| unbalanced_unique_top | 20000 |   5 |  1634 |         0 |                      3 |                           2 |                 0.1679 |                 0.1797 |                       0.7449 |                 0.2413 |                      1 |
| unbalanced_unique_top | 20000 |   6 |  1634 |         0 |                      4 |                           2 |                 0.1737 |                 0.1855 |                       0.8791 |                 0.211  |                      1 |

### Localisation cost: exploitability and revenue against the profile count


#### replicated_unique_top

|     n |   Q |   stage1_share_of_horizon |   exploit_LB_per_round |   exploit_UB_per_round |   bidding_only_gain |   revenue_LB_per_round |   revenue_UB_per_round |   benchmark_M2_per_round |   revenue_bound_B_slack_per_round |   B_slack_below_n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
|  2000 |   1 |                    0.489  |                 0.091  |                 0.1258 |               293.4 |                 0.5364 |                 0.5364 |                     0.65 |                            1.0585 |                 0 |
|  2000 |   2 |                    0.978  |                 0.2786 |                 0.2786 |               586.8 |                 0.6451 |                 0.6451 |                     0.65 |                            1.6726 |                 0 |
|  2000 |   3 |                    1      |                 0.3006 |                 0.3006 |                 0   |                 0.6502 |                 0.6502 |                     0.65 |                            1.8197 |                 0 |
|  2000 |   4 |                    1      |                 0.3006 |                 0.3006 |                 0   |                 0.6505 |                 0.6505 |                     0.65 |                            1.9447 |                 0 |
|  2000 |   5 |                    1      |                 0.3015 |                 0.3015 |                 0   |                 0.6506 |                 0.6506 |                     0.65 |                            2.0698 |                 0 |
|  2000 |   6 |                    1      |                 0.3001 |                 0.3001 |                 0   |                 0.6501 |                 0.6501 |                     0.65 |                            2.1949 |                 0 |
|  8000 |   1 |                    0.3232 |                 0.0606 |                 0.079  |               775.8 |                 0.5499 |                 0.5499 |                     0.65 |                            0.6809 |                 1 |
|  8000 |   2 |                    0.6465 |                 0.084  |                 0.12   |              1551.6 |                 0.5977 |                 0.5977 |                     0.65 |                            1.0658 |                 0 |
|  8000 |   3 |                    0.9698 |                 0.2728 |                 0.2728 |              2327.4 |                 0.6455 |                 0.6455 |                     0.65 |                            1.4508 |                 0 |
|  8000 |   4 |                    1      |                 0.3001 |                 0.3001 |                 0   |                 0.6501 |                 0.6501 |                     0.65 |                            1.5428 |                 0 |
|  8000 |   5 |                    1      |                 0.3004 |                 0.3004 |                 0   |                 0.6502 |                 0.6502 |                     0.65 |                            1.6045 |                 0 |
|  8000 |   6 |                    1      |                 0.3004 |                 0.3004 |                 0   |                 0.6502 |                 0.6502 |                     0.65 |                            1.6662 |                 0 |
| 20000 |   1 |                    0.2451 |                 0.0447 |                 0.0566 |              1470.6 |                 0.565  |                 0.565  |                     0.65 |                            0.5091 |                 1 |
| 20000 |   2 |                    0.4902 |                 0.0668 |                 0.0904 |              2941.2 |                 0.5926 |                 0.5926 |                     0.65 |                            0.793  |                 1 |
| 20000 |   3 |                    0.7353 |                 0.0813 |                 0.1161 |              4411.8 |                 0.6202 |                 0.6202 |                     0.65 |                            1.0769 |                 0 |
| 20000 |   4 |                    0.9804 |                 0.2831 |                 0.2831 |              5882.4 |                 0.6478 |                 0.6478 |                     0.65 |                            1.3609 |                 0 |
| 20000 |   5 |                    1      |                 0.3001 |                 0.3001 |                 0   |                 0.6501 |                 0.6501 |                     0.65 |                            1.4193 |                 0 |
| 20000 |   6 |                    1      |                 0.3    |                 0.3    |                 0   |                 0.65   |                 0.65   |                     0.65 |                            1.4582 |                 0 |

#### replicated_tied_top

|     n |   Q |   stage1_share_of_horizon |   exploit_LB_per_round |   exploit_UB_per_round |   bidding_only_gain |   revenue_LB_per_round |   revenue_UB_per_round |   benchmark_M2_per_round |   revenue_bound_B_slack_per_round |   B_slack_below_n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
|  2000 |   1 |                    0.489  |                 0.0347 |                 0.0515 |               260.8 |                 0.623  |                 0.623  |                      0.8 |                            1.0585 |                 0 |
|  2000 |   2 |                    0.978  |                 0.2549 |                 0.2549 |               521.6 |                 0.6807 |                 0.6807 |                      0.8 |                            1.6726 |                 0 |
|  2000 |   3 |                    1      |                 0.2672 |                 0.2672 |                 0   |                 0.6835 |                 0.6835 |                      0.8 |                            1.8197 |                 0 |
|  2000 |   4 |                    1      |                 0.2672 |                 0.2672 |                 0   |                 0.6838 |                 0.6838 |                      0.8 |                            1.9447 |                 0 |
|  2000 |   5 |                    1      |                 0.268  |                 0.268  |                 0   |                 0.6836 |                 0.6836 |                      0.8 |                            2.0698 |                 0 |
|  2000 |   6 |                    1      |                 0.2668 |                 0.2668 |                 0   |                 0.6835 |                 0.6835 |                      0.8 |                            2.1949 |                 0 |
|  8000 |   1 |                    0.3232 |                 0.0203 |                 0.0296 |               689.6 |                 0.657  |                 0.657  |                      0.8 |                            0.6809 |                 1 |
|  8000 |   2 |                    0.6465 |                 0.0919 |                 0.0919 |              1379.2 |                 0.6696 |                 0.6696 |                      0.8 |                            1.0658 |                 0 |
|  8000 |   3 |                    0.9698 |                 0.2517 |                 0.2517 |              2068.8 |                 0.6822 |                 0.6822 |                      0.8 |                            1.4508 |                 0 |
|  8000 |   4 |                    1      |                 0.2668 |                 0.2668 |                 0   |                 0.6835 |                 0.6835 |                      0.8 |                            1.5428 |                 0 |
|  8000 |   5 |                    1      |                 0.267  |                 0.267  |                 0   |                 0.6834 |                 0.6834 |                      0.8 |                            1.6045 |                 0 |
|  8000 |   6 |                    1      |                 0.267  |                 0.267  |                 0   |                 0.6834 |                 0.6834 |                      0.8 |                            1.6662 |                 0 |
| 20000 |   1 |                    0.2451 |                 0.0141 |                 0.0201 |              1307.2 |                 0.6822 |                 0.6822 |                      0.8 |                            0.5091 |                 1 |
| 20000 |   2 |                    0.4902 |                 0.0267 |                 0.0348 |              2614.4 |                 0.6826 |                 0.6826 |                      0.8 |                            0.793  |                 1 |
| 20000 |   3 |                    0.7353 |                 0.1407 |                 0.1407 |              3921.6 |                 0.6829 |                 0.6829 |                      0.8 |                            1.0769 |                 0 |
| 20000 |   4 |                    0.9804 |                 0.2573 |                 0.2573 |              5228.8 |                 0.6833 |                 0.6833 |                      0.8 |                            1.3609 |                 0 |
| 20000 |   5 |                    1      |                 0.2668 |                 0.2668 |                 0   |                 0.6834 |                 0.6834 |                      0.8 |                            1.4193 |                 0 |
| 20000 |   6 |                    1      |                 0.2667 |                 0.2667 |                 0   |                 0.6833 |                 0.6833 |                      0.8 |                            1.4582 |                 0 |

#### replicated_K2_unique

|     n |   Q |   stage1_share_of_horizon |   exploit_LB_per_round |   exploit_UB_per_round |   bidding_only_gain |   revenue_LB_per_round |   revenue_UB_per_round |   benchmark_M2_per_round |   revenue_bound_B_slack_per_round |   B_slack_below_n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
|  2000 |   1 |                    0.326  |                 0.1    |                 0.1223 |               293.4 |                 0.5419 |                 0.5419 |                     0.65 |                            0.848  |                 1 |
|  2000 |   2 |                    0.652  |                 0.1322 |                 0.1747 |               586.8 |                 0.6547 |                 0.6547 |                     0.65 |                            1.2544 |                 0 |
|  2000 |   3 |                    0.978  |                 0.4253 |                 0.4253 |               880.2 |                 0.7674 |                 0.7674 |                     0.65 |                            1.6607 |                 0 |
|  2000 |   4 |                    1      |                 0.45   |                 0.45   |                 0   |                 0.775  |                 0.775  |                     0.65 |                            1.7631 |                 0 |
|  2000 |   5 |                    1      |                 0.45   |                 0.45   |                 0   |                 0.775  |                 0.775  |                     0.65 |                            1.8435 |                 0 |
|  2000 |   6 |                    1      |                 0.4513 |                 0.4513 |                 0   |                 0.7754 |                 0.7754 |                     0.65 |                            1.9238 |                 0 |
|  2000 |   7 |                    1      |                 0.45   |                 0.45   |                 0   |                 0.775  |                 0.775  |                     0.65 |                            2.0042 |                 0 |
|  2000 |   8 |                    1      |                 0.45   |                 0.45   |                 0   |                 0.775  |                 0.775  |                     0.65 |                            2.0846 |                 0 |
|  8000 |   1 |                    0.2155 |                 0.0635 |                 0.0754 |               775.8 |                 0.5615 |                 0.5615 |                     0.65 |                            0.5497 |                 1 |
|  8000 |   2 |                    0.431  |                 0.0943 |                 0.1177 |              1551.6 |                 0.6201 |                 0.6201 |                     0.65 |                            0.805  |                 1 |
|  8000 |   3 |                    0.6465 |                 0.1156 |                 0.1499 |              2327.4 |                 0.6788 |                 0.6788 |                     0.65 |                            1.0603 |                 0 |
|  8000 |   4 |                    0.862  |                 0.3055 |                 0.3055 |              3103.2 |                 0.7374 |                 0.7374 |                     0.65 |                            1.3157 |                 0 |
|  8000 |   5 |                    1      |                 0.45   |                 0.45   |                 0   |                 0.775  |                 0.775  |                     0.65 |                            1.4935 |                 0 |
|  8000 |   6 |                    1      |                 0.4503 |                 0.4503 |                 0   |                 0.7751 |                 0.7751 |                     0.65 |                            1.5333 |                 0 |
|  8000 |   7 |                    1      |                 0.4503 |                 0.4503 |                 0   |                 0.7751 |                 0.7751 |                     0.65 |                            1.5732 |                 0 |
|  8000 |   8 |                    1      |                 0.45   |                 0.45   |                 0   |                 0.775  |                 0.775  |                     0.65 |                            1.613  |                 0 |
| 20000 |   1 |                    0.1634 |                 0.0461 |                 0.0538 |              1470.6 |                 0.5767 |                 0.5767 |                     0.65 |                            0.4125 |                 1 |
| 20000 |   2 |                    0.3268 |                 0.0714 |                 0.0867 |              2941.2 |                 0.6154 |                 0.6154 |                     0.65 |                            0.601  |                 1 |
| 20000 |   3 |                    0.4902 |                 0.0917 |                 0.1145 |              4411.8 |                 0.6542 |                 0.6542 |                     0.65 |                            0.7896 |                 1 |
| 20000 |   4 |                    0.6536 |                 0.1081 |                 0.138  |              5882.4 |                 0.6929 |                 0.6929 |                     0.65 |                            0.9781 |                 1 |
| 20000 |   5 |                    0.817  |                 0.2648 |                 0.2648 |              7353   |                 0.7316 |                 0.7316 |                     0.65 |                            1.1666 |                 0 |
| 20000 |   6 |                    0.9804 |                 0.4302 |                 0.4302 |              8823.6 |                 0.7704 |                 0.7704 |                     0.65 |                            1.3551 |                 0 |
| 20000 |   7 |                    1      |                 0.4501 |                 0.4501 |                 0   |                 0.775  |                 0.775  |                     0.65 |                            1.3998 |                 0 |
| 20000 |   8 |                    1      |                 0.45   |                 0.45   |                 0   |                 0.775  |                 0.775  |                     0.65 |                            1.4249 |                 0 |

#### regime_switch

|     n |   Q |   stage1_share_of_horizon |   exploit_LB_per_round |   exploit_UB_per_round |   bidding_only_gain |   revenue_LB_per_round |   revenue_UB_per_round |   benchmark_M2_per_round |   revenue_bound_B_slack_per_round |   B_slack_below_n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
|  2000 |   2 |                    0.978  |                 0.2058 |                 0.2058 |               440.1 |                 0.5386 |                 0.5386 |                   0.625  |                            1.6726 |                 0 |
|  2000 |   4 |                    1      |                 0.2254 |                 0.2254 |                 0   |                 0.5421 |                 0.5421 |                   0.625  |                            1.9447 |                 0 |
|  2000 |   6 |                    1      |                 0.225  |                 0.225  |                 0   |                 0.5415 |                 0.5415 |                   0.6248 |                            2.1949 |                 0 |
|  8000 |   2 |                    0.6465 |                 0.0471 |                 0.0778 |              1163.7 |                 0.5188 |                 0.5188 |                   0.625  |                            1.0658 |                 0 |
|  8000 |   4 |                    1      |                 0.2251 |                 0.2251 |                 0   |                 0.5418 |                 0.5418 |                   0.625  |                            1.5428 |                 0 |
|  8000 |   6 |                    1      |                 0.2253 |                 0.2253 |                 0   |                 0.5417 |                 0.5417 |                   0.6249 |                            1.6662 |                 0 |
| 20000 |   2 |                    0.4902 |                 0.0348 |                 0.0584 |              2205.9 |                 0.5268 |                 0.5268 |                   0.625  |                            0.793  |                 1 |
| 20000 |   4 |                    0.9804 |                 0.2091 |                 0.2091 |              4411.8 |                 0.5411 |                 0.5411 |                   0.625  |                            1.3609 |                 0 |
| 20000 |   6 |                    1      |                 0.225  |                 0.225  |                 0   |                 0.5417 |                 0.5417 |                   0.625  |                            1.4582 |                 0 |
| 50000 |   2 |                    0.371  |                 0.0265 |                 0.0417 |              4174.2 |                 0.5404 |                 0.5404 |                   0.625  |                            0.5908 |                 1 |
| 50000 |   4 |                    0.7421 |                 0.0816 |                 0.0963 |              8348.4 |                 0.5411 |                 0.5411 |                   0.625  |                            1.0108 |                 0 |
| 50000 |   6 |                    1      |                 0.225  |                 0.225  |                 0   |                 0.5417 |                 0.5417 |                   0.625  |                            1.3177 |                 0 |

### Where the profile count bites (analytic, regime.csv)

|   K |             n |       L_n |   Qmax_all_profiles_finish_bidding |   Qmax_bound_below_2n |   Qmax_monitor_active |
|--:|--:|--:|--:|--:|--:|
|   2 |          1000 |       200 |                                  2 |                     2 |                     2 |
|   2 |         10000 |      1007 |                                  4 |                     4 |                     4 |
|   2 |        100000 |      5002 |                                  9 |                     9 |                     9 |
|   2 |       1000000 |     24561 |                                 20 |                    20 |                    20 |
|   2 |      10000000 |    119625 |                                 41 |                    41 |                    41 |
|   2 |     100000000 |    579102 |                                 76 |                    76 |                    76 |
|   2 |    1000000000 |   2790241 |                                152 |                   152 |                   152 |
|   2 |   10000000000 |  13393465 |                                362 |                   362 |                   362 |
|   2 | 1000000000000 | 305923106 |                               1448 |                  1448 |                  1448 |
|   3 |          1000 |       166 |                                  2 |                     2 |                     1 |
|   3 |         10000 |      1007 |                                  3 |                     3 |                     3 |
|   3 |        100000 |      5002 |                                  6 |                     6 |                     6 |
|   3 |       1000000 |     24561 |                                 13 |                    13 |                    13 |
|   3 |      10000000 |    119625 |                                 27 |                    27 |                    27 |
|   3 |     100000000 |    579102 |                                 57 |                    57 |                    57 |
|   3 |    1000000000 |   2790241 |                                108 |                   108 |                   108 |
|   3 |   10000000000 |  13393465 |                                215 |                   215 |                   215 |
|   3 | 1000000000000 | 305923106 |                               1024 |                  1024 |                  1024 |

### Non-top branch: smallest horizon at which 4 s_n <= delta (nontop_thresholds.csv)

|   K |   delta |       n_min |   log10_n_min |
|--:|--:|--:|--:|
|   2 |   0.5   |       13861 |          4.14 |
|   2 |   0.3   |       75504 |          4.88 |
|   2 |   0.25  |      137412 |          5.14 |
|   2 |   0.2   |      284911 |          5.45 |
|   2 |   0.15  |      725441 |          5.86 |
|   2 |   0.1   |     2685083 |          6.43 |
|   2 |   0.05  |    24692083 |          7.39 |
|   2 |   0.02  |   451546450 |          8.65 |
|   2 |   0.01  |  4007452996 |          9.6  |
|   2 |   0.005 | 35205660862 |         10.55 |
|   3 |   0.5   |       14097 |          4.15 |
|   3 |   0.3   |       76618 |          4.88 |
|   3 |   0.25  |      139294 |          5.14 |
|   3 |   0.2   |      288550 |          5.46 |
|   3 |   0.15  |      734059 |          5.87 |
|   3 |   0.1   |     2714044 |          6.43 |
|   3 |   0.05  |    24921969 |          7.4  |
|   3 |   0.02  |   455115528 |          8.66 |
|   3 |   0.01  |  4035893390 |          9.61 |
|   3 |   0.005 | 35432526259 |         10.55 |

### Contextual ablation ladder (synthetic paired simulation)

cells: 2888 rows over families ['heterogeneous', 'regime_switch', 'replicated_honest_top', 'replicated_tied_top', 'replicated_unique_top', 'rotating_top'], horizons [np.int64(20000)], profile counts [np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(6)], rungs ['pl_mesp', 'pl_nofallback', 'pl_nomonitor', 'pl_noslack', 'pl_rawprice', 'pl_runnerup', 'pl_shared', 'pl_windowed'], behaviours 19


#### heterogeneous, n = 20000, Q = 1

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01225 | underbid_15      |                                        0 |                                        0.48118 |                                 -0.05333 |                                           0.43761 |
| pl_mesp       |                                       0.01225 | underbid_15      |                                        0 |                                        0.48118 |                                 -0.05333 |                                           0.43761 |
| pl_rawprice   |                                       0.01225 | underbid_15      |                                        0 |                                        0.56622 |                                 -0.05333 |                                           0.55017 |
| pl_nofallback |                                       0.01225 | underbid_15      |                                        0 |                                        0.48118 |                                 -0.099   |                                           0.43761 |
| pl_runnerup   |                                       0.01225 | underbid_15      |                                        0 |                                        0.48118 |                                 -0.19876 |                                           0.43761 |
| pl_noslack    |                                       0.07174 | bid_zero         |                                        1 |                                        0.81313 |                                 -0.05333 |                                           0.43761 |
| pl_windowed   |                                       0.11324 | primary_shade_15 |                                        0 |                                        0.48118 |                                 -0.05333 |                                           0.43761 |
| pl_nomonitor  |                                       0.33035 | bait_switch      |                                        0 |                                        0.48118 |                                 -0.19876 |                                           0.43761 |

#### heterogeneous, n = 20000, Q = 2

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01191 | boundary_ride    |                                   0      |                                        0.59467 |                                 -0.05323 |                                           0.58798 |
| pl_mesp       |                                       0.02451 | underbid_15      |                                   0      |                                        0.53858 |                                 -0.10631 |                                           0.46317 |
| pl_rawprice   |                                       0.02451 | underbid_15      |                                   0      |                                        0.596   |                                 -0.10631 |                                           0.57573 |
| pl_nofallback |                                       0.02451 | underbid_15      |                                   0      |                                        0.53858 |                                 -0.10631 |                                           0.46317 |
| pl_runnerup   |                                       0.02451 | underbid_15      |                                   0      |                                        0.53858 |                                 -0.10631 |                                           0.46317 |
| pl_windowed   |                                       0.03823 | primary_shade_15 |                                   0      |                                        0.53858 |                                 -0.10631 |                                           0.46317 |
| pl_nomonitor  |                                       0.11176 | bait_switch      |                                   0      |                                        0.53858 |                                 -0.10631 |                                           0.46317 |
| pl_noslack    |                                       0.11925 | bid_zero         |                                   0.9925 |                                        0.71716 |                                 -0.10631 |                                           0.46317 |

#### heterogeneous, n = 20000, Q = 3

| rung          |   best tested unilateral deviation, per round | which         |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01216 | boundary_ride |                                  0       |                                        0.4696  |                                 -0.05296 |                                           0.43815 |
| pl_mesp       |                                       0.08014 | bid_zero      |                                  0       |                                        0.58676 |                                 -0.15923 |                                           0.50408 |
| pl_runnerup   |                                       0.08014 | bid_zero      |                                  0       |                                        0.58676 |                                 -0.15923 |                                           0.50408 |
| pl_nofallback |                                       0.08014 | bid_zero      |                                  0       |                                        0.58676 |                                 -0.15923 |                                           0.50408 |
| pl_windowed   |                                       0.08014 | bid_zero      |                                  0       |                                        0.58676 |                                 -0.15923 |                                           0.50408 |
| pl_nomonitor  |                                       0.09047 | bait_switch   |                                  0       |                                        0.58676 |                                 -0.15923 |                                           0.50408 |
| pl_rawprice   |                                       0.10001 | bid_zero      |                                  0       |                                        0.61658 |                                 -0.15923 |                                           0.61665 |
| pl_noslack    |                                       0.18082 | bid_zero      |                                  0.99333 |                                        0.643   |                                 -0.15923 |                                           0.50408 |

#### regime_switch, n = 20000, Q = 2

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0       | profile          |                                    0.27  |                                        0.50102 |                                 -0.01048 |                                           0.51337 |
| pl_runnerup   |                                       0.0249  | primary_shade_05 |                                    0     |                                        0.52687 |                                 -0.02059 |                                           0.51246 |
| pl_nofallback |                                       0.02501 | primary_shade_05 |                                    0     |                                        0.52687 |                                 -0.02059 |                                           0.51246 |
| pl_mesp       |                                       0.02504 | primary_shade_05 |                                    0     |                                        0.52687 |                                 -0.02059 |                                           0.51246 |
| pl_rawprice   |                                       0.02529 | primary_shade_05 |                                    0     |                                        0.58426 |                                 -0.02059 |                                           0.62502 |
| pl_windowed   |                                       0.07628 | primary_shade_15 |                                    0     |                                        0.52687 |                                 -0.02059 |                                           0.51246 |
| pl_noslack    |                                       0.10642 | bid_zero         |                                    0.995 |                                        0.58919 |                                 -0.02059 |                                           0.51246 |
| pl_nomonitor  |                                       0.26028 | bait_switch      |                                    0     |                                        0.52687 |                                 -0.02059 |                                           0.51246 |

#### regime_switch, n = 20000, Q = 4

| rung          |   best tested unilateral deviation, per round | which        |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0       | profile      |                                  0.265   |                                        0.49933 |                                 -0.01037 |                                           0.51207 |
| pl_mesp       |                                       0.20908 | bid_zero     |                                  0       |                                        0.54084 |                                 -0.04083 |                                           0.51166 |
| pl_nomonitor  |                                       0.20908 | bid_zero     |                                  0       |                                        0.54084 |                                 -0.04083 |                                           0.51166 |
| pl_nofallback |                                       0.20908 | bid_zero     |                                  0       |                                        0.54084 |                                 -0.04083 |                                           0.51166 |
| pl_windowed   |                                       0.20908 | bid_zero     |                                  0       |                                        0.54084 |                                 -0.04083 |                                           0.51166 |
| pl_runnerup   |                                       0.20908 | bid_zero     |                                  0       |                                        0.54084 |                                 -0.04083 |                                           0.51166 |
| pl_rawprice   |                                       0.21128 | bid_zero     |                                  0       |                                        0.54305 |                                 -0.04083 |                                           0.62422 |
| pl_noslack    |                                       0.22288 | sabotage_all |                                  0.93625 |                                        0.54146 |                                 -0.04083 |                                           0.51166 |

#### regime_switch, n = 20000, Q = 6

| rung          |   best tested unilateral deviation, per round | which    |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.03679 | bid_zero |                                        0 |                                        0.37641 |                                 -0.00416 |                                           0.33903 |
| pl_mesp       |                                       0.225   | bid_zero |                                        0 |                                        0.54139 |                                 -0.04175 |                                          -1       |
| pl_nomonitor  |                                       0.225   | bid_zero |                                        0 |                                        0.54139 |                                 -0.04175 |                                          -1       |
| pl_nofallback |                                       0.225   | bid_zero |                                        0 |                                        0.54139 |                                 -0.04175 |                                          -1       |
| pl_noslack    |                                       0.225   | bid_zero |                                        0 |                                        0.54139 |                                 -0.04175 |                                          -1       |
| pl_rawprice   |                                       0.225   | bid_zero |                                        0 |                                        0.54139 |                                 -0.04175 |                                          -1       |
| pl_runnerup   |                                       0.225   | bid_zero |                                        0 |                                        0.54139 |                                 -0.04175 |                                          -1       |
| pl_windowed   |                                       0.225   | bid_zero |                                        0 |                                        0.54139 |                                 -0.04175 |                                          -1       |

#### replicated_honest_top, n = 20000, Q = 1

| rung          |   best tested unilateral deviation, per round | which    |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_noslack    |                                       0.03541 | bid_zero |                                    0.585 |                                        0.71266 |                                 -0.12301 |                                           0.58794 |
| pl_shared     |                                       0.05719 | bid_zero |                                    0     |                                        0.72104 |                                 -0.12301 |                                           0.58794 |
| pl_nofallback |                                       0.05719 | bid_zero |                                    0     |                                        0.72104 |                                 -0.12301 |                                           0.58794 |
| pl_mesp       |                                       0.05719 | bid_zero |                                    0     |                                        0.72104 |                                 -0.12301 |                                           0.58794 |
| pl_nomonitor  |                                       0.05719 | bid_zero |                                    0     |                                        0.72104 |                                 -0.12301 |                                           0.58794 |
| pl_rawprice   |                                       0.05719 | bid_zero |                                    0     |                                        0.72104 |                                 -0.12301 |                                           0.7005  |
| pl_runnerup   |                                       0.05719 | bid_zero |                                    0     |                                        0.72104 |                                 -0.12301 |                                           0.58794 |
| pl_windowed   |                                       0.05719 | bid_zero |                                    0     |                                        0.72104 |                                 -0.12301 |                                           0.58794 |

#### replicated_honest_top, n = 20000, Q = 2

| rung          |   best tested unilateral deviation, per round | which    |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.05498 | bid_zero |                                     0    |                                        0.72082 |                                 -0.12257 |                                           0.58744 |
| pl_noslack    |                                       0.0895  | bid_zero |                                     0.55 |                                        0.68195 |                                 -0.24493 |                                           0.58788 |
| pl_nofallback |                                       0.11364 | bid_zero |                                     0    |                                        0.69284 |                                 -0.24493 |                                           0.58788 |
| pl_mesp       |                                       0.11364 | bid_zero |                                     0    |                                        0.69284 |                                 -0.24493 |                                           0.58788 |
| pl_nomonitor  |                                       0.11364 | bid_zero |                                     0    |                                        0.69284 |                                 -0.24493 |                                           0.58788 |
| pl_runnerup   |                                       0.11364 | bid_zero |                                     0    |                                        0.69284 |                                 -0.24493 |                                           0.58788 |
| pl_windowed   |                                       0.11364 | bid_zero |                                     0    |                                        0.69284 |                                 -0.24493 |                                           0.58788 |
| pl_rawprice   |                                       0.11374 | bid_zero |                                     0    |                                        0.69294 |                                 -0.24493 |                                           0.70044 |

#### replicated_honest_top, n = 20000, Q = 3

| rung          |   best tested unilateral deviation, per round | which    |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.05719 | bid_zero |                                  0       |                                        0.7211  |                                 -0.12287 |                                           0.58786 |
| pl_noslack    |                                       0.15923 | bid_zero |                                  0.55667 |                                        0.65385 |                                 -0.36782 |                                           0.58717 |
| pl_nofallback |                                       0.17131 | bid_zero |                                  0       |                                        0.66397 |                                 -0.36782 |                                           0.58717 |
| pl_mesp       |                                       0.17131 | bid_zero |                                  0       |                                        0.66397 |                                 -0.36782 |                                           0.58717 |
| pl_nomonitor  |                                       0.17131 | bid_zero |                                  0       |                                        0.66397 |                                 -0.36782 |                                           0.58717 |
| pl_runnerup   |                                       0.17131 | bid_zero |                                  0       |                                        0.66397 |                                 -0.36782 |                                           0.58717 |
| pl_windowed   |                                       0.17131 | bid_zero |                                  0       |                                        0.66397 |                                 -0.36782 |                                           0.58717 |
| pl_rawprice   |                                       0.17135 | bid_zero |                                  0       |                                        0.664   |                                 -0.36782 |                                           0.69973 |

#### replicated_tied_top, n = 20000, Q = 1

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_rawprice   |                                       0.00565 | boundary_ride    |                                    0     |                                        0.76575 |                                 -0.04929 |                                           0.79406 |
| pl_mesp       |                                       0.00604 | boundary_ride    |                                    0     |                                        0.68156 |                                 -0.04929 |                                           0.6815  |
| pl_runnerup   |                                       0.00604 | boundary_ride    |                                    0     |                                        0.68156 |                                 -0.18243 |                                           0.6815  |
| pl_nofallback |                                       0.00604 | boundary_ride    |                                    0     |                                        0.68156 |                                 -0.06979 |                                           0.6815  |
| pl_shared     |                                       0.00604 | boundary_ride    |                                    0     |                                        0.68156 |                                 -0.04929 |                                           0.6815  |
| pl_windowed   |                                       0.05605 | primary_shade_15 |                                    0     |                                        0.68156 |                                 -0.04929 |                                           0.6815  |
| pl_noslack    |                                       0.06555 | bid_zero         |                                    0.995 |                                        0.76494 |                                 -0.04929 |                                           0.6815  |
| pl_nomonitor  |                                       0.25448 | bait_switch      |                                    0     |                                        0.68156 |                                 -0.18243 |                                           0.6815  |

#### replicated_tied_top, n = 20000, Q = 2

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.00573 | boundary_ride    |                                   0      |                                        0.68164 |                                 -0.04916 |                                           0.68109 |
| pl_mesp       |                                       0.02049 | bid_zero         |                                   0      |                                        0.68259 |                                 -0.09815 |                                           0.6816  |
| pl_runnerup   |                                       0.02049 | bid_zero         |                                   0      |                                        0.68259 |                                 -0.09815 |                                           0.6816  |
| pl_nofallback |                                       0.02049 | bid_zero         |                                   0      |                                        0.68259 |                                 -0.09815 |                                           0.6816  |
| pl_windowed   |                                       0.03957 | primary_shade_15 |                                   0      |                                        0.68259 |                                 -0.09815 |                                           0.6816  |
| pl_rawprice   |                                       0.04985 | bid_zero         |                                   0      |                                        0.73925 |                                 -0.09815 |                                           0.79417 |
| pl_noslack    |                                       0.12861 | bid_zero         |                                   0.9875 |                                        0.73112 |                                 -0.09815 |                                           0.6816  |
| pl_nomonitor  |                                       0.17997 | bait_switch      |                                   0      |                                        0.68259 |                                 -0.09815 |                                           0.6816  |

#### replicated_tied_top, n = 20000, Q = 3

| rung          |   best tested unilateral deviation, per round | which         |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.00567 | boundary_ride |                                    0     |                                        0.68224 |                                 -0.04887 |                                           0.68222 |
| pl_mesp       |                                       0.13946 | bid_zero      |                                    0     |                                        0.68267 |                                 -0.14707 |                                           0.68154 |
| pl_nomonitor  |                                       0.13946 | bid_zero      |                                    0     |                                        0.68267 |                                 -0.14707 |                                           0.68154 |
| pl_nofallback |                                       0.13946 | bid_zero      |                                    0     |                                        0.68267 |                                 -0.14707 |                                           0.68154 |
| pl_windowed   |                                       0.13946 | bid_zero      |                                    0     |                                        0.68267 |                                 -0.14707 |                                           0.68154 |
| pl_runnerup   |                                       0.13946 | bid_zero      |                                    0     |                                        0.68267 |                                 -0.14707 |                                           0.68154 |
| pl_rawprice   |                                       0.15456 | bid_zero      |                                    0     |                                        0.71229 |                                 -0.14707 |                                           0.7941  |
| pl_noslack    |                                       0.19481 | bid_zero      |                                    0.985 |                                        0.70025 |                                 -0.14707 |                                           0.68154 |

#### replicated_unique_top, n = 20000, Q = 1

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01225 | underbid_15      |                                    0     |                                        0.56531 |                                 -0.05333 |                                           0.53816 |
| pl_mesp       |                                       0.01225 | underbid_15      |                                    0     |                                        0.56531 |                                 -0.05333 |                                           0.53816 |
| pl_runnerup   |                                       0.01225 | underbid_15      |                                    0     |                                        0.56531 |                                 -0.19054 |                                           0.53816 |
| pl_nofallback |                                       0.01225 | underbid_15      |                                    0     |                                        0.56531 |                                 -0.09056 |                                           0.53816 |
| pl_rawprice   |                                       0.01226 | underbid_15      |                                    0     |                                        0.65021 |                                 -0.05333 |                                           0.65072 |
| pl_noslack    |                                       0.07143 | bid_zero         |                                    0.995 |                                        0.82121 |                                 -0.05333 |                                           0.53816 |
| pl_windowed   |                                       0.11323 | primary_shade_15 |                                    0     |                                        0.56531 |                                 -0.05333 |                                           0.53816 |
| pl_nomonitor  |                                       0.40626 | bait_switch      |                                    0     |                                        0.56531 |                                 -0.19054 |                                           0.53816 |

#### replicated_unique_top, n = 20000, Q = 2

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01225 | underbid_15      |                                    0     |                                        0.56459 |                                 -0.05323 |                                           0.53715 |
| pl_rawprice   |                                       0.02466 | primary_shade_05 |                                    0     |                                        0.64998 |                                 -0.10631 |                                           0.6499  |
| pl_runnerup   |                                       0.02487 | primary_shade_05 |                                    0     |                                        0.59262 |                                 -0.10631 |                                           0.53734 |
| pl_nofallback |                                       0.02494 | primary_shade_05 |                                    0     |                                        0.59262 |                                 -0.10631 |                                           0.53734 |
| pl_mesp       |                                       0.02495 | primary_shade_05 |                                    0     |                                        0.59262 |                                 -0.10631 |                                           0.53734 |
| pl_windowed   |                                       0.07647 | primary_shade_15 |                                    0     |                                        0.59262 |                                 -0.10631 |                                           0.53734 |
| pl_noslack    |                                       0.143   | bid_zero         |                                    0.995 |                                        0.74716 |                                 -0.10631 |                                           0.53734 |
| pl_nomonitor  |                                       0.27393 | bait_switch      |                                    0     |                                        0.59262 |                                 -0.10631 |                                           0.53734 |

#### replicated_unique_top, n = 20000, Q = 3

| rung          |   best tested unilateral deviation, per round | which       |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01225 | underbid_15 |                                    0     |                                        0.56541 |                                 -0.05296 |                                           0.53825 |
| pl_mesp       |                                       0.07163 | bid_zero    |                                    0     |                                        0.62005 |                                 -0.15923 |                                           0.53726 |
| pl_runnerup   |                                       0.07163 | bid_zero    |                                    0     |                                        0.62005 |                                 -0.15923 |                                           0.53726 |
| pl_nofallback |                                       0.07163 | bid_zero    |                                    0     |                                        0.62005 |                                 -0.15923 |                                           0.53726 |
| pl_windowed   |                                       0.07163 | bid_zero    |                                    0     |                                        0.62005 |                                 -0.15923 |                                           0.53726 |
| pl_rawprice   |                                       0.10143 | bid_zero    |                                    0     |                                        0.6498  |                                 -0.15923 |                                           0.64982 |
| pl_nomonitor  |                                       0.14221 | bait_switch |                                    0     |                                        0.62005 |                                 -0.15923 |                                           0.53726 |
| pl_noslack    |                                       0.21689 | bid_zero    |                                    0.985 |                                        0.68099 |                                 -0.15923 |                                           0.53726 |

#### replicated_unique_top, n = 20000, Q = 6

| rung          |   best tested unilateral deviation, per round | which       |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01225 | underbid_15 |                                        0 |                                        0.56432 |                                 -0.0532  |                                           0.53653 |
| pl_mesp       |                                       0.30002 | bid_zero    |                                        0 |                                        0.64992 |                                 -0.21672 |                                          -1       |
| pl_nomonitor  |                                       0.30002 | bid_zero    |                                        0 |                                        0.64992 |                                 -0.21672 |                                          -1       |
| pl_nofallback |                                       0.30002 | bid_zero    |                                        0 |                                        0.64992 |                                 -0.21672 |                                          -1       |
| pl_noslack    |                                       0.30002 | bid_zero    |                                        0 |                                        0.64992 |                                 -0.21672 |                                          -1       |
| pl_rawprice   |                                       0.30002 | bid_zero    |                                        0 |                                        0.64992 |                                 -0.21672 |                                          -1       |
| pl_runnerup   |                                       0.30002 | bid_zero    |                                        0 |                                        0.64992 |                                 -0.21672 |                                          -1       |
| pl_windowed   |                                       0.30002 | bid_zero    |                                        0 |                                        0.64992 |                                 -0.21672 |                                          -1       |

#### rotating_top, n = 20000, Q = 1

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.01218 | boundary_ride    |                                    0     |                                        0.55716 |                                 -0.05333 |                                           0.53816 |
| pl_mesp       |                                       0.01218 | boundary_ride    |                                    0     |                                        0.55716 |                                 -0.05333 |                                           0.53816 |
| pl_runnerup   |                                       0.01218 | boundary_ride    |                                    0     |                                        0.55716 |                                 -0.19869 |                                           0.53816 |
| pl_nofallback |                                       0.01218 | boundary_ride    |                                    0     |                                        0.55716 |                                 -0.09871 |                                           0.53816 |
| pl_rawprice   |                                       0.01219 | boundary_ride    |                                    0     |                                        0.64206 |                                 -0.05333 |                                           0.65072 |
| pl_noslack    |                                       0.06356 | bid_zero         |                                    0.995 |                                        0.73837 |                                 -0.05333 |                                           0.53816 |
| pl_windowed   |                                       0.11324 | primary_shade_15 |                                    0     |                                        0.55716 |                                 -0.05333 |                                           0.53816 |
| pl_nomonitor  |                                       0.40626 | bait_switch      |                                    0     |                                        0.55716 |                                 -0.19869 |                                           0.53816 |

#### rotating_top, n = 20000, Q = 2

| rung          |   best tested unilateral deviation, per round | which            |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.00591 | boundary_ride    |                                    0     |                                        0.60841 |                                 -0.05323 |                                           0.60585 |
| pl_rawprice   |                                       0.01231 | primary_shade_05 |                                    0     |                                        0.63429 |                                 -0.10631 |                                           0.65084 |
| pl_runnerup   |                                       0.01238 | primary_shade_05 |                                    0     |                                        0.57688 |                                 -0.10631 |                                           0.53828 |
| pl_nofallback |                                       0.01244 | primary_shade_05 |                                    0     |                                        0.57688 |                                 -0.10631 |                                           0.53828 |
| pl_mesp       |                                       0.01245 | primary_shade_05 |                                    0     |                                        0.57688 |                                 -0.10631 |                                           0.53828 |
| pl_windowed   |                                       0.03823 | primary_shade_15 |                                    0     |                                        0.57688 |                                 -0.10631 |                                           0.53828 |
| pl_noslack    |                                       0.11589 | bid_zero         |                                    0.995 |                                        0.68208 |                                 -0.10631 |                                           0.53828 |
| pl_nomonitor  |                                       0.13721 | bait_switch      |                                    0     |                                        0.57688 |                                 -0.10631 |                                           0.53828 |

#### rotating_top, n = 20000, Q = 3

| rung          |   best tested unilateral deviation, per round | which         |   switch rate under the proposed profile |   revenue per round under the proposed profile |   worst joint honest headroom, per round |   mean announced price under the proposed profile |
|:--|--:|:--|--:|--:|--:|--:|
| pl_shared     |                                       0.00603 | boundary_ride |                                    0     |                                        0.53963 |                                 -0.05296 |                                           0.5311  |
| pl_mesp       |                                       0.08451 | bid_zero      |                                    0     |                                        0.5955  |                                 -0.15923 |                                           0.53733 |
| pl_runnerup   |                                       0.08451 | bid_zero      |                                    0     |                                        0.5955  |                                 -0.15923 |                                           0.53733 |
| pl_nofallback |                                       0.08451 | bid_zero      |                                    0     |                                        0.5955  |                                 -0.15923 |                                           0.53733 |
| pl_windowed   |                                       0.08451 | bid_zero      |                                    0     |                                        0.5955  |                                 -0.15923 |                                           0.53733 |
| pl_nomonitor  |                                       0.09478 | bait_switch   |                                    0     |                                        0.5955  |                                 -0.15923 |                                           0.53733 |
| pl_rawprice   |                                       0.10437 | bid_zero      |                                    0     |                                        0.62526 |                                 -0.15923 |                                           0.64989 |
| pl_noslack    |                                       0.18063 | bid_zero      |                                    0.985 |                                        0.63637 |                                 -0.15923 |                                           0.53733 |

### Monitor detection delay against the first-order formula (PL-MESP only)

| family                |     n |   Q | behavior                     |   shortfall |   median delay |   first-order prediction |   ratio |
|:--|--:|--:|:--|--:|--:|--:|--:|
| heterogeneous         | 20000 |   1 | bait_switch                  |       0.438 |         106    |                  105.238 |   1.007 |
| heterogeneous         | 20000 |   1 | joint:bait_switch            |       0.438 |         106    |                  105.238 |   1.007 |
| heterogeneous         | 20000 |   1 | joint:primary_shade_15       |       0.15  |         880.5  |                  895.713 |   0.983 |
| heterogeneous         | 20000 |   1 | joint:trigger_fallback_shade |       0.438 |         106    |                  105.238 |   1.007 |
| heterogeneous         | 20000 |   1 | primary_shade_05             |       0.05  |        7840    |                 8061.42  |   0.973 |
| heterogeneous         | 20000 |   1 | primary_shade_15             |       0.15  |         880.5  |                  895.713 |   0.983 |
| heterogeneous         | 20000 |   1 | trigger_fallback_shade       |       0.438 |         106    |                  105.238 |   1.007 |
| heterogeneous         | 20000 |   2 | bait_switch                  |       0.463 |         105    |                   93.944 |   1.118 |
| heterogeneous         | 20000 |   2 | joint:bait_switch            |       0.463 |          95.5  |                   93.944 |   1.017 |
| heterogeneous         | 20000 |   2 | joint:primary_shade_15       |       0.15  |         891.25 |                  895.713 |   0.995 |
| heterogeneous         | 20000 |   2 | joint:trigger_fallback_shade |       0.463 |          95.5  |                   93.944 |   1.017 |
| heterogeneous         | 20000 |   2 | primary_shade_05             |       0.05  |        4646.5  |                 8061.42  |   0.576 |
| heterogeneous         | 20000 |   2 | primary_shade_15             |       0.15  |         894    |                  895.713 |   0.998 |
| heterogeneous         | 20000 |   2 | trigger_fallback_shade       |       0.463 |         105    |                   93.944 |   1.118 |
| heterogeneous         | 20000 |   3 | bait_switch                  |       0.504 |          82.5  |                   79.313 |   1.04  |
| heterogeneous         | 20000 |   3 | joint:bait_switch            |       0.504 |          86    |                   79.313 |   1.084 |
| heterogeneous         | 20000 |   3 | joint:primary_shade_15       |       0.15  |         868    |                  895.713 |   0.969 |
| heterogeneous         | 20000 |   3 | joint:trigger_fallback_shade |       0.504 |          86    |                   79.313 |   1.084 |
| heterogeneous         | 20000 |   3 | primary_shade_15             |       0.15  |         864.75 |                  895.713 |   0.965 |
| heterogeneous         | 20000 |   3 | trigger_fallback_shade       |       0.504 |          82.5  |                   79.313 |   1.04  |
| regime_switch         | 20000 |   2 | bait_switch                  |       0.512 |         141    |                   76.741 |   1.837 |
| regime_switch         | 20000 |   2 | joint:bait_switch            |       0.512 |         141    |                   76.741 |   1.837 |
| regime_switch         | 20000 |   2 | joint:primary_shade_15       |       0.15  |         878.25 |                  895.713 |   0.981 |
| regime_switch         | 20000 |   2 | joint:trigger_fallback_shade |       0.512 |         141    |                   76.741 |   1.837 |
| regime_switch         | 20000 |   2 | primary_shade_05             |       0.05  |        4905    |                 8061.42  |   0.608 |
| regime_switch         | 20000 |   2 | primary_shade_15             |       0.15  |         878.25 |                  895.713 |   0.981 |
| regime_switch         | 20000 |   2 | trigger_fallback_shade       |       0.512 |         141    |                   76.741 |   1.837 |
| regime_switch         | 20000 |   4 | bait_switch                  |       0.512 |          37.5  |                   76.981 |   0.487 |
| regime_switch         | 20000 |   4 | joint:bait_switch            |       0.512 |          37.5  |                   76.981 |   0.487 |
| regime_switch         | 20000 |   4 | joint:trigger_fallback_shade |       0.512 |          37.5  |                   76.981 |   0.487 |
| regime_switch         | 20000 |   4 | trigger_fallback_shade       |       0.512 |          37.5  |                   76.981 |   0.487 |
| replicated_honest_top | 20000 |   2 | bait_switch                  |       0.588 |          53    |                   58.314 |   0.909 |
| replicated_honest_top | 20000 |   2 | joint:bait_switch            |       0.588 |          53    |                   58.314 |   0.909 |
| replicated_honest_top | 20000 |   2 | joint:primary_shade_15       |       0.15  |         744    |                  895.713 |   0.831 |
| replicated_honest_top | 20000 |   2 | joint:trigger_fallback_shade |       0.588 |          53    |                   58.314 |   0.909 |
| replicated_honest_top | 20000 |   2 | primary_shade_15             |       0.15  |         744    |                  895.713 |   0.831 |
| replicated_honest_top | 20000 |   2 | trigger_fallback_shade       |       0.588 |          53    |                   58.314 |   0.909 |
| replicated_honest_top | 20000 |   3 | bait_switch                  |       0.587 |          55    |                   58.455 |   0.941 |
| replicated_honest_top | 20000 |   3 | joint:bait_switch            |       0.587 |          55    |                   58.455 |   0.941 |
| replicated_honest_top | 20000 |   3 | joint:primary_shade_15       |       0.15  |        1160    |                  895.713 |   1.295 |
| replicated_honest_top | 20000 |   3 | joint:trigger_fallback_shade |       0.587 |          55    |                   58.455 |   0.941 |
| replicated_honest_top | 20000 |   3 | primary_shade_15             |       0.15  |        1160    |                  895.713 |   1.295 |
| replicated_honest_top | 20000 |   3 | trigger_fallback_shade       |       0.587 |          55    |                   58.455 |   0.941 |
| replicated_tied_top   | 20000 |   1 | bait_switch                  |       0.682 |          44    |                   43.393 |   1.014 |
| replicated_tied_top   | 20000 |   1 | joint:bait_switch            |       0.682 |          44    |                   43.393 |   1.014 |
| replicated_tied_top   | 20000 |   1 | joint:primary_shade_15       |       0.15  |         858    |                  895.713 |   0.958 |
| replicated_tied_top   | 20000 |   1 | joint:trigger_fallback_shade |       0.682 |          44    |                   43.393 |   1.014 |
| replicated_tied_top   | 20000 |   1 | primary_shade_05             |       0.05  |        7402    |                 8061.42  |   0.918 |
| replicated_tied_top   | 20000 |   1 | primary_shade_15             |       0.15  |         851    |                  895.713 |   0.95  |
| replicated_tied_top   | 20000 |   1 | trigger_fallback_shade       |       0.682 |          44    |                   43.393 |   1.014 |
| replicated_tied_top   | 20000 |   2 | bait_switch                  |       0.682 |          44    |                   43.38  |   1.014 |
| replicated_tied_top   | 20000 |   2 | joint:bait_switch            |       0.682 |          44    |                   43.38  |   1.014 |
| replicated_tied_top   | 20000 |   2 | joint:primary_shade_15       |       0.15  |         885.5  |                  895.713 |   0.989 |
| replicated_tied_top   | 20000 |   2 | joint:trigger_fallback_shade |       0.682 |          44    |                   43.38  |   1.014 |
| replicated_tied_top   | 20000 |   2 | primary_shade_05             |       0.05  |        4688    |                 8061.42  |   0.582 |
| replicated_tied_top   | 20000 |   2 | primary_shade_15             |       0.15  |         886.5  |                  895.713 |   0.99  |
| replicated_tied_top   | 20000 |   2 | trigger_fallback_shade       |       0.682 |          44    |                   43.38  |   1.014 |
| replicated_tied_top   | 20000 |   3 | bait_switch                  |       0.682 |          44    |                   43.388 |   1.014 |
| replicated_tied_top   | 20000 |   3 | joint:bait_switch            |       0.682 |          44    |                   43.388 |   1.014 |
| replicated_tied_top   | 20000 |   3 | joint:primary_shade_15       |       0.15  |         862.5  |                  895.713 |   0.963 |
| replicated_tied_top   | 20000 |   3 | joint:trigger_fallback_shade |       0.682 |          44    |                   43.388 |   1.014 |
| replicated_tied_top   | 20000 |   3 | primary_shade_15             |       0.15  |         869.5  |                  895.713 |   0.971 |
| replicated_tied_top   | 20000 |   3 | trigger_fallback_shade       |       0.682 |          44    |                   43.388 |   1.014 |
| replicated_unique_top | 20000 |   1 | bait_switch                  |       0.538 |          70    |                   69.588 |   1.006 |
| replicated_unique_top | 20000 |   1 | joint:bait_switch            |       0.538 |          70    |                   69.588 |   1.006 |
| replicated_unique_top | 20000 |   1 | joint:primary_shade_15       |       0.15  |         856    |                  895.713 |   0.956 |
| replicated_unique_top | 20000 |   1 | joint:trigger_fallback_shade |       0.538 |          70    |                   69.588 |   1.006 |
| replicated_unique_top | 20000 |   1 | primary_shade_05             |       0.05  |        7759    |                 8061.42  |   0.962 |
| replicated_unique_top | 20000 |   1 | primary_shade_15             |       0.15  |         856    |                  895.713 |   0.956 |
| replicated_unique_top | 20000 |   1 | trigger_fallback_shade       |       0.538 |          70    |                   69.588 |   1.006 |
| replicated_unique_top | 20000 |   2 | bait_switch                  |       0.537 |          70.5  |                   69.801 |   1.01  |
| replicated_unique_top | 20000 |   2 | joint:bait_switch            |       0.537 |          70.5  |                   69.801 |   1.01  |
| replicated_unique_top | 20000 |   2 | joint:primary_shade_15       |       0.15  |         889.75 |                  895.713 |   0.993 |
| replicated_unique_top | 20000 |   2 | joint:trigger_fallback_shade |       0.537 |          70.5  |                   69.801 |   1.01  |
| replicated_unique_top | 20000 |   2 | primary_shade_05             |       0.05  |        4763.5  |                 8061.42  |   0.591 |
| replicated_unique_top | 20000 |   2 | primary_shade_15             |       0.15  |         889.75 |                  895.713 |   0.993 |
| replicated_unique_top | 20000 |   2 | trigger_fallback_shade       |       0.537 |          70.5  |                   69.801 |   1.01  |
| replicated_unique_top | 20000 |   3 | bait_switch                  |       0.537 |          70    |                   69.82  |   1.003 |
| replicated_unique_top | 20000 |   3 | joint:bait_switch            |       0.537 |          70    |                   69.82  |   1.003 |
| replicated_unique_top | 20000 |   3 | joint:primary_shade_15       |       0.15  |         863.5  |                  895.713 |   0.964 |
| replicated_unique_top | 20000 |   3 | joint:trigger_fallback_shade |       0.537 |          70    |                   69.82  |   1.003 |
| replicated_unique_top | 20000 |   3 | primary_shade_15             |       0.15  |         863.5  |                  895.713 |   0.964 |
| replicated_unique_top | 20000 |   3 | trigger_fallback_shade       |       0.537 |          70    |                   69.82  |   1.003 |
| rotating_top          | 20000 |   1 | bait_switch                  |       0.538 |          70    |                   69.588 |   1.006 |
| rotating_top          | 20000 |   1 | joint:bait_switch            |       0.538 |          70    |                   69.588 |   1.006 |
| rotating_top          | 20000 |   1 | joint:primary_shade_15       |       0.15  |         856    |                  895.713 |   0.956 |
| rotating_top          | 20000 |   1 | joint:trigger_fallback_shade |       0.538 |          70    |                   69.588 |   1.006 |
| rotating_top          | 20000 |   1 | primary_shade_05             |       0.05  |        7759    |                 8061.42  |   0.962 |
| rotating_top          | 20000 |   1 | primary_shade_15             |       0.15  |         856    |                  895.713 |   0.956 |
| rotating_top          | 20000 |   1 | trigger_fallback_shade       |       0.538 |          70    |                   69.588 |   1.006 |
| rotating_top          | 20000 |   2 | bait_switch                  |       0.538 |          70    |                   69.556 |   1.006 |
| rotating_top          | 20000 |   2 | joint:bait_switch            |       0.538 |          70    |                   69.556 |   1.006 |
| rotating_top          | 20000 |   2 | joint:primary_shade_15       |       0.15  |         890    |                  895.713 |   0.994 |
| rotating_top          | 20000 |   2 | joint:trigger_fallback_shade |       0.538 |          70    |                   69.556 |   1.006 |
| rotating_top          | 20000 |   2 | primary_shade_05             |       0.05  |        4693    |                 8061.42  |   0.582 |
| rotating_top          | 20000 |   2 | primary_shade_15             |       0.15  |         895    |                  895.713 |   0.999 |
| rotating_top          | 20000 |   2 | trigger_fallback_shade       |       0.538 |          70    |                   69.556 |   1.006 |
| rotating_top          | 20000 |   3 | bait_switch                  |       0.537 |          70.5  |                   69.803 |   1.01  |
| rotating_top          | 20000 |   3 | joint:bait_switch            |       0.537 |          70    |                   69.803 |   1.003 |
| rotating_top          | 20000 |   3 | joint:primary_shade_15       |       0.15  |         874    |                  895.713 |   0.976 |
| rotating_top          | 20000 |   3 | joint:trigger_fallback_shade |       0.537 |          70    |                   69.803 |   1.003 |
| rotating_top          | 20000 |   3 | primary_shade_15             |       0.15  |         863.75 |                  895.713 |   0.964 |
| rotating_top          | 20000 |   3 | trigger_fallback_shade       |       0.537 |          70.5  |                   69.803 |   1.01  |

### Deviation search: best searched gain against the certified interval

grid: delta in [np.float64(0.0), np.float64(0.05), np.float64(0.1), np.float64(0.125), np.float64(0.15), np.float64(0.2), np.float64(0.3), np.float64(0.5), np.float64(0.7), np.float64(1.0)], c in [np.float64(0.0), np.float64(0.25), np.float64(0.5), np.float64(0.75), np.float64(1.0), np.float64(1.5)]; 200 paired replicates per point

The check that is exact on both sides compares the searched VALUE with the certified upper bound
on the value, V_FUB. Comparing a simulated GAIN with the certified gain interval is not valid: it
subtracts a noisy baseline from an exact bound, and at the cells where the certified optimum is
deterministic it produces spurious exceedances of about a tenth of a percent.

points at which the searched VALUE exceeds V_FUB: 0 of 1080

| source                          | family                |     n |   Q |   best_delta |   best_c |   best_searched_gain |       lo |       hi |   certified_LB |   certified_UB |   fraction_of_certified_LB |   searched_value |   V_FUB |   value_exceeds_V_FUB |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| search_regime_switch_v2         | regime_switch         |  8000 |   1 |         0    |      1.5 |              187.598 |  160.682 |  214.514 |        325.143 |        474.467 |                      0.577 |          2512.53 | 2799.8  |                     0 |
| search_regime_switch_v2         | regime_switch         |  8000 |   2 |         0    |      1.5 |              207.149 |  202.483 |  211.814 |        377.168 |        622.672 |                      0.549 |          2668.82 | 3096.03 |                     0 |
| search_regime_switch_v2         | regime_switch         |  8000 |   3 |         1    |      0   |             1808.57  | 1807.01  | 1810.12  |       1807.97  |       1807.97  |                      1     |          2844.6  | 2844.6  |                     0 |
| search_regime_switch_v2         | regime_switch         | 20000 |   1 |         0    |      1.5 |              325.986 |  279.697 |  372.275 |        584.621 |        825.758 |                      0.558 |          6118.6  | 6626.47 |                     0 |
| search_regime_switch_v2         | regime_switch         | 20000 |   2 |         0    |      1.5 |              408.347 |  395.385 |  421.309 |        696.286 |       1167.4   |                      0.586 |          7770.7  | 8539.42 |                     0 |
| search_regime_switch_v2         | regime_switch         | 20000 |   3 |         1    |      0   |              961.225 |  956.589 |  965.862 |       1873.99  |       2100.95  |                      0.513 |          5392.2  | 6527.65 |                     0 |
| search_replicated_tied_top_v2   | replicated_tied_top   |  8000 |   1 |         0    |      1.5 |               80.822 |   50.821 |  110.823 |        162.745 |        236.411 |                      0.497 |          1534.01 | 1728.43 |                     0 |
| search_replicated_tied_top_v2   | replicated_tied_top   |  8000 |   2 |         1    |      0   |              690.268 |  625.605 |  754.93  |        734.923 |        734.923 |                      0.939 |          1896.4  | 1896.4  |                     0 |
| search_replicated_tied_top_v2   | replicated_tied_top   |  8000 |   3 |         1    |      0   |             2015.03  | 2010.92  | 2019.14  |       2013.67  |       2013.67  |                      1.001 |          2844.6  | 2844.6  |                     0 |
| search_replicated_tied_top_v2   | replicated_tied_top   | 20000 |   1 |         0    |      1.5 |              159.937 |  124.239 |  195.636 |        281.451 |        401.044 |                      0.568 |          3704.41 | 4047.81 |                     0 |
| search_replicated_tied_top_v2   | replicated_tied_top   | 20000 |   2 |         1    |      0   |              443.533 |  230.663 |  656.403 |        534.388 |        695.612 |                      0.83  |          3594.8  | 3807.71 |                     0 |
| search_replicated_tied_top_v2   | replicated_tied_top   | 20000 |   3 |         1    |      0   |             2795.03  | 2704.13  | 2885.93  |       2814.78  |       2814.78  |                      0.993 |          5392.2  | 5392.2  |                     0 |
| search_replicated_unique_top_v2 | replicated_unique_top |  8000 |   1 |         0.15 |      1.5 |              334.974 |  314.567 |  355.38  |        484.416 |        632.004 |                      0.692 |          3739.44 | 4041.74 |                     0 |
| search_replicated_unique_top_v2 | replicated_unique_top |  8000 |   2 |         0.2  |      1.5 |              534.635 |  513.7   |  555.571 |        671.833 |        959.698 |                      0.796 |          2571.13 | 2995.52 |                     0 |
| search_replicated_unique_top_v2 | replicated_unique_top |  8000 |   3 |         1    |      0   |             2182.96  | 2182.65  | 2183.27  |       2182.69  |       2182.69  |                      1     |          2844.6  | 2844.6  |                     0 |
| search_replicated_unique_top_v2 | replicated_unique_top | 20000 |   1 |         0.2  |      1.5 |              572.136 |  452.037 |  692.235 |        893.126 |       1132.15  |                      0.641 |          9380.89 | 9952.5  |                     0 |
| search_replicated_unique_top_v2 | replicated_unique_top | 20000 |   2 |         0.2  |      1.5 |             1060.78  | 1043.55  | 1078     |       1335.82  |       1808.69  |                      0.794 |          7441.55 | 8198.17 |                     0 |
| search_replicated_unique_top_v2 | replicated_unique_top | 20000 |   3 |         1    |      0   |             1432.48  | 1427.38  | 1437.57  |       1626.46  |       2321.59  |                      0.881 |          5392.2  | 6280.19 |                     0 |

### CG-MESP: the horizon at which each guarantee first says anything (analytic)

|   D |   log10_n_price_positive |   log10_n_A_below_n |   log10_n_B_below_n |   log10_n_C_below_n |   log10_n_all_three |   log10_n_public_En_below_n |
|--:|--:|--:|--:|--:|--:|--:|
|   1 |                      6.1 |                 5.2 |                 6.8 |                 7.1 |                 7.1 |                         2.9 |
|   2 |                      8.5 |                 7.5 |                 9.3 |                 9.8 |                 9.8 |                         3.7 |
|   3 |                     11.1 |                10   |                12   |                12.6 |                12.6 |                         4.7 |
|   4 |                     13.7 |                12.7 |                14.9 |                15.5 |                15.5 |                         5.7 |
|   5 |                     16.5 |                15.5 |                17.8 |                18.6 |                18.6 |                         6.5 |
|   6 |                     19.4 |                18.4 |                20.8 |                21.7 |                21.7 |                         7.4 |
|   7 |                     22.4 |                21.4 |                23.9 |                24.9 |                24.9 |                         9.1 |
|   8 |                     25.4 |                24.4 |                27.1 |                28.2 |                28.2 |                         9.6 |
|   9 |                     28.5 |                27.5 |                30.3 |                31.6 |                31.6 |                        11   |
|  10 |                     31.7 |                30.7 |                33.7 |                35   |                35   |                        11.4 |
|  11 |                     34.9 |                33.9 |                37   |                38.5 |                38.5 |                        13.4 |
|  12 |                     38.2 |                37.2 |                40.5 |                42   |                42   |                        13.9 |

### CG-MESP at runnable horizons (analytic)

|   D |         n |   g_n |   J_n |   L_n |    s_n |   rho_n |   sigma_n |   price_clipped_to_zero |   K_J_L_over_n |   boundA_over_n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
|   2 |      1000 |     4 |    16 |    16 | 1.0596 |  2.7958 |    5.9745 |                       1 |         0.512  |          6.9434 |
|   2 |     10000 |     7 |    49 |    40 | 0.77   |  2.0628 |    4.3729 |                       1 |         0.392  |          4.4218 |
|   2 |    100000 |    11 |   121 |   101 | 0.5402 |  1.6087 |    3.2294 |                       1 |         0.2444 |          2.8061 |
|   2 |   1000000 |    16 |   256 |   252 | 0.3739 |  1.3095 |    2.4313 |                       1 |         0.129  |          1.8721 |
|   2 |  10000000 |    26 |   676 |   631 | 0.2549 |  0.9311 |    1.6957 |                       1 |         0.0853 |          1.2342 |
|   2 | 100000000 |    40 |  1600 |  1585 | 0.1717 |  0.6866 |    1.2018 |                       1 |         0.0507 |          0.8412 |
|   3 |      1000 |     4 |    64 |    10 | 1.3402 |  3.4242 |    7.4449 |                       1 |         1      |         12.8523 |
|   3 |     10000 |     5 |   125 |    22 | 1.0383 |  3.537  |    6.652  |                       1 |         0.55   |          7.4565 |
|   3 |    100000 |     7 |   343 |    47 | 0.7919 |  3.0961 |    5.4719 |                       1 |         0.3224 |          5.1369 |
|   3 |   1000000 |    10 |  1000 |   100 | 0.5936 |  2.5661 |    4.3468 |                       1 |         0.2    |          3.6798 |
|   3 |  10000000 |    15 |  3375 |   216 | 0.4356 |  1.9766 |    3.2835 |                       1 |         0.1458 |          2.6443 |
|   3 | 100000000 |    22 | 10648 |   465 | 0.3171 |  1.529  |    2.4802 |                       1 |         0.099  |          1.9168 |

### CG-MESP, structural regime: lemmas and the three inequalities (cg_structural.json)

| inst   |      n |   K |   g |    L |   J |   awarded |   mean_tau |   viol_P2 |   viol_P4 |   switches |   false_switches |   best_searched_gain |   boundA |   A_holds |   revenue_deficit_B |   slackB |   B_holds |   honest_deficit_C |   slackC |   C_holds |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| C      | 200000 |   2 |   3 | 4000 |   9 |         9 |     0.4932 |         0 |         0 |          0 |                0 |              5752.38 |    81694 |         1 |            32676.8  |   150206 |         1 |           -6792.67 |   192129 |         1 |
| C      | 400000 |   2 |   3 | 8000 |   9 |         9 |     0.5687 |         0 |         0 |          0 |                0 |              9903.05 |   140344 |         1 |            45669.4  |   261755 |         1 |          -13556.3  |   322557 |         1 |
| D      | 200000 |   3 |   3 | 2500 |  27 |         4 |     0.4222 |         0 |         0 |          0 |                0 |              5182.02 |   169443 |         1 |            -9520.96 |   298911 |         1 |            7414.17 |   396234 |         1 |
| E      | 200000 |   2 |   3 | 4000 |   9 |         9 |     0.2206 |         0 |         0 |          0 |                0 |              1511.57 |   132606 |         1 |            65932.7  |   218088 |         1 |          -10637    |   276982 |         1 |
| E      | 400000 |   2 |   4 | 5000 |  16 |        16 |     0.3139 |         0 |         0 |          0 |                0 |              3106.08 |   241115 |         1 |           103463    |   403006 |         1 |          -23935.2  |   507552 |         1 |
| F      | 200000 |   3 |   3 | 2500 |  27 |         4 |     0.2828 |         0 |         0 |          0 |                0 |              5495.68 |   179835 |         1 |            -9490.86 |   312767 |         1 |           96548.8  |   413555 |         1 |

### CG-MESP, necessity of the oscillation allowance (cg_oscillation.json)

| inst   |      n |   g |    L |   osc_mult |   awarded_cubes |   viol_P2 |   viol_P4 |   P2_violation_rate |   P4_violation_rate |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| E      | 200000 |   3 | 4000 |       0    |              54 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   3 | 4000 |       0.25 |              54 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   3 | 4000 |       0.5  |              54 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   3 | 4000 |       1    |              54 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   3 | 4000 |       2    |              54 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   3 | 4000 |       3    |              54 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   6 | 2000 |       0    |             216 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   6 | 2000 |       0.25 |             216 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   6 | 2000 |       0.5  |             216 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   6 | 2000 |       1    |             216 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   6 | 2000 |       2    |             216 |         0 |         0 |                   0 |                   0 |
| E      | 200000 |   6 | 2000 |       3    |             216 |         0 |         0 |                   0 |                   0 |

### CG-MESP, the mechanism at its own tuned parameters (cg_tuned.json)

| inst   |       n |   K |   D |   g |   L |    J |      h |      s |    rho |   sigma |   mean_tau |   zero_price_share |   awarded |   switches |    rev |         bench_M2 |   bench_honest |   stage1 |           boundA |           slackB |           slackC |   revenue_per_round |   bench_M2_per_round |   stage1_share |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| C      |   20000 |   2 |   2 |   8 |  53 |   64 | 0.125  | 0.693  | 1.9275 |  4.0064 |          0 |                  1 |        64 |          0 |   5922 |  15799.3         |           6000 |     6784 |  76856.3         | 113622           | 161387           |              0.2961 |               0.79   |         0.3392 |
| C      |  200000 |   2 |   2 |  12 | 132 |  144 | 0.0833 | 0.4862 | 1.5564 |  3.0151 |          0 |                  1 |       144 |          0 |  32960 | 158001           |          60000 |    38016 | 496107           | 842033           |      1.11162e+06 |              0.1648 |               0.79   |         0.1901 |
| C      | 2000000 |   2 |   2 |  19 | 332 |  361 | 0.0526 | 0.3337 | 1.1543 |  2.1554 |          0 |                  1 |       361 |          0 | 208141 |      1.58001e+06 |         600000 |   239704 |      3.26974e+06 |      5.98737e+06 |      7.59813e+06 |              0.1041 |               0.79   |         0.1199 |
| D      |   20000 |   3 |   3 |   6 |  28 |  216 | 0.1667 | 0.9572 | 3.1476 |  6.0192 |          0 |                  1 |       174 |          0 |  15119 |  15815.4         |           6000 |    17900 | 170736           | 178655           | 301376           |              0.756  |               0.7908 |         0.895  |
| D      |  200000 |   3 |   3 |   8 |  59 |  512 | 0.125  | 0.7297 | 2.8592 |  5.0482 |          0 |                  1 |       512 |          0 |  76158 | 158170           |          60000 |    90624 |      1.06458e+06 |      1.4368e+06  |      2.08994e+06 |              0.3808 |               0.7909 |         0.4531 |
| D      | 2000000 |   3 |   3 |  12 | 126 | 1728 | 0.0833 | 0.5431 | 2.2385 |  3.8678 |          0 |                  1 |      1728 |          0 | 548553 |      1.58166e+06 |         600000 |   653184 |      7.3233e+06  |      1.09674e+07 |      1.50884e+07 |              0.2743 |               0.7908 |         0.3266 |
| E      |   20000 |   2 |   2 |   8 |  53 |   64 | 0.125  | 0.693  | 1.9275 |  4.0064 |          0 |                  1 |        64 |          0 |   7235 |  15336.1         |           5000 |     6784 |  76856.3         | 113622           | 161387           |              0.3618 |               0.7668 |         0.3392 |
| E      |  200000 |   2 |   2 |  12 | 132 |  144 | 0.0833 | 0.4862 | 1.5564 |  3.0151 |          0 |                  1 |       144 |          0 |  50538 | 153337           |          50000 |    38016 | 496107           | 842033           |      1.11162e+06 |              0.2527 |               0.7667 |         0.1901 |
| E      | 2000000 |   2 |   2 |  19 | 332 |  361 | 0.0526 | 0.3337 | 1.1543 |  2.1554 |          0 |                  1 |       361 |          0 | 413169 |      1.5334e+06  |         500000 |   239704 |      3.26974e+06 |      5.98737e+06 |      7.59813e+06 |              0.2066 |               0.7667 |         0.1199 |
