"""
generate_quadrant_overview.py
==============================

Standalone-Skript fuer Abbildung in Kap. 3.3.1 (Quadrantenklassifikation).

Erzeugt eine Uebersichts-Abbildung, in der alle 6.521 Unternehmen-Kennzahl-
Kombinationen im gemeinsamen phi-sigma-Raum dargestellt werden, gefaerbt nach
Kennzahl. Quadranten-Trennlinien werden am GLOBALEN Median ueber alle Punkte
gezogen (nicht pro Kennzahl), Quadranten-Labels in die vier Ecken.

Wichtig: Diese Darstellung entspricht NICHT der eigentlichen Klassifikation
(die erfolgt pro Kennzahl mit eigenem Median). Sie dient als Uebersichts-
referenz, die Lage und Streuung der sieben Kennzahl-Verteilungen sichtbar
macht.

Output: PNG + PDF im output/ar/ Ordner.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "output" / "ar" / "ar_features.csv"
OUT_DIR = PROJECT_ROOT / "output" / "ar"

# Sieben Hauptkennzahlen (Reihenfolge wie in der Thesis: Profitabilitaet -> Liquiditaet -> Kapitalstruktur)
RATIOS_ORDER = [
    "ROA",
    "ROE",
    "EBIT_margin",
    "fcf_margin",
    "current_ratio",
    "debt_to_equity",
    "equity_ratio",
]

# Anzeige-Labels (Deutsch, wie in Thesis)
RATIO_LABELS = {
    "ROA": "ROA",
    "ROE": "ROE",
    "EBIT_margin": "EBIT-Marge",
    "fcf_margin": "FCF-Marge",
    "current_ratio": "Current Ratio",
    "debt_to_equity": "Debt/Equity",
    "equity_ratio": "Eigenkapitalquote",
}

# Farbpalette nach Gruppen: Profitabilitaet (Cool-Toene gespreizt), Liquiditaet (Gruen), Kapitalstruktur (Rot/Orange)
RATIO_COLORS = {
    "ROA":            "#08306b",   # Navy
    "ROE":            "#2c7fb8",   # Mittelblau
    "EBIT_margin":    "#6a51a3",   # Purpur
    "fcf_margin":     "#00bcd4",   # Tuerkis
    "current_ratio":  "#2ca02c",   # Gruen
    "debt_to_equity": "#d62728",   # Rot
    "equity_ratio":   "#ff7f0e",   # Orange
}

# Quadranten-Labels (deutsche Namen aus 3.3.1)
QUADRANT_LABELS = {
    "ll": "Korrektiv-Stabil",      # phi unter Median, sigma unter Median
    "lh": "Korrektiv-Volatil",     # phi unter Median, sigma ueber Median
    "rl": "Persistent-Stabil",     # phi ueber Median, sigma unter Median
    "rh": "Persistent-Volatil",    # phi ueber Median, sigma ueber Median
}


def main() -> None:
    # ---------------------------------------------------------------
    # 1. Daten laden + filtern auf die sieben Hauptkennzahlen
    # ---------------------------------------------------------------
    df = pd.read_csv(DATA_PATH)
    df = df[df["ratio"].isin(RATIOS_ORDER)].copy()
    df = df.dropna(subset=["phi1", "sigma_diff"])
    print(f"Datenpunkte gesamt (nach NA-Filter): {len(df):,}")

    # ---------------------------------------------------------------
    # 2. Globale Mediane (Quadranten-Trennlinien)
    # ---------------------------------------------------------------
    phi_median_global = df["phi1"].median()
    sigma_median_global = df["sigma_diff"].median()
    print(f"Globaler Median phi1   = {phi_median_global:+.4f}")
    print(f"Globaler Median sigma  = {sigma_median_global:.4f}")

    # ---------------------------------------------------------------
    # 3. Plot
    # ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 7), dpi=150)

    # Scatter pro Kennzahl in fester Reihenfolge (damit Legenden-Reihenfolge stimmt)
    for ratio in RATIOS_ORDER:
        sub = df[df["ratio"] == ratio]
        ax.scatter(
            sub["phi1"],
            sub["sigma_diff"],
            s=14,
            alpha=0.55,
            c=RATIO_COLORS[ratio],
            label=RATIO_LABELS[ratio],
            edgecolors="none",
        )

    # Quadranten-Linien (globaler Median)
    ax.axvline(phi_median_global, color="#444", linestyle="--", linewidth=1.0, alpha=0.7, zorder=0)
    ax.axhline(sigma_median_global, color="#444", linestyle="--", linewidth=1.0, alpha=0.7, zorder=0)

    # Achsen-Bereiche: phi an empirischem Bereich, sigma fest auf 0..1 gecappt
    phi_lo, phi_hi = df["phi1"].quantile(0.005), df["phi1"].quantile(0.995)
    sig_lo, sig_hi = 0.0, 1.0
    ax.set_xlim(phi_lo, phi_hi)
    ax.set_ylim(sig_lo, sig_hi)

    # Hinweis: wieviele Punkte oberhalb des sigma-Caps liegen
    above = df[df["sigma_diff"] > sig_hi]
    if len(above) > 0:
        breakdown = above["ratio"].value_counts()
        breakdown_str = ", ".join(f"{RATIO_LABELS.get(r, r)}: {n}" for r, n in breakdown.items())
        clip_note = f"Nicht dargestellt: {len(above)} Punkte mit σ(ΔY) > 1 ({breakdown_str})"
        ax.text(
            0.5, -0.14, clip_note,
            transform=ax.transAxes,
            ha="center", va="top",
            fontsize=8, color="#555", style="italic",
        )

    # Quadranten-Labels in die vier Ecken (Achsen-Koordinaten)
    label_kwargs = dict(
        fontsize=10,
        fontweight="bold",
        color="#222",
        alpha=0.85,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#999", alpha=0.8),
    )
    ax.text(0.02, 0.97, QUADRANT_LABELS["lh"], transform=ax.transAxes,
            ha="left", va="top", **label_kwargs)
    ax.text(0.98, 0.97, QUADRANT_LABELS["rh"], transform=ax.transAxes,
            ha="right", va="top", **label_kwargs)
    ax.text(0.02, 0.03, QUADRANT_LABELS["ll"], transform=ax.transAxes,
            ha="left", va="bottom", **label_kwargs)
    ax.text(0.98, 0.03, QUADRANT_LABELS["rl"], transform=ax.transAxes,
            ha="right", va="bottom", **label_kwargs)

    # Median-Beschriftung an die Linien (klein, neben der Achse)
    ax.text(phi_median_global, sig_hi * 0.995,
            f"  Median φ₁ = {phi_median_global:+.2f}",
            ha="left", va="top", fontsize=8, color="#444", alpha=0.8)
    ax.text(phi_hi * 0.995, sigma_median_global,
            f"Median σ(ΔY) = {sigma_median_global:.2f}  ",
            ha="right", va="bottom", fontsize=8, color="#444", alpha=0.8)

    # Achsen-Beschriftung
    ax.set_xlabel("φ₁  (Mean-Reversion-Koeffizient)", fontsize=11)
    ax.set_ylabel("σ(ΔY)  (Veränderungsvolatilität)", fontsize=11)
    ax.set_title(
        "Übersicht aller Unternehmen-Kennzahl-Kombinationen im φ–σ-Raum\n"
        f"(N = {len(df):,}, Quadranten-Trennlinien am globalen Median)",
        fontsize=11,
    )

    # Legende rechts neben dem Plot
    leg = ax.legend(
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        frameon=False,
        fontsize=9,
        title="Kennzahl",
        title_fontsize=10,
        markerscale=1.6,
    )
    for handle in leg.legend_handles:
        handle.set_alpha(1.0)

    # Grid (dezent)
    ax.grid(True, linestyle=":", alpha=0.35)
    ax.set_axisbelow(True)

    plt.tight_layout()

    # ---------------------------------------------------------------
    # 4. Speichern
    # ---------------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUT_DIR / "quadrant_overview_all_ratios.png"
    pdf_path = OUT_DIR / "quadrant_overview_all_ratios.pdf"
    fig.savefig(png_path, dpi=200, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    print(f"\nGespeichert: {png_path}")
    print(f"Gespeichert: {pdf_path}")


if __name__ == "__main__":
    main()
