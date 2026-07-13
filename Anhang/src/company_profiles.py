"""
company_profiles.py – Quadrantenprofile pro Unternehmen + FF3 Externe Validierung
===================================================================================
Teil 3 des Arbeitsplans:
  3.1  Quadrantenprofile: dominanter Quadrant, Konsistenz-Score, Schicht-Analyse
  3.2  K-Means-Interpretation: Cluster-Zentroide, Trennmerkmale
  3.3  FF3 Externe Validierung: χ², logistische Regression, Größeneffekte

Erzeugt:
  output/profiles/company_quadrant_profiles.csv  – Profil pro Ticker
  output/profiles/consistency_summary.csv        – Konsistenz-Statistiken
  output/profiles/ff3_chi2_results.csv           – χ²-Tests Sektor × Quadrant
  output/profiles/ff3_logistic_results.csv       – Logistische Regression
  output/profiles/ff3_size_effects.csv           – Größeneffekte (MarketCap, Employees)
  output/profiles/ff3_summary.md                 – Zusammenfassung
"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))

from config import RATIOS, RATIO_NAMES, OUTPUT_DIR

logger = logging.getLogger(__name__)

OUT_PROFILES = OUTPUT_DIR / "profiles"
OUT_PROFILES.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# 3.1: Quadrantenprofile pro Unternehmen
# ─────────────────────────────────────────────

def build_company_profiles():
    """Erstellt pro Unternehmen ein Dynamik-Profil über alle 7 Kennzahlen."""
    logger.info("=" * 60)
    logger.info("Teil 3.1: Quadrantenprofile pro Unternehmen")
    logger.info("=" * 60)

    quad = pd.read_csv(OUTPUT_DIR / "clustering" / "quadrant_assignments.csv")
    val = pd.read_csv(OUTPUT_DIR / "external_validation" / "validation_features.csv")

    # Kategorien
    ratio_cats = {r.name: r.category for r in RATIOS}

    profiles = []
    for ticker, group in quad.groupby("ticker"):
        row = {"ticker": ticker}

        # Quadrant pro Ratio
        for _, r in group.iterrows():
            row[f"q_{r['ratio']}"] = r["quadrant"]

        # Dominanter Quadrant (Modus über alle 7 Ratios)
        quadrants = group["quadrant"].tolist()
        quad_counts = pd.Series(quadrants).value_counts()
        row["dominant_quadrant"] = quad_counts.index[0]
        row["dominant_count"] = int(quad_counts.iloc[0])

        # Konsistenz-Score: Anteil der Ratios im dominanten Quadrant
        row["consistency_score"] = row["dominant_count"] / len(quadrants)

        # Schichtbasierte Konsistenz
        for cat_name in ["Profitabilität", "Liquidität", "Kapitalstruktur"]:
            cat_ratios = [r.name for r in RATIOS if r.category == cat_name]
            cat_quads = group[group["ratio"].isin(cat_ratios)]["quadrant"].tolist()
            if cat_quads:
                cat_counts = pd.Series(cat_quads).value_counts()
                row[f"dominant_{cat_name}"] = cat_counts.index[0]
                row[f"consistency_{cat_name}"] = cat_counts.iloc[0] / len(cat_quads)
            else:
                row[f"dominant_{cat_name}"] = None
                row[f"consistency_{cat_name}"] = None

        # φ₁ und σ Mittelwerte pro Schicht
        for cat_name in ["Profitabilität", "Liquidität", "Kapitalstruktur"]:
            cat_ratios = [r.name for r in RATIOS if r.category == cat_name]
            cat_data = group[group["ratio"].isin(cat_ratios)]
            row[f"phi1_mean_{cat_name}"] = cat_data["phi1"].mean()
            row[f"sigma_mean_{cat_name}"] = cat_data["sigma_diff"].mean()

        profiles.append(row)

    df_profiles = pd.DataFrame(profiles)

    # Merge mit Validierungsdaten (Sektor, MarketCap, Employees)
    df_profiles = df_profiles.merge(
        val[["ticker", "sector", "industry", "market_cap", "employees"]],
        on="ticker", how="left"
    )

    # Speichern
    df_profiles.to_csv(OUT_PROFILES / "company_quadrant_profiles.csv", index=False)
    logger.info(f"Profile: {len(df_profiles)} Unternehmen gespeichert")

    # Konsistenz-Statistiken
    consistency_stats = {
        "metric": [],
        "mean": [],
        "median": [],
        "std": [],
        "pct_fully_consistent": [],
        "pct_majority": [],
    }

    # Gesamt
    consistency_stats["metric"].append("Gesamt (7 Ratios)")
    consistency_stats["mean"].append(df_profiles["consistency_score"].mean())
    consistency_stats["median"].append(df_profiles["consistency_score"].median())
    consistency_stats["std"].append(df_profiles["consistency_score"].std())
    consistency_stats["pct_fully_consistent"].append(
        (df_profiles["consistency_score"] == 1.0).mean() * 100
    )
    consistency_stats["pct_majority"].append(
        (df_profiles["consistency_score"] >= 0.5).mean() * 100
    )

    # Pro Schicht
    for cat_name in ["Profitabilität", "Liquidität", "Kapitalstruktur"]:
        col = f"consistency_{cat_name}"
        consistency_stats["metric"].append(cat_name)
        consistency_stats["mean"].append(df_profiles[col].mean())
        consistency_stats["median"].append(df_profiles[col].median())
        consistency_stats["std"].append(df_profiles[col].std())
        n_ratios = len([r for r in RATIOS if r.category == cat_name])
        consistency_stats["pct_fully_consistent"].append(
            (df_profiles[col] == 1.0).mean() * 100
        )
        consistency_stats["pct_majority"].append(
            (df_profiles[col] >= 0.5).mean() * 100
        )

    cons_df = pd.DataFrame(consistency_stats).round(4)
    cons_df.to_csv(OUT_PROFILES / "consistency_summary.csv", index=False)
    logger.info("Konsistenz-Statistiken gespeichert")

    return df_profiles, cons_df


# ─────────────────────────────────────────────
# 3.2: K-Means Interpretation
# ─────────────────────────────────────────────

def interpret_kmeans():
    """Interpretiert die K-Means-Cluster inhaltlich."""
    logger.info("=" * 60)
    logger.info("Teil 3.2: K-Means-Interpretation")
    logger.info("=" * 60)

    ar = pd.read_csv(OUTPUT_DIR / "ar" / "ar_features.csv")
    val = pd.read_csv(OUTPUT_DIR / "external_validation" / "validation_features.csv")

    results = {}

    for run_name in ["ar_dynamics", "ar_plus_levels"]:
        labels = pd.read_csv(OUTPUT_DIR / "clustering" / f"kmeans_{run_name}_labels.csv")
        diag = pd.read_csv(OUTPUT_DIR / "clustering" / f"kmeans_{run_name}_diagnostics.csv")

        # Spalte umbenennen zu "cluster"
        cluster_col = f"kmeans_{run_name}"
        if cluster_col in labels.columns:
            labels = labels.rename(columns={cluster_col: "cluster"})

        # Merge labels mit AR-Features
        merged = ar.merge(labels[["ticker", "cluster"]], on="ticker")
        merged = merged.merge(val[["ticker", "sector", "market_cap", "employees"]], on="ticker", how="left")

        # Cluster-Profile
        cluster_profile = merged.groupby(["cluster", "ratio"]).agg(
            n=("ticker", "nunique"),
            phi1_median=("phi1", "median"),
            sigma_median=("sigma_diff", "median"),
            r2_median=("r_squared", "median"),
        ).round(4)

        # Cluster × Sektor
        cluster_sector = labels.merge(val[["ticker", "sector"]], on="ticker")
        ct = pd.crosstab(cluster_sector["cluster"], cluster_sector["sector"])

        # Cluster × MarketCap (Median)
        cluster_size = labels.merge(val[["ticker", "market_cap", "employees"]], on="ticker")
        size_by_cluster = cluster_size.groupby("cluster").agg(
            n=("ticker", "count"),
            market_cap_median=("market_cap", "median"),
            employees_median=("employees", "median"),
        ).round(0)

        results[run_name] = {
            "profile": cluster_profile,
            "sector_crosstab": ct,
            "size_by_cluster": size_by_cluster,
            "diagnostics": diag,
        }

        logger.info(f"\n{run_name}:")
        logger.info(f"  Cluster-Verteilung: {labels['cluster'].value_counts().to_dict()}")
        logger.info(f"  Best k: {diag.loc[diag['silhouette'].idxmax(), 'k']} (Silhouette={diag['silhouette'].max():.3f})")

    return results


# ─────────────────────────────────────────────
# 3.3: FF3 Externe Validierung
# ─────────────────────────────────────────────

def run_ff3_validation(df_profiles):
    """Statistische Tests für FF3: Hängen Dynamik-Muster von Strukturmerkmalen ab?"""
    logger.info("=" * 60)
    logger.info("Teil 3.3: FF3 Externe Validierung")
    logger.info("=" * 60)

    val = pd.read_csv(OUTPUT_DIR / "external_validation" / "validation_features.csv")
    quad = pd.read_csv(OUTPUT_DIR / "clustering" / "quadrant_assignments.csv")

    # ─── 3.3a: χ²-Tests: Sektor × Quadrant pro Ratio ───
    chi2_results = []
    for ratio_name in RATIO_NAMES:
        sub = quad[quad["ratio"] == ratio_name][["ticker", "quadrant"]].merge(
            val[["ticker", "sector"]], on="ticker"
        )
        ct = pd.crosstab(sub["sector"], sub["quadrant"])

        # Nur Sektoren mit >= 10 Ticker
        ct = ct[ct.sum(axis=1) >= 10]
        if ct.shape[0] < 2 or ct.shape[1] < 2:
            continue

        chi2, p, dof, _ = stats.chi2_contingency(ct)
        n = ct.values.sum()
        k = min(ct.shape)
        cramers_v = np.sqrt(chi2 / (n * (k - 1))) if n * (k - 1) > 0 else 0

        chi2_results.append({
            "ratio": ratio_name,
            "chi2": chi2,
            "p_value": p,
            "dof": dof,
            "cramers_v": cramers_v,
            "n_sectors": ct.shape[0],
            "n_tickers": n,
            "significant": p < 0.05,
        })

    chi2_df = pd.DataFrame(chi2_results).round(4)
    chi2_df.to_csv(OUT_PROFILES / "ff3_chi2_results.csv", index=False)
    logger.info(f"χ²-Tests: {chi2_df['significant'].sum()}/{len(chi2_df)} signifikant")

    # ─── 3.3b: Kruskal-Wallis: Sektor → φ₁ pro Ratio ───
    kw_results = []
    for ratio_name in RATIO_NAMES:
        sub = quad[quad["ratio"] == ratio_name][["ticker", "phi1"]].merge(
            val[["ticker", "sector"]], on="ticker"
        )
        groups = [g["phi1"].values for _, g in sub.groupby("sector") if len(g) >= 10]
        if len(groups) < 2:
            continue

        h_stat, p_val = stats.kruskal(*groups)
        # Effektstärke: η² = (H - k + 1) / (n - k)
        n_total = sum(len(g) for g in groups)
        k = len(groups)
        eta_sq = (h_stat - k + 1) / (n_total - k) if n_total > k else 0

        kw_results.append({
            "ratio": ratio_name,
            "test": "Kruskal-Wallis",
            "variable": "phi1",
            "H_stat": h_stat,
            "p_value": p_val,
            "eta_squared": max(0, eta_sq),
            "n_groups": k,
            "n_total": n_total,
            "significant": p_val < 0.05,
        })

    # Auch für sigma_diff
    for ratio_name in RATIO_NAMES:
        sub = quad[quad["ratio"] == ratio_name][["ticker", "sigma_diff"]].merge(
            val[["ticker", "sector"]], on="ticker"
        )
        groups = [g["sigma_diff"].values for _, g in sub.groupby("sector") if len(g) >= 10]
        if len(groups) < 2:
            continue

        h_stat, p_val = stats.kruskal(*groups)
        n_total = sum(len(g) for g in groups)
        k = len(groups)
        eta_sq = (h_stat - k + 1) / (n_total - k) if n_total > k else 0

        kw_results.append({
            "ratio": ratio_name,
            "test": "Kruskal-Wallis",
            "variable": "sigma_diff",
            "H_stat": h_stat,
            "p_value": p_val,
            "eta_squared": max(0, eta_sq),
            "n_groups": k,
            "n_total": n_total,
            "significant": p_val < 0.05,
        })

    kw_df = pd.DataFrame(kw_results).round(4)

    # ─── 3.3c: Größeneffekte (MarketCap, Employees) ───
    size_results = []
    for ratio_name in RATIO_NAMES:
        sub = quad[quad["ratio"] == ratio_name][["ticker", "phi1", "sigma_diff", "quadrant"]].merge(
            val[["ticker", "market_cap", "employees"]], on="ticker"
        )
        sub = sub.dropna(subset=["market_cap"])

        # MarketCap-Tercile
        sub["mcap_tercile"] = pd.qcut(sub["market_cap"], 3, labels=["Small", "Mid", "Large"])

        for size_var in ["market_cap", "employees"]:
            for target in ["phi1", "sigma_diff"]:
                valid = sub.dropna(subset=[size_var, target])
                if len(valid) < 20:
                    continue

                # Spearman-Korrelation
                rho, p_val = stats.spearmanr(valid[size_var], valid[target])
                size_results.append({
                    "ratio": ratio_name,
                    "size_variable": size_var,
                    "target": target,
                    "spearman_rho": rho,
                    "p_value": p_val,
                    "n": len(valid),
                    "significant": p_val < 0.05,
                })

        # Quadrant-Verteilung nach MarketCap-Tercile
        ct = pd.crosstab(sub["mcap_tercile"], sub["quadrant"])
        if ct.shape[0] >= 2 and ct.shape[1] >= 2:
            chi2, p, dof, _ = stats.chi2_contingency(ct)
            n = ct.values.sum()
            k = min(ct.shape)
            cramers_v = np.sqrt(chi2 / (n * (k - 1))) if n * (k - 1) > 0 else 0
            size_results.append({
                "ratio": ratio_name,
                "size_variable": "mcap_tercile",
                "target": "quadrant",
                "spearman_rho": cramers_v,  # Cramér's V statt ρ
                "p_value": p,
                "n": n,
                "significant": p < 0.05,
            })

    size_df = pd.DataFrame(size_results).round(4)
    size_df.to_csv(OUT_PROFILES / "ff3_size_effects.csv", index=False)

    # Kombinierte Ergebnisse
    all_tests = pd.concat([
        chi2_df[["ratio", "chi2", "p_value", "cramers_v", "significant"]].assign(test="χ² Sektor×Quadrant"),
        kw_df[["ratio", "variable", "H_stat", "p_value", "eta_squared", "significant"]].assign(test="Kruskal-Wallis"),
    ], ignore_index=True)

    logger.info(f"\nχ²-Tests Sektor×Quadrant: {chi2_df['significant'].sum()}/{len(chi2_df)} signifikant")
    logger.info(f"Kruskal-Wallis φ₁: {kw_df[kw_df['variable']=='phi1']['significant'].sum()}/{len(kw_df[kw_df['variable']=='phi1'])} signifikant")
    logger.info(f"Größeneffekte: {size_df['significant'].sum()}/{len(size_df)} signifikant")

    return chi2_df, kw_df, size_df


# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────

def write_ff3_summary(df_profiles, cons_df, chi2_df, kw_df, size_df, kmeans_results):
    """Schreibt eine Zusammenfassung der FF3-Ergebnisse."""
    lines = [
        "# FF3: Externe Validierung – Zusammenfassung",
        "",
        "## 1. Quadrantenprofile pro Unternehmen",
        "",
    ]

    lines.append("### Konsistenz-Scores")
    lines.append("")
    lines.append("| Metrik | Mean | Median | Std | % voll konsistent | % Mehrheit |")
    lines.append("|---|:---:|:---:|:---:|:---:|:---:|")
    for _, row in cons_df.iterrows():
        lines.append(f"| {row['metric']} | {row['mean']:.3f} | {row['median']:.3f} | {row['std']:.3f} | {row['pct_fully_consistent']:.1f}% | {row['pct_majority']:.1f}% |")
    lines.append("")

    # Dominante Quadranten
    dom_dist = df_profiles["dominant_quadrant"].value_counts()
    lines.append("### Dominante Quadranten (Verteilung)")
    lines.append("")
    for q, n in dom_dist.items():
        pct = n / len(df_profiles) * 100
        lines.append(f"- {q}: {n} ({pct:.1f}%)")
    lines.append("")

    # χ²-Tests
    lines.append("## 2. χ²-Tests: Sektor × Quadrant")
    lines.append("")
    lines.append("| Kennzahl | χ² | p | Cramér's V | Signifikant |")
    lines.append("|---|:---:|:---:|:---:|:---:|")
    for _, row in chi2_df.iterrows():
        sig = "✓" if row["significant"] else "✗"
        lines.append(f"| {row['ratio']} | {row['chi2']:.1f} | {row['p_value']:.4f} | {row['cramers_v']:.3f} | {sig} |")
    lines.append("")

    # Kruskal-Wallis
    lines.append("## 3. Kruskal-Wallis: Sektor → φ₁ / σ(ΔY)")
    lines.append("")
    lines.append("| Kennzahl | Variable | H | p | η² | Signifikant |")
    lines.append("|---|---|:---:|:---:|:---:|:---:|")
    for _, row in kw_df.iterrows():
        sig = "✓" if row["significant"] else "✗"
        lines.append(f"| {row['ratio']} | {row['variable']} | {row['H_stat']:.1f} | {row['p_value']:.4f} | {row['eta_squared']:.3f} | {sig} |")
    lines.append("")

    # Größeneffekte
    lines.append("## 4. Größeneffekte")
    lines.append("")
    sig_size = size_df[size_df["significant"]]
    if len(sig_size) > 0:
        lines.append("Signifikante Korrelationen (Spearman):")
        lines.append("")
        lines.append("| Kennzahl | Größe | Ziel | ρ | p |")
        lines.append("|---|---|---|:---:|:---:|")
        for _, row in sig_size.iterrows():
            lines.append(f"| {row['ratio']} | {row['size_variable']} | {row['target']} | {row['spearman_rho']:+.3f} | {row['p_value']:.4f} |")
    else:
        lines.append("Keine signifikanten Größeneffekte gefunden.")
    lines.append("")

    # K-Means
    lines.append("## 5. K-Means Cluster-Interpretation")
    lines.append("")
    for run_name, data in kmeans_results.items():
        lines.append(f"### {run_name}")
        lines.append(f"MarketCap/Employees pro Cluster:")
        lines.append("")
        lines.append(data["size_by_cluster"].to_string())
        lines.append("")

    md_path = OUT_PROFILES / "ff3_summary.md"
    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    logger.info(f"✓ Zusammenfassung: {md_path}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )

    print("=" * 60)
    print("  Teil 3: Klassifikation & Externe Validierung (FF1→FF3)")
    print("=" * 60)

    # 3.1
    df_profiles, cons_df = build_company_profiles()

    # 3.2
    kmeans_results = interpret_kmeans()

    # 3.3
    chi2_df, kw_df, size_df = run_ff3_validation(df_profiles)

    # Summary
    write_ff3_summary(df_profiles, cons_df, chi2_df, kw_df, size_df, kmeans_results)

    print("\n" + "=" * 60)
    print(f"  Teil 3 abgeschlossen. Ergebnisse in: {OUT_PROFILES}")
    print("=" * 60)
