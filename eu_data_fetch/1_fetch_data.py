#!/usr/bin/env python3
"""
Daten-Download und Kennzahlen-Berechnung für Masterarbeit

Lädt Finanzdaten von EODHD und berechnet Kennzahlen.
Fortsetzbar: überspringt bereits heruntergeladene Unternehmen.

Nutzung:
    python src/1_fetch_data.py --api-key DEIN_KEY                 # Alle US-Aktien mit Market Cap > 1B
    python src/1_fetch_data.py --api-key DEIN_KEY --limit 100     # Nur 100 Unternehmen
    python src/1_fetch_data.py --api-key DEIN_KEY --continue      # Nur neue Unternehmen
    python src/1_fetch_data.py --recalc                           # Nur Kennzahlen neu berechnen

EODHD API: https://eodhd.com/
"""

import pandas as pd
import numpy as np
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional
import logging
import argparse
from datetime import datetime

# ============================================================
# KONFIGURATION
# ============================================================

# --- Pfade ---
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data"
RAW_PATH = DATA_PATH / "raw"
RATIOS_PATH = DATA_PATH / "ratios"
COMBINED_PATH = DATA_PATH / "combined"

# --- API ---
EODHD_BASE_URL = "https://eodhd.com/api"
REQUEST_DELAY = 0.25  # Sekunden zwischen API-Requests

# --- Region & Börsen ---
REGION = "US"  # "US" oder "EU"
REGIONS = {
    "US": ["US"],
    "EU": ["XETRA", "LSE", "PA", "AS", "MI", "MC", "SW"]
}

# --- Unternehmensfilter ---
MIN_MARKET_CAP = 1_000_000_000  # 1 Milliarde USD
STOCK_TYPE = "Common Stock"     # Nur Stammaktien (keine ETFs, ADRs etc.)

# --- Kennzahlen ---
# Welche Ratios berechnet und in die Pipeline übergeben werden
# Prozent-Ratios (×100): ROA, ROE, EBIT_margin, equity_ratio, fcf_margin
# Verhältnis-Ratios (roh): current_ratio, debt_to_equity
RATIOS = ["EBIT_margin", "ROA", "ROE", "current_ratio", "debt_to_equity", "equity_ratio", "fcf_margin"]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# API FUNKTIONEN
# ============================================================

def fetch_exchange_symbols(api_key: str, exchange: str = "US") -> pd.DataFrame:
    """Holt alle Symbole einer Börse von EODHD.

    Rein: API-Key, Börsenkürzel (z.B. "US", "XETRA")
    Raus: DataFrame mit Code, Name, Type etc. pro Symbol
    """
    url = f"{EODHD_BASE_URL}/exchange-symbol-list/{exchange}"
    params = {"api_token": api_key, "fmt": "json"}

    response = requests.get(url, params=params)
    response.raise_for_status()

    df = pd.DataFrame(response.json())
    return df


def fetch_fundamentals(api_key: str, symbol: str) -> Optional[Dict]:
    """Holt Fundamentaldaten für ein Symbol von EODHD.

    Rein: API-Key, Ticker-Symbol (z.B. "AAPL")
    Raus: Dict mit General, Highlights, Financials oder None bei Fehler
    """
    ticker = symbol if "." in symbol else f"{symbol}.US"
    url = f"{EODHD_BASE_URL}/fundamentals/{ticker}"
    params = {"api_token": api_key, "fmt": "json"}

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"{symbol}: HTTP {response.status_code}")
            return None
    except Exception as e:
        logger.warning(f"{symbol}: {e}")
        return None


def extract_financials(data: Dict, symbol: str) -> Dict[str, pd.DataFrame]:
    """Extrahiert Finanzdaten aus API-Response.

    Rein: EODHD-Response-Dict, Ticker-Symbol
    Raus: Dict mit Keys 'income_statement', 'balance_sheet', 'cashflow' (je DataFrame)
          und 'profile' (Dict mit Stammdaten)
    """
    result = {}

    financials = data.get("Financials", {})

    # Income Statement
    income = financials.get("Income_Statement", {}).get("quarterly", {})
    if income:
        df = pd.DataFrame(income).T
        df["symbol"] = symbol
        df["date"] = df.index
        result["income_statement"] = df

    # Balance Sheet
    balance = financials.get("Balance_Sheet", {}).get("quarterly", {})
    if balance:
        df = pd.DataFrame(balance).T
        df["symbol"] = symbol
        df["date"] = df.index
        result["balance_sheet"] = df

    # Cash Flow
    cashflow = financials.get("Cash_Flow", {}).get("quarterly", {})
    if cashflow:
        df = pd.DataFrame(cashflow).T
        df["symbol"] = symbol
        df["date"] = df.index
        result["cashflow"] = df

    # General Info
    general = data.get("General", {})
    highlights = data.get("Highlights", {})
    if general:
        result["profile"] = {
            # Identifikation
            "symbol": symbol,
            "name": general.get("Name"),
            "isin": general.get("ISIN"),
            "cusip": general.get("CUSIP"),
            # Börse & Region
            "exchange": general.get("Exchange"),
            "currency": general.get("CurrencyCode"),
            "country": general.get("CountryName"),
            "country_iso": general.get("CountryISO"),
            # Klassifikation
            "type": general.get("Type"),
            "sector": general.get("Sector"),
            "industry": general.get("Industry"),
            "gic_sector": general.get("GicSector"),
            "gic_industry": general.get("GicIndustry"),
            # Unternehmensdaten
            "ipo_date": general.get("IPODate"),
            "fiscal_year_end": general.get("FiscalYearEnd"),
            "employees": general.get("FullTimeEmployees"),
            "description": general.get("Description"),
            # Bewertung (Highlights)
            "market_cap": highlights.get("MarketCapitalization"),
            "ebitda": highlights.get("EBITDA"),
            "pe_ratio": highlights.get("PERatio"),
            "peg_ratio": highlights.get("PEGRatio"),
            "book_value": highlights.get("BookValue"),
            "dividend_yield": highlights.get("DividendYield"),
            "dividend_share": highlights.get("DividendShare"),
            "eps": highlights.get("EarningsShare"),
            # Performance (Highlights)
            "revenue_ttm": highlights.get("RevenueTTM"),
            "profit_margin": highlights.get("ProfitMargin"),
            "operating_margin": highlights.get("OperatingMarginTTM"),
            "roa": highlights.get("ReturnOnAssetsTTM"),
            "roe": highlights.get("ReturnOnEquityTTM"),
            "revenue_growth_yoy": highlights.get("QuarterlyRevenueGrowthYOY"),
            "earnings_growth_yoy": highlights.get("QuarterlyEarningsGrowthYOY"),
        }

    return result


# ============================================================
# KENNZAHLEN-BERECHNUNG
# ============================================================

def calculate_ratios(symbol: str, income_df: pd.DataFrame, balance_df: pd.DataFrame,
                     cashflow_df: pd.DataFrame) -> pd.DataFrame:
    """Berechnet 7 Finanzkennzahlen aus Quartalsdaten.

    Rein: Ticker-Symbol + je ein DataFrame für Income Statement, Balance Sheet, Cash Flow
    Raus: DataFrame mit Spalten [symbol, date, fiscal_year, fiscal_quarter, + 7 Kennzahlen]
          Kennzahlen: EBIT_margin(%), ROA(%), ROE(%), current_ratio, debt_to_equity, equity_ratio(%), fcf_margin(%)
    """

    # Merge auf Datum
    income_df["date"] = pd.to_datetime(income_df["date"])
    balance_df["date"] = pd.to_datetime(balance_df["date"])
    cashflow_df["date"] = pd.to_datetime(cashflow_df["date"])

    df = income_df.merge(balance_df, on="date", suffixes=("", "_bal"))
    df = df.merge(cashflow_df, on="date", suffixes=("", "_cf"))

    if len(df) == 0:
        return pd.DataFrame()

    # Hilfsfunktion für sichere Division
    def safe_div(a, b):
        return np.where((b != 0) & (~np.isnan(b)), a / b, np.nan)

    # Numerische Konvertierung
    def to_numeric(col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors='coerce')
        return np.nan

    # Werte extrahieren
    revenue = to_numeric("totalRevenue")
    ebit = to_numeric("ebit")
    net_income = to_numeric("netIncome")
    total_assets = to_numeric("totalAssets")
    total_equity = to_numeric("totalStockholderEquity")
    total_liabilities = to_numeric("totalLiab")
    current_assets = to_numeric("totalCurrentAssets")
    current_liabilities = to_numeric("totalCurrentLiabilities")
    operating_cashflow = to_numeric("operatingCashflow") if "operatingCashflow" in df.columns else to_numeric("totalCashFromOperatingActivities")
    capex = to_numeric("capitalExpenditures")

    # Kennzahlen berechnen
    ratios = pd.DataFrame()
    ratios["symbol"] = symbol
    ratios["date"] = df["date"]

    # Datum aufsplitten
    ratios["fiscal_year"] = df["date"].dt.year
    ratios["fiscal_quarter"] = df["date"].dt.quarter

    # Profitabilität
    ratios["EBIT_margin"] = safe_div(ebit, revenue) * 100
    ratios["ROA"] = safe_div(net_income, total_assets) * 100
    ratios["ROE"] = safe_div(net_income, total_equity) * 100

    # Liquidität
    ratios["current_ratio"] = safe_div(current_assets, current_liabilities)

    # Verschuldung
    ratios["debt_to_equity"] = safe_div(total_liabilities, total_equity)
    ratios["equity_ratio"] = safe_div(total_equity, total_assets) * 100

    # Cash Flow
    fcf = operating_cashflow - np.abs(capex) if not isinstance(capex, float) else operating_cashflow
    ratios["fcf_margin"] = safe_div(fcf, revenue) * 100

    # Sortieren
    ratios = ratios.sort_values("date").reset_index(drop=True)

    return ratios


# ============================================================
# SPEICHERFUNKTIONEN
# ============================================================

def save_raw_data(symbol: str, financials: Dict):
    """Speichert Rohdaten als CSV in data/raw/{Typ}/{symbol}.csv."""

    for data_type in ["income_statement", "balance_sheet", "cashflow", "profile"]:
        if data_type not in financials:
            continue

        if data_type == "profile":
            folder = RAW_PATH / "profiles"
            folder.mkdir(parents=True, exist_ok=True)
            pd.DataFrame([financials[data_type]]).to_csv(folder / f"{symbol}.csv", index=False)
        else:
            folder_map = {
                "income_statement": "income_statements",
                "balance_sheet": "balance_sheets",
                "cashflow": "cashflows"
            }
            folder = RAW_PATH / folder_map[data_type]
            folder.mkdir(parents=True, exist_ok=True)
            financials[data_type].to_csv(folder / f"{symbol}.csv", index=False)


def save_ratios(symbol: str, ratios_df: pd.DataFrame):
    """Speichert berechnete Kennzahlen in data/ratios/{symbol}.csv."""
    RATIOS_PATH.mkdir(parents=True, exist_ok=True)
    ratios_df.to_csv(RATIOS_PATH / f"{symbol}.csv", index=False)


def combine_all_ratios():
    COMBINED_PATH.mkdir(parents=True, exist_ok=True)

    all_dfs = []
    for f in RATIOS_PATH.glob("*.csv"):
        df = pd.read_csv(f)
        df["symbol"] = f.stem.upper()   # ← NEU: Symbol als Spalte hinzufügen
        all_dfs.append(df)

    if not all_dfs:
        logger.warning("Keine Kennzahlen-Dateien gefunden")
        return

    combined = pd.concat(all_dfs, ignore_index=True)
    combined = combined.sort_values(["symbol", "fiscal_year", "fiscal_quarter"])

    # Wide Format
    combined.to_csv(COMBINED_PATH / "all_ratios_wide.csv", index=False)

    # Long Format
    id_cols = ["symbol", "date", "fiscal_year", "fiscal_quarter"]
    value_cols = RATIOS
    # Filter nur vorhandene Spalten
    value_cols = [c for c in value_cols if c in combined.columns]
    if value_cols:
        long_df = combined.melt(id_vars=id_cols, value_vars=value_cols, var_name="ratio", value_name="ratio_value")
        long_df.to_csv(COMBINED_PATH / "all_ratios_long.csv", index=False)

    logger.info(f"Kombiniert: {len(combined)} Zeilen, {combined['symbol'].nunique()} Unternehmen")


# ============================================================
# HAUPTFUNKTIONEN
# ============================================================

def get_existing_symbols() -> set:
    """Gibt bereits heruntergeladene Symbole zurück."""
    existing = set()
    if RATIOS_PATH.exists():
        for f in RATIOS_PATH.glob("*.csv"):
            existing.add(f.stem)
    return existing


def download_and_process(api_key: str, symbols: List[str], skip_existing: bool = True,
                         min_market_cap: float = 0):
    """Hauptschleife: lädt Fundamentaldaten pro Symbol, filtert nach Market Cap, berechnet Kennzahlen.

    Rein: API-Key, Symbol-Liste, skip_existing (--continue), min_market_cap
    Raus: (Anzahl Erfolge, Liste fehlgeschlagener Symbole)
    Seiteneffekt: Speichert Roh- und Kennzahlen-CSVs
    """

    existing = get_existing_symbols() if skip_existing else set()

    # Alphabetisch sortieren und ab letztem Buchstaben fortsetzen
    if skip_existing and existing:
        symbols = sorted(symbols)
        last_symbol = max(existing)
        resume_from = last_symbol[0]  # Erster Buchstabe
        symbols = [s for s in symbols if s[0] >= resume_from]
        logger.info(f"Fortsetzen ab Buchstabe '{resume_from}' (letztes Symbol: {last_symbol}, {len(symbols)} verbleibend)")

    # Filtern (bereits heruntergeladene ausschließen)
    to_process = [s for s in symbols if s not in existing]
    logger.info(f"Zu verarbeiten: {len(to_process)} (übersprungen: {len(existing) if skip_existing else 0})")

    success = 0
    skipped_market_cap = 0
    failed = []

    for i, symbol in enumerate(to_process):
        if (i + 1) % 50 == 0 or i == 0:
            logger.info(f"[{i+1}/{len(to_process)}] Fortschritt... (Erfolg: {success}, MarketCap-Skip: {skipped_market_cap})")

        # API-Request
        data = fetch_fundamentals(api_key, symbol)
        if not data:
            failed.append(symbol)
            time.sleep(REQUEST_DELAY)
            continue

        # Infos extrahieren
        general = data.get("General", {})
        highlights = data.get("Highlights", {})
        name = general.get("Name", "")[:30]  # Kürzen für Output
        sector = general.get("Sector", "")
        market_cap = highlights.get("MarketCapitalization")

        if market_cap is None:
            skipped_market_cap += 1
            logger.info(f"  ✗ {symbol} - {name} (Market Cap fehlt)")
            time.sleep(REQUEST_DELAY)
            continue

        market_cap = float(market_cap)

        if market_cap < min_market_cap:
            skipped_market_cap += 1
            logger.info(f"  ✗ {symbol} - {name} ({market_cap/1e9:.2f}B < {min_market_cap/1e9:.1f}B)")
            time.sleep(REQUEST_DELAY)
            continue

        # Daten extrahieren
        financials = extract_financials(data, symbol)
        if financials.get("income_statement") is None:
            logger.info(f"  ✗ {symbol} - {name} (keine Finanzdaten)")
            failed.append(symbol)
            time.sleep(REQUEST_DELAY)
            continue

        # Rohdaten speichern
        save_raw_data(symbol, financials)

        # Kennzahlen berechnen
        try:
            ratios = calculate_ratios(
                symbol,
                financials.get("income_statement", pd.DataFrame()),
                financials.get("balance_sheet", pd.DataFrame()),
                financials.get("cashflow", pd.DataFrame())
            )
            if len(ratios) > 0:
                save_ratios(symbol, ratios)
                success += 1
                logger.info(f"  ✓ {symbol} - {name} | {sector} | {market_cap/1e9:.1f}B | {len(ratios)} Quartale")
            else:
                logger.info(f"  ✗ {symbol} - {name} (keine Ratios berechnet)")
                failed.append(symbol)
        except Exception as e:
            logger.info(f"  ✗ {symbol} - {name} (Fehler: {e})")
            failed.append(symbol)

        time.sleep(REQUEST_DELAY)

    logger.info(f"\nErfolgreich: {success}")
    logger.info(f"Übersprungen (Market Cap): {skipped_market_cap}")
    logger.info(f"Fehlgeschlagen: {len(failed)}")

    return success, failed


def recalculate_all_ratios():
    """Berechnet alle Kennzahlen aus Rohdaten neu (--recalc Modus).

    Liest data/raw/, berechnet Kennzahlen neu, schreibt data/ratios/ und data/combined/.
    Nützlich wenn calculate_ratios() geändert wurde.
    """

    # FIX: alte (kaputte) Ratio-Dateien entfernen
    if RATIOS_PATH.exists():
        for f in RATIOS_PATH.glob("*.csv"):
            f.unlink()

    symbols = set()
    for f in (RAW_PATH / "income_statements").glob("*.csv"):
        symbols.add(f.stem)

    logger.info(f"Neuberechnung für {len(symbols)} Unternehmen")

    for symbol in sorted(symbols):
        try:
            income = pd.read_csv(RAW_PATH / "income_statements" / f"{symbol}.csv")
            balance = pd.read_csv(RAW_PATH / "balance_sheets" / f"{symbol}.csv")
            cashflow = pd.read_csv(RAW_PATH / "cashflows" / f"{symbol}.csv")

            ratios = calculate_ratios(symbol, income, balance, cashflow)
            if len(ratios) > 0:
                save_ratios(symbol, ratios)
        except Exception as e:
            logger.warning(f"{symbol}: {e}")

    combine_all_ratios()


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Daten-Download für Masterarbeit")
    parser.add_argument("--api-key", "-k", help="EODHD API Key")
    parser.add_argument("--limit", "-n", type=int, default=None, help="Max. Anzahl Unternehmen")
    parser.add_argument("--continue", "-c", dest="continue_download", action="store_true",
                       help="Nur neue Unternehmen laden")
    parser.add_argument("--recalc", action="store_true", help="Nur Kennzahlen neu berechnen")
    parser.add_argument("--min-market-cap", type=float, default=MIN_MARKET_CAP,
                       help=f"Min. Market Cap (default: {MIN_MARKET_CAP/1e9:.0f}B)")
    parser.add_argument("--combine", action="store_true", help="Nur kombinierte Datei erstellen")

    args = parser.parse_args()

    # Nur kombinieren
    if args.combine:
        combine_all_ratios()
        return

    # Nur neu berechnen
    if args.recalc:
        recalculate_all_ratios()
        return

    # Download benötigt API Key
    if not args.api_key:
        print("Fehler: --api-key benötigt")
        print("\nBeispiel: python fetch_data.py --api-key DEIN_KEY")
        return

    # Unternehmensliste holen (Multi-Exchange für EU)
    logger.info(f"Lade Unternehmensliste für Region: {REGION}...")

    all_dfs = []
    for exchange in REGIONS[REGION]:
        df = fetch_exchange_symbols(args.api_key, exchange)
        df["_exchange"] = exchange
        all_dfs.append(df)
        logger.info(f"  {exchange}: {len(df)} Symbole")
        time.sleep(REQUEST_DELAY)

    all_symbols = pd.concat(all_dfs, ignore_index=True)
    logger.info(f"Gesamt: {len(all_symbols)} Symbole")

    # Nur Common Stock filtern
    if "Type" in all_symbols.columns:
        filtered = all_symbols[all_symbols["Type"] == STOCK_TYPE]
        logger.info(f"Nach Type Filter (Common Stock): {len(filtered)}")
    else:
        filtered = all_symbols

    # Symbol mit Exchange-Suffix für API (z.B. "SAP.XETRA")
    if REGION == "US":
        symbols = filtered["Code"].tolist()
    else:
        symbols = (filtered["Code"] + "." + filtered["_exchange"]).tolist()

    # Limit anwenden
    if args.limit:
        symbols = symbols[:args.limit]
        logger.info(f"Limitiert auf: {len(symbols)}")

    logger.info(f"Market Cap Filter: > {args.min_market_cap/1e9:.1f}B USD (wird bei Download geprüft)")

    # Download starten
    download_and_process(args.api_key, symbols, skip_existing=args.continue_download,
                        min_market_cap=args.min_market_cap)

    # Kombinieren
    combine_all_ratios()

    logger.info("\nFertig!")
    logger.info(f"Output: {COMBINED_PATH / 'all_ratios_wide.csv'}")


if __name__ == "__main__":
    main()
