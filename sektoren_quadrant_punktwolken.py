# -*- coding: utf-8 -*-
"""
sektoren_quadrant_punktwolken.py — wie branchen_quadrant_punktwolken.py, aber
auf Sektor-Ebene (die zehn/elf GICS-Hauptgruppen, Spalte 'sector' in
company_quadrant_profiles.csv), nicht auf Branchen-Ebene (GICS-Sub-Industry).

Grund: Die zu prüfende Aussage im Kapitel-5-Text spricht explizit von
"sektor-spezifischer Tech-Krise" — die relevante Gruppierung dafür ist der
Sektor "Technology" (einer von zehn GICS-Hauptsektoren), nicht eine einzelne
Sub-Branche wie "Semiconductors".

Quellen: output/ratios/ratio_panel.csv + output/profiles/company_quadrant_profiles.csv
Ausgabe: output/plots/sektoren_punktwolken/<sektor>.png + _manifest.csv
Aufruf:  python3 sektoren_quadrant_punktwolken.py
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path("/Users/tobi/Documents/GitHub/Zeitreihenanalyse Finanzkennzahlen")
OUT_DIR = ROOT / "output" / "plots" / "sektoren_punktwolken"

PROFITABILITAET = ["ROA", "ROE", "EBIT_margin", "fcf_margin"]
PHASEN = [("Dot-Com · 2001Q1", "2001Q1"),
          ("Finanzkrise · 2009Q2", "2009Q2"),
          ("COVID · 2020Q3", "2020Q3")]
QUADRANTEN = ["PERSISTENT-VOLATIL", "KORREKTIV-VOLATIL",
              "PERSISTENT-STABIL", "KORREKTIV-STABIL"]

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


def kruskal_stat_subset(d, sektor):
    """Kruskal-Wallis NUR innerhalb dieses Sektors (zusätzlich zur Gesamt-Stat)."""
    sub = d[d.sector == sektor]
    return kruskal_stat(sub)


def zeichnen_fuer_sektor(sektor, phasen_daten, phasen_stats_gesamt, out_path):
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.6), sharex=True)
    pos = np.arange(len(QUADRANTEN))[::-1]

    for ax, (titel, q) in zip(axes, PHASEN):
        d = phasen_daten[q]
        h, p, eps2 = phasen_stats_gesamt[q]
        h_s, p_s, eps2_s = kruskal_stat_subset(d, sektor)

        gruppen = [d[d.quadrant == quad].ady.values for quad in QUADRANTEN]
        bp = ax.boxplot(gruppen, positions=pos, vert=False, widths=0.62,
                         patch_artist=True, showfliers=False, whis=(5, 95))
        for patch, quad in zip(bp["boxes"], QUADRANTEN):
            patch.set_facecolor(QUADRANT_FARBEN_ARBEIT[quad])
            patch.set_alpha(0.85)
        for med in bp["medians"]:
            med.set_color("black")

        t = d[d.sector == sektor]
        if len(t) > 0:
            jitter = (np.random.default_rng(7).random(len(t)) - 0.5) * 0.3
            ypos = t.quadrant.map({qd: pp for qd, pp in zip(QUADRANTEN, pos)}).values + jitter
            ax.scatter(t.ady.values, ypos, s=22, color="black", alpha=0.85, zorder=5)
            ax.text(0.02, 0.985, f"n={len(t)}", transform=ax.transAxes,
                    fontsize=8, ha="left", va="top",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.75, edgecolor="none"))

        p_str = "n/a" if np.isnan(p) else (f"{p:.1e}" if p < 0.001 else f"{p:.3f}")
        eps2_str = "n/a" if np.isnan(eps2) else f"{eps2:.3f}"
        ps_str = "n/a" if np.isnan(p_s) else (f"{p_s:.1e}" if p_s < 0.001 else f"{p_s:.3f}")
        eps2s_str = "n/a" if np.isnan(eps2_s) else f"{eps2_s:.3f}"

        ax.set_xscale("log")
        ax.set_xlim(1e-4, 1e0)
        ax.set_title(f"{titel}\nGesamt: KW p={p_str}, ε²={eps2_str}\n"
                      f"Nur {sektor}: KW p={ps_str}, ε²={eps2s_str}",
                      fontsize=9.5, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        ax.set_xlabel("|ΔY| am Peak-Quartal (Profitabilität, log)", fontsize=9)

    axes[0].set_yticks(pos, [q.replace("-", "-\n") for q in QUADRANTEN], fontsize=9)
    for ax in axes[1:]:
        ax.set_yticks(pos, ["" for _ in QUADRANTEN])

    fig.suptitle(f"Quadranten-Reaktionen — Sektor: {sektor}", fontsize=13, fontweight="bold", y=1.05)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panel, prof = load_data()

    phasen_daten = {}
    phasen_stats = {}
    for _, q in PHASEN:
        d = daten_fuer_phase(panel, prof, q)
        phasen_daten[q] = d
        phasen_stats[q] = kruskal_stat(d)

    sektoren = sorted(prof["sector"].dropna().unique())
    manifest = []

    for sektor in sektoren:
        n_firms = int((prof["sector"] == sektor).sum())
        fname = safe_filename(sektor) + ".png"
        out_path = OUT_DIR / fname
        zeichnen_fuer_sektor(sektor, phasen_daten, phasen_stats, out_path)

        row = {"sektor": sektor, "n_firmen": n_firms, "datei": fname}
        for titel, q in PHASEN:
            h_s, p_s, eps2_s = kruskal_stat_subset(phasen_daten[q], sektor)
            row[f"p_{q}"] = p_s
            row[f"eps2_{q}"] = eps2_s
        manifest.append(row)
        print(f"  {sektor} ({n_firms} Firmen) -> {fname}")

    manifest_df = pd.DataFrame(manifest).sort_values("n_firmen", ascending=False)
    manifest_df.to_csv(OUT_DIR / "_manifest.csv", index=False)
    print(f"\n{len(sektoren)} Sektor-Bilder gespeichert in: {OUT_DIR}")
    print(f"Manifest: {OUT_DIR / '_manifest.csv'}")

    print("\nKruskal-Wallis GESAMT (alle Firmen, 4 Quadranten, |ΔY| exaktes Peak-Quartal):")
    for titel, q in PHASEN:
        h, p, eps2 = phasen_stats[q]
        print(f"  {titel}: H={h:.2f} p={p:.3e} eps2={eps2:.4f}")


if __name__ == "__main__":
    main()
