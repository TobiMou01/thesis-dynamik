"""
sector_drift_rolling.py – Rollierender Median pro Sektor (oder Branche)
================================================================================
Untersucht den langfristigen Drift der Kennzahl-Mediane innerhalb jeder
Sektor- (oder Sub-Industry-)Gruppe.

Methodik:
- Pro Gruppe (Sektor oder Branche) wird je Quartal der Median der Kennzahl
  über die zugehoerigen Unternehmen berechnet.
- Auf die so entstehende Aggregat-Zeitreihe wird ein gleitender Median ueber
  ROLLING_WINDOW Quartale gelegt.
- Pro Gruppe x Kennzahl wird zusaetzlich ein linearer Trend (OLS-Regression
  Median(Y) gegen den Quartalsindex) ueber die volle Periode geschaetzt.

Konfiguration (am Anfang der Datei):
- ROLLING_WINDOW     Fensterlaenge in Quartalen
- GROUP_BY           "sector" (zehn GICS-Hauptgruppen) oder "industry" (Sub-Industries)
- MIN_FIRMS_PER_GROUP Mindest-Firmenanzahl pro Gruppe (kleinere Gruppen werden gefiltert)

Outputs in output/ar/sector_drift/:
- median_pro_quartal_<group_by>.csv     Long-Form: group, ratio, quarter, median
- rolling_median_<group_by>.csv         Long-Form: group, ratio, quarter, rolling_median
- trend_pro_gruppe_<group_by>.csv       Slope/R²/p pro Gruppe x Kennzahl
- gruppen_uebersicht_<group_by>.csv     Firmenanzahl pro Gruppe

Outputs in output/plots/sector_drift/:
- drift_rolling_<group_by>_<ratio>.png  Sieben Plots, jeweils ein Plot pro Kennzahl
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from config import OUT_AR, OUT_PLOTS, OUT_RATIOS, RAW_PROFILE, ensure_output_dirs

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────
# Konfiguration (frei anpassbar)
# ─────────────────────────────────────────────────────────────────────────

ROLLING_WINDOW: int = 25            # Quartale, gleitende Median-Fensterlaenge
GROUP_BY: str = "sector"            # "sector" (10 GICS) oder "industry" (Sub)
MIN_FIRMS_PER_GROUP: int = 20       # kleinere Gruppen werden gefiltert

MAIN_RATIOS: list[str] = [
    "ROA", "ROE", "EBIT_margin", "fcf_margin",
    "current_ratio", "debt_to_equity", "equity_ratio",
]

# Krisen-Phasen aus peak_windows.csv fuer visuellen Anker
CRISIS_PHASES: list[tuple[str, str, str]] = [
    ("Dot-Com",  "2000Q4", "2002Q1"),
    ("GFC",      "2008Q4", "2009Q3"),
    ("COVID",    "2020Q1", "2020Q4"),
]

# Deutsche Kennzahl-Bezeichnungen fuer Plot-Titel
RATIO_LABEL: dict[str, str] = {
    "ROA": "ROA",
    "ROE": "ROE",
    "EBIT_margin": "EBIT-Marge",
    "fcf_margin": "FCF-Marge",
    "current_ratio": "Current Ratio",
    "debt_to_equity": "Debt/Equity",
    "equity_ratio": "Eigenkapitalquote",
}


# ─────────────────────────────────────────────────────────────────────────
# Daten-Vorbereitung
# ─────────────────────────────────────────────────────────────────────────

def load_group_assignments(group_by: str = GROUP_BY) -> pd.DataFrame:
    """Liest pro Ticker die Sektor- und Industry-Zuordnung aus den Profil-CSVs.

    Returns
    -------
    DataFrame mit Spalten ticker und group_label (= sector oder industry).
    """
    rows: list[dict] = []
    profile_dir = Path(RAW_PROFILE)
    for f in profile_dir.glob("*.csv"):
        try:
            prof = pd.read_csv(f, nrows=1)
        except Exception:
            continue
        if group_by not in prof.columns:
            continue
        rows.append({
            "ticker": f.stem,
            "group_label": str(prof[group_by].iloc[0]).strip(),
        })
    df = pd.DataFrame(rows)
    df = df[df["group_label"].notna() & (df["group_label"] != "nan")
            & (df["group_label"] != "None")]
    logger.info(f"Group-Zuordnung ({group_by}): {len(df)} Ticker, "
                f"{df['group_label'].nunique()} Gruppen")
    return df


def attach_group(panel: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    """Mergt das Ratio-Panel mit der Group-Zuordnung. Tickers ohne Gruppe fliegen raus."""
    merged = panel.merge(groups, on="ticker", how="inner")
    n_before = panel["ticker"].nunique()
    n_after = merged["ticker"].nunique()
    logger.info(f"Panel: {n_after}/{n_before} Ticker mit Group-Label")
    return merged


def filter_small_groups(merged: pd.DataFrame,
                        min_firms: int = MIN_FIRMS_PER_GROUP) -> pd.DataFrame:
    """Filtert Gruppen mit weniger als min_firms Unternehmen."""
    counts = merged.groupby("group_label")["ticker"].nunique()
    keep = counts[counts >= min_firms].index
    out = merged[merged["group_label"].isin(keep)].copy()
    dropped = sorted(set(counts.index) - set(keep))
    logger.info(f"Filter: {len(keep)} Gruppen mit ≥ {min_firms} Firmen behalten, "
                f"{len(dropped)} kleinere Gruppen verworfen")
    if dropped:
        small_counts = counts.loc[dropped].sort_values()
        logger.info(f"  Verworfene Gruppen: {dict(small_counts)}")
    return out


# ─────────────────────────────────────────────────────────────────────────
# Median & Rolling-Median
# ─────────────────────────────────────────────────────────────────────────

def compute_group_quarter_medians(merged: pd.DataFrame,
                                  ratios: list[str] = MAIN_RATIOS) -> pd.DataFrame:
    """Pro Gruppe und Quartal den Median jeder Kennzahl ueber die Firmen.

    Returns
    -------
    Long-Form DataFrame mit Spalten group, ratio, quarter, median.
    """
    long_rows: list[dict] = []
    for ratio in ratios:
        if ratio not in merged.columns:
            continue
        sub = merged[["ticker", "quarter", "group_label", ratio]].dropna(subset=[ratio])
        agg = (sub.groupby(["group_label", "quarter"])[ratio]
                  .median()
                  .reset_index()
                  .rename(columns={"group_label": "group", ratio: "median"}))
        agg["ratio"] = ratio
        long_rows.append(agg)
    out = pd.concat(long_rows, ignore_index=True)
    return out[["group", "ratio", "quarter", "median"]]


def _rolling_ar1_c(y_series: np.ndarray, window: int) -> np.ndarray:
    """Rolling AR(1)-Drift c pro Position.

    Schaetzt fuer jedes Fenster der Laenge `window` die Gleichung
    ΔY(t) = c + φ · ΔY(t-1) + ε(t)
    und gibt den Intercept c zurueck. Position des Werts: am Ende des Fensters.
    """
    # Erste Differenzen
    dy = np.diff(y_series)
    n = len(dy)
    c_values = np.full(len(y_series), np.nan)
    for i in range(window - 1, n):
        sub = dy[i - window + 1: i + 1]
        # AR(1) auf ΔY: y = ΔY(t), x = ΔY(t-1)
        x = sub[:-1]
        y = sub[1:]
        mask = ~(np.isnan(x) | np.isnan(y))
        if mask.sum() < 10:
            continue
        X = np.column_stack([np.ones(mask.sum()), x[mask]])
        try:
            coefs, *_ = np.linalg.lstsq(X, y[mask], rcond=None)
            c_values[i + 1] = float(coefs[0])  # +1 weil dy[i] entspricht Y[i+1]
        except Exception:
            continue
    return c_values


def compute_rolling_c_per_firm(merged: pd.DataFrame,
                               ratios: list[str] = MAIN_RATIOS,
                               window: int = ROLLING_WINDOW) -> pd.DataFrame:
    """Pro Firma x Kennzahl: rollender AR(1)-c-Wert.

    Returns
    -------
    Long-Form DataFrame mit Spalten ticker, group, ratio, quarter, c.
    """
    logger.info(f"AR(1)-c im Rolling Window ({window}Q) pro Firma berechnen ...")
    panel = merged.sort_values(["ticker", "quarter"]).reset_index(drop=True)
    quarter_order = sorted(panel["quarter"].unique(),
                           key=lambda q: pd.Period(q, freq="Q"))
    qmap = {q: i for i, q in enumerate(quarter_order)}

    rows: list[dict] = []
    grouped = panel.groupby("ticker", sort=False)
    n_tickers = len(grouped)
    for idx, (ticker, sub) in enumerate(grouped, 1):
        if idx % 200 == 0:
            logger.info(f"  Ticker {idx}/{n_tickers} …")
        sub = sub.sort_values("quarter")
        group_label = sub["group_label"].iloc[0]
        quarters = sub["quarter"].tolist()
        for ratio in ratios:
            if ratio not in sub.columns:
                continue
            y = sub[ratio].values
            if np.sum(~np.isnan(y)) < window:
                continue
            c_arr = _rolling_ar1_c(y, window)
            for q, c_val in zip(quarters, c_arr):
                if np.isnan(c_val):
                    continue
                rows.append({
                    "ticker": ticker,
                    "group": group_label,
                    "ratio": ratio,
                    "quarter": q,
                    "c": c_val,
                })
    return pd.DataFrame(rows)


def aggregate_rolling_c_by_group(c_df: pd.DataFrame) -> pd.DataFrame:
    """Median c pro Gruppe x Kennzahl x Quartal ueber die Firmen."""
    agg = (c_df.groupby(["group", "ratio", "quarter"])["c"]
              .agg(["median", "count"])
              .reset_index()
              .rename(columns={"median": "c_median", "count": "n_firms"}))
    return agg


def apply_rolling_median(median_df: pd.DataFrame,
                         window: int = ROLLING_WINDOW) -> pd.DataFrame:
    """Gleitender Median ueber die Aggregat-Zeitreihe pro Gruppe x Kennzahl."""
    quarter_order = sorted(median_df["quarter"].unique(),
                           key=lambda q: pd.Period(q, freq="Q"))
    qmap = {q: i for i, q in enumerate(quarter_order)}
    median_df = median_df.copy()
    median_df["qidx"] = median_df["quarter"].map(qmap)

    rows: list[dict] = []
    for (group, ratio), grp in median_df.groupby(["group", "ratio"], sort=False):
        grp = grp.sort_values("qidx")
        roll = (grp.set_index("qidx")["median"]
                   .rolling(window=window, min_periods=max(5, window // 2),
                            center=True)
                   .median())
        out = grp.copy()
        out["rolling_median"] = roll.values
        rows.append(out)
    return pd.concat(rows, ignore_index=True).drop(columns="qidx")


def compute_linear_trends(median_df: pd.DataFrame) -> pd.DataFrame:
    """Linearer Trend pro Gruppe x Kennzahl ueber die volle Periode."""
    quarter_order = sorted(median_df["quarter"].unique(),
                           key=lambda q: pd.Period(q, freq="Q"))
    qmap = {q: i for i, q in enumerate(quarter_order)}

    rows: list[dict] = []
    for (group, ratio), grp in median_df.groupby(["group", "ratio"], sort=False):
        x = grp["quarter"].map(qmap).astype(float).values
        y = grp["median"].astype(float).values
        mask = ~np.isnan(y)
        if mask.sum() < 10:
            continue
        result = stats.linregress(x[mask], y[mask])
        slope_per_q = float(result.slope)
        trend_25y = slope_per_q * 100  # 25 Jahre = 100 Quartale
        rows.append({
            "group": group,
            "ratio": ratio,
            "slope_per_quarter": round(slope_per_q, 6),
            "trend_25y_total": round(trend_25y, 4),
            "r_squared": round(float(result.rvalue) ** 2, 4),
            "p_value": float(result.pvalue),
            "n_quartale": int(mask.sum()),
        })
    return (pd.DataFrame(rows)
              .sort_values(["ratio", "trend_25y_total"],
                           key=lambda s: s.abs() if s.name == "trend_25y_total" else s,
                           ascending=[True, False])
              .reset_index(drop=True))


# ─────────────────────────────────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────────────────────────────────

def _plot_ratio_group(roll_df: pd.DataFrame, ratios: list[str],
                      group_title: str, out_path: Path, window: int,
                      ncols: int | None = None) -> None:
    """Plot fuer eine Kennzahlgruppe.

    Layout: 1 x len(ratios) Subplots, jeweils mit allen Sektoren als Linien.
    """
    if ncols is None:
        ncols = len(ratios)
    nrows = 1
    fig_width = 6.5 if ncols == 1 else (5.8 * ncols + 2.5)
    fig, axes = plt.subplots(nrows, ncols, figsize=(fig_width, 5.4),
                             squeeze=False, sharex=True)
    axes_flat = axes.flatten()

    cmap = plt.get_cmap("tab10")

    # Quartal-Index global ermitteln
    quarter_order = sorted(roll_df["quarter"].unique(),
                           key=lambda q: pd.Period(q, freq="Q"))
    qmap = {q: i for i, q in enumerate(quarter_order)}
    sorted_groups = sorted(roll_df["group"].unique())

    for i, ratio in enumerate(ratios):
        ax = axes_flat[i]
        sub = roll_df[roll_df["ratio"] == ratio].copy()
        sub["qidx"] = sub["quarter"].map(qmap)
        for k, g in enumerate(sorted_groups):
            s = sub[sub["group"] == g].sort_values("qidx")
            line, = ax.plot(s["qidx"], s["rolling_median"],
                            color=cmap(k % 10), linewidth=1.5)
            if i == ncols - 1:  # Legende nur am letzten Subplot
                line.set_label(g)

        # Krisen-Marker
        for label, start, end in CRISIS_PHASES:
            if start in qmap and end in qmap:
                ax.axvspan(qmap[start] - 0.5, qmap[end] + 0.5,
                           color="grey", alpha=0.18, zorder=0)
        # Jahres-Ticks
        year_ticks = [j for j, q in enumerate(quarter_order)
                      if q.endswith("Q1")][::4]
        year_labels = [quarter_order[j][:4] for j in year_ticks]
        ax.set_xticks(year_ticks)
        ax.set_xticklabels(year_labels, rotation=0, fontsize=9)
        ax.set_xlabel("Quartal", fontsize=10)
        ax.set_ylabel(RATIO_LABEL.get(ratio, ratio), fontsize=10)
        ax.set_title(RATIO_LABEL.get(ratio, ratio), fontsize=11)
        ax.grid(True, alpha=0.25, linestyle=":")
        ax.axhline(0, color="black", linewidth=0.4, alpha=0.4)

    # Krisen-Phasen-Annotation am ersten Subplot (oben mittig)
    ax0 = axes_flat[0]
    for label, start, end in CRISIS_PHASES:
        if start in qmap and end in qmap:
            mid = (qmap[start] + qmap[end]) / 2
            ax0.text(mid, ax0.get_ylim()[1], label,
                     ha="center", va="top", fontsize=8.5, color="dimgrey",
                     bbox=dict(facecolor="white", edgecolor="none",
                               boxstyle="round,pad=0.2", alpha=0.7))

    # Globale Legende rechts neben dem letzten Subplot
    last_ax = axes_flat[-1]
    last_ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5),
                   fontsize=9, frameon=False, title="Sektor")

    fig.suptitle(f"{group_title} — Rollierender Median pro Sektor "
                 f"(Fenster: {window} Quartale)", fontsize=13)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"  Gruppen-Plot: {out_path.name}")


def _plot_one_group(roll_df: pd.DataFrame, group_name: str, out_path: Path,
                    window: int) -> None:
    """Pro Sektor ein Plot mit 7 Subplots (eine pro Kennzahl, eigene y-Achse).

    Layout 2x4, der achte Slot bleibt leer.
    """
    sub = roll_df[roll_df["group"] == group_name].copy()
    if sub.empty:
        return
    quarter_order = sorted(sub["quarter"].unique(),
                           key=lambda q: pd.Period(q, freq="Q"))
    qmap = {q: i for i, q in enumerate(quarter_order)}
    sub["qidx"] = sub["quarter"].map(qmap)

    fig, axes = plt.subplots(2, 4, figsize=(14, 7.5), sharex=True)
    axes_flat = axes.flatten()
    cmap = plt.get_cmap("tab10")

    for i, ratio in enumerate(MAIN_RATIOS):
        ax = axes_flat[i]
        s = sub[sub["ratio"] == ratio].sort_values("qidx")
        if not s.empty:
            ax.plot(s["qidx"], s["rolling_median"],
                    color=cmap(i % 10), linewidth=1.6)
        # Krisen-Marker
        for label, start, end in CRISIS_PHASES:
            if start in qmap and end in qmap:
                ax.axvspan(qmap[start] - 0.5, qmap[end] + 0.5,
                           color="grey", alpha=0.18, zorder=0)
        ax.set_title(RATIO_LABEL.get(ratio, ratio), fontsize=11)
        ax.grid(True, alpha=0.25, linestyle=":")
        ax.axhline(0, color="black", linewidth=0.4, alpha=0.4)

    # Letztes Subplot mit Krisen-Legende fuellen
    ax = axes_flat[7]
    ax.axis("off")
    crisis_text = "Graue Markierungen:\n"
    for label, start, end in CRISIS_PHASES:
        crisis_text += f"  {label}: {start}–{end}\n"
    ax.text(0.05, 0.92, crisis_text, va="top", ha="left",
            fontsize=10, family="monospace")

    # Jahres-Ticks nur auf der unteren Reihe
    year_ticks = [i for i, q in enumerate(quarter_order)
                  if q.endswith("Q1")][::4]
    year_labels = [quarter_order[i][:4] for i in year_ticks]
    for ax in axes[1, :]:
        ax.set_xticks(year_ticks)
        ax.set_xticklabels(year_labels, rotation=0, fontsize=9)
        ax.set_xlabel("Quartal", fontsize=10)

    fig.suptitle(f"{group_name} — Rollierender Median aller Kennzahlen "
                 f"(Fenster: {window} Quartale)", fontsize=13)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"  Sektor-Plot: {out_path.name}")


def _plot_c_one_ratio(c_agg: pd.DataFrame, ratio: str, out_path: Path,
                      window: int) -> None:
    """Plot des AR(1)-c-Medians pro Sektor ueber die Zeit."""
    sub = c_agg[c_agg["ratio"] == ratio].copy()
    if sub.empty:
        return
    groups = sorted(sub["group"].unique())
    quarter_order = sorted(sub["quarter"].unique(),
                           key=lambda q: pd.Period(q, freq="Q"))
    qmap = {q: i for i, q in enumerate(quarter_order)}
    sub["qidx"] = sub["quarter"].map(qmap)

    fig, ax = plt.subplots(figsize=(11, 6))
    cmap = plt.get_cmap("tab10")
    for i, g in enumerate(groups):
        s = sub[sub["group"] == g].sort_values("qidx")
        ax.plot(s["qidx"], s["c_median"], color=cmap(i % 10),
                linewidth=1.5, label=g)

    for label, start, end in CRISIS_PHASES:
        if start in qmap and end in qmap:
            ax.axvspan(qmap[start] - 0.5, qmap[end] + 0.5,
                       color="grey", alpha=0.18, zorder=0)
            mid = (qmap[start] + qmap[end]) / 2
            ax.text(mid, ax.get_ylim()[1], label,
                    ha="center", va="top", fontsize=8.5, color="dimgrey",
                    bbox=dict(facecolor="white", edgecolor="none",
                              boxstyle="round,pad=0.2", alpha=0.7))

    year_ticks = [i for i, q in enumerate(quarter_order) if q.endswith("Q1")][::2]
    year_labels = [quarter_order[i][:4] for i in year_ticks]
    ax.set_xticks(year_ticks)
    ax.set_xticklabels(year_labels, rotation=0)

    ax.set_xlabel("Quartal (Ende des 25Q-Fensters)")
    ax.set_ylabel(f"AR(1)-Drift c — Median pro Sektor")
    ax.set_title(f"{RATIO_LABEL.get(ratio, ratio)} — Rollender AR(1)-Drift c "
                 f"(Fenster: {window} Quartale)", fontsize=12)
    ax.axhline(0, color="black", linewidth=0.5, alpha=0.6)
    ax.grid(True, alpha=0.25, linestyle=":")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5),
              fontsize=9, frameon=False)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"  c-Plot: {out_path.name}")


def _plot_one_ratio(roll_df: pd.DataFrame, ratio: str, out_path: Path,
                    window: int) -> None:
    """Ein Plot pro Kennzahl. Linien pro Gruppe, Krisen-Marker als Schraffuren."""
    sub = roll_df[roll_df["ratio"] == ratio].copy()
    if sub.empty:
        return
    groups = sorted(sub["group"].unique())
    quarter_order = sorted(sub["quarter"].unique(),
                           key=lambda q: pd.Period(q, freq="Q"))
    qmap = {q: i for i, q in enumerate(quarter_order)}
    sub["qidx"] = sub["quarter"].map(qmap)

    fig, ax = plt.subplots(figsize=(11, 6))

    cmap = plt.get_cmap("tab10")
    for i, g in enumerate(groups):
        s = sub[sub["group"] == g].sort_values("qidx")
        ax.plot(s["qidx"], s["rolling_median"], color=cmap(i % 10),
                linewidth=1.5, label=g)

    # Krisen-Schraffuren
    for label, start, end in CRISIS_PHASES:
        if start in qmap and end in qmap:
            ax.axvspan(qmap[start] - 0.5, qmap[end] + 0.5,
                       color="grey", alpha=0.18, zorder=0)
            mid = (qmap[start] + qmap[end]) / 2
            ax.text(mid, ax.get_ylim()[1], label,
                    ha="center", va="top", fontsize=8.5, color="dimgrey",
                    bbox=dict(facecolor="white", edgecolor="none",
                              boxstyle="round,pad=0.2", alpha=0.7))

    # x-Achse mit Jahres-Ticks
    year_ticks = [i for i, q in enumerate(quarter_order)
                  if q.endswith("Q1")][::2]  # alle zwei Jahre
    year_labels = [quarter_order[i][:4] for i in year_ticks]
    ax.set_xticks(year_ticks)
    ax.set_xticklabels(year_labels, rotation=0)

    ax.set_xlabel("Quartal")
    ax.set_ylabel(f"{RATIO_LABEL.get(ratio, ratio)} (Median, gleitend {window}Q)")
    ax.set_title(f"{RATIO_LABEL.get(ratio, ratio)} — Rollierender Median pro Gruppe "
                 f"(Fenster: {window} Quartale)", fontsize=12)
    ax.grid(True, alpha=0.25, linestyle=":")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5),
              fontsize=9, frameon=False)
    ax.axhline(0, color="black", linewidth=0.4, alpha=0.4)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"  Plot: {out_path.name}")


# ─────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────

def run_drift_analysis(group_by: str = GROUP_BY,
                       window: int = ROLLING_WINDOW,
                       min_firms: int = MIN_FIRMS_PER_GROUP) -> dict:
    out_dir = OUT_AR / "sector_drift"
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_dir = OUT_PLOTS / "sector_drift"
    plot_dir.mkdir(parents=True, exist_ok=True)

    # Daten laden
    panel = pd.read_csv(OUT_RATIOS / "ratio_panel.csv")
    logger.info(f"Panel: {len(panel)} Zeilen, {panel['ticker'].nunique()} Ticker")

    groups = load_group_assignments(group_by)
    merged = attach_group(panel, groups)
    merged = filter_small_groups(merged, min_firms)

    # Gruppen-Uebersicht
    overview = (merged.groupby("group_label")["ticker"].nunique()
                .sort_values(ascending=False)
                .reset_index()
                .rename(columns={"group_label": "group", "ticker": "n_firms"}))
    overview_path = out_dir / f"gruppen_uebersicht_{group_by}.csv"
    overview.to_csv(overview_path, index=False)
    logger.info(f"Gruppen-Uebersicht: {overview_path}")

    # Aggregation: Median pro Gruppe x Quartal x Kennzahl
    median_df = compute_group_quarter_medians(merged)
    median_path = out_dir / f"median_pro_quartal_{group_by}.csv"
    median_df.to_csv(median_path, index=False)
    logger.info(f"Median pro Quartal: {median_path}")

    # Rolling-Median
    roll_df = apply_rolling_median(median_df, window=window)
    roll_path = out_dir / f"rolling_median_{group_by}.csv"
    roll_df.to_csv(roll_path, index=False)
    logger.info(f"Rolling-Median: {roll_path}")

    # Lineare Trends
    trends = compute_linear_trends(median_df)
    trend_path = out_dir / f"trend_pro_gruppe_{group_by}.csv"
    trends.to_csv(trend_path, index=False)
    logger.info(f"Trend-Tabelle: {trend_path}")

    # Plots Niveau-Median, Variante A: pro Kennzahl alle Sektoren
    for ratio in MAIN_RATIOS:
        plot_path = plot_dir / f"drift_rolling_{group_by}_{ratio}.png"
        _plot_one_ratio(roll_df, ratio, plot_path, window)

    # Plots Niveau-Median, Variante B: pro Sektor alle Kennzahlen
    for group_name in sorted(roll_df["group"].unique()):
        safe = group_name.replace("/", "-").replace(" ", "_")
        plot_path = plot_dir / f"by_group_{group_by}_{safe}.png"
        _plot_one_group(roll_df, group_name, plot_path, window)

    # Plots Niveau-Median, Variante C: vier Kennzahlgruppen mit Subplots
    ratio_groups = [
        ("Renditen",        ["ROA", "ROE"],                            "01_renditen"),
        ("Margen",          ["EBIT_margin", "fcf_margin"],             "02_margen"),
        ("Liquidität",      ["current_ratio"],                         "03_liquiditaet"),
        ("Kapitalstruktur", ["debt_to_equity", "equity_ratio"],        "04_kapitalstruktur"),
    ]
    for group_title, ratios, fname in ratio_groups:
        plot_path = plot_dir / f"gruppe_{fname}_{group_by}.png"
        _plot_ratio_group(roll_df, ratios, group_title, plot_path, window)

    # AR(1)-c im Rolling Window pro Firma + Aggregat pro Gruppe
    c_df = compute_rolling_c_per_firm(merged, window=window)
    c_path = out_dir / f"rolling_c_per_firm_{group_by}.csv"
    c_df.to_csv(c_path, index=False)
    logger.info(f"Rolling-c pro Firma: {c_path}")

    c_agg = aggregate_rolling_c_by_group(c_df)
    c_agg_path = out_dir / f"rolling_c_per_group_{group_by}.csv"
    c_agg.to_csv(c_agg_path, index=False)
    logger.info(f"Rolling-c pro Gruppe: {c_agg_path}")

    # Plots c-Median
    for ratio in MAIN_RATIOS:
        c_plot_path = plot_dir / f"rolling_c_{group_by}_{ratio}.png"
        _plot_c_one_ratio(c_agg, ratio, c_plot_path, window)

    return {
        "overview": overview,
        "median_df": median_df,
        "rolling_df": roll_df,
        "trends": trends,
        "c_df": c_df,
        "c_agg": c_agg,
    }


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

    print("=" * 72)
    print("  Aggregat-Drift pro Gruppe — Rollierender Median")
    print(f"  GROUP_BY = {GROUP_BY}   |   ROLLING_WINDOW = {ROLLING_WINDOW}")
    print(f"  MIN_FIRMS_PER_GROUP = {MIN_FIRMS_PER_GROUP}")
    print("=" * 72)

    result = run_drift_analysis()

    print()
    print("Gruppen-Uebersicht:")
    print(result["overview"].to_string(index=False))

    print()
    print("Top-10 staerkste Trends (nach |Trend ueber 25 J|):")
    top = (result["trends"]
           .assign(abs_trend=lambda d: d["trend_25y_total"].abs())
           .sort_values("abs_trend", ascending=False)
           .head(10)
           .drop(columns="abs_trend"))
    print(top.to_string(index=False))

    print()
    print("=" * 72)
    print(f"  Outputs:   output/ar/sector_drift/")
    print(f"  Plots:     output/plots/sector_drift/")
    print("=" * 72)
