"""
Verifikations-Skript für Kapitel 4 (FF1).

Liest die in Kap. 4 zitierten zentralen Kennwerte aus den CSVs in
anhang/zwischenergebnisse/ und vergleicht sie mit den im Text genannten Werten.

Aufruf:
    python verifiziere_kap4.py

Output:
    Konsole-Ausgabe mit OK / MISMATCH pro Kennwert.
    Bei Mismatch: berechneter Wert vs. Text-Wert mit Differenz.
"""
from pathlib import Path
import pandas as pd
import numpy as np

ZWISCHEN = Path(__file__).resolve().parent.parent / "zwischenergebnisse"

# Erwartete Werte aus dem aktuellen Text-Stand von Kap. 4
ERWARTET = {
    # Kap. 4.1.1 — Überblick der Dynamiktypen
    "phi_median_global": -0.32,  # Para 311
    "sigma_median_global": 0.09,  # Para 311
    "phi_anteil_positiv_global": 11.3,  # Prozent, Para 315
    # Kap. 4.1.2 — Profitabilität
    "phi_median_ROA": -0.43,
    "phi_median_ROE": -0.43,
    "phi_median_EBIT_margin": -0.43,
    "phi_median_fcf_margin": -0.46,
    # Kap. 4.1.3 — Liquidität
    "phi_median_current_ratio": -0.17,
    # Kap. 4.1.4 — Kapitalstruktur
    "phi_median_debt_to_equity": -0.09,
    "phi_median_equity_ratio": -0.04,
    "phi_pos_anteil_debt_to_equity": 28,  # Prozent
    "phi_pos_anteil_equity_ratio": 36,  # Prozent
}

def check(name, actual, expected, tol_pct=2):
    """Vergleich actual vs. expected mit relativer Toleranz tol_pct in Prozent."""
    diff = abs(actual - expected)
    tol = max(abs(expected) * tol_pct / 100, 0.001)
    status = "✓ passt" if diff <= tol else "✗ MISMATCH"
    print(f"  {status:14s} {name:40s} | berechnet {actual:+.4f}  |  erwartet {expected:+.4f}  |  Δ {diff:.4f}")
    return diff <= tol

def main():
    # Lade die AR-Schätzungen
    ar_path = ZWISCHEN / "03_ar_schaetzungen.csv"
    if not ar_path.exists():
        print(f"FEHLER: {ar_path.name} fehlt. Erst Pipeline laufen lassen.")
        return

    ar = pd.read_csv(ar_path)
    RATIOS = ["ROA", "ROE", "EBIT_margin", "fcf_margin",
              "current_ratio", "debt_to_equity", "equity_ratio"]
    ar = ar[ar["ratio"].isin(RATIOS)]

    print("=" * 80)
    print("VERIFIKATION KAPITEL 4")
    print("=" * 80)

    # 4.1.1 — globale Mediane
    print("\n[Kap. 4.1.1 — Überblick]")
    check("phi-Median global", ar["phi1"].median(), ERWARTET["phi_median_global"])
    check("sigma-Median global", ar["sigma_diff"].median(), ERWARTET["sigma_median_global"])
    pos_pct = (ar["phi1"] > 0).mean() * 100
    check("Anteil positives phi global (%)", pos_pct, ERWARTET["phi_anteil_positiv_global"])

    # Pro Kennzahl phi-Median
    print("\n[Kap. 4.1.2-4.1.4 — phi-Mediane pro Kennzahl]")
    for r in RATIOS:
        med = ar[ar["ratio"] == r]["phi1"].median()
        check(f"phi-Median {r}", med, ERWARTET[f"phi_median_{r}"])

    # Positiv-phi-Anteile Kapitalstruktur
    print("\n[Kap. 4.1.4 — positive phi-Anteile Kapitalstruktur]")
    for r in ["debt_to_equity", "equity_ratio"]:
        pos = (ar[ar["ratio"] == r]["phi1"] > 0).mean() * 100
        check(f"Anteil positives phi {r} (%)", pos, ERWARTET[f"phi_pos_anteil_{r}"])

    print("\n" + "=" * 80)
    print("Fertig. Mismatches oben markiert mit ✗.")

if __name__ == "__main__":
    main()
