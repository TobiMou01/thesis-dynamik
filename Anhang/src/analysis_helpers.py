"""
analysis_helpers.py — Daten-Helper für die Notebook-Analyse-Layer
==================================================================

Reine Daten-Loader und Aggregations-Funktionen. KEINE Plot-Erzeugung —
Plots werden direkt in den Notebooks geschrieben, damit die Visualisierungs-
Logik beim Lesen des Notebooks sichtbar ist.

Aufbau:
  A. Low-Level Loader        — laden CSVs aus output/ als pandas DataFrames
  B. Mid-Level Aggregationen — Sektor-Pivots, Quadranten-Berechnung,
                               Deskriptivstatistik, Signifikanzraten
  C. Stats-Funktionen        — Halblebensdauer (τ-Formel), Bonferroni-Schwelle,
                               χ²-Test auf Quadranten-Gleichverteilung

Konvention für Notebook-Nutzung:
  >>> from src.analysis_helpers import load_ar_features, compute_sector_pivot
  >>> ar = load_ar_features()
  >>> pivot_phi1 = compute_sector_pivot(ar, "phi1", agg="median")
  >>> pivot_phi1  # Jupyter rendert als Tabelle

Alle CSV-Pfade relativ zum PROJECT_ROOT in config.py.
"""

from __future__ import annotations

from itertools import combinations
from math import log
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from scipy import stats

try:
    from .config import PROJECT_ROOT, RATIO_NAMES, RATIOS
except ImportError:
    from config import PROJECT_ROOT, RATIO_NAMES, RATIOS  # type: ignore


# ─────────────────────────────────────────────
# Anzeigereihenfolge & Labels
# ─────────────────────────────────────────────
RATIO_ORDER = [
    "ROA", "ROE", "EBIT_margin", "fcf_margin",
    "current_ratio", "debt_to_equity", "equity_ratio",
]
RATIO_LABEL = {
    "ROA": "ROA", "ROE": "ROE", "EBIT_margin": "EBIT-Marge",
    "fcf_margin": "FCF-Marge", "current_ratio": "Current Ratio",
    "debt_to_equity": "Debt/Equity", "equity_ratio": "Eigenkapitalquote",
}
RATIO_LAYER = {
    "ROA": "Profitabilität", "ROE": "Profitabilität",
    "EBIT_margin": "Profitabilität", "fcf_margin": "Profitabilität",
    "current_ratio": "Liquidität",
    "debt_to_equity": "Kapitalstruktur", "equity_ratio": "Kapitalstruktur",
}
SECTOR_ORDER = [
    "Industrials", "Consumer Cyclical", "Technology", "Healthcare",
    "Utilities", "Consumer Defensive", "Basic Materials",
    "Real Estate", "Energy", "Communication Services",
]


# ═════════════════════════════════════════════
# A. Low-Level Loader
# ═════════════════════════════════════════════

def _csv(rel: str) -> Path:
    """Pfad-Helfer relativ zum PROJECT_ROOT."""
    return PROJECT_ROOT / rel


def load_ar_features(model: str = "diff1") -> pd.DataFrame:
    """AR-Schätzungen pro Ticker × Kennzahl (alle 6.521 Schätzungen).

    Args:
        model: 'diff1' (Hauptmodell) oder 'all' für alle 4 Modellvarianten.

    Returns:
        DataFrame mit Spalten ticker, ratio, phi1, phi1_se, phi1_pval,
        c, r_squared, sigma_diff, n_obs, half_life [, model].
    """
    if model == "diff1":
        return pd.read_csv(_csv("output/ar/ar_features.csv"))
    elif model == "all":
        return pd.read_csv(_csv("output/ar/ar_features_all.csv"))
    else:
        df = pd.read_csv(_csv("output/ar/ar_features_all.csv"))
        return df[df["model"] == model].copy()


def load_ar_summary() -> pd.DataFrame:
    """Aggregierte AR-Statistik pro Kennzahl (Tab. 4.1-Quelle)."""
    return pd.read_csv(_csv("output/ar/ar_summary_by_ratio.csv"))


def load_ar_summary_multimodel() -> pd.DataFrame:
    """Aggregierte AR-Statistik pro Kennzahl × Modellvariante (Tab. 4.5-Quelle)."""
    return pd.read_csv(_csv("output/ar/ar_summary_by_model_ratio.csv"))


def load_ratio_panel() -> pd.DataFrame:
    """Aufbereitetes Kennzahl-Panel (932 Ticker × 100 Quartale × 7 Ratios)."""
    return pd.read_csv(_csv("output/ratios/ratio_panel.csv"))


def load_company_profiles() -> pd.DataFrame:
    """Quadranten-Profile pro Unternehmen mit Sektor-Info."""
    return pd.read_csv(_csv("output/profiles/company_quadrant_profiles.csv"))


def load_phi1_sigma_correlation() -> pd.DataFrame:
    """Spearman-Korrelation φ₁ × σ pro Kennzahl (Tab. 4.7-Quelle)."""
    return pd.read_csv(_csv("output/ar/phi1_sigma_correlation.csv"))


def load_corr_matrix(which: str = "phi1") -> pd.DataFrame:
    """7×7 Korrelationsmatrix (für FF2).

    Args:
        which: 'phi1' oder 'sigma'.
    """
    assert which in ("phi1", "sigma")
    return pd.read_csv(_csv(f"output/interdependence/corr_{which}.csv"), index_col=0)


def load_pval_matrix(which: str = "phi1") -> pd.DataFrame:
    """7×7 p-Wert-Matrix (für FF2)."""
    assert which in ("phi1", "sigma")
    return pd.read_csv(_csv(f"output/interdependence/pval_{which}.csv"), index_col=0)


def load_pval_long(which: str = "phi1") -> pd.DataFrame:
    """Long-Form mit Bonferroni-Markierung (21 Paare pro which)."""
    assert which in ("phi1", "sigma")
    return pd.read_csv(_csv(f"output/interdependence/pval_{which}_long.csv"))


def load_sample_comparison() -> pd.DataFrame:
    """Stichprobenrobustheit (Tab. 4.6-Quelle)."""
    return pd.read_csv(_csv("output/robustness/sample_comparison.csv"))


def load_ff3_chi2() -> pd.DataFrame:
    """FF3 χ²-Tests Sektor × Quadrant (Tab. 6.3-Quelle in FF3)."""
    return pd.read_csv(_csv("output/profiles/ff3_chi2_results.csv"))


def load_ff3_size_effects() -> pd.DataFrame:
    """FF3 Größeneffekte (Spearman) — Tab. 6.4-Quelle in FF3."""
    return pd.read_csv(_csv("output/profiles/ff3_size_effects.csv"))


def load_kmeans_labels() -> pd.DataFrame:
    """K-Means Cluster-Zuordnung pro Ticker."""
    return pd.read_csv(_csv("output/clustering/kmeans_ar_dynamics_labels.csv"))


# ═════════════════════════════════════════════
# B. Mid-Level Aggregationen
# ═════════════════════════════════════════════

def attach_sector(ar: pd.DataFrame) -> pd.DataFrame:
    """Merged AR-Features mit Sektor-Info aus company_quadrant_profiles."""
    profiles = load_company_profiles()[["ticker", "sector", "industry",
                                          "market_cap", "employees"]]
    return ar.merge(profiles, on="ticker", how="left")


def compute_sector_pivot(
    ar: pd.DataFrame,
    value_col: str = "phi1",
    agg: str = "median",
) -> pd.DataFrame:
    """Pivot Sektor × Kennzahl mit gewählter Aggregation.

    Args:
        ar: AR-Features mit Sektor-Spalte (vorher attach_sector aufrufen).
        value_col: 'phi1', 'sigma_diff', 'r_squared', 'phi1_pval' etc.
        agg: 'median', 'mean', 'std' — oder Callable.

    Returns:
        DataFrame mit Sektoren als Zeilen, Kennzahlen als Spalten.
        Zeilen sortiert nach SECTOR_ORDER, Spalten nach RATIO_ORDER.
    """
    if "sector" not in ar.columns:
        ar = attach_sector(ar)
    pivot = ar.pivot_table(index="sector", columns="ratio",
                            values=value_col, aggfunc=agg)
    # Sektoren ohne Reihenfolge-Eintrag (z.B. 'Other') landen am Ende
    avail_sectors = [s for s in SECTOR_ORDER if s in pivot.index]
    other = [s for s in pivot.index if s not in SECTOR_ORDER]
    pivot = pivot.reindex(avail_sectors + other)
    pivot = pivot[[r for r in RATIO_ORDER if r in pivot.columns]]
    return pivot


def compute_signif_rate_by_sector(ar: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    """Signifikanzrate pro Sektor × Kennzahl in Prozent."""
    if "sector" not in ar.columns:
        ar = attach_sector(ar)
    pivot = ar.pivot_table(
        index="sector", columns="ratio", values="phi1_pval",
        aggfunc=lambda s: (s < alpha).mean() * 100,
    )
    avail_sectors = [s for s in SECTOR_ORDER if s in pivot.index]
    other = [s for s in pivot.index if s not in SECTOR_ORDER]
    pivot = pivot.reindex(avail_sectors + other)
    pivot = pivot[[r for r in RATIO_ORDER if r in pivot.columns]]
    return pivot


def compute_quadrants(ar: pd.DataFrame) -> pd.DataFrame:
    """Berechnet pro Ticker × Kennzahl den Quadranten (Median-Split).

    Quadranten:
      - KORREKTIV-STABIL  (φ₁ < median, σ ≤ median)
      - KORREKTIV-VOLATIL (φ₁ < median, σ > median)
      - PERSISTENT-STABIL (φ₁ ≥ median, σ ≤ median)
      - PERSISTENT-VOLATIL (φ₁ ≥ median, σ > median)

    Returns:
        Kopie von ar mit zusätzlicher Spalte 'quadrant' und den verwendeten
        Median-Werten 'phi1_median_used', 'sigma_median_used' pro Ratio.
    """
    out = ar.copy()
    # Median pro Ratio
    medians = ar.groupby("ratio")[["phi1", "sigma_diff"]].median().rename(
        columns={"phi1": "phi1_median_used", "sigma_diff": "sigma_median_used"}
    )
    out = out.merge(medians, left_on="ratio", right_index=True)
    out["quadrant"] = out.apply(
        lambda r: ("KORREKTIV" if r["phi1"] < r["phi1_median_used"] else "PERSISTENT")
        + "-"
        + ("VOLATIL" if r["sigma_diff"] > r["sigma_median_used"] else "STABIL"),
        axis=1,
    )
    return out


def compute_descriptive_stats(
    ar: pd.DataFrame,
    by: str = "ratio",
    value_cols: tuple = ("phi1", "sigma_diff", "r_squared"),
) -> pd.DataFrame:
    """Vollständige Deskriptivstatistik (Mean, Median, Std, IQR, p5, p95) pro Gruppe.

    Args:
        ar: AR-Features (mit oder ohne Sektor-Merge).
        by: Gruppenspalte ('ratio' für Kennzahlen-weise, 'sector' für sektoral).
        value_cols: Welche Werte beschreiben.

    Returns:
        Long-Format DataFrame mit Spalten group, value, mean, median, std,
        iqr_low, iqr_high, p5, p95, n.
    """
    rows = []
    for group_val, group_df in ar.groupby(by):
        for vc in value_cols:
            s = group_df[vc].dropna()
            if len(s) == 0:
                continue
            rows.append({
                by: group_val,
                "value": vc,
                "mean": s.mean(),
                "median": s.median(),
                "std": s.std(),
                "iqr_low": s.quantile(0.25),
                "iqr_high": s.quantile(0.75),
                "p5": s.quantile(0.05),
                "p95": s.quantile(0.95),
                "n": len(s),
            })
    return pd.DataFrame(rows)


# ═════════════════════════════════════════════
# C. Stats-Funktionen
# ═════════════════════════════════════════════

def halflife_tau(phi1: float) -> float:
    """Halblebensdauer t½ = ln(0,5) / ln(1+φ₁) in Quartalen.

    Wohl­definiert nur für φ₁ ∈ (−1, 0). Sonst NaN.
    """
    if phi1 is None or pd.isna(phi1):
        return float("nan")
    one_plus = 1.0 + phi1
    if one_plus <= 0 or one_plus >= 1:
        return float("nan")
    return log(0.5) / log(one_plus)


def add_halflife_columns(summary: pd.DataFrame) -> pd.DataFrame:
    """Erweitert ar_summary_by_ratio.csv um hl_quarters_tau und hl_years_tau.

    Idempotent: kann mehrfach aufgerufen werden.
    """
    out = summary.copy()
    out["hl_quarters_tau"] = out["phi1_median"].apply(halflife_tau).round(4)
    out["hl_years_tau"] = (out["hl_quarters_tau"] / 4).round(4)
    return out


def bonferroni_threshold(alpha: float = 0.05, n_tests: int = 1) -> float:
    """Bonferroni-korrigierte Signifikanzschwelle."""
    return alpha / n_tests


def quadrant_uniformity_chi2(ar: pd.DataFrame) -> pd.DataFrame:
    """χ²-Test auf Gleichverteilung der vier Quadranten pro Kennzahl.

    Methodisches Backup zu Tab. 4.7 (Spearman φ₁ × σ).
    """
    quads = compute_quadrants(ar)
    rows = []
    for ratio, sub in quads.groupby("ratio"):
        counts = sub["quadrant"].value_counts()
        ks = int(counts.get("KORREKTIV-STABIL", 0))
        kv = int(counts.get("KORREKTIV-VOLATIL", 0))
        ps = int(counts.get("PERSISTENT-STABIL", 0))
        pv = int(counts.get("PERSISTENT-VOLATIL", 0))
        n = ks + kv + ps + pv
        chi2, p = stats.chisquare([ks, kv, ps, pv], [n / 4] * 4)
        rows.append({"ratio": ratio, "n": n, "KS": ks, "KV": kv,
                      "PS": ps, "PV": pv, "chi2": round(chi2, 2),
                      "p_value": round(p, 4)})
    return pd.DataFrame(rows).set_index("ratio").reindex(
        [r for r in RATIO_ORDER if r in quads["ratio"].unique()]
    ).reset_index()


def correlation_with_bonferroni(
    pval_matrix: pd.DataFrame,
    n_total_tests: int = 42,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Long-Form aller Paare mit Bonferroni-Markierung.

    Args:
        pval_matrix: 7×7 p-Wert-Matrix (von load_pval_matrix).
        n_total_tests: 42 für FF2 (21 phi1-Paare + 21 sigma-Paare).
        alpha: Familienweise Fehlerrate.
    """
    threshold = bonferroni_threshold(alpha, n_total_tests)
    ratios = list(pval_matrix.index)
    rows = []
    for a, b in combinations(ratios, 2):
        p = float(pval_matrix.loc[a, b])
        rows.append({
            "ratio_a": a, "ratio_b": b, "p_value": p,
            "significant_05": p < alpha,
            "significant_bonferroni": p < threshold,
        })
    return pd.DataFrame(rows)


# ═════════════════════════════════════════════
# Schnell-Referenz für Notebook-Nutzer
# ═════════════════════════════════════════════
__all__ = [
    # Konstanten
    "RATIO_ORDER", "RATIO_LABEL", "RATIO_LAYER", "SECTOR_ORDER",
    # Loader
    "load_ar_features", "load_ar_summary", "load_ar_summary_multimodel",
    "load_ratio_panel", "load_company_profiles", "load_phi1_sigma_correlation",
    "load_corr_matrix", "load_pval_matrix", "load_pval_long",
    "load_sample_comparison", "load_ff3_chi2", "load_ff3_size_effects",
    "load_kmeans_labels",
    # Aggregationen
    "attach_sector", "compute_sector_pivot", "compute_signif_rate_by_sector",
    "compute_quadrants", "compute_descriptive_stats",
    # Stats
    "halflife_tau", "add_halflife_columns", "bonferroni_threshold",
    "quadrant_uniformity_chi2", "correlation_with_bonferroni",
]
