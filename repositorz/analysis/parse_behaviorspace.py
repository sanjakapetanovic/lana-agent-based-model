"""
Utilities for parsing NetLogo BehaviorSpace exports (Spreadsheet version 2.0).

The raw CSV outputs produced by BehaviorSpace are "wide": each run is represented by a repeated block of columns.
This module converts them into tidy pandas DataFrames.

Supported patterns (as used in this project):
- "[reporter]" header row followed by a "[final]" row (typical for most experiments).
- "[final value]" header row followed by a values row whose first cell is empty (observed in some experiments).
- "[all run data]" time-series section (used by the energy-decay verification).

License: MIT
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class ParsedBehaviorSpace:
    """Container for parsed outputs."""
    final: pd.DataFrame
    all_run_data: Optional[pd.DataFrame] = None


def _read_rows(path: str | Path) -> List[List[str]]:
    rows: List[List[str]] = []
    with open(path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def _find_row_index(rows: List[List[str]], first_cell: str) -> Optional[int]:
    for i, row in enumerate(rows):
        if row and row[0].strip() == first_cell:
            return i
    return None


def _to_scalar(x: str):
    x = x.strip()
    if x == "" or x.lower() in {"na", "nan"}:
        return None
    if x.lower() == "true":
        return True
    if x.lower() == "false":
        return False
    try:
        if "." in x or "e" in x.lower():
            return float(x)
        return int(x)
    except Exception:
        return x


def _parse_repeated_blocks(header: List[str], values: List[str]) -> pd.DataFrame:
    step_positions = [i for i, h in enumerate(header) if h.strip() == "[step]"]
    if not step_positions:
        raise ValueError("Could not find '[step]' in header row; unsupported layout.")

    # Infer block size
    if len(step_positions) >= 2:
        block_size = step_positions[1] - step_positions[0]
    else:
        block_size = len(header) - step_positions[0]

    records: List[Dict[str, object]] = []
    for start in step_positions:
        end = min(start + block_size, len(header))
        block_header = header[start:end]
        block_values = values[start:end]
        rec: Dict[str, object] = {}
        for k, v in zip(block_header, block_values):
            key = k.strip()
            if key == "":
                continue
            rec[key] = _to_scalar(v)
        records.append(rec)

    return pd.DataFrame.from_records(records)


def parse_final(path: str | Path) -> pd.DataFrame:
    """
    Parse per-run final values from a BehaviorSpace Spreadsheet 2.0 export.

    Returns
    -------
    pd.DataFrame
        One row per run configuration.
    """
    rows = _read_rows(path)

    i_rep = _find_row_index(rows, "[reporter]")
    if i_rep is not None:
        header = rows[i_rep][1:]
        i_final = _find_row_index(rows, "[final]")
        if i_final is None:
            raise ValueError("Found [reporter] but not [final].")
        values = rows[i_final][1:]
        return _parse_repeated_blocks(header, values)

    i_fv = _find_row_index(rows, "[final value]")
    if i_fv is not None:
        header = rows[i_fv][1:]
        if i_fv + 1 >= len(rows):
            raise ValueError("Found [final value] but missing values row.")
        values_row = rows[i_fv + 1]
        values = values_row[1:] if values_row and values_row[0].strip() == "" else values_row
        return _parse_repeated_blocks(header, values)

    raise ValueError("Unsupported BehaviorSpace layout: could not find [reporter] or [final value].")


def parse_all_run_data(path: str | Path) -> pd.DataFrame:
    """
    Parse the '[all run data]' time-series section (one row per tick per run).

    Returns
    -------
    pd.DataFrame
        One row per tick per run.
    """
    rows = _read_rows(path)
    i_all = _find_row_index(rows, "[all run data]")
    if i_all is None:
        raise ValueError("This file does not contain an [all run data] section.")

    header = rows[i_all][1:]
    step_positions = [i for i, h in enumerate(header) if h.strip() == "[step]"]
    if not step_positions:
        raise ValueError("Could not infer block layout in [all run data] section.")
    if len(step_positions) >= 2:
        block_size = step_positions[1] - step_positions[0]
    else:
        block_size = len(header) - step_positions[0]

    out_records: List[Dict[str, object]] = []
    for r in rows[i_all + 1 :]:
        if not r:
            continue
        # Stop if we hit a new labeled section
        if r[0].strip().startswith("[") and r[0].strip() != "":
            break
        values = r[1:] if r and r[0].strip() == "" else r
        for start in step_positions:
            end = min(start + block_size, len(header))
            rec: Dict[str, object] = {}
            for k, v in zip(header[start:end], values[start:end]):
                key = k.strip()
                if key == "":
                    continue
                rec[key] = _to_scalar(v)
            out_records.append(rec)

    return pd.DataFrame.from_records(out_records)
