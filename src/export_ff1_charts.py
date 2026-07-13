"""
export_ff1_charts.py – Exportiert FF1-relevante Charts als PNG
===============================================================
Erzeugt statische Versionen der interaktiven Notebook-Plots.
Aufruf: python src/export_ff1_charts.py
Output: output/plots/ff1_*.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns

# ── Pfade ──
PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
from config import RATIO_NAMES, OUT_AR, OUT_CLUSTER, OUT_PLOTS, OUT_EXTVAL, ensure_output_dirs

ensure_output_dirs()

# ── Daten laden ──
af = pd.read_csv(OUT_AR / "ar_features.csv")
qa = pd.read_csv(OUT_CLUSTER / "quadrant_assignments.csv")
vf = pd.read_csv(OUT_EXTVAL / "validation_features.csv")

sector_map = vf[["ticker", "sector"]].drop_duplicates()
af = af.merge(sector_map, on="ticker", how="left")
qa = qa.merge(sector_map, on="ticker", how="left")

RATIO_ORDER = ["ROA", "ROE", "EBIT_margin", "fcf_margin",
               "current_ratio", "debt_to_equity", "equity_ratio"]
RATIO_LABELS = {
    "ROA": "ROA", "ROE": "ROE", "EBIT_margin": "EBIT-Marge",
    "fcf_margin": "FCF-Marge", "current_ratio": "Current Ratio",
    "debt_to_equity": "Debt/Equity", "equity_ratio": "EK-Quote",
}

# Einheitliches Styling
plt.rcParams.update({
    "figure.dpi": 200,
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
})
COLOR_PROF = "#2171B5"
COLOR_LIQ = "#6BAED6"
COLOR_CAP = "#BDD7E7"
RATIO_COLORS = {
    "ROA": COLOR_PROF, "ROE": COLOR_PROF, "EBIT_margin": COLOR_PROF,
    "fcf_margin": COLOR_PROF, "current_ratio": COLOR_LIQ,
    "debt_to_equity": COLOR_CAP, "equity_ratio": COLOR_CAP,
}


def save(fig, name):
    path = OUT_PLOTS / f"ff1_{name}.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {path.name}")


# ══════════════════════════════════════════════
# 1. φ₁-Boxplots pro Kennzahl
# ══════════════════════════════════════════════
print("1. φ₁-Boxplots …")
fig, ax = plt.subplots(figsize=(8, 4))
data = [af[af["ratio"] == r]["phi1"].dropna() for r in RATIO_ORDER]
bp = ax.boxplot(data, vert=True, patch_artist=True, widths=0.6,
                medianprops=dict(color="black", linewidth=1.5))
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(RATIO_COLORS[RATIO_ORDER[i]])
    patch.set_alpha(0.8)
ax.set_xticklabels([RATIO_LABELS[r] for r in RATIO_ORDER], rotation=30, ha="right")
ax.set_ylabel("φ₁ (AR-Koeffizient auf ΔY)")
ax.axhline(0, color="gray", linewidth=0.5, linestyle="--")
ax.set_title("Mean-Reversion-Stärke pro Kennzahl (φ₁ auf Differenzen)")
fig.tight_layout()
save(fig, "phi1_boxplots")


# ══════════════════════════════════════════════
# 2. σ(ΔY)-Boxplots pro Kennzahl (log-Skala)
# ══════════════════════════════════════════════
print("2. σ(ΔY)-Boxplots …")
fig, ax = plt.subplots(figsize=(8, 4))
data = [af[af["ratio"] == r]["sigma_diff"].dropna() for r in RATIO_ORDER]
bp = ax.boxplot(data, vert=True, patch_artist=True, widths=0.6,
                medianprops=dict(color="black", linewidth=1.5))
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(RATIO_COLORS[RATIO_ORDER[i]])
    patch.set_alpha(0.8)
ax.set_xticklabels([RATIO_LABELS[r] for r in RATIO_ORDER], rotation=30, ha="right")
ax.set_ylabel("σ(ΔY) – Änderungsvolatilität")
ax.set_yscale("log")
ax.set_title("Änderungsvolatilität pro Kennzahl (σ der Differenzen)")
fig.tight_layout()
save(fig, "sigma_boxplots")


# ══════════════════════════════════════════════
# 3. Quadranten-Scatter pro Kennzahl (2×4 Grid)
# ══════════════════════════════════════════════
print("3. Quadranten-Scatter …")
QUAD_COLORS = {
    "KORREKTIV-STABIL": "#2CA02C", "KORREKTIV-VOLATIL": "#D62728",
    "PERSISTENT-STABIL": "#1F77B4", "PERSISTENT-VOLATIL": "#FF7F0E",
}
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes_flat = axes.flatten()
for i, ratio in enumerate(RATIO_ORDER):
    ax = axes_flat[i]
    sub = qa[qa["ratio"] == ratio]
    for quad, color in QUAD_COLORS.items():
        mask = sub["quadrant"] == quad
        ax.scatter(sub.loc[mask, "phi1"], sub.loc[mask, "sigma_diff"],
                   c=color, alpha=0.3, s=8, label=quad, edgecolors="none")
    phi_med = sub["phi1"].median()
    sig_med = sub["sigma_diff"].median()
    ax.axvline(phi_med, color="gray", linewidth=0.5, linestyle="--")
    ax.axhline(sig_med, color="gray", linewidth=0.5, linestyle="--")
    ax.set_title(RATIO_LABELS[ratio], fontsize=10)
    ax.set_xlabel("φ₁")
    ax.set_ylabel("σ(ΔY)")
# Hide 8th subplot
axes_flat[7].axis("off")
axes_flat[7].legend(*axes_flat[0].get_legend_handles_labels(),
                     loc="center", fontsize=9, markerscale=3)
fig.suptitle("Quadranten-Scatter: φ₁ × σ(ΔY) pro Kennzahl", fontsize=13, y=1.01)
fig.tight_layout()
save(fig, "quadrant_scatter")


# ══════════════════════════════════════════════
# 4. Signifikanzrate + R² pro Kennzahl
# ══════════════════════════════════════════════
print("4. Signifikanz & R² …")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

signif = [(af[af["ratio"] == r]["phi1_pval"] < 0.05).mean() * 100 for r in RATIO_ORDER]
bars = ax1.bar(range(len(RATIO_ORDER)), signif,
               color=[RATIO_COLORS[r] for r in RATIO_ORDER], alpha=0.8)
ax1.set_xticks(range(len(RATIO_ORDER)))
ax1.set_xticklabels([RATIO_LABELS[r] for r in RATIO_ORDER], rotation=30, ha="right")
ax1.set_ylabel("Anteil signifikant (%)")
ax1.set_title("Signifikanzrate (p < 0,05)")
ax1.set_ylim(0, 105)
for bar, val in zip(bars, signif):
    ax1.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.0f}%",
             ha="center", va="bottom", fontsize=8)

r2_med = [af[af["ratio"] == r]["r_squared"].median() for r in RATIO_ORDER]
bars2 = ax2.bar(range(len(RATIO_ORDER)), r2_med,
                color=[RATIO_COLORS[r] for r in RATIO_ORDER], alpha=0.8)
ax2.set_xticks(range(len(RATIO_ORDER)))
ax2.set_xticklabels([RATIO_LABELS[r] for r in RATIO_ORDER], rotation=30, ha="right")
ax2.set_ylabel("R² (Median)")
ax2.set_title("Erklärungskraft des AR(1)-Modells")
for bar, val in zip(bars2, r2_med):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.003, f"{val:.3f}",
             ha="center", va="bottom", fontsize=8)
fig.tight_layout()
save(fig, "signif_r2")


# ══════════════════════════════════════════════
# 5. Heatmap: φ₁ (Median) pro Sektor × Kennzahl
# ══════════════════════════════════════════════
print("5. Sektor-Heatmap φ₁ …")
sectors_ordered = af.groupby("sector")["ticker"].nunique().sort_values(ascending=False)
sectors_ordered = sectors_ordered[sectors_ordered >= 10].index.tolist()

pivot = af[af["sector"].isin(sectors_ordered)].pivot_table(
    index="sector", columns="ratio", values="phi1", aggfunc="median"
)
pivot = pivot.reindex(index=sectors_ordered, columns=RATIO_ORDER)

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="RdBu", center=0,
            vmin=-0.55, vmax=0.05, linewidths=0.5, ax=ax,
            xticklabels=[RATIO_LABELS[r] for r in RATIO_ORDER],
            cbar_kws={"label": "φ₁ (Median)"})
ax.set_title("Mean-Reversion-Stärke: Sektor × Kennzahl")
ax.set_ylabel("")
fig.tight_layout()
save(fig, "heatmap_phi1_sector")


# ══════════════════════════════════════════════
# 6. Heatmap: σ(ΔY) (Median) pro Sektor × Kennzahl
# ══════════════════════════════════════════════
print("6. Sektor-Heatmap σ …")
pivot_sig = af[af["sector"].isin(sectors_ordered)].pivot_table(
    index="sector", columns="ratio", values="sigma_diff", aggfunc="median"
)
pivot_sig = pivot_sig.reindex(index=sectors_ordered, columns=RATIO_ORDER)

# Log-transform for better color differentiation
pivot_log = np.log10(pivot_sig)

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(pivot_log, annot=pivot_sig.round(3).values, fmt="",
            cmap="YlOrRd", linewidths=0.5, ax=ax,
            xticklabels=[RATIO_LABELS[r] for r in RATIO_ORDER],
            cbar_kws={"label": "log₁₀ σ(ΔY)"})
ax.set_title("Änderungsvolatilität: Sektor × Kennzahl (Annotation = Rohwert)")
ax.set_ylabel("")
fig.tight_layout()
save(fig, "heatmap_sigma_sector")


# ══════════════════════════════════════════════
# 7. Heatmap: Signifikanzrate pro Sektor × Kennzahl
# ══════════════════════════════════════════════
print("7. Sektor-Heatmap Signifikanz …")
af["signif"] = (af["phi1_pval"] < 0.05).astype(int)
pivot_s = af[af["sector"].isin(sectors_ordered)].pivot_table(
    index="sector", columns="ratio", values="signif", aggfunc="mean"
) * 100
pivot_s = pivot_s.reindex(index=sectors_ordered, columns=RATIO_ORDER)

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(pivot_s, annot=True, fmt=".0f", cmap="Greens",
            vmin=0, vmax=100, linewidths=0.5, ax=ax,
            xticklabels=[RATIO_LABELS[r] for r in RATIO_ORDER],
            cbar_kws={"label": "% signifikant (p < 0,05)"})
ax.set_title("Signifikanzrate: Sektor × Kennzahl")
ax.set_ylabel("")
fig.tight_layout()
save(fig, "heatmap_signif_sector")


# ══════════════════════════════════════════════
# 8. Quadrantenverteilung pro Sektor (Stacked Bar)
# ══════════════════════════════════════════════
print("8. Quadrantenverteilung pro Sektor …")
prof_ratios = ["ROA", "ROE", "EBIT_margin", "fcf_margin"]
qa_prof = qa[qa["ratio"].isin(prof_ratios) & qa["sector"].isin(sectors_ordered)]

cross = pd.crosstab(qa_prof["sector"], qa_prof["quadrant"], normalize="index") * 100
quad_order = ["KORREKTIV-STABIL", "KORREKTIV-VOLATIL", "PERSISTENT-STABIL", "PERSISTENT-VOLATIL"]
cross = cross.reindex(columns=quad_order, fill_value=0)
cross = cross.reindex(index=sectors_ordered)

fig, ax = plt.subplots(figsize=(10, 5))
cross.plot(kind="barh", stacked=True, ax=ax,
           color=[QUAD_COLORS[q] for q in quad_order], alpha=0.85)
ax.set_xlabel("Anteil (%)")
ax.set_title("Quadrantenverteilung pro Sektor (Profitabilitätskennzahlen)")
ax.legend(title="Quadrant", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
ax.set_xlim(0, 100)
fig.tight_layout()
save(fig, "quadrant_sector_bars")


print(f"\nFertig – {len(list(OUT_PLOTS.glob('ff1_*.png')))} Charts exportiert nach {OUT_PLOTS}")
