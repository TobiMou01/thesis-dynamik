#!/usr/bin/env python3
"""
EU-Daten-Download für Masterarbeit — Finanzkennzahlen europäischer Unternehmen

Lädt Fundamentaldaten von EODHD für alle relevanten europäischen Börsen.
Erzeugt exakt die gleiche Ordner- und Datenstruktur wie der US-Datenabruf,
damit die Daten in der bestehenden Pipeline weiterverarbeitet werden können.

Datenstruktur (Output):
    data/raw/income_statements/{SYMBOL}.{EXCHANGE}.csv
    data/raw/balance_sheets/{SYMBOL}.{EXCHANGE}.csv
    data/raw/cashflows/{SYMBOL}.{EXCHANGE}.csv
    data/raw/profiles/{SYMBOL}.{EXCHANGE}.csv

Nutzung:
    python fetch_data_eu.py --api-key DEIN_KEY                    # Alle EU-Börsen, Market Cap > 300M
    python fetch_data_eu.py --api-key DEIN_KEY --limit 50         # Test: nur 50 Unternehmen
    python fetch_data_eu.py --api-key DEIN_KEY --continue         # Fortsetzen (überspringt vorhandene)
    python fetch_data_eu.py --api-key DEIN_KEY --exchanges XETRA LSE  # Nur bestimmte Börsen

EODHD API: https://eodhd.com/
"""

import pandas as pd
import numpy as np
import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging
import argparse
from datetime import datetime

# ============================================================
# KONFIGURATION
# ============================================================

# --- Pfade ---
# Eigener Ordner, komplett getrennt von US-Daten
BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
RAW_PATH = DATA_PATH / "raw"
LOG_PATH = BASE_PATH / "logs"

# --- API ---
EODHD_BASE_URL = "https://eodhd.com/api"
REQUEST_DELAY = 0.25  # Sekunden zwischen API-Requests

# --- Europäische Börsen ---
# 19 Börsenplätze, sortiert nach erwarteter Relevanz (Anzahl großer Unternehmen)
EU_EXCHANGES = {
    # Große Märkte
    "LSE":   {"country": "UK",          "currency": "GBP", "name": "London Stock Exchange"},
    "XETRA": {"country": "Germany",     "currency": "EUR", "name": "Frankfurt (XETRA)"},
    "PA":    {"country": "France",       "currency": "EUR", "name": "Euronext Paris"},
    "AS":    {"country": "Netherlands",  "currency": "EUR", "name": "Euronext Amsterdam"},
    "SW":    {"country": "Switzerland",  "currency": "CHF", "name": "SIX Swiss Exchange"},
    # Italien (Borsa Italiana) wird von EODHD nicht unterstützt (MI=404, ETLX=leer)
    "MC":    {"country": "Spain",        "currency": "EUR", "name": "Bolsa de Madrid"},
    "ST":    {"country": "Sweden",       "currency": "SEK", "name": "Stockholm (Nasdaq Nordic)"},
    # Mittlere Märkte
    "CO":    {"country": "Denmark",      "currency": "DKK", "name": "Copenhagen (Nasdaq Nordic)"},
    "OL":    {"country": "Norway",       "currency": "NOK", "name": "Oslo Børs"},
    "HE":    {"country": "Finland",      "currency": "EUR", "name": "Helsinki (Nasdaq Nordic)"},
    "BR":    {"country": "Belgium",      "currency": "EUR", "name": "Euronext Brussels"},
    "VI":    {"country": "Austria",      "currency": "EUR", "name": "Wiener Börse"},
    "ISE":   {"country": "Ireland",      "currency": "EUR", "name": "Irish Stock Exchange"},
    "LS":    {"country": "Portugal",     "currency": "EUR", "name": "Euronext Lisbon"},
    # Kleinere Märkte (Osteuropa)
    "WA":    {"country": "Poland",       "currency": "PLN", "name": "Warsaw Stock Exchange"},
    "AT":    {"country": "Greece",       "currency": "EUR", "name": "Athens Stock Exchange"},
    "BUD":   {"country": "Hungary",      "currency": "HUF", "name": "Budapest Stock Exchange"},
    "PR":    {"country": "Czech Republic","currency": "CZK", "name": "Prague Stock Exchange"},
}

# --- Unternehmensfilter ---
# 300M in Lokalwährung als Vorfilter — großzügig, damit nichts verloren geht.
# Feinfilterung über Profildaten im Nachgang möglich.
MIN_MARKET_CAP = 300_000_000
STOCK_TYPE = "Common Stock"  # Nur Stammaktien (keine ETFs, ADRs etc.)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


# ============================================================
# API FUNKTIONEN
# ============================================================

def fetch_exchange_symbols(api_key: str, exchange: str) -> pd.DataFrame:
    """Holt alle Symbole einer Börse von EODHD.

    Rein: API-Key, Börsenkürzel (z.B. "XETRA", "LSE")
    Raus: DataFrame mit Code, Name, Type, ISIN etc. pro Symbol
    """
    url = f"{EODHD_BASE_URL}/exchange-symbol-list/{exchange}"
    params = {"api_token": api_key, "fmt": "json"}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    df = pd.DataFrame(response.json())
    return df


def fetch_fundamentals(api_key: str, ticker: str) -> Optional[Dict]:
    """Holt Fundamentaldaten für einen Ticker von EODHD.

    Rein: API-Key, vollständiger Ticker (z.B. "SAP.XETRA", "SHEL.LSE")
    Raus: Dict mit General, Highlights, Financials oder None bei Fehler
    """
    url = f"{EODHD_BASE_URL}/fundamentals/{ticker}"
    params = {"api_token": api_key, "fmt": "json"}

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"{ticker}: HTTP {response.status_code}")
            return None
    except Exception as e:
        logger.warning(f"{ticker}: {e}")
        return None


# ============================================================
# DATEN-EXTRAKTION (identisch zum US-Skript)
# ============================================================

def extract_financials(data: Dict, ticker: str) -> Dict:
    """Extrahiert Finanzdaten aus API-Response.

    Rein: EODHD-Response-Dict, Ticker (z.B. "SAP.XETRA")
    Raus: Dict mit Keys 'income_statement', 'balance_sheet', 'cashflow' (je DataFrame)
          und 'profile' (Dict mit Stammdaten)

    WICHTIG: Erzeugt exakt die gleiche Struktur wie das US-Skript.
    """
    result = {}
    financials = data.get("Financials", {})

    # Income Statement
    income = financials.get("Income_Statement", {}).get("quarterly", {})
    if income:
        df = pd.DataFrame(income).T
        df["symbol"] = ticker
        df["date"] = df.index
        result["income_statement"] = df

    # Balance Sheet
    balance = financials.get("Balance_Sheet", {}).get("quarterly", {})
    if balance:
        df = pd.DataFrame(balance).T
        df["symbol"] = ticker
        df["date"] = df.index
        result["balance_sheet"] = df

    # Cash Flow
    cashflow = financials.get("Cash_Flow", {}).get("quarterly", {})
    if cashflow:
        df = pd.DataFrame(cashflow).T
        df["symbol"] = ticker
        df["date"] = df.index
        result["cashflow"] = df

    # General Info / Profile
    # Exakt gleiche Felder wie im US-Skript, damit die Profil-CSVs identisch sind
    general = data.get("General", {})
    highlights = data.get("Highlights", {})
    if general:
        result["profile"] = {
            # Identifikation
            "symbol": ticker,
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
# SPEICHERFUNKTIONEN
# ============================================================

def save_raw_data(ticker: str, financials: Dict):
    """Speichert Rohdaten als CSV in data/raw/{Typ}/{ticker}.csv.

    Ticker-Format: CODE.EXCHANGE (z.B. SAP.XETRA)
    Erzeugt exakt die gleiche Ordnerstruktur wie das US-Skript.
    """
    for data_type in ["income_statement", "balance_sheet", "cashflow", "profile"]:
        if data_type not in financials:
            continue

        if data_type == "profile":
            folder = RAW_PATH / "profiles"
            folder.mkdir(parents=True, exist_ok=True)
            pd.DataFrame([financials[data_type]]).to_csv(folder / f"{ticker}.csv", index=False)
        else:
            folder_map = {
                "income_statement": "income_statements",
                "balance_sheet": "balance_sheets",
                "cashflow": "cashflows"
            }
            folder = RAW_PATH / folder_map[data_type]
            folder.mkdir(parents=True, exist_ok=True)
            financials[data_type].to_csv(folder / f"{ticker}.csv", index=False)


# ============================================================
# DOWNLOAD-LOGIK
# ============================================================

def get_existing_tickers() -> set:
    """Gibt bereits heruntergeladene Ticker zurück (aus profiles-Ordner)."""
    existing = set()
    profiles_path = RAW_PATH / "profiles"
    if profiles_path.exists():
        for f in profiles_path.glob("*.csv"):
            # Dateiname ist z.B. "SAP.XETRA.csv" → Ticker "SAP.XETRA"
            existing.add(f.stem)
    return existing


def download_exchange(api_key: str, exchange: str, symbols: List[str],
                      existing: set, min_market_cap: float,
                      stats: Dict) -> List[str]:
    """Lädt Fundamentaldaten für alle Symbole einer Börse herunter.

    Rein: API-Key, Exchange-Code, Symbol-Liste, bereits vorhandene Ticker,
          Market-Cap-Untergrenze, Stats-Dict (wird in-place aktualisiert)
    Raus: Liste fehlgeschlagener Ticker
    """
    failed = []

    for i, symbol in enumerate(symbols):
        ticker = f"{symbol}.{exchange}"

        # Bereits vorhanden → überspringen
        if ticker in existing:
            continue

        if (stats["processed"] + 1) % 100 == 0 or stats["processed"] == 0:
            logger.info(
                f"  [{stats['processed']+1}] Fortschritt — "
                f"Erfolg: {stats['success']}, "
                f"MarketCap-Skip: {stats['skipped_mc']}, "
                f"Fehler: {stats['failed']}"
            )

        stats["processed"] += 1

        # API-Request
        data = fetch_fundamentals(api_key, ticker)
        if not data:
            failed.append(ticker)
            stats["failed"] += 1
            time.sleep(REQUEST_DELAY)
            continue

        # Basis-Infos extrahieren
        general = data.get("General", {})
        highlights = data.get("Highlights", {})
        name = general.get("Name", "")[:30]
        sector = general.get("Sector", "")
        market_cap = highlights.get("MarketCapitalization")

        # Market Cap prüfen
        if market_cap is None:
            stats["skipped_mc"] += 1
            time.sleep(REQUEST_DELAY)
            continue

        market_cap = float(market_cap)

        if market_cap < min_market_cap:
            stats["skipped_mc"] += 1
            time.sleep(REQUEST_DELAY)
            continue

        # Daten extrahieren
        financials = extract_financials(data, ticker)
        if financials.get("income_statement") is None:
            logger.info(f"  ✗ {ticker} — {name} (keine Finanzdaten)")
            failed.append(ticker)
            stats["failed"] += 1
            time.sleep(REQUEST_DELAY)
            continue

        # Rohdaten speichern
        save_raw_data(ticker, financials)
        stats["success"] += 1
        logger.info(
            f"  ✓ {ticker} — {name} | {sector} | "
            f"{market_cap/1e9:.2f}B | {exchange}"
        )

        time.sleep(REQUEST_DELAY)

    return failed


def run_download(api_key: str, exchanges: List[str], limit: Optional[int],
                 skip_existing: bool, min_market_cap: float):
    """Hauptfunktion: Iteriert über alle Börsen, filtert und lädt herunter."""

    existing = get_existing_tickers() if skip_existing else set()
    if existing:
        logger.info(f"Bereits vorhanden: {len(existing)} Ticker (werden übersprungen)")

    # Statistiken
    stats = {"success": 0, "skipped_mc": 0, "failed": 0, "processed": 0}
    all_failed = []

    # Log-Datei für Zusammenfassung
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for exchange in exchanges:
        info = EU_EXCHANGES.get(exchange, {})
        logger.info(f"\n{'='*60}")
        logger.info(f"Börse: {exchange} — {info.get('name', exchange)} ({info.get('country', '?')})")
        logger.info(f"{'='*60}")

        # Symbolliste holen
        try:
            df = fetch_exchange_symbols(api_key, exchange)
            logger.info(f"  Gesamte Symbole: {len(df)}")
        except Exception as e:
            logger.error(f"  Fehler beim Laden der Symbolliste: {e}")
            continue

        time.sleep(REQUEST_DELAY)

        # Leere Börse überspringen (z.B. wenn API 0 Symbole liefert)
        if len(df) == 0 or "Code" not in df.columns:
            logger.warning(f"  Keine Symbole gefunden — Börse übersprungen")
            continue

        # Nur Common Stock filtern
        if "Type" in df.columns:
            df = df[df["Type"] == STOCK_TYPE]
            logger.info(f"  Nach Type-Filter (Common Stock): {len(df)}")

        symbols = df["Code"].tolist()

        # Limit (pro Börse, falls gesetzt — für Tests)
        if limit:
            symbols = symbols[:limit]
            logger.info(f"  Limitiert auf: {len(symbols)}")

        logger.info(f"  Starte Download für {len(symbols)} Symbole...")

        # Download
        failed = download_exchange(
            api_key, exchange, symbols, existing, min_market_cap, stats
        )
        all_failed.extend(failed)

    # ============================================================
    # ZUSAMMENFASSUNG
    # ============================================================

    logger.info(f"\n{'='*60}")
    logger.info(f"ZUSAMMENFASSUNG")
    logger.info(f"{'='*60}")
    logger.info(f"Verarbeitet:           {stats['processed']}")
    logger.info(f"Erfolgreich gespeichert: {stats['success']}")
    logger.info(f"MarketCap < {min_market_cap/1e6:.0f}M:    {stats['skipped_mc']}")
    logger.info(f"Fehlgeschlagen:        {stats['failed']}")

    # Aktuelle Gesamtzahl
    total_profiles = len(list((RAW_PATH / "profiles").glob("*.csv"))) if (RAW_PATH / "profiles").exists() else 0
    logger.info(f"\nGesamt im Ordner:      {total_profiles} Unternehmen")

    # Log speichern
    summary = {
        "timestamp": timestamp,
        "exchanges": exchanges,
        "min_market_cap": min_market_cap,
        "stats": stats,
        "failed_tickers": all_failed[:100],  # Nur erste 100 loggen
    }
    log_file = LOG_PATH / f"run_{timestamp}.json"
    with open(log_file, "w") as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Log gespeichert: {log_file}")

    return stats, all_failed


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="EU-Daten-Download für Masterarbeit (EODHD API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python fetch_data_eu.py --api-key KEY                      # Alle 19 EU-Börsen
  python fetch_data_eu.py --api-key KEY --exchanges XETRA LSE PA  # Nur bestimmte Börsen
  python fetch_data_eu.py --api-key KEY --limit 10           # Test: 10 pro Börse
  python fetch_data_eu.py --api-key KEY --continue           # Fortsetzen
  python fetch_data_eu.py --list-exchanges                   # Verfügbare Börsen anzeigen
        """
    )

    parser.add_argument("--api-key", "-k", help="EODHD API Key")
    parser.add_argument("--exchanges", "-e", nargs="+", default=None,
                        help="Nur bestimmte Börsen (z.B. XETRA LSE PA)")
    parser.add_argument("--limit", "-n", type=int, default=None,
                        help="Max. Anzahl Unternehmen PRO BÖRSE (für Tests)")
    parser.add_argument("--continue", "-c", dest="continue_download", action="store_true",
                        help="Bereits vorhandene Ticker überspringen")
    parser.add_argument("--min-market-cap", type=float, default=MIN_MARKET_CAP,
                        help=f"Min. Market Cap in Lokalwährung (default: {MIN_MARKET_CAP/1e6:.0f}M)")
    parser.add_argument("--list-exchanges", action="store_true",
                        help="Verfügbare EU-Börsen anzeigen und beenden")
    parser.add_argument("--status", action="store_true",
                        help="Aktuellen Download-Status anzeigen")

    args = parser.parse_args()

    # --- Börsen anzeigen ---
    if args.list_exchanges:
        print(f"\nVerfügbare EU-Börsen ({len(EU_EXCHANGES)}):\n")
        print(f"{'Code':<8} {'Land':<20} {'Währung':<8} {'Name'}")
        print("-" * 70)
        for code, info in EU_EXCHANGES.items():
            print(f"{code:<8} {info['country']:<20} {info['currency']:<8} {info['name']}")
        return

    # --- Status anzeigen ---
    if args.status:
        print("\nAktueller Download-Status:\n")
        for folder in ["income_statements", "balance_sheets", "cashflows", "profiles"]:
            path = RAW_PATH / folder
            count = len(list(path.glob("*.csv"))) if path.exists() else 0
            print(f"  {folder:<25} {count:>6} Dateien")

        # Nach Börse aufschlüsseln
        profiles_path = RAW_PATH / "profiles"
        if profiles_path.exists():
            exchange_counts = {}
            for f in profiles_path.glob("*.csv"):
                # Dateiname: CODE.EXCHANGE.csv → Exchange ist der letzte Teil vor .csv
                parts = f.stem.split(".")
                if len(parts) >= 2:
                    ex = parts[-1]
                    exchange_counts[ex] = exchange_counts.get(ex, 0) + 1
            print(f"\nNach Börse:")
            for ex, count in sorted(exchange_counts.items(), key=lambda x: -x[1]):
                info = EU_EXCHANGES.get(ex, {})
                print(f"  {ex:<8} {count:>6}  ({info.get('country', '?')})")
        return

    # --- Download benötigt API Key ---
    if not args.api_key:
        print("Fehler: --api-key benötigt")
        print("\nBeispiel: python fetch_data_eu.py --api-key DEIN_KEY")
        print("          python fetch_data_eu.py --api-key DEIN_KEY --limit 10  # Testlauf")
        return

    # --- Börsen auswählen ---
    if args.exchanges:
        # Prüfen ob alle angegebenen Börsen existieren
        invalid = [e for e in args.exchanges if e not in EU_EXCHANGES]
        if invalid:
            print(f"Unbekannte Börsen: {invalid}")
            print(f"Verfügbar: {list(EU_EXCHANGES.keys())}")
            return
        exchanges = args.exchanges
    else:
        exchanges = list(EU_EXCHANGES.keys())

    logger.info(f"EU-Datenabruf gestartet")
    logger.info(f"Börsen: {len(exchanges)} ({', '.join(exchanges)})")
    logger.info(f"Market Cap Filter: > {args.min_market_cap/1e6:.0f}M (Lokalwährung)")
    logger.info(f"Output: {RAW_PATH}")

    # --- Download ---
    run_download(
        api_key=args.api_key,
        exchanges=exchanges,
        limit=args.limit,
        skip_existing=args.continue_download,
        min_market_cap=args.min_market_cap,
    )

    logger.info("\nFertig!")


if __name__ == "__main__":
    main()
