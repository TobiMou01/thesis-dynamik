"""
classify.py – Klassifikation: Median-Quadranten + flexibles K-Means
====================================================================
Zwei Methoden, komplementär:

1. MEDIAN-QUADRANTEN (theoriebasiert, fix)
   - Pro Kennzahl: φ₁ × σ → 4 Quadranten via Median-Split
   - Transparent, reproduzierbar, immer 4 Gruppen

2. K-MEANS (datengetrieben, flexibel)
   - Beliebige Feature-Matrix als Input
   - Automatische k-Optimierung via Silhouette
   - Designed für wechselnde Fragestellungen:
     · nur AR-Parameter (φ₁, σ) über alle Kennzahlen
     · AR-Parameter + Level-Mittelwerte
     · einzelne Kennzahl-Subsets
     · ...was immer du vergleichen willst
"""

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler

from config import (
    RATIO_NAMES, QUADRANT_LABELS,
    OUT_AR, OUT_CLUSTER, OUT_RATIOS, ensure_output_dirs,
)

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════
# TEIL 1: MEDIAN-QUADRANTEN
# ══════════════════════════════════════════════
def assign_quadrants(features: pd.DataFrame) -> pd.DataFrame:
    """Median-Split pro Kennzahl auf φ₁ × σ → 4 Quadranten."""
    df = features.copy()

    medians = (
        df.groupby("ratio")[["phi1", "sigma_diff"]]
        .median()
        .rename(columns={"phi1": "phi1_median", "sigma_diff": "sigma_median"})
    )
    df = df.merge(medians, on="ratio", how="left")

    df["phi1_above_median"] = df["phi1"] >= df["phi1_median"]
    df["sigma_above_median"] = df["sigma_diff"] >= df["sigma_median"]

    ql = QUADRANT_LABELS
    conditions = {
        (False, False): ql.low_phi_low_vol,
        (False, True):  ql.low_phi_high_vol,
        (True,  False): ql.high_phi_low_vol,
        (True,  True):  ql.high_phi_high_vol,
    }
    df["quadrant"] = [
        conditions[(p, s)]
        for p, s in zip(df["phi1_above_median"], df["sigma_above_median"])
    ]
    return df


def quadrant_summary(classified: pd.DataFrame) -> pd.DataFrame:
    summary = (
        classified.groupby(["ratio", "quadrant"]).size().unstack(fill_value=0)
    )
    totals = summary.sum(axis=1)
    pct = summary.div(totals, axis=0).mul(100).round(1)
    pct.columns = [f"{c}_pct" for c in pct.columns]
    return pd.concat([summary, pct], axis=1)


def threshold_table(classified: pd.DataFrame) -> pd.DataFrame:
    return (
        classified.groupby("ratio")[["phi1_median", "sigma_median"]]
        .first().round(4)
    )


# ══════════════════════════════════════════════
# TEIL 2: FLEXIBLES K-MEANS
# ══════════════════════════════════════════════
@dataclass
class KMeansResult:
    """Container für ein K-Means-Ergebnis."""
    name: str                    # Bezeichnung des Runs (z.B. "ar_all_ratios")
    k: int                       # gewähltes k
    silhouette: float            # Silhouette-Score
    labels: pd.Series            # Cluster-Labels, indiziert auf ticker
    feature_cols: list[str]      # verwendete Features
    silhouette_curve: dict[int, float]  # k → Silhouette für alle getesteten k
    inertia_curve: dict[int, float]     # k → Inertia (Elbow)


def build_feature_matrix(
    ar_features: pd.DataFrame,
    ratio_panel: pd.DataFrame | None = None,
    feature_spec: dict[str, list[str]] | None = None,
) -> pd.DataFrame:
    """Baut eine Ticker-Level Feature-Matrix aus verschiedenen Quellen.

    Args:
        ar_features: AR-Ergebnisse (ticker × ratio × phi1/sigma_diff/...).
        ratio_panel: Optional – Kennzahlen-Panel für Level-Features.
        feature_spec: Dict das steuert, welche Features eingebaut werden.
            Keys sind Quelltypen, Values die gewünschten Spalten:
            {
                "ar": ["phi1", "sigma_diff"],        # aus ar_features
                "level_mean": ["ROA", "ROE"],         # Mittelwert über Zeit
                "level_std": ["ROA"],                  # Std über Zeit
                "level_trend": ["ROA"],                # lin. Trend-Steigung
            }
            Default: {"ar": ["phi1", "sigma_diff"]} für alle Kennzahlen.

    Returns:
        DataFrame mit ticker als Index, eine Spalte pro Feature.
        Spaltenformat: "{ratio}_{feature}" (z.B. "ROA_phi1", "ROE_sigma_diff").
    """
    if feature_spec is None:
        feature_spec = {"ar": ["phi1", "sigma_diff"]}

    parts: list[pd.DataFrame] = []

    # --- AR-Features: pivotieren von long zu wide ---
    if "ar" in feature_spec:
        for col in feature_spec["ar"]:
            pivot = (
                ar_features
                .pivot(index="ticker", columns="ratio", values=col)
                .rename(columns=lambda r: f"{r}_{col}")
            )
            parts.append(pivot)

    # --- Level-Features aus dem Ratio-Panel ---
    if ratio_panel is not None:
        grouped = ratio_panel.groupby("ticker")

        if "level_mean" in feature_spec:
            means = grouped[feature_spec["level_mean"]].mean()
            means.columns = [f"{c}_mean" for c in means.columns]
            parts.append(means)

        if "level_std" in feature_spec:
            stds = grouped[feature_spec["level_std"]].std(ddof=1)
            stds.columns = [f"{c}_level_std" for c in stds.columns]
            parts.append(stds)

        if "level_trend" in feature_spec:
            # Lineare Steigung über die gesamte Zeitreihe
            trends = {}
            for ratio in feature_spec["level_trend"]:
                def _slope(g: pd.Series) -> float:
                    y = g.dropna().values
                    if len(y) < 3:
                        return np.nan
                    x = np.arange(len(y))
                    return float(np.polyfit(x, y, 1)[0])
                trends[f"{ratio}_trend"] = grouped[ratio].apply(_slope)
            parts.append(pd.DataFrame(trends))

    if not parts:
        raise ValueError("feature_spec hat keine gültigen Quellen ergeben.")

    matrix = pd.concat(parts, axis=1)
    # NaN-Zeilen entfernen (Ticker ohne genug Daten)
    n_before = len(matrix)
    matrix = matrix.dropna()
    n_dropped = n_before - len(matrix)
    if n_dropped > 0:
        logger.info("Feature-Matrix: %d Ticker entfernt wegen NaN (%d verbleibend)",
                     n_dropped, len(matrix))

    return matrix


def run_kmeans(
    matrix: pd.DataFrame,
    name: str = "default",
    k_range: range = range(2, 9),
    random_state: int = 42,
) -> KMeansResult:
    """K-Means mit automatischer k-Wahl via Silhouette.

    Args:
        matrix: Feature-Matrix (ticker × features), wird z-standardisiert.
        name: Bezeichnung für diesen Run.
        k_range: Zu testende k-Werte.
        random_state: Seed für Reproduzierbarkeit.

    Returns:
        KMeansResult mit optimalem k und Cluster-Labels.
    """
    scaler = StandardScaler()
    X = scaler.fit_transform(matrix.values)

    silhouette_curve: dict[int, float] = {}
    inertia_curve: dict[int, float] = {}

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=random_state, n_init=20)
        labels = km.fit_predict(X)
        silhouette_curve[k] = float(silhouette_score(X, labels))
        inertia_curve[k] = float(km.inertia_)

    best_k = max(silhouette_curve, key=silhouette_curve.get)
    best_sil = silhouette_curve[best_k]

    # Finaler Fit mit bestem k
    km_final = KMeans(n_clusters=best_k, random_state=random_state, n_init=20)
    final_labels = km_final.fit_predict(X)

    label_series = pd.Series(final_labels, index=matrix.index, name=f"kmeans_{name}")

    logger.info("K-Means '%s': k=%d (Silhouette=%.3f), %d Ticker, %d Features",
                name, best_k, best_sil, len(matrix), matrix.shape[1])

    return KMeansResult(
        name=name,
        k=best_k,
        silhouette=best_sil,
        labels=label_series,
        feature_cols=list(matrix.columns),
        silhouette_curve=silhouette_curve,
        inertia_curve=inertia_curve,
    )


def compare_with_quadrants(
    kmeans_result: KMeansResult,
    quadrant_df: pd.DataFrame,
    ratio: str,
) -> float | None:
    """Adjusted Rand Index zwischen K-Means-Labels und Quadranten für eine Kennzahl."""
    q_sub = quadrant_df[quadrant_df["ratio"] == ratio][["ticker", "quadrant"]]
    merged = q_sub.merge(
        kmeans_result.labels.reset_index().rename(columns={"index": "ticker"}),
        on="ticker", how="inner",
    )
    if len(merged) < 10:
        return None
    return float(adjusted_rand_score(merged["quadrant"], merged[f"kmeans_{kmeans_result.name}"]))


def save_kmeans_result(result: KMeansResult) -> None:
    """Speichert Labels und Diagnostik."""
    # Labels
    labels_path = OUT_CLUSTER / f"kmeans_{result.name}_labels.csv"
    result.labels.reset_index().to_csv(labels_path, index=False)

    # Diagnostik
    diag = pd.DataFrame({
        "k": list(result.silhouette_curve.keys()),
        "silhouette": list(result.silhouette_curve.values()),
        "inertia": [result.inertia_curve[k] for k in result.silhouette_curve],
    })
    diag_path = OUT_CLUSTER / f"kmeans_{result.name}_diagnostics.csv"
    diag.to_csv(diag_path, index=False)

    logger.info("K-Means '%s' gespeichert: %s, %s", result.name, labels_path, diag_path)


# ══════════════════════════════════════════════
# CLI – Standardläufe
# ══════════════════════════════════════════════
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    ensure_output_dirs()

    # --- Daten laden ---
    ar_features = pd.read_csv(OUT_AR / "ar_features.csv")
    ratio_panel = pd.read_csv(OUT_RATIOS / "ratio_panel.csv")
    logger.info("Daten geladen: %d AR-Zeilen, %d Panel-Zeilen",
                len(ar_features), len(ratio_panel))

    # ── 1. Quadranten ──
    classified = assign_quadrants(ar_features)
    classified.to_csv(OUT_CLUSTER / "quadrant_assignments.csv", index=False)
    thresholds = threshold_table(classified)
    thresholds.to_csv(OUT_CLUSTER / "quadrant_thresholds.csv")
    q_summary = quadrant_summary(classified)
    q_summary.to_csv(OUT_CLUSTER / "quadrant_summary.csv")

    print(f"\n{'='*70}")
    print("  QUADRANTEN")
    print(f"{'='*70}")
    print(f"\nSchwellenwerte:")
    print(thresholds.to_string())
    print(f"\nVerteilung:")
    print(q_summary.to_string())

    # ── 2. K-Means: AR-Dynamik (φ₁ + σ aller Kennzahlen) ──
    matrix_ar = build_feature_matrix(ar_features, feature_spec={"ar": ["phi1", "sigma_diff"]})
    result_ar = run_kmeans(matrix_ar, name="ar_dynamics")
    save_kmeans_result(result_ar)

    # ── 3. K-Means: AR + Level-Mittelwerte ──
    matrix_full = build_feature_matrix(
        ar_features, ratio_panel,
        feature_spec={
            "ar": ["phi1", "sigma_diff"],
            "level_mean": RATIO_NAMES,
        },
    )
    result_full = run_kmeans(matrix_full, name="ar_plus_levels")
    save_kmeans_result(result_full)

    # ── Vergleich ──
    print(f"\n{'='*70}")
    print("  K-MEANS")
    print(f"{'='*70}")
    for res in [result_ar, result_full]:
        print(f"\n  Run '{res.name}':")
        print(f"    k={res.k}, Silhouette={res.silhouette:.3f}, "
              f"{len(res.labels)} Ticker, {len(res.feature_cols)} Features")
        print(f"    Silhouette-Kurve: {res.silhouette_curve}")
        print(f"    Features: {res.feature_cols[:6]}{'...' if len(res.feature_cols) > 6 else ''}")

        # ARI vs Quadranten pro Kennzahl
        aris = {}
        for ratio in RATIO_NAMES:
            ari = compare_with_quadrants(res, classified, ratio)
            if ari is not None:
                aris[ratio] = round(ari, 3)
        if aris:
            print(f"    ARI vs Quadranten: {aris}")
