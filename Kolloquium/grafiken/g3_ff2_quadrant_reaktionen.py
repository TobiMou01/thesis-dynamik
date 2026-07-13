# -*- coding: utf-8 -*-
"""FF2 / Kapitel 5.2.3 — Quadranten-Reaktionen in den drei Krisen als BOXPLOT
(Design der Masterarbeit, Wiedererkennung zu Abb. 29) — log-Skala + fixe Achsen
über alle drei Krisen für direkte Vergleichbarkeit.

Beobachtungen: |dY| am Peak-Quartal, gepoolt über die vier Profitabilitäts-Kennzahlen
(je Firma x Kennzahl eine Beobachtung), Quadrant = Klassifikation der jeweiligen Kennzahl.
Hauptdaten je Phase wie Kapitel 5.2.3: Dot-Com 2001Q1, GFC 2009Q2, COVID 2020Q3.

Zweite Ausgabe: identische Grafik, aber im Dot-Com-Panel sind die Technologie-
Unternehmen als schwarze Punkte markiert.

Quellen: output/ratios/ratio_panel.csv + output/profiles/company_quadrant_profiles.csv
Ausgabe: g3_ff2_quadrant_reaktionen_boxplot.png · g3b_dotcom_tech_markiert.png
Aufruf:  python3 g3_ff2_quadrant_reaktionen.py
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stil_kolloquium import ROOT, QUADRANT_FARBEN_ARBEIT, arbeit_style, speichern

arbeit_style()

PROFITABILITAET = ["ROA", "ROE", "EBIT_margin", "fcf_margin"]
PHASEN = [("Dot-Com · 2001Q1", "2001Q1"),
          ("Finanzkrise · 2009Q2", "2009Q2"),
          ("COVID · 2020Q3", "2020Q3")]
QUADRANTEN = ["PERSISTENT-VOLATIL", "KORREKTIV-VOLATIL",
              "PERSISTENT-STABIL", "KORREKTIV-STABIL"]

panel = pd.read_csv(ROOT / "output/ratios/ratio_panel.csv").sort_values(["ticker", "quarter"])
prof = pd.read_csv(ROOT / "output/profiles/company_quadrant_profiles.csv")

# |dY| pro Firma x Kennzahl am Peak-Quartal + Quadranten-Zuordnung der Kennzahl
def daten_fuer_phase(q):
    frames = []
    for r in PROFITABILITAET:
        dy = panel.groupby("ticker")[r].diff()
        tmp = panel[["ticker", "quarter"]].copy()
        tmp["ady"] = dy.abs()
        tmp = tmp[tmp.quarter == q].merge(
            prof[["ticker", f"q_{r}", "sector"]].rename(columns={f"q_{r}": "quadrant"}),
            on="ticker")
        frames.append(tmp)
    d = pd.concat(frames)
    return d[(d.ady > 0) & d.quadrant.notna()]

def zeichnen(tech_markieren, dateiname):
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.4), sharex=True)
    pos = np.arange(len(QUADRANTEN))[::-1]
    for ax, (titel, q) in zip(axes, PHASEN):
        d = daten_fuer_phase(q)
        gruppen = [d[d.quadrant == quad].ady.values for quad in QUADRANTEN]
        bp = ax.boxplot(gruppen, positions=pos, vert=False, widths=0.62,
                        patch_artist=True, showfliers=False, whis=(5, 95))
        for patch, quad in zip(bp["boxes"], QUADRANTEN):
            patch.set_facecolor(QUADRANT_FARBEN_ARBEIT[quad])
            patch.set_alpha(0.85)
        for med in bp["medians"]:
            med.set_color("black")
        if tech_markieren and q == "2001Q1":
            t = d[d.sector == "Technology"]
            jitter = (np.random.default_rng(7).random(len(t)) - 0.5) * 0.3
            ypos = t.quadrant.map({qd: p for qd, p in zip(QUADRANTEN, pos)}).values + jitter
            ax.scatter(t.ady.values, ypos, s=14, color="black", alpha=0.7,
                       zorder=5, label="Technologie")
            ax.legend(loc="lower right", frameon=False, fontsize=9)
        ax.set_xscale("log")
        ax.set_xlim(1e-4, 1e0)          # fixe Achse über alle drei Krisen
        ax.set_title(titel, fontsize=12, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        ax.set_xlabel("|ΔY| am Peak-Quartal (Profitabilität, log)", fontsize=9.5)
    axes[0].set_yticks(pos, [q.replace("-", "-\n") for q in QUADRANTEN], fontsize=9)
    for ax in axes[1:]:
        ax.set_yticks(pos, ["" for _ in QUADRANTEN])
    fig.tight_layout()
    speichern(fig, dateiname)

zeichnen(False, "g3_ff2_quadrant_reaktionen_boxplot.png")
zeichnen(True, "g3b_dotcom_tech_markiert.png")
