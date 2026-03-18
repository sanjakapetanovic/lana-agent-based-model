#!/usr/bin/env python3
"""Generate remaining figures: Fig 4, 5, 6 + Tab 4, 6, 7 + complete all.

Reads data from LANA_DATA_DIR and writes output to LANA_OUTPUT_DIR.
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from parse_netlogo_spreadsheet import parse_spreadsheet

DATA = os.environ.get('LANA_DATA_DIR', os.path.join(script_dir, '..', 'data'))
OUT = os.environ.get('LANA_OUTPUT_DIR', os.path.join(script_dir, '..', 'output'))
os.makedirs(OUT, exist_ok=True)

def find_csv(experiment_label):
    """Find CSV file matching an experiment label."""
    clean = os.path.join(DATA, f"{experiment_label}.csv")
    if os.path.exists(clean):
        return clean
    for f in os.listdir(DATA):
        if experiment_label in f and f.endswith('.csv'):
            return os.path.join(DATA, f)
    raise FileNotFoundError(f"No CSV found for experiment: {experiment_label}")

plt.rcParams.update({
    'figure.figsize': (10, 6), 'font.size': 11,
    'axes.titlesize': 13, 'axes.labelsize': 12,
    'figure.dpi': 150, 'savefig.bbox': 'tight'
})

def get_metric(runs, metric, default=0):
    return np.array([r.get(metric, default) for r in runs], dtype=float)

def paired_wilcoxon(x, y):
    try:
        stat, p = stats.wilcoxon(x, y)
    except:
        stat, p = 0, 1.0
    diffs = x - y
    ranks = stats.rankdata(np.abs(diffs))
    r_plus = np.sum(ranks[diffs > 0])
    r_minus = np.sum(ranks[diffs < 0])
    r_rb = (r_plus - r_minus) / (r_plus + r_minus) if (r_plus + r_minus) > 0 else 0
    d = np.mean(diffs) / np.std(diffs, ddof=1) if np.std(diffs, ddof=1) > 0 else 0
    walsh = []
    n = len(diffs)
    for i in range(n):
        for j in range(i, n):
            walsh.append((diffs[i] + diffs[j]) / 2)
    hl = np.median(walsh)
    return p, r_rb, d, hl

# Parse data
_, E2 = parse_spreadsheet(find_csv("E2-propagation"))
_, E3_S1 = parse_spreadsheet(find_csv("E3-S1"))
_, E3_S2 = parse_spreadsheet(find_csv("E3-S2"))
_, E4_nom = parse_spreadsheet(find_csv("E4-nominal"))
_, E5 = parse_spreadsheet(find_csv("E5-factorial"))

E4_data = {}
for param in ['KAPPA-E', 'THRESHOLD', 'POp', 'BETA', 'GAMMA', 'D', 'RHO', 'ALPHA']:
    _, runs = parse_spreadsheet(find_csv(f"E4-{param}"))
    E4_data[param] = runs

E2_full = [r for r in E2 if r.get('BASELINE?') == 'false']
E2_base = [r for r in E2 if r.get('BASELINE?') == 'true']

# ============================================================
# FIG 5: E2 Propagation — wavefront speed + t50/t90
# ============================================================
print("Generating Fig 5: E2 Propagation...")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

ax = axes[0]
t50_full = get_metric(E2_full, 'report-t50')
t50_full_valid = t50_full[t50_full >= 0]
bp = ax.boxplot([t50_full_valid], tick_labels=['Full'], patch_artist=True, widths=0.4)
bp['boxes'][0].set_facecolor('#FFCDD2')
ax.set_ylabel('t50 (ticks)')
ax.set_title('(a) t50: 50% activation')
ax.text(0.95, 0.95, f'median={np.median(t50_full_valid):.0f}\nIQR=[{np.percentile(t50_full_valid,25):.0f}, {np.percentile(t50_full_valid,75):.0f}]',
        transform=ax.transAxes, va='top', ha='right', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax = axes[1]
t90_full = get_metric(E2_full, 'report-t90')
t90_full_valid = t90_full[t90_full >= 0]
bp = ax.boxplot([t90_full_valid], tick_labels=['Full'], patch_artist=True, widths=0.4)
bp['boxes'][0].set_facecolor('#FFCDD2')
ax.set_ylabel('t90 (ticks)')
ax.set_title('(b) t90: 90% activation')
ax.text(0.95, 0.95, f'median={np.median(t90_full_valid):.0f}\nIQR=[{np.percentile(t90_full_valid,25):.0f}, {np.percentile(t90_full_valid,75):.0f}]',
        transform=ax.transAxes, va='top', ha='right', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax = axes[2]
ws_full = get_metric(E2_full, 'report-wavefront-speed')
ws_full_valid = ws_full[ws_full > 0]
bp = ax.boxplot([ws_full_valid], tick_labels=['Full'], patch_artist=True, widths=0.4)
bp['boxes'][0].set_facecolor('#FFCDD2')
ax.set_ylabel('Wavefront speed (patches/tick)')
ax.set_title('(c) Wavefront Speed')
ax.text(0.95, 0.95, f'median={np.median(ws_full_valid):.3f}\nIQR=[{np.percentile(ws_full_valid,25):.3f}, {np.percentile(ws_full_valid,75):.3f}]',
        transform=ax.transAxes, va='top', ha='right', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('E2: Propagation Benchmark (N=150, localized stimulus, 50 seeds)', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig5_E2_Propagation.png'))
plt.close()
print("  Fig 5 saved.")

# ============================================================
# FIG 4: E2 Full vs Baseline
# ============================================================
print("Generating Fig 4: E2 Full vs Baseline comparison...")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (metric, label) in enumerate([
    ('report-t50', 't50 (ticks)'),
    ('report-t90', 't90 (ticks)'),
    ('report-wavefront-speed', 'Wavefront Speed')
]):
    ax = axes[idx]
    full_vals = get_metric(E2_full, metric)
    base_vals = get_metric(E2_base, metric)
    bp = ax.boxplot([base_vals, full_vals], tick_labels=['Baseline', 'Full'],
                    patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('#BBDEFB')
    bp['boxes'][1].set_facecolor('#FFCDD2')
    ax.set_ylabel(label)
    ax.set_title(label)

plt.suptitle('E2: Propagation — Full vs Baseline', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig4_E2_FullVsBaseline.png'))
plt.close()
print("  Fig 4 saved.")

# ============================================================
# FIG 6: E3 FR distribution
# ============================================================
print("Generating Fig 6: E3 FR distribution...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax = axes[0]
fr_s1 = get_metric(E3_S1, 'report-FR')
fr_s2 = get_metric(E3_S2, 'report-FR')

ax.hist(fr_s1, bins=15, alpha=0.6, color='#2196F3', label=f'S1 (μ={np.mean(fr_s1):.4f})', density=True)
ax.hist(fr_s2, bins=15, alpha=0.6, color='#F44336', label=f'S2 (μ={np.mean(fr_s2):.4f})', density=True)
ax.set_xlabel('Firing Rate')
ax.set_ylabel('Density')
ax.set_title('(a) FR Distribution: S1 vs S2')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1]
seeds_s1 = get_metric(E3_S1, 'SEED')
matched_s1 = []
matched_s2 = []
for seed in sorted(set(seeds_s1)):
    s1_runs = [r for r in E3_S1 if r.get('SEED') == seed]
    s2_runs = [r for r in E3_S2 if r.get('SEED') == seed]
    if s1_runs and s2_runs:
        matched_s1.append(s1_runs[0].get('report-FR', 0))
        matched_s2.append(s2_runs[0].get('report-FR', 0))

ax.scatter(matched_s1, matched_s2, alpha=0.6, c='purple', edgecolors='black', linewidth=0.5)
ax.plot([0, max(matched_s2)*1.1], [0, max(matched_s2)*1.1], 'k--', alpha=0.3, label='y=x')
ax.set_xlabel('S1 FR')
ax.set_ylabel('S2 FR')
ax.set_title('(b) Paired FR: S1 vs S2 (seed-matched)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.suptitle('E3: S1 vs S2 Regime Comparison — Firing Rate', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig6_E3_FR_Distribution.png'))
plt.close()
print("  Fig 6 saved.")

# ============================================================
# REMAINING TABLES (Tab 1, 4, 6, 7)
# ============================================================
print("\nGenerating remaining tables...")

with open(os.path.join(OUT, 'Tab1_Parameters.txt'), 'w') as f:
    f.write("Table 1: Nominal Parameters (S1) and S2 Changes\n")
    f.write("=" * 75 + "\n")
    f.write(f"{'Parameter':<20} {'Symbol':<8} {'S1 Value':<12} {'S2 Value':<12} {'NetLogo':<15}\n")
    f.write("-" * 75 + "\n")
    params = [
        ("N", "N", "150", "150", "N-NODES"),
        ("Leak", "α", "0.2", "0.2", "ALPHA"),
        ("Threshold", "θ", "1.0", "0.8", "THRESHOLD"),
        ("Reset", "V_reset", "0", "0", "V-RESET"),
        ("Refractory", "POp", "10", "10", "POp"),
        ("Inhib frac", "—", "0.2", "0.1", "INHIB-FRAC"),
        ("NFun mean", "—", "0.9", "0.9", "INIT-NFUN-MEAN"),
        ("NFun SD", "—", "0.08", "0.08", "INIT-NFUN-SD"),
        ("Out-degree mean", "—", "3", "3", "INIT-DEG-MEAN"),
        ("Out-degree SD", "—", "1", "1", "INIT-DEG-SD"),
        ("Signal speed", "—", "4", "4", "OUT-RANGE"),
        ("Signal radius", "—", "5", "5", "RADIUS-SIGNAL"),
        ("Signal decay", "β", "0.95", "0.95", "BETA"),
        ("Spatial atten.", "γ", "0.05", "0.05", "GAMMA"),
        ("E diffusion", "D", "0.15", "0.15", "D"),
        ("E decay", "ρ", "0.01", "0.005", "RHO"),
        ("E coupling", "κ_E", "0.6", "0.2", "KAPPA-E"),
        ("Stim period", "—", "10", "10", "REPEAT-K"),
        ("Plasticity μ,λ", "—", "0.01, 0.05", "—", "(hardcoded)"),
    ]
    for p in params:
        s2_mark = " ◄" if p[2] != p[3] and p[3] != "—" else ""
        f.write(f"{p[0]:<20} {p[1]:<8} {p[2]:<12} {p[3]:<12}{s2_mark} {p[4]:<15}\n")

print("  Tab 1 saved.")

with open(os.path.join(OUT, 'Tab4_E2_Propagation.txt'), 'w') as f:
    f.write("Table 4: Propagation Metrics (E2)\n")
    f.write("=" * 90 + "\n")
    f.write(f"{'Metric':<25} {'Full median [IQR]':<30} {'Baseline median [IQR]':<30}\n")
    f.write("-" * 90 + "\n")
    for metric, label in [('report-t50', 't50'), ('report-t90', 't90'),
                          ('report-wavefront-speed', 'Wavefront speed'),
                          ('report-active-fraction', 'Active fraction')]:
        full = get_metric(E2_full, metric)
        base = get_metric(E2_base, metric)
        f_med = np.median(full)
        f_iqr = f"[{np.percentile(full, 25):.3f}, {np.percentile(full, 75):.3f}]"
        b_med = np.median(base)
        b_iqr = f"[{np.percentile(base, 25):.3f}, {np.percentile(base, 75):.3f}]"
        f.write(f"{label:<25} {f_med:.3f} {f_iqr:<25} {b_med:.3f} {b_iqr:<25}\n")

print("  Tab 4 saved.")

nom_metrics = {}
for metric in ['report-FR', 'report-fano']:
    nom_metrics[metric] = np.mean(get_metric(E4_nom, metric))

param_map = {
    'KAPPA-E': ('κ_E', 'KAPPA-E'), 'THRESHOLD': ('θ', 'THRESHOLD'),
    'POp': ('POp', 'POp'), 'BETA': ('β', 'BETA'),
    'GAMMA': ('γ', 'GAMMA'), 'D': ('D', 'D'),
    'RHO': ('ρ', 'RHO'), 'ALPHA': ('α', 'ALPHA'),
}

with open(os.path.join(OUT, 'Tab6_E4_OAT.txt'), 'w') as f:
    f.write("Table 6: OAT Sensitivity — % Change from Nominal\n")
    f.write("=" * 100 + "\n")
    f.write(f"{'Parameter':<12} {'Low':<8} {'High':<8} {'%ΔFR Low':>10} {'%ΔFR High':>10} {'%ΔFano Low':>12} {'%ΔFano High':>12}\n")
    f.write("-" * 100 + "\n")
    for param, (greek, varname) in param_map.items():
        runs = E4_data[param]
        vals = sorted(set(r.get(varname, 0) for r in runs))
        if len(vals) >= 2:
            low_runs = [r for r in runs if r.get(varname) == vals[0]]
            high_runs = [r for r in runs if r.get(varname) == vals[-1]]
            low_fr = np.mean(get_metric(low_runs, 'report-FR'))
            high_fr = np.mean(get_metric(high_runs, 'report-FR'))
            low_fano = np.mean(get_metric(low_runs, 'report-fano'))
            high_fano = np.mean(get_metric(high_runs, 'report-fano'))
            pct_fr_low = ((low_fr - nom_metrics['report-FR']) / nom_metrics['report-FR'] * 100) if nom_metrics['report-FR'] > 0 else 0
            pct_fr_high = ((high_fr - nom_metrics['report-FR']) / nom_metrics['report-FR'] * 100) if nom_metrics['report-FR'] > 0 else 0
            pct_fano_low = ((low_fano - nom_metrics['report-fano']) / nom_metrics['report-fano'] * 100) if nom_metrics['report-fano'] > 0 else 0
            pct_fano_high = ((high_fano - nom_metrics['report-fano']) / nom_metrics['report-fano'] * 100) if nom_metrics['report-fano'] > 0 else 0
            f.write(f"{greek:<12} {vals[0]:<8} {vals[-1]:<8} {pct_fr_low:>+10.1f}% {pct_fr_high:>+10.1f}% {pct_fano_low:>+12.1f}% {pct_fano_high:>+12.1f}%\n")

print("  Tab 6 saved.")

with open(os.path.join(OUT, 'Tab7_E5_Factorial.txt'), 'w') as f:
    f.write("Table 7: Factorial 2⁴ Main Effects on FR\n")
    f.write("=" * 70 + "\n")
    f.write(f"{'Factor':<15} {'Low':<8} {'High':<8} {'FR_low':<12} {'FR_high':<12} {'ΔFR':<10} {'% total'}\n")
    f.write("-" * 70 + "\n")
    factors = [('THRESHOLD', 'θ'), ('KAPPA-E', 'κ_E'), ('INHIB-FRAC', 'INHIB'), ('RHO', 'ρ')]
    effects = []
    for varname, greek in factors:
        vals = sorted(set(r.get(varname, 0) for r in E5))
        low_runs = [r for r in E5 if r.get(varname) == vals[0]]
        high_runs = [r for r in E5 if r.get(varname) == vals[-1]]
        fr_low = np.mean(get_metric(low_runs, 'report-FR'))
        fr_high = np.mean(get_metric(high_runs, 'report-FR'))
        effect = fr_high - fr_low
        effects.append((greek, vals[0], vals[-1], fr_low, fr_high, effect))
    total_abs = sum(abs(e[5]) for e in effects)
    for greek, low, high, fr_l, fr_h, eff in effects:
        pct = abs(eff) / total_abs * 100 if total_abs > 0 else 0
        f.write(f"{greek:<15} {low:<8} {high:<8} {fr_l:<12.6f} {fr_h:<12.6f} {eff:<+10.6f} {pct:.1f}%\n")

print("  Tab 7 saved.")
print("\nAll remaining figures and tables generated!")
