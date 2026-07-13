"""
check_aggregate_drift.py
=========================

Prueft pro Hauptkennzahl, ob der ueber alle Unternehmen aggregierte Median
einen systematischen Trend ueber die 100 Quartale aufweist.

Anders als der c-Wert pro Unternehmen aus dem AR(1)-Modell (der sich beim
Mitteln ueber Unternehmen rausmittelt), kann der Aggregat-Median pro Quartal
einen Trend zeigen, wenn z. B. die ganze Stichprobe in eine Richtung driftet.

Output:
  - aggregat_drift_pro_kennzahl.png  (Liniendiagramm pro Kennzahl, 7 Subplots)
  - aggregat_drift_summary.csv       (linearer Trend pro Kennzahl)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent
OUT_DIR = PROJECT_ROOT / "output" / "ar"

# ---------------------------------------------------------------
# Daten
# ---------------------------------------------------------------
panel = pd.read_csv(PROJECT_ROOT / "output" / "ratios" / "ratio_panel.csv")
panel["quarter"] = pd.PeriodIndex(panel["quarter"], freq="Q")

RATIOS = [
    "ROA", "ROE", "EBIT_margin", "fcf_margin",
    "current_ratio", "debt_to_equity", "equity_ratio",
]
RATIO_LABELS = {
    "ROA": "ROA", "ROE": "ROE",
    "EBIT_margin": "EBIT-Marge", "fcf_margin": "FCF-Marge",
    "current_ratio": "Current Ratio",
    "debt_to_equity": "Debt/Equity", "equity_ratio": "Eigenkapitalquote",
}
LAYER_COLORS = {
    "ROA": "#08306b", "ROE": "#2c7fb8",
    "EBIT_margin": "#6a51a3", "fcf_margin": "#00bcd4",
    "current_ratio": "#2ca02c",
    "debt_to_equity": "#d62728", "equity_ratio": "#ff7f0e",
}

# ---------------------------------------------------------------
# Aggregat-Mediane pro Quartal pro Kennzahl
# ---------------------------------------------------------------
trend_rows = []
medians_per_quarter = {}

for ratio in RATIOS:
    if ratio not in panel.columns:
        print(f"WARNUNG: {ratio} nicht im Panel")
        continue
    sub = panel[["quarter", ratio]].dropna()
    medians = sub.groupby("quarter")[ratio].median().sort_index()
    means = sub.groupby("quarter")[ratio].mean().sort_index()
    medians_per_quarter[ratio] = medians

    # Linearer Trend ueber die Quartals-Mediane
    x = np.arange(len(medians))
    slope, intercept, r_val, p_val, se = stats.linregress(x, medians.values)

    # Veraenderung von erstem zu letztem Quartal nach Trendlinie
    delta_total = slope * (len(medians) - 1)
    median_start = medians.iloc[0]
    median_end = medians.iloc[-1]

    trend_rows.append({
        "ratio": ratio,
        "n_quartale": len(medians),
        "median_2000Q1": float(median_start),
        "median_2024Q4": float(median_end),
        "delta_total": float(median_end - median_start),
        "slope_pro_quartal": float(slope),
        "delta_aus_trend_25j": float(delta_total),
        "r_squared_trend": float(r_val ** 2),
        "p_trend": float(p_val),
    })
    print(f"{RATIO_LABELS[ratio]:20s}  Median 2000Q1: {median_start:+.4f}  ->  2024Q4: {median_end:+.4f}  "
          f"|  Trend-Slope: {slope:+.5f}/Q  R²={r_val**2:.3f}  p={p_val:.4f}")

trend_df = pd.DataFrame(trend_rows)
trend_csv = OUT_DIR / "aggregat_drift_summary.csv"
trend_df.to_csv(trend_csv, index=False)
print(f"\nGespeichert: {trend_csv}")

# ---------------------------------------------------------------
# Plot: 7 Subplots, eines pro Kennzahl
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes_flat = axes.flatten()

for i, ratio in enumerate(RATIOS):
    ax = axes_flat[i]
    medians = medians_per_quarter[ratio]
    color = LAYER_COLORS[ratio]
    ax.plot(medians.index.to_timestamp(), medians.values,
            color=color, linewidth=1.4, alpha=0.85, label="Median pro Quartal")

    # Trendlinie
    x = np.arange(len(medians))
    slope, intercept, *_ = stats.linregress(x, medians.values)
    trend_line = intercept + slope * x
    ax.plot(medians.index.to_timestamp(), trend_line,
            color="black", linewidth=1.2, linestyle="--", alpha=0.7,
            label=f"Trend: {slope:+.5f}/Q")

    ax.set_title(RATIO_LABELS[ratio], fontsize=10, fontweight="bold")
    ax.set_xlabel("Quartal", fontsize=9)
    ax.set_ylabel(RATIO_LABELS[ratio], fontsize=9)
    ax.grid(True, linestyle=":", alpha=0.35)
    ax.legend(loc="best", fontsize=7, frameon=False)
    ax.tick_params(axis="x", labelrotation=30, labelsize=7)
    ax.tick_params(axis="y", labelsize=8)

# Letzten Subplot ausblenden (8 Slots fuer 7 Kennzahlen)
axes_flat[7].axis("off")

fig.suptitle("Aggregat-Median pro Quartal je Kennzahl (2000 Q1 – 2024 Q4) mit linearem Trend",
             fontsize=12, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.96])

out_png = OUT_DIR / "aggregat_drift_pro_kennzahl.png"
out_pdf = OUT_DIR / "aggregat_drift_pro_kennzahl.pdf"
fig.savefig(out_png, dpi=200, bbox_inches="tight")
fig.savefig(out_pdf, bbox_inches="tight")
print(f"Gespeichert: {out_png}")
print(f"Gespeichert: {out_pdf}")
