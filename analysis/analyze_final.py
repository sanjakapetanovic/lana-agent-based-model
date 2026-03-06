#!/usr/bin/env python3
"""
LANA Complete Analysis Pipeline
================================
Reads BehaviorSpace CSV outputs → produces:
  1. Statistical tests (Wilcoxon, Friedman, effect sizes)
  2. Publication-ready tables (LaTeX + Markdown)
  3. Figures (matplotlib) saved as PDF/PNG
  4. Summary report (console + file)

USAGE:
  python analyze_final.py

FILES EXPECTED in same directory (or outputs/ subdirectory):
  - baseline_S1.csv      (BehaviorSpace table export)
  - regimes_S1_S2_S3.csv
  - chain_baseline.csv
  - lesion_S3.csv
  - robustness.csv        (optional)

BehaviorSpace exports: use "Table" output, semicolon or comma separated.
The script auto-detects separator and skips BehaviorSpace header rows.

OUTPUT:
  - figures/fig_baseline.pdf
  - figures/fig_regimes.pdf
  - figures/fig_lesion.pdf
  - figures/fig_chain.pdf
  - figures/fig_robustness.pdf
  - tables/table_baseline.md
  - tables/table_regimes.md
  - tables/table_lesion.md
  - report.txt
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
from pathlib import Path

warnings.filterwarnings('ignore')

# Try importing optional deps
try:
    from scipy import stats as sp_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("[WARN] scipy not found — statistical tests will be skipped")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("[WARN] matplotlib not found — figures will be skipped")

# ============================================================
# CONFIG
# ============================================================

SEEDS = list(range(1, 31))
REGIMES = ['S1', 'S2', 'S3']
METRICS_BASELINE = [
    'mean-firing-rate', 'final-total-spikes', 'synchrony-index',
    'fano-factor', 'spike-cv', 'active-neuron-fraction', 'mean-weight'
]
METRICS_REGIME = [
    'mean-firing-rate', 'synchrony-index', 'fano-factor',
    'spike-cv', 'active-neuron-fraction', 'mean-weight'
]

FIGDIR = Path('figures')
TABDIR = Path('tables')
REPORT_FILE = Path('report.txt')

report_lines = []

def log(msg):
    print(msg)
    report_lines.append(msg)

def save_report():
    with open(REPORT_FILE, 'w') as f:
        f.write('\n'.join(report_lines))
    log(f"\n[SAVED] Report → {REPORT_FILE}")

# ============================================================
# UTILITIES
# ============================================================

def smart_read(filepath):
    """Read BehaviorSpace CSV, auto-detecting format."""
    fp = Path(filepath)
    if not fp.exists():
        # Try in outputs/ subdir
        fp = Path('outputs') / fp.name
    if not fp.exists():
        return None

    # BehaviorSpace "Table" exports often have 6 header lines
    # Try reading with different skip rows
    for skiprows in [0, 6, 7, 1]:
        for sep in [',', ';', '\t']:
            try:
                df = pd.read_csv(fp, sep=sep, skiprows=skiprows)
                if len(df.columns) > 2 and len(df) > 0:
                    # Clean column names
                    df.columns = [c.strip().strip('"').strip("'").strip('[]') for c in df.columns]
                    return df
            except Exception:
                continue
    return None


def find_col(df, *patterns):
    """Find first column matching any pattern (case-insensitive)."""
    for p in patterns:
        for c in df.columns:
            if p.lower() in c.lower():
                return c
    return None


def cohen_d_paired(x, y):
    diff = np.array(x, dtype=float) - np.array(y, dtype=float)
    sd = np.std(diff, ddof=1)
    return np.mean(diff) / sd if sd > 0 else 0.0


def rank_biserial_r(W, n):
    denom = n * (n + 1) / 2
    return 1 - (2 * W) / denom if denom > 0 else 0.0


def fmt_med_iqr(vals):
    vals = np.array(vals, dtype=float)
    med = np.median(vals)
    q25, q75 = np.percentile(vals, [25, 75])
    return f"{med:.4f} [{q25:.4f}, {q75:.4f}]"


def wilcoxon_test(x, y):
    """Returns (statistic, p-value) or (nan, nan) if not possible."""
    if not HAS_SCIPY:
        return np.nan, np.nan
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    diff = x - y
    if np.all(diff == 0):
        return 0.0, 1.0
    try:
        stat, p = sp_stats.wilcoxon(x, y)
        return stat, p
    except Exception:
        return np.nan, np.nan


# ============================================================
# 1. BASELINE ANALYSIS
# ============================================================

def analyze_baseline():
    log("\n" + "=" * 70)
    log("  1. BASELINE ANALYSIS — Full LANA vs Neuron-only (paired seeds)")
    log("=" * 70)

    df = smart_read('baseline_S1.csv')
    if df is None:
        log("  [SKIP] baseline_S1.csv not found.")
        log("  → Run BehaviorSpace 'Baseline-S1' experiment first.")
        return

    bl_col = find_col(df, 'baseline')
    seed_col = find_col(df, 'seed')
    if not bl_col or not seed_col:
        log(f"  [ERROR] Columns: {list(df.columns)}")
        return

    full = df[df[bl_col].astype(str).str.lower().isin(['false', '0', 'off'])].sort_values(seed_col).reset_index(drop=True)
    base = df[df[bl_col].astype(str).str.lower().isin(['true', '1', 'on'])].sort_values(seed_col).reset_index(drop=True)
    log(f"  Full runs: {len(full)}, Baseline runs: {len(base)}")

    merged = full.merge(base, on=seed_col, suffixes=('_full', '_base'))
    n = len(merged)
    log(f"  Paired: {n} seeds\n")

    # Table
    rows = []
    header = f"  {'Metric':<22} {'Full (med [IQR])':<28} {'Baseline (med [IQR])':<28} {'p':>8} {'d':>7} {'r':>7}"
    log(header)
    log(f"  {'-'*100}")

    md_rows = ["| Metric | Full model (med [IQR]) | Baseline (med [IQR]) | Wilcoxon p | Cohen d | r_rb |",
               "|--------|----------------------|---------------------|-----------|---------|------|"]

    for m in METRICS_BASELINE:
        fc = find_col(merged, m + '_full') or find_col(merged, m)
        bc = find_col(merged, m + '_base')
        if not fc or not bc:
            continue
        fv = merged[fc].astype(float).values
        bv = merged[bc].astype(float).values

        W, p = wilcoxon_test(fv, bv)
        d = cohen_d_paired(fv, bv)
        r = rank_biserial_r(W, n) if not np.isnan(W) else np.nan

        f_str = fmt_med_iqr(fv)
        b_str = fmt_med_iqr(bv)
        log(f"  {m:<22} {f_str:<28} {b_str:<28} {p:>8.4f} {d:>7.2f} {r:>7.2f}")
        md_rows.append(f"| {m} | {f_str} | {b_str} | {p:.4f} | {d:.2f} | {r:.2f} |")
        rows.append({'metric': m, 'full': f_str, 'base': b_str, 'p': p, 'd': d, 'r': r})

    # Save table
    TABDIR.mkdir(exist_ok=True)
    with open(TABDIR / 'table_baseline.md', 'w') as f:
        f.write('\n'.join(md_rows))
    log(f"\n  [SAVED] → {TABDIR / 'table_baseline.md'}")

    # Figure
    if HAS_MPL and rows:
        fig, axes = plt.subplots(1, min(3, len(rows)), figsize=(4 * min(3, len(rows)), 4))
        if not hasattr(axes, '__iter__'):
            axes = [axes]
        plot_metrics = ['mean-firing-rate', 'synchrony-index', 'fano-factor']
        for i, m in enumerate(plot_metrics):
            if i >= len(axes):
                break
            fc = find_col(merged, m + '_full')
            bc = find_col(merged, m + '_base')
            if not fc or not bc:
                continue
            fv = merged[fc].astype(float).values
            bv = merged[bc].astype(float).values
            ax = axes[i]
            bp = ax.boxplot([fv, bv], labels=['Full', 'Baseline'], widths=0.5,
                           patch_artist=True, medianprops=dict(color='black', linewidth=2))
            bp['boxes'][0].set_facecolor('#4C72B0')
            bp['boxes'][1].set_facecolor('#DD8452')
            # Paired lines
            for j in range(len(fv)):
                ax.plot([1, 2], [fv[j], bv[j]], color='gray', alpha=0.3, linewidth=0.5)
            ax.set_title(m.replace('-', ' ').title(), fontsize=10)
            ax.set_ylabel(m)
        plt.tight_layout()
        FIGDIR.mkdir(exist_ok=True)
        fig.savefig(FIGDIR / 'fig_baseline.pdf', dpi=300, bbox_inches='tight')
        fig.savefig(FIGDIR / 'fig_baseline.png', dpi=150, bbox_inches='tight')
        plt.close()
        log(f"  [SAVED] → {FIGDIR / 'fig_baseline.pdf'}")


# ============================================================
# 2. REGIME COMPARISON
# ============================================================

def analyze_regimes():
    log("\n" + "=" * 70)
    log("  2. REGIME COMPARISON — S1 vs S2 vs S3 (Friedman + post hoc)")
    log("=" * 70)

    df = smart_read('regimes_S1_S2_S3.csv')
    if df is None:
        log("  [SKIP] regimes_S1_S2_S3.csv not found.")
        log("  → Run BehaviorSpace 'Regimes-S1-S2-S3' experiment first.")
        return

    reg_col = find_col(df, 'regime')
    seed_col = find_col(df, 'seed')
    if not reg_col or not seed_col:
        log(f"  [ERROR] Columns: {list(df.columns)}")
        return

    md_rows = ["| Metric | S1 (med [IQR]) | S2 (med [IQR]) | S3 (med [IQR]) | Friedman p | S1-S2 p (Bonf) | S1-S3 p (Bonf) | S2-S3 p (Bonf) |",
               "|--------|---|---|---|---|---|---|---|"]

    plot_data = {}
    for m in METRICS_REGIME:
        mcol = find_col(df, m)
        if not mcol:
            continue

        groups = {}
        for regime in REGIMES:
            sub = df[df[reg_col].astype(str).str.upper() == regime].sort_values(seed_col)
            if len(sub) > 0:
                groups[regime] = sub[mcol].astype(float).values

        if len(groups) < 2:
            continue

        log(f"\n  --- {m} ---")
        strs = {}
        for r in REGIMES:
            if r in groups:
                s = fmt_med_iqr(groups[r])
                strs[r] = s
                log(f"    {r}: {s}")

        # Friedman
        friedman_p = np.nan
        if HAS_SCIPY and len(groups) == 3:
            min_n = min(len(v) for v in groups.values())
            trimmed = {k: v[:min_n] for k, v in groups.items()}
            try:
                stat_f, friedman_p = sp_stats.friedmanchisquare(*trimmed.values())
                log(f"    Friedman χ²={stat_f:.3f}, p={friedman_p:.4f}")
            except Exception as e:
                log(f"    Friedman: error ({e})")

        # Post hoc pairwise Wilcoxon (Bonferroni × 3)
        pairs = [('S1', 'S2'), ('S1', 'S3'), ('S2', 'S3')]
        ph = {}
        for a, b in pairs:
            if a in groups and b in groups:
                min_n = min(len(groups[a]), len(groups[b]))
                W, p = wilcoxon_test(groups[a][:min_n], groups[b][:min_n])
                p_bonf = min(p * 3, 1.0) if not np.isnan(p) else np.nan
                d = cohen_d_paired(groups[a][:min_n], groups[b][:min_n])
                ph[f"{a}-{b}"] = p_bonf
                log(f"    {a} vs {b}: p={p:.4f} (Bonf={p_bonf:.4f}), d={d:.2f}")

        md_row = f"| {m} | {strs.get('S1','-')} | {strs.get('S2','-')} | {strs.get('S3','-')} | {friedman_p:.4f} | {ph.get('S1-S2',np.nan):.4f} | {ph.get('S1-S3',np.nan):.4f} | {ph.get('S2-S3',np.nan):.4f} |"
        md_rows.append(md_row)

        if m in ['mean-firing-rate', 'synchrony-index', 'spike-cv']:
            plot_data[m] = groups

    TABDIR.mkdir(exist_ok=True)
    with open(TABDIR / 'table_regimes.md', 'w') as f:
        f.write('\n'.join(md_rows))
    log(f"\n  [SAVED] → {TABDIR / 'table_regimes.md'}")

    # Figure
    if HAS_MPL and plot_data:
        n_plots = len(plot_data)
        fig, axes = plt.subplots(1, n_plots, figsize=(4 * n_plots, 4.5))
        if n_plots == 1:
            axes = [axes]
        colors = {'S1': '#4C72B0', 'S2': '#DD8452', 'S3': '#55A868'}

        for i, (m, groups) in enumerate(plot_data.items()):
            ax = axes[i]
            data = [groups.get(r, []) for r in REGIMES if r in groups]
            labels = [r for r in REGIMES if r in groups]
            bp = ax.boxplot(data, labels=labels, widths=0.5, patch_artist=True,
                           medianprops=dict(color='black', linewidth=2))
            for j, box in enumerate(bp['boxes']):
                box.set_facecolor(colors.get(labels[j], 'gray'))
            ax.set_title(m.replace('-', ' ').title(), fontsize=10)
            ax.set_ylabel(m)

        plt.tight_layout()
        FIGDIR.mkdir(exist_ok=True)
        fig.savefig(FIGDIR / 'fig_regimes.pdf', dpi=300, bbox_inches='tight')
        fig.savefig(FIGDIR / 'fig_regimes.png', dpi=150, bbox_inches='tight')
        plt.close()
        log(f"  [SAVED] → {FIGDIR / 'fig_regimes.pdf'}")


# ============================================================
# 3. CHAIN BENCHMARK
# ============================================================

def analyze_chain():
    log("\n" + "=" * 70)
    log("  3. CHAIN BENCHMARK — Full vs Baseline propagation")
    log("=" * 70)

    df = smart_read('chain_baseline.csv')
    if df is None:
        df = smart_read('chain-summary.csv')
    if df is None:
        log("  [SKIP] chain_baseline.csv / chain-summary.csv not found.")
        log("  → Run BehaviorSpace 'Chain-baseline' or run-chain-once.")
        return

    log(f"  Rows: {len(df)}, Columns: {list(df.columns)}")

    bl_col = find_col(df, 'baseline')
    delay_col = find_col(df, 'fixed-delay', 'delay')
    speed_col = find_col(df, 'speed')
    mae_col = find_col(df, 'mae')
    complete_col = find_col(df, 'complete')

    if not bl_col:
        log("  [WARN] No BASELINE column; showing overall stats")
        if speed_col:
            log(f"  Speed: mean={df[speed_col].astype(float).mean():.4f}")
        return

    for bl_val in ['false', 'true']:
        sub = df[df[bl_col].astype(str).str.lower() == bl_val]
        label = "Full" if bl_val == 'false' else "Baseline"
        log(f"\n  {label} ({len(sub)} runs):")
        if complete_col:
            n_complete = sub[complete_col].astype(str).str.lower().isin(['true', '1']).sum()
            log(f"    Completed chains: {n_complete}/{len(sub)}")
        if speed_col:
            speeds = sub[speed_col].astype(float)
            valid = speeds[speeds > 0]
            if len(valid) > 0:
                log(f"    Speed: mean={valid.mean():.4f}, sd={valid.std():.4f}")
        if mae_col:
            maes = sub[mae_col].astype(float)
            valid = maes[maes >= 0]
            if len(valid) > 0:
                log(f"    MAE: mean={valid.mean():.6f}")

    # Figure: speed vs delay for full and baseline
    if HAS_MPL and delay_col and speed_col:
        fig, ax = plt.subplots(figsize=(5, 4))
        for bl_val, color, label in [('false', '#4C72B0', 'Full'), ('true', '#DD8452', 'Baseline')]:
            sub = df[df[bl_col].astype(str).str.lower() == bl_val]
            if len(sub) == 0:
                continue
            delays = sub[delay_col].astype(float)
            speeds = sub[speed_col].astype(float)
            # Group by delay
            for d in sorted(delays.unique()):
                mask = delays == d
                s = speeds[mask]
                valid = s[s > 0]
                if len(valid) > 0:
                    ax.scatter([d] * len(valid), valid, color=color, alpha=0.4, s=20)
                    ax.plot(d, valid.mean(), 'o', color=color, markersize=8)

        # Theory line
        d_range = np.linspace(0.5, df[delay_col].astype(float).max() + 0.5, 100)
        ax.plot(d_range, 1.0 / d_range, 'k--', alpha=0.5, label='Theory (1/delay)')
        ax.set_xlabel('Synaptic delay (ticks)')
        ax.set_ylabel('Propagation speed (neurons/tick)')
        ax.set_title('Chain benchmark: Full vs Baseline')
        ax.legend(['Theory', 'Full', 'Baseline'])
        plt.tight_layout()
        FIGDIR.mkdir(exist_ok=True)
        fig.savefig(FIGDIR / 'fig_chain.pdf', dpi=300, bbox_inches='tight')
        fig.savefig(FIGDIR / 'fig_chain.png', dpi=150, bbox_inches='tight')
        plt.close()
        log(f"  [SAVED] → {FIGDIR / 'fig_chain.pdf'}")


# ============================================================
# 4. LESION ANALYSIS
# ============================================================

def analyze_lesion():
    log("\n" + "=" * 70)
    log("  4. LESION ANALYSIS — S3 pre/post dynamics")
    log("=" * 70)

    df = smart_read('lesion_S3.csv')
    if df is None:
        log("  [SKIP] lesion_S3.csv not found.")
        log("  → Run BehaviorSpace 'Lesion-S3' experiment (per-tick reporters).")
        return

    log(f"  Rows: {len(df)}, Columns: {list(df.columns)}")

    seed_col = find_col(df, 'seed')
    tick_col = find_col(df, 'tick', 'step')
    spike_col = find_col(df, 'totalspike', 'last-spike', 'neurons with')
    lin_col = find_col(df, 'lesionin', 'inside')
    lout_col = find_col(df, 'lesionout', 'outside')

    if not seed_col or not tick_col or not spike_col:
        log("  [ERROR] Cannot find required columns (seed, tick, spikes)")
        log(f"  Available: {list(df.columns)}")
        return

    LESION_ONSET = 250  # Must match model setting

    seeds = sorted(df[seed_col].unique())
    log(f"  Seeds: {len(seeds)}")

    summaries = []
    for seed in seeds:
        sdf = df[df[seed_col] == seed].sort_values(tick_col)
        ticks = sdf[tick_col].astype(float).values
        spikes = sdf[spike_col].astype(float).values

        # Pre-lesion plateau (tick 50 to onset-50)
        pre_mask = (ticks >= 50) & (ticks < LESION_ONSET - 50)
        pre_vals = spikes[pre_mask]
        pre_mean = np.mean(pre_vals) if len(pre_vals) > 0 else np.nan

        # Post-lesion immediate (onset to onset+50)
        post_mask = (ticks >= LESION_ONSET) & (ticks < LESION_ONSET + 50)
        post_vals = spikes[post_mask]
        post_min = np.min(post_vals) if len(post_vals) > 0 else np.nan
        post_mean = np.mean(post_vals) if len(post_vals) > 0 else np.nan

        # Recovery (onset+50 to onset+250)
        rec_mask = (ticks >= LESION_ONSET + 50) & (ticks < LESION_ONSET + 250)
        rec_vals = spikes[rec_mask]
        rec_mean = np.mean(rec_vals) if len(rec_vals) > 0 else np.nan

        # Final plateau (last 200 ticks)
        if len(ticks) > 200:
            final_vals = spikes[-200:]
            final_mean = np.mean(final_vals)
        else:
            final_mean = np.nan

        drop_ratio = post_mean / pre_mean if pre_mean > 0 else np.nan
        rec_ratio = rec_mean / pre_mean if pre_mean > 0 else np.nan

        summaries.append({
            'seed': seed, 'pre_plateau': pre_mean, 'post_min': post_min,
            'post_mean': post_mean, 'recovery_mean': rec_mean,
            'final_plateau': final_mean, 'drop_ratio': drop_ratio,
            'recovery_ratio': rec_ratio
        })

    sdf = pd.DataFrame(summaries)
    log(f"\n  Pre-lesion plateau:  {fmt_med_iqr(sdf['pre_plateau'].dropna())}")
    log(f"  Post-lesion min:     {fmt_med_iqr(sdf['post_min'].dropna())}")
    log(f"  Post-lesion mean:    {fmt_med_iqr(sdf['post_mean'].dropna())}")
    log(f"  Recovery mean:       {fmt_med_iqr(sdf['recovery_mean'].dropna())}")
    log(f"  Final plateau:       {fmt_med_iqr(sdf['final_plateau'].dropna())}")
    log(f"  Drop ratio:          {fmt_med_iqr(sdf['drop_ratio'].dropna())}")
    log(f"  Recovery ratio:      {fmt_med_iqr(sdf['recovery_ratio'].dropna())}")

    # Pre vs post Wilcoxon
    if HAS_SCIPY:
        valid = sdf.dropna(subset=['pre_plateau', 'post_mean'])
        if len(valid) > 5:
            W, p = wilcoxon_test(valid['pre_plateau'], valid['post_mean'])
            d = cohen_d_paired(valid['pre_plateau'], valid['post_mean'])
            log(f"\n  Pre vs Post: Wilcoxon p={p:.4f}, d={d:.2f}")

    # Save table
    TABDIR.mkdir(exist_ok=True)
    md = ["| Phase | Median [IQR] |",
          "|-------|-------------|"]
    for phase, col in [('Pre-lesion plateau', 'pre_plateau'), ('Post-lesion (acute)', 'post_mean'),
                       ('Recovery', 'recovery_mean'), ('Final plateau', 'final_plateau'),
                       ('Drop ratio', 'drop_ratio'), ('Recovery ratio', 'recovery_ratio')]:
        vals = sdf[col].dropna()
        md.append(f"| {phase} | {fmt_med_iqr(vals)} |")
    with open(TABDIR / 'table_lesion.md', 'w') as f:
        f.write('\n'.join(md))
    log(f"  [SAVED] → {TABDIR / 'table_lesion.md'}")

    # Figure: time course
    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 4))

        # Aggregate across seeds: median ± IQR per tick
        all_ticks = sorted(df[tick_col].astype(float).unique())
        medians, q25s, q75s = [], [], []
        for t in all_ticks:
            vals = df[df[tick_col].astype(float) == t][spike_col].astype(float)
            medians.append(np.median(vals))
            q25s.append(np.percentile(vals, 25))
            q75s.append(np.percentile(vals, 75))

        ax.plot(all_ticks, medians, color='#4C72B0', linewidth=1.5, label='Median spikes')
        ax.fill_between(all_ticks, q25s, q75s, color='#4C72B0', alpha=0.2, label='IQR')
        ax.axvline(x=LESION_ONSET, color='red', linestyle='--', linewidth=1.5, label=f'Lesion onset (t={LESION_ONSET})')
        ax.set_xlabel('Tick')
        ax.set_ylabel('Population spike count')
        ax.set_title('S3 Lesion dynamics: pre/post time course')
        ax.legend(fontsize=8)
        plt.tight_layout()
        FIGDIR.mkdir(exist_ok=True)
        fig.savefig(FIGDIR / 'fig_lesion.pdf', dpi=300, bbox_inches='tight')
        fig.savefig(FIGDIR / 'fig_lesion.png', dpi=150, bbox_inches='tight')
        plt.close()
        log(f"  [SAVED] → {FIGDIR / 'fig_lesion.pdf'}")


# ============================================================
# 5. ROBUSTNESS
# ============================================================

def analyze_robustness():
    log("\n" + "=" * 70)
    log("  5. ROBUSTNESS — ±10% OAT perturbation")
    log("=" * 70)

    df = smart_read('robustness.csv')
    if df is None:
        log("  [SKIP] robustness.csv not found.")
        log("  → Run BehaviorSpace 'Robustness' experiments (OAT design).")
        return

    log(f"  Rows: {len(df)}, Columns: {list(df.columns)}")

    # Detect which parameters were varied
    fr_col = find_col(df, 'mean-firing-rate', 'firing')
    if not fr_col:
        log("  [ERROR] No firing rate column found")
        return

    params_to_check = ['KAPPA-E', 'D', 'ALPHA']
    plot_data = {}

    for param in params_to_check:
        pcol = find_col(df, param.lower())
        if not pcol:
            continue
        unique_vals = sorted(df[pcol].astype(float).unique())
        if len(unique_vals) < 2:
            continue

        log(f"\n  Parameter: {param} (levels: {unique_vals})")
        group_data = {}
        for val in unique_vals:
            sub = df[df[pcol].astype(float) == val]
            fr = sub[fr_col].astype(float)
            group_data[val] = fr.values
            log(f"    {param}={val}: FR mean={fr.mean():.4f}, sd={fr.std():.4f}")

        plot_data[param] = (unique_vals, group_data)

    # Tornado-style figure
    if HAS_MPL and plot_data:
        fig, ax = plt.subplots(figsize=(6, 3 + len(plot_data)))
        y_pos = 0
        yticks, ylabels = [], []

        for param, (levels, groups) in plot_data.items():
            nominal = levels[len(levels) // 2]  # Middle value = nominal
            nom_mean = np.mean(groups[nominal])

            for val in levels:
                if val == nominal:
                    continue
                diff = np.mean(groups[val]) - nom_mean
                pct = (diff / nom_mean * 100) if nom_mean != 0 else 0
                color = '#DD8452' if pct > 0 else '#4C72B0'
                ax.barh(y_pos, pct, color=color, height=0.6, alpha=0.8)
                ax.text(pct + (1 if pct >= 0 else -1), y_pos,
                       f'{pct:+.1f}%', va='center', fontsize=8)
                yticks.append(y_pos)
                pct_change = ((val - nominal) / nominal * 100)
                ylabels.append(f'{param} ({pct_change:+.0f}%)')
                y_pos += 1

        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels, fontsize=9)
        ax.set_xlabel('Change in firing rate (%)')
        ax.set_title('Robustness: ±10% parameter perturbation')
        ax.axvline(x=0, color='black', linewidth=0.5)
        plt.tight_layout()
        FIGDIR.mkdir(exist_ok=True)
        fig.savefig(FIGDIR / 'fig_robustness.pdf', dpi=300, bbox_inches='tight')
        fig.savefig(FIGDIR / 'fig_robustness.png', dpi=150, bbox_inches='tight')
        plt.close()
        log(f"  [SAVED] → {FIGDIR / 'fig_robustness.pdf'}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    log("=" * 70)
    log("  LANA COMPLETE ANALYSIS PIPELINE")
    log("  Place BehaviorSpace CSV exports in this directory or outputs/")
    log("=" * 70)

    analyze_baseline()
    analyze_regimes()
    analyze_chain()
    analyze_lesion()
    analyze_robustness()

    log("\n" + "=" * 70)
    log("  PIPELINE COMPLETE")
    log("=" * 70)
    log(f"\n  Outputs:")
    log(f"    Tables:  {TABDIR}/")
    log(f"    Figures: {FIGDIR}/")
    log(f"    Report:  {REPORT_FILE}")
    log(f"\n  Copy figures + tables into manuscript.")
    log(f"  Fill in placeholder values in MANUSCRIPT_ADDITIONS.md")

    save_report()
