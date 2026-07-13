"""
lead_lag_v2.py – Lead-Lag-Cross-Korrelation der ΔY-Innovationen (v2)
================================================================================
Identisch zum Original lead_lag.py, mit drei Anpassungen:

  (1) BOOTSTRAP_B = 10_000  (vorher 1_000)
      Begründung: Davidson/MacKinnon (2000) — α·(B+1) ∈ ℕ als Konsistenz-
      bedingung. Für α_bonf = 0,05/189 ≈ 2,65e-4 folgt B ≥ 3.774. Für stabile
      Quantilsschätzung am 99,9735-%-Rand ist B = 10.000 die belastbare Wahl.
      Die 95-%-CIs werden dadurch ebenfalls glatter.

  (2) Fisher-z-Mittelwert als zusätzliche Spalte
      Zweck: Diskrepanz Median ↔ Mean(Fisher-z) ist diagnostisch für die
      Schiefe der firmenspezifischen ρ_i. Median bleibt das Hauptmaß
      (robust gegen Heavy Tails der Quartals-ΔY).

  (3) Benjamini-Hochberg-FDR als zusätzliche Signifikanzspalte
      Begründung: Bonferroni ist bei 189 stark abhängigen Tests konservativ.
      FDR zeigt transparent, welche Befunde unter milderer Korrektur
      zusätzlich überleben würden. Hauptkriterium bleibt Bonferroni.

Inputs werden aus dem Hauptpfad gelesen, Outputs landen in
v2/output/interdependence/ bzw. v2/output/plots/ — das Original-Skript bleibt
unberührt.

Cache: Per-Firm-Korrelationen sind identisch zum Original und werden direkt aus
dem Hauptcache geladen, falls vorhanden.
"""

from __future__ import annotations

import logging
import sys
from itertools import combinations
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

# Pfade
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from interdependence import BLOCK_DEFS, RATIO_LABEL  # noqa: E402

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────
# Konfiguration
# ─────────────────────────────────────────────────────────────────────────

MAIN_RATIOS: list[str] = [
    "ROA", "ROE", "EBIT_margin", "fcf_margin",
    "current_ratio", "debt_to_equity", "equity_ratio",
]
LAGS: list[int] = list(range(-4, 5))
MIN_QUARTERS_PER_FIRM: int = 40
MIN_OBS_PER_FIRM: int = 30
BOOTSTRAP_B: int = 10_000          # v2: 10× erhöht
BOOTSTRAP_SEED: int = 42
CI_LEVEL: int = 95
ALPHA: float = 0.05
N_PAIRS: int = 21
N_LAGS_TOTAL: int = 9
N_TESTS_BONF: int = N_PAIRS * N_LAGS_TOTAL  # 189
ALPHA_BONF: float = ALPHA / N_TESTS_BONF
CI_LEVEL_BONF: float = 100 * (1 - ALPHA_BONF)


# Pfade
PANEL_CSV = REPO_ROOT / "output" / "ratios" / "ratio_panel.csv"
ORIG_CACHE = REPO_ROOT / "output" / "interdependence" / "_cache_lead_lag_per_firm.csv"
V2_OUT_INTERDEP = REPO_ROOT / "v2" / "output" / "interdependence"
V2_OUT_PLOTS = REPO_ROOT / "v2" / "output" / "plots"


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
    """Pro Ticker × Paar × Lag eine Spearman-Korrelation aus den ΔY-Reihen."""
    logger.info(
        f"Per-Firm-Korrelationen: {panel['ticker'].nunique()} Ticker"
    )
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
            if int(np.sum(~np.isnan(arr))) < MIN_QUARTERS_PER_FIRM:
                continue
            diffs[r] = arr
        for a, b in pairs:
            if a not in diffs or b not in diffs:
                continue
            for k in lags:
                rho, pval = _shifted_spearman(diffs[a], diffs[b], k)
                if np.isnan(rho):
                    continue
                rows.append({"ticker": ticker, "ratio_x": a, "ratio_y": b,
                             "lag": k, "rho": rho, "pvalue": pval})
    return pd.DataFrame(rows)


def _bootstrap_median_ci(values: np.ndarray, n_boot: int,
                         seed: int, ci_level: float) -> tuple[float, float]:
    """Bootstrap-Perzentil-KI für den Median (vektorisiert)."""
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


def _bootstrap_median_ci_dual(values: np.ndarray, n_boot: int, seed: int,
                              ci_level_a: float, ci_level_b: float
                              ) -> tuple[float, float, float, float]:
    """Ein Bootstrap-Lauf, beide CIs ableiten. Effizient für 95 % + Bonferroni.

    Returns: (lo_a, hi_a, lo_b, hi_b)
    """
    n = len(values)
    if n < 10:
        nan = float("nan")
        return nan, nan, nan, nan
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    samples = values[idx]
    medians = np.median(samples, axis=1)
    pa_lo = (100 - ci_level_a) / 2
    pa_hi = 100 - pa_lo
    pb_lo = (100 - ci_level_b) / 2
    pb_hi = 100 - pb_lo
    lo_a, hi_a, lo_b, hi_b = np.percentile(
        medians, [pa_lo, pa_hi, pb_lo, pb_hi]
    )
    return float(lo_a), float(hi_a), float(lo_b), float(hi_b)


def _fisher_z_mean(rhos: np.ndarray) -> float:
    """Gemittelter Pearson-äquivalenter Korrelationswert via Fisher-z.

    rhos werden auf (-0.999, 0.999) geclippt, um Inf bei z=arctanh(±1) zu
    vermeiden. Rücktransformation: tanh(mean(z)).
    """
    vals = rhos[~np.isnan(rhos)]
    if len(vals) == 0:
        return float("nan")
    clipped = np.clip(vals, -0.999, 0.999)
    z = np.arctanh(clipped)
    return float(np.tanh(np.mean(z)))


def _bh_fdr_significant(pvals: np.ndarray, alpha: float = ALPHA) -> np.ndarray:
    """Benjamini-Hochberg-FDR: Boolean-Array, True = signifikant unter BH.

    Standardprozedur: Sortiere p-Werte aufsteigend, finde größtes k mit
    p_(k) ≤ k/m · alpha, verwirf alle H_(1)…H_(k).
    """
    m = len(pvals)
    if m == 0:
        return np.array([], dtype=bool)
    order = np.argsort(pvals)
    sorted_p = pvals[order]
    thresholds = (np.arange(1, m + 1) / m) * alpha
    below = sorted_p <= thresholds
    if not below.any():
        return np.zeros(m, dtype=bool)
    k_max = np.max(np.where(below)[0])
    sig_sorted = np.zeros(m, dtype=bool)
    sig_sorted[: k_max + 1] = True
    sig = np.zeros(m, dtype=bool)
    sig[order] = sig_sorted
    return sig


def aggregate_across_firms(per_firm: pd.DataFrame) -> pd.DataFrame:
    """Aggregation pro (Paar, Lag): Median, Fisher-z-Mean, Quartile, CIs,
    Anteile signifikanter Firmen, BH-FDR-Flag."""
    rows: list[dict] = []
    for (a, b, k), grp in per_firm.groupby(
        ["ratio_x", "ratio_y", "lag"], sort=False
    ):
        sub = grp.dropna(subset=["rho"])
        vals = sub["rho"].values
        if len(vals) < 10:
            continue
        median = float(np.median(vals))
        fz_mean = _fisher_z_mean(vals)
        q25 = float(np.percentile(vals, 25))
        q75 = float(np.percentile(vals, 75))
        ci_lo, ci_hi, ci_bonf_lo, ci_bonf_hi = _bootstrap_median_ci_dual(
            vals, n_boot=BOOTSTRAP_B, seed=BOOTSTRAP_SEED,
            ci_level_a=CI_LEVEL, ci_level_b=CI_LEVEL_BONF,
        )
        share_sig = float("nan")
        median_p = 1.0
        if "pvalue" in sub.columns:
            pvals = sub["pvalue"].dropna().values
            if len(pvals) > 0:
                share_sig = float((pvals < ALPHA).mean())
                median_p = float(np.median(pvals))
        sig_05 = bool((ci_lo > 0 and ci_hi > 0) or (ci_lo < 0 and ci_hi < 0))
        sig_bonf = bool((ci_bonf_lo > 0 and ci_bonf_hi > 0)
                        or (ci_bonf_lo < 0 and ci_bonf_hi < 0))
        rows.append({
            "ratio_x": a, "ratio_y": b, "lag": int(k),
            "median_rho": round(median, 4),
            "fisher_z_mean": round(fz_mean, 4),
            "q25_rho": round(q25, 4), "q75_rho": round(q75, 4),
            "ci_lower": round(ci_lo, 4), "ci_upper": round(ci_hi, 4),
            "ci_bonf_lower": round(ci_bonf_lo, 4),
            "ci_bonf_upper": round(ci_bonf_hi, 4),
            "share_significant": round(share_sig, 4),
            "median_pvalue": round(median_p, 4),
            "n_firms": int(len(vals)),
            "significant_05": sig_05,
            "significant_bonferroni": sig_bonf,
        })
    out = (pd.DataFrame(rows)
           .sort_values(["ratio_x", "ratio_y", "lag"])
           .reset_index(drop=True))

    # FDR (Benjamini-Hochberg) auf "Median-Test"-Niveau über alle (Paar, Lag)-
    # Kombinationen. Test-p pro Zelle = Median der firmenspezifischen p-Werte.
    bh_pvals = out["median_pvalue"].values
    out["fdr_bh_significant"] = _bh_fdr_significant(bh_pvals, alpha=ALPHA)
    return out


def _classify_interpretation(peak_lag: int, peak_rho: float,
                             sig_bonf: bool) -> str:
    if not sig_bonf:
        return "kein robuster Zusammenhang"
    if peak_lag == 0:
        return "gleichzeitig"
    if peak_lag > 0:
        return f"X führt Y um {peak_lag} Quartal(e)"
    return f"Y führt X um {-peak_lag} Quartal(e)"


def extract_peak_lags(long_df: pd.DataFrame) -> pd.DataFrame:
    """Pro Paar das Lag mit max |median_rho| samt Bonferroni- und FDR-Flag."""
    rows: list[dict] = []
    for (a, b), grp in long_df.groupby(["ratio_x", "ratio_y"], sort=False):
        idx = grp["median_rho"].abs().idxmax()
        row = grp.loc[idx]
        ci_lo = float(row["ci_lower"])
        ci_hi = float(row["ci_upper"])
        ci_bonf_lo = float(row["ci_bonf_lower"])
        ci_bonf_hi = float(row["ci_bonf_upper"])
        sig_05 = bool((ci_lo > 0 and ci_hi > 0) or (ci_lo < 0 and ci_hi < 0))
        sig_bonf = bool((ci_bonf_lo > 0 and ci_bonf_hi > 0)
                        or (ci_bonf_lo < 0 and ci_bonf_hi < 0))
        peak_lag = int(row["lag"])
        peak_rho = float(row["median_rho"])
        rows.append({
            "ratio_x": a, "ratio_y": b,
            "peak_lag": peak_lag, "peak_rho": peak_rho,
            "peak_fisher_z_mean": float(row["fisher_z_mean"]),
            "peak_ci_lower": ci_lo, "peak_ci_upper": ci_hi,
            "peak_ci_bonf_lower": ci_bonf_lo,
            "peak_ci_bonf_upper": ci_bonf_hi,
            "share_significant": float(row.get("share_significant",
                                               float("nan"))),
            "n_firms": int(row["n_firms"]),
            "peak_significant_05": sig_05,
            "peak_significant_bonferroni": sig_bonf,
            "peak_significant_fdr": bool(row["fdr_bh_significant"]),
            "interpretation": _classify_interpretation(peak_lag, peak_rho,
                                                       sig_bonf),
        })
    return (pd.DataFrame(rows)
            .sort_values("peak_rho", key=lambda s: s.abs(), ascending=False)
            .reset_index(drop=True))


# ─────────────────────────────────────────────────────────────────────────
# Heatmap
# ─────────────────────────────────────────────────────────────────────────

def _plot_lead_lag_heatmap(peaks: pd.DataFrame, out_path: Path) -> None:
    """Untere Dreiecks-Heatmap mit Peak-Lag pro Zelle (v2-Variante)."""
    ratios = MAIN_RATIOS
    n = len(ratios)
    lag_mat = pd.DataFrame(np.nan, index=ratios, columns=ratios)
    rho_mat = pd.DataFrame(np.nan, index=ratios, columns=ratios)
    sig_mat = pd.DataFrame(False, index=ratios, columns=ratios)
    pos = {r: i for i, r in enumerate(ratios)}
    for _, row in peaks.iterrows():
        a, b = row["ratio_x"], row["ratio_y"]
        lag = int(row["peak_lag"])
        rho = float(row["peak_rho"])
        ia, ib = pos[a], pos[b]
        if ia > ib:
            lag_mat.iloc[ia, ib] = lag
            rho_mat.iloc[ia, ib] = rho
            sig_mat.iloc[ia, ib] = bool(row["peak_significant_bonferroni"])
        else:
            lag_mat.iloc[ib, ia] = -lag
            rho_mat.iloc[ib, ia] = rho
            sig_mat.iloc[ib, ia] = bool(row["peak_significant_bonferroni"])
    observed_lags = peaks["peak_lag"].astype(int)
    lag_abs = max(abs(int(observed_lags.min())),
                  abs(int(observed_lags.max())), 1)
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
                continue
            if i == j:
                ax.text(j, i, "—", ha="center", va="center", fontsize=10,
                        color="gray")
                continue
            lag = int(lag_mat.iloc[i, j])
            rho = float(rho_mat.iloc[i, j])
            star = "*" if bool(sig_mat.iloc[i, j]) else ""
            label = f"k={lag:+d}\nρ={rho:+.2f}{star}"
            color = "white" if abs(lag) >= lag_abs else "black"
            ax.text(j, i, label, ha="center", va="center", fontsize=8.5,
                    color=color)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(short, rotation=0)
    ax.set_yticklabels(short)
    ax.set_xlabel("Y (Folge-Kennzahl)")
    ax.set_ylabel("X (Vorlauf-Kennzahl)")
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
    ax.legend(handles=legend_patches, loc="upper right",
              bbox_to_anchor=(0.98, 0.98), frameon=False, fontsize=10)
    cbar = fig.colorbar(im, ax=ax, shrink=0.78, pad=0.06)
    cbar.set_label("Peak-Lag k* (Quartale)")
    cbar.set_ticks(list(range(vmin, vmax + 1)))
    ax.set_title(
        "Lead-Lag-Cross-Korrelation der ΔY-Innovationen (v2)\n"
        f"B = {BOOTSTRAP_B:,}  |  * Bootstrap-Bonferroni-KI "
        f"(α / {N_TESTS_BONF}) schließt Null aus",
        fontsize=11, pad=10,
    )
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Heatmap gespeichert: {out_path}")


# ─────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────

def run() -> dict[str, pd.DataFrame]:
    V2_OUT_INTERDEP.mkdir(parents=True, exist_ok=True)
    V2_OUT_PLOTS.mkdir(parents=True, exist_ok=True)

    # Cache: Per-Firm-Korrelationen sind in v2 identisch — Original-Cache
    # bevorzugt
    if ORIG_CACHE.exists():
        logger.info(f"Lade Original-Cache: {ORIG_CACHE}")
        per_firm = pd.read_csv(ORIG_CACHE)
    else:
        panel = pd.read_csv(PANEL_CSV)
        logger.info(f"Panel geladen: {PANEL_CSV} ({len(panel)} Zeilen)")
        per_firm = compute_per_firm_correlations(panel)
        v2_cache = V2_OUT_INTERDEP / "_cache_lead_lag_per_firm.csv"
        per_firm.to_csv(v2_cache, index=False)
        logger.info(f"Cache gespeichert: {v2_cache}")
    logger.info(f"Per-Firm-Korrelationen: {len(per_firm)} Zeilen")

    long_df = aggregate_across_firms(per_firm)
    long_path = V2_OUT_INTERDEP / "corr_lead_lag_v2.csv"
    long_df.to_csv(long_path, index=False)
    logger.info(f"Long-Form gespeichert: {long_path}")

    peaks = extract_peak_lags(long_df)
    peaks_path = V2_OUT_INTERDEP / "corr_lead_lag_peaks_v2.csv"
    peaks.to_csv(peaks_path, index=False)
    logger.info(f"Peaks gespeichert: {peaks_path}")

    plot_path = V2_OUT_PLOTS / "ff2_lead_lag_heatmap_v2.png"
    _plot_lead_lag_heatmap(peaks, plot_path)

    return {"per_firm": per_firm, "long": long_df, "peaks": peaks}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    print("=" * 70)
    print("  FF2 – Lead-Lag-Cross-Korrelation (v2)")
    print(f"  Lags: {LAGS[0]} … {LAGS[-1]}  |  B = {BOOTSTRAP_B:,}  "
          f"|  Seed = {BOOTSTRAP_SEED}")
    print("=" * 70)
    results = run()
    print()
    peaks = results["peaks"]
    print("--- Peak-Lags pro Paar (sortiert nach |ρ|) ---")
    print(peaks[["ratio_x", "ratio_y", "peak_lag", "peak_rho",
                 "peak_significant_05", "peak_significant_bonferroni",
                 "peak_significant_fdr", "share_significant",
                 "interpretation"]].to_string(index=False))
    print("\n" + "=" * 70)
    print(f"  Outputs: {V2_OUT_INTERDEP}")
    print(f"  Heatmap: {V2_OUT_PLOTS}/ff2_lead_lag_heatmap_v2.png")
    print("=" * 70)
