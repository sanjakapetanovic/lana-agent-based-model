# LANA :: Local Adaptive Neural Agents

Kapetanović S., Dželalija M., Bijedić N., Gašpar D., Tipurić-Spužević S.

Archived release (Zenodo DOI): [https://doi.org/10.5281/zenodo.19085845](https://doi.org/10.5281/zenodo.19085845)
---
## Overview

LANA is a NetLogo-based agent-based spiking neural network model that decomposes neural recruitment into four separable, independently testable components:

1. **Thresholded neuronal state** — leaky integrate-and-fire neurons with refractory periods
2. **Mobile signal transport** — spike-emitted agents that propagate through space with decay
3. **Directed delayed synaptic coupling** — distance-dependent delays with bounded STDP
4. **Activity-dependent environmental field** — diffusive gain-control variable with divisive normalization

The central contribution is architectural rather than numerical: propagation and feedback are represented as measurable, removable components rather than hidden aggregate coupling terms. Compared with general-purpose spiking simulators (Brian2, NEURON, NEST), LANA does not aim to improve efficiency or biophysical detail — its specific value is that mobile signal agents and environmental feedback remain explicit objects that can be observed, removed and audited.

---

## What is included

### 1) Model code

| File | Description |
|------|-------------|
| `code/LANA_VALIDATION.nlogox` | Original NetLogo model file with validation modes and BehaviorSpace experiments. |
| `code/LANA_VALIDATION_FINAL.nlogox` | Extended model with neuron-only baseline (`BASELINE?`), regime presets, lesion protocol, chain benchmark. |
| `code/LANA_v3.1_COMPLETE.nlogo` | v3.1 release model with corrected t50/t90, linear-regression wavefront speed, source-region reporters, 26 BehaviorSpace experiments (E0a–E6b). |
| `code/LANA_v3_1_ablation.nlogox` | **[R1]** Ablation variant with `DISABLE-E-FEEDBACK?` and `DISABLE-SIGNAL-COUPLING?` switches for component-wise ablation control. |
| `code/LANA_v3_1_eeg.nlogox` | **[R2]** EEG tick-by-tick variant with `report-spikes-this-tick`, `report-meanE-this-tick`, `report-active-this-tick` reporters and `EEG-S1-tickbytick` / `EEG-S2-tickbytick` BehaviorSpace experiments (`runMetricsEveryStep=true`). |

### 2) Raw simulation outputs

#### v3.1 manuscript experiments (~1,780 runs)

| File | Description | Runs |
|------|-------------|------|
| `data/E0a-chain-delay.csv` | Mini-V&V: delay propagation | 100 |
| `data/E0b-decay.csv` | Mini-V&V: E-field decay (per-tick) | 50 |
| `data/E0c-threshold.csv` | Mini-V&V: threshold activation | 140 |
| `data/E0d-refractory.csv` | Mini-V&V: refractory enforcement | 100 |
| `data/E0e-chain-control.csv` | Mini-V&V: chain baseline control | 80 |
| `data/E1-baseline.csv` | Full model vs neuron-only baseline (50 seeds × 2) | 100 |
| `data/E1b-calibration-sweep.csv` | Calibration sweep (20 seeds × 6 STIM-AMP levels) | 120 |
| `data/E2-propagation.csv` | Propagation benchmark (50 seeds × 2) | 100 |
| `data/E2b-calibrated-baseline.csv` | Calibrated baseline control (50 seeds × 2) | 100 |
| `data/E3-S1.csv` / `data/E3-S2.csv` | Resting vs hyperexcitable regime (50 each) | 100 |
| `data/E4-nominal.csv` + `data/E4-*.csv` | OAT sensitivity (8 parameters) | 340 |
| `data/E5-factorial.csv` | 2⁴ factorial design (16 × 20 seeds) | 320 |
| `data/E6a-baseline-N300.csv` | N=300 baseline robustness | 40 |
| `data/E6b-S1-N300.csv` / `data/E6b-S2-N300.csv` | N=300 regime robustness | 40 |

#### R1 supplementary experiments (~540 runs)

| File | Description | Runs |
|------|-------------|------|
| `data/LANA_v3_1_E1-baseline-spreadsheet.csv` | E1 raw spreadsheet export | 100 |
| `data/LANA_v3_1_E3-S1-spreadsheet.csv` | E3-S1 raw spreadsheet export | 50 |
| `data/LANA_v3_1_E3-S2-spreadsheet.csv` | E3-S2 raw spreadsheet export | 50 |
| `data/LANA_v3_1_E6a-baseline-N300-spreadsheet.csv` | N=300 baseline (Table S1) | 40 |
| `data/LANA_v3_1_E6b-S1-N300-spreadsheet.csv` | N=300 S1 (Table S1) | 20 |
| `data/LANA_v3_1_E6b-S2-N300-spreadsheet.csv` | N=300 S2 (Table S1) | 20 |
| `data/LANA_v3_1_E7-longer-horizon-full-baseline-spreadsheet.csv` | 3000-tick full vs baseline (Table S5) | 40 |
| `data/LANA_v3_1_E7-longer-horizon-S1-spreadsheet.csv` | 3000-tick S1 control (Table S5) | 20 |
| `data/LANA_v3_1_E7-longer-horizon-S2-spreadsheet.csv` | 3000-tick S2 control (Table S5) | 20 |
| `data/LANA_v3_1_E8-theta-kappa-grid-spreadsheet.csv` | Three-level θ × κ_E grid (Table S6) | 180 |

#### R1 ablation experiments (~200 runs)

| File | Description | Runs |
|------|-------------|------|
| `data/LANA_v3_1_ablation_E9a-ablation-full-spreadsheet.csv` | Full model (ablation control) | 50 |
| `data/LANA_v3_1_ablation_E9b-ablation-no-efeedback-spreadsheet.csv` | No environmental feedback | 50 |
| `data/LANA_v3_1_ablation_E9c-ablation-no-signal-coupling-spreadsheet.csv` | No direct signal-to-neuron transport | 50 |
| `data/LANA_v3_1_ablation_E9d-ablation-baseline-spreadsheet.csv` | Neuron-only baseline | 50 |

#### R2 EEG tick-by-tick time series (100 runs)

| File | Description | Runs |
|------|-------------|------|
| `data/LANA_v3_1_eeg_EEG-S1-tickbytick-spreadsheet.csv` | S1 regime: 50 seeds × 1001 ticks × 3 reporters | 50 |
| `data/LANA_v3_1_eeg_EEG-S2-tickbytick-spreadsheet.csv` | S2 regime: 50 seeds × 1001 ticks × 3 reporters | 50 |

#### R2 EEG–LANA processed outputs

| File | Description |
|------|-------------|
| `data/eeg_features_100subj.csv` | Per-subject, per-condition EEG feature matrix (100 subjects × 2 conditions = 200 rows) |
| `data/eeg_eo_vs_ec_100subj.csv` | EEG paired Wilcoxon tests (9 features, n = 100 pairs) |
| `data/lana_features_100subj.csv` | Per-seed, per-regime LANA feature matrix (50 seeds × 2 regimes = 100 rows) |
| `data/lana_s1_vs_s2_100subj.csv` | LANA paired Wilcoxon tests (12 features, n = 50 pairs) |
| `data/eeg_lana_comparison_100subj.csv` | Direction-of-change concordance (8 feature families) |
| `data/subjects_used_100subj.csv` | EEG subject inclusion/exclusion list |
| `data/parameters/LANA_parameter_table.csv` | Complete parameter table for S1 and S2 regimes |

### 3) Analysis scripts

| Script | Description |
|--------|-------------|
| `analysis_scripts/run_analysis.py` | v3.1 analysis entry point |
| `analysis_scripts/generate_all_analysis.py` | Generates Figures 2–3, 7–9 and Tables from v3.1 CSVs |
| `analysis_scripts/generate_remaining_figs.py` | Generates Figures 4–6 and remaining Tables |
| `analysis_scripts/parse_netlogo_spreadsheet.py` | Universal BehaviorSpace spreadsheet parser |
| `scripts/lana_eeg_pipeline_v5.py` | **[R2]** 100-subject EEG–LANA comparison pipeline |
| `scripts/download_eeg_100.py` | **[R2]** EEG data download from PhysioNet |
| `scripts/requirements.txt` | Python dependencies |
| `analysis/analyze_final.py` | Original V&V analysis pipeline |

### 4) Figures

#### Scientific Reports manuscript figures

| File | Description |
|------|-------------|
| `figures/Figure_1_Architecture.tiff` | LANA model architecture (600 dpi) |
| `figures/Figure_2_Baseline.png` | Full model vs nominal neuron-only baseline (E1) |
| `figures/Figure_3_Ablation.png` | Ablation and calibrated-baseline panel (E9 + E1b/E2b) |
| `figures/Figure_4_Propagation.png` | Localized propagation benchmark (E2) |
| `figures/Figure_5_Regime.png` | Regime transition and robustness (E3, E4, E5) |
| `figures/Figure_6_EEG_LANA.png` | **[R2]** 100-subject EEG–LANA feature-level benchmark |

#### R2 EEG standalone figures

| File | Description |
|------|-------------|
| `figures/Figure_EEG_Benchmark.png/.tiff` | **[R2]** EEG spectral bands, posterior alpha, additional features |
| `figures/Figure_Concordance.png/.tiff` | **[R2]** Direction-of-change concordance chart |
| `figures/Figure_Boxplots.png/.tiff` | **[R2]** LANA S1 vs S2 boxplots |
| `figures/Figure_Posterior_Alpha.png/.tiff` | **[R2]** Posterior alpha EO vs EC sanity check |
| `figures/Figure_LANA_Spectral.png/.tiff` | **[R2]** LANA spectral distribution |
| `figures/Figure_EEG_Features.png/.tiff` | **[R2]** EEG feature comparison with significance |

### 5) Supplementary Information

Tables S1–S10 for the Scientific Reports submission:

| Table | Content |
|-------|---------|
| S1 | Full parameter table |
| S2 | Operator verification inventory |
| S3 | Baseline calibration controls (E1b/E2b) |
| S4 | Component-wise ablation outputs (E9) |
| S5 | Sensitivity/factorial summaries (E4/E5) and longer-horizon/grid controls (E7/E8) |
| S6 | Robustness controls (E6, N=300) |
| S7 | EEG preprocessing audit |
| S8 | EEG EO vs EC statistics (100 subjects, Wilcoxon, FDR-adjusted q-values) |
| S9 | LANA S1 vs S2 statistics (50 seeds, Wilcoxon, FDR-adjusted q-values) |
| S10 | EEG–LANA concordance and label-permutation null benchmark |

---

## Key results

### Evidence chain (Table 1 in manuscript)

| Block | Purpose | Main conclusion |
|-------|---------|-----------------|
| E0 | Operator verification | All prespecified pass criteria satisfied |
| E1 | Full vs nominal baseline | Full model recruited; baseline silent |
| E1b/E2b | Calibrated baseline | Local activation did not produce distributed recruitment |
| R1/E9 | Component-wise ablation | Transport required for recruitment; feedback acts as suppressive gain control |
| E3 | S1 vs S2 regimes | S2 increased activity, accelerated recruitment |
| E4/E5/E6+ | Sensitivity/robustness | Effects structured, not hand-tuned |
| EEG | External benchmark | 2/6 concordance, P_perm = 0.95 → scope-defining, not validation |

### Component ablation summary (Table 2 in manuscript)

| Condition | Firing rate | Active fraction | Mean E | t50 | t90 |
|-----------|------------|-----------------|--------|-----|-----|
| Full model | 0.0271 | ~1.00 | 1.96 | 17 | 32 |
| No environmental feedback | 0.0880 | ~1.00 | 13.50 | 13 | 22 |
| No signal-to-neuron transport | 0.000 | 0.00 | 0.18 | NR | NR |
| Neuron-only baseline | 0.000 | 0.00 | 0.00 | NR | NR |

### EEG benchmark summary

- **Dataset:** PhysioNet EEGBCI, 100 subjects, Run 1 (EO) vs Run 2 (EC)
- **Feature extraction:** Per-channel then averaged (avoids average-reference cancellation)
- **Posterior alpha sanity check:** 0.126 (EO) → 0.409 (EC), 3.2× increase, p < 0.001, r = +0.999
- **EEG–LANA concordance:** 2/6 comparable feature families concordant
- **Label-permutation null:** P_perm = 0.95 for ≥2 matches → not enriched
- **Interpretation:** EEG constrains model scope; it is not waveform-level validation

---

## How to reproduce

### Requirements

- **NetLogo 7.0.2+** — [download](https://ccl.northwestern.edu/netlogo/)
- **Python 3.9+** with packages: `mne`, `numpy`, `pandas`, `scipy`, `matplotlib`

### Reproduce LANA simulations

Pre-computed outputs are included. To re-run:

1. Open the desired `.nlogox` file in NetLogo
2. Tools → BehaviorSpace → select experiment → Run
3. Experiments: E0a–E8 (principal model), E9a–E9d (ablation), EEG-S1/S2-tickbytick (EEG)

### Reproduce EEG–LANA comparison

```bash
pip install -r scripts/requirements.txt
python scripts/download_eeg_100.py        # ~130 MB from PhysioNet
python scripts/lana_eeg_pipeline_v5.py    # generates all CSV outputs
```

### Reproduce v3.1 figures and tables

```bash
python analysis_scripts/run_analysis.py data/ output/
```

---

## Operational regime definitions

| Parameter | S1 (resting) | S2 (hyperexcitable) | Justification |
|-----------|-------------|--------------------|----|
| θ (threshold) | 1.0 | **0.8** | GSA 65.1% FR effect |
| κ_E (env. coupling) | 0.6 | **0.2** | N2 regime shift |
| INHIB-FRAC | 0.2 | **0.1** | N1 monotonic suppression |
| ρ (env. decay) | 0.01 | **0.005** | GSA 88% synchrony effect |

**Bold** values differ from S1. All other parameters identical.

## Neuron-only baseline

The `BASELINE?` switch disables signal agents, environmental field and divisive normalization simultaneously. Synaptic transmission remains active. The calibrated baseline (E1b/E2b) shows that even with near-complete source activation (~98%), distributed recruitment remains ~3.2% vs ~95.5% in the full model.

---

## Run totals

| Release | Runs | Notes |
|---------|------|-------|
| Original V&V | ~2,000 | + 3,010 decay samples |
| Original baseline/regime/lesion | 390 | |
| v3.1 manuscript | ~1,780 | |
| R1 supplementary | ~540 | E7, E8, ablation |
| R2 EEG tick-by-tick | 100 | 50 S1 + 50 S2 |
| **Grand total** | **~4,810** | **+ 3,010 decay samples** |

## Hardware

Intel Core i7-10750H (2.60 GHz, 6 cores), 16 GB RAM, Windows 10 Pro, NetLogo 7.0.2, Python 3.12+

---

## License

MIT License. See `LICENSE`.

## Citation

If you use this model or data, please cite both the archived repository DOI and the associated manuscript. See `CITATION.cff` for a machine-readable citation.

**Repository:** Kapetanović S, Dželalija M, Bijedić N, Gašpar D, Tipurić-Spužević S. (2026). LANA agent-based model: code and data release v3.1-R2. Zenodo. [https://doi.org/10.5281/zenodo.19085845](https://doi.org/10.5281/zenodo.19085845)

## Ethics

No new human participant data were collected. The EEG component uses publicly available de-identified recordings from the PhysioNet EEGBCI dataset (Schalk et al. 2004; Goldberger et al. 2000).
