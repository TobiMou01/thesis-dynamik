"""
lead_lag_prewhitened.py – Pre-Whitening-Variante der Lead-Lag-Analyse
================================================================================
Robustheits-Pendant zu lead_lag_v2.py mit einer methodischen Anpassung:

  Statt der rohen ΔY-Reihen werden die Residuen ε(t) eines AR(1)-Modells auf
  ΔY verwendet:

        ΔY(t) = c + φ · ΔY(t−1) + ε(t)
        ε(t)   = ΔY(t) − ĉ − φ̂ · ΔY(t−1)

  Die Spearman-Cross-Korrelation wird dann auf ε_X(t−k) × ε_Y(t) gerechnet
  statt auf ΔY_X(t−k) × ΔY_Y(t).

Begründung
----------
- Box/Jenkins, Haugh (1976), Pierce/Haugh (1977): klassisches Pre-Whitening
  vor jeder Cross-Correlation-Funktion. Bartletts SE-Formel 1/T gilt nur
  für white-noise-Inputs.
- Granger/Newbold (1974): gemeinsame Autokorrelationsstruktur erzeugt
  "spurious cross-correlation". Differenzierung allein reicht nicht, weil
  die ΔY-Reihen selbst autokorreliert sind (φ_ΔY ≈ −0,43 bei
  Profitabilitätskennzahlen — typische Overdifferencing-Signatur, weil die
  zugrundeliegenden Accounting Ratios stationär statt I(1) sind, vgl.
  Nissim/Penman 2001, Fairfield/Yohn 2001).
- Nach Pre-Whitening sind die Innovationen ε(t) annähernd unkorreliert.
  Cross-Korrelationen sind dann frei vom Mean-Reversion-Echo, das im
  Originalskript bei Lag ±1 sichtbar wird.

Vorgehen
--------
1. Pro Ticker × Kennzahl ΔY berechnen.
2. AR(1) per OLS (statsmodels) auf ΔY fitten, falls n ≥ MIN_QUARTERS_PER_FIRM.
3. Residuen ε extrahieren.
4. Spearman-CCF auf ε mit Lags −4…+4.
5. Aggregation (Median, Fisher-z-Mean), Pair-Bootstrap-CIs (95 % + Bonferroni),
   FDR, Peak-Lags — identisch zu lead_lag_v2.py.

Outputs landen in v2/output/interdependence/ bzw. v2/output/plots/ mit dem
Suffix "_prewhitened".
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
import statsmodels.api as sm
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from interdependence import BLOCK_DEFS, RATIO_LABEL  # noqa: E402

# Lokale Konfiguration ausleihen
sys.path.insert(0, str(HERE))
from lead_lag_v2 import (  # noqa: E402
    MAIN_RATIOS, LAGS, MIN_QUARTERS_PER_FIRM, MIN_OBS_PER_FIRM,
    BOOTSTRAP_B, BOOTSTRAP_SEED, CI_LEVEL, ALPHA, N_TESTS_BONF,
    CI_LEVEL_BONF, PANEL_CSV, V2_OUT_INTERDEP, V2_OUT_PLOTS,
    _shifted_spearman, _bootstrap_median_ci, _bootstrap_median_ci_dual,
    _fisher_z_mean, _bh_fdr_significant, _classify_interpretation,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────
# AR(1)-Pre-Whitening
# ─────────────────────────────────────────────────────────────────────────

def _ar1_residuals(diff_series: np.ndarray) -> np.ndarray | None:
    """Fittet AR(1) auf ΔY und gibt Residuen-Array (gleicher Länge wie Input)
    mit NaN an den Stellen zurück, an denen kein Residuum existiert
    (führender Wert + alle NaN-Eingaben).
    """
    s = pd.Series(diff_series)
    valid = s.dropna()
    if len(valid) < MIN_QUARTERS_PER_FIRM:
        return None
    y = valid.values[1:]
    x = valid.values[:-1]
    if len(y) < 5:
        return None
    X = sm.add_constant(x)
    try:
        res = sm.OLS(y, X, missing="drop").fit()
    except Exception:
        return None
    c, phi = float(res.params[0]), float(res.params[1])
    eps = np.full_like(diff_series, fill_value=np.nan, dtype=float)
    # Residuen den Original-Indizes zuweisen — wir brauchen die Position
    # innerhalb des Original-Arrays
    valid_idx = np.where(~np.isnan(diff_series))[0]
    # ε(t) ab t = valid_idx[1] (das erste valid hat keinen Vorgänger)
    for i in range(1, len(valid_idx)):
        pos = valid_idx[i]
        prev_val = diff_series[valid_idx[i - 1]]
        eps[pos] = diff_series[pos] - c - phi * prev_val
    return eps


def compute_per_firm_prewhitened(panel: pd.DataFrame) -> pd.DataFrame:
    """Pro Ticker × Paar × Lag Spearman auf AR(1)-Residuen der ΔY-Reihen."""
    panel = panel.sort_values(["ticker", "quarter"]).reset_index(drop=True)
    rows: list[dict] = []
    pairs = list(combinations(MAIN_RATIOS, 2))
    grouped = panel.groupby("ticker", sort=False)
    n_tickers = len(grouped)
    for idx, (ticker, sub) in enumerate(grouped, 1):
        if idx % 100 == 0:
            logger.info(f"  Ticker {idx}/{n_tickers} …")
        eps_by_ratio: dict[str, np.ndarray] = {}
        for r in MAIN_RATIOS:
            if r not in sub.columns:
                continue
            diff_arr = sub[r].diff().values
            eps = _ar1_residuals(diff_arr)
            if eps is None:
                continue
            eps_by_ratio[r] = eps
        for a, b in pairs:
            if a not in eps_by_ratio or b not in eps_by_ratio:
                continue
            for k in LAGS:
                rho, pval = _shifted_spearman(
                    eps_by_ratio[a], eps_by_ratio[b], k
                )
                if np.isnan(rho):
                    continue
                rows.append({"ticker": ticker, "ratio_x": a, "ratio_y": b,
                             "lag": k, "rho": rho, "pvalue": pval})
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────
# Aggregation (analog zu v2)
# ─────────────────────────────────────────────────────────────────────────

def aggregate_across_firms(per_firm: pd.DataFrame) -> pd.DataFrame:
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
    out["fdr_bh_significant"] = _bh_fdr_significant(
        out["median_pvalue"].values, alpha=ALPHA
    )
    return out


def extract_peak_lags(long_df: pd.DataFrame) -> pd.DataFrame:
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
        "Lead-Lag-CCF nach AR(1)-Pre-Whitening der ΔY-Reihen\n"
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

    cache_pw = V2_OUT_INTERDEP / "_cache_lead_lag_per_firm_prewhitened.csv"
    if cache_pw.exists():
        logger.info(f"Lade Pre-Whitening-Cache: {cache_pw}")
        per_firm = pd.read_csv(cache_pw)
    else:
        panel = pd.read_csv(PANEL_CSV)
        logger.info(f"Panel geladen: {PANEL_CSV} ({len(panel)} Zeilen)")
        per_firm = compute_per_firm_prewhitened(panel)
        per_firm.to_csv(cache_pw, index=False)
        logger.info(f"Pre-Whitening-Cache gespeichert: {cache_pw}")
    logger.info(f"Per-Firm-Korrelationen: {len(per_firm)} Zeilen")

    long_df = aggregate_across_firms(per_firm)
    long_path = V2_OUT_INTERDEP / "corr_lead_lag_prewhitened.csv"
    long_df.to_csv(long_path, index=False)
    logger.info(f"Long-Form gespeichert: {long_path}")

    peaks = extract_peak_lags(long_df)
    peaks_path = V2_OUT_INTERDEP / "corr_lead_lag_peaks_prewhitened.csv"
    peaks.to_csv(peaks_path, index=False)
    logger.info(f"Peaks gespeichert: {peaks_path}")

    plot_path = V2_OUT_PLOTS / "ff2_lead_lag_heatmap_prewhitened.png"
    _plot_lead_lag_heatmap(peaks, plot_path)

    return {"per_firm": per_firm, "long": long_df, "peaks": peaks}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    print("=" * 70)
    print("  FF2 – Lead-Lag-CCF nach AR(1)-Pre-Whitening der ΔY-Reihen")
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
    print(f"  Heatmap: {V2_OUT_PLOTS}/ff2_lead_lag_heatmap_prewhitened.png")
    print("=" * 70)
