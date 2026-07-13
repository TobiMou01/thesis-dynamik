"""
lead_lag.py – Cross-Korrelation der ΔY-Innovationen mit Lags
================================================================================
Untersucht, ob Schocks in einer Kennzahl Schocks in einer anderen zeitlich
vorauslaufen. Spezifikation in `output/SPEC_E61_Lead_Lag.md`.

Methodik (kurz):
- Pro Unternehmen ΔY = Y(t) − Y(t-1) je Kennzahl.
- Pro Unternehmen i und Paar (x, y) Spearman-Rangkorrelation der ΔY-Reihen
  fuer Lags k ∈ {−4, …, +4}. Konvention: positives k bedeutet, x fuehrt y
  um k Quartale (corr(x(t−k), y(t))).
- Mindestens 30 gemeinsame Beobachtungen je Lag.
- Aggregation auf Stichprobenebene: Median(ρ_i(k)) ueber alle Firmen.
- Pair-Bootstrap auf Firmen-Ebene (B = 1000) fuer 95-%-Konfidenzintervall des
  Median.
- Peak-Lag pro Paar: k* = argmax |median ρ_i(k)|.

Outputs in output/interdependence/:
- corr_lead_lag.csv          189 Zeilen (21 Paare × 9 Lags) mit ratio_x,
                              ratio_y, lag, median_rho, q25_rho, q75_rho,
                              ci_lower, ci_upper, n_firms.
- corr_lead_lag_peaks.csv    21 Zeilen mit ratio_x, ratio_y, peak_lag,
                              peak_rho, peak_ci_lower, peak_ci_upper, n_firms.

Output in output/plots/:
- ff2_lead_lag_heatmap.png   7×7-Heatmap mit Peak-Lag pro Zelle, Farbe = Lag,
                              Annotation = ρ und Lag, Bonferroni-Stern wenn
                              das KI Null ausschliesst.
"""

import logging
from itertools import combinations
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

from config import OUT_INTERDEP, OUT_PLOTS, OUT_RATIOS, ensure_output_dirs
from interdependence import BLOCK_DEFS, RATIO_LABEL

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────
# Konfiguration
# ─────────────────────────────────────────────────────────────────────────

MAIN_RATIOS: list[str] = [
    "ROA", "ROE", "EBIT_margin", "fcf_margin",
    "current_ratio", "debt_to_equity", "equity_ratio",
]
LAGS: list[int] = list(range(-4, 5))   # -4 ... +4 (9 Lags)
MIN_QUARTERS_PER_FIRM: int = 40        # Mindestbeobachtungen je Kennzahl-Reihe
MIN_OBS_PER_FIRM: int = 30             # Mindestbeobachtungen nach Lag-Verschiebung
BOOTSTRAP_B: int = 10_000              # Pair-Bootstrap-Resamples (B=10.000 fuer stabile KIs)
BOOTSTRAP_SEED: int = 42
CI_LEVEL: int = 95
ALPHA: float = 0.05
N_PAIRS: int = 21
N_LAGS_TOTAL: int = 9
N_TESTS_BONF: int = N_PAIRS * N_LAGS_TOTAL  # = 189
ALPHA_BONF: float = ALPHA / N_TESTS_BONF
CI_LEVEL_BONF: float = 100 * (1 - ALPHA_BONF)   # ≈ 99,9735 %


# ─────────────────────────────────────────────────────────────────────────
# Berechnungen
# ─────────────────────────────────────────────────────────────────────────

def _shifted_spearman(x: np.ndarray, y: np.ndarray,
                      lag: int) -> tuple[float, float]:
    """Spearman-rho und p-Wert zwischen x(t-lag) und y(t)."""
    if lag > 0:
        a, b = x[:-lag], y[lag:]
    elif lag < 0:
        a, b = x[-lag:], y[:lag]
    else:
        a, b = x, y
    mask = ~(np.isnan(a) | np.isnan(b))
    if mask.sum() < MIN_OBS_PER_FIRM:
        return np.nan, np.nan
    try:
        res = stats.spearmanr(a[mask], b[mask])
        return float(res.statistic), float(res.pvalue)
    except Exception:
        return np.nan, np.nan


def compute_per_firm_correlations(
    panel: pd.DataFrame,
    ratios: list[str] = MAIN_RATIOS,
    lags: list[int] = LAGS,
) -> pd.DataFrame:
    """Pro Ticker × Paar × Lag eine Spearman-Korrelation aus den ΔY-Reihen.

    Returns
    -------
    DataFrame mit Spalten ticker, ratio_x, ratio_y, lag, rho.
    """
    logger.info(
        f"Per-Firm-Korrelationen: {panel['ticker'].nunique()} Ticker, "
        f"{len(list(combinations(ratios, 2)))} Paare, {len(lags)} Lags"
    )

    # Sicher sortieren: pro Ticker chronologisch
    panel = panel.sort_values(["ticker", "quarter"]).reset_index(drop=True)

    rows: list[dict] = []
    grouped = panel.groupby("ticker", sort=False)
    pairs = list(combinations(ratios, 2))
    n_tickers = len(grouped)
    for idx, (ticker, sub) in enumerate(grouped, 1):
        if idx % 100 == 0:
            logger.info(f"  Ticker {idx}/{n_tickers} …")
        diffs = {}
        for r in ratios:
            if r not in sub.columns:
                continue
            arr = sub[r].diff().values
            # Defensiv: Mindestens MIN_QUARTERS_PER_FIRM nicht-NaN-Werte
            n_valid = int(np.sum(~np.isnan(arr)))
            if n_valid < MIN_QUARTERS_PER_FIRM:
                continue
            diffs[r] = arr
        for a, b in pairs:
            if a not in diffs or b not in diffs:
                continue
            xa = diffs[a]
            xb = diffs[b]
            for k in lags:
                rho, pval = _shifted_spearman(xa, xb, k)
                if np.isnan(rho):
                    continue
                rows.append({
                    "ticker": ticker,
                    "ratio_x": a,
                    "ratio_y": b,
                    "lag": k,
                    "rho": rho,
                    "pvalue": pval,
                })

    return pd.DataFrame(rows)


def _bootstrap_median_ci(values: np.ndarray, n_boot: int = BOOTSTRAP_B,
                         seed: int = BOOTSTRAP_SEED,
                         ci_level: float = CI_LEVEL) -> tuple[float, float]:
    """Bootstrap-Perzentil-KI fuer den Median (vektorisiert)."""
    n = len(values)
    if n < 10:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    samples = values[idx]
    medians = np.median(samples, axis=1)
    lo = float(np.percentile(medians, (100 - ci_level) / 2))
    hi = float(np.percentile(medians, 100 - (100 - ci_level) / 2))
    return lo, hi


def _bootstrap_median_dual_ci(values: np.ndarray, n_boot: int = BOOTSTRAP_B,
                              seed: int = BOOTSTRAP_SEED
                              ) -> tuple[float, float, float, float]:
    """Ein Bootstrap-Lauf, zwei KIs (95% und Bonferroni 99,9735%)."""
    n = len(values)
    if n < 10:
        nan = float("nan")
        return nan, nan, nan, nan
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    samples = values[idx]
    medians = np.median(samples, axis=1)
    lo_95 = float(np.percentile(medians, (100 - CI_LEVEL) / 2))
    hi_95 = float(np.percentile(medians, 100 - (100 - CI_LEVEL) / 2))
    lo_bonf = float(np.percentile(medians, (100 - CI_LEVEL_BONF) / 2))
    hi_bonf = float(np.percentile(medians, 100 - (100 - CI_LEVEL_BONF) / 2))
    return lo_95, hi_95, lo_bonf, hi_bonf


def aggregate_across_firms(per_firm: pd.DataFrame) -> pd.DataFrame:
    """Aggregation pro (Paar, Lag): Median, Quartile, 95-% + Bonferroni-CI,
    n_firms, share_significant, median_pvalue, significant_05,
    significant_bonferroni, significant_fdr."""
    rows: list[dict] = []
    for (a, b, k), grp in per_firm.groupby(["ratio_x", "ratio_y", "lag"], sort=False):
        sub = grp.dropna(subset=["rho"])
        vals = sub["rho"].values
        if len(vals) < 10:
            continue
        median = float(np.median(vals))
        q25 = float(np.percentile(vals, 25))
        q75 = float(np.percentile(vals, 75))
        ci_lo, ci_hi, ci_bonf_lo, ci_bonf_hi = _bootstrap_median_dual_ci(vals)
        # Anteil signifikanter Firmen + Median-p-Wert (fuer FDR)
        if "pvalue" in sub.columns:
            pvals = sub["pvalue"].dropna().values
            if len(pvals) > 0:
                share_sig = float((pvals < ALPHA).mean())
                median_pval = float(np.median(pvals))
            else:
                share_sig = float("nan")
                median_pval = float("nan")
        else:
            share_sig = float("nan")
            median_pval = float("nan")
        sig_05 = bool((ci_lo > 0 and ci_hi > 0) or (ci_lo < 0 and ci_hi < 0))
        sig_bonf = bool((ci_bonf_lo > 0 and ci_bonf_hi > 0)
                        or (ci_bonf_lo < 0 and ci_bonf_hi < 0))
        rows.append({
            "ratio_x": a,
            "ratio_y": b,
            "lag": int(k),
            "median_rho": round(median, 4),
            "q25_rho": round(q25, 4),
            "q75_rho": round(q75, 4),
            "ci_lower": round(ci_lo, 4),
            "ci_upper": round(ci_hi, 4),
            "ci_bonf_lower": round(ci_bonf_lo, 4),
            "ci_bonf_upper": round(ci_bonf_hi, 4),
            "share_significant": round(share_sig, 4),
            "median_pvalue": median_pval,
            "n_firms": int(len(vals)),
            "significant_05": sig_05,
            "significant_bonferroni": sig_bonf,
        })
    df = pd.DataFrame(rows)
    # Benjamini-Hochberg-FDR ueber die 189 (= 21 Paare × 9 Lags) Median-p-Werte
    if "median_pvalue" in df.columns and df["median_pvalue"].notna().any():
        df = df.sort_values("median_pvalue").reset_index(drop=True)
        m = len(df)
        ranks = np.arange(1, m + 1)
        crit = (ranks / m) * ALPHA
        df["bh_critical"] = crit.round(6)
        passes = df["median_pvalue"].values < crit
        # Schritt-Down: das groesste i mit p_i < (i/m)·alpha definiert die
        # Bonferroni-Hochberg-Schwelle.
        if passes.any():
            cutoff_idx = int(np.where(passes)[0].max())
            df["significant_fdr"] = df.index <= cutoff_idx
        else:
            df["significant_fdr"] = False
    else:
        df["significant_fdr"] = False
    return (df.sort_values(["ratio_x", "ratio_y", "lag"])
              .reset_index(drop=True))


def _classify_interpretation(peak_lag: int, sig_fdr: bool) -> str:
    """Klassifikation des Lead-Lag-Verhaeltnisses anhand FDR-Signifikanz.

    - Nicht FDR-signifikant -> kein robuster Zusammenhang
    - peak_lag == 0 -> gleichzeitig
    - peak_lag > 0  -> X fuehrt Y (um |peak_lag| Quartale)
    - peak_lag < 0  -> Y fuehrt X (um |peak_lag| Quartale)
    """
    if not sig_fdr:
        return "kein robuster Zusammenhang"
    if peak_lag == 0:
        return "gleichzeitig"
    if peak_lag > 0:
        return f"X führt Y um {peak_lag} Quartal(e)"
    return f"Y führt X um {-peak_lag} Quartal(e)"


def extract_peak_lags(long_df: pd.DataFrame) -> pd.DataFrame:
    """Pro Paar das Lag mit max |median_rho| samt Signifikanz-Markierungen."""
    rows: list[dict] = []
    for (a, b), grp in long_df.groupby(["ratio_x", "ratio_y"], sort=False):
        idx = grp["median_rho"].abs().idxmax()
        row = grp.loc[idx]
        ci_lo = float(row["ci_lower"])
        ci_hi = float(row["ci_upper"])
        ci_bonf_lo = float(row["ci_bonf_lower"])
        ci_bonf_hi = float(row["ci_bonf_upper"])
        sig_05 = bool(row.get("significant_05", False))
        sig_bonf = bool(row.get("significant_bonferroni", False))
        sig_fdr = bool(row.get("significant_fdr", False))
        peak_lag = int(row["lag"])
        peak_rho = float(row["median_rho"])
        rows.append({
            "ratio_x": a,
            "ratio_y": b,
            "peak_lag": peak_lag,
            "peak_rho": peak_rho,
            "peak_ci_lower": ci_lo,
            "peak_ci_upper": ci_hi,
            "peak_ci_bonf_lower": ci_bonf_lo,
            "peak_ci_bonf_upper": ci_bonf_hi,
            "share_significant": float(row.get("share_significant", float("nan"))),
            "median_pvalue": float(row.get("median_pvalue", float("nan"))),
            "n_firms": int(row["n_firms"]),
            "peak_significant_05": sig_05,
            "peak_significant_bonferroni": sig_bonf,
            "peak_significant_fdr": sig_fdr,
            "interpretation": _classify_interpretation(peak_lag, sig_fdr),
        })
    return (pd.DataFrame(rows)
            .sort_values("peak_rho", key=lambda s: s.abs(), ascending=False)
            .reset_index(drop=True))


# ─────────────────────────────────────────────────────────────────────────
# Heatmap
# ─────────────────────────────────────────────────────────────────────────

def _plot_lead_lag_heatmap(peaks: pd.DataFrame, out_path: Path) -> None:
    """Untere Dreiecks-Heatmap mit Peak-Lag pro Zelle.

    Nur untere Dreieckshaelfte sichtbar (die Lead-Lag-Beziehung X->Y ist
    symmetrisch zu Y->X mit umgekehrtem Vorzeichen, daher kein Mehrwert
    durch volles Quadrat).

    Farbe: Lag (Diverging-Colormap, blau = X folgt Y, rot = X fuehrt Y).
    Annotation: Lag und ρ. Stern, wenn Bootstrap-KI bei Bonferroni-Schwelle
    Null ausschliesst.

    Lag-Range der Colormap wird dynamisch aus den tatsaechlich beobachteten
    Peak-Lags abgeleitet.
    """
    ratios = MAIN_RATIOS
    n = len(ratios)

    # Lag- und Rho-Matrix nur unteres Dreieck befuellen (Zeilen > Spalten)
    lag_mat = pd.DataFrame(np.nan, index=ratios, columns=ratios)
    rho_mat = pd.DataFrame(np.nan, index=ratios, columns=ratios)
    sig_mat = pd.DataFrame(False, index=ratios, columns=ratios)
    pos = {r: i for i, r in enumerate(ratios)}
    # Stern markiert FDR-Signifikanz (selektiver als Bonferroni-Bootstrap,
    # weil bei n = 932 die Bootstrap-KIs fuer praktisch alle Median-rho
    # Null ausschliessen).
    sig_col = "peak_significant_fdr" if "peak_significant_fdr" in peaks.columns \
              else "peak_significant_bonferroni"
    for _, row in peaks.iterrows():
        a, b = row["ratio_x"], row["ratio_y"]
        lag = int(row["peak_lag"])
        rho = float(row["peak_rho"])
        ia, ib = pos[a], pos[b]
        # Zelle mit Zeile > Spalte (untere Dreieckshaelfte). Wenn ia > ib,
        # gehoert das Paar (a,b) ins untere Dreieck mit Lag wie im Output;
        # andernfalls muss das Lag-Vorzeichen gespiegelt werden.
        if ia > ib:
            lag_mat.iloc[ia, ib] = lag
            rho_mat.iloc[ia, ib] = rho
            sig_mat.iloc[ia, ib] = bool(row[sig_col])
        else:
            lag_mat.iloc[ib, ia] = -lag
            rho_mat.iloc[ib, ia] = rho
            sig_mat.iloc[ib, ia] = bool(row[sig_col])

    # Adaptive Lag-Range aus tatsaechlichen Peak-Lags
    observed_lags = peaks["peak_lag"].astype(int)
    lag_min = int(observed_lags.min())
    lag_max = int(observed_lags.max())
    lag_abs = max(abs(lag_min), abs(lag_max), 1)
    vmin, vmax = -lag_abs, lag_abs

    fig, ax = plt.subplots(figsize=(8.5, 7))
    cmap = LinearSegmentedColormap.from_list(
        "lag_div",
        ["#08306B", "#4A90C2", "#FFFFFF", "#D86A60", "#67001F"],
        N=256,
    )
    im = ax.imshow(lag_mat.values, cmap=cmap, vmin=vmin, vmax=vmax,
                   aspect="equal")

    short = [RATIO_LABEL.get(r, r) for r in ratios]
    for i in range(n):
        for j in range(n):
            if j > i:
                continue          # obere Dreieckshaelfte leer
            if i == j:
                ax.text(j, i, "—", ha="center", va="center", fontsize=10,
                        color="gray")
                continue
            lag = int(lag_mat.iloc[i, j])
            rho = float(rho_mat.iloc[i, j])
            star = "*" if bool(sig_mat.iloc[i, j]) else ""
            label = f"k={lag:+d}\nρ={rho:+.2f}{star}"
            # Textfarbe abhaengig vom Lag-Betrag relativ zur Skala
            color = "white" if abs(lag) >= lag_abs else "black"
            ax.text(j, i, label, ha="center", va="center", fontsize=8.5,
                    color=color)

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(short, rotation=0)
    ax.set_yticklabels(short)
    ax.set_xlabel("Y (Folge-Kennzahl)")
    ax.set_ylabel("X (Vorlauf-Kennzahl)")

    # Block-Rahmen entlang der Diagonale (im Dreieck als L-Form sichtbar)
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
    # Legende in den leeren oberen Dreiecksbereich legen
    ax.legend(handles=legend_patches, loc="upper right",
              bbox_to_anchor=(0.98, 0.98), frameon=False, fontsize=10)

    cbar = fig.colorbar(im, ax=ax, shrink=0.78, pad=0.06)
    cbar.set_label("Peak-Lag k* (Quartale)")
    cbar.set_ticks(list(range(vmin, vmax + 1)))

    ax.set_title(
        "Lead-Lag-Cross-Korrelation der ΔY-Innovationen\n"
        "* Benjamini-Hochberg-FDR-signifikant (über 189 Tests)",
        fontsize=12, pad=10,
    )

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Heatmap gespeichert: {out_path}")


# ─────────────────────────────────────────────────────────────────────────
# CLI-Runner
# ─────────────────────────────────────────────────────────────────────────

def run_lead_lag_analysis(
    panel_csv: Path = None,
    out_dir: Path = None,
    plot_dir: Path = None,
    use_cache: bool = True,
) -> dict[str, pd.DataFrame]:
    if panel_csv is None:
        panel_csv = OUT_RATIOS / "ratio_panel.csv"
    if out_dir is None:
        out_dir = OUT_INTERDEP
    if plot_dir is None:
        plot_dir = OUT_PLOTS
    out_dir.mkdir(parents=True, exist_ok=True)

    per_firm_cache = out_dir / "_cache_lead_lag_per_firm.csv"

    if use_cache and per_firm_cache.exists():
        logger.info(f"Per-Firm-Cache gefunden: {per_firm_cache} — wird geladen")
        per_firm = pd.read_csv(per_firm_cache)
    else:
        panel = pd.read_csv(panel_csv)
        logger.info(f"Panel geladen: {panel_csv} ({len(panel)} Zeilen)")
        per_firm = compute_per_firm_correlations(panel)
        per_firm.to_csv(per_firm_cache, index=False)
        logger.info(f"Per-Firm-Cache gespeichert: {per_firm_cache}")
    logger.info(f"Per-Firm-Korrelationen: {len(per_firm)} Zeilen")

    long_df = aggregate_across_firms(per_firm)
    long_path = out_dir / "corr_lead_lag.csv"
    long_df.to_csv(long_path, index=False)
    logger.info(f"  Long-Form gespeichert: {long_path}")

    peaks = extract_peak_lags(long_df)
    peaks_path = out_dir / "corr_lead_lag_peaks.csv"
    peaks.to_csv(peaks_path, index=False)
    logger.info(f"  Peaks gespeichert: {peaks_path}")

    plot_path = plot_dir / "ff2_lead_lag_heatmap.png"
    _plot_lead_lag_heatmap(peaks, plot_path)

    return {"per_firm": per_firm, "long": long_df, "peaks": peaks}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    ensure_output_dirs()

    print("=" * 70)
    print("  FF2 – Lead-Lag-Cross-Korrelation der ΔY-Innovationen")
    print(f"  Lags: {LAGS[0]} … {LAGS[-1]}  |  B = {BOOTSTRAP_B}  |  Seed = {BOOTSTRAP_SEED}")
    print("=" * 70)

    results = run_lead_lag_analysis()

    print()
    peaks = results["peaks"]
    print("--- Peak-Lags pro Paar (sortiert nach |ρ|) ---")
    print(peaks[["ratio_x", "ratio_y", "peak_lag", "peak_rho",
                 "peak_significant_05", "peak_significant_bonferroni",
                 "share_significant", "interpretation"]].to_string(index=False))

    print("\n" + "=" * 70)
    print(f"  Outputs: {OUT_INTERDEP}")
    print(f"  Heatmap: {OUT_PLOTS}/ff2_lead_lag_heatmap.png")
    print("=" * 70)
