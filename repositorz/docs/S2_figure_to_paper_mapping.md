# S2: Figure and Table Mapping

## Figures

| File | Paper Reference | Test | Description |
|:-----|:---------------|:-----|:------------|
| Fig01_LANA_architecture.png | Figure 1 | — | Model architecture diagram |
| Fig02_V1_chain_delay_speed.png | Figure 2 | V1 | Chain delay: speed = 1/delay |
| Fig03_V2_energy_decay.png | Figure 3 | V2 | Energy field decay vs theory |
| Fig04_M1_threshold_bifurcation.png | Figure 4 | M1 | Firing rate bifurcation |
| Fig05_M2_refractory.png | Figure 5 | M2 | Min ISI = POp + 1 |
| Fig06_N1_ei_balance.png | Figure 6 | N1 | FR vs inhibitory fraction |
| Fig07_N2_phase_transition.png | Figure 7 | N2 | CV and oscillation vs κ_E |
| Fig08_GSA_sensitivity.png | Figure 8 | GSA | Main effect sizes (%) |
| Fig09_R1_network_size.png | Figure 9 | R1 | FR convergence with N |
| Fig10_R2_plasticity_convergence.png | Figure 10 | R2 | Weight decay over 2000 ticks |

## Tables

| Paper Table | Test | Contents |
|:-----------|:-----|:---------|
| Table 1 | All | V&V experiment overview and pass criteria |
| Table 2 | V1 | Chain delay verification results |
| Table 2A | V1, V2, V3, V4 | Analytical reference solution comparison |
| Table 3 | M2 | Refractory period results |
| Table 4 | E1 | Weight gating results |
| Table 5 | N1 | EI balance summary statistics |
| Table 6 | N2 | Phase transition summary |
| Table 7 | GSA | Main effect sizes (%) |
| Table 8 | R1 | Network size robustness |
| Table A1 | — | Model parameters (Appendix) |

## Data Files

| CSV File | Test | Paper Section |
|:---------|:-----|:-------------|
| V1_chain_delay.csv | V1 | Phase 1 |
| V2_energy_decay.csv | V2 | Phase 1 |
| V3_signal_attenuation.csv | V3 | Phase 1 |
| V4_diffusion_operator.csv | V4 | Phase 1 |
| M1_threshold_bifurcation.csv | M1 | Phase 2 |
| M2_refractory.csv | M2 | Phase 2 |
| E1_weight_speed.csv | E1 | Phase 3 |
| N1_ei_balance.csv | N1 | Phase 4 |
| N2_phase_transition.csv | N2 | Phase 4 |
| GSA_sensitivity.csv | GSA | Phase 5 |
| R1_network_size.csv | R1 | Robustness |
| R2_plasticity.csv | R2 | Robustness |


## Supplementary figures

- **FigS1_M1_cross_implementation** — Cross‑implementation check for the analytic single‑neuron threshold (Supplementary material; supports the M1 test).