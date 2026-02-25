# Supplementary S1 — BehaviorSpace configurations

This document records the exact BehaviorSpace experiments used for the manuscript.

**NetLogo version used:** 7.0.3  
**Model:** `code/LANA_VALIDATION.nlogox`  
**Reproducibility:** all experiments were run with explicit `SEED` values.

---

## Summary of experiments

| ID | Phase | Purpose | Parameter sweep | Seeds | Ticks | BehaviorSpace runs | Notes |
|----|------:|---------|-----------------|------:|------:|-------------------:|------|
| V1 | 1 | Synaptic delay propagation (chain) | `FIXED-DELAY ∈ {1,2,3,4,5}` | 10 | 200 | 50 | 11‑neuron chain, single stimulus |
| V2 | 1 | Environmental decay operator | `RHO = 0.01` (fixed), `D=0`, `E0=5` | 10 | 300 | 10 | **3,010 time‑series samples** (10 runs × 301 ticks) used for the decay fit |
| V3 | 1 | Signal distance‑attenuation operator | `GAMMA ∈ {0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0}` × `BETA ∈ {0.5, 0.8, 0.95}`; `N-NODES=100`; `KAPPA-E=0`; `D=0`; `THRESHOLD=1.5` | 20 | 500 | 480 | standard network; isolates the signal reach channel; BehaviorSpace: `Vx_signal_attenuation` |
| V4 | 1 | E-field diffusion operator | `D ∈ {0.0, 0.0333…, 0.0666…, 0.1, 0.1333…, 0.1666…, 0.2}`; `RHO=0`; hot spot at origin (`E=100` at (0,0) on baseline field `E0=5`) | 10 | 500 | 70 | diffusion redistributes without loss (mean E conserved); BehaviorSpace: `Vx_diffusion_operator` |
| M1 | 2 | Threshold bifurcation | `STIM-AMP ∈ {0.1,…,3.0}` (Δ=0.1) | 10 | 200 | 300 | single neuron; direct membrane stimulus every `REPEAT-K` |
| M2 | 2 | Refractory enforcement | `POp ∈ {5,10,15,20,25}` | 10 | 500 | 50 | outputs: global min ISI |
| E1 | 3 | Weight gating vs propagation | `FIXED-W ∈ {0.5,1.0,1.5,2.0,2.5}` | 20 | 200 | 100 | chain with `FIXED-DELAY=1` |
| N1 | 4 | EI balance | `INHIB-FRAC ∈ {0.0,0.1,0.2,0.3,0.4}` | 30 | 500 | 150 | outputs: FR, Fano, synchrony |
| N2 | 4 | Coupling-driven regime shift | `KAPPA-E ∈ {0.0,0.2,…,2.0}` (Δ=0.2) | 20 | 500 | 220 | outputs: FR, CV, oscillatory flag |
| GSA | 5 | Factorial sensitivity screening | `KAPPA-E (5) × RHO (3) × THRESHOLD (3)` | 10 | 500 | 450 | full factorial |
| R1 | R | Network size robustness | `N-NODES ∈ {50,100,150,200,250}` | 20 | 500 | 100 | outputs: FR, CV, synchrony |
| R2 | R | Plasticity convergence | plasticity on (default) | 20 | 2000 | 20 | long runs |

---

## Output files

Raw exports are stored in `data/raw/` with one file per experiment:

- `V1_chain_delay.csv`
- `V2_energy_decay.csv`
- `V3_signal_attenuation.csv`
- `V4_diffusion_operator.csv`
- `M1_threshold_bifurcation.csv`
- `M2_refractory.csv`
- `E1_weight_speed.csv`
- `N1_ei_balance.csv`
- `N2_phase_transition.csv`
- `GSA_sensitivity.csv`
- `R1_network_size.csv`
- `R2_plasticity.csv`