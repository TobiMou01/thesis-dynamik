"""
custom_ratios.py — Optionale Kennzahlen-Definitionen für Robustheit & Exploration
==================================================================================

Wird nur aktiviert, wenn config.INCLUDE_CUSTOM_RATIOS = True.

Drei Beispiel-Definitionen, die jeweils eine eigene methodische Hypothese
prüfbar machen:

  1. Gross Margin (Bruttomarge)
     — vor allen Kostenarten in der GuV; testet die Markt/Management-These
       aus 4.3.1 noch einmal stärker (je näher am Marktdruck, desto stärker
       die Mean-Reversion).

  2. Cash Conversion Cycle (CCC)
     — Working-Capital-Zyklus in Tagen; bietet eine zweite Liquiditätskennzahl
       mit fundamental anderer Mechanik als die Current Ratio (Strom statt Bestand).

  3. Net Debt / EBITDA
     — Praxis-Standard für Kreditrisiko; mischt Bestand (Net Debt) und Strom
       (EBITDA) und ist damit ein direkter empirischer Test der Strom-Bestand-
       Achse aus dem Vier-Achsen-Modell (Achse 3).

Konvention:
  - Jede Kennzahl ist eine RatioDef-Instanz mit formula + required_cols.
  - Formula nimmt das raw_panel (DataFrame mit Spalten aus required_cols)
    und gibt eine pandas Series mit dem Kennzahl-Wert pro Zeile zurück.
  - Nenner wird wie üblich vor Division replaced(0, np.nan) — das übernimmt
    die Formel selbst, damit der Loader-Code nicht angepasst werden muss.

Erweiterung:
  - Eine neue Kennzahl: hier eine weitere RatioDef definieren und in
    CUSTOM_RATIOS aufnehmen. Pipeline mit INCLUDE_CUSTOM_RATIOS=True
    neu laufen lassen.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from .config import RatioDef
except ImportError:
    from config import RatioDef  # type: ignore


# ─────────────────────────────────────────────
# 1. Gross Margin
# ─────────────────────────────────────────────
def _gross_margin(raw: pd.DataFrame) -> pd.Series:
    """Gross Margin = grossProfit / totalRevenue.

    Falls grossProfit nicht verfügbar ist, wird er als
    totalRevenue − costOfRevenue abgeleitet.
    """
    rev = raw["totalRevenue"].replace(0, np.nan)
    if "grossProfit" in raw.columns and raw["grossProfit"].notna().any():
        gross = raw["grossProfit"]
    else:
        gross = raw["totalRevenue"] - raw["costOfRevenue"]
    return gross / rev


GROSS_MARGIN = RatioDef(
    name="gross_margin",
    label="Bruttomarge",
    category="Profitabilität",
    formula=_gross_margin,
    required_cols={"income": ["totalRevenue", "grossProfit", "costOfRevenue"]},
)


# ─────────────────────────────────────────────
# 2. Cash Conversion Cycle (CCC)
# ─────────────────────────────────────────────
def _ccc(raw: pd.DataFrame) -> pd.Series:
    """Cash Conversion Cycle in Tagen.

    CCC = DSO + DIO − DPO
        = (AR / Sales)·91,25 + (Inv / COGS)·91,25 − (AP / COGS)·91,25

    91,25 = 365 / 4 — Quartalskonvention statt Tageskonvention,
    damit die Werte als „Tage je Quartal" interpretierbar sind.
    """
    sales_q = raw["totalRevenue"].replace(0, np.nan)
    cogs_q = raw["costOfRevenue"].replace(0, np.nan)
    days_per_q = 365 / 4

    dso = (raw["netReceivables"] / sales_q) * days_per_q
    dio = (raw["inventory"] / cogs_q) * days_per_q
    dpo = (raw["accountsPayable"] / cogs_q) * days_per_q
    return dso + dio - dpo


CASH_CONVERSION_CYCLE = RatioDef(
    name="cash_conversion_cycle",
    label="Cash Conversion Cycle (Tage)",
    category="Liquidität",
    formula=_ccc,
    required_cols={
        "income": ["totalRevenue", "costOfRevenue"],
        "balance": ["netReceivables", "inventory", "accountsPayable"],
    },
)



# ─────────────────────────────────────────────
# 4. Quick Ratio (Acid-Test)
# ─────────────────────────────────────────────
def _quick_ratio(raw: pd.DataFrame) -> pd.Series:
    """Quick Ratio = (Current Assets − Inventory) / Current Liabilities.

    Strengeres Liquiditaetsmass als Current Ratio, weil Vorraete (illiquid)
    aus dem Zaehler herausgerechnet werden.
    """
    cur_assets = raw["totalCurrentAssets"]
    inv = raw["inventory"].fillna(0) if "inventory" in raw.columns else 0
    cur_liab = raw["totalCurrentLiabilities"].replace(0, np.nan)
    return (cur_assets - inv) / cur_liab


QUICK_RATIO = RatioDef(
    name="quick_ratio",
    label="Quick Ratio",
    category="Liquidität",
    formula=_quick_ratio,
    required_cols={"balance": ["totalCurrentAssets", "inventory", "totalCurrentLiabilities"]},
)


# ─────────────────────────────────────────────
# 3. Net Debt / EBITDA
# ─────────────────────────────────────────────
def _net_debt_ebitda(raw: pd.DataFrame) -> pd.Series:
    """Net Debt / EBITDA.

    Net Debt = shortLongTermDebtTotal − cash − shortTermInvestments
    (Negative Net Debt = Netto-Cash-Position; bleibt im Quotienten erhalten,
    weil ökonomisch interpretierbar als „so viele EBITDA-Quartale Cash-Reserve".)
    """
    debt = raw["shortLongTermDebtTotal"]
    cash = raw["cash"].fillna(0) if "cash" in raw.columns else 0
    sti = raw["shortTermInvestments"].fillna(0) if "shortTermInvestments" in raw.columns else 0
    net_debt = debt - cash - sti

    ebitda = raw["ebitda"].replace(0, np.nan)
    return net_debt / ebitda


NET_DEBT_EBITDA = RatioDef(
    name="net_debt_ebitda",
    label="Net Debt / EBITDA",
    category="Kapitalstruktur",
    formula=_net_debt_ebitda,
    required_cols={
        "balance": ["shortLongTermDebtTotal", "cash", "shortTermInvestments"],
        "income": ["ebitda"],
    },
)


# ─────────────────────────────────────────────
# Liste — wird in config.py importiert wenn INCLUDE_CUSTOM_RATIOS = True
# ─────────────────────────────────────────────
CUSTOM_RATIOS: list[RatioDef] = [
    # GROSS_MARGIN,  # Profitabilitaet — deaktiviert nach Hypothesen-Test (28.04.2026): Bruttomarge zeigt schwaechste Mean-Reversion (-0.36) statt staerkste, Hypothese widerlegt. Definition bleibt erhalten fuer eventuelle Re-Aktivierung.
    CASH_CONVERSION_CYCLE,
    QUICK_RATIO,
    NET_DEBT_EBITDA,
]
