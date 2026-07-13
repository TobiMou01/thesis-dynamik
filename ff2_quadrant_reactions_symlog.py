# -*- coding: utf-8 -*-
"""
ff2_quadrant_reactions_symlog.py — Abbildung 29 (Original-Balkendiagramm), neu
dargestellt mit symmetrisch-logarithmischer x-Achse statt linearer Achse.

Ändert NICHTS an den Werten, nur an der Achsen-Transformation: 0 in der Mitte,
danach Verdopplungs-Schritte (0,01 / 0,02 / 0,04 / 0,08 / 0,16 / 0,32) statt
linearer Skala. So bleiben die kleinen Balken der stabilen Quadranten sichtbar,
obwohl die Fehlerbalken der volatilen Quadranten sehr viel breiter sind.
Beschriftet werden nur 0, ±0,01, ±0,04, ±0,16 (schlanke Auswahl, keine
Zahlen-Überladung).

Herkunft der Werte:
- Balkenwerte (Mittl. Median ΔY): exakt nachgerechnet aus
  output/ratios/ratio_panel.csv + output/external_validation/validation_features.csv
  (Peak-Quartal ± 1, Mittelwert der vier Kennzahl-Mediane ROA/ROE/EBIT_margin/
  fcf_margin pro Quadrant) — verifiziert, < 10% Abweichung zur Pixelmessung
  des Originalbilds output/plots/ff2_quadrant_reactions.png.
- Fehlerbalken (Halbbreite): aus Pixelmessung des Originalbilds. Die exakte
  Berechnungsformel des verlorenen Original-Skripts ("explore.py") ließ sich
  nicht zweifelsfrei rekonstruieren (siehe reconstruct_ff2_quadrant_reactions.py) —
  diese Werte sind eine Messung des Originalbilds, keine Neuberechnung.

Ausgabe: output/plots/ff2_quadrant_reactions_symlog.png
Aufruf:  python3 ff2_quadrant_reactions_symlog.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter

ROOT = "/Users/tobi/Documents/GitHub/Zeitreihenanalyse Finanzkennzahlen/"

QUAD_ORDER = ["KORREKTIV-STABIL", "PERSISTENT-STABIL", "KORREKTIV-VOLATIL", "PERSISTENT-VOLATIL"]
QUAD_COLORS = {
    "KORREKTIV-STABIL": "#1f77b4", "KORREKTIV-VOLATIL": "#d62728",
    "PERSISTENT-STABIL": "#2ca02c", "PERSISTENT-VOLATIL": "#ff7f0e",
}

# Balkenwerte (Mittl. Median ΔY) -- nachgerechnet, verifiziert
BAR = {
    "Dot-Com 2001": {"KORREKTIV-STABIL": 0.0014, "PERSISTENT-STABIL": 0.0004,
                      "KORREKTIV-VOLATIL": -0.0007, "PERSISTENT-VOLATIL": 0.0003},
    "GFC 2009": {"KORREKTIV-STABIL": 0.0034, "PERSISTENT-STABIL": 0.0060,
                  "KORREKTIV-VOLATIL": 0.0102, "PERSISTENT-VOLATIL": 0.0127},
    "COVID 2020": {"KORREKTIV-STABIL": 0.0060, "PERSISTENT-STABIL": 0.0062,
                    "KORREKTIV-VOLATIL": 0.0085, "PERSISTENT-VOLATIL": 0.0083},
}

# Fehlerbalken (Halbbreite) -- aus Pixelmessung des Originalbilds
ERR = {
    "Dot-Com 2001": {"KORREKTIV-STABIL": 0.0229, "PERSISTENT-STABIL": 0.0206,
                       "KORREKTIV-VOLATIL": 0.2073, "PERSISTENT-VOLATIL": 0.2480},
    "GFC 2009": {"KORREKTIV-STABIL": 0.0189, "PERSISTENT-STABIL": 0.0217,
                  "KORREKTIV-VOLATIL": 0.1630, "PERSISTENT-VOLATIL": 0.1705},
    "COVID 2020": {"KORREKTIV-STABIL": 0.0244, "PERSISTENT-STABIL": 0.0241,
                    "KORREKTIV-VOLATIL": 0.0984, "PERSISTENT-VOLATIL": 0.1529},
}

LINTHRESH = 0.01
TICK_GRID = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
ALL_TICKS = sorted([-t for t in TICK_GRID] + [0] + TICK_GRID)
LABELED = {0.0, 0.01, 0.04, 0.16, -0.01, -0.04, -0.16}


def fmt(x, pos):
    if x in LABELED or -x in LABELED:
        if x == 0:
            return "0"
        return f"{x:.2f}".rstrip("0").rstrip(".")
    return ""


def main():
    fig, axes = plt.subplots(1, 3, figsize=(20, 6.9))
    fig.suptitle("Quadrant-Reaktionen: Wie reagieren verschiedene Dynamik-Typen?",
                 fontsize=15, fontweight="bold", y=0.99)

    y_pos = np.arange(len(QUAD_ORDER))

    for ax, phase in zip(axes, BAR.keys()):
        values = [BAR[phase][q] for q in QUAD_ORDER]
        errors = [ERR[phase][q] for q in QUAD_ORDER]
        colors = [QUAD_COLORS[q] for q in QUAD_ORDER]

        ax.barh(y_pos, values, xerr=errors, color=colors,
                error_kw=dict(ecolor="gray", capsize=4, linewidth=1.2))
        ax.axvline(0, color="black", linewidth=1.0)

        ax.set_xscale("symlog", linthresh=LINTHRESH, linscale=1.0)
        ax.xaxis.set_major_locator(FixedLocator(ALL_TICKS))
        ax.xaxis.set_major_formatter(FuncFormatter(fmt))
        ax.xaxis.set_minor_formatter(NullFormatter())
        max_abs = max(abs(v) + e for v, e in zip(values, errors))
        ax.set_xlim(-max_abs * 1.15, max_abs * 1.15)

        ax.set_yticks(y_pos)
        if ax is axes[0]:
            ax.set_yticklabels(QUAD_ORDER, fontsize=11)
        else:
            ax.set_yticklabels(["" for _ in QUAD_ORDER])
        ax.set_title(phase, fontsize=13, fontweight="bold")
        ax.set_xlabel("Mittl. Median ΔY (Profitabilität)", fontsize=10)
        ax.grid(axis="x", which="major", alpha=0.25)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out = ROOT + "output/plots/ff2_quadrant_reactions_symlog.png"
    fig.savefig(out, dpi=112)
    print("gespeichert:", out)


if __name__ == "__main__":
    main()
