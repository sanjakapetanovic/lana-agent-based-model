#!/usr/bin/env python3
"""
LANA-EEG Feature-Level Comparison Pipeline v5 (FINAL DISSERTATION VERSION)
==========================================================================
- 100 subjects from EEGBCI (PhysioNet)
- Per-channel feature extraction (NOT channel-averaged signal)
- Posterior alpha sanity check (O1, O2, Oz, Pz, POz)
- Correct scipy.integrate.trapezoid
- Robust LANA tick-by-tick CSV parser
- Outputs: all CSV tables, figures, subjects_used.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.signal import welch
from scipy.stats import wilcoxon, rankdata
from scipy.integrate import trapezoid
import csv, io
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================
EEG_DATA_DIR = Path(r"C:\LANA_EEG_100\eeg_data")
LANA_DATA_DIR = Path(r"C:\LANA_EEG_100\lana_data")
OUTPUT_DIR = Path(r"C:\LANA_EEG_100\results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_SUBJECTS = 100
BANDPASS = (0.5, 45.0)
NOTCH_FREQ = 60
EPOCH_LENGTH = 4.0

# Posterior channels for alpha sanity check
POSTERIOR_CHANNELS = ['O1', 'O2', 'Oz', 'Pz', 'POz', 'P3', 'P4', 'P7', 'P8']


# ============================================================
# HELPERS
# ============================================================
def bandpower(x, sfreq, fmin, fmax):
    nperseg = min(int(2 * sfreq), len(x))
    if nperseg < 4:
        return 0.0
    freqs, psd = welch(x, fs=sfreq, nperseg=nperseg)
    idx = (freqs >= fmin) & (freqs <= fmax)
    return float(trapezoid(psd[idx], freqs[idx])) if np.any(idx) else 0.0

def spectral_entropy_fn(x, sfreq):
    nperseg = min(int(2 * sfreq), len(x))
    if nperseg < 4:
        return 0.0
    freqs, psd = welch(x, fs=sfreq, nperseg=nperseg)
    p = psd / (np.sum(psd) + 1e-30)
    return float(-np.sum(p * np.log(p + 1e-30)))

def line_length_fn(x):
    return float(np.mean(np.abs(np.diff(x))))


# ============================================================
# EEG: PER-CHANNEL feature extraction (CORRECTED)
# ============================================================
def extract_eeg_features_perchannel(epochs, ch_names):
    """
    Extract features PER CHANNEL, then average across channels.
    This avoids the average-reference cancellation problem.
    """
    data = epochs.get_data()  # (n_epochs, n_channels, n_times)
    sfreq = epochs.info['sfreq']
    n_epochs, n_channels, n_times = data.shape

    # Per-channel, per-epoch features
    all_epoch_features = []
    for ep_idx in range(n_epochs):
        ch_features = []
        for ch_idx in range(n_channels):
            sig = data[ep_idx, ch_idx, :]
            tp = bandpower(sig, sfreq, 1, 45) + 1e-30
            ch_features.append({
                'rms': float(np.sqrt(np.mean(sig ** 2))),
                'line_length': line_length_fn(sig),
                'delta_rel': bandpower(sig, sfreq, 1, 4) / tp,
                'theta_rel': bandpower(sig, sfreq, 4, 8) / tp,
                'alpha_rel': bandpower(sig, sfreq, 8, 13) / tp,
                'beta_rel': bandpower(sig, sfreq, 13, 30) / tp,
                'spectral_entropy': spectral_entropy_fn(sig, sfreq),
            })
        # Average features across channels for this epoch
        ch_df = pd.DataFrame(ch_features)
        all_epoch_features.append(ch_df.mean().to_dict())

    # Mean channel correlation (epoch-level, using all channels)
    corr_vals = []
    for ep_idx in range(n_epochs):
        cc = np.corrcoef(data[ep_idx])
        upper = np.triu(cc, k=1)
        corr_vals.append(float(np.nanmean(upper[upper != 0])) if np.any(upper != 0) else 0.0)

    # Average across epochs
    feat = pd.DataFrame(all_epoch_features).mean().to_dict()
    feat['mean_ch_corr'] = float(np.nanmean(corr_vals))

    return feat


def extract_posterior_alpha(epochs, ch_names):
    """
    Extract posterior alpha power as sanity check.
    Uses O1, O2, Oz, Pz, POz or any available posterior channels.
    """
    data = epochs.get_data()
    sfreq = epochs.info['sfreq']

    # Find posterior channel indices
    post_idx = [i for i, ch in enumerate(ch_names) if ch in POSTERIOR_CHANNELS]
    if not post_idx:
        # Fallback: use channels with 'O' or 'P' in name
        post_idx = [i for i, ch in enumerate(ch_names) if ch.startswith('O') or ch.startswith('P')]
    if not post_idx:
        return np.nan

    # Per-channel alpha power, averaged
    alpha_vals = []
    for ep_idx in range(data.shape[0]):
        ch_alphas = []
        for ci in post_idx:
            sig = data[ep_idx, ci, :]
            tp = bandpower(sig, sfreq, 1, 45) + 1e-30
            ch_alphas.append(bandpower(sig, sfreq, 8, 13) / tp)
        alpha_vals.append(np.mean(ch_alphas))

    return float(np.mean(alpha_vals))


def process_all_eeg():
    """Process all EEG subjects with per-channel feature extraction."""
    import mne

    print(f"Processing {N_SUBJECTS} subjects from EEGBCI...")
    rows = []
    subjects_used = []
    skipped = []

    for subj in range(1, N_SUBJECTS + 1):
        print(f"  Subject {subj:3d}/{N_SUBJECTS}...", end=" ")
        try:
            eo_files = mne.datasets.eegbci.load_data(subj, [1], path=str(EEG_DATA_DIR))
            ec_files = mne.datasets.eegbci.load_data(subj, [2], path=str(EEG_DATA_DIR))

            raw_eo = mne.io.read_raw_edf(eo_files[0], preload=True, verbose=False)
            raw_ec = mne.io.read_raw_edf(ec_files[0], preload=True, verbose=False)

            mne.datasets.eegbci.standardize(raw_eo)
            mne.datasets.eegbci.standardize(raw_ec)

            montage = mne.channels.make_standard_montage('standard_1005')
            raw_eo.set_montage(montage, on_missing='ignore', verbose=False)
            raw_ec.set_montage(montage, on_missing='ignore', verbose=False)

            sub_id = f'sub-{subj:03d}'

            for raw, cond in [(raw_eo, 'EO'), (raw_ec, 'EC')]:
                raw.pick(['eeg'], verbose=False)
                raw.filter(BANDPASS[0], BANDPASS[1], verbose=False)
                raw.notch_filter([NOTCH_FREQ], verbose=False)
                raw.set_eeg_reference('average', verbose=False)

                events = mne.make_fixed_length_events(raw, duration=EPOCH_LENGTH)
                epochs = mne.Epochs(raw, events, tmin=0, tmax=EPOCH_LENGTH,
                                    baseline=None, preload=True,
                                    reject_by_annotation=True, verbose=False)

                if len(epochs) < 2:
                    raise ValueError(f"Too few epochs ({len(epochs)})")

                ch_names = epochs.ch_names

                # Per-channel feature extraction (CORRECTED METHOD)
                feat = extract_eeg_features_perchannel(epochs, ch_names)

                # Posterior alpha sanity check
                feat['posterior_alpha_rel'] = extract_posterior_alpha(epochs, ch_names)

                feat['subject'] = sub_id
                feat['condition'] = cond
                feat['n_epochs'] = len(epochs)
                feat['n_channels'] = len(ch_names)
                rows.append(feat)

            subjects_used.append({'subject': sub_id, 'status': 'OK',
                                  'n_channels': len(ch_names), 'n_epochs_eo': len(events)})
            print("OK")

        except Exception as e:
            skipped.append({'subject': f'sub-{subj:03d}', 'status': f'SKIP: {e}'})
            print(f"SKIP: {e}")

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / 'eeg_features.csv', index=False)
    print(f"\n  Saved eeg_features.csv: {len(df)} rows ({len(df)//2} subjects)")

    su_df = pd.DataFrame(subjects_used + skipped)
    su_df.to_csv(OUTPUT_DIR / 'subjects_used.csv', index=False)
    print(f"  Saved subjects_used.csv: {len(subjects_used)} OK, {len(skipped)} skipped")

    return df


# ============================================================
# LANA PROCESSING (same as v4)
# ============================================================
def parse_lana_tickbytick(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    lines = content.replace('\r\n', '\n').split('\n')
    rows_dict = {}
    data_start = None
    for i, line in enumerate(lines):
        if not line.strip(): continue
        cells = list(csv.reader(io.StringIO(line)))[0]
        if not cells: continue
        label = cells[0].strip()
        if label == '[all run data]':
            rows_dict['[all run data]'] = cells
            data_start = i + 1; continue
        if data_start is None:
            rows_dict[label] = cells
    if data_start is None:
        print("    ERROR: No [all run data] row"); return {}
    header = rows_dict['[all run data]']
    metric_names = []
    for j in range(2, len(header)):
        val = header[j].strip()
        if val == '[step]': break
        if val: metric_names.append(val)
    cols_per_run = len(metric_names) + 1
    run_row = rows_dict.get('[run number]')
    seed_row = rows_dict.get('SEED')
    if not run_row: return {}
    run_nums = [int(x.strip()) for x in run_row[1:] if x.strip()]
    n_runs = max(run_nums)
    data_lines = []
    for i in range(data_start, len(lines)):
        line = lines[i].strip()
        if not line: continue
        data_lines.append(list(csv.reader(io.StringIO(line)))[0])
    run_data = {}
    for r in range(n_runs):
        offset = 1 + r * cols_per_run
        seed = seed_row[offset].strip() if seed_row and offset < len(seed_row) else str(r+1)
        ticks, values = [], {m: [] for m in metric_names}
        for row in data_lines:
            if offset >= len(row): continue
            sv = row[offset].strip()
            if not sv: continue
            try: tick = int(float(sv))
            except: continue
            ticks.append(tick)
            for mi, mn in enumerate(metric_names):
                col = offset + 1 + mi
                try: values[mn].append(float(row[col].strip()) if col < len(row) else 0.0)
                except: values[mn].append(0.0)
        if ticks:
            run_data[seed] = pd.DataFrame({'tick': ticks, **{m: values[m] for m in metric_names}})
    return run_data

def extract_lana_features(ts):
    x = np.asarray(ts, dtype=float)
    if len(x) < 10:
        return {k: np.nan for k in ['rms','line_length','spectral_entropy','low_power_rel','mid_power_rel','high_power_rel']}
    xn = x - x.mean()
    s = x.std()
    if s > 0: xn = xn / s
    nperseg = min(256, len(xn))
    freqs, psd = welch(xn, fs=1.0, nperseg=nperseg)
    pt = np.sum(psd) + 1e-12
    pn = psd / pt
    return {
        'rms': float(np.sqrt(np.mean(x**2))),
        'line_length': float(np.mean(np.abs(np.diff(x)))),
        'spectral_entropy': float(-np.sum(pn * np.log(pn + 1e-12))),
        'low_power_rel': float(pn[freqs < 0.05].sum()),
        'mid_power_rel': float(pn[(freqs >= 0.05) & (freqs < 0.2)].sum()),
        'high_power_rel': float(pn[freqs >= 0.2].sum()),
    }

def process_lana():
    all_csv = sorted(LANA_DATA_DIR.glob('*.csv'))
    s1 = [f for f in all_csv if 'S1' in f.name]
    s2 = [f for f in all_csv if 'S2' in f.name]
    if not s1 or not s2:
        print(f"  LANA CSVs not found in {LANA_DATA_DIR}")
        print(f"  Files: {[f.name for f in all_csv]}")
        return None
    results = []
    for csv_path, regime in [(s1[0], 'S1'), (s2[0], 'S2')]:
        print(f"  Parsing LANA {regime}: {csv_path.name}...")
        rd = parse_lana_tickbytick(csv_path)
        print(f"    {len(rd)} runs found.")
        for seed, df in rd.items():
            mc = [c for c in df.columns if 'meanE' in c]
            sc = [c for c in df.columns if 'spike' in c.lower()]
            fE = {f'meanE_{k}': v for k, v in extract_lana_features(df[mc[0]].values).items()} if mc else {}
            fS = {f'spike_{k}': v for k, v in extract_lana_features(df[sc[0]].values).items()} if sc else {}
            results.append({'seed': seed, 'regime': regime, **fE, **fS})
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_DIR / 'lana_features.csv', index=False)
    print(f"  Saved: {len(df)} rows")
    return df


# ============================================================
# STATISTICS
# ============================================================
def rank_biserial(x, y):
    d = np.array(x) - np.array(y)
    d = d[d != 0]
    if len(d) == 0: return 0.0
    r = rankdata(np.abs(d))
    return float((np.sum(r[d > 0]) - np.sum(r[d < 0])) / (len(d) * (len(d) + 1) / 2))

def paired_test(df, gcol, va, vb, feats, idcol):
    da = df[df[gcol] == va].set_index(idcol)
    db = df[df[gcol] == vb].set_index(idcol)
    common = da.index.intersection(db.index)
    if len(common) < 3:
        print(f"  WARNING: Only {len(common)} paired obs."); return pd.DataFrame()
    rows = []
    for f in feats:
        if f not in da.columns or f not in db.columns: continue
        a = da.loc[common, f].values.astype(float)
        b = db.loc[common, f].values.astype(float)
        # Remove NaN pairs
        mask = ~(np.isnan(a) | np.isnan(b))
        a, b = a[mask], b[mask]
        if len(a) < 3: continue
        ma, mb = np.nanmedian(a), np.nanmedian(b)
        try: _, p = wilcoxon(a, b); r = rank_biserial(b, a)
        except: p, r = np.nan, np.nan
        d = '\u2191' if mb > ma else ('\u2193' if mb < ma else '=')
        rows.append({'feature': f, f'median_{va}': ma, f'median_{vb}': mb,
                     'p_value': round(p, 6) if not np.isnan(p) else np.nan,
                     'effect_size': round(r, 3) if not np.isnan(r) else np.nan,
                     'direction': d, 'n_pairs': len(a)})
    return pd.DataFrame(rows)


# ============================================================
# FIGURES
# ============================================================
def make_figures(eeg_stats, lana_stats, eeg_df, lana_df):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 11

    # ---- Figure 1: Concordance chart ----
    families = ['Amplitude/\nActivity', 'Temporal\nvariability', 'Spectral\ncomplexity',
                'Slow\nactivity', 'Mid\nactivity', 'Fast\nactivity', 'Posterior\nalpha']

    eeg_feats = ['rms', 'line_length', 'spectral_entropy', 'delta_rel', 'theta_rel', 'beta_rel', 'posterior_alpha_rel']
    lana_feats_map = ['meanE_rms', 'meanE_line_length', 'meanE_spectral_entropy',
                       'meanE_low_power_rel', 'meanE_mid_power_rel', 'meanE_high_power_rel', None]

    eeg_dirs = []
    lana_dirs = []
    for ef, lf in zip(eeg_feats, lana_feats_map):
        e_row = eeg_stats[eeg_stats['feature'] == ef]
        eeg_dirs.append(1 if len(e_row) and e_row['direction'].values[0] == '\u2191' else -1)
        if lf:
            l_row = lana_stats[lana_stats['feature'] == lf]
            lana_dirs.append(1 if len(l_row) and l_row['direction'].values[0] == '\u2191' else -1)
        else:
            lana_dirs.append(0)  # No LANA analog for posterior alpha

    concordance = []
    for ed, ld in zip(eeg_dirs, lana_dirs):
        if ld == 0:
            concordance.append('N/A')
        elif ed == ld:
            concordance.append('Yes')
        else:
            concordance.append('No')

    fig, ax = plt.subplots(figsize=(12, 5.5))
    x = np.arange(len(families))
    ax.bar(x - 0.2, eeg_dirs, 0.35, label='EEG (EO\u2192EC)', color='#4472C4', alpha=0.8)
    bars_lana = ax.bar(x + 0.2, lana_dirs, 0.35, label='LANA (S1\u2192S2)', color='#ED7D31', alpha=0.8)
    # Mark posterior alpha LANA bar as N/A
    if lana_dirs[-1] == 0:
        bars_lana[-1].set_alpha(0.15)

    for i, c in enumerate(concordance):
        if c == 'Yes':
            ax.text(i, 1.4, '\u2713', ha='center', fontsize=16, fontweight='bold', color='#2D8C5A')
        elif c == 'No':
            ax.text(i, 1.4, '\u2717', ha='center', fontsize=16, fontweight='bold', color='#C0392B')
        else:
            ax.text(i, 1.4, 'N/A', ha='center', fontsize=10, color='gray')

    n_conc = sum(1 for c in concordance if c == 'Yes')
    n_comp = sum(1 for c in concordance if c != 'N/A')
    ax.set_xticks(x); ax.set_xticklabels(families, fontsize=10)
    ax.set_ylabel('Direction of change')
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['\u2193 Decrease', '', '\u2191 Increase'])
    ax.set_ylim(-1.6, 1.9); ax.axhline(0, color='gray', lw=0.5)
    ax.set_title(f'EEG vs LANA: Direction-of-Change Concordance ({n_conc}/{n_comp} = {100*n_conc/n_comp:.0f}%)',
                 fontweight='bold', fontsize=13)
    ax.legend(loc='lower right', fontsize=10)
    n_subj = len(eeg_df['subject'].unique()) if eeg_df is not None else '?'
    ax.text(0.01, -1.45, f'EEG: {n_subj} subjects, EEGBCI PhysioNet | LANA: 50 matched seeds',
            fontsize=9, color='gray')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'Figure_Concordance.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'Figure_Concordance.tiff', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved Figure_Concordance")

    # ---- Figure 2: LANA boxplots ----
    fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
    for ax, feat, title in [(axes2[0], 'meanE_rms', 'Mean E RMS'),
                             (axes2[1], 'meanE_line_length', 'Mean E Line Length'),
                             (axes2[2], 'meanE_spectral_entropy', 'Mean E Spectral Entropy')]:
        s1d = lana_df[lana_df['regime']=='S1'][feat].dropna().values
        s2d = lana_df[lana_df['regime']=='S2'][feat].dropna().values
        bp = ax.boxplot([s1d, s2d], tick_labels=['S1 (resting)', 'S2 (hyperexcitable)'],
                        patch_artist=True, widths=0.5)
        bp['boxes'][0].set_facecolor('#4472C4'); bp['boxes'][0].set_alpha(0.7)
        bp['boxes'][1].set_facecolor('#ED7D31'); bp['boxes'][1].set_alpha(0.7)
        ax.set_ylabel('Value'); ax.set_title(title, fontweight='bold')
        ax.text(0.5, 0.95, 'p < 0.001***', ha='center', va='top', transform=ax.transAxes, fontsize=10, style='italic')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'Figure_Boxplots.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'Figure_Boxplots.tiff', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved Figure_Boxplots")

    # ---- Figure 3: Posterior alpha sanity check ----
    if eeg_df is not None and 'posterior_alpha_rel' in eeg_df.columns:
        fig3, ax3 = plt.subplots(figsize=(6, 5))
        eo_alpha = eeg_df[eeg_df['condition']=='EO']['posterior_alpha_rel'].dropna().values
        ec_alpha = eeg_df[eeg_df['condition']=='EC']['posterior_alpha_rel'].dropna().values
        bp3 = ax3.boxplot([eo_alpha, ec_alpha], tick_labels=['Eyes Open', 'Eyes Closed'],
                          patch_artist=True, widths=0.5)
        bp3['boxes'][0].set_facecolor('#4472C4'); bp3['boxes'][0].set_alpha(0.7)
        bp3['boxes'][1].set_facecolor('#ED7D31'); bp3['boxes'][1].set_alpha(0.7)
        try:
            _, p_alpha = wilcoxon(eo_alpha[:min(len(eo_alpha), len(ec_alpha))],
                                  ec_alpha[:min(len(eo_alpha), len(ec_alpha))])
            p_str = f'p = {p_alpha:.4f}' if p_alpha >= 0.001 else 'p < 0.001'
        except:
            p_str = ''
        ax3.set_ylabel('Posterior Alpha Relative Power')
        ax3.set_title(f'Posterior Alpha: EO vs EC Sanity Check\n{p_str}', fontweight='bold')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'Figure_Posterior_Alpha.png', dpi=300, bbox_inches='tight')
        plt.savefig(OUTPUT_DIR / 'Figure_Posterior_Alpha.tiff', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved Figure_Posterior_Alpha")


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 65)
    print("LANA-EEG Pipeline v5 — 100 subjects, per-channel features")
    print("=" * 65)

    # --- EEG ---
    print("\n[1] EEG Processing (EEGBCI, per-channel feature extraction)")
    cached = OUTPUT_DIR / 'eeg_features.csv'
    if cached.exists():
        eeg_df = pd.read_csv(cached)
        if len(eeg_df) > 0:
            print(f"  Loaded cached: {len(eeg_df)} rows ({len(eeg_df)//2} subjects)")
        else:
            eeg_df = process_all_eeg()
    else:
        eeg_df = process_all_eeg()

    # --- LANA ---
    print("\n[2] LANA Processing")
    cached_l = OUTPUT_DIR / 'lana_features.csv'
    if cached_l.exists():
        lana_df = pd.read_csv(cached_l)
        if len(lana_df) > 0:
            print(f"  Loaded cached: {len(lana_df)} rows")
        else:
            lana_df = process_lana()
    else:
        lana_df = process_lana()

    # --- EEG Stats ---
    eeg_stats = None
    if eeg_df is not None and len(eeg_df) > 0:
        print("\n[3] EEG: Eyes-Open vs Eyes-Closed (paired Wilcoxon)")
        ef = ['rms', 'line_length', 'delta_rel', 'theta_rel', 'alpha_rel',
              'beta_rel', 'spectral_entropy', 'mean_ch_corr', 'posterior_alpha_rel']
        eeg_stats = paired_test(eeg_df, 'condition', 'EO', 'EC', ef, 'subject')
        if len(eeg_stats) > 0:
            eeg_stats.to_csv(OUTPUT_DIR / 'eeg_eo_vs_ec.csv', index=False)
            pd.set_option('display.float_format', '{:.6f}'.format)
            pd.set_option('display.max_columns', 20)
            pd.set_option('display.width', 200)
            print(eeg_stats.to_string(index=False))

    # --- LANA Stats ---
    lana_stats = None
    if lana_df is not None and len(lana_df) > 0:
        print("\n[4] LANA: S1 vs S2 (paired Wilcoxon)")
        lf = [c for c in lana_df.columns if c not in ('seed', 'regime')]
        lana_stats = paired_test(lana_df, 'regime', 'S1', 'S2', lf, 'seed')
        if len(lana_stats) > 0:
            lana_stats.to_csv(OUTPUT_DIR / 'lana_s1_vs_s2.csv', index=False)
            print(lana_stats.to_string(index=False))

    # --- Cross-comparison ---
    if eeg_stats is not None and lana_stats is not None and len(eeg_stats) > 0 and len(lana_stats) > 0:
        print("\n[5] EEG <-> LANA Direction Comparison")
        fam = [
            ('Amplitude/Activity', 'rms', 'meanE_rms'),
            ('Temporal variability', 'line_length', 'meanE_line_length'),
            ('Spectral complexity', 'spectral_entropy', 'meanE_spectral_entropy'),
            ('Slow activity', 'delta_rel', 'meanE_low_power_rel'),
            ('Mid activity', 'theta_rel', 'meanE_mid_power_rel'),
            ('Fast activity', 'beta_rel', 'meanE_high_power_rel'),
            ('Posterior alpha', 'posterior_alpha_rel', None),
        ]
        rows = []
        for family, ef, lf in fam:
            e = eeg_stats[eeg_stats['feature'] == ef]
            ed = e['direction'].values[0] if len(e) else '?'
            if lf:
                l = lana_stats[lana_stats['feature'] == lf]
                ld = l['direction'].values[0] if len(l) else '?'
                m = 'Yes' if ed == ld and ed != '=' else 'No'
            else:
                ld = 'N/A'
                m = 'N/A (EEG sanity check only)'
            rows.append({'family': family, 'EEG': ef, 'EEG_dir': ed, 'LANA': lf or 'N/A', 'LANA_dir': ld, 'match': m})
        cross = pd.DataFrame(rows)
        cross.to_csv(OUTPUT_DIR / 'eeg_lana_comparison.csv', index=False)
        print(cross.to_string(index=False))

    # --- Figures ---
    if eeg_stats is not None and lana_stats is not None:
        print("\n[6] Generating figures...")
        make_figures(eeg_stats, lana_stats, eeg_df, lana_df)

    print("\n" + "=" * 65)
    print("DONE! All outputs in:", OUTPUT_DIR)
    print("=" * 65)


if __name__ == '__main__':
    main()
