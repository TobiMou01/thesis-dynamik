"""
load_data.py – Rohdaten einlesen, bereinigen, Kennzahlen berechnen, Panel bauen
================================================================================
Workflow:
  1. Alle Ticker ermitteln (Schnittmenge der 3 Quell-Ordner)
  2. Sektor- und ADR-Filter (Finanzsektor + American Depositary Receipts)
  3. Pro Ticker: Bilanz, GuV und Cashflow einlesen, auf 2000–2024 filtern
  4. Vollständigkeitsfilter: nur Ticker mit exakt 100 Quartalen
  5. Rohwerte-Panel zusammenführen
  6. Rolling-Window Outlier Detection auf Rohwerten (vor Kennzahlenberechnung)
  7. NaN/Null-Qualitätsfilter: Ticker mit >10 fehlenden Quartalen entfernen
  8. Kennzahlen berechnen (Zähler / Nenner) aus bereinigten Rohwerten
  9. Winsorizing auf Kennzahlen (1%/99%-Perzentil)
 10. Ergebnis: ein Panel-DataFrame (ticker × quarter × ratio)
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from config import (
    RAW_BALANCE, RAW_CASHFLOW, RAW_INCOME, RAW_PROFILE,
    YEAR_START, YEAR_END, EXPECTED_QUARTERS,
    EXCLUDED_SECTORS, PROFILE_SECTOR_COL, ADR_NAME_KEYWORDS,
    RATIOS, RATIO_NAMES, RAW_COLS,
    OUTLIER_WINDOW_SIZE, OUTLIER_SIGMA, OUTLIER_MIN_FLAGS,
    OUTLIER_MIN_RATIO, OUTLIER_CORRECTION, CROSS_METRIC_PAIRS,
    OUTLIER_OVERRIDES_PATH, NAN_MAX_QUARTERS,
    WINSORIZE_QUANTILES,
    OUT_RATIOS, OUT_PREPROCESS, SRC_DIRS,
    ensure_output_dirs,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# 1. Ticker ermitteln
# ─────────────────────────────────────────────
def _csv_tickers(folder: Path) -> set[str]:
    """Gibt die Menge aller Ticker zurück, die als CSV in *folder* liegen."""
    return {p.stem for p in folder.glob("*.csv")}


def get_ticker_universe() -> list[str]:
    """Schnittmenge der Ticker über alle drei Quell-Ordner, sortiert."""
    sets = [_csv_tickers(d) for name, d in SRC_DIRS.items() if name != "profile"]
    common = sets[0].intersection(*sets[1:])
    logger.info("Ticker-Universum: %d (Schnittmenge aus %s)",
                len(common), [d.name for d in [RAW_BALANCE, RAW_INCOME, RAW_CASHFLOW]])
    return sorted(common)


# ─────────────────────────────────────────────
# 2. Sektor- und ADR-Filter
# ─────────────────────────────────────────────
def _load_profiles() -> dict[str, dict[str, str]]:
    """Liest alle Profil-CSVs und gibt {ticker: {sector, name}} zurück."""
    profiles: dict[str, dict[str, str]] = {}
    for csv_path in RAW_PROFILE.glob("*.csv"):
        try:
            df = pd.read_csv(csv_path, nrows=1)
            if len(df) == 0:
                continue
            ticker = df["symbol"].iloc[0] if "symbol" in df.columns else csv_path.stem
            profiles[ticker] = {
                "sector": str(df[PROFILE_SECTOR_COL].iloc[0]) if PROFILE_SECTOR_COL in df.columns else "",
                "name": str(df["name"].iloc[0]) if "name" in df.columns else "",
            }
        except Exception:
            pass
    return profiles


def load_sector_map() -> dict[str, str]:
    """Liest alle Profil-CSVs und gibt {ticker: sector} zurück."""
    return {t: p["sector"] for t, p in _load_profiles().items()}


def filter_sectors(tickers: list[str], sector_map: dict[str, str]) -> list[str]:
    """Entfernt Ticker, deren Sektor in EXCLUDED_SECTORS liegt."""
    kept = [t for t in tickers if sector_map.get(t, "") not in EXCLUDED_SECTORS]
    n_removed = len(tickers) - len(kept)
    logger.info("Sektor-Filter: %d entfernt, %d verbleibend", n_removed, len(kept))
    return kept


def filter_adrs(tickers: list[str], profiles: dict[str, dict[str, str]]) -> list[str]:
    """Entfernt ADRs (American Depositary Receipts) anhand des Profilnamens.

    Exklusion wenn der Name eines der ADR_NAME_KEYWORDS enthält.
    Begründung: ADRs bilden ausländische Unternehmen ab, die ggf. unter IFRS
    statt US-GAAP berichten und Doppelzählungen verursachen.
    """
    removed = []
    kept = []
    for t in tickers:
        name_upper = profiles.get(t, {}).get("name", "").upper()
        if any(kw in name_upper for kw in ADR_NAME_KEYWORDS):
            removed.append(t)
        else:
            kept.append(t)

    if removed:
        logger.info("ADR-Filter: %d entfernt, %d verbleibend", len(removed), len(kept))
    return kept


# ─────────────────────────────────────────────
# 3. Einzelne Quelle für einen Ticker laden
# ─────────────────────────────────────────────
def _load_source(ticker: str, src_name: str) -> pd.DataFrame | None:
    """Lädt eine CSV, filtert auf 2000–2024, indiziert auf Kalenderquartal.

    Gibt None zurück, wenn die Datei fehlt oder leer ist.
    Bei Quartalsduplikaten wird der jeweils letzte Eintrag behalten
    (spätestes Filing-Datum).
    """
    folder = SRC_DIRS[src_name]
    path = folder / f"{ticker}.csv"
    if not path.exists():
        return None

    df = pd.read_csv(path)
    if "date" not in df.columns or len(df) == 0:
        return None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Zeitraum filtern
    df = df[(df["date"].dt.year >= YEAR_START) & (df["date"].dt.year <= YEAR_END)]

    # Kalenderquartal als Index
    df["quarter"] = df["date"].dt.to_period("Q")

    # Bei Duplikaten: spätestes Datum behalten (= aktuellstes Filing)
    df = df.sort_values("date").drop_duplicates(subset=["quarter"], keep="last")
    df = df.set_index("quarter").sort_index()

    # Metadaten-Spalten entfernen
    drop_cols = [c for c in ("date", "filing_date", "currency_symbol", "symbol") if c in df.columns]
    df = df.drop(columns=drop_cols)

    # Alles numerisch erzwingen
    df = df.apply(pd.to_numeric, errors="coerce")

    return df


# ─────────────────────────────────────────────
# 4. Vollständigkeitsfilter
# ─────────────────────────────────────────────
def _build_expected_quarters() -> pd.PeriodIndex:
    """Gibt die 100 erwarteten Kalenderquartale Q1/2000 bis Q4/2024 zurück."""
    return pd.period_range(
        start=f"{YEAR_START}Q1",
        end=f"{YEAR_END}Q4",
        freq="Q",
    )


EXPECTED_QTR_INDEX = _build_expected_quarters()
assert len(EXPECTED_QTR_INDEX) == EXPECTED_QUARTERS, (
    f"Erwartete {EXPECTED_QUARTERS} Quartale, aber PeriodIndex hat {len(EXPECTED_QTR_INDEX)}"
)


def _is_complete(dfs: dict[str, pd.DataFrame]) -> bool:
    """Prüft, ob *alle* Quellen exakt die 100 erwarteten Quartale abdecken."""
    for src_name, df in dfs.items():
        if df is None:
            return False
        if not EXPECTED_QTR_INDEX.isin(df.index).all():
            return False
    return True


# ─────────────────────────────────────────────
# 5. Rohwerte zusammenführen (pro Ticker)
# ─────────────────────────────────────────────
# Ableitung: Welche RAW_COLS kommen aus welcher Quelle?
# Unterstützt sowohl simple Quotienten als auch Formel-Kennzahlen
# (s. RatioDef.iter_required_cols).
_SRC_TO_COLS: dict[str, list[str]] = {}
for _r in RATIOS:
    for _src, _col in _r.iter_required_cols():
        _SRC_TO_COLS.setdefault(_src, set()).add(_col)
_SRC_TO_COLS = {k: sorted(v) for k, v in _SRC_TO_COLS.items()}


def _merge_raw_values(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Führt die drei Quellen zu einem flachen Rohwerte-DataFrame zusammen.

    Rückgabe: DataFrame mit Index=quarter, Spalten=RAW_COLS.
    """
    parts = []
    for src_name in ("income", "balance", "cashflow"):
        cols = _SRC_TO_COLS.get(src_name, [])
        parts.append(sources[src_name].reindex(columns=cols))

    merged = pd.concat(parts, axis=1, join="outer").sort_index()
    return merged


# ─────────────────────────────────────────────
# 6. Rolling-Window Outlier Detection
# ─────────────────────────────────────────────
def _detect_and_correct_outliers(
    values: np.ndarray,
    window_size: int = 8,
    sigma: float = 3.0,
    min_flags: int = 3,
    min_ratio: float = 5.0,
    correction: str = "window_median",
) -> dict:
    """Erkennt und korrigiert Ausreißer per Multi-Window Rolling-Verfahren.

    Für jedes gleitende Fenster der Größe *window_size* werden MEDIAN und
    STDEV.P berechnet.  Ein Datenpunkt gilt als Ausreißer, wenn:
      (a) mindestens *min_flags* Fenster ihn als >*sigma*×Std markieren UND
      (b) |original / corrected| ≥ *min_ratio* (Mindest-Abweichungsfaktor).

    Returns:
        dict mit "is_outlier", "flag_counts", "corrected", "n_outliers".
    """
    n = len(values)
    flag_counts = np.zeros(n, dtype=int)
    # Pro Datenpunkt: alle Fenster-Mediane sammeln, die ihn flaggen
    window_medians: list[list[float]] = [[] for _ in range(n)]

    for t in range(window_size, n + 1):
        window = values[t - window_size:t]
        valid = window[~np.isnan(window)]
        if len(valid) < window_size // 2:
            continue
        median = np.median(valid)
        std = np.std(valid, ddof=0)          # STDEV.P – entspricht Excel
        if std == 0:
            continue

        for i in range(t - window_size, t):
            if np.isnan(values[i]):
                continue
            if abs(values[i] - median) > sigma * std:
                flag_counts[i] += 1
                window_medians[i].append(median)

    # Korrekturwert = Median aller Fenster-Mediane (robust gegen Ausreißer-Fenster)
    best_window_median = np.array([
        np.median(wm) if wm else np.nan for wm in window_medians
    ])

    # Zwei Bedingungen: min_flags UND min_ratio
    is_outlier = flag_counts >= min_flags
    corrected = values.copy().astype(float)

    if correction == "window_median":
        for i in np.where(is_outlier)[0]:
            corr_val = best_window_median[i]
            # min_ratio-Prüfung: Abweichungsfaktor muss groß genug sein
            if corr_val != 0 and not np.isnan(corr_val):
                abs_ratio = abs(values[i] / corr_val)
                if abs_ratio < min_ratio:
                    is_outlier[i] = False       # kein Outlier → nicht korrigieren
                    continue
            elif corr_val == 0 and values[i] == 0:
                is_outlier[i] = False
                continue
            corrected[i] = corr_val
    elif correction == "linear_interp":
        series = pd.Series(corrected)
        series[is_outlier] = np.nan
        corrected = series.interpolate(method="linear").values

    return {
        "is_outlier": is_outlier,
        "flag_counts": flag_counts,
        "corrected": corrected,
        "n_outliers": int(is_outlier.sum()),
    }


def _compute_isolation_score(
    values: np.ndarray, idx: int, corrected_val: float,
) -> float:
    """Neighbor Isolation Score: |original − neighbor_mean| / |corrected − neighbor_mean|.

    Misst, ob der Originalwert ein isolierter Sprung ist (Score > 3 → isoliert).
    Nachbarn = die ein oder zwei direkt angrenzenden Datenpunkte.
    """
    neighbors = []
    if idx > 0 and not np.isnan(values[idx - 1]):
        neighbors.append(values[idx - 1])
    if idx < len(values) - 1 and not np.isnan(values[idx + 1]):
        neighbors.append(values[idx + 1])
    if not neighbors:
        return np.nan
    neighbor_mean = np.mean(neighbors)
    denom = abs(corrected_val - neighbor_mean)
    if denom == 0:
        return np.inf if values[idx] != neighbor_mean else 0.0
    return abs(values[idx] - neighbor_mean) / denom


def _load_overrides() -> set[tuple[str, str, str]]:
    """Lädt die manuelle Override-Liste (ticker, quarter, column).

    Einträge in dieser Liste werden vom Algorithmus zwar geflagt,
    aber nicht korrigiert (was_corrected=False).
    """
    if not OUTLIER_OVERRIDES_PATH.exists():
        return set()
    df = pd.read_csv(OUTLIER_OVERRIDES_PATH)
    if df.empty:
        return set()
    required = {"ticker", "quarter", "column"}
    if not required.issubset(df.columns):
        logger.warning("Override-CSV hat nicht die erwarteten Spalten %s – wird ignoriert", required)
        return set()
    overrides = set(zip(df["ticker"], df["quarter"], df["column"]))
    logger.info("Overrides geladen: %d Einträge aus %s", len(overrides), OUTLIER_OVERRIDES_PATH.name)
    return overrides


def _clean_raw_panel(
    raw_panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Wendet Rolling-Window Outlier Detection auf alle RAW_COLS an.

    Verarbeitung pro Ticker × Spalte.  Parameter aus config.py.
    Zusätzlich werden pro Outlier zwei informative Crosscheck-Spalten berechnet:
      - is_isolated: Neighbor Isolation Score > 3
      - cross_metric_flagged: logisch verknüpfte Spalte ebenfalls im selben Quartal geflagt

    Manuelle Overrides (outlier_overrides.csv) werden berücksichtigt:
    geflagte Werte, die in der Override-Liste stehen, werden NICHT korrigiert
    und im Report mit was_corrected=False dokumentiert.

    Returns:
        (bereinigtes Panel, Outlier-Report als DataFrame)
    """
    df_clean = raw_panel.copy()
    report_rows: list[dict] = []
    total_outliers = {m: 0 for m in RAW_COLS}
    overrides = _load_overrides()
    n_overridden = 0

    # Cross-Metric-Lookup: col → set von Partner-Spalten
    cross_partners: dict[str, set[str]] = {}
    for a, b in CROSS_METRIC_PAIRS:
        cross_partners.setdefault(a, set()).add(b)
        cross_partners.setdefault(b, set()).add(a)

    for ticker, group in raw_panel.groupby("ticker"):
        idx = group.index

        # Phase 1: Detection + Correction pro Spalte
        results: dict[str, dict] = {}
        for col in RAW_COLS:
            values = group[col].values.astype(float)
            if np.all(np.isnan(values)):
                continue
            results[col] = _detect_and_correct_outliers(
                values,
                window_size=OUTLIER_WINDOW_SIZE,
                sigma=OUTLIER_SIGMA,
                min_flags=OUTLIER_MIN_FLAGS,
                min_ratio=OUTLIER_MIN_RATIO,
                correction=OUTLIER_CORRECTION,
            )

            # Override-Prüfung: Originalwert wiederherstellen wenn Override
            corrected = results[col]["corrected"].copy()
            for oi in np.where(results[col]["is_outlier"])[0]:
                qtr = group.iloc[oi]["quarter"]
                if (ticker, qtr, col) in overrides:
                    corrected[oi] = values[oi]          # Originalwert behalten
                    n_overridden += 1

            df_clean.loc[idx, col] = corrected
            total_outliers[col] += results[col]["n_outliers"]

        # Phase 2: Report mit Crosschecks (braucht alle Spalten-Ergebnisse)
        for col, result in results.items():
            if result["n_outliers"] == 0:
                continue
            values = group[col].values.astype(float)
            outlier_positions = np.where(result["is_outlier"])[0]

            for oi in outlier_positions:
                qtr = group.iloc[oi]["quarter"]
                is_override = (ticker, qtr, col) in overrides

                # Isolation Score
                iso_score = _compute_isolation_score(
                    values, oi, result["corrected"][oi],
                )

                # Cross-Metric: ist eine Partner-Spalte im gleichen Quartal auch Outlier?
                cross_flagged = False
                for partner in cross_partners.get(col, set()):
                    if partner in results and results[partner]["is_outlier"][oi]:
                        cross_flagged = True
                        break

                report_rows.append({
                    "ticker": ticker,
                    "quarter": qtr,
                    "column": col,
                    "original_value": values[oi],
                    "corrected_value": values[oi] if is_override else result["corrected"][oi],
                    "flag_count": int(result["flag_counts"][oi]),
                    "was_corrected": not is_override,
                    "isolation_score": round(iso_score, 2) if np.isfinite(iso_score) else iso_score,
                    "is_isolated": iso_score > 3 if np.isfinite(iso_score) else False,
                    "cross_metric_flagged": cross_flagged,
                })

    # Summary loggen
    total = sum(total_outliers.values())
    logger.info("Outlier Detection: %d Ausreißer geflagt, davon %d per Override geschützt",
                total, n_overridden)
    for col, count in total_outliers.items():
        if count > 0:
            logger.info("  %-35s: %4d", col, count)

    report = pd.DataFrame(report_rows) if report_rows else pd.DataFrame()
    return df_clean, report


# ─────────────────────────────────────────────
# 7. NaN/Null-Qualitätsfilter
# ─────────────────────────────────────────────
def _filter_nan_tickers(raw_panel: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Entfernt Ticker mit zu vielen fehlenden Werten in Zähler-/Nenner-Spalten.

    Regeln (Szenario C):
      - Nenner-Spalten: 0 ODER NaN zählen als fehlend (→ Kennzahl undefiniert)
      - Zähler-Spalten: nur NaN zählt (0 ist ein valider Wert, z.B. Break-even)
      - shortLongTermDebtTotal wird ausgenommen (NaN = Feld nicht gemeldet)
    Schwelle: NAN_MAX_QUARTERS (config.py)
    """
    # Formula-basierte Ratios haben leere col-Felder → ausfiltern
    den_cols = list({r.denominator_col for r in RATIOS if r.denominator_col})
    num_cols = list({r.numerator_col for r in RATIOS if r.numerator_col} - {"shortLongTermDebtTotal"})

    bad_tickers: set[str] = set()
    for ticker, group in raw_panel.groupby("ticker"):
        for col in den_cols:
            n_bad = ((group[col] == 0) | group[col].isna()).sum()
            if n_bad > NAN_MAX_QUARTERS:
                bad_tickers.add(ticker)
                break
        if ticker in bad_tickers:
            continue
        for col in num_cols:
            if group[col].isna().sum() > NAN_MAX_QUARTERS:
                bad_tickers.add(ticker)
                break

    n_removed = len(bad_tickers)
    if n_removed:
        raw_panel = raw_panel[~raw_panel["ticker"].isin(bad_tickers)].reset_index(drop=True)
        logger.info("NaN-Qualitätsfilter: %d Ticker entfernt (>%d fehlende Quartale), %d verbleibend",
                    n_removed, NAN_MAX_QUARTERS, raw_panel["ticker"].nunique())
    return raw_panel, n_removed


# ─────────────────────────────────────────────
# 8. Kennzahlen berechnen
# ─────────────────────────────────────────────
def _compute_ratios_from_raw(raw_panel: pd.DataFrame) -> pd.DataFrame:
    """Berechnet alle in RATIOS definierten Kennzahlen aus dem Rohwerte-Panel.

    Zwei Zweige:
      - Einfacher Quotient: r.numerator_col / r.denominator_col (Standard)
      - Formel: r.formula(raw_panel) liefert die Kennzahl-Series direkt

    Rückgabe: raw_panel ergänzt um RATIO_NAMES-Spalten.
    """
    for r in RATIOS:
        if r.is_formula:
            try:
                raw_panel[r.name] = r.formula(raw_panel)
            except Exception as exc:
                logger.warning(
                    "Formel-Kennzahl %s konnte nicht berechnet werden: %s",
                    r.name, exc,
                )
                raw_panel[r.name] = np.nan
        else:
            num = raw_panel[r.numerator_col]
            den = raw_panel[r.denominator_col].replace(0, np.nan)
            raw_panel[r.name] = num / den
    return raw_panel


def _winsorize_ratios(panel: pd.DataFrame) -> pd.DataFrame:
    """Winsorisiert Kennzahlen auf WINSORIZE_QUANTILES (pro Kennzahl).

    Kappt Extremwerte auf das q-te / (1−q)-te Perzentil.
    Begründung: Nahe-null Nenner erzeugen ökonomisch sinnlose Extremratios.
    """
    q_low, q_high = WINSORIZE_QUANTILES
    n_clipped = 0
    for col in RATIO_NAMES:
        vals = panel[col].dropna()
        if vals.empty:
            continue
        lo, hi = vals.quantile(q_low), vals.quantile(q_high)
        clipped = panel[col].clip(lower=lo, upper=hi)
        n_clipped += (clipped != panel[col]).sum()
        panel[col] = clipped
    logger.info("Winsorizing (%s/%s): %d Werte gekappt",
                f"{q_low:.0%}", f"{q_high:.0%}", n_clipped)
    return panel


# ─────────────────────────────────────────────
# Hauptfunktion
# ─────────────────────────────────────────────
def build_ratio_panel(save: bool = True) -> pd.DataFrame:
    """Kompletter Pipeline-Durchlauf: Laden → Filtern → Bereinigen → Berechnen.

    Rückgabe: Long-Format DataFrame mit Spalten [ticker, quarter, <ratios>].
    """
    ensure_output_dirs()

    # 1. Ticker-Universum
    tickers = get_ticker_universe()

    # 2. Sektor- und ADR-Filter
    profiles = _load_profiles()
    sector_map = {t: p["sector"] for t, p in profiles.items()}
    tickers = filter_sectors(tickers, sector_map)
    tickers = filter_adrs(tickers, profiles)

    # 3+4. Laden + Vollständigkeitsfilter → Rohwerte sammeln
    complete_tickers: list[str] = []
    all_raw: list[pd.DataFrame] = []

    for ticker in tickers:
        sources = {
            "income": _load_source(ticker, "income"),
            "balance": _load_source(ticker, "balance"),
            "cashflow": _load_source(ticker, "cashflow"),
        }

        if not _is_complete(sources):
            continue

        # 5. Rohwerte zusammenführen
        raw_row = _merge_raw_values(sources)
        raw_row["ticker"] = ticker
        complete_tickers.append(ticker)
        all_raw.append(raw_row)

    logger.info("Vollständigkeitsfilter: %d / %d Ticker bestanden (100 Quartale lückenlos)",
                len(complete_tickers), len(tickers))

    if not all_raw:
        raise RuntimeError("Kein einziger Ticker hat den Vollständigkeitsfilter bestanden!")

    # Rohwerte-Panel zusammenbauen
    raw_panel = pd.concat(all_raw, ignore_index=False)
    raw_panel = raw_panel.reset_index()                     # quarter wird Spalte
    raw_panel["quarter"] = raw_panel["quarter"].astype(str)
    raw_panel = raw_panel.sort_values(["ticker", "quarter"]).reset_index(drop=True)

    # Rohwerte-Panel speichern (vor Bereinigung, für Datenqualitäts-Analyse)
    if save:
        raw_path = OUT_RATIOS / "raw_values_panel.csv"
        raw_panel[["ticker", "quarter"] + RAW_COLS].to_csv(raw_path, index=False)
        logger.info("Rohwerte-Panel: %s (%d Zeilen, %d Ticker)",
                     raw_path, len(raw_panel), len(complete_tickers))

    # 6. Rolling-Window Outlier Detection auf Rohwerten
    raw_panel, outlier_report = _clean_raw_panel(raw_panel)

    # Outlier-Report speichern (Dokumentation für Methodenteil)
    if save and not outlier_report.empty:
        report_path = OUT_PREPROCESS / "outlier_report.csv"
        outlier_report.to_csv(report_path, index=False)
        logger.info("Outlier-Report: %s (%d Korrekturen)", report_path, len(outlier_report))

    # 7. NaN/Null-Qualitätsfilter (nach Bereinigung, vor Kennzahlenberechnung)
    raw_panel, _ = _filter_nan_tickers(raw_panel)

    # 8. Kennzahlen aus bereinigten Rohwerten berechnen
    raw_panel = _compute_ratios_from_raw(raw_panel)

    # 9. Winsorizing auf Kennzahlen (Extremratios durch nahe-null Nenner begrenzen)
    raw_panel = _winsorize_ratios(raw_panel)

    # Spaltenreihenfolge
    n_final = raw_panel["ticker"].nunique()
    panel = raw_panel[["ticker", "quarter"] + RATIO_NAMES]

    if save:
        out_path = OUT_RATIOS / "ratio_panel.csv"
        panel.to_csv(out_path, index=False)
        logger.info("Panel gespeichert: %s (%d Zeilen, %d Ticker)",
                     out_path, len(panel), n_final)

    return panel


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    panel = build_ratio_panel(save=True)

    # Zusammenfassung
    n_tickers = panel["ticker"].nunique()
    print(f"\n{'='*60}")
    print(f"  Panel fertig: {n_tickers} Unternehmen × max {EXPECTED_QUARTERS} Quartale")
    print(f"  Kennzahlen: {RATIO_NAMES}")
    print(f"  Gespeichert: output/ratios/ratio_panel.csv")
    print(f"{'='*60}")
    print(f"\nDeskriptive Statistik:")
    print(panel[RATIO_NAMES].describe().round(4).to_string())
