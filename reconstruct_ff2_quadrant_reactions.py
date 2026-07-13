# -*- coding: utf-8 -*-
"""
reconstruct_ff2_quadrant_reactions.py — Rekonstruktion von output/plots/ff2_quadrant_reactions.png

Das Original-Skript ("explore.py", siehe Kommentar in src/config.py Zeile 458)
existiert nicht mehr im Projekt. Diese Datei rekonstruiert die Abbildung anhand
von Pixelmessungen im vorhandenen PNG (Balkenlaengen, Fehlerbalken-Enden,
Achsenskalen) und der an anderer Stelle im Projekt dokumentierten Methodik
(peak_windows.csv, quadrant_<ratio>-Spalten in validation_features.csv).

Bestaetigt (Abweichung < 10% zu den Pixelmessungen der Originalgrafik):
- Datengrundlage: output/ratios/ratio_panel.csv + output/external_validation/validation_features.csv
- Krisenfenster: Haupt-Peak-Quartal +/- 1 Quartal (Dot-Com 2001Q1, GFC 2009Q2,
  COVID 2020Q3) - identisch zur Fenster-Definition, die auch den im Kapitel-5-Text
  zitierten Mann-Whitney-/Kruskal-Wallis-Kennzahlen zugrunde liegt.
- Balkenwert ("Mittl. Median ΔY"): Pro Kennzahl (ROA, ROE, EBIT_margin, fcf_margin)
  wird ΔY je Ticker im Fenster gebildet, nach der jeweiligen Kennzahl-eigenen
  Quadranten-Klassifikation (quadrant_<ratio> aus validation_features.csv)
  gruppiert und der Median gebildet. Der Balken zeigt den Mittelwert dieser
  vier Kennzahl-Mediane pro Quadrant.
- Farben, Reihenfolge der Quadranten, Titel und Achsenbeschriftung sind per
  Pixelabgleich (exakte Farbwerte, Titeltext-Fragmente in analysis.ipynb)
  bestaetigt.

NICHT zweifelsfrei rekonstruierbar:
- Die exakte Fehlerbalken-Formel. Zwei Kandidaten stehen zur Wahl (siehe
  ERROR_METRIC unten):
    "std" -> Standardabweichung der gepoolten ΔY-Werte. Trifft die stabilen
             Quadranten zu breit (ca. 3-4x zu groß), die volatilen eher zu breit.
    "iqr" -> (Q75-Q25)/1.349, robuste Std-Schätzung. Trifft die stabilen
             Quadranten fast exakt, die volatilen eher zu schmal (ca. 2-3x zu klein).
  Keine der beiden Varianten trifft beide Quadranten-Typen gleichzeitig exakt.
  Falls die urspruengliche Formel noch bekannt ist, bitte hier nachtragen.

Ausgabe: output/plots/ff2_quadrant_reactions_reconstructed.png (bzw. _iqr.png)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = "/Users/tobi/Documents/GitHub/Zeitreihenanalyse Finanzkennzahlen/"

PROFIT_RATIOS = ["ROA", "ROE", "EBIT_margin", "fcf_margin"]

# Reihenfolge unten -> oben im barh (ergibt oben->unten wie im Original:
# PERSISTENT-VOLATIL, KORREKTIV-VOLATIL, PERSISTENT-STABIL, KORREKTIV-STABIL)
QUAD_ORDER = ["KORREKTIV-STABIL", "PERSISTENT-STABIL", "KORREKTIV-VOLATIL", "PERSISTENT-VOLATIL"]

# Exakte Material-Design-Farben aus dem Projekt (analysis.ipynb, Zelle 37 / 77)
QUAD_COLORS = {
    "KORREKTIV-STABIL": "#2196F3",
    "KORREKTIV-VOLATIL": "#F44336",
    "PERSISTENT-STABIL": "#4CAF50",
    "PERSISTENT-VOLATIL": "#FF9800",
}

CRISES = [
    ("Dot-Com 2001", "2001Q1"),
    ("GFC 2009", "2009Q2"),
    ("COVID 2020", "2020Q3"),
]

ERROR_METRIC = "std"  # "std" (Default) oder "iqr" -- siehe Docstring oben


def load_data():
    panel = pd.read_csv(ROOT + "output/ratios/ratio_panel.csv")
    validation = pd.read_csv(ROOT + "output/external_validation/validation_features.csv")
    return panel, validation


def window_quarters(all_quarters, center, half=1):
    idx = {q: i for i, q in enumerate(all_quarters)}
    ci = idx[center]
    return [all_quarters[i] for i in range(max(0, ci - half), min(len(all_quarters), ci + half + 1))]


def dy_for_ratio(panel, ratio):
    p = panel.sort_values(["ticker", "quarter"])
    df = p[["ticker", "quarter"]].copy()
    df["dy"] = p.groupby("ticker")[ratio].diff()
    return df.dropna(subset=["dy"])


def crisis_bar_and_error(panel, validation, all_quarters, center_quarter, error_metric=ERROR_METRIC):
    quarters = window_quarters(all_quarters, center_quarter, half=1)
    pooled = {q: [] for q in QUAD_ORDER}
    per_ratio_median = {q: [] for q in QUAD_ORDER}

    for ratio in PROFIT_RATIOS:
        qcol = f"quadrant_{ratio}"
        grp = validation[["ticker", qcol]].rename(columns={qcol: "quadrant"})
        dy = dy_for_ratio(panel, ratio)
        dy = dy[dy["quarter"].isin(quarters)]
        dy = dy.merge(grp, on="ticker", how="left").dropna(subset=["quadrant"])
        med = dy.groupby("quadrant")["dy"].median()
        for q in QUAD_ORDER:
            if q in med.index:
                per_ratio_median[q].append(med[q])
            pooled[q].extend(dy.loc[dy["quadrant"] == q, "dy"].values)

    bar = {q: np.mean(per_ratio_median[q]) for q in QUAD_ORDER}

    err = {}
    for q in QUAD_ORDER:
        arr = np.array(pooled[q])
        if error_metric == "iqr":
            q25, q75 = np.percentile(arr, [25, 75])
            err[q] = (q75 - q25) / 1.349
        else:
            err[q] = np.std(arr)

    return bar, err


def make_plot(error_metric, out_name):
    panel, validation = load_data()
    all_quarters = sorted(panel["quarter"].unique())

    fig, axes = plt.subplots(1, 3, figsize=(20, 6.9))
    fig.suptitle("Quadrant-Reaktionen: Wie reagieren verschiedene Dynamik-Typen?",
                 fontsize=15, fontweight="bold", y=0.99)

    y_pos = np.arange(len(QUAD_ORDER))

    for ax, (label, center_quarter) in zip(axes, CRISES):
        bar, err = crisis_bar_and_error(panel, validation, all_quarters, center_quarter,
                                         error_metric=error_metric)

        values = [bar[q] for q in QUAD_ORDER]
        errors = [err[q] for q in QUAD_ORDER]
        colors = [QUAD_COLORS[q] for q in QUAD_ORDER]

        ax.barh(y_pos, values, xerr=errors, color=colors,
                error_kw=dict(ecolor="gray", capsize=4, linewidth=1.2))
        ax.axvline(0, color="black", linewidth=1.0)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(QUAD_ORDER, fontsize=11)
        ax.set_title(label, fontsize=13, fontweight="bold")
        ax.set_xlabel("Mittl. Median ΔY (Profitabilität)", fontsize=10)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = ROOT + f"output/plots/{out_name}"
    fig.savefig(out_path, dpi=112, bbox_inches=None)
    print(f"Gespeichert: {out_path}")


def main():
    make_plot("std", "ff2_quadrant_reactions_reconstructed.png")
    make_plot("iqr", "ff2_quadrant_reactions_reconstructed_iqr.png")


if __name__ == "__main__":
    main()
