"""
interdependence.py – FF2-Korrelationsanalyse zwischen Kennzahlen
================================================================================
Berechnet die paarweisen Korrelationen der firmenspezifischen AR(1)-Parameter
phi1 und sigma_diff über alle Kombinationen aus zwei Kennzahlen (21 Paare bei
sieben Hauptkennzahlen).

Methodik:
- Spearman-Rangkorrelation pro Kennzahlpaar.
- Bonferroni-Korrektur innerhalb jeder Test-Familie (21 phi-Paare bzw. 21
  sigma-Paare), Schwelle alpha/21 = 0,00238.
- Pair-Bootstrap-Konfidenzintervalle (B = 1.000 Resamples auf Unternehmensebene,
  95-%-Perzentil-KI, Seed fest fuer Reproduzierbarkeit).

Outputs in output/interdependence/:
- corr_phi1.csv, corr_sigma.csv     7x7 Korrelationsmatrizen (rho)
- pval_phi1.csv, pval_sigma.csv     7x7 p-Wert-Matrizen
- corr_phi1_long.csv, corr_sigma_long.csv  Long-Form 21 Paare mit ratio_a,
                                            ratio_b, rho, p_value, ci_lower,
                                            ci_upper, significant_05,
                                            significant_bonferroni, n
- sig_bonferroni_phi1.csv, sig_bonferroni_sigma.csv  symmetrische Bool-Matrizen

Beschraenkt auf die sieben Hauptkennzahlen (ROA, ROE, EBIT-Marge, FCF-Marge,
Current Ratio, Debt/Equity, Eigenkapitalquote). Vergleichskennzahlen werden
nicht aufgenommen.
"""

import logging
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

from config import OUT_AR, OUT_INTERDEP, OUT_PLOTS, ensure_output_dirs

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────
# Konfiguration
# ─────────────────────────────────────────────────────────────────────────

MAIN_RATIOS: list[str] = [
    "ROA",
    "ROE",
    "EBIT_margin",
    "fcf_margin",
    "current_ratio",
    "debt_to_equity",
    "equity_ratio",
]

ALPHA_RAW: float = 0.05
N_TESTS_PER_FAMILY: int = 21          # 7 ueber 2
ALPHA_BONF: float = ALPHA_RAW / N_TESTS_PER_FAMILY  # = 0.002381

BOOTSTRAP_B: int = 1000
BOOTSTRAP_SEED: int = 42
CI_LEVEL: int = 95


# ─────────────────────────────────────────────────────────────────────────
# Berechnungen
# ─────────────────────────────────────────────────────────────────────────

def _bootstrap_spearman_ci(
    x: np.ndarray,
    y: np.ndarray,
    n_boot: int = BOOTSTRAP_B,
    seed: int = BOOTSTRAP_SEED,
    ci_level: int = CI_LEVEL,
) -> tuple[float, float]:
    """Pair-Bootstrap-Perzentil-KI fuer Spearman-rho.

    Pro Resample werden n Unternehmen mit Zuruecklegen gezogen (auf Paar-Ebene,
    nicht auf Beobachtungs-Ebene), die x- und y-Werte parallel verschoben und
    Spearman-rho neu berechnet.
    """
    rng = np.random.default_rng(seed)
    n = len(x)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        rho, _ = stats.spearmanr(x[idx], y[idx])
        boots[b] = rho
    lo = float(np.percentile(boots, (100 - ci_level) / 2))
    hi = float(np.percentile(boots, 100 - (100 - ci_level) / 2))
    return lo, hi


def compute_pairwise_correlations(
    features: pd.DataFrame,
    param: str,
    ratios: list[str] = MAIN_RATIOS,
    n_boot: int = BOOTSTRAP_B,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Spearman-rho und p-Wert fuer jedes Kennzahl-Paar plus Bootstrap-KI.

    Parameters
    ----------
    features
        Long-Form DataFrame mit ticker, ratio und der Param-Spalte
        (phi1 oder sigma_diff).
    param
        Spaltenname der zu korrelierenden Groesse (phi1 oder sigma_diff).
    ratios
        Liste der zu beruecksichtigenden Kennzahlen (Reihenfolge bestimmt
        Matrix-Reihenfolge).
    n_boot
        Anzahl Bootstrap-Resamples.

    Returns
    -------
    corr_mat
        7x7 DataFrame mit Spearman-rho, Diagonale = 1.
    pval_mat
        7x7 DataFrame mit p-Werten, Diagonale = 0.
    long_df
        Long-Form-Tabelle mit 21 Zeilen, Spalten ratio_a, ratio_b, rho,
        p_value, n, ci_lower, ci_upper, significant_05, significant_bonferroni.
    """
    sub = features[features["ratio"].isin(ratios)].copy()
    wide = sub.pivot_table(index="ticker", columns="ratio", values=param)
    wide = wide.reindex(columns=ratios)
    logger.info(
        f"  pivot wide-Form fuer {param}: {wide.shape[0]} Ticker, "
        f"{wide.shape[1]} Kennzahlen, "
        f"{wide.notna().all(axis=1).sum()} ohne NaN"
    )

    corr_mat = pd.DataFrame(np.eye(len(ratios)), index=ratios, columns=ratios)
    pval_mat = pd.DataFrame(np.zeros((len(ratios), len(ratios))),
                            index=ratios, columns=ratios)

    long_rows: list[dict] = []
    for a, b in combinations(ratios, 2):
        pair = wide[[a, b]].dropna()
        n_pair = len(pair)
        if n_pair < 10:
            logger.warning(f"    {a} x {b}: nur {n_pair} Paare, uebersprungen")
            continue
        x = pair[a].values
        y = pair[b].values
        rho, p_val = stats.spearmanr(x, y)
        rho = float(rho)
        p_val = float(p_val)
        ci_lo, ci_hi = _bootstrap_spearman_ci(x, y, n_boot=n_boot)

        # Symmetrische Matrizen
        corr_mat.loc[a, b] = rho
        corr_mat.loc[b, a] = rho
        pval_mat.loc[a, b] = p_val
        pval_mat.loc[b, a] = p_val

        long_rows.append({
            "ratio_a": a,
            "ratio_b": b,
            "n": n_pair,
            "rho": round(rho, 4),
            "p_value": p_val,
            "ci_lower": round(ci_lo, 4),
            "ci_upper": round(ci_hi, 4),
            "significant_05": bool(p_val < ALPHA_RAW),
            "significant_bonferroni": bool(p_val < ALPHA_BONF),
        })

    long_df = pd.DataFrame(long_rows).sort_values("p_value").reset_index(drop=True)
    return corr_mat, pval_mat, long_df


# ─────────────────────────────────────────────────────────────────────────
# Visualisierung
# ─────────────────────────────────────────────────────────────────────────

# Block-Zuordnung der Kennzahlen (Drei-Dynamiktypen-Struktur aus Kap. 4):
# Profitabilitaet umfasst die vier Profitabilitaetskennzahlen,
# Liquiditaet ist die Current Ratio, Kapitalstruktur die zwei Bilanzkennzahlen.
BLOCK_DEFS: list[tuple[str, str, list[str]]] = [
    ("Profitabilität",  "#1F77B4", ["ROA", "ROE", "EBIT_margin", "fcf_margin"]),  # blau
    ("Liquidität",      "#2CA02C", ["current_ratio"]),                              # gruen
    ("Kapitalstruktur", "#D62728", ["debt_to_equity", "equity_ratio"]),             # rot
]

# Kurzlabels fuer die Heatmap-Achsen
RATIO_LABEL: dict[str, str] = {
    "ROA": "ROA",
    "ROE": "ROE",
    "EBIT_margin": "EBIT",
    "fcf_margin": "FCF",
    "current_ratio": "CR",
    "debt_to_equity": "DE",
    "equity_ratio": "EQ",
}


def _plot_correlation_heatmap(
    corr_mat: pd.DataFrame,
    long_df: pd.DataFrame,
    param_label: str,
    out_path: Path,
    title: str | None = None,
) -> None:
    """Heatmap (untere Dreieckshaelfte) einer Korrelationsmatrix.

    Annotiert jede Zelle mit dem rho-Wert. Wenn der Bonferroni-Test (α/21)
    positiv ist, wird ein Stern angehaengt. Drei farbige Bloecke markieren die
    Dynamiktypen (Profitabilitaet, Liquiditaet, Kapitalstruktur).
    """
    ratios = list(corr_mat.index)
    n = len(ratios)

    # Mapping ratio -> Bonferroni-Markierung aus long_df aufbauen
    sig_map: dict[tuple[str, str], bool] = {}
    for _, row in long_df.iterrows():
        sig_map[(row["ratio_a"], row["ratio_b"])] = bool(row["significant_bonferroni"])
        sig_map[(row["ratio_b"], row["ratio_a"])] = bool(row["significant_bonferroni"])

    # Untere Dreieckshaelfte als sichtbare Werte
    mask_upper = np.triu(np.ones((n, n), dtype=bool), k=1)
    plot_vals = corr_mat.where(~mask_upper)

    fig, ax = plt.subplots(figsize=(8.5, 7))

    # Eigene Diverging-Colormap (Tobi-Stil: dezenter als reines RdBu)
    cmap = LinearSegmentedColormap.from_list(
        "rho_div",
        ["#08306B", "#4A90C2", "#FFFFFF", "#D86A60", "#67001F"],
        N=256,
    )
    im = ax.imshow(plot_vals.values, cmap=cmap, vmin=-1.0, vmax=1.0,
                   aspect="equal")

    # Zell-Annotationen
    for i in range(n):
        for j in range(n):
            if j > i:
                continue
            val = corr_mat.iloc[i, j]
            if i == j:
                label = f"{val:.2f}"
                color = "white"
            else:
                ratio_a = ratios[i]
                ratio_b = ratios[j]
                star = "*" if sig_map.get((ratio_a, ratio_b), False) else ""
                label = f"{val:.2f}{star}"
                color = "white" if abs(val) > 0.55 else "black"
            ax.text(j, i, label, ha="center", va="center",
                    fontsize=10, color=color)

    # Achsenbeschriftung
    short_labels = [RATIO_LABEL.get(r, r) for r in ratios]
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(short_labels, rotation=0)
    ax.set_yticklabels(short_labels)

    # Block-Rahmen
    pos = {r: i for i, r in enumerate(ratios)}
    legend_patches = []
    for name, color, members in BLOCK_DEFS:
        idxs = sorted(pos[m] for m in members if m in pos)
        if not idxs:
            continue
        lo, hi = idxs[0], idxs[-1]
        rect = mpatches.Rectangle(
            (lo - 0.5, lo - 0.5), hi - lo + 1, hi - lo + 1,
            linewidth=2.4, edgecolor=color, facecolor="none",
        )
        ax.add_patch(rect)
        legend_patches.append(mpatches.Patch(edgecolor=color, facecolor="none",
                                             linewidth=2.0, label=name))

    # Legende (oben rechts ausserhalb des Datenbereichs)
    leg = ax.legend(handles=legend_patches, loc="upper right",
                    bbox_to_anchor=(1.02, 1.0), frameon=False, fontsize=10)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.78, pad=0.06)
    cbar.set_label("Spearman ρ")

    # Titel
    if title is None:
        title = f"{param_label}-Korrelationsmatrix (Spearman)"
    ax.set_title(f"{title}\n* Bonferroni-signifikant (α/21 = 0,0024)",
                 fontsize=12, pad=10)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"  Heatmap gespeichert: {out_path}")


def render_heatmaps(out_dir: Path = None) -> None:
    """Heatmaps fuer phi1 und sigma rendern aus den CSV-Outputs."""
    if out_dir is None:
        out_dir = OUT_PLOTS
    interdep_dir = OUT_INTERDEP

    for label, title_name in [("phi1", "φ"), ("sigma", "σ")]:
        corr_mat = pd.read_csv(interdep_dir / f"corr_{label}.csv", index_col=0)
        long_df = pd.read_csv(interdep_dir / f"corr_{label}_long.csv")
        out_path = out_dir / f"ff2_corr_{label}_heatmap.png"
        _plot_correlation_heatmap(corr_mat, long_df, title_name, out_path)


def _save_bonferroni_mirror(long_df: pd.DataFrame,
                            ratios: list[str],
                            out_path: Path) -> pd.DataFrame:
    """Symmetrische Bool-Matrix der Bonferroni-Markierungen schreiben."""
    mat = pd.DataFrame(False, index=ratios, columns=ratios)
    for _, row in long_df.iterrows():
        mat.loc[row["ratio_a"], row["ratio_b"]] = bool(row["significant_bonferroni"])
        mat.loc[row["ratio_b"], row["ratio_a"]] = bool(row["significant_bonferroni"])
    mat.to_csv(out_path)
    return mat


def run_interdependence_analysis(
    features_csv: Path = None,
    out_dir: Path = None,
    n_boot: int = BOOTSTRAP_B,
) -> dict[str, pd.DataFrame]:
    """Komplette Korrelationsanalyse fuer phi und sigma. Schreibt alle CSVs."""
    if features_csv is None:
        features_csv = OUT_AR / "ar_features.csv"
    if out_dir is None:
        out_dir = OUT_INTERDEP
    out_dir.mkdir(parents=True, exist_ok=True)

    features = pd.read_csv(features_csv)
    logger.info(
        f"AR-Features geladen: {features_csv} "
        f"({len(features)} Zeilen, {features['ticker'].nunique()} Ticker)"
    )

    results: dict[str, pd.DataFrame] = {}

    param_map = {
        "phi1": "phi1",
        "sigma": "sigma_diff",
    }

    for label, col in param_map.items():
        logger.info(f"Korrelationsanalyse: {label} ({col})")
        corr_mat, pval_mat, long_df = compute_pairwise_correlations(
            features, param=col, n_boot=n_boot
        )

        # Matrizen
        corr_path = out_dir / f"corr_{label}.csv"
        pval_path = out_dir / f"pval_{label}.csv"
        corr_mat.round(4).to_csv(corr_path, index_label="ratio")
        pval_mat.round(6).to_csv(pval_path, index_label="ratio")
        logger.info(f"  Matrix gespeichert: {corr_path.name}, {pval_path.name}")

        # Long-Form
        long_path = out_dir / f"corr_{label}_long.csv"
        long_df.to_csv(long_path, index=False)
        logger.info(f"  Long-Form gespeichert: {long_path.name} "
                    f"({len(long_df)} Paare)")

        # Bonferroni-Mirror
        sig_path = out_dir / f"sig_bonferroni_{label}.csv"
        _save_bonferroni_mirror(long_df, MAIN_RATIOS, sig_path)
        logger.info(f"  Bonferroni-Matrix: {sig_path.name}")

        n_sig_05 = int(long_df["significant_05"].sum())
        n_sig_bonf = int(long_df["significant_bonferroni"].sum())
        logger.info(
            f"  Signifikanz: {n_sig_05}/21 bei alpha=0,05; "
            f"{n_sig_bonf}/21 nach Bonferroni (alpha/21 = {ALPHA_BONF:.5f})"
        )

        results[f"corr_{label}"] = corr_mat
        results[f"pval_{label}"] = pval_mat
        results[f"long_{label}"] = long_df

    return results


# ─────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    ensure_output_dirs()

    print("=" * 70)
    print("  FF2 – Paarweise Spearman-Korrelationen der AR(1)-Parameter")
    print(f"  Bonferroni-Schwelle: alpha/21 = {ALPHA_BONF:.5f}")
    print(f"  Pair-Bootstrap: B = {BOOTSTRAP_B}, Seed = {BOOTSTRAP_SEED}")
    print("=" * 70)

    results = run_interdependence_analysis()

    print()
    for label in ("phi1", "sigma"):
        long_df = results[f"long_{label}"]
        print(f"\n--- {label.upper()} (Top-Paare) ---")
        cols = ["ratio_a", "ratio_b", "rho", "ci_lower", "ci_upper",
                "p_value", "significant_bonferroni"]
        print(long_df[cols].head(10).to_string(index=False))

    print("\n" + "=" * 70)
    print("  Heatmaps rendern ...")
    print("=" * 70)
    render_heatmaps()

    print("\n" + "=" * 70)
    print(f"  Outputs in: {OUT_INTERDEP}")
    print(f"  Heatmaps in: {OUT_PLOTS}")
    print("=" * 70)
