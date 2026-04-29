# LANA — Supplementary Material (Code, Data, and Reproducibility)

This repository contains the NetLogo LANA (Local Adaptive Neural Agents) model, the full verification & validation (V&V) test-suite outputs, and analysis scripts supporting the manuscript:

**A Rule-Based Agent-Based Neural Model with Explicit Signal Transport and Environment-Mediated Feedback: The LANA Model**

Archived release (Zenodo DOI): [[https://doi.org/10.5281/zenodo.19085845](https://doi.org/10.5281/zenodo.19085845)  ](https://doi.org/10.5281/zenodo.19878413)
Current release: **v3.1-R1** (April 2026)

---

## What is included

### 1) Model code

| File | Description |
|------|-------------|
| `code/LANA_VALIDATION.nlogox` | Original NetLogo model file (includes validation modes and BehaviorSpace experiment definitions). |
| `code/LANA_VALIDATION_FINAL.nlogox` | Extended model incorporating the neuron-only baseline configuration (`BASELINE?` switch), operational regime presets (`REGIME` chooser: S1/S2/S3), mid-simulation lesion protocol (`LESION-ONSET` slider), automated chain benchmark (`run-chain-once`), and expanded CSV logging with regime and lesion-zone columns. |
| `code/LANA_v3.1_COMPLETE.nlogo` | v3.1 release model with corrected t50/t90 percentile indexing, linear-regression wavefront speed, source-region reporters, and all 26 BehaviorSpace experiment definitions (E0a–E6b, E1b, E2b). See `CHANGELOG_v3.1.txt` for full details. |
| `code/LANA_v3_1_ablation.nlogox` | **[R1 NEW]** Ablation variant used for the supplementary component-wise ablation control (Table S9). Supports disabling environmental feedback and/or direct signal-to-neuron transport input independently. |

### 2) Raw simulation outputs (BehaviorSpace)

#### Original V&V suite

- `data/raw/*.csv` — raw BehaviorSpace exports (Spreadsheet version 2.0) for all original V&V experiments.
- `data/raw/baseline_S1.csv` — full model vs neuron-only baseline comparison (60 runs: 30 seeds × 2 conditions, 500 ticks).
- `data/raw/regimes_S1_S2_S3.csv` — three-regime comparison (90 runs: 30 seeds × 3 regimes, 500 ticks).
- `data/raw/chain_baseline.csv` — chain propagation benchmark under full and baseline conditions (120 runs: 20 seeds × 3 delays × 2 conditions, 500 ticks).
- `data/raw/lesion_S3.csv` — lesion dynamics with per-tick recording (30 runs: 30 seeds, 1000 ticks, tick-level reporters).
- `data/raw/robustness.csv` — local sensitivity for kappa_E (30 runs: 10 seeds × 3 levels).
- `data/raw/robustness_D.csv` — local sensitivity for D (30 runs: 10 seeds × 3 levels).
- `data/raw/robustness_ALPHA.csv` — local sensitivity for alpha (30 runs: 10 seeds × 3 levels).
- `data/tidy/*_tidy.csv` — tidy (long-format) exports parsed from the raw files (one row per run, plus time-series where applicable).

#### v3.1 manuscript experiments (~1,780 runs)

All CSV files use clean experiment-label names:

| File | Description | Runs |
|------|-------------|------|
| `data/E0a-chain-delay.csv` | Mini-V&V: delay propagation | 100 |
| `data/E0b-decay.csv` | Mini-V&V: E-field decay (per-tick) | 50 |
| `data/E0c-threshold.csv` | Mini-V&V: threshold activation | 140 |
| `data/E0d-refractory.csv` | Mini-V&V: refractory enforcement | 100 |
| `data/E0e-chain-control.csv` | Mini-V&V: chain baseline control | 80 |
| `data/E1-baseline.csv` | Full model vs neuron-only baseline (50 seeds × 2 conditions) | 100 |
| `data/E1b-calibration-sweep.csv` | Calibration sweep for localized stimulation (20 seeds × 6 STIM-AMP levels) | 120 |
| `data/E2-propagation.csv` | Propagation benchmark under localized stimulation (50 seeds × 2 conditions) | 100 |
| `data/E2b-calibrated-baseline.csv` | Calibrated baseline control (50 seeds × 2 conditions) | 100 |
| `data/E3-S1.csv` | Resting regime (50 runs) | 50 |
| `data/E3-S2.csv` | Hyperexcitable regime (50 runs) | 50 |
| `data/E4-nominal.csv` | OAT nominal reference | 20 |
| `data/E4-*.csv` | OAT parameter sweeps (ALPHA, BETA, D, GAMMA, KAPPA-E, POp, RHO, THRESHOLD) | 8 × 40 |
| `data/E5-factorial.csv` | 2⁴ factorial design (16 combinations × 20 seeds) | 320 |
| `data/E6a-baseline-N300.csv` | N=300 baseline robustness | 40 |
| `data/E6b-S1-N300.csv` | N=300 S1 robustness | 20 |
| `data/E6b-S2-N300.csv` | N=300 S2 robustness | 20 |

#### R1 revision — supplementary experiments

The following BehaviorSpace spreadsheet-format CSVs were added during the R1 manuscript revision to support supplementary tables (S1, S5, S6, S9) and the component-wise ablation control:

| File | Experiment label | Description | Runs |
|------|-----------------|-------------|------|
| `data/LANA_v3_1_E1-baseline-spreadsheet.csv` | E1-baseline | Full model vs neuron-only baseline (raw spreadsheet export) | 100 |
| `data/LANA_v3_1_E3-S1-spreadsheet.csv` | E3-S1 | Resting regime (raw spreadsheet export) | 50 |
| `data/LANA_v3_1_E3-S2-spreadsheet.csv` | E3-S2 | Hyperexcitable regime (raw spreadsheet export) | 50 |
| `data/LANA_v3_1_E6a-baseline-N300-spreadsheet.csv` | E6a-baseline-N300 | N=300 baseline robustness (Table S1) | 40 |
| `data/LANA_v3_1_E6b-S1-N300-spreadsheet.csv` | E6b-S1-N300 | N=300 S1 robustness (Table S1) | 20 |
| `data/LANA_v3_1_E6b-S2-N300-spreadsheet.csv` | E6b-S2-N300 | N=300 S2 robustness (Table S1) | 20 |
| `data/LANA_v3_1_E7-longer-horizon-full-baseline-spreadsheet.csv` | E7-longer-horizon-full-baseline | 3000-tick full vs baseline control (Table S5) | 40 |
| `data/LANA_v3_1_E7-longer-horizon-S1-spreadsheet.csv` | E7-longer-horizon-S1 | 3000-tick S1 longer-horizon control (Table S5) | 20 |
| `data/LANA_v3_1_E7-longer-horizon-S2-spreadsheet.csv` | E7-longer-horizon-S2 | 3000-tick S2 longer-horizon control (Table S5) | 20 |
| `data/LANA_v3_1_E8-theta-kappa-grid-spreadsheet.csv` | E8-theta-kappa-grid | Three-level θ × κ\_E grid (Table S6) | 180 |

**Total R1 supplementary runs: ~540 additional BehaviorSpace runs.**

### 3) Regime parameter files

- `data/params/nominal_S1.csv` — S1 (resting) nominal parameter vector.
- `data/params/nominal_S2.csv` — S2 (hyperexcitable) nominal parameter vector with V&V justification for each deviation from S1.
- `data/params/nominal_S3.csv` — S3 (lesion) nominal parameter vector.
- `data/params/seeds.csv` — list of 30 random seeds used in all paired-design experiments.

### 4) Processed summaries

- `data/processed/summary_all_tests.csv` — key pass/fail metrics and headline numbers used in the manuscript.
- `data/processed/LANA_VV_table_summaries.xlsx` — reviewer-friendly table summaries (means + uncertainty).

### 5) Figures

#### Original V&V figures

- `figures/Fig*.png` — main manuscript figures (raster, 300 dpi).
- `figures/Fig*.pdf` — PDF versions of the same figures (vector container).
- `figures/fig_baseline.(png|pdf)` — Full model vs neuron-only baseline: firing rate, synchrony index, and active neuron fraction (30 paired seeds).
- `figures/fig_regimes.(png|pdf)` — Three-regime comparison (S1/S2/S3): firing rate, synchrony index, and mean synaptic weight.
- `figures/fig_lesion.(png|pdf)` — Lesion dynamics (S3): population activity time course and inside vs outside lesion zone.
- `figures/fig_robustness.(png|pdf)` — Local sensitivity tornado plot: ±10% OAT perturbation of kappa_E, D, and alpha.
- `figures/FigS1_M1_cross_implementation.(png|pdf)` — supplementary cross-implementation check (single-neuron threshold).

#### v3.1 manuscript figures

| File | Description |
|------|-------------|
| `figures/Fig1_Architecture.png` | LANA model architecture diagram. |
| `figures/Fig2_MiniVV.png` | Compact internal verification (E0): chain speed, decay, threshold bifurcation, refractory. |
| `figures/Fig3_E1_Baseline.png` | Full model vs neuron-only baseline (E1). |
| `figures/Fig4_E2_FullVsBaseline.png` | Propagation benchmark: full vs baseline (E2). |
| `figures/Fig5_E2_Propagation.png` | Propagation metrics: t50, t90, wavefront speed (E2). |
| `figures/Fig6_E3_FR_Distribution.png` | Seed-matched firing-rate comparison S1 vs S2 (E3). |
| `figures/Fig7_E3_Regime.png` | Paired regime metrics: FR, Fano, CV, Mean E (E3). |
| `figures/Fig8_E4_Tornado.png` | OAT sensitivity tornado plot (E4). |
| `figures/Fig9_E5_Factorial.png` | Factorial main effects and θ × κ\_E interaction (E5). |

#### R1 revision — revised manuscript figures (600 dpi)

Revised versions of Figures 3–9 prepared during the R1 revision in response to reviewer feedback. Changes are limited to readability and formatting; no data, statistics, or scientific content was altered. See `figures_revised/REVISION_CHANGELOG.md` for a detailed description of each change.

| File | Description |
|------|-------------|
| `figures_revised/Figure_3.png` | Full model vs neuron-only baseline (E1) — titles removed, panel labels (a)–(c) added. |
| `figures_revised/Figure_4.png` | Propagation benchmark (E2) — titles removed, panel labels (a)–(b) added. |
| `figures_revised/Figure_5.png` | First-spike maps and wavefront speed (E2) — titles removed, panel labels (a)–(c) added. |
| `figures_revised/Figure_6.png` | S1 vs S2 firing-rate comparison (E3) — titles removed, panel labels (a)–(b) added. |
| `figures_revised/Figure_7.png` | Paired regime metrics (E3) — titles removed, panel labels (a)–(d) added. |
| `figures_revised/Figure_8.png` | OAT sensitivity tornado plot (E4) — internal title removed. |
| `figures_revised/Figure_9.png` | Focused 2⁴ factorial screening (E5) — titles removed, panel labels (a)–(b) added. |
| `figures_revised/REVISION_CHANGELOG.md` | Detailed log of all figure edits for the R1 revision. |

**Summary of R1 figure changes:**
- All internal graph titles removed from Figures 3–9 (descriptive content moved to figure captions in the manuscript).
- Panel labels (a), (b), (c), (d) added consistently across all multi-panel figures.
- Notation consistency verified: κ\_E, θ × κ\_E, OAT, r\_rb consistent across all figures and manuscript text.
- All figures exported at 600 dpi PNG with embedded fonts and no overlapping text.

### 6) Tables (v3.1)

| File | Description |
|------|-------------|
| `tables/Tab1_Parameters.txt` | Model parameters for S1 and S2 regimes. |
| `tables/Tab2_E0_MiniVV.txt` | Mini-V&V verification summary. |
| `tables/Tab3_E1_Baseline_CI.txt` | Full model vs baseline with paired statistics. |
| `tables/Tab4_E2_Propagation.txt` | Propagation metrics. |
| `tables/Tab5_E3_Regime_CI.txt` | S1 vs S2 regime comparison with paired statistics. |
| `tables/Tab6_E4_OAT.txt` | OAT sensitivity: percentage change from nominal. |
| `tables/Tab7_E5_Factorial.txt` | Factorial 2⁴ main effects on firing rate. |
| `tables/TabS1_E6_Robustness.txt` | N=300 robustness check (supplementary Table S1). |

### 7) Supplementary materials (v3.1)

- `supplement/Supplementary_Tables_S2_S3.docx` — Table S2 (baseline calibration sweep) and Table S3 (calibrated baseline vs full model comparison).
- `supplement/Extended_Output_Summaries.txt` — Aggregated summary statistics for all experimental blocks (E0–E6, E1b, E2b).
- `supplement/Implementation_Notes_Non_Central_Modes.txt` — Documentation for code modes not used in central analyses (chain verification, decay test, single-neuron test, lesion mode, etc.).
- `supplement/Archived_Parameter_and_Output_Files.txt` — Complete BehaviorSpace parameter configurations, seed lists, and output file manifest for the fixed experimental protocol.

### 8) Analysis scripts

#### Original V&V analysis

- `analysis/analyze_final.py` — complete analysis pipeline: reads all BehaviorSpace CSV exports, computes paired statistics (Wilcoxon signed-rank, Friedman, Cohen's d, rank-biserial r), generates publication-ready tables (Markdown) and figures (PDF/PNG), and writes a summary report.
- `analysis/` — additional Python scripts to parse BehaviorSpace exports and regenerate summary tables / selected figures from the original V&V suite.

#### v3.1 manuscript analysis

| Script | Description |
|--------|-------------|
| `analysis_scripts/run_analysis.py` | Entry point: accepts `<data_directory>` and optional `[output_directory]` as arguments. |
| `analysis_scripts/generate_all_analysis.py` | Generates Figures 2, 3, 7–9 and Tables 2, 3, S1 from v3.1 CSV files. |
| `analysis_scripts/generate_remaining_figs.py` | Generates Figures 4–6 and Tables 1, 4, 6, 7. |
| `analysis_scripts/parse_netlogo_spreadsheet.py` | Universal parser for NetLogo BehaviorSpace spreadsheet-format CSVs. |

### 9) Documentation

- `docs/S1_BehaviorSpace_configurations.md` — exact parameter sweeps and run counts for all original experiments.
- `docs/S2_figure_to_paper_mapping.md` — mapping between figure files and manuscript sections.
- `CHANGELOG_v3.1.txt` — code changes, metric updates, and reproducibility notes for v3.1.

---

## Software requirements

- **NetLogo 7.0.2+** (v3.1 model) or **NetLogo 7.0.3+** (original V&V model). Newer NetLogo 7.x should also work.
- **Python 3.10+** (optional, only for re-running the analysis pipelines).

Install Python dependencies:
```bash
pip install -r requirements.txt
```

---

## Experimental design overview

### Original V&V suite

| Phase | Test | Purpose | Ticks | Runs |
|-------|------|---------|-------|------|
| 1 | V1 | Chain delay operator verification | 200 | 50 |
| 1 | V2 | Environment decay operator verification | 300 | 10 (3,010 time-series samples) |
| 1 | V3 | Signal distance-attenuation verification | 500 | 480 |
| 1 | V4 | E-field diffusion operator verification | 500 | 70 |
| 2 | M1 | Single-neuron threshold bifurcation | 200 | 300 |
| 2 | M2 | Refractory enforcement | 500 | 50 |
| 3 | E1 | Weight gating vs propagation | 200 | 100 |
| 3 | E2 | Delay–speed (reuses V1) | — | — |
| 4 | N1 | EI balance sweep | 500 | 150 |
| 4 | N2 | Coupling-driven regime shift | 500 | 220 |
| 5 | GSA | Factorial sensitivity screening | 500 | 450 |
| R | RR1 | Network size robustness | 500 | 100 |
| R | RR2 | Plasticity convergence (long runs) | 2000 | 20 |

**Total (original suite): 2,000 BehaviorSpace runs + 3,010 decay time-series samples.**

### Original baseline, regime, and lesion experiments

| Experiment | Purpose | Design | Ticks | Runs |
|------------|---------|--------|-------|------|
| baseline_S1 | Neuron-only baseline vs full model | 30 seeds × 2 conditions, matched-seed | 500 | 60 |
| regimes_S1_S2_S3 | Three operational regimes | 30 seeds × 3 regimes, matched-seed | 500 | 90 |
| chain_baseline | Chain propagation control | 20 seeds × 3 delays × 2 conditions | 500 | 120 |
| lesion_S3 | Lesion dynamics (pre/post) | 30 seeds, per-tick recording | 1000 | 30 |
| robustness (κ\_E) | Local sensitivity ±10% κ\_E | 10 seeds × 3 levels, OAT | 500 | 30 |
| robustness (D) | Local sensitivity ±10% D | 10 seeds × 3 levels, OAT | 500 | 30 |
| robustness (α) | Local sensitivity ±10% α | 10 seeds × 3 levels, OAT | 500 | 30 |

**Total (revision additions): 390 BehaviorSpace runs.**

### v3.1 manuscript experiments

| Experiment | Description | Seeds | Ticks | Runs |
|------------|-------------|-------|-------|------|
| E0a–E0e | Mini-V&V compact verification | variable | variable | 520 |
| E1 | Full model vs neuron-only baseline | 50 × 2 | 1000 | 100 |
| E1b | Calibration sweep (localized stim) | 20 × 6 | 1000 | 120 |
| E2 | Propagation benchmark | 50 × 2 | 1000 | 100 |
| E2b | Calibrated baseline control | 50 × 2 | 1000 | 100 |
| E3 | S1 vs S2 regime comparison | 50 × 2 | 1000 | 100 |
| E4 | OAT sensitivity (8 parameters) | 20 × 17 | 1000 | 340 |
| E5 | 2⁴ factorial design | 20 × 16 | 1000 | 320 |
| E6 | N=300 robustness | 20 × 4 | 1000 | 80 |

**Total (v3.1): ~1,780 BehaviorSpace runs.**

### R1 revision — supplementary experiments

| Experiment | Description | Seeds | Ticks | Runs | Supports |
|------------|-------------|-------|-------|------|----------|
| E6a-baseline-N300 | N=300 baseline robustness | 20 × 2 | 1000 | 40 | Table S1 |
| E6b-S1-N300 | N=300 S1 robustness | 20 | 1000 | 20 | Table S1 |
| E6b-S2-N300 | N=300 S2 robustness | 20 | 1000 | 20 | Table S1 |
| E7-longer-horizon-full-baseline | 3000-tick full vs baseline | 20 × 2 | 3000 | 40 | Table S5 |
| E7-longer-horizon-S1 | 3000-tick S1 control | 20 | 3000 | 20 | Table S5 |
| E7-longer-horizon-S2 | 3000-tick S2 control | 20 | 3000 | 20 | Table S5 |
| E8-theta-kappa-grid | Three-level θ × κ\_E grid | 20 × 9 | 1000 | 180 | Table S6 |
| Ablation control | Component-wise ablation | — | 1000 | ~200 | Table S9 |

**Total (R1 supplementary): ~540 additional BehaviorSpace runs.**

### Grand total across all releases: ~4,710 runs + 3,010 decay samples.

---

## Operational regime definitions

Three operational regimes are defined as fixed parameter vectors applied at model initialization. All comparisons use a matched-seed paired design (same seeds, identical network topology and stimulus protocol).

| Parameter | S1 (resting) | S2 (hyperexcitable) | S3 (lesion) | V&V justification |
|-----------|-------------|--------------------|-----------|--------------------|
| κ\_E | 0.6 | **0.2** | 0.6 | N2 regime shift (Table 6) |
| θ | 1.0 | **0.8** | 1.0 | GSA 65.1% FR effect (Table 7) |
| INHIB-FRAC | 0.2 | **0.1** | 0.2 | N1 monotonic suppression (Table 5) |
| ρ | 0.01 | **0.005** | 0.01 | GSA 88% synchrony effect (Table 7) |
| LESION-RADIUS | 0 | 0 | 5 | — |
| LESION-DROP | — | — | 0.3 | — |
| LESION-ONSET | — | — | 250 | — |

**Bold** values differ from S1. All other parameters identical to Table A1 defaults. Complete parameter vectors are provided in `data/params/`.

---

## Neuron-only baseline configuration

The `BASELINE?` switch disables three components simultaneously while preserving all other model mechanics:

- **Signal agents** — creation, propagation, and decay of mobile signal agents are bypassed.
- **Environmental field** — diffusion, decay, and deposition are skipped (E = 0 throughout).
- **Divisive normalization** — neuronal efficacy is not modulated by the local field (N\_i^eff = N\_i).

Synaptic transmission via the eligibility-countdown delay mechanism remains fully active. External stimulus is delivered as direct membrane-potential injection preserving the spatial profile. The chain benchmark confirms identical propagation speed (v = 1/delay) and zero mean absolute error under both conditions across all tested delays.

The v3.1 calibrated baseline control (E1b, E2b) further demonstrates that even when the baseline stimulus amplitude is increased to produce near-complete source-region activation (~98%), distributed network recruitment remains minimal (~3.2%) compared to the full model (~95.5%). See `supplement/Supplementary_Tables_S2_S3.docx`.

---

## How to reproduce the results

### A) Re-run simulations (NetLogo)

**v3.1 experiments (manuscript):**

1. Open `code/LANA_v3.1_COMPLETE.nlogo` in NetLogo 7.0.2+.
2. Go to Tools → BehaviorSpace.
3. Select any experiment (E0a through E6b-S2-N300).
4. Run with default settings.

**Original V&V experiments:**

1. Open `code/LANA_VALIDATION_FINAL.nlogox` in NetLogo 7.0.3+.
2. Set `REGIME` to the desired regime (S1, S2, S3, or "none" for manual parameter control).
3. Set `BASELINE?` to ON (neuron-only) or OFF (full model).
4. Click setup → go (or step) to run interactively.
5. For batch experiments: open Tools → BehaviorSpace and configure as described in `docs/S1_BehaviorSpace_configurations.md`.

### B) Regenerate v3.1 figures and tables from raw CSV outputs

```bash
# Install dependencies
pip install -r requirements.txt

# Run the v3.1 analysis pipeline
python analysis_scripts/run_analysis.py data/ output/
```
Generated figures and tables will be written to `output/`.

### C) Run the original V&V analysis pipeline

```bash
# Run complete original analysis (reads CSVs from data/raw/, outputs tables + figures)
python analysis/analyze_final.py
```

The script produces:
- `tables/table_baseline.md` — full vs baseline paired comparison.
- `tables/table_regimes.md` — three-regime Friedman + post hoc.
- `tables/table_lesion.md` — lesion pre/post dynamics.
- `figures/fig_baseline.pdf`, `fig_regimes.pdf`, `fig_lesion.pdf`, `fig_robustness.pdf` — publication figures.
- `report.txt` — all statistical results in plain text.

### D) Rebuild original V&V tables and figures

```bash
python -m analysis.make_tables  --input data/raw --output data/processed
python -m analysis.make_figures --input data/raw --output figures --format png
```

---

## v3.1 model version notes

Changes from v3.0 are documented in `CHANGELOG_v3.1.txt`. Key updates:

- **t50/t90 percentile indexing:** corrected from floor to ceiling-1 for proper percentile computation.
- **Wavefront speed:** changed from naive mean-d/mean-t to linear regression (time ~ distance, speed = 1/slope).
- **Removed ad hoc E-source term:** the Low-NFun E deposition block was removed for model clarity.
- **Source-region reporters:** added `report-source-active-fraction` and `report-source-FR` for calibrated baseline analysis.
- **finalize-run-logs:** added for BehaviorSpace final-command CSV export.

All metric changes are small (< 3%) and do not affect any qualitative conclusions. See `CHANGELOG_v3.1.txt` for the full list of updated values.

---

## R1 revision notes (April 2026)

The R1 revision addresses reviewer feedback on figure formatting, supplementary robustness controls, and the component-wise ablation analysis. The following items were added to the repository:

**New data files (10 CSV files):**
- E1, E3, E6 spreadsheet-format raw exports for independent verification.
- E7 longer-horizon controls (3000 ticks) for full-vs-baseline and S1-vs-S2 comparisons (Table S5).
- E8 three-level θ × κ\_E grid supporting the supplementary response-surface analysis (Table S6).

**New model code (1 file):**
- `LANA_v3_1_ablation.nlogox` — ablation variant for the component-wise ablation control (Table S9).

**Revised figures (7 PNG files, 600 dpi):**
- Figures 3–9 revised per reviewer requirements: all internal graph titles removed, panel labels (a)/(b)/(c)/(d) added, notation consistency (κ\_E, θ × κ\_E, OAT) verified, exported at 600 dpi. No data, statistics, or scientific content was changed. Full details in `figures_revised/REVISION_CHANGELOG.md`.

---

## Note on experiment naming

In the NetLogo BehaviorSpace configuration, the manuscript tests V3 and V4 correspond to BehaviorSpace experiment names `Vx_signal_attenuation` and `Vx_diffusion_operator`, respectively. This naming reflects the internal verification suite label used in the model file.

v3.1 experiments use the naming convention E0a through E6b-S2-N300, matching both the manuscript and the CSV file names in `data/`.

R1 supplementary experiments use E7 (longer-horizon) and E8 (theta-kappa grid) labels.

---

## License

MIT License. See `LICENSE`.

## Citation

If you use this model or data, please cite both the archived repository DOI and the associated manuscript. See `CITATION.cff` for a machine-readable citation.

**Repository:** Kapetanović S, Dželalija M, Bijedić N, Gašpar D, Tipurić-Spužević S. (2026). Zenodo. [https://doi.org/10.5281/zenodo.19085845](https://doi.org/10.5281/zenodo.19085845)

**Associated manuscript:** Kapetanović S, Dželalija M, Bijedić N, Gašpar D, Tipurić-Spužević S. (2026). A Rule-Based Agent-Based Neural Model with Explicit Signal Transport and Environment-Mediated Feedback: The LANA Model.
