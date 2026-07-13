# -*- coding: utf-8 -*-
"""Gemeinsames Dark-Design für alle Kolloquium-Grafiken.
Farbwerte exakt aus dem Foliendeck ausgelesen (Master + Folienobjekte)."""
from pathlib import Path
import matplotlib as mpl

# Repo-Wurzel (grafiken/ liegt in Kolloquium/, Kolloquium liegt in der Repo-Wurzel)
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

# ---- Deck-Farben ----
BG      = "#082E1C"   # Folien-Hintergrund (Master)
CARD    = "#153B29"   # Kartenfläche
TEXT    = "#F2EFDA"   # Haupttext
SAGE    = "#B3BC9A"   # Sekundärtext
GREY    = "#798D6F"   # Tertiärtext / Achsen
BLUE    = "#79A2F9"   # Profitabilität
YELLOW  = "#E6D34F"   # Liquidität
CORAL   = "#F36451"   # Kapitalstruktur

# Quadranten (aus Folie "Drei Dynamiktypen")
Q_KV = "#6AA7F4"; Q_PV = "#F36451"; Q_KS = "#3EB977"; Q_PS = "#E4CA5F"
QUADRANT_FARBEN = {
    "KORREKTIV-VOLATIL": Q_KV, "PERSISTENT-VOLATIL": Q_PV,
    "KORREKTIV-STABIL": Q_KS, "PERSISTENT-STABIL": Q_PS,
}

# ---- Kennzahlen: Reihenfolge, Anzeigename, Gruppenfarbe ----
KENNZAHLEN = ["ROA", "ROE", "EBIT_margin", "fcf_margin",
              "current_ratio", "debt_to_equity", "equity_ratio"]
LABELS = {"ROA": "ROA", "ROE": "ROE", "EBIT_margin": "EBIT-Marge",
          "fcf_margin": "FCF-Marge", "current_ratio": "Current Ratio",
          "debt_to_equity": "Debt/Equity", "equity_ratio": "EK-Quote"}
GRUPPE = {"ROA": BLUE, "ROE": BLUE, "EBIT_margin": BLUE, "fcf_margin": BLUE,
          "current_ratio": YELLOW, "debt_to_equity": CORAL, "equity_ratio": CORAL}

STRUKTURVARIABLEN = {   # Reihenfolge wie Kapitel 6.1
    "market_cap": "Marktkap.", "total_assets_median": "Bilanzsumme",
    "employees": "Mitarbeiter", "ppe_to_ta_median": "Anlagen-Int.",
    "capex_to_ta_median": "Investitions-Int.", "roa_median": "Median-Prof.",
    "accruals_median": "Accruals",
}

def arbeit_style():
    """Design der Masterarbeit: weißer Hintergrund, matplotlib-Standard (wie die Plots in output/)."""
    mpl.rcdefaults()
    mpl.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight",
        "font.size": 11,
    })

# Quadranten-Farben der Arbeit (Abb. 7–9, matplotlib-Standard)
QUADRANT_FARBEN_ARBEIT = {
    "KORREKTIV-STABIL": "#1f77b4", "KORREKTIV-VOLATIL": "#d62728",
    "PERSISTENT-STABIL": "#2ca02c", "PERSISTENT-VOLATIL": "#ff7f0e",
}

def dark_style():
    """rcParams für das Deck-Design setzen."""
    mpl.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
        "text.color": TEXT, "axes.edgecolor": GREY, "axes.labelcolor": SAGE,
        "xtick.color": SAGE, "ytick.color": SAGE,
        "axes.titlecolor": TEXT, "axes.titleweight": "bold",
        "font.family": "sans-serif", "font.size": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight",
    })

def speichern(fig, name):
    p = OUT / name
    fig.savefig(p)  # Hintergrund folgt dem aktiven Stil (arbeit_style = weiß, dark_style = Deck-Grün)
    print("gespeichert:", p)
