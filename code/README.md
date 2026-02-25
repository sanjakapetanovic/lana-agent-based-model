# LANA V&V — Supplementary Material (Code, Data, and Reproducibility)

This repository contains the **NetLogo LANA (Local Adaptive Neural Agents) Validation Edition v5** model,
the full **verification & validation (V&V) test-suite outputs**, and lightweight **analysis scripts**
supporting the manuscript:

> *“LANA (Local Adaptive Neural Agents): A Reproducible Verification and Validation Suite for a Spatial Agent‑Based Spiking Network Model”*

## What is included

### 1) Model code
- `code/LANA_VALIDATION.nlogox` — the NetLogo model file (includes validation modes and BehaviorSpace experiment definitions).

### 2) Raw simulation outputs (BehaviorSpace)
- `data/raw/*.csv` — raw BehaviorSpace exports (**Spreadsheet version 2.0**) for all experiments.
- `data/tidy/*_tidy.csv` — tidy (long-format) exports parsed from the raw files (one row per run, plus time‑series where applicable).

### 3) Processed summaries
- `data/processed/summary_all_tests.csv` — key pass/fail metrics and headline numbers used in the manuscript.
- `data/processed/LANA_VV_table_summaries.xlsx` — reviewer‑friendly table summaries (means + uncertainty).

### 4) Figures
- `figures/Fig*.png` — main manuscript figures (raster).
- `figures/Fig*.pdf` — PDF versions of the same figures (vector container, generated from PNG for convenience).
- `figures/FigS1_M1_cross_implementation.(png|pdf)` — supplementary cross‑implementation check (single‑neuron threshold).

### 5) Reproducibility scripts
- `analysis/` — Python scripts to parse BehaviorSpace exports and regenerate summary tables / selected figures.

---

## Software requirements
- **NetLogo 7.0.3** (version used for the reported runs; newer NetLogo 7.x should also work).
- Python 3.10+ (optional, only for re‑running table/figure aggregation).

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Experiments included (manuscript mapping)

| Phase | Test | Purpose (short) | Ticks | BehaviorSpace runs |
|------:|------|------------------|------:|-------------------:|
| 1 | V1 | Chain delay operator verification | 200 | 50 |
| 1 | V2 | Environment decay operator verification | 300 | 10 runs (**3,010 time‑series samples** for the fit) |
| 1 | V3 | Signal distance‑attenuation verification | 500 | 480 |
| 1 | V4 | E‑field diffusion operator verification | 500 | 70 |
| 2 | M1 | Single‑neuron threshold bifurcation | 200 | 300 |
| 2 | M2 | Refractory enforcement | 500 | 50 |
| 3 | E1 | Weight gating vs propagation | 200 | 100 |
| 3 | E2 | Delay–speed (reuses V1) | — | — |
| 4 | N1 | EI balance sweep | 500 | 150 |
| 4 | N2 | Coupling‑driven regime shift | 500 | 220 |
| 5 | GSA | Factorial sensitivity screening | 500 | 450 |
| R | R1 | Network size robustness | 500 | 100 |
| R | R2 | Plasticity convergence (long runs) | 2000 | 20 |

**Total:** 2,000 BehaviorSpace runs + 3,010 decay time‑series samples.

---

## How to reproduce the results

### A) Re-run simulations (NetLogo)
1. Open `code/LANA_VALIDATION.nlogox` in NetLogo.
2. Open **Tools → BehaviorSpace**.
3. Select the experiment matching the phase/test (see `docs/S1_BehaviorSpace_configurations.md`).
4. Export results as **Spreadsheet** (CSV).

### B) Rebuild tables and selected figures (Python)
From the repository root:

```bash
python -m analysis.make_tables  --input data/raw --output data/processed
python -m analysis.make_figures --input data/raw --output figures --format png
```

---

## Documentation
- `docs/S1_BehaviorSpace_configurations.md` — exact parameter sweeps and run counts.
- `docs/S2_figure_to_paper_mapping.md` — mapping between figure files and manuscript sections.

---

## License
MIT License. See `LICENSE`.


### Note on experiment naming

In the NetLogo BehaviorSpace configuration, the manuscript tests **V3** and **V4** correspond to BehaviorSpace experiment names `Vx_signal_attenuation` and `Vx_diffusion_operator`, respectively. This naming reflects the internal verification suite label used in the model file.
