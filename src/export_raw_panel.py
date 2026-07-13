"""
export_raw_panel.py – Rohwerte-Panel aus den Quell-CSVs exportieren
====================================================================
Erzeugt ein CSV mit den Basisfeldern der Kennzahlenberechnung:
  ticker, quarter, netIncome, totalAssets, totalStockholderEquity,
  ebit, totalRevenue, freeCashFlow, totalCurrentAssets,
  totalCurrentLiabilities, shortLongTermDebtTotal

Designentscheidungen:
  - Separates Skript (keine Änderung an bestehender Ratio-Pipeline)
  - Zeitraumfilter: 2000–2024
  - Quartalsduplikate: pro Quartal letzter Eintrag (spätestes date)
  - Merge-Schlüssel: ticker + quarter
  - Fehlende Felder/Quellen bleiben als NaN
"""

import logging

import pandas as pd

from config import OUT_RATIOS, ensure_output_dirs
from load_data import (
    _is_complete as ld_is_complete,
    _load_source as ld_load_source,
    filter_sectors,
    get_ticker_universe,
    load_sector_map,
)

logger = logging.getLogger(__name__)


INCOME_FIELDS = ["netIncome", "ebit", "totalRevenue"]
BALANCE_FIELDS = [
    "totalAssets",
    "totalStockholderEquity",
    "totalCurrentAssets",
    "totalCurrentLiabilities",
    "shortLongTermDebtTotal",
]
CASHFLOW_FIELDS = ["freeCashFlow"]

FINAL_COLUMNS = [
    "ticker",
    "quarter",
    "netIncome",
    "totalAssets",
    "totalStockholderEquity",
    "ebit",
    "totalRevenue",
    "freeCashFlow",
    "totalCurrentAssets",
    "totalCurrentLiabilities",
    "shortLongTermDebtTotal",
]


def get_filtered_tickers() -> list[str]:
    """Repliziert exakt die Ticker-Filterung aus load_data.py."""
    tickers = get_ticker_universe()  # Schnittmenge der drei Rohquellen
    sector_map = load_sector_map()
    tickers = filter_sectors(tickers, sector_map)  # Finanzsektor exkludieren
    return tickers


def build_raw_panel(save: bool = True) -> pd.DataFrame:
    """Erzeugt das Rohwerte-Panel im Long-Format."""
    ensure_output_dirs()
    tickers = get_filtered_tickers()

    all_rows: list[pd.DataFrame] = []
    complete_tickers = 0

    for ticker in tickers:
        sources = {
            "income": ld_load_source(ticker, "income"),
            "balance": ld_load_source(ticker, "balance"),
            "cashflow": ld_load_source(ticker, "cashflow"),
        }

        if not ld_is_complete(sources):
            continue
        complete_tickers += 1

        income = sources["income"].reindex(columns=INCOME_FIELDS)
        balance = sources["balance"].reindex(columns=BALANCE_FIELDS)
        cashflow = sources["cashflow"].reindex(columns=CASHFLOW_FIELDS)

        merged = pd.concat([income, balance, cashflow], axis=1, join="outer").sort_index()
        if len(merged) == 0:
            continue

        merged = merged.reset_index()
        merged["quarter"] = merged["quarter"].astype(str)
        merged["ticker"] = ticker
        all_rows.append(merged)

    if not all_rows:
        raise RuntimeError("Kein Rohdaten-Panel erzeugt: keine Daten im Zeitraum gefunden.")

    panel = pd.concat(all_rows, ignore_index=True)
    panel = panel[FINAL_COLUMNS]

    if save:
        out_path = OUT_RATIOS / "raw_values_panel.csv"
        panel.to_csv(out_path, index=False)
        logger.info(
            "Rohwerte-Panel gespeichert: %s (%d Zeilen, %d Ticker)",
            out_path,
            len(panel),
            panel["ticker"].nunique(),
        )
    logger.info("Vollständigkeitsfilter (wie load_data): %d / %d Ticker", complete_tickers, len(tickers))

    return panel


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    panel = build_raw_panel(save=True)
    print(f"\n{'='*60}")
    print(f"  Rohwerte-Panel fertig: {panel['ticker'].nunique()} Unternehmen")
    print(f"  Zeilen: {len(panel)}")
    print("  Gespeichert: output/ratios/raw_values_panel.csv")
    print(f"{'='*60}")
