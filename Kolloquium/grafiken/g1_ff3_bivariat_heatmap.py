# -*- coding: utf-8 -*-
"""FF3 / Kapitel 6.1 — Bivariate Spearman-Heatmap im Design der Masterarbeit.
Zwei Panels (sigma links, phi rechts), RdBu-Farbskala wie die 6_1er-Plots der Arbeit,
bewusst OHNE Signifikanz-Sterne (Folien-Version, schlicht).
Quelle: output/ff3/bivariate_spearman.csv  ->  g1_ff3_bivariat_heatmap.png
Aufruf:  python3 g1_ff3_bivariat_heatmap.py
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stil_kolloquium import (ROOT, KENNZAHLEN, LABELS, STRUKTURVARIABLEN,
                             arbeit_style, speichern)

arbeit_style()
df = pd.read_csv(ROOT / "output/ff3/bivariate_spearman.csv")
svars = list(STRUKTURVARIABLEN)

fig, axes = plt.subplots(1, 2, figsize=(13.4, 5.0))
for ax, param, titel in [(axes[0], "sigma", "Spearman ρ — σ"), (axes[1], "phi", "Spearman ρ — φ")]:
    sub = df[df.param == param]
    rho = np.full((len(svars), len(KENNZAHLEN)), np.nan)
    for i, sv in enumerate(svars):
        for j, kz in enumerate(KENNZAHLEN):
            z = sub[(sub.struct_var == sv) & (sub.ratio == kz)]
            if len(z):
                rho[i, j] = z.spearman_rho.iloc[0]
    im = ax.imshow(rho, cmap="RdBu_r", vmin=-0.55, vmax=0.55, aspect="auto")
    for i in range(len(svars)):
        for j in range(len(KENNZAHLEN)):
            dunkel = abs(rho[i, j]) > 0.33
            ax.text(j, i, f"{rho[i, j]:+.2f}".replace(".", ","),
                    ha="center", va="center", fontsize=9,
                    color="white" if dunkel else "black")
    ax.set_xticks(range(len(KENNZAHLEN)), [LABELS[k] for k in KENNZAHLEN],
                  rotation=35, ha="right", fontsize=10)
    if ax is axes[0]:
        ax.set_yticks(range(len(svars)), [STRUKTURVARIABLEN[s] for s in svars], fontsize=10)
    else:
        ax.set_yticks(range(len(svars)), ["" for _ in svars])
    ax.set_title(titel, fontsize=13)

cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02)
cb.set_label("ρ")
speichern(fig, "g1_ff3_bivariat_heatmap.png")
