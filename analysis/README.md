# Analysis scripts (reproducibility)

This folder contains lightweight Python scripts used to:
1) parse NetLogo BehaviorSpace outputs exported in **Spreadsheet version 2.0** format,
2) regenerate the **summary tables** reported in the manuscript, and
3) regenerate selected **figures** from the raw CSV outputs.

## Requirements
Install dependencies from the repository root:

```bash
pip install -r requirements.txt
```

## Quick start
From the repository root:

```bash
python -m analysis.make_tables --input data/raw --output data/processed
python -m analysis.make_figures --input data/raw --output figures --format png
```

## Notes
- The parser targets the BehaviorSpace layouts used in this project (final-value blocks, and the `all run data`
  section used by the energy-decay verification).
- If you export BehaviorSpace outputs in a different format, update `parse_behaviorspace.py`.
