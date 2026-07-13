"""
config.py – Zentrale Konfiguration der Analyse-Pipeline
========================================================
Masterarbeit: Zeitreihenbasierte Analyse der Dynamik von Finanzkennzahlen
Autor: Tobias Mourier, TH Wildau, 2026

Methodische Entscheidungen:
  - AR(1) auf ersten Differenzen ΔY (nicht Levels)
  - Fixer Zeitraum 2000–2024 für alle Unternehmen
  - Nur Unternehmen mit lückenlosem Quartalsdatensatz (100 Quartale)
  - Einfache Volatilität σ(ΔY) als zweite Dimension (kein GARCH)

Sektionsreihenfolge folgt der Pipeline:
  Pfade → Zeitraum → Filter → Kennzahlen → AR → Klassifikation
  → Interdependenz → Externe Validierung → Explore → Hilfsfunktionen
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable, Optional

import pandas as pd  # nur für Type-Hints in RatioDef.formula


# ─────────────────────────────────────────────
# Pfade
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Rohdaten-Unterordner (je eine CSV pro Ticker)
RAW_BALANCE = RAW_DIR / "balance_sheets"
RAW_INCOME = RAW_DIR / "income_statements"
RAW_CASHFLOW = RAW_DIR / "cashflows"
RAW_PROFILE = RAW_DIR / "profiles"

# Output-Unterordner (Pipeline-Reihenfolge)
OUT_RATIOS = OUTPUT_DIR / "ratios"                    # load_data.py
OUT_PREPROCESS = OUTPUT_DIR / "preprocessing"          # load_data.py (Outlier-Report)
OUT_AR = OUTPUT_DIR / "ar"                            # ar_model.py
OUT_CLUSTER = OUTPUT_DIR / "clustering"               # classify.py
OUT_INTERDEP = OUTPUT_DIR / "interdependence"         # interdependence.py
OUT_EXTVAL = OUTPUT_DIR / "external_validation"       # external_validation.py
OUT_EXPLORE = OUTPUT_DIR / "explore"                  # explore.py
OUT_PLOTS = OUTPUT_DIR / "plots"                      # Visualisierungen

# Quelldatei-Mapping (Kurzname → Pfad)
SRC_DIRS: dict[str, Path] = {
    "income": RAW_INCOME,
    "balance": RAW_BALANCE,
    "cashflow": RAW_CASHFLOW,
    "profile": RAW_PROFILE,
}


# ─────────────────────────────────────────────
# Zeitraum & Vollständigkeitsfilter
# ─────────────────────────────────────────────
YEAR_START = 2000
YEAR_END = 2024

EXPECTED_QUARTERS = (YEAR_END - YEAR_START + 1) * 4  # = 100
"""Q1 2000 bis Q4 2024 = 25 Jahre × 4 = 100 Quartale.
Nur Unternehmen, die für *alle* 100 Quartale einen Datenpunkt haben,
kommen in die Analyse. Harter Vollständigkeitsfilter – keine Lücken."""


# ─────────────────────────────────────────────
# Sektor-Exklusion
# ─────────────────────────────────────────────
EXCLUDED_SECTORS = frozenset([
    "Financial Services",
    "Banks",
    "Insurance",
])
"""Finanzsektor wird exkludiert, da fundamental andere Bilanzstruktur
(Leverage = Geschäftsmodell, nicht Risikofaktor). Vgl. Fama & French (1992)."""

PROFILE_SECTOR_COL = "sector"

ADR_NAME_KEYWORDS = frozenset(["ADR", "ADS", "DEPOSITARY"])
"""Ticker werden exkludiert, wenn ihr Profilname eines dieser Schlüsselwörter
enthält.  ADRs (American Depositary Receipts) bilden ausländische Unternehmen
ab, deren Finanzdaten ggf. unter IFRS statt US-GAAP berichtet werden und
die zu Doppelzählungen mit dem Originallisting führen können."""


# ─────────────────────────────────────────────
# Ausreißerbereinigung (Rolling Window)
# ─────────────────────────────────────────────
RAW_COLS: list[str] = [
    "netIncome", "totalAssets", "totalStockholderEquity",
    "ebit", "totalRevenue", "freeCashFlow",
    "totalCurrentAssets", "totalCurrentLiabilities",
    "shortLongTermDebtTotal",
]
"""Rohwert-Spalten, auf die die Rolling-Outlier-Detection angewendet wird
(vor Kennzahlenberechnung)."""

OUTLIER_WINDOW_SIZE = 8
"""Fenstergröße in Quartalen (8 = 2 Jahre)."""

OUTLIER_SIGMA = 3.0
"""Schwelle: |Wert − Median| > SIGMA × Std → Flagging."""

OUTLIER_MIN_FLAGS = 3
"""Mindestanzahl Fenster, die einen Punkt als Ausreißer markieren müssen.
Dreifach-Bestätigung erhöht die Konfidenz und verhindert Fehlkorrekturen."""

OUTLIER_MIN_RATIO = 5.0
"""Mindest-Abweichungsfaktor: |original / corrected| muss ≥ MIN_RATIO sein.
Stellt sicher, dass nur Werte korrigiert werden, die sich um mindestens
das Fünffache vom Korrekturwert unterscheiden."""

OUTLIER_CORRECTION = "window_median"
"""Korrekturstrategie: Ersatz durch Fenster-Median."""

# Cross-Metrik-Paare für Crosscheck (logisch verknüpfte Bilanzpositionen)
CROSS_METRIC_PAIRS: list[tuple[str, str]] = [
    ("netIncome", "ebit"),                             # beide GuV
    ("totalAssets", "totalStockholderEquity"),          # beide Bilanz
    ("totalCurrentAssets", "totalCurrentLiabilities"),  # beide Current
]
"""Logisch verknüpfte Spaltenpaare.  Gleichzeitiges Flagging im selben
Quartal erhöht die Konfidenz für einen API-Fehler."""

OUTLIER_OVERRIDES_PATH = OUT_PREPROCESS / "outlier_overrides.csv"
"""Manuell gepflegte Liste von (ticker, quarter, column)-Tripeln, die
von der automatischen Korrektur ausgenommen werden.  Ermöglicht es,
nach Stichprobenprüfung echte Geschäftsereignisse (z.B. Tax Reform,
Goodwill-Impairment) zu schützen."""

# ─────────────────────────────────────────────
# NaN/Null-Qualitätsfilter
# ─────────────────────────────────────────────
NAN_MAX_QUARTERS = 10
"""Maximal erlaubte fehlende Quartale pro Ticker × Spalte.
Ticker mit mehr als NAN_MAX_QUARTERS fehlenden Werten in einer
Nenner-Spalte (0 oder NaN) oder einer Zähler-Spalte (nur NaN)
werden aus dem Panel entfernt.
Ausnahme: shortLongTermDebtTotal – dort ist NaN häufig ein
Zeichen für fehlende Datenfelder in älteren Filings, kein
Qualitätsproblem."""

# ─────────────────────────────────────────────
# Winsorizing auf Kennzahlen
# ─────────────────────────────────────────────
WINSORIZE_QUANTILES = (0.01, 0.99)
"""Untere und obere Grenze für Winsorisierung der berechneten Kennzahlen.
Werte unterhalb des 1. bzw. oberhalb des 99. Perzentils werden auf
den jeweiligen Schwellenwert gekappt.  Wirkt NACH der Outlier-Detection
auf Rohwerten und NACH der Kennzahlenberechnung.
Begründung: Nahe-null Nenner erzeugen ökonomisch sinnlose Extremratios
(z.B. EBIT/Revenue wenn Revenue ≈ 0).  Die Rohwerte selbst sind korrekt,
aber die resultierenden Kennzahlen verzerren AR-Schätzung und Scatter-Plots."""


# ─────────────────────────────────────────────
# Kennzahlen-Definitionen
# ─────────────────────────────────────────────
@dataclass(frozen=True)
class RatioDef:
    """Definition einer Finanzkennzahl.

    Zwei Modi:
      - Einfacher Quotient: numerator_col / denominator_col (Standard).
      - Komplexe Formel: formula(raw_panel) -> Series, dazu required_cols als
        {src: [col, ...]}, damit der Loader die richtigen Spalten zieht.

    Es muss genau einer der beiden Modi spezifiziert sein.
    """
    name: str               # interner Kurzname
    label: str              # Anzeigename für Plots/Tabellen
    category: str           # Profitabilität / Liquidität / Kapitalstruktur

    # Modus 1: einfacher Quotient (Standard)
    numerator_col: str = ""
    numerator_src: str = ""    # "income" | "balance" | "cashflow"
    denominator_col: str = ""
    denominator_src: str = ""

    # Modus 2: komplexe Formel
    formula: Optional[Callable[[pd.DataFrame], pd.Series]] = None
    required_cols: Optional[dict[str, list[str]]] = None
    # required_cols Beispiel:
    #   {"income": ["totalRevenue", "ebit"], "balance": ["totalCurrentAssets"]}

    def __post_init__(self):
        has_simple = bool(self.numerator_col and self.numerator_src
                          and self.denominator_col and self.denominator_src)
        has_formula = self.formula is not None
        if has_simple and has_formula:
            raise ValueError(
                f"RatioDef {self.name!r}: nicht beides gleichzeitig — "
                "entweder simple (num/den) ODER formula."
            )
        if not (has_simple or has_formula):
            raise ValueError(
                f"RatioDef {self.name!r}: keine Berechnungsvorschrift — "
                "weder simple (num/den) noch formula spezifiziert."
            )
        if has_formula and not self.required_cols:
            raise ValueError(
                f"RatioDef {self.name!r}: formula gesetzt, aber required_cols fehlt. "
                "required_cols muss alle Quellspalten der Formel auflisten."
            )

    @property
    def is_formula(self) -> bool:
        """Returns True wenn diese Kennzahl eine komplexe Formel benutzt."""
        return self.formula is not None

    def iter_required_cols(self):
        """Yieldet (src, col)-Paare aller benötigten Spalten — für beide Modi."""
        if self.is_formula:
            for src, cols in (self.required_cols or {}).items():
                for col in cols:
                    yield src, col
        else:
            yield self.numerator_src, self.numerator_col
            yield self.denominator_src, self.denominator_col


RATIOS: list[RatioDef] = [
    # --- Profitabilität ---
    RatioDef(
        name="ROA",
        label="Return on Assets",
        category="Profitabilität",
        numerator_col="netIncome",
        numerator_src="income",
        denominator_col="totalAssets",
        denominator_src="balance",
    ),
    RatioDef(
        name="ROE",
        label="Return on Equity",
        category="Profitabilität",
        numerator_col="netIncome",
        numerator_src="income",
        denominator_col="totalStockholderEquity",
        denominator_src="balance",
    ),
    RatioDef(
        name="EBIT_margin",
        label="EBIT-Marge",
        category="Profitabilität",
        numerator_col="ebit",
        numerator_src="income",
        denominator_col="totalRevenue",
        denominator_src="income",
    ),
    RatioDef(
        name="fcf_margin",
        label="Free-Cashflow-Marge",
        category="Profitabilität",
        numerator_col="freeCashFlow",
        numerator_src="cashflow",
        denominator_col="totalRevenue",
        denominator_src="income",
    ),
    # --- Liquidität ---
    RatioDef(
        name="current_ratio",
        label="Current Ratio",
        category="Liquidität",
        numerator_col="totalCurrentAssets",
        numerator_src="balance",
        denominator_col="totalCurrentLiabilities",
        denominator_src="balance",
    ),
    # --- Kapitalstruktur ---
    RatioDef(
        name="debt_to_equity",
        label="Debt-to-Equity",
        category="Kapitalstruktur",
        numerator_col="shortLongTermDebtTotal",
        numerator_src="balance",
        denominator_col="totalStockholderEquity",
        denominator_src="balance",
    ),
    RatioDef(
        name="equity_ratio",
        label="Eigenkapitalquote",
        category="Kapitalstruktur",
        numerator_col="totalStockholderEquity",
        numerator_src="balance",
        denominator_col="totalAssets",
        denominator_src="balance",
    ),
]

# ─────────────────────────────────────────────
# Optionale Custom-Kennzahlen (Robustheits- und Explorations-Bausteine)
# ─────────────────────────────────────────────
INCLUDE_CUSTOM_RATIOS: bool = True
"""Wenn True, werden die Kennzahlen aus src/custom_ratios.py an RATIOS angehängt.
Nutzungs-Logik:
  - False (Default) → Hauptanalyse mit den 7 originalen Kennzahlen, Ergebnisse
    in den DOCX-Kapiteln bleiben reproduzierbar.
  - True → CCC, Net Debt/EBITDA, Gross Margin etc. werden zusätzlich geschätzt.
    Outputs in output/ar/ enthalten dann mehr Zeilen pro Ticker.
Empfohlener Workflow:
  - Hauptanalyse mit False fertigschreiben.
  - Zur Exploration / Robustheits-Anhang: True setzen, Pipeline neu laufen lassen,
    explore-Notebook nutzen, Befunde in einem separaten Block diskutieren."""

if INCLUDE_CUSTOM_RATIOS:
    try:
        from .custom_ratios import CUSTOM_RATIOS
    except ImportError:
        # Erlaubt direkten Aufruf von config.py ohne Paket-Kontext
        from custom_ratios import CUSTOM_RATIOS  # type: ignore
    RATIOS = RATIOS + list(CUSTOM_RATIOS)


RATIO_NAMES: list[str] = [r.name for r in RATIOS]


# ─────────────────────────────────────────────
# AR(1)-Modell auf ersten Differenzen
# ─────────────────────────────────────────────
AR_ORDER = 1
"""Lag-Ordnung des AR-Modells. Literaturstandard für Earnings-Persistenz."""

DIFF_ORDER = 1
"""Differenzierungsordnung: ΔY(t) = Y(t) − Y(t−1).
Erste Differenzen machen nicht-stationäre Reihen stationär und
verschieben den Fokus von Niveaus auf Veränderungsraten."""


# ─────────────────────────────────────────────
# Modellvarianten (Multi-Model-Framework)
# ─────────────────────────────────────────────
@dataclass(frozen=True)
class ModelSpec:
    """Spezifikation einer AR-Modellvariante.

    Attributes:
        name:           Kurzname (wird als 'model'-Spalte in ar_features.csv gespeichert)
        label:          Anzeigename für Plots/Tabellen
        diff_order:     Differenzierungsordnung (0 = Levels, 1 = 1. Diff, 4 = saisonal)
        ar_lags:        Anzahl der AR-Lags (1 = AR(1), 2 = AR(2))
        seasonal_diff:  Optionale zusaetzliche saisonale Differenzierung VOR diff_order
                        (0 = aus, 4 = saisonal). Wird zuerst angewandt, dann diff_order auf
                        die saisonbereinigte Reihe. Beispiel: seasonal_diff=4 + diff_order=1
                        ergibt Δ₁Δ₄Y (Box-Jenkins-Filter fuer Quartalsdaten mit Saisonalitaet).
        is_primary:     True = Hauptanalyse, False = Robustheitscheck
    """
    name: str
    label: str
    diff_order: int
    ar_lags: int
    seasonal_diff: int = 0
    is_primary: bool = False


MODEL_SPECS: list[ModelSpec] = [
    ModelSpec(
        name="diff1",
        label="AR(1) auf 1. Differenzen (ΔY)",
        diff_order=1, ar_lags=1, is_primary=True,
    ),
    ModelSpec(
        name="levels",
        label="AR(1) auf Niveaus (Y)",
        diff_order=0, ar_lags=1,
    ),
    ModelSpec(
        name="ar2_diff1",
        label="AR(2) auf 1. Differenzen",
        diff_order=1, ar_lags=2,
    ),
    ModelSpec(
        name="diff4",
        label="AR(1) auf saisonale Differenzen (Δ₄Y)",
        diff_order=4, ar_lags=1,
    ),
    ModelSpec(
        name="diff1_diff4",
        label="AR(1) auf saisonbereinigten 1. Differenzen (Δ₁Δ₄Y)",
        diff_order=1, ar_lags=1, seasonal_diff=4,
    ),
]
"""Alle zu schätzenden Modellvarianten.
diff1 = Hauptanalyse (einheitliche 1. Differenz, vgl. Uniformitäts-Trade-off).
levels = Ergänzende Perspektive (Niveaupersistenz, vgl. Dichev & Tang).
ar2_diff1 = Prüfung auf relevante Lag-2-Effekte.
diff4 = Saisonale Differenzen Y(t) − Y(t−4) für Persistenz von Jahresveränderungen.
diff1_diff4 = Saisonbereinigte 1. Differenzen (Δ₁Δ₄Y) als direkter Saisonalitäts-Check
              für das Hauptmodell."""


# ─────────────────────────────────────────────
# Volatilitätsmaß (zweite Dimension)
# ─────────────────────────────────────────────
# Einfache Standardabweichung der Differenzen σ(ΔY).
# Kein GARCH – bei Quartalsdaten und heterogener Datenlänge
# liefert GARCH(1,1) nur bei ~20 % der Unternehmen
# signifikante Ergebnisse (vgl. Zhu et al. 2025).
# σ(ΔY) ist robust, immer berechenbar und interpretierbar.
VOL_MEASURE = "std_diff"


# ─────────────────────────────────────────────
# Klassifikation – Median-Quadranten
# ─────────────────────────────────────────────
@dataclass(frozen=True)
class QuadrantLabels:
    """Beschriftung der vier Median-Quadranten (φ₁ × σ_ΔY).

    Kontext: AR(1) auf ersten Differenzen ΔY(t) = Y(t) − Y(t−1).
    φ₁ ist fast immer negativ (Mean-Reversion der Veränderungen).
    Die Achsen sind:
      - φ₁: über/unter Median → schwache/starke Mean-Reversion
        (φ₁ nahe 0 = schwach, φ₁ stark negativ = stark)
      - σ(ΔY): über/unter Median → hohe/niedrige Änderungsvolatilität

    "high_phi" = φ₁ über Median = näher an 0 = SCHWACHE Mean-Reversion
    "low_phi"  = φ₁ unter Median = stärker negativ = STARKE Mean-Reversion
    """
    low_phi_low_vol: str = "KORREKTIV-STABIL"     # starke Mean-Reversion, geringe Volatilität
    low_phi_high_vol: str = "KORREKTIV-VOLATIL"    # starke Mean-Reversion, hohe Volatilität
    high_phi_low_vol: str = "PERSISTENT-STABIL"    # schwache Mean-Reversion, geringe Volatilität
    high_phi_high_vol: str = "PERSISTENT-VOLATIL"  # schwache Mean-Reversion, hohe Volatilität


QUADRANT_LABELS = QuadrantLabels()

# K-Means-Parameter
KMEANS_K_RANGE = range(2, 7)
"""Getestete Cluster-Anzahlen. k=2..6 deckt gängige Strukturen ab,
ohne Overfitting bei n≈1000."""

KMEANS_RANDOM_STATE = 42
"""Seed für Reproduzierbarkeit."""


# ─────────────────────────────────────────────
# Interdependenz (FF2)
# ─────────────────────────────────────────────
INTERDEP_ALPHA = 0.05
"""Signifikanzniveau für Korrelationstests und Cramér's V."""


# ─────────────────────────────────────────────
# Externe Validierung (FF3)
# ─────────────────────────────────────────────
EXTVAL_ALPHA = 0.05
"""Signifikanzniveau für Chi²- und Kruskal-Wallis-Tests."""


# ─────────────────────────────────────────────
# Explore (Volatilitäts-Events)
# ─────────────────────────────────────────────
# Parameter werden in explore.py definiert (rolling window, percentile etc.),
# da sie explorativer Natur sind und nicht zur Kern-Methodik gehören.


# ─────────────────────────────────────────────
# Hilfsfunktionen
# ─────────────────────────────────────────────
def ensure_output_dirs() -> None:
    """Legt alle Output-Unterordner an, falls sie nicht existieren."""
    for d in (OUT_RATIOS, OUT_PREPROCESS, OUT_AR, OUT_CLUSTER,
              OUT_INTERDEP, OUT_EXTVAL, OUT_EXPLORE, OUT_PLOTS):
        d.mkdir(parents=True, exist_ok=True)
