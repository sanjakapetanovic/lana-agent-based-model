"""
Generate summary tables for the LANA V&V manuscript from raw BehaviorSpace CSV outputs.

Usage:
  python -m analysis.make_tables --input data/raw --output data/processed

Outputs:
  - table_summaries.xlsx (human-readable)
  - table_summaries.csv  (machine-readable, tidy)

License: MIT
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .parse_behaviorspace import parse_final


def mean_sd_ci(x: pd.Series) -> tuple[float, float, float]:
    x = pd.to_numeric(x, errors="coerce").dropna()
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    m = float(x.mean())
    sd = float(x.std(ddof=1)) if len(x) > 1 else 0.0
    ci = 1.96 * sd / np.sqrt(len(x)) if len(x) > 1 else 0.0
    return (m, sd, ci)


def summarize_by(df: pd.DataFrame, by: str, metrics: list[str]) -> pd.DataFrame:
    out_rows = []
    for level, g in df.groupby(by):
        row = {by: level, "n": len(g)}
        for m in metrics:
            mu, sd, ci = mean_sd_ci(g[m])
            row[f"{m}_mean"] = mu
            row[f"{m}_sd"] = sd
            row[f"{m}_ci95"] = ci
        out_rows.append(row)
    return pd.DataFrame(out_rows).sort_values(by).reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to data/raw folder")
    ap.add_argument("--output", required=True, help="Path to data/processed folder")
    args = ap.parse_args()

    in_dir = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # N1 EI balance
    n1 = parse_final(in_dir / "N1_ei_balance.csv")
    n1_sum = summarize_by(
        n1,
        by="INHIB-FRAC",
        metrics=["mean-firing-rate", "fano-factor", "synchrony-index"],
    )

    # N2 phase transition
    n2 = parse_final(in_dir / "N2_phase_transition.csv")
    if "is-oscillating?" in n2.columns:
        n2["oscillatory"] = n2["is-oscillating?"].astype(float)
    else:
        n2["oscillatory"] = np.nan
    n2_sum = summarize_by(
        n2,
        by="KAPPA-E",
        metrics=["mean-firing-rate", "spike-cv", "oscillatory"],
    )

    # R1 network size (optional)
    r1_path = in_dir / "R1_network_size.csv"
    r1_sum = pd.DataFrame()
    if r1_path.exists():
        r1 = parse_final(r1_path)
        # Some exports use 'N-NODES' as the varied parameter; adjust if needed.
        by_col = "N-NODES" if "N-NODES" in r1.columns else ("N-NODES?" if "N-NODES?" in r1.columns else None)
        if by_col is not None:
            r1_sum = summarize_by(r1, by=by_col, metrics=["mean-firing-rate", "synchrony-index", "fano-factor", "active-neuron-fraction"])
            # Add coefficient of variation for firing rate (SD/mean) to match Table 8 convention
            if "mean-firing-rate_mean" in r1_sum.columns and "mean-firing-rate_sd" in r1_sum.columns:
                r1_sum["mean-firing-rate_cv_pct"] = 100.0 * r1_sum["mean-firing-rate_sd"] / r1_sum["mean-firing-rate_mean"].replace(0, np.nan)

    # Excel workbook for quick review
    xlsx_path = out_dir / "table_summaries.xlsx"
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as xw:
        n1_sum.to_excel(xw, sheet_name="N1_EI_balance", index=False)
        n2_sum.to_excel(xw, sheet_name="N2_phase_transition", index=False)
        if not r1_sum.empty:
            r1_sum.to_excel(xw, sheet_name="R1_network_size", index=False)

    # Tidy CSV for scripts
    frames = []
    for name, df in [("N1", n1_sum), ("N2", n2_sum), ("R1", r1_sum)]:
        if df is None or df.empty:
            continue
        tmp = df.copy()
        tmp.insert(0, "table", name)
        frames.append(tmp)
    if frames:
        pd.concat(frames, ignore_index=True).to_csv(out_dir / "table_summaries.csv", index=False)

    print(f"Wrote: {xlsx_path}")


if __name__ == "__main__":
    main()