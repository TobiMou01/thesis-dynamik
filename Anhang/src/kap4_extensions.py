"""
kap4_extensions.py
==================

Erweiterungen und Hilfsroutinen für Kapitel 4 (FF1 — Ergebnisse) der Masterarbeit
"Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen börsennotierter Unternehmen"
von Tobias Mourier, TH Wildau.

Erzeugt am 25. April 2026 in der Cowork-Session.
Reproduziert alle in dieser Sitzung gerechneten Erweiterungen und Plots, damit sie
beim Re-Run der Pipeline oder bei Datenänderungen wieder erzeugt werden können.

Inhalt
------
1. compute_halflife_tau         — E5.4 Halblebensdauer via t½ = ln(0,5)/ln(1+φ₁) (Quartale)
2. extend_summary_with_halflife — fügt hl_quarters_tau und hl_years_tau in ar_summary_by_ratio.csv ein
3. apply_bonferroni_ff2          — E6.5 Bonferroni-Korrektur (α/42) für FF2-Korrelationsmatrizen
4. apply_bonferroni_ff3          — E7.5 Bonferroni-Korrektur (α/7) für FF3-χ²-Tests
5. compute_quadrant_chi2_uniformity — χ²-Test auf Gleichverteilung der vier Quadranten pro Kennzahl
6. plot_phi1_kde                 — KDE-Histogramm der φ₁-Verteilung (7 Panels)
7. plot_sigma_kde                — KDE-Histogramm der σ(ΔY)-Verteilung (7 Panels)
8. plot_phi1_sigma_scatter       — φ₁-σ-Scatterplots mit Median-Splits (7 Panels)
9. plot_quadrant_examples        — Quadranten-Zeitreihen für vier Beispielfirmen (Walmart, Boeing, Microsoft, Amazon)

Aufruf-Beispiel
---------------
::

    from src.kap4_extensions import (
        extend_summary_with_halflife,
        apply_bonferroni_ff2,
        apply_bonferroni_ff3,
        compute_quadrant_chi2_uniformity,
        plot_phi1_kde, plot_sigma_kde,
        plot_phi1_sigma_scatter, plot_quadrant_examples,
    )

    # Tabellen-Erweiterungen
    extend_summary_with_halflife()
    apply_bonferroni_ff2()
    apply_bonferroni_ff3()
    compute_quadrant_chi2_uniformity()

    # Plots
    plot_phi1_kde()
    plot_sigma_kde()
    plot_phi1_sigma_scatter()
    plot_quadrant_examples()

Oder direkt als Skript:
    python src/kap4_extensions.py

"""

from __future__ import annotations

from itertools import combinations
from math import log
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


# ─────────────────────────────────────────────────────────────────────────
# Konfiguration
# ─────────────────────────────────────────────────────────────────────────

LAYER_COLORS = {
    "Profitabilität":   "#2C5F8D",
    "Liquidität":       "#7FB069",
    "Kapitalstruktur":  "#C75D4F",
}
RATIO_LAYER = {
    "ROA": "Profitabilität", "ROE": "Profitabilität",
    "EBIT_margin": "Profitabilität", "fcf_margin": "Profitabilität",
    "current_ratio": "Liquidität",
    "debt_to_equity": "Kapitalstruktur", "equity_ratio": "Kapitalstruktur",
}
RATIO_LABEL = {
    "ROA": "ROA", "ROE": "ROE", "EBIT_margin": "EBIT-Marge",
    "fcf_margin": "FCF-Marge", "current_ratio": "Current Ratio",
    "debt_to_equity": "Debt/Equity", "equity_ratio": "Eigenkapitalquote",
}
RATIO_ORDER = [
    "ROA", "ROE", "EBIT_margin", "fcf_margin",
    "current_ratio", "debt_to_equity", "equity_ratio",
]
QUAD_COLORS = {
    "KORREKTIV-STABIL":   "#1F77B4",
    "KORREKTIV-VOLATIL":  "#D62728",
    "PERSISTENT-STABIL":  "#2CA02C",
    "PERSISTENT-VOLATIL": "#FF7F0E",
}
QUADRANT_EXAMPLES = {
    "KORREKTIV-STABIL":   ("WMT",  "Walmart",   "Consumer Defensive"),
    "KORREKTIV-VOLATIL":  ("BA",   "Boeing",    "Industrials"),
    "PERSISTENT-STABIL":  ("MSFT", "Microsoft", "Technology"),
    "PERSISTENT-VOLATIL": ("AMZN", "Amazon",    "Consumer Cyclical"),
}

PLOT_RC = {
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.titlesize": 11, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
    "figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
}


def _ensure_paths(*paths: str | Path) -> None:
    """Stellt sicher, dass die Output-Verzeichnisse existieren."""
    for p in paths:
        Path(p).parent.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────
# 1.  E5.4 — Halblebensdauer
# ─────────────────────────────────────────────────────────────────────────

def compute_halflife_tau(phi1: float) -> float:
    """Halblebensdauer t½ = ln(0,5) / ln(1 + φ₁) in Quartalen.

    Setzt den Stollhoff/Steglich-Konventionswert für φ₁ in der Differenzen-
    Spezifikation voraus, in der (1 + φ₁) der AR-Koeffizient in der
    Levels-Parametrisierung ist.

    Parameters
    ----------
    phi1 : float
        Mean-Reversion-Koeffizient aus AR(1) auf erste Differenzen.
        Erwartet wird typischerweise φ₁ ∈ (−1, 0).

    Returns
    -------
    float
        Halblebensdauer in Quartalen, oder NaN wenn (1 + φ₁) ∉ (0, 1).
    """
    if phi1 is None or pd.isna(phi1):
        return float("nan")
    one_plus = 1.0 + phi1
    if one_plus <= 0 or one_plus >= 1:
        return float("nan")
    return log(0.5) / log(one_plus)


def extend_summary_with_halflife(
    summary_csv: str = "output/ar/ar_summary_by_ratio.csv",
) -> pd.DataFrame:
    """Fügt drei Spalten in ar_summary_by_ratio.csv ein:

    - hl_years          (= hl_median / 4, Pipeline-Konvention)
    - hl_quarters_tau   (= ln(0,5)/ln(1+φ₁_median))
    - hl_years_tau      (= hl_quarters_tau / 4)

    Die τ-Variante entspricht der in Kap. 4.1.1 verwendeten Halblebensdauer.
    """
    df = pd.read_csv(summary_csv)
    df["hl_years"] = (df["hl_median"] / 4).round(4)
    df["hl_quarters_tau"] = df["phi1_median"].apply(compute_halflife_tau).round(4)
    df["hl_years_tau"] = (df["hl_quarters_tau"] / 4).round(4)
    df.to_csv(summary_csv, index=False)
    return df


# ─────────────────────────────────────────────────────────────────────────
# 2.  E6.5 / E7.5 — Bonferroni-Korrekturen
# ─────────────────────────────────────────────────────────────────────────

ALPHA_RAW = 0.05


def apply_bonferroni_ff2(
    interdep_dir: str = "output/interdependence",
    n_total_tests: int = 21,  # Test-Familie pro Korrelationsart (φ ODER σ)
) -> dict[str, pd.DataFrame]:
    """Bonferroni-Korrektur (α/21 ≈ 0,00238) für FF2-Korrelationsmatrizen.

    Hinweis: Seit 20.05.2026 ist die Schwelle pro Test-Familie (21 Tests) statt
    über beide Familien zusammen (42 Tests). Canonical Source für die Bonferroni-
    Markierungen ist `src/interdependence.py`, das die Spearman-Korrelationen
    inklusive Bonferroni-Mirror und Bootstrap-CI in einem Lauf erzeugt. Diese
    Funktion bleibt als Convenience erhalten, um die Bonferroni-Markierung
    isoliert auf vorhandene pval_*.csv anzuwenden.

    Erzeugt vier Dateien in interdep_dir:

    - sig_bonferroni_phi1.csv : 7×7 Bool-Matrix, symmetrisch, Diagonale=False
    - sig_bonferroni_sigma.csv: gleich für σ
    - pval_phi1_long.csv      : 21 Paare mit ratio_a, ratio_b, p_value,
                                 significant_05, significant_bonferroni
    - pval_sigma_long.csv     : 21 Paare gleich für σ

    Originale pval_*.csv bleiben unverändert.
    """
    alpha_bonf = ALPHA_RAW / n_total_tests
    interdep = Path(interdep_dir)
    out: dict[str, pd.DataFrame] = {}

    for which in ("phi1", "sigma"):
        pval = pd.read_csv(interdep / f"pval_{which}.csv", index_col=0)
        ratios = list(pval.index)

        # Mirror-Matrix
        sig_mat = pd.DataFrame(False, index=ratios, columns=ratios)
        for a, b in combinations(ratios, 2):
            is_sig = pval.loc[a, b] < alpha_bonf
            sig_mat.loc[a, b] = is_sig
            sig_mat.loc[b, a] = is_sig
        sig_mat.to_csv(interdep / f"sig_bonferroni_{which}.csv")
        out[f"sig_bonferroni_{which}"] = sig_mat

        # Long-Form (obere Dreieckshälfte, 21 Paare)
        long_rows = [
            {
                "ratio_a": a,
                "ratio_b": b,
                "p_value": float(pval.loc[a, b]),
                "significant_05": float(pval.loc[a, b]) < ALPHA_RAW,
                "significant_bonferroni": float(pval.loc[a, b]) < alpha_bonf,
            }
            for a, b in combinations(ratios, 2)
        ]
        long_df = pd.DataFrame(long_rows)
        long_df.to_csv(interdep / f"pval_{which}_long.csv", index=False)
        out[f"pval_{which}_long"] = long_df
    return out


def apply_bonferroni_ff3(
    chi2_csv: str = "output/profiles/ff3_chi2_results.csv",
    n_tests: int = 7,
) -> pd.DataFrame:
    """Bonferroni-Korrektur (α/7 ≈ 0,00714) für die sieben χ²-Tests in FF3.

    Fügt Spalte significant_bonferroni in ff3_chi2_results.csv ein.
    """
    alpha_bonf = ALPHA_RAW / n_tests
    df = pd.read_csv(chi2_csv)
    df["significant_bonferroni"] = df["p_value"] < alpha_bonf
    df.to_csv(chi2_csv, index=False)
    return df


# ─────────────────────────────────────────────────────────────────────────
# 3.  χ²-Test auf Gleichverteilung der Quadranten (Methodik 3.3.3)
# ─────────────────────────────────────────────────────────────────────────

def compute_quadrant_chi2_uniformity(
    ar_features_csv: str = "output/ar/ar_features.csv",
    out_csv: str = "output/ar/quadrant_chi2_uniformity.csv",
) -> pd.DataFrame:
    """χ²-Test auf Gleichverteilung der vier Median-Split-Quadranten pro Kennzahl.

    Wären die zwei Quadrantendimensionen φ₁ und σ(ΔY) statistisch unabhängig,
    sollten die vier Quadranten nahe an n/4 Beobachtungen je Zelle liegen. Eine
    signifikante Abweichung von Gleichverteilung ist ein zweiter Beleg
    (zusätzlich zum Spearman-Test in 4.5.3) für eine Kopplung der Achsen.

    Speichert die Ergebnisse als CSV und gibt sie als DataFrame zurück.
    """
    ar = pd.read_csv(ar_features_csv)
    rows = []
    for ratio in RATIO_ORDER:
        sub = ar[ar["ratio"] == ratio][["phi1", "sigma_diff"]].dropna().copy()
        if len(sub) == 0:
            continue
        p_med = sub["phi1"].median()
        s_med = sub["sigma_diff"].median()
        sub["quad"] = sub.apply(
            lambda r: (
                ("KORREKTIV" if r["phi1"] < p_med else "PERSISTENT")
                + "-"
                + ("VOLATIL" if r["sigma_diff"] > s_med else "STABIL")
            ),
            axis=1,
        )
        counts = sub["quad"].value_counts()
        ks = int(counts.get("KORREKTIV-STABIL", 0))
        kv = int(counts.get("KORREKTIV-VOLATIL", 0))
        ps = int(counts.get("PERSISTENT-STABIL", 0))
        pv = int(counts.get("PERSISTENT-VOLATIL", 0))
        n = ks + kv + ps + pv
        chi2, p = stats.chisquare([ks, kv, ps, pv], [n / 4] * 4)
        rows.append(
            {"ratio": ratio, "n": n, "KS": ks, "KV": kv,
             "PS": ps, "PV": pv, "chi2": chi2, "p": p}
        )
    df = pd.DataFrame(rows)
    _ensure_paths(out_csv)
    df.to_csv(out_csv, index=False)
    return df


# ─────────────────────────────────────────────────────────────────────────
# 4.  Plot-Helpers
# ─────────────────────────────────────────────────────────────────────────

def _setup_rc() -> None:
    plt.rcParams.update(PLOT_RC)


def _seven_panel_grid():
    fig, axes = plt.subplots(2, 4, figsize=(15, 6.5))
    return fig, axes.flatten()


# ─────────────────────────────────────────────────────────────────────────
# 5.  Plots
# ─────────────────────────────────────────────────────────────────────────

def plot_phi1_kde(
    ar_features_csv: str = "output/ar/ar_features.csv",
    out_path: str = "output/plots/ff1_phi1_kde.png",
) -> None:
    """KDE der φ₁-Verteilung pro Kennzahl mit Histogramm-Hintergrund (Abb. 4.1b)."""
    _setup_rc()
    ar = pd.read_csv(ar_features_csv)
    fig, axes = _seven_panel_grid()
    legend_handles = [
        mpatches.Patch(color=c, alpha=0.5, label=l) for l, c in LAYER_COLORS.items()
    ]
    for i, ratio in enumerate(RATIO_ORDER):
        ax = axes[i]
        sub = ar[ar["ratio"] == ratio]["phi1"].dropna()
        layer = RATIO_LAYER[ratio]
        color = LAYER_COLORS[layer]
        ax.hist(sub, bins=40, density=True, color=color, alpha=0.35, edgecolor="none")
        kde = stats.gaussian_kde(sub)
        xx = np.linspace(sub.min(), sub.max(), 250)
        ax.plot(xx, kde(xx), color=color, lw=2)
        ax.axvline(0, color="black", ls="--", lw=0.8, alpha=0.5)
        ax.axvline(sub.median(), color=color, ls=":", lw=1.2)
        ax.text(
            0.02, 0.95,
            f"Median: {sub.median():.3f}\nn = {len(sub)}\n{layer}",
            transform=ax.transAxes, fontsize=8.5, va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="lightgray", alpha=0.85),
        )
        ax.set_title(RATIO_LABEL[ratio], fontweight="bold")
        ax.set_xlabel("φ₁")
        if i % 4 == 0:
            ax.set_ylabel("Dichte")
        ax.set_xlim(-1.0, 0.6)
    axes[7].axis("off")
    axes[7].legend(handles=legend_handles, loc="center", frameon=True,
                   fontsize=10, title="Schicht")
    fig.suptitle("Verteilung der unternehmensspezifischen φ₁-Schätzungen nach Kennzahl",
                 fontsize=13, fontweight="bold", y=1.00)
    plt.tight_layout()
    _ensure_paths(out_path)
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()


def plot_sigma_kde(
    ar_features_csv: str = "output/ar/ar_features.csv",
    out_path: str = "output/plots/ff1_sigma_kde.png",
) -> None:
    """KDE der σ(ΔY)-Verteilung pro Kennzahl, gecappt auf 99-Perzentil (Abb. 4.2b)."""
    _setup_rc()
    ar = pd.read_csv(ar_features_csv)
    fig, axes = _seven_panel_grid()
    legend_handles = [
        mpatches.Patch(color=c, alpha=0.5, label=l) for l, c in LAYER_COLORS.items()
    ]
    for i, ratio in enumerate(RATIO_ORDER):
        ax = axes[i]
        sub = ar[ar["ratio"] == ratio]["sigma_diff"].dropna()
        p99 = sub.quantile(0.99)
        sub_cap = sub[sub <= p99]
        layer = RATIO_LAYER[ratio]
        color = LAYER_COLORS[layer]
        ax.hist(sub_cap, bins=45, density=True, color=color, alpha=0.35, edgecolor="none")
        kde = stats.gaussian_kde(sub_cap)
        xx = np.linspace(sub_cap.min(), sub_cap.max(), 250)
        ax.plot(xx, kde(xx), color=color, lw=2)
        ax.axvline(sub.median(), color=color, ls=":", lw=1.2)
        ax.text(
            0.95, 0.95,
            f"Median: {sub.median():.3f}\nn = {len(sub)}\nx-Achse < p99",
            transform=ax.transAxes, fontsize=8.5, va="top", ha="right",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="lightgray", alpha=0.85),
        )
        ax.set_title(RATIO_LABEL[ratio], fontweight="bold")
        ax.set_xlabel("σ(ΔY)")
        if i % 4 == 0:
            ax.set_ylabel("Dichte")
    axes[7].axis("off")
    axes[7].legend(handles=legend_handles, loc="center", frameon=True,
                   fontsize=10, title="Schicht")
    fig.suptitle("Verteilung der unternehmensspezifischen σ(ΔY)-Schätzungen nach Kennzahl",
                 fontsize=13, fontweight="bold", y=1.00)
    plt.tight_layout()
    _ensure_paths(out_path)
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()


def plot_phi1_sigma_scatter(
    ar_features_csv: str = "output/ar/ar_features.csv",
    out_path: str = "output/plots/ff1_phi1_sigma_scatter.png",
) -> None:
    """φ₁-σ-Scatter pro Kennzahl mit Median-Splits (Abb. 4.9)."""
    _setup_rc()
    ar = pd.read_csv(ar_features_csv)
    fig, axes = plt.subplots(2, 4, figsize=(15, 7))
    axes = axes.flatten()
    legend_handles = [
        mpatches.Patch(color=c, alpha=0.6, label=q) for q, c in QUAD_COLORS.items()
    ]
    for i, ratio in enumerate(RATIO_ORDER):
        ax = axes[i]
        sub = ar[ar["ratio"] == ratio][["phi1", "sigma_diff"]].dropna().copy()
        if len(sub) == 0:
            continue
        p_med = sub["phi1"].median()
        s_med = sub["sigma_diff"].median()
        sub["quad"] = sub.apply(
            lambda r: ("KORREKTIV" if r["phi1"] < p_med else "PERSISTENT")
            + "-"
            + ("VOLATIL" if r["sigma_diff"] > s_med else "STABIL"),
            axis=1,
        )
        for q, col in QUAD_COLORS.items():
            qsub = sub[sub["quad"] == q]
            ax.scatter(qsub["phi1"], qsub["sigma_diff"], s=8, alpha=0.45,
                       color=col, edgecolor="none")
        ax.axvline(p_med, color="black", ls="--", lw=0.9, alpha=0.7)
        ax.axhline(s_med, color="black", ls="--", lw=0.9, alpha=0.7)
        ax.set_title(f"{RATIO_LABEL[ratio]} (n={len(sub)})", fontweight="bold")
        ax.set_xlabel("φ₁")
        if i % 4 == 0:
            ax.set_ylabel("σ(ΔY)")
        ax.set_ylim(0, sub["sigma_diff"].quantile(0.99))
    axes[7].axis("off")
    axes[7].legend(handles=legend_handles, loc="center", frameon=True,
                   fontsize=10, title="Quadrant")
    fig.suptitle("Verortung der Unternehmen im φ₁-σ-Raum pro Kennzahl "
                 "(gestrichelte Linien = Median-Splits)",
                 fontsize=13, fontweight="bold", y=1.00)
    plt.tight_layout()
    _ensure_paths(out_path)
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()


def plot_quadrant_examples(
    ar_features_csv: str = "output/ar/ar_features.csv",
    panel_csv: str = "output/ratios/ratio_panel.csv",
    out_path: str = "output/plots/ff1_quadrant_examples.png",
) -> None:
    """ROA-Zeitreihen für vier Beispielfirmen pro Quadrant (Abb. 4.10).

    Standardwahl: Walmart (KS), Boeing (KV), Microsoft (PS), Amazon (PV).
    """
    _setup_rc()
    ar = pd.read_csv(ar_features_csv)
    panel = pd.read_csv(panel_csv)

    fig, axes = plt.subplots(2, 2, figsize=(13, 7))
    for ax, (quad, (ticker, name, sector)) in zip(axes.flatten(),
                                                    QUADRANT_EXAMPLES.items()):
        sub = panel[panel["ticker"] == ticker].sort_values("quarter").copy()
        if len(sub) == 0:
            ax.text(0.5, 0.5, f"{ticker} nicht im Panel",
                    ha="center", va="center", transform=ax.transAxes)
            continue
        sub["quarter"] = pd.to_datetime(sub["quarter"], errors="coerce")
        roa = sub["ROA"].dropna()
        if len(roa) == 0:
            continue
        roa_z = (sub["ROA"] - sub["ROA"].mean()) / sub["ROA"].std()
        color = QUAD_COLORS[quad]
        ax.plot(sub["quarter"], roa_z, color=color, lw=1.4)
        arrow = ar[(ar["ticker"] == ticker) & (ar["ratio"] == "ROA")]
        phi1_val = arrow["phi1"].iloc[0] if len(arrow) > 0 else np.nan
        sigma_val = arrow["sigma_diff"].iloc[0] if len(arrow) > 0 else np.nan
        ax.axhline(0, color="black", ls="--", lw=0.7, alpha=0.5)
        ax.axhspan(-1, 1, alpha=0.06, color=color)
        ax.set_title(
            f"{name} ({ticker}) — {quad}\n"
            f"ROA-φ₁ = {phi1_val:.2f}, σ(ΔROA) = {sigma_val:.3f}",
            fontweight="bold", fontsize=10.5,
        )
        ax.set_xlabel("Quartal")
        ax.set_ylabel("ROA (z-Score)")
        ax.set_ylim(-3.5, 3.5)
        ax.text(
            0.01, 0.97, sector, transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="lightgray", alpha=0.8),
        )
    fig.suptitle("Beispielhafte ROA-Zeitreihen für die vier Quadranten "
                 "(z-standardisiert, 2000Q1–2024Q4)",
                 fontsize=13, fontweight="bold", y=1.00)
    plt.tight_layout()
    _ensure_paths(out_path)
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────
# 6.  Skript-Modus: alle Erweiterungen in einem Aufruf
# ─────────────────────────────────────────────────────────────────────────

def run_all() -> None:
    """Alle Erweiterungen und Plots in einem Aufruf."""
    print("[1/8] E5.4 — Halblebensdauer-Spalten in ar_summary_by_ratio.csv ...")
    extend_summary_with_halflife()

    print("[2/8] E6.5 — Bonferroni FF2 (α/42) ...")
    apply_bonferroni_ff2()

    print("[3/8] E7.5 — Bonferroni FF3 (α/7) ...")
    apply_bonferroni_ff3()

    print("[4/8] χ²-Test auf Quadranten-Gleichverteilung ...")
    compute_quadrant_chi2_uniformity()

    print("[5/8] Plot Abb. 4.1b — KDE φ₁-Verteilung ...")
    plot_phi1_kde()

    print("[6/8] Plot Abb. 4.2b — KDE σ(ΔY)-Verteilung ...")
    plot_sigma_kde()

    print("[7/8] Plot Abb. 4.9 — φ₁-σ-Scatter mit Median-Splits ...")
    plot_phi1_sigma_scatter()

    print("[8/8] Plot Abb. 4.10 — Quadranten-Zeitreihen-Beispiele ...")
    plot_quadrant_examples()

    print("\nFertig — alle Erweiterungen für Kapitel 4 erzeugt.")


if __name__ == "__main__":
    run_all()
