# LANA V&V  --  Supplementary Material (Code, Data, and Reproducibility)

This repository contains the NetLogo **LANA (Local Adaptive Neural Agents)** model, the full verification & validation (V&V) test-suite outputs, and analysis scripts supporting the manuscript:

> **Systematic Verification and Validation of the LANA Agent-Based Spiking Neural Network Model**

---

## What is included

### 1) Model code

* `code/LANA_VALIDATION.nlogox`  --  the original NetLogo model file (includes validation modes and BehaviorSpace experiment definitions).
* `code/LANA_VALIDATION_FINAL.nlogox`  --  the extended model incorporating the neuron-only baseline configuration (`BASELINE?` switch), operational regime presets (`REGIME` chooser: S1/S2/S3), mid-simulation lesion protocol (`LESION-ONSET` slider), automated chain benchmark (`run-chain-once`), and expanded CSV logging with regime and lesion-zone columns.

### 2) Raw simulation outputs (BehaviorSpace)

* `data/raw/*.csv`  --  raw BehaviorSpace exports (Spreadsheet version 2.0) for all original V&V experiments.
* `data/raw/baseline_S1.csv`  --  full model vs neuron-only baseline comparison (60 runs: 30 seeds x 2 conditions, 500 ticks).
* `data/raw/regimes_S1_S2_S3.csv`  --  three-regime comparison (90 runs: 30 seeds x 3 regimes, 500 ticks).
* `data/raw/chain_baseline.csv`  --  chain propagation benchmark under full and baseline conditions (120 runs: 20 seeds x 3 delays x 2 conditions, 500 ticks).
* `data/raw/lesion_S3.csv`  --  lesion dynamics with per-tick recording (30 runs: 30 seeds, 1000 ticks, tick-level reporters).
* `data/raw/robustness.csv`  --  local sensitivity for kappa_E (30 runs: 10 seeds x 3 levels).
* `data/raw/robustness_D.csv`  --  local sensitivity for D (30 runs: 10 seeds x 3 levels).
* `data/raw/robustness_ALPHA.csv`  --  local sensitivity for alpha (30 runs: 10 seeds x 3 levels).
* `data/tidy/*_tidy.csv`  --  tidy (long-format) exports parsed from the raw files (one row per run, plus time-series where applicable).

### 3) Regime parameter files

* `data/params/nominal_S1.csv`  --  S1 (resting) nominal parameter vector.
* `data/params/nominal_S2.csv`  --  S2 (hyperexcitable) nominal parameter vector with V&V justification for each deviation from S1.
* `data/params/nominal_S3.csv`  --  S3 (lesion) nominal parameter vector.
* `data/params/seeds.csv`  --  list of 30 random seeds used in all paired-design experiments.

### 4) Processed summaries

* `data/processed/summary_all_tests.csv`  --  key pass/fail metrics and headline numbers used in the manuscript.
* `data/processed/LANA_VV_table_summaries.xlsx`  --  reviewer-friendly table summaries (means + uncertainty).

### 5) Figures

* `figures/Fig*.png`  --  main manuscript figures (raster, 300 dpi).
* `figures/Fig*.pdf`  --  PDF versions of the same figures (vector container).
* `figures/fig_baseline.(png|pdf)`  --  Full model vs neuron-only baseline: firing rate, synchrony index, and active neuron fraction (30 paired seeds).
* `figures/fig_regimes.(png|pdf)`  --  Three-regime comparison (S1/S2/S3): firing rate, synchrony index, and mean synaptic weight.
* `figures/fig_lesion.(png|pdf)`  --  Lesion dynamics (S3): population activity time course and inside vs outside lesion zone.
* `figures/fig_robustness.(png|pdf)`  --  Local sensitivity tornado plot: +/-10% OAT perturbation of kappa_E, D, and alpha.
* `figures/FigS1_M1_cross_implementation.(png|pdf)`  --  supplementary cross-implementation check (single-neuron threshold).

### 6) Analysis scripts

* `analysis/analyze_final.py`  --  complete analysis pipeline: reads all BehaviorSpace CSV exports, computes paired statistics (Wilcoxon signed-rank, Friedman, Cohen's d, rank-biserial r), generates publication-ready tables (Markdown) and figures (PDF/PNG), and writes a summary report.
* `analysis/`  --  additional Python scripts to parse BehaviorSpace exports and regenerate summary tables / selected figures from the original V&V suite.

### 7) Documentation

* `docs/S1_BehaviorSpace_configurations.md`  --  exact parameter sweeps and run counts for all original experiments.
* `docs/S2_figure_to_paper_mapping.md`  --  mapping between figure files and manuscript sections.

---

## Software requirements

* **NetLogo 7.0.3+** (version used for the reported runs; newer NetLogo 7.x should also work).
* **Python 3.10+** (optional, only for re-running the analysis pipeline).

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
| 3 | E2 | Delay–speed (reuses V1) |  --  |  --  |
| 4 | N1 | EI balance sweep | 500 | 150 |
| 4 | N2 | Coupling-driven regime shift | 500 | 220 |
| 5 | GSA | Factorial sensitivity screening | 500 | 450 |
| R | RR1 | Network size robustness | 500 | 100 |
| R | RR2 | Plasticity convergence (long runs) | 2000 | 20 |

**Total (original suite):** 2,000 BehaviorSpace runs + 3,010 decay time-series samples.

### Baseline, regime, and lesion experiments (revision additions)

| Experiment | Purpose | Design | Ticks | Runs |
|------------|---------|--------|------:|-----:|
| baseline_S1 | Neuron-only baseline vs full model | 30 seeds x 2 conditions (BASELINE? true/false), matched-seed paired | 500 | 60 |
| regimes_S1_S2_S3 | Three operational regimes | 30 seeds x 3 regimes (S1/S2/S3), matched-seed paired | 500 | 90 |
| chain_baseline | Chain propagation control | 20 seeds x 3 delays x 2 conditions, matched-seed paired | 500 | 120 |
| lesion_S3 | Lesion dynamics (pre/post) | 30 seeds, per-tick recording, LESION-ONSET = 250 | 1000 | 30 |
| robustness (kappa_E) | Local sensitivity +/-10% kappa_E | 10 seeds x 3 levels (0.54, 0.60, 0.66), OAT | 500 | 30 |
| robustness (D) | Local sensitivity +/-10% D | 10 seeds x 3 levels (0.135, 0.15, 0.165), OAT | 500 | 30 |
| robustness (alpha) | Local sensitivity +/-10% alpha | 10 seeds x 3 levels (0.18, 0.20, 0.22), OAT | 500 | 30 |

**Total (revision additions):** 390 BehaviorSpace runs.

**Grand total:** 2,390 runs + 3,010 decay samples.

---

## Operational regime definitions

Three operational regimes are defined as fixed parameter vectors applied at model initialization. All comparisons use a matched-seed paired design (same 30 seeds, identical network topology and stimulus protocol).

| Parameter | S1 (resting) | S2 (hyperexcitable) | S3 (lesion) | V&V justification |
|-----------|:---:|:---:|:---:|---|
| kappa_E | 0.6 | **0.2** | 0.6 | N2 regime shift (Table 6) |
| theta | 1.0 | **0.8** | 1.0 | GSA 65.1% FR effect (Table 7) |
| INHIB-FRAC | 0.2 | **0.1** | 0.2 | N1 monotonic suppression (Table 5) |
| rho | 0.01 | **0.005** | 0.01 | GSA 88% synchrony effect (Table 7) |
| LESION-RADIUS | 0 | 0 | **5** |  --  |
| LESION-DROP |  --  |  --  | **0.3** |  --  |
| LESION-ONSET |  --  |  --  | **250** |  --  |

Bold values differ from S1. All other parameters identical to Table A1 defaults. Complete parameter vectors are provided in `data/params/`.

---

## Neuron-only baseline configuration

The `BASELINE?` switch disables three components simultaneously while preserving all other model mechanics:

1. **Signal agents**  --  creation, propagation, and decay of mobile signal agents are bypassed.
2. **Environmental field**  --  diffusion, decay, and deposition are skipped (E = 0 throughout).
3. **Divisive normalization**  --  neuronal efficacy is not modulated by the local field (N_i^eff = N_i).

Synaptic transmission via the eligibility-countdown delay mechanism remains fully active. External stimulus is delivered as direct membrane-potential injection preserving the spatial profile. The chain benchmark confirms identical propagation speed (v = 1/delay) and zero mean absolute error under both conditions across all tested delays.

---

## How to reproduce the results

### A) Re-run simulations (NetLogo)

1. Open `code/LANA_VALIDATION_FINAL.nlogox` in NetLogo 7.0.3+.
2. Set **REGIME** to the desired regime (S1, S2, S3, or "none" for manual parameter control).
3. Set **BASELINE?** to ON (neuron-only) or OFF (full model).
4. Click **setup** → **go** (or **step**) to run interactively.
5. For batch experiments: open Tools → BehaviorSpace and configure as described in `docs/S1_BehaviorSpace_configurations.md`.

### B) Run the analysis pipeline (Python)

```bash
# Install dependencies
pip install -r requirements.txt

# Run complete analysis (reads CSVs from data/raw/, outputs tables + figures)
python analysis/analyze_final.py
```

The script produces:
- `tables/table_baseline.md`  --  full vs baseline paired comparison.
- `tables/table_regimes.md`  --  three-regime Friedman + post hoc.
- `tables/table_lesion.md`  --  lesion pre/post dynamics.
- `figures/fig_baseline.pdf`, `fig_regimes.pdf`, `fig_lesion.pdf`, `fig_robustness.pdf`  --  publication figures.
- `report.txt`  --  all statistical results in plain text.

### C) Rebuild original V&V tables and figures

```bash
python -m analysis.make_tables  --input data/raw --output data/processed
python -m analysis.make_figures --input data/raw --output figures --format png
```

---

## Key results summary

| Comparison | Key finding | Statistical test | Effect size |
|------------|------------|-----------------|-------------|
| Full vs baseline (firing rate) | 11x higher in full model | Wilcoxon p = 1.86 x 10-9 | d = 5.25, r = 1.00 |
| Full vs baseline (active fraction) | 100% vs 6.7% | Wilcoxon p = 1.69 x 10-6 | d = 4.89, r = 1.00 |
| Chain: full = baseline | Speed = 1/delay, MAE = 0 | Identical in 120/120 runs |  --  |
| S1 vs S2 (firing rate) | S2 2.15x higher | Friedman p < 10-13, Bonf. p < 0.0001 | d = 5.56 |
| Lesion drop (S3) | 22.5% reduction | Wilcoxon p = 1.73 x 10-6 | d = 1.54 |
| Robustness (+/-10% kappa_E) | +/-9.8% firing rate change | Monotonic, proportionate |  --  |

---

## Note on experiment naming

In the NetLogo BehaviorSpace configuration, the manuscript tests V3 and V4 correspond to BehaviorSpace experiment names `Vx_signal_attenuation` and `Vx_diffusion_operator`, respectively. This naming reflects the internal verification suite label used in the model file.

---

## License

MIT License. See `LICENSE`.

## Citation

If you use this model or data, please cite the manuscript and this repository. See `CITATION.cff` for a machine-readable citation.
