"""
Generate manuscript figures from raw BehaviorSpace outputs.

Usage:
  python -m analysis.make_figures --input data/raw --output figures --format png

This script regenerates the **data-driven** figures (Figures 2–10).
Figure 1 (conceptual architecture) is a schematic and is therefore not regenerated here.

License: MIT
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .parse_behaviorspace import parse_final, parse_all_run_data


def _save(path: Path, fmt: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path.with_suffix("." + fmt), dpi=300)
    plt.close()


def _ci95(sd: np.ndarray, n: np.ndarray) -> np.ndarray:
    n = np.maximum(n, 1)
    return 1.96 * sd / np.sqrt(n)


def fig_v1_chain_speed(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_final(in_dir / "V1_chain_delay.csv")
    g = df.groupby("FIXED-DELAY")["chain-speed"].agg(["mean", "std", "count"]).reset_index()
    x = g["FIXED-DELAY"].to_numpy(dtype=float)
    y = g["mean"].to_numpy(dtype=float)
    yerr = _ci95(g["std"].to_numpy(dtype=float), g["count"].to_numpy(dtype=float))

    plt.figure()
    plt.errorbar(x, y, yerr=yerr, fmt="o", label="Measured")
    plt.plot(x, 1.0 / x, linestyle="--", label="Theory (1/delay)")
    plt.xlabel("FIXED-DELAY (ticks)")
    plt.ylabel("Speed (neurons/tick)")
    plt.title("V1: Chain delay verification")
    plt.legend()
    _save(out_dir / "Fig02_V1_chain_speed_reproduced", fmt)


def fig_v2_decay(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_all_run_data(in_dir / "V2_energy_decay.csv")
    g = df.groupby("ticks")["decay-E-current"].mean().reset_index()
    t = g["ticks"].to_numpy(dtype=float)
    E = g["decay-E-current"].to_numpy(dtype=float)

    # analytic curve (rho=0.01, E0=5)
    rho = 0.01
    E0 = 5.0
    theory = E0 * (1 - rho) ** t

    plt.figure()
    plt.plot(t, E, label="NetLogo mean")
    plt.plot(t, theory, linestyle="--", label="Theory")
    plt.xlabel("ticks")
    plt.ylabel("Mean E")
    plt.title("V2: Energy decay verification")
    plt.legend()
    _save(out_dir / "Fig03_V2_energy_decay_reproduced", fmt)


def fig_m1_threshold(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_final(in_dir / "M1_threshold_bifurcation.csv")
    g = df.groupby("STIM-AMP")["mean-firing-rate"].agg(["mean", "std", "count"]).reset_index()
    x = g["STIM-AMP"].to_numpy(dtype=float)
    y = g["mean"].to_numpy(dtype=float)
    yerr = _ci95(g["std"].to_numpy(dtype=float), g["count"].to_numpy(dtype=float))

    plt.figure()
    plt.errorbar(x, y, yerr=yerr, fmt="o-")
    plt.xlabel("STIM-AMP")
    plt.ylabel("Mean firing rate (spikes/tick)")
    plt.title("M1: Threshold bifurcation")
    _save(out_dir / "Fig04_M1_threshold_bifurcation_reproduced", fmt)


def fig_m2_refractory(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_final(in_dir / "M2_refractory.csv")
    g = df.groupby("POp")["global-min-isi"].agg(["mean", "std", "count"]).reset_index()
    x = g["POp"].to_numpy(dtype=float)
    y = g["mean"].to_numpy(dtype=float)

    plt.figure()
    plt.plot(x, y, "o-", label="Measured")
    plt.plot(x, x + 1, linestyle="--", label="Theory (POp + 1)")
    plt.xlabel("POp (ticks)")
    plt.ylabel("Global minimum ISI (ticks)")
    plt.title("M2: Refractory enforcement")
    plt.legend()
    _save(out_dir / "Fig05_M2_refractory_reproduced", fmt)


def fig_n1(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_final(in_dir / "N1_ei_balance.csv")
    g = df.groupby("INHIB-FRAC")["mean-firing-rate"].agg(["mean", "std", "count"]).reset_index()
    x = g["INHIB-FRAC"].to_numpy(dtype=float)
    y = g["mean"].to_numpy(dtype=float)
    yerr = _ci95(g["std"].to_numpy(dtype=float), g["count"].to_numpy(dtype=float))

    plt.figure()
    plt.errorbar(x, y, yerr=yerr, fmt="o-")
    plt.xlabel("INHIB-FRAC")
    plt.ylabel("Mean firing rate (spikes/tick)")
    plt.title("N1: Excitation–inhibition balance")
    _save(out_dir / "Fig06_N1_ei_balance_reproduced", fmt)


def fig_n2(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_final(in_dir / "N2_phase_transition.csv")
    df["oscillatory"] = df["is-oscillating?"].astype(float)

    g = df.groupby("KAPPA-E").agg(
        fr_mean=("mean-firing-rate", "mean"),
        fr_sd=("mean-firing-rate", "std"),
        fr_n=("mean-firing-rate", "count"),
        cv_mean=("spike-cv", "mean"),
        cv_sd=("spike-cv", "std"),
        cv_n=("spike-cv", "count"),
        osc_frac=("oscillatory", "mean"),
    ).reset_index()

    x = g["KAPPA-E"].to_numpy(dtype=float)

    plt.figure()
    plt.plot(x, g["cv_mean"].to_numpy(dtype=float), "o-")
    plt.axhline(1.0, linestyle="--")
    plt.xlabel("KAPPA-E (κ_E)")
    plt.ylabel("Spike-count CV")
    plt.title("N2: Coupling-driven regime shift (CV)")
    _save(out_dir / "Fig07a_N2_CV_reproduced", fmt)

    plt.figure()
    plt.plot(x, 100 * g["osc_frac"].to_numpy(dtype=float), "o-")
    plt.xlabel("KAPPA-E (κ_E)")
    plt.ylabel("Oscillatory runs (%)")
    plt.title("N2: Oscillatory-like fraction")
    _save(out_dir / "Fig07b_N2_oscfrac_reproduced", fmt)


def fig_gsa_effect_sizes(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_final(in_dir / "GSA_sensitivity.csv")

    outcomes = {
        "FR": "mean-firing-rate",
        "Spikes": "final-total-spikes",
        "Active": "active-neuron-fraction",
        "Synchrony": "synchrony-index",
        "Mean weight": "mean-weight",
    }
    params = ["KAPPA-E", "RHO", "THRESHOLD"]

    # Compute effect sizes
    eff = {p: [] for p in params}
    for label, col in outcomes.items():
        grand = float(np.nanmean(df[col].to_numpy(dtype=float)))
        for p in params:
            means = df.groupby(p)[col].mean()
            es = (means.max() - means.min()) / grand * 100.0 if grand != 0 else np.nan
            eff[p].append(es)

    x = np.arange(len(outcomes))
    width = 0.25

    plt.figure()
    # Bars side-by-side: one series per parameter
    for i, p in enumerate(params):
        plt.bar(x + (i - 1) * width, eff[p], width=width, label=p)
    plt.xticks(x, list(outcomes.keys()), rotation=25, ha="right")
    plt.ylabel("Main effect size (%)")
    plt.title("GSA: Main effect sizes (normalized)")
    plt.legend()
    _save(out_dir / "Fig08_GSA_effect_sizes_reproduced", fmt)


def fig_r1_network_size(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_final(in_dir / "R1_network_size.csv")
    # Some exports may name the parameter slightly differently; handle both.
    by = "N-NODES" if "N-NODES" in df.columns else ("N-NODES?" if "N-NODES?" in df.columns else None)
    if by is None:
        return
    g = df.groupby(by)["mean-firing-rate"].agg(["mean", "std", "count"]).reset_index()
    x = g[by].to_numpy(dtype=float)
    y = g["mean"].to_numpy(dtype=float)
    yerr = _ci95(g["std"].to_numpy(dtype=float), g["count"].to_numpy(dtype=float))

    plt.figure()
    plt.errorbar(x, y, yerr=yerr, fmt="o-")
    plt.xlabel("N (neurons)")
    plt.ylabel("Mean firing rate (spikes/tick)")
    plt.title("R1: Robustness to network size")
    _save(out_dir / "Fig09_R1_network_size_reproduced", fmt)


def fig_r2_plasticity(in_dir: Path, out_dir: Path, fmt: str):
    df = parse_all_run_data(in_dir / "R2_plasticity.csv")
    g = df.groupby("ticks")["mean-weight"].agg(["mean", "std", "count"]).reset_index()
    t = g["ticks"].to_numpy(dtype=float)
    w = g["mean"].to_numpy(dtype=float)
    werr = _ci95(g["std"].to_numpy(dtype=float), g["count"].to_numpy(dtype=float))

    plt.figure()
    plt.plot(t, w, label="Mean weight")
    plt.fill_between(t, w - werr, w + werr, alpha=0.2)
    plt.xlabel("ticks")
    plt.ylabel("Mean synaptic weight")
    plt.title("R2: Plasticity convergence")
    plt.legend()
    _save(out_dir / "Fig10_R2_plasticity_convergence_reproduced", fmt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to data/raw folder")
    ap.add_argument("--output", required=True, help="Path to output figures folder")
    ap.add_argument("--format", default="png", choices=["png", "pdf"], help="Output format")
    args = ap.parse_args()

    in_dir = Path(args.input)
    out_dir = Path(args.output)

    fig_v1_chain_speed(in_dir, out_dir, args.format)
    fig_v2_decay(in_dir, out_dir, args.format)
    fig_m1_threshold(in_dir, out_dir, args.format)
    fig_m2_refractory(in_dir, out_dir, args.format)
    fig_n1(in_dir, out_dir, args.format)
    fig_n2(in_dir, out_dir, args.format)
    fig_gsa_effect_sizes(in_dir, out_dir, args.format)
    fig_r1_network_size(in_dir, out_dir, args.format)
    fig_r2_plasticity(in_dir, out_dir, args.format)

    print(f"Figures written to {out_dir}")


if __name__ == "__main__":
    main()
