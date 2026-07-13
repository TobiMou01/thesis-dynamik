"""
ar_model.py – AR-Schätzung (Multi-Model-Framework)
====================================================
Für jeden Ticker × Kennzahl × Modellvariante:
  1. Zeitreihe Y(t) laden
  2. Transformation anwenden (diff_order: 0=Levels, 1=ΔY, 4=Δ₄Y)
  3. AR(p) per OLS schätzen (ar_lags: 1 oder 2)
  4. Volatilität σ berechnen (Std der transformierten Reihe)
  5. Half-Life berechnen (nur bei |φ₁|<1 und φ₁>0 auf Levels sinnvoll)

Modellvarianten werden über MODEL_SPECS in config.py gesteuert.

Ergebnis: ar_features.csv mit Spalten
  (model, ticker, ratio, phi1, phi1_se, phi1_pval, [phi2, phi2_pval],
   sigma_diff, half_life, c, r_squared, n_obs)
"""

import logging
import warnings
from typing import Optional

import numpy as np
import pandas as pd
import statsmodels.api as sm

from config import (
    RATIO_NAMES, AR_ORDER, DIFF_ORDER,
    MODEL_SPECS, ModelSpec,
    OUT_AR, ensure_output_dirs,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Generische AR-Schätzung für eine Einzelreihe
# ─────────────────────────────────────────────
def _fit_ar(series: pd.Series, diff_order: int, ar_lags: int,
            seasonal_diff: int = 0) -> dict | None:
    """Schätzt AR(p) auf einer (ggf. differenzierten) Zeitreihe.

    Args:
        series:        Level-Zeitreihe Y(t), indiziert auf Quartal.
        diff_order:    Differenzierungsordnung (0 = Levels, 1 = ΔY, 4 = Δ₄Y).
        ar_lags:       Anzahl AR-Lags (1 oder 2).
        seasonal_diff: Optionale zusaetzliche saisonale Differenzierung VOR diff_order.
                       0 = aus, 4 = saisonal (Box-Jenkins-Filter Δ₁Δ₄Y wenn diff_order=1).

    Returns:
        Dict mit Schätzergebnissen oder None bei zu wenig Daten / Fehler.
    """
    # Transformation: zuerst saisonale Differenz (wenn gewuenscht), dann diff_order
    if seasonal_diff > 0:
        series = series.diff(seasonal_diff)
    if diff_order > 0:
        transformed = series.diff(diff_order).dropna()
    else:
        transformed = series.dropna()

    min_obs = ar_lags + 3
    if len(transformed) < min_obs:
        return None

    # Volatilität der transformierten Reihe
    sigma = float(transformed.std(ddof=1))
    if sigma < 1e-15:
        return None

    # AR-Matrix aufbauen: y(t) = c + φ₁·y(t-1) [+ φ₂·y(t-2)] + ε(t)
    y = transformed.iloc[ar_lags:].values
    X_parts = []
    for lag in range(1, ar_lags + 1):
        X_parts.append(transformed.shift(lag).iloc[ar_lags:].values)

    X = np.column_stack(X_parts)

    # NaN-Bereinigung
    mask = ~np.isnan(y)
    for col in range(X.shape[1]):
        mask &= ~np.isnan(X[:, col])
    y = y[mask]
    X = X[mask]

    n_obs = len(y)
    if n_obs < min_obs:
        return None

    X = sm.add_constant(X)

    try:
        model = sm.OLS(y, X).fit()
    except Exception:
        return None

    # Ergebnisse extrahieren
    phi1 = float(model.params[1])
    phi1_se = float(model.bse[1])
    phi1_pval = float(model.pvalues[1])
    c = float(model.params[0])
    r_squared = float(model.rsquared)

    result = {
        "phi1": phi1,
        "phi1_se": phi1_se,
        "phi1_pval": phi1_pval,
        "c": c,
        "r_squared": r_squared,
        "sigma_diff": sigma,
        "n_obs": n_obs,
    }

    # AR(2)-Koeffizient wenn vorhanden
    if ar_lags >= 2:
        result["phi2"] = float(model.params[2])
        result["phi2_se"] = float(model.bse[2])
        result["phi2_pval"] = float(model.pvalues[2])

    # Half-Life
    if diff_order == 0 and 0 < phi1 < 1:
        # Auf Levels: HL = log(0.5) / log(φ₁) → Quartale bis 50% Mean-Reversion
        result["half_life"] = float(np.log(0.5) / np.log(phi1))
    elif diff_order > 0 and -1 < phi1 < 0:
        # Auf Diffs: HL = log(0.5) / log(|φ₁|) → wie schnell die Korrektur abklingt
        result["half_life"] = float(np.log(0.5) / np.log(abs(phi1)))
    else:
        result["half_life"] = np.nan

    return result


# Legacy-Wrapper für Abwärtskompatibilität
def _fit_ar1_on_diff(series: pd.Series) -> dict | None:
    """Schätzt AR(1) auf 1. Differenzen. Wrapper um _fit_ar()."""
    return _fit_ar(series, diff_order=DIFF_ORDER, ar_lags=AR_ORDER)


# ─────────────────────────────────────────────
# Multi-Model-Schätzung für gesamtes Panel
# ─────────────────────────────────────────────
def estimate_ar_features_multimodel(
    panel: pd.DataFrame,
    specs: list[ModelSpec] | None = None,
) -> pd.DataFrame:
    """Schätzt AR-Modelle für alle Ticker × Kennzahlen × Modellvarianten.

    Args:
        panel: DataFrame mit Spalten [ticker, quarter, <RATIO_NAMES>].
        specs: Liste von ModelSpec-Objekten. Default: MODEL_SPECS aus config.

    Returns:
        Feature-Matrix mit Spalte 'model' zur Unterscheidung der Varianten.
    """
    if specs is None:
        specs = MODEL_SPECS

    results: list[dict] = []
    tickers = sorted(panel["ticker"].unique())
    n_tickers = len(tickers)

    for spec in specs:
        logger.info("Modell '%s' (%s): diff_order=%d, ar_lags=%d, seasonal_diff=%d ...",
                     spec.name, spec.label, spec.diff_order, spec.ar_lags,
                     getattr(spec, "seasonal_diff", 0))
        count = 0

        for ticker in tickers:
            df_t = panel[panel["ticker"] == ticker].set_index("quarter").sort_index()

            for ratio in RATIO_NAMES:
                series = df_t[ratio].copy()

                seas = getattr(spec, "seasonal_diff", 0)
                n_valid = series.notna().sum()
                # Mindest-Beobachtungszahl: ar_lags + diff_order + seasonal_diff + 3 (Sicherheitspuffer)
                if n_valid < spec.ar_lags + spec.diff_order + seas + 3:
                    continue

                fit = _fit_ar(
                    series,
                    diff_order=spec.diff_order,
                    ar_lags=spec.ar_lags,
                    seasonal_diff=seas,
                )
                if fit is None:
                    continue

                results.append({
                    "model": spec.name,
                    "ticker": ticker,
                    "ratio": ratio,
                    **fit,
                })
                count += 1

        logger.info("  → %d Schätzungen (%d Ticker)", count, n_tickers)

    features = pd.DataFrame(results)
    return features


# Legacy-Wrapper
def estimate_ar_features(panel: pd.DataFrame) -> pd.DataFrame:
    """Schätzt nur die primäre Modellvariante (diff1). Abwärtskompatibel."""
    primary = [s for s in MODEL_SPECS if s.is_primary]
    if not primary:
        primary = [MODEL_SPECS[0]]
    df = estimate_ar_features_multimodel(panel, specs=primary)
    # Spalte 'model' entfernen für Kompatibilität mit bestehendem Code
    if "model" in df.columns:
        df = df.drop(columns=["model"])
    return df


# ─────────────────────────────────────────────
# Zusammenfassung pro Kennzahl (+ Modell)
# ─────────────────────────────────────────────
def summarize_by_ratio(features: pd.DataFrame) -> pd.DataFrame:
    """Deskriptive Statistik der AR-Parameter, gruppiert nach Kennzahl (und Modell)."""
    group_cols = ["ratio"]
    if "model" in features.columns:
        group_cols = ["model", "ratio"]

    summary = (
        features
        .groupby(group_cols)
        .agg(
            n=("phi1", "count"),
            phi1_mean=("phi1", "mean"),
            phi1_median=("phi1", "median"),
            phi1_std=("phi1", "std"),
            phi1_signif_pct=("phi1_pval", lambda s: (s < 0.05).mean() * 100),
            sigma_mean=("sigma_diff", "mean"),
            sigma_median=("sigma_diff", "median"),
            r2_median=("r_squared", "median"),
            hl_median=("half_life", "median"),
        )
        .round(4)
    )
    return summary


# ─────────────────────────────────────────────
# Thesis-Tabelle: Modellvarianten-Vergleich (Kap. 3.4.1)
# ─────────────────────────────────────────────
def build_thesis_table_modellvarianten(summary: pd.DataFrame, out_dir) -> None:
    """Baut die Vergleichs-Tabelle der vier Modellvarianten fuer Kap. 3.4.1.

    Format: Zeilen = 7 Hauptkennzahlen, Spalten = phi-1-Median und R-Quadrat-
    Median pro Modell (8 Datenspalten + Kennzahl-Spalte).

    Output:
      - thesis_table_modellvarianten.xlsx (Word-faehig)
      - thesis_table_modellvarianten.md   (Markdown, copy-paste)
    """
    # 7 Hauptkennzahlen in fester Thesis-Reihenfolge (Profitabilitaet -> Liquiditaet -> Kapitalstruktur)
    main_ratios_order = [
        "ROA", "ROE", "EBIT_margin", "fcf_margin",
        "current_ratio", "debt_to_equity", "equity_ratio",
    ]
    ratio_labels = {
        "ROA": "ROA",
        "ROE": "ROE",
        "EBIT_margin": "EBIT-Marge",
        "fcf_margin": "FCF-Marge",
        "current_ratio": "Current Ratio",
        "debt_to_equity": "Debt/Equity",
        "equity_ratio": "Eigenkapitalquote",
    }

    # Modell-Reihenfolge: Hauptmodell zuerst, dann die vier Robustheits-Vergleiche
    model_order = ["diff1", "ar2_diff1", "levels", "diff4", "diff1_diff4"]
    model_labels = {
        "diff1": "diff1",
        "ar2_diff1": "AR(2)",
        "levels": "Levels",
        "diff4": "Δ₄Y",
        "diff1_diff4": "Δ₁Δ₄Y",
    }

    # summary hat MultiIndex (model, ratio). Reset zum Filtern.
    df = summary.reset_index()
    df = df[df["ratio"].isin(main_ratios_order)]
    df = df[df["model"].isin(model_order)]

    # Pivot pro Kennzahl: phi und R-Quadrat pro Modell nebeneinander
    rows: list[dict] = []
    for ratio in main_ratios_order:
        row: dict = {"Kennzahl": ratio_labels[ratio]}
        sub = df[df["ratio"] == ratio]
        for model in model_order:
            cell = sub[sub["model"] == model]
            phi = cell["phi1_median"].values
            r2 = cell["r2_median"].values
            row[f"φ₁ {model_labels[model]}"] = round(float(phi[0]), 2) if len(phi) else None
            row[f"R² {model_labels[model]}"] = round(float(r2[0]), 2) if len(r2) else None
        rows.append(row)

    table = pd.DataFrame(rows)

    # XLSX-Output
    out_xlsx = out_dir / "thesis_table_modellvarianten.xlsx"
    try:
        table.to_excel(out_xlsx, index=False)
        logger.info("Thesis-Tabelle Modellvarianten (XLSX): %s", out_xlsx)
    except Exception as exc:
        logger.warning("XLSX-Export fehlgeschlagen (openpyxl?): %s", exc)

    # Markdown-Output (für direktes Copy-Paste in Word/Doc)
    md_lines: list[str] = []
    md_lines.append("# Tabelle 3.4.1 — φ₁- und R²-Mediane unter den fünf Modellvarianten")
    md_lines.append("")
    md_lines.append("Pro Kennzahl: φ₁-Median und R²-Median unter den fünf Spezifikationen "
                    "(diff1 = AR(1) auf 1. Differenzen / Hauptmodell; AR(2) = AR(2) auf 1. Differenzen; "
                    "Levels = AR(1) auf Niveaus; Δ₄Y = AR(1) auf saisonalen Differenzen; "
                    "Δ₁Δ₄Y = AR(1) auf saisonbereinigten 1. Differenzen).")
    md_lines.append("")
    md_lines.append("Quelle: `output/ar/ar_summary_by_model_ratio.csv`")
    md_lines.append("")
    md_lines.append("| " + " | ".join(table.columns) + " |")
    md_lines.append("|" + "|".join(["---"] * len(table.columns)) + "|")
    for _, row in table.iterrows():
        cells = [str(row["Kennzahl"])]
        for col in table.columns[1:]:
            val = row[col]
            if val is None or (isinstance(val, float) and np.isnan(val)):
                cells.append("")
            elif col.startswith("φ₁"):
                # phi-Werte mit Vorzeichen, Minus als typografisch korrektes Zeichen
                cells.append(f"{val:+.2f}".replace("-", "−"))
            else:
                cells.append(f"{val:.2f}")
        md_lines.append("| " + " | ".join(cells) + " |")

    out_md = out_dir / "thesis_table_modellvarianten.md"
    out_md.write_text("\n".join(md_lines), encoding="utf-8")
    logger.info("Thesis-Tabelle Modellvarianten (MD): %s", out_md)


# ─────────────────────────────────────────────
# Dimensionsunabhaengigkeit: phi1-sigma-Spearman + Thesis-Tabelle (Kap. 3.4.3)
# ─────────────────────────────────────────────
def compute_phi1_sigma_correlation(features_primary: pd.DataFrame, out_dir) -> pd.DataFrame:
    """Berechnet pro Hauptkennzahl die Pearson- und Spearman-Korrelation zwischen phi-1 und sigma(ΔY)
    auf der Hauptmodell-Schaetzung (diff1).

    Beschraenkt sich bewusst auf die sieben Hauptkennzahlen (ROA, ROE, EBIT-Marge, FCF-Marge,
    Current Ratio, Debt/Equity, Eigenkapitalquote). Vergleichskennzahlen (Quick Ratio, CCC,
    Net Debt/EBITDA) werden nicht aufgenommen, weil sie in 3.4.3 nicht Gegenstand der Pruefung
    sind und die Bonferroni-Korrektur (alpha/7) sich auf genau diese sieben Tests bezieht.

    Speichert das Ergebnis als output/ar/phi1_sigma_correlation.csv mit Spalten
    ratio, n, r_pearson, p_pearson, r_spearman, p_spearman, r_spearman_log, p_spearman_log.

    Returns:
        DataFrame mit den Korrelationsergebnissen pro Hauptkennzahl.
    """
    from scipy import stats

    main_ratios = {"ROA", "ROE", "EBIT_margin", "fcf_margin",
                   "current_ratio", "debt_to_equity", "equity_ratio"}

    rows: list[dict] = []
    for ratio in features_primary["ratio"].unique():
        if ratio not in main_ratios:
            continue
        sub = features_primary[features_primary["ratio"] == ratio].copy()
        sub = sub.dropna(subset=["phi1", "sigma_diff"])
        if len(sub) < 10:
            continue
        x = sub["phi1"].values
        y = sub["sigma_diff"].values
        # Pearson
        r_p, p_p = stats.pearsonr(x, y)
        # Spearman
        r_s, p_s = stats.spearmanr(x, y)
        # Spearman auf log(sigma) — invariant unter monotoner Transformation, daher identisch
        # mit r_spearman; wird zur Konsistenz mit bestehendem CSV-Format mitgeschrieben.
        rows.append({
            "ratio": _ratio_display(ratio),
            "n": len(sub),
            "r_pearson": float(r_p),
            "p_pearson": float(p_p),
            "r_spearman": float(r_s),
            "p_spearman": float(p_s),
            "r_spearman_log": float(r_s),
            "p_spearman_log": float(p_s),
        })

    corr_df = pd.DataFrame(rows)
    out_csv = out_dir / "phi1_sigma_correlation.csv"
    corr_df.to_csv(out_csv, index=False)
    logger.info(f"Spearman/Pearson φ-σ-Korrelation: {out_csv}")
    return corr_df


def _ratio_display(ratio: str) -> str:
    """Mappt interne Ratio-Namen auf die im CSV erwarteten Anzeigenamen."""
    mapping = {
        "EBIT_margin": "EBIT-M.",
        "fcf_margin": "FCF-M.",
        "current_ratio": "CR",
        "debt_to_equity": "D/E",
        "equity_ratio": "EQ-R.",
    }
    return mapping.get(ratio, ratio)


def build_thesis_table_dimension(corr_df: pd.DataFrame, out_dir) -> None:
    """Baut die Spearman-Korrelations-Tabelle phi-1 × sigma(ΔY) fuer Kap. 3.4.3.

    Format: Zeilen = 7 Hauptkennzahlen, Spalten = n, rho_Spearman, p-Wert,
    Signifikanz-Markierung bei alpha = 0.05 (5 Spalten inkl. Kennzahl).

    Standard-Signifikanzschwelle alpha = 0.05. Eine Bonferroni-Korrektur ist hier nicht noetig,
    weil die p-Werte entweder klar unter oder klar ueber jeder ueblichen Schwelle liegen.

    Output:
      - thesis_table_dimensionsunabhaengigkeit.xlsx (Word-faehig)
      - thesis_table_dimensionsunabhaengigkeit.md   (Markdown, copy-paste)
    """
    main_ratios_order_display = [
        "ROA", "ROE", "EBIT-M.", "FCF-M.", "CR", "D/E", "EQ-R.",
    ]
    ratio_labels = {
        "ROA": "ROA",
        "ROE": "ROE",
        "EBIT-M.": "EBIT-Marge",
        "FCF-M.": "FCF-Marge",
        "CR": "Current Ratio",
        "D/E": "Debt/Equity",
        "EQ-R.": "Eigenkapitalquote",
    }

    rows: list[dict] = []
    for ratio_key in main_ratios_order_display:
        sub = corr_df[corr_df["ratio"] == ratio_key]
        if len(sub) == 0:
            continue
        cell = sub.iloc[0]
        rho = float(cell["r_spearman"])
        rows.append({
            "Kennzahl": ratio_labels[ratio_key],
            "n": int(cell["n"]),
            "ρ (Spearman)": round(rho, 3),
            "ρ²": round(rho ** 2, 3),
            "p": float(cell["p_spearman"]),
        })

    table = pd.DataFrame(rows)

    # XLSX
    out_xlsx = out_dir / "thesis_table_dimensionsunabhaengigkeit.xlsx"
    try:
        table.to_excel(out_xlsx, index=False)
        logger.info(f"Thesis-Tabelle Dimensionsunabhaengigkeit (XLSX): {out_xlsx}")
    except Exception as exc:
        logger.warning(f"XLSX-Export fehlgeschlagen: {exc}")

    # Markdown
    md_lines: list[str] = []
    md_lines.append("# Tabelle 3.4.3 — Spearman-Rangkorrelation φ₁ × σ(ΔY) pro Kennzahl")
    md_lines.append("")
    md_lines.append("Ein negatives ρ entspricht der mechanischen Kopplungs-Hypothese (höhere σ → "
                    "negativeres φ₁). ρ² gibt den Anteil der gemeinsamen Variation an, der durch "
                    "die Korrelation erklärt wird. Signifikanzschwelle: p < 0,05.")
    md_lines.append("")
    md_lines.append("Quelle: `output/ar/phi1_sigma_correlation.csv`")
    md_lines.append("")
    md_lines.append("| Kennzahl | n | ρ (Spearman) | ρ² | p |")
    md_lines.append("|---|---|---|---|---|")
    for _, row in table.iterrows():
        rho_val = row["ρ (Spearman)"]
        rho_str = f"{rho_val:+.3f}".replace("-", "−")
        r2_val = row["ρ²"]
        r2_str = f"{r2_val:.3f}"
        p_val = row["p"]
        if p_val < 0.001:
            p_str = f"{p_val:.1e}"
        else:
            p_str = f"{p_val:.3f}"
        md_lines.append(f"| {row['Kennzahl']} | {row['n']} | {rho_str} | {r2_str} | {p_str} |")

    out_md = out_dir / "thesis_table_dimensionsunabhaengigkeit.md"
    out_md.write_text("\n".join(md_lines), encoding="utf-8")
    logger.info(f"Thesis-Tabelle Dimensionsunabhaengigkeit (MD): {out_md}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    ensure_output_dirs()

    # Panel laden
    panel = pd.read_csv(OUT_AR.parent / "ratios" / "ratio_panel.csv")
    logger.info("Panel geladen: %d Zeilen, %d Ticker",
                len(panel), panel["ticker"].nunique())

    # ── Multi-Model-Schätzung ──
    features_all = estimate_ar_features_multimodel(panel)

    # Gesamte Feature-Matrix speichern (alle Modelle)
    out_all = OUT_AR / "ar_features_all.csv"
    features_all.to_csv(out_all, index=False)
    logger.info("Alle Modelle: %s (%d Zeilen)", out_all, len(features_all))

    # Primäres Modell separat speichern (Abwärtskompatibilität)
    primary_name = next((s.name for s in MODEL_SPECS if s.is_primary), MODEL_SPECS[0].name)
    features_primary = features_all[features_all["model"] == primary_name].drop(columns=["model"])
    out_detail = OUT_AR / "ar_features.csv"
    features_primary.to_csv(out_detail, index=False)
    logger.info("Primäres Modell (%s): %s (%d Zeilen)", primary_name, out_detail, len(features_primary))

    # Zusammenfassung
    summary = summarize_by_ratio(features_all)
    out_summary = OUT_AR / "ar_summary_by_model_ratio.csv"
    summary.to_csv(out_summary)
    logger.info("Zusammenfassung: %s", out_summary)

    # Thesis-Tabelle fuer Kap. 3.4.1 (XLSX + Markdown)
    build_thesis_table_modellvarianten(summary, OUT_AR)

    # Dimensionsunabhaengigkeit fuer Kap. 3.4.3:
    # phi1-sigma-Spearman-Korrelation auf Hauptmodell + Thesis-Tabelle
    corr_df = compute_phi1_sigma_correlation(features_primary, OUT_AR)
    build_thesis_table_dimension(corr_df, OUT_AR)

    # Print
    for spec in MODEL_SPECS:
        sub = features_all[features_all["model"] == spec.name]
        n_est = len(sub)
        n_tick = sub["ticker"].nunique()
        print(f"\n{'='*70}")
        print(f"  {spec.label}")
        print(f"  {n_tick} Ticker, {n_est} Schätzungen")
        print(f"{'='*70}")
        sub_summary = summarize_by_ratio(sub.drop(columns=["model"]))
        print(sub_summary.to_string())
