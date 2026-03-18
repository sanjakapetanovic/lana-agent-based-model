# LANA — Supplementary Material (Code, Data, and Reproducibility)

This repository contains the NetLogo **LANA (Local Adaptive Neural Agents)** model, the full verification & validation (V&V) test-suite outputs, and analysis scripts supporting the manuscript:

> **A Rule-Based Agent-Based Neural Model with Explicit Signal Transport and Environment-Mediated Feedback: The LANA Model**

Archived release (Zenodo DOI):(https://doi.org/10.5281/zenodo.19085845)
Current release: **v3.1** (March 2026)

---

## What is included

### 1) Model code

* `code/LANA_VALIDATION.nlogox` — the original NetLogo model file (includes validation modes and BehaviorSpace experiment definitions).
* `code/LANA_VALIDATION_FINAL.nlogox` — the extended model incorporating the neuron-only baseline configuration (`BASELINE?` switch), operational regime presets (`REGIME` chooser: S1/S2/S3), mid-simulation lesion protocol (`LESION-ONSET` slider), automated chain benchmark (`run-chain-once`), and expanded CSV logging with regime and lesion-zone columns.
* `code/LANA_v3.1_COMPLETE.nlogo` — **v3.1 release model** with corrected t50/t90 percentile indexing, linear-regression wavefront speed, source-region reporters, and all 26 BehaviorSpace experiment definitions (E0a–E6b, E1b, E2b). See `CHANGELOG_v3.1.txt` for full details.

### 2) Raw simulation outputs (BehaviorSpace)

#### Original V&V suite

* `data/raw/*.csv` — raw BehaviorSpace exports (Spreadsheet version 2.0) for all original V&V experiments.
* `data/raw/baseline_S1.csv` — full model vs neuron-only baseline comparison (60 runs: 30 seeds × 2 conditions, 500 ticks).
* `data/raw/regimes_S1_S2_S3.csv` — three-regime comparison (90 runs: 30 seeds × 3 regimes, 500 ticks).
* `data/raw/chain_baseline.csv` — chain propagation benchmark under full and baseline conditions (120 runs: 20 seeds × 3 delays × 2 conditions, 500 ticks).
* `data/raw/lesion_S3.csv` — lesion dynamics with per-tick recording (30 runs: 30 seeds, 1000 ticks, tick-level reporters).
* `data/raw/robustness.csv` — local sensitivity for kappa_E (30 runs: 10 seeds × 3 levels).
* `data/raw/robustness_D.csv` — local sensitivity for D (30 runs: 10 seeds × 3 levels).
* `data/raw/robustness_ALPHA.csv` — local sensitivity for alpha (30 runs: 10 seeds × 3 levels).
* `data/tidy/*_tidy.csv` — tidy (long-format) exports parsed from the raw files (one row per run, plus time-series where applicable).

#### v3.1 manuscript experiments (~1,780 runs)

All CSV files use clean experiment-label names:

* `data/E0a-chain-delay.csv` — Mini-V&V: delay propagation (100 runs)
* `data/E0b-decay.csv` — Mini-V&V: E-field decay (50 runs, per-tick)
* `data/E0c-threshold.csv` — Mini-V&V: threshold activation (140 runs)
* `data/E0d-refractory.csv` — Mini-V&V: refractory enforcement (100 runs)
* `data/E0e-chain-control.csv` — Mini-V&V: chain baseline control (80 runs)
* `data/E1-baseline.csv` — Full model vs neuron-only baseline (100 runs: 50 seeds × 2 conditions)
* `data/E1b-calibration-sweep.csv` — Calibration sweep for localized stimulation (120 runs: 20 seeds × 6 STIM-AMP levels)
* `data/E2-propagation.csv` — Propagation benchmark under localized stimulation (100 runs: 50 seeds × 2 conditions)
* `data/E2b-calibrated-baseline.csv` — Calibrated baseline control (100 runs: 50 seeds × 2 conditions)
* `data/E3-S1.csv` — Resting regime (50 runs)
* `data/E3-S2.csv` — Hyperexcitable regime (50 runs)
* `data/E4-nominal.csv` — OAT nominal reference (20 runs)
* `data/E4-ALPHA.csv`, `E4-BETA.csv`, `E4-D.csv`, `E4-GAMMA.csv`, `E4-KAPPA-E.csv`, `E4-POp.csv`, `E4-RHO.csv`, `E4-THRESHOLD.csv` — OAT parameter sweeps (8 × 40 runs)
* `data/E5-factorial.csv` — 2⁴ factorial design (320 runs: 16 combinations × 20 seeds)
* `data/E6a-baseline-N300.csv` — N=300 baseline robustness (40 runs)
* `data/E6b-S1-N300.csv` — N=300 S1 robustness (20 runs)
* `data/E6b-S2-N300.csv` — N=300 S2 robustness (20 runs)

### 3) Regime parameter files

* `data/params/nominal_S1.csv` — S1 (resting) nominal parameter vector.
* `data/params/nominal_S2.csv` — S2 (hyperexcitable) nominal parameter vector with V&V justification for each deviation from S1.
* `data/params/nominal_S3.csv` — S3 (lesion) nominal parameter vector.
* `data/params/seeds.csv` — list of 30 random seeds used in all paired-design experiments.

### 4) Processed summaries

* `data/processed/summary_all_tests.csv` — key pass/fail metrics and headline numbers used in the manuscript.
* `data/processed/LANA_VV_table_summaries.xlsx` — reviewer-friendly table summaries (means + uncertainty).

### 5) Figures

#### Original V&V figures

* `figures/Fig*.png` — main manuscript figures (raster, 300 dpi).
* `figures/Fig*.pdf` — PDF versions of the same figures (vector container).
* `figures/fig_baseline.(png|pdf)` — Full model vs neuron-only baseline: firing rate, synchrony index, and active neuron fraction (30 paired seeds).
* `figures/fig_regimes.(png|pdf)` — Three-regime comparison (S1/S2/S3): firing rate, synchrony index, and mean synaptic weight.
* `figures/fig_lesion.(png|pdf)` — Lesion dynamics (S3): population activity time course and inside vs outside lesion zone.
* `figures/fig_robustness.(png|pdf)` — Local sensitivity tornado plot: ±10% OAT perturbation of kappa_E, D, and alpha.
* `figures/FigS1_M1_cross_implementation.(png|pdf)` — supplementary cross-implementation check (single-neuron threshold).

#### v3.1 manuscript figures

* `figures/Fig1_Architecture.png` — LANA model architecture diagram.
* `figures/Fig2_MiniVV.png` — Compact internal verification (E0): chain speed, decay, threshold bifurcation, refractory.
* `figures/Fig3_E1_Baseline.png` — Full model vs neuron-only baseline (E1).
* `figures/Fig4_E2_FullVsBaseline.png` — Propagation benchmark: full vs baseline (E2).
* `figures/Fig5_E2_Propagation.png` — Propagation metrics: t50, t90, wavefront speed (E2).
* `figures/Fig6_E3_FR_Distribution.png` — Seed-matched firing-rate comparison S1 vs S2 (E3).
* `figures/Fig7_E3_Regime.png` — Paired regime metrics: FR, Fano, CV, Mean E (E3).
* `figures/Fig8_E4_Tornado.png` — OAT sensitivity tornado plot (E4).
* `figures/Fig9_E5_Factorial.png` — Factorial main effects and θ × κ_E interaction (E5).

### 6) Tables (v3.1)

* `tables/Tab1_Parameters.txt` — Model parameters for S1 and S2 regimes.
* `tables/Tab2_E0_MiniVV.txt` — Mini-V&V verification summary.
* `tables/Tab3_E1_Baseline_CI.txt` — Full model vs baseline with paired statistics.
* `tables/Tab4_E2_Propagation.txt` — Propagation metrics.
* `tables/Tab5_E3_Regime_CI.txt` — S1 vs S2 regime comparison with paired statistics.
* `tables/Tab6_E4_OAT.txt` — OAT sensitivity: percentage change from nominal.
* `tables/Tab7_E5_Factorial.txt` — Factorial 2⁴ main effects on firing rate.
* `tables/TabS1_E6_Robustness.txt` — N=300 robustness check (supplementary Table S1).

### 7) Supplementary materials (v3.1)

* `supplement/Supplementary_Tables_S2_S3.docx` — Table S2 (baseline calibration sweep) and Table S3 (calibrated baseline vs full model comparison).
* `supplement/Extended_Output_Summaries.txt` — Aggregated summary statistics for all experimental blocks (E0–E6, E1b, E2b).
* `supplement/Implementation_Notes_Non_Central_Modes.txt` — Documentation for code modes not used in central analyses (chain verification, decay test, single-neuron test, lesion mode, etc.).
* `supplement/Archived_Parameter_and_Output_Files.txt` — Complete BehaviorSpace parameter configurations, seed lists, and output file manifest for the fixed experimental protocol.

### 8) Analysis scripts

#### Original V&V analysis

* `analysis/analyze_final.py` — complete analysis pipeline: reads all BehaviorSpace CSV exports, computes paired statistics (Wilcoxon signed-rank, Friedman, Cohen's d, rank-biserial r), generates publication-ready tables (Markdown) and figures (PDF/PNG), and writes a summary report.
* `analysis/` — additional Python scripts to parse BehaviorSpace exports and regenerate summary tables / selected figures from the original V&V suite.

#### v3.1 manuscript analysis

* `analysis_scripts/run_analysis.py` — entry point: accepts `<data_directory>` and optional `[output_directory]` as arguments.
* `analysis_scripts/generate_all_analysis.py` — generates Figures 2, 3, 7–9 and Tables 2, 3, S1 from v3.1 CSV files.
* `analysis_scripts/generate_remaining_figs.py` — generates Figures 4–6 and Tables 1, 4, 6, 7.
* `analysis_scripts/parse_netlogo_spreadsheet.py` — universal parser for NetLogo BehaviorSpace spreadsheet-format CSVs.

### 9) Documentation

* `docs/S1_BehaviorSpace_configurations.md` — exact parameter sweeps and run counts for all original experiments.
* `docs/S2_figure_to_paper_mapping.md` — mapping between figure files and manuscript sections.
* `CHANGELOG_v3.1.txt` — code changes, metric updates, and reproducibility notes for v3.1.

---

## Software requirements

* **NetLogo 7.0.2+** (v3.1 model) or **NetLogo 7.0.3+** (original V&V model). Newer NetLogo 7.x should also work.
* **Python 3.10+** (optional, only for re-running the analysis pipelines).

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Experimental design overview

### Original V&V suite

| Phase | Test | Purpose | Ticks | BehaviorSpace runs |
|-------|------|---------|------:|-------------------:|
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

**Total (original suite):** 2,000 BehaviorSpace runs + 3,010 decay time-series samples.

### Original baseline, regime, and lesion experiments

| Experiment | Purpose | Design | Ticks | Runs |
|------------|---------|--------|------:|-----:|
| baseline_S1 | Neuron-only baseline vs full model | 30 seeds × 2 conditions (BASELINE? true/false), matched-seed paired | 500 | 60 |
| regimes_S1_S2_S3 | Three operational regimes | 30 seeds × 3 regimes (S1/S2/S3), matched-seed paired | 500 | 90 |
| chain_baseline | Chain propagation control | 20 seeds × 3 delays × 2 conditions, matched-seed paired | 500 | 120 |
| lesion_S3 | Lesion dynamics (pre/post) | 30 seeds, per-tick recording, LESION-ONSET = 250 | 1000 | 30 |
| robustness (kappa_E) | Local sensitivity ±10% kappa_E | 10 seeds × 3 levels (0.54, 0.60, 0.66), OAT | 500 | 30 |
| robustness (D) | Local sensitivity ±10% D | 10 seeds × 3 levels (0.135, 0.15, 0.165), OAT | 500 | 30 |
| robustness (alpha) | Local sensitivity ±10% alpha | 10 seeds × 3 levels (0.18, 0.20, 0.22), OAT | 500 | 30 |

**Total (revision additions):** 390 BehaviorSpace runs.

### v3.1 manuscript experiments

| Experiment | Description | Seeds | Ticks | Runs |
|------------|-------------|------:|------:|-----:|
| E0a–E0e | Mini-V&V compact verification | variable | variable | 520 |
| E1 | Full model vs neuron-only baseline | 50 × 2 | 1000 | 100 |
| E1b | Calibration sweep (localized stim) | 20 × 6 | 1000 | 120 |
| E2 | Propagation benchmark | 50 × 2 | 1000 | 100 |
| E2b | Calibrated baseline control | 50 × 2 | 1000 | 100 |
| E3 | S1 vs S2 regime comparison | 50 × 2 | 1000 | 100 |
| E4 | OAT sensitivity (8 parameters) | 20 × 17 | 1000 | 340 |
| E5 | 2⁴ factorial design | 20 × 16 | 1000 | 320 |
| E6 | N=300 robustness | 20 × 4 | 1000 | 80 |

**Total (v3.1):** ~1,780 BehaviorSpace runs.

**Grand total across all releases:** ~4,170 runs + 3,010 decay samples.

---

## Operational regime definitions

Three operational regimes are defined as fixed parameter vectors applied at model initialization. All comparisons use a matched-seed paired design (same seeds, identical network topology and stimulus protocol).

| Parameter | S1 (resting) | S2 (hyperexcitable) | S3 (lesion) | V&V justification |
|-----------|:---:|:---:|:---:|---|
| kappa_E | 0.6 | **0.2** | 0.6 | N2 regime shift (Table 6) |
| theta | 1.0 | **0.8** | 1.0 | GSA 65.1% FR effect (Table 7) |
| INHIB-FRAC | 0.2 | **0.1** | 0.2 | N1 monotonic suppression (Table 5) |
| rho | 0.01 | **0.005** | 0.01 | GSA 88% synchrony effect (Table 7) |
| LESION-RADIUS | 0 | 0 | **5** | — |
| LESION-DROP | — | — | **0.3** | — |
| LESION-ONSET | — | — | **250** | — |

Bold values differ from S1. All other parameters identical to Table A1 defaults. Complete parameter vectors are provided in `data/params/`.

---

## Neuron-only baseline configuration

The `BASELINE?` switch disables three components simultaneously while preserving all other model mechanics:

1. **Signal agents** — creation, propagation, and decay of mobile signal agents are bypassed.
2. **Environmental field** — diffusion, decay, and deposition are skipped (E = 0 throughout).
3. **Divisive normalization** — neuronal efficacy is not modulated by the local field (N_i^eff = N_i).

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
2. Set **REGIME** to the desired regime (S1, S2, S3, or "none" for manual parameter control).
3. Set **BASELINE?** to ON (neuron-only) or OFF (full model).
4. Click **setup** → **go** (or **step**) to run interactively.
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

* **t50/t90 percentile indexing:** corrected from `floor` to `ceiling-1` for proper percentile computation.
* **Wavefront speed:** changed from naive mean-d/mean-t to linear regression (time ~ distance, speed = 1/slope).
* **Removed ad hoc E-source term:** the Low-NFun E deposition block was removed for model clarity.
* **Source-region reporters:** added `report-source-active-fraction` and `report-source-FR` for calibrated baseline analysis.
* **finalize-run-logs:** added for BehaviorSpace final-command CSV export.

All metric changes are small (< 3%) and do not affect any qualitative conclusions. See `CHANGELOG_v3.1.txt` for the full list of updated values.

---

## Note on experiment naming

In the NetLogo BehaviorSpace configuration, the manuscript tests V3 and V4 correspond to BehaviorSpace experiment names `Vx_signal_attenuation` and `Vx_diffusion_operator`, respectively. This naming reflects the internal verification suite label used in the model file.

v3.1 experiments use the naming convention `E0a` through `E6b-S2-N300`, matching both the manuscript and the CSV file names in `data/`.

---

## License

MIT License. See `LICENSE`.

## Citation

If you use this model or data, please cite both the archived repository DOI and the associated manuscript. See `CITATION.cff` for a machine-readable citation.

Repository:
Kapetanović S, Dželalija M, Bijedić N, Gašpar D, Tipurić-Spužević S. (2025). Zenodo. (https://doi.org/10.5281/zenodo.19085845)

Associated manuscript:
Kapetanović S, Dželalija M, Bijedić N, Gašpar D, Tipurić-Spužević S. (2025). *A Rule-Based Agent-Based Neural Model with Explicit Signal Transport and Environment-Mediated Feedback: The LANA Model*.
