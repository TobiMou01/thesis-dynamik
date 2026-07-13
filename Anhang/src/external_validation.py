"""
external_validation.py – Externe Strukturmerkmale für Validierung
=================================================================
Baut eine flache Tabelle pro Ticker mit:
  - Strukturmerkmale: Branche, Marktkapitalisierung, Mitarbeiterzahl
  - Einzel-Quadranten: 7 kennzahlspezifische Quadranten
  - Kategorie-Quadranten: Modus über Profitabilität / Liquidität / Kapitalstruktur
  - K-Means-Cluster: aus classify.py

Alle Tests (Chi², Kruskal-Wallis, Cramér's V) → Jupyter Notebook.
"""

import logging
from collections import Counter

import pandas as pd

from config import (
    RAW_PROFILE, RATIOS,
    OUT_CLUSTER, OUT_EXTVAL,
    ensure_output_dirs,
)

logger = logging.getLogger(__name__)

# Kategorie-Mapping aus config.RATIOS ableiten
RATIO_CATEGORIES: dict[str, list[str]] = {}
for r in RATIOS:
    RATIO_CATEGORIES.setdefault(r.category, []).append(r.name)


# ──────────────────────────────────────────────
# Profil-Daten laden
# ──────────────────────────────────────────────
def load_profiles(tickers: set[str]) -> pd.DataFrame:
    """Lädt Branche, MarketCap, Employees aus den Profil-CSVs."""
    rows = []
    for ticker in sorted(tickers):
        path = RAW_PROFILE / f"{ticker}.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path, nrows=1)
        rows.append({
            "ticker": ticker,
            "sector": df["sector"].iloc[0] if "sector" in df.columns else None,
            "industry": df["industry"].iloc[0] if "industry" in df.columns else None,
            "market_cap": pd.to_numeric(df["market_cap"].iloc[0], errors="coerce")
                if "market_cap" in df.columns else None,
            "employees": pd.to_numeric(df["employees"].iloc[0], errors="coerce")
                if "employees" in df.columns else None,
        })
    profiles = pd.DataFrame(rows)
    logger.info("Profile geladen: %d Ticker, davon %d mit Sektor, %d mit MarketCap, %d mit Employees",
                len(profiles),
                profiles["sector"].notna().sum(),
                profiles["market_cap"].notna().sum(),
                profiles["employees"].notna().sum())
    return profiles


# ──────────────────────────────────────────────
# Kategorie-Quadranten (Modus pro Kategorie)
# ──────────────────────────────────────────────
def compute_category_quadrants(quadrant_assignments: pd.DataFrame) -> pd.DataFrame:
    """Bestimmt pro Ticker und Kennzahl-Kategorie den dominanten Quadranten (Modus).

    Profitabilität: ROA, ROE, EBIT_margin, fcf_margin → Modus
    Liquidität:     current_ratio → direkt
    Kapitalstruktur: debt_to_equity, equity_ratio → Modus
    """
    records = []
    for ticker, group in quadrant_assignments.groupby("ticker"):
        row = {"ticker": ticker}
        for category, ratio_names in RATIO_CATEGORIES.items():
            quadrants = group.loc[group["ratio"].isin(ratio_names), "quadrant"].tolist()
            if quadrants:
                # Modus: häufigster Quadrant; bei Gleichstand → erster alphabetisch
                counts = Counter(quadrants)
                max_count = max(counts.values())
                modes = sorted(k for k, v in counts.items() if v == max_count)
                row[f"quadrant_{category}"] = modes[0]
        records.append(row)
    return pd.DataFrame(records)


# ──────────────────────────────────────────────
# Alles mergen → eine flache Tabelle
# ──────────────────────────────────────────────
def build_validation_table(
    quadrant_assignments: pd.DataFrame,
    kmeans_labels: dict[str, pd.Series] | None = None,
) -> pd.DataFrame:
    """Baut die vollständige Validierungstabelle.

    Args:
        quadrant_assignments: Output von classify.assign_quadrants().
        kmeans_labels: Dict {run_name: Series(ticker→label)}.

    Returns:
        DataFrame (ticker × Strukturmerkmale × Quadranten × Cluster).
    """
    tickers = set(quadrant_assignments["ticker"].unique())

    # 1. Profile
    profiles = load_profiles(tickers)

    # 2. Einzel-Quadranten: long → wide (eine Spalte pro Kennzahl)
    quad_wide = (
        quadrant_assignments[["ticker", "ratio", "quadrant"]]
        .pivot(index="ticker", columns="ratio", values="quadrant")
        .rename(columns=lambda c: f"quadrant_{c}")
        .reset_index()
    )

    # 3. Kategorie-Quadranten
    cat_quads = compute_category_quadrants(quadrant_assignments)

    # 4. Zusammenführen
    result = profiles.merge(quad_wide, on="ticker", how="inner")
    result = result.merge(cat_quads, on="ticker", how="left")

    # 5. K-Means-Labels anhängen
    if kmeans_labels:
        for name, labels in kmeans_labels.items():
            label_df = labels.reset_index()
            label_df.columns = ["ticker", f"kmeans_{name}"]
            result = result.merge(label_df, on="ticker", how="left")

    logger.info("Validierungstabelle: %d Ticker × %d Spalten", *result.shape)
    return result


# ══════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    ensure_output_dirs()
    OUT_EXTVAL.mkdir(parents=True, exist_ok=True)

    # --- Daten laden ---
    quadrants = pd.read_csv(OUT_CLUSTER / "quadrant_assignments.csv")

    # K-Means-Labels laden (alle vorhandenen Runs)
    kmeans_files = list(OUT_CLUSTER.glob("kmeans_*_labels.csv"))
    kmeans_labels = {}
    for f in kmeans_files:
        name = f.stem.replace("kmeans_", "").replace("_labels", "")
        df = pd.read_csv(f)
        col = [c for c in df.columns if c != "ticker"][0]
        kmeans_labels[name] = df.set_index("ticker")[col]
    logger.info("K-Means-Runs geladen: %s", list(kmeans_labels.keys()))

    # --- Tabelle bauen & speichern ---
    table = build_validation_table(quadrants, kmeans_labels)
    out_path = OUT_EXTVAL / "validation_features.csv"
    table.to_csv(out_path, index=False)

    # --- Übersicht ---
    print(f"\n{'='*70}")
    print("  EXTERNAL VALIDATION – Feature-Tabelle")
    print(f"{'='*70}")
    print(f"\n  Ticker: {len(table)}")
    print(f"  Spalten: {list(table.columns)}")
    print(f"\n  Sektor-Verteilung (Top 10):")
    print(table["sector"].value_counts().head(10).to_string())
    print(f"\n  MarketCap: {table['market_cap'].describe()[['count','mean','min','max']].to_string()}")
    print(f"\n  Employees: {table['employees'].describe()[['count','mean','min','max']].to_string()}")
    print(f"\n  Gespeichert: {out_path}")
