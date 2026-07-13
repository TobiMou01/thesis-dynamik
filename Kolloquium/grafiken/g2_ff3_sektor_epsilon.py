# -*- coding: utf-8 -*-
"""FF3 / Kapitel 6.2.1 — Kruskal-Wallis-Sektoreffekt epsilon^2 im Design der Masterarbeit.
Horizontale Balken je Kennzahl: sigma (dunkelblau) vs. phi (hellgrau) auf gleicher Skala —
die Farben tragen genau eine Botschaft: sigma substanziell, phi klein. Ohne Sterne.
Quelle: output/ff3/kruskal_wallis_sektor.csv  ->  g2_ff3_sektor_epsilon.png
Aufruf:  python3 g2_ff3_sektor_epsilon.py
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stil_kolloquium import ROOT, KENNZAHLEN, LABELS, arbeit_style, speichern

arbeit_style()
df = pd.read_csv(ROOT / "output/ff3/kruskal_wallis_sektor.csv")

FARBE_SIGMA = "#1f77b4"   # Standard-Blau der Arbeit
FARBE_PHI = "#c7c7c7"     # neutrales Grau

fig, ax = plt.subplots(figsize=(11.0, 4.8))
y = np.arange(len(KENNZAHLEN))[::-1]
h = 0.36
for kz, yy in zip(KENNZAHLEN, y):
    for param, offset, farbe in [("sigma", +h/2 + 0.02, FARBE_SIGMA),
                                 ("phi",   -h/2 - 0.02, FARBE_PHI)]:
        z = df[(df.ratio == kz) & (df.param == param)].iloc[0]
        ax.barh(yy + offset, z.epsilon_squared, height=h, color=farbe, zorder=3)
        ax.text(z.epsilon_squared + 0.003, yy + offset,
                f"{z.epsilon_squared:.2f}".replace(".", ","),
                va="center", fontsize=9, color="black")

ax.set_yticks(y, [LABELS[k] for k in KENNZAHLEN], fontsize=11)
ax.set_xlim(0, 0.26)
ax.set_xlabel("Kruskal-Wallis ε² — durch den Sektor erklärter Anteil der Variation")
ax.grid(axis="x", alpha=0.3, zorder=0)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=FARBE_SIGMA, label="σ"),
                   plt.Rectangle((0, 0), 1, 1, color=FARBE_PHI, label="φ")],
          loc="lower right", frameon=False, fontsize=12)
speichern(fig, "g2_ff3_sektor_epsilon.png")
