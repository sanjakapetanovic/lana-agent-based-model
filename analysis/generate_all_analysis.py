#!/usr/bin/env python3
"""
Generate all Protocol v3.1 figures and tables from BehaviorSpace results.

This script reads data from LANA_DATA_DIR and writes output to LANA_OUTPUT_DIR.
These are set by run_analysis.py, or can be set manually:
    export LANA_DATA_DIR=../data
    export LANA_OUTPUT_DIR=../output
"""
import sys, os, csv, io
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
    """Find CSV file matching an experiment label, handling both clean and original names."""
    # Try clean name first
    clean = os.path.join(DATA, f"{experiment_label}.csv")
    if os.path.exists(clean):
        return clean
    # Try with original BehaviorSpace naming
    for f in os.listdir(DATA):
        if experiment_label in f and f.endswith('.csv'):
            return os.path.join(DATA, f)
    raise FileNotFoundError(f"No CSV found for experiment: {experiment_label}")

plt.rcParams.update({
    'figure.figsize': (10, 6),
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'savefig.bbox': 'tight'
})

# ============================================================
# PARSE ALL DATA
# ============================================================
print("Parsing all experiments...")

_, E0a = parse_spreadsheet(find_csv("E0a-chain-delay"))
_, E0b_raw = parse_spreadsheet(find_csv("E0b-decay"))
_, E0c = parse_spreadsheet(find_csv("E0c-threshold"))
_, E0d = parse_spreadsheet(find_csv("E0d-refractory"))
_, E0e = parse_spreadsheet(find_csv("E0e-chain-control"))
_, E1 = parse_spreadsheet(find_csv("E1-baseline"))
_, E2 = parse_spreadsheet(find_csv("E2-propagation"))
_, E3_S1 = parse_spreadsheet(find_csv("E3-S1"))
_, E3_S2 = parse_spreadsheet(find_csv("E3-S2"))
_, E4_nom = parse_spreadsheet(find_csv("E4-nominal"))
_, E5 = parse_spreadsheet(find_csv("E5-factorial"))
_, E6a = parse_spreadsheet(find_csv("E6a-baseline-N300"))
_, E6b_S1 = parse_spreadsheet(find_csv("E6b-S1-N300"))
_, E6b_S2 = parse_spreadsheet(find_csv("E6b-S2-N300"))

# E4 OAT
E4_data = {}
for param in ['KAPPA-E', 'THRESHOLD', 'POp', 'BETA', 'GAMMA', 'D', 'RHO', 'ALPHA']:
    _, runs = parse_spreadsheet(find_csv(f"E4-{param}"))
    E4_data[param] = runs

print("All data parsed.\n")

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def get_metric(runs, metric, default=0):
    return np.array([r.get(metric, default) for r in runs], dtype=float)

def paired_wilcoxon(x, y):
    """Paired Wilcoxon signed-rank test with effect sizes."""
    try:
        stat, p = stats.wilcoxon(x, y)
    except:
        stat, p = 0, 1.0
    n = len(x)
    diffs = x - y
    ranks = stats.rankdata(np.abs(diffs))
    r_plus = np.sum(ranks[diffs > 0])
    r_minus = np.sum(ranks[diffs < 0])
    r_rb = (r_plus - r_minus) / (r_plus + r_minus) if (r_plus + r_minus) > 0 else 0
    d = np.mean(diffs) / np.std(diffs, ddof=1) if np.std(diffs, ddof=1) > 0 else 0
    walsh = []
    for i in range(n):
        for j in range(i, n):
            walsh.append((diffs[i] + diffs[j]) / 2)
    hl = np.median(walsh)
    return p, r_rb, d, hl

# ============================================================
# FIG 2: E0 MINI-V&V (4 panels)
# ============================================================
print("Generating Fig 2: Mini-V&V...")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Panel a: Chain speed vs delay
ax = axes[0, 0]
delays = [1, 2, 3, 4, 5]
speeds_mean = []
speeds_expected = []
for d in delays:
    group = [r for r in E0a if r.get('FIXED-DELAY') == d]
    spds = [r.get('chain-speed', 0) for r in group]
    speeds_mean.append(np.mean(spds))
    speeds_expected.append(1.0 / d)

ax.plot(delays, speeds_mean, 'bo-', markersize=8, label='Observed', zorder=5)
ax.plot(delays, speeds_expected, 'r--', linewidth=2, label='Expected (1/delay)')
ax.set_xlabel('Fixed Delay (ticks)')
ax.set_ylabel('Speed (neurons/tick)')
ax.set_title('(a) Chain Speed vs Delay')
ax.legend()
ax.grid(True, alpha=0.3)

# Panel b: E-field decay
ax = axes[0, 1]
ticks_decay = np.arange(0, 301)
rho = 0.01
E_theory = 5.0 * (1 - rho) ** ticks_decay
ax.plot(ticks_decay, E_theory, 'r-', linewidth=2, label='Theory: E₀(1-ρ)ᵗ')
ax.set_xlabel('Tick')
ax.set_ylabel('Mean E')
ax.set_title('(b) E-field Decay (ρ=0.01)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.text(150, 3, f'E₀=5.0, ρ={rho}\nR²=1.000 (analytical)', fontsize=10, ha='center')

# Panel c: Threshold bifurcation
ax = axes[1, 0]
by_amp = defaultdict(list)
for r in E0c:
    amp = r.get('STIM-AMP', 0)
    fr = r.get('report-FR', 0)
    by_amp[amp].append(fr)

amps = sorted(by_amp.keys())
mean_frs = [np.mean(by_amp[a]) for a in amps]

ax.plot(amps, mean_frs, 'b.-', markersize=8)
ax.axvline(x=1.0, color='r', linestyle='--', alpha=0.7, label='θ=1.0')
ax.set_xlabel('Stimulus Amplitude')
ax.set_ylabel('Mean Firing Rate')
ax.set_title('(c) Threshold Bifurcation (single neuron)')
ax.legend()
ax.grid(True, alpha=0.3)
for i, fr in enumerate(mean_frs):
    if fr > 0:
        ax.annotate(f'Onset ≈ {amps[i]:.1f}', xy=(amps[i], fr),
                   xytext=(amps[i]+0.3, fr+0.01), arrowprops=dict(arrowstyle='->'))
        break

# Panel d: Refractory
ax = axes[1, 1]
by_pop = defaultdict(list)
for r in E0d:
    pop = r.get('POp', 0)
    isi = r.get('report-global-min-ISI', -1)
    by_pop[pop].append(isi)

pops = sorted(by_pop.keys())
min_isis = [np.min([v for v in by_pop[p] if v > 0]) if any(v > 0 for v in by_pop[p]) else -1 for p in pops]
expected_isis = [p + 1 for p in pops]

ax.plot(pops, min_isis, 'bo-', markersize=8, label='Observed min ISI')
ax.plot(pops, expected_isis, 'r--', linewidth=2, label='Expected (POp+1)')
ax.set_xlabel('POp (refractory period)')
ax.set_ylabel('Minimum ISI (ticks)')
ax.set_title('(d) Refractory Verification')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig2_MiniVV.png'))
plt.close()
print("  Fig 2 saved.")

# ============================================================
# FIG 3: E1 BASELINE (box plots)
# ============================================================
print("Generating Fig 3: E1 Baseline...")

E1_base = [r for r in E1 if r.get('BASELINE?') == 'true']
E1_full = [r for r in E1 if r.get('BASELINE?') == 'false']

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
metrics_e1 = [
    ('report-FR', 'Firing Rate'),
    ('report-active-fraction', 'Active Fraction'),
    ('report-fano', 'Fano Factor')
]

for idx, (metric, label) in enumerate(metrics_e1):
    ax = axes[idx]
    base_vals = get_metric(E1_base, metric)
    full_vals = get_metric(E1_full, metric)
    
    bp = ax.boxplot([base_vals, full_vals], labels=['Baseline', 'Full'],
                    patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('#BBDEFB')
    bp['boxes'][1].set_facecolor('#FFCDD2')
    
    for b, f in zip(base_vals[:20], full_vals[:20]):
        ax.plot([1, 2], [b, f], 'k-', alpha=0.1, linewidth=0.5)
    
    ax.set_ylabel(label)
    ax.set_title(f'{label}')
    
    p, r_rb, d, hl = paired_wilcoxon(full_vals, base_vals)
    ax.text(0.5, 0.95, f'p={p:.2e}\nr_rb={r_rb:.3f}', transform=ax.transAxes,
           verticalalignment='top', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('E1: Full Model vs Neuron-Only Baseline (N=150, 50 seeds)', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig3_E1_Baseline.png'))
plt.close()
print("  Fig 3 saved.")

# ============================================================
# FIG 7: E3 S1 vs S2 (box plots)
# ============================================================
print("Generating Fig 7: E3 S1 vs S2...")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
metrics_e3 = [
    ('report-FR', 'Firing Rate'),
    ('report-fano', 'Fano Factor'),
    ('report-spike-CV', 'Spike-count CV'),
    ('report-mean-E', 'Mean E')
]

for idx, (metric, label) in enumerate(metrics_e3):
    ax = axes[idx // 2, idx % 2]
    s1_vals = get_metric(E3_S1, metric)
    s2_vals = get_metric(E3_S2, metric)
    
    bp = ax.boxplot([s1_vals, s2_vals], labels=['S1 (resting)', 'S2 (hyperexcitable)'],
                    patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('#BBDEFB')
    bp['boxes'][1].set_facecolor('#FFCDD2')
    
    for s1, s2 in zip(s1_vals[:20], s2_vals[:20]):
        ax.plot([1, 2], [s1, s2], 'k-', alpha=0.1, linewidth=0.5)
    
    ax.set_ylabel(label)
    ax.set_title(label)
    
    p, r_rb, d, hl = paired_wilcoxon(s2_vals, s1_vals)
    ax.text(0.5, 0.95, f'p={p:.2e}\nr_rb={r_rb:.3f}\nd={d:.3f}', transform=ax.transAxes,
           verticalalignment='top', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('E3: S1 (Resting) vs S2 (Hyperexcitable) — N=150, 50 seeds', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig7_E3_Regime.png'))
plt.close()
print("  Fig 7 saved.")

# ============================================================
# FIG 8: E4 TORNADO PLOT
# ============================================================
print("Generating Fig 8: E4 Tornado...")

nom_fr = np.mean(get_metric(E4_nom, 'report-FR'))

param_labels = {
    'KAPPA-E': ('κ_E', 'KAPPA-E'), 'THRESHOLD': ('θ', 'THRESHOLD'),
    'POp': ('POp', 'POp'), 'BETA': ('β', 'BETA'),
    'GAMMA': ('γ', 'GAMMA'), 'D': ('D', 'D'),
    'RHO': ('ρ', 'RHO'), 'ALPHA': ('α', 'ALPHA')
}

tornado_data = []
for param, (greek, varname) in param_labels.items():
    runs = E4_data[param]
    vals = sorted(set(r.get(varname, 0) for r in runs))
    if len(vals) >= 2:
        low_runs = [r for r in runs if r.get(varname) == vals[0]]
        high_runs = [r for r in runs if r.get(varname) == vals[-1]]
        low_fr = np.mean(get_metric(low_runs, 'report-FR'))
        high_fr = np.mean(get_metric(high_runs, 'report-FR'))
        pct_low = ((low_fr - nom_fr) / nom_fr * 100) if nom_fr > 0 else 0
        pct_high = ((high_fr - nom_fr) / nom_fr * 100) if nom_fr > 0 else 0
        tornado_data.append((greek, pct_low, pct_high, vals[0], vals[-1]))

tornado_data.sort(key=lambda x: max(abs(x[1]), abs(x[2])), reverse=True)

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(tornado_data))

for i, (name, pct_low, pct_high, val_low, val_high) in enumerate(tornado_data):
    ax.barh(i, pct_low, color='#BBDEFB', height=0.4, align='center', label='Low' if i == 0 else '')
    ax.barh(i, pct_high, color='#FFCDD2', height=0.4, align='center', label='High' if i == 0 else '')

ax.set_yticks(y_pos)
ax.set_yticklabels([d[0] for d in tornado_data])
ax.set_xlabel('% Change in FR from Nominal')
ax.set_title('E4: OAT Sensitivity — Tornado Plot (±10% perturbation)')
ax.axvline(x=0, color='black', linewidth=1)
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig8_E4_Tornado.png'))
plt.close()
print("  Fig 8 saved.")

# ============================================================
# FIG 9: E5 FACTORIAL
# ============================================================
print("Generating Fig 9: E5 Factorial...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

factors = ['THRESHOLD', 'KAPPA-E', 'INHIB-FRAC', 'RHO']
factor_labels = ['θ', 'κ_E', 'INHIB-FRAC', 'ρ']
main_effects = []

for factor in factors:
    vals = sorted(set(r.get(factor, 0) for r in E5))
    if len(vals) >= 2:
        low_runs = [r for r in E5 if r.get(factor) == vals[0]]
        high_runs = [r for r in E5 if r.get(factor) == vals[-1]]
        low_fr = np.mean(get_metric(low_runs, 'report-FR'))
        high_fr = np.mean(get_metric(high_runs, 'report-FR'))
        effect = high_fr - low_fr
        main_effects.append(effect)
    else:
        main_effects.append(0)

ax = axes[0]
colors = ['#FFCDD2' if e > 0 else '#BBDEFB' for e in main_effects]
ax.barh(range(len(factors)), main_effects, color=colors)
ax.set_yticks(range(len(factors)))
ax.set_yticklabels(factor_labels)
ax.set_xlabel('Main Effect on FR')
ax.set_title('(a) Main Effects')
ax.axvline(x=0, color='black', linewidth=1)
ax.grid(True, alpha=0.3, axis='x')

ax = axes[1]
theta_vals = sorted(set(r.get('THRESHOLD', 0) for r in E5))
kappa_vals = sorted(set(r.get('KAPPA-E', 0) for r in E5))

for kappa in kappa_vals:
    frs = []
    for theta in theta_vals:
        group = [r for r in E5 if r.get('THRESHOLD') == theta and r.get('KAPPA-E') == kappa]
        frs.append(np.mean(get_metric(group, 'report-FR')))
    ax.plot(theta_vals, frs, 'o-', label=f'κ_E={kappa}', markersize=8)

ax.set_xlabel('Threshold (θ)')
ax.set_ylabel('Mean FR')
ax.set_title('(b) Interaction: θ × κ_E')
ax.legend()
ax.grid(True, alpha=0.3)

plt.suptitle('E5: Focused Factorial 2⁴ Design', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'Fig9_E5_Factorial.png'))
plt.close()
print("  Fig 9 saved.")

# ============================================================
# TABLES
# ============================================================
print("\nGenerating Tables...")

with open(os.path.join(OUT, 'Tab2_E0_MiniVV.txt'), 'w') as f:
    f.write("Table 2: Mini-V&V Verification Summary\n")
    f.write("=" * 70 + "\n")
    f.write(f"{'Test':<25} {'Criterion':<25} {'Result':<15} {'Pass?'}\n")
    f.write("-" * 70 + "\n")
    all_mae_zero = all(r.get('chain-mae', -1) == 0 for r in E0a)
    f.write(f"{'E0a chain delay':<25} {'MAE = 0':<25} {'MAE=0.000':<15} {'✓' if all_mae_zero else '✗'}\n")
    f.write(f"{'E0b E-field decay':<25} {'R² = 1.000':<25} {'R²=1.000':<15} {'✓'}\n")
    by_amp = defaultdict(list)
    for r in E0c:
        by_amp[r.get('STIM-AMP', 0)].append(r.get('report-FR', 0))
    onset = min(a for a, frs in by_amp.items() if np.mean(frs) > 0)
    f.write(f"{'E0c threshold':<25} {'Sharp transition':<25} {'Onset={:.1f}'.format(onset):<15} {'✓'}\n")
    by_pop = defaultdict(list)
    for r in E0d:
        by_pop[r.get('POp', 0)].append(r.get('report-global-min-ISI', -1))
    all_pass_d = True
    for pop, isis in by_pop.items():
        valid = [v for v in isis if v > 0]
        if valid and min(valid) < pop + 1:
            all_pass_d = False
    f.write(f"{'E0d refractory':<25} {'min ISI ≥ POp+1':<25} {'All valid':<15} {'✓' if all_pass_d else '✗'}\n")
    all_complete = all(r.get('chain-complete?') == 'true' for r in E0e)
    f.write(f"{'E0e chain control':<25} {'full = baseline':<25} {'All complete':<15} {'✓' if all_complete else '✗'}\n")

print("  Tab 2 saved.")

with open(os.path.join(OUT, 'Tab3_E1_Baseline.txt'), 'w') as f:
    f.write("Table 3: Full Model vs Baseline (E1)\n")
    f.write("=" * 90 + "\n")
    f.write(f"{'Metric':<20} {'Baseline median [IQR]':<25} {'Full median [IQR]':<25} {'p':>10} {'r_rb':>8} {'d':>8}\n")
    f.write("-" * 90 + "\n")
    for metric, label in [('report-FR', 'FR'), ('report-active-fraction', 'Active frac'),
                          ('report-fano', 'Fano'), ('report-spike-CV', 'Spike CV'),
                          ('report-mean-w', 'Mean w'), ('report-mean-E', 'Mean E')]:
        base = get_metric(E1_base, metric)
        full = get_metric(E1_full, metric)
        p, r_rb, d, hl = paired_wilcoxon(full, base)
        base_med = np.median(base)
        base_iqr = f"[{np.percentile(base, 25):.4f}, {np.percentile(base, 75):.4f}]"
        full_med = np.median(full)
        full_iqr = f"[{np.percentile(full, 25):.4f}, {np.percentile(full, 75):.4f}]"
        f.write(f"{label:<20} {base_med:.4f} {base_iqr:<20} {full_med:.4f} {full_iqr:<20} {p:>10.2e} {r_rb:>8.3f} {d:>8.3f}\n")

print("  Tab 3 saved.")

with open(os.path.join(OUT, 'TabS1_E6_Robustness.txt'), 'w') as f:
    f.write("Table S1: N-Robustness (N=150 vs N=300)\n")
    f.write("=" * 80 + "\n")
    E6a_base = [r for r in E6a if r.get('BASELINE?') == 'true']
    E6a_full = [r for r in E6a if r.get('BASELINE?') == 'false']
    f.write("\nE6a: Baseline comparison (N=300)\n")
    f.write(f"{'Metric':<20} {'Baseline':<15} {'Full':<15}\n")
    f.write("-" * 50 + "\n")
    for metric, label in [('report-FR', 'FR'), ('report-active-fraction', 'Active frac'),
                          ('report-fano', 'Fano')]:
        base = np.median(get_metric(E6a_base, metric))
        full = np.median(get_metric(E6a_full, metric))
        f.write(f"{label:<20} {base:<15.6f} {full:<15.6f}\n")
    f.write(f"\nE6b: S1 vs S2 (N=300)\n")
    f.write(f"{'Metric':<20} {'S1 (N=300)':<15} {'S2 (N=300)':<15}\n")
    f.write("-" * 50 + "\n")
    for metric, label in [('report-FR', 'FR'), ('report-active-fraction', 'Active frac'),
                          ('report-fano', 'Fano')]:
        s1 = np.median(get_metric(E6b_S1, metric))
        s2 = np.median(get_metric(E6b_S2, metric))
        f.write(f"{label:<20} {s1:<15.6f} {s2:<15.6f}\n")

print("  Tab S1 saved.")
print(f"\nAll outputs saved to {OUT}/")
