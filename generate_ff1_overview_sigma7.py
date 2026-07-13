#!/usr/bin/env python3
"""
FF1 Big-Picture Jointplot — VARIANTE mit 7 Volatilitaets-Boxplots pro Kennzahl.

Identisch zur Original-Grafik (Notebook kap4_FF1.ipynb, Zelle 3 ->
output/plots/ff1_overview_jointplot_log.png): gleicher Scatter (3 Schichten),
gleicher oberer phi1-Boxplot (3 Schichten). EINZIGER Unterschied: Der rechte
sigma(dY)-Marginal zeigt statt 3 Schicht-Boxplots jetzt 7 Boxplots — einen pro
Kennzahl (nach Schicht eingefaerbt), um zu zeigen, dass Volatilitaet primaer
INNERHALB einer Kennzahl ueber Unternehmen vergleichbar ist.

Erzeugt eine NEUE Datei, die alte bleibt unangetastet.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter

# ── Pfade ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
AR_FEATURES = ROOT / "output" / "ar" / "ar_features.csv"
OUT_PNG = ROOT / "output" / "plots" / "ff1_overview_jointplot_log_sigma_pro_kennzahl.png"

# ── Konstanten (identisch zu analysis_helpers / Notebook-Setup) ──────────
RATIO_ORDER = ["ROA", "ROE", "EBIT_margin", "fcf_margin",
               "current_ratio", "debt_to_equity", "equity_ratio"]
RATIO_LAYER = {
    "ROA": "Profitabilität", "ROE": "Profitabilität",
    "EBIT_margin": "Profitabilität", "fcf_margin": "Profitabilität",
    "current_ratio": "Liquidität",
    "debt_to_equity": "Kapitalstruktur", "equity_ratio": "Kapitalstruktur",
}
# Kurzlabels fuer den schmalen rechten Panel
RATIO_SHORT = {
    "ROA": "ROA", "ROE": "ROE", "EBIT_margin": "EBIT", "fcf_margin": "FCF",
    "current_ratio": "CR", "debt_to_equity": "D/E", "equity_ratio": "EK-Q",
}
LAYER_COLORS = {"Profitabilität": "#2C5F8D", "Liquidität": "#7FB069",
                "Kapitalstruktur": "#C75D4F"}
LAYER_ORDER_BP = ["Profitabilität", "Liquidität", "Kapitalstruktur"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.titlesize": 11, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
    "figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
})

# ── Daten ────────────────────────────────────────────────────────────────
ar_bp = pd.read_csv(AR_FEATURES).dropna(subset=["phi1", "sigma_diff"])
ar_bp = ar_bp[ar_bp["sigma_diff"] > 0]
ar_bp["layer"] = ar_bp["ratio"].map(RATIO_LAYER)

phi1_med_bp = ar_bp.loc[ar_bp["layer"].notna(), "phi1"].median()
sigma_med_bp = ar_bp.loc[ar_bp["layer"].notna(), "sigma_diff"].median()
phi_lo, phi_hi = ar_bp.loc[ar_bp["layer"].notna(), "phi1"].quantile([0.005, 0.995])
sig_lo = ar_bp.loc[ar_bp["layer"].notna(), "sigma_diff"].quantile(0.01)
sig_hi = ar_bp.loc[ar_bp["layer"].notna(), "sigma_diff"].quantile(0.99)

# ── Figure/Layout (identisch zum Original) ───────────────────────────────
fig = plt.figure(figsize=(11, 8.5))
gs = GridSpec(2, 2, width_ratios=[5, 1], height_ratios=[1, 5],
              hspace=0.05, wspace=0.05)
ax_main = fig.add_subplot(gs[1, 0])
ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)
ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)

# ── Haupt-Scatter (unveraendert: 3 Schichten) ────────────────────────────
for layer in LAYER_ORDER_BP:
    sub = ar_bp[ar_bp["layer"] == layer]
    ax_main.scatter(sub["phi1"], sub["sigma_diff"],
                    c=LAYER_COLORS[layer], alpha=0.35, s=12,
                    edgecolors="none", label=f"{layer} (n={len(sub)})")

ax_main.axvline(phi1_med_bp, color="#444", linewidth=0.9, linestyle="--", alpha=0.7)
ax_main.axhline(sigma_med_bp, color="#444", linewidth=0.9, linestyle="--", alpha=0.7)
ax_main.set_xlabel("phi1 (Mean-Reversion-Stärke)")
ax_main.set_ylabel("sigma(delta Y) — log-skaliert")
ax_main.set_xlim(phi_lo, phi_hi)
ax_main.set_yscale("log")
ax_main.set_ylim(sig_lo, sig_hi)
ax_main.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}"))
ax_main.minorticks_off()
ax_main.legend(loc="lower left", framealpha=0.92)

# ── Oberer Marginal-Boxplot (unveraendert: 3 Schichten, phi1) ────────────
top_data = [ar_bp[ar_bp["layer"] == l]["phi1"].values for l in LAYER_ORDER_BP]
top_colors = [LAYER_COLORS[l] for l in LAYER_ORDER_BP]
bp_top = ax_top.boxplot(top_data, vert=False, widths=0.55, patch_artist=True,
                        positions=range(len(LAYER_ORDER_BP)), showfliers=False,
                        medianprops=dict(color="black", linewidth=1.4))
for patch, c in zip(bp_top["boxes"], top_colors):
    patch.set_facecolor(c); patch.set_alpha(0.7)
ax_top.set_yticks(range(len(LAYER_ORDER_BP)))
ax_top.set_yticklabels(LAYER_ORDER_BP, fontsize=8)
ax_top.tick_params(axis="x", labelbottom=False)
ax_top.spines["bottom"].set_visible(False)
ax_top.set_xlim(phi_lo, phi_hi)
ax_top.axvline(phi1_med_bp, color="#444", linewidth=0.9, linestyle="--", alpha=0.7)

# ── Rechter Marginal-Boxplot — NEU: 7 Kennzahlen statt 3 Schichten ───────
right_data = [ar_bp[ar_bp["ratio"] == r]["sigma_diff"].values for r in RATIO_ORDER]
right_colors = [LAYER_COLORS[RATIO_LAYER[r]] for r in RATIO_ORDER]
bp_right = ax_right.boxplot(right_data, vert=True, widths=0.6, patch_artist=True,
                            positions=range(len(RATIO_ORDER)), showfliers=False,
                            medianprops=dict(color="black", linewidth=1.4))
for patch, c in zip(bp_right["boxes"], right_colors):
    patch.set_facecolor(c); patch.set_alpha(0.7)
ax_right.set_xticks(range(len(RATIO_ORDER)))
ax_right.set_xticklabels([RATIO_SHORT[r] for r in RATIO_ORDER],
                         fontsize=8, rotation=45, ha="right")
ax_right.tick_params(axis="y", labelleft=False)
ax_right.spines["left"].set_visible(False)
ax_right.set_yscale("log")
ax_right.set_ylim(sig_lo, sig_hi)
ax_right.minorticks_off()
ax_right.axhline(sigma_med_bp, color="#444", linewidth=0.9, linestyle="--", alpha=0.7)

fig.suptitle("Big-Picture FF1: Mean-Reversion x Volatilität — drei Schichten + vier Quadranten",
             fontsize=12, y=0.97)

OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT_PNG)
print("gespeichert:", OUT_PNG)

# ── Referenz: Median-Volatilitaet pro Kennzahl ───────────────────────────
print("\nMedian sigma(dY) pro Kennzahl:")
for r in RATIO_ORDER:
    vals = ar_bp[ar_bp["ratio"] == r]["sigma_diff"]
    print(f"  {RATIO_SHORT[r]:5s} ({RATIO_LAYER[r]:15s}) n={len(vals):3d}  median={vals.median():.4f}")
