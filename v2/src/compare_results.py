"""
compare_results.py – Side-by-Side Vergleich Original / v2 / Pre-Whitening
================================================================================
Lädt die drei Peak-Lag-Tabellen und stellt sie nebeneinander dar.

Outputs in v2/output/interdependence/:
- comparison_peaks.csv    Pro Paar: peak_lag und peak_rho in allen drei Varianten
- comparison_summary.txt  Verteilung der Peak-Lags pro Variante
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

ORIG_PEAKS = REPO_ROOT / "output" / "interdependence" / "corr_lead_lag_peaks.csv"
V2_PEAKS = REPO_ROOT / "v2" / "output" / "interdependence" / "corr_lead_lag_peaks_v2.csv"
PW_PEAKS = REPO_ROOT / "v2" / "output" / "interdependence" / "corr_lead_lag_peaks_prewhitened.csv"

OUT_CSV = REPO_ROOT / "v2" / "output" / "interdependence" / "comparison_peaks.csv"
OUT_TXT = REPO_ROOT / "v2" / "output" / "interdependence" / "comparison_summary.txt"


def main() -> None:
    orig = pd.read_csv(ORIG_PEAKS)[["ratio_x", "ratio_y", "peak_lag",
                                    "peak_rho",
                                    "peak_significant_bonferroni"]]
    v2 = pd.read_csv(V2_PEAKS)[["ratio_x", "ratio_y", "peak_lag",
                                "peak_rho",
                                "peak_significant_bonferroni",
                                "peak_significant_fdr"]]
    pw = pd.read_csv(PW_PEAKS)[["ratio_x", "ratio_y", "peak_lag",
                                "peak_rho",
                                "peak_significant_bonferroni",
                                "peak_significant_fdr"]]
    orig = orig.rename(columns={
        "peak_lag": "lag_orig", "peak_rho": "rho_orig",
        "peak_significant_bonferroni": "sig_bonf_orig",
    })
    v2 = v2.rename(columns={
        "peak_lag": "lag_v2", "peak_rho": "rho_v2",
        "peak_significant_bonferroni": "sig_bonf_v2",
        "peak_significant_fdr": "sig_fdr_v2",
    })
    pw = pw.rename(columns={
        "peak_lag": "lag_pw", "peak_rho": "rho_pw",
        "peak_significant_bonferroni": "sig_bonf_pw",
        "peak_significant_fdr": "sig_fdr_pw",
    })
    comp = (orig.merge(v2, on=["ratio_x", "ratio_y"])
            .merge(pw, on=["ratio_x", "ratio_y"]))
    # Sortiere nach |rho_orig|
    comp = comp.reindex(
        comp["rho_orig"].abs().sort_values(ascending=False).index
    ).reset_index(drop=True)
    comp.to_csv(OUT_CSV, index=False)
    print(f"Comparison-CSV: {OUT_CSV}")
    print()

    summary_lines = []
    for col, label in [("lag_orig", "Original"),
                       ("lag_v2", "v2 (B=10k)"),
                       ("lag_pw", "Pre-Whitening")]:
        dist = comp[col].value_counts().sort_index()
        line = f"{label:18s}  Peak-Lag-Verteilung: " + ", ".join(
            f"k={int(k):+d}: {int(v)}" for k, v in dist.items()
        )
        summary_lines.append(line)
    summary = "\n".join(summary_lines)
    print(summary)
    OUT_TXT.write_text(summary + "\n")
    print(f"\nSummary: {OUT_TXT}")
    print()

    # Verschiebungen Original → Pre-Whitening
    shifts = comp[comp["lag_orig"] != comp["lag_pw"]][
        ["ratio_x", "ratio_y", "lag_orig", "rho_orig", "lag_pw", "rho_pw"]
    ]
    print("--- Paare, bei denen Pre-Whitening das Peak-Lag verschiebt ---")
    if len(shifts) == 0:
        print("(keine)")
    else:
        print(shifts.to_string(index=False))

    print()
    print("--- FDR-signifikante Paare in v2 ---")
    print(comp[comp["sig_fdr_v2"]][
        ["ratio_x", "ratio_y", "rho_v2", "lag_v2"]
    ].to_string(index=False))

    print()
    print("--- FDR-signifikante Paare nach Pre-Whitening ---")
    print(comp[comp["sig_fdr_pw"]][
        ["ratio_x", "ratio_y", "rho_pw", "lag_pw"]
    ].to_string(index=False))


if __name__ == "__main__":
    main()
