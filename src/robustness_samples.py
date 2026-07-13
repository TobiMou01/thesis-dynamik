"""
robustness_samples.py – Robustheitsanalysen für variable Stichproben
=====================================================================
Teil 2 des Arbeitsplans:
  2.1  Variable Completeness-Filter (60Q, 40Q statt 100Q)
  2.2  Financial Services als separate Kohorte
  2.3  Vergleichstabelle der φ₁-Mediane

Erzeugt:
  output/robustness/sample_comparison.csv   – φ₁-Mediane pro Sample × Ratio
  output/robustness/financial_services.csv  – AR-Features nur Financial Services
  output/robustness/sample_ticker_counts.csv – Ticker-Anzahlen pro Sample
  output/robustness/robustness_summary.md   – Zusammenfassung als Markdown
"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Projektpfad
PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))

from config import (
    RAW_BALANCE, RAW_CASHFLOW, RAW_INCOME, RAW_PROFILE,
    YEAR_START, YEAR_END, EXPECTED_QUARTERS,
    EXCLUDED_SECTORS, PROFILE_SECTOR_COL, ADR_NAME_KEYWORDS,
    RATIOS, RATIO_NAMES, RAW_COLS,
    OUTLIER_WINDOW_SIZE, OUTLIER_SIGMA, OUTLIER_MIN_FLAGS,
    OUTLIER_MIN_RATIO, OUTLIER_CORRECTION,
    NAN_MAX_QUARTERS, WINSORIZE_QUANTILES,
    OUTPUT_DIR, SRC_DIRS, MODEL_SPECS,
)
from load_data import (
    get_ticker_universe, _load_profiles, filter_sectors, filter_adrs,
    _load_source, _build_expected_quarters, _merge_raw_values,
    _clean_raw_panel, _filter_nan_tickers, _compute_ratios_from_raw,
    _winsorize_ratios,
)
from ar_model import _fit_ar

logger = logging.getLogger(__name__)

# Output
OUT_ROBUST = OUTPUT_DIR / "robustness"
OUT_ROBUST.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# Hilfsfunktionen
# ─────────────────────────────────────────────

def _count_available_quarters(ticker: str) -> int | None:
    """Zählt, wie viele Quartale (Schnittmenge über 3 Quellen) ein Ticker hat."""
    all_qtrs = None
    for src_name in ("income", "balance", "cashflow"):
        df = _load_source(ticker, src_name)
        if df is None:
            return None
        qtrs = set(df.index.astype(str))
        all_qtrs = qtrs if all_qtrs is None else all_qtrs & qtrs
    return len(all_qtrs) if all_qtrs else 0


def _build_panel_variable_completeness(
    tickers: list[str],
    min_quarters: int,
    profiles: dict,
) -> pd.DataFrame | None:
    """Baut ein Ratio-Panel mit variablem Completeness-Filter.

    Statt 100Q lückenlos wird hier geprüft:
    - Schnittmenge der Quartale über 3 Quellen >= min_quarters
    - Quartale innerhalb 2000-2024

    WICHTIG: Identische Aufbereitungslogik wie build_ratio_panel() in load_data.py:
    - Gleiche Outlier-Detection (Rolling-Window, gleiche Parameter aus config.py)
    - Gleicher NaN-Qualitätsfilter (NAN_MAX_QUARTERS)
    - Gleiche Winsorize-Quantile (WINSORIZE_QUANTILES)
    Einziger Unterschied: min_quarters statt fixer 100Q.
    """
    expected_qtr_index = _build_expected_quarters()

    complete_tickers = []
    all_raw = []

    for ticker in tickers:
        sources = {
            "income": _load_source(ticker, "income"),
            "balance": _load_source(ticker, "balance"),
            "cashflow": _load_source(ticker, "cashflow"),
        }
        if any(v is None for v in sources.values()):
            continue

        # Schnittmenge der verfügbaren Quartale
        common_qtrs = set(sources["income"].index)
        for src in ("balance", "cashflow"):
            common_qtrs &= set(sources[src].index)

        # Nur Quartale innerhalb des erwarteten Zeitraums
        valid_qtrs = common_qtrs & set(expected_qtr_index)

        if len(valid_qtrs) < min_quarters:
            continue

        # Auf gemeinsame Quartale filtern
        valid_idx = pd.PeriodIndex(sorted(valid_qtrs))
        for src_name in sources:
            sources[src_name] = sources[src_name].loc[
                sources[src_name].index.isin(valid_idx)
            ]

        raw_row = _merge_raw_values(sources)
        raw_row["ticker"] = ticker
        complete_tickers.append(ticker)
        all_raw.append(raw_row)

    if not all_raw:
        return None

    logger.info("Variable Filter (%dQ): %d / %d Ticker",
                min_quarters, len(complete_tickers), len(tickers))

    raw_panel = pd.concat(all_raw, ignore_index=False)
    raw_panel = raw_panel.reset_index()
    raw_panel["quarter"] = raw_panel["quarter"].astype(str)
    raw_panel = raw_panel.sort_values(["ticker", "quarter"]).reset_index(drop=True)

    # Outlier Detection – identisch zur Hauptpipeline (config-Parameter)
    raw_panel, _ = _clean_raw_panel(raw_panel)

    # NaN-Filter – identisch zur Hauptpipeline
    raw_panel, _ = _filter_nan_tickers(raw_panel)

    # Kennzahlen berechnen
    raw_panel = _compute_ratios_from_raw(raw_panel)
    raw_panel = _winsorize_ratios(raw_panel)

    panel = raw_panel[["ticker", "quarter"] + RATIO_NAMES]
    return panel


def _estimate_ar_for_panel(panel: pd.DataFrame, model_name: str = "diff1") -> pd.DataFrame:
    """Schätzt AR(1) auf 1. Differenzen für ein Panel.

    Gibt ein DataFrame mit ticker, ratio, phi1, sigma_diff, r_squared, n_obs zurück.
    """
    # Finde den passenden ModelSpec
    spec = next(s for s in MODEL_SPECS if s.name == model_name)

    results = []
    for ticker in panel["ticker"].unique():
        sub = panel[panel["ticker"] == ticker].sort_values("quarter")
        for ratio_name in RATIO_NAMES:
            series = sub[ratio_name].values.astype(float)
            series = pd.Series(series)
            fit = _fit_ar(series, diff_order=spec.diff_order, ar_lags=spec.ar_lags)
            if fit is not None:
                fit["ticker"] = ticker
                fit["ratio"] = ratio_name
                results.append(fit)

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    return df


# ─────────────────────────────────────────────
# 2.1: Variable Completeness
# ─────────────────────────────────────────────

def run_variable_completeness():
    """Erzeugt AR-Features für verschiedene Completeness-Schwellen."""
    logger.info("=" * 60)
    logger.info("Teil 2.1: Variable Completeness-Filter")
    logger.info("=" * 60)

    # Basis: Ticker nach Sektor- und ADR-Filter (wie Hauptpipeline)
    tickers = get_ticker_universe()
    profiles = _load_profiles()
    sector_map = {t: p["sector"] for t, p in profiles.items()}
    tickers = filter_sectors(tickers, sector_map)
    tickers = filter_adrs(tickers, profiles)

    configs = [
        {"label": "100Q (Hauptanalyse)", "min_q": 100},
        {"label": "80Q", "min_q": 80},
        {"label": "60Q", "min_q": 60},
        {"label": "40Q", "min_q": 40},
    ]

    all_results = []
    ticker_counts = []

    for cfg in configs:
        label = cfg["label"]
        min_q = cfg["min_q"]
        logger.info(f"\n--- {label} (min_quarters={min_q}) ---")

        if min_q == 100:
            # Nutze existierende Hauptanalyse
            panel_path = OUTPUT_DIR / "ratios" / "ratio_panel.csv"
            panel = pd.read_csv(panel_path)
            ar_path = OUTPUT_DIR / "ar" / "ar_features.csv"
            ar_feats = pd.read_csv(ar_path)
        else:
            panel = _build_panel_variable_completeness(tickers, min_q, profiles)
            if panel is None or panel.empty:
                logger.warning(f"Kein Panel für {label}")
                continue
            ar_feats = _estimate_ar_for_panel(panel, model_name="diff1")

        n_tickers = panel["ticker"].nunique() if panel is not None else 0
        n_ar = len(ar_feats)
        logger.info(f"  {label}: {n_tickers} Ticker, {n_ar} AR-Schätzungen")

        ticker_counts.append({
            "sample": label,
            "min_quarters": min_q,
            "n_tickers": n_tickers,
            "n_ar_estimates": n_ar,
        })

        # φ₁-Mediane pro Ratio
        for ratio_name in RATIO_NAMES:
            sub = ar_feats[ar_feats["ratio"] == ratio_name]
            if sub.empty:
                continue
            all_results.append({
                "sample": label,
                "min_quarters": min_q,
                "ratio": ratio_name,
                "n": len(sub),
                "phi1_median": sub["phi1"].median(),
                "phi1_mean": sub["phi1"].mean(),
                "phi1_std": sub["phi1"].std(),
                "sigma_median": sub["sigma_diff"].median(),
                "r2_median": sub["r_squared"].median(),
                "signif_pct": (sub["phi1_pval"] < 0.05).mean() * 100,
            })

    comparison = pd.DataFrame(all_results).round(4)
    comparison.to_csv(OUT_ROBUST / "sample_comparison.csv", index=False)

    counts_df = pd.DataFrame(ticker_counts)
    counts_df.to_csv(OUT_ROBUST / "sample_ticker_counts.csv", index=False)

    logger.info(f"\n✓ Gespeichert: {OUT_ROBUST / 'sample_comparison.csv'}")

    # Thesis-Tabelle fuer Kap. 3.4.2 (XLSX + Markdown)
    build_thesis_table_stichproben(comparison, OUT_ROBUST)

    return comparison, counts_df


# ─────────────────────────────────────────────
# Thesis-Tabelle: Stichprobenrobustheit (Kap. 3.4.2)
# ─────────────────────────────────────────────
def build_thesis_table_stichproben(comparison: pd.DataFrame, out_dir) -> None:
    """Baut die Vergleichs-Tabelle der vier Stichproben fuer Kap. 3.4.2.

    Format: Zeilen = 7 Hauptkennzahlen, Spalten = phi-1-Median pro Stichprobe
    (4 Stichproben + Kennzahl-Spalte = 5 Spalten).

    Output:
      - thesis_table_stichproben.xlsx (Word-faehig)
      - thesis_table_stichproben.md   (Markdown, copy-paste)
    """
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

    sample_order = ["100Q (Hauptanalyse)", "80Q", "60Q", "40Q"]
    sample_labels = {
        "100Q (Hauptanalyse)": "100Q",
        "80Q": "80Q",
        "60Q": "60Q",
        "40Q": "40Q",
    }

    df = comparison.copy()
    df = df[df["ratio"].isin(main_ratios_order)]
    df = df[df["sample"].isin(sample_order)]

    rows: list[dict] = []
    for ratio in main_ratios_order:
        row: dict = {"Kennzahl": ratio_labels[ratio]}
        sub = df[df["ratio"] == ratio]
        for sample in sample_order:
            cell = sub[sub["sample"] == sample]
            if len(cell):
                row[f"φ₁ {sample_labels[sample]}"] = round(float(cell["phi1_median"].iloc[0]), 2)
            else:
                row[f"φ₁ {sample_labels[sample]}"] = None
        rows.append(row)

    table = pd.DataFrame(rows)

    # XLSX
    out_xlsx = out_dir / "thesis_table_stichproben.xlsx"
    try:
        table.to_excel(out_xlsx, index=False)
        logger.info(f"Thesis-Tabelle Stichproben (XLSX): {out_xlsx}")
    except Exception as exc:
        logger.warning(f"XLSX-Export fehlgeschlagen (openpyxl?): {exc}")

    # Markdown (fuer Copy-Paste in Word/Doc)
    md_lines: list[str] = []
    md_lines.append("# Tabelle 3.4.2 — φ₁-Mediane unter den vier Stichproben")
    md_lines.append("")
    md_lines.append("Pro Kennzahl: φ₁-Median unter unterschiedlichen Mindest-Quartalsanforderungen "
                    "(100Q = Hauptanalyse mit 932 Unternehmen, 80Q mit 1.231, 60Q mit 1.855, "
                    "40Q mit 2.356 Unternehmen).")
    md_lines.append("")
    md_lines.append("Quelle: `output/robustness/sample_comparison.csv`")
    md_lines.append("")
    md_lines.append("| " + " | ".join(table.columns) + " |")
    md_lines.append("|" + "|".join(["---"] * len(table.columns)) + "|")
    for _, row in table.iterrows():
        cells = [str(row["Kennzahl"])]
        for col in table.columns[1:]:
            val = row[col]
            if val is None or (isinstance(val, float) and np.isnan(val)):
                cells.append("")
            else:
                cells.append(f"{val:+.2f}".replace("-", "−"))
        md_lines.append("| " + " | ".join(cells) + " |")

    out_md = out_dir / "thesis_table_stichproben.md"
    out_md.write_text("\n".join(md_lines), encoding="utf-8")
    logger.info(f"Thesis-Tabelle Stichproben (MD): {out_md}")


# ─────────────────────────────────────────────
# 2.2: Financial Services Robustheitscheck
# ─────────────────────────────────────────────

def run_financial_services():
    """Separate Pipeline-Run nur für Financial Services Ticker."""
    logger.info("=" * 60)
    logger.info("Teil 2.2: Financial Services Robustheitscheck")
    logger.info("=" * 60)

    tickers = get_ticker_universe()
    profiles = _load_profiles()
    sector_map = {t: p["sector"] for t, p in profiles.items()}

    # NUR Financial Services, Banks, Insurance
    fin_sectors = {"Financial Services", "Banks", "Insurance"}
    fin_tickers = [t for t in tickers if sector_map.get(t, "") in fin_sectors]

    # ADR-Filter weiterhin anwenden
    fin_tickers = filter_adrs(fin_tickers, profiles)
    logger.info(f"Financial Services Ticker nach ADR-Filter: {len(fin_tickers)}")

    # Variable Completeness: 60Q (damit genug Ticker übrig bleiben)
    configs = [
        {"label": "FinServ_100Q", "min_q": 100},
        {"label": "FinServ_60Q", "min_q": 60},
    ]

    all_results = []
    for cfg in configs:
        label = cfg["label"]
        min_q = cfg["min_q"]
        logger.info(f"\n--- {label} ---")

        panel = _build_panel_variable_completeness(fin_tickers, min_q, profiles)
        if panel is None or panel.empty:
            logger.warning(f"Kein Panel für {label}")
            continue

        n_tickers = panel["ticker"].nunique()
        ar_feats = _estimate_ar_for_panel(panel, model_name="diff1")
        logger.info(f"  {label}: {n_tickers} Ticker, {len(ar_feats)} AR-Schätzungen")

        # Speichere AR-Features separat
        ar_feats["sample"] = label
        all_results.append(ar_feats)

    if all_results:
        fin_ar = pd.concat(all_results, ignore_index=True)
        fin_ar.to_csv(OUT_ROBUST / "financial_services.csv", index=False)
        logger.info(f"\n✓ Gespeichert: {OUT_ROBUST / 'financial_services.csv'}")
        return fin_ar
    return pd.DataFrame()


# ─────────────────────────────────────────────
# 2.3: Summary-Report
# ─────────────────────────────────────────────

def write_summary(comparison, counts_df, fin_ar):
    """Schreibt eine Markdown-Zusammenfassung der Robustheitsanalysen."""
    logger.info("Schreibe Zusammenfassung...")

    lines = [
        "# Robustheitsanalyse: Variable Stichproben",
        "",
        "## 1. Ticker-Anzahlen pro Sample",
        "",
    ]

    if not counts_df.empty:
        lines.append("| Sample | Min. Quartale | Ticker | AR-Schätzungen |")
        lines.append("|--------|:---:|:---:|:---:|")
        for _, row in counts_df.iterrows():
            lines.append(f"| {row['sample']} | {row['min_quarters']} | {row['n_tickers']:,} | {row['n_ar_estimates']:,} |")
        lines.append("")

    lines.append("## 2. φ₁-Mediane: Stabilität über Stichproben")
    lines.append("")

    if not comparison.empty:
        # Pivot: Ratio × Sample
        pivot = comparison.pivot_table(
            index="ratio", columns="sample", values="phi1_median", sort=False
        )
        # Sortierung nach Ratio-Reihenfolge
        pivot = pivot.reindex([r for r in RATIO_NAMES if r in pivot.index])

        lines.append("| Kennzahl | " + " | ".join(pivot.columns) + " |")
        lines.append("|----------|" + "|".join([":---:" for _ in pivot.columns]) + "|")
        for ratio in pivot.index:
            vals = [f"{pivot.loc[ratio, c]:.3f}" if pd.notna(pivot.loc[ratio, c]) else "–" for c in pivot.columns]
            lines.append(f"| {ratio} | " + " | ".join(vals) + " |")
        lines.append("")

        # Interpretation
        lines.append("**Interpretation:** Wenn die φ₁-Mediane über alle Samples stabil bleiben,")
        lines.append("spricht das gegen einen Survivorship Bias im Vollständigkeitsfilter.")
        lines.append("Große Abweichungen bei 40Q/60Q deuten auf Selektionseffekte hin.")
        lines.append("")

    # Financial Services
    if not fin_ar.empty:
        lines.append("## 3. Financial Services Robustheitscheck")
        lines.append("")

        for sample_label in fin_ar["sample"].unique():
            sub = fin_ar[fin_ar["sample"] == sample_label]
            n_tickers = sub["ticker"].nunique()
            lines.append(f"### {sample_label} ({n_tickers} Ticker)")
            lines.append("")

            summary = sub.groupby("ratio").agg(
                phi1_med=("phi1", "median"),
                sigma_med=("sigma_diff", "median"),
                r2_med=("r_squared", "median"),
            ).round(4)

            lines.append("| Kennzahl | φ₁ Median | σ(ΔY) Median | R² Median |")
            lines.append("|----------|:---------:|:------------:|:---------:|")
            for ratio in RATIO_NAMES:
                if ratio in summary.index:
                    r = summary.loc[ratio]
                    lines.append(f"| {ratio} | {r['phi1_med']:.3f} | {r['sigma_med']:.4f} | {r['r2_med']:.3f} |")
            lines.append("")

        lines.append("**Interpretation:** Financial Services zeigen erwartungsgemäß höhere")
        lines.append("Persistenz bei Bilanzstruktur-Kennzahlen (Leverage = Geschäftsmodell).")
        lines.append("Die Drei-Schichten-Hierarchie (Profitabilität > Liquidität > Kapitalstruktur)")
        lines.append("sollte dennoch erkennbar sein.")
        lines.append("")

    md_path = OUT_ROBUST / "robustness_summary.md"
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
    print("  Teil 2: Erweiterte Stichproben + Robustheit")
    print("=" * 60)

    # 2.1
    comparison, counts_df = run_variable_completeness()

    # 2.2
    fin_ar = run_financial_services()

    # 2.3
    write_summary(comparison, counts_df, fin_ar)

    print("\n" + "=" * 60)
    print("  Robustheitsanalyse abgeschlossen.")
    print(f"  Ergebnisse in: {OUT_ROBUST}")
    print("=" * 60)
