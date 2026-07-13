# -*- coding: utf-8 -*-
"""
branchen_quadrant_punktwolken.py — Quadranten-Reaktionsboxplots (wie Kolloquium
g3_ff2_quadrant_reaktionen.py / Abb. 29 der Arbeit) mit Punktwolken-Overlay pro
Branche (GICS-Sub-Industry), um Branchen-Cluster innerhalb der Quadranten
sichtbar zu machen — insbesondere zur Prüfung der Aussage:

  "Die Dot-Com-Phase bleibt der einzige Peak ohne signifikante
   Quadranten-Trennung, was den Charakter dieser Phase als
   sektor-spezifische Tech-Krise mit geringer Querschnittsbreite stützt."

Für jede der 122 Branchen (validation_features.csv-Spalte 'industry') wird ein
Bild mit den drei Krisen-Panels (Dot-Com 2001Q1, GFC 2009Q2, COVID 2020Q3)
erzeugt. Die Boxplots zeigen die Gesamtverteilung |ΔY| pro Quadrant (wie im
Original), die Firmen der jeweiligen Branche sind zusätzlich als schwarze
Punkte in ALLEN drei Panels markiert (nicht nur im Dot-Com-Panel wie im
Original-Skript, das nur Technologie markierte).

Zusätzlich wird pro Phase der Kruskal-Wallis-Test über die vier Quadranten auf
genau denselben Daten, die im Plot liegen (|ΔY| am Einzel-Peak-Quartal, gepoolt
über die vier Profitabilitäts-Kennzahlen), im Titel ausgewiesen. Achtung: das
ist NICHT identisch mit dem im Kapitel-5-Text zitierten Test (der nutzt ein
Peak-Quartal ± 1 Fenster, dieses Skript nur das exakte Peak-Quartal wie das
Original-Kolloquium-Skript) — dient hier als schneller Zusatz-Check auf
denselben Boxplot-Daten.

Quellen: output/ratios/ratio_panel.csv + output/profiles/company_quadrant_profiles.csv
Ausgabe: output/plots/branchen_punktwolken/<branche>.png + _manifest.csv
Aufruf:  python3 branchen_quadrant_punktwolken.py
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path("/Users/tobi/Documents/GitHub/Zeitreihenanalyse Finanzkennzahlen")
OUT_DIR = ROOT / "output" / "plots" / "branchen_punktwolken"

PROFITABILITAET = ["ROA", "ROE", "EBIT_margin", "fcf_margin"]
PHASEN = [("Dot-Com · 2001Q1", "2001Q1"),
          ("Finanzkrise · 2009Q2", "2009Q2"),
          ("COVID · 2020Q3", "2020Q3")]
QUADRANTEN = ["PERSISTENT-VOLATIL", "KORREKTIV-VOLATIL",
              "PERSISTENT-STABIL", "KORREKTIV-STABIL"]

# Quadranten-Farben der Arbeit (Abb. 7-9, siehe Kolloquium/grafiken/stil_kolloquium.py)
QUADRANT_FARBEN_ARBEIT = {
    "KORREKTIV-STABIL": "#1f77b4", "KORREKTIV-VOLATIL": "#d62728",
    "PERSISTENT-STABIL": "#2ca02c", "PERSISTENT-VOLATIL": "#ff7f0e",
}


def safe_filename(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[^\w\-]+", "_", name, flags=re.UNICODE)
    return re.sub(r"_+", "_", name).strip("_")


def load_data():
    panel = pd.read_csv(ROOT / "output/ratios/ratio_panel.csv").sort_values(["ticker", "quarter"])
    prof = pd.read_csv(ROOT / "output/profiles/company_quadrant_profiles.csv")
    return panel, prof


def daten_fuer_phase(panel, prof, q):
    """|dY| pro Firma x Kennzahl am Peak-Quartal + Quadranten-Zuordnung der Kennzahl.
    Identisch zur Logik in Kolloquium/grafiken/g3_ff2_quadrant_reaktionen.py."""
    frames = []
    for r in PROFITABILITAET:
        dy = panel.groupby("ticker")[r].diff()
        tmp = panel[["ticker", "quarter"]].copy()
        tmp["ady"] = dy.abs()
        tmp = tmp[tmp.quarter == q].merge(
            prof[["ticker", f"q_{r}", "sector", "industry"]].rename(columns={f"q_{r}": "quadrant"}),
            on="ticker")
        frames.append(tmp)
    d = pd.concat(frames)
    return d[(d.ady > 0) & d.quadrant.notna()]


def kruskal_stat(d):
    groups = [d.loc[d.quadrant == q, "ady"].values for q in QUADRANTEN]
    groups = [g for g in groups if len(g) >= 5]
    if len(groups) < 2:
        return np.nan, np.nan, np.nan
    h, p = stats.kruskal(*groups)
    n = sum(len(g) for g in groups)
    eps2 = h / (n - 1) if n > 1 else np.nan
    return h, p, eps2


def zeichnen_fuer_branche(panel, prof, branche, phasen_daten, phasen_stats, out_path):
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.4), sharex=True)
    pos = np.arange(len(QUADRANTEN))[::-1]

    for ax, (titel, q) in zip(axes, PHASEN):
        d = phasen_daten[q]
        h, p, eps2 = phasen_stats[q]

        gruppen = [d[d.quadrant == quad].ady.values for quad in QUADRANTEN]
        bp = ax.boxplot(gruppen, positions=pos, vert=False, widths=0.62,
                         patch_artist=True, showfliers=False, whis=(5, 95))
        for patch, quad in zip(bp["boxes"], QUADRANTEN):
            patch.set_facecolor(QUADRANT_FARBEN_ARBEIT[quad])
            patch.set_alpha(0.85)
        for med in bp["medians"]:
            med.set_color("black")

        # Punktwolke: Firmen dieser Branche in diesem Phasen-Panel
        t = d[d.industry == branche]
        if len(t) > 0:
            jitter = (np.random.default_rng(7).random(len(t)) - 0.5) * 0.3
            ypos = t.quadrant.map({qd: pp for qd, pp in zip(QUADRANTEN, pos)}).values + jitter
            ax.scatter(t.ady.values, ypos, s=22, color="black", alpha=0.85, zorder=5)
            ax.text(0.02, 0.985, f"n={len(t)}", transform=ax.transAxes,
                    fontsize=8, ha="left", va="top",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.75, edgecolor="none"))

        p_str = "n/a" if np.isnan(p) else (f"{p:.1e}" if p < 0.001 else f"{p:.3f}")
        eps2_str = "n/a" if np.isnan(eps2) else f"{eps2:.3f}"
        ax.set_xscale("log")
        ax.set_xlim(1e-4, 1e0)
        ax.set_title(f"{titel}\nKW p={p_str}, ε²={eps2_str}", fontsize=10.5, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        ax.set_xlabel("|ΔY| am Peak-Quartal (Profitabilität, log)", fontsize=9)

    axes[0].set_yticks(pos, [q.replace("-", "-\n") for q in QUADRANTEN], fontsize=9)
    for ax in axes[1:]:
        ax.set_yticks(pos, ["" for _ in QUADRANTEN])

    fig.suptitle(f"Quadranten-Reaktionen — Branche: {branche}", fontsize=12.5, fontweight="bold", y=1.03)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panel, prof = load_data()

    # Phasen-Daten + Kruskal-Wallis-Stats einmal zentral berechnen (gilt für alle Branchen gleich)
    phasen_daten = {}
    phasen_stats = {}
    for _, q in PHASEN:
        d = daten_fuer_phase(panel, prof, q)
        phasen_daten[q] = d
        phasen_stats[q] = kruskal_stat(d)

    branchen = sorted(prof["industry"].dropna().unique())
    manifest = []

    for branche in branchen:
        n_firms = int((prof["industry"] == branche).sum())
        sektor = prof.loc[prof["industry"] == branche, "sector"].mode()
        sektor = sektor.iloc[0] if len(sektor) else ""
        fname = safe_filename(branche) + ".png"
        out_path = OUT_DIR / fname
        zeichnen_fuer_branche(panel, prof, branche, phasen_daten, phasen_stats, out_path)
        manifest.append({"branche": branche, "sektor": sektor, "n_firmen": n_firms, "datei": fname})
        print(f"  {branche} ({n_firms} Firmen) -> {fname}")

    manifest_df = pd.DataFrame(manifest).sort_values("n_firmen", ascending=False)
    manifest_df.to_csv(OUT_DIR / "_manifest.csv", index=False)
    print(f"\n{len(branchen)} Branchen-Bilder gespeichert in: {OUT_DIR}")
    print(f"Manifest: {OUT_DIR / '_manifest.csv'}")

    # Kruskal-Wallis-Übersicht über alle drei Phasen (gilt fuer alle Branchen-Bilder gleich)
    print("\nKruskal-Wallis (4 Quadranten, |ΔY| am exakten Peak-Quartal, alle Firmen gepoolt):")
    for titel, q in PHASEN:
        h, p, eps2 = phasen_stats[q]
        print(f"  {titel}: H={h:.2f} p={p:.3e} eps2={eps2:.4f}")


if __name__ == "__main__":
    main()
